"""
Strategy specification v3 (AGENT_PROMPT.md section 10).

Every strategy in strategies.yaml is an "ID card": id, version, status, family, hypothesis, source,
allowed regimes, timeframes, long/short rules, stop, targets, time stop, cooldown, control twin,
known weaknesses and a changelog. This module reads and checks the cards, fingerprints the parts
that decide trades (a tested version may never change - section 10), and turns stop / target
settings into prices.

Pure functions only: no internet, no files.
"""
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
        bad = [f"{ref} '{s[ref]}' is not in strategies.yaml" for ref in ("control_twin", "twin_of")
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
