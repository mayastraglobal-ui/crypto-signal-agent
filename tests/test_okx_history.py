"""Roadmap step 2 (operator request 2026-10-06): OKX USDT-perpetual candle history for the scalping timeframes,
and real funding for longs. Offline: a fake OKX (files + REST) built from one made-up 1-minute price series."""
import datetime as dt
import io
import os
import sys
import tempfile
import unittest
import zipfile

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import scanner as sc  # noqa: E402
from engine import derivs as dv  # noqa: E402
from engine import okx_history as oh  # noqa: E402

MIN = 60_000
CN = dt.timezone(dt.timedelta(hours=8))


def cn_ms(*a):
    return int(dt.datetime(*a, tzinfo=CN).timestamp() * 1000)


def minutes(a, b):
    """The made-up 1-minute candles from a to b (ms)."""
    t = np.arange(a, b, MIN, dtype=np.int64)
    i = t // MIN
    c = 100 + np.sin(i / 37.0) * 5 + (i % 11) * 0.01
    o = np.r_[c[0], c[:-1]] if len(c) else c
    return pd.DataFrame(dict(open_time=t, open=o, high=np.maximum(o, c) + 0.05, low=np.minimum(o, c) - 0.05, close=c,
                             vol=1.0, vol_ccy=0.01 * (1 + i % 3), vol_quote=c * 0.01 * (1 + i % 3)))


def zipped(df, confirm=1):
    out = df.assign(instrument_name="BTC-USDT-SWAP", confirm=confirm)[
        ["instrument_name", "open", "high", "low", "close", "vol", "vol_ccy", "vol_quote", "open_time", "confirm"]]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("x.csv", out.to_csv(index=False))
    return buf.getvalue()


class R:
    def __init__(self, code, content=b"", js=None):
        self.status_code, self.content, self._js = code, content, js

    def json(self):
        return self._js


class FakeOKX:
    """Month files: missing_months -> 404; day files for every day; REST: candles before `after`."""

    def __init__(self, now, missing_months=(), missing_days=()):
        self.now, self.missing_months, self.missing_days, self.calls = now, set(missing_months), set(missing_days), []

    def __call__(self, url, params=None):
        self.calls.append(url)
        if "/monthly/" in url:
            ym = url.rsplit("-candlesticks-", 1)[1][:7]
            if ym in self.missing_months:
                return R(404)
            a, b = oh.month_span(ym)
            return R(200, zipped(minutes(a, b)))
        if "/daily/" in url:
            ymd = url.rsplit("-candlesticks-", 1)[1][:10]
            if ymd in self.missing_days:
                return R(404)
            a = cn_ms(*map(int, ymd.split("-")))
            return R(200, zipped(minutes(a, a + 86_400_000)))
        tf = {"5m": "5m", "15m": "15m", "30m": "30m"}[params["bar"]]
        step = sc.TF_MS[tf]
        end = int(params.get("after") or (self.now // step * step))
        m = minutes(end - 100 * step, end)
        c = oh.resample(m.rename(columns={"vol_ccy": "volume", "vol_quote": "quote_volume"}), tf, end)
        rows = [[str(int(r.open_time)), r.open, r.high, r.low, r.close, 0, r.volume, r.quote_volume, "1"]
                for r in c.itertuples()][::-1]
        rows = [r for r in rows if int(r[0]) + step <= self.now] if not params.get("after") else rows
        return R(200, js={"code": "0", "data": rows})


class Calendar(unittest.TestCase):
    def test_months_and_days_follow_beijing_time(self):
        self.assertEqual(oh.month_span("2026-03")[0], cn_ms(2026, 3, 1))
        self.assertEqual(dt.datetime.fromtimestamp(oh.month_span("2026-03")[0] / 1000, dt.timezone.utc).hour, 16)
        self.assertEqual(oh.months(cn_ms(2026, 1, 15), cn_ms(2026, 3, 5)), ["2026-01", "2026-02"])
        self.assertEqual(oh.months(cn_ms(2026, 1, 15), cn_ms(2026, 3, 1)), ["2026-01", "2026-02"])
        self.assertEqual(oh.days(cn_ms(2026, 3, 1, 5), cn_ms(2026, 3, 3, 1)), ["2026-03-01", "2026-03-02"])
        self.assertIn("/monthly/202603/BTC-USDT-SWAP-candlesticks-2026-03.zip", oh.month_url("BTC", "2026-03"))
        self.assertIn("/daily/20260302/BTC-USDT-SWAP-candlesticks-2026-03-02.zip", oh.day_url("BTC", "2026-03-02"))

    def test_resample_adds_up_minutes_and_never_keeps_a_half_candle(self):
        a = cn_ms(2026, 3, 1)
        m = minutes(a, a + 47 * MIN)                     # 3 whole 15m candles + 2 minutes
        r = oh.resample(m.rename(columns={"vol_ccy": "volume", "vol_quote": "quote_volume"}), "15m")
        self.assertEqual(len(r), 3)
        self.assertEqual(int(r["open_time"].iloc[0]) % sc.TF_MS["15m"], 0)
        first = m.iloc[:15]
        self.assertEqual(r["open"].iloc[0], first["open"].iloc[0])
        self.assertEqual(r["close"].iloc[0], first["close"].iloc[14])
        self.assertEqual(r["high"].iloc[0], first["high"].max())
        self.assertAlmostEqual(r["volume"].iloc[0], first["vol_ccy"].sum())

    def test_parse_reads_okx_columns(self):
        a = cn_ms(2026, 3, 1)
        df = oh.parse_zip(zipped(minutes(a, a + 5 * MIN)))
        self.assertEqual(list(df.columns), oh.COLS)
        self.assertEqual(len(df), 5)
        self.assertAlmostEqual(df["volume"].iloc[0], 0.01 * (1 + (a // MIN) % 3))

    def test_archive_rows_count_even_when_marked_unconfirmed(self):
        """OKX's older month files say confirm = 0 on every row (e.g. 2023-10): the month is over, so they are closed
        candles - dropping them left months-long holes in the 5-year history (2026-10-09). A repeated minute counts
        once."""
        a = cn_ms(2023, 10, 1)
        m = minutes(a, a + 5 * MIN)
        df = oh.parse_zip(zipped(pd.concat([m, m.tail(1)]), confirm=0))
        self.assertEqual(len(df), 5)
        self.assertTrue(df["open_time"].is_monotonic_increasing)


class Download(unittest.TestCase):
    def test_files_then_rest_cached_and_continuous(self):
        now = cn_ms(2026, 3, 5, 10, 7)
        fake = FakeOKX(now, missing_months={"2025-12", "2026-02"})       # Dec: before listing; Feb: not out yet
        with tempfile.TemporaryDirectory() as d:
            h = oh.History(d, get=fake, sleep=lambda s: None)
            out, note = h.coin("BTC", {"5m": 20_000, "15m": 3000}, now)
            idx = h.index["BTC"]
            self.assertEqual(idx["months"].get("2025-12"), "missing")      # ended > 45 days ago: never comes
            self.assertNotIn("2026-02", idx["months"])                       # recent: tried again next run
            self.assertEqual(idx["months"]["2026-01"], "ok")
            self.assertIn("2026-02-10", idx["days"])                         # Feb covered by day files meanwhile
            m5 = out["5m"]
            self.assertEqual(int(m5["open_time"].min()), cn_ms(2026, 1, 1))  # first OKX candle (Dec missing)
            gaps = np.diff(m5["open_time"].to_numpy())
            self.assertTrue((gaps == sc.TF_MS["5m"]).all())                  # no hole between month, days and REST
            self.assertLessEqual(int(m5["close_time"].max()), now)           # closed candles only
            self.assertGreaterEqual(int(m5["close_time"].max()), now - sc.TF_MS["5m"])
            self.assertEqual(len(out["15m"]), 3000)                          # the newest 3000 only
            want = oh.resample(minutes(cn_ms(2026, 2, 3), cn_ms(2026, 2, 4)).rename(
                columns={"vol_ccy": "volume", "vol_quote": "quote_volume"}), "5m")
            got = m5.set_index("open_time").loc[want["open_time"]]
            np.testing.assert_allclose(got["close"].to_numpy(), want["close"].to_numpy())
            files = len([u for u in fake.calls if u.endswith(".zip")])
            out2, note2 = oh.History(d, get=fake, sleep=lambda s: None).coin("BTC", {"5m": 20_000, "15m": 3000}, now)
            self.assertEqual(len([u for u in fake.calls if u.endswith(".zip")]) - files, 1)   # only Feb tried again
            self.assertEqual(len(out2["5m"]), len(m5))

    def test_young_listing_is_stitched_to_binance_spot(self):
        step = sc.TF_MS["15m"]
        spot = pd.DataFrame(dict(open_time=np.arange(0, 100) * step, open=1.0, high=1.0, low=1.0, close=1.0,
                                 volume=1.0, quote_volume=1.0))
        okx = pd.DataFrame(dict(open_time=np.arange(60, 120) * step, open=2.0, high=2.0, low=2.0, close=2.0,
                                volume=2.0, quote_volume=2.0))
        df, note = oh.stitch(okx, spot, 100, "15m")
        self.assertEqual(len(df), 100)
        self.assertEqual(df["close"].iloc[-60:].tolist(), [2.0] * 60)        # OKX wins wherever it exists
        self.assertEqual(df["close"].iloc[:40].tolist(), [1.0] * 40)
        self.assertTrue((df["close_time"] == df["open_time"] + step - 1).all())
        self.assertIn("Binance spot before", note)
        self.assertEqual(oh.stitch(okx, spot.iloc[:0], 100, "15m")[1], "OKX perpetual")


class LongFunding(unittest.TestCase):
    def cfg(self, market="futures"):
        with open(os.path.join(ROOT, "config.yaml")) as f:
            c = sc.yaml.safe_load(f)
        c["costs"]["long"]["market"] = market
        for side in ("long", "short"):
            c["costs"][side].update(taker_fee_pct=0, maker_fee_pct=0, slippage_pct=0)
        return c

    def run_long(self, cfg, fund_long):
        n = 10
        o = h = l = c = np.full(n, 100.0)                                     # price never moves: costs only
        return sc.simulate_trade(o, h + 0.1, l - 0.1, c, 0, 1, 100.0, 1.0, cfg, n, 8.0, fund_long=fund_long)

    def test_longs_pay_the_higher_of_config_and_real_funding(self):
        cfg = self.cfg()
        base = self.run_long(cfg, None)["r"]                                 # 0.01% per 8h, 10 bars of 8h
        self.assertAlmostEqual(base, -10 * 0.0001 * 100)
        low = self.run_long(cfg, np.full(10, 0.00005))["r"]                  # real 0.005% < config: never less
        self.assertAlmostEqual(low, base)
        high = self.run_long(cfg, np.full(10, 0.0005))["r"]                  # real 0.05% > config: real is paid
        self.assertAlmostEqual(high, -10 * 0.0005 * 100)
        spot = self.cfg("spot")
        spot["costs"]["long"]["funding_pct_per_8h"] = 0.0
        self.assertAlmostEqual(self.run_long(spot, np.full(10, 0.0005))["r"], 0.0)   # spot longs: no funding

    def test_align_gives_longs_the_positive_rates(self):
        t = np.arange(0, 6) * 8 * 3_600_000
        f = pd.DataFrame(dict(time=t, coin="BTC", source="okx", rate=[0.0003, -0.0002, 0.0001, 0.0, -0.0004, 0.0002]))
        h = pd.DataFrame(columns=dv.HOURLY_COLS)
        a = dv.align(t + 1, t + 1, h, f)
        np.testing.assert_allclose(a["_fund_long"], [0.0003, 0.0, 0.0001, 0.0, 0.0, 0.0002])
        np.testing.assert_allclose(a["_fund_short"], [0.0, 0.0002, 0.0, 0.0, 0.0004, 0.0])


class Config(unittest.TestCase):
    def test_scalping_timeframes_have_two_years_on_okx(self):    # 30m / 15m: 5 years since 2026-10-09
        with open(os.path.join(ROOT, "config.yaml")) as f:
            R = sc.yaml.safe_load(f)["research"]
        self.assertEqual(R["okx_timeframes"], ["30m", "15m", "5m"])
        for tf in ("30m", "15m", "5m"):
            self.assertGreaterEqual(R["history_bars"][tf] * sc.TF_MS[tf], 2 * 365 * 86_400_000 - 86_400_000)


if __name__ == "__main__":
    unittest.main()
