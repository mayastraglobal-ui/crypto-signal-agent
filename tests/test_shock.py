"""⚡ Shock alarm (2026-10-10): every minute, a note when the market moves suddenly between candle closes.
Information only. Offline: made-up candles, nothing is sent."""
import csv
import datetime as dt
import os
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import journal_review as JRV  # noqa: E402
import live_watcher as LW  # noqa: E402
from engine import shock as shk  # noqa: E402
from engine import weekly_review as WR  # noqa: E402

T0 = 1_791_158_400_000                     # 2026-10-05 00:00 UTC
H, M = 3_600_000, 60_000
NOW = T0 + 10 * H                          # 18:00 Beijing
S = shk.settings(None)


def minutes(now=NOW, n=600, drop=0.0, vol=10.0, spike=1.0, hole=False):
    """n closed 1-minute candles before now around 100; the last 15 move linearly by `drop` with `spike` x volume."""
    ot = np.arange(now - n * M, now, M, dtype=np.int64)
    cl = 100 + 0.05 * np.sin(np.arange(n))
    cl[-15:] = cl[-16] + drop * np.arange(1, 16) / 15
    op = np.r_[cl[0], cl[:-1]]
    v = np.full(n, vol)
    v[-15:] *= spike
    m = dict(open_time=ot, open=op, high=np.maximum(op, cl) + 0.05, low=np.minimum(op, cl) - 0.05, close=cl, volume=v)
    if hole:
        m = {k: np.delete(x, [n - 8, n - 9]) for k, x in m.items()}
    return m


def hours(now=NOW, n=60, wide=False):
    """Closed 1H candles: open / close 100, high 100.5, low 99.5 (ATR = 1 = 1%). wide: yesterday's first candle
    ranged 97 - 103 (out of the ATR's 14 candles), so smaller moves break nothing."""
    ot = np.arange(now // H * H - n * H, now // H * H, H, dtype=np.int64)
    h = dict(open_time=ot, high=np.full(n, 100.5), low=np.full(n, 99.5), close=np.full(n, 100.0))
    if wide:
        k = int(np.searchsorted(ot, now // 86_400_000 * 86_400_000 - 86_400_000))
        h["high"][k], h["low"][k] = 103.0, 97.0
    return h


def check(m1, h1=None):
    W = S["window_min"]
    return shk.measure(m1, len(m1["close"]), shk.context(h1 or hours(), int(m1["open_time"][-W]), S["atr_n"]), S)


class Measure(unittest.TestCase):
    def test_quiet_market_fires_nothing(self):
        f = check(minutes())
        self.assertEqual(f["triggers"], [])
        self.assertAlmostEqual(f["vol_x"], 1.0)

    def test_a_crash_is_a_fast_move_with_volume_that_breaks_yesterdays_low(self):
        f = check(minutes(drop=-2.5, spike=6))
        self.assertEqual(f["triggers"], ["move", "volume", "sweep_low"])
        self.assertEqual((f["d"], f["level"]), (-1, 99.5))
        self.assertLess(f["move_atr"], -2.4)
        self.assertAlmostEqual(f["vol_x"], 6.0)
        self.assertEqual(f["ms"], NOW)

    def test_thresholds(self):
        wide = hours(wide=True)
        self.assertEqual(check(minutes(drop=-1.6), wide)["triggers"], [])           # 1.6x the 1H range: not yet
        self.assertEqual(check(minutes(drop=2.0), wide)["triggers"], ["move"])
        self.assertEqual(check(minutes(drop=1.4, spike=4), wide)["triggers"], [])   # 4x volume: not yet
        self.assertEqual(check(minutes(drop=1.4, spike=6), wide)["triggers"], ["volume"])
        self.assertEqual(check(minutes(drop=0.5, spike=9), wide)["triggers"], [])   # volume without a real move
        self.assertEqual(check(minutes(drop=0.7))["triggers"], [])                  # a quiet poke above yesterday
        up = check(minutes(drop=1.3))                                               # broken during a real move
        self.assertEqual((up["triggers"], up["d"]), (["sweep_high"], 1))

    def test_a_sweep_counts_only_the_first_time_today(self):
        h1 = hours()
        h1["low"][-3] = 99.0                                                         # today already went below
        self.assertEqual(check(minutes(drop=-1.3))["triggers"], ["sweep_low"])
        self.assertNotIn("sweep_low", check(minutes(drop=-1.3), h1)["triggers"])

    def test_holes_and_too_little_data_are_never_guessed(self):
        self.assertIsNone(check(minutes(drop=-3, hole=True)))
        self.assertIsNone(shk.measure(minutes(n=40), 12, shk.context(hours(), NOW - 15 * M), S))
        self.assertIsNone(shk.context(hours(n=10), NOW - 15 * M))


class Decide(unittest.TestCase):
    def test_cooldown_bigger_and_sweeps_once_a_day(self):
        st = {}
        crash = check(minutes(drop=-2.0, spike=6))
        new = shk.decide({"ETH": crash}, st, NOW, S)
        self.assertEqual(len(new), 1)
        self.assertFalse(new[0]["bigger"])
        self.assertEqual(shk.decide({"ETH": crash}, st, NOW + 5 * M, S), [])        # the cooldown: not news
        worse = check(minutes(drop=-4.5, spike=6))
        again = shk.decide({"ETH": worse}, st, NOW + 10 * M, S)
        self.assertTrue(again[0]["bigger"])                                          # the move doubled
        self.assertIn("getting bigger", shk.line(again[0]))
        later = shk.decide({"ETH": check(minutes(drop=-1.3))}, st, NOW + 2 * H, S)
        self.assertEqual(later, [])                                                  # yesterday's low: once a day
        nxt = T0 + 24 * H + 10 * H
        self.assertEqual(len(shk.decide({"ETH": check(minutes(now=nxt, drop=-1.3), hours(now=nxt))}, st, nxt, S)), 1)

    def test_one_wave_of_a_market_move_and_the_daily_cap(self):
        st = {}
        mk = lambda coin, d=-1: dict(coin=coin, d=d)                                  # noqa: E731
        self.assertIsNone(shk.hold([mk("BTC")], st, NOW, S))
        shk.sent([mk("BTC")], st, NOW)
        self.assertEqual(shk.hold([mk("ETH")], st, NOW + 2 * M, S), "same wave")     # alts follow BTC: the same move
        self.assertEqual(shk.hold([mk("BTC"), mk("ETH")], st, NOW + 3 * M, S), "same wave")
        self.assertIsNone(shk.hold([mk("ETH", 1)], st, NOW + 3 * M, S))               # the other direction: news
        self.assertIsNone(shk.hold([mk("SOL"), mk("SUI")], st, NOW + 4 * M, S))       # the move spreads: news
        shk.sent([mk("SOL"), mk("SUI")], st, NOW + 4 * M)
        self.assertEqual(st["shock_wave"][2], ["BTC", "ETH", "SOL", "SUI"])           # held coins joined it
        self.assertIsNone(shk.hold([mk("ETH")], st, NOW + 20 * M, S))                 # the wave is over
        st["shock_sent"] = [NOW] * S["max_per_day"]
        self.assertEqual(shk.hold([mk("XRP", 1)], st, NOW + 30 * M, S), "daily cap")

    def test_the_note(self):
        s = dict(check(minutes(drop=-2.5, spike=6)), coin="ETH", bigger=False)
        t = shk.text([s], {"BTC": -0.6, "SOL": 0.1}, [("ETH", 1, "TEST"), ("BTC", -1, "PAPER")], NOW)
        for want in ("⚡ <b>Market shock</b> · 18:00 Beijing", "📉 <b>ETH</b> 97.48", "-2.5% in 15 min",
                     "volume 6.0x", "broke yesterday's low 99.5000", "Others (15 min): BTC -0.6% · SOL +0.1%",
                     "⚠️ You follow a LONG on ETH (demo): check its stop on OKX.", "not a trade signal",
                     "never chase a shock", "/shock off"):
            self.assertIn(want, t)
        self.assertNotIn("on BTC", t)                                                # BTC did not shock


class Outcome(unittest.TestCase):
    def test_kept_going_or_reversed_signed_in_the_shocks_direction(self):
        ot = np.arange(NOW, NOW + 5 * H, 5 * M, dtype=np.int64)
        cl = np.linspace(97.5, 95.5, len(ot))
        m5 = dict(open_time=ot, high=cl + 0.1, low=cl - 0.1, close=cl)
        r = shk.outcome(m5, NOW, -1, 97.5)
        self.assertGreater(r["after_1h"], 0)
        self.assertGreater(r["after_4h"], r["after_1h"])                             # it kept falling: positive
        self.assertLess(r["worst"], 0.2)
        self.assertIsNone(shk.outcome(m5, NOW + 2 * H, -1, 97.5))                    # 4 hours have not passed


class Review(unittest.TestCase):
    def rows(self):
        mk = lambda t, coin, after, same, sent="sent", trig="move": dict(        # noqa: E731
            time_utc=t, coin=coin, side="DOWN", triggers=trig, move_pct="-2.5", after_4h_pct=after,
            alerts_4h_same=str(same), sent=sent)
        return [mk("2026-10-05 09:00", "ETH", "1.2", 1, trig="move+sweep_low"), mk("2026-10-05 09:00", "SOL", "-0.8", 0),
                mk("2026-10-06 03:00", "ETH", "", 0, "daily cap"), mk("2026-09-20 01:00", "BTC", "3", 0)]

    def test_the_weeks_numbers(self):
        sv = shk.review(self.rows(), NOW + 2 * 86_400_000)
        self.assertEqual((sv["n"], sv["sent"], sv["done"], sv["kept"], sv["reversed"], sv["caught"]), (3, 2, 2, 1, 1, 1))
        self.assertEqual(sv["by_coin"], {"ETH": 2, "SOL": 1})
        self.assertEqual(sv["by_kind"], {"move": 3, "sweep_low": 1})
        text = "\n".join(shk.lines(sv))
        self.assertIn("4 hours later: 1 kept going, 1 reversed", text)
        self.assertIn("followed by a strategy alert in the same direction within 4h: 1 of 3", text)

    def test_github_reads_the_log_and_the_weekly_review_shows_it(self):
        buf = ",".join(shk.COLS) + "\n" + "\n".join(
            ",".join(str(r.get(c, "")) for c in shk.COLS) for r in self.rows()) + "\n"
        sv = JRV.shocks_review(buf, NOW + 2 * 86_400_000)
        self.assertEqual(sv["n"], 3)
        self.assertIsNone(JRV.shocks_review(None, NOW))
        now = dt.datetime(2026, 10, 7, 5, tzinfo=dt.timezone.utc)
        rv = WR.build(now, pd.DataFrame(), {}, {}, {}, [], [], shocks=sv)
        self.assertIn("## ⚡ Shock alarm", WR.render(rv))
        self.assertIn("4 hours later: 1 kept going", WR.render(rv))
        self.assertIn("⚡ Shocks: 3 this week (2 sent) · 4h later 1 kept going, 1 reversed", WR.telegram(rv))
        rv = WR.build(now, pd.DataFrame(), {}, {}, {}, [], [])
        self.assertIn("no shock log on GitHub yet", WR.render(rv))
        self.assertNotIn("⚡", WR.telegram(rv))


class FakeFeed:
    name = "fake"

    def __init__(self):
        self.m1 = {"BTC": minutes(drop=-2.5, spike=6), "ETH": minutes()}
        ot = np.arange(NOW - H, NOW + 5 * H, 5 * M, dtype=np.int64)
        cl = np.where(ot < NOW, 100.0, np.linspace(97.5, 96.0, len(ot)))
        self.m5 = pd.DataFrame(dict(open_time=ot, open=cl, high=cl + 0.1, low=cl - 0.1, close=cl, volume=1.0))
        self.calls = []

    def minutes(self, coin, n):
        self.calls.append(coin)
        return {k: v[-n:] for k, v in self.m1[coin].items()}

    def candles(self, coin, tf, n, recent_only=False):
        if tf == "5m":
            return self.m5
        h = hours()
        return pd.DataFrame(dict(h, open=h["close"], volume=1.0, close_time=h["open_time"] + H - 1))


class Watcher(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.shocks = os.path.join(self.tmp.name, "journal", "shocks.csv")
        for p in (mock.patch.object(LW, "STATE", os.path.join(self.tmp.name, "state.json")),
                  mock.patch.object(LW, "SHOCKS", self.shocks), mock.patch.object(LW, "log"),
                  mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "1:x", "TELEGRAM_CHAT_ID": "42"})):
            p.start()
            self.addCleanup(p.stop)
        self.now = NOW + 5000
        self.feed = FakeFeed()
        self.w = LW.Watcher(self.feed, send=True, git=False, now_fn=lambda: self.now)
        self.w.coins, self.w.extra = ["BTC", "ETH"], []
        self.sent = []
        p = mock.patch.object(LW, "telegram_message",
                              side_effect=lambda text, *a, **k: self.sent.append(text) or (True, "", 1))
        p.start()
        self.addCleanup(p.stop)

    def test_one_note_then_cooldown_then_the_4h_outcome_in_the_log(self):
        self.w.state["trades"]["x"] = dict(coin="BTC", d=1, label="TEST")
        new = self.w.shock_check(self.now)
        self.assertEqual([s["coin"] for s in new], ["BTC"])
        self.assertEqual(len(self.sent), 1)
        for want in ("📉 <b>BTC</b>", "Others (15 min): ETH", "You follow a LONG on BTC (demo)"):
            self.assertIn(want, self.sent[0])
        self.assertEqual(self.w.state["shock_sent"], [self.now])
        self.assertIn("⚡ Shock alarm: ON · 1 sent today (max 8)", self.w.status_text(self.now))
        self.now += M
        self.assertEqual(self.w.shock_check(self.now), [])                          # the cooldown
        self.assertEqual(len(self.sent), 1)
        self.assertFalse(os.path.exists(self.shocks))                               # the outcome needs 4 hours
        self.w.state["alerts"]["a1"] = dict(sent_ms=NOW + H, coin="BTC", d=-1)     # a strategy alert followed
        self.now = NOW + 4 * H + 7 * M
        self.w.shock_check(self.now)
        rows = list(csv.DictReader(open(self.shocks, encoding="utf-8")))
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual((r["coin"], r["side"], r["triggers"], r["sent"]), ("BTC", "DOWN", "move+volume+sweep_low",
                                                                             "sent"))
        self.assertGreater(float(r["after_4h_pct"]), 0)                             # it kept falling
        self.assertEqual((r["alerts_4h"], r["alerts_4h_same"]), ("1", "1"))
        self.assertEqual(self.w.state["shock_pending"], [])

    def test_off_and_pause_hold_the_note_but_it_is_still_logged(self):
        msg = dict(update_id=1, message=dict(chat=dict(id=42), date=self.now // 1000, text="/shock off"))
        self.w.on_update(msg, self.now)
        self.assertIn("Shock alarm is <b>OFF</b>", self.sent[-1])
        self.sent.clear()
        self.w.shock_check(self.now)
        self.assertEqual(self.sent, [])
        self.assertEqual(self.w.state["shock_pending"][0]["sent"], "off")
        self.w.state.update(shock_on=True, shock_last={}, shock_swept={}, paused_until=-1)
        self.w.shock_check(self.now)
        self.assertEqual(self.sent, [])
        self.assertEqual(self.w.state["shock_pending"][-1]["sent"], "paused")
        self.w.state.update(paused_until=0, shock_last={}, shock_swept={}, shock_sent=[self.now] * 10)
        self.w.shock_check(self.now)
        self.assertEqual(self.sent, [])
        self.assertEqual(self.w.state["shock_pending"][-1]["sent"], "daily cap")

    def test_the_minute_schedule_and_a_feed_without_minutes(self):
        self.w.shock_minute(self.now)
        self.assertEqual(self.w.next_shock_ms, NOW + M + S["check_delay_s"] * 1000)
        self.feed.minutes = mock.Mock(side_effect=RuntimeError("OKX down"))
        self.w.shock_minute(self.now + M)                                            # never raises
        self.assertFalse(LW.Watcher(LW.SyntheticSwap(), send=False, git=False).shock_ok())

    def test_the_wait_between_5m_passes_checks_every_minute(self):
        calls = []
        self.w.shock_check = lambda now: calls.append(now)
        sleep = lambda sec: setattr(self, "now", self.now + int(sec * 1000))           # noqa: E731
        with mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": ""}), mock.patch.object(LW.time, "sleep", sleep):
            self.w.wait_until(NOW + 5 * M + 8000)
        self.assertGreaterEqual(self.now, NOW + 5 * M + 8000)
        self.assertEqual(calls[0], NOW + 5000)                                         # at once, then each minute
        self.assertEqual([c - NOW for c in calls[1:]], [k * M + 5000 for k in range(1, 6)])


if __name__ == "__main__":
    unittest.main()
