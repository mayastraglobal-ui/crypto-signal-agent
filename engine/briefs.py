"""
Email content built from facts (AGENT_PROMPT.md section 20) - Phase 12.

The engine writes every email itself (no AI): the "why" points come only from values measured at the
signal candle (trend, structure, momentum, volume, SMC context, session), the invalidation list from the
strategy's own rules, and the evidence from the backtest layers and the paper / live record.

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


def invalidation(p):
    """What cancels the trade - only the strategy's tested rules plus the section 16 watch items."""
    out = [f"Stop-loss {p['stop']:.6g} is hit (the trade is closed, -1R before costs)"]
    if p.get("exit_rule"):
        out.append("Early exit rule becomes true: " + " AND ".join(map(str, p["exit_rule"])))
    out.append(f"Time stop: closed after {p['max_hold']} if no target is reached")
    if p.get("confirm_5m"):
        out.append("Before entry: no 5m confirmation within 6 bars, or a 5m break of structure against the trade")
    out.append("Watch (not an exit): an opposite structure break, a regime change or a volatility spike")
    return out


def evidence(board_row, paper, live):
    """Evidence lines: Layers A/B/C with sample sizes + the paper and live record (section 20)."""
    b = board_row or {}

    def n_avg(n, a):
        return "not run yet" if n in (None, "") or (isinstance(n, float) and not math.isfinite(n)) \
            else f"{int(n)} trades, {float(a):+.2f}R avg"
    lines = [f"Layer B (all history): {n_avg(b.get('trades'), b.get('avg_r'))}"
             + (f", PF {float(b['profit_factor']):.2f}" if _num(b.get("profit_factor")) is not None else ""),
             "Layer C (walk-forward): " + (f"{b['walk_forward']} windows profitable" if b.get("walk_forward")
                                           else "not run yet"),
             f"Layer A (last 15 days): {n_avg(b.get('layer_a_trades'), b.get('layer_a_avg_r') or 0)}",
             f"Paper record: {n_avg(paper['n'], paper['avg_r']) if paper and paper['n'] else 'none yet'}",
             f"Live record: {n_avg(live['n'], live['avg_r']) if live and live['n'] else 'none yet'}"]
    return lines


def record(logdf, strategy, version, tf, stages):
    """Closed results of one strategy version x timeframe in the given stages: dict(n, avg_r)."""
    if logdf is None or logdf.empty:
        return dict(n=0, avg_r=0.0)
    d = logdf[(logdf["strategy"] == strategy) & (logdf["version"].fillna("1.0").astype(str) == str(version))
              & (logdf["tf"] == tf) & logdf["stage"].isin(stages) & (logdf["status"] != "OPEN")]
    r = d["result_r"].dropna().astype(float)
    return dict(n=int(len(r)), avg_r=float(r.mean()) if len(r) else 0.0)


def fmt(x):
    x = float(x)
    return f"{x:,.2f}" if x >= 1000 else f"{x:,.4f}" if x >= 1 else f"{x:.6g}"


REGIME_ORDER = ["1w", "1d", "4h", "1h", "30m", "15m", "5m"]


def entry_email(e):
    """[ENTRY] email (section 20) from an entry card e. Returns dict(subject, lines)."""
    d = 1 if e["direction"] == "LONG" else -1
    R = abs(e["entry"] - e["stop"])
    rr = abs(e["targets"][0]["price"] - e["entry"]) / R if R > 0 and e["targets"] else 0.0
    subject = (f"[ENTRY] {e['direction']} {e['coin']}/{e['quote']} | {e['tf']} | {e['strategy']} v{e['version']} | "
               f"R:R {rr:.1f}")
    z = sorted(e["entry_zone"])
    L = [f"{e['direction']} {e['coin']}/{e['quote']} - {e['market']} · {e['tf']} · {e['strategy']} v{e['version']} "
         f"({e['stage']})",
         f"Time: {e['utc']} UTC / {e['beijing']} Beijing · data {e['data_state']}",
         "Regime: " + " · ".join(f"{tf.upper()} {e['regimes'][tf]}" for tf in REGIME_ORDER if e["regimes"].get(tf)),
         "",
         f"Entry zone : {fmt(z[0])} - {fmt(z[1])}   (do not chase outside it)",
         f"Stop-loss  : {fmt(e['stop'])}  ({R / e['entry'] * 100:.2f}% away)"]
    for i, t in enumerate(e["targets"], 1):
        last = i == len(e["targets"])
        what = "close the rest" if last else f"close {t['close_pct']}%, " + (
            "move stop to entry (breakeven)" if i == 1 else "move stop to TP1")
        L.append(f"TP{i}        : {fmt(t['price'])}  ({t['r']:.1f}R) -> {what}")
    L.append(f"R:R to TP1 : {rr:.2f}")
    if e.get("confirm_5m"):
        L.append(f"5m confirm : bar closed {e['confirm_5m']} UTC" + (f" ({e['smc_5m']})" if e.get("smc_5m") else ""))
    sz = e["size"]
    L.append(f"Size       : {sz['qty']:.6g} {e['coin']} (~{sz['usdt']:.0f} USDT) = {sz['risk_usdt']:.2f} USDT risk "
             f"({sz['risk_pct']:g}% of the account)" + (" - made smaller: more would need over 3x leverage"
                                                       if sz.get("capped") else ""))
    if d == -1:
        L.append("Market     : FUTURES ONLY (a short cannot be done on spot); futures fees and funding are counted")
    L.append(f"Expires    : {e['expires']}")
    L += ["", "Why this signal exists:"] + [f"  - {w}" for w in e["why"]]
    L += ["", "What cancels it:"] + [f"  - {w}" for w in e["invalidation"]]
    L += ["", "Evidence:"] + [f"  - {w}" for w in e["evidence"]]
    return dict(subject=subject, lines=L)


EXIT_WORDS = {"BE": "BE (rest stopped at entry)", "TRAIL": "TRAIL (rest stopped at the previous target)",
              "SL": "SL", "TIME": "TIME", "EXIT_RULE": "EXIT_RULE"}


def exit_email(x):
    """[EXIT] email (section 20): x = dict(coin, quote, direction, tf, strategy, version, kind TP1_HIT / CLOSED,
    close_reason, result_r, entry, exit_price, next_action, closed_utc, stage)."""
    if x["kind"] == "TP1_HIT":
        reason = "TP1"
        head = f"TP1 reached - part closed, stop moved to breakeven ({fmt(x['entry'])})"
    else:
        reason = EXIT_WORDS.get(x["close_reason"], x["close_reason"])
        head = f"Closed: {reason}, result {x['result_r']:+.2f}R after costs"
    subject = f"[EXIT] {x['coin']}/{x['quote']} {x['direction']} | {reason}"
    L = [f"{x['coin']}/{x['quote']} {x['direction']} · {x['tf']} · {x['strategy']} v{x['version']} ({x['stage']})",
         f"Time: {x['utc']} UTC / {x['beijing']} Beijing", "", head,
         f"Entry {fmt(x['entry'])}" + (f" · exit {fmt(x['exit_price'])}" if x.get("exit_price") else ""),
         f"Next action: {x['next_action']}"]
    return dict(subject=subject, lines=L)


def daily_email(dly):
    """The 08:00 Beijing daily report (section 20) from the scan's `daily` block."""
    subject = f"[DAILY] Crypto signal report {dly['date']} - {dly['signals']} signal(s), BTC 1D {dly['btc'].get('1d', '?')}"
    L = [f"Daily report - {dly['utc']} UTC / {dly['beijing']} Beijing", "",
         "MARKET", f"  BTC trend: daily {dly['btc'].get('1d', '?')}, 4H {dly['btc'].get('4h', '?')}"
         + (f" · Fear & Greed {dly['fear_greed']['value']} ({dly['fear_greed']['label']})" if dly.get("fear_greed") else ""),
         f"  Data: {dly['data_state']}", "",
         "TOP COINS (signal list)",
         "  Coin  | Price       | 24h vol (M) | 1W / 1D / 4H / 1H regime                        | 30m momentum | 15m setup | 5m trigger"]
    for r in dly["matrix"]:
        L.append(f"  {r['coin']:<5} | {fmt(r['price']):>11} | {r['vol_24h_m']:>11.0f} | "
                 f"{' / '.join(r['regimes']):<48} | {r['mom_30m']:<12} | {r['setup_15m']:<9} | {r['trigger_5m']}")
    L += ["", "STRATEGY HEALTH (last 24 hours)"] + ([f"  - {c}" for c in dly["health"]] or ["  no status changes"])
    L += ["", "EVENT CALENDAR (next 7 days)"] + ([f"  - {e}" for e in dly["events"]] or ["  none listed"])
    if dly.get("calendar_warning"):
        L.append(f"  ! {dly['calendar_warning']}")
    return dict(subject=subject, lines=L)
