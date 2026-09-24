"""Phase 5 tests: market regime engine (labels, evidence, confidence, timeframe permission, daily log).

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
from engine import regime as R  # noqa: E402
from test_data_quality import run_copy  # noqa: E402

D1, W1, H4 = 86_400_000, 7 * 86_400_000, 14_400_000
T0 = 1_700_000_000_000 // W1 * W1


def path(closes, tf_ms=H4, wick=0.3, vol=None, seed=5):
    """Candles following the given closes, with small wicks."""
    rng = np.random.default_rng(seed)
    c = np.asarray(closes, float)
    o = np.r_[c[0], c[:-1]]
    w = np.abs(rng.normal(0, wick, len(c))) + 0.05
    df = pd.DataFrame({"open_time": T0 + tf_ms * np.arange(len(c)), "open": o,
                       "high": np.maximum(o, c) + w, "low": np.minimum(o, c) - w, "close": c,
                       "volume": vol if vol is not None else rng.uniform(90, 110, len(c))})
    df["close_time"] = df["open_time"] + tf_ms - 1
    return df


def trend(n, step, seed=1):
    """A realistic zig-zag trend: 5 candles with the trend, 2 candles of pullback, repeat."""
    rng = np.random.default_rng(seed)
    c = [100.0]
    for i in range(n - 1):
        c.append(c[-1] + (step if i % 7 < 5 else -1.2 * step) + rng.normal(0, 0.1))
    return np.array(c)


class ClassifyRules(unittest.TestCase):
    """The rule table, row by row, with hand-made numbers."""

    def label(self, **kw):
        row = dict(enough=True, score=0, adx=15.0, bb_pct=0.5, atr_ratio=1.0, recent_range_exp=False,
                   recent_up_event=False, recent_down_event=False, move=0.0)
        row.update(kw)
        lab, d = R.classify(pd.DataFrame([row]))
        return lab.iloc[0], d.iloc[0]

    def test_every_label(self):
        cases = [
            (dict(enough=False, score=3, adx=40), "UNCLEAR"),
            (dict(bb_pct=0.95, recent_range_exp=True, recent_up_event=True), "EXPANSION"),
            (dict(bb_pct=0.05, atr_ratio=0.6, adx=12), "COMPRESSION"),
            (dict(score=3, adx=30), "STRONG_BULL"),
            (dict(score=-3, adx=30), "STRONG_BEAR"),
            (dict(score=3, adx=22), "WEAK_BULL"),          # all votes agree but trend not strong
            (dict(score=2, adx=35), "WEAK_BULL"),
            (dict(score=-2, adx=10), "WEAK_BEAR"),
            (dict(score=1, adx=15, atr_ratio=1.5), "HIGH_VOL_RANGE"),
            (dict(score=0, adx=15), "RANGE"),
            (dict(score=-1, adx=30), "TRANSITION"),
            (dict(score=0, adx=22), "UNCLEAR"),             # mixed votes, strength in between
        ]
        for kw, want in cases:
            self.assertEqual(self.label(**kw)[0], want, kw)

    def test_expansion_direction(self):
        self.assertEqual(self.label(bb_pct=0.95, recent_range_exp=True, recent_down_event=True)[1], "down")
        self.assertEqual(self.label(bb_pct=0.95, recent_range_exp=True, recent_up_event=True)[1], "up")
        self.assertIsNone(self.label(score=3, adx=30)[1])

    def test_compression_needs_weak_adx_and_expansion_needs_an_event(self):
        self.assertNotEqual(self.label(bb_pct=0.05, atr_ratio=0.6, adx=30, score=3)[0], "COMPRESSION")
        self.assertNotEqual(self.label(bb_pct=0.95, recent_range_exp=True)[0], "EXPANSION")     # no event
        self.assertNotEqual(self.label(bb_pct=0.95, recent_up_event=True)[0], "EXPANSION")      # no range exp.

    def test_missing_volatility_history_never_gives_volatility_labels(self):
        self.assertEqual(self.label(bb_pct=np.nan, atr_ratio=np.nan, score=0, adx=15)[0], "RANGE")
        self.assertEqual(self.label(bb_pct=np.nan, atr_ratio=np.nan, recent_range_exp=True, recent_up_event=True,
                                    score=3, adx=30)[0], "STRONG_BULL")


class PricePaths(unittest.TestCase):
    def test_steady_climb_is_strong_bull(self):
        r = R.compute(path(trend(600, 1.0)), "4h")
        self.assertEqual(r["label"].iloc[-1], "STRONG_BULL")
        d = R.describe(r)
        self.assertIn("close above EMA-fast above EMA-slow", d["supporting"])
        self.assertIn("swing structure up (HH/HL)", d["supporting"])
        self.assertNotEqual(d["confidence"], "weak")

    def test_steady_fall_is_strong_bear(self):
        r = R.compute(path(trend(600, -1.0) + 500), "4h")
        self.assertEqual(r["label"].iloc[-1], "STRONG_BEAR")
        self.assertEqual(R.direction("STRONG_BEAR"), -1)

    def test_short_history_is_unclear(self):
        r = R.compute(path(trend(150, 1.0)), "4h")               # EMA200 needs 200 candles
        self.assertEqual(r["label"].iloc[-1], "UNCLEAR")
        d = R.describe(r)
        self.assertEqual(d["confidence"], "weak")
        self.assertIn("not enough history on this timeframe", d["contradicting"])

    def test_weekly_uses_10_40_so_young_coins_get_a_label(self):
        closes = trend(80, 1.0)
        weekly = R.compute(path(closes, tf_ms=W1), "1w")
        daily = R.compute(path(closes, tf_ms=D1), "1d")
        self.assertEqual(weekly["label"].iloc[-1], "STRONG_BULL")
        self.assertEqual(daily["label"].iloc[-1], "UNCLEAR")      # 80 daily candles: no EMA200 yet

    def test_squeeze_is_compression_and_breakout_is_expansion(self):
        # a FRESH squeeze: 25 very quiet candles after a normal market. (After many quiet candles,
        # quiet becomes the new normal and the engine rightly calls it RANGE, not COMPRESSION.)
        rng = np.random.default_rng(2)
        wild = 100 + np.cumsum(rng.normal(0, 1.2, 300)) * 0.3
        wild = wild - (wild - 100) * np.linspace(0, 1, 300)       # drifts back to 100
        calm = 100 + rng.normal(0, 0.05, 25)
        closes = np.r_[wild, calm]
        wicks = np.r_[np.full(300, 1.0), np.full(25, 0.02)]
        df = path(closes, wick=0.0)
        df["high"] = np.maximum(df["open"], df["close"]) + wicks
        df["low"] = np.minimum(df["open"], df["close"]) - wicks
        r = R.compute(df, "4h")
        self.assertEqual(r["label"].iloc[-1], "COMPRESSION")
        blast = [100.2 + 1.5 * i for i in range(1, 5)]            # big candles up, high volume
        df2 = path(np.r_[closes, blast], wick=0.0)
        df2["high"] = np.maximum(df2["open"], df2["close"]) + np.r_[wicks, np.full(4, 0.05)]
        df2["low"] = np.minimum(df2["open"], df2["close"]) - np.r_[wicks, np.full(4, 0.05)]
        df2.loc[df2.index[-4:], "volume"] = 400
        r2 = R.compute(df2, "4h")
        self.assertEqual(r2["label"].iloc[-1], "EXPANSION")
        self.assertEqual(r2["expansion_dir"].iloc[-1], "up")
        self.assertEqual(R.direction("EXPANSION", "up"), 1)

    def test_no_look_ahead(self):
        df = scanner.Synthetic().klines("BTCUSDT", "4h", 1200)
        full = R.compute(df, "4h")
        for cut in (400, 777, 1001):
            past = R.compute(df.iloc[:cut], "4h")
            pd.testing.assert_frame_equal(full.iloc[:cut], past, check_dtype=False, obj=f"cut {cut}")


class Confidence(unittest.TestCase):
    def row(self, **kw):
        base = dict(label="STRONG_BULL", expansion_dir=None, ema_slow=90.0, adx=32.0, ema_vote=1, slope_vote=1,
                    slope_atr=2.0, structure="up", structure_vote=1, atr_ratio=1.0, bb_pct=0.5, rel_vol5=1.1,
                    rsi=62.0, score=3)
        base.update(kw)
        return pd.DataFrame([base])

    def test_all_agree_is_strong(self):
        d = R.describe(self.row())
        self.assertEqual(d["confidence"], "strong")
        self.assertEqual(d["contradicting"], [])

    def test_one_contradiction_is_moderate_two_is_weak(self):
        self.assertEqual(R.describe(self.row(rel_vol5=0.5))["confidence"], "moderate")
        d = R.describe(self.row(rel_vol5=0.5, adx=26.0))                # low volume + ADX near 25
        self.assertEqual(d["confidence"], "weak")
        self.assertTrue(any("close to a threshold" in x for x in d["contradicting"]))

    def test_never_a_percentage(self):
        d = R.describe(self.row())
        self.assertIn(d["confidence"], ("strong", "moderate", "weak"))
        self.assertEqual(d["states"], dict(volatility="normal", momentum="up", structure="up"))


class Permission(unittest.TestCase):
    def regs(self, w, d, h4, h1):
        return {"1w": dict(label=w), "1d": dict(label=d), "4h": dict(label=h4), "1h": dict(label=h1)}

    def test_two_of_three_and_weekly_veto(self):
        self.assertEqual(R.permission(self.regs("WEAK_BULL", "STRONG_BULL", "WEAK_BULL", "RANGE"))[0],
                         "LONG allowed")
        verdict, why = R.permission(self.regs("STRONG_BEAR", "STRONG_BULL", "WEAK_BULL", "RANGE"))
        self.assertEqual(verdict, "NO TRADE")
        self.assertIn("weekly veto", why)
        self.assertEqual(R.permission(self.regs("RANGE", "WEAK_BEAR", "STRONG_BEAR", "WEAK_BULL"))[0],
                         "SHORT allowed")
        self.assertEqual(R.permission(self.regs("STRONG_BULL", "WEAK_BEAR", "STRONG_BEAR", "RANGE"))[0],
                         "NO TRADE")
        verdict, why = R.permission(self.regs("RANGE", "WEAK_BULL", "WEAK_BEAR", "RANGE"))
        self.assertEqual(verdict, "NO TRADE")
        self.assertIn("disagree", why)

    def test_expansion_counts_by_direction_and_unclear_counts_for_nothing(self):
        r = self.regs("RANGE", "WEAK_BULL", "EXPANSION", "UNCLEAR")
        r["4h"]["expansion_dir"] = "up"
        self.assertEqual(R.permission(r)[0], "LONG allowed")
        self.assertEqual(R.permission(self.regs("RANGE", "WEAK_BULL", "UNCLEAR", "UNCLEAR"))[0], "NO TRADE")


class DailyLog(unittest.TestCase):
    def test_log_is_append_only_with_btc_context(self):
        g = dict(data_source="Binance", coins={
            "BTC": dict(timeframes={tf: dict(label="WEAK_BULL", expansion_dir=None, confidence="moderate")
                                    for tf in ("1w", "1d", "4h", "1h")}, permission="LONG allowed")})
        with tempfile.TemporaryDirectory() as tmp:
            old = scanner.MEMORY
            scanner.MEMORY = tmp
            try:
                scanner.write_regime_log(g, dt.datetime(2026, 9, 24, 0, 20, tzinfo=dt.timezone.utc))
                scanner.write_regime_log(g, dt.datetime(2026, 9, 25, 0, 19, tzinfo=dt.timezone.utc))
            finally:
                scanner.MEMORY = old
            with open(os.path.join(tmp, "market_regime_log.md")) as f:
                text = f.read()
        self.assertEqual(text.count("# Market regime log"), 1)
        self.assertLess(text.index("## 2026-09-24"), text.index("## 2026-09-25"))
        self.assertIn("BTC context: 1W WEAK_BULL (moderate)", text)

    def test_offline_runs_log_once_per_day_and_never_touch_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            for _ in range(2):
                p = run_copy(tmp, "scanner.py", "--offline")
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            with open(os.path.join(tmp, "reports", "regime_state_offline.json")) as f:
                self.assertEqual(json.load(f)["last_logged_date"], dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"))
            self.assertFalse(os.path.exists(os.path.join(tmp, "memory", "market_regime_log.md")))
            with open(os.path.join(tmp, "reports", "regime.json")) as f:
                g = json.load(f)
            self.assertEqual(list(g["coins"])[0], "BTC")
            for c in g["coins"].values():
                self.assertEqual(set(c["timeframes"]), {"1w", "1d", "4h", "1h"})
                self.assertIn(c["permission"], ("LONG allowed", "SHORT allowed", "NO TRADE"))
            with open(os.path.join(tmp, "reports", "latest.md")) as f:
                md = f.read()
            self.assertIn("## 0f. Market regime", md)
            self.assertNotIn(" nan ", md)


if __name__ == "__main__":
    unittest.main()
