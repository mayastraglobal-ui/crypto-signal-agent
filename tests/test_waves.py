"""2026-10-15 (operator: "remove 5m check + one alert per wave"): 4H / 1H 🔵 TEST alerts go out at the candle close
(as in their 5-year backtest), 30m and faster still wait for their 5m candle; the 5m check's verdict on 4H / 1H setups is
still recorded silently (the side-by-side record); at most 2 TEST alerts per wave (the same direction within 8 hours),
the rest named in one information note; the replay applies the same rules."""
import os
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import scanner as sc  # noqa: E402
from engine import confirm5m as c5m  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import signal_center as SCX  # noqa: E402
from test_signal_center import test_alert as full_alert  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
H = 3_600_000


def coin():
    return dict(n=40, win_rate=45.0, avg_r=0.3, total_r=12.0, test_n=10, test_avg_r=0.2, score=1.9)


def t(coin_="BTC", d=1, score=1.0, tf="4h"):
    return dict(label="TEST", coin=coin_, d=d, tf=tf, strategy="P01-BREAKOUT-V1", test=dict(score=score))


class Rules(unittest.TestCase):
    def test_config(self):
        S = SCX.settings(CFG.get("signal_center"))
        self.assertEqual(S["confirm_5m_tfs"], ["30m", "15m", "5m"])
        self.assertEqual((S["wave_max"], S["wave_hours"]), (2, 8.0))
        self.assertFalse(SCX.needs_5m("4h", S))
        self.assertFalse(SCX.needs_5m("1h", S))
        self.assertTrue(SCX.needs_5m("30m", S))
        self.assertFalse(SCX.needs_5m("30m", dict(S, confirm_5m=False)))     # the master switch still works
        self.assertEqual(c5m.settings(CFG.get("confirm_5m"))["compare_tfs"], ["4h", "1h"])

    def test_two_per_wave_strongest_first_then_a_new_wave(self):
        S = SCX.settings(None)
        waves = {}
        send, over = SCX.wave_filter([t("SOL", score=1), t("BTC", score=3), t("ETH", score=2)], waves, 0, S)
        self.assertEqual([a["coin"] for a in send], ["BTC", "ETH"])          # the strongest evidence first
        self.assertEqual([a["wave"] for a in send], [(1, 2), (2, 2)])
        self.assertEqual([a["coin"] for a in over], ["SOL"])
        send, over = SCX.wave_filter([t("XRP", d=-1)], waves, H, S)           # the other side: its own wave
        self.assertEqual([a["coin"] for a in send], ["XRP"])
        send, over = SCX.wave_filter([t("ZEC")], waves, 7 * H, S)              # still the long wave (7 h)
        self.assertEqual((send, [a["coin"] for a in over]), ([], ["ZEC"]))
        send, over = SCX.wave_filter([t("ZEC")], waves, 8 * H + 1, S)          # 8 hours on: a new wave
        self.assertEqual([a["coin"] for a in send], ["ZEC"])
        self.assertEqual(waves["1"]["n"], 1)
        all_ = [t(c) for c in ("A", "B", "C")]
        self.assertEqual(SCX.wave_filter(all_, {}, 0, dict(S, wave_max=0)), (all_, []))   # 0 = off

    def test_wave_note_and_alert_line(self):
        txt = SCX.wave_text([t("SOL", d=-1), t("XRP", d=-1, tf="1h")], 2)
        self.assertIn("🌊 <b>Wave: more SHORT setups</b>", txt)
        self.assertIn("SOL (P01-BREAKOUT-V1 4h), XRP (P01-BREAKOUT-V1 1h)", txt)
        self.assertIn("first 2 alerts of this wave", txt)
        self.assertIn("Information only", txt)
        a = full_alert(tf="4h", wave=(1, 2))
        self.assertIn("🌊 Wave alert 1 of 2 (SHORT side, 8 hours)", lv.message(a))


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
        clock = mock.patch.object(sc.time, "time", lambda: (self.now + 20 * 60_000) / 1000)
        clock.start()
        self.addCleanup(clock.stop)
        self.w = LW.Watcher(LW.SyntheticSwap(), send=True, git=False, now_fn=lambda: self.now)
        self.w.coins, self.w.extra = ["BTC"], []
        self.v1 = self.w.cards["P01-BREAKOUT-V1@1.0"]
        self.w.tests = {"P01-BREAKOUT-V1@1.0|4h": {"BTC": dict(coin(), strategy=1, version="V1")}}
        self.w.watch = [(self.v1, "4h", "TEST")]
        self.w.regime_fit = {}
        self.sent = []
        p1 = mock.patch.object(LW, "telegram_message",
                               side_effect=lambda text, *a, **k: self.sent.append((text, k.get("buttons"))) or (True, "", 77))
        p2 = mock.patch.object(LW, "tg_api", side_effect=lambda *a, **k: (True, {}))
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

    def test_4h_alerts_at_the_close_and_records_the_5m_verdict_silently(self):
        self.w.SC = dict(self.w.SC, pullback=False)        # a market entry (2026-10-25: TEST 4H / 1H = a pullback limit,
        with self.fire():                                  # which has no 5m side-by-side - tests/test_pullback.py)
            a = self.w.tick(self.now)
        self.assertEqual(len(a), 1)                                        # no waiting: sent at the 4H close
        self.assertEqual((a[0]["tf"], a[0]["wave"]), ("4h", (1, 2)))
        msgs = [x for x, _ in self.sent if "<b>TEST · SHORT BTC</b>" in x]
        self.assertEqual(len(msgs), 1)
        self.assertIn("🌊 Wave alert 1 of 2", msgs[0])
        self.assertFalse(any("<b>Watch ·" in x for x, _ in self.sent))     # no 👀 waiting note
        self.assertEqual(len(self.w.pending), 1)                           # ... only the silent 5m verdict
        p = self.w.pending[0]
        self.assertTrue(p["verdict_only"])
        twin = self.w.state["shadow"][p["twin"]]
        self.assertTrue(twin["no5m"])
        n_msgs = len(self.sent)
        with mock.patch.object(c5m, "check", return_value=dict(state=c5m.EXPIRED, idx=None, bars=6, why="no", smc=[])):
            self.now += 300_000
            self.assertEqual(self.w.tick(self.now), [])
        self.assertEqual(self.w.pending, [])
        self.assertEqual(twin["five_min"], "rejected")                    # recorded, nothing sent, nothing released
        self.assertEqual(len(self.sent), n_msgs)
        self.assertTrue(any(k.startswith("TEST|BTC|-1") for k in self.w.state["sent"]))   # the cooldown holds

    def test_the_third_alert_of_a_wave_is_a_note_once(self):
        mk = lambda c: full_alert(coin=c, inst=f"{c}-USDT-SWAP", tf="4h", close_ms=self.now - 1,  # noqa: E731
                                  sent_ms=self.now, key=f"k{c}")
        self.w.deliver([mk("BTC"), mk("ETH")], self.now)
        self.w.deliver([mk("SOL")], self.now + H)
        self.w.deliver([mk("XRP")], self.now + 2 * H)
        alerts = [x for x, _ in self.sent if "<b>TEST · SHORT" in x]
        notes = [x for x, _ in self.sent if "Wave: more SHORT setups" in x]
        self.assertEqual(len(alerts), 2)
        self.assertEqual(len(notes), 1)                                    # one note per wave
        self.assertIn("SOL", notes[0])
        self.assertEqual(len(self.w.state["test_sent"]), 2)
        self.w.deliver([mk("SUI")], self.now + 9 * H)                      # a new wave
        self.assertEqual(len([x for x, _ in self.sent if "<b>TEST · SHORT" in x]), 3)

    def test_30m_still_waits_for_its_5m_candle(self):
        v2 = self.w.cards["P01-BREAKOUT-V2@1.0"]
        self.w.tests = {"P01-BREAKOUT-V2@1.0|30m": {"BTC": dict(coin(), strategy=1, version="V2")}}
        self.w.watch = [(v2, "30m", "TEST")]
        with self.fire():
            self.assertEqual(self.w.tick(self.now), [])
        self.assertEqual(len(self.w.pending), 1)
        self.assertFalse(self.w.pending[0].get("verdict_only"))

    def test_replay_uses_the_same_rules(self):
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        body = src[src.index("def replay(w"):src.index("def replay_text")]
        self.assertIn('scx.needs_5m(a["tf"], w.SC)', body)
        self.assertIn("scx.wave_filter([a], waves", body)
        self.assertIn('why="wave maximum reached"', body)
        self.assertIn("over the wave maximum", src)


if __name__ == "__main__":
    unittest.main()
