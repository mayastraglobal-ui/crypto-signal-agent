"""2026-10-25 (operator: "add pullback entry"): a 4H / 1H 🔵 TEST setup is a limit order 0.25 ATR behind the signal
close, waiting 6 candles (not filled = no trade) - in the live watcher's alert and in the hourly scan's TEST record.
5+ years on the 12 alert strategies x their coins: +0.30R a trade instead of +0.25R. A card's own limit entry, the
5m-confirmed cards and 30m and faster keep their entry; PAPER / LIVE are unchanged."""
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
from engine import live as lv  # noqa: E402
from engine import signal_center as SCX  # noqa: E402
from test_signal_center import test_alert as full_alert  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
H = 3_600_000


class Rule(unittest.TestCase):
    def test_config_and_rule(self):
        S = SCX.settings(CFG.get("signal_center"))
        self.assertEqual((S["pullback"], S["pullback_offset_atr"], S["pullback_bars"], S["pullback_tfs"]),
                         (True, 0.25, 6, ["4h", "1h"]))
        card = dict(id="P01-BREAKOUT-V1", version="1.0")
        self.assertEqual(SCX.pullback_entry(card, "4h", S), (0.25, 6))
        self.assertEqual(SCX.pullback_entry(card, "1h", S), (0.25, 6))
        self.assertIsNone(SCX.pullback_entry(card, "30m", S))                       # 30m and faster: unchanged
        self.assertIsNone(SCX.pullback_entry(dict(card, entry=dict(type="limit", offset_atr=0, valid_bars=2)), "1h", S))
        self.assertIsNone(SCX.pullback_entry(dict(card, confirm_5m=True), "4h", S))
        self.assertIsNone(SCX.pullback_entry(card, "4h", dict(S, pullback=False)))  # the switch

    def test_alert_text(self):
        a = full_alert(tf="4h", limit_bars=6, pullback=True)
        txt = lv.message(a)
        self.assertIn("LIMIT", txt)
        self.assertIn("🎯 Pullback entry: wait for this price, do not chase", txt)
        self.assertNotIn("🎯", lv.message(full_alert(tf="4h")))

    def test_the_scan_uses_it_for_test_records(self):
        src = open(os.path.join(ROOT, "scanner.py"), encoding="utf-8").read()
        self.assertIn("pull = None if graded else scx.pullback_entry(s, tf, SCP)", src)


class Watcher(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        for p in [mock.patch.object(LW, "STATE", os.path.join(self.tmp.name, "state.json")),
                  mock.patch.object(LW, "JOURNAL", os.path.join(self.tmp.name, "journal", "my_trades.csv")),
                  mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "1:x", "TELEGRAM_CHAT_ID": "42"}),
                  mock.patch.object(LW, "log")]:
            p.start()
            self.addCleanup(p.stop)
        self.hour = (int(__import__("time").time() * 1000) // (4 * H)) * 4 * H
        self.now = self.hour + 8000
        clock = mock.patch.object(sc.time, "time", lambda: (self.now + 20 * 60_000) / 1000)
        clock.start()
        self.addCleanup(clock.stop)
        self.w = LW.Watcher(LW.SyntheticSwap(), send=True, git=False, now_fn=lambda: self.now)
        self.w.coins, self.w.extra = ["BTC"], []
        v1 = self.w.cards["P01-BREAKOUT-V1@1.0"]
        coin = dict(n=40, win_rate=45.0, avg_r=0.3, total_r=12.0, test_n=10, test_avg_r=0.2, score=1.9,
                    strategy=1, version="V1")
        self.w.tests = {"P01-BREAKOUT-V1@1.0|4h": {"BTC": coin}}
        self.w.watch = [(v1, "4h", "TEST")]
        self.w.regime_fit = {}
        self.sent = []
        for p in [mock.patch.object(LW, "telegram_message",
                                    side_effect=lambda text, *a, **k: self.sent.append(text) or (True, "", 77)),
                  mock.patch.object(LW, "tg_api", side_effect=lambda *a, **k: (True, {}))]:
            p.start()
            self.addCleanup(p.stop)

    def fire(self, d=-1):
        def fake(s, tf, fr, cfg, gc=None, detail=None):
            n = fr["n"]
            L, S_ = np.zeros(n, bool), np.zeros(n, bool)
            (L if d == 1 else S_)[n - 1] = True
            return L, S_, None, None, {c: sc.level_array(c, fr["ns"], n) for c in LW.sspec.columns_needed(s)}
        return mock.patch.object(sc, "strategy_signals", fake)

    def test_a_4h_test_alert_is_a_limit_behind_the_close(self):
        seen = {}
        real = sc.prepare_coin

        def keep(*a, **k):
            pc = real(*a, **k)
            fr = pc["frames"].get("4h")
            if fr is not None:
                seen["close"], seen["atr"] = float(fr["df"]["close"].iloc[-1]), float(fr["df"]["_atr"].iloc[-1])
            return pc
        with self.fire(), mock.patch.object(sc, "prepare_coin", keep):
            a = self.w.tick(self.now)
        self.assertEqual(len(a), 1)
        self.assertEqual((a[0]["limit_bars"], a[0]["pullback"]), (6, True))
        self.assertAlmostEqual(a[0]["entry"], seen["close"] + 0.25 * seen["atr"], places=6)   # a short: above
        msg = [x for x in self.sent if "<b>TEST · SHORT BTC</b>" in x][0]
        self.assertIn("SELL LIMIT", msg)
        self.assertIn("🎯 Pullback entry", msg)
        self.assertFalse(any(p.get("verdict_only") for p in self.w.pending))   # no 5m side-by-side for a limit

    def test_switched_off_is_the_market_entry(self):
        self.w.SC = dict(self.w.SC, pullback=False)
        with self.fire():
            a = self.w.tick(self.now)
        self.assertEqual((a[0]["limit_bars"], a[0]["pullback"]), (None, False))


if __name__ == "__main__":
    unittest.main()
