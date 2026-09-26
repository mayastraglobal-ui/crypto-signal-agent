"""
Phase 19 A tests: strategy-family validation gates (research only).

- the family table: which family is in which group; a family not listed gets the tight (old) rules
- the measurements: Monte Carlo per 100 trades does NOT grow with the number of trades (the whole-history drawdown
  does), drawdown duration, loss clustering
- the verdicts: the trend group drops the single 10R gate for recovery factor + DD per 100 trades + duration; the
  tight group keeps 10R (and the 8R Monte Carlo) and adds clustering + duration
- live safety: the suspension / paper limits come from the same rule; nothing changes in shadow mode
- shadow mode cannot be switched on early; every re-evaluation is one more trial; fees, risk per trade and the
  trials bar are unchanged; the calibration method does not depend on the card's own average
- the +100% cost stress is shown, never a gate

Run:  python -m unittest test_family_gates -v      (from tests/)
"""
import datetime as dt
import os
import sys
import unittest

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scanner  # noqa: E402
from engine import family_gates as FGM  # noqa: E402
from engine import lifecycle as LC  # noqa: E402
from engine import risk as RK  # noqa: E402
from engine import trials as TR  # noqa: E402

def read(path):
    with open(path) as f:
        return f.read()


CFG = yaml.safe_load(read(os.path.join(ROOT, "config.yaml")))
FG = FGM.settings(CFG["family_gates"])
V, R = CFG["validation"], CFG["research"]
DAY = 86_400_000


def trades(r, step_days=1.0, t0=0):
    return [dict(r=float(x), entry_time=int(t0 + i * step_days * DAY)) for i, x in enumerate(r)]


def edge(n, seed=1, win=2.0, p=0.4):
    """n trades of a trend-like edge: 40% win +2R, 60% lose -1R (avg +0.2R)."""
    rng = np.random.default_rng(seed)
    return np.where(rng.random(n) < p, win, -1.0)


def metrics(**kw):
    m = dict(n=500, net_r=60.0, max_dd_r=15.0, recovery=4.0, window=dict(window=100, runs=1000, dd95_r=12.0,
                                                                          dd_median_r=6.0, streak95=10),
             duration=dict(days=200, trades=50, share=0.2, span_days=1000, recovered=True),
             clustering=dict(streak=8, streak95=10, clustered=False))
    m.update(kw)
    return m


class Table(unittest.TestCase):
    def test_groups(self):
        for fam in ("trend_following", "momentum", "breakout", "mtf_pullback"):
            self.assertEqual(FGM.group_of(fam, FG), "trend", fam)
        for fam in ("mean_reversion", "liquidity_reversal", "smc", "price_action", "something_new", None):
            self.assertEqual(FGM.group_of(fam, FG), "tight", fam)

    def test_every_family_of_every_card_is_placed_explicitly(self):
        fams = set()
        for f in ("strategies.yaml", "strategies_lab.yaml"):
            p = os.path.join(ROOT, f)
            if os.path.exists(p):
                fams |= {x["family"] for x in yaml.safe_load(read(p)) or [] if isinstance(x, dict) and "family" in x}
        listed = {f for g in FG["groups"].values() for f in g["families"]}
        self.assertEqual(fams - listed, set())

    def test_nothing_that_must_never_loosen_was_touched(self):
        self.assertEqual(CFG["account"]["risk_per_trade_pct"], 0.5)
        self.assertEqual(CFG["risk"]["max_risk_pct"], 1.0)
        self.assertEqual(R["cost_stress_x"], 1.5)                 # the +50% GATE stays
        self.assertEqual(R["trials_alpha"], 0.05)
        self.assertEqual(V["max_drawdown_r"], 10)                 # kept for the tight group
        self.assertEqual((R["monte_carlo_max_dd_r"], R["paper_max_dd_r"], CFG["risk"]["strategy_max_dd_r"]), (8, 8, 8))
        self.assertEqual(CFG["costs"]["long"]["taker_fee_pct"], 0.10)
        tight, trend = FG["groups"]["tight"], FG["groups"]["trend"]
        self.assertTrue(tight["keep_max_drawdown_r"] and tight["keep_whole_history_mc"] and tight["loss_clustering"])
        self.assertGreaterEqual(trend["min_recovery_factor"], 3)
        self.assertEqual(FG["cost_report_x"], 2.0)


class Shadow(unittest.TestCase):
    def test_shadow_until_operator_yes_after_the_period(self):
        base = dict(FG, shadow_start="2026-09-26", shadow_days=14)
        day = dt.date(2026, 10, 20)
        self.assertEqual(FGM.mode(dict(base, mode="shadow", operator_ok="2026-10-11"), day)[0], "shadow")
        self.assertEqual(FGM.mode(dict(base, mode="active", operator_ok=None), day)[0], "shadow")
        self.assertEqual(FGM.mode(dict(base, mode="active", operator_ok="2026-10-01"), day)[0], "shadow")  # too early
        self.assertEqual(FGM.mode(dict(base, mode="active", operator_ok="2026-10-10"), dt.date(2026, 10, 9))[0],
                         "shadow")
        self.assertEqual(FGM.mode(dict(base, mode="active", operator_ok="2026-10-10"), day)[0], "active")
        self.assertEqual(FGM.mode(dict(base, mode="active", shadow_start=None, operator_ok="2026-10-10"), day)[0],
                         "shadow")

    def test_committed_config_is_in_shadow_for_the_whole_period(self):
        start = dt.date.fromisoformat(str(FG["shadow_start"]))
        self.assertGreaterEqual(int(FG["shadow_days"]), 14)
        for d in range(int(FG["shadow_days"])):
            self.assertEqual(FGM.mode(FG, start + dt.timedelta(days=d))[0], "shadow")

    def test_research_moves_on_the_new_rule_only_when_active(self):
        src = read(os.path.join(ROOT, "research.py"))
        self.assertIn('if fg_mode == "active":\n            base_status, reasons, paper_ok, paper_reasons = '
                      'new_base, new_reasons, new_ok, new_paper', src)
        self.assertEqual(src.count("new_ok, new_paper"), 3)                   # computed, twin check, used if active

    def test_live_limits_only_reach_the_risk_engine_when_active(self):
        res = dict(family_gates=dict(mode="shadow", live_limits={"A@1.0|4h": dict(live_r=15.7)}))
        self.assertEqual(FGM.active_live_limits(res), {})
        res["family_gates"]["mode"] = "active"
        self.assertEqual(FGM.active_live_limits(res), {"A@1.0|4h": 15.7})
        self.assertEqual(FGM.active_live_limits(None), {})


class Measurements(unittest.TestCase):
    def test_dd_per_100_trades_does_not_grow_with_sample_size(self):
        r = edge(300)
        few, many = FGM.measure(trades(r), FG), FGM.measure(trades(np.tile(r, 10)), FG)
        self.assertGreater(many["max_dd_r"], few["max_dd_r"] - 1e-9)       # the old measure can only grow
        self.assertLess(abs(many["window"]["dd95_r"] - few["window"]["dd95_r"]), 1.5)
        self.assertEqual(few["window"]["window"], 100)

    def test_window_mc_deterministic_and_none_for_tiny(self):
        r = edge(200, seed=3)
        self.assertEqual(FGM.window_mc(r), FGM.window_mc(r))
        self.assertIsNone(FGM.window_mc([1.0]))

    def test_underwater(self):
        # +1, -1, -1, +3 (new peak on day 3), -1 to the end (day 4..5 unrecovered)
        u = FGM.underwater([1, -1, -1, 3, -1, -0.5], [0, DAY, 2 * DAY, 3 * DAY, 4 * DAY, 5 * DAY])
        self.assertEqual((u["days"], u["trades"], u["recovered"]), (3.0, 2, True))
        self.assertAlmostEqual(u["share"], 0.6)
        u = FGM.underwater([1, 1, -1, -1], [0, DAY, 2 * DAY, 10 * DAY])    # never recovers: to the last trade
        self.assertEqual((u["days"], u["recovered"]), (9.0, False))
        self.assertEqual(FGM.underwater([], [])["share"], 0.0)

    def test_clustering(self):
        r = np.r_[-np.ones(30), np.full(70, 1.0)]                          # all losses first
        self.assertTrue(FGM.clustering(r)["clustered"])
        self.assertFalse(FGM.clustering(np.tile([1.0, -1.0], 50))["clustered"])

    def test_recovery_factor(self):
        m = FGM.measure(trades([2, -1, -1, 3]), FG)
        self.assertEqual((m["net_r"], m["max_dd_r"], m["recovery"]), (3.0, 2.0, 1.5))
        self.assertEqual(FGM.measure(trades([1, 2]), FG)["recovery"], 99.0)          # no drawdown: JSON-safe


class Verdicts(unittest.TestCase):
    def test_trend_group_replaces_the_10r_gate(self):
        self.assertEqual(FGM.dd_reasons(metrics(max_dd_r=22.5), "trend", FG, V), [])     # 22.5R is fine now ...
        lim = FG["groups"]["trend"]
        for bad, word in ((dict(recovery=2.9), "recovery factor"), (dict(recovery=None), "recovery factor"),
                          (dict(window=dict(window=100, dd95_r=lim["max_mc_dd95_per_100_r"] + 0.1)), "per 100 trades"),
                          (dict(window=None), "per 100 trades"),
                          (dict(duration=dict(days=900, share=lim["max_dd_duration_share"] + 0.01)), "longest drawdown")):
            out = FGM.dd_reasons(metrics(**bad), "trend", FG, V)
            self.assertEqual(len(out), 1, bad)
            self.assertIn(word, out[0])
        # clustering is shown, not a trend-group gate
        self.assertEqual(FGM.dd_reasons(metrics(clustering=dict(streak=30, streak95=10, clustered=True)), "trend", FG,
                                        V), [])

    def test_tight_group_keeps_10r_and_adds_clustering_and_duration(self):
        self.assertEqual(FGM.dd_reasons(metrics(max_dd_r=9.9), "tight", FG, V), [])
        self.assertIn("max drawdown 10.5R", FGM.dd_reasons(metrics(max_dd_r=10.5), "tight", FG, V))
        out = FGM.dd_reasons(metrics(max_dd_r=5, clustering=dict(streak=30, streak95=10, clustered=True)), "tight",
                             FG, V)
        self.assertEqual(len(out), 1)
        self.assertIn("loss clustering", out[0])
        out = FGM.dd_reasons(metrics(max_dd_r=5, duration=dict(days=900, share=0.9)), "tight", FG, V)
        self.assertEqual(len(out), 1)
        self.assertIn("longest drawdown", out[0])
        # recovery factor and DD per 100 trades are not tight-group gates
        self.assertEqual(FGM.dd_reasons(metrics(max_dd_r=5, recovery=0.5, window=None), "tight", FG, V), [])
        self.assertTrue(FGM.uses_whole_history_mc("tight", FG))
        self.assertFalse(FGM.uses_whole_history_mc("trend", FG))

    def test_judge_old_rule_unchanged_and_new_rule_replaces_only_the_dd_check(self):
        st = dict(n=1105, exp_r=0.123, pf=1.28, max_dd_r=22.5)
        dev, val = dict(n=744, exp_r=0.11), dict(n=361, exp_r=0.149)
        old = LC.judge(st, dev, val, None, V, 0.0, 0.05)
        self.assertEqual((old[0], old[1]), ("BACKTESTING", ["max drawdown 22.5R"]))
        self.assertEqual(LC.judge(st, dev, val, None, V, 0.0, 0.05, dd_checks=[])[0], "VALIDATION")
        new = LC.judge(st, dev, val, None, V, 0.0, 0.05, dd_checks=["recovery factor 1.00"])
        self.assertEqual(new[:2], ("BACKTESTING", ["recovery factor 1.00"]))
        # every other gate still applies under the new rule
        self.assertIn("profit factor 1.10", LC.judge(dict(st, pf=1.1), dev, val, None, V, 0.0, 0.05, dd_checks=[])[1])
        self.assertEqual(LC.judge(dict(st, exp_r=0.05), dev, val, None, V, 0.0, 0.05, dd_checks=[])[0], "BACKTESTING")

    def test_paper_gate_without_whole_history_mc_still_has_every_other_gate(self):
        ev = dict(monte_carlo=dict(runs=1000, n=1105, dd95_r=26.7), t_stat=3.66,
                  walk_forward=dict(passed=True, positive=5, judged=5, pooled_avg_r=0.1),
                  positive_coins=list("ABCDEFGH"), stress=dict(avg_r=0.092),
                  perturbation=dict(stable=True, worst=None), overfit=[], all=dict(n=1105), validate=dict(n=361))
        self.assertFalse(LC.paper_gate("VALIDATION", ev, None, R, (3.27, 92), 8.0, True)[0])     # old: 26.7R > 8R
        self.assertTrue(LC.paper_gate("VALIDATION", ev, None, R, (3.27, 92), None, True)[0])
        self.assertFalse(LC.paper_gate("VALIDATION", ev, None, R, (3.7, 500), None, True)[0])    # trials bar stays
        self.assertFalse(LC.paper_gate("VALIDATION", dict(ev, stress=dict(avg_r=-0.01)), None, R, (3.27, 92), None,
                                       True)[0])                                                 # +50% gate stays

    def test_verdict(self):
        self.assertEqual(FGM.verdict("VALIDATION", True), "PAPER_TRADING")
        self.assertEqual(FGM.verdict("VALIDATION", False), "VALIDATION")
        self.assertEqual(FGM.verdict("BACKTESTING", True), "BACKTESTING")


class LiveSafety(unittest.TestCase):
    def test_limits_from_the_same_rule(self):
        cap = FG["groups"]["trend"]["max_mc_dd95_per_100_r"]
        lim = FGM.live_limit(metrics(window=dict(window=100, dd95_r=15.7)), "trend", FG, 8, 8)
        self.assertEqual((lim["live_r"], lim["paper_r"]), (15.7, 15.7))
        self.assertEqual(FGM.live_limit(metrics(window=dict(window=100, dd95_r=cap + 5)), "trend", FG, 8, 8)["live_r"],
                         cap)
        self.assertEqual(FGM.live_limit(metrics(), "tight", FG, 8, 8)["live_r"], 8.0)

    def test_approved_card_is_not_suspended_at_once(self):
        """A trend card that passed (its 95% DD per 100 trades <= the limit) lives under its own number: a normal
        bad-luck drawdown above the old 8R does not suspend it; one beyond its own 95% does."""
        rows = [dict((c, np.nan) for c in scanner.LOG_COLS) for _ in range(4)]
        for r, (d, x) in zip(rows, ((10, 3.0), (11, -4.0), (12, -3.0), (13, -3.0))):   # 3R up, then 10R down
            r.update(coin="BTC", tf="4h", strategy="T", version="1.0", direction="LONG", status="SL", stage="APPROVED",
                     state="CLOSED", result_r=x, closed_time_utc=f"2026-09-{d:02d} 10:00", entry_time_utc="")
        lg = pd.DataFrame(rows, columns=scanner.LOG_COLS)
        now = dt.datetime(2026, 9, 24, 12, 0, tzinfo=dt.timezone.utc)
        old = RK.Book(lg, now, RK.settings(CFG["risk"]), {})
        self.assertEqual(old.suspended(), ["T@1.0|4h"])                                # 10R > 8R
        new = RK.Book(lg, now, RK.settings(dict(CFG["risk"], strategy_dd_limits={"T@1.0|4h": 15.7})), {})
        self.assertEqual((new.dd_limit("T@1.0|4h"), new.suspended()), (15.7, []))
        self.assertEqual(new.dd_limit("OTHER@1.0|1h"), 8.0)                            # others keep 8R
        tight = RK.Book(lg, now, RK.settings(dict(CFG["risk"], strategy_dd_limits={"T@1.0|4h": 9.0})), {})
        self.assertEqual(tight.suspended(), ["T@1.0|4h"])


class Trials(unittest.TestCase):
    def test_every_re_evaluation_is_one_more_trial_once(self):
        origin = FGM.REEVAL_ORIGIN.format(v=1)
        rows = TR.number([dict(strategy="A", version="1.0", tf="4h", first_tested_utc="x", origin="library")], 0)
        new = TR.additions(rows, [("A", "1.0", "4h", "library"), ("A", "1.0", "4h", origin)], "now")
        self.assertEqual([(r["trial"], r["origin"]) for r in new], [(2, origin)])
        again = TR.additions(rows + new, [("A", "1.0", "4h", "library"), ("A", "1.0", "4h", origin)], "later")
        self.assertEqual(again, [])                                                    # not every day
        v2 = TR.additions(rows + new, [("A", "1.0", "4h", FGM.REEVAL_ORIGIN.format(v=2))], "later")
        self.assertEqual(len(v2), 1)                                                   # a new rule set counts again
        self.assertGreater(TR.need_t(92, 0.05), TR.need_t(46, 0.05))                   # the bar only rises

    def test_research_counts_re_evaluations(self):
        src = read(os.path.join(ROOT, "research.py"))
        self.assertIn("tested_now + [(k[0], k[1], k[2], reeval) for k in sorted(per)]", src)


class Calibration(unittest.TestCase):
    def cells(self, shift=0.0):
        out = {}
        for i in range(4):
            r = edge(400, seed=10 + i) + shift
            out[f"C{i}@1.0|4h"] = (list(r), [int(j * DAY) for j in range(len(r))])
        return out

    def test_method_ignores_the_cards_own_average(self):
        a, b = FGM.calibrate(self.cells(), 0.10, 30, draws=4000), FGM.calibrate(self.cells(-0.5), 0.10, 30, draws=4000)
        self.assertEqual(a["max_mc_dd95_per_100_r"], b["max_mc_dd95_per_100_r"])
        self.assertEqual(a["max_dd_duration_share"], b["max_dd_duration_share"])

    def test_limits_are_the_95th_percentile_rounded_up(self):
        c = FGM.calibrate(self.cells(), 0.10, 30, draws=4000)
        self.assertGreaterEqual(c["max_mc_dd95_per_100_r"], c["dd_per_100"]["p95"])
        self.assertLess(c["max_mc_dd95_per_100_r"] - c["dd_per_100"]["p95"], 0.5)
        self.assertGreaterEqual(c["max_dd_duration_share"], c["duration_share"]["p95"])
        self.assertEqual(c["judged_cells"], 4)

    def test_config_matches_the_recorded_calibration(self):
        doc = read(os.path.join(ROOT, "memory", "family_gates_calibration.md"))
        trend, tight = FG["groups"]["trend"], FG["groups"]["tight"]
        self.assertIn(f"max_mc_dd95_per_100_r: {trend['max_mc_dd95_per_100_r']}", doc)
        self.assertIn(f"trend max_dd_duration_share: {trend['max_dd_duration_share']}", doc)
        self.assertIn(f"tight max_dd_duration_share: {tight['max_dd_duration_share']}", doc)


class Report(unittest.TestCase):
    def test_shadow_table_lines(self):
        cell = dict(strategy="D", version="1.0", tf="4h", family_gate=dict(
            group="trend", old="BACKTESTING", new="PAPER_TRADING", changed=True, new_reasons=[],
            metrics=metrics(recovery=6.02, window=dict(window=100, dd95_r=15.7),
                            duration=dict(days=592, share=0.18))))
        res = dict(family_gates=dict(rules_version=1, mode_text="shadow mode"), cells={"D@1.0|4h": cell})
        md = "\n".join(FGM.report_lines(res))
        self.assertIn("1 of 1 strategy / timeframe tests would get a different verdict", md)
        self.assertIn("| D v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 6.02 | 15.7R | 592 d (18%) |", md)
        self.assertEqual(FGM.report_lines({}), [])


if __name__ == "__main__":
    unittest.main()
