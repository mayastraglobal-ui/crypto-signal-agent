"""
The weekly review (Forward Test Program PR 3, operator plan 2026-10-09): what the 🔵 TEST and 🟡 PAPER strategies of
the program did on the live market, and which ones move up or down - with the operator's tap.

Inputs (all files the agent already writes):
  * reports/signals_log.csv - every TEST / PAPER setup the hourly scan recorded (stage, result after fees, fees_r,
    market_type); TEST rows have NO 5m check
  * reports/program.json   - the 5-year backtest per strategy / version / timeframe / coin
  * reports/journal_review.json - the live watcher's alerts (5m-confirmed) and the operator's taps (journal sync)
  * memory/strategy_registry.csv, reports/research_counts.json, the promotions (config.yaml + the operator's taps)

What it decides, by fixed rules (never a gate, cost or trials-bar change):
  * PROMOTE candidates: a TEST strategy / version / timeframe / coin with >= promote_min_trades closed live setups,
    an average above promote_min_avg_r AFTER fees, and a positive backtest on that coin - best evidence first,
    at most paper_max in paper together, one per strategy per coin. It only becomes 🟡 PAPER after the operator's tap
    (or a promotions line in config.yaml). PAPER is practice: 🟢 LIVE still needs the full pass bar, 20 good paper
    signals and the operator's approval line - nothing here lowers that.
  * DEMOTE: a promoted pair whose paper record has >= demote_min_trades closed signals averaging below
    demote_below_r goes back to 🔵 TEST by itself (the safer direction needs no tap).
  * honest confidence for every number (few trades = "too early"), results by market type, before / after fees,
    with vs without the 5m check, ideas for new versions (Claude's weekly research may turn one into a lab card),
    and a system check.
Pure functions only: no internet, no files.
"""
import datetime as dt
import math

import numpy as np
import pandas as pd

DEFAULTS = dict(promote_min_trades=10, promote_min_avg_r=0.0, paper_max=5, demote_min_trades=10,
                demote_below_r=0.0, idea_min_trades=10, idea_market_below_r=-0.20, idea_fee_gap_r=0.15,
                idea_5m_gap_r=0.20)
LIVE_STAGES = ("TEST", "PAPER_TRADING")
BJ = dt.timezone(dt.timedelta(hours=8))


def settings(section):
    s = dict(DEFAULTS)
    s.update({k: v for k, v in (section or {}).items() if k in DEFAULTS})
    for k in ("promote_min_trades", "paper_max", "demote_min_trades", "idea_min_trades"):
        s[k] = int(s[k])
    return s


def confidence(n, avg, sd=None):
    """Honest words for a live result (Idea 3)."""
    if n == 0:
        return "no live trade yet"
    head = f"{avg:+.2f}R over {n} trade{'s' if n != 1 else ''}"
    if n < 10:
        return f"{head}: too early to say anything"
    t = avg / (sd / math.sqrt(n)) if sd and sd > 0 else 0.0
    if avg <= 0:
        return f"{head}: not working so far"
    if t < 1:
        return f"{head}: still uncertain - could be luck"
    if t < 2:
        return f"{head}: promising, not proven"
    return f"{head}: strong so far (live results can still change)"


def _stats(r):
    r = np.asarray([x for x in r if x == x], dtype=float)
    if not len(r):
        return dict(n=0, win_rate=0.0, avg_r=0.0, total_r=0.0, sd=0.0)
    return dict(n=int(len(r)), win_rate=round(float((r > 0).mean()) * 100, 1), avg_r=round(float(r.mean()), 3),
                total_r=round(float(r.sum()), 2), sd=float(r.std(ddof=1)) if len(r) > 1 else 0.0)


def verdict_of(market_type):
    """'DOWN (1D WEAK_BULL, ...)' -> 'DOWN'."""
    return str(market_type or "").split(" ")[0] or "unknown"


def number_from_id(key):
    """'P07-SQUEEZE-RETEST-V1@1.0|4h' -> 7 (the program's naming), else None."""
    head = str(key).split("-")[0]
    return int(head[1:]) if head[:1] == "P" and head[1:].isdigit() else None


def cell_key(row):
    return f"{row['strategy']}@{row['version']}|{row['tf']}"


# ---------------------------------------------------------------- promotions
def parse_promotions(cfg_list, decisions=None):
    """The operator's promotions: config.yaml -> promotions (lines {strategy, version, tf, coin, date}) and the taps
    in Telegram (journal/decisions.csv rows with action promote / unpromote, read by journal_review.py).
    Returns [dict(key, coin, date, source)] - the newest decision per pair wins, an unpromote removes it."""
    out = {}
    for x in cfg_list or []:
        try:
            k = f"{x['strategy']}@{str(x.get('version', '1.0'))}|{x['tf']}"
            out[(k, str(x["coin"]))] = dict(key=k, coin=str(x["coin"]), date=str(x.get("date") or ""), source="config")
        except (KeyError, TypeError):
            continue
    for d in sorted(decisions or [], key=lambda d: str(d.get("time_utc") or "")):
        k, c = d.get("key"), d.get("coin")
        if not k or not c:
            continue
        if d.get("action") == "promote":
            out[(k, c)] = dict(key=k, coin=c, date=str(d.get("time_utc") or "")[:10], source="Telegram")
        elif d.get("action") == "unpromote":
            out.pop((k, c), None)
    return sorted(out.values(), key=lambda p: (p["date"], p["key"], p["coin"]))


def paper_record(logdf, key, coin):
    """Closed PAPER_TRADING results (after fees) of one cell on one coin, oldest first."""
    if logdf is None or logdf.empty:
        return []
    d = logdf[(logdf["stage"] == "PAPER_TRADING") & (logdf["status"] != "OPEN") & (logdf["coin"] == coin)]
    d = d.dropna(subset=["result_r"])
    d = d[d.apply(lambda r: cell_key(dict(strategy=r["strategy"], version=str(r["version"] or "1.0"),
                                           tf=r["tf"])) == key, axis=1)] if len(d) else d
    return d.sort_values("closed_time_utc")["result_r"].astype(float).tolist() if len(d) else []


def active_promotions(promos, logdf, number_of, S):
    """Which promotions are in force: oldest first, at most paper_max pairs, one per program strategy per coin, and
    never a pair whose paper record failed (demoted). number_of: {'id@ver': program strategy number}.
    Returns (active {key: [coins]}, demoted [dict], refused [dict(why)])."""
    active, demoted, refused, used = {}, [], [], set()
    for p in promos:
        rec = paper_record(logdf, p["key"], p["coin"])
        if len(rec) >= S["demote_min_trades"] and float(np.mean(rec[-S["demote_min_trades"]:])) < S["demote_below_r"]:
            demoted.append(dict(p, n=len(rec), avg_r=round(float(np.mean(rec[-S["demote_min_trades"]:])), 3)))
            continue
        num = number_of.get(p["key"].split("|")[0])
        if (num, p["coin"]) in used:
            refused.append(dict(p, why=f"strategy {num} already in paper on {p['coin']} (one per strategy per coin)"))
            continue
        if sum(len(v) for v in active.values()) >= S["paper_max"]:
            refused.append(dict(p, why=f"paper is full ({S['paper_max']} pairs)"))
            continue
        used.add((num, p["coin"]))
        active.setdefault(p["key"], []).append(p["coin"])
    return active, demoted, refused


def promotion_moves(active, prev_via, status_of, blocked=()):
    """What the research run does with the promotions tonight. active: {key: coins} in force; prev_via: the keys that
    were PAPER because of a promotion until now; status_of(key): the cell's status after tonight's lifecycle;
    blocked: keys that may never be promoted (BIASED). Returns (to_paper, release, via):
      to_paper - set the cell to PAPER_TRADING (promoted, not there yet);
      release  - PAPER only because of a promotion that is no longer in force (demoted / unpromoted): back to testing;
      via      - the keys that are PAPER because of a promotion after tonight (PAPER only on their promoted coins).
    A cell that reached PAPER through the pass bar itself is left alone (PAPER on every coin); APPROVED / RETIRED too."""
    to_paper, release, via = [], [], []
    for k in sorted(active):
        st = status_of(k)
        if k in blocked or st in ("APPROVED", "RETIRED") or (st == "PAPER_TRADING" and k not in prev_via):
            continue
        via.append(k)
        if st != "PAPER_TRADING":
            to_paper.append(k)
    for k in sorted(prev_via or []):
        if k not in via and status_of(k) == "PAPER_TRADING":
            release.append(k)
    return to_paper, release, via


# ---------------------------------------------------------------- the review
def live_table(logdf, now, keys=None):
    """{(key, coin): dict(stage, all, week, gross, by_market)} from the signals log (TEST and PAPER rows of the
    program cells). keys: the program cell keys (None = every cell)."""
    out = {}
    if logdf is None or logdf.empty:
        return out
    d = logdf[logdf["stage"].isin(LIVE_STAGES) & (logdf["status"] != "OPEN")].dropna(subset=["result_r"]).copy()
    if d.empty:
        return out
    d["version"] = d["version"].fillna("1.0").astype(str)
    d["key"] = d["strategy"] + "@" + d["version"] + "|" + d["tf"]
    if keys is not None:
        d = d[d["key"].isin(set(keys))]
    week0 = pd.Timestamp(now.replace(tzinfo=None) - dt.timedelta(days=7))
    closed = pd.to_datetime(d["closed_time_utc"], errors="coerce")
    fees = pd.to_numeric(d["fees_r"], errors="coerce") if "fees_r" in d else pd.Series(np.nan, index=d.index)
    for (k, coin, stage), g in d.groupby(["key", "coin", "stage"]):
        r = g["result_r"].astype(float)
        f = fees.loc[g.index]
        wk = closed.loc[g.index] >= week0
        bym = {}
        for v, gg in g.groupby(g["market_type"].map(verdict_of) if "market_type" in g else pd.Series("unknown",
                                                                                                  index=g.index)):
            bym[v] = _stats(gg["result_r"].astype(float))
        out[(k, coin, stage)] = dict(all=_stats(r), week=_stats(r[wk.to_numpy()]),
                                     gross=_stats((r + f).dropna()) if f.notna().any() else None, by_market=bym)
    return out


def build(now, logdf, program, reg_cells, promos_active, demoted, refused, journal=None, research_runs=None,
          scan_utc=None, S=None):
    """The weekly review dict (reports/weekly_review.json). now: UTC datetime. promos_active: {key: [coins]}."""
    S = S or settings(None)
    cells = (program or {}).get("cells") or {}
    live = live_table(logdf, now, list(cells))
    rows, cands = [], []
    in_paper = {(k, c) for k, cs in (promos_active or {}).items() for c in cs}
    nums = {(k, c): (cells.get(k) or {}).get("strategy") or number_from_id(k)
            for k, cs in (promos_active or {}).items() for c in cs}
    for (k, coin, stage), x in sorted(live.items()):
        c = cells.get(k) or {}
        bt = (c.get("coins") or {}).get(coin) or {}
        a = x["all"]
        row = dict(key=k, coin=coin, stage="PAPER" if stage == "PAPER_TRADING" else "TEST", strategy=c.get("strategy"),
                   name=c.get("name"), version=c.get("version"), tf=k.split("|")[1], live=a, week=x["week"],
                   gross=x["gross"], by_market=x["by_market"],
                   backtest=dict(n=bt.get("n"), avg_r=bt.get("avg_r"), win_rate=bt.get("win_rate")) if bt else None,
                   confidence=confidence(a["n"], a["avg_r"], a["sd"]))
        rows.append(row)
        if row["stage"] == "TEST" and (k, coin) not in in_paper and a["n"] >= S["promote_min_trades"] and \
                a["avg_r"] > S["promote_min_avg_r"] and bt and float(bt.get("avg_r") or 0) > 0:
            cands.append(dict(row, score=round(a["avg_r"] * math.sqrt(a["n"]), 3)))
    # promotion candidates: the best evidence first, room in paper, one per strategy per coin
    room = max(0, S["paper_max"] - len(in_paper))
    used = {(nums[p], p[1]) for p in in_paper}
    promote = []
    for cd in sorted(cands, key=lambda r: -r["score"]):
        if len(promote) >= room:
            break
        if (cd["strategy"], cd["coin"]) in used:
            continue
        used.add((cd["strategy"], cd["coin"]))
        promote.append(dict(key=cd["key"], coin=cd["coin"], strategy=cd["strategy"], name=cd["name"],
                            version=cd["version"], tf=cd["tf"], live=cd["live"], backtest=cd["backtest"],
                            confidence=cd["confidence"],
                            why=f"{cd['live']['n']} live TEST setups, {cd['live']['avg_r']:+.2f}R a trade after fees "
                                f"({cd['live']['win_rate']:.0f}% won); 5-year backtest on {cd['coin']} "
                                f"{float(cd['backtest']['avg_r']):+.2f}R over {cd['backtest']['n']} trades"))
    return dict(week=f"{now.isocalendar()[0]}-W{now.isocalendar()[1]:02d}", utc=now.strftime("%Y-%m-%d %H:%M"),
                final=now.weekday() == 6 and now.hour >= 4, rows=rows, promote=promote,
                paper=[dict(key=k, coins=cs) for k, cs in sorted((promos_active or {}).items())],
                demoted=demoted or [], refused=refused or [], ideas=ideas(rows, journal, S),
                five_min=five_min(rows, journal), system=system_check(now, research_runs, scan_utc, program, journal,
                                                                      rows),
                totals=totals(rows), settings=S)


def totals(rows):
    out = {}
    for st in ("TEST", "PAPER"):
        n = sum(r["live"]["n"] for r in rows if r["stage"] == st)
        tot = sum(r["live"]["total_r"] for r in rows if r["stage"] == st)
        wn = sum(r["week"]["n"] for r in rows if r["stage"] == st)
        wt = sum(r["week"]["total_r"] for r in rows if r["stage"] == st)
        out[st] = dict(n=n, total_r=round(tot, 2), avg_r=round(tot / n, 3) if n else None, week_n=wn,
                       week_total_r=round(wt, 2))
    return out


def ideas(rows, journal, S):
    """Idea 2: plain suggestions for new versions (Claude's weekly research may turn one into a lab card - one change
    each, tested like every card; nothing changes by itself)."""
    out = []
    for r in rows:
        name = f"{r['key'].split('@')[0]} {r['tf']} on {r['coin']}"
        for v, x in (r["by_market"] or {}).items():
            if x["n"] >= S["idea_min_trades"] and x["avg_r"] <= S["idea_market_below_r"] and v not in ("unknown", ""):
                out.append(f"{name}: loses in {v} markets ({x['avg_r']:+.2f}R over {x['n']}) - test a version that "
                           f"stands down when the coin is {v}")
        g = r.get("gross")
        if g and g["n"] >= S["idea_min_trades"] and g["avg_r"] > 0 >= r["live"]["avg_r"] and \
                g["avg_r"] - r["live"]["avg_r"] >= S["idea_fee_gap_r"]:
            out.append(f"{name}: positive before fees ({g['avg_r']:+.2f}R) but not after ({r['live']['avg_r']:+.2f}R) - "
                       "test a limit-entry or fee-cap version")
    fm = five_min(rows, journal)
    for x in fm.get("by_strategy") or []:
        if x["confirmed_n"] >= S["idea_min_trades"] and x["all_n"] >= S["idea_min_trades"] and \
                x["all_gross_r"] - x["confirmed_r"] >= S["idea_5m_gap_r"]:
            out.append(f"{x['strategy']}: the 5m check made it worse ({x['confirmed_r']:+.2f}R confirmed vs "
                       f"{x['all_gross_r']:+.2f}R for every setup, before fees) - consider TEST alerts without it")
    return out[:8]


def five_min(rows, journal):
    """With vs without the 5m check: the watcher's TEST alerts (5m-confirmed, plan result before fees, from the
    journal) vs every TEST setup the hourly scan recorded (no 5m check, before fees = result_r + fees_r)."""
    tests = (journal or {}).get("tests") or {}
    by = {}
    for r in rows:
        if r["stage"] != "TEST" or not r.get("gross"):
            continue
        sid = r["key"].split("@")[0]
        x = by.setdefault(sid, dict(strategy=sid, all_n=0, all_sum=0.0))
        x["all_n"] += r["gross"]["n"]
        x["all_sum"] += r["gross"]["avg_r"] * r["gross"]["n"]
    out = []
    for sid, t in sorted(tests.items()):
        x = by.get(sid)
        if not x or not t.get("n"):
            continue
        out.append(dict(strategy=sid, confirmed_n=int(t["n"]), confirmed_r=round(float(t["avg_r"]), 3),
                        all_n=x["all_n"], all_gross_r=round(x["all_sum"] / x["all_n"], 3) if x["all_n"] else 0.0))
    conf_n = sum(int(t.get("n") or 0) for t in tests.values())
    conf_sum = sum(float(t.get("avg_r") or 0) * int(t.get("n") or 0) for t in tests.values())
    all_n = sum(x["all_n"] for x in by.values())
    all_sum = sum(x["all_sum"] for x in by.values())
    return dict(confirmed_n=conf_n, confirmed_r=round(conf_sum / conf_n, 3) if conf_n else None, all_n=all_n,
                all_gross_r=round(all_sum / all_n, 3) if all_n else None, by_strategy=out,
                note=None if journal else "the watcher's alerts reach GitHub only with journal sync "
                                          "(windows\\6_journal_sync.bat)")


def system_check(now, research_runs, scan_utc, program, journal, rows):
    """Idea C part 2: did every part run this week? [(ok, text)]."""
    out = []
    days = sorted({str(x.get("date")) for x in research_runs or [] if x.get("date")})
    last7 = [d for d in days if d >= (now - dt.timedelta(days=7)).strftime("%Y-%m-%d")]
    out.append((len(last7) >= 6, f"nightly research ran on {len(last7)} of the last 7 days"
                + (f" (last {days[-1]})" if days else "")))
    out.append((scan_utc is not None, f"hourly scan: last run {scan_utc or 'unknown'} UTC"))
    cells = (program or {}).get("cells") or {}
    if cells:
        fresh = sum(1 for c in cells.values() if str(c.get("tested_utc") or "") >=
                    (now - dt.timedelta(days=7)).strftime("%Y-%m-%d"))
        out.append((fresh == len(cells), f"program rotation: {fresh} of {len(cells)} strategy / timeframe tests "
                                         "re-tested in the last 7 days"))
    else:
        out.append((False, "program results: none yet (reports/program.json)"))
    if journal:
        last = journal.get("last_entry_utc")
        out.append((bool(last) and str(last) >= (now - dt.timedelta(days=2)).strftime("%Y-%m-%d"),
                    f"live watcher journal: last entry {last or 'none'} UTC"))
    else:
        out.append((None, "live watcher: journal sync off - GitHub cannot see the watcher (optional)"))
    n_week = sum(r["week"]["n"] for r in rows if r["stage"] == "TEST")
    out.append((True, f"TEST setups closed this week (GitHub record): {n_week}"))
    return [dict(ok=o, text=t) for o, t in out]


def _r(x):
    return "-" if x is None else f"{x:+.2f}R"


def render(rv):
    """reports/weekly_review.md."""
    t = rv["totals"]
    L = [f"# Weekly review · {rv['week']}", "",
         f"Made {rv['utc']} UTC by the hourly scan (engine/weekly_review.py). Live = the program's 🔵 TEST setups (the "
         "GitHub record, no 5m check) and 🟡 PAPER signals, closed, after fees unless it says before fees. "
         "Promotion to PAPER needs the operator's tap; LIVE still needs the full pass bar and the approval line.", "",
         "## System check", ""]
    L += [f"- {'✅' if s['ok'] else '⚪' if s['ok'] is None else '⚠️'} {s['text']}" for s in rv["system"]]
    L += ["", "## Totals", "",
          f"- TEST: {t['TEST']['n']} closed setups since the start, {_r(t['TEST']['avg_r'])} a trade; this week "
          f"{t['TEST']['week_n']} ({t['TEST']['week_total_r']:+.2f}R)",
          f"- PAPER: {t['PAPER']['n']} closed signals, {_r(t['PAPER']['avg_r'])} a trade; this week "
          f"{t['PAPER']['week_n']} ({t['PAPER']['week_total_r']:+.2f}R)", "", "## Promote to 🟡 PAPER (your tap)", ""]
    L += [f"{i + 1}. {p['name'] or p['key']} {p['version']} {p['tf']} on {p['coin']} - {p['why']}. {p['confidence']}."
          for i, p in enumerate(rv["promote"])] or ["None this week (each needs 10+ closed live TEST setups, positive "
                                                    "after fees, and a positive backtest on that coin)."]
    L += ["", "## In paper"]
    L += [f"- {p['key'].replace('|', ' ')} on {', '.join(p['coins'])}" for p in rv["paper"]] or ["- none"]
    if rv["demoted"]:
        L += ["", "## Demoted (back to 🔵 TEST)"] + [f"- {d['key'].replace('|', ' ')} on {d['coin']}: paper "
                                                     f"{d['avg_r']:+.2f}R over its last trades" for d in rv["demoted"]]
    if rv["refused"]:
        L += ["", "## Promotions not applied"] + [f"- {d['key'].replace('|', ' ')} on {d['coin']}: {d['why']}"
                                                  for d in rv["refused"]]
    fm = rv["five_min"]
    L += ["", "## With vs without the 5m check (before fees)", "",
          f"- watcher alerts (5m-confirmed): {fm['confirmed_n']} plan results, {_r(fm['confirmed_r'])} a trade",
          f"- every TEST setup (GitHub, no 5m check): {fm['all_n']}, {_r(fm['all_gross_r'])} a trade"]
    if fm.get("note"):
        L.append(f"- note: {fm['note']}")
    L += ["", "## Ideas for new versions", ""] + ([f"- {x}" for x in rv["ideas"]] or ["- none yet (each needs 10+ "
                                                                                   "live trades)"])
    L += ["", "## Every live strategy / version / coin", "",
          "| Strategy | TF | Coin | Stage | Live | Win % | After fees | Before fees | This week | Backtest | Confidence |",
          "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for r in sorted(rv["rows"], key=lambda r: (r["stage"] != "PAPER", -r["live"]["n"])):
        bt = r["backtest"] or {}
        L.append(f"| {r['key'].split('@')[0]} | {r['tf']} | {r['coin']} | {r['stage']} | {r['live']['n']} | "
                 f"{r['live']['win_rate']:.0f} | {_r(r['live']['avg_r'])} | "
                 f"{_r(r['gross']['avg_r']) if r.get('gross') else '-'} | {r['week']['n']} ({r['week']['total_r']:+.1f}R) | "
                 f"{_r(bt.get('avg_r'))} | {r['confidence']} |")
    if not rv["rows"]:
        L.append("| - | - | - | - | 0 | - | - | - | - | - | no closed live setup yet |")
    return "\n".join(L) + "\n"


def telegram(rv):
    """The weekly Telegram message (the watcher adds one ✅ Promote button per candidate)."""
    t = rv["totals"]
    L = [f"📊 <b>Weekly review · {rv['week']}</b>",
         f"🔵 TEST: {t['TEST']['week_n']} setups closed this week ({t['TEST']['week_total_r']:+.1f}R) · "
         f"{t['TEST']['n']} since the start ({_r(t['TEST']['avg_r'])} a trade, after fees)",
         f"🟡 PAPER: {t['PAPER']['week_n']} this week ({t['PAPER']['week_total_r']:+.1f}R)", ""]
    if rv["promote"]:
        L.append("<b>Ready for 🟡 PAPER</b> (tap to promote):")
        L += [f"{i + 1}. {p['name'] or p['key']} {p['version']} {p['tf']} · {p['coin']}\n   {p['confidence']}"
              for i, p in enumerate(rv["promote"])]
    else:
        L.append("Nothing ready for PAPER yet: each needs 10+ live TEST setups, positive after fees.")
    if rv["demoted"]:
        L += ["", "Back to 🔵 TEST (paper results below 0R): " + ", ".join(
            f"{d['key'].split('@')[0]} {d['key'].split('|')[1]} {d['coin']}" for d in rv["demoted"])]
    bad = [s["text"] for s in rv["system"] if s["ok"] is False]
    L += ["", "System check: " + ("✅ all parts ran" if not bad else "⚠️ " + "; ".join(bad))]
    if rv["ideas"]:
        L += ["", f"💡 {len(rv['ideas'])} idea(s) for new versions - in the weekly email and reports/weekly_review.md"]
    L.append("\n<i>PAPER is practice. Real-money (LIVE) signals still need 20 good paper signals and your approval.</i>")
    return "\n".join(L)
