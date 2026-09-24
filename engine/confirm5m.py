"""
5-minute entry-confirmation protocol (AGENT_PROMPT.md section 8) - Phase 10.

After a closed 15m / 30m trigger of a strategy whose card says `confirm_5m: true`, the next closed
5-minute bars (at most 6) decide:
  CONFIRMED    a bar closes in the trade direction with a body >= 50% of its range, relative volume
               >= 1.0, price within entry +- 0.2R, and no opposing displacement since the trigger
  INVALIDATED  price touched the stop, or a 5m structure break (BOS / CHoCH) against the trade,
               before a confirmation - structure broken before entry
  EXPIRED      6 bars without a confirmation - no entry
  AWAITING     fewer than 6 closed bars so far (live only: the next run looks again)
Optional SMC signs on the way (5m sweep, displacement, engulfing bar) are recorded, never required.

Only CLOSED 5m bars that opened after the trigger candle closed are used, so the result can never
depend on the future. Pure functions: no internet, no files.
"""
import numpy as np

DEFAULTS = dict(
    bars=6,                  # scan up to 6 closed 5m bars
    min_body_pct=0.5,        # confirming bar: body >= 50% of its range
    min_rel_vol=1.0,         # ... and relative volume >= 1.0
    zone_r=0.2,              # ... and its close within the planned entry +- 0.2R
)
CONFIRMED, INVALIDATED, EXPIRED, AWAITING = "CONFIRMED", "INVALIDATED", "EXPIRED", "AWAITING"
# columns of the prepared 5m frame (features + SMC) that the protocol reads
NEEDS = ["body_pct", "rel_vol", "displacement_up", "displacement_down", "bull_engulf", "bear_engulf",
         "smc_bos_up", "smc_bos_down", "smc_choch_up", "smc_choch_down", "smc_sweep_bull", "smc_sweep_bear"]


def settings(section):
    s = dict(DEFAULTS)
    s.update(section or {})
    return s


def arrays(df, feats):
    """The numbers the protocol needs from a prepared 5m frame (df = candles, feats = features + SMC)."""
    out = {k: df[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close")}
    out["open_time"] = df["open_time"].to_numpy(dtype=np.int64)
    out["close_time"] = df["close_time"].to_numpy(dtype=np.int64)
    for k in NEEDS:
        x = feats[k].to_numpy() if k in feats else np.zeros(len(df))
        out[k] = np.nan_to_num(x.astype(float), nan=0.0)
    return out


def first_bar(m5, after_ms):
    """Index of the first 5m bar that OPENS at or after `after_ms` (= the trigger candle's close + 1 ms)."""
    return int(np.searchsorted(m5["open_time"], after_ms, side="left"))


def check(m5, after_ms, d, entry, stop, S=None):
    """Run the protocol for a trigger whose candle closed at after_ms - 1.
    m5: arrays(); d: +1 long / -1 short; entry, stop: the planned prices (R = |entry - stop|).
    Returns dict(state, idx (5m index of the deciding bar or None), bars (5m bars looked at), why, smc)."""
    S = settings(S)
    R = abs(entry - stop)
    j0, n = first_bar(m5, after_ms), len(m5["close"])
    smc, opposing = [], False
    up = d == 1
    for j in range(j0, min(j0 + int(S["bars"]), n)):
        o, h, l, c = m5["open"][j], m5["high"][j], m5["low"][j], m5["close"][j]
        seen = j - j0 + 1
        if (up and l <= stop) or (not up and h >= stop):
            return dict(state=INVALIDATED, idx=j, bars=seen, why="price reached the stop before entry", smc=smc)
        if m5["smc_bos_down" if up else "smc_bos_up"][j] or m5["smc_choch_down" if up else "smc_choch_up"][j]:
            return dict(state=INVALIDATED, idx=j, bars=seen, why="5m structure broke against the trade", smc=smc)
        if m5["smc_sweep_bull" if up else "smc_sweep_bear"][j]:
            smc.append("5m liquidity sweep")
        if m5["displacement_down" if up else "displacement_up"][j]:
            opposing = True
        ok = (d * (c - o) > 0 and m5["body_pct"][j] >= S["min_body_pct"] and m5["rel_vol"][j] >= S["min_rel_vol"]
              and abs(c - entry) <= S["zone_r"] * R and not opposing)
        if ok:
            if m5["displacement_up" if up else "displacement_down"][j]:
                smc.append("5m displacement")
            if m5["bull_engulf" if up else "bear_engulf"][j]:
                smc.append("5m engulfing bar")
            return dict(state=CONFIRMED, idx=j, bars=seen, why="5m bar confirmed", smc=sorted(set(smc)))
    seen = max(0, min(n, j0 + int(S["bars"])) - j0)
    if seen >= int(S["bars"]):
        return dict(state=EXPIRED, idx=None, bars=seen,
                    why=f"no 5m confirmation in {int(S['bars'])} bars" + (" (opposing displacement)" if opposing else ""),
                    smc=smc)
    return dict(state=AWAITING, idx=None, bars=seen, why=f"{seen}/{int(S['bars'])} 5m bars so far", smc=smc)


def exit_on_5m(trigger_close_time, trigger_exit, m5_close_time):
    """A trigger-timeframe exit rule mapped onto 5m bars: it fires on the 5m bar that closes together
    with the trigger candle whose exit rule was true (same moment as in the plain backtest)."""
    out = np.zeros(len(m5_close_time), bool)
    if trigger_exit is None:
        return None
    hits = np.asarray(trigger_close_time)[np.asarray(trigger_exit, bool)]
    idx = np.searchsorted(m5_close_time, hits)
    ok = (idx < len(m5_close_time))
    idx = idx[ok]
    ok2 = m5_close_time[idx] == hits[ok]
    out[idx[ok2]] = True
    return out
