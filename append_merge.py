#!/usr/bin/env python3
"""
Git merge driver for the append-only files (strategies_lab.yaml, events.yaml, the memory/ records and ledgers).

Two workflows can add to the same file at the same time (e.g. the Brain applies Claude's lab card while the research
run appends the engine's variant card). Git's normal text merge then aligns lines the two additions share (a lab
card's '  targets:', '    - 2R', ...) and interleaves them - on 26 Sep 2026 that broke both lab cards. This driver
merges only what an append-only file allows: both sides must keep the common base unchanged at the start, and the
result is one side followed by the other side's addition, each addition whole. Anything else is a real conflict
(exit 1): the workflow stops and nothing is pushed.

Set up (the workflows do this before `git pull --rebase`):
  git config merge.append.name "append-only files: keep both additions whole"
  git config merge.append.driver "python3 append_merge.py %O %A %B"
and .gitattributes names the files (`strategies_lab.yaml merge=append`).

  python3 append_merge.py BASE OURS THEIRS      (git calls it; the result is written to OURS)
"""
import sys


def read(path):
    with open(path, encoding="utf-8", errors="surrogateescape") as f:
        return f.read()


def merge(base, ours, theirs):
    """The merged text, or None when one side changed or removed a line of the base (not append-only)."""
    if not ours.startswith(base) or not theirs.startswith(base):
        return None
    add_ours, add_theirs = ours[len(base):], theirs[len(base):]
    if not add_theirs or add_theirs == add_ours or ours.endswith(add_theirs):
        return ours
    if not add_ours or theirs.endswith(add_ours):
        return theirs
    return ours + ("" if ours.endswith("\n") or not ours else "\n") + add_theirs


def main(argv):
    if len(argv) != 4:
        sys.exit("usage: append_merge.py BASE OURS THEIRS")
    base, ours, theirs = (read(p) for p in argv[1:])
    out = merge(base, ours, theirs)
    if out is None:
        print(f"append_merge: {argv[2]}: an earlier line was changed on one side - not an append-only merge",
              file=sys.stderr)
        return 1
    with open(argv[2], "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
