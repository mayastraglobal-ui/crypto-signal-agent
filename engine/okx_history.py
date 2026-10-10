"""
OKX USDT-perpetual candle history for the research backtests (roadmap step 2, operator request 2026-10-06).

The operator trades OKX USDT perpetuals, so on the scalping timeframes (config.yaml -> research.okx_timeframes:
30m, 15m, 5m) the backtests use OKX perpetual candles instead of Binance spot:
  1. OKX's monthly files of 1-minute candles (www.okx.com/cdn/okex/traderecords/candlesticks/monthly/...),
     added up to 5m / 15m / 30m candles;
  2. the daily files for the days after the newest monthly file;
  3. the newest candles from OKX's REST API (history-candles).
Months and days already read are remembered in the cache index, so after the first run each run downloads only
what is new. Before a coin was listed on OKX perpetuals there are no OKX candles; research.py then keeps the
Binance spot candles before the first OKX candle (stitch), so a young listing does not shorten the history.

OKX's files follow Beijing time (UTC+8): a "month" starts at 16:00 UTC the day before. Every 30m / 15m / 5m
candle still starts on the same UTC boundary, because 8 hours is a whole number of 30 minutes.
Volume = the coin amount (OKX vol_ccy), quote volume = USDT (vol_quote), as in the live watcher.
"""
import datetime as dt
import io
import json
import os
import time
import zipfile

import numpy as np
import pandas as pd

from engine.timeframes import TF_MS

BASE = "https://www.okx.com"
FILES = BASE + "/cdn/okex/traderecords/candlesticks"
COLS = ["open_time", "open", "high", "low", "close", "volume", "quote_volume"]
CN = dt.timezone(dt.timedelta(hours=8))          # OKX file dates are Beijing time
DAY_MS = 86_400_000
MISSING_AFTER_DAYS = 45                          # a month / day file still 404 this long after it ended = never comes
MAX_DAYS_PER_RUN = 70                            # daily files read per coin per run (they only cover recent days)
MAX_REST_REQUESTS = 60                           # REST pages (100 candles each) per coin x timeframe per run


def inst(base):
    return f"{base}-USDT-SWAP"


def month_url(base, ym):
    return f"{FILES}/monthly/{ym.replace('-', '')}/{inst(base)}-candlesticks-{ym}.zip"


def day_url(base, ymd):
    return f"{FILES}/daily/{ymd.replace('-', '')}/{inst(base)}-candlesticks-{ymd}.zip"


def _cn(ms):
    return dt.datetime.fromtimestamp(ms / 1000, CN)


def _cn_ms(d):
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=CN).timestamp() * 1000)


def months(start_ms, end_ms):
    """Beijing-time months ('YYYY-MM') that END before end_ms, from the one holding start_ms."""
    out, d = [], _cn(start_ms).date().replace(day=1)
    while True:
        nxt = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        if _cn_ms(nxt) > end_ms:
            return out
        out.append(f"{d:%Y-%m}")
        d = nxt


def month_span(ym):
    d = dt.date(int(ym[:4]), int(ym[5:7]), 1)
    nxt = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    return _cn_ms(d), _cn_ms(nxt)


def days(start_ms, end_ms):
    """Beijing-time days ('YYYY-MM-DD') that END before end_ms, from the one holding start_ms."""
    out, d = [], _cn(start_ms).date()
    while _cn_ms(d + dt.timedelta(days=1)) <= end_ms:
        out.append(f"{d:%Y-%m-%d}")
        d += dt.timedelta(days=1)
    return out


def parse_zip(content):
    """1-minute candles of one OKX file. The files only cover FINISHED months / days (months() and days() never
    ask for one still running), so every candle in them is closed: their `confirm` column is ignored - OKX's older
    archive files (e.g. 2023-09 to 2023-11 and 2024-02 to 2024-07) say confirm = 0 on every row, and dropping those
    rows left months-long holes that made the 5-year 30m / 15m history UNSAFE (found 2026-10-09)."""
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        name = next(n for n in z.namelist() if n.endswith(".csv"))
        df = pd.read_csv(z.open(name))
    out = pd.DataFrame({"open_time": df["open_time"].astype("int64"), "open": df["open"], "high": df["high"],
                        "low": df["low"], "close": df["close"], "volume": df["vol_ccy"],
                        "quote_volume": df["vol_quote"]})
    out = out.astype({c: float for c in COLS[1:]}).drop_duplicates("open_time", keep="last")   # a minute repeated
    return out.sort_values("open_time").reset_index(drop=True)


def resample(m1, tf, until_ms=None):
    """1-minute candles -> tf candles on UTC boundaries. A candle is kept only when it is over (it ends at or before
    until_ms, default: the last minute present) - never a half-built candle."""
    if m1 is None or not len(m1):
        return pd.DataFrame(columns=COLS)
    step = TF_MS[tf]
    g = (m1["open_time"].to_numpy(dtype=np.int64) // step) * step
    out = m1.assign(_g=g).groupby("_g", sort=True).agg(open=("open", "first"), high=("high", "max"),
                                                        low=("low", "min"), close=("close", "last"),
                                                        volume=("volume", "sum"),
                                                        quote_volume=("quote_volume", "sum"))
    out = out.reset_index().rename(columns={"_g": "open_time"})
    end = until_ms if until_ms is not None else int(m1["open_time"].max()) + 60_000
    return out[out["open_time"] + step <= end][COLS].reset_index(drop=True)


def missing(okx, tf, bars, now_ms):
    """Candles missing from an OKX frame inside the window it should cover (the newest `bars` closed candles, or
    since its first candle when that is younger). A coin OKX delisted and listed again has a hole of months: ZEC's
    perpetual archive stops in 2024-01 and starts again on 2025-11-06 (found 2026-10-10)."""
    if okx is None or not len(okx):
        return bars
    step = TF_MS[tf]
    start = max(int(okx["open_time"].min()), (now_ms // step - bars) * step)
    want = (now_ms // step) * step - start
    have = int(((okx["open_time"] >= start) & (okx["open_time"] + step <= now_ms)).sum())
    return max(0, want // step - have)


def _day(ms):
    return f"{dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc):%Y-%m-%d}"


def stitch(okx, spot, bars, tf):
    """OKX perpetual candles, with Binance spot candles where OKX has none: before the first OKX candle (a young OKX
    listing) and inside OKX holes (a delisted and relisted perpetual). Never after the newest OKX candle.
    Returns (candles, note)."""
    if okx is None or not len(okx):
        return spot, "Binance spot (no OKX perpetual candles)"
    step = TF_MS[tf]
    first, last = int(okx["open_time"].min()), int(okx["open_time"].max())
    if spot is None or not len(spot):
        return okx.tail(bars).reset_index(drop=True), "OKX perpetual"
    t = spot["open_time"].astype("int64")
    fill = spot[(t <= last) & ~t.isin(okx["open_time"].astype("int64"))]
    df = pd.concat([fill[COLS], okx[COLS]], ignore_index=True).astype({"open_time": "int64"})
    df = df.sort_values("open_time").tail(bars).reset_index(drop=True)
    ft = fill["open_time"].astype("int64")
    ft = ft[ft >= int(df["open_time"].min())].sort_values().to_numpy()   # Binance candles inside the kept window
    if not len(ft):
        return okx.tail(bars).reset_index(drop=True), "OKX perpetual"
    df["close_time"] = df["open_time"] + step - 1
    holes = []                                   # runs of 1+ day of Binance candles inside the OKX history
    inside = ft[ft > first]
    if len(inside):
        cuts = np.flatnonzero(np.diff(inside) > step) + 1
        for run in np.split(inside, cuts):
            if run[-1] + step - run[0] >= DAY_MS:
                holes.append(f"{_day(int(run[0]))} to {_day(int(run[-1]) + step)}")
    note = f"OKX perpetual from {_day(first)}, Binance spot before" if (ft < first).any() else "OKX perpetual"
    if holes:
        note += f" and in {len(holes)} gap(s): " + ", ".join(holes)
    elif len(inside):
        note += f" ({len(inside)} missing candle(s) from Binance spot)"
    return df, note


class History:
    """OKX perpetual candles per coin, cached in cache_dir (okx_<COIN>_<tf>.csv.gz + okx_index.json).
    get(url, params=None) -> response (requests.get by default; tests pass a fake)."""

    def __init__(self, cache_dir, get=None, sleep=time.sleep):
        import requests
        self.dir, self.sleep = cache_dir, sleep
        self.get = get or (lambda url, params=None: requests.get(url, params=params, timeout=60))
        os.makedirs(cache_dir, exist_ok=True)
        self.index_path = os.path.join(cache_dir, "okx_index.json")
        try:
            with open(self.index_path) as f:
                self.index = json.load(f)
        except (OSError, ValueError):
            self.index = {}

    def _path(self, base, tf):
        return os.path.join(self.dir, f"okx_{base}_{tf}.csv.gz")

    def _file(self, url):
        """bytes / 'missing' (404) / None (try again next run)."""
        try:
            r = self.get(url)
        except Exception:
            return None
        if r.status_code == 200 and r.content[:2] == b"PK":
            return r.content
        return "missing" if r.status_code == 404 else None

    def _rest(self, base, tf, since_ms):
        """Newest closed candles after since_ms from the REST API (at most MAX_REST_REQUESTS pages)."""
        bar = {"5m": "5m", "15m": "15m", "30m": "30m", "1h": "1H", "4h": "4H"}[tf]
        rows, after = [], None
        for _ in range(MAX_REST_REQUESTS):
            p = {"instId": inst(base), "bar": bar, "limit": 100}
            if after:
                p["after"] = after
            try:
                j = self.get(BASE + "/api/v5/market/history-candles", p).json()
            except Exception:
                break
            data = (j.get("data") or []) if j.get("code") == "0" else []
            if not data:
                break
            rows += data
            after = data[-1][0]
            if int(after) <= since_ms or len(data) < 100:
                break
            self.sleep(0.12)
        rows = [r for r in rows if (len(r) < 9 or r[8] == "1") and int(r[0]) > since_ms]
        if not rows:
            return pd.DataFrame(columns=COLS)
        df = pd.DataFrame([[r[0], r[1], r[2], r[3], r[4], r[6], r[7] if len(r) > 7 else np.nan] for r in rows],
                          columns=COLS)
        return df.astype({"open_time": "int64", **{c: float for c in COLS[1:]}})

    def coin(self, base, wants, now_ms):
        """{tf: candles} of base's OKX perpetual, newest wants[tf] candles at most (only CLOSED candles).
        Returns ({tf: DataFrame}, note). An empty frame = no OKX perpetual history for that coin."""
        idx = self.index.setdefault(base, {"months": {}, "days": {}})
        start = min(now_ms - n * TF_MS[tf] for tf, n in wants.items())
        old = {}
        for tf in wants:
            try:
                old[tf] = pd.read_csv(self._path(base, tf))
            except (OSError, ValueError):
                old[tf] = pd.DataFrame(columns=COLS)
        pieces = {tf: [] for tf in wants}
        new_months = new_days = 0
        for ym in months(start, now_ms):
            if ym in idx["months"]:
                continue
            got = self._file(month_url(base, ym))
            if isinstance(got, bytes):
                m1 = parse_zip(got)
                for tf in wants:
                    pieces[tf].append(resample(m1, tf, month_span(ym)[1]))
                idx["months"][ym], new_months = "ok", new_months + 1
            elif got == "missing" and now_ms - month_span(ym)[1] > MISSING_AFTER_DAYS * DAY_MS:
                idx["months"][ym] = "missing"
        covered = max([month_span(m)[1] for m, s in idx["months"].items() if s == "ok"], default=None)
        day_from = max(start, covered or start, now_ms - MAX_DAYS_PER_RUN * DAY_MS)
        for ymd in days(day_from, now_ms):
            if ymd in idx["days"]:
                continue
            got = self._file(day_url(base, ymd))
            if isinstance(got, bytes):
                m1 = parse_zip(got)
                d0 = _cn_ms(dt.date.fromisoformat(ymd))
                for tf in wants:
                    pieces[tf].append(resample(m1, tf, d0 + DAY_MS))
                idx["days"][ymd], new_days = "ok", new_days + 1
            elif got == "missing" and now_ms - _cn_ms(dt.date.fromisoformat(ymd)) > MISSING_AFTER_DAYS * DAY_MS:
                idx["days"][ymd] = "missing"
        if covered:                                   # days inside a month file are no longer needed in the index
            idx["days"] = {k: v for k, v in idx["days"].items() if _cn_ms(dt.date.fromisoformat(k)) >= covered}
        out = {}
        for tf, n in wants.items():
            parts = [old[tf]] + pieces[tf]
            last = max([int(p["open_time"].max()) for p in parts if len(p)], default=None)
            fresh = self._rest(base, tf, last if last is not None else now_ms - n * TF_MS[tf])
            parts.append(fresh[fresh["open_time"] + TF_MS[tf] <= now_ms])
            df = pd.concat([p[COLS] for p in parts if len(p)], ignore_index=True) if any(len(p) for p in parts) \
                else pd.DataFrame(columns=COLS)
            if len(df):
                df = df.astype({"open_time": "int64"}).drop_duplicates("open_time", keep="last")
                df = df.sort_values("open_time").tail(n).reset_index(drop=True)
                df[COLS].to_csv(self._path(base, tf), index=False, compression="gzip")
            df = df.astype({"open_time": "int64", **{c: float for c in COLS[1:]}}) if len(df) else df
            df["close_time"] = df["open_time"] + TF_MS[tf] - 1
            out[tf] = df
        with open(self.index_path, "w") as f:
            json.dump(self.index, f, indent=1, sort_keys=True)
        return out, f"{new_months} month file(s), {new_days} day file(s) new"
