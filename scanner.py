#!/usr/bin/env python3
"""
Crypto Signal Agent - scanner + backtester
==========================================
Every run it:
  1. picks liquid, established coins (skips meme / AI / stable / brand-new coins)
  2. downloads candles for 4h, 1h, 30m, 15m, 5m
  3. backtests every strategy in strategies.yaml (spec v3, with fees + slippage), only in the
     market regimes each strategy allows and with higher-timeframe permission
  4. moves each strategy version along its lifecycle (BACKTESTING / VALIDATION / FAILED ...)
  5. finds fresh entry signals and builds a full trade plan (entry, SL, targets, hold time);
     only APPROVED strategies (operator's yes) give emailed signals
  6. tracks every signal through its states (5m confirmation, active, TP1, closed - Phase 10) to see
     if it REALLY worked (live proof), and opens every report with the position book
  7. writes reports/latest.md (for you) and reports/latest.json (for Claude)

It never places trades. Signals only.

Run:  python scanner.py            (live data)
      python scanner.py --offline  (synthetic data, for testing the code)
"""
import argparse
import datetime as dt
import json
import math
import os
import sys
import time
import zlib

import numpy as np
import pandas as pd
import requests
import yaml

import publish_live

from engine import attribution as att
from engine import briefs
from engine import charts
from engine import confirm5m as c5m
from engine import data_quality as dq
from engine import digest
from engine import evidence as evid
from engine import features as fe
from engine import lifecycle as lc
from engine import memory as mem
from engine import positions as pos
from engine import regime as rg
from engine import risk as rk
from engine import research as rs
from engine import smc
from engine import strategy_spec as sspec
from engine import timeframes as tfm
from engine import universe as uni

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(ROOT, "reports")
MEMORY = os.path.join(ROOT, "memory")
REGISTRY = os.path.join(MEMORY, "strategy_registry.csv")
TF_MS = tfm.TF_MS
DASH_BARS = 120                    # candles per coin and timeframe kept for the dashboard charts (1h = 5 days)
HTF = tfm.LEGACY_HTF            # higher timeframe used by the current strategies' htf_up / htf_down
TF_ORDER = tfm.TRADE_ORDER      # timeframes the strategies run on
CONTEXT = tfm.CONTEXT_TFS       # 1w, 1d: downloaded for higher-timeframe context
BJ = dt.timezone(dt.timedelta(hours=8))


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# =====================================================================
# 1. MARKET DATA  (Binance public data, OKX as fallback)
# =====================================================================
class Binance:
    name = "Binance"
    BASES = ["https://data-api.binance.vision", "https://api.binance.com",
             "https://api1.binance.com", "https://api-gcp.binance.com"]

    def __init__(self):
        self.s = requests.Session()
        self.base = None

    def _get(self, path, params=None):
        bases = [self.base] if self.base else self.BASES
        last = None
        for base in bases:
            for attempt in range(4):
                try:
                    r = self.s.get(base + path, params=params, timeout=20)
                    if r.status_code == 200:
                        self.base = base
                        return r.json()
                    last = f"{base} HTTP {r.status_code}"
                    if r.status_code in (418, 429) or r.status_code >= 500:
                        time.sleep(2 + 3 * attempt)
                        continue
                    break
                except requests.RequestException as e:
                    last = f"{base} {e.__class__.__name__}"
                    time.sleep(1 + attempt)
        raise RuntimeError(f"Binance request failed: {last}")

    def tickers(self):
        out = []
        for t in self._get("/api/v3/ticker/24hr"):
            out.append({"symbol": t["symbol"], "last": float(t["lastPrice"]),
                        "change_pct": float(t["priceChangePercent"]),
                        "quote_volume": float(t["quoteVolume"]),
                        "bid": float(t.get("bidPrice") or 0), "ask": float(t.get("askPrice") or 0)})
        return out

    def depth(self, symbol):
        d = self._get("/api/v3/depth", {"symbol": symbol, "limit": 1000})
        return ([(float(p), float(q)) for p, q in d["bids"]],
                [(float(p), float(q)) for p, q in d["asks"]])

    def klines(self, symbol, tf, n):
        rows, end = [], None
        while len(rows) < n:
            lim = min(1000, n - len(rows))
            p = {"symbol": symbol, "interval": tf, "limit": lim}
            if end:
                p["endTime"] = end
            data = self._get("/api/v3/klines", p)
            if not data:
                break
            rows = data + rows
            end = data[0][0] - 1
            if len(data) < lim:
                break
            time.sleep(0.05)
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame([r[:6] + [r[7]] for r in rows],
                          columns=["open_time", "open", "high", "low", "close", "volume", "quote_volume"])
        return _finish(df, tf)


class OKX:
    name = "OKX"
    BASE = "https://www.okx.com"
    BAR = {"5m": "5m", "15m": "15m", "30m": "30m", "1h": "1H", "4h": "4H", "1d": "1Dutc", "1w": "1Wutc"}

    def __init__(self):
        self.s = requests.Session()

    def _get(self, path, params=None):
        last = None
        for attempt in range(4):
            try:
                r = self.s.get(self.BASE + path, params=params, timeout=20)
                if r.status_code == 200 and r.json().get("code") == "0":
                    return r.json()["data"]
                last = f"HTTP {r.status_code} {r.text[:120]}"
            except requests.RequestException as e:
                last = e.__class__.__name__
            time.sleep(1.5 + 2 * attempt)
        raise RuntimeError(f"OKX request failed: {last}")

    def tickers(self):
        out = []
        for t in self._get("/api/v5/market/tickers", {"instType": "SPOT"}):
            base, _, quote = t["instId"].partition("-")
            last, op = float(t["last"] or 0), float(t["open24h"] or 0)
            out.append({"symbol": base + quote, "last": last,
                        "change_pct": (last / op - 1) * 100 if op else 0.0,
                        "quote_volume": float(t["volCcy24h"] or 0),
                        "bid": float(t.get("bidPx") or 0), "ask": float(t.get("askPx") or 0)})
        return out

    def depth(self, symbol):
        d = self._get("/api/v5/market/books", {"instId": symbol[:-4] + "-" + symbol[-4:], "sz": 400})[0]
        return ([(float(r[0]), float(r[1])) for r in d["bids"]],
                [(float(r[0]), float(r[1])) for r in d["asks"]])

    def klines(self, symbol, tf, n):
        inst = symbol[:-4] + "-" + symbol[-4:]
        rows, after = [], None
        while len(rows) < n:
            p = {"instId": inst, "bar": self.BAR[tf], "limit": 100}
            if after:
                p["after"] = after
            data = self._get("/api/v5/market/history-candles", p)
            if not data:
                break
            rows += data
            after = data[-1][0]
            time.sleep(0.12)
            if len(data) < 100:
                break
        if not rows:
            return pd.DataFrame()
        rows = [r for r in rows if len(r) < 9 or r[8] == "1"]   # confirmed candles only
        df = pd.DataFrame([r[:6] + [r[7] if len(r) > 7 else np.nan] for r in rows],
                          columns=["open_time", "open", "high", "low", "close", "volume", "quote_volume"])
        return _finish(df, tf)


def _finish(df, tf):
    """Numbers only. Sorting, duplicates and unfinished candles are handled (and reported)
    by engine/data_quality.py - always load candles through fetch_checked()."""
    df = df.astype(float)
    df["open_time"] = df["open_time"].astype("int64")
    df["close_time"] = df["open_time"] + TF_MS[tf] - 1
    return df


def fetch_checked(feed, symbol, tf, n, dq_cfg):
    """Download candles and run the data-quality checks. Returns (clean_df, report).
    clean_df has CLOSED candles only, sorted, without duplicates."""
    raw = feed.klines(symbol, tf, n)
    return dq.check_candles(raw, TF_MS[tf], int(time.time() * 1000), dq_cfg)


def cross_timeframe_check(data, sym, base, quality):
    """Each higher candle must agree with the lower candles inside it (e.g. 4H high = highest of
    its four 1H highs). A disagreement makes the HIGHER timeframe DEGRADED (no signals from it).
    Returns {"1h>4h": {checked, mismatches, examples}, ...}."""
    out = {}
    for lo_tf, hi_tf in tfm.CONSISTENCY_PAIRS:
        lo, hi = data.get((sym, lo_tf)), data.get((sym, hi_tf))
        if lo is None or hi is None:
            continue
        r = tfm.consistency(lo, hi, TF_MS[lo_tf], TF_MS[hi_tf])
        out[f"{lo_tf}>{hi_tf}"] = r
        if r["mismatches"] and (base, hi_tf) in quality:
            dq.add_problem(quality[(base, hi_tf)], dq.DEGRADED,
                           f"{r['mismatches']} of {r['checked']} candle(s) disagree with the {lo_tf} "
                           f"candles inside them ({'; '.join(r['examples'])})")
    return out


class Synthetic:
    """Fake but realistic-looking prices, used only for --offline testing.
    A scenario (dict, see --scenario) can set per-coin 24h volume, 24h change, order-book depth,
    a daily-volume factor (for volume-spike tests) and extra coins."""
    name = "Synthetic (offline test)"
    NAMES = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "LINK", "AVAX", "DOGE", "FET", "USDC",
             "DOT", "LTC", "TRX", "ATOM", "NEWCOIN", "FAKEUSD", "PUMP"]

    def __init__(self, seed=7, fault=None, scenario=None):
        self.seed = seed
        self.fault = fault   # plant a data problem to test the safety checks (see --fault)
        sc = scenario or {}
        self.sc = sc
        rng = np.random.default_rng(seed)
        names = self.NAMES + sc.get("extra_coins", [])
        self.vol24 = {n: float(sc.get("quote_volume", {}).get(n, rng.uniform(1e8, 2e9))) for n in names}
        self.change = {n: float(sc.get("change_pct", {}).get(n, 40.0 if n == "PUMP" else rng.normal(0, 3)))
                       for n in names}

    def _rng(self, *key):
        return np.random.default_rng(zlib.crc32(repr((key, self.seed)).encode()))

    def tickers(self):
        return [{"symbol": n + "USDT", "last": 1.0, "change_pct": self.change[n],
                 "quote_volume": self.vol24[n], "bid": 0.9999, "ask": 1.0001} for n in self.vol24]

    def depth(self, symbol):
        per_side = float(self.sc.get("depth_usd", {}).get(symbol[:-4], 5e6))
        levels = 50
        bids = [(100 * (1 - 0.0001 * (i + 1)), per_side / levels / 100) for i in range(levels)]
        asks = [(100 * (1 + 0.0001 * (i + 1)), per_side / levels / 100) for i in range(levels)]
        return bids, asks

    def klines(self, symbol, tf, n):
        coin = symbol[:-4]
        if coin == "NEWCOIN" and tf == "1d":
            n = 40
        rng = self._rng(symbol, tf)
        vol = {"5m": .003, "15m": .005, "30m": .007, "1h": .01, "4h": .02, "1d": .04, "1w": .1}[tf]
        if coin == "FAKEUSD":
            vol = 0.0005       # behaves like a stablecoin
        regime = np.repeat(rng.choice([-1, 0, 1], size=n // 150 + 1), 150)[:n]
        ret = rng.standard_t(4, n) * vol * 0.7 + (0 if coin == "FAKEUSD" else regime * vol * 0.12)
        if coin == "FAKEUSD":
            close = 100 * (1 + np.clip(ret, -0.005, 0.005))
        else:
            close = 100 * np.exp(np.cumsum(ret))
        opn = np.r_[close[0], close[:-1]]
        spread = np.abs(rng.normal(0, vol * 0.6, n)) * close
        high = np.maximum(opn, close) + spread
        low = np.minimum(opn, close) - spread
        volu = rng.lognormal(10, 0.5, n) * (1 + 3 * np.abs(ret) / vol / 10)
        # quote volume: on average matches the 24h ticker volume (scaled to the candle length)
        daily = self.vol24.get(coin, 1e8) * float(self.sc.get("daily_volume_factor", {}).get(coin, 1.0))
        qvol = volu / volu.mean() * daily * TF_MS[tf] / TF_MS["1d"]
        now = int(time.time() * 1000) // TF_MS[tf] * TF_MS[tf]
        ot = now - TF_MS[tf] * np.arange(n, 0, -1)
        df = pd.DataFrame({"open_time": ot, "open": opn, "high": high, "low": low,
                           "close": close, "volume": volu, "quote_volume": qvol})
        if symbol == "BTCUSDT" and self.fault == "stale_btc":
            df["open_time"] -= 10 * TF_MS[tf]          # feed stopped 10 candles ago
        elif symbol == "ETHUSDT" and self.fault == "bad_prices":
            df.loc[df.index[-5], "low"] = -1.0          # impossible negative price
        return _finish(df, tf)


def fear_greed(offline):
    if offline:
        return None
    try:
        d = requests.get("https://api.alternative.me/fng/?limit=2", timeout=15).json()["data"]
        return {"value": int(d[0]["value"]), "label": d[0]["value_classification"],
                "yesterday": int(d[1]["value"])}
    except Exception:
        return None


# =====================================================================
# 2. INDICATORS + RULE LANGUAGE
# =====================================================================
def _wilder(x, n):
    return x.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def make_namespace(df, feats=None):
    """Everything a strategy rule can use. Results are cached per candle table.
    feats (engine.features.compute) adds the feature engine's columns by name, e.g.
    displacement_up, bull_engulf, close_loc, rel_vol, structure_up, stoch_rsi_k, vwap, obv."""
    cache = {}
    o, h, l, c, v = (df[k] for k in ("open", "high", "low", "close", "volume"))

    def cached(fn):
        def wrap(*args):
            key = (fn.__name__,) + tuple(id(a) if isinstance(a, pd.Series) else a for a in args)
            if key not in cache:
                cache[key] = (fn(*args), args)   # keep args alive so ids stay unique
            return cache[key][0]
        wrap.__name__ = fn.__name__
        return wrap

    @cached
    def ema(x, n): return x.ewm(span=n, adjust=False, min_periods=n).mean()

    @cached
    def sma(x, n): return x.rolling(n, min_periods=n).mean()

    @cached
    def rsi(x, n=14):
        d = x.diff()
        au, ad = _wilder(d.clip(lower=0), n), _wilder(-d.clip(upper=0), n)
        r = 100 - 100 / (1 + au / ad.replace(0, np.nan))
        return r.where(~((ad == 0) & au.notna()), 100.0)

    @cached
    def tr(): return pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)

    @cached
    def atr(n=14): return _wilder(tr(), n)

    @cached
    def adx(n=14):
        up, dn = h.diff(), -l.diff()
        pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=df.index)
        mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=df.index)
        a = _wilder(tr(), n)
        pdi, mdi = 100 * _wilder(pdm, n) / a, 100 * _wilder(mdm, n) / a
        dx = 100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan)
        return _wilder(dx, n)

    @cached
    def macd_line(x, f=12, s=26): return ema(x, f) - ema(x, s)

    @cached
    def macd_signal(x, f=12, s=26, sig=9): return ema(macd_line(x, f, s), sig)

    @cached
    def macd_hist(x, f=12, s=26, sig=9): return macd_line(x, f, s) - macd_signal(x, f, s, sig)

    @cached
    def bb_mid(x, n=20): return sma(x, n)

    @cached
    def _std(x, n): return x.rolling(n, min_periods=n).std(ddof=0)

    @cached
    def bb_upper(x, n=20, k=2): return sma(x, n) + k * _std(x, n)

    @cached
    def bb_lower(x, n=20, k=2): return sma(x, n) - k * _std(x, n)

    @cached
    def bb_width(x, n=20, k=2): return (bb_upper(x, n, k) - bb_lower(x, n, k)) / sma(x, n)

    @cached
    def highest(x, n): return x.rolling(n, min_periods=n).max()

    @cached
    def lowest(x, n): return x.rolling(n, min_periods=n).min()

    @cached
    def shift(x, n=1): return x.shift(n)

    def prev(x): return shift(x, 1)

    @cached
    def vol_sma(n=20): return sma(v, n)

    @cached
    def pct_rank(x, n=100):
        return x.rolling(n, min_periods=n).apply(lambda w: (w[:-1] < w[-1]).mean(), raw=True)

    @cached
    def supertrend_dir(n=10, mult=3):
        a = atr(n).to_numpy()
        hl2 = ((h + l) / 2).to_numpy()
        cc = c.to_numpy()
        ub, lb = hl2 + mult * a, hl2 - mult * a
        fu, fl = ub.copy(), lb.copy()
        d = np.full(len(cc), np.nan)
        for i in range(1, len(cc)):
            if np.isnan(a[i]):
                continue
            if not np.isnan(fu[i - 1]):
                fu[i] = ub[i] if (ub[i] < fu[i - 1] or cc[i - 1] > fu[i - 1]) else fu[i - 1]
                fl[i] = lb[i] if (lb[i] > fl[i - 1] or cc[i - 1] < fl[i - 1]) else fl[i - 1]
            prevd = d[i - 1] if not np.isnan(d[i - 1]) else 1
            if prevd == 1:
                d[i] = -1 if cc[i] < fl[i] else 1
            else:
                d[i] = 1 if cc[i] > fu[i] else -1
        return pd.Series(d, index=df.index)

    def cross_up(a, b):
        pb = b.shift(1) if isinstance(b, pd.Series) else b
        return (a > b) & (a.shift(1) <= pb)

    def cross_down(a, b):
        pb = b.shift(1) if isinstance(b, pd.Series) else b
        return (a < b) & (a.shift(1) >= pb)

    def within(x, n):
        """x was true on this candle or one of the n-1 candles before."""
        return x.astype(float).rolling(int(n), min_periods=1).max().fillna(0) > 0

    def bars_since(x):
        """Candles since x was last true (0 = this candle); NaN if never."""
        b = x.astype("boolean").fillna(False).to_numpy(dtype=bool)
        pos = np.arange(len(b))
        last = np.maximum.accumulate(np.where(b, pos, -1))
        return pd.Series(np.where(last >= 0, pos - last, np.nan), index=df.index)

    ns = dict(open=o, high=h, low=l, close=c, volume=v,
              htf_up=df.get("htf_up", pd.Series(True, index=df.index)),
              htf_down=df.get("htf_down", pd.Series(True, index=df.index)),
              ema=ema, sma=sma, rsi=rsi, atr=atr, adx=adx, macd_line=macd_line,
              macd_signal=macd_signal, macd_hist=macd_hist, bb_mid=bb_mid,
              bb_upper=bb_upper, bb_lower=bb_lower, bb_width=bb_width, highest=highest,
              lowest=lowest, shift=shift, prev=prev, vol_sma=vol_sma, pct_rank=pct_rank,
              supertrend_dir=supertrend_dir, cross_up=cross_up, cross_down=cross_down,
              within=within, bars_since=bars_since, abs=abs, min=min, max=max, np=np)
    if feats is not None:
        for col in feats.columns:
            if col not in ns:           # never replace an existing building block (e.g. atr())
                ns[col] = pd.Series(feats[col].to_numpy(), index=df.index)
    return ns


def eval_rules(rules, ns, index):
    """ALL rules true -> True. Returns a boolean numpy array."""
    if not rules:
        return np.zeros(len(index), dtype=bool)
    out = pd.Series(True, index=index)
    for rule in rules:
        res = eval(str(rule), {"__builtins__": {}}, ns)   # rules come from YOUR strategies.yaml
        if not isinstance(res, pd.Series):
            res = pd.Series(bool(res), index=index)
        out &= res.fillna(False).astype(bool)
    return out.to_numpy().copy()


def add_htf(df, htf_df):
    """Attach higher-timeframe trend, using ONLY higher-TF candles already closed (no look-ahead)."""
    if htf_df is None or htf_df.empty:
        df["htf_up"] = True
        df["htf_down"] = True
        return df
    hc = htf_df["close"]
    e20 = hc.ewm(span=20, adjust=False, min_periods=20).mean()
    e50 = hc.ewm(span=50, adjust=False, min_periods=50).mean()
    t = pd.DataFrame({"close_time": htf_df["close_time"],
                      "htf_up": (hc > e50) & (e20 > e50),
                      "htf_down": (hc < e50) & (e20 < e50)})
    m = tfm.align_higher(df, t, ["htf_up", "htf_down"])
    df["htf_up"] = m["htf_up"].astype("boolean").fillna(False).astype(bool).to_numpy()
    df["htf_down"] = m["htf_down"].astype("boolean").fillna(False).astype(bool).to_numpy()
    return df


H4_CONTEXT = ["range_low", "range_high", "range_pos", "bull_ob_low", "bull_ob_high", "bear_ob_low", "bear_ob_high",
              "liq_above", "liq_below"]


def add_h4_context(frames):
    """Give every timeframe below 4H the SMC context of the newest CLOSED 4H candle as h4_* columns
    (e.g. h4_bull_ob_low). No 4H data -> the columns are empty (NaN), so rules using them stay false."""
    h4 = None
    if "4h" in frames:
        d4, f4 = frames["4h"]
        h4 = pd.DataFrame({"close_time": d4["close_time"].to_numpy()})
        for col in H4_CONTEXT:
            h4[col] = f4["smc_" + col].to_numpy(dtype=float)
    for tf, (df, feats) in frames.items():
        if TF_MS[tf] >= TF_MS["4h"]:
            continue
        m = tfm.align_higher(df, h4, H4_CONTEXT)
        for col in H4_CONTEXT:
            feats["h4_" + col] = m[col].to_numpy(dtype=float)


def prepare_coin(sym, base, data, quality, tfs, cfg):
    """Everything the strategies of ONE coin need, per trade timeframe: candles (+ higher-timeframe
    trend), features incl. SMC columns (+ h4_* context), the rule namespace, ATR, and the regime of
    every regime timeframe as it was known at each candle. Used by the hourly scan AND the research run.
    Returns dict(frames={tf: dict(df, feats, ns, reg, n)}, smc={tf: detect result}, recs, rg_series)."""
    fe_cfg, smc_cfg = fe.settings(cfg.get("features")), smc.settings(cfg.get("smc"))
    rg_cfg = rg.settings(cfg.get("regime"))
    pairs, smc_out = {}, {}
    for tf in tfs:
        df = data.get((sym, tf))
        if df is None or len(df) < 300 or quality[(base, tf)]["state"] == dq.UNSAFE:
            continue    # never backtest on data we cannot trust
        df = add_htf(df.copy(), data.get((sym, HTF[tf])))
        feats = fe.compute(df, TF_MS[tf], fe_cfg)
        feats.index = df.index
        res = smc.detect(df, feats, data.get((sym, "1d")), data.get((sym, "1w")), TF_MS[tf], smc_cfg)
        smc_out[tf] = res
        for col in smc.EVENT_COLUMNS + smc.CONTEXT_COLUMNS:   # SMC joins the features (rules + evidence)
            feats["smc_" + col] = res["series"][col].to_numpy()
        pairs[tf] = (df, feats)
    add_h4_context(pairs)

    # market regime per timeframe: the report record, and the full history for the gates
    recs, reg_hist, rg_ser = {}, {}, {}
    for rtf in rg_cfg["timeframes"]:
        df_r, q = data.get((sym, rtf)), quality.get((base, rtf))
        if df_r is None or len(df_r) == 0 or (q is not None and q["state"] == dq.UNSAFE):
            recs[rtf] = dict(label="UNCLEAR", expansion_dir=None, confidence="weak", supporting=[],
                             contradicting=["price data UNSAFE or missing"],
                             states=dict(volatility="unknown", momentum="unknown", structure="unknown"),
                             values={})
            continue
        f_r = pairs[rtf][1] if rtf in pairs else fe.compute(df_r, TF_MS[rtf], fe_cfg)
        r_r = rg.compute(df_r, rtf, f_r, rg_cfg)
        recs[rtf] = rg.describe(r_r, -1, rg_cfg)
        rg_ser[(base, rtf)] = (df_r["close_time"].to_numpy(), r_r["label"].to_numpy())
        reg_hist[rtf] = pd.DataFrame({"close_time": df_r["close_time"].to_numpy(),
                                      "label": r_r["label"].to_numpy(dtype=object),
                                      "exp_dir": r_r["expansion_dir"].to_numpy(dtype=object)})
    frames = {}
    for tf, (df, feats) in pairs.items():
        reg = {}                            # regime of every regime timeframe, as known at each candle
        for rtf, hist in reg_hist.items():
            m = tfm.align_higher(df, hist, ["label", "exp_dir"])
            reg[rtf] = (m["label"].to_numpy(dtype=object), m["exp_dir"].to_numpy(dtype=object))
        ns = make_namespace(df, feats)
        df["_atr"] = ns["atr"](14)
        frames[tf] = dict(df=df, feats=feats, ns=ns, reg=reg, n=len(df))
    return dict(frames=frames, smc=smc_out, recs=recs, rg_series=rg_ser)


def strategy_signals(s, tf, fr, cfg, gc=None, detail=None):
    """Entry signals of one strategy on one prepared timeframe, AFTER the warm-up and the market gates
    (allowed regimes + timeframe permission). gc (optional) counts the candles each gate stood down;
    detail (optional dict) receives the raw signals and each gate's verdict (missed-move learning).
    Returns (long, short, exit_long, exit_short, level columns). Raises on a rule error."""
    ns, n, idx = fr["ns"], fr["n"], fr["df"].index
    L = eval_rules(s.get("long"), ns, idx)
    S = eval_rules(s.get("short"), ns, idx) if cfg["signals"]["allow_shorts"] else np.zeros(n, bool)
    XL = eval_rules(s.get("exit_long"), ns, idx) if s.get("exit_long") else None
    XS = eval_rules(s.get("exit_short"), ns, idx) if s.get("exit_short") else None
    cols = {c: level_array(c, ns, n) for c in sspec.columns_needed(s)}
    L[:250] = False     # warm-up: let long indicators settle
    S[:250] = False
    gl, gs, reg_ok, perm_l, perm_s = lc.gate_arrays(s, tf, fr["reg"], n)
    if detail is not None:
        detail.update(raw_l=L.copy(), raw_s=S.copy(), reg_ok=reg_ok, perm_l=perm_l, perm_s=perm_s)
    if gc is not None:
        raw = L | S
        gc["raw"] += int(raw.sum())
        gc["regime"] += int((raw & ~reg_ok).sum())
        gc["permission"] += int(((L & reg_ok & ~perm_l) | (S & reg_ok & ~perm_s)).sum())
    return L & gl, S & gs, XL, XS, cols


def setup_states(s, tf, fr, cfg, coin, stage):
    """WATCH / SETUP_FORMING (section 13) on the newest closed candle - shown in the report, never stored.
    WATCH = the strategy's market gates are open for this direction; SETUP_FORMING = gates open and all
    entry rules but ONE are true (the missing rule is named; needs >= 2 rules). All true = a trigger (a signal)."""
    n, ns, t = fr["n"], fr["ns"], fr["n"] - 1
    gl, gs, _, _, _ = lc.gate_arrays(s, tf, fr["reg"], n)
    out = []
    for d, ok, side in ((1, gl[t], "long"), (-1, gs[t], "short")):
        if not ok or not s.get(side) or (d == -1 and not cfg["signals"]["allow_shorts"]):
            continue
        missing = []
        for rule in s[side]:
            try:
                v = eval(str(rule), {"__builtins__": {}}, ns)     # rules come from YOUR strategies.yaml
            except Exception:
                return []
            v = v.iloc[t] if isinstance(v, pd.Series) else v
            if not (pd.notna(v) and bool(v)):
                missing.append(str(rule))
        if not missing:
            continue
        out.append(dict(coin=coin, tf=tf, strategy=s["id"], version=s["version"], stage=stage,
                        direction="LONG" if d == 1 else "SHORT",
                        state=pos.FORMING if len(missing) == 1 and len(s[side]) >= 2 else pos.WATCH,
                        rules_true=f"{len(s[side]) - len(missing)}/{len(s[side])}",
                        missing=missing[0] if len(missing) == 1 else None))
    return out


def load_research(offline=False):
    """Results of the newest daily research run (reports/research.json), or None."""
    path = os.path.join(REPORTS, "research_offline.json" if offline else "research.json")
    if offline and not os.path.exists(path):
        path = os.path.join(REPORTS, "research.json")
    try:
        return json.load(open(path)) if os.path.exists(path) else None
    except ValueError:
        return None


def board_row(x, tf, status, reg_cell, rc, per_coin, gc, live, now_ms, RC):
    """One scoreboard line: lifecycle status, Layers B/C from research (rc), Layer A from this run."""
    gc = gc or dict(raw=0, regime=0, permission=0, stop=0, target=0)
    la = rs.layer_a([t for tr in per_coin.values() for t in tr], now_ms, RC["layer_a_days"], RC["layer_a_split_day"])
    ev = (rc or {}).get("evidence", {})
    b_all = ev.get("all", {})
    wf = ev.get("walk_forward", {})
    pert = ev.get("perturbation", {})
    return dict(strategy=x["id"], version=x["version"], family=x["family"], gate=x["gate"], tf=tf, status=status,
                status_since=reg_cell.get("since_utc"), researched=rc is not None,
                history_from=(rc or {}).get("history_from"),
                trades=b_all.get("n"), win_rate=b_all.get("win_rate"), avg_r=b_all.get("avg_r"),
                profit_factor=b_all.get("pf"), max_dd_r=b_all.get("max_dd_r"),
                develop_avg_r=ev.get("develop", {}).get("avg_r"), validate_avg_r=ev.get("validate", {}).get("avg_r"),
                long_avg_r=ev.get("long", {}).get("avg_r"), short_avg_r=ev.get("short", {}).get("avg_r"),
                walk_forward=f"{wf['positive']}/{wf['judged']}" if wf else None, walk_forward_passed=wf.get("passed"),
                stress_avg_r=ev.get("stress", {}).get("avg_r"), perturb_stable=pert.get("stable"),
                perturb_worst=(f"{pert['worst']['change']}: {pert['worst']['avg_r']:+.2f}R"
                               if pert.get("worst") else None),
                positive_coins=len(ev.get("positive_coins", [])) if ev else None,
                median_cost_r=ev.get("median_cost_r"), overfit="; ".join(ev.get("overfit", [])) or None,
                required_avg_r=(rc or {}).get("required_avg_r"), beats_twin=(rc or {}).get("beats_twin"),
                layer_a_trades=la["all"]["n"], layer_a_avg_r=la["all"]["avg_r"],
                layer_a_first_avg_r=la["first"]["avg_r"], layer_a_last_avg_r=la["last"]["avg_r"],
                signal_candles=gc["raw"], blocked_by_regime=gc["regime"], blocked_by_permission=gc["permission"],
                skipped_stop=gc["stop"], skipped_target=gc["target"], confirm_5m=bool(x.get("confirm_5m")),
                skipped_5m_expired=gc.get("5m_expired", 0), skipped_5m_invalidated=gc.get("5m_invalidated", 0),
                live_signals=live["n"] if live else 0, live_avg_r=round(live["exp_r"], 3) if live else None,
                twin_of=x.get("twin_of"), control_twin=x.get("control_twin"),
                note=(rc or {}).get("note", ""),
                attribution=_attribution_brief((rc or {}).get("attribution")),
                why_not="; ".join((rc or {}).get("reasons", []) + (rc or {}).get("paper_gate_failed", []))
                if rc else "waiting for the first daily research run (Layers B/C)")


def _attribution_brief(a):
    """The part of a research cell's failure attribution the report shows (full detail: research.json)."""
    if not a:
        return None
    # common among losers AND (for tags winners can have too) clearly more common than among winners
    frequent = sorted(((k, v["loss_share"]) for k, v in a["tags"].items() if v["loss_share"] >= 0.25 and
                       (v["kind"] == "losers only" or v["loss_share"] >= v["win_share"] + 0.05)),
                      key=lambda x: -x[1])
    return dict(losses=a["losses"], wins=a["wins"], systematic=a["systematic"], frequent=frequent[:4],
                mae_mfe=a["mae_mfe"], gross_avg_r=a["gross_avg_r"], avg_r=a["avg_r"],
                strategy_level=a.get("strategy_level", []), diagnosis=a.get("diagnosis", []))


def evidence_for(rc, per_coin, coin):
    """(all coins, this coin) backtest summary behind a signal: Layer B from research when available,
    otherwise this run's shorter backtest."""
    if rc and rc.get("evidence"):
        ev = rc["evidence"]
        conv = lambda x: dict(n=x["n"], exp_r=x["avg_r"], win_rate=x["win_rate"] / 100, pf=x["pf"],
                              avg_bars=x["avg_bars"])
        empty = dict(n=0, avg_r=0.0, win_rate=0.0, pf=0.0, avg_bars=0.0)
        return conv(ev["all"]), conv(ev["by_coin"].get(coin, empty))
    return (stats([t for tr in per_coin.values() for t in tr]), stats(per_coin.get(coin, [])))


def mark_oos(trades, n, cfg):
    """Develop (first 70% of this coin's candles) vs validate / unseen test (last 30%)."""
    split_idx = int(n * cfg["validation"]["in_sample_share"])
    for t in trades:
        t["oos"] = t["entry_idx"] >= split_idx


def mark_oos_for(strat, trades, n, cfg, m5=None):
    """mark_oos(), except for 5m-confirmed strategies: their trades exist only where 5m history exists, so
    develop / validate is the first 70% / last 30% of the 5m PERIOD (by entry time)."""
    if not strat.get("confirm_5m") or m5 is None or not len(m5["open_time"]):
        return mark_oos(trades, n, cfg)
    a, b = int(m5["open_time"][0]), int(m5["close_time"][-1])
    split = a + (b - a) * float(cfg["validation"]["in_sample_share"])
    for t in trades:
        t["oos"] = t["entry_time"] >= split


def regime_at(reg, tf, i):
    """Label of the strategy's regime timeframe at candle i (None if unknown)."""
    lab = reg[lc.regime_tf(tf)][0][i] if lc.regime_tf(tf) in reg else None
    return lab if isinstance(lab, str) else None


def level_array(expr, ns, n):
    """A stop / target level used by a strategy (a column name or an expression), as floats."""
    x = eval(str(expr), {"__builtins__": {}}, ns)   # comes from YOUR strategies.yaml
    if isinstance(x, pd.Series):
        return x.astype(float).to_numpy()
    return np.full(n, float(x))


# =====================================================================
# 3. BACKTEST ENGINE
# =====================================================================
def trade_costs(cfg, d):
    """Costs as fractions for one direction: longs = SPOT costs, shorts = FUTURES costs + funding."""
    c = cfg["costs"]["long" if d == 1 else "short"]
    return dict(taker=c["taker_fee_pct"] / 100, maker=c["maker_fee_pct"] / 100,
                slip=c["slippage_pct"] / 100, funding_8h=c.get("funding_pct_per_8h", 0.0) / 100)


def market_type(d):
    return "spot" if d == 1 else "futures only"


def simulate_trade(o, h, l, c, j0, d, entry, R, cfg, max_hold, bar_hours, exit_arr=None, tps=None, split=None,
                   info=None):
    """Manage one trade from candle j0 (entry candle). Returns dict or None if still open
    (then `info`, if given, receives the targets hit so far and the current stop - the position book).
    tps / split: take-profit prices and the share closed at each (default: config trade plan 1R/2R/3R).
    Conservative: if stop and target are touched in the same candle we assume the STOP hit first.
    Funding (shorts) is charged on the part still open, for every candle held, at entry notional.
    Also measured: MAE / MFE = the worst / best price reached while the trade was open, in R
    (Phase 9 failure attribution), and the funding paid, in R."""
    tp = cfg["trade_plan"]
    k = trade_costs(cfg, d)
    fee_t, fee_m, slip = k["taker"], k["maker"], k["slip"]
    fund_bar = k["funding_8h"] * bar_hours / 8
    if tps is None:
        tps, split = [entry + d * r * R for r in tp["tp_r"]], tp["tp_split"]
    stop = entry - d * R
    remaining, pnl, fees, funding, hit = 1.0, 0.0, fee_t * entry, 0.0, 0
    mae = mfe = 0.0
    n = len(c)

    def done(j, reason):
        return dict(exit_idx=j, r=(pnl - fees) / R, reason=reason, hit=hit, bars=j - j0 + 1,
                    mae_r=mae / R, mfe_r=mfe / R, funding_r=funding / R)
    for j in range(j0, n):
        fees += remaining * fund_bar * entry
        funding += remaining * fund_bar * entry
        worst, best = (l[j], h[j]) if d == 1 else (h[j], l[j])
        mae, mfe = min(mae, d * (worst - entry)), max(mfe, d * (best - entry))
        # --- stop-loss first (worst case) ---
        if (d == 1 and l[j] <= stop) or (d == -1 and h[j] >= stop):
            px = o[j] if ((d == 1 and o[j] < stop) or (d == -1 and o[j] > stop)) else stop
            px *= (1 - slip * d)
            pnl += remaining * d * (px - entry)
            fees += remaining * fee_t * px
            return done(j, "SL" if hit == 0 else f"TP{hit}+stop")
        # --- take-profits ---
        while hit < len(tps) and ((d == 1 and h[j] >= tps[hit]) or (d == -1 and l[j] <= tps[hit])):
            frac = split[hit] if hit < len(tps) - 1 else remaining
            pnl += frac * d * (tps[hit] - entry)
            fees += frac * fee_m * tps[hit]
            remaining -= frac
            hit += 1
            if hit == 1 and tp.get("move_stop_to_breakeven_after_tp1", True):
                stop = entry
            elif hit >= 2 and tp.get("move_stop_to_tp1_after_tp2", True):
                stop = tps[hit - 2]
        if remaining <= 1e-9:
            return done(j, f"TP{hit}")
        if hit > 0 and ((d == 1 and c[j] <= stop) or (d == -1 and c[j] >= stop)):
            px = stop * (1 - slip * d)       # came back through the moved stop in the same candle
            pnl += remaining * d * (px - entry)
            fees += remaining * fee_t * px
            return done(j, f"TP{hit}+stop")
        # --- early exit rule / time stop (at candle close) ---
        rule_exit = exit_arr is not None and exit_arr[j]
        if rule_exit or (j - j0 + 1) >= max_hold:
            px = c[j] * (1 - slip * d)
            pnl += remaining * d * (px - entry)
            fees += remaining * fee_t * px
            return done(j, "exit-rule" if rule_exit else "time")
    if info is not None:
        info.update(hit=hit, stop=stop, mae_r=mae / R, mfe_r=mfe / R, bars=n - j0)
    return None


def plan_trade(strat, t, d, entry, atr_t, cols, cfg, skipped=None):
    """Stop distance R, take-profit prices and split for a trade planned at the close of candle t,
    using only values known then (cols = level columns the strategy's stop / targets read).
    None = no valid trade; the reason is counted in `skipped` (stop / target)."""
    def skip(why):
        if skipped is not None:
            skipped[why] = skipped.get(why, 0) + 1
        return None
    if not np.isfinite(atr_t) or atr_t <= 0:
        return skip("stop")
    st = strat["stop"]
    if st["method"] == "atr":
        R = st["atr"] * atr_t
    else:
        lev = cols[st["long_level" if d == 1 else "short_level"]][t]
        if not np.isfinite(lev):
            return skip("stop")
        R = d * (entry - (lev - d * st.get("buffer_atr", 0.2) * atr_t))
        if R <= 0 or R > st.get("max_width_atr", 3.0) * atr_t:   # stop on the wrong side or too wide
            return skip("stop")
    tg = sspec.targets(strat, d, entry, R, t, cols, cfg["trade_plan"])
    return skip("target") if tg is None else (R, tg[0], tg[1])


def backtest(df, sig_long, sig_short, ex_long, ex_short, strat, cfg, tf, cols=None, skipped=None):
    o, h, l, c = (df[k].to_numpy() for k in ("open", "high", "low", "close"))
    ot = df["open_time"].to_numpy()
    atr = df["_atr"].to_numpy()
    bar_hours = TF_MS[tf] / 3_600_000
    n, t, trades = len(c), 0, []
    while t < n - 1:
        d = 1 if sig_long[t] else (-1 if sig_short[t] else 0)
        if d == 0:
            t += 1
            continue
        entry = o[t + 1] * (1 + trade_costs(cfg, d)["slip"] * d)   # enter at NEXT candle open
        plan = plan_trade(strat, t, d, entry, atr[t], cols or {}, cfg, skipped)
        if plan is None:
            t += 1
            continue
        R, tps, split = plan
        res = simulate_trade(o, h, l, c, t + 1, d, entry, R, cfg, strat["time_stop_bars"], bar_hours,
                             ex_long if d == 1 else ex_short, tps, split)
        if res is None:
            break
        k = trade_costs(cfg, d)
        res.update(entry_idx=t + 1, signal_idx=t, dir=d, entry_time=int(ot[t + 1]), entry=float(entry), R=float(R),
                   tp1=float(tps[0]), tps=[float(x) for x in tps], cost_r=float(entry * 2 * (k["taker"] + k["slip"]) / R))   # round trip, in R
        trades.append(res)
        t = res["exit_idx"] + int(strat.get("cooldown_bars", 0))    # wait before the next trade
    return trades


def backtest_5m(df, sig_long, sig_short, ex_long, ex_short, strat, cfg, tf, cols, m5, confirm=True, skipped=None,
                S5=None):
    """Backtest of a strategy whose card says confirm_5m (section 8): each closed 15m / 30m trigger waits
    for the 5-minute protocol (engine/confirm5m.py); CONFIRMED -> enter at the close of the confirming
    5m bar, EXPIRED / INVALIDATED -> no trade. The stop and target PRICES stay where the trigger put them.
    The trade is then managed on 5m bars (time stop = the same clock time as on the trigger timeframe).
    confirm=False gives the SAME strategy without the 5m check, entered at the next open and managed on
    the same 5m bars over the same period: the fair control twin for "does the 5m check help?".
    Trigger candles before the first 5m bar are skipped (no 5m history there)."""
    if m5 is None or not len(m5["close"]):
        return []
    o, c = df["open"].to_numpy(), df["close"].to_numpy()
    ot, ct = df["open_time"].to_numpy(), df["close_time"].to_numpy()
    atr = df["_atr"].to_numpy()
    o5, h5, l5, cl5 = m5["open"], m5["high"], m5["low"], m5["close"]
    ot5 = m5["open_time"]
    n, n5 = len(c), len(cl5)
    max_hold = int(strat["time_stop_bars"] * TF_MS[tf] // TF_MS["5m"])
    ex5 = {1: c5m.exit_on_5m(ct, ex_long, m5["close_time"]), -1: c5m.exit_on_5m(ct, ex_short, m5["close_time"])}
    count = skipped if skipped is not None else {}
    t, trades = 0, []
    while t < n - 1:
        d = 1 if sig_long[t] else (-1 if sig_short[t] else 0)
        if d == 0 or ct[t] + 1 < ot5[0]:
            t += 1
            continue
        k = trade_costs(cfg, d)
        j0 = c5m.first_bar(m5, int(ct[t]) + 1)
        if j0 >= n5:
            break
        entry0 = o5[j0] * (1 + k["slip"] * d)                  # the plain entry: next open, as in backtest()
        plan = plan_trade(strat, t, d, entry0, atr[t], cols or {}, cfg, skipped)
        if plan is None:
            t += 1
            continue
        R0, tps, split = plan
        stop = entry0 - d * R0
        info5 = dict(bars=0, smc=[])
        if confirm:
            chk = c5m.check(m5, int(ct[t]) + 1, d, entry0, stop, S5)
            if chk["state"] == c5m.AWAITING:                   # the data ends inside the 6-bar window
                break
            if chk["state"] != c5m.CONFIRMED:
                count["5m_" + chk["state"].lower()] = count.get("5m_" + chk["state"].lower(), 0) + 1
                t += 1
                continue
            js = chk["idx"] + 1
            entry = cl5[chk["idx"]] * (1 + k["slip"] * d)
            info5 = dict(bars=chk["bars"], smc=chk["smc"])
        else:
            js, entry = j0, entry0
        R = d * (entry - stop)
        if R <= 0 or d * (tps[0] - entry) <= 0:
            count["stop"] = count.get("stop", 0) + 1
            t += 1
            continue
        if js >= n5:
            break
        res = simulate_trade(o5, h5, l5, cl5, js, d, entry, R, cfg, max_hold, TF_MS["5m"] / 3_600_000,
                             ex5[d], tps, split)
        if res is None:
            break
        entry_idx = int(np.searchsorted(ot, ot5[js], side="right") - 1)       # trigger candle holding the 5m bar
        exit_idx = int(np.searchsorted(ot, ot5[res["exit_idx"]], side="right") - 1)
        entry_idx = max(entry_idx, t + 1)
        res.update(exit_idx=exit_idx, entry_idx=entry_idx, bars=max(1, exit_idx - entry_idx + 1), signal_idx=t, dir=d, entry_time=int(ot5[js]),
                   entry=float(entry), R=float(R), tp1=float(tps[0]), tps=[float(x) for x in tps],
                   cost_r=float(entry * 2 * (k["taker"] + k["slip"]) / R),
                   confirm_bars=info5["bars"], smc_5m=info5["smc"])
        trades.append(res)
        t = max(t + 1, exit_idx + int(strat.get("cooldown_bars", 0)))
    return trades


def m5_arrays(frames):
    """The 5-minute protocol's input for one coin (None when there is no trustworthy 5m data)."""
    fr = frames.get("5m")
    return c5m.arrays(fr["df"], fr["feats"]) if fr else None


def run_backtest(df, L, S, XL, XS, strat, cfg, tf, cols=None, skipped=None, m5=None, S5=None):
    """backtest() - or backtest_5m() for a card with confirm_5m (it needs the coin's 5m arrays)."""
    if strat.get("confirm_5m"):
        return backtest_5m(df, L, S, XL, XS, strat, cfg, tf, cols, m5, True, skipped, S5)
    return backtest(df, L, S, XL, XS, strat, cfg, tf, cols, skipped)


stats = rs.stats          # summary of trades (engine/research.py), in time order


# =====================================================================
# 4. FORWARD TEST (did past signals really work?)
# =====================================================================
LOG_COLS = ["id", "signal_time_utc", "coin", "tf", "strategy", "direction", "entry", "stop",
            "tp1", "tp2", "tp3", "max_hold_bars", "status", "result_r", "closed_time_utc",
            "version", "stage", "tp_split",
            "conditions", "regime_at_entry", "session", "mae_r", "mfe_r", "tags",      # Phase 9 attribution
            "state", "state_note", "planned_entry", "entry_time_utc", "sim_tf", "bars_5m",  # Phase 10 states
            "confirm_5m_utc", "smc_5m", "close_reason", "current_stop", "warnings", "next_action",
            "risk_blocks"]                                                                  # Phase 11 risk engine
TEXT_COLS = ["closed_time_utc", "version", "stage", "tp_split", "conditions", "regime_at_entry", "session", "tags",
             "state", "state_note", "entry_time_utc", "sim_tf", "confirm_5m_utc", "smc_5m", "close_reason",
             "warnings", "next_action", "risk_blocks"]
EVENT_COLS = ["time_utc", "id", "coin", "tf", "strategy", "version", "stage", "from_state", "to_state", "price", "note"]


def log_path(offline, name="signals_log.csv"):
    """Offline test runs keep their own copy (signals_log_offline.csv ...), never the real record."""
    root, ext = os.path.splitext(name)
    return os.path.join(REPORTS, f"{root}_offline{ext}" if offline else name)


def load_log(path=None):
    p = path or os.path.join(REPORTS, "signals_log.csv")
    if os.path.exists(p):
        df = pd.read_csv(p, dtype={c: str for c in TEXT_COLS})
        for col in LOG_COLS:
            if col not in df:
                df[col] = np.nan
        df = df[LOG_COLS]
    else:
        df = pd.DataFrame(columns=LOG_COLS)
    for c in TEXT_COLS:                   # an all-empty column is read as numbers; text must fit in it
        df[c] = df[c].astype(object)
    return df


def ts_ms(txt):
    return int(pd.Timestamp(txt).value // 1_000_000)


def fmt_ms(ms):
    return pd.to_datetime(int(ms), unit="ms").strftime("%Y-%m-%d %H:%M")


def _event(events, now_txt, row, old, new, price=None, note=""):
    if old is not None or new is not None:
        pos.check_move(old, new)
    events.append(dict(time_utc=now_txt, id=row["id"], coin=row["coin"], tf=row["tf"], strategy=row["strategy"],
                       version=str(row["version"]) if pd.notna(row["version"]) else "1.0", stage=row["stage"],
                       from_state=old or "", to_state=new, price=price, note=note))


def resolve_pending(logdf, m5_by_coin, cfg, events, now_txt, only=None):
    """AWAITING_5M rows: run the 5-minute protocol (section 8) on the closed 5m bars since the trigger.
    CONFIRMED -> ENTRY_TRIGGERED -> POSITION_ACTIVE at the confirming bar's close (stop and target prices
    stay); EXPIRED / INVALIDATED -> no trade (result stays empty); still < 6 bars -> look again next run.
    m5_by_coin: {coin: confirm5m.arrays()} of this run (a coin without trustworthy 5m data waits)."""
    S5 = c5m.settings(cfg.get("confirm_5m"))
    for i, row in logdf.iterrows():
        if pos.row_state(row) != pos.AWAITING or (only is not None and row["id"] not in only):
            continue
        m5 = m5_by_coin.get(row["coin"])
        if m5 is None:
            continue
        d = 1 if row["direction"] == "LONG" else -1
        planned = float(row["planned_entry"]) if pd.notna(row["planned_entry"]) else float(row["entry"])
        stop = float(row["stop"])
        after = ts_ms(row["signal_time_utc"]) + 60_000     # the trigger candle closed at the END of that minute
        if m5["open_time"][0] > after:          # the 5m candles right after the trigger are no longer downloaded
            chk = dict(state=c5m.EXPIRED, idx=None, bars=0, smc=[],
                       why="the 5m candles after the trigger are no longer available - not decided, no entry")
        else:
            chk = c5m.check(m5, after, d, planned, stop, S5)
        logdf.at[i, "bars_5m"] = chk["bars"]
        if chk["state"] == c5m.AWAITING:
            logdf.at[i, "state_note"] = chk["why"]
            continue
        when = fmt_ms(m5["close_time"][chk["idx"]] if chk["idx"] is not None
                      else m5["close_time"][min(max(c5m.first_bar(m5, after) + chk["bars"] - 1, 0),
                                                len(m5["close_time"]) - 1)])
        if chk["state"] == c5m.CONFIRMED:
            entry = float(m5["close"][chk["idx"]]) * (1 + trade_costs(cfg, d)["slip"] * d)
            if d * (entry - stop) <= 0 or d * (float(row["tp1"]) - entry) <= 0:     # as backtest_5m: no trade
                chk = dict(chk, state=c5m.INVALIDATED, why="confirmed price already beyond the stop or TP1")
            else:
                logdf.at[i, "entry"], logdf.at[i, "entry_time_utc"] = entry, when
                logdf.at[i, "confirm_5m_utc"], logdf.at[i, "smc_5m"] = when, ";".join(chk["smc"])
                logdf.at[i, "state"], logdf.at[i, "current_stop"] = pos.ACTIVE, stop
                logdf.at[i, "state_note"] = f"5m bar {chk['bars']}/{S5['bars']} confirmed"
                logdf.at[i, "next_action"] = pos.next_action(pos.ACTIVE, [])
                _event(events, now_txt, row, pos.AWAITING, pos.TRIGGERED, entry, logdf.at[i, "state_note"]
                       + (f" ({', '.join(chk['smc'])})" if chk["smc"] else ""))
                _event(events, now_txt, row, pos.TRIGGERED, pos.ACTIVE, entry, f"entry at {when} UTC")
                continue
        state = pos.EXPIRED if chk["state"] == c5m.EXPIRED else pos.INVALIDATED
        logdf.at[i, "state"], logdf.at[i, "status"], logdf.at[i, "close_reason"] = state, state, state
        logdf.at[i, "closed_time_utc"], logdf.at[i, "state_note"] = when, chk["why"]
        logdf.at[i, "next_action"] = "none - no entry"
        _event(events, now_txt, row, pos.AWAITING, state, None, chk["why"])
    return logdf


def update_forward(logdf, data, quality, feed, cfg, cards=None, rg_series=None, exits=None, mon=None,
                   events=None, now_txt="", only=None):
    """Replay candles after each OPEN position (POSITION_ACTIVE / TP1_HIT) using exactly the backtest's
    rules: stop, targets, breakeven after TP1, time stop and the strategy's exit rule (exits =
    {(coin, tf, 'id@version'): (close times, exit_long, exit_short)} of this run). Positions of 5m-confirmed
    strategies are managed on 5m bars, like in backtest_5m(). Signals whose candles are UNSAFE stay open
    until the data is trustworthy again. A position that closes gets MAE / MFE and its section 17 tags;
    one that stays open gets its state, current stop, section 16 warnings (mon) and next action.
    Returns (log, rows closed in this run)."""
    closed_now = []
    events = events if events is not None else []
    for i, row in logdf[logdf["status"] == "OPEN"].iterrows():
        state = pos.row_state(row)
        if state not in (pos.ACTIVE, pos.TP1_HIT) or (only is not None and row["id"] not in only):
            continue
        coin, tf = row["coin"], row["tf"]
        sym = coin + cfg["market"]["quote"]
        stf = row["sim_tf"] if isinstance(row["sim_tf"], str) and row["sim_tf"] else tf
        df = data.get((sym, stf))
        rep = quality.get((coin, stf))
        if df is None:
            try:
                df, rep = fetch_checked(feed, sym, stf, 1000, cfg.get("data_quality"))
            except Exception:
                continue
        if rep is None or rep["state"] == dq.UNSAFE:
            continue
        start = row["entry_time_utc"] if isinstance(row["entry_time_utc"], str) and row["entry_time_utc"] \
            else row["signal_time_utc"]
        pos0 = int(np.searchsorted(df["open_time"].to_numpy(), ts_ms(start), side="right"))   # first candle after entry
        after = df.iloc[pos0:].reset_index(drop=True)
        if after.empty:
            continue
        d = 1 if row["direction"] == "LONG" else -1
        entry, stop = float(row["entry"]), float(row["stop"])
        R = abs(entry - stop)
        tps = [float(row[k]) for k in ("tp1", "tp2", "tp3") if pd.notna(row[k]) and str(row[k]) != ""]
        split = ([float(x) for x in str(row["tp_split"]).split("/")] if pd.notna(row["tp_split"])
                 and str(row["tp_split"]) else list(cfg["trade_plan"]["tp_split"]))
        if len(split) != len(tps):
            tps, split = None, None                     # old rows: the config trade plan
        ver = str(row["version"]) if pd.notna(row["version"]) else "1.0"
        ex = (exits or {}).get((coin, tf, f"{row['strategy']}@{ver}"))
        exit_arr = c5m.exit_on_5m(ex[0], ex[1 if d == 1 else 2], after["close_time"].to_numpy()) if ex else None
        o, h, l, c = (after[k].to_numpy() for k in ("open", "high", "low", "close"))
        info = {}
        res = simulate_trade(o, h, l, c, 0, d, entry, R, cfg, int(row["max_hold_bars"]) * (TF_MS[tf] // TF_MS[stf]),
                             TF_MS[stf] / 3_600_000, exit_arr, tps, split, info)
        if not res:
            new = pos.TP1_HIT if info.get("hit", 0) >= 1 else pos.ACTIVE
            m = (mon or {}).get((coin, tf))
            warn = pos.warnings(d, ts_ms(start), m["ct"], m["flags"], m["atr"], m["reg_now"],
                                row["regime_at_entry"] if isinstance(row["regime_at_entry"], str) else None) if m else []
            logdf.at[i, "state"], logdf.at[i, "current_stop"] = new, info.get("stop", stop)
            logdf.at[i, "warnings"], logdf.at[i, "next_action"] = ";".join(warn), pos.next_action(new, warn)
            if new != state:
                _event(events, now_txt, row, state, new, info.get("stop"), "TP1 reached - stop moved to breakeven")
            continue
        if res["hit"] >= 1 and state == pos.ACTIVE:
            _event(events, now_txt, row, pos.ACTIVE, pos.TP1_HIT, None, "TP1 reached - stop moved to breakeven")
        logdf.at[i, "status"] = res["reason"]
        logdf.at[i, "result_r"] = round(res["r"], 3)
        logdf.at[i, "closed_time_utc"] = fmt_ms(after["close_time"].iloc[res["exit_idx"]])
        logdf.at[i, "mae_r"], logdf.at[i, "mfe_r"] = round(res["mae_r"], 3), round(res["mfe_r"], 3)
        logdf.at[i, "state"], logdf.at[i, "close_reason"] = pos.CLOSED, pos.close_reason(res["reason"])
        logdf.at[i, "warnings"], logdf.at[i, "next_action"] = "", "none - closed"
        _event(events, now_txt, row, pos.TP1_HIT if res["hit"] >= 1 else state, pos.CLOSED, None,
               f"{logdf.at[i, 'close_reason']} {res['r']:+.2f}R")
        strat = (cards or {}).get(f"{row['strategy']}@{ver}")
        tdf, tpos0, tres = df, pos0, res
        if stf != tf:                         # tags are read on the trigger timeframe
            tdf = data.get((sym, tf))
            if tdf is not None:
                tot = tdf["open_time"].to_numpy()
                tpos0 = int(np.searchsorted(tot, ts_ms(start), side="right"))
                tex = int(np.searchsorted(tot, int(after["open_time"].iloc[res["exit_idx"]]), side="right") - 1)
                tres = dict(res, exit_idx=max(tex - tpos0, 0))
        if strat is not None and tdf is not None and tpos0 >= 1:
            try:
                tags = live_outcome_tags(tdf, tpos0, tres, d, entry, R, tps[0] if tps else entry + d * R,
                                         coin, tf, strat, cfg, rg_series or {})
                logdf.at[i, "tags"] = ";".join(tags)
            except Exception as e:           # attribution must never stop the forward test
                log(f"attribution failed for {row['id']}: {e}")
        closed_now.append(i)
    return logdf, closed_now


class EmailContext:
    """Builds the section 20 email content during the scan (notify.py only sends it): [ENTRY] cards with a
    chart for APPROVED signals, [EXIT] cards for APPROVED TP1 / closes, the daily block, [SYSTEM] reminders."""

    def __init__(self, cfg, now, data, regimes, feat_last, coin_state, board, logdf, risk_pct, RK, acct, tf_ms, lb):
        self.cfg, self.now, self.data, self.regimes, self.feat_last = cfg, now, data, regimes, feat_last
        self.coin_state, self.logdf, self.risk_pct, self.RK, self.acct = coin_state, logdf, risk_pct, RK, acct
        self.board = {(b["strategy"], str(b["version"]), b["tf"]): b for b in board}
        self.quote, self.tf_ms, self.lb = cfg["market"]["quote"], tf_ms, lb
        self.utc, self.bj = now.strftime("%Y-%m-%d %H:%M"), now.astimezone(BJ).strftime("%Y-%m-%d %H:%M")

    def regime_row(self, coin):
        out = {tf: r["label"] for tf, r in (self.regimes.get(coin, {}).get("timeframes") or {}).items()}
        for tf in ("30m", "15m", "5m"):
            f = self.feat_last.get((coin, tf))
            if f is not None and len(f) and f["structure"].iloc[-1] in ("up", "down"):
                out[tf] = f"structure {f['structure'].iloc[-1]}"
        return out

    def evidence(self, strategy, version, tf):
        return briefs.evidence(self.board.get((strategy, str(version), tf)),
                               briefs.record(self.logdf, strategy, version, tf, ["PAPER_TRADING", "VALIDATION"]),
                               briefs.record(self.logdf, strategy, version, tf, ["APPROVED"]))

    def chart(self, name, coin, tf, title, entry, stop, targets, entry_ms=None, exit_ms=None, exit_price=None,
              current_stop=None):
        df = self.data.get((coin + self.quote, tf))
        if df is None or df.empty:
            return None
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name)
        try:
            return os.path.relpath(charts.trade_chart(df, os.path.join(REPORTS, "charts", safe + ".png"), title, entry,
                                                      stop, targets, entry_ms, exit_ms, exit_price, current_stop), ROOT)
        except Exception as e:                  # a chart must never stop an email
            log(f"chart failed for {name}: {e}")
            return None

    def _card(self, **kw):
        e = dict(quote=self.quote, utc=self.utc, beijing=self.bj, regimes=self.regime_row(kw["coin"]),
                 data_state=self.coin_state.get(kw["coin"], "?"),
                 evidence=self.evidence(kw["strategy"], kw["version"], kw["tf"]))
        e.update(kw)
        e.update(briefs.entry_email(e))
        return e

    def entry_from_plan(self, p):
        exp = (self.now + dt.timedelta(milliseconds=self.tf_ms[p["timeframe"]])).strftime("%Y-%m-%d %H:%M")
        e = self._card(coin=p["coin"], direction=p["direction"], market=p["market"], tf=p["timeframe"],
                       strategy=p["strategy"], version=p["version"], stage=p["stage"], entry=p["entry"],
                       entry_zone=p["entry_zone"], stop=p["stop"], targets=p["targets"], confirm_5m=None,
                       size=dict(qty=p["position_qty"], usdt=p["position_usdt"], risk_usdt=p["risk_usdt"],
                                 risk_pct=p["risk_pct"], capped=p["size_capped"]),
                       expires=f"{exp} UTC - after that, or once price leaves the entry zone, skip it",
                       why=briefs.why_points(1 if p["direction"] == "LONG" else -1, p["context"], p["facts"],
                                             p["session"], p["conditions"]),
                       invalidation=briefs.invalidation(p))
        e["chart"] = self.chart(f"entry_{p['coin']}_{p['timeframe']}_{p['strategy']}_{p['signal_time_utc']}", p["coin"],
                                p["timeframe"], e["subject"][8:], p["entry"], p["stop"],
                                [t["price"] for t in p["targets"]], p["signal_ms"])
        return e

    def _row(self, rid):
        m = self.logdf[self.logdf["id"] == rid]
        return None if m.empty else m.iloc[-1]

    def from_events(self, events):
        """APPROVED state changes worth an email (operator decision): the 5m-confirmed entry, TP1, the close."""
        out = []
        for ev in events:
            if ev["stage"] != "APPROVED" or ev["to_state"] not in (pos.ACTIVE, pos.TP1_HIT, pos.CLOSED):
                continue
            r = self._row(ev["id"])
            if r is None:
                continue
            d = 1 if r["direction"] == "LONG" else -1
            tps = [float(r[k]) for k in ("tp1", "tp2", "tp3") if pd.notna(r[k]) and str(r[k]) != ""]
            stf = r["sim_tf"] if isinstance(r["sim_tf"], str) and r["sim_tf"] else r["tf"]
            entry, stop = float(r["entry"]), float(r["stop"])
            if ev["to_state"] == pos.ACTIVE:
                if stf != "5m" or ev["from_state"] != pos.TRIGGERED:
                    continue                     # plain entries are emailed from the plan (signals)
                R = abs(entry - stop)
                split = [float(x) for x in str(r["tp_split"]).split("/")] if pd.notna(r["tp_split"]) else []
                z = rk.size(self.acct, self.risk_pct, entry, stop, self.RK["max_leverage"])
                e = self._card(coin=r["coin"], direction=r["direction"], market=market_type(d), tf=r["tf"],
                               strategy=r["strategy"], version=str(r["version"]), stage="APPROVED", entry=entry,
                               entry_zone=[entry - 0.2 * R, entry + 0.2 * R], stop=stop,
                               targets=[dict(price=t, r=abs(t - entry) / R, close_pct=round(x * 100))
                                        for t, x in zip(tps, split or [1.0] * len(tps))],
                               confirm_5m=r["confirm_5m_utc"], smc_5m=r["smc_5m"] if isinstance(r["smc_5m"], str) else "",
                               size=dict(qty=z["qty"], usdt=z["notional"], risk_usdt=z["risk_usdt"],
                                         risk_pct=self.risk_pct, capped=z["capped"]),
                               expires="entered at the close of the confirming 5m bar",
                               why=[f"{r['tf']} setup of {r['strategy']} confirmed by a closed 5m bar",
                                    f"Regime at the trigger: {r['regime_at_entry'] or '?'}",
                                    "Conditions at the trigger: " + (str(r["conditions"]).replace(";", ", ")
                                                                     if isinstance(r["conditions"], str) and r["conditions"]
                                                                     else "none flagged")],
                               invalidation=briefs.invalidation(dict(stop=stop, exit_rule=None, confirm_5m=False,
                                                                     max_hold=tf_to_text(r["tf"], int(r["max_hold_bars"])))))
                e["chart"] = self.chart(f"entry_{ev['id']}", r["coin"], "5m", e["subject"][8:], entry, stop, tps,
                                        ts_ms(r["entry_time_utc"]))
                out.append(dict(key=f"{ev['id']}|ENTRY", kind="ENTRY", **{k: e[k] for k in ("subject", "lines", "chart")}))
                continue
            closed = ev["to_state"] == pos.CLOSED
            x = dict(coin=r["coin"], quote=self.quote, direction=r["direction"], tf=r["tf"], strategy=r["strategy"],
                     version=str(r["version"]), stage="APPROVED", kind=ev["to_state"], utc=self.utc, beijing=self.bj,
                     close_reason=r["close_reason"] if closed else None,
                     result_r=float(r["result_r"]) if closed and pd.notna(r["result_r"]) else 0.0, entry=entry,
                     next_action=("none - the trade is closed" if closed else
                                  f"stop moved to breakeven ({briefs.fmt(entry)}); keep the rest open for the next target"))
            m = briefs.exit_email(x)
            start = r["entry_time_utc"] if isinstance(r["entry_time_utc"], str) and r["entry_time_utc"] else r["signal_time_utc"]
            m["chart"] = self.chart(f"exit_{ev['id']}_{ev['to_state']}", r["coin"], stf, m["subject"][7:], entry, stop,
                                    tps, ts_ms(start),
                                    ts_ms(r["closed_time_utc"]) - self.tf_ms[stf] + 60_000 if closed else None,
                                    None, float(r["current_stop"]) if pd.notna(r["current_stop"]) else None)
            out.append(dict(key=f"{ev['id']}|{ev['to_state']}", kind="EXIT", **m))
        return out

    def daily(self, coins, snap, watching, plans, book, btc, fg, data_state, changes, research_utc, risk_out,
              n_signals=0):
        """The block the 08:00 Beijing daily email is made from (notify.py daily)."""
        rank = {pos.FORMING: 1, pos.WATCH: 2}
        rows = []
        for c in coins:
            sn = snap.get(c, {})
            rg = self.regime_row(c)
            f30 = self.feat_last.get((c, "30m"))
            roc = float(f30["roc"].iloc[-1]) if f30 is not None and len(f30) and pd.notna(f30["roc"].iloc[-1]) else None
            st15 = "SIGNAL" if any(p["coin"] == c and p["timeframe"] == "15m" for p in plans) else min(
                (w["state"] for w in watching if w["coin"] == c and w["tf"] == "15m"), key=lambda x: rank[x],
                default="-")
            aw = [a for a in book["awaiting"] if a["coin"] == c]
            rows.append(dict(coin=c, price=sn.get("price", float("nan")), vol_24h_m=(sn.get("vol_24h") or 0) / 1e6,
                             regimes=[rg.get(tf, "?") for tf in ("1w", "1d", "4h", "1h")],
                             mom_30m="?" if roc is None else f"{roc:+.1f}% ROC",
                             setup_15m=st15, trigger_5m=f"AWAITING {aw[0]['bars']}/6" if aw else "-"))
        fresh = bool(research_utc) and (self.now - pd.Timestamp(research_utc, tz="UTC").to_pydatetime()
                                        <= dt.timedelta(hours=24))
        health = [f"{c['key']} {c['tf']}: {c['old']} -> {c['new']}" for c in (changes if fresh else [])]
        health += [f"SUSPENDED {k}" for k in risk_out["suspended"]] + risk_out["halts_text"]
        return dict(date=self.now.strftime("%Y-%m-%d"), utc=self.utc, beijing=self.bj, btc=btc, fear_greed=fg,
                    data_state=data_state, matrix=rows, health=health, signals=n_signals,
                    events=[f"{e['name']} {e['start_utc']} UTC" for e in risk_out["upcoming_events"]],
                    calendar_warning=risk_out["calendar_warning"])

    def reminders(self, board, scan_minutes):
        """[SYSTEM] reminders sent once each (notify.py system): an APPROVED strategy while scans are hourly."""
        appr = sorted({f"{b['strategy']}@{b['version']}|{b['tf']}" for b in board if b["status"] == "APPROVED"})
        if appr and scan_minutes > 15:
            return [dict(key="approved_while_hourly", subject="[SYSTEM] A strategy is APPROVED - scans are still hourly",
                         lines=[f"APPROVED: {', '.join(appr)}.",
                                f"The scan runs every {scan_minutes} minutes, so a live entry or exit alert can "
                                "arrive up to that late (AGENT_PROMPT.md section 19 asks for every 15 minutes).",
                                "Ask Claude to switch the scan to every 15 minutes (a one-line change)."])]
        return []


def not_actionable(new_rows, logdf):
    """Ids of signals logged in THIS run whose trade already moved past the entry here (TP1, closed, expired,
    invalidated, no trade): found up to an hour late, they are not worth an [ENTRY] or [EXIT] email."""
    done = set(logdf.loc[~logdf["state"].isin([pos.ACTIVE, pos.AWAITING]), "id"])
    return {r["id"] for r in new_rows} & done


def apply_risk(plans, book):
    """Run every plan through the risk engine, best score first: an APPROVED plan that fails a step becomes
    NO_TRADE, one that passes takes its place in the book (the next plans see it); PAPER / VALIDATION plans are
    only marked with the steps that WOULD block them live (they never take a place)."""
    for p in sorted(plans, key=lambda p: -p["confidence_score"]):
        p["risk_blocks"] = book.check(p, p.get("cooldown_ms", 0))
        p["no_trade"] = p["stage"] == "APPROVED" and bool(p["risk_blocks"])
        if p["stage"] == "APPROVED" and not p["no_trade"]:
            book.accept(p)
    return plans


def risk_summary(logdf, now, RK, groups, pct, pct_note, calendar_problem, plans, state_path):
    """Section 15 state after this run: day / week R, halts, suspended strategies, correlation groups, the event
    calendar, and what changed since the previous run (transitions -> one [SYSTEM] email each, notify.py)."""
    b = rk.Book(logdf, now, RK, groups)
    now_ms = int(now.timestamp() * 1000)
    halts, suspended = b.halts(), b.suspended()
    nxt = rk.upcoming(RK["events"], now_ms, RK["calendar_horizon_days"])
    active = rk.blackout(now_ms, RK["events"], RK["blackout_minutes"])
    warn = (f"event calendar has an error: {calendar_problem}" if calendar_problem else
            f"calendar not maintained - no event listed for the next {RK['calendar_horizon_days']} days "
            "(events.yaml)" if not nxt else None)
    prev = {}
    if os.path.exists(state_path):
        try:
            with open(state_path) as f:
                prev = json.load(f)
        except ValueError:
            prev = {}
    transitions = []
    for h in halts:
        if h not in prev.get("halts", []):
            transitions.append(dict(kind="start", what=h, text=rk.STEPS[h]))
    for h in prev.get("halts", []):
        if h not in halts:
            transitions.append(dict(kind="end", what=h, text=rk.STEPS[h].split(" - ")[0] + " - lifted"))
    for k in suspended:
        if k not in prev.get("suspended", []):
            transitions.append(dict(kind="start", what=k, text=f"{k} SUSPENDED: live drawdown {b.dd[k]:.1f}R "
                                    f"> {RK['strategy_max_dd_r']:g}R. Resume only by adding it to config.yaml -> "
                                    "risk -> resume with today's date"))
    for k in prev.get("suspended", []):
        if k not in suspended:
            transitions.append(dict(kind="end", what=k, text=f"{k} resumed (config.yaml -> risk -> resume)"))
    with open(state_path, "w") as f:
        json.dump(dict(updated_utc=now.strftime("%Y-%m-%d %H:%M"), halts=halts, suspended=suspended), f, indent=1)
    fmt_e = [dict(start_utc=fmt_ms(e[0]), end_utc=fmt_ms(e[1]), type=e[2], name=e[3]) for e in nxt]
    return dict(day_r=b.day_r, week_r=b.week_r, halts=halts, halts_text=[rk.STEPS[h] for h in halts],
                suspended=suspended, drawdowns=b.dd, risk_pct=pct, risk_note=pct_note,
                groups=sorted(set(v for v in groups.values() if "+" in v)),
                blackout_now=[e[3] for e in active], upcoming_events=fmt_e,
                next_event=(f"{fmt_e[0]['name']} {fmt_e[0]['start_utc']} UTC" if fmt_e else None),
                calendar_warning=warn, transitions=transitions,
                no_trade=[dict(coin=p["coin"], tf=p["timeframe"], strategy=p["strategy"], direction=p["direction"],
                               steps=[rk.STEPS[x] for x in p["risk_blocks"]]) for p in plans if p.get("no_trade")],
                limits=dict(day_r=RK["day_limit_r"], week_r=RK["week_limit_r"], positions=RK["max_positions"],
                            per_coin=RK["max_per_coin"], strategy_dd_r=RK["strategy_max_dd_r"],
                            blackout_minutes=RK["blackout_minutes"], min_tp1_r=RK["min_tp1_r"],
                            max_leverage=RK["max_leverage"], corr_threshold=RK["corr_threshold"]))


def write_events(events, offline):
    """Append-only record of every state change (section 13): reports/position_events.csv."""
    if not events:
        return
    p = log_path(offline, "position_events.csv")
    pd.DataFrame(events, columns=EVENT_COLS).to_csv(p, mode="a", header=not os.path.exists(p), index=False)


def live_outcome_tags(df, pos0, res, d, entry, R, tp1, coin, tf, strat, cfg, rg_series):
    """Section 17 tags of a closed paper / live signal - the same rules as for backtest trades."""
    A = att.settings(cfg.get("attribution"))
    feats = fe.compute(df, TF_MS[tf], fe.settings(cfg.get("features")))
    feats.index = df.index
    reg = {}
    for rtf in lc.PERMISSION_TFS + ["1w"]:
        ser = rg_series.get((coin, rtf))
        if ser is not None:
            hist = pd.DataFrame({"close_time": ser[0], "label": ser[1], "exp_dir": [None] * len(ser[0])})
            m = tfm.align_higher(df, hist, ["label", "exp_dir"])
            reg[rtf] = (m["label"].to_numpy(dtype=object), m["exp_dir"].to_numpy(dtype=object))
    ctx = att.context(df, feats, reg, TF_MS[tf])
    k = trade_costs(cfg, d)
    tr = dict(res, dir=d, signal_idx=pos0 - 1, entry_idx=pos0, exit_idx=pos0 + res["exit_idx"], entry=entry, R=R,
              tp1=tp1, cost_r=entry * 2 * (k["taker"] + k["slip"]) / R)
    return att.outcome_tags(ctx, tr, dict(strat, _A=A), lc.regime_tf(tf))


def forward_stats(logdf):
    """Live results per (strategy, version, timeframe). Rows from before spec v3 count as version 1.0."""
    closed = logdf[logdf["status"] != "OPEN"].dropna(subset=["result_r"]).copy()
    closed["version"] = closed["version"].fillna("1.0").astype(str)
    out = {}
    for (s, v, tf), g in closed.groupby(["strategy", "version", "tf"]):
        r = g["result_r"].astype(float)
        out[(s, v, tf)] = dict(n=len(r), win_rate=float((r > 0).mean()), exp_r=float(r.mean()))
    return out


# =====================================================================
# 5. HELPERS
# =====================================================================
def repo_slug():
    return os.environ.get("GITHUB_REPOSITORY", "mayastraglobal-ui/crypto-signal-agent")


def storage_info(offline):
    """Repository size (GitHub's own number, updated with some delay) and the size of this run's large
    files, which go to branch live-reports (replaced every run) instead of main's history."""
    live = {os.path.basename(p): os.path.getsize(os.path.join(ROOT, p)) for p in publish_live.LIVE_FILES
            if os.path.exists(os.path.join(ROOT, p))}
    repo_kb = None
    if not offline:
        try:
            headers = {"Accept": "application/vnd.github+json"}
            if os.environ.get("GITHUB_TOKEN"):
                headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
            r = requests.get(f"https://api.github.com/repos/{repo_slug()}", headers=headers, timeout=10)
            r.raise_for_status()
            repo_kb = int(r.json()["size"])
        except Exception as e:
            log(f"repository size not available: {e}")
    return dict(repo_size_mb=None if repo_kb is None else round(repo_kb / 1024, 1),
                live_files_kb={k: round(v / 1024) for k, v in live.items()},
                live_total_mb=round(sum(live.values()) / 1024 / 1024, 2), live_branch=publish_live.BRANCH)


def fmt_price(x):
    if x == 0 or not np.isfinite(x):
        return "0"
    digits = max(2, 5 - int(math.floor(math.log10(abs(x)))) - 1)
    return f"{x:,.{min(digits, 8)}f}"


def tf_to_text(tf, bars):
    mins = TF_MS[tf] / 60000 * bars
    return f"{mins/60:.1f} h" if mins >= 120 else f"{mins:.0f} min"


# =====================================================================
# 6. MAIN
# =====================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="use synthetic data (code test)")
    ap.add_argument("--coins", type=int, default=None,
                    help="override the number of research coins (test runs)")
    ap.add_argument("--fault", choices=["stale_btc", "bad_prices"], default=None,
                    help="offline only: plant a data problem to test the safety checks")
    ap.add_argument("--scenario", default=None,
                    help="offline only: JSON file with per-coin volumes / moves / depth (tests)")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
    os.makedirs(REPORTS, exist_ok=True)
    started = dt.datetime.now(dt.timezone.utc)

    # ---------- strategy ID cards (spec v3) + the registry of tested versions ----------
    strategies, spec_problems, idle = sspec.load(
        yaml.safe_load(open(os.path.join(ROOT, "strategies.yaml"))), rg.LABELS, TF_ORDER)
    reg_path = os.path.join(REPORTS, "strategy_registry_offline.csv") if args.offline else REGISTRY
    reg_src = reg_path if os.path.exists(reg_path) else REGISTRY      # offline starts from the real one
    registry = (lc.registry_from_frame(pd.read_csv(reg_src, dtype={"version": str}))
                if os.path.exists(reg_src) else lc.empty_registry())
    fps = {sspec.key(x): sspec.fingerprint(x) for x in strategies}
    for x in list(strategies):
        msg = lc.immutable_problem(registry, x, fps[sspec.key(x)])
        if msg:
            spec_problems.setdefault(x["id"], []).append(msg)
            strategies.remove(x)
    for sid, errs in spec_problems.items():
        log(f"STRATEGY NOT RUN {sid}: {'; '.join(errs)}")

    # ---------- data source ----------
    if (args.fault or args.scenario) and not args.offline:
        sys.exit("--fault and --scenario only work together with --offline")
    scenario = json.load(open(args.scenario)) if args.scenario else None
    feeds = [Synthetic(fault=args.fault, scenario=scenario)] if args.offline else [Binance(), OKX()]
    feed, tickers = None, None
    for f in feeds:
        try:
            tickers = f.tickers()
            feed = f
            break
        except Exception as e:
            log(f"{f.name} unavailable: {e}")
    if feed is None:
        sys.exit("No market data source reachable.")   # workflow emails "[SYSTEM] scan FAILED"

    # ---------- second exchange, for the cross-venue price check ----------
    dq_cfg = dq.settings(cfg.get("data_quality"))
    second, second_name = None, None
    for f in feeds:
        if f is feed:
            continue
        try:
            second = {t["symbol"]: t["last"] for t in f.tickers()}
            second_name = f.name
            break
        except Exception as e:
            log(f"cross-venue check: {f.name} unavailable ({e})")

    # ---------- universe: which coins may we look at? (AGENT_PROMPT.md section 4) ----------
    U = uni.settings(cfg.get("universe"))
    if args.coins:
        U["research_coins"] = args.coins
        U["signal_coins"] = min(U["signal_coins"], args.coins)
    mkt = cfg["market"]
    always = set(mkt.get("always_include", []))
    state_path = os.path.join(REPORTS, "universe_state_offline.json" if args.offline
                              else "universe_state.json")
    ustate = json.load(open(state_path)) if os.path.exists(state_path) else uni.empty_state()
    prev_members = list(ustate["members"])
    cands, name_excluded = uni.prefilter(tickers, mkt, U)
    pool = uni.candidate_pool(cands, always | set(prev_members), U["candidate_pool"])
    log(f"Data source: {feed.name}; {len(cands)} coins over the volume floor, checking {len(pool)}")
    ustate, suspended = uni.update_suspensions(
        ustate, {c["base"]: c["change_pct"] for c in pool}, U, started.strftime("%Y-%m-%d"))

    daily_data, measures, elig, quality, failed = {}, {}, {}, {}, []
    for u in pool:
        sym, base = u["symbol"], u["base"]
        try:
            daily, rep = fetch_checked(feed, sym, "1d", int(cfg["timeframes"].get("1d", 1000)), dq_cfg)
        except Exception as e:
            log(f"skip {sym}: {e}")
            failed.append(base)
            continue
        try:
            depth = feed.depth(sym)
        except Exception as e:
            log(f"order book {sym} not available: {e}")
            depth = None
        book = (u["bid"], u["ask"]) if u.get("bid") and u.get("ask") else None
        measures[base] = uni.measure(u, daily, book, depth, U)
        elig[base] = uni.eligibility(measures[base], U, mkt["min_listing_days"], rep["state"],
                                     base in suspended)
        daily_data[base] = daily
        quality[(base, "1d")] = rep
    vol = {c["base"]: c["quote_volume"] for c in pool}
    ranked = uni.rank(sorted((b for b, r in elig.items() if r["ok"]), key=lambda b: -vol[b]), always)
    not_elig = {b: r["reasons"] for b, r in elig.items() if not r["ok"]}
    for b in prev_members:
        if b not in elig:
            not_elig[b] = [name_excluded.get(b) or ("download failed" if b in failed else
                           f"24h volume below {uni.usd(U['min_24h_volume_usdt'])} or no longer listed")]
    ustate, u_events = uni.eligibility_changes(ustate, elig)
    ustate, m_events, view = uni.update_membership(ustate, ranked, U, always, not_elig)
    u_events += m_events
    log(f"Signal coins: {', '.join(view['signal'])} | research only: {', '.join(view['research_only'])}")

    # ---------- download every timeframe for the research coins ----------
    data, coins, xtf = {}, [], {}
    by_base = {c["base"]: c for c in pool}
    tfs = [tf for tf in TF_ORDER if tf in cfg["timeframes"]]
    for base in view["research"]:
        u = by_base[base]
        sym = u["symbol"]
        try:
            got = {tf: fetch_checked(feed, sym, tf, int(cfg["timeframes"][tf]), dq_cfg)
                   for tf in ["1w"] + tfs}
        except Exception as e:
            log(f"skip {sym}: {e}")
            failed.append(base)
            continue
        data[(sym, "1d")] = daily_data[base]
        data[(sym, "7d")] = tfm.rolling_7d(daily_data[base])     # built from checked daily candles
        for tf, (df_tf, rep) in got.items():
            data[(sym, tf)] = df_tf
            quality[(base, tf)] = rep
        xtf[base] = None if args.offline else cross_timeframe_check(data, sym, base, quality)
        for tf in CONTEXT + tfs:
            rep = quality[(base, tf)]
            if rep["state"] != dq.GOOD:
                log(f"data {rep['state']}: {sym} {tf}: {'; '.join(rep['problems'])}")
        coins.append(u)
        log(f"loaded {sym}")

    # ---------- judge data quality: per coin, then the whole system ----------
    cross = dq.cross_venue({c["base"]: c["last"] for c in coins},
                           None if second is None else
                           {c["base"]: second.get(c["symbol"]) for c in coins},
                           dq_cfg["cross_venue_max_pct"])
    coin_state = {c["base"]: dq.worst(cross[c["base"]]["state"],
                                     *(quality[(c["base"], tf)]["state"] for tf in CONTEXT + tfs))
                  for c in coins}
    watched = always | set(prev_members) | set(view["research"])
    for b in watched:     # coins we should be watching but could not trust
        if b not in coin_state and (b, "1d") in quality and quality[(b, "1d")]["state"] == dq.UNSAFE:
            coin_state[b] = dq.UNSAFE
    sys_state, sys_reason = dq.system_state(coin_state, "BTC", [b for b in failed if b in watched],
                                            dq_cfg["system_unsafe_coin_share"])
    log(f"Data quality: system {sys_state} - {sys_reason}")

    # a signal coin whose data turned UNSAFE on any timeframe leaves the list at once
    unsafe_members = {b: "price data UNSAFE: " + "; ".join(
                          f"{tf} {p}" for tf in CONTEXT + tfs for p in quality.get((b, tf), {}).get("problems", []))
                      for b in view["signal"] if coin_state.get(b) == dq.UNSAFE}
    if unsafe_members:
        ustate, ev = uni.remove_members(ustate, unsafe_members)
        u_events += ev
        view["signal"] = [b for b in view["signal"] if b not in unsafe_members]
    signal_set = set(view["signal"])

    def signals_allowed(base, tf):
        """Only GOOD data may produce signals: the signal timeframe, its higher timeframe,
        the cross-exchange price check, and the whole system."""
        if base not in signal_set:              # research-only coins never give signals
            return False
        if sys_state == dq.UNSAFE or cross[base]["state"] != dq.GOOD:
            return False
        for t in (tf, HTF.get(tf)):
            r = quality.get((base, t))
            if t and (r is None or r["state"] != dq.GOOD):
                return False
        return True

    # ---------- per coin: features, SMC, regimes, market gates, backtests ----------
    per = {}       # (id, version, tf) -> {coin: trades}
    gate_counts = {}                        # (id, version, tf) -> signal candles blocked by each gate
    rule_errors = {}                        # id@version -> problems while evaluating its rules
    live = []      # candidate signals
    snap = {}      # coin snapshot for report
    fe_cfg = fe.settings(cfg.get("features"))
    feat_last = {}                          # (coin, tf) -> features of the newest closed candles
    smc_cfg = smc.settings(cfg.get("smc"))
    smc_res = {}                            # (coin, tf) -> SMC events, flags and state
    ev_frames = {tf: [] for tf in tfs}      # candle evidence input, per timeframe
    rg_cfg = rg.settings(cfg.get("regime"))
    regimes = {}
    rg_series = {}                          # (coin, tf) -> (close_time array, label array) for stamping
    lb = int(cfg["signals"]["lookback_bars"])
    scan_ms = int(cfg["signals"].get("scan_interval_minutes", 60)) * 60_000
    att_cfg = att.settings(cfg.get("attribution"))
    S5 = c5m.settings(cfg.get("confirm_5m"))
    m5_by_coin = {}                         # coin -> 5m arrays (5-minute protocol, section 8)
    exits = {}                              # (coin, tf, id@version) -> exit rules, for open positions
    mon = {}                                # (coin, tf) -> what the section 16 warnings read
    watching = []                           # WATCH / SETUP_FORMING (report only)
    dash_candles = {}                       # coin -> tf -> newest candles, for the dashboard charts (Phase 16)
    for u in coins:
        sym, base = u["symbol"], u["base"]
        pc = prepare_coin(sym, base, data, quality, tfs, cfg)
        m5 = m5_arrays(pc["frames"])
        if m5 is not None:
            m5_by_coin[base] = m5
        rg_series.update(pc["rg_series"])
        verdict_now, reason = rg.permission(pc["recs"])
        regimes[base] = dict(timeframes=pc["recs"], permission=verdict_now, permission_reason=reason)
        for tf, fr in pc["frames"].items():
            df, feats, ns, reg, n = fr["df"], fr["feats"], fr["ns"], fr["reg"], fr["n"]
            ctx = None                      # attribution context, built only when a signal needs it
            smc_res[(base, tf)] = pc["smc"][tf]
            feat_last[(base, tf)] = feats[[c for c in feats.columns if not c.startswith("h4_")]].tail(3)
            ev_frames[tf].append((base, df, feats))
            if base in signal_set:
                k = df.tail(DASH_BARS)
                dash_candles.setdefault(base, {})[tf] = [
                    [int(a), float(b), float(c), float(d), float(e)] for a, b, c, d, e in
                    zip(k["open_time"], k["open"], k["high"], k["low"], k["close"])]
                tail = slice(max(0, n - 500), n)
                mon[(base, tf)] = dict(ct=df["close_time"].to_numpy()[tail], atr=df["_atr"].to_numpy()[tail],
                                       reg_now=regime_at(reg, tf, n - 1),
                                       flags={k: np.nan_to_num(feats[c].to_numpy()[tail].astype(float)).astype(bool)
                                              for k, c in (("bos_up", "smc_bos_up"), ("bos_down", "smc_bos_down"),
                                                           ("choch_up", "smc_choch_up"),
                                                           ("choch_down", "smc_choch_down"),
                                                           ("disp_up", "displacement_up"),
                                                           ("disp_down", "displacement_down"))})
            if tf == "1h":
                snap[base] = dict(price=float(df["close"].iloc[-1]),
                                  atr_pct=float(df["_atr"].iloc[-1] / df["close"].iloc[-1] * 100),
                                  rsi_1h=float(ns["rsi"](ns["close"], 14).iloc[-1]),
                                  change_24h=u["change_pct"], vol_24h=u["quote_volume"])
            for s in strategies:
                if tf not in s["timeframes"]:
                    continue
                k3 = (s["id"], s["version"], tf)
                gc = gate_counts.setdefault(k3, dict(raw=0, regime=0, permission=0, stop=0, target=0))
                try:
                    L, S, XL, XS, cols = strategy_signals(s, tf, fr, cfg, gc)
                except Exception as e:
                    log(f"RULE ERROR in {s['id']} {tf}: {e}")
                    rule_errors.setdefault(sspec.key(s), set()).add(f"{tf}: {e}")
                    continue
                tr = run_backtest(df, L, S, XL, XS, s, cfg, tf, cols, gc, m5, S5)
                mark_oos_for(s, tr, n, cfg, m5)
                per.setdefault(k3, {})[base] = tr
                if base in signal_set and (XL is not None or XS is not None):
                    exits[(base, tf, sspec.key(s))] = (df["close_time"].to_numpy(), XL, XS)
                tracked = registry["cells"].get(f"{sspec.key(s)}|{tf}", {}).get("status")
                if base in signal_set and tracked in ("VALIDATION", "PAPER_TRADING", "APPROVED"):
                    watching += setup_states(s, tf, fr, cfg, base, tracked)
                # ---- fresh signals on the last closed candles (all candles since the previous hourly run) ----
                for k in range(min(n - 1, max(lb, -(-scan_ms // TF_MS[tf])))):
                    t_i = n - 1 - k
                    d = 1 if L[t_i] else (-1 if S[t_i] else 0)
                    if d == 0:
                        continue
                    a = df["_atr"].iloc[t_i]
                    entry = float(df["close"].iloc[-1]) if k == 0 else float(df["open"].iloc[t_i + 1])
                    plan = plan_trade(s, t_i, d, entry, a, cols, cfg)
                    if plan is None:
                        continue
                    R, tps, split = plan
                    if ctx is None:
                        ctx = att.context(df, feats, reg, TF_MS[tf])
                    if k > 0 and not s.get("confirm_5m"):
                        # older signal: still valid only if no SL/TP1 hit and price near entry
                        # (5m-confirmed strategies: the 5-minute protocol replays those bars instead)
                        seg = df.iloc[t_i + 1:]
                        if (d == 1 and (seg["low"].min() <= entry - R or seg["high"].max() >= tps[0])) or \
                           (d == -1 and (seg["high"].max() >= entry + R or seg["low"].min() <= tps[0])):
                            continue
                        if abs(df["close"].iloc[-1] - entry) > 0.3 * R:
                            continue
                    live.append(dict(coin=base, symbol=sym, tf=tf, strategy=s["id"], version=s["version"], dir=d,
                                     entry=entry, R=float(R), tps=[float(x) for x in tps], split=split,
                                     atr=float(a), age_bars=k, confirm_5m=bool(s.get("confirm_5m")),
                                     signal_time=int(df["close_time"].iloc[t_i]),
                                     htf_up=bool(df["htf_up"].iloc[t_i]),
                                     htf_down=bool(df["htf_down"].iloc[t_i]),
                                     regime=regime_at(reg, tf, t_i),
                                     conditions=att.conditions(ctx, t_i, d, s, att_cfg),
                                     facts=briefs.facts_at(feats, t_i, d),
                                     levels=[float(feats[c].iloc[t_i]) for c in
                                             (("smc_liq_above", "resistance") if d == 1 else
                                              ("smc_liq_below", "support")) if c in feats],   # section 14 step 10
                                     session=ctx["kz"][t_i] or ("outside killzones" if ctx["intraday"] else "n/a"),
                                     rsi=float(ns["rsi"](ns["close"], 14).iloc[t_i]),
                                     vol_ratio=float(df["volume"].iloc[t_i] / ns["vol_sma"](20).iloc[t_i])))
                    break
        del pc

    # ---------- candle evidence: patterns vs random entries (research evidence, not a signal) ----------
    ev_cfg = evid.settings(cfg.get("evidence"))
    costs_by_dir = {1: trade_costs(cfg, 1), -1: trade_costs(cfg, -1)}
    ev_patterns = dict(evid.PATTERNS, **SMC_PATTERNS)
    evidence = {tf: evid.study(ev_frames[tf], costs_by_dir, TF_MS[tf] / 3_600_000, ev_cfg, seed_key=tf,
                               patterns=ev_patterns)
                for tf in tfs if ev_frames[tf]}
    del ev_frames

    # ---------- forward test (live proof) + state machine (sections 8, 13, 16) ----------
    cards = {sspec.key(x): x for x in strategies}
    now_txt = started.strftime("%Y-%m-%d %H:%M")
    events = []                              # every state change of this run -> reports/position_events.csv
    logdf = resolve_pending(load_log(log_path(args.offline)), m5_by_coin, cfg, events, now_txt)
    logdf, closed_now = update_forward(logdf, data, quality, feed, cfg, cards, rg_series, exits, mon, events, now_txt)
    fwd = forward_stats(logdf)

    # ---------- scoreboard: status + Layers B/C from the daily research run, Layer A from this run ----------
    V, RC = cfg["validation"], cfg["research"]
    research = load_research(args.offline)
    cells = research.get("cells", {}) if research else {}
    now_ms = int(started.timestamp() * 1000)
    by_key = {sspec.key(x): x for x in strategies}
    board, verdict = [], {}
    for x in strategies:
        for tf in [t for t in tfs if t in x["timeframes"]]:
            k3, ck = (x["id"], x["version"], tf), f"{x['id']}@{x['version']}|{tf}"
            status = registry["cells"].get(ck, {}).get("status") or "FORMALIZED"
            verdict[k3] = status
            board.append(board_row(x, tf, status, registry["cells"].get(ck, {}), cells.get(ck),
                                   per.get(k3, {}), gate_counts.get(k3), fwd.get(k3), now_ms, RC))
    rows = {(b["strategy"], b["tf"]): b for b in board}
    for b in board:                         # control-twin numbers next to each SMC strategy
        tw = rows.get((b["control_twin"], b["tf"])) if b["control_twin"] else None
        b["twin_avg_r"] = tw["avg_r"] if tw else None
        b["twin_validate_avg_r"] = tw["validate_avg_r"] if tw else None
        if b["confirm_5m"]:                 # -5M: its twin is measured over the same 5m period (research run)
            sw = (cells.get(f"{b['strategy']}@{b['version']}|{b['tf']}") or {}).get("twin_same_window")
            b["twin_avg_r"] = sw["all"]["avg_r"] if sw else None
            b["twin_validate_avg_r"] = sw["validate"]["avg_r"] if sw else None
    order = {st: i for i, st in enumerate(["APPROVED", "PAPER_TRADING", "VALIDATION", "BACKTESTING", "FORMALIZED",
                                           "FAILED", "RETIRED"])}
    board.sort(key=lambda b: (order.get(b["status"], 9), -(b["avg_r"] if b["avg_r"] is not None else -9)))

    # ---------- market mood ----------
    btc = {}
    for tf in ("1d", "4h"):
        d = data.get(("BTC" + cfg["market"]["quote"], tf))
        if d is not None and len(d) > 200:
            c = d["close"]
            e50, e200 = c.ewm(span=50, adjust=False).mean().iloc[-1], c.ewm(span=200, adjust=False).mean().iloc[-1]
            btc[tf] = "UP" if c.iloc[-1] > e50 > e200 else "DOWN" if c.iloc[-1] < e50 < e200 else "SIDEWAYS"
    fg = fear_greed(args.offline)

    # ---------- risk engine settings (section 15; engine/risk.py) ----------
    calendar_problem = None
    try:
        RK = rk.settings(cfg.get("risk"), (cfg.get("events") or [])
                         + rk.load_calendar(os.path.join(ROOT, rk.CALENDAR_FILE)))
    except ValueError as e:                  # a broken calendar entry is reported, never silently skipped
        calendar_problem = str(e)
        RK = rk.settings(cfg.get("risk"), [])
    quote = cfg["market"]["quote"]
    closes_1h = {b: data[(b + quote, "1h")].set_index("close_time")["close"]
                 for b in view["signal"] if data.get((b + quote, "1h")) is not None}
    groups = rk.corr_groups(closes_1h, RK["corr_threshold"], RK["corr_bars"])
    risk_pct, risk_note = rk.risk_pct(cfg["account"]["risk_per_trade_pct"], logdf, started, RK)

    # ---------- build trade plans ----------
    tp = cfg["trade_plan"]
    acct = cfg["account"]["size_usdt"]
    plans, blocked = [], []
    for sgl in live:
        key = (sgl["strategy"], sgl["version"], sgl["tf"])
        stage = verdict.get(key)
        if stage not in ("VALIDATION", "PAPER_TRADING", "APPROVED"):   # only versions that passed the backtest gate
            continue
        if sgl["coin"] not in signal_set:      # research-only coin: backtest only, never a signal
            continue
        if not signals_allowed(sgl["coin"], sgl["tf"]):
            blocked.append(f"{sgl['coin']} {sgl['tf']} {sgl['strategy']}")
            continue
        pooled, cst = evidence_for(cells.get(f"{key[0]}@{key[1]}|{key[2]}"), per.get(key, {}), sgl["coin"])
        if cst["n"] < V["min_coin_trades"]:
            continue
        shrunk = (cst["n"] * cst["exp_r"] + 20 * pooled["exp_r"]) / (cst["n"] + 20)
        if shrunk <= V["min_expectancy_r"] or cst["exp_r"] <= 0:
            continue
        d, e, R = sgl["dir"], sgl["entry"], sgl["R"]
        tps, split = sgl["tps"], sgl["split"]
        against_btc = (d == 1 and btc.get("4h") == "DOWN") or (d == -1 and btc.get("4h") == "UP")
        sz = rk.size(acct, risk_pct, e, e - d * R, RK["max_leverage"])
        strat = by_key[f"{sgl['strategy']}@{sgl['version']}"]
        plans.append(dict(
            coin=sgl["coin"], pair=sgl["symbol"], timeframe=sgl["tf"], strategy=sgl["strategy"],
            version=sgl["version"], stage=stage, family=strat["family"], confirm_5m=sgl["confirm_5m"],
            state=pos.AWAITING if sgl["confirm_5m"] else pos.ACTIVE,
            conditions=sgl["conditions"], session=sgl["session"],
            direction="LONG" if d == 1 else "SHORT", market=market_type(d),
            signal_time_utc=pd.to_datetime(sgl["signal_time"], unit="ms").strftime("%Y-%m-%d %H:%M"),
            signal_age_candles=sgl["age_bars"],
            entry=e, entry_zone=[e - 0.2 * R, e + 0.2 * R], stop=e - d * R,
            targets=[dict(price=px, r=round(abs(px - e) / R, 2), close_pct=round(x * 100)) for px, x in zip(tps, split)],
            tp1=tps[0], tp2=tps[1] if len(tps) > 1 else None, tp3=tps[2] if len(tps) > 2 else None,
            tp_split=split, risk_pct_of_price=R / e * 100,
            expected_hold=tf_to_text(sgl["tf"], cst["avg_bars"] or pooled["avg_bars"]),
            max_hold=tf_to_text(sgl["tf"], strat["time_stop_bars"]), max_hold_bars=strat["time_stop_bars"],
            position_qty=sz["qty"], position_usdt=sz["notional"], leverage_needed=sz["leverage"],
            risk_usdt=sz["risk_usdt"], size_capped=sz["capped"], risk_pct=risk_pct,
            signal_ms=int(sgl["signal_time"]), levels=sgl["levels"], facts=sgl["facts"],
            cooldown_ms=int(strat.get("cooldown_bars", 0)) * TF_MS[sgl["tf"]],
            backtest_coin=dict(trades=cst["n"], win_rate=cst["win_rate"], avg_r=cst["exp_r"]),
            backtest_all=dict(trades=pooled["n"], win_rate=pooled["win_rate"], avg_r=pooled["exp_r"],
                              pf=pooled["pf"]),
            confidence_score=round(shrunk + (0 if not against_btc else -0.05), 3),
            why=strat.get("logic", "").strip(), rules_met=strat["long" if d == 1 else "short"],
            exit_rule=strat.get("exit_long" if d == 1 else "exit_short"),
            context=dict(htf_trend="UP" if sgl["htf_up"] else "DOWN" if sgl["htf_down"] else "SIDEWAYS",
                         regime=sgl["regime"], permission=regimes.get(sgl["coin"], {}).get("permission"),
                         rsi14=round(sgl["rsi"], 1), volume_vs_avg=round(sgl["vol_ratio"], 2),
                         btc_4h=btc.get("4h"), against_btc_trend=against_btc)))
    # combine agreement / conflicts per coin (APPROVED and VALIDATION kept apart)
    by = {}
    for p in plans:
        by.setdefault((p["stage"], p["coin"]), []).append(p)
    final = []
    for (_, coin), ps in by.items():
        dirs = {p["direction"] for p in ps}
        for p in ps:
            p["agreeing_signals"] = sum(q["direction"] == p["direction"] for q in ps)
            p["conflict"] = len(dirs) > 1
            p["confidence_score"] += 0.03 * (p["agreeing_signals"] - 1) - (0.1 if p["conflict"] else 0)
        final.append(max(ps, key=lambda p: p["confidence_score"]))
    final.sort(key=lambda p: -p["confidence_score"])
    # risk engine (section 14 steps 9-13, section 15): APPROVED plans that fail a step become NO_TRADE; every
    # plan (paper too) records which steps would block it (risk_blocks), so each rule's value can be measured
    apply_risk(plans, rk.Book(logdf, started, RK, groups))
    # emailed: APPROVED entries. An APPROVED 5m-confirmed setup waits for its 5m bar first (AWAITING_5M,
    # in the position book); emails on its later state changes arrive with Phase 12.
    emailable = [p for p in final if p["stage"] == "APPROVED" and not p["confirm_5m"] and not p["no_trade"]]
    watch = [p for p in final if p not in emailable and not p["no_trade"]][: cfg["signals"]["max_in_report"]]
    final = emailable[: cfg["signals"]["max_in_report"]]

    # ---------- log new signals and move them through their states ----------
    # EVERY plan is logged (not only the best one per coin shown above): each strategy's paper record must
    # hold all of its signals. PAPER / VALIDATION signals are logged but never emailed.
    existing = set(logdf["id"].astype(str))
    new_rows = []
    for p in plans:
        sid = f"{p['coin']}-{p['timeframe']}-{p['strategy']}-{p['signal_time_utc']}"
        if sid in existing:
            continue
        existing.add(sid)
        row = dict(id=sid, signal_time_utc=p["signal_time_utc"], coin=p["coin"],
                   tf=p["timeframe"], strategy=p["strategy"], direction=p["direction"],
                   entry=p["entry"], stop=p["stop"], tp1=p["tp1"], tp2=p["tp2"],
                   tp3=p["tp3"], max_hold_bars=p["max_hold_bars"], status="OPEN",
                   result_r=np.nan, closed_time_utc="", version=p["version"], stage=p["stage"],
                   tp_split="/".join(f"{x:g}" for x in p["tp_split"]),
                   conditions=";".join(p["conditions"]), regime_at_entry=p["context"]["regime"] or "",
                   session=p["session"] or "", state=p["state"], planned_entry=p["entry"],
                   risk_blocks=";".join(p["risk_blocks"]),
                   entry_time_utc="" if p["confirm_5m"] else p["signal_time_utc"],
                   sim_tf="5m" if p["confirm_5m"] else p["timeframe"], bars_5m=0 if p["confirm_5m"] else np.nan,
                   current_stop=p["stop"],
                   state_note="waiting for a 5m confirmation" if p["confirm_5m"] else "entry at the signal candle close",
                   next_action="wait for the 5m bar" if p["confirm_5m"] else pos.next_action(pos.ACTIVE, []))
        if p["no_trade"]:
            why = "; ".join(rk.STEPS[x] for x in p["risk_blocks"])
            row.update(state=pos.NO_TRADE, status=pos.NO_TRADE, close_reason=pos.NO_TRADE, closed_time_utc=now_txt,
                       state_note=why, next_action="none - risk engine said no", entry_time_utc="")
            _event(events, now_txt, row, None, pos.NO_TRADE, p["entry"], why)
        elif p["confirm_5m"]:
            _event(events, now_txt, row, None, pos.AWAITING, p["entry"], f"{p['timeframe']} trigger closed")
        else:
            _event(events, now_txt, row, None, pos.TRIGGERED, p["entry"], f"{p['timeframe']} signal candle closed")
            _event(events, now_txt, row, pos.TRIGGERED, pos.ACTIVE, p["entry"], "")
        new_rows.append(row)
    if new_rows:
        logdf = pd.concat([logdf, pd.DataFrame(new_rows, columns=LOG_COLS)], ignore_index=True)
        for c in TEXT_COLS:
            logdf[c] = logdf[c].astype(object)
        new_ids = {r["id"] for r in new_rows}           # an older trigger may already be decided by now
        logdf = resolve_pending(logdf, m5_by_coin, cfg, events, now_txt, only=new_ids)
        logdf, more = update_forward(logdf, data, quality, feed, cfg, cards, rg_series, exits, mon, events, now_txt,
                                     only=new_ids)
        closed_now += more
    logdf.to_csv(log_path(args.offline), index=False)
    write_events(events, args.offline)
    if not args.offline:
        mem.ensure(MEMORY)                 # every section 22 knowledge file exists, with its header
        write_failure_journal(logdf.loc[[i for i in closed_now if float(logdf.at[i, "result_r"]) < 0]], started,
                              mem.review_days(cfg.get("memory"), "failure_journal"))
    quote = cfg["market"]["quote"]
    prices = {(sym[: -len(quote)], tf): float(d["close"].iloc[-1]) for (sym, tf), d in data.items()
              if d is not None and len(d) and sym.endswith(quote)}
    risk_out = risk_summary(logdf, started, RK, groups, risk_pct, risk_note, calendar_problem, plans,
                            log_path(args.offline, "risk_state.json"))
    book = pos.build(logdf, started, prices, dict(day_r=RK["day_limit_r"], week_r=RK["week_limit_r"],
                                                  heat=RK["max_positions"]))
    book_text = pos.lines(book, S5["bars"], risk_out)
    watching.sort(key=lambda x: (x["state"] != pos.FORMING, x["coin"], x["tf"]))
    json.dump(dict(generated_utc=now_txt, book=book, text=book_text, risk=risk_out, watching=watching,
                   events_this_run=events),
              open(log_path(args.offline, "positions.json"), "w"), indent=1, default=float)
    with open(os.path.join(REPORTS, "dashboard_data.json"), "w") as f:       # large-ish: branch live-reports only
        json.dump(dict(generated_utc=now_txt, tf_ms={t: TF_MS[t] for t in tfs}, candles=dash_candles), f)

    # ---------- memory (section 22): execution notes when data problems start / end, weekly coin facts ----------
    if not args.offline:
        md = cfg.get("memory")
        iss, fees = execution_issues(quality, cross, failed, cfg)
        write_execution_notes(iss, fees, started, os.path.join(REPORTS, "execution_state.json"),
                              mem.review_days(md, "execution_notes"))
        write_coin_notes(view["signal"], lambda: {
            c: coin_facts(c, data.get((c + quote, "1d")), rg_series.get((c, "1d")), groups.get(c, c),
                          snap.get(c, {}).get("vol_24h"), cells, V["min_coin_trades"], started)
            for c in view["signal"]}, started, os.path.join(REPORTS, "coin_notes_state.json"),
            mem.review_days(md, "coin_notes"))
    memory_out = mem.status(MEMORY, started)

    # ---------- emails (section 20): entry / exit cards, charts, the daily block ----------
    mail = EmailContext(cfg, started, data, regimes, feat_last, coin_state, board, logdf, risk_pct, RK, acct,
                        TF_MS, lb)
    # a signal found up to an hour late whose trade already ENDED in this same run is not actionable:
    # neither an [ENTRY] nor an [EXIT] email (it stays in the log and the report)
    over = not_actionable(new_rows, logdf)
    final = [p for p in final if f"{p['coin']}-{p['timeframe']}-{p['strategy']}-{p['signal_time_utc']}" not in over]
    for p in final:                                   # APPROVED entries at the signal candle
        p["email"] = mail.entry_from_plan(p)
    email_events = [e for e in mail.from_events(events)          # APPROVED: 5m-confirmed entries, TP1, closes
                    if e["key"].split("|")[0] not in over]
    daily = mail.daily(view["signal"], snap, watching, plans, book, btc, fg, sys_state,
                       (research or {}).get("changes", []), (research or {}).get("run_utc"), risk_out, len(final))
    daily["claude_review"] = claude_review(started)          # Phase 14: yesterday's Claude daily review, if any
    weekly = (digest.weekly(started, logdf, board, research, read_text(os.path.join(MEMORY, "strategy_lifecycle.md")),
                            *claude_weekly(started)) if digest.is_weekly_time(started) else None)

    # ---------- data-quality report ----------
    dq_out = dict(
        checked_utc=started.strftime("%Y-%m-%d %H:%M"), system_state=sys_state, reason=sys_reason,
        status_code="DATA_STALE / SIGNAL_DISABLED" if sys_state == dq.UNSAFE else "SIGNALS_ALLOWED",
        data_source=feed.name, second_exchange=second_name, failed_downloads=failed,
        blocked_signals=blocked,
        coins={c["base"]: dict(state=coin_state[c["base"]], cross_venue=cross[c["base"]],
                               timeframes={tf: quality[(c["base"], tf)] for tf in CONTEXT + tfs})
               for c in coins})
    for b in elig:        # candidates whose daily data failed the checks (not downloaded further)
        r = quality[(b, "1d")]
        if b not in dq_out["coins"] and r["state"] != dq.GOOD:
            dq_out["coins"][b] = dict(state=r["state"], cross_venue=dict(state=dq.GOOD, deviation_pct=None,
                                                                         note="not checked"),
                                      timeframes={"1d": r})
    json.dump(dq_out, open(os.path.join(REPORTS, "data_quality.json"), "w"), indent=1, default=float)

    # ---------- features + candle evidence reports ----------
    EVENT_COLS = ["displacement_up", "displacement_down", "bull_engulf", "bear_engulf", "bull_reject",
                  "bear_reject", "breakout_up", "breakout_down", "retest_up", "retest_down",
                  "failed_breakout_up", "failed_breakout_down", "bull_div", "bear_div"]
    feat_out = dict(checked_utc=started.strftime("%Y-%m-%d %H:%M"), coins={})
    for (b, tf), last in feat_last.items():
        row = last.iloc[-1]
        vals = {k: (None if isinstance(x, float) and not np.isfinite(x) else
                    bool(x) if isinstance(x, (bool, np.bool_)) else
                    float(x) if isinstance(x, (int, float, np.integer, np.floating)) else x)
                for k, x in row.items()}
        vals["recent_events"] = [e for e in EVENT_COLS if last[e].any()]
        feat_out["coins"].setdefault(b, {})[tf] = vals
    json.dump(feat_out, open(os.path.join(REPORTS, "features.json"), "w"), indent=1, default=str)
    ev_out = dict(checked_utc=started.strftime("%Y-%m-%d %H:%M"),
                  label="RESEARCH EVIDENCE, NOT A SIGNAL", settings=ev_cfg,
                  coins=[c["base"] for c in coins], timeframes=evidence)
    json.dump(ev_out, open(os.path.join(REPORTS, "feature_evidence.json"), "w"), indent=1, default=float)

    # ---------- regime report + once-a-day regime log ----------
    order = (["BTC"] if "BTC" in regimes else []) + [b for b in regimes if b != "BTC"]
    rg_out = dict(checked_utc=started.strftime("%Y-%m-%d %H:%M"), data_source=feed.name,
                  note="Regimes now gate every strategy: each trades only in its allowed regimes and with "
                       "timeframe permission (strategy spec v3).",
                  settings=rg_cfg, coins={b: regimes[b] for b in order})
    json.dump(rg_out, open(os.path.join(REPORTS, "regime.json"), "w"), indent=1, default=str)
    rstate_path = os.path.join(REPORTS, "regime_state_offline.json" if args.offline else "regime_state.json")
    rstate = json.load(open(rstate_path)) if os.path.exists(rstate_path) else {}
    today = started.strftime("%Y-%m-%d")
    if regimes and rstate.get("last_logged_date") != today:
        if not args.offline:
            write_regime_log(rg_out, started)
        json.dump({"last_logged_date": today}, open(rstate_path, "w"))

    # ---------- SMC report + append-only live event log ----------
    smc_out = dict(checked_utc=started.strftime("%Y-%m-%d %H:%M"), version=smc.VERSION,
                   note="SMC = hypotheses to test, not doctrine. Strategies S5-S8 use these rules and are "
                        "tested against control twins without SMC.",
                   killzone_now=smc.killzone(int(started.timestamp() * 1000), smc_cfg["killzones"]),
                   coins={})
    for (b, tf), res in smc_res.items():
        smc_out["coins"].setdefault(b, {})[tf] = dict(state=res["state"], recent_events=res["events"][-10:])
    json.dump(smc_out, open(os.path.join(REPORTS, "smc.json"), "w"), indent=1, default=float)
    if not args.offline:
        write_smc_log(smc_res, [c for c in view["signal"]], smc_cfg, rg_series, started, feed.name)
    del smc_res

    # ---------- timeframes report ----------
    models = cfg.get("timeframe_model", {}).get("models", tfm.DEFAULT_MODELS)
    active = cfg.get("timeframe_model", {}).get("active", "B")
    available = set(CONTEXT + tfs + ["7d"])
    tf_out = dict(active_model=active, active_chain=tfm.describe(models[active]),
                  missing_for_active=tfm.missing_timeframes(models[active], available),
                  models={k: dict(chain=tfm.describe(m), missing=tfm.missing_timeframes(m, available))
                          for k, m in models.items()},
                  coins={})
    for c in coins:
        sym, b = c["symbol"], c["base"]
        bars = {tf: int(len(data[(sym, tf)])) if data.get((sym, tf)) is not None else 0
                for tf in ["1w", "1d", "7d"] + tfs}
        w = data.get((sym, "1w"))
        since = (pd.to_datetime(int(w["open_time"].iloc[0]), unit="ms").strftime("%Y-%m")
                 if w is not None and len(w) else None)
        tf_out["coins"][b] = dict(bars=bars, weekly_history_from=since, cross_check=xtf.get(b))

    # ---------- universe report, memory of streaks, and the append-only universe log ----------
    rank_vol = {c["base"]: i + 1 for i, c in enumerate(cands)}
    cand_rows = []
    for c in pool:
        b = c["base"]
        status = ("SIGNAL" if b in signal_set else "RESEARCH" if b in view["research_only"]
                  else "WAITING" if b in view["waiting"] else
                  "ELIGIBLE" if b in elig and elig[b]["ok"] else "EXCLUDED")
        r = elig.get(b, dict(ok=False, reasons=["download failed"], flags=[]))
        row = dict(measures.get(b, {}), coin=b, status=status, volume_rank=rank_vol.get(b),
                   eligible=r["ok"], reasons=r["reasons"], flags=r["flags"],
                   in_streak=ustate["in_streak"].get(b, 0), out_streak=ustate["out_streak"].get(b, 0))
        cand_rows.append(row)
    u_out = dict(checked_utc=started.strftime("%Y-%m-%d %H:%M"), run=ustate["runs"],
                 signal=view["signal"], research_only=view["research_only"], waiting=view["waiting"],
                 leaving=view["leaving"], empty_slots=U["signal_coins"] - len(view["signal"]),
                 rules=dict(signal_coins=U["signal_coins"], research_coins=U["research_coins"],
                            hysteresis_runs=U["hysteresis_runs"]),
                 events=u_events, candidates=cand_rows, excluded_by_list=name_excluded)
    json.dump(u_out, open(os.path.join(REPORTS, "universe.json"), "w"), indent=1, default=float)
    json.dump(ustate, open(state_path, "w"), indent=1)
    if u_events:
        for e in u_events:
            log(f"universe {e['action']}: {e['coin']} - {e['why']}")
        if not args.offline:
            write_universe_log(u_events, started)

    # ---------- write reports ----------
    closed = logdf[logdf["status"] != "OPEN"].dropna(subset=["result_r"])
    fwd_total = dict(signals=int(len(logdf)), closed=int(len(closed)),
                     open=int((logdf["status"] == "OPEN").sum()),
                     win_rate=float((closed["result_r"].astype(float) > 0).mean()) if len(closed) else None,
                     avg_r=float(closed["result_r"].astype(float).mean()) if len(closed) else None,
                     total_r=float(closed["result_r"].astype(float).sum()) if len(closed) else 0.0)
    out = dict(generated_utc=started.strftime("%Y-%m-%d %H:%M"),
               generated_beijing=started.astimezone(BJ).strftime("%Y-%m-%d %H:%M"),
               data_source=feed.name, coins_scanned=[c["base"] for c in coins],
               market=dict(btc_trend=btc, fear_greed=fg), settings=dict(
                   account_usdt=acct, risk_pct=cfg["account"]["risk_per_trade_pct"],
                   fees=cfg["costs"], tp_r=tp["tp_r"], tp_split=tp["tp_split"]),
               position_book=book, position_book_text=book_text, risk=risk_out, watching=watching[:30],
               memory=memory_out, state_changes=events, email_events=email_events, daily=daily,
               daily_subject=briefs.daily_email(daily)["subject"], daily_lines=briefs.daily_email(daily)["lines"],
               weekly=weekly,
               email_settings=dict(email_watching=bool(cfg["signals"].get("email_watching", False))),
               reminders=mail.reminders(board, int(cfg["signals"].get("scan_interval_minutes", 60))),
               signals=final, validation_signals=watch, strategy_scoreboard=board, forward_test=fwd_total,
               lifecycle=dict(registry=os.path.relpath(REGISTRY, ROOT), experiments=len(registry["versions"]),
                              changes=(research or {}).get("changes", []),
                              approval=(research or {}).get("approval") or {},
                              research_run=(research or {}).get("run_utc"),
                              candidate_lessons=(research or {}).get("candidate_lessons", []),
                              missed_moves=(research or {}).get("missed_moves", []),
                              research_history=(research or {}).get("history", {}),
                              not_run={k: sorted(v) for k, v in spec_problems.items()},
                              rule_errors={k: sorted(v) for k, v in rule_errors.items()},
                              idle=[dict(id=x["id"], version=x["version"], status=x["status"],
                                         hypothesis=x["hypothesis"]) for x in idle],
                              bar=dict(min_trades=V["min_trades"], min_expectancy_r=V["min_expectancy_r"],
                                       min_profit_factor=V["min_profit_factor"],
                                       max_drawdown_r=V["max_drawdown_r"],
                                       retune_penalty_r=V["retune_penalty_r"], max_cost_to_r=V["max_cost_to_r"],
                                       research=RC)),
               coin_snapshot=snap, data_quality=dq_out, universe=u_out, timeframes=tf_out,
               features_1h={b: feat_out["coins"].get(b, {}).get("1h") for b in view["signal"]},
               candle_evidence=ev_out, regime=rg_out, smc=smc_out)
    json.dump(out, open(os.path.join(REPORTS, "latest.json"), "w"), indent=1, default=float)
    out["storage"] = storage_info(args.offline)          # measured after latest.json exists
    md = render_md(out, cfg)
    open(os.path.join(REPORTS, "latest.md"), "w").write(md)
    os.makedirs(os.path.join(REPORTS, "daily"), exist_ok=True)
    open(os.path.join(REPORTS, "daily", started.strftime("%Y-%m-%d") + ".md"), "w").write(md)
    pd.DataFrame(board).to_csv(os.path.join(REPORTS, "strategy_scoreboard.csv"), index=False)
    log(f"Done: {len(coins)} coins, {len(board)} strategy/timeframe tests, "
        f"{sum(b['status'] == 'VALIDATION' for b in board)} in VALIDATION, "
        f"{sum(b['status'] == 'PAPER_TRADING' for b in board)} in PAPER_TRADING, {len(final)} signals, "
        f"{len(watch)} paper/validation signals (not emailed)")


def write_failure_journal(rows, when, days=7):
    """memory/failure_journal.md (section 17): every logged signal that closed with a loss - one section 22 record
    with its conditions at entry, what happened (tags) and how far it went both ways (MAE / MFE). Append-only."""
    if rows is None or rows.empty:
        return
    txt = lambda x: x if isinstance(x, str) and x else "-"
    for _, r in rows.iterrows():
        mem.append(MEMORY, "failure_journal.md", mem.record(
            f"{r['coin']} {r['direction']} {r['tf']} {r['strategy']} v{txt(r['version'])} - {r['status']} "
            f"{float(r['result_r']):+.2f}R",
            [f"- signal {r['signal_time_utc']} UTC, closed {r['closed_time_utc']} UTC, stage {txt(r['stage'])}",
             f"- MAE {float(r['mae_r']):+.2f}R / MFE {float(r['mfe_r']):+.2f}R",
             f"- at entry: session {txt(r['session'])}, conditions: {txt(r['conditions']).replace(';', ', ')}",
             f"- what happened: {txt(r['tags']).replace(';', ', ')}",
             "- root cause / fix: (review)"],
            timestamp=when.strftime("%Y-%m-%d %H:%M UTC"), source="engine: hourly scan (reports/signals_log.csv)",
            evidence=f"FACT: {txt(r['stage'])} result {float(r['result_r']):+.2f}R after costs; tags by fixed rules",
            confidence="one trade - an example, not a pattern", strategy=f"{r['strategy']} v{txt(r['version'])}",
            asset=r["coin"], timeframe=r["tf"], regime=txt(r["regime_at_entry"]), review=mem.plus_days(when, days)))


def execution_issues(quality, cross, failed, cfg):
    """Data problems of this run as {key: text} (section 22 execution notes) + a fingerprint of the fee settings."""
    out = {}
    for (coin, tf), r in quality.items():
        if r.get("state") in (dq.DEGRADED, dq.UNSAFE):
            out[f"data|{coin}|{tf}"] = f"{coin} {tf} data: " + ("; ".join(r.get("problems") or []) or r["state"])
    for coin, c in (cross or {}).items():
        if c.get("state") in (dq.DEGRADED, dq.UNSAFE):
            out[f"cross|{coin}"] = (f"{coin} price differs between exchanges ({c['state']}"
                                    + (f", {c['deviation_pct']:.2f}%" if c.get("deviation_pct") is not None else "") + ")")
    for coin in failed or []:
        out[f"download|{coin}"] = f"{coin} download failed"
    fees = json.dumps(cfg["costs"], sort_keys=True)
    return out, fees


def write_execution_notes(issues, fees, when, state_path, days=30):
    """memory/execution_notes.md: a record when a data problem STARTS and when it ENDS (not every hour), and
    when the fee settings change (the first run records the fees in use). Returns what was written."""
    prev = {}
    if os.path.exists(state_path):
        with open(state_path) as f:
            prev = json.load(f)
    old = prev.get("issues", {})
    stamp = dict(timestamp=when.strftime("%Y-%m-%d %H:%M UTC"), source="engine: hourly scan (data check)",
                 strategy="-", timeframe="-", regime="-", review=mem.plus_days(when, days))
    written = []
    for k in sorted(set(issues) - set(old)):
        written.append(mem.record(f"START {issues[k]}", ["- signals from this data are blocked while it lasts"],
                                  evidence="FACT: measured by engine/data_quality.py", confidence="measured",
                                  asset=k.split("|")[1], **stamp))
    for k in sorted(set(old) - set(issues)):
        written.append(mem.record(f"END {old[k]}", [f"- problem first seen {prev.get('since', {}).get(k, '?')} UTC"],
                                  evidence="FACT: the data passes the checks again", confidence="measured",
                                  asset=k.split("|")[1], **stamp))
    if prev.get("fees") != fees:
        written.append(mem.record("Fee settings " + ("in use" if "fees" not in prev else "CHANGED"),
                                  [f"- costs: {fees}"] + ([f"- before: {prev['fees']}"] if "fees" in prev else []),
                                  evidence="FACT: config.yaml -> costs", confidence="configured, not observed",
                                  asset="all", **stamp))
    for t in written:
        mem.append(MEMORY, "execution_notes.md", t)
    since = {k: prev.get("since", {}).get(k, stamp["timestamp"]) for k in issues}
    with open(state_path, "w") as f:
        json.dump(dict(issues=issues, since=since, fees=fees), f, indent=1)
    return written


def coin_facts(coin, daily_df, rg_1d, group, vol_24h, cells, min_trades, now):
    """Measured facts about one coin for memory/coin_notes.md (no interpretation)."""
    facts = []
    if daily_df is not None and len(daily_df) > 30:
        d = daily_df.tail(90)
        rng = ((d["high"] - d["low"]) / d["close"] * 100)
        facts.append(f"- daily range (last 90 days): median {rng.median():.1f}%, 90th percentile {rng.quantile(0.9):.1f}%")
    if rg_1d is not None and len(rg_1d[1]):
        labs = pd.Series(rg_1d[1][-90:]).value_counts(normalize=True)
        facts.append("- 1D regime (last 90 days): " + ", ".join(f"{k} {v * 100:.0f}%" for k, v in labs.items()))
    facts.append(f"- moves with (1h correlation >= 0.7): {group if '+' in str(group) else 'no other signal coin'}")
    if vol_24h:
        facts.append(f"- 24h volume now: {vol_24h / 1e6:,.0f}M")
    good = []
    for ck, c in (cells or {}).items():
        x = (c.get("evidence") or {}).get("by_coin", {}).get(coin)
        if x and x["n"] >= min_trades and x["avg_r"] > 0:
            good.append(f"{ck.replace('|', ' ')} ({x['n']} trades, {x['avg_r']:+.2f}R)")
    facts.append("- strategies profitable on it in the research run (>= "
                 f"{min_trades} trades): " + ("; ".join(sorted(good)[:8]) or "none"))
    return facts


def write_coin_notes(coins, facts_by_coin, when, state_path, days=30):
    """memory/coin_notes.md: one facts record per signal coin, once a week (first scan on Sunday UTC).
    facts_by_coin: {coin: [lines]} or a function returning it (only called when the notes are due)."""
    prev = {}
    if os.path.exists(state_path):
        with open(state_path) as f:
            prev = json.load(f)
    today = when.strftime("%Y-%m-%d")
    if when.weekday() != 6 or prev.get("last") == today:
        return False
    if callable(facts_by_coin):
        facts_by_coin = facts_by_coin()
    for c in coins:
        mem.append(MEMORY, "coin_notes.md", mem.record(
            f"{c} - weekly facts {today}", facts_by_coin.get(c, []) + ["- interpretation: (review)"],
            timestamp=when.strftime("%Y-%m-%d %H:%M UTC"), source="engine: hourly scan + daily research run",
            evidence="FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines",
            confidence="measured", strategy="-", asset=c, timeframe="1d, 1h", regime="-",
            review=mem.plus_days(when, days)))
    with open(state_path, "w") as f:
        json.dump(dict(last=today), f)
    return True


def write_experiments(new_exp, registry):
    """memory/experiments.md: one line per strategy VERSION the first time it is tested (section 11
    experiment count). Append-only."""
    if not new_exp:
        return
    os.makedirs(MEMORY, exist_ok=True)
    path = os.path.join(MEMORY, "experiments.md")
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("# Experiments\n\nAppend-only count of every strategy version ever tested (AGENT_PROMPT.md "
                    "section 11). Each new version of the same idea raises its bar by +0.02R per trade.\n\n"
                    "| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |\n|---|---|---|---|---|---|\n")
        for e in new_exp:
            twin = f" (control twin of {e['twin_of']})" if e.get("twin_of") else ""
            f.write(f"| EXP-{e['experiment']:04d} | {e['first_tested_utc']} | {e['key']}{twin} | {e['family']} | "
                    f"{', '.join(e['timeframes'])} | {e['hypothesis']} |\n")


def read_text(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def claude_review(now):
    """Section 19: the daily review runs at 23:30 Beijing (15:30 UTC) - the morning email shows yesterday's."""
    day = (now - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    rel = f"reports/claude/daily/{day}.md"
    return digest.claude_summary(read_text(os.path.join(ROOT, rel)), rel, day)


def claude_weekly(now):
    """Section 19: the weekly research of this Sunday (or, if it is missing, none - never an old week's)."""
    rel = f"reports/claude/weekly/{now.strftime('%Y-%m-%d')}.md"
    return read_text(os.path.join(ROOT, rel)), rel


def write_lifecycle_log(changes, when):
    """memory/strategy_lifecycle.md: every status change of a strategy version x timeframe. Append-only."""
    if not changes:
        return
    os.makedirs(MEMORY, exist_ok=True)
    path = os.path.join(MEMORY, "strategy_lifecycle.md")
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("# Strategy lifecycle log\n\nAppend-only (AGENT_PROMPT.md section 12). Written by the engine "
                    "when a strategy version changes status on a timeframe.\nBACKTESTING = tested, not good enough "
                    "yet · VALIDATION = passed the long-history bar (signals logged, not emailed) · FAILED = enough "
                    "trades and losing · PAPER_TRADING = passed every research test (paper signals, not emailed) · "
                    "RETIRED = paper results broke the limits · APPROVED needs the operator's yes.\n")
        f.write(f"\n## {when.strftime('%Y-%m-%d %H:%M')} UTC\n")
        for c in changes:
            f.write(f"- **{c['key']} {c['tf']}**: {c['old']} → **{c['new']}**"
                    + (f" ({c['why']})" if c.get("why") else "") + "\n")


def write_universe_log(events, when):
    """Append-only log of every join / leave / exclusion change (memory/universe_log.md)."""
    os.makedirs(MEMORY, exist_ok=True)
    path = os.path.join(MEMORY, "universe_log.md")
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("# Universe log\n\nAppend-only record of which coins the agent watches, and why "
                    "(AGENT_PROMPT.md section 4). Written by the engine; only CHANGES are logged.\n"
                    "JOIN / LEAVE = signal list (top 7) · EXCLUDED / ELIGIBLE = rule results · "
                    "FLAG = worth knowing, not excluded.\n")
        f.write(f"\n## {when.strftime('%Y-%m-%d %H:%M')} UTC\n")
        for e in events:
            f.write(f"- **{e['action']}** {e['coin']} - {e['why']}\n")


def render_universe(u, w):
    w("## 0b. Coins this run")
    n = u["rules"]["signal_coins"]
    w(f"- **Signal coins ({len(u['signal'])}/{n})** - only these can give signals: "
      + (", ".join(f"**{c}**" for c in u["signal"]) or "none"))
    if u["empty_slots"] > 0:
        w(f"- {u['empty_slots']} empty slot(s): waiting for a coin to hold a top-{n} rank for "
          f"{u['rules']['hysteresis_runs']} runs in a row")
    w(f"- **Research only** - backtested, never a signal: " + (", ".join(u["research_only"]) or "none"))
    if u["waiting"]:
        w("- **Waiting to join:** " + ", ".join(f"{c} ({k}/{u['rules']['hysteresis_runs']} runs)"
                                                for c, k in u["waiting"].items()))
    if u["leaving"]:
        w("- **Outside the top, may leave:** " + ", ".join(f"{c} ({k}/{u['rules']['hysteresis_runs']} runs)"
                                                          for c, k in u["leaving"].items()))
    if u["events"]:
        w("- **Changes this run** (also written to `memory/universe_log.md`):")
        for e in u["events"]:
            w(f"  - **{e['action']}** {e['coin']} - {e['why']}")
    rows = [c for c in u["candidates"] if c["status"] == "EXCLUDED"]
    flagged = [c for c in u["candidates"] if any("not available" not in f for f in c["flags"])]
    if rows:
        w("\n| Not eligible | 24h volume | Why |\n|---|---|---|")
        for c in rows:
            v = uni.usd(c["vol_24h"]) if c.get("vol_24h") is not None else "-"
            w(f"| {c['coin']} | {v} | {'; '.join(c['reasons'])} |")
    if flagged:
        w("\n**Flags (not excluded):** " + "; ".join(
            f"{c['coin']}: " + ", ".join(f for f in c["flags"] if "not available" not in f) for c in flagged))
    if u["excluded_by_list"]:
        w(f"\n*Skipped by your exclusion lists:* " + ", ".join(
            f"{c}" for c in sorted(u["excluded_by_list"])) + " (see `config.yaml`)")
    w("")


REGIME_TFS = ["1w", "1d", "4h", "1h"]
SMC_PATTERNS = {"smc_sweep_bull": 1, "smc_sweep_bear": -1, "smc_bos_up": 1, "smc_bos_down": -1,
                "smc_choch_up": 1, "smc_choch_down": -1, "smc_fvg_retrace_bull": 1, "smc_fvg_retrace_bear": -1}
SMC_HTF = {"4h": "1d", "1h": "4h", "30m": "1h", "15m": "1h", "5m": "1h"}   # regime stamped on each event
SMC_LOG_COLS = ["known_utc", "coin", "tf", "event", "direction", "level", "zone_low", "zone_high", "size_atr",
                "killzone_ny", "htf", "htf_regime", "details", "engine", "source"]


def write_smc_log(smc_res, coins, s, rg_series, started, source):
    """Append NEW SMC events (known after the last logged candle) to memory/smc_events.csv.
    Signal coins and s["log_timeframes"] only. The first live run starts the log one hour back
    (no backfill of old history). Watermarks per coin/timeframe live in reports/smc_state.json."""
    state_path = os.path.join(REPORTS, "smc_state.json")
    st = json.load(open(state_path)) if os.path.exists(state_path) else {}
    start_ms = int(started.timestamp() * 1000) - 3_600_000
    rows = []
    for coin in coins:
        for tf in s.get("log_timeframes", ["4h", "1h", "30m", "15m"]):
            res = smc_res.get((coin, tf))
            if res is None:
                continue
            key = f"{coin}|{tf}"
            mark = st.get(key, start_ms)
            ser = rg_series.get((coin, SMC_HTF.get(tf)))
            for e in res["events"]:
                if e["time"] <= mark:
                    continue
                reg = None
                if ser is not None:
                    i = np.searchsorted(ser[0], e["time"], side="right") - 1
                    reg = ser[1][i] if i >= 0 else None
                rows.append(dict(known_utc=pd.to_datetime(e["time"] + 1, unit="ms").strftime("%Y-%m-%d %H:%M"),
                                 coin=coin, tf=tf, event=e["event"], direction="bull" if e["dir"] == 1 else "bear",
                                 level=e["level"], zone_low=e["zone_low"], zone_high=e["zone_high"],
                                 size_atr=e["size_atr"], killzone_ny=e["killzone"] or "", htf=SMC_HTF.get(tf),
                                 htf_regime=reg or "", details=e["info"], engine=smc.VERSION, source=source))
            if res["events"] or key not in st:
                st[key] = max([mark] + [e["time"] for e in res["events"]])
    if rows:
        os.makedirs(MEMORY, exist_ok=True)
        path = os.path.join(MEMORY, "smc_events.csv")
        pd.DataFrame(rows, columns=SMC_LOG_COLS).to_csv(path, mode="a", header=not os.path.exists(path),
                                                        index=False)
    json.dump(st, open(state_path, "w"), indent=1)
    return len(rows)


def render_smc(g, signal, w):
    w("## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)")
    w(f"Killzone right now (New York time): **{g['killzone_now'] or 'none'}**. Nothing trades on SMC yet; "
      "every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). "
      "Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.\n")
    w("| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block "
      "| 1H range position | Liquidity above (1H) | Liquidity below (1H) |")
    w("|---|---|---|---|---|---|---|---|")
    fp = lambda x: fmt_price(x) if x is not None else "-"
    for coin in signal:
        c = g["coins"].get(coin, {})
        m15, h4, h1 = (c.get(tf, {}).get("state") for tf in ("15m", "4h", "1h"))
        if not m15:
            w(f"| {coin} | no 15m data | | | | | | |")
            continue
        lb = m15["last_break"]
        trend = f"{m15['trend'] or 'not set'}" + (f" ({lb['kind']} {lb['candles_ago']} candles ago)" if lb else "")
        sw = {k: v for k, v in m15["last_sweep"].items() if v is not None}
        sweep = (f"{'sell-side (bullish idea)' if min(sw, key=sw.get) == 'bull' else 'buy-side (bearish idea)'} "
                 f"{min(sw.values())} candles ago") if sw else "-"
        open_g = [x for x in m15["open_fvgs"]]
        fvg = (f"{'bull' if open_g[-1]['dir'] == 1 else 'bear'} {fp(open_g[-1]['low'])}-{fp(open_g[-1]['high'])}"
               f"{' (retraced)' if open_g[-1]['retraced'] else ''}") if open_g else "-"
        act = [x for x in (h4 or {}).get("order_blocks", []) if x["state"] == "active"]
        ob = (f"{'bull' if act[-1]['dir'] == 1 else 'bear'} {fp(act[-1]['low'])}-{fp(act[-1]['high'])}") if act else "-"
        rngs = (h1 or {}).get("dealing_range")
        pos = f"{rngs['zone']} ({rngs['position'] * 100:.0f}%)" if rngs else "-"
        liq = lambda lst: (f"{lst[0]['kind']} {fp(lst[0]['level'])} ({lst[0]['dist_atr']} ATR)" if lst else "-")
        w(f"| **{coin}** | {trend} | {sweep} | {fvg} | {ob} | {pos} | {liq((h1 or {}).get('liquidity_above', []))} "
          f"| {liq((h1 or {}).get('liquidity_below', []))} |")
    w("\n*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. "
      "Definitions: `memory/smc_research.md`.*\n")


def regime_cell(r):
    lab = r["label"] + (f" {r['expansion_dir']}" if r.get("expansion_dir") else "")
    return f"{lab} ({r['confidence']})"


def write_regime_log(rg_out, when):
    """Append today's regimes to memory/market_regime_log.md (once per UTC day)."""
    os.makedirs(MEMORY, exist_ok=True)
    path = os.path.join(MEMORY, "market_regime_log.md")
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("# Market regime log\n\nAppend-only, one entry per UTC day (AGENT_PROMPT.md section 6). "
                    "Written by the engine from closed candles; confidence is evidence-based, never a %.\n"
                    "Permission: LONG needs 2 of 1D/4H/1H bullish and no 1W STRONG_BEAR (SHORT: mirror).\n")
        f.write(f"\n## {when.strftime('%Y-%m-%d')} (logged {when.strftime('%H:%M')} UTC · source "
                f"{rg_out['data_source']})\n")
        btc = rg_out["coins"].get("BTC")
        if btc:
            f.write("BTC context: " + " · ".join(f"{tf.upper()} {regime_cell(btc['timeframes'][tf])}"
                                                 for tf in REGIME_TFS if tf in btc["timeframes"])
                    + f" → {btc['permission']}\n")
        f.write("\n| Coin | 1W | 1D | 4H | 1H | Permission |\n|---|---|---|---|---|---|\n")
        for coin, c in rg_out["coins"].items():
            f.write(f"| {coin} | " + " | ".join(regime_cell(c["timeframes"][tf]) if tf in c["timeframes"]
                                                else "-" for tf in REGIME_TFS)
                    + f" | {c['permission']} |\n")


def render_regime(g, w):
    w("## 0f. Market regime")
    w("The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees "
      "(strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and "
      "no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. "
      f"*{g['note']}*\n")
    if not g["coins"]:
        w("No coin data.\n")
        return
    w("| Coin | 1W | 1D | 4H | 1H | Permission |")
    w("|---|---|---|---|---|---|")
    for coin, c in g["coins"].items():
        w(f"| **{coin}** | " + " | ".join(regime_cell(c["timeframes"][tf]) if tf in c["timeframes"] else "-"
                                          for tf in REGIME_TFS)
          + f" | {c['permission']} ({c['permission_reason']}) |")
    btc = g["coins"].get("BTC")
    if btc:
        w("\n**BTC evidence** (most coins follow BTC):")
        for tf in REGIME_TFS:
            r = btc["timeframes"].get(tf)
            if not r:
                continue
            w(f"- **{tf.upper()} {regime_cell(r)}** - for: {'; '.join(r['supporting']) or '-'} · "
              f"against: {'; '.join(r['contradicting']) or '-'}")
    w("\n*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*\n")


def render_features(fs, w):
    w("## 0d. Market features now (1H, newest closed candle)")
    w("Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels "
      "(HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.\n")
    w("| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal "
      "| Last 3 candles |")
    w("|---|---|---|---|---|---|---|")
    num = lambda x, f="{:.2f}": "-" if x is None else f.format(x)
    for coin, f in fs.items():
        if not f:
            w(f"| {coin} | no 1H data | | | | | |")
            continue
        st = f.get("structure") or "not enough swings"
        labels = f"{f.get('swing_high_label') or '-'}/{f.get('swing_low_label') or '-'}"
        w(f"| {coin} | {st} ({labels}) | {num(f.get('last_swing_high'), '{:,.6g}')} / "
          f"{num(f.get('last_swing_low'), '{:,.6g}')} | {num(f.get('close_loc'))} | "
          f"{num(f.get('rel_vol'), '{:.2f}x')} | {num(f.get('atr_ratio'), '{:.2f}x')} | "
          f"{', '.join(f['recent_events']) or '-'} |")
    w("")


def render_evidence(e, w):
    w("## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL")
    st = e["settings"]
    w("Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side "
      "(bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).\n")
    w(f"If you had entered at the NEXT candle's open after each pattern, with a stop {st['stop_atr']:g} ATR away: "
      f"how often did price reach +1R / +2R / +3R **after costs** before the stop (max {st['max_bars']} candles)? "
      f"**Random** = the same test on random candles (same coins, same direction, "
      f"{st['random_per_event']}x as many). **Verdict** compares +1R with random: 'beats chance' only if "
      "better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit "
      "(it can happen after +1R was reached, so the columns can add up to more than 100%). "
      "Many rows are compared at once, so an occasional "
      "'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.\n")
    w("| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    pct = lambda x: "-" if x is None else f"{x * 100:.0f}%"
    for tf, pats in e["timeframes"].items():
        for pat, r in pats.items():
            cost = "-" if r["cost_r"] is None else f"{r['cost_r']:.2f}R"
            w(f"| {tf} | {pat} | {r['events']} | {pct(r['reached'][0])} | {pct(r['reached'][1])} | "
              f"{pct(r['reached'][2])} | {pct(r['stopped'])} | {pct(r['random_reached'][0])} | "
              f"{pct(r['random_reached'][1])} | {r['verdict']} | {cost} |")
    w("")


def render_timeframes(t, w):
    w("## 0c. Timeframes loaded")
    w(f"- **Timeframe model {t['active_model']} (active):** {t['active_chain']}. "
      "Higher timeframes give permission, lower ones give timing; a candle only ever uses "
      "higher-timeframe candles that had already closed.")
    if t["missing_for_active"]:
        w(f"- ⚠️ Model {t['active_model']} needs timeframes that are not downloaded: "
          + ", ".join(t["missing_for_active"]))
    later = [f"{k} (needs {', '.join(m['missing'])})" for k, m in t["models"].items() if m["missing"]]
    if later:
        w("- Models to test later: " + "; ".join(later))
    if not t["coins"]:
        w("")
        return
    cols = list(next(iter(t["coins"].values()))["bars"])
    w("\n| Coin | " + " | ".join(c.upper() for c in cols) + " | Weekly history from | Cross-check |")
    w("|---|" + "---|" * (len(cols) + 2))
    for coin, c in t["coins"].items():
        x = c["cross_check"]
        if x is None:
            check = "not run (offline test data)"
        else:
            bad = [f"{k}: {v['mismatches']}" for k, v in x.items() if v["mismatches"]]
            n = sum(v["checked"] for v in x.values())
            check = ("⚠️ disagree: " + ", ".join(bad)) if bad else f"OK ({n} candles)"
        w(f"| {coin} | " + " | ".join(str(c["bars"][k]) for k in cols)
          + f" | {c['weekly_history_from'] or '-'} | {check} |")
    w("\n*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. "
      "Cross-check = do the bigger candles agree with the smaller candles inside them?*\n")


def render_dq(q, w):
    w("## 0. Data check")
    meaning = {dq.GOOD: "all data passed the checks - signals allowed",
               dq.DEGRADED: "signals only from coins with GOOD data; the others are analysis-only",
               dq.UNSAFE: "**`DATA_STALE / SIGNAL_DISABLED`** - no signals this run"}
    w(f"- **System: {q['system_state']}** - {meaning[q['system_state']]} ({q['reason']})")
    devs = [c["cross_venue"]["deviation_pct"] for c in q["coins"].values()
            if c["cross_venue"]["deviation_pct"] is not None]
    if q["second_exchange"] and devs:
        w(f"- **Price cross-check** {q['data_source']} vs {q['second_exchange']}: "
          f"largest difference {max(devs):.2f}% (limit 0.5%)")
    else:
        w("- **Price cross-check:** second exchange not available this run (not guessed)")
    if q["failed_downloads"]:
        w(f"- **Download failed:** {', '.join(q['failed_downloads'])}")
    if q["blocked_signals"]:
        w(f"- **Signals blocked by bad data:** {'; '.join(q['blocked_signals'])}")
    rows = []
    for coin, c in q["coins"].items():
        why = [f"{tf}: {p}" for tf, r in c["timeframes"].items() for p in r["problems"]]
        if c["cross_venue"]["state"] != dq.GOOD:
            why.append(c["cross_venue"]["note"])
        if why:
            rows.append(f"| {coin} | **{c['state']}** | {'; '.join(why)} |")
    if rows:
        w("\n| Coin | Data state | Problem |\n|---|---|---|")
        for r in rows:
            w(r)
    else:
        w(f"- All {len(q['coins'])} coins passed every check on every timeframe.")
    n_notes = sum(len(r["notes"]) for c in q["coins"].values() for r in c["timeframes"].values())
    if n_notes:
        w(f"- {n_notes} small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`")
    w("")


def render_plans(plans, settings, w):
    w("| # | Coin | TF | Side | Market | Entry | Stop-loss | Targets | Expected hold | Score |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for i, p in enumerate(plans, 1):
        tg = " / ".join(fmt_price(t["price"]) for t in p["targets"])
        w(f"| {i} | **{p['coin']}** | {p['timeframe']} | {p['direction']} | {p['market']} | {fmt_price(p['entry'])} | "
          f"{fmt_price(p['stop'])} | {tg} | {p['expected_hold']} | {p['confidence_score']:.2f} |")
    w("")
    for i, p in enumerate(plans, 1):
        c = p["context"]
        w(f"#### {i}. {p['coin']} {p['direction']} ({p['market']}) · {p['timeframe']} · "
          f"`{p['strategy']}` v{p['version']} ({p['stage']})")
        w(f"- **Signal candle closed:** {p['signal_time_utc']} UTC"
          + (f" ({p['signal_age_candles']} candle(s) ago - still valid)" if p['signal_age_candles'] and
             not p.get("confirm_5m") else ""))
        if p.get("confirm_5m"):
            w("- **5m confirmation needed** (section 8): enter only after a closed 5m bar in the trade direction "
              "(body ≥ 50%, volume ≥ average, price within the entry zone) within 6 bars - otherwise no trade. "
              "Its state is in the position book above.")
        w(f"- **Entry zone:** {fmt_price(min(p['entry_zone']))} - {fmt_price(max(p['entry_zone']))} "
          f"(don't chase if price already left this zone)")
        w(f"- **Stop-loss:** {fmt_price(p['stop'])} ({p['risk_pct_of_price']:.2f}% away)")
        for j, t in enumerate(p["targets"], 1):
            last = j == len(p["targets"])
            after = ("close the rest" if last else f"close {t['close_pct']}%, " +
                     ("move stop to entry (breakeven)" if j == 1 else "move stop to TP1"))
            w(f"- **TP{j}:** {fmt_price(t['price'])} ({t['r']:.1f}R) -> {after}")
        w(f"- **Hold time:** usually ~{p['expected_hold']}; close anyway after {p['max_hold']}")
        if p.get("exit_rule"):
            w(f"- **Early exit if:** {' AND '.join(map(str, p['exit_rule']))}")
        w(f"- **Position size** (account {settings['account_usdt']} USDT, risk "
          f"{p.get('risk_pct', settings['risk_pct']):g}% = {p['risk_usdt']:.2f} USDT): buy **{p['position_qty']:.6g} "
          f"{p['coin']}** (~{p['position_usdt']:.0f} USDT" + (f", needs ~{p['leverage_needed']:.1f}x leverage"
                                                if p['leverage_needed'] > 1 else "") + ")"
          + (" - **made smaller: more would need over 3x leverage**" if p.get("size_capped") else ""))
        if p.get("risk_blocks"):
            w("- **Risk engine" + (" said NO (logged as NO_TRADE):** " if p.get("no_trade") else " would block it live:** ")
              + "; ".join(rk.STEPS[x] for x in p["risk_blocks"]))
        w(f"- **Why:** {p['why']}")
        w(f"- **Rules that were true:** " + "; ".join(f"`{r}`" for r in p["rules_met"]))
        w(f"- **Context:** regime {c.get('regime') or '?'}, {c.get('permission') or '?'}, higher-TF trend "
          f"{c['htf_trend']}, RSI(14) {c['rsi14']}, volume {c['volume_vs_avg']}x average, "
          f"BTC 4H {c['btc_4h']}" + (" ⚠️ AGAINST BTC trend" if c["against_btc_trend"] else "")
          + (" ⚠️ other strategies disagree on direction" if p["conflict"] else "")
          + (f" · {p['agreeing_signals']} strategies agree" if p["agreeing_signals"] > 1 else ""))
        bc, ba = p["backtest_coin"], p["backtest_all"]
        w(f"- **Backtest proof:** on {p['coin']}: {bc['trades']} trades, {bc['win_rate']*100:.0f}% win, "
          f"{bc['avg_r']:+.2f}R avg · all coins: {ba['trades']} trades, {ba['win_rate']*100:.0f}% win, "
          f"{ba['avg_r']:+.2f}R avg, PF {ba['pf']:.2f}\n")


def render_memory(m, w):
    if not m:
        return
    w("### 3e. Memory (section 22)")
    w("| File | Size | Records | Newest record |")
    w("|---|---|---|---|")
    for f in m["files"]:
        w(f"| `memory/{f['file']}` | {f['kb']} KB | {f['records'] or '-'} | {f['last'] or '-'} |")
    if m["missing"]:
        w(f"\nNot created yet: {', '.join(m['missing'])}")
    w(f"\n**Reviews due** (review date passed; for the reviews): " + (
        "; ".join(f"`{d['file']}` {d['title']} ({d['review']})" for d in m["due"][:10])
        + (f" … and {len(m['due']) - 10} more" if len(m["due"]) > 10 else "") if m["due"] else "none"))
    w("Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.\n")


def render_risk(r, w):
    if not r:
        return
    L = r["limits"]
    w("### 2d. Risk engine (section 15 - independent of the strategies)")
    w(f"- **Live results:** today {r['day_r']:+.2f}R (limit {L['day_r']:g}R), this week {r['week_r']:+.2f}R "
      f"(limit {L['week_r']:g}R) · **halts:** " + ("; ".join(r["halts_text"]) or "none"))
    w(f"- **Suspended strategies** (live drawdown > {L['strategy_dd_r']:g}R): " + (", ".join(r["suspended"]) or "none"))
    w(f"- **Risk per trade:** {r['risk_pct']:g}%" + (f" ({r['risk_note']})" if r["risk_note"] else "")
      + f" · leverage never above {L['max_leverage']:g}x (the position is made smaller instead)")
    w(f"- **Heat:** max {L['positions']} positions, {L['per_coin']} per coin, 1 per group of correlated coins and "
      f"direction (1h correlation ≥ {L['corr_threshold']:g}) · groups now: " + (", ".join(r["groups"]) or "none"))
    w(f"- **Every live entry also needs:** reward to TP1 ≥ {L['min_tp1_r']:g}R, no opposing level before TP1, no "
      f"high-impact event within ±{L['blackout_minutes']} min, no duplicate")
    ev = r["upcoming_events"]
    w("- **Event calendar (next 7 days):** " + (", ".join(f"{e['name']} {e['start_utc']} UTC" for e in ev) or "none listed")
      + (f" · **BLACKOUT NOW:** {', '.join(r['blackout_now'])}" if r["blackout_now"] else ""))
    if r["calendar_warning"]:
        w(f"- ⚠️ **{r['calendar_warning']}**")
    if r["no_trade"]:
        w("- **NO_TRADE this run** (APPROVED signals the risk engine refused): " + "; ".join(
            f"{x['coin']} {x['direction']} {x['tf']} {x['strategy']}: {', '.join(x['steps'])}" for x in r["no_trade"]))
    w("")


def render_watching(rows, w):
    w("### 2c. Watching - no signal yet (report only, never emailed)")
    if not rows:
        w("No tracked strategy (VALIDATION or higher) has its market filters open right now.\n")
        return
    w("WATCH = the strategy's trend / regime filters are open; SETUP_FORMING = all entry rules but one are true.\n")
    w("| Coin | TF | Strategy | Stage | Side | State | Rules true | Still missing |")
    w("|---|---|---|---|---|---|---|---|")
    for r in rows:
        w(f"| {r['coin']} | {r['tf']} | {r['strategy']} v{r['version']} | {r['stage']} | {r['direction']} | "
          f"{r['state']} | {r['rules_true']} | {('`' + r['missing'].replace('|', '¦') + '`') if r['missing'] else '-'} |")
    w("")


def render_scoreboard(o, w):
    bar = o["lifecycle"]["bar"]
    R = bar["research"]
    num = lambda x, f="{:+.2f}": "-" if x is None else f.format(x)
    w("## 3. Strategy scoreboard (after fees)")
    run = o["lifecycle"].get("research_run")
    w(f"**Status and long-history numbers** come from the daily research run "
      f"({'last run ' + run + ' UTC' if run else 'not run yet'}); **Layer A** (the last {R['layer_a_days']} days) "
      "is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission "
      "are counted.\n")
    w(f"- **VALIDATION** = long history (Layer B): ≥ {bar['min_trades']} trades, ≥ {bar['min_expectancy_r']:+.2f}R "
      f"per trade (+{bar['retune_penalty_r']:.2f}R per re-tuned version), profit factor ≥ {bar['min_profit_factor']}, "
      f"max drawdown ≤ {bar['max_drawdown_r']:g}R, profitable in both the develop and the validate part, and "
      f"cost-viable (fees + slippage ≤ {bar['max_cost_to_r']:.2f}R, i.e. stop ≥ {1 / bar['max_cost_to_r']:.0f}x the "
      "round-trip cost).")
    w(f"- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ {R['walk_forward_min_positive']} of "
      f"{R['walk_forward_windows'] - 1} windows profitable and together profitable) + edge on ≥ "
      f"{R['min_positive_coins']} coins + still profitable with costs +{(R['cost_stress_x'] - 1) * 100:.0f}% + every "
      f"±{R['perturb_pct']}% change still profitable + no overfitting flag + beats its control twin. Paper signals "
      "are logged, never emailed.")
    w("- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper "
      "results broke the limits; only a new version can be tested again.\n")
    w("| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R "
      "| Walk-fwd | Costs +50% | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) "
      "| Stood down (regime / permission) | Paper+live signals | Why not |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for b in o["strategy_scoreboard"]:
        live = f"{b['live_signals']} ({b['live_avg_r']:+.2f})" if b["live_signals"] else "0"
        stable = "-" if b["perturb_stable"] is None else ("stable" if b["perturb_stable"] else "✗ ") + \
            (f" {b['perturb_worst']}" if not b["perturb_stable"] and b["perturb_worst"] else "")
        wf = "-" if b["walk_forward"] is None else b["walk_forward"] + ("" if b["walk_forward_passed"] else " ✗")
        w(f"| {b['strategy']} | {b['version']} | {b['tf']} | **{b['status']}** | {num(b['trades'], '{}')} | "
          f"{num(b['win_rate'], '{}')} | {num(b['avg_r'], '{:+.3f}')} | {num(b['profit_factor'], '{}')} | "
          f"{num(b['max_dd_r'], '{}R')} | {num(b['develop_avg_r'])} / {num(b['validate_avg_r'])} | "
          f"{num(b['long_avg_r'])} / {num(b['short_avg_r'])} | {wf} | {num(b['stress_avg_r'])} | {stable} | "
          f"{num(b['positive_coins'], '{}')} | {num(b['median_cost_r'], '{:.2f}R')} | "
          f"{b['layer_a_trades']}, {b['layer_a_avg_r']:+.2f} ({b['layer_a_first_avg_r']:+.2f} / "
          f"{b['layer_a_last_avg_r']:+.2f}) | {b['blocked_by_regime']} / {b['blocked_by_permission']} of "
          f"{b['signal_candles']} | {live} | {b['why_not']} |")
    w("")


def render_lifecycle(g, board, w):
    w("### 3b. Strategy lifecycle and control twins")
    w("IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). "
      f"Strategy versions tested so far: **{g['experiments']}** (`memory/experiments.md`); full record per version "
      "and timeframe in `memory/strategy_registry.csv`.\n")
    twins = [b for b in board if b["control_twin"]]
    if twins:
        w("**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the "
          "validate part, with enough trades on both sides):\n")
        w("| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |")
        w("|---|---|---|---|---|---|---|---|")
        num = lambda x: "-" if x is None else f"{x:+.3f}"
        for b in twins:
            beat = {True: "yes", False: "no", None: "too few trades to compare"}[b["beats_twin"]] \
                if b["researched"] else "waiting for research"
            w(f"| {b['strategy']} | {b['tf']} | {b['trades'] if b['trades'] is not None else '-'} | {num(b['avg_r'])} | "
              f"{num(b['validate_avg_r'])} | {num(b['twin_avg_r'])} | {num(b['twin_validate_avg_r'])} | {beat} |")
        w("")
    notes = [b for b in board if b.get("note")]
    for b in notes:
        w(f"- **{b['strategy']} v{b['version']} {b['tf']}:** {b['note']}")
    if g["changes"]:
        ch = g["changes"]
        w("**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): " + "; ".join(
            f"{c['key']} {c['tf']} {c['old']} → {c['new']}" for c in ch[:12])
          + (f"; ... and {len(ch) - 12} more" if len(ch) > 12 else ""))
    appr = g.get("approval") or {}
    for p in appr.get("eligible") or []:
        w(f"- 🗳 **Approval pack ready: {p['strategy']} v{p['version']} {p['tf']}** - {p['paper_signals']} paper signals, "
          f"average {p['paper_avg_r']:+.2f}R. Approve for live emails? (yes/no) - read `{p['pack']}`; to say yes, copy "
          "its line into `config.yaml` → `approvals:`.")
    for x in appr.get("warnings") or []:
        w(f"- ⚠️ **Approval:** {x}")
    for x in appr.get("pine") or []:
        w(f"- 📈 **TradingView script ({x['key']}):** " + (f"`{x['file']}` ({x['mode']} mode) - paste it into TradingView's "
                                                          "Pine Editor to check it with your own eyes"
                                                          if x.get("file") else f"export failed: {x.get('error')}"))
    for sid, errs in g["not_run"].items():
        w(f"- ⚠️ **{sid} not run:** {'; '.join(errs)}")
    for sid, errs in g["rule_errors"].items():
        w(f"- ⚠️ **{sid} rule error:** {'; '.join(errs)}")
    if g["idle"]:
        w("- **Not tested (IDEA / RETIRED):** " + "; ".join(f"{x['id']} v{x['version']} ({x['status']})"
                                                            for x in g["idle"]))
    w("")


def render_attribution(g, board, w):
    w("### 3d. Why trades lose (failure attribution)")
    rows = [b for b in board if b.get("attribution") and b["trades"] and b["trades"] >= 30]
    if not g.get("research_run"):
        w("Filled in by the daily research run.\n")
        return
    w("Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → "
      "`attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than "
      "among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for "
      "losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was "
      "in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / "
      "timeframe tests with 30+ trades are shown.\n")
    if rows:
        w("| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) "
          "| Losers' best point "
          "| Winners' worst point | R before / after costs |")
        w("|---|---|---|---|---|---|---|---|---|")
        num = lambda x: "-" if x is None else f"{x:+.2f}"
        for b in rows:
            a = b["attribution"]
            sysc = ", ".join(a["systematic"] + [x.split(":")[0] for x in a["strategy_level"]]) or "none"
            freq = ", ".join(f"{k} {v * 100:.0f}%" for k, v in a["frequent"]) or "-"
            w(f"| {b['strategy']} | {b['tf']} | {b['status']} | {a['losses'] + a['wins']} ({a['losses']}) | {sysc} | "
              f"{freq} | {num(a['mae_mfe']['losers_mfe_median'])}R | {num(a['mae_mfe']['winners_mae_median'])}R | "
              f"{num(a['gross_avg_r'])} / {num(a['avg_r'])} |")
        w("")
    else:
        w("No strategy / timeframe test has 30+ trades yet.\n")
    if g.get("candidate_lessons"):
        w("**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything "
          "changes, and any change is a new version): " + "; ".join(
              f"`{x['tag']}` ({x['evidence']})" for x in g["candidate_lessons"]))
    missed = g.get("missed_moves") or []
    if missed:
        w("\n**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). "
          "Never change a rule just because a missed move became large:")
        for m in missed:
            w(f"- {m['coin']} {m['direction']} {m['pct']:+.1f}% ({m['start_utc']} → {m['end_utc']} UTC): {m['verdict']}")
    else:
        w("\n**Missed moves:** no strong move in the last 24 hours at the last research run.")
    w("\n*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? "
      "other timeframe? systematic or random?) are answered per test in `reports/research.json` → "
      "`cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*\n")


def render_research(g, w):
    w("### 3c. Research layers (daily run)")
    if not g.get("research_run"):
        w("The daily research run (Layers B/C, costs +50%, ±20% test) has not run yet. It runs once a day on GitHub "
          "(workflow **Research**) and can be started by hand from the Actions tab.\n")
        return
    w(f"Last run: **{g['research_run']} UTC**. History used per timeframe (all research coins pooled; "
      "develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time "
      "windows, the first one only warms up):\n")
    w("| TF | Coins | From | To | Candles (largest coin) | Note |")
    w("|---|---|---|---|---|---|")
    for tf, h in g["research_history"].items():
        w(f"| {tf} | {h['coins']} | {h['from']} | {h['to']} | {h['bars']} | {h.get('note', '')} |")
    w("\n*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): "
      "`reports/research.json`.*\n")


def render_md(o, cfg):
    L = []
    w = L.append
    w(f"# Crypto Signal Report\n")
    w(f"**Updated:** {o['generated_beijing']} Beijing time ({o['generated_utc']} UTC) · "
      f"data: {o['data_source']} · {len(o['coins_scanned'])} coins scanned\n")
    w("> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.\n")
    st = o.get("storage")
    if st:
        w(f"**Storage:** repository {'not checked (offline)' if st['repo_size_mb'] is None else str(st['repo_size_mb']) + ' MB (GitHub)'}"
          f" · large files of this run {st['live_total_mb']:.1f} MB, published to branch `{st['live_branch']}` "
          "(replaced every run, no history)\n")
    if o.get("position_book_text"):
        w("```")
        for line in o["position_book_text"]:
            w(line)
        w("```")
        w("Paper = signals of PAPER_TRADING / VALIDATION versions (tracked, never emailed). The day / week limits, "
          "heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every "
          "state change: `reports/position_events.csv`.\n")
    render_dq(o["data_quality"], w)
    render_universe(o["universe"], w)
    render_timeframes(o["timeframes"], w)
    render_features(o["features_1h"], w)
    render_evidence(o["candle_evidence"], w)
    render_regime(o["regime"], w)
    render_smc(o["smc"], o["universe"]["signal"], w)
    m = o["market"]
    w("## 1. Market mood")
    bt = m["btc_trend"]
    w(f"- **BTC trend:** daily = **{bt.get('1d', '?')}**, 4H = **{bt.get('4h', '?')}**  "
      "(most coins follow BTC - trading against BTC's trend is harder)")
    if m.get("fear_greed"):
        fg = m["fear_greed"]
        w(f"- **Fear & Greed index:** {fg['value']} ({fg['label']}), yesterday {fg['yesterday']}  "
          "(extreme fear/greed = bigger, faster moves)")
    w("")
    w("## 2. Signals right now")
    w("Only **APPROVED** strategy versions (your yes, after paper trading) give signals and emails.\n")
    if not o["signals"]:
        w("**No trade passes all the checks right now. That is normal - no trade is also a position.**\n")
    else:
        render_plans(o["signals"], o["settings"], w)
    if o["validation_signals"]:
        w("### 2b. Paper and validation signals - NOT emailed, do not trade")
        w("From strategy versions in PAPER_TRADING (their paper record decides approval later) or VALIDATION "
          "(passed the long-history bar only). Logged in `reports/signals_log.csv` so their real results can be "
          "checked.\n")
        render_plans(o["validation_signals"], o["settings"], w)
    render_watching(o.get("watching") or [], w)
    render_risk(o.get("risk"), w)
    render_scoreboard(o, w)
    render_lifecycle(o["lifecycle"], o["strategy_scoreboard"], w)
    render_research(o["lifecycle"], w)
    render_attribution(o["lifecycle"], o["strategy_scoreboard"], w)
    render_memory(o.get("memory"), w)
    f = o["forward_test"]
    w("## 4. Live track record (real signals, checked after they happened)")
    if f["closed"]:
        w(f"- {f['signals']} signals logged · {f['closed']} finished · {f['open']} still open")
        w(f"- Win rate **{f['win_rate']*100:.0f}%**, average **{f['avg_r']:+.2f}R** per trade, total **{f['total_r']:+.1f}R** "
          f"(at {o['settings']['risk_pct']}% risk, +1R = +{o['settings']['risk_pct']}% of account)")
    else:
        w(f"- {f['signals']} signals logged, none finished yet. Give it a few weeks before trusting anything.")
    w("\n**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding "
      "(shorts are **futures only**). Details in `config.yaml` → `costs`.")
    base = f"https://github.com/{repo_slug()}/blob/{publish_live.BRANCH}/"
    w("\n**Full data** (branch `" + publish_live.BRANCH + "`, newest copy only): " + " · ".join(
        f"[{os.path.basename(p)}]({base}{p})" for p in publish_live.LIVE_FILES))
    w("\n---\n*R = your risk on the trade. +2R means you made twice what you risked. "
      "Full explanation in the beginner guide.*")
    return "\n".join(L)


if __name__ == "__main__":
    main()
