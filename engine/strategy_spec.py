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


def key(spec):
    return f"{spec['id']}@{spec['version']}"


def fingerprint(spec):
    """Short hash of the trade-deciding parts of a card."""
    core = {k: spec.get(k) for k in LOGIC_KEYS}
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
    """List of problems with one card (empty = fine)."""
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
    if spec.get("confirm_5m"):
        errs.append("confirm_5m: the 5-minute confirmation protocol arrives in Phase 10 - set it to false")
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
        s = dict(s, version=str(s["version"]), cooldown_bars=int(s.get("cooldown_bars", 0) or 0))
        seen.add(key(s))
        (ok if s["status"] == "FORMALIZED" else idle).append(s)
    ids = {s["id"] for s in ok + idle}
    for s in list(ok):
        bad = [f"{ref} '{s[ref]}' is not in strategies.yaml" for ref in ("control_twin", "twin_of")
               if s.get(ref) and s[ref] not in ids]
        if bad:
            problems.setdefault(s["id"], []).extend(bad)
            ok.remove(s)
    return ok, problems, idle


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
