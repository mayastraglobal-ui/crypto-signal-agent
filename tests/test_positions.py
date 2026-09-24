"""Phase 10 tests: the 5-minute entry-confirmation protocol (section 8), the 5m backtest and its fair
control twin, the signal state machine (section 13), position monitoring (section 16) and the position book.

Run:  python -m unittest discover -s tests -v
"""
import datetime as dt
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
from engine import confirm5m as C5  # noqa: E402
from engine import positions as P  # noqa: E402
from engine import regime as RG  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402
from test_data_quality import run_copy  # noqa: E402

CFG = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
M5 = 300_000
T0 = 1_700_000_100_000 // 900_000 * 900_000        # a 15m boundary


def m5_bars(rows, start=T0):
    """5m arrays from rows of (open, high, low, close, rel_vol) + optional flags dict."""
    n = len(rows)
    out = {k: np.array([r[i] for r in rows], float) for i, k in enumerate(("open", "high", "low", "close"))}
    out["open_time"] = start + M5 * np.arange(n, dtype=np.int64)
    out["close_time"] = out["open_time"] + M5 - 1
    rng = np.maximum(out["high"] - out["low"], 1e-12)
    out["body_pct"] = np.abs(out["close"] - out["open"]) / rng
    out["rel_vol"] = np.array([r[4] for r in rows], float)
    for k in C5.NEEDS:
        if k not in ("body_pct", "rel_vol"):
            out[k] = np.array([float((r[5] if len(r) > 5 else {}).get(k, 0)) for r in rows])
    return out


NEUTRAL = (100.0, 100.3, 99.7, 100.0, 1.2)          # doji: never confirms
GOOD_UP = (100.0, 100.6, 99.95, 100.5, 1.5)         # body 0.5/0.65 = 77%, rel vol 1.5, close +0.5 (R = 5 -> 0.1R)


class Protocol(unittest.TestCase):
    """engine/confirm5m.check: entry 100, stop 95 (R = 5), long unless said otherwise."""

    def chk(self, rows, d=1, entry=100.0, stop=95.0, after=T0):
        return C5.check(m5_bars(rows), after, d, entry, stop)

    def test_confirms_on_the_first_good_bar(self):
        r = self.chk([NEUTRAL, NEUTRAL, GOOD_UP, GOOD_UP])
        self.assertEqual((r["state"], r["idx"], r["bars"]), (C5.CONFIRMED, 2, 3))

    def test_each_condition_is_needed(self):
        for bad, why in [((100.0, 100.6, 99.95, 100.5, 0.9), "volume below average"),
                         ((100.0, 100.6, 99.4, 100.2, 1.5), "body 0.2/1.2 < 50%"),
                         ((100.5, 100.6, 99.95, 100.0, 1.5), "closes against the trade"),
                         ((101.0, 102.1, 100.95, 102.0, 1.5), "close 2.0 away > 0.2R = 1.0")]:
            r = self.chk([bad] * 6)
            self.assertEqual(r["state"], C5.EXPIRED, why)

    def test_expired_after_six_bars_awaiting_before(self):
        self.assertEqual(self.chk([NEUTRAL] * 6)["state"], C5.EXPIRED)
        self.assertEqual(self.chk([NEUTRAL] * 6 + [GOOD_UP])["state"], C5.EXPIRED)    # bar 7 is too late
        r = self.chk([NEUTRAL] * 4)
        self.assertEqual((r["state"], r["bars"]), (C5.AWAITING, 4))

    def test_invalidated_by_stop_or_structure_break(self):
        r = self.chk([NEUTRAL, (100.0, 100.2, 94.9, 99.0, 1.0), GOOD_UP])
        self.assertEqual((r["state"], r["idx"]), (C5.INVALIDATED, 1))
        r = self.chk([NEUTRAL, NEUTRAL + ({"smc_choch_down": 1},), GOOD_UP])
        self.assertEqual((r["state"], r["idx"]), (C5.INVALIDATED, 1))
        r = self.chk([NEUTRAL, NEUTRAL + ({"smc_bos_up": 1},), GOOD_UP])        # break WITH the trade: fine
        self.assertEqual(r["state"], C5.CONFIRMED)

    def test_opposing_displacement_blocks_later_bars(self):
        r = self.chk([NEUTRAL + ({"displacement_down": 1},), GOOD_UP, GOOD_UP])
        self.assertEqual(r["state"], C5.AWAITING)
        self.assertEqual(self.chk([NEUTRAL + ({"displacement_down": 1},)] + [GOOD_UP] * 5)["state"], C5.EXPIRED)

    def test_short_is_the_mirror(self):
        down = (100.0, 100.05, 99.4, 99.5, 1.5)
        r = self.chk([NEUTRAL, down], d=-1, stop=105.0)
        self.assertEqual((r["state"], r["idx"]), (C5.CONFIRMED, 1))
        self.assertEqual(self.chk([GOOD_UP] * 6, d=-1, stop=105.0)["state"], C5.EXPIRED)

    def test_optional_smc_signs_are_recorded_not_required(self):
        r = self.chk([NEUTRAL + ({"smc_sweep_bull": 1},), GOOD_UP + ({"bull_engulf": 1, "displacement_up": 1},)])
        self.assertEqual(r["state"], C5.CONFIRMED)
        self.assertEqual(r["smc"], ["5m displacement", "5m engulfing bar", "5m liquidity sweep"])

    def test_bars_before_the_trigger_close_are_never_used(self):
        rows = [GOOD_UP, NEUTRAL, NEUTRAL, NEUTRAL]
        self.assertEqual(self.chk(rows, after=T0)["state"], C5.CONFIRMED)
        r = self.chk(rows, after=T0 + 1)             # trigger closed at T0: bar 0 opened before -> ignored
        self.assertEqual((r["state"], r["bars"]), (C5.AWAITING, 3))

    def test_no_look_ahead_at_any_cut(self):
        rng = np.random.default_rng(3)
        for trial in range(200):
            rows = []
            for _ in range(10):
                o = 100 + rng.normal(0, 0.3)
                c = o + rng.normal(0, 0.4)
                rows.append((o, max(o, c) + abs(rng.normal(0, 0.2)), min(o, c) - abs(rng.normal(0, 0.2)), c,
                             rng.uniform(0.5, 2), {"smc_choch_down": float(rng.random() < 0.05),
                                                   "displacement_down": float(rng.random() < 0.05)}))
            full = self.chk(rows, stop=99.0)
            for cut in range(0, 10):
                part = self.chk(rows[:cut], stop=99.0)
                if part["state"] == C5.AWAITING:
                    self.assertTrue(full["idx"] is None or full["idx"] >= cut, (trial, cut))
                else:
                    self.assertEqual((part["state"], part["idx"]), (full["state"], full["idx"]), (trial, cut))

    def test_exit_rule_maps_to_the_5m_bar_closing_with_the_trigger_candle(self):
        ct15 = T0 + 900_000 * np.arange(1, 4) - 1
        m = m5_bars([NEUTRAL] * 9)
        out = C5.exit_on_5m(ct15, np.array([False, True, False]), m["close_time"])
        self.assertEqual(list(np.flatnonzero(out)), [5])
        self.assertIsNone(C5.exit_on_5m(ct15, None, m["close_time"]))


def aggregated(n15=400, seed=1):
    """Consistent 15m + 5m candles from one random 5m path (so 5m and 15m agree)."""
    rng = np.random.default_rng(seed)
    n5 = n15 * 3
    c = 100 * np.exp(np.cumsum(rng.normal(0, 0.002, n5)))
    o = np.r_[100, c[:-1]]
    h = np.maximum(o, c) * (1 + rng.uniform(0, 0.001, n5))
    l = np.minimum(o, c) * (1 - rng.uniform(0, 0.001, n5))
    ot5 = T0 + M5 * np.arange(n5, dtype=np.int64)
    d5 = pd.DataFrame(dict(open_time=ot5, open=o, high=h, low=l, close=c, volume=rng.uniform(1, 3, n5)))
    d5["close_time"] = d5["open_time"] + M5 - 1
    g = np.arange(n5) // 3
    d15 = pd.DataFrame(dict(open_time=d5.groupby(g)["open_time"].first(), open=d5.groupby(g)["open"].first(),
                            high=d5.groupby(g)["high"].max(), low=d5.groupby(g)["low"].min(),
                            close=d5.groupby(g)["close"].last(), volume=d5.groupby(g)["volume"].sum()))
    d15["close_time"] = d15["open_time"] + 900_000 - 1
    d15["_atr"] = (d15["high"] - d15["low"]).rolling(14, min_periods=1).mean()
    feats = pd.DataFrame({k: np.zeros(n5) for k in C5.NEEDS})
    rngb = np.maximum(d5["high"] - d5["low"], 1e-12)
    feats["body_pct"] = (d5["close"] - d5["open"]).abs() / rngb
    feats["rel_vol"] = 1.5
    return d15.reset_index(drop=True), d5, C5.arrays(d5, feats)


STRAT = dict(id="T", version="1.0", stop=dict(method="atr", atr=2.0), targets=None, time_stop_bars=12,
             cooldown_bars=0, confirm_5m=True)


class Backtest5m(unittest.TestCase):
    def signals(self, n, every=37):
        L = np.zeros(n, bool)
        L[20::every] = True
        return L, np.zeros(n, bool)

    def test_plain_twin_enters_like_the_normal_backtest(self):
        d15, _, m5 = aggregated()
        L, S = self.signals(len(d15))
        plain = scanner.backtest(d15, L, S, None, None, dict(STRAT, confirm_5m=False), CFG, "15m")
        twin = scanner.backtest_5m(d15, L, S, None, None, STRAT, CFG, "15m", {}, m5, confirm=False)
        self.assertEqual([t["signal_idx"] for t in twin][:3], [t["signal_idx"] for t in plain][:3])
        for a, b in zip(plain[:3], twin[:3]):
            self.assertAlmostEqual(a["entry"], b["entry"])          # same next-open entry, same slippage
            self.assertEqual(a["entry_time"], b["entry_time"])
            self.assertEqual(a["entry_idx"], b["entry_idx"])

    def test_confirmed_entry_is_the_close_of_the_confirming_bar(self):
        d15, _, m5 = aggregated()
        L, S = self.signals(len(d15))
        skipped = {}
        tr = scanner.backtest_5m(d15, L, S, None, None, STRAT, CFG, "15m", {}, m5, True, skipped)
        self.assertTrue(tr)
        slip = scanner.trade_costs(CFG, 1)["slip"]
        for t in tr:
            after = int(d15["close_time"].iloc[t["signal_idx"]]) + 1
            j0 = C5.first_bar(m5, after)
            entry0 = m5["open"][j0] * (1 + slip)
            chk = C5.check(m5, after, 1, entry0, entry0 - 2.0 * d15["_atr"].iloc[t["signal_idx"]])
            self.assertEqual(chk["state"], C5.CONFIRMED)
            self.assertAlmostEqual(t["entry"], m5["close"][chk["idx"]] * (1 + slip))
            self.assertEqual(t["entry_time"], int(m5["open_time"][chk["idx"] + 1]))
            self.assertGreaterEqual(t["entry_idx"], t["signal_idx"] + 1)
        self.assertEqual(sum(skipped.values()) + len(tr) >= len(tr), True)

    def test_nothing_confirms_nothing_trades(self):
        d15, d5, m5 = aggregated()
        m5 = dict(m5, rel_vol=np.zeros(len(m5["close"])))           # volume never confirms
        L, S = self.signals(len(d15))
        skipped = {}
        self.assertEqual(scanner.backtest_5m(d15, L, S, None, None, STRAT, CFG, "15m", {}, m5, True, skipped), [])
        self.assertGreater(skipped.get("5m_expired", 0), 0)

    def test_no_look_ahead_trades_before_the_cut_do_not_change(self):
        d15, d5, _ = aggregated(seed=5)
        L, S = self.signals(len(d15), every=11)
        feats = pd.DataFrame({k: np.zeros(len(d5)) for k in C5.NEEDS})
        feats["body_pct"] = (d5["close"] - d5["open"]).abs() / np.maximum(d5["high"] - d5["low"], 1e-12)
        feats["rel_vol"] = 1.5
        full = scanner.backtest_5m(d15, L, S, None, None, STRAT, CFG, "15m", {}, C5.arrays(d5, feats))
        for cut15 in (150, 220, 333):
            cut5 = cut15 * 3
            part = scanner.backtest_5m(d15.iloc[:cut15].copy(), L[:cut15], S[:cut15], None, None, STRAT, CFG, "15m",
                                       {}, C5.arrays(d5.iloc[:cut5], feats.iloc[:cut5]))
            done = [t for t in full if t["exit_idx"] < cut15 - 1]
            self.assertEqual([(t["signal_idx"], round(t["r"], 9)) for t in part[:len(done)]],
                             [(t["signal_idx"], round(t["r"], 9)) for t in done], cut15)

    def test_triggers_before_the_5m_history_are_skipped(self):
        d15, d5, m5 = aggregated()
        L, S = self.signals(len(d15), every=5)
        cut = 600                                            # 5m history starts at 15m candle 200
        m5_late = {k: v[cut:] for k, v in m5.items()}
        tr = scanner.backtest_5m(d15, L, S, None, None, STRAT, CFG, "15m", {}, m5_late, confirm=False)
        self.assertTrue(tr)
        self.assertTrue(all(t["signal_idx"] >= 199 and t["entry_time"] >= m5_late["open_time"][0] for t in tr))
        first = min(t["signal_idx"] for t in tr)
        self.assertEqual(tr[0]["entry_time"], int(d15["close_time"].iloc[first]) + 1)

    def test_dispatch_and_split_by_5m_period(self):
        d15, _, m5 = aggregated()
        L, S = self.signals(len(d15))
        self.assertEqual(scanner.run_backtest(d15, L, S, None, None, dict(STRAT, confirm_5m=False), CFG, "15m"),
                         scanner.backtest(d15, L, S, None, None, dict(STRAT, confirm_5m=False), CFG, "15m"))
        self.assertEqual(scanner.run_backtest(d15, L, S, None, None, STRAT, CFG, "15m", {}, None, None), [])
        tr = scanner.run_backtest(d15, L, S, None, None, STRAT, CFG, "15m", {}, None, m5)
        scanner.mark_oos_for(STRAT, tr, len(d15), CFG, m5)
        split = m5["open_time"][0] + (m5["close_time"][-1] - m5["open_time"][0]) * CFG["validation"]["in_sample_share"]
        self.assertTrue(all(t["oos"] == (t["entry_time"] >= split) for t in tr))
        self.assertTrue(any(t["oos"] for t in tr) and not all(t["oos"] for t in tr))


class Cards(unittest.TestCase):
    RAW = yaml.safe_load(open(os.path.join(ROOT, "strategies.yaml")))

    def test_5m_cards_are_their_twin_plus_the_5m_check(self):
        ok, problems, _ = SP.load(self.RAW, RG.LABELS, scanner.TF_ORDER)
        self.assertEqual(problems, {})
        by = {s["id"]: s for s in ok}
        fives = [s for s in ok if s.get("confirm_5m")]
        self.assertEqual(sorted(s["id"] for s in fives), ["S5-SWEEP-MSS-FVG-5M", "S6-OB-FVG-5M",
                                                          "S7-SILVER-BULLET-5M", "S8-PDH-PDL-SWEEP-5M"])
        for s in fives:
            tw = by[s["control_twin"]]
            self.assertEqual(s["id"], tw["id"] + "-5M")
            for k in SP.LOGIC_KEYS:
                if k not in ("confirm_5m", "timeframes"):
                    self.assertEqual(s.get(k), tw.get(k), (s["id"], k))
            self.assertTrue(set(s["timeframes"]) <= {"15m", "30m"})

    def test_a_5m_card_that_changes_anything_else_is_refused(self):
        raw = [dict(r) for r in self.RAW]
        five = next(r for r in raw if r["id"] == "S6-OB-FVG-5M")
        five["time_stop_bars"] = 31
        _, problems, _ = SP.load(raw, RG.LABELS, scanner.TF_ORDER)
        self.assertIn("S6-OB-FVG-5M", problems)
        five["time_stop_bars"] = 30
        five["timeframes"] = ["1h"]
        _, problems, _ = SP.load(raw, RG.LABELS, scanner.TF_ORDER)
        self.assertIn("S6-OB-FVG-5M", problems)
        s8 = next(r for r in raw if r["id"] == "S8-PDH-PDL-SWEEP-5M")
        s8["timeframes"] = ["1h", "30m"]                  # its twin runs on 1h too - still only 15m / 30m
        _, problems, _ = SP.load(raw, RG.LABELS, scanner.TF_ORDER)
        self.assertIn("S8-PDH-PDL-SWEEP-5M", problems)
        s8["timeframes"] = ["30m"]
        five["timeframes"] = ["15m"]
        del five["control_twin"]
        _, problems, _ = SP.load(raw, RG.LABELS, scanner.TF_ORDER)
        self.assertIn("S6-OB-FVG-5M", problems)


class States(unittest.TestCase):
    def test_allowed_and_forbidden_moves(self):
        for a, b in [(None, P.AWAITING), (None, P.TRIGGERED), (P.AWAITING, P.EXPIRED), (P.AWAITING, P.INVALIDATED),
                     (P.AWAITING, P.TRIGGERED), (P.TRIGGERED, P.ACTIVE), (P.ACTIVE, P.TP1_HIT), (P.TP1_HIT, P.CLOSED),
                     (P.ACTIVE, P.CLOSED)]:
            P.check_move(a, b)
        for a, b in [(None, P.ACTIVE), (P.AWAITING, P.ACTIVE), (P.CLOSED, P.ACTIVE), (P.EXPIRED, P.TRIGGERED),
                     (P.TP1_HIT, P.ACTIVE), (P.ACTIVE, P.EXPIRED)]:
            with self.assertRaises(ValueError, msg=f"{a}->{b}"):
                P.check_move(a, b)

    def test_close_reasons(self):
        self.assertEqual([P.close_reason(x) for x in ("SL", "TP1+stop", "TP2+stop", "TP2", "TP1", "time", "exit-rule")],
                         ["SL", "BE", "TRAIL", "TP2", "TP1", "TIME", "EXIT_RULE"])

    def test_rows_from_before_phase_10(self):
        self.assertEqual(P.row_state({"status": "OPEN"}), P.ACTIVE)
        self.assertEqual(P.row_state({"status": "SL", "state": np.nan}), P.CLOSED)
        self.assertEqual(P.row_state({"status": "OPEN", "state": P.AWAITING}), P.AWAITING)

    def test_warnings_only_after_entry(self):
        ct = np.arange(10) * 100
        f = {k: np.zeros(10, bool) for k in ("bos_up", "bos_down", "choch_up", "choch_down", "disp_up", "disp_down")}
        atr = np.ones(10)
        f["choch_down"][3] = True
        self.assertEqual(P.warnings(1, 500, ct, f, atr, "WEAK_BULL", "WEAK_BULL"), [])      # before the entry
        self.assertIn("opposing structure break (MSS/CHoCH/BOS)", P.warnings(1, 200, ct, f, atr, None, None))
        self.assertEqual(P.warnings(-1, 200, ct, f, atr, None, None), [])                    # with a short: fine
        atr2 = atr.copy()
        atr2[-1] = 2.5
        self.assertTrue(any("volatility" in w for w in P.warnings(1, 500, ct, f, atr2, None, None)))
        self.assertEqual(P.warnings(1, 500, ct, f, atr, "RANGE", "WEAK_BULL"), ["regime changed WEAK_BULL -> RANGE"])
        self.assertEqual(P.next_action(P.TP1_HIT, ["x"]), "HOLD - stop at breakeven · watch: x")


def log_row(**kw):
    r = {c: np.nan for c in scanner.LOG_COLS}
    r.update(id="BTC-15m-T-x", signal_time_utc="2023-11-14 22:14", coin="BTC", tf="15m", strategy="T",
             direction="LONG", entry=100.0, stop=95.0, tp1=110.0, tp2=115.0, tp3=np.nan, max_hold_bars=12,
             status="OPEN", closed_time_utc="", version="1.0", stage="PAPER_TRADING", tp_split="0.5/0.5")
    r.update(kw)
    return r


class Book(unittest.TestCase):
    NOW = dt.datetime(2026, 9, 24, 12, 0, tzinfo=dt.timezone.utc)      # a Thursday

    def test_empty_book_says_so(self):
        b = P.build(scanner.load_log(os.path.join(ROOT, "no_such.csv")), self.NOW)
        text = P.lines(b)
        self.assertTrue(text[0].startswith("POSITION BOOK — 2026-09-24 12:00 UTC / 2026-09-24 20:00 Beijing"))
        self.assertEqual(text[1], "No open or pending positions.")
        self.assertIn("Heat: 0/3", text[2])

    def test_live_paper_awaiting_and_the_day_week_sums(self):
        rows = [log_row(id="a", stage="APPROVED", state=P.ACTIVE),
                log_row(id="b", stage="APPROVED", state=P.TP1_HIT, current_stop=100.0),
                log_row(id="c", state=P.ACTIVE),
                log_row(id="d", state=P.AWAITING, bars_5m=2),
                log_row(id="e", stage="APPROVED", state=P.CLOSED, status="SL", result_r=-1.0,
                        closed_time_utc="2026-09-24 09:00", close_reason="SL"),
                log_row(id="f", stage="APPROVED", state=P.CLOSED, status="TP2", result_r=2.5,
                        closed_time_utc="2026-09-22 09:00", close_reason="TP2"),        # Tuesday: week only
                log_row(id="g", stage="APPROVED", state=P.CLOSED, status="SL", result_r=-1.0,
                        closed_time_utc="2026-09-20 09:00"),                            # last week: neither
                log_row(id="h", state=P.CLOSED, status="TP1", result_r=0.8, closed_time_utc="2026-09-24 10:00"),
                log_row(id="i", state=P.EXPIRED, status="EXPIRED", closed_time_utc="2026-09-24 10:00")]
        b = P.build(pd.DataFrame(rows), self.NOW, {("BTC", "15m"): 102.5})
        self.assertEqual([p["id"] for p in b["active"]], ["a", "b"])
        self.assertEqual([p["id"] for p in b["paper"]], ["c"])
        self.assertEqual([p["id"] for p in b["awaiting"]], ["d"])
        self.assertEqual(sorted(p["id"] for p in b["closed_today"]), ["e", "h", "i"])
        self.assertEqual((b["day_r"], b["week_r"], b["paper_day_r"], b["heat"]), (-1.0, 1.5, 0.8, 2))
        self.assertEqual(b["active"][0]["open_r"], 0.5)
        self.assertEqual(b["active"][1]["stop"], 100.0)                  # stop moved to breakeven
        text = "\n".join(P.lines(b))
        self.assertIn("Awaiting:  BTC · LONG · 15m · T (PAPER_TRADING) · 2/6 5m bars", text)
        self.assertIn("Day: -1.00R (limit -3R) · Week: +1.50R (limit -6R) · Heat: 2/3", text)


class ForwardStates(unittest.TestCase):
    """scanner.resolve_pending + update_forward on consistent synthetic candles."""

    def frames(self, rows5):
        m = m5_bars(rows5, start=T0)
        d5 = pd.DataFrame({k: m[k] for k in ("open_time", "open", "high", "low", "close")})
        d5["close_time"] = m["close_time"]
        return m, d5

    def run_rows(self, rows, rows5, exits=None):
        m, d5 = self.frames(rows5)
        log = pd.DataFrame(rows, columns=scanner.LOG_COLS)
        for c in scanner.TEXT_COLS:
            log[c] = log[c].astype(object)
        ev = []
        log = scanner.resolve_pending(log, {"BTC": m}, CFG, ev, "now")
        data = {("BTCUSDT", "5m"): d5}
        quality = {("BTC", "5m"): dict(state="GOOD", problems=[])}
        log, closed = scanner.update_forward(log, data, quality, None, CFG, {}, {}, exits, {}, ev, "now")
        return log, ev, closed

    def awaiting(self, **kw):
        trig = pd.to_datetime(T0 - 1, unit="ms").strftime("%Y-%m-%d %H:%M")       # trigger candle closed at T0-1
        return log_row(signal_time_utc=trig, state=P.AWAITING, planned_entry=100.0, sim_tf="5m", bars_5m=0, **kw)

    def test_confirm_then_tp1_then_breakeven(self):
        rows5 = [NEUTRAL, GOOD_UP, (100.5, 111.0, 100.4, 110.5, 1.0), (110.5, 110.6, 100.0, 100.2, 1.0)]
        log, ev, closed = self.run_rows([self.awaiting()], rows5)
        r = log.iloc[0]
        slip = scanner.trade_costs(CFG, 1)["slip"]
        self.assertAlmostEqual(float(r["entry"]), 100.5 * (1 + slip))
        self.assertEqual((r["state"], r["close_reason"], r["status"]), (P.CLOSED, "BE", "TP1+stop"))
        self.assertEqual([(e["from_state"], e["to_state"]) for e in ev],
                         [(P.AWAITING, P.TRIGGERED), (P.TRIGGERED, P.ACTIVE), (P.ACTIVE, P.TP1_HIT),
                          (P.TP1_HIT, P.CLOSED)])
        self.assertEqual(closed, [0])

    def test_tp1_hit_and_still_open(self):
        rows5 = [NEUTRAL, GOOD_UP, (100.5, 111.0, 100.4, 110.5, 1.0), (110.5, 111.0, 109.0, 110.0, 1.0)]
        log, ev, _ = self.run_rows([self.awaiting()], rows5)
        r = log.iloc[0]
        self.assertEqual((r["state"], r["status"]), (P.TP1_HIT, "OPEN"))
        self.assertAlmostEqual(float(r["current_stop"]), float(r["entry"]))      # breakeven
        self.assertTrue(r["next_action"].startswith("HOLD - stop at breakeven"))

    def test_expired_and_invalidated_leave_no_result(self):
        log, ev, _ = self.run_rows([self.awaiting()], [NEUTRAL] * 6)
        r = log.iloc[0]
        self.assertEqual((r["state"], r["status"]), (P.EXPIRED, P.EXPIRED))
        self.assertTrue(pd.isna(r["result_r"]))
        self.assertEqual(scanner.forward_stats(log), {})                        # not a trade
        log, ev, _ = self.run_rows([self.awaiting()], [NEUTRAL, (100.0, 100.1, 94.0, 95.5, 1.0)])
        self.assertEqual(log.iloc[0]["state"], P.INVALIDATED)
        log, ev, _ = self.run_rows([self.awaiting()], [NEUTRAL, NEUTRAL])
        self.assertEqual((log.iloc[0]["state"], int(log.iloc[0]["bars_5m"])), (P.AWAITING, 2))
        self.assertEqual(ev, [])

    def test_a_trigger_older_than_the_5m_history_is_not_decided_on_later_bars(self):
        trig = pd.to_datetime(T0 - 3 * 900_000 - 1, unit="ms").strftime("%Y-%m-%d %H:%M")
        row = log_row(signal_time_utc=trig, state=P.AWAITING, planned_entry=100.0, sim_tf="5m", bars_5m=0)
        log, ev, _ = self.run_rows([row], [NEUTRAL, GOOD_UP])
        self.assertEqual(log.iloc[0]["state"], P.EXPIRED)
        self.assertIn("no longer available", log.iloc[0]["state_note"])

    def test_exit_rule_is_applied_like_in_the_backtest(self):
        rows5 = [NEUTRAL, GOOD_UP, NEUTRAL, NEUTRAL, NEUTRAL, NEUTRAL]
        ct15 = T0 + 900_000 * np.arange(1, 3) - 1                  # two 15m candles after the trigger
        exits = {("BTC", "15m", "T@1.0"): (ct15, np.array([False, True]), np.array([False, False]))}
        log, _, _ = self.run_rows([self.awaiting()], rows5, exits)
        self.assertEqual((log.iloc[0]["state"], log.iloc[0]["close_reason"]), (P.CLOSED, "EXIT_RULE"))
        log, _, _ = self.run_rows([self.awaiting()], rows5, None)
        self.assertEqual(log.iloc[0]["state"], P.ACTIVE)

    def test_time_stop_is_the_same_clock_time_on_5m_bars(self):
        rows5 = [NEUTRAL, GOOD_UP] + [(100.5, 100.8, 100.2, 100.5, 1.0)] * 5
        log, ev, _ = self.run_rows([self.awaiting(max_hold_bars=1)], rows5)     # 1 x 15m = 3 x 5m bars
        r = log.iloc[0]
        self.assertEqual((r["state"], r["close_reason"]), (P.CLOSED, "TIME"))
        self.assertEqual(r["closed_time_utc"], pd.to_datetime(T0 + 5 * M5 - 1, unit="ms").strftime("%Y-%m-%d %H:%M"))

    def test_old_log_file_still_loads_and_runs(self):
        old_cols = scanner.LOG_COLS[:scanner.LOG_COLS.index("state")]
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "signals_log.csv")
            trig = pd.to_datetime(T0 - 1, unit="ms").strftime("%Y-%m-%d %H:%M")
            pd.DataFrame([{k: v for k, v in log_row(signal_time_utc=trig, tf="5m").items() if k in old_cols}],
                         columns=old_cols).to_csv(p, index=False)
            log = scanner.load_log(p)
        self.assertEqual(list(log.columns), scanner.LOG_COLS)
        rows5 = [(100.0, 111.0, 99.9, 110.8, 1.0), (110.8, 116.0, 110.0, 115.5, 1.0)]
        m, d5 = self.frames(rows5)
        log, closed = scanner.update_forward(log, {("BTCUSDT", "5m"): d5}, {("BTC", "5m"): dict(state="GOOD")},
                                             None, CFG, {}, {}, None, {}, [], "now")
        self.assertEqual((log.iloc[0]["state"], log.iloc[0]["close_reason"]), (P.CLOSED, "TP2"))

    def test_paper_signals_are_logged(self):              # the Phase 8 bug: PAPER_TRADING never reached the log
        with open(os.path.join(ROOT, "scanner.py")) as f:
            src = f.read()
        self.assertIn('if stage not in ("VALIDATION", "PAPER_TRADING", "APPROVED"):', src)


class EndToEnd(unittest.TestCase):
    def test_offline_scan_moves_logged_signals_and_writes_the_book(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "reports"))
            now = pd.Timestamp.now(tz="UTC").floor("15min") - pd.Timedelta(minutes=15)
            trig = (now - pd.Timedelta(milliseconds=1)).strftime("%Y-%m-%d %H:%M")
            old = (now - pd.Timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
            rows = [log_row(id="await", signal_time_utc=trig, state=P.AWAITING, planned_entry=1.0, entry=1.0,
                            stop=0.0001, tp1=1e9, tp2=np.nan, sim_tf="5m", bars_5m=0),
                    log_row(id="old", signal_time_utc=old, entry=1.0, stop=0.0001, tp1=1e9, tp2=np.nan,
                            tp_split="1")]
            pd.DataFrame(rows, columns=scanner.LOG_COLS).to_csv(
                os.path.join(tmp, "reports", "signals_log_offline.csv"), index=False)
            p = run_copy(tmp, "scanner.py", "--offline", "--coins", "4")
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            log = pd.read_csv(os.path.join(tmp, "reports", "signals_log_offline.csv"))
            self.assertEqual(log["id"].tolist()[:2], ["await", "old"])          # kept, not duplicated
            self.assertEqual(log["id"].nunique(), len(log))
            a, o = log.iloc[0], log.iloc[1]
            self.assertGreaterEqual(int(a["bars_5m"]), 1)                   # the protocol looked at 5m bars
            self.assertIn(o["state"], (P.ACTIVE, P.TP1_HIT, P.CLOSED))         # old-format row got a state
            with open(os.path.join(tmp, "reports", "positions_offline.json")) as f:
                book = json.load(f)
            self.assertTrue(book["text"][0].startswith("POSITION BOOK"))
            with open(os.path.join(tmp, "reports", "latest.md")) as f:
                md = f.read()
            self.assertIn("POSITION BOOK", md.split("## 0. Data check")[0])      # the report opens with it
            self.assertIn("### 2c. Watching", md)
            self.assertFalse(os.path.exists(os.path.join(tmp, "reports", "signals_log.csv")))   # real log untouched
            with open(os.path.join(tmp, "reports", "latest.json")) as f:
                rep = json.load(f)
            self.assertEqual(rep["position_book_text"], book["text"])


if __name__ == "__main__":
    unittest.main()
