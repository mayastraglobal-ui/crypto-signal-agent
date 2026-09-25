#!/usr/bin/env python3
"""
Apply the work of Claude's scheduled tasks to main - safely (Phase 14; the rules are in engine/brain.py).

Run by the Brain workflow (.github/workflows/brain.yml) in a checkout of main. For each task branch
(claude/brain-briefing, claude/brain-daily, claude/brain-weekly) with a new commit since the last run:

  1. compare the branch with the main it started from (git merge-base)
  2. engine/brain.review(): only new reports/claude/ files, record additions to the knowledge files, calendar
     entries (events.yaml) and lab strategy cards (strategies_lab.yaml) pass
  3. all good -> copy them onto THIS (newest) main: new files are written, additions appended at the end
     any problem -> nothing from that push is applied, and the problems go into the [SYSTEM] email

reports/claude/state.json remembers the last commit handled per branch (so nothing is applied twice).

  python brain_guard.py --out result.json
"""
import argparse
import datetime as dt
import json
import os
import subprocess

from engine import brain

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(ROOT, "reports", "claude", "state.json")


def git(*args, check=True):
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p


def show(rev, path):
    p = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=ROOT, capture_output=True)
    return p.stdout.decode("utf-8", errors="replace") if p.returncode == 0 else None


def read(path):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return None
    with open(full, encoding="utf-8", errors="replace") as f:
        return f.read()


def changes_of(sha):
    base = git("merge-base", "HEAD", sha).stdout.strip()
    out = []
    for line in git("diff", "--name-status", "--no-renames", base, sha).stdout.splitlines():
        st, path = line.split("\t", 1)
        out.append(dict(path=path, status=st[0], base=show(base, path), new=show(sha, path)))
    return out


def handle(branch, state, now):
    if git("fetch", "--quiet", "origin", branch, check=False).returncode != 0:
        return None                                        # the task has never pushed
    sha = git("rev-parse", "FETCH_HEAD").stdout.strip()
    if state.get(branch, {}).get("sha") == sha:
        return None                                        # already handled
    subject = git("log", "-1", "--format=%s", sha).stdout.strip()
    changes = changes_of(sha)
    paths = {c["path"] for c in changes} | {brain.sspec.LIBRARY_FILE}      # the library: lab cards are checked against it
    applies, probs, skipped = brain.review(changes, {p: read(p) for p in paths}, dt.datetime.now(dt.timezone.utc), branch)
    for a in applies:
        full = os.path.join(ROOT, a["path"])
        os.makedirs(os.path.dirname(full), exist_ok=True)
        text = brain.apply_text(read(a["path"]), a)
        with open(full, "w", encoding="utf-8") as f:
            f.write(text)
    res = dict(branch=branch, sha=sha, subject=subject, when=now,
               status="rejected" if probs else "applied", problems=probs,
               applied=[a["path"] for a in applies], skipped=skipped)
    state[branch] = {k: res[k] for k in ("sha", "subject", "when", "status", "problems", "applied")}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="write what happened as JSON (for notify.py brain)")
    args = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    results = [r for r in (handle(b, state, now) for b in brain.BRANCHES) if r]
    if results:
        os.makedirs(os.path.dirname(STATE), exist_ok=True)
        with open(STATE, "w") as f:
            json.dump(state, f, indent=1)
    for r in results:
        print(f"{r['branch']} {r['sha'][:8]} ({r['subject']}): {r['status'].upper()}"
              + "".join(f"\n  + {p}" for p in r["applied"]) + "".join(f"\n  = {p} (already on main)" for p in r["skipped"])
              + "".join(f"\n  ! {p}" for p in r["problems"]))
    if not results:
        print("No new work from Claude's tasks.")
    if args.out:
        with open(args.out, "w") as f:
            json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()
