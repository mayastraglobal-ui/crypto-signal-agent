"""
Signal state machine and position book (AGENT_PROMPT.md sections 13 and 16) - Phase 10.

  NO_SETUP -> WATCH -> SETUP_FORMING -> AWAITING_5M -> ENTRY_TRIGGERED -> POSITION_ACTIVE
     -> TP1_HIT (stop -> breakeven) -> CLOSED (TP / BE / SL / TIME / EXIT_RULE)
  side exits: EXPIRED (no 5m confirmation in 6 bars) · INVALIDATED (structure broken before entry)
  NO_TRADE: an APPROVED signal the risk engine did not allow (Phase 11) - logged with the failed step

WATCH and SETUP_FORMING are shown in the report only; every tracked signal (a row of
reports/signals_log.csv) starts at AWAITING_5M (strategies with confirm_5m) or at ENTRY_TRIGGERED.
Exits come only from the strategy's tested rules; the other section-16 checks are WARNINGS.

Pure functions: no internet, no files.
"""
import datetime as dt

import numpy as np
import pandas as pd

WATCH, FORMING = "WATCH", "SETUP_FORMING"
AWAITING, TRIGGERED, ACTIVE, TP1_HIT, CLOSED = "AWAITING_5M", "ENTRY_TRIGGERED", "POSITION_ACTIVE", "TP1_HIT", "CLOSED"
EXPIRED, INVALIDATED, NO_TRADE = "EXPIRED", "INVALIDATED", "NO_TRADE"
OPEN_STATES = [AWAITING, ACTIVE, TP1_HIT]        # rows the next run still has to look at
FINAL_STATES = [CLOSED, EXPIRED, INVALIDATED, NO_TRADE]
# which state may follow which (anything else is a bug and raises)
NEXT = {None: {AWAITING, TRIGGERED, NO_TRADE}, AWAITING: {AWAITING, TRIGGERED, EXPIRED, INVALIDATED},
        TRIGGERED: {ACTIVE, TP1_HIT, CLOSED}, ACTIVE: {ACTIVE, TP1_HIT, CLOSED}, TP1_HIT: {TP1_HIT, CLOSED}}
BJ = dt.timezone(dt.timedelta(hours=8))
LIMITS = dict(day_r=-3.0, week_r=-6.0, heat=3)     # section 15 - enforced by engine/risk.py


def check_move(old, new):
    """Raise if old -> new is not an allowed state change."""
    if new not in NEXT.get(old, set()):
        raise ValueError(f"state change {old} -> {new} is not allowed")


def row_state(row):
    """State of a log row; rows written before Phase 10 have no state: OPEN = active, else closed."""
    s = row.get("state")
    if isinstance(s, str) and s:
        return s
    return ACTIVE if row.get("status") == "OPEN" else CLOSED


def close_reason(sim_reason):
    """simulate_trade() reason -> section 13 close reason."""
    if sim_reason == "SL":
        return "SL"
    if sim_reason == "TP1+stop":
        return "BE"                     # TP1 taken, the rest stopped at breakeven
    if sim_reason.endswith("+stop"):
        return "TRAIL"                  # TP2+ taken, the rest stopped at the previous target
    if sim_reason.startswith("TP"):
        return sim_reason               # every target reached
    return {"time": "TIME", "exit-rule": "EXIT_RULE"}.get(sim_reason, sim_reason.upper())


def warnings(d, since, ct, flags, atr, reg_label, reg_at_entry, vol_x=2.0):
    """Section 16 checks that are NOT exits (never tested in the backtest): shown as 'watch: ...'.
    d: +1/-1; since: close time (ms) of the entry candle; ct: close times of the trigger timeframe;
    flags: {'bos_up','bos_down','choch_up','choch_down','disp_up','disp_down'} arrays; atr: ATR array;
    reg_label: regime label now; reg_at_entry: regime label at the signal."""
    out = []
    k = np.flatnonzero(np.asarray(ct) > since)
    if len(k):
        against = "down" if d == 1 else "up"
        if flags[f"choch_{against}"][k].any() or flags[f"bos_{against}"][k].any():
            out.append("opposing structure break (MSS/CHoCH/BOS)")
        if flags[f"disp_{against}"][k].any():
            out.append("opposing displacement candle")
        a0 = atr[max(k[0] - 1, 0)]
        if np.isfinite(a0) and a0 > 0 and np.isfinite(atr[-1]) and atr[-1] >= vol_x * a0:
            out.append(f"volatility spike (ATR {atr[-1] / a0:.1f}x since entry)")
    if reg_label and reg_at_entry and reg_label != reg_at_entry:
        out.append(f"regime changed {reg_at_entry} -> {reg_label}")
    return out


def next_action(state, warn):
    base = "HOLD - stop at breakeven" if state == TP1_HIT else "HOLD"
    return base + (" · watch: " + "; ".join(warn) if warn else "")


def open_r(d, entry, stop, price):
    """Unrealised result of the whole position in R at `price` (before costs); stop = the ORIGINAL stop."""
    R = abs(entry - stop)
    return d * (price - entry) / R if R > 0 else 0.0


def _fmt(x):
    x = float(x)
    return f"{x:,.2f}" if x >= 1000 else f"{x:,.4f}" if x >= 1 else f"{x:.6g}"


def build(logdf, now, prices=None, limits=None):
    """The position book (section 16) from the signals log. prices: {(coin, tf) or coin: newest close}, for
    the open R (read on the timeframe the position is managed on).
    APPROVED rows are real positions (Active); PAPER_TRADING / VALIDATION rows are the paper record."""
    prices = prices or {}
    rows = [] if logdf is None or logdf.empty else logdf.to_dict("records")
    today = now.strftime("%Y-%m-%d")
    week0 = (now - dt.timedelta(days=now.weekday())).strftime("%Y-%m-%d")   # Monday of this week (UTC)
    active, paper, awaiting, closed = [], [], [], []
    day_r = week_r = paper_day_r = 0.0
    for r in rows:
        st, live = row_state(r), r.get("stage") == "APPROVED"
        d = 1 if r["direction"] == "LONG" else -1
        item = dict(id=r["id"], coin=r["coin"], direction=r["direction"], tf=r["tf"], strategy=r["strategy"],
                    version=str(r.get("version") or "1.0"), stage=r.get("stage") or "", state=st)
        if st == AWAITING:
            item.update(bars=int(float(r.get("bars_5m") or 0)), trigger=r["signal_time_utc"])
            awaiting.append(item)
        elif st in (ACTIVE, TP1_HIT, TRIGGERED):
            stf = r.get("sim_tf") if isinstance(r.get("sim_tf"), str) and r.get("sim_tf") else r["tf"]
            px = prices.get((r["coin"], stf), prices.get(r["coin"]))
            cur = r.get("current_stop")
            item.update(entry=float(r["entry"]), stop=float(cur) if pd.notna(cur) and cur != "" else float(r["stop"]),
                        open_r=round(open_r(d, float(r["entry"]), float(r["stop"]), px), 2) if px else None,
                        next_action=r.get("next_action") if isinstance(r.get("next_action"), str) and r.get("next_action")
                        else next_action(st, []))
            (active if live else paper).append(item)
        closed_day = str(r.get("closed_time_utc") or "")[:10]
        if st in FINAL_STATES and st != NO_TRADE and closed_day == today:
            res = float(r["result_r"]) if pd.notna(r.get("result_r")) else None
            item.update(reason=r.get("close_reason") or r.get("status"), result_r=res, live=live)
            closed.append(item)
        if st == CLOSED and pd.notna(r.get("result_r")):
            res = float(r["result_r"])
            if live and closed_day == today:
                day_r += res
            if live and closed_day >= week0:
                week_r += res
            if not live and closed_day == today:
                paper_day_r += res
    return dict(utc=now.strftime("%Y-%m-%d %H:%M"), beijing=now.astimezone(BJ).strftime("%Y-%m-%d %H:%M"),
                active=active, awaiting=awaiting, paper=paper, closed_today=closed,
                day_r=round(day_r, 2), week_r=round(week_r, 2), paper_day_r=round(paper_day_r, 2),
                heat=len(active), limits=limits or LIMITS,
                empty=not (active or awaiting or paper or closed))


def lines(book, bars_5m=6, risk=None):
    """The book as text (section 16 layout) - the first thing in every report and email."""
    def pos(p):
        opr = "?" if p["open_r"] is None else f"{p['open_r']:+.2f}"
        return (f"{p['coin']} · {p['direction']} · {p['tf']} · {p['strategy']} v{p['version']} · entry {_fmt(p['entry'])}"
                f" · stop {_fmt(p['stop'])} · open {opr}R · {p['next_action']}")
    out = [f"POSITION BOOK — {book['utc']} UTC / {book['beijing']} Beijing"]
    if book["empty"]:
        out.append("No open or pending positions.")
    else:
        out.append("Active:    " + (" | ".join(pos(p) for p in book["active"]) or "none"))
        out.append("Awaiting:  " + (" | ".join(f"{p['coin']} · {p['direction']} · {p['tf']} · {p['strategy']} "
                                               f"({p['stage']}) · {p['bars']}/{bars_5m} 5m bars"
                                               for p in book["awaiting"]) or "none"))
        out.append("Paper:     " + (" | ".join(pos(p) + f" ({p['stage']})" for p in book["paper"]) or "none"))
        out.append("Closed:    " + (" | ".join(f"{p['coin']} {p['direction']} {p['tf']} {p['strategy']} {p['reason']}"
                                               + ("" if p["result_r"] is None else f" {p['result_r']:+.2f}R")
                                               + ("" if p["live"] else " (paper)")
                                               for p in book["closed_today"]) or "none"))
    L = book["limits"]
    out.append(f"Day: {book['day_r']:+.2f}R (limit {L['day_r']:g}R) · Week: {book['week_r']:+.2f}R "
               f"(limit {L['week_r']:g}R) · Heat: {book['heat']}/{L['heat']}"
               + (f" · paper today {book['paper_day_r']:+.2f}R" if book["paper_day_r"] else ""))
    if risk is not None:
        out.append("Risk:      " + ("; ".join(risk["halts_text"] + [f"SUSPENDED {k}" for k in risk["suspended"]])
                                    or "no halt") + f" · risk per trade {risk['risk_pct']:g}%"
                   + (" · NEXT EVENT " + risk["next_event"] if risk.get("next_event") else "")
                   + (" · ⚠ " + risk["calendar_warning"] if risk.get("calendar_warning") else ""))
    return out
