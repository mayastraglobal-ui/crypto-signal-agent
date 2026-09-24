"""
Market regime engine (AGENT_PROMPT.md section 6).

For every closed candle of a timeframe it gives one label:
  STRONG_BULL · WEAK_BULL · RANGE · HIGH_VOL_RANGE · WEAK_BEAR · STRONG_BEAR ·
  EXPANSION · COMPRESSION · TRANSITION · UNCLEAR
plus, for the newest candle, an evidence record: confidence (strong / moderate / weak - never a %),
supporting evidence, contradicting evidence, and volatility / momentum / structure states.

The label at candle t uses only candles 0..t. Pure functions: no internet, no files.
"""
import numpy as np
import pandas as pd

from engine import features as fe
from engine import timeframes as tfm

LABELS = ["STRONG_BULL", "WEAK_BULL", "RANGE", "HIGH_VOL_RANGE", "WEAK_BEAR", "STRONG_BEAR",
          "EXPANSION", "COMPRESSION", "TRANSITION", "UNCLEAR"]
BULL, BEAR = {"STRONG_BULL", "WEAK_BULL"}, {"STRONG_BEAR", "WEAK_BEAR"}

DEFAULTS = dict(
    timeframes=["1w", "1d", "4h", "1h"],
    ema=[50, 200],               # EMA structure: close vs EMA50 vs EMA200 ...
    ema_by_tf={"1w": [10, 40]},  # ... except weekly: 10/40 weeks ~ the calendar span of 50/200 days
    slope_bars=10,               # EMA-fast slope over 10 candles ...
    slope_atr=1.0,               # ... more than 1 ATR up = bull vote, down = bear vote
    adx_n=14,
    adx_strong=25,               # ADX > 25 = strong trend
    adx_weak=20,                 # ADX < 20 = weak trend / ranging
    adx_borderline=2,            # ADX within 2 points of 20 or 25 = borderline (lowers confidence)
    bb_n=20, bb_k=2.0,           # Bollinger Bands (20, 2)
    bb_rank_n=100,               # Bollinger width compared with the last 100 candles (percentile)
    expansion_bb_pct=0.90,       # EXPANSION: width in its top 10% ...
    expansion_range_atr=1.5,     # ... and a candle range >= 1.5x the ATR before it (range expansion) ...
                                 # ... and a displacement / breakout, all within the last few candles
    compression_bb_pct=0.10,     # COMPRESSION: width in its bottom 10% ...
    compression_atr_x=0.8,       # ... and ATR <= 0.8x normal and ADX < 20
    high_vol_atr_x=1.3,          # a range with ATR >= 1.3x normal = HIGH_VOL_RANGE
    low_vol_atr_x=0.8,           # ATR <= 0.8x normal = low volatility
    recent_bars=3,               # "recently" = within the last 3 candles
    low_volume_x=0.7,            # 5-candle volume below 0.7x normal = weak participation
)


def settings(cfg_section):
    out = dict(DEFAULTS)
    out.update(cfg_section or {})
    return out


def _adx(df, n):
    h, l, c = df["high"], df["low"], df["close"]
    up, dn = h.diff(), -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=df.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=df.index)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    a = fe._wilder(tr, n)
    pdi, mdi = 100 * fe._wilder(pdm, n) / a, 100 * fe._wilder(mdm, n) / a
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan)
    return fe._wilder(dx, n)


def _pct_rank(x, n):
    """Share of the previous n values that are below the current value (0..1), NaN until n+1 values."""
    v = x.to_numpy(dtype=float)
    out = np.full(len(v), np.nan)
    for i in range(n, len(v)):
        w = v[i - n:i]
        if np.isfinite(v[i]) and np.isfinite(w).all():
            out[i] = (w < v[i]).mean()
    return pd.Series(out, index=x.index)


def compute(df, tf, feats=None, s=None):
    """Regime inputs and the label for every candle. feats = engine.features.compute(df) if you
    already have it (saves time). Returns a DataFrame (same index as df)."""
    s = settings(s)
    df = df.reset_index(drop=True)
    if feats is None:
        feats = fe.compute(df, tfm.TF_MS.get(tf, 0))
    feats = feats.reset_index(drop=True)
    c = df["close"].astype(float)
    fast_n, slow_n = s["ema_by_tf"].get(tf, s["ema"])
    ema_f = c.ewm(span=fast_n, adjust=False, min_periods=fast_n).mean()
    ema_s = c.ewm(span=slow_n, adjust=False, min_periods=slow_n).mean()
    atr = feats["atr"]
    r = pd.DataFrame(index=df.index)
    r["ema_fast"], r["ema_slow"] = ema_f, ema_s
    r["ema_vote"] = np.where((c > ema_f) & (ema_f > ema_s), 1, np.where((c < ema_f) & (ema_f < ema_s), -1, 0))
    r["slope_atr"] = (ema_f - ema_f.shift(s["slope_bars"])) / atr
    r["slope_vote"] = np.where(r["slope_atr"] > s["slope_atr"], 1, np.where(r["slope_atr"] < -s["slope_atr"], -1, 0))
    st = feats["structure"]
    r["structure"] = st
    r["structure_vote"] = np.where(st == "up", 1, np.where(st == "down", -1, 0))
    r["score"] = r["ema_vote"] + r["slope_vote"] + r["structure_vote"]
    r["adx"] = _adx(df, s["adx_n"])
    mid = c.rolling(s["bb_n"]).mean()
    sd = c.rolling(s["bb_n"]).std(ddof=0)
    r["bb_width"] = 2 * s["bb_k"] * sd / mid
    r["bb_pct"] = _pct_rank(r["bb_width"], int(s["bb_rank_n"]))
    r["atr_ratio"] = feats["atr_ratio"]
    r["rel_vol5"] = feats["rel_vol"].rolling(5).mean()
    k = int(s["recent_bars"])
    up_ev = (feats["displacement_up"] | feats["breakout_up"]).astype(int).rolling(k, min_periods=1).max() > 0
    dn_ev = (feats["displacement_down"] | feats["breakout_down"]).astype(int).rolling(k, min_periods=1).max() > 0
    r["recent_up_event"], r["recent_down_event"] = up_ev, dn_ev
    r["recent_range_exp"] = (feats["range_atr"] >= s["expansion_range_atr"]).astype(int) \
        .rolling(k, min_periods=1).max() > 0
    r["rsi"] = fe.rsi(c, 14)

    r["enough"] = ema_s.notna() & r["adx"].notna() & r["slope_atr"].notna()
    r["move"] = c - c.shift(k)
    r["label"], r["expansion_dir"] = classify(r, s)
    return r


def classify(r, s=None):
    """The label rules, checked in order (first match wins). r needs the columns: enough, score, adx,
    bb_pct, atr_ratio, recent_range_exp, recent_up_event, recent_down_event, move.
    Returns (labels, expansion directions)."""
    s = settings(s)
    adx, sc, ar, bp = r["adx"], r["score"], r["atr_ratio"], r["bb_pct"]
    up_ev, dn_ev = r["recent_up_event"].astype(bool), r["recent_down_event"].astype(bool)
    vol_ok = bp.notna() & ar.notna()
    mixed = sc.abs() <= 1
    conds = [~r["enough"].astype(bool),
             bp.notna() & (bp >= s["expansion_bb_pct"]) & r["recent_range_exp"].astype(bool) & (up_ev | dn_ev),
             vol_ok & (bp <= s["compression_bb_pct"]) & (ar <= s["compression_atr_x"]) & (adx < s["adx_weak"]),
             (sc == 3) & (adx >= s["adx_strong"]), (sc == -3) & (adx >= s["adx_strong"]),
             sc >= 2, sc <= -2,
             mixed & (adx < s["adx_weak"]) & vol_ok & (ar >= s["high_vol_atr_x"]),
             mixed & (adx < s["adx_weak"]),
             mixed & (adx >= s["adx_strong"])]
    choices = ["UNCLEAR", "EXPANSION", "COMPRESSION", "STRONG_BULL", "STRONG_BEAR", "WEAK_BULL", "WEAK_BEAR",
               "HIGH_VOL_RANGE", "RANGE", "TRANSITION"]
    labels = pd.Series(np.select(conds, choices, default="UNCLEAR"), index=r.index)   # mixed + ADX 20-25
    d = np.where(up_ev & ~dn_ev, "up", np.where(dn_ev & ~up_ev, "down", np.where(r["move"] >= 0, "up", "down")))
    exp_dir = pd.Series(d, index=r.index, dtype=object).where(labels == "EXPANSION", None)
    return labels, exp_dir


def direction(label, exp_dir=None):
    """+1 bullish, -1 bearish, 0 neither."""
    if label in BULL or (label == "EXPANSION" and exp_dir == "up"):
        return 1
    if label in BEAR or (label == "EXPANSION" and exp_dir == "down"):
        return -1
    return 0


def describe(r, i=-1, s=None):
    """Evidence record for one candle (default: the newest) of a compute() result."""
    s = settings(s)
    row = r.iloc[i]
    label = row["label"]
    exp_dir = row["expansion_dir"] if isinstance(row["expansion_dir"], str) else None
    d = direction(label, exp_dir)
    ranging = label in ("RANGE", "HIGH_VOL_RANGE", "COMPRESSION")
    sup, con = [], []
    num = lambda x: None if x is None or (isinstance(x, float) and not np.isfinite(x)) else float(x)

    if pd.isna(row["ema_slow"]) or pd.isna(row["adx"]):
        return dict(label="UNCLEAR", expansion_dir=None, confidence="weak",
                    supporting=[], contradicting=["not enough history on this timeframe"],
                    states=dict(volatility="unknown", momentum="unknown", structure="unknown"),
                    values={})

    def vote(v, bull_text, bear_text, flat_text):
        text = bull_text if v == 1 else bear_text if v == -1 else flat_text
        if d != 0:
            (sup if v == d else con).append(text if v != 0 else text + " (neutral)")
        elif ranging:
            (con if v != 0 else sup).append(text)
        else:
            sup.append(text) if label == "TRANSITION" and v != 0 else con.append(text)

    vote(row["ema_vote"], "close above EMA-fast above EMA-slow", "close below EMA-fast below EMA-slow",
         "EMAs not lined up")
    vote(row["slope_vote"], f"EMA-fast rising ({row['slope_atr']:+.1f} ATR in {s['slope_bars']} candles)",
         f"EMA-fast falling ({row['slope_atr']:+.1f} ATR in {s['slope_bars']} candles)",
         f"EMA-fast flat ({row['slope_atr']:+.1f} ATR in {s['slope_bars']} candles)")
    st = row["structure"] if isinstance(row["structure"], str) else None
    vote(row["structure_vote"], "swing structure up (HH/HL)", "swing structure down (LH/LL)",
         f"swing structure {st or 'not formed yet'}")

    adx = row["adx"]
    adx_text = f"ADX {adx:.0f}"
    if adx >= s["adx_strong"]:
        (con if ranging else sup).append(adx_text + " = strong trend")
    elif adx < s["adx_weak"]:
        (sup if ranging or label == "UNCLEAR" else con).append(adx_text + " = weak trend / ranging")
    else:
        con.append(adx_text + " = in between (20-25)")
    if min(abs(adx - s["adx_weak"]), abs(adx - s["adx_strong"])) <= s["adx_borderline"]:
        con.append(f"ADX {adx:.0f} is close to a threshold")

    ar, bp = row["atr_ratio"], row["bb_pct"]
    if pd.notna(ar) and pd.notna(bp):
        vt = f"candle size {ar:.2f}x normal, Bollinger width above {bp * 100:.0f}% of the last {s['bb_rank_n']} candles"
        if ar >= s["high_vol_atr_x"] and d != 0 and label != "EXPANSION":
            con.append(vt + " (unusually wild for a trend)")
        else:
            sup.append(vt)
        vol_state = "high" if ar >= s["high_vol_atr_x"] else "low" if ar <= s["low_vol_atr_x"] else "normal"
    else:
        con.append("volatility history too short to compare")
        vol_state = "unknown"
    rv = row["rel_vol5"]
    if pd.notna(rv) and d != 0:
        if rv < s["low_volume_x"]:
            con.append(f"volume only {rv:.2f}x normal (weak participation)")
        else:
            sup.append(f"volume {rv:.2f}x normal")
    if label == "EXPANSION":
        sup.append(f"range expansion + displacement / breakout {exp_dir} in the last {s['recent_bars']} candles")
    if label == "UNCLEAR":
        con.append("signals are mixed and trend strength is in between")

    n_con = len(con)
    confidence = "weak" if label == "UNCLEAR" or n_con >= 2 else "moderate" if n_con == 1 else "strong"
    rsi = row["rsi"]
    momentum = "unknown" if pd.isna(rsi) else "up" if rsi > 55 else "down" if rsi < 45 else "neutral"
    return dict(label=label, expansion_dir=exp_dir, confidence=confidence, supporting=sup,
                contradicting=con,
                states=dict(volatility=vol_state, momentum=momentum, structure=st or "not formed yet"),
                values=dict(adx=num(adx), atr_ratio=num(ar), bb_pct=num(bp), slope_atr=num(row["slope_atr"]),
                            rsi=num(rsi), rel_vol5=num(rv), score=int(row["score"])))


def permission(regimes):
    """Timeframe agreement (AGENT_PROMPT.md section 5): LONG needs at least 2 of 1D/4H/1H bullish and
    no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. Otherwise NO TRADE.
    regimes: {tf: {"label":..., "expansion_dir":...}}. Returns (verdict, reason)."""
    dirs = {tf: direction(regimes[tf]["label"], regimes[tf].get("expansion_dir")) if tf in regimes else 0
            for tf in ("1d", "4h", "1h")}
    weekly = regimes.get("1w", {}).get("label")
    bulls = [tf for tf, x in dirs.items() if x == 1]
    bears = [tf for tf, x in dirs.items() if x == -1]
    show = ", ".join(f"{tf.upper()} {regimes.get(tf, {}).get('label', 'n/a')}" for tf in ("1d", "4h", "1h"))
    if len(bulls) >= 2:
        if weekly == "STRONG_BEAR":
            return "NO TRADE", f"weekly veto: 1W STRONG_BEAR against {'/'.join(t.upper() for t in bulls)} bullish"
        return "LONG allowed", f"{'/'.join(t.upper() for t in bulls)} bullish" + \
            (f", 1W {weekly}" if weekly else "")
    if len(bears) >= 2:
        if weekly == "STRONG_BULL":
            return "NO TRADE", f"weekly veto: 1W STRONG_BULL against {'/'.join(t.upper() for t in bears)} bearish"
        return "SHORT allowed", f"{'/'.join(t.upper() for t in bears)} bearish" + \
            (f", 1W {weekly}" if weekly else "")
    return "NO TRADE", f"timeframes disagree ({show})"
