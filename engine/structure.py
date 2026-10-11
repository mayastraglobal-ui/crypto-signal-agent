"""
🧭 Structure card (operator request 2026-10-11, the playbook's section 2 + checklist "price at a marked 4H zone,
not in the middle of nowhere"). INFORMATION ONLY: it never creates, blocks or changes an alert, a rule or a size.

It reads the 4H Smart-Money-Concepts detectors that already run for every coin (engine/smc.py) and answers three
questions for the price of an alert:
  1. 4H structure - which way did the last break of structure go (BOS / CHoCH), and does it agree with the alert?
  2. Liquidity     - the nearest pool above and below (equal highs / lows, swing points, yesterday's / last week's
                     high and low) and how far it is in R (a pool before TP1 is worth knowing).
  3. Location      - at a 4H demand / supply zone (an active order block or an open fair value gap), or where in the
                     4H dealing range (discount / middle / premium / outside).

Everything is read at the CLOSE of a 4H candle (closed candles only, like the strategies), so the same card can be
rebuilt for any past candle - the weekly review compares closed signals by location ("structure_4h" column of
reports/signals_log.csv). Pure functions: no internet, no files.
"""
import numpy as np

DEFAULTS = dict(
    tf="4h",                 # the timeframe whose structure is shown
    near_atr=0.25,           # "at a zone" = inside it or within 0.25 x the 4H ATR of its edge
    middle=[0.35, 0.65],     # dealing-range position 35% - 65% = the middle (no edge)
)
POOL_NAMES = {"PDH": "yesterday's high", "PDL": "yesterday's low", "PWH": "last week's high",
              "PWL": "last week's low"}
VERDICTS = ["good", "middle", "against", "outside", "unknown"]       # the weekly review's groups, in this order
VERDICT_TEXT = {"good": "at a zone or edge that fits the direction", "middle": "middle of the 4H range",
                "against": "at a zone or edge against the direction", "outside": "outside the 4H range (breakout)",
                "unknown": "no 4H range yet"}


def settings(cfg_section):
    out = dict(DEFAULTS)
    out.update(cfg_section or {})
    return out


def _px(x, ref=None):
    """A price with the decimals of its size (or of ref) - the same rule as the alerts."""
    if x is None or x != x:
        return "-"
    a = abs(ref if ref else x)
    return f"{x:,.2f}" if a >= 100 else (f"{x:,.4f}" if a >= 1 else f"{x:.6f}")


def _num(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return x if np.isfinite(x) else None


def snapshot(res, df, atr, t=None):
    """The 4H structure known at the close of candle t (default: the newest).
    res = engine.smc.detect() of that candle table, df = the same candles, atr = their ATR (array or number).
    Returns None when there are no candles."""
    ser = res["series"]
    n = len(ser)
    if n == 0 or len(df) != n:
        return None
    t = n - 1 if t is None else int(t)
    brk, obs, fvgs = None, {}, {}
    for e in res["events"]:
        if e["t"] > t:
            break
        ev, key = e["event"], (e["dir"], e.get("zone_low"), e.get("zone_high"))
        if ev in ("BOS", "CHOCH"):
            brk = e
        elif ev == "ORDER_BLOCK":
            obs[key] = e["t"]
        elif ev == "OB_INVALID":
            obs.pop(key, None)
        elif ev == "FVG":
            fvgs[key] = e["t"]
        elif ev == "FVG_FILLED":
            fvgs.pop(key, None)
    a = _num(atr[t] if hasattr(atr, "__len__") else atr)
    row = ser.iloc[t]
    kinds = res.get("liq_kind") or {}
    zones = [dict(dir=d, low=lo, high=hi, kind="order block", age=t - born) for (d, lo, hi), born in obs.items()
             if lo is not None and hi is not None] + \
            [dict(dir=d, low=lo, high=hi, kind="fair value gap", age=t - born) for (d, lo, hi), born in fvgs.items()
             if lo is not None and hi is not None]

    def pool(side):
        lev = _num(row["liq_above" if side == "above" else "liq_below"])
        arr = kinds.get(side)
        kind = arr[t] if arr is not None and len(arr) == n else None
        return None if lev is None else dict(level=lev, kind=POOL_NAMES.get(kind, kind or "swing point"))

    rl, rh = _num(row["range_low"]), _num(row["range_high"])
    return dict(
        t=t, close_ms=int(df["close_time"].iloc[t]), close=float(df["close"].iloc[t]), atr=a,
        trend=None if brk is None else int(brk["dir"]),
        last_break=None if brk is None else dict(kind=brk["event"], dir=int(brk["dir"]), level=_num(brk["level"]),
                                                 candles_ago=t - int(brk["t"])),
        range=None if rl is None or rh is None or rh <= rl else dict(low=rl, high=rh),
        liq_above=pool("above"), liq_below=pool("below"),
        demand=[z for z in zones if z["dir"] == 1], supply=[z for z in zones if z["dir"] == -1])


def _zone_at(zones, price, near):
    hit = [z for z in zones if z["low"] - near <= price <= z["high"] + near]
    return min(hit, key=lambda z: abs((z["low"] + z["high"]) / 2 - price)) if hit else None


def place(snap, price, s=None):
    """Where price sits: (location, zone or None, range position or None).
    location: demand / supply / discount / middle / premium / above / below / unknown."""
    s = settings(s)
    near = s["near_atr"] * (snap.get("atr") or 0)
    dem, sup = _zone_at(snap["demand"], price, near), _zone_at(snap["supply"], price, near)
    rng = snap.get("range")
    pos = None if not rng else (price - rng["low"]) / (rng["high"] - rng["low"])
    if dem and sup:                                  # both: the one whose middle is nearer
        mid = lambda z: abs((z["low"] + z["high"]) / 2 - price)
        dem, sup = (dem, None) if mid(dem) <= mid(sup) else (None, sup)
    if dem:
        return "demand", dem, pos
    if sup:
        return "supply", sup, pos
    if pos is None:
        return "unknown", None, None
    if pos > 1:
        return "above", None, pos
    if pos < 0:
        return "below", None, pos
    lo, hi = s["middle"]
    return ("discount" if pos < lo else "premium" if pos > hi else "middle"), None, pos


def verdict(loc, d):
    """good / middle / against / outside / unknown for an alert in direction d (1 long, -1 short)."""
    if loc in ("above", "below"):
        return "outside"
    if loc in ("middle", "unknown"):
        return loc
    good = ("demand", "discount") if d == 1 else ("supply", "premium")
    return "good" if loc in good else "against"


def card(snap, price, d, R=None, tp1=None, s=None):
    """The structure card of one alert: dict(loc, verdict, trend_agree, pos, room_r, before_tp1, tag, lines).
    price = the alert's entry, d = 1 long / -1 short, R = its stop distance (price), tp1 = its first target."""
    s = settings(s)
    side = "LONG" if d == 1 else "SHORT"
    loc, zone, pos = place(snap, price, s)
    vd = verdict(loc, d)
    tr = snap.get("trend")
    agree = "none" if tr is None else ("with" if tr == d else "against")
    opp = snap.get("liq_above") if d == 1 else snap.get("liq_below")
    room_r = before = None
    if opp and R and (opp["level"] - price) * d > 0:
        room_r = round((opp["level"] - price) * d / R, 2)
        before = tp1 is not None and (opp["level"] - tp1) * d < 0
    # line 1: structure
    lb = snap.get("last_break")
    if lb:
        name = "BOS" if lb["kind"] == "BOS" else "CHoCH"
        l1 = (f"🧭 <b>4H structure:</b> {'uptrend' if tr == 1 else 'downtrend'} · last {name} "
              f"{'up' if lb['dir'] == 1 else 'down'} at {_px(lb['level'], price)} ({lb['candles_ago']} candles ago)")
        l1 += f" · with your {side}" if agree == "with" else f" · ⚠️ against your {side}"
    else:
        l1 = "🧭 <b>4H structure:</b> no break of structure yet - no clear 4H trend"
    # line 2: liquidity
    parts = []
    for nm, p, sg in (("above", snap.get("liq_above"), 1), ("below", snap.get("liq_below"), -1)):
        if p and (p["level"] - price) * sg > 0:
            dist = f", {abs(p['level'] - price) / R:.1f}R" if R else ""
            parts.append(f"{nm} {_px(p['level'], price)} ({p['kind']}{dist})")
    l2 = "💧 <b>Liquidity:</b> " + (" · ".join(parts) if parts else "no pool marked near price")
    if before:
        l2 += f" · ⚠️ the pool {'above' if d == 1 else 'below'} sits before TP1 - price may stall there"
    # line 3: location
    pct = "" if pos is None else f", {pos * 100:.0f}% of the range"
    zt = "" if not zone else f" ({zone['kind']} {_px(zone['low'], price)}-{_px(zone['high'], price)})"
    texts = {
        "demand": ("✅" if d == 1 else "⚠️") + f" at a 4H demand zone{zt}" + ("" if d == 1 else
                                                                            f" - buyers' area, against a {side}"),
        "supply": ("✅" if d == -1 else "⚠️") + f" at a 4H supply zone{zt}" + ("" if d == -1 else
                                                                             f" - sellers' area, against a {side}"),
        "discount": ("✅" if d == 1 else "⚠️") + f" lower part of the 4H range (discount{pct})"
                    + ("" if d == 1 else f" - late for a {side}"),
        "premium": ("✅" if d == -1 else "⚠️") + f" upper part of the 4H range (premium{pct})"
                   + ("" if d == -1 else f" - late for a {side}"),
        "middle": f"⚠️ middle of the 4H range ({0 if pos is None else pos * 100:.0f}%) - the playbook prefers "
                  "the edges",
        "above": "ℹ️ above the 4H range - a breakout, no 4H zone here",
        "below": "ℹ️ below the 4H range - a breakdown, no 4H zone here",
        "unknown": "ℹ️ no 4H range marked yet",
    }
    l3 = f"📍 <b>Location:</b> {texts[loc]}"
    return dict(loc=loc, verdict=vd, trend_agree=agree, pos=None if pos is None else round(pos, 3),
                room_r=room_r, before_tp1=bool(before), tag=f"{vd};{loc};{agree}",
                lines=[l1, l2, l3, "<i>Information only - the strategy's own rules made this alert.</i>"])


def overview(snap, price, coin, s=None):
    """/structure COIN: the 4H picture without a trade direction (Telegram HTML lines)."""
    s = settings(s)
    loc, zone, pos = place(snap, price, s)
    lb, tr = snap.get("last_break"), snap.get("trend")
    out = [f"🧭 <b>{coin} 4H structure</b> · price {_px(price)}"]
    if lb:
        out.append(f"Trend: <b>{'UP' if tr == 1 else 'DOWN'}</b> · last {'BOS' if lb['kind'] == 'BOS' else 'CHoCH'} "
                   f"{'up' if lb['dir'] == 1 else 'down'} at {_px(lb['level'], price)} ({lb['candles_ago']} candles ago)")
    else:
        out.append("Trend: no break of structure yet")
    rng = snap.get("range")
    if rng:
        out.append(f"Range: {_px(rng['low'], price)} - {_px(rng['high'], price)} · price at {pos * 100:.0f}% "
                   f"({'discount' if pos < 0.5 else 'premium'} half)" if 0 <= pos <= 1 else
                   f"Range: {_px(rng['low'], price)} - {_px(rng['high'], price)} · price "
                   f"{'ABOVE' if pos > 1 else 'BELOW'} it")
    for nm, p, sg in (("above", snap.get("liq_above"), 1), ("below", snap.get("liq_below"), -1)):
        if p and (p["level"] - price) * sg > 0:
            pct = abs(p["level"] / price - 1) * 100
            out.append(f"💧 Liquidity {nm}: {_px(p['level'], price)} ({p['kind']}, {pct:.1f}% away)")

    def nearest(zones, sg):
        cand = [z for z in zones if (z["low"] - price) * sg > 0 or z["low"] <= price <= z["high"]]
        return min(cand, key=lambda z: abs((z["low"] + z["high"]) / 2 - price)) if cand else None
    for nm, z, sg in (("Supply", nearest(snap["supply"], 1), 1), ("Demand", nearest(snap["demand"], -1), -1)):
        if z:
            where = "at price" if z["low"] <= price <= z["high"] else ("above" if sg == 1 else "below")
            out.append(f"{'🟥' if z['dir'] == -1 else '🟩'} {nm} {where}: {z['kind']} {_px(z['low'], price)}-"
                       f"{_px(z['high'], price)}")
    names = {"demand": "at a 4H demand zone", "supply": "at a 4H supply zone", "discount": "lower part of the range",
             "premium": "upper part of the range", "middle": "middle of the range (no edge)",
             "above": "above the range", "below": "below the range", "unknown": "no range marked yet"}
    out.append(f"📍 Now: <b>{names[loc]}</b>")
    out.append("<i>Read at the last 4H close. Information only - it never makes or blocks an alert.</i>")
    return out


def review(rows):
    """Weekly review: closed signals grouped by their location verdict. rows = dicts with structure_4h (tag text)
    and result_r. Returns [dict(verdict, text, n, avg_r, wins)] in VERDICTS order (only groups with signals)."""
    groups = {}
    for r in rows:
        tag, res = str(r.get("structure_4h") or ""), _num(r.get("result_r"))
        if res is None or not tag or tag == "nan":
            continue
        groups.setdefault(tag.split(";")[0], []).append(res)
    out = []
    for v in VERDICTS:
        vals = groups.get(v)
        if vals:
            out.append(dict(verdict=v, text=VERDICT_TEXT[v], n=len(vals), avg_r=round(float(np.mean(vals)), 3),
                            wins=sum(x > 0 for x in vals)))
    return out
