"""The weekly review (Forward Test Program PR 3): live TEST / PAPER results after and before fees, by market type,
honest confidence, promotion candidates (the operator's tap), demotions by the paper record, ideas for new versions,
the 5m comparison, the system check - and the promotions in the research run, the hourly scan, the live watcher
(Telegram buttons, journal/decisions.csv) and the weekly email. Offline."""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import scanner as sc  # noqa: E402
from engine import emails as em  # noqa: E402
from engine import journal as jr  # noqa: E402
from engine import mailfacts as mf  # noqa: E402
from engine import signal_center as SCX  # noqa: E402
from engine import weekly_review as WR  # noqa: E402

NOW = dt.datetime(2026, 10, 25, 5, 0, tzinfo=dt.timezone.utc)          # a Sunday, after 04:00 UTC
S = WR.settings(None)
K1 = "P01-BREAKOUT-V2@1.0|1h"
K2 = "P07-SQUEEZE-RETEST-V1@1.0|4h"


def rows(key, coin, rs, stage="TEST", fees=0.1, market="DOWN (1D WEAK_BULL, 4H WEAK_BEAR, 1H STRONG_BEAR)",
         days_ago=2):
    sid, rest = key.split("@")
    ver, tf = rest.split("|")
    t = (NOW - dt.timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M")
    return [dict(id=f"{coin}-{tf}-{sid}-{i}-{stage}", coin=coin, tf=tf, strategy=sid, version=ver, stage=stage,
                 status="TP2" if r > 0 else "SL", result_r=r, fees_r=fees, closed_time_utc=t, market_type=market)
            for i, r in enumerate(rs)]


def log(*parts):
    return pd.DataFrame([r for p in parts for r in p])


def program():
    def cell(n, name, ver, coins):
        return dict(strategy=n, name=name, version=ver, coins=coins, tested_utc="2026-10-24 01:00")
    return {"cells": {K1: cell(1, "Breakout", "V2", {"BTC": dict(n=120, avg_r=0.3, win_rate=40), "ETH": dict(n=90, avg_r=0.1)}),
                      K2: cell(7, "Squeeze", "V1", {"SOL": dict(n=60, avg_r=-0.2)})}}


class Words(unittest.TestCase):
    def test_confidence_is_honest(self):
        self.assertIn("too early", WR.confidence(4, 0.9, 1.0))
        self.assertIn("not working", WR.confidence(30, -0.1, 1.0))
        self.assertIn("still uncertain", WR.confidence(12, 0.2, 1.5))
        self.assertIn("promising", WR.confidence(40, 0.3, 1.5))
        self.assertIn("strong so far", WR.confidence(100, 0.5, 1.5))
        self.assertEqual(WR.confidence(0, 0.0), "no live trade yet")


class Promotions(unittest.TestCase):
    def test_config_and_taps_newest_wins(self):
        cfg = [dict(strategy="P01-BREAKOUT-V2", version="1.0", tf="1h", coin="BTC", date="2026-10-18"), dict(bad=1)]
        taps = [dict(time_utc="2026-10-19 02:00", action="promote", key=K2, coin="SOL"),
                dict(time_utc="2026-10-20 02:00", action="unpromote", key=K1, coin="BTC")]
        p = WR.parse_promotions(cfg, taps)
        self.assertEqual([(x["key"], x["coin"], x["source"]) for x in p], [(K2, "SOL", "Telegram")])

    def test_limits_and_demotion(self):
        promos = [dict(key=K1, coin="BTC", date="1"), dict(key="P01-BREAKOUT-V1@1.0|4h", coin="BTC", date="2"),
                  dict(key=K2, coin="SOL", date="3"), dict(key=K1, coin="ETH", date="4")]
        nums = {"P01-BREAKOUT-V2@1.0": 1, "P01-BREAKOUT-V1@1.0": 1, "P07-SQUEEZE-RETEST-V1@1.0": 7}
        lg = log(rows(K2, "SOL", [-1.0] * 6 + [0.5] * 4, stage="PAPER_TRADING"))
        act, dem, ref = WR.active_promotions(promos, lg, nums, dict(S, paper_max=2))
        self.assertEqual(act, {K1: ["BTC", "ETH"]})
        self.assertEqual([d["key"] for d in dem], [K2])                    # paper record below 0R over 10
        self.assertIn("one per strategy per coin", ref[0]["why"])
        act2, _, ref2 = WR.active_promotions(promos[:1] + promos[3:], log(), nums, dict(S, paper_max=1))
        self.assertEqual(act2, {K1: ["BTC"]})
        self.assertIn("paper is full", ref2[0]["why"])

    def test_moves(self):
        st = {K1: "BACKTESTING", K2: "PAPER_TRADING", "X@1.0|1h": "PAPER_TRADING", "Y@1.0|1h": "PAPER_TRADING"}
        to, rel, via = WR.promotion_moves({K1: ["BTC"], "X@1.0|1h": ["BTC"]}, {K2, "Y@1.0|1h"}, st.get)
        self.assertEqual(to, [K1])
        self.assertEqual(via, [K1])                     # X reached PAPER through the pass bar: left alone
        self.assertEqual(rel, [K2, "Y@1.0|1h"])         # promotion ended
        self.assertEqual(WR.promotion_moves({K1: ["BTC"]}, set(), st.get, blocked={K1})[0], [])


class Review(unittest.TestCase):
    def build(self, lg, active=None, journal=None):
        return WR.build(NOW, lg, program(), {}, active or {}, [], [], journal,
                        [dict(date=(NOW - dt.timedelta(days=i)).strftime("%Y-%m-%d")) for i in range(7)],
                        "2026-10-25 05:00", S)

    def test_candidates_need_ten_live_trades_positive_after_fees_and_a_positive_backtest(self):
        lg = log(rows(K1, "BTC", [2.0, -1.0] * 6),                      # +0.5R over 12, backtest +0.3R
                 rows(K1, "ETH", [2.0, -1.0] * 4),                      # only 8
                 rows(K2, "SOL", [2.0, -1.0] * 6))                      # backtest negative on SOL
        rv = self.build(lg)
        self.assertEqual([(p["key"], p["coin"]) for p in rv["promote"]], [(K1, "BTC")])
        self.assertIn("12 live TEST setups, +0.50R a trade after fees", rv["promote"][0]["why"])
        row = next(r for r in rv["rows"] if r["coin"] == "BTC")
        self.assertEqual(row["gross"]["avg_r"], 0.6)                      # before fees = after + 0.1
        self.assertEqual(row["by_market"]["DOWN"]["n"], 12)
        self.assertEqual(rv["totals"]["TEST"]["n"], 32)
        self.assertTrue(rv["final"])
        md = WR.render(rv)
        for want in ("## System check", "## Promote to 🟡 PAPER (your tap)", "## With vs without the 5m check",
                     "| P01-BREAKOUT-V2 | 1h | BTC | TEST | 12 |"):
            self.assertIn(want, md)
        tg = WR.telegram(rv)
        self.assertIn("Ready for 🟡 PAPER", tg)
        self.assertIn("LIVE) signals still need 20 good paper signals", tg)

    def test_paper_full_and_one_per_strategy_per_coin(self):
        lg = log(rows(K1, "BTC", [2.0, -1.0] * 6))
        self.assertEqual(self.build(lg, active={"P01-BREAKOUT-V1@1.0|4h": ["BTC"]})["promote"], [])  # strategy 1 on BTC
        self.assertEqual(WR.build(NOW, lg, program(), {}, {f"X{i}@1.0|1h": ["BTC"] for i in range(5)}, [], [], None,
                                  [], None, S)["promote"], [])                                        # paper full

    def test_ideas_and_5m_and_system(self):
        lg = log(rows(K1, "BTC", [-1.0] * 6 + [0.5] * 4, market="CHOPPY (1D RANGE, 4H RANGE, 1H RANGE)", fees=0.6),
                 rows(K1, "ETH", [2.0, -1.0] * 5))
        journal = dict(last_entry_utc="2026-10-24 12:00", tests={"P01-BREAKOUT-V2": dict(n=12, avg_r=-0.4)})
        rv = self.build(lg, journal=journal)
        ideas = " ".join(rv["ideas"])
        self.assertIn("loses in CHOPPY markets", ideas)
        self.assertIn("positive before fees", ideas)
        fm = rv["five_min"]
        self.assertEqual((fm["confirmed_n"], fm["confirmed_r"]), (12, -0.4))
        self.assertIn("the 5m check made it worse", ideas)
        texts = [s["text"] for s in rv["system"]]
        self.assertTrue(any("nightly research ran on 7 of the last 7 days" in t for t in texts))
        self.assertTrue(all(s["ok"] is not False for s in rv["system"]))
        eight = [dict(date=(NOW - dt.timedelta(days=i)).strftime("%Y-%m-%d")) for i in range(8)]   # 8 dates on file
        rv3 = WR.build(NOW, log(), program(), {}, {}, [], [], dict(last_entry_utc=None), eight, "x", S)
        texts = [s["text"] for s in rv3["system"]]
        self.assertTrue(any("ran on 7 of the last 7 days" in t for t in texts))             # never "8 of 7"
        self.assertIn(dict(ok=None, text="live watcher journal: synced, no alert recorded yet"), rv3["system"])
        rv2 = WR.build(NOW, log(), None, {}, {}, [], [], None, [], None, S)
        self.assertIn(False, [s["ok"] for s in rv2["system"]])
        self.assertIsNone(rv2["five_min"]["confirmed_r"])
        self.assertIn("journal sync", rv2["five_min"]["note"])

    def test_email_part(self):
        rv = self.build(log(rows(K1, "BTC", [2.0, -1.0] * 6)))
        f = mf.program_facts(rv)
        self.assertEqual(f["system"], "all parts ran")
        self.assertTrue(f["promote"][0].startswith("P01-BREAKOUT-V2 1h on BTC"))
        self.assertIsNone(mf.program_facts(None))
        html = str(em.weekly(dict(program=f)))
        self.assertIn("Forward Test Program", html)
        self.assertIn("Promote (tap in Telegram)", html)


class PaperOnlyOnPromotedCoins(unittest.TestCase):
    def test_signal_center_and_scan(self):
        prog = {"cells": {K1: dict(strategy=1, name="B", version="V2", status="PAPER_TRADING",
                                   coins={"BTC": dict(n=50, avg_r=0.3), "ETH": dict(n=50, avg_r=0.2)})}}
        reg = {K1: dict(status="PAPER_TRADING")}
        self.assertEqual(SCX.test_list(prog, reg, SCX.settings(None)), {})            # PAPER through the pass bar
        t = SCX.test_list(prog, reg, SCX.settings(None), {K1: ["BTC"]})
        self.assertEqual(list(t[K1]), ["ETH"])                                         # still TEST on ETH
        self.assertEqual(SCX.scan_stage("PAPER_TRADING", t, K1, "BTC", {K1: ["BTC"]})[0], "PAPER_TRADING")
        self.assertEqual(SCX.scan_stage("PAPER_TRADING", t, K1, "ETH", {K1: ["BTC"]})[0], "TEST")
        self.assertEqual(SCX.scan_stage("PAPER_TRADING", {}, K1, "SOL", {K1: ["BTC"]}), (None, None))


class Journal(unittest.TestCase):
    def test_decisions_and_test_plan_results(self):
        d = jr.read_decisions("time_utc,week,action,key,coin\n2026-10-25 05:10,2026-W43,promote,X@1.0|1h,BTC\n"
                              ",,delete,Y,Z\n")
        self.assertEqual([x["key"] for x in d], ["X@1.0|1h"])
        text = ("\n".join([",".join(jr.COLS)] + [
            f"2026-10-2{i} 01:00,a{i},alert,TEST,BTC,LONG,1h,P01-BREAKOUT-V2,1.0,100,99,102,103,,," for i in range(3)] + [
            f"2026-10-2{i} 05:00,a{i},plan,TEST,BTC,LONG,1h,P01-BREAKOUT-V2,1.0,100,99,102,103,,102,{r}"
            for i, r in ((0, 2.0), (1, -1.0), (2, 2.0))]) + "\n")
        rv = jr.review(jr.read(text), int(NOW.timestamp() * 1000))
        self.assertEqual(rv["tests"], {"P01-BREAKOUT-V2": dict(n=3, avg_r=1.0)})


class Watcher(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        patches = [mock.patch.object(LW, "STATE", os.path.join(self.tmp.name, "state.json")),
                   mock.patch.object(LW, "JOURNAL", os.path.join(self.tmp.name, "journal", "my_trades.csv")),
                   mock.patch.object(LW, "DECISIONS", os.path.join(self.tmp.name, "journal", "decisions.csv")),
                   mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "1:x", "TELEGRAM_CHAT_ID": "42"}),
                   mock.patch.object(LW, "log")]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.now = int(NOW.timestamp() * 1000)
        self.w = LW.Watcher(LW.SyntheticSwap(), send=True, git=False, now_fn=lambda: self.now)
        self.w.dsync = LW.JournalSync(LW.DECISIONS, remote="journal/decisions.csv")
        self.sent, self.api = [], []
        for p in (mock.patch.object(LW, "telegram_message", side_effect=lambda text, *a, **k: self.sent.append(
                      (text, k.get("buttons"))) or (True, "", 77)),
                  mock.patch.object(LW, "tg_api", side_effect=lambda m, p, *a, **k: self.api.append((m, p)) or (True, {}))):
            p.start()
            self.addCleanup(p.stop)
        lg = log(rows(K1, "BTC", [2.0, -1.0] * 6))
        rv = WR.build(NOW, lg, program(), {}, {}, [], [], None, [], "x", S)
        rv["telegram"] = WR.telegram(rv)
        self.rv = rv

    def press(self, data):
        return dict(update_id=2, callback_query=dict(id="q", data=data, message=dict(chat=dict(id=42), message_id=77)))

    def test_weekly_message_once_and_a_tap_without_journal_sync(self):
        with mock.patch.object(LW.Watcher, "_json", side_effect=lambda rel: self.rv if "weekly" in rel else None):
            self.assertTrue(self.w.weekly_review(self.now))
            self.assertFalse(self.w.weekly_review(self.now))                 # once per week
        text, buttons = self.sent[-1]
        self.assertIn("Weekly review", text)
        self.assertEqual(buttons["inline_keyboard"][0][0]["callback_data"], "promo|0")
        with mock.patch.dict(os.environ, {"JOURNAL_GITHUB_TOKEN": ""}):
            self.w.on_update(self.press("promo|0"), self.now)
        self.assertIn("promotions:", self.sent[-1][0])
        self.assertIn("{strategy: P01-BREAKOUT-V2, version: \"1.0\", tf: 1h, coin: BTC, date: 2026-10-25}", self.sent[-1][0])
        with open(LW.DECISIONS) as f:
            self.assertEqual(f.read().splitlines()[1].split(",")[2:], ["promote", K1, "BTC"])
        self.w.on_update(self.press("promo|7"), self.now)
        self.assertIn("no longer current", self.api[-1][1]["text"])

    def test_a_tap_with_journal_sync_uploads_the_decision(self):
        self.w.state["review"] = dict(week="2026-W43", promote=[dict(key=K1, coin="BTC", name="P01 1h BTC")])
        with mock.patch.object(self.w.dsync, "push", return_value=(True, "1 rows")) as push:
            self.w.on_update(self.press("promo|0"), self.now)
        push.assert_called_once()
        self.assertIn("🟡 Promoted", self.sent[-1][0])
        self.assertIn("LIVE still needs", self.sent[-1][0])

    def test_review_command_and_paper_only_on_promoted_coins(self):
        with mock.patch.object(LW.Watcher, "_json", side_effect=lambda rel: self.rv if "weekly" in rel else None):
            self.assertIn("Weekly review", self.w.command("review", "", self.now))
        self.assertIn(("main", "reports/promotions_state.json"), LW.SYNC_FILES)
        self.assertIn(("main", "reports/weekly_review.json"), LW.SYNC_FILES)


class ResearchApplies(unittest.TestCase):
    """research.py --offline in a copy: a promotions line makes the program cell PAPER (only on its coin, never eligible
    for LIVE through the promotion), and its paper record below 0R demotes it the next night."""

    def test_promote_then_demote(self):
        from test_data_quality import run_copy
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        for name in ("research.py", "strategies_program.yaml"):
            shutil.copy(os.path.join(ROOT, name), tmp)
        with open(os.path.join(ROOT, "config.yaml")) as f:
            cfg = f.read().replace("promotions: []", "promotions:\n  - {strategy: P08-SESSION-BREAKOUT-V2, version: \"1.0\", "
                                   "tf: 15m, coin: BTC, date: 2026-10-18}")
        with open(os.path.join(tmp, "config.yaml"), "w") as f:
            f.write(cfg)
        run = lambda: subprocess.run([sys.executable, "research.py", "--offline", "--coins", "1", "--program", "8"],
                                     cwd=tmp, capture_output=True, text=True, timeout=900)
        run_copy(tmp, "research.py", "--offline", "--coins", "1", "--program", "none")   # the copy (+ a first run)
        with open(os.path.join(tmp, "config.yaml"), "w") as f:      # run_copy copied the real config over ours
            f.write(cfg)
        p = run()
        self.assertEqual(p.returncode, 0, p.stdout[-3000:] + p.stderr[-3000:])
        st = json.load(open(os.path.join(tmp, "reports", "promotions_state_offline.json")))
        self.assertEqual(st["active"], {"P08-SESSION-BREAKOUT-V2@1.0|15m": ["BTC"]})
        reg = pd.read_csv(os.path.join(tmp, "reports", "strategy_registry_offline.csv"), dtype={"version": str})
        cell = reg[(reg["id"] == "P08-SESSION-BREAKOUT-V2") & (reg["tf"] == "15m")].iloc[0]
        self.assertEqual(cell["status"], "PAPER_TRADING")
        out = json.load(open(os.path.join(tmp, "reports", "research_offline.json")))
        self.assertNotIn("P08-SESSION-BREAKOUT-V2@1.0|15m", out["approval"]["eligible"])
        # 10 paper signals below 0R on BTC -> demoted the next night
        sig = log(rows("P08-SESSION-BREAKOUT-V2@1.0|15m", "BTC", [-1.0] * 10, stage="PAPER_TRADING"))
        for col in sc.LOG_COLS:
            if col not in sig:
                sig[col] = np.nan
        sig[sc.LOG_COLS].to_csv(os.path.join(tmp, "reports", "signals_log.csv"), index=False)
        p = run()
        self.assertEqual(p.returncode, 0, p.stdout[-3000:] + p.stderr[-3000:])
        st = json.load(open(os.path.join(tmp, "reports", "promotions_state_offline.json")))
        self.assertEqual(st["active"], {})
        self.assertEqual([d["key"] for d in st["demoted"]], ["P08-SESSION-BREAKOUT-V2@1.0|15m"])
        reg = pd.read_csv(os.path.join(tmp, "reports", "strategy_registry_offline.csv"), dtype={"version": str})
        cell = reg[(reg["id"] == "P08-SESSION-BREAKOUT-V2") & (reg["tf"] == "15m")].iloc[0]
        self.assertNotEqual(cell["status"], "PAPER_TRADING")


if __name__ == "__main__":
    unittest.main()
