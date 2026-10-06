"""Step 3a (operator's playbook, 2026-10-06): the engine features the playbook needs - the playbook gate, limit
entries at a level (market when the level is unknown), 'whichever first' targets, >= 1.5R to the last target after
fees, a minimum stop width, and the playbook's trade management (breakeven + fees, trail behind the last confirmed
swing / EMA9, +0.5R within N candles, invalidation exits) - the same in the backtest, the paper record and the
Telegram follow-up."""
import copy
import os
import sys
import unittest

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import scanner as sc  # noqa: E402
from engine import follow as fl  # noqa: E402
from engine import lifecycle as lc  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import manage as mg  # noqa: E402
from engine import positions as P  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
M5 = 300_000
T0 = 1_700_000_100_000 // 900_000 * 900_000
MANAGE = {"be_plus_fees": True, "trail": {"swing_n": 3, "ema": 9}, "progress": {"r": 0.5, "bars": 6},
          "invalidate": {"long": "inv_l", "short": "inv_s", "every": "15m"}}


def card(**kw):
    raw = dict(id="PB", version="1.0", status="FORMALIZED", family="mtf_pullback", gate="playbook", hypothesis="h",
               source="playbook", regimes=["STRONG_BULL"], timeframes=["5m"], long=["close > 1"], short=["close < 1"],
               stop={"method": "structure", "long_level": "stop_l", "short_level": "stop_s", "buffer_atr": 0,
                     "min_width_atr": 0.5, "max_width_atr": 3.0},
               targets={"long": ["1R", "max(2R, tp2_l)"], "short": ["1R", "max(2R, tp2_s)"], "split": [0.5, 0.5],
                        "min_rr_after_fees": 1.5},
               time_stop_bars=48, known_weaknesses="w", manage=MANAGE)
    raw.update(kw)
    return raw


def zero_cost():
    c = copy.deepcopy(CFG)
    for side in ("long", "short"):
        c["costs"][side].update(taker_fee_pct=0, maker_fee_pct=0, slippage_pct=0, funding_pct_per_8h=0)
    return c


class Spec(unittest.TestCase):
    def test_settings_are_checked(self):
        self.assertEqual(SP.manage_problems(card()), [])
        self.assertEqual(SP.entry_problems(card(entry={"type": "limit", "long_level": "a", "short_level": "b",
                                                       "valid_bars": 2})), [])
        for bad in ({"trail": {"swing_n": 0, "ema": 9}}, {"progress": {"r": 0.5}}, {"invalidate": {"long": "x"}},
                    {"be_plus_fees": "yes"}, {"other": 1}, {}):
            self.assertTrue(SP.manage_problems(card(manage=bad)), bad)
        self.assertTrue(SP.entry_problems(card(entry={"type": "limit", "long_level": "a", "valid_bars": 2})))
        self.assertTrue(SP.entry_problems(card(entry={"type": "limit", "long_level": "a", "short_level": "b",
                                                      "offset_atr": 0.2, "valid_bars": 2})))
        self.assertIn("playbook", SP.GATES)
        cols = SP.columns_needed(card(entry={"type": "limit", "long_level": "el", "short_level": "es", "valid_bars": 2}))
        self.assertTrue({"stop_l", "tp2_l", "el", "es", "inv_l", "inv_s"} <= cols)

    def test_min_target_is_whichever_comes_first(self):
        cols = {"vw": np.array([101.5, 103.0, 99.0])}
        self.assertEqual(SP._level(SP.parse_target("min(2R, vw)"), 1, 100.0, 1.0, 0, cols), 101.5)   # VWAP first
        self.assertEqual(SP._level(SP.parse_target("min(2R, vw)"), 1, 100.0, 1.0, 1, cols), 102.0)   # 2R first
        self.assertEqual(SP._level(SP.parse_target("min(2R, vw)"), 1, 100.0, 1.0, 2, cols), 102.0)   # VWAP behind

    def test_playbook_gate_lets_the_card_decide(self):
        n = 5
        reg = {t: (np.array(["STRONG_BEAR"] * n, dtype=object), np.array([None] * n, dtype=object))
               for t in ("1w", "1d", "4h", "1h")}
        gl, gs, ok, _, _ = lc.gate_arrays(card(), "5m", reg, n)
        self.assertTrue(gl.all() and gs.all() and ok.all())
        gl, _, _, _, _ = lc.gate_arrays(card(gate="trend"), "5m", reg, n)
        self.assertFalse(gl.any())


class Trail(unittest.TestCase):
    def test_swings_are_known_only_n_candles_later(self):
        l = np.array([10, 9, 8, 7, 8, 9, 10, 11, 12], dtype=float)
        h = l + 1
        _, lo = mg.confirmed_swings(h, l, 3)
        self.assertTrue(np.isnan(lo[5]))                                   # the low at 3 is not confirmed yet
        self.assertEqual(lo[6], 7.0)                                       # confirmed 3 candles later
        c = l + 0.5
        tl, _ = mg.trail_levels(h, l, c, 3, 3)
        self.assertEqual(tl[8], min(7.0, mg.ema(c, 3)[8]))                 # the further (lower) of swing and EMA
        cut = mg.confirmed_swings(h[:7], l[:7], 3)[1]
        np.testing.assert_array_equal(cut, lo[:7])                         # no look-ahead

    def test_closes_of_15m(self):
        ct = T0 + np.arange(6) * M5 + M5 - 1
        self.assertEqual(mg.closes_of(ct, 900_000).tolist(), [False, False, True, False, False, True])


class Simulate(unittest.TestCase):
    def sim(self, rows, manage=None, trail=None, inval=None, cfg=None, R=1.0, tps=(101.0, 102.0)):
        a = np.array(rows, dtype=float)
        return sc.simulate_trade(a[:, 0], a[:, 1], a[:, 2], a[:, 3], 0, 1, 100.0, R, cfg or zero_cost(), 48, 1 / 12,
                                 tps=list(tps), split=[0.5, 0.5], manage=manage, trail=trail, inval=inval)

    def test_breakeven_plus_fees(self):
        rows = [(100, 101.2, 99.8, 101), (101, 101.1, 100.1, 100.2)]
        r = self.sim(rows, manage={"be_plus_fees": True}, cfg=CFG)
        k = sc.trade_costs(CFG, 1)
        be = 100 * (1 + k["taker"] + k["taker"] + k["slip"])
        self.assertEqual(r["reason"], "TP1+stop")                          # 100.1 <= be (~100.15): stopped
        r = self.sim(rows, manage={"be_plus_fees": False}, cfg=CFG)
        self.assertIsNone(r)                                               # plain breakeven 100.0 not touched
        self.assertGreater(be, 100.1)

    def test_trail_tightens_after_tp1_from_the_next_candle(self):
        rows = [(100, 101.2, 99.9, 101.1), (101.1, 101.6, 100.9, 101.5), (101.5, 101.6, 100.95, 101.0)]
        trail = np.array([100.0, 101.0, 101.0])
        r = self.sim(rows, manage={"be_plus_fees": False}, trail=trail)
        self.assertEqual(r["reason"], "TP1+stop")                          # trailed to 101 (from candle 1's close)
        self.assertEqual(r["exit_idx"], 2)
        self.assertAlmostEqual(r["r"], 0.5 * 1 + 0.5 * 1)
        self.assertIsNone(self.sim(rows[:2], manage={}, trail=trail))      # TP1 candle itself: no trail yet

    def test_no_progress_exits_at_the_candle_close(self):
        rows = [(100, 100.3, 99.8, 100.1)] * 6
        r = self.sim(rows, manage={"progress": {"r": 0.5, "bars": 6}})
        self.assertEqual((r["reason"], r["exit_idx"]), ("time", 5))
        rows2 = [(100, 100.6, 99.8, 100.1)] + rows[1:]                     # +0.6R reached in candle 0
        self.assertIsNone(self.sim(rows2, manage={"progress": {"r": 0.5, "bars": 6}}))

    def test_invalidation_only_on_15m_closes(self):
        rows = [(100, 100.2, 99.4, 99.5), (99.5, 99.8, 99.3, 99.6), (99.6, 99.7, 99.3, 99.4)]
        mask = np.array([False, False, True])
        r = self.sim(rows, inval=(99.55, mask))
        self.assertEqual((r["reason"], r["exit_idx"]), ("exit-rule", 2))   # candle 0 closed below too: not a 15m close
        self.assertAlmostEqual(r["r"], -0.6)


def frame(rows, **cols):
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"], dtype=float)
    df["open_time"] = T0 + np.arange(len(df)) * M5
    df["close_time"] = df["open_time"] + M5 - 1
    df["_atr"] = 1.0
    for k, v in cols.items():
        df[k] = v
    return df


class Backtest(unittest.TestCase):
    def run_bt(self, df, spec, at=0, cfg=None):
        sig = np.zeros(len(df), bool)
        sig[at] = True
        cols = {c: df[c].to_numpy(dtype=float) if c in df else np.full(len(df), np.nan) for c in SP.columns_needed(spec)}
        sk = {}
        return sc.backtest(df, sig, np.zeros(len(df), bool), None, None, spec, cfg or zero_cost(), "5m", cols, sk), sk

    def test_limit_at_a_level_and_market_when_unknown(self):
        rows = [(100, 100.5, 99.5, 100), (100, 100.2, 99.4, 99.8), (99.8, 101.8, 99.7, 101.7), (101.7, 103.6, 101.6, 103.5)]
        spec = card(entry={"type": "limit", "long_level": "el", "short_level": "es", "valid_bars": 3}, manage=None)
        df = frame(rows, el=[99.5, np.nan, np.nan, np.nan], stop_l=98.0, tp2_l=103.0)
        tr, _ = self.run_bt(df, spec)
        self.assertEqual((tr[0]["entry"], tr[0]["entry_idx"]), (99.5, 1))   # filled at the 50% level
        df2 = frame(rows, el=np.nan, stop_l=99.0, tp2_l=103.0)
        tr, _ = self.run_bt(df2, spec)
        self.assertEqual((tr[0]["entry"], tr[0]["entry_idx"]), (100.0, 1))   # unknown level: market at the next open

    def test_reward_and_stop_width_rules(self):
        rows = [(100, 100.5, 99.5, 100)] + [(100, 100.4, 99.6, 100)] * 3 + [(100, 100.1, 98.8, 99)]   # ends at SL
        spec = card(manage=None)
        tr, sk = self.run_bt(frame(rows, stop_l=99.0, tp2_l=101.2), spec)   # TP2 = 2R (max(2R, level))
        self.assertEqual(len(tr), 1)
        tr, sk = self.run_bt(frame(rows, stop_l=99.0, tp2_l=101.2), spec, cfg=CFG)
        self.assertEqual(len(tr), 1)                                      # 2R minus fees still >= 1.5R
        spec2 = card(manage=None, targets=dict(card()["targets"], min_rr_after_fees=1.99))
        tr, sk = self.run_bt(frame(rows, stop_l=99.0, tp2_l=101.2), spec2, cfg=CFG)
        self.assertEqual((tr, sk.get("target")), ([], 1))                 # not 1.99R after fees
        tr, sk = self.run_bt(frame(rows, stop_l=99.7, tp2_l=103), spec)
        self.assertEqual((tr, sk.get("stop")), ([], 1))                   # 0.3 ATR stop < 0.5 ATR minimum


class PaperAndFollow(unittest.TestCase):
    def test_paper_record_uses_the_card_management(self):
        rows = [(100, 100.3, 99.8, 100.1)] * 9
        df = frame(rows)
        sig = pd.to_datetime(T0 - 60_000, unit="ms").strftime("%Y-%m-%d %H:%M")
        row = {c: np.nan for c in sc.LOG_COLS}
        row.update(id="x", signal_time_utc=sig, coin="BTC", tf="5m", strategy="PB", direction="LONG", entry=100.0,
                   stop=99.0, tp1=101.0, tp2=102.0, tp3=np.nan, max_hold_bars=48, status="OPEN", closed_time_utc="",
                   version="1.0", stage="PAPER_TRADING", tp_split="0.5/0.5", state=P.ACTIVE, entry_time_utc=sig,
                   sim_tf="5m", inval_level=99.0)
        log = pd.DataFrame([row], columns=sc.LOG_COLS)
        for c in sc.TEXT_COLS:
            log[c] = log[c].astype(object)
        spec = SP._finish(SP.render(card()), card())
        log, _ = sc.update_forward(log, {("BTCUSDT", "5m"): df}, {("BTC", "5m"): dict(state="GOOD")}, None, CFG,
                                   {"PB@1.0": spec}, {}, None, {}, [], "now")
        r = log.iloc[0]
        self.assertEqual((r["state"], r["close_reason"]), (P.CLOSED, "TIME"))     # no +0.5R in 6 candles
        self.assertEqual(r["closed_time_utc"], pd.to_datetime(T0 + 6 * M5 - 1, unit="ms").strftime("%Y-%m-%d %H:%M"))

    def alert(self, **kw):
        a = dict(label="PAPER", coin="BTC", inst="BTC-USDT-SWAP", d=1, tf="5m", strategy="A", version="1.0",
                 entry=100.0, R=1.0, tps=[101.0, 102.0], split=[0.5, 0.5], zone_r=0.2, max_hold=48,
                 close_ms=T0 - 1, sent_ms=T0 + 9000, manage=MANAGE, inval=99.2, be_frac=0.0012, regimes={},
                 warnings=[], size={}, risk_pct=0.5)
        a.update(kw)
        return a

    def bars(self, rows, trail=None):
        return [dict(open_time=T0 + i * M5, open=o, high=h, low=lo, close=c,
                     trail_long=(trail[i] if trail is not None else np.nan)) for i, (o, h, lo, c) in enumerate(rows)]

    def test_follow_breakeven_fees_trail_message_and_invalidation(self):
        t = fl.open_trade(self.alert(manage=dict(MANAGE, progress=None)), "a", T0, {})
        ev = fl.step(t, self.bars([(100, 101.2, 99.9, 101.1), (101.1, 101.4, 100.6, 101.3)], trail=[100.1, 100.5]))
        self.assertEqual(ev[0]["kind"], "tp")
        self.assertAlmostEqual(ev[0]["stop"], 100.12)                      # entry + 0.12% fees
        self.assertIn("break-even + fees", fl.text(t, ev[0]))
        ev = fl.step(t, self.bars([(100, 101.2, 99.9, 101.1), (101.1, 101.4, 100.6, 101.3),
                                   (101.3, 101.5, 101.1, 101.4)], trail=[100.1, 100.5, 101.0]))
        self.assertEqual([e["kind"] for e in ev], ["trail"])               # 100.5 trail (from the last close)
        self.assertIn("Move the stop-loss to <b>100.50", fl.text(t, ev[0]))

    def test_follow_progress_and_invalid(self):
        t = fl.open_trade(self.alert(), "a", T0, {})
        ev = fl.step(t, self.bars([(100, 100.3, 99.8, 100.1)] * 6))
        self.assertEqual(ev[-1]["kind"], "time")
        self.assertIn("+0.5R not reached within 6 candles", fl.text(t, ev[-1]))
        t = fl.open_trade(self.alert(), "a", T0, {})
        ev = fl.step(t, self.bars([(100, 100.3, 99.1, 99.15), (99.15, 99.3, 99.1, 99.15), (99.15, 99.3, 99.05, 99.1)]))
        self.assertEqual((ev[-1]["kind"], ev[-1]["at_ms"]), ("invalid", T0 + 3 * M5))   # the 15m close only
        self.assertIn("Setup invalidated", fl.text(t, ev[-1]))

    def test_alert_lists_the_management(self):
        txt = lv.message(dict(self.alert(), label="PAPER"))
        self.assertIn("After TP1: stop to entry + fees, trail the rest behind the last 5m swing / EMA9", txt)
        self.assertIn("exit at market if +0.5R is not reached within 6 5m candles (30m)", txt)
        self.assertIn("Invalidation: exit on a 15m close below 99.20", txt)


if __name__ == "__main__":
    unittest.main()
