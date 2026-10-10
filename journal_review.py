#!/usr/bin/env python3
"""
Journal sync, GitHub side (operator request 2026-10-06): read the operator's journal from the branch `journal`
(uploaded by the live watcher, live_watcher.py JournalSync) and write the facts the agent learns from:

  reports/journal_review.json   numbers (the weekly email's "Your own trades" part)
  reports/journal_review.md     the same as text (Claude's fact sheet, brain_pack.py)

  reports/shocks_review.json    ⚡ the shock alarm's week (journal/shocks.csv on the branch `journal`): how many shocks,
                                kept going or reversed 4 hours later, followed by a strategy alert or not
  reports/watcher_health.json   is the live watcher running? (its hourly heartbeat on the branch watcher-heartbeat;
                                notify.py system emails an ALERT when it is silent for 2 hours, FIXED when it is back)
  python journal_review.py              fetch the branch, write both files (run by the hourly scan)
  python journal_review.py --file X     use a local my_trades.csv instead (a test)

No branch yet (journal sync not set up) -> nothing is written. Report only: never changes a gate, cost or strategy.
"""
import argparse
import csv
import datetime as dt
import io
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
DECISIONS = "journal/decisions.csv"      # PR 3: the operator's taps under the weekly review (promote / unpromote)
SHOCKS = "journal/shocks.csv"            # ⚡ the shock alarm's log (2026-10-10)
SHOCKS_JSON = os.path.join(ROOT, "reports", "shocks_review.json")
HEALTH_JSON = os.path.join(ROOT, "reports", "watcher_health.json")
HB_BRANCH, HB_FILE = "watcher-heartbeat", "heartbeat.json"
SILENT_AFTER_MIN = 120                   # no heartbeat for 2 hours = the watcher (PC) is off, asleep or offline


def fetch(root=ROOT, path=PATH, branch=BRANCH):
    """The file's text from origin/<branch>, or None when the branch or the file is not there."""
    git = lambda *a: subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)  # noqa: E731
    if git("fetch", "--quiet", "--depth", "1", "origin", branch).returncode != 0:
        return None
    r = git("show", f"FETCH_HEAD:{path}")
    return r.stdout if r.returncode == 0 else None


def health(text, now_ms, silent_after_min=SILENT_AFTER_MIN):
    """The live watcher's state from its heartbeat file: OK (heard from within silent_after_min), SILENT (older),
    OFF (no heartbeat on GitHub: the journal-sync token is not set up, or the watcher is older than 2026-10-10)."""
    checked = time.strftime("%Y-%m-%d %H:%M", time.gmtime(now_ms / 1000))
    try:
        hb = json.loads(text) if text else None
    except ValueError:
        hb = None
    if not hb or not hb.get("utc"):
        return dict(state="OFF", checked_utc=checked, last_utc=None, age_min=None, heartbeat=None,
                    text="no heartbeat on GitHub - the watcher needs journal sync (JOURNAL_GITHUB_TOKEN) and the "
                         "update of 2026-10-10")
    last = int(_utc_ms(hb["utc"]))
    age = max(0, (now_ms - last) // 60_000)
    ok = age <= silent_after_min
    return dict(state="OK" if ok else "SILENT", checked_utc=checked, last_utc=hb["utc"], age_min=int(age),
                heartbeat=hb, text=(f"live watcher: last heartbeat {hb['utc']} UTC ({age} min ago)" if ok else
                                    f"live watcher SILENT: no heartbeat for {age // 60}h{age % 60:02d}m (last "
                                    f"{hb['utc']} UTC) - the PC may be off, asleep or offline"))


def _utc_ms(txt):
    return dt.datetime.strptime(txt, "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc).timestamp() * 1000


def shocks_review(text, now_ms):
    """The shock alarm's week from journal/shocks.csv (None when there is no log on GitHub yet)."""
    if not text:
        return None
    from engine import shock as shk
    rows = list(csv.DictReader(io.StringIO(text)))
    sv = shk.review(rows, now_ms)
    sv["checked_utc"] = time.strftime("%Y-%m-%d %H:%M", time.gmtime(now_ms / 1000))
    sv["lines"] = shk.lines(sv)
    return sv


def write_health(h, path=HEALTH_JSON):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(h, f, indent=1)


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
        h = health(fetch(path=HB_FILE, branch=HB_BRANCH), int(time.time() * 1000))
        write_health(h)
        print(h["text"])
        sv = shocks_review(fetch(path=SHOCKS), int(time.time() * 1000))
        if sv is not None:
            write_health(sv, SHOCKS_JSON)
            print(f"shock log: {sv['n']} shock(s) in the last 7 days")
    if text is None:
        print("No journal on GitHub yet (journal sync not set up) - nothing written.")
        return 0
    rows = jr.read(text)
    rv = jr.review(rows, int(time.time() * 1000))
    rv["decisions"] = jr.read_decisions(None if args.file else fetch(path=DECISIONS))
    write(rv)
    print("\n".join(jr.lines(rv)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
