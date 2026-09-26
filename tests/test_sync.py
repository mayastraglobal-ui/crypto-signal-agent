"""Two workflows adding to the same append-only file at the same time (26 Sep 2026: the Brain applied Claude's lab card
while the research run appended the engine's variant card; git's `merge=union` interleaved the two cards and both
broke). The `append` merge driver (append_merge.py), .gitattributes, the workflows' Save steps and
memory_guard.py --after-sync.

Run:  python -m unittest tests.test_sync -v
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import append_merge  # noqa: E402
import memory_guard  # noqa: E402
import test_brain  # noqa: E402
from engine import memory as mem  # noqa: E402
from engine import regime as rg  # noqa: E402
from engine import strategy_spec as SS  # noqa: E402
from engine import timeframes as tfm  # noqa: E402

LAB = test_brain.read(os.path.join(ROOT, "strategies_lab.yaml"))
HEAD = test_brain.lab_header(LAB)
LIB = yaml.safe_load(test_brain.read(os.path.join(ROOT, "strategies.yaml")))


def git(cwd, *args):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return p


def cards_text(n):
    """Two real lab cards that share many lines (targets, split ...) - the case union merging interleaves."""
    cards = yaml.safe_load(LAB) or []
    if len(cards) < 2:                                    # the lab may be empty: two variants of a library card
        base = next(c for c in LIB if c.get("targets"))
        cards = [dict(base, id="SYNC-A", version="1.0"), dict(base, id="SYNC-B", version="1.0")]
    return yaml.dump([cards[n]], sort_keys=False, allow_unicode=True, width=110)


def loads(text):
    try:
        lab = yaml.safe_load(text) or []
    except yaml.YAMLError:
        return None
    ok, problems, _, _ = SS.load_library(LIB, lab, rg.LABELS, tfm.TRADE_ORDER)
    return None if [k for k in problems if str(k).startswith("lab")] else sorted(SS.key(c) for c in ok if c.get("lab"))


class Driver(unittest.TestCase):
    def test_merge_rules(self):
        m = append_merge.merge
        self.assertEqual(m("a\n", "a\nb\n", "a\nc\n"), "a\nb\nc\n", "both additions, one after the other")
        self.assertEqual(m("a\n", "a\nb\n", "a\n"), "a\nb\n")
        self.assertEqual(m("a\n", "a\n", "a\nc\n"), "a\nc\n")
        self.assertEqual(m("a\n", "a\nb\n", "a\nb\n"), "a\nb\n", "the same addition is kept once")
        self.assertEqual(m("a", "ab", "ac"), "ab\nc")
        self.assertIsNone(m("a\n", "A\nb\n", "a\nc\n"), "a changed line is not an append-only merge")
        self.assertIsNone(m("a\nb\n", "a\n", "a\nb\nc\n"), "a deleted line neither")


class GitMerge(unittest.TestCase):
    """The real case in a real repository: main + a header-only lab; two branches each append one card."""

    def repo(self, attr):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        git(tmp, "init", "-q", "-b", "main")
        git(tmp, "config", "user.email", "t@t")
        git(tmp, "config", "user.name", "t")
        git(tmp, "config", "merge.append.driver", f"{sys.executable} {os.path.join(ROOT, 'append_merge.py')} %O %A %B")
        with open(os.path.join(tmp, ".gitattributes"), "w") as f:
            f.write(f"strategies_lab.yaml {attr}\n")
        with open(os.path.join(tmp, "strategies_lab.yaml"), "w") as f:
            f.write(HEAD)
        git(tmp, "add", "-A")
        git(tmp, "commit", "-qm", "base")
        for br, n in (("brain", 0), ("research", 1)):
            git(tmp, "checkout", "-q", "-b", br, "main")
            with open(os.path.join(tmp, "strategies_lab.yaml"), "a") as f:
                f.write(cards_text(n))
            git(tmp, "commit", "-qam", br)
        git(tmp, "checkout", "-q", "main")
        git(tmp, "merge", "-q", "brain")                   # the Brain pushed first
        git(tmp, "checkout", "-q", "research")
        p = git(tmp, "rebase", "main")                     # the research run's `git pull --rebase`
        return tmp, p

    def test_union_interleaves_and_append_keeps_both_cards(self):
        want = sorted({*loads(HEAD + cards_text(0)), *loads(HEAD + cards_text(1))})
        tmp, p = self.repo("merge=union")                  # the old setting: a "clean" merge ...
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertNotEqual(loads(test_brain.read(os.path.join(tmp, "strategies_lab.yaml"))), want,
                            "... that breaks the cards (this is what happened on 26 Sep 2026)")
        tmp, p = self.repo("merge=append")
        self.assertEqual(p.returncode, 0, p.stderr)
        text = test_brain.read(os.path.join(tmp, "strategies_lab.yaml"))
        self.assertEqual(loads(text), want, "both cards whole")
        self.assertTrue(text.startswith(HEAD + cards_text(0)), "the pushed card first, then ours")

    def test_a_changed_line_is_a_conflict_not_a_merge(self):
        tmp, _ = self.repo("merge=append")
        git(tmp, "checkout", "-q", "-b", "edit", "main")
        with open(os.path.join(tmp, "strategies_lab.yaml")) as f:
            text = f.read()
        with open(os.path.join(tmp, "strategies_lab.yaml"), "w") as f:
            f.write(text.replace("# ", "#  ", 1) + "# more\n")
        git(tmp, "commit", "-qam", "edit")
        git(tmp, "checkout", "-q", "research")
        self.assertNotEqual(git(tmp, "rebase", "edit").returncode, 0)


class Setup(unittest.TestCase):
    def test_every_append_only_file_uses_the_driver(self):
        attrs = test_brain.read(os.path.join(ROOT, ".gitattributes"))
        rules = dict(ln.split() for ln in attrs.splitlines() if ln.strip() and not ln.startswith("#"))
        for path in mem.APPEND_ONLY + ["events.yaml"]:
            self.assertEqual(rules.get(path), "merge=append", path)
        self.assertNotIn("merge=union", attrs.replace("`merge=union`", ""))

    def test_workflows_register_the_driver_and_check_before_pushing(self):
        for name in ("scan.yml", "research.yml", "brain.yml", "pine.yml"):
            text = test_brain.read(os.path.join(ROOT, ".github", "workflows", name))
            save = text[text.index("git config user.name"):]
            self.assertIn('git config merge.append.driver "python3 append_merge.py %O %A %B"', save, name)
            self.assertLess(save.index("merge.append.driver"), save.index("git pull --rebase"), name)
            self.assertLess(save.index("git pull --rebase"), save.index("memory_guard.py --after-sync"), name)
            self.assertLess(save.index("memory_guard.py --after-sync"), save.index("git push"), name)


class AfterSync(unittest.TestCase):
    def test_a_broken_lab_card_is_found(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        shutil.copy(os.path.join(ROOT, "strategies.yaml"), tmp)
        with mock.patch.object(memory_guard, "ROOT", tmp):
            with open(os.path.join(tmp, "strategies_lab.yaml"), "w") as f:
                f.write(HEAD + cards_text(0) + cards_text(1))
            self.assertEqual(memory_guard.lab_problems(), [])
            broken = (HEAD + cards_text(0)).replace("  time_stop_bars:", "  #time_stop_bars:")
            with open(os.path.join(tmp, "strategies_lab.yaml"), "w") as f:
                f.write(broken)
            probs = memory_guard.lab_problems()
            self.assertTrue(probs and "time_stop_bars" in probs[0], probs)
            with open(os.path.join(tmp, "strategies_lab.yaml"), "w") as f:
                f.write(HEAD + "- id: [\n")
            self.assertIn("not readable", memory_guard.lab_problems()[0])


if __name__ == "__main__":
    unittest.main()
