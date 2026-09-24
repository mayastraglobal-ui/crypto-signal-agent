"""
Data quality checks (AGENT_PROMPT.md section 3).

Every candle table is checked before anything uses it. Each check gives one of three states:

  GOOD      -> signals allowed
  DEGRADED  -> analysis only (no signals from this coin / timeframe)
  UNSAFE    -> no signals; if it hits BTC or many coins, ALL signals stop (DATA_STALE / SIGNAL_DISABLED)

These functions are pure: no internet, no files. `now_ms` is always passed in, so the
same input gives the same verdict every time (and tests can travel in time).
"""
import numpy as np
import pandas as pd

GOOD, DEGRADED, UNSAFE = "GOOD", "DEGRADED", "UNSAFE"
_RANK = {GOOD: 0, DEGRADED: 1, UNSAFE: 2}

DEFAULTS = dict(
    stale_periods=2,            # last closed candle older than 2 candle-lengths -> UNSAFE
    max_missing_pct=1.0,        # more than 1% of candles missing -> UNSAFE
    recent_bars=300,            # any missing candle in the newest 300 -> DEGRADED
    volume_median_bars=50,      # "normal" volume = median of the 50 candles before
    volume_check_bars=3,        # check the newest 3 closed candles for volume spikes
    volume_spike_warn=10.0,     # 10x normal volume -> warning only (real breakouts do this)
    volume_spike_degraded=50.0, # 50x normal volume -> probably bad data -> DEGRADED
    cross_venue_max_pct=0.5,    # Binance vs OKX price differ by more than 0.5% -> DEGRADED
    system_unsafe_coin_share=0.30,  # more than 30% of coins UNSAFE -> whole system UNSAFE
)


def worst(*states):
    """The most serious of several states (GOOD < DEGRADED < UNSAFE)."""
    states = [s for s in states if s]
    return max(states, key=_RANK.get) if states else GOOD


def settings(cfg_section):
    out = dict(DEFAULTS)
    out.update(cfg_section or {})
    return out


def check_candles(df, tf_ms, now_ms, dq=None):
    """Check and clean one candle table.

    df     : columns open_time, open, high, low, close, volume (close_time optional), times in ms
    tf_ms  : candle length in ms
    now_ms : the current time in ms. Candles that have not closed by now are removed.

    Returns (clean_df, report). report = {state, problems, notes}.
      problems -> the reasons for DEGRADED / UNSAFE
      notes    -> things fixed or worth knowing that do not change the state
    """
    dq = settings(dq)
    problems, notes = [], []
    state = GOOD

    def flag(new_state, text):
        nonlocal state
        state = worst(state, new_state)
        problems.append(f"{new_state}: {text}")

    if df is None or len(df) == 0:
        flag(UNSAFE, "no candles received")
        return (df if df is not None else pd.DataFrame()), _report(state, problems, notes, 0)

    df = df.copy()
    df["open_time"] = df["open_time"].astype("int64")
    df["close_time"] = df["open_time"] + tf_ms - 1

    # --- order ---
    if not df["open_time"].is_monotonic_increasing:
        notes.append("candles arrived out of order - sorted")
        df = df.sort_values("open_time", kind="stable")

    # --- duplicates ---
    dup = df["open_time"].duplicated(keep=False)
    if dup.any():
        cols = ["open", "high", "low", "close", "volume"]
        conflicting = int((df[dup].groupby("open_time")[cols].nunique() > 1).any(axis=1).sum())
        n_extra = int(df["open_time"].duplicated().sum())
        if conflicting:
            flag(DEGRADED, f"{conflicting} duplicate candle time(s) with DIFFERENT prices")
        else:
            notes.append(f"{n_extra} exact duplicate candle(s) removed")
        df = df.drop_duplicates("open_time", keep="last")

    # --- only closed candles (also removes anything 'from the future') ---
    forming = df["close_time"] >= now_ms
    if forming.any():
        notes.append(f"{int(forming.sum())} unfinished candle(s) ignored (UNCONFIRMED)")
        df = df[~forming]
    df = df.reset_index(drop=True)
    if df.empty:
        flag(UNSAFE, "no closed candles")
        return df, _report(state, problems, notes, 0)

    # --- impossible prices / volumes ---
    px = df[["open", "high", "low", "close"]]
    bad_px = px.isna().any(axis=1) | (px <= 0).any(axis=1)
    if bad_px.any():
        flag(UNSAFE, f"{int(bad_px.sum())} candle(s) with zero, negative or missing price")
    hi_lo = df["high"] < df["low"]
    if hi_lo.any():
        flag(UNSAFE, f"{int(hi_lo.sum())} candle(s) with high below low")
    tol = 1e-9 * df["high"].abs()
    outside = ((df[["open", "close"]].max(axis=1) > df["high"] + tol) |
               (df[["open", "close"]].min(axis=1) < df["low"] - tol)) & ~hi_lo
    if outside.any():
        flag(UNSAFE, f"{int(outside.sum())} candle(s) with open/close outside the high-low range")
    bad_vol = df["volume"].isna() | (df["volume"] < 0)
    if bad_vol.any():
        flag(UNSAFE, f"{int(bad_vol.sum())} candle(s) with negative or missing volume")

    # --- missing candles (gaps) ---
    steps = df["open_time"].diff().iloc[1:]
    if (steps % tf_ms != 0).any():
        flag(UNSAFE, "candle times are not on the timeframe grid")
    missing_each = (steps // tf_ms - 1).clip(lower=0)
    missing = int(missing_each.sum())
    if missing:
        expected = len(df) + missing
        pct = missing / expected * 100
        recent_start = df["open_time"].iloc[max(0, len(df) - int(dq["recent_bars"]))]
        recent_missing = int(missing_each[df["open_time"].iloc[1:] > recent_start].sum())
        if pct > dq["max_missing_pct"]:
            flag(UNSAFE, f"{missing} missing candle(s) ({pct:.2f}% of history)")
        elif recent_missing:
            flag(DEGRADED, f"{recent_missing} missing candle(s) in the newest {int(dq['recent_bars'])}")
        else:
            notes.append(f"{missing} missing candle(s) in older history ({pct:.2f}%)")

    # --- stale feed ---
    age = now_ms - int(df["close_time"].iloc[-1])
    if age > dq["stale_periods"] * tf_ms:
        flag(UNSAFE, f"stale feed: newest closed candle is {age / tf_ms:.1f} candle-lengths old")

    # --- abnormal volume on the newest candles ---
    k, m = int(dq["volume_check_bars"]), int(dq["volume_median_bars"])
    vol = df["volume"].to_numpy(dtype=float)
    for i in range(max(m, len(vol) - k), len(vol)):
        base = np.nanmedian(vol[i - m:i])
        if not np.isfinite(base) or base <= 0:
            notes.append("normal volume is zero - volume spike check skipped")
            break
        ratio = vol[i] / base
        when = pd.to_datetime(df["open_time"].iloc[i], unit="ms").strftime("%m-%d %H:%M")
        if ratio >= dq["volume_spike_degraded"]:
            flag(DEGRADED, f"volume {ratio:.0f}x normal on candle {when} UTC (possible bad data)")
        elif ratio >= dq["volume_spike_warn"]:
            notes.append(f"volume spike {ratio:.0f}x normal on candle {when} UTC")

    return df, _report(state, problems, notes, len(df), last_close_ms=int(df["close_time"].iloc[-1]))


def _report(state, problems, notes, bars, last_close_ms=None):
    return dict(state=state, problems=problems, notes=notes, bars=bars, last_close_ms=last_close_ms)


def cross_venue(primary, secondary, max_pct=DEFAULTS["cross_venue_max_pct"]):
    """Compare last prices of the same coins on two exchanges.

    primary / secondary: {coin: price}. secondary None = second exchange unavailable.
    Returns {coin: {state, deviation_pct or None, note}}.
    """
    out = {}
    for coin, p in primary.items():
        q = (secondary or {}).get(coin)
        if secondary is None or q is None or not p or not q or p <= 0 or q <= 0:
            out[coin] = dict(state=GOOD, deviation_pct=None,
                             note="second exchange not available" if secondary is None
                             else "coin not listed on second exchange")
            continue
        dev = abs(p / q - 1) * 100
        bad = dev > max_pct
        out[coin] = dict(state=DEGRADED if bad else GOOD, deviation_pct=round(dev, 3),
                         note=f"price differs {dev:.2f}% between exchanges" if bad else "")
    return out


def system_state(coin_states, btc_coin="BTC", failed=(), share=DEFAULTS["system_unsafe_coin_share"]):
    """Decide the state of the whole system.

    coin_states: {coin: state} for coins that were checked.
    failed:      coins whose download failed completely (count as UNSAFE).
    Returns (state, reason).
    """
    states = dict(coin_states)
    for c in failed:
        states[c] = UNSAFE
    if not states:
        return UNSAFE, "no coin data at all"
    if states.get(btc_coin) == UNSAFE:
        return UNSAFE, "BTC data is UNSAFE (BTC drives the whole market)"
    if btc_coin not in states:
        return UNSAFE, "BTC data missing"
    n_bad = sum(s == UNSAFE for s in states.values())
    if n_bad / len(states) > share:
        return UNSAFE, f"{n_bad} of {len(states)} coins have UNSAFE data"
    not_good = sorted(c for c, s in states.items() if s != GOOD)
    if not_good:
        return DEGRADED, "some coins are analysis-only: " + ", ".join(not_good)
    return GOOD, "all checks passed"
