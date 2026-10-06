#!/usr/bin/env python3
"""
Journal sync, GitHub side (operator request 2026-10-06): read the operator's journal from the branch `journal`
(uploaded by the live watcher, live_watcher.py JournalSync) and write the facts the agent learns from:

  reports/journal_review.json   numbers (the weekly email's "Your own trades" part)
  reports/journal_review.md     the same as text (Claude's fact sheet, brain_pack.py)

  python journal_review.py              fetch the branch, write both files (run by the hourly scan)
  python journal_review.py --file X     use a local my_trades.csv instead (a test)

No branch yet (journal sync not set up) -> nothing is written. Report only: never changes a gate, cost or strategy.
"""
import argparse
import json
import os
import subprocess
import sys
import time

from engine import journal as jr

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(ROOT, "reports", "journal_review.json")
OUT_MD = os.path.join(ROOT, "reports", "journal_review.md")
BRANCH = "journal"
PATH = "journal/my_trades.csv"


def fetch(root=ROOT):
    """The journal text from origin/journal, or None when the branch or the file is not there."""
    git = lambda *a: subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)  # noqa: E731
    if git("fetch", "--quiet", "--depth", "1", "origin", BRANCH).returncode != 0:
        return None
    r = git("show", f"FETCH_HEAD:{PATH}")
    return r.stdout if r.returncode == 0 else None


def write(rv, out_json=OUT_JSON, out_md=OUT_MD):
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w") as f:
        json.dump(rv, f, indent=1)
    with open(out_md, "w") as f:
        f.write("# Your own trades (journal sync)\n\n"
                "From journal/my_trades.csv on the branch `journal` (the live watcher's Telegram buttons, the plan "
                "result of every alert and your /result replies). Plan = the backtest rules followed on 5m candles, "
                "before fees. Report only: nothing here changes a strategy, a gate or a cost.\n\n"
                + "\n".join(jr.lines(rv)) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--file", help="a local my_trades.csv instead of the branch")
    args = ap.parse_args()
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = fetch()
    if text is None:
        print("No journal on GitHub yet (journal sync not set up) - nothing written.")
        return 0
    rows = jr.read(text)
    rv = jr.review(rows, int(time.time() * 1000))
    write(rv)
    print("\n".join(jr.lines(rv)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
