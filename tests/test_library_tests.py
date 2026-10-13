"""🔵 TEST alerts for library strategies the operator names (signal_center.library_tests, 2026-10-13 "build 1H test
alerts": the 6 Oct "4H trend + 1H entry" TRD-H4-BREAKOUT-S3 1h). Their per-coin rows come from the nightly
research.json in the layout of program.json, so the same TEST bar applies; program.json itself never changes."""
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import scanner as sc  # noqa: E402
from engine import signal_center as SCX  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
KEY = "TRD-H4-BREAKOUT-S3@1.0|1h"


def research(status="BACKTESTING", avg=0.152):
    coin = lambda n, a: dict(n=n, avg_r=a, win_rate=40.0, pf=1.2)
    return dict(run_utc="2026-10-13 01:02", cells={KEY: dict(
        strategy="TRD-H4-BREAKOUT-S3", version="1.0", tf="1h", status=status,
        evidence=dict(all=dict(n=939, avg_r=avg), validate=dict(n=309, avg_r=0.273),
                      by_coin=dict(BTC=coin(175, 0.341), ETH=coin(203, 0.063), XRP=coin(117, 0.281),
                                   ZEC=coin(131, -0.029), SUI=coin(12, 0.5))))})


class Rows(unittest.TestCase):
    def test_config_names_the_4h_trend_1h_entry_strategy(self):
        self.assertEqual(SCX.settings(CFG["signal_center"])["library_tests"], [KEY])
        self.assertEqual(SCX.settings(None)["library_tests"], [])

    def test_rows_take_the_program_layout_and_the_same_bar(self):
        lib = SCX.library_rows(research(), [KEY, "missing@1.0|4h"])
        self.assertEqual(list(lib), [KEY])
        row = lib[KEY]
        self.assertEqual((row["strategy"], row["version"], row["tf"], row["trades"]), ("TRD-H4-BREAKOUT-S3", "1.0", "1h", 939))
        S = SCX.settings(None)
        p = SCX.with_library(dict(cells={}), lib)
        alerts = SCX.alert_list(SCX.test_list(p, {}, S), p, {}, S)
        self.assertEqual(sorted(alerts[KEY]), ["BTC", "XRP"])     # ETH +0.06 below the bar, ZEC negative, SUI 12 trades
        failed = SCX.with_library(dict(cells={}), SCX.library_rows(research(status="FAILED"), [KEY]))
        self.assertEqual(SCX.alert_list(SCX.test_list(failed, {}, S), failed, {}, S), {})
        self.assertEqual(SCX.with_library(None, {}), None)

    def test_program_json_is_never_changed(self):
        prog = dict(cells={"P01-BREAKOUT-V1@1.0|4h": dict(strategy=1)})
        merged = SCX.with_library(prog, SCX.library_rows(research(), [KEY]))
        self.assertEqual(list(prog["cells"]), ["P01-BREAKOUT-V1@1.0|4h"])
        self.assertEqual(sorted(merged["cells"]), ["P01-BREAKOUT-V1@1.0|4h", KEY])


class Wiring(unittest.TestCase):
    def test_the_hourly_scan_writes_the_small_file(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(sc, "REPORTS", d):
            for name, obj in (("program", dict(cells={})), ("research", research())):
                with open(os.path.join(d, f"{name}.json"), "w") as f:
                    json.dump(obj, f)
            p = sc.program_with_library(CFG)
            self.assertIn(KEY, p["cells"])
            with open(os.path.join(d, "library_tests.json")) as f:
                self.assertEqual(list(json.load(f)["cells"]), [KEY])
            os.remove(os.path.join(d, "research.json"))
            self.assertNotIn(KEY, sc.program_with_library(CFG, write=False)["cells"])   # no research: program only

    def test_the_watcher_watches_it_as_test(self):
        lib = dict(cells=SCX.library_rows(research(), [KEY]))
        files = {"reports/program.json": dict(cells={}), "reports/library_tests.json": lib}
        with tempfile.TemporaryDirectory() as d, mock.patch.object(LW, "STATE", os.path.join(d, "s.json")), \
                mock.patch.object(LW, "log"), mock.patch.object(LW.Watcher, "_json", side_effect=lambda rel: files.get(rel)):
            w = LW.Watcher(LW.SyntheticSwap(), send=False, git=False)
        self.assertIn(("TRD-H4-BREAKOUT-S3", "1h", "TEST"), [(s["id"], tf, lab) for s, tf, lab in w.watch])
        self.assertEqual(sorted(w.tests[KEY]), ["BTC", "XRP"])
        self.assertIn(("main", "reports/library_tests.json"), LW.SYNC_FILES)


if __name__ == "__main__":
    unittest.main()
