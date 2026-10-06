"""
Roadmap step 5 part 2 (operator, 2026-10-06): strategies by market type.

The research run already splits every strategy / timeframe cell's backtest trades by the market regime at entry
(engine/attribution.py by_regime, the same numbers as memory/playbook.md). This module turns that into a live filter:
a strategy does not alert in a regime where it measurably lost money - at least MIN_N backtest trades there with an
average of AVOID_R or worse (fees included). It only ever REMOVES alerts; it never adds one, and an unknown regime or
too few trades means no block (no evidence either way).

  table(cells)               -> {"id@version|tf": {regime: [n, avg R]}} - written by the research run as
                                reports/regime_fit.json (the live watcher downloads it)
  blocked(fit, key, regime)  -> the reason the alert is blocked, or None
Pure: no internet, no files.
"""
from engine.playbook import AVOID_R, MIN_N


def table(cells):
    out = {}
    for ck, c in (cells or {}).items():
        seg = ((c.get("attribution") or {}).get("by_regime")) or {}
        rows = {lab: [int(v["n"]), round(float(v["avg_r"]), 3)] for lab, v in seg.items()
                if isinstance(v, dict) and v.get("n")}
        if rows:
            out[ck] = rows
    return out


def blocked(fit, key, regime, min_n=MIN_N, max_r=AVOID_R):
    """key = 'id@version|tf'. A reason string when this cell lost money in this regime, else None."""
    row = ((fit or {}).get(key) or {}).get(regime) if regime else None
    if not row:
        return None
    n, avg = row
    if n >= min_n and avg <= max_r:
        return f"lost money in {regime} markets in the backtest ({avg:+.2f}R over {n} trades)"
    return None
