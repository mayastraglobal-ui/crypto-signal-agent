"""
Phase 18 part B tests: the lookahead + recursive check (a card that peeks into the future or depends on where history
starts is BIASED - FAILED for good), Monte Carlo trade-order shuffling (95% worst drawdown gate, expected worst losing
streak), and rule significance (one entry rule removed at a time; the simpler card queued in the lab).

Run:  python -m unittest test_robust -v      (from tests/)
"""
import copy
import itertools
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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scanner as sc  # noqa: E402
import test_brain  # noqa: E402
import test_lab  # noqa: E402
import test_learn  # noqa: E402
from engine import approval as AP  # noqa: E402
from engine import bias as BI  # noqa: E402
from engine import data_quality as dq  # noqa: E402
from engine import debate as DB  # noqa: E402
from engine import ideas as I  # noqa: E402
from engine import lifecycle as LC  # noqa: E402
from engine import research as RS  # noqa: E402
from engine import strategy_spec as SS  # noqa: E402

CFG = yaml.safe_load(test_brain.read(os.path.join(ROOT, "config.yaml")))
TFS = ["1h", "30m"]


def brute_streak(r):
    best = cur = 0
    for x in r:
        cur = cur + 1 if x < 0 else 0
        best = max(best, cur)
    return best


def brute_dd(r):
    eq, peak, dd = 0.0, 0.0, 0.0
    for x in r:
        eq += x
        peak = max(peak, eq)
        dd = max(dd, peak - eq)
    return dd


class MonteCarlo(unittest.TestCase):
    def test_same_trades_other_orders(self):
        rng = np.random.default_rng(3)
        r = rng.normal(0.1, 1.0, 300)
        mc = RS.monte_carlo(r, 1000)
        self.assertEqual(mc, RS.monte_carlo(r, 1000), "deterministic (fixed seed)")
        self.assertEqual((mc["runs"], mc["n"]), (1000, 300))
        self.assertAlmostEqual(mc["dd_r"], round(brute_dd(r), 1), places=6)
        self.assertEqual(mc["streak"], brute_streak(r))
        self.assertLessEqual(mc["dd_median_r"], mc["dd95_r"])
        self.assertLessEqual(mc["streak_median"], mc["streak95"])
        coin = RS.monte_carlo([1.0, -1.0] * 100, 1000)       # fair coin, 200 trades: the 95% level is well above typical
        self.assertGreaterEqual(coin["dd95_r"], coin["dd_median_r"] + 4)
        self.assertGreaterEqual(coin["streak95"], coin["streak_median"] + 2)
        self.assertTrue(9 <= coin["streak95"] <= 11, coin)
        self.assertIsNone(RS.monte_carlo([0.5], 100))

    def test_extremes(self):
        mc = RS.monte_carlo([-1.0] * 10, 50)                 # every order is the same
        self.assertEqual((mc["dd_r"], mc["dd95_r"], mc["streak"], mc["streak95"]), (10.0, 10.0, 10, 10))
        mc = RS.monte_carlo([2.0] * 5 + [-1.0] * 5, 1000)    # sorted wins-then-losses: all 5 losses in a row
        self.assertEqual((mc["dd_r"], mc["streak"]), (5.0, 5))
        self.assertLess(mc["streak_median"], 5, "shuffled, a 5-loss streak is rare")

    def test_vector_helpers_match_brute_force(self):
        rng = np.random.default_rng(9)
        m = rng.normal(0, 1, (40, 60))
        np.testing.assert_allclose(RS._max_dd(m), [brute_dd(x) for x in m])
        np.testing.assert_array_equal(RS._max_streak(m < 0), [brute_streak(x) for x in m])
        for bits in itertools.product([0, 1], repeat=6):     # every 6-trade win / loss pattern
            x = np.array([-1.0 if b else 1.0 for b in bits])
            self.assertEqual(int(RS._max_streak((x < 0)[None, :])[0]), brute_streak(x))

    def test_gate(self):
        mc = dict(runs=1000, n=120, dd95_r=12.8)
        ok, why = RS.mc_gate(mc, 8)
        self.assertFalse(ok)
        self.assertIn("95% worst drawdown 12.8R over 1000 shuffles of 120 trades - above the 8R limit", why)
        self.assertEqual(RS.mc_gate(dict(mc, dd95_r=8.0), 8), (True, None), "at the limit is within it")
        self.assertFalse(RS.mc_gate(None, 8)[0])

    def test_paper_gate_needs_it(self):
        cell = test_learn.cell()
        ev = dict(cell["evidence"], monte_carlo=dict(runs=1000, n=300, dd95_r=9.5), t_stat=5.0)
        R = CFG["research"]
        ok, reasons = LC.paper_gate("VALIDATION", ev, None, R, None, 8.0, True)
        self.assertTrue(any(x.startswith("Monte Carlo: 95% worst drawdown 9.5R") for x in reasons), reasons)
        ok2, reasons2 = LC.paper_gate("VALIDATION", dict(ev, monte_carlo=dict(ev["monte_carlo"], dd95_r=7.0)), None, R,
                                      None, 8.0, True)
        self.assertFalse(any("Monte Carlo" in x for x in reasons2))
        self.assertTrue(any("did not run" in x for x in LC.paper_gate("VALIDATION", ev, None, R, None, None, False)[1]))

    def test_config_is_never_looser_than_the_risk_limit(self):
        R = CFG["research"]
        self.assertEqual(R["monte_carlo_runs"], 1000)
        self.assertLessEqual(R["monte_carlo_max_dd_r"], CFG["risk"]["strategy_max_dd_r"])
        src = test_brain.read(os.path.join(ROOT, "research.py"))
        self.assertIn('min(float(R.get("monte_carlo_max_dd_r", cfg["risk"]["strategy_max_dd_r"])),\n'
                      '                   float(cfg["risk"]["strategy_max_dd_r"]))', src)

    def test_approval_pack_shows_the_streak(self):
        c = test_learn.cell()
        c["evidence"]["monte_carlo"] = dict(runs=1000, n=300, dd_r=6.6, dd_median_r=7.9, dd95_r=12.1, streak=7,
                                            streak_median=8, streak95=11)
        c["evidence"]["rules"] = [dict(label="without rule 2", rule="rel_vol > 1.5", n=420, avg_r=0.12, adds=False),
                                  dict(label="without rule 1", rule="htf_up", n=500, avg_r=0.02, adds=True)]
        c["bias"] = None
        text = "\n".join(AP.pack(c, test_brain.Approval().spec(), [], {}, AP.settings(None), "2026-09-26 00:50"))
        self.assertIn("**expected worst losing streak: 11 losses in a row**", text)
        self.assertIn("95% worst drawdown 12.1R", text)
        self.assertIn("without rule 2 (rel_vol > 1.5): 420 trades, +0.120R - ADDS NOTHING", text)
        self.assertIn("lookahead / recursive check: passed", text)
        bull, bear = DB.cell_cases(c)
        self.assertTrue(any("expected worst losing streak 11 in a row" in x for x in bear))
        self.assertTrue(any("1 entry rule(s) add nothing" in x for x in bear))


class RuleSignificance(unittest.TestCase):
    def card(self):
        raw = dict(id="X", version="1.0", long=["a > {p}", "b > 1", "c"], short=["a < {q}", "b < 1", "d"],
                   params=dict(p=1, q=2), stop={"method": "atr", "atr": 1.5}, time_stop_bars=10, timeframes=["1h"])
        return dict(SS.render(raw), _raw=raw)

    def test_drops(self):
        d = SS.rule_drops(self.card())
        self.assertEqual([x[0] for x in d], ["without rule 1", "without rule 2", "without rule 3"])
        self.assertEqual(d[0][3], "a > 1 / a < 2", "the rule text is shown with its numbers")
        self.assertEqual(d[0][2]["long"], ["b > 1", "c"])
        self.assertEqual(d[0][2]["params"], {}, "p and q were only used by the removed rule")
        self.assertEqual(d[1][2]["params"], dict(p=1, q=2))
        self.assertEqual(d[0][2]["short"], ["b < 1", "d"])
        self.assertEqual(d[0][1]["long"], ["b > 1", "c"], "the rendered card to backtest")
        one = dict(self.card(), _raw=dict(self.card()["_raw"], long=["a > {p}"], short=["a < {q}", "b < 1"]))
        d = SS.rule_drops(one)
        self.assertEqual([x[0] for x in d], ["without rule 1", "without rule 2"])
        self.assertEqual(d[0][2]["long"], ["a > {p}"], "a side with one rule keeps it")
        self.assertEqual(SS.rule_drops(dict(self.card(), _raw=dict(self.card()["_raw"], long=["a"], short=["b"]))), [])

    def test_verdicts(self):
        base = dict(n=200, avg_r=0.10)
        out = RS.rule_significance(base, {"without rule 1": ("a", {"BTC": (150, 18.0), "ETH": (100, 10.0)}),
                                          "without rule 2": ("b", {"BTC": (300, 15.0)}),
                                          "without rule 3": ("c", {"BTC": (20, 5.0)})}, 30)
        self.assertEqual([(x["label"], x["n"], x["avg_r"], x["adds"]) for x in out],
                         [("without rule 1", 250, 0.112, False), ("without rule 2", 300, 0.05, True),
                          ("without rule 3", 20, 0.25, None)])
        self.assertIsNone(RS.rule_significance(dict(n=10, avg_r=0.1), {"w": ("a", {"B": (90, 9.0)})}, 30)[0]["adds"])
        self.assertFalse(RS.rule_significance(base, {"w": ("a", {"B": (200, 20.0)})}, 30)[0]["adds"],
                         "the same result without the rule: the rule adds nothing")

    def simpler_cell(self, targets=True, status="BACKTESTING"):
        lib = copy.deepcopy(test_lab.lib("donchian_breakout"))
        if targets:
            lib["targets"] = {"long": ["2R", "3R"], "short": ["2R", "3R"], "split": [0.5, 0.5]}
        lib["_raw"] = copy.deepcopy(lib)
        card = dict(lib, lab=False)
        rule = SS.rule_drops(card)[-1]
        cell = dict(strategy="donchian_breakout", version="1.0", tf="1h", status=status, bias=None,
                    evidence=dict(all=dict(n=300, avg_r=0.05)),
                    rules_adding_nothing=[dict(label=rule[0], rule=rule[3], n=420, avg_r=0.09, adds=False)])
        return {"donchian_breakout@1.0|1h": cell}, {"donchian_breakout@1.0": card}, rule

    def test_simpler_card_queued_in_the_lab(self):
        cells, cards, rule = self.simpler_cell()
        new, skipped = I.simpler_cards(cells, cards, "2026-09-27", 3, test_lab.B.rg.LABELS, sc.TF_ORDER)
        self.assertEqual(skipped, {})
        c = new[0]
        self.assertEqual(c["id"], f"donchian_breakout-S{rule[0].split()[-1]}")
        self.assertEqual((c["factory"], c["parent"]), ("variant_search", "result: donchian_breakout@1.0 1h"))
        self.assertEqual(c["long"], rule[2]["long"])
        self.assertIn("420 trades avg +0.090R", c["factory_evidence"])
        others = {x["id"]: x for x in cards.values()}
        self.assertEqual(SS.lab_card_problems(c, others, test_lab.B.rg.LABELS, sc.TF_ORDER), [])
        self.assertEqual(SS.change_count(cards["donchian_breakout@1.0"]["_raw"], c), ["long/short"])
        self.assertEqual(I.simpler_cards(cells, cards, "2026-09-27", 0, test_lab.B.rg.LABELS, sc.TF_ORDER)[0], [])

    def test_not_queued_says_why(self):
        cells, cards, _ = self.simpler_cell(targets=False)
        new, skipped = I.simpler_cards(cells, cards, "2026-09-27", 3, test_lab.B.rg.LABELS, sc.TF_ORDER)
        self.assertEqual(new, [])
        self.assertIn("first target must be >= 2R", skipped["donchian_breakout@1.0|1h"])
        cells, cards, _ = self.simpler_cell(status="FAILED")
        self.assertEqual(I.simpler_cards(cells, cards, "2026-09-27", 3, test_lab.B.rg.LABELS, sc.TF_ORDER),
                         ([], {}), "a FAILED cell's rules are only reported")


def synthetic(n=3000):
    feed = sc.Synthetic()
    data, quality = {}, {}
    for tf in ["1w", "1d"] + TFS + ["4h"]:
        raw = feed.klines("BTCUSDT", tf, min(n, 1000) if tf == "1w" else n)
        df, rep = dq.check_candles(raw, sc.TF_MS[tf], int(raw["close_time"].max()) + 1,
                                   dq.settings(CFG.get("data_quality")))
        data[("BTCUSDT", tf)], quality[("BTC", tf)] = df, rep
    return data, quality


_orig_ns = sc.make_namespace


def planted_ns(df, feats):
    """The engine's namespace plus two planted bugs: 'peek' = the close 2 candles LATER (lookahead) and 'count' = the
    number of candles since the history started (depends on where history starts)."""
    ns = _orig_ns(df, feats)
    ns["peek"] = df["close"].shift(-2)
    ns["count"] = pd.Series(np.arange(len(df), dtype=float), index=df.index)
    return ns


class BiasCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data, cls.quality = synthetic()
        lib = [c for c in sc.load_cards()[0] if c["id"] == "donchian_breakout"][0]
        base = dict(copy.deepcopy(lib), timeframes=TFS)
        cls.clean = dict(base, id="clean")
        cls.peek = dict(base, id="peeker", long=list(base["long"]) + ["close < peek"],
                        short=list(base["short"]) + ["close > peek"])
        cls.count = dict(base, id="counter", long=list(base["long"]) + ["count > 1800"],
                         short=list(base["short"]) + ["count > 1800"])
        cls.boot = dict(base, id="booter", long=list(base["long"]) + ["count < 1100"],
                        short=list(base["short"]) + ["count < 1100"])       # differs only early, then never again
        cls.S = BI.settings(dict(lookahead_cuts=3))
        with mock.patch.object(sc, "make_namespace", planted_ns):
            btc = sc.btc_frames(cls.data, "USDT", TFS)
            full = sc.prepare_coin("BTCUSDT", "BTC", cls.data, cls.quality, TFS, CFG, None, btc)
            cls.res = BI.check_coin("BTCUSDT", "BTC", cls.data, cls.quality, TFS, CFG, None, btc, full,
                                    [cls.clean, cls.peek, cls.count, cls.boot], sc.prepare_coin, sc.eval_rules,
                                    sc.level_array,
                                    SS.columns_needed, cls.S)

    def test_finds_the_planted_lookahead(self):
        f = self.res["findings"]
        self.assertNotIn("clean@1.0", f, BI.summary(f.get("clean@1.0", [])))
        look = [x for x in f["peeker@1.0"] if x["check"] == "lookahead"]
        self.assertEqual({x["what"] for x in look}, {"long: close < peek", "short: close > peek"})
        self.assertEqual({x["tf"] for x in look} <= set(TFS), True)
        self.assertTrue(all(0 < x["bars"] <= 2 * 3 for x in look), "only the last 2 candles before each cut differ")

    def test_finds_the_planted_recursive_value(self):
        f = self.res["findings"]["counter@1.0"]
        self.assertEqual({x["check"] for x in f}, {"recursive"}, "a running count has no lookahead - it depends on "
                                                                "where history starts")
        self.assertEqual({x["what"] for x in f}, {"long: count > 1800", "short: count > 1800"})
        self.assertEqual(len(self.res["cuts"]), 3)
        self.assertEqual(sorted(self.res["checked"]), ["booter@1.0", "clean@1.0", "counter@1.0", "peeker@1.0"])
        self.assertEqual(self.res["recursive"], dict(drop=500, settle=1000, tolerance_pct=0.1))

    def test_warm_up_only_is_a_warning_not_biased(self):
        """A difference that dies out early (a slow warm-up) is a warning; one that persists stays BIASED."""
        self.assertNotIn("booter@1.0", self.res["findings"], BI.summary(self.res["findings"].get("booter@1.0", [])))
        w = self.res["warnings"]["booter@1.0"]
        self.assertEqual({x["what"] for x in w}, {"long: count < 1100", "short: count < 1100"})
        self.assertIn("counter@1.0", self.res["findings"], "a running count still differs late - BIASED")
        self.assertNotIn("counter@1.0", self.res["warnings"])
        lines = "\n".join(BI.report_lines(dict(duration_s=60, robustness=dict(bias=self.res))))
        self.assertIn("booter@1.0: warm-up only", lines)
        self.assertIn("counter@1.0 BIASED", lines)

    def test_differences_rules(self):
        full = pd.DataFrame({"open_time": np.arange(10) * 10})
        cut = pd.DataFrame({"open_time": np.arange(2, 8) * 10})
        a = dict(b=np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], bool), x=np.arange(10, dtype=float))
        c = dict(b=a["b"][2:8].copy(), x=a["x"][2:8].copy())
        self.assertEqual(BI.differences(full, a, cut, c), [])
        c["b"][5] = ~c["b"][5]
        c["x"][0] = np.nan
        d = {x["what"]: x for x in BI.differences(full, a, cut, c)}
        self.assertEqual((d["b"]["bars"], d["b"]["of"], d["b"]["first_ms"], d["b"]["late"]), (1, 6, 70, 1))
        self.assertEqual((d["x"]["last_ms"], d["x"]["late"]), (20, 0), "only the first candle differs")
        self.assertEqual(d["x"]["first_ms"], 20, "a value that becomes unknown counts")
        self.assertEqual([x["what"] for x in BI.differences(full, a, cut, c, from_ms=30)], ["b"])
        self.assertEqual(BI.differences(full, a, cut, c, from_ms=30, tol_share=0.2), [], "1 of 5 flips is tolerated")
        both = dict(x=np.array([np.nan, 1.0]))
        self.assertEqual(BI.differences(pd.DataFrame({"open_time": [0, 1]}), both, pd.DataFrame({"open_time": [0, 1]}),
                                        dict(x=np.array([np.nan, 1.0 + 1e-12]))), [], "both unknown / rounding = same")

    def test_cuts_and_data(self):
        self.assertEqual(BI.pick_cuts([5, 1, 3, 3, 9, 7, 2, 8], 3, 0.3), [2, 5, 9])
        self.assertEqual(BI.pick_cuts([], 3), [])
        d = BI.cut_data(self.data, end_ms=int(self.data[("BTCUSDT", "1h")]["close_time"].iloc[2000]))
        self.assertEqual(len(d[("BTCUSDT", "1h")]), 2001)
        self.assertTrue((d[("BTCUSDT", "30m")]["close_time"] <= d[("BTCUSDT", "1h")]["close_time"].iloc[-1]).all())
        d = BI.cut_data(self.data, drop=500, drop_tfs=["1h"])
        self.assertEqual(len(d[("BTCUSDT", "1h")]), len(self.data[("BTCUSDT", "1h")]) - 500)
        self.assertEqual(len(d[("BTCUSDT", "1d")]), len(self.data[("BTCUSDT", "1d")]), "context timeframes untouched")

    def test_the_library_is_clean(self):
        """Every card in strategies.yaml passes both checks on synthetic data (they use closed candles only)."""
        cards = [dict(c, timeframes=[t for t in c["timeframes"] if t in TFS]) for c in sc.load_cards()[0]]
        cards = [c for c in cards if c["timeframes"]]
        data, quality = synthetic(6000)     # SMC levels remember old swings: 3000 candles leave too little to settle
        btc = sc.btc_frames(data, "USDT", TFS)
        full = sc.prepare_coin("BTCUSDT", "BTC", data, quality, TFS, CFG, None, btc)
        res = BI.check_coin("BTCUSDT", "BTC", data, quality, TFS, CFG, None, btc, full, cards,
                            sc.prepare_coin, sc.eval_rules, sc.level_array, SS.columns_needed, self.S)
        self.assertEqual(res["findings"], {})
        self.assertEqual(len(res["checked"]), len(cards))

    def test_higher_timeframe_inputs_settle_first(self):
        """Real history: the 1h and 4h candles cover the same years, and both are trade timeframes, so the recursive
        run starts 500 x 4h (not 500 x 1h) later on the 4h input of htf_up. Check v1 compared the 1h candles before
        that 4h trend had settled and called every htf_up / htf_down card BIASED (research run 2026-09-26)."""
        tfs = ["4h", "1h"]
        feed, data, quality = sc.Synthetic(), {}, {}
        for tf, n in (("1w", 700), ("1d", 3000), ("4h", 3000), ("1h", 12000)):       # 4h and 1h: the same 500 days
            raw = feed.klines("BTCUSDT", tf, n)
            df, rep = dq.check_candles(raw, sc.TF_MS[tf], int(raw["close_time"].max()) + 1,
                                       dq.settings(CFG.get("data_quality")))
            data[("BTCUSDT", tf)], quality[("BTC", tf)] = df, rep
        lib = [c for c in sc.load_cards()[0] if any("htf_up" in str(r) for r in c.get("long") or [])]
        self.assertTrue(lib, "the library has htf_up cards")
        cards = [dict(c, timeframes=[t for t in tfs if t in c["timeframes"]] or ["1h"]) for c in lib[:2]]
        base = lib[0]                                       # a plain EMA-based higher-timeframe filter must pass too
        cards.append(dict(base, id="ema_htf", timeframes=["1h"], long=["htf_up", "close > ema(close,50)"],
                          short=["htf_down", "close < ema(close,50)"], exit_long=[], exit_short=[]))
        btc = sc.btc_frames(data, "USDT", tfs)
        full = sc.prepare_coin("BTCUSDT", "BTC", data, quality, tfs, CFG, None, btc)
        res = BI.check_coin("BTCUSDT", "BTC", data, quality, tfs, CFG, None, btc, full, cards, sc.prepare_coin,
                            sc.eval_rules, sc.level_array, SS.columns_needed, self.S)
        self.assertEqual(res["findings"], {}, {k: BI.summary(v) for k, v in res["findings"].items()})
        self.assertTrue(all("1h" in v for v in res["checked"].values()))
        self.assertIn("ema_htf@1.0", res["checked"])

    def test_settled_from_waits_for_longer_timeframes(self):
        h = 3_600_000
        frames = {"1h": dict(df=pd.DataFrame({"open_time": np.arange(2000) * h})),
                  "4h": dict(df=pd.DataFrame({"open_time": (np.arange(500) * 4 + 1000) * h})),
                  "30m": dict(df=pd.DataFrame({"open_time": np.arange(4000) * h // 2 + 900 * h}))}
        self.assertEqual(BI.settled_from(frames, "1h", 10), (1000 + 40) * h, "the 4h input settles last")
        self.assertEqual(BI.settled_from(frames, "4h", 10), (1000 + 40) * h)
        self.assertEqual(BI.settled_from(frames, "30m", 10), (1000 + 40) * h)
        self.assertEqual(BI.settled_from(dict(frames, **{"4h": dict(df=pd.DataFrame({"open_time": np.arange(500) * 4 * h}))}),
                                         "1h", 10), 40 * h, "10 candles of 4h still take 40 hours")
        self.assertIsNone(BI.settled_from(frames, "15m", 10))

    def test_stored_bias_of_an_older_check_is_checked_again(self):
        t = BI.tag("recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00)")
        self.assertTrue(t.endswith(f"(check v{BI.CHECK_VERSION})"))
        self.assertTrue(BI.sticky(t))
        self.assertFalse(BI.sticky("recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00)"),
                         "written by check v1, before the higher-timeframe fix")
        self.assertFalse(BI.sticky("x (check v1)"))
        self.assertTrue(BI.sticky(f"x (check v{BI.CHECK_VERSION + 1})"))
        self.assertFalse(BI.sticky(None))
        self.assertEqual(BI.tag(""), "")

    def test_biased_status_is_final(self):
        for st in ("BACKTESTING", "VALIDATION", "PAPER_TRADING", "APPROVED", "FAILED"):
            self.assertEqual(LC.biased_status(st, "lookahead on 1h: x")[0], "FAILED")
        self.assertEqual(LC.biased_status("RETIRED", "x")[0], "RETIRED")
        self.assertEqual(LC.biased_status("VALIDATION", ""), ("VALIDATION", ""))
        self.assertIn("bias", LC.CELL_COLS)

    def test_report_lines(self):
        res = dict(duration_s=6000, cells={}, robustness=dict(
            time_budget_min=90, rules_skipped_coins=["LTC"], monte_carlo=dict(runs=1000, limit_r=8.0),
            bias=dict(coin="BTC", cuts=["a", "b"], recursive=dict(drop=500), checked={"x@1.0": ["1h"]}, seconds=3.0,
                      findings={"x@1.0": [dict(check="lookahead", tf="1h", what="long: close < peek", bars=2, of=900,
                                               first_utc="2026-01-01 00:00")]}),
            rules_adding_nothing={"y@1.0|1h": [{}]}, simpler_queued=[dict(id="y-S2")]))
        text = "\n".join(BI.report_lines(res))
        self.assertIn("100.0 min (budget 90 min) - OVER BUDGET", text)
        self.assertIn("rule test skipped for LTC", text)
        self.assertIn("⛔ **x@1.0 BIASED** - FAILED on every timeframe, for good: lookahead on 1h: long: close < peek "
                      "(2 of 900 candles differ", text)
        self.assertIn("Simpler cards queued in the lab: y-S2", text)
        err = "\n".join(BI.report_lines(dict(robustness=dict(bias=dict(error="boom")))))
        self.assertIn("did NOT run (boom) - no card can reach PAPER_TRADING", err)
        self.assertEqual(BI.report_lines({}), [])


class EndToEnd(unittest.TestCase):
    """The research run with a planted lookahead card: BIASED, FAILED on every timeframe, in the registry - and still
    FAILED on the next run even when the check finds nothing (it can never pass)."""

    def test_research_run(self):
        from test_data_quality import run_copy
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        for name in ("research.py", "memory_guard.py"):
            shutil.copy(os.path.join(ROOT, name), tmp)
        run_copy(tmp, "-c", "pass")                                    # copies the engine and the files
        with open(os.path.join(tmp, "scanner.py"), "a") as f:
            f.write("\n\n_orig_ns = make_namespace\n\n\ndef make_namespace(df, feats):   # planted by the test\n"
                    "    ns = _orig_ns(df, feats)\n    ns['peek'] = df['close'].shift(-2)\n    return ns\n")
        lib = yaml.safe_load(test_brain.read(os.path.join(tmp, "strategies.yaml")))
        peek = copy.deepcopy(next(c for c in lib if c["id"] == "donchian_breakout"))
        peek.update(id="peeker", timeframes=["1h", "30m"], long=peek["long"] + ["close < peek"],
                    short=peek["short"] + ["close > peek"])
        with open(os.path.join(tmp, "strategies.yaml"), "a") as f:
            f.write("\n" + yaml.safe_dump([peek], sort_keys=False))
        run = lambda: subprocess.run([sys.executable, "research.py", "--offline", "--coins", "2"], cwd=tmp,
                                     capture_output=True, text=True, timeout=900)   # run_copy would copy the files again
        p = run()
        self.assertEqual(p.returncode, 0, p.stdout[-3000:] + p.stderr[-3000:])
        res = json.loads(test_brain.read(os.path.join(tmp, "reports", "research_offline.json")))
        self.assertEqual(res["not_run"], {}, res["rule_errors"])
        for tf in ("1h", "30m"):
            c = res["cells"][f"peeker@1.0|{tf}"]
            self.assertEqual(c["status"], "FAILED")
            self.assertTrue(c["bias"].startswith("lookahead on "), c["bias"])
            self.assertTrue(c["reasons"][0].startswith("BIASED - lookahead on "))
        others = [c for k, c in res["cells"].items() if not k.startswith("peeker")]
        self.assertTrue(others and all(c["bias"] is None for c in others))
        self.assertTrue(all("monte_carlo" in c["evidence"] and "rules" in c["evidence"] for c in others))
        rb = res["robustness"]
        self.assertEqual(sorted(rb["bias"]["findings"]), ["peeker@1.0"])
        self.assertEqual(rb["monte_carlo"], dict(runs=1000, limit_r=8.0))
        reg = pd.read_csv(os.path.join(tmp, "reports", "strategy_registry_offline.csv"), dtype={"version": str})
        row = reg[(reg["id"] == "peeker") & (reg["tf"] == "1h")].iloc[0]
        self.assertEqual(row["status"], "FAILED")
        self.assertTrue(str(row["bias"]).startswith("lookahead on "))
        self.assertIn("mc_dd95_r", reg.columns)
        # the next run cannot find it (no cuts, no shifted start) - the version stays BIASED for good
        cfg = yaml.safe_load(test_brain.read(os.path.join(tmp, "config.yaml")))
        cfg["research"]["bias_check"] = dict(lookahead_cuts=0, recursive_drop=0)
        with open(os.path.join(tmp, "config.yaml"), "w") as f:
            yaml.safe_dump(cfg, f)
        p = run()
        self.assertEqual(p.returncode, 0, p.stdout[-3000:] + p.stderr[-3000:])
        res = json.loads(test_brain.read(os.path.join(tmp, "reports", "research_offline.json")))
        self.assertEqual(res["robustness"]["bias"]["findings"], {})
        self.assertEqual(res["cells"]["peeker@1.0|1h"]["status"], "FAILED")
        self.assertTrue(res["cells"]["peeker@1.0|1h"]["bias"].startswith("lookahead on "))


class Docs(unittest.TestCase):
    def test_sources_recorded_before_use(self):
        from engine import curriculum as CU
        done = CU.studied(test_brain.read(os.path.join(ROOT, "memory", "research_sources.md")))
        self.assertIn("R3", done)
        self.assertIn("R5", done)


if __name__ == "__main__":
    unittest.main()
