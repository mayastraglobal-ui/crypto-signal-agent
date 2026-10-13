"""Strategy 11 (operator request 2026-10-13): early momentum - the intraday_momentum gate (1H already moving, 4H not
STRONG against), the market-wide break counts (mkt_up / mkt_dn), the step counter (steps_up / steps_dn), the program
cards (V1-V4 + control, both directions), the control never alerting, and the 🌊 momentum notes (👀 forming, ⚠️ late,
🔄 bounce - information only)."""
import os
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402
import scanner as sc  # noqa: E402
from engine import lifecycle as LC  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import momentum_notes as MN  # noqa: E402
from engine import program as PG  # noqa: E402
from engine import regime as RG  # noqa: E402
from engine import signal_center as SCX  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as f:
    CFG = yaml.safe_load(f)
M30 = 1_800_000


def candles(close, high=None, low=None, t0=0, step=M30, volume=None):
    close = np.asarray(close, dtype=float)
    n = len(close)
    ot = t0 + np.arange(n, dtype=np.int64) * step
    return pd.DataFrame(dict(open_time=ot, open=close, high=close + 0.1 if high is None else high,
                             low=close - 0.1 if low is None else low, close=close,
                             volume=np.ones(n) if volume is None else volume, close_time=ot + step - 1))


def reg(**tfs):
    return {tf: (np.array(v, dtype=object), np.array([None] * len(v), dtype=object)) for tf, v in tfs.items()}


class Gate(unittest.TestCase):
    def test_1h_moving_is_enough_and_only_a_strong_4h_trend_blocks(self):
        s = dict(gate="intraday_momentum", regimes=list(RG.LABELS))
        r = reg(**{"1w": ["STRONG_BULL"] * 4, "1d": ["STRONG_BULL"] * 4,
                   "4h": ["TRANSITION", "WEAK_BULL", "STRONG_BULL", "TRANSITION"],
                   "1h": ["TRANSITION"] * 4, "1h_mom": ["DOWN", "DOWN", "DOWN", "FLAT"]})
        gl, gs, *_ = LC.gate_arrays(s, "30m", r, 4)
        self.assertEqual(gs.tolist(), [True, True, False, False])   # 4H TRANSITION / WEAK_BULL ok, STRONG_BULL not
        self.assertFalse(gl.any())
        self.assertFalse(LC.gate_arrays(dict(s, gate="intraday"), "30m", r, 4)[1].any())   # the old gate waited
        self.assertFalse(LC.gate_arrays(s, "30m", {k: v for k, v in r.items() if k != "1h_mom"}, 4)[1].any())
        self.assertIn("intraday_momentum", SP.GATES)

    def test_momentum_1h_labels(self):
        up = np.linspace(100, 130, 60)
        m = sc.momentum_1h(np.r_[up, up[::-1]])
        self.assertIsNone(m[5])                                     # EMA20 not ready
        self.assertEqual(m[59], "UP")
        self.assertEqual(m[-1], "DOWN")
        df = pd.DataFrame(dict(open_time=np.arange(3) * 3_600_000, high=1.0, low=1.0))
        g = sc.add_context(df, pd.DataFrame(index=df.index),
                           reg(**{"1h_mom": ["UP", "FLAT", None]}), "30m")
        self.assertEqual(g["dir_1h_mom"].tolist()[:2], [1.0, 0.0])
        self.assertTrue(np.isnan(g["dir_1h_mom"].iloc[2]))


class Blocks(unittest.TestCase):
    def test_steps_count_new_breaks_not_every_candle(self):
        # flat, then three separate breakdowns (2 candles, 1, 1) with pauses of 4 candles between them
        c = [100.0] * 30 + [99, 98.5, 98.6, 98.7, 98.8, 98.9, 98, 98.1, 98.2, 98.3, 98.4, 97]
        df = candles(c)
        ns = sc.make_namespace(df)
        st = ns["steps_dn"](20, 3, 24).to_numpy()
        self.assertEqual(st[29], 0)
        self.assertEqual(st[30], 1)                                 # 1st step
        self.assertEqual(st[31], 1)                                 # the same step continues
        self.assertEqual(st[36], 2)                                 # a new break after 4 quiet candles: 2nd step
        self.assertEqual(st[41], 3)                                 # 3rd step: late
        self.assertEqual(ns["steps_up"](20, 3, 24).to_numpy()[41], 0)
        self.assertEqual(ns["steps_dn"](20, 3, 4).to_numpy()[41], 1)   # an older step left the window

    def test_a_close_back_over_the_average_starts_a_new_move(self):
        # three breakdowns, then a recovery above the EMA20, then a new breakdown: step 1 again, not step 4
        c = [100.0] * 30 + [99, 98.5, 98.6, 98.7, 98.8, 98.9, 98, 98.1, 98.2, 98.3, 98.4, 97] + \
            [99.5, 100.5, 101, 100.5, 100] + [96.0]
        st = sc.make_namespace(candles(c))["steps_dn"](20, 3, 24).to_numpy()
        self.assertEqual(st[41], 3)
        self.assertEqual(st[-1], 1)                                 # the night's steps do not count in the new fall

    def test_breadth_counts_coins_breaking_the_same_way(self):
        flat = [100.0] * 30
        down = flat[:-1] + [95.0]
        frames = {"BTC": {"30m": candles(down)}, "ETH": {"30m": candles(down)}, "SOL": {"30m": candles(flat)},
                  "XRP": {"30m": candles(flat[:-1] + [105.0])}}
        b = sc.breadth_frames(frames, ["30m"])["30m"]
        self.assertEqual(b["mkt_dn"].iloc[-1], 2)
        self.assertEqual(b["mkt_up"].iloc[-1], 1)
        self.assertEqual(b["mkt_n"].iloc[-1], 4)
        b2 = sc.breadth_frames({k: frames[k] for k in ("BTC", "ETH")}, ["30m"])["30m"]
        self.assertTrue(np.isnan(b2["mkt_dn"].iloc[-1]))           # fewer than 3 coins: unknown, rules stay false

    def test_breadth_reaches_the_rules_through_the_btc_frames(self):
        flat = [100.0] * 300
        down = flat[:-1] + [95.0]
        data = {(c + "USDT", "30m"): candles(down if c != "SUI" else flat) for c in ("BTC", "ETH", "SOL", "SUI")}
        cfg = dict(CFG, universe=dict(CFG["universe"], own_coins=["BTC", "ETH", "SOL", "SUI"]))
        btc = sc.btc_frames(data, "USDT", ["30m"], sc.market_breadth(data, "USDT", cfg))
        df = sc.attach_market(data[("SUIUSDT", "30m")].copy(), None, btc["30m"])
        ns = sc.make_namespace(df)
        self.assertEqual(ns["mkt_dn"].iloc[-1], 3)
        self.assertEqual(ns["mkt_up"].iloc[-1], 0)
        df2 = sc.attach_market(data[("SUIUSDT", "30m")].copy(), None, sc.btc_frames(data, "USDT", ["30m"])["30m"])
        self.assertTrue(np.isnan(sc.make_namespace(df2)["mkt_dn"].iloc[-1]))    # no breadth given: unknown

    def test_new_blocks_are_known_to_the_card_checker(self):
        for f in ("steps_up", "steps_dn"):
            self.assertIn(f, SP.FUNCTIONS)
        for c in ("mkt_up", "mkt_dn", "dir_1h_mom"):
            self.assertIn(c, SP.COLUMNS)
        self.assertEqual(SP.expr_problems("mkt_dn >= 3", ["30m"]), [])
        self.assertEqual(SP.expr_problems("steps_dn(20,3,24) <= 2", ["30m"]), [])
        self.assertTrue(SP.uses_breadth(dict(long=["mkt_up >= 3"], short=[])))
        self.assertFalse(SP.uses_breadth(dict(long=["close > 1"], short=["close < 1"])))


class Cards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ok, problems, _, _ = sc.load_cards()
        cls.problems = {k: v for k, v in problems.items() if "P11" in k}
        cls.cards = {c["id"]: c for c in ok if PG.is_program(c) and PG.number(c) == 11}

    def test_all_five_load(self):
        self.assertEqual(self.problems, {})
        self.assertEqual(sorted(self.cards), ["P11-MOMENTUM-C", "P11-MOMENTUM-V1", "P11-MOMENTUM-V2",
                                              "P11-MOMENTUM-V3", "P11-MOMENTUM-V4"])
        self.assertEqual({c["program"]["version"] for c in self.cards.values()}, {"V1", "V2", "V3", "V4", "C"})
        self.assertEqual(self.cards["P11-MOMENTUM-V3"]["timeframes"], ["1h"])
        for c in self.cards.values():
            self.assertEqual(c["gate"], "intraday_momentum")
            self.assertTrue(c["long"] and c["short"], c["id"])           # both directions

    def test_v1_has_the_early_filters_and_beats_its_control(self):
        v1 = self.cards["P11-MOMENTUM-V1"]
        rules = " ".join(v1["short"])
        for part in ("mkt_dn", "btc_ret", "steps_dn", "rsi(close,14) > 30", "atr(14) < 2.5"):
            self.assertIn(part, rules)
        self.assertEqual(v1["control_twin"], "P11-MOMENTUM-C")
        self.assertEqual(self.cards["P11-MOMENTUM-C"]["twin_of"], "P11-MOMENTUM-V1")
        self.assertNotIn("mkt_", " ".join(self.cards["P11-MOMENTUM-C"]["short"]))

    def test_tested_after_strategies_9_and_10(self):
        cards = list(self.cards.values()) + [dict(id=f"P{k:02d}", version="1.0", timeframes=["4h"],
                                                  program=dict(strategy=k, name="x", version="V1"), _program=True)
                                             for k in (7, 8, 9, 10)]
        cells = {f"P{k:02d}@1.0|4h": dict(status="FAILED", last_checked_utc="2026-10-1%d" % (k - 5)) for k in (7, 8)}
        self.assertEqual(PG.batch(cards, cells, 2)[0], [9, 10])     # never tested 9, 10 first (lower number)
        cells.update({f"P{k:02d}@1.0|4h": dict(status="FAILED", last_checked_utc="2026-10-14") for k in (9, 10)})
        self.assertIn(11, PG.batch(cards, cells, 2)[0])

    def test_telegram_gets_only_cells_with_a_real_edge(self):
        row = lambda avg: dict(n=40, avg_r=avg, win_rate=50, test_n=10, test_avg_r=0.2)
        p = dict(cells={"A@1.0|4h": dict(strategy=1, version="V1", status="BACKTESTING", avg_r=0.19,
                                         coins={"BTC": row(0.38), "XRP": row(0.07)}),
                        "B@1.0|1h": dict(strategy=1, version="V5", status="FAILED", avg_r=-0.02,
                                         coins={"ETH": row(0.01), "BTC": row(0.2)})})
        S = SCX.settings(None)
        tests = SCX.test_list(p, {}, S)
        self.assertEqual(sorted(tests), ["A@1.0|4h", "B@1.0|1h"])                 # GitHub still records both
        self.assertEqual(SCX.alert_list(tests, p, {}, S), {"A@1.0|4h": {"BTC": tests["A@1.0|4h"]["BTC"]}})
        wide = SCX.settings(dict(alert_skip_failed=False, alert_min_avg_r=0.0))
        self.assertEqual(SCX.alert_list(tests, p, {}, wide), tests)                # the old wider list

    def test_control_never_sends_a_test_alert(self):
        row = dict(n=40, avg_r=0.3, win_rate=50, test_n=10, test_avg_r=0.2)
        p = dict(cells={"P11-MOMENTUM-C@1.0|30m": dict(strategy=11, version="C", status="FAILED", coins={"SOL": row}),
                        "P11-MOMENTUM-V1@1.0|30m": dict(strategy=11, version="V1", status="FAILED",
                                                        coins={"SOL": row})})
        t = SCX.test_list(p, {}, SCX.settings(None))
        self.assertEqual(list(t), ["P11-MOMENTUM-V1@1.0|30m"])


def state(**kw):
    s = dict(close_ms=0, close=100.0, prev_close=100.5, ema=101.0, prev_ema=101.2, atr=1.0, rsi=40.0, low20=99.8,
             high20=104.0, brk_dn=False, brk_up=False, step_dn=0.0, step_up=0.0, high24=104.0, low24=99.0,
             mom="DOWN", h4="TRANSITION", m15_ms=0, m15_close=100.0, m15_vol_x=1.5)
    s.update(kw)
    return s


class Notes(unittest.TestCase):
    S = MN.settings(dict(enabled=True))

    def test_off_by_default_and_tighter(self):
        d = MN.settings(None)
        self.assertFalse(d["enabled"])
        self.assertEqual((d["min_coins"], d["max_per_day"]), (3, 6))
        self.assertFalse(MN.settings(CFG.get("momentum_notes"))["enabled"])

    def test_forming_needs_the_level_close_volume_and_the_gate(self):
        self.assertEqual(MN.forming(state(), -1, self.S), 99.8)               # 0.2 ATR above the 30m low
        self.assertIsNone(MN.forming(state(m15_close=100.5), -1, self.S))      # 0.7 ATR away: not yet
        self.assertIsNone(MN.forming(state(m15_vol_x=1.0), -1, self.S))        # no volume
        self.assertIsNone(MN.forming(state(mom="FLAT"), -1, self.S))           # the 1H is not falling
        self.assertIsNone(MN.forming(state(h4="STRONG_BULL"), -1, self.S))     # strong 4H uptrend
        self.assertIsNone(MN.forming(state(brk_dn=True), -1, self.S))          # already broken: not "forming"
        self.assertIsNone(MN.forming(state(), 1, self.S))                      # nothing forming upward

    def test_late_names_why(self):
        self.assertEqual(MN.late(state(brk_dn=True, step_dn=1.0, rsi=35.0, close=99.0), -1, self.S), [])   # early
        why = MN.late(state(brk_dn=True, step_dn=3.0, rsi=23.0, close=97.0), -1, self.S)
        self.assertEqual(len(why), 3)
        self.assertIn("3rd breakdown", why[0])
        self.assertIn("RSI 23", why[1])
        self.assertIn("4.0 ATR below", why[2])
        self.assertEqual(MN.late(state(brk_dn=True, step_dn=3.0, mom="UP"), -1, self.S), [])   # not this gate

    def test_plan_needs_a_market_wide_move_one_message_and_cools_down(self):
        two = {"SOL": state(), "SUI": state(), "BTC": state(m15_close=101.0)}
        self.assertEqual(MN.plan(two, 10, ["15m"], {}, self.S), [])            # 2 coins: not market-wide
        three = {"SOL": state(), "SUI": state(), "BTC": state(brk_dn=True)}
        out = MN.plan(three, 10, ["15m"], {}, self.S)
        self.assertEqual(len(out), 1)                                           # ONE message for all coins
        self.assertEqual((out[0]["kind"], out[0]["coins"]), ("forming", ["SOL", "SUI"]))
        self.assertIn("• SOL", out[0]["text"])
        self.assertIn("Already through: BTC", out[0]["text"])
        self.assertIn("Information only", out[0]["text"])
        sent = {k: 10 for k in out[0]["keys"]}
        self.assertEqual(MN.plan(three, 10 + 60 * 60_000, ["15m"], sent, self.S), [])        # within 2 hours
        self.assertEqual(len(MN.plan(three, 10 + 121 * 60_000, ["15m"], sent, self.S)), 1)

    def test_late_then_bounce_once(self):
        lt = {"SOL": state(brk_dn=True, step_dn=3.0, rsi=23.0, close=97.0, ema=99.0, prev_close=97.5, prev_ema=99.2)}
        out = MN.plan(lt, 0, ["15m", "30m"], {}, self.S)
        self.assertEqual([n["kind"] for n in out], ["late"])
        self.assertIn("risky to start a new short", out[0]["text"])
        self.assertIn("SOL down 6.7% in 24h", out[0]["text"])
        sent = {out[0]["keys"][0]: 0}
        back = {"SOL": state(close=99.5, ema=99.2, prev_close=98.9, prev_ema=99.3)}
        b = MN.plan(back, 3 * 3_600_000, ["15m", "30m"], sent, self.S)
        self.assertEqual([n["kind"] for n in b], ["bounce"])
        self.assertIn("NOT a tested strategy", b[0]["text"])
        sent[b[0]["keys"][0]] = 3 * 3_600_000
        self.assertEqual(MN.plan(back, 4 * 3_600_000, ["15m", "30m"], sent, self.S), [])   # once per late note
        self.assertEqual(MN.plan(back, 13 * 3_600_000, ["30m"], {out[0]["keys"][0]: 0}, self.S), [])   # too long after


class Watcher(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        for p in (mock.patch.object(LW, "STATE", os.path.join(self.tmp.name, "state.json")), mock.patch.object(LW, "log")):
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.tmp.cleanup)
        self.w = LW.Watcher(LW.SyntheticSwap(), send=False, git=False)

    def test_command_switches_notes_off_and_on(self):
        self.assertFalse(self.w.momentum_ok())                    # off by default (config.yaml)
        self.w.state["mom_on"] = True                             # the old key from the first version is ignored
        self.assertFalse(self.w.momentum_ok())
        self.assertIn("OFF", self.w.command("momentum", "", 0))
        self.assertIn("ON", self.w.command("momentum", "on", 0))
        self.assertTrue(self.w.momentum_ok())
        self.assertIn("OFF", self.w.command("momentum", "off", 0))
        self.assertFalse(self.w.momentum_ok())
        self.assertIn("/momentum", lv.HELP)
        self.assertIn("Momentum notes", self.w.status_text(0))

    def test_notes_cap_pause_and_record(self):
        st = {c: state() for c in ("SOL", "SUI", "XRP")}
        up = {c: state(mom="UP", m15_close=103.9, high20=104.0) for c in ("BTC", "ETH", "ZEC")}
        with mock.patch.object(self.w, "say", return_value=(True, "", None)) as say:
            self.w.MN = dict(self.w.MN, max_per_day=1)
            sent = self.w.momentum_notes(dict(st, **up), 10, ["15m"])
            self.assertEqual(len(sent), 1)                         # the daily cap: 1 message (3 coins in it)
            self.assertEqual(say.call_count, 1)
            for c in ("SOL", "SUI", "XRP"):
                self.assertIn(f"forming|{c}|-1", self.w.state["mom_last"])
            self.w.state["paused_until"] = -1
            self.assertEqual(self.w.momentum_notes(st, 20, ["15m"]), [])

    def test_took_it_after_the_plan_ended_is_refused(self):
        a = dict(label="TEST", coin="ETH", inst="ETH-USDT-SWAP", d=-1, tf="1h", strategy="P01", version="1.0",
                 entry=2439.5, R=38.0, tps=[2363.5], split=[1.0], max_hold=60, close_ms=0, sent_ms=0, choice=None,
                 plan_end=dict(kind="stop", at_ms=8100_000, r=-1.0))
        self.w.state["alerts"]["x1"] = a
        with mock.patch.object(self.w, "say", return_value=(True, "", None)) as say:
            toast = self.w.on_button(dict(id="q", data="took|x1"), 12_600_000)
        self.assertEqual(toast, "Too late - not recorded.")
        self.assertIn("already hit its stop", say.call_args[0][0])
        self.assertNotIn("x1", self.w.state["trades"])
        self.assertIsNone(a["choice"])
        b = dict(a, plan_end=None)
        self.w.state["alerts"]["x2"] = b
        self.w.state["shadow"]["x2"] = dict(hit=1)
        self.assertIn("already reached TP1", self.w.too_late("x2", b))
        self.w.state["shadow"]["x2"] = dict(hit=0)
        self.assertIsNone(self.w.too_late("x2", b))


if __name__ == "__main__":
    unittest.main()
