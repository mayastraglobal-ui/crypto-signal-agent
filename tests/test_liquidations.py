"""Liquidation recording (2026-10-28, operator: "build 1+2+3"): OKX keeps only about a day of filled liquidation
orders, so derivs.py records them every hour into reports/liquidations.csv.gz as 5-minute buckets per coin (long /
short USD, counts, the largest). The parser, the buckets, the merge that never counts a liquidation twice and never
shrinks the history, the end-to-end recorder with a fake internet, the report column and the carried file. Also the
TEST alerts limited to 4H / 1H (signal_center alert_tfs)."""
import datetime as dt
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import derivs  # noqa: E402
import publish_live  # noqa: E402
import scanner as sc  # noqa: E402
from engine import derivs as D  # noqa: E402
from engine import signal_center as SCX  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
T0 = 1_793_000_000_000 // 300_000 * 300_000           # a 5-minute boundary (Oct 2026)
M = 60_000


def order(ts, pos, sz, px, side=None):
    return dict(ts=str(ts), posSide=pos, side=side or ("sell" if pos == "long" else "buy"), sz=str(sz), bkPx=str(px))


class Parse(unittest.TestCase):
    def test_usd_side_and_buckets(self):
        page = [dict(details=[order(T0 + M, "long", 2, 80_000), order(T0 + 2 * M, "short", 5, 80_100),
                              order(T0 + 6 * M, "net", 1, 79_000, side="sell"),        # net mode: a forced sell
                              order(T0 + 7 * M, "short", "", 79_000)])]                 # unknown size: skipped
        ev = D.okx_liquidations([page], 0.01)                                           # BTC: 0.01 BTC a contract
        self.assertEqual([(e["long"], round(e["usd"])) for e in ev], [(True, 1600), (False, 4005), (True, 790)])
        rows = D.liq_buckets("BTC", ev)
        self.assertEqual([r["ts"] for r in rows], [T0, T0 + 300_000])
        self.assertEqual((rows[0]["long_usd"], rows[0]["short_usd"], rows[0]["long_n"], rows[0]["short_n"]),
                         (1600.0, 4005.0, 1, 1))
        self.assertEqual(rows[0]["max_usd"], 4005.0)

    def test_the_same_window_twice_is_not_counted_twice(self):
        ev = D.okx_liquidations([[dict(details=[order(T0 + k * M, "long", 1, 100) for k in range(12)])]], 1.0)
        once = D.merge_liq(None, "SOL", ev)
        twice = D.merge_liq(once, "SOL", ev)
        pd.testing.assert_frame_equal(once.reset_index(drop=True), twice.reset_index(drop=True))
        self.assertEqual(float(once["long_usd"].sum()), 1200.0)

    def test_old_buckets_stay_and_the_cut_off_first_bucket_keeps_its_value(self):
        full = D.okx_liquidations([[dict(details=[order(T0 + k * M, "long", 1, 100) for k in range(15)])]], 1.0)
        liq = D.merge_liq(None, "SOL", full)                                      # buckets T0, +5, +10 (5 each)
        later = [e for e in full if e["ts"] >= T0 + 7 * M] + \
            D.okx_liquidations([[dict(details=[order(T0 + 16 * M, "short", 1, 100)])]], 1.0)
        out = D.merge_liq(liq, "SOL", later)                                      # window starts inside T0+5
        by = out.set_index("ts")
        self.assertEqual(by.loc[T0, "long_usd"], 500.0)                           # older: kept
        self.assertEqual(by.loc[T0 + 300_000, "long_usd"], 500.0)                 # cut-off bucket: old value kept
        self.assertEqual(by.loc[T0 + 900_000, "short_usd"], 100.0)                # new
        self.assertGreaterEqual(len(out), len(liq))                               # never shrinks
        other = D.merge_liq(out, "ETH", D.okx_liquidations([[dict(details=[order(T0, "long", 1, 10)])]], 1.0))
        self.assertEqual(set(other["coin"]), {"SOL", "ETH"})

    def test_quality_last_24_hours(self):
        ev = D.okx_liquidations([[dict(details=[order(T0, "long", 1, 100), order(T0 - 30 * 3_600_000, "short", 1, 100)])]], 1.0)
        q = D.liq_quality(D.merge_liq(None, "SOL", ev), "SOL", T0 + M)
        self.assertEqual((q["buckets"], q["long_24h_usd"], q["short_24h_usd"]), (2, 100.0, 0.0))
        self.assertEqual(D.liq_quality(None, "SOL", T0)["buckets"], 0)


class Recorder(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        for name, f in (("HOURLY", "derivs_hourly.csv.gz"), ("FUNDING", "funding.csv.gz"),
                        ("QUALITY", "derivs_quality.json"), ("LIQ", "liquidations.csv.gz"), ("REPORTS", "")):
            p = mock.patch.object(derivs, name, os.path.join(self.tmp, f) if f else self.tmp)
            p.start()
            self.addCleanup(p.stop)
        self.pages = []

    def fetch(self, url, params=None, raw=False):
        if "fapi.binance.com" in url:
            raise OSError("451 Client Error: restricted location")
        if "data.binance.vision" in url:
            raise OSError("404")
        if "instruments" in url:
            return {"data": [dict(instId="BTC-USDT-SWAP", ctVal="0.01")]}
        if "liquidation-orders" in url:
            self.pages.append(params.get("after"))
            if params.get("after"):                                            # page 2: older, then the end
                return {"data": [dict(details=[order(T0 - 10 * M, "short", 10, 80_000)])]} \
                    if int(params["after"]) > T0 - 10 * M else {"data": []}
            return {"data": [dict(details=[order(T0 + M, "long", 100, 80_000), order(T0, "long", 1, 80_000)])]}
        if "funding" in url:
            return {"data": [dict(fundingTime=str(T0), fundingRate="0.0001")]}
        if "open-interest" in url:
            return {"data": [[str(T0), "7e8", "1"]]}
        if "long-short" in url:
            return {"data": [[str(T0), "1.8"]]}
        return {"data": [[str(T0), "100", "120"]]}

    def test_end_to_end_pages_file_and_quality(self):
        now = dt.datetime.fromtimestamp((T0 + 5 * M) / 1000, dt.timezone.utc)
        q = derivs.run(now, self.fetch, ["BTC"])
        self.assertEqual(self.pages[0], None)
        self.assertEqual(self.pages[1], T0)                    # the next page starts below the oldest order seen
        liq = D.read(derivs.LIQ, D.LIQ_COLS)
        self.assertEqual(round(float(liq["long_usd"].sum())), 80_800)          # 101 contracts x 0.01 x 80,000
        self.assertEqual(round(float(liq["short_usd"].sum())), 8_000)
        self.assertEqual(q["BTC"]["liquidations"]["buckets"], 2)
        n = len(liq)
        derivs.run(now, self.fetch, ["BTC"])                                   # the same window again
        self.assertEqual(len(D.read(derivs.LIQ, D.LIQ_COLS)), n)
        self.assertEqual(round(float(D.read(derivs.LIQ, D.LIQ_COLS)["long_usd"].sum())), 80_800)

    def test_a_failing_liquidation_call_never_stops_the_recorder(self):
        def broken(url, params=None, raw=False):
            if "liquidation-orders" in url:
                raise OSError("timeout")
            return self.fetch(url, params, raw)
        q = derivs.run(dt.datetime.fromtimestamp(T0 / 1000, dt.timezone.utc), broken, ["BTC"])
        self.assertEqual(q["BTC"]["fetch"]["source"], "okx")                   # the main series still recorded
        self.assertIn("liquidations: OSError", " ".join(q["BTC"]["fetch"]["errors"]))


class Wiring(unittest.TestCase):
    def test_the_file_is_carried_and_never_committed(self):
        self.assertIn("reports/liquidations.csv.gz", publish_live.LIVE_FILES)
        with open(os.path.join(ROOT, ".gitignore")) as f:
            self.assertIn("reports/liquidations.csv.gz", f.read())

    def test_report_column(self):
        x = dict(liquidations=dict(buckets=3, long_24h_usd=1_411_819, short_24h_usd=25_000))
        self.assertEqual(sc.liq_cell(x), "$1.4M / $25k")
        self.assertEqual(sc.liq_cell({}), "-")


class AlertTimeframes(unittest.TestCase):
    def test_only_4h_and_1h_reach_telegram(self):
        S = SCX.settings(CFG["signal_center"])
        self.assertEqual(S["alert_tfs"], ["4h", "1h"])
        row = dict(n=40, avg_r=0.3, win_rate=50, test_n=10, test_avg_r=0.2)
        cells = {f"P01-BREAKOUT-V1@1.0|{tf}": dict(strategy=1, version="V1", status="BACKTESTING", avg_r=0.3,
                                                   coins={"SOL": row}) for tf in ("4h", "1h", "30m", "15m")}
        p = dict(cells=cells)
        tests = SCX.test_list(p, {}, S)
        self.assertEqual(len(tests), 4)                        # GitHub still records all four silently
        self.assertEqual(sorted(SCX.alert_list(tests, p, {}, S)), ["P01-BREAKOUT-V1@1.0|1h", "P01-BREAKOUT-V1@1.0|4h"])
        self.assertEqual(len(SCX.alert_list(tests, p, {}, dict(S, alert_tfs=[]))), 4)    # [] = every timeframe
        self.assertEqual(SCX.settings(None)["alert_tfs"], [])                           # default: unchanged


if __name__ == "__main__":
    unittest.main()
