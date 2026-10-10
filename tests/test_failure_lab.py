"""Failure Lab (2026-10-10): repair cards for the loss tags, and learning which repairs work."""
import datetime as dt
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import scanner as sc  # noqa: E402
from engine import failure_lab as flab  # noqa: E402
from engine import regime as rg  # noqa: E402
from engine import strategy_spec as sspec  # noqa: E402
from engine import weekly_review as wrv  # noqa: E402

TODAY = dt.date(2026, 10, 10)
S = flab.settings({})
_cards = None


def cards():
    global _cards
    if _cards is None:
        s, _, _, _ = sc.load_cards()
        _cards = {sspec.key(x): x for x in s}
    return _cards


def tag(losers=120, share=0.6, w=-0.3, wo=0.5, flag=True):
    return dict(losers=losers, loss_share=share, n_with=200, avg_r_with=w, avg_r_without=wo, flag=flag)


def cell(key="P01-BREAKOUT-V1@1.0", tf="4h", status="BACKTESTING", n=300, avg=0.08, val=0.05, gross=0.12, tags=None,
         by_regime=None):
    sid, ver = key.split("@")
    return dict(strategy=sid, version=ver, tf=tf, status=status,
                evidence=dict(all=dict(n=n, avg_r=avg), validate=dict(n=n // 3, avg_r=val)),
                attribution=dict(gross_avg_r=gross, tags=tags if tags is not None else {"false_breakout": tag()},
                                 by_regime=by_regime or {}))


def cells_of(*cs):
    return {f"{c['strategy']}@{c['version']}|{c['tf']}": c for c in cs}


class Candidates(unittest.TestCase):
    def test_only_tags_that_hurt_with_enough_losers(self):
        cs = cells_of(cell(tags={"false_breakout": tag(), "stop_too_tight": tag(losers=10),
                                 "low_relative_volume": tag(w=0.4, wo=0.1),           # the tag HELPS: no repair
                                 "volatility_spike": tag()}))                          # no repair for it
        got = [t for _, _, t in flab.candidates(cs, cards(), S)]
        self.assertEqual(got, ["false_breakout"])

    def test_failed_cells_only_as_near_misses(self):
        near = cell(status="FAILED", avg=-0.02, gross=0.05)
        dead = cell(key="P02-EMA-PULLBACK-V1@1.0", status="FAILED", avg=-0.2, gross=-0.1)
        got = {c["strategy"] for c, _, _ in flab.candidates(cells_of(near, dead), cards(), S)}
        self.assertEqual(got, {"P01-BREAKOUT-V1"})
        few = cell(n=50)
        self.assertEqual(flab.candidates(cells_of(few), cards(), S), [])               # under 100 trades


class Cards(unittest.TestCase):
    def test_a_repair_is_a_valid_one_change_lab_card(self):
        out, considered = flab.cards_for(cells_of(cell()), cards(), TODAY, 3, rg.LABELS, sc.TF_ORDER, {}, S)
        self.assertEqual(considered, 1)
        self.assertEqual(len(out), 1)
        c = out[0]
        self.assertEqual(c["id"], "P01-BREAKOUT-V1-FDISP")
        self.assertEqual((c["factory"], c["status"], c["version"], c["added"]), ("failure", "FORMALIZED", "1.0", str(TODAY)))
        self.assertEqual(c["repair"], dict(tag="false_breakout", kind="DISP", tf="4h",
                                           parent_cell="P01-BREAKOUT-V1@1.0|4h"))
        self.assertIn("within(displacement_up, 3)", c["long"])
        self.assertIn("n=120", c["factory_evidence"])
        others = {x["id"]: x for x in cards().values()}
        self.assertEqual(sspec.lab_card_problems(c, others, rg.LABELS, sc.TF_ORDER), [])
        self.assertEqual(sspec.factory_problems(c, flab.LOSS_TAGS, engine=True), [])
        raw = {k: v for k, v in cards()["P01-BREAKOUT-V1@1.0"]["_raw"].items() if not k.startswith("_")}
        self.assertEqual(len(sspec.change_count(raw, c)), 1)

    def test_one_per_parent_quota_and_no_repeat(self):
        cs = cells_of(cell(tags={"false_breakout": tag(), "stop_too_tight": tag()}),
                      cell(key="P02-EMA-PULLBACK-V1@1.0", tags={"stop_too_tight": tag()}))
        out, _ = flab.cards_for(cs, cards(), TODAY, 5, rg.LABELS, sc.TF_ORDER, {}, S)
        self.assertEqual(sorted(c["variant_of"] for c in out), ["P01-BREAKOUT-V1@1.0", "P02-EMA-PULLBACK-V1@1.0"])
        self.assertEqual(len(flab.cards_for(cs, cards(), TODAY, 1, rg.LABELS, sc.TF_ORDER, {}, S)[0]), 1)
        self.assertEqual(flab.cards_for(cs, cards(), TODAY, 0, rg.LABELS, sc.TF_ORDER, {}, S)[0], [])
        again, _ = flab.cards_for(cs, cards(), TODAY, 5, rg.LABELS, sc.TF_ORDER, {}, S, existing=out)
        self.assertFalse({c["id"] for c in again} & {c["id"] for c in out})            # never the same repair twice

    def test_wider_stop_repair(self):
        cs = cells_of(cell(tags={"stop_too_tight": tag(w=-1.0, wo=0.3)}))
        c = flab.cards_for(cs, cards(), TODAY, 1, rg.LABELS, sc.TF_ORDER, {}, S)[0][0]
        self.assertEqual((c["id"], c["stop"]["atr"]), ("P01-BREAKOUT-V1-FWIDESTOP", 2.5))


class Learning(unittest.TestCase):
    def test_the_record_orders_and_retires_repairs(self):
        cs = cells_of(cell())
        board = {"DISP": dict(tried=4, helped=0, passed=0)}                            # never helped: stopped
        self.assertIsNone(flab.prior(board, "DISP", S))
        c = flab.cards_for(cs, cards(), TODAY, 1, rg.LABELS, sc.TF_ORDER, board, S)[0][0]
        self.assertEqual(c["repair"]["kind"], "RETEST")              # RVOL does not apply: the card has a volume rule
        board = {"DISP": dict(tried=3, helped=0, passed=0), "RETEST": dict(tried=3, helped=3, passed=1)}
        c = flab.cards_for(cs, cards(), TODAY, 1, rg.LABELS, sc.TF_ORDER, board, S)[0][0]
        self.assertEqual(c["repair"]["kind"], "RETEST")              # the repair that worked is tried first

    def test_results_compare_child_with_parent_and_keep_old_rows(self):
        parent = cell(avg=0.08, val=0.05)
        child = dict(cell(key="P01-BREAKOUT-V1-FDISP@1.0", avg=0.15, val=0.09), status="VALIDATION")
        card = dict(cards()["P01-BREAKOUT-V1@1.0"], id="P01-BREAKOUT-V1-FDISP", factory="failure",
                    repair=dict(tag="false_breakout", kind="DISP", tf="4h", parent_cell="P01-BREAKOUT-V1@1.0|4h"))
        waiting = dict(card, id="P01-BREAKOUT-V1-FRETEST", repair=dict(card["repair"], kind="RETEST"))
        cs = dict(cards(), **{"P01-BREAKOUT-V1-FDISP@1.0": card, "P01-BREAKOUT-V1-FRETEST@1.0": waiting})
        old = [dict(child="X-FADX@1.0|1h", parent="X@1.0|1h", tag="range_market", kind="ADX", helped=False,
                    passed=False, avg_r=0, parent_avg_r=0.1, test_r=0, parent_test_r=0.1, status="FAILED")]
        rows, pending = flab.results(cells_of(parent, child), cs, old, "2026-10-11 01:00")
        self.assertEqual(pending, ["P01-BREAKOUT-V1-FRETEST"])
        r = next(x for x in rows if x["kind"] == "DISP")
        self.assertTrue(r["helped"] and r["passed"])
        self.assertIn("X-FADX@1.0|1h", [x["child"] for x in rows])                    # a lesson is never lost
        by_kind, by_tag = flab.scoreboard(rows)
        self.assertEqual(by_kind["DISP"], dict(tried=1, helped=1, passed=1))
        self.assertEqual(by_tag["range_market"]["helped"], 0)
        worse = dict(child, evidence=dict(all=dict(n=300, avg_r=0.20), validate=dict(n=100, avg_r=0.01)))
        r2 = next(x for x in flab.results(cells_of(parent, worse), cs, [], "t")[0] if x["kind"] == "DISP")
        self.assertFalse(r2["helped"])                               # better overall but worse on the unseen part


class Review(unittest.TestCase):
    def test_weekly_review_shows_the_failure_lab(self):
        rows = [dict(child="A-FDISP@1.0|4h", parent="A@1.0|4h", tag="false_breakout", kind="DISP", helped=True,
                     passed=False, avg_r=0.2, parent_avg_r=0.1, test_r=0.1, parent_test_r=0.05, status="BACKTESTING",
                     checked="2026-10-11 01:00")]
        fl = flab.summary(rows, [], ["B-FADX"], 4, 1, S)
        part = wrv.failure_part(fl)
        self.assertEqual((part["judged"], part["helped"], part["pending"]), (1, 1, 1))
        self.assertTrue(any("DISP helped 1 of 1" in x for x in part["lines"]))
        import pandas as pd
        rv = wrv.build(dt.datetime(2026, 10, 18, 5, tzinfo=dt.timezone.utc), pd.DataFrame(), {}, {}, {}, [], [],
                       failure_lab=fl)
        self.assertIn("## Failure Lab", wrv.render(rv))
        self.assertIn("🔧 Failure Lab: 1 repair(s) judged", wrv.telegram(rv))
        self.assertIsNone(wrv.failure_part(None))


if __name__ == "__main__":
    unittest.main()
