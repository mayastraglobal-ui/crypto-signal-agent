"""Step 3d (operator, 2026-10-06): the playbook made flexible - graded setups (must-haves + bonus points, grade B =
half size), the operator's three rule changes (A in London, B on 15m triggers, C's wider box), the fee fix
(stop.max_cost_r, limit entries) - and the originals left exactly as written."""
import os
import sys
import unittest

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import scanner as sc  # noqa: E402
from engine import flow_history as fh  # noqa: E402
from engine import risk as rk  # noqa: E402
from engine import scalp_playbook as pb  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)


def synth(seed=3):
    f = sc.Synthetic(seed=seed)
    return (f.klines("BTCUSDT", "5m", 3000).reset_index(drop=True), f.klines("BTCUSDT", "15m", 1200).reset_index(drop=True),
            f.klines("BTCUSDT", "1h", 600).reset_index(drop=True))


class Grades(unittest.TestCase):
    def test_points_decide_trade_half_and_full_size(self):
        out, P = {}, pb.settings()
        core = np.array([True, True, True, True, False])
        bonus = [np.array([1, 1, 1, 0, 1], bool), np.array([1, 1, 0, 0, 1], bool), np.array([1, 0, 0, 0, 1], bool)]
        pb._grade(out, "B", "long", core, bonus, P)
        self.assertEqual(out["pbBg_score_long"].tolist(), [3, 2, 1, 0, 0])      # no must-haves: no score
        self.assertEqual(out["pbBg_long"].tolist(), [1, 1, 0, 0, 0])            # 2+ points = a trade
        self.assertEqual(out["pbBg_half_long"].tolist(), [0, 1, 0, 0, 0])       # 2 points = half size
        self.assertEqual(out["pbBp_long"].tolist(), [1, 0, 0, 0, 0])            # A+ only

    def test_graded_contains_the_playbook_setups_and_aplus_is_inside_graded(self):
        d5, d15, d1h = synth()
        out = pb.compute(d5, d15, d1h, delta=np.random.default_rng(1).normal(0, 1, len(d5)))
        for s in ("A", "B", "C"):
            for side in ("long", "short"):
                g, p = out[f"pb{s}g_{side}"] == 1, out[f"pb{s}p_{side}"] == 1
                self.assertFalse((p & ~g).any(), f"{s} {side}: an A+ setup that is not a graded setup")
        # every playbook A signal (all its conditions) is a graded A+ setup at full size
        for side in ("long", "short"):
            a = out[f"pbA_{side}"] == 1
            self.assertFalse((a & (out[f"pbAg_{side}"] != 1)).any())
            self.assertFalse((out[f"pbA_{side}"] == 1).sum() > (out[f"pbA_ldn_{side}"] == 1).sum())   # London adds


class NoLookAhead15m(unittest.TestCase):
    def test_15m_triggers_and_new_columns_ignore_the_future(self):
        f = sc.Synthetic(seed=5)
        d15 = f.klines("BTCUSDT", "15m", 2400).reset_index(drop=True)
        d1h = f.klines("BTCUSDT", "1h", 700).reset_index(drop=True)
        delta = np.random.default_rng(2).normal(0, 1, len(d15))
        full = pb.compute(d15, d15, d1h, delta=delta, tf_ms=900_000)
        cut = int(d15["close_time"].iloc[2000])
        c15, c1 = (d[d["close_time"] <= cut].reset_index(drop=True) for d in (d15, d1h))
        part = pb.compute(c15, c15, c1, delta=delta[:len(c15)], tf_ms=900_000)
        for k in pb.COLUMNS:
            a, b = np.asarray(full[k], dtype=float)[:len(c15)], np.asarray(part[k], dtype=float)
            same = (a == b) | (np.isnan(a) & np.isnan(b))
            self.assertTrue(same[-300:].all(), f"{k} (15m) changes when later candles are added")

    def test_15m_flow_is_the_sum_of_three_whole_5m_candles(self):
        fl = pd.DataFrame({"open_time": [0, 300_000, 600_000, 900_000, 1_200_000], "delta": [1.0, 2.0, 3.0, 4.0, 5.0],
                           "src": 1})
        r = fh.resample(fl, 900_000)
        self.assertEqual(r["open_time"].tolist(), [0])                 # the second 15m candle is incomplete: unknown
        self.assertEqual(r["delta"].tolist(), [6.0])
        self.assertIs(fh.resample(fl, 300_000), fl)


class FeeCap(unittest.TestCase):
    def card(self, cap):
        return dict(stop=dict(method="atr", atr=1.0, max_cost_r=cap), targets=None)

    def test_costs_above_the_cap_mean_no_trade(self):
        k = sc.trade_costs(CFG, 1)
        entry, atr = 100.0, 0.5                                         # R = 0.5 = 0.5% of the price
        maker_r = entry * (k["maker"] + k["taker"] + k["slip"]) / atr
        taker_r = entry * (k["taker"] + k["slip"] + k["taker"] + k["slip"]) / atr
        cap = (maker_r + taker_r) / 2                                   # between the two
        sk = {}
        self.assertIsNone(sc.plan_trade(self.card(cap), 0, 1, entry, atr, {}, CFG, sk))
        self.assertEqual(sk, {"cost": 1})
        self.assertIsNotNone(sc.plan_trade(self.card(cap), 0, 1, entry, atr, {}, CFG, maker=True))   # limit: cheaper
        self.assertIsNotNone(sc.plan_trade(dict(stop=dict(method="atr", atr=1.0), targets=None), 0, 1, entry, atr, {},
                                           CFG))                        # no cap: as before

    def test_card_checks(self):
        base = next(c for c in yaml.safe_load(open(os.path.join(ROOT, "strategies.yaml"))) if c["id"] == "PB-B-GRADED")
        labels, tfs = sc.rg.LABELS, list(sc.TF_MS)
        self.assertEqual(SP.check(base, labels, tfs), [])
        bad = dict(base, stop=dict(base["stop"], max_cost_r=5))
        self.assertTrue(any("max_cost_r" in e for e in SP.check(bad, labels, tfs)))
        bad = dict(base, half_size={"long": "pbBg_half_long"})
        self.assertTrue(any("half_size" in e for e in SP.check(bad, labels, tfs)))


class HalfSize(unittest.TestCase):
    def test_grade_b_halves_the_size_with_its_reason(self):
        card = dict(half_size=dict(long="h_l", short="h_s", why="grade B setup (2 of 5 bonus points)"))
        feats = pd.DataFrame({"h_l": [0.0, 1.0], "h_s": [1.0, 0.0]})
        self.assertIsNone(sc.half_size_reason(card, feats, 1, 0))
        self.assertEqual(sc.half_size_reason(card, feats, 1, 1), "grade B setup (2 of 5 bonus points)")
        self.assertIsNone(sc.half_size_reason({}, feats, 1, 1))
        PB = rk.pb_settings(CFG.get("playbook"))
        f, why = rk.pb_size_factor(pd.DataFrame(columns=sc.LOG_COLS), pd.Timestamp("2026-10-07 14:00", tz="UTC"), PB,
                                   grade="grade B setup (2 of 5 bonus points)")
        self.assertEqual(f, 0.5)
        self.assertIn("grade B", why[0])


class Library(unittest.TestCase):
    def test_new_versions_change_one_thing_and_originals_stay(self):
        cards = {c["id"]: c for c in sc.load_cards()[0]}
        same = lambda a, b, skip: [k for k in SP.LOGIC_KEYS if k not in skip and cards[a].get(k) != cards[b].get(k)]  # noqa: E731
        self.assertEqual(same("PB-A-PULLBACK-LDN", "PB-A-PULLBACK", {"long", "short"}), [])
        self.assertEqual(same("PB-C-BREAKOUT-W20", "PB-C-BREAKOUT", {"long", "short", "stop", "targets", "manage"}), [])
        self.assertEqual(same("PB-B-SWEEP-15M", "PB-B-SWEEP", {"timeframes", "time_stop_bars"}), [])
        self.assertEqual(same("PB-B-SWEEP-LIMIT", "PB-B-SWEEP", {"entry", "stop"}), [])
        for g, p in (("PB-A-GRADED", "PB-A-APLUS"), ("PB-B-GRADED", "PB-B-APLUS"), ("PB-C-GRADED", "PB-C-APLUS")):
            self.assertEqual(same(g, p, {"long", "short"}), [])
            self.assertEqual(cards[g]["stop"]["max_cost_r"], 0.25)
        for c in ("PB-A-PULLBACK", "PB-B-SWEEP", "PB-C-BREAKOUT"):
            self.assertNotIn("max_cost_r", cards[c]["stop"])            # the originals: as written


if __name__ == "__main__":
    unittest.main()
