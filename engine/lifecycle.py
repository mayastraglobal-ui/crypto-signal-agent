"""
Strategy lifecycle, promotion gates and market gates (AGENT_PROMPT.md sections 5, 6, 11, 12).

  IDEA -> FORMALIZED -> BACKTESTING -> VALIDATION -> PAPER_TRADING -> APPROVED (operator OK)
                                    \\-> FAILED                        -> RETIRED / REVISED

- The AUTHOR sets IDEA / FORMALIZED / RETIRED in strategies.yaml.
- The ENGINE sets BACKTESTING / VALIDATION / FAILED / PAPER_TRADING / RETIRED per strategy version and
  timeframe, once a day (research.py). PAPER_TRADING needs every Phase 8 test (walk-forward, costs +50%,
  +-20% parameters, >= 3 coins, no overfitting flag, beating the control twin). APPROVED always needs
  the operator's yes - the engine never sets it.

Market gates (applied to every candle, in backtests AND live, using closed candles only):
- regime gate: the strategy trades only in the regimes it lists (on its regime timeframe);
- permission gate: see strategy_spec.GATES.

Pure functions only: no internet, no files.
"""
import numpy as np
import pandas as pd

from engine import regime as rg

ENGINE_STATUSES = ["BACKTESTING", "VALIDATION", "FAILED", "PAPER_TRADING", "APPROVED", "RETIRED"]
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


def judge(st, ins, oos, live, V, penalty_r=0.0, median_cost_r=None):
    """Section 12 '-> VALIDATION' gate on one strategy version x timeframe (all coins pooled).
    st / ins / oos: stats of all / develop (first 70%) / unseen test (last 30%) trades.
    live: forward-test stats or None. median_cost_r: typical round-trip cost in R (section 11 cost
    viability: the stop must be >= 4x the round-trip cost, i.e. cost <= 0.25R). None = not checked.
    Returns (status, reasons, required expectancy)."""
    need = V["min_expectancy_r"] + penalty_r
    reasons = []
    if median_cost_r is not None and median_cost_r > V["max_cost_to_r"]:
        reasons.append(f"not cost-viable: fees + slippage {median_cost_r:.2f}R per trade "
                       f"(stop must be ≥ {1 / V['max_cost_to_r']:.0f}x the round-trip cost)")
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


def paper_gate(status, ev, twin, R):
    """Section 12 '-> PAPER_TRADING' (automatic). ev = research.evaluate() of this cell;
    twin = its control twin's evaluate() or None (only strategies that HAVE a twin need one).
    Returns (passed, reasons)."""
    reasons = []
    if status != "VALIDATION":
        reasons.append("not in VALIDATION")
    wf = ev["walk_forward"]
    if not wf["passed"]:
        reasons.append(f"walk-forward: {wf['positive']} of {wf['judged']} windows profitable, "
                       f"together {wf['pooled_avg_r']:+.2f}R")
    if len(ev["positive_coins"]) < R["min_positive_coins"]:
        reasons.append(f"edge on {len(ev['positive_coins'])} coin(s), needs {R['min_positive_coins']}")
    if ev["stress"]["avg_r"] <= 0:
        reasons.append(f"costs +50%: {ev['stress']['avg_r']:+.2f}R per trade")
    if not ev["perturbation"]["stable"]:
        w = ev["perturbation"]["worst"]
        reasons.append("±20% test: " + (f"{w['change']} gives {w['avg_r']:+.2f}R" if w else "not run"))
    if ev["overfit"]:
        reasons.append("HIGH OVERFITTING RISK: " + "; ".join(ev["overfit"]))
    if twin is not None:
        cmp = twin_compare(ev, twin, R)
        if cmp is not True:
            reasons.append("control twin: " + ("too few trades to compare" if cmp is None else "does not beat it"))
    return not reasons, reasons


def twin_compare(ev, twin, R):
    """True = beats the twin overall AND in the validate part; None = too few trades to tell."""
    a, b = ev["all"], twin["all"]
    if min(a["n"], b["n"]) < R["twin_min_trades"] or min(ev["validate"]["n"], twin["validate"]["n"]) < R["twin_min_validate_trades"]:
        return None
    return bool(a["avg_r"] > b["avg_r"] and ev["validate"]["avg_r"] > twin["validate"]["avg_r"])


def paper_record(results_r):
    """Closed PAPER signals of one cell, oldest first -> n, average of the last 20, drawdown."""
    r = np.asarray(results_r, dtype=float)
    if not len(r):
        return dict(n=0, last_avg_r=None, max_dd_r=0.0)
    eq = np.cumsum(r)
    dd = float((np.maximum.accumulate(np.r_[0, eq]) - np.r_[0, eq]).max())
    return dict(n=len(r), last_avg_r=float(r[-20:].mean()), max_dd_r=dd)


def next_status(prev, base, paper_ok, paper, failed_runs, R):
    """The lifecycle move for one strategy version x timeframe after a research run.
    prev: status before; base: judge() result on Layer B; paper_ok: paper_gate() passed;
    paper: paper_record(); failed_runs: consecutive runs that failed the VALIDATION gate while in paper.
    Returns (status, note, failed_runs). The engine never sets APPROVED."""
    if prev == "RETIRED":
        return "RETIRED", "retired - only a new version can be tested again", 0
    if prev in ("PAPER_TRADING", "APPROVED"):
        if paper["n"] >= R["paper_retire_last_n"] and paper["last_avg_r"] < R["paper_retire_below_r"]:
            return "RETIRED", (f"last {R['paper_retire_last_n']} paper signals average "
                               f"{paper['last_avg_r']:+.2f}R (limit {R['paper_retire_below_r']:+.2f}R)"), 0
        if paper["max_dd_r"] > R["paper_max_dd_r"]:
            return "RETIRED", f"paper drawdown {paper['max_dd_r']:.1f}R (limit {R['paper_max_dd_r']}R)", 0
        if base != "VALIDATION":
            failed_runs += 1
            if failed_runs >= R["demote_after_failed_runs"]:
                return base, f"failed the long-history test {failed_runs} runs in a row - leaves {prev}", 0
            return prev, f"failed the long-history test ({failed_runs} of {R['demote_after_failed_runs']} runs)", failed_runs
        return prev, "", 0
    if base == "VALIDATION" and paper_ok:
        return "PAPER_TRADING", "passed every Phase 8 test - paper signals start (logged, never emailed)", 0
    return base, "", 0


def empty_registry():
    return dict(versions={}, cells={})


VERSION_COLS = ["id", "version", "family", "fingerprint", "experiment", "first_tested_utc", "hypothesis"]
CELL_COLS = ["tf", "status", "since_utc", "last_checked_utc", "trades", "avg_r", "profit_factor", "max_dd_r",
             "train_avg_r", "test_avg_r", "required_avg_r", "beats_twin", "gates_failed",
             "history_from", "walk_forward", "stress_avg_r", "perturb_worst", "positive_coins",
             "median_cost_r", "overfit", "paper_gate_failed", "paper_signals", "failed_runs"]


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
        reg["versions"][k] = {c: r.get(c) for c in VERSION_COLS}      # older files lack newer columns
        reg["versions"][k]["experiment"] = int(r["experiment"])
        reg["cells"][f"{k}|{r['tf']}"] = {c: r.get(c) for c in CELL_COLS if c != "tf"}
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
