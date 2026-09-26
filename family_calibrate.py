#!/usr/bin/env python3
"""
Phase 19 A: calibrate the family table (config.yaml -> family_gates) from history, and show which cards would change
verdict. Research only - it never edits config.yaml, never moves a strategy.

Input: the research run's per-trade results as published for the dashboard (branch gh-pages, folder charts/t: one file
per strategy version x timeframe x coin, every trade with its result in R) and, for the verdict table, the research
run's evidence (branch live-reports, reports/research.json).

  git fetch origin gh-pages live-reports
  mkdir -p /tmp/fg && git archive origin/gh-pages charts | tar x -C /tmp/fg
  git show origin/live-reports:reports/research.json > /tmp/fg/research.json
  python family_calibrate.py --trades /tmp/fg/charts/t --research /tmp/fg/research.json

The method is engine/family_gates.calibrate() - fixed before any verdict is looked at. The limits it prints are copied
into config.yaml by the operator's pull request (a new rules_version if they ever change), and every card is then
re-evaluated under them (one extra row per cell in memory/trials.csv).
"""
import argparse
import copy
import glob
import json
import os
import sys

import pandas as pd
import yaml

from engine import family_gates as fg
from engine import lifecycle as lc
from engine import trials as trl

ROOT = os.path.dirname(os.path.abspath(__file__))


def load_trades(folder):
    """{cell key: (r list, entry-time ms list)} from the chart trade files (all coins of a cell pooled)."""
    cells = {}
    for p in sorted(glob.glob(os.path.join(folder, "*.json"))):
        with open(p) as f:
            d = json.load(f)
        if len(d.get("trades") or []) != d.get("n"):
            sys.exit(f"{p}: the file keeps only the newest {len(d['trades'])} of {d['n']} trades - cannot calibrate")
        r, t = cells.setdefault(d["key"], ([], []))
        for x in d["trades"]:
            r.append(float(x["r"]))
            t.append(int(x["et"]) * 1000)
    return cells


def families():
    df = pd.read_csv(os.path.join(ROOT, "memory", "strategy_registry.csv"), dtype={"version": str})
    return {f"{r.id}@{r.version}": r.family for r in df.itertuples()}


def as_trades(r, t):
    return [dict(r=a, entry_time=b) for a, b in zip(r, t)]


def old_and_new(research, trades, fam, FG, cfg):
    """The verdict each cell of the last research run gets under the OLD rules and under the family table, with
    the trials bar AFTER the re-evaluation rows are counted (the same as research.py will do)."""
    V, R = cfg["validation"], cfg["research"]
    n_trials = research["trials"]["total"]
    n_after = n_trials + len(research["cells"])                  # one re-evaluation row per cell
    bar_after = (trl.need_t(n_after, R["trials_alpha"]), n_after)
    mc_limit = min(float(R["monte_carlo_max_dd_r"]), float(cfg["risk"]["strategy_max_dd_r"]))
    checked = set(((research.get("robustness") or {}).get("bias") or {}).get("checked") or {})
    cards = {}
    for f in ("strategies.yaml", "strategies_lab.yaml"):
        path = os.path.join(ROOT, f)
        if os.path.exists(path):
            for x in yaml.safe_load(open(path)) or []:
                if isinstance(x, dict) and "id" in x:
                    cards[f"{x['id']}@{x.get('version')}"] = x
    rows = []
    for ck, c in sorted(research["cells"].items()):
        ev = copy.deepcopy(c["evidence"])
        st = lambda s: dict(n=s["n"], exp_r=s["avg_r"], pf=s["pf"], max_dd_r=s["max_dd_r"])
        a, dv, vl = st(ev["all"]), st(ev["develop"]), st(ev["validate"])
        need = c["required_avg_r"] - V["min_expectancy_r"]
        spec = cards.get(ck.split("|")[0]) or {}
        has_twin = bool(spec.get("control_twin") or spec.get("confirm_5m"))
        bias_checked = ck.split("|")[0] in checked
        old_b, _, _ = lc.judge(a, dv, vl, None, V, need, ev["median_cost_r"])
        old_ok, old_why = lc.paper_gate(old_b, ev, None, R, (trl.need_t(n_trials, R["trials_alpha"]), n_trials),
                                        mc_limit, bias_checked)
        g = fg.group_of(fam.get(ck.split("|")[0]), FG)
        r, t = trades.get(ck, ([], []))
        m = fg.measure(as_trades(r, t), FG)
        new_b, new_why, _ = lc.judge(a, dv, vl, None, V, need, ev["median_cost_r"],
                                     dd_checks=fg.dd_reasons(m, g, FG, V))
        new_ok, new_pwhy = lc.paper_gate(new_b, ev, None, R, bar_after,
                                         mc_limit if fg.uses_whole_history_mc(g, FG) else None, bias_checked)
        if has_twin and c.get("beats_twin") is not True:
            old_ok = new_ok = False
            old_why, new_pwhy = old_why + ["control twin"], new_pwhy + ["control twin"]
        if c.get("bias"):
            old_ok = new_ok = False
        old_v = "FAILED" if c.get("bias") else fg.verdict(old_b, old_ok)
        new_v = "FAILED" if c.get("bias") else fg.verdict(new_b, new_ok)
        rows.append(dict(cell=ck, group=g, family=fam.get(ck.split("|")[0]), old=old_v, new=new_v, metrics=m,
                         new_reasons=[x for x in new_why if x] + (new_pwhy if new_b == "VALIDATION" else []),
                         limits=fg.live_limit(m, g, FG, cfg["risk"]["strategy_max_dd_r"], R["paper_max_dd_r"])))
    return rows, bar_after


def robustness(trades, fam, FG, V, group):
    """Leave-one-out (each cell removed in turn) and other random seeds: how much the limits move."""
    cells = {k: v for k, v in trades.items() if fg.group_of(fam.get(k.split("|")[0]), FG) == group}
    loo = {k: fg.calibrate({a: b for a, b in cells.items() if a != k}, V["min_expectancy_r"], V["min_trades"],
                           int(FG["window_trades"]), pct=FG["reference_percentile"]) for k in sorted(cells)}
    seeds = [fg.calibrate(cells, V["min_expectancy_r"], V["min_trades"], int(FG["window_trades"]),
                          pct=FG["reference_percentile"], seed=x)["dd_per_100"]["p95"] for x in (1, 2, 3, 4, 5)]
    return dict(loo_dd=[min(x["max_mc_dd95_per_100_r"] for x in loo.values()),
                        max(x["max_mc_dd95_per_100_r"] for x in loo.values())],
                loo_share=[min(x["max_dd_duration_share"] for x in loo.values()),
                           max(x["max_dd_duration_share"] for x in loo.values())],
                loo=loo, seeds_p95=seeds)


def fmt_pct(x):
    return "-" if x is None else f"{x * 100:.0f}%"


def render(out, run_utc, FG, V):
    """memory/family_gates_calibration.md - how each number of the family table was chosen."""
    L = ["# Family gates - calibration (Phase 19 A)", "",
         f"Rules version {FG['rules_version']}. Written by `family_calibrate.py` from the research run of {run_utc} UTC "
         "(per-trade results: branch gh-pages `charts/t`; evidence: branch live-reports `reports/research.json`). "
         "Research only - no fee, risk-per-trade or trials-bar change.", "",
         "## 1. The method (fixed before any card's verdict was computed)", "",
         "- **Groups** (by the card's `family`): trend = trend_following, momentum, breakout, mtf_pullback; tight = "
         "mean_reversion, liquidity_reversal, smc, price_action and any family not listed.",
         "- **Reference** = every historical trade of every card of the group (all timeframes, all coins, the whole "
         f"tested history), with the average moved to the pass bar (+{V['min_expectancy_r']:.2f}R). It is \"a strategy of "
         "this family with exactly the minimum acceptable edge\": the family's real spread of wins and losses, no "
         "better and no worse an edge. No card is fitted: the losing cards count as much as the winning ones.",
         f"- **Every limit = the {FG['reference_percentile']}th percentile of the reference** (the same 95% the engine "
         "already uses for Monte Carlo), rounded UP (0.5R, 0.05).",
         f"  - `max_mc_dd95_per_100_r`: 20,000 random sequences of {FG['window_trades']} reference trades -> their "
         "worst drawdown -> the 95th percentile.",
         "  - `max_dd_duration_share`: every group cell with >= 30 trades, its OWN time-ordered trades moved to the "
         "pass bar (keeps its real bunching of losses in time) -> longest time below a previous peak as a share of its "
         "tested period -> the 95th percentile over the cells.",
         "  - `min_recovery_factor: 3` is the operator's number; below is what it means for a pass-bar strategy.",
         "  - loss clustering (tight group): the real longest losing streak must not exceed the 95th percentile of "
         "1,000 random orders of the same trades.",
         "- A card is then measured the same way on its own trades: Monte Carlo 95% worst drawdown of 100 trades drawn "
         "from ITS trades (does not grow with the number of trades), its longest drawdown in days / share, its "
         "recovery factor.", ""]
    for g, c in out["groups"].items():
        rb = out["robustness"].get(g) or {}
        L += [f"## 2{'ab'[list(out['groups']).index(g)]}. {g} group", "",
              f"- {c['cells']} cells, {c['trades']:,} trades; raw average {c.get('raw_avg_r', 0):+.3f}R, spread "
              f"(sd) {c.get('sd_r', 0):.2f}R, win rate {c.get('win_rate', 0) * 100:.0f}% -> moved to "
              f"+{c['pass_bar_r']:.2f}R",
              f"- worst drawdown in 100 trades of the reference: median {c['dd_per_100']['p50']}R · 75% "
              f"{c['dd_per_100']['p75']}R · 90% {c['dd_per_100']['p90']}R · **95% {c['dd_per_100']['p95']}R** · 99% "
              f"{c['dd_per_100']['p99']}R",
              f"  -> `{g} max_mc_dd95_per_100_r: {c['max_mc_dd95_per_100_r']}`"
              + ("" if g == "trend" else " (computed, not used: the tight group keeps 10R / 8R)"),
              f"- longest drawdown as a share of the tested period ({c.get('judged_cells')} cells with >= 30 trades, "
              f"each at the pass bar): median {fmt_pct(c['duration_share']['p50'])} · 75% "
              f"{fmt_pct(c['duration_share']['p75'])} · **95% {fmt_pct(c['duration_share']['p95'])}** · max "
              f"{fmt_pct(c['duration_share']['max'])}",
              f"  -> `{g} max_dd_duration_share: {c['max_dd_duration_share']}`",
              f"- recovery factor of those cells at the pass bar: 25% {c['recovery_at_pass_bar']['p25']} · median "
              f"{c['recovery_at_pass_bar']['p50']} · {fmt_pct(c['recovery_at_pass_bar']['share_at_least_3'])} reach 3 "
              "- so RF >= 3 asks for MORE than the minimum edge (or a long, steady record)",
              f"- real histories with clustered losses (streak above 95% of random orders): "
              f"{fmt_pct(c['clustered_share'])} of the cells",
              f"- robustness: leaving out one cell at a time gives {rb.get('loo_dd')}R and "
              f"{rb.get('loo_share')} (duration); other random seeds give 95% = "
              f"{', '.join(f'{x:.2f}' for x in rb.get('seeds_p95') or [])}R - the limit used is the stricter end", "",
              "| Cell (moved to the pass bar) | Trades | Moved by | Longest DD | Share | RF | Real streak / 95% random |",
              "|---|---|---|---|---|---|---|"]
        L += [f"| {k.replace('|', ' ')} | {v['n']} | {v['shifted_by_r']:+.3f}R | {v['dd_days']:.0f} d | {fmt_pct(v['dd_share'])} | "
              f"{v['recovery']} | {v['real_streak']} / {v['streak95']} |" for k, v in c.get("per_cell", {}).items()]
        L.append("")
    if out.get("verdicts"):
        tb = out["trials_bar_after"]
        L += ["## 3. Old vs new verdict of every cell (the same research run)", "",
              f"Trials bar after the re-evaluation rows ({tb['trials']} trials): t >= {tb['need_t']}. The new verdict "
              "is SHOWN only (shadow mode) - nothing moves on it until the operator's yes after the shadow period.", "",
              "| Cell | Group | Old | New | Trades | RF | 95% DD / 100 | Longest DD | Live / paper limit | New rule: why not |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for r in out["verdicts"]:
            m = r["metrics"]
            w, d = m.get("window") or {}, m.get("duration") or {}
            L.append(f"| {r['cell'].replace('|', ' ')} | {r['group']} | {r['old']} | {'**' + r['new'] + '**' if r['new'] != r['old'] else r['new']} "
                     f"| {m['n']} | {'-' if m.get('recovery') is None else m['recovery']} | {w.get('dd95_r', '-')}R | "
                     f"{d.get('days', 0):.0f} d ({fmt_pct(d.get('share'))}) | {r['limits']['live_r']:g}R | "
                     f"{'; '.join(r['new_reasons'][:2]) or 'passes every gate'} |")
        L.append("")
    return "\n".join(L) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--trades", required=True, help="folder of chart trade files (gh-pages charts/t)")
    p.add_argument("--research", help="research.json of the same run (live-reports) - for the verdict table")
    p.add_argument("--json", help="write the calibration + verdicts here as JSON")
    p.add_argument("--doc", help="write the calibration record (markdown) here, e.g. memory/family_gates_calibration.md")
    a = p.parse_args()
    cfg = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
    FG = fg.settings(cfg.get("family_gates"))
    V = cfg["validation"]
    trades, fam = load_trades(a.trades), families()
    out = dict(groups={})
    for g, row in FG["groups"].items():
        cells = {k: v for k, v in trades.items() if fg.group_of(fam.get(k.split("|")[0]), FG) == g}
        out["groups"][g] = fg.calibrate(cells, V["min_expectancy_r"], V["min_trades"],
                                        int(FG["window_trades"]), pct=FG["reference_percentile"])
        c = out["groups"][g]
        print(f"[{g}] {c['cells']} cells, {c['trades']} trades: max_mc_dd95_per_100_r = "
              f"{c.get('max_mc_dd95_per_100_r')}, max_dd_duration_share = {c.get('max_dd_duration_share')}")
    out["robustness"] = {g: robustness(trades, fam, FG, V, g) for g in FG["groups"]}
    research = json.load(open(a.research)) if a.research else {}
    if a.research:
        rows, bar = old_and_new(research, trades, fam, FG, cfg)
        out["verdicts"], out["trials_bar_after"] = rows, dict(need_t=round(bar[0], 3), trials=bar[1])
        for r in rows:
            if r["old"] != r["new"]:
                print(f"CHANGES: {r['cell']} ({r['group']}): {r['old']} -> {r['new']}")
    if a.json:
        with open(a.json, "w") as f:
            json.dump(out, f, indent=1, default=float)
    if a.doc:
        with open(a.doc, "w") as f:
            f.write(render(out, research.get("run_utc", "-"), FG, V))


if __name__ == "__main__":
    main()
