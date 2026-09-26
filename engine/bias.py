"""
Lookahead and recursive checks (Phase 18 B item 4) - ideas from freqtrade's lookahead-analysis and recursive-analysis
(R3, GPL-3.0: the ideas only, rewritten here; no code copied).

  * LOOKAHEAD: the history is cut right after a signal candle (every candle that closed later is removed, on every
    timeframe) and everything is computed again. Each entry / exit rule and each stop / target level of every card
    must give EXACTLY the same answer on every candle both runs share. A difference means the full run knew something
    that was not known at that candle - the backtest used the future.
  * RECURSIVE: the history of every trade timeframe starts 500 candles later. After a settling stretch, the rules and
    levels must again give the same answers (a tiny share of flips from rounding is tolerated). A difference means a
    value depends on where the history starts (e.g. a running total), so live values - computed on a few hundred
    candles - would not match the backtest.

A card that fails either check is BIASED: every timeframe of that version is FAILED and can never pass (research.py,
the registry column `bias`). The check runs on the first research coin (BTC). Pure functions; the engine's own
prepare / rule functions are passed in.
"""
import re
import time

import numpy as np
import pandas as pd

WARMUP = 250                     # scanner.strategy_signals: no signal in the first 250 candles


def cut_data(data, end_ms=None, drop=0, drop_tfs=()):
    """A copy of the candle tables {(symbol, tf): df}: only candles closed by end_ms, and/or the first `drop` candles
    of the timeframes in drop_tfs removed."""
    out = {}
    for key, df in data.items():
        if df is None:
            out[key] = df
            continue
        d = df
        if end_ms is not None:
            d = d[d["close_time"] <= end_ms]
        if drop and key[1] in drop_tfs:
            d = d.iloc[drop:]
        out[key] = d.reset_index(drop=True)
    return out


CHECK_VERSION = 2          # v2: higher-timeframe inputs must settle too (settled_from)
_VERSION_TAG = re.compile(r"\(check v(\d+)\)$")


def tag(text):
    """A BIASED finding as stored in the registry: '... (check v2)'."""
    return f"{text} (check v{CHECK_VERSION})" if text else text


def sticky(text):
    """A stored BIASED finding keeps the card FAILED for good only when the current check version (or a later one)
    found it. Findings of an older, corrected check are checked again on this run - a real bias is found again."""
    m = _VERSION_TAG.search(str(text or "").strip())
    return bool(m) and int(m.group(1)) >= CHECK_VERSION


def bar_ms(df):
    ot = df["open_time"].to_numpy()
    return int(np.median(np.diff(ot))) if len(ot) > 1 else 0


def settled_from(frames, tf, settle):
    """Where the recursive comparison of timeframe tf starts: after `settle` candles of tf itself AND of every longer
    timeframe (its higher-timeframe inputs, e.g. htf_up on 1h reads 4h). Every timeframe starts `drop` of ITS OWN
    candles later, so a 4h input settles much later than the 1h candles that read it (check v2 - v1 compared the 1h
    candles while their 4h trend had not settled yet: a false alarm on every card using htf_up / htf_down)."""
    own = frames.get(tf)
    if own is None or not len(own["df"]):
        return None
    size = bar_ms(own["df"])
    out = []
    for fr in frames.values():
        ot = fr["df"]["open_time"].to_numpy()
        if len(ot) and bar_ms(fr["df"]) >= size:
            out.append(int(ot[min(len(ot) - 1, settle)]))
    return max(out) if out else None


def cut_frames(frames, end_ms):
    """{tf: df} (e.g. BTC's closes for btc_ret) cut at end_ms."""
    return {tf: df[df["close_time"] <= end_ms].reset_index(drop=True) for tf, df in (frames or {}).items()}


def rule_arrays(spec, fr, eval_rules, level_array, columns_needed):
    """{what: array}: every single entry / exit rule of a card (booleans) and every stop / target level (floats)."""
    ns, idx, n = fr["ns"], fr["df"].index, fr["n"]
    out = {}
    for side in ("long", "short", "exit_long", "exit_short"):
        for rule in spec.get(side) or []:
            out[f"{side}: {rule}"] = np.asarray(eval_rules([rule], ns, idx), dtype=bool)
    for c in sorted(columns_needed(spec)):
        out[f"level: {c}"] = np.asarray(level_array(c, ns, n), dtype=float)
    return out


def signal_times(spec, arrays, df):
    """Close times of the candles where all long rules (or all short rules) are true, after the warm-up."""
    n = len(df)
    sides = []
    for side in ("long", "short"):
        rules = [a for k, a in arrays.items() if k.startswith(side + ": ")]
        if rules:
            sides.append(np.logical_and.reduce(rules))
    if not sides:
        return np.array([], dtype=np.int64)
    sig = np.logical_or.reduce(sides)
    sig[:WARMUP] = False
    return df["close_time"].to_numpy()[sig[:n]]


def differences(full_df, full_arr, cut_df, cut_arr, from_ms=None, tol_share=0.0, rtol=1e-9):
    """Compare the arrays of two runs on the candles both have (matched by open time, from from_ms on).
    Returns [dict(what, bars, of, first_ms, last_ms, late)] for every rule / level that differs on more than tol_share
    of them; late = differing candles in the second half of the compared candles (0 = the difference died out)."""
    tf_, tc = full_df["open_time"].to_numpy(), cut_df["open_time"].to_numpy()
    pos = np.searchsorted(tf_, tc)
    ok = pos < len(tf_)
    ok[ok] = tf_[pos[ok]] == tc[ok]
    if from_ms is not None:
        ok &= tc >= from_ms
    out = []
    n_ok = int(ok.sum())
    if not n_ok:
        return out
    for k, a in cut_arr.items():
        b = full_arr.get(k)
        if b is None:
            continue
        x, y = a[ok], b[pos[ok]]
        if x.dtype == bool:
            bad = x != y
        else:
            both_nan = np.isnan(x) & np.isnan(y)
            close = np.abs(x - y) <= rtol * np.maximum(1.0, np.abs(y))
            bad = ~(both_nan | close)
        nb = int(bad.sum())
        if nb > tol_share * n_ok:
            out.append(dict(what=k, bars=nb, of=n_ok, first_ms=int(tc[ok][bad][0]), last_ms=int(tc[ok][bad][-1]),
                            late=int(bad[n_ok // 2:].sum())))
    return out


def pick_cuts(times, n_cuts, lo=0.3):
    """n_cuts signal close times spread over the later part (from the `lo` quantile on) of all signal times."""
    t = np.unique(np.asarray(times, dtype=np.int64))
    if not len(t) or n_cuts <= 0:
        return []
    t = t[int(lo * (len(t) - 1)):]
    idx = np.unique(np.linspace(0, len(t) - 1, min(n_cuts, len(t))).round().astype(int))
    return [int(t[i]) for i in idx]


def check_coin(sym, base, data, quality, tfs, cfg, derivs, btc, full, cards, prepare, eval_rules, level_array,
               columns_needed, S):
    """Run both checks on one coin. full = prepare(...) on the whole history (the research run's own frames);
    cards = the loaded strategy cards; S = settings(). Returns dict(coin, cuts, recursive, findings={card key:
    [dict(check, tf, what, bars, of, first_utc)]}, checked={card key: [tf]}, seconds)."""
    t0 = time.time()
    arrays, times = {}, []
    for s in cards:
        for tf in s["timeframes"]:
            fr = full["frames"].get(tf)
            if fr is None:
                continue
            try:
                a = rule_arrays(s, fr, eval_rules, level_array, columns_needed)
            except Exception:
                continue                                   # a rule error is reported by the research run itself
            arrays[(f"{s['id']}@{s['version']}", tf)] = a
            times += list(signal_times(s, a, fr["df"]))
    cuts = pick_cuts(times, int(S["lookahead_cuts"]))
    findings, checked, warnings = {}, {}, {}
    by_key = {f"{s['id']}@{s['version']}": s for s in cards}

    def run(kind, pc, from_ms_fn, tol):
        for (key, tf), fa in arrays.items():
            fr = pc["frames"].get(tf)
            if fr is None:
                continue
            from_ms = from_ms_fn(tf, pc)
            try:
                ca = rule_arrays(by_key[key], fr, eval_rules, level_array, columns_needed)
            except Exception as e:
                findings.setdefault(key, []).append(dict(check=kind, tf=tf, what=f"rule error on the shorter history: "
                                                         f"{e}", bars=0, of=0, first_utc="-"))
                continue
            checked.setdefault(key, set()).add(tf)
            for d in differences(full["frames"][tf]["df"], fa, fr["df"], ca, from_ms, tol):
                f = dict(check=kind, tf=tf, what=d["what"], bars=d["bars"], of=d["of"],
                         first_utc=pd.to_datetime(d["first_ms"], unit="ms").strftime("%Y-%m-%d %H:%M"),
                         last_utc=pd.to_datetime(d["last_ms"], unit="ms").strftime("%Y-%m-%d %H:%M"))
                # recursive differences that die out (none in the later half of the compared history) are a slow
                # warm-up (e.g. a long EMA on a higher timeframe), not a card whose answers depend on where history
                # starts: a warning, never BIASED. Lookahead differences are always BIASED.
                (warnings if kind == "recursive" and d["late"] == 0 else findings).setdefault(key, []).append(f)

    for t in cuts:
        pc = prepare(sym, base, cut_data(data, end_ms=t), quality, tfs, cfg, derivs, cut_frames(btc, t))
        run("lookahead", pc, lambda tf, pc_: None, 0.0)
    drop, settle = int(S["recursive_drop"]), int(S["recursive_settle"])
    pc = prepare(sym, base, cut_data(data, drop=drop, drop_tfs=tfs), quality, tfs, cfg, derivs, btc)

    run("recursive", pc, lambda tf, pc_: settled_from(pc_["frames"], tf, settle),
        float(S["recursive_tolerance_pct"]) / 100)
    for store in (findings, warnings):                      # one line per rule / level, the first finding
        for key in list(store):
            seen, keep = set(), []
            for f in store[key]:
                k = (f["check"], f["what"])
                if k not in seen:
                    seen.add(k)
                    keep.append(f)
            store[key] = keep
    for key in list(warnings):                              # a card that is BIASED anyway needs no warm-up warning
        if key in findings:
            warnings.pop(key)
    return dict(coin=base, cuts=[pd.to_datetime(t, unit="ms").strftime("%Y-%m-%d %H:%M") for t in cuts],
                recursive=dict(drop=drop, settle=settle, tolerance_pct=float(S["recursive_tolerance_pct"])),
                findings=findings, warnings=warnings, checked={k: sorted(v) for k, v in checked.items()},
                seconds=round(time.time() - t0, 1))


DEFAULTS = dict(lookahead_cuts=6, recursive_drop=500, recursive_settle=1000, recursive_tolerance_pct=0.1)


def settings(section):
    S = dict(DEFAULTS)
    S.update({k: v for k, v in (section or {}).items() if k in DEFAULTS})
    return S


def summary(finds):
    """'lookahead on 1h: long: x > y (3 of 900 candles, first 2024-01-02 10:00)' - one line per finding."""
    return [f"{f['check']} on {f['tf']}: {f['what']} ({f['bars']} of {f['of']} candles differ, first {f['first_utc']})"
            for f in finds]


def report_lines(research):
    """reports/latest.md section 3b: the research run's duration and the Phase 18 B checks (markdown lines)."""
    research = research or {}
    rb = research.get("robustness")
    if not rb:
        return []
    L = []
    dur = research.get("duration_s")
    if dur is not None:
        budget = rb.get("time_budget_min", 90)
        L.append(f"**Research run duration:** {dur / 60:.1f} min (budget {budget} min)"
                 + (" - OVER BUDGET: tell the operator" if dur > budget * 60 else "")
                 + (f"; rule test skipped for {', '.join(rb['rules_skipped_coins'])} to stay inside it"
                    if rb.get("rules_skipped_coins") else "") + ".\n")
    b = rb.get("bias") or {}
    if b.get("error"):
        L.append(f"**Lookahead / recursive check:** did NOT run ({b['error']}) - no card can reach PAPER_TRADING "
                 "until it runs.\n")
    elif b:
        L.append(f"**Lookahead / recursive check** (on {b.get('coin')}): {len(b.get('checked') or {})} cards checked - "
                 f"history cut after {len(b.get('cuts') or [])} signal candles, and started "
                 f"{(b.get('recursive') or {}).get('drop')} candles later; {len(b.get('findings') or {})} BIASED "
                 f"({b.get('seconds')} s).\n")
        for k, f in sorted((b.get("findings") or {}).items()):
            L.append(f"- ⛔ **{k} BIASED** - FAILED on every timeframe, for good: " + "; ".join(summary(f)[:3]))
        for k, f in sorted((b.get("warnings") or {}).items()):
            L.append(f"- ⚠ **{k}: warm-up only** (a warning, not BIASED - the differences die out early): "
                     + "; ".join(summary(f)[:2]))
        if b.get("findings") or b.get("warnings"):
            L.append("")
    mc = rb.get("monte_carlo") or {}
    cells = research.get("cells") or {}
    shown = [(k, c) for k, c in sorted(cells.items()) if c.get("status") in ("VALIDATION", "PAPER_TRADING", "APPROVED")
             and (c["evidence"].get("monte_carlo") or {}).get("n")]
    if mc:
        L.append(f"**Monte Carlo** ({mc.get('runs')} shuffles of each cell's trades): PAPER_TRADING also needs the 95% "
                 f"worst drawdown ≤ {mc.get('limit_r'):g}R.\n")
        if shown:
            L.append("| Strategy | TF | Status | Trades | Drawdown as it happened | 95% worst drawdown | Expected worst "
                     "losing streak |")
            L.append("|---|---|---|---|---|---|---|")
            for k, c in shown:
                m = c["evidence"]["monte_carlo"]
                L.append(f"| {c['strategy']} v{c['version']} | {c['tf']} | {c['status']} | {m['n']} | {m['dd_r']:.1f}R | "
                         f"{m['dd95_r']:.1f}R{' ✗' if m['dd95_r'] > mc.get('limit_r', 1e9) else ''} | {m['streak95']} |")
            L.append("")
    idle = rb.get("rules_adding_nothing") or {}
    if idle:
        L.append(f"**Rule significance:** in {len(idle)} strategy / timeframe cell(s) an entry rule adds nothing (the "
                 "card does at least as well without it). Simpler cards queued in the lab: "
                 + (", ".join(x["id"] for x in rb.get("simpler_queued") or []) or "none") + ".\n")
    return L
