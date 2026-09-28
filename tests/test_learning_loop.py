"""Learning-loop upgrades: near-duplicate strategies (one idea, not two), the "vs yesterday / vs last week" lines of
the daily and weekly emails, and the dashboard's progress charts. Report only - no rule changes.

Run:  python -m unittest tests.test_learning_loop -v
"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine import dashboard  # noqa: E402
from engine import dupes  # noqa: E402
from engine import emails as em  # noqa: E402
from engine import mailfacts as mf  # noqa: E402

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
        self.assertEqual(mf.source_count("# Research sources\n\n### a@1.0 - x\n- y\n### b@1.0 - z\n"), 2)
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
