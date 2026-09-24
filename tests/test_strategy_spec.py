"""Phase 7 tests: strategy spec v3 (ID cards, immutable versions, targets), lifecycle gates, market gates
(regime + timeframe permission), SMC strategy building blocks without look-ahead, and the whole engine.

Run:  python -m unittest discover -s tests -v
"""
import json
import os
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scanner  # noqa: E402
from engine import features as F  # noqa: E402
from engine import lifecycle as LC  # noqa: E402
from engine import regime as RG  # noqa: E402
from engine import smc as SMC  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402
from test_data_quality import run_copy, shared_offline_run  # noqa: E402

CFG = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
RAW = yaml.safe_load(open(os.path.join(ROOT, "strategies.yaml")))
LEGACY = {"trend_pullback": (1.5, 30), "donchian_breakout": (2.0, 60), "rsi2_dip_buy": (2.0, 15),
          "bb_squeeze_breakout": (1.5, 30), "macd_trend_cross": (1.5, 40), "supertrend_flip": (2.0, 60),
          "liquidity_sweep_reversal": (1.0, 20), "ema_9_21_cross": (1.5, 40)}


def card(**kw):
    base = dict(id="X1", version="1.0", status="FORMALIZED", family="trend_following", gate="trend",
                hypothesis="h", source="test", regimes=["STRONG_BULL"], timeframes=["1h"], long=["close > open"],
                short=["close < open"], stop=dict(method="atr", atr=1.0), time_stop_bars=10,
                known_weaknesses="w")
    base.update(kw)
    return base


class Library(unittest.TestCase):
    """The strategies.yaml shipped in the repo."""

    def test_every_card_is_valid(self):
        ok, problems, idle = SP.load(RAW, RG.LABELS, scanner.TF_ORDER)
        self.assertEqual(problems, {})
        self.assertEqual(len(ok), 20)
        ids = {s["id"] for s in ok}
        for sid in ("S5-SWEEP-MSS-FVG", "S6-OB-FVG", "S7-SILVER-BULLET", "S8-PDH-PDL-SWEEP"):
            self.assertIn(sid, ids)

    def test_legacy_strategies_keep_their_stop_and_hold_time(self):
        ok, _, _ = SP.load(RAW, RG.LABELS, scanner.TF_ORDER)
        by = {s["id"]: s for s in ok}
        for sid, (atr, bars) in LEGACY.items():
            self.assertEqual(by[sid]["stop"], dict(method="atr", atr=atr), sid)
            self.assertEqual(by[sid]["time_stop_bars"], bars, sid)
            self.assertEqual(by[sid]["cooldown_bars"], 0, sid)
            self.assertIsNone(by[sid].get("targets"), sid)          # still the config TP1/2/3 plan

    def test_every_smc_strategy_has_a_matching_control_twin(self):
        ok, _, _ = SP.load(RAW, RG.LABELS, scanner.TF_ORDER)
        by = {s["id"]: s for s in ok}
        mains = [s for s in ok if s["family"] == "smc" and not s.get("twin_of") and not s.get("confirm_5m")]
        self.assertEqual(len(mains), 4)
        for s in mains:
            tw = by[s["control_twin"]]
            self.assertEqual(tw["twin_of"], s["id"])
            for k in ("gate", "regimes", "timeframes", "targets", "time_stop_bars", "cooldown_bars"):
                self.assertEqual(tw.get(k), s.get(k), f"{s['id']} twin differs in {k}")
            self.assertNotEqual(tw["long"], s["long"])

    def test_mean_reversion_only_in_ranges(self):          # operator decision 3 (Phase 7 plan)
        for s in RAW:
            if s.get("gate") == "mean_reversion":
                self.assertTrue(set(s["regimes"]) <= {"RANGE", "HIGH_VOL_RANGE"}, s["id"])

    def test_no_5m_for_smc_and_5m_confirmation_only_on_the_5m_versions(self):   # operator decisions 4 + 5
        for s in RAW:
            self.assertEqual(bool(s.get("confirm_5m")), s["id"].endswith("-5M"), s["id"])   # Phase 10
            if s["family"] == "smc":
                self.assertNotIn("5m", s["timeframes"], s["id"])


class Cards(unittest.TestCase):
    def test_problems_are_reported_not_crashing(self):
        bad = [card(id="A", version=1.1), card(id="B", status="VALIDATION"), card(id="C", family="magic"),
               card(id="D", regimes=["MOON"]), card(id="E", confirm_5m=True), card(id="F", hypothesis=""),
               card(id="G", stop=dict(method="structure", long_level="low")),
               card(id="H", targets=dict(long=["2R"], short=["2R"], split=[0.5])),
               card(id="I", control_twin="NOPE")]
        ok, problems, _ = SP.load(bad, RG.LABELS, scanner.TF_ORDER)
        self.assertEqual(set(problems), {"B", "C", "D", "E", "F", "G", "H", "I"})
        self.assertEqual([s["id"] for s in ok], ["A"])             # 1.1 -> "1.1" is fine
        self.assertEqual(ok[0]["version"], "1.1")

    def test_idea_and_retired_are_not_run(self):
        ok, problems, idle = SP.load([card(id="A", status="IDEA"), card(id="B", status="RETIRED"), card(id="C")],
                                     RG.LABELS, scanner.TF_ORDER)
        self.assertEqual([s["id"] for s in ok], ["C"])
        self.assertEqual([s["id"] for s in idle], ["A", "B"])

    def test_fingerprint_sees_rules_not_words(self):
        a = card()
        self.assertEqual(SP.fingerprint(a), SP.fingerprint(card(hypothesis="other words", changelog=["x"])))
        self.assertNotEqual(SP.fingerprint(a), SP.fingerprint(card(long=["close > open", "volume > 0"])))
        self.assertNotEqual(SP.fingerprint(a), SP.fingerprint(card(stop=dict(method="atr", atr=1.1))))
        self.assertNotEqual(SP.fingerprint(a), SP.fingerprint(card(regimes=["STRONG_BULL", "RANGE"])))

    def test_registry_csv_round_trip(self):
        reg = LC.empty_registry()
        a, b = card(), card(id="Y", version="2.10")
        fps = {"X1@1.0": SP.fingerprint(a), "Y@2.10": SP.fingerprint(b)}
        reg, _, _ = LC.update(reg, [a, b], fps, {("X1", "1.0", "1h"): "FAILED", ("Y", "2.10", "4h"): "VALIDATION",
                                                ("Y", "2.10", "1h"): "BACKTESTING"}, "t")
        reg["cells"]["Y@2.10|4h"]["avg_r"] = 0.2
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "r.csv")
            LC.registry_to_frame(reg).to_csv(path, index=False)
            back = LC.registry_from_frame(pd.read_csv(path, dtype={"version": str}))
        self.assertEqual(back["versions"], reg["versions"])
        self.assertEqual(back["cells"]["Y@2.10|4h"]["avg_r"], 0.2)
        self.assertEqual({k: c["status"] for k, c in back["cells"].items()},
                         {k: c["status"] for k, c in reg["cells"].items()})
        _, _, changes = LC.update(back, [a, b], fps, {("X1", "1.0", "1h"): "FAILED"}, "t2")
        self.assertEqual(changes, [])                     # unchanged status -> nothing to log

    def test_tested_version_is_immutable(self):
        reg = LC.empty_registry()
        a = card()
        reg, new, _ = LC.update(reg, [a], {"X1@1.0": SP.fingerprint(a)}, {("X1", "1.0", "1h"): "BACKTESTING"}, "t")
        self.assertEqual(len(new), 1)
        self.assertIsNone(LC.immutable_problem(reg, a, SP.fingerprint(a)))
        edited = card(long=["close > open", "volume > 0"])
        msg = LC.immutable_problem(reg, edited, SP.fingerprint(edited))
        self.assertIn("1.0 -> 1.1", msg)
        v2 = card(version="1.1", long=["close > open", "volume > 0"])
        self.assertIsNone(LC.immutable_problem(reg, v2, SP.fingerprint(v2)))
        self.assertAlmostEqual(LC.retune_penalty(reg, v2, 0.02), 0.02)       # one earlier version
        self.assertAlmostEqual(LC.retune_penalty(reg, a, 0.02), 0.0)


class Targets(unittest.TestCase):
    TP = dict(tp_r=[1.0, 2.0, 3.0], tp_split=[0.4, 0.3, 0.3])

    def test_default_is_the_config_trade_plan(self):
        self.assertEqual(SP.targets(card(), 1, 100.0, 2.0, 0, {}, self.TP), ([102.0, 104.0, 106.0], [0.4, 0.3, 0.3]))
        self.assertEqual(SP.targets(card(), -1, 100.0, 2.0, 0, {}, self.TP)[0], [98.0, 96.0, 94.0])

    def test_pool_targets_and_the_2r_rule(self):
        c = card(targets=dict(long=["2R", "max(3R, pool)"], short=["2R", "max(3R, pool)"], split=[0.5, 0.5],
                              need=dict(long="pool", short="pool", min_r=2.0)))
        cols = {"pool": np.array([110.0, 104.5, 103.0, 90.0])}
        self.assertEqual(SP.targets(c, 1, 100.0, 1.0, 0, cols, self.TP)[0], [102.0, 110.0])   # pool farther
        self.assertEqual(SP.targets(c, 1, 100.0, 1.0, 1, cols, self.TP)[0], [102.0, 104.5])
        self.assertEqual(SP.targets(c, 1, 100.0, 2.0, 1, cols, self.TP)[0], [104.0, 106.0])   # 3R farther
        self.assertIsNone(SP.targets(c, 1, 100.0, 2.0, 2, cols, self.TP))         # pool only 1.5R away
        self.assertIsNone(SP.targets(c, 1, 100.0, 1.0, 3, cols, self.TP))         # pool on the wrong side
        self.assertEqual(SP.targets(c, -1, 100.0, 1.0, 3, cols, self.TP)[0], [98.0, 90.0])

    def test_levels_must_step_outwards(self):
        c = card(targets=dict(long=["mid", "top"], short=["mid", "bot"], split=[0.5, 0.5]))
        cols = {"mid": np.array([105.0, 99.0]), "top": np.array([110.0, 110.0]), "bot": np.array([90.0, 90.0])}
        self.assertEqual(SP.targets(c, 1, 100.0, 1.0, 0, cols, self.TP)[0], [105.0, 110.0])
        self.assertIsNone(SP.targets(c, 1, 100.0, 1.0, 1, cols, self.TP))         # middle already behind entry
        with self.assertRaises(ValueError):
            SP.parse_target("3 bananas")


class MarketGates(unittest.TestCase):
    def reg(self, **tfs):
        return {tf: (np.array(v, dtype=object), np.array([None] * len(v), dtype=object)) for tf, v in tfs.items()}

    def test_trend_needs_two_of_three_and_weekly_veto(self):
        s = card(regimes=list(RG.LABELS))
        reg = self.reg(**{"1d": ["WEAK_BULL"] * 3, "4h": ["STRONG_BULL", "RANGE", "WEAK_BULL"],
                          "1h": ["RANGE", "RANGE", "WEAK_BEAR"], "1w": [None, None, "STRONG_BEAR"]})
        gl, gs, *_ = LC.gate_arrays(s, "1h", reg, 3)
        self.assertEqual(gl.tolist(), [True, False, False])     # 2 bull / only 1 bull / weekly veto
        self.assertFalse(gs.any())
        gl_rev, *_ = LC.gate_arrays(dict(s, gate="reversal"), "1h", reg, 3)
        self.assertEqual(gl_rev.tolist(), [True, False, True])   # reversal types skip the weekly veto

    def test_expansion_counts_with_its_direction(self):
        reg = {"1d": (np.array(["EXPANSION", "EXPANSION"], dtype=object), np.array(["up", "down"], dtype=object)),
               "4h": (np.array(["WEAK_BULL", "WEAK_BULL"], dtype=object), np.array([None, None], dtype=object))}
        gl, *_ = LC.gate_arrays(card(regimes=list(RG.LABELS)), "4h", reg, 2)
        self.assertEqual(gl.tolist(), [True, False])

    def test_regime_list_on_the_right_timeframe(self):
        self.assertEqual([LC.regime_tf(t) for t in ("1d", "4h", "1h", "30m", "15m", "5m")],
                         ["1d", "4h", "1h", "1h", "1h", "1h"])
        reg = self.reg(**{"1d": ["WEAK_BULL"] * 2, "4h": ["WEAK_BULL", "RANGE"], "1h": ["STRONG_BULL", "WEAK_BULL"]})
        gl, _, reg_ok, *_ = LC.gate_arrays(card(regimes=["STRONG_BULL"]), "15m", reg, 2)   # 15m -> 1H regime
        self.assertEqual(reg_ok.tolist(), [True, False])
        self.assertEqual(gl.tolist(), [True, False])
        gl4, *_ = LC.gate_arrays(card(regimes=["WEAK_BULL"]), "4h", reg, 2)                # 4H -> 4H regime
        self.assertEqual(gl4.tolist(), [True, False])

    def test_mean_reversion_gate(self):
        s = card(gate="mean_reversion", regimes=["RANGE", "HIGH_VOL_RANGE"])
        reg = self.reg(**{"1h": ["RANGE", "RANGE", "WEAK_BULL", "RANGE"],
                          "4h": ["WEAK_BEAR", "STRONG_BEAR", "RANGE", "RANGE"],
                          "1d": ["RANGE", "RANGE", "RANGE", "RANGE"], "1w": [None, None, None, "STRONG_BULL"]})
        gl, gs, *_ = LC.gate_arrays(s, "1h", reg, 4)
        self.assertEqual(gl.tolist(), [True, False, False, True])   # never long against a STRONG_BEAR 4H
        self.assertEqual(gs.tolist(), [True, True, False, False])   # never short against a STRONG_BULL 1W

    def test_missing_timeframes_mean_no_permission(self):
        gl, gs, *_ = LC.gate_arrays(card(regimes=list(RG.LABELS) + [None]), "1h", {}, 2)
        self.assertFalse(gl.any() or gs.any())


class Judge(unittest.TestCase):
    V = CFG["validation"]

    def st(self, n, exp, pf=2.0, dd=2.0):
        return dict(n=n, exp_r=exp, pf=pf, max_dd_r=dd)

    def test_gate(self):
        ok = self.st(40, 0.2)
        self.assertEqual(LC.judge(ok, self.st(28, 0.2), self.st(12, 0.2), None, self.V)[0], "VALIDATION")
        self.assertEqual(LC.judge(self.st(40, 0.08), self.st(28, 0.1), self.st(12, 0.05), None, self.V)[0],
                         "BACKTESTING")                                        # below +0.10R
        self.assertEqual(LC.judge(self.st(40, 0.2, dd=11), self.st(28, 0.2), self.st(12, 0.2), None, self.V)[0],
                         "BACKTESTING")                                        # drawdown > 10R
        self.assertEqual(LC.judge(self.st(12, 0.5), self.st(8, 0.5), self.st(4, 0.5), None, self.V)[0],
                         "BACKTESTING")                                        # too few trades
        self.assertEqual(LC.judge(self.st(40, -0.1, pf=0.8), self.st(28, 0), self.st(12, -0.2), None, self.V)[0],
                         "FAILED")
        live_bad = dict(n=25, exp_r=-0.3)
        self.assertEqual(LC.judge(ok, self.st(28, 0.2), self.st(12, 0.2), live_bad, self.V)[0], "FAILED")
        status, reasons, need = LC.judge(ok, self.st(28, 0.2), self.st(12, 0.2), None, self.V, penalty_r=0.12)
        self.assertEqual((status, round(need, 2)), ("BACKTESTING", 0.22))       # re-tuning raises the bar
        self.assertNotIn("PAPER_TRADING", [LC.judge(ok, ok, ok, None, self.V)[0]])  # needs Phase 8


class RuleHelpers(unittest.TestCase):
    def test_within_and_bars_since(self):
        df = pd.DataFrame({"open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": 1.0}, index=range(6))
        ns = scanner.make_namespace(df)
        x = pd.Series([False, True, False, False, True, False])
        self.assertEqual(ns["within"](x, 2).tolist(), [False, True, True, False, True, True])
        np.testing.assert_array_equal(ns["bars_since"](x).to_numpy(), [np.nan, 0, 1, 2, 0, 1])


def candles(rows, tf=900_000):
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"])
    df["volume"] = 1.0
    df["open_time"] = tf * np.arange(len(df))
    df["close_time"] = df["open_time"] + tf - 1
    df["_atr"] = 1.0
    return df


class Backtest(unittest.TestCase):
    def test_structure_stop_next_open_and_cooldown(self):
        rows = [(100, 100.5, 99.5, 100)] * 40
        rows[11] = (101, 104, 100.8, 103.5)            # candle after the first signal runs to +2R quickly
        df = candles(rows)
        s = card(stop=dict(method="structure", long_level="lvl", short_level="lvl", buffer_atr=0.2,
                           max_width_atr=3.0),
                 targets=dict(long=["2R"], short=["2R"], split=[1.0]), cooldown_bars=5, time_stop_bars=10)
        lvl = np.full(40, 99.8)
        L = np.zeros(40, bool)
        L[[10, 12, 20]] = True                          # 12 comes during the cooldown -> ignored
        tr = scanner.backtest(df, L, np.zeros(40, bool), None, None, s, CFG, "15m", {"lvl": lvl})
        self.assertEqual([t["entry_idx"] for t in tr], [11, 21])
        entry = 101 * (1 + CFG["costs"]["long"]["slippage_pct"] / 100)
        R = entry - (99.8 - 0.2)
        self.assertEqual(tr[0]["reason"], "TP1")
        self.assertAlmostEqual(tr[0]["r"] + 0, (2 * R - (entry * 0.001 + (entry + 2 * R) * 0.001)) / R, places=6)

    def test_setups_without_a_valid_stop_or_target_are_skipped_and_counted(self):
        df = candles([(100, 100.5, 99.5, 100)] * 30)
        s = card(stop=dict(method="structure", long_level="lvl", short_level="lvl", max_width_atr=3.0),
                 targets=dict(long=["pool"], short=["pool"], split=[1.0],
                              need=dict(long="pool", short="pool", min_r=2.0)))
        lvl = np.full(30, 99.0)
        lvl[5] = 95.0                                     # stop 5 ATR away: too wide
        lvl[7] = 101.0                                    # stop above a long entry: wrong side
        pool = np.full(30, 101.0)                          # the pool is only ~0.9R away
        L = np.zeros(30, bool)
        L[[5, 7, 9]] = True
        skipped = {}
        tr = scanner.backtest(df, L, np.zeros(30, bool), None, None, s, CFG, "15m",
                              {"lvl": lvl, "pool": pool}, skipped)
        self.assertEqual(tr, [])
        self.assertEqual(skipped, {"stop": 2, "target": 1})


class NoLookAhead(unittest.TestCase):
    """New SMC context columns and the h4_* columns must not use later candles."""

    def test_smc_context_known_at_close(self):
        feed = scanner.Synthetic()
        df = feed.klines("BTCUSDT", "15m", 1500)
        daily, weekly = feed.klines("BTCUSDT", "1d", 300), feed.klines("BTCUSDT", "1w", 100)
        full = SMC.detect(df, F.compute(df, 900_000), daily, weekly, 900_000)["series"]
        for cut in (401, 877, 1203):
            part = df.iloc[:cut]
            past = SMC.detect(part, F.compute(part, 900_000), daily, weekly, 900_000)["series"]
            pd.testing.assert_frame_equal(full[SMC.CONTEXT_COLUMNS].iloc[:cut], past[SMC.CONTEXT_COLUMNS],
                                          obj=f"cut {cut}")
        self.assertTrue(full["range_pos"].notna().any() and full["liq_above"].notna().any())
        self.assertTrue(full["in_killzone"].any() and not full["in_killzone"].all())
        # every value describes THIS candle's close: pools above/below it, its place in the range
        c = df["close"].to_numpy()
        up, dn = full["liq_above"].to_numpy(), full["liq_below"].to_numpy()
        self.assertTrue((up[np.isfinite(up)] > c[np.isfinite(up)]).all())
        self.assertTrue((dn[np.isfinite(dn)] < c[np.isfinite(dn)]).all())
        pos = (c - full["range_low"]) / (full["range_high"] - full["range_low"])
        np.testing.assert_allclose(full["range_pos"].dropna(), pos[full["range_pos"].notna()])

    def test_newest_candle_context_many_cuts(self):
        """The NEWEST candle is what live signals use: its context must equal the full-history value."""
        feed = scanner.Synthetic()
        df = feed.klines("ETHUSDT", "30m", 700)
        daily, weekly = feed.klines("ETHUSDT", "1d", 200), feed.klines("ETHUSDT", "1w", 60)
        full = SMC.detect(df, F.compute(df, 1_800_000), daily, weekly, 1_800_000)["series"]
        for cut in range(300, 701, 8):
            part = df.iloc[:cut]
            last = SMC.detect(part, F.compute(part, 1_800_000), daily, weekly, 1_800_000)["series"].iloc[-1]
            pd.testing.assert_series_equal(last[SMC.CONTEXT_COLUMNS], full[SMC.CONTEXT_COLUMNS].iloc[cut - 1],
                                           check_names=False, obj=f"cut {cut}")

    def test_h4_context_uses_closed_4h_candles_only(self):
        feed = scanner.Synthetic()
        d15, d4 = feed.klines("BTCUSDT", "15m", 1200), feed.klines("BTCUSDT", "4h", 400)
        f15 = pd.DataFrame(index=d15.index)
        f4 = pd.DataFrame({"smc_" + c: np.arange(len(d4), dtype=float) for c in scanner.H4_CONTEXT})
        frames = {"15m": (d15, f15), "4h": (d4, f4)}
        scanner.add_h4_context(frames)
        ct4 = d4["close_time"].to_numpy()
        for i in (100, 555, 1001):
            closed = np.flatnonzero(ct4 <= d15["close_time"].iloc[i])
            want = float(closed[-1]) if len(closed) else np.nan
            self.assertEqual(f15["h4_bull_ob_low"].iloc[i], want)
            self.assertTrue(ct4[int(want)] <= d15["close_time"].iloc[i])
        del frames["4h"]                                       # no 4H data -> empty columns, no crash
        f15b = pd.DataFrame(index=d15.index)
        scanner.add_h4_context({"15m": (d15, f15b)})
        self.assertTrue(f15b["h4_range_low"].isna().all())


class EndToEnd(unittest.TestCase):
    """The hourly scan with the Phase 7 gates (the research run itself: tests/test_research.py)."""

    def test_offline_scan_gates_and_report(self):
        tmp, p = shared_offline_run()          # one plain offline scan, shared (read-only)
        if True:
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            with open(os.path.join(tmp, "reports", "latest.json")) as f:
                out = json.load(f)
            board = out["strategy_scoreboard"]
            self.assertTrue(board)
            # no research run yet: every version waits as FORMALIZED and nothing can signal
            self.assertEqual({b["status"] for b in board}, {"FORMALIZED"})
            self.assertEqual(out["signals"], [])
            self.assertEqual(out["validation_signals"], [])
            self.assertTrue(any(b["strategy"].startswith("S5") for b in board))
            self.assertTrue(any(b["blocked_by_regime"] + b["blocked_by_permission"] > 0 for b in board))
            self.assertEqual(out["lifecycle"]["not_run"], {})
            self.assertEqual(out["lifecycle"]["rule_errors"], {})
            self.assertFalse(os.path.exists(os.path.join(tmp, "memory")))   # offline never writes memory/
            with open(os.path.join(tmp, "reports", "latest.md")) as f:
                md = f.read()
            for text in ("## 3. Strategy scoreboard", "### 3b. Strategy lifecycle", "SMC vs control twin",
                         "waiting for the first daily research run",
                         "**Storage:** repository not checked (offline)", "branch `live-reports`",
                         "/blob/live-reports/reports/latest.json"):
                self.assertIn(text, md)


if __name__ == "__main__":
    unittest.main()
