"""
Monthly clean-up (Phase 17 D, item 12) - ADD ONLY, history is never deleted.

Run by the research run on the 1st of each month (research.py; `--cleanup` forces it):
  * retire dead cards: a strategy version whose every tested timeframe has been FAILED or RETIRED for 30+ days is
    added to memory/retired_cards.csv. The card stays in strategies.yaml / strategies_lab.yaml; the engine just stops
    re-testing it (scanner.load_cards). To bring one back, delete its line in a pull request.
  * duplicate lessons: pairs of lessons in memory/lessons.md whose titles say nearly the same thing.
  * re-check old lessons (30+ days): does the loss tag a lesson is about still show up as systematic in today's
    research? The numbers are measured here.
The engine never writes lessons (section 17.7), so the duplicates and re-checks go into memory/cleanup_log.md and the
next daily review writes the "Merged: ..." / "Re-check: ..." records into lessons.md (the fact sheet lists them).
Pure functions; research.py writes the files.
"""
import csv
import datetime as dt
import io
import re

from engine import attribution as att
from engine import memory as mem

DEAD_STATUSES = {"FAILED", "RETIRED"}
DEAD_DAYS = 30
OLD_LESSON_DAYS = 30
SIMILAR = 0.6
RETIRED_COLS = ["key", "retired_utc", "reason"]
STOP = {"a", "an", "the", "in", "on", "of", "and", "or", "to", "is", "are", "with", "for", "when", "at", "by"}
TAGS = att.CONDITIONS + att.PATH_TAGS + att.LOSER_TAGS


def retired(text):
    """memory/retired_cards.csv -> {key: reason}."""
    return {r["key"]: r.get("reason", "") for r in csv.DictReader(io.StringIO(text or "")) if r.get("key")}


def dead_cards(registry, retired_keys, now):
    """[(key, reason)]: versions whose every tested cell is FAILED / RETIRED since 30+ days (never APPROVED / paper)."""
    cells = {}
    for ck, c in registry["cells"].items():
        cells.setdefault(ck.split("|")[0], []).append((ck.split("|")[1], c))
    out = []
    for key, rows in sorted(cells.items()):
        if key in retired_keys or not rows:
            continue
        if any(c.get("status") not in DEAD_STATUSES for _, c in rows):
            continue
        ages = []
        for _, c in rows:
            try:
                ages.append((now - dt.datetime.strptime(str(c.get("since_utc"))[:16], "%Y-%m-%d %H:%M")
                             .replace(tzinfo=dt.timezone.utc)).days)
            except ValueError:
                ages.append(0)
        if min(ages) >= DEAD_DAYS:
            out.append((key, f"every timeframe {'/'.join(sorted({c.get('status') for _, c in rows}))} for "
                             f"{min(ages)}+ days ({', '.join(tf for tf, _ in rows)})"))
    return out


def _words(title):
    return {w for w in re.findall(r"[a-z0-9_]+", title.lower()) if w not in STOP}


def _blocks(text):
    """[(title, whole record text)] of a knowledge file."""
    parts = ("\n" + (text or "")).split("\n### ")[1:]
    return [(p.splitlines()[0].strip(), p) for p in parts]


def duplicate_lessons(lessons_text):
    """[(title a, title b, similarity)] - lessons whose titles share most of their words. Records already merged
    ('Merged: ...') or reviews ('Review: ...', 'Re-check: ...') are left out."""
    titles = [t for t, _ in _blocks(lessons_text) if not t.lower().startswith(("merged:", "review:", "re-check:"))]
    merged = " ".join(b for t, b in _blocks(lessons_text) if t.lower().startswith("merged:"))
    out = []
    for i, a in enumerate(titles):
        for b in titles[i + 1:]:
            wa, wb = _words(a), _words(b)
            sim = len(wa & wb) / len(wa | wb) if wa | wb else 0
            if sim >= SIMILAR and not (a in merged and b in merged):
                out.append((a, b, round(sim, 2)))
    return out


def recheck_lessons(lessons_text, research, now):
    """[dict(title, age_days, tags, now)] for lessons 30+ days old: is their loss tag still systematic today?"""
    systematic = {}
    for ck, c in ((research or {}).get("cells") or {}).items():
        for t in ((c.get("attribution") or {}).get("systematic") or []):
            systematic.setdefault(t, []).append(ck)
    out = []
    for title, block in _blocks(lessons_text):
        if title.lower().startswith(("merged:", "review:", "re-check:")):
            continue
        rec = (mem.parse("### " + block) or [{}])[0]
        try:
            age = (now.date() - dt.date.fromisoformat(str(rec.get("timestamp", ""))[:10])).days
        except ValueError:
            continue
        if age < OLD_LESSON_DAYS:
            continue
        tags = [t for t in TAGS if re.search(rf"\b{re.escape(t)}\b", block)]
        if not tags:
            out.append(dict(title=title, age_days=age, tags=[], now="no loss tag named - re-check it by hand"))
            continue
        now_txt = "; ".join(f"{t}: systematic in {len(systematic.get(t, []))} test(s) now"
                            + (" - STILL HOLDS" if len(systematic.get(t, [])) >= 2 else " - NO LONGER SHOWS")
                            for t in tags)
        out.append(dict(title=title, age_days=age, tags=tags, now=now_txt))
    return out


def run(registry, retired_text, lessons_text, research, now):
    rk = retired(retired_text)
    return dict(month=now.strftime("%Y-%m"), run_utc=now.strftime("%Y-%m-%d %H:%M"),
                dead=[dict(key=k, reason=r) for k, r in dead_cards(registry, set(rk), now)],
                duplicates=[dict(a=a, b=b, similarity=s) for a, b, s in duplicate_lessons(lessons_text)],
                rechecks=recheck_lessons(lessons_text, research, now), already_retired=len(rk))


def retired_rows(result, header):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    if header:
        w.writerow(RETIRED_COLS)
    for d in result["dead"]:
        w.writerow([d["key"], result["run_utc"], d["reason"]])
    return buf.getvalue()


def log_text(result):
    """The month's section of memory/cleanup_log.md (append-only)."""
    L = [f"\n## {result['month']} clean-up · {result['run_utc']} UTC",
         f"- retired (no longer re-tested; the cards stay in their files): "
         + ("; ".join(f"{d['key']} ({d['reason']})" for d in result["dead"]) or "none")]
    L.append("- possible duplicate lessons (the daily review writes one 'Merged: ...' record for each pair): "
             + ("; ".join(f"'{d['a']}' ~ '{d['b']}' ({d['similarity']})" for d in result["duplicates"]) or "none"))
    L.append("- old lessons re-checked on today's data (the daily review writes a 'Re-check: ...' record for each): "
             + ("; ".join(f"'{r['title']}' ({r['age_days']} days): {r['now']}" for r in result["rechecks"]) or "none"))
    return "\n".join(L) + "\n"
