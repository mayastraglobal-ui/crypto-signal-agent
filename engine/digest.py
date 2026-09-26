"""
The weekly email and the Claude summaries in the engine's emails (AGENT_PROMPT.md sections 19-20) - Phase 14.

  * weekly(): the numbers of the WEEKLY email (engine/emails.py, format v2), built by the hourly scan from measured
    numbers only (works WITHOUT Claude): results of the week (LIVE / PAPER / VALIDATION kept apart), lifecycle
    changes, strong moves, failure tags. The older text email that lived here was removed with format v2.

Pure functions (files are passed in as text); no internet.
"""
import datetime as dt
import re

import pandas as pd


WEEKLY_FROM_HOUR = 4          # Sunday, first scan from 04:00 UTC (12:00 Beijing) - after Claude's weekly research
STAGES = [("APPROVED", "LIVE (approved strategies)"), ("PAPER_TRADING", "PAPER"), ("VALIDATION", "VALIDATION")]


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


def weekly(now, logdf, research, lifecycle_text):
    """The numbers of the week ending now for the WEEKLY email (engine/emails.py weekly, format v2): results by
    stage (LIVE, PAPER and VALIDATION kept apart - never added up), lifecycle changes, strong moves, failure tags."""
    a, b = pd.Timestamp(now - dt.timedelta(days=7)), pd.Timestamp(now)
    rows = closed_between(logdf, a, b)
    moves = [m for m in (research or {}).get("missed_moves") or [] if pd.Timestamp(m["start_utc"], tz="UTC") >= a]
    return dict(week=week_label(now), results=results_by_stage(rows), lifecycle=lifecycle_between(lifecycle_text, a, b),
                missed_moves=moves, loss_tags=loss_tags(rows))
