#!/usr/bin/env python3
"""
Build the web dashboard (Phase 16; engine/dashboard.py) and, with --publish, put it on GitHub Pages.

  python build_dashboard.py            write site/index.html from the report files (nothing is sent anywhere)
  python build_dashboard.py --publish  ... and force-push it to the branch gh-pages as ONE commit (no history)

Reads (every one may be missing - the page then says so): reports/latest.json and reports/dashboard_data.json
(hourly scan), reports/research.json (daily research run), the newest Claude briefing and daily review
(reports/claude/), reports/pine/. The workflows run `python publish_live.py --restore` first so the large files
are there. One-time setup: GitHub -> Settings -> Pages -> Source "Deploy from a branch" -> gh-pages / (root).
"""
import argparse
import datetime as dt
import json
import os
import sys

import publish_live
from engine import dashboard

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(ROOT, "reports")
SITE = os.path.join(ROOT, "site")
BRANCH = "gh-pages"
REPO = os.environ.get("GITHUB_REPOSITORY") or "mayastraglobal-ui/crypto-signal-agent"
README = "# gh-pages\n\nThe TradeSentry dashboard, rebuilt by the workflows (build_dashboard.py). One commit, no history.\n"


def load(name):
    p = os.path.join(REPORTS, name)
    if not os.path.exists(p):
        return None
    try:
        with open(p) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def newest(folder):
    d = os.path.join(REPORTS, "claude", folder)
    names = sorted(x for x in os.listdir(d) if x.endswith(".md")) if os.path.isdir(d) else []
    if not names:
        return None
    with open(os.path.join(d, names[-1]), encoding="utf-8", errors="replace") as f:
        return f"reports/claude/{folder}/{names[-1]}", f.read()


def inputs(now):
    pine_dir = os.path.join(REPORTS, "pine")
    return dict(latest=load("latest.json"), research=load("research.json"), candles=load("dashboard_data.json"),
                briefing=newest("briefings"), review=newest("daily"),
                pine_files=[f"reports/pine/{x}" for x in sorted(os.listdir(pine_dir)) if x.endswith(".pine")]
                if os.path.isdir(pine_dir) else [],
                repo_url=f"https://github.com/{REPO}", built_utc=now.strftime("%Y-%m-%d %H:%M"))


def build(now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    page = dashboard.render(inputs(now))
    os.makedirs(SITE, exist_ok=True)
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    with open(os.path.join(SITE, ".nojekyll"), "w") as f:
        f.write("")
    print(f"dashboard: site/index.html ({len(page.encode()) // 1024} KB)")
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--publish", action="store_true", help="force-push site/ to the gh-pages branch")
    args = ap.parse_args()
    build()
    if args.publish:
        try:
            publish_live.publish(files=["site/index.html", "site/.nojekyll"], branch=BRANCH, readme=README,
                                 title="Dashboard", strip="site/")
        except RuntimeError as e:
            sys.exit(str(e))


if __name__ == "__main__":
    main()
