"""
Trading sessions as rule building blocks (the Forward Test Program, operator plan 2026-10-09).

Fixed UTC hours (no daylight-saving shift, so a backtest and the live watcher always agree):
  Asia    00:00 - 08:00 UTC  (08:00 - 16:00 Beijing)
  London  08:00 - 13:00 UTC  (16:00 - 21:00 Beijing)
  New York 13:00 - 21:00 UTC (21:00 - 05:00 Beijing)
A candle belongs to the session its OPEN time is in.

asia_high / asia_low = the highest high / lowest low of today's Asia candles (UTC day). They are known only once the
Asia session is over: on the candle that closes at 08:00 UTC and on every later candle of the same UTC day; before
that (and on a day with no Asia candle) they are unknown (NaN), so a rule using them is false. No look-ahead.

Pure functions only: no internet, no files.
"""
import numpy as np
import pandas as pd

HOUR_MS, DAY_MS = 3_600_000, 86_400_000
SESSIONS = {"asia": (0, 8), "london": (8, 13), "ny": (13, 21)}
COLUMNS = ["sess_asia", "sess_london", "sess_ny", "asia_high", "asia_low"]


def columns(open_time, high, low, tf_ms):
    """{column: numpy array} for candles with these open times (ms, UTC)."""
    ot = np.asarray(open_time, dtype=np.int64)
    hour = (ot % DAY_MS) // HOUR_MS
    out = {f"sess_{k}": ((hour >= a) & (hour < b)).astype(float) for k, (a, b) in SESSIONS.items()}
    day = ot // DAY_MS
    a_end = SESSIONS["asia"][1] * HOUR_MS
    in_asia = (ot % DAY_MS) < a_end
    df = pd.DataFrame({"day": day, "h": np.asarray(high, dtype=float), "l": np.asarray(low, dtype=float)})
    rng = df[in_asia].groupby("day").agg(h=("h", "max"), l=("l", "min"))
    known = (ot % DAY_MS) + int(tf_ms) >= a_end            # this candle closes at or after the end of Asia
    hi = pd.Series(day).map(rng["h"]).to_numpy(dtype=float)
    lo = pd.Series(day).map(rng["l"]).to_numpy(dtype=float)
    out["asia_high"] = np.where(known, hi, np.nan)
    out["asia_low"] = np.where(known, lo, np.nan)
    return out
