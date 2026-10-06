"""
Trade management helpers beyond the trade plan (step 3: the operator's playbook, section 7).

The trailing stop of the playbook: after TP1 the rest of the position trails "behind the most recent confirmed 5m
swing low (long) or below EMA9 on 5m closes, whichever is further". A swing low is a candle whose low is lower than
the lows of n candles on each side; it is CONFIRMED only n candles later (no look-ahead). The value at candle j
uses candles up to j only; the stop for candle j+1 uses the value at the close of candle j.
Pure functions, numpy in / numpy out: the backtest, the hourly paper record and the live watcher's follow-up all
use the same code.
"""
import numpy as np


def ema(x, n):
    x = np.asarray(x, dtype=float)
    out = np.full(len(x), np.nan)
    if len(x) < n:
        return out
    a = 2.0 / (n + 1)                              # = pandas ewm(span=n, adjust=False, min_periods=n)
    v = x[0]
    for i in range(len(x)):
        v = x[i] if i == 0 else a * x[i] + (1 - a) * v
        if i >= n - 1:
            out[i] = v
    return out


def confirmed_swings(h, l, n):
    """(last confirmed swing high, last confirmed swing low) known at each candle's close."""
    h, l = np.asarray(h, dtype=float), np.asarray(l, dtype=float)
    m = len(h)
    hi, lo = np.full(m, np.nan), np.full(m, np.nan)
    last_h = last_l = np.nan
    for j in range(m):
        i = j - n                                  # the candle that becomes confirmed at j
        if i - n >= 0:
            win_h, win_l = h[i - n:i + n + 1], l[i - n:i + n + 1]
            if h[i] == win_h.max() and (win_h == h[i]).sum() == 1:
                last_h = h[i]
            if l[i] == win_l.min() and (win_l == l[i]).sum() == 1:
                last_l = l[i]
        hi[j], lo[j] = last_h, last_l
    return hi, lo


def trail_levels(h, l, c, swing_n=3, ema_n=9):
    """(long trail, short trail) per candle close: the further of the last confirmed swing and the EMA."""
    sh, sl = confirmed_swings(h, l, swing_n)
    e = ema(c, ema_n)
    long_t = np.where(np.isfinite(sl) & np.isfinite(e), np.minimum(sl, e), np.where(np.isfinite(sl), sl, e))
    short_t = np.where(np.isfinite(sh) & np.isfinite(e), np.maximum(sh, e), np.where(np.isfinite(sh), sh, e))
    return long_t, short_t


def closes_of(close_time, tf_ms):
    """True for candles whose close is also the close of a `tf_ms` candle (e.g. the 5m candles closing a 15m one)."""
    return (np.asarray(close_time, dtype=np.int64) + 1) % int(tf_ms) == 0
