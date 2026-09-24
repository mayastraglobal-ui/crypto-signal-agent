"""Phase 8 tests: long-history cache, research layers (A/B/C), cost viability, costs +50%, +-20% test,
overfitting flag, control twin, the PAPER_TRADING gate and the freeze rules, and the daily run end to end.

Run:  python -m unittest discover -s tests -v
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import research  # noqa: E402
import scanner  # noqa: E402
from engine import history as H  # noqa: E402
from engine import lifecycle as LC  # noqa: E402
from engine import regime as RG  # noqa: E402
from engine import research as RS  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402

CFG = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
R, V = CFG["research"], CFG["validation"]
RAW = yaml.safe_load(open(os.path.join(ROOT, "strategies.yaml")))
DAY, H1 = 86_400_000, 3_600_000
# fingerprints of the tested v1.0 cards (Phase 7 + 10). Turning numbers into {params} must not change them.
FROZEN = {
    "trend_pullback@1.0": "8a44ad271501a1e0", "donchian_breakout@1.0": "16bf4b27106859c9",
    "rsi2_dip_buy@1.0": "80f89b0ee2f96e4e", "bb_squeeze_breakout@1.0": "7ed0a9a3cc499679",
    "macd_trend_cross@1.0": "6a3c81e197391ab9", "supertrend_flip@1.0": "e208c9fdd9dec25b",
    "liquidity_sweep_reversal@1.0": "87de3b4c3b4aef5b", "ema_9_21_cross@1.0": "805776176a3ea9f7",
    "S5-SWEEP-MSS-FVG@1.0": "e5b96d987fa6faa1", "S5-SWEEP-MSS-FVG-noSMC@1.0": "0b58800aaa3e6011",
    "S6-OB-FVG@1.0": "7cd5cecc6e32325b", "S6-OB-FVG-noSMC@1.0": "3625bec421c0fc06",
    "S7-SILVER-BULLET@1.0": "898cf8575314471e", "S7-SILVER-BULLET-noSMC@1.0": "afa15a7a4ae803d4",
    "S8-PDH-PDL-SWEEP@1.0": "742b8bd48603d659", "S8-PDH-PDL-SWEEP-noSMC@1.0": "651c1e2ec3e0594c",
    # Phase 10: the 5-minute confirmation versions
    "S5-SWEEP-MSS-FVG-5M@1.0": "f9d1c2e50f046b7d", "S6-OB-FVG-5M@1.0": "a9e6bcfa6fe62d0c",
    "S7-SILVER-BULLET-5M@1.0": "40a897f8c1b3aed2", "S8-PDH-PDL-SWEEP-5M@1.0": "f0aeec94c99360d9",
}


def trade(r, t, coin="BTC", d=1, oos=False, cost_r=0.1):
    return dict(r=r, entry_time=t, coin=coin, dir=d, oos=oos, bars=5, cost_r=cost_r)


class Params(unittest.TestCase):
    def test_templating_kept_every_tested_version_identical(self):
        ok, problems, _ = SP.load(RAW, RG.LABELS, scanner.TF_ORDER)
        self.assertEqual(problems, {})
        self.assertEqual({SP.key(s): SP.fingerprint(s) for s in ok}, FROZEN)

    def test_render_and_checks(self):
        c = dict(id="X", version="1.0", status="FORMALIZED", family="trend_following", gate="trend", hypothesis="h",
                 source="s", regimes=["STRONG_BULL"], timeframes=["1h"], long=["ema(close,{fast}) > {lvl}"],
                 short=["close < open"], stop=dict(method="atr", atr=1.5), time_stop_bars=10, known_weaknesses="w",
                 params=dict(fast=20, lvl=1.5))
        self.assertEqual(SP.render(c)["long"], ["ema(close,20) > 1.5"])
        self.assertEqual(SP.render(c, {"fast": 16})["long"], ["ema(close,16) > 1.5"])
        self.assertEqual(SP.check(c, RG.LABELS, scanner.TF_ORDER), [])
        self.assertTrue(any("does not define" in e for e in SP.check(dict(c, params=dict(fast=20)), RG.LABELS,
                                                                        scanner.TF_ORDER)))
        self.assertTrue(any("not used" in e for e in SP.check(dict(c, params=dict(fast=20, lvl=1, x=3)), RG.LABELS,
                                                                 scanner.TF_ORDER)))
        self.assertTrue(any("positive" in e for e in SP.check(dict(c, params=dict(fast=20, lvl=-1)), RG.LABELS,
                                                                 scanner.TF_ORDER)))

    def test_nudge(self):
        self.assertEqual((SP.nudge(20, 0.8), SP.nudge(20, 1.2)), (16, 24))
        self.assertEqual((SP.nudge(2, 0.8), SP.nudge(2, 1.2)), (1, 3))          # whole numbers always move
        self.assertEqual((SP.nudge(1, 0.8), SP.nudge(1.5, 1.2)), (1, 1.8))       # never below 1
        self.assertEqual(SP.nudge(0.2, 0.8), 0.16)

    def test_variants_one_at_a_time(self):
        ok, _, _ = SP.load(RAW, RG.LABELS, scanner.TF_ORDER)
        tp = next(s for s in ok if s["id"] == "trend_pullback")
        vs = SP.variants(tp, 20)
        self.assertEqual(len(vs), 2 * (7 + 1 + 1))                 # 7 params + stop + time stop, down and up
        by = {label: (v, changed) for label, v, changed in vs}
        v, changed = by["fast 20→16"]
        self.assertTrue(changed)
        self.assertIn("ema(close,16) > ema(close,50)", v["long"])
        self.assertEqual(v["stop"], tp["stop"])                    # only ONE thing changes
        v, changed = by["stop atr 1.5→1.8"]
        self.assertFalse(changed)
        self.assertEqual((v["stop"]["atr"], v["long"]), (1.8, tp["long"]))
        self.assertEqual(by["time_stop_bars 30→24"][0]["time_stop_bars"], 24)
        s5 = next(s for s in ok if s["id"] == "S5-SWEEP-MSS-FVG")
        labels = [x[0] for x in SP.variants(s5, 20)]
        self.assertIn("stop buffer_atr 0.2→0.24", labels)
        self.assertIn("stop max_width_atr 3.0→2.4", labels)
        self.assertTrue(all(v["version"] == s5["version"] for _, v, _ in SP.variants(s5, 20)))


class RegistryFormat(unittest.TestCase):
    def test_reads_a_phase7_registry(self):
        old_cols = ["id", "version", "family", "fingerprint", "experiment", "first_tested_utc", "hypothesis", "tf",
                    "status", "since_utc", "last_checked_utc", "trades", "avg_r", "profit_factor", "max_dd_r",
                    "train_avg_r", "test_avg_r", "required_avg_r", "beats_twin", "gates_failed"]
        row = ["trend_pullback", "1.0", "mtf_pullback", FROZEN["trend_pullback@1.0"], 1, "2026-09-24 20:17", "h",
               "1h", "FAILED", "2026-09-24 20:17", "2026-09-24 20:17", 40, -0.1, 0.8, 5.0, 0.0, -0.2, 0.1, "",
               "avg -0.10R/trade"]
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "r.csv")
            pd.DataFrame([row], columns=old_cols).to_csv(path, index=False)
            reg = LC.registry_from_frame(pd.read_csv(path, dtype={"version": str}))
        cell = reg["cells"]["trend_pullback@1.0|1h"]
        self.assertEqual((cell["status"], cell["failed_runs"]), ("FAILED", None))
        ok, _, _ = SP.load(RAW, RG.LABELS, scanner.TF_ORDER)
        tp = next(s for s in ok if s["id"] == "trend_pullback")
        self.assertIsNone(LC.immutable_problem(reg, tp, SP.fingerprint(tp)))   # still the same tested version


class FakeFeed:
    """Candles 'now' on a fixed grid; counts how many candles each request asked for."""

    def __init__(self, now_ms, tf="1h"):
        self.now, self.tf, self.asked = now_ms, tf, []

    def klines(self, symbol, tf, n):
        self.asked.append(n)
        step = scanner.TF_MS[tf]
        last = self.now // step * step
        ot = last - step * np.arange(n - 1, -1, -1)
        price = 100 + (ot // step % 50).astype(float)
        return pd.DataFrame({"open_time": ot, "open": price, "high": price + 1, "low": price - 1, "close": price,
                             "volume": 1.0, "quote_volume": 100.0})


class HistoryCache(unittest.TestCase):
    def test_full_then_incremental_then_deeper(self):
        now = 1_790_000_000_000
        with tempfile.TemporaryDirectory() as tmp:
            f = FakeFeed(now)
            df, how = H.update(f, "BTCUSDT", "1h", 500, now, tmp)
            self.assertEqual((len(df), how, f.asked), (500, "full download", [500]))
            f.now = now + 3 * H1                                        # three hours later
            df2, how = H.update(f, "BTCUSDT", "1h", 500, f.now, tmp)
            self.assertEqual(f.asked[-1], 5)                           # only the missing candles (+2 overlap)
            self.assertEqual(len(df2), 500)
            self.assertTrue(df2["open_time"].is_monotonic_increasing and df2["open_time"].is_unique)
            self.assertEqual(int(df2["open_time"].iloc[-1]), f.now // H1 * H1)
            self.assertEqual(list(df2["close_time"] - df2["open_time"]), [H1 - 1] * 500)
            H.update(f, "BTCUSDT", "1h", 800, f.now, tmp)               # deeper history wanted -> full again
            self.assertEqual(f.asked[-1], 800)
            f.now += 400 * DAY                                         # cache far too old -> full again
            H.update(f, "BTCUSDT", "1h", 800, f.now, tmp)
            self.assertEqual(f.asked[-1], 800)

    def test_no_cache_folder_means_plain_download(self):
        f = FakeFeed(1_790_000_000_000)
        df, how = H.update(f, "BTCUSDT", "1h", 50, f.now, None)
        self.assertEqual((len(df), how), (50, "no cache"))


class Layers(unittest.TestCase):
    def test_stats_in_time_order(self):
        # listed coin by coin (+5 first) the drawdown would be 2R; in clock order it is only 1R
        tr = [trade(5, 2, "B"), trade(-1, 1, "A"), trade(-1, 3, "A")]
        self.assertEqual(RS.stats(tr)["max_dd_r"], 1.0)

    def test_layer_a_split(self):
        now = 100 * DAY
        tr = [trade(1, now - 20 * DAY), trade(-1, now - 14 * DAY), trade(0.5, now - 6 * DAY), trade(2, now - 2 * DAY)]
        a = RS.layer_a(tr, now, 15, 10)
        self.assertEqual((a["all"]["n"], a["first"]["n"], a["last"]["n"]), (3, 2, 1))
        self.assertEqual(a["last"]["avg_r"], 2.0)

    def test_walk_forward(self):
        wins = RS.windows(0, 600, 6)
        self.assertEqual(wins[0], (0, 100))
        good = [trade(1, 100 * w + k) for w in range(1, 6) for k in range(5)]
        wf = RS.walk_forward(good + [trade(-50, 5)], wins, 5, 3)   # a disaster in the warm-up window is ignored
        self.assertEqual((wf["positive"], wf["judged"], wf["passed"]), (5, 5, True))
        thin = [trade(1, 100 * w + k) for w in (1, 2) for k in range(5)] + [trade(1, 350)] * 4 + \
               [trade(-0.2, 450 + k) for k in range(5)] + [trade(1, 550)]
        wf = RS.walk_forward(thin, wins, 5, 3)
        self.assertEqual([r["verdict"] for r in wf["windows"]],
                         ["warm-up", "profitable", "profitable", "too few trades", "losing", "too few trades"])
        self.assertFalse(wf["passed"])                            # only 2 of 5
        # 3 of 5 windows a little profitable, 2 windows losing a lot: together losing -> fail
        mixed = [trade(0.1, 100 * w + k) for w in (1, 2, 3) for k in range(5)] + \
                [trade(-1.0, 100 * w + k) for w in (4, 5) for k in range(5)]
        wf = RS.walk_forward(mixed, wins, 5, 3)
        self.assertEqual(wf["positive"], 3)
        self.assertLess(wf["pooled_avg_r"], 0)
        self.assertFalse(wf["passed"])

    def test_concentration_and_overfit(self):
        self.assertEqual(RS.concentration({"A": 6, "B": 2, "C": -3}), ("A", 0.75))
        self.assertEqual(RS.concentration({"A": -1}), (None, 0.0))

    def evaluate(self, per, stress=None, variants=None):
        packed = lambda pc: {c: (len(tr), sum(t["r"] for t in tr)) for c, tr in pc.items()}
        variants = {k: packed(v) for k, v in (variants or {"x": per}).items()}
        return RS.evaluate(per, stress or per, variants, RS.windows(0, 600, 6), R, 5)

    def spread(self, r=0.5, coins=("A", "B", "C", "D")):
        return {c: [trade(r, 100 + 20 * k + i, c, oos=k >= 20) for k in range(25)] for i, c in enumerate(coins)}

    def test_evaluate(self):
        ev = self.evaluate(self.spread())
        self.assertEqual(ev["positive_coins"], ["A", "B", "C", "D"])
        self.assertEqual(ev["overfit"], [])
        self.assertTrue(ev["perturbation"]["stable"])
        self.assertEqual(ev["median_cost_r"], 0.1)
        one = self.spread()
        one["A"] = [dict(t, r=20.0) for t in one["A"]]
        for c in "BCD":
            one[c] = [dict(t, r=0.01) for t in one[c]]
        self.assertTrue(any("from A" in x for x in self.evaluate(one)["overfit"]))
        bad_var = {"fast 20→16": self.spread(-0.1), "fast 20→24": self.spread(0.4)}
        ev = self.evaluate(self.spread(), variants=bad_var)
        self.assertFalse(ev["perturbation"]["stable"])
        self.assertEqual(ev["perturbation"]["worst"]["change"], "fast 20→16")
        self.assertFalse(self.evaluate(self.spread(), variants={"v": {}})["perturbation"]["stable"])   # 0 trades

    def test_stressed_costs(self):
        c = research.stressed(CFG, 1.5)
        self.assertAlmostEqual(c["costs"]["long"]["taker_fee_pct"], CFG["costs"]["long"]["taker_fee_pct"] * 1.5)
        self.assertAlmostEqual(c["costs"]["short"]["funding_pct_per_8h"],
                               CFG["costs"]["short"]["funding_pct_per_8h"] * 1.5)
        self.assertNotEqual(c["costs"]["long"]["slippage_pct"], CFG["costs"]["long"]["slippage_pct"])


class Gates(unittest.TestCase):
    def ev(self, **kw):
        base = dict(all=dict(n=60, avg_r=0.3), validate=dict(n=20, avg_r=0.3), positive_coins=["A", "B", "C"],
                    walk_forward=dict(passed=True, positive=4, judged=5, pooled_avg_r=0.3),
                    stress=dict(avg_r=0.1), perturbation=dict(stable=True, worst=None), overfit=[])
        base.update(kw)
        return base

    def test_cost_viability_is_part_of_validation(self):
        st = dict(n=40, exp_r=0.3, pf=2.0, max_dd_r=3.0)
        ok = dict(n=28, exp_r=0.3)
        oos = dict(n=12, exp_r=0.3)
        self.assertEqual(LC.judge(st, ok, oos, None, V, 0, 0.2)[0], "VALIDATION")
        status, reasons, _ = LC.judge(st, ok, oos, None, V, 0, 0.3)       # fees eat > 1/4 of the stop
        self.assertEqual(status, "BACKTESTING")
        self.assertIn("not cost-viable", reasons[0])

    def test_paper_gate_each_condition(self):
        self.assertEqual(LC.paper_gate("VALIDATION", self.ev(), None, R), (True, []))
        cases = {"not in VALIDATION": ("BACKTESTING", self.ev()),
                 "walk-forward": ("VALIDATION", self.ev(walk_forward=dict(passed=False, positive=2, judged=5,
                                                                          pooled_avg_r=0.1))),
                 "coin": ("VALIDATION", self.ev(positive_coins=["A", "B"])),
                 "costs +50%": ("VALIDATION", self.ev(stress=dict(avg_r=-0.01))),
                 "±20%": ("VALIDATION", self.ev(perturbation=dict(stable=False,
                                                                  worst=dict(change="fast 20→16", avg_r=-0.1)))),
                 "OVERFITTING": ("VALIDATION", self.ev(overfit=["70% of the profit from A"]))}
        for word, (status, ev) in cases.items():
            ok, reasons = LC.paper_gate(status, ev, None, R)
            self.assertFalse(ok, word)
            self.assertTrue(any(word in r for r in reasons), (word, reasons))

    def test_control_twin(self):
        me = self.ev()
        worse = self.ev(all=dict(n=60, avg_r=0.1), validate=dict(n=20, avg_r=0.1))
        better = self.ev(all=dict(n=60, avg_r=0.5), validate=dict(n=20, avg_r=0.2))
        self.assertTrue(LC.twin_compare(me, worse, R))
        self.assertFalse(LC.twin_compare(me, better, R))                  # must win in BOTH parts
        late = self.ev(all=dict(n=60, avg_r=0.1), validate=dict(n=20, avg_r=0.4))   # twin better in validate
        self.assertFalse(LC.twin_compare(me, late, R))
        self.assertIsNone(LC.twin_compare(me, self.ev(all=dict(n=10, avg_r=0.0)), R))
        self.assertTrue(LC.paper_gate("VALIDATION", me, worse, R)[0])
        self.assertFalse(LC.paper_gate("VALIDATION", me, better, R)[0])

    def test_lifecycle_moves(self):
        none = LC.paper_record([])
        self.assertEqual(LC.next_status("VALIDATION", "VALIDATION", True, none, 0, R)[0], "PAPER_TRADING")
        self.assertEqual(LC.next_status(None, "VALIDATION", False, none, 0, R)[0], "VALIDATION")
        self.assertEqual(LC.next_status("BACKTESTING", "FAILED", False, none, 0, R)[0], "FAILED")
        # in paper: one failed long-history run is tolerated, the second one demotes
        st, note, runs = LC.next_status("PAPER_TRADING", "BACKTESTING", False, none, 0, R)
        self.assertEqual((st, runs), ("PAPER_TRADING", 1))
        st, note, runs = LC.next_status("PAPER_TRADING", "BACKTESTING", False, none, 1, R)
        self.assertEqual((st, runs), ("BACKTESTING", 0))
        self.assertEqual(LC.next_status("PAPER_TRADING", "VALIDATION", False, none, 1, R)[:3:2], ("PAPER_TRADING", 0))
        # freeze rules from the paper record
        bad = LC.paper_record([0.5] * 5 + [-0.3] * 20)
        self.assertEqual(LC.next_status("PAPER_TRADING", "VALIDATION", True, bad, 0, R)[0], "RETIRED")
        deep = LC.paper_record([1.0] * 3 + [-1.0] * 9)                   # 9R down from the best point
        self.assertEqual(LC.next_status("PAPER_TRADING", "VALIDATION", True, deep, 0, R)[0], "RETIRED")
        fine = LC.paper_record([1.0, -1.0] * 12)
        self.assertEqual(LC.next_status("PAPER_TRADING", "VALIDATION", True, fine, 0, R)[0], "PAPER_TRADING")
        self.assertEqual(LC.next_status("RETIRED", "VALIDATION", True, none, 0, R)[0], "RETIRED")
        for prev in (None, "BACKTESTING", "VALIDATION", "PAPER_TRADING"):
            for base in ("BACKTESTING", "VALIDATION", "FAILED"):
                self.assertNotEqual(LC.next_status(prev, base, True, none, 0, R)[0], "APPROVED")


def run(tmp, script, *args):
    return subprocess.run([sys.executable, script, "--offline", *args], cwd=tmp, capture_output=True, text=True,
                          timeout=900)


class EndToEnd(unittest.TestCase):
    def test_scan_research_scan(self):
        from test_data_quality import run_copy
        with tempfile.TemporaryDirectory() as tmp:
            p = run_copy(tmp, "scanner.py", "--offline", "--coins", "3")
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            import shutil
            shutil.copy(os.path.join(ROOT, "research.py"), tmp)
            p = run(tmp, "research.py", "--coins", "3")
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            with open(os.path.join(tmp, "reports", "research_offline.json")) as f:
                res = json.load(f)
            self.assertEqual(len(res["coins"]), 3)
            self.assertEqual(res["not_run"], {})
            cell = res["cells"]["trend_pullback@1.0|1h"]
            for k in ("all", "develop", "validate", "long", "short", "by_coin", "walk_forward", "stress",
                      "perturbation", "median_cost_r", "overfit"):
                self.assertIn(k, cell["evidence"])
            self.assertEqual(len(cell["evidence"]["walk_forward"]["windows"]), R["walk_forward_windows"])
            self.assertEqual(len(cell["evidence"]["perturbation"]["variants"]), 18)
            self.assertIn(cell["status"], LC.ENGINE_STATUSES)
            a = cell["attribution"]                                   # Phase 9: why trades lose
            self.assertEqual(a["losses"] + a["wins"], cell["evidence"]["all"]["n"])
            self.assertGreaterEqual(len(a["diagnosis"]), 6)
            for k in ("tags", "systematic", "mae_mfe", "by_regime", "by_session", "by_direction", "not_measurable"):
                self.assertIn(k, a)
            self.assertIn("missed_moves", res)
            self.assertIn("candidate_lessons", res)
            self.assertFalse(any(c["status"] == "APPROVED" for c in res["cells"].values()))
            reg = pd.read_csv(os.path.join(tmp, "reports", "strategy_registry_offline.csv"), dtype={"version": str})
            self.assertEqual(len(reg), len(res["cells"]))
            self.assertFalse(os.path.exists(os.path.join(tmp, "memory")))       # offline never writes memory/

            p = run(tmp, "scanner.py", "--coins", "3")                            # hourly scan reads the results
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            with open(os.path.join(tmp, "reports", "latest.json")) as f:
                out = json.load(f)
            self.assertEqual(out["lifecycle"]["research_run"], res["run_utc"])
            row = next(b for b in out["strategy_scoreboard"] if b["strategy"] == "trend_pullback" and b["tf"] == "1h")
            self.assertTrue(row["researched"])
            self.assertEqual(row["status"], cell["status"])
            self.assertEqual(row["trades"], cell["evidence"]["all"]["n"])
            self.assertEqual(out["signals"], [])                                   # nothing is APPROVED
            with open(os.path.join(tmp, "reports", "latest.md")) as f:
                md = f.read()
            self.assertIn("### 3c. Research layers (daily run)", md)
            self.assertIn("### 3d. Why trades lose", md)
            self.assertIn("Layer A", md)

            # a tested version edited in place is refused by BOTH runs
            with open(os.path.join(tmp, "strategies.yaml")) as f:
                raw = yaml.safe_load(f)
            edited = copy.deepcopy(raw)
            edited[0]["params"]["fast"] = 21
            with open(os.path.join(tmp, "strategies.yaml"), "w") as f:
                yaml.safe_dump(edited, f, sort_keys=False)
            for script in ("research.py", "scanner.py"):
                p = run(tmp, script, "--coins", "3")
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            with open(os.path.join(tmp, "reports", "research_offline.json")) as f:
                self.assertIn("trend_pullback", json.load(f)["not_run"])
            with open(os.path.join(tmp, "reports", "latest.json")) as f:
                self.assertIn("trend_pullback", json.load(f)["lifecycle"]["not_run"])


if __name__ == "__main__":
    unittest.main()
