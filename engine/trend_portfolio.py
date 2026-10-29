"""
Trend portfolio (2026-10-29, operator: "build trend portfolio") - PAPER ONLY until the operator decides otherwise.

The idea (after Zarattini, Pagani & Barbon 2025, "Catching Crypto Trends", SSRN 5209907; our own version - their exact
rules were not verified): on DAILY candles, each of the operator's coins has 9 trend signals, one per lookback
(5 / 10 / 20 / 30 / 60 / 90 / 150 / 250 / 360 days). A signal turns ON at a daily close above the highest high of its
lookback, and OFF at a close below its ratcheting mid-line ((highest high + lowest low) / 2 of the lookback, never
lowered while ON). The coin's target = the share of its 9 signals that are ON (6 of 9 = 67% of that coin's part of
the account). Long only, no leverage, every coin gets an equal part. Decided at the daily close (00:00 UTC = 08:00
Beijing), held the next day.

Measured 2026-10-29 (Binance daily since 2018, the 7 own coins, 0.10% a side on every change + funding 0.01% / 8 h on
what is held): about 35% a year, Sharpe 1.40, worst drop 26% (buy and hold: 36%, 0.81, 75%); 2018 +1%, 2022 -11%.
Other lookback sets 1.30-1.40, costs doubled 1.36. Without ZEC 2025 was -4% and 2026 -6%: it earns in big trends.

The paper account starts with paper_capital on its first day and follows every target change after costs - the same
arithmetic as the backtest. Pure functions: no internet, no files.
"""
import math

import numpy as np
import pandas as pd

DEFAULTS = dict(enabled=True, telegram=True, lookbacks=(5, 10, 20, 30, 60, 90, 150, 250, 360), paper_capital=1000.0,
                side_cost_pct=0.10, funding_pct_per_8h=0.01)
DAY_MS = 86_400_000


def settings(section, costs=None):
    """section: config.yaml -> trend_portfolio; costs: config.yaml -> costs.long (taker + slippage a side, funding)."""
    s = dict(DEFAULTS)
    if costs:
        s["side_cost_pct"] = float(costs.get("taker_fee_pct", 0.05)) + float(costs.get("slippage_pct", 0.05))
        s["funding_pct_per_8h"] = float(costs.get("funding_pct_per_8h", 0.01))
    s.update({k: v for k, v in (section or {}).items() if k in DEFAULTS})
    s["lookbacks"] = [int(x) for x in s["lookbacks"]]
    s["paper_capital"], s["side_cost_pct"] = float(s["paper_capital"]), float(s["side_cost_pct"])
    s["funding_pct_per_8h"] = float(s["funding_pct_per_8h"])
    s["enabled"], s["telegram"] = bool(s["enabled"]), bool(s["telegram"])
    return s


def signal_states(high, low, close, L):
    """1 / 0 per daily candle: the lookback-L trend signal at that close (ON at a close above the highest high of the
    L candles before; OFF at a close below the ratcheting mid-line). Unknown (not enough candles yet) = 0."""
    h, l, c = (np.asarray(x, dtype=float) for x in (high, low, close))
    hh = pd.Series(h).rolling(L, min_periods=L).max().shift().to_numpy()
    ll = pd.Series(l).rolling(L, min_periods=L).min().shift().to_numpy()
    on, pos, stop = np.zeros(len(c)), 0, math.nan
    for i in range(len(c)):
        if math.isnan(hh[i]):
            continue
        mid = (hh[i] + ll[i]) / 2
        if pos == 0 and c[i] > hh[i]:
            pos, stop = 1, mid
        elif pos == 1:
            stop = max(stop, mid)
            if c[i] < stop:
                pos = 0
        on[i] = pos
    return on


def targets(daily, S):
    """daily: DataFrame of closed daily candles (open_time, high, low, close), oldest first. Returns DataFrame
    (open_time, close, on = signals ON, n, weight = on / n) per candle."""
    states = np.vstack([signal_states(daily["high"], daily["low"], daily["close"], L) for L in S["lookbacks"]])
    n = len(S["lookbacks"])
    on = states.sum(axis=0)
    return pd.DataFrame(dict(open_time=daily["open_time"].to_numpy(dtype=np.int64), close=daily["close"].to_numpy(float),
                             on=on.astype(int), n=n, weight=on / n,
                             longest_on=[max([L for L, s in zip(S["lookbacks"], states[:, i]) if s] or [0])
                                         for i in range(states.shape[1])]))


def day_return(prev_w, new_w, ret, S, coins=None):
    """One day of the paper account (fractions): the weights held over the day (prev_w, decided at yesterday's close)
    earn the coins' returns; changing to new_w at today's close costs side_cost on the change; funding is charged on
    what was held. Every coin of `coins` is an equal part; a coin without a price that day (not listed yet) is cash."""
    coins = sorted(coins or (set(prev_w) | set(new_w) | set(ret)))
    side, fund = S["side_cost_pct"] / 100, S["funding_pct_per_8h"] / 100 * 3
    parts = []
    for c in coins:
        w0, w1, r = float(prev_w.get(c, 0.0)), float(new_w.get(c, 0.0)), ret.get(c)
        earn = w0 * r if r is not None and r == r else 0.0
        parts.append(earn - abs(w1 - w0) * side - w0 * fund)
    return float(np.mean(parts)) if parts else 0.0


def update(prev, frames, S, now_ms):
    """The new state of the portfolio from yesterday's state (prev, or None on the first day) and every coin's closed
    daily candles (frames = {coin: DataFrame}). Each new closed day since prev['day'] is booked in order, so a missed
    day is caught up. Returns the state dict (see reports/trend_portfolio.json)."""
    tg = {c: targets(d, S) for c, d in frames.items() if d is not None and len(d)}
    days = sorted({int(t) for d in tg.values() for t in d["open_time"]})
    if not days:
        return prev
    by = {c: d.set_index("open_time") for c, d in tg.items()}
    st = dict(prev or {})
    hist = list(st.get("history") or [])
    last = st.get("day_ms")
    todo = [d for d in days if last is None or d > int(last)]
    if last is None:
        todo = todo[-1:]                               # the first run starts the paper account on the newest day
    w_prev = dict(st.get("weights") or {})
    equity = float(st.get("equity", S["paper_capital"]))
    for d in todo:
        new_w, ret = {}, {}
        for c, x in by.items():
            if d in x.index:
                new_w[c] = float(x.at[d, "weight"])
                prev_day = x.index[x.index < d]
                if len(prev_day) and prev_day[-1] == d - DAY_MS:
                    ret[c] = float(x.at[d, "close"] / x.at[prev_day[-1], "close"] - 1)
            else:
                new_w[c] = float(w_prev.get(c, 0.0))    # no candle that day: unchanged
        r = day_return(w_prev, new_w, ret, S, list(by))   # the first day (nothing held yet): only the buying in
        equity *= 1 + r
        hist.append(dict(day=pd.to_datetime(d, unit="ms").strftime("%Y-%m-%d"), equity=round(equity, 2),
                         ret_pct=round(r * 100, 3), weights={c: round(w, 4) for c, w in sorted(new_w.items())}))
        w_prev, last = new_w, d
    day = int(last)
    coins = {}
    for c, x in sorted(by.items()):
        if day not in x.index:
            continue
        row, before = x.loc[day], x[x.index < day]
        y = float(before["weight"].iloc[-1]) if len(before) else 0.0
        part = equity / max(1, len(by))
        coins[c] = dict(on=int(row["on"]), n=int(row["n"]), weight=round(float(row["weight"]), 4),
                        yesterday=round(y, 4), price=float(row["close"]), usd=round(part * float(row["weight"]), 2),
                        change_usd=round(part * (float(row["weight"]) - y), 2), longest_on=int(row["longest_on"]))
    invested = sum(x["usd"] for x in coins.values())
    return dict(st, version=1, day_ms=day, day=pd.to_datetime(day, unit="ms").strftime("%Y-%m-%d"),
                updated_utc=pd.to_datetime(now_ms, unit="ms").strftime("%Y-%m-%d %H:%M"),
                started=st.get("started") or hist[0]["day"], start_capital=S["paper_capital"],
                equity=round(equity, 2), invested_usd=round(invested, 2),
                weights={c: x["weight"] for c, x in coins.items()}, coins=coins, history=hist[-1000:],
                lookbacks=S["lookbacks"])


def backtest(frames, S, since=None):
    """The same rules over the candles given (each new day booked as in update): yearly return, Sharpe, worst drop of
    the portfolio and of holding the same coins in equal parts. since: 'YYYY-MM-DD' (optional)."""
    tg = {c: targets(d, S).set_index("open_time") for c, d in frames.items() if d is not None and len(d)}
    days = sorted({int(t) for d in tg.values() for t in d.index})
    if since:
        cut = int(pd.Timestamp(since).value // 10**6)
        days = [d for d in days if d >= cut]
    rp, rh, w_prev = [], [], {}
    for d in days:
        new_w, ret = {}, {}
        for c, x in tg.items():
            if d in x.index:
                new_w[c] = float(x.at[d, "weight"])
                if d - DAY_MS in x.index:
                    ret[c] = float(x.at[d, "close"] / x.at[d - DAY_MS, "close"] - 1)
        rp.append(day_return(w_prev, new_w, ret, S, list(tg)))
        rh.append(float(np.mean([ret.get(c, 0.0) for c in tg])) if tg else 0.0)
        w_prev = new_w

    def summary(r):
        r = np.asarray(r, dtype=float)
        if len(r) < 30:
            return None
        eq = np.cumprod(1 + r)
        yrs = len(r) / 365
        return dict(cagr_pct=round((eq[-1] ** (1 / yrs) - 1) * 100, 1),
                    sharpe=round(float(r.mean() / r.std() * math.sqrt(365)), 2) if r.std() > 0 else None,
                    max_dd_pct=round(float(np.max(1 - eq / np.maximum.accumulate(eq))) * 100, 1))
    first = pd.to_datetime(days[0], unit="ms").strftime("%Y-%m-%d") if days else None
    return dict(since=first, days=len(days), portfolio=summary(rp), hold=summary(rh))


def _usd(v):
    return f"${v:,.0f}" if abs(v) >= 10 else f"${v:,.2f}"


def telegram_text(st):
    """The daily Telegram message (HTML)."""
    if not st or not st.get("coins"):
        return "📊 Trend portfolio: no data yet - GitHub's hourly scan writes it after the daily close (08:00 Beijing)."
    lines = [f"📊 <b>Trend portfolio</b> (PAPER) · {st['day']} daily close",
             "Target for each coin = how many of its 9 trends are up (one equal part of the account each):"]
    for c, x in st["coins"].items():
        bar = "🟩" * x["on"] + "⬜" * (x["n"] - x["on"])
        lines.append(f"• <b>{c}</b> {x['weight'] * 100:.0f}% in ({x['on']}/{x['n']}) {bar} · {_usd(x['usd'])}")
    ch = [(c, x) for c, x in st["coins"].items() if abs(x["weight"] - x["yesterday"]) > 1e-9]
    if len(st.get("history") or []) <= 1:
        lines.append("🆕 First day of the paper account: these targets are its starting positions.")
    elif ch:
        lines.append("Changes today:")
        for c, x in ch:
            act = "buy" if x["change_usd"] > 0 else "sell"
            qty = abs(x["change_usd"]) / x["price"] if x["price"] else 0
            lines.append(f"  {'🟢' if act == 'buy' else '🔴'} {c} {x['yesterday'] * 100:.0f}% → {x['weight'] * 100:.0f}%: "
                         f"{act} {_usd(abs(x['change_usd']))} (~{qty:.4g} {c})")
    else:
        lines.append("No changes today - hold.")
    gain = (st["equity"] / st["start_capital"] - 1) * 100
    lines.append(f"Paper account: <b>{_usd(st['equity'])}</b> ({gain:+.1f}% since {st['started']}) · invested "
                 f"{_usd(st['invested_usd'])}, cash {_usd(st['equity'] - st['invested_usd'])}")
    bt = st.get("backtest") or {}
    if bt.get("portfolio") and bt.get("hold"):
        p, h = bt["portfolio"], bt["hold"]
        lines.append(f"Backtest since {bt['since']}: {p['cagr_pct']:+.0f}% a year, worst drop {p['max_dd_pct']:.0f}% "
                     f"(holding: {h['cagr_pct']:+.0f}% a year, worst drop {h['max_dd_pct']:.0f}%)")
    lines.append("<i>Paper only - practice. Long only, no leverage. /portfolio any time, /portfolio off to stop "
                 "this message.</i>")
    return "\n".join(lines)


def markdown(st):
    """reports/trend_portfolio.md."""
    if not st or not st.get("coins"):
        return "# Trend portfolio (paper)\n\nNo data yet.\n"
    out = ["# Trend portfolio (paper)", "",
           f"Daily close {st['day']} (updated {st['updated_utc']} UTC). 9 trend signals per coin (lookbacks "
           f"{', '.join(str(x) for x in st['lookbacks'])} days): ON at a close above the lookback's high, OFF below its "
           "ratcheting mid-line. Target = the share ON. Long only, no leverage, equal parts. Paper only "
           "(`docs/TREND_PORTFOLIO.md`).", "",
           "| Coin | Trends up | Target | Yesterday | Paper position | Change today | Price |",
           "|---|---|---:|---:|---:|---:|---:|"]
    for c, x in st["coins"].items():
        out.append(f"| {c} | {x['on']}/{x['n']} | {x['weight'] * 100:.0f}% | {x['yesterday'] * 100:.0f}% | {_usd(x['usd'])} | "
                   f"{'+' if x['change_usd'] > 0 else ''}{_usd(x['change_usd']) if x['change_usd'] else '-'} | {x['price']:,.6g} |")
    gain = (st["equity"] / st["start_capital"] - 1) * 100
    out += ["", f"**Paper account: {_usd(st['equity'])}** ({gain:+.2f}% since {st['started']}, start "
                f"{_usd(st['start_capital'])}) · invested {_usd(st['invested_usd'])}.", ""]
    bt = st.get("backtest") or {}
    if bt.get("portfolio") and bt.get("hold"):
        p, h = bt["portfolio"], bt["hold"]
        out += [f"Backtest on the candles the scan has (since {bt['since']}, {bt['days']} days, costs included): "
                f"portfolio {p['cagr_pct']:+.1f}% a year, Sharpe {p['sharpe']}, worst drop {p['max_dd_pct']:.1f}% · "
                f"holding the same coins {h['cagr_pct']:+.1f}% a year, Sharpe {h['sharpe']}, worst drop "
                f"{h['max_dd_pct']:.1f}%.", ""]
    out += ["## Paper account, last 30 days", "", "| Day | Account | Day's result |", "|---|---:|---:|"]
    out += [f"| {h['day']} | {_usd(h['equity'])} | {h['ret_pct']:+.2f}% |" for h in (st.get("history") or [])[-30:][::-1]]
    return "\n".join(out) + "\n"
