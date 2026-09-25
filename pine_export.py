#!/usr/bin/env python3
"""
Export a strategy as a TradingView Pine Script v6 strategy (Phase 15; engine/pine.py).

A CROSS-CHECK for your eyes: paste the file into TradingView (Pine Editor -> paste -> Add to chart) on the
exported timeframe. The engine's own entries for the coin on the chart are embedded as green / red triangles,
and a table counts matched / only engine / only Pine entries. TradingView never sends signals.

  python pine_export.py <id> <version> <tf>              e.g.  python pine_export.py donchian_breakout 1.0 4h
  python pine_export.py <id> <version> <tf> --offline    synthetic data (code test)

It downloads the newest candles of the signal coins (--bars per timeframe), runs the engine's own backtest of
that card on them (the same code as the hourly scan) and writes reports/pine/<id>_v<version>_<tf>.pine.
APPROVED strategies are exported automatically by the daily research run (all research coins, full history).
On GitHub: Actions -> "Pine export" -> Run workflow. Nothing here places trades.
"""
import argparse
import datetime as dt
import json
import os
import sys

import yaml

import scanner as sc
from engine import confirm5m as c5m
from engine import data_quality as dq
from engine import history
from engine import pine
from engine import regime as rg
from engine import strategy_spec as sspec

OUT = os.path.join(sc.REPORTS, "pine")


def coins_to_use(offline, n):
    path = os.path.join(sc.REPORTS, "universe.json")
    coins = json.load(open(path)).get("signal", []) if os.path.exists(path) and not offline else []
    return (coins or ["BTC", "ETH", "SOL"])[:n]


def find_card(cfg, sid, version):
    cards, problems, idle = sspec.load(yaml.safe_load(open(os.path.join(sc.ROOT, "strategies.yaml"))), rg.LABELS,
                                       sc.TF_ORDER)
    for s in cards + idle:
        if s["id"] == sid and str(s["version"]) == str(version):
            return s
    raise SystemExit(f"{sid} v{version} is not a valid card in strategies.yaml"
                     + (f" ({'; '.join(problems[sid])})" if sid in problems else ""))


def engine_trades(spec, tf, cfg, coins, bars, offline, now_ms):
    """The engine's backtest trades of this card on each coin (same functions as the hourly scan)."""
    feed = sc.Synthetic() if offline else sc.Binance()
    tfs = [t for t in sc.TF_ORDER if t in cfg["timeframes"]]
    dq_cfg = dq.settings(cfg.get("data_quality"))
    S5 = c5m.settings(cfg.get("confirm_5m"))
    per = {}
    for base in coins:
        sym = base + cfg["market"]["quote"]
        data, quality = {}, {}
        try:
            for t in ["1w", "1d"] + tfs:
                raw, _ = history.update(feed, sym, t, bars, now_ms, None)
                data[(sym, t)], quality[(base, t)] = dq.check_candles(raw, sc.TF_MS[t], now_ms, dq_cfg)
        except Exception as e:
            print(f"skip {base}: {e}")
            continue
        pc = sc.prepare_coin(sym, base, data, quality, tfs, cfg)
        fr = pc["frames"].get(tf)
        if fr is None:
            print(f"skip {base}: no usable {tf} data")
            continue
        L, S, XL, XS, cols = sc.strategy_signals(spec, tf, fr, cfg)
        per[base] = sc.run_backtest(fr["df"], L, S, XL, XS, spec, cfg, tf, cols, None, sc.m5_arrays(pc["frames"]), S5)
        print(f"{base} {tf}: {len(per[base])} engine trades")
    return per


def write(spec, tf, cfg, per, now_txt, folder=OUT, note=""):
    text, info = pine.build(spec, tf, cfg, sc.HTF.get(tf, "1d"), pine.signals_from_trades(per), now_txt, note)
    probs = pine.structure_problems(text)
    if probs:
        raise RuntimeError(f"generated Pine failed the structure check: {probs}")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, pine.filename(spec["id"], spec["version"], tf))
    with open(path, "w") as f:
        f.write(text)
    return path, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("version")
    ap.add_argument("tf")
    ap.add_argument("--offline", action="store_true", help="synthetic data (code test)")
    ap.add_argument("--bars", type=int, default=1500, help="candles per timeframe to download")
    ap.add_argument("--coins", type=int, default=7, help="how many signal coins to embed")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(os.path.join(sc.ROOT, "config.yaml")))
    spec = find_card(cfg, args.id, args.version)
    if args.tf not in spec["timeframes"]:
        sys.exit(f"{args.id} v{args.version} runs on {spec['timeframes']}, not {args.tf}")
    if args.tf not in pine.PINE_TF:
        sys.exit(f"timeframe {args.tf} cannot be exported")
    now = dt.datetime.now(dt.timezone.utc)
    per = engine_trades(spec, args.tf, cfg, coins_to_use(args.offline, args.coins), args.bars, args.offline,
                        int(now.timestamp() * 1000))
    folder = os.path.join(sc.REPORTS, "pine_offline") if args.offline else OUT
    path, info = write(spec, args.tf, cfg, per, now.strftime("%Y-%m-%d %H:%M"), folder,
                       f"last {args.bars} candles of {', '.join(sorted(per))}")
    print(f"Wrote {os.path.relpath(path, sc.ROOT)}: {info['mode']} mode, {info['signals']} engine entries embedded"
          + (f"; not translated: {', '.join(info['unsupported'])}" if info["unsupported"] else ""))


if __name__ == "__main__":
    main()
