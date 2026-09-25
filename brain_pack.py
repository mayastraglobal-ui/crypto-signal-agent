#!/usr/bin/env python3
"""
The fact sheet for Claude's scheduled tasks (Phase 14; tasks/*.md).

Claude explains and researches - it never computes prices, results or statistics itself (AGENT_PROMPT.md
section 1). This prints every number a task needs, taken from the engine's own files:

  python publish_live.py --restore      (first: fetch the large report files, e.g. latest.json, research.json)
  python brain_pack.py briefing         (position book, market, signals, risk, events)
  python brain_pack.py daily            (+ last 24 hours: closed signals, losses and tags, lifecycle, reviews due,
                                          the strategy lab and the trials counter)
  python brain_pack.py weekly           (+ last 7 days, missed moves, candidate lessons, approval packs, SMC twins,
                                          the lab, the event calendar)

Read-only: it writes nothing.
"""
import datetime as dt
import json
import os
import sys

import pandas as pd

from engine import digest
from engine import memory as mem

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(ROOT, "reports")
MEMORY = os.path.join(ROOT, "memory")


def load_json(name):
    p = os.path.join(REPORTS, name)
    return json.load(open(p)) if os.path.exists(p) else None


def read(path):
    return open(path, encoding="utf-8", errors="replace").read() if os.path.exists(path) else None


def recent_files(folder, n=3):
    d = os.path.join(REPORTS, "claude", folder)
    names = sorted(x for x in os.listdir(d) if x.endswith(".md")) if os.path.isdir(d) else []
    return [f"reports/claude/{folder}/{x}" for x in names[-n:]]


def fmt_r(x):
    return "-" if x is None or x != x else f"{float(x):+.2f}R"


def target(kind, now):
    """Where this run's output goes (the Brain guard only accepts these names).
    briefing: Beijing date + the nearest slot 0820 / 1420 / 2120; daily and weekly: the UTC date (the morning
    [DAILY] email reads yesterday's review, the Sunday [WEEKLY] email reads that Sunday's research)."""
    if kind == "briefing":
        bj = now + dt.timedelta(hours=8)
        mins = bj.hour * 60 + bj.minute
        slot = min(("0820", 500), ("1420", 860), ("2120", 1280), key=lambda s: abs(mins - s[1]))[0]
        return f"reports/claude/briefings/{bj:%Y-%m-%d}-{slot}.md"
    return f"reports/claude/{kind}/{now:%Y-%m-%d}.md"


def calendar_lines(now, days=90):
    """events.yaml as the weekly task needs it: what is listed for the next 90 days, how each date was checked,
    and which months have no NFP / CPI / PCE / FOMC entry yet."""
    from engine import risk as rk
    out = ["", f"## Event calendar (events.yaml) - next {days} days, and what looks missing"]
    try:
        items = rk.load_calendar(os.path.join(ROOT, rk.CALENDAR_FILE))
    except ValueError as e:
        return out + [f"- ! {e}"]
    t0, t1 = now.strftime("%Y-%m-%d"), (now + dt.timedelta(days=days)).strftime("%Y-%m-%d")
    listed = [e for e in items if t0 <= str(e.get("utc", ""))[:10] <= t1]
    out += [f"- {e.get('utc')} UTC {e.get('type')}: {e.get('name')} (check: {e.get('check', '-')})" for e in listed] \
        or ["- nothing listed"]
    months = sorted({(now + dt.timedelta(days=d)).strftime("%Y-%m") for d in range(0, days + 1, 7)}
                    - {now.strftime("%Y-%m")})             # the current month may already be past its releases
    for m in months:
        have = {e.get("type") for e in items if str(e.get("utc", "")).startswith(m)}
        miss = [t for t in ("NFP", "CPI", "PCE") if t not in have]
        if miss:
            out.append(f"- {m}: no {', '.join(miss)} entry yet (FOMC meets 8 times a year - check its calendar)")
    return out


def lab_lines(now, research):
    """Phase 17: where candidates go (strategies_lab.yaml), how many may still be added, what exists already, the
    trials counter, and how the lab cards are doing."""
    import yaml
    from engine import brain
    from engine import strategy_spec as sspec
    out = ["", "## Strategy lab (strategies_lab.yaml) - where your candidate cards go"]
    try:
        lab = brain._cards(read(os.path.join(ROOT, sspec.LAB_FILE)))
        lib = brain._cards(read(os.path.join(ROOT, sspec.LIBRARY_FILE)))
    except (yaml.YAMLError, ValueError) as e:
        return out + [f"- ! the lab or library file is not readable ({e}) - add no card, say so in your output"]
    days = [brain._day(c.get("added")) for c in lab if isinstance(c, dict)]
    today = now.date()
    n_day = sum(d == today for d in days)
    n_week = sum(d is not None and today - dt.timedelta(days=6) <= d <= today for d in days)
    left = max(0, min(brain.LAB_PER_DAY - n_day, brain.LAB_PER_WEEK - n_week))
    out += [f"- cards in the lab: {len(lab)} · added today: {n_day} of {brain.LAB_PER_DAY} · last 7 days: {n_week} of "
            f"{brain.LAB_PER_WEEK} · you may add at most {left} card(s) now (a control twin counts)",
            f"- write each card with added: \"{today}\", status: FORMALIZED, evidence_class, source, targets (first "
            f">= {sspec.MIN_TP1_R:g}R), a changelog line, and a control twin (twin_of) for an SMC / 5m ingredient"]
    latest = {}
    for c, where in [(c, "library") for c in lib] + [(c, "lab") for c in lab]:
        if isinstance(c, dict) and c.get("id"):
            old = latest.get(c["id"])
            try:
                if old is None or sspec._vkey(c.get("version")) > sspec._vkey(old[0]):
                    latest[c["id"]] = (str(c.get("version")), where)
            except ValueError:
                pass
    out += ["- existing ids (latest version): " + "; ".join(f"{k} v{v} ({w})" for k, (v, w) in sorted(latest.items()))]
    tr = (research or {}).get("trials")
    out += [f"- trials counter: {tr['total']} tests so far; PAPER_TRADING needs t >= {tr['need_t']:.2f} - every new "
            "card raises this bar for all" if tr else "- trials counter: not available yet (next research run)"]
    cells = [(k, c) for k, c in ((research or {}).get("cells") or {}).items() if c.get("lab")]
    out += [f"- lab cell {k}: {c['status']} · {c['evidence']['all']['n']} trades, {fmt_r(c['evidence']['all']['avg_r'])}"
            f" · t {c.get('t_stat') if c.get('t_stat') is not None else '-'}" for k, c in sorted(cells)[:30]] \
        or ["- no lab card has been researched yet"]
    return out


def pack(kind, now):
    rep, research = load_json("latest.json"), load_json("research.json")
    out = [f"# Fact sheet for the {kind} task - {now:%Y-%m-%d %H:%M} UTC",
           "All numbers below come from the engine. Quote them; never recompute or invent numbers.",
           f"WRITE YOUR OUTPUT TO: {target(kind, now)}", ""]
    if rep is None:
        return out + ["reports/latest.json is missing - run `python publish_live.py --restore` first. "
                      "If it is still missing, say in your output that the engine report was not available."]
    age_h = (now - pd.Timestamp(rep["generated_utc"], tz="UTC").to_pydatetime()).total_seconds() / 3600
    out += [f"Engine report: {rep['generated_utc']} UTC ({age_h:.1f} hours old)"
            + (" - STALE: say so, the hourly scan may have failed" if age_h > 2.5 else ""),
            f"Data state: {rep['daily'].get('data_state', '?')}", "", "## Position book (copy as is)"]
    out += rep.get("position_book_text") or ["(none)"]
    out += ["", "## Market, top coins, strategy health, event calendar (the engine's daily block)"]
    out += (rep.get("daily_lines") or [])[1:]
    out += ["", "## Signals this run"]
    sig = rep.get("signals") or []
    out += [f"- LIVE {(p.get('email') or {}).get('subject') or p['coin'] + ' ' + p['direction']}: entry {p.get('entry')}, "
            f"stop {p.get('stop')}, targets {', '.join(str(t['price']) for t in p.get('targets') or [])}"
            for p in sig] or ["- no live signal"]
    vs = rep.get("validation_signals") or []
    out += [f"- {len(vs)} paper / validation signal(s) (logged, not emailed): "
            + "; ".join(f"{p['coin']} {p['direction']} {p['timeframe']} {p['strategy']} ({p.get('stage')})" for p in vs[:10])]
    out += [f"- watching (not signals): " + ("; ".join(f"{w['coin']} {w['direction']} {w['tf']} {w['strategy']} "
                                                       f"{w['state']} ({w['stage']})" for w in (rep.get('watching') or [])[:10])
                                             or "none")]
    risk = rep.get("risk") or {}
    out += ["", "## Risk engine", f"- halts: {'; '.join(risk.get('halts_text') or []) or 'none'}",
            f"- suspended strategies: {', '.join(map(str, risk.get('suspended') or [])) or 'none'}",
            f"- next events: {'; '.join(map(str, risk.get('upcoming_events') or [])) or 'none listed'}"
            + (f" (! {risk['calendar_warning']})" if risk.get("calendar_warning") else "")]
    if kind == "briefing":
        out += ["", "## Your earlier outputs (read the newest for continuity)"] + [f"- {p}" for p in
                                                                                    recent_files("briefings", 2)]
        return out

    days = 1 if kind == "daily" else 7
    a, b = pd.Timestamp(now - dt.timedelta(days=days)), pd.Timestamp(now)
    logp = os.path.join(REPORTS, "signals_log.csv")
    logdf = pd.read_csv(logp, dtype=str) if os.path.exists(logp) else pd.DataFrame()
    rows = digest.closed_between(logdf, a, b)
    out += ["", f"## Closed signals, last {days} day(s) (LIVE / PAPER / VALIDATION kept apart)"]
    out += [f"- {r['label']}: {r['n']} closed, {r['wins']} won, total {r['total_r']:+.2f}R" for r in digest.results_by_stage(rows)]
    out += [f"  - {x['coin']} {x['tf']} {x['strategy']} v{x.get('version')} {x.get('direction')} ({x.get('stage')}): "
            f"{fmt_r(float(x['result_r']))} {x.get('close_reason') or ''} · tags: {x.get('tags') or '-'} · "
            f"MAE {x.get('mae_r') or '-'} MFE {x.get('mfe_r') or '-'}" for x in rows[:40]]
    exp = logdf[logdf["state"].isin(["EXPIRED", "INVALIDATED", "NO_TRADE"])] if not logdf.empty and "state" in logdf else []
    if len(exp):
        t = pd.to_datetime(exp["signal_time_utc"], utc=True, errors="coerce")
        exp = exp[(t >= a) & (t < b)]
        out += [f"- {x['state']}: {x['coin']} {x['tf']} {x['strategy']} - {x.get('state_note') or ''}"
                for x in exp.to_dict("records")[:20]]
    out += ["", "## Failure tags on losing signals"] + ([f"- {t}: {n}" for t, n in digest.loss_tags(rows)] or ["- none"])
    life = digest.lifecycle_between(read(os.path.join(MEMORY, "strategy_lifecycle.md")), a, b)
    out += ["", f"## Lifecycle changes, last {days} day(s)"] + ([f"- {x}" for x in life[:40]] or ["- none"])
    research = research or {}
    out += ["", f"## Daily research run: {research.get('run_utc', 'not available')}"]
    out += ["### Candidate lessons (systematic in 2+ backtests)"] + (
        [f"- {c['tag']}: {c['evidence']} ({', '.join(c['cells'][:6])})" for c in research.get("candidate_lessons") or []]
        or ["- none"])
    moves = [m for m in research.get("missed_moves") or [] if pd.Timestamp(m["start_utc"], tz="UTC") >= a]
    out += ["### Missed strong moves"] + ([f"- {m['coin']} {m['direction']} {m['size_atr']}x ATR from {m['start_utc']} "
                                          f"(regime before: {m.get('regime')}): {m['verdict']}" for m in moves[:20]]
                                         or ["- none in this period"])
    failing = [(k, c) for k, c in (research.get("cells") or {}).items()
               if c["status"] in ("FAILED", "BACKTESTING") and c["evidence"]["all"]["n"] >= 30]
    out += ["### Failing strategy cells with 30+ backtest trades (diagnosis from engine/attribution.py)"]
    for k, c in sorted(failing, key=lambda x: x[1]["evidence"]["all"]["avg_r"])[:12]:
        att = c.get("attribution") or {}
        out += [f"- {k}: {c['evidence']['all']['n']} trades, {fmt_r(c['evidence']['all']['avg_r'])}; systematic tags: "
                f"{', '.join(att.get('systematic') or []) or 'none'}"] + [f"  - {d}" for d in (att.get("diagnosis") or [])[:4]]
    appr = research.get("approval") or {}
    out += ["### Approval packs"] + ([f"- {p['key']}: {p['pack']}" for p in appr.get("eligible") or []] or ["- none eligible"])
    out += [f"- ! {w}" for w in appr.get("warnings") or []]
    if kind == "weekly":
        cells = research.get("cells") or {}
        out += ["### Control-twin comparisons (does the special ingredient add anything?)"]
        out += [f"- {k}: {'beats' if c.get('beats_twin') else 'does not beat' if c.get('beats_twin') is False else 'too few trades vs'} "
                f"its twin" for k, c in sorted(cells.items()) if c.get("beats_twin") is not None or c.get("twin_same_window")][:30]
    out += lab_lines(now, research)
    if kind == "weekly":
        out += calendar_lines(now)
    st = mem.status(MEMORY, now)
    out += ["", "## Memory reviews due (write a NEW review record for each; never edit the old one)"]
    out += [f"- {d['file']}: {d['title']} (due {d['review']})" for d in st["due"][:30]] or ["- none"]
    lessons = mem.parse(read(os.path.join(MEMORY, "lessons.md")) or "")
    out += ["", "## Existing lessons"] + ([f"- {r['title']} ({r.get('evidence')})" for r in lessons] or ["- none yet"])
    out += ["", "## Your earlier outputs (read them first)"] + [f"- {p}" for p in
                                                                 recent_files("daily") + recent_files("weekly", 2)]
    return out


def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "briefing"
    if kind not in ("briefing", "daily", "weekly"):
        sys.exit("usage: python brain_pack.py briefing|daily|weekly")
    print("\n".join(pack(kind, dt.datetime.now(dt.timezone.utc))))


if __name__ == "__main__":
    main()
