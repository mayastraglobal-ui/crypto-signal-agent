"""
Long candle history for the research layers (AGENT_PROMPT.md section 11, Layer B / C).

Years of candles are kept in a local cache folder (on GitHub: the Actions cache, never committed),
one gzipped CSV per coin and timeframe. Each run downloads only the candles that are new since the
last run. If the wanted depth grows (config change) or the cache is gone, everything is downloaded
once again. The raw candles are always re-checked by engine/data_quality.py afterwards.
"""
import json
import os

import pandas as pd

from engine.timeframes import TF_MS

COLS = ["open_time", "open", "high", "low", "close", "volume", "quote_volume"]


def _paths(cache_dir, symbol, tf):
    return os.path.join(cache_dir, f"{symbol}_{tf}.csv.gz"), os.path.join(cache_dir, "index.json")


def _numbers(df, tf):
    df = df[[c for c in COLS if c in df]].astype(float)
    df["open_time"] = df["open_time"].astype("int64")
    df["close_time"] = df["open_time"] + TF_MS[tf] - 1
    return df


def update(feed, symbol, tf, bars, now_ms, cache_dir=None):
    """Up to `bars` newest candles of symbol / tf (fewer when the coin is younger).
    Returns (candles, how) - how = 'cache + N new', 'full download' or 'no cache'."""
    if not cache_dir:
        return feed.klines(symbol, tf, bars), "no cache"
    os.makedirs(cache_dir, exist_ok=True)
    path, index_path = _paths(cache_dir, symbol, tf)
    index = json.load(open(index_path)) if os.path.exists(index_path) else {}
    key = f"{symbol}|{tf}"
    old = pd.read_csv(path) if os.path.exists(path) and index.get(key, 0) >= bars else None
    if old is not None and len(old):
        missing = int((now_ms - int(old["open_time"].max())) // TF_MS[tf]) + 2
        if missing < bars:
            new = feed.klines(symbol, tf, missing)
            df = pd.concat([old, new[[c for c in COLS if c in new]]], ignore_index=True)
            df = df.drop_duplicates("open_time", keep="last")      # the newest download wins
            how = f"cache + {len(new)} new"
        else:
            df, how = feed.klines(symbol, tf, bars), "full download"
    else:
        df, how = feed.klines(symbol, tf, bars), "full download"
    if df is None or len(df) == 0:
        return pd.DataFrame(columns=COLS), how
    df = _numbers(df.sort_values("open_time").tail(bars).reset_index(drop=True), tf)
    df[[c for c in COLS if c in df]].to_csv(path, index=False, compression="gzip")
    index[key] = bars
    json.dump(index, open(index_path, "w"), indent=1)
    return df, how
