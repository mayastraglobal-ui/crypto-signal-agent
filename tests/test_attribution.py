"""Phase 9 tests: failure attribution (section 17) - MAE / MFE, every reason tag on hand-made candles,
losers-vs-winners statistics, the diagnosis, missed moves, no look-ahead, the forward test + failure journal.

Run:  python -m unittest discover -s tests -v
"""
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
from engine import attribution as AT  # noqa: E402
from engine import features as F  # noqa: E402
from engine import regime as RG  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402

CFG = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
A = AT.settings(CFG.get("attribution"))
H1 = 3_600_000


def card(**kw):
    c = dict(id="X", version="1.0", family="trend_following", gate="trend", regimes=["STRONG_BULL", "WEAK_BULL"],
             stop=dict(method="atr", atr=1.0), time_stop_bars=20, long=["close > open"], short=["close < open"])
    c.update(kw)
    return c


def ctx(n=60, **over):
    """A flat, calm market: every array can be overridden."""
    c = dict(open=np.full(n, 100.0), high=np.full(n, 100.5), low=np.full(n, 99.5), close=np.full(n, 100.0),
             atr=np.full(n, 1.0), ema20=np.full(n, 100.0), rsi=np.full(n, 50.0), adx=np.full(n, 30.0),
             rel_vol=np.full(n, 1.0), disp_up=np.zeros(n, bool), disp_dn=np.zeros(n, bool),
             fail_up=np.zeros(n, bool), fail_dn=np.zeros(n, bool), h4_bull_ob_low=np.full(n, np.nan),
             h4_bear_ob_high=np.full(n, np.nan), kz=np.array(["London"] * n, dtype=object), intraday=True,
             reg={"1h": (np.array(["WEAK_BULL"] * n, dtype=object), np.array([None] * n, dtype=object))}, n=n)
    c.update(over)
    return c


def trade(**kw):
    t = dict(dir=1, signal_idx=20, entry_idx=21, exit_idx=25, entry=100.0, R=1.0, tp1=101.0, r=-1.0, reason="SL",
             hit=0, mae_r=-1.0, mfe_r=0.5, cost_r=0.1, funding_r=0.0, bars=5)
    t.update(kw)
    return t


class MaeMfe(unittest.TestCase):
    def test_simulator_measures_the_worst_and_best_point(self):
        o = np.array([100.0, 100.0, 100.5])
        h = np.array([100.8, 101.5, 102.2])
        l = np.array([99.4, 99.9, 100.2])
        c = np.array([100.0, 100.5, 102.0])
        res = scanner.simulate_trade(o, h, l, c, 0, 1, 100.0, 1.0, CFG, 10, 1.0, tps=[102.0], split=[1.0])
        self.assertEqual(res["reason"], "TP1")
        self.assertAlmostEqual(res["mae_r"], -0.6)
        self.assertAlmostEqual(res["mfe_r"], 2.2)
        short = scanner.simulate_trade(o, h, l, c, 0, -1, 100.0, 5.0, CFG, 3, 8.0)
        self.assertAlmostEqual(short["funding_r"], 3 * CFG["costs"]["short"]["funding_pct_per_8h"] / 100 * 100 / 5)
        self.assertAlmostEqual(short["mae_r"], -2.2 / 5)


class Conditions(unittest.TestCase):
    def tags(self, c, d=1, strat=None, t=20):
        return AT.conditions(c, t, d, strat or card(), A)

    def test_calm_market_has_no_tags(self):
        self.assertEqual(self.tags(ctx()), [])

    def test_each_condition(self):
        n = 60
        self.assertIn("range_market", self.tags(ctx(adx=np.full(n, 15.0))))
        self.assertNotIn("range_market", self.tags(ctx(adx=np.full(n, 15.0)), strat=card(gate="mean_reversion")))
        strong_bear = {"1h": (np.array(["WEAK_BULL"] * n, dtype=object), np.array([None] * n, dtype=object)),
                       "1d": (np.array(["STRONG_BEAR"] * n, dtype=object), np.array([None] * n, dtype=object))}
        self.assertIn("htf_conflict", self.tags(ctx(reg=strong_bear)))
        self.assertNotIn("htf_conflict", self.tags(ctx(reg=strong_bear), d=-1))
        self.assertIn("low_relative_volume", self.tags(ctx(rel_vol=np.full(n, 0.5))))
        self.assertIn("overextended_entry", self.tags(ctx(close=np.full(n, 102.5))))       # 2.5 ATR above EMA20
        self.assertIn("overextended_entry", self.tags(ctx(rsi=np.full(n, 80.0))))
        self.assertNotIn("overextended_entry", self.tags(ctx(rsi=np.full(n, 80.0)), d=-1))
        late = np.full(n, 100.0)
        late[20] = 103.5                                                                     # +3.5 ATR in 10 candles
        self.assertIn("late_entry", self.tags(ctx(close=late, ema20=late)))
        self.assertIn("wrong_session", self.tags(ctx(kz=np.array(["Asia"] * n, dtype=object))))
        self.assertNotIn("wrong_session", self.tags(ctx(kz=np.array([None] * n, dtype=object), intraday=False)))
        self.assertIn("data_issue", AT.conditions(ctx(), 20, 1, card(), A, data_ok=False))

    def test_no_displacement_only_where_a_strong_candle_is_claimed(self):
        self.assertIn("no_displacement", self.tags(ctx(), strat=card(family="breakout")))
        self.assertIn("no_displacement", self.tags(ctx(), strat=card(family="smc", gate="trend")))
        self.assertNotIn("no_displacement", self.tags(ctx(), strat=card(family="smc", gate="reversal")))
        self.assertNotIn("no_displacement", self.tags(ctx(), strat=card()))
        disp = np.zeros(60, bool)
        disp[19] = True
        self.assertNotIn("no_displacement", self.tags(ctx(disp_up=disp), strat=card(family="breakout")))


class Outcomes(unittest.TestCase):
    def tags(self, c, tr, strat=None):
        return AT.outcome_tags(c, tr, dict(strat or card(), _A=A), "1h")

    def test_each_outcome_tag(self):
        n = 60
        self.assertIn("stop_too_wide", self.tags(ctx(), trade(R=3.0)))
        big = np.full(n, 100.5)
        big[23] = 104.0
        self.assertIn("volatility_spike", self.tags(ctx(high=big), trade()))
        fail = np.zeros(n, bool)
        fail[23] = True
        self.assertIn("false_breakout", self.tags(ctx(fail_up=fail), trade(), card(family="breakout")))
        self.assertNotIn("false_breakout", self.tags(ctx(fail_up=fail), trade()))              # not a breakout idea
        flip = np.array(["WEAK_BULL"] * n, dtype=object)
        flip[24] = "WEAK_BEAR"
        self.assertIn("trend_reversal", self.tags(ctx(reg={"1h": (flip, np.array([None] * n, dtype=object))}), trade()))
        already = np.array(["WEAK_BEAR"] * n, dtype=object)             # regime was already against it at entry
        self.assertNotIn("trend_reversal", self.tags(ctx(reg={"1h": (already, np.array([None] * n, dtype=object))}),
                                                     trade(), card(regimes=list(RG.LABELS))))
        out = np.array(["WEAK_BULL"] * n, dtype=object)
        out[24] = "RANGE"
        tg = self.tags(ctx(reg={"1h": (out, np.array([None] * n, dtype=object))}), trade())
        self.assertIn("regime_mismatch", tg)
        self.assertNotIn("trend_reversal", tg)
        ob = np.full(n, 99.8)
        lowc = np.full(n, 100.0)
        lowc[23] = 99.5
        s6 = card(family="smc", long=["h4_bull_ob_high < 1"])
        self.assertIn("ob_failed", self.tags(ctx(h4_bull_ob_low=ob, close=lowc), trade(), s6))
        self.assertNotIn("ob_failed", self.tags(ctx(h4_bull_ob_low=ob), trade(), s6))

    def test_loser_only_tags(self):
        n = 60
        self.assertIn("fees_slippage", self.tags(ctx(), trade(r=-0.05, cost_r=0.1, reason="time")))
        self.assertNotIn("fees_slippage", self.tags(ctx(), trade(r=-0.5, cost_r=0.1)))
        self.assertNotIn("fees_slippage", self.tags(ctx(), trade(r=-0.15, cost_r=0.1, reason="time")))   # costs < loss
        self.assertIn("funding", self.tags(ctx(), trade(dir=-1, r=-0.02, funding_r=0.05, tp1=99.0, reason="time")))
        after = np.full(n, 100.5)
        after[27] = 101.2                                                   # TP1 (101) reached after the stop
        self.assertIn("stop_too_tight", self.tags(ctx(high=after), trade()))
        late = np.full(n, 100.5)
        late[45] = 101.2                                                    # ... but only after the hold time
        self.assertNotIn("stop_too_tight", self.tags(ctx(high=late), trade()))
        self.assertIn("bad_target", self.tags(ctx(), trade(mfe_r=0.9, reason="time", r=-0.3)))
        sweep = card(family="smc", gate="reversal", stop=dict(method="structure", long_level="smc_sweep_bull_low",
                                                             short_level="smc_sweep_bear_high"))
        self.assertIn("sweep_continued", self.tags(ctx(), trade(), sweep))
        self.assertIn("indicator_lag", self.tags(ctx(), trade(mfe_r=0.1)))
        self.assertNotIn("indicator_lag", self.tags(ctx(), trade(mfe_r=0.1), card(family="breakout")))
        winner = self.tags(ctx(high=after), trade(r=1.5, reason="TP1", hit=1, mfe_r=0.1))
        self.assertFalse(set(winner) & set(AT.LOSER_TAGS))                 # never on a winning trade


class Statistics(unittest.TestCase):
    def trades(self, tag_in_losers, tag_in_winners, n_l=40, n_w=60, tag="late_entry"):
        out = [dict(r=-1.0, tags=[tag] if i < tag_in_losers else [], mae_r=-1.0, mfe_r=0.3, dir=1, regime="WEAK_BULL",
                    session="London", cost_r=0.1, funding_r=0.0) for i in range(n_l)]
        out += [dict(r=1.0, tags=[tag] if i < tag_in_winners else [], mae_r=-0.4, mfe_r=1.2, dir=1, regime="WEAK_BULL",
                     session="London", cost_r=0.1, funding_r=0.0) for i in range(n_w)]
        return out

    def test_systematic_only_when_more_common_in_losers(self):
        s = AT.summarize(self.trades(24, 6), A)                             # 60% of losers vs 10% of winners
        self.assertEqual(s["systematic"], ["late_entry"])
        self.assertEqual((s["tags"]["late_entry"]["loss_share"], s["tags"]["late_entry"]["win_share"]), (0.6, 0.1))
        self.assertEqual(AT.summarize(self.trades(24, 36), A)["systematic"], [])   # just as common in winners
        self.assertEqual(AT.summarize(self.trades(12, 3, n_l=20, n_w=30), A)["systematic"], [])   # < 30 losses

    def test_loser_only_tags_use_their_share(self):
        s = AT.summarize(self.trades(12, 0, tag="stop_too_tight"), A)       # 30% of 40 losses
        self.assertEqual(s["tags"]["stop_too_tight"]["kind"], "losers only")
        self.assertEqual(s["systematic"], ["stop_too_tight"])
        self.assertEqual(AT.summarize(self.trades(8, 0, tag="stop_too_tight"), A)["systematic"], [])   # 20%
        self.assertEqual(AT.summarize(self.trades(12, 0, n_l=20, tag="stop_too_tight"), A)["systematic"], [])  # < 30

    def test_mae_mfe_and_costs(self):
        s = AT.summarize(self.trades(0, 0), A)
        self.assertEqual((s["mae_mfe"]["winners_mae_median"], s["mae_mfe"]["losers_mfe_median"]), (-0.4, 0.3))
        self.assertAlmostEqual(s["gross_avg_r"], s["avg_r"] + 0.1)
        self.assertEqual(s["by_regime"]["WEAK_BULL"]["n"], 100)

    def test_diagnosis_answers_the_questions(self):
        s = AT.summarize(self.trades(24, 6), A)
        lines = AT.diagnose(s, {"4h": 0.2}, A, [dict(change="stop atr 1.5→1.8", avg_r=0.3)])
        text = " ".join(lines)
        for word in ("Sample", "Regime", "Timing", "Stop / target", "stop atr 1.5→1.8", "Costs", "4h", "late_entry"):
            self.assertIn(word, text)
        few = AT.summarize(self.trades(0, 0, n_l=5, n_w=5), A)
        self.assertIn("too small", AT.diagnose(few, {}, A)[0])


class MissedMoves(unittest.TestCase):
    def frame(self, closes, now):
        n = len(closes)
        ot = now // H1 * H1 - H1 * np.arange(n, 0, -1)
        return pd.DataFrame({"open_time": ot, "close": closes}), ot

    def test_strong_move_found_and_checked(self):
        now = 1_790_000_000_000
        closes = np.full(60, 100.0)
        closes[50:58] = np.linspace(100, 107, 8)                            # +7 ATR in 7 hours ...
        closes[58:] = 107.0                                                 # ... and it stays there
        df, ot = self.frame(closes, now)
        moves = AT.strong_moves(df, np.full(60, 1.0), now, A)
        self.assertEqual(len(moves), 1)
        m = moves[0]
        self.assertEqual((m["dir"], m["size_atr"]), (1, 7.0))
        ct = ot + H1 - 1
        z = np.zeros(60, bool)
        raw = z.copy()
        raw[m["start"] - 1] = True                                          # a setup 1 hour before the move
        ok = np.ones(60, bool)
        self.assertEqual(AT.check_move(m, ct, raw, z, ok, ok, ok, raw, z, A), "signal")
        self.assertEqual(AT.check_move(m, ct, raw, z, z, ok, ok, z, z, A), "blocked by the regime gate")
        self.assertEqual(AT.check_move(m, ct, raw, z, ok, z, ok, z, z, A), "blocked by the permission gate")
        self.assertEqual(AT.check_move(m, ct, raw, z, ok, ok, ok, z, z, A), "no valid stop / target")
        self.assertEqual(AT.check_move(m, ct, z, z, ok, ok, ok, z, z, A), "no setup")
        early = z.copy()
        early[m["start"] - 6] = True                                        # too early to count
        self.assertEqual(AT.check_move(m, ct, early, z, ok, ok, ok, early, z, A), "no setup")
        self.assertIn("identifiable", AT.move_verdict({"a": "signal", "b": "no setup"}))
        self.assertIn("filtered out", AT.move_verdict({"a": "blocked by the regime gate"}))
        self.assertIn("not identifiable", AT.move_verdict({"a": "no setup"}))

    def test_old_or_small_moves_ignored(self):
        now = 1_790_000_000_000
        closes = np.full(60, 100.0)
        closes[5:12] = np.linspace(100, 110, 7)                             # strong but 2 days ago
        closes[12:] = 110.0
        df, _ = self.frame(closes, now)
        self.assertEqual(AT.strong_moves(df, np.full(60, 1.0), now, A), [])
        small = np.full(60, 100.0)
        small[50:58] = np.linspace(100, 104, 8)                             # only 4 ATR
        small[58:] = 104.0
        df, _ = self.frame(small, now)
        self.assertEqual(AT.strong_moves(df, np.full(60, 1.0), now, A), [])


class NoLookAhead(unittest.TestCase):
    def test_conditions_use_only_candles_up_to_the_signal(self):
        feed = scanner.Synthetic()
        df = feed.klines("BTCUSDT", "1h", 800)
        full = AT.context(df, F.compute(df, H1), {}, H1)
        s = card(family="breakout")
        for cut in (301, 555, 799):
            part = df.iloc[:cut]
            past = AT.context(part, F.compute(part, H1), {}, H1)
            for d in (1, -1):
                self.assertEqual(AT.conditions(full, cut - 1, d, s, A), AT.conditions(past, cut - 1, d, s, A), cut)


class ForwardTest(unittest.TestCase):
    def test_closed_signal_gets_mae_mfe_tags_and_a_journal_entry(self):
        feed = scanner.Synthetic()
        df = feed.klines("ETHUSDT", "1h", 400)
        i = 300
        entry = float(df["open"].iloc[i + 1])
        sig_close = pd.to_datetime(int(df["close_time"].iloc[i]), unit="ms").strftime("%Y-%m-%d %H:%M")
        R = float((df["high"] - df["low"]).iloc[i - 20:i].mean()) * 0.3             # a tight stop: it gets hit
        log = scanner.load_log().iloc[0:0]
        row = {c: np.nan for c in scanner.LOG_COLS}
        row.update(id="t1", signal_time_utc=sig_close, coin="ETH", tf="1h", strategy="trend_pullback", version="1.0",
                   stage="VALIDATION", direction="LONG", entry=entry, stop=entry - R, tp1=entry + 5 * R,
                   tp_split="1", max_hold_bars=60, status="OPEN", conditions="late_entry", regime_at_entry="WEAK_BULL",
                   session="London")
        log = pd.concat([log, pd.DataFrame([row])], ignore_index=True)
        ok, _, _ = SP.load(yaml.safe_load(open(os.path.join(ROOT, "strategies.yaml"))), RG.LABELS, scanner.TF_ORDER)
        cards = {SP.key(x): x for x in ok}
        q = {("ETH", "1h"): dict(state="GOOD")}
        out, closed = scanner.update_forward(log, {("ETHUSDT", "1h"): df}, q, feed, CFG, cards, {})
        self.assertEqual(closed, [0])
        r = out.iloc[0]
        self.assertNotEqual(r["status"], "OPEN")
        self.assertTrue(np.isfinite(float(r["mae_r"])) and np.isfinite(float(r["mfe_r"])))
        self.assertLessEqual(float(r["mae_r"]), 0)
        self.assertIsInstance(r["tags"], str)
        with tempfile.TemporaryDirectory() as tmp:
            old = scanner.MEMORY
            scanner.MEMORY = tmp
            try:
                scanner.write_failure_journal(out.loc[closed], pd.Timestamp("2026-09-24 20:00", tz="UTC"))
                scanner.write_failure_journal(out.loc[closed], pd.Timestamp("2026-09-24 21:00", tz="UTC"))
            finally:
                scanner.MEMORY = old
            with open(os.path.join(tmp, "failure_journal.md")) as f:
                text = f.read()
        self.assertEqual(text.count("# Failure journal"), 1)                 # header once, entries appended
        self.assertEqual(text.count("ETH LONG 1h"), 2)
        self.assertIn("late_entry", text)


if __name__ == "__main__":
    unittest.main()
