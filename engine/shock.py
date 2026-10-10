"""
Shock alarm (operator request 2026-10-10: "if the market falls or rallies suddenly, tell me while it happens").

The strategies look at the market only when a candle closes. The live watcher now also checks every minute, on OKX's
closed 1-minute candles, whether something unusual is happening, and sends a short ⚡ Telegram note:

  fast move     the last 15 minutes moved more than 1.8x the coin's normal 1-hour range (ATR of the 1H candles)
  volume spike  the last 15 minutes traded 5x the normal volume, with a real move (1.2x the 1H range)
  sweep         price broke yesterday's high or low (UTC day = the day that starts 08:00 Beijing) during a move of 1x the
                1H range, the first time today

One note for all the coins that fire in the same minute; one note per coin in 30 minutes; the coins of a market-wide move
are one wave (15 minutes, a new note only when 2+ more coins join); at most 8 notes a day. Tuned on a 14-day replay of
real OKX candles (27 Sep - 10 Oct 2026): ~3 notes a day, at most 7, one note at the start of the 7 Oct crash.

INFORMATION ONLY: never a trade signal, gate, size or approval, and it never touches a strategy or a test. Every shock
is logged with what price did 1 and 4 hours later, and whether a strategy alert followed, for the Sunday review.

Pure functions: no internet, no files. live_watcher.py fetches the candles, sends and logs.
"""
import datetime as dt
import html

import numpy as np

BJ = dt.timezone(dt.timedelta(hours=8))
DAY = 86_400_000
H = 3_600_000
M = 60_000

DEFAULTS = dict(
    enabled=True,
    window_min=15,          # the move is measured over the last 15 closed 1-minute candles
    move_atr=1.8,           # fast move: |move| >= 1.8 x ATR(14) of the 1H candles ...
    min_move_pct=0.0,       # ... and at least this many % (0 = no floor)
    atr_n=14,
    vol_x=5.0,              # volume spike: 15-minute volume >= 5x the normal 15 minutes ...
    vol_move_atr=1.2,       # ... with a move of at least 1.2 x ATR (volume without a move is mostly noise)
    vol_base_min=240,       # the normal volume: the 4 hours before the window
    sweep=True,             # yesterday's high / low broken, the first time today (once per side and day)
    sweep_min_atr=0.1,      # ... by at least 0.1 x ATR (a 1-tick poke is not a sweep) ...
    sweep_move_atr=1.0,     # ... during a move of at least 1 x ATR
    wave_min=15,             # same-direction shocks within this many minutes of a note = the same wave (logged only) ...
    wave_spread=2,          # ... unless at least 2 coins new to the wave join it (the move is spreading: a new note)
    cooldown_min=30,        # one note per coin in 30 minutes ...
    escalate_x=2.0,         # ... unless the same-direction move has grown to 2x the one in the last note
    max_per_day=8,          # at most 8 notes a Beijing day (the rest are only logged)
    check_delay_s=5,        # seconds after each minute (OKX finalises the 1-minute candle)
    outcome_hours=4,        # the log row is written 4 hours later, with the 1h / 4h result
)
TRIGGER_NAMES = dict(move="fast move", volume="volume spike", sweep_high="broke yesterday's high",
                     sweep_low="broke yesterday's low")


def settings(section):
    s = dict(DEFAULTS)
    s.update({k: v for k, v in (section or {}).items() if k in DEFAULTS})
    return s


def atr(h1, n=14):
    """Average true range of the newest n closed 1H candles (dict of arrays high / low / close), or None."""
    hi, lo, cl = (np.asarray(h1[k], dtype=float) for k in ("high", "low", "close"))
    if len(cl) < n + 1:
        return None
    tr = np.maximum(hi[1:] - lo[1:], np.maximum(abs(hi[1:] - cl[:-1]), abs(lo[1:] - cl[:-1])))
    a = float(tr[-n:].mean())
    return a if a > 0 else None


def context(h1, start_ms, n=14):
    """What a window starting at start_ms is compared with, from closed 1H candles (arrays open_time / high / low /
    close, ascending): the ATR, yesterday's high / low (the UTC day before start_ms's day) and today's high / low
    before the window (from the 1H candles closed by then). None when there are too few candles."""
    ot = np.asarray(h1["open_time"], dtype=np.int64)
    done = ot + H <= start_ms
    if done.sum() < n + 1:
        return None
    sub = {k: np.asarray(h1[k], dtype=float)[done] for k in ("high", "low", "close")}
    day0 = start_ms // DAY * DAY
    y = done & (ot >= day0 - DAY) & (ot < day0)
    t = done & (ot >= day0)
    hi, lo = np.asarray(h1["high"], dtype=float), np.asarray(h1["low"], dtype=float)
    return dict(atr=atr(sub, n), day0=day0,
                y_hi=float(hi[y].max()) if y.any() else None, y_lo=float(lo[y].min()) if y.any() else None,
                t_hi=float(hi[t].max()) if t.any() else None, t_lo=float(lo[t].min()) if t.any() else None,
                h1_end=int(ot[done][-1] + H))


def measure(m1, i, ctx, S):
    """The shock checks on the window of 1-minute candles ending before index i (m1: arrays open_time, open, high,
    low, close, volume - closed candles, ascending, one a minute). ctx: context(). Returns dict(d, move_pct,
    move_atr, vol_x, triggers, price, level, ms) - triggers empty when nothing fired - or None (too little data)."""
    W = int(S["window_min"])
    if ctx is None or not ctx.get("atr") or i < W + 1:
        return None
    ot = m1["open_time"]
    j = i - W
    if int(ot[i - 1]) - int(ot[j]) > W * M:                          # 2+ missing minutes: skip, never guess
        return None
    start, last = float(m1["open"][j]), float(m1["close"][i - 1])
    move = last - start
    a = ctx["atr"]
    out = dict(d=1 if move >= 0 else -1, move_pct=round((last / start - 1) * 100, 2), move_atr=round(move / a, 2),
               vol_x=None, triggers=[], price=last, level=None, ms=int(ot[i - 1]) + M, start=start, atr=a)
    big = abs(move) >= S["move_atr"] * a and abs(out["move_pct"]) >= S["min_move_pct"]
    if big:
        out["triggers"].append("move")
    b0 = max(0, j - int(S["vol_base_min"]))
    base = m1["volume"][b0:j]
    if len(base) >= W * 4 and float(np.sum(base)) > 0:
        vx = float(np.sum(m1["volume"][j:i])) / (float(np.mean(base)) * W)
        out["vol_x"] = round(vx, 1)
        if vx >= S["vol_x"] and abs(move) >= S["vol_move_atr"] * a:
            out["triggers"].append("volume")
    if S["sweep"] and ctx.get("y_hi") is not None:
        # today's extremes before the window: the closed 1H candles of today + the 1-minute candles after them
        k0 = int(np.searchsorted(ot, max(ctx["day0"], ctx["h1_end"])))
        pre_hi = [x for x in (ctx.get("t_hi"), float(m1["high"][k0:j].max()) if j > k0 else None) if x is not None]
        pre_lo = [x for x in (ctx.get("t_lo"), float(m1["low"][k0:j].min()) if j > k0 else None) if x is not None]
        whi, wlo = float(m1["high"][j:i].max()), float(m1["low"][j:i].min())
        gap = S["sweep_min_atr"] * a
        moving = abs(move) >= S["sweep_move_atr"] * a
        if moving and whi >= ctx["y_hi"] + gap and (not pre_hi or max(pre_hi) < ctx["y_hi"] + gap):
            out["triggers"].append("sweep_high")
            out["level"] = ctx["y_hi"]
        elif moving and wlo <= ctx["y_lo"] - gap and (not pre_lo or min(pre_lo) > ctx["y_lo"] - gap):
            out["triggers"].append("sweep_low")
            out["level"] = ctx["y_lo"]
        if out["triggers"] in (["sweep_high"], ["sweep_low"]):        # a sweep alone: its side is the direction
            out["d"] = 1 if out["triggers"][0] == "sweep_high" else -1
    return out


def sent_today(times, now_ms):
    day0 = int(dt.datetime.fromtimestamp(now_ms / 1000, BJ).replace(hour=0, minute=0, second=0, microsecond=0)
               .timestamp() * 1000)
    return sum(1 for t in times if int(t) >= day0)


def decide(found, st, now_ms, S):
    """Which shocks are news. found: {coin: measure() with triggers}. st: the watcher's state with keys shock_last
    {coin: [ms, d, move_atr]}, shock_swept {coin: "YYYY-MM-DD:H|L,..."}, shock_sent [ms]. Returns the new shocks (each
    with 'bigger' when it repeats inside the cooldown because the move doubled); updates shock_last / shock_swept.
    Repeats inside the cooldown are dropped silently (not news). The caller applies on/off, pause and the daily cap."""
    new = []
    day = dt.datetime.fromtimestamp(now_ms / 1000, dt.timezone.utc).strftime("%Y-%m-%d")
    for coin, f in sorted(found.items()):
        trig = list(f["triggers"])
        swept = st.setdefault("shock_swept", {}).get(coin, "")
        sides = set(swept.split(":")[1].split(",")) if swept.startswith(day + ":") else set()
        for t, side in (("sweep_high", "H"), ("sweep_low", "L")):
            if t in trig and side in sides:
                trig.remove(t)
        if not trig:
            continue
        for t, side in (("sweep_high", "H"), ("sweep_low", "L")):      # a side counts once a day, even in a cooldown
            if t in trig:
                sides.add(side)
        if sides:
            st["shock_swept"][coin] = day + ":" + ",".join(sorted(sides))
        last = st.setdefault("shock_last", {}).get(coin)
        bigger = False
        if last and now_ms - int(last[0]) < int(S["cooldown_min"]) * M:
            if not (int(last[1]) == f["d"] and abs(f["move_atr"]) >= S["escalate_x"] * max(abs(float(last[2])), 0.01)
                    and "move" in trig):
                continue
            bigger = True
        st["shock_last"][coin] = [now_ms, f["d"], f["move_atr"]]
        new.append(dict(f, coin=coin, triggers=trig, bigger=bigger))
    return new


def hold(new, st, now_ms, S):
    """Why a note with these new shocks is not sent, or None to send it: 'daily cap' (max_per_day notes this Beijing
    day) or 'same wave' (all in the direction of a note sent within wave_min minutes and fewer than wave_spread coins
    new to that wave: the coins of a market-wide move follow each other within minutes and the first note shows them
    all; a move that keeps growing gets its 'getting bigger' note after the wave). A held coin joins the wave. The
    caller checks on / off and the pause first, and records a sent note with sent()."""
    last = st.get("shock_wave")
    if last and now_ms - int(last[0]) < int(S["wave_min"]) * M and all(s["d"] == int(last[1]) for s in new):
        coins = set(last[2] if len(last) > 2 else [])
        if len({s["coin"] for s in new} - coins) < int(S["wave_spread"]):
            last[2:] = [sorted(coins | {s["coin"] for s in new})]
            return "same wave"
    if sent_today(st.get("shock_sent") or [], now_ms) >= int(S["max_per_day"]):
        return "daily cap"
    return None


def sent(new, st, now_ms):
    st.setdefault("shock_sent", []).append(now_ms)
    ds = {s["d"] for s in new}
    last = st.get("shock_wave")
    same = last and len(last) > 2 and now_ms - int(last[0]) < 60 * M and len(ds) == 1 and int(last[1]) in ds
    st["shock_wave"] = [now_ms, ds.pop() if len(ds) == 1 else 0,
                        sorted(set(last[2] if same else []) | {s["coin"] for s in new})]


def _px(x):
    return f"{x:,.2f}" if x >= 100 else f"{x:,.4f}" if x >= 1 else f"{x:.6f}"


def line(s):
    """One coin's line of the note."""
    arrow = "📈" if s["d"] == 1 else "📉"
    bits = [f"{s['move_pct']:+.1f}% in 15 min ({abs(s['move_atr']):.1f}x its normal 1H range)"]
    if s.get("vol_x") is not None and ("volume" in s["triggers"] or s["vol_x"] >= 2):
        bits.append(f"volume {s['vol_x']:.1f}x")
    if "sweep_high" in s["triggers"]:
        bits.append(f"broke yesterday's high {_px(s['level'])}")
    if "sweep_low" in s["triggers"]:
        bits.append(f"broke yesterday's low {_px(s['level'])}")
    return f"{arrow} <b>{html.escape(s['coin'])}</b> {_px(s['price'])} · " + " · ".join(bits) \
        + (" · <b>getting bigger</b>" if s.get("bigger") else "")


def text(shocks, others, open_trades, now_ms):
    """The ⚡ Telegram note. shocks: decide() rows to send; others: {coin: move_pct} of the coins that did not fire;
    open_trades: [(coin, d, label)] of the trades the operator follows."""
    when = dt.datetime.fromtimestamp(now_ms / 1000, BJ).strftime("%H:%M Beijing")
    L = [f"⚡ <b>Market shock</b> · {when}"] + [line(s) for s in shocks]
    if others:
        L.append("Others (15 min): " + " · ".join(f"{c} {p:+.1f}%" for c, p in sorted(others.items())))
    hit = {s["coin"] for s in shocks}
    for coin, d, label in open_trades:
        if coin in hit:
            L.append(f"⚠️ You follow a {'LONG' if d == 1 else 'SHORT'} on {html.escape(coin)}"
                     + (" (demo)" if label == "TEST" else "") + ": check its stop on OKX.")
    L.append("<i>Information only - not a trade signal. Your strategies check at their next candle close; "
             "never chase a shock.</i> /shock off to stop these notes.")
    return "\n".join(L)


def outcome(m5, ms, d, price, hours=4, bar_ms=5 * M):
    """What price did after a shock at ms: % change after 1h and after `hours`, and the largest move with / against
    the shock's direction meanwhile (all signed so that + = the shock kept going). m5: arrays open_time, high, low,
    close of closed candles of bar_ms (5m live). None when the candles do not reach ms + hours yet."""
    ot = np.asarray(m5["open_time"], dtype=np.int64)
    ct = ot + bar_ms
    if not len(ct) or ct[-1] < ms + hours * H:
        return None
    sel = (ot >= ms) & (ct <= ms + hours * H)
    if not sel.any():
        return None
    hi, lo, cl = (np.asarray(m5[k], dtype=float) for k in ("high", "low", "close"))

    def at(t):
        k = int(np.searchsorted(ct, t, side="right")) - 1
        return float(cl[k]) if k >= 0 else price
    pct = lambda x: round(d * (x / price - 1) * 100, 2)                 # noqa: E731
    return dict(after_1h=pct(at(ms + H)), after_4h=pct(at(ms + hours * H)),
                best=pct(float(hi[sel].max()) if d == 1 else float(lo[sel].min())),
                worst=pct(float(lo[sel].min()) if d == 1 else float(hi[sel].max())))


# ---------------------------------------------------------------- the log (journal/shocks.csv) and the weekly summary
COLS = ["time_utc", "coin", "side", "triggers", "move_pct", "move_atr", "vol_x", "level", "price", "sent",
        "after_1h_pct", "after_4h_pct", "best_pct", "worst_pct", "alerts_4h", "alerts_4h_same"]


def row(p, res, alerts):
    """A log row for a pending shock p (dict ms, coin, d, triggers, move_pct, move_atr, vol_x, level, price, sent),
    its outcome() res and the strategy alerts [(sent_ms, coin, d)] seen on that coin."""
    within = [a for a in alerts if a[1] == p["coin"] and p["ms"] <= int(a[0]) <= p["ms"] + 4 * H]
    res = res or {}
    return [dt.datetime.fromtimestamp(p["ms"] / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M"), p["coin"],
            "UP" if p["d"] == 1 else "DOWN", "+".join(p["triggers"]), p["move_pct"], p["move_atr"],
            "" if p.get("vol_x") is None else p["vol_x"], "" if p.get("level") is None else p["level"], p["price"],
            p["sent"], res.get("after_1h", ""), res.get("after_4h", ""), res.get("best", ""), res.get("worst", ""),
            len(within), sum(1 for a in within if int(a[2]) == p["d"])]


def review(rows, now_ms, days=7):
    """The Sunday review's numbers from the log rows (dicts with COLS keys, values as text): this week's shocks, how
    many kept going / reversed after 4h, how many a strategy alert followed in the same direction."""
    cut = now_ms - days * DAY
    week = []
    for r in rows:
        try:
            ms = dt.datetime.strptime(r["time_utc"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc).timestamp() * 1000
        except (KeyError, ValueError):
            continue
        if ms >= cut:
            week.append(r)
    num = lambda r, k: float(r[k]) if str(r.get(k, "")).strip() not in ("", "nan") else None   # noqa: E731
    done = [r for r in week if num(r, "after_4h_pct") is not None]
    kept = [r for r in done if num(r, "after_4h_pct") > 0]
    caught = [r for r in week if int(float(r.get("alerts_4h_same") or 0)) > 0]
    by_coin = {}
    for r in week:
        by_coin[r["coin"]] = by_coin.get(r["coin"], 0) + 1
    by_kind = {}
    for r in week:
        for t in str(r.get("triggers") or "").split("+"):
            if t:
                by_kind[t] = by_kind.get(t, 0) + 1
    big = sorted(done, key=lambda r: -abs(num(r, "move_pct") or 0))[:5]
    avg4 = round(sum(num(r, "after_4h_pct") for r in done) / len(done), 2) if done else None
    return dict(n=len(week), sent=sum(1 for r in week if r.get("sent") == "sent"), done=len(done), kept=len(kept),
                reversed=len(done) - len(kept), avg_after_4h=avg4, caught=len(caught), by_coin=by_coin,
                by_kind=by_kind, biggest=[dict(time_utc=r["time_utc"], coin=r["coin"], side=r["side"],
                                               move_pct=num(r, "move_pct"), after_4h=num(r, "after_4h_pct"),
                                               caught=int(float(r.get("alerts_4h_same") or 0)) > 0) for r in big])


def lines(sv):
    """Plain-English lines for the weekly review (sv: review())."""
    if not sv or not sv.get("n"):
        return ["no shock this week (or the watcher's shock log has not reached GitHub: journal sync)"]
    L = [f"{sv['n']} shock(s) this week, {sv['sent']} sent to Telegram (the rest: over the daily cap, paused "
         f"or /shock off)",
         "by kind: " + ", ".join(f"{TRIGGER_NAMES.get(k, k)} {v}" for k, v in sorted(sv["by_kind"].items())),
         "by coin: " + ", ".join(f"{c} {v}" for c, v in sorted(sv["by_coin"].items(), key=lambda x: -x[1]))]
    if sv["done"]:
        L.append(f"4 hours later: {sv['kept']} kept going, {sv['reversed']} reversed (average "
                 f"{sv['avg_after_4h']:+.2f}% in the shock's direction)")
    L.append(f"followed by a strategy alert in the same direction within 4h: {sv['caught']} of {sv['n']}"
             + (" - the strategies missed most shocks: material for the research (a reversal or sweep version)"
                if sv["n"] >= 5 and sv["caught"] * 3 < sv["n"] else ""))
    for b in sv["biggest"]:
        L.append(f"  {b['time_utc']} UTC {b['coin']} {b['side']} {b['move_pct']:+.1f}% -> 4h later "
                 f"{b['after_4h']:+.1f}% {'(a strategy alerted)' if b['caught'] else '(no strategy alert)'}")
    return L
