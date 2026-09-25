"""Phase 15 tests: Pine Script export (engine/pine.py, pine_export.py).

The Pine text itself can only be compiled by TradingView. What is tested here:
  * every building block's translation (and what is refused, never silently skipped)
  * the same translated tree evaluated with Pine semantics (pine_sim) equals the engine, bar by bar
  * the higher-timeframe selection has no look-ahead and equals the engine's
  * every card builds a structurally sound script; the embedded engine entries are the engine's own

Run:  python -m unittest discover -s tests -v
"""
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import pine_export  # noqa: E402
import scanner  # noqa: E402
from engine import approval as AP  # noqa: E402
from engine import pine as P  # noqa: E402
from engine import regime as RG  # noqa: E402
from engine import strategy_spec as SP  # noqa: E402


def read(path):
    with open(path) as f:
        return f.read()


CFG = yaml.safe_load(read(os.path.join(ROOT, "config.yaml")))
CARDS, _, _ = SP.load(yaml.safe_load(read(os.path.join(ROOT, "strategies.yaml"))), RG.LABELS, scanner.TF_ORDER)
LEGACY = ["trend_pullback", "donchian_breakout", "rsi2_dip_buy", "bb_squeeze_breakout", "macd_trend_cross",
          "supertrend_flip", "liquidity_sweep_reversal", "ema_9_21_cross"]


def card(sid):
    return next(s for s in CARDS if s["id"] == sid)


def emit(rule):
    em = P.Emitter()
    return em, em.expr(P.parse(rule))


class Translate(unittest.TestCase):
    def test_building_blocks(self):
        cases = {
            "ema(close,20)": "f_ema(close, 20)", "sma(close,5)": "ta.sma(close, 5)", "rsi(close,2)": "f_rsi(close, 2)",
            "atr(14)": "f_atr(14)", "adx(14)": "f_adx(14)", "highest(high,20)": "ta.highest(high, 20)",
            "lowest(low,10)": "ta.lowest(low, 10)", "vol_sma(20)": "ta.sma(volume, 20)",
            "supertrend_dir(10,3)": "f_st_dir(10, 3.0)", "bars_since(close > open)": "ta.barssince(",
            "pct_rank(close,100)": "f_pct_rank(close, 100)", "bb_width(close,20,2)": "ta.stdev(close, 20, true)",
            "macd_signal(close)": "f_ema(close, 12) - f_ema(close, 26)",
        }
        for rule, want in cases.items():
            em, e = emit(rule)
            self.assertIn(want, "\n".join(em.lines) + e, rule)
        em, e = emit("prev(highest(high,20))")
        self.assertTrue(e.endswith("[1]"), e)
        em, e = emit("shift(close, 3)")
        self.assertEqual(e, "close[3]")
        em, e = emit("cross_up(ema(close,9), ema(close,21))")
        self.assertIn("v1 > v2 and v1[1] <= v2[1]", "\n".join(em.lines))
        em, e = emit("cross_down(rsi(close,14), 70)")
        self.assertIn("v1 < 70 and v1[1] >= 70", "\n".join(em.lines))
        em, e = emit("within(low <= ema(close,20), 20)")
        self.assertIn("not na(v3) and v3 < 20", "\n".join(em.lines))
        em, e = emit("htf_up")
        self.assertEqual(e, "htf_up")
        self.assertTrue(em.htf)
        em, e = emit("(close > open) & ~(volume < 5) | (abs(close - open) >= max(1, 2))")
        self.assertEqual(e, "(((close > open) and (not (volume < 5))) or (math.abs((close - open)) >= math.max(1, 2)))")
        em, e = emit("(close > open) | abs(close - open) >= 1")      # Python: | binds tighter than >= - kept
        self.assertEqual(e, "(((close > open) or math.abs((close - open))) >= 1)")
        em, e = emit("1 < close < 5")
        self.assertEqual(e, "((1 < close) and (close < 5))")

    def test_custom_pine_functions_follow_the_engine_formulas(self):
        """pine_sim mirrors these functions line by line; this pins the Pine text to the same formulas."""
        L = P.LIB
        self.assertIn("float a = 2.0 / (n + 1)", L["f_ema"])
        self.assertIn("float a = 1.0 / n", L["f_rma"])
        for k in ("f_ema", "f_rma"):
            self.assertIn("e := na(e) ? src : a * src + (1 - a) * e", L[k])
            self.assertIn("cnt >= n ? e : na", L[k])
        self.assertIn("f_rma(na(d) ? na : math.max(d, 0.0), n)", L["f_rsi"])
        self.assertIn("dn == 0 ? 100.0", L["f_rsi"])
        self.assertIn("f_rma(f_tr(), n)", L["f_atr"])
        self.assertIn("math.max(high - low, math.abs(high - close[1]), math.abs(low - close[1]))", L["f_tr"])
        self.assertIn("up > dn and up > 0 ? up : 0.0", L["f_adx"])
        self.assertIn("dn > up and dn > 0 ? dn : 0.0", L["f_adx"])
        self.assertIn("fu := ub < pfu or close[1] > pfu ? ub : pfu", L["f_st_dir"])
        self.assertIn("fl := lb > pfl or close[1] < pfl ? lb : pfl", L["f_st_dir"])
        self.assertIn("d := prevd == 1 ? (close < fl ? -1.0 : 1.0) : (close > fu ? 1.0 : -1.0)", L["f_st_dir"])
        self.assertIn("else if src[i] < src", L["f_pct_rank"])
        self.assertIn("cnt * 1.0 / (n - 1)", L["f_pct_rank"])
        for fn, body in L.items():                     # whatever a function calls is emitted with it
            used = set(re.findall(r"\b(f_\w+)\(", body)) - {fn}
            self.assertLessEqual(used, set(P.LIB_DEPS[fn]), fn)

    def test_defaults_are_the_engines(self):
        self.assertEqual(P.parse("rsi(close)"), ("call", "rsi", [("src", "close")], [14]))
        self.assertEqual(P.parse("macd_line(close)"), ("call", "macd_line", [("src", "close")], [12, 26]))
        self.assertEqual(P.parse("supertrend_dir()"), ("call", "supertrend_dir", [], [10, 3.0]))

    def test_every_call_is_hoisted_out_of_the_conditions(self):
        """Pine v6 evaluates and/or lazily: a stateful function inside a condition would skip candles."""
        for sid in LEGACY:
            s = card(sid)
            text, info = P.build(s, s["timeframes"][0], CFG, scanner.HTF.get(s["timeframes"][0], "1d"), {}, "t")
            for ln in text.splitlines():
                if re.match(r"^bool (longSig|shortSig|exitL|exitS) = ", ln):
                    self.assertNotRegex(ln, r"(f_\w+|ta\.\w+)\(", (sid, ln))

    def test_same_call_is_computed_once(self):
        em = P.Emitter()
        P.emit_rules(em, ["close > ema(close,20)", "low <= ema(close,20) * 1.002", "rsi(close,14) > 40",
                          "rsi(close,14) < 65"])
        self.assertEqual(sum("f_ema(close, 20)" in ln for ln in em.lines), 1)
        self.assertEqual(sum("f_rsi(close, 14)" in ln for ln in em.lines), 1)

    def test_what_cannot_be_translated_is_refused_by_name(self):
        for rule, name in [("smc_choch_up", "smc_choch_up"), ("displacement_up", "displacement_up"),
                           ("np.log(close) > 1", "np.log"), ("ema(close, n=20) > 1", "ema"),
                           ("ema(close, open) > 1", "ema: 'n' must be a number"), ("foo(close)", "foo"),
                           ("close % 2", "operator Mod"), ("ema(close)", "ema: 'n' missing")]:
            with self.assertRaises(P.Unsupported) as cm:
                P.parse(rule)
            self.assertIn(name, cm.exception.args[0][0], rule)

    def test_mode_per_card(self):
        for s in CARDS:
            ok, bad = P.check_card(s)
            self.assertEqual(ok, s["id"] in LEGACY, (s["id"], bad))
            if not ok:
                self.assertTrue(bad)
        ok, bad = P.check_card(card("S8-PDH-PDL-SWEEP-noSMC"))      # rules translate, the level targets do not
        self.assertIn("targets.need (a level column)", bad)
        self.assertIn("target smc_pd_mid", bad)


class SameAsEngine(unittest.TestCase):
    """The translated tree, evaluated with Pine semantics, equals the engine on synthetic candles."""

    @classmethod
    def setUpClass(cls):
        feed = scanner.Synthetic()
        cls.frames = []
        for sym, tf, htf in [("BTCUSDT", "1h", "4h"), ("SOLUSDT", "15m", "1h"), ("ETHUSDT", "4h", "1d")]:
            df = feed.klines(sym, tf, 2500).reset_index(drop=True)
            hd = feed.klines(sym, htf, 900).reset_index(drop=True)
            eng = scanner.add_htf(df.copy(), hd)
            up, dn = P.htf_sim(df, hd)
            cls.frames.append((sym, tf, eng, hd, up, dn))

    def test_higher_timeframe_trend(self):
        for sym, tf, eng, hd, up, dn in self.frames:
            np.testing.assert_array_equal(up, eng["htf_up"].to_numpy(), sym)
            np.testing.assert_array_equal(dn, eng["htf_down"].to_numpy(), sym)
            self.assertTrue(up.any() and dn.any(), sym)

    def test_higher_timeframe_has_no_look_ahead(self):
        sym, tf, eng, hd, up, dn = self.frames[0]
        cut = 1800
        t = eng["close_time"].iloc[cut]
        up2, _ = P.htf_sim(eng.iloc[:cut + 1], hd[hd["close_time"] <= t])      # only candles closed by then
        np.testing.assert_array_equal(up2, up[:cut + 1])

    def test_every_rule_of_every_translatable_card(self):
        n = 0
        for sym, tf, eng, *_ in self.frames:
            ns = scanner.make_namespace(eng)
            for sid in LEGACY:
                s = card(sid)
                for k in ("long", "short", "exit_long", "exit_short"):
                    for r in s.get(k) or []:
                        e = scanner.eval_rules([r], ns, eng.index)
                        p = P.pine_sim(r, eng).astype(bool)
                        self.assertEqual(int((e != p).sum()), 0, (sym, sid, r))
                        n += int(e.sum())
                rule = s["stop"].get("long_level")
                if rule:
                    self.fail("legacy cards use ATR stops")
        self.assertGreater(n, 200, "the rules must fire often enough for the comparison to mean something")

    def test_ties_and_flat_candles(self):
        """Repeated prices (ties) and flat candles - where < vs <= and divide-by-zero guards matter."""
        feed = scanner.Synthetic()
        df = feed.klines("BTCUSDT", "1h", 600).reset_index(drop=True)
        df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].round(0)
        df.loc[200:260, ["open", "high", "low", "close"]] = 100.0
        df["htf_up"] = df["htf_down"] = True
        ns = scanner.make_namespace(df)
        for expr in ["pct_rank(close,5)", "rsi(close,14)", "adx(14)", "supertrend_dir(10,3)", "bb_width(close,20,2)"]:
            e = np.asarray(eval(expr, {"__builtins__": {}}, ns), dtype=float)
            p = np.asarray(P.pine_sim(expr, df), dtype=float)
            np.testing.assert_array_equal(np.isnan(e), np.isnan(p), expr)
            np.testing.assert_allclose(e[~np.isnan(e)], p[~np.isnan(p)], atol=1e-9, err_msg=expr)

    def test_indicator_values(self):
        for sym, tf, eng, *_ in self.frames:
            ns = scanner.make_namespace(eng)
            for expr in ["rsi(close,14)", "rsi(close,2)", "atr(14)", "adx(14)", "supertrend_dir(10,3)",
                         "pct_rank(prev(bb_width(close,20,2)),100)", "macd_hist(close)", "ema(close,200)",
                         "bb_lower(close,20,2)", "bars_since(close > open)", "vol_sma(20)", "lowest(low,20)"]:
                e = np.asarray(eval(expr, {"__builtins__": {}}, ns), dtype=float)
                p = np.asarray(P.pine_sim(expr, eng), dtype=float)
                np.testing.assert_array_equal(np.isnan(e), np.isnan(p), (sym, expr))
                np.testing.assert_allclose(e[~np.isnan(e)], p[~np.isnan(p)], rtol=0, atol=1e-9, err_msg=f"{sym} {expr}")


class Script(unittest.TestCase):
    SIG = {"BTC": [dict(entry_ms=1_790_000_000_000, dir=1, stop=100.0, tps=[110.0, 120.0]),
                   dict(entry_ms=1_780_000_000_000, dir=-1, stop=200.0, tps=[180.0])],
           "ETH": [dict(entry_ms=1_785_000_000_000, dir=1, stop=10.0, tps=[11.0, 12.0, 13.0])]}

    def test_every_card_and_timeframe_builds_a_sound_script(self):
        for s in CARDS:
            for tf in s["timeframes"]:
                text, info = P.build(s, tf, CFG, scanner.HTF.get(tf, "1d"), self.SIG, "2026-09-25 00:00")
                self.assertEqual(P.structure_problems(text), [], (s["id"], tf))
                self.assertIn(f'timeframe.period != "{P.PINE_TF[tf]}"', text)
                self.assertIn("//@version=6", text)
                self.assertIn("Not financial advice", text)
                self.assertIn(SP.fingerprint(s), text)
                self.assertEqual(info["mode"], "RULES" if s["id"] in LEGACY else "REPLAY")
                for fn in re.findall(r"\b(f_\w+)\(", text):              # every custom function is defined
                    self.assertRegex(text, rf"(?m)^{fn}\(", (s["id"], fn))
                self.assertEqual(text.count("strategy.entry("), 1)

    def test_structure_check_catches_mistakes(self):
        self.assertTrue(P.structure_problems("//@version=6\nx = (1\n"))
        self.assertTrue(P.structure_problems("//@version=6\nbool x = a & b\n"))
        self.assertTrue(P.structure_problems("x = 1\n"))
        self.assertTrue(P.structure_problems("//@version=6\nif x\n   y := 1\n"))
        self.assertEqual(P.structure_problems("//@version=6\n// a & b in a comment\nx = (1)\n"), [])

    def test_costs_plan_and_embedded_entries(self):
        s = card("donchian_breakout")
        text, info = P.build(s, "4h", CFG, "1d", self.SIG, "now")
        c = CFG["costs"]["long"]
        self.assertIn(f"commission_value = {c['taker_fee_pct'] + c['slippage_pct']:.4f}", text)
        self.assertIn(f"int HOLD = {s['time_stop_bars']}", text)
        self.assertIn("array<float> TP_R = array.from(1.0, 2.0, 3.0)", text)
        self.assertIn("array<float> SPLIT = array.from(0.4, 0.3, 0.3)", text)
        self.assertIn('request.security(syminfo.tickerid, "D", f_htf(), lookahead = barmerge.lookahead_on)', text)
        for ln in ["bool htfNow = htc == time_close", "float hc = htfNow ? hc0 : hc1", "float h20 = htfNow ? h20_0 : h20_1",
                   "float h50 = htfNow ? h50_0 : h50_1", "    [close, e20, e50, close[1], e20[1], e50[1], time_close]"]:
            self.assertIn(ln, text.splitlines())             # current HTF candle only when it closes on this candle
        self.assertIn('syminfo.basecurrency == "BTC"', text)
        self.assertIn("eT := array.from(1780000000000, 1790000000000)", text)       # sorted by time
        self.assertIn("eP3 := array.from(float(na), float(na))", text)
        self.assertIn("f_R(d, e) => 2.0 * ", text)
        self.assertEqual((info["signals"], info["coins"]), (3, ["BTC", "ETH"]))
        text, info = P.build(card("S6-OB-FVG"), "15m", CFG, "1h", {}, "now")
        self.assertIn("array<float> SPLIT = array.from(0.5, 0.5, 0.0)", text)        # the card's split in replay
        self.assertIn("REPLAY mode", text)
        self.assertIn("h4_bull_ob_high", text.split("//@version=6")[0])              # the header names what is missing
        self.assertIn("eT := array.new<int>()", text)

    def test_structure_stop_width_check(self):
        s = dict(card("donchian_breakout"), stop={"method": "structure", "long_level": "lowest(low,10)",
                                                  "short_level": "highest(high,10)", "buffer_atr": 0.2,
                                                  "max_width_atr": 3.0})
        text, info = P.build(s, "4h", CFG, "1d", {}, "now")
        self.assertEqual(info["mode"], "RULES")
        self.assertIn("float MAXW = 3.0", text)
        self.assertIn("r <= MAXW * ", text)
        self.assertRegex(text, r"f_R\(d, e\) => d == 1 \? e - \(v\d+ - 0.2 \* v\d+\) : \(v\d+ \+ 0.2 \* v\d+\) - e")

    def test_signals_from_trades(self):
        trades = {"BTC": [dict(entry_time=2, dir=1, entry=100.0, R=5.0, tp1=105.0, tps=[105.0, 110.0]),
                          dict(entry_time=1, dir=-1, entry=50.0, R=2.0, tp1=48.0)], "ETH": []}
        out = P.signals_from_trades(trades, keep=1)
        self.assertEqual(out, {"BTC": [dict(entry_ms=2, dir=1, stop=95.0, tps=[105.0, 110.0])]})
        self.assertEqual(P.signals_from_trades(trades)["BTC"][0], dict(entry_ms=1, dir=-1, stop=52.0, tps=[48.0]))

    def test_backtest_trades_carry_their_targets(self):
        feed = scanner.Synthetic()
        df = feed.klines("BTCUSDT", "1h", 1500).reset_index(drop=True)
        df["_atr"] = scanner.make_namespace(df)["atr"](14)
        L = np.zeros(len(df), bool)
        L[300::97] = True
        tr = scanner.backtest(df, L, np.zeros(len(df), bool), None, None, card("rsi2_dip_buy"), CFG, "1h")
        self.assertTrue(tr)
        for t in tr:
            self.assertEqual(len(t["tps"]), 3)
            self.assertAlmostEqual(t["tps"][0], t["tp1"])


class Export(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_write_embeds_the_engines_trades(self):
        s = card("ema_9_21_cross")
        trades = {"BTC": [dict(entry_time=1_790_000_000_000, dir=1, entry=100.0, R=2.0, tp1=102.0, tps=[102.0])]}
        path, info = pine_export.write(s, "1h", CFG, trades, "2026-09-25 00:00", self.tmp, "test")
        self.assertEqual(os.path.basename(path), "ema_9_21_cross_v1.0_1h.pine")
        text = read(path)
        self.assertIn("eS := array.from(98.0)", text)
        self.assertEqual(info["mode"], "RULES")

    def test_offline_end_to_end(self):
        p = subprocess.run([sys.executable, "pine_export.py", "donchian_breakout", "1.0", "4h", "--offline",
                            "--coins", "2", "--bars", "900"], cwd=ROOT, capture_output=True, text=True, timeout=600)
        self.assertEqual(p.returncode, 0, p.stderr[-2000:])
        self.assertIn("RULES mode", p.stdout)
        text = read(os.path.join(ROOT, "reports/pine_offline/donchian_breakout_v1.0_4h.pine"))
        n = int(re.search(r"(\d+) engine entries embedded", p.stdout).group(1))
        self.assertEqual(n, sum(len(re.findall(r"\d{13}", ln)) for ln in text.splitlines() if "eT := " in ln))
        for bad in [["nope", "1.0", "4h"], ["donchian_breakout", "1.0", "15m"]]:
            p = subprocess.run([sys.executable, "pine_export.py", *bad, "--offline"], cwd=ROOT, capture_output=True,
                               text=True, timeout=120)
            self.assertNotEqual(p.returncode, 0, bad)

    def test_pack_explains_how_to_see_it_on_tradingview(self):
        from test_brain import Approval
        a = Approval()
        text = "\n".join(AP.pack(a.cell(), a.spec(), [], {}, AP.settings(None), "2026-10-04 00:50"))
        self.assertIn('"Pine export" → Run workflow with `S6-OB-FVG` / `1.0` / `15m`', text)
        self.assertIn("reports/pine/S6-OB-FVG_v1.0_15m.pine", text)
        self.assertEqual(P.filename("S6-OB-FVG", "1.0", "15m"), "S6-OB-FVG_v1.0_15m.pine")

    def test_research_exports_only_approved(self):
        import research
        s = card("donchian_breakout")
        trades = [dict(entry_time=1_790_000_000_000, dir=-1, entry=100.0, R=2.0, tp1=98.0, tps=[98.0, 96.0, 94.0])]
        cells = {"donchian_breakout@1.0|4h": dict(strategy="donchian_breakout", version="1.0", tf="4h",
                                                   status="APPROVED"),
                 "donchian_breakout@1.0|1h": dict(strategy="donchian_breakout", version="1.0", tf="1h",
                                                   status="PAPER_TRADING"),
                 "ghost@1.0|1h": dict(strategy="ghost", version="1.0", tf="1h", status="APPROVED")}
        per = {("donchian_breakout", "1.0", "4h"): {"BTC": trades}}
        out = research.export_approved(cells, per, {"donchian_breakout@1.0": s}, CFG, "now", self.tmp)
        self.assertEqual(os.listdir(self.tmp), ["donchian_breakout_v1.0_4h.pine"])
        self.assertEqual(out[0]["mode"], "RULES")
        self.assertIn("error", out[1])                                     # reported, never fatal
        self.assertIn("eS := array.from(102.0)", read(os.path.join(self.tmp, "donchian_breakout_v1.0_4h.pine")))

    def test_report_lists_approved_scripts(self):
        out = []
        g = dict(experiments=1, changes=[], not_run={}, rule_errors={}, idle=[],
                 approval=dict(pine=[dict(key="a@1.0|4h", file="reports/pine/a_v1.0_4h.pine", mode="RULES"),
                                     dict(key="b@1.0|1h", error="boom")]))
        scanner.render_lifecycle(g, [], out.append)
        text = "\n".join(out)
        self.assertIn("`reports/pine/a_v1.0_4h.pine` (RULES mode)", text)
        self.assertIn("export failed: boom", text)

    def test_workflow_passes_inputs_safely(self):
        wf = yaml.safe_load(read(os.path.join(ROOT, ".github/workflows/pine.yml")))
        steps = wf["jobs"]["pine"]["steps"]
        run = next(s for s in steps if s.get("name", "").startswith("Export"))
        self.assertNotIn("${{", run["run"], "inputs go through env, never straight into the shell")
        self.assertEqual(run["env"]["STRATEGY"], "${{ inputs.strategy }}")


if __name__ == "__main__":
    unittest.main()
