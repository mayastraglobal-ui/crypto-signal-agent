"""Email redesign tests: no markdown symbols, subjects <= 70 characters, every template renders with missing values,
HTML + text parts, numbers taken from the engine files, links to real pages, the Email summary block and its guard,
the 'failed twice in a row' rule.

Run:  python -m unittest tests.test_email_design -v
"""
import datetime as dt
import email
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import notify  # noqa: E402
from engine import brain  # noqa: E402
from engine import btcharts  # noqa: E402
from engine import emails as em  # noqa: E402
from engine import mailfacts as mf  # noqa: E402
from engine import mailkit as mk  # noqa: E402
from engine import mdpage  # noqa: E402
from engine import summary as esum  # noqa: E402

NOW = dt.datetime(2026, 9, 26, 1, 7, tzinfo=dt.timezone.utc)
PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 64


def entry_card(**kw):
    e = dict(coin="BTC", quote="USDT", direction="LONG", market="spot", tf="1h", strategy="S6-OB-FVG", version="1.0",
             utc="2026-09-26 01:07", valid_until_utc="2026-09-26 02:00", entry=83950.0, entry_zone=[83850.0, 84050.0],
             stop=83300.0, targets=[dict(price=85250.0, r=2.0, close_pct=50), dict(price=85900.0, r=3.0, close_pct=50)],
             size=dict(qty=0.0077, usdt=646.0, risk_usdt=5.0, risk_pct=0.5), account=1000, data_state="GOOD",
             why=["Trend: higher timeframe up, regime WEAK_BULL (allowed for this strategy)",
                  "Structure: swing structure up, break of structure up 2 candle(s) ago",
                  "Momentum and volume: RSI(14) 58.1"],
             backtest=dict(trades=412, avg_r=0.18, streak95=9), checks=dict(open=1, max_open=3, no_event=True, risk_ok=True),
             live_chart=em.tradingview("BTC", "USDT", "1h"),
             backtest_chart=btcharts.page_url("https://o.github.io/r/", "S6-OB-FVG", "1.0", "1h", "BTC"))
    e.update(kw)
    return e


def update_x(**kw):
    x = dict(coin="BTC", quote="USDT", direction="LONG", tf="1h", strategy="S", version="1.0", kind="TP1_HIT",
             utc="2026-09-26 03:07", entry=83950.0, stop_now=83950.0, targets=[85250.0, 85900.0], tp_split=[50, 50],
             tp1_r=2.0, price_now=85260.0, entered_utc="2026-09-26 01:12", open=1, max_open=3, day_r=2.0, week_r=2.0,
             live_chart="https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval=60")
    x.update(kw)
    return x


def rep_file():
    return dict(generated_utc="2026-09-26 01:07", signals=[],
                position_book=dict(heat=1, limits=dict(heat=3), day_r=0.5, week_r=-1.25, active=[], awaiting=[],
                                   closed_today=[dict(live=True, state="CLOSED", result_r=1.5, reason="TP2"),
                                                 dict(live=True, state="CLOSED", result_r=-1.0, reason="SL"),
                                                 dict(live=False, state="CLOSED", result_r=2.0, reason="TP2"),
                                                 dict(live=True, state="EXPIRED", result_r=None, reason="EXPIRED")]),
                data_quality=dict(system_state="GOOD"),
                risk=dict(upcoming_events=[dict(start_utc="2026-09-30 12:30", end_utc="2026-09-30 12:30", type="PCE",
                                                name="US PCE / Personal Income and Outlays (Aug data)")],
                          halts=[], blackout_now=[]),
                daily=dict(matrix=[dict(coin="BTC", price=84571.2, regimes=["TRANSITION", "WEAK_BULL", "RANGE", "RANGE"],
                                        mom_30m="+0.4% ROC", move_30m=0.4),
                                   dict(coin="SUI", price=1.1467, regimes=["RANGE", "EXPANSION", "UNCLEAR", "RANGE"],
                                        mom_30m="-2.1% ROC")]),
                universe=dict(signal=["BTC", "SUI"]))


def all_mails(empty=False):
    """Every template, with full inputs or with (almost) everything missing."""
    if empty:
        return [em.entry(dict(coin="BTC", direction="SHORT", tf="1h", strategy="S", version="1.0", entry=1.0,
                              entry_zone=[1.0, 1.0], stop=1.0)),
                em.update(dict(coin="BTC", direction="LONG", tf="1h", kind="CLOSED", close_reason="SL")),
                em.update(dict(coin="BTC", direction="LONG", tf="1h", kind="TP1_HIT")),
                em.update(dict(coin="BTC", direction="LONG", tf="1h", kind="CANCELLED")),
                em.action(dict(what="scan")), em.fixed(dict(what="research")),
                em.notice(dict(title="x", subject=["x"])),
                em.briefing(dict(slot="08:20")), em.daily(dict()), em.weekly(dict(week_no=39))]
    rep = rep_file()
    brief = mf.briefing(rep, "08:20", "2026-09-26 00:40", dict(headline="Nothing to trade. Wait.", sub="BTC is flat.",
                                                              do="Wait for a LIVE email.", dont="Don't chase SUI."),
                        "https://o.github.io/r/claude/briefings/2026-09-26-0820.html", "https://o.github.io/r/")
    return [em.entry(entry_card()), em.entry(entry_card(direction="SHORT", stop=84600.0,
                                                        targets=[dict(price=82650.0, r=2.0, close_pct=100)])),
            em.update(update_x()), em.update(update_x(kind="CLOSED", close_reason="SL", result_r=-1.0)),
            em.update(update_x(kind="CLOSED", close_reason="TIME", result_r=0.4)),
            em.update(update_x(kind="CLOSED", close_reason="TP2", result_r=2.4)),
            em.update(update_x(kind="CANCELLED", cancel_reason="no 5m confirmation")),
            em.action(dict(what="scan", times_utc=["2026-09-26 02:07", "2026-09-26 03:07"], run_url="https://x/1")),
            em.fixed(dict(what="brain", run_url="https://x/2")), em.briefing(brief),
            em.daily(dict(date="2026-09-26", counts=dict(backtests=516, per_coin={"BTC": 52}, strategies=22, tests=52,
                                                        tests_per_coin=52, coins=10),
                          ideas=[dict(name="R4-BBRSI v1.0 · 1h", what="Buy oversold closes.", source="FREQTRADE",
                                      status="TESTING")], closest=[("S v1.0 4h", "+0.05R of +0.10R", 0.5, "needs +0.05R per trade")],
                          summary=dict(lesson="Low volume breakouts fail.", tomorrow="Watch the PCE release."))),
            em.weekly(dict(week_no=39, counts=dict(backtests=3540, strategies=22), passed=0, close=1,
                           ideas_by_source={"RESEARCH": 3, "FREQTRADE": 2}, decision=[dict(cell="S v1.0 4h",
                                                                                          pack_url="https://x/p")]))]


def visible(html):
    """The text a reader sees (tags, styles and link targets removed)."""
    s = re.sub(r"<style.*?</style>", "", html, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"&#?\w+;", " ", s)


class Design(unittest.TestCase):
    def test_no_markdown_symbols_anywhere(self):
        for m in all_mails() + all_mails(True):
            for part in (re.sub(r"https?://\S+", "", m["text"]), visible(m["html"])):
                for sym in ("#", "**", "```", "`", "__"):
                    self.assertNotIn(sym, part, (m["subject"], sym))
            self.assertNotIn("#", m["subject"])

    def test_subjects_short(self):
        for m in all_mails() + all_mails(True):
            self.assertLessEqual(len(m["subject"]), 70, m["subject"])
            self.assertTrue(m["subject"].strip())
        long = em.entry(entry_card(coin="VERYLONGCOINNAME", entry_zone=[0.000012345, 0.000012399], stop=0.0000119))
        self.assertLessEqual(len(long["subject"]), 70)

    def test_spec_subjects(self):
        m = all_mails()
        self.assertEqual(m[0]["subject"], "▲ LONG BTC · 1H · Enter 83,850–84,050 · Stop 83,300")
        self.assertTrue(m[1]["subject"].startswith("▼ SHORT BTC · 1H"))
        self.assertEqual(m[2]["subject"], "✓ TP1 hit · BTC LONG +2.0R · move stop to entry")
        self.assertEqual(m[3]["subject"], "✕ Stop hit · BTC LONG −1.0R · trade closed")
        self.assertTrue(m[4]["subject"].startswith("⏱ Time exit · BTC LONG +0.4R"))
        self.assertEqual(m[5]["subject"], "✓ TP2 hit · BTC LONG +2.4R · trade closed")
        self.assertEqual(m[6]["subject"], "⊘ Cancelled · BTC LONG · no 5m confirmation")
        self.assertEqual(m[7]["subject"], "! Action needed · hourly scan failed 2× in a row")
        self.assertEqual(m[9]["subject"], "08:20 · Busy · 0 signals · Next: US PCE Wed 20:30")
        self.assertEqual(m[10]["subject"], "Daily · 0 trades · 516 backtests · 1 new idea")
        self.assertEqual(m[11]["subject"], "Week 39 · 3,540 backtests · 5 new ideas · 0 passed")

    def test_missing_values_show_a_dash_never_a_guess(self):
        for m in all_mails(True):
            self.assertIn("<!DOCTYPE html>", m["html"])
            self.assertIsNone(re.search(r"\bNone\b(?! today| this week)", m["text"]))
            self.assertNotIn("nan", m["text"].lower().replace("financial", ""))
        self.assertIn("–", em.daily(dict())["text"])
        self.assertIn("Backtest: – trades", em.entry(entry_card(backtest={}))["text"])

    def test_html_is_phone_and_gmail_safe(self):
        for m in all_mails():
            h = m["html"]
            self.assertIn("max-width:600px", h)
            self.assertNotIn("<script", h.lower())
            self.assertNotIn("<link", h.lower())
            self.assertNotIn("@import", h)
            self.assertNotIn("<style", h.lower())                     # inline CSS only
            imgs = re.findall(r"<img[^>]*src=\"([^\"]+)\"", h)
            self.assertTrue(all(x == "cid:chart" for x in imgs))     # only the chart image, from the attachment
        self.assertIn("cid:chart", em.entry(entry_card(chart_cid="chart"))["html"])

    def test_entry_content(self):
        t = em.entry(entry_card())["text"]
        for part in ("ENTRY SIGNAL · LIVE", "26 Sep · 09:07 Beijing", "▲ LONG BTC", "BTC/USDT · 1H · Spot · S6-OB-FVG v1.0",
                     "Valid until 10:00", "Stop-loss  | 83,300", "−0.77% · −1R", "Exit everything if hit",
                     "+1.55% · +2.0R", "Close 50%, move stop to entry", "Close the rest",
                     "Your size (1,000 USDT account): 0.0077 BTC ≈ 646 USDT", "Loss if stopped: 5.00 USDT (0.5%)",
                     "WHY (3 REASONS)", "Backtest: 412 trades, average +0.18R per trade after fees, 95% worst losing "
                     "streak 9 trades", "✓ No big news ±60 min", "✓ Data OK", "✓ Open trades 1 / 3",
                     "✓ Risk manager: go", "Skip this signal if price has already left the entry zone"):
            self.assertIn(part, t)
        self.assertEqual(t.count("\n  1. "), 1)
        self.assertNotIn("  4. ", t)                                         # at most 3 reasons
        s = em.entry(entry_card(direction="SHORT", stop=84600.0, targets=[dict(price=82650.0, r=2.0, close_pct=100)]))
        self.assertIn("Futures only", s["text"])
        self.assertIn("Sell only inside this zone", s["text"])
        c = em.entry(entry_card(why=["Trend: up", "Structure: x", "Caution: late in the session"]))["text"]
        self.assertIn("Caution: late in the session", c)                    # a caution is never cut
        self.assertIn("! Big news within 60 min", em.entry(entry_card(checks=dict(no_event=False, open=3,
                                                                                   max_open=3)))["text"])

    def test_update_content(self):
        t = em.update(update_x())["text"]
        for part in ("TRADE UPDATE · LIVE", "✓ TP1 HIT   +2.0R", "BTC LONG · 1H · entered 09:12",
                     "1. Close 50% at 85,250", "2. Move stop to 83,950 (your entry)", "Next target: 85,900 (+0.75%)",
                     "Open trades 1 / 3 · Today +2.0R · This week +2.0R"):
            self.assertIn(part, t)
        self.assertIn("Nothing to do – the trade is closed.",
                      em.update(update_x(kind="CLOSED", close_reason="SL", result_r=-1.0))["text"])
        self.assertIn("Close what is left", em.update(update_x(kind="CLOSED", close_reason="TIME", result_r=0.4))["text"])
        risk_free = [m["text"] + m["html"] for m in all_mails()]
        self.assertFalse(any(re.search(r"risk[- ]free", x, re.I) for x in risk_free))   # no profit promise

    def test_mime_parts_and_inline_chart(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        with open(os.path.join(tmp, "c.png"), "wb") as f:
            f.write(PNG)
        m = em.entry(entry_card(chart_cid="chart"))
        with mock.patch.object(notify, "ROOT", tmp):
            msg = notify.build_message(dict(m, chart="c.png"), "a@b.c", "a@b.c")
        parsed = email.message_from_bytes(msg.as_bytes())
        types = [p.get_content_type() for p in parsed.walk()]
        self.assertEqual(types[0], "multipart/alternative")
        self.assertIn("text/plain", types)
        self.assertIn("text/html", types)
        self.assertIn("image/png", types)
        img = next(p for p in parsed.walk() if p.get_content_type() == "image/png")
        self.assertEqual(img["Content-ID"], "<chart>")
        plain = email.message_from_bytes(notify.build_message(em.action(dict(what="scan")), "a@b.c", "a@b.c").as_bytes())
        self.assertEqual(sorted(p.get_content_type() for p in plain.walk()),
                         ["multipart/alternative", "text/html", "text/plain"])


class Numbers(unittest.TestCase):
    """The emails show the engine files' numbers."""

    def test_briefing_from_latest_json(self):
        rep = rep_file()
        b = mf.briefing(rep, "08:20", "2026-09-26 00:40", None, None, "https://d/")
        self.assertEqual([c["price"] for c in b["coins"]], [84571.2, 1.1467])
        self.assertEqual([c["move_30m"] for c in b["coins"]], [0.4, -2.1])          # the old string is read too
        self.assertEqual((b["open"], b["max_open"], b["signals"]), (1, 3, 0))
        t = em.briefing(b)["text"]
        self.assertIn("BTC  | 84,571 | ▲ Up", t)
        self.assertIn("SUI  | 1.1467 | ⚡ Fast move | −2.1%", t)
        self.assertIn("Open trades: 1 / 3", t)
        self.assertIn("Wed 30 · 20:30 | US PCE", t)
        self.assertIn("Claude's summary is missing", t)
        self.assertEqual(em.mood(b), "Busy")                                        # 1 open trade
        self.assertEqual(em.mood(dict(b, open=0)), "Calm")
        self.assertEqual(em.mood(dict(b, data_state="DEGRADED")), "Risk-off")
        self.assertEqual(em.mood(dict(b, coins=[dict(move_30m=3.2)])), "Volatile")
        self.assertEqual(em.mood(dict(b, signals=1)), "Busy")
        self.assertEqual(em.market_bias([dict(regime_1d="WEAK_BULL")] * 4 + [dict(regime_1d="RANGE")] * 3), "▲ Up bias")
        self.assertEqual(em.market_bias([dict(regime_1d="WEAK_BULL")] * 3 + [dict(regime_1d="BEAR")] * 4), "▼ Down bias")

    def test_daily_from_the_files(self):
        rep = rep_file()
        hist = [dict(date="2026-09-25", backtests=500, per_coin={"BTC": 50}, strategies=21, tests=50, tests_per_coin=50,
                     coins=1), dict(date="2026-09-26", backtests=516, per_coin={"BTC": 52, "SUI": 52, "ADA": 40},
                                    strategies=22, tests=52, tests_per_coin=52, coins=3)]
        lab = [dict(id="R4-BBRSI", version="1.0", added="2026-09-26", factory="literature", timeframes=["1h"],
                    source="R4 freqtrade-strategies", description="Buy oversold closes."),
               dict(id="X", version="1.1", added="2026-09-26", factory="failure", timeframes=["4h"], hypothesis="h"),
               dict(id="OLD", version="1.0", added="2026-09-20", factory="variant_search")]
        research = dict(cells={"X@1.1|4h": dict(strategy="X", version="1.1", tf="4h", status="FAILED")})
        lessons = "### a\n- timestamp: 2026-09-26 15:40 UTC · source: x\n### b\n- timestamp: 2026-09-25 15:40 UTC\n"
        d = mf.daily(rep, research, hist, lab, lessons, "", "2026-09-26", "2026-09-26 15:50", None, None, "https://d/")
        self.assertEqual(d["counts"]["backtests"], 516)
        self.assertEqual([t["result_r"] for t in d["trades"]], [1.5, -1.0])            # live closed only
        self.assertEqual(d["lessons_added"], 1)
        self.assertEqual([(i["source"], i["status"]) for i in d["ideas"]], [("FREQTRADE", "TESTING"),
                                                                            ("LOSS PATTERN", "FAILED")])
        t = em.daily(d)["text"]
        for part in ("2 trades today. 516 backtests, 2 new ideas, 1 lesson.", "Win / loss: 1 / 1", "Day result: +0.5R",
                     "Backtests: 516", "Strategies: 22", "Coins: 3", "22 strategies × their timeframes = 52 tests per coin",
                     "● BTC 52", "● SUI 52", "○ ADA 40", "R4-BBRSI v1.0 · 1h [FREQTRADE · TESTING] - Buy oversold closes."):
            self.assertIn(part, t)
        self.assertLess(t.index("● BTC"), t.index("○ ADA"))                           # signal coins first

    def test_status_chips(self):
        self.assertEqual(em.status_chip(["BACKTESTING", "VALIDATION"]), "PASSED")
        self.assertEqual(em.status_chip(["PAPER_TRADING"]), "PASSED")
        self.assertEqual(em.status_chip(["FAILED", "BIASED"]), "FAILED")
        self.assertEqual(em.status_chip(["FAILED", "BACKTESTING"]), "TESTING")
        self.assertEqual(em.status_chip([]), "TESTING")                               # not tested yet

    def test_closest_to_passing(self):
        cells = {"a": dict(strategy="A", version="1.0", tf="4h", status="BACKTESTING", required_avg_r=0.1,
                           evidence=dict(all=dict(n=80, avg_r=0.05))),
                 "b": dict(strategy="B", version="1.0", tf="1h", status="FAILED", required_avg_r=0.1,
                           evidence=dict(all=dict(n=300, avg_r=-0.2))),
                 "c": dict(strategy="C", version="1.0", tf="1h", status="VALIDATION", required_avg_r=0.1,
                           evidence=dict(all=dict(n=300, avg_r=0.3))),
                 "d": dict(strategy="D", version="1.0", tf="1h", status="FAILED", bias="lookahead", required_avg_r=0.1,
                           evidence=dict(all=dict(n=300, avg_r=0.09)))}
        rows = em.closest(cells)
        self.assertEqual([r[0] for r in rows], ["A v1.0 4h", "B v1.0 1h"])            # passed and BIASED left out
        self.assertEqual(rows[0][1], "+0.05R of +0.10R")
        self.assertAlmostEqual(rows[0][2], 0.5)
        self.assertEqual(rows[0][3], "needs +0.05R per trade")
        self.assertEqual(mf.close_cells(dict(cells=cells)), 1)

    def test_weekly_sums_the_last_7_days(self):
        hist = [dict(date=f"2026-09-{d:02d}", backtests=100 * d, strategies=d, coins=10) for d in range(18, 28)]
        now = dt.datetime(2026, 9, 27, 4, 7, tzinfo=dt.timezone.utc)
        life = ["S6 v1.0 4h: BACKTESTING → VALIDATION (x)", "S7 v1.0 1h: PAPER_TRADING → VALIDATION (x)",
                "S8 v1.0 1h: FORMALIZED → FAILED (x)"]
        research = dict(approval=dict(eligible=[dict(strategy="S6", version="1.0", tf="4h", pack="reports/approval/S6.md")]))
        w = mf.weekly(dict(weekly=dict(card=dict(sources=4, tasks_done=27, tasks_expected=29, data_problems=[]))),
                      research, hist, [], "", life, now, dict(headline="One is close.", sub="Decide below.",
                                                             next="Test the queue.", improvement="Fewer cards."),
                      None, "https://d/", "https://o.github.io/r/", "https://github.com/o/r")
        self.assertEqual(w["counts"]["backtests"], sum(100 * d for d in range(21, 28)))
        self.assertEqual(w["passed"], 1)                                              # a demotion is not a pass
        self.assertEqual(w["decision"][0]["pack_url"], "https://github.com/o/r/blob/main/reports/approval/S6.md")
        self.assertEqual(w["decision"][0]["chart_url"], "https://o.github.io/r/chart.html#s=S6&v=1.0&tf=4h")
        t = em.weekly(w)["text"]
        for part in ("WEEKLY REPORT · WEEK 39  |  21–27 Sep", "Backtests: 16,800", "Approve S6 v1.0 4h for live signals? "
                     "Reply yes or no.", "Research sources read  | 4", "Claude tasks delivered | 27 of 29",
                     "Data sources           | ✓ All OK", "Self-improvement idea  | Fewer cards.", "Test the queue."):
            self.assertIn(part, t)


class Links(unittest.TestCase):
    def test_report_pages_are_where_the_dashboard_writes_them(self):
        import build_dashboard
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        rep, site = os.path.join(tmp, "reports"), os.path.join(tmp, "site")
        for folder, name in (("briefings", "2026-09-26-0820.md"), ("daily", "2026-09-26.md"), ("weekly", "2026-09-27.md"),
                             ("lessons", "2026-09-26.md")):
            os.makedirs(os.path.join(rep, "claude", folder))
            with open(os.path.join(rep, "claude", folder, name), "w") as f:
                f.write("# Title *x*\n\n## Summary\n- one **two** `c` https://example.com\n\n| a | b |\n|---|---|\n| 1 | 2 |\n")
        with mock.patch.object(build_dashboard, "REPORTS", rep), mock.patch.object(build_dashboard, "SITE", site), \
                mock.patch.object(build_dashboard, "ROOT", tmp):
            files = build_dashboard.claude_pages()
        with mock.patch.object(notify, "pages_base", lambda: "https://o.github.io/r/"):
            for rel in ("reports/claude/briefings/2026-09-26-0820.md", "reports/claude/daily/2026-09-26.md",
                        "reports/claude/weekly/2026-09-27.md", "reports/claude/lessons/2026-09-26.md"):
                url = notify.page_url(rel)
                path = url.replace("https://o.github.io/r/", "site/")
                self.assertIn(path, files)
                self.assertTrue(os.path.exists(os.path.join(tmp, path)))
        with open(os.path.join(site, "claude", "daily", "2026-09-26.html")) as f:
            page = f.read()
        self.assertIn("<strong>two</strong>", page)
        self.assertIn('<a href="https://example.com">', page)
        self.assertIn("<table>", page)
        self.assertNotIn("<script", page)

    def test_markdown_page_escapes_html(self):
        h = mdpage.to_html("# x\n<script>alert(1)</script> [a](javascript:alert(1))")
        self.assertNotIn("<script>", h)
        self.assertNotIn('href="javascript', h)

    def test_live_and_backtest_chart_links(self):
        self.assertEqual(em.tradingview("BTC", "USDT", "1h"),
                         "https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval=60")
        self.assertEqual(em.tradingview("SOL", "USDT", "4h", True),
                         "https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT.P&interval=240")
        h = em.entry(entry_card())["html"]
        self.assertIn('href="https://o.github.io/r/chart.html#s=S6-OB-FVG&amp;v=1.0&amp;tf=1h&amp;c=BTC"', h)
        self.assertIn(">Backtest chart</a>", h)
        self.assertNotIn('href=""', "".join(m["html"] for m in all_mails(True)))     # a missing link: no button


class SummaryBlock(unittest.TestCase):
    GOOD = ("# Briefing\n## Summary\nx\n## Email summary\n- headline: Nothing to trade. Wait.\n- sub: BTC is flat.\n"
            "- mood: Calm\n- do: Wait for a LIVE email.\n- don't: Don't chase SUI.\n## Position book\n")

    def test_parse_and_check(self):
        self.assertEqual(esum.parse(self.GOOD), dict(headline="Nothing to trade. Wait.", sub="BTC is flat.", mood="Calm",
                                                     do="Wait for a LIVE email.", dont="Don't chase SUI."))
        self.assertEqual(esum.problems(self.GOOD, "briefing"), [])
        self.assertIsNone(esum.parse("# x\n## Summary\n"))
        bad = self.GOOD.replace("Nothing to trade. Wait.", "one two three four five six seven eight nine")
        self.assertTrue(any("at most 8" in p for p in esum.problems(bad, "briefing")))
        self.assertTrue(any("plain text" in p for p in esum.problems(self.GOOD.replace("BTC is flat.", "**BTC** flat"),
                                                                     "briefing")))
        self.assertTrue(any("mood" in p for p in esum.problems(self.GOOD.replace("Calm", "Happy"), "briefing")))
        self.assertTrue(any("missing" in p for p in esum.problems(self.GOOD.replace("- do: Wait for a LIVE email.\n", ""),
                                                                  "briefing")))
        self.assertTrue(any("no '## Email summary'" in p for p in esum.problems("# x\n", "daily")))
        self.assertEqual(esum.problems("## Email summary\n- lesson: a\n- tomorrow: b\n", "daily"), [])
        self.assertTrue(any("unknown key" in p for p in esum.problems("## Email summary\n- lesson: a\n- tomorrow: b\n"
                                                                      "- color: red\n", "daily")))
        self.assertEqual(esum.kind_of("reports/claude/weekly/2026-09-27.md"), "weekly")

    def test_guard_refuses_a_report_without_the_block(self):
        def change(path, new):
            return dict(path=path, status="A", base=None, new=new)
        briefing = self.GOOD.replace("## Position book\n", "## Bull vs bear\n- Bull case: a\n- Bear case: b\n"
                                     "- Risk manager: no veto\n")
        _, probs, _ = brain.review([change("reports/claude/briefings/2026-09-26-0820.md", briefing)], {})
        self.assertEqual(probs, [])
        _, probs, _ = brain.review([change("reports/claude/daily/2026-09-26.md", "# Daily\n## Summary\nok\n")], {})
        self.assertTrue(any("Email summary" in p for p in probs))
        _, probs, _ = brain.review([change("reports/claude/weekly/2026-09-27.md", "# W\n## Email summary\n- headline: a\n"
                                           "- sub: b\n- next: c\n- improvement: guaranteed profits\n")], {})
        self.assertTrue(any("profit promise" in p for p in probs))                   # the guard's lint covers it too

    def test_tasks_explain_the_block(self):
        with open(os.path.join(ROOT, "tasks", "COMMON.md")) as f:
            common = f.read()
        m = re.search(r"```\n\s*## Email summary\n(.*?)\n\s*```", common, re.S)
        example = "\n".join(ln.strip() for ln in m.group(1).splitlines())
        self.assertEqual(esum.problems("## Email summary\n" + example, "briefing"), [])   # the example passes


class Failures(unittest.TestCase):
    def run_mode(self, runs, mode="failed"):
        sent = []
        with mock.patch.object(notify, "earlier_runs", lambda: runs), \
                mock.patch.object(notify, "send_mail", lambda m: sent.append(m) or True):
            if mode == "recovered":
                notify.recovered_email("scan")
            else:
                notify.failed_email(mode)
        return sent

    def test_one_failure_is_silent_the_second_emails_once(self):
        ok, bad = ("success", "2026-09-26 01:07", "u"), ("failure", "2026-09-26 02:07", "u")
        self.assertEqual(self.run_mode([ok, bad]), [])                                # first failure: silent
        m = self.run_mode([bad, ok])                                                  # second in a row: one email
        self.assertEqual(len(m), 1)
        self.assertIn("hourly scan failed 2× in a row", m[0]["subject"])
        self.assertIn("At 10:07 and", m[0]["text"])
        self.assertEqual(self.run_mode([bad, bad, ok]), [])                          # third: already reported
        self.assertEqual(len(self.run_mode(None)), 1)                                 # GitHub not readable: send
        self.assertIn("daily research run", self.run_mode([bad], "research_failed")[0]["subject"])

    def test_fixed_once_after_a_reported_streak(self):
        ok, bad = ("success", "t", "u"), ("failure", "t", "u")
        self.assertEqual(self.run_mode([ok, bad], "recovered"), [])
        self.assertEqual(self.run_mode([bad, ok], "recovered"), [])                   # 1 failure was never emailed
        m = self.run_mode([bad, bad, ok], "recovered")
        self.assertEqual(len(m), 1)
        self.assertTrue(m[0]["subject"].startswith("✓ Fixed · hourly scan works again"))


class NotifyRun(unittest.TestCase):
    """notify.py as the workflows run it, in a temporary copy (DRY_RUN prints instead of sending)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        for f in ("notify.py", "config.yaml"):
            shutil.copy(os.path.join(ROOT, f), self.tmp)
        shutil.copytree(os.path.join(ROOT, "engine"), os.path.join(self.tmp, "engine"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        os.makedirs(os.path.join(self.tmp, "reports", "claude", "briefings"))
        os.makedirs(os.path.join(self.tmp, "memory"))
        with open(os.path.join(self.tmp, "memory", "beginner_course.md"), "w") as f:
            f.write("# Course\n\n## L01 · What is R\nR is the amount you risk.\n\n## L02 · Stops\nAlways set one.\n")

    def write(self, name, obj):
        with open(os.path.join(self.tmp, "reports", name), "w") as f:
            json.dump(obj, f)

    def run_notify(self, *args):
        env = {k: v for k, v in os.environ.items() if k not in ("GMAIL_USER", "GMAIL_APP_PASSWORD", "GITHUB_RUN_ID")}
        env.update(DRY_RUN="1", GITHUB_REPOSITORY="o/r")
        p = subprocess.run([sys.executable, "notify.py", *args], cwd=self.tmp, env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        return p.stdout

    def subjects(self, out):
        return re.findall(r"Subject: (.*)", out)

    def test_brain_sends_briefing_and_daily_review_once(self):
        rep = rep_file()
        self.write("latest.json", rep)
        rel = "reports/claude/briefings/2026-09-26-0820.md"
        with open(os.path.join(self.tmp, rel), "w") as f:
            f.write(SummaryBlock.GOOD)
        os.makedirs(os.path.join(self.tmp, "reports", "claude", "daily"))
        with open(os.path.join(self.tmp, "reports/claude/daily/2026-09-26.md"), "w") as f:
            f.write("# D\n## Email summary\n- lesson: Low volume breakouts fail.\n- tomorrow: Watch PCE.\n")
        res = os.path.join(self.tmp, "res.json")
        with open(res, "w") as f:
            json.dump([dict(status="applied", branch="claude/brain-briefing", sha="a" * 40, when="2026-09-26 00:40",
                            applied=[rel, "reports/claude/daily/2026-09-26.md"], problems=[])], f)
        out = self.run_notify("brain", res)
        s = self.subjects(out)
        self.assertEqual(s[0], "08:20 · Busy · 0 signals · Next: US PCE Wed 20:30")
        self.assertTrue(s[1].startswith("Daily · 2 trades"))
        self.assertIn("Nothing to trade. Wait.", out)
        self.assertIn("https://o.github.io/r/claude/briefings/2026-09-26-0820.html", out)
        self.assertIn("Low volume breakouts fail.", out)
        self.assertIn("Beginner lesson: https://o.github.io/r/claude/lessons/2026-09-26.html", out)
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "reports/claude/lessons/2026-09-26.md")))
        with open(os.path.join(self.tmp, "reports", "curriculum_sent.json")) as f:
            self.assertEqual(json.load(f), ["L01"])
        self.assertEqual(self.subjects(self.run_notify("brain", res)), [])            # only once

    def test_fallbacks_only_when_claude_is_missing_and_only_once(self):
        rep = rep_file()
        self.write("latest.json", rep)                                                # 01:07 UTC = 09:07 Beijing
        s = self.subjects(self.run_notify("daily"))
        self.assertEqual(s, ["08:20 · Busy · 0 signals · Next: US PCE Wed 20:30"])
        self.assertEqual(self.subjects(self.run_notify("daily")), [])
        self.write("latest.json", dict(rep, generated_utc="2026-09-26 18:07"))
        s = self.subjects(self.run_notify("daily"))
        self.assertEqual(len(s), 1)
        self.assertTrue(s[0].startswith("Daily · "))
        self.write("latest.json", dict(rep, generated_utc="2026-09-27 01:07"))
        with open(os.path.join(self.tmp, "reports/claude/briefings/2026-09-27-0820.md"), "w") as f:
            f.write("# x\n")
        self.assertEqual(self.subjects(self.run_notify("daily")), [])                 # Claude's briefing is there

    def test_signals_new_and_old_email_blocks(self):
        m = em.entry(entry_card())
        self.write("latest.json", dict(rep_file(), signals=[dict(coin="BTC", timeframe="1h", strategy="S",
                                                                 signal_time_utc="t", email=m)],
                                       email_events=[dict(key="k", subject="[EXIT] old", lines=["**x**", "y"])],
                                       email_settings={}))
        out = self.run_notify()
        self.assertEqual(self.subjects(out), [m["subject"], "[EXIT] old"])
        self.assertNotIn("**", out)
        self.assertEqual(self.subjects(self.run_notify()), [])

    def test_samples_are_marked_test(self):
        self.write("latest.json", rep_file())
        out = self.run_notify("samples")
        s = self.subjects(out)
        self.assertEqual(len(s), 7)
        self.assertTrue(all(x.startswith("TEST · ") for x in s))
        self.assertEqual(out.count("the trade numbers are EXAMPLES"), 7)
        self.assertIn("EXAMPLE v1.0", out)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "reports", "curriculum_sent.json")))  # nothing moved on


class ResearchCounts(unittest.TestCase):
    def test_counts_and_history(self):
        import research
        started = dt.datetime(2026, 9, 26, 0, 40, tzinfo=dt.timezone.utc)
        c = research.run_counts(started, {"BTC": 52, "ADA": 40}, [1, 2, 3], {("a", "1", "1h"): 1, ("b", "1", "4h"): 1},
                                [dict(id="V", version="1.1", added="2026-09-26", factory="variant_search",
                                      timeframes=["4h"], description="d"), dict(id="O", added="2026-09-20")],
                                {"V@1.1|4h": dict(strategy="V", version="1.1", status="BACKTESTING")})
        self.assertEqual((c["backtests"], c["coins"], c["strategies"], c["tests"], c["tests_per_coin"]), (92, 2, 3, 2, 52))
        self.assertEqual([x["id"] for x in c["new_cards"]], ["V"])
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        with mock.patch.object(research.sc, "REPORTS", tmp):
            research.save_counts(c, False)
            research.save_counts(dict(c, backtests=93), False)                        # a re-run the same day replaces
            with open(os.path.join(tmp, "research_counts.json")) as f:
                hist = json.load(f)
        self.assertEqual(len(hist), 1)
        self.assertEqual(hist[0]["backtests"], 93)
        self.assertEqual(hist[0]["new_cards"], 1)


if __name__ == "__main__":
    unittest.main()
