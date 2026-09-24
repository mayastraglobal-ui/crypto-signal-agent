#!/usr/bin/env python3
"""
Append-only guard (AGENT_PROMPT.md section 17: results, experiments and losses are never overwritten or deleted).

Run by both workflows just before they commit: every append-only file (engine/memory.py -> APPEND_ONLY) must
still start with exactly the content of the last commit - only additions are allowed. If an earlier line was
changed or removed, this exits with an error, the workflow stops before committing (nothing is saved) and the
usual "[SYSTEM] ... FAILED" email goes out.

  python memory_guard.py            check the working tree against HEAD
"""
import os
import subprocess
import sys

from engine import memory as mem

ROOT = os.path.dirname(os.path.abspath(__file__))


def committed(path):
    p = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=ROOT, capture_output=True)
    return p.stdout.decode("utf-8", errors="replace") if p.returncode == 0 else None


def check(paths=mem.APPEND_ONLY):
    problems = []
    for path in paths:
        old = committed(path)
        full = os.path.join(ROOT, path)
        new = None
        if os.path.exists(full):
            with open(full, encoding="utf-8", errors="replace") as f:
                new = f.read()
        why = mem.append_only_problems(old, new)
        if why:
            problems.append(f"{path}: {why}")
    return problems


def main():
    problems = check()
    if problems:
        print("APPEND-ONLY RULE BROKEN - nothing will be committed (AGENT_PROMPT.md section 17):")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"memory guard: {len(mem.APPEND_ONLY)} append-only files checked - only additions")


if __name__ == "__main__":
    main()
