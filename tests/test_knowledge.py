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
            self.assertEqual(len(SS.edge_lines(c)), 4)

    def test_edge_is_not_part_of_the_rules(self):
        c = SS.render(test_lab.lib("trend_pullback"))
        self.assertEqual(SS.fingerprint(c), SS.fingerprint({k: v for k, v in c.items() if k != "edge"}))
        self.assertNotIn("edge", SS.LOGIC_KEYS)

    def test_rules_for_the_block(self):
        self.assertIn("edge block missing", SS.edge_problems({})[0])
        e = dict(test_lab.lib("trend_pullback")["edge"])
        self.assertEqual(SS.edge_problems({"edge": e}), [])
        for k in SS.EDGE_KEYS:
            short = dict(e, **{k: "too short"})
            self.assertEqual(len(SS.edge_problems({"edge": short})), 1, k)
            self.assertIn(f"edge.{k}", SS.edge_problems({"edge": {x: v for x, v in e.items() if x != k}})[0])

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
        self.assertIn(f"{self.PATH} merge=union", read(os.path.join(ROOT, ".gitattributes")))
        self.assertEqual(B.lint(text), [])

    def test_tasks_may_add_a_record(self):
        base = read(os.path.join(ROOT, self.PATH))
        add = test_brain.rec("Review: Options expiries (Deribit)", ev="RESEARCH_FINDING: 1 paper")
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

    def test_committed_playbook_and_files(self):
        text = read(os.path.join(ROOT, "memory", "playbook.md"))
        self.assertTrue(text.startswith("# Regime playbook (generated - do not edit)"))
        self.assertNotIn("memory/playbook.md", B.KNOWLEDGE)                     # Claude's tasks cannot write it
        self.assertNotIn("memory/playbook.md", mem.APPEND_ONLY)                 # rewritten by every research run
        self.assertIn("reports/*_offline.md", read(os.path.join(ROOT, ".gitignore")))


class Curriculum(unittest.TestCase):
    def test_lessons(self):
        lessons = CUR.parse(read(os.path.join(ROOT, "memory", "curriculum.md")))
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
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        rep = os.path.join(tmp, "latest.json")
        sent_mail = []
        patches = [mock.patch.object(notify, "REPORTS", tmp),
                   mock.patch.object(notify, "DAILY_SENT", os.path.join(tmp, "daily_sent.json")),
                   mock.patch.object(notify, "CURRICULUM_SENT", os.path.join(tmp, "curriculum_sent.json")),
                   mock.patch.object(notify, "send", lambda s, b, a=(): sent_mail.append((s, b)) or True)]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

        def day(d):
            test_brain.dump(dict(generated_utc=f"{d} 00:07", position_book_text=["BOOK"],
                                 daily=dict(date=d, utc=f"{d} 00:07"), daily_lines=["DAILY BODY"]), rep)
        day("2026-09-26")
        notify.daily_email()
        notify.daily_email()                                                   # same day: nothing new
        self.assertEqual(len(sent_mail), 1)
        self.assertIn("LESSON 1 of", sent_mail[0][1])
        self.assertIn("What \"R\" means", sent_mail[0][1])
        day("2026-09-27")
        notify.daily_email()
        self.assertIn("LESSON 2 of", sent_mail[1][1])
        self.assertEqual(test_brain.json.loads(read(os.path.join(tmp, "curriculum_sent.json"))), ["L01", "L02"])
        # a broken lesson file never stops the daily email
        with mock.patch.object(notify, "CURRICULUM", os.path.join(tmp, "missing.md")):
            day("2026-09-28")
            notify.daily_email()
        self.assertEqual(len(sent_mail), 3)
        self.assertNotIn("LESSON", sent_mail[2][1])


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
