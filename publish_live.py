#!/usr/bin/env python3
"""
Publish the large report files that are replaced every run to the branch `live-reports`.

The branch always holds exactly ONE commit (force-pushed, no parent), so it never builds up history:
main keeps the small, important history (memory/, signals_log.csv, strategy_scoreboard.csv,
reports/daily/, latest.md); `live-reports` keeps only the newest copy of the big files.

  python publish_live.py            publish: files present in reports/ are taken from this run, the
                                    missing ones (e.g. research.json during the hourly scan) are carried
                                    over from the current live-reports branch
  python publish_live.py --restore  copy the files from live-reports into reports/ when they are not
                                    there yet (the hourly scan needs the daily research.json)
  python publish_live.py --refresh  ALWAYS overwrite reports/ with the newest live-reports copy (Claude's task
                                    sessions are persistent: an old copy from an earlier run must be replaced)

It only uses git plumbing inside this checkout (so the workflow's push credentials apply) and never
touches main or the working tree's index.
"""
import argparse
import datetime as dt
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
BRANCH = "live-reports"
LIVE_FILES = ["reports/latest.json", "reports/smc.json", "reports/features.json", "reports/regime.json",
              "reports/feature_evidence.json", "reports/data_quality.json", "reports/research.json",
              "reports/dashboard_data.json"]
README = """# live-reports

The newest copy of the large report files of the Crypto Signal Agent, replaced on every run
(one commit, force-pushed - this branch has no history on purpose).

| File | Written by | What |
|---|---|---|
| reports/latest.json | hourly scan | the whole report as data (signals, scoreboard, regimes, SMC ...) |
| reports/data_quality.json | hourly scan | data check per coin and timeframe |
| reports/features.json | hourly scan | newest features per coin and timeframe |
| reports/feature_evidence.json | hourly scan | candle / SMC patterns vs random entries |
| reports/regime.json | hourly scan | market regime per coin and timeframe, with evidence |
| reports/smc.json | hourly scan | SMC state and newest events |
| reports/research.json | daily research run | Layers A/B/C, stress, +-20%, failure attribution, missed moves |

The history that matters (memory/, signals_log.csv, strategy_scoreboard.csv, daily reports, latest.md)
is on the main branch.
"""


def git(*args, env=None, check=True, data=None):
    p = subprocess.run(["git", *args], cwd=ROOT, env=env, input=data, capture_output=True,
                       text=data is None or isinstance(data, str))
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p


def fetch_previous(remote, branch=BRANCH):
    """True when the branch exists (it is then in FETCH_HEAD)."""
    return git("fetch", "--depth=1", remote, branch, check=False).returncode == 0


def previous_blob(path):
    p = git("rev-parse", "--verify", "--quiet", f"FETCH_HEAD:{path}", check=False)
    return p.stdout.strip() if p.returncode == 0 else None


def restore(remote="origin", files=LIVE_FILES, overwrite=False):
    """Copy live files from the live branch: only the missing ones (the workflows: never replace a file of this
    run), or all of them with overwrite=True (--refresh: Claude's persistent task sessions). Returns the paths."""
    if not fetch_previous(remote):
        print(f"{BRANCH} does not exist yet - nothing to restore")
        return []
    done = []
    for path in files:
        full = os.path.join(ROOT, path)
        if (os.path.exists(full) and not overwrite) or previous_blob(path) is None:
            continue
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f:
            f.write(subprocess.run(["git", "cat-file", "blob", f"FETCH_HEAD:{path}"], cwd=ROOT,
                                   capture_output=True, check=True).stdout)
        done.append(path)
    when = git("log", "-1", "--format=%s", "FETCH_HEAD", check=False).stdout.strip()
    print(("refreshed" if overwrite else "restored") + ": " + (", ".join(done) or "nothing") + f" (from: {when})")
    return done


def publish(remote="origin", files=LIVE_FILES, when=None, branch=BRANCH, readme=README, title="Live reports",
            strip=""):
    """One parentless commit with this run's files (+ the previous copy of the missing ones), force-pushed.
    strip: a folder prefix removed from the published paths (the dashboard's site/ goes to the branch root)."""
    had_previous = fetch_previous(remote, branch)
    entries, sources = [], {}
    for path in files:
        full = os.path.join(ROOT, path)
        dest = path[len(strip):] if strip and path.startswith(strip) else path
        if os.path.exists(full):
            blob = git("hash-object", "-w", full).stdout.strip()
            sources[dest] = "this run"
        elif had_previous and previous_blob(dest):
            blob = previous_blob(dest)
            sources[dest] = "kept from the previous copy"
        else:
            continue
        entries.append((blob, dest))
    readme_blob = git("hash-object", "-w", "--stdin", data=readme).stdout.strip()
    entries.append((readme_blob, "README.md"))
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, "index"),
                   GIT_AUTHOR_NAME="signal-bot", GIT_AUTHOR_EMAIL="signal-bot@users.noreply.github.com",
                   GIT_COMMITTER_NAME="signal-bot", GIT_COMMITTER_EMAIL="signal-bot@users.noreply.github.com")
        for blob, path in entries:
            git("update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env=env)
        tree = git("write-tree", env=env).stdout.strip()
        when = when or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
        commit = git("commit-tree", tree, "-m", f"{title} {when} UTC (replaced every run)", env=env).stdout.strip()
    git("push", "--force", remote, f"{commit}:refs/heads/{branch}")
    for path, how in sources.items():
        print(f"{path}: {how}")
    print(f"published {len(sources)} file(s) to {branch} as one commit ({commit[:8]})")
    return commit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--restore", action="store_true", help="copy missing live files from the live branch")
    ap.add_argument("--refresh", action="store_true",
                    help="overwrite the live files with the newest copy from the live branch (task sessions)")
    ap.add_argument("--remote", default="origin")
    args = ap.parse_args()
    try:
        if args.refresh or args.restore:
            restore(args.remote, overwrite=args.refresh)
        else:
            publish(args.remote)
    except RuntimeError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
