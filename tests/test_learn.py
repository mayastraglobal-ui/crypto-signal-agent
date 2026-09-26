"""
Phase 18 part A tests: the research loop (lab card `parent:`, Feedback records, feedback due, idea chains), bull vs
bear with a risk manager that can veto (approval packs, briefing fact sheet, the guard's briefing check), and the
reference projects R1-R8 in the curriculum (weekly, one a week).

Run:  python -m unittest test_learn -v      (from tests/)
"""
import copy
import datetime as dt
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
import scanner  # noqa: E402
import test_brain  # noqa: E402
import test_lab  # noqa: E402
from engine import approval as AP  # noqa: E402
from engine import brain as B  # noqa: E402
from engine import curriculum as CU  # noqa: E402
from engine import debate as DB  # noqa: E402
from engine import ideas as I  # noqa: E402
from engine import research_loop as RL  # noqa: E402
from engine import strategy_spec as SS  # noqa: E402

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 9, 25, 16, 0, tzinfo=UTC)
TFS = ["4h", "1h", "30m", "15m", "5m"]
LESSONS = test_brain.BASE + test_brain.rec("Breakouts fail in chop")


def fb(key="LAB-PLAIN-1@1.0", ts="2026-09-26 15:30", nxt="stop this line", result="1h FAILED 212 trades -0.05R",
       skip=()):
    lines = {"parent": "result: trend_pullback@1.0 1h", "hypothesis": "RSI alone continues the trend.",
             "result": result, "teaches": "the RSI filter adds nothing on 1h", "next": nxt}
    return (f"\n### Feedback: {key}\n- timestamp: {ts} UTC · source: research run {ts[:10]} · evidence: "
            "BACKTEST_EVIDENCE: 1 cell, 212 trades · confidence: medium · strategy: LAB-PLAIN-1 v1.0 · asset: research "
            "coins · timeframe: 1h · regime: - · review: 2026-10-26\n"
            + "".join(f"  - {k}: {v}\n" for k, v in lines.items() if k not in skip))


def row(key, tf, status, since, trades=212, avg=-0.05, test=-0.08, gates="avg -0.05R/trade (needs +0.10R)"):
    sid, ver = key.split("@")
    return dict(id=sid, version=ver, tf=tf, status=status, since_utc=since, trades=str(trades), avg_r=str(avg),
                test_avg_r=str(test), gates_failed=gates)


class ParentField(unittest.TestCase):
    """Every lab card names what led to it (R1: an experiment remembers its parent)."""

    def test_formats(self):
        P = lambda p, others=None: SS.parent_problems(dict(id="X", parent=p), others, TFS)
        self.assertIn("parent missing", P(None)[0])
        self.assertIn("not '<kind>: <reference>'", P("because of a lesson")[0])
        self.assertIn("not '<kind>: <reference>'", P("hunch: it looks good")[0])       # unknown kind
        self.assertIn("too short", P("lesson: ab")[0])
        self.assertEqual(P("lesson: Breakouts fail in chop"), [])
        self.assertEqual(P("result: trend_pullback@1.0 1h", {"trend_pullback": {}}), [])
        self.assertIn("must be", P("result: trend_pullback 1h", {"trend_pullback": {}})[0])
        self.assertIn("timeframe", P("result: trend_pullback@1.0 2h", {"trend_pullback": {}})[0])
        self.assertIn("is not a card", P("result: nosuch@1.0 1h", {"trend_pullback": {}})[0])
        self.assertIn("is not a card", P("card: nosuch@1.0", {"trend_pullback": {}})[0])
        self.assertEqual(P("card: X@1.0", {}), [], "a new version may name the earlier version of itself")
        self.assertIn("date", P("missed_move: BTC big move last week")[0])
        self.assertEqual(P("missed_move: BTC up 6x ATR on 2026-09-20"), [])

    def test_lab_cards_need_it_twins_and_the_library_do_not(self):
        card, twin = test_lab.smc_pair()
        others = {c["id"]: c for c in test_lab.LIB + [card, twin]}
        no_parent = {k: v for k, v in card.items() if k != "parent"}
        probs = SS.lab_card_problems(no_parent, {k: v for k, v in others.items() if k != card["id"]},
                                     B.rg.LABELS, TFS)
        self.assertTrue(any("parent missing" in p for p in probs))
        self.assertEqual(SS.lab_card_problems(twin, {k: v for k, v in others.items() if k != twin["id"]},
                                              B.rg.LABELS, TFS), [], "a control twin is a benchmark: no parent")
        ok, problems, _, _ = SS.load_library(test_lab.LIB, [], B.rg.LABELS, TFS)
        self.assertFalse(problems, "library cards (strategies.yaml) do not need a parent")

    def test_guard_checks_the_named_record_exists(self):
        card = test_lab.plain(1, parent="lesson: Breakouts fail in chop")
        change = test_lab.lab_change([card])
        main = {SS.LAB_FILE: test_lab.LAB_HEAD, SS.LIBRARY_FILE: test_lab.LIB_TEXT}
        _, probs, _ = B.review([change], main, NOW, "claude/brain-weekly", test_lab.BIG)
        self.assertTrue(any("not a record title in memory/lessons.md" in p for p in probs), probs)
        _, probs, _ = B.review([change], dict(main, **{"memory/lessons.md": LESSONS}), NOW, "claude/brain-weekly",
                               test_lab.BIG)
        self.assertEqual(probs, [])
        # the record may also be added in the same push
        add = test_brain.change("memory/lessons.md", "M", test_brain.BASE, LESSONS)
        _, probs, _ = B.review([change, add], dict(main, **{"memory/lessons.md": test_brain.BASE}), NOW,
                               "claude/brain-weekly", test_lab.BIG)
        self.assertEqual(probs, [])

    def test_failure_parent_may_name_a_loss_tag_with_its_count(self):
        mem = {p: "" for p in RL.FILES.values()}
        P = lambda p: RL.parent_exists_problems(dict(parent=p), mem, B.LOSS_TAGS)
        self.assertEqual(P("failure: low_relative_volume in 38% of losses, n=64"), [])
        self.assertTrue(P("failure: low_relative_volume in many losses"))          # no count
        self.assertTrue(P("failure: bad luck in 38% of losses, n=64"))               # not an engine tag
        self.assertEqual(P("result: trend_pullback@1.0 1h"), [], "result parents are checked against the cards")

    def test_engine_variant_cards_carry_their_parent(self):
        cells, cards = I_cells()
        new = I.variant_cards(cells, cards, "2026-09-27", 3, B.rg.LABELS, TFS)
        self.assertTrue(new)
        for c in new:
            self.assertRegex(c["parent"], r"^result: \S+@1\.0 \S+$")
            self.assertEqual(SS.parent_problems(c, {x["id"]: x for x in cards.values()}, TFS), [])


def I_cells():
    """A strong BACKTESTING cell of a library card (the engine's variant search input)."""
    lib = {f"{c['id']}@{c['version']}": c for c in test_lab.LIB}
    key = "donchian_breakout@1.0"
    ev = dict(all=dict(n=120, avg_r=0.08), validate=dict(n=40, avg_r=0.06))
    cell = dict(strategy="donchian_breakout", version="1.0", tf="1h", status="BACKTESTING", evidence=ev,
                attribution=dict(by_regime={}))
    return {f"{key}|1h": cell}, lib


class Feedback(unittest.TestCase):
    """After a test: hypothesis -> result -> what it teaches -> next hypothesis or 'stop this line' (R1)."""

    def test_record_rules(self):
        self.assertEqual(RL.feedback_problems(fb()), [])
        self.assertIn("'- next: ...'", RL.feedback_problems(fb(skip=("next",)))[0])
        self.assertIn("'- teaches: ...'", RL.feedback_problems(fb(skip=("teaches", "parent")))[0])
        self.assertIn("engine's numbers", RL.feedback_problems(fb(result="it failed badly"))[0])
        self.assertIn("Feedback: <id>@<version>", RL.feedback_problems(fb(key="my idea"))[0])
        self.assertEqual(RL.feedback_problems(test_brain.rec("Not a feedback record")), [], "other records untouched")

    def test_guard_refuses_a_bad_feedback_record(self):
        p = "memory/experiments.md"
        base = "# Experiments\n\n| # | a |\n|---|---|\n| EXP-0001 | x |\n"
        _, probs, _ = B.review([test_brain.change(p, "M", base, base + fb(skip=("result",)))], {p: base})
        self.assertTrue(any("'- result: ...'" in x for x in probs), probs)
        applies, probs, _ = B.review([test_brain.change(p, "M", base, base + fb())], {p: base})
        self.assertEqual(probs, [])
        self.assertEqual(applies[0]["kind"], "append")

    def test_due_until_written_and_again_after_a_status_change(self):
        card = dict(test_lab.plain(1), lab=True, parent="result: trend_pullback@1.0 1h")
        cards = {"LAB-PLAIN-1@1.0": card, "trend_pullback@1.0": dict(test_lab.lib("trend_pullback"), lab=False)}
        self.assertEqual(RL.feedback_due(cards, [], {}), [], "not tested yet: nothing to give feedback on")
        rows = [row("LAB-PLAIN-1@1.0", "1h", "FAILED", "2026-09-26 00:49"), row("trend_pullback@1.0", "1h", "FAILED",
                                                                               "2026-09-24 20:19")]
        due = RL.feedback_due(cards, rows, {})
        self.assertEqual([d["key"] for d in due], ["LAB-PLAIN-1@1.0"], "library cards are not part of the loop")
        self.assertIn("1h FAILED 212 trades -0.050R (unseen -0.080R)", due[0]["cells"])
        self.assertEqual(due[0]["parent"], "result: trend_pullback@1.0 1h")
        done = RL.feedback_records(fb(ts="2026-09-26 15:30"))
        self.assertEqual(RL.feedback_due(cards, rows, done), [])
        rows[0]["since_utc"] = "2026-10-02 00:49"                      # a cell changed status after the feedback
        self.assertEqual(RL.feedback_due(cards, rows, done)[0]["last_feedback"], "2026-09-26 15:30")
        twin = dict(card, twin_of="X")
        self.assertEqual(RL.feedback_due({"LAB-PLAIN-1@1.0": twin}, rows, {}), [], "a control twin needs none")

    def test_idea_chains(self):
        a = dict(test_lab.plain(1), lab=True, parent="lesson: Breakouts fail in chop")
        b = dict(test_lab.plain(1), version="1.1", lab=True, parent="result: LAB-PLAIN-1@1.0 1h")
        c = dict(test_lab.plain(2), lab=True, parent="result: trend_pullback@1.0 1h")
        cards = {"LAB-PLAIN-1@1.0": a, "LAB-PLAIN-1@1.1": b, "LAB-PLAIN-2@1.0": c,
                 "trend_pullback@1.0": dict(test_lab.lib("trend_pullback"), lab=False)}
        rows = [row("LAB-PLAIN-1@1.0", "1h", "FAILED", "2026-09-26 00:49")]
        fbs = RL.feedback_records(fb(key="LAB-PLAIN-1@1.1", nxt="stop this line"))
        ch = RL.chains(cards, rows, fbs)
        self.assertEqual(ch[0], ("lesson: Breakouts fail in chop", ["LAB-PLAIN-1@1.0", "LAB-PLAIN-1@1.1"],
                                 "stop this line"))
        self.assertEqual(ch[1], ("result: trend_pullback@1.0 1h", ["LAB-PLAIN-2@1.0"], None),
                         "a library result is the root, not a step")
        text = "\n".join(RL.chain_lines(cards, rows, fbs))
        self.assertIn("LAB-PLAIN-1@1.0 [1h FAILED 212 trades -0.050R (unseen -0.080R)] -> LAB-PLAIN-1@1.1 "
                      "[not tested yet] -> next: stop this line", text)
        self.assertIn("feedback not written yet", text)
        self.assertIn("no lab card with a parent yet", RL.chain_lines({}, [], {})[0])

    def test_fact_sheets_show_the_loop(self):
        # the idea chains are in the weekly research's fact sheet (and so in Claude's full weekly page); the weekly
        # email (format v2) links to that page instead of repeating them
        card = dict(test_lab.plain(1), lab=True, parent="result: trend_pullback@1.0 1h")
        with mock.patch.object(RL, "load", return_value=({"LAB-PLAIN-1@1.0": card},
                                                         [row("LAB-PLAIN-1@1.0", "1h", "FAILED", "2026-09-26 00:49")],
                                                         {})):
            daily = "\n".join(brain_pack.research_loop_lines("daily"))
            weekly = "\n".join(brain_pack.research_loop_lines("weekly"))
        self.assertIn("results waiting for feedback", daily)
        self.assertIn("- LAB-PLAIN-1@1.0 (parent: result: trend_pullback@1.0 1h)", daily)
        self.assertNotIn("waiting for feedback", weekly)
        self.assertIn("## Idea chains", weekly)

    def test_engine_table_restarts_after_review_records(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        path = os.path.join(tmp, "experiments.md")
        e = dict(experiment=21, first_tested_utc="2026-09-27 00:49", key="X@1.0", family="f", timeframes=["1h"],
                 hypothesis="h")
        with mock.patch.object(scanner, "MEMORY", tmp):
            scanner.write_experiments([e], None)
            scanner.write_experiments([dict(e, experiment=22)], None)
            with open(path, "a") as f:
                f.write(fb())
            scanner.write_experiments([dict(e, experiment=23)], None)
        text = test_brain.read(path)
        self.assertEqual(text.count("| # | First tested (UTC)"), 2, "one header at the start, one after the records")
        self.assertIn("| EXP-0022 |", text.split("### Feedback")[0])
        after = text.split("### Feedback")[1]
        self.assertLess(after.index("| # | First tested"), after.index("| EXP-0023 |"))


def cell(good=True):
    c = test_brain.Approval().cell()
    if not good:
        c = copy.deepcopy(c)
        for part in ("all", "validate"):
            c["evidence"][part]["avg_r"] = -0.1
        c["evidence"]["stress"]["avg_r"] = -0.2
        c["evidence"]["walk_forward"]["passed"] = False
        c["beats_twin"] = False
        c["paper"] = dict(n=22, avg_r=-0.3)
    return c


def report(**over):
    rep = dict(generated_utc="2026-09-25 15:07",
               risk=dict(day_r=0.0, week_r=0.0, halts_text=[], blackout_now=[], upcoming_events=[
                   dict(start_utc="2026-09-30 12:30", type="PCE", name="US PCE")],
                   limits=dict(day_r=-3, week_r=-6, positions=3, blackout_minutes=60)),
               position_book=dict(heat=0, limits=dict(heat=3)),
               data_quality=dict(system_state="GOOD", coins={"BTC": dict(state="GOOD"), "ETH": dict(state="GOOD")}),
               universe=dict(signal=["BTC", "ETH"]),
               regime=dict(coins={
                   "BTC": dict(permission="LONG allowed", permission_reason="1D/4H bullish",
                               timeframes={"1d": dict(label="WEAK_BULL", supporting=["ADX 44 = strong trend"]),
                                           "4h": dict(label="STRONG_BULL"), "1h": dict(label="RANGE")}),
                   "ETH": dict(permission="NO TRADE", permission_reason="timeframes disagree",
                               timeframes={"1d": dict(label="WEAK_BEAR", supporting=["close below EMA-fast"]),
                                           "4h": dict(label="RANGE"), "1h": dict(label="RANGE")})}))
    for k, v in over.items():
        rep[k] = v
    return rep


class BullBear(unittest.TestCase):
    """Two sides, engine numbers only (R2); a risk manager that can only say 'not now'."""

    def test_cases_from_the_engine_numbers_only(self):
        bull, bear = DB.cell_cases(cell())
        self.assertTrue(any(x.startswith("unseen part of the backtest") for x in bull))
        self.assertTrue(any("beats its control twin" in x for x in bull))
        self.assertTrue(any("worst drawdown" in x for x in bear), "the bear side always shows the drawdown")
        self.assertTrue(any("range_market" in x for x in bear))
        bull2, bear2 = DB.cell_cases(cell(False))
        self.assertFalse(any("unseen part" in x for x in bull2))
        self.assertTrue(any("unseen part" in x for x in bear2))
        self.assertTrue(any("does NOT beat" in x for x in bear2))
        self.assertTrue(any("paper is" in x and "below the backtest" in x for x in bear2))
        for x in bull + bear + bull2 + bear2:
            self.assertRegex(x, r"\d|twin|no coin", "every point carries a number from the engine")
        lines = DB.case_lines([], [], dict(veto=False, reasons=[], checks=[("heat", False, "heat 0 of 3")]))
        self.assertEqual(lines[0], "Bull case: nothing in the engine's numbers", "an empty side says so")

    def test_data_check_uses_only_the_signal_coins(self):
        """A candidate coin (e.g. a new listing such as BABY or VTHO) with bad data never vetoes the whole market or
        an approval pack; a signal coin with bad data and a bad system state still do."""
        now = NOW.replace(hour=15, minute=30)
        coins = {"BTC": dict(state="GOOD"), "ETH": dict(state="GOOD"), "BABY": dict(state="UNSAFE"),
                 "VTHO": dict(state="DEGRADED")}
        rep = report(data_quality=dict(system_state="GOOD", coins=coins))
        rm = DB.risk_manager(rep, now)
        self.assertFalse(rm["veto"], rm)
        self.assertNotIn("BABY", DB.risk_line(rm))
        pack = DB.risk_manager(rep, now, regimes=["WEAK_BULL", "STRONG_BULL"], tf="4h")          # an approval pack
        self.assertFalse(dict((n, v) for n, v, _ in pack["checks"])["data"], pack)
        bad_eth = report(data_quality=dict(system_state="GOOD", coins=dict(coins, ETH=dict(state="UNSAFE"))))
        rm = DB.risk_manager(bad_eth, now)
        self.assertTrue(rm["veto"])
        self.assertIn("not GOOD: ETH", DB.risk_line(rm))
        self.assertTrue(DB.risk_manager(report(data_quality=dict(system_state="UNSAFE", coins=coins)), now)["veto"])
        self.assertTrue(DB.risk_manager(rep, now, coin="BABY", direction="LONG")["veto"], "one coin: its own data")

    def test_regime_cases(self):
        bull, bear = DB.regime_cases(report()["regime"]["coins"]["BTC"])
        self.assertEqual(bull, ["1D WEAK_BULL (ADX 44 = strong trend)", "4H STRONG_BULL"])
        self.assertEqual(bear, ["no clear direction on 1H RANGE"])

    def test_each_veto(self):
        now = NOW.replace(hour=15, minute=30)
        rm = DB.risk_manager(report(), now)
        self.assertFalse(rm["veto"], rm)
        self.assertTrue(DB.risk_line(rm).startswith("Risk manager: no veto ("))
        cases = {
            "event": report(risk=dict(report()["risk"], upcoming_events=[dict(start_utc="2026-09-25 16:15",
                                                                              name="US CPI")])),
            "heat": report(position_book=dict(heat=3, limits=dict(heat=3))),
            "data": report(data_quality=dict(system_state="DEGRADED", coins={})),
            "limits": report(risk=dict(report()["risk"], day_r=-2.4)),
        }
        for name, rep in cases.items():
            rm = DB.risk_manager(rep, now)
            self.assertTrue(rm["veto"], name)
            self.assertEqual([n for n, v, _ in rm["checks"] if v], [name])
        self.assertIn("US CPI", DB.risk_line(DB.risk_manager(cases["event"], now)))
        self.assertIn("FULL", DB.risk_line(DB.risk_manager(cases["heat"], now)))
        self.assertFalse(DB.risk_manager(report(risk=dict(report()["risk"], day_r=-2.0)), now)["veto"],
                         "-2.0R of -3R is not yet near (75%)")
        self.assertTrue(DB.risk_manager(report(risk=dict(report()["risk"], week_r=-4.5)), now)["veto"])
        self.assertTrue(DB.risk_manager(report(risk=dict(report()["risk"], halts_text=["day limit hit"])), now)["veto"])
        self.assertTrue(DB.risk_manager(report(), now + dt.timedelta(hours=3))["veto"], "a stale report is a veto")
        rm = DB.risk_manager(None, now)
        self.assertTrue(rm["veto"], "no report = conditions unknown = veto")
        # a signal: regime against its direction; one coin's data
        self.assertFalse(DB.risk_manager(report(), now, coin="BTC", direction="LONG")["veto"])
        rm = DB.risk_manager(report(), now, coin="BTC", direction="SHORT")
        self.assertEqual([n for n, v, _ in rm["checks"] if v], ["regime"])
        rep = report(data_quality=dict(system_state="GOOD", coins={"BTC": dict(state="GOOD"),
                                                                   "ETH": dict(state="DEGRADED")}))
        self.assertFalse(DB.risk_manager(rep, now, coin="BTC", direction="LONG")["veto"])
        self.assertTrue(DB.risk_manager(rep, now, coin="ETH", direction="LONG")["veto"])
        # a strategy: is any signal coin in one of its regimes on its timeframe?
        self.assertFalse(DB.risk_manager(report(), now, regimes=["STRONG_BULL"], tf="4h")["veto"])
        rm = DB.risk_manager(report(), now, regimes=["STRONG_BEAR"], tf="15m")
        self.assertIn("0 of 2 signal coins are in one of its regimes on 1H now - regime against", rm["reasons"])

    def test_approval_pack_has_the_debate_first(self):
        now = NOW.replace(hour=15, minute=30)
        spec = test_brain.Approval().spec()
        text = "\n".join(AP.pack(cell(), spec, [], {}, AP.settings(None), "2026-09-25 15:30",
                                 DB.risk_manager(report(), now, regimes=["RANGE"], tf="15m")))
        i = text.index("## 0. Bull vs bear")
        self.assertLess(i, text.index("## 1. Definition"))
        for k in ("- Bull case: unseen part", "- Bear case: ", "- Risk manager: no veto"):
            self.assertIn(k, text)
        veto = "\n".join(AP.pack(cell(), spec, [], {}, AP.settings(None), "2026-09-25 15:30"))
        self.assertIn("- Risk manager: VETO - the hourly report is not available", veto)
        self.assertIn("No veto is never a reason to say yes", text)
        self.assertEqual(B.lint(text), [], "no profit promise, no win probability")

    def test_write_packs_passes_the_report_on(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        import research
        c = dict(cell(), strategy="S6-OB-FVG", version="1.0", tf="15m")
        spec = test_brain.Approval().spec()
        reg = dict(versions={}, cells={})
        with mock.patch.object(scanner, "REPORTS", tmp):
            out = research.write_packs({"S6-OB-FVG@1.0|15m": c}, ["S6-OB-FVG@1.0|15m"], {"S6-OB-FVG@1.0": spec},
                                       reg, AP.settings(None), "2026-09-25 15:30", True, report(),
                                       NOW.replace(hour=15, minute=30))
            text = test_brain.read(os.path.join(tmp, "approval_offline", "S6-OB-FVG_v1.0_15m.md"))
        self.assertTrue(out[0]["risk"].startswith("Risk manager: VETO - "), "WEAK_BULL: no coin in it on 1H")
        self.assertIn(out[0]["risk"], text)
        self.assertIsNone(research.hourly_report(True), "offline tests never read a live report")

    def test_briefing_fact_sheet(self):
        now = NOW.replace(hour=15, minute=30)
        rep = report(signals=[], validation_signals=[dict(coin="BTC", direction="long", timeframe="15m",
                                                          strategy="S6-OB-FVG", version="1.0", stage="PAPER")],
                     watching=[])
        res = {"cells": {"S6-OB-FVG@1.0|15m": dict(cell(), strategy="S6-OB-FVG", tf="15m")}}
        text = "\n".join(brain_pack.debate_lines(rep, res, now))
        self.assertIn("- whole market: Risk manager: no veto", text)
        self.assertIn("  - Bull case: 1D WEAK_BULL (ADX 44 = strong trend); 4H STRONG_BULL", text)
        self.assertIn("  - SHORT: Risk manager: VETO - BTC regime: LONG allowed", text)
        self.assertIn("- signal BTC LONG 15m S6-OB-FVG (PAPER):", text)
        self.assertIn("  - Bull case: unseen part of the backtest", text)
        empty = "\n".join(brain_pack.debate_lines(report(), {}, now))
        self.assertIn("- no signal or watched setup this run", empty)


class BriefingGuard(unittest.TestCase):
    P = "reports/claude/briefings/2026-09-26-0820.md"

    def review(self, text):
        return B.review([test_brain.change(self.P, "A", None, text)], {self.P: None})

    def test_briefing_needs_the_three_lines(self):
        head = "# BTC holds\n## Summary\nquiet\n" + test_brain.EMAIL["briefings"]
        self.assertEqual(self.review(head + test_brain.DEBATE)[1], [])
        self.assertIn("no '## Bull vs bear' section", "\n".join(self.review(head)[1]))
        probs = "\n".join(self.review(head + "## Bull vs bear\n- Bull case: x 1\n- Bear case: y 2\n")[1])
        self.assertIn("'Risk manager:'", probs)
        probs = "\n".join(self.review(head + "## Bull vs bear\n- Bull case: 1\n- Bear case: 2\n"
                                      "- Risk manager: looks fine to me\n")[1])
        self.assertIn("must say VETO", probs)
        ok = head + "## Bull vs bear\n**Bull case:** 1D WEAK_BULL\n**Bear case:** 1H RANGE\n" \
                    "**Risk manager:** VETO - US CPI at 12:30 UTC\n## News\nx\n"
        self.assertEqual(self.review(ok)[1], [], "bold labels are fine")
        # the daily review and the weekly research are not briefings
        p = "reports/claude/daily/2026-09-26.md"
        self.assertEqual(B.review([test_brain.change(p, "A", None, "# D\n" + test_brain.EMAIL["daily"])], {p: None})[1],
                         [])


class ReferenceProjects(unittest.TestCase):
    """R1-R8 in memory/curriculum.md: the weekly research studies one a week."""

    def test_curriculum_file(self):
        text = test_brain.read(os.path.join(ROOT, "memory", "curriculum.md"))
        proj = CU.parse_projects(text)
        self.assertEqual([p["id"] for p in proj], [f"R{i}" for i in range(1, 9)])
        self.assertTrue(all(any(ln.startswith("- licence:") for ln in p["lines"]) for p in proj))
        plan = CU.parse_plan(text)
        self.assertEqual(len(plan), 24, "the daily reading plan is unchanged")
        self.assertFalse(any("Reference projects" in ln for ln in plan[-1]["lines"]), "a heading ends an item")
        self.assertIn("GPL-3.0 - ideas only", "\n".join(proj[2]["lines"]))

    def test_studied_and_next(self):
        src = ("### [R1] RD-Agent\n- timestamp: 2026-09-25 16:00 UTC · x\n"
               "### [C01] Momentum\n- timestamp: 2026-09-26 15:30 UTC · x\n")
        done = CU.studied(src)
        self.assertEqual(done, {"R1": "2026-09-25 16:00 UTC", "C01": "2026-09-26 15:30 UTC"})
        text = test_brain.read(os.path.join(ROOT, "memory", "curriculum.md"))
        self.assertEqual(CU.next_item(CU.parse_projects(text), done)["id"], "R2")
        self.assertEqual(CU.next_item(CU.parse_plan(text), done)["id"], "C02", "R items do not move the daily plan")

    def test_build_records_exist_and_weekly_sheet_names_the_next(self):
        src = test_brain.read(os.path.join(ROOT, "memory", "research_sources.md"))
        done = CU.studied(src)
        for r in ("R1", "R2", "R8"):                       # opened before integrating (Part A uses R1, R2, R8)
            self.assertIn(r, done)
        recs = {}                        # the build session's record = the FIRST one per project (later re-checks append)
        for x in B.mem.parse(src):
            if x["title"].startswith("[R"):
                recs.setdefault(x["title"][:4], x)
        for r in ("[R1]", "[R2]", "[R8]"):
            self.assertRegex(recs[r]["source"], r"commit [0-9a-f]{40}")
        blocks = ["\n### " + blk for blk in ("\n" + src).split("\n### ")[1:]]
        mine = "".join(next(x for x in blocks if x.startswith("\n### " + r["title"] + "\n")) for r in recs.values())
        self.assertEqual(B.check_records(mine, "memory/research_sources.md"), [],
                         "the build session's records pass the guard's own record rules")
        rec = test_brain.rec("[R1] Microsoft RD-Agent - re-check", ev="RESEARCH_FINDING: release notes, 1 source") \
            .replace("source: Claude daily review", "source: https://github.com/microsoft/RD-Agent (commit 484776c, 2026-09-23)")
        probs = B.check_records(rec, "memory/research_sources.md")
        self.assertTrue(any("full 40-character commit" in x for x in probs), probs)           # a short hash: refused
        full = rec.replace("commit 484776c", "commit " + "4" * 40)
        self.assertFalse([x for x in B.check_records(full, "memory/research_sources.md") if "commit" in x])
        self.assertFalse([x for x in B.check_records(test_brain.rec("[C04] a paper"), "memory/research_sources.md")
                          if "commit" in x], "only reference projects need a commit")
        text = "\n".join(brain_pack.project_lines())
        nxt = CU.next_item(CU.parse_projects(test_brain.read(os.path.join(ROOT, "memory", "curriculum.md"))), done)
        todo = [x for x in CU.parse_projects(test_brain.read(os.path.join(ROOT, "memory", "curriculum.md")))
                if x["id"] not in done]
        self.assertEqual(nxt["id"], todo[0]["id"] if todo else min(done, key=lambda k: (done[k], k)),
                         "the first project not studied yet, else the one studied longest ago")
        self.assertIn(f"- {nxt['id']}: {nxt['title']}", text)
        self.assertIn("what we deliberately do NOT take", text)


class Tasks(unittest.TestCase):
    def test_task_files_ask_for_it(self):
        read = lambda n: test_brain.read(os.path.join(ROOT, "tasks", n))
        self.assertIn("## Bull vs bear", read("briefing.md"))
        self.assertIn("Feedback: <id>@<version>", read("daily_review.md"))
        self.assertIn("parent", read("COMMON.md"))
        w = read("weekly_research.md")
        self.assertIn("reference project", w.lower())
        self.assertIn("Idea chains", w)


if __name__ == "__main__":
    unittest.main()
