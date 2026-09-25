"""
The agent's weekly report card (Phase 17 D, item 11) - measured from the engine's own files, so it works even when
Claude did not run. Shown in the [WEEKLY] email and in the weekly research task's fact sheet.

  1  ideas researched          new research_sources records and new lab cards this week (by factory)
  2  lab cards tested          lab strategy/timeframe cells tested for the first time this week (trials.csv)
  3  pass rate per factory     lab cells that reached VALIDATION or better, per idea factory
  4  idea -> test result       days from a lab card's `added` date to its first research test (median, max)
  5  backtest vs paper gap     paper average R minus the backtest's unseen-data average R (5+ paper signals)
  6  late / false signals      late = expired before entry or tagged late_entry; false = lost without ever
                               reaching +0.25R (MFE) - PAPER and LIVE kept apart
  7  missed moves              strong moves this week and whether any strategy caught them
  8  pages that failed         news feeds that failed + the pages Claude's tasks listed as not opened
  9  Claude task runs          runs expected vs delivered, refused pushes, run time (from each output's run log)
 10  lab slots                 cards used vs allowed per factory this week
 11  process improvement       ONE proposal by the weekly research ("## Process improvement"), for the operator

Pure functions (files are passed in as text / data).
"""
import datetime as dt
import re
import statistics

import pandas as pd

from engine import strategy_spec as sspec
from engine import trials as trl

EXPECTED_RUNS = {"briefings": 21, "daily": 7, "weekly": 1}        # per week: 3 briefings a day, 1 daily, 1 weekly
RUN_RE = re.compile(r"started (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC.*?finished (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC")


def _day(x):
    try:
        return dt.date.fromisoformat(str(x)[:10])
    except ValueError:
        return None


def section(text, heading):
    """Lines under '## <heading>...' until the next '## ' (empty lines dropped)."""
    out, on = [], False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            on = line[3:].strip().lower().startswith(heading.lower())
            continue
        if on and line.strip():
            out.append(line.rstrip())
    return out


def ideas_researched(sources_text, lab, a, b):
    """Records added to research_sources.md and lab cards added in [a, b) (dates)."""
    recs = [r for r in _records(sources_text) if _day(r) and a <= _day(r) < b]
    cards = [c for c in lab if isinstance(c, dict) and _day(c.get("added")) and a <= _day(c.get("added")) < b]
    by_f = {}
    for c in cards:
        by_f[c.get("factory") or "-"] = by_f.get(c.get("factory") or "-", 0) + 1
    return dict(sources=len(recs), cards=len(cards), by_factory=by_f)


def _records(text):
    return re.findall(r"^- timestamp: (\d{4}-\d{2}-\d{2})", text or "", flags=re.M)


def idea_to_test(lab, trial_rows):
    """Days from each lab card's `added` date to the first research test of any of its timeframes."""
    first = {}
    for r in trial_rows:
        k = f"{r['strategy']}@{r['version']}"
        d = _day(r.get("first_tested_utc"))
        if d and (k not in first or d < first[k]):
            first[k] = d
    days, waiting = [], []
    for c in lab:
        if not isinstance(c, dict) or not _day(c.get("added")):
            continue
        k = f"{c.get('id')}@{c.get('version')}"
        if k in first:
            days.append((first[k] - _day(c["added"])).days)
        else:
            waiting.append(k)
    return dict(n=len(days), median=statistics.median(days) if days else None, max=max(days) if days else None,
                waiting=waiting)


def paper_gap(cells, min_n=5):
    """Paper average R vs the backtest's unseen-data average R, per cell with enough paper signals."""
    rows = []
    for ck, c in (cells or {}).items():
        p, v = c.get("paper") or {}, (c.get("evidence") or {}).get("validate") or {}
        if (p.get("n") or 0) >= min_n and p.get("avg_r") is not None and v.get("n"):
            rows.append(dict(cell=ck, paper_n=p["n"], paper=round(p["avg_r"], 3), backtest=v["avg_r"],
                             gap=round(p["avg_r"] - v["avg_r"], 3)))
    return sorted(rows, key=lambda x: x["gap"])


def late_false(logdf, a, b):
    """Signals of the week: late (expired before entry, or tagged late_entry) and false (closed at a loss without
    ever reaching +0.25R), per stage."""
    out = {}
    if logdf is None or logdf.empty:
        return out
    t = pd.to_datetime(logdf["signal_time_utc"], utc=True, errors="coerce")
    d = logdf[(t >= a) & (t < b)]
    for stage, g in d.groupby(d["stage"].fillna("-")):
        late = int(((g["state"] == "EXPIRED") | g["tags"].fillna("").str.contains("late_entry")).sum())
        r = pd.to_numeric(g["result_r"], errors="coerce")
        mfe = pd.to_numeric(g["mfe_r"], errors="coerce")
        closed = r.notna()
        false = int((closed & (r < 0) & (mfe.fillna(0) < 0.25)).sum())
        out[stage] = dict(signals=int(len(g)), closed=int(closed.sum()), late=late, false=false)
    return out


def failed_pages(feeds, claude_texts):
    """News feed sources that failed now + the pages Claude's outputs listed under '## Pages that failed'."""
    feed = [f"{k}: {v.get('error')}" for k, v in ((feeds or {}).get("sources") or {}).items() if v.get("status") != "ok"]
    pages = [ln.strip("- ").strip() for t in claude_texts for ln in section(t, "Pages that failed")
             if ln.strip("- ").strip().lower() not in ("none", "-", "")]
    return dict(feeds=feed, pages=pages)


def task_runs(files, runs_rows, a, b):
    """files: {kind: {path: text}} of Claude outputs dated in the week; runs_rows: reports/claude/runs.csv rows.
    Delivered vs expected, refused pushes, run minutes from each output's '## Run log' line."""
    out = {}
    for kind, exp in EXPECTED_RUNS.items():
        texts = files.get(kind) or {}
        mins, errors = [], 0
        for t in texts.values():
            log = " ".join(section(t, "Run log"))
            m = RUN_RE.search(log)
            if m:
                d = (pd.Timestamp(m.group(2)) - pd.Timestamp(m.group(1))).total_seconds() / 60
                if 0 <= d < 24 * 60:
                    mins.append(d)
            errors += bool(re.search(r"usage limit|rate limit|timed? ?out|error", log, re.I))
        out[kind] = dict(expected=exp, delivered=len(texts), minutes_median=round(statistics.median(mins))
                         if mins else None, run_logs=len(mins), reported_problems=errors)
    refused = [r for r in runs_rows if r.get("status") == "rejected" and _day(r.get("when"))
               and a <= _day(r["when"]) < b]
    out["refused_pushes"] = len(refused)
    return out


def lab_slots(lab, quota, today):
    """Cards per factory in the 7 days up to today vs the factory's quota."""
    q = dict(sspec.DEFAULT_QUOTA, **(quota or {}))
    used = {f: 0 for f in q}
    for c in lab:
        d = _day(c.get("added")) if isinstance(c, dict) else None
        if d and today - dt.timedelta(days=6) <= d <= today and c.get("factory") in used:
            used[c["factory"]] += 1
    return {f: dict(used=used[f], allowed=int(q[f])) for f in q}


def build(now, research, logdf, lab, trials_text, sources_text, feeds, claude_files, runs_rows, quota,
          weekly_text=None):
    """The whole report card as data (JSON-ready)."""
    a, b = (now - dt.timedelta(days=7)).date(), now.date() + dt.timedelta(days=1)
    ta, tb = pd.Timestamp(now - dt.timedelta(days=7)), pd.Timestamp(now)
    rows = trl.parse(trials_text)
    lab_keys = {f"{c.get('id')}@{c.get('version')}" for c in lab if isinstance(c, dict)}
    tested = [r for r in rows if f"{r['strategy']}@{r['version']}" in lab_keys and _day(r.get("first_tested_utc"))
              and a <= _day(r["first_tested_utc"]) < b]
    moves = [m for m in (research or {}).get("missed_moves") or [] if pd.Timestamp(m["start_utc"], tz="UTC") >= ta]
    verdicts = {}
    for m in moves:
        verdicts[m["verdict"]] = verdicts.get(m["verdict"], 0) + 1
    proposal = section(weekly_text, "Process improvement")
    return dict(
        week_from=str(a), week_to=str(now.date()),
        ideas=ideas_researched(sources_text, lab, a, b), lab_cells_tested=len(tested),
        factories=(research or {}).get("factories") or {}, idea_to_test=idea_to_test(lab, rows),
        paper_gap=paper_gap((research or {}).get("cells")), signals=late_false(logdf, ta, tb),
        missed=dict(n=len(moves), verdicts=verdicts), failed=failed_pages(feeds, [t for k in claude_files.values()
                                                                               for t in k.values()]),
        runs=task_runs(claude_files, runs_rows, a, b), slots=lab_slots(lab, quota, now.date()),
        proposal=proposal[:8])


def lines(rc):
    """The report card as plain lines for the email / fact sheet."""
    i = rc["ideas"]
    L = [f"AGENT REPORT CARD ({rc['week_from']} to {rc['week_to']}) - measured by the engine",
         f"  1. Ideas researched: {i['sources']} new source record(s), {i['cards']} new lab card(s)"
         + (" (" + ", ".join(f"{k} {v}" for k, v in sorted(i["by_factory"].items())) + ")" if i["by_factory"] else ""),
         f"  2. Lab cards tested: {rc['lab_cells_tested']} new strategy/timeframe test(s) of lab cards"]
    f = [f"{k} {v['passed']}/{v['cells']}" for k, v in rc["factories"].items() if v.get("cells")]
    L.append("  3. Pass rate per factory (reached VALIDATION or better): " + ("; ".join(f) or "nothing tested yet"))
    t = rc["idea_to_test"]
    L.append("  4. Idea -> test result: " + (f"median {t['median']} day(s), longest {t['max']} ({t['n']} cards)"
                                             if t["n"] else "no lab card tested yet")
             + (f"; {len(t['waiting'])} card(s) not tested yet" if t["waiting"] else ""))
    g = rc["paper_gap"]
    L.append("  5. Backtest vs paper gap: " + ("; ".join(f"{x['cell']} paper {x['paper']:+.2f}R vs backtest "
                                                       f"{x['backtest']:+.2f}R (gap {x['gap']:+.2f}R, {x['paper_n']} "
                                                       "signals)" for x in g[:4])
                                             or "no cell with 5+ closed paper signals yet"))
    s = rc["signals"]
    L.append("  6. Late / false signals: " + ("; ".join(f"{k}: {v['signals']} signals, {v['late']} late, {v['false']}"
                                                       f" false of {v['closed']} closed" for k, v in sorted(s.items()))
                                            or "no signals this week"))
    m = rc["missed"]
    L.append(f"  7. Missed strong moves: {m['n']}" + (" - " + "; ".join(f"{k}: {n}" for k, n in m["verdicts"].items())
                                                      if m["verdicts"] else ""))
    fp = rc["failed"]
    L.append(f"  8. Pages that failed to open: {len(fp['feeds'])} feed source(s) now, {len(fp['pages'])} page(s) "
             "listed by Claude's tasks" + (" - " + "; ".join((fp["feeds"] + fp["pages"])[:5]) if fp["feeds"] or
                                           fp["pages"] else ""))
    r = rc["runs"]
    L.append("  9. Claude task runs: " + "; ".join(
        f"{k} {v['delivered']}/{v['expected']}" + (f" (~{v['minutes_median']} min)" if v["minutes_median"] else "")
        + (f", {v['reported_problems']} reported a problem" if v["reported_problems"] else "")
        for k, v in r.items() if isinstance(v, dict)) + f"; {r['refused_pushes']} push(es) refused by the guard"
             + " (missing runs = not run, usage limit or refused)")
    L.append("  10. Lab slots this week: " + ", ".join(f"{k} {v['used']}/{v['allowed']}" for k, v in rc["slots"].items()))
    L.append("  11. The agent's process improvement for itself (you decide - reply or change it by pull request):")
    L += [f"      {x}" for x in rc["proposal"]] or ["      none proposed this week (the weekly research did not run or "
                                                     "wrote no '## Process improvement' section)"]
    return L


def collect(root, now, research, logdf):
    """Reads the files the report card needs (the only function here that touches files) and builds it."""
    import csv
    import json
    import os

    import yaml

    def text(*p):
        full = os.path.join(root, *p)
        if not os.path.exists(full):
            return None
        with open(full, encoding="utf-8", errors="replace") as f:
            return f.read()
    try:
        lab = [c for c in (yaml.safe_load(text(sspec.LAB_FILE) or "") or []) if isinstance(c, dict)]
    except yaml.YAMLError:
        lab = []
    try:
        cfg = yaml.safe_load(text("config.yaml") or "") or {}
    except yaml.YAMLError:
        cfg = {}
    try:
        feeds = json.loads(text("reports", "feeds.json") or "null")
    except ValueError:
        feeds = None
    a = (now - dt.timedelta(days=7)).date()
    files = {}
    for kind in EXPECTED_RUNS:
        d = os.path.join(root, "reports", "claude", kind)
        for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            day = _day(name[:10])
            if name.endswith(".md") and day and a <= day <= now.date():
                files.setdefault(kind, {})[name] = text("reports", "claude", kind, name)
    runs_txt = text("reports", "claude", "runs.csv")
    runs = list(csv.DictReader(runs_txt.splitlines())) if runs_txt else []
    return build(now, research, logdf, lab, text("memory", "trials.csv"), text("memory", "research_sources.md"),
                 feeds, files, runs, (cfg.get("lab") or {}).get("factory_quota"),
                 text("reports", "claude", "weekly", f"{now:%Y-%m-%d}.md"))
