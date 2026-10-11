"""🧭 Structure card tests (operator request 2026-10-11): the 4H structure snapshot rebuilt from the SMC detectors
(same answers as their own state, no look-ahead), the location verdicts, the alert / watch-note lines, /structure,
the signals-log tag and the weekly review groups - plus the two playbook extras of the same upgrade: BTC dominance
(context only) and the drawdown brake.

Run:  python -m unittest discover -s tests -v
"""
import datetime as dt
import os
import sys
import types
import unittest

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import live_watcher as LW  # noqa: E402
import scanner  # noqa: E402
from engine import features as F  # noqa: E402
from engine import live as lv  # noqa: E402
from engine import risk as rk  # noqa: E402
from engine import smc as S  # noqa: E402
from engine import structure as st  # noqa: E402
from engine import weather as wx  # noqa: E402
from engine import weekly_review as wr  # noqa: E402
from test_smc import H1, calm, frame, zigzag  # noqa: E402

UP = [95, 90, 95, 100, 95, 92, 97, 102, 97, 94, 99, 104, 99, 96, 97]     # HH / HL (test_smc.Structure)
CRASH = [(96.9, 97.0, 91.0, 91.2, 400.0)]                                  # CHoCH down with displacement
GAP = [(100.0, 100.5, 99.8, 100.4, 100), (100.4, 101.8, 100.3, 101.7, 100),
       (101.7, 102.3, 101.5, 102.2, 100)]                                  # bullish FVG 100.5 - 101.5


def detect(rows):
    df = frame(rows)
    feats = F.compute(df, H1)
    return S.detect(df, feats, tf_ms=H1), df, feats["atr"].to_numpy()


def snap_of(rows, t=None):
    res, df, atr = detect(rows)
    return st.snapshot(res, df, atr, t)


def fake(trend=1, rng=(100.0, 110.0), above=None, below=None, demand=(), supply=(), atr=1.0):
    """A hand-made snapshot (the shape of st.snapshot)."""
    return dict(t=0, close_ms=0, close=105.0, atr=atr, trend=trend,
                last_break=None if trend is None else dict(kind="BOS", dir=trend, level=104.0, candles_ago=3),
                range=None if rng is None else dict(low=rng[0], high=rng[1]),
                liq_above=above, liq_below=below,
                demand=[dict(dir=1, low=lo, high=hi, kind="order block", age=1) for lo, hi in demand],
                supply=[dict(dir=-1, low=lo, high=hi, kind="fair value gap", age=1) for lo, hi in supply])


class Snapshot(unittest.TestCase):
    def test_matches_the_detectors_own_state(self):
        res, df, atr = detect(zigzag(UP))
        s = st.snapshot(res, df, atr)
        self.assertEqual(s["trend"], 1 if res["state"]["trend"] == "up" else -1)
        self.assertEqual(s["last_break"]["kind"], "BOS")
        rng = res["state"]["dealing_range"]
        self.assertEqual((s["range"]["low"], s["range"]["high"]), (rng["low"], rng["high"]))
        if res["state"]["liquidity_above"]:
            self.assertAlmostEqual(s["liq_above"]["level"], res["state"]["liquidity_above"][0]["level"])
        if res["state"]["liquidity_below"]:
            self.assertAlmostEqual(s["liq_below"]["level"], res["state"]["liquidity_below"][0]["level"])
            kind = res["state"]["liquidity_below"][0]["kind"]
            self.assertEqual(s["liq_below"]["kind"], st.POOL_NAMES.get(kind, kind))

    def test_choch_turns_the_trend_and_marks_a_supply_zone(self):
        rows = zigzag(UP) + CRASH
        s = snap_of(rows)
        self.assertEqual(s["trend"], -1)
        self.assertEqual(s["last_break"]["kind"], "CHOCH")
        obs = [z for z in s["supply"] if z["kind"] == "order block"]
        self.assertEqual(len(obs), 1)                             # the bearish order block of the crash
        z = obs[0]
        loc, zone, _ = st.place(s, (z["low"] + z["high"]) / 2)
        self.assertEqual(loc, "supply")
        self.assertFalse(any(z["dir"] == 1 for z in s["supply"]))

    def test_no_look_ahead(self):
        rows = zigzag(UP) + CRASH + calm(8, 92.0)
        res, df, atr = detect(rows)
        for t in (20, len(zigzag(UP)) - 1, len(rows) - 3):
            full = st.snapshot(res, df, atr, t)
            cut = snap_of(rows[: t + 1])
            for k in ("trend", "last_break", "range", "liq_above", "liq_below"):
                self.assertEqual(full[k], cut[k], (t, k))
            self.assertEqual([(z["low"], z["high"]) for z in full["demand"] + full["supply"]],
                             [(z["low"], z["high"]) for z in cut["demand"] + cut["supply"]], t)

    def test_fvg_is_a_demand_zone_until_filled(self):
        rows = calm(30) + GAP
        s = snap_of(rows)
        self.assertEqual([(z["low"], z["high"], z["kind"]) for z in s["demand"]], [(100.5, 101.5, "fair value gap")])
        self.assertEqual(st.place(s, 101.0)[0], "demand")
        filled = snap_of(rows + [(102.2, 102.3, 101.2, 101.4, 100), (101.4, 101.5, 100.3, 100.6, 100)])
        self.assertEqual(filled["demand"], [])

    def test_empty_table(self):
        res, df, atr = detect(calm(5))
        self.assertIsNone(st.snapshot(res, df.iloc[:0], atr))


class Location(unittest.TestCase):
    def test_range_positions(self):
        s = fake()
        for price, loc in ((101, "discount"), (105, "middle"), (109, "premium"), (111, "above"), (99, "below")):
            self.assertEqual(st.place(s, price)[0], loc, price)
        self.assertEqual(st.place(fake(rng=None), 105)[0], "unknown")

    def test_zones_win_over_the_range_and_count_near_edges(self):
        s = fake(demand=[(100.0, 101.0)], supply=[(108.5, 109.5)])
        self.assertEqual(st.place(s, 101.2)[0], "demand")        # 0.2 above the zone, within 0.25 ATR
        self.assertEqual(st.place(s, 101.4)[0], "discount")      # too far: the range decides
        self.assertEqual(st.place(s, 109.0)[0], "supply")

    def test_verdicts_per_direction(self):
        cases = {("demand", 1): "good", ("demand", -1): "against", ("discount", 1): "good",
                 ("premium", 1): "against", ("premium", -1): "good", ("supply", -1): "good",
                 ("middle", 1): "middle", ("above", 1): "outside", ("below", -1): "outside",
                 ("unknown", 1): "unknown"}
        for (loc, d), v in cases.items():
            self.assertEqual(st.verdict(loc, d), v, (loc, d))


class Card(unittest.TestCase):
    def test_long_in_discount_with_the_trend(self):
        s = fake(above=dict(level=103.0, kind="equal highs"), below=dict(level=99.0, kind="yesterday's low"))
        c = st.card(s, 101.0, 1, R=1.0, tp1=103.5)
        self.assertEqual(c["tag"], "good;discount;with")
        self.assertEqual(c["room_r"], 2.0)
        self.assertTrue(c["before_tp1"])                         # the pool at 103 sits before TP1 103.5
        self.assertEqual(len(c["lines"]), 4)
        self.assertIn("with your LONG", c["lines"][0])
        self.assertIn("equal highs, 2.0R", c["lines"][1])
        self.assertIn("before TP1", c["lines"][1])
        self.assertIn("✅ lower part of the 4H range", c["lines"][2])

    def test_short_against_the_trend_at_demand(self):
        c = st.card(fake(demand=[(100.5, 101.5)]), 101.0, -1, R=1.0, tp1=99.0)
        self.assertEqual(c["tag"], "against;demand;against")
        self.assertIn("⚠️ against your SHORT", c["lines"][0])
        self.assertIn("buyers' area, against a SHORT", c["lines"][2])
        self.assertFalse(c["before_tp1"])

    def test_no_structure_yet(self):
        c = st.card(fake(trend=None, rng=None), 101.0, 1, R=1.0)
        self.assertEqual(c["tag"], "unknown;unknown;none")
        self.assertIn("no clear 4H trend", c["lines"][0])
        self.assertIn("no pool marked", c["lines"][1])

    def test_overview_for_the_command(self):
        s = fake(above=dict(level=112.0, kind="swing high"), demand=[(100.0, 101.0)], supply=[(108.5, 109.5)])
        txt = "\n".join(st.overview(s, 105.0, "BTC"))
        for part in ("BTC 4H structure", "Trend: <b>UP</b>", "50%", "Liquidity above: 112.00", "Supply above",
                     "Demand below", "middle of the range"):
            self.assertIn(part, txt)

    def test_review_groups(self):
        rows = [dict(structure_4h="good;demand;with", result_r=2.0), dict(structure_4h="good;discount;none",
                                                                            result_r=-1.0),
                dict(structure_4h="middle;middle;with", result_r=-1.0), dict(structure_4h="", result_r=1.0),
                dict(structure_4h="against;premium;with", result_r=None)]
        out = st.review(rows)
        self.assertEqual([(x["verdict"], x["n"], x["avg_r"], x["wins"]) for x in out],
                         [("good", 2, 0.5, 1), ("middle", 1, -1.0, 0)])


class Messages(unittest.TestCase):
    def alert(self, card=None):
        return dict(label="TEST", coin="XRP", inst="XRP-USDT-SWAP", d=1, tf="30m", strategy="P04", version="1.0",
                    entry=1.40, R=0.007, tps=[1.414, 1.421], split=[0.5, 0.5], zone_r=0.2,
                    size=dict(qty=700, notional=980, risk_usdt=5.0, capped=False), risk_pct=0.5, max_hold=60,
                    regimes={"4h": "UP"}, close_ms=1_700_000_000_000, sent_ms=1_700_000_000_000, valid_bars=2,
                    structure=card)

    def test_alert_and_watch_note_show_the_card(self):
        c = st.card(fake(above=dict(level=103.0, kind="equal highs")), 101.0, 1, R=1.0, tp1=103.5)
        msg = lv.message(self.alert(c))
        for line in c["lines"]:
            self.assertIn(line, msg)
        note = lv.watch_text(self.alert(c))
        self.assertIn(c["lines"][2], note)
        self.assertNotIn(c["lines"][0], note)                     # the note carries the location only

    def test_without_a_card_nothing_changes(self):
        msg = lv.message(self.alert(None))
        self.assertNotIn("🧭", msg)
        self.assertNotIn("📍", lv.watch_text(self.alert(None)))
        self.assertIn("/structure", lv.HELP)

    def test_structure_command(self):
        w = types.SimpleNamespace(ST=st.settings(None), struct={}, coins=["BTC", "ETH"])
        self.assertIn("No structure yet", LW.Watcher.structure_text(w, "", 0))
        w.struct = {"BTC": dict(snap=fake(), price=105.0, price_ms=1_700_000_000_000, ms=0)}
        self.assertIn("BTC: UP · middle (50%)", LW.Watcher.structure_text(w, "", 0))
        self.assertIn("Trend: <b>UP</b>", LW.Watcher.structure_text(w, "btc", 0))
        self.assertIn("I don't watch DOGE", LW.Watcher.structure_text(w, "doge", 0))
        w.ST = dict(w.ST, enabled=False)
        self.assertIn("switched off", LW.Watcher.structure_text(w, "", 0))

    def test_card_is_fail_safe(self):
        w = types.SimpleNamespace(ST=st.settings(None), struct={"BTC": dict(snap=None, price=1.0)})
        self.assertIsNone(LW.Watcher.structure_card(w, "BTC", 1, 100.0, 1.0, [102.0]))   # broken snapshot
        self.assertIsNone(LW.Watcher.structure_card(w, "ETH", 1, 100.0, 1.0, [102.0]))   # not read yet
        self.assertIn("engine/structure.py", LW.CODE_FILES)


class SignalsLog(unittest.TestCase):
    def test_tag_uses_the_4h_close_before_the_signal(self):
        rows = zigzag(UP) + CRASH + calm(8, 92.0)
        res, df, atr = detect(rows)
        t = len(zigzag(UP)) - 1                                  # before the crash: still an uptrend
        sig_ms = int(df["close_time"].iloc[t]) + 30 * 60_000     # a 30m signal inside the next candle
        tag = scanner.structure_tag((res, df, atr), sig_ms, 97.0, 1, 1.0, [99.0], st.settings(None))
        want = st.card(st.snapshot(res, df, atr, t), 97.0, 1, R=1.0, tp1=99.0)["tag"]
        self.assertEqual(tag, want)
        self.assertTrue(tag.endswith(";with"))
        self.assertEqual(scanner.structure_tag(None, sig_ms, 97.0, 1, 1.0, [99.0], st.settings(None)), "")
        self.assertIn("structure_4h", scanner.LOG_COLS)
        self.assertIn("structure_4h", scanner.TEXT_COLS)

    def test_weekly_review_location_part(self):
        log = pd.DataFrame([dict(stage="TEST", status="TP1", result_r=1.5, structure_4h="good;demand;with"),
                            dict(stage="TEST", status="SL", result_r=-1.0, structure_4h="middle;middle;with"),
                            dict(stage="TEST", status="OPEN", result_r=np.nan, structure_4h="good;demand;with"),
                            dict(stage="APPROVED", status="SL", result_r=-1.0, structure_4h="good;demand;with")])
        out = wr.location_part(log)
        self.assertEqual([(x["verdict"], x["n"]) for x in out], [("good", 1), ("middle", 1)])
        self.assertEqual(wr.location_part(log.drop(columns=["structure_4h"])), [])


class Dominance(unittest.TestCase):
    def test_reads(self):
        cases = [(dict(pct=58, ch24=-0.5), 2.0, "rotating into altcoins"),
                 (dict(pct=58, ch24=0.5), -2.0, "flight to BTC"),
                 (dict(pct=58, ch24=0.5), 2.0, "BTC leads"),
                 (dict(pct=58, ch24=-0.5), -2.0, "falling less than BTC"),
                 (dict(pct=58, ch24=0.1), 2.0, "flat"),
                 (dict(pct=58, ch24=None), 2.0, "no 24h comparison")]
        for dom, px, part in cases:
            self.assertIn(part, wx.dominance_read(dom, px)["read"], (dom, px))
        self.assertIsNone(wx.dominance_read(None, 1.0))

    def test_offline_scan_never_fetches(self):
        self.assertIsNone(scanner.btc_dominance(True, dt.datetime.now(dt.timezone.utc)))


class DrawdownBrake(unittest.TestCase):
    def log(self, results):
        return pd.DataFrame([dict(stage="APPROVED", state="CLOSED", result_r=r,
                                  closed_time_utc=f"2026-11-{i + 1:02d} 10:00",
                                  entry_time_utc=f"2026-09-{i + 1:02d} 10:00") for i, r in enumerate(results)])

    def test_on_at_ten_percent_off_back_at_the_peak(self):
        S = rk.settings({})
        self.assertFalse(rk.drawdown_brake(self.log([1] + [-1] * 10), 1.0, S)["on"])     # 9.9% below the peak
        on = rk.drawdown_brake(self.log([1] + [-1] * 11), 1.0, S)
        self.assertTrue(on["on"])
        self.assertGreaterEqual(on["dd_pct"], 10)
        self.assertTrue(rk.drawdown_brake(self.log([1] + [-1] * 11 + [3] * 5), 1.0, S)["on"])   # not back yet
        self.assertFalse(rk.drawdown_brake(self.log([1] + [-1] * 11 + [3] * 8), 1.0, S)["on"])  # back at the peak

    def test_risk_pct_uses_it_and_zero_switches_it_off(self):
        now = dt.datetime(2026, 12, 1, tzinfo=dt.timezone.utc)                # first live month over
        lg = self.log([1] + [-1] * 11)
        pct, note = rk.risk_pct(1.0, lg, now, rk.settings({}))
        self.assertEqual(pct, 0.5)
        self.assertIn("drawdown brake", note)
        self.assertEqual(rk.risk_pct(1.0, lg, now, rk.settings({"drawdown_brake_pct": 0}))[0], 1.0)
        self.assertEqual(rk.risk_pct(1.0, self.log([1, -1]), now, rk.settings({}))[0], 1.0)
        paper = lg.assign(stage="PAPER_TRADING")                              # only real (LIVE) trades count
        self.assertFalse(rk.drawdown_brake(paper, 1.0, rk.settings({}))["on"])


if __name__ == "__main__":
    unittest.main()
