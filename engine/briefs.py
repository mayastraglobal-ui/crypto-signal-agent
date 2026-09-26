"""
Email content built from facts (AGENT_PROMPT.md section 20) - Phase 12.

The engine writes the "why" of every signal email itself (no AI): the points come only from values measured at the
signal candle (trend, structure, momentum, volume, SMC context, session). The email layouts are in engine/emails.py
(format v2); the older text templates that lived here were removed with it.

Pure functions: no internet, no files.
"""
import math

import numpy as np

RECENT = 10          # "recent" SMC event = within the last 10 candles of the signal timeframe


def _num(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def facts_at(feats, t, d):
    """What was true at the close of signal candle t (index), for a trade in direction d (+1 / -1)."""
    def col(name):
        return feats[name].to_numpy() if name in feats else None

    def recent(name, n=RECENT):
        a = col(name)
        if a is None:
            return None
        w = np.nan_to_num(a[max(0, t - n + 1): t + 1].astype(float))
        hits = np.flatnonzero(w)
        return None if not len(hits) else int(len(w) - 1 - hits[-1])       # candles ago
    def at(name):
        a = col(name)
        return None if a is None else a[t]
    up = d == 1
    return dict(
        range_pos=_num(at("smc_range_pos")),
        sweep_ago=recent("smc_sweep_bull" if up else "smc_sweep_bear"),
        choch_ago=recent("smc_choch_up" if up else "smc_choch_down"),
        bos_ago=recent("smc_bos_up" if up else "smc_bos_down"),
        displacement_ago=recent("displacement_up" if up else "displacement_down", 5),
        fvg_retrace=bool(_num(at("smc_fvg_retrace_bull" if up else "smc_fvg_retrace_bear")) or 0),
        in_ob=bool(_num(at("smc_in_bull_ob" if up else "smc_in_bear_ob")) or 0),
        rel_vol=_num(at("rel_vol")),
        structure=feats["structure"].iloc[t] if "structure" in feats else None,
    )


def ago(n):
    return "on the signal candle" if n == 0 else f"{n} candle(s) ago"


def why_points(d, ctx, facts, session, conditions):
    """3-5 short reasons, each a measured fact. ctx = the plan's context (htf trend, regime, RSI, volume)."""
    side = "up" if d == 1 else "down"
    pts = [f"Trend: higher timeframe {ctx.get('htf_trend', '?')}, regime {ctx.get('regime') or '?'} "
           "(allowed for this strategy)"]
    st = []
    if facts.get("structure") in ("up", "down"):
        st.append(f"swing structure {facts['structure']}")
    if facts.get("choch_ago") is not None:
        st.append(f"change of character {side} {ago(facts['choch_ago'])}")
    elif facts.get("bos_ago") is not None:
        st.append(f"break of structure {side} {ago(facts['bos_ago'])}")
    if st:
        pts.append("Structure: " + ", ".join(st))
    mom = [f"RSI(14) {ctx['rsi14']}"] if ctx.get("rsi14") is not None else []
    if facts.get("displacement_ago") is not None:
        mom.append(f"strong {side} candle {ago(facts['displacement_ago'])}")
    if ctx.get("volume_vs_avg") is not None:
        mom.append(f"volume {ctx['volume_vs_avg']}x its 20-candle average")
    if mom:
        pts.append("Momentum and volume: " + ", ".join(mom))
    smc = []
    if facts.get("sweep_ago") is not None:
        smc.append(f"liquidity {'below' if d == 1 else 'above'} taken {ago(facts['sweep_ago'])}")
    if facts.get("fvg_retrace"):
        smc.append("price back in a fair value gap")
    if facts.get("in_ob"):
        smc.append("price in an order block")
    rp = facts.get("range_pos")
    if rp is not None:
        smc.append("below the dealing range" if rp < 0 else "above the dealing range" if rp > 1 else
                   ("discount" if rp < 0.5 else "premium") + f" ({rp * 100:.0f}% of the dealing range)")
    if session and session not in ("n/a",):
        smc.append(f"session: {session}")
    if smc:
        pts.append("SMC context: " + ", ".join(smc))
    if conditions:                        # a caution is never cut: at most 4 reasons + the caution
        return pts[:4] + ["Caution: " + ", ".join(c.replace("_", " ") for c in conditions)]
    return pts[:5]
