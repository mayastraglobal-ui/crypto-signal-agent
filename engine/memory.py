"""
Memory files (AGENT_PROMPT.md section 22) - Phase 13.

  * one record format for the knowledge files: every entry carries timestamp, source, evidence, confidence,
    strategy/version, asset, timeframe, regime and review date
  * file headers (what the file is, who writes it, the format) so every section 22 file exists
  * reviews due (records whose review date has passed) and a status per file for the report
  * the append-only rule (section 17: never overwrite or delete results, experiments or losses) as a check

The engine writes FACTS only. Interpretation (lessons, coin behaviour) comes from the reviews (Claude,
Phase 14) or the operator. Pure functions + small file helpers; no internet.
"""
import datetime as dt
import os
import re

FIELDS = ["timestamp", "source", "evidence", "confidence", "strategy", "asset", "timeframe", "regime", "review"]
EVIDENCE_CLASSES = ["FACT", "RESEARCH_FINDING", "BACKTEST_EVIDENCE", "CLAIM", "HYPOTHESIS", "MODEL_OUTPUT",
                    "UNVERIFIED_OPINION"]            # section 18
DEFAULT_REVIEW_DAYS = dict(lessons=30, coin_notes=30, research_sources=90, failure_journal=7, missed_trades=7,
                           execution_notes=30)
RECORD_RULE = ("Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · "
               "confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` "
               "(section 22), then its details. `-` = not applicable.")
HEADERS = {
    "failure_journal.md": (
        "# Failure journal\n\nAppend-only (AGENT_PROMPT.md section 17), written by the engine. One entry per logged "
        "signal (validation / paper / live) that closed with a loss. Tags are measured by fixed rules "
        "(`engine/attribution.py`); root causes and fixes are added by the reviews - never by changing rules "
        "mid-trade. MAE / MFE = worst / best point of the trade, in R.\n"),
    "missed_trades.md": (
        "# Missed trades\n\nAppend-only (AGENT_PROMPT.md section 17.4), written by the daily research run. A strong "
        "move = at least 5x the 1H ATR within 12 hours on a research coin. For each: did any strategy have a signal "
        "before it started - and if it was filtered out, by what? **Never change a rule just because a missed move "
        "became large.**\n"),
    "lessons.md": (
        "# Lessons\n\nAppend-only (AGENT_PROMPT.md section 17.7). Only VALIDATED lessons, each with evidence counts "
        "(how many strategy / timeframe tests, how many trades, which samples). Written by the reviews (Claude, "
        "Phase 14) or the operator - **never by the engine automatically**. Candidate lessons (a tag that is "
        "systematic in 2 or more tests) are listed in the report (section 3d) until a review decides. Single stories "
        "and opinions are not lessons. A lesson that stops holding gets a NEW record (status REJECTED), the old one "
        "stays.\n"),
    "research_sources.md": (
        "# Research sources\n\nAppend-only (AGENT_PROMPT.md section 18). Every source behind a strategy idea: title, "
        "URL (only if known - **citations are never invented**), date, claim, evidence class (FACT · "
        "RESEARCH_FINDING · BACKTEST_EVIDENCE · CLAIM · HYPOTHESIS · MODEL_OUTPUT · UNVERIFIED_OPINION), derived "
        "hypothesis and limitations. The engine adds one record when a strategy version is first tested (from its "
        "card); the reviews add external sources. Test results live in `memory/strategy_registry.csv`.\n"),
    "coin_notes.md": (
        "# Coin notes\n\nAppend-only. How each signal coin tends to behave. The engine adds one block of measured "
        "FACTS per coin every week (first scan on Sunday, UTC): daily range, time spent in each regime, which coins "
        "it moves with, volume, which strategies were profitable on it. Interpretation is added by the reviews.\n"),
    "execution_notes.md": (
        "# Execution notes\n\nAppend-only. Observed data problems, fees and slippage. The engine records data problems "
        "when they START and when they END (not every hour), and every change of the fee settings. Slippage: the "
        "agent never trades, so there are no real fills yet - backtests use the configured slippage.\n"),
}
# files that may only grow (section 17: never overwrite or delete results, experiments or losses)
APPEND_ONLY = ["memory/changelog.md", "memory/experiments.md", "memory/strategy_lifecycle.md", "memory/universe_log.md",
               "memory/market_regime_log.md", "memory/smc_events.csv", "memory/failure_journal.md",
               "memory/missed_trades.md", "memory/lessons.md", "memory/research_sources.md", "memory/coin_notes.md",
               "memory/execution_notes.md", "reports/position_events.csv", "memory/trials.csv", "strategies_lab.yaml"]
LINE_RE = re.compile(r"^- timestamp: (.*)$")


def review_days(section, kind):
    days = dict(DEFAULT_REVIEW_DAYS)
    days.update((section or {}).get("review_days") or {})
    return int(days[kind])


def record(title, body=(), **fields):
    """One section 22 record as markdown. Unknown / empty fields are written as '-'."""
    bad = set(fields) - set(FIELDS)
    if bad:
        raise ValueError(f"unknown record fields {sorted(bad)}")
    ev = str(fields.get("evidence") or "")
    if ev and ev.split(":")[0].split(" ")[0] not in EVIDENCE_CLASSES:
        raise ValueError(f"evidence must start with a class {EVIDENCE_CLASSES}: {ev!r}")
    vals = [str(fields.get(k)) if fields.get(k) not in (None, "") else "-" for k in FIELDS]
    head = "- " + " · ".join(f"{k}: {v.replace(' · ', ', ')}" for k, v in zip(FIELDS, vals))
    return "\n".join([f"\n### {title}", head, *[f"  {b}" for b in body]]) + "\n"


def parse(text):
    """Records in a file's text: [dict(title, <fields>)] (older non-record entries are ignored)."""
    out, title = [], None
    for line in text.splitlines():
        if line.startswith("### "):
            title = line[4:].strip()
            continue
        m = LINE_RE.match(line)
        if m and title is not None:
            rec = dict(title=title)
            for part in line[2:].split(" · "):
                k, _, v = part.partition(": ")
                rec[k.strip()] = v.strip()
            out.append(rec)
            title = None
    return out


def ensure(memory_dir, names=None):
    """Create the knowledge files that do not exist yet, with their header. Returns the files created."""
    os.makedirs(memory_dir, exist_ok=True)
    made = []
    for name in names or HEADERS:
        p = os.path.join(memory_dir, name)
        if not os.path.exists(p):
            with open(p, "w") as f:
                f.write(HEADERS[name] + "\n" + RECORD_RULE + "\n")
            made.append(name)
    return made


def append(memory_dir, name, text):
    ensure(memory_dir, [name])
    with open(os.path.join(memory_dir, name), "a") as f:
        f.write(text)


def plus_days(now, days):
    return (now + dt.timedelta(days=days)).strftime("%Y-%m-%d")


def status(memory_dir, now):
    """Per memory file: size, number of section 22 records, newest record time; plus the reviews due."""
    files, due = [], []
    today = now.strftime("%Y-%m-%d")
    for name in sorted(os.listdir(memory_dir)) if os.path.isdir(memory_dir) else []:
        p = os.path.join(memory_dir, name)
        if not os.path.isfile(p):
            continue
        with open(p, errors="replace") as f:
            text = f.read()
        recs = parse(text) if name.endswith(".md") else []
        files.append(dict(file=name, kb=round(os.path.getsize(p) / 1024, 1), records=len(recs),
                          last=max((r.get("timestamp", "") for r in recs), default=None)))
        for r in recs:
            rv = r.get("review", "-")
            if re.match(r"^\d{4}-\d{2}-\d{2}$", rv) and rv <= today:
                due.append(dict(file=name, title=r["title"], review=rv))
    missing = sorted(set(HEADERS) - {f["file"] for f in files})
    return dict(files=files, due=sorted(due, key=lambda d: d["review"]), missing=missing)


def append_only_problems(old_text, new_text):
    """'' when new_text keeps old_text unchanged at its start (only additions), else what went wrong."""
    if old_text is None:
        return ""
    if new_text is None:
        return "the file was deleted"
    if new_text.startswith(old_text):
        return ""
    a, b = old_text.splitlines(), new_text.splitlines()
    for i, (x, y) in enumerate(zip(a, b), 1):
        if x != y:
            return f"line {i} was changed"
    return f"lines {len(b) + 1}-{len(a)} were removed" if len(b) < len(a) else "the last line was changed"
