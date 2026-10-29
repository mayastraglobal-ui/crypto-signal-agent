#!/usr/bin/env python3
"""
Trend portfolio, the daily step (2026-10-29, operator: "build trend portfolio") - PAPER ONLY. The rules and the
backtest are in engine/trend_portfolio.py; the guide is docs/TREND_PORTFOLIO.md.

Run by the hourly scan workflow after scanner.py. It does its work once per daily close: when a new closed daily
candle exists (after 00:00 UTC = 08:00 Beijing), it downloads every own coin's daily candles (Binance spot, the same
data as the backtest), books the new day(s) in the paper account and writes
  reports/trend_portfolio.json   the state: targets per coin, today's changes, the paper account (the live watcher
                                 sends it to Telegram once a day)
  reports/trend_portfolio.md     the same as a page
Any other hour it changes nothing. A failure is printed and never stops the scan (continue-on-error).

  python trend_portfolio.py            the daily step
  python trend_portfolio.py --force    recompute now (the paper account still books each day only once)
"""
import argparse
import json
import os
import sys
import time

import yaml

import scanner as sc
from engine import data_quality as dq
from engine import trend_portfolio as tp

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(ROOT, "reports", "trend_portfolio.json")
PAGE = os.path.join(ROOT, "reports", "trend_portfolio.md")
BARS = 1000                       # daily candles per coin: the 360-day signal needs 361; the rest = the backtest shown


def load_state(path=STATE):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def coins(cfg):
    return list(sc.breadth_coins(cfg))                 # the operator's own coins (universe.own_coins)


def run(cfg, feed, now_ms, force=False, path=STATE, page=PAGE):
    """Returns (state, note). Writes the files only when a new daily close was booked (or force)."""
    S = tp.settings(cfg.get("trend_portfolio"), (cfg.get("costs") or {}).get("long"))
    if not S["enabled"]:
        return None, "trend portfolio disabled (config.yaml -> trend_portfolio.enabled)"
    prev = load_state(path)
    newest_close = now_ms // tp.DAY_MS * tp.DAY_MS - tp.DAY_MS          # open time of the newest closed daily candle
    if prev and int(prev.get("day_ms", 0)) >= newest_close and not force:
        return prev, f"up to date ({prev['day']})"
    dq_cfg = dq.settings(cfg.get("data_quality"))
    frames, problems = {}, []
    for c in coins(cfg):
        try:
            d, rep = sc.fetch_checked(feed, c + cfg["market"]["quote"], "1d", BARS, dq_cfg)
        except Exception as e:
            problems.append(f"{c}: download failed ({type(e).__name__})")
            continue
        if rep["state"] == dq.UNSAFE or d is None or not len(d):
            problems.append(f"{c}: daily data {rep['state']}")
            continue
        frames[c] = d[["open_time", "high", "low", "close"]].reset_index(drop=True)
    if not frames or "BTC" not in frames:
        return prev, "no usable daily data: " + "; ".join(problems)
    st = tp.update(prev, frames, S, now_ms)
    st["backtest"] = tp.backtest(frames, S)
    st["problems"] = problems
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(st, f, indent=1, default=float)
    with open(page, "w") as f:
        f.write(tp.markdown(st))
    return st, f"booked {st['day']}: paper account ${st['equity']:,.2f}" + (f" ({'; '.join(problems)})" if problems else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    with open(os.path.join(ROOT, "config.yaml")) as f:
        cfg = yaml.safe_load(f)
    st, note = run(cfg, sc.Binance(), int(time.time() * 1000), a.force)
    print("Trend portfolio:", note)
    if st is None and "disabled" not in note:
        sys.exit(1)


if __name__ == "__main__":
    main()
