"""
Smart Money Concepts / ICT detectors (AGENT_PROMPT.md section 9).

SMC is treated as TESTABLE HYPOTHESES, NOT DOCTRINE. Every concept is an exact rule on closed candles,
and every event is stamped with the candle at which it became KNOWABLE - nothing is ever drawn in
afterwards. One pass over the candles, keeping state (pools, structure, gaps, order blocks) as it goes.

Pure functions: no internet, no files.
"""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

VERSION = "smc-1.0"
NY = ZoneInfo("America/New_York")

DEFAULTS = dict(
    equal_pct=0.1,           # two swing highs (lows) within 0.1% = equal highs (lows): a liquidity pool
    sweep_atr=0.1,           # sweep: the wick goes through a pool by >= 0.1 ATR ...
                             # ... and the candle CLOSES back inside
    fvg_atr=0.25,            # fair value gap must be >= 0.25 ATR
    displacement_bars=3,     # a BOS/CHoCH "with displacement": displacement candle within the last 3 candles
    ob_lookback=10,          # order block = last opposite candle within 10 candles before the displacement
    leg_bars=10,             # displacement leg for OTE: extreme of the last 10 candles before the break
    ote=[0.62, 0.79],        # optimal trade entry = 62% - 79% retracement of that leg
    amd_bars=10,             # power of 3: consolidation -> sweep -> CHoCH within 10 candles
    amd_consolidation_bars=5,  # ... consolidation seen within 5 candles before the sweep
    max_pools=30,            # keep the newest 30 swing pools per side
    max_open=50,             # keep the newest 50 open gaps / order blocks
    # New York time windows (start hour, end hour); summer/winter time handled automatically
    killzones={"Asia": [20, 24], "London": [2, 5], "NY AM": [7, 10], "Silver Bullet": [10, 11]},
)

EVENT_COLUMNS = ["sweep_bull", "sweep_bear", "bos_up", "bos_down", "choch_up", "choch_down",
                 "fvg_retrace_bull", "fvg_retrace_bear"]
# per-candle CONTEXT (Phase 7): what was known at the close of each candle, for strategy rules
CONTEXT_COLUMNS = ["range_low", "range_high", "range_pos",           # active dealing range; pos < 0.5 = discount
                   "bull_ob_low", "bull_ob_high", "bear_ob_low", "bear_ob_high",   # newest ACTIVE order blocks
                   "in_bull_ob", "in_bear_ob",                        # this candle traded into an active OB
                   "sweep_bull_low", "sweep_bear_high",               # extreme of the newest sweep (for stops)
                   "sweep_pdl", "sweep_pdh",                          # this candle swept the prior-day low / high
                   "liq_above", "liq_below",                          # nearest liquidity pool above / below close
                   "pdh", "pdl", "pd_mid",                            # prior-day high / low / middle
                   "kz_asia", "kz_london", "kz_ny_am", "kz_silver_bullet", "in_killzone"]
KZ_COLUMNS = {"Asia": "kz_asia", "London": "kz_london", "NY AM": "kz_ny_am", "Silver Bullet": "kz_silver_bullet"}


def settings(cfg_section):
    out = dict(DEFAULTS)
    out.update(cfg_section or {})
    return out


def killzone(open_ms, zones=None):
    """Name of the New York killzone a candle STARTS in (or None)."""
    zones = zones or DEFAULTS["killzones"]
    h = dt.datetime.fromtimestamp(open_ms / 1000, tz=NY).hour
    for name, (a, b) in zones.items():
        if a <= h < b:
            return name
    return None


def killzone_hours(open_ms, zones=None):
    """Vectorised killzone(): one name (or None) per candle start time."""
    zones = zones or DEFAULTS["killzones"]
    hours = pd.to_datetime(np.asarray(open_ms, dtype="int64"), unit="ms", utc=True).tz_convert(NY).hour.to_numpy()
    out = np.full(len(hours), None, dtype=object)
    for name, (a, b) in zones.items():
        out[(hours >= a) & (hours < b)] = name
    return out


def previous_levels(df, higher):
    """For every candle: high and low of the newest HIGHER candle that had closed before this candle
    opened (previous day / previous week). NaN when there is none."""
    n = len(df)
    hi, lo = np.full(n, np.nan), np.full(n, np.nan)
    if higher is None or len(higher) == 0:
        return hi, lo
    h = higher.sort_values("close_time")
    idx = np.searchsorted(h["close_time"].to_numpy(), df["open_time"].to_numpy(), side="left") - 1
    ok = idx >= 0
    hi[ok] = h["high"].to_numpy()[idx[ok]]
    lo[ok] = h["low"].to_numpy()[idx[ok]]
    return hi, lo


def detect(df, feats, daily=None, weekly=None, tf_ms=None, s=None):
    """Run every detector over one candle table.

    df      : closed candles (open_time, close_time, open, high, low, close)
    feats   : engine.features.compute(df) (swings, ATR, displacement, consolidation)
    daily / weekly : closed 1D / 1W candles for PDH/PDL and PWH/PWL pools (optional)
    Returns dict(events=[...], series=DataFrame of per-candle event flags + CONTEXT_COLUMNS, state=...)."""
    s = settings(s)
    df = df.reset_index(drop=True)
    f = feats.reset_index(drop=True)
    n = len(df)
    o, h, l, c = (df[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close"))
    ct, ot = df["close_time"].to_numpy(), df["open_time"].to_numpy()
    atr = f["atr"].to_numpy()
    atr_prev = np.r_[np.nan, atr[:-1]]
    sh, sl = f["swing_high"].to_numpy(), f["swing_low"].to_numpy()
    shp, slp = f["swing_high_price"].to_numpy(), f["swing_low_price"].to_numpy()
    disp_up, disp_dn = f["displacement_up"].to_numpy(), f["displacement_down"].to_numpy()
    consol = f["consolidation"].to_numpy()
    pdh, pdl = previous_levels(df, daily)
    pwh, pwl = previous_levels(df, weekly)
    kz_on = tf_ms is None or tf_ms <= 3_600_000                 # killzones only mean something intraday

    events = []
    flags = {k: np.zeros(n, bool) for k in EVENT_COLUMNS}
    pools = []          # dict(level, side, kind, born)
    fvgs = []           # dict(dir, low, high, born, retraced)
    obs = []            # dict(dir, low, high, born, state: active / breaker, retested)
    last_sh = last_sl = None     # dict(level, t, broken)
    trend, last_break = None, None
    last_sweep = {1: None, -1: None}
    ote = None
    known = {}          # PDH / PDL / PWH / PWL level currently in force (a pool only when it CHANGES)
    ctx = {k: np.full(n, np.nan) for k in CONTEXT_COLUMNS}
    for k in ("in_bull_ob", "in_bear_ob", "sweep_pdl", "sweep_pdh", "in_killzone") + tuple(KZ_COLUMNS.values()):
        ctx[k] = np.zeros(n, bool)
    ctx["pdh"], ctx["pdl"], ctx["pd_mid"] = pdh, pdl, (pdh + pdl) / 2
    if kz_on and n:
        kz = killzone_hours(ot, s["killzones"])
        for name, col in KZ_COLUMNS.items():
            ctx[col] = kz == name
        ctx["in_killzone"] = kz != None      # noqa: E711 (element-wise on an object array)
    sweep_ext = {1: np.nan, -1: np.nan}

    def add(t, event, d, level=None, lo=None, hi=None, size=None, info=""):
        events.append(dict(t=int(t), time=int(ct[t]), event=event, dir=int(d),
                           level=None if level is None else float(level),
                           zone_low=None if lo is None else float(lo), zone_high=None if hi is None else float(hi),
                           size_atr=None if size is None or not np.isfinite(size) else round(float(size), 3),
                           killzone=killzone(int(ot[t]), s["killzones"]) if kz_on else None, info=info))

    for t in range(n):
        a = atr_prev[t] if np.isfinite(atr_prev[t]) else atr[t]
        # ---------- 1. new liquidity pools become known at this candle ----------
        for key, lev, side in (("PDH", pdh[t], 1), ("PDL", pdl[t], -1), ("PWH", pwh[t], 1), ("PWL", pwl[t], -1)):
            if np.isfinite(lev) and known.get(key) != lev:              # a new day / week began
                known[key] = lev
                pools = [p for p in pools if p["kind"] != key]           # the old level is replaced
                pools.append(dict(level=lev, side=side, kind=key, born=t))
        if sh[t]:
            lev = shp[t]
            eq = [p for p in pools if p["side"] == 1 and p["kind"] in ("swing high", "equal highs")
                  and abs(p["level"] - lev) <= lev * s["equal_pct"] / 100]
            if eq:
                p = eq[-1]
                p.update(level=max(p["level"], lev), kind="equal highs")
            else:
                pools.append(dict(level=lev, side=1, kind="swing high", born=t))
            last_sh = dict(level=lev, t=t, broken=False)
        if sl[t]:
            lev = slp[t]
            eq = [p for p in pools if p["side"] == -1 and p["kind"] in ("swing low", "equal lows")
                  and abs(p["level"] - lev) <= lev * s["equal_pct"] / 100]
            if eq:
                p = eq[-1]
                p.update(level=min(p["level"], lev), kind="equal lows")
            else:
                pools.append(dict(level=lev, side=-1, kind="swing low", born=t))
            last_sl = dict(level=lev, t=t, broken=False)
        for side in (1, -1):
            swing = [p for p in pools if p["side"] == side and p["kind"] not in ("PDH", "PDL", "PWH", "PWL")]
            for p in swing[:-s["max_pools"]]:
                pools.remove(p)

        # ---------- 2. sweeps: wick through a pool, close back inside ----------
        if np.isfinite(a) and a > 0:
            for side in (1, -1):
                hit = [p for p in pools if p["side"] == side and p["born"] < t and
                       ((side == 1 and h[t] >= p["level"] + s["sweep_atr"] * a) or
                        (side == -1 and l[t] <= p["level"] - s["sweep_atr"] * a))]
                # used up: swept (wick >= 0.1 ATR through) or closed beyond; a tiny poke leaves it alive
                through = hit + [p for p in pools if p["side"] == side and p["born"] < t and p not in hit and
                                 ((side == 1 and c[t] > p["level"]) or (side == -1 and c[t] < p["level"]))]
                if hit:
                    key = max(hit, key=lambda p: p["level"] * side)       # the most extreme pool swept
                    back_inside = c[t] < key["level"] if side == 1 else c[t] > key["level"]
                    if back_inside:
                        d = -side          # buy-side swept = bearish idea; sell-side swept = bullish idea
                        kinds = sorted({p["kind"] for p in hit})
                        add(t, "SWEEP", d, level=key["level"], size=abs((h[t] if side == 1 else l[t]) - key["level"]) / a,
                            info=f"{'buy' if side == 1 else 'sell'}-side liquidity swept ({', '.join(kinds)})")
                        flags["sweep_bull" if d == 1 else "sweep_bear"][t] = True
                        last_sweep[d] = t
                        sweep_ext[d] = l[t] if d == 1 else h[t]
                        if d == 1 and "PDL" in kinds:
                            ctx["sweep_pdl"][t] = True
                        if d == -1 and "PDH" in kinds:
                            ctx["sweep_pdh"][t] = True
                for p in through:
                    pools.remove(p)

        # ---------- 3. structure: BOS / CHoCH (with displacement) / weak break ----------
        for side in (1, -1):
            sw = last_sh if side == 1 else last_sl
            if sw is None or sw["broken"] or sw["t"] >= t:
                continue
            broke = c[t] > sw["level"] if side == 1 else c[t] < sw["level"]
            if not broke:
                continue
            sw["broken"] = True
            dwin = disp_up if side == 1 else disp_dn
            d_idx = [k for k in range(max(0, t - s["displacement_bars"] + 1), t + 1) if dwin[k]]
            with_disp = bool(d_idx)
            want = "up" if side == 1 else "down"
            if trend == want or trend is None:
                kind = "BOS"
                trend = want
            elif with_disp:
                kind = "CHOCH"
                trend = want
            else:
                kind = "WEAK_BREAK"
            add(t, kind, side, level=sw["level"], size=abs(c[t] - sw["level"]) / a if a else None,
                info=("with displacement" if with_disp else "no displacement")
                + (" (first break, sets the trend)" if kind == "BOS" and last_break is None else ""))
            if kind != "WEAK_BREAK":
                flags[("bos_" if kind == "BOS" else "choch_") + want][t] = True
                last_break = dict(kind=kind, dir=side, t=t, level=sw["level"])
                lo_leg = l[max(0, t - s["leg_bars"]):t + 1].min() if side == 1 else None
                hi_leg = h[max(0, t - s["leg_bars"]):t + 1].max() if side == -1 else None
                if side == 1:
                    top, bot = h[t], lo_leg
                    ote = dict(dir=1, t=t, low=top - s["ote"][1] * (top - bot), high=top - s["ote"][0] * (top - bot))
                else:
                    top, bot = hi_leg, l[t]
                    ote = dict(dir=-1, t=t, low=bot + s["ote"][0] * (top - bot), high=bot + s["ote"][1] * (top - bot))
                # order block: last opposite candle before the displacement that caused this break
                if with_disp:
                    start = d_idx[0]
                    for k in range(start - 1, max(-1, start - 1 - s["ob_lookback"]), -1):
                        if (side == 1 and c[k] < o[k]) or (side == -1 and c[k] > o[k]):
                            obs.append(dict(dir=side, low=l[k], high=h[k], born=t, state="active", retested=False))
                            add(t, "ORDER_BLOCK", side, lo=l[k], hi=h[k],
                                info=f"last {'bearish' if side == 1 else 'bullish'} candle before the displacement")
                            break

        # ---------- 4. power of 3 (AMD): consolidation -> sweep -> CHoCH with displacement ----------
        for d in (1, -1):
            if (flags["choch_up" if d == 1 else "choch_down"][t] and last_sweep[d] is not None
                    and t - last_sweep[d] <= s["amd_bars"]):
                sw_t = last_sweep[d]
                if consol[max(0, sw_t - s["amd_consolidation_bars"]):sw_t].any():
                    add(t, "AMD", d, info=f"consolidation -> sweep ({t - sw_t} candle(s) ago) -> CHoCH")

        # ---------- 5. order blocks: retest, invalidation, breaker retest ----------
        for ob in obs:
            if ob["born"] >= t:
                continue
            if ob["state"] == "active":
                closed_through = c[t] < ob["low"] if ob["dir"] == 1 else c[t] > ob["high"]
                if closed_through:
                    ob["state"] = "breaker"
                    ob["retested"] = False
                    add(t, "OB_INVALID", ob["dir"], lo=ob["low"], hi=ob["high"],
                        info="closed through the order block - it becomes a breaker")
                    continue
                touched = l[t] <= ob["high"] if ob["dir"] == 1 else h[t] >= ob["low"]
                if touched and not ob["retested"]:
                    ob["retested"] = True
                    add(t, "OB_RETEST", ob["dir"], lo=ob["low"], hi=ob["high"], info="first return into the order block")
            elif ob["state"] == "breaker" and not ob["retested"]:
                # a failed bullish OB is retested from BELOW (and the other way round)
                touched = h[t] >= ob["low"] if ob["dir"] == 1 else l[t] <= ob["high"]
                if touched:
                    ob["retested"] = True
                    add(t, "BREAKER_RETEST", -ob["dir"], lo=ob["low"], hi=ob["high"],
                        info="failed order block retested from the other side")
        obs = [ob for ob in obs if not (ob["state"] == "breaker" and ob["retested"])][-s["max_open"]:]

        # ---------- 6. fair value gaps: new, first retrace, filled ----------
        for g in fvgs:
            if g["born"] >= t:
                continue
            if g["dir"] == 1:
                if not g["retraced"] and l[t] <= g["high"]:
                    g["retraced"] = True
                    add(t, "FVG_RETRACE", 1, lo=g["low"], hi=g["high"], info="first retrace into the gap")
                    flags["fvg_retrace_bull"][t] = True
                if l[t] <= g["low"]:
                    g["filled"] = True
                    add(t, "FVG_FILLED", 1, lo=g["low"], hi=g["high"])
            else:
                if not g["retraced"] and h[t] >= g["low"]:
                    g["retraced"] = True
                    add(t, "FVG_RETRACE", -1, lo=g["low"], hi=g["high"], info="first retrace into the gap")
                    flags["fvg_retrace_bear"][t] = True
                if h[t] >= g["high"]:
                    g["filled"] = True
                    add(t, "FVG_FILLED", -1, lo=g["low"], hi=g["high"])
        fvgs = [g for g in fvgs if not g.get("filled")][-s["max_open"]:]
        if t >= 2 and np.isfinite(atr[t]) and atr[t] > 0:
            if l[t] > h[t - 2] and (l[t] - h[t - 2]) >= s["fvg_atr"] * atr[t]:
                fvgs.append(dict(dir=1, low=h[t - 2], high=l[t], born=t, retraced=False))
                add(t, "FVG", 1, lo=h[t - 2], hi=l[t], size=(l[t] - h[t - 2]) / atr[t])
            elif h[t] < l[t - 2] and (l[t - 2] - h[t]) >= s["fvg_atr"] * atr[t]:
                fvgs.append(dict(dir=-1, low=h[t], high=l[t - 2], born=t, retraced=False))
                add(t, "FVG", -1, lo=h[t], hi=l[t - 2], size=(l[t - 2] - h[t]) / atr[t])

        # ---------- 7. context known at the close of this candle ----------
        ctx["sweep_bull_low"][t], ctx["sweep_bear_high"][t] = sweep_ext[1], sweep_ext[-1]
        if last_sh and last_sl and last_sh["level"] > last_sl["level"]:
            ctx["range_low"][t], ctx["range_high"][t] = last_sl["level"], last_sh["level"]
            ctx["range_pos"][t] = (c[t] - last_sl["level"]) / (last_sh["level"] - last_sl["level"])
        for side, name in ((1, "bull"), (-1, "bear")):
            act = [ob for ob in obs if ob["dir"] == side and ob["state"] == "active"]
            if act:
                ctx[name + "_ob_low"][t], ctx[name + "_ob_high"][t] = act[-1]["low"], act[-1]["high"]
            ctx["in_" + name + "_ob"][t] = any(ob["born"] < t and l[t] <= ob["high"] and h[t] >= ob["low"]
                                               for ob in act)
        up = [p["level"] for p in pools if p["side"] == 1 and p["level"] > c[t]]
        dn = [p["level"] for p in pools if p["side"] == -1 and p["level"] < c[t]]
        ctx["liq_above"][t] = min(up) if up else np.nan
        ctx["liq_below"][t] = max(dn) if dn else np.nan

    # ---------- state at the newest candle ----------
    last = n - 1
    price = c[last] if n else np.nan
    rng = None
    if last_sh and last_sl and last_sh["level"] > last_sl["level"]:
        pos = (price - last_sl["level"]) / (last_sh["level"] - last_sl["level"])
        rng = dict(high=float(last_sh["level"]), low=float(last_sl["level"]), position=float(pos),
                   zone="above the range" if pos > 1 else "below the range" if pos < 0 else
                   "premium" if pos > 0.5 else "discount")
    above = sorted((p for p in pools if p["side"] == 1 and p["level"] > price), key=lambda p: p["level"])
    below = sorted((p for p in pools if p["side"] == -1 and p["level"] < price), key=lambda p: -p["level"])
    a_last = atr[last] if n and np.isfinite(atr[last]) else np.nan
    pool_view = lambda p: dict(kind=p["kind"], level=float(p["level"]),
                               dist_atr=None if not np.isfinite(a_last) else round(float(abs(p["level"] - price) / a_last), 2))
    state = dict(
        trend=trend, last_break=None if last_break is None else dict(
            kind=last_break["kind"], dir=last_break["dir"], level=float(last_break["level"]),
            candles_ago=last - last_break["t"]),
        dealing_range=rng,
        ote=None if ote is None else dict(dir=ote["dir"], low=float(ote["low"]), high=float(ote["high"]),
                                          candles_ago=last - ote["t"]),
        liquidity_above=[pool_view(p) for p in above[:3]], liquidity_below=[pool_view(p) for p in below[:3]],
        open_fvgs=[dict(dir=g["dir"], low=float(g["low"]), high=float(g["high"]), retraced=g["retraced"],
                        candles_ago=last - g["born"]) for g in fvgs[-5:]],
        order_blocks=[dict(dir=ob["dir"], low=float(ob["low"]), high=float(ob["high"]), state=ob["state"],
                           candles_ago=last - ob["born"]) for ob in obs[-5:]],
        last_sweep={("bull" if d == 1 else "bear"): (None if last_sweep[d] is None else last - last_sweep[d])
                    for d in (1, -1)},
        killzone_now=killzone(int(ot[last]), s["killzones"]) if n and kz_on else None,
    )
    series = pd.DataFrame(flags)
    for k in CONTEXT_COLUMNS:
        series[k] = ctx[k]
    return dict(events=events, series=series, state=state)
