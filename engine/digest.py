"""
The weekly email and the Claude summaries in the engine's emails (AGENT_PROMPT.md sections 19-20) - Phase 14.

  * weekly(): the [WEEKLY] email, built by the hourly scan from measured numbers only (works WITHOUT Claude):
    results of the week (LIVE / PAPER / VALIDATION kept apart), scoreboard, lifecycle changes, why trades lost,
    SMC/ICT control-twin findings, missed moves, approval packs with the yes/no question - then Claude's weekly
    research (sources, experiment queue) if the weekly task wrote it.
  * claude_summary(): the '## Summary' of a Claude review file, for the [DAILY] email.

Pure functions (files are passed in as text); no internet.
"""
import datetime as dt
import re

import pandas as pd

WEEKLY_FROM_HOUR = 4          # Sunday, first scan from 04:00 UTC (12:00 Beijing) - after Claude's weekly research
STAGES = [("APPROVED", "LIVE (approved strategies)"), ("PAPER_TRADING", "PAPER"), ("VALIDATION", "VALIDATION")]


def section(text, heading="Summary", max_lines=12):
    """The lines under '## <heading>' (until the next '## '), without empty lines at the ends."""
    out, on = [], False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            if on:
                break
            on = line[3:].strip().lower().startswith(heading.lower())
            continue
        if on:
            out.append(line.rstrip())
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out[:max_lines] + (["  (…more in the file)"] if len(out) > max_lines else [])


def claude_summary(text, path, when):
    """The daily review's summary for the [DAILY] email, clearly marked as Claude-written."""
    if text is None:
        return None
    lines = section(text, "Summary")
    return dict(file=path, date=when, lines=lines or ["(the review has no '## Summary' section - see the file)"])


def is_weekly_time(now):
    return now.weekday() == 6 and now.hour >= WEEKLY_FROM_HOUR


def week_label(now):
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def closed_between(logdf, a, b):
    """Closed signals (not NO_TRADE) whose close time is in [a, b), as records."""
    if logdf is None or logdf.empty:
        return []
    d = logdf[(logdf["status"] != "OPEN") & (logdf.get("state", pd.Series("", index=logdf.index)) != "NO_TRADE")]
    d = d.dropna(subset=["result_r", "closed_time_utc"])
    t = pd.to_datetime(d["closed_time_utc"], utc=True, errors="coerce")
    d = d[(t >= a) & (t < b)]
    return d.to_dict("records")


def results_by_stage(rows):
    out = []
    for st, label in STAGES:
        r = [float(x["result_r"]) for x in rows if x.get("stage") == st]
        out.append(dict(stage=st, label=label, n=len(r), wins=sum(v > 0 for v in r),
                        total_r=round(sum(r), 2), avg_r=round(sum(r) / len(r), 3) if r else None))
    return out


def loss_tags(rows):
    """How often each failure tag (section 17) appears on this week's losing signals."""
    cnt = {}
    for x in rows:
        if float(x["result_r"]) < 0:
            for t in str(x.get("tags") or "").split(";"):
                if t.strip() and t.strip() != "nan":
                    cnt[t.strip()] = cnt.get(t.strip(), 0) + 1
    return sorted(cnt.items(), key=lambda x: (-x[1], x[0]))


def lifecycle_between(text, a, b):
    """Lines of memory/strategy_lifecycle.md written in [a, b) (blocks start with '## YYYY-MM-DD HH:MM UTC')."""
    out, on = [], False
    for line in (text or "").splitlines():
        m = re.match(r"^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC", line)
        if m:
            t = pd.Timestamp(m.group(1), tz="UTC")
            on = a <= t < b
            continue
        if on and line.startswith("- "):
            out.append(line[2:].replace("**", ""))
    return out


def weekly(now, logdf, board, research, lifecycle_text, claude_text, claude_path):
    """The [WEEKLY] email of the week ending now (dict: week, subject, lines)."""
    a, b = pd.Timestamp(now - dt.timedelta(days=7)), pd.Timestamp(now)
    rows = closed_between(logdf, a, b)
    res = results_by_stage(rows)
    research = research or {}
    wk = week_label(now)
    live = res[0]
    subject = (f"[WEEKLY] {wk} - live {live['n']} closed ({live['total_r']:+.1f}R), "
               f"paper {res[1]['n']} closed ({res[1]['total_r']:+.1f}R)")
    L = [f"Weekly report {wk} - {a:%Y-%m-%d} to {b:%Y-%m-%d %H:%M} UTC", "",
         "1. RESULTS THIS WEEK (closed signals; LIVE, PAPER and VALIDATION are kept apart - never add them up)"]
    L += [f"  {r['label']}: {r['n']} closed, {r['wins']} won, total {r['total_r']:+.2f}R"
          + (f", average {r['avg_r']:+.2f}R" if r["avg_r"] is not None else "") for r in res]
    if sum(r["n"] for r in res) < 20:
        L.append("  Small sample - a week says little about any strategy.")
    counts = {}
    for x in board:
        counts[x["status"]] = counts.get(x["status"], 0) + 1
    L += ["", "2. STRATEGY SCOREBOARD (backtest, Layer B)",
          "  " + " · ".join(f"{k} {v}" for k, v in sorted(counts.items()))]
    top = [x for x in board if x["status"] in ("APPROVED", "PAPER_TRADING", "VALIDATION")]
    for x in sorted(top, key=lambda x: ["APPROVED", "PAPER_TRADING", "VALIDATION"].index(x["status"])):
        avg = x.get("avg_r")
        L.append(f"  - {x['strategy']} v{x['version']} {x['tf']}: {x['status']} · backtest "
                 + (f"{avg:+.2f}R over {x.get('trades')} trades" if isinstance(avg, (int, float)) and avg == avg
                    else "not researched yet")
                 + (f" · live signals {x['live_signals']}" if x.get("live_signals") else ""))
    if not top:
        L.append("  No strategy has passed the backtest bar yet - no paper or live signals. That is a result too.")
    life = lifecycle_between(lifecycle_text, a, b)
    L += ["", "3. LIFECYCLE CHANGES THIS WEEK"] + ([f"  - {x}" for x in life[:25]] or ["  none"])
    if len(life) > 25:
        L.append(f"  (+{len(life) - 25} more in memory/strategy_lifecycle.md)")
    tags = loss_tags(rows)
    L += ["", "4. WHY TRADES LOST (failure tags on this week's losing signals)"]
    L += [f"  - {t}: {n}" for t, n in tags[:10]] or ["  no losing signals this week"]
    cand = research.get("candidate_lessons") or []
    if cand:
        L.append("  Candidate lessons (systematic in 2+ backtests - a review decides):")
        L += [f"  - {c['tag']}: {c['evidence']}" for c in cand[:6]]
    smc = [x for x in board if x.get("family") == "smc" and x.get("control_twin")]
    L += ["", "5. SMC / ICT FINDINGS (does the SMC ingredient beat the same idea without it?)"]
    verdict = {True: "beats its twin", False: "does NOT beat its twin"}
    L += [f"  - {x['strategy']} v{x['version']} {x['tf']}: "
          + verdict.get(x.get("beats_twin") if isinstance(x.get("beats_twin"), bool) else
                        {"True": True, "False": False}.get(str(x.get("beats_twin"))), "too few trades to compare")
          for x in smc[:12]] or ["  no SMC strategy researched yet"]
    moves = [m for m in research.get("missed_moves") or [] if pd.Timestamp(m["start_utc"], tz="UTC") >= a]
    L += ["", "6. MISSED STRONG MOVES (5x the 1H ATR within 12 hours)"]
    if moves:
        v = {}
        for m in moves:
            v[m["verdict"]] = v.get(m["verdict"], 0) + 1
        L.append(f"  {len(moves)} moves: " + "; ".join(f"{k}: {n}" for k, n in sorted(v.items(), key=lambda x: -x[1])))
    else:
        L.append("  none recorded this week")
    appr = research.get("approval") or {}
    L += ["", "7. APPROVAL PACKS (section 21)"]
    for p in appr.get("eligible") or []:
        L += [f"  - Approve {p['strategy']} v{p['version']} {p['tf']} for live emails? (yes/no)",
              f"    paper {p['paper_signals']} signals, average {p['paper_avg_r']:+.2f}R; backtest unseen "
              f"{p['backtest_validate_avg_r']:+.2f}R. Pack: {p['pack']}",
              "    To say yes: copy the line from the pack into `approvals:` in config.yaml. No reply = no."]
    if not appr.get("eligible"):
        L.append("  none - no strategy has 20+ paper signals that meet the section 12 numbers yet")
    L += [f"  ! {w}" for w in (appr.get("warnings") or [])[:6]]
    L += ["", "8. CLAUDE'S WEEKLY RESEARCH (written by the AI - sources, ideas and the experiment queue; ideas are "
          "not evidence until backtested)"]
    if claude_text:
        body = [ln.rstrip() for ln in claude_text.splitlines()]
        L += [f"  {ln}" if ln else "" for ln in body[:150]]
        if len(body) > 150:
            L.append(f"  (…the rest is in {claude_path})")
    else:
        L.append("  Claude's weekly research is not available this week (the task did not run or was refused by "
                 "the guard). Everything above is from the engine and complete without it.")
    return dict(week=wk, subject=subject, lines=L)
