"""
Strategy lifecycle, promotion gates and market gates (AGENT_PROMPT.md sections 5, 6, 11, 12).

  IDEA -> FORMALIZED -> BACKTESTING -> VALIDATION -> PAPER_TRADING -> APPROVED (operator OK)
                                    \\-> FAILED                        -> RETIRED / REVISED

- The AUTHOR sets IDEA / FORMALIZED / RETIRED in strategies.yaml.
- The ENGINE sets BACKTESTING / VALIDATION / FAILED per strategy version and timeframe, every run.
- PAPER_TRADING needs the Phase 8 tests (walk-forward windows, costs +50%, +-20% parameters,
  beating the control twin), so nothing can reach it yet. APPROVED always needs the operator's yes.

Market gates (applied to every candle, in backtests AND live, using closed candles only):
- regime gate: the strategy trades only in the regimes it lists (on its regime timeframe);
- permission gate: see strategy_spec.GATES.

Pure functions only: no internet, no files.
"""
import numpy as np
import pandas as pd

from engine import regime as rg

ENGINE_STATUSES = ["BACKTESTING", "VALIDATION", "FAILED", "PAPER_TRADING", "APPROVED"]
PERMISSION_TFS = ["1d", "4h", "1h"]


def regime_tf(tf):
    """Which timeframe's regime a signal timeframe must respect: 1D -> 1D, 4H -> 4H, 1H and below -> 1H."""
    return tf if tf in ("1d", "4h") else "1h"


def directions(labels, exp_dirs):
    """Vectorised regime.direction(): +1 bullish, -1 bearish, 0 neither."""
    labels = np.asarray(labels, dtype=object)
    exp_dirs = np.asarray(exp_dirs, dtype=object)
    bull = np.isin(labels, list(rg.BULL)) | ((labels == "EXPANSION") & (exp_dirs == "up"))
    bear = np.isin(labels, list(rg.BEAR)) | ((labels == "EXPANSION") & (exp_dirs == "down"))
    return np.where(bull, 1, np.where(bear, -1, 0))


def gate_arrays(spec, tf, reg, n):
    """For each of n trade candles: may this strategy go long / short here?
    reg: {regime timeframe: (labels, expansion directions)} already aligned to the trade candles
    (closed candles only); a missing timeframe counts as 'no information' (UNCLEAR, no veto).
    Returns (long_ok, short_ok, regime_ok, perm_long, perm_short)."""
    def lab(t):
        return np.asarray(reg[t][0], dtype=object) if t in reg else np.full(n, None, dtype=object)

    def dirs(t):
        return directions(*reg[t]) if t in reg else np.zeros(n, int)

    regime_ok = np.isin(lab(regime_tf(tf)), list(spec["regimes"]))
    wk = lab("1w")
    if spec["gate"] == "mean_reversion":
        strong_bear = np.zeros(n, bool)
        strong_bull = np.zeros(n, bool)
        for t in ["1w", "1d", "4h"]:
            strong_bear |= lab(t) == "STRONG_BEAR"
            strong_bull |= lab(t) == "STRONG_BULL"
        perm_long, perm_short = ~strong_bear, ~strong_bull
    else:
        d = np.vstack([dirs(t) for t in PERMISSION_TFS])
        perm_long, perm_short = (d == 1).sum(0) >= 2, (d == -1).sum(0) >= 2
        if spec["gate"] == "trend":                  # weekly veto; reversal types are exempt (section 5)
            perm_long &= wk != "STRONG_BEAR"
            perm_short &= wk != "STRONG_BULL"
    return regime_ok & perm_long, regime_ok & perm_short, regime_ok, perm_long, perm_short


def judge(st, ins, oos, live, V, penalty_r=0.0):
    """Section 12 '-> VALIDATION' gate on one strategy version x timeframe (all coins pooled).
    st / ins / oos: stats of all / develop (first 70%) / unseen test (last 30%) trades.
    live: forward-test stats or None. Returns (status, reasons, required expectancy)."""
    need = V["min_expectancy_r"] + penalty_r
    reasons = []
    if st["n"] < V["min_trades"]:
        reasons.append(f"only {st['n']} trades")
    if st["exp_r"] < need:
        reasons.append(f"avg {st['exp_r']:+.2f}R/trade (needs {need:+.2f}R)")
    if st["pf"] < V["min_profit_factor"]:
        reasons.append(f"profit factor {st['pf']:.2f}")
    if st["max_dd_r"] > V["max_drawdown_r"]:
        reasons.append(f"max drawdown {st['max_dd_r']:.1f}R")
    if oos["n"] < V["min_oos_trades"]:
        reasons.append(f"only {oos['n']} unseen-test trades")
    if ins["exp_r"] <= 0 or oos["exp_r"] <= 0:
        reasons.append("not profitable in BOTH train and unseen test")
    live_bad = bool(live and live["n"] >= V["forward_pause_after"] and live["exp_r"] < V["forward_pause_below_r"])
    if live_bad:
        reasons.append(f"LIVE results bad ({live['exp_r']:+.2f}R over {live['n']} signals)")
    if not reasons:
        return "VALIDATION", reasons, need
    if live_bad or (st["n"] >= V["min_trades"] and (st["exp_r"] <= 0 or oos["exp_r"] <= 0)):
        return "FAILED", reasons, need
    return "BACKTESTING", reasons, need


def empty_registry():
    return dict(versions={}, cells={})


VERSION_COLS = ["id", "version", "family", "fingerprint", "experiment", "first_tested_utc", "hypothesis"]
CELL_COLS = ["tf", "status", "since_utc", "last_checked_utc", "trades", "avg_r", "profit_factor", "max_dd_r",
             "train_avg_r", "test_avg_r", "required_avg_r", "beats_twin", "gates_failed"]


def registry_to_frame(reg):
    """memory/strategy_registry.csv (section 22): one row per strategy version x timeframe."""
    rows = []
    for ck, cell in reg["cells"].items():
        k = ck.split("|")[0]
        v = reg["versions"].get(k, {})
        rows.append({**{c: v.get(c) for c in VERSION_COLS}, "tf": ck.split("|")[1],
                     **{c: cell.get(c) for c in CELL_COLS if c != "tf"}})
    return pd.DataFrame(rows, columns=VERSION_COLS + CELL_COLS).sort_values(["experiment", "tf"])


def registry_from_frame(df):
    reg = empty_registry()
    for r in df.to_dict("records"):
        r = {k: (None if isinstance(x, float) and np.isnan(x) else x) for k, x in r.items()}
        k = f"{r['id']}@{r['version']}"
        reg["versions"][k] = {c: r[c] for c in VERSION_COLS}
        reg["versions"][k]["experiment"] = int(r["experiment"])
        reg["cells"][f"{k}|{r['tf']}"] = {c: r[c] for c in CELL_COLS if c != "tf"}
    return reg


def immutable_problem(reg, spec, fp):
    """A tested version whose trade rules changed without a new version number is refused."""
    k = f"{spec['id']}@{spec['version']}"
    old = reg["versions"].get(k)
    if old and old["fingerprint"] != fp:
        return (f"{k} was already tested with different rules - a tested version never changes. "
                f"Give the new rules a new version (e.g. {spec['version']} -> {_next(spec['version'])}) "
                "and a changelog line")
    return None


def _next(v):
    a, b = v.split(".")
    return f"{a}.{int(b) + 1}"


def retune_penalty(reg, spec, step):
    """+step R of required expectancy for every EARLIER version of the same idea (section 11)."""
    k = f"{spec['id']}@{spec['version']}"
    earlier = [x for x, v in reg["versions"].items() if v["id"] == spec["id"] and x != k]
    return step * len(earlier)


def update(reg, specs, fps, results, now):
    """Record new versions (the experiment log) and status changes per version x timeframe.
    results: {(id, version, tf): status}. Returns (registry, new experiments, status changes)."""
    new_exp, changes = [], []
    for s in specs:
        k = f"{s['id']}@{s['version']}"
        if k not in reg["versions"]:
            reg["versions"][k] = dict(id=s["id"], version=s["version"], fingerprint=fps[k], family=s["family"],
                                      first_tested_utc=now, hypothesis=s["hypothesis"].strip(),
                                      experiment=len(reg["versions"]) + 1)
            new_exp.append(dict(reg["versions"][k], key=k, timeframes=s["timeframes"],
                                twin_of=s.get("twin_of")))
    for (sid, ver, tf), status in sorted(results.items()):
        ck = f"{sid}@{ver}|{tf}"
        old = reg["cells"].get(ck, {}).get("status")
        if old != status:
            changes.append(dict(key=f"{sid}@{ver}", tf=tf, old=old or "FORMALIZED", new=status))
            reg["cells"][ck] = dict(status=status, since_utc=now)
        reg["cells"][ck]["last_checked_utc"] = now
    return reg, new_exp, changes
