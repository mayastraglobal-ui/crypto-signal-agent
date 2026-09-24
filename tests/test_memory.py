"""Phase 13 tests: memory files (section 22), the record format, the engine's memory writers and the
append-only guard (section 17).

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
import research  # noqa: E402
import scanner  # noqa: E402
from engine import memory as M  # noqa: E402
from engine import regime as RG  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402

NOW = dt.datetime(2026, 9, 27, 0, 7, tzinfo=dt.timezone.utc)          # a Sunday
CFG = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))


class TmpMemory(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.old = (scanner.MEMORY, scanner.REPORTS)
        scanner.MEMORY, scanner.REPORTS = self.dir, self.dir
        self.addCleanup(lambda: (setattr(scanner, "MEMORY", self.old[0]), setattr(scanner, "REPORTS", self.old[1])))

    def text(self, name):
        with open(os.path.join(self.dir, name)) as f:
            return f.read()


class Records(unittest.TestCase):
    def test_every_field_in_order_and_round_trip(self):
        t = M.record("BTC LONG 1h", ["- detail"], timestamp="2026-09-24 10:00 UTC", source="engine", evidence="FACT: x",
                     confidence="measured", strategy="S v1.0", asset="BTC", timeframe="1h", regime="WEAK_BULL",
                     review="2026-10-01")
        line = t.splitlines()[2]
        self.assertEqual([p.split(":")[0] for p in line[2:].split(" · ")], M.FIELDS)
        r = M.parse(t)[0]
        self.assertEqual((r["title"], r["asset"], r["review"], r["evidence"]), ("BTC LONG 1h", "BTC", "2026-10-01",
                                                                                  "FACT: x"))

    def test_missing_fields_dash_and_bad_input(self):
        r = M.parse(M.record("t", timestamp="now", evidence="CLAIM"))[0]
        self.assertEqual((r["asset"], r["regime"], r["review"]), ("-", "-", "-"))
        with self.assertRaises(ValueError):
            M.record("t", colour="red")
        with self.assertRaises(ValueError):
            M.record("t", evidence="I think so")                 # not an evidence class
        r = M.parse(M.record("t", source="a · b", evidence="FACT"))[0]
        self.assertEqual(r["source"], "a, b")                    # the separator never breaks the line

    def test_ensure_status_and_due_reviews(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(sorted(M.ensure(d)), sorted(M.HEADERS))
            with open(os.path.join(d, "lessons.md"), "a") as f:
                f.write(M.record("old", timestamp="2026-08-01", evidence="FACT", review="2026-09-01"))
                f.write(M.record("new", timestamp="2026-09-20", evidence="FACT", review="2026-10-20"))
            self.assertEqual(M.ensure(d), [])                     # never overwritten
            st = M.status(d, NOW)
            self.assertEqual(st["missing"], [])
            self.assertEqual([(x["file"], x["title"]) for x in st["due"]], [("lessons.md", "old")])
            les = next(f for f in st["files"] if f["file"] == "lessons.md")
            self.assertEqual((les["records"], les["last"]), (2, "2026-09-20"))


class AppendOnly(unittest.TestCase):
    def test_rule(self):
        self.assertEqual(M.append_only_problems("a\nb\n", "a\nb\nc\n"), "")
        self.assertEqual(M.append_only_problems(None, "anything"), "")
        self.assertEqual(M.append_only_problems("a\nb\n", "a\nX\nc\n"), "line 2 was changed")
        self.assertEqual(M.append_only_problems("a\nb\nc\n", "a\nb\n"), "lines 3-3 were removed")
        self.assertEqual(M.append_only_problems("a\n", None), "the file was deleted")

    def test_guard_in_a_git_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copy(os.path.join(ROOT, "memory_guard.py"), tmp)
            shutil.copytree(os.path.join(ROOT, "engine"), os.path.join(tmp, "engine"),
                            ignore=shutil.ignore_patterns("__pycache__"))
            os.makedirs(os.path.join(tmp, "memory"))
            env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
                       GIT_COMMITTER_EMAIL="t@t")

            def sh(*a):
                return subprocess.run(list(a), cwd=tmp, env=env, capture_output=True, text=True)

            def write(name, text, mode="w"):
                with open(os.path.join(tmp, "memory", name), mode) as f:
                    f.write(text)
            sh("git", "init", "-q")
            write("failure_journal.md", "# J\n\n### loss 1\n")
            write("strategy_registry.csv", "id,status\nA,BACKTESTING\n")
            sh("git", "add", "-A")
            sh("git", "commit", "-q", "-m", "c")
            write("failure_journal.md", "### loss 2\n", "a")
            write("strategy_registry.csv", "id,status\nA,VALIDATION\n")        # allowed: updated in place
            write("lessons.md", "# L\n")                                         # new file: fine
            p = sh(sys.executable, "memory_guard.py")
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            write("failure_journal.md", "# J\n\n### loss 1 (edited)\n### loss 2\n")
            p = sh(sys.executable, "memory_guard.py")
            self.assertEqual(p.returncode, 1)
            self.assertIn("memory/failure_journal.md: line 3 was changed", p.stdout)
            os.remove(os.path.join(tmp, "memory", "failure_journal.md"))
            p = sh(sys.executable, "memory_guard.py")
            self.assertIn("memory/failure_journal.md: the file was deleted", p.stdout)

    def test_workflows_run_the_guard_before_committing(self):
        for wf in ("scan.yml", "research.yml"):
            with open(os.path.join(ROOT, ".github", "workflows", wf)) as f:
                s = f.read()
            self.assertLess(s.index("python memory_guard.py"), s.index("git add reports memory"), wf)

    def test_every_section_22_file_is_known(self):
        with open(os.path.join(ROOT, "AGENT_PROMPT.md")) as f:
            sec = f.read().split("## 22.")[1].split("## 23.")[0]
        listed = set(re.findall(r"`memory/([\w.]+)`", sec))
        with open(os.path.join(ROOT, "memory", "README.md")) as f:
            index = f.read()
        for name in listed:
            self.assertTrue(os.path.exists(os.path.join(ROOT, "memory", name)), name)
            self.assertIn(f"`{name}`", index, name)
        self.assertTrue(set(M.HEADERS) <= listed)


def loss_row(**kw):
    r = {c: np.nan for c in scanner.LOG_COLS}
    r.update(id="x", coin="SOL", direction="LONG", tf="1h", strategy="S", version="1.0", stage="PAPER_TRADING",
             signal_time_utc="2026-09-26 10:00", closed_time_utc="2026-09-26 14:00", status="SL", result_r=-1.04,
             mae_r=-1.0, mfe_r=0.4, regime_at_entry="RANGE", session="London", conditions="range_market",
             tags="stop_too_tight")
    r.update(kw)
    return r


class Writers(TmpMemory):
    def test_failure_journal_record(self):
        scanner.write_failure_journal(pd.DataFrame([loss_row()], columns=scanner.LOG_COLS), NOW, 7)
        r = M.parse(self.text("failure_journal.md"))[0]
        self.assertEqual(r["title"], "SOL LONG 1h S v1.0 - SL -1.04R")
        self.assertEqual((r["asset"], r["timeframe"], r["regime"], r["review"], r["strategy"]),
                         ("SOL", "1h", "RANGE", "2026-10-04", "S v1.0"))
        self.assertTrue(r["evidence"].startswith("FACT: PAPER_TRADING result -1.04R"))
        self.assertIn("what happened: stop_too_tight", self.text("failure_journal.md"))

    def test_execution_notes_only_on_start_end_and_fee_change(self):
        st = os.path.join(self.dir, "state.json")
        q = {("BTC", "1h"): dict(state="DEGRADED", problems=["2 gaps"]), ("ETH", "1h"): dict(state="GOOD")}
        iss, fees = scanner.execution_issues(q, {"ETH": dict(state="DEGRADED", deviation_pct=0.8)}, ["XRP"], CFG)
        self.assertEqual(sorted(iss), ["cross|ETH", "data|BTC|1h", "download|XRP"])
        w = scanner.write_execution_notes(iss, fees, NOW, st)
        self.assertEqual(len(w), 4)                                   # 3 starts + the fees in use
        self.assertEqual(scanner.write_execution_notes(iss, fees, NOW, st), [])   # same state: nothing
        later = NOW + dt.timedelta(hours=3)
        iss2 = {k: v for k, v in iss.items() if k != "data|BTC|1h"}
        w = scanner.write_execution_notes(iss2, fees.replace("0.1", "0.2"), later, st)
        titles = [M.parse(t)[0]["title"] for t in w]
        self.assertEqual(titles, ["END BTC 1h data: 2 gaps", "Fee settings CHANGED"])
        self.assertIn(f"first seen {NOW.strftime('%Y-%m-%d %H:%M')} UTC", w[0])
        self.assertEqual(len(M.parse(self.text("execution_notes.md"))), 6)

    def test_coin_notes_weekly_on_sunday_only(self):
        st = os.path.join(self.dir, "cn.json")
        calls = []

        def facts():
            calls.append(1)
            return {"BTC": ["- fact"]}
        self.assertFalse(scanner.write_coin_notes(["BTC"], facts, NOW - dt.timedelta(days=1), st))   # Saturday
        self.assertEqual(calls, [])                                   # facts not even computed
        self.assertTrue(scanner.write_coin_notes(["BTC"], facts, NOW, st))
        self.assertFalse(scanner.write_coin_notes(["BTC"], facts, NOW + dt.timedelta(hours=1), st))  # same Sunday
        self.assertTrue(scanner.write_coin_notes(["BTC"], facts, NOW + dt.timedelta(days=7), st))
        recs = M.parse(self.text("coin_notes.md"))
        self.assertEqual([r["title"] for r in recs], ["BTC - weekly facts 2026-09-27", "BTC - weekly facts 2026-10-04"])

    def test_coin_facts_are_measured(self):
        n = 120
        d = pd.DataFrame(dict(high=np.full(n, 102.0), low=np.full(n, 98.0), close=np.full(n, 100.0)))
        cells = {"S@1.0|1h": dict(evidence=dict(by_coin={"BTC": dict(n=12, avg_r=0.2)})),
                 "T@1.0|4h": dict(evidence=dict(by_coin={"BTC": dict(n=3, avg_r=0.9)})),       # too few
                 "U@1.0|1h": dict(evidence=dict(by_coin={"BTC": dict(n=40, avg_r=-0.1)}))}
        f = scanner.coin_facts("BTC", d, (np.arange(n), np.array(["RANGE"] * 60 + ["WEAK_BULL"] * 60)), "BTC+ETH",
                               2e9, cells, 5, NOW)
        text = "\n".join(f)
        self.assertIn("median 4.0%", text)
        self.assertIn("WEAK_BULL 67%, RANGE 33%", text)               # last 90 days, most frequent first
        self.assertIn("BTC+ETH", text)
        self.assertIn("S@1.0 1h (12 trades, +0.20R)", text)
        self.assertNotIn("T@1.0", text)
        self.assertNotIn("U@1.0", text)


class Research(TmpMemory):
    def setUp(self):
        super().setUp()
        self.oldr = research.sc.MEMORY
        research.sc.MEMORY = self.dir

    def tearDown(self):
        research.sc.MEMORY = self.oldr

    def test_sources_backfill_once_and_no_invented_urls(self):
        with open(os.path.join(ROOT, "strategies.yaml")) as f:
            ok, _, _ = SP.load(yaml.safe_load(f), RG.LABELS, scanner.TF_ORDER)
        research.write_sources(ok, NOW)
        research.write_sources(ok, NOW + dt.timedelta(days=1))             # nothing new -> nothing added
        recs = M.parse(self.text("research_sources.md"))
        self.assertEqual(len(recs), len(ok))
        by = {r["title"].split(" ")[0]: r for r in recs}
        self.assertTrue(by["S6-OB-FVG@1.0"]["evidence"].startswith("CLAIM"))
        self.assertTrue(by["S6-OB-FVG-5M@1.0"]["evidence"].startswith("CLAIM"))
        self.assertTrue(by["liquidity_sweep_reversal@1.0"]["evidence"].startswith("HYPOTHESIS"))
        self.assertEqual(sum(r["evidence"].startswith("CLAIM") for r in recs), 8)       # S5-S8 + their -5M
        self.assertTrue(by["S6-OB-FVG-noSMC@1.0"]["evidence"].startswith("HYPOTHESIS: control twin"))
        self.assertTrue(by["trend_pullback@1.0"]["evidence"].startswith("HYPOTHESIS"))
        self.assertEqual(by["S6-OB-FVG@1.0"]["review"], "2026-12-26")
        self.assertNotIn("http", self.text("research_sources.md"))
        self.assertEqual(self.text("research_sources.md").count("URL: none recorded"), len(ok))
        card = dict(ok[0], id="NEW", source_url="https://example.org/paper")
        research.write_sources([card], NOW)
        self.assertIn("URL: https://example.org/paper", self.text("research_sources.md"))

    def test_missed_move_record(self):
        research.write_missed([dict(coin="SOL", direction="up", pct=9.1, size_atr=6.2, start_utc="a", end_utc="b",
                                    signal_coin=True, verdict="identifiable: blocked by the regime gate",
                                    findings={"S v1.0 1h": "blocked (regime)"}, strategies_checked=12,
                                    regime="RANGE")], NOW, dict(strong_move_bars=12), 7)
        r = M.parse(self.text("missed_trades.md"))[0]
        self.assertEqual((r["asset"], r["regime"], r["timeframe"], r["review"]), ("SOL", "RANGE", "1h", "2026-10-04"))
        self.assertIn("- S v1.0 1h: blocked (regime)", self.text("missed_trades.md"))


if __name__ == "__main__":
    unittest.main()
