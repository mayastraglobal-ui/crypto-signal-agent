"""Learning-loop upgrades: near-duplicate strategies (one idea, not two), the "vs yesterday / vs last week" lines of
the daily and weekly emails, the dashboard's progress charts, and the weekly fixes (sources read, no word cut in
half, one sentence per day). Report only - no rule changes.

Run:  python -m unittest tests.test_learning_loop -v
"""
import datetime as dt
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine import dashboard  # noqa: E402
from engine import dupes  # noqa: E402
from engine import emails as em  # noqa: E402
from engine import mailfacts as mf  # noqa: E402
from engine import mailkit as mk  # noqa: E402

H = 3_600_000


def trades(coin, starts, d=1):
    return [dict(entry_time=s * H, dir=d, r=0.2) for s in starts]


def cell(*coins_starts):
    return {c: trades(c, s) for c, s in coins_starts}


class NearDuplicates(unittest.TestCase):
    def test_identical_trades_on_the_same_timeframe(self):
        """The 28 Sep example: donchian_breakout-VEXIT and -VEXIT-VRVOL 4h - 939 trades, +0.226R, all the same."""
        same = cell(("BTC", range(0, 500)), ("ETH", range(0, 439)))
        per = {("donchian_breakout-VEXIT", "1.0", "4h"): same, ("donchian_breakout-VEXIT-VRVOL", "1.0", "4h"): same,
               ("donchian_breakout-VEXIT", "1.0", "1h"): same}
        order = dupes.age_order({"donchian_breakout-VEXIT@1.0": dict(first_tested_utc="2026-09-27 00:50"),
                                 "donchian_breakout-VEXIT-VRVOL@1.0": dict(first_tested_utc="2026-09-28 00:52")},
                                ["donchian_breakout-VEXIT@1.0", "donchian_breakout-VEXIT-VRVOL@1.0"])
        d = dupes.find(per, order)
        self.assertEqual(d, {"donchian_breakout-VEXIT-VRVOL@1.0|4h": dict(
            of="donchian_breakout-VEXIT@1.0|4h", overlap=1.0, shared=939, trades=939)})   # the older one is kept
        self.assertEqual(dupes.label("donchian_breakout-VEXIT-VRVOL@1.0|4h"), "donchian_breakout-VEXIT-VRVOL v1.0 4h")
        lines = "".join(dupes.report_lines(dict(near_duplicates=d)))
        self.assertIn("donchian_breakout-VEXIT-VRVOL v1.0 4h = near-duplicate of donchian_breakout-VEXIT v1.0 4h "
                      "(100% of 939 trades shared)", lines)
        self.assertEqual(dupes.report_lines({}), [])

    def test_70_percent_of_the_bigger_cell(self):
        a = cell(("BTC", range(100)))
        b70 = cell(("BTC", list(range(70)) + list(range(1000, 1030))))           # 70 of 100 shared
        b69 = cell(("BTC", list(range(69)) + list(range(1000, 1031))))           # 69 of 100
        small = cell(("BTC", range(30)))                                          # inside a, but 30 / 100
        order = {"A@1.0": (0, "1", "A"), "B@1.0": (0, "2", "B")}
        self.assertIn("B@1.0|1h", dupes.find({("A", "1.0", "1h"): a, ("B", "1.0", "1h"): b70}, order))
        self.assertEqual(dupes.find({("A", "1.0", "1h"): a, ("B", "1.0", "1h"): b69}, order), {})
        self.assertEqual(dupes.find({("A", "1.0", "1h"): a, ("B", "1.0", "1h"): small}, order), {})

    def test_same_trade_means_same_coin_candle_and_direction(self):
        a = cell(("BTC", range(50)))
        other_coin = cell(("ETH", range(50)))
        other_side = {"BTC": trades("BTC", range(50), d=-1)}
        order = {"A@1.0": (0, "1", "A"), "B@1.0": (0, "2", "B")}
        for b in (other_coin, other_side):
            self.assertEqual(dupes.find({("A", "1.0", "1h"): a, ("B", "1.0", "1h"): b}, order), {})
        self.assertEqual(dupes.find({("A", "1.0", "1h"): a, ("B", "1.0", "4h"): a}, order), {})   # other timeframe

    def test_twins_and_small_cells_are_not_compared(self):
        a = cell(("BTC", range(50)))
        order = {"A@1.0": (0, "1", "A"), "A-noSMC@1.0": (0, "2", "A-noSMC")}
        self.assertEqual(dupes.find({("A", "1.0", "1h"): a, ("A-noSMC", "1.0", "1h"): a}, order,
                                    skip={"A-noSMC@1.0"}), {})
        tiny = cell(("BTC", range(10)))
        self.assertEqual(dupes.find({("A", "1.0", "1h"): tiny, ("B", "1.0", "1h"): tiny}, order), {})

    def test_three_copies_all_point_to_the_oldest(self):
        a = cell(("BTC", range(60)))
        per = {("C", "1.0", "1h"): a, ("A", "1.0", "1h"): a, ("B", "1.0", "1h"): a}
        order = dupes.age_order({"A@1.0": dict(first_tested_utc="2026-09-01 00:00")}, ["A@1.0", "B@1.0", "C@1.0"])
        d = dupes.find(per, order)
        self.assertEqual({k: x["of"] for k, x in d.items()}, {"B@1.0|1h": "A@1.0|1h", "C@1.0|1h": "A@1.0|1h"})

    def test_ideas_count_a_duplicate_card_once(self):
        d = {"B@1.0|4h": dict(of="A@1.0|4h")}
        self.assertEqual(dupes.ideas({"A@1.0": ["4h"], "B@1.0": ["4h"]}, d), 1)
        self.assertEqual(dupes.ideas({"A@1.0": ["4h"], "B@1.0": ["4h", "1h"]}, d), 2)   # B's 1h is its own idea

    def test_closest_to_passing_lists_the_idea_once(self):
        ev = dict(all=dict(n=939, avg_r=0.226))
        cells = {"A@1.0|4h": dict(strategy="A", version="1.0", tf="4h", status="BACKTESTING", required_avg_r=0.3,
                                  evidence=ev),
                 "B@1.0|4h": dict(strategy="B", version="1.0", tf="4h", status="BACKTESTING", required_avg_r=0.3,
                                  evidence=ev, near_duplicate=dict(of="A@1.0|4h"))}
        self.assertEqual([r[0] for r in em.closest(cells)], ["A v1.0 4h"])


HIST = [dict(date="2026-09-20", new_cards=1, best_avg_r=0.15, cells_testing=10, cells_failed=30, sources=20),
        dict(date="2026-09-26", new_cards=1),                                  # an older entry: no learning numbers
        dict(date="2026-09-27", new_cards=0, best_avg_r=0.206, cells_testing=12, cells_failed=34, sources=25,
             lab_cards=5, ideas=22),
        dict(date="2026-09-28", new_cards=2, best_avg_r=0.226, cells_testing=13, cells_failed=33, sources=27,
             lab_cards=7, ideas=24)]


SOURCES = """# Research sources

### trend_pullback@1.0 - Buy the dip inside an up-trend
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card trend_pullback@1.0 · evidence: HYPOTHESIS
### [R2] TradingAgents - bull vs bear debate
- timestamp: 2026-09-22 16:00 UTC · source: https://github.com/TauricResearch/TradingAgents · evidence: FACT
### [C01] Time Series Momentum (Moskowitz, Ooi, Pedersen 2012)
- timestamp: 2026-09-26 06:40 UTC · source: https://doi.org/10.1016/j.jfineco.2011.11.003 · evidence: RESEARCH_FINDING
### R4-BBRSI@1.0 - Bollinger + RSI dip
- timestamp: 2026-09-27 00:50 UTC · source: strategies_lab.yaml card R4-BBRSI@1.0 · evidence: UNVERIFIED_OPINION
### Binance Futures funding rates FAQ - when funding is paid and how it is built
- timestamp: 2026-09-27 01:10 UTC · source: https://www.binance.com/en/support/faq · evidence: FACT
"""


class WeeklyFixes(unittest.TestCase):
    def test_learned_from_online_is_sources_read_not_strategy_cards(self):
        self.assertEqual(mf.sources_read(SOURCES, "2026-09-22"),
                         ["Binance Futures funding rates FAQ - when funding is paid and how it is built",   # newest first
                          "[C01] Time Series Momentum (Moskowitz, Ooi, Pedersen 2012)",
                          "[R2] TradingAgents - bull vs bear debate"])
        self.assertEqual(mf.sources_read(SOURCES, "2026-09-26", n=5),
                         ["Binance Futures funding rates FAQ - when funding is paid and how it is built",
                          "[C01] Time Series Momentum (Moskowitz, Ooi, Pedersen 2012)"])      # only this week's

    def test_nothing_is_cut_mid_word(self):
        s = "not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost)"
        for n in range(10, len(s)):
            c = mk.clip(s, n)
            self.assertLessEqual(len(c), n)
            self.assertTrue(c.endswith("…"))
            self.assertTrue(s.startswith(c[:-1]))
            self.assertIn(s[len(c) - 1:len(c)], (" ", ",", ";", ":", "(", ""), c)   # the cut is at a word end
        self.assertEqual(mk.clip("short", 10), "short")
        self.assertEqual(mk.clip("unbreakablewordthatislong", 10), "unbreakab…")     # one long word: no choice
        cells = {"A@1.0|4h": dict(strategy="A", version="1.0", tf="4h", status="FAILED", required_avg_r=0.1,
                                  evidence=dict(all=dict(n=500, avg_r=0.2)), reasons=[s])}
        note = em.closest(cells)[0][3]
        self.assertEqual(note, "average met – still fails: not cost-viable: fees + slippage 0.25R per trade")
        subj = mk.subject(["Week 39", "0 approved", "closest: a_very_long_strategy_name_with_words and more words here"])
        self.assertLessEqual(len(subj), 70)
        self.assertNotIn("closest: a_very", subj.replace("…", ""))                 # the last part dropped whole

    def test_progress_history_one_plain_sentence_per_day(self):
        self.assertEqual(mf.day_sentence(["Phase 0 — operator settings", "Phase 1 — data quality",
                                          "Phase 2 — tradable universe"]),
                         "Built Phase 0 — operator settings and 2 more.")
        self.assertEqual(mf.day_sentence(["Email format v2 - type pill first, an ACTION box in every email",
                                          "Fix: false BIASED alarm on every htf_up / htf_down card (bias check v2)",
                                          "Fix: the risk manager's data check uses only the signal coins"]),
                         "Built Email format v2; fixed false BIASED alarm on every htf_up / htf_down card and 1 more.")
        self.assertEqual(mf.day_sentence(["Fix: two concurrent appends broke both lab cards; tests independent"]),
                         "Fixed two concurrent appends broke both lab cards.")
        self.assertIsNone(mf.day_sentence([]))
        long = mf.day_sentence(["x " * 60])
        self.assertTrue(long.endswith("…") and "x x" in long and len(long) < 90)
        w = mf.weekly({}, {}, [], "", dt.datetime(2026, 9, 28, 4, tzinfo=dt.timezone.utc), None, None, None,
                      changelog_text="## 2026-09-26 · Claude · Fix: a thing (detail)\n## 2026-09-26 · Claude · New X\n",
                      sources_text=SOURCES)
        self.assertEqual(w["history"], [("Sat 26", "Built New X; fixed a thing.")])
        self.assertEqual(w["learned"]["online"][0], "Binance Futures funding rates FAQ - when funding is paid and how "
                                                    "it is built")


class Versus(unittest.TestCase):
    def test_vs_yesterday(self):
        self.assertEqual(mf.versus(HIST, "2026-09-28", 1),
                         "vs yesterday · best avg R +0.226R (+0.020R) · testing 13 (+1) · failed 33 (−1) · "
                         "new lab cards 2 (yesterday 0) · sources read 27 (+2)")

    def test_vs_last_week(self):
        self.assertEqual(mf.versus(HIST, "2026-09-28", 7),                     # 20 Sep: the newest entry >= 7 days back
                         "vs last week · best avg R +0.226R (+0.076R) · testing 13 (+3) · failed 33 (+3) · "
                         "new lab cards 3 (last week 1) · sources read 27 (+7)")
        old = [dict(HIST[0], date="2026-09-10")] + HIST[1:]                   # no run in the week before: its date
        self.assertTrue(mf.versus(old, "2026-09-28", 7).startswith("vs 10 Sep · "))

    def test_old_entries_show_a_dash_and_nothing_is_guessed(self):
        s = mf.versus(HIST, "2026-09-27", 1)                                   # 27 Sep vs 26 Sep (no numbers)
        self.assertEqual(s, "vs yesterday · best avg R +0.206R · testing 12 · failed 34 · new lab cards 0 "
                            "(yesterday 1) · sources read 25")
        self.assertIsNone(mf.versus(HIST[:1], "2026-09-20", 1))                  # nothing to compare with
        self.assertIsNone(mf.versus([], "2026-09-28", 1))
        self.assertIn("best avg R –", mf.versus([dict(date="2026-09-27"), dict(date="2026-09-28")], "2026-09-28", 1))

    def test_source_count(self):
        self.assertEqual(mf.source_count(SOURCES), 3)                          # strategy-card records not counted
        self.assertEqual(mf.source_count(None), 0)

    def test_in_the_daily_and_weekly_emails(self):
        d = em.daily(dict(date="2026-09-28", counts=dict(backtests=531, strategies=25, ideas=24, near_duplicates=1,
                                                         coins=9),
                          versus=mf.versus(HIST, "2026-09-28", 1)))
        self.assertIn("vs yesterday · best avg R +0.226R (+0.020R)", d["text"])
        self.assertIn("24", d["text"])
        self.assertIn("1 near-duplicate = 1 idea", d["text"])
        self.assertNotIn("vs yesterday", em.daily(dict(date="2026-09-28"))["text"])   # no line without numbers
        w = em.weekly(dict(week_no=39, funnel=dict(TESTED=59, TESTING=13, PAPER=0, APPROVED=0, FAILED=46, NEAR_DUP=1),
                           versus=mf.versus(HIST, "2026-09-28", 7)))
        self.assertIn("vs last week · best avg R +0.226R", w["text"])
        self.assertIn("58", w["text"])                                           # 59 cells, 1 near-duplicate
        self.assertIn("1 near-duplicate counted as one idea.", w["text"])


class ProgressChart(unittest.TestCase):
    def test_series_and_dashboard_charts(self):
        s = mf.progress_series(list(reversed(HIST)))
        self.assertEqual([r[0] for r in s], ["2026-09-20", "2026-09-26", "2026-09-27", "2026-09-28"])  # oldest first
        self.assertEqual(s[-1], ("2026-09-28", 0.226, 13, 33, 7, 27, 24))
        self.assertEqual(s[1][1:], (None,) * 6)
        html = dashboard.learning_progress(s)
        for title in ("Best avg R", "Cells testing", "Cells failed", "Lab cards", "Research sources read", "Ideas"):
            self.assertIn(title, html)
        self.assertEqual(html.count("<svg"), 6)
        self.assertIn("+0.226R", html)
        self.assertEqual(dashboard.learning_progress([]), "")
        self.assertIn("no numbers yet", dashboard.svg_series([("2026-09-28", None)], "x"))

    def test_on_the_page(self):
        page = dashboard.render(dict(latest=dict(generated_utc="2026-09-28 13:22", strategy_scoreboard=[]),
                                     research=dict(near_duplicates={"B@1.0|4h": dict(of="A@1.0|4h", overlap=1.0,
                                                                                      trades=939, shared=939)}),
                                     progress=mf.progress_series(HIST), built_utc="2026-09-28 13:30"))
        self.assertIn("Learning progress per research day", page)
        self.assertIn("B@1.0 4h = near-duplicate of A@1.0 4h (100% of 939 trades shared)", page)


if __name__ == "__main__":
    unittest.main()
