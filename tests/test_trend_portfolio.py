"""Trend portfolio (2026-10-29, operator: "build trend portfolio") - paper only: 9 daily trend signals per own coin
(ON at a close above the lookback's high, OFF below its ratcheting mid-line), target = the share ON. The signals, the
paper account (costs, catch-up, booked once per day), the daily step, the Telegram message and the watcher's once-a-day
note and /portfolio command."""
import os
import shutil
import sys
import tempfile
import time
import types
import unittest

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import trend_portfolio as TPS  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import trend_portfolio as TP  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
DAY = TP.DAY_MS
T0 = 1_760_000_000_000 // DAY * DAY


def daily(close, t0=T0):
    c = np.asarray(close, dtype=float)
    return pd.DataFrame(dict(open_time=t0 + np.arange(len(c), dtype=np.int64) * DAY, high=c * 1.001, low=c * 0.999,
                             close=c))


S = TP.settings(dict(lookbacks=[3, 5]), dict(taker_fee_pct=0.05, slippage_pct=0.05, funding_pct_per_8h=0.01))


class Signals(unittest.TestCase):
    def test_on_at_a_new_high_off_below_the_ratcheting_midline(self):
        c = [100] * 6 + [101, 103, 106, 110, 111, 108, 104, 100]
        d = daily(c)
        on = TP.signal_states(d["high"], d["low"], d["close"], 3)
        self.assertEqual(list(on[:6]), [0] * 6)
        self.assertEqual(on[6], 1)                                     # a close above the 3-day high
        self.assertEqual(list(on[6:11]), [1] * 5)                      # held while it rises (the mid-line ratchets up)
        self.assertEqual(on[11], 0)                                    # 108 < the mid-line of 106 / 110 / 111 (~108.5)
        self.assertEqual(list(on[12:]), [0, 0])

    def test_target_is_the_share_on(self):
        t = TP.targets(daily([100] * 8 + [101, 103]), S)
        self.assertEqual(int(t["n"].iloc[-1]), 2)
        self.assertEqual(float(t["weight"].iloc[-1]), 1.0)
        self.assertEqual(int(t["longest_on"].iloc[-1]), 5)
        self.assertEqual(float(t["weight"].iloc[0]), 0.0)

    def test_config_and_costs(self):
        s = TP.settings(CFG.get("trend_portfolio"), CFG["costs"]["long"])
        self.assertEqual(s["lookbacks"], [5, 10, 20, 30, 60, 90, 150, 250, 360])
        self.assertAlmostEqual(s["side_cost_pct"], 0.10)              # OKX taker 0.05% + slippage 0.05%
        self.assertEqual((s["paper_capital"], s["enabled"]), (1000.0, True))


class PaperAccount(unittest.TestCase):
    def test_day_return(self):
        r = TP.day_return({"BTC": 1.0, "ETH": 0.0}, {"BTC": 0.5, "ETH": 0.0}, {"BTC": 0.10, "ETH": -0.5}, S)
        # BTC: +10% - 0.5 x 0.1% sell - 0.03% funding; ETH: nothing held; equal parts
        self.assertAlmostEqual(r, (0.10 - 0.0005 - 0.0003) / 2)
        self.assertAlmostEqual(TP.day_return({}, {"BTC": 1}, {}, S, ["BTC", "ETH", "SOL"]), -0.001 / 3)   # unlisted = cash

    def test_first_day_then_one_day_at_a_time(self):
        c = [100] * 8 + [101, 103, 106, 110]
        st = TP.update(None, {"BTC": daily(c[:-1]), "ETH": daily([50] * 11)}, S, T0)
        self.assertEqual(len(st["history"]), 1)                       # starts on the newest day only
        self.assertAlmostEqual(st["equity"], 1000 * (1 - 0.001 / 2), places=2)   # buying BTC in
        self.assertEqual(st["coins"]["BTC"]["weight"], 1.0)
        self.assertEqual(st["coins"]["ETH"]["on"], 0)
        again = TP.update(st, {"BTC": daily(c[:-1]), "ETH": daily([50] * 11)}, S, T0)
        self.assertEqual(len(again["history"]), 1)                    # the same day is never booked twice
        nxt = TP.update(st, {"BTC": daily(c), "ETH": daily([50] * 12)}, S, T0)
        self.assertEqual(len(nxt["history"]), 2)
        exp = st["equity"] * (1 + (110 / 106 - 1 - 0.0003) / 2)
        self.assertAlmostEqual(nxt["equity"], exp, places=1)
        self.assertEqual(nxt["started"], st["started"])

    def test_missed_days_are_caught_up(self):
        c = [100] * 8 + [101, 103, 106, 110, 111, 112]
        st = TP.update(None, {"BTC": daily(c[:10])}, S, T0)
        nxt = TP.update(st, {"BTC": daily(c)}, S, T0)
        self.assertEqual([h["day"] for h in nxt["history"]][-4:],
                         [pd.to_datetime(T0 + k * DAY, unit="ms").strftime("%Y-%m-%d") for k in range(10, 14)])

    def test_backtest_and_texts(self):
        rng = np.random.default_rng(0)
        frames = {"BTC": daily(100 * np.exp(np.cumsum(rng.normal(0.002, 0.03, 400)))),
                  "ETH": daily(50 * np.exp(np.cumsum(rng.normal(0.0, 0.03, 400))))}
        bt = TP.backtest(frames, S)
        self.assertEqual(set(bt), {"since", "days", "portfolio", "hold"})
        self.assertIsNotNone(bt["portfolio"]["max_dd_pct"])
        st = dict(TP.update(None, frames, S, T0), backtest=bt)
        text = TP.telegram_text(st)
        self.assertIn("Trend portfolio</b> (PAPER)", text)
        self.assertIn("First day of the paper account", text)
        self.assertIn("Paper only", text)
        st2 = TP.update(st, {k: daily(np.r_[v["close"].to_numpy(), v["close"].iloc[-1] * 1.3]) for k, v in frames.items()},
                        S, T0)
        t2 = TP.telegram_text(st2)
        self.assertNotIn("First day", t2)
        self.assertTrue("Changes today" in t2 or "No changes today" in t2)
        self.assertIn("| Coin | Trends up |", TP.markdown(st2))
        self.assertIn("no data yet", TP.telegram_text(None))


class DailyStep(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.path, self.page = os.path.join(self.tmp, "tp.json"), os.path.join(self.tmp, "tp.md")

    class Feed:
        def __init__(self, n=400, missing=()):
            self.calls, self.n, self.missing = 0, n, set(missing)

        def klines(self, symbol, tf, n):
            self.calls += 1
            if symbol[:-4] in self.missing:
                raise OSError("down")
            now = int(time.time() * 1000) // DAY * DAY            # closed daily candles up to yesterday
            c = 100 * np.exp(np.cumsum(np.full(self.n, 0.002)))
            ot = now - DAY * np.arange(self.n, 0, -1)
            return TPS.sc._finish(pd.DataFrame(dict(open_time=ot, open=c, high=c * 1.01, low=c * 0.99, close=c,
                                                    volume=np.ones(self.n), quote_volume=np.ones(self.n))), "1d")

    def test_once_per_daily_close(self):
        now = int(time.time() * 1000)
        feed = self.Feed()
        st, note = TPS.run(CFG, feed, now, path=self.path, page=self.page)
        self.assertIn("booked", note)
        self.assertTrue(os.path.exists(self.page))
        n = feed.calls
        st2, note2 = TPS.run(CFG, feed, now + 60_000, path=self.path, page=self.page)
        self.assertIn("up to date", note2)
        self.assertEqual(feed.calls, n)                             # nothing downloaded until the next close
        self.assertEqual(st2["day"], st["day"])

    def test_no_btc_no_write(self):
        st, note = TPS.run(CFG, self.Feed(missing={"BTC"}), int(time.time() * 1000), path=self.path, page=self.page)
        self.assertIsNone(st)
        self.assertFalse(os.path.exists(self.path))

    def test_a_missing_coin_is_reported_not_fatal(self):
        st, note = TPS.run(CFG, self.Feed(missing={"SUI"}), int(time.time() * 1000), path=self.path, page=self.page)
        self.assertNotIn("SUI", st["coins"])
        self.assertIn("SUI: download failed", note)

    def test_workflow_step(self):
        scan = open(os.path.join(ROOT, ".github", "workflows", "scan.yml"), encoding="utf-8").read()
        self.assertLess(scan.index("python scanner.py"), scan.index("python trend_portfolio.py"))
        self.assertLess(scan.index("python trend_portfolio.py"), scan.index("Save reports"))


class Watcher(unittest.TestCase):
    def fake(self, st, on=True):
        said = []
        w = types.SimpleNamespace(_json=lambda rel: st, cfg=CFG, state={"portfolio_on": on}, say=said.append,
                                  _save_state=lambda: None)
        return w, said

    def test_one_message_per_day(self):
        st = {"day": "2026-10-28", "coins": {"BTC": dict(on=2, n=9, weight=0.22, yesterday=0.22, price=1.0, usd=32,
                                                       change_usd=0, longest_on=10)},
              "equity": 1000, "start_capital": 1000, "started": "2026-10-28", "invested_usd": 32, "history": [{}]}
        w, said = self.fake(st)
        self.assertTrue(LW.Watcher.portfolio_note(w))
        self.assertFalse(LW.Watcher.portfolio_note(w))              # the same day again: nothing
        self.assertEqual(len(said), 1)
        self.assertIn("BTC", said[0])
        w2, said2 = self.fake(st, on=False)
        self.assertFalse(LW.Watcher.portfolio_note(w2))             # /portfolio off

    def test_files_command_and_help(self):
        self.assertIn(("main", "reports/trend_portfolio.json"), LW.SYNC_FILES)
        self.assertIn("engine/trend_portfolio.py", LW.CODE_FILES)
        self.assertIn("/portfolio", lv.HELP)
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn('if cmd == "portfolio":', src)
        self.assertIn("self.portfolio_note()", src)


if __name__ == "__main__":
    unittest.main()
