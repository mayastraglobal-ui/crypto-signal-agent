"""Phase 1 tests: data-quality checks (AGENT_PROMPT.md section 3).

Each test plants ONE problem in clean synthetic candles and checks it is caught.
Run:  python -m unittest discover -s tests -v
"""
import atexit
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine import data_quality as dq  # noqa: E402

H = 3_600_000                     # one 1h candle in ms
T0 = 1_750_000_000_000 // H * H   # a fixed, aligned start time


def candles(n=500, tf_ms=H, seed=1):
    """Clean, realistic 1h candles: open_time T0, T0+1h, ..."""
    rng = np.random.default_rng(seed)
    close = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    opn = np.r_[close[0], close[:-1]]
    wick = np.abs(rng.normal(0, 0.003, n)) * close
    return pd.DataFrame({"open_time": T0 + tf_ms * np.arange(n),
                         "open": opn, "high": np.maximum(opn, close) + wick,
                         "low": np.minimum(opn, close) - wick, "close": close,
                         "volume": rng.lognormal(10, 0.3, n)})


def now_after(df, tf_ms=H, extra_ms=60_000):
    """A 'now' just after the last candle closed."""
    return int(df["open_time"].iloc[-1]) + tf_ms + extra_ms


def check(df, now=None):
    return dq.check_candles(df, H, now if now is not None else now_after(df))


class CandleChecks(unittest.TestCase):
    def test_clean_data_is_good(self):
        clean, r = check(candles())
        self.assertEqual(r["state"], dq.GOOD, r)
        self.assertEqual(r["problems"], [])
        self.assertEqual(len(clean), 500)

    def test_empty_is_unsafe(self):
        self.assertEqual(check(candles().iloc[:0], now=T0)[1]["state"], dq.UNSAFE)

    def test_out_of_order_is_sorted_and_noted(self):
        df = candles().sample(frac=1, random_state=3)
        clean, r = check(df, now=now_after(candles()))
        self.assertEqual(r["state"], dq.GOOD)
        self.assertTrue(clean["open_time"].is_monotonic_increasing)
        self.assertTrue(any("out of order" in n for n in r["notes"]))

    def test_exact_duplicate_removed_and_noted(self):
        df = candles()
        df = pd.concat([df, df.iloc[[100]]])
        clean, r = check(df, now=now_after(candles()))
        self.assertEqual(r["state"], dq.GOOD)
        self.assertEqual(len(clean), 500)
        self.assertTrue(any("duplicate" in n for n in r["notes"]))

    def test_conflicting_duplicate_is_degraded(self):
        df = candles()
        twin = df.iloc[[100]].copy()
        twin["volume"] *= 2
        _, r = check(pd.concat([df, twin]), now=now_after(candles()))
        self.assertEqual(r["state"], dq.DEGRADED)

    def test_unfinished_candle_is_ignored(self):
        df = candles()
        now = int(df["open_time"].iloc[-1]) + H // 2      # last candle only half done
        clean, r = check(df, now=now)
        self.assertEqual(len(clean), 499)
        self.assertLess(clean["close_time"].iloc[-1], now)
        self.assertTrue(any("UNCONFIRMED" in n for n in r["notes"]))
        self.assertEqual(r["state"], dq.GOOD)

    def test_recent_gap_is_degraded(self):
        df = candles().drop(index=[480, 481])
        _, r = check(df, now=now_after(candles()))
        self.assertEqual(r["state"], dq.DEGRADED)
        self.assertIn("2 missing", r["problems"][0])

    def test_old_small_gap_is_only_a_note(self):
        df = candles().drop(index=[50])                   # outside the newest 300
        _, r = check(df, now=now_after(candles()))
        self.assertEqual(r["state"], dq.GOOD)
        self.assertTrue(any("missing" in n for n in r["notes"]))

    def test_many_missing_is_unsafe(self):
        df = candles().drop(index=range(10, 20))           # 10 of 500 = 2% > 1%
        _, r = check(df, now=now_after(candles()))
        self.assertEqual(r["state"], dq.UNSAFE)

    def test_off_grid_timestamp_is_unsafe(self):
        df = candles()
        df.loc[200, "open_time"] += 60_000                 # 1 minute off the hourly grid
        _, r = check(df)
        self.assertEqual(r["state"], dq.UNSAFE)

    def test_zero_negative_and_missing_prices_are_unsafe(self):
        for col, val in [("close", 0.0), ("low", -5.0), ("open", np.nan)]:
            df = candles()
            df.loc[300, col] = val
            _, r = check(df)
            self.assertEqual(r["state"], dq.UNSAFE, (col, val))

    def test_high_below_low_is_unsafe(self):
        df = candles()
        hi, lo = df.loc[300, "high"], df.loc[300, "low"]
        df.loc[300, "high"], df.loc[300, "low"] = lo, hi
        _, r = check(df)
        self.assertEqual(r["state"], dq.UNSAFE)
        self.assertTrue(any("high below low" in p for p in r["problems"]))

    def test_close_outside_range_is_unsafe(self):
        df = candles()
        df.loc[300, "close"] = df.loc[300, "high"] * 1.05
        _, r = check(df)
        self.assertEqual(r["state"], dq.UNSAFE)

    def test_negative_volume_is_unsafe(self):
        df = candles()
        df.loc[300, "volume"] = -1
        self.assertEqual(check(df)[1]["state"], dq.UNSAFE)

    def test_stale_feed_is_unsafe(self):
        df = candles()
        self.assertEqual(check(df, now=now_after(df) + H)[1]["state"], dq.GOOD)       # 1 late: fine
        _, r = check(df, now=now_after(df) + 3 * H)                                   # 3+ late
        self.assertEqual(r["state"], dq.UNSAFE)
        self.assertTrue(any("stale" in p for p in r["problems"]))

    def test_volume_spike_warning_vs_degraded(self):
        df = candles()
        med = df["volume"].iloc[-51:-1].median()
        df.loc[499, "volume"] = med * 15
        _, r = check(df)
        self.assertEqual(r["state"], dq.GOOD)              # a real breakout can do 15x
        self.assertTrue(any("volume spike" in n for n in r["notes"]))
        df.loc[499, "volume"] = med * 80
        self.assertEqual(check(df)[1]["state"], dq.DEGRADED)

    def test_input_is_not_modified(self):
        df = candles().sample(frac=1, random_state=1)
        before = df.copy()
        check(df, now=now_after(candles()))
        pd.testing.assert_frame_equal(df, before)


class LookAhead(unittest.TestCase):
    """The verdict at time t may only depend on candles CLOSED by t (no peeking at the future)."""

    def test_future_candles_never_change_a_past_verdict(self):
        full = candles(600)
        full.loc[590, "low"] = -1.0                       # a disaster planted in the FUTURE
        for k in (350, 450, 550):
            now = int(full["open_time"].iloc[k - 1]) + H + 1   # candle k-1 just closed
            clean_past, r_past = check(full.iloc[:k], now=now)
            clean_all, r_all = check(full, now=now)           # same moment, future rows present
            self.assertEqual(r_past["state"], dq.GOOD)
            self.assertEqual(r_all["state"], r_past["state"], k)
            self.assertEqual(r_all["problems"], r_past["problems"])
            pd.testing.assert_frame_equal(clean_all, clean_past)

    def test_past_problem_is_seen_once_it_closes(self):
        full = candles(600)
        full.loc[590, "low"] = -1.0
        now = int(full["open_time"].iloc[590]) + H + 1        # candle 590 has now closed
        self.assertEqual(check(full, now=now)[1]["state"], dq.UNSAFE)


class CrossVenueAndSystem(unittest.TestCase):
    def test_cross_venue(self):
        out = dq.cross_venue({"BTC": 100.0, "ETH": 100.0, "XRP": 1.0},
                             {"BTC": 100.3, "ETH": 100.8, "XRP": None}, 0.5)
        self.assertEqual(out["BTC"]["state"], dq.GOOD)
        self.assertEqual(out["ETH"]["state"], dq.DEGRADED)
        self.assertEqual(out["XRP"]["state"], dq.GOOD)            # not listed there: not guessed
        self.assertIsNone(out["XRP"]["deviation_pct"])

    def test_cross_venue_unavailable_is_not_guessed(self):
        out = dq.cross_venue({"BTC": 100.0}, None)
        self.assertEqual(out["BTC"]["state"], dq.GOOD)
        self.assertIn("not available", out["BTC"]["note"])

    def test_system_state(self):
        good = {c: dq.GOOD for c in ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "LINK", "DOT", "LTC", "AVAX"]}
        self.assertEqual(dq.system_state(good)[0], dq.GOOD)
        self.assertEqual(dq.system_state(dict(good, ETH=dq.DEGRADED))[0], dq.DEGRADED)
        self.assertEqual(dq.system_state(dict(good, ETH=dq.UNSAFE))[0], dq.DEGRADED)
        self.assertEqual(dq.system_state(dict(good, BTC=dq.UNSAFE))[0], dq.UNSAFE)
        four_bad = dict(good, ETH=dq.UNSAFE, SOL=dq.UNSAFE, BNB=dq.UNSAFE, XRP=dq.UNSAFE)
        self.assertEqual(dq.system_state(four_bad)[0], dq.UNSAFE)          # 40% > 30%
        self.assertEqual(dq.system_state(good, failed=["ETH"])[0], dq.DEGRADED)
        self.assertEqual(dq.system_state(good, failed=["ETH", "SOL", "BNB", "XRP"])[0], dq.UNSAFE)
        self.assertEqual(dq.system_state({})[0], dq.UNSAFE)
        self.assertEqual(dq.system_state({"ETH": dq.GOOD})[0], dq.UNSAFE)   # BTC missing


def run_copy(tmp, *args):
    """Run scanner.py in a throw-away copy of the repo, so real reports/ are never touched."""
    for name in ("scanner.py", "notify.py", "config.yaml", "strategies.yaml", "publish_live.py", "pine_export.py"):
        shutil.copy(os.path.join(ROOT, name), tmp)
    lab = os.path.join(tmp, "strategies_lab.yaml")
    if not os.path.exists(lab):                  # an EMPTY lab: engine tests must not depend on today's lab cards
        head = []
        with open(os.path.join(ROOT, "strategies_lab.yaml")) as f:
            for line in f:
                if line.startswith("- "):
                    break
                head.append(line)
        with open(lab, "w") as f:
            f.write("".join(head))
    if not os.path.exists(os.path.join(tmp, "engine")):
        shutil.copytree(os.path.join(ROOT, "engine"), os.path.join(tmp, "engine"),
                        ignore=shutil.ignore_patterns("__pycache__"))
    return subprocess.run([sys.executable, *args], cwd=tmp, capture_output=True, text=True, timeout=600)


_SHARED = {}


def shared_offline_run():
    """ONE plain `scanner.py --offline` run per test process, shared by the tests that only READ its
    output (features, SMC, timeframes, strategy gates). Returns (folder, finished process).
    Tests that plant faults, change files or need several runs keep their own run_copy()."""
    if "run" not in _SHARED:
        tmp = tempfile.mkdtemp(prefix="shared_scan_")
        atexit.register(shutil.rmtree, tmp, True)
        _SHARED["run"] = (tmp, run_copy(tmp, "scanner.py", "--offline"))
    return _SHARED["run"]


class EndToEnd(unittest.TestCase):
    """Whole engine on synthetic data (--offline), with and without planted faults."""

    def scan(self, tmp, *extra):
        p = run_copy(tmp, "scanner.py", "--offline", "--coins", "6", *extra)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        return (json.load(open(os.path.join(tmp, "reports", "data_quality.json"))),
                open(os.path.join(tmp, "reports", "latest.md")).read())

    def test_clean_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            q, md = self.scan(tmp)
            self.assertEqual(q["system_state"], dq.GOOD)
            self.assertIn("## 0. Data check", md)

    def test_stale_btc_disables_all_signals_and_emails_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            q, md = self.scan(tmp, "--fault", "stale_btc")
            self.assertEqual(q["system_state"], dq.UNSAFE)
            self.assertEqual(q["status_code"], "DATA_STALE / SIGNAL_DISABLED")
            self.assertIn("DATA_STALE / SIGNAL_DISABLED", md)
            self.assertEqual(json.load(open(os.path.join(tmp, "reports", "latest.json")))["signals"], [])
            env = dict(os.environ, DRY_RUN="1")
            first = subprocess.run([sys.executable, "notify.py", "system"], cwd=tmp, env=env,
                                   capture_output=True, text=True)
            self.assertIn("Subject: ! Market data unsafe · signals paused", first.stdout)
            again = subprocess.run([sys.executable, "notify.py", "system"], cwd=tmp, env=env,
                                   capture_output=True, text=True)
            self.assertNotIn("Subject:", again.stdout)                # no repeat every hour
            self.scan(tmp)                                           # data healthy again
            back = subprocess.run([sys.executable, "notify.py", "system"], cwd=tmp, env=env,
                                  capture_output=True, text=True)
            self.assertIn("Subject: ✓ Fixed · market data OK", back.stdout)

    def test_bad_prices_on_one_coin_block_only_that_coin(self):
        with tempfile.TemporaryDirectory() as tmp:
            q, _ = self.scan(tmp, "--fault", "bad_prices")
            self.assertEqual(q["coins"]["ETH"]["state"], dq.UNSAFE)
            self.assertEqual(q["coins"]["BTC"]["state"], dq.GOOD)
            self.assertEqual(q["system_state"], dq.DEGRADED)


if __name__ == "__main__":
    unittest.main()
