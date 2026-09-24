"""
The Brain guard (AGENT_PROMPT.md sections 1, 17, 22, 25) - Phase 14.

Claude's scheduled tasks (briefings, daily review, weekly research - tasks/*.md) never write to main. Each task
pushes its work to its own branch (claude/brain-briefing, claude/brain-daily, claude/brain-weekly). The Brain
workflow (brain.yml, always run from main) checks every change with review() below and copies only what is
allowed onto the newest main:

  * NEW text files in reports/claude/briefings|daily|weekly/ with the expected file name
  * ADDITIONS at the end of the knowledge files (lessons, failure journal, missed trades, research sources,
    coin notes, feature notes, SMC research, experiments), written as section 22 records

Everything else is refused - code, config.yaml, strategies.yaml (new strategy versions go through a pull request
the operator merges), workflows, the engine's ledgers, or any edit / deletion of an earlier line. Lessons need
strong evidence (FACT / RESEARCH_FINDING / BACKTEST_EVIDENCE with counts). Profit promises and win
probabilities are refused (section 25). One problem refuses the whole push: nothing half-applied.

Pure functions; the git work is in brain_guard.py.
"""
import re

from engine import memory as mem

BRANCHES = ["claude/brain-briefing", "claude/brain-daily", "claude/brain-weekly"]
NEW_FILES = {                                            # folder -> allowed file names
    "reports/claude/briefings/": re.compile(r"^\d{4}-\d{2}-\d{2}-(0820|1420|2120)\.md$"),
    "reports/claude/daily/": re.compile(r"^\d{4}-\d{2}-\d{2}\.md$"),
    "reports/claude/weekly/": re.compile(r"^\d{4}-\d{2}-\d{2}\.md$"),
}
KNOWLEDGE = ["memory/lessons.md", "memory/failure_journal.md", "memory/missed_trades.md",
             "memory/research_sources.md", "memory/coin_notes.md", "memory/feature_notes.md",
             "memory/smc_research.md", "memory/experiments.md"]
LESSON_CLASSES = ["FACT", "RESEARCH_FINDING", "BACKTEST_EVIDENCE"]      # section 17.7: validated lessons only
MAX_KB = 64                                              # per new file / per addition
MAX_FILES = 12
_NEG = r"(?<!not )(?<!no )(?<!never )(?<!n't )(?<!without )"
FORBIDDEN = [                                            # section 25: never promise profits or state a win probability
    (re.compile(_NEG + r"\bguarantee(d|s)?\b", re.I), "profit promise ('guaranteed')"),
    (re.compile(r"\brisk[- ]free\b", re.I), "profit promise ('risk-free')"),
    (re.compile(r"\b(can'?t|cannot|can not) (lose|fail)\b", re.I), "profit promise ('can't lose')"),
    (re.compile(r"\b(sure|easy) (win|thing|money|profit)s?\b", re.I), "profit promise ('sure win')"),
    (re.compile(r"\bhigh[- ]probability\b", re.I), "'high probability' without statistics (section 1)"),
    (re.compile(r"\b\d{1,3}(\.\d+)? ?%\s*(chance|probability|likelihood|odds)\s+(?:(?:of|to|that)\s+)?(?:(?:this|the|it|a|we|you)\s+)?"
                r"(trade|setup|signal|position|win|winning|profit|succeed|success|work|hit|reach)", re.I),
     "win probability for a trade (section 25)"),
    (re.compile(r"\b(chance|probability|odds|likelihood) (of|to) (winning|win|profit|success|succeed)", re.I),
     "win probability for a trade (section 25)"),
]


def lint(text):
    """Section 25 phrases, one problem per offending line."""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        for rx, why in FORBIDDEN:
            if rx.search(line):
                out.append(f"line {i}: {why}: {line.strip()[:120]!r}")
                break
    return out


def check_records(added, path):
    """An addition to a knowledge file must be section 22 records only: '### title', then the field line."""
    probs = []
    head = added.split("\n### ", 1)[0] if not added.lstrip("\n").startswith("### ") else ""
    if head.strip():
        probs.append("text outside a record (every addition must start with a '### ' title)")
    titles = [ln for ln in added.splitlines() if ln.startswith("### ")]
    recs = mem.parse(added)
    if len(recs) != len(titles) or not titles:
        probs.append(f"{len(titles)} '### ' title(s) but {len(recs)} with a '- timestamp: …' field line")
    for r in recs:
        miss = [k for k in mem.FIELDS if not r.get(k)]
        if miss:
            probs.append(f"record {r['title']!r}: missing {', '.join(miss)}")
            continue
        cls = r["evidence"].split(":")[0].split(" ")[0]
        if cls not in mem.EVIDENCE_CLASSES:
            probs.append(f"record {r['title']!r}: evidence must start with a class {mem.EVIDENCE_CLASSES}")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", r["review"]):
            probs.append(f"record {r['title']!r}: review must be a date YYYY-MM-DD")
        if path.endswith("lessons.md"):
            if cls not in LESSON_CLASSES:
                probs.append(f"lesson {r['title']!r}: evidence {cls} is not enough - a lesson needs "
                             f"{' / '.join(LESSON_CLASSES)} (section 17.7)")
            elif not re.search(r"\d", r["evidence"]):
                probs.append(f"lesson {r['title']!r}: evidence must carry counts (tests, trades, samples)")
    return probs


def allowed_new(path):
    for folder, rx in NEW_FILES.items():
        if path.startswith(folder) and rx.match(path[len(folder):]):
            return True
    return False


def review(changes, main_files):
    """changes: [dict(path, status 'A'/'M'/'D'/..., base=text or None, new=text or None)] = the task branch vs the
    main it started from; main_files: {path: text or None} on the newest main.
    Returns (applies, problems, skipped): applies = [dict(path, kind 'new'/'append', text)] (to copy onto main),
    skipped = changes already on main (a re-run). Any problem -> apply nothing."""
    applies, probs, skipped = [], [], []
    if len(changes) > MAX_FILES:
        probs.append(f"{len(changes)} files changed - at most {MAX_FILES} per task run")
    for c in changes:
        p, st, new = c["path"], c["status"], c.get("new")
        cur = main_files.get(p)
        if st == "A" and allowed_new(p):
            if not (new or "").strip():
                probs.append(f"{p}: empty file")
                continue
            if len(new.encode()) > MAX_KB * 1024:
                probs.append(f"{p}: larger than {MAX_KB} KB")
            if cur is not None:
                (skipped.append(p) if cur == new else probs.append(f"{p}: already exists on main - files are never "
                                                                    "overwritten (use a new file name)"))
                continue
            probs += [f"{p}: {x}" for x in lint(new)]
            applies.append(dict(path=p, kind="new", text=new))
        elif st == "M" and p in KNOWLEDGE:
            why = mem.append_only_problems(c.get("base") or "", new)
            if why:
                probs.append(f"{p}: {why} - memory files only grow (section 17)")
                continue
            added = new[len(c.get("base") or ""):]
            if not added.strip():
                continue
            if len(added.encode()) > MAX_KB * 1024:
                probs.append(f"{p}: addition larger than {MAX_KB} KB")
            if cur is not None and cur.endswith(added):
                skipped.append(p)
                continue
            probs += [f"{p}: {x}" for x in lint(added)]
            probs += [f"{p}: {x}" for x in check_records(added, p)]
            applies.append(dict(path=p, kind="append", text=added))
        elif p in KNOWLEDGE:
            probs.append(f"{p}: {'deleted' if st == 'D' else 'created or renamed'} - knowledge files may only grow")
        elif p == "strategies.yaml":
            probs.append(f"{p}: new strategy versions go through a pull request for the operator, not this branch")
        else:
            probs.append(f"{p}: not allowed ({st}) - Claude's tasks may only add reports/claude/ files and records "
                         "at the end of the knowledge files; code, config, workflows and the engine's files are "
                         "changed only through a pull request the operator merges")
    return ([] if probs else applies), probs, skipped


def apply_text(current, a):
    """The new content of a file on main after one apply."""
    if a["kind"] == "new":
        return a["text"]
    cur = current or ""
    return cur + ("" if not cur or cur.endswith("\n") else "\n") + a["text"]
