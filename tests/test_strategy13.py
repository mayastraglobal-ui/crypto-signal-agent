"""Strategy 13 (operator request 2026-10-27: "build strategy 13"): the daily Turtle, long only - buy a close above the
55-day high, exit at a close below the 20-day low, no fixed target. The cards (V1-V3 + control on 4H with day-sized
windows), the btc_close building block (BTC above its 200-day average), one trade per coin at a time in the live
watcher and the hourly record (backtest_takes: as the backtest), the market entry that skips the TEST pullback, the
longer 4H history, and the follow-up that tells the exit line and the trend exit."""
import os
import sys
import unittest

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import scanner as sc  # noqa: E402
from engine import follow as fl  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import program as PG  # noqa: E402
from engine import regime as RG  # noqa: E402
from engine import signal_center as SCX  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
H4, M5 = 4 * 3_600_000, 300_000


def candles(close, step=H4, spread=0.001):
    close = np.asarray(close, dtype=float)
    ot = np.arange(len(close), dtype=np.int64) * step
    return pd.DataFrame(dict(open_time=ot, open=close, high=close * (1 + spread), low=close * (1 - spread),
                             close=close, volume=np.ones(len(close)), close_time=ot + step - 1))


def program_cards():
    with open(os.path.join(ROOT, "strategies_program.yaml")) as f:
        prog = yaml.safe_load(f)
    ok, problems, _, _ = SP.load_library([], [], RG.LABELS, ["4h", "1h", "30m", "15m"], prog)
    return {c["id"]: c for c in ok if c["id"].startswith("P13")}, [p for p in problems if "P13" in str(p)]


def breakout_card(**kw):
    c = dict(id="T13", version="1.0", long=["close > prev(highest(high,20))"], short=["close < 0"],
             exit_long=["close < prev(lowest(low,10))"], exit_short=[], stop=dict(method="atr", atr=5.0),
             targets=dict(long=["40R"], short=["40R"], split=[1.0]), time_stop_bars=1200, cooldown_bars=0,
             one_trade=True)
    c.update(kw)
    return c


def run(card, close):
    df = candles(close)
    df["_atr"] = np.full(len(df), 1.0)
    ns = sc.make_namespace(df)
    L = sc.eval_rules(card["long"], ns, df.index)
    S = sc.eval_rules(card["short"], ns, df.index)
    XL = sc.eval_rules(card["exit_long"], ns, df.index)
    oo = []
    tr = sc.backtest(df, L, S, XL, None, card, CFG, "4h", {}, None, oo)
    return df, L, tr, oo


class Cards(unittest.TestCase):
    def test_four_cards_load(self):
        cards, problems = program_cards()
        self.assertEqual(problems, [])
        self.assertEqual(sorted(cards), ["P13-TURTLE-C", "P13-TURTLE-V1", "P13-TURTLE-V2", "P13-TURTLE-V3"])
        self.assertEqual({PG.number(c) for c in cards.values()}, {13})
        for c in cards.values():
            self.assertEqual(c["timeframes"], ["4h"])
            self.assertEqual(c["short"], ["close < 0"])             # long only: a price is never below zero
            self.assertEqual(c["long"][0], "close > prev(highest(high,330))")     # 55 days of 4H candles
            self.assertTrue(c["one_trade"])
            self.assertEqual(c["entry"], {"type": "market"})
            self.assertEqual(c["stop"], {"method": "atr", "atr": 5.0})          # ~2 daily ATR
            self.assertIsNone(SCX.pullback_entry(c, "4h", SCX.settings(None)))  # no 🎯 pullback wait
        v1 = cards["P13-TURTLE-V1"]
        self.assertEqual(v1["exit_long"], ["close < prev(lowest(low,120))"])  # 20 days
        self.assertEqual(v1["targets"]["long"], ["40R"])
        self.assertEqual(v1["control_twin"], "P13-TURTLE-C")
        self.assertEqual(fl.channel_exit(v1, 1), 120)
        self.assertEqual(cards["P13-TURTLE-V2"]["long"][-1], "btc_close > sma(btc_close,1200)")
        self.assertEqual(cards["P13-TURTLE-V3"]["long"][-1], "close > sma(close,1200)")
        c = cards["P13-TURTLE-C"]
        self.assertEqual((c["exit_long"], c["time_stop_bars"], c["targets"]["long"]), ([], 30, ["2R", "3R"]))
        self.assertIsNone(fl.channel_exit(c, 1))

    def test_the_control_never_alerts(self):
        row = dict(n=40, avg_r=0.3, win_rate=50, test_n=10, test_avg_r=0.2)
        p = dict(cells={"P13-TURTLE-C@1.0|4h": dict(strategy=13, version="C", status="BACKTESTING", avg_r=0.3,
                                                    coins={"SOL": row}),
                        "P13-TURTLE-V1@1.0|4h": dict(strategy=13, version="V1", status="BACKTESTING", avg_r=0.3,
                                                     coins={"SOL": row})})
        self.assertEqual(list(SCX.test_list(p, {}, SCX.settings(None))), ["P13-TURTLE-V1@1.0|4h"])

    def test_a_control_that_passes_never_alerts_or_emails(self):
        cards, _ = program_cards()
        c = cards["P13-TURTLE-C"]
        self.assertEqual(sc.lab_status(c, "PAPER_TRADING"), "VALIDATION")       # recorded silently
        self.assertIsNone(lv.alert_label(sc.lab_status(c, "PAPER_TRADING"), c.get("lab"),
                                         lv.settings(CFG.get("live_watcher"))))
        v1 = cards["P13-TURTLE-V1"]
        self.assertEqual(lv.alert_label(sc.lab_status(v1, "PAPER_TRADING"), v1.get("lab"),
                                        lv.settings(CFG.get("live_watcher"))), "PAPER")
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn("st = sc.lab_status(s, (reg[\"cells\"].get(", src)

    def test_other_cards_keep_the_pullback(self):
        S = SCX.settings(None)
        self.assertIsNotNone(SCX.pullback_entry(dict(id="x"), "4h", S))
        self.assertIsNone(SCX.pullback_entry(dict(id="x", entry=dict(type="limit", valid_bars=3)), "4h", S))

    def test_a_limit_level_may_use_params(self):
        card = dict(params=dict(n=330), entry=dict(type="limit", long_level="prev(highest(high,{n}))",
                                                   short_level="close", valid_bars=12))
        self.assertIn("n", SP.placeholders(card))
        self.assertEqual(SP.render(card)["entry"]["long_level"], "prev(highest(high,330))")


class BtcClose(unittest.TestCase):
    def test_the_block_is_btc_on_the_same_candle(self):
        coin, btc = candles(np.linspace(10, 20, 50)), candles(np.linspace(100, 50, 50))
        df = sc.attach_market(coin.copy(), None, btc, "SOL")
        ns = sc.make_namespace(df)
        self.assertTrue(np.allclose(ns["btc_close"].to_numpy(), btc["close"].to_numpy()))
        below = sc.eval_rules(["btc_close > sma(btc_close,10)"], ns, df.index)
        self.assertFalse(below.any())                         # BTC falling: below its average all along

    def test_the_card_checker_knows_the_block(self):
        self.assertIn("btc_close", SP.COLUMNS)
        self.assertIn("btc_close", SP.LEAD_BLOCKS)
        self.assertEqual(SP.expr_problems("btc_close > sma(btc_close,1200)", ["4h"]), [])
        card = dict(breakout_card(one_trade="yes"), status="FORMALIZED", family="breakout", gate="trend",
                    hypothesis="h", source="s", regimes=["RANGE"], timeframes=["4h"], known_weaknesses="w")
        self.assertIn("one_trade must be true or false", SP.check(card, RG.LABELS, ["4h"]))
        self.assertNotIn("one_trade must be true or false", SP.check(dict(card, one_trade=True), RG.LABELS, ["4h"]))


class OneTrade(unittest.TestCase):
    # flat at 100, a breakout, a rally with a new high on every candle
    UP = [100.0] * 40 + list(np.linspace(101, 130, 30))

    def test_a_rally_is_one_trade(self):
        card = breakout_card()
        df, L, tr, oo = run(card, self.UP)
        n = len(df)
        self.assertGreater(L[40:].sum(), 20)                  # the breakout rule is true on every new high
        self.assertEqual(tr, [])
        self.assertEqual(oo[0]["signal_idx"], 40)             # the first break is the open trade
        self.assertTrue(sc.backtest_takes(card, tr, oo, 40, n))
        self.assertFalse(sc.backtest_takes(card, tr, oo, n - 1, n))      # a later high: no new alert
        self.assertTrue(sc.backtest_takes(dict(card, one_trade=False), tr, oo, n - 1, n))   # other cards: as before

    def test_a_new_break_after_the_exit_is_a_new_trade(self):
        card = breakout_card()
        close = self.UP + list(np.linspace(129, 95, 12)) + [95.0] * 20 + [140.0]
        df, L, tr, oo = run(card, close)
        n = len(df)
        self.assertEqual(len(tr), 1)
        self.assertEqual(tr[0]["reason"], "exit-rule")        # the close below the 10-candle low
        self.assertEqual(oo, [])
        self.assertTrue(L[n - 1])
        self.assertTrue(sc.backtest_takes(card, tr, oo, n - 1, n))

    def test_the_scan_and_the_watcher_ask_the_backtest(self):
        scan = open(os.path.join(ROOT, "scanner.py"), encoding="utf-8").read()
        self.assertIn("if d == 0 or not backtest_takes(s, tr, open_now, t_i, n):", scan)
        watch = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn("if not sc.backtest_takes(s, tr, open_now, t, fr[\"n\"]):", watch)


class History(unittest.TestCase):
    def test_4h_history_holds_the_200_day_average_and_a_trade(self):
        self.assertGreaterEqual(int(CFG["timeframes"]["4h"]), 1200 + 1200)
        S = lv.settings(CFG.get("live_watcher"))
        self.assertGreaterEqual(S["bars_tf"]["4h"], 1200 + 1200)
        self.assertEqual(S["bars"], 500)                      # the other timeframes as before
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn('int((self.S.get("bars_tf") or {}).get(tf, self.S["bars"]))', src)

    def test_a_long_plan_record_is_kept_until_its_max_hold(self):
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn('int(t.get("end_ms") or 0) - int(t["taken_ms"]) + 86_400_000', src)
        self.assertEqual(lv.hold_text("4h", 1200), "1200 candles (~200 days)")
        self.assertEqual(lv.hold_text("1h", 2), "2 candles (~2h00m)")


def alert(**kw):
    a = dict(label="TEST", coin="BTC", inst="BTC-USDT-SWAP", d=1, tf="4h", strategy="P13-TURTLE-V1", version="1.0",
             entry=100.0, R=5.0, tps=[300.0], split=[1.0], zone_r=0.2, max_hold=1200, regimes={}, close_ms=H4 * 400 - 1,
             sent_ms=H4 * 400, valid_bars=2, chan_n=120, chan_line=90.0)
    a.update(kw)
    return a


class FollowUp(unittest.TestCase):
    def test_the_alert_shows_the_trend_exit_not_the_far_target(self):
        text = lv.message(alert())
        self.assertIn("Target: none - ride the trend", text)
        self.assertIn("Exit: a 4H close below the lowest low of the last 20 days (now <b>90.00</b>)", text)
        self.assertNotIn("TP1", text)
        self.assertIn("TP1:", lv.message(alert(chan_n=None)))

    def test_channel_rule_only(self):
        self.assertEqual(fl.channel_exit(dict(exit_long=["close < prev(lowest(low,120))"]), 1), 120)
        self.assertEqual(fl.channel_exit(dict(exit_short=["close > prev(highest(high,10))"]), -1), 10)
        self.assertIsNone(fl.channel_exit(dict(exit_long=["close < prev(lowest(low,10))", "rsi(close,14) < 30"]), 1))
        self.assertIsNone(fl.channel_exit(dict(exit_long=["close < ema(close,20)"]), 1))

    def test_the_line_is_told_above_the_stop_and_the_exit_closes(self):
        t = fl.open_trade(alert(), "a1", H4 * 400)
        bar = lambda i, c, **k: dict(open_time=H4 * 400 + i * M5, open=c, high=c + 0.1, low=c - 0.1, close=c, **k)  # noqa
        ev = fl.step(t, [bar(0, 101, chan_line=90.0)])         # below the stop (95): the stop protects, no message
        self.assertEqual(ev, [])
        ev = fl.step(t, [bar(1, 110, chan_line=97.0)])
        self.assertEqual([(e["kind"], e["px"]) for e in ev], [("line", 97.0)])
        self.assertEqual(fl.step(t, [bar(2, 111, chan_line=97.5)]), [])       # +0.1R: not worth a message
        ev = fl.step(t, [bar(3, 112, chan_line=99.0)])
        self.assertEqual([e["kind"] for e in ev], ["line"])
        self.assertIn("Exit line moved", fl.text(t, ev[0]))
        self.assertIn("exit line 99.00", fl.summary(t))
        ev = fl.step(t, [bar(4, 104, chan_line=99.0, chan_exit=True)])
        self.assertEqual(ev[0]["kind"], "channel")
        self.assertAlmostEqual(ev[0]["result_r"], 0.8)
        self.assertTrue(t["closed"])
        self.assertIn("Trend exit", fl.text(t, ev[0]))
        self.assertIn("20-day low", fl.text(t, ev[0]))

    def test_channel_on_5m_flags_only_the_closing_candle(self):
        c4 = [100.0] * 12 + [90.0]                            # the 13th 4H candle closes below the 10-candle low
        card = candles(c4)
        m5 = candles(np.full(13 * 48, 100.0), step=M5)
        m5 = candles(np.full(14 * 48, 100.0), step=M5)
        out = LW.channel_on_5m(m5, card, 10, 1)
        hits = np.nonzero(out["chan_exit"])[0]
        self.assertEqual(hits[0], 13 * 48 - 1)                # from the 5m candle closing that 4H candle ...
        self.assertEqual(len(hits), 48 + 1)                   # ... on: a 4H candle that comes in late still exits
        self.assertTrue(np.isnan(out["chan_line"][:9 * 48 - 1]).all())     # fewer than 10 closed 4H candles
        self.assertAlmostEqual(out["chan_line"][12 * 48], 99.9)
        self.assertFalse(LW.channel_on_5m(m5, card.iloc[:5], 10, 1)["chan_exit"].any())
        late = LW.channel_on_5m(m5, card, 10, 1, from_ms=13 * H4)     # the trade began after that candle
        self.assertFalse(late["chan_exit"].any())


if __name__ == "__main__":
    unittest.main()
