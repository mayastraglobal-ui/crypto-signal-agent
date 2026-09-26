"""Phase 17 part A tests: the strategy lab (strategies_lab.yaml), its Brain guard checks, lab cards in research and
the scan (never APPROVED, never emailed), the trials counter and the rising pass bar, and the task instructions.

Run:  python -m unittest test_lab -v      (from tests/)
"""
import copy
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brain_pack  # noqa: E402
import research  # noqa: E402
import scanner  # noqa: E402
import test_brain  # noqa: E402
from engine import approval as AP  # noqa: E402
from engine import brain as B  # noqa: E402
from engine import data_quality as dq  # noqa: E402
from engine import digest as D  # noqa: E402
from engine import lifecycle as LC  # noqa: E402
from engine import memory as mem  # noqa: E402
from engine import regime as rg  # noqa: E402
from engine import strategy_spec as SS  # noqa: E402
from engine import timeframes as tfm  # noqa: E402
from engine import trials as T  # noqa: E402

UTC = dt.timezone.utc
read = test_brain.read
NOW = dt.datetime(2026, 9, 25, 16, 0, tzinfo=UTC)
LIB = yaml.safe_load(read(os.path.join(ROOT, "strategies.yaml")))
LIB_TEXT = read(os.path.join(ROOT, "strategies.yaml"))
LAB_HEAD = read(os.path.join(ROOT, "strategies_lab.yaml"))
CFG = yaml.safe_load(read(os.path.join(ROOT, "config.yaml")))


def lib(sid):
    return copy.deepcopy(next(c for c in LIB if c["id"] == sid))


def v11(**over):
    """trend_pullback v1.1: exactly one change (targets 2R / 3R) - a valid lab card."""
    c = lib("trend_pullback")
    c.update(version="1.1", evidence_class="HYPOTHESIS", added=str(NOW.date()), factory="failure",
             parent="result: trend_pullback@1.0 1h",
             factory_evidence="bad_target in 41% of losses, n=64 (trend_pullback v1.0 1h)",
             targets={"long": ["2R", "3R"], "short": ["2R", "3R"], "split": [0.5, 0.5]},
             changelog=["1.1 (2026-09-25): targets 2R / 3R instead of the config default."])
    c.update(over)
    return c


def smc_pair(added=None):
    """A new SMC idea + its control twin (the same idea without the sweep)."""
    added = added or str(NOW.date())
    base = dict(status="FORMALIZED", family="smc", gate="trend", regimes=["STRONG_BULL", "WEAK_BULL"],
                source="ICT material", evidence_class="CLAIM", added=added, timeframes=["1h"], factory="missed_move",
                factory_evidence="BTC up 6x ATR on 2026-09-20 - no strategy had a setup",
                stop={"method": "atr", "atr": 1.5}, targets={"long": ["2R"], "short": ["2R"], "split": [1.0]},
                time_stop_bars=20, known_weaknesses="untested", changelog=["1.0 (2026-09-25): first version."])
    card = dict(base, id="LAB-SWEEP-RSI", version="1.0", hypothesis="A sweep with RSI reset continues.",
                parent="missed_move: BTC up 6x ATR on 2026-09-20",
                edge=dict(type="forced_flow", works_in=["STRONG_BULL", "WEAK_BULL"],
                          who_pays="traders stopped out below the swept low", mechanism="forced selling ends after the "
                          "sweep and momentum turns up", fails_when="strong down-trends that keep sweeping lows",
                          kill_rule="unseen-data average below 0R or it no longer beats its control twin"),
                long=["bars_since(smc_sweep_bull) <= 5", "rsi(close,14) > 50"],
                short=["bars_since(smc_sweep_bear) <= 5", "rsi(close,14) < 50"], control_twin="LAB-SWEEP-RSI-noSMC")
    twin = dict(base, id="LAB-SWEEP-RSI-noSMC", version="1.0", hypothesis="Control: RSI alone.",
                long=["rsi(close,14) > 50"], short=["rsi(close,14) < 50"], twin_of="LAB-SWEEP-RSI")
    return card, twin


class _NoAliases(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def dump(cards):
    return yaml.dump(cards, Dumper=_NoAliases, sort_keys=False, allow_unicode=True)


def plain(i=0, **over):
    """A new plain indicator card (no special ingredient, so no twin)."""
    c, _ = smc_pair()
    c = dict(c, id=f"LAB-PLAIN-{i}", long=["rsi(close,14) > 50"], short=["rsi(close,14) < 50"], control_twin=None)
    c.update(over)
    return c


def lab_change(new_cards, base=LAB_HEAD):
    return dict(path=SS.LAB_FILE, status="M", base=base, new=base + dump(new_cards))


BIG = {f: 99 for f in SS.FACTORIES}          # factory quotas out of the way (tested on their own in test_ideas.py)


def review(new_cards, base=LAB_HEAD, current=None, branch="claude/brain-weekly", now=NOW, quota=BIG):
    return B.review([lab_change(new_cards, base)], {SS.LAB_FILE: base if current is None else current,
                                                   SS.LIBRARY_FILE: LIB_TEXT}, now, branch, quota)


class BuildingBlocks(unittest.TestCase):
    """Lab rules are run by the engine, so they may only use the engine's own building blocks."""

    @classmethod
    def setUpClass(cls):
        feed, now = scanner.Synthetic(), int(time.time() * 1000)
        data, q = {}, {}
        for tf in ["1w", "1d"] + tfm.TRADE_ORDER:
            df, rep = dq.check_candles(feed.klines("BTCUSDT", tf, 1500), scanner.TF_MS[tf], now,
                                       dq.settings(CFG.get("data_quality")))
            data[("BTCUSDT", tf)], q[("BTC", tf)] = df, rep
        cls.pc = scanner.prepare_coin("BTCUSDT", "BTC", data, q, tfm.TRADE_ORDER, CFG)

    def test_lists_match_the_engines_real_namespace(self):
        for tf, fr in self.pc["frames"].items():
            names = set(fr["ns"]) - {"np"}                   # numpy stays out of reach of lab rules
            want = SS.FUNCTIONS | SS.COLUMNS | (SS.H4_COLUMNS if tf in SS.H4_TFS else set())
            self.assertEqual(names, want, tf)

    def test_every_library_rule_passes_and_a_passing_rule_really_runs(self):
        for c in LIB:
            r = SS.render(c)
            for k in ("long", "short", "exit_long", "exit_short"):
                for rule in r.get(k) or []:
                    self.assertEqual(SS.expr_problems(rule, c["timeframes"]), [], (c["id"], rule))
                    for tf in c["timeframes"]:
                        fr = self.pc["frames"][tf]
                        scanner.eval_rules([rule], fr["ns"], fr["df"].index)       # no error

    def test_anything_else_is_refused(self):
        bad = ["().__class__", "close.shift(1) > close", "close[0] > 1", "(lambda: 1)()", "'a' == 'a'",
               "close ** 2 > 1", "__import__('os').system('true')", "np.log(close) > 1", "foo(close) > 1",
               "[x for x in (1, 2)]", "ema > 1", "open(close)", "exec('1')", "close if True else open",
               "(y := 1)", "{1: 2}", "close >", "True"]
        for rule in bad:
            self.assertTrue(SS.expr_problems(rule, ["1h"]), rule)
        self.assertTrue(SS.expr_problems("h4_range_low < close", ["4h"]))          # h4_* only below 4H
        self.assertEqual(SS.expr_problems("h4_range_low < close", ["1h", "15m"]), [])
        self.assertEqual(SS.expr_problems("cross_up(ema(close,9), ema(close,21)) & (rel_vol > 1.5) | ~htf_down",
                                          ["1h"]), [])

    def test_an_unsafe_lab_card_never_reaches_eval(self):
        c = v11(long=["__import__('os').system('touch pwned')"])
        ok, problems, _, _ = SS.load_library(LIB, [c], rg.LABELS, tfm.TRADE_ORDER)
        self.assertNotIn("trend_pullback@1.1", {SS.key(x) for x in ok})
        self.assertIn("lab: trend_pullback", problems)


class CardRules(unittest.TestCase):
    def others(self, *extra):
        out = {c["id"]: c for c in LIB}
        out.update({c["id"]: c for c in extra})
        return out

    def problems(self, card, *extra):
        o = {k: v for k, v in self.others(*extra).items() if k != card["id"]}
        return SS.lab_card_problems(card, o, rg.LABELS, tfm.TRADE_ORDER)

    def test_a_good_card_and_a_good_smc_pair(self):
        self.assertEqual(self.problems(v11()), [])
        card, twin = smc_pair()
        self.assertEqual(self.problems(card, twin), [])
        self.assertEqual(self.problems(twin, card), [])

    def test_first_target_at_least_2r(self):
        for tg, ok in [(None, False), ({"long": ["1R", "3R"], "short": ["1R", "3R"], "split": [0.5, 0.5]}, False),
                       ({"long": ["1.9R"], "short": ["1.9R"], "split": [1.0]}, False),
                       ({"long": ["max(1R, smc_liq_above)"], "short": ["max(1R, smc_liq_below)"], "split": [1.0]}, False),
                       ({"long": ["smc_liq_above"], "short": ["smc_liq_below"], "split": [1.0],
                         "need": {"long": "smc_liq_above", "short": "smc_liq_below", "min_r": 1.0}}, False),
                       ({"long": ["smc_liq_above"], "short": ["smc_liq_below"], "split": [1.0]}, False),
                       ({"long": ["2R"], "short": ["2R"], "split": [1.0]}, True),
                       ({"long": ["max(2R, smc_liq_above)"], "short": ["max(2R, smc_liq_below)"], "split": [1.0]}, True),
                       ({"long": ["smc_liq_above"], "short": ["smc_liq_below"], "split": [1.0],
                         "need": {"long": "smc_liq_above", "short": "smc_liq_below", "min_r": 2.0}}, True),
                       ({"long": ["2R"], "short": ["1R"], "split": [1.0]}, False)]:
            c = v11(targets=tg) if tg else {k: v for k, v in v11().items() if k != "targets"}
            p = [x for x in self.problems(c) if "target" in x]
            self.assertEqual(not p, ok, (tg, p))

    def test_source_evidence_and_changelog(self):
        self.assertTrue(self.problems(v11(evidence_class=None)))
        self.assertTrue(self.problems(v11(evidence_class="GOSSIP")))
        self.assertEqual(self.problems(v11(evidence_class="CLAIM: a blog post")), [])
        self.assertTrue(self.problems(v11(source="")))
        self.assertTrue(self.problems(v11(changelog=[])))
        self.assertTrue(self.problems(v11(changelog=["1.0 (2026-09-24): old line only"])))

    def test_control_twin_rules(self):
        card, twin = smc_pair()
        self.assertIn("needs control_twin", " ".join(self.problems(dict(card, control_twin=None))))
        self.assertIn("is not in", " ".join(self.problems(card)))                      # twin missing
        self.assertIn("twin_of", " ".join(self.problems(card, dict(twin, twin_of=None))))
        same = dict(twin, long=card["long"], short=card["short"])                       # keeps the ingredient
        self.assertIn("WITHOUT", " ".join(self.problems(card, same)))
        five = dict(v11(), id="LAB-5M", version="1.0", timeframes=["15m"], confirm_5m=True, control_twin=None,
                    changelog=["1.0: first"])
        self.assertIn("control_twin", " ".join(self.problems(five)))
        self.assertIsNone(SS.special(v11()))                                           # plain indicators: no twin

    def test_one_change_per_version(self):
        self.assertEqual(SS.version_problems(v11(), LIB), [])
        card, twin = smc_pair()
        self.assertEqual(SS.version_problems(card, LIB), [])                           # a new id
        self.assertIn("already exists", SS.version_problems(lib("trend_pullback"), LIB)[0])
        self.assertIn("higher", SS.version_problems(v11(version="0.9"), LIB)[0])
        two = v11(time_stop_bars=40)
        self.assertIn("changes 2", SS.version_problems(two, LIB)[0])
        none = dict(lib("trend_pullback"), version="1.1")
        self.assertIn("changes 0", SS.version_problems(none, LIB)[0])
        p = dict(lib("trend_pullback"), version="1.1", params=dict(lib("trend_pullback")["params"], fast=21))
        self.assertEqual(SS.version_problems(p, LIB), [])                              # one parameter
        p2 = dict(p, params=dict(p["params"], slow=55))
        self.assertIn("changes 2", SS.version_problems(p2, LIB)[0])
        r = lib("trend_pullback")                                                     # a rule + its new parameter
        r.update(version="1.1", long=r["long"] + ["rel_vol > {rv}"], short=r["short"] + ["rel_vol > {rv}"],
                 params=dict(r["params"], rv=1.5))
        self.assertEqual(SS.version_problems(r, LIB), [])
        self.assertEqual(SS.version_problems(dict(v11(), version="1.2", time_stop_bars=40), LIB + [v11()]), [])


class Guard(unittest.TestCase):
    def test_accepted_and_applied_at_the_end(self):
        applies, probs, _ = review([v11()])
        self.assertEqual(probs, [])
        self.assertEqual(applies[0]["path"], SS.LAB_FILE)
        card, twin = smc_pair()
        applies, probs, _ = review([card, twin])                    # the twin may come in the same push
        self.assertEqual(probs, [])
        merged = B.apply_text(LAB_HEAD, applies[0])
        self.assertEqual([c["id"] for c in yaml.safe_load(merged)], [card["id"], twin["id"]])

    def assertRefused(self, why, *a, **k):
        applies, probs, _ = review(*a, **k)
        self.assertEqual(applies, [])
        self.assertIn(why, " | ".join(probs))

    def test_refusals(self):
        self.assertRefused("FORMALIZED", [v11(status="IDEA")])
        self.assertRefused("added must be today", [v11(added="2026-09-20")])
        self.assertRefused("added must be today", [v11(added=None)])
        self.assertRefused("first long target", [v11(targets={"long": ["1R"], "short": ["2R"], "split": [1.0]})])
        self.assertRefused("exactly ONE", [v11(time_stop_bars=40)])
        self.assertRefused("already exists", [lib("trend_pullback") | {"evidence_class": "HYPOTHESIS",
                                                                           "added": str(NOW.date())}])
        self.assertRefused("not allowed", [plain(long=["close.shift(1) > open"])])
        self.assertRefused("unknown building block", [plain(short=["rsi(close,14) < level"])])
        self.assertRefused("only the daily review and the weekly research", [v11()], branch="claude/brain-briefing")
        self.assertRefused("win probability", [v11(hypothesis="A 90% chance to win on this setup.")])
        self.assertRefused("not a strategy card", ["just text"])
        base = LAB_HEAD + dump([v11()])
        for new in (LAB_HEAD, base.replace("targets 2R / 3R", "targets") + dump([smc_pair()[1]])):   # delete / edit
            applies, probs, _ = B.review([dict(path=SS.LAB_FILE, status="M", base=base, new=new)],
                                         {SS.LAB_FILE: base, SS.LIBRARY_FILE: LIB_TEXT}, NOW, "claude/brain-daily")
            self.assertEqual(applies, [])
            self.assertIn("lab cards are only added", " ".join(probs))
        applies, probs, _ = B.review([dict(path=SS.LAB_FILE, status="D", base=base, new=None)],
                                     {SS.LAB_FILE: base, SS.LIBRARY_FILE: LIB_TEXT}, NOW, "claude/brain-daily")
        self.assertEqual(applies, [])
        self.assertTrue(probs)

    def test_an_edit_disguised_as_an_addition(self):
        """Text only added at the end, but indented so it becomes part of the last card: still an edit."""
        base = LAB_HEAD + dump([v11()])
        applies, probs, _ = B.review([dict(path=SS.LAB_FILE, status="M", base=base, new=base + "  cooldown_bars: 5\n")],
                                     {SS.LAB_FILE: base, SS.LIBRARY_FILE: LIB_TEXT}, NOW, "claude/brain-daily")
        self.assertEqual(applies, [])
        self.assertIn("earlier cards changed", " ".join(probs))

    def test_a_broken_file_on_main_is_not_made_worse(self):
        self.assertRefused("does not fit the newest lab file", [plain()], current=LAB_HEAD + "- id: [\n")

    def test_refusals_on_bad_yaml(self):
        applies, probs, _ = B.review([dict(path=SS.LAB_FILE, status="M", base=LAB_HEAD, new=LAB_HEAD + "- id: [\n")],
                                     {SS.LAB_FILE: LAB_HEAD, SS.LIBRARY_FILE: LIB_TEXT}, NOW, "claude/brain-weekly")
        self.assertIn("not a valid card list", " ".join(probs))

    def test_day_and_week_limits(self):
        cards = [plain(i) for i in range(4)]
        self.assertEqual(review(cards[:3])[1], [])
        self.assertRefused("at most 3 a day", cards)
        # 3 already on main today + 1 more -> refused; yesterday's cards count for the week
        on_main = LAB_HEAD + dump(cards[:3])
        self.assertRefused("at most 3 a day", [dict(cards[3], id="LAB-X")], base=on_main)
        week = []
        for d in range(1, 7):
            for j in range(2):
                c = dict(cards[0], id=f"LAB-W{d}-{j}", added=str(NOW.date() - dt.timedelta(days=d)))
                week.append(c)
        base = LAB_HEAD + dump(week[:9])          # 9 cards in the last 6 days
        self.assertEqual(review([dict(cards[0], id="LAB-NEW-1")], base=base)[1], [])
        self.assertRefused("at most 10", [dict(cards[0], id="LAB-NEW-1"), dict(cards[0], id="LAB-NEW-2")], base=base)
        old = LAB_HEAD + dump([dict(c, added="2026-09-01") for c in week])             # older than 7 days: free
        self.assertEqual(review(cards[:3], base=old)[1], [])

    def test_fits_the_newest_main_and_reruns_are_skipped(self):
        plain = globals()["plain"]("X")
        # the other task appended the SAME new id meanwhile -> refused (a card is never written twice)
        self.assertRefused("already exists", [plain], current=LAB_HEAD + dump([plain | {"source": "other task"}]))
        # the other task appended a different card meanwhile -> both kept, ours goes after it
        other = dict(plain, id="LAB-OTHER")
        applies, probs, _ = review([plain], current=LAB_HEAD + dump([other]))
        self.assertEqual(probs, [])
        merged = yaml.safe_load(B.apply_text(LAB_HEAD + dump([other]), applies[0]))
        self.assertEqual([x["id"] for x in merged], ["LAB-OTHER", "LAB-PLAIN-X"])
        applies, probs, skipped = review([plain], current=LAB_HEAD + dump([plain]))
        self.assertEqual((applies, probs, skipped), ([], [], [SS.LAB_FILE]))

    def test_library_edits_still_go_through_the_operator(self):
        applies, probs, _ = B.review([dict(path="strategies.yaml", status="M", base="a\n", new="a\nb\n")],
                                     {"strategies.yaml": "a\n"}, NOW, "claude/brain-weekly")
        self.assertIn(SS.LAB_FILE, probs[0])
        self.assertIn("pull request", probs[0])


class GuardOnGit(unittest.TestCase):
    """brain_guard.py end to end with a lab push (git, throw-away repositories)."""
    setUp = test_brain.GuardOnGit.setUp
    write = test_brain.GuardOnGit.write
    push_task = test_brain.GuardOnGit.push_task
    guard = test_brain.GuardOnGit.guard

    def test_lab_push_applied_then_a_bad_one_refused(self):
        for f in ("strategies.yaml", "strategies_lab.yaml"):
            shutil.copy(os.path.join(ROOT, f), os.path.join(self.main, f))
        test_brain.git(self.main, "add", "-A")
        test_brain.git(self.main, "commit", "-qm", "library")
        test_brain.git(self.main, "push", "-q", "origin", "main")
        today = dt.datetime.now(UTC).date()
        good = v11(added=str(today))
        self.push_task("claude/brain-daily", {"reports/claude/daily/2026-09-25.md": "# D\n## Summary\nok\n"
                                                                                    + test_brain.EMAIL["daily"]},
                       {"strategies_lab.yaml": dump([good])})
        res = self.guard()
        self.assertEqual(res[0]["status"], "applied", res[0]["problems"])
        lab = yaml.safe_load(test_brain.read(os.path.join(self.main, "strategies_lab.yaml")))
        self.assertEqual([SS.key(c) for c in lab], ["trend_pullback@1.1"])
        p = subprocess.run([sys.executable, "memory_guard.py"], cwd=self.main, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout)
        # the briefing may not add cards; a whole push is refused, main unchanged
        self.push_task("claude/brain-briefing", {}, {"strategies_lab.yaml": dump([v11(version="1.2", added=str(today),
                                                                                       time_stop_bars=40)])})
        res = self.guard()
        self.assertEqual(res[0]["status"], "rejected")
        self.assertEqual(len(yaml.safe_load(test_brain.read(os.path.join(self.main, "strategies_lab.yaml")))), 1)


class LabInTheEngine(unittest.TestCase):
    def test_moved_cards_and_the_lab_flag(self):
        card, twin = smc_pair()
        ok, problems, _, moved = SS.load_library(LIB, [v11(), card, twin], rg.LABELS, tfm.TRADE_ORDER)
        self.assertEqual(problems, {})
        keys = {SS.key(x): x for x in ok}
        self.assertTrue(keys["trend_pullback@1.1"]["lab"])
        self.assertFalse(keys["trend_pullback@1.0"].get("lab"))
        self.assertEqual(SS.fingerprint(keys["trend_pullback@1.1"]),
                         SS.fingerprint(SS.render(v11())), "the lab mark is not part of the rules")
        # the operator copied the card into strategies.yaml: that copy runs, the lab one is ignored
        lib2 = LIB + [{k: v for k, v in v11().items() if k != "added"}]
        ok, problems, _, moved = SS.load_library(lib2, [v11()], rg.LABELS, tfm.TRADE_ORDER)
        self.assertEqual(moved, ["trend_pullback@1.1"])
        self.assertFalse(next(x for x in ok if SS.key(x) == "trend_pullback@1.1").get("lab"))

    def test_a_broken_lab_file_never_stops_the_library(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        shutil.copy(os.path.join(ROOT, "strategies.yaml"), tmp)
        with open(os.path.join(tmp, SS.LAB_FILE), "w") as f:
            f.write("- id: [\n")
        with mock.patch.object(scanner, "ROOT", tmp):
            ok, problems, _, _ = scanner.load_cards()
        self.assertEqual(len(ok), len([c for c in LIB if c["status"] == "FORMALIZED"]))
        self.assertIn(SS.LAB_FILE, problems)
        os.remove(os.path.join(tmp, SS.LAB_FILE))
        with mock.patch.object(scanner, "ROOT", tmp):
            self.assertEqual(scanner.load_cards()[1], {})                   # no lab file: fine

    def test_never_approved(self):
        self.assertEqual(scanner.lab_status({"lab": True}, "APPROVED"), "PAPER_TRADING")
        self.assertEqual(scanner.lab_status({}, "APPROVED"), "APPROVED")
        listed = dict(date="2026-09-25")
        st, _, warn = AP.decide("PAPER_TRADING", listed, True, [], lab=True)
        self.assertEqual(st, "PAPER_TRADING")
        self.assertIn("strategies.yaml by pull request", warn)
        self.assertEqual(AP.decide("APPROVED", listed, True, [], lab=True)[0], "PAPER_TRADING")
        self.assertEqual(AP.decide("PAPER_TRADING", None, True, [], lab=True), ("PAPER_TRADING", "", None))
        self.assertEqual(AP.decide("PAPER_TRADING", listed, True, [])[0], "APPROVED")      # library unchanged
        for prev in (None, "BACKTESTING", "VALIDATION", "PAPER_TRADING", "APPROVED"):
            for ok in (True, False):
                self.assertNotEqual(AP.decide(prev, listed, ok, [], lab=True)[0], "APPROVED")

    def test_a_lab_plan_is_never_emailed(self):
        base = dict(stage="APPROVED", confirm_5m=False, no_trade=False)
        self.assertEqual(len(scanner.emailable_now([base, dict(base, lab=True), dict(base, stage="PAPER_TRADING"),
                                                    dict(base, confirm_5m=True), dict(base, no_trade=True)])), 1)

    def test_pack_of_a_lab_card_says_move_it_first(self):
        a = test_brain.Approval("test_pack_has_every_section_21_part_and_the_yes_line")
        lab = "\n".join(AP.pack(a.cell(), dict(a.spec(), lab=True), [], {}, AP.settings(None), "2026-10-04 00:50"))
        self.assertIn("This is a LAB card", lab)
        self.assertLess(lab.index("This is a LAB card"), lab.index("To say yes, add this"))
        plain = "\n".join(AP.pack(a.cell(), a.spec(), [], {}, AP.settings(None), "2026-10-04 00:50"))
        self.assertNotIn("LAB card", plain)


class Trials(unittest.TestCase):
    def test_bar_rises_with_the_number_of_trials(self):
        self.assertAlmostEqual(T.need_t(1, 0.05), 1.645, places=3)
        bars = [T.need_t(n, 0.05) for n in (1, 2, 10, 50, 100, 500, 1000)]
        self.assertEqual(bars, sorted(bars))
        self.assertLess(bars[0], bars[-1])
        self.assertAlmostEqual(T.need_t(100, 0.05), 3.29, places=2)
        self.assertEqual(T.need_t(0, 0.05), T.need_t(1, 0.05))

    def test_research_evidence_carries_the_t_statistic(self):
        rng = np.random.default_rng(3)
        per = {c: [dict(entry_time=i * 3_600_000 + k, r=float(rng.normal(0.1, 1)), oos=i >= 70, dir=1, bars=5,
                        cost_r=0.05) for i in range(100)] for k, c in enumerate(["BTC", "ETH"])}
        from engine import research as RS
        ev = RS.evaluate(per, per, {}, RS.windows(0, 100 * 3_600_000 + 10, 4), CFG["research"], 5)
        want = T.t_stat([t["r"] for tr in per.values() for t in tr])
        self.assertAlmostEqual(ev["t_stat"], want, places=3)
        self.assertIsNone(RS.evaluate({"BTC": []}, {}, {}, RS.windows(0, 10, 4), CFG["research"], 5)["t_stat"])

    def test_t_statistic(self):
        r = np.random.default_rng(1).normal(0.2, 1.0, 300)
        want = r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))
        self.assertAlmostEqual(T.t_stat(r), want, places=9)
        self.assertIsNone(T.t_stat([1.0]))
        self.assertIsNone(T.t_stat([0.5, 0.5, 0.5]))

    def test_file_rows_backfill_and_numbering(self):
        reg = LC.empty_registry()
        reg["versions"] = {"a@1.0": dict(id="a", version="1.0", experiment=2, first_tested_utc="2026-09-24 00:40"),
                           "b@1.0": dict(id="b", version="1.0", experiment=1, first_tested_utc="2026-09-23 00:40")}
        reg["cells"] = {"a@1.0|1h": {}, "a@1.0|4h": {}, "b@1.0|1h": {}}
        rows = T.number(T.backfill(reg), 0)
        self.assertEqual([T.key(r) for r in rows], ["b@1.0|1h", "a@1.0|1h", "a@1.0|4h"])
        self.assertEqual([r["trial"] for r in rows], [1, 2, 3])
        new = T.additions(rows, [("a", "1.0", "1h", "library"), ("c", "1.0", "1h", "lab"), ("c", "1.0", "1h", "lab")],
                          "2026-09-26 00:40")
        self.assertEqual([(T.key(r), r["trial"]) for r in new], [("c@1.0|1h", 4)])
        back = T.parse(T.to_csv(rows, True) + T.to_csv(new, False))
        self.assertEqual(len(back), 4)
        s = T.summary(back, 0.05, "2026-09-26")
        self.assertEqual((s["total"], s["new"], s["lab"]), (4, 1, 1))

    def test_research_writes_the_file_once_and_only_appends(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        path = os.path.join(tmp, "trials.csv")
        reg = LC.empty_registry()
        reg["versions"] = {"a@1.0": dict(id="a", version="1.0", experiment=1, first_tested_utc="2026-09-24")}
        reg["cells"] = {"a@1.0|1h": {}}
        with mock.patch.object(research, "TRIALS", path):
            rows, new = research.update_trials(reg, [("a", "1.0", "1h", "library"), ("x", "1.0", "4h", "lab")],
                                               "2026-09-25 00:40", False)
            self.assertEqual((len(rows), len(new)), (2, 1))
            with open(path) as f:
                first = f.read()
            rows, new = research.update_trials(reg, [("a", "1.0", "1h", "library"), ("y", "1.1", "1h", "lab")],
                                               "2026-09-26 00:40", False)
            self.assertEqual((len(rows), len(new)), (3, 1))
            with open(path) as f:
                text = f.read()
        self.assertTrue(text.startswith(first), "the file only grows")
        self.assertEqual(mem.append_only_problems(first, text), "")
        self.assertIn("memory/trials.csv", mem.APPEND_ONLY)
        self.assertIn("strategies_lab.yaml", mem.APPEND_ONLY)
        with open(os.path.join(ROOT, ".gitattributes")) as f:
            self.assertIn("memory/trials.csv merge=union", f.read())

    def test_paper_gate_needs_the_bar(self):
        ev = dict(walk_forward=dict(passed=True, positive=4, judged=5, pooled_avg_r=0.2), positive_coins=["a", "b", "c"],
                  stress=dict(avg_r=0.1), perturbation=dict(stable=True, worst=None), overfit=[], t_stat=2.5,
                  all=dict(n=100, avg_r=0.2), validate=dict(n=30, avg_r=0.2))
        R = CFG["research"]
        self.assertEqual(LC.paper_gate("VALIDATION", ev, None, R), (True, []))                  # no bar given
        self.assertTrue(LC.paper_gate("VALIDATION", ev, None, R, (T.need_t(5, 0.05), 5))[0])   # 2.5 >= 2.33
        ok, why = LC.paper_gate("VALIDATION", ev, None, R, (T.need_t(50, 0.05), 50))           # 2.5 < 3.09
        self.assertFalse(ok)
        self.assertIn("multiple-testing bar", why[0])
        self.assertFalse(LC.paper_gate("VALIDATION", dict(ev, t_stat=None), None, R, (1.0, 1))[0])
        self.assertEqual(CFG["research"]["trials_alpha"], 0.05)

    def test_weekly_email_shows_the_counter(self):
        rows = T.number([dict(strategy="a", version="1.0", tf="1h", first_tested_utc="2026-09-01 00:40", origin="library"),
                         dict(strategy="b", version="1.0", tf="1h", first_tested_utc="2026-09-26 00:40", origin="lab")], 0)
        board = [dict(strategy="b", version="1.0", tf="1h", status="BACKTESTING", lab=True, family="momentum")]
        w = D.weekly(dt.datetime(2026, 9, 27, 4, 0, tzinfo=UTC), test_brain.log_rows([]), board, {}, "", None, "x",
                     T.to_csv(rows, True), 0.05)
        text = "\n".join(w["lines"])
        self.assertIn("Trials counter: 2 strategy / version / timeframe tests so far (1 new this week, 1 of them "
                      "from the lab)", text)
        self.assertIn(f">= {T.need_t(2, 0.05):.2f}", text)
        self.assertIn("Strategy lab", text)
        w2 = D.weekly(dt.datetime(2026, 9, 27, 4, 0, tzinfo=UTC), test_brain.log_rows([]), [], {}, "", None, "x")
        self.assertIn("starts with the next daily research run", "\n".join(w2["lines"]))

    def test_fact_sheet_lab_part(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        shutil.copy(os.path.join(ROOT, "strategies.yaml"), tmp)
        with open(os.path.join(tmp, SS.LAB_FILE), "w") as f:
            f.write(LAB_HEAD + dump([v11(), dict(v11(), version="1.2", added="2026-09-24", time_stop_bars=40)]))
        res = dict(trials=dict(total=60, need_t=3.14), cells={"trend_pullback@1.1|1h": dict(
            lab=True, status="BACKTESTING", t_stat=0.4, evidence=dict(all=dict(n=40, avg_r=0.05)))})
        with mock.patch.object(brain_pack, "ROOT", tmp):
            text = "\n".join(brain_pack.lab_lines(NOW, res))
        self.assertIn("added today: 1 of 3", text)
        self.assertIn("last 7 days: 2 of 10", text)
        self.assertIn("you may add at most 2 card(s) now", text)
        self.assertIn("trend_pullback v1.2 (lab)", text)
        self.assertIn("PAPER_TRADING needs t >= 3.14", text)
        self.assertIn("lab cell trend_pullback@1.1|1h: BACKTESTING", text)


class Tasks(unittest.TestCase):
    def test_instructions_point_to_the_lab(self):
        common = read(os.path.join(ROOT, "tasks", "COMMON.md"))
        weekly = read(os.path.join(ROOT, "tasks", "weekly_research.md"))
        daily = read(os.path.join(ROOT, "tasks", "daily_review.md"))
        for text in (common, weekly, daily):
            self.assertIn("strategies_lab.yaml", text)
            self.assertNotIn("PROPOSED", text)
        self.assertIn("## Candidates (added to the lab)", weekly)
        self.assertIn("2R", common)
        self.assertIn(f"{B.LAB_PER_DAY} new cards per UTC day and {B.LAB_PER_WEEK} per 7 days", common)
        self.assertEqual(B.LAB_BRANCHES, ["claude/brain-daily", "claude/brain-weekly"])

    def test_lab_file_is_a_valid_empty_card_list(self):
        self.assertEqual(B._cards(LAB_HEAD), [])
        ok, problems, _, _ = scanner.load_cards()
        self.assertFalse([k for k in problems if k.startswith("lab") or k == SS.LAB_FILE], problems)


class EndToEnd(unittest.TestCase):
    """scan -> research -> scan offline with a lab card: tested like the library, counted as trials, shown as lab,
    and even when forced to APPROVED (with the operator's line in config.yaml) it stays in paper and emails nothing."""

    def test_lab_card_through_the_engine(self):
        from test_data_quality import run_copy
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        p = run_copy(tmp, "scanner.py", "--offline", "--coins", "3")        # the first scan: library only
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        with open(os.path.join(tmp, SS.LAB_FILE), "w") as f:                # then the daily review adds a card
            f.write(LAB_HEAD + dump([v11()]))
        shutil.copy(os.path.join(ROOT, "research.py"), tmp)
        run = lambda s: subprocess.run([sys.executable, s, "--offline", "--coins", "3"], cwd=tmp, capture_output=True,
                                       text=True, timeout=900)
        p = run("research.py")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        res = json.loads(read(os.path.join(tmp, "reports", "research_offline.json")))
        self.assertEqual(res["not_run"], {})
        self.assertEqual(res["lab"]["cards"], ["trend_pullback@1.1"])
        lab_cells = {k: c for k, c in res["cells"].items() if c["lab"]}
        self.assertEqual(sorted(lab_cells), sorted(f"trend_pullback@1.1|{tf}" for tf in v11()["timeframes"]))
        for k, c in lab_cells.items():                                   # the same tests as the library
            for part in ("walk_forward", "stress", "perturbation", "positive_coins", "overfit"):
                self.assertIn(part, c["evidence"], k)
            self.assertEqual(len(c["evidence"]["perturbation"]["variants"]), 18)
        rows = T.parse(read(os.path.join(tmp, "reports", "trials_offline.csv")))
        self.assertEqual(len(rows), len(res["cells"]))
        self.assertEqual(sum(r["origin"] == "lab" for r in rows), len(lab_cells))
        self.assertEqual(res["trials"]["total"], len(rows))
        self.assertAlmostEqual(res["trials"]["need_t"], T.need_t(len(rows), 0.05), places=3)
        for c in res["cells"].values():                                  # nobody reaches paper below the bar
            if c["status"] == "PAPER_TRADING":
                self.assertGreaterEqual(c["t_stat"], c["need_t"])
        self.assertFalse(os.path.exists(os.path.join(tmp, "memory")))    # offline never writes memory/
        pb = read(os.path.join(tmp, "reports", "playbook_offline.md"))      # Phase 17 B: the regime playbook
        self.assertTrue(pb.startswith("# Regime playbook"))
        self.assertEqual(sorted(res["playbook"]), sorted(rg.LABELS))

        # force the lab cell to APPROVED and list it in config.yaml -> both runs keep it in paper
        reg_p = os.path.join(tmp, "reports", "strategy_registry_offline.csv")
        reg = pd.read_csv(reg_p, dtype={"version": str})
        reg.loc[(reg["id"] == "trend_pullback") & (reg["version"] == "1.1"), "status"] = "APPROVED"
        reg.to_csv(reg_p, index=False)
        cfg = yaml.safe_load(read(os.path.join(tmp, "config.yaml")))
        cfg["approvals"] = [dict(strategy="trend_pullback", version="1.1", tf=tf, date="2026-09-25")
                            for tf in v11()["timeframes"]]
        with open(os.path.join(tmp, "config.yaml"), "w") as f:
            yaml.safe_dump(cfg, f, sort_keys=False)
        p = run("scanner.py")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        out = json.loads(read(os.path.join(tmp, "reports", "latest.json")))
        rows_b = [b for b in out["strategy_scoreboard"] if b["lab"]]
        self.assertTrue(rows_b)
        self.assertEqual({b["status"] for b in rows_b}, {"PAPER_TRADING"})
        self.assertFalse([s for s in out["signals"] if s.get("lab") or s["strategy"] == "trend_pullback"
                          and s["version"] == "1.1"])
        md = read(os.path.join(tmp, "reports", "latest.md"))
        self.assertIn("trend_pullback 🧪 lab", md)
        self.assertIn("**Trials counter:**", md)
        p = run("research.py")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        res = json.loads(read(os.path.join(tmp, "reports", "research_offline.json")))
        self.assertFalse([k for k, c in res["cells"].items() if c["lab"] and c["status"] == "APPROVED"])
        self.assertTrue(any("never approved" in w for w in res["approval"]["warnings"]))
        self.assertEqual(len(T.parse(read(os.path.join(tmp, "reports", "trials_offline.csv")))),
                         res["trials"]["total"], "a second run adds no trial for cells already counted")


if __name__ == "__main__":
    unittest.main()
