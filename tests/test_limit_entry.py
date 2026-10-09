"""Roadmap step 2B (operator request 2026-10-06): limit-order entries - the card setting, the backtest (maker fee,
no slippage, no fill = no trade, only the stop in the fill candle), the hourly paper record (AWAITING_FILL), the
Telegram alert and trade follow-up, the TradingView export and the emails."""
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
from engine import emails as em  # noqa: E402
from engine import follow as fl  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import pine  # noqa: E402
from engine import positions as P  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
H = 3_600_000
T0 = 1_700_000_100_000 // H * H
LIMIT = {"type": "limit", "offset_atr": 0.5, "valid_bars": 2}


def card(**kw):
    raw = dict(id="T", version="1.0", status="FORMALIZED", family="breakout", gate="trend", hypothesis="h",
               source="s", regimes=["STRONG_BULL"], timeframes=["1h"], long=["close > 1"], short=["close < 1"],
               stop={"method": "atr", "atr": 1.0}, time_stop_bars=6, known_weaknesses="w",
               targets={"long": ["2R", "3R"], "short": ["2R", "3R"], "split": [0.5, 0.5]})
    raw.update(kw)
    return raw


def frame(rows):
    """rows = [(open, high, low, close)] 1h candles; ATR fixed at 2."""
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"], dtype=float)
    df["open_time"] = T0 + np.arange(len(df)) * H
    df["close_time"] = df["open_time"] + H - 1
    df["_atr"] = 2.0
    return df


def zero_slip():
    c = copy.deepcopy(CFG)
    for side in ("long", "short"):
        c["costs"][side]["slippage_pct"] = 0.0
    return c


class Card(unittest.TestCase):
    def test_setting_is_checked(self):
        self.assertEqual(SP.entry_problems(card(entry=LIMIT)), [])
        self.assertEqual(SP.entry_problems(card()), [])
        self.assertEqual(SP.entry_problems(card(entry={"type": "market"})), [])
        bad = [{"type": "stop"}, {"type": "limit", "valid_bars": 0}, {"type": "limit", "valid_bars": 2.5},
               {"type": "limit", "valid_bars": 2, "offset_atr": -1}, {"type": "limit", "valid_bars": 2, "offset_atr": 3},
               {"type": "limit", "valid_bars": 2, "x": 1}, {"type": "market", "valid_bars": 2}, "limit"]
        for b in bad:
            self.assertTrue(SP.entry_problems(card(entry=b)), b)
        self.assertTrue(SP.entry_problems(card(entry=LIMIT, confirm_5m=True)))
        self.assertEqual(SP.limit_entry(card(entry=LIMIT)), (0.5, 2))
        self.assertIsNone(SP.limit_entry(card()))

    def test_cards_without_it_keep_their_fingerprint(self):
        plain = card()
        old = dict((k, plain.get(k)) for k in SP.LOGIC_KEYS if k not in SP.OPTIONAL_LOGIC)   # before step 2B
        import hashlib
        import json
        before = hashlib.sha256(json.dumps(old, sort_keys=True, default=str).encode()).hexdigest()[:16]
        self.assertEqual(SP.fingerprint(plain), before)
        self.assertNotEqual(SP.fingerprint(card(entry=LIMIT)), before)
        self.assertEqual(SP.change_count(card(), card(entry=LIMIT)), ["entry"])

    def test_the_limit_distance_is_in_the_20pct_test(self):
        s = SP._finish(SP.render(card(entry=LIMIT)), card(entry=LIMIT))
        labels = [v[0] for v in SP.variants(s, 20)]
        self.assertIn("entry offset_atr 0.5→0.4", labels)
        self.assertIn("entry offset_atr 0.5→0.6", labels)


class Backtest(unittest.TestCase):
    def run_bt(self, rows, d=1, cfg=None, at=0, **kw):
        df = frame(rows)
        sig = np.zeros(len(df), bool)
        sig[at] = True
        L, S = (sig, np.zeros(len(df), bool)) if d == 1 else (np.zeros(len(df), bool), sig)
        sk = {}
        tr = sc.backtest(df, L, S, None, None, card(entry=dict(LIMIT, **kw)), cfg or CFG, "1h", {}, sk)
        return tr, sk

    def test_fills_at_the_limit_with_the_maker_fee(self):
        # signal close 100, ATR 2 -> limit 99, stop 97, TP1 103, TP2 105
        rows = [(100, 100, 100, 100), (100, 100.5, 99.5, 100), (100, 100.2, 98.9, 99.5), (99.5, 103.2, 99.4, 103),
                (103, 105.5, 102.8, 105)]
        tr, _ = self.run_bt(rows)
        self.assertEqual(len(tr), 1)
        t = tr[0]
        self.assertEqual((t["entry"], t["entry_idx"], t["reason"]), (99.0, 2, "TP2"))
        k = sc.trade_costs(CFG, 1)
        gross = 0.5 * 4 + 0.5 * 6
        fees = k["maker"] * 99 + 0.5 * k["maker"] * 103 + 0.5 * k["maker"] * 105
        self.assertAlmostEqual(t["r"] * 2.0, gross - fees - t["funding_r"] * 2.0, places=6)
        self.assertAlmostEqual(t["cost_r"], 99 * (k["maker"] + k["taker"] + k["slip"]) / 2.0)

    def test_no_fill_no_trade(self):
        rows = [(100, 100, 100, 100), (100, 101, 99.5, 101), (101, 104, 100.5, 103.5), (103.5, 106, 103, 105)]
        tr, sk = self.run_bt(rows)
        self.assertEqual(tr, [])                                              # the move happened without us
        self.assertEqual(sk["limit_unfilled"], 1)

    def test_the_fill_candle_counts_the_stop_but_not_a_target(self):
        rows = [(100, 100, 100, 100), (100, 104, 98.5, 101), (101, 101.5, 100, 101)] + [(101, 101.5, 100.5, 101)] * 6
        tr, _ = self.run_bt(rows)                                             # touched 99 and TP1 103 in candle 1
        self.assertEqual(tr[0]["hit"], 0)                                     # TP1 not counted in the fill candle
        tr, _ = self.run_bt([(100, 100, 100, 100), (100, 100.2, 96.5, 97)] + [(97, 97.5, 96.8, 97)] * 6)
        self.assertEqual(tr[0]["reason"], "SL")                               # filled and stopped in one candle

    def test_short_is_the_mirror(self):
        rows = [(100, 100, 100, 100), (100, 101.1, 99.8, 100.5), (100.5, 100.6, 96.8, 97), (97, 97.2, 94.8, 95)]
        tr, _ = self.run_bt(rows, d=-1)
        self.assertEqual((tr[0]["entry"], tr[0]["entry_idx"], tr[0]["reason"]), (101.0, 1, "TP2"))

    def test_data_ending_inside_the_window_stops_the_backtest(self):
        tr, sk = self.run_bt([(100, 100, 100, 100), (100, 101, 99.5, 100.5)])
        self.assertEqual((tr, sk.get("limit_unfilled")), ([], None))


def log_row(**kw):
    r = {c: np.nan for c in sc.LOG_COLS}
    sig = pd.to_datetime(T0 + H - 60_000, unit="ms").strftime("%Y-%m-%d %H:%M")   # candle 0 closed
    r.update(id="BTC-1h-T-x", signal_time_utc=sig, coin="BTC", tf="1h", strategy="T", direction="LONG",
             entry=99.0, stop=97.0, tp1=103.0, tp2=105.0, tp3=np.nan, max_hold_bars=6, status="OPEN",
             closed_time_utc="", version="1.0", stage="PAPER_TRADING", tp_split="0.5/0.5", state=P.AWAITING_FILL,
             planned_entry=99.0, entry_type="limit", limit_bars=2, entry_time_utc="", sim_tf="1h", bars_5m=0)
    r.update(kw)
    return r


class PaperRecord(unittest.TestCase):
    def run_rows(self, rows):
        df = frame(rows)
        log = pd.DataFrame([log_row()], columns=sc.LOG_COLS)
        for c in sc.TEXT_COLS:
            log[c] = log[c].astype(object)
        data, quality = {("BTCUSDT", "1h"): df}, {("BTC", "1h"): dict(state="GOOD", problems=[])}
        ev = []
        log = sc.resolve_limits(log, data, quality, CFG, ev, "now")
        log, closed = sc.update_forward(log, data, quality, None, CFG, {}, {}, None, {}, ev, "now")
        return log.iloc[0], ev

    def test_fill_then_managed_from_the_fill_candle(self):
        r, ev = self.run_rows([(100, 100, 100, 100), (100, 100.5, 99.5, 100), (100, 100.2, 98.9, 99.5),
                               (99.5, 103.2, 99.4, 103), (103, 105.5, 102.8, 105)])
        self.assertEqual(r["state"], P.CLOSED)
        self.assertEqual(r["entry_time_utc"], pd.to_datetime(T0 + 2 * H, unit="ms").strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(r["close_reason"], "TP2")
        self.assertEqual([(e["from_state"], e["to_state"]) for e in ev][:2],
                         [(P.AWAITING_FILL, P.TRIGGERED), (P.TRIGGERED, P.ACTIVE)])
        bt = Backtest().run_bt([(100, 100, 100, 100), (100, 100.5, 99.5, 100), (100, 100.2, 98.9, 99.5),
                                (99.5, 103.2, 99.4, 103), (103, 105.5, 102.8, 105)])[0][0]
        self.assertAlmostEqual(float(r["result_r"]), round(bt["r"], 3))    # paper record = backtest rules

    def test_expired_and_still_waiting(self):
        r, ev = self.run_rows([(100, 100, 100, 100), (100, 101, 99.5, 101), (101, 104, 100.5, 103.5)])
        self.assertEqual((r["state"], r["status"]), (P.EXPIRED, P.EXPIRED))
        self.assertTrue(pd.isna(r["result_r"]))
        self.assertIn("not filled within 2", r["state_note"])
        r, _ = self.run_rows([(100, 100, 100, 100), (100, 101, 99.5, 101)])
        self.assertEqual(r["state"], P.AWAITING_FILL)
        self.assertIn("1/2", r["state_note"])

    def test_states_and_book(self):
        P.check_move(None, P.AWAITING_FILL)
        P.check_move(P.AWAITING_FILL, P.TRIGGERED)
        P.check_move(P.AWAITING_FILL, P.EXPIRED)
        with self.assertRaises(ValueError):
            P.check_move(P.AWAITING_FILL, P.CLOSED)
        import datetime as dt
        b = P.build(pd.DataFrame([log_row(bars_5m=1)]), dt.datetime(2026, 9, 24, tzinfo=dt.timezone.utc))
        self.assertEqual([x["limit"] for x in b["limit_orders"]], [99.0])
        self.assertFalse(b["empty"])
        self.assertIn("limit 99.0000 · 1/2 candles waited", "\n".join(P.lines(b)))


class Telegram(unittest.TestCase):
    def alert(self, **kw):
        a = dict(label="LIVE", coin="SOL", inst="SOL-USDT-SWAP", d=1, tf="1h", strategy="T", version="1.0",
                 entry=99.0, R=2.0, tps=[103.0, 105.0], split=[0.5, 0.5], zone_r=0.2, max_hold=6,
                 close_ms=T0 + H - 1, sent_ms=T0 + H + 9000, limit_bars=2, regimes={}, warnings=[],
                 size=dict(qty=1.0, notional=99.0, leverage=0.1, risk_usdt=5.0, capped=False), risk_pct=0.5)
        a.update(kw)
        return a

    def test_alert_names_the_limit_and_the_cancel_time(self):
        t = lv.message(self.alert())
        self.assertIn("BUY LIMIT 99.00", t)
        self.assertIn(f"cancel at {lv.bj(T0 + 3 * H)} if not filled (2 1h candles)", t)
        self.assertIn("No fill = no trade", t)
        self.assertNotIn("(zone", t)
        self.assertIn("(zone 98.6000 – 99.4000)", lv.message(self.alert(limit_bars=None)))

    def follow(self, rows):
        t = fl.open_trade(self.alert(tf="5m"), "a", T0 + H, dict(move_stop_to_breakeven_after_tp1=True))
        bars = [dict(open_time=T0 + H + i * 300_000, open=o, high=h, low=lo, close=c) for i, (o, h, lo, c) in
                enumerate(rows)]
        return t, fl.step(t, bars)

    def test_follow_waits_for_the_fill_then_manages(self):
        t, ev = self.follow([(100, 100.5, 99.5, 100), (100, 103.5, 98.8, 103), (103, 103.5, 102.5, 103.2)])
        self.assertEqual([e["kind"] for e in ev], ["fill", "tp"])           # TP1 only after the fill candle
        self.assertIn("Limit filled", fl.text(t, ev[0]))
        t2, _ = self.follow([(100, 100.5, 99.5, 100)])
        self.assertIn("limit waiting for a fill", fl.summary(t2))

    def test_follow_expires_without_a_fill(self):
        t, ev = self.follow([(100, 100.5, 99.5, 100), (100, 101, 99.4, 100.5), (100.5, 101, 100, 100.8)])
        self.assertEqual([e["kind"] for e in ev], ["expired"])
        self.assertTrue(t["closed"])
        self.assertIn("cancel the limit order", fl.text(t, ev[0]))


class Export(unittest.TestCase):
    def test_pine_replays_limit_orders(self):
        s = SP._finish(SP.render(card(entry=LIMIT)), card(entry=LIMIT))
        ok, bad = pine.check_card(s)
        self.assertFalse(ok)
        self.assertIn("entry: limit order", bad)
        sig = pine.signals_from_trades({"BTC": [dict(entry_time=T0, dir=1, entry=99.0, R=2.0, tps=[103.0], tp1=103.0)]})
        text, info = pine.build(s, "1h", CFG, "4h", sig, "now")
        self.assertEqual(info["mode"], "REPLAY")
        self.assertIn("bool LIMIT_ENTRY = true", text)
        self.assertIn("limit = LIMIT_ENTRY ? e : na", text)
        self.assertIn("eE := array.from(99.0", text)
        self.assertEqual(pine.structure_problems(text), [])

    def test_email_plan_says_limit(self):
        e = dict(direction="LONG", entry=99.0, entry_zone=[99.0, 99.0], stop=97.0, tf="1h", limit_bars=2,
                 targets=[dict(price=103.0, r=2.0, close_pct=50)])
        rows = em.plan_table(e)[1]["rows"]
        self.assertIn("limit", rows[0][1])
        self.assertIn("cancel after 2", rows[0][2])


if __name__ == "__main__":
    unittest.main()
