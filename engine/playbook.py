"""
The regime playbook (Phase 17 B) - memory/playbook.md, rewritten by every daily research run.

For each market regime: which strategy families and which strategy / timeframe cells made money in it, which lost,
and what "no trade" means there. Built ONLY from measured numbers: the research run's backtest trades (all coins,
all history, fees included), split by the regime at entry (failure attribution, section 17). Nothing is written by
hand or by Claude, so it can never say more than the data.

It is a map, not a signal: a cell listed as "made money" still needs every research test and the operator's yes
before it sends an email. Pure functions; research.py writes the file.
"""
MIN_N = 30                 # trades in a regime before a cell or family is listed at all
AVOID_R = -0.10            # average R at or below this with MIN_N trades -> "lost money here"
TOP = 6                    # cells listed per regime and side

NO_TRADE = {
    "STRONG_BULL": "no long setup from a strategy that fits, or price far above its averages (chasing)",
    "WEAK_BULL": "no setup, or the higher timeframes disagree",
    "RANGE": "price in the middle of the range; breakouts without volume",
    "HIGH_VOL_RANGE": "candles several ATRs wide: stops get hit by noise",
    "WEAK_BEAR": "no setup, or the higher timeframes disagree",
    "STRONG_BEAR": "no short setup from a strategy that fits, or buying dips against the trend",
    "COMPRESSION": "before the break: wait for a close outside the range",
    "EXPANSION": "the move is already several ATRs old (late entry)",
    "TRANSITION": "the trend is changing: most trend and range strategies are unreliable here",
    "UNCLEAR": "the data does not show a regime - stand aside",
}


def build(cells, family_of, labels):
    """cells: research.json cells ({key: cell with attribution.by_regime}); family_of: {'id@version': family}.
    Returns {label: dict(fits, avoid, families, cells_seen)} - lists of (name, n, avg R), best / worst first."""
    out = {}
    for label in labels:
        rows, fam = [], {}
        for ck, c in cells.items():
            seg = ((c.get("attribution") or {}).get("by_regime") or {}).get(label)
            if not seg or seg["n"] < MIN_N:
                continue
            name = f"{c['strategy']} v{c['version']} {c['tf']}" + (" (lab)" if c.get("lab") else "")
            rows.append((name, int(seg["n"]), float(seg["avg_r"]), c.get("status")))
            f = family_of.get(f"{c['strategy']}@{c['version']}", "?")
            n0, s0 = fam.get(f, (0, 0.0))
            fam[f] = (n0 + seg["n"], s0 + seg["n"] * seg["avg_r"])
        fits = sorted([r for r in rows if r[2] >= 0.005], key=lambda r: -r[2])[:TOP]      # rounds to +0.01R or more
        avoid = sorted([r for r in rows if r[2] <= AVOID_R], key=lambda r: r[2])[:TOP]
        families = sorted(((f, n, s / n) for f, (n, s) in fam.items() if n >= MIN_N), key=lambda x: -x[2])
        out[label] = dict(fits=fits, avoid=avoid, families=families, cells_seen=len(rows))
    return out


def _r(x):
    return f"{x:+.2f}R"


def section(label, pb):
    """The playbook lines of one regime."""
    p = pb.get(label)
    L = [f"## {label}"]
    if not p or not p["cells_seen"]:
        return L + [f"- no strategy has {MIN_N}+ backtest trades in this regime yet - no evidence either way",
                    f"- no trade looks like: {NO_TRADE.get(label, '-')}", ""]
    L.append("- families (all their trades in this regime): "
             + ("; ".join(f"{f} {_r(a)} ({n})" for f, n, a in p["families"]) or "none with enough trades"))
    L.append("- made money here: " + ("; ".join(f"{n} {_r(a)} over {k} trades [{s}]" for n, k, a, s in p["fits"])
                                      or "NOTHING - no tested strategy made money in this regime"))
    L.append("- lost money here: " + ("; ".join(f"{n} {_r(a)} over {k} trades" for n, k, a, _ in p["avoid"])
                                      or "none below " + _r(AVOID_R)))
    L.append(f"- no trade looks like: {NO_TRADE.get(label, '-')}"
             + ("; and here NO strategy has shown an edge - standing aside IS the playbook" if not p["fits"] else ""))
    return L + [""]


def render(pb, run_utc, labels):
    head = ["# Regime playbook (generated - do not edit)", "",
            f"Written by the daily research run {run_utc} UTC from backtest trades only (all coins, all history, "
            "fees included), split by the market regime at entry. A cell or family needs "
            f"{MIN_N}+ trades in a regime to be listed. [status] = its lifecycle status now.", "",
            "**A map, not a signal.** \"Made money here\" is measured history, not a forecast, and is not "
            "significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.", ""]
    body = []
    for label in labels:
        body += section(label, pb)
    return "\n".join(head + body)
