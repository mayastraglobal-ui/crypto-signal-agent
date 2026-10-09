"""
Trade follow-up for the live watcher (roadmap step 4, operator request 2026-10-06).

After the operator presses "✅ Took it" under an alert, the watcher follows that trade on 5m candles with the SAME
management rules as the backtests (scanner.simulate_trade): stop first when the stop and a target are touched in
one candle, TP1 -> stop to entry, TP2 -> stop to TP1, the last target closes the rest, and the time stop at the
strategy's max hold. At each step it tells the operator on Telegram what to do. The strategy's own early-exit rule
is not followed here (the alert's max hold is).
A limit-entry alert (roadmap step 2B) first waits for the fill: price back at the limit within the card's
valid_bars candles -> filled (only the stop counts in the fill candle, as in the backtest); otherwise -> expired, no
trade.
Step 3 (the operator's playbook) adds the card's manage block, with the backtest's rules: after TP1 the stop goes to
entry + fees (be_plus_fees) and trails the last confirmed 5m swing / EMA9 (a message when it should move by 0.25R
or more); no +0.5R within N candles -> exit (progress); a close beyond the setup's invalidation level -> exit.
Pure: no internet, no files. A trade is a plain dict, so it can live in the watcher's JSON state.
"""
import datetime as dt

from engine import live as lv
from engine import timeframes as tfm

FIVE = tfm.TF_MS["5m"]


def open_trade(a, aid, taken_ms, tp_cfg=None):
    """A followed trade from a remembered alert. Follows from the 5m candle in which the operator pressed
    'Took it' (never before the entry candle). The time stop counts from the entry candle, as in the backtests."""
    tp_cfg = tp_cfg or {}
    start = a["close_ms"] + 1
    tps = [float(x) for x in a["tps"]]
    split = list(a.get("split") or [1.0 / len(tps)] * len(tps)) if tps else []
    lim = a.get("limit_bars")
    man = a.get("manage") or {}
    d, entry = int(a["d"]), float(a["entry"])
    iv_every = (man.get("invalidate") or {}).get("every")
    extra = dict(be_price=entry * (1 + d * float(a.get("be_frac") or 0)) if man.get("be_plus_fees") else entry,
                 progress=man.get("progress"), trailing=bool(man.get("trail")), trail_cfg=man.get("trail"),
                 last_trail=None, told_stop=None,
                 inval=a.get("inval"), inval_every_ms=tfm.TF_MS[iv_every] if iv_every else None, bars_in=0, mfe=0.0)
    return dict(extra, id=aid, label=a["label"], coin=a["coin"], inst=a.get("inst", a["coin"]), d=int(a["d"]), tf=a["tf"],
                filled=not lim, fill_by_ms=start + int(lim) * tfm.TF_MS[a["tf"]] if lim else None,
                max_hold=int(a["max_hold"]) if a.get("max_hold") else None,
                strategy=a["strategy"], version=a.get("version"), entry=float(a["entry"]), R=float(a["R"]),
                stop=float(a["entry"]) - int(a["d"]) * float(a["R"]), tps=tps, split=split, hit=0, remaining=1.0,
                realized=0.0, checked_ms=max(start, taken_ms // FIVE * FIVE),
                end_ms=start + int(a["max_hold"]) * tfm.TF_MS[a["tf"]] if a.get("max_hold") else None,
                taken_ms=taken_ms, be=bool(tp_cfg.get("move_stop_to_breakeven_after_tp1", True)),
                trail=bool(tp_cfg.get("move_stop_to_tp1_after_tp2", True)), closed=False)


def step(t, bars):
    """Walk the trade through closed 5m candles (dicts with open_time, open, high, low, close), oldest first; only
    candles not seen yet count. Changes t and returns the events: dict(kind='tp'|'stop'|'time', at_ms, px, ...)."""
    out, d = [], t["d"]
    for b in bars:
        ot = int(b["open_time"])
        if t["closed"] or ot < t["checked_ms"]:
            continue
        o, h, l, c = (float(b[k]) for k in ("open", "high", "low", "close"))
        at = ot + FIVE
        t["checked_ms"] = at
        fill_bar = False
        if not t.get("filled", True):                                              # a limit order still waiting
            if (d == 1 and l <= t["entry"]) or (d == -1 and h >= t["entry"]):
                t["filled"], fill_bar = True, True
                step_ms = tfm.TF_MS[t["tf"]]
                if t.get("max_hold"):                    # the time stop counts from the fill candle (backtest)
                    t["end_ms"] = ot // step_ms * step_ms + t["max_hold"] * step_ms
                out.append(dict(kind="fill", px=t["entry"], at_ms=at))
            elif at >= t["fill_by_ms"]:
                t["closed"] = True
                out.append(dict(kind="expired", px=None, at_ms=at, final=True, result_r=None))
                continue
            else:
                continue
        tv = t.get("last_trail")                                                   # known at the last close
        if t.get("trailing") and t["hit"] >= 1 and tv is not None and not fill_bar:
            new = max(t["stop"], tv) if d == 1 else min(t["stop"], tv)
            if new != t["stop"]:
                t["stop"] = new
                told = t.get("told_stop")
                if told is None or abs(new - told) >= 0.25 * t["R"]:
                    t["told_stop"] = new
                    out.append(dict(kind="trail", px=new, at_ms=ot))
        t["last_trail"] = (b.get("trail_long") if d == 1 else b.get("trail_short"))
        if t["last_trail"] is not None and t["last_trail"] != t["last_trail"]:     # NaN
            t["last_trail"] = None
        t["bars_in"] = t.get("bars_in", 0) + 1
        t["mfe"] = max(t.get("mfe", 0.0), d * ((h if d == 1 else l) - t["entry"]))
        if (d == 1 and l <= t["stop"]) or (d == -1 and h >= t["stop"]):             # stop first (worst case)
            px = o if ((d == 1 and o < t["stop"]) or (d == -1 and o > t["stop"])) else t["stop"]
            out.append(_close(t, "stop", px, at))
            continue
        if fill_bar:                                     # the fill candle: targets only from the next candle
            continue
        while t["hit"] < len(t["tps"]) and ((d == 1 and h >= t["tps"][t["hit"]]) or (d == -1 and l <= t["tps"][t["hit"]])):
            i = t["hit"]
            last = i == len(t["tps"]) - 1
            frac = t["remaining"] if last else min(float(t["split"][i]), t["remaining"])
            t["realized"] += frac * d * (t["tps"][i] - t["entry"]) / t["R"]
            t["remaining"] -= frac
            t["hit"] += 1
            if t["hit"] == 1 and t["be"]:
                t["stop"] = t.get("be_price", t["entry"])
            elif t["hit"] >= 2 and t["trail"]:
                t["stop"] = t["tps"][t["hit"] - 2]
            ev = dict(kind="tp", n=t["hit"], px=t["tps"][i], frac=frac, stop=t["stop"], at_ms=at)
            if t["remaining"] <= 1e-9:
                t["remaining"], t["closed"] = 0.0, True
                ev.update(final=True, result_r=t["realized"])
            out.append(ev)
        if t["closed"]:
            continue
        if t["hit"] > 0 and ((d == 1 and c <= t["stop"]) or (d == -1 and c >= t["stop"])):
            out.append(_close(t, "stop", t["stop"], at))                         # back through the moved stop
            continue
        iv, every = t.get("inval"), t.get("inval_every_ms")
        if iv is not None and (not every or at % every == 0) and d * (c - iv) < 0:
            out.append(_close(t, "invalid", c, at))                              # the setup is invalidated
            continue
        pg = t.get("progress")
        if pg and t["bars_in"] == int(pg["bars"]) and t["mfe"] < float(pg["r"]) * t["R"]:
            out.append(dict(_close(t, "time", c, at), why=f"+{pg['r']:g}R not reached within {pg['bars']} candles"))
            continue
        if t["end_ms"] and at >= t["end_ms"]:
            out.append(_close(t, "time", c, at))
    return out


def _close(t, kind, px, at):
    t["realized"] += t["remaining"] * t["d"] * (px - t["entry"]) / t["R"]
    t["remaining"], t["closed"] = 0.0, True
    return dict(kind=kind, px=px, at_ms=at, hit=t["hit"], result_r=t["realized"], final=True)


def _head(t):
    side = "LONG" if t["d"] == 1 else "SHORT"
    return f"<b>{side} {t['coin']}</b> · {t['tf']} {t['strategy']}" + ("" if t["label"] == "LIVE" else f" ({t['label']})")


def text(t, ev):
    """Telegram text (HTML) of one follow-up event: what happened and what to do now."""
    px = lambda x: lv.fmt_px(x, t["entry"])                                          # noqa: E731
    when = f"(5m candle closed {lv.bj(ev['at_ms'])})"
    if ev["kind"] == "fill":
        return (f"✅ Limit filled · {_head(t)}\nPrice reached your limit {px(t['entry'])}. Set the stop-loss "
                f"<b>{px(t['stop'])}</b> and the TPs on OKX now if you haven't. {when}")
    if ev["kind"] == "trail":
        return (f"🔁 Trail the stop · {_head(t)}\nMove the stop-loss to <b>{px(ev['px'])}</b> (behind the last 5m swing / "
                f"EMA9). (5m candle closed {lv.bj(ev['at_ms'])})")
    if ev["kind"] == "expired":
        return (f"⌛ Limit not filled · {_head(t)}\nPrice did not come back to {px(t['entry'])} in time → "
                f"<b>cancel the limit order</b> on OKX. No trade. {when}")
    done = (f"\nTrade finished: about <b>{ev['result_r']:+.1f}R</b> before fees." if ev.get("final") else "")
    if ev["kind"] == "tp":
        if ev.get("final"):
            return f"🏁 TP{ev['n']} hit · {_head(t)}\nTP{ev['n']} {px(ev['px'])} reached → close the rest. {when}{done}"
        move = ("Move the stop-loss to <b>entry {}</b> (break-even{}).".format(
                    px(ev["stop"]), " + fees" if abs(ev["stop"] - t["entry"]) > 1e-12 else "") if ev["n"] == 1 else
                f"Move the stop-loss to <b>TP{ev['n'] - 1} {px(ev['stop'])}</b>.")
        return (f"🎯 TP{ev['n']} hit · {_head(t)}\nTP{ev['n']} {px(ev['px'])} reached → close "
                f"{ev['frac'] * 100:.0f}% of the position. {move} {when}")
    if ev["kind"] == "stop":
        what = ("Stop-loss hit" if ev["hit"] == 0 else
                "Stopped at entry (break-even) after TP1" if abs(ev["px"] - t["entry"]) < 1e-12 else
                "Stopped at break-even + fees after TP1" if abs(ev["px"] - t.get("be_price", t["entry"])) < 1e-12 else
                f"Moved stop hit after TP{ev['hit']}")
        return f"🛑 {what} · {_head(t)}\nStop {px(ev['px'])}. If OKX hasn't closed it, close it now. {when}{done}"
    if ev["kind"] == "invalid":
        return (f"❌ Setup invalidated · {_head(t)}\nA close beyond {px(t['inval'])} → <b>exit at market</b> "
                f"(about {px(ev['px'])}). {when}{done}")
    why = ev.get("why") or "the strategy's max hold is over"
    return (f"⏱ Time stop · {_head(t)}\n{why[0].upper() + why[1:]} → close the rest at market "
            f"(about {px(ev['px'])}). {when}{done}")


def summary(t):
    """One line for /trades."""
    side = "LONG" if t["d"] == 1 else "SHORT"
    px = lambda x: lv.fmt_px(x, t["entry"])                                          # noqa: E731
    state = ("limit waiting for a fill" if not t.get("filled", True) else
             "no target yet" if t["hit"] == 0 else f"TP{t['hit']} hit")
    end = (f", time stop {dt.datetime.fromtimestamp(t['end_ms'] / 1000, lv.BJ):%d %b %H:%M} Beijing"
           if t.get("end_ms") else "")
    return (f"• {side} {t['coin']} {t['tf']} ({t['label']}) · entry {px(t['entry'])} · stop {px(t['stop'])} · "
            f"{state}{end}")
