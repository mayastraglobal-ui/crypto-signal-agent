"""
📈 Live track record + 🚨 drift monitor (operator request 2026-10-13: "build track record ... perfectly safe way").

The track record: every 🔵 TEST, 🟡 PAPER and 🟢 LIVE setup the hourly scan recorded (reports/signals_log.csv - entry at
the signal candle close, the same plan rules for every setup, results AFTER fees), per strategy / version /
timeframe / coin: trades, win %, average R, total R, worst drawdown, losing streaks, the equity curve - next to what
the 5-year backtest says for that coin (reports/research.json by_coin). One honest scorecard.

The drift monitor asks, for every strategy / timeframe / coin with live results: is this still inside what its own
backtest calls normal? Two checks, both on closed live setups only:
  * losing streak: the current run of losses L, with the backtest's loss rate q on that coin, has a chance of
    p = 1 - (1 - q^L)^(n - L + 1) to appear somewhere in n trades. p < streak_p (5%) -> DRIFT.
  * average: n >= avg_min_n live setups, the live average is below 0R and more than avg_z (2) standard errors below
    the backtest average (the live spread, at least sd_floor) -> DRIFT.
A DRIFT pauses that pair's Telegram alerts (TEST, PAPER and LIVE alike) - the SAFE direction only. GitHub keeps
recording its setups silently, so the same checks run every hour on the growing record and the pause ends by itself
once neither check fires any more (e.g. a win ended the streak and the average is back within range). The monitor
never promotes, never changes a rule, gate, size, cost or approval - better-than-expected results are only reported.
Pure functions only: no internet, no files.
"""
import math

import numpy as np
import pandas as pd

DEFAULTS = dict(enabled=True, streak_p=0.05, min_streak=3, avg_min_n=15, avg_z=2.0, sd_floor=1.0, curve_points=60)
STAGES = {"TEST": "🔵 TEST", "PAPER_TRADING": "🟡 PAPER", "APPROVED": "🟢 LIVE"}


def settings(raw):
    s = dict(DEFAULTS)
    s.update({k: v for k, v in (raw or {}).items() if k in DEFAULTS})
    for k in ("streak_p", "avg_z", "sd_floor"):
        s[k] = float(s[k])
    for k in ("min_streak", "avg_min_n", "curve_points"):
        s[k] = int(s[k])
    s["enabled"] = bool(s["enabled"])
    return s


def streak_p(L, n, q):
    """Chance that a run of at least L losses appears somewhere in n trades with loss rate q (independent trades;
    a slightly generous approximation - it never says 'rare' too early)."""
    if L <= 0 or n < L or not 0 < q < 1:
        return 1.0
    return 1.0 - (1.0 - q ** L) ** (n - L + 1)


def _runs(r):
    """(current losing run, longest losing run) of a list of results (oldest first)."""
    cur = best = 0
    for x in r:
        cur = cur + 1 if x <= 0 else 0
        best = max(best, cur)
    return cur, best


def stats(r):
    """Trades, wins, win %, average, total, worst drawdown (R, from the running peak), losing runs, sample sd."""
    r = [float(x) for x in r]
    n = len(r)
    if not n:
        return dict(n=0, wins=0, win_rate=None, avg_r=None, total_r=0.0, max_dd_r=0.0, cur_loss_run=0, max_loss_run=0,
                    sd=None)
    eq = np.cumsum(r)
    dd = float(np.max(np.maximum.accumulate(np.r_[0.0, eq])[1:] - eq)) if n else 0.0
    cur, best = _runs(r)
    return dict(n=n, wins=int(sum(1 for x in r if x > 0)), win_rate=round(100.0 * sum(1 for x in r if x > 0) / n, 1),
                avg_r=round(float(np.mean(r)), 3), total_r=round(float(eq[-1]), 2), max_dd_r=round(max(dd, 0.0), 2),
                cur_loss_run=cur, max_loss_run=best, sd=round(float(np.std(r, ddof=1)), 3) if n > 1 else None)


def drift(live, bt, S):
    """(verdict, reasons): 'drift' (pause), 'watch' (a warning sign, no pause) or 'ok'. live: stats(); bt: the
    backtest on this coin {n, avg_r, win_rate} or None (no backtest = never paused, only reported)."""
    if not live["n"] or not bt or not bt.get("n"):
        return "ok", []
    why, warn = [], []
    wr = bt.get("win_rate")
    q = 1.0 - float(wr) / 100.0 if wr is not None else None
    L = live["cur_loss_run"]
    if q is not None and L >= S["min_streak"]:
        p = streak_p(L, live["n"], q)
        txt = (f"{L} losses in a row - in its backtest ({wr:.0f}% won) a run that long shows up in "
               f"{p * 100:.0f}% of {live['n']}-trade periods")
        (why if p < S["streak_p"] else warn).append(txt)
    if live["n"] >= S["avg_min_n"] and bt.get("avg_r") is not None:
        se = max(float(live["sd"] or 0), S["sd_floor"]) / math.sqrt(live["n"])
        z = (live["avg_r"] - float(bt["avg_r"])) / se
        txt = (f"live {live['avg_r']:+.2f}R over {live['n']} vs backtest {float(bt['avg_r']):+.2f}R "
               f"({z:+.1f} standard errors)")
        if live["avg_r"] < 0 and z < -S["avg_z"]:
            why.append(txt)
        elif z < -S["avg_z"] / 2:
            warn.append(txt)
    if why:
        return "drift", why
    return ("watch", warn) if warn else ("ok", [])


def backtests(research, program=None):
    """{(key, coin): {n, avg_r, win_rate}} from research.json's by_coin (every cell), program.json's coins as a
    fallback (program cells on a night research.json missed)."""
    out = {}
    for ck, row in ((program or {}).get("cells") or {}).items():
        for coin, x in (row.get("coins") or {}).items():
            out[(ck, coin)] = dict(n=x.get("n"), avg_r=x.get("avg_r"), win_rate=x.get("win_rate"))
    for ck, c in ((research or {}).get("cells") or {}).items():
        for coin, x in (((c.get("evidence") or {}).get("by_coin")) or {}).items():
            out[(ck, coin)] = dict(n=x.get("n"), avg_r=x.get("avg_r"), win_rate=x.get("win_rate"))
    return out


def build(logdf, now_utc, research=None, program=None, prev=None, S=None):
    """The track record dict (reports/track_record.json). logdf: the signals log; prev: the last file (the drift
    pauses' start times are kept). now_utc: 'YYYY-MM-DD HH:MM'."""
    S = S or settings(None)
    bts = backtests(research, program)
    prev_paused = {(p["key"], p["coin"]): p for p in (prev or {}).get("paused") or []}
    pairs, paused, curve_rows = [], [], []
    d = None
    if logdf is not None and len(logdf):
        d = logdf[logdf["stage"].isin(list(STAGES)) & (logdf["status"].astype(str) != "OPEN")].copy()
        d["result_r"] = pd.to_numeric(d["result_r"], errors="coerce")
        d = d.dropna(subset=["result_r"])
        d["version"] = d["version"].fillna("1.0").astype(str)
        d["key"] = d["strategy"].astype(str) + "@" + d["version"] + "|" + d["tf"].astype(str)
        d["_t"] = pd.to_datetime(d["closed_time_utc"].fillna(d["signal_time_utc"]), errors="coerce")
        d = d.sort_values("_t", kind="stable")
    if d is not None and len(d):
        for (k, coin), g in d.groupby(["key", "coin"], sort=True):
            st = stats(g["result_r"].tolist())
            stage = g["stage"].iloc[-1]
            bt = bts.get((k, coin))
            verdict, why = drift(st, bt, S) if S["enabled"] else ("ok", [])
            row = dict(key=k, coin=coin, stage=stage, label=STAGES.get(stage, stage), live=st, backtest=bt,
                       verdict=verdict, why=why, last_utc=str(g["closed_time_utc"].iloc[-1] or ""))
            pairs.append(row)
            if verdict == "drift":
                since = (prev_paused.get((k, coin)) or {}).get("since_utc") or now_utc
                paused.append(dict(key=k, coin=coin, label=row["label"], since_utc=since, why=why))
        eq = np.cumsum(d["result_r"].to_numpy(dtype=float))
        step = max(1, len(eq) // S["curve_points"])
        curve_rows = [dict(t=str(t)[:16], r=round(float(e), 2)) for t, e in zip(d["_t"].iloc[::step], eq[::step])]
        if curve_rows and curve_rows[-1]["r"] != round(float(eq[-1]), 2):
            curve_rows.append(dict(t=str(d["_t"].iloc[-1])[:16], r=round(float(eq[-1]), 2)))
    by_stage = {}
    for stage, label in STAGES.items():
        r = d[d["stage"] == stage]["result_r"].tolist() if d is not None and len(d) else []
        by_stage[stage] = dict(label=label, **stats(r))
    total = stats(d["result_r"].tolist() if d is not None and len(d) else [])
    pairs.sort(key=lambda p: ({"drift": 0, "watch": 1, "ok": 2}[p["verdict"]], -p["live"]["n"]))
    resumed = [dict(key=k, coin=c) for (k, c) in prev_paused if (k, c) not in {(p["key"], p["coin"]) for p in paused}]
    return dict(utc=now_utc, settings=S, total=total, by_stage=by_stage, pairs=pairs, paused=paused, resumed=resumed,
                curve=curve_rows,
                note="Every TEST / PAPER / LIVE setup the hourly scan recorded (entry at the signal close, after fees). "
                     "The alerts actually sent (5m-confirmed) are in the journal review.")


def _r(x):
    return "-" if x is None else f"{x:+.2f}R"


def md_lines(tr):
    """reports/track_record.md."""
    t = tr["total"]
    L = ["# 📈 Live track record", "",
         f"Updated {tr['utc']} UTC by the hourly scan (engine/track_record.py). {tr['note']}", "",
         "| Stage | Closed | Win % | Average | Total | Worst drawdown | Longest losing run |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for s in list(tr["by_stage"].values()) + [dict(t, label="**All**")]:
        wr = "-" if s["win_rate"] is None else f"{s['win_rate']:.0f}"
        L.append(f"| {s['label']} | {s['n']} | {wr} | {_r(s['avg_r'])} | {s['total_r']:+.2f}R | {s['max_dd_r']:.2f}R | "
                 f"{s['max_loss_run']} |")
    L += ["", "## 🚨 Drift monitor", ""]
    if tr["paused"]:
        L.append("Alerts **paused** (outside what the backtest calls normal - GitHub keeps recording, the pause ends by "
                 "itself when the checks clear):")
        L += [f"- {p['label']} {p['key'].replace('|', ' ')} on {p['coin']} since {p['since_utc']} UTC: "
              + "; ".join(p["why"]) for p in tr["paused"]]
    else:
        L.append("- nothing paused: every strategy's live results are inside what its backtest calls normal.")
    watch = [p for p in tr["pairs"] if p["verdict"] == "watch"]
    if watch:
        L += ["", "Warning signs (no pause yet):"] + [f"- {p['key'].replace('|', ' ')} on {p['coin']}: "
                                                      + "; ".join(p["why"]) for p in watch]
    L += ["", "## Per strategy and coin (live vs 5-year backtest)", "",
          "| Strategy | TF | Coin | Stage | Closed | Win % | Live avg | Backtest avg | Total | Worst DD | Check |",
          "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for p in tr["pairs"]:
        lv, bt = p["live"], p["backtest"] or {}
        L.append(f"| {p['key'].split('@')[0]} | {p['key'].split('|')[1]} | {p['coin']} | {p['label']} | {lv['n']} | "
                 f"{lv['win_rate']:.0f} | {_r(lv['avg_r'])} | {_r(bt.get('avg_r'))} | {lv['total_r']:+.2f}R | "
                 f"{lv['max_dd_r']:.2f}R | {dict(drift='🚨 paused', watch='⚠️ watch', ok='✅')[p['verdict']]} |")
    if not tr["pairs"]:
        L.append("| - | - | - | - | 0 | - | - | - | - | - | no closed live setup yet |")
    if tr["curve"]:
        L += ["", "## Equity curve (all stages, R after fees)", "", "| Closed | Running total |", "|---|---:|"]
        L += [f"| {c['t']} | {c['r']:+.2f}R |" for c in tr["curve"][-20:]]
    return L


def telegram(tr, limit=8):
    """/track: the scorecard in a few lines."""
    t = tr["total"]
    L = [f"📈 <b>Live track record</b> · {tr['utc']} UTC",
         f"All: {t['n']} closed · {_r(t['avg_r'])} a trade · total {t['total_r']:+.2f}R · worst drawdown "
         f"{t['max_dd_r']:.2f}R (after fees)"]
    for s in tr["by_stage"].values():
        if s["n"]:
            L.append(f"{s['label']}: {s['n']} · {s['win_rate']:.0f}% won · {_r(s['avg_r'])} · {s['total_r']:+.2f}R")
    if tr["paused"]:
        L += ["", "🚨 <b>Paused by the drift monitor</b>:"]
        L += [f"• {p['key'].split('@')[0]} {p['key'].split('|')[1]} {p['coin']}: {p['why'][0]}" for p in tr["paused"]]
    top = [p for p in tr["pairs"] if p["live"]["n"]][:limit]
    if top:
        L += ["", "Live vs backtest:"]
        L += [f"{dict(drift='🚨', watch='⚠️', ok='✅')[p['verdict']]} {p['key'].split('@')[0]} {p['key'].split('|')[1]} "
              f"{p['coin']}: {p['live']['n']} · {_r(p['live']['avg_r'])} (backtest {_r((p['backtest'] or {}).get('avg_r'))})"
              for p in top]
    if not t["n"]:
        L.append("No closed live setup yet - the record grows with every TEST / PAPER setup.")
    L.append("<i>The full table: reports/track_record.md on GitHub.</i>")
    return "\n".join(L)


def change_notes(tr, known):
    """Telegram notes for pauses that are new and pauses that ended since the watcher last looked. known: the set of
    'key|coin' strings the watcher already told the operator about. Returns (notes, the new known set)."""
    now = {f"{p['key']}|{p['coin']}" for p in tr.get("paused") or []}
    notes = []
    for p in tr.get("paused") or []:
        if f"{p['key']}|{p['coin']}" not in known:
            notes.append(f"🚨 <b>Drift monitor: alerts paused</b> · {p['label']} {p['key'].split('@')[0]} "
                         f"{p['key'].split('|')[1]} on {p['coin']}\n" + "\n".join(f"• {w}" for w in p["why"])
                         + "\nIts live results are outside what its 5-year backtest calls normal. GitHub keeps "
                           "recording it; alerts come back by themselves when the checks clear. Nothing else changed.")
    for k in sorted(set(known) - now):
        sid, _, rest = k.partition("@")
        notes.append(f"✅ <b>Drift monitor: alerts back on</b> · {sid} {rest.split('|')[1]} on {rest.split('|')[2]} - its "
                     "live results are back inside the normal range.")
    return notes, now
