"""
The operator's scalping playbook (docs/playbook/Crypto_Scalping_Playbook.txt, docs/PLAYBOOK.md) as building blocks.
(Not to be confused with engine/playbook.py, the research run's regime playbook.)

Every definition is the playbook's own, with its numbers. Everything is computed on CLOSED candles and every value
at a 5m candle uses only what was known at that candle's close: higher timeframes = their last CLOSED candle,
swing points only after their confirmation candles, the daily / weekly / Asia levels only once their period ended.

  compute(d5, d15, d1h, d4h=None, btc15=None, delta=None, oi=None, funding=None, P=None)
      -> dict of numpy arrays, one value per 5m candle (the column names below)

Context    pb_trend / pb_range / pb_transition (1H regime, section 3.2), pb_bias_bull / pb_bias_bear (1H bias, 3.3),
           pb_sess_asia / _london / _ny / _late (UTC sessions, 2.3), pb_vwap_crosses (24 x 15m), pb_funding_ok_long /
           _short (section 5.4: funding above +0.05% / below -0.05% per 8h blocks that side), pb_btc_ok_long / _short
           (2.2: no altcoin long while BTC's 15m structure breaks down, and vice versa)
Strategy A pbA_long / pbA_short (5.1) with pbA_entry_*, pbA_stop_*, pbA_tp2_*, pbA_inval_*; pbA_cvd_long / _short
           (the optional CVD confirmation: the trigger candle's delta is positive / negative)
Strategy B pbB_long / pbB_short (5.2, OI confirmation only) and pbB_cvd_long / _short (any of CVD divergence,
           absorption or the OI drop), pbB_stop_*, pbB_tp2_*, pbB_inval_*, pbB_half (trend regime: half size)
Strategy C pbC_long / pbC_short (5.3) and pbC_cvd_long / _short (+ CVD not making a new low / high on the retest),
           pbC_stop_*, pbC_tp2_*, pbC_inval_*
1 = true, 0 = false, NaN = unknown (a rule reading NaN is false). Pure: no internet, no files.
"""
import numpy as np
import pandas as pd

from engine import features as fe
from engine.timeframes import align_higher

DEFAULTS = dict(
    adx_trend=25.0, adx_range=20.0, slope_bars=10, slope_atr=0.1,       # 3.2 regime
    vwap_cross_bars=24, vwap_crosses=4,                                  # 3.2 range / 5.4 chop
    swing_5m=3, swing_15m=3, swing_1h=5, swing_4h=5,                     # 4.2 pivots
    swing_memory=480,                 # unbroken 1H / 4H swings count for 480 candles (20 / 80 days): the live watcher
                                      # keeps 500 candles, so live and backtest see the same levels
    zone_atr=0.25,                                                       # 2.4 level zone = level +- 0.25 x ATR(15m)
    rej_wick=0.6, rej_close=0.67, rej_range_atr=0.6,                     # 4.3 rejection candle
    engulf_body=1.2, vol_spike=1.5,                                      # 4.3 engulfing / volume spike
    funding_max=0.05,                                                    # 5.4 funding extreme (% per 8h)
    # Strategy A (5.1)
    a_level_atr=0.5, a_depth_atr=0.8, a_trig_vol=1.2, a_small_atr=0.8,
    a_stop_buffer=0.1, a_stop_atr=1.5, a_stop_min_atr=0.8,
    # Strategy B (5.2)
    b_sweep_atr=0.1, b_back_bars=3, b_oi_drop=1.0, b_absorb_x=1.5, b_range_bars=24, b_eq_atr=0.1,
    # Strategy C (5.3)
    c_comp_atr=0.8, c_comp_bars=8, c_comp_box=1.2, c_under_atr=0.5, c_break_atr=0.2, c_break_body=0.6,
    c_retest_bars=12, c_stop_atr=0.5, c_inval_atr=0.3,
)
# sessions (UTC hour ranges) - section 2.3; which strategy may trade in which session
SESSIONS = dict(asia=(0.0, 7.0), london=(7.0, 10.0), ny=(13.0, 16.0))     # ny = NY open + London/NY overlap
SESSION_OPEN = dict(london=(7.0, 8.0), ny=(13.5, 14.5))                   # "near a session open" (5.3)
LATE_FROM = 20.0                                                          # late US: 20:00 UTC onwards
H_MS = 3_600_000
DAY_MS = 86_400_000


def settings(section=None):
    s = dict(DEFAULTS)
    s.update({k: v for k, v in (section or {}).items() if k in DEFAULTS})
    return s


# ---------------------------------------------------------------- basic series
def _wilder(x, n):
    return pd.Series(x).ewm(alpha=1 / n, adjust=False, min_periods=n).mean().to_numpy()


def _ema(x, n):
    return pd.Series(x).ewm(span=n, adjust=False, min_periods=n).mean().to_numpy()


def _sma(x, n):
    return pd.Series(x).rolling(n, min_periods=n).mean().to_numpy()


def atr(df, n=14):
    h, l, c = (df[k].to_numpy(dtype=float) for k in ("high", "low", "close"))
    pc = np.r_[np.nan, c[:-1]]
    tr = np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0)
    return _wilder(tr, n)


def adx(df, n=14):
    h, l = df["high"].to_numpy(dtype=float), df["low"].to_numpy(dtype=float)
    up, dn = np.r_[np.nan, np.diff(h)], -np.r_[np.nan, np.diff(l)]
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    mdm = np.where((dn > up) & (dn > 0), dn, 0.0)
    a = atr(df, n)
    pdi, mdi = 100 * _wilder(pdm, n) / a, 100 * _wilder(mdm, n) / a
    with np.errstate(invalid="ignore", divide="ignore"):
        dx = 100 * np.abs(pdi - mdi) / np.where(pdi + mdi == 0, np.nan, pdi + mdi)
    return _wilder(dx, n)


def daily_vwap(df):
    """VWAP anchored at 00:00 UTC (section 4.1)."""
    tp = ((df["high"] + df["low"] + df["close"]) / 3).to_numpy(dtype=float)
    v = df["volume"].to_numpy(dtype=float)
    day = df["open_time"].to_numpy(dtype=np.int64) // DAY_MS
    s = pd.DataFrame({"pv": tp * v, "v": v, "d": day})
    g = s.groupby("d")
    with np.errstate(invalid="ignore", divide="ignore"):
        return (g["pv"].cumsum() / g["v"].cumsum().replace(0, np.nan)).to_numpy()


def swings(h, l, n):
    """Confirmed pivots (section 4.2): (idx_high, val_high, idx_low, val_low) of the LAST confirmed swing high / low
    known at each candle's close. A pivot at i is confirmed at i + n."""
    m = len(h)
    ih, vh, il, vl = (np.full(m, np.nan) for _ in range(4))
    lh = lvh = ll = lvl = np.nan
    for j in range(m):
        i = j - n
        if i - n >= 0:
            wh, wl = h[i - n:i + n + 1], l[i - n:i + n + 1]
            if h[i] >= wh.max() and (wh == h[i]).sum() == 1:
                lh, lvh = i, h[i]
            if l[i] <= wl.min() and (wl == l[i]).sum() == 1:
                ll, lvl = i, l[i]
        ih[j], vh[j], il[j], vl[j] = lh, lvh, ll, lvl
    return ih, vh, il, vl


def structure(df, n):
    """Market structure events (section 4.2) at each close. Returns (bias_event, seq): bias_event = +1 after a
    bullish BOS, -1 after a bearish BOS, 0 after a CHoCH (a warning) - the LAST event so far; seq = +1 / -1 / 0 the
    current up / down / unclear sequence (higher highs and higher lows / lower highs and lower lows)."""
    h, l, c = (df[k].to_numpy(dtype=float) for k in ("high", "low", "close"))
    m = len(c)
    ev, sq = np.zeros(m), np.zeros(m)
    highs, lows = [], []                     # confirmed swing values, in order
    last_ev, broken_h, broken_l = 0.0, None, None
    for j in range(m):
        i = j - n
        if i - n >= 0:
            wh, wl = h[i - n:i + n + 1], l[i - n:i + n + 1]
            if h[i] >= wh.max() and (wh == h[i]).sum() == 1:
                highs.append(h[i])
                broken_h = None
            if l[i] <= wl.min() and (wl == l[i]).sum() == 1:
                lows.append(l[i])
                broken_l = None
        s = 0
        if len(highs) >= 2 and len(lows) >= 2:
            if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
                s = 1
            elif highs[-1] < highs[-2] and lows[-1] < lows[-2]:
                s = -1
        if highs and broken_h is None and c[j] > highs[-1]:
            broken_h = highs[-1]
            last_ev = 1.0 if s == 1 else (0.0 if s == -1 else last_ev)    # BOS up / CHoCH up
        if lows and broken_l is None and c[j] < lows[-1]:
            broken_l = lows[-1]
            last_ev = -1.0 if s == -1 else (0.0 if s == 1 else last_ev)  # BOS down / CHoCH down
        ev[j], sq[j] = last_ev, s
    return ev, sq


def _on5(d5, df, cols):
    """Columns of the newest CLOSED candle of df at each 5m close (no look-ahead)."""
    return align_higher(d5, df.assign(**cols), list(cols)).to_dict("series")


def _hour(open_ms):
    return (np.asarray(open_ms, dtype=np.int64) % DAY_MS) / H_MS


# ---------------------------------------------------------------- context (sections 2-3)
def regime_1h(d1h, P):
    """1H regime (3.2): trend = ADX >= 25 AND |EMA50 slope over 10 bars| >= 0.1 x ATR per bar AND price on the slope's
    side of EMA200; range = ADX <= 20 OR 4+ VWAP crosses in the last 24 x 15m candles; else transition.
    The crossings make it a range even when the trend conditions hold (price chopping around VWAP is not a trend).
    Bias (3.3): bullish = close > EMA200, EMA50 > EMA200 and the last 1H structure event a bullish BOS."""
    c = d1h["close"].to_numpy(dtype=float)
    ax, e50, e200, a = adx(d1h), _ema(c, 50), _ema(c, 200), atr(d1h)
    k = int(P["slope_bars"])
    slope = (e50 - np.r_[np.full(k, np.nan), e50[:-k]]) / k
    up = (slope >= P["slope_atr"] * a) & (c > e200)
    dn = (slope <= -P["slope_atr"] * a) & (c < e200)
    trend_1h = (ax >= P["adx_trend"]) & (up | dn)
    ev, _ = structure(d1h, int(P["swing_1h"]))
    bull = (c > e200) & (e50 > e200) & (ev == 1)
    bear = (c < e200) & (e50 < e200) & (ev == -1)
    known = np.isfinite(ax) & np.isfinite(e200)
    return dict(trend_1h=np.where(known, trend_1h, np.nan), adx_low=np.where(known, ax <= P["adx_range"], np.nan),
                bull=np.where(known, bull, np.nan), bear=np.where(known, bear, np.nan))


def vwap_crosses(d15, n):
    c = d15["close"].to_numpy(dtype=float)
    vw = daily_vwap(d15)
    side = np.sign(c - vw)
    cross = (side != np.r_[np.nan, side[:-1]]) & np.isfinite(side) & np.isfinite(np.r_[np.nan, side[:-1]]) & (side != 0)
    return pd.Series(cross.astype(float)).rolling(n, min_periods=n).sum().to_numpy()


# ---------------------------------------------------------------- levels (section 2.4)
def day_levels(d5, d15, d1d=None):
    """PDH / PDL, weekly / monthly open, previous week high / low, today's Asia high / low (only after 07:00 UTC),
    the previous UTC day's volume profile (POC / VAH / VAL from its 15m candles). All as known at each 5m close.
    The day / week / month levels come from the daily candles when given (the live watcher keeps 500 of them but
    only ~41 hours of 5m candles), else from the 5m candles themselves."""
    ot = d5["open_time"].to_numpy(dtype=np.int64)
    day = ot // DAY_MS
    own = pd.DataFrame({"d": day, "o": d5["open"].to_numpy(float), "h": d5["high"].to_numpy(float),
                        "l": d5["low"].to_numpy(float)}).groupby("d").agg(o=("o", "first"), h=("h", "max"),
                                                                           l=("l", "min"), n=("o", "size"))
    own = own[own["n"] >= 288].drop(columns="n")            # whole days of this market's own 5m candles first ...
    if d1d is not None and len(d1d):                        # ... the daily candles for the days before them
        dd = pd.DataFrame({"d": d1d["open_time"].to_numpy(dtype=np.int64) // DAY_MS, "o": d1d["open"].to_numpy(float),
                           "h": d1d["high"].to_numpy(float), "l": d1d["low"].to_numpy(float)}).set_index("d")
        days = pd.concat([dd[~dd.index.isin(own.index)], own]).sort_index()
    else:
        days = own
    if not len(days):
        days = pd.DataFrame({"o": [np.nan], "h": [np.nan], "l": [np.nan]}, index=[int(day.min())])
    full = days.reindex(np.arange(min(days.index.min(), day.min()), max(days.index.max(), day.max()) + 1))
    first5 = pd.Series(d5["open"].to_numpy(float), index=day).groupby(level=0).first()
    full["o"] = full["o"].fillna(first5.reindex(full.index))   # today's open: its first 5m candle
    prev = full.shift(1)                                    # the previous day's high / low (fully closed)
    out = dict(pdh=prev["h"].reindex(day).to_numpy(), pdl=prev["l"].reindex(day).to_numpy())
    wk_of = (full.index.to_numpy() + 3) // 7                # 1970-01-01 was a Thursday: weeks start on Monday
    mo_of = pd.to_datetime(full.index.to_numpy() * DAY_MS, unit="ms").to_period("M").astype(str).to_numpy()
    f = full.assign(w=wk_of, m=mo_of)
    w_open = f.groupby("w")["o"].first()                    # the open of the week's first day (known at its start)
    m_open = f.groupby("m")["o"].first()
    wk = f.groupby("w").agg(h=("h", "max"), l=("l", "min")).shift(1)
    week = (day + 3) // 7
    month = pd.to_datetime(ot, unit="ms").to_period("M").astype(str).to_numpy()
    out["wk_open"] = w_open.reindex(week).to_numpy()
    out["mo_open"] = m_open.reindex(month).to_numpy()
    out["pwh"], out["pwl"] = wk["h"].reindex(week).to_numpy(), wk["l"].reindex(week).to_numpy()
    h, l = d5["high"].to_numpy(dtype=float), d5["low"].to_numpy(dtype=float)
    hour = _hour(ot)
    asia = hour < SESSIONS["asia"][1]
    a = pd.DataFrame({"d": day, "h": np.where(asia, h, np.nan), "l": np.where(asia, l, np.nan)}).groupby("d").max()
    al = pd.DataFrame({"d": day, "l": np.where(asia, l, np.nan)}).groupby("d")["l"].min()
    done = hour >= SESSIONS["asia"][1]                      # the Asia range is known once Asia is over
    out["asia_h"] = np.where(done, a["h"].reindex(day).to_numpy(), np.nan)
    out["asia_l"] = np.where(done, al.reindex(day).to_numpy(), np.nan)
    # previous day's volume profile on 15m
    t15 = d15["open_time"].to_numpy(dtype=np.int64) // DAY_MS
    tp = ((d15["high"] + d15["low"] + d15["close"]) / 3).to_numpy(dtype=float)
    v15 = d15["volume"].to_numpy(dtype=float)
    vp = {}
    for d in np.unique(t15):
        idx = np.flatnonzero(t15 == d)
        if len(idx) >= 48:                                  # at least half a day of candles
            p, va, vl = fe.volume_profile(tp[idx], v15[idx], len(idx))
            vp[d + 1] = (p[-1], va[-1], vl[-1])             # used on the NEXT day
    for j, name in enumerate(("poc", "vah", "val")):
        out[name] = np.array([vp.get(d, (np.nan,) * 3)[j] for d in day])
    return out


def unbroken_swings(df, n, memory=480):
    """(nearest unbroken confirmed swing high ABOVE the close, nearest unbroken swing low BELOW) at each close; only
    swings confirmed within the last `memory` candles (no dependence on how far back the history starts)."""
    h, l, c = (df[k].to_numpy(dtype=float) for k in ("high", "low", "close"))
    m = len(c)
    above, below = np.full(m, np.nan), np.full(m, np.nan)
    highs, lows = [], []
    for j in range(m):
        i = j - n
        if i - n >= 0:
            if h[i] >= h[i - n:i + n + 1].max() and (h[i - n:i + n + 1] == h[i]).sum() == 1:
                highs.append((j, h[i]))
            if l[i] <= l[i - n:i + n + 1].min() and (l[i - n:i + n + 1] == l[i]).sum() == 1:
                lows.append((j, l[i]))
        highs = [x for x in highs if x[1] >= c[j] and x[0] > j - memory]   # a close above breaks a swing high
        lows = [x for x in lows if x[1] <= c[j] and x[0] > j - memory]
        above[j] = min(x[1] for x in highs) if highs else np.nan
        below[j] = max(x[1] for x in lows) if lows else np.nan
    return above, below


def round_levels(price):
    """Round numbers (2.4): steps of 10^(digits - 2) - BTC 60,000 -> 1,000; ETH 2,500 -> 100; SOL 150 -> 10."""
    p = np.asarray(price, dtype=float)
    with np.errstate(invalid="ignore", divide="ignore"):
        step = 10.0 ** (np.floor(np.log10(np.where(p > 0, p, np.nan))) - 1)
    return np.floor(p / step) * step, np.ceil(p / step) * step


# ---------------------------------------------------------------- candles (section 4.3)
def candles(df, a, P):
    o, h, l, c, v = (df[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close", "volume"))
    rng = h - l
    with np.errstate(invalid="ignore", divide="ignore"):
        lw, uw = (np.minimum(o, c) - l) / rng, (h - np.maximum(o, c)) / rng
        cl = (c - l) / rng
    big = rng >= P["rej_range_atr"] * a
    body, pb = np.abs(c - o), np.abs(np.r_[np.nan, c[:-1]] - np.r_[np.nan, o[:-1]])
    po, pc = np.r_[np.nan, o[:-1]], np.r_[np.nan, c[:-1]]
    vavg = _sma(v, 20)
    return dict(
        bull_rej=(lw >= P["rej_wick"]) & (cl >= P["rej_close"]) & big,
        bear_rej=(uw >= P["rej_wick"]) & (cl <= 1 - P["rej_close"]) & big,
        bull_eng=(c > po) & (o <= pc) & (body >= P["engulf_body"] * pb) & (pc < po),
        bear_eng=(c < po) & (o >= pc) & (body >= P["engulf_body"] * pb) & (pc > po),
        vavg=vavg, rng=rng, body=body)


# ---------------------------------------------------------------- the whole playbook on 5m
def compute(d5, d15, d1h, d4h=None, btc15=None, delta=None, oi=None, funding=None, P=None, d1d=None):
    P = settings(P)
    n = len(d5)
    o, h, l, c, v = (d5[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close", "volume"))
    ot = d5["open_time"].to_numpy(dtype=np.int64)
    a5, e9 = atr(d5), _ema(c, 9)
    vw5 = daily_vwap(d5)
    cd = candles(d5, a5, P)
    out = {}

    # --- 15m: ATR, EMA21, VWAP, compression, pullbacks, ranges (the last CLOSED 15m candle) ---
    a15 = atr(d15)
    c15, h15, l15, v15 = (d15[k].to_numpy(dtype=float) for k in ("close", "high", "low", "volume"))
    e21, vw15 = _ema(c15, 21), daily_vwap(d15)
    m15 = len(c15)
    nb = int(P["c_comp_bars"])
    box_h = pd.Series(h15).rolling(nb, min_periods=nb).max().to_numpy()
    box_l = pd.Series(l15).rolling(nb, min_periods=nb).min().to_numpy()
    comp = (a15 < P["c_comp_atr"] * _sma(a15, 50)) & ((box_h - box_l) <= P["c_comp_box"] * a15)
    rb = int(P["b_range_bars"])
    rng_hi = pd.Series(h15).rolling(rb, min_periods=rb).max().to_numpy()
    rng_lo = pd.Series(l15).rolling(rb, min_periods=rb).min().to_numpy()
    crosses = vwap_crosses(d15, int(P["vwap_cross_bars"]))
    ih, vh, il, vl = swings(h15, l15, int(P["swing_15m"]))
    pull = _pullbacks(h15, l15, v15, a15, ih, vh, il, vl, P)
    # equal lows / highs: the last two confirmed 15m swing lows (highs) within 0.1 x ATR(15m) of each other
    eq_l, eq_h = np.full(m15, np.nan), np.full(m15, np.nan)
    prev_l = pd.Series(vl).where(pd.Series(vl).diff() != 0).ffill().shift(1).to_numpy()
    prev_h = pd.Series(vh).where(pd.Series(vh).diff() != 0).ffill().shift(1).to_numpy()
    with np.errstate(invalid="ignore"):
        ok_l, ok_h = np.abs(vl - prev_l) <= P["b_eq_atr"] * a15, np.abs(vh - prev_h) <= P["b_eq_atr"] * a15
    eq_l[ok_l], eq_h[ok_h] = ((vl + prev_l) / 2)[ok_l], ((vh + prev_h) / 2)[ok_h]
    ot15 = d15["open_time"].to_numpy(dtype=np.int64)
    sw_l_t = np.where(np.isfinite(il), ot15[np.nan_to_num(il, nan=0).astype(int)], np.nan)
    sw_h_t = np.where(np.isfinite(ih), ot15[np.nan_to_num(ih, nan=0).astype(int)], np.nan)
    f15 = dict(a15=a15, e21=e21, vw15=vw15, comp=comp.astype(float), box_h=box_h, box_l=box_l, rng_hi=rng_hi,
               rng_lo=rng_lo, crosses=crosses, eq_l=eq_l, eq_h=eq_h, sw_l=vl, sw_h=vh, sw_l_t=sw_l_t, sw_h_t=sw_h_t,
               **pull)
    if btc15 is not None and len(btc15):
        bev, bsq = structure(btc15, int(P["swing_15m"]))
    s15 = _on5(d5, d15, f15)
    if btc15 is not None and len(btc15):
        sb = _on5(d5, btc15, dict(btc_ev=bev, btc_sq=bsq))
    # --- 1H regime / bias, 1H and 4H unbroken swings ---
    r1 = regime_1h(d1h, P)
    sw1_up, sw1_dn = unbroken_swings(d1h, int(P["swing_1h"]), int(P["swing_memory"]))
    s1 = _on5(d5, d1h, dict(**r1, sw1_up=sw1_up, sw1_dn=sw1_dn))
    if d4h is not None and len(d4h):
        sw4_up, sw4_dn = unbroken_swings(d4h, int(P["swing_4h"]), int(P["swing_memory"]))
        s4 = _on5(d5, d4h, dict(sw4_up=sw4_up, sw4_dn=sw4_dn))
    else:
        s4 = dict(sw4_up=np.full(n, np.nan), sw4_dn=np.full(n, np.nan))
    g = lambda d, k: np.asarray(d[k], dtype=float)          # noqa: E731

    known = np.isfinite(g(s1, "trend_1h")) & np.isfinite(g(s15, "crosses"))
    many = g(s15, "crosses") >= P["vwap_crosses"]
    trend = known & (g(s1, "trend_1h") == 1) & ~many
    rangeg = known & ((g(s1, "adx_low") == 1) | many)
    trans = known & ~trend & ~rangeg
    bull, bear = g(s1, "bull") == 1, g(s1, "bear") == 1
    for k, x in dict(pb_trend=trend, pb_range=rangeg, pb_transition=trans, pb_bias_bull=bull & known,
                     pb_bias_bear=bear & known).items():
        out[k] = np.where(known, x, np.nan)
    out["pb_vwap_crosses"] = g(s15, "crosses")

    # --- sessions (UTC) ---
    hr = _hour(ot)
    dow = ((ot // DAY_MS) + 3) % 7                          # 0 = Monday ... 5 = Saturday, 6 = Sunday
    sess = {k: (hr >= a0) & (hr < a1) for k, (a0, a1) in SESSIONS.items()}
    near_open = np.zeros(n, bool)
    for a0, a1 in SESSION_OPEN.values():
        near_open |= (hr >= a0) & (hr < a1)
    late = (hr >= LATE_FROM) | (dow >= 5)
    for k, x in sess.items():
        out[f"pb_sess_{k}"] = x.astype(float)
    out["pb_late"] = late.astype(float)

    # --- funding / BTC filters (5.4, 2.2) ---
    fr = np.asarray(funding, dtype=float) if funding is not None else np.full(n, np.nan)
    out["pb_funding_ok_long"] = np.where(np.isfinite(fr), fr <= P["funding_max"], 1.0)
    out["pb_funding_ok_short"] = np.where(np.isfinite(fr), fr >= -P["funding_max"], 1.0)
    if btc15 is not None and len(btc15):
        bev_, bsq_ = g(sb, "btc_ev"), g(sb, "btc_sq")
        down = (bev_ == -1) | ((bev_ == 0) & (bsq_ == 1))   # bearish BOS, or a CHoCH out of an up-sequence
        up = (bev_ == 1) | ((bev_ == 0) & (bsq_ == -1))
        out["pb_btc_ok_long"], out["pb_btc_ok_short"] = (~down).astype(float), (~up).astype(float)
    else:                                                   # BTC itself (or no BTC data): nothing to conflict with
        out["pb_btc_ok_long"], out["pb_btc_ok_short"] = np.ones(n), np.ones(n)

    # --- levels (2.4) ---
    lv = day_levels(d5, d15, d1d)
    rd, ru = round_levels(c)
    levels = dict(lv, sw1_up=g(s1, "sw1_up"), sw1_dn=g(s1, "sw1_dn"), sw4_up=g(s4, "sw4_up"),
                  sw4_dn=g(s4, "sw4_dn"), rnd_dn=rd, rnd_up=ru)
    a15_5 = g(s15, "a15")
    L = np.vstack([np.asarray(x, dtype=float) for x in levels.values()])
    major_lo = np.vstack([levels[k] for k in ("pdl", "asia_l", "pwl", "wk_open")])
    major_hi = np.vstack([levels[k] for k in ("pdh", "asia_h", "pwh", "wk_open")])
    for k in ("pdh", "pdl", "asia_h", "asia_l", "poc", "vah", "val"):
        out[f"pb_{k}"] = np.asarray(levels[k], dtype=float)
    out["pb_vwap"] = vw5

    # --- Strategy A: trend pullback (5.1) ---
    for d, side in ((1, "long"), (-1, "short")):
        sfx = "l" if d == 1 else "s"
        ok_pull = g(s15, f"pull_ok_{sfx}") == 1
        pl = g(s15, f"pull_px_{sfx}")                      # the pullback low (long) / high (short)
        imp = g(s15, f"imp_px_{sfx}")                      # the impulse high (long) / low (short) = previous swing
        zlo = np.fmin(g(s15, "e21"), g(s15, "vw15"))
        zhi = np.fmax(g(s15, "e21"), g(s15, "vw15"))
        touched = (pl <= zhi) if d == 1 else (pl >= zlo)    # the pullback reached the EMA21 / VWAP zone
        gap = np.where(L > zhi, L - zhi, np.where(L < zlo, zlo - L, 0.0))
        near = np.nanmin(np.where(np.isfinite(L), gap, np.inf), axis=0) <= P["a_level_atr"] * a15_5
        trig_c = (cd["bull_rej"] | cd["bull_eng"]) if d == 1 else (cd["bear_rej"] | cd["bear_eng"])
        trig = trig_c & ((c > e9) if d == 1 else (c < e9)) & (v >= P["a_trig_vol"] * cd["vavg"])
        regime_ok = trend & (bull if d == 1 else bear)
        sig = regime_ok & sess["ny"] & ok_pull & touched & near & trig
        mid = (h + l) / 2
        entry = np.where(cd["rng"] >= P["a_small_atr"] * a5, mid, np.nan)   # small candle: market (NaN)
        e_est = np.where(np.isfinite(entry), entry, c)
        s1_ = pl - d * P["a_stop_buffer"] * a5
        s2_ = e_est - d * P["a_stop_atr"] * a5
        stop = np.maximum(s1_, s2_) if d == 1 else np.minimum(s1_, s2_)      # the tighter of the two ...
        floor = e_est - d * P["a_stop_min_atr"] * a5
        stop = np.minimum(stop, floor) if d == 1 else np.maximum(stop, floor)  # ... but at least 0.8 x ATR(5m)
        nxt = _next_level(L, e_est, d)
        tp2 = np.where(d * (imp - e_est) > 0, imp, nxt)
        dl = delta if delta is not None else np.full(n, np.nan)
        out[f"pbA_{side}"] = sig.astype(float)
        out[f"pbA_cvd_{side}"] = np.where(np.isfinite(dl), d * dl > 0, np.nan)
        out[f"pbA_entry_{side}"], out[f"pbA_stop_{side}"], out[f"pbA_tp2_{side}"] = entry, stop, tp2
        out[f"pbA_inval_{side}"] = pl

    # --- Strategy B: liquidity sweep reversal (5.2) and Strategy C: breakout and retest (5.3) ---
    cvd = _cvd(delta, ot) if delta is not None else np.full(n, np.nan)
    oi_chg = _oi_change(oi, n)
    b = _strategy_b(o, h, l, c, ot, a5, cd, cvd, delta, oi_chg, levels, major_lo, major_hi, s15, trend, rangeg,
                    trans, bull, bear, sess, P)
    cc = _strategy_c(h, l, c, v, a5, cd, cvd, L, s15, trend, rangeg, trans, bull, bear, sess, near_open, P)
    out.update(b)
    out.update(cc)
    return out


def _next_level(L, price, d):
    """The nearest marked level beyond price in direction d (NaN if none)."""
    with np.errstate(invalid="ignore"):
        ahead = np.where(d * (L - price) > 0, L, np.nan)
    if d == 1:
        return np.where(np.isfinite(ahead).any(axis=0), np.nanmin(np.where(np.isfinite(ahead), ahead, np.inf), axis=0),
                        np.nan)
    return np.where(np.isfinite(ahead).any(axis=0), np.nanmax(np.where(np.isfinite(ahead), ahead, -np.inf), axis=0),
                    np.nan)


def _pullbacks(h, l, v, a, ih, vh, il, vl, P):
    """Strategy A's 15m pullback (5.1), both directions, at each 15m close. Long: the impulse = from the last
    confirmed swing low (the higher low) up to the highest high since; the pullback = the candles after that high.
    OK when the pullback is >= 0.8 x ATR(15m) deep, on lower average volume than the impulse, and has not broken the
    higher low. Short = mirror."""
    m = len(h)
    out = {k: np.full(m, np.nan) for k in ("pull_ok_l", "pull_px_l", "imp_px_l", "pull_ok_s", "pull_px_s", "imp_px_s")}
    cv = np.r_[0.0, np.cumsum(np.nan_to_num(v))]
    for j in range(m):
        for d, sw_i, sw_v, sfx in ((1, il[j], vl[j], "l"), (-1, ih[j], vh[j], "s")):
            if not np.isfinite(sw_i):
                continue
            s = int(sw_i)
            seg = h[s:j + 1] if d == 1 else l[s:j + 1]
            k = s + int(np.argmax(seg) if d == 1 else np.argmin(seg))     # the impulse extreme
            if k >= j or k == s:
                continue
            pul = l[k + 1:j + 1] if d == 1 else h[k + 1:j + 1]
            px = pul.min() if d == 1 else pul.max()
            depth = (h[k] - px) if d == 1 else (px - l[k])
            vol_imp = (cv[k + 1] - cv[s]) / (k + 1 - s)
            vol_pul = (cv[j + 1] - cv[k + 1]) / (j - k)
            intact = (px > sw_v) if d == 1 else (px < sw_v)
            out[f"pull_ok_{sfx}"][j] = float(depth >= P["a_depth_atr"] * a[j] and vol_pul < vol_imp and intact)
            out[f"pull_px_{sfx}"][j] = px
            out[f"imp_px_{sfx}"][j] = h[k] if d == 1 else l[k]
    return out


def _cvd(delta, ot):
    """Cumulative volume delta, reset at 00:00 UTC (section 4.1). Unknown delta -> unknown CVD that day so far."""
    d = pd.Series(np.asarray(delta, dtype=float))
    day = pd.Series(np.asarray(ot, dtype=np.int64) // DAY_MS)
    return d.groupby(day).cumsum(skipna=False).to_numpy()


def _oi_change(oi, n):
    """Open-interest change over the last hour, in % (hourly data: the change known at each 5m close)."""
    if oi is None:
        return np.full(n, np.nan)
    x = pd.Series(np.asarray(oi, dtype=float))
    with np.errstate(invalid="ignore", divide="ignore"):
        return ((x / x.shift(12) - 1) * 100).to_numpy()


def _strategy_b(o, h, l, c, ot, a5, cd, cvd, delta, oi_chg, levels, major_lo, major_hi, s15, trend, rangeg, trans,
                bull, bear, sess, P):
    """Strategy B (5.2). Long: a 5m wick trades below a marked low (Asia low, PDL, VAL, the 24 x 15m range low or an
    equal-lows cluster) by >= 0.1 x ATR(5m), then a 5m candle closes back above it within 3 candles (signal on that
    close). Regime: range (with the 1H bias, or at a major level), transition (major levels only), trend (only
    against the trend at a major level - half size). Confirmation: OI drop >= 1% (pbB_*) or, with CVD
    (pbB_cvd_*), any of: OI drop, bullish CVD divergence at the sweep, an absorption candle at the sweep."""
    n = len(c)
    out = {}
    nb = int(P["b_back_bars"])
    lows = dict(asia_l=levels["asia_l"], pdl=levels["pdl"], val=levels["val"],
                rng_lo=np.asarray(s15["rng_lo"], dtype=float), eq_l=np.asarray(s15["eq_l"], dtype=float))
    highs = dict(asia_h=levels["asia_h"], pdh=levels["pdh"], vah=levels["vah"],
                 rng_hi=np.asarray(s15["rng_hi"], dtype=float), eq_h=np.asarray(s15["eq_h"], dtype=float))
    dl = np.asarray(delta, dtype=float) if delta is not None else np.full(n, np.nan)
    davg = pd.Series(np.abs(dl)).rolling(20, min_periods=10).mean().to_numpy()
    rng_mid = (np.asarray(s15["rng_hi"], dtype=float) + np.asarray(s15["rng_lo"], dtype=float)) / 2
    for d, side, lv_set, major in ((1, "long", lows, major_lo), (-1, "short", highs, major_hi)):
        sig = np.zeros(n, bool)
        lvl_sw = np.full(n, np.nan)
        ext = np.full(n, np.nan)                            # the sweep's wick extreme
        is_major = np.zeros(n, bool)
        for name, arr in lv_set.items():
            arr = np.asarray(arr, dtype=float)
            ref = np.r_[np.full(nb, np.nan), arr[:-nb]] if n > nb else np.full(n, np.nan)   # the level BEFORE
            for i in range(nb, n):
                L = ref[i]
                if not np.isfinite(L) or not np.isfinite(a5[i]) or d * (c[i] - L) <= 0:
                    continue
                if d * (c[i - 1] - L) > 0 and not _swept(d, h, l, a5, i, i, L, P):
                    continue                                # not the FIRST close back inside
                ks = [k for k in range(i - nb + 1, i + 1) if _swept(d, h, l, a5, k, k, L, P)]
                if not ks or any(d * (c[k] - L) > 0 for k in range(ks[0], i)):
                    continue
                w = (l[ks[0]:i + 1].min() if d == 1 else h[ks[0]:i + 1].max())
                if not sig[i] or d * (L - lvl_sw[i]) > 0:   # several levels: the outermost one swept
                    sig[i], lvl_sw[i], ext[i] = True, L, w
                    is_major[i] = bool(np.any(np.abs(major[:, i] - L) <= 1e-9 * max(abs(L), 1)))
        with_bias = bull if d == 1 else bear
        against = bear if d == 1 else bull
        reg_ok = (rangeg & (with_bias | is_major)) | (trans & is_major) | (trend & against & is_major)
        sess_ok = sess["asia"] | sess["london"] | sess["ny"]
        oi_ok = (oi_chg <= -P["b_oi_drop"]) & np.isfinite(oi_chg)
        k0 = np.maximum(np.arange(n) - nb + 1, 0)
        # CVD divergence (4.3): the sweep made a lower low (higher high) than the previous confirmed 15m swing low
        # (high) while the CVD made a higher low (lower high) than at that swing - the same UTC day only (CVD resets);
        # absorption: a strong opposite delta candle (>= 1.5 x the average |delta|) closing in its upper (lower) half
        prev_sw = np.asarray(s15["sw_l" if d == 1 else "sw_h"], dtype=float)
        prev_t = np.asarray(s15["sw_l_t" if d == 1 else "sw_h_t"], dtype=float)
        div = np.zeros(n, bool)
        absorb = np.zeros(n, bool)
        for i in np.flatnonzero(sig):
            seg = slice(k0[i], i + 1)
            if np.isfinite(cvd[seg]).all() and np.isfinite(prev_sw[i]) and np.isfinite(prev_t[i]):
                lower = (ext[i] < prev_sw[i]) if d == 1 else (ext[i] > prev_sw[i])
                j_ext = k0[i] + int(np.argmin(l[seg]) if d == 1 else np.argmax(h[seg]))
                a0 = int(np.searchsorted(ot, int(prev_t[i])))
                at_sw = cvd[a0:a0 + 3]                       # the 5m candles of that 15m swing candle
                same_day = a0 < n and ot[a0] // DAY_MS == ot[j_ext] // DAY_MS
                if lower and same_day and len(at_sw) and np.isfinite(at_sw).all():
                    div[i] = (cvd[j_ext] > at_sw.min()) if d == 1 else (cvd[j_ext] < at_sw.max())
            for k in range(k0[i], i + 1):
                rng = h[k] - l[k]
                if rng > 0 and np.isfinite(dl[k]) and np.isfinite(davg[k]) and abs(dl[k]) >= P["b_absorb_x"] * davg[k]:
                    if (d == 1 and dl[k] < 0 and c[k] >= l[k] + 0.5 * rng) or \
                            (d == -1 and dl[k] > 0 and c[k] <= h[k] - 0.5 * rng):
                        absorb[i] = True
        base = sig & reg_ok & sess_ok
        out[f"pbB_{side}"] = (base & oi_ok).astype(float)
        out[f"pbB_cvd_{side}"] = (base & (oi_ok | div | absorb)).astype(float)
        out[f"pbB_stop_{side}"] = ext - d * P["b_sweep_atr"] * a5
        cand = np.vstack([rng_mid, np.asarray(levels["poc"], dtype=float),
                          np.asarray(s15["rng_hi" if d == 1 else "rng_lo"], dtype=float)])
        out[f"pbB_tp2_{side}"] = _next_level(cand, c, d)
        out[f"pbB_inval_{side}"] = lvl_sw
        out[f"pbB_half_{side}"] = (base & trend).astype(float)
    return out


def _swept(d, h, l, a5, k0, k1, L, P):
    k = k1
    return (l[k] <= L - P["b_sweep_atr"] * a5[k]) if d == 1 else (h[k] >= L + P["b_sweep_atr"] * a5[k])


def _strategy_c(h, l, c, v, a5, cd, cvd, L, s15, trend, rangeg, trans, bull, bear, sess, near_open, P):
    """Strategy C (5.3). Long: 15m compression directly under a marked level (the level within 0.5 x ATR(15m) above
    the 8-candle box); a 5m strong breakout candle closes above it (>= 0.2 x ATR beyond, body >= 60%, volume spike) -
    no entry on that candle; within 12 x 5m candles price returns to the level zone and prints a bullish rejection
    candle (signal on that close); a 5m close back inside by more than 0.3 x ATR first cancels it. Regime: trend in
    the breakout's direction, or a range / transition when the breakout comes near a session open. With CVD
    (pbC_cvd_*): the retest's CVD stays above its low since the breakout."""
    n = len(c)
    out = {}
    comp = np.asarray(s15["comp"], dtype=float) == 1
    bh, bl, a15 = (np.asarray(s15[k], dtype=float) for k in ("box_h", "box_l", "a15"))
    zone = P["zone_atr"] * a15
    for d, side in ((1, "long"), (-1, "short")):
        edge = bh if d == 1 else bl
        lev = _next_level(L, edge - d * 1e-12, d)          # the nearest level at / beyond the box edge
        under = comp & np.isfinite(lev) & (d * (lev - edge) <= P["c_under_atr"] * a15)
        brk = (d * (c - lev) >= P["c_break_atr"] * a5) & (cd["body"] >= P["c_break_body"] * cd["rng"]) & \
              (v >= P["vol_spike"] * cd["vavg"])
        prev_under = np.r_[False, under[:-1]]
        start = brk & prev_under                            # the compression was there before the breakout candle
        reg_at = (trend & (bull if d == 1 else bear)) | ((rangeg | trans) & near_open)
        sig, sig_cvd = np.zeros(n, bool), np.zeros(n, bool)
        stop, tp2, inval = np.full(n, np.nan), np.full(n, np.nan), np.full(n, np.nan)
        rej = cd["bull_rej"] if d == 1 else cd["bear_rej"]
        for b in np.flatnonzero(start & reg_at):
            Lb, zb, height = lev[b], zone[b], (bh[b] - bl[b])
            for i in range(b + 1, min(b + int(P["c_retest_bars"]), n - 1) + 1):
                if d * (c[i] - (Lb - d * P["c_inval_atr"] * a5[i])) < 0:
                    break                                   # closed back inside: setup cancelled
                in_zone = (l[i] <= Lb + zb) if d == 1 else (h[i] >= Lb - zb)
                if in_zone and rej[i]:
                    sig[i] = True
                    seg = cvd[b:i + 1]
                    sig_cvd[i] = bool(np.isfinite(seg).all() and (d * (cvd[i] - (seg[:-1].min() if d == 1 else
                                                                                  seg[:-1].max())) > 0))
                    stop[i] = min(l[i], Lb - P["c_stop_atr"] * a5[i]) if d == 1 else max(h[i], Lb + P["c_stop_atr"] * a5[i])
                    mm, nx = Lb + d * height, _next_level(L[:, [i]], np.array([Lb]), d)[0]
                    cand = [x for x in (mm, nx) if np.isfinite(x) and d * (x - c[i]) > 0]
                    tp2[i] = (min(cand) if d == 1 else max(cand)) if cand else np.nan   # whichever comes first
                    inval[i] = Lb - d * P["c_inval_atr"] * a5[i]
                    break
        sess_ok = sess["london"] | sess["ny"]
        out[f"pbC_{side}"] = (sig & sess_ok).astype(float)
        out[f"pbC_cvd_{side}"] = (sig_cvd & sess_ok).astype(float)
        out[f"pbC_stop_{side}"], out[f"pbC_tp2_{side}"], out[f"pbC_inval_{side}"] = stop, tp2, inval
    return out


def coin_list(section, stats):
    """The playbook's coins (2.5): BTC, ETH and the short list, only those meeting the filters on the exchange the
    operator trades (24h volume >= min_volume_usdt, spread <= max_spread_pct), core first, then the most liquid,
    at most max_coins. stats = {coin: (24h volume in USDT, spread %)} of OKX USDT perpetuals; empty -> None (unknown:
    no coin filter rather than a guess)."""
    if not stats:
        return None
    sec = section or {}
    vmin, smax = float(sec.get("min_volume_usdt", 5e8)), float(sec.get("max_spread_pct", 0.02))

    def ok(c):
        v, sp = stats.get(c, (0.0, None))
        return v >= vmin and (sp is None or sp <= smax)
    core = [c for c in sec.get("coins_core", ["BTC", "ETH"]) if ok(c)]
    extra = sorted([c for c in sec.get("coins_extra", []) if ok(c)], key=lambda c: -stats[c][0])
    return (core + extra)[:int(sec.get("max_coins", 4))]


def max_isolated_leverage(entry, R, liq_x=2.0):
    """Section 6.1: on isolated margin the liquidation price must lie at least liq_x stop distances BEYOND the stop,
    i.e. entry / leverage >= (1 + liq_x) x R (maintenance margin ignored, so this is slightly generous)."""
    return int(np.floor(entry / ((1 + liq_x) * R))) if R > 0 else 0


COLUMNS = (["pb_trend", "pb_range", "pb_transition", "pb_bias_bull", "pb_bias_bear", "pb_vwap_crosses",
            "pb_sess_asia", "pb_sess_london", "pb_sess_ny", "pb_late", "pb_funding_ok_long", "pb_funding_ok_short",
            "pb_btc_ok_long", "pb_btc_ok_short", "pb_pdh", "pb_pdl", "pb_asia_h", "pb_asia_l", "pb_poc", "pb_vah",
            "pb_val", "pb_vwap"]
           + [f"pb{s}_{k}{side}" for s in "A" for k in ("", "cvd_", "entry_", "stop_", "tp2_", "inval_")
              for side in ("long", "short")]
           + [f"pb{s}_{k}{side}" for s in "BC" for k in ("", "cvd_", "stop_", "tp2_", "inval_")
              for side in ("long", "short")]
           + ["pbB_half_long", "pbB_half_short"])
