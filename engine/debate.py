"""
Bull vs bear, and a risk manager with a veto (Phase 18 A item 2).

Idea studied in TradingAgents (R2, memory/research_sources.md): a bull researcher and a bear researcher argue, a risk
team weighs in, a manager decides. Rewritten here in our own, much smaller form - no code copied, no language model:

  * Bull case / Bear case: ONLY the engine's own numbers (backtest, walk-forward, stress test, paper, regime matrix).
    A side with nothing to say says so - it is never filled with opinion.
  * Risk manager: fixed checks that can VETO (event within the blackout window, heat full, regime against, data not
    GOOD or the report stale, day / week loss limit near or a halt). In TradingAgents the risk team only debates and
    the manager may overrule it; here a veto cannot be argued away - it only ever says "not now" (never "go").

Used by the approval packs (engine/approval.py) and the briefing fact sheet (brain_pack.py). Pure functions.
"""
import datetime as dt

import pandas as pd

from engine import regime as rg

LIMIT_NEAR = 0.75          # "limit near": 75% of the day / week loss limit already used (a veto only tightens)
STALE_H = 2.5              # the hourly report is older than this -> its conditions are not current


def _f(x, fmt="+.2f"):
    return "-" if x is None or x != x else f"{x:{fmt}}R"


def cell_cases(cell):
    """(bull, bear): lists of plain sentences, each with the engine's number. cell = a research.json cell."""
    ev, att, paper = cell["evidence"], cell.get("attribution") or {}, cell.get("paper") or {}
    bull, bear = [], []
    a, v = ev["all"], ev["validate"]
    (bull if (v["avg_r"] or 0) > 0 else bear).append(
        f"unseen part of the backtest (last 30%): {_f(v['avg_r'], '+.3f')} per trade over {v['n']} trades")
    (bull if (a["avg_r"] or 0) > 0 else bear).append(
        f"whole history: {_f(a['avg_r'], '+.3f')} per trade over {a['n']} trades, profit factor {a['pf']:.2f}")
    wf = ev["walk_forward"]
    (bull if wf["passed"] else bear).append(
        f"walk-forward: {wf['positive']} of {wf['judged']} time windows profitable, together {_f(wf['pooled_avg_r'], '+.3f')}")
    st = ev["stress"]
    (bull if (st["avg_r"] or 0) > 0 else bear).append(f"costs +50%: {_f(st['avg_r'], '+.3f')} per trade")
    pv = ev["perturbation"]
    if pv["stable"]:
        bull.append(f"every parameter -20% / +20% stays profitable ({len(pv['variants'])} variants)")
    elif pv.get("worst"):
        bear.append(f"not stable: {pv['worst']['change']} gives {_f(pv['worst']['avg_r'], '+.3f')} per trade")
    if ev["positive_coins"]:
        bull.append(f"an edge on {len(ev['positive_coins'])} coin(s): {', '.join(ev['positive_coins'])}")
    else:
        bear.append("no coin with an edge on its own")
    if cell.get("beats_twin") is True:
        bull.append("beats its control twin (the special ingredient adds something)")
    elif cell.get("beats_twin") is False:
        bear.append("does NOT beat its control twin (the special ingredient adds nothing measurable)")
    bear.append(f"worst drawdown in the backtest: {a['max_dd_r']:.1f}R · wins {a['win_rate']:.0f}% of trades")
    if att.get("systematic"):
        bear.append(f"systematic loss tags: {', '.join(att['systematic'])} ({att.get('losses', 0)} losing trades)")
    bear += [f"overfitting flag: {o}" for o in ev.get("overfit") or []]
    n, avg = int(paper.get("n") or 0), paper.get("avg_r")
    if n and avg is not None:
        (bull if avg >= 0 else bear).append(f"paper trading: {_f(avg)} per signal over {n} closed signals")
        gap = (v["avg_r"] or 0) - avg
        if gap > 0:
            bear.append(f"paper is {gap:.2f}R per trade below the backtest's unseen part")
    if cell.get("history_from") and str(cell["history_from"]) > "2024":
        bear.append(f"history starts only {cell['history_from']} - may miss a full bull / bear cycle")
    return bull, bear


def regime_cases(coin_regime):
    """(bull, bear) for one coin from the engine's regime matrix: bullish / bearish timeframes with their reasons."""
    bull, bear, flat = [], [], []
    for tf in ("1w", "1d", "4h", "1h"):
        r = (coin_regime.get("timeframes") or {}).get(tf)
        if not r:
            continue
        d = rg.direction(r.get("label"), r.get("expansion_dir"))
        if d:
            why = "; ".join((r.get("supporting") or [])[:2])
            (bull if d > 0 else bear).append(f"{tf.upper()} {r['label']}" + (f" ({why})" if why else ""))
        elif r.get("label"):
            flat.append(f"{tf.upper()} {r['label']}")
    if flat:
        bear.append("no clear direction on " + ", ".join(flat))       # against any directional trade there
    return bull, bear


def _upcoming(risk, now, minutes):
    out = []
    for e in risk.get("upcoming_events") or []:
        try:
            t = pd.Timestamp(e["start_utc"], tz="UTC").to_pydatetime()
        except (KeyError, ValueError):
            continue
        if dt.timedelta(minutes=-minutes) <= t - now <= dt.timedelta(minutes=minutes):
            out.append(f"{e.get('name') or e.get('type')} at {e['start_utc']} UTC")
    return out


def risk_manager(rep, now, coin=None, direction=None, regimes=None, tf=None, coins=None):
    """The risk manager's checks on the hourly report `rep` (reports/latest.json) at time `now`.
    coin + direction ('LONG' / 'SHORT'): one signal; regimes + tf: a strategy's allowed regimes on its timeframe,
    checked on `coins` (default: the signal coins). Returns dict(veto, reasons, checks=[(name, veto, text)])."""
    if not rep:
        return dict(veto=True, reasons=["the hourly report is not available - conditions unknown"],
                    checks=[("report", True, "not available - conditions unknown")])
    checks = []
    age = (now - pd.Timestamp(rep["generated_utc"], tz="UTC").to_pydatetime()).total_seconds() / 3600
    risk, book = rep.get("risk") or {}, rep.get("position_book") or {}
    lim = risk.get("limits") or {}
    mins = int(lim.get("blackout_minutes") or 60)
    ev = list(risk.get("blackout_now") or []) + _upcoming(risk, now, mins)
    checks.append(("event", bool(ev), f"high-impact event within {mins} min: {'; '.join(map(str, ev))}" if ev
                   else f"no high-impact event within {mins} min"))
    heat, cap = int(book.get("heat") or 0), int((book.get("limits") or {}).get("heat") or lim.get("positions") or 0)
    checks.append(("heat", bool(cap) and heat >= cap, f"heat {heat} of {cap} open live positions"
                   + (" - FULL" if cap and heat >= cap else "")))
    dq = rep.get("data_quality") or {}
    state = dq.get("system_state") or (rep.get("daily") or {}).get("data_state") or "unknown"
    bad = [c for c, x in (dq.get("coins") or {}).items() if x.get("state") != "GOOD" and (coin is None or c == coin)]
    data_bad = state != "GOOD" or bool(bad) or age > STALE_H
    checks.append(("data", data_bad, f"data {state}" + (f", not GOOD: {', '.join(bad)}" if bad else "")
                   + (f", report {age:.1f} h old (stale)" if age > STALE_H else f", report {age:.1f} h old")))
    halts = list(risk.get("halts_text") or [])
    near = []
    for k, name in (("day_r", "day"), ("week_r", "week")):
        v, limit = risk.get(k), lim.get(k)
        if v is not None and limit and float(limit) < 0 and float(v) <= LIMIT_NEAR * float(limit):
            near.append(f"{name} {float(v):+.1f}R of {float(limit):+.0f}R")
    checks.append(("limits", bool(halts or near), "; ".join(halts + [f"{x} (limit near)" for x in near])
                   or f"day {float(risk.get('day_r') or 0):+.1f}R / week {float(risk.get('week_r') or 0):+.1f}R, no halt"))
    rc = (rep.get("regime") or {}).get("coins") or {}
    if coin and direction:
        perm = (rc.get(coin) or {}).get("permission") or "unknown"
        against = perm != f"{direction} allowed"
        checks.append(("regime", against, f"{coin} regime: {perm}"
                       + (f" ({(rc.get(coin) or {}).get('permission_reason')})" if against else "")))
    elif regimes and tf:
        from engine import lifecycle as lc
        rtf = lc.regime_tf(tf)
        pool = coins or (rep.get("universe") or {}).get("signal") or list(rc)
        fit = [c for c in pool if (((rc.get(c) or {}).get("timeframes") or {}).get(rtf) or {}).get("label") in regimes]
        checks.append(("regime", not fit, f"{len(fit)} of {len(pool)} signal coins are in one of its regimes on "
                       f"{rtf.upper()} now" + (f" ({', '.join(fit)})" if fit else " - regime against")))
    reasons = [t for _, v, t in checks if v]
    return dict(veto=bool(reasons), reasons=reasons, checks=checks)


def risk_line(rm):
    """'Risk manager: VETO - ...' or 'Risk manager: no veto (...)' - one line."""
    if rm["veto"]:
        return "Risk manager: VETO - " + "; ".join(rm["reasons"])
    return "Risk manager: no veto (" + "; ".join(t for _, _, t in rm["checks"]) + ")"


def case_lines(bull, bear, rm, indent=""):
    return [f"{indent}Bull case: " + ("; ".join(bull) if bull else "nothing in the engine's numbers"),
            f"{indent}Bear case: " + ("; ".join(bear) if bear else "nothing in the engine's numbers"),
            indent + risk_line(rm)]
