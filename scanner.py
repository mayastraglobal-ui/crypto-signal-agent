#!/usr/bin/env python3
"""
Crypto Signal Agent - scanner + backtester
==========================================
Every run it:
  1. picks liquid, established coins (skips meme / AI / stable / brand-new coins)
  2. downloads candles for 4h, 1h, 30m, 15m, 5m
  3. backtests every strategy in strategies.yaml (with fees + slippage)
  4. keeps only strategies that pass the validation rules in config.yaml
  5. finds fresh entry signals and builds a full trade plan (entry, SL, TP1/2/3, hold time)
  6. tracks every past signal forward to see if it REALLY worked (live proof)
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

import numpy as np
import pandas as pd
import requests
import yaml

from engine import data_quality as dq

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(ROOT, "reports")
TF_MS = {"5m": 300_000, "15m": 900_000, "30m": 1_800_000, "1h": 3_600_000,
         "4h": 14_400_000, "1d": 86_400_000}
HTF = {"5m": "1h", "15m": "1h", "30m": "4h", "1h": "4h", "4h": "1d"}
TF_ORDER = ["4h", "1h", "30m", "15m", "5m"]
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
                        "quote_volume": float(t["quoteVolume"])})
        return out

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
        df = pd.DataFrame([r[:6] for r in rows],
                          columns=["open_time", "open", "high", "low", "close", "volume"])
        return _finish(df, tf)


class OKX:
    name = "OKX"
    BASE = "https://www.okx.com"
    BAR = {"5m": "5m", "15m": "15m", "30m": "30m", "1h": "1H", "4h": "4H", "1d": "1Dutc"}

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
                        "quote_volume": float(t["volCcy24h"] or 0)})
        return out

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
        df = pd.DataFrame([r[:6] for r in rows],
                          columns=["open_time", "open", "high", "low", "close", "volume"])
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


class Synthetic:
    """Fake but realistic-looking prices, used only for --offline testing."""
    name = "Synthetic (offline test)"

    def __init__(self, seed=7, fault=None):
        self.seed = seed
        self.fault = fault   # plant a data problem to test the safety checks (see --fault)

    def tickers(self):
        names = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "LINK", "AVAX", "DOGE", "FET",
                 "USDC", "DOT", "LTC", "NEWCOIN"]
        rng = np.random.default_rng(self.seed)
        return [{"symbol": n + "USDT", "last": 1.0, "change_pct": float(rng.normal(0, 3)),
                 "quote_volume": float(rng.uniform(5e7, 2e9))} for n in names]

    def klines(self, symbol, tf, n):
        if symbol == "NEWCOINUSDT" and tf == "1d":
            n = 40
        rng = np.random.default_rng(abs(hash((symbol, tf, self.seed))) % 2**32)
        vol = {"5m": .003, "15m": .005, "30m": .007, "1h": .01, "4h": .02, "1d": .04}[tf]
        regime = np.repeat(rng.choice([-1, 0, 1], size=n // 150 + 1), 150)[:n]
        ret = rng.standard_t(4, n) * vol * 0.7 + regime * vol * 0.12
        close = 100 * np.exp(np.cumsum(ret))
        opn = np.r_[close[0], close[:-1]]
        spread = np.abs(rng.normal(0, vol * 0.6, n)) * close
        high = np.maximum(opn, close) + spread
        low = np.minimum(opn, close) - spread
        volu = rng.lognormal(10, 0.5, n) * (1 + 3 * np.abs(ret) / vol / 10)
        now = int(time.time() * 1000) // TF_MS[tf] * TF_MS[tf]
        ot = now - TF_MS[tf] * np.arange(n, 0, -1)
        df = pd.DataFrame({"open_time": ot, "open": opn, "high": high, "low": low,
                           "close": close, "volume": volu})
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


def make_namespace(df):
    """Everything a strategy rule can use. Results are cached per candle table."""
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

    ns = dict(open=o, high=h, low=l, close=c, volume=v,
              htf_up=df.get("htf_up", pd.Series(True, index=df.index)),
              htf_down=df.get("htf_down", pd.Series(True, index=df.index)),
              ema=ema, sma=sma, rsi=rsi, atr=atr, adx=adx, macd_line=macd_line,
              macd_signal=macd_signal, macd_hist=macd_hist, bb_mid=bb_mid,
              bb_upper=bb_upper, bb_lower=bb_lower, bb_width=bb_width, highest=highest,
              lowest=lowest, shift=shift, prev=prev, vol_sma=vol_sma, pct_rank=pct_rank,
              supertrend_dir=supertrend_dir, cross_up=cross_up, cross_down=cross_down,
              abs=abs, min=min, max=max, np=np)
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
    m = pd.merge_asof(df[["close_time"]].astype("int64"), t.astype({"close_time": "int64"}),
                      on="close_time", direction="backward")
    df["htf_up"] = m["htf_up"].fillna(False).astype(bool).to_numpy()
    df["htf_down"] = m["htf_down"].fillna(False).astype(bool).to_numpy()
    return df


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


def simulate_trade(o, h, l, c, j0, d, entry, R, cfg, max_hold, bar_hours, exit_arr=None):
    """Manage one trade from candle j0 (entry candle). Returns dict or None if still open.
    Conservative: if stop and target are touched in the same candle we assume the STOP hit first.
    Funding (shorts) is charged on the part still open, for every candle held, at entry notional."""
    tp = cfg["trade_plan"]
    k = trade_costs(cfg, d)
    fee_t, fee_m, slip = k["taker"], k["maker"], k["slip"]
    fund_bar = k["funding_8h"] * bar_hours / 8
    tps = [entry + d * r * R for r in tp["tp_r"]]
    split = tp["tp_split"]
    stop = entry - d * R
    remaining, pnl, fees, hit = 1.0, 0.0, fee_t * entry, 0
    n = len(c)
    for j in range(j0, n):
        fees += remaining * fund_bar * entry
        # --- stop-loss first (worst case) ---
        if (d == 1 and l[j] <= stop) or (d == -1 and h[j] >= stop):
            px = o[j] if ((d == 1 and o[j] < stop) or (d == -1 and o[j] > stop)) else stop
            px *= (1 - slip * d)
            pnl += remaining * d * (px - entry)
            fees += remaining * fee_t * px
            reason = "SL" if hit == 0 else f"TP{hit}+stop"
            return dict(exit_idx=j, r=(pnl - fees) / R, reason=reason, hit=hit, bars=j - j0 + 1)
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
            return dict(exit_idx=j, r=(pnl - fees) / R, reason="TP3", hit=hit, bars=j - j0 + 1)
        if hit > 0 and ((d == 1 and c[j] <= stop) or (d == -1 and c[j] >= stop)):
            px = stop * (1 - slip * d)       # came back through the moved stop in the same candle
            pnl += remaining * d * (px - entry)
            fees += remaining * fee_t * px
            return dict(exit_idx=j, r=(pnl - fees) / R, reason=f"TP{hit}+stop", hit=hit, bars=j - j0 + 1)
        # --- early exit rule / time stop (at candle close) ---
        rule_exit = exit_arr is not None and exit_arr[j]
        if rule_exit or (j - j0 + 1) >= max_hold:
            px = c[j] * (1 - slip * d)
            pnl += remaining * d * (px - entry)
            fees += remaining * fee_t * px
            return dict(exit_idx=j, r=(pnl - fees) / R, reason="exit-rule" if rule_exit else "time",
                        hit=hit, bars=j - j0 + 1)
    return None


def backtest(df, sig_long, sig_short, ex_long, ex_short, strat, cfg, tf):
    o, h, l, c = (df[k].to_numpy() for k in ("open", "high", "low", "close"))
    atr = df["_atr"].to_numpy()
    bar_hours = TF_MS[tf] / 3_600_000
    n, t, trades = len(c), 0, []
    while t < n - 1:
        d = 1 if sig_long[t] else (-1 if sig_short[t] else 0)
        if d == 0 or not np.isfinite(atr[t]) or atr[t] <= 0:
            t += 1
            continue
        entry = o[t + 1] * (1 + trade_costs(cfg, d)["slip"] * d)   # enter at NEXT candle open
        R = strat["stop_atr"] * atr[t]
        res = simulate_trade(o, h, l, c, t + 1, d, entry, R, cfg, strat["max_hold_bars"], bar_hours,
                             ex_long if d == 1 else ex_short)
        if res is None:
            break
        res.update(entry_idx=t + 1, dir=d)
        trades.append(res)
        t = res["exit_idx"]
    return trades


def stats(trades):
    if not trades:
        return dict(n=0, win_rate=0.0, exp_r=0.0, pf=0.0, max_dd_r=0.0, avg_bars=0.0, total_r=0.0)
    r = np.array([t["r"] for t in trades])
    gains, losses = r[r > 0].sum(), -r[r < 0].sum()
    eq = np.cumsum(r)
    dd = float((np.maximum.accumulate(np.r_[0, eq]) - np.r_[0, eq]).max())
    return dict(n=len(r), win_rate=float((r > 0).mean()), exp_r=float(r.mean()),
                pf=float(gains / losses) if losses > 0 else float("inf") if gains > 0 else 0.0,
                max_dd_r=dd, avg_bars=float(np.mean([t["bars"] for t in trades])),
                total_r=float(r.sum()))


# =====================================================================
# 4. FORWARD TEST (did past signals really work?)
# =====================================================================
LOG_COLS = ["id", "signal_time_utc", "coin", "tf", "strategy", "direction", "entry", "stop",
            "tp1", "tp2", "tp3", "max_hold_bars", "status", "result_r", "closed_time_utc"]


def load_log():
    p = os.path.join(REPORTS, "signals_log.csv")
    if os.path.exists(p):
        df = pd.read_csv(p)
        for col in LOG_COLS:
            if col not in df:
                df[col] = np.nan
        return df[LOG_COLS]
    return pd.DataFrame(columns=LOG_COLS)


def update_forward(logdf, data, quality, feed, cfg):
    """Replay candles after each OPEN signal using the exact same SL/TP rules.
    Signals whose candles are UNSAFE stay OPEN until the data is trustworthy again."""
    for i, row in logdf[logdf["status"] == "OPEN"].iterrows():
        sym, tf = row["coin"] + cfg["market"]["quote"], row["tf"]
        df = data.get((sym, tf))
        rep = quality.get((row["coin"], tf))
        if df is None:
            try:
                df, rep = fetch_checked(feed, sym, tf, 1000, cfg.get("data_quality"))
            except Exception:
                continue
        if rep is None or rep["state"] == dq.UNSAFE:
            continue
        st = int(pd.Timestamp(row["signal_time_utc"]).value // 1_000_000)
        after = df[df["open_time"] > st].reset_index(drop=True)
        if after.empty:
            continue
        d = 1 if row["direction"] == "LONG" else -1
        entry, stop = float(row["entry"]), float(row["stop"])
        R = abs(entry - stop)
        o, h, l, c = (after[k].to_numpy() for k in ("open", "high", "low", "close"))
        res = simulate_trade(o, h, l, c, 0, d, entry, R, cfg, int(row["max_hold_bars"]),
                             TF_MS[tf] / 3_600_000)
        if res:
            logdf.at[i, "status"] = res["reason"]
            logdf.at[i, "result_r"] = round(res["r"], 3)
            logdf.at[i, "closed_time_utc"] = pd.to_datetime(
                after["close_time"].iloc[res["exit_idx"]], unit="ms").strftime("%Y-%m-%d %H:%M")
    return logdf


def forward_stats(logdf):
    closed = logdf[logdf["status"] != "OPEN"].dropna(subset=["result_r"])
    out = {}
    for (s, tf), g in closed.groupby(["strategy", "tf"]):
        r = g["result_r"].astype(float)
        out[(s, tf)] = dict(n=len(r), win_rate=float((r > 0).mean()), exp_r=float(r.mean()))
    return out


# =====================================================================
# 5. HELPERS
# =====================================================================
def fmt_price(x):
    if x == 0 or not np.isfinite(x):
        return "0"
    digits = max(2, 5 - int(math.floor(math.log10(abs(x)))) - 1)
    return f"{x:,.{min(digits, 8)}f}"


def tf_to_text(tf, bars):
    mins = TF_MS[tf] / 60000 * bars
    return f"{mins/60:.1f} h" if mins >= 120 else f"{mins:.0f} min"


def pick_universe(feed, cfg):
    m = cfg["market"]
    q = m["quote"]
    excluded = {x.upper() for x in m["exclude_meme"] + m["exclude_ai"] + m["exclude_other"]}
    rows = []
    for t in feed.tickers():
        s = t["symbol"]
        if not s.endswith(q):
            continue
        base = s[: -len(q)]
        if (base in excluded or base.endswith(("UP", "DOWN", "BULL", "BEAR"))
                or base.startswith("1000") or t["quote_volume"] < m["min_24h_volume_usdt"]):
            continue
        rows.append(dict(t, base=base))
    rows.sort(key=lambda r: -r["quote_volume"])
    must = [r for r in rows if r["base"] in m["always_include"]]
    rest = [r for r in rows if r["base"] not in m["always_include"]]
    return (must + rest)[: m["top_n_coins"] + 5]   # a few spare for the age filter


# =====================================================================
# 6. MAIN
# =====================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="use synthetic data (code test)")
    ap.add_argument("--coins", type=int, default=None, help="override number of coins")
    ap.add_argument("--fault", choices=["stale_btc", "bad_prices"], default=None,
                    help="offline only: plant a data problem to test the safety checks")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
    strategies = [s for s in yaml.safe_load(open(os.path.join(ROOT, "strategies.yaml")))
                  if s.get("status", "active") in ("active", "candidate")]
    if args.coins:
        cfg["market"]["top_n_coins"] = args.coins
    os.makedirs(REPORTS, exist_ok=True)
    started = dt.datetime.now(dt.timezone.utc)

    # ---------- data source ----------
    if args.fault and not args.offline:
        sys.exit("--fault only works together with --offline")
    feeds = [Synthetic(fault=args.fault)] if args.offline else [Binance(), OKX()]
    feed, universe = None, None
    for f in feeds:
        try:
            universe = pick_universe(f, cfg)
            feed = f
            break
        except Exception as e:
            log(f"{f.name} unavailable: {e}")
    if feed is None:
        sys.exit("No market data source reachable.")   # workflow emails "[SYSTEM] scan FAILED"
    log(f"Data source: {feed.name}; candidate coins: {len(universe)}")

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

    # ---------- download + data-quality checks ----------
    data, coins, quality, failed = {}, [], {}, []
    tfs = [tf for tf in TF_ORDER if tf in cfg["timeframes"]]
    for u in universe:
        if len(coins) >= cfg["market"]["top_n_coins"]:
            break
        sym, base = u["symbol"], u["base"]
        try:
            daily, rep = fetch_checked(feed, sym, "1d", 400, dq_cfg)
            if len(daily) < cfg["market"]["min_listing_days"]:
                log(f"skip {sym}: only {len(daily)} days of history")
                continue
            got = {"1d": (daily, rep)}
            for tf in tfs:
                got[tf] = fetch_checked(feed, sym, tf, int(cfg["timeframes"][tf]), dq_cfg)
        except Exception as e:
            log(f"skip {sym}: {e}")
            failed.append(base)
            continue
        for tf, (df_tf, rep) in got.items():
            data[(sym, tf)] = df_tf
            quality[(base, tf)] = rep
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
                                     *(quality[(c["base"], tf)]["state"] for tf in ["1d"] + tfs))
                  for c in coins}
    sys_state, sys_reason = dq.system_state(coin_state, "BTC", failed,
                                            dq_cfg["system_unsafe_coin_share"])
    log(f"Data quality: system {sys_state} - {sys_reason}")

    def signals_allowed(base, tf):
        """Only GOOD data may produce signals: the signal timeframe, its higher timeframe,
        the cross-exchange price check, and the whole system."""
        if sys_state == dq.UNSAFE or cross[base]["state"] != dq.GOOD:
            return False
        for t in (tf, HTF.get(tf)):
            r = quality.get((base, t))
            if t and (r is None or r["state"] != dq.GOOD):
                return False
        return True

    # ---------- backtest everything ----------
    per = {}       # (strategy, tf) -> {coin: trades}
    live = []      # candidate signals
    snap = {}      # coin snapshot for report
    lb = int(cfg["signals"]["lookback_bars"])
    for u in coins:
        sym, base = u["symbol"], u["base"]
        for tf in tfs:
            df = data.get((sym, tf))
            if df is None or len(df) < 300 or quality[(base, tf)]["state"] == dq.UNSAFE:
                continue    # never backtest on data we cannot trust
            df = add_htf(df.copy(), data.get((sym, HTF[tf])))
            ns = make_namespace(df)
            df["_atr"] = ns["atr"](14)
            n = len(df)
            if tf == "1h":
                snap[base] = dict(price=float(df["close"].iloc[-1]),
                                  atr_pct=float(df["_atr"].iloc[-1] / df["close"].iloc[-1] * 100),
                                  rsi_1h=float(ns["rsi"](ns["close"], 14).iloc[-1]),
                                  change_24h=u["change_pct"], vol_24h=u["quote_volume"])
            for s in strategies:
                if tf not in s.get("timeframes", tfs):
                    continue
                try:
                    L = eval_rules(s.get("long"), ns, df.index)
                    S = eval_rules(s.get("short"), ns, df.index) if cfg["signals"]["allow_shorts"] \
                        else np.zeros(n, bool)
                    XL = eval_rules(s.get("exit_long"), ns, df.index) if s.get("exit_long") else None
                    XS = eval_rules(s.get("exit_short"), ns, df.index) if s.get("exit_short") else None
                except Exception as e:
                    log(f"RULE ERROR in {s['name']}: {e}")
                    continue
                L[:250] = False     # warm-up: let long indicators settle
                S[:250] = False
                tr = backtest(df, L, S, XL, XS, s, cfg, tf)
                split_idx = int(n * cfg["validation"]["in_sample_share"])
                for t in tr:
                    t["oos"] = t["entry_idx"] >= split_idx
                per.setdefault((s["name"], tf), {})[base] = tr
                # ---- fresh signals on the last closed candles ----
                for k in range(lb):
                    t_i = n - 1 - k
                    d = 1 if L[t_i] else (-1 if S[t_i] else 0)
                    if d == 0:
                        continue
                    a = df["_atr"].iloc[t_i]
                    entry = float(df["close"].iloc[-1]) if k == 0 else float(df["open"].iloc[t_i + 1])
                    R = s["stop_atr"] * a
                    if k > 0:   # older signal: still valid only if no SL/TP1 hit and price near entry
                        seg = df.iloc[t_i + 1:]
                        if (d == 1 and (seg["low"].min() <= entry - R or seg["high"].max() >= entry + R)) or \
                           (d == -1 and (seg["high"].max() >= entry + R or seg["low"].min() <= entry - R)):
                            continue
                        if abs(df["close"].iloc[-1] - entry) > 0.3 * R:
                            continue
                    live.append(dict(coin=base, symbol=sym, tf=tf, strategy=s["name"], dir=d,
                                     entry=entry, R=float(R), atr=float(a), age_bars=k,
                                     signal_time=int(df["close_time"].iloc[t_i]),
                                     htf_up=bool(df["htf_up"].iloc[t_i]),
                                     htf_down=bool(df["htf_down"].iloc[t_i]),
                                     rsi=float(ns["rsi"](ns["close"], 14).iloc[t_i]),
                                     vol_ratio=float(df["volume"].iloc[t_i] / ns["vol_sma"](20).iloc[t_i])))
                    break

    # ---------- forward test (live proof) ----------
    logdf = update_forward(load_log(), data, quality, feed, cfg) if not args.offline else load_log()
    fwd = forward_stats(logdf)

    # ---------- judge each strategy x timeframe ----------
    V = cfg["validation"]
    board = []
    verdict = {}
    for (sname, tf), by_coin in per.items():
        allt = [t for tr in by_coin.values() for t in tr]
        st, ins, oos = stats(allt), stats([t for t in allt if not t["oos"]]), stats([t for t in allt if t["oos"]])
        reasons = []
        if st["n"] < V["min_trades"]:
            reasons.append(f"only {st['n']} trades")
        if st["exp_r"] < V["min_expectancy_r"]:
            reasons.append(f"avg {st['exp_r']:+.2f}R/trade")
        if st["pf"] < V["min_profit_factor"]:
            reasons.append(f"profit factor {st['pf']:.2f}")
        if oos["n"] < V["min_oos_trades"]:
            reasons.append(f"only {oos['n']} unseen-test trades")
        if ins["exp_r"] <= 0 or oos["exp_r"] <= 0:
            reasons.append("not profitable in BOTH train and unseen test")
        f = fwd.get((sname, tf))
        if f and f["n"] >= V["forward_pause_after"] and f["exp_r"] < V["forward_pause_below_r"]:
            reasons.append(f"LIVE results bad ({f['exp_r']:+.2f}R over {f['n']} signals)")
        if not reasons:
            status = "WORKS"
        elif st["exp_r"] > 0 and oos["exp_r"] > 0 and not (f and f["n"] >= V["forward_pause_after"]
                                                          and f["exp_r"] < V["forward_pause_below_r"]):
            status = "WEAK"
        else:
            status = "FAILS"
        verdict[(sname, tf)] = status
        board.append(dict(strategy=sname, tf=tf, status=status, trades=st["n"],
                          win_rate=round(st["win_rate"] * 100, 1), avg_r=round(st["exp_r"], 3),
                          profit_factor=round(st["pf"], 2) if np.isfinite(st["pf"]) else 99,
                          max_dd_r=round(st["max_dd_r"], 1), train_avg_r=round(ins["exp_r"], 3),
                          test_avg_r=round(oos["exp_r"], 3), test_trades=oos["n"],
                          avg_hold=tf_to_text(tf, st["avg_bars"]) if st["n"] else "-",
                          live_signals=f["n"] if f else 0,
                          live_avg_r=round(f["exp_r"], 3) if f else None,
                          why_not="; ".join(reasons)))
    board.sort(key=lambda b: ({"WORKS": 0, "WEAK": 1, "FAILS": 2}[b["status"]], -b["avg_r"]))

    # ---------- market mood ----------
    btc = {}
    for tf in ("1d", "4h"):
        d = data.get(("BTC" + cfg["market"]["quote"], tf))
        if d is not None and len(d) > 200:
            c = d["close"]
            e50, e200 = c.ewm(span=50, adjust=False).mean().iloc[-1], c.ewm(span=200, adjust=False).mean().iloc[-1]
            btc[tf] = "UP" if c.iloc[-1] > e50 > e200 else "DOWN" if c.iloc[-1] < e50 < e200 else "SIDEWAYS"
    fg = fear_greed(args.offline)

    # ---------- build trade plans ----------
    tp = cfg["trade_plan"]
    acct = cfg["account"]["size_usdt"]
    risk_usd = acct * cfg["account"]["risk_per_trade_pct"] / 100
    plans, blocked = [], []
    for sgl in live:
        key = (sgl["strategy"], sgl["tf"])
        if verdict.get(key) != "WORKS":
            continue
        if not signals_allowed(sgl["coin"], sgl["tf"]):
            blocked.append(f"{sgl['coin']} {sgl['tf']} {sgl['strategy']}")
            continue
        by_coin = per[key]
        pooled = stats([t for tr in by_coin.values() for t in tr])
        cst = stats(by_coin.get(sgl["coin"], []))
        if cst["n"] < V["min_coin_trades"]:
            continue
        shrunk = (cst["n"] * cst["exp_r"] + 20 * pooled["exp_r"]) / (cst["n"] + 20)
        if shrunk <= V["min_expectancy_r"] or cst["exp_r"] <= 0:
            continue
        d, e, R = sgl["dir"], sgl["entry"], sgl["R"]
        against_btc = (d == 1 and btc.get("4h") == "DOWN") or (d == -1 and btc.get("4h") == "UP")
        qty = risk_usd / R
        strat = next(s for s in strategies if s["name"] == sgl["strategy"])
        plans.append(dict(
            coin=sgl["coin"], pair=sgl["symbol"], timeframe=sgl["tf"], strategy=sgl["strategy"],
            direction="LONG" if d == 1 else "SHORT", market=market_type(d),
            signal_time_utc=pd.to_datetime(sgl["signal_time"], unit="ms").strftime("%Y-%m-%d %H:%M"),
            signal_age_candles=sgl["age_bars"],
            entry=e, entry_zone=[e - 0.2 * R, e + 0.2 * R], stop=e - d * R,
            tp1=e + d * tp["tp_r"][0] * R, tp2=e + d * tp["tp_r"][1] * R, tp3=e + d * tp["tp_r"][2] * R,
            risk_pct_of_price=R / e * 100,
            expected_hold=tf_to_text(sgl["tf"], cst["avg_bars"] or pooled["avg_bars"]),
            max_hold=tf_to_text(sgl["tf"], strat["max_hold_bars"]), max_hold_bars=strat["max_hold_bars"],
            position_qty=qty, position_usdt=qty * e, leverage_needed=qty * e / acct, risk_usdt=risk_usd,
            backtest_coin=dict(trades=cst["n"], win_rate=cst["win_rate"], avg_r=cst["exp_r"]),
            backtest_all=dict(trades=pooled["n"], win_rate=pooled["win_rate"], avg_r=pooled["exp_r"],
                              pf=pooled["pf"]),
            confidence_score=round(shrunk + (0 if not against_btc else -0.05), 3),
            why=strat.get("logic", "").strip(), rules_met=strat["long" if d == 1 else "short"],
            exit_rule=strat.get("exit_long" if d == 1 else "exit_short"),
            context=dict(htf_trend="UP" if sgl["htf_up"] else "DOWN" if sgl["htf_down"] else "SIDEWAYS",
                         rsi14=round(sgl["rsi"], 1), volume_vs_avg=round(sgl["vol_ratio"], 2),
                         btc_4h=btc.get("4h"), against_btc_trend=against_btc)))
    # combine agreement / conflicts per coin
    by = {}
    for p in plans:
        by.setdefault(p["coin"], []).append(p)
    final = []
    for coin, ps in by.items():
        dirs = {p["direction"] for p in ps}
        for p in ps:
            p["agreeing_signals"] = sum(q["direction"] == p["direction"] for q in ps)
            p["conflict"] = len(dirs) > 1
            p["confidence_score"] += 0.03 * (p["agreeing_signals"] - 1) - (0.1 if p["conflict"] else 0)
        final.append(max(ps, key=lambda p: p["confidence_score"]))
    final.sort(key=lambda p: -p["confidence_score"])
    final = final[: cfg["signals"]["max_in_report"]]

    # ---------- log new signals for forward testing ----------
    if not args.offline:
        existing = set(logdf["id"].astype(str))
        new_rows = []
        for p in final:
            sid = f"{p['coin']}-{p['timeframe']}-{p['strategy']}-{p['signal_time_utc']}"
            if sid in existing:
                continue
            new_rows.append(dict(id=sid, signal_time_utc=p["signal_time_utc"], coin=p["coin"],
                                 tf=p["timeframe"], strategy=p["strategy"], direction=p["direction"],
                                 entry=p["entry"], stop=p["stop"], tp1=p["tp1"], tp2=p["tp2"],
                                 tp3=p["tp3"], max_hold_bars=p["max_hold_bars"], status="OPEN",
                                 result_r=np.nan, closed_time_utc=""))
        if new_rows:
            logdf = pd.concat([logdf, pd.DataFrame(new_rows)], ignore_index=True)
        logdf.to_csv(os.path.join(REPORTS, "signals_log.csv"), index=False)

    # ---------- data-quality report ----------
    dq_out = dict(
        checked_utc=started.strftime("%Y-%m-%d %H:%M"), system_state=sys_state, reason=sys_reason,
        status_code="DATA_STALE / SIGNAL_DISABLED" if sys_state == dq.UNSAFE else "SIGNALS_ALLOWED",
        data_source=feed.name, second_exchange=second_name, failed_downloads=failed,
        blocked_signals=blocked,
        coins={c["base"]: dict(state=coin_state[c["base"]], cross_venue=cross[c["base"]],
                               timeframes={tf: quality[(c["base"], tf)] for tf in ["1d"] + tfs})
               for c in coins})
    json.dump(dq_out, open(os.path.join(REPORTS, "data_quality.json"), "w"), indent=1, default=float)

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
               signals=final, strategy_scoreboard=board, forward_test=fwd_total,
               coin_snapshot=snap, data_quality=dq_out)
    json.dump(out, open(os.path.join(REPORTS, "latest.json"), "w"), indent=1, default=float)
    md = render_md(out, cfg)
    open(os.path.join(REPORTS, "latest.md"), "w").write(md)
    os.makedirs(os.path.join(REPORTS, "daily"), exist_ok=True)
    open(os.path.join(REPORTS, "daily", started.strftime("%Y-%m-%d") + ".md"), "w").write(md)
    pd.DataFrame(board).to_csv(os.path.join(REPORTS, "strategy_scoreboard.csv"), index=False)
    log(f"Done: {len(coins)} coins, {len(board)} strategy/timeframe tests, "
        f"{sum(b['status'] == 'WORKS' for b in board)} WORK, {len(final)} signals")


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


def render_md(o, cfg):
    L = []
    w = L.append
    w(f"# Crypto Signal Report\n")
    w(f"**Updated:** {o['generated_beijing']} Beijing time ({o['generated_utc']} UTC) · "
      f"data: {o['data_source']} · {len(o['coins_scanned'])} coins scanned\n")
    w("> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.\n")
    render_dq(o["data_quality"], w)
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
    if not o["signals"]:
        w("**No trade passes all the checks right now. That is normal - no trade is also a position.**\n")
    else:
        w("| # | Coin | TF | Side | Market | Entry | Stop-loss | TP1 | TP2 | TP3 | Expected hold | Score |")
        w("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for i, p in enumerate(o["signals"], 1):
            w(f"| {i} | **{p['coin']}** | {p['timeframe']} | {p['direction']} | {p['market']} | {fmt_price(p['entry'])} | "
              f"{fmt_price(p['stop'])} | {fmt_price(p['tp1'])} | {fmt_price(p['tp2'])} | {fmt_price(p['tp3'])} | "
              f"{p['expected_hold']} | {p['confidence_score']:.2f} |")
        w("")
        split = o["settings"]["tp_split"]
        for i, p in enumerate(o["signals"], 1):
            c = p["context"]
            w(f"### {i}. {p['coin']} {p['direction']} ({p['market']}) · {p['timeframe']} · strategy `{p['strategy']}`")
            w(f"- **Signal candle closed:** {p['signal_time_utc']} UTC"
              + (f" ({p['signal_age_candles']} candle(s) ago - still valid)" if p['signal_age_candles'] else ""))
            w(f"- **Entry zone:** {fmt_price(min(p['entry_zone']))} - {fmt_price(max(p['entry_zone']))} "
              f"(don't chase if price already left this zone)")
            w(f"- **Stop-loss:** {fmt_price(p['stop'])} ({p['risk_pct_of_price']:.2f}% away)")
            w(f"- **TP1:** {fmt_price(p['tp1'])} -> close {int(split[0]*100)}%, move stop to entry (breakeven)")
            w(f"- **TP2:** {fmt_price(p['tp2'])} -> close {int(split[1]*100)}%, move stop to TP1")
            w(f"- **TP3:** {fmt_price(p['tp3'])} -> close the rest")
            w(f"- **Hold time:** usually ~{p['expected_hold']}; close anyway after {p['max_hold']}")
            if p.get("exit_rule"):
                w(f"- **Early exit if:** {' AND '.join(map(str, p['exit_rule']))}")
            w(f"- **Position size** (account {o['settings']['account_usdt']} USDT, risk "
              f"{o['settings']['risk_pct']}% = {p['risk_usdt']:.2f} USDT): buy **{p['position_qty']:.6g} {p['coin']}** "
              f"(~{p['position_usdt']:.0f} USDT" + (f", needs ~{p['leverage_needed']:.1f}x leverage" if p['leverage_needed'] > 1 else "")
              + ")")
            w(f"- **Why:** {p['why']}")
            w(f"- **Rules that were true:** " + "; ".join(f"`{r}`" for r in p["rules_met"]))
            w(f"- **Context:** higher-TF trend {c['htf_trend']}, RSI(14) {c['rsi14']}, volume {c['volume_vs_avg']}x average, "
              f"BTC 4H {c['btc_4h']}" + (" ⚠️ AGAINST BTC trend" if c["against_btc_trend"] else "")
              + (" ⚠️ other strategies disagree on direction" if p["conflict"] else "")
              + (f" · {p['agreeing_signals']} strategies agree" if p["agreeing_signals"] > 1 else ""))
            bc, ba = p["backtest_coin"], p["backtest_all"]
            w(f"- **Backtest proof:** on {p['coin']}: {bc['trades']} trades, {bc['win_rate']*100:.0f}% win, "
              f"{bc['avg_r']:+.2f}R avg · all coins: {ba['trades']} trades, {ba['win_rate']*100:.0f}% win, "
              f"{ba['avg_r']:+.2f}R avg, PF {ba['pf']:.2f}\n")
    w("## 3. Strategy scoreboard (auto backtest)")
    w("WORKS = passed every test -> can give signals · WEAK = positive but not proven -> watch only · "
      "FAILS = ignored\n")
    w("| Strategy | TF | Status | Trades | Win % | Avg R/trade | PF | Train R | Unseen-test R | Avg hold | Live signals (avg R) | Why not |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for b in o["strategy_scoreboard"]:
        live = f"{b['live_signals']} ({b['live_avg_r']:+.2f})" if b["live_signals"] else "0"
        w(f"| {b['strategy']} | {b['tf']} | **{b['status']}** | {b['trades']} | {b['win_rate']} | {b['avg_r']:+.3f} | "
          f"{b['profit_factor']} | {b['train_avg_r']:+.3f} | {b['test_avg_r']:+.3f} | {b['avg_hold']} | {live} | {b['why_not']} |")
    w("")
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
    w("\n---\n*R = your risk on the trade. +2R means you made twice what you risked. "
      "Full explanation in the beginner guide.*")
    return "\n".join(L)


if __name__ == "__main__":
    main()
