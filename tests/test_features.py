"""Phase 4 tests: feature engine (no look-ahead, exact definitions) and the candle evidence tool
(patterns vs random entries - research evidence, not a signal).

Run:  python -m unittest discover -s tests -v
"""
import json
import os
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scanner  # noqa: E402
from engine import evidence as E  # noqa: E402
from engine import features as F  # noqa: E402
from test_data_quality import run_copy  # noqa: E402

H1 = 3_600_000
T0 = 1_750_000_000_000 // H1 * H1


def frame(rows):
    """Candles from (open, high, low, close, volume) tuples, one hour apart."""
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close", "volume"])
    df["open_time"] = T0 + H1 * np.arange(len(df))
    df["close_time"] = df["open_time"] + H1 - 1
    return df


def calm(n, price=100.0, vol=100.0):
    """Quiet candles: every candle 1 point wide, small bodies alternating up/down."""
    rows = []
    for i in range(n):
        o = price + (0.1 if i % 2 else -0.1)
        c = price - (0.1 if i % 2 else -0.1)
        rows.append((o, price + 0.5, price - 0.5, c, vol))
    return rows


def synthetic(coin="BTCUSDT", tf="1h", n=1200):
    return scanner.Synthetic().klines(coin, tf, n)


class NoLookAhead(unittest.TestCase):
    def test_every_feature_ignores_the_future(self):
        df = synthetic(n=900)
        full = F.compute(df, H1)
        for cut in (250, 511, 777):
            past = F.compute(df.iloc[:cut], H1)
            pd.testing.assert_frame_equal(full.iloc[:cut], past, check_dtype=False, obj=f"cut {cut}")

    def test_swing_is_invisible_until_confirmed(self):
        rows = calm(40)
        o, h, l, c, v = rows[20]
        rows[20] = (o, 110.0, l, c, v)                          # a clear peak at candle 20
        f = F.compute(frame(rows), H1)
        k = F.DEFAULTS["swing_n"]
        self.assertFalse(f["swing_high"].iloc[20:20 + k].any())  # not known yet
        self.assertTrue(f["swing_high"].iloc[20 + k])             # known 3 candles later
        self.assertEqual(f["swing_high_price"].iloc[20 + k], 110.0)
        early = F.compute(frame(rows).iloc[:20 + k], H1)          # stop right before confirmation
        self.assertFalse(early["swing_high"].any())


class Definitions(unittest.TestCase):
    def test_candle_shape(self):
        f = F.compute(frame([(100, 110, 90, 105, 1)]), H1).iloc[0]
        self.assertAlmostEqual(f["body_pct"], 0.25)
        self.assertAlmostEqual(f["upper_wick_pct"], 0.25)
        self.assertAlmostEqual(f["lower_wick_pct"], 0.5)
        self.assertAlmostEqual(f["close_loc"], 0.75)

    def test_displacement_needs_size_body_and_volume(self):
        base = calm(40)
        big = (100.0, 103.2, 99.9, 103.0, 200.0)                # 3.3x ATR, body 94%, volume 2x
        f = F.compute(frame(base + [big]), H1)
        self.assertTrue(f["displacement_up"].iloc[-1])
        quiet = (100.0, 103.2, 99.9, 103.0, 100.0)              # same candle, normal volume
        self.assertFalse(F.compute(frame(base + [quiet]), H1)["displacement_up"].iloc[-1])
        wicky = (100.0, 104.0, 97.0, 101.0, 200.0)              # big range but body only 14%
        self.assertFalse(F.compute(frame(base + [wicky]), H1)["displacement_up"].iloc[-1])
        down = (103.0, 103.1, 99.8, 100.0, 200.0)
        f = F.compute(frame(base + [down]), H1)
        self.assertTrue(f["displacement_down"].iloc[-1])
        self.assertFalse(f["displacement_up"].iloc[-1])

    def test_engulfing(self):
        rows = calm(10) + [(101.0, 101.2, 99.8, 100.0, 1), (99.9, 101.5, 99.7, 101.3, 1)]
        f = F.compute(frame(rows), H1)
        self.assertTrue(f["bull_engulf"].iloc[-1])
        self.assertFalse(f["bear_engulf"].iloc[-1])
        rows = calm(10) + [(100.0, 101.2, 99.8, 101.0, 1), (101.1, 101.3, 99.5, 99.7, 1)]
        self.assertTrue(F.compute(frame(rows), H1)["bear_engulf"].iloc[-1])
        rows = calm(10) + [(101.0, 101.2, 99.8, 100.0, 1), (100.2, 100.9, 100.1, 100.8, 1)]  # inside
        self.assertFalse(F.compute(frame(rows), H1)["bull_engulf"].iloc[-1])

    def test_pin_bars(self):
        f = F.compute(frame(calm(5) + [(100.0, 100.3, 97.0, 100.2, 1)]), H1).iloc[-1]
        self.assertTrue(f["bull_reject"])                         # long lower wick, closes near the top
        self.assertFalse(f["bear_reject"])
        f = F.compute(frame(calm(5) + [(100.0, 103.0, 99.7, 99.8, 1)]), H1).iloc[-1]
        self.assertTrue(f["bear_reject"])
        f = F.compute(frame(calm(5) + [(100.0, 100.3, 97.0, 98.0, 1)]), H1).iloc[-1]
        self.assertFalse(f["bull_reject"])                        # long wick but closed low

    def test_structure_hh_hl_and_divergence(self):
        # zig-zag up: lows 90, 92, 94 and highs 100, 102, 104 -> HH / HL -> "up"
        pts = [95, 90, 95, 100, 95, 92, 97, 102, 97, 94, 99, 104, 99, 96]
        rows = []
        for a, b in zip(pts[:-1], pts[1:]):
            for x in np.linspace(a, b, 5)[:-1]:
                rows.append((x, x + 0.2, x - 0.2, x, 1))
        f = F.compute(frame(rows + calm(6, price=96)), H1)
        self.assertEqual(f["swing_high_label"].iloc[-1], "HH")
        self.assertEqual(f["swing_low_label"].iloc[-1], "HL")
        self.assertEqual(f["structure"].iloc[-1], "up")
        self.assertTrue(f["structure_up"].iloc[-1])

    def test_bearish_divergence_higher_high_weaker_rsi(self):
        up_fast = [100 + 2 * i for i in range(15)]               # strong rise to 128
        down = [128 - 1.5 * i for i in range(1, 9)]              # pull back
        up_slow = [116 + 0.9 * i for i in range(1, 16)]          # slow grind to a HIGHER high
        down2 = [129.5 - 1.5 * i for i in range(1, 9)]
        closes = up_fast + down + up_slow + down2
        rows = [(c - 0.1, c + 0.3, c - 0.3, c, 1) for c in closes]
        f = F.compute(frame(rows), H1)
        self.assertTrue(f["bear_div"].any())
        t = int(np.flatnonzero(f["bear_div"].to_numpy())[0])
        self.assertGreaterEqual(t, len(up_fast) + len(down) + len(up_slow) - 1 + F.DEFAULTS["swing_n"])

    def test_breakout_retest_and_failed_breakout(self):
        base = calm(30)
        rows = base + [(100.2, 101.4, 100.1, 101.2, 1),           # breakout above 100.5
                       (101.1, 101.2, 100.6, 100.9, 1)]            # dips to the level, holds
        f = F.compute(frame(rows), H1)
        self.assertTrue(f["breakout_up"].iloc[-2])
        self.assertTrue(f["retest_up"].iloc[-1])
        self.assertFalse(f["failed_breakout_up"].iloc[-1])
        rows = base + [(100.2, 101.4, 100.1, 101.2, 1), (101.0, 101.1, 99.8, 100.0, 1)]  # closes back in
        f = F.compute(frame(rows), H1)
        self.assertTrue(f["failed_breakout_up"].iloc[-1])
        self.assertFalse(f["retest_up"].iloc[-1])

    def test_consolidation_impulse_pullback(self):
        rows = calm(40)
        f = F.compute(frame(rows), H1)
        self.assertTrue(f["consolidation"].iloc[-1])
        rally = [(100 + i, 101 + i, 99.9 + i, 101 + i, 1) for i in range(5)]    # +5 in 5 candles
        back = [(104.5, 104.6, 102.4, 102.5, 1)]                                 # gives back ~50%
        f = F.compute(frame(rows + rally + back), H1)
        self.assertTrue(f["impulse_up"].iloc[len(rows) + 4])
        self.assertTrue(f["pullback_up"].iloc[-1])
        broke = [(104.5, 104.6, 98.0, 98.5, 1)]                                  # below the start
        self.assertFalse(F.compute(frame(rows + rally + broke), H1)["pullback_up"].iloc[-1])

    def test_indicators_exist_and_vwap_resets_daily(self):
        df = synthetic(n=300)
        f = F.compute(df, H1)
        for col in ("stoch_rsi_k", "stoch_rsi_d", "roc", "keltner_upper", "keltner_lower", "obv", "vwap"):
            self.assertTrue(f[col].iloc[-1] == f[col].iloc[-1], col)          # not NaN
        first_of_day = np.flatnonzero((df["open_time"] % 86_400_000 == 0).to_numpy())[1]
        tp = (df["high"] + df["low"] + df["close"]) / 3
        self.assertAlmostEqual(f["vwap"].iloc[first_of_day], tp.iloc[first_of_day])
        daily = F.compute(scanner.Synthetic().klines("BTCUSDT", "1d", 300), 86_400_000)
        self.assertTrue(daily["vwap"].isna().all())               # not meaningful on 1D


class RuleLanguage(unittest.TestCase):
    def test_existing_strategies_unchanged_and_features_usable(self):
        strategies = yaml.safe_load(open(os.path.join(ROOT, "strategies.yaml")))
        df = scanner.add_htf(synthetic(n=1500), synthetic(tf="4h", n=600))
        feats = F.compute(df, H1)
        plain, rich = scanner.make_namespace(df), scanner.make_namespace(df, feats)
        for s in strategies:
            for side in ("long", "short", "exit_long", "exit_short"):
                if s.get(side):
                    np.testing.assert_array_equal(scanner.eval_rules(s[side], plain, df.index),
                                                  scanner.eval_rules(s[side], rich, df.index),
                                                  err_msg=f"{s['name']} {side}")
        self.assertTrue(callable(rich["atr"]))                    # building block not overwritten
        out = scanner.eval_rules(["bull_engulf", "close_loc > 0.5", "rel_vol > 0"], rich, df.index)
        self.assertEqual(out.sum(), (feats["bull_engulf"] & (feats["close_loc"] > 0.5)
                                     & (feats["rel_vol"] > 0)).sum())


COSTS = {1: dict(taker=0.001, slip=0.0005, funding_8h=0.0),
         -1: dict(taker=0.0005, slip=0.0005, funding_8h=0.0001)}


class EvidenceOutcome(unittest.TestCase):
    def arrays(self, path):
        o = np.array([p[0] for p in path], float)
        h = np.array([p[1] for p in path], float)
        l = np.array([p[2] for p in path], float)
        c = np.array([p[3] for p in path], float)
        return o, h, l, c

    def test_reaches_targets_after_costs(self):
        s = E.settings({"max_bars": 5})
        path = [(100, 100, 100, 100)] + [(100, 100.5, 99.5, 100)] + \
               [(100, 101.6, 99.6, 101.5), (101.5, 103.0, 101.0, 102.9), (103, 103.1, 102, 102.5),
                (102.5, 102.6, 98, 98.5)]
        o, h, l, c = self.arrays(path)
        best, stopped, cost_r = E.outcome(o, h, l, c, 0, 1, 1.0, COSTS[1], 1.0, s)
        # entry 100.05, R = 1, cost ~0.25 -> +1R at 101.30, +2R at 102.30, +3R at 103.30
        self.assertEqual(best, 2)
        self.assertTrue(stopped)                  # later the stop (99.05) was hit
        self.assertAlmostEqual(cost_r, 100.05 * (0.002 + 0.0005), places=6)

    def test_costs_can_turn_a_touch_into_a_miss(self):
        s = E.settings({"max_bars": 3})
        path = [(100, 100, 100, 100), (100, 100.5, 99.5, 100), (100, 101.1, 99.5, 101), (101, 101.1, 100.5, 101)]
        o, h, l, c = self.arrays(path)
        self.assertEqual(E.outcome(o, h, l, c, 0, 1, 1.0, COSTS[1], 1.0, s)[0], 0)   # 101.1 < 101.30

    def test_stop_first_in_the_same_candle(self):
        s = E.settings({"max_bars": 3})
        path = [(100, 100, 100, 100), (100, 100.5, 99.5, 100), (100, 104, 98, 100), (100, 100, 100, 100)]
        o, h, l, c = self.arrays(path)
        best, stopped, _ = E.outcome(o, h, l, c, 0, 1, 1.0, COSTS[1], 1.0, s)
        self.assertEqual(best, 0)
        self.assertTrue(stopped)

    def test_short_and_not_enough_future(self):
        s = E.settings({"max_bars": 3})
        path = [(100, 100, 100, 100), (100, 100.2, 99.8, 100), (100, 100.1, 97.5, 97.6), (97.6, 97.7, 96, 96.1)]
        o, h, l, c = self.arrays(path)
        best, stopped, _ = E.outcome(o, h, l, c, 0, -1, 1.0, COSTS[-1], 8.0, s)
        self.assertEqual(best, 3)
        self.assertFalse(stopped)
        self.assertIsNone(E.outcome(o, h, l, c, 1, -1, 1.0, COSTS[-1], 8.0, s))       # runs off the end


class EvidenceStudy(unittest.TestCase):
    def planted(self, edge, seed=3, n=4000):
        """Random walk; at 120 marked candles a bullish engulfing is 'seen'. With edge=True the price
        then really rallies 4 ATR over the next 8 candles."""
        rng = np.random.default_rng(seed)
        close = 100 + np.cumsum(rng.normal(0, 0.5, n))
        marks = np.arange(100, n - 60, 30)[:120]
        if edge:
            bump = np.zeros(n)
            for t in marks:
                bump[t + 1:t + 9] += np.linspace(0.5, 4.0, 8)
                bump[t + 9:] += 4.0
            close = close + bump
        o = np.r_[close[0], close[:-1]]
        df = pd.DataFrame({"open": o, "high": np.maximum(o, close) + 0.2, "low": np.minimum(o, close) - 0.2,
                           "close": close})
        f = pd.DataFrame({"atr": np.full(n, 1.0)})
        for pat in E.PATTERNS:
            f[pat] = False
        f.loc[marks, "bull_engulf"] = True
        return [("X", df, f)]

    def test_planted_edge_beats_chance_and_random_is_not(self):
        s = E.settings(None)
        good = E.study(self.planted(True), COSTS, 1.0, s, "t")["bull_engulf"]
        self.assertEqual(good["verdict"], "beats chance")
        self.assertEqual(good["events"], 120)
        self.assertEqual(good["random_events"], 1200)            # 10 random entries per event
        plain = E.study(self.planted(False), COSTS, 1.0, s, "t")["bull_engulf"]
        self.assertNotEqual(plain["verdict"], "beats chance")
        self.assertEqual(E.study(self.planted(True), COSTS, 1.0, s, "t")["bear_engulf"]["verdict"],
                         "too few to judge")

    def test_deterministic(self):
        a = E.study(self.planted(False), COSTS, 1.0, None, "t")
        b = E.study(self.planted(False), COSTS, 1.0, None, "t")
        self.assertEqual(a, b)

    def test_random_data_rarely_beats_chance(self):
        feed = scanner.Synthetic()
        frames = []
        for coin in ("BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"):
            df = feed.klines(coin, "1h", 2000)
            frames.append((coin, df, F.compute(df, H1)))
        res = E.study(frames, COSTS, 1.0, None, "1h")
        beats = [p for p, r in res.items() if r["verdict"] == "beats chance"]
        self.assertLessEqual(len(beats), 1, beats)


class EndToEnd(unittest.TestCase):
    def test_offline_report_has_features_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = run_copy(tmp, "scanner.py", "--offline")
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            with open(os.path.join(tmp, "reports", "latest.md")) as f:
                md = f.read()
            self.assertIn("## 0d. Market features now", md)
            self.assertIn("## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL", md)
            with open(os.path.join(tmp, "reports", "feature_evidence.json")) as f:
                e = json.load(f)
            self.assertEqual(e["label"], "RESEARCH EVIDENCE, NOT A SIGNAL")
            self.assertEqual(set(e["timeframes"]), {"4h", "1h", "30m", "15m", "5m"})
            one = e["timeframes"]["1h"]["bull_engulf"]
            self.assertEqual(one["random_events"], 10 * one["events"])
            with open(os.path.join(tmp, "reports", "features.json")) as f:
                feats = json.load(f)
            self.assertIn("structure", feats["coins"]["BTC"]["1h"])


if __name__ == "__main__":
    unittest.main()
