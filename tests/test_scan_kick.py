"""2026-10-26 (operator: "no scan for 2 hours"): GitHub started the hourly scan only every 3-5 hours. The live watcher
(always on) starts a workflow (workflow_dispatch on main) when none waits or runs and the newest run started more
than 75 minutes ago (the research: 26 hours); it checks every 20 minutes; without Actions permission it is off."""
import datetime as dt
import os
import sys
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import live_watcher as LW  # noqa: E402

NOW = int(dt.datetime(2026, 10, 26, 8, 44, tzinfo=dt.timezone.utc).timestamp() * 1000)


def iso(minutes_ago):
    return (dt.datetime.fromtimestamp(NOW / 1000, dt.timezone.utc) - dt.timedelta(minutes=minutes_ago)) \
        .strftime("%Y-%m-%dT%H:%M:%SZ")


class Resp:
    def __init__(self, code, body=None):
        self.status_code, self.body = code, body or {}

    def json(self):
        return self.body


class FakeGitHub:
    def __init__(self, runs, dispatch_code=204, list_code=200):
        self.runs, self.dispatch_code, self.list_code, self.calls = runs, dispatch_code, list_code, []

    def __call__(self, method, url, **kw):
        self.calls.append((method, url.split("/repos/")[1]))
        if method == "GET":
            wf = url.split("/workflows/")[1].split("/")[0]
            return Resp(self.list_code, dict(workflow_runs=self.runs.get(wf, [])))
        return Resp(self.dispatch_code)


class Kick(unittest.TestCase):
    def setUp(self):
        p = mock.patch.dict(os.environ, {"JOURNAL_GITHUB_TOKEN": "github_pat_x"})
        p.start()
        self.addCleanup(p.stop)

    def dispatched(self, gh):
        return [u.split("/workflows/")[1].split("/")[0] for m, u in gh.calls if m == "POST"]

    def test_starts_a_late_scan_only(self):
        gh = FakeGitHub({"scan.yml": [dict(status="completed", created_at=iso(250))],
                         "research.yml": [dict(status="completed", created_at=iso(8 * 60))]})
        k = LW.ScanKick(http=gh)
        notes = k.check(NOW)
        self.assertEqual(self.dispatched(gh), ["scan.yml"])
        self.assertIn("started scan.yml (GitHub's schedule was 250 min late)", notes[0])
        self.assertIn("checked", k.status(NOW + 60_000))
        self.assertEqual(k.check(NOW + 5 * 60_000), [])                 # every 20 minutes, not every pass
        self.assertEqual(len(gh.calls), 3)

    def test_on_time_or_running_starts_nothing(self):
        gh = FakeGitHub({"scan.yml": [dict(status="completed", created_at=iso(50))],
                         "research.yml": [dict(status="in_progress", created_at=iso(30 * 60))]})
        self.assertEqual(LW.ScanKick(http=gh).check(NOW), [])
        self.assertEqual(self.dispatched(gh), [])
        gh = FakeGitHub({"scan.yml": [dict(status="queued", created_at=iso(300))]})
        LW.ScanKick(http=gh).check(NOW)
        self.assertNotIn("scan.yml", self.dispatched(gh))

    def test_research_after_26_hours(self):
        gh = FakeGitHub({"scan.yml": [dict(status="completed", created_at=iso(10))],
                         "research.yml": [dict(status="completed", created_at=iso(27 * 60))]})
        LW.ScanKick(http=gh).check(NOW)
        self.assertEqual(self.dispatched(gh), ["research.yml"])

    def test_without_actions_permission_it_is_off_and_says_so(self):
        gh = FakeGitHub({"scan.yml": [dict(status="completed", created_at=iso(250))]}, dispatch_code=403)
        k = LW.ScanKick(http=gh)
        notes = k.check(NOW)
        self.assertIn("Actions: Read and write", notes[0])
        self.assertIn("⚠️", k.status(NOW))
        self.assertEqual(k.check(NOW + 30 * 60_000), [])                # quiet for 6 hours
        with mock.patch.dict(os.environ, {"JOURNAL_GITHUB_TOKEN": ""}):
            self.assertEqual(LW.ScanKick(http=gh).check(NOW), [])      # no token: nothing at all
            self.assertIsNone(LW.ScanKick(http=gh).status(NOW))

    def test_wired_into_the_loop_and_status(self):
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn("for note in self.kick.check(self.now_fn()):", src)
        self.assertIn("scan_kick=self.kick.status(now_ms)", src)
        self.assertIn("Late-scan kick:", open(os.path.join(ROOT, "engine", "live.py"), encoding="utf-8").read())


if __name__ == "__main__":
    unittest.main()
