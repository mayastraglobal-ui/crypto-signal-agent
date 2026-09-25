"""Phase 16 tests: the web dashboard (engine/dashboard.py, build_dashboard.py, publish to gh-pages).

Run:  python -m unittest discover -s tests -v
"""
import datetime as dt
import json
import os
import re
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
import build_dashboard  # noqa: E402
import publish_live  # noqa: E402
import scanner  # noqa: E402
from engine import dashboard as D  # noqa: E402
from engine import positions as POS  # noqa: E402
from test_data_quality import shared_offline_run  # noqa: E402

SECTIONS = ["book", "market", "signals", "strategies", "approval", "risk", "claude"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def git(cwd, *args):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr)
    return p.stdout.strip()


class FromOfflineScan(unittest.TestCase):
    """The page built from a real offline scan (synthetic data)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp, p = shared_offline_run()
        assert p.returncode == 0, p.stderr[-2000:]
        cls.latest = json.loads(read(os.path.join(cls.tmp, "reports", "latest.json")))
        cls.data = json.loads(read(os.path.join(cls.tmp, "reports", "dashboard_data.json")))
        cls.page = D.render(dict(latest=cls.latest, candles=cls.data, repo_url="https://github.com/o/r",
                                 built_utc="2026-09-25 01:00"))

    def test_scan_writes_candles_of_the_signal_coins(self):
        signal = set(self.latest["universe"]["signal"]) if isinstance(self.latest.get("universe"), dict) \
            else {r["coin"] for r in self.latest["daily"]["matrix"]}
        self.assertEqual(set(self.data["candles"]), signal)
        for coin, by_tf in self.data["candles"].items():
            self.assertIn("1h", by_tf)
            for tf, rows in by_tf.items():
                self.assertLessEqual(len(rows), scanner.DASH_BARS)
                self.assertTrue(all(len(r) == 5 and r[2] >= max(r[1], r[4]) and r[3] <= min(r[1], r[4]) for r in rows))
                self.assertEqual([r[0] for r in rows], sorted(r[0] for r in rows))

    def test_every_section_and_a_chart_per_coin(self):
        for s in SECTIONS:
            self.assertIn(f'<section id="{s}">', self.page)
        coins = [r["coin"] for r in self.latest["daily"]["matrix"]]
        self.assertEqual(self.page.count('class="chart"'), len(coins))
        for c in coins:
            self.assertIn(f'aria-label="{c} 1h"', self.page)
        self.assertIn("Research signal. Not financial advice.", self.page)
        self.assertLess(len(self.page.encode()), 1_000_000)

    def test_self_contained(self):
        """No external scripts, styles, fonts or images - nothing can break or track in the browser."""
        self.assertNotRegex(self.page, r"<script[^>]+src=")
        self.assertNotRegex(self.page, r"<link[^>]+stylesheet")
        self.assertNotIn("@import", self.page)
        self.assertNotRegex(self.page, r"<img[^>]+src=\"https?:")
        for url in re.findall(r'href="([^"]+)"', self.page):
            self.assertTrue(url.startswith(("#", "https://github.com/o/r/", "chart.html")), url)   # + the chart page

    def test_stale_warning_in_the_browser(self):
        self.assertIn(f'data-utc="{self.latest["generated_utc"]}"', self.page)
        self.assertEqual(D.STALE_HOURS, 2.0)                       # the hourly scan missed ~2 runs
        self.assertIn("if(h>2.0)", self.page)
        self.assertIn("STALE: last update", self.page)


class Render(unittest.TestCase):
    def test_nothing_yet(self):
        page = D.render({})
        self.assertIn("No engine report yet", page)
        for s in SECTIONS:
            self.assertIn(f'<section id="{s}">', page)
        self.assertIn("No trade is a valid result", page)

    def book(self):
        return dict(utc="u", beijing="b", empty=False, day_r=-1.0, week_r=2.5, paper_day_r=0.5, heat=1,
                    limits=dict(day_r=-3, week_r=-6, heat=3), awaiting=[],
                    active=[dict(coin="BTC", direction="LONG", tf="1h", sim_tf="1h", strategy="S6", version="1.0",
                                 stage="APPROVED", entry=100.0, stop=95.0, tp1=110.0, open_r=0.4, next_action="hold")],
                    paper=[dict(coin="ETH", direction="SHORT", tf="15m", sim_tf="15m", strategy="S5", version="1.0",
                                stage="PAPER_TRADING", entry=50.0, stop=52.0, tp1=46.0, open_r=-0.2, next_action="hold")],
                    closed_today=[dict(coin="SOL", direction="LONG", tf="1h", strategy="S6", reason="TP", result_r=2.0,
                                       live=True),
                                  dict(coin="ADA", direction="LONG", tf="1h", strategy="S5", reason="SL", result_r=-1.0,
                                       live=False)])

    def candles(self, n=50, base=100.0):
        return [[1_790_000_000_000 + i * 3_600_000, base, base + 2, base - 2, base + (1 if i % 2 else -1)]
                for i in range(n)]

    def test_live_and_paper_are_labelled_never_mixed(self):
        rep = dict(generated_utc="2026-09-25 00:07", position_book=self.book(),
                   daily=dict(matrix=[dict(coin="BTC", regimes=["A"], price=100)]),
                   strategy_scoreboard=[dict(strategy="S6", version="1.0", tf="1h", status="APPROVED", trades=40,
                                             avg_r=0.2, profit_factor=1.4, walk_forward="4/5", live_signals=3,
                                             live_avg_r=0.5)])
        page = D.render(dict(latest=rep, candles=dict(candles={"BTC": {"1h": self.candles()},
                                                               "ETH": {"15m": self.candles(base=50)}})))
        book = page.split('<section id="book">')[1].split("</section>")[0]
        self.assertIn('<span class="badge ok">LIVE</span>', book)
        self.assertIn('PAPER · PAPER_TRADING', book)
        self.assertIn("<td>LIVE</td>", book)
        self.assertIn("<td>PAPER</td>", book)
        self.assertIn("paper today +0.50R", book)
        self.assertIn('aria-label="BTC 1h · S6 LONG (LIVE)"', book)
        self.assertIn('aria-label="ETH 15m · S5 SHORT (PAPER)"', book)
        strat = page.split('<section id="strategies">')[1]
        for h in ("BACKTEST trades", "BACKTEST avg", "LIVE signals", "LIVE avg"):
            self.assertIn(f"<th>{h}</th>", strat)
        market = page.split('<section id="market">')[1].split("</section>")[0]
        self.assertIn("entry 100.00", market)        # the 1h live position is drawn on the coin's market chart

    def test_everything_from_files_is_escaped(self):
        evil = '<script>alert(1)</script>'
        rep = dict(generated_utc='"><script>x</script>', position_book=dict(self.book(), active=[dict(
            self.book()["active"][0], strategy=evil, next_action=evil)]),
                   watching=[dict(coin=evil, direction="LONG", tf="1h", strategy="s", stage="V", state="W",
                                  missing=evil)])
        page = D.render(dict(latest=rep, briefing=("reports/claude/briefings/x.md",
                                                   f"# {evil}\n[bad](javascript:alert(1)) <img src=x onerror=y>")))
        self.assertEqual(page.count("<script>"), 1)                  # only the page's own age script
        self.assertNotIn("javascript:alert", page.replace("[bad](javascript:alert(1))", ""))
        self.assertNotIn("<img", page)

    def test_claude_is_marked_as_ai(self):
        page = D.render(dict(latest=dict(generated_utc="x"),
                             briefing=("reports/claude/briefings/2026-09-25-0820.md", "# Hi\n## Summary\nquiet"),
                             review=None))
        claude = page.split('<section id="claude">')[1]
        self.assertIn("written by the AI", claude)
        self.assertIn('<span class="badge ai">AI</span>Latest briefing - 2026-09-25-0820', claude)
        self.assertIn("Latest daily review: none yet.", claude)

    def test_approval_and_risk(self):
        rep = dict(generated_utc="x", lifecycle=dict(approval=dict(
            eligible=[dict(strategy="S6", version="1.0", tf="15m", paper_signals=22, paper_avg_r=0.2,
                           backtest_validate_avg_r=0.3, pack="reports/approval/S6_v1.0_15m.md")], warnings=["w1"])),
                   risk=dict(halts_text=["day limit"], suspended=["S5@1.0|1h"], risk_pct=0.5, blackout_now=True,
                             upcoming_events=["2026-10-02 12:30 NFP"], calendar_warning="calendar not maintained",
                             groups=[["BTC", "ETH"]], limits=dict(day_r=-3)))
        page = D.render(dict(latest=rep, repo_url="https://github.com/o/r", pine_files=["reports/pine/a_v1.0_4h.pine"]))
        self.assertIn("Approve S6 v1.0 15m for live emails? (yes/no)", page)
        self.assertIn('href="https://github.com/o/r/blob/main/reports/approval/S6_v1.0_15m.md"', page)
        self.assertIn("a_v1.0_4h.pine", page)
        self.assertIn('<span class="badge bad">day limit</span>', page)
        self.assertIn("SUSPENDED S5@1.0|1h", page)
        self.assertIn("EVENT BLACKOUT NOW", page)
        self.assertIn("2026-10-02 12:30 NFP", page)
        self.assertIn("BTC+ETH", page)


class Chart(unittest.TestCase):
    def test_levels_and_labels(self):
        c = [[1_790_000_000_000 + i * 3_600_000, 100.0, 101.0, 99.0, 100.5] for i in range(30)]
        svg = D.svg_chart(c, [("entry", 100.4, "entry"), ("stop", 100.3, "stop"), ("TP1", 100.6, "tp")], "X 1h")
        ys = sorted(float(y) for y in re.findall(r'<text class="lbl [a-z]+" x="[\d.]+" y="([\d.]+)"', svg))
        self.assertEqual(len(ys), 4)                                    # 3 levels + the last price
        self.assertTrue(all(b - a >= 13.9 for a, b in zip(ys, ys[1:])), ys)     # never on top of each other
        self.assertTrue(all(0 <= y <= 210 for y in ys))
        self.assertEqual(svg.count('<rect class="body'), 30)
        for ln in re.findall(r'<line class="lvl [a-z]+"[^>]+y1="([\d.]+)"', svg):
            self.assertTrue(20 <= float(ln) <= 190)                     # levels are inside the plot
        self.assertIn("X 1h", svg)

    def test_flat_or_missing_candles(self):
        flat = [[1_790_000_000_000 + i, 5.0, 5.0, 5.0, 5.0] for i in range(10)]
        self.assertIn("<svg", D.svg_chart(flat, [("stop", None, "stop")], "flat"))
        self.assertIn("no candles for", D.svg_chart([], [], "none"))
        self.assertIn("no candles for", D.svg_chart(None, [], "none"))

    def test_markdown(self):
        h = D.md("# Title\n- one **bold**\n- two `code`\ntext https://a.io/x?y=1&z=2\n[s](https://b.io)")
        self.assertIn("<h3>Title</h3>", h)
        self.assertIn("<ul>\n<li>one <strong>bold</strong></li>\n<li>two <code>code</code></li>\n</ul>", h)
        self.assertIn('<a href="https://a.io/x?y=1&amp;z=2" rel="noopener noreferrer" target="_blank">', h)
        self.assertIn('<a href="https://b.io" rel="noopener noreferrer" target="_blank">s</a>', h)


class Build(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_build_from_folder_with_missing_files(self):
        reports, site = os.path.join(self.tmp, "reports"), os.path.join(self.tmp, "site")
        os.makedirs(os.path.join(reports, "claude", "briefings"))
        for name, text in (("2026-09-24-2120.md", "# old"), ("2026-09-25-0820.md", "# newest one")):
            with open(os.path.join(reports, "claude", "briefings", name), "w") as f:
                f.write(text)
        with open(os.path.join(reports, "latest.json"), "w") as f:
            f.write("{broken json")
        with mock.patch.object(build_dashboard, "REPORTS", reports), mock.patch.object(build_dashboard, "SITE", site):
            inp = build_dashboard.inputs(dt.datetime(2026, 9, 25, tzinfo=dt.timezone.utc))
            self.assertEqual(inp["briefing"][0], "reports/claude/briefings/2026-09-25-0820.md")
            self.assertIsNone(inp["latest"])                             # a broken file never stops the page
            self.assertIsNone(inp["review"])
            files = build_dashboard.build(dt.datetime(2026, 9, 25, tzinfo=dt.timezone.utc), prev=lambda: None)
        self.assertTrue(os.path.exists(os.path.join(site, ".nojekyll")))
        self.assertEqual(files[:3], ["site/index.html", "site/.nojekyll", "site/chart.html"])   # + the chart library
        page = read(os.path.join(site, "index.html"))
        self.assertIn("No engine report yet", page)
        self.assertIn("newest one", page)

    def test_positions_carry_what_the_charts_need(self):
        import pandas as pd
        df = pd.DataFrame([dict(id="a", coin="BTC", direction="LONG", tf="15m", strategy="S", version="1.0",
                                stage="APPROVED", status="OPEN", state="POSITION_ACTIVE", entry=100.0, stop=95.0,
                                tp1=110.0, sim_tf="5m", signal_time_utc="2026-09-25 00:00",
                                entry_time_utc="2026-09-25 00:20", current_stop="", result_r=None,
                                closed_time_utc="", next_action="")])
        b = POS.build(df, dt.datetime(2026, 9, 25, 1, tzinfo=dt.timezone.utc), {("BTC", "5m"): 101.0})
        p = b["active"][0]
        self.assertEqual((p["tp1"], p["sim_tf"], p["since"]), (110.0, "5m", "2026-09-25 00:20"))

    def test_publish_to_gh_pages_one_commit_at_the_root(self):
        origin = os.path.join(self.tmp, "origin.git")
        work = os.path.join(self.tmp, "work")
        git(self.tmp, "init", "-q", "--bare", "-b", "main", origin)
        git(self.tmp, "clone", "-q", origin, work)
        for c in (["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            git(work, *c)
        with open(os.path.join(work, "x.txt"), "w") as f:
            f.write("x")
        git(work, "add", "-A")
        git(work, "commit", "-qm", "x")
        git(work, "push", "-q", "origin", "main")
        os.makedirs(os.path.join(work, "site"))
        with mock.patch.object(publish_live, "ROOT", work):
            for i in range(2):
                with open(os.path.join(work, "site", "index.html"), "w") as f:
                    f.write(f"<html>{i}</html>")
                with open(os.path.join(work, "site", ".nojekyll"), "w") as f:
                    f.write("")
                publish_live.publish(files=["site/index.html", "site/.nojekyll"], branch="gh-pages",
                                     readme="r", title="Dashboard", strip="site/")
        git(work, "fetch", "-q", "origin", "gh-pages")
        self.assertEqual(git(work, "rev-list", "--count", "FETCH_HEAD"), "1")          # never builds history
        self.assertEqual(sorted(git(work, "ls-tree", "--name-only", "FETCH_HEAD").split()),
                         [".nojekyll", "README.md", "index.html"])
        self.assertEqual(git(work, "show", "FETCH_HEAD:index.html"), "<html>1</html>")
        self.assertEqual(git(work, "rev-list", "--count", "origin/main"), "1")          # main untouched

    def test_workflows(self):
        for name in ("scan.yml", "research.yml", "brain.yml"):
            wf = yaml.safe_load(read(os.path.join(ROOT, ".github", "workflows", name)))
            steps = list(wf["jobs"].values())[0]["steps"]
            dash = [s for s in steps if s.get("name", "").startswith("Dashboard")]
            self.assertEqual(len(dash), 1, name)
            self.assertTrue(dash[0].get("continue-on-error"), f"{name}: the dashboard must never stop a run")
            self.assertIn("build_dashboard.py --publish", dash[0]["run"])
            names = [s.get("name", "") for s in steps]
            if name != "brain.yml":
                self.assertGreater(names.index(dash[0]["name"]),
                                   next(i for i, n in enumerate(names) if n.startswith("Publish the large")), name)
        brain = read(os.path.join(ROOT, ".github", "workflows", "brain.yml"))
        self.assertIn("r['status'] == 'applied'", brain)                     # only when Claude's work was applied
        self.assertIn("reports/dashboard_data.json", publish_live.LIVE_FILES)


if __name__ == "__main__":
    unittest.main()
