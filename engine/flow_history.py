"""
Order-flow history: the volume delta (aggressive buys - aggressive sells) per 5m candle, for the playbook's CVD
(docs/PLAYBOOK.md; operator decision 2026-10-06: use real aggressive volume).

Backtests: Binance USDT-M futures 5m candles from data.binance.vision (monthly files, then daily files) - each has the
taker buy volume, so delta = 2 x taker buy volume - volume (coin units). The newest day(s): OKX's taker volume per 5m
(REST, coin units). Cached like the candle history (data/history: flow_<COIN>_5m.csv.gz + flow_index.json); a later
run downloads only new days. The CVD resets at 00:00 UTC, so one day never mixes the two sources.
"""
import datetime as dt
import io
import json
import os
import time
import zipfile

import numpy as np
import pandas as pd

VISION = "https://data.binance.vision/data/futures/um"
OKX = "https://www.okx.com/api/v5/rubik/stat/taker-volume-contract"
DAY_MS, FIVE = 86_400_000, 300_000
COLS = ["open_time", "delta", "src"]                   # src: 1 = Binance futures, 2 = OKX
MISSING_AFTER_DAYS = 45


def _months(start_ms, end_ms):
    out, d = [], dt.datetime.fromtimestamp(start_ms / 1000, dt.timezone.utc).date().replace(day=1)
    while True:
        nxt = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        if dt.datetime(nxt.year, nxt.month, 1, tzinfo=dt.timezone.utc).timestamp() * 1000 > end_ms:
            return out
        out.append(f"{d:%Y-%m}")
        d = nxt


def _ms(d):
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp() * 1000)


def parse_vision(content):
    """Binance kline zip -> DataFrame(open_time, delta, src=1)."""
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        raw = z.read(z.namelist()[0]).decode()
    first = raw.split("\n", 1)[0]
    df = pd.read_csv(io.StringIO(raw), header=0 if first.startswith("open_time") else None)
    if not first.startswith("open_time"):
        df = df.iloc[:, :11]
        df.columns = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "count",
                      "taker_buy_volume", "taker_buy_quote_volume"]
    ot = df["open_time"].astype("int64")
    ot = np.where(ot > 10**14, ot // 1000, ot)        # newer files are in microseconds
    return pd.DataFrame({"open_time": ot, "delta": 2 * df["taker_buy_volume"].astype(float) - df["volume"].astype(float),
                         "src": 1})


class History:
    def __init__(self, cache_dir, get=None, sleep=time.sleep):
        import requests
        self.dir, self.sleep = cache_dir, sleep
        self.get = get or (lambda url, params=None: requests.get(url, params=params, timeout=60))
        os.makedirs(cache_dir, exist_ok=True)
        self.index_path = os.path.join(cache_dir, "flow_index.json")
        try:
            with open(self.index_path) as f:
                self.index = json.load(f)
        except (OSError, ValueError):
            self.index = {}

    def _file(self, url):
        try:
            r = self.get(url)
        except Exception:
            return None
        if r.status_code == 200 and r.content[:2] == b"PK":
            return r.content
        return "missing" if r.status_code == 404 else None

    def okx_recent(self, base, since_ms, now_ms, pages=4):
        """OKX taker volume (coin units) per 5m candle after since_ms: delta = buy - sell."""
        rows, end = [], None
        for _ in range(pages):
            p = {"instId": f"{base}-USDT-SWAP", "period": "5m", "unit": "0", "limit": 100}
            if end:
                p["end"] = end
            try:
                j = self.get(OKX, p).json()
            except Exception:
                break
            data = (j.get("data") or []) if j.get("code") == "0" else []
            if not data:
                break
            rows += data
            end = data[-1][0]
            if int(end) <= since_ms:
                break
            self.sleep(0.2)
        df = pd.DataFrame([(int(r[0]), float(r[2]) - float(r[1])) for r in rows], columns=["open_time", "delta"])
        df["src"] = 2
        return df[(df["open_time"] > since_ms) & (df["open_time"] + FIVE <= now_ms)]

    def coin(self, base, bars, now_ms):
        """DataFrame(open_time, delta, src) of the newest `bars` 5m candles (missing candles simply absent)."""
        idx = self.index.setdefault(base, {"months": {}, "days": {}})
        path = os.path.join(self.dir, f"flow_{base}_5m.csv.gz")
        try:
            old = pd.read_csv(path)
        except (OSError, ValueError):
            old = pd.DataFrame(columns=COLS)
        start = now_ms - bars * FIVE
        sym = f"{base}USDT"
        parts = [old]
        for ym in _months(start, now_ms):
            if ym in idx["months"]:
                continue
            got = self._file(f"{VISION}/monthly/klines/{sym}/5m/{sym}-5m-{ym}.zip")
            if isinstance(got, bytes):
                parts.append(parse_vision(got))
                idx["months"][ym] = "ok"
            elif got == "missing":
                end = _ms((dt.date(int(ym[:4]), int(ym[5:]), 28) + dt.timedelta(days=4)).replace(day=1))
                if now_ms - end > MISSING_AFTER_DAYS * DAY_MS:
                    idx["months"][ym] = "missing"
        covered = max([_ms((dt.date(int(m[:4]), int(m[5:]), 28) + dt.timedelta(days=4)).replace(day=1))
                       for m, s in idx["months"].items() if s == "ok"], default=start)
        d = dt.datetime.fromtimestamp(max(covered, start, now_ms - 70 * DAY_MS) / 1000, dt.timezone.utc).date()
        today = dt.datetime.fromtimestamp(now_ms / 1000, dt.timezone.utc).date()
        while d < today:
            key = f"{d:%Y-%m-%d}"
            if key not in idx["days"]:
                got = self._file(f"{VISION}/daily/klines/{sym}/5m/{sym}-5m-{key}.zip")
                if isinstance(got, bytes):
                    parts.append(parse_vision(got))
                    idx["days"][key] = "ok"
                elif got == "missing" and now_ms - _ms(d) > MISSING_AFTER_DAYS * DAY_MS:
                    idx["days"][key] = "missing"
            d += dt.timedelta(days=1)
        idx["days"] = {k: v for k, v in idx["days"].items() if _ms(dt.date.fromisoformat(k)) >= covered}
        df = pd.concat([p[COLS] for p in parts if len(p)], ignore_index=True) if any(len(p) for p in parts) \
            else pd.DataFrame(columns=COLS)
        df = df.astype({"open_time": "int64"}).drop_duplicates("open_time", keep="last").sort_values("open_time")
        # today (and any day Binance has not published yet): OKX, whole UTC days only from OKX (CVD resets daily)
        last_day = (int(df["open_time"].max()) // DAY_MS + 1) * DAY_MS if len(df) else now_ms // DAY_MS * DAY_MS
        recent = self.okx_recent(base, last_day - 1, now_ms)
        recent = recent[recent["open_time"] >= last_day]
        df = df.tail(bars).reset_index(drop=True)
        if len(df):
            df[COLS].to_csv(path, index=False, compression="gzip")
        with open(self.index_path, "w") as f:
            json.dump(self.index, f, indent=1, sort_keys=True)
        return pd.concat([df, recent[COLS]], ignore_index=True).sort_values("open_time").reset_index(drop=True)


def okx_today(base, now_ms, get=None):
    """Today's (UTC) delta per 5m candle from OKX - what the hourly scan and the live watcher need: the CVD resets
    at 00:00 UTC, so today's candles are enough for every playbook check made now."""
    import requests
    h = History.__new__(History)
    h.get = get or (lambda url, params=None: requests.get(url, params=params, timeout=20))
    h.sleep = time.sleep
    return h.okx_recent(base, now_ms // DAY_MS * DAY_MS - 1, now_ms).sort_values("open_time").reset_index(drop=True)


def resample(flow, tf_ms):
    """The delta per tf_ms candle (step 3d: 15m triggers) = the sum of its 5m deltas; a candle with a 5m delta missing
    is left out (unknown, never a partial sum)."""
    if flow is None or not len(flow) or int(tf_ms) == FIVE:
        return flow
    per = int(tf_ms) // FIVE
    f = pd.DataFrame({"t": flow["open_time"].to_numpy(dtype=np.int64) // int(tf_ms) * int(tf_ms),
                      "delta": flow["delta"].to_numpy(dtype=float)})
    g = f.groupby("t")["delta"].agg(["sum", "count"])
    g = g[g["count"] == per]
    return pd.DataFrame({"open_time": g.index.to_numpy(dtype=np.int64), "delta": g["sum"].to_numpy(), "src": 0})


def align(open_time, flow):
    """The delta of each candle (by open time); NaN where unknown."""
    if flow is None or not len(flow):
        return np.full(len(open_time), np.nan)
    s = pd.Series(flow["delta"].to_numpy(dtype=float), index=flow["open_time"].to_numpy(dtype=np.int64))
    s = s[~s.index.duplicated(keep="last")]
    return s.reindex(np.asarray(open_time, dtype=np.int64)).to_numpy()
