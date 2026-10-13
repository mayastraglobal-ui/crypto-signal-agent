"""The 4H side-by-side record (operator 2026-10-13: "test 4H without 5m check"): every 4H setup that waits for its 5m
candle gets a silent twin entered at the signal close, marked passed / rejected by the 5m check, journaled as
"plan no5m <verdict>"; the journal review and the weekly review compare the same setups with and without the check.
The alerts themselves never change."""
import csv
import os
import sys
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
from engine import confirm5m as c5m  # noqa: E402
from engine import journal as JR  # noqa: E402
from engine import weekly_review as WR  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)


def setup(tf="4h", **kw):
    p = dict(label="TEST", coin="BTC", inst="BTC-USDT-SWAP", d=1, tf=tf, strategy="P01-BREAKOUT-V1", version="1.0",
             entry=100.0, R=2.0, tps=[104.0, 106.0], split=[0.5, 0.5], max_hold=60, close_ms=14_400_000 - 1,
             limit_bars=None, manage=None, inval=None, be_frac=0.0)
    p.update(kw)
    return p


class Watcher(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.journal = os.path.join(self.tmp.name, "journal", "my_trades.csv")
        for p in (mock.patch.object(LW, "STATE", os.path.join(self.tmp.name, "s.json")),
                  mock.patch.object(LW, "JOURNAL", self.journal), mock.patch.object(LW, "log")):
            p.start()
            self.addCleanup(p.stop)
        self.w = LW.Watcher(LW.SyntheticSwap(), send=False, git=False)

    def test_config_compares_4h_only(self):
        self.assertEqual(c5m.settings(CFG.get("confirm_5m"))["compare_tfs"], ["4h"])
        self.assertEqual(c5m.settings(None)["compare_tfs"], [])

    def test_a_4h_setup_gets_a_twin_entered_at_the_signal_close(self):
        sid = self.w.twin_5m(setup(), 14_400_000 + 8000)
        t = self.w.state["shadow"][sid]
        self.assertTrue(t["no5m"])
        self.assertEqual((t["entry"], t["stop"], t["checked_ms"]), (100.0, 98.0, 14_400_000))
        self.assertIsNone(self.w.twin_5m(setup(tf="15m"), 14_400_000))       # 15m: no twin
        self.w.twin_mark(dict(twin=sid), "rejected")
        self.assertEqual(t["five_min"], "rejected")
        self.w.twin_mark(dict(twin=None), "passed")                          # no twin: nothing happens

    def test_the_twin_result_is_journaled_with_the_5m_verdict(self):
        sid = self.w.twin_5m(setup(), 14_400_000)
        self.w.twin_mark(dict(twin=sid), "passed")
        fin = dict(kind="stop", at_ms=20_000_000, px=98.0, result_r=-1.0, final=True)
        with mock.patch.object(self.w, "_advance", return_value=[fin]):
            self.w.follow(21_000_000)
        self.assertNotIn(sid, self.w.state["shadow"])
        rows = list(csv.DictReader(open(self.journal, encoding="utf-8")))
        self.assertEqual([(r["alert_id"], r["event"], r["tf"], r["result_r"]) for r in rows],
                         [(sid, "plan no5m passed", "4h", "-1.0")])

    def test_confirmations_mark_the_twin(self):
        sid = self.w.twin_5m(setup(), 14_400_000)
        self.w.pending = [dict(setup(), after_ms=14_400_000, coin="BTC", twin=sid, key="k", reserved_ms=None)]
        with mock.patch.object(LW.sc, "m5_arrays", return_value={"x": 1}), \
                mock.patch.object(LW.c5m, "check", return_value=dict(state="REJECTED", why="no body")):
            self.assertEqual(self.w.confirmations("BTC", dict(frames={}), 15_000_000), [])
        self.assertEqual(self.w.state["shadow"][sid]["five_min"], "rejected")


class Review(unittest.TestCase):
    def rows(self):
        r = lambda aid, ev, tf, x, label="TEST": dict(time_utc="2026-10-13 08:00", alert_id=aid, event=ev, label=label,
                                                      coin="BTC", side="LONG", tf=tf, strategy="P01", version="1.0",
                                                      result_r=x)
        return [r("n5a", "plan no5m passed", "4h", "2.0"), r("n5b", "plan no5m rejected", "4h", "-1.0"),
                r("n5c", "plan no5m rejected", "4h", "2.0"), r("n5d", "plan no5m undecided", "4h", "-1.0"),
                r("a1", "alert", "4h", ""), r("a1", "plan", "4h", "1.5"),
                r("a2", "alert", "15m", ""), r("a2", "plan", "15m", "-1.0")]

    def test_twins_are_not_alerts_and_compare_by_timeframe(self):
        rows = self.rows()
        self.assertEqual([t["id"] for t in JR.trades(rows)], ["a1", "a2"])     # twins never count as alerts
        c = JR.compare_5m(rows)
        self.assertEqual(list(c), ["4h"])
        self.assertEqual((c["4h"]["twin_all"]["n"], c["4h"]["twin_all"]["avg_r"]), (4, 0.5))
        self.assertEqual((c["4h"]["twin_passed"]["n"], c["4h"]["twin_passed"]["avg_r"]), (1, 2.0))
        self.assertEqual((c["4h"]["twin_rejected"]["n"], c["4h"]["twin_rejected"]["avg_r"]), (2, 0.5))
        self.assertEqual((c["4h"]["sent"]["n"], c["4h"]["sent"]["avg_r"]), (1, 1.5))
        rv = JR.review(rows, 1_800_000_000_000)
        self.assertIn("compare_5m", rv)
        self.assertTrue(any("the ones it rejected +0.50R over 2" in x for x in JR.lines(rv)))

    def test_weekly_review_shows_it_and_suggests_only_with_enough_trades(self):
        S = WR.settings(None)
        mk = lambda n, a: dict(n=n, avg_r=a, total_r=n * a, wins=0)
        cmp = {"4h": dict(twin_all=mk(25, 0.1), twin_passed=mk(12, -0.2), twin_rejected=mk(13, 0.3), sent=mk(12, -0.3))}
        fm = WR.five_min([], dict(compare_5m=cmp))
        self.assertEqual(fm["side_by_side"], cmp)
        ideas = WR.ideas([], dict(compare_5m=cmp), S)
        self.assertTrue(any("REJECTED did better" in x and "your decision" in x for x in ideas))
        few = {"4h": dict(cmp["4h"], twin_passed=mk(3, -0.2))}
        self.assertFalse(any("5m check" in x for x in WR.ideas([], dict(compare_5m=few), S)))


if __name__ == "__main__":
    unittest.main()
