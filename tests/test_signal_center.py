"""The Signal Center (Forward Test Program PR 2): 🔵 TEST alerts for program strategies positive on a coin in the
5-year backtest - the TEST list, merging, the daily cap, ⭐ agreement, the against-the-daily mark, the 5m
confirmation, the demo book, /tests, ℹ️ Details, the new alert layout, /weather in Beijing time, the hourly scan's
silent record and the safety replay. Offline: Telegram is mocked, prices are synthetic."""
import copy
import os
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import scanner as sc  # noqa: E402
from engine import confirm5m as c5m  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import positions as pos  # noqa: E402
from engine import program as PG  # noqa: E402
from engine import signal_center as SCX  # noqa: E402
from engine import weather as wx  # noqa: E402

H = 3_600_000
T0 = 1_791_158_400_000                                              # 2026-10-05 00:00 UTC = 08:00 Beijing
S = SCX.settings(None)


def coin(n=120, avg=0.3, win=45.0, test_n=30, test_avg=0.2):
    return dict(n=n, avg_r=avg, win_rate=win, test_n=test_n, test_avg_r=test_avg)


def program(**cells):
    return {"cells": {ck: dict(strategy=int(ck[1:3]), name="Breakout", version=ck.split("@")[0][-2:],
                               status="BACKTESTING", coins=c) for ck, c in cells.items()}}


class TestList(unittest.TestCase):
    def test_only_positive_coins_with_enough_trades_and_a_not_negative_test_part(self):
        p = program(**{"P01-BREAKOUT-V1@1.0|4h": dict(BTC=coin(), ETH=coin(n=12), SOL=coin(avg=-0.1),
                                                       XRP=coin(test_avg=-0.3), BNB=coin(test_n=3, test_avg=-0.5),
                                                       ADA=coin(test_n=0, test_avg=None))})
        t = SCX.test_list(p, {}, S)
        self.assertEqual(sorted(t["P01-BREAKOUT-V1@1.0|4h"]), ["ADA", "BNB", "BTC"])
        self.assertEqual(t["P01-BREAKOUT-V1@1.0|4h"]["BTC"]["score"], round(0.3 * 120 ** 0.5, 3))
        self.assertEqual(SCX.test_list(None, {}, S), {})
        self.assertEqual(SCX.test_list(p, {}, dict(S, enabled=False)), {})

    def test_status_decides(self):
        ck = "P01-BREAKOUT-V1@1.0|4h"
        p = program(**{ck: dict(BTC=coin())})
        for st, want in (("PAPER_TRADING", False), ("APPROVED", False), ("RETIRED", False), ("VALIDATION", True),
                         ("FAILED", True), ("BACKTESTING", True)):
            self.assertEqual(ck in SCX.test_list(p, {ck: dict(status=st)}, S), want, st)
        bad = {ck: dict(status="FAILED", gates_failed="LIVE results bad (-0.20R over 22 signals)")}
        self.assertEqual(SCX.test_list(p, bad, S), {})                  # the live record failed it: no more TEST


def cand(tf="4h", sid="P01-BREAKOUT-V1", score=1.0, d=1, coin_="BTC", n=1):
    return dict(label="TEST", coin=coin_, d=d, tf=tf, strategy=sid, test=dict(strategy=n, version=sid[-2:], score=score))


class Selection(unittest.TestCase):
    def test_merge_keeps_the_strongest_per_coin_direction_strategy(self):
        out = SCX.merge([cand(score=1.0), cand("1h", "P01-BREAKOUT-V2", 3.0), cand("4h", "P04-MACD-V1", 2.0, n=4),
                         cand(d=-1, score=0.5)])
        self.assertEqual([(a["strategy"], a["tf"], a["d"]) for a in out],
                         [("P01-BREAKOUT-V2", "1h", 1), ("P04-MACD-V1", "4h", 1), ("P01-BREAKOUT-V1", "4h", -1)])
        self.assertEqual(out[0]["also"], ["V1 4h"])

    def test_daily_cap_counts_beijing_days(self):
        bj_midnight = T0 + 16 * H                                         # 2026-10-06 00:00 Beijing
        self.assertEqual(SCX.sent_today([bj_midnight - 1, bj_midnight + 1], bj_midnight + 5), 1)
        keep, drop = SCX.cap([cand(score=x) for x in (1, 5, 3)], 8, dict(S, max_per_day=10))
        self.assertEqual([a["test"]["score"] for a in keep], [5, 3])
        self.assertEqual([a["test"]["score"] for a in drop], [1])

    def test_agreement_and_against_the_daily(self):
        a = cand()
        recent = [dict(coin="BTC", d=1, tf="1h", strategy="P04-MACD-V2", sent_ms=T0 - H),
                  dict(coin="BTC", d=1, tf="15m", strategy="P01-BREAKOUT-V2", sent_ms=T0 - 9 * H),   # too old
                  dict(coin="BTC", d=-1, tf="30m", strategy="P02-X", sent_ms=T0)]                    # other side
        self.assertEqual(SCX.agreement(a, recent, T0, S, others=[a, cand("30m", "P01-BREAKOUT-V2")]),
                         ["1h P04", "30m P01"])
        recs = {"1d": dict(label="WEAK_BULL"), "4h": dict(label="WEAK_BEAR"), "1h": dict(label="STRONG_BEAR")}
        self.assertEqual(SCX.against_daily(-1, recs), "1D WEAK_BULL")
        self.assertIsNone(SCX.against_daily(1, recs))
        self.assertIsNone(SCX.against_daily(-1, {}))
        self.assertTrue(SCX.market_type(recs).endswith("(1D WEAK_BULL, 4H WEAK_BEAR, 1H STRONG_BEAR)"))
        w = dict(verdict=dict(icon="🌧", title="Trend down day"), coins=[dict(coin="BTC", verdict="DOWN")])
        self.assertEqual(SCX.weather_line(w, "BTC"), "🌧 Trend down day · BTC: " + wx.COIN_WORD["DOWN"])
        self.assertIsNone(SCX.weather_line(None, "BTC"))

    def test_program_rows_hold_the_unseen_part_per_coin(self):
        rows = PG.coin_rows({"BTC": [dict(r=1.0, oos=False), dict(r=-1.0, oos=True), dict(r=2.0, oos=True)]}, 1)
        self.assertEqual((rows["BTC"]["test_n"], rows["BTC"]["test_avg_r"]), (2, 0.5))


def test_alert(**kw):
    a = dict(label="TEST", coin="BTC", inst="BTC-USDT-SWAP", d=-1, tf="1h", strategy="P01-BREAKOUT-V2",
             version="1.0", entry=100.0, R=2.0, tps=[96.0, 94.0], split=[0.5, 0.5], zone_r=0.2, max_hold=60,
             size=dict(qty=2.5, notional=250.0, leverage=0.25, risk_usdt=5.0, capped=False), risk_pct=0.5,
             regimes={"1d": "WEAK_BULL", "4h": "WEAK_BEAR"}, close_ms=T0 - 1, sent_ms=T0 + 300_000, valid_bars=2,
             warnings=[], test=dict(n=128, win_rate=46.0, avg_r=0.38, test_avg_r=0.12, score=4.3, strategy=1,
                                    version="V2"),
             program=dict(name="Breakout (Donchian + volume + ADX)", version="V2"), agree=["4h P01"],
             against="1D WEAK_BULL", weather="🌧 Trend down day · BTC: down", market="DOWN (1D WEAK_BULL, ...)",
             confirm="CONFIRMED on the 08:05 Beijing 5m bar close")
    a.update(kw)
    return a


class Layout(unittest.TestCase):
    def test_test_alert_text(self):
        t = lv.message(test_alert())
        for want in ("🔵 <b>TEST · SHORT BTC</b> · 1H ⭐", "Breakout (Donchian + volume + ADX) · V2 (P01-BREAKOUT-V2)",
                     "⭐ Same direction on: 4h P01", "Stop: <b>102.00</b> (2.00% away) · −$5.00",
                     "TP1: <b>96.00</b> (2.0R) · +$5.00 on the 50% closed", "margin $83.33 at 3x",
                     "Past: BTC won 46% of 128 backtest trades · +0.38R a trade after fees",
                     "Market: 🌧 Trend down day", "⚠️ Against the daily trend (1D WEAK_BULL) - context only",
                     "5m check: ✓ CONFIRMED", "🔵 TEST = a setup of a strategy", "Candle closed 08:00 Beijing"):
            self.assertIn(want, t)
        self.assertNotIn("fee", t.split("Past")[0].lower())                   # no fee line in the alert
        b = lv.choice_buttons("a1")["inline_keyboard"]
        self.assertEqual([x["text"] for x in b[0]], ["✅ Took it", "❌ Skip"])
        self.assertEqual(b[-1][0]["callback_data"], "info|a1")

    def test_details(self):
        cards, _, _, _ = sc.load_cards()
        card = next(c for c in cards if c["id"] == "P01-BREAKOUT-V2")
        t = lv.details_text(test_alert(), card)
        for want in ("ℹ️ <b>Breakout (Donchian + volume + ADX)</b> · V2", "Rules (short", "close &lt; prev(lowest(low,20))",
                     "4H and 1H trend the same way", "Why it can work", "When it fails",
                     "Backtest on BTC</b> (5 years, after fees): 128 trades, 46% won, +0.38R a trade, unseen last part "
                     "+0.12R", "promotes a strategy to 🟡 PAPER only"):
            self.assertIn(want, t)
        self.assertIn("P01-BREAKOUT-V2", lv.details_text(test_alert(), None))

    def test_weather_in_beijing_time(self):
        self.assertEqual(wx.beijing("2026-10-08 08:00"), "10-08 16:00 Beijing")
        self.assertEqual(wx.beijing("soon"), "soon UTC")


class Watcher(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        patches = [mock.patch.object(LW, "STATE", os.path.join(self.tmp.name, "state.json")),
                   mock.patch.object(LW, "JOURNAL", os.path.join(self.tmp.name, "journal", "my_trades.csv")),
                   mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "1:x", "TELEGRAM_CHAT_ID": "42"}),
                   mock.patch.object(LW, "log")]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.hour = (int(__import__("time").time() * 1000) // (4 * H)) * 4 * H
        self.now = self.hour + 8000
        self.w = LW.Watcher(LW.SyntheticSwap(), send=True, git=False, now_fn=lambda: self.now)
        self.w.coins, self.w.extra = ["BTC"], []
        self.v1, self.v2 = self.w.cards["P01-BREAKOUT-V1@1.0"], self.w.cards["P01-BREAKOUT-V2@1.0"]
        self.w.tests = {"P01-BREAKOUT-V1@1.0|4h": {"BTC": dict(coin(), score=3.3, strategy=1, version="V1")},
                        "P01-BREAKOUT-V2@1.0|1h": {"BTC": dict(coin(), score=5.0, strategy=1, version="V2")}}
        self.w.watch = [(self.v1, "4h", "TEST"), (self.v2, "1h", "TEST")]
        self.sent, self.api = [], []
        p1 = mock.patch.object(LW, "telegram_message",
                               side_effect=lambda text, *a, **k: self.sent.append((text, k.get("buttons"))) or (True, "", 77))
        p2 = mock.patch.object(LW, "tg_api", side_effect=lambda m, p, *a, **k: self.api.append((m, p)) or (True, {}))
        for p in (p1, p2):
            p.start()
            self.addCleanup(p.stop)

    def fire(self, d=-1):
        def fake(s, tf, fr, cfg, gc=None, detail=None):
            n = fr["n"]
            L, S_ = np.zeros(n, bool), np.zeros(n, bool)
            (L if d == 1 else S_)[n - 1] = True
            return L, S_, None, None, {c: sc.level_array(c, fr["ns"], n) for c in LW.sspec.columns_needed(s)}
        return mock.patch.object(sc, "strategy_signals", fake)

    def confirmed(self):
        return mock.patch.object(c5m, "check", side_effect=lambda m5, after, d, e, st, S=None: dict(
            state=c5m.CONFIRMED, idx=c5m.first_bar(m5, after), bars=1, why="ok", smc=[]))

    def test_trigger_waits_for_5m_then_one_merged_alert(self):
        with self.fire():
            self.assertEqual(self.w.tick(self.now), [])                     # 4H + 1H fired: waiting for the 5m bar
        self.assertEqual(len(self.w.pending), 1)                            # merged: one per coin + side + strategy
        p = self.w.pending[0]
        self.assertEqual((p["strategy"], p["tf"]), ("P01-BREAKOUT-V2", "1h"))  # the stronger backtest evidence
        self.assertEqual(p["agree"], ["4h P01"])
        with self.fire(), self.confirmed():
            self.now += 300_000
            a = self.w.tick(self.now)
        self.assertEqual(len(a), 1)
        self.assertEqual((a[0]["label"], a[0]["d"]), ("TEST", -1))
        self.assertIn("5m bar close", a[0]["confirm"])
        self.assertIn("🔵 <b>TEST · SHORT BTC</b>", self.sent[-1][0])
        self.assertIn("Past: BTC won 45%", self.sent[-1][0])
        self.assertEqual(self.w.state["test_sent"], [self.now])
        with self.fire():                                                   # the TEST cooldown: no repeat
            self.now += 300_000
            self.assertEqual(self.w.tick(self.now), [])
        self.assertEqual(self.w.pending, [])

    def test_watch_note_at_once_while_the_5m_check_waits(self):          # 👀 2026-10-10
        with self.fire():
            self.assertEqual(self.w.tick(self.now), [])
        notes = [(t, b) for t, b in self.sent if "<b>Watch ·" in t]
        self.assertEqual(len(notes), 1)                                     # merged setup: one note
        text, buttons = notes[0]
        self.assertIn("<b>Watch · SHORT BTC</b> · 1H", text)
        self.assertIn("Waiting up to 30 min for a 5m candle", text)
        self.assertIn("Information only - not a trade signal", text)
        self.assertIsNone(buttons)                                          # never buttons: not a signal
        self.assertEqual(len(self.w.pending), 1)
        self.assertEqual(self.w.state["watch_sent"], [self.now])
        self.assertIn("Watch notes: ON · 1 sent today", self.w.status_text(self.now))

    def test_watch_off_cap_and_pause(self):
        msg = lambda t: dict(update_id=1, message=dict(chat=dict(id=42), date=self.now // 1000, text=t))  # noqa: E731
        self.w.on_update(msg("/watch off"), self.now)
        self.assertIn("Watch notes are <b>OFF</b>", self.sent[-1][0])
        with self.fire():
            self.w.tick(self.now)
        self.assertFalse(any("<b>Watch ·" in t for t, _ in self.sent))
        self.assertEqual(len(self.w.pending), 1)                            # the TEST setup itself still waits
        self.w.on_update(msg("/watch on"), self.now)
        self.assertIn("<b>ON</b>", self.sent[-1][0])
        a = dict(self.w.pending[0])
        self.w.SC = dict(self.w.SC, watch_max_per_day=1)
        self.w.state["watch_sent"] = [self.now]
        self.assertFalse(self.w.watch_note(a, self.now))                   # the daily maximum
        self.w.state["watch_sent"] = []
        self.w.state["paused_until"] = -1
        self.assertFalse(self.w.watch_note(a, self.now))                   # /pause holds them too
        self.w.state["paused_until"] = 0
        self.assertTrue(self.w.watch_note(a, self.now))

    def test_failed_5m_check_releases_the_setup(self):
        with self.fire():
            self.w.tick(self.now)
        key = self.w.pending[0]["key"]
        with mock.patch.object(c5m, "check", return_value=dict(state=c5m.EXPIRED, idx=None, bars=6, why="no", smc=[])):
            self.now += 300_000
            self.w.tick(self.now)
        self.assertNotIn(key, self.w.state["sent"])

    def test_tests_off_cap_and_only_positive_coins(self):
        self.w.on_update(dict(update_id=1, message=dict(chat=dict(id=42), date=self.now // 1000, text="/tests off")),
                         self.now)
        self.assertIn("OFF", self.sent[-1][0])
        with self.fire():
            self.assertEqual(self.w.tick(self.now), [])
        self.assertEqual(self.w.pending, [])
        self.w.state["tests_on"] = True
        self.w.tests = {"P01-BREAKOUT-V1@1.0|4h": {"ETH": dict(coin(), score=3.3, strategy=1, version="V1")}}
        with self.fire():
            self.w.tick(self.now)
        self.assertEqual(self.w.pending, [])                               # BTC was not positive for this cell
        self.w.SC = dict(self.w.SC, max_per_day=1)
        self.w.state["test_sent"] = [self.now]
        self.w.deliver([dict(test_alert(), sent_ms=self.now)], self.now)
        self.assertEqual(self.sent[-1][0].split("\n")[0][:20], "🔵 TEST alerts are <b"[:20])   # nothing new sent

    def test_details_button_and_demo_book(self):
        self.w.deliver([dict(test_alert(strategy="P01-BREAKOUT-V2"), sent_ms=self.now)], self.now)
        buttons = self.sent[-1][1]["inline_keyboard"]
        aid = buttons[0][0]["callback_data"].split("|")[1]
        press = lambda data: dict(update_id=2, callback_query=dict(id="q", data=data,
                                                                   message=dict(chat=dict(id=42), message_id=77)))
        self.w.on_update(press(f"info|{aid}"), self.now)
        self.assertIn("Rules (short", self.sent[-1][0])
        self.w.on_update(press(f"took|{aid}"), self.now)
        self.assertIn("🔵 Demo book", self.sent[-1][0])
        self.assertEqual(self.w.state["trades"][aid]["label"], "TEST")
        self.assertEqual(self.w.pb_journal(self.now)[0], 0)                # never counted in the loss limits
        self.w.state["results"].append(dict(id=aid, coin="BTC", d=-1, tf="1h", label="TEST", strategy="P01",
                                            r=-1.0, how="finished", ended_ms=self.now))
        self.assertEqual(self.w.pb_journal(self.now)[1], 0)
        txt = self.w.trades_text(self.now)
        self.assertIn("🔵 Demo book (TEST trades", txt)
        self.assertIn("Demo book, last 30 days: 1 finished", txt)
        st = self.w.status_text(self.now)
        self.assertIn("🔵 TEST alerts: ON", st)


class Reload(unittest.TestCase):
    def test_program_file_adds_test_cells_not_already_alerting(self):
        prog = program(**{"P01-BREAKOUT-V1@1.0|4h": dict(BTC=coin()), "P07-SQUEEZE-RETEST-V2@1.0|1h": dict(ETH=coin())})
        with tempfile.TemporaryDirectory() as d, mock.patch.object(LW, "STATE", os.path.join(d, "s.json")), \
                mock.patch.object(LW, "log"), \
                mock.patch.object(LW.Watcher, "_json", side_effect=lambda rel: prog if rel.endswith("program.json") else None):
            w = LW.Watcher(LW.SyntheticSwap(), send=False, git=False)
        tests = sorted((s["id"], tf) for s, tf, lab in w.watch if lab == "TEST")
        self.assertEqual(tests, [("P01-BREAKOUT-V1", "4h"), ("P07-SQUEEZE-RETEST-V2", "1h")])
        self.assertIn(("main", "reports/program.json"), LW.SYNC_FILES)
        self.assertIn("engine/signal_center.py", LW.CODE_FILES)


class GitHubRecord(unittest.TestCase):
    def test_scan_records_test_pairs_as_stage_test(self):
        tests = {"P01-BREAKOUT-V1@1.0|4h": {"BTC": dict(n=100)}}
        self.assertEqual(SCX.scan_stage("PAPER_TRADING", tests, "P01-BREAKOUT-V1@1.0|4h", "BTC"), ("PAPER_TRADING", None))
        self.assertEqual(SCX.scan_stage("VALIDATION", {}, "X@1.0|4h", "BTC"), ("VALIDATION", None))
        self.assertEqual(SCX.scan_stage("BACKTESTING", tests, "P01-BREAKOUT-V1@1.0|4h", "BTC"), ("TEST", dict(n=100)))
        self.assertEqual(SCX.scan_stage("FAILED", tests, "P01-BREAKOUT-V1@1.0|4h", "ETH"), (None, None))
        self.assertEqual(SCX.scan_stage("BACKTESTING", tests, "P01-BREAKOUT-V1@1.0|1h", "BTC"), (None, None))

    def test_test_rows_are_not_positions_or_paper(self):
        row = dict(id="x", coin="BTC", direction="SHORT", tf="1h", strategy="P01", version="1.0", stage="TEST",
                   state=pos.ACTIVE, status="OPEN", entry=100.0, stop=102.0, tp1=96.0, signal_time_utc="2026-10-05 00:00",
                   entry_time_utc="2026-10-05 00:00", sim_tf="1h", current_stop=102.0, result_r=np.nan)
        b = pos.build(pd.DataFrame([row]), pd.Timestamp("2026-10-05 02:00", tz="UTC").to_pydatetime())
        self.assertFalse(any(b.get(k) for k in ("active", "paper", "awaiting", "closed", "limit_orders")))
        self.assertIn("market_type", sc.LOG_COLS)
        self.assertIn("market_type", sc.TEXT_COLS)


class Replay(unittest.TestCase):
    def test_rules_in_time_order_cooldown_cap_and_results(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(LW, "STATE", os.path.join(d, "s.json")), \
                mock.patch.object(LW, "log"):
            w = LW.Watcher(LW.SyntheticSwap(), send=False, git=False)
        w.coins = ["BTC"]
        w.SC = dict(w.SC, max_per_day=2)
        v2 = w.cards["P01-BREAKOUT-V2@1.0"]
        w.tests = {"P01-BREAKOUT-V2@1.0|1h": {"BTC": dict(coin(), score=5.0, strategy=1, version="V2")}}
        w.watch = [(v2, "1h", "TEST")]

        def fake(s, tf, fr, cfg, gc=None, detail=None):                    # a short every 3rd 1h candle
            n = fr["n"]
            S_ = np.zeros(n, bool)
            S_[np.arange(n) % 3 == 0] = True
            return np.zeros(n, bool), S_, None, None, {}
        with mock.patch.object(sc, "strategy_signals", fake), \
                mock.patch.object(c5m, "check", side_effect=lambda m5, after, *a, **k: dict(
                    state=c5m.CONFIRMED, idx=c5m.first_bar(m5, after), bars=1, why="ok", smc=[])):
            rep = LW.replay(w, 3)
        al = rep["alerts"]
        self.assertTrue(al)
        times = [a["sent_ms"] for a in al]
        self.assertEqual(times, sorted(times))
        self.assertTrue(all(b - a >= w.SC["cooldown_minutes"] * 60_000 - 300_000 for a, b in zip(times, times[1:])))
        self.assertLessEqual(rep["summary"]["max_day"], 2)
        self.assertGreater(rep["summary"]["capped"], 0)
        self.assertIn("Replay of the last 3 days", LW.replay_text(rep))


if __name__ == "__main__":
    unittest.main()
