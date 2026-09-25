"""Housekeeping tests: the large report files go to branch live-reports as ONE commit (no history),
missing files are carried over, the hourly scan can restore research.json, main never gets them.

Run:  python -m unittest discover -s tests -v
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import brain_pack  # noqa: E402
import publish_live  # noqa: E402

ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")


def sh(cwd, *args):
    p = subprocess.run(list(args), cwd=cwd, env=ENV, capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    return p.stdout


class LiveBranch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.remote = os.path.join(self.tmp, "remote.git")
        sh(self.tmp, "git", "init", "-q", "--bare", "-b", "main", self.remote)
        seed = self.clone("seed")
        with open(os.path.join(seed, "README.md"), "w") as f:
            f.write("main\n")
        sh(seed, "git", "add", "README.md")
        sh(seed, "git", "commit", "-q", "-m", "main")
        sh(seed, "git", "push", "-q", "origin", "HEAD:main")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def clone(self, name):
        path = os.path.join(self.tmp, name)
        sh(self.tmp, "git", "clone", "-q", self.remote, path)
        shutil.copy(os.path.join(ROOT, "publish_live.py"), path)
        os.makedirs(os.path.join(path, "reports"), exist_ok=True)
        return path

    def write(self, repo, name, text):
        with open(os.path.join(repo, "reports", name), "w") as f:
            f.write(text)

    def run_script(self, repo, *args):
        return subprocess.run([sys.executable, "publish_live.py", *args], cwd=repo, env=ENV,
                              capture_output=True, text=True)

    def live(self, path):
        return sh(self.remote, "git", "show", f"{publish_live.BRANCH}:{path}")

    def commits(self):
        return int(sh(self.remote, "git", "rev-list", "--count", publish_live.BRANCH).strip())

    def test_one_commit_carry_over_and_restore(self):
        hourly = self.clone("hourly")
        self.write(hourly, "latest.json", '{"run": 1}')
        self.write(hourly, "smc.json", '{"smc": 1}')
        p = self.run_script(hourly)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual((self.live("reports/latest.json"), self.commits()), ('{"run": 1}', 1))
        self.assertIn("live-reports", self.live("README.md"))

        research = self.clone("research")                    # the daily run only makes research.json
        self.write(research, "research.json", '{"research": 1}')
        self.assertEqual(self.run_script(research).returncode, 0)
        self.assertEqual(self.live("reports/research.json"), '{"research": 1}')
        self.assertEqual(self.live("reports/latest.json"), '{"run": 1}')     # kept from the previous copy
        self.assertEqual(self.commits(), 1)                                # still no history

        hourly2 = self.clone("hourly2")                     # next hourly scan: restore, then publish
        p = self.run_script(hourly2, "--restore")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        with open(os.path.join(hourly2, "reports", "research.json")) as f:
            self.assertEqual(f.read(), '{"research": 1}')
        self.write(hourly2, "latest.json", '{"run": 2}')
        self.assertEqual(self.run_script(hourly2).returncode, 0)
        self.assertEqual((self.live("reports/latest.json"), self.live("reports/research.json"), self.commits()),
                         ('{"run": 2}', '{"research": 1}', 1))
        self.assertEqual(self.live("reports/smc.json"), '{"smc": 1}')
        # main is untouched: only the seed commit, no report files
        self.assertEqual(int(sh(self.remote, "git", "rev-list", "--count", "main").strip()), 1)
        self.assertNotIn("reports", sh(self.remote, "git", "ls-tree", "--name-only", "main"))

    def test_restore_before_the_branch_exists_is_harmless(self):
        repo = self.clone("first")
        p = self.run_script(repo, "--restore")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("does not exist yet", p.stdout)
        self.assertFalse(os.path.exists(os.path.join(repo, "reports", "research.json")))

    def test_restore_never_overwrites_a_file_of_this_run(self):
        a = self.clone("a")
        self.write(a, "research.json", "old")
        self.run_script(a)
        b = self.clone("b")
        self.write(b, "research.json", "new")
        self.run_script(b, "--restore")
        with open(os.path.join(b, "reports", "research.json")) as f:
            self.assertEqual(f.read(), "new")


class TaskSessionSecondRun(LiveBranch):
    """Claude's task sessions are persistent: the 14:20 briefing reused the 00:26 latest.json. A second run in the
    same session must get the newest copies (--refresh) and the fact sheet must warn loudly about old ones."""

    def rep(self, when):
        return json.dumps(dict(generated_utc=when, daily=dict(data_state="GOOD"), position_book_text=["book"],
                               daily_lines=["x"], signals=[], validation_signals=[], watching=[], risk={}))

    def md(self, repo, when):
        with open(os.path.join(repo, "reports", "latest.md"), "w") as f:
            f.write(f"# Crypto Signal Report\n\n**Updated:** x Beijing time ({when} UTC) · data: Binance\n")

    def fact_sheet(self, repo, live):
        with mock.patch.object(brain_pack, "REPORTS", os.path.join(repo, "reports")):
            return "\n".join(brain_pack.pack("briefing", dt.datetime(2026, 9, 25, 6, 20, tzinfo=dt.timezone.utc), live))

    def test_second_run_in_the_same_session(self):
        scan = self.clone("scan")
        self.write(scan, "latest.json", self.rep("2026-09-25 00:26"))
        self.assertEqual(self.run_script(scan).returncode, 0)
        task = self.clone("task")                                  # the persistent task session, first run
        p = self.run_script(task, "--refresh")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("refreshed: reports/latest.json", p.stdout)
        self.md(task, "2026-09-25 00:26")
        live = brain_pack.live_status(task)
        self.assertEqual((live["differs"], live["missing"]), ([], []))
        self.assertNotIn("STALE ENGINE FILES", self.fact_sheet(task, live))

        self.write(scan, "latest.json", self.rep("2026-09-25 06:24"))  # later hourly scans publish a new copy
        self.assertEqual(self.run_script(scan).returncode, 0)
        self.md(task, "2026-09-25 06:24")                             # the task's git pull brings the new latest.md

        self.run_script(task, "--restore")                          # the old start command: keeps the OLD copy
        with open(os.path.join(task, "reports", "latest.json")) as f:
            self.assertIn("00:26", f.read())
        live = brain_pack.live_status(task)
        self.assertEqual(live["differs"], ["reports/latest.json"])
        sheet = self.fact_sheet(task, live)
        self.assertTrue(sheet.startswith("!!! STALE ENGINE FILES"))
        self.assertIn("latest.json is from 2026-09-25 00:26 UTC, but reports/latest.md on main was updated "
                      "2026-09-25 06:24 UTC", sheet)
        self.assertIn("reports/latest.json is not the newest copy on live-reports", sheet)

        p = self.run_script(task, "--refresh")                      # the new start command: always the newest
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        with open(os.path.join(task, "reports", "latest.json")) as f:
            self.assertIn("06:24", f.read())
        live = brain_pack.live_status(task)
        self.assertEqual((live["differs"], live["missing"]), ([], []))
        sheet = self.fact_sheet(task, live)
        self.assertNotIn("STALE", sheet)
        self.assertIn("Engine report: 2026-09-25 06:24 UTC", sheet)

    def test_warnings_without_the_live_branch(self):
        self.assertEqual(brain_pack.md_updated("**Updated:** 2026-09-25 14:18 Beijing time (2026-09-25 06:18 UTC) ·"),
                         "2026-09-25 06:18")
        rep = dict(generated_utc="2026-09-25 06:18")
        md = "**Updated:** x (2026-09-25 06:18 UTC)"
        self.assertEqual(brain_pack.stale_warnings(rep, md, None), [])
        self.assertEqual(len(brain_pack.stale_warnings(dict(generated_utc="2026-09-25 05:18"), md, None)), 1)
        self.assertEqual(brain_pack.stale_warnings(None, md, None), [])                 # missing: said elsewhere
        self.assertEqual(brain_pack.live_status(self.clone("nolive")), None)            # no live branch yet
        self.assertEqual(len(brain_pack.stale_warnings(rep, md, dict(commit="c", differs=[],
                                                                      missing=["reports/research.json"]))), 1)

    def test_task_start_commands_refresh(self):
        with open(os.path.join(ROOT, "tasks", "COMMON.md")) as f:
            text = f.read()
        self.assertIn("python publish_live.py --refresh", text)
        self.assertNotIn("publish_live.py --restore", text)
        self.assertIn("STALE ENGINE FILES", text)
        self.assertEqual(set(brain_pack.LIVE_FILES) - set(publish_live.LIVE_FILES), set())


class MainStaysSmall(unittest.TestCase):
    def test_large_files_are_ignored_on_main(self):
        with open(os.path.join(ROOT, ".gitignore")) as f:
            ignored = f.read().split()
        for path in publish_live.LIVE_FILES:
            self.assertIn(path, ignored)
        for keep in ("reports/latest.md", "reports/signals_log.csv", "reports/strategy_scoreboard.csv"):
            self.assertNotIn(keep, ignored)

    def test_workflows_restore_and_publish(self):
        for wf in ("scan.yml", "research.yml"):
            with open(os.path.join(ROOT, ".github", "workflows", wf)) as f:
                text = f.read()
            self.assertIn("python publish_live.py", text, wf)
            self.assertLess(text.index("git push"), text.index("python publish_live.py\n"), wf)   # main first
        with open(os.path.join(ROOT, ".github", "workflows", "scan.yml")) as f:
            text = f.read()
        self.assertLess(text.index("publish_live.py --restore"), text.index("python scanner.py"))


if __name__ == "__main__":
    unittest.main()
