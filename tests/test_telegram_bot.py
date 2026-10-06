"""Telegram commands, alert buttons and the trade follow-up (roadmap step 4, operator request 2026-10-06).
Offline: Telegram is mocked, prices are made up."""
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
from engine import follow as fl  # noqa: E402
from engine import live as lv  # noqa: E402

M5 = 300_000
T0 = 1_791_158_400_000                                              # 2026-10-05 00:00 UTC
TP_CFG = dict(move_stop_to_breakeven_after_tp1=True, move_stop_to_tp1_after_tp2=True)


def alert(d=1, entry=100.0, R=1.0, tps=(102.0, 103.0), split=(0.5, 0.5), tf="5m", max_hold=12, label="PAPER"):
    return dict(label=label, coin="SOL", inst="SOL-USDT-SWAP", d=d, tf=tf, strategy="S", version="1.0", entry=entry,
                R=R, tps=list(tps), split=list(split), max_hold=max_hold, close_ms=T0 - 1, sent_ms=T0 + 9000)


def bars(rows, start=T0):
    """rows = [(open, high, low, close)] -> 5m candles from start."""
    return [dict(open_time=start + i * M5, open=o, high=h, low=lo, close=c, close_time=start + (i + 1) * M5 - 1)
            for i, (o, h, lo, c) in enumerate(rows)]


class Follow(unittest.TestCase):
    def test_tp1_moves_the_stop_to_entry_then_stopped_at_entry(self):
        t = fl.open_trade(alert(), "a1", T0, TP_CFG)
        ev = fl.step(t, bars([(100, 101, 99.5, 100.5), (100.5, 102.2, 100.4, 101.5), (101.5, 101.6, 99.9, 100.2)]))
        self.assertEqual([e["kind"] for e in ev], ["tp", "stop"])
        self.assertEqual(ev[0]["stop"], 100.0)                                 # break-even after TP1
        self.assertAlmostEqual(ev[1]["result_r"], 0.5 * 2.0)                   # half closed at 2R, rest at entry
        self.assertTrue(t["closed"])
        self.assertIn("Move the stop-loss to <b>entry 100.00</b>", fl.text(t, ev[0]))
        self.assertIn("Stopped at entry", fl.text(t, ev[1]))
        self.assertIn("+1.0R", fl.text(t, ev[1]))

    def test_stop_first_when_stop_and_target_touch_in_one_candle(self):
        t = fl.open_trade(alert(d=-1, tps=(98.0, 97.0)), "a1", T0, TP_CFG)
        ev = fl.step(t, bars([(100, 101.5, 97.5, 99)]))                        # both the stop and TP1 touched
        self.assertEqual([e["kind"] for e in ev], ["stop"])
        self.assertAlmostEqual(ev[0]["result_r"], -1.0)
        self.assertIn("Stop-loss hit", fl.text(t, ev[0]))

    def test_time_stop_and_candles_are_never_counted_twice(self):
        t = fl.open_trade(alert(max_hold=3), "a1", T0, TP_CFG)
        b = bars([(100, 100.5, 99.5, 100.2)] * 3)
        self.assertEqual(fl.step(t, b[:2]), [])
        self.assertEqual(fl.step(t, b[:2]), [])                                # same candles again: nothing new
        ev = fl.step(t, b)
        self.assertEqual([e["kind"] for e in ev], ["time"])
        self.assertAlmostEqual(ev[0]["result_r"], 0.2)
        self.assertIn("Time stop", fl.text(t, ev[0]))

    def test_follows_from_when_the_operator_took_it(self):
        t = fl.open_trade(alert(), "a1", T0 + 2 * M5 + 60_000, TP_CFG)          # pressed during the 3rd candle
        ev = fl.step(t, bars([(100, 100, 98, 99)] + [(100, 100.5, 99.5, 100)] * 3))   # the stop before: not counted
        self.assertEqual(ev, [])

    def test_same_result_as_the_backtest_rules(self):
        """The follow-up must manage a trade exactly like scanner.simulate_trade (costs set to 0)."""
        cfg = copy.deepcopy(sc.load_config() if hasattr(sc, "load_config") else LW.yaml.safe_load(
            open(os.path.join(ROOT, "config.yaml"))))
        for side in ("long", "short"):
            cfg["costs"][side].update(taker_fee_pct=0, maker_fee_pct=0, slippage_pct=0, funding_pct_per_8h=0)
        cfg["costs"]["short"]["funding_real_x"] = 1.0
        rng = np.random.default_rng(3)
        checked = 0
        for k in range(300):
            d = 1 if k % 2 else -1
            c = 100 * np.exp(np.cumsum(rng.normal(0, 0.004, 60)))
            o = np.r_[100.0, c[:-1]]
            h = np.maximum(o, c) * (1 + rng.uniform(0, 0.003, 60))
            lo = np.minimum(o, c) * (1 - rng.uniform(0, 0.003, 60))
            R, entry = 0.6, 100.0
            tps = [entry + d * r * R for r in (1.0, 2.0, 3.0)]
            sim = sc.simulate_trade(o, h, lo, c, 0, d, entry, R, cfg, 40, 1 / 12, tps=tps, split=[0.4, 0.3, 0.3])
            t = fl.open_trade(alert(d=d, R=R, tps=tps, split=(0.4, 0.3, 0.3), max_hold=40), "x", T0, TP_CFG)
            ev = fl.step(t, bars(list(zip(o, h, lo, c))))
            if sim is None:
                self.assertFalse(t["closed"])
                continue
            checked += 1
            self.assertTrue(t["closed"])
            self.assertAlmostEqual(ev[-1]["result_r"], sim["r"], places=9)
            self.assertEqual(ev[-1]["at_ms"], T0 + (sim["exit_idx"] + 1) * M5)
        self.assertGreater(checked, 200)


class Helpers(unittest.TestCase):
    def test_commands_and_durations(self):
        self.assertEqual(lv.parse_command("/Pause@my_bot 2h"), ("pause", "2h"))
        self.assertEqual(lv.parse_command("/status"), ("status", ""))
        self.assertEqual(lv.parse_command("hello"), (None, "hello"))
        self.assertIsNone(lv.parse_duration(""))
        self.assertEqual(lv.parse_duration("2"), 2 * 3_600_000)
        self.assertEqual(lv.parse_duration("90m"), 90 * 60_000)
        for bad in ("abc", "-1", "9d", "200h"):
            with self.assertRaises(ValueError):
                lv.parse_duration(bad)

    def test_buttons(self):
        first = lv.choice_buttons("a1")["inline_keyboard"]
        self.assertEqual([b["callback_data"] for b in first[0]], ["took|a1", "skip|a1"])
        took = lv.choice_buttons("a1", "took")["inline_keyboard"]
        self.assertIn("✓", took[0][0]["text"])
        self.assertEqual(took[1][0]["callback_data"], "closed|a1")
        self.assertEqual(len(lv.choice_buttons("a1", "done")["inline_keyboard"][0]), 1)
        for row in took:
            for b in row:
                self.assertLessEqual(len(b["callback_data"].encode()), 64)      # Telegram's limit


class Bot(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        patches = [mock.patch.object(LW, "STATE", os.path.join(self.tmp.name, "state.json")),
                   mock.patch.object(LW, "JOURNAL", os.path.join(self.tmp.name, "journal", "my_trades.csv")),
                   mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "1:x", "TELEGRAM_CHAT_ID": "42"}),
                   mock.patch.object(LW, "log")]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.now = T0 + 9000
        self.w = LW.Watcher(LW.SyntheticSwap(), send=True, git=False, now_fn=lambda: self.now)
        self.sent, self.api = [], []
        p1 = mock.patch.object(LW, "telegram_message",
                               side_effect=lambda text, *a, **k: self.sent.append((text, k.get("buttons"))) or (True, "", 77))
        p2 = mock.patch.object(LW, "tg_api", side_effect=lambda method, payload, *a, **k: self.api.append(
            (method, payload)) or (True, {}))
        for p in (p1, p2):
            p.start()
            self.addCleanup(p.stop)

    def tearDown(self):
        self.tmp.cleanup()

    def msg(self, text, chat=42, age_s=0):
        return dict(update_id=1, message=dict(chat=dict(id=chat), date=(self.now // 1000) - age_s, text=text))

    def press(self, data):
        return dict(update_id=2, callback_query=dict(id="q", data=data, message=dict(chat=dict(id=42), message_id=77)))

    def test_status_help_and_unknown(self):
        self.w.on_update(self.msg("/status"), self.now)
        self.assertIn("Live watcher running", self.sent[-1][0])
        self.assertIn("Watching", self.sent[-1][0])
        self.w.on_update(self.msg("/help"), self.now)
        self.assertIn("/pause", self.sent[-1][0])
        self.w.on_update(self.msg("/nonsense"), self.now)
        self.assertIn("/help", self.sent[-1][0])

    def test_only_the_operators_chat_and_no_old_messages(self):
        self.w.on_update(self.msg("/status", chat=99), self.now)
        self.w.on_update(self.msg("/status", age_s=3600), self.now)
        self.w.on_update(dict(update_id=3, callback_query=dict(id="q", data="took|x",
                                                               message=dict(chat=dict(id=99), message_id=1))), self.now)
        self.assertEqual(self.sent, [])
        self.assertEqual(self.w.state["trades"], {})

    def test_pause_holds_new_alerts_but_not_followups(self):
        self.w.on_update(self.msg("/pause 2h"), self.now)
        self.assertIn("paused until", self.sent[-1][0])
        self.assertTrue(self.w.paused(self.now))
        n = len(self.sent)
        self.w.deliver([dict(alert(), size={}, risk_pct=0.5, zone_r=0.2, regimes={}, warnings=[])], self.now)
        self.assertEqual(len(self.sent), n)                                     # held back
        self.w.pause_check(self.now + 3 * 3_600_000)                            # the pause ends by itself
        self.assertFalse(self.w.paused(self.now + 3 * 3_600_000))
        self.assertIn("pause is over", self.sent[-1][0])
        self.w.on_update(self.msg("/pause"), self.now)
        self.assertEqual(self.w.state["paused_until"], -1)
        self.w.on_update(self.msg("/resume"), self.now)
        self.assertFalse(self.w.paused(self.now))

    def test_took_it_follows_the_trade_to_the_end_and_records_it(self):
        self.w.deliver([dict(alert(), size={}, risk_pct=0.5, zone_r=0.2, regimes={}, warnings=[])], self.now)
        text, buttons = self.sent[-1]
        self.assertIn("PAPER LONG SOL", text)
        aid = buttons["inline_keyboard"][0][0]["callback_data"].split("|")[1]
        self.w.on_update(self.press(f"took|{aid}"), self.now)
        self.assertIn(aid, self.w.state["trades"])
        self.assertIn("Following your LONG SOL", self.sent[-1][0])
        edit = [p for m, p in self.api if m == "editMessageReplyMarkup"][-1]
        self.assertEqual(edit["reply_markup"]["inline_keyboard"][1][0]["callback_data"], f"closed|{aid}")
        df = pd.DataFrame(bars([(100, 101, 99.5, 100.5), (100.5, 102.2, 100.4, 101.5), (101.5, 103.5, 101.4, 103)]))
        self.now = T0 + 3 * M5 + 9000
        with mock.patch.object(LW.Watcher, "update", return_value=df):
            self.w.follow(self.now)
        texts = [t for t, _ in self.sent]
        self.assertTrue(any("TP1 hit" in t for t in texts))
        self.assertTrue(any("TP2 hit" in t and "+2.5R" in t for t in texts))
        self.assertEqual(self.w.state["trades"], {})
        self.assertEqual(self.w.state["alerts"][aid]["choice"], "done")
        self.assertAlmostEqual(self.w.state["results"][-1]["r"], 2.5)
        self.w.on_update(self.msg("/trades"), self.now)
        self.assertIn("+2.5R", self.sent[-1][0])
        with open(LW.JOURNAL) as f:
            rows = f.read().splitlines()
        self.assertEqual(rows[0].split(",")[:3], ["time_utc", "alert_id", "event"])
        self.assertEqual([r.split(",")[2] for r in rows[1:]], ["alert", "took", "tp1", "tp2", "plan"])
        self.assertEqual(rows[-1].split(",")[-1], "2.5")                         # the silent plan follow-up agrees
        self.assertEqual(self.w.state["shadow"], {})
        self.w.on_update(self.press(f"skip|{aid}"), self.now)                  # finished: the choice is final
        self.assertEqual(self.w.state["alerts"][aid]["choice"], "done")

    def test_skip_and_closed_it(self):
        self.w.deliver([dict(alert(), size={}, risk_pct=0.5, zone_r=0.2, regimes={}, warnings=[])], self.now)
        aid = self.sent[-1][1]["inline_keyboard"][0][0]["callback_data"].split("|")[1]
        self.w.on_update(self.press(f"took|{aid}"), self.now)
        self.w.on_update(self.press(f"skip|{aid}"), self.now)                  # changed their mind
        self.assertEqual(self.w.state["trades"], {})
        self.w.on_update(self.press(f"took|{aid}"), self.now)
        self.w.on_update(self.press(f"closed|{aid}"), self.now)
        self.assertEqual(self.w.state["trades"], {})
        self.assertEqual(self.w.state["alerts"][aid]["choice"], "closed")
        self.assertEqual(self.w.state["results"][-1]["how"], "closed by you")
        self.assertIn("too old", self.w.on_button(dict(id="q", data="took|nope"), self.now))

    def test_poll_reads_each_update_once(self):
        LW.tg_api.side_effect = lambda method, payload, *a, **k: self.api.append((method, payload)) or (
            True, [self.msg("/status") | dict(update_id=10)] if method == "getUpdates" else {})
        self.w.poll(5)
        self.assertEqual(self.w.state["tg_offset"], 11)
        self.assertIn("Live watcher running", self.sent[-1][0])
        self.w.poll(5)
        self.assertEqual([p.get("offset") for m, p in self.api if m == "getUpdates"], [None, 11])
        with mock.patch.dict(os.environ, {"TELEGRAM_CHAT_ID": ""}):
            self.assertFalse(self.w.commands_on())                               # no chat id: no polling

    def test_state_survives_a_restart(self):
        self.w.on_update(self.msg("/pause"), self.now)
        w2 = LW.Watcher(LW.SyntheticSwap(), send=True, git=False, now_fn=lambda: self.now)
        self.assertTrue(w2.paused(self.now))


if __name__ == "__main__":
    unittest.main()
