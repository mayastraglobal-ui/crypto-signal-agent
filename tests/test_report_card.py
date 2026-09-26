"""Phase 17 part D tests: the agent's weekly report card and the monthly clean-up (add only).

Run:  python -m unittest test_report_card -v      (from tests/)
"""
import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brain_guard  # noqa: E402
import brain_pack  # noqa: E402
import scanner  # noqa: E402
import test_brain  # noqa: E402
import test_lab  # noqa: E402
from engine import cleanup as CL  # noqa: E402
from engine import digest as DG  # noqa: E402
from engine import lifecycle as LC  # noqa: E402
from engine import memory as mem  # noqa: E402
from engine import report_card as RC  # noqa: E402
from engine import trials as T  # noqa: E402

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 10, 4, 4, 7, tzinfo=UTC)          # a Sunday
read = test_brain.read
A, B = dt.date(2026, 9, 27), dt.date(2026, 10, 5)


def lab_card(i, added, factory="failure"):
    return dict(id=f"L{i}", version="1.0", added=added, factory=factory)


def log_rows(rows):
    cols = ["signal_time_utc", "stage", "state", "tags", "result_r", "mfe_r"]
    return pd.DataFrame([dict(zip(cols, r)) for r in rows], columns=cols)


WEEKLY = """# Weekly research 2026-10-04
## Summary
x
## Process improvement
- Change: spend the failure quota only on cells with 100+ trades.
- Why: 3 failure cards this week, none past BACKTESTING (report card 3).
- Check: failure pass rate next month.
## Pages that failed to open
- https://papers.ssrn.com/x (blocked)
## Run log
- run: started 2026-10-04 01:53 UTC, finished 2026-10-04 02:31 UTC; problems: none
"""


class Pieces(unittest.TestCase):
    def test_ideas_and_idea_to_test(self):
        src = ("\n### a\n- timestamp: 2026-09-28 10:00 UTC · x\n\n### b\n- timestamp: 2026-09-01 10:00 UTC · x\n")
        lab = [lab_card(1, "2026-09-28"), lab_card(2, "2026-09-30", "literature"), lab_card(3, "2026-09-01")]
        i = RC.ideas_researched(src, lab, A, B)
        self.assertEqual((i["sources"], i["cards"], i["by_factory"]), (1, 2, {"failure": 1, "literature": 1}))
        rows = T.number([dict(strategy="L1", version="1.0", tf="1h", first_tested_utc="2026-09-29 00:40", origin="lab"),
                         dict(strategy="L1", version="1.0", tf="4h", first_tested_utc="2026-10-01 00:40", origin="lab"),
                         dict(strategy="L3", version="1.0", tf="1h", first_tested_utc="2026-09-05 00:40", origin="lab")], 0)
        t = RC.idea_to_test(lab, rows)
        self.assertEqual((t["n"], t["median"], t["max"], t["waiting"]), (2, 2.5, 4, ["L2@1.0"]))   # 1 day and 4 days

    def test_paper_gap_and_signals(self):
        cells = {"x|1h": dict(paper=dict(n=8, avg_r=-0.1), evidence=dict(validate=dict(n=40, avg_r=0.25))),
                 "y|1h": dict(paper=dict(n=3, avg_r=0.5), evidence=dict(validate=dict(n=40, avg_r=0.1)))}
        g = RC.paper_gap(cells)
        self.assertEqual([(x["cell"], x["gap"]) for x in g], [("x|1h", -0.35)])            # y has 3 signals only
        log = log_rows([("2026-10-01 10:00", "PAPER_TRADING", "CLOSED", "", -1.0, 0.1),      # false
                        ("2026-10-01 11:00", "PAPER_TRADING", "CLOSED", "", -1.0, 0.8),      # a loss, not false
                        ("2026-10-02 11:00", "PAPER_TRADING", "EXPIRED", "", None, None),    # late
                        ("2026-10-02 12:00", "APPROVED", "CLOSED", "late_entry", 1.2, 1.5),  # late
                        ("2026-09-01 12:00", "APPROVED", "CLOSED", "", -1.0, 0.0)])          # last month
        s = RC.late_false(log, pd.Timestamp(NOW - dt.timedelta(days=7)), pd.Timestamp(NOW))
        self.assertEqual(s["PAPER_TRADING"], dict(signals=3, closed=2, late=1, false=1))
        self.assertEqual(s["APPROVED"], dict(signals=1, closed=1, late=1, false=0))

    def test_pages_runs_slots(self):
        f = RC.failed_pages(dict(sources={"CoinDesk": dict(status="ok"), "The Block": dict(status="error", error="403")}),
                            [WEEKLY, "## Pages that failed to open\n- none\n"])
        self.assertEqual((f["feeds"], f["pages"]), (["The Block: 403"], ["https://papers.ssrn.com/x (blocked)"]))
        runs = RC.task_runs({"weekly": {"2026-10-04.md": WEEKLY},
                             "daily": {"a.md": "## Run log\n- run: started 2026-10-01 15:27 UTC, finished 2026-10-01 "
                                               "15:40 UTC; problems: usage limit reached\n"}},
                            [dict(when="2026-10-02 15:45", status="rejected"), dict(when="2026-09-01 15:45",
                                                                                   status="rejected")], A, B)
        self.assertEqual(runs["weekly"], dict(expected=1, delivered=1, minutes_median=38, run_logs=1,
                                              reported_problems=0))
        self.assertEqual((runs["daily"]["delivered"], runs["daily"]["reported_problems"]), (1, 1))
        self.assertEqual(runs["briefings"]["delivered"], 0)
        self.assertEqual(runs["refused_pushes"], 1)
        slots = RC.lab_slots([lab_card(1, "2026-10-01"), lab_card(2, "2026-09-20"),
                              lab_card(3, "2026-10-02", "variant_search")], {"failure": 5}, NOW.date())
        self.assertEqual(slots["failure"], dict(used=1, allowed=5))
        self.assertEqual(slots["variant_search"], dict(used=1, allowed=3))


class Card(unittest.TestCase):
    def test_all_eleven_items_and_the_proposal(self):
        rc = RC.build(NOW, dict(factories={"failure": dict(cards=2, cells=4, passed=1, pass_rate=0.25)},
                                missed_moves=[dict(start_utc="2026-10-01 10:00", verdict="no strategy had a setup")]),
                      log_rows([]), [lab_card(1, "2026-10-01")], "", "", None, {"weekly": {"w": WEEKLY}}, [], {},
                      WEEKLY)
        text = "\n".join(RC.lines(rc))
        for i in range(1, 12):
            self.assertIn(f"  {i}. ", text)
        self.assertIn("failure 1/4", text)
        self.assertIn("Missed strong moves: 1 - no strategy had a setup: 1", text)
        self.assertIn("spend the failure quota only on cells with 100+ trades", text)
        self.assertIn("weekly 1/1 (~38 min)", text)
        self.assertEqual(test_brain.B.lint(text), [])
        none = "\n".join(RC.lines(RC.build(NOW, {}, None, [], None, None, None, {}, [], None, None)))
        self.assertIn("none proposed this week", none)

    def test_collect_reads_the_repository_files(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        for d in ("memory", "reports/claude/weekly", "reports/claude/daily"):
            os.makedirs(os.path.join(tmp, d))
        shutil.copy(os.path.join(ROOT, "config.yaml"), tmp)
        with open(os.path.join(tmp, "strategies_lab.yaml"), "w") as f:
            f.write(yaml.safe_dump([lab_card(1, "2026-10-01")]))
        with open(os.path.join(tmp, "reports/claude/weekly/2026-10-04.md"), "w") as f:
            f.write(WEEKLY)
        with open(os.path.join(tmp, "reports/claude/daily/2026-09-01.md"), "w") as f:     # last month: not counted
            f.write("# old\n")
        with open(os.path.join(tmp, "reports/claude/runs.csv"), "w") as f:
            f.write("when,branch,sha,status,problems,applied\n2026-10-02 10:00,claude/brain-daily,abc,rejected,2,0\n")
        rc = RC.collect(tmp, NOW, {}, None)
        self.assertEqual((rc["runs"]["weekly"]["delivered"], rc["runs"]["daily"]["delivered"]), (1, 0))
        self.assertEqual(rc["runs"]["refused_pushes"], 1)
        self.assertEqual(rc["ideas"]["cards"], 1)
        self.assertTrue(rc["proposal"])

    def test_weekly_email_and_fact_sheet(self):
        w = DG.weekly(NOW, test_brain.log_rows([]), [], {}, "", WEEKLY, "x", card_lines=["AGENT REPORT CARD (x)",
                                                                                         "  1. y"])
        text = "\n".join(w["lines"])
        self.assertLess(text.index("AGENT REPORT CARD"), text.index("8. CLAUDE'S WEEKLY RESEARCH"))
        with mock.patch.object(scanner.rcard, "collect", side_effect=RuntimeError("boom")):
            self.assertIn("could not be built", scanner.report_card(NOW, {}, None)[0][0])   # never stops the email
        common = read(os.path.join(ROOT, "tasks", "COMMON.md"))
        self.assertIn("## Run log", common)
        self.assertIn("## Pages that failed to open", common)
        self.assertIn("## Process improvement", read(os.path.join(ROOT, "tasks", "weekly_research.md")))
        self.assertTrue(RC.RUN_RE.search(common))                               # the example parses

    def test_guard_logs_every_push(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        with mock.patch.object(brain_guard, "RUNS", os.path.join(tmp, "runs.csv")):
            for st in ("applied", "rejected"):
                brain_guard.log_run(dict(when="2026-10-01 10:00", branch="claude/brain-daily", sha="abcdef123456",
                                         status=st, problems=["p"] if st == "rejected" else [], applied=["a"]))
            text = read(os.path.join(tmp, "runs.csv"))
        self.assertEqual(text.splitlines()[0], "when,branch,sha,status,problems,applied")
        self.assertEqual(text.splitlines()[2], "2026-10-01 10:00,claude/brain-daily,abcdef12,rejected,1,1")
        for f in ("reports/claude/runs.csv", "memory/retired_cards.csv", "memory/cleanup_log.md"):
            self.assertIn(f, mem.APPEND_ONLY)


def registry(cells):
    reg = LC.empty_registry()
    for ck, (status, since) in cells.items():
        reg["cells"][ck] = dict(status=status, since_utc=since)
    return reg


class Cleanup(unittest.TestCase):
    def test_dead_cards(self):
        reg = registry({"a@1.0|1h": ("FAILED", "2026-08-01 00:40"), "a@1.0|4h": ("RETIRED", "2026-08-20 00:40"),
                        "b@1.0|1h": ("FAILED", "2026-08-01 00:40"), "b@1.0|4h": ("BACKTESTING", "2026-08-01 00:40"),
                        "c@1.0|1h": ("FAILED", "2026-09-25 00:40"),
                        "d@1.0|1h": ("FAILED", "2026-07-01 00:40")})
        dead = CL.dead_cards(reg, {"d@1.0"}, dt.datetime(2026, 10, 1, 0, 40, tzinfo=UTC))
        self.assertEqual([k for k, _ in dead], ["a@1.0"])               # b still tested, c too recent, d already out
        self.assertIn("42+ days", dead[0][1])

    def test_duplicate_lessons_and_rechecks(self):
        rec = lambda t, ts, body="details": (f"\n### {t}\n- timestamp: {ts} · source: x · evidence: FACT: 3 tests · "
                                             f"confidence: m · strategy: - · asset: - · timeframe: - · regime: - · "
                                             f"review: 2026-11-01\n  {body}\n")
        text = (rec("Range markets hurt trend pullbacks", "2026-08-01 10:00 UTC", "range_market in 40% of losses")
                + rec("Trend pullbacks hurt in range markets", "2026-08-20 10:00 UTC", "range_market again")
                + rec("Low volume breakouts fail", "2026-09-28 10:00 UTC", "low_relative_volume")
                + rec("Funding matters", "2026-08-01 10:00 UTC", "no tag here"))
        dups = CL.duplicate_lessons(text)
        self.assertEqual([(a, b) for a, b, _ in dups], [("Range markets hurt trend pullbacks",
                                                         "Trend pullbacks hurt in range markets")])
        merged = text + rec("Merged: Range markets hurt trend pullbacks + Trend pullbacks hurt in range markets",
                            "2026-10-01 15:30 UTC")
        self.assertEqual(CL.duplicate_lessons(merged), [])               # already merged by the daily review
        research = dict(cells={"x|1h": dict(attribution=dict(systematic=["range_market"])),
                               "y|4h": dict(attribution=dict(systematic=["range_market"]))})
        rc = CL.recheck_lessons(text, research, dt.datetime(2026, 10, 1, tzinfo=UTC))
        by = {r["title"]: r for r in rc}
        self.assertIn("STILL HOLDS", by["Range markets hurt trend pullbacks"]["now"])
        self.assertNotIn("Low volume breakouts fail", by)                # younger than 30 days
        self.assertIn("by hand", by["Funding matters"]["now"])
        gone = CL.recheck_lessons(text, dict(cells={}), dt.datetime(2026, 10, 1, tzinfo=UTC))
        self.assertIn("NO LONGER SHOWS", {r["title"]: r for r in gone}["Range markets hurt trend pullbacks"]["now"])

    def test_outputs_are_additions_only(self):
        res = CL.run(registry({"a@1.0|1h": ("FAILED", "2026-08-01 00:40")}), "", "", {},
                     dt.datetime(2026, 10, 1, 0, 40, tzinfo=UTC))
        rows = CL.retired_rows(res, True)
        self.assertEqual(rows.splitlines()[0], "key,retired_utc,reason")
        self.assertEqual(CL.retired(rows), {"a@1.0": res["dead"][0]["reason"]})
        self.assertEqual(CL.retired_rows(res, False).count("\n"), 1)
        log = CL.log_text(res)
        self.assertIn("## 2026-10 clean-up", log)
        self.assertIn("a@1.0", log)

    def test_retired_cards_are_not_tested_but_stay_in_the_files(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        shutil.copy(os.path.join(ROOT, "strategies.yaml"), tmp)
        os.makedirs(os.path.join(tmp, "memory"))
        with open(os.path.join(tmp, "memory", "retired_cards.csv"), "w") as f:
            f.write("key,retired_utc,reason\nema_9_21_cross@1.0,2026-10-01 00:40,dead\n")
        with mock.patch.object(scanner, "ROOT", tmp), mock.patch.object(scanner, "MEMORY", os.path.join(tmp, "memory")):
            ok, problems, idle, _ = scanner.load_cards()
        self.assertNotIn("ema_9_21_cross@1.0", {f"{x['id']}@{x['version']}" for x in ok})
        self.assertIn("RETIRED (monthly clean-up)", {x["status"] for x in idle})
        self.assertIn("ema_9_21_cross", read(os.path.join(tmp, "strategies.yaml")))

    def test_fact_sheet_and_task(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        with open(os.path.join(tmp, "cleanup_log.md"), "w") as f:
            f.write("# Monthly clean-up log\n" + CL.log_text(dict(month="2026-10", run_utc="2026-10-01 00:40",
                                                                  dead=[], duplicates=[dict(a="x", b="y", similarity=0.7)],
                                                                  rechecks=[])))
        with mock.patch.object(brain_pack, "MEMORY", tmp):
            first = "\n".join(brain_pack.cleanup_lines(dt.datetime(2026, 10, 1, 15, 30, tzinfo=UTC)))
            later = brain_pack.cleanup_lines(dt.datetime(2026, 10, 9, 15, 30, tzinfo=UTC))
        self.assertIn("'x' ~ 'y' (0.7)", first)
        self.assertIn("Merged: <title>", first)
        self.assertEqual(later, [])
        daily = read(os.path.join(ROOT, "tasks", "daily_review.md"))
        self.assertIn("Monthly clean-up (first 3 days of a month", daily)
        self.assertIn("11. Run the end commands", daily)


if __name__ == "__main__":
    unittest.main()
