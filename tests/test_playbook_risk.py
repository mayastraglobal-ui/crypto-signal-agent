"""Step 3c: the operator's playbook risk rules for its PB-* strategies (engine/risk.py check_pb, pb_size_factor),
the coin filters, the isolated-margin leverage limit and the playbook's stricter pass bar."""
import datetime as dt
import os
import sys
import unittest

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import research  # noqa: E402
import scanner as sc  # noqa: E402
from engine import scalp_playbook as pbk  # noqa: E402
from engine import risk as rk  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
NOW = dt.datetime(2026, 10, 7, 14, 0, tzinfo=dt.timezone.utc)      # a Wednesday, NY session


def row(**kw):
    r = {c: np.nan for c in sc.LOG_COLS}
    r.update(id=kw.get("id", "x"), coin="BTC", tf="5m", strategy="PB-B-SWEEP", version="1.0", direction="LONG",
             stage="APPROVED", state="CLOSED", status="SL", result_r=-1.0, closed_time_utc="2026-10-07 10:00",
             entry_time_utc="2026-10-07 09:30", signal_time_utc="2026-10-07 09:29")
    r.update(kw)
    return r


def plan(**kw):
    p = dict(coin="ETH", timeframe="5m", strategy="PB-A-PULLBACK", version="1.0", direction="LONG", entry=100.0,
             stop=99.0, tp1=101.0, signal_ms=int(NOW.timestamp() * 1000), levels=[], gate="playbook", risk_pct=0.5)
    p.update(kw)
    return p


def book(rows, events=(), coins=None):
    S = rk.settings(CFG.get("risk"), list(events))
    S["playbook"] = rk.pb_settings(CFG.get("playbook"))
    S["pb_coins"] = coins
    return rk.Book(pd.DataFrame(rows, columns=sc.LOG_COLS) if rows else pd.DataFrame(columns=sc.LOG_COLS), NOW, S, {})


class Rules(unittest.TestCase):
    def test_playbook_plans_skip_the_agent_tp1_and_path_rules(self):
        self.assertEqual(book([]).check(plan()), [])                          # TP1 = 1R is fine for the playbook
        self.assertIn("rr_tp1", book([]).check(plan(gate="trend")))           # the agent's rule for the others

    def test_two_positions_and_open_risk(self):
        rows = [row(id="a", state="POSITION_ACTIVE", status="OPEN", result_r=np.nan, coin="SOL"),
                row(id="b", state="POSITION_ACTIVE", status="OPEN", result_r=np.nan, coin="XRP")]
        self.assertIn("pb_heat", book(rows).check(plan()))
        self.assertIn("pb_open_risk", book(rows[:1]).check(plan(risk_pct=1.0)))
        self.assertNotIn("pb_open_risk", book(rows[:1]).check(plan(risk_pct=0.5)))

    def test_daily_loss_and_losing_streaks(self):
        two = [row(id="a", result_r=-1.0, closed_time_utc="2026-10-07 09:00"),
               row(id="b", result_r=-1.0, closed_time_utc="2026-10-07 10:00")]
        self.assertIn("pb_day_halt", book(two).check(plan()))                 # -2R today
        three = [row(id=str(i), result_r=-0.5, closed_time_utc=f"2026-10-07 13:{40 + i * 5}") for i in range(3)]
        self.assertIn("pb_losses_pause", book(three).check(plan()))           # 3rd loss at 13:50: break until 14:20
        later = [dict(r, closed_time_utc=r["closed_time_utc"].replace("13:", "12:")) for r in three]
        self.assertNotIn("pb_losses_pause", book(later).check(plan()))        # the break is over
        four = three + [row(id="9", result_r=-0.1, closed_time_utc="2026-10-07 13:55")]
        self.assertIn("pb_losses_stop", book(four).check(plan()))
        won = three + [row(id="9", result_r=0.8, closed_time_utc="2026-10-07 13:58")]
        self.assertNotIn("pb_losses_pause", book(won).check(plan()))          # a win ends the streak

    def test_max_trades_a_day_counts_this_run_too(self):
        rows = [row(id=str(i), result_r=0.2, entry_time_utc=f"2026-10-07 0{i}:00", closed_time_utc=f"2026-10-07 0{i}:30")
                for i in range(5)]
        b = book(rows)
        self.assertEqual(b.check(plan()), [])
        b.accept(plan())
        self.assertIn("pb_trades_day", b.check(plan(coin="SOL")))

    def test_news_window_is_15_minutes_and_coin_list(self):
        ev = [{"utc": "2026-10-07 14:20", "type": "CPI", "name": "CPI"}]
        self.assertNotIn("pb_blackout", book([], ev).check(plan()))           # 20 min away: allowed by the playbook
        self.assertIn("blackout", book([], ev).check(plan(gate="trend")))     # the agent's 60 min for the others
        ev2 = [{"utc": "2026-10-07 14:10", "type": "CPI", "name": "CPI"}]
        self.assertIn("pb_blackout", book([], ev2).check(plan()))
        self.assertIn("pb_coin", book([], coins=["BTC"]).check(plan()))


class Size(unittest.TestCase):
    def test_half_size_rules(self):
        PB = rk.pb_settings(CFG.get("playbook"))
        empty = pd.DataFrame(columns=sc.LOG_COLS)
        self.assertEqual(rk.pb_size_factor(empty, NOW, PB)[0], 1.0)
        self.assertEqual(rk.pb_size_factor(empty, NOW, PB, late=True)[0], 0.5)
        self.assertEqual(rk.pb_size_factor(empty, NOW, PB, half=True)[0], 0.5)
        big = pd.DataFrame([row(result_r=2.4, status="TP2")], columns=sc.LOG_COLS)
        f, why = rk.pb_size_factor(big, NOW, PB)
        self.assertEqual(f, 0.5)
        self.assertIn("after a win", why[0])
        bad_week = pd.DataFrame([row(id=str(i), result_r=-2.0, closed_time_utc=f"2026-09-3{i} 10:00") for i in range(3)],
                                columns=sc.LOG_COLS)
        self.assertEqual(rk.last_week_r(bad_week, NOW), -6.0)
        self.assertEqual(rk.pb_size_factor(empty, NOW, PB, last_week_r=-6.0)[0], 0.5)

    def test_coin_list_and_isolated_leverage(self):
        sec = CFG["playbook"]
        stats = {"BTC": (9e9, 0.001), "ETH": (5e9, 0.002), "SOL": (8e8, 0.01), "BNB": (3e8, 0.01),
                 "XRP": (9e8, 0.05)}
        self.assertEqual(pbk.coin_list(sec, stats), ["BTC", "ETH", "SOL"])   # BNB too thin, XRP spread too wide
        self.assertIsNone(pbk.coin_list(sec, {}))                            # unknown: no filter, not a guess
        self.assertEqual(pbk.max_isolated_leverage(60_000, 150, 2.0), 133)   # 60000 / (3 x 150)


class PassBar(unittest.TestCase):
    def test_playbook_cards_need_the_stricter_bar(self):
        V = CFG["validation"]
        pb = research.playbook_bar(V, {"gate": "playbook"}, CFG)
        self.assertEqual((pb["min_expectancy_r"], pb["min_profit_factor"], pb["min_trades"]),
                         (max(V["min_expectancy_r"], 0.15), max(V["min_profit_factor"], 1.3), max(V["min_trades"], 100)))
        self.assertIs(research.playbook_bar(V, {"gate": "trend"}, CFG), V)


if __name__ == "__main__":
    unittest.main()
