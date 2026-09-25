"""
Feature engine: candle shape, momentum, volume, price action, extra indicators
(AGENT_PROMPT.md section 7).

compute(df, tf_ms, settings) -> one row of features per candle.
Golden rule: the value at candle t uses ONLY candles 0..t (closed candles). A swing high/low
"exists" only once the N candles after it have closed - it is never drawn in afterwards.

Pure functions only: no internet, no files.
"""
import numpy as np
import pandas as pd

DEFAULTS = dict(
    atr_n=14,
    atr_median_n=100,           # ATR vs its 100-candle median
    rel_vol_n=20,               # relative volume = this candle / mean of the previous 20
    persistence_n=10,           # share of the last 10 closes that were up
    expansion_x=1.5,            # range >= 1.5 x ATR = range expansion
    contraction_x=0.5,          # range <= 0.5 x ATR = range contraction
    displacement_range_atr=1.5, # displacement: range >= 1.5 x ATR ...
    displacement_body_pct=0.6,  # ... body >= 60% of the range ...
    displacement_rel_vol=1.3,   # ... relative volume >= 1.3
    rejection_wick_body_x=2.0,  # pin bar: wick >= 2 x body ...
    rejection_wick_pct=0.6,     # ... and >= 60% of the range, close in the far third
    swing_n=3,                  # swing = highest/lowest point with 3 candles on each side
    level_touch_atr=0.25,       # swing points within 0.25 ATR of a level count as touches
    level_lookback_swings=30,   # levels come from the last 30 confirmed swings of each kind
    consolidation_n=20,         # consolidation: 20-candle range <= 3 x ATR
    consolidation_atr=3.0,
    breakout_n=20,              # breakout: close beyond the previous 20-candle high / low
    retest_bars=5,              # retest: back to the broken level within 5 candles, and holds
    retest_atr=0.25,
    failed_bars=3,              # failed breakout: closes back inside within 3 candles
    impulse_atr=2.5,            # impulse: move >= 2.5 x ATR within 5 candles
    impulse_bars=5,
    pullback_min=0.382,         # pullback: gives back 38.2% - 61.8% of the impulse leg
    pullback_max=0.618,
    rsi_n=14,
    stoch_rsi=[14, 14, 3, 3],   # RSI length, stochastic length, K smoothing, D smoothing
    roc_n=10,
    keltner=[20, 10, 2.0],      # EMA length, ATR length, multiplier
    ichimoku=[9, 26, 52],       # Phase 18 C: tenkan, kijun, senkou B lengths (the cloud is drawn kijun candles ahead)
)
FIB_LEVELS = (0.382, 0.5, 0.618, 0.786)

BOOL_FEATURES = ["expansion", "contraction", "displacement_up", "displacement_down", "bull_engulf",
                 "bear_engulf", "bull_reject", "bear_reject", "swing_high", "swing_low",
                 "consolidation", "breakout_up", "breakout_down", "retest_up", "retest_down",
                 "failed_breakout_up", "failed_breakout_down", "impulse_up", "impulse_down",
                 "pullback_up", "pullback_down", "bull_div", "bear_div"]


def settings(cfg_section):
    out = dict(DEFAULTS)
    out.update(cfg_section or {})
    return out


def _wilder(x, n):
    return x.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def atr(df, n=14):
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return _wilder(tr, n)


def rsi(c, n=14):
    d = c.diff()
    au, ad = _wilder(d.clip(lower=0), n), _wilder(-d.clip(upper=0), n)
    r = 100 - 100 / (1 + au / ad.replace(0, np.nan))
    return r.where(~((ad == 0) & au.notna()), 100.0)


def _run_length(cond):
    """How many candles in a row (ending at t) the condition has been true."""
    c = cond.astype(int).to_numpy()
    out = np.zeros(len(c), dtype=int)
    run = 0
    for i, x in enumerate(c):
        run = run + 1 if x else 0
        out[i] = run
    return out


def volume_profile(tp, v, n, bins=24, area=0.70, chunk=20000):
    """Rolling volume profile over the last n candles: (poc, vah, val) arrays; NaN for the first n-1 candles.
    Candle i's volume counts at its typical price tp[i]; bins span the window's lowest to highest typical price."""
    m = len(tp)
    poc, vah, val = (np.full(m, np.nan) for _ in range(3))
    if m < n or n < 2:
        return poc, vah, val
    from numpy.lib.stride_tricks import sliding_window_view
    P, V = sliding_window_view(tp, n), sliding_window_view(v, n)          # row j = candles j .. j+n-1
    for a in range(0, len(P), chunk):
        p, w = P[a:a + chunk], V[a:a + chunk]
        lo, hi = p.min(axis=1), p.max(axis=1)
        width = np.where(hi > lo, (hi - lo) / bins, np.nan)
        b = np.clip(np.floor((p - lo[:, None]) / width[:, None]), 0, bins - 1)
        b = np.nan_to_num(b, nan=0).astype(int)
        hist = np.zeros((len(p), bins))
        np.add.at(hist, (np.repeat(np.arange(len(p)), n), b.ravel()), w.ravel())
        top = hist.argmax(axis=1)
        order = np.argsort(-hist, axis=1, kind="stable")
        cum = np.cumsum(np.take_along_axis(hist, order, axis=1), axis=1)
        tot = cum[:, -1:]
        keep = np.arange(bins)[None, :] <= (cum < area * tot).sum(axis=1)[:, None]
        top_bin = np.where(keep, order, -10**9).max(axis=1)
        low_bin = np.where(keep, order, 10**9).min(axis=1)
        ok = np.isfinite(width) & (tot[:, 0] > 0)
        rows = slice(a + n - 1, a + n - 1 + len(p))
        poc[rows] = np.where(ok, lo + (top + 0.5) * width, np.where(hi == lo, lo, np.nan))
        vah[rows] = np.where(ok, lo + (top_bin + 1) * width, np.where(hi == lo, lo, np.nan))
        val[rows] = np.where(ok, lo + low_bin * width, np.where(hi == lo, lo, np.nan))
    return poc, vah, val


def _anchored_vwap(tp, v, anchor):
    """VWAP from the anchor candle (e.g. the last confirmed swing) to each candle; NaN before the first anchor.
    Summed per anchor window (not as a difference of running totals), so it does not depend on where history starts."""
    n = len(tp)
    out = np.full(n, np.nan)
    a = np.where(np.isfinite(anchor), anchor, -1).astype(int)
    starts = np.flatnonzero(np.r_[True, a[1:] != a[:-1]])
    ends = np.r_[starts[1:], n]
    for s0, e0 in zip(starts, ends):
        if a[s0] < 0:
            continue
        pv, vol = np.cumsum(tp[a[s0]:e0] * v[a[s0]:e0]), np.cumsum(v[a[s0]:e0])
        k0 = s0 - a[s0]
        with np.errstate(invalid="ignore", divide="ignore"):
            out[s0:e0] = pv[k0:] / np.where(vol[k0:] > 0, vol[k0:], np.nan)
    return out


def compute(df, tf_ms, s=None):
    """Features for every candle of one candle table (sorted, closed candles only)."""
    s = settings(s)
    df = df.reset_index(drop=True)
    o, h, l, c, v = (df[k].astype(float) for k in ("open", "high", "low", "close", "volume"))
    n = len(df)
    f = pd.DataFrame(index=df.index)

    # ---------- candle shape ----------
    rng = h - l
    safe = rng.replace(0, np.nan)
    body = (c - o).abs()
    f["body_pct"] = (body / safe).fillna(0.0)
    f["upper_wick_pct"] = ((h - np.maximum(o, c)) / safe).fillna(0.0)
    f["lower_wick_pct"] = ((np.minimum(o, c) - l) / safe).fillna(0.0)
    f["close_loc"] = ((c - l) / safe).fillna(0.5)

    # ---------- momentum ----------
    a = atr(df, s["atr_n"])
    a_prev = a.shift(1)                                   # ATR before this candle (not inflated by it)
    f["atr"] = a
    f["consec_up"] = _run_length(c > c.shift())
    f["consec_down"] = _run_length(c < c.shift())
    f["range_atr"] = rng / a_prev
    f["expansion"] = f["range_atr"] >= s["expansion_x"]
    f["contraction"] = f["range_atr"] <= s["contraction_x"]
    f["atr_ratio"] = a / a.rolling(s["atr_median_n"], min_periods=s["atr_median_n"]).median()
    f["momentum_persist"] = (c > c.shift()).astype(float).rolling(s["persistence_n"]).mean()

    # ---------- volume ----------
    f["rel_vol"] = v / v.shift(1).rolling(s["rel_vol_n"], min_periods=s["rel_vol_n"]).mean()
    f["vol_accel"] = v.rolling(3).mean() / v.shift(3).rolling(3).mean()

    # ---------- special candles ----------
    disp = (rng >= s["displacement_range_atr"] * a_prev) & (f["body_pct"] >= s["displacement_body_pct"]) \
        & (f["rel_vol"] >= s["displacement_rel_vol"])
    f["displacement_up"] = disp & (c > o)
    f["displacement_down"] = disp & (c < o)
    po, pc = o.shift(), c.shift()
    f["bull_engulf"] = (pc < po) & (c > o) & (o <= pc) & (c >= po) & (body > (pc - po).abs())
    f["bear_engulf"] = (pc > po) & (c < o) & (o >= pc) & (c <= po) & (body > (pc - po).abs())
    lw, uw = np.minimum(o, c) - l, h - np.maximum(o, c)
    f["bull_reject"] = (lw >= s["rejection_wick_body_x"] * body) & (f["lower_wick_pct"] >= s["rejection_wick_pct"]) \
        & (f["close_loc"] >= 2 / 3)
    f["bear_reject"] = (uw >= s["rejection_wick_body_x"] * body) & (f["upper_wick_pct"] >= s["rejection_wick_pct"]) \
        & (f["close_loc"] <= 1 / 3)

    # ---------- swings (confirmed N candles later) ----------
    k = int(s["swing_n"])
    left_hi = h.shift(1).rolling(k, min_periods=k).max()
    right_hi = h[::-1].shift(1).rolling(k, min_periods=k).max()[::-1]
    left_lo = l.shift(1).rolling(k, min_periods=k).min()
    right_lo = l[::-1].shift(1).rolling(k, min_periods=k).min()[::-1]
    pivot_hi = ((h > left_hi) & (h >= right_hi)).to_numpy()
    pivot_lo = ((l < left_lo) & (l <= right_lo)).to_numpy()
    # the pivot at candle p becomes KNOWN at candle p + k
    f["swing_high"] = pd.Series(np.r_[np.zeros(k, bool), pivot_hi[:n - k]] if n > k else np.zeros(n, bool))
    f["swing_low"] = pd.Series(np.r_[np.zeros(k, bool), pivot_lo[:n - k]] if n > k else np.zeros(n, bool))
    f["swing_high_price"] = h.shift(k).where(f["swing_high"])
    f["swing_low_price"] = l.shift(k).where(f["swing_low"])
    f["last_swing_high"] = f["swing_high_price"].ffill()
    f["last_swing_low"] = f["swing_low_price"].ffill()

    # ---------- structure (HH/HL/LH/LL) and RSI divergence at confirmed swings ----------
    r = rsi(c, s["rsi_n"]).to_numpy()
    hi_lab = np.full(n, None, dtype=object)
    lo_lab = np.full(n, None, dtype=object)
    bull_div = np.zeros(n, bool)
    bear_div = np.zeros(n, bool)
    prev_h = prev_l = None      # (price, rsi at the pivot)
    for t in np.flatnonzero(f["swing_high"].to_numpy()):
        p = t - k
        cur = (h.iloc[p], r[p])
        if prev_h is not None:
            hi_lab[t] = "HH" if cur[0] > prev_h[0] else "LH" if cur[0] < prev_h[0] else "EQH"
            if cur[0] > prev_h[0] and np.isfinite(cur[1]) and np.isfinite(prev_h[1]) and cur[1] < prev_h[1]:
                bear_div[t] = True
        prev_h = cur
    for t in np.flatnonzero(f["swing_low"].to_numpy()):
        p = t - k
        cur = (l.iloc[p], r[p])
        if prev_l is not None:
            lo_lab[t] = "HL" if cur[0] > prev_l[0] else "LL" if cur[0] < prev_l[0] else "EQL"
            if cur[0] < prev_l[0] and np.isfinite(cur[1]) and np.isfinite(prev_l[1]) and cur[1] > prev_l[1]:
                bull_div[t] = True
        prev_l = cur
    f["swing_high_label"] = pd.Series(hi_lab).ffill()
    f["swing_low_label"] = pd.Series(lo_lab).ffill()
    f["structure"] = np.where((f["swing_high_label"] == "HH") & (f["swing_low_label"] == "HL"), "up",
                              np.where((f["swing_high_label"] == "LH") & (f["swing_low_label"] == "LL"),
                                       "down", "mixed"))
    f.loc[f["swing_high_label"].isna() | f["swing_low_label"].isna(), "structure"] = None
    f["structure_up"] = f["structure"] == "up"
    f["structure_down"] = f["structure"] == "down"
    f["bull_div"] = bull_div
    f["bear_div"] = bear_div

    # ---------- nearest levels from confirmed swings ----------
    res, sup, res_t, sup_t = (np.full(n, np.nan) for _ in range(4))
    highs, lows = [], []
    sh, sl = f["swing_high_price"].to_numpy(), f["swing_low_price"].to_numpy()
    av, cv = a.to_numpy(), c.to_numpy()
    lb, touch = int(s["level_lookback_swings"]), s["level_touch_atr"]
    for t in range(n):
        if not np.isnan(sh[t]):
            highs = (highs + [sh[t]])[-lb:]
        if not np.isnan(sl[t]):
            lows = (lows + [sl[t]])[-lb:]
        if not np.isfinite(av[t]):
            continue
        pts = np.array(highs + lows)
        above = [x for x in highs if x > cv[t]]
        below = [x for x in lows if x < cv[t]]
        if above:
            res[t] = min(above)
            res_t[t] = int((np.abs(pts - res[t]) <= touch * av[t]).sum())
        if below:
            sup[t] = max(below)
            sup_t[t] = int((np.abs(pts - sup[t]) <= touch * av[t]).sum())
    f["resistance"] = res
    f["support"] = sup
    f["resistance_dist_atr"] = (f["resistance"] - c) / a
    f["support_dist_atr"] = (c - f["support"]) / a
    f["resistance_touches"] = res_t
    f["support_touches"] = sup_t

    # ---------- consolidation, breakout, retest, failed breakout ----------
    m = int(s["consolidation_n"])
    f["consolidation"] = (h.rolling(m).max() - l.rolling(m).min()) / a <= s["consolidation_atr"]
    b = int(s["breakout_n"])
    top, bot = h.shift(1).rolling(b, min_periods=b).max(), l.shift(1).rolling(b, min_periods=b).min()
    f["breakout_up"] = c > top
    f["breakout_down"] = c < bot
    ret_up, ret_dn, fail_up, fail_dn = (np.zeros(n, bool) for _ in range(4))
    lv, hv = l.to_numpy(), h.to_numpy()
    for t0 in np.flatnonzero(f["breakout_up"].to_numpy()):
        lvl = top.iloc[t0]
        for t in range(t0 + 1, min(n, t0 + 1 + int(s["retest_bars"]))):
            if lv[t] <= lvl + s["retest_atr"] * av[t] and cv[t] > lvl:
                ret_up[t] = True
                break
        for t in range(t0 + 1, min(n, t0 + 1 + int(s["failed_bars"]))):
            if cv[t] < lvl:
                fail_up[t] = True
                break
    for t0 in np.flatnonzero(f["breakout_down"].to_numpy()):
        lvl = bot.iloc[t0]
        for t in range(t0 + 1, min(n, t0 + 1 + int(s["retest_bars"]))):
            if hv[t] >= lvl - s["retest_atr"] * av[t] and cv[t] < lvl:
                ret_dn[t] = True
                break
        for t in range(t0 + 1, min(n, t0 + 1 + int(s["failed_bars"]))):
            if cv[t] > lvl:
                fail_dn[t] = True
                break
    f["retest_up"], f["retest_down"] = ret_up, ret_dn
    f["failed_breakout_up"], f["failed_breakout_down"] = fail_up, fail_dn

    # ---------- impulse and pullback ----------
    ib = int(s["impulse_bars"])
    a_before = a.shift(ib)
    f["impulse_up"] = (c - l.rolling(ib).min()) >= s["impulse_atr"] * a_before
    f["impulse_down"] = (h.rolling(ib).max() - c) >= s["impulse_atr"] * a_before
    pb_up, pb_dn = np.zeros(n, bool), np.zeros(n, bool)
    leg_up = leg_dn = None      # [start, extreme]
    lo_roll, hi_roll = l.rolling(ib).min().to_numpy(), h.rolling(ib).max().to_numpy()
    iu, idn = f["impulse_up"].to_numpy(), f["impulse_down"].to_numpy()
    for t in range(n):
        # up legs: consecutive impulse candles extend one leg; a new impulse after a pause starts a new one
        if iu[t]:
            if leg_up is not None and t > 0 and iu[t - 1]:
                leg_up = [min(leg_up[0], lo_roll[t]), max(leg_up[1], hv[t])]
            else:
                leg_up = [lo_roll[t], hv[t]]
        elif leg_up is not None:
            leg_up[1] = max(leg_up[1], hv[t])
            if lv[t] <= leg_up[0]:
                leg_up = None                                   # broke the start: no longer a pullback
            else:
                depth = (leg_up[1] - cv[t]) / (leg_up[1] - leg_up[0])
                pb_up[t] = s["pullback_min"] <= depth <= s["pullback_max"]
        # down legs: mirror image
        if idn[t]:
            if leg_dn is not None and t > 0 and idn[t - 1]:
                leg_dn = [max(leg_dn[0], hi_roll[t]), min(leg_dn[1], lv[t])]
            else:
                leg_dn = [hi_roll[t], lv[t]]
        elif leg_dn is not None:
            leg_dn[1] = min(leg_dn[1], lv[t])
            if hv[t] >= leg_dn[0]:
                leg_dn = None
            else:
                depth = (cv[t] - leg_dn[1]) / (leg_dn[0] - leg_dn[1])
                pb_dn[t] = s["pullback_min"] <= depth <= s["pullback_max"]
    f["pullback_up"], f["pullback_down"] = pb_up, pb_dn

    # ---------- extra indicators ----------
    rn, sn, kn, dn = s["stoch_rsi"]
    rr = rsi(c, rn)
    lo_r, hi_r = rr.rolling(sn).min(), rr.rolling(sn).max()
    stoch = ((rr - lo_r) / (hi_r - lo_r).replace(0, np.nan)) * 100
    f["stoch_rsi_k"] = stoch.rolling(kn).mean()
    f["stoch_rsi_d"] = f["stoch_rsi_k"].rolling(dn).mean()
    f["roc"] = (c / c.shift(s["roc_n"]) - 1) * 100
    en, an, mult = s["keltner"]
    mid = c.ewm(span=en, adjust=False, min_periods=en).mean()
    ka = atr(df, an)
    f["keltner_mid"], f["keltner_upper"], f["keltner_lower"] = mid, mid + mult * ka, mid - mult * ka
    f["obv"] = (np.sign(c.diff()).fillna(0) * v).cumsum()
    if tf_ms < 86_400_000:
        day = df["open_time"].astype("int64") // 86_400_000          # resets every UTC day
        tp = (h + l + c) / 3
        f["vwap"] = (tp * v).groupby(day).cumsum() / v.groupby(day).cumsum().replace(0, np.nan)
    else:
        f["vwap"] = np.nan                                            # not meaningful on 1D and above
    f["avwap_day"] = f["vwap"]                                        # Phase 18 C: VWAP anchored at the daily open

    # ---------- Phase 18 C: Fibonacci, VWAP anchored at the last swing, Ichimoku (all from closed candles) ----------
    pos = np.arange(n)
    hi_at = pd.Series(np.where(f["swing_high"].fillna(False).to_numpy(dtype=bool), pos - k, np.nan)).ffill().to_numpy()
    lo_at = pd.Series(np.where(f["swing_low"].fillna(False).to_numpy(dtype=bool), pos - k, np.nan)).ffill().to_numpy()
    H, L = f["last_swing_high"].to_numpy(dtype=float), f["last_swing_low"].to_numpy(dtype=float)
    known = np.isfinite(hi_at) & np.isfinite(lo_at)
    up_leg = known & (hi_at > lo_at)                  # the newest confirmed swing is a high: the last leg went UP
    f["fib_dir"] = np.where(known, np.where(up_leg, 1.0, -1.0), np.nan)
    for r in FIB_LEVELS:                              # retracement of the last leg (up: measured down from the high)
        f[f"fib_{int(round(r * 1000)):03d}"] = np.where(known, np.where(up_leg, H - r * (H - L), L + r * (H - L)), np.nan)
    tp_ = ((h + l + c) / 3).to_numpy(dtype=float)
    vv = v.to_numpy(dtype=float)
    for name, at in (("avwap_swing_high", hi_at), ("avwap_swing_low", lo_at)):
        f[name] = _anchored_vwap(tp_, vv, at)
    tn, kjn, sbn = s["ichimoku"]
    mid = lambda m: (h.rolling(m, min_periods=m).max() + l.rolling(m, min_periods=m).min()) / 2
    f["ichi_tenkan"], f["ichi_kijun"] = mid(tn), mid(kjn)
    f["ichi_span_a"] = ((f["ichi_tenkan"] + f["ichi_kijun"]) / 2).shift(kjn)   # computed kijun candles AGO
    f["ichi_span_b"] = mid(sbn).shift(kjn)
    f["ichi_cloud_top"] = np.fmax(f["ichi_span_a"], f["ichi_span_b"])
    f["ichi_cloud_bottom"] = np.fmin(f["ichi_span_a"], f["ichi_span_b"])
    # (the chikou span - the close drawn kijun candles BACK - is left out on purpose: in a backtest it is lookahead)

    for col in BOOL_FEATURES + ["structure_up", "structure_down"]:
        f[col] = f[col].fillna(False).astype(bool)
    return f
