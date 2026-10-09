"""The Forward Test Program (operator plan 2026-10-09): 10 strategies x 4 versions in strategies_program.yaml, the
4H + 1H market gates (1W / 1D context only), the session and regime-direction building blocks, the trailing ATR exit,
the nightly batches with carried results, and the per-coin results file (after and before fees)."""
import copy
import re
import os
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import memory_guard  # noqa: E402
import scanner as sc  # noqa: E402
from engine import ideas  # noqa: E402
from engine import lifecycle as LC  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import manage as mg  # noqa: E402
from engine import program as PG  # noqa: E402
from engine import regime as RG  # noqa: E402
from engine import sessions as SS  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
with open(os.path.join(ROOT, SP.PROGRAM_FILE)) as f:
    RAW = yaml.safe_load(f)
H = 3_600_000


def loaded():
    ok, problems, _, _ = sc.load_cards()
    return [c for c in ok if PG.is_program(c)], problems


class Cards(unittest.TestCase):
    def test_forty_cards_load_and_are_lab_cards(self):
        cards, problems = loaded()
        self.assertFalse({k: v for k, v in problems.items() if str(k).startswith("program")})
        self.assertEqual(len(cards), 47)                                    # 10 x V1-V4 + 7 V5 (2026-10-09)
        self.assertTrue(all(c["lab"] for c in cards))                       # never APPROVED from this file
        self.assertEqual(sorted({PG.number(c) for c in cards}), list(range(1, 11)))
        self.assertEqual(sum(len(c["timeframes"]) for c in cards), 79)
        self.assertEqual(len({c["id"] for c in cards}), 47)

    def test_each_version_differs_from_v1_in_one_way(self):
        by = {(c["program"]["strategy"], c["program"]["version"]): c for c in RAW}
        for n in range(1, 11):
            v1, v2, v3, v4 = (by[(n, v)] for v in ("V1", "V2", "V3", "V4"))
            self.assertNotIn(v1["timeframes"][0], v2["timeframes"])
            self.assertTrue(set(v2["timeframes"]) <= {"1h", "30m", "15m"})
            self.assertEqual(v3["long"], v1["long"] + ["dir_1d > 0"])
            self.assertEqual(v3["short"], v1["short"] + ["dir_1d < 0"])
            self.assertEqual(v4["manage"], {"trail": {"atr_n": 22, "atr_x": 3.0}})
            self.assertEqual(v4["targets"]["long"], ["2R", "10R"])
            self.assertNotIn("exit_long", v4)
            self.assertEqual(v4["time_stop_bars"], 2 * v1["time_stop_bars"])
            for k in ("long", "short", "stop", "gate", "regimes", "family"):
                self.assertEqual(v2[k], v1[k], (n, k))
                self.assertEqual(v4[k], v1[k], (n, k))
            for k in ("stop", "targets", "time_stop_bars", "timeframes", "gate"):
                self.assertEqual(v3[k], v1[k], (n, k))
            self.assertNotIn("htf_up", " ".join(v1["long"]))                  # 4H + 1H come from the gate

    def test_v5_is_v2_with_the_fast_4h_gate(self):
        by = {(c["program"]["strategy"], c["program"]["version"]): c for c in RAW}
        v5 = sorted(n for n, v in by if v == "V5")
        self.assertEqual(v5, [n for n in range(1, 11) if by[(n, "V1")]["gate"] == "intraday"])
        for n in v5:
            a, b = by[(n, "V2")], by[(n, "V5")]
            self.assertEqual(b["gate"], "intraday_fast")
            diff = [k for k in SP.LOGIC_KEYS if a.get(k) != b.get(k)]
            self.assertEqual(diff, ["gate"], n)

    def test_program_block_is_required_and_the_brain_may_not_write_the_file(self):
        c = copy.deepcopy(RAW[0])
        self.assertEqual(SP.program_card_problems(c), [])
        c["program"]["version"] = "V9"
        self.assertTrue(SP.program_card_problems(c))
        del c["program"]
        self.assertIn("program block missing", SP.program_card_problems(c)[0])
        with open(os.path.join(ROOT, SP.LIBRARY_FILE)) as f:
            main = yaml.safe_load(f)
        bad = dict(copy.deepcopy(RAW[0]), program=None)
        _, problems, _, _ = SP.load_library(main, [], RG.LABELS, sc.TF_ORDER, [bad])
        self.assertIn(f"program: {bad['id']}", problems)

    def test_engine_variants_of_a_program_card_are_plain_lab_cards(self):
        cards, _ = loaded()
        c = cards[0]
        cell = dict(strategy=c["id"], version=c["version"], tf=c["timeframes"][0], status="BACKTESTING",
                    evidence=dict(all=dict(n=300, avg_r=0.2, pf=1.4), validate=dict(n=90, avg_r=0.15),
                                  long=dict(n=150, avg_r=0.2), short=dict(n=150, avg_r=0.2)),
                    attribution=dict(by_regime={}, systematic=[]), reasons=["only 300 trades"])
        out = ideas.variant_cards({f"{c['id']}@1.0|4h": cell}, {f"{c['id']}@1.0": c}, "2026-10-10", 3, RG.LABELS,
                                  sc.TF_ORDER, [])
        for v in out:
            self.assertNotIn("program", v)
            self.assertFalse(any(str(k).startswith("_") for k in v))


class Gates(unittest.TestCase):
    def reg(self, **tfs):
        return {tf: (np.array(v, dtype=object), np.array([None] * len(v), dtype=object)) for tf, v in tfs.items()}

    def test_intraday_needs_4h_and_1h_and_ignores_the_daily_and_weekly(self):
        s = dict(gate="intraday", regimes=list(RG.LABELS))
        reg = self.reg(**{"1w": ["STRONG_BULL"] * 4, "1d": ["STRONG_BULL"] * 4,
                          "4h": ["WEAK_BEAR", "WEAK_BEAR", "WEAK_BULL", "STRONG_BEAR"],
                          "1h": ["WEAK_BEAR", "RANGE", "WEAK_BULL", "STRONG_BEAR"]})
        gl, gs, *_ = LC.gate_arrays(s, "1h", reg, 4)
        self.assertEqual(gs.tolist(), [True, False, False, True])   # a SHORT while 1W / 1D are strongly bullish
        self.assertEqual(gl.tolist(), [False, False, True, False])
        old_s = LC.gate_arrays(dict(s, gate="trend"), "1h", reg, 4)[1]
        self.assertFalse(old_s[0])                                   # the old trend gate blocked that short

    def test_intraday_reversal_never_against_a_strong_4h_trend(self):
        s = dict(gate="intraday_reversal", regimes=["RANGE"])
        reg = self.reg(**{"1w": ["STRONG_BEAR"] * 3, "1d": ["STRONG_BEAR"] * 3,
                          "4h": ["RANGE", "STRONG_BEAR", "STRONG_BULL"], "1h": ["RANGE"] * 3})
        gl, gs, *_ = LC.gate_arrays(s, "15m", reg, 3)
        self.assertEqual(gl.tolist(), [True, False, True])           # 1W / 1D STRONG_BEAR do not block
        self.assertEqual(gs.tolist(), [True, True, False])

    def test_fast_4h_gate_reads_the_ema_trend_not_the_regime_label(self):
        s = dict(gate="intraday_fast", regimes=list(RG.LABELS))
        reg = self.reg(**{"4h": ["TRANSITION", "UNCLEAR", "WEAK_BULL"], "1h": ["STRONG_BEAR", "STRONG_BEAR", "WEAK_BULL"],
                          "4h_fast": ["DOWN", "FLAT", "UP"], "1d": ["STRONG_BULL"] * 3})
        gl, gs, *_ = LC.gate_arrays(s, "15m", reg, 3)
        self.assertEqual(gs.tolist(), [True, False, False])          # 4H label TRANSITION, fast trend DOWN: short ok
        self.assertEqual(gl.tolist(), [False, False, True])
        self.assertFalse(LC.gate_arrays(dict(s, gate="intraday"), "15m", reg, 3)[1][0])   # the label gate said no
        self.assertFalse(LC.gate_arrays(s, "15m", {k: v for k, v in reg.items() if k != "4h_fast"}, 3)[1].any())

    def test_fast_trend_is_the_htf_ema_test(self):
        up = np.linspace(100, 200, 120)
        f = sc.fast_trend(np.r_[up, up[::-1]])
        self.assertIsNone(f[10])                                      # EMA50 not ready yet
        self.assertEqual(f[119], "UP")
        self.assertEqual(f[-1], "DOWN")
        n = 3
        df = pd.DataFrame(dict(open_time=np.arange(n) * H, high=1.0, low=1.0))
        reg = {"4h_fast": (np.array(["UP", "FLAT", None], dtype=object), np.array([None] * n, dtype=object))}
        g = sc.add_context(df, pd.DataFrame(index=df.index), reg, "1h")
        self.assertEqual(g["dir_4h_fast"].tolist()[:2], [1.0, 0.0])
        self.assertTrue(np.isnan(g["dir_4h_fast"].iloc[2]))

    def test_new_gates_are_known(self):
        self.assertIn("intraday_fast", SP.GATES)
        self.assertIn("intraday", SP.GATES)
        self.assertIn("intraday_reversal", SP.GATES)


class Blocks(unittest.TestCase):
    def test_sessions_and_the_asia_range_known_only_after_asia(self):
        day = 1_760_000_000_000 // 86_400_000 * 86_400_000
        ot = np.array([day + i * H for i in range(30)])
        hi = np.arange(30, dtype=float) + 100
        lo = hi - 1
        c = SS.columns(ot, hi, lo, H)
        self.assertEqual(c["sess_asia"][:8].tolist(), [1.0] * 8)
        self.assertEqual(c["sess_london"][8:13].tolist(), [1.0] * 5)
        self.assertEqual(c["sess_ny"][13:21].tolist(), [1.0] * 8)
        self.assertTrue(np.isnan(c["asia_high"][:7]).all())          # Asia not over yet
        self.assertEqual(c["asia_high"][7], 107.0)                   # the 07:00 candle closes at 08:00
        self.assertEqual(c["asia_high"][20], 107.0)
        self.assertEqual(c["asia_low"][20], 99.0)
        self.assertTrue(np.isnan(c["asia_high"][24 + 3]))            # next day, before 08:00
        c4 = SS.columns(ot[::4], hi[::4], lo[::4], 4 * H)            # 4H candles: 00:00 and 04:00 make Asia
        self.assertTrue(np.isnan(c4["asia_high"][0]))
        self.assertEqual(c4["asia_high"][1], 104.0)

    def test_regime_direction_columns(self):
        n = 3
        df = pd.DataFrame(dict(open_time=np.arange(n) * H, high=1.0, low=1.0))
        reg = {"1d": (np.array(["WEAK_BULL", "STRONG_BEAR", np.nan], dtype=object), np.array([None] * n, dtype=object)),
               "4h": (np.array(["EXPANSION", "EXPANSION", "RANGE"], dtype=object), np.array(["up", "down", None], dtype=object))}
        f = sc.add_context(df, pd.DataFrame(index=df.index), reg, "1h")
        self.assertEqual(f["dir_1d"].tolist()[:2], [1.0, -1.0])
        self.assertTrue(np.isnan(f["dir_1d"].iloc[2]))               # unknown -> a rule using it is false
        self.assertEqual(f["dir_4h"].tolist(), [1.0, -1.0, 0.0])
        self.assertTrue(f["dir_1w"].isna().all())
        for k in ("dir_1d", "sess_asia", "asia_high"):
            self.assertIn(k, SP.COLUMNS)


class TrailingExit(unittest.TestCase):
    def test_chandelier_matches_the_rule_building_blocks(self):
        rng = np.random.default_rng(3)
        c = 100 + np.cumsum(rng.normal(0, 1, 400))
        h, l = c + rng.random(400), c - rng.random(400)
        df = pd.DataFrame(dict(open=c, high=h, low=l, close=c, volume=1.0))
        ns = sc.make_namespace(df)
        lt, st = mg.chandelier_levels(h, l, c, 22, 3.0)
        ref_l = (ns["highest"](ns["high"], 22) - 3.0 * ns["atr"](22)).to_numpy()
        ref_s = (ns["lowest"](ns["low"], 22) + 3.0 * ns["atr"](22)).to_numpy()
        np.testing.assert_allclose(lt[30:], ref_l[30:], rtol=1e-9)
        np.testing.assert_allclose(st[30:], ref_s[30:], rtol=1e-9)
        a, b = mg.trail_for({"atr_n": 22, "atr_x": 3.0}, h, l, c)
        np.testing.assert_allclose(a[30:], lt[30:])
        a2, _ = mg.trail_for({"swing_n": 3, "ema": 9}, h, l, c)
        np.testing.assert_allclose(a2, mg.trail_levels(h, l, c, 3, 9)[0])

    def test_trail_settings_are_checked(self):
        ok = {"trail": {"atr_n": 22, "atr_x": 3.0}}
        self.assertEqual(SP.manage_problems({"manage": ok}), [])
        for bad in ({"atr_n": 1, "atr_x": 3.0}, {"atr_n": 22, "atr_x": 50}, {"atr_n": 22}, {"atr_n": 22, "ema": 9}):
            self.assertTrue(SP.manage_problems({"manage": {"trail": bad}}), bad)

    def test_backtest_runner_trails_after_tp1(self):
        n = 120
        c = np.concatenate([np.full(40, 100.0), np.linspace(100, 115, 50), np.linspace(115, 100, 30)])
        df = pd.DataFrame(dict(open_time=np.arange(n) * 4 * H, open=c, high=c + 0.5, low=c - 0.5, close=c,
                               volume=1.0))
        df["close_time"] = df["open_time"] + 4 * H - 1
        df["_atr"] = 1.0
        L = np.zeros(n, bool)
        L[45] = True
        s = dict(stop={"method": "atr", "atr": 2.0}, targets={"long": ["2R", "10R"], "short": ["2R", "10R"],
                                                            "split": [0.5, 0.5]},
                 manage={"trail": {"atr_n": 22, "atr_x": 3.0}}, time_stop_bars=200)
        cfg = copy.deepcopy(CFG)
        tr = sc.backtest(df, L, np.zeros(n, bool), None, None, s, cfg, "4h")
        self.assertEqual(len(tr), 1)
        self.assertEqual(tr[0]["reason"], "TP1+stop")                  # the trail took the rest out on the way down
        self.assertGreater(tr[0]["r"], 2.0)                            # more than TP1 alone: the runner gained
        self.assertIn("fees_r", tr[0])
        self.assertGreater(tr[0]["fees_r"], 0)

    def test_live_follow_reads_the_card_timeframe_without_look_ahead(self):
        card = pd.DataFrame(dict(open_time=np.arange(40) * 4 * H, high=np.arange(40) + 101.0,
                                 low=np.arange(40) + 99.0, close=np.arange(40) + 100.0))
        card["close_time"] = card["open_time"] + 4 * H - 1
        m5 = pd.DataFrame(dict(open_time=np.arange(30 * 4 * 12, 31 * 4 * 12) * 300_000))
        m5["close_time"] = m5["open_time"] + 299_999
        out = LW.trail_on_5m(m5, card, {"atr_n": 5, "atr_x": 2.0})
        lt, _ = mg.chandelier_levels(card["high"], card["low"], card["close"], 5, 2.0)
        self.assertEqual(out["trail_long"][0], lt[29])                 # inside 4H candle 30: candle 29's level
        self.assertEqual(out["trail_long"][-1], lt[30])                # its last 5m candle closes it
        self.assertTrue(np.isnan(LW.trail_on_5m(m5, None, {"atr_n": 5, "atr_x": 2.0})["trail_long"]).all())

    def test_alert_names_the_trailing_exit(self):
        a = dict(label="PAPER", coin="BTC", inst="BTC-USDT-SWAP", d=1, tf="4h", strategy="P01-BREAKOUT-V4",
                 version="1.0", entry=100.0, R=2.0, tps=[104.0, 120.0], split=[0.5, 0.5], zone_r=0.2, max_hold=120,
                 close_ms=0, sent_ms=9000, manage={"trail": {"atr_n": 22, "atr_x": 3.0}}, regimes={}, warnings=[],
                 size={}, risk_pct=0.5)
        text = lv.message(a)
        self.assertIn("3 ATR behind the highest high / lowest low of the last 22 4h candles", text)


def reg_cells(**status):
    return {k: dict(status=v[0], last_checked_utc=v[1]) for k, v in status.items()}


class Batches(unittest.TestCase):
    def cards(self):
        return loaded()[0]

    def test_never_tested_first_then_oldest(self):
        cards = self.cards()
        chosen, why = PG.batch(cards, {}, 2)
        self.assertEqual(chosen, [1, 2])
        self.assertIn("never tested", why[1])
        cells = {}
        for c in cards:
            for ck in PG.cell_keys(c):
                cells[ck] = dict(status="BACKTESTING", last_checked_utc=f"2026-10-{PG.number(c) % 5 + 10:02d} 01:00")
        chosen, why = PG.batch(cards, cells, 2)
        self.assertEqual(chosen, [5, 10])                                # checked 2026-10-10 = longest ago
        self.assertIn("longest ago", why[5])

    def test_paper_strategies_are_checked_every_night(self):
        cards = self.cards()
        cells = {}
        for c in cards:
            for ck in PG.cell_keys(c):
                cells[ck] = dict(status="FAILED", last_checked_utc="2026-10-12 01:00")
        cells["P07-SQUEEZE-RETEST-V2@1.0|30m"] = dict(status="PAPER_TRADING", last_checked_utc="2026-10-12 01:00")
        chosen, why = PG.batch(cards, cells, 1)
        self.assertIn(7, chosen)
        self.assertEqual(len(chosen), 2)
        self.assertIn("checked every night", why[7])

    def test_modes(self):
        cards = self.cards()
        self.assertEqual(PG.batch(cards, {}, 2, "all")[0], list(range(1, 11)))
        self.assertEqual(PG.batch(cards, {}, 2, "none")[0], [])
        self.assertEqual(PG.batch(cards, {}, 2, "4,9,77")[0], [4, 9])
        run, skipped = PG.select(cards + [dict(id="X", version="1.0")], [1])
        self.assertEqual({PG.number(c) for c in run if PG.is_program(c)}, {1})
        self.assertIn("X", [c["id"] for c in run])                       # the library always runs
        self.assertEqual(len(skipped), 42)                                 # 47 cards - strategy 1 (V1-V5)

    def test_carried_cells_keep_their_results_and_take_the_registry_status(self):
        cards = self.cards()
        ck = "P03-FIB-PULLBACK-V1@1.0|4h"
        prev = {ck: dict(strategy="P03-FIB-PULLBACK-V1", version="1.0", tf="4h", status="BACKTESTING",
                         evidence={"all": {"n": 120}})}
        out = PG.carry(prev, [c for c in cards if PG.number(c) == 3], {ck: {"status": "VALIDATION"}}, "2026-10-10 01:00")
        self.assertEqual(out[ck]["status"], "VALIDATION")
        self.assertEqual(out[ck]["carried_from"], "2026-10-10 01:00")
        again = PG.carry(out, [c for c in cards if PG.number(c) == 3], {}, "2026-10-11 01:00")
        self.assertEqual(again[ck]["carried_from"], "2026-10-10 01:00")   # the run the numbers really came from


def trade(r, fees, t=0, d=1, oos=False):
    return dict(r=r, fees_r=fees, entry_time=t, dir=d, oos=oos, bars=3)


class Results(unittest.TestCase):
    def test_per_coin_after_and_before_fees(self):
        rows = PG.coin_rows({"BTC": [trade(2.0, 0.1), trade(-1.0, 0.1)] * 3, "ETH": [trade(-1.0, 0.2)] * 6}, 5)
        self.assertEqual(rows["BTC"]["avg_r"], 0.5)
        self.assertEqual(rows["BTC"]["gross_avg_r"], 0.6)
        self.assertTrue(rows["BTC"]["positive"])
        self.assertFalse(rows["ETH"]["positive"])
        self.assertEqual(rows["ETH"]["win_rate"], 0.0)

    def test_table_keeps_untested_rows_and_renders(self):
        cards = loaded()[0]
        c1 = next(c for c in cards if c["id"] == "P01-BREAKOUT-V1")
        ev = dict(all=dict(n=6, win_rate=50.0, avg_r=0.5, pf=2.0), validate=dict(n=2, avg_r=0.4),
                  long=dict(avg_r=0.5), short=dict(avg_r=0.0))
        cells = {"P01-BREAKOUT-V1@1.0|4h": dict(strategy=c1["id"], version="1.0", tf="4h", status="BACKTESTING",
                                                evidence=ev, reasons=["only 6 trades"], paper_gate_failed=[])}
        per = {(c1["id"], "1.0", "4h"): {"BTC": [trade(2.0, 0.1), trade(-1.0, 0.1)] * 3}}
        first = PG.table(None, cards, cells, per, 5, "2026-10-09 01:00", [1], {}, [2])["cells"]["P01-BREAKOUT-V1@1.0|4h"]
        old = {"cells": {"P05-RANGE-REVERSAL-V1@1.0|4h": dict(first, strategy=5, name="Range reversal"),
                         "GONE-V1@1.0|4h": dict(first, strategy=11)}}
        t = PG.table(old, cards, cells, per, 5, "2026-10-10 01:00", [1, 2], {1: "never tested yet"}, [3, 4])
        self.assertIn("P05-RANGE-REVERSAL-V1@1.0|4h", t["cells"])          # carried from the last file
        self.assertNotIn("GONE-V1@1.0|4h", t["cells"])                     # no longer a program card
        row = t["cells"]["P01-BREAKOUT-V1@1.0|4h"]
        self.assertEqual((row["avg_r"], row["gross_avg_r"], row["positive_coins"]), (0.5, 0.6, ["BTC"]))
        self.assertEqual(row["why_not"], ["only 6 trades"])
        md = PG.render(t)
        self.assertIn("## 1. Breakout", md)
        self.assertIn("| V1 | 4h | BACKTESTING | 6 | 50 | +0.50R | +0.60R | +0.40R | BTC |", md)
        self.assertIn("next night: 3, 4", md)
        self.assertIn("No program strategy", PG.render(dict(t, cells={})))


class Wiring(unittest.TestCase):
    def test_watcher_syncs_the_file_and_knows_the_new_code(self):
        self.assertIn(("main", SP.PROGRAM_FILE), LW.SYNC_FILES)
        self.assertIn("engine/sessions.py", LW.CODE_FILES)

    def test_config(self):
        self.assertEqual(CFG["research"]["history_bars"]["15m"], 175200)      # 5 years
        self.assertEqual(CFG["research"]["history_bars"]["30m"], 87600)
        self.assertEqual(CFG["research"]["history_bars"]["5m"], 210240)       # 5m stays 2 years (entry check)
        self.assertGreaterEqual(PG.settings(CFG.get("program"))["strategies_per_night"], 1)

    def test_memory_guard_checks_the_program_file(self):
        with tempfile.TemporaryDirectory() as d:
            for f in (SP.LIBRARY_FILE, SP.LAB_FILE):
                with open(os.path.join(ROOT, f)) as src, open(os.path.join(d, f), "w") as dst:
                    dst.write(src.read())
            bad = [dict(copy.deepcopy(RAW[0]), gate="nonsense")]
            with open(os.path.join(d, SP.PROGRAM_FILE), "w") as f:
                yaml.safe_dump(bad, f)
            with mock.patch.object(memory_guard, "ROOT", d):
                probs = memory_guard.lab_problems()
            self.assertTrue(any(p.startswith(SP.PROGRAM_FILE) for p in probs))

    def test_research_offline_runs_one_program_batch(self):
        import json
        import shutil
        import subprocess
        from test_data_quality import run_copy
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        for name in ("research.py", SP.PROGRAM_FILE):
            shutil.copy(os.path.join(ROOT, name), tmp)
        p = run_copy(tmp, "research.py", "--offline", "--coins", "1", "--program", "8")
        self.assertEqual(p.returncode, 0, p.stdout[-3000:] + p.stderr[-3000:])
        with open(os.path.join(tmp, "reports", "research_offline.json")) as f:
            out = json.load(f)
        self.assertEqual(out["program"]["tested_tonight"], [8])
        tested = {c["strategy"] for c in out["cells"].values() if not c.get("carried_from")}
        self.assertTrue({"P08-SESSION-BREAKOUT-V1", "P08-SESSION-BREAKOUT-V2"} <= tested)
        self.assertFalse(any(x.startswith("P01-") for x in tested))
        self.assertEqual(out["not_run"], {})
        with open(os.path.join(tmp, "reports", "program_offline.json")) as f:
            t = json.load(f)
        self.assertIn("P08-SESSION-BREAKOUT-V2@1.0|15m", t["cells"])
        self.assertTrue(os.path.exists(os.path.join(tmp, "reports", "program_offline.md")))
        # a night that runs too long drops the whole batch (never half-tested) - it goes first the next night
        with open(os.path.join(tmp, "config.yaml")) as f:
            cfg = re.sub(r"skip_after_min: \d+", "skip_after_min: 0", f.read())
        with open(os.path.join(tmp, "config.yaml"), "w") as f:
            f.write(cfg)
        p = subprocess.run([sys.executable, "research.py", "--offline", "--coins", "1", "--program", "3"], cwd=tmp,
                           capture_output=True, text=True, timeout=900)
        self.assertEqual(p.returncode, 0, p.stdout[-3000:] + p.stderr[-3000:])
        self.assertIn("tonight's batch is dropped", p.stdout + p.stderr)
        with open(os.path.join(tmp, "reports", "research_offline.json")) as f:
            out = json.load(f)
        self.assertEqual(out["program"]["tested_tonight"], [])
        self.assertIn("too long", out["program"]["why"]["3"])
        self.assertFalse([k for k, c in out["cells"].items() if k.startswith("P03-") and not c.get("carried_from")])
        self.assertTrue([k for k in out["cells"] if k.startswith("P08-")])          # last night's results carried


if __name__ == "__main__":
    unittest.main()
