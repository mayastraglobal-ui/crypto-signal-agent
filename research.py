#!/usr/bin/env python3
"""
Daily research run (AGENT_PROMPT.md sections 11 and 12) - Phase 8.

For every strategy version x timeframe, on the research coins of the last hourly scan:
  Layer B   - the longest history available (develop = first 70%, validate = last 30% of each coin)
  Layer C   - walk-forward: the history cut into equal time windows, judged one after the other
  costs     - cost viability (stop >= 4x the round-trip cost) and a stress test with costs +50%
  +-20%     - every parameter moved down and up, one at a time
  coins     - edge on >= 3 coins; overfitting flag; control-twin comparison
Then every version x timeframe moves along its lifecycle (BACKTESTING / VALIDATION / FAILED /
PAPER_TRADING / RETIRED). APPROVED is never set by the engine - it needs the operator's yes.

It uses exactly the same engine as the hourly scan (scanner.prepare_coin / strategy_signals / backtest).
It never places trades.

Run:  python research.py            (live data; long history cached in data/history)
      python research.py --offline  (synthetic data, for testing the code)
"""
import argparse
import copy
import datetime as dt
import json
import os
import sys
import time

import numpy as np
import pandas as pd
import yaml

import scanner as sc
from engine import data_quality as dq
from engine import history
from engine import lifecycle as lc
from engine import regime as rg
from engine import research as rs
from engine import strategy_spec as sspec

CACHE = os.path.join(sc.ROOT, "data", "history")
log = sc.log


def stressed(cfg, x):
    """The config with fees, slippage and funding multiplied by x (costs +50% = 1.5)."""
    c = copy.deepcopy(cfg)
    for side in ("long", "short"):
        for k in ("taker_fee_pct", "maker_fee_pct", "slippage_pct", "funding_pct_per_8h"):
            if k in c["costs"][side]:
                c["costs"][side][k] *= x
    return c


def research_coins(offline, limit):
    """Signal + research-only coins chosen by the newest hourly scan (reports/universe.json)."""
    path = os.path.join(sc.REPORTS, "universe.json")
    coins = []
    if os.path.exists(path):
        u = json.load(open(path))
        coins = list(u.get("signal", [])) + list(u.get("research_only", []))
    if not coins and offline:
        coins = ["BTC", "ETH", "SOL", "BNB"]
    if not coins:
        sys.exit("No coins: reports/universe.json is missing - the hourly scan must run first.")
    return coins[:limit] if limit else coins


def load_registry(offline):
    path = os.path.join(sc.REPORTS, "strategy_registry_offline.csv") if offline else sc.REGISTRY
    src = path if os.path.exists(path) else sc.REGISTRY
    reg = (lc.registry_from_frame(pd.read_csv(src, dtype={"version": str}))
           if os.path.exists(src) else lc.empty_registry())
    return reg, path


def paper_results(logdf):
    """Closed PAPER signals per (strategy, version, tf), oldest first."""
    out = {}
    if logdf.empty:
        return out
    d = logdf[(logdf["stage"] == "PAPER_TRADING") & (logdf["status"] != "OPEN")].dropna(subset=["result_r"]).copy()
    d["version"] = d["version"].fillna("1.0").astype(str)
    for (s, v, tf), g in d.sort_values("closed_time_utc").groupby(["strategy", "version", "tf"]):
        out[(s, v, tf)] = g["result_r"].astype(float).tolist()
    return out


def fmt_day(ms):
    return pd.to_datetime(int(ms), unit="ms").strftime("%Y-%m-%d")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="use synthetic data (code test)")
    ap.add_argument("--coins", type=int, default=None, help="only the first N research coins (test runs)")
    args = ap.parse_args()

    t_start = time.time()
    cfg = yaml.safe_load(open(os.path.join(sc.ROOT, "config.yaml")))
    R, V = cfg["research"], cfg["validation"]
    started = dt.datetime.now(dt.timezone.utc)
    now_ms = int(started.timestamp() * 1000)
    now_txt = started.strftime("%Y-%m-%d %H:%M")
    dq_cfg = dq.settings(cfg.get("data_quality"))
    tfs = [tf for tf in sc.TF_ORDER if tf in cfg["timeframes"]]

    strategies, problems, _ = sspec.load(yaml.safe_load(open(os.path.join(sc.ROOT, "strategies.yaml"))),
                                         rg.LABELS, sc.TF_ORDER)
    registry, reg_path = load_registry(args.offline)
    fps = {sspec.key(x): sspec.fingerprint(x) for x in strategies}
    for x in list(strategies):
        msg = lc.immutable_problem(registry, x, fps[sspec.key(x)])
        if msg:
            problems.setdefault(x["id"], []).append(msg)
            strategies.remove(x)
    by_key = {sspec.key(x): x for x in strategies}
    variants = {k: sspec.variants(x, R["perturb_pct"]) for k, x in by_key.items()}

    feed = sc.Synthetic() if args.offline else sc.Binance()     # long history only from the main exchange
    cache = None if args.offline else CACHE
    bars = {tf: (min(int(R["history_bars"][tf]), int(R["offline_history_bars"])) if args.offline
                 else int(R["history_bars"][tf])) for tf in ["1w", "1d"] + tfs}
    cfg_stress = stressed(cfg, R["cost_stress_x"])
    coins = research_coins(args.offline, args.coins)
    log(f"Research run: {len(coins)} coins ({', '.join(coins)}), {len(strategies)} strategy versions, "
        f"{sum(len(v) for v in variants.values())} ±{R['perturb_pct']}% variants")

    per, stress, var = {}, {}, {}            # (id, version, tf) -> {coin: trades} (var: -> {label: {coin: ...}})
    spans, hist, skipped, rule_errors = {}, {}, {}, {}
    for base in coins:
        sym = base + cfg["market"]["quote"]
        data, quality = {}, {}
        try:
            for tf in ["1w", "1d"] + tfs:
                raw, how = history.update(feed, sym, tf, bars[tf], now_ms, cache)
                df, rep = dq.check_candles(raw, sc.TF_MS[tf], now_ms, dq_cfg)
                data[(sym, tf)], quality[(base, tf)] = df, rep
                log(f"{sym} {tf}: {len(df)} candles ({how}), data {rep['state']}"
                    + (f" - {'; '.join(rep['problems'])}" if rep["problems"] else ""))
        except Exception as e:
            log(f"skip {sym}: {e}")
            skipped[base] = f"download failed: {e}"
            continue
        pc = sc.prepare_coin(sym, base, data, quality, tfs, cfg)
        for tf in tfs:
            if tf not in pc["frames"]:
                skipped.setdefault(base, "")
                skipped[base] += f"{tf} not researched (data {quality[(base, tf)]['state']}); "
        for tf, fr in pc["frames"].items():
            df, n = fr["df"], fr["n"]
            hist.setdefault(tf, {})[base] = (int(df["open_time"].iloc[0]), int(df["close_time"].iloc[-1]), n)
            spans.setdefault(tf, []).append((int(df["open_time"].iloc[min(250, n - 1)]), int(df["close_time"].iloc[-1])))
            for s in strategies:
                if tf not in s["timeframes"]:
                    continue
                k3 = (s["id"], s["version"], tf)
                try:
                    L, S, XL, XS, cols = sc.strategy_signals(s, tf, fr, cfg)
                except Exception as e:
                    log(f"RULE ERROR in {s['id']} {tf}: {e}")
                    rule_errors.setdefault(sspec.key(s), set()).add(f"{tf}: {e}")
                    continue
                for cf, store in ((cfg, per), (cfg_stress, stress)):
                    tr = sc.backtest(df, L, S, XL, XS, s, cf, tf, cols)
                    sc.mark_oos(tr, n, cfg)
                    store.setdefault(k3, {})[base] = tr
                for label, v, rules_changed in variants[sspec.key(s)]:
                    sig = (L, S, XL, XS, cols)
                    if rules_changed:
                        try:
                            sig = sc.strategy_signals(v, tf, fr, cfg)
                        except Exception as e:
                            rule_errors.setdefault(sspec.key(s), set()).add(f"{tf} variant {label}: {e}")
                            sig = (np.zeros(n, bool), np.zeros(n, bool), None, None, cols)
                    tv = sc.backtest(df, *sig[:4], v, cfg, tf, sig[4])
                    # only the count and the total R are kept (all trades of 160+ variants would not fit in memory)
                    var.setdefault(k3, {}).setdefault(label, {})[base] = (len(tv), float(sum(t["r"] for t in tv)))
        log(f"researched {sym}")
        del pc, data

    # ---------- evidence per strategy version x timeframe ----------
    wins = {tf: rs.windows(min(a for a, _ in sp), max(b for _, b in sp), int(R["walk_forward_windows"]))
            for tf, sp in spans.items()}
    evals = {k3: rs.evaluate(per[k3], stress.get(k3, {}), var.get(k3, {}), wins[k3[2]], R, V["min_coin_trades"])
             for k3 in per}
    logdf = sc.load_log()
    fwd = sc.forward_stats(logdf)
    paper = paper_results(logdf)

    # ---------- lifecycle ----------
    results, cells = {}, {}
    for k3, ev in evals.items():
        sid, ver, tf = k3
        s = by_key[f"{sid}@{ver}"]
        raw = ev.pop("_raw")
        base_status, reasons, need = lc.judge(raw["st"], raw["dev"], raw["val"], fwd.get(k3), V,
                                              lc.retune_penalty(registry, s, V["retune_penalty_r"]),
                                              ev["median_cost_r"])
        twin = None
        if s.get("control_twin"):
            twin = next((e for k, e in evals.items() if k[0] == s["control_twin"] and k[2] == tf), None)
        paper_ok, paper_reasons = lc.paper_gate(base_status, ev, twin, R)
        if s.get("control_twin") and twin is None:
            paper_ok, paper_reasons = False, paper_reasons + ["control twin was not tested"]
        ck = f"{sid}@{ver}|{tf}"
        prev = registry["cells"].get(ck, {})
        rec = lc.paper_record(paper.get(k3, []))
        status, note, failed = lc.next_status(prev.get("status"), base_status, paper_ok, rec,
                                              int(prev.get("failed_runs") or 0), R)
        results[k3] = status
        cells[ck] = dict(strategy=sid, version=ver, tf=tf, status=status, base_status=base_status,
                         reasons=reasons, paper_gate_failed=paper_reasons if base_status == "VALIDATION" else [],
                         note=note, failed_runs=failed, required_avg_r=round(need, 3),
                         beats_twin=lc.twin_compare(ev, twin, R) if twin else None,
                         history_from=fmt_day(min(t["entry_time"] for tr in per[k3].values() for t in tr))
                         if any(per[k3].values()) else None,
                         paper=rec, evidence=ev)

    tested = [x for x in strategies if any(k[0] == x["id"] and k[1] == x["version"] for k in per)]
    registry, new_exp, changes = lc.update(registry, tested, fps, results, now_txt)
    for c in changes:
        cell = cells[f"{c['key']}|{c['tf']}"]
        c["why"] = cell["note"] or "; ".join(cell["reasons"] + cell["paper_gate_failed"])
    for ck, c in cells.items():
        ev, wf = c["evidence"], c["evidence"]["walk_forward"]
        registry["cells"][ck].update(
            trades=ev["all"]["n"], avg_r=ev["all"]["avg_r"], profit_factor=ev["all"]["pf"],
            max_dd_r=ev["all"]["max_dd_r"], train_avg_r=ev["develop"]["avg_r"], test_avg_r=ev["validate"]["avg_r"],
            required_avg_r=c["required_avg_r"], beats_twin=c["beats_twin"],
            gates_failed="; ".join(c["reasons"]), history_from=c["history_from"],
            walk_forward=f"{wf['positive']}/{wf['judged']}", stress_avg_r=ev["stress"]["avg_r"],
            perturb_worst=(f"{ev['perturbation']['worst']['change']}: {ev['perturbation']['worst']['avg_r']:+.3f}R"
                           if ev["perturbation"]["worst"] else None),
            positive_coins=len(ev["positive_coins"]), median_cost_r=ev["median_cost_r"],
            overfit="; ".join(ev["overfit"]) or None, paper_gate_failed="; ".join(c["paper_gate_failed"]) or None,
            paper_signals=c["paper"]["n"], failed_runs=c["failed_runs"])
    os.makedirs(os.path.dirname(reg_path), exist_ok=True)
    lc.registry_to_frame(registry).to_csv(reg_path, index=False)
    if not args.offline:
        sc.write_experiments(new_exp, registry)
        sc.write_lifecycle_log(changes, started)

    # ---------- report ----------
    history_out = {}
    for tf, h in hist.items():
        a, b = min(x[0] for x in h.values()), max(x[1] for x in h.values())
        years = (b - a) / (365 * rs.DAY_MS)
        history_out[tf] = dict(coins=len(h), **{"from": fmt_day(a), "to": fmt_day(b)},
                               bars=max(x[2] for x in h.values()),
                               note="" if years >= 2 else f"only {years:.1f} years - may miss a full bull/bear cycle")
    out = dict(run_utc=now_txt, duration_s=round(time.time() - t_start), data_source=feed.name, coins=coins,
               skipped=skipped, history=history_out, settings=R, changes=changes,
               not_run={k: v for k, v in problems.items()}, rule_errors={k: sorted(v) for k, v in rule_errors.items()},
               walk_forward_windows={tf: [dict(start=fmt_day(a), end=fmt_day(b)) for a, b in w] for tf, w in wins.items()},
               cells=cells)
    path = os.path.join(sc.REPORTS, "research_offline.json" if args.offline else "research.json")
    json.dump(out, open(path, "w"), indent=1, default=float)
    n_status = pd.Series(list(results.values())).value_counts().to_dict() if results else {}
    log(f"Research done in {out['duration_s']} s: {len(cells)} strategy/timeframe cells - {n_status}")


if __name__ == "__main__":
    main()
