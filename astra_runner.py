#!/usr/bin/env python3
"""Prepare, invoke, and validate a GPT-6 Astra research-Brain task.

Only the explicitly supplied output path may be written.  The generated text
is validated through ``engine.brain.review`` before it is saved; this is the
same rule set used by ``brain_guard.py`` when task-branch work is applied.
"""
import argparse
import datetime as dt
import os
import sys

import brain_pack
from engine import brain
from engine.astra_brain import AstraBrain
from engine.brain_provider import BrainProvider

ROOT = os.path.dirname(os.path.abspath(__file__))
TASKS = ("briefing", "daily", "weekly")


def read(relative):
    with open(os.path.join(ROOT, relative), encoding="utf-8", errors="replace") as f:
        return f.read()


def relevant_prompt():
    """Return the constitution sections that define the Brain boundary."""
    text = read("AGENT_PROMPT.md")
    markers = ("## 0.", "## 1.", "## 17.", "## 22.", "## 25.")
    chunks = []
    for marker in markers:
        start = text.find(marker)
        if start < 0:
            continue
        end = text.find("\n## ", start + len(marker))
        chunks.append(text[start:end if end >= 0 else len(text)])
    return "\n\n".join(chunks)


def context_for(task, now):
    """Build read-only task context from the task specification and engine."""
    fact_sheet = "\n".join(brain_pack.pack(task, now, brain_pack.live_status()))
    return "\n\n".join((
        "# Governing prompt excerpts\n" + relevant_prompt(),
        "# Shared task rules\n" + read("tasks/COMMON.md"),
        f"# Task instructions ({task})\n" + read(f"tasks/{'daily_review' if task == 'daily' else 'weekly_research' if task == 'weekly' else 'briefing'}.md"),
        "# Memory conventions\n" + read("memory/README.md"),
        "# Deterministic fact sheet (authoritative for every numeric claim)\n" + fact_sheet,
        "# Required output\nReturn only the Markdown artifact specified by the task. Do not use tools or propose file edits.",
    ))


def branch_for(task):
    return f"astra/brain-{task}"


def run_task(task, now, provider: BrainProvider):
    """Invoke the configured research provider with deterministic, read-only context."""
    return provider.run(task, context_for(task, now))


def validate(task, output, path, now):
    """Validate generated text without applying it or granting write access."""
    changes = [dict(path=path, status="A", base=None, new=output)]
    applies, problems, _ = brain.review(changes, {path: None, brain.sspec.LIBRARY_FILE: read(brain.sspec.LIBRARY_FILE)},
                                        now, branch_for(task))
    return applies, problems


def output_path(task, integration=False):
    if integration:
        return "reports/astra/daily-integration.md"
    now = dt.datetime.now(dt.timezone.utc)
    return brain_pack.target(task, now).replace("reports/claude/", "reports/astra/")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", choices=TASKS)
    parser.add_argument("--output")
    parser.add_argument("--integration", action="store_true")
    args = parser.parse_args()
    if args.integration and args.task != "daily":
        parser.error("--integration is only valid for daily")
    path = args.output or output_path(args.task, args.integration)
    allowed_prefix = "reports/astra/"
    if not path.startswith(allowed_prefix) or os.path.isabs(path) or ".." in path.split("/"):
        parser.error("output must be a permitted reports/astra path")
    now = dt.datetime.now(dt.timezone.utc)
    output = run_task(args.task, now, AstraBrain())
    if args.integration:
        output = (f"<!-- model: gpt-6-astra; timestamp: {now:%Y-%m-%d %H:%M UTC}; task: daily; "
                  "source_context: AGENT_PROMPT.md, tasks, memory, deterministic fact sheet -->\n" + output +
                  "\n\n## Astra validation\n- status: passed deterministic artifact validation; Brain Guard remains the final gate\n")
    _, problems = validate(args.task, output, path, now)
    if problems:
        print("Astra output rejected by Brain Guard rules:", *problems, sep="\n", file=sys.stderr)
        return 2
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "x", encoding="utf-8") as f:
        f.write(output + ("" if output.endswith("\n") else "\n"))
    print(f"Validated Astra {args.task} artifact: {path}")


if __name__ == "__main__":
    main()
