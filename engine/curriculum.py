"""
The operator's beginner course (memory/beginner_course.md, one lesson per [DAILY] email) and the agent's reading plan
(memory/curriculum.md, one item per daily review - Phase 17 B item 8).

Lessons are `## Lxx · title` blocks. notify.py daily adds the next lesson not had yet to the email and remembers it in
reports/curriculum_sent.json; after the last lesson the course starts again. Pure functions.
"""
import re

HEAD = re.compile(r"^## (L\d+) · (.+)$")


def parse(text):
    """[dict(id, title, lines)] in file order."""
    out = []
    for line in (text or "").splitlines():
        m = HEAD.match(line.strip())
        if m:
            out.append(dict(id=m.group(1), title=m.group(2).strip(), lines=[]))
        elif out and line.startswith("## "):
            out.append(None)                                   # another heading ends the lesson
        elif out and out[-1] is not None and line.strip():
            out[-1]["lines"].append(line.strip())
    return [x for x in out if x]


def next_lesson(lessons, sent):
    """The first lesson not sent yet; when all were sent, the course starts again (sent is then reset).
    Returns (lesson or None, the sent list to store after sending it)."""
    if not lessons:
        return None, list(sent)
    had = set(sent)
    todo = [x for x in lessons if x["id"] not in had]
    if not todo:
        return lessons[0], [lessons[0]["id"]]
    return todo[0], list(sent) + [todo[0]["id"]]


def email_lines(lesson, lessons):
    n = next(i for i, x in enumerate(lessons, 1) if x["id"] == lesson["id"])
    return ["", f"LESSON {n} of {len(lessons)}: {lesson['title']}"] + [f"  {ln}" for ln in lesson["lines"]]


ITEM = re.compile(r"^## (C\d+) · ([a-z_]+) · (.+)$")
KINDS = ["paper", "book", "exchange_research", "post_mortem", "interview"]


def parse_plan(text):
    """The reading plan: [dict(id, kind, title, lines)] from `## Cxx · kind · title` blocks."""
    out = []
    for line in (text or "").splitlines():
        m = ITEM.match(line.strip())
        if m:
            out.append(dict(id=m.group(1), kind=m.group(2), title=m.group(3).strip(), lines=[]))
        elif line.startswith("## "):
            out.append(None)
        elif out and out[-1] is not None and line.strip():
            out[-1]["lines"].append(line.strip())
    return [x for x in out if x]


def studied(sources_text):
    """{item id: newest timestamp} of the reading-plan items already recorded in memory/research_sources.md (records
    whose title starts with '[Cxx]')."""
    out, cur = {}, None
    for line in (sources_text or "").splitlines():
        m = re.match(r"^### \[(C\d+)\]", line)
        if m:
            cur = m.group(1)
            continue
        t = re.match(r"^- timestamp: ([^·]+)", line)
        if t and cur:
            out[cur] = max(out.get(cur, ""), t.group(1).strip())
            cur = None
    return out


def next_item(plan, done):
    """Today's item: the first one never studied; when all were studied, the one studied longest ago (rotation)."""
    if not plan:
        return None
    todo = [x for x in plan if x["id"] not in done]
    return todo[0] if todo else min(plan, key=lambda x: (done.get(x["id"], ""), x["id"]))
