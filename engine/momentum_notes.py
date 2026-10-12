"""
🌊 Momentum notes (strategy 11, operator request 2026-10-13): where a market-wide move stands, in three plain notes.
INFORMATION ONLY - never a trade signal, gate, size or approval; strategy 11's own versions (strategies_program.yaml,
P11-MOMENTUM-*) send the 🔵 TEST trade alerts once their 5-year backtest is positive on a coin.

The operator: "get a watch alert when the move is forming ... don't tell me to short when the market has almost
finished falling, the market goes up because it has already gone down." So the live watcher tells the three phases
of a move apart:
  👀 forming   (every 15m close) the coin's 15m price is pressing on its 30m 20-candle low (high) - within near_atr x
               the 30m ATR, the 30m close not through it yet - with rising 15m volume, the 1H already moving that way
               (scanner.momentum_1h) and the 4H not in a STRONG trend against it, while at least min_coins coins do
               the same (or already broke): a market-wide break may come at the next 30m close.
  ⚠️ late      (30m close) a 30m break that is already stretched: the 3rd step or later (steps_dn / steps_up),
               RSI(14) beyond 30 / 70, or more than late_ext ATR from the 30m EMA20 - no new trade that way; protect
               open profits.
  🔄 bounce    (30m close, after a ⚠️ late note on that coin in the last bounce_hours) the 30m close crosses back over
               its EMA20: the stretched move may be over. A bounce trade is NOT tested - this only says "careful".
At most max_per_day notes a Beijing day; one forming note per coin and direction in forming_cooldown_min, one late note
in late_cooldown_min, one bounce note per late note. /momentum on|off in Telegram; never while paused.
Pure functions only: no internet, no files.
"""
import math

import numpy as np

DEFAULTS = dict(enabled=True, near_atr=0.3, vol_x=1.2, min_coins=2, late_step=3, late_rsi=30.0, late_ext=2.5,
                bounce_hours=12, max_per_day=12, forming_cooldown_min=120, late_cooldown_min=240)
SIDE = {1: "LONG", -1: "SHORT"}


def settings(raw):
    s = dict(DEFAULTS)
    s.update({k: v for k, v in (raw or {}).items() if k in DEFAULTS})
    for k in ("min_coins", "late_step", "bounce_hours", "max_per_day", "forming_cooldown_min", "late_cooldown_min"):
        s[k] = int(s[k])
    for k in ("near_atr", "vol_x", "late_rsi", "late_ext"):
        s[k] = float(s[k])
    s["enabled"] = bool(s["enabled"])
    return s


def _f(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _last(series):
    a = np.asarray(series, dtype=float)
    return _f(a[-1]) if len(a) else None


def coin_state(pc):
    """The numbers the notes need from one prepared coin (scanner.prepare_coin): the newest closed 30m candle and
    the newest closed 15m candle. None when the 30m frame is missing."""
    f30 = (pc.get("frames") or {}).get("30m")
    if f30 is None or f30["n"] < 60:
        return None
    ns, df = f30["ns"], f30["df"]
    c, h, l = ns["close"], ns["high"], ns["low"]
    ema = ns["ema"](c, 20)
    atr = ns["atr"](14)
    reg = f30.get("reg") or {}
    mom = reg.get("1h_mom", ([None],))[0]
    h4 = reg.get("4h", ([None],))[0]
    st = dict(close_ms=int(df["close_time"].iloc[-1]), close=_last(c), prev_close=_f(c.iloc[-2]),
              ema=_last(ema), prev_ema=_f(ema.iloc[-2]), atr=_last(atr), rsi=_last(ns["rsi"](c, 14)),
              low20=_last(ns["lowest"](l, 20)), high20=_last(ns["highest"](h, 20)),
              brk_dn=bool(c.iloc[-1] < ns["lowest"](l, 20).shift(1).iloc[-1]),
              brk_up=bool(c.iloc[-1] > ns["highest"](h, 20).shift(1).iloc[-1]),
              step_dn=_last(ns["steps_dn"](20, 3, 24)), step_up=_last(ns["steps_up"](20, 3, 24)),
              high24=_last(ns["highest"](h, 48)), low24=_last(ns["lowest"](l, 48)),
              mom=mom[-1] if len(mom) else None, h4=h4[-1] if len(h4) else None)
    f15 = (pc.get("frames") or {}).get("15m")
    if f15 is not None and f15["n"] >= 30:
        n15 = f15["ns"]
        v, vs = n15["volume"], n15["vol_sma"](20)
        st.update(m15_ms=int(f15["df"]["close_time"].iloc[-1]), m15_close=_last(n15["close"]),
                  m15_vol_x=_f(v.iloc[-1] / vs.shift(1).iloc[-1]) if _f(vs.shift(1).iloc[-1]) else None)
    return st


def _allowed(st, d):
    """The 1H already moves that way and the 4H is not in a STRONG trend against it (the strategy 11 gate)."""
    return st.get("mom") == ("DOWN" if d == -1 else "UP") and st.get("h4") != ("STRONG_BULL" if d == -1 else "STRONG_BEAR")


def forming(st, d, S):
    """The 15m price presses on the 30m 20-candle low (d=-1) / high (d=1), not broken yet at the 30m close, with
    rising 15m volume, under the strategy 11 gate. Returns the level or None."""
    if not st or not _allowed(st, d) or st.get("m15_close") is None or not st.get("atr"):
        return None
    lvl = st["low20"] if d == -1 else st["high20"]
    if lvl is None or (st["brk_dn"] if d == -1 else st["brk_up"]):
        return None
    gap = d * (lvl - st["m15_close"])          # how far the 15m price still is from the level (negative = through it)
    if gap > S["near_atr"] * st["atr"] or (st.get("m15_vol_x") or 0) < S["vol_x"]:
        return None
    return lvl


def late(st, d, S):
    """A 30m break that is already stretched (step >= late_step, RSI beyond late_rsi, or more than late_ext ATR from
    the EMA20) under the strategy 11 gate. Returns [reasons] or []."""
    if not st or not (st["brk_dn"] if d == -1 else st["brk_up"]) or not _allowed(st, d):
        return []
    why = []
    step = st["step_dn"] if d == -1 else st["step_up"]
    if step is not None and step >= S["late_step"]:
        why.append(f"{_nth(int(step))} {'breakdown' if d == -1 else 'breakout'} in 12 hours")
    rsi = st.get("rsi")
    if rsi is not None and (rsi < S["late_rsi"] if d == -1 else rsi > 100 - S["late_rsi"]):
        why.append(f"RSI {rsi:.0f} ({'oversold' if d == -1 else 'overbought'})")
    if st.get("atr") and st.get("ema") is not None:
        ext = d * (st["close"] - st["ema"]) / st["atr"]
        if ext > S["late_ext"]:
            why.append(f"{ext:.1f} ATR {'below' if d == -1 else 'above'} the 30m average")
    return why


def bounce(st, d):
    """After a stretched move in direction d, the 30m close crossed back over its EMA20 (a fall: back above it)."""
    if not st or None in (st.get("close"), st.get("ema"), st.get("prev_close"), st.get("prev_ema")):
        return False
    if d == -1:
        return st["close"] > st["ema"] and st["prev_close"] <= st["prev_ema"]
    return st["close"] < st["ema"] and st["prev_close"] >= st["prev_ema"]


def _nth(k):
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(k, f"{k}th")


def _p(x):
    return f"{x:,.6g}" if x is not None else "-"


def move_pct(st, d):
    """How far the coin already moved from the 24-hour high (a fall) / low (a rally), in %."""
    ref = st.get("high24") if d == -1 else st.get("low24")
    return None if not ref else (st["close"] / ref - 1) * 100


def plan(states, now_ms, closed, sent, S):
    """Which notes to send now. states: {coin: coin_state}; closed: the timeframes that just closed; sent: the notes
    state {'kind|coin|d': ms}. Returns [dict(kind, coin, d, key, text)] - the caller records and caps them."""
    out = []
    if "15m" in closed:
        groups = {}
        for d in (-1, 1):
            hits = {c: forming(st, d, S) for c, st in states.items()}
            hits = {c: v for c, v in hits.items() if v is not None}
            broke = [c for c, st in states.items() if st and (st["brk_dn"] if d == -1 else st["brk_up"])]
            groups[d] = (hits, broke)
        for d, (hits, broke) in groups.items():
            if len(set(hits) | set(broke)) < S["min_coins"]:
                continue
            for c, lvl in sorted(hits.items()):
                key = f"forming|{c}|{d}"
                if key in sent and now_ms - int(sent[key]) < S["forming_cooldown_min"] * 60_000:
                    continue
                st = states[c]
                others = sorted((set(hits) | set(broke)) - {c})
                out.append(dict(kind="forming", coin=c, d=d, key=key, text=forming_text(c, d, st, lvl, others)))
    if "30m" in closed:
        for c, st in sorted(states.items()):
            for d in (-1, 1):
                why = late(st, d, S)
                key = f"late|{c}|{d}"
                if why and not (key in sent and now_ms - int(sent[key]) < S["late_cooldown_min"] * 60_000):
                    out.append(dict(kind="late", coin=c, d=d, key=key, text=late_text(c, d, st, why)))
                bk = sent.get(f"bounce|{c}|{d}")
                if key in sent and now_ms - int(sent[key]) <= S["bounce_hours"] * 3_600_000 and \
                        (bk is None or int(bk) < int(sent[key])) and bounce(st, d):
                    out.append(dict(kind="bounce", coin=c, d=d, key=f"bounce|{c}|{d}", text=bounce_text(c, d, st)))
    return out


def forming_text(coin, d, st, lvl, others):
    word = "breakdown" if d == -1 else "breakout"
    away = abs(st["m15_close"] / lvl - 1) * 100
    return "\n".join([
        f"👀 <b>{coin} - {word} forming</b> (30m)",
        f"Price {_p(st['m15_close'])} is {away:.2f}% from the 30m {'support' if d == -1 else 'resistance'} "
        f"{_p(lvl)} · 15m volume {st.get('m15_vol_x') or 0:.1f}x · 1H {'falling' if d == -1 else 'rising'}",
        "Same on " + (", ".join(others) if others else "-") + " - a market-wide move may start at the next 30m close.",
        f"Watch the next 30m close {'below' if d == -1 else 'above'} {_p(lvl)}. A 🔵 strategy 11 alert comes only if "
        "the break happens and the version is positive in its backtest.",
        "<i>Information only - not a trade signal. /momentum off stops these notes.</i>"])


def late_text(coin, d, st, why):
    mv = move_pct(st, d)
    side = "short" if d == -1 else "long"
    return "\n".join([
        f"⚠️ <b>{coin} - late {'fall' if d == -1 else 'rally'}</b> (30m)",
        f"{'Down' if d == -1 else 'Up'} {abs(mv):.1f}% from the 24-hour {'high' if d == -1 else 'low'}"
        if mv is not None else f"Price {_p(st['close'])}",
        "Stretched: " + "; ".join(why) + ".",
        f"<b>No new {side} now</b> - this is where moves often bounce. Already {side}: take profit or tighten "
        "your stop.",
        "<i>Information only. /momentum off stops these notes.</i>"])


def bounce_text(coin, d, st):
    return "\n".join([
        f"🔄 <b>{coin} - bounce after the {'fall' if d == -1 else 'rally'}</b> (30m)",
        f"The 30m close {_p(st['close'])} is back {'above' if d == -1 else 'below'} its average {_p(st['ema'])}: the "
        f"stretched {'fall' if d == -1 else 'rally'} may be over.",
        f"Shorts: protect profits. A bounce {'long' if d == -1 else 'short'} is NOT a tested strategy - wait for a "
        "🔵 alert. If price turns back down at the average, strategy 11's retest version (V4) may alert."
        if d == -1 else
        f"Longs: protect profits. A bounce short is NOT a tested strategy - wait for a 🔵 alert. If price turns back "
        "up at the average, strategy 11's retest version (V4) may alert.",
        "<i>Information only. /momentum off stops these notes.</i>"])
