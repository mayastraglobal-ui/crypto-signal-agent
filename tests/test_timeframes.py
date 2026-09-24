"""Phase 3 tests: timeframes 1W -> 5m, safe higher-timeframe alignment, rolling 7D,
cross-timeframe consistency and the timeframe model.

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
from engine import data_quality as dq  # noqa: E402
from engine import timeframes as T  # noqa: E402
from test_data_quality import run_copy, shared_offline_run  # noqa: E402

M5, H1, H4, D1, W1 = (T.TF_MS[k] for k in ("5m", "1h", "4h", "1d", "1w"))
MONDAY = pd.Timestamp("2025-01-06", tz="UTC").value // 1_000_000     # a Monday 00:00 UTC


def candles_from(base, tf_ms, n_lower_per, lower):
    """Aggregate a lower frame into higher candles exactly (like an exchange does)."""
    g = lower.groupby((lower["open_time"] - base) // tf_ms)
    out = g.agg(open=("open", "first"), high=("high", "max"), low=("low", "min"),
                close=("close", "last"), volume=("volume", "sum"), n=("open", "size")).reset_index()
    out = out[out["n"] == n_lower_per]
    out["open_time"] = base + out.iloc[:, 0] * tf_ms
    out["close_time"] = out["open_time"] + tf_ms - 1
    return out[["open_time", "close_time", "open", "high", "low", "close", "volume"]].reset_index(drop=True)


def walk(n, tf_ms, start=MONDAY, seed=1):
    rng = np.random.default_rng(seed)
    c = 100 * np.exp(np.cumsum(rng.normal(0, 0.003, n)))
    o = np.r_[c[0], c[:-1]]
    w = np.abs(rng.normal(0, 0.001, n)) * c
    df = pd.DataFrame({"open_time": start + tf_ms * np.arange(n), "open": o,
                       "high": np.maximum(o, c) + w, "low": np.minimum(o, c) - w, "close": c,
                       "volume": rng.uniform(1, 3, n)})
    df["close_time"] = df["open_time"] + tf_ms - 1
    return df


class AlignHigher(unittest.TestCase):
    def test_only_closed_higher_candles_are_used(self):
        h1 = walk(24 * 60, H1)
        h4 = candles_from(MONDAY, H4, 4, h1)
        h4["tag"] = np.arange(len(h4))
        m = T.align_higher(h1, h4, ["tag"])
        for i in range(0, len(h1), 7):
            tag = m["tag"].iloc[i]
            if np.isnan(tag):
                self.assertLess(h1["close_time"].iloc[i], h4["close_time"].iloc[0])
                continue
            used = h4.iloc[int(tag)]
            self.assertLessEqual(used["close_time"], h1["close_time"].iloc[i])      # closed already
            nxt = h4[h4["close_time"] > used["close_time"]]
            if len(nxt):                                                        # and it is the newest
                self.assertGreater(nxt["close_time"].iloc[0], h1["close_time"].iloc[i])

    def test_future_candles_never_change_the_past(self):
        h1 = walk(24 * 40, H1)
        h4 = candles_from(MONDAY, H4, 4, h1)
        full = T.align_higher(h1, h4, ["close"])
        for k in (101, 402, 803):              # cut in the MIDDLE of a 4H candle
            cut = h1["close_time"].iloc[k - 1]
            past = T.align_higher(h1.iloc[:k], h4[h4["close_time"] <= cut], ["close"])
            pd.testing.assert_series_equal(full["close"].iloc[:k], past["close"])

    def test_mid_week_candle_sees_last_week_not_the_current_week(self):
        h4 = walk(6 * 7 * 3, H4)                     # three weeks of 4H candles from a Monday
        w1 = candles_from(MONDAY, W1, 42, h4)
        m = T.align_higher(h4, w1, ["close"])
        wednesday_week2 = h4.index[(h4["open_time"] == MONDAY + W1 + 2 * D1 + 8 * H1)][0]
        self.assertEqual(m["close"].loc[wednesday_week2], w1["close"].iloc[0])   # week 1, closed
        last_of_week2 = h4.index[h4["close_time"] == w1["close_time"].iloc[1]][0]
        self.assertEqual(m["close"].loc[last_of_week2], w1["close"].iloc[1])    # week 2 just closed
        self.assertTrue(np.isnan(m["close"].iloc[0]))                            # nothing closed yet

    def test_unsorted_input_keeps_row_order(self):
        h1 = walk(200, H1)
        h4 = candles_from(MONDAY, H4, 4, h1)
        shuffled = h1.sample(frac=1, random_state=2)
        a = T.align_higher(shuffled, h4, ["close"])
        b = T.align_higher(h1, h4, ["close"]).loc[shuffled.index]
        pd.testing.assert_frame_equal(a, b)


class LegacyHtfUnchanged(unittest.TestCase):
    """The existing strategies must see exactly the same htf_up / htf_down as before Phase 3."""

    @staticmethod
    def old_add_htf(df, htf_df):          # the pre-Phase-3 implementation, copied verbatim
        hc = htf_df["close"]
        e20 = hc.ewm(span=20, adjust=False, min_periods=20).mean()
        e50 = hc.ewm(span=50, adjust=False, min_periods=50).mean()
        t = pd.DataFrame({"close_time": htf_df["close_time"],
                          "htf_up": (hc > e50) & (e20 > e50),
                          "htf_down": (hc < e50) & (e20 < e50)})
        m = pd.merge_asof(df[["close_time"]].astype("int64"), t.astype({"close_time": "int64"}),
                          on="close_time", direction="backward")
        df["htf_up"] = m["htf_up"].fillna(False).astype(bool).to_numpy()
        df["htf_down"] = m["htf_down"].fillna(False).astype(bool).to_numpy()
        return df

    def test_identical_on_every_legacy_pair(self):
        feed = scanner.Synthetic()
        for coin in ("BTCUSDT", "SOLUSDT"):
            for tf, htf in T.LEGACY_HTF.items():
                lo = feed.klines(coin, tf, 1500)
                hi = feed.klines(coin, htf, 600)
                new = scanner.add_htf(lo.copy(), hi)
                old = self.old_add_htf(lo.copy(), hi)
                np.testing.assert_array_equal(new["htf_up"].to_numpy(), old["htf_up"].to_numpy())
                np.testing.assert_array_equal(new["htf_down"].to_numpy(), old["htf_down"].to_numpy())
                self.assertEqual(new["htf_up"].dtype, bool)


class Rolling7D(unittest.TestCase):
    def test_values_and_no_look_ahead(self):
        d = walk(60, D1)
        r = T.rolling_7d(d)
        self.assertEqual(len(r), 54)
        row = r.iloc[10]                         # covers daily candles 10..16
        win = d.iloc[10:17]
        self.assertEqual(row["open"], win["open"].iloc[0])
        self.assertEqual(row["close"], win["close"].iloc[-1])
        self.assertEqual(row["high"], win["high"].max())
        self.assertEqual(row["low"], win["low"].min())
        self.assertAlmostEqual(row["volume"], win["volume"].sum())
        self.assertEqual(row["close_time"], win["close_time"].iloc[-1])
        past = T.rolling_7d(d.iloc[:30])           # future days never change a past 7D candle
        pd.testing.assert_frame_equal(r.iloc[:len(past)].reset_index(drop=True), past)

    def test_window_with_missing_day_is_dropped(self):
        d = walk(30, D1).drop(index=[15]).reset_index(drop=True)
        r = T.rolling_7d(d)
        covered = set(r["close_time"])
        for day in range(15, 22):                  # every window that contains day 15
            self.assertNotIn(MONDAY + D1 * (day + 1) - 1, covered)
        self.assertIn(MONDAY + D1 * 23 - 1, covered)

    def test_too_short(self):
        self.assertEqual(len(T.rolling_7d(walk(5, D1))), 0)


class Consistency(unittest.TestCase):
    def setUp(self):
        self.h1 = walk(24 * 20, H1)
        self.h4 = candles_from(MONDAY, H4, 4, self.h1)

    def test_clean_data_agrees(self):
        r = T.consistency(self.h1, self.h4, H1, H4)
        self.assertEqual(r["checked"], 50)
        self.assertEqual(r["mismatches"], 0)

    def test_planted_errors_are_caught(self):
        for field, factor in [("high", 1.01), ("low", 0.99), ("open", 1.002), ("close", 0.998),
                              ("volume", 1.5)]:
            h4 = self.h4.copy()
            h4.loc[h4.index[-2], field] *= factor
            r = T.consistency(self.h1, h4, H1, H4)
            self.assertEqual(r["mismatches"], 1, field)
            self.assertIn(field, r["examples"][0])

    def test_incomplete_group_is_skipped_not_an_error(self):
        h1 = self.h1.drop(index=[self.h1.index[-6]])       # a gap inside the second-last 4H candle
        r = T.consistency(h1, self.h4, H1, H4)
        self.assertEqual(r["mismatches"], 0)
        self.assertEqual(r["checked"], 49)

    def test_weekly_from_daily_monday_weeks(self):
        d = walk(7 * 30, D1)
        w = candles_from(MONDAY, W1, 7, d)
        self.assertEqual(T.consistency(d, w, D1, W1)["mismatches"], 0)
        w.loc[w.index[-1], "high"] *= 1.05
        self.assertEqual(T.consistency(d, w, D1, W1)["mismatches"], 1)

    def test_scanner_marks_higher_timeframe_degraded(self):
        h4 = self.h4.copy()
        h4.loc[h4.index[-3], "high"] *= 1.02
        data = {("XUSDT", "1h"): self.h1, ("XUSDT", "4h"): h4}
        quality = {("X", "1h"): dq.check_candles(self.h1, H1, int(self.h1["close_time"].iloc[-1]) + 1)[1],
                   ("X", "4h"): dq.check_candles(h4, H4, int(h4["close_time"].iloc[-1]) + 1)[1]}
        self.assertEqual(quality[("X", "4h")]["state"], dq.GOOD)
        out = scanner.cross_timeframe_check(data, "XUSDT", "X", quality)
        self.assertEqual(out["1h>4h"]["mismatches"], 1)
        self.assertEqual(quality[("X", "4h")]["state"], dq.DEGRADED)       # the higher one
        self.assertEqual(quality[("X", "1h")]["state"], dq.GOOD)
        self.assertIn("disagree with the 1h", quality[("X", "4h")]["problems"][0])


class WeeklyDataQuality(unittest.TestCase):
    def test_weekly_candles_pass_and_stale_weekly_is_unsafe(self):
        w = walk(300, W1)
        now = int(w["close_time"].iloc[-1]) + 3 * D1
        self.assertEqual(dq.check_candles(w, W1, now)[1]["state"], dq.GOOD)
        self.assertEqual(dq.check_candles(w, W1, now + 2 * W1)[1]["state"], dq.UNSAFE)

    def test_unfinished_week_is_ignored(self):
        w = walk(300, W1)
        now = int(w["open_time"].iloc[-1]) + 3 * D1        # the last week is only 3 days old
        clean, r = dq.check_candles(w, W1, now)
        self.assertEqual(len(clean), 299)
        self.assertEqual(r["state"], dq.GOOD)


class Model(unittest.TestCase):
    def test_roles_and_description(self):
        r = T.model_roles(T.DEFAULT_MODELS["B"])
        self.assertEqual(r, dict(bias=["1d", "4h", "1h"], setup="30m", trigger="15m", execution="5m",
                                 veto="1w"))
        self.assertEqual(T.describe(T.DEFAULT_MODELS["B"]),
                         "1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry")

    def test_config_model_is_valid_and_fully_downloaded(self):
        cfg = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
        tm = cfg["timeframe_model"]
        available = set(cfg["timeframes"]) | {"7d"}
        self.assertEqual(tm["active"], "B")
        self.assertEqual(T.missing_timeframes(tm["models"]["B"], available), [])
        self.assertEqual(T.missing_timeframes(tm["models"]["D"], available), ["2h"])
        for m in tm["models"].values():
            self.assertTrue(all(tf in T.TF_MS for tf in m["chain"]))


class EndToEnd(unittest.TestCase):
    def test_offline_report_shows_all_timeframes(self):
        tmp, p = shared_offline_run()          # one plain offline scan, shared (read-only)
        if True:
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            with open(os.path.join(tmp, "reports", "latest.json")) as f:
                t = json.load(f)["timeframes"]
            with open(os.path.join(tmp, "reports", "latest.md")) as f:
                md = f.read()
            self.assertEqual(t["active_model"], "B")
            self.assertEqual(t["missing_for_active"], [])
            btc = t["coins"]["BTC"]["bars"]
            self.assertEqual(btc["1w"], 500)
            self.assertEqual(btc["1d"], 1000)
            self.assertEqual(btc["7d"], 994)
            self.assertIn("## 0c. Timeframes loaded", md)
            self.assertIn("not run (offline test data)", md)
            with open(os.path.join(tmp, "reports", "data_quality.json")) as f:
                self.assertIn("1w", json.load(f)["coins"]["BTC"]["timeframes"])


if __name__ == "__main__":
    unittest.main()
