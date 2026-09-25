#!/usr/bin/env python3
"""
Outside feeds -> reports/feeds.json (run by the hourly scan workflow; the rules are in engine/feeds.py).

GitHub Actions has open internet; Claude's task environment does not. So this saves, every hour, what the tasks
need from outside: crypto news headlines (CoinDesk, Cointelegraph, The Block), the Fear & Greed index, Binance
announcements (listings, delistings, maintenance) and the next Deribit BTC / ETH options expiries.
Each source is fetched on its own; a failure is written into the file (status "error") and never stops the run.

  python feeds.py                  fetch and write reports/feeds.json
"""
import datetime as dt
import json
import os
import sys

import requests

from engine import feeds as F

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "reports", "feeds.json")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; crypto-signal-agent feeds; +https://github.com/)",
           "Accept": "application/rss+xml, application/xml, application/json, text/xml, */*"}


def get(url, as_json):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json() if as_json else r.text


def coins():
    """Our coins (signal + research-only) from the newest scan - headlines mentioning them are marked."""
    p = os.path.join(ROOT, "reports", "universe.json")
    try:
        u = json.load(open(p))
        return sorted(set(u.get("signal", [])) | set(u.get("research_only", [])))
    except (OSError, ValueError):
        return ["BTC", "ETH"]


def collect(now, fetch=None, our_coins=()):
    """Everything, source by source. fetch(url, as_json) is replaceable for tests (default: get)."""
    fetch = fetch or get
    out = dict(generated_utc=now.strftime("%Y-%m-%d %H:%M"), note=F.NOTE, sources={}, news=[], fear_greed=None,
               binance=None, deribit=[])

    def run(name, url, as_json, parse):
        try:
            res = parse(fetch(url, as_json))
            out["sources"][name] = dict(status="ok", url=url)
            return res
        except Exception as e:                       # any failure: recorded, never fatal
            out["sources"][name] = dict(status="error", url=url, error=f"{type(e).__name__}: {str(e)[:160]}")
            return None

    for name, url in F.NEWS.items():
        out["news"] += run(name, url, False, lambda x, n=name: F.parse_rss(x, n, our_coins)) or []
    out["news"].sort(key=lambda x: x["utc"] or "", reverse=True)
    out["fear_greed"] = run("Fear & Greed", F.FNG_URL, True, F.parse_fng)
    out["binance"] = run("Binance announcements", F.BINANCE_URL, True, lambda x: F.parse_binance(x, our_coins))
    for cur in F.DERIBIT_CURRENCIES:
        out["deribit"] += run(f"Deribit {cur} options", F.DERIBIT_URL.format(cur=cur), True,
                              lambda x, c=cur: F.parse_deribit(x, c, now)) or []
    return out


def main():
    now = dt.datetime.now(dt.timezone.utc)
    out = collect(now, our_coins=coins())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    for name, s in out["sources"].items():
        print(f"{name}: {s['status']}" + (f" - {s['error']}" if s.get("error") else ""))
    print(f"{len(out['news'])} headlines, {len(out['deribit'])} expiries -> {os.path.relpath(OUT, ROOT)}")
    if not any(s["status"] == "ok" for s in out["sources"].values()):
        sys.exit(1)                                  # nothing at all: shown as a failed step (never stops the scan)


if __name__ == "__main__":
    main()
