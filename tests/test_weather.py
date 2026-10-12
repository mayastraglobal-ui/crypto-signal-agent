"""Upgrade 10, the market weather (engine/weather.py): verdicts from the agent's own permission, volatility and the
usual 24h move from daily candles, crowding, the /weather reply and the briefing email block. Offline, synthetic."""
import datetime as dt
import json
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
from engine import emails as em  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import mailfacts as mf  # noqa: E402
from engine import signal_center as scx  # noqa: E402
from engine import weather as wx  # noqa: E402

NOW = dt.datetime(2026, 10, 8, 8, 0, tzinfo=dt.timezone.utc)


def rec(d1, h4, h1):
    return {"1w": dict(label="WEAK_BULL"), "1d": dict(label=d1, values=dict(adx=30)),
            "4h": dict(label=h4, values=dict(adx=25)), "1h": dict(label=h1, values=dict(adx=20))}


def regime(perm, d1="WEAK_BULL", h4="WEAK_BULL", h1="WEAK_BULL"):
    return dict(timeframes=rec(d1, h4, h1), permission=perm, permission_reason="test")


def daily(n=800, vol=0.02, seed=1, last_vol=None):
    rng = np.random.default_rng(seed)
    r = rng.normal(0, vol, n)
    if last_vol is not None:
        r[-20:] = rng.normal(0, last_vol, 20)
    c = 100 * np.exp(np.cumsum(r))
    span = np.abs(rng.normal(0, vol, n)) * c
    return c + span / 2, c - span / 2, c


class Verdicts(unittest.TestCase):
    def test_coin_verdict_follows_the_agents_own_permission(self):
        self.assertEqual(wx.coin_verdict(rec("WEAK_BULL", "WEAK_BULL", "RANGE"), "LONG allowed"), "UP")
        self.assertEqual(wx.coin_verdict(rec("WEAK_BEAR", "WEAK_BEAR", "RANGE"), "SHORT allowed"), "DOWN")
        self.assertEqual(wx.coin_verdict(rec("WEAK_BULL", "RANGE", "COMPRESSION"), "NO TRADE"), "RANGE")
        self.assertEqual(wx.coin_verdict(rec("WEAK_BULL", "TRANSITION", "WEAK_BEAR"), "NO TRADE"), "CHOPPY")

    def test_market_verdict(self):
        c = lambda *v: [dict(coin=k, verdict=x) for k, x in zip(["BTC", "ETH", "SOL", "XRP"], v)]  # noqa: E731
        self.assertEqual(wx.market_verdict(c("UP", "UP", "CHOPPY", "UP"), []), "TREND_UP")
        self.assertEqual(wx.market_verdict(c("UP", "CHOPPY", "CHOPPY", "RANGE"), []), "MIXED")
        self.assertEqual(wx.market_verdict(c("DOWN", "DOWN", "DOWN", "CHOPPY"), []), "TREND_DOWN")
        self.assertEqual(wx.market_verdict(c("RANGE", "UP", "UP", "UP"), []), "RANGE")
        self.assertEqual(wx.market_verdict(c("CHOPPY", "UP", "UP", "UP"), []), "CHOPPY")
        self.assertEqual(wx.market_verdict(c("UP", "UP", "UP", "UP"), ["US CPI"]), "NEWS")


class Volatility(unittest.TestCase):
    def test_usual_move_is_measured_on_similar_days(self):
        st = wx.daily_stats(*daily())
        self.assertIsNotNone(st)
        self.assertLess(st["usual_move_pct"], st["move_8of10_pct"])
        self.assertGreater(st["days"], 30)
        lo, hi = st["band"]
        self.assertLess(lo, st["price"])
        self.assertGreater(hi, st["price"])

    def test_a_wild_spell_is_high_volatility(self):
        calm = wx.daily_stats(*daily(vol=0.02))
        wild = wx.daily_stats(*daily(vol=0.02, last_vol=0.08))
        self.assertGreater(wild["vol_pctile"], 90)
        self.assertIn(wild["vol_label"], ("high", "extreme"))
        self.assertGreater(wild["atr_pct"], calm["atr_pct"])

    def test_too_little_history_says_nothing(self):
        self.assertIsNone(wx.daily_stats(*daily(n=40)))


class Crowding(unittest.TestCase):
    def frames(self, rate, oi_old, oi_new):
        t = int(NOW.timestamp() * 1000)
        h = pd.DataFrame(dict(ts=[t - 25 * 3_600_000, t - 3_600_000], coin="BTC", source="okx",
                              oi_usd=[oi_old, oi_new], ls_ratio=1.0, taker_ratio=1.0))
        f = pd.DataFrame(dict(time=[t - 8 * 3_600_000], coin="BTC", source="okx", rate=[rate]))
        return h, f

    def test_labels(self):
        self.assertEqual(wx.crowding(*self.frames(0.0005, 100, 110))["label"], "crowded long")
        self.assertEqual(wx.crowding(*self.frames(0.0005, 100, 101))["label"], "leaning long")
        self.assertEqual(wx.crowding(*self.frames(-0.0002, 100, 110))["label"], "crowded short")
        self.assertEqual(wx.crowding(*self.frames(0.0001, 100, 110))["label"], "neutral")
        c = wx.crowding(*self.frames(0.0005, 100, 110))
        self.assertAlmostEqual(c["funding_pct"], 0.05)
        self.assertAlmostEqual(c["oi_24h_pct"], 10.0)
        self.assertEqual(wx.crowding(None, None)["label"], "unknown")


class Turning(unittest.TestCase):
    """2026-10-12 (operator: "fix weather wording"): a fall on 1H that 4H / 1D have not confirmed is named for it."""
    def recs(self, h1, h4, mo1="down", su1="up", mo4="down", su4="mixed"):
        return {"1w": dict(label="WEAK_BULL"), "1d": dict(label="TRANSITION"),
                "4h": dict(label=h4, states=dict(momentum=mo4, structure=su4)),
                "1h": dict(label=h1, states=dict(momentum=mo1, structure=su1))}

    def test_turning_per_coin(self):
        self.assertEqual(wx.turning(self.recs("TRANSITION", "RANGE"), "NO TRADE"), "down")       # 12 Oct
        self.assertEqual(wx.turning(self.recs("TRANSITION", "RANGE", "up", "down", "up", "down"), "NO TRADE"), "up")
        self.assertEqual(wx.turning(self.recs("WEAK_BEAR", "TRANSITION", mo4="neutral"), "NO TRADE"), "down")
        self.assertIsNone(wx.turning(self.recs("RANGE", "RANGE"), "NO TRADE"))                # a range wiggle
        self.assertIsNone(wx.turning(self.recs("TRANSITION", "WEAK_BULL"), "NO TRADE"))       # 4H against it
        self.assertIsNone(wx.turning(self.recs("WEAK_BEAR", "WEAK_BEAR"), "SHORT allowed"))   # confirmed: DOWN
        self.assertIsNone(wx.turning(self.recs("TRANSITION", "RANGE", mo1="neutral"), "NO TRADE"))

    def test_market_verdict_and_words(self):
        c = lambda *v: [dict(coin=k, verdict=x, turning=t) for k, (x, t) in zip(["BTC", "ETH", "SOL", "XRP"], v)]  # noqa
        ch, dn = ("CHOPPY", None), ("CHOPPY", "down")
        self.assertEqual(wx.market_verdict(c(dn, dn, ch, ("DOWN", None)), []), "TURNING_DOWN")
        self.assertEqual(wx.market_verdict(c(dn, ch, ch, ch), []), "CHOPPY")          # BTC alone
        self.assertEqual(wx.market_verdict(c(ch, dn, dn, dn), []), "CHOPPY")          # BTC not turning
        self.assertEqual(wx.market_verdict(c(("CHOPPY", "up"), ("CHOPPY", "up"), ch, ch), []), "TURNING_UP")
        self.assertEqual(wx.market_verdict(c(dn, dn, dn, dn), ["US CPI"]), "NEWS")
        self.assertEqual(wx.coin_word(dict(verdict="CHOPPY", turning="down")), "turning down (not confirmed)")
        self.assertEqual(wx.coin_word(dict(verdict="RANGE", turning=None)), "range")

    def test_the_weather_text(self):
        regs = {k: dict(timeframes=self.recs("TRANSITION", "RANGE"), permission="NO TRADE", permission_reason="t")
                for k in ("BTC", "ETH", "SOL")}
        w = wx.build(NOW, regs, {}, {}, {}, [])
        self.assertEqual(w["verdict"]["code"], "TURNING_DOWN")
        self.assertEqual([c["verdict"] for c in w["coins"]], ["CHOPPY"] * 3)      # the recorded verdict is unchanged
        self.assertIn("Turning down - not confirmed", w["telegram"])
        self.assertIn("↘️ BTC: turning down (not confirmed)", w["telegram"])
        self.assertIn("SHORT alert comes only once 1H and 4H both point down", w["telegram"])
        self.assertIn("ETH turning down", "\n".join(wx.md_lines(w)))
        self.assertIn("BTC: turning down", scx.weather_line(w, "BTC"))


def weather(perm_btc="NO TRADE", blackout=None, events=None):
    regs = {"BTC": regime(perm_btc, "WEAK_BULL", "TRANSITION", "WEAK_BEAR"), "ETH": regime("LONG allowed"),
            "SOL": regime("NO TRADE", "WEAK_BULL", "RANGE", "RANGE")}
    return wx.build(NOW, regs, {"BTC": daily(), "ETH": daily(seed=2)}, {}, {"BTC": dict(change_24h=-2.0),
                                                                          "ETH": dict(change_24h=-1.0),
                                                                          "SOL": dict(change_24h=0.0)},
                    events or [], blackout, dict(value=64, label="Greed"))


class Build(unittest.TestCase):
    def test_choppy_day_explains_and_never_signals(self):
        w = weather()
        self.assertEqual(w["verdict"]["code"], "CHOPPY")
        self.assertEqual([c["coin"] for c in w["coins"]], ["BTC", "ETH", "SOL"])
        self.assertEqual(w["breadth"], dict(UP=1, DOWN=0, RANGE=1, CHOPPY=1))
        self.assertAlmostEqual(w["alts_vs_btc_24h"], 1.5)
        self.assertNotIn("signal", {k for k in w if k != "note"})          # no signal field of any kind
        t = w["telegram"]
        self.assertIn("Choppy", t)
        self.assertIn("not a forecast", t)
        self.assertIn("never creates a signal", t)
        json.dumps(w)                                                       # the file is plain JSON

    def test_news_blackout_and_event_warning(self):
        ev = [dict(start_utc="2026-10-08 12:30", name="US CPI")]
        w = weather("LONG allowed", blackout=["US CPI"], events=ev)
        self.assertEqual(w["verdict"]["code"], "NEWS")
        self.assertTrue(any("within 24 hours" in x for x in w["warnings"]))
        self.assertEqual(w["events"][0]["hours"], 4.5)

    def test_md_lines(self):
        lines = wx.md_lines(weather())
        self.assertTrue(lines[0].startswith("- verdict"))
        self.assertIn("never creates a signal", lines[-1])
        self.assertIn("not available", wx.md_lines(None)[0])


class Telegram(unittest.TestCase):
    def test_reply_with_age_and_missing_file(self):
        w = weather()
        now_ms = int(NOW.timestamp() * 1000)
        self.assertIn("Made by GitHub's hourly scan 0m ago", lv.weather_text(w, now_ms))
        self.assertIn("Older than 3 hours", lv.weather_text(w, now_ms + 4 * 3_600_000))
        self.assertIn("No market weather yet", lv.weather_text(None, now_ms))
        self.assertIn("/weather", lv.HELP)

    def test_watcher_command_reads_the_downloaded_file(self):
        self.assertIn(("main", "reports/market_weather.json"), LW.SYNC_FILES)
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "reports"))
            with open(os.path.join(d, "reports", "market_weather.json"), "w") as f:
                json.dump(weather(), f)
            w = LW.Watcher.__new__(LW.Watcher)
            with mock.patch.object(LW, "ROOT", d):
                self.assertIn("Choppy", w.command("weather", "", int(NOW.timestamp() * 1000)))
            with mock.patch.object(LW, "ROOT", os.path.join(d, "none")):
                self.assertIn("No market weather yet", w.command("weather", "", int(NOW.timestamp() * 1000)))


class Email(unittest.TestCase):
    def test_briefing_shows_the_weather_and_changes_list_a_new_verdict(self):
        w = weather()
        blocks = em.weather_blocks(w)
        self.assertEqual(blocks[0], ("section", "Market weather"))
        kv = dict(blocks[1][1])
        self.assertIn("Choppy", kv["Verdict"])
        self.assertIn("not a forecast", kv["BTC usual 24h move"])
        self.assertEqual(em.weather_blocks(None), [])
        b = mf.briefing(dict(weather=w), "08:20", "2026-10-08 00:20", None, None, None)
        self.assertIs(b["weather"], w)
        self.assertIn("Market weather", str(em.briefing(b)))
        prev = mf.snapshot(dict(weather=w, generated_utc="2026-10-08 00:20"), None, None, [])
        w2 = weather("LONG allowed")
        now = mf.snapshot(dict(weather=w2, generated_utc="2026-10-08 06:20"), None, None, [])
        self.assertIn(("◆", f"Market weather: {w['verdict']['title']} → {w2['verdict']['title']}"),
                      mf.diff(prev, now))


if __name__ == "__main__":
    unittest.main()
