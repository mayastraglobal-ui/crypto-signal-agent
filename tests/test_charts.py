"""
Phase 18 part D tests: the backtest chart page (data files, the page itself, the bundled Lightweight Charts library with
its licence and attribution, nothing loaded from outside), its links from the dashboard, the approval packs (with the
Pine script) and the [ENTRY] / [EXIT] emails, and publishing it so the hourly dashboard rebuild keeps the data.

Run:  python -m unittest test_charts -v      (from tests/)
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_dashboard  # noqa: E402
import scanner  # noqa: E402
import test_brain  # noqa: E402
import test_emails  # noqa: E402
import test_learn  # noqa: E402
from engine import approval as AP  # noqa: E402
from engine import emails as EM  # noqa: E402
from engine import btcharts as BC  # noqa: E402
from engine import dashboard as DB  # noqa: E402

H = 3_600_000
VENDOR = os.path.join(ROOT, "vendor", "lightweight-charts")


def trade(i, d=1, r=1.5, bars=3, reason="TP2"):
    return dict(entry_time=1_700_000_000_000 + i * H, exit_idx=i + bars - 1, bars=bars, dir=d, entry=100.0 + i,
                R=2.0, tps=[104.0 + i, 106.0 + i], r=r, reason=reason)


class Data(unittest.TestCase):
    def test_trades_equity_and_drawdown(self):
        ot = 1_700_000_000_000 + np.arange(100) * H
        tr = [trade(10, r=2.0), trade(20, d=-1, r=-1.0, reason="SL"), trade(30, r=-1.5, bars=1),
              trade(30, r=0.5, bars=1)]                        # two exits on the same candle
        doc = BC.trades_doc("X@1.0|1h", "1h", "BTC", tr, ot, None)
        self.assertEqual(doc["n"], 4)
        t0 = doc["trades"][0]
        self.assertEqual((t0["et"], t0["xt"]), (ot[10] // 1000, ot[12] // 1000), "exit = open of the exit candle")
        self.assertEqual((t0["d"], t0["e"], t0["s"], t0["tp"]), (1, 110.0, 108.0, [114.0, 116.0]))
        self.assertEqual(doc["trades"][1]["s"], 122.0, "a short's stop is above the entry")
        self.assertEqual(doc["equity"], [[ot[12] // 1000, 2.0], [ot[22] // 1000, 1.0], [ot[30] // 1000, 0.0]])
        self.assertEqual(doc["drawdown"], [[ot[12] // 1000, 0.0], [ot[22] // 1000, -1.0], [ot[30] // 1000, -2.0]])
        self.assertEqual((doc["total_r"], doc["max_dd_r"]), (0.0, 2.0))
        five = BC.trades_doc("Y@1.0|15m", "15m", "BTC", [trade(10, bars=4)], ot, BC.FIVE_MIN)
        self.assertEqual(five["trades"][0]["xt"] - five["trades"][0]["et"], 3 * 300, "5m-confirmed: 5m bars")
        many = BC.trades_doc("Z", "1h", "BTC", [trade(i % 90, r=0.1) for i in range(BC.MAX_TRADES + 50)], ot, None)
        self.assertEqual(len(many["trades"]), BC.MAX_TRADES)
        self.assertEqual(many["trades"][-1]["et"], max(x["et"] for x in many["trades"]), "the newest trades are kept")
        oldest = BC.trades_doc("Z", "1h", "BTC", [trade(1)] + [trade(50, r=0.1) for _ in range(BC.MAX_TRADES)], ot, None)
        self.assertNotIn(ot[1] // 1000, [x["et"] for x in oldest["trades"]], "the oldest trade is the one dropped")
        self.assertEqual(many["n"], BC.MAX_TRADES + 50, "the equity curve uses every trade")

    def test_candles_and_writer(self):
        n = BC.CANDLES + 200
        df = pd.DataFrame(dict(open_time=1_700_000_000_000 + np.arange(n) * H, open=np.full(n, 1.123456789),
                               high=2.0, low=0.5, close=1.0))
        doc = BC.candles_doc("BTC", "1h", df)
        self.assertEqual(len(doc["t"]), BC.CANDLES)
        self.assertEqual(doc["t"][-1], int(df["open_time"].iloc[-1]) // 1000)
        self.assertEqual(doc["o"][0], 1.123457, "7 significant digits")
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        os.makedirs(os.path.join(tmp, "t"))
        open(os.path.join(tmp, "t", "stale.json"), "w").close()
        w = BC.Writer(tmp)
        self.assertFalse(os.path.exists(os.path.join(tmp, "t", "stale.json")), "a fresh set every run")
        w.candles("BTC", "1h", df)
        w.trades("S@x", "1.0", "1h", "BTC", [trade(5)], df["open_time"].to_numpy())
        rows = w.finish({}, "2026-09-26 00:50")
        self.assertEqual(rows[0]["slug"], "S_x_v1.0_1h")
        self.assertEqual(w.files(), ["index.json", "c/BTC_1h.json", "t/S_x_v1.0_1h_BTC.json"])
        man = json.load(open(os.path.join(tmp, "index.json")))
        self.assertEqual(build_dashboard.manifest_files(man), w.files())

    def test_urls(self):
        self.assertEqual(BC.page_url("https://a.github.io/r/", "S", "1.0", "1h", "BTC"),
                         "https://a.github.io/r/chart.html#s=S&v=1.0&tf=1h&c=BTC")
        self.assertEqual(BC.pages_base({}, "own/repo"), "https://own.github.io/repo/")
        self.assertEqual(BC.pages_base({"dashboard": {"url": "https://x.example/d"}}), "https://x.example/d")
        self.assertEqual(BC.page_url("https://x.example/d", "S", "1.0", "4h"), "https://x.example/d/chart.html#s=S&v=1.0&tf=4h")


class Page(unittest.TestCase):
    def test_nothing_loaded_from_outside_and_attribution(self):
        page = BC.page()
        for src in re.findall(r'<script[^>]*src="([^"]+)"', page) + re.findall(r'<link[^>]*href="([^"]+)"', page):
            self.assertFalse(src.startswith(("http:", "https:", "//")), src)
        self.assertIn(f'<script src="{BC.LIB}"></script>', page)
        self.assertNotIn("@import", page)
        self.assertIn('<a href="https://www.tradingview.com/">', page)
        self.assertIn("TradingView Lightweight Charts™ - Copyright (c) 2025 TradingView, Inc.", page)
        self.assertIn("attributionLogo: true", page)
        self.assertIn('href="vendor/lightweight-charts/LICENSE"', page)
        self.assertIn("BACKTEST - history, not a promise", page)
        for js in re.findall(r"fetch\(([^)]*)\)", page):
            self.assertNotIn("http", js)

    def test_bundled_library_unchanged(self):
        lib = os.path.join(ROOT, BC.LIB)
        with open(lib, "rb") as f:
            body = f.read()
        self.assertEqual(hashlib.sha256(body).hexdigest(),
                         "e21cc5caa0226ef30bd8549c50b9ef926615f2a4ee6b4e486353477a55f598cf")
        self.assertIn(b"TradingView Lightweight Charts\xe2\x84\xa2 v5.2.1", body[:300])
        self.assertIn("Apache License", test_brain.read(os.path.join(VENDOR, "LICENSE")))
        self.assertIn("TradingView, Inc. https://www.tradingview.com/", test_brain.read(os.path.join(VENDOR, "NOTICE")))
        self.assertIn("e21cc5caa0226ef3", test_brain.read(os.path.join(VENDOR, "README.md")))

    @unittest.skipUnless(shutil.which("node") and subprocess.run(
        ["node", "-e", "require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright')"],
        capture_output=True).returncode == 0 and os.path.exists("/opt/pw-browsers"),
        "needs node + playwright + chromium (the build environment has them; CI does not)")
    def test_page_draws_in_a_browser(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        site = os.path.join(tmp, "site")
        w = BC.Writer(os.path.join(site, "charts"))
        rng = np.random.default_rng(1)
        n = 400
        c = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
        df = pd.DataFrame(dict(open_time=1_700_000_000_000 + np.arange(n) * H, open=np.r_[100, c[:-1]],
                               high=np.maximum(np.r_[100, c[:-1]], c) * 1.002, low=np.minimum(np.r_[100, c[:-1]], c) * 0.998,
                               close=c))
        w.candles("BTC", "1h", df)
        w.trades("S", "1.0", "1h", "BTC", [trade(i, d=1 if i % 2 else -1, r=(-1) ** i * 1.2) for i in range(20, 380, 30)],
                 df["open_time"].to_numpy())
        w.finish({"S@1.0|1h": dict(status="BACKTESTING")}, "2026-09-26 00:50")
        with open(os.path.join(site, "chart.html"), "w") as f:
            f.write(BC.page())
        os.makedirs(os.path.join(site, "vendor", "lightweight-charts"))
        shutil.copy(os.path.join(ROOT, BC.LIB), os.path.join(site, BC.LIB))
        js = os.path.join(tmp, "check.js")
        with open(js, "w") as f:
            f.write("""const {chromium} = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(process.argv[2]); await p.waitForFunction(() => window.chartReady === true, null, {timeout: 20000});
  const out = await p.evaluate(() => ({canvases: document.querySelectorAll('canvas').length,
    pos: document.getElementById('pos').textContent, info: document.getElementById('info').textContent}));
  await p.click('#prev'); out.after = await p.evaluate(() => document.getElementById('pos').textContent);
  out.errs = errs; console.log(JSON.stringify(out)); await b.close(); })();""")
        srv = subprocess.Popen([sys.executable, "-m", "http.server", "8799"], cwd=site, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
        self.addCleanup(srv.kill)
        import time
        time.sleep(1)
        p = subprocess.run(["node", js, "http://localhost:8799/chart.html#s=S&v=1.0&tf=1h&c=BTC"], capture_output=True,
                           text=True, timeout=120)
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout.strip().splitlines()[-1])
        self.assertEqual(out["errs"], [])
        self.assertGreaterEqual(out["canvases"], 6, "price, equity and drawdown panes")
        self.assertEqual((out["pos"], out["after"]), ("12 / 12", "11 / 12"))
        self.assertIn("S v1.0 · 1h · BTC: 12 backtest trades", out["info"])


class Publish(unittest.TestCase):
    def test_this_runs_data_or_the_published_copy(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        reports, site = os.path.join(tmp, "reports"), os.path.join(tmp, "site")
        w = BC.Writer(os.path.join(reports, "backtest_charts"))
        df = pd.DataFrame(dict(open_time=1_700_000_000_000 + np.arange(50) * H, open=1.0, high=1.0, low=1.0, close=1.0))
        w.candles("BTC", "1h", df)
        w.trades("S", "1.0", "1h", "BTC", [trade(3)], df["open_time"].to_numpy())
        w.finish({}, "2026-09-26 00:50")
        with mock.patch.multiple(build_dashboard, REPORTS=reports, SITE=site,
                                 CHART_DATA=os.path.join(reports, "backtest_charts")):
            files = build_dashboard.build(prev=lambda: None)
            self.assertIn("site/charts/t/S_v1.0_1h_BTC.json", files)
            self.assertTrue(os.path.exists(os.path.join(site, "charts", "c", "BTC_1h.json")))
            for v in build_dashboard.VENDOR + ["chart.html", "index.html"]:
                self.assertIn(f"site/{v}", files)
                self.assertTrue(os.path.exists(os.path.join(site, v)), v)
            index = test_brain.read(os.path.join(site, "index.html"))
            self.assertIn('href="chart.html"', index)
            # the hourly scan: no chart data of its own -> the published copy's files are listed (publish keeps them)
            shutil.rmtree(os.path.join(reports, "backtest_charts"))
            prev = json.loads(test_brain.read(os.path.join(site, "charts", "index.json")))
            shutil.rmtree(os.path.join(site, "charts"))
            files = build_dashboard.build(prev=lambda: prev)
            self.assertIn("site/charts/t/S_v1.0_1h_BTC.json", files)
            self.assertFalse(os.path.exists(os.path.join(site, "charts")), "nothing local - publish() keeps the copy")
            self.assertEqual([f for f in build_dashboard.build(prev=lambda: None) if "/charts/" in f], [])

    def test_publish_keeps_missing_files_from_the_previous_copy(self):
        src = test_brain.read(os.path.join(ROOT, "publish_live.py"))
        self.assertIn('sources[dest] = "kept from the previous copy"', src)


class Links(unittest.TestCase):
    def test_dashboard_strategy_table(self):
        rep = dict(strategy_scoreboard=[dict(strategy="S", version="1.0", tf="1h", status="BACKTESTING", trades=10,
                                             avg_r=0.1), dict(strategy="T", version="1.0", tf="4h", status="FAILED")])
        html_ = DB.render(dict(latest=rep, charts=dict(cells=[dict(strategy="S", version="1.0", tf="1h")])))
        self.assertIn('<a href="chart.html#s=S&amp;v=1.0&amp;tf=1h">chart</a>', html_)
        self.assertIn("Backtest chart</th>", html_)
        appr = DB.render(dict(research=dict(approval=dict(eligible=[dict(
            strategy="S", version="1.0", tf="1h", paper_signals=22, paper_avg_r=0.2, backtest_validate_avg_r=0.3,
            pack="reports/approval/S_v1.0_1h.md", pine="reports/pine/S_v1.0_1h.pine")]))))
        self.assertIn('href="chart.html#s=S&amp;v=1.0&amp;tf=1h">backtest chart</a>', appr)
        self.assertIn("reports/pine/S_v1.0_1h.pine\">Pine script</a>", appr)

    def test_approval_pack(self):
        cell = test_learn.cell()
        spec = test_brain.Approval().spec()
        links = dict(chart="https://o.github.io/r/chart.html#s=S6-OB-FVG&v=1.0&tf=15m",
                     pine="https://github.com/o/r/blob/main/reports/pine/S6-OB-FVG_v1.0_15m.pine",
                     pine_path="reports/pine/S6-OB-FVG_v1.0_15m.pine")
        text = "\n".join(AP.pack(cell, spec, [], {}, AP.settings(None), "2026-09-26 00:50", None, links))
        self.assertIn("**Check the trades before you say yes:**", text)
        self.assertIn("- backtest chart (every trade on the candles, stop and targets, equity and drawdown): "
                      "https://o.github.io/r/chart.html#s=S6-OB-FVG&v=1.0&tf=15m", text)
        self.assertIn("- TradingView: open https://github.com/o/r/blob/main/reports/pine/S6-OB-FVG_v1.0_15m.pine", text)
        self.assertLess(text.index("Check the trades"), text.index("## 1. Definition"))
        bare = "\n".join(AP.pack(cell, spec, [], {}, AP.settings(None), "2026-09-26 00:50"))
        self.assertIn("backtest chart: not available", bare)
        self.assertIn('"Pine export"', bare)

    def test_emails_keep_the_chart_image_and_add_the_link(self):
        url = "https://o.github.io/r/chart.html#s=S6-OB-FVG&v=1.0&tf=15m&c=ETH"
        m = EM.live_entry(dict(test_emails.card(backtest_chart=url), chart_cid="chart"))
        self.assertIn(f"Backtest chart: {url}", m["text"])
        self.assertIn('src="cid:chart"', m["html"])
        self.assertNotIn("Backtest chart:", EM.live_entry(test_emails.card())["text"], "no link: no button")
        base = dict(coin="ETH", quote="USDT", direction="LONG", tf="15m", strategy="S", version="1.0",
                    entry=100.0, kind="CLOSED", close_reason="SL", result_r=-1.0)
        self.assertIn(f"Backtest chart: {url}", EM.live_update(dict(base, backtest_chart=url))["text"])

    def test_email_context_builds_the_link_and_keeps_the_png(self):
        fe = test_emails.FromEvents()
        with tempfile.TemporaryDirectory() as tmp:
            rows = [test_emails.log_row(state=test_emails.P.TP1_HIT, current_stop=100.0),
                    test_emails.log_row(id="f", sim_tf="5m", entry=100.5, confirm_5m_utc="2023-11-14 22:24",
                                        entry_time_utc="2023-11-14 22:24", smc_5m="")]
            m = fe.ctx(rows, tmp)
            out = m.from_events([fe.ev(test_emails.P.ACTIVE, test_emails.P.TP1_HIT),
                                 fe.ev(test_emails.P.AWAITING, test_emails.P.TRIGGERED, rid="f"),
                                 fe.ev(test_emails.P.TRIGGERED, test_emails.P.ACTIVE, rid="f")])
            fe.doCleanups()
        self.assertEqual(len(out), 2)
        for o in out:
            self.assertTrue(o["chart"] and o["chart"].endswith(".png"), "the chart image stays")
            self.assertTrue(any(ln.startswith("Backtest chart: https://") and "chart.html#s=S&v=1.0" in ln
                                and "&c=ETH" in ln for ln in o["text"].splitlines()), o["text"])
            self.assertIn("cid:chart", o["html"])                                   # the image inside the email


class Research(unittest.TestCase):
    """The research run writes the page's data: one candle file per coin x timeframe, one trade file per cell x coin."""

    def test_offline_run(self):
        from test_data_quality import run_copy
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        shutil.copy(os.path.join(ROOT, "research.py"), tmp)
        p = run_copy(tmp, "research.py", "--offline", "--coins", "2")
        self.assertEqual(p.returncode, 0, p.stdout[-2000:] + p.stderr[-2000:])
        folder = os.path.join(tmp, "reports", "backtest_charts_offline")
        man = json.loads(test_brain.read(os.path.join(folder, "index.json")))
        res = json.loads(test_brain.read(os.path.join(tmp, "reports", "research_offline.json")))
        keys = {f"{c['strategy']}@{c['version']}|{c['tf']}" for c in man["cells"]}
        self.assertTrue(keys)
        self.assertLessEqual(keys, set(res["cells"]))
        for rel in build_dashboard.manifest_files(man):
            self.assertTrue(os.path.exists(os.path.join(folder, rel)), rel)
        c = man["cells"][0]
        coin = sorted(c["coins"])[0]
        doc = json.loads(test_brain.read(os.path.join(folder, "t", f"{c['slug']}_{coin}.json")))
        cell = res["cells"][f"{c['strategy']}@{c['version']}|{c['tf']}"]
        self.assertEqual(doc["n"], cell["evidence"]["by_coin"][coin]["n"], "the same trades as the research")
        self.assertIn("backtest_charts_offline/", test_brain.read(os.path.join(ROOT, ".gitignore")))
        n = res["counts"]                                    # email redesign: what the run did, for the emails
        self.assertEqual(n["coins"], 2)
        self.assertEqual(n["backtests"], sum(n["per_coin"].values()))
        self.assertEqual(n["tests"], len(res["cells"]))
        self.assertEqual(n["backtests"], sum(len(c["evidence"]["by_coin"]) for c in res["cells"].values()))
        hist = json.loads(test_brain.read(os.path.join(tmp, "reports", "research_counts_offline.json")))
        self.assertEqual(hist[-1]["backtests"], n["backtests"])


if __name__ == "__main__":
    unittest.main()
