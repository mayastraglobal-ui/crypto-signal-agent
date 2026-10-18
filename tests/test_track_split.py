"""2026-10-18 (operator: "fix the track report"): the track record and the weekly review show YOUR alerts (the setups
that could reach Telegram: the watcher's alert list + every PAPER / LIVE signal; versions of one setup counted once)
apart from the silent research records (the other positive program pairs GitHub keeps); the drift monitor pauses only
pairs that can alert; the hourly scan passes the alert list to both."""
import os
import sys
import unittest

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import scanner as sc  # noqa: E402
from engine import signal_center as SCX  # noqa: E402
from engine import track_record as TR  # noqa: E402
from engine import weekly_review as WR  # noqa: E402

MINE, WEAK = "P01-BREAKOUT-V1@1.0|4h", "P04-MACD-SUPERTREND-V5@1.0|30m"


def rows(results, strategy, tf, coin="ETH", start="2026-10-01 00:00", stage="TEST", direction="SHORT", t=None):
    ts = pd.date_range(start, periods=len(results), freq="4h") if t is None else pd.to_datetime(t)
    return pd.DataFrame(dict(strategy=strategy, version="1.0", tf=tf, coin=coin, stage=stage, status="SL",
                             direction=direction, result_r=results, signal_time_utc=ts.strftime("%Y-%m-%d %H:%M"),
                             closed_time_utc=(ts + pd.Timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")))


def research(win=40.0, avg=0.2):
    return dict(cells={k: dict(evidence=dict(by_coin=dict(ETH=dict(n=197, avg_r=avg, win_rate=win))))
                       for k in (MINE, WEAK)})


class Split(unittest.TestCase):
    def test_your_alerts_apart_from_the_silent_records(self):
        log = pd.concat([rows([2.0, -1.0], "P01-BREAKOUT-V1", "4h"),
                         rows([-1.0] * 5, "P04-MACD-SUPERTREND-V5", "30m", start="2026-10-05 00:00"),
                         rows([1.5], "donchian_breakout", "4h", stage="PAPER_TRADING", start="2026-10-09 00:00")],
                        ignore_index=True)
        tr = TR.build(log, "2026-10-13 07:00", research(), alerts={(MINE, "ETH")})
        self.assertTrue(tr["alerts_known"])
        self.assertEqual((tr["yours"]["n"], tr["yours"]["total_r"]), (3, 2.5))      # 2 TEST on the list + 1 PAPER
        self.assertEqual((tr["silent"]["n"], tr["silent"]["total_r"]), (5, -5.0))
        self.assertEqual(tr["total"]["n"], 8)                                          # everything, as before
        sent = {(p["key"], p["coin"]): p["sent"] for p in tr["pairs"]}
        self.assertTrue(sent[(MINE, "ETH")])
        self.assertFalse(sent[(WEAK, "ETH")])
        txt = TR.telegram(tr)
        self.assertIn("<b>Your alerts</b>: 3 closed", txt)
        self.assertIn("Silent research records (strategies NOT sent to you): 5", txt)
        self.assertNotIn("P04-MACD-SUPERTREND-V5", txt)                                # silent pairs not listed
        md = "\n".join(TR.md_lines(tr))
        self.assertIn("| **Your alerts** (could reach your Telegram) | 3 |", md)
        self.assertIn("| Silent research records (never sent to you) | 5 |", md)
        self.assertIn("| silent |", md)

    def test_versions_of_one_setup_count_once(self):
        t = ["2026-10-15 03:59"]
        log = pd.concat([rows([-1.05], "P01-BREAKOUT-V1", "4h", t=t), rows([-1.05], "P01-BREAKOUT-V4", "4h", t=t)],
                        ignore_index=True)
        tr = TR.build(log, "2026-10-16 00:00", None,
                      alerts={(MINE, "ETH"), ("P01-BREAKOUT-V4@1.0|4h", "ETH")})
        self.assertEqual((tr["yours"]["n"], tr["yours"]["total_r"]), (1, -1.05))      # one merged alert
        self.assertEqual(tr["total"]["n"], 2)

    def test_the_drift_monitor_pauses_only_pairs_that_can_alert(self):
        log = pd.concat([rows([-1.0] * 8, "P01-BREAKOUT-V1", "4h"),
                         rows([-1.0] * 8, "P04-MACD-SUPERTREND-V5", "30m")], ignore_index=True)
        tr = TR.build(log, "2026-10-13 07:00", research(), alerts={(MINE, "ETH")})
        self.assertEqual([(p["key"], p["coin"]) for p in tr["paused"]], [(MINE, "ETH")])
        old = TR.build(log, "2026-10-13 07:00", research())                            # list unknown: as before
        self.assertEqual(len(old["paused"]), 2)
        self.assertFalse(old["alerts_known"])
        self.assertEqual(old["yours"], old["total"])
        self.assertIn("All: 16 closed", TR.telegram(old))

    def test_alert_pairs_is_the_watchers_list(self):
        row = dict(n=40, avg_r=0.3, win_rate=50, test_n=10, test_avg_r=0.2)
        weak = dict(row, avg_r=0.02)
        p = dict(cells={MINE: dict(strategy=1, version="V1", status="BACKTESTING", avg_r=0.2, coins={"ETH": row}),
                        WEAK: dict(strategy=4, version="V5", status="FAILED", avg_r=0.01, coins={"ETH": weak})})
        S = SCX.settings(None)
        self.assertEqual(SCX.alert_pairs(p, {}, S), {(MINE, "ETH")})


class WeeklyReview(unittest.TestCase):
    def rv(self):
        mk = lambda n, t, sent: dict(stage="TEST", sent=sent, live=dict(n=n, total_r=t), week=dict(n=n, total_r=t))  # noqa
        return [mk(1, -1.05, True), mk(20, -13.95, False)]

    def test_totals_and_texts(self):
        t = WR.totals(self.rv())
        self.assertTrue(t["known"])
        self.assertEqual((t["YOURS"]["n"], t["YOURS"]["total_r"]), (1, -1.05))
        self.assertEqual((t["SILENT"]["n"], t["SILENT"]["total_r"]), (20, -13.95))
        self.assertEqual(t["TEST"]["n"], 21)
        rv = dict(totals=t, week="2026-W42", promote=[], demoted=[], system=[], ideas=[],
                  track=dict(alerts_known=True, yours=dict(n=1, avg_r=-1.05, total_r=-1.05, max_dd_r=1.05),
                             silent=dict(n=20, avg_r=-0.7), total=dict(n=21), paused=[]))
        txt = WR.telegram(rv)
        self.assertIn("🔵 <b>Your TEST alerts</b>: 1 closed this week (-1.1R)", txt)
        self.assertIn("Silent research records (not sent to you): 20 this week", txt)
        self.assertIn("📈 Track record (your alerts, after fees): 1 closed", txt)
        unknown = WR.totals([dict(r, sent=None) for r in self.rv()])
        self.assertFalse(unknown["known"])


class Wiring(unittest.TestCase):
    def test_the_scan_passes_the_alert_list(self):
        src = open(os.path.join(ROOT, "scanner.py"), encoding="utf-8").read()
        self.assertIn("track_record(started, logdf, cfg, args.offline, registry)", src)
        self.assertIn("alerts=alert_pairs(cfg, offline, registry))", src)
        self.assertIn("track=read_json(\"track_record\", offline), alerts=alert_pairs(cfg, offline, registry))", src)
        self.assertTrue(callable(sc.alert_pairs))


if __name__ == "__main__":
    unittest.main()
