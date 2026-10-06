"""
Trade follow-up for the live watcher (roadmap step 4, operator request 2026-10-06).

After the operator presses "✅ Took it" under an alert, the watcher follows that trade on 5m candles with the SAME
management rules as the backtests (scanner.simulate_trade): stop first when the stop and a target are touched in
one candle, TP1 -> stop to entry, TP2 -> stop to TP1, the last target closes the rest, and the time stop at the
strategy's max hold. At each step it tells the operator on Telegram what to do. The strategy's own early-exit rule
is not followed here (the alert's max hold is).
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
    return dict(id=aid, label=a["label"], coin=a["coin"], inst=a.get("inst", a["coin"]), d=int(a["d"]), tf=a["tf"],
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
        if (d == 1 and l <= t["stop"]) or (d == -1 and h >= t["stop"]):             # stop first (worst case)
            px = o if ((d == 1 and o < t["stop"]) or (d == -1 and o > t["stop"])) else t["stop"]
            out.append(_close(t, "stop", px, at))
            continue
        while t["hit"] < len(t["tps"]) and ((d == 1 and h >= t["tps"][t["hit"]]) or (d == -1 and l <= t["tps"][t["hit"]])):
            i = t["hit"]
            last = i == len(t["tps"]) - 1
            frac = t["remaining"] if last else min(float(t["split"][i]), t["remaining"])
            t["realized"] += frac * d * (t["tps"][i] - t["entry"]) / t["R"]
            t["remaining"] -= frac
            t["hit"] += 1
            if t["hit"] == 1 and t["be"]:
                t["stop"] = t["entry"]
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
    when = f"(5m candle closed {lv.utc(ev['at_ms'])})"
    done = (f"\nTrade finished: about <b>{ev['result_r']:+.1f}R</b> before fees." if ev.get("final") else "")
    if ev["kind"] == "tp":
        if ev.get("final"):
            return f"🏁 TP{ev['n']} hit · {_head(t)}\nTP{ev['n']} {px(ev['px'])} reached → close the rest. {when}{done}"
        move = ("Move the stop-loss to <b>entry {}</b> (break-even).".format(px(ev["stop"])) if ev["n"] == 1 else
                f"Move the stop-loss to <b>TP{ev['n'] - 1} {px(ev['stop'])}</b>.")
        return (f"🎯 TP{ev['n']} hit · {_head(t)}\nTP{ev['n']} {px(ev['px'])} reached → close "
                f"{ev['frac'] * 100:.0f}% of the position. {move} {when}")
    if ev["kind"] == "stop":
        what = ("Stop-loss hit" if ev["hit"] == 0 else
                "Stopped at entry (break-even) after TP1" if abs(ev["px"] - t["entry"]) < 1e-12 else
                f"Moved stop hit after TP{ev['hit']}")
        return f"🛑 {what} · {_head(t)}\nStop {px(ev['px'])}. If OKX hasn't closed it, close it now. {when}{done}"
    return (f"⏱ Time stop · {_head(t)}\nThe strategy's max hold is over → close the rest at market "
            f"(about {px(ev['px'])}). {when}{done}")


def summary(t):
    """One line for /trades."""
    side = "LONG" if t["d"] == 1 else "SHORT"
    px = lambda x: lv.fmt_px(x, t["entry"])                                          # noqa: E731
    state = "no target yet" if t["hit"] == 0 else f"TP{t['hit']} hit"
    end = (f", time stop {dt.datetime.fromtimestamp(t['end_ms'] / 1000, dt.timezone.utc):%d %b %H:%M} UTC"
           if t.get("end_ms") else "")
    return (f"• {side} {t['coin']} {t['tf']} ({t['label']}) · entry {px(t['entry'])} · stop {px(t['stop'])} · "
            f"{state}{end}")
