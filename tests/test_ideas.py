"""Phase 17 part C tests: futures market data (recording, sources, history, data checks, no look-ahead), the new
building blocks, real funding in short costs (never lower), the six idea factories (evidence, quotas), the engine's
variant search, lead-lag, pass rate per factory.

Run:  python -m unittest test_ideas -v      (from tests/)
"""
import copy
import datetime as dt
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from unittest import mock

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brain_pack  # noqa: E402
import derivs  # noqa: E402
import publish_live  # noqa: E402
import scanner  # noqa: E402
import test_brain  # noqa: E402
import test_lab  # noqa: E402
from engine import brain as B  # noqa: E402
from engine import derivs as D  # noqa: E402
from engine import digest as DG  # noqa: E402
from engine import ideas as I  # noqa: E402
from engine import regime as rg  # noqa: E402
from engine import strategy_spec as SS  # noqa: E402
from engine import timeframes as tfm  # noqa: E402

UTC = dt.timezone.utc
H = D.HOUR_MS
T0 = 1_790_000_000_000 // H * H            # a whole hour
read = test_brain.read
CFG = test_lab.CFG


def bn_rows(n=3, start=T0):
    oi = [dict(symbol="BTCUSDT", sumOpenInterest="1", sumOpenInterestValue=str(1e9 + i), timestamp=start + i * H)
          for i in range(n)]
    ls = [dict(symbol="BTCUSDT", longShortRatio=str(1.5 + i / 10), longAccount="0.6", shortAccount="0.4",
               timestamp=start + i * H) for i in range(n)]
    tk = [dict(buySellRatio=str(0.9 + i / 10), buyVol="1", sellVol="1", timestamp=start + i * H) for i in range(n)]
    return oi, ls, tk


class Parsers(unittest.TestCase):
    def test_binance_and_okx(self):
        rows = D.binance_hourly("BTC", *bn_rows())
        self.assertEqual([r["ts"] for r in rows], [T0, T0 + H, T0 + 2 * H])
        self.assertEqual((rows[1]["oi_usd"], rows[1]["ls_ratio"], rows[1]["taker_ratio"]), (1e9 + 1, 1.6, 1.0))
        f = D.binance_funding("BTC", [dict(symbol="BTCUSDT", fundingTime=T0, fundingRate="-0.0002", markPrice="1")])
        self.assertEqual(f, [dict(time=T0, coin="BTC", source="binance", rate=-0.0002)])
        ok = D.okx_hourly("ETH", {"data": [[str(T0), "5e8", "1"]]}, {"data": [[str(T0), "2.1"]]},
                          {"data": [[str(T0), "100", "150"]]})
        self.assertEqual((ok[0]["source"], ok[0]["oi_usd"], ok[0]["ls_ratio"], ok[0]["taker_ratio"]),
                         ("okx", 5e8, 2.1, 1.5))                               # buy / sell
        of = D.okx_funding("ETH", {"data": [dict(fundingTime=str(T0), fundingRate="0.0001", realizedRate="0.00012")]})
        self.assertEqual(of[0]["rate"], 0.00012)

    def test_data_binance_vision_files(self):
        day = pd.Timestamp(T0, unit="ms", tz="UTC").floor("D")
        lines = ["create_time,symbol,sum_open_interest,sum_open_interest_value,count_toptrader_long_short_ratio,"
                 "sum_toptrader_long_short_ratio,count_long_short_ratio,sum_taker_long_short_vol_ratio"]
        for m in (0, 5, 55, 60):
            t = (day + pd.Timedelta(minutes=m)).strftime("%Y-%m-%d %H:%M:%S")
            lines.append(f"{t},BTCUSDT,1,{1000 + m},1,1,{1 + m / 100},{2 + m / 100}")
        rows = D.vision_metrics("BTC", "\n".join(lines))
        self.assertEqual(len(rows), 2)                                         # hours 00 and 01
        self.assertEqual((rows[0]["oi_usd"], rows[0]["ls_ratio"]), (1055.0, 1.55))   # the LAST snapshot of the hour
        f = D.vision_funding("BTC", "calc_time,funding_interval_hours,last_funding_rate\n1790000000000,8,0.0001\n")
        self.assertEqual(f[0]["rate"], 0.0001)
        f2 = D.vision_funding("BTC", "1790000000000,8,-0.0001\n")                 # no header
        self.assertEqual(f2[0]["rate"], -0.0001)


class History(unittest.TestCase):
    def test_merge_prefers_binance_and_never_shrinks(self):
        a = D.merge(None, D.okx_hourly("BTC", {"data": [[str(T0), "5", "1"]]}, {}, {}), "ts")
        b = D.merge(a, D.binance_hourly("BTC", *bn_rows(2)), "ts")
        self.assertEqual(list(b["source"]), ["binance", "binance"])
        c = D.merge(b, [], "ts")
        self.assertEqual(len(c), 2)
        d = D.merge(c, D.okx_hourly("BTC", {"data": [[str(T0), "5", "1"]]}, {}, {}), "ts")
        self.assertEqual(list(d["source"]), ["binance", "binance"])             # a worse source never replaces

    def test_quality(self):
        h = D.merge(None, D.binance_hourly("BTC", *bn_rows(3)), "ts")
        f = D.merge(None, [dict(time=T0 + 2 * H, coin="BTC", source="binance", rate=0.0001)], "time")
        q = D.quality(h, f, ["BTC", "SOL"], T0 + 3 * H)
        self.assertEqual(q["BTC"]["state"], "GOOD")
        self.assertEqual(q["SOL"]["state"], "MISSING")
        late = D.quality(h, f, ["BTC"], T0 + 10 * H)["BTC"]
        self.assertEqual(late["state"], "STALE")
        bad = h.copy()
        bad.loc[0, "ls_ratio"] = -1
        self.assertEqual(D.quality(bad, f, ["BTC"], T0 + 3 * H)["BTC"]["invalid"], 1)
        self.assertTrue(np.isnan(D.clean(bad, f)[0].loc[0, "ls_ratio"]))
        mixed = D.merge(h, D.okx_hourly("BTC", {"data": [[str(T0 + 3 * H), "5", "1"]]}, {}, {}), "ts")
        self.assertIn("mixed sources", " ".join(D.quality(mixed, f, ["BTC"], T0 + 4 * H)["BTC"]["problems"]))

    def test_synthetic_is_repeatable(self):
        a, b = D.synthetic("SOL", T0, T0 + 50 * H), D.synthetic("SOL", T0, T0 + 50 * H)
        pd.testing.assert_frame_equal(a[0], b[0])
        pd.testing.assert_frame_equal(a[1], b[1])


class NoLookAhead(unittest.TestCase):
    def test_align(self):
        h = D.merge(None, D.binance_hourly("BTC", *bn_rows(3)), "ts")     # rows for hours T0, T0+H, T0+2H
        f = pd.DataFrame([dict(time=T0 + H, coin="BTC", source="binance", rate=-0.0003)])
        close = np.array([T0 + H - 1, T0 + H, T0 + 2 * H + 30 * 60_000, T0 + 20 * H])
        a = D.align(close, close - 15 * 60_000, h, f)
        # the hour starting at T0 is known only from its END (T0 + 1h)
        self.assertTrue(np.isnan(a["oi"][0]))
        self.assertEqual(a["oi"][1], 1e9)
        self.assertEqual(a["oi"][2], 1e9 + 1)                                   # T0+2H's row not finished yet
        self.assertTrue(np.isnan(a["oi"][3]))                                   # too old -> unknown
        self.assertTrue(np.isnan(a["funding_rate"][0]))
        self.assertAlmostEqual(a["funding_rate"][1], -0.03)                     # %, known at settlement
        self.assertAlmostEqual(a["_fund_short"][2], 0.0003)                     # negative rate: shorts pay
        self.assertEqual(a["_fund_short"][0], 0.0)

    def test_building_blocks_on_candles(self):
        n = 400
        df = pd.DataFrame(dict(open_time=T0 + np.arange(n) * H, close_time=T0 + np.arange(n) * H + H - 1,
                               open=100.0, high=101.0, low=99.0, close=100 + np.arange(n) * 0.1, volume=1.0))
        hh, ff = D.synthetic("BTC", T0 - 30 * H, T0 + n * H)
        btc = df[["close_time"]].assign(close=np.arange(n) + 1000.0)
        df = scanner.attach_market(df, (hh, ff), btc)
        ns = scanner.make_namespace(df)
        self.assertTrue(np.isfinite(ns["oi"].iloc[-1]))
        self.assertAlmostEqual(ns["oi_chg"](24).iloc[-1], (df["_oi"].iloc[-1] / df["_oi"].iloc[-25] - 1) * 100)
        self.assertAlmostEqual(ns["btc_ret"](1).iloc[-1], (1399 / 1398 - 1) * 100)
        z = ns["funding_z"](50)
        self.assertTrue(np.isfinite(z.iloc[-1]))
        # a later change of the data never changes earlier values (no look-ahead)
        df2 = df.copy()
        cut = scanner.attach_market(df2.iloc[:200].copy(), (hh[hh["ts"] < T0 + 199 * H], ff[ff["time"] < T0 + 200 * H]),
                                    btc.iloc[:200])
        pd.testing.assert_series_equal(scanner.make_namespace(cut)["oi"], ns["oi"].iloc[:200], check_names=False)
        # BTC price from a different candle is never used
        odd = scanner.attach_market(df.copy(), None, btc.assign(close_time=btc["close_time"] + 1))
        self.assertTrue(odd["_btc_close"].isna().all())
        empty = scanner.make_namespace(scanner.attach_market(df.copy(), None, None))
        self.assertTrue(empty["funding_rate"].isna().all() and empty["btc_ret"](1).isna().all())

    def test_rules_with_the_new_blocks(self):
        for r in ("funding_z(200) > 2", "oi_chg(24) > 5", "ls_ratio > 2", "taker_ratio < 0.8", "btc_ret(4) > 1"):
            self.assertEqual(SS.expr_problems(r, ["1h"]), [], r)


class RealFunding(unittest.TestCase):
    def trade(self, d, fund, cfg=CFG):
        n = 30
        c = np.full(n, 100.0)
        return scanner.simulate_trade(c, c + 0.1, c - 0.1, c, 0, d, 100.0, 5.0, cfg, 24, 1.0, fund_real=fund)

    def test_never_lower_than_the_config_rate(self):
        flat = self.trade(-1, None)["funding_r"]
        self.assertGreater(flat, 0)
        self.assertAlmostEqual(self.trade(-1, np.zeros(30))["funding_r"], flat)   # funding received: not counted
        high = self.trade(-1, np.full(30, 0.001))["funding_r"]                   # shorts pay 0.1% / 8h
        self.assertAlmostEqual(high, flat * 10)
        self.assertEqual(self.trade(1, np.full(30, 0.001))["funding_r"], 0)      # longs are spot: no funding
        stressed = self.trade(-1, np.full(30, 0.001), test_brain.research.stressed(CFG, 1.5))["funding_r"]
        self.assertAlmostEqual(stressed, high * 1.5)
        self.assertEqual(CFG["costs"]["short"]["funding_real_x"], 1.0)
        self.assertEqual(CFG["costs"]["short"]["funding_pct_per_8h"], 0.01)       # unchanged


class Factories(unittest.TestCase):
    def card(self, **kw):
        c = test_lab.plain("F")
        c.update(kw)
        return c

    def test_evidence_per_factory(self):
        tags = B.LOSS_TAGS
        P = lambda **kw: SS.factory_problems(self.card(**kw), tags)
        self.assertIn("factory must be one of", P(factory="gut_feeling")[0])
        self.assertIn("reserved for the engine", P(factory="variant_search")[0])
        self.assertEqual(SS.factory_problems(self.card(factory="variant_search", factory_evidence="x" * 30), tags,
                                             engine=True), [])
        self.assertTrue(P(factory="literature", factory_evidence="Moskowitz et al. 2012, section 4"))   # no URL
        self.assertEqual(P(factory="literature", factory_evidence="Moskowitz et al. 2012, section 4",
                           source_url="https://www.sciencedirect.com/x"), [])
        self.assertTrue(P(factory="failure", factory_evidence="range_market in many losses, n=12"))
        self.assertTrue(P(factory="failure", factory_evidence="unknown_tag in many losses, n=80"))
        self.assertEqual(P(factory="failure", factory_evidence="range_market in 40% of losses, n=80"), [])
        self.assertTrue(P(factory="missed_move", factory_evidence="a big move last week, nobody caught it"))
        self.assertTrue(P(factory="market_structure", factory_evidence="crowded longs before liquidations"))
        self.assertEqual(P(factory="market_structure", factory_evidence="crowded longs before liquidations",
                           long=["funding_z(200) > 2"], short=["funding_z(200) < -2"]), [])
        self.assertTrue(P(factory="lead_lag", factory_evidence="SOL follows BTC by an hour (n=5998)"))
        self.assertEqual(P(factory="lead_lag", factory_evidence="SOL follows BTC by an hour (n=5998)",
                           long=["btc_ret(1) > 1"], short=["btc_ret(1) < -1"]), [])

    def test_quota_per_factory_and_engine_cards(self):
        cards = [test_lab.plain(i) for i in range(3)]                           # 3 x missed_move (quota 2)
        applies, probs, _ = test_lab.review(cards, quota={})
        self.assertIn("'missed_move' cards in the last 7 days - that factory's quota is 2", " ".join(probs))
        applies, probs, _ = test_lab.review(cards[:2], quota={})
        self.assertEqual(probs, [])
        # the engine's variant cards neither use Claude's limits nor can Claude write one
        eng = [dict(test_lab.plain(f"E{i}"), factory="variant_search", factory_evidence="x" * 30) for i in range(3)]
        base = test_lab.LAB_HEAD + test_lab.dump(eng)
        self.assertEqual(test_lab.review(cards[:2] + [dict(test_lab.plain(9), factory="failure",
                                                             factory_evidence="range_market 40% of losses, n=80")],
                                         base=base, quota={})[1], [])
        applies, probs, _ = test_lab.review([dict(test_lab.plain(8), factory="variant_search",
                                                  factory_evidence="x" * 30)], quota={})
        self.assertIn("reserved for the engine", " ".join(probs))


def rcell(sid, tf, status="BACKTESTING", n=60, val=0.2, allr=0.1, by_regime=None, version="1.0"):
    return dict(strategy=sid, version=version, tf=tf, status=status,
                evidence=dict(all=dict(n=n, avg_r=allr), validate=dict(n=20, avg_r=val)),
                attribution=dict(by_regime=by_regime or {}))


class VariantSearch(unittest.TestCase):
    def setUp(self):
        ok, _, _, _ = SS.load_library(test_lab.LIB, [], rg.LABELS, tfm.TRADE_ORDER)
        self.cards = {SS.key(x): x for x in ok}

    def run_vs(self, cells, n=3, cards=None):
        return I.variant_cards(cells, cards or self.cards, dt.date(2026, 9, 27), n, rg.LABELS, tfm.TRADE_ORDER)

    def test_first_variant_of_a_card_without_2r_targets_is_the_exit(self):
        out = self.run_vs({"a": rcell("donchian_breakout", "4h"), "b": rcell("rsi2_dip_buy", "1h", val=0.1)})
        self.assertEqual([c["id"] for c in out], ["donchian_breakout-VEXIT", "rsi2_dip_buy-VEXIT"])  # best first
        c = out[0]
        others = {x["id"]: x for x in test_lab.LIB}
        self.assertEqual(SS.lab_card_problems(c, others, rg.LABELS, tfm.TRADE_ORDER), [])
        self.assertEqual(SS.change_count(self.cards["donchian_breakout@1.0"]["_raw"], c), ["targets"])
        self.assertEqual((c["factory"], c["variant_of"], c["added"]), ("variant_search", "donchian_breakout@1.0",
                                                                       "2026-09-27"))
        self.assertIn("4h: 60 trades", c["factory_evidence"])
        self.assertEqual(len(self.run_vs({"a": rcell("donchian_breakout", "4h")}, n=0)), 0)

    def test_next_variants_regime_filter_timeframe(self):
        parent = dict(test_lab.lib("donchian_breakout"), id="DB2", targets={"long": ["2R"], "short": ["2R"],
                                                                             "split": [1.0]})
        cards = {"DB2@1.0": SS.load([parent], rg.LABELS, tfm.TRADE_ORDER)[0][0]}
        bad = {"STRONG_BEAR": dict(n=40, avg_r=-0.3), "WEAK_BULL": dict(n=90, avg_r=0.2)}
        out = self.run_vs({"a": rcell("DB2", "1h", by_regime=bad)}, cards=cards)
        self.assertEqual(out[0]["id"], "DB2-VREGIME")
        self.assertNotIn("STRONG_BEAR", out[0]["regimes"])
        self.assertNotIn("STRONG_BEAR", out[0]["edge"]["works_in"])
        cards2 = dict(cards)
        taken = dict(out[0], lab=True)
        cards2["DB2-VREGIME@1.0"] = taken                                       # already written -> next kind
        nxt = self.run_vs({"a": rcell("DB2", "1h", by_regime=bad)}, cards=cards2)
        self.assertEqual(nxt[0]["id"], "DB2-VRVOL")                             # DB2 already uses adx
        self.assertIn("rel_vol > {v_rv}", nxt[0]["long"])

    def test_skipped_parents(self):
        cells = {"a": rcell("S5-SWEEP-MSS-FVG", "15m"), "b": rcell("S5-SWEEP-MSS-FVG-noSMC", "15m"),
                 "c": rcell("donchian_breakout", "4h", status="FAILED"),
                 "d": rcell("trend_pullback", "1h", n=10)}
        self.assertEqual(self.run_vs(cells), [])                                # SMC, twin, FAILED, too few trades


class LeadLagAndStats(unittest.TestCase):
    def test_lead_lag_finds_a_follower(self):
        rng = np.random.default_rng(3)
        b = np.cumsum(rng.normal(0, 1, 3000)) + 5000
        alt = np.r_[b[0], b[:-1]] * 0.01 + rng.normal(0, 0.001, 3000).cumsum() + 50      # follows BTC by 1 candle
        df = pd.DataFrame(dict(close=alt, _btc_close=b))
        ll = I.lead_lag(df)
        self.assertTrue(ll["lags"][1]["clear"])
        self.assertGreater(ll["lags"][1]["corr"], 0.3)
        self.assertIsNone(I.lead_lag(pd.DataFrame(dict(close=alt))))

    def test_factory_stats_and_weekly_line(self):
        cards = {"A@1.0": dict(lab=True, factory="failure"), "B@1.0": dict(lab=True, factory="failure"),
                 "L@1.0": dict(factory="failure")}                             # library: not a factory card
        cells = {"1": dict(strategy="A", version="1.0", status="VALIDATION"),
                 "2": dict(strategy="A", version="1.0", status="FAILED"),
                 "3": dict(strategy="L", version="1.0", status="PAPER_TRADING")}
        st = I.factory_stats(cells, cards)
        self.assertEqual((st["failure"]["cards"], st["failure"]["cells"], st["failure"]["passed"]), (2, 2, 1))
        self.assertEqual(st["failure"]["pass_rate"], 0.5)
        self.assertIsNone(st["literature"]["pass_rate"])
        line = " ".join(DG.factory_lines(dict(factories=st)))
        self.assertIn("failure 1/2 (50%)", line)
        self.assertNotIn("literature", line)


class Recorder(unittest.TestCase):
    """derivs.py end to end with a fake internet: Binance refused, OKX used, files back-filled, history kept."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        for name, f in (("HOURLY", "derivs_hourly.csv.gz"), ("FUNDING", "funding.csv.gz"),
                        ("QUALITY", "derivs_quality.json"), ("REPORTS", "")):
            p = mock.patch.object(derivs, name, os.path.join(self.tmp, f) if f else self.tmp)
            p.start()
            self.addCleanup(p.stop)

    def fake(self, binance_ok):
        now = T0 + 5 * H

        def zipped(text):
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as z:
                z.writestr("x.csv", text)
            return buf.getvalue()

        def fetch(url, params=None, raw=False):
            if "fapi.binance.com" in url:
                if not binance_ok:
                    raise OSError("451 Client Error: restricted location")
                oi, ls, tk = bn_rows(3, T0 + 2 * H)
                return {"openInterestHist": oi, "globalLongShortAccountRatio": ls,
                        "takerlongshortRatio": tk}.get(url.rsplit("/", 1)[1]) or \
                    [dict(fundingTime=T0, fundingRate="0.0001")]
            if "okx.com" in url:
                if "funding" in url:
                    return {"data": [dict(fundingTime=str(T0), fundingRate="0.0001")]}
                if "open-interest" in url:
                    return {"data": [[str(T0 + 4 * H), "7e8", "1"]]}
                if "long-short" in url:
                    return {"data": [[str(T0 + 4 * H), "1.8"]]}
                return {"data": [[str(T0 + 4 * H), "100", "120"]]}
            if "data.binance.vision" in url and "metrics" in url:
                day = url.rsplit("-metrics-", 1)[1][:10]
                return zipped(f"create_time,symbol,sum_open_interest,sum_open_interest_value,count_toptrader_long_short_ratio,"
                              f"sum_toptrader_long_short_ratio,count_long_short_ratio,sum_taker_long_short_vol_ratio\n"
                              f"{day} 10:00:00,BTCUSDT,1,900,1,1,1.2,1.1\n")
            if "fundingRate" in url:
                raise OSError("404")
            raise AssertionError(url)
        return fetch, dt.datetime.fromtimestamp(now / 1000, UTC)

    def test_fallback_backfill_and_quality(self):
        fetch, now = self.fake(binance_ok=False)
        q = derivs.run(now, fetch, ["BTC"])
        self.assertEqual(q["BTC"]["fetch"]["source"], "okx")
        self.assertIn("451", " ".join(q["BTC"]["fetch"]["errors"]))
        h = D.read(derivs.HOURLY, D.HOURLY_COLS)
        self.assertEqual(set(h["source"]), {"okx", "binance_files"})
        self.assertEqual(q["BTC"]["fetch"]["backfilled_hours"], 4)               # backfill_per_run days
        with open(derivs.QUALITY) as f:
            self.assertIn("BTC", json.load(f)["coins"])
        n1 = len(h)
        fetch2, _ = self.fake(binance_ok=True)
        q2 = derivs.run(now, fetch2, ["BTC"])
        self.assertEqual(q2["BTC"]["fetch"]["source"], "binance")
        self.assertGreater(len(D.read(derivs.HOURLY, D.HOURLY_COLS)), n1)          # history only grows

    def test_unreadable_history_is_never_replaced(self):
        with open(derivs.HOURLY, "wb") as f:
            f.write(b"\x00garbage" * 100)
        fetch, now = self.fake(binance_ok=True)
        with self.assertRaises(RuntimeError):
            derivs.run(now, fetch, ["BTC"])
        with open(derivs.HOURLY, "rb") as f:
            self.assertTrue(f.read().startswith(b"\x00garbage"))


class Wiring(unittest.TestCase):
    def test_workflows_files_and_docs(self):
        scan = read(os.path.join(ROOT, ".github", "workflows", "scan.yml"))
        self.assertLess(scan.index("python derivs.py"), scan.index("python scanner.py"))
        self.assertLess(scan.index("publish_live.py --restore"), scan.index("python derivs.py"))   # history first
        steps = yaml.safe_load(scan)["jobs"][next(iter(yaml.safe_load(scan)["jobs"]))]["steps"]
        self.assertTrue(next(s for s in steps if s.get("run") == "python derivs.py")["continue-on-error"])
        self.assertIn("strategies_lab.yaml", read(os.path.join(ROOT, ".github", "workflows", "research.yml")))
        for f in ("reports/derivs_hourly.csv.gz", "reports/funding.csv.gz"):
            self.assertIn(f, publish_live.LIVE_FILES)
            self.assertIn(f, read(os.path.join(ROOT, ".gitignore")))
        self.assertEqual(set(CFG["lab"]["factory_quota"]), set(SS.FACTORIES))
        common = read(os.path.join(ROOT, "tasks", "COMMON.md"))
        self.assertIn("factory_evidence", common)
        self.assertIn("funding_z(200)", read(os.path.join(ROOT, "strategies.yaml")))

    def test_fact_sheet_parts(self):
        rep = dict(derivs=dict(checked_utc="2026-09-25 14:00", coins=dict(BTC=dict(
            state="GOOD", hours=500, last=dict(funding_pct=0.01, ls_ratio=1.8, taker_ratio=0.95), problems=[]))))
        t = "\n".join(brain_pack.market_data_lines(rep))
        self.assertIn("BTC: GOOD · 500 h of history · funding +0.0100% · long/short 1.80", t)
        self.assertIn("not recorded yet", "\n".join(brain_pack.market_data_lines({})))
        res = dict(factories=I.factory_stats({}, {}), variant_search=dict(new=[dict(id="X-VEXIT", evidence="e")]),
                   lead_lag=dict(SOL=dict(lags={1: dict(corr=0.2, n=900, clear=True)})))
        t = "\n".join(brain_pack.factory_lines(dt.datetime(2026, 9, 27, tzinfo=UTC), res))
        self.assertIn("variant_search", t)
        self.assertIn("X-VEXIT", t)
        self.assertIn("SOL lag 1h corr +0.200 (n=900)", t)
        self.assertIn("you may add 2", t)


if __name__ == "__main__":
    unittest.main()
