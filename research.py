#!/usr/bin/env python3
"""
Daily research run (AGENT_PROMPT.md sections 11 and 12) - Phase 8.

For every strategy version x timeframe, on the research coins of the last hourly scan:
  Layer B   - the longest history available (develop = first 70%, validate = last 30% of each coin)
  Layer C   - walk-forward: the history cut into equal time windows, judged one after the other
  costs     - cost viability (stop >= 4x the round-trip cost) and a stress test with costs +50%
  +-20%     - every parameter moved down and up, one at a time
  coins     - edge on >= 3 coins; overfitting flag; control-twin comparison
  5m check  - strategies with confirm_5m (section 8) are backtested through the 5-minute protocol; their
              control twin is the SAME strategy without the check, run over the same period on the same
              5m bars (a fair comparison - Phase 10)
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

import pine_export
import scanner as sc
from engine import approval as ap
from engine import attribution as att
from engine import confirm5m as c5m
from engine import data_quality as dq
from engine import history
from engine import lifecycle as lc
from engine import playbook as pbk
from engine import regime as rg
from engine import memory as mem
from engine import research as rs
from engine import strategy_spec as sspec
from engine import trials as trl

CACHE = os.path.join(sc.ROOT, "data", "history")
TRIALS = os.path.join(sc.MEMORY, "trials.csv")
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


def update_trials(registry, tested, now_txt, offline):
    """Phase 17: memory/trials.csv gets one row per strategy version x timeframe the first time it is tested (the
    file only grows). Created from the registry the first time. Offline runs write reports/trials_offline.csv.
    tested: [(id, version, tf, origin)]. Returns (all rows, rows added this run)."""
    path = os.path.join(sc.REPORTS, "trials_offline.csv") if offline else TRIALS
    src = path if os.path.exists(path) else TRIALS
    text = ""
    if os.path.exists(src):
        with open(src) as f:
            text = f.read()
    rows = trl.parse(text)
    head = not rows
    if not rows:
        rows = trl.number(trl.backfill(registry), 0)
    new = trl.additions(rows, tested, now_txt)
    if head or new or src != path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if head or src != path:
            with open(path, "w") as f:
                f.write(trl.to_csv(rows + new, True))
        else:
            with open(path, "a") as f:
                f.write(("" if text.endswith("\n") else "\n") + trl.to_csv(new, False))
    return rows + new, new


def paper_results(logdf):
    """Closed PAPER signals per (strategy, version, tf), oldest first - followed by its live (APPROVED) signals,
    so the retirement limits keep watching a version after the operator's yes (section 12)."""
    out = {}
    if logdf.empty:
        return out
    d = logdf[logdf["stage"].isin(["PAPER_TRADING", "APPROVED"]) & (logdf["status"] != "OPEN")].dropna(subset=["result_r"]).copy()
    d["version"] = d["version"].fillna("1.0").astype(str)
    for (s, v, tf), g in d.sort_values("closed_time_utc").groupby(["strategy", "version", "tf"]):
        out[(s, v, tf)] = g["result_r"].astype(float).tolist()
    return out


def move_findings(moves, s, tf, fr, detail, L, S, cols, cfg, A, found):
    """Section 17.4: what this strategy on this timeframe did around each strong move of the coin."""
    df, n = fr["df"], fr["n"]
    ct, o, c, atr = (df["close_time"].to_numpy(), df["open"].to_numpy(), df["close"].to_numpy(),
                     df["_atr"].to_numpy())
    for m in moves:
        a = m["start_ms"] - int(A["signal_window_bars"]) * 3_600_000
        idx = np.flatnonzero((ct >= a) & (ct < m["start_ms"] + 3_600_000))
        fin_l, fin_s = L.copy(), S.copy()
        for t in idx:                    # a gated signal only counts if it had a valid stop and target
            for d, arr in ((1, fin_l), (-1, fin_s)):
                if arr[t] and sc.plan_trade(s, t, d, o[t + 1] if t + 1 < n else c[t], atr[t], cols, cfg) is None:
                    arr[t] = False
        found.setdefault(m["key"], {})[f"{s['id']} v{s['version']} {tf}"] = att.check_move(
            m, ct, detail["raw_l"], detail["raw_s"], detail["reg_ok"], detail["perm_l"], detail["perm_s"],
            fin_l, fin_s, A)


def fmt_day(ms):
    return pd.to_datetime(int(ms), unit="ms").strftime("%Y-%m-%d")


def write_missed(missed, when, A, days=7):
    """memory/missed_trades.md (section 17.4): strong moves of the last day and whether they were
    identifiable beforehand - one section 22 record per move. Append-only; nothing on a day without strong moves."""
    for m in missed:
        mem.append(sc.MEMORY, "missed_trades.md", mem.record(
            f"{m['coin']} {m['direction']} {m['pct']:+.1f}% ({m['size_atr']}x ATR), {m['start_utc']} -> {m['end_utc']}",
            [f"- verdict: {m['verdict']}" + ("" if m["signal_coin"] else " (research-only coin)")]
            + [f"- {k}: {v}" for k, v in m["findings"].items()],
            timestamp=when.strftime("%Y-%m-%d %H:%M UTC"), source="engine: daily research run",
            evidence=f"FACT: move of {m['size_atr']}x the 1H ATR within {A['strong_move_bars']} hours; "
                     f"{m['strategies_checked']} strategy / timeframe tests checked",
            confidence="measured on closed candles", strategy="all", asset=m["coin"], timeframe="1h",
            regime=m.get("regime") or "-", review=mem.plus_days(when, days)))


def write_sources(strategies, when, days=90):
    """memory/research_sources.md (section 18): one record per strategy version, the first time it is tested
    (older versions are back-filled once). Only what the card says - a URL only if the card has `source_url`."""
    path = os.path.join(sc.MEMORY, "research_sources.md")
    have = ""
    if os.path.exists(path):
        with open(path) as f:
            have = f.read()
    for s in strategies:
        key = f"{s['id']}@{s['version']}"
        if f"### {key} " in have:
            continue
        # SMC / ICT ideas (and their -5M versions) are CLAIMs from that material; the older indicator strategies
        # and the control twins are our own HYPOTHESES (operator decision, Phase 13)
        cls = s.get("evidence_class") or ("CLAIM" if s["family"] == "smc" and not s.get("twin_of") else "HYPOTHESIS")
        text = mem.record(
            f"{key} - {s.get('description') or s['id']}",
            [f"- title / source: {s.get('source') or '-'}", f"- URL: {s.get('source_url') or 'none recorded'}",
             f"- claim: {s['hypothesis']}",
             f"- derived hypothesis (tested): {key} makes money after fees in regimes {', '.join(s['regimes'])} on "
             f"{', '.join(s['timeframes'])}" + (f", and beats its control twin {s['control_twin']}"
                                                  if s.get("control_twin") else ""),
             f"- limitations: {s.get('known_weaknesses') or '-'}",
             "- test results: `memory/strategy_registry.csv` / report section 3"],
            timestamp=when.strftime("%Y-%m-%d %H:%M UTC"),
            source=f"{sspec.LAB_FILE if s.get('lab') else sspec.LIBRARY_FILE} card {key}",
            evidence=cls + (": control twin - a benchmark, not an idea" if s.get("twin_of") else ": not tested when recorded"),
            confidence="untested idea", strategy=f"{s['id']} v{s['version']}", asset="research coins",
            timeframe=", ".join(s["timeframes"]), regime=", ".join(s["regimes"]), review=mem.plus_days(when, days))
        mem.append(sc.MEMORY, "research_sources.md", text)
        have += text


def approval_step(ck, status, note, rec, ev, approvals, AP, warnings, eligible_cells, lab=False):
    """Section 12: after the automatic lifecycle move, the operator's approvals list (config.yaml) is applied.
    Collects the cells that meet the numbers (for the packs) and the approvals that could not be applied.
    lab: a strategies_lab.yaml card - never APPROVED (Phase 17)."""
    ok, why_not = ap.eligible(status, rec, ev["validate"]["avg_r"] if ev["validate"]["n"] else None, AP)
    new_status, ap_note, warn = ap.decide(status, approvals.get(ck), ok, why_not, lab)
    if warn:
        warnings.append(f"{ck}: {warn}")
    if ok and new_status == "PAPER_TRADING":
        eligible_cells.append(ck)
    return (new_status, ap_note) if new_status != status else (status, note)


def export_approved(cells, per, by_key, cfg, now_txt, folder):
    """Phase 15: every APPROVED version x timeframe as a TradingView Pine script, with the engine's research
    trades embedded. A failed export is reported, never fatal."""
    out = []
    for ck, c in sorted(cells.items()):
        if c["status"] != "APPROVED":
            continue
        k3 = (c["strategy"], c["version"], c["tf"])
        try:
            path, info = pine_export.write(by_key[f"{k3[0]}@{k3[1]}"], k3[2], cfg, per.get(k3, {}), now_txt, folder,
                                           "research history of " + ", ".join(sorted(per.get(k3, {}))))
            out.append(dict(key=ck, file=os.path.relpath(path, sc.ROOT), mode=info["mode"]))
        except Exception as e:
            log(f"Pine export of {ck} failed: {e}")
            out.append(dict(key=ck, error=str(e)))
    return out


def write_packs(cells, eligible_cells, by_key, registry, AP, now_txt, offline):
    """Section 21: one approval pack per PAPER_TRADING version x timeframe that meets the section 12 numbers
    (reports/approval/). Packs of cells that are no longer eligible are removed (the report, not memory)."""
    folder = os.path.join(sc.REPORTS, "approval_offline" if offline else "approval")
    os.makedirs(folder, exist_ok=True)
    bpath = os.path.join(sc.REPORTS, "strategy_scoreboard.csv")
    board = pd.read_csv(bpath, dtype={"version": str}) if os.path.exists(bpath) else pd.DataFrame()
    out, keep = [], set()
    for ck in sorted(eligible_cells):
        c = cells[ck]
        spec = by_key[f"{c['strategy']}@{c['version']}"]
        lineage = [(v["version"], str(v.get("first_tested_utc") or "-")[:10],
                    (registry["cells"].get(f"{k}|{c['tf']}") or {}).get("status") or "not on this timeframe")
                   for k, v in sorted(registry["versions"].items(), key=lambda x: x[1]["experiment"])
                   if v["id"] == c["strategy"]]
        row = {}
        if not board.empty:
            m = board[(board["strategy"] == c["strategy"]) & (board["version"] == c["version"]) & (board["tf"] == c["tf"])]
            row = {k: (None if pd.isna(v) else v) for k, v in m.iloc[0].items()} if len(m) else {}
        name = ap.filename(c["strategy"], c["version"], c["tf"])
        with open(os.path.join(folder, name), "w") as f:
            f.write("\n".join(ap.pack(c, spec, lineage, row, AP, now_txt)) + "\n")
        keep.add(name)
        out.append(dict(key=ck, strategy=c["strategy"], version=c["version"], tf=c["tf"],
                        pack=f"reports/{os.path.basename(folder)}/{name}", paper_signals=c["paper"]["n"],
                        paper_avg_r=c["paper"]["avg_r"], backtest_validate_avg_r=c["evidence"]["validate"]["avg_r"]))
    for old in os.listdir(folder):
        if old.endswith(".md") and old not in keep:
            os.remove(os.path.join(folder, old))
    return out


def main():
    ap_ = argparse.ArgumentParser()
    ap_.add_argument("--offline", action="store_true", help="use synthetic data (code test)")
    ap_.add_argument("--coins", type=int, default=None, help="only the first N research coins (test runs)")
    args = ap_.parse_args()

    t_start = time.time()
    cfg = yaml.safe_load(open(os.path.join(sc.ROOT, "config.yaml")))
    R, V = cfg["research"], cfg["validation"]
    A = att.settings(cfg.get("attribution"))
    started = dt.datetime.now(dt.timezone.utc)
    now_ms = int(started.timestamp() * 1000)
    now_txt = started.strftime("%Y-%m-%d %H:%M")
    dq_cfg = dq.settings(cfg.get("data_quality"))
    tfs = [tf for tf in sc.TF_ORDER if tf in cfg["timeframes"]]

    strategies, problems, _, moved = sc.load_cards()          # strategies.yaml + strategies_lab.yaml (Phase 17)
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
    plain5 = {}                               # 5m-confirmed cells: the same signals WITHOUT the 5m check
    S5 = c5m.settings(cfg.get("confirm_5m"))
    spans, hist, skipped, rule_errors = {}, {}, {}, {}
    moves_all, move_found = [], {}           # missed-move learning (section 17.4)
    signal_coins = set(json.load(open(os.path.join(sc.REPORTS, "universe.json"))).get("signal", [])) \
        if os.path.exists(os.path.join(sc.REPORTS, "universe.json")) else set(coins)
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
        m5 = sc.m5_arrays(pc["frames"])
        moves = []
        if "1h" in pc["frames"]:
            f1 = pc["frames"]["1h"]
            moves = att.strong_moves(f1["df"], f1["df"]["_atr"].to_numpy(), now_ms, A)
            for m in moves:
                i0 = int(np.searchsorted(f1["df"]["close_time"].to_numpy(), m["start_ms"], side="right")) - 1
                m.update(coin=base, signal_coin=base in signal_coins, key=f"{base}|{m['start_ms']}|{m['dir']}",
                         regime=sc.regime_at(f1["reg"], "1h", i0) if i0 >= 0 else None)   # known before the move
            moves_all += moves
        for tf in tfs:
            if tf not in pc["frames"]:
                skipped.setdefault(base, "")
                skipped[base] += f"{tf} not researched (data {quality[(base, tf)]['state']}); "
        for tf, fr in pc["frames"].items():
            df, n = fr["df"], fr["n"]
            ctx = att.context(df, fr["feats"], fr["reg"], sc.TF_MS[tf])
            hist.setdefault(tf, {})[base] = (int(df["open_time"].iloc[0]), int(df["close_time"].iloc[-1]), n)
            spans.setdefault(tf, []).append((int(df["open_time"].iloc[min(250, n - 1)]), int(df["close_time"].iloc[-1])))
            for s in strategies:
                if tf not in s["timeframes"]:
                    continue
                k3 = (s["id"], s["version"], tf)
                detail = {}
                try:
                    L, S, XL, XS, cols = sc.strategy_signals(s, tf, fr, cfg, detail=detail)
                except Exception as e:
                    log(f"RULE ERROR in {s['id']} {tf}: {e}")
                    rule_errors.setdefault(sspec.key(s), set()).add(f"{tf}: {e}")
                    continue
                for cf, store in ((cfg, per), (cfg_stress, stress)):
                    tr = sc.run_backtest(df, L, S, XL, XS, s, cf, tf, cols, None, m5, S5)
                    sc.mark_oos_for(s, tr, n, cfg, m5)
                    store.setdefault(k3, {})[base] = tr
                if s.get("confirm_5m"):
                    tr = sc.backtest_5m(df, L, S, XL, XS, s, cfg, tf, cols, m5, False, None, S5)
                    sc.mark_oos_for(s, tr, n, cfg, m5)
                    plain5.setdefault(k3, {})[base] = tr
                for t in per[k3][base]:                    # section 17: why did each trade win or lose?
                    att.tag_trade(ctx, t, s, lc.regime_tf(tf), A)
                if moves:
                    move_findings(moves, s, tf, fr, detail, L, S, cols, cfg, A, move_found)
                for label, v, rules_changed in variants[sspec.key(s)]:
                    sig = (L, S, XL, XS, cols)
                    if rules_changed:
                        try:
                            sig = sc.strategy_signals(v, tf, fr, cfg)
                        except Exception as e:
                            rule_errors.setdefault(sspec.key(s), set()).add(f"{tf} variant {label}: {e}")
                            sig = (np.zeros(n, bool), np.zeros(n, bool), None, None, cols)
                    tv = sc.run_backtest(df, *sig[:4], v, cfg, tf, sig[4], None, m5, S5)
                    # only the count and the total R are kept (all trades of 160+ variants would not fit in memory)
                    var.setdefault(k3, {}).setdefault(label, {})[base] = (len(tv), float(sum(t["r"] for t in tv)))
        log(f"researched {sym}")
        del pc, data, m5

    # ---------- evidence per strategy version x timeframe ----------
    wins = {tf: rs.windows(min(a for a, _ in sp), max(b for _, b in sp), int(R["walk_forward_windows"]))
            for tf, sp in spans.items()}
    confirm_keys = {sspec.key(x) for x in strategies if x.get("confirm_5m")}

    def wins_for(k3):               # 5m-confirmed cells: walk-forward windows over the 5m period (their only data)
        return wins.get("5m", wins[k3[2]]) if f"{k3[0]}@{k3[1]}" in confirm_keys else wins[k3[2]]
    evals = {k3: rs.evaluate(per[k3], stress.get(k3, {}), var.get(k3, {}), wins_for(k3), R, V["min_coin_trades"])
             for k3 in per}
    logdf = sc.load_log()
    fwd = sc.forward_stats(logdf)
    paper = paper_results(logdf)
    AP = ap.settings(cfg.get("approval"))
    approvals, approval_problems = ap.parse_approvals(cfg.get("approvals"))
    approval_warnings, eligible_cells = [], []
    trial_rows, trial_new = update_trials(registry, [(k[0], k[1], k[2], "lab" if by_key[f"{k[0]}@{k[1]}"].get("lab")
                                                      else "library") for k in sorted(per)], now_txt, args.offline)
    alpha = float(R.get("trials_alpha", 0.05))
    trial_bar = (trl.need_t(len(trial_rows), alpha), len(trial_rows))
    log(f"Trials counter: {len(trial_rows)} strategy / version / timeframe tests ({len(trial_new)} new) - "
        f"PAPER_TRADING needs t >= {trial_bar[0]:.2f}")

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
        if s.get("confirm_5m"):               # the fair twin: same signals, no 5m check, same period, same 5m bars
            twin = rs.evaluate(plain5.get(k3, {}), {}, {}, wins_for(k3), R, V["min_coin_trades"]) if k3 in plain5 else None
            if twin:
                twin.pop("_raw")
        elif s.get("control_twin"):
            twin = next((e for k, e in evals.items() if k[0] == s["control_twin"] and k[2] == tf), None)
        paper_ok, paper_reasons = lc.paper_gate(base_status, ev, twin, R, trial_bar)
        if s.get("control_twin") and twin is None:
            paper_ok, paper_reasons = False, paper_reasons + ["control twin was not tested"]
        ck = f"{sid}@{ver}|{tf}"
        prev = registry["cells"].get(ck, {})
        rec = lc.paper_record(paper.get(k3, []))
        status, note, failed = lc.next_status(prev.get("status"), base_status, paper_ok, rec,
                                              int(prev.get("failed_runs") or 0), R)
        status, note = approval_step(ck, status, note, rec, ev, approvals, AP, approval_warnings, eligible_cells,
                                     bool(s.get("lab")))
        results[k3] = status
        cells[ck] = dict(strategy=sid, version=ver, tf=tf, status=status, base_status=base_status, lab=bool(s.get("lab")),
                         t_stat=ev["t_stat"], need_t=round(trial_bar[0], 3),
                         reasons=reasons, paper_gate_failed=paper_reasons if base_status == "VALIDATION" else [],
                         note=note, failed_runs=failed, required_avg_r=round(need, 3),
                         beats_twin=lc.twin_compare(ev, twin, R) if twin else None,
                         twin_same_window=dict(all=twin["all"], validate=twin["validate"])
                         if twin and s.get("confirm_5m") else None,
                         history_from=fmt_day(min(t["entry_time"] for tr in per[k3].values() for t in tr))
                         if any(per[k3].values()) else None,
                         paper=rec, evidence=ev)

    # ---------- failure attribution per strategy version x timeframe (section 17) ----------
    for ck, cell in cells.items():
        k3 = (cell["strategy"], cell["version"], cell["tf"])
        a = att.summarize([t for tr in per[k3].values() for t in tr], A)
        dev, val = cell["evidence"]["develop"], cell["evidence"]["validate"]
        a["strategy_level"] = (["structural_change: profitable in the develop part, losing in the validate part"]
                               if min(dev["n"], val["n"]) >= 10 and dev["avg_r"] > 0 > val["avg_r"] else [])
        cell["attribution"] = a
    for ck, cell in cells.items():
        others = {c["tf"]: c["evidence"]["all"]["avg_r"] for c in cells.values()
                  if c["strategy"] == cell["strategy"] and c["version"] == cell["version"] and c["tf"] != cell["tf"]
                  and c["evidence"]["all"]["n"] >= V["min_trades"]}
        stops = [v for v in cell["evidence"]["perturbation"]["variants"] if v["change"].startswith("stop")]
        cell["attribution"]["diagnosis"] = att.diagnose(cell["attribution"], others, A, stops)
    lessons = {}
    for ck, cell in cells.items():
        for tag in cell["attribution"]["systematic"]:
            lessons.setdefault(tag, []).append(ck)
    candidate_lessons = [dict(tag=t, cells=v, evidence=f"systematic in {len(v)} strategy/timeframe tests")
                         for t, v in sorted(lessons.items(), key=lambda x: -len(x[1])) if len(v) >= 2]
    missed = []
    for m in moves_all:
        found = move_found.get(m["key"], {})
        missed.append(dict(coin=m["coin"], signal_coin=m["signal_coin"], regime=m.get("regime"), direction="up" if m["dir"] == 1 else "down",
                           size_atr=m["size_atr"], pct=m["pct"],
                           start_utc=pd.to_datetime(m["start_ms"], unit="ms").strftime("%Y-%m-%d %H:%M"),
                           end_utc=pd.to_datetime(m["end_ms"], unit="ms").strftime("%Y-%m-%d %H:%M"),
                           verdict=att.move_verdict(found),
                           findings={k: v for k, v in sorted(found.items()) if v not in ("no setup", "no candles")},
                           strategies_checked=len(found)))

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
    packs = write_packs(cells, eligible_cells, by_key, registry, AP, now_txt, args.offline)
    approval_out = dict(eligible=packs, approved=sorted(ck for ck, c in cells.items() if c["status"] == "APPROVED"),
                        listed=sorted(approvals), warnings=approval_warnings + approval_problems
                        + [f"{k}: approval listed but this strategy version / timeframe was not researched this run"
                           for k in sorted(set(approvals) - set(cells))], settings=AP)
    pine_out = export_approved(cells, per, by_key, cfg, now_txt,
                               os.path.join(sc.REPORTS, "pine_offline" if args.offline else "pine"))
    approval_out["pine"] = pine_out
    if not args.offline:
        sc.write_experiments(new_exp, registry)
        sc.write_lifecycle_log(changes, started)
        write_missed(missed, started, A, mem.review_days(cfg.get("memory"), "missed_trades"))
        write_sources(tested, started, mem.review_days(cfg.get("memory"), "research_sources"))

    # ---------- regime playbook (Phase 17 B): measured results per regime -> memory/playbook.md (weekly) ----------
    fam_of = {k: x["family"] for k, x in by_key.items()}
    playbook, pb_matrix = pbk.build(cells, fam_of, rg.LABELS), pbk.matrix(cells, fam_of)
    pb_path = os.path.join(sc.REPORTS, "playbook_offline.md") if args.offline else os.path.join(sc.MEMORY, "playbook.md")
    if args.offline or started.weekday() == 6 or not os.path.exists(pb_path):       # Sundays (and the first time)
        os.makedirs(os.path.dirname(pb_path), exist_ok=True)
        with open(pb_path, "w") as f:
            f.write(pbk.render(playbook, now_txt, rg.LABELS, pb_matrix) + "\n")

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
               attribution_settings=A, candidate_lessons=candidate_lessons, missed_moves=missed,
               approval=approval_out, cells=cells, playbook=playbook, playbook_matrix=pb_matrix,
               trials=dict(trl.summary(trial_rows, alpha), added_this_run=len(trial_new),
                           file=os.path.relpath(TRIALS, sc.ROOT)),
               lab=dict(file=sspec.LAB_FILE, cards=sorted(k for k, x in by_key.items() if x.get("lab")),
                        moved_to_library=moved))
    path = os.path.join(sc.REPORTS, "research_offline.json" if args.offline else "research.json")
    json.dump(out, open(path, "w"), indent=1, default=float)
    n_status = pd.Series(list(results.values())).value_counts().to_dict() if results else {}
    log(f"Research done in {out['duration_s']} s: {len(cells)} strategy/timeframe cells - {n_status}")


if __name__ == "__main__":
    main()
