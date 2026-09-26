"""Email format v2 tests: every template (A-K) renders with missing values, subjects <= 70 characters starting with the
type word, a type pill first, an ACTION box in every email, PAPER emails never look LIVE, no markdown symbols, HTML +
text parts, updates are replies in their entry's thread, numbers taken from the engine files, the changes-only
briefing, the alert registry (one ALERT per problem, one FIXED), the watchdog, links to real pages, the Email summary
block and its guard, the 'failed twice in a row' rule.

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
             live=dict(n=6, total_r=2.4), live_chart=em.tradingview("BTC", "USDT", "1h"),
             backtest_chart=btcharts.page_url("https://o.github.io/r/", "S6-OB-FVG", "1.0", "1h", "BTC"))
    e.update(kw)
    return e


PAPER = dict(number=4, needed=20, closed=3, won=2, total_r=2.2, avg_r=0.73, bt_avg_r=0.12, max_div=0.3)


def paper_card(**kw):
    return entry_card(**dict(dict(stage="PAPER_TRADING", paper=PAPER, journal_url="https://o.github.io/r/"), **kw))


def update_x(**kw):
    x = dict(coin="BTC", quote="USDT", direction="LONG", tf="1h", strategy="S", version="1.0", kind="TP1_HIT",
             utc="2026-09-26 03:42", entry=83950.0, stop_now=83950.0, targets=[85250.0, 85900.0], tp_split=[50, 50],
             tp1_r=2.0, price_now=85310.0, signal_utc="2026-09-26 01:07", entered_utc="2026-09-26 01:12",
             entry_zone=[83850.0, 84050.0], risk_usdt=5.0, risk_pct=0.5, open=1, max_open=3, day_r=1.0, week_r=1.0,
             live_chart="https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval=60")
    x.update(kw)
    return x


def stop_x(**kw):
    return update_x(**dict(dict(coin="SOL", direction="SHORT", kind="CLOSED", close_reason="SL", result_r=-1.0,
                                entry=122.30, exit_price=124.10, utc="2026-09-26 07:48", entered_utc="2026-09-26 05:05",
                                tag="trend reversal", record=dict(n=9, won=5, total_r=2.1, streak=1, bt_streak=5)), **kw))


def rep_file():
    return dict(generated_utc="2026-09-26 01:07", signals=[],
                market=dict(btc_trend={"1d": "UP", "4h": "UP"}, fear_greed=dict(value=74, label="Greed", yesterday=71)),
                position_book=dict(heat=1, limits=dict(heat=3), day_r=0.5, week_r=-1.25, active=[], awaiting=[],
                                   closed_today=[dict(live=True, state="CLOSED", result_r=1.5, reason="TP2"),
                                                 dict(live=True, state="CLOSED", result_r=-1.0, reason="SL"),
                                                 dict(live=False, state="CLOSED", result_r=2.0, reason="TP2"),
                                                 dict(live=True, state="EXPIRED", result_r=None, reason="EXPIRED")]),
                data_quality=dict(system_state="GOOD", coins={"BTC": dict(state="GOOD"), "VTHO": dict(state="UNSAFE")}),
                risk=dict(upcoming_events=[dict(start_utc="2026-09-30 12:30", end_utc="2026-09-30 12:30", type="PCE",
                                                name="US PCE / Personal Income and Outlays (Aug data)")],
                          halts=[], blackout_now=[]),
                daily=dict(matrix=[dict(coin="BTC", price=84571.2, regimes=["TRANSITION", "WEAK_BULL", "RANGE", "RANGE"],
                                        mom_30m="+0.4% ROC", move_30m=0.4),
                                   dict(coin="SUI", price=1.1467, regimes=["RANGE", "EXPANSION", "UNCLEAR", "RANGE"],
                                        mom_30m="-2.1% ROC"),
                                   dict(coin="ADA", price=0.61, regimes=["RANGE", "RANGE", "RANGE", "RANGE"])]),
                universe=dict(signal=["BTC", "SUI"], candidates=[dict(coin="BTC", change_24h=1.374),
                                                                 dict(coin="SUI", change_24h=-2.5)]))


REGISTRY = ("id,version,tf,status,bias\nA,1.0,4h,FAILED,\nA,1.0,4h,BACKTESTING,\nB,1.0,1h,FAILED,\nC,1.0,1h,PAPER_TRADING,\n"
            "D,1.0,1h,APPROVED,\nE,1.0,1h,VALIDATION,\nF,1.0,1h,BACKTESTING,lookahead\n")
CELLS = {"a": dict(strategy="A", version="1.0", tf="4h", status="BACKTESTING", required_avg_r=0.1,
                   evidence=dict(all=dict(n=80, avg_r=0.05)))}


def all_mails(empty=False):
    """Every template (A-K), with full inputs or with (almost) everything missing: (letter, email)."""
    if empty:
        mini = dict(coin="BTC", direction="SHORT", tf="1h", strategy="S", version="1.0", entry=1.0, entry_zone=[1.0, 1.0],
                    stop=1.0)
        return [("A", em.live_entry(mini)),
                ("B", em.live_update(dict(coin="BTC", direction="LONG", tf="1h", kind="CLOSED", close_reason="SL"))),
                ("B", em.live_update(dict(coin="BTC", direction="LONG", tf="1h", kind="TP1_HIT"))),
                ("B", em.live_update(dict(coin="BTC", direction="LONG", tf="1h", kind="CANCELLED"))),
                ("B", em.live_update(dict(coin="BTC", direction="LONG", tf="1h", kind="FILLED"))),
                ("B", em.live_update(dict(coin="BTC", direction="LONG", tf="1h", kind="WARNING"))),
                ("C", em.paper_signal(dict(mini, stage="PAPER_TRADING"))),
                ("D", em.paper_update(dict(coin="BTC", direction="LONG", tf="1h", kind="TP1_HIT", stage="PAPER_TRADING"))),
                ("E", em.paper_complete(dict(strategy="S", version="1.0", tf="4h"))),
                ("F", em.alert(dict(title="x"))), ("G", em.fixed(dict())),
                ("H", em.briefing(dict(slot="08:20"))), ("I", em.changes(dict(slot="14:20"))),
                ("J", em.daily(dict())), ("K", em.weekly(dict(week_no=39)))]
    rep = rep_file()
    brief = mf.briefing(rep, "08:20", "2026-09-26 00:40", dict(headline="Nothing to trade. Wait.", sub="BTC is flat.",
                                                              do="Wait for a LIVE email.", dont="Don't chase SUI."),
                        "https://o.github.io/r/claude/briefings/2026-09-26-0820.html", "https://o.github.io/r/",
                        dict(cells=CELLS), REGISTRY, [dict(date="2026-09-26", backtests=460, coins=10)], [],
                        "C01 Time Series Momentum")
    return [("A", em.live_entry(entry_card())),
            ("A", em.live_entry(entry_card(direction="SHORT", stop=84600.0,
                                           targets=[dict(price=82650.0, r=2.0, close_pct=100)]))),
            ("B", em.live_update(update_x())), ("B", em.live_update(stop_x())),
            ("B", em.live_update(update_x(kind="CLOSED", close_reason="TIME", result_r=0.4, exit_price=84210.0))),
            ("B", em.live_update(update_x(kind="CLOSED", close_reason="TP2", result_r=2.5, exit_price=85900.0))),
            ("B", em.live_update(update_x(kind="CLOSED", close_reason="BE", result_r=1.0, exit_price=83950.0))),
            ("B", em.live_update(update_x(kind="CANCELLED", cancel_reason="price left the zone"))),
            ("B", em.live_update(update_x(kind="FILLED", stop_now=83300.0))),
            ("B", em.live_update(update_x(kind="WARNING", event=dict(name="US CPI (Aug data)", type="CPI", minutes=30,
                                                                     start_utc="2026-09-26 04:12")))),
            ("C", em.paper_signal(paper_card(coin="ETH", tf="4h"))),
            ("D", em.paper_update(update_x(coin="ETH", tf="4h", stage="PAPER_TRADING", paper=PAPER))),
            ("E", em.paper_complete(dict(strategy="donchian_breakout", version="1.1", tf="4h", utc="2026-09-26 13:05",
                                         results=[2.0, -1.0] * 10, total_r=10.0, passed=True, needed=20,
                                         rows=[("Trades", "20", "1,097", True), ("Win rate", "50%", "54%", None)],
                                         chips=[("All 20 closed and scored", True)], pack_url="https://x/p"))),
            ("F", em.alert(dict(title="Market data unsafe", impact="signals paused", utc="2026-09-26 06:05",
                                auto="signals paused automatically", nothing="The agent paused new signals by itself.",
                                broke="Binance price feed stale for 2 h", impact_long="No new signals.",
                                tried="Refetch 3 times", open_trades="0 / 3", meaning="Prices are old.",
                                buttons=[("Dashboard", "https://o.github.io/r/")]))),
            ("G", em.fixed(dict(thing="market data", title="Market data unsafe", since_utc="2026-09-26 06:05",
                                utc="2026-09-26 07:10", missed=0, cause="Binance feed stale; fixed itself"))),
            ("H", em.briefing(brief)),
            ("I", em.changes(mf.changes(rep, "14:20", "08:20", "2026-09-26 06:20",
                                        [("✓", "donchian_breakout v1.0 4h: FAILED → BACKTESTING"),
                                         ("◆", "New idea in the lab: R4-BBRSI.")], "https://p/"))),
            ("J", em.daily(dict(date="2026-09-26", counts=dict(backtests=460, strategies=20, coins=10),
                                live_trades=[], paper_trades=[], day_r=0.0, week_r=0.0,
                                ideas=[dict(name="R4-BBRSI v1.0 · 1h", what="Buy oversold closes.", source="FREQTRADE",
                                            status="TESTING")], lessons_added=1,
                                closest=[("S v1.0 4h", "+0.05R of +0.10R", 0.5, "needs +0.05R per trade")],
                                health=[("Data GOOD", True), ("Tests red on main", False)],
                                summary=dict(lesson="Low volume breakouts fail.", tomorrow="Watch the PCE release.")))),
            ("K", em.weekly(dict(week_no=39, funnel=dict(TESTED=46, TESTING=13, PAPER=0, APPROVED=0, FAILED=33),
                                 closest=[("donchian_breakout v1.1 4h", "+0.09R of +0.10R", 0.9, "needs +0.01R")],
                                 decision=[dict(cell="S v1.0 4h", pack_url="https://x/p")],
                                 history=[("Sat 26", "Bias check v2 (#31)")], tests="Tests: 566 · ✓ green on main")))]


def visible(html):
    """The text a reader sees (tags, styles and link targets removed)."""
    s = re.sub(r"<style.*?</style>", "", html, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"&#?\w+;", " ", s)


TYPE = {"A": "LIVE ", "B": "LIVE ", "C": "PAPER ", "D": "PAPER ", "E": "PAPER ", "F": "! ", "G": "✓ Fixed",
        "H": "08:20 · ", "I": "14:20 · ", "J": "Daily · ", "K": "Week 39 · "}
PILL = {"A": "LIVE", "B": "LIVE", "C": "PAPER", "D": "PAPER", "E": "PAPER", "F": "ALERT", "G": "FIXED", "H": "BRIEFING",
        "I": "BRIEFING", "J": "DAILY", "K": "WEEKLY"}


class Design(unittest.TestCase):
    """The format v2 rules for every email."""

    def test_no_markdown_symbols_anywhere(self):
        for _, m in all_mails() + all_mails(True):
            for part in (re.sub(r"https?://\S+", "", m["text"]), visible(m["html"])):
                for sym in ("**", "```", "`", "__", "\n#", "# "):
                    self.assertNotIn(sym, part, (m["subject"], sym))

    def test_subjects_short_and_start_with_the_type(self):
        for letter, m in all_mails() + all_mails(True):
            self.assertLessEqual(len(m["subject"]), 70, m["subject"])
            self.assertTrue(m["subject"].startswith(TYPE[letter]), (letter, m["subject"]))
        long = em.live_entry(entry_card(coin="VERYLONGCOINNAME", entry_zone=[0.000012345, 0.000012399], stop=0.0000119))
        self.assertLessEqual(len(long["subject"]), 70)
        self.assertTrue(long["subject"].startswith("LIVE ▲ LONG VERYLONGCOINNAME"))

    def test_type_pill_first_and_action_box_in_every_email(self):
        for letter, m in all_mails() + all_mails(True):
            self.assertEqual(m["pill"], PILL[letter], m["subject"])
            self.assertTrue(m["text"].startswith(f"[{PILL[letter]}] "), m["subject"])
            self.assertTrue(m["has_action"], m["subject"])
            t = m["text"]
            title = re.search(r"^(DO NOW|PRACTICE NOW|ACTION|YOUR DECISION)$", t, re.M)
            self.assertIsNotNone(title, m["subject"])
            body = t[:title.start()]                                   # only the header and the banner come first
            self.assertLessEqual(len([ln for ln in body.splitlines() if ln.strip()]), 6, m["subject"])
        self.assertIn("\nACTION\n  None. No approved strategy yet.", em.briefing(dict(slot="08:20", approved=0))["text"])

    def test_paper_emails_never_look_live(self):
        for letter, m in all_mails() + all_mails(True):
            if letter not in ("C", "D", "E"):
                continue
            self.assertFalse(set(m["tones"]) & set(mk.LIVE_TONES), m["subject"])        # never the LIVE green banner
            self.assertNotIn("LIVE", m["subject"] + m["text"] + visible(m["html"]), m["subject"])
            self.assertIn(f"2px dashed {mk.PAPER_BLUE}", m["html"])                     # the dashed blue card
            self.assertNotIn(f"background:{mk.GREEN};color:#FFFFFF", m["html"].replace(" ", ""))
        for letter, m in all_mails():
            if letter in ("A", "B"):
                self.assertNotIn("dashed", m["html"])

    def test_spec_subjects(self):
        s = [m["subject"] for _, m in all_mails()]
        self.assertEqual(s[0], "LIVE ▲ LONG BTC 1H · Enter 83,850–84,050 · Stop 83,300")
        self.assertTrue(s[1].startswith("LIVE ▼ SHORT BTC 1H"))
        self.assertEqual(s[2], "LIVE ✓ TP1 hit · BTC LONG +2.0R · move stop to entry")
        self.assertEqual(s[3], "LIVE ✕ Stop hit · SOL SHORT −1.0R · trade closed")
        self.assertEqual(s[4], "LIVE ⏱ Time exit · BTC LONG +0.4R · close the rest")
        self.assertEqual(s[5], "LIVE ✓ TP2 hit · BTC LONG +2.5R · trade closed")
        self.assertEqual(s[6], "LIVE = Rest stopped at entry · BTC LONG +1.0R · closed")
        self.assertEqual(s[7], "LIVE ⊘ Cancelled · BTC LONG · price left the zone")
        self.assertEqual(s[8], "LIVE ● Filled · BTC LONG at 83,950 · stop active")
        self.assertEqual(s[9], "LIVE ! Warning · BTC LONG open · US CPI in 30 min")
        self.assertEqual(s[10], "PAPER ▲ LONG ETH 4H · #4 of 20 · practice only")
        self.assertEqual(s[11], "PAPER ✓ TP1 hit · ETH LONG +2.0R · #4 of 20")
        self.assertEqual(s[12], "PAPER ● 20 of 20 done · donchian_breakout 4H +10.0R · your decision")
        self.assertEqual(s[13], "! Market data unsafe · signals paused")
        self.assertEqual(s[14], "✓ Fixed · market data OK · 0 signals missed")
        self.assertEqual(s[15], "08:20 · No trade · BTC up · PCE Wed 20:30")
        self.assertEqual(s[16], "14:20 · 2 changes · still no trade")
        self.assertEqual(s[17], "Daily · 0 trades · 460 backtests · 1 new lesson")
        self.assertEqual(s[18], "Week 39 · 0 approved · closest: donchian_breakout 4H")

    def test_missing_values_show_a_dash_never_a_guess(self):
        for _, m in all_mails(True):
            self.assertIn("<!DOCTYPE html>", m["html"])
            self.assertIsNone(re.search(r"\bNone\b(?![.] | –| this week| today|\.$)", m["text"]), m["subject"])
            self.assertNotIn("nan", m["text"].lower().replace("financial", ""))
        self.assertIn("–", em.daily(dict())["text"])
        self.assertIn("Backtest: – trades", em.live_entry(entry_card(backtest={}))["text"])

    def test_html_and_text_parts_phone_and_gmail_safe(self):
        for _, m in all_mails():
            h = m["html"]
            self.assertTrue(m["text"].strip())
            self.assertIn("max-width:600px", h)
            self.assertNotIn("<script", h.lower())
            self.assertNotIn("<link", h.lower())
            self.assertNotIn("@import", h)
            self.assertNotIn("<style", h.lower())                     # inline CSS only
            imgs = re.findall(r"<img[^>]*src=\"([^\"]+)\"", h)
            self.assertTrue(all(x == "cid:chart" for x in imgs))     # only the chart image, from the attachment
        self.assertIn("cid:chart", em.live_entry(entry_card(chart_cid="chart"))["html"])

    def test_live_entry_content(self):
        t = em.live_entry(entry_card())["text"]
        for part in ("[LIVE] ENTRY SIGNAL  |  26 Sep · 09:07 Beijing", "▲ LONG BTC", "BTC/USDT · 1H · Spot · S6-OB-FVG v1.0",
                     "Valid until 10:00", "DO NOW\n  Place a limit BUY between 83,850 and 84,050. Set the stop at 83,300 "
                     "right away.", "THE PLAN", "Stop  | 83,300 −1R", "Exit everything if hit", "TP1   | 85,250 +2R",
                     "Close 50%, move stop to entry", "TP2   | 85,900 +3R    | Close the rest",
                     "Your size (1,000 USDT account): 0.0077 BTC (≈ 646 USDT)",
                     "Loss if stopped: 5.00 USDT (0.5% of account)",
                     "WHY (3 REASONS)", "Backtest: 412 trades, average +0.18R per trade after fees, 95% worst losing "
                     "streak 9 trades", "✓ No big news ±60 min", "✓ Data OK", "✓ Open trades 1 / 3",
                     "✓ Risk manager: go", "APPROVED · live 6 trades · +2.4R so far",
                     "Skip this signal if price has already left the entry zone"):
            self.assertIn(part, t)
        self.assertNotIn("  4. ", t)                                         # at most 3 reasons
        order = [t.index(x) for x in ("[LIVE]", "▲ LONG BTC", "DO NOW", "THE PLAN", "WHY", "APPROVED · live", "--")]
        self.assertEqual(order, sorted(order))                               # the v2 order
        s = em.live_entry(entry_card(direction="SHORT", stop=84600.0, targets=[dict(price=82650.0, r=2.0, close_pct=100)]))
        self.assertIn("Futures only", s["text"])
        self.assertIn("Sell only inside this zone", s["text"])
        self.assertIn("Place a limit SELL (futures)", s["text"])
        c = em.live_entry(entry_card(why=["Trend: up", "Structure: x", "Caution: late in the session"]))["text"]
        self.assertIn("Caution: late in the session", c)                    # a caution is never cut
        self.assertIn("! Big news within 60 min", em.live_entry(entry_card(checks=dict(no_event=False, open=3,
                                                                                        max_open=3)))["text"])

    def test_live_update_content(self):
        t = em.live_update(update_x())["text"]
        for part in ("[LIVE] TRADE UPDATE", "✓ TP1 HIT   +2.0R", "BTC LONG · 1H · entered 09:12",
                     "1. Close 50% at 85,250.", "2. Move the stop to 83,950 (your entry).",
                     "Next target TP2: 85,900 (+0.69% away)", "THIS TRADE SO FAR", "09:07  Signal sent · entry zone "
                     "83,850–84,050", "09:12  Filled at 83,950", "11:42  TP1 hit at 85,250 · 50% closed",
                     " next  TP2 85,900, or stop at entry (no loss)", "Today +1.0R · Week +1.0R · Open 1 / 3"):
            self.assertIn(part, t)
        s = em.live_update(stop_x())["text"]
        for part in ("✕ STOP HIT   −1.0R", "Nothing. The trade is closed. This was the planned 1R loss.",
                     "Entry: 122.30", "Stopped at: 124.10", "Held: 2 h 43 m", "Result: −5.00 USDT (0.5% of account)",
                     "WHY IT LOST (ENGINE TAG)\ntrend reversal", "Yes. Live 9 trades, 5 won, +2.1R. Losing streak 1 "
                     "(backtest worst: 5)."):
            self.assertIn(part, s)
        self.assertIn("Watch it.", em.live_update(stop_x(record=dict(n=9, won=2, total_r=-4.0, streak=6, bt_streak=5)))
                      ["text"])
        self.assertIn("Close the rest at the market price",
                      em.live_update(update_x(kind="CLOSED", close_reason="TIME", result_r=0.4))["text"])
        self.assertIn("Cancel your limit order. Do not enter.", em.live_update(update_x(kind="CANCELLED"))["text"])
        self.assertIn("Nothing. Check the stop is set at 83,300.",
                      em.live_update(update_x(kind="FILLED", stop_now=83300.0))["text"])
        risk_free = [m["text"] + m["html"] for _, m in all_mails()]
        self.assertFalse(any(re.search(r"risk[- ]free", x, re.I) for x in risk_free))   # no profit promise

    def test_paper_content(self):
        t = em.paper_signal(paper_card(coin="ETH", tf="4h"))["text"]
        for part in ("[PAPER] PRACTICE SIGNAL", "PRACTICE ONLY – DO NOT USE REAL MONEY", "PRACTICE NOW",
                     "1. Write it in your paper journal", "2. Watch the chart. Would you have entered?",
                     "| On paper", "ROAD TO REAL MONEY", "Paper signal 4 of 20  (16 to go)",
                     "Paper so far 3 · 2 won · +2.2R", "Backtest expects +0.12R per trade. Paper averages +0.73R per "
                     "trade. Paper is on track.", "Open chart: https://www.tradingview.com", "Paper journal: https://o"):
            self.assertIn(part, t)
        for word in ("Your size", "Loss if stopped", "USDT account"):
            self.assertNotIn(word, t)                                        # practice: no money boxes
        self.assertIn("Paper is behind.", em.paper_signal(paper_card(paper=dict(PAPER, avg_r=-0.3)))["text"])
        self.assertIn("No paper trade closed yet.", em.paper_signal(paper_card(paper=dict(PAPER, closed=0)))["text"])
        d = em.paper_update(update_x(stage="PAPER_TRADING", paper=PAPER))["text"]
        for part in ("[PAPER] PRACTICE UPDATE", "1. In your journal: close 50% at 85,250.",
                     "2. Move the paper stop to 83,950 (your entry).", "Paper entry: 83,950", "STRATEGY PAPER SCORE"):
            self.assertIn(part, d)
        c = em.paper_complete(dict(strategy="S", version="1.1", tf="4h", results=[2.0, -1.0] * 10, total_r=10.0,
                                   passed=False, reasons=["paper -0.10R is 0.40R below the backtest's +0.30R"]))["text"]
        self.assertIn("20 paper signals done. It did not pass.", c)
        self.assertIn("YOUR DECISION\n  None – paper -0.10R is 0.40R below the backtest's +0.30R.", c)
        self.assertIn("W L W L", c)

    def test_alert_and_fixed_content(self):
        a = all_mails()[13][1]
        t = a["text"]
        for part in ("[ALERT] SYSTEM", "! Market data unsafe", "Since 14:05 Beijing · signals paused automatically",
                     "DO NOW\n  Nothing. The agent paused new signals by itself.",
                     "No 'Fixed' email by 20:05? Forward this email to the builder.", "WHAT BROKE: Binance price feed",
                     "IMPACT: No new signals.", "AGENT TRIED: Refetch 3 times", "OPEN TRADES: 0 / 3", "WHAT IT MEANS"):
            self.assertIn(part, t)
        self.assertIn("1. Open the failed run", em.alert(dict(title="x", steps=["Open the failed run (button below)."]))
                      ["text"])
        g = all_mails()[14][1]["text"]
        for part in ("[FIXED] SYSTEM", "✓ Market data OK again", "Down: 14:05–15:10 (Beijing)", "Duration: 1 h 5 m",
                     "Signals missed: 0", "Cause: Binance feed stale; fixed itself", "Closes the alert 'Market data unsafe'"):
            self.assertIn(part, g)

    def test_mime_parts_inline_chart_and_threads(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        with open(os.path.join(tmp, "c.png"), "wb") as f:
            f.write(PNG)
        m = em.live_entry(entry_card(chart_cid="chart"))
        with mock.patch.object(notify, "ROOT", tmp):
            msg = notify.build_message(dict(m, chart="c.png", thread="BTC-1h-S-t"), "a@b.c", "a@b.c")
        parsed = email.message_from_bytes(msg.as_bytes())
        types = [p.get_content_type() for p in parsed.walk()]
        self.assertEqual(types[0], "multipart/alternative")
        self.assertIn("text/plain", types)
        self.assertIn("text/html", types)
        self.assertIn("image/png", types)
        img = next(p for p in parsed.walk() if p.get_content_type() == "image/png")
        self.assertEqual(img["Content-ID"], "<chart>")
        entry_id = parsed["Message-ID"]
        self.assertEqual(entry_id, notify.thread_id("BTC-1h-S-t"))
        self.assertIsNone(parsed["In-Reply-To"])
        up = email.message_from_bytes(notify.build_message(dict(em.live_update(update_x()), thread="BTC-1h-S-t",
                                                                 reply=True), "a@b.c", "a@b.c").as_bytes())
        self.assertEqual(up["In-Reply-To"], entry_id)                         # every update is a reply to its entry
        self.assertEqual(up["References"], entry_id)
        self.assertNotEqual(up["Message-ID"], entry_id)
        plain = email.message_from_bytes(notify.build_message(em.fixed(dict()), "a@b.c", "a@b.c").as_bytes())
        self.assertEqual(sorted(p.get_content_type() for p in plain.walk()),
                         ["multipart/alternative", "text/html", "text/plain"])
        self.assertIsNone(plain["In-Reply-To"])


class Numbers(unittest.TestCase):
    """The emails show the engine files' numbers."""

    def test_briefing_from_latest_json(self):
        rep = rep_file()
        b = mf.briefing(rep, "08:20", "2026-09-26 00:40", None, None, "https://d/", dict(cells=CELLS), REGISTRY,
                        [dict(date="2026-09-26", backtests=460, coins=10)],
                        [dict(id="R4-BBRSI", version="1.0")], "C01 Time Series Momentum")
        self.assertEqual([c["coin"] for c in b["coins"]], ["BTC", "SUI"])                # the signal coins only
        self.assertEqual([c["change_24h"] for c in b["coins"]], [1.374, -2.5])
        self.assertEqual((b["open"], b["max_open"], b["signals"]), (1, 3, 0))
        self.assertEqual(b["progress"]["counts"], dict(APPROVED=1, PAPER=1, TESTING=2, FAILED=2, TESTED=6))
        t = em.briefing(b)["text"]
        for part in ("BTC: 84,571 (1D up · 4H up)", "Mood (Fear & Greed): Greed 74 (yesterday 71)",
                     "BTC  | 84,571 | ▲ Up        | +1.4%", "SUI  | 1.1467 | ⚡ Fast move | −2.5%",
                     "Wed 30 · 20:30 | US PCE", "Claude's summary is missing",
                     "TEST: 460 backtests on 10 coins at 08:40, incl. new R4-BBRSI", "CHECK: A v1.0 4h – needs +0.05R",
                     "STUDY: C01 Time Series Momentum", "Approved 1 · Paper 1 · Testing 2 · Failed 2",
                     "Closest: A v1.0 4h: +0.05R of +0.10R", "System ✓ OK · last scan 09:07 · data GOOD"):
            self.assertIn(part, t)
        self.assertIn("ACTION\n  Check the stops of your 1 open trade.", t)

    def test_changes_only_briefing(self):
        rep = rep_file()
        s0 = mf.snapshot(rep, {}, REGISTRY, [dict(id="X", version="1.0")])
        self.assertEqual(mf.diff(s0, s0), [])                                              # nothing changed
        self.assertEqual(mf.diff(None, s0), [])
        rep2 = dict(rep, daily=dict(matrix=[dict(rep["daily"]["matrix"][0], regimes=["X", "WEAK_BEAR"])]
                                    + rep["daily"]["matrix"][1:]),
                    data_quality=dict(rep["data_quality"], system_state="DEGRADED"))
        s1 = mf.snapshot(rep2, {}, REGISTRY.replace("E,1.0,1h,VALIDATION", "E,1.0,1h,PAPER_TRADING"),
                         [dict(id="X", version="1.0"), dict(id="R4-BBRSI", version="1.0")])
        ch = mf.diff(s0, s1)
        self.assertEqual([c[1] for c in ch], ["BTC daily trend: ▲ Up → ▼ Down", "E v1.0 1h: VALIDATION → PAPER_TRADING",
                                              "New idea in the lab: R4-BBRSI. Testing starts at the next research run.",
                                              "Data GOOD → DEGRADED"])
        t = em.changes(mf.changes(rep2, "21:20", "14:20", "2026-09-26 13:20", ch, "https://p/"))["text"]
        for part in ("[BRIEFING] 21:20 update", "4 changes since 14:20. Still no trade.", "WHAT CHANGED",
                     "◆ BTC daily trend", "UNCHANGED", "Signals 0 · Open trades 1 / 3 · BTC up · Next event: PCE"):
            self.assertIn(part, t)

    def test_daily_from_the_files(self):
        rep = rep_file()
        hist = [dict(date="2026-09-25", backtests=500, strategies=21, coins=1),
                dict(date="2026-09-26", backtests=516, strategies=22, coins=3)]
        lab = [dict(id="R4-BBRSI", version="1.0", added="2026-09-26", factory="literature", timeframes=["1h"],
                    source="R4 freqtrade-strategies", description="Buy oversold closes."),
               dict(id="X", version="1.1", added="2026-09-26", factory="failure", timeframes=["4h"], hypothesis="h"),
               dict(id="OLD", version="1.0", added="2026-09-20", factory="variant_search")]
        research = dict(run_utc="2026-09-26 00:40",
                        cells={"X@1.1|4h": dict(strategy="X", version="1.1", tf="4h", status="FAILED")},
                        changes=[dict(key="donchian_breakout@1.0", tf="4h", old="FAILED", new="BACKTESTING")],
                        missed_moves=[dict(coin="SUI", direction="up", pct=13.4, start_utc="2026-09-26 02:00",
                                           verdict="not identifiable: no strategy had a setup before the move"),
                                      dict(coin="ENA", direction="up", pct=18.4, start_utc="2026-09-26 03:00",
                                           verdict="identifiable: at least one strategy had a valid signal")])
        lessons = "### a\n- timestamp: 2026-09-26 15:40 UTC · source: x\n### b\n- timestamp: 2026-09-25 15:40 UTC\n"
        log = "## 2026-09-26 · Claude (BUILD mode) · Fix: bias check v2\n## 2026-09-25 · Claude · Phase 18\n"
        d = mf.daily(rep, research, hist, lab, lessons, "", "2026-09-26", "2026-09-26 15:50", None, None, "https://d/",
                     REGISTRY, log, [("2026-09-26", "Email format v2 (#33)")], {}, ("Tests green", True))
        self.assertEqual(d["counts"]["backtests"], 516)
        self.assertEqual([t["result_r"] for t in d["live_trades"]], [1.5, -1.0])        # live closed only
        self.assertEqual(len(d["paper_trades"]), 1)
        self.assertEqual(d["lessons_added"], 1)
        self.assertEqual([(i["source"], i["status"]) for i in d["ideas"]], [("FREQTRADE", "TESTING"),
                                                                            ("LOSS PATTERN", "FAILED")])
        t = em.daily(d)["text"]
        for part in ("2 trades. 516 backtests, 2 new ideas, 1 lesson.", "Live: 2 (closed trades)", "Paper: 1 (closed)",
                     "Day: +0.5R", "Week: −1.2R", "Missed moves: SUI +13.4% (correct skip), ENA +18.4% (real miss)",
                     "Backtests: 516", "Strategies: 22", "Coins: 3",
                     "STATUS: donchian_breakout 4h: FAILED → BACKTESTING",
                     "BUILT: Fix: bias check v2; Email format v2 (#33)",
                     "R4-BBRSI v1.0 · 1h [FREQTRADE · TESTING] - Buy oversold closes.", "3 · CLOSEST TO PASSING",
                     "4 · LEARNED TODAY", "5 · TOMORROW", "WATCH: PCE Wed 20:30; research run 08:40",
                     "✓ Data GOOD · ! Last scan 09:07 · ✓ Tests green · ! Candidate coins with bad data: VTHO"):
            self.assertIn(part, t)
        self.assertIn("ACTION\n  Check the stops of your 1 open trade.", t)

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

    def test_weekly_from_the_files(self):
        now = dt.datetime(2026, 9, 27, 4, 7, tzinfo=dt.timezone.utc)
        research = dict(approval=dict(eligible=[dict(strategy="S6", version="1.0", tf="4h", pack="reports/approval/S6.md")]),
                        cells=CELLS)
        rep = dict(rep_file(), weekly=dict(week="2026-W39", results=[dict(stage="APPROVED", n=2, total_r=0.5),
                                                                     dict(stage="PAPER_TRADING", n=3, total_r=1.2)],
                                           lifecycle=[], card=dict(sources=4, data_problems=[]),
                                           missed_moves=[dict(verdict="not identifiable: x")] * 4))
        log = ("## 2026-09-24 · Claude · Phase 0 — settings\n## 2026-09-26 · Claude · Fix: false BIASED alarm\n"
               "## 2026-09-19 · Claude · Old\n")
        lessons = "### Wider stops do not save losing entries\n- timestamp: 2026-09-26 06:22 UTC · x\n"
        sources = "### [R1] RD-Agent\n- timestamp: 2026-09-26 06:40 UTC · x\n### old\n- timestamp: 2026-09-01 00:00 UTC\n"
        queue = "### Queue: R4-CLUC@1.0\n- timestamp: t\n  - card:\n```yaml\n- id: R4-CLUC\n```\n"
        w = mf.weekly(rep, research, [], queue, now, dict(headline="One is close.", sub="Decide below.",
                                                          next="Test the queue.", improvement="Fewer cards."),
                      None, "https://d/", "https://o.github.io/r/", "https://github.com/o/r", REGISTRY, log,
                      [("2026-09-26", "Bias check v2 (#31)")], lessons, sources,
                      dict(sources={"CoinDesk": dict(status="ok"), "The Block": dict(status="error")}),
                      "C01 Time Series Momentum", "Tests: 566 · ✓ green on main")
        self.assertEqual(w["decision"][0]["pack_url"], "https://github.com/o/r/blob/main/reports/approval/S6.md")
        self.assertEqual(w["decision"][0]["chart_url"], "https://o.github.io/r/chart.html#s=S6&v=1.0&tf=4h")
        self.assertEqual(w["funnel"]["TESTED"], 6)
        t = em.weekly(w)["text"]
        for part in ("[WEEKLY] Week 39  |  21–27 Sep", "YOUR DECISION\n  Approve S6 v1.0 4h for real-money signals? "
                     "Reply YES or NO.", "Live: 2 (+0.5R)", "Paper: 3 (+1.2R)", "Missed: 4 (4 correct skip)",
                     "Tested: 6 (cells)", "FROM MISTAKES\n  - false BIASED alarm", "FROM TESTING\n  - Wider stops",
                     "FROM ONLINE\n  - [R1] RD-Agent", "! Feeds failing: The Block",
                     "Thu 24 | Phase 0 — settings", "Sat 26 | Fix: false BIASED alarm; Bias check v2 (#31)",
                     "Tests: 566 · ✓ green on main", "RESEARCH SOURCES READ: 4", "DATA SOURCES: ✓ All OK",
                     "SELF-IMPROVEMENT IDEA: Fewer cards.", "TEST: R4-CLUC", "FIX: A v1.0 4h – needs +0.05R per trade",
                     "STUDY: C01 Time Series Momentum", "EVENTS: PCE Wed 30", "PLAN: Test the queue."):
            self.assertIn(part, t)
        self.assertNotIn("Old", t)                                             # outside the 7 days


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
        h = em.live_entry(entry_card())["html"]
        self.assertIn('href="https://o.github.io/r/chart.html#s=S6-OB-FVG&amp;v=1.0&amp;tf=1h&amp;c=BTC"', h)
        self.assertIn(">Backtest chart</a>", h)
        self.assertNotIn('href=""', "".join(m["html"] for _, m in all_mails(True)))     # a missing link: no button


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
        self.assertEqual(m[0]["subject"], "! Hourly scan failed twice · no new signals or trade updates")
        self.assertIn("Since 10:07 Beijing", m[0]["text"])                           # the first failed run
        self.assertIn("1. Open the failed run", m[0]["text"])
        self.assertEqual(self.run_mode([bad, bad, ok]), [])                          # third: already reported
        self.assertEqual(len(self.run_mode(None)), 1)                                 # GitHub not readable: send
        self.assertIn("Daily research run failed twice", self.run_mode([bad], "research_failed")[0]["subject"])
        self.assertIn("Tests on main failing", self.run_mode([ok], "tests_failed")[0]["subject"])   # tests: 1st red
        self.assertEqual(self.run_mode([bad, ok], "tests_failed"), [])                # already reported

    def test_fixed_once_after_a_reported_streak(self):
        ok, bad = ("success", "2026-09-26 01:07", "u"), ("failure", "2026-09-26 02:07", "u")
        self.assertEqual(self.run_mode([ok, bad], "recovered"), [])
        self.assertEqual(self.run_mode([bad, ok], "recovered"), [])                   # 1 failure was never emailed
        m = self.run_mode([bad, bad, ok], "recovered")
        self.assertEqual(len(m), 1)
        self.assertEqual(m[0]["subject"], "✓ Fixed · hourly scan OK")
        self.assertIn("Cause: 2 failed runs in a row, then this run worked", m[0]["text"])


class Alerts(unittest.TestCase):
    """The alert registry: one ALERT per problem, one FIXED when it recovers; the watchdog; system and risk alerts."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        rep = os.path.join(self.tmp, "reports")
        os.makedirs(os.path.join(rep, "claude", "briefings"))
        self.sent = []
        for name, value in (("REPORTS", rep),
                            ("send_mail", lambda m: self.sent.append(m) or True),
                            ("pages_base", lambda: "https://o.github.io/r/")):
            p = mock.patch.object(notify, name, value)
            p.start()
            self.addCleanup(p.stop)
        self.rep = rep

    def write(self, name, obj):
        with open(os.path.join(self.rep, name), "w") as f:
            json.dump(obj, f)

    def subjects(self):
        s = [m["subject"] for m in self.sent]
        self.sent.clear()
        return s

    def test_open_once_close_once(self):
        a = dict(title="Market data unsafe", impact="signals paused", utc="2026-09-26 06:05", thing="market data")
        self.assertTrue(notify.alert_open("scan", "data", a))
        self.assertFalse(notify.alert_open("scan", "data", a))                        # one ALERT per problem
        self.assertEqual(self.subjects(), ["! Market data unsafe · signals paused"])
        self.assertTrue(notify.alert_close("scan", "data", "2026-09-26 07:10", missed=0))
        self.assertFalse(notify.alert_close("scan", "data", "2026-09-26 08:10"))
        self.assertEqual(self.subjects(), ["✓ Fixed · market data OK · 0 signals missed"])

    def test_data_alert_only_for_the_system_or_a_signal_coin(self):
        self.write("latest.json", rep_file())
        q = dict(checked_utc="2026-09-26 06:05", system_state="DEGRADED", reason="x", second_exchange="OKX",
                 blocked_signals=[],
                 coins={"BTC": dict(state="GOOD", timeframes={}), "VTHO": dict(state="UNSAFE", timeframes={})})
        self.write("data_quality.json", q)
        notify.system_email()
        self.assertEqual(self.subjects(), [])                                         # a candidate coin: no alert
        q["coins"]["SUI"] = dict(state="UNSAFE", timeframes={"1h": dict(problems=["stale"])})
        self.write("data_quality.json", q)
        notify.system_email()
        notify.system_email()
        self.assertEqual(self.subjects(), ["! Market data unsafe · no signals on SUI"])
        q["coins"].pop("SUI")
        self.write("data_quality.json", dict(q, checked_utc="2026-09-26 07:05"))
        notify.system_email()
        self.assertEqual(self.subjects(), ["✓ Fixed · market data OK · 0 signals missed"])

    def test_risk_halt_alert_and_fixed(self):
        self.write("latest.json", dict(rep_file(), risk=dict(transitions=[dict(kind="start", what="day loss",
                                                                               text="Day -3.0R: halted")])))
        notify.risk_email()
        self.assertEqual(self.subjects(), ["! Risk halt: day loss · no new live entries"])
        self.write("latest.json", dict(rep_file(), generated_utc="2026-09-27 00:07",
                                       risk=dict(transitions=[dict(kind="end", what="day loss", text="new day")])))
        notify.risk_email()
        self.assertEqual(self.subjects(), ["✓ Fixed · risk halt (day loss) OK"])

    def test_watchdog_scan_and_missing_claude_tasks(self):
        self.write("latest.json", rep_file())                                         # scan at 01:07 UTC
        os.makedirs(os.path.join(self.rep, "claude", "daily"))
        for rel in ("briefings/2026-09-25-1420.md", "briefings/2026-09-25-2120.md", "daily/2026-09-25.md"):
            with open(os.path.join(self.rep, "claude", rel), "w") as f:                  # yesterday's all arrived
                f.write("# x\n")
        with mock.patch.object(notify, "ROOT", self.tmp):
            notify.watchdog(dt.datetime(2026, 9, 26, 1, 30, tzinfo=dt.timezone.utc))
            self.assertEqual(self.subjects(), ["! Claude 08:20 briefing missing · the engine sends its numbers"])
            notify.watchdog(dt.datetime(2026, 9, 26, 3, 30, tzinfo=dt.timezone.utc))
            self.assertEqual(self.subjects(), ["! No scan for 2 hours · no signals, no trade updates"])
            with open(os.path.join(self.rep, "claude", "briefings", "2026-09-26-0820.md"), "w") as f:
                f.write("# late\n")
            self.write("latest.json", dict(rep_file(), generated_utc="2026-09-26 03:07"))
            notify.watchdog(dt.datetime(2026, 9, 26, 3, 40, tzinfo=dt.timezone.utc))
            self.assertEqual(sorted(self.subjects()), ["✓ Fixed · Claude briefing OK", "✓ Fixed · hourly scan OK"])
            notify.watchdog(dt.datetime(2026, 9, 26, 3, 55, tzinfo=dt.timezone.utc))
            self.assertEqual(self.subjects(), [])                                     # nothing twice

    def test_watchdog_no_alert_when_a_newer_report_arrived(self):
        self.write("latest.json", dict(rep_file(), generated_utc="2026-09-26 09:07"))
        os.makedirs(os.path.join(self.rep, "claude", "daily"))
        for rel in ("briefings/2026-09-25-1420.md", "briefings/2026-09-25-2120.md", "briefings/2026-09-26-0820.md",
                    "briefings/2026-09-26-1420.md",
                    "daily/2026-09-26.md"):                                   # 25 Sep's daily is missing, 26 Sep's is there
            with open(os.path.join(self.rep, "claude", rel), "w") as f:
                f.write("# x\n")
        with mock.patch.object(notify, "ROOT", self.tmp):
            notify.watchdog(dt.datetime(2026, 9, 26, 9, 24, tzinfo=dt.timezone.utc))   # the 26 Sep 09:24 UTC case
        self.assertEqual(self.subjects(), [])                                     # no ALERT + FIXED pair

    def test_brain_refusal_alert_and_fixed(self):
        self.write("latest.json", rep_file())
        res = os.path.join(self.tmp, "res.json")
        with open(res, "w") as f:
            json.dump([dict(status="rejected", branch="claude/brain-daily", sha="a" * 40, when="2026-09-26 15:40",
                            applied=[], problems=["memory/lessons.md: a line was changed"])], f)
        with mock.patch.object(notify, "BRAIN_SENT", os.path.join(self.rep, "brain_sent.json")):
            notify.brain_email(res)
            notify.brain_email(res)
            self.assertEqual(self.subjects(), ["! Claude daily review refused · nothing reached main"])
            with open(res, "w") as f:
                json.dump([dict(status="applied", branch="claude/brain-daily", sha="b" * 40, when="2026-09-27 15:40",
                                applied=[], problems=[])], f)
            notify.brain_email(res)
            self.assertEqual(self.subjects(), ["✓ Fixed · Claude daily review OK"])


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
        self.assertEqual(s[0], "08:20 · No trade · BTC up · PCE Wed 20:30")
        self.assertTrue(s[1].startswith("Daily · 2 trades"))
        self.assertIn("Nothing to trade. Wait.", out)
        self.assertIn("https://o.github.io/r/claude/briefings/2026-09-26-0820.html", out)
        self.assertIn("Low volume breakouts fail.", out)
        self.assertIn("Beginner lesson: https://o.github.io/r/claude/lessons/2026-09-26.html", out)
        self.assertIn("LEARN: Your 2-min lesson: What is R", out)
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "reports/claude/lessons/2026-09-26.md")))
        with open(os.path.join(self.tmp, "reports", "curriculum_sent.json")) as f:
            self.assertEqual(json.load(f), ["L01"])
        self.assertEqual(self.subjects(self.run_notify("brain", res)), [])            # only once
        rel2 = "reports/claude/briefings/2026-09-26-1420.md"                          # 14:20: nothing changed
        with open(os.path.join(self.tmp, rel2), "w") as f:
            f.write(SummaryBlock.GOOD)
        with open(res, "w") as f:
            json.dump([dict(status="applied", branch="claude/brain-briefing", sha="c" * 40, when="2026-09-26 06:40",
                            applied=[rel2], problems=[])], f)
        out = self.run_notify("brain", res)
        self.assertEqual(self.subjects(out), [])
        self.assertIn("14:20 briefing: nothing changed since the last briefing - no email.", out)
        rel3 = "reports/claude/briefings/2026-09-26-2120.md"                          # 21:20: a new lab card
        with open(os.path.join(self.tmp, rel3), "w") as f:
            f.write(SummaryBlock.GOOD)
        with open(os.path.join(self.tmp, "strategies_lab.yaml"), "w") as f:
            f.write("- id: R4-BBRSI\n  version: '1.0'\n")
        with open(res, "w") as f:
            json.dump([dict(status="applied", branch="claude/brain-briefing", sha="d" * 40, when="2026-09-26 13:40",
                            applied=[rel3], problems=[])], f)
        out = self.run_notify("brain", res)
        self.assertEqual(self.subjects(out), ["21:20 · 1 change · still no trade"])
        self.assertIn("New idea in the lab: R4-BBRSI", out)

    def test_fallbacks_only_when_claude_is_missing_and_only_once(self):
        rep = rep_file()
        self.write("latest.json", rep)                                                # 01:07 UTC = 09:07 Beijing
        s = self.subjects(self.run_notify("daily"))
        self.assertEqual(s, ["08:20 · No trade · BTC up · PCE Wed 20:30"])
        self.assertEqual(self.subjects(self.run_notify("daily")), [])
        self.write("latest.json", dict(rep, generated_utc="2026-09-26 18:07"))
        s = self.subjects(self.run_notify("daily"))
        self.assertEqual(len(s), 1)
        self.assertTrue(s[0].startswith("Daily · "))
        self.write("latest.json", dict(rep, generated_utc="2026-09-27 01:07"))
        with open(os.path.join(self.tmp, "reports/claude/briefings/2026-09-27-0820.md"), "w") as f:
            f.write("# x\n")
        self.assertEqual(self.subjects(self.run_notify("daily")), [])                 # Claude's briefing is there

    def test_signals_new_email_blocks_and_old_ones_skipped(self):
        m = em.live_entry(entry_card())
        self.write("latest.json", dict(rep_file(), signals=[dict(coin="BTC", timeframe="1h", strategy="S",
                                                                 signal_time_utc="t", email=dict(m, thread="BTC-t"))],
                                       email_events=[dict(key="k", subject="[EXIT] old", lines=["**x**", "y"]),
                                                     dict(key="u", subject="LIVE ✓ TP1 hit", text="t", html="<p>h</p>",
                                                          thread="BTC-t", reply=True)]))
        out = self.run_notify()
        self.assertEqual(self.subjects(out), [m["subject"], "LIVE ✓ TP1 hit"])         # an old block is never sent
        self.assertIn(f"Thread: {notify.thread_id('BTC-t')} (reply)", out)
        self.assertEqual(self.subjects(self.run_notify()), [])

    def test_samples_are_marked_test(self):
        self.write("latest.json", rep_file())
        out = self.run_notify("samples")
        s = self.subjects(out)
        self.assertEqual(len(s), 12)                                                  # A, B x2, C, D, E, F, G, H, I, J, K
        self.assertTrue(all(x.startswith("TEST · ") for x in s))
        for x, word in zip(s, ["LIVE ▲", "LIVE ✓ TP1", "LIVE ✕ Stop", "PAPER ▲", "PAPER ✓ TP1", "PAPER ● 20 of 20", "! ",
                               "✓ Fixed", "08:20 · ", "14:20 · ", "Daily · ", "Week "]):
            self.assertTrue(x.startswith("TEST · " + word), (x, word))
        self.assertEqual(out.count("the trade numbers are EXAMPLES"), 12)
        self.assertIn("EXAMPLE v1.0", out)
        for f in ("alerts_scan.json", "briefing_snapshot_scan.json", "paper_sent.json"):
            self.assertFalse(os.path.exists(os.path.join(self.tmp, "reports", f)))   # a sample stores nothing
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
