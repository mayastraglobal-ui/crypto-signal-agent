"""Phase 6 tests: SMC / ICT detectors (hand-made candles for every concept, no look-ahead, killzones in
summer and winter, the append-only live event log, SMC rows in the candle evidence).

Run:  python -m unittest discover -s tests -v
"""
import datetime as dt
import json
import os
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scanner  # noqa: E402
from engine import features as F  # noqa: E402
from engine import smc as S  # noqa: E402
from test_data_quality import run_copy, shared_offline_run  # noqa: E402

H1, D1 = 3_600_000, 86_400_000
T0 = pd.Timestamp("2025-01-06", tz="UTC").value // 1_000_000        # a Monday 00:00 UTC


def frame(rows, start=T0, tf=H1):
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close", "volume"])
    df["open_time"] = start + tf * np.arange(len(df))
    df["close_time"] = df["open_time"] + tf - 1
    return df


def calm(n, price=100.0):
    """Quiet candles 1 point wide (ATR ~ 1), tiny alternating bodies."""
    return [(price + (0.1 if i % 2 else -0.1), price + 0.5, price - 0.5, price - (0.1 if i % 2 else -0.1), 100.0)
            for i in range(n)]


def run(rows, **kw):
    df = frame(rows)
    return S.detect(df, F.compute(df, H1), tf_ms=H1, **kw)


def kinds(res, event=None):
    return [(e["t"], e["event"], e["dir"]) for e in res["events"] if event is None or e["event"] == event]


def with_peak(n=40, at=20, high=102.0):
    rows = calm(n)
    o, h, l, c, v = rows[at]
    rows[at] = (o, high, l, c, v)
    return rows


class Sweeps(unittest.TestCase):
    def test_buy_side_sweep_needs_wick_through_and_close_back_inside(self):
        rows = with_peak() + [(100.0, 102.4, 99.8, 101.0, 100)]          # wick 0.4 above, closes below
        r = run(rows)
        sw = [e for e in r["events"] if e["event"] == "SWEEP"]
        self.assertEqual(len(sw), 1)
        self.assertEqual(sw[0]["t"], 40)
        self.assertEqual(sw[0]["dir"], -1)                                # buy-side swept = bearish idea
        self.assertEqual(sw[0]["level"], 102.0)
        self.assertIn("buy-side", sw[0]["info"])
        self.assertTrue(r["series"]["sweep_bear"].iloc[40])

    def test_close_beyond_is_not_a_sweep_and_tiny_poke_is_not_either(self):
        self.assertEqual(kinds(run(with_peak() + [(100.0, 102.6, 99.8, 102.4, 100)]), "SWEEP"), [])
        r = run(with_peak() + [(100.0, 102.03, 99.8, 101.0, 100)])
        self.assertEqual(kinds(r, "SWEEP"), [])
        self.assertEqual(r["state"]["liquidity_above"][0]["level"], 102.0)   # tiny poke: pool still there

    def test_pool_is_used_up_and_unconfirmed_swing_is_no_pool(self):
        rows = with_peak() + [(100.0, 102.4, 99.8, 101.0, 100), (100.0, 102.4, 99.8, 101.0, 100)]
        self.assertEqual(len(kinds(run(rows), "SWEEP")), 1)                # swept once only
        rows = with_peak(n=22, at=20) + [(100.0, 102.4, 99.8, 101.0, 100)]  # peak not yet confirmed
        self.assertEqual(kinds(run(rows), "SWEEP"), [])

    def test_sell_side_sweep(self):
        rows = calm(40)
        o, h, l, c, v = rows[20]
        rows[20] = (o, h, 98.0, c, v)
        r = run(rows + [(100.0, 100.2, 97.6, 99.2, 100)])
        self.assertEqual(kinds(r, "SWEEP"), [(40, "SWEEP", 1)])
        self.assertTrue(r["series"]["sweep_bull"].iloc[40])

    def test_equal_highs_pool(self):
        rows = with_peak()
        o, h, l, c, v = rows[30]
        rows[30] = (o, 102.05, l, c, v)                                    # within 0.1% of 102
        r = run(rows)
        self.assertEqual(r["state"]["liquidity_above"][0]["kind"], "equal highs")
        self.assertEqual(r["state"]["liquidity_above"][0]["level"], 102.05)

    def test_previous_day_high_is_a_pool(self):
        day0 = calm(24)
        daily = pd.DataFrame({"open_time": [T0], "close_time": [T0 + D1 - 1], "open": [100.0], "high": [100.5],
                              "low": [99.5], "close": [100.0], "volume": [1.0]})
        rows = day0 + calm(5) + [(100.0, 100.9, 99.8, 100.2, 100)]          # day 1: pokes PDH, closes back
        df = frame(rows)
        r = S.detect(df, F.compute(df, H1), daily=daily, tf_ms=H1)
        sw = [e for e in r["events"] if e["event"] == "SWEEP"]
        self.assertEqual(sw[-1]["t"], 29)
        self.assertIn("PDH", sw[-1]["info"])

    def test_previous_levels_use_only_closed_higher_candles(self):
        daily = pd.DataFrame({"open_time": [T0, T0 + D1], "close_time": [T0 + D1 - 1, T0 + 2 * D1 - 1],
                              "high": [110.0, 120.0], "low": [90.0, 80.0]})
        df = frame(calm(48))                                               # day 0 and day 1
        hi, lo = S.previous_levels(df, daily)
        self.assertTrue(np.isnan(hi[:24]).all())                           # day 0: no previous day yet
        self.assertTrue((hi[24:] == 110.0).all())                          # day 1 sees day 0, never day 1
        self.assertTrue((lo[24:] == 90.0).all())


def zigzag(points, per=4):
    """Candles walking between the given points; each candle opens at the previous close (real bodies)."""
    rows, prev = [], points[0]
    for a, b in zip(points[:-1], points[1:]):
        for x in np.linspace(a, b, per + 1)[1:]:
            rows.append((prev, max(prev, x) + 0.2, min(prev, x) - 0.2, x, 100.0))
            prev = x
    return rows


class Structure(unittest.TestCase):
    UP = [95, 90, 95, 100, 95, 92, 97, 102, 97, 94, 99, 104, 99, 96, 97]      # HH/HL, last swing low ~94

    def test_bos_in_trend_then_choch_with_displacement(self):
        base = zigzag(self.UP)
        r0 = run(base)
        self.assertEqual(r0["state"]["trend"], "up")
        self.assertIn("BOS", [e["event"] for e in r0["events"]])
        crash = [(96.9, 97.0, 91.0, 91.2, 400.0)]                          # big, solid, heavy volume
        r = run(base + crash)
        last = [e for e in r["events"] if e["t"] == len(base)]
        self.assertIn(("CHOCH", -1), [(e["event"], e["dir"]) for e in last])
        self.assertEqual(r["state"]["trend"], "down")
        self.assertTrue(r["series"]["choch_down"].iloc[-1])

    def test_break_without_displacement_is_weak_and_keeps_trend(self):
        base = zigzag(self.UP)
        drift = [(96.8 - 0.5 * i, 97.0 - 0.5 * i, 96.2 - 0.5 * i, 96.3 - 0.5 * i, 100.0) for i in range(6)]
        r = run(base + drift)
        self.assertIn("WEAK_BREAK", [e["event"] for e in r["events"]])
        self.assertNotIn("CHOCH", [e["event"] for e in r["events"]])
        self.assertEqual(r["state"]["trend"], "up")

    def test_order_block_invalidation_and_breaker_retest(self):
        base = zigzag(self.UP)
        crash = [(96.9, 97.0, 91.0, 91.2, 400.0)]
        r = run(base + crash)
        ob = [e for e in r["events"] if e["event"] == "ORDER_BLOCK"]
        self.assertEqual(len(ob), 1)
        self.assertEqual(ob[0]["dir"], -1)
        k = max(i for i, (o, h, l, c, v) in enumerate(base) if c > o)     # last bullish candle before
        self.assertEqual((ob[0]["zone_low"], ob[0]["zone_high"]), (base[k][2], base[k][1]))
        zl, zh = ob[0]["zone_low"], ob[0]["zone_high"]
        up = [(91.5, zh + 1.2, 91.4, zh + 1.0, 100.0)]                    # closes above -> invalid
        back = [(zh + 1.0, zh + 1.1, zl - 0.1, zl + 0.05, 100.0)]          # comes back down into it
        r2 = run(base + crash + up + back)
        ev = [(e["event"], e["dir"]) for e in r2["events"] if e["t"] >= len(base) + 1]
        self.assertIn(("OB_INVALID", -1), ev)
        self.assertIn(("BREAKER_RETEST", 1), ev)

    def test_premium_discount_and_ote(self):
        base = zigzag(self.UP)
        r = run(base)
        rng = r["state"]["dealing_range"]
        self.assertGreater(rng["high"], rng["low"])
        pos = (base[-1][3] - rng["low"]) / (rng["high"] - rng["low"])
        self.assertAlmostEqual(rng["position"], pos)
        self.assertEqual(rng["zone"], "premium" if pos > 0.5 else "discount")
        ote = r["state"]["ote"]
        self.assertEqual(ote["dir"], 1)
        self.assertLess(ote["low"], ote["high"])


class Gaps(unittest.TestCase):
    def test_fvg_retrace_and_fill(self):
        rows = calm(30) + [(100.0, 100.5, 99.8, 100.4, 100), (100.4, 101.8, 100.3, 101.7, 100),
                           (101.7, 102.3, 101.5, 102.2, 100)]              # low 101.5 > high 100.5
        r = run(rows)
        fvg = [e for e in r["events"] if e["event"] == "FVG"]
        self.assertEqual((fvg[-1]["dir"], fvg[-1]["zone_low"], fvg[-1]["zone_high"]), (1, 100.5, 101.5))
        r2 = run(rows + [(102.2, 102.3, 101.2, 101.4, 100), (101.4, 101.5, 100.3, 100.6, 100)])
        ev = [(e["t"], e["event"]) for e in r2["events"] if e["event"] in ("FVG_RETRACE", "FVG_FILLED")]
        self.assertEqual(ev, [(33, "FVG_RETRACE"), (34, "FVG_FILLED")])
        self.assertTrue(r2["series"]["fvg_retrace_bull"].iloc[33])

    def test_tiny_gap_is_ignored(self):
        rows = calm(30) + [(100.0, 100.5, 99.8, 100.4, 100), (100.4, 100.7, 100.3, 100.6, 100),
                           (100.6, 100.9, 100.55, 100.8, 100)]             # gap 0.05 < 0.25 ATR
        self.assertEqual(kinds(run(rows), "FVG"), [])


class PowerOfThree(unittest.TestCase):
    def test_consolidation_sweep_choch(self):
        down = zigzag([110, 115, 108, 112, 105, 109, 102, 104])            # LH/LL: trend down
        box = calm(24, price=103.0)
        o, h, l, c, v = box[10]
        box[10] = (o, h, 101.8, c, v)                                      # a swing low inside the box
        sweep = [(103.0, 103.2, 101.3, 102.9, 100.0)]                      # sell-side sweep, back inside
        rip = [(102.9, 107.8, 102.8, 107.6, 500.0)]                        # displacement up through highs
        r = run(down + box + sweep + rip)
        ev = [(e["event"], e["dir"]) for e in r["events"] if e["t"] >= len(down) + len(box)]
        self.assertIn(("SWEEP", 1), ev)
        self.assertIn(("CHOCH", 1), ev)
        self.assertIn(("AMD", 1), ev)


class Killzones(unittest.TestCase):
    @staticmethod
    def ms(y, m, d, hh, mm):
        return int(dt.datetime(y, m, d, hh, mm, tzinfo=dt.timezone.utc).timestamp() * 1000)

    def test_summer_and_winter_time(self):
        self.assertEqual(S.killzone(self.ms(2026, 7, 15, 6, 30)), "London")      # 02:30 New York (EDT)
        self.assertIsNone(S.killzone(self.ms(2026, 1, 15, 6, 30)))               # 01:30 New York (EST)
        self.assertEqual(S.killzone(self.ms(2026, 1, 15, 7, 30)), "London")      # 02:30 New York (EST)
        self.assertEqual(S.killzone(self.ms(2026, 7, 15, 14, 30)), "Silver Bullet")
        self.assertEqual(S.killzone(self.ms(2026, 7, 15, 12, 0)), "NY AM")
        self.assertEqual(S.killzone(self.ms(2026, 7, 16, 0, 30)), "Asia")        # 20:30 the day before

    def test_no_killzones_above_1h(self):
        df = frame(calm(40), tf=4 * H1)
        r = S.detect(df, F.compute(df, 4 * H1), tf_ms=4 * H1)
        self.assertIsNone(r["state"]["killzone_now"])
        self.assertTrue(all(e["killzone"] is None for e in r["events"]))


class NoLookAhead(unittest.TestCase):
    def test_events_before_t_never_change(self):
        feed = scanner.Synthetic()
        df = feed.klines("BTCUSDT", "1h", 1500)
        d, w = feed.klines("BTCUSDT", "1d", 400), feed.klines("BTCUSDT", "1w", 200)
        full = S.detect(df, F.compute(df, H1), d, w, H1)
        for cut in (500, 901, 1333):
            part = df.iloc[:cut]
            past = S.detect(part, F.compute(part, H1), d, w, H1)
            self.assertEqual([e for e in full["events"] if e["t"] < cut], past["events"], f"cut {cut}")
            pd.testing.assert_frame_equal(full["series"].iloc[:cut], past["series"])


class EventLog(unittest.TestCase):
    def test_watermarks_no_backfill_no_duplicates(self):
        start = dt.datetime(2026, 9, 24, 18, 20, tzinfo=dt.timezone.utc)
        now_ms = int(start.timestamp() * 1000)
        ev = lambda minutes_ago, name: dict(t=0, time=now_ms - minutes_ago * 60_000, event=name, dir=1, level=1.0,
                                            zone_low=None, zone_high=None, size_atr=0.3, killzone=None, info="x")
        res = {("BTC", "15m"): dict(events=[ev(300, "OLD"), ev(30, "NEW1"), ev(10, "NEW2")])}
        rg_series = {("BTC", "1h"): (np.array([now_ms - 7_200_000, now_ms - 3_600_001]),
                                     np.array(["RANGE", "WEAK_BULL"]))}
        s = S.settings({"log_timeframes": ["15m"]})
        with tempfile.TemporaryDirectory() as tmp:
            old = (scanner.MEMORY, scanner.REPORTS)
            scanner.MEMORY, scanner.REPORTS = os.path.join(tmp, "memory"), tmp
            try:
                self.assertEqual(scanner.write_smc_log(res, ["BTC"], s, rg_series, start, "Binance"), 2)
                self.assertEqual(scanner.write_smc_log(res, ["BTC"], s, rg_series, start, "Binance"), 0)
                res[("BTC", "15m")]["events"].append(ev(-5, "NEW3"))
                later = start + dt.timedelta(hours=1)
                self.assertEqual(scanner.write_smc_log(res, ["BTC"], s, rg_series, later, "Binance"), 1)
                log = pd.read_csv(os.path.join(tmp, "memory", "smc_events.csv"))
            finally:
                scanner.MEMORY, scanner.REPORTS = old
        self.assertEqual(list(log["event"]), ["NEW1", "NEW2", "NEW3"])      # no old history, no duplicates
        self.assertEqual(list(log.columns), scanner.SMC_LOG_COLS)
        self.assertEqual(log["htf_regime"].iloc[0], "WEAK_BULL")
        self.assertEqual(log["engine"].iloc[0], S.VERSION)

    def test_offline_run_reports_smc_and_never_logs(self):
        tmp, p = shared_offline_run()          # one plain offline scan, shared (read-only)
        if True:
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertFalse(os.path.exists(os.path.join(tmp, "memory", "smc_events.csv")))
            with open(os.path.join(tmp, "reports", "latest.md")) as f:
                md = f.read()
            self.assertIn("## 0g. SMC now", md)
            with open(os.path.join(tmp, "reports", "smc.json")) as f:
                g = json.load(f)
            self.assertEqual(set(g["coins"]["BTC"]), {"4h", "1h", "30m", "15m", "5m"})
            with open(os.path.join(tmp, "reports", "feature_evidence.json")) as f:
                e = json.load(f)
            for pat in scanner.SMC_PATTERNS:
                self.assertIn(pat, e["timeframes"]["15m"])
                r = e["timeframes"]["15m"][pat]
                self.assertEqual(r["random_events"], 10 * r["events"])


if __name__ == "__main__":
    unittest.main()
