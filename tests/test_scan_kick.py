"""2026-10-26 (operator: "no scan for 2 hours"): GitHub started the hourly scan only every 3-5 hours. The live watcher
(always on) starts a workflow (workflow_dispatch on main) when none waits or runs and - since 2026-10-31 ("hourly scan
is too late") - the hourly ones (scan :07, Brain :47) have no run since this hour's minute (the research: 26 hours
old); it checks every 5 minutes; without Actions permission it is off."""
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


FRESH = [dict(status="completed", created_at=iso(60))]        # a research run 1 hour old: not due


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
                         "brain.yml": [dict(status="completed", created_at=iso(10))],
                         "research.yml": [dict(status="completed", created_at=iso(8 * 60))]})
        k = LW.ScanKick(http=gh)
        notes = k.check(NOW)
        self.assertEqual(self.dispatched(gh), ["scan.yml"])
        self.assertIn("started scan.yml (no run since 08:07 UTC)", notes[0])
        self.assertIn("checked", k.status(NOW + 60_000))
        self.assertEqual(k.check(NOW + 2 * 60_000), [])                 # every 5 minutes, not every pass
        self.assertEqual(len(gh.calls), 4)

    def test_one_run_per_clock_hour(self):
        # NOW = 08:44 UTC: this hour's scan minute is 08:07; a run from 07:58 (within 10 minutes before it) counts
        for ago, start in ((37, False), (46, False), (55, True), (70, True)):
            gh = FakeGitHub({"scan.yml": [dict(status="completed", created_at=iso(ago))],
                             "brain.yml": [dict(status="completed", created_at=iso(1))], "research.yml": FRESH})
            LW.ScanKick(http=gh).check(NOW)
            self.assertEqual("scan.yml" in self.dispatched(gh), start, ago)
        # before minute 7 the due time is the previous hour's :07 (07:07 for a check at 08:03)
        early = NOW - 41 * 60_000
        gh = FakeGitHub({"scan.yml": [dict(status="completed", created_at=iso(80))],
                         "brain.yml": [dict(status="completed", created_at=iso(1))], "research.yml": FRESH})
        LW.ScanKick(http=gh).check(early)
        self.assertEqual(self.dispatched(gh), [])
        self.assertEqual(LW.ScanKick().check_ms, 5 * 60_000)

    def test_brain_watchdog_kicked_after_minute_47(self):
        later = NOW + 10 * 60_000                                        # 08:54: this hour's Brain minute 08:47 passed
        gh = FakeGitHub({"scan.yml": [dict(status="completed", created_at=iso(30))],
                         "brain.yml": [dict(status="completed", created_at=iso(55))], "research.yml": FRESH})
        notes = LW.ScanKick(http=gh).check(later)
        self.assertEqual(self.dispatched(gh), ["brain.yml"])
        self.assertIn("no run since 08:47 UTC", notes[0])

    def test_on_time_or_running_starts_nothing(self):
        gh = FakeGitHub({"scan.yml": [dict(status="completed", created_at=iso(30))],
                         "brain.yml": [dict(status="completed", created_at=iso(50))],
                         "research.yml": [dict(status="in_progress", created_at=iso(30 * 60))]})
        self.assertEqual(LW.ScanKick(http=gh).check(NOW), [])
        self.assertEqual(self.dispatched(gh), [])
        gh = FakeGitHub({"scan.yml": [dict(status="queued", created_at=iso(300))]})
        LW.ScanKick(http=gh).check(NOW)
        self.assertNotIn("scan.yml", self.dispatched(gh))

    def test_research_after_26_hours(self):
        gh = FakeGitHub({"scan.yml": [dict(status="completed", created_at=iso(10))],
                         "brain.yml": [dict(status="completed", created_at=iso(10))],
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

    def test_scheduled_scans_four_chances_an_hour_with_a_gate(self):
        wf = open(os.path.join(ROOT, ".github", "workflows", "scan.yml"), encoding="utf-8").read()
        for m in (7, 22, 37, 52):
            self.assertIn(f'cron: "{m} * * * *"', wf)
        self.assertIn("needs: gate", wf)
        self.assertIn("needs.gate.outputs.run == 'true'", wf)
        self.assertIn('[ "$age" -lt 45 ] && run=false', wf)
        self.assertIn('gh run cancel "${{ github.run_id }}"', wf)
        self.assertIn('if [ "${{ github.event_name }}" = "schedule" ]; then', wf)    # a started run always scans
        brain = open(os.path.join(ROOT, ".github", "workflows", "brain.yml"), encoding="utf-8").read()
        self.assertIn('cron: "17 * * * *"', brain)

    def test_wired_into_the_loop_and_status(self):
        src = open(os.path.join(ROOT, "live_watcher.py"), encoding="utf-8").read()
        self.assertIn("for note in self.kick.check(self.now_fn()):", src)
        self.assertIn("scan_kick=self.kick.status(now_ms)", src)
        self.assertIn("Late-scan kick:", open(os.path.join(ROOT, "engine", "live.py"), encoding="utf-8").read())


if __name__ == "__main__":
    unittest.main()
