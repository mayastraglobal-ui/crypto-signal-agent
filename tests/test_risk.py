"""Phase 11 tests: the risk engine (section 14 steps 9-13, section 15) and the event blackout.

Run:  python -m unittest discover -s tests -v
"""
import datetime as dt
import json
import os
import subprocess
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
from engine import positions as P  # noqa: E402
from engine import risk as RK  # noqa: E402
from test_data_quality import run_copy  # noqa: E402

CFG = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
NOW = dt.datetime(2026, 9, 24, 12, 0, tzinfo=dt.timezone.utc)          # a Thursday
NOW_MS = int(NOW.timestamp() * 1000)
MIN = 60_000


def S(**kw):
    return RK.settings(dict(CFG["risk"], **kw.pop("risk", {})), kw.pop("events", []))


def row(**kw):
    r = {c: np.nan for c in scanner.LOG_COLS}
    r.update(id=kw.get("id", "x"), signal_time_utc="2026-09-24 08:00", coin="BTC", tf="1h", strategy="T",
             direction="LONG", entry=100.0, stop=95.0, tp1=110.0, max_hold_bars=10, status="OPEN", version="1.0",
             stage="APPROVED", state=P.ACTIVE, closed_time_utc="", entry_time_utc="2026-09-24 08:00")
    r.update(kw)
    return r


def closed(r, when, **kw):
    return row(state=P.CLOSED, status="SL" if r < 0 else "TP1", result_r=r, closed_time_utc=when, **kw)


def log(*rows):
    return pd.DataFrame(list(rows), columns=scanner.LOG_COLS)


def plan(**kw):
    p = dict(coin="SOL", timeframe="1h", strategy="T", version="1.0", direction="LONG", entry=100.0, stop=95.0,
             tp1=110.0, signal_ms=NOW_MS - 5 * MIN, levels=[])
    p.update(kw)
    return p


class Calendar(unittest.TestCase):
    def test_parse_and_bad_entries(self):
        ev = RK.parse_events([{"utc": "2026-10-14 12:30", "type": "CPI", "name": "US CPI"},
                              {"from": "2026-10-02 08:00", "until": "2026-10-02 11:00", "type": "exchange_incident"}])
        self.assertEqual([e[2] for e in ev], ["exchange_incident", "CPI"])          # sorted by time
        for bad in ([{"utc": "not a date"}], [{"from": "2026-10-02 11:00", "until": "2026-10-02 08:00"}],
                    [{"name": "no time"}]):
            with self.assertRaises(ValueError):
                RK.parse_events(bad)

    def test_blackout_window_edges(self):
        ev = RK.parse_events([{"utc": "2026-09-24 12:30", "name": "US CPI"}])
        t = ev[0][0]
        for off, inside in ((-60, True), (-61, False), (0, True), (60, True), (61, False)):
            self.assertEqual(bool(RK.blackout(t + off * MIN, ev, 60)), inside, off)
        inc = RK.parse_events([{"from": "2026-09-24 08:00", "until": "2026-09-24 11:00", "name": "incident"}])
        self.assertTrue(RK.blackout(inc[0][0] + 90 * MIN, inc, 60))                  # the whole span
        self.assertTrue(RK.blackout(inc[0][1] + 60 * MIN, inc, 60))
        self.assertFalse(RK.blackout(inc[0][1] + 61 * MIN, inc, 60))

    def test_upcoming(self):
        ev = RK.parse_events([{"utc": "2026-09-25 12:30", "name": "a"}, {"utc": "2026-10-10 12:30", "name": "b"},
                              {"utc": "2026-09-20 12:30", "name": "old"}])
        self.assertEqual([e[3] for e in RK.upcoming(ev, NOW_MS, 7)], ["a"])


class Limits(unittest.TestCase):
    def test_day_and_week_count_only_closed_live_results(self):
        lg = log(closed(-1.5, "2026-09-24 09:00"), closed(-1.0, "2026-09-24 11:00"),
                 closed(-2.0, "2026-09-22 10:00"),                                # Tuesday: week only
                 closed(-5.0, "2026-09-21 00:00"),                                # Monday 00:00: week
                 closed(-9.0, "2026-09-20 23:59"),                                # Sunday before: neither
                 closed(-4.0, "2026-09-24 09:00", stage="PAPER_TRADING"),         # paper: neither
                 row(state=P.EXPIRED, status="EXPIRED", closed_time_utc="2026-09-24 09:00"))
        self.assertEqual(RK.day_week_r(lg, NOW), (-2.5, -9.5))

    def test_halts_at_the_limits(self):
        for day, halted in ((-2.99, False), (-3.0, True)):
            b = RK.Book(log(closed(day, "2026-09-24 09:00")), NOW, S(), {})
            self.assertEqual("day_halt" in b.check(plan()), halted, day)
        b = RK.Book(log(closed(-2.0, "2026-09-24 09:00"), closed(-4.0, "2026-09-22 09:00")), NOW, S(), {})
        self.assertEqual(b.check(plan()), ["week_halt"])

    def test_strategy_suspension_and_resume(self):
        rows = [closed(r, f"2026-09-{d:02d} 10:00", tf="1h") for d, r in
                ((10, 3.0), (11, -2.0), (12, -3.0), (13, -2.5), (14, -1.0))]      # 3R up, then 8.5R down
        b = RK.Book(log(*rows), NOW, S(), {})
        self.assertEqual(b.dd["T@1.0|1h"], 8.5)
        self.assertEqual(b.suspended(), ["T@1.0|1h"])
        self.assertIn("suspended", b.check(plan()))
        self.assertNotIn("suspended", b.check(plan(timeframe="4h")))              # per version x timeframe
        b = RK.Book(log(*rows), NOW, S(risk=dict(resume={"T@1.0|1h": "2026-09-13"})), {})
        self.assertEqual((b.dd["T@1.0|1h"], b.suspended()), (3.5, []))
        b = RK.Book(log(*rows[:-1]), NOW, S(), {})
        self.assertEqual(b.suspended(), [])                                       # 7.5R: not yet


class Heat(unittest.TestCase):
    def test_positions_coin_and_correlated_exposure(self):
        groups = {"BTC": "BTC+ETH", "ETH": "BTC+ETH", "SOL": "SOL", "ADA": "ADA", "XRP": "XRP"}
        opened = log(row(id="a", coin="BTC"), row(id="b", coin="SOL", state=P.AWAITING, strategy="U"),
                     row(id="c", coin="ADA", stage="PAPER_TRADING"))                # paper does not count
        b = RK.Book(opened, NOW, S(), groups)
        self.assertEqual(b.check(plan(coin="XRP")), [])
        self.assertEqual(b.check(plan(coin="SOL")), ["coin"])
        self.assertEqual(b.check(plan(coin="ETH")), ["correlated"])
        self.assertEqual(b.check(plan(coin="ETH", direction="SHORT", stop=105.0, tp1=90.0)), [])   # a hedge
        b.accept(plan(coin="XRP"))
        self.assertEqual(b.check(plan(coin="ADA")), ["heat"])                      # 3 open now

    def test_correlation_groups(self):
        rng = np.random.default_rng(0)
        base = rng.normal(0, 0.01, 800)
        idx = np.arange(800)

        def px(r):
            return pd.Series(100 * np.exp(np.cumsum(r)), index=idx)
        closes = {"BTC": px(base), "ETH": px(base + rng.normal(0, 0.004, 800)),
                  "SOL": px(base + rng.normal(0, 0.004, 800)), "XRP": px(rng.normal(0, 0.01, 800))}
        g = RK.corr_groups(closes, 0.7, 720)
        self.assertEqual(g["BTC"], "BTC+ETH+SOL")
        self.assertEqual(g["ETH"], g["SOL"])
        self.assertEqual(g["XRP"], "XRP")
        self.assertEqual(RK.corr_groups({"BTC": px(base)}, 0.7, 720), {"BTC": "BTC"})
        a, b = rng.normal(0, 0.01, 800), rng.normal(0, 0.01, 800)          # A, B unrelated; C moves with both
        g = RK.corr_groups({"A": px(a), "B": px(b), "C": px(a + b)}, 0.6, 720)
        self.assertEqual(set(g.values()), {"A+B+C"})                          # joined through C


class EntryRules(unittest.TestCase):
    def test_reward_to_tp1_at_least_2r(self):
        b = RK.Book(log(), NOW, S(), {})
        self.assertEqual(b.check(plan(tp1=110.0)), [])                             # exactly 2R
        self.assertEqual(b.check(plan(tp1=109.9)), ["rr_tp1"])
        self.assertEqual(b.check(plan(direction="SHORT", stop=105.0, tp1=90.1)), ["rr_tp1"])
        self.assertEqual(b.check(plan(direction="SHORT", stop=105.0, tp1=90.0)), [])

    def test_path_to_tp1(self):
        b = RK.Book(log(), NOW, S(), {})
        self.assertEqual(b.check(plan(levels=[105.0])), ["path"])                  # pool before TP1
        self.assertEqual(b.check(plan(levels=[110.0])), [])                        # the target itself
        self.assertEqual(b.check(plan(levels=[109.8])), [])                        # within 0.05R of TP1
        self.assertEqual(b.check(plan(levels=[112.0, 94.0, float("nan")])), [])    # beyond / behind / unknown
        self.assertEqual(b.check(plan(direction="SHORT", stop=105.0, tp1=90.0, levels=[95.0])), ["path"])

    def test_blackout_by_signal_time_or_now(self):
        ev = [{"utc": "2026-09-24 12:45", "name": "FOMC"}]
        b = RK.Book(log(), NOW, S(events=ev), {})
        self.assertEqual(b.check(plan()), ["blackout"])                            # now is 45 min before
        self.assertEqual(b.check(plan(signal_ms=NOW_MS - 120 * MIN)), ["blackout"])   # signal old, NOW inside
        ev = [{"utc": "2026-09-24 14:00", "name": "FOMC"}]
        self.assertEqual(RK.Book(log(), NOW, S(events=ev), {}).check(plan()), [])

    def test_duplicate_open_or_cooling_down(self):
        b = RK.Book(log(row(coin="SOL", tf="1h")), NOW, S(), {})
        self.assertIn("duplicate", b.check(plan()))
        lg = log(closed(1.0, "2026-09-24 11:00", coin="SOL"))
        self.assertEqual(RK.Book(lg, NOW, S(), {}).check(plan(), cooldown_ms=0), [])
        self.assertEqual(RK.Book(lg, NOW, S(), {}).check(plan(), cooldown_ms=4 * 3_600_000), ["duplicate"])
        self.assertEqual(RK.Book(lg, NOW, S(), {}).check(plan(strategy="U"), cooldown_ms=4 * 3_600_000), [])
        refused = log(row(coin="SOL", state=P.NO_TRADE, status=P.NO_TRADE, closed_time_utc="2026-09-24 11:00"),
                      row(coin="SOL", state=P.EXPIRED, status=P.EXPIRED, closed_time_utc="2026-09-24 11:00"))
        self.assertEqual(RK.Book(refused, NOW, S(), {}).check(plan(), cooldown_ms=4 * 3_600_000), [])   # no trade


class Sizing(unittest.TestCase):
    def test_formula_and_leverage_cap(self):
        z = RK.size(1000, 0.5, 100.0, 95.0, 3)
        self.assertAlmostEqual(z["qty"], 1.0)
        self.assertAlmostEqual(z["risk_usdt"], 5.0)
        self.assertFalse(z["capped"])
        z = RK.size(1000, 0.5, 100.0, 99.9, 3)                                     # 0.1% stop -> 5x needed
        self.assertTrue(z["capped"])
        self.assertAlmostEqual(z["leverage"], 3.0)
        self.assertLess(z["risk_usdt"], 5.0)                                       # smaller risk, never bigger

    def test_risk_pct_caps_and_first_month(self):
        s = S()
        self.assertEqual(RK.risk_pct(0.5, log(), NOW, s)[0], 0.5)
        self.assertEqual(RK.risk_pct(0.8, log(), NOW, s)[0], 0.5)                  # no live entry yet
        young = log(row(entry_time_utc="2026-09-10 08:00"))
        old = log(row(entry_time_utc="2026-08-01 08:00"))
        self.assertEqual(RK.risk_pct(0.8, young, NOW, s)[0], 0.5)
        self.assertEqual(RK.risk_pct(0.8, old, NOW, s)[0], 0.8)
        self.assertEqual(RK.risk_pct(2.0, old, NOW, s), (1.0, "config risk 2% is above the 1% maximum - capped"))
        self.assertEqual(RK.risk_pct(0.8, log(row(entry_time_utc="2026-08-01 08:00", stage="PAPER_TRADING")),
                                     NOW, s)[0], 0.5)                             # paper is not live

    def test_size_never_follows_results(self):              # no martingale, no "increase size after a loss"
        old = row(entry_time_utc="2026-08-01 08:00")
        losses = log(old, *[closed(-1.0, f"2026-09-{d:02d} 10:00", id=f"l{d}") for d in range(1, 20)])
        wins = log(old, *[closed(2.0, f"2026-09-{d:02d} 10:00", id=f"w{d}") for d in range(1, 20)])
        self.assertEqual(RK.risk_pct(0.8, losses, NOW, S()), RK.risk_pct(0.8, wins, NOW, S()))

    def test_stops_only_move_towards_profit(self):
        rng = np.random.default_rng(1)
        for trial in range(300):
            d = 1 if trial % 2 else -1
            c = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, 40)))
            o = np.r_[100, c[:-1]]
            h, l = np.maximum(o, c) * 1.002, np.minimum(o, c) * 0.998
            for n in range(2, 40, 7):
                info = {}
                res = scanner.simulate_trade(o[:n], h[:n], l[:n], c[:n], 0, d, 100.0, 2.0, CFG, 999, 1, None,
                                             [100 + d * 2, 100 + d * 4, 100 + d * 6], [0.4, 0.3, 0.3], info)
                if res is None:
                    self.assertGreaterEqual(d * (info["stop"] - (100 - d * 2.0)), 0, (trial, n))


class ApplyRisk(unittest.TestCase):
    def test_approved_fail_becomes_no_trade_paper_is_only_marked(self):
        b = RK.Book(log(), NOW, S(), {})
        plans = [dict(plan(coin=c, stage=st), confidence_score=sc) for c, st, sc in
                 (("A", "APPROVED", 0.9), ("B", "APPROVED", 0.8), ("C", "PAPER_TRADING", 0.95),
                  ("D", "APPROVED", 0.7), ("E", "APPROVED", 0.6), ("F", "APPROVED", 0.5))]
        plans[3]["tp1"] = 105.0                                                    # D: only 1R to TP1
        scanner.apply_risk(plans, b)
        by = {p["coin"]: p for p in plans}
        self.assertEqual([c for c in "ABCDEF" if by[c]["no_trade"]], ["D", "F"])   # F: heat (A, B, E open)
        self.assertEqual(by["D"]["risk_blocks"], ["rr_tp1"])
        self.assertEqual(by["F"]["risk_blocks"], ["heat"])
        self.assertFalse(by["C"]["no_trade"])                                      # paper: never NO_TRADE ...
        self.assertEqual(by["C"]["risk_blocks"], [])                               # ... checked first, book empty
        self.assertEqual(len(b.open), 3)


class Alerts(unittest.TestCase):
    def summary(self, lg, path):
        return scanner.risk_summary(lg, NOW, S(), {}, 0.5, "", None, [], path)

    def test_one_transition_when_a_halt_starts_and_one_when_it_ends(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "risk_state.json")
            bad = log(closed(-3.2, "2026-09-24 09:00"))
            self.assertEqual([t["kind"] + ":" + t["what"] for t in self.summary(bad, p)["transitions"]],
                             ["start:day_halt"])
            self.assertEqual(self.summary(bad, p)["transitions"], [])              # still halted: no repeat
            self.assertEqual([t["kind"] for t in self.summary(log(), p)["transitions"]], ["end"])
            r = self.summary(log(), p)
            self.assertIn("calendar not maintained", r["calendar_warning"])

    def test_calendar_problem_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = scanner.risk_summary(log(), NOW, S(), {}, 0.5, "", "events entry 1: bad", [],
                                     os.path.join(tmp, "s.json"))
        self.assertIn("error", r["calendar_warning"])


class EndToEnd(unittest.TestCase):
    def test_offline_scan_halts_after_a_bad_day_and_emails_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "reports"))
            today = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d")
            pd.DataFrame([closed(-3.5, today + " 00:00", id="bad", coin="BTC")], columns=scanner.LOG_COLS).to_csv(
                os.path.join(tmp, "reports", "signals_log_offline.csv"), index=False)
            env = dict(os.environ, DRY_RUN="1")
            p = run_copy(tmp, "scanner.py", "--offline", "--coins", "4")          # run 1: the halt starts
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            out = subprocess.run([sys.executable, "notify.py", "system"], cwd=tmp, env=env, capture_output=True,
                                 text=True).stdout
            self.assertIn("Subject: [SYSTEM] Risk HALT: day_halt", out)
            self.assertIn("POSITION BOOK", out)
            out = subprocess.run([sys.executable, "notify.py", "system"], cwd=tmp, env=env, capture_output=True,
                                 text=True).stdout
            self.assertNotIn("[SYSTEM] Risk", out)                                  # same run: never twice
            with open(os.path.join(tmp, "config.yaml")) as f:
                cfg = yaml.safe_load(f)
            soon = (pd.Timestamp.now(tz="UTC") + pd.Timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
            cfg["events"] = [{"utc": soon, "type": "FOMC", "name": "FOMC test"}]
            with open(os.path.join(tmp, "config.yaml"), "w") as f:
                yaml.safe_dump(cfg, f, sort_keys=False)
            p = subprocess.run([sys.executable, "scanner.py", "--offline", "--coins", "4"], cwd=tmp,
                               capture_output=True, text=True, timeout=600)            # run 2: still halted
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            with open(os.path.join(tmp, "reports", "latest.json")) as f:
                rep = json.load(f)
            r = rep["risk"]
            self.assertEqual((r["day_r"], r["halts"], r["transitions"]), (-3.5, ["day_halt"], []))
            self.assertEqual(r["blackout_now"], ["FOMC test"])
            self.assertIsNone(r["calendar_warning"])
            self.assertTrue(any(line.startswith("Risk:") and "daily loss limit" in line
                                for line in rep["position_book_text"]))
            with open(os.path.join(tmp, "reports", "latest.md")) as f:
                self.assertIn("### 2d. Risk engine", f.read())
            out = subprocess.run([sys.executable, "notify.py", "system"], cwd=tmp, env=env, capture_output=True,
                                 text=True).stdout
            self.assertNotIn("[SYSTEM] Risk", out)                                  # no change -> no email

if __name__ == "__main__":
    unittest.main()
