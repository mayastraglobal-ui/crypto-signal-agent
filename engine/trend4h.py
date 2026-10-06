"""
Roadmap step 5 part 1 (operator, 2026-10-06): "the proven trend, a faster entry".

The 4H Donchian breakout (donchian_breakout and its -VEXIT variant) is the one family with a measured edge (850+
trades, about +0.25R a trade, positive on unseen data and on 8 coins). This module turns it into a TREND WINDOW that
faster timeframes can read: trend4h_long = 1 while the 4H Donchian setup would be in a long trade, trend4h_short
the same for shorts, trend4h_age = 4H candles since its breakout candle. Cards on 1H / 30m / 15m / 5m then look for
their own (better-priced) entry inside that window.

The window's rules are FROZEN here (not read from the card), so a later change to the card can never silently
change cards that use the window:
  start  = the 4H card's entry rules on a closed 4H candle (htf_up, a close above the previous 20-candle high,
           volume > 1.5 x average, ADX(14) > 20; shorts mirrored) after its gate (trend gate, its regimes)
  end    = its exit rule (a close below the previous 10-candle low), its 2 x ATR stop from the breakout close
           touched, 60 candles, or a breakout the other way (which starts the opposite window)
Known at each 4H candle's CLOSE; the faster candles read the newest closed 4H candle (no look-ahead).
Pure: no internet, no files.
"""
import numpy as np

RULES = dict(
    long=["htf_up", "close > prev(highest(high,20))", "volume > vol_sma(20) * 1.5", "adx(14) > 20"],
    short=["htf_down", "close < prev(lowest(low,20))", "volume > vol_sma(20) * 1.5", "adx(14) > 20"],
    exit_long=["close < prev(lowest(low,10))"],
    exit_short=["close > prev(highest(high,10))"],
)
GATE = dict(gate="trend", regimes=["STRONG_BULL", "WEAK_BULL", "STRONG_BEAR", "WEAK_BEAR", "EXPANSION", "COMPRESSION"])
STOP_ATR, MAX_BARS, WARMUP = 2.0, 60, 250
COLUMNS = ["trend4h_long", "trend4h_short", "trend4h_age"]
TFS = ["1h", "30m", "15m", "5m"]          # the timeframes that can read the window (below 4H)


def window(h, l, c, atr, sig_l, sig_s, ex_l, ex_s, stop_atr=STOP_ATR, max_bars=MAX_BARS):
    """State at each 4H close: +1 long window, -1 short window, 0 none; and the age (candles since the breakout)."""
    n = len(c)
    state, age = np.zeros(n), np.full(n, np.nan)
    cur, start, stop = 0, -1, np.nan
    for j in range(n):
        if cur == 1 and (j - start >= max_bars or l[j] <= stop or ex_l[j]):
            cur = 0
        elif cur == -1 and (j - start >= max_bars or h[j] >= stop or ex_s[j]):
            cur = 0
        if np.isfinite(atr[j]) and atr[j] > 0:
            if sig_l[j]:
                cur, start, stop = 1, j, c[j] - stop_atr * atr[j]
            elif sig_s[j]:
                cur, start, stop = -1, j, c[j] + stop_atr * atr[j]
        state[j] = cur
        age[j] = j - start if cur else np.nan
    return state, age
