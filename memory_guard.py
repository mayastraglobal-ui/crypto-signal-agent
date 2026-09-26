#!/usr/bin/env python3
"""
Append-only guard (AGENT_PROMPT.md section 17: results, experiments and losses are never overwritten or deleted).

Run by both workflows just before they commit: every append-only file (engine/memory.py -> APPEND_ONLY) must
still start with exactly the content of the last commit - only additions are allowed. If an earlier line was
changed or removed, this exits with an error, the workflow stops before committing (nothing is saved) and the
usual "[SYSTEM] ... FAILED" email goes out.

  python memory_guard.py               check the working tree against HEAD (before committing)
  python memory_guard.py --after-sync  after `git pull --rebase`, before pushing: every append-only file still starts
                                       with the pushed main (@{upstream}), and every strategy card in
                                       strategies_lab.yaml still loads - a merge that broke a file is never pushed
"""
import os
import subprocess
import sys

from engine import memory as mem

ROOT = os.path.dirname(os.path.abspath(__file__))


def committed(path, rev="HEAD"):
    p = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=ROOT, capture_output=True)
    return p.stdout.decode("utf-8", errors="replace") if p.returncode == 0 else None


def check(paths=mem.APPEND_ONLY, rev="HEAD"):
    problems = []
    for path in paths:
        old = committed(path, rev)
        full = os.path.join(ROOT, path)
        new = None
        if os.path.exists(full):
            with open(full, encoding="utf-8", errors="replace") as f:
                new = f.read()
        why = mem.append_only_problems(old, new)
        if why:
            problems.append(f"{path}: {why}")
    return problems


def lab_problems():
    """Every card of strategies_lab.yaml must still load in the engine (a broken merge would silently drop it)."""
    import yaml
    from engine import regime as rg
    from engine import strategy_spec as sspec
    from engine import timeframes as tfm
    path = os.path.join(ROOT, sspec.LAB_FILE)
    if not os.path.exists(path):
        return []
    try:
        with open(path) as f:
            lab = yaml.safe_load(f) or []
        with open(os.path.join(ROOT, sspec.LIBRARY_FILE)) as f:
            lib = yaml.safe_load(f) or []
    except yaml.YAMLError as e:
        return [f"{sspec.LAB_FILE}: not readable after the merge ({str(e).splitlines()[0]})"]
    if not isinstance(lab, list):
        return [f"{sspec.LAB_FILE}: not a list of cards after the merge"]
    _, problems, _, _ = sspec.load_library(lib, lab, rg.LABELS, tfm.TRADE_ORDER)
    return [f"{sspec.LAB_FILE}: {k}: {'; '.join(v)}" for k, v in problems.items() if str(k).startswith("lab")]


def main():
    if "--after-sync" in sys.argv:
        problems = check(rev="@{upstream}") + lab_problems()
        if problems:
            print("THE MERGE WITH THE NEWEST MAIN BROKE A FILE - nothing will be pushed:")
            for p in problems:
                print(f"  - {p}")
            sys.exit(1)
        print("memory guard (after sync): append-only files start with the pushed main; every lab card loads")
        return
    problems = check()
    if problems:
        print("APPEND-ONLY RULE BROKEN - nothing will be committed (AGENT_PROMPT.md section 17):")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"memory guard: {len(mem.APPEND_ONLY)} append-only files checked - only additions")


if __name__ == "__main__":
    main()
