"""Phase 12 tests: [ENTRY] / [EXIT] / [DAILY] / [WATCH] / [SYSTEM] emails (section 20) and chart images.

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
    def test_entry_subject_and_body(self):
        m = B.entry_email(card())
        self.assertEqual(m["subject"], "[ENTRY] LONG ETH/USDT | 15m | S6-OB-FVG v1.0 | R:R 2.4")
        text = "\n".join(m["lines"])
        for part in ("2026-09-24 00:07 UTC / 2026-09-24 08:07 Beijing · data GOOD",
                     "Regime: 1W WEAK_BULL · 1D STRONG_BULL · 4H WEAK_BULL · 1H RANGE · 15M structure up",
                     "Entry zone : 99.0000 - 101.0000", "Stop-loss  : 95.0000  (5.00% away)",
                     "TP1        : 112.0000  (2.4R) -> close 50%, move stop to entry (breakeven)",
                     "TP2        : 120.0000  (4.0R) -> close the rest", "R:R to TP1 : 2.40",
                     "= 5.00 USDT risk (0.5% of the account)", "Expires    : 2026-09-24 00:22 UTC",
                     "Why this signal exists:", "What cancels it:", "Evidence:"):
            self.assertIn(part, text)
        self.assertNotIn("FUTURES ONLY", text)
        self.assertNotIn("5m confirm", text)

    def test_short_is_futures_only_and_5m_bar_is_named(self):
        m = B.entry_email(card(direction="SHORT", market="futures only", stop=105.0,
                               targets=[dict(price=88.0, r=2.4, close_pct=100)],
                               confirm_5m="2026-09-24 00:04", smc_5m="5m engulfing bar",
                               size=dict(qty=1.0, usdt=100.0, risk_usdt=5.0, risk_pct=0.5, capped=True)))
        text = "\n".join(m["lines"])
        self.assertTrue(m["subject"].startswith("[ENTRY] SHORT ETH/USDT | 15m |"))
        self.assertIn("FUTURES ONLY", text)
        self.assertIn("5m confirm : bar closed 2026-09-24 00:04 UTC (5m engulfing bar)", text)
        self.assertIn("more would need over 3x leverage", text)

    def test_exit_subjects(self):
        base = dict(coin="ETH", quote="USDT", direction="LONG", tf="15m", strategy="S", version="1.0", stage="APPROVED",
                    utc="u", beijing="b", entry=100.0, next_action="n")
        self.assertEqual(B.exit_email(dict(base, kind="TP1_HIT", close_reason=None, result_r=0))["subject"],
                         "[EXIT] ETH/USDT LONG | TP1")
        for reason, word in (("SL", "SL"), ("BE", "BE (rest stopped at entry)"), ("TIME", "TIME"),
                             ("EXIT_RULE", "EXIT_RULE"), ("TP2", "TP2")):
            m = B.exit_email(dict(base, kind="CLOSED", close_reason=reason, result_r=-1.02))
            self.assertEqual(m["subject"], f"[EXIT] ETH/USDT LONG | {word}")
            self.assertIn("result -1.02R after costs", "\n".join(m["lines"]))

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

    def test_evidence_and_daily(self):
        ev = B.evidence(dict(trades=84, avg_r=0.225, profit_factor=1.4, walk_forward="3/5", layer_a_trades=9,
                             layer_a_avg_r=0.1), dict(n=0, avg_r=0), dict(n=3, avg_r=-0.5))
        self.assertEqual(ev[0], "Layer B (all history): 84 trades, +0.23R avg, PF 1.40")
        self.assertEqual(ev[1], "Layer C (walk-forward): 3/5 windows profitable")
        self.assertEqual(ev[3:], ["Paper record: none yet", "Live record: 3 trades, -0.50R avg"])
        self.assertEqual(B.evidence(None, None, None)[1], "Layer C (walk-forward): not run yet")
        d = B.daily_email(dict(date="2026-09-24", utc="u", beijing="b", btc={"1d": "UP", "4h": "DOWN"}, fear_greed=None,
                               data_state="GOOD", signals=0,
                               matrix=[dict(coin="BTC", price=65000.0, vol_24h_m=1234.0,
                                            regimes=["WEAK_BULL", "RANGE", "RANGE", "RANGE"], mom_30m="+0.4% ROC",
                                            setup_15m="WATCH", trigger_5m="-")],
                               health=[], events=[], calendar_warning="calendar not maintained"))
        self.assertEqual(d["subject"], "[DAILY] Crypto signal report 2026-09-24 - 0 signal(s), BTC 1D UP")
        text = "\n".join(d["lines"])
        for part in ("BTC   |   65,000.00 |        1234 | WEAK_BULL / RANGE / RANGE / RANGE", "no status changes",
                     "none listed", "! calendar not maintained"):
            self.assertIn(part, text)


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
        return dict(id=rid, stage=stage, from_state=frm, to_state=to)

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
                                 self.ev(P.ACTIVE, P.CLOSED, "PAPER_TRADING", "p"),           # paper: no email
                                 self.ev(None, P.TRIGGERED), self.ev(P.TRIGGERED, P.ACTIVE),   # plain entry: no
                                 self.ev(P.AWAITING, P.TRIGGERED, rid="f"), self.ev(P.TRIGGERED, P.ACTIVE, rid="f"),
                                 self.ev(None, P.AWAITING), self.ev(P.AWAITING, P.EXPIRED)])     # report only
            self.assertEqual([(o["key"], o["subject"]) for o in out],
                             [("ETH-15m-S-t|TP1_HIT", "[EXIT] ETH/USDT LONG | TP1"),
                              ("c|CLOSED", "[EXIT] ETH/USDT LONG | SL"),
                              ("f|ENTRY", "[ENTRY] LONG ETH/USDT | 15m | S v1.0 | R:R 1.7")])
            self.assertIn("5m confirm : bar closed 2023-11-14 22:24 UTC", "\n".join(out[2]["lines"]))
            for o in out:
                with open(os.path.join(ROOT, o["chart"]) if not os.path.isabs(o["chart"]) else o["chart"], "rb") as f:
                    self.assertEqual(f.read(8), PNG)

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
        os.makedirs(os.path.join(self.tmp, "reports", "charts"))
        with open(os.path.join(self.tmp, "reports", "charts", "a.png"), "wb") as f:
            f.write(PNG)

    def write(self, **kw):
        rep = dict(generated_utc="2026-09-24 00:07", position_book_text=["POSITION BOOK — test", "No open or pending positions."],
                   signals=[], email_events=[], position_book=dict(awaiting=[]), watching=[], reminders=[],
                   email_settings=dict(email_watching=False), daily=None)
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
        return dict(coin=coin, timeframe="15m", strategy="S", signal_time_utc="2026-09-24 00:00",
                    email=dict(subject=f"[ENTRY] LONG {coin}/USDT | 15m | S v1.0 | R:R 2.0", lines=["body"],
                               chart="reports/charts/a.png"))

    def test_one_email_per_signal_book_first_footer_last_and_only_once(self):
        self.write(signals=[self.sig("ETH"), self.sig("BTC")],
                   email_events=[dict(key="x|CLOSED", subject="[EXIT] ETH/USDT LONG | SL", lines=["b"], chart=None)])
        out = self.run_notify()
        self.assertEqual(self.emails(out), ["[ENTRY] LONG ETH/USDT | 15m | S v1.0 | R:R 2.0",
                                            "[ENTRY] LONG BTC/USDT | 15m | S v1.0 | R:R 2.0", "[EXIT] ETH/USDT LONG | SL"])
        self.assertEqual(out.count("Attachment: a.png"), 2)
        first = out.split("--- DRY RUN (not sent) ---")[1]
        body = first.split("\n\n", 1)[1].strip().splitlines()
        self.assertEqual(body[0], "POSITION BOOK — test")
        self.assertEqual(body[-1], "Research signal. Not financial advice.")
        self.assertEqual(self.emails(self.run_notify()), [])                     # never twice

    def test_daily_once_per_day_and_only_in_the_morning(self):
        daily = dict(date="2026-09-24", utc="2026-09-24 00:07")
        self.write(daily=daily, daily_subject="[DAILY] Crypto signal report 2026-09-24", daily_lines=["x"])
        self.assertEqual(self.emails(self.run_notify("daily")), ["[DAILY] Crypto signal report 2026-09-24"])
        self.assertEqual(self.emails(self.run_notify("daily")), [])
        self.write(daily=dict(date="2026-09-25", utc="2026-09-25 13:07"), daily_subject="[DAILY] d", daily_lines=[])
        self.assertEqual(self.emails(self.run_notify("daily")), [])               # mid-day: skip
        self.write(daily=dict(date="2026-09-25", utc="2026-09-25 05:07"), daily_subject="[DAILY] d", daily_lines=[])
        self.assertEqual(self.emails(self.run_notify("daily")), ["[DAILY] d"])     # 00:07 run failed: 05:07 sends

    def test_watch_only_when_enabled(self):
        w = [dict(coin="ETH", tf="15m", strategy="S", direction="LONG", stage="APPROVED", state="SETUP_FORMING",
                  missing="smc_choch_up"),
             dict(coin="BTC", tf="15m", strategy="S", direction="LONG", stage="VALIDATION", state="SETUP_FORMING",
                  missing="x")]
        self.write(watching=w)
        self.assertEqual(self.emails(self.run_notify()), [])
        self.write(watching=w, email_settings=dict(email_watching=True))
        out = self.run_notify()
        self.assertEqual(self.emails(out), ["[WATCH] 1 setup(s) forming - no entry yet"])
        self.assertNotIn("BTC", out.split("Subject:")[1])
        self.assertEqual(self.emails(self.run_notify()), [])

    def test_reminder_once_and_no_secrets_never_breaks(self):
        self.write(reminders=[dict(key="approved_while_hourly", subject="[SYSTEM] A strategy is APPROVED", lines=["x"])])
        self.assertIn("[SYSTEM] A strategy is APPROVED", self.emails(self.run_notify("system")))
        self.assertNotIn("[SYSTEM] A strategy is APPROVED", self.emails(self.run_notify("system")))
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
        for k in ("email_events", "daily", "daily_subject", "daily_lines", "reminders", "email_settings"):
            self.assertIn(k, rep)
        self.assertTrue(rep["daily_subject"].startswith("[DAILY] Crypto signal report"))
        self.assertEqual(len(rep["daily"]["matrix"]), len(rep["universe"]["signal"]))
        self.assertFalse(rep["email_settings"]["email_watching"])


if __name__ == "__main__":
    unittest.main()
