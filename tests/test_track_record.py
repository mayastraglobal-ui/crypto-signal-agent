"""📈 The live track record and 🚨 the drift monitor (operator 2026-10-13: "build track record ... perfectly safe
way"): live results after fees per strategy / coin next to the 5-year backtest, a pause of a pair's Telegram alerts
when its live results leave what the backtest calls normal (the safe direction only), the pause ending by itself,
the watcher's filter / notes / /track, and the Brain's hourly schedule (small fixes)."""
import os
import sys
import tempfile
import unittest
from unittest import mock

import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import scanner as sc  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import track_record as TR  # noqa: E402
from engine import weekly_review as WR  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
KEY = "P01-BREAKOUT-V1@1.0|4h"


def log(results, coin="BTC", stage="TEST", strategy="P01-BREAKOUT-V1", tf="4h", start="2026-10-01 00:00"):
    t = pd.date_range(start, periods=len(results), freq="4h")
    return pd.DataFrame(dict(strategy=strategy, version="1.0", tf=tf, coin=coin, stage=stage, status="SL",
                             result_r=results, signal_time_utc=t.strftime("%Y-%m-%d %H:%M"),
                             closed_time_utc=(t + pd.Timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")))


def research(win=40.0, avg=0.2):
    return dict(cells={KEY: dict(evidence=dict(by_coin=dict(BTC=dict(n=197, avg_r=avg, win_rate=win))))})


class Engine(unittest.TestCase):
    S = TR.settings(None)

    def test_stats(self):
        s = TR.stats([2.0, -1.0, -1.0, 2.0, -1.0, -1.0, -1.0])
        self.assertEqual((s["n"], s["wins"], s["total_r"], s["cur_loss_run"], s["max_loss_run"]), (7, 2, -1.0, 3, 3))
        self.assertEqual(s["max_dd_r"], 3.0)                         # running total peaks at +2, ends at -1
        self.assertEqual(TR.stats([])["n"], 0)

    def test_streak_chance(self):
        self.assertAlmostEqual(TR.streak_p(8, 8, 0.6), 0.6 ** 8)
        self.assertLess(TR.streak_p(8, 8, 0.6), 0.05)                # 8 straight losses at 40% won: rare
        self.assertGreater(TR.streak_p(5, 40, 0.6), 0.5)             # 5 in a row over 40 trades: normal
        self.assertEqual(TR.streak_p(0, 10, 0.6), 1.0)

    def test_a_rare_losing_run_pauses_a_normal_one_does_not(self):
        bt = dict(n=197, avg_r=0.2, win_rate=40.0)
        v, why = TR.drift(TR.stats([-1.0] * 8), bt, self.S)
        self.assertEqual(v, "drift")
        self.assertIn("8 losses in a row", why[0])
        self.assertEqual(TR.drift(TR.stats([2.0, -1.0, -1.0, -1.0]), bt, self.S)[0], "watch")   # 3 in 4: a sign only
        self.assertEqual(TR.drift(TR.stats([2.0, -1.0, 2.0]), bt, self.S)[0], "ok")
        self.assertEqual(TR.drift(TR.stats([-1.0] * 8), None, self.S)[0], "ok")       # no backtest: never paused

    def test_a_live_average_far_below_the_backtest_pauses(self):
        bt = dict(n=197, avg_r=0.3, win_rate=60.0)
        r = [-1.0, 0.5, -1.0, -0.8, 0.4] * 4                         # 20 trades, -0.38R, no long losing run
        v, why = TR.drift(TR.stats(r), bt, self.S)
        self.assertEqual(v, "drift")
        self.assertTrue(any("standard errors" in w for w in why))
        good = [2.0, -1.0, -1.0] * 6                                 # 18 trades, 0R: below the backtest, not < 0
        self.assertNotEqual(TR.drift(TR.stats(good), bt, self.S)[0], "drift")

    def test_build_pauses_and_the_pause_ends_by_itself(self):
        tr = TR.build(log([-1.0] * 8), "2026-10-13 07:00", research())
        self.assertEqual([(p["key"], p["coin"]) for p in tr["paused"]], [(KEY, "BTC")])
        self.assertEqual(tr["paused"][0]["since_utc"], "2026-10-13 07:00")
        self.assertEqual(tr["total"]["n"], 8)
        later = TR.build(log([-1.0] * 9), "2026-10-13 11:00", research(), prev=tr)
        self.assertEqual(later["paused"][0]["since_utc"], "2026-10-13 07:00")       # the start is kept
        back = TR.build(log([-1.0] * 8 + [2.0, 2.0]), "2026-10-14 07:00", research(), prev=later)
        self.assertEqual(back["paused"], [])                         # a win ended the run: alerts back
        self.assertEqual(back["resumed"], [dict(key=KEY, coin="BTC")])
        self.assertIn("Drift monitor", "\n".join(TR.md_lines(tr)))
        self.assertIn("Paused by the drift monitor", TR.telegram(tr))

    def test_open_and_other_stages_are_handled(self):
        d = pd.concat([log([2.0, -1.0]), log([1.0], stage="PAPER_TRADING", strategy="donchian_breakout"),
                       log([5.0], stage="CHECK")], ignore_index=True)
        d.loc[d.index[0], "status"] = "OPEN"
        tr = TR.build(d, "2026-10-13 07:00", research())
        self.assertEqual((tr["by_stage"]["TEST"]["n"], tr["by_stage"]["PAPER_TRADING"]["n"], tr["total"]["n"]), (1, 1, 2))
        empty = TR.build(None, "2026-10-13 07:00")
        self.assertEqual(empty["total"]["n"], 0)
        self.assertIn("No closed live setup yet", TR.telegram(empty))

    def test_change_notes_once_per_change(self):
        tr = TR.build(log([-1.0] * 8), "2026-10-13 07:00", research())
        notes, known = TR.change_notes(tr, set())
        self.assertEqual(len(notes), 1)
        self.assertIn("alerts paused", notes[0])
        self.assertEqual(TR.change_notes(tr, known)[0], [])
        notes, known = TR.change_notes(dict(paused=[]), known)
        self.assertIn("alerts back on", notes[0])
        self.assertIn("4h on BTC", notes[0])
        self.assertEqual(known, set())


class Wiring(unittest.TestCase):
    def test_config_and_safe_defaults(self):
        S = TR.settings(CFG.get("track_record"))
        self.assertTrue(S["enabled"])
        self.assertEqual((S["streak_p"], S["avg_min_n"], S["avg_z"]), (0.05, 15, 2.0))

    def test_the_hourly_scan_writes_both_files(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(sc, "REPORTS", d), mock.patch.object(sc, "log"):
            import datetime as dt
            tr = sc.track_record(dt.datetime(2026, 10, 13, 7), log([-1.0] * 8), CFG, False)
            self.assertEqual(tr["paused"], [])                       # no research.json: no backtest, never paused
            self.assertTrue(os.path.exists(os.path.join(d, "track_record.json")))
            self.assertTrue(os.path.exists(os.path.join(d, "track_record.md")))

    def test_the_watcher_skips_paused_pairs_and_tells_once(self):
        tr = TR.build(log([-1.0] * 8), "2026-10-13 07:00", research())
        files = {"reports/track_record.json": tr}
        with tempfile.TemporaryDirectory() as d, mock.patch.object(LW, "STATE", os.path.join(d, "s.json")), \
                mock.patch.object(LW, "log"), mock.patch.object(LW.Watcher, "_json", side_effect=lambda rel: files.get(rel)):
            w = LW.Watcher(LW.SyntheticSwap(), send=False, git=False)
            self.assertEqual(w.drift_paused, {(KEY, "BTC")})
            with mock.patch.object(w, "say", return_value=(True, "", None)) as say:
                self.assertEqual(len(w.drift_notes()), 1)
                self.assertEqual(w.drift_notes(), [])            # told once
                self.assertEqual(say.call_count, 1)
            self.assertIn("Live track record", w.command("track", "", 0))
            self.assertIn("Paused by the drift monitor: P01-BREAKOUT-V1 4h BTC", w.status_text(0))
        self.assertIn(("main", "reports/track_record.json"), LW.SYNC_FILES)
        self.assertIn("engine/track_record.py", LW.CODE_FILES)
        self.assertIn("/track", lv.HELP)
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn("in self.drift_paused:", src)               # the filter in signals() for every label

    def test_weekly_review_line(self):
        tr = TR.build(log([-1.0] * 8), "2026-10-13 07:00", research())
        txt = WR.telegram(dict(totals=dict(TEST=dict(week_n=0, week_total_r=0, n=0, avg_r=None),
                                           PAPER=dict(week_n=0, week_total_r=0)), week="2026-W42", promote=[],
                               demoted=[], system=[], ideas=[], track=dict(total=tr["total"],
                                                                            paused=["P01-BREAKOUT-V1 4h BTC"])))
        self.assertIn("📈 Track record", txt)
        self.assertIn("paused: P01-BREAKOUT-V1 4h BTC", txt)


class SmallFixes(unittest.TestCase):
    def test_brain_runs_hourly(self):
        wf = open(os.path.join(ROOT, ".github", "workflows", "brain.yml"), encoding="utf-8").read()
        self.assertIn('cron: "47 * * * *"', wf)
        self.assertNotIn("*/15", wf)

    def test_replay_gives_every_coin_btc_and_breadth(self):
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        body = src[src.index("def replay(w"):src.index("def replay_text")]
        self.assertIn("sc.market_breadth(allD", body)
        self.assertNotIn('if coin == "BTC"\n', body)


if __name__ == "__main__":
    unittest.main()
