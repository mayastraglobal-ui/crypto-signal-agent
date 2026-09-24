"""Phase 0 tests: direction-aware trading costs, funding, and safety guards on config.yaml.

Run:  python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

import numpy as np
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import scanner  # noqa: E402

CFG = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))


def flat(n, px=100.0):
    a = np.full(n, px)
    return a, a.copy(), a.copy(), a.copy()


class CostTests(unittest.TestCase):
    def test_long_uses_spot_costs(self):
        # Price never moves; trade closes on the time stop after 3 candles.
        o, h, l, c = flat(5)
        res = scanner.simulate_trade(o, h, l, c, 0, 1, 100.0, 2.0, CFG, 3, 8.0)
        # exit 100*(1-0.0005)=99.95 -> pnl -0.05; fees 0.10% in + 0.10% out; no funding
        expected = (-0.05 - (0.001 * 100 + 0.001 * 99.95)) / 2.0
        self.assertEqual(res["reason"], "time")
        self.assertAlmostEqual(res["r"], expected, places=9)

    def test_short_uses_futures_costs_plus_funding(self):
        o, h, l, c = flat(5)
        res = scanner.simulate_trade(o, h, l, c, 0, -1, 100.0, 2.0, CFG, 3, 8.0)
        # exit 100.05 -> pnl -0.05; fees 0.05% in + 0.05% out; funding 0.01% x 3 periods of 8h
        expected = (-0.05 - (0.0005 * 100 + 0.0005 * 100.05 + 3 * 0.0001 * 100)) / 2.0
        self.assertAlmostEqual(res["r"], expected, places=9)

    def test_funding_scales_with_time_held(self):
        o, h, l, c = flat(5)
        r_1h = scanner.simulate_trade(o, h, l, c, 0, -1, 100.0, 2.0, CFG, 3, 1.0)["r"]
        r_8h = scanner.simulate_trade(o, h, l, c, 0, -1, 100.0, 2.0, CFG, 3, 8.0)["r"]
        self.assertAlmostEqual(r_1h - r_8h, 3 * 0.0001 * 100 * (1 - 1 / 8) / 2.0, places=9)
        self.assertLess(r_8h, r_1h)   # holding longer costs more funding

    def test_funding_always_charged_to_shorts_never_longs(self):
        self.assertGreater(scanner.trade_costs(CFG, -1)["funding_8h"], 0)
        self.assertEqual(scanner.trade_costs(CFG, 1)["funding_8h"], 0)

    def test_stop_fills_first_when_stop_and_target_in_same_candle(self):
        o = np.array([100.0, 100.0])
        h = np.array([110.0, 110.0])   # TP1 (102) touched ...
        l = np.array([90.0, 90.0])     # ... and stop (98) touched in the same candle
        c = np.array([100.0, 100.0])
        res = scanner.simulate_trade(o, h, l, c, 0, 1, 100.0, 2.0, CFG, 10, 1.0)
        self.assertEqual(res["reason"], "SL")
        self.assertLess(res["r"], -1.0)   # a full loss plus costs

    def test_market_labels(self):
        self.assertEqual(scanner.market_type(1), "spot")
        self.assertEqual(scanner.market_type(-1), "futures only")


class SafetyGuards(unittest.TestCase):
    """These fail if someone weakens the rules in config.yaml (AGENT_PROMPT.md section 15/17)."""

    def test_costs_are_never_zero(self):
        for side in ("long", "short"):
            k = CFG["costs"][side]
            self.assertGreater(k["taker_fee_pct"], 0)
            self.assertGreater(k["maker_fee_pct"], 0)
            self.assertGreater(k["slippage_pct"], 0)
        self.assertGreater(CFG["costs"]["short"]["funding_pct_per_8h"], 0)

    def test_risk_per_trade_capped_at_one_percent(self):
        self.assertLessEqual(CFG["account"]["risk_per_trade_pct"], 1.0)
        self.assertGreater(CFG["account"]["risk_per_trade_pct"], 0)

    def test_validation_bar_not_lowered(self):
        v = CFG["validation"]
        self.assertGreaterEqual(v["min_trades"], 30)
        self.assertGreaterEqual(v["min_expectancy_r"], 0.05)
        self.assertGreaterEqual(v["min_profit_factor"], 1.15)


if __name__ == "__main__":
    unittest.main()
