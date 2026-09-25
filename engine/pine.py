"""
Pine Script export (AGENT_PROMPT.md sections 2 and 27.4 step 15) - Phase 15.

TradingView is the operator's "eyes": a strategy card from strategies.yaml becomes a Pine Script v6 *strategy*
to paste into TradingView's Pine editor, as a visual CROSS-CHECK. TradingView never sends signals; the engine
stays the only source of numbers.

Two modes, chosen automatically:
  RULES  - every building block of the card's entry / exit rules, stop and targets has an exact Pine translation
           (below). Pine computes the signals itself; the engine's own entries are embedded as markers, and a
           table counts "matched / only engine / only Pine" (Pine cannot apply the engine's regime gate, so
           "only Pine" entries are expected - the table says so).
  REPLAY - some block cannot be translated exactly (SMC detectors, feature-engine columns, level columns):
           re-writing them in Pine would be a second, different engine. Instead Pine enters on the engine's own
           embedded signals with the engine's stop / target prices and manages them itself, so TradingView's
           tester is an independent check of fills, stops and targets.

Translation: a rule is parsed (Python ast) into a small tree; every function call is hoisted into its own global
variable (Pine v6 evaluates `and` / `or` lazily, and stateful functions must run on every bar). Engine formulas
that differ from TradingView's built-ins (EMA / RMA seeding, RSI, ATR, ADX, supertrend, percent rank) get small
custom Pine functions written to the engine's exact formula (scanner.make_namespace). pine_sim() evaluates the
same tree with Pine semantics in Python - the tests compare it with the engine, bar by bar.

Pure functions; no internet.
"""
import ast
import math
import re

import numpy as np
import pandas as pd

from engine import strategy_spec as sspec

PINE_TF = {"5m": "5", "15m": "15", "30m": "30", "1h": "60", "4h": "240", "1d": "D"}
SOURCES = ["open", "high", "low", "close", "volume"]
# name: (series args, [(param, default)])
FUNCS = {
    "ema": (1, [("n", None)]), "sma": (1, [("n", None)]), "rsi": (1, [("n", 14)]),
    "atr": (0, [("n", 14)]), "adx": (0, [("n", 14)]),
    "macd_line": (1, [("f", 12), ("s", 26)]), "macd_signal": (1, [("f", 12), ("s", 26), ("sig", 9)]),
    "macd_hist": (1, [("f", 12), ("s", 26), ("sig", 9)]),
    "bb_mid": (1, [("n", 20)]), "bb_upper": (1, [("n", 20), ("k", 2)]), "bb_lower": (1, [("n", 20), ("k", 2)]),
    "bb_width": (1, [("n", 20), ("k", 2)]),
    "highest": (1, [("n", None)]), "lowest": (1, [("n", None)]), "vol_sma": (0, [("n", 20)]),
    "pct_rank": (1, [("n", 100)]), "supertrend_dir": (0, [("n", 10), ("mult", 3)]),
    "within": (1, [("n", None)]), "bars_since": (1, []),
    "cross_up": (2, []), "cross_down": (2, []),
    "shift": (1, [("n", 1)]), "prev": (1, []),
}
MATH = {"abs": "math.abs", "min": "math.min", "max": "math.max"}
CMP = {ast.Gt: ">", ast.GtE: ">=", ast.Lt: "<", ast.LtE: "<=", ast.Eq: "==", ast.NotEq: "!="}
BIN = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}
INT_PARAMS = {"n", "f", "s", "sig"}


class Unsupported(Exception):
    pass


# ---------------------------------------------------------------------------------------------------------------
# 1. rule text -> tree
# ---------------------------------------------------------------------------------------------------------------
def _num(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        v = _num(node.operand)
        return None if v is None else -v
    return None


def parse(text):
    """One rule / level expression -> tree. Raises Unsupported(names) for anything without an exact translation."""
    try:
        node = ast.parse(str(text), mode="eval").body
    except SyntaxError as e:
        raise Unsupported([f"cannot read '{text}': {e.msg}"])
    return _tree(node)


def _tree(n):
    v = _num(n)
    if v is not None:
        return ("num", v)
    if isinstance(n, ast.Name):
        if n.id in SOURCES:
            return ("src", n.id)
        if n.id in ("htf_up", "htf_down"):
            return ("htf", n.id[4:])
        raise Unsupported([n.id])
    if isinstance(n, ast.Call):
        if not isinstance(n.func, ast.Name):
            raise Unsupported([ast.unparse(n.func)])
        name = n.func.id
        if name in MATH:
            return ("math", name, [_tree(a) for a in n.args])
        if name not in FUNCS or n.keywords:
            raise Unsupported([name])
        nser, params = FUNCS[name]
        if len(n.args) < nser or len(n.args) > nser + len(params):
            raise Unsupported([f"{name} with {len(n.args)} arguments"])
        series = [_tree(a) for a in n.args[:nser]]
        vals = []
        for i, (p, default) in enumerate(params):
            if nser + i < len(n.args):
                x = _num(n.args[nser + i])
                if x is None:
                    raise Unsupported([f"{name}: '{p}' must be a number"])
            elif default is None:
                raise Unsupported([f"{name}: '{p}' missing"])
            else:
                x = default
            vals.append(int(x) if p in INT_PARAMS else float(x))
        if name == "prev":
            return ("hist", series[0], 1)
        if name == "shift":
            return ("hist", series[0], vals[0])
        return ("call", name, series, vals)
    if isinstance(n, ast.BinOp):
        if type(n.op) in BIN:
            return ("bin", BIN[type(n.op)], _tree(n.left), _tree(n.right))
        if isinstance(n.op, ast.BitAnd):
            return ("and", _tree(n.left), _tree(n.right))
        if isinstance(n.op, ast.BitOr):
            return ("or", _tree(n.left), _tree(n.right))
        raise Unsupported([f"operator {type(n.op).__name__}"])
    if isinstance(n, ast.BoolOp):
        parts = [_tree(v) for v in n.values]
        out = parts[0]
        for p in parts[1:]:
            out = ("and" if isinstance(n.op, ast.And) else "or", out, p)
        return out
    if isinstance(n, ast.UnaryOp):
        if isinstance(n.op, (ast.Invert, ast.Not)):
            return ("not", _tree(n.operand))
        if isinstance(n.op, ast.USub):
            return ("neg", _tree(n.operand))
        raise Unsupported([f"operator {type(n.op).__name__}"])
    if isinstance(n, ast.Compare):
        out, left = None, _tree(n.left)
        for op, right in zip(n.ops, n.comparators):
            if type(op) not in CMP:
                raise Unsupported([f"comparison {type(op).__name__}"])
            r = _tree(right)
            c = ("cmp", CMP[type(op)], left, r)
            out = c if out is None else ("and", out, c)
            left = r
        return out
    raise Unsupported([ast.unparse(n)])


def check_card(spec):
    """(rules_ok, unsupported names) for the card's entry / exit rules, stop and targets."""
    bad = []

    def need(text):
        try:
            parse(text)
        except Unsupported as e:
            bad.extend(e.args[0])
    for k in ("long", "short", "exit_long", "exit_short"):
        for r in spec.get(k) or []:
            need(r)
    st = spec["stop"]
    if st["method"] == "structure":
        need(st["long_level"])
        need(st["short_level"])
    tg = spec.get("targets")
    if tg:
        if tg.get("need"):
            bad.append("targets.need (a level column)")
        for item in (tg.get("long") or []) + (tg.get("short") or []):
            if not re.match(r"^\s*\d+(\.\d+)?R\s*$", str(item)):
                bad.append(f"target {item}")
    return not bad, sorted(set(bad))


# ---------------------------------------------------------------------------------------------------------------
# 2. tree -> Pine (with hoisting)
# ---------------------------------------------------------------------------------------------------------------
LIB = {
    "f_ema": """f_ema(src, n) =>
    // pandas ewm(span=n, adjust=False, min_periods=n): starts at the first value, nothing before n values
    float a = 2.0 / (n + 1)
    var float e = na
    var int cnt = 0
    if not na(src)
        e := na(e) ? src : a * src + (1 - a) * e
        cnt += 1
    cnt >= n ? e : na""",
    "f_rma": """f_rma(src, n) =>
    // Wilder smoothing as the engine does it (pandas ewm(alpha=1/n, adjust=False, min_periods=n))
    float a = 1.0 / n
    var float e = na
    var int cnt = 0
    if not na(src)
        e := na(e) ? src : a * src + (1 - a) * e
        cnt += 1
    cnt >= n ? e : na""",
    "f_tr": """f_tr() =>
    na(close[1]) ? high - low : math.max(high - low, math.abs(high - close[1]), math.abs(low - close[1]))""",
    "f_atr": """f_atr(n) =>
    f_rma(f_tr(), n)""",
    "f_rsi": """f_rsi(src, n) =>
    float d = src - src[1]
    float up = f_rma(na(d) ? na : math.max(d, 0.0), n)
    float dn = f_rma(na(d) ? na : math.max(-d, 0.0), n)
    na(up) or na(dn) ? na : dn == 0 ? 100.0 : 100.0 - 100.0 / (1.0 + up / dn)""",
    "f_adx": """f_adx(n) =>
    float up = high - high[1]
    float dn = low[1] - low
    float pdm = not na(up) and not na(dn) and up > dn and up > 0 ? up : 0.0
    float mdm = not na(up) and not na(dn) and dn > up and dn > 0 ? dn : 0.0
    float a = f_rma(f_tr(), n)
    float pdi = 100 * f_rma(pdm, n) / a
    float mdi = 100 * f_rma(mdm, n) / a
    float dx = na(pdi) or na(mdi) or pdi + mdi == 0 ? na : 100 * math.abs(pdi - mdi) / (pdi + mdi)
    f_rma(dx, n)""",
    "f_st_dir": """f_st_dir(n, mult) =>
    // the engine's supertrend direction (+1 up, -1 down) - TradingView's ta.supertrend uses the opposite sign
    float a = f_atr(n)
    float mid = (high + low) / 2
    float ub = mid + mult * a
    float lb = mid - mult * a
    var float fu = na
    var float fl = na
    var float d = na
    float pfu = fu
    float pfl = fl
    float pd = d
    if na(a)
        fu := ub
        fl := lb
        d := na
    else
        if not na(pfu)
            fu := ub < pfu or close[1] > pfu ? ub : pfu
            fl := lb > pfl or close[1] < pfl ? lb : pfl
        else
            fu := ub
            fl := lb
        float prevd = na(pd) ? 1.0 : pd
        d := prevd == 1 ? (close < fl ? -1.0 : 1.0) : (close > fu ? 1.0 : -1.0)
    d""",
    "f_pct_rank": """f_pct_rank(src, n) =>
    // share of the previous n-1 values below this one (the engine's pct_rank)
    float r = na
    if bar_index >= n - 1
        int cnt = 0
        bool bad = na(src)
        for i = 1 to n - 1
            if na(src[i])
                bad := true
            else if src[i] < src
                cnt += 1
        r := bad ? na : cnt * 1.0 / (n - 1)
    r""",
}
LIB_DEPS = {"f_atr": ["f_rma", "f_tr"], "f_rsi": ["f_rma"], "f_adx": ["f_rma", "f_tr"],
            "f_st_dir": ["f_atr", "f_rma", "f_tr"], "f_ema": [], "f_rma": [], "f_tr": [], "f_pct_rank": []}
LIB_ORDER = ["f_ema", "f_rma", "f_tr", "f_atr", "f_rsi", "f_adx", "f_st_dir", "f_pct_rank"]


def _fmtnum(v):
    if isinstance(v, int) or float(v).is_integer() and abs(v) < 1e15:
        return str(int(v)) if isinstance(v, int) else f"{float(v):.1f}"
    return repr(float(v))


class Emitter:
    """Builds the hoisted variable lines; one variable per distinct function call / needed sub-expression."""

    def __init__(self, prefix="v"):
        self.lines, self.memo, self.lib, self.htf = [], {}, set(), False
        self.prefix, self.count = prefix, 0

    def hoist(self, key, expr, kind="float"):
        if key not in self.memo:
            self.count += 1
            name = f"{self.prefix}{self.count}"
            self.memo[key] = name
            self.lines.append(f"{kind} {name} = {expr}")
        return self.memo[key]

    def var(self, t):
        """A plain name holding t (so it can take a history reference or be passed on)."""
        if t[0] in ("src", "num"):
            return t[1] if t[0] == "src" else _fmtnum(t[1])
        e = self.expr(t)
        if re.match(r"^[A-Za-z_]\w*$", e):
            return e
        return self.hoist(("var", repr(t)), e, "bool" if is_bool(t) else "float")

    def use(self, *names):
        for n in names:
            self.lib.add(n)
            self.lib.update(LIB_DEPS[n])

    def expr(self, t):
        k = t[0]
        if k == "num":
            return _fmtnum(t[1])
        if k == "src":
            return t[1]
        if k == "htf":
            self.htf = True
            return f"htf_{t[1]}"
        if k == "hist":
            return self.var(t[1]) if t[1][0] == "num" else f"{self.var(t[1])}[{t[2]}]"
        if k == "bin":
            return f"({self.expr(t[2])} {t[1]} {self.expr(t[3])})"
        if k == "neg":
            return f"(-{self.expr(t[1])})"
        if k == "cmp":
            return f"({self.expr(t[2])} {t[1]} {self.expr(t[3])})"
        if k in ("and", "or"):
            return f"({self.expr(t[1])} {k} {self.expr(t[2])})"
        if k == "not":
            return f"(not {self.expr(t[1])})"
        if k == "math":
            return f"{MATH[t[1]]}({', '.join(self.expr(a) for a in t[2])})"
        if k == "call":
            return self.call(t)
        raise ValueError(t)

    def call(self, t):
        _, name, ser, vals = t
        key = ("call", repr(t))
        if key in self.memo:
            return self.memo[key]
        a = [self.var(s) for s in ser]
        p = [_fmtnum(v) for v in vals]
        if name == "ema":
            self.use("f_ema")
            e = f"f_ema({a[0]}, {p[0]})"
        elif name == "sma":
            e = f"ta.sma({a[0]}, {p[0]})"
        elif name == "rsi":
            self.use("f_rsi")
            e = f"f_rsi({a[0]}, {p[0]})"
        elif name == "atr":
            self.use("f_atr")
            e = f"f_atr({p[0]})"
        elif name == "adx":
            self.use("f_adx")
            e = f"f_adx({p[0]})"
        elif name in ("macd_line", "macd_signal", "macd_hist"):
            self.use("f_ema")
            line = self.hoist(("macd", a[0], p[0], p[1]), f"f_ema({a[0]}, {p[0]}) - f_ema({a[0]}, {p[1]})")
            if name == "macd_line":
                return self.memo.setdefault(key, line)
            sig = self.hoist(("macds", line, p[2]), f"f_ema({line}, {p[2]})")
            if name == "macd_signal":
                return self.memo.setdefault(key, sig)
            e = f"{line} - {sig}"
        elif name in ("bb_mid", "bb_upper", "bb_lower", "bb_width"):
            mid = self.hoist(("sma", a[0], p[0]), f"ta.sma({a[0]}, {p[0]})")
            if name == "bb_mid":
                return self.memo.setdefault(key, mid)
            sd = self.hoist(("stdev", a[0], p[0]), f"ta.stdev({a[0]}, {p[0]}, true)")
            up = self.hoist(("bbu", mid, sd, p[1]), f"{mid} + {p[1]} * {sd}")
            lo = self.hoist(("bbl", mid, sd, p[1]), f"{mid} - {p[1]} * {sd}")
            if name == "bb_upper":
                return self.memo.setdefault(key, up)
            if name == "bb_lower":
                return self.memo.setdefault(key, lo)
            e = f"({up} - {lo}) / {mid}"
        elif name == "highest":
            e = f"ta.highest({a[0]}, {p[0]})"
        elif name == "lowest":
            e = f"ta.lowest({a[0]}, {p[0]})"
        elif name == "vol_sma":
            e = f"ta.sma(volume, {p[0]})"
        elif name == "pct_rank":
            self.use("f_pct_rank")
            e = f"f_pct_rank({a[0]}, {p[0]})"
        elif name == "supertrend_dir":
            self.use("f_st_dir")
            e = f"f_st_dir({p[0]}, {p[1]})"
        elif name == "bars_since":
            e = f"ta.barssince({a[0]})"
        elif name == "within":
            bs = self.hoist(("bs", a[0]), f"ta.barssince({a[0]})")
            return self.hoist(key, f"not na({bs}) and {bs} < {p[0]}", "bool")
        elif name in ("cross_up", "cross_down"):
            gt, ge = (">", "<=") if name == "cross_up" else ("<", ">=")
            b1 = a[1] if ser[1][0] == "num" else f"{a[1]}[1]"
            return self.hoist(key, f"{a[0]} {gt} {a[1]} and {a[0]}[1] {ge} {b1}", "bool")
        else:
            raise ValueError(name)
        return self.hoist(key, e)


def is_bool(t):
    return t[0] in ("cmp", "and", "or", "not", "htf") or (t[0] == "call" and t[1] in ("within", "cross_up",
                                                                                         "cross_down"))


def emit_rules(em, rules):
    """ALL rules true -> 'a and b and ...' (each rule a bool expression)."""
    if not rules:
        return "false"
    parts = []
    for r in rules:
        t = parse(r)
        e = em.expr(t)
        parts.append(e if is_bool(t) else f"({e} != 0)")
    return " and ".join(parts)


# ---------------------------------------------------------------------------------------------------------------
# 3. the whole script
# ---------------------------------------------------------------------------------------------------------------
def _fl(v):
    """A Pine float literal (always with a decimal point, so array.from() builds array<float>)."""
    t = f"{float(v):.10g}"
    return t if any(ch in t for ch in ".en") else t + ".0"


def _arr(vals, kind):
    if not vals:
        return f"array.new<{kind}>()"
    if kind == "int":
        return "array.from(" + ", ".join(str(int(v)) for v in vals) + ")"
    return "array.from(" + ", ".join("float(na)" if v is None or not math.isfinite(v) else _fl(v) for v in vals) + ")"


def engine_arrays(signals):
    """signals: {coin: [dict(entry_ms, dir, stop, tps)]} -> Pine lines that fill the arrays for the chart's coin."""
    L = ["var array<int> eT = array.new<int>()", "var array<int> eD = array.new<int>()",
         "var array<float> eS = array.new<float>()", "var array<float> eP1 = array.new<float>()",
         "var array<float> eP2 = array.new<float>()", "var array<float> eP3 = array.new<float>()",
         "if barstate.isfirst"]
    coins = sorted(signals)
    if not coins:
        L.append("    eT := array.new<int>()")
    for i, c in enumerate(coins):
        s = sorted(signals[c], key=lambda x: x["entry_ms"])
        tp = lambda k: [x["tps"][k] if len(x.get("tps") or []) > k else None for x in s]
        L += [f"    {'if' if i == 0 else 'else if'} syminfo.basecurrency == \"{c}\"",
              f"        eT := {_arr([x['entry_ms'] for x in s], 'int')}",
              f"        eD := {_arr([x['dir'] for x in s], 'int')}",
              f"        eS := {_arr([x.get('stop') for x in s], 'float')}",
              f"        eP1 := {_arr(tp(0), 'float')}", f"        eP2 := {_arr(tp(1), 'float')}",
              f"        eP3 := {_arr(tp(2), 'float')}"]
    return L


def build(spec, tf, cfg, htf_tf, signals, now_txt, coins_note=""):
    """The Pine script (text) + a summary dict(mode, unsupported, coins, signals)."""
    rules_ok, bad = check_card(spec)
    mode = "RULES" if rules_ok else "REPLAY"
    tp_plan = cfg["trade_plan"]
    tg = spec.get("targets")
    tps_r, split = [float(x) for x in tp_plan["tp_r"]], [float(x) for x in tp_plan["tp_split"]]
    if tg:                           # REPLAY takes the target prices from the engine; the split is the card's
        split = [float(x) for x in tg["split"]]
        if rules_ok:
            tps_r = [float(str(x).strip()[:-1]) for x in tg["long"]]
    split = (split + [0.0, 0.0, 0.0])[:3]
    tps_r = (tps_r + [0.0, 0.0, 0.0])[:3]
    long_cost = cfg["costs"]["long"]
    commission = float(long_cost["taker_fee_pct"]) + float(long_cost["slippage_pct"])
    slip = {1: float(cfg["costs"]["long"]["slippage_pct"]) / 100, -1: float(cfg["costs"]["short"]["slippage_pct"]) / 100}
    ptf = PINE_TF[tf]
    title = f"TradeSentry {spec['id']} v{spec['version']} {tf}"
    n_sig = sum(len(v) for v in signals.values())
    H = [f"// {title} - {mode} mode",
         f"// Exported by the engine on {now_txt} UTC (engine/pine.py). Do not edit - export again instead.",
         f"// Card fingerprint: {sspec.fingerprint(spec)} · open it on a {tf} chart (BINANCE:<COIN>USDT).",
         "// A CROSS-CHECK for your eyes (AGENT_PROMPT.md section 2): TradingView never sends signals; the engine's",
         "// numbers stay the reference. Research signal. Not financial advice.",
         "//"]
    if mode == "RULES":
        H += ["// RULES mode: Pine computes the entry / exit rules itself with the engine's exact formulas.",
              "// Pine cannot apply the engine's regime gate (2 of 1D/4H/1H + weekly veto), data checks or risk engine,",
              "// so it shows MORE entries than the engine: the table counts matched / only engine / only Pine."]
    else:
        H += ["// REPLAY mode: these parts have no exact Pine translation, so Pine does NOT recompute the rules:",
              f"//   {', '.join(bad)}",
              "// Pine enters on the engine's own signals (embedded below) with the engine's stop and targets, and",
              "// TradingView's tester manages the trades independently (fills, stops, targets, time stop)."]
    H += ["// Known small differences: entries fill at the next open without slippage (costs are charged as one",
          f"// commission of {commission:.2f}% per side = long taker fee + slippage); when a stop and a target are both",
          "// touched in one candle the engine assumes the stop, TradingView's broker emulator may not; averages",
          "// can differ in the first candles of the chart. Engine signals embedded: "
          f"{n_sig} ({coins_note or ', '.join(sorted(signals)) or 'none'})."]
    S = [*H, "//@version=6",
         f"strategy(\"{title}\", overlay = true, initial_capital = 10000, pyramiding = 0, "
         f"commission_type = strategy.commission.percent, commission_value = {commission:.4f}, slippage = 0, "
         "default_qty_type = strategy.fixed, default_qty_value = 1, max_labels_count = 500, "
         "process_orders_on_close = false)", ""]
    em = Emitter()
    body = []
    if mode == "RULES":
        long_s, short_s = emit_rules(em, spec["long"]), emit_rules(em, spec["short"])
        exl = emit_rules(em, spec.get("exit_long") or [])
        exs = emit_rules(em, spec.get("exit_short") or [])
        em.use("f_atr")
        atr_v = em.hoist(("call", repr(("call", "atr", [], [14]))), "f_atr(14)")
        st = spec["stop"]
        if st["method"] == "structure":
            lv_l, lv_s = em.var(parse(st["long_level"])), em.var(parse(st["short_level"]))
    lib = [LIB[k] for k in LIB_ORDER if k in em.lib]
    S += lib + ([""] if lib else [])
    if em.htf:
        S += ["// higher timeframe trend, exactly as the engine: the newest " + htf_tf + " candle CLOSED by this "
              "candle's close (no look-ahead)",
              "f_htf() =>",
              "    float e20 = f_ema(close, 20)",
              "    float e50 = f_ema(close, 50)",
              "    [close, e20, e50, close[1], e20[1], e50[1], time_close]",
              f"[hc0, h20_0, h50_0, hc1, h20_1, h50_1, htc] = request.security(syminfo.tickerid, \"{PINE_TF[htf_tf]}\", "
              "f_htf(), lookahead = barmerge.lookahead_on)",
              "bool htfNow = htc == time_close",
              "float hc = htfNow ? hc0 : hc1",
              "float h20 = htfNow ? h20_0 : h20_1",
              "float h50 = htfNow ? h50_0 : h50_1",
              "bool htf_up = not na(h50) and not na(h20) and hc > h50 and h20 > h50",
              "bool htf_down = not na(h50) and not na(h20) and hc < h50 and h20 < h50", ""]
        if "f_ema" not in em.lib:
            S[S.index("f_htf() =>"):S.index("f_htf() =>")] = [LIB["f_ema"], ""]
    S += [f"if timeframe.period != \"{ptf}\"",
          f"    runtime.error(\"Open this script on a {tf} chart - it was exported for {tf}.\")", ""]
    S += engine_arrays(signals) + [""]
    S += ["// ---------- engine entries on this chart (markers + match table) ----------",
          "// index of the engine entry with t0 <= time < t1, or -1",
          "f_eng_idx(t0, t1) =>",
          "    int n = array.size(eT)",
          "    int res = -1",
          "    if n > 0",
          "        int i = array.binary_search_leftmost(eT, t0)   // the value, or the next smaller one (-1 = none)",
          "        if i < 0 or array.get(eT, i) < t0",
          "            i += 1",
          "        if i < n and array.get(eT, i) >= t0 and array.get(eT, i) < t1",
          "            res := i",
          "    res",
          "int engI = f_eng_idx(time, time_close)",
          "bool engL = engI >= 0 and array.get(eD, engI) == 1",
          "bool engS = engI >= 0 and array.get(eD, engI) == -1",
          "plotshape(engL, \"Engine long entry\", shape.triangleup, location.belowbar, color.new(color.green, 0), "
          "size = size.small)",
          "plotshape(engS, \"Engine short entry\", shape.triangledown, location.abovebar, color.new(color.red, 0), "
          "size = size.small)", ""]
    S += ["// ---------- trade plan ----------",
          f"float SLIP_L = {slip[1]}", f"float SLIP_S = {slip[-1]}",
          f"array<float> TP_R = array.from({', '.join(_fl(x) for x in tps_r)})",
          f"array<float> SPLIT = array.from({', '.join(_fl(x) for x in split)})",
          f"int HOLD = {int(spec['time_stop_bars'])}", f"int COOLDOWN = {int(spec.get('cooldown_bars') or 0)}",
          "var float curStop = na", "var float tp1 = na", "var float tp2 = na", "var float tp3 = na",
          "var float qty0 = na", "var float entryPx = na", "var int entryBar = na", "var int dirNow = 0",
          "bool placedNow = false", ""]
    if mode == "RULES":
        S += ["// ---------- the card's rules (every function call is its own line so it runs on every candle) ----------"]
        S += em.lines + [f"bool longSig = {long_s}", f"bool shortSig = {short_s}", f"bool exitL = {exl}",
                         f"bool exitS = {exs}", ""]
        if st["method"] == "atr":
            S += [f"f_R(d, e) => {float(st['atr'])} * {atr_v}"]
        else:
            b, w = float(st.get("buffer_atr", 0.2)), float(st.get("max_width_atr", 3.0))
            S += [f"f_R(d, e) => d == 1 ? e - ({lv_l} - {b} * {atr_v}) : ({lv_s} + {b} * {atr_v}) - e",
                  f"float MAXW = {w}"]
        S += ["int lastExit = strategy.closedtrades > 0 ? strategy.closedtrades.exit_bar_index(strategy.closedtrades - 1) "
              ": -1000000",
              "bool flat = strategy.position_size == 0 and strategy.opentrades == 0",
              "int want = flat and bar_index >= lastExit + COOLDOWN ? (longSig ? 1 : shortSig ? -1 : 0) : 0",
              "if want != 0",
              "    float e = close * (1 + (want == 1 ? SLIP_L : SLIP_S) * want)   // next open ~ this close (24/7 market)",
              "    float r = f_R(want, e)",
              "    bool ok = not na(r) and r > 0" + ("" if st["method"] == "atr" else " and r <= MAXW * " + atr_v),
              "    if ok",
              "        entryPx := e",
              "        dirNow := want",
              "        curStop := e - want * r",
              "        tp1 := e + want * array.get(TP_R, 0) * r",
              "        tp2 := array.get(SPLIT, 1) > 0 ? e + want * array.get(TP_R, 1) * r : na",
              "        tp3 := array.get(SPLIT, 2) > 0 ? e + want * array.get(TP_R, 2) * r : na",
              "        qty0 := strategy.equity * 0.01 / r   // 1% risk per trade: the tester's profit reads in R",
              "        strategy.entry(want == 1 ? \"L\" : \"S\", want == 1 ? strategy.long : strategy.short, qty = qty0)",
              "        placedNow := true"]
    else:
        tfms = {"5m": 300000, "15m": 900000, "30m": 1800000, "1h": 3600000, "4h": 14400000, "1d": 86400000}[tf]
        S += [f"int TF_MS = {tfms}",
              "// REPLAY: an engine entry inside the NEXT candle -> place the order now (it fills at the next open)",
              "int nxt = f_eng_idx(time_close, time_close + TF_MS)",
              "bool flat = strategy.position_size == 0 and strategy.opentrades == 0",
              "if flat and nxt >= 0",
              "    int want = array.get(eD, nxt)",
              "    float s = array.get(eS, nxt)",
              "    float e = close",
              "    float r = math.abs(e - s)",
              "    if not na(s) and r > 0",
              "        entryPx := e",
              "        dirNow := want",
              "        curStop := s",
              "        tp1 := array.get(eP1, nxt)",
              "        tp2 := array.get(eP2, nxt)",
              "        tp3 := array.get(eP3, nxt)",
              "        qty0 := strategy.equity * 0.01 / r",
              "        strategy.entry(want == 1 ? \"L\" : \"S\", want == 1 ? strategy.long : strategy.short, qty = qty0)",
              "        placedNow := true",
              "bool exitL = false", "bool exitS = false"]
    S += ["",
          "// ---------- manage the open trade like the engine: TP split, stop to breakeven after TP1, to TP1 after TP2 ----------",
          "if strategy.opentrades > 0 and na(entryBar)",
          "    entryBar := strategy.opentrades.entry_bar_index(0)",
          "if strategy.opentrades == 0 and strategy.position_size == 0 and not na(entryBar)",
          "    entryBar := na",
          "float left = math.abs(strategy.position_size)",
          "if strategy.opentrades > 0 and not na(qty0)",
          "    float done = qty0 - left",
          "    if done >= array.get(SPLIT, 0) * qty0 * 0.999 and not na(tp1)",
          "        curStop := dirNow == 1 ? math.max(curStop, strategy.position_avg_price) : math.min(curStop, strategy.position_avg_price)",
          "    if done >= (array.get(SPLIT, 0) + array.get(SPLIT, 1)) * qty0 * 0.999 and not na(tp2)",
          "        curStop := tp1",
          "string eid = dirNow == 1 ? \"L\" : \"S\"",
          "if not na(qty0) and dirNow != 0",
          "    float q1 = array.get(SPLIT, 0) * qty0",
          "    float q2 = array.get(SPLIT, 1) * qty0",
          "    if na(tp2)",
          "        strategy.exit(\"TP1\", eid, limit = tp1, stop = curStop, comment_profit = \"TP1\", comment_loss = \"SL\")",
          "    else",
          "        strategy.exit(\"TP1\", eid, qty = q1, limit = tp1, stop = curStop, comment_profit = \"TP1\", comment_loss = \"SL\")",
          "        if na(tp3)",
          "            strategy.exit(\"TP2\", eid, limit = tp2, stop = curStop, comment_profit = \"TP2\", comment_loss = \"SL\")",
          "        else",
          "            strategy.exit(\"TP2\", eid, qty = q2, limit = tp2, stop = curStop, comment_profit = \"TP2\", comment_loss = \"SL\")",
          "            strategy.exit(\"TP3\", eid, limit = tp3, stop = curStop, comment_profit = \"TP3\", comment_loss = \"SL\")",
          "// early exit rule / time stop at the candle close (like the engine)",
          "if strategy.opentrades > 0 and not na(entryBar)",
          "    bool ruleOut = (dirNow == 1 and exitL) or (dirNow == -1 and exitS)",
          "    if ruleOut or bar_index - entryBar + 1 >= HOLD",
          "        strategy.close_all(comment = ruleOut ? \"EXIT_RULE\" : \"TIME\", immediately = true)",
          "if strategy.opentrades == 0 and strategy.position_size == 0 and not placedNow",
          "    qty0 := na",
          "    dirNow := 0",
          "plot(strategy.opentrades > 0 ? curStop : na, \"Stop\", color.new(color.red, 0), style = plot.style_linebr)",
          "plot(strategy.opentrades > 0 ? tp1 : na, \"TP1\", color.new(color.teal, 0), style = plot.style_linebr)", "",
          "// ---------- match table: engine entries vs this script's entries ----------",
          "bool pineIn = strategy.opentrades > 0 and strategy.opentrades.entry_bar_index(strategy.opentrades - 1) == bar_index",
          "var int nBoth = 0", "var int nEng = 0", "var int nPine = 0",
          "bool inWindow = array.size(eT) > 0 and time >= array.get(eT, 0)",
          "if inWindow",
          "    if engI >= 0 and pineIn",
          "        nBoth += 1",
          "    else if engI >= 0",
          "        nEng += 1",
          "    else if pineIn",
          "        nPine += 1",
          "var table tb = table.new(position.top_right, 2, 5, bgcolor = color.new(color.black, 80))",
          "if barstate.islast",
          f"    table.cell(tb, 0, 0, \"{mode} mode\", text_color = color.white)",
          "    table.cell(tb, 1, 0, array.size(eT) > 0 ? str.tostring(array.size(eT)) + \" engine entries\" : "
          "\"no engine entries for \" + syminfo.basecurrency, text_color = color.white)",
          "    table.cell(tb, 0, 1, \"matched\", text_color = color.white)",
          "    table.cell(tb, 1, 1, str.tostring(nBoth), text_color = color.white)",
          "    table.cell(tb, 0, 2, \"only engine\", text_color = color.white)",
          "    table.cell(tb, 1, 2, str.tostring(nEng), text_color = color.white)",
          "    table.cell(tb, 0, 3, \"only Pine\", text_color = color.white)",
          "    table.cell(tb, 1, 3, str.tostring(nPine), text_color = color.white)",
          "    table.cell(tb, 0, 4, \"why\", text_color = color.white)",
          "    table.cell(tb, 1, 4, " + ("\"only Pine = engine regime gate / risk / data checks\"" if mode == "RULES"
                                        else "\"rules not recomputed (replay)\"") + ", text_color = color.white)"]
    text = "\n".join(S) + "\n"
    return text, dict(mode=mode, unsupported=bad, signals=n_sig, coins=sorted(signals))


def signals_from_trades(per_coin, keep=300):
    """The engine's backtest trades {coin: [trade]} -> the entries embedded in the script (newest `keep` per coin):
    entry candle open time, direction, stop and target prices."""
    out = {}
    for coin, trades in per_coin.items():
        rows = [dict(entry_ms=int(t["entry_time"]), dir=int(t["dir"]), stop=float(t["entry"] - t["dir"] * t["R"]),
                     tps=[float(x) for x in t.get("tps") or [t["tp1"]]]) for t in trades]
        if rows:
            out[coin] = sorted(rows, key=lambda x: x["entry_ms"])[-keep:]
    return out


def filename(sid, version, tf):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{sid}_v{version}_{tf}") + ".pine"


def structure_problems(text):
    """Cheap checks the tests (and the exporter) run on every script: balanced brackets / quotes, header, no
    Python leftovers. TradingView's compiler is the real check - see the README."""
    probs = []
    code = "\n".join(ln.split("//")[0] if not ln.lstrip().startswith("//") else "" for ln in text.splitlines())
    for a, b in ("()", "[]"):
        if code.count(a) != code.count(b):
            probs.append(f"unbalanced {a}{b}: {code.count(a)} vs {code.count(b)}")
    if code.count('"') % 2:
        probs.append("odd number of quotes")
    if "//@version=6" not in text:
        probs.append("missing //@version=6")
    for bad in (" & ", " | ", "~", "True", "False", "None", "np.", "&&", "||"):
        if bad in code:
            probs.append(f"python leftover {bad.strip()!r}")
    for ln in code.splitlines():
        if ln.strip() and (len(ln) - len(ln.lstrip())) % 4:
            probs.append(f"indent not a multiple of 4: {ln[:60]!r}")
            break
    return probs


# ---------------------------------------------------------------------------------------------------------------
# 4. the same tree with Pine semantics in Python (for the tests: engine vs translation, bar by bar)
# ---------------------------------------------------------------------------------------------------------------
def _ema_like(x, a, n):
    out, e, cnt = np.full(len(x), np.nan), np.nan, 0
    for i, v in enumerate(x):
        if not np.isnan(v):
            e = v if np.isnan(e) else a * v + (1 - a) * e
            cnt += 1
        out[i] = e if cnt >= n else np.nan
    return out


def _tr(h, l, c):
    pc = np.r_[np.nan, c[:-1]]
    return np.where(np.isnan(pc), h - l, np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0))


def _hist(x, n):
    return np.r_[np.full(n, np.nan if x.dtype.kind == "f" else False), x[:-n]] if n else x


def _roll(x, n, fn):
    return getattr(pd.Series(x).rolling(n, min_periods=n), fn)().to_numpy()


def _barssince(b):
    out, last = np.full(len(b), np.nan), -1
    for i, v in enumerate(b):
        if v:
            last = i
        out[i] = i - last if last >= 0 else np.nan
    return out


def _st_dir(h, l, c, n, mult):
    a = _ema_like(_tr(h, l, c), 1.0 / n, n)
    mid = (h + l) / 2
    ub, lb = mid + mult * a, mid - mult * a
    fu = fl = d = np.nan
    out = np.full(len(c), np.nan)
    for i in range(len(c)):
        pfu, pfl, pd_ = fu, fl, d
        if np.isnan(a[i]):
            fu, fl, d = ub[i], lb[i], np.nan
        else:
            if not np.isnan(pfu):
                fu = ub[i] if (ub[i] < pfu or c[i - 1] > pfu) else pfu
                fl = lb[i] if (lb[i] > pfl or c[i - 1] < pfl) else pfl
            else:
                fu, fl = ub[i], lb[i]
            prevd = 1.0 if np.isnan(pd_) else pd_
            d = (-1.0 if c[i] < fl else 1.0) if prevd == 1 else (1.0 if c[i] > fu else -1.0)
        out[i] = d
    return out


def pine_sim(text_or_tree, df, htf=None):
    """Evaluate a rule with Pine semantics (the functions in LIB). df: open..volume (+ htf_up / htf_down columns
    computed by htf_sim for rules that use them). Returns a numpy array (bool for conditions)."""
    t = parse(text_or_tree) if isinstance(text_or_tree, str) else text_or_tree
    o, h, l, c, v = (df[k].to_numpy(dtype=float) for k in SOURCES)
    src = dict(open=o, high=h, low=l, close=c, volume=v)

    def ev(t):
        k = t[0]
        if k == "num":
            return np.full(len(c), float(t[1]))
        if k == "src":
            return src[t[1]]
        if k == "htf":
            return df[f"htf_{t[1]}"].to_numpy(dtype=bool)
        if k == "hist":
            return _hist(ev(t[1]), t[2])
        if k == "bin":
            a, b = ev(t[2]), ev(t[3])
            with np.errstate(all="ignore"):
                return {"+": a + b, "-": a - b, "*": a * b, "/": a / b}[t[1]]
        if k == "neg":
            return -ev(t[1])
        if k == "cmp":
            a, b = ev(t[2]), ev(t[3])
            with np.errstate(invalid="ignore"):
                r = {">": a > b, ">=": a >= b, "<": a < b, "<=": a <= b, "==": a == b, "!=": a != b}[t[1]]
            return r & ~(np.isnan(a.astype(float)) | np.isnan(b.astype(float))) if t[1] != "!=" else r
        if k == "and":
            return ev(t[1]).astype(bool) & ev(t[2]).astype(bool)
        if k == "or":
            return ev(t[1]).astype(bool) | ev(t[2]).astype(bool)
        if k == "not":
            return ~ev(t[1]).astype(bool)
        if k == "math":
            args = [ev(a) for a in t[2]]
            return np.abs(args[0]) if t[1] == "abs" else (np.fmin if t[1] == "min" else np.fmax)(*args)
        name, ser, p = t[1], [ev(s) for s in t[2]], t[3]
        if name == "ema":
            return _ema_like(ser[0], 2.0 / (p[0] + 1), p[0])
        if name == "sma":
            return _roll(ser[0], p[0], "mean")
        if name == "rsi":
            x = ser[0]
            d = np.r_[np.nan, np.diff(x)]
            up = _ema_like(np.where(np.isnan(d), np.nan, np.maximum(d, 0)), 1.0 / p[0], p[0])
            dn = _ema_like(np.where(np.isnan(d), np.nan, np.maximum(-d, 0)), 1.0 / p[0], p[0])
            with np.errstate(all="ignore"):
                r = np.where(dn == 0, 100.0, 100.0 - 100.0 / (1.0 + up / dn))
            return np.where(np.isnan(up) | np.isnan(dn), np.nan, r)
        if name == "atr":
            return _ema_like(_tr(h, l, c), 1.0 / p[0], p[0])
        if name == "adx":
            n = p[0]
            up, dn = np.r_[np.nan, np.diff(h)], np.r_[np.nan, -np.diff(l)]
            ok = ~np.isnan(up) & ~np.isnan(dn)
            pdm = np.where(ok & (up > dn) & (up > 0), up, 0.0)
            mdm = np.where(ok & (dn > up) & (dn > 0), dn, 0.0)
            a = _ema_like(_tr(h, l, c), 1.0 / n, n)
            with np.errstate(all="ignore"):
                pdi, mdi = 100 * _ema_like(pdm, 1.0 / n, n) / a, 100 * _ema_like(mdm, 1.0 / n, n) / a
                dx = np.where(np.isnan(pdi) | np.isnan(mdi) | (pdi + mdi == 0), np.nan,
                              100 * np.abs(pdi - mdi) / (pdi + mdi))
            return _ema_like(dx, 1.0 / n, n)
        if name in ("macd_line", "macd_signal", "macd_hist"):
            line = _ema_like(ser[0], 2.0 / (p[0] + 1), p[0]) - _ema_like(ser[0], 2.0 / (p[1] + 1), p[1])
            if name == "macd_line":
                return line
            sig = _ema_like(line, 2.0 / (p[2] + 1), p[2])
            return sig if name == "macd_signal" else line - sig
        if name.startswith("bb_"):
            mid = _roll(ser[0], p[0], "mean")
            if name == "bb_mid":
                return mid
            sd = pd.Series(ser[0]).rolling(p[0], min_periods=p[0]).std(ddof=0).to_numpy()
            up, lo = mid + p[1] * sd, mid - p[1] * sd
            return {"bb_upper": up, "bb_lower": lo}.get(name, (up - lo) / mid if name == "bb_width" else None)
        if name == "highest":
            return _roll(ser[0], p[0], "max")
        if name == "lowest":
            return _roll(ser[0], p[0], "min")
        if name == "vol_sma":
            return _roll(v, p[0], "mean")
        if name == "pct_rank":
            x, n = ser[0], p[0]
            out = np.full(len(x), np.nan)
            for i in range(n - 1, len(x)):
                w = x[i - n + 1:i + 1]
                if not np.isnan(w).any():
                    out[i] = (w[:-1] < w[-1]).sum() / (n - 1)
            return out
        if name == "supertrend_dir":
            return _st_dir(h, l, c, p[0], p[1])
        if name == "bars_since":
            return _barssince(ser[0].astype(bool))
        if name == "within":
            bs = _barssince(ser[0].astype(bool))
            return ~np.isnan(bs) & (np.nan_to_num(bs, nan=1e18) < p[0])
        if name in ("cross_up", "cross_down"):
            a, b = ser
            a1, b1 = _hist(a, 1), _hist(b, 1)
            with np.errstate(invalid="ignore"):
                r = (a > b) & (a1 <= b1) if name == "cross_up" else (a < b) & (a1 >= b1)
            return r & ~np.isnan(a) & ~np.isnan(b) & ~np.isnan(a1) & ~np.isnan(b1)
        raise ValueError(name)
    return ev(t)


def htf_sim(df, htf_df):
    """The Pine higher-timeframe selection (f_htf + htfNow) in Python: per lower candle, the newest higher candle
    whose close time is <= the lower candle's close time; ema 20 / 50 with the engine's formula."""
    hc = htf_df["close"].to_numpy(dtype=float)
    e20, e50 = _ema_like(hc, 2 / 21, 20), _ema_like(hc, 2 / 51, 50)
    idx = np.searchsorted(htf_df["close_time"].to_numpy(), df["close_time"].to_numpy(), side="right") - 1
    ok = idx >= 0
    j = np.where(ok, idx, 0)
    c_, a_, b_ = np.where(ok, hc[j], np.nan), np.where(ok, e20[j], np.nan), np.where(ok, e50[j], np.nan)
    good = ~np.isnan(a_) & ~np.isnan(b_)
    with np.errstate(invalid="ignore"):
        return good & (c_ > b_) & (a_ > b_), good & (c_ < b_) & (a_ < b_)
