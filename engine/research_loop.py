"""
The research loop (Phase 18 A item 1): hypothesis -> test -> feedback -> next hypothesis.

Idea studied in Microsoft RD-Agent (R1, memory/research_sources.md): every experiment remembers the one it came from,
and after each test a feedback step writes what was observed, whether the hypothesis held and the next hypothesis.
Rewritten here in our own, much smaller form - no code copied:

  * every lab card names its `parent:` - the result, lesson, failure, missed move, experiment or source that led to it
    (format checked in strategy_spec.parent_problems; that the named record exists is checked here, by the Brain guard)
  * after a research run tests a lab card, the daily review writes ONE feedback record in memory/experiments.md:
        ### Feedback: <id>@<version>
        - timestamp: ... (the section 22 line)
        - parent: <the card's parent>
        - hypothesis: <the card's hypothesis>
        - result: <the engine's numbers, from the fact sheet>
        - teaches: <what it teaches>
        - next: <the next hypothesis> | stop this line
    It is due again when a cell of the card changes status later.
  * idea chains (parent -> card -> result -> next) for the weekly email and the fact sheets.

The engine never writes the feedback itself (Claude explains; the engine measures). Pure functions.
"""
import re

FEEDBACK = "Feedback:"
FEEDBACK_KEYS = ["parent", "hypothesis", "result", "teaches", "next"]
STOP = "stop this line"
KEY_RE = re.compile(r"^\S+@\d+(?:\.\d+)*$")
TS_RE = re.compile(r"^- timestamp: (\d{4}-\d{2}-\d{2} \d{2}:\d{2})")
FILES = dict(lesson="memory/lessons.md", failure="memory/failure_journal.md", experiment="memory/experiments.md",
             source="memory/research_sources.md")


def titles(text):
    return [ln[4:].strip() for ln in (text or "").splitlines() if ln.startswith("### ")]


def _matches(ref, title):
    a, b = ref.lower().strip(" .'\""), title.lower().strip(" .'\"")
    return len(b) >= 4 and (a == b or a.startswith(b) or b.startswith(a))


def parent_exists_problems(card, memory, loss_tags=()):
    """The parent a lab card names must exist: a record title in the file of its kind (memory = {path: text} on main
    plus this push's additions); a 'failure' parent may instead name an engine loss tag with its count (n=...).
    'result' / 'card' parents are checked against the card files (strategy_spec.parent_problems)."""
    from engine import strategy_spec as sspec
    pp = sspec.parse_parent(card.get("parent"))
    if pp is None or pp[0] not in FILES:
        return []
    kind, ref = pp
    if any(_matches(ref, t) for t in titles(memory.get(FILES[kind]))):
        return []
    if kind == "failure" and any(re.search(rf"\b{re.escape(t)}\b", ref) for t in loss_tags) and re.search(r"\bn\s*=\s*\d+", ref):
        return []
    if kind == "experiment" and re.search(r"\bEXP-\d{4}\b", ref) and \
            re.search(r"\b" + re.escape(re.search(r"EXP-\d{4}", ref).group(0)) + r"\b", memory.get(FILES[kind]) or ""):
        return []
    return [f"parent {kind} {ref!r} is not a record title in {FILES[kind]} (copy the title of the record that led to "
            "this card)"]


def _blocks(text):
    parts = ("\n" + (text or "")).split("\n### ")[1:]
    return [(p.splitlines()[0].strip(), p.splitlines()[1:]) for p in parts]


def feedback_records(text):
    """{card key: [dict(timestamp, parent, hypothesis, result, teaches, next)]} in file order."""
    out = {}
    for title, body in _blocks(text):
        if not title.startswith(FEEDBACK):
            continue
        key = title[len(FEEDBACK):].strip()
        rec = dict(timestamp=None)
        for ln in body:
            m = TS_RE.match(ln.strip())
            if m:
                rec["timestamp"] = m.group(1)
                continue
            s = ln.strip()
            for k in FEEDBACK_KEYS:
                if s.lower().startswith(f"- {k}:"):
                    rec.setdefault(k, s.split(":", 1)[1].strip())
        out.setdefault(key, []).append(rec)
    return out


def feedback_problems(added):
    """Brain guard: a 'Feedback: <id>@<version>' record in memory/experiments.md has all five detail lines, a result
    with the engine's numbers and a next step ('stop this line' or the next hypothesis)."""
    probs = []
    for title, body in _blocks(added):
        if not title.startswith(FEEDBACK):
            continue
        key = title[len(FEEDBACK):].strip()
        if not KEY_RE.match(key):
            probs.append(f"record {title!r}: the title must be 'Feedback: <id>@<version>'")
        rec = (feedback_records("### " + title + "\n" + "\n".join(body)).get(key) or [{}])[0]
        miss = [k for k in FEEDBACK_KEYS if not rec.get(k)]
        if miss:
            probs.append(f"record {title!r}: needs detail lines " + ", ".join(f"'- {k}: ...'" for k in miss)
                         + " (hypothesis -> result -> what it teaches -> next hypothesis or 'stop this line')")
        elif not re.search(r"\d", rec["result"]):
            probs.append(f"record {title!r}: result must quote the engine's numbers (trades, R) from the fact sheet")
    return probs


def _cells(rows, key):
    return [r for r in rows if f"{r.get('id')}@{r.get('version')}" == key]


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def cell_text(r):
    avg, test = _num(r.get("avg_r")), _num(r.get("test_avg_r"))
    n = _num(r.get("trades"))
    return (f"{r.get('tf')} {r.get('status')}"
            + (f" {int(n)} trades {avg:+.3f}R" if n is not None and avg is not None else "")
            + (f" (unseen {test:+.3f}R)" if test is not None else ""))


def feedback_due(cards, rows, fb):
    """Lab cards whose results need a feedback record: tested, and no feedback yet or a cell changed status since the
    newest one. cards = {key: card}; rows = memory/strategy_registry.csv rows (dicts); fb = feedback_records()."""
    out = []
    for key, c in sorted(cards.items()):
        if not c.get("lab") or c.get("twin_of"):
            continue
        cells = _cells(rows, key)
        if not cells:
            continue
        last = max((r["timestamp"] or "" for r in fb.get(key, [])), default="")
        changed = max(str(r.get("since_utc") or "") for r in cells)
        if last and changed <= last:
            continue
        out.append(dict(key=key, parent=c.get("parent") or "-", hypothesis=" ".join(str(c.get("hypothesis") or "").split()),
                        cells=[cell_text(r) for r in sorted(cells, key=lambda r: str(r.get("tf")))],
                        gates=sorted({str(r.get("gates_failed")) for r in cells if str(r.get("gates_failed") or "") not in
                                      ("", "nan")})[:3],
                        last_feedback=last or None))
    return out


def chains(cards, rows, fb, limit=15):
    """Idea chains ending in a lab card: [(root text, [card keys from oldest to newest], next text)].
    A card's parent 'result: X@v tf' or 'card: X@v' links it to card X@v; any other parent is the chain's root."""
    from engine import strategy_spec as sspec
    link = {}
    for key, c in cards.items():
        pp = sspec.parse_parent(c.get("parent"))
        if pp and pp[0] in ("result", "card"):
            link[key] = pp[1].split()[0]
    lab = {k for k, c in cards.items() if c.get("lab") and not c.get("twin_of") and c.get("parent")}
    children = {v for k, v in link.items() if k in lab}
    out = []
    for leaf in sorted(lab - children):
        path, k, seen = [leaf], leaf, {leaf}
        while k in link and link[k] in cards and link[k] not in seen and cards[link[k]].get("lab"):
            k = link[k]
            path.insert(0, k)
            seen.add(k)
        first = cards[path[0]]
        root = str(first.get("parent") or "-")
        recs = fb.get(leaf) or []
        nxt = recs[-1].get("next") if recs else None
        out.append((root, path, nxt))
    return out[:limit]


def chain_lines(cards, rows, fb, indent="  "):
    """The idea chains as plain lines (weekly email, fact sheets)."""
    ch = chains(cards, rows, fb)
    if not ch:
        return [f"{indent}- no lab card with a parent yet - chains start when the reviews add cards"]
    out = []
    for root, path, nxt in ch:
        steps = []
        for k in path:
            cells = _cells(rows, k)
            steps.append(f"{k} [{'; '.join(cell_text(r) for r in cells) or 'not tested yet'}]")
        out.append(f"{indent}- {root} -> " + " -> ".join(steps)
                   + (f" -> next: {nxt}" if nxt else " -> feedback not written yet"))
    return out


def load(root):
    """(cards {key: card with lab flag}, registry rows, feedback records) from the repository files."""
    import csv
    import os

    import yaml

    from engine import strategy_spec as sspec
    cards = {}
    for name, lab in ((sspec.LIBRARY_FILE, False), (sspec.LAB_FILE, True)):
        p = os.path.join(root, name)
        try:
            items = yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else []
        except yaml.YAMLError:
            items = []
        for c in items or []:
            if isinstance(c, dict) and c.get("id"):
                cards[f"{c['id']}@{c.get('version')}"] = dict(c, lab=lab)
    p = os.path.join(root, "memory", "strategy_registry.csv")
    rows = list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []
    p = os.path.join(root, "memory", "experiments.md")
    fb = feedback_records(open(p, encoding="utf-8").read()) if os.path.exists(p) else {}
    return cards, rows, fb
