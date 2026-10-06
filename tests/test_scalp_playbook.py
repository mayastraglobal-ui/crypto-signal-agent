"""Step 3b: the operator's playbook definitions (engine/scalp_playbook.py) - candles, structure, regime, levels, sessions,
CVD - checked on hand-made candles, and the whole set checked for look-ahead on synthetic data."""
import os
import sys
import unittest

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import scanner as sc  # noqa: E402
from engine import flow_history as fh  # noqa: E402
from engine import scalp_playbook as pb  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402
from engine.timeframes import TF_MS  # noqa: E402

DAY = 86_400_000
T0 = 1_790_640_000_000 // DAY * DAY          # a UTC midnight (2026-09-29, a Tuesday)


def frame(rows, tf="5m", t0=T0, vol=None):
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"], dtype=float)
    df["open_time"] = t0 + np.arange(len(df)) * TF_MS[tf]
    df["close_time"] = df["open_time"] + TF_MS[tf] - 1
    df["volume"] = 1.0 if vol is None else vol
    return df


class Candles(unittest.TestCase):
    def test_rejection_engulfing_exact_definitions(self):
        P = pb.settings()
        rows = [(100, 100.2, 99.0, 99.2),          # bearish
                (99.1, 100.0, 97.0, 99.8),          # lower wick 2.1/3.0 = 70%, close in the top third
                (99.8, 100.0, 99.0, 99.5),
                (99.4, 100.4, 99.3, 100.3)]         # engulfs the bearish candle before (body 0.9 >= 1.2 x 0.3)
        df = frame(rows)
        cd = pb.candles(df, np.full(4, 1.0), P)
        self.assertEqual(cd["bull_rej"].tolist(), [False, True, False, False])
        self.assertTrue(cd["bull_eng"][3])
        small = pb.candles(df, np.full(4, 10.0), P)        # range < 0.6 x ATR: not a rejection
        self.assertFalse(small["bull_rej"][1])

    def test_round_numbers(self):
        lo, hi = pb.round_levels(np.array([61_234.0, 2_567.0, 148.3]))
        self.assertEqual(lo.tolist(), [61_000.0, 2_500.0, 140.0])
        self.assertEqual(hi.tolist(), [62_000.0, 2_600.0, 150.0])


class Structure(unittest.TestCase):
    def test_pivots_are_known_n_candles_later_and_bos(self):
        up = [100, 102, 101, 104, 103, 106, 105, 108, 107, 110, 109, 112, 111, 114, 113, 116]
        rows = [(x, x + 0.5, x - 0.5, x) for x in up]
        df = frame(rows, "1h")
        ih, vh, il, vl = pb.swings(df["high"].to_numpy(), df["low"].to_numpy(), 1)
        self.assertTrue(np.isnan(vh[1]))                    # the high at 1 is confirmed at 2
        self.assertEqual(vh[2], 102.5)
        ev, sq = pb.structure(df, 1)
        self.assertEqual(sq[-1], 1)                         # higher highs and higher lows
        self.assertEqual(ev[-1], 1)                         # the last event: a bullish BOS
        down = frame([(x, x + 0.5, x - 0.5, x) for x in up[::-1]], "1h")
        ev, sq = pb.structure(down, 1)
        self.assertEqual((sq[-1], ev[-1]), (-1, -1))

    def test_regime_trend_and_bias_on_a_steady_uptrend(self):
        n = 400
        c = 100 * np.exp(np.cumsum(np.full(n, 0.004)) + 0.002 * np.sin(np.arange(n)))
        df = frame([(x * 0.999, x * 1.004, x * 0.996, x) for x in c], "1h")
        r = pb.regime_1h(df, pb.settings())
        self.assertEqual(r["trend_1h"][-1], 1.0)
        self.assertEqual(r["adx_low"][-1], 0.0)


class Levels(unittest.TestCase):
    def test_day_week_and_asia_levels(self):
        n = 2 * 288 + 120                                  # two days and 10 hours of 5m candles
        x = 100 + np.arange(n) * 0.01
        d5 = frame([(v, v + 0.05, v - 0.05, v) for v in x])
        d15 = frame([(v, v + 0.1, v - 0.1, v) for v in x[::3]], "15m")
        lv = pb.day_levels(d5, d15)
        i = 288 + 10                                        # day 2, 00:50
        self.assertAlmostEqual(lv["pdh"][i], x[287] + 0.05)
        self.assertAlmostEqual(lv["pdl"][i], x[0] - 0.05)
        self.assertTrue(np.isnan(lv["asia_h"][288 + 83]))   # 06:55 - Asia not over yet
        self.assertAlmostEqual(lv["asia_h"][288 + 84], x[288 + 83] + 0.05)   # 07:00 - known now
        self.assertTrue(np.isfinite(lv["poc"][i]))          # the previous day's profile
        self.assertTrue(np.isnan(lv["poc"][10]))            # no previous day
        self.assertEqual(lv["wk_open"][i], x[0])            # same week (Tuesday start of data)

    def test_live_window_with_daily_candles_gives_the_backtest_levels(self):
        n = 10 * 288                                         # 10 days of 5m candles
        x = 100 + np.sin(np.arange(n) / 50.0) * 3 + np.arange(n) * 0.001
        d5 = frame([(v, v + 0.05, v - 0.05, v) for v in x])
        d15 = frame([(v, v + 0.1, v - 0.1, v) for v in x[::3]], "15m")
        g = d5.assign(d=d5["open_time"] // DAY).groupby("d")
        d1 = pd.DataFrame({"open_time": g["open_time"].first(), "open": g["open"].first(), "high": g["high"].max(),
                           "low": g["low"].min(), "close": g["close"].last()}).reset_index(drop=True)
        full = pb.day_levels(d5, d15)
        tail = d5.tail(500).reset_index(drop=True)            # what the live watcher holds (~41 hours)
        live = pb.day_levels(tail, d15, d1[d1["open_time"] <= int(tail["open_time"].iloc[-1])])
        for k in ("pdh", "pdl", "wk_open", "mo_open", "pwh", "pwl"):
            np.testing.assert_allclose(live[k][-100:], full[k][-100:], err_msg=k)

    def test_cvd_resets_at_midnight(self):
        ot = T0 + np.arange(5) * DAY // 2
        self.assertEqual(pb._cvd(np.array([1.0, 2.0, 3.0, 4.0, 5.0]), ot).tolist(), [1.0, 3.0, 3.0, 7.0, 5.0])


class Flow(unittest.TestCase):
    def test_delta_from_binance_taker_volume_and_alignment(self):
        import io
        import zipfile
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("x.csv", "open_time,open,high,low,close,volume,close_time,quote_volume,count,taker_buy_volume,"
                                "taker_buy_quote_volume,ignore\n1000,1,1,1,1,10,1299,1,1,7,1,0\n1300,1,1,1,1,4,1599,1,1,1,1,0\n")
        df = fh.parse_vision(buf.getvalue())
        self.assertEqual(df["delta"].tolist(), [4.0, -2.0])          # 2 x 7 - 10, 2 x 1 - 4
        self.assertEqual(fh.align([1000, 1300, 1600], df).tolist()[:2], [4.0, -2.0])
        self.assertTrue(np.isnan(fh.align([1000, 1300, 1600], df)[2]))


class NoLookAhead(unittest.TestCase):
    def test_every_column_is_the_same_when_the_future_is_cut_off(self):
        f = sc.Synthetic(seed=3)
        d5 = f.klines("BTCUSDT", "5m", 3000).reset_index(drop=True)
        d15 = f.klines("BTCUSDT", "15m", 1200).reset_index(drop=True)
        d1h = f.klines("BTCUSDT", "1h", 600).reset_index(drop=True)
        delta = np.random.default_rng(1).normal(0, 1, len(d5))
        full = pb.compute(d5, d15, d1h, delta=delta)
        cut_ms = int(d5["close_time"].iloc[2400])
        c5, c15, c1 = (d[d["close_time"] <= cut_ms].reset_index(drop=True) for d in (d5, d15, d1h))
        part = pb.compute(c5, c15, c1, delta=delta[:len(c5)])
        for k in pb.COLUMNS:
            a, b = np.asarray(full[k], dtype=float)[:len(c5)], np.asarray(part[k], dtype=float)
            same = (a == b) | (np.isnan(a) & np.isnan(b))
            self.assertTrue(same[-300:].all(), f"{k} changes when later candles are added")

    def test_cards_load_and_use_only_known_columns(self):
        cards, problems, _, _ = sc.load_cards()
        self.assertEqual(problems, {})
        pbc = [c for c in cards if c["id"].startswith("PB-")]
        self.assertEqual(len(pbc), 6)
        for c in pbc:
            self.assertEqual((c["gate"], c["timeframes"]), ("playbook", ["5m"]))
            used = SP.columns_needed(c) | {n for r in c["long"] + c["short"] + (c.get("exit_long") or []) +
                                           (c.get("exit_short") or []) for n in SP._names(r)}
            self.assertTrue(used <= set(pb.COLUMNS), used - set(pb.COLUMNS))
        by = {c["id"]: c for c in pbc}
        for a, b in (("PB-B-SWEEP", "PB-B-SWEEP-noCVD"), ("PB-C-BREAKOUT", "PB-C-BREAKOUT-noCVD"),
                     ("PB-A-PULLBACK-CVD", "PB-A-PULLBACK")):
            diff = [k for k in SP.LOGIC_KEYS if k not in ("long", "short") and by[a].get(k) != by[b].get(k)]
            self.assertEqual(diff, [], (a, b))                        # the twins differ only in the CVD rule


if __name__ == "__main__":
    unittest.main()
