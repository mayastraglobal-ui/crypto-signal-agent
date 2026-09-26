"""Phase 14 tests: the Brain guard (Claude's task work -> main), approval packs and the operator's yes,
the weekly email, Claude's summaries in the engine's emails, and the fact sheet.

Run:  python -m unittest discover -s tests -v
"""
import datetime as dt
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import brain_pack  # noqa: E402
import notify  # noqa: E402
import research  # noqa: E402
import scanner  # noqa: E402
from engine import approval as AP  # noqa: E402
from engine import brain as B  # noqa: E402
from engine import briefs  # noqa: E402
from engine import digest as D  # noqa: E402
from engine import research as RS  # noqa: E402

UTC = dt.timezone.utc
REC = ("\n### {title}\n- timestamp: 2026-09-25 15:30 UTC · source: Claude daily review · evidence: {ev} · "
       "confidence: medium · strategy: S6-OB-FVG@1.0 · asset: BTC · timeframe: 15m · regime: RANGE · review: {rv}\n"
       "  details\n")


DEBATE = ("## Bull vs bear\n- Bull case: 1D WEAK_BULL (ADX 44)\n- Bear case: 1H RANGE\n"
          "- Risk manager: no veto (heat 0 of 3)\n")          # Phase 18 A: every briefing has it
EMAIL = {"briefings": "## Email summary\n- headline: Quiet.\n- sub: Nothing moves.\n- do: Wait.\n- dont: Don't chase.\n",
         "daily": "## Email summary\n- lesson: Small samples mislead.\n- tomorrow: Watch PCE.\n",
         "weekly": "## Email summary\n- headline: Quiet week.\n- sub: No decision.\n- next: Test the queue.\n"
                   "- improvement: Fewer cards.\n"}      # the email redesign: every Claude report has its block


def lab_header(text):
    """The comment header of strategies_lab.yaml without its cards (tests must not depend on today's cards)."""
    out = []
    for line in text.splitlines(keepends=True):
        if line.startswith("- "):
            break
        out.append(line)
    return "".join(out)


def email_block(path):
    return next(v for k, v in EMAIL.items() if f"/{k}/" in path)


def rec(title="A lesson", ev="BACKTEST_EVIDENCE: 3 tests, 412 trades", rv="2026-10-25"):
    return REC.format(title=title, ev=ev, rv=rv)


BASE = "# Lessons\n\nheader\n"


def change(path, status="M", base=BASE, new=None):
    return dict(path=path, status=status, base=base, new=new)


class Guard(unittest.TestCase):
    def ok(self, changes, main=None):
        applies, probs, skipped = B.review(changes, main or {c["path"]: c["base"] for c in changes})
        self.assertEqual(probs, [])
        return applies, skipped

    def refused(self, changes, main=None, needle=""):
        applies, probs, _ = B.review(changes, main or {c["path"]: c["base"] for c in changes})
        self.assertTrue(probs, "expected a refusal")
        self.assertEqual(applies, [], "a refused push applies nothing")
        self.assertIn(needle, "\n".join(probs))
        return probs

    def test_new_report_files_only_with_the_expected_names(self):
        for p in ["reports/claude/briefings/2026-09-25-0820.md", "reports/claude/briefings/2026-09-25-1420.md",
                  "reports/claude/briefings/2026-09-25-2120.md", "reports/claude/daily/2026-09-25.md",
                  "reports/claude/weekly/2026-09-27.md"]:
            applies, _ = self.ok([change(p, "A", None, "# Title\n## Summary\nfine\n" + email_block(p) + DEBATE)],
                                 {p: None})
            self.assertEqual(applies[0]["kind"], "new")
        for p in ["reports/claude/briefings/2026-09-25-0900.md", "reports/claude/daily/today.md",
                  "reports/claude/other/2026-09-25.md", "reports/latest.md", "reports/claude/daily/2026-09-25.txt"]:
            self.refused([change(p, "A", None, "# x\n")], {p: None}, "not allowed")

    def test_changing_a_report_file_or_creating_a_knowledge_file_is_refused(self):
        p = "reports/claude/daily/2026-09-25.md"
        self.refused([change(p, "M", "# old\n", "# old\nmore\n")], {p: "# old\n"})
        self.refused([change("memory/lessons.md", "A", None, rec())], {"memory/lessons.md": None}, "created")

    def test_existing_file_is_never_overwritten_but_a_rerun_is_skipped(self):
        p = "reports/claude/daily/2026-09-25.md"
        self.refused([change(p, "A", None, "# new\n")], {p: "# old\n"}, "never overwritten")
        applies, skipped = self.ok([change(p, "A", None, "# same\n")], {p: "# same\n"})
        self.assertEqual((applies, skipped), ([], [p]))

    def test_record_appended_to_a_knowledge_file(self):
        applies, _ = self.ok([change("memory/lessons.md", new=BASE + rec())])
        self.assertEqual(applies, [dict(path="memory/lessons.md", kind="append", text=rec())])

    def test_append_goes_onto_the_newest_main(self):
        grown = BASE + "\n### engine line\n- timestamp: x\n"            # main grew after the task branched off
        applies, _ = self.ok([change("memory/failure_journal.md", new=BASE + rec(ev="HYPOTHESIS: root cause"))],
                             {"memory/failure_journal.md": grown})
        out = B.apply_text(grown, applies[0])
        self.assertTrue(out.startswith(grown) and out.endswith(rec(ev="HYPOTHESIS: root cause")))
        self.assertEqual(B.apply_text("no newline", dict(kind="append", text="x\n")), "no newline\nx\n")

    def test_editing_or_deleting_an_earlier_line_is_refused(self):
        self.refused([change("memory/lessons.md", new="# Lessons\n\nCHANGED\n" + rec())], needle="only grow")
        self.refused([change("memory/lessons.md", new="# Lessons\n")], needle="only grow")
        self.refused([change("memory/lessons.md", "D", new=None)], needle="deleted")

    def test_lessons_need_strong_evidence_with_counts(self):
        self.refused([change("memory/lessons.md", new=BASE + rec(ev="HYPOTHESIS: maybe"))], needle="not enough")
        self.refused([change("memory/lessons.md", new=BASE + rec(ev="CLAIM: a blog says so"))], needle="not enough")
        self.refused([change("memory/lessons.md", new=BASE + rec(ev="BACKTEST_EVIDENCE: many tests"))],
                     needle="counts")
        self.ok([change("memory/failure_journal.md", base=BASE, new=BASE + rec(ev="HYPOTHESIS: a guess"))])

    def test_record_format_is_enforced(self):
        self.refused([change("memory/coin_notes.md", new=BASE + "just a note\n")], needle="outside a record")
        self.refused([change("memory/coin_notes.md", new=BASE + "\n### t\nno field line\n")], needle="field line")
        self.refused([change("memory/coin_notes.md", new=BASE + rec(ev="GUESS: x"))], needle="class")
        self.refused([change("memory/coin_notes.md", new=BASE + rec(rv="next month"))], needle="review must be")
        bad = rec().replace(" · regime: RANGE", "")
        self.refused([change("memory/coin_notes.md", new=BASE + bad)], needle="missing")

    def test_code_config_strategies_and_workflows_are_refused(self):
        for p in ["scanner.py", "config.yaml", "engine/risk.py", ".github/workflows/scan.yml", "brain_guard.py",
                  "reports/signals_log.csv", "memory/strategy_registry.csv", "memory/changelog.md",
                  "memory/strategy_lifecycle.md", "tasks/COMMON.md"]:
            self.refused([change(p, "M", "a\n", "a\nb\n")], {p: "a\n"}, "not allowed")
        self.refused([change("strategies.yaml", "M", "a\n", "a\nb\n")], {"strategies.yaml": "a\n"}, "pull request")

    def test_one_problem_refuses_the_whole_push(self):
        good = change("reports/claude/daily/2026-09-25.md", "A", None, "# ok\n" + EMAIL["daily"])
        probs = self.refused([good, change("config.yaml", "M", "a\n", "b\n")],
                             {"reports/claude/daily/2026-09-25.md": None, "config.yaml": "a\n"}, "config.yaml")
        self.assertEqual(len(probs), 1)

    def test_too_many_files(self):
        many = [change(f"reports/claude/daily/2026-09-{i:02d}.md", "A", None, "# x\n") for i in range(1, 14)]
        self.refused(many, {c["path"]: None for c in many}, "at most")

    def test_honesty_phrases(self):
        bad = ["This setup is guaranteed to work", "a risk-free trade", "you can't lose here",
               "a high-probability setup", "a 70% chance this trade wins", "70 % probability of profit",
               "the probability of winning is good", "easy money today", "Guarantees profit"]
        fine = ["Past results are no guarantee of future results", "profit is not guaranteed",
                "this doesn't guarantee anything", "markets price a 70% chance of a Fed cut in October",
                "backtest win rate 45% over 120 trades", "the probability of a rate cut rose (CME FedWatch)"]
        for t in bad:
            self.assertTrue(B.lint(t), t)
        for t in fine:
            self.assertEqual(B.lint(t), [], t)
        p = "reports/claude/briefings/2026-09-25-0820.md"
        self.refused([change(p, "A", None, "# x\nA guaranteed win today\n")], {p: None}, "profit promise")

    def test_empty_addition_is_ignored(self):
        applies, _ = self.ok([change("memory/lessons.md", new=BASE + "\n")])
        self.assertEqual(applies, [])


def read(path):
    with open(path) as f:
        return f.read()


def dump(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f)


def git(cwd, *args):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr)
    return p.stdout.strip()


class GuardOnGit(unittest.TestCase):
    """brain_guard.py end to end on a throw-away repository: branch -> guard -> newest main."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.origin = os.path.join(self.tmp, "origin.git")
        git(self.tmp, "init", "-q", "--bare", "-b", "main", self.origin)
        self.main = os.path.join(self.tmp, "main")
        git(self.tmp, "clone", "-q", self.origin, self.main)
        for c in (["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            git(self.main, *c)
        shutil.copytree(os.path.join(ROOT, "engine"), os.path.join(self.main, "engine"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        os.makedirs(os.path.join(self.main, "memory"))
        for f in ["brain_guard.py", "memory_guard.py", "append_merge.py", ".gitattributes"]:
            shutil.copy(os.path.join(ROOT, f), os.path.join(self.main, f))
        self.write(self.main, "memory/lessons.md", BASE)
        self.write(self.main, "memory/failure_journal.md", BASE)
        git(self.main, "add", "-A")
        git(self.main, "commit", "-qm", "start")
        git(self.main, "push", "-q", "origin", "main")
        self.task = os.path.join(self.tmp, "task")
        git(self.tmp, "clone", "-q", self.origin, self.task)
        for c in (["config", "user.email", "c@c"], ["config", "user.name", "claude"]):
            git(self.task, *c)

    def write(self, repo, path, text, mode="w"):
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, mode) as f:
            f.write(text)

    def push_task(self, branch, files, appends):
        """Two commits (files, then appends): the guard must see everything since the branch left main."""
        git(self.task, "fetch", "-q", "origin", "main")
        git(self.task, "checkout", "-q", "-B", branch, "origin/main")
        for p, t in files.items():
            self.write(self.task, p, t)
        git(self.task, "add", "-A")
        git(self.task, "commit", "-qm", f"task {branch} files", "--allow-empty")
        for p, t in appends.items():
            self.write(self.task, p, t, "a")
        git(self.task, "add", "-A")
        git(self.task, "commit", "-qm", f"task {branch}", "--allow-empty")
        git(self.task, "push", "-q", "-f", "origin", branch)

    def guard(self):
        out = os.path.join(self.tmp, "result.json")
        p = subprocess.run([sys.executable, "brain_guard.py", "--out", out], cwd=self.main, capture_output=True,
                           text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(read(out))

    def test_applies_onto_newest_main_once_and_refuses_bad_pushes(self):
        self.push_task("claude/brain-daily", {"reports/claude/daily/2026-09-25.md": "# Daily\n## Summary\nok\n"
                                                                                    + EMAIL["daily"]},
                       {"memory/lessons.md": rec()})
        # meanwhile the engine appended to the failure journal on main (the task branch does not have it)
        self.write(self.main, "memory/failure_journal.md", rec("engine loss", ev="FACT: -1R"), "a")
        git(self.main, "commit", "-qam", "scan")
        res = self.guard()
        self.assertEqual([r["status"] for r in res], ["applied"])
        self.assertEqual(sorted(res[0]["applied"]), ["memory/lessons.md", "reports/claude/daily/2026-09-25.md"])
        self.assertEqual(read(os.path.join(self.main, "memory/lessons.md")), BASE + rec())
        self.assertIn("engine loss", read(os.path.join(self.main, "memory/failure_journal.md")))
        p = subprocess.run([sys.executable, "memory_guard.py"], cwd=self.main, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertEqual(self.guard(), [], "the same push is never applied twice")
        # a push that also touches code: refused as a whole, main unchanged
        self.push_task("claude/brain-weekly", {"reports/claude/weekly/2026-09-27.md": "# W\n",
                                               "engine/brain.py": "# gone\n"}, {})
        before = read(os.path.join(self.main, "engine/brain.py"))
        res = self.guard()
        self.assertEqual(res[0]["status"], "rejected")
        self.assertFalse(os.path.exists(os.path.join(self.main, "reports/claude/weekly/2026-09-27.md")))
        self.assertEqual(read(os.path.join(self.main, "engine/brain.py")), before)
        state = json.loads(read(os.path.join(self.main, "reports/claude/state.json")))
        self.assertEqual(state["claude/brain-weekly"]["status"], "rejected")

    def test_append_merge_keeps_both_sides_of_append_only_files(self):
        """.gitattributes + the `append` driver the workflows register: the hourly scan and the Brain workflow can
        both append; a rebase keeps both additions whole."""
        git(self.main, "config", "merge.append.driver", "python3 append_merge.py %O %A %B")
        self.write(self.task, "memory/lessons.md", rec("from the task"), "a")
        git(self.task, "commit", "-qam", "task")
        git(self.task, "push", "-q", "origin", "HEAD:main")
        self.write(self.main, "memory/lessons.md", rec("from the scan"), "a")
        git(self.main, "commit", "-qam", "scan")
        git(self.main, "pull", "-q", "--rebase", "origin", "main")
        text = read(os.path.join(self.main, "memory/lessons.md"))
        self.assertIn("from the task", text)
        self.assertIn("from the scan", text)


class Approval(unittest.TestCase):
    S = AP.settings(None)

    def test_settings_and_parse(self):
        self.assertEqual(self.S, dict(min_paper_signals=20, min_paper_avg_r=0.0, max_divergence_r=0.30))
        got, probs = AP.parse_approvals([
            {"strategy": "S6-OB-FVG", "version": "1.0", "tf": "15m", "date": "2026-10-04"},
            {"strategy": "S6-OB-FVG", "version": "1.0", "tf": "1h"},
            {"strategy": "X", "version": "1.0", "tf": "1h", "date": "04/10/2026"}, "yes"])
        self.assertEqual(list(got), ["S6-OB-FVG@1.0|15m"])
        self.assertEqual(len(probs), 3)
        self.assertEqual(AP.parse_approvals(None), ({}, []))

    def test_eligibility_numbers(self):
        good = dict(n=20, avg_r=0.1)
        self.assertEqual(AP.eligible("PAPER_TRADING", good, 0.3, self.S), (True, []))
        self.assertFalse(AP.eligible("PAPER_TRADING", dict(n=19, avg_r=0.5), 0.3, self.S)[0])
        self.assertFalse(AP.eligible("PAPER_TRADING", dict(n=30, avg_r=-0.01), 0.1, self.S)[0])
        self.assertTrue(AP.eligible("PAPER_TRADING", dict(n=30, avg_r=0.0), 0.3, self.S)[0])      # 0R is enough
        ok, why = AP.eligible("PAPER_TRADING", dict(n=30, avg_r=0.05), 0.40, self.S)             # 0.35R below
        self.assertFalse(ok)
        self.assertIn("divergence", why[0])
        self.assertTrue(AP.eligible("PAPER_TRADING", dict(n=30, avg_r=0.10), 0.40, self.S)[0])    # exactly 0.30R
        self.assertFalse(AP.eligible("VALIDATION", good, 0.3, self.S)[0])
        self.assertFalse(AP.eligible("PAPER_TRADING", good, None, self.S)[0])

    def test_only_the_operator_approves(self):
        e = dict(date="2026-10-04")
        self.assertEqual(AP.decide("PAPER_TRADING", None, True, [])[0], "PAPER_TRADING")      # engine never approves
        st, note, warn = AP.decide("PAPER_TRADING", e, True, [])
        self.assertEqual((st, warn), ("APPROVED", None))
        self.assertIn("2026-10-04", note)
        st, _, warn = AP.decide("PAPER_TRADING", e, False, ["5 closed paper signals, needs 20"])
        self.assertEqual(st, "PAPER_TRADING")
        self.assertIn("needs 20", warn)
        self.assertEqual(AP.decide("APPROVED", e, False, ["x"])[0], "APPROVED")      # retirement rules decide
        self.assertEqual(AP.decide("APPROVED", None, True, [])[0], "PAPER_TRADING")  # line removed = back to paper
        st, _, warn = AP.decide("RETIRED", e, False, [])
        self.assertEqual(st, "RETIRED")
        self.assertIn("RETIRED", warn)
        self.assertEqual(AP.decide("FAILED", None, False, []), ("FAILED", "", None))

    def cell(self):
        rng = np.random.default_rng(1)
        per = {c: [dict(entry_time=i * 3_600_000 + k, r=float(rng.normal(0.2, 1)), oos=i >= 70, dir=1 if i % 2 else -1,
                        bars=5, cost_r=0.05) for i in range(100)] for k, c in enumerate(["BTC", "ETH", "SOL"])}
        wins = RS.windows(0, 100 * 3_600_000 + 10, 4)
        R = yaml.safe_load(read(os.path.join(ROOT, "config.yaml")))["research"]
        ev = RS.evaluate(per, per, {"fast 20→16": {"BTC": (10, 2.0)}}, wins, R, 5)
        ev.pop("_raw")
        return dict(strategy="S6-OB-FVG", version="1.0", tf="15m", status="PAPER_TRADING", evidence=ev,
                    beats_twin=True, twin_same_window=None, history_from="2021-01-01",
                    paper=dict(n=22, avg_r=0.2, last_avg_r=0.1, max_dd_r=3.0),
                    attribution=dict(losses=40, wins=60, systematic=["range_market"],
                                     tags={"range_market": dict(losers=20, loss_share=0.5)},
                                     diagnosis=["Regime: loses in RANGE"]))

    def spec(self):
        return dict(id="S6-OB-FVG", version="1.0", family="smc", gate="trend", regimes=["WEAK_BULL"],
                    hypothesis="h", source="s", long=["a"], short=["b"], stop={"method": "atr", "atr": 1.5},
                    control_twin="S6-OB-FVG-noSMC", known_weaknesses="fails in ranges")

    def test_pack_has_every_section_21_part_and_the_yes_line(self):
        text = "\n".join(AP.pack(self.cell(), self.spec(), [("1.0", "2026-09-24", "PAPER_TRADING")], {}, self.S,
                                 "2026-10-04 00:50"))
        for h in ["Definition and lineage", "Backtest (Layers A / B)", "Walk-forward", "Paper trading",
                  "Control twin", "Sensitivity", "Cost stress test", "Risk metrics", "Why it loses",
                  "Known limitations", "(yes/no)", "Not financial advice"]:
            self.assertIn(h, text)
        self.assertIn('- {strategy: S6-OB-FVG, version: "1.0", tf: 15m, date: 2026-10-04}', text)
        self.assertIn("fails in ranges", text)
        line = [l for l in text.splitlines() if l.startswith("  - {strategy")][0]
        got, probs = AP.parse_approvals(yaml.safe_load("approvals:\n" + line)["approvals"])
        self.assertEqual((list(got), probs), (["S6-OB-FVG@1.0|15m"], []), "the line in the pack parses")
        self.assertEqual(AP.filename("S6-OB-FVG", "1.0", "15m"), "S6-OB-FVG_v1.0_15m.md")

    def test_write_packs_and_stale_packs_removed(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        with mock.patch.object(scanner, "REPORTS", tmp):
            folder = os.path.join(tmp, "approval")
            os.makedirs(folder)
            with open(os.path.join(folder, "old_v1.0_1h.md"), "w") as f:
                f.write("stale")
            c = self.cell()
            reg = dict(versions={"S6-OB-FVG@1.0": dict(id="S6-OB-FVG", version="1.0", experiment=1,
                                                      first_tested_utc="2026-09-24 20:00")},
                       cells={"S6-OB-FVG@1.0|15m": dict(status="PAPER_TRADING")})
            out = research.write_packs({"S6-OB-FVG@1.0|15m": c}, ["S6-OB-FVG@1.0|15m"],
                                       {"S6-OB-FVG@1.0": self.spec()}, reg, self.S, "2026-10-04 00:50", False)
            self.assertEqual(os.listdir(folder), ["S6-OB-FVG_v1.0_15m.md"])
            self.assertEqual(out[0]["pack"], "reports/approval/S6-OB-FVG_v1.0_15m.md")
            self.assertIn("v1.0 first tested 2026-09-24 (PAPER_TRADING)",
                          read(os.path.join(folder, "S6-OB-FVG_v1.0_15m.md")))

    def test_research_approval_step(self):
        ev = dict(validate=dict(n=40, avg_r=0.25))
        good, few = dict(n=25, avg_r=0.1), dict(n=5, avg_r=0.1)
        appr = {"S6@1.0|15m": dict(date="2026-10-04")}
        for status, rec_, listed, want, n_warn, n_elig in [
                ("PAPER_TRADING", good, appr, "APPROVED", 0, 0),
                ("PAPER_TRADING", good, {}, "PAPER_TRADING", 0, 1),      # eligible -> pack, but no yes
                ("PAPER_TRADING", few, appr, "PAPER_TRADING", 1, 0),
                ("APPROVED", good, {}, "PAPER_TRADING", 0, 1),
                ("RETIRED", good, appr, "RETIRED", 1, 0)]:
            warns, elig = [], []
            st, note = research.approval_step("S6@1.0|15m", status, "old note", rec_, ev, listed, self.S, warns, elig)
            self.assertEqual((st, len(warns), len(elig)), (want, n_warn, n_elig), (status, listed))
            self.assertEqual(note == "old note", st == status)
        warns = []
        self.assertEqual(research.approval_step("S6@1.0|15m", "PAPER_TRADING", "", good, dict(validate=dict(n=0, avg_r=0)),
                                                appr, self.S, warns, [])[0], "PAPER_TRADING")   # no backtest to compare

    def test_paper_record_continues_with_live_results(self):
        df = pd.DataFrame([
            dict(stage="PAPER_TRADING", status="WIN", result_r=1.0, closed_time_utc="2026-09-01 00:00", strategy="S6",
                 version="1.0", tf="15m"),
            dict(stage="APPROVED", status="LOSS", result_r=-1.0, closed_time_utc="2026-09-20 00:00", strategy="S6",
                 version="1.0", tf="15m"),
            dict(stage="APPROVED", status="OPEN", result_r=None, closed_time_utc=None, strategy="S6", version="1.0",
                 tf="15m"),
            dict(stage="VALIDATION", status="WIN", result_r=2.0, closed_time_utc="2026-09-02 00:00", strategy="S6",
                 version="1.0", tf="15m")])
        self.assertEqual(research.paper_results(df), {("S6", "1.0", "15m"): [1.0, -1.0]})

    def test_report_shows_packs_and_approval_warnings(self):
        out = []
        g = dict(experiments=3, changes=[], not_run={}, rule_errors={}, idle=[],
                 approval=dict(eligible=[dict(strategy="S6-OB-FVG", version="1.0", tf="15m", paper_signals=22,
                                              paper_avg_r=0.2, pack="reports/approval/S6-OB-FVG_v1.0_15m.md")],
                               warnings=["x@1.0|1h: approval not applied - status is VALIDATION"]))
        scanner.render_lifecycle(g, [], out.append)
        text = "\n".join(out)
        self.assertIn("Approval pack ready: S6-OB-FVG v1.0 15m", text)
        self.assertIn("(yes/no)", text)
        self.assertIn("approval not applied", text)

    def test_config_has_no_approval_by_default(self):
        cfg = yaml.safe_load(read(os.path.join(ROOT, "config.yaml")))
        self.assertEqual(cfg["approvals"], [])
        self.assertEqual(AP.settings(cfg["approval"]), self.S)


def log_rows(rows):
    cols = ["stage", "status", "state", "result_r", "closed_time_utc", "tags", "coin", "tf", "strategy"]
    return pd.DataFrame([dict(zip(cols, r)) for r in rows], columns=cols)


NOW = dt.datetime(2026, 9, 27, 4, 7, tzinfo=UTC)      # a Sunday


class Weekly(unittest.TestCase):
    def test_timing(self):
        self.assertTrue(D.is_weekly_time(NOW))
        self.assertFalse(D.is_weekly_time(NOW.replace(hour=3, minute=59)))
        self.assertFalse(D.is_weekly_time(NOW + dt.timedelta(days=1)))
        self.assertEqual(D.week_label(NOW), "2026-W39")

    def test_results_kept_apart_and_only_this_week(self):
        df = log_rows([
            ("APPROVED", "WIN", "CLOSED", 2.0, "2026-09-26 10:00", "", "BTC", "15m", "S6"),
            ("APPROVED", "LOSS", "CLOSED", -1.0, "2026-09-25 10:00", "range_market;late_entry", "ETH", "15m", "S6"),
            ("PAPER_TRADING", "LOSS", "CLOSED", -1.0, "2026-09-26 11:00", "range_market", "SOL", "1h", "S5"),
            ("PAPER_TRADING", "WIN", "CLOSED", 3.0, "2026-09-10 11:00", "", "SOL", "1h", "S5"),     # older
            ("APPROVED", "OPEN", "POSITION_ACTIVE", None, None, "", "BNB", "15m", "S6"),
            ("APPROVED", "NO_TRADE", "NO_TRADE", 0.0, "2026-09-26 12:00", "", "XRP", "15m", "S6")])
        rows = D.closed_between(df, pd.Timestamp(NOW - dt.timedelta(days=7)), pd.Timestamp(NOW))
        res = {r["stage"]: r for r in D.results_by_stage(rows)}
        self.assertEqual((res["APPROVED"]["n"], res["APPROVED"]["total_r"]), (2, 1.0))
        self.assertEqual((res["PAPER_TRADING"]["n"], res["PAPER_TRADING"]["total_r"]), (1, -1.0))
        self.assertEqual(D.loss_tags(rows), [("range_market", 2), ("late_entry", 1)])

    def test_lifecycle_between(self):
        text = ("# log\n\n## 2026-09-19 00:50 UTC\n- **a@1.0 1h**: X → **Y**\n"
                "## 2026-09-26 00:50 UTC\n- **b@1.0 1h**: FORMALIZED → **VALIDATION** (why)\n")
        self.assertEqual(D.lifecycle_between(text, pd.Timestamp(NOW - dt.timedelta(days=7)), pd.Timestamp(NOW)),
                         ["b@1.0 1h: FORMALIZED → VALIDATION (why)"])

    def board(self):
        return [dict(strategy="S6-OB-FVG", version="1.0", tf="15m", status="PAPER_TRADING", avg_r=0.21, trades=140,
                     family="smc", control_twin="S6-OB-FVG-noSMC", beats_twin=True, live_signals=0),
                dict(strategy="S6-OB-FVG-noSMC", version="1.0", tf="15m", status="FAILED", avg_r=-0.1, trades=300,
                     family="price_action", control_twin=None, beats_twin=None, live_signals=0)]

    def test_weekly_email_sections_and_claude_part(self):
        research_ = dict(candidate_lessons=[dict(tag="range_market", cells=["a", "b"], evidence="systematic in 2")],
                         missed_moves=[dict(start_utc="2026-09-25 10:00", verdict="no strategy had a setup")],
                         approval=dict(eligible=[dict(strategy="S6-OB-FVG", version="1.0", tf="15m", paper_signals=22,
                                                      paper_avg_r=0.2, backtest_validate_avg_r=0.3,
                                                      pack="reports/approval/S6-OB-FVG_v1.0_15m.md")], warnings=[]))
        w = D.weekly(NOW, log_rows([]), self.board(), research_, "", "# Weekly\n## Summary\nidea\n",
                     "reports/claude/weekly/2026-09-27.md")
        text = "\n".join(w["lines"])
        for i in range(1, 9):
            self.assertIn(f"\n{i}. " if i > 1 else "1. ", text)
        self.assertIn("Approve S6-OB-FVG v1.0 15m for live emails? (yes/no)", text)
        self.assertIn("beats its twin", text)
        self.assertIn("range_market: systematic in 2", text)
        self.assertIn("1 moves", text)
        self.assertIn("  idea", text)
        self.assertTrue(w["subject"].startswith("[WEEKLY] 2026-W39"))
        w2 = D.weekly(NOW, log_rows([]), [], {}, None, None, "x")
        t2 = "\n".join(w2["lines"])
        self.assertIn("not available this week", t2)
        self.assertIn("No strategy has passed", t2)

    def test_section_and_summary(self):
        text = "# T\n\n## Summary\n\nline 1\nline 2\n\n## Other\nno\n"
        self.assertEqual(D.section(text), ["line 1", "line 2"])
        self.assertEqual(D.section(text, "other"), ["no"])
        self.assertEqual(len(D.section("## Summary\n" + "x\n" * 20, max_lines=5)), 6)
        self.assertIsNone(D.claude_summary(None, "p", "d"))
        self.assertIn("no '## Summary'", D.claude_summary("# only a title\n", "p", "d")["lines"][0])


class ClaudeInEngineEmails(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_daily_email_shows_yesterdays_review_marked_as_ai(self):
        os.makedirs(os.path.join(self.tmp, "reports/claude/daily"))
        with open(os.path.join(self.tmp, "reports/claude/daily/2026-09-25.md"), "w") as f:
            f.write("# Daily review\n## Summary\nTwo paper losses in a range.\n## Losses\nx\n")
        with mock.patch.object(scanner, "ROOT", self.tmp):
            cr = scanner.claude_review(dt.datetime(2026, 9, 26, 0, 7, tzinfo=UTC))
            self.assertIsNone(scanner.claude_review(dt.datetime(2026, 9, 27, 0, 7, tzinfo=UTC)))
            self.assertEqual(scanner.claude_weekly(NOW), (None, "reports/claude/weekly/2026-09-27.md"))
        self.assertEqual(cr["lines"], ["Two paper losses in a range."])
        dly = dict(date="2026-09-26", utc="u", beijing="b", btc={}, fear_greed=None, data_state="GOOD", matrix=[],
                   health=[], events=[], signals=0, claude_review=cr)
        text = "\n".join(briefs.daily_email(dly)["lines"])
        self.assertIn("CLAUDE DAILY REVIEW (written by the AI", text)
        self.assertIn("Two paper losses in a range.", text)
        text = "\n".join(briefs.daily_email(dict(dly, claude_review=None))["lines"])
        self.assertIn("no review for yesterday", text)


class NotifyModes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        os.makedirs(os.path.join(self.tmp, "reports/claude/briefings"))
        for name in ("REPORTS",):
            p = mock.patch.object(notify, name, os.path.join(self.tmp, "reports"))
            p.start()
            self.addCleanup(p.stop)
        for name, f in (("WEEKLY_SENT", "weekly_sent.json"), ("BRAIN_SENT", "brain_sent.json")):
            p = mock.patch.object(notify, name, os.path.join(self.tmp, "reports", f))
            p.start()
            self.addCleanup(p.stop)
        p = mock.patch.object(notify, "ROOT", self.tmp)
        p.start()
        self.addCleanup(p.stop)
        self.sent = []
        p = mock.patch.object(notify, "send_mail", lambda m: self.sent.append((m["subject"], m["text"])) or True)
        p.start()
        self.addCleanup(p.stop)
        p = mock.patch.object(notify, "pages_base", lambda: "https://o.github.io/r/")
        p.start()
        self.addCleanup(p.stop)

    def latest(self, **kw):
        dump(dict(generated_utc="2026-09-27 04:07", position_book_text=["POSITION BOOK", "none"], **kw),
             os.path.join(self.tmp, "reports/latest.json"))

    def test_weekly_once_per_week(self):
        self.latest(weekly=dict(week="2026-W39", subject="[WEEKLY] 2026-W39", lines=["x"]))
        notify.weekly_email()
        notify.weekly_email()
        self.assertEqual(len(self.sent), 1)
        self.assertTrue(self.sent[0][0].startswith("Week 39 · "))
        self.assertTrue(self.sent[0][1].startswith("WEEKLY REPORT · WEEK 39"))
        self.assertIn("Not financial advice.", self.sent[0][1])
        self.latest(weekly=None)
        notify.weekly_email()
        self.assertEqual(len(self.sent), 1)

    def test_briefing_email_and_refusal_email_once(self):
        self.latest()
        p = "reports/claude/briefings/2026-09-25-0820.md"
        with open(os.path.join(self.tmp, p), "w") as f:
            f.write("# BTC holds its range\n## Summary\nquiet\n" + EMAIL["briefings"]
                    + "\n**Research signal. Not financial advice.**\n")
        res = [dict(branch="claude/brain-briefing", sha="a" * 40, subject="Briefing", status="applied", problems=[],
                    applied=[p, "memory/research_sources.md"], skipped=[]),
               dict(branch="claude/brain-daily", sha="b" * 40, subject="Daily", status="rejected",
                    problems=["config.yaml: not allowed"], applied=[], skipped=[])]
        path = os.path.join(self.tmp, "r.json")
        dump(res, path)
        notify.brain_email(path)
        notify.brain_email(path)
        self.assertEqual([s for s, _ in self.sent], ["08:20 · Calm · – signals",
                                                     "! Action needed · Claude task refused (brain-daily)"])
        body = self.sent[0][1]
        self.assertIn("Quiet.", body)
        self.assertIn("https://o.github.io/r/claude/briefings/2026-09-25-0820.html", body)
        self.assertIn("config.yaml: not allowed", self.sent[1][1])


class FactSheet(unittest.TestCase):
    def test_output_paths_are_the_ones_the_guard_accepts(self):
        for h, m, slot in [(0, 20, "0820"), (23, 55, "0820"), (6, 20, "1420"), (13, 20, "2120"), (13, 45, "2120")]:
            now = dt.datetime(2026, 9, 25, h, m, tzinfo=UTC)
            p = brain_pack.target("briefing", now)
            self.assertTrue(p.endswith(f"-{slot}.md"), (h, m, p))
            self.assertTrue(B.allowed_new(p), p)
        self.assertEqual(brain_pack.target("briefing", dt.datetime(2026, 9, 25, 23, 55, tzinfo=UTC)),
                         "reports/claude/briefings/2026-09-26-0820.md")               # Beijing date
        self.assertTrue(B.allowed_new(brain_pack.target("daily", NOW)))
        self.assertEqual(brain_pack.target("weekly", NOW.replace(hour=2)), "reports/claude/weekly/2026-09-27.md")
        self.assertEqual(scanner.claude_weekly(NOW)[1], brain_pack.target("weekly", NOW.replace(hour=2)),
                         "the weekly email reads the file the weekly task writes")
        day = dt.datetime(2026, 9, 25, 15, 30, tzinfo=UTC)
        self.assertEqual(brain_pack.target("daily", day), "reports/claude/daily/2026-09-25.md")

    def test_pack_without_engine_report(self):
        with mock.patch.object(brain_pack, "REPORTS", tempfile.mkdtemp()):
            text = "\n".join(brain_pack.pack("daily", NOW))
        self.assertIn("latest.json is missing", text)
        self.assertIn("WRITE YOUR OUTPUT TO: reports/claude/daily/2026-09-27.md", text)

    def test_task_files_exist_and_name_their_branches(self):
        for f, br in [("briefing.md", "claude/brain-briefing"), ("daily_review.md", "claude/brain-daily"),
                      ("weekly_research.md", "claude/brain-weekly")]:
            text = read(os.path.join(ROOT, "tasks", f))
            self.assertIn(br, text)
            self.assertIn(br, B.BRANCHES)
            self.assertIn("tasks/COMMON.md", text)
        common = read(os.path.join(ROOT, "tasks", "COMMON.md"))
        for k in B.KNOWLEDGE:
            self.assertIn(os.path.basename(k), common)


if __name__ == "__main__":
    unittest.main()


CAL = ("# calendar\nevents:\n"
       "  - {utc: \"2026-10-02 12:30\", type: NFP, name: \"US jobs\", source: \"https://www.bls.gov/x\", check: official_page}\n")


def ev_line(utc="2026-11-06 13:30", typ="NFP", src="https://www.bls.gov/schedule/news_release/empsit.htm",
            check="official_page", name="US jobs report (Oct data)"):
    return f"  - {{utc: \"{utc}\", type: {typ}, name: \"{name}\", source: \"{src}\", check: {check}}}\n"


class CalendarGuard(unittest.TestCase):
    """events.yaml: the weekly research may only ADD complete, officially sourced entries."""

    def review(self, new, base=CAL, cur=None):
        return B.review([dict(path="events.yaml", status="M", base=base, new=new)],
                        {"events.yaml": base if cur is None else cur})

    def test_a_checked_addition_is_applied(self):
        applies, probs, _ = self.review(CAL + ev_line())
        self.assertEqual(probs, [])
        self.assertEqual(applies, [dict(path="events.yaml", kind="append", text=ev_line())])

    def test_refusals(self):
        cases = [(CAL.replace("12:30", "13:30") + ev_line(), "only added"),                 # edited an entry
                 ("# calendar\nevents: []\n", "only"),                                         # deleted
                 (CAL + ev_line(src="https://example.com/cal"), "official site"),
                 (CAL + ev_line(src="http://www.bls.gov/x"), "official site"),
                 (CAL + ev_line(src="https://bls.gov.evil.io/x"), "official site"),
                 (CAL + ev_line(check="operator"), "check must be"),
                 (CAL + ev_line(check="guess"), "check must be"),
                 (CAL + ev_line(typ="RUMOUR"), "type must be"),
                 (CAL + ev_line(utc="2026-11-06"), "utc must be"),
                 (CAL + ev_line(utc="2026-10-02 12:30"), "already in the calendar"),
                 (CAL + ev_line(name=""), "name missing"),
                 (CAL + "  - {utc: [broken\n", "not a valid calendar"),
                 (CAL + ev_line(name="a guaranteed move"), "profit promise"),
                 (CAL + "events: []\n", "earlier entries changed"),     # looks appended, silently wipes the list
                 (CAL + "events:\n" + ev_line(), "earlier entries changed")]
        for new, needle in cases:
            applies, probs, _ = self.review(new)
            self.assertEqual(applies, [], needle)
            self.assertIn(needle, "\n".join(probs), needle)

    def test_addition_fits_the_newest_main(self):
        cur = CAL + ev_line(utc="2026-10-14 12:30", typ="CPI", name="US CPI")         # the operator added one
        applies, probs, _ = self.review(CAL + ev_line(), cur=cur)
        self.assertEqual(probs, [])
        merged = B.apply_text(cur, applies[0])
        self.assertEqual([e["type"] for e in yaml.safe_load(merged)["events"]], ["NFP", "CPI", "NFP"])
        applies, probs, _ = self.review(CAL + ev_line(), cur=CAL + "other_key: 1\n")  # events no longer last
        self.assertIn("does not fit", "\n".join(probs))

    def test_real_calendar_is_accepted_by_its_own_rules(self):
        """Every entry of the committed events.yaml meets the rules the guard applies to new ones
        (the operator's 'operator' mark aside)."""
        text = read(os.path.join(ROOT, "events.yaml"))
        items = yaml.safe_load(text)["events"]
        self.assertGreaterEqual(len(items), 10)
        for e in items:
            one = "events:\n  - " + json.dumps({k: (v if k != "check" or v != "operator" else "indirect")
                                                for k, v in e.items()}) + "\n"
            self.assertEqual(B.check_calendar("events: []\n", one, None), [], e)


class CalendarFile(unittest.TestCase):
    """events.yaml (the engine's calendar): times follow the US summer / winter time rule."""

    def test_times_and_weekdays(self):
        import engine.risk as RK
        items = RK.load_calendar(os.path.join(ROOT, "events.yaml"))
        self.assertEqual(len(RK.parse_events(items)), len(items))
        for e in items:
            t = dt.datetime.strptime(e["utc"], "%Y-%m-%d %H:%M")
            self.assertLess(t.weekday(), 5, e)                                              # never a weekend
            summer = dt.datetime(2026, 3, 8, 7) <= t < dt.datetime(2026, 11, 1, 6)       # US summer time 2026
            if e["type"] in ("NFP", "CPI", "PCE", "GDP", "PPI"):
                self.assertEqual(t.strftime("%H:%M"), "12:30" if summer else "13:30", e)  # 8:30 a.m. New York
            if e["type"] == "FOMC":
                self.assertEqual(t.strftime("%H:%M"), "18:00" if summer else "19:00", e)  # 2:00 p.m. New York
            self.assertIn(e["check"], {"official_page", "official_search", "indirect", "operator"})
        self.assertEqual({(e["utc"], e["type"]) for e in items if e["type"] == "FOMC"},
                         {("2026-10-28 18:00", "FOMC"), ("2026-12-09 19:00", "FOMC")})

    def test_loader(self):
        import engine.risk as RK
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        self.assertEqual(RK.load_calendar(os.path.join(tmp, "none.yaml")), [])
        for text, ok in (("events: []\n", True), ("# only comments\n", True), ("events: {a: 1}\n", False),
                         ("events: [1, 2]\n", False), ("events: [\n", False)):
            p = os.path.join(tmp, "e.yaml")
            with open(p, "w") as f:
                f.write(text)
            if ok:
                self.assertEqual(RK.load_calendar(p), [])
            else:
                with self.assertRaises(ValueError):
                    RK.load_calendar(p)

    def test_scan_reads_the_calendar_file(self):
        src = read(os.path.join(ROOT, "scanner.py"))
        self.assertIn('rk.load_calendar(os.path.join(ROOT, rk.CALENDAR_FILE))', src)
        lines = brain_pack.calendar_lines(dt.datetime(2026, 9, 27, tzinfo=UTC))
        self.assertIn("events.yaml", lines[1])
        self.assertTrue(any("2026-10-02 12:30 UTC NFP" in ln for ln in lines))
        self.assertTrue(any(ln.startswith("- 2026-11: no NFP") for ln in lines))      # the gap is shown
        self.assertFalse(any(ln.startswith("- 2026-09:") for ln in lines))            # not the current month


class Workflows(unittest.TestCase):
    def test_pinned_runner_and_node24_actions(self):
        folder = os.path.join(ROOT, ".github", "workflows")
        for name in sorted(os.listdir(folder)):
            wf = yaml.safe_load(read(os.path.join(folder, name)))
            for job in wf["jobs"].values():
                self.assertEqual(job["runs-on"], "ubuntu-24.04", name)
                uses = [s["uses"] for s in job["steps"] if "uses" in s]
                self.assertNotIn("actions/checkout@v4", uses, name)
                self.assertNotIn("actions/setup-python@v5", uses, name)
                self.assertTrue(any(u == "actions/checkout@v5" for u in uses), name)

    def test_brain_save_step_without_reports_claude(self):
        """The Save step must not fail when reports/claude does not exist yet (nothing applied so far)."""
        wf = yaml.safe_load(read(os.path.join(ROOT, ".github", "workflows", "brain.yml")))
        steps = wf["jobs"]["brain"]["steps"]
        save = next(s for s in steps if s.get("name") == "Save")["run"]
        # the guard checks lab strategy cards with the engine's card checker (numpy / pandas): full requirements
        self.assertIn("pip install -r requirements.txt",
                      next(s for s in steps if s.get("name", "").startswith("Install"))["run"])
        self.assertIn("strategies_lab.yaml", save)
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        origin, work = os.path.join(tmp, "o.git"), os.path.join(tmp, "w")
        git(tmp, "init", "-q", "--bare", "-b", "main", origin)
        git(tmp, "clone", "-q", origin, work)
        for c in (["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            git(work, *c)
        os.makedirs(os.path.join(work, "memory"))
        with open(os.path.join(work, "memory", "lessons.md"), "w") as f:
            f.write("x\n")
        for f in ("memory_guard.py", "append_merge.py", ".gitattributes"):         # what the Save step runs
            shutil.copy(os.path.join(ROOT, f), os.path.join(work, f))
        shutil.copytree(os.path.join(ROOT, "engine"), os.path.join(work, "engine"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        git(work, "add", "-A")
        git(work, "commit", "-qm", "start")
        git(work, "push", "-q", "-u", "origin", "main")
        run = lambda: subprocess.run(["bash", "-e", "-c", save], cwd=work, capture_output=True, text=True)
        p = run()
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)                       # nothing new: still green
        self.assertIn("Nothing new", p.stdout)
        with open(os.path.join(work, "memory", "lessons.md"), "a") as f:
            f.write("y\n")
        p = run()
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)                       # a change: committed + pushed
        self.assertEqual(git(work, "rev-list", "--count", "origin/main"), "2")
