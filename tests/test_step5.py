"""Roadmap step 5 (operator, 2026-10-06): the proven 4H trend with a faster entry (engine/trend4h.py), strategies by
market type (engine/regime_fit.py) and the scalping variants of the engine's variant search (engine/ideas.py)."""
import copy
import json
import os
import sys
import unittest

import numpy as np
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import scanner as sc  # noqa: E402
from engine import data_quality as dq  # noqa: E402
from engine import ideas  # noqa: E402
from engine import regime as rg  # noqa: E402
from engine import regime_fit as rfit  # noqa: E402
from engine import strategy_spec as SS  # noqa: E402
from engine import trend4h as t4  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)


def synthetic(n4=1500):
    feed, data, q = sc.Synthetic(seed=7), {}, {}
    for tf, n in (("1w", 300), ("1d", 1200), ("4h", n4), ("1h", 4 * n4), ("15m", 6000)):
        raw = feed.klines("BTCUSDT", tf, n)
        df, rep = dq.check_candles(raw, sc.TF_MS[tf], int(raw["close_time"].max()) + 1, dq.settings(CFG.get("data_quality")))
        data[("BTCUSDT", tf)], q[("BTC", tf)] = df, rep
    return data, q


class Window(unittest.TestCase):
    def test_starts_on_a_breakout_and_ends_on_exit_stop_or_time(self):
        n = 10
        c = np.full(n, 100.0)
        h, l, atr = c + 1, c - 1, np.full(n, 2.0)
        z = np.zeros(n, bool)
        L, S, XL = z.copy(), z.copy(), z.copy()
        L[1], XL[4] = True, True
        st, age = t4.window(h, l, c, atr, L, S, XL, z)
        self.assertEqual(st.tolist(), [0, 1, 1, 1, 0, 0, 0, 0, 0, 0])          # the exit rule closes it at 4
        self.assertEqual(age[3], 2)
        l2 = l.copy()
        l2[3] = 95.0                                                            # 2 x ATR below the 100 close = 96
        st, _ = t4.window(h, l2, c, atr, L, S, z, z)
        self.assertEqual(st[:5].tolist(), [0, 1, 1, 0, 0])
        st, _ = t4.window(h, l, c, atr, L, S, z, z, max_bars=3)
        self.assertEqual(st[:6].tolist(), [0, 1, 1, 1, 0, 0])
        S2 = z.copy()
        S2[3] = True                                                            # a breakout the other way flips it
        st, _ = t4.window(h, l, c, atr, L, S2, z, z)
        self.assertEqual(st[:5].tolist(), [0, 1, 1, -1, -1])


class Columns(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data, cls.q = synthetic()
        cls.pc = sc.prepare_coin("BTCUSDT", "BTC", cls.data, cls.q, ["4h", "1h", "15m"], CFG)

    def test_faster_timeframes_get_the_window_from_closed_4h_candles(self):
        for tf in ("1h", "15m"):
            f = self.pc["frames"][tf]["feats"]
            for col in t4.COLUMNS:
                self.assertIn(col, f)
            self.assertFalse(((f["trend4h_long"] == 1) & (f["trend4h_short"] == 1)).any())
        self.assertNotIn("trend4h_long", self.pc["frames"]["4h"]["feats"])

    def test_no_look_ahead(self):
        end = int(self.data[("BTCUSDT", "4h")]["close_time"].iloc[1300])
        cut = {k: d[d["close_time"] <= end].reset_index(drop=True) for k, d in self.data.items()}
        part = sc.prepare_coin("BTCUSDT", "BTC", cut, self.q, ["4h", "1h", "15m"], CFG)
        for tf in ("1h", "15m"):
            a = self.pc["frames"][tf]["feats"]
            b = part["frames"][tf]["feats"]
            m = len(b)
            for col in t4.COLUMNS:
                x, y = a[col].to_numpy()[:m], b[col].to_numpy()
                same = (x == y) | (np.isnan(x) & np.isnan(y))
                self.assertTrue(same[-200:].all(), f"{tf} {col} changes when later candles are added")

    def test_cards_and_their_twins(self):
        cards = {c["id"]: c for c in sc.load_cards()[0]}
        for cid in ("TRD-H4-PULLBACK", "TRD-H4-BREAKOUT"):
            c, tw = cards[cid], cards[cid + "-noT4"]
            self.assertEqual(c["control_twin"], tw["id"])
            self.assertEqual(c["stop"]["max_cost_r"], 0.25)
            self.assertTrue(set(c["timeframes"]) <= set(SS.T4_TFS))
            self.assertEqual([r for r in c["long"] if "trend4h" not in r], tw["long"])   # only the window differs
            self.assertEqual(SS.expr_problems("trend4h_long == 1", ["4h"])[0][:16], "'trend4h_long ==")


class RegimeFit(unittest.TestCase):
    def test_blocks_only_measured_losing_regimes(self):
        cells = {"X@1.0|15m": {"attribution": {"by_regime": {"RANGE": {"n": 40, "avg_r": -0.2},
                                                             "STRONG_BULL": {"n": 50, "avg_r": 0.3},
                                                             "TRANSITION": {"n": 12, "avg_r": -0.9}}}}}
        fit = rfit.table(cells)
        self.assertEqual(fit["X@1.0|15m"]["RANGE"], [40, -0.2])
        self.assertIn("RANGE", rfit.blocked(fit, "X@1.0|15m", "RANGE"))
        self.assertIsNone(rfit.blocked(fit, "X@1.0|15m", "STRONG_BULL"))
        self.assertIsNone(rfit.blocked(fit, "X@1.0|15m", "TRANSITION"))        # too few trades to say
        self.assertIsNone(rfit.blocked(fit, "X@1.0|15m", None))
        self.assertIsNone(rfit.blocked({}, "Y@1.0|1h", "RANGE"))

    def test_the_committed_file_matches_the_research_cells(self):
        with open(os.path.join(ROOT, "reports", "regime_fit.json")) as f:
            fit = json.load(f)
        self.assertTrue(all(isinstance(v, dict) for v in fit.values()))


class Variants(unittest.TestCase):
    def cell(self, cost):
        return dict(strategy="X", version="1.0", tf="15m", status="BACKTESTING", attribution={},
                    evidence=dict(median_cost_r=cost, all=dict(n=100, avg_r=0.05), validate=dict(n=30, avg_r=0.04)))

    def test_limit_and_fee_cap_variants_when_fees_hurt(self):
        lib = [c for c in sc.load_cards()[0] if c["id"] == "donchian_breakout"][0]
        raw = copy.deepcopy(dict(lib["_raw"], targets=dict(long=["2R", "3R"], short=["2R", "3R"], split=[0.5, 0.5])))
        kinds = [k for k, _, _ in ideas._variants(raw, self.cell(0.3), sc.TF_ORDER)]
        self.assertEqual(kinds[:2], ["LIMIT", "FEECAP"])
        kinds = [k for k, _, _ in ideas._variants(raw, self.cell(0.05), sc.TF_ORDER)]
        self.assertNotIn("LIMIT", kinds)                                        # fees do not hurt: not tried
        for _, _, change in ideas._variants(raw, self.cell(0.3), sc.TF_ORDER):
            self.assertEqual(len(SS.change_count(raw, dict(raw, **change))), 1)   # one change each
            card = dict(raw, **change)
            self.assertEqual(SS.check(card, rg.LABELS, sc.TF_ORDER), [])


if __name__ == "__main__":
    unittest.main()
