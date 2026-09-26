"""Phase 12 tests, format v2: the scan's trade emails (LIVE / PAPER signals and updates, FILLED, WARNING, PAPER
complete, the flood guard), reminders and chart images.

Run:  python -m unittest discover -s tests -v
"""
import datetime as dt
import json
import os
import re
import shutil
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
from engine import briefs as B  # noqa: E402
from engine import charts as CH  # noqa: E402
from engine import positions as P  # noqa: E402
from engine import risk as RK  # noqa: E402
from test_data_quality import shared_offline_run  # noqa: E402

CFG = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
NOW = dt.datetime(2026, 9, 24, 0, 7, tzinfo=dt.timezone.utc)
PNG = b"\x89PNG\r\n\x1a\n"


def card(**kw):
    e = dict(coin="ETH", quote="USDT", direction="LONG", market="spot", tf="15m", strategy="S6-OB-FVG", version="1.0",
             stage="APPROVED", utc="2026-09-24 00:07", beijing="2026-09-24 08:07", data_state="GOOD",
             regimes={"1w": "WEAK_BULL", "1d": "STRONG_BULL", "4h": "WEAK_BULL", "1h": "RANGE", "15m": "structure up"},
             entry=100.0, entry_zone=[99.0, 101.0], stop=95.0,
             targets=[dict(price=112.0, r=2.4, close_pct=50), dict(price=120.0, r=4.0, close_pct=50)],
             confirm_5m=None, size=dict(qty=1.0, usdt=100.0, risk_usdt=5.0, risk_pct=0.5, capped=False),
             expires="2026-09-24 00:22 UTC", why=["a", "b", "c"], invalidation=["x"], evidence=["e"])
    e.update(kw)
    return e


def candles(n=150, seed=0):
    rng = np.random.default_rng(seed)
    c = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    o = np.r_[100, c[:-1]]
    ot = 1_700_000_000_000 + 900_000 * np.arange(n)
    return pd.DataFrame(dict(open_time=ot, open=o, high=np.maximum(o, c) * 1.003, low=np.minimum(o, c) * 0.997,
                             close=c, close_time=ot + 899_999))


class Content(unittest.TestCase):
    """The v2 LIVE entry built from a scan card (engine/emails.py; the full design tests are in test_email_design)."""

    def test_entry_subject_and_body(self):
        m = scanner.emx.live_entry(card())
        self.assertEqual(m["subject"], "LIVE ▲ LONG ETH 15M · Enter 99.00–101.00 · Stop 95.00")
        for part in ("[LIVE] ENTRY SIGNAL", "Place a limit BUY between 99.00 and 101.00. Set the stop at 95.00",
                     "Stop  | 95.00 −1R", "TP1   | 112.00 +2.4R | Close 50%, move stop to entry",
                     "TP2   | 120.00 +4R", "Loss if stopped: 5.00 USDT (0.5% of account)"):
            self.assertIn(part, m["text"])
        self.assertNotIn("Futures only", m["text"])

    def test_short_is_futures_only_and_5m_bar_is_named(self):
        m = scanner.emx.live_entry(card(direction="SHORT", market="futures only", stop=105.0,
                                        targets=[dict(price=88.0, r=2.4, close_pct=100)],
                                        valid_note="Enter now: the 5m bar confirmed it",
                                        size=dict(qty=1.0, usdt=100.0, risk_usdt=5.0, risk_pct=0.5, capped=True)))
        self.assertTrue(m["subject"].startswith("LIVE ▼ SHORT ETH 15M ·"))
        self.assertIn("Futures only", m["text"])
        self.assertIn("Sell (futures) now near 100.00 – the 5m bar confirmed it", m["text"])
        self.assertIn("more would need over 3x leverage", m["text"])

    def test_why_points_come_from_facts(self):
        facts = dict(range_pos=0.3, sweep_ago=0, choch_ago=2, bos_ago=None, displacement_ago=None, fvg_retrace=True,
                     in_ob=False, rel_vol=1.4, structure="up")
        ctx = dict(htf_trend="UP", regime="WEAK_BULL", rsi14=55.1, volume_vs_avg=1.4)
        w = B.why_points(1, ctx, facts, "London", [])
        self.assertTrue(3 <= len(w) <= 5)
        text = " | ".join(w)
        for part in ("higher timeframe UP, regime WEAK_BULL", "change of character up 2 candle(s) ago",
                     "RSI(14) 55.1", "volume 1.4x", "liquidity below taken on the signal candle",
                     "price back in a fair value gap", "discount (30% of the dealing range)", "session: London"):
            self.assertIn(part, text)
        full = B.why_points(1, ctx, dict(facts, displacement_ago=1), "London", ["late_entry", "wrong_session"])
        self.assertEqual(len(full), 5)
        self.assertEqual(full[-1], "Caution: late entry, wrong session")       # never cut ...
        self.assertTrue(full[3].startswith("SMC context:"))                     # ... and nothing else is
        w = B.why_points(-1, ctx, dict(facts, range_pos=1.3), None, ["low_relative_volume"])
        self.assertIn("above the dealing range", " ".join(w))
        self.assertIn("liquidity above taken", " ".join(w))

    def test_facts_at_reads_only_up_to_the_signal_candle(self):
        n = 30
        feats = pd.DataFrame({k: np.zeros(n) for k in ("smc_sweep_bull", "smc_choch_up", "smc_bos_up",
                                                        "displacement_up", "smc_fvg_retrace_bull", "smc_in_bull_ob",
                                                        "smc_range_pos", "rel_vol")})
        feats["structure"] = "up"
        feats.loc[20, "smc_sweep_bull"] = 1
        feats.loc[25, "smc_choch_up"] = 1                    # AFTER the signal candle below
        f = B.facts_at(feats, 22, 1)
        self.assertEqual((f["sweep_ago"], f["choch_ago"]), (2, None))
        self.assertIsNone(B.facts_at(feats, 22, -1)["sweep_ago"])


class Charts(unittest.TestCase):
    def test_png_with_levels(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = candles()
            p = CH.trade_chart(d, os.path.join(tmp, "c", "x.png"), "T", 100.0, 95.0, [110.0, None, float("nan")],
                               int(d["open_time"].iloc[-10]), int(d["open_time"].iloc[-2]), 101.0, 100.0)
            with open(p, "rb") as f:
                self.assertEqual(f.read(8), PNG)
            self.assertGreater(os.path.getsize(p), 5000)
            with self.assertRaises(ValueError):
                CH.trade_chart(d.iloc[:0], os.path.join(tmp, "y.png"), "T", 1, 0.9, [])


def log_row(**kw):
    r = {c: np.nan for c in scanner.LOG_COLS}
    r.update(id="ETH-15m-S-t", signal_time_utc="2023-11-14 22:14", coin="ETH", tf="15m", strategy="S", version="1.0",
             direction="LONG", entry=100.0, stop=95.0, tp1=110.0, tp2=120.0, tp_split="0.5/0.5", max_hold_bars=10,
             status="OPEN", stage="APPROVED", state=P.ACTIVE, closed_time_utc="", entry_time_utc="2023-11-14 22:14",
             sim_tf="15m", current_stop=95.0, regime_at_entry="WEAK_BULL", conditions="", max_hold=None)
    r.update(kw)
    return r


class FromEvents(unittest.TestCase):
    def ctx(self, rows, tmp):
        log = pd.DataFrame(rows, columns=scanner.LOG_COLS)
        data = {("ETHUSDT", "15m"): candles(), ("ETHUSDT", "5m"): candles(seed=2)}
        old = scanner.REPORTS
        scanner.REPORTS = tmp                              # charts land in the temporary folder
        self.addCleanup(setattr, scanner, "REPORTS", old)
        return scanner.EmailContext(CFG, NOW, data, {}, {}, {"ETH": "GOOD"}, [], log, 0.5,
                                    RK.settings(CFG["risk"], []), 1000, scanner.TF_MS, 2)

    def ev(self, frm, to, stage="APPROVED", rid="ETH-15m-S-t"):
        return dict(id=rid, stage=stage, from_state=frm, to_state=to, strategy="S", version="1.0", tf="15m")

    def test_which_state_changes_email(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows = [log_row(state=P.TP1_HIT, current_stop=100.0),
                    log_row(id="c", state=P.CLOSED, status="SL", result_r=-1.03, close_reason="SL",
                            closed_time_utc="2023-11-15 01:14"),
                    log_row(id="p", stage="PAPER_TRADING", state=P.CLOSED, status="SL", result_r=-1.0,
                            close_reason="SL", closed_time_utc="2023-11-15 01:14"),
                    log_row(id="f", sim_tf="5m", entry=100.5, confirm_5m_utc="2023-11-14 22:24",
                            entry_time_utc="2023-11-14 22:24", smc_5m="")]
            m = self.ctx(rows, tmp)
            out = m.from_events([self.ev(P.ACTIVE, P.TP1_HIT), self.ev(P.TP1_HIT, P.CLOSED, rid="c"),
                                 self.ev(P.ACTIVE, P.CLOSED, "PAPER_TRADING", "p"),           # paper: a PAPER email
                                 self.ev(P.ACTIVE, P.CLOSED, "VALIDATION", "p"),              # validation: none
                                 self.ev(None, P.TRIGGERED), self.ev(P.TRIGGERED, P.ACTIVE),   # plain entry: no
                                 self.ev(P.AWAITING, P.TRIGGERED, rid="f"), self.ev(P.TRIGGERED, P.ACTIVE, rid="f"),
                                 self.ev(None, P.AWAITING), self.ev(P.AWAITING, P.EXPIRED)])     # cancelled
            self.assertEqual([(o["key"], o["subject"]) for o in out],
                             [("ETH-15m-S-t|TP1_HIT", "LIVE ✓ TP1 hit · ETH LONG +2.0R · move stop to entry"),
                              ("c|CLOSED", "LIVE ✕ Stop hit · ETH LONG −1.0R · trade closed"),
                              ("p|CLOSED", "PAPER ✕ Stop hit · ETH LONG −1.0R · #1 of 20"),
                              ("f|ENTRY", "LIVE ▲ LONG ETH 15M · Enter 99.40–101.60 · Stop 95.00"),
                              ("ETH-15m-S-t|EXPIRED", "LIVE ⊘ Cancelled · ETH LONG · no 5m confirmation")])
            self.assertIn("the 5m bar confirmed it", out[3]["text"])
            self.assertIn("1. Close 50% at 110.00", out[0]["text"])
            self.assertIsNone(out[4]["chart"])                                     # no chart for a cancelled signal
            self.assertEqual({o["thread"] for o in out}, {"ETH-15m-S-t", "c", "p", "f"})   # one thread per trade
            self.assertEqual([bool(o.get("reply")) for o in out], [True, True, True, False, True])
            self.assertEqual([o["paper_mail"] for o in out], [False, False, True, False, False])
            for o in out[:4]:
                with open(os.path.join(ROOT, o["chart"]) if not os.path.isabs(o["chart"]) else o["chart"], "rb") as f:
                    self.assertEqual(f.read(8), PNG)

    def test_paper_signal_from_a_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            sid = "ETH-15m-S-2023-11-14 22:14"
            m = self.ctx([log_row(id=sid, stage="PAPER_TRADING")], tmp)
            p = dict(coin="ETH", direction="LONG", market="spot", timeframe="15m", strategy="S", version="1.0",
                     stage="PAPER_TRADING", entry=100.0, entry_zone=[99.0, 101.0], stop=95.0,
                     targets=[dict(price=110.0, r=2.0, close_pct=50), dict(price=120.0, r=4.0, close_pct=50)],
                     position_qty=1.0, position_usdt=100.0, risk_usdt=5.0, risk_pct=0.5, size_capped=False,
                     context=dict(htf_trend="UP", regime="WEAK_BULL"), facts={}, session=None, conditions=[],
                     risk_blocks=[], no_trade=False, signal_time_utc="2023-11-14 22:14",
                     signal_ms=int(candles()["open_time"].iloc[-3]))
            e = m.entry_from_plan(p)
            self.assertEqual(e["subject"], "PAPER ▲ LONG ETH 15M · #1 of 20 · practice only")
            self.assertEqual((e["thread"], e["paper_mail"]), (sid, True))
            self.assertIn("PRACTICE ONLY – DO NOT USE REAL MONEY", e["text"])
            self.assertNotIn("LIVE", e["text"])
            m.board = {("S", "1.0", "15m"): dict(lab=True)}                                   # a lab card: no email
            self.assertEqual(m.from_events([self.ev(P.ACTIVE, P.TP1_HIT, "PAPER_TRADING", sid)]), [])

    def test_filled_and_warning_follow_ups(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows = [log_row(id="a", entry_time_utc="2026-09-23 23:07", signal_time_utc="2026-09-23 23:07"),
                    log_row(id="old", entry_time_utc="2026-09-20 10:00", signal_time_utc="2026-09-20 10:00"),
                    log_row(id="v", stage="VALIDATION", entry_time_utc="2026-09-23 23:07")]
            m = self.ctx(rows, tmp)
            book = P.build(m.logdf, NOW, {}, dict(day_r=-3, week_r=-6, heat=3))
            m.set_state(book, dict(upcoming_events=[dict(start_utc="2026-09-24 00:37", type="CPI",
                                                         name="US CPI (Aug data)")]), {})
            out = m.followups([])
            self.assertEqual([o["key"] for o in out], ["a|FILLED", "a|WARNING|2026-09-24 00:37", "old|WARNING|2026-09-24 00:37"])
            self.assertEqual(out[0]["subject"], "LIVE ● Filled · ETH LONG at 100.00 · stop active")
            self.assertEqual(out[1]["subject"], "LIVE ! Warning · ETH LONG open · US CPI in 30 min")
            self.assertIn("The agent does not move your stop", out[1]["text"])
            self.assertTrue(all(o["reply"] and o["thread"] for o in out))
            self.assertEqual(m.followups([dict(id="a")])[0]["key"], "a|WARNING|2026-09-24 00:37")   # moved this run

    def test_paper_complete_once_at_the_20th_closed_paper_signal(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows = [log_row(id=f"p{i}", stage="PAPER_TRADING", state=P.CLOSED, status="TP1", close_reason="TP2",
                            result_r=2.0 if i % 3 else -1.0, closed_time_utc=f"2026-09-{1 + i:02d} 10:00",
                            signal_time_utc=f"2026-09-{1 + i:02d} 08:00") for i in range(20)]
            m = self.ctx(rows, tmp)
            m.board = {("S", "1.0", "15m"): dict(status="PAPER_TRADING", validate_avg_r=0.9, trades=400, win_rate=0.5,
                                                  max_dd_r=12.0)}
            out = m.paper_complete([19], {})
            self.assertEqual(len(out), 1)
            self.assertEqual(out[0]["subject"], "PAPER ● 20 of 20 done · S 15M +19.0R · your decision")
            self.assertIn("Approve S v1.0 15M for real-money signals? Reply YES or NO.", out[0]["text"])
            m.logdf = m.logdf.iloc[:19]
            self.assertEqual(m.paper_complete([18], {}), [])                      # the 19th: not yet

    def test_reminder_when_approved_and_hourly(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = self.ctx([], tmp)
            board = [dict(strategy="S", version="1.0", tf="15m", status="APPROVED")]
            self.assertEqual([r["key"] for r in m.reminders(board, 60)], ["approved_while_hourly"])
            self.assertEqual(m.reminders(board, 15), [])
            self.assertEqual(m.reminders([dict(board[0], status="PAPER_TRADING")], 60), [])


class SameRun(unittest.TestCase):
    def test_signals_already_over_in_their_first_run_are_not_emailed(self):
        log = pd.DataFrame([log_row(id="a", state=P.ACTIVE), log_row(id="b", state=P.CLOSED),
                            log_row(id="c", state=P.TP1_HIT), log_row(id="d", state=P.AWAITING),
                            log_row(id="old", state=P.CLOSED)], columns=scanner.LOG_COLS)
        new = [dict(id=i) for i in ("a", "b", "c", "d")]
        self.assertEqual(scanner.not_actionable(new, log), {"b", "c"})


class Notify(unittest.TestCase):
    """notify.py in a temporary folder with a hand-made latest.json (DRY_RUN prints instead of sending)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        shutil.copy(os.path.join(ROOT, "notify.py"), self.tmp)
        shutil.copytree(os.path.join(ROOT, "engine"), os.path.join(self.tmp, "engine"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        os.makedirs(os.path.join(self.tmp, "reports", "charts"))
        with open(os.path.join(self.tmp, "reports", "charts", "a.png"), "wb") as f:
            f.write(PNG)

    def write(self, **kw):
        rep = dict(generated_utc="2026-09-24 00:07", signals=[], email_events=[], position_book=dict(awaiting=[]),
                   watching=[], reminders=[], daily=None)
        rep.update(kw)
        with open(os.path.join(self.tmp, "reports", "latest.json"), "w") as f:
            json.dump(rep, f)

    def run_notify(self, *args, dry=True):
        env = {k: v for k, v in os.environ.items() if k not in ("GMAIL_USER", "GMAIL_APP_PASSWORD", "DRY_RUN")}
        if dry:
            env["DRY_RUN"] = "1"
        p = subprocess.run([sys.executable, "notify.py", *args], cwd=self.tmp, env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        return p.stdout

    def emails(self, out):
        return re.findall(r"Subject: (.*)", out)

    def sig(self, coin):
        m = scanner.emx.live_entry(dict(card(coin=coin), chart_cid="chart"))
        return dict(coin=coin, timeframe="15m", strategy="S", signal_time_utc="2026-09-24 00:00",
                    email=dict(m, chart="reports/charts/a.png", thread=f"{coin}-t"))

    def test_one_email_per_signal_with_its_chart_and_only_once(self):
        self.write(signals=[self.sig("ETH"), self.sig("BTC")],
                   email_events=[dict(key="x|CLOSED", subject="✕ Stop hit · ETH LONG −1.0R · trade closed",
                                      text="t", html="<p>h</p>", chart=None)])
        out = self.run_notify()
        self.assertEqual(self.emails(out), ["LIVE ▲ LONG ETH 15M · Enter 99.00–101.00 · Stop 95.00",
                                            "LIVE ▲ LONG BTC 15M · Enter 99.00–101.00 · Stop 95.00",
                                            "✕ Stop hit · ETH LONG −1.0R · trade closed"])
        self.assertEqual(out.count("Inline image: a.png"), 2)
        first = out.split("--- DRY RUN (not sent) ---")[1]
        self.assertIn("[LIVE] ENTRY SIGNAL", first)
        self.assertIn("not financial advice", first.strip().splitlines()[-1])
        self.assertEqual(self.emails(self.run_notify()), [])                     # never twice

    def test_paper_flood_guard_three_an_hour_the_rest_in_the_next_briefing(self):
        ev = [dict(key=f"p{i}|PAPER", kind="ENTRY", subject=f"PAPER ▲ LONG ETH 15M · #{i} of 20 · practice only",
                   text="t", html="<p>h</p>", paper_mail=True, thread=f"p{i}") for i in range(5)]
        ev.append(dict(key="done", kind="PAPER_COMPLETE", subject="PAPER ● 20 of 20 done · S 15M +5.0R · your decision",
                       text="t", html="<p>h</p>", paper_mail=True))
        self.write(email_events=ev)
        out = self.run_notify()
        self.assertEqual(self.emails(out), [e["subject"] for e in ev[:3]] + [ev[5]["subject"]])   # complete: never held
        self.assertEqual(out.count("held back"), 2)
        with open(os.path.join(self.tmp, "reports", "paper_sent.json")) as f:
            held = json.load(f)["held"]
        self.assertEqual([h["key"] for h in held], ["p3|PAPER", "p4|PAPER"])
        self.assertEqual(self.emails(self.run_notify()), [])                     # held ones are not sent later

    def test_reminder_once_and_no_secrets_never_breaks(self):
        self.write(reminders=[dict(key="approved_while_hourly", subject="[SYSTEM] A strategy is APPROVED", lines=["x"])])
        self.assertIn("! A strategy is APPROVED · action needed once", self.emails(self.run_notify("system")))
        self.assertNotIn("! A strategy is APPROVED · action needed once", self.emails(self.run_notify("system")))
        self.write(signals=[self.sig("ETH")])
        out = self.run_notify(dry=False)                                         # no secrets, no dry run
        self.assertIn("not set up", out)
        with open(os.path.join(self.tmp, "reports", "notified.json")) as f:
            self.assertEqual(json.load(f), [])                                   # not marked as sent


class EndToEnd(unittest.TestCase):
    def test_offline_scan_writes_the_email_blocks(self):
        tmp, p = shared_offline_run()
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        with open(os.path.join(tmp, "reports", "latest.json")) as f:
            rep = json.load(f)
        for k in ("email_events", "daily", "reminders"):
            self.assertIn(k, rep)
        for k in ("daily_subject", "daily_lines", "email_settings"):                  # the old templates are gone
            self.assertNotIn(k, rep)
        self.assertEqual(len(rep["daily"]["matrix"]), len(rep["universe"]["signal"]))
        for e in rep["email_events"]:
            self.assertTrue(e["subject"].startswith(("LIVE ", "PAPER ")), e["subject"])


if __name__ == "__main__":
    unittest.main()
