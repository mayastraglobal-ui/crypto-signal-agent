"""
Futures market-structure data (Phase 17 C, item 10): funding rate, open interest, long/short account ratio and
taker buy/sell volume ratio - free public data, no API key.

  * derivs.py (hourly, in the scan workflow) fetches it and APPENDS it to two history files that travel on the
    live-reports branch: reports/derivs_hourly.csv.gz (one row per coin and hour) and reports/funding.csv.gz (one row
    per coin and funding settlement). Exchanges keep only ~30 days of hourly open interest, so the history is saved
    from now on; data.binance.vision daily / monthly files back-fill older days a few at a time.
  * ONE SERIES PER SOURCE (never mixed): open interest and long/short levels differ between exchanges, so rows of
    different sources are never merged into one line. OKX (MAIN_SOURCE - reachable from the servers that run us) is
    the main series: every building block reads ONLY it, in backtests and live alike. Binance (its API when reachable,
    and the data.binance.vision files) is kept as a separate series for research only.
  * No value or change is ever computed across two sources: align() returns each candle's source code, and the
    building blocks that compare two moments (oi_chg, funding_z) return "unknown" when the source differs.
  * quality(): per coin - how old the newest main-series row is, gaps, impossible values; a main series that contains
    more than one source is DEGRADED (never GOOD).
  * align(): the values as they were KNOWN at each candle's close (no look-ahead): an hourly row counts from the END of
    its hour; a funding rate from its settlement time; too-old values (max age) become "unknown" (NaN), so rules that
    use them stay false and no live signal is built on stale data.

Pure functions; the fetching is in derivs.py.
"""
import csv
import io
import math
import zlib

import numpy as np
import pandas as pd

HOUR_MS = 3_600_000
HOURLY_COLS = ["ts", "coin", "source", "oi_usd", "ls_ratio", "taker_ratio"]     # ts = start of the hour (ms, UTC)
FUNDING_COLS = ["time", "coin", "source", "rate"]                                # rate = fraction per settlement
MAIN_SOURCE = "okx"                               # the only series the building blocks use (backtest AND live)
RESEARCH_SOURCES = ("binance", "binance_files")   # kept separately, research only
SOURCE_CODE = {"okx": 1, "binance": 2, "binance_files": 3, "synthetic": 4}
MAX_AGE_H = {"hourly": 3, "funding": 9}        # older than this = unknown (hourly stats / funding settlements)
LIMITS = dict(ls_ratio=(0.01, 100.0), taker_ratio=(0.01, 100.0), rate=(-0.03, 0.03))   # beyond = impossible / outlier


def _f(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return math.nan
    return v if math.isfinite(v) else math.nan


def hour_of(ms):
    return int(ms) // HOUR_MS * HOUR_MS


# ---------------- parsers (Binance API, OKX API, data.binance.vision files) ----------------
def binance_hourly(coin, oi, ls, taker):
    """/futures/data/openInterestHist, /globalLongShortAccountRatio, /takerlongshortRatio (period=1h) -> rows."""
    rows = {}
    for x in oi or []:
        rows.setdefault(hour_of(x["timestamp"]), {})["oi_usd"] = _f(x.get("sumOpenInterestValue"))
    for x in ls or []:
        rows.setdefault(hour_of(x["timestamp"]), {})["ls_ratio"] = _f(x.get("longShortRatio"))
    for x in taker or []:
        rows.setdefault(hour_of(x["timestamp"]), {})["taker_ratio"] = _f(x.get("buySellRatio"))
    return [dict(ts=t, coin=coin, source="binance", **{k: v.get(k, math.nan) for k in ("oi_usd", "ls_ratio",
                                                                                   "taker_ratio")})
            for t, v in sorted(rows.items())]


def binance_funding(coin, data):
    """/fapi/v1/fundingRate -> [dict(time, coin, source, rate)]."""
    return [dict(time=int(x["fundingTime"]), coin=coin, source="binance", rate=_f(x["fundingRate"]))
            for x in data or []]


def okx_hourly(coin, oi, ls, taker):
    """OKX rubik: open-interest-volume [[ts, oi_usd, vol]], long-short-account-ratio [[ts, ratio]],
    taker-volume [[ts, sell, buy]] (period 1H) -> rows."""
    rows = {}
    for x in (oi or {}).get("data") or []:
        rows.setdefault(hour_of(x[0]), {})["oi_usd"] = _f(x[1])
    for x in (ls or {}).get("data") or []:
        rows.setdefault(hour_of(x[0]), {})["ls_ratio"] = _f(x[1])
    for x in (taker or {}).get("data") or []:
        sell, buy = _f(x[1]), _f(x[2])
        rows.setdefault(hour_of(x[0]), {})["taker_ratio"] = buy / sell if sell and sell > 0 else math.nan
    return [dict(ts=t, coin=coin, source="okx", **{k: v.get(k, math.nan) for k in ("oi_usd", "ls_ratio",
                                                                               "taker_ratio")})
            for t, v in sorted(rows.items())]


def okx_funding(coin, data):
    """OKX /public/funding-rate-history -> rows (realizedRate when given, else fundingRate)."""
    return [dict(time=int(x["fundingTime"]), coin=coin, source="okx",
                 rate=_f(x.get("realizedRate") or x.get("fundingRate"))) for x in (data or {}).get("data") or []]


def _csv_rows(text):
    rd = csv.reader(io.StringIO(text))
    rows = [r for r in rd if r]
    if rows and not rows[0][0][:1].isdigit():                     # header present
        head, rows = [h.strip() for h in rows[0]], rows[1:]
    else:
        head = None
    return head, rows


def vision_metrics(coin, text):
    """data.binance.vision .../daily/metrics/<SYM>-metrics-<day>.csv (5-minute snapshots) -> hourly rows (the last
    snapshot of each hour). Columns: create_time, symbol, sum_open_interest, sum_open_interest_value,
    count_toptrader_long_short_ratio, sum_toptrader_long_short_ratio, count_long_short_ratio,
    sum_taker_long_short_vol_ratio."""
    head, rows = _csv_rows(text)
    head = head or ["create_time", "symbol", "sum_open_interest", "sum_open_interest_value",
                    "count_toptrader_long_short_ratio", "sum_toptrader_long_short_ratio", "count_long_short_ratio",
                    "sum_taker_long_short_vol_ratio"]
    ix = {h: i for i, h in enumerate(head)}
    by_hour = {}
    for r in rows:
        t = pd.Timestamp(r[ix["create_time"]], tz="UTC")
        ms = int(t.value // 1_000_000)
        by_hour[hour_of(ms)] = (ms, r)                             # rows are in time order: the last one wins
    out = []
    for h, (_, r) in sorted(by_hour.items()):
        out.append(dict(ts=h, coin=coin, source="binance_files", oi_usd=_f(r[ix["sum_open_interest_value"]]),
                        ls_ratio=_f(r[ix["count_long_short_ratio"]]),
                        taker_ratio=_f(r[ix["sum_taker_long_short_vol_ratio"]])))
    return out


def vision_funding(coin, text):
    """data.binance.vision .../monthly/fundingRate/<SYM>-fundingRate-<YYYY-MM>.csv: calc_time, funding_interval_hours,
    last_funding_rate -> rows."""
    head, rows = _csv_rows(text)
    head = head or ["calc_time", "funding_interval_hours", "last_funding_rate"]
    ix = {h: i for i, h in enumerate(head)}
    return [dict(time=int(float(r[ix["calc_time"]])), coin=coin, source="binance_files",
                 rate=_f(r[ix["last_funding_rate"]])) for r in rows]


# ---------------- history files ----------------
def merge(old, new, key):
    """Append new rows to the history: one row per (coin, SOURCE, key) - every source keeps its own series (the row
    seen first is kept for the same time). Never drops history."""
    cols = HOURLY_COLS if key == "ts" else FUNDING_COLS
    frames = [f for f in (old, pd.DataFrame(new, columns=cols)) if f is not None and len(f)]
    if not frames:
        return pd.DataFrame(columns=cols)
    df = pd.concat(frames, ignore_index=True).drop_duplicates(["coin", "source", key], keep="first")
    return df.sort_values(["coin", "source", key]).reset_index(drop=True)[cols]


def series(df, source=MAIN_SOURCE):
    """The rows of one source (None = all rows - only for checks and tests)."""
    return df if source is None or not len(df) else df[df["source"] == source]


def read(path, cols):
    try:
        df = pd.read_csv(path)
    except (OSError, ValueError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=cols)
    return df[cols] if set(cols) <= set(df.columns) else pd.DataFrame(columns=cols)


# ---------------- data quality ----------------
def quality(hourly, funding, coins, now_ms, main=MAIN_SOURCE):
    """Per coin, on the MAIN series (the one the building blocks read): state GOOD / DEGRADED / STALE / MISSING, age
    of the newest row and funding rate, gaps in the last 7 days, impossible values. DEGRADED = the main series holds
    more than one source (levels not comparable). The research series (Binance) is only counted.
    STALE / MISSING -> the building blocks read 'unknown' for new candles."""
    out = {}
    for c in coins:
        allh = hourly[hourly["coin"] == c] if len(hourly) else hourly
        allf = funding[funding["coin"] == c] if len(funding) else funding
        h, f = series(allh, main), series(allf, main)
        research = {s: int((allh["source"] == s).sum()) for s in sorted(set(allh["source"]) - {main})} if len(allh) else {}
        if not len(h):
            out[c] = dict(state="MISSING", problems=[f"no {main} (main series) data yet"], hours=0,
                          research_rows=research)
            continue
        last = int(h["ts"].max())
        age_h = (now_ms - (last + HOUR_MS)) / HOUR_MS
        week = h[h["ts"] >= now_ms - 7 * 24 * HOUR_MS]
        expected = 7 * 24 if int(h["ts"].min()) <= now_ms - 7 * 24 * HOUR_MS else len(week)
        gaps = max(0, expected - len(week))
        bad = 0
        for col in ("ls_ratio", "taker_ratio"):
            lo, hi = LIMITS[col]
            v = h[col].astype(float)
            bad += int(((v < lo) | (v > hi)).sum())
        lo, hi = LIMITS["rate"]
        bad_f = int(((f["rate"].astype(float) < lo) | (f["rate"].astype(float) > hi)).sum()) if len(f) else 0
        probs = []
        if age_h > MAX_AGE_H["hourly"]:
            probs.append(f"newest hourly row is {age_h:.1f} h old")
        if gaps:
            probs.append(f"{gaps} missing hours in the last 7 days")
        if bad or bad_f:
            probs.append(f"{bad + bad_f} impossible / outlier values (ignored)")
        mixed = h["source"].nunique() > 1 or (len(f) and f["source"].nunique() > 1)
        if mixed:
            probs.append("mixed sources in the main series: " + ", ".join(sorted(set(h["source"]) | set(f["source"])))
                         + " - levels are not comparable (DEGRADED)")
        f_age = (now_ms - int(f["time"].max())) / HOUR_MS if len(f) else None
        if f_age is None or f_age > MAX_AGE_H["funding"]:
            probs.append("funding rate missing or older than 9 h")
        state = "STALE" if age_h > MAX_AGE_H["hourly"] else "DEGRADED" if mixed else "GOOD"
        out[c] = dict(state=state, main_source=main, research_rows=research, age_h=round(age_h, 1),
                      hours=int(len(h)), first_utc=pd.to_datetime(int(h["ts"].min()), unit="ms").strftime("%Y-%m-%d"),
                      gaps_7d=int(gaps), invalid=int(bad + bad_f), sources=sorted(h["source"].unique().tolist()),
                      funding_rows=int(len(f)), funding_age_h=None if f_age is None else round(f_age, 1),
                      last=dict(oi_usd=_f(h.iloc[-1]["oi_usd"]), ls_ratio=_f(h.iloc[-1]["ls_ratio"]),
                                taker_ratio=_f(h.iloc[-1]["taker_ratio"]),
                                funding_pct=_f(f.iloc[-1]["rate"]) * 100 if len(f) else None),
                      problems=probs)
    return out


def clean(hourly, funding):
    """Impossible values -> NaN (never used), so one bad print cannot fire a rule."""
    h, f = hourly.copy(), funding.copy()
    for col in ("ls_ratio", "taker_ratio"):
        lo, hi = LIMITS[col]
        v = h[col].astype(float)
        h[col] = v.where((v >= lo) & (v <= hi))
    lo, hi = LIMITS["rate"]
    if len(f):
        v = f["rate"].astype(float)
        f["rate"] = v.where((v >= lo) & (v <= hi))
    return h, f


# ---------------- alignment to candles (no look-ahead) ----------------
def _asof(times, known_at, values, max_age_ms):
    """values[i] known from known_at[i] (sorted); for each time the newest value known by then, if not too old."""
    out = np.full(len(times), np.nan)
    if not len(known_at):
        return out
    idx = np.searchsorted(known_at, times, side="right") - 1
    ok = idx >= 0
    out[ok] = values[idx[ok]]
    age = np.where(ok, times - known_at[np.clip(idx, 0, None)], np.inf)
    out[age > max_age_ms] = np.nan
    return out


def align(close_time, open_time, coin_hourly, coin_funding, source=MAIN_SOURCE):
    """Columns for one coin's candles, each value as KNOWN at the candle close, from ONE source (the main series):
    funding_rate (% per settlement), oi (USD), ls_ratio, taker_ratio, and _hsrc / _fsrc (the source code of the row each
    candle used; 0 = unknown) so no change is ever computed across two sources.
    _fund_short (backtest COSTS, not a building block): the fraction per 8 hours a SHORT pays at each candle's OPEN -
    the HIGHEST of every source's -rate (never lower than any exchange's real cost; 0 when funding was positive)."""
    close_time, open_time = np.asarray(close_time, dtype=np.int64), np.asarray(open_time, dtype=np.int64)
    out = {}
    all_f = coin_funding
    coin_hourly, coin_funding = series(coin_hourly, source), series(coin_funding, source)
    h = coin_hourly.sort_values("ts") if len(coin_hourly) else coin_hourly
    known = (h["ts"].to_numpy(dtype=np.int64) + HOUR_MS) if len(h) else np.array([], dtype=np.int64)
    for col, name in (("oi_usd", "oi"), ("ls_ratio", "ls_ratio"), ("taker_ratio", "taker_ratio")):
        vals = h[col].to_numpy(dtype=float) if len(h) else np.array([])
        out[name] = _asof(close_time, known, vals, MAX_AGE_H["hourly"] * HOUR_MS)
    codes = h["source"].map(SOURCE_CODE).fillna(9).to_numpy(dtype=float) if len(h) else np.array([])
    out["_hsrc"] = np.nan_to_num(_asof(close_time, known, codes, MAX_AGE_H["hourly"] * HOUR_MS), nan=0.0)
    f = coin_funding.dropna(subset=["rate"]).sort_values("time") if len(coin_funding) else coin_funding
    ft = f["time"].to_numpy(dtype=np.int64) if len(f) else np.array([], dtype=np.int64)
    fr = f["rate"].to_numpy(dtype=float) if len(f) else np.array([])
    out["funding_rate"] = _asof(close_time, ft, fr, MAX_AGE_H["funding"] * HOUR_MS) * 100
    fcodes = f["source"].map(SOURCE_CODE).fillna(9).to_numpy(dtype=float) if len(f) else np.array([])
    out["_fsrc"] = np.nan_to_num(_asof(close_time, ft, fcodes, MAX_AGE_H["funding"] * HOUR_MS), nan=0.0)
    pay = np.zeros(len(open_time))                   # costs: the most any exchange's shorts paid (never less)
    for _, g in (all_f.dropna(subset=["rate"]).groupby("source") if len(all_f) else []):
        g = g.sort_values("time")
        at_open = _asof(open_time, g["time"].to_numpy(dtype=np.int64), g["rate"].to_numpy(dtype=float),
                        MAX_AGE_H["funding"] * HOUR_MS)
        pay = np.maximum(pay, np.where(np.isfinite(at_open), np.maximum(0.0, -at_open), 0.0))
    out["_fund_short"] = pay
    return out


def synthetic(coin, t0_ms, t1_ms, seed=0, source=MAIN_SOURCE):
    """Offline test data: hourly rows and 8-hourly funding with realistic ranges, labelled as the main source so the
    offline engine reads it like live data (never written to the real history)."""
    rng = np.random.default_rng(zlib.crc32(coin.encode()) % 1000 + seed)
    hours = np.arange(hour_of(t0_ms), t1_ms, HOUR_MS)
    oi = 1e9 * np.exp(np.cumsum(rng.normal(0, 0.01, len(hours))))
    hourly = pd.DataFrame(dict(ts=hours, coin=coin, source=source, oi_usd=oi,
                               ls_ratio=np.clip(1 + np.cumsum(rng.normal(0, 0.02, len(hours))) * 0.1, 0.3, 3),
                               taker_ratio=np.clip(rng.normal(1, 0.15, len(hours)), 0.3, 3)))
    settle = np.arange((t0_ms // (8 * HOUR_MS) + 1) * 8 * HOUR_MS, t1_ms, 8 * HOUR_MS)
    funding = pd.DataFrame(dict(time=settle, coin=coin, source=source,
                                rate=np.clip(rng.normal(0.0001, 0.0002, len(settle)), -0.003, 0.003)))
    return hourly[HOURLY_COLS], funding[FUNDING_COLS]
