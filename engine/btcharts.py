"""
Backtest chart pages (Phase 18 D): one page on the dashboard (chart.html) that shows any strategy x timeframe x coin -
candles with the backtest's buy / sell arrows, the chosen trade's entry, stop and targets as lines, and the equity
curve and drawdown below.

Library: TradingView Lightweight Charts (R7, Apache-2.0), bundled in vendor/lightweight-charts/ with its licence and
notice and published with the page - nothing is loaded from outside. Layout idea (panes stacked under the price chart:
equity, drawdown) from backtesting.py (R6, AGPL-3.0: the idea only, no code).

The research run writes the data (research.py -> Writer), build_dashboard.py publishes it with the page:
  charts/index.json                     what exists: strategy / version / timeframe cells, their coins, statuses
  charts/c/<COIN>_<tf>.json             the last candles of one coin and timeframe (shared by every strategy)
  charts/t/<id>_v<ver>_<tf>_<COIN>.json the backtest trades of one cell on one coin, the equity curve and drawdown
Pure helpers + a small file writer; no internet.
"""
import json
import os
import re

import numpy as np

CANDLES = 1500                 # candles per coin x timeframe on the page (the newest ones)
MAX_TRADES = 3000              # trades per file (the newest; the equity curve always uses all of them)
FIVE_MIN = 300_000


def slug(strategy, version, tf):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{strategy}_v{version}_{tf}")


def _num(x):
    return None if x is None or not np.isfinite(x) else float(f"{float(x):.7g}")


def candles_doc(coin, tf, df, n=CANDLES):
    """{coin, tf, t: [open time, seconds], o, h, l, c} of the newest n candles."""
    d = df.tail(n)
    return dict(coin=coin, tf=tf, t=[int(x) // 1000 for x in d["open_time"]],
                **{k[0]: [_num(x) for x in d[k]] for k in ("open", "high", "low", "close")})


def trades_doc(key, tf, coin, trades, open_times, bar_ms):
    """The trades of one cell on one coin: entry / exit time (seconds, candle open), direction, entry, stop, targets,
    result in R and why it closed; plus the equity curve (cumulative R at each exit) and its drawdown."""
    ot = np.asarray(open_times, dtype=np.int64)
    rows = []
    for t in sorted(trades, key=lambda x: x["entry_time"]):
        et = int(t["entry_time"])
        xi = t.get("exit_idx")
        if bar_ms is None and xi is not None and 0 <= int(xi) < len(ot):
            xt = int(ot[int(xi)])
        else:                                      # 5m-confirmed trades count their bars on 5m candles
            xt = et + (max(1, int(t.get("bars") or 1)) - 1) * int(bar_ms or FIVE_MIN)
        R = float(t.get("R") or 0.0)
        rows.append(dict(et=et // 1000, xt=max(xt, et) // 1000, d=int(t["dir"]), e=_num(t["entry"]),
                         s=_num(t["entry"] - t["dir"] * R) if R else None, tp=[_num(x) for x in t.get("tps") or []],
                         r=round(float(t["r"]), 3), why=str(t.get("reason") or "")))
    eq, dd, total, peak = [], [], 0.0, 0.0
    for x in sorted(rows, key=lambda x: x["xt"]):
        total += x["r"]
        peak = max(peak, total)
        if eq and eq[-1][0] == x["xt"]:            # several exits on one candle: one point
            eq[-1][1], dd[-1][1] = round(total, 3), round(total - peak, 3)
        else:
            eq.append([x["xt"], round(total, 3)])
            dd.append([x["xt"], round(total - peak, 3)])
    n = len(rows)
    return dict(key=key, tf=tf, coin=coin, n=n, total_r=round(total, 3),
                max_dd_r=round(-min([v for _, v in dd] or [0.0]), 3),
                trades=rows[-MAX_TRADES:], equity=eq, drawdown=dd)


class Writer:
    """Collects the research run's chart data into a folder (reports/backtest_charts)."""

    def __init__(self, folder):
        self.folder = folder
        self.cells = {}
        for sub in ("c", "t"):
            os.makedirs(os.path.join(folder, sub), exist_ok=True)
        for sub in ("c", "t"):                     # a fresh set every run
            for name in os.listdir(os.path.join(folder, sub)):
                os.remove(os.path.join(folder, sub, name))

    def _dump(self, rel, doc):
        with open(os.path.join(self.folder, rel), "w") as f:
            json.dump(doc, f, separators=(",", ":"))

    def candles(self, coin, tf, df):
        self._dump(f"c/{coin}_{tf}.json", candles_doc(coin, tf, df))

    def trades(self, strategy, version, tf, coin, trades, open_times, bar_ms=None):
        s = slug(strategy, version, tf)
        doc = trades_doc(f"{strategy}@{version}|{tf}", tf, coin, trades, open_times, bar_ms)
        self._dump(f"t/{s}_{coin}.json", doc)
        self.cells.setdefault((strategy, str(version), tf), {})[coin] = dict(n=doc["n"], total_r=doc["total_r"])

    def finish(self, cells, built_utc):
        """charts/index.json: every cell with its status and the coins that have a file."""
        rows = []
        for (sid, ver, tf), coins in sorted(self.cells.items()):
            c = cells.get(f"{sid}@{ver}|{tf}") or {}
            rows.append(dict(strategy=sid, version=ver, tf=tf, slug=slug(sid, ver, tf), status=c.get("status"),
                             lab=bool(c.get("lab")), coins=coins))
        self._dump("index.json", dict(built_utc=built_utc, candles=CANDLES, cells=rows))
        return rows

    def files(self):
        out = ["index.json"]
        for sub in ("c", "t"):
            out += [f"{sub}/{x}" for x in sorted(os.listdir(os.path.join(self.folder, sub)))]
        return out


def page_url(base, strategy, version, tf, coin=None):
    """The chart page of one strategy x timeframe (x coin) on the dashboard."""
    frag = f"s={strategy}&v={version}&tf={tf}" + (f"&c={coin}" if coin else "")
    return (base.rstrip("/") + "/" if base else "") + "chart.html#" + frag


def pages_base(cfg, repo=None):
    """The dashboard's address: config.yaml dashboard.url, else GitHub Pages of the repository."""
    url = ((cfg or {}).get("dashboard") or {}).get("url")
    if url:
        return str(url)
    repo = repo or os.environ.get("GITHUB_REPOSITORY") or "mayastraglobal-ui/crypto-signal-agent"
    owner, name = repo.split("/", 1)
    return f"https://{owner}.github.io/{name}/"


LIB = "vendor/lightweight-charts/lightweight-charts.standalone.production.js"

PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>TradeSentry - backtest chart</title>
<style>
:root{--bg:#0f1419;--fg:#e6e6e6;--mut:#8b949e;--card:#161b22;--line:#30363d;--up:#26a69a;--dn:#ef5350}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,Segoe UI,Roboto,sans-serif}
header,main,footer{max-width:1200px;margin:0 auto;padding:10px 14px}
h1{font-size:18px;margin:4px 0} a{color:#58a6ff} select,button{background:var(--card);color:var(--fg);
border:1px solid var(--line);border-radius:6px;padding:5px 8px;margin:2px}
.pane{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:8px 0}
.small{font-size:12px;color:var(--mut)} .bar{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.win{color:var(--up)} .loss{color:var(--dn)} .badge{border:1px solid var(--line);border-radius:10px;padding:1px 8px}
</style></head><body>
<header><h1>Backtest chart <span class="small">(BACKTEST - history, not a promise)</span></h1>
<div class="bar"><select id="cell"></select><select id="coin"></select>
<button id="prev">◀ trade</button><span id="pos" class="small"></span><button id="next">trade ▶</button>
<a href="index.html">dashboard</a></div><div id="info" class="small"></div></header>
<main><div class="small">Price: ▲ buy / ▼ sell at the entry candle, ● exit (green = won, red = lost). Lines: the
chosen trade's entry, stop and targets.</div><div id="price" class="pane"></div>
<div class="small">Equity: cumulative result in R of every backtest trade on this coin (after costs)</div>
<div id="equity" class="pane"></div><div class="small">Drawdown: R below the best point so far</div>
<div id="dd" class="pane"></div><div id="trade" class="small"></div></main>
<footer class="small">Charts: TradingView Lightweight Charts™ - Copyright (c) 2025 TradingView, Inc.
<a href="https://www.tradingview.com/">https://www.tradingview.com/</a> - Apache License 2.0
(<a href="vendor/lightweight-charts/LICENSE">licence</a>, <a href="vendor/lightweight-charts/NOTICE">notice</a>).
Built <span id="built"></span> UTC. Research signal. Not financial advice.</footer>
<script src="%(lib)s"></script>
<script>
"use strict";
const LW = window.LightweightCharts, $ = id => document.getElementById(id);
const LOC = (() => { try { new Intl.DateTimeFormat(navigator.language); return navigator.language; } catch (e) { return "en-US"; } })();
const opts = h => ({height: h, localization: {locale: LOC},
  layout: {background: {color: "#161b22"}, textColor: "#c9d1d9", attributionLogo: true},
  grid: {vertLines: {color: "#21262d"}, horzLines: {color: "#21262d"}}, timeScale: {timeVisible: true},
  rightPriceScale: {borderColor: "#30363d"}});
let index = null, data = null, sel = 0, lines = [], charts = [], priceSeries = null, markersApi = null;
function params() { const p = new URLSearchParams(location.hash.slice(1)); return Object.fromEntries(p.entries()); }
function setHash(o) { location.hash = new URLSearchParams(o).toString(); }
async function getJSON(u) { const r = await fetch(u, {cache: "no-cache"}); if (!r.ok) throw new Error(u + " " + r.status); return r.json(); }
function clearCharts() { charts.forEach(c => c.remove()); charts = []; lines = []; }
function fillSelects(p) {
  const cs = $("cell"); cs.innerHTML = "";
  index.cells.forEach((c, i) => { const o = document.createElement("option"); o.value = i;
    o.textContent = `${c.strategy} v${c.version} ${c.tf} (${c.status || "-"}${c.lab ? ", lab" : ""})`; cs.appendChild(o); });
  let i = index.cells.findIndex(c => c.strategy === p.s && c.version === p.v && c.tf === p.tf); if (i < 0) i = 0;
  cs.value = i; const cell = index.cells[i], coins = Object.keys(cell.coins).sort();
  const co = $("coin"); co.innerHTML = "";
  coins.forEach(k => { const o = document.createElement("option"); o.value = k;
    o.textContent = `${k} (${cell.coins[k].n} trades, ${cell.coins[k].total_r >= 0 ? "+" : ""}${cell.coins[k].total_r}R)`; co.appendChild(o); });
  co.value = coins.includes(p.c) ? p.c : coins[0]; return [cell, co.value];
}
function showTrade() {
  const T = data.trades.trades; if (!T.length) { $("pos").textContent = "no trades"; return; }
  sel = Math.max(0, Math.min(sel, T.length - 1)); const t = T[sel];
  lines.forEach(l => priceSeries.removePriceLine(l)); lines = [];
  const add = (price, color, title, style) => { if (price != null) lines.push(priceSeries.createPriceLine(
    {price, color, lineWidth: 1, lineStyle: style, axisLabelVisible: true, title})); };
  add(t.e, "#58a6ff", "entry", 0); add(t.s, "#ef5350", "stop", 2);
  t.tp.forEach((p, k) => add(p, "#26a69a", "TP" + (k + 1), 2));
  $("pos").textContent = `${sel + 1} / ${T.length}`;
  $("trade").innerHTML = `Trade ${sel + 1}: ${t.d > 0 ? "LONG" : "SHORT"} · entry ${t.e} · stop ${t.s} · targets ` +
    `${t.tp.join(", ")} · <span class="${t.r >= 0 ? "win" : "loss"}">${t.r >= 0 ? "+" : ""}${t.r}R</span> (${t.why}) · ` +
    `${new Date(t.et * 1000).toISOString().slice(0, 16)} → ${new Date(t.xt * 1000).toISOString().slice(0, 16)} UTC`;
  const cd = data.candles, inside = t.et >= cd.t[0] && t.et <= cd.t[cd.t.length - 1];
  if (!inside) $("trade").innerHTML += " · <b>older than the candles shown</b> (only its lines are drawn)";
  const step = cd.t.length > 1 ? cd.t[1] - cd.t[0] : 3600, span = Math.max(step * 30, (t.xt - t.et) * 4);
  if (inside) charts[0].timeScale().setVisibleRange({from: t.et - span, to: t.xt + span});
}
async function load() {
  const p = params(); const [cell, coin] = fillSelects(p);
  const [cd, td] = await Promise.all([getJSON(`charts/c/${coin}_${cell.tf}.json`), getJSON(`charts/t/${cell.slug}_${coin}.json`)]);
  data = {candles: cd, trades: td}; clearCharts();
  const pc = LW.createChart($("price"), opts(420)); charts.push(pc);
  priceSeries = pc.addSeries(LW.CandlestickSeries, {upColor: "#26a69a", downColor: "#ef5350", borderVisible: false,
    priceLineVisible: false,
    wickUpColor: "#26a69a", wickDownColor: "#ef5350"});
  priceSeries.setData(cd.t.map((t, i) => ({time: t, open: cd.o[i], high: cd.h[i], low: cd.l[i], close: cd.c[i]})));
  const first = cd.t[0], last = cd.t[cd.t.length - 1], mk = [];
  td.trades.forEach(t => {
    if (t.et >= first && t.et <= last) mk.push({time: t.et, position: t.d > 0 ? "belowBar" : "aboveBar",
      color: t.d > 0 ? "#26a69a" : "#ef5350", shape: t.d > 0 ? "arrowUp" : "arrowDown", text: t.d > 0 ? "buy" : "sell"});
    if (t.xt >= first && t.xt <= last) mk.push({time: t.xt, position: t.d > 0 ? "aboveBar" : "belowBar",
      color: t.r >= 0 ? "#26a69a" : "#ef5350", shape: "circle", text: (t.r >= 0 ? "+" : "") + t.r + "R"});
  });
  mk.sort((a, b) => a.time - b.time); markersApi = LW.createSeriesMarkers(priceSeries, mk);
  const ec = LW.createChart($("equity"), opts(180)); charts.push(ec);
  ec.addSeries(LW.LineSeries, {color: "#58a6ff", lineWidth: 2}).setData(td.equity.map(([time, value]) => ({time, value})));
  const dc = LW.createChart($("dd"), opts(140)); charts.push(dc);
  dc.addSeries(LW.AreaSeries, {lineColor: "#ef5350", topColor: "rgba(239,83,80,0.05)", bottomColor: "rgba(239,83,80,0.4)",
    invertFilledArea: false}).setData(td.drawdown.map(([time, value]) => ({time, value})));
  ec.timeScale().fitContent(); dc.timeScale().fitContent();
  $("info").textContent = `${cell.strategy} v${cell.version} · ${cell.tf} · ${coin}: ${td.n} backtest trades, ` +
    `total ${td.total_r >= 0 ? "+" : ""}${td.total_r}R, worst drawdown ${td.max_dd_r}R · status ${cell.status || "-"} · ` +
    `the price chart shows the newest ${cd.t.length} candles`;
  sel = td.trades.length - 1; showTrade(); window.chartReady = true;
}
$("prev").onclick = () => { sel--; showTrade(); }; $("next").onclick = () => { sel++; showTrade(); };
$("cell").onchange = () => { const c = index.cells[$("cell").value]; setHash({s: c.strategy, v: c.version, tf: c.tf}); };
$("coin").onchange = () => { const p = params(); p.c = $("coin").value; setHash(p); };
window.onhashchange = () => load().catch(e => { $("info").textContent = "could not load: " + e.message; });
getJSON("charts/index.json").then(ix => { index = ix; $("built").textContent = ix.built_utc;
  if (!ix.cells.length) { $("info").textContent = "no backtest chart data yet (the daily research run writes it)"; return; }
  return load(); }).catch(e => { $("info").textContent = "no backtest chart data yet: " + e.message; });
</script></body></html>
"""


def page():
    return PAGE % dict(lib=LIB)
