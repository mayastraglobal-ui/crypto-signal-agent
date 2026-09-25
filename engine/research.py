"""
Research layers and promotion evidence (AGENT_PROMPT.md sections 11 and 12).

- Layer A: the last 15 days (days 1-10 vs days 11-15). Shown only - never enough alone.
- Layer B: the longest history available, develop (first 70% of each coin) vs validate (last 30%).
- Layer C: walk-forward - the history cut into time windows; does the edge hold window after window?
  (Nothing is fitted to the data, so every window after the warm-up one is out of sample.)
- cost viability (stop >= 4x the round-trip cost), costs +50%, +-20% parameter changes,
  edge on >= 3 coins, overfitting flag, control twin.
- Phase 18 B: Monte Carlo trade-order shuffling (95% worst drawdown, longest losing streak) and rule significance
  (does each entry rule improve the result?) - ideas from Jesse (R5), rewritten; no code copied.

Pure functions only: no internet, no files.
"""
import numpy as np

from engine import trials

DAY_MS = 86_400_000


def stats(trades):
    """Summary of trades, in time order (drawdown is measured in the order trades happened)."""
    if not trades:
        return dict(n=0, win_rate=0.0, exp_r=0.0, pf=0.0, max_dd_r=0.0, avg_bars=0.0, total_r=0.0)
    trades = sorted(trades, key=lambda t: t.get("entry_time", 0))
    r = np.array([t["r"] for t in trades])
    gains, losses = r[r > 0].sum(), -r[r < 0].sum()
    eq = np.cumsum(r)
    dd = float((np.maximum.accumulate(np.r_[0, eq]) - np.r_[0, eq]).max())
    return dict(n=len(r), win_rate=float((r > 0).mean()), exp_r=float(r.mean()),
                pf=float(gains / losses) if losses > 0 else float("inf") if gains > 0 else 0.0,
                max_dd_r=dd, avg_bars=float(np.mean([t["bars"] for t in trades])), total_r=float(r.sum()))


def short(st):
    """A stats dict made safe for JSON / tables."""
    return dict(n=st["n"], win_rate=round(st["win_rate"] * 100, 1), avg_r=round(st["exp_r"], 3),
                pf=round(st["pf"], 2) if np.isfinite(st["pf"]) else 99.0, max_dd_r=round(st["max_dd_r"], 1),
                total_r=round(st["total_r"], 1), avg_bars=round(st["avg_bars"], 1))


def layer_a(trades, now_ms, days=15, split_day=10):
    """Trades that STARTED in the last `days` days: all, days 1-split_day, and the rest (newest)."""
    start = now_ms - days * DAY_MS
    mid = start + split_day * DAY_MS
    recent = [t for t in trades if t["entry_time"] >= start]
    return dict(all=short(stats(recent)),
                first=short(stats([t for t in recent if t["entry_time"] < mid])),
                last=short(stats([t for t in recent if t["entry_time"] >= mid])))


def windows(t0, t1, k):
    """k equal time windows [start, end) covering t0..t1."""
    edges = np.linspace(t0, t1, k + 1)
    return [(int(edges[i]), int(edges[i + 1])) for i in range(k)]


def walk_forward(trades, wins, min_trades, min_positive):
    """Layer C. wins[0] is the warm-up window; the others are judged in time order.
    A window with fewer than min_trades trades is 'no information' (not a win).
    Pass = at least min_positive profitable windows AND all judged windows together profitable."""
    rows = []
    for i, (a, b) in enumerate(wins):
        st = stats([t for t in trades if a <= t["entry_time"] < b])
        rows.append(dict(window=i, start=a, end=b, n=st["n"], avg_r=round(st["exp_r"], 3),
                         total_r=round(st["total_r"], 2), warm_up=i == 0,
                         verdict="warm-up" if i == 0 else "too few trades" if st["n"] < min_trades
                         else "profitable" if st["exp_r"] > 0 else "losing"))
    judged = [t for t in trades if wins and wins[1][0] <= t["entry_time"] < wins[-1][1]] if len(wins) > 1 else []
    pooled = stats(judged)
    positive = sum(r["verdict"] == "profitable" for r in rows)
    return dict(windows=rows, positive=positive, judged=len(wins) - 1, pooled_avg_r=round(pooled["exp_r"], 3),
                pooled_n=pooled["n"], passed=bool(positive >= min_positive and pooled["exp_r"] > 0))


def by_coin(per_coin):
    return {c: short(stats(tr)) for c, tr in per_coin.items()}


def concentration(parts):
    """Largest share of the profit coming from one part (coin or window). parts: {name: total R}."""
    pos = {k: v for k, v in parts.items() if v > 0}
    total = sum(pos.values())
    if total <= 0:
        return None, 0.0
    k = max(pos, key=pos.get)
    return k, pos[k] / total


def evaluate(per_coin, stress_per_coin, variant_results, wins, cfg_r, min_coin_trades):
    """Everything Phase 8 measures for ONE strategy version x timeframe (pooled over coins).
    per_coin / stress_per_coin: {coin: trades}; variant_results: {label: {coin: (trades, total R)}}.
    Returns a JSON-ready dict; the verdicts (gates) are applied in engine/lifecycle.py."""
    allt = [t for tr in per_coin.values() for t in tr]
    st = stats(allt)
    dev, val = stats([t for t in allt if not t["oos"]]), stats([t for t in allt if t["oos"]])
    coins = by_coin(per_coin)
    pos_coins = sorted(c for c, x in coins.items() if x["n"] >= min_coin_trades and x["avg_r"] > 0)
    wf = walk_forward(allt, wins, int(cfg_r["walk_forward_min_trades"]), int(cfg_r["walk_forward_min_positive"]))
    stress = stats([t for tr in stress_per_coin.values() for t in tr])
    var_rows = []
    for label, pc in variant_results.items():
        n = sum(x[0] for x in pc.values())
        var_rows.append(dict(change=label, n=n, avg_r=round(sum(x[1] for x in pc.values()) / n, 3) if n else 0.0))
    worst = min(var_rows, key=lambda x: x["avg_r"]) if var_rows else None
    costs = [t["cost_r"] for t in allt if np.isfinite(t.get("cost_r", np.nan))]
    top_coin, coin_share = concentration({c: x["total_r"] for c, x in coins.items()})
    top_win, win_share = concentration({f"window {r['window']}": r["total_r"] for r in wf["windows"]
                                        if not r["warm_up"]})
    limit = float(cfg_r["overfit_max_share"])
    overfit = []
    if st["exp_r"] > 0 and coin_share > limit:
        overfit.append(f"{coin_share * 100:.0f}% of the profit from {top_coin}")
    if st["exp_r"] > 0 and win_share > limit:
        overfit.append(f"{win_share * 100:.0f}% of the profit from {top_win}")
    return dict(all=short(st), develop=short(dev), validate=short(val),
                t_stat=(lambda x: None if x is None else round(x, 3))(trials.t_stat([t["r"] for t in allt])),
                long=short(stats([t for t in allt if t["dir"] == 1])),
                short=short(stats([t for t in allt if t["dir"] == -1])),
                by_coin=coins, positive_coins=pos_coins, walk_forward=wf,
                stress=short(stress), perturbation=dict(variants=var_rows, worst=worst,
                                                        stable=bool(var_rows) and all(v["n"] > 0 and v["avg_r"] > 0
                                                                                      for v in var_rows)),
                median_cost_r=round(float(np.median(costs)), 3) if costs else None,
                overfit=overfit, _raw=dict(st=st, dev=dev, val=val))


def monte_carlo(r, runs=1000, seed=7, chunk=100):
    """Trade-order shuffling (Phase 18 B): the same trades in `runs` random orders. The results of the trades stay
    the same - only their order changes - so this shows how deep a drawdown and how long a losing streak the SAME
    edge can produce by bad luck. r: trade results in R (any order). Deterministic (fixed seed).
    Returns dict(runs, n, dd_r, dd_median_r, dd95_r, streak, streak_median, streak95) or None (< 2 trades)."""
    r = np.asarray(r, dtype=float)
    n = len(r)
    if n < 2:
        return None
    rng = np.random.default_rng(seed)
    dd, st = np.empty(runs), np.empty(runs, dtype=int)
    for a in range(0, runs, chunk):
        k = min(chunk, runs - a)
        m = rng.permuted(np.broadcast_to(r, (k, n)), axis=1)
        dd[a:a + k] = _max_dd(m)
        st[a:a + k] = _max_streak(m < 0)
    return dict(runs=int(runs), n=int(n), dd_r=round(float(_max_dd(r[None, :])[0]), 1),
                dd_median_r=round(float(np.median(dd)), 1), dd95_r=round(float(np.percentile(dd, 95)), 1),
                streak=int(_max_streak(r[None, :] < 0)[0]), streak_median=int(np.median(st)),
                streak95=int(np.ceil(np.percentile(st, 95))))


def _max_dd(m):
    """Largest fall from a peak of the running total, per row (the start counts as a peak at 0)."""
    eq = np.cumsum(m, axis=1)
    eq = np.concatenate([np.zeros((len(m), 1)), eq], axis=1)
    return (np.maximum.accumulate(eq, axis=1) - eq).max(axis=1)


def _max_streak(loss):
    """Longest run of True per row."""
    c = np.cumsum(loss, axis=1)
    last_reset = np.maximum.accumulate(np.where(loss, 0, c), axis=1)
    return (c - last_reset).max(axis=1)


def mc_gate(mc, limit_r):
    """PAPER_TRADING also needs the 95% worst drawdown within the risk limit. (passed, reason or None)."""
    if mc is None:
        return False, "Monte Carlo: fewer than 2 trades"
    if mc["dd95_r"] > limit_r:
        return False, (f"Monte Carlo: 95% worst drawdown {mc['dd95_r']:.1f}R over {mc['runs']} shuffles of "
                       f"{mc['n']} trades - above the {limit_r:g}R limit")
    return True, None


def rule_significance(base, drops, min_trades):
    """Does each entry rule improve the result? base = stats of the card as written (short()); drops = {label:
    (rule text, {coin: (trades, total R)})} for the card with that rule removed. A rule 'adds nothing' when the
    card without it has at least min_trades trades and an average per trade at least as good (after costs).
    Returns [dict(label, rule, n, avg_r, adds)] - adds None = too few trades to judge."""
    out = []
    for label, (rule, pc) in drops.items():
        n = sum(x[0] for x in pc.values())
        avg = round(sum(x[1] for x in pc.values()) / n, 3) if n else None
        adds = None
        if n >= min_trades and base["n"] >= min_trades:
            adds = bool(base["avg_r"] > avg)
        out.append(dict(label=label, rule=rule, n=int(n), avg_r=avg, adds=adds))
    return out
