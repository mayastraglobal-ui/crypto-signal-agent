"""
The beginner curriculum (Phase 17 B): memory/curriculum.md, one lesson per [DAILY] email.

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
