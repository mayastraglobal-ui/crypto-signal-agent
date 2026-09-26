"""Phase 17 part B tests: the edge block, memory/market_mechanics.md, the regime playbook (memory/playbook.md) and the
beginner curriculum (one lesson per [DAILY] email).

Run:  python -m unittest test_knowledge -v      (from tests/)
"""
import copy
import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brain_pack  # noqa: E402
import notify  # noqa: E402
import test_brain  # noqa: E402
import test_lab  # noqa: E402
from engine import approval as AP  # noqa: E402
from engine import brain as B  # noqa: E402
from engine import curriculum as CUR  # noqa: E402
from engine import memory as mem  # noqa: E402
from engine import playbook as PB  # noqa: E402
from engine import regime as rg  # noqa: E402
from engine import strategy_spec as SS  # noqa: E402

read = test_brain.read
LIB = yaml.safe_load(read(os.path.join(ROOT, "strategies.yaml")))


class EdgeBlock(unittest.TestCase):
    def test_every_library_idea_has_an_edge_and_twins_are_exempt(self):
        for c in LIB:
            if c.get("twin_of"):
                continue
            self.assertEqual(SS.edge_problems(c), [], c["id"])
            self.assertIn(c["edge"]["type"], SS.EDGE_TYPES)
            self.assertEqual(len(SS.edge_lines(c)), 6)
            self.assertEqual(c["edge"]["works_in"], c["regimes"])

    def test_edge_is_not_part_of_the_rules(self):
        c = SS.render(test_lab.lib("trend_pullback"))
        self.assertEqual(SS.fingerprint(c), SS.fingerprint({k: v for k, v in c.items() if k != "edge"}))
        self.assertNotIn("edge", SS.LOGIC_KEYS)

    def test_rules_for_the_block(self):
        self.assertIn("edge block missing", SS.edge_problems({})[0])
        e = dict(test_lab.lib("trend_pullback")["edge"])
        tp = test_lab.lib("trend_pullback")
        self.assertEqual(SS.edge_problems(tp), [])
        for bad, why in ((dict(e, type="luck"), "edge.type"), (dict(e, works_in=[]), "edge.works_in"),
                         (dict(e, works_in=["RANGE"]), "not in the card's regimes")):
            card = dict(test_lab.lib("trend_pullback"), edge=bad)
            self.assertIn(why, " ".join(SS.edge_problems(card)))
        for k in SS.EDGE_KEYS:
            short = dict(e, **{k: "too short"})
            self.assertEqual(len(SS.edge_problems(dict(tp, edge=short))), 1, k)
            self.assertIn(f"edge.{k}", SS.edge_problems(dict(tp, edge={x: v for x, v in e.items() if x != k}))[0])

    def test_lab_card_without_an_edge_is_refused_but_a_twin_is_not(self):
        card = {k: v for k, v in test_lab.v11().items() if k != "edge"}
        applies, probs, _ = test_lab.review([card])
        self.assertEqual(applies, [])
        self.assertIn("edge block missing", " ".join(probs))
        c, twin = test_lab.smc_pair()
        self.assertNotIn("edge", twin)
        self.assertEqual(test_lab.review([c, twin])[1], [])

    def test_approval_pack_shows_the_edge_first(self):
        a = test_brain.Approval("test_pack_has_every_section_21_part_and_the_yes_line")
        spec = dict(a.spec(), edge=test_lab.lib("S6-OB-FVG")["edge"])
        text = "\n".join(AP.pack(a.cell(), spec, [], {}, AP.settings(None), "2026-10-04 00:50"))
        self.assertIn("- edge (why it should work", text)
        self.assertLess(text.index("Who pays:"), text.index("## 2. Backtest"))
        bare = "\n".join(AP.pack(a.cell(), a.spec(), [], {}, AP.settings(None), "2026-10-04 00:50"))
        self.assertIn("NOT WRITTEN - ask for an edge block", bare)

    def test_fact_sheet_edges(self):
        res = dict(cells={"S6-OB-FVG@1.0|15m": dict(strategy="S6-OB-FVG", version="1.0", status="VALIDATION"),
                          "x@1.0|1h": dict(strategy="x", version="1.0", status="FAILED")})
        text = "\n".join(brain_pack.edge_lines_for(res))
        self.assertIn("S6-OB-FVG@1.0:", text)
        self.assertIn("Who pays:", text)
        self.assertNotIn("x@1.0", text)
        self.assertIn("no strategy in VALIDATION", "\n".join(brain_pack.edge_lines_for({})))


class MarketMechanics(unittest.TestCase):
    PATH = "memory/market_mechanics.md"

    def test_file_is_complete_records_and_append_only(self):
        text = read(os.path.join(ROOT, self.PATH))
        recs = mem.parse(text)
        self.assertGreaterEqual(len(recs), 10)
        body = text[text.index("\n### "):]
        self.assertEqual(B.check_records(body, self.PATH), [])
        for r in recs:                       # honest labels: nothing unsourced is called FACT or a finding
            if "no source was opened" in r["evidence"]:
                self.assertTrue(r["evidence"].startswith("CLAIM"), r["title"])
        self.assertIn(self.PATH, B.KNOWLEDGE)
        self.assertIn(self.PATH, mem.APPEND_ONLY)
        self.assertIn(f"{self.PATH} merge=append", read(os.path.join(ROOT, ".gitattributes")))
        self.assertEqual(B.lint(text), [])

    def test_tasks_may_add_a_record(self):
        base = read(os.path.join(ROOT, self.PATH))
        add = test_brain.rec("Review: Options expiries (Deribit)", ev="RESEARCH_FINDING: 1 paper").replace(
            "  details\n", "  - mechanism: hedging flows\n  - strategies: none yet\n")
        applies, probs, _ = B.review([test_brain.change(self.PATH, "M", base, base + add)], {self.PATH: base})
        self.assertEqual(probs, [])
        applies, probs, _ = B.review([test_brain.change(self.PATH, "M", base, base.replace("Open interest", "OI"))],
                                     {self.PATH: base})
        self.assertTrue(probs)


def cell(sid, tf, by_regime, status="BACKTESTING", lab=False):
    return dict(strategy=sid, version="1.0", tf=tf, status=status, lab=lab,
                attribution=dict(by_regime={k: dict(n=n, avg_r=a) for k, (n, a) in by_regime.items()}))


class Playbook(unittest.TestCase):
    def setUp(self):
        self.cells = {"a|1h": cell("a", "1h", {"RANGE": (40, 0.20), "STRONG_BULL": (100, -0.3)}),
                      "b|4h": cell("b", "4h", {"RANGE": (60, -0.15), "STRONG_BULL": (29, 2.0)}, lab=True),
                      "c|1h": cell("c", "1h", {"RANGE": (100, 0.002)})}
        self.fam = {"a@1.0": "breakout", "b@1.0": "breakout", "c@1.0": "mean_reversion"}
        self.pb = PB.build(self.cells, self.fam, rg.LABELS)

    def test_only_measured_cells_with_enough_trades(self):
        r = self.pb["RANGE"]
        self.assertEqual([x[0] for x in r["fits"]], ["a v1.0 1h"])            # c +0.002R is not "made money"
        self.assertEqual([x[0] for x in r["avoid"]], ["b v1.0 4h (lab)"])
        fam = {f: (n, round(a, 4)) for f, n, a in r["families"]}
        self.assertEqual(fam["breakout"], (100, round((40 * 0.2 + 60 * -0.15) / 100, 4)))   # trade-weighted
        s = self.pb["STRONG_BULL"]
        self.assertEqual(s["fits"], [])                                         # b has only 29 trades there
        self.assertEqual([x[0] for x in s["avoid"]], ["a v1.0 1h"])
        self.assertEqual(self.pb["COMPRESSION"]["cells_seen"], 0)

    def test_render_every_regime_and_no_trade(self):
        text = PB.render(self.pb, "2026-09-26 00:40", rg.LABELS)
        for lab in rg.LABELS:
            self.assertIn(f"## {lab}", text)
        self.assertIn("A map, not a signal", text)
        bull = PB.section("STRONG_BULL", self.pb)
        self.assertIn("NOTHING - no tested strategy made money", "\n".join(bull))
        self.assertIn("standing aside IS the playbook", "\n".join(bull))
        self.assertIn("no evidence either way", "\n".join(PB.section("COMPRESSION", self.pb)))
        self.assertEqual(B.lint(text), [])

    def test_fact_sheet_shows_the_regimes_of_now(self):
        rep = dict(universe=dict(signal=["BTC", "ETH"]), regime=dict(coins={
            "BTC": dict(timeframes={"4h": dict(label="RANGE"), "1h": dict(label="RANGE")}),
            "ETH": dict(timeframes={"4h": dict(label="STRONG_BULL")})}))
        res = dict(playbook=json.loads(json.dumps(self.pb)))                  # as research.json stores it
        text = "\n".join(brain_pack.playbook_lines(rep, res))
        self.assertIn("### RANGE - now on BTC 4h, BTC 1h", text)
        self.assertIn("### STRONG_BULL - now on ETH 4h", text)
        self.assertNotIn("COMPRESSION", text)
        self.assertIn("not available yet", "\n".join(brain_pack.playbook_lines(rep, {})))

    def test_family_timeframe_matrix(self):
        mx = PB.matrix(self.cells, self.fam)
        self.assertEqual(mx["breakout|1h"]["RANGE"], [40, 0.2])
        self.assertEqual(mx["breakout|4h"], {"RANGE": [60, -0.15], "BULL": [29, 2.0]})
        self.assertEqual(mx["mean_reversion|1h"]["RANGE"], [100, 0.002])
        text = "\n".join(PB.matrix_lines(mx))
        self.assertIn("| breakout | 1h | -0.30R (100) ✗ | - | +0.20R (40) ✓ | - |", text)
        self.assertIn("| breakout | 4h | +2.00R (29) | - | -0.15R (60) ✗ | - |", text)      # 29 trades: no mark
        self.assertEqual(set(PB.GROUPS), {"BULL", "BEAR", "RANGE", "TRANSITION"})
        self.assertEqual(sorted(x for v in PB.GROUPS.values() for x in v), sorted(rg.LABELS))

    def test_committed_playbook_and_files(self):
        text = read(os.path.join(ROOT, "memory", "playbook.md"))
        self.assertTrue(text.startswith("# Regime playbook (generated - do not edit)"))
        self.assertNotIn("memory/playbook.md", B.KNOWLEDGE)                     # Claude's tasks cannot write it
        self.assertNotIn("memory/playbook.md", mem.APPEND_ONLY)                 # rewritten by every research run
        self.assertIn("reports/*_offline.md", read(os.path.join(ROOT, ".gitignore")))


class Curriculum(unittest.TestCase):
    def test_lessons(self):
        lessons = CUR.parse(read(os.path.join(ROOT, "memory", "beginner_course.md")))
        self.assertGreaterEqual(len(lessons), 12)
        self.assertEqual([x["id"] for x in lessons], [f"L{i:02d}" for i in range(1, len(lessons) + 1)])
        for x in lessons:
            self.assertTrue(x["lines"], x["id"])
            self.assertTrue(any(ln.startswith("Try it:") for ln in x["lines"]), x["id"])
            self.assertEqual(B.lint("\n".join(x["lines"])), [], x["id"])

    def test_order_and_restart(self):
        lessons = CUR.parse("## L01 · A\none\n## L02 · B\ntwo\n## Other heading\nnot a lesson\n")
        self.assertEqual([x["lines"] for x in lessons], [["one"], ["two"]])
        first, sent = CUR.next_lesson(lessons, [])
        self.assertEqual((first["id"], sent), ("L01", ["L01"]))
        second, sent = CUR.next_lesson(lessons, sent)
        self.assertEqual((second["id"], sent), ("L02", ["L01", "L02"]))
        again, sent = CUR.next_lesson(lessons, sent)
        self.assertEqual((again["id"], sent), ("L01", ["L01"]))
        self.assertEqual(CUR.next_lesson([], ["L01"]), (None, ["L01"]))
        self.assertEqual(CUR.email_lines(second, lessons)[1], "LESSON 2 of 2: B")

    def test_daily_email_carries_one_lesson_and_remembers_it(self):
        """Email redesign: each DAILY REVIEW email links the next beginner lesson, published as a page."""
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        sent_mail = []
        patches = [mock.patch.object(notify, "ROOT", tmp),
                   mock.patch.object(notify, "REPORTS", os.path.join(tmp, "reports")),
                   mock.patch.object(notify, "LESSONS", os.path.join(tmp, "reports", "claude", "lessons")),
                   mock.patch.object(notify, "CURRICULUM_SENT", os.path.join(tmp, "curriculum_sent.json")),
                   mock.patch.object(notify, "pages_base", lambda: "https://o.github.io/r/"),
                   mock.patch.object(notify, "send_mail", lambda m: sent_mail.append((m["subject"], m["text"])) or True)]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        rep = dict(generated_utc="2026-09-26 15:50")
        notify.send_daily_review(None, rep, "2026-09-26", rep["generated_utc"])
        self.assertIn("Beginner lesson: https://o.github.io/r/claude/lessons/2026-09-26.html", sent_mail[0][1])
        page = read(os.path.join(tmp, "reports", "claude", "lessons", "2026-09-26.md"))
        self.assertTrue(page.startswith("# Beginner lesson 1 of"))
        self.assertIn("What \"R\" means", page)
        notify.send_daily_review(None, rep, "2026-09-27", rep["generated_utc"])
        self.assertTrue(read(os.path.join(tmp, "reports", "claude", "lessons", "2026-09-27.md")).startswith(
            "# Beginner lesson 2 of"))
        self.assertEqual(test_brain.json.loads(read(os.path.join(tmp, "curriculum_sent.json"))), ["L01", "L02"])
        # a broken lesson file never stops the daily email
        with mock.patch.object(notify, "CURRICULUM", os.path.join(tmp, "missing.md")):
            notify.send_daily_review(None, rep, "2026-09-28", rep["generated_utc"])
        self.assertEqual(len(sent_mail), 3)
        self.assertNotIn("Beginner lesson:", sent_mail[2][1])


class ReadingPlan(unittest.TestCase):
    def test_plan_file(self):
        plan = CUR.parse_plan(read(os.path.join(ROOT, "memory", "curriculum.md")))
        self.assertGreaterEqual(len(plan), 20)
        self.assertEqual([x["id"] for x in plan], [f"C{i:02d}" for i in range(1, len(plan) + 1)])
        self.assertEqual({x["kind"] for x in plan}, set(CUR.KINDS))           # every kind the plan asks for
        for x in plan:
            self.assertTrue(any(ln.startswith("- read:") or ln.startswith("- read / listen:") for ln in x["lines"]))
            self.assertTrue(any(ln.startswith("- for us:") for ln in x["lines"]), x["id"])
            self.assertNotIn("http", " ".join(x["lines"]), "no URL from memory - the task opens the real source")
        self.assertIn("have NOT been opened", read(os.path.join(ROOT, "memory", "curriculum.md")))

    def test_rotation(self):
        plan = [dict(id=f"C0{i}", kind="paper", title=str(i), lines=[]) for i in (1, 2, 3)]
        src = ("\n### [C02] something\n- timestamp: 2026-09-20 15:30 UTC · source: x\n"
               "\n### [C01] other\n- timestamp: 2026-09-21 15:30 UTC · source: x\n"
               "\n### [C01] again\n- timestamp: 2026-09-24 15:30 UTC · source: x\n### unrelated\n")
        done = CUR.studied(src)
        self.assertEqual(done, {"C02": "2026-09-20 15:30 UTC", "C01": "2026-09-24 15:30 UTC"})
        self.assertEqual(CUR.next_item(plan, done)["id"], "C03")                  # never studied first
        done["C03"] = "2026-09-25 15:30 UTC"
        self.assertEqual(CUR.next_item(plan, done)["id"], "C02")                  # then the oldest
        self.assertIsNone(CUR.next_item([], {}))

    def test_fact_sheet_names_todays_item(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        shutil.copy(os.path.join(ROOT, "memory", "curriculum.md"), tmp)
        with open(os.path.join(tmp, "research_sources.md"), "w") as f:
            f.write("\n### [C01] Time series momentum\n- timestamp: 2026-09-24 15:30 UTC · source: daily\n")
        with mock.patch.object(brain_pack, "MEMORY", tmp):
            text = "\n".join(brain_pack.curriculum_lines())
        self.assertIn("- C02 (paper): Risks and returns of cryptocurrency - not studied yet", text)
        self.assertIn("1 studied at least once", text)
        daily = read(os.path.join(ROOT, "tasks", "daily_review.md"))
        self.assertIn("Curriculum (one item a day)", daily)
        self.assertIn("At most ONE testable hypothesis", daily)


class MechanicsRule(unittest.TestCase):
    def test_records_name_mechanism_and_strategies(self):
        base = read(os.path.join(ROOT, "memory", "market_mechanics.md"))
        good = test_brain.rec("Basis trade", ev="CLAIM: blog").replace("  details\n", "  - mechanism: spot vs futures "
                                                                        "spread\n  - strategies: none yet\n")
        applies, probs, _ = B.review([test_brain.change(B.MECHANICS, "M", base, base + good)], {B.MECHANICS: base})
        self.assertEqual(probs, [])
        bad = test_brain.rec("Basis trade", ev="CLAIM: blog")
        applies, probs, _ = B.review([test_brain.change(B.MECHANICS, "M", base, base + bad)], {B.MECHANICS: base})
        self.assertEqual(applies, [])
        self.assertEqual(sum("needs a detail line" in p for p in probs), 2)
        self.assertEqual(B.check_mechanics(base[base.index("### Index: which strategies"):].join(["\n", ""])), [])


class Tasks(unittest.TestCase):
    def test_instructions(self):
        common = read(os.path.join(ROOT, "tasks", "COMMON.md"))
        weekly = read(os.path.join(ROOT, "tasks", "weekly_research.md"))
        brief = read(os.path.join(ROOT, "tasks", "briefing.md"))
        self.assertIn("market_mechanics.md", common)
        self.assertIn("edge block", common)
        self.assertIn("## Market mechanics and edges", weekly)
        self.assertIn("10. Run the end commands", weekly)
        self.assertIn("Playbook for", brief)


if __name__ == "__main__":
    unittest.main()
