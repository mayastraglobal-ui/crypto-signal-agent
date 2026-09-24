"""Housekeeping tests: the large report files go to branch live-reports as ONE commit (no history),
missing files are carried over, the hourly scan can restore research.json, main never gets them.

Run:  python -m unittest discover -s tests -v
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
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
