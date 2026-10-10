"""The live watcher's heartbeat (2026-10-10): the watcher tells GitHub every hour that it runs; the hourly scan emails
an ALERT when it goes silent for 2 hours and a FIXED when it is back."""
import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import journal_review as JRV  # noqa: E402
import live_watcher as LW  # noqa: E402
import notify  # noqa: E402
from engine import weekly_review as WR  # noqa: E402

T0 = 1_791_158_400_000                     # 2026-10-05 00:00 UTC
H = 3_600_000


class FakeGitHub:
    """Just the git-data calls the heartbeat uses."""

    def __init__(self, branch=False, fail=False):
        self.branch, self.fail, self.calls, self.files = branch, fail, [], []

    def __call__(self, method, url, headers=None, json=None, **kw):
        path = url.split("/repos/")[1].split("/", 2)[2]
        self.calls.append((method, path))
        r = mock.Mock()
        if self.fail:
            r.status_code, body = 500, dict(message="boom")
        elif method == "POST" and path == "git/trees":
            assert json["tree"][0]["path"] == "heartbeat.json"
            self.files.append(json["tree"][0]["content"])
            r.status_code, body = 201, dict(sha="t")
        elif method == "POST" and path == "git/commits":
            assert json["parents"] == []                          # one commit, no history builds up
            r.status_code, body = 201, dict(sha="c")
        elif method == "PATCH" and path == "git/refs/heads/watcher-heartbeat":
            assert json["force"] is True
            r.status_code, body = (200, {}) if self.branch else (422, dict(message="Reference does not exist"))
        elif method == "POST" and path == "git/refs":
            assert json["ref"] == "refs/heads/watcher-heartbeat"
            self.branch = True
            r.status_code, body = 201, {}
        else:
            r.status_code, body = 404, {}
        r.json.return_value = body
        return r


class Heartbeat(unittest.TestCase):
    def test_off_without_a_token(self):
        gh = FakeGitHub()
        with mock.patch.dict(os.environ, {"JOURNAL_GITHUB_TOKEN": ""}):
            hb = LW.Heartbeat(http=gh)
            self.assertEqual(hb.push(T0, {}), (False, "off"))
            self.assertIsNone(hb.status(T0))
        self.assertEqual(gh.calls, [])

    def test_hourly_on_its_own_branch_creating_it_once(self):
        gh = FakeGitHub()
        with mock.patch.dict(os.environ, {"JOURNAL_GITHUB_TOKEN": "t"}):
            hb = LW.Heartbeat(http=gh)
            self.assertEqual(hb.push(T0, dict(fails=0)), (True, "sent"))
            self.assertTrue(gh.branch)
            self.assertEqual(json.loads(gh.files[-1])["utc"], "2026-10-05 00:00")
            n = len(gh.calls)
            self.assertEqual(hb.push(T0 + 30 * 60_000, {}), (True, "not due"))
            self.assertEqual(len(gh.calls), n)                                  # not yet an hour: no call
            self.assertEqual(hb.push(T0 + H, {})[1], "sent")
            self.assertNotIn(("POST", "git/refs"), gh.calls[n:])                  # the branch exists now
            self.assertIn("GitHub emails you", hb.status(T0 + H))
        self.assertFalse(any("main" in p or "journal" in p for _, p in gh.calls))   # only its own branch

    def test_a_failure_is_retried_at_the_next_pass(self):
        gh = FakeGitHub(fail=True)
        with mock.patch.dict(os.environ, {"JOURNAL_GITHUB_TOKEN": "t"}):
            hb = LW.Heartbeat(http=gh)
            ok, note = hb.push(T0, {})
            self.assertFalse(ok)
            self.assertIn("500", note)
            self.assertIn("failing", hb.status(T0))
            gh.fail = False
            self.assertEqual(hb.push(T0 + 5 * 60_000, {}), (True, "sent"))       # 5 minutes later, not an hour


class Health(unittest.TestCase):
    def test_states(self):
        now = T0 + 10 * H
        self.assertEqual(JRV.health(None, now)["state"], "OFF")
        self.assertEqual(JRV.health("not json", now)["state"], "OFF")
        ok = JRV.health(json.dumps(dict(utc="2026-10-05 09:00")), now)
        self.assertEqual((ok["state"], ok["age_min"]), ("OK", 60))
        silent = JRV.health(json.dumps(dict(utc="2026-10-05 07:30", open_trades=1)), now)
        self.assertEqual((silent["state"], silent["age_min"]), ("SILENT", 150))
        self.assertIn("SILENT: no heartbeat for 2h30m", silent["text"])


class Emails(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.rep = os.path.join(self.tmp, "reports")
        os.makedirs(self.rep)
        self.sent = []
        for name, value in (("REPORTS", self.rep), ("send_mail", lambda m: self.sent.append(m) or True),
                            ("pages_base", lambda: "https://o.github.io/r/")):
            p = mock.patch.object(notify, name, value)
            p.start()
            self.addCleanup(p.stop)

    def health(self, h):
        with open(os.path.join(self.rep, "watcher_health.json"), "w") as f:
            json.dump(h, f)

    def test_alert_once_when_silent_fixed_once_when_back(self):
        notify.watcher_email()                                                   # no file: nothing
        self.health(dict(state="OFF"))
        notify.watcher_email()
        self.assertEqual(self.sent, [])
        silent = JRV.health(json.dumps(dict(utc="2026-10-05 07:30", open_trades=2)), T0 + 10 * H)
        self.health(silent)
        notify.watcher_email()
        notify.watcher_email()
        self.assertEqual([m["subject"] for m in self.sent], ["! Live watcher silent · no Telegram alerts"])
        self.assertIn("2_start_watcher.bat", self.sent[0]["text"])
        self.assertIn("check their stops on OKX", self.sent[0]["text"])
        self.sent.clear()
        self.health(JRV.health(json.dumps(dict(utc="2026-10-05 11:00")), T0 + 11 * H))
        notify.watcher_email()
        notify.watcher_email()
        self.assertEqual(len(self.sent), 1)
        self.assertIn("Fixed", self.sent[0]["subject"])


class Review(unittest.TestCase):
    def test_the_weekly_system_check_uses_the_heartbeat(self):
        now = dt.datetime(2026, 10, 18, 5, tzinfo=dt.timezone.utc)
        ms = int(now.timestamp() * 1000)
        ok = JRV.health(json.dumps(dict(utc="2026-10-18 04:30")), ms)
        rv = WR.build(now, pd.DataFrame(), {}, {}, {}, [], [], dict(last_entry_utc=None), watcher=ok)
        self.assertIn(dict(ok=True, text=ok["text"]), rv["system"])
        silent = JRV.health(json.dumps(dict(utc="2026-10-17 20:00")), ms)
        rv = WR.build(now, pd.DataFrame(), {}, {}, {}, [], [], dict(last_entry_utc=None), watcher=silent)
        self.assertIn(dict(ok=False, text=silent["text"]), rv["system"])
        rv = WR.build(now, pd.DataFrame(), {}, {}, {}, [], [], dict(last_entry_utc=None),
                      watcher=dict(state="OFF"))
        self.assertTrue(any("synced, no alert recorded yet" in s["text"] for s in rv["system"]))   # journal fallback


if __name__ == "__main__":
    unittest.main()
