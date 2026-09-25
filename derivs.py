#!/usr/bin/env python3
"""
Record futures market-structure data every hour (Phase 17 C, item 10; the rules are in engine/derivs.py).

For every signal and research-only coin: funding rate history, and hourly open interest (USD), long/short account
ratio and taker buy/sell ratio. Appended to reports/derivs_hourly.csv.gz and reports/funding.csv.gz, which travel on
the live-reports branch (publish_live.py) - the history is kept from now on, because the exchanges keep only ~30
days of hourly open interest. Older days are back-filled from data.binance.vision files, a few per run.
Writes reports/derivs_quality.json (small, on main) for the report and Claude's fact sheet.

Two SEPARATE series (never mixed - their levels differ): OKX = the main series, the only one the building blocks read;
Binance (its API when reachable + data.binance.vision files) = research only. A failure is recorded and never stops
the scan.

  python derivs.py                 fetch, append, check (run by the hourly scan workflow before scanner.py)
"""
import datetime as dt
import io
import json
import os
import sys
import zipfile

import requests
import yaml

from engine import derivs as D

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(ROOT, "reports")
HOURLY = os.path.join(REPORTS, "derivs_hourly.csv.gz")
FUNDING = os.path.join(REPORTS, "funding.csv.gz")
QUALITY = os.path.join(REPORTS, "derivs_quality.json")
FAPI = "https://fapi.binance.com"
OKX = "https://www.okx.com"
VISION = "https://data.binance.vision/data/futures/um"
HEADERS = {"User-Agent": "crypto-signal-agent (derivs recorder)"}


def get(url, params=None, raw=False):
    r = requests.get(url, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.content if raw else r.json()


def unzip_csv(content):
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        return z.read(z.namelist()[0]).decode("utf-8", errors="replace")


def settings():
    try:
        with open(os.path.join(ROOT, "config.yaml")) as f:
            s = (yaml.safe_load(f) or {}).get("derivs") or {}
    except OSError:
        s = {}
    return dict(backfill_days=int(s.get("backfill_days", 365)), backfill_per_run=int(s.get("backfill_per_run", 4)))


def coins():
    try:
        with open(os.path.join(REPORTS, "universe.json")) as f:
            u = json.load(f)
        return list(dict.fromkeys(list(u.get("signal", [])) + list(u.get("research_only", []))))
    except (OSError, ValueError):
        return ["BTC", "ETH"]


def fetch_okx(coin, fetch=get):
    """The MAIN series (every building block reads only this): OKX rubik hourly stats + funding history."""
    inst, q = f"{coin}-USDT-SWAP", dict(ccy=coin, period="1H")
    hourly = D.okx_hourly(coin, fetch(OKX + "/api/v5/rubik/stat/contracts/open-interest-volume", q),
                          fetch(OKX + "/api/v5/rubik/stat/contracts/long-short-account-ratio", q),
                          fetch(OKX + "/api/v5/rubik/stat/taker-volume", dict(q, instType="CONTRACTS")))
    funding = D.okx_funding(coin, fetch(OKX + "/api/v5/public/funding-rate-history", dict(instId=inst, limit=100)))
    return hourly, funding


def fetch_binance(coin, fetch=get):
    """A RESEARCH series only (kept separately, never mixed with the main one): Binance USDT-M futures API."""
    sym, p = coin + "USDT", dict(symbol=coin + "USDT", period="1h", limit=500)
    hourly = D.binance_hourly(coin, fetch(FAPI + "/futures/data/openInterestHist", p),
                              fetch(FAPI + "/futures/data/globalLongShortAccountRatio", p),
                              fetch(FAPI + "/futures/data/takerlongshortRatio", p))
    funding = D.binance_funding(coin, fetch(FAPI + "/fapi/v1/fundingRate", dict(symbol=sym, limit=1000)))
    return hourly, funding


def fetch_live(coin, fetch=get):
    """(hourly rows, funding rows, {source: ok?}, errors) - both series, each on its own; one failing never
    replaces the other (the main series simply has a gap, which the building blocks read as 'unknown')."""
    rows_h, rows_f, got, errs = [], [], {}, []
    for name, fn in ((D.MAIN_SOURCE, fetch_okx), ("binance", fetch_binance)):
        try:
            h, f = fn(coin, fetch)
            rows_h += h
            rows_f += f
            got[name] = True
        except Exception as e:
            got[name] = False
            errs.append(f"{name}: {type(e).__name__}: {str(e)[:120]}")
    return rows_h, rows_f, got, errs


def backfill(coin, hourly_hist, funding_hist, now, S, fetch=get):
    """A few older days (data.binance.vision daily metrics) and months (funding) per run, newest missing first."""
    sym, rows_h, rows_f, errs = coin + "USDT", [], [], []
    have = set((hourly_hist[hourly_hist["coin"] == coin]["ts"] // (24 * D.HOUR_MS)).astype(int)) if len(hourly_hist) else set()
    todo = [now.date() - dt.timedelta(days=k) for k in range(2, S["backfill_days"] + 1)]
    todo = [d for d in todo if (dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp() * 1000)
            // (24 * D.HOUR_MS) not in have][:S["backfill_per_run"]]
    for d in todo:
        try:
            rows_h += D.vision_metrics(coin, unzip_csv(fetch(f"{VISION}/daily/metrics/{sym}/{sym}-metrics-{d}.zip",
                                                             raw=True)))
        except Exception as e:
            errs.append(f"files {d}: {type(e).__name__}")
            break                                        # older days are unlikely to exist either
    months = sorted({(d.year, d.month) for d in (now.date() - dt.timedelta(days=k)
                                                 for k in range(35, S["backfill_days"] + 1, 28))}, reverse=True)
    have_f = set(pd_month(funding_hist[funding_hist["coin"] == coin]["time"])) if len(funding_hist) else set()
    for y, m in [x for x in months if x not in have_f][:1]:
        try:
            rows_f += D.vision_funding(coin, unzip_csv(fetch(
                f"{VISION}/monthly/fundingRate/{sym}/{sym}-fundingRate-{y}-{m:02d}.zip", raw=True)))
        except Exception as e:
            errs.append(f"funding files {y}-{m:02d}: {type(e).__name__}")
    return rows_h, rows_f, errs


def pd_month(times):
    return {(t.year, t.month) for t in (dt.datetime.fromtimestamp(int(x) / 1000, dt.timezone.utc) for x in times)}


def run(now, fetch=get, coin_list=None):
    S = settings()
    hourly, funding = D.read(HOURLY, D.HOURLY_COLS), D.read(FUNDING, D.FUNDING_COLS)
    for path, df in ((HOURLY, hourly), (FUNDING, funding)):
        if os.path.exists(path) and os.path.getsize(path) > 200 and not len(df):
            raise RuntimeError(f"{path} exists but cannot be read - nothing written (history is never replaced)")
    n_before = (len(hourly), len(funding))
    status = {}
    for c in coin_list or coins():
        h, f, got, errs = fetch_live(c, fetch)
        bh, bf, berr = backfill(c, D.series(hourly, "binance_files"), D.series(funding, "binance_files"), now, S, fetch)
        hourly = D.merge(hourly, h + bh, "ts")
        funding = D.merge(funding, f + bf, "time")
        status[c] = dict(source=D.MAIN_SOURCE if got.get(D.MAIN_SOURCE) else None, sources=got,
                         new_hourly=len(h), backfilled_hours=len(bh), errors=errs + berr)
    if len(hourly) < n_before[0] or len(funding) < n_before[1]:
        raise RuntimeError("history would shrink - nothing written")              # never lose history
    os.makedirs(REPORTS, exist_ok=True)
    hourly.to_csv(HOURLY, index=False, compression="gzip")
    funding.to_csv(FUNDING, index=False, compression="gzip")
    q = D.quality(*D.clean(hourly, funding), list(status), int(now.timestamp() * 1000))
    for c in q:
        q[c]["fetch"] = status[c]
    with open(QUALITY, "w") as f:
        json.dump(dict(checked_utc=now.strftime("%Y-%m-%d %H:%M"), coins=q), f, indent=1, default=float)
    return q


def main():
    q = run(dt.datetime.now(dt.timezone.utc))
    for c, x in q.items():
        print(f"{c}: {x['state']} · main {D.MAIN_SOURCE} {'ok' if x['fetch']['source'] else 'FAILED'} · "
              f"{x.get('hours', 0)} hours of main history · research rows {x.get('research_rows', {})}"
              + "".join(f"\n  ! {p}" for p in x.get("problems", []) + x["fetch"]["errors"]))
    if not any(x["fetch"]["source"] for x in q.values()):
        sys.exit(1)                                   # nothing fetched: a failed (continue-on-error) step


if __name__ == "__main__":
    main()
