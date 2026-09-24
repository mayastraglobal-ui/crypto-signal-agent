"""
Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL (AGENT_PROMPT.md section 7:
"test candle claims with evidence").

For a candle pattern (e.g. bullish engulfing) we ask: if you had entered at the NEXT candle's open,
with a stop 1 ATR away, how often did price reach +1R, +2R, +3R (after costs) before the stop?
The same test on RANDOM candles (same coins, same long/short mix, same stop/targets/costs) is the
baseline: a pattern is only interesting if it clearly beats chance.

Pure functions only: no internet, no files.
"""
import zlib

import numpy as np

DEFAULTS = dict(
    stop_atr=1.0,          # stop distance = 1 x ATR (the ATR of the pattern candle)
    targets_r=[1, 2, 3],   # measured targets, in R, AFTER costs
    max_bars=30,           # give up (timeout) after 30 candles
    random_per_event=10,   # random baseline: 10 random entries per pattern entry
    min_events=30,         # fewer events than this -> "too few to judge"
)
PATTERNS = {                # feature column -> direction (1 = long, -1 = short)
    "displacement_up": 1, "displacement_down": -1,
    "bull_engulf": 1, "bear_engulf": -1,
    "bull_reject": 1, "bear_reject": -1,
}


def settings(cfg_section):
    out = dict(DEFAULTS)
    out.update(cfg_section or {})
    return out


def outcome(o, h, l, c, t, d, atr_t, costs, bar_hours, s):
    """Result of ONE hypothetical entry after the signal candle t (enter at open of t+1).
    Returns (best target reached before the stop: 0..3, stopped: bool, cost_in_R) or None
    when there is not enough future data (the last candles of the table are skipped).
    Stop first when stop and target are touched in the same candle (conservative)."""
    n = len(c)
    end = t + 1 + int(s["max_bars"])
    if end > n or not np.isfinite(atr_t) or atr_t <= 0:
        return None
    entry = o[t + 1] * (1 + costs["slip"] * d)
    R = s["stop_atr"] * atr_t
    stop = entry - d * R
    hs, ls = h[t + 1:end], l[t + 1:end]
    held = np.arange(1, len(hs) + 1)
    # cost to get in and out (fees + exit slippage + funding for shorts), in price, per candle held
    cost = entry * (costs["taker"] * 2 + costs["slip"] + costs["funding_8h"] * held * bar_hours / 8)
    stop_hit = (ls <= stop) if d == 1 else (hs >= stop)
    first_stop = int(np.argmax(stop_hit)) if stop_hit.any() else len(hs)
    best = 0
    for k, tr in enumerate(s["targets_r"], 1):
        level = entry + d * (tr * R + cost)
        hit = (hs >= level) if d == 1 else (ls <= level)
        first = int(np.argmax(hit)) if hit.any() else len(hs)
        if first < first_stop:              # strictly before: same candle counts as the stop
            best = k
    return best, first_stop < len(hs), float(cost[0] / R)


def study(frames, costs_by_dir, bar_hours, s=None, seed_key="", patterns=None):
    """Run every pattern + its random baseline over several candle tables of ONE timeframe.

    frames: list of (coin, candles_df, features_df) - features from engine.features.compute
    costs_by_dir: {1: cost dict, -1: cost dict} (taker, slip, funding_8h as fractions)
    patterns: {column: direction}; default PATTERNS (candle patterns)
    Returns {pattern: {...counts and shares...}}."""
    s = settings(s)
    out = {}
    for pat, d in (patterns or PATTERNS).items():
        res = dict(events=0, reached=[0] * len(s["targets_r"]), stopped=0, cost_r=[],
                   rnd_events=0, rnd_reached=[0] * len(s["targets_r"]), rnd_stopped=0)
        for coin, df, f in frames:
            o, h, l, c = (df[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close"))
            a = f["atr"].to_numpy()
            idx = np.flatnonzero(f[pat].to_numpy())
            got = 0
            for t in idx:
                r = outcome(o, h, l, c, t, d, a[t], costs_by_dir[d], bar_hours, s)
                if r is None:
                    continue
                got += 1
                _add(res, r, "")
                res["cost_r"].append(r[2])
            # random baseline: same coin, same direction, random candles with enough data after them
            valid = np.flatnonzero(np.isfinite(a) & (a > 0))
            valid = valid[valid + 1 + int(s["max_bars"]) <= len(c)]
            want = got * int(s["random_per_event"])
            if want and len(valid):
                rng = np.random.default_rng(zlib.crc32(f"{seed_key}|{coin}|{pat}".encode()))
                for t in rng.choice(valid, size=want, replace=want > len(valid)):
                    r = outcome(o, h, l, c, t, d, a[t], costs_by_dir[d], bar_hours, s)
                    if r is not None:
                        _add(res, r, "rnd_")
        out[pat] = summarize(res, s)
    return out


def _add(res, r, prefix):
    best, stopped, _ = r
    res[prefix + "events"] += 1
    for k in range(best):
        res[prefix + "reached"][k] += 1
    res[prefix + "stopped"] += int(stopped)


def summarize(res, s):
    """Shares, the random baseline, and a plain verdict: beats chance / worse / can't tell."""
    n, m = res["events"], res["rnd_events"]
    share = lambda x, k: x / k if k else None
    rows = dict(events=n, random_events=m,
                reached=[share(x, n) for x in res["reached"]],
                random_reached=[share(x, m) for x in res["rnd_reached"]],
                stopped=share(res["stopped"], n), random_stopped=share(res["rnd_stopped"], m),
                cost_r=float(np.median(res["cost_r"])) if res["cost_r"] else None)
    p, q = rows["reached"][0], rows["random_reached"][0]
    if n < s["min_events"] or p is None or q is None:
        rows["verdict"] = "too few to judge"
    else:
        se = np.sqrt(p * (1 - p) / n + q * (1 - q) / max(m, 1))   # normal wobble of the difference
        diff = p - q
        rows["verdict"] = ("beats chance" if diff > 2 * se else
                           "worse than chance" if diff < -2 * se else "can't tell from chance")
    return rows
