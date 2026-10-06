"""Live watcher (operator request 2026-10-05): instant Telegram alerts at every 5m candle close.
Offline: synthetic prices, nothing is sent."""
import os
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import scanner as sc  # noqa: E402
from engine import confirm5m as c5m  # noqa: E402
from engine import live as lv  # noqa: E402

H = 3_600_000


class Helpers(unittest.TestCase):
    def test_settings_and_closed_timeframes(self):
        S = lv.settings({"cooldown_minutes": 30, "unknown": 1})
        self.assertEqual(S["cooldown_minutes"], 30)
        self.assertNotIn("unknown", S)
        self.assertEqual(S["stages"], {"APPROVED": "LIVE", "PAPER_TRADING": "PAPER"})
        day = 1_791_158_400_000                                     # 2026-10-05 00:00 UTC
        self.assertEqual(lv.closed_at(day), ["5m", "15m", "30m", "1h", "4h"])
        self.assertEqual(lv.closed_at(day + 5 * 60_000), ["5m"])
        self.assertEqual(lv.closed_at(day + 30 * 60_000), ["5m", "15m", "30m"])
        self.assertEqual(lv.closed_at(day + H), ["5m", "15m", "30m", "1h"])
        self.assertEqual(lv.boundary(day + 7 * 60_000), day + 5 * 60_000)

    def test_only_paper_and_approved_alert_and_lab_never_live(self):
        S = lv.settings(None)
        self.assertEqual(lv.alert_label("APPROVED", False, S), "LIVE")
        self.assertEqual(lv.alert_label("PAPER_TRADING", False, S), "PAPER")
        self.assertEqual(lv.alert_label("APPROVED", True, S), "PAPER")          # lab card: paper at most
        for st in ("BACKTESTING", "VALIDATION", "FAILED", "RETIRED", None):
            self.assertIsNone(lv.alert_label(st, False, S))

    def test_cooldown(self):
        S = lv.settings(None)
        k = lv.dedupe_key("BTC", 1, "X", "1.0", "15m")
        self.assertTrue(lv.allowed({}, k, 0, S))
        self.assertFalse(lv.allowed({k: 0}, k, 59 * 60_000, S))
        self.assertTrue(lv.allowed({k: 0}, k, 60 * 60_000, S))

    def test_message_has_everything_needed_to_trade(self):
        a = dict(label="LIVE", coin="BTC", inst="BTC-USDT-SWAP", d=-1, tf="15m", strategy="S", version="1.0",
                 entry=100.0, R=2.0, tps=[96.0, 94.0], split=[0.5, 0.5], zone_r=0.2,
                 size=dict(qty=2.5, notional=250.0, leverage=0.25, risk_usdt=5.0, capped=False), risk_pct=0.5,
                 max_hold=8, regimes={"1w": "WEAK_BEAR", "4h": "STRONG_BEAR"}, close_ms=H - 1, sent_ms=H + 9000,
                 valid_bars=2, warnings=["test warning"])
        t = lv.message(a)
        for want in ("LIVE SHORT BTC", "BTC-USDT-SWAP", "99.60 – 100.40", "Stop-loss: <b>102.00</b>",
                     "TP1: <b>96.00</b> (2.0R, close 50%)", "TP2: <b>94.00</b> (3.0R", "$5.00", "~2h00m", "1W WEAK_BEAR", "⚠️ test warning", "01:00 UTC", "not financial advice"):
            self.assertIn(want, t)
        self.assertNotIn("PAPER", t)
        self.assertIn("practice only", lv.message(dict(a, label="PAPER")))


class EndToEnd(unittest.TestCase):
    """The whole path on synthetic prices: download, data checks, prepare_coin, the strategy rules, plan_trade,
    sizing, the alert text, the duplicate guard and the 5m confirmation."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.state = mock.patch.object(LW, "STATE", os.path.join(self.tmp.name, "state.json"))
        self.state.start()
        self.w = LW.Watcher(LW.SyntheticSwap(), send=False, git=False)
        self.w.coins, self.w.extra = ["BTC"], []
        cards, _, _, _ = sc.load_cards()
        self.plain = next(c for c in cards if "1h" in c["timeframes"] and not c.get("confirm_5m")
                          and c["stop"]["method"] == "atr")
        self.c5 = next(c for c in cards if c.get("confirm_5m") and "15m" in c["timeframes"])
        self.hour = (int(__import__("time").time() * 1000) // H) * H

    def tearDown(self):
        self.state.stop()
        self.tmp.cleanup()

    def fire(self, d=1):
        def fake(s, tf, fr, cfg, gc=None, detail=None):
            n = fr["n"]
            L, S = np.zeros(n, bool), np.zeros(n, bool)
            (L if d == 1 else S)[n - 1] = True
            cols = {c: sc.level_array(c, fr["ns"], n) for c in LW.sspec.columns_needed(s)}
            return L, S, None, None, cols
        return mock.patch.object(sc, "strategy_signals", fake)

    def test_a_trigger_on_the_closed_candle_alerts_once(self):
        self.w.watch = [(self.plain, "1h", "LIVE")]
        with self.fire(1), mock.patch.object(LW, "telegram") as tg:
            a = self.w.tick(self.hour + 8000)
            tg.assert_not_called()                                     # send=False: printed, not sent
        self.assertEqual(len(a), 1)
        a = a[0]
        self.assertEqual((a["coin"], a["tf"], a["d"], a["label"]), ("BTC", "1h", 1, "LIVE"))
        self.assertEqual(a["close_ms"], self.hour - 1)                  # the candle that just closed
        self.assertGreater(a["R"], 0)
        self.assertLess(a["entry"] - a["R"], a["entry"])                  # stop below a long entry
        self.assertTrue(all(tp > a["entry"] for tp in a["tps"]))
        self.assertAlmostEqual(a["size"]["risk_usdt"], 1000 * 0.5 / 100, places=6)
        with self.fire(1):
            self.assertEqual(self.w.tick(self.hour + 9000), [])          # duplicate guard
        self.assertIn("LIVE LONG BTC", lv.message(a))

    def test_nothing_runs_when_no_watched_timeframe_closed(self):
        self.w.watch = [(self.plain, "1h", "LIVE")]
        with self.fire(1):
            self.assertEqual(self.w.tick(self.hour + 5 * 60_000 + 8000), [])  # only 5m closed
        self.assertEqual(self.w.frames, {})                                 # and nothing was downloaded

    def test_5m_cards_wait_for_the_confirmation(self):
        now = int(__import__("time").time() * 1000)
        q = ((now - 30 * 60_000) // (15 * 60_000)) * 15 * 60_000      # a 15m close whose next 5m bar has closed
        self.w.watch = [(self.c5, "15m", "PAPER")]
        plan = mock.patch.object(sc, "plan_trade", side_effect=lambda s, t, d, e, a, c, cfg, sk=None:
                                 (2.0, [e + d * 4.0, e + d * 6.0], [0.5, 0.5]))   # SMC stops need SMC levels
        plan.start()
        self.addCleanup(plan.stop)
        with self.fire(-1), mock.patch.object(c5m, "check", return_value=dict(state=c5m.AWAITING, smc=[])):
            self.assertEqual(self.w.tick(q + 8000), [])
        self.assertEqual(len(self.w.pending), 1)
        m5_close = q + 5 * 60_000 - 1
        ok = dict(state=c5m.CONFIRMED, idx=None, bars=1, why="5m bar confirmed", smc=["5m displacement"])

        def confirmed(m5, after_ms, d, entry, stop, S=None):
            j = int(np.searchsorted(m5["close_time"], m5_close))
            return dict(ok, idx=j)
        with self.fire(-1), mock.patch.object(c5m, "check", side_effect=confirmed):
            a = self.w.tick(q + 5 * 60_000 + 8000)
        self.assertEqual(len(a), 1)
        self.assertEqual((a[0]["label"], a[0]["d"]), ("PAPER", -1))
        self.assertIn("CONFIRMED", a[0]["confirm"])
        self.assertEqual(self.w.pending, [])
        self.assertTrue(all(tp < a[0]["entry"] for tp in a[0]["tps"]))   # short targets below the 5m entry

    def test_no_signal_from_untrusted_data(self):
        self.w.watch = [(self.plain, "1h", "LIVE")]
        with self.fire(1), mock.patch.object(LW.Watcher, "_good", return_value=False):
            self.assertEqual(self.w.tick(self.hour + 8000), [])


class WindowsPC(unittest.TestCase):
    """The Windows setup (docs/WINDOWS_WATCHER.md): settings file, no-git sync from GitHub, the batch files."""

    def test_settings_file_fills_the_environment_but_never_overrides_it(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "telegram.env")
            with open(p, "w") as f:
                f.write("# comment\nTELEGRAM_BOT_TOKEN=123:abc\nTELEGRAM_CHAT_ID= 42 \nEMPTY=\n")
            with mock.patch.dict(os.environ, {"TELEGRAM_CHAT_ID": "7"}, clear=True):
                LW.load_settings(p)
                self.assertEqual(os.environ["TELEGRAM_BOT_TOKEN"], "123:abc")
                self.assertEqual(os.environ["TELEGRAM_CHAT_ID"], "7")            # the environment wins
                self.assertNotIn("EMPTY", os.environ)
            LW.load_settings(os.path.join(d, "missing.env"))                     # no file: no error

    def test_sync_writes_only_complete_valid_files(self):
        class R:
            def __init__(self, code, content):
                self.status_code, self.content = code, content
        good = {"config.yaml": b"a: 1\n", "memory/strategy_registry.csv": b"id,version\nx,1.0\n",
                "reports/universe.json": b'{"signal": ["BTC"]}', "reports/funding.csv.gz": b"\x1f\x8b..."}

        def get(url):
            path = url.split("/", 6)[6]
            if path in good:
                return R(200, good[path])
            if path == "strategies.yaml":
                return R(200, b"<html>rate limited: [")                            # an error page, not YAML
            return R(404, b"Not Found")
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "strategies.yaml"), "w") as f:
                f.write("- id: keep_me\n")
            up, problems = LW.sync_files(d, "o/r", get)
            self.assertEqual(sorted(up), sorted(good))
            with open(os.path.join(d, "strategies.yaml")) as f:
                self.assertIn("keep_me", f.read())                                 # a bad download never replaces
            self.assertTrue(any("strategies.yaml" in p for p in problems))
            self.assertEqual(LW.sync_files(d, "o/r", get)[0], [])                  # unchanged: nothing rewritten
            with open(os.path.join(d, "reports", "universe.json")) as f:
                self.assertEqual(f.read(), '{"signal": ["BTC"]}')

    def test_code_outdated_ignores_line_endings(self):
        class R:
            status_code, content = 200, b"print(1)\nprint(2)\n"
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "engine"))
            for p in LW.CODE_FILES:
                with open(os.path.join(d, *p.split("/")), "wb") as f:
                    f.write(b"print(1)\r\nprint(2)\r\n")                          # a Windows copy
            self.assertEqual(LW.code_outdated(d, "o/r", lambda url: R()), [])
            with open(os.path.join(d, "scanner.py"), "wb") as f:
                f.write(b"print(3)\n")
            self.assertEqual(LW.code_outdated(d, "o/r", lambda url: R()), ["scanner.py"])

    def test_batch_files_are_windows_files_and_call_real_scripts(self):
        wdir = os.path.join(ROOT, "windows")
        names = sorted(os.listdir(wdir))
        self.assertEqual(names, ["1_setup.bat", "2_start_watcher.bat", "3_stop_watcher.bat", "4_update.bat",
                                 "5_remove_autostart.bat", "run_watcher.bat"])
        for n in names:
            with open(os.path.join(wdir, n), "rb") as f:
                b = f.read()
            self.assertNotIn(b"\n", b.replace(b"\r\n", b""), f"{n}: every line must end with CRLF")
            self.assertTrue(b.startswith(b"@echo off"), n)
        text = open(os.path.join(wdir, "1_setup.bat")).read()
        for flag in ("--test-telegram", "--setup-telegram", "--sync"):
            self.assertIn(flag, text)
        run = open(os.path.join(wdir, "run_watcher.bat")).read()
        self.assertIn("live_watcher.py", run)
        self.assertIn("STOP_WATCHER", run)
        self.assertIn("STOP_WATCHER", open(os.path.join(wdir, "3_stop_watcher.bat")).read())
        upd = open(os.path.join(wdir, "4_update.bat")).read()
        self.assertIn("telegram.env", upd)                                         # settings kept on update
        self.assertIn("--from-temp", upd)                                          # never rewrites itself mid-run
        ignored = open(os.path.join(ROOT, ".gitignore")).read().split()
        for p in ("telegram.env", "logs/", ".venv/", "STOP_WATCHER", "reports/live_watcher_state.json"):
            self.assertIn(p, ignored)


class TelegramSend(unittest.TestCase):
    def test_missing_settings_are_reported_not_raised(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            ok, err = LW.telegram("x")
        self.assertFalse(ok)
        self.assertIn("TELEGRAM_BOT_TOKEN", err)


if __name__ == "__main__":
    unittest.main()
