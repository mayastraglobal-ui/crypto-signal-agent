"""Upgrade 10, the market weather (engine/weather.py): verdicts from the agent's own permission, volatility and the
usual 24h move from daily candles, crowding, the /weather reply and the briefing email block. Offline, synthetic."""
import datetime as dt
import json
import os
import sys
import tempfile
import types
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


class DailyTrend(unittest.TestCase):
    """2026-11-03 (operator: "BTC fell from 87,000 to 76,000 and /weather says turning down"): when BTC's daily chart
    clearly trends, the verdict names that trend and says the strategies still wait; a 1H bounce inside it is a
    bounce, not "turning up". Display only: the recorded coin verdicts (the market types) are unchanged."""
    def fall(self, n=400, drop=0.12):
        c = np.r_[np.linspace(80, 100, n - 40), np.linspace(100, 100 * (1 - drop), 40)]
        c = c * (1 + 0.004 * np.sin(np.arange(n)))                        # small daily wiggles
        return c * 1.01, c * 0.99, c

    def test_price_trend(self):
        p = wx.price_trend(*self.fall())
        self.assertEqual(p["dir"], "down")
        self.assertLess(p["chg_pct"], -5)
        self.assertEqual(p["swing"], "lower highs and lower lows")
        h, lo, c = (200 - a for a in self.fall())                         # the mirror image: a rise
        self.assertEqual(wx.price_trend(lo, h, c)["dir"], "up")
        flat = np.full(400, 100.0) * (1 + 0.01 * np.sin(np.arange(400)))
        self.assertEqual(wx.price_trend(flat * 1.01, flat * 0.99, flat)["dir"], "sideways")
        self.assertIsNone(wx.price_trend(*(a[:50] for a in self.fall())))
        t = wx.price_text(p)
        self.assertTrue(t.startswith("DOWN · -"))
        self.assertIn("lower highs and lower lows", t)
        self.assertNotIn("average", t)                                     # operator: no 50 / 200-day averages

    def test_daily_view(self):
        dn, up = dict(price=dict(dir="down")), dict(price=dict(dir="up"))
        self.assertEqual(wx.daily_view("TURNING_DOWN", dn), "DOWNTREND_WAIT")
        self.assertEqual(wx.daily_view("CHOPPY", dn), "DOWNTREND_WAIT")
        self.assertEqual(wx.daily_view("TURNING_UP", dn), "BOUNCE_DOWNTREND")
        self.assertEqual(wx.daily_view("TURNING_DOWN", up), "DIP_UPTREND")
        self.assertEqual(wx.daily_view("CHOPPY", up), "UPTREND_WAIT")
        for code in ("TREND_DOWN", "TREND_UP", "MIXED", "RANGE", "NEWS"):
            self.assertEqual(wx.daily_view(code, dn), code)                # confirmed / other verdicts stay
        self.assertEqual(wx.daily_view("CHOPPY", dict(price=dict(dir="sideways"))), "CHOPPY")
        self.assertEqual(wx.daily_view("TURNING_DOWN", None), "TURNING_DOWN")
        self.assertEqual(wx.coin_word(dict(verdict="CHOPPY", turning="down", price=dict(dir="down"))),
                         "downtrend on the daily chart (not confirmed)")
        self.assertEqual(wx.coin_word(dict(verdict="CHOPPY", turning="up", price=dict(dir="down"))),
                         "bounce in a downtrend (daily)")
        self.assertEqual(wx.coin_word(dict(verdict="DOWN", turning=None, price=dict(dir="down"))), "trend down")

    def test_the_3_nov_case(self):
        rc = Turning().recs("WEAK_BEAR", "UNCLEAR", mo4="down", su4="mixed")
        regs = {k: dict(timeframes=rc, permission="NO TRADE", permission_reason="t") for k in ("BTC", "ETH", "SOL")}
        w = wx.build(NOW, regs, {k: self.fall() for k in regs}, {}, {}, [])
        self.assertEqual(w["verdict"]["code"], "DOWNTREND_WAIT")
        self.assertEqual([c["verdict"] for c in w["coins"]], ["CHOPPY"] * 3)    # the recorded verdict is unchanged
        t = w["telegram"]
        self.assertIn("Downtrend - the strategies wait", t)
        self.assertIn("BTC price trend (daily chart): <b>DOWN", t)
        self.assertIn("Strategy alerts (need 4H and 1H to agree)", t)
        self.assertIn("↘️ BTC: downtrend on the daily chart (not confirmed)", t)
        self.assertNotIn("Turning", t)
        self.assertIn("daily price trend DOWN", "\n".join(wx.md_lines(w)))


class LiveCandles(unittest.TestCase):
    """2026-11-03 (operator: "daily / 4H / 1H: the trend from the last closed candles and the live candle, well
    organized"; chose 1D 2 / 4H 3 / 1H 3 closed candles, the majority colour, BTC in full + one line per other coin,
    2 strategy lines at the bottom, a day from 08:00 Beijing): the /weather candle report, read from OKX when asked."""
    T = 1_762_000_000_000

    def rows(self, d1=((100, 101), (101, 99)), h4=((98, 98.5), (98.5, 98.2), (98.2, 97.9)),
             h1=((97.9, 98.0), (98.0, 97.95), (97.95, 98.1))):
        q = lambda t, o, c, closed: (t, o, max(o, c) * 1.01, min(o, c) * 0.99, c, closed)  # noqa: E731
        mk = lambda done, now: [q(self.T + i, o, c, True) for i, (o, c) in enumerate(done)] + \
            [q(self.T + 9, *now, False)]                                                # noqa: E731
        return {"1d": mk(list(d1), (99, 99.5)), "4h": mk(list(h4), (97.9, 97.7)), "1h": mk(list(h1), (98.1, 98.4))}

    def test_trend_rule(self):
        b, r = [dict(dir="bull", pct=1.0)], [dict(dir="bear", pct=-1.98)]
        self.assertEqual(wx.trend_of(b + r + r), "bear")                                # 2 of 3 red
        self.assertEqual(wx.trend_of(b + r), "bear")                                    # a tie: the bigger move
        self.assertEqual(wx.trend_of([dict(dir="bull", pct=1.0), dict(dir="bear", pct=-1.0)]), "mixed")
        self.assertIsNone(wx.trend_of([]))
        self.assertEqual(wx.TREND_N, {"1d": 2, "4h": 3, "1h": 3})

    def test_report(self):
        rep = wx.candle_report({"BTC": self.rows(), "ETH": self.rows(d1=((50, 51), (51, 52)))}, ["BTC", "ETH"])
        b = rep["coins"][0]
        self.assertEqual(len(b["1d"]["closed"]), 2)
        self.assertEqual(b["1d"]["trend"], "bear")                     # +1.0% then -1.98%: a tie, the bigger move
        self.assertEqual(b["1d"]["now"]["dir"], "bull")                 # today so far
        self.assertEqual([x["dir"] for x in b["4h"]["closed"]], ["bull", "bear", "bear"])
        self.assertEqual(b["4h"]["trend"], "bear")
        self.assertEqual(b["1h"]["trend"], "bull")                     # bull, bear (-0.05%), bull
        self.assertEqual(b["price"], 98.4)
        self.assertEqual(rep["coins"][1]["1d"]["trend"], "bull")
        self.assertEqual(wx.candle(100, 100.04)["dir"], "flat")

    def test_text(self):
        w = dict(verdict=dict(title="Downtrend - the strategies wait for a clean 4H / 1H"),
                 events=[dict(name="US jobs report", start_utc="2026-11-06 13:30")])
        t = wx.candles_text(wx.candle_report({"BTC": self.rows(), "SOL": self.rows()}, ["BTC", "SOL"]),
                            "11-03 17:30 Beijing", wx.strategy_note(w))
        lines = t.split("\n")
        self.assertEqual(lines[0], "📊 <b>BTC 98.40</b> · 11-03 17:30 Beijing")
        self.assertEqual(lines[1], "🔴 <b>BEARISH · 2 of 3 timeframes red</b>")                  # A
        self.assertIn("   Yesterday high 102.01 · low 98.01 → ↔️ now inside yesterday's range", lines)   # B
        for head in ("📅 <b>DAILY</b>", "⏱ <b>4 HOUR</b>", "⏰ <b>1 HOUR</b>"):
            self.assertIn(head, lines)
        self.assertIn("   Trend: <b>🔴 BEAR</b>  (🟢 +1.0% · 🔴 -2.0%)", lines)
        self.assertIn("   Today live: 🟢 BULL +0.5%", lines)
        self.assertIn("   Trend: <b>🔴 BEAR</b>  (🟢 🔴 🔴)", lines)
        self.assertIn("   Live candle: 🔴 BEAR -0.2%", lines)
        self.assertIn("<code>SOL </code> 🔴(🟢) · 🔴(🔴) · 🟢(🟢)", lines)
        self.assertIn("🧠 Strategy alerts: Downtrend - the strategies wait for a clean 4H / 1H", lines)
        self.assertIn("📅 Next event: US jobs report 11-06 21:30 Beijing", lines)
        self.assertNotIn("average", t)
        self.assertIsNone(wx.candles_text(None, "x"))
        self.assertEqual(wx.strategy_note(None), [])

    def test_summary_levels_and_change_note(self):
        x = lambda d, h4, h1: {"1d": dict(trend=d), "4h": dict(trend=h4), "1h": dict(trend=h1)}  # noqa: E731
        self.assertEqual(wx.overall(x("bear", "bear", "bear")), ("🔴", "BEARISH · all 3 timeframes red"))
        self.assertEqual(wx.overall(x("bull", "bull", "bear"))[0], "🟢")
        self.assertEqual(wx.overall(x("bull", "bear", "mixed"))[0], "⚪")
        c = dict(price=95.0, **{"1d": dict(prev=dict(high=102.0, low=98.0))})
        self.assertEqual(wx.range_side(c), "below")
        self.assertIn("⬇️ now BELOW yesterday's low (weak)", wx.range_note(c))
        self.assertEqual(wx.range_side(dict(c, price=103.0)), "above")
        self.assertIsNone(wx.range_note(dict(price=1.0, **{"1d": {}})))
        t = wx.trend_change_text("BTC", "4h", "bear", "bull", [dict(dir="bull", pct=1)] * 3, 77000)
        self.assertIn("⏱ 4H trend changed · <b>BTC</b> 77,000", t)
        self.assertIn("🔴 BEAR → 🟢 BULL", t)
        self.assertIn("/trendalert off", t)

    def notes_watcher(self, rows, state=None):
        said = []

        class Feed:
            name = "fake"

            def recent(s, coin, tf, n=3):
                return rows(tf)
        w = LW.Watcher.__new__(LW.Watcher)
        w.cfg, w.feed, w.state, w.say = dict(universe=dict(own_coins=["BTC"])), Feed(), dict(state or {}), said.append
        w._save_state, w._json = (lambda: None), (lambda rel: None)
        return w, said

    def test_morning_report_once_a_day(self):                                          # C
        day = 1_762_128_000_000                                                         # 2026-11-03 00:00 UTC
        w, said = self.notes_watcher(lambda tf: self.rows()[tf])
        w.state["trend_seen"] = {"1d": 0, "4h": 0}                                     # D out of the way
        LW.Watcher.TREND_TFS, keep = (), LW.Watcher.TREND_TFS
        try:
            self.assertEqual(w.candle_notes(day + 3 * 60_000), [])                     # 08:03 Beijing: not yet
            self.assertEqual(w.candle_notes(day + 6 * 60_000), ["morning"])
            self.assertIn("☀️ Morning candle report", said[0])
            self.assertEqual(w.candle_notes(day + 30 * 60_000), [])                    # once a day
            w.state["morning_day"] = None
            self.assertEqual(w.candle_notes(day + 3 * 3_600_000), [])                  # 11:00 Beijing: too late
            w.state["morning_on"] = False
            self.assertEqual(w.candle_notes(day + 6 * 60_000), [])                     # /morning off
        finally:
            LW.Watcher.TREND_TFS = keep

    def test_trend_change_note(self):                                                  # D
        H4 = 4 * 3_600_000
        t0 = 1_762_128_000_000                                                          # a 4H close
        colours = {"v": [(1, 0.9), (1, 0.9), (1, 0.9)]}                                 # 3 red

        def rows(tf):
            if tf != "4h":
                raise RuntimeError("only 4H in this test")
            base = now["t"] // H4 * H4 - 3 * H4
            return [(base + i * H4, o, o, c, c, True) for i, (o, c) in enumerate(colours["v"])] + \
                [(base + 3 * H4, 1, 1, 1, 1, False)]
        now = {"t": t0 + 2 * 60_000}
        w, said = self.notes_watcher(rows, dict(morning_on=False))
        w.candle_notes(now["t"])
        self.assertEqual((w.state["trend_last"]["4h"], said), ("bear", []))           # first close: remembered only
        w.candle_notes(now["t"] + 60_000)
        self.assertEqual(said, [])                                                      # the same close: nothing
        colours["v"] = [(1, 0.9), (1, 1.1), (1, 1.1)]                                   # 2 of 3 green
        now["t"] = t0 + H4 + 2 * 60_000
        self.assertEqual(w.candle_notes(now["t"]), ["4h"])
        self.assertIn("🔴 BEAR → 🟢 BULL", said[0])
        colours["v"] = [(1, 1.1), (1, 1.1), (1, 0.9)]
        now["t"] = t0 + 2 * H4 + 30_000                                                 # under a minute after the close
        self.assertEqual(w.candle_notes(now["t"]), [])
        now["t"] = t0 + 2 * H4 + 2 * 60_000
        w.state["trend_alert_on"] = False
        self.assertEqual(w.candle_notes(now["t"]), [])                                  # /trendalert off: still bull
        self.assertEqual(w.state["trend_last"]["4h"], "bull")

    def test_commands(self):
        w, _ = self.notes_watcher(lambda tf: [])
        self.assertIn("is now <b>OFF</b>", LW.Watcher.command(w, "morning", "off", self.T))
        self.assertFalse(w.state["morning_on"])
        self.assertIn("<b>ON</b>", LW.Watcher.command(w, "trendalert", "", self.T))
        for c in ("/morning on|off", "/trendalert on|off"):
            self.assertIn(c, lv.HELP)
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn("self.candle_notes(self.now_fn())", src)

    def test_watcher_command(self):
        class Feed:
            name = "fake"

            def recent(s, coin, tf, n=3):
                assert n == wx.TREND_N[tf] + 1                         # the closed candles + the live one
                return self.rows()[tf]
        w = types.SimpleNamespace(cfg=dict(universe=dict(own_coins=["BTC", "ETH"])), feed=Feed())
        t = LW.Watcher.candles_now(w, self.T, dict(verdict=dict(title="Choppy - stay out")))
        self.assertIn("📊 <b>BTC", t)
        self.assertIn("<code>ETH </code>", t)
        self.assertIn("🧠 Strategy alerts: Choppy - stay out", t)

        class Down:
            name = "down"

            def recent(s, coin, tf, n=3):
                raise RuntimeError("OKX request failed")
        self.assertIsNone(LW.Watcher.candles_now(types.SimpleNamespace(cfg=w.cfg, feed=Down()), self.T))
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn("live = self.candles_now(now_ms, w)", src)
        self.assertIn("return live or lv.weather_text(w, now_ms)", src)
        self.assertIn("/weather - the candles right now", lv.HELP)


def weather(perm_btc="NO TRADE", blackout=None, events=None):
    regs = {"BTC": regime(perm_btc, "WEAK_BULL", "TRANSITION", "WEAK_BEAR"), "ETH": regime("LONG allowed"),
            "SOL": regime("NO TRADE", "WEAK_BULL", "RANGE", "RANGE")}
    # seeds 4 / 5: sideways daily charts (2026-11-03: a trending daily chart now names the verdict - DailyTrend)
    return wx.build(NOW, regs, {"BTC": daily(seed=4), "ETH": daily(seed=5)}, {}, {"BTC": dict(change_24h=-2.0),
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
