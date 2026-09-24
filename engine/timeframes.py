"""
Timeframes 1W -> 5m (AGENT_PROMPT.md sections 3 and 5).

Higher timeframes give PERMISSION, lower timeframes give TIMING. The golden rule here:
a candle may only use a higher-timeframe candle that had already CLOSED at that moment.
(A 4H candle on Wednesday sees LAST week's weekly candle, never the unfinished current one.)

Pure functions only: no internet, no files.
"""
import numpy as np
import pandas as pd

TF_MS = {"5m": 300_000, "15m": 900_000, "30m": 1_800_000, "1h": 3_600_000, "2h": 7_200_000,
         "4h": 14_400_000, "1d": 86_400_000, "7d": 7 * 86_400_000, "1w": 7 * 86_400_000}
CONTEXT_TFS = ["1w", "1d"]                            # downloaded for context, not traded (yet)
TRADE_ORDER = ["4h", "1h", "30m", "15m", "5m"]        # timeframes the current strategies run on
# Higher timeframe each CURRENT strategy looks at through htf_up / htf_down. Kept unchanged
# until the strategy spec v3 (Phase 7) switches strategies to the timeframe model below.
LEGACY_HTF = {"5m": "1h", "15m": "1h", "30m": "4h", "1h": "4h", "4h": "1d"}
# Pairs checked against each other: (lower, higher). The higher candle must equal its lower candles.
CONSISTENCY_PAIRS = [("5m", "15m"), ("15m", "30m"), ("30m", "1h"), ("1h", "4h"), ("4h", "1d"), ("1d", "1w")]

DEFAULT_MODELS = {
    "A": {"chain": ["7d", "1d", "4h", "1h", "15m", "5m"]},
    "B": {"chain": ["1d", "4h", "1h", "30m", "15m", "5m"], "veto": "1w"},
    "C": {"chain": ["7d", "1d", "1h", "30m", "15m", "5m"]},
    "D": {"chain": ["1d", "2h", "30m", "15m", "5m"]},
}


# ---------------------------------------------------------------------
# 1. Using higher-timeframe values safely
# ---------------------------------------------------------------------
def align_higher(lower, higher, columns):
    """For every LOWER candle, the given columns of the newest HIGHER candle that had closed
    by the time the lower candle closed (close_time <= lower close_time). Earlier than the first
    closed higher candle -> NaN. Returns a DataFrame with the lower frame's index.

    lower / higher need a close_time column (ms). No look-ahead is possible: a higher candle
    is matched only once its close_time has passed."""
    if higher is None or len(higher) == 0:
        return pd.DataFrame({c: np.nan for c in columns}, index=lower.index)
    right = higher[["close_time"] + list(columns)].copy()
    right["close_time"] = right["close_time"].astype("int64")
    right = right.sort_values("close_time")
    left = pd.DataFrame({"close_time": lower["close_time"].astype("int64").to_numpy(),
                         "_pos": np.arange(len(lower))}).sort_values("close_time")
    m = pd.merge_asof(left, right, on="close_time", direction="backward")
    m = m.sort_values("_pos")
    out = m[list(columns)]
    out.index = lower.index
    return out


# ---------------------------------------------------------------------
# 2. Rolling 7-day candles (a "week" that ends today)
# ---------------------------------------------------------------------
def rolling_7d(daily):
    """One candle per day covering that day and the 6 days before it. Built from CLOSED daily
    candles only. Days whose 7-day window has a missing day are dropped (never guessed)."""
    if daily is None or len(daily) < 7:
        return pd.DataFrame(columns=["open_time", "close_time", "open", "high", "low", "close", "volume"])
    d = daily.sort_values("open_time").reset_index(drop=True)
    out = pd.DataFrame({
        "open_time": d["open_time"].shift(6),
        "close_time": d["close_time"],
        "open": d["open"].shift(6),
        "high": d["high"].rolling(7).max(),
        "low": d["low"].rolling(7).min(),
        "close": d["close"],
        "volume": d["volume"].rolling(7).sum(),
    })
    if "quote_volume" in d:
        out["quote_volume"] = d["quote_volume"].rolling(7).sum()
    complete = (d["open_time"] - d["open_time"].shift(6)) == 6 * TF_MS["1d"]
    out = out[complete].dropna(subset=["open", "high", "low"])
    out["open_time"] = out["open_time"].astype("int64")
    return out.reset_index(drop=True)


# ---------------------------------------------------------------------
# 3. Do higher candles agree with the lower candles inside them?
# ---------------------------------------------------------------------
def consistency(lower, higher, lower_ms, higher_ms, last_n=50, price_tol_pct=0.01, volume_tol_pct=1.0):
    """Compare the newest `last_n` higher candles that are FULLY covered by lower candles:
    open = first lower open, close = last lower close, high = max lower high, low = min lower low,
    volume = sum of lower volumes (within tolerances). Incomplete groups (gaps, first candle of a
    new listing) are skipped, not counted as errors.

    Returns {checked, mismatches, examples}."""
    res = dict(checked=0, mismatches=0, examples=[])
    if lower is None or higher is None or len(lower) == 0 or len(higher) == 0:
        return res
    per = higher_ms // lower_ms
    lo = lower[["open_time", "open", "high", "low", "close", "volume"]].sort_values("open_time")
    hi = higher[["open_time", "open", "high", "low", "close", "volume"]].sort_values("open_time")
    hi = hi[hi["open_time"] >= lo["open_time"].iloc[0]].tail(int(last_n))
    if hi.empty:
        return res
    h_open = hi["open_time"].astype("int64").to_numpy()
    owner = pd.merge_asof(pd.DataFrame({"open_time": lo["open_time"].astype("int64").to_numpy()}),
                          pd.DataFrame({"open_time": h_open, "h_open": h_open}),
                          on="open_time", direction="backward")    # the higher candle each lower one starts in
    lo = lo.assign(h_open=owner["h_open"].to_numpy())
    lo = lo[lo["h_open"].notna() & (lo["open_time"] < lo["h_open"] + higher_ms)]
    g = lo.groupby("h_open").agg(n=("open", "size"), open=("open", "first"), high=("high", "max"),
                                 low=("low", "min"), close=("close", "last"), volume=("volume", "sum"))
    g = g[g["n"] == per]
    hi = hi.set_index(hi["open_time"].astype("int64"))
    for h_open, agg in g.iterrows():
        h = hi.loc[int(h_open)]
        res["checked"] += 1
        bad = [f for f in ("open", "high", "low", "close")
               if abs(h[f] - agg[f]) > abs(h[f]) * price_tol_pct / 100]
        if abs(h["volume"] - agg["volume"]) > max(abs(h["volume"]), 1e-12) * volume_tol_pct / 100:
            bad.append("volume")
        if bad:
            res["mismatches"] += 1
            if len(res["examples"]) < 3:
                when = pd.to_datetime(int(h_open), unit="ms").strftime("%Y-%m-%d %H:%M")
                res["examples"].append(f"{when} UTC: {', '.join(bad)}")
    return res


# ---------------------------------------------------------------------
# 4. The timeframe model (which timeframe does what)
# ---------------------------------------------------------------------
def model_roles(model):
    """Roles of a model: the last timeframe = execution (entry), the one before = trigger,
    the one before that = setup, everything above = bias (permission). veto = optional weekly veto."""
    chain = list(model["chain"])
    return dict(bias=chain[:-3], setup=chain[-3], trigger=chain[-2], execution=chain[-1],
                veto=model.get("veto"))


def missing_timeframes(model, available):
    """Timeframes a model needs that are not downloaded (e.g. 2H for Model D)."""
    need = list(model["chain"]) + ([model["veto"]] if model.get("veto") else [])
    return [tf for tf in need if tf not in available]


def describe(model):
    r = model_roles(model)
    parts = ([f"{r['veto'].upper()} veto"] if r["veto"] else []) + [tf.upper() for tf in r["bias"]] + \
            [f"{r['setup']} setup", f"{r['trigger']} trigger", f"{r['execution']} entry"]
    return " → ".join(parts)
