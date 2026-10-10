"""Journal sync (operator request 2026-10-06): every alert's plan result, the operator's /result, the upload to the
branch `journal`, and the review the hourly scan writes. Offline: Telegram and GitHub are mocked."""
import base64
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tests"))
import journal_review as JRV  # noqa: E402
import live_watcher as LW  # noqa: E402
from engine import emails as em  # noqa: E402
from engine import journal as jr  # noqa: E402
from engine import mailfacts as mf  # noqa: E402
from test_telegram_bot import M5, T0, alert, bars  # noqa: E402


def row(aid, event, result=None, strategy="S", tf="5m", time="2026-10-05 00:00"):
    return dict(time_utc=time, alert_id=aid, event=event, label="PAPER", coin="SOL", side="LONG", tf=tf,
                strategy=strategy, version="1.0", entry="100", stop="99", tp1="102", tp2="", tp3="", price="",
                result_r="" if result is None else str(result))


def journal(*groups):
    rows = []
    for g in groups:
        rows += g
    return rows


class Review(unittest.TestCase):
    NOW = T0 + 86_400_000

    def test_groups_plan_results_and_the_gap(self):
        rows = []
        for i in range(6):                                   # took: plan +1.0R, the operator made +0.6R
            rows += [row(f"t{i}", "alert"), row(f"t{i}", "took"), row(f"t{i}", "tp1", 1.0), row(f"t{i}", "plan", 1.0),
                     row(f"t{i}", "your result", 0.6)]
        for i in range(5):                                   # skipped: plan +1.5R
            rows += [row(f"s{i}", "alert"), row(f"s{i}", "skipped"), row(f"s{i}", "plan", 1.5)]
        rows += [row("n0", "alert"), row("n0", "plan not filled")]
        rv = jr.review(rows, self.NOW)
        g = rv["all"]
        self.assertEqual((g["alerts"], g["took"], g["skipped"], g["no_answer"]), (12, 6, 5, 1))
        self.assertAlmostEqual(g["plan_took"]["avg_r"], 1.0)
        self.assertAlmostEqual(g["plan_skipped"]["avg_r"], 1.5)
        self.assertAlmostEqual(g["gap"]["avg_r"], -0.4)
        text = " ".join(rv["findings"])
        self.assertIn("skipped did better", text)
        self.assertIn("below the plan", text)
        self.assertIn("never changes them", text)            # report only: the operator decides about costs
        self.assertEqual(rv["recent"]["alerts"], 12)
        self.assertEqual(rv["per_strategy"][0]["cell"], "S 5m")
        md = "\n".join(jr.lines(rv))
        self.assertIn("took 6", md)

    def test_few_trades_give_no_finding_and_old_journals_still_count(self):
        rows = [row("a", "took"), row("a", "stop", -1.0)]    # before journal sync: no alert / plan rows
        rv = jr.review(rows, self.NOW)
        self.assertEqual(rv["all"]["took"], 1)
        self.assertAlmostEqual(rv["all"]["plan_took"]["avg_r"], -1.0)     # the follow-up's result is the plan's
        self.assertEqual(rv["findings"], [])
        self.assertEqual(jr.review([], self.NOW)["findings"], ["No alert in your journal yet."])

    def test_early_close_and_reminders(self):
        rows = []
        for i in range(12):
            rows += [row(f"x{i}", "alert"), row(f"x{i}", "plan", 0.5)]
        for i in range(5):
            rows += [row(f"c{i}", "alert"), row(f"c{i}", "took"), row(f"c{i}", "closed by you"),
                     row(f"c{i}", "plan", 2.0), row(f"c{i}", "your result", 0.5)]
        for i in range(6):
            rows += [row(f"m{i}", "alert"), row(f"m{i}", "took"), row(f"m{i}", "plan", 1.0)]
        text = " ".join(jr.review(rows, self.NOW)["findings"])
        self.assertIn("Closing early cost you 1.50R", text)
        self.assertIn("got no button", text)
        self.assertIn("/result", text)

    def test_parse_result(self):
        self.assertEqual(jr.parse_result("1.2"), (None, 1.2))
        self.assertEqual(jr.parse_result("+1,5R"), (None, 1.5))
        self.assertEqual(jr.parse_result("abc123 -1"), ("abc123", -1.0))
        for bad in ("", "x", "50", "1 2 3"):
            with self.assertRaises(ValueError):
                jr.parse_result(bad)

    def test_weekly_email_part(self):
        rows = []
        for i in range(6):
            rows += [row(f"t{i}", "alert", time="2026-10-05 00:00"), row(f"t{i}", "took"), row(f"t{i}", "plan", 1.0),
                     row(f"t{i}", "your result", 0.6)]
        j = mf.journal_facts(jr.review(rows, self.NOW))
        self.assertEqual((j["alerts"], j["took"]), (6, 6))
        self.assertIsNone(mf.journal_facts(None))
        self.assertIsNone(mf.journal_facts(jr.review([], self.NOW)))
        w = dict(week_no=41, days="1–7 Oct", journal=j, funnel={}, live={}, paper={}, missed={})
        html = json.dumps(em.weekly(w), default=str)
        self.assertIn("Your own trades", html)
        self.assertIn("below the plan", html)

    def test_review_script_writes_both_files(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "my_trades.csv")
            pd.DataFrame([row("a", "alert"), row("a", "took"), row("a", "plan", 1.0)], columns=jr.COLS).to_csv(
                src, index=False)
            out_j, out_m = os.path.join(d, "r.json"), os.path.join(d, "r.md")
            with mock.patch.object(JRV, "OUT_JSON", out_j), mock.patch.object(JRV, "OUT_MD", out_m), \
                    mock.patch.object(sys, "argv", ["journal_review.py", "--file", src]), mock.patch("builtins.print"):
                JRV.write.__defaults__ = (out_j, out_m)
                try:
                    self.assertEqual(JRV.main(), 0)
                finally:
                    JRV.write.__defaults__ = (JRV.OUT_JSON, JRV.OUT_MD)
            self.assertEqual(json.load(open(out_j))["all"]["took"], 1)
            self.assertIn("report only", open(out_m).read().lower())

    def test_no_branch_writes_nothing(self):
        with mock.patch.object(JRV, "fetch", return_value=None), mock.patch.object(JRV, "write") as w, \
                mock.patch.object(JRV, "write_health"), \
                mock.patch.object(sys, "argv", ["journal_review.py"]), mock.patch("builtins.print"):
            JRV.main()
        w.assert_not_called()


class FakeGitHub:
    """The few GitHub REST calls JournalSync makes, in memory."""

    def __init__(self, branch=False, fail_put=0):
        self.branch, self.file, self.sha, self.calls, self.fail_put = branch, None, None, [], fail_put

    def __call__(self, method, url, headers=None, json=None, **kw):
        path = url.split("/repos/", 1)[1].split("/", 2)[2]
        self.calls.append((method, path, headers.get("Authorization")))
        r = mock.Mock()
        if method == "GET" and path.startswith("git/ref/heads/journal"):
            r.status_code, body = (200, {}) if self.branch else (404, {})
        elif method == "POST" and path == "git/trees":
            assert json["tree"][0]["path"] == "README.md"
            r.status_code, body = 201, dict(sha="t1")
        elif method == "POST" and path == "git/commits":
            assert json["parents"] == []                        # a branch of its own: no history from main
            r.status_code, body = 201, dict(sha="c1")
        elif method == "POST" and path == "git/refs":
            self.branch = True
            r.status_code, body = 201, {}
        elif method == "GET" and path.startswith("contents/"):
            r.status_code, body = (200, dict(sha=self.sha)) if self.file else (404, {})
        elif method == "PUT" and path == "contents/journal/my_trades.csv":
            assert json["branch"] == "journal"
            if self.fail_put:
                self.fail_put -= 1
                r.status_code, body = 409, dict(message="sha mismatch")
            elif self.file is not None and json.get("sha") != self.sha:
                r.status_code, body = 409, dict(message="sha mismatch")
            else:
                self.file = base64.b64decode(json["content"])
                self.sha = f"s{len(self.calls)}"
                r.status_code, body = 200, dict(content=dict(sha=self.sha))
        else:
            r.status_code, body = 500, {}
        r.json.return_value = body
        return r


class Sync(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "my_trades.csv")
        with open(self.path, "w") as f:
            f.write(",".join(jr.COLS) + "\n1,a,alert\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_off_without_a_token(self):
        gh = FakeGitHub()
        with mock.patch.dict(os.environ, {"JOURNAL_GITHUB_TOKEN": ""}):
            s = LW.JournalSync(self.path, http=gh)
            self.assertEqual(s.push(T0), (False, "off"))
            self.assertIn("off", s.status(T0))
        self.assertEqual(gh.calls, [])

    def test_creates_the_branch_uploads_and_only_again_when_changed(self):
        gh = FakeGitHub()
        with mock.patch.dict(os.environ, {"JOURNAL_GITHUB_TOKEN": "github_pat_x"}):
            s = LW.JournalSync(self.path, http=gh)
            self.assertEqual(s.push(T0), (True, "1 rows"))
            self.assertTrue(gh.branch)
            self.assertIn(b"1,a,alert", gh.file)
            n = len(gh.calls)
            self.assertEqual(s.push(T0), (True, "unchanged"))
            self.assertEqual(len(gh.calls), n)                                 # nothing new: no call
            with open(self.path, "a") as f:
                f.write("2,a,took\n")
            self.assertTrue(s.push(T0 + M5)[0])
            self.assertIn(b"2,a,took", gh.file)
            self.assertIn("uploaded", s.status(T0 + M5))
        self.assertTrue(all(auth == "Bearer github_pat_x" for _, _, auth in gh.calls))
        self.assertFalse(any("main" in p for _, p, _ in gh.calls))           # main is never touched

    def test_retries_once_when_the_copy_changed_and_reports_failures(self):
        gh = FakeGitHub(branch=True, fail_put=1)
        with mock.patch.dict(os.environ, {"JOURNAL_GITHUB_TOKEN": "t"}):
            self.assertTrue(LW.JournalSync(self.path, http=gh).push(T0)[0])
            bad = LW.JournalSync(self.path, http=lambda *a, **k: mock.Mock(status_code=401, json=lambda: {}))
            ok, note = bad.push(T0)
            self.assertIn("failing", bad.status(T0))
        self.assertFalse(ok)
        self.assertIn("401", note)

    def test_setup_saves_the_token_only_when_the_upload_works(self):
        env = os.path.join(self.tmp.name, "telegram.env")
        with open(env, "w") as f:
            f.write("TELEGRAM_BOT_TOKEN=1:x\nTELEGRAM_CHAT_ID=42\n")
        with mock.patch.dict(os.environ, {}, clear=False), mock.patch("builtins.print"):
            os.environ.pop("JOURNAL_GITHUB_TOKEN", None)
            failing = mock.Mock(push=mock.Mock(return_value=(False, "HTTP 403")))
            self.assertFalse(LW.setup_github(env, ask=lambda _: "bad", sync=failing))
            self.assertNotIn("JOURNAL_GITHUB_TOKEN", open(env).read())
            self.assertNotIn("JOURNAL_GITHUB_TOKEN", os.environ)
            working = mock.Mock(push=mock.Mock(return_value=(True, "0 rows")))
            self.assertTrue(LW.setup_github(env, ask=lambda _: "github_pat_ok", sync=working))
        text = open(env).read()
        self.assertIn("TELEGRAM_CHAT_ID=42", text)                            # the Telegram settings are kept
        self.assertEqual(text.count("JOURNAL_GITHUB_TOKEN=github_pat_ok"), 1)


class WatcherJournal(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        patches = [mock.patch.object(LW, "STATE", os.path.join(self.tmp.name, "state.json")),
                   mock.patch.object(LW, "JOURNAL", os.path.join(self.tmp.name, "journal", "my_trades.csv")),
                   mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "1:x", "TELEGRAM_CHAT_ID": "42",
                                                "JOURNAL_GITHUB_TOKEN": ""}),
                   mock.patch.object(LW, "log")]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.now = T0 + 9000
        self.w = LW.Watcher(LW.SyntheticSwap(), send=True, git=False, now_fn=lambda: self.now)
        self.sent = []
        for p in (mock.patch.object(LW, "telegram_message", side_effect=lambda text, *a, **k:
                                    self.sent.append(text) or (True, "", 77)),
                  mock.patch.object(LW, "tg_api", return_value=(True, {}))):
            p.start()
            self.addCleanup(p.stop)

    def tearDown(self):
        self.tmp.cleanup()

    def deliver(self):
        self.w.deliver([dict(alert(), size={}, risk_pct=0.5, zone_r=0.2, regimes={}, warnings=[])], self.now)
        return next(iter(self.w.state["alerts"]))

    def events(self):
        return [r["event"] for r in jr.read(open(LW.JOURNAL).read())]

    def test_a_skipped_alert_still_gets_its_plan_result(self):
        aid = self.deliver()
        self.assertIn(aid, self.w.state["shadow"])
        self.w.on_button(dict(id="q", data=f"skip|{aid}"), self.now)
        df = pd.DataFrame(bars([(100, 101, 99.5, 100.5), (100.5, 102.2, 100.4, 101.5), (101.5, 103.5, 101.4, 103)]))
        self.now = T0 + 3 * M5 + 9000
        n = len(self.sent)
        with mock.patch.object(LW.Watcher, "update", return_value=df):
            self.w.follow(self.now)
        self.assertEqual(len(self.sent), n)                                     # silent: no message
        self.assertEqual(self.events(), ["alert", "skipped", "plan"])
        rv = jr.review(jr.read(open(LW.JOURNAL).read()), self.now)
        self.assertAlmostEqual(rv["all"]["plan_skipped"]["avg_r"], 2.5)
        self.assertEqual(self.w.state["shadow"], {})

    def test_result_command_records_the_real_result(self):
        aid = self.deliver()
        self.w.on_button(dict(id="q", data=f"took|{aid}"), self.now)
        self.assertIn("still open", self.w.command("result", "1.0", self.now))
        self.w.on_button(dict(id="q", data=f"closed|{aid}"), self.now)
        self.assertIn("/result 1.2", self.sent[-1])                             # the closing message asks for it
        self.assertIn("Send your real result", self.w.command("result", "abc", self.now))
        reply = self.w.command("result", "+0.8R", self.now)
        self.assertIn("+0.80R", reply)
        self.assertEqual(self.events()[-1], "your result")
        self.assertIn("waiting", self.w.command("result", "1", self.now))       # nothing left without a result
        self.assertIn("+0.80R", self.w.command("result", f"{aid} 0.8", self.now))   # by id: corrected
        self.assertIn("yours +0.8R", self.w.trades_text(self.now))
        self.assertIn("/result", LW.lv.HELP)

    def test_status_shows_the_sync_and_dry_runs_write_no_journal(self):
        self.assertIn("Journal sync to GitHub: off", self.w.status_text(self.now))
        dry = LW.Watcher(LW.SyntheticSwap(), send=False, git=False, now_fn=lambda: self.now)
        dry.deliver([dict(alert(), size={}, risk_pct=0.5, zone_r=0.2, regimes={}, warnings=[])], self.now)
        self.assertFalse(os.path.exists(LW.JOURNAL))
        self.assertEqual(dry.state["shadow"], {})

    def test_an_open_plan_follow_up_is_dropped_after_14_days(self):
        self.deliver()
        self.now += 15 * 86_400_000
        with mock.patch.object(LW.Watcher, "update", return_value=pd.DataFrame(bars([(100, 100.5, 99.5, 100)]))):
            self.w.follow(self.now)
        self.assertEqual(self.w.state["shadow"], {})

    def test_review_runs_in_the_scan_and_tests_skip_the_journal_branch(self):
        scan = open(os.path.join(ROOT, ".github", "workflows", "scan.yml")).read()
        self.assertIn("python journal_review.py", scan)
        self.assertLess(scan.index("journal_review.py"), scan.index("notify.py weekly"))
        tests = open(os.path.join(ROOT, ".github", "workflows", "tests.yml")).read()
        self.assertIn("- journal", tests.split("paths-ignore")[0])
        self.assertIn("engine/journal.py", LW.CODE_FILES)
        self.assertIn("journal/", open(os.path.join(ROOT, ".gitignore")).read())   # the PC's journal stays local


if __name__ == "__main__":
    unittest.main()
