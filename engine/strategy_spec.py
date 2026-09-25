"""
Strategy specification v3 (AGENT_PROMPT.md section 10).

Every strategy in strategies.yaml is an "ID card": id, version, status, family, hypothesis, source,
allowed regimes, timeframes, long/short rules, stop, targets, time stop, cooldown, control twin,
known weaknesses and a changelog. This module reads and checks the cards, fingerprints the parts
that decide trades (a tested version may never change - section 10), and turns stop / target
settings into prices.

Phase 17: strategies_lab.yaml holds the cards Claude's daily review and weekly research add (append-only, checked
by the Brain guard). The engine tests them exactly like strategies.yaml, but a lab card can never be APPROVED:
the operator moves it into strategies.yaml by pull request first. Lab rules are run by the engine, so they may
only use the building blocks below (lab_card_problems / expr_problems) - nothing else a Python expression could do.

Pure functions only: no internet, no files.
"""
import ast
import hashlib
import json
import math
import re

AUTHOR_STATUSES = ["IDEA", "FORMALIZED", "RETIRED"]     # what the author writes in strategies.yaml
FAMILIES = {                                              # section 10 experiment batch A-H
    "trend_following": "A", "momentum": "B", "breakout": "C", "mean_reversion": "D",
    "price_action": "E", "mtf_pullback": "F", "liquidity_reversal": "G", "smc": "H",
}
GATES = {
    "trend": "needs 2 of 1D/4H/1H in its direction; no trade against a STRONG weekly trend",
    "reversal": "needs 2 of 1D/4H/1H in its direction; declared reversal type, so no weekly veto",
    "mean_reversion": "trades only in its (range) regimes; never against a STRONG 1W/1D/4H trend",
}
REQUIRED = ["id", "version", "status", "family", "gate", "hypothesis", "source", "regimes", "timeframes",
            "long", "short", "stop", "time_stop_bars", "known_weaknesses"]
# the parts that decide trades: changing any of them needs a new version number
LOGIC_KEYS = ["family", "gate", "regimes", "timeframes", "long", "short", "exit_long", "exit_short", "stop",
              "targets", "time_stop_bars", "cooldown_bars", "confirm_5m"]
VERSION_RE = re.compile(r"^\d+\.\d+$")
R_RE = re.compile(r"^(\d+(?:\.\d+)?)R$")
MAX_RE = re.compile(r"^max\((.+),(.+)\)$")
NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
PARAM_RE = re.compile(r"\{(\w+)\}")
TEMPLATE_KEYS = ["long", "short", "exit_long", "exit_short", "stop", "targets"]
CONFIRM_TFS = ["30m", "15m"]           # the 5-minute protocol (section 8) runs after a closed 15m / 30m trigger

# ---------- the strategy lab (Phase 17) ----------
LIBRARY_FILE, LAB_FILE = "strategies.yaml", "strategies_lab.yaml"
EVIDENCE_CLASSES = ["FACT", "RESEARCH_FINDING", "BACKTEST_EVIDENCE", "CLAIM", "HYPOTHESIS", "MODEL_OUTPUT",
                    "UNVERIFIED_OPINION"]           # = engine/memory.py (section 22)
MIN_TP1_R = 2.0                                     # a lab card's first target is at least 2R away
# the edge block (Phase 17 B): WHY a strategy should make money, in four plain lines. Required on lab cards (not on
# control twins, which are benchmarks). The engine adds the measured evidence next to it; it never proves the edge.
EDGE_KEYS = {"who_pays": "who is on the other side of the trade, and why they lose",
             "mechanism": "what market behaviour makes the move happen",
             "fails_when": "the regimes / conditions where it should NOT work",
             "kill_rule": "the result that would show the edge is gone"}
EDGE_MIN_CHARS = 20
EDGE_TYPES = {"behavioural": "a bias of other traders (fear, chasing, anchoring, over-reaction)",
              "forced_flow": "trades others MUST make (liquidations, funding, stop-losses, rebalancing, expiries)",
              "risk_premium": "being paid for carrying a risk others avoid",
              "structural": "how the market is built (sessions, listings, fees, exchange rules)"}
# the building blocks a rule may use (the rule namespace of scanner.make_namespace + the feature / SMC columns;
# tests/test_lab.py checks these lists against the engine's real namespace)
FUNCTIONS = {"ema", "sma", "rsi", "atr", "adx", "macd_line", "macd_signal", "macd_hist", "bb_mid", "bb_upper",
             "bb_lower", "bb_width", "highest", "lowest", "shift", "prev", "vol_sma", "pct_rank", "supertrend_dir",
             "cross_up", "cross_down", "within", "bars_since", "abs", "min", "max"}
COLUMNS = {"open", "high", "low", "close", "volume", "htf_up", "htf_down",
           # engine/features.py
           "atr_ratio", "bear_div", "bear_engulf", "bear_reject", "body_pct", "breakout_down", "breakout_up",
           "bull_div", "bull_engulf", "bull_reject", "close_loc", "consec_down", "consec_up", "consolidation",
           "contraction", "displacement_down", "displacement_up", "expansion", "failed_breakout_down",
           "failed_breakout_up", "impulse_down", "impulse_up", "keltner_lower", "keltner_mid", "keltner_upper",
           "last_swing_high", "last_swing_low", "lower_wick_pct", "momentum_persist", "obv", "pullback_down",
           "pullback_up", "range_atr", "rel_vol", "resistance", "resistance_dist_atr", "resistance_touches",
           "retest_down", "retest_up", "roc", "stoch_rsi_d", "stoch_rsi_k", "structure", "structure_down",
           "structure_up", "support", "support_dist_atr", "support_touches", "swing_high", "swing_high_label",
           "swing_high_price", "swing_low", "swing_low_label", "swing_low_price", "upper_wick_pct", "vol_accel",
           "vwap",
           # engine/smc.py (this timeframe)
           "smc_bear_ob_high", "smc_bear_ob_low", "smc_bos_down", "smc_bos_up", "smc_bull_ob_high",
           "smc_bull_ob_low", "smc_choch_down", "smc_choch_up", "smc_fvg_retrace_bear", "smc_fvg_retrace_bull",
           "smc_in_bear_ob", "smc_in_bull_ob", "smc_in_killzone", "smc_kz_asia", "smc_kz_london", "smc_kz_ny_am",
           "smc_kz_silver_bullet", "smc_liq_above", "smc_liq_below", "smc_pd_mid", "smc_pdh", "smc_pdl",
           "smc_range_high", "smc_range_low", "smc_range_pos", "smc_sweep_bear", "smc_sweep_bear_high",
           "smc_sweep_bull", "smc_sweep_bull_low", "smc_sweep_pdh", "smc_sweep_pdl"}
H4_COLUMNS = {"h4_bear_ob_high", "h4_bear_ob_low", "h4_bull_ob_high", "h4_bull_ob_low", "h4_liq_above",
              "h4_liq_below", "h4_range_high", "h4_range_low", "h4_range_pos"}     # only below 4H
H4_TFS = ["1h", "30m", "15m", "5m"]
SPECIAL_PREFIXES = ("smc_", "h4_")         # the SMC / ICT ingredient: a card using it needs a control twin
_OPS = (ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Compare, ast.Call, ast.Name, ast.Load,
        ast.Constant, ast.keyword, ast.And, ast.Or, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.FloorDiv,
        ast.BitAnd, ast.BitOr, ast.BitXor, ast.Not, ast.Invert, ast.USub, ast.UAdd, ast.Eq, ast.NotEq, ast.Lt,
        ast.LtE, ast.Gt, ast.GtE)


def _fmt(v):
    return str(int(v)) if isinstance(v, int) and not isinstance(v, bool) else repr(float(v))


def _fill(x, p):
    if isinstance(x, str):
        return PARAM_RE.sub(lambda m: _fmt(p[m.group(1)]), x)
    if isinstance(x, list):
        return [_fill(v, p) for v in x]
    if isinstance(x, dict):
        return {k: _fill(v, p) for k, v in x.items()}
    return x


def placeholders(spec):
    """Names used as {name} in the rules, stop and targets."""
    found = set()

    def walk(x):
        if isinstance(x, str):
            found.update(PARAM_RE.findall(x))
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
    for k in TEMPLATE_KEYS:
        walk(spec.get(k))
    return found


def render(spec, params=None, stop=None, time_stop_bars=None):
    """The card with every {name} replaced by its value (params overrides the card's own params).
    The engine always runs rendered cards; the fingerprint is taken from the rendered rules."""
    p = dict(spec.get("params") or {})
    p.update(params or {})
    out = dict(spec)
    for k in TEMPLATE_KEYS:
        if k in out and out[k] is not None:
            out[k] = _fill(out[k], p)
    if stop:
        out["stop"] = dict(out["stop"], **stop)
    if time_stop_bars:
        out["time_stop_bars"] = int(time_stop_bars)
    out["params"] = p
    return out


def nudge(v, factor):
    """v moved by factor (e.g. 0.8 / 1.2). Whole numbers stay whole and always move by at least 1."""
    if isinstance(v, int) and not isinstance(v, bool):
        new = int(round(v * factor))
        if new == v:
            new = v + (1 if factor > 1 else -1)
        return max(1, new)
    return round(float(v) * factor, 6)


def variants(spec, pct):
    """The +-pct% robustness test (AGENT_PROMPT.md section 11): every parameter moved down and up,
    ONE AT A TIME - the card's params plus the stop size and the time stop.
    spec: a loaded card (with '_raw'). Returns [(label, rendered card, entry rules changed?)]."""
    raw = spec.get("_raw", spec)
    out = []
    for f in (1 - pct / 100, 1 + pct / 100):
        for name, v in (raw.get("params") or {}).items():
            nv = nudge(v, f)
            out.append((f"{name} {_fmt(v)}→{_fmt(nv)}", _finish(render(raw, {name: nv}), raw), True))
        st = raw["stop"]
        for k in (("atr",) if st["method"] == "atr" else ("buffer_atr", "max_width_atr")):
            v = st.get(k, 0.2 if k == "buffer_atr" else 3.0)
            nv = nudge(float(v), f)
            out.append((f"stop {k} {_fmt(float(v))}→{_fmt(nv)}", _finish(render(raw, stop={k: nv}), raw), False))
        tb = int(raw["time_stop_bars"])
        nv = nudge(tb, f)
        out.append((f"time_stop_bars {tb}→{nv}", _finish(render(raw, time_stop_bars=nv), raw), False))
    return out


def _finish(card, raw):
    card = dict(card, version=str(raw["version"]), cooldown_bars=int(raw.get("cooldown_bars", 0) or 0))
    card["_raw"] = raw
    return card


def key(spec):
    return f"{spec['id']}@{spec['version']}"


def fingerprint(spec):
    """Short hash of the trade-deciding parts of a card."""
    core = {k: spec.get(k) for k in LOGIC_KEYS}      # call it on RENDERED cards (see render)
    return hashlib.sha256(json.dumps(core, sort_keys=True, default=str).encode()).hexdigest()[:16]


def parse_target(item):
    """'2R' -> ('r', 2.0) · 'smc_liq_above' -> ('col', name) · 'max(3R, col)' -> ('max', [a, b]).
    Raises ValueError for anything else."""
    x = str(item).replace(" ", "")
    m = R_RE.match(x)
    if m:
        return ("r", float(m.group(1)))
    m = MAX_RE.match(x)
    if m:
        return ("max", [parse_target(m.group(1)), parse_target(m.group(2))])
    if NAME_RE.match(x):
        return ("col", x)
    raise ValueError(f"target '{item}' not understood (use e.g. 2R, a column name, or max(3R, column))")


def columns_needed(spec):
    """Column names the stop / target settings read (checked against the data at run time)."""
    out = set()
    st = spec.get("stop") or {}
    if st.get("method") == "structure":
        out |= {st.get("long_level"), st.get("short_level")}
    tg = spec.get("targets") or {}

    def walk(p):
        if p[0] == "col":
            out.add(p[1])
        elif p[0] == "max":
            for q in p[1]:
                walk(q)
    for side in ("long", "short"):
        for item in tg.get(side) or []:
            walk(parse_target(item))
    need = tg.get("need") or {}
    out |= {need.get("long"), need.get("short")}
    return {c for c in out if c}


def check(spec, labels, timeframes):
    """List of problems with one card (empty = fine). spec = the card as written (with {params})."""
    errs = [f"missing '{k}'" for k in REQUIRED if spec.get(k) in (None, "", [])]
    if errs:
        return errs
    if not VERSION_RE.match(str(spec["version"])):
        errs.append(f"version '{spec['version']}' must look like \"1.0\" (in quotes)")
    if spec["status"] not in AUTHOR_STATUSES:
        errs.append(f"status '{spec['status']}' must be one of {', '.join(AUTHOR_STATUSES)} "
                    "(the engine sets BACKTESTING / VALIDATION / ... itself)")
    if spec["family"] not in FAMILIES:
        errs.append(f"family '{spec['family']}' unknown ({', '.join(FAMILIES)})")
    if spec["gate"] not in GATES:
        errs.append(f"gate '{spec['gate']}' unknown ({', '.join(GATES)})")
    bad = [r for r in spec["regimes"] if r not in labels]
    if bad:
        errs.append(f"unknown regimes {bad}")
    bad = [t for t in spec["timeframes"] if t not in timeframes]
    if bad:
        errs.append(f"unknown timeframes {bad}")
    st = spec["stop"]
    if not isinstance(st, dict) or st.get("method") not in ("atr", "structure"):
        errs.append("stop.method must be 'atr' or 'structure'")
    elif st["method"] == "atr" and not (isinstance(st.get("atr"), (int, float)) and st["atr"] > 0):
        errs.append("stop.atr must be a positive number")
    elif st["method"] == "structure" and not (st.get("long_level") and st.get("short_level")):
        errs.append("a structure stop needs long_level and short_level")
    tg = spec.get("targets")
    if tg is not None:
        try:
            lg, sh = tg.get("long") or [], tg.get("short") or []
            for item in lg + sh:
                parse_target(item)
            split = tg.get("split") or []
            if not lg or len(lg) != len(sh) or len(split) != len(lg):
                errs.append("targets need the same number of long, short and split entries")
            elif abs(sum(split) - 1) > 1e-9 or min(split) <= 0:
                errs.append("targets.split must be positive and add up to 1")
        except ValueError as e:
            errs.append(str(e))
    if not (isinstance(spec["time_stop_bars"], int) and spec["time_stop_bars"] > 0):
        errs.append("time_stop_bars must be a positive whole number")
    c5 = spec.get("confirm_5m", False)
    if not isinstance(c5, bool):
        errs.append("confirm_5m must be true or false")
    elif c5:
        if not set(spec["timeframes"]) <= set(CONFIRM_TFS):
            errs.append(f"confirm_5m: the 5-minute protocol follows a 15m or 30m trigger - timeframes must be "
                        f"within {CONFIRM_TFS}")
        if not spec.get("control_twin"):
            errs.append("confirm_5m: needs control_twin = the same strategy without the 5m check (section 8)")
    params = spec.get("params") or {}
    if not isinstance(params, dict):
        errs.append("params must be a list of name: number")
        return errs
    bad = [k for k, v in params.items() if isinstance(v, bool) or not isinstance(v, (int, float)) or v <= 0]
    if bad:
        errs.append(f"params {bad} must be positive numbers")
    used = placeholders(spec)
    if used - set(params):
        errs.append(f"rules use {sorted(used - set(params))} but params does not define them")
    if set(params) - used:
        errs.append(f"params {sorted(set(params) - used)} are not used in any rule")
    return errs


def load(items, labels, timeframes):
    """Check every card. Returns (runnable cards, problems {id or #n: [..]}, idle cards (IDEA / RETIRED))."""
    ok, problems, idle, seen = [], {}, [], set()
    for i, s in enumerate(items or []):
        name = s.get("id") or f"#{i + 1}"
        errs = check(s, labels, timeframes)
        if not errs and key(s) in seen:
            errs = [f"{key(s)} appears twice"]
        if errs:
            problems[name] = errs
            continue
        raw = dict(s, version=str(s["version"]))
        s = _finish(render(raw), raw)
        seen.add(key(s))
        (ok if s["status"] == "FORMALIZED" else idle).append(s)
    ids = {s["id"] for s in ok + idle}
    for s in list(ok):
        bad = [f"{ref} '{s[ref]}' is not in strategies.yaml or strategies_lab.yaml" for ref in ("control_twin", "twin_of")
               if s.get(ref) and s[ref] not in ids]
        if not bad and s.get("confirm_5m"):
            bad = confirm_twin_problems(s, next((x for x in ok if x["id"] == s["control_twin"]), None))
        if bad:
            problems.setdefault(s["id"], []).extend(bad)
            ok.remove(s)
    return ok, problems, idle


def confirm_twin_problems(s, twin):
    """A 5m-confirmed card must be its control twin + the 5m check, nothing else: same rules, stop, targets,
    exits, hold time, gates (compared after the parameters are filled in), on timeframes the twin also runs."""
    if twin is None:
        return [f"control_twin '{s['control_twin']}' is not a runnable (FORMALIZED) card"]
    if twin.get("confirm_5m"):
        return ["the control twin of a 5m-confirmed card must not use the 5m check itself"]
    diff = [k for k in LOGIC_KEYS if k not in ("confirm_5m", "timeframes") and s.get(k) != twin.get(k)]
    if diff:
        return [f"differs from its control twin in {diff} - only the 5m check may differ"]
    if not set(s["timeframes"]) <= set(twin["timeframes"]):
        return ["runs on timeframes its control twin does not run on"]
    return []


def _level(p, d, entry, R, t, cols):
    if p[0] == "r":
        return entry + d * p[1] * R
    if p[0] == "col":
        return float(cols[p[1]][t])
    a, b = (_level(q, d, entry, R, t, cols) for q in p[1])     # 'max' = whichever is FARTHER away
    if not (math.isfinite(a) and math.isfinite(b)):
        return a if math.isfinite(a) else b
    return max(a, b) if d == 1 else min(a, b)


def targets(spec, d, entry, R, t, cols, trade_plan):
    """Take-profit prices and the share closed at each, for a trade planned at candle t.
    Default: the config trade plan (1R / 2R / 3R). Returns (prices, split) or None = no valid trade
    (a needed level is missing, too close (< need.min_r), or a target is not beyond the one before)."""
    tg = spec.get("targets")
    if not tg:
        return [entry + d * r * R for r in trade_plan["tp_r"]], list(trade_plan["tp_split"])
    need = tg.get("need")
    if need:
        lev = float(cols[need["long" if d == 1 else "short"]][t])
        if not math.isfinite(lev) or d * (lev - entry) < float(need.get("min_r", 0)) * R:
            return None
    prices, last = [], entry
    for item in tg["long" if d == 1 else "short"]:
        px = _level(parse_target(item), d, entry, R, t, cols)
        if not math.isfinite(px) or d * (px - last) <= 0:
            return None
        prices.append(px)
        last = px
    return prices, list(tg["split"])


# ---------- the strategy lab (Phase 17) ----------
def _names(expr):
    try:
        return {n.id for n in ast.walk(ast.parse(str(expr), mode="eval")) if isinstance(n, ast.Name)}
    except SyntaxError:
        return set()


def expr_problems(expr, tfs):
    """A rule or level of a LAB card: only the building blocks - known column names, numbers, arithmetic,
    comparisons, & | ~, and calls of the known functions. No attribute access, indexing, text, powers or
    anything else (the engine evaluates these rules; they come from an automated task)."""
    try:
        tree = ast.parse(str(expr), mode="eval")
    except SyntaxError as e:
        return [f"{expr!r}: not a valid rule ({e.msg})"]
    probs, calls = [], set()
    for node in ast.walk(tree):
        if not isinstance(node, _OPS):
            probs.append(f"{expr!r}: '{type(node).__name__}' is not allowed (only building blocks, numbers and "
                         "operators)")
        elif isinstance(node, ast.Constant) and (isinstance(node.value, bool) or not isinstance(node.value, (int, float))):
            probs.append(f"{expr!r}: only numbers may be written as values")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(id(node.func))
            if not isinstance(node.func, ast.Name) or node.func.id not in FUNCTIONS:
                probs.append(f"{expr!r}: unknown function "
                             f"{node.func.id if isinstance(node.func, ast.Name) else ast.unparse(node.func)!r}")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and id(node) not in calls:
            if node.id in H4_COLUMNS:
                if not set(tfs) <= set(H4_TFS):
                    probs.append(f"{expr!r}: {node.id} exists only below 4H (timeframes {H4_TFS})")
            elif node.id not in COLUMNS:
                probs.append(f"{expr!r}: unknown building block {node.id!r}"
                             + (" (a function - call it, e.g. ema(close,20))" if node.id in FUNCTIONS else ""))
    return list(dict.fromkeys(probs))


def _entry_rules(card):
    return [r for k in ("long", "short") for r in (card.get(k) or [])]


def smc_blocks(card):
    return {n for r in _entry_rules(card) for n in _names(r) if n.startswith(SPECIAL_PREFIXES)}


def special(card):
    """The special ingredient a control twin must isolate: SMC / ICT building blocks in the entry rules, or the
    5-minute confirmation. None = a plain indicator card."""
    if card.get("confirm_5m"):
        return "the 5-minute confirmation"
    used = sorted(smc_blocks(card))
    return f"SMC building blocks ({', '.join(used)})" if used else None


def tp1_r(card, side):
    """How far the first target is, in R, at least (None = not known in advance / not >= a fixed R)."""
    tg = card.get("targets") or {}
    first = (tg.get(side) or [None])[0]
    if first is None:
        return None
    p = parse_target(first)
    if p[0] == "r":
        return p[1]
    if p[0] == "max":                       # the farther of the two: at least the R part
        return max([q[1] for q in p[1] if q[0] == "r"], default=None)
    need = tg.get("need") or {}             # a column target: only when `need` demands it is min_r away
    return float(need.get("min_r") or 0) if need.get(side) == p[1] else None


def lab_card_problems(card, others, labels, timeframes):
    """Everything a LAB card must meet on its own (and against the cards it names). others = {id: card} of every
    other card in strategies.yaml and strategies_lab.yaml. [] = fine."""
    if not isinstance(card, dict):
        return ["not a strategy card (a block of 'name: value' lines)"]
    probs = check(card, labels, timeframes)
    if probs:
        return probs
    try:
        r = render(card)
    except KeyError as e:
        return [f"rule uses {{{e.args[0]}}} but params does not define it"]
    tfs = card["timeframes"]
    for k in ("long", "short", "exit_long", "exit_short"):
        for rule in r.get(k) or []:
            probs += expr_problems(rule, tfs)
    st = r["stop"]
    if st.get("method") == "structure":
        probs += expr_problems(st["long_level"], tfs) + expr_problems(st["short_level"], tfs)
    for c in columns_needed(r) - {st.get("long_level"), st.get("short_level")}:
        probs += expr_problems(c, tfs)
    if not card.get("targets"):
        probs.append(f"targets missing - the config default takes profit at 1R; a lab card's first target must be "
                     f">= {MIN_TP1_R:g}R")
    else:
        for side in ("long", "short"):
            x = tp1_r(r, side)
            if x is None or x < MIN_TP1_R:
                probs.append(f"first {side} target must be >= {MIN_TP1_R:g}R (e.g. \"2R\", \"max(2R, smc_liq_above)\", or "
                             f"a level with need.min_r >= {MIN_TP1_R:g})")
    cls = str(card.get("evidence_class") or "").split(":")[0].strip()
    if cls not in EVIDENCE_CLASSES:
        probs.append(f"evidence_class must be one of {EVIDENCE_CLASSES} (how strong the source is)")
    log = card.get("changelog")
    if not isinstance(log, list) or not any(str(x).startswith(str(card["version"])) for x in log):
        probs.append(f"changelog needs a line starting with \"{card['version']}\" (what this version is / changes)")
    if not card.get("twin_of"):                                 # a control twin is a benchmark, not an idea
        probs += edge_problems(card)
    ing = None if card.get("twin_of") else special(card)       # a control twin is itself the benchmark
    twin = others.get(card.get("control_twin")) if card.get("control_twin") else None
    if ing and not card.get("control_twin"):
        probs.append(f"uses {ing} - needs control_twin: the same card without it (it must be beaten)")
    elif card.get("control_twin") and twin is None:
        probs.append(f"control_twin '{card['control_twin']}' is not in strategies.yaml or strategies_lab.yaml")
    elif twin is not None and not card.get("confirm_5m"):
        if twin.get("twin_of") != card["id"]:
            probs.append(f"control_twin '{card['control_twin']}' must be written as this card's twin "
                         f"(twin_of: {card['id']})")
        if ing and not smc_blocks(twin) < smc_blocks(card):
            probs.append(f"control_twin '{card['control_twin']}' keeps the whole special ingredient - the twin must "
                         "be the same idea WITHOUT it")
    if card.get("twin_of") and card["twin_of"] not in others:
        probs.append(f"twin_of '{card['twin_of']}' is not in strategies.yaml or strategies_lab.yaml")
    return list(dict.fromkeys(probs))


def edge_problems(card):
    """The edge block: edge: {type, who_pays, mechanism, works_in, fails_when, kill_rule}.
    type: one of EDGE_TYPES; works_in: the regimes it should work in (a subset of the card's regimes); the other four
    a real sentence each."""
    e = card.get("edge")
    if not isinstance(e, dict):
        return ["edge block missing - edge: {type: <" + " | ".join(EDGE_TYPES) + ">, works_in: [<regimes>], "
                + ", ".join(f"{k}: <{v}>" for k, v in EDGE_KEYS.items()) + "}"]
    probs = [f"edge.{k} missing or too short ({EDGE_KEYS[k]}; at least {EDGE_MIN_CHARS} characters)"
             for k in EDGE_KEYS if len(" ".join(str(e.get(k) or "").split())) < EDGE_MIN_CHARS]
    if e.get("type") not in EDGE_TYPES:
        probs.append(f"edge.type must be one of {sorted(EDGE_TYPES)} (who is on the other side and why they lose)")
    w = e.get("works_in")
    if not isinstance(w, list) or not w:
        probs.append("edge.works_in must list the regimes it should work in, e.g. [STRONG_BULL, WEAK_BULL]")
    elif set(w) - set(card.get("regimes") or []):
        probs.append(f"edge.works_in {sorted(set(w) - set(card.get('regimes') or []))} are not in the card's regimes")
    return probs


def edge_lines(card):
    """The edge block as plain lines ([] when the card has none)."""
    e = card.get("edge")
    if not isinstance(e, dict):
        return []
    names = {"who_pays": "Who pays", "mechanism": "Mechanism", "fails_when": "Fails when", "kill_rule": "Kill rule"}
    w = e.get("works_in")
    return ([f"Type: {e.get('type') or '-'}", f"Works in: {', '.join(w) if isinstance(w, list) else w or '-'}"]
            + [f"{names[k]}: {' '.join(str(e.get(k) or '-').split())}" for k in EDGE_KEYS])


def _vkey(v):
    return tuple(int(x) for x in str(v).split("."))


def change_count(old, new):
    """How many things a new version changes vs the version before (section 10: exactly ONE per version).
    Entry rules (long + short together), exits, stop, targets, time stop, cooldown, regimes, timeframes, gate,
    family and the 5m check each count once; each parameter whose value changed counts once (a parameter that
    comes or goes with a rule change belongs to that change)."""
    groups = [("long", "short"), ("exit_long", "exit_short"), ("stop",), ("targets",), ("time_stop_bars",),
              ("cooldown_bars",), ("regimes",), ("timeframes",), ("gate",), ("family",), ("confirm_5m",)]
    norm = {"cooldown_bars": 0, "confirm_5m": False}
    diff = [g for g in groups if any(old.get(k, norm.get(k)) != new.get(k, norm.get(k)) for k in g)]
    po, pn = old.get("params") or {}, new.get("params") or {}
    diff += [(f"params.{k}",) for k in sorted(set(po) & set(pn)) if po[k] != pn[k]]
    if ("long", "short") not in diff and set(po) != set(pn):
        diff.append(("params",))
    return ["/".join(g) for g in diff]


def version_problems(card, earlier):
    """A lab card is a NEW id, or a NEW version of an existing id that changes exactly one thing vs its latest
    version. earlier = every card already in strategies.yaml / strategies_lab.yaml (and earlier in this push)."""
    same = [c for c in earlier if isinstance(c, dict) and c.get("id") == card.get("id")]
    if not same:
        return []
    v = str(card.get("version"))
    if any(str(c.get("version")) == v for c in same):
        return [f"{card['id']}@{v} already exists - a card is never changed; write a new version"]
    try:
        last = max(same, key=lambda c: _vkey(c.get("version")))
        if _vkey(v) <= _vkey(last.get("version")):
            return [f"version {v} must be higher than the latest {card['id']} version {last['version']}"]
    except ValueError:
        return [f"version {v!r} must look like \"1.1\""]
    diff = change_count(last, card)
    if len(diff) != 1:
        return [f"a new version changes exactly ONE thing vs v{last['version']} - this one changes "
                f"{len(diff)}: {', '.join(diff) or 'nothing'}"]
    return []


def load_library(main_items, lab_items, labels, timeframes):
    """strategies.yaml + strategies_lab.yaml, checked. Lab cards are marked lab=True and must also pass
    lab_card_problems (building blocks only). A lab card whose id@version is also in strategies.yaml has been moved
    there by the operator: the strategies.yaml copy is used. Returns (runnable, problems, idle, moved keys)."""
    main_items = [x for x in (main_items or [])]
    main_keys = {f"{x.get('id')}@{x.get('version')}" for x in main_items if isinstance(x, dict)}
    everything = {x.get("id"): x for x in main_items + list(lab_items or []) if isinstance(x, dict)}
    items, bad, moved = list(main_items), {}, []
    for i, c in enumerate(lab_items or [], 1):
        name = f"lab: {c.get('id') if isinstance(c, dict) and c.get('id') else f'#{i}'}"
        if isinstance(c, dict) and f"{c.get('id')}@{c.get('version')}" in main_keys:
            moved.append(f"{c['id']}@{c['version']}")
            continue
        others = {k: v for k, v in everything.items() if k != (c.get("id") if isinstance(c, dict) else None)}
        errs = lab_card_problems(c, others, labels, timeframes)
        if errs:
            bad[name] = errs
            continue
        items.append(dict(c, lab=True))
    ok, problems, idle = load(items, labels, timeframes)
    problems.update(bad)
    return ok, problems, idle, moved
