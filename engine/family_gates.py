"""
Strategy-family validation gates (Phase 19 A) - research only.

Why: validation.max_drawdown_r = 10R is one number for every family, measured on the trades of ALL coins over up to
~9 years. A drawdown in R grows with the number of trades, so a strategy with many trades is penalised for its sample
size, not for its risk. Trend / breakout / momentum strategies also win rarely and big, so they have deeper and longer
drawdowns than mean-reversion ones at the same edge.

The family table (config.yaml -> family_gates) replaces the single 10R gate with measurements that do not grow with
the number of trades:

  trend group (trend_following, momentum, breakout, mtf_pullback):
    recovery factor   net R / max drawdown (whole history)                                        >= min_recovery_factor
    DD per 100 trades Monte Carlo 95% worst drawdown of 100 trades drawn from the card's trades      <= max_mc_dd95_per_100_r
    DD duration       longest time below a previous peak, as a share of the tested period           <= max_dd_duration_share
    + ALL existing gates (expectancy, PF, unseen test, walk-forward, costs +50%, +-20%, coins, twin, trials bar, bias)
  tight group (mean_reversion, liquidity_reversal, smc, price_action and any family not listed):
    the existing 10R max drawdown and the 8R Monte Carlo limit stay, plus
    loss clustering   the real (time-ordered) longest losing streak must not be longer than 95% of random orders
    DD duration       as above, with the tight group's own limit

How the limits are chosen (fixed BEFORE looking at any card's verdict - calibrate() below, family_calibrate.py):
  reference = every historical trade of every card of the group (all timeframes, all coins, the latest research run),
  with the average moved to the pass bar (validation.min_expectancy_r) - "a strategy of this family with exactly the
  minimum acceptable edge". Every limit is the 95th percentile of that reference (the same 95% the engine already uses
  for Monte Carlo), rounded UP (0.5R / 0.05). No limit is fitted to one card.

Live safety (Phase 19 A item 2): the live suspension limit and paper_max_dd_r come from the same rule - the card's own
Monte Carlo 95% worst drawdown per 100 trades, never above its group limit (trend group); the tight group keeps
risk.strategy_max_dd_r / research.paper_max_dd_r.

Shadow mode: the new verdict is computed and shown next to the old one; nothing moves on it until the operator sets
mode: active AND operator_ok (a date at least shadow_days after shadow_start).

Pure functions only: no internet, no files.
"""
import datetime as dt
import math

import numpy as np

DAY_MS = 86_400_000
REEVAL_ORIGIN = "re-evaluation: family gates v{v}"
DEFAULTS = dict(rules_version=1, mode="shadow", shadow_start=None, shadow_days=14, operator_ok=None,
                window_trades=100, mc_runs=1000, reference_percentile=95, cost_report_x=2.0,
                default_group="tight", groups={})


def settings(section):
    s = dict(DEFAULTS)
    s.update(section or {})
    s["groups"] = {g: dict(v or {}) for g, v in (s.get("groups") or {}).items()}
    return s


def group_of(family, FG):
    """Which row of the family table a card belongs to; a family not listed falls into the default (tight) group."""
    for g, row in FG["groups"].items():
        if family in (row.get("families") or []):
            return g
    return FG["default_group"]


def mode(FG, today):
    """('active' | 'shadow', why). 'active' needs mode: active AND an operator_ok date on or after the end of the
    shadow period - otherwise the engine stays in shadow and says why (nothing moves on the new rule)."""
    if str(FG.get("mode")) != "active":
        return "shadow", "shadow mode: new verdicts are shown only"
    start, ok = _date(FG.get("shadow_start")), _date(FG.get("operator_ok"))
    if start is None:
        return "shadow", "mode: active needs shadow_start - still in shadow"
    end = start + dt.timedelta(days=int(FG["shadow_days"]))
    if ok is None:
        return "shadow", "mode: active needs operator_ok (the date of your yes) - still in shadow"
    if ok < end or today < end:
        return "shadow", f"the shadow period runs until {end} - still in shadow"
    return "active", f"active since your yes on {ok}"


def _date(x):
    if x in (None, ""):
        return None
    if isinstance(x, dt.date):
        return x
    try:
        return dt.date.fromisoformat(str(x)[:10])
    except ValueError:
        return None


# ---------------------------------------------------------------- measurements ----------------------------------

def _dd_rows(m):
    """Largest fall from a peak of the running total, per row (the start counts as a peak at 0)."""
    eq = np.concatenate([np.zeros((len(m), 1)), np.cumsum(m, axis=1)], axis=1)
    return (np.maximum.accumulate(eq, axis=1) - eq).max(axis=1)


def _streak_rows(loss):
    c = np.cumsum(loss, axis=1)
    return (c - np.maximum.accumulate(np.where(loss, 0, c), axis=1)).max(axis=1)


def window_mc(r, window=100, runs=1000, seed=11, chunk=250):
    """Monte Carlo per `window` trades: `runs` sequences of `window` trades drawn at random (with replacement) from
    the card's trades. The answer does not grow with the card's number of trades - it is "how deep can the next 100
    trades go by bad luck, with this card's own wins and losses". Deterministic (fixed seed).
    Returns dict(window, runs, dd95_r, dd_median_r, streak95) or None (< 2 trades)."""
    r = np.asarray(r, dtype=float)
    if len(r) < 2:
        return None
    rng = np.random.default_rng(seed)
    dd, st = np.empty(runs), np.empty(runs)
    for a in range(0, runs, chunk):
        k = min(chunk, runs - a)
        m = r[rng.integers(0, len(r), size=(k, window))]
        dd[a:a + k] = _dd_rows(m)
        st[a:a + k] = _streak_rows(m < 0)
    return dict(window=int(window), runs=int(runs), dd95_r=round(float(np.percentile(dd, 95)), 1),
                dd_median_r=round(float(np.median(dd)), 1), streak95=int(np.ceil(np.percentile(st, 95))))


def underwater(r, t):
    """Longest drawdown DURATION of the time-ordered equity curve: from the trade that set a peak to the trade that
    makes a new one (or the last trade, if it never recovered). r, t: results and entry times (ms), time order.
    Returns dict(days, trades, share, span_days, recovered) - share = days / the tested period."""
    r, t = np.asarray(r, dtype=float), np.asarray(t, dtype=np.int64)
    if not len(r):
        return dict(days=0.0, trades=0, share=0.0, span_days=0.0, recovered=True)
    eq = np.cumsum(r)
    best, peak_i, worst = 0.0, -1, (0, 0, True)       # the start is a peak at 0 (before the first trade)
    for i, x in enumerate(eq):
        if x > best + 1e-12:
            if i - peak_i > 1:
                worst = max(worst, (_ms_between(t, peak_i, i), i - peak_i - 1, True), key=lambda w: w[0])
            best, peak_i = x, i
    if peak_i < len(eq) - 1:                           # still under water at the end
        worst = max(worst, (_ms_between(t, peak_i, len(eq) - 1), len(eq) - 1 - peak_i, False), key=lambda w: w[0])
    span = float(t[-1] - t[0]) if len(t) > 1 else 0.0
    return dict(days=round(worst[0] / DAY_MS, 1), trades=int(worst[1]),
                share=round(worst[0] / span, 3) if span > 0 else 0.0, span_days=round(span / DAY_MS, 1),
                recovered=bool(worst[2]))


def _ms_between(t, a, b):
    return float(t[b] - t[max(a, 0)])


def clustering(r, runs=1000, seed=13, pct=95):
    """Loss clustering: is the real (time-ordered) longest losing streak longer than `pct`% of random orders of the
    same trades? Losses of a pooled multi-coin history bunch together when many coins lose at once (a crash day, a
    trend that runs over a mean-reversion idea). Returns dict(streak, streak95, clustered) or None (< 2 trades)."""
    r = np.asarray(r, dtype=float)
    if len(r) < 2:
        return None
    rng = np.random.default_rng(seed)
    st = np.empty(runs)
    for a in range(0, runs, 250):
        k = min(250, runs - a)
        st[a:a + k] = _streak_rows(rng.permuted(np.broadcast_to(r, (k, len(r))), axis=1) < 0)
    real = int(_streak_rows((r < 0)[None, :])[0])
    lim = int(np.ceil(np.percentile(st, pct)))
    return dict(streak=real, streak95=lim, clustered=bool(real > lim))


def measure(trades, FG):
    """Every family-gate measurement of one strategy version x timeframe (all coins pooled, entry-time order)."""
    tr = sorted(trades, key=lambda x: x.get("entry_time", 0))
    r = np.array([x["r"] for x in tr], dtype=float)
    t = np.array([x.get("entry_time", 0) for x in tr], dtype=np.int64)
    if not len(r):
        return dict(n=0, net_r=0.0, max_dd_r=0.0, recovery=None, window=None, duration=underwater(r, t),
                    clustering=None)
    eq = np.cumsum(r)
    dd = float((np.maximum.accumulate(np.r_[0, eq]) - np.r_[0, eq]).max())
    net = float(r.sum())
    return dict(n=int(len(r)), net_r=round(net, 1), max_dd_r=round(dd, 1),
                recovery=round(net / dd, 2) if dd > 0 else (None if net <= 0 else 99.0),   # 99 = no drawdown (JSON-safe)
                window=window_mc(r, int(FG["window_trades"]), int(FG["mc_runs"])),
                duration=underwater(r, t), clustering=clustering(r, int(FG["mc_runs"]),
                                                                 pct=float(FG["reference_percentile"])))


# ---------------------------------------------------------------- verdicts --------------------------------------

def dd_reasons(m, group, FG, V):
    """The drawdown part of the '-> VALIDATION' gate under the family table (it replaces the single max_drawdown_r
    check). Returns the failed checks (empty = passed)."""
    row = FG["groups"].get(group) or {}
    out = []
    win, dur, cl = m.get("window"), m.get("duration") or {}, m.get("clustering")
    if "min_recovery_factor" in row:
        rf = m.get("recovery")
        if rf is None or rf < float(row["min_recovery_factor"]):
            out.append(f"recovery factor {'-' if rf is None else f'{rf:.2f}'} (net {m['net_r']:+.1f}R / max drawdown "
                       f"{m['max_dd_r']:.1f}R) - needs {float(row['min_recovery_factor']):g}")
    if "max_mc_dd95_per_100_r" in row:
        if win is None or win["dd95_r"] > float(row["max_mc_dd95_per_100_r"]):
            got = "-" if win is None else f"{win['dd95_r']:.1f}R"
            out.append(f"Monte Carlo 95% worst drawdown per {FG['window_trades']} trades {got} - limit "
                       f"{float(row['max_mc_dd95_per_100_r']):g}R")
    if row.get("keep_max_drawdown_r", False) and m["max_dd_r"] > float(V["max_drawdown_r"]):
        out.append(f"max drawdown {m['max_dd_r']:.1f}R")
    if "max_dd_duration_share" in row and dur.get("share", 0) > float(row["max_dd_duration_share"]):
        out.append(f"longest drawdown {dur['days']:.0f} days = {dur['share'] * 100:.0f}% of the tested period "
                   f"(limit {float(row['max_dd_duration_share']) * 100:.0f}%)")
    if row.get("loss_clustering") and cl and cl["clustered"]:
        out.append(f"loss clustering: {cl['streak']} losses in a row as it happened, random orders stay at or below "
                   f"{cl['streak95']} in {FG['reference_percentile']:g}% of cases")
    return out


def uses_whole_history_mc(group, FG):
    """The tight group keeps the Phase 18 B whole-history Monte Carlo limit (8R) at PAPER_TRADING; the trend group
    replaces it with the per-100-trades Monte Carlo in dd_reasons()."""
    return bool((FG["groups"].get(group) or {}).get("keep_whole_history_mc", False))


def verdict(base_status, paper_ok):
    """The automatic verdict a rule set gives one cell today: PAPER_TRADING, VALIDATION, BACKTESTING or FAILED."""
    return "PAPER_TRADING" if base_status == "VALIDATION" and paper_ok else base_status


def live_limit(m, group, FG, risk_limit_r, paper_limit_r):
    """Item 2: the live suspension limit and the paper drawdown limit of one cell, from the SAME family rule.
    Trend group: the card's own Monte Carlo 95% worst drawdown per 100 trades (what bad luck alone can do to it),
    never above the group's limit. Tight group: unchanged (risk.strategy_max_dd_r / research.paper_max_dd_r).
    Returns dict(live_r, paper_r, rule)."""
    row = FG["groups"].get(group) or {}
    win = m.get("window")
    if "max_mc_dd95_per_100_r" in row and win:
        lim = min(float(win["dd95_r"]), float(row["max_mc_dd95_per_100_r"]))
        return dict(live_r=lim, paper_r=lim, rule=f"own Monte Carlo 95% worst drawdown per {FG['window_trades']} "
                                                  f"trades (cap {float(row['max_mc_dd95_per_100_r']):g}R)")
    return dict(live_r=float(risk_limit_r), paper_r=float(paper_limit_r), rule="unchanged (tight group)")


# ---------------------------------------------------------------- calibration -----------------------------------

def _round_up(x, step):
    return math.ceil(round(x / step, 9)) * step


def calibrate(cells, min_exp_r, min_trades, window=100, draws=20000, pct=95, seed=17):
    """The family table's limits from history (the method is fixed; the numbers come out of the data).
    cells: {cell key: (r list, entry-time list)} of ONE group - every card of the group's families, every timeframe,
    all coins pooled, as the latest research run produced them.
    reference = the trades with their average moved to min_exp_r (the pass bar): the same spread of wins and losses,
    exactly the minimum acceptable edge.
      max_mc_dd95_per_100_r = pct-th percentile of the drawdown of `draws` random 100-trade sequences of the
                              pooled reference, rounded up to 0.5R
      max_dd_duration_share = pct-th percentile, over the group's cells with >= min_trades trades, of the longest
                              drawdown (share of the tested period) of each cell's OWN time-ordered trades with the
                              average moved to the pass bar (keeps each card's real bunching of losses), up 0.05
    Also shown (not limits): the recovery factor of those shifted cells, and how often real histories cluster losses.
    Returns a JSON-ready dict."""
    rng = np.random.default_rng(seed)
    pooled = np.concatenate([np.asarray(r, dtype=float) for r, _ in cells.values()]) if cells else np.zeros(0)
    out = dict(cells=len(cells), trades=int(len(pooled)), pass_bar_r=float(min_exp_r), window=int(window),
               draws=int(draws), percentile=pct)
    if len(pooled) < 2:
        return out
    ref = pooled - pooled.mean() + float(min_exp_r)
    dd = np.concatenate([_dd_rows(ref[rng.integers(0, len(ref), size=(min(2000, draws - a), window))])
                         for a in range(0, draws, 2000)])
    out.update(raw_avg_r=round(float(pooled.mean()), 3), sd_r=round(float(pooled.std(ddof=1)), 3),
               win_rate=round(float((pooled > 0).mean()), 3),
               dd_per_100=dict(p50=round(float(np.percentile(dd, 50)), 2), p75=round(float(np.percentile(dd, 75)), 2),
                               p90=round(float(np.percentile(dd, 90)), 2), p95=round(float(np.percentile(dd, 95)), 2),
                               p99=round(float(np.percentile(dd, 99)), 2)),
               max_mc_dd95_per_100_r=_round_up(float(np.percentile(dd, pct)), 0.5))
    shares, rfs, per_cell, clustered = [], [], {}, 0
    for k, (r, t) in sorted(cells.items()):
        r = np.asarray(r, dtype=float)
        if len(r) < min_trades:
            continue
        o = np.argsort(np.asarray(t, dtype=np.int64), kind="stable")
        rs_, ts = r[o] - r.mean() + float(min_exp_r), np.asarray(t, dtype=np.int64)[o]
        u = underwater(rs_, ts)
        eq = np.cumsum(rs_)
        mdd = float((np.maximum.accumulate(np.r_[0, eq]) - np.r_[0, eq]).max())
        rf = float(rs_.sum()) / mdd if mdd > 0 else math.inf
        c = clustering(r[o], 1000, pct=pct)
        clustered += bool(c and c["clustered"])
        shares.append(u["share"])
        rfs.append(rf)
        per_cell[k] = dict(n=int(len(r)), shifted_by_r=round(float(min_exp_r) - float(r.mean()), 3),
                           dd_share=u["share"], dd_days=u["days"], recovery=round(rf, 2) if np.isfinite(rf) else None,
                           real_streak=c["streak"] if c else None, streak95=c["streak95"] if c else None)
    if shares:
        s = np.array(shares)
        out.update(duration_share=dict(p50=round(float(np.percentile(s, 50)), 3),
                                       p75=round(float(np.percentile(s, 75)), 3),
                                       p95=round(float(np.percentile(s, pct)), 3), max=round(float(s.max()), 3)),
                   max_dd_duration_share=round(_round_up(float(np.percentile(s, pct)), 0.05), 2),
                   recovery_at_pass_bar=dict(p25=round(float(np.percentile(rfs, 25)), 2),
                                             p50=round(float(np.percentile(rfs, 50)), 2),
                                             share_at_least_3=round(float(np.mean(np.array(rfs) >= 3)), 2)),
                   clustered_share=round(clustered / len(shares), 2), judged_cells=len(shares), per_cell=per_cell)
    return out


def active_live_limits(research):
    """{cell key: live suspension limit in R} for the risk engine - ONLY when the research run judged by the family
    table (mode active). In shadow mode: {} (the risk engine keeps risk.strategy_max_dd_r for every strategy)."""
    fgs = (research or {}).get("family_gates") or {}
    if fgs.get("mode") != "active":
        return {}
    return {k: float(v["live_r"]) for k, v in (fgs.get("live_limits") or {}).items() if v and v.get("live_r")}


# ---------------------------------------------------------------- report ----------------------------------------

def report_lines(research):
    """reports/latest.md section 3b: the shadow table (old verdict vs new verdict per cell) - markdown lines."""
    fg = (research or {}).get("family_gates")
    if not fg:
        return []
    cells = (research or {}).get("cells") or {}
    L = [f"**Family gates (Phase 19 A, rules v{fg.get('rules_version')}) - {fg.get('mode_text')}.** The single "
         f"max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts "
         f"side by side; until you say yes after the shadow period, only the OLD verdict moves anything.\n"]
    ch = [(k, c) for k, c in sorted(cells.items()) if (c.get("family_gate") or {}).get("changed")]
    L.append(f"{len(ch)} of {len(cells)} strategy / timeframe tests would get a different verdict.\n")
    if ch:
        L.append("| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | "
                 "Why (new rule) |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for k, c in ch:
            f = c["family_gate"]
            m = f["metrics"]
            w, d = m.get("window") or {}, m.get("duration") or {}
            L.append(f"| {c['strategy']} v{c['version']} | {c['tf']} | {f['group']} | {f['old']} | **{f['new']}** | "
                     f"{'-' if m.get('recovery') is None else m['recovery']} | {w.get('dd95_r', '-')}R | "
                     f"{d.get('days', 0):.0f} d ({d.get('share', 0) * 100:.0f}%) | "
                     f"{'; '.join(f['new_reasons'][:3]) or 'passes every gate'} |")
        L.append("")
    return L
