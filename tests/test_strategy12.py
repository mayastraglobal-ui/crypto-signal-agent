"""Strategy 12 (operator request 2026-10-14: "build strategy 12"): follow the leader - when BTC jumps 3% in a day, buy
the coin already rising the most compared with BTC. The leader rank building block (lead_rank), its way from the
candles to the rules (market_breadth -> btc_frames -> attach_market -> make_namespace) in the backtest, the hourly scan
and the live watcher, the program cards (V1-V3 + control, long only), the watcher downloading every own coin, and the
save step retry of the scan / research workflows."""
import os
import sys
import unittest

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import scanner as sc  # noqa: E402
from engine import program as PG  # noqa: E402
from engine import regime as RG  # noqa: E402
from engine import signal_center as SCX  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
H4 = 4 * 3_600_000


def candles(close, step=H4):
    close = np.asarray(close, dtype=float)
    ot = np.arange(len(close), dtype=np.int64) * step
    return pd.DataFrame(dict(open_time=ot, open=close, high=close * 1.001, low=close * 0.999, close=close,
                             volume=np.ones(len(close)), close_time=ot + step - 1))


def jump(last_gain, n=300):
    """Flat at 100, then the last 6 candles rise to 100 * (1 + last_gain)."""
    c = [100.0] * (n - 6) + list(100 * (1 + last_gain * np.arange(1, 7) / 6))
    return c


GAINS = dict(BTC=0.04, ETH=0.03, SOL=0.10, XRP=0.05, SUI=0.02)


def market(gains=GAINS):
    return {(c + "USDT", "4h"): candles(jump(g)) for c, g in gains.items()}


def program_cards():
    with open(os.path.join(ROOT, "strategies_program.yaml")) as f:
        prog = yaml.safe_load(f)
    ok, problems, _, _ = SP.load_library([], [], RG.LABELS, ["4h", "1h", "30m", "15m"], prog)
    return {c["id"]: c for c in ok if c["id"].startswith("P12")}, [p for p in problems if "P12" in str(p)]


class LeaderRank(unittest.TestCase):
    def test_ranks_by_gain_minus_btc(self):
        fb = {k[0][:-4]: {"4h": v} for k, v in market().items()}
        lf = sc.leader_frames(fb, ["4h"], (6,))["4h"]
        last = lf.iloc[-1]
        self.assertEqual(last["lead_6_SOL"], 1)                  # +10% vs BTC +4%: the leader
        self.assertEqual(last["lead_6_XRP"], 2)
        self.assertEqual(last["lead_6_ETH"], 3)
        self.assertEqual(last["lead_6_SUI"], 4)
        self.assertNotIn("lead_6_BTC", lf.columns)               # BTC is never ranked
        self.assertTrue(np.isnan(lf["lead_6_SOL"].iloc[3]))     # fewer than 6 candles back: unknown

    def test_too_few_coins_or_no_btc_is_unknown(self):
        fb = {k[0][:-4]: {"4h": v} for k, v in market(dict(BTC=0.04, ETH=0.03, SOL=0.1)).items()}
        self.assertEqual(sc.leader_frames(fb, ["4h"]), {})        # 2 coins besides BTC: nothing ranked
        fb = {k[0][:-4]: {"4h": v} for k, v in market(dict(ETH=0.03, SOL=0.1, XRP=0.05, SUI=0.0)).items()}
        self.assertEqual(sc.leader_frames(fb, ["4h"]), {})        # no BTC: nothing ranked
        fb = {k[0][:-4]: {"4h": v} for k, v in market().items()}
        fb["SUI"]["4h"] = fb["SUI"]["4h"].iloc[:-1]               # SUI misses the last candle
        fb["XRP"]["4h"] = fb["XRP"]["4h"].iloc[:-1]
        lf = sc.leader_frames(fb, ["4h"], (6,))["4h"]
        self.assertTrue(np.isnan(lf["lead_6_SOL"].iloc[-1]))     # only 2 coins rankable then: unknown

    def test_the_rank_reaches_the_rules_of_each_coin(self):
        data = market()
        cfg = dict(CFG, universe=dict(CFG["universe"], own_coins=list(GAINS)))
        btc = sc.btc_frames(data, "USDT", ["4h"], sc.market_breadth(data, "USDT", cfg))
        for coin, want in (("SOL", 1), ("SUI", 4)):
            ns = sc.make_namespace(sc.attach_market(data[(coin + "USDT", "4h")].copy(), None, btc["4h"], coin))
            self.assertEqual(ns["lead_rank"](6).iloc[-1], want)
            self.assertTrue(np.isnan(ns["lead_rank"](5).iloc[-1]))   # an n outside LEAD_NS: unknown
        ns = sc.make_namespace(sc.attach_market(data[("SOLUSDT", "4h")].copy(), None, btc["4h"]))
        self.assertTrue(np.isnan(ns["lead_rank"](6).iloc[-1]))       # no coin given: unknown
        ns = sc.make_namespace(sc.attach_market(data[("BTCUSDT", "4h")].copy(), None, btc["4h"], "BTC"))
        self.assertTrue(np.isnan(ns["lead_rank"](6).iloc[-1]))       # BTC: never a leader

    def test_market_frames_join_breadth_and_ranks(self):
        self.assertEqual(sc.LEAD_TFS, ("4h", "1h"))
        self.assertEqual(sc.MARKET_TFS, ("4h", "1h", "30m", "15m"))
        data = {}
        for c, g in GAINS.items():
            for tf in ("4h", "1h"):
                data[(c + "USDT", tf)] = candles(jump(g), sc.TF_MS[tf])
        cfg = dict(CFG, universe=dict(CFG["universe"], own_coins=list(GAINS)))
        mk = sc.market_breadth(data, "USDT", cfg)
        self.assertIn("mkt_up", mk["1h"])                         # strategy 11 counts on 1H
        self.assertIn("lead_24_SOL", mk["1h"])                    # strategy 12 ranks on 1H
        self.assertNotIn("mkt_up", mk["4h"])                      # no counts on 4H (not a breadth timeframe)
        self.assertIn("lead_6_SOL", mk["4h"])
        self.assertTrue(mk["1h"]["close_time"].is_monotonic_increasing)

    def test_the_card_checker_knows_the_block(self):
        self.assertIn("lead_rank", SP.FUNCTIONS)
        self.assertIn("lead_rank", SP.BREADTH_BLOCKS)
        self.assertEqual(SP.expr_problems("lead_rank(6) == 1", ["4h"]), [])


class Cards(unittest.TestCase):
    def test_four_cards_load(self):
        cards, problems = program_cards()
        self.assertEqual(problems, [])
        self.assertEqual(sorted(cards), ["P12-LEADER-C", "P12-LEADER-V1", "P12-LEADER-V2", "P12-LEADER-V3"])
        self.assertEqual({PG.number(c) for c in cards.values()}, {12})
        self.assertEqual({c["id"]: c["timeframes"] for c in cards.values()},
                         {"P12-LEADER-V1": ["4h"], "P12-LEADER-V2": ["4h"], "P12-LEADER-V3": ["1h"],
                          "P12-LEADER-C": ["4h"]})
        for c in cards.values():
            self.assertEqual(c["gate"], "intraday_reversal")       # only never against a STRONG 4H bear
            self.assertEqual(c["short"], ["close < 0"])             # long only: a price is never below zero
            self.assertTrue(SP.uses_breadth(c) == (c["id"] != "P12-LEADER-C"))
        v1 = cards["P12-LEADER-V1"]
        self.assertEqual(v1["long"], ["btc_ret(6) >= 3", "prev(btc_ret(6)) < 3", "lead_rank(6) == 1"])
        self.assertEqual(v1["control_twin"], "P12-LEADER-C")
        self.assertEqual(cards["P12-LEADER-C"]["long"], ["btc_ret(6) >= 3", "prev(btc_ret(6)) < 3"])
        self.assertEqual(cards["P12-LEADER-V2"]["long"][-1], "lead_rank(3) == 1")
        self.assertEqual(cards["P12-LEADER-V3"]["long"][-1], "lead_rank(24) == 1")

    def test_v1_buys_only_the_leader_and_the_control_buys_all(self):
        cards, _ = program_cards()
        data = market()
        cfg = dict(CFG, universe=dict(CFG["universe"], own_coins=list(GAINS)))
        btc = sc.btc_frames(data, "USDT", ["4h"], sc.market_breadth(data, "USDT", cfg))
        fired = {}
        for coin in GAINS:
            df = sc.attach_market(data[(coin + "USDT", "4h")].copy(), None, btc["4h"], coin)
            ns = sc.make_namespace(df)
            for cid in ("P12-LEADER-V1", "P12-LEADER-C"):
                c = cards[cid]
                lg = sc.eval_rules(c["long"], ns, df.index)
                self.assertFalse(sc.eval_rules(c["short"], ns, df.index).any())
                if lg.any():
                    fired.setdefault(cid, []).append((coin, int(np.where(lg)[0][-1])))
        # BTC passes +3% over 6 candles on the 5th rising candle: index 298 of 300 (the first candle only)
        self.assertEqual(fired["P12-LEADER-V1"], [("SOL", 298)])
        self.assertEqual(sorted(c for c, _ in fired["P12-LEADER-C"]), sorted(GAINS))

    def test_the_control_never_alerts(self):
        row = dict(n=40, avg_r=0.3, win_rate=50, test_n=10, test_avg_r=0.2)
        p = dict(cells={"P12-LEADER-C@1.0|4h": dict(strategy=12, version="C", status="BACKTESTING", avg_r=0.3,
                                                    coins={"SOL": row}),
                        "P12-LEADER-V1@1.0|4h": dict(strategy=12, version="V1", status="BACKTESTING", avg_r=0.3,
                                                     coins={"SOL": row})})
        self.assertEqual(list(SCX.test_list(p, {}, SCX.settings(None))), ["P12-LEADER-V1@1.0|4h"])


class Wiring(unittest.TestCase):
    def test_the_watcher_downloads_every_own_coin(self):
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn('self.extra = [c for c in dict.fromkeys(["BTC"] + sc.breadth_coins(self.cfg)) '
                      'if c not in self.coins]', src)
        self.assertIn("t in sc.MARKET_TFS]", src)                # the replay: 4H too for the ranks
        self.assertIn("BNB", sc.breadth_coins(CFG))

    def test_research_builds_the_market_frames(self):
        src = open(os.path.join(ROOT, "research.py"), encoding="utf-8").read()
        self.assertIn("sc.market_frames(fb, btf)", src)
        self.assertIn("btf = [tf for tf in sc.MARKET_TFS if tf in tfs]", src)

    def test_prepare_coin_hands_over_the_coin(self):
        src = open(os.path.join(ROOT, "scanner.py"), encoding="utf-8").read()
        self.assertIn("df = attach_market(df, derivs, (btc or {}).get(tf), base)", src)

    def test_scan_and_research_retry_the_save_push(self):
        for wf in ("scan.yml", "research.yml"):
            text = open(os.path.join(ROOT, ".github", "workflows", wf), encoding="utf-8").read()
            self.assertIn("for i in 1 2 3 4; do", text, wf)
            self.assertIn("bash git_sync.sh && python memory_guard.py --after-sync && git push && exit 0", text, wf)


if __name__ == "__main__":
    unittest.main()
