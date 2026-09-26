"""
The web dashboard (AGENT_PROMPT.md sections 2 and 27.4 step 16, "optional: web dashboard") - Phase 16.

One self-contained HTML page (no external scripts, fonts or images; charts are inline SVG drawn here), rebuilt
from the engine's own report files after every hourly scan, daily research run and Claude briefing, and published
to GitHub Pages (branch gh-pages). Deterministic code only: it shows the engine's numbers, never computes new ones.
BACKTEST, PAPER and LIVE are always labelled and never added together (section 24).

render(inputs) -> html. Pure; no internet, no files.
"""
import datetime as dt
import html
import json
import math
import re

STALE_HOURS = 2.0
STATUS_ORDER = ["APPROVED", "PAPER_TRADING", "VALIDATION", "BACKTESTING", "FAILED", "RETIRED", "FORMALIZED"]


def esc(x):
    return html.escape("" if x is None else str(x), quote=True)


def fnum(x, fmt="{:,.4g}"):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return "-"
    try:
        return fmt.format(float(x))
    except (TypeError, ValueError):
        return esc(x)


def fr(x):
    """An R value with its sign, or '-'."""
    return "-" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f"{float(x):+.2f}R"


def price(x):
    if x is None:
        return "-"
    x = float(x)
    return f"{x:,.2f}" if abs(x) >= 100 else f"{x:.4f}" if abs(x) >= 1 else f"{x:.6g}"


# ---------------------------------------------------------------------------------------------------------------
# small, safe markdown (Claude's files): escape first, then a few patterns; links only http(s)
# ---------------------------------------------------------------------------------------------------------------
def md(text, max_lines=200):
    out, in_list = [], False
    for raw in (text or "").splitlines()[:max_lines]:
        line = esc(raw.rstrip())
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)
        line = re.sub(r"\[([^\]]+)\]\((https?://(?:(?!&quot;)[^\s)<])+)\)",
                      r'<a href="\2" rel="noopener noreferrer" target="_blank">\1</a>', line)
        line = re.sub(r"(?<![\"=>])(https?://(?:(?!&quot;)[^\s<)])+)",
                      r'<a href="\1" rel="noopener noreferrer" target="_blank">\1</a>', line)
        m = re.match(r"^(#{1,4}) (.*)$", line)
        item = re.match(r"^\s*[-*] (.*)$", line)
        if in_list and not item:
            out.append("</ul>")
            in_list = False
        if m:
            lvl = min(len(m.group(1)) + 2, 6)
            out.append(f"<h{lvl}>{m.group(2)}</h{lvl}>")
        elif item:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{item.group(1)}</li>")
        elif line.strip():
            out.append(f"<p>{line}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------------------------
# SVG candle chart
# ---------------------------------------------------------------------------------------------------------------
def svg_chart(candles, levels=(), title="", width=460, height=210):
    """candles: [[open_ms, o, h, l, c], ...]; levels: [(label, price, css class)]. Inline SVG (theme via CSS)."""
    if not candles:
        return f'<div class="nochart">no candles for {esc(title)}</div>'
    lv = [(a, float(p), c) for a, p, c in levels if p is not None and math.isfinite(float(p))]
    lo = min(min(k[3] for k in candles), *[p for _, p, _ in lv]) if lv else min(k[3] for k in candles)
    hi = max(max(k[2] for k in candles), *[p for _, p, _ in lv]) if lv else max(k[2] for k in candles)
    pad = (hi - lo) * 0.06 or abs(hi) * 0.01 or 1.0
    lo, hi = lo - pad, hi + pad
    left, right, top, bottom = 4, 112, 20, 20
    w, h = width - left - right, height - top - bottom
    n = len(candles)
    step = w / n
    y = lambda p: top + (hi - p) / (hi - lo) * h
    parts = [f'<svg class="chart" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}" '
             f'preserveAspectRatio="xMidYMid meet">',
             f'<text class="ctitle" x="{left}" y="14">{esc(title)}</text>']
    for i, (t, o, hh, ll, c) in enumerate(candles):
        x = left + i * step + step / 2
        cls = "up" if c >= o else "dn"
        parts.append(f'<line class="wick {cls}" x1="{x:.1f}" x2="{x:.1f}" y1="{y(hh):.1f}" y2="{y(ll):.1f}"/>')
        y1, y2 = sorted((y(o), y(c)))
        parts.append(f'<rect class="body {cls}" x="{x - step * 0.35:.1f}" y="{y1:.1f}" width="{max(step * 0.7, 0.8):.1f}" '
                     f'height="{max(y2 - y1, 0.6):.1f}"/>')
    for label, p, cls in lv:
        parts.append(f'<line class="lvl {cls}" x1="{left}" x2="{left + w}" y1="{y(p):.1f}" y2="{y(p):.1f}"/>')
    last = candles[-1][4]
    tags = sorted([(y(p), f"{label} {price(p)}", cls) for label, p, cls in lv] + [(y(last), price(last), "last")])
    gap, placed = 14.0, []                     # labels never overlap: push each one below the one above it
    for yy, text, cls in tags:
        yy = max(yy, placed[-1][0] + gap) if placed else yy
        placed.append((yy, text, cls))
    shift = max(0.0, placed[-1][0] - (top + h)) if placed else 0.0
    for yy, text, cls in placed:
        parts.append(f'<text class="lbl {cls}" x="{left + w + 3}" y="{yy - shift + 4:.1f}">{esc(text)}</text>')
    d0 = dt.datetime.fromtimestamp(candles[0][0] / 1000, dt.timezone.utc).strftime("%m-%d %H:%M")
    d1 = dt.datetime.fromtimestamp(candles[-1][0] / 1000, dt.timezone.utc).strftime("%m-%d %H:%M")
    parts.append(f'<text class="axis" x="{left}" y="{height - 4}">{d0}</text>')
    parts.append(f'<text class="axis" x="{left + w}" y="{height - 4}" text-anchor="end">{d1} UTC</text>')
    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------------------------------------------
# page
# ---------------------------------------------------------------------------------------------------------------
CSS = """
:root{--bg:#f6f7f9;--card:#fff;--fg:#1c2230;--mut:#5f6b7a;--line:#e3e6eb;--up:#16a34a;--dn:#dc2626;--acc:#2563eb;
--warn:#b45309;--warnbg:#fef3c7;--bad:#b91c1c;--badbg:#fee2e2;--ok:#15803d;--okbg:#dcfce7;--ai:#7c3aed;--aibg:#f3e8ff}
@media (prefers-color-scheme:dark){:root{--bg:#0f1218;--card:#171b23;--fg:#e6e9ef;--mut:#9aa4b2;--line:#2a303b;
--up:#22c55e;--dn:#f87171;--acc:#60a5fa;--warn:#fbbf24;--warnbg:#3a2a07;--bad:#fca5a5;--badbg:#3b1111;--ok:#86efac;
--okbg:#0f2e1b;--ai:#c4b5fd;--aibg:#241a3a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,-apple-system,
"Segoe UI",Roboto,sans-serif}a{color:var(--acc)}header{position:sticky;top:0;z-index:5;background:var(--card);
border-bottom:1px solid var(--line);padding:10px 16px}header h1{font-size:17px;margin:0 0 4px}nav{display:flex;gap:6px;
overflow-x:auto;padding-top:6px}nav a{white-space:nowrap;text-decoration:none;font-size:13px;padding:3px 9px;
border:1px solid var(--line);border-radius:14px;color:var(--fg)}main{max-width:1100px;margin:0 auto;padding:12px 16px 40px}
section{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:14px 0;
scroll-margin-top:96px}h2{font-size:16px;margin:0 0 8px}h3,h4,h5,h6{font-size:14px;margin:12px 0 4px}
.badge{display:inline-block;font-size:12px;padding:1px 8px;border-radius:10px;margin:2px 4px 2px 0;font-weight:600}
.ok{background:var(--okbg);color:var(--ok)}.warn{background:var(--warnbg);color:var(--warn)}
.bad{background:var(--badbg);color:var(--bad)}.ai{background:var(--aibg);color:var(--ai)}.mut{color:var(--mut)}
.small{font-size:13px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.card{border:1px solid var(--line);border-radius:8px;padding:8px 10px}.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:5px 6px;
border-bottom:1px solid var(--line);white-space:nowrap}th{color:var(--mut);font-weight:600}
.pos{color:var(--up)}.neg{color:var(--dn)}svg.chart{width:100%;height:auto;display:block}
svg .wick{stroke-width:1}svg .up{stroke:var(--up);fill:var(--up)}svg .dn{stroke:var(--dn);fill:var(--dn)}
svg .lvl{stroke-width:1.2;stroke-dasharray:5 4}svg .lbl,svg .axis,svg .ctitle{font-size:13px;fill:var(--mut)}
svg .ctitle{font-weight:600;fill:var(--fg)}svg .entry{stroke:var(--acc);fill:var(--acc)}svg .stop{stroke:var(--dn);
fill:var(--dn)}svg .tp{stroke:var(--up);fill:var(--up)}svg .last{fill:var(--fg)}.nochart{color:var(--mut);font-size:13px}
.ai-box{border-left:4px solid var(--ai);padding-left:10px}details summary{cursor:pointer;color:var(--acc);margin:6px 0}
footer{text-align:center;color:var(--mut);font-size:13px;padding:10px}code{font-size:12px}
"""
JS = """(function(){var el=document.getElementById('age');if(!el)return;var t=Date.parse(el.dataset.utc.replace(' ','T')+':00Z');
if(isNaN(t))return;var h=(Date.now()-t)/36e5;var s=h<1?Math.round(h*60)+' min ago':h.toFixed(1)+' h ago';
el.textContent=s;if(h>%s){el.className='badge bad';el.textContent='STALE: last update '+s+
' - the hourly scan may have stopped. Do not act on this page.';}})();"""


def _rclass(x):
    return "" if x is None else "pos" if float(x) > 0 else "neg" if float(x) < 0 else ""


def table(headers, rows, cls=""):
    if not rows:
        return '<p class="mut small">none</p>'
    h = "".join(f"<th>{esc(x)}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def render(inp):
    """inp: dict(latest, research, candles, briefing=(path, text), review=(path, text), approval_files, pine_files,
    repo_url, built_utc). Every part may be missing; the page says so instead of failing."""
    rep = inp.get("latest") or {}
    research = inp.get("research") or {}
    dash = inp.get("candles") or {}
    candles = dash.get("candles") or {}
    repo = inp.get("repo_url") or ""
    blob = lambda p: f"{repo}/blob/main/{p}" if repo else p
    book = rep.get("position_book") or {}
    risk = rep.get("risk") or {}
    daily = rep.get("daily") or {}
    gen = rep.get("generated_utc") or "-"
    state = daily.get("data_state") or (rep.get("data_quality") or {}).get("system_state") or "unknown"
    S = []

    # ---------- header ----------
    st_cls = "ok" if str(state).startswith("GOOD") else "bad" if "UNSAFE" in str(state) else "warn"
    head = (f'<header><h1>TradeSentry dashboard</h1><div class="small">Engine report {esc(gen)} UTC · '
            f'{esc(book.get("beijing", ""))} Beijing · <span class="badge {st_cls}">data {esc(state)}</span>'
            f'<span id="age" class="badge ok" data-utc="{esc(gen)}">updated {esc(gen)} UTC</span></div>'
            '<nav><a href="#book">Positions</a><a href="#market">Market</a><a href="#signals">Signals</a>'
            '<a href="#strategies">Strategies</a><a href="#approval">Approval</a><a href="#risk">Risk</a>'
            '<a href="#claude">Claude</a><a href="chart.html">Backtest charts</a></nav></header>')
    if not rep:
        S.append('<section><h2>No engine report yet</h2><p>The hourly scan has not published '
                 '<code>reports/latest.json</code> yet. This page fills in after the next scan.</p></section>')

    # ---------- 1. position book ----------
    L = book.get("limits") or {}
    b = [f'<section id="book"><h2>1. Position book</h2><p class="small">'
         f'Day <b class="{_rclass(book.get("day_r"))}">{fr(book.get("day_r"))}</b> (limit {esc(L.get("day_r", "-"))}R) · '
         f'Week <b class="{_rclass(book.get("week_r"))}">{fr(book.get("week_r"))}</b> (limit {esc(L.get("week_r", "-"))}R) · '
         f'Heat {esc(book.get("heat", 0))}/{esc(L.get("heat", "-"))}'
         + (f' · paper today {fr(book.get("paper_day_r"))}' if book.get("paper_day_r") else "") + "</p>"]
    if book.get("empty", True):
        b.append('<p>No open or pending positions. <span class="mut">No trade is a valid result.</span></p>')
    rows = [[f'<b>{esc(p["coin"])}</b>', esc(p["direction"]), esc(p["tf"]), f'{esc(p["strategy"])} v{esc(p["version"])}',
             '<span class="badge ok">LIVE</span>', price(p.get("entry")), price(p.get("stop")),
             f'<span class="{_rclass(p.get("open_r"))}">{fr(p.get("open_r"))}</span>', esc(p.get("next_action"))]
            for p in book.get("active") or []]
    rows += [[f'<b>{esc(p["coin"])}</b>', esc(p["direction"]), esc(p["tf"]), f'{esc(p["strategy"])} v{esc(p["version"])}',
              f'<span class="badge warn">PAPER · {esc(p["stage"])}</span>', price(p.get("entry")), price(p.get("stop")),
              f'<span class="{_rclass(p.get("open_r"))}">{fr(p.get("open_r"))}</span>', esc(p.get("next_action"))]
             for p in book.get("paper") or []]
    if rows:
        b.append("<h3>Open</h3>" + table(["Coin", "Side", "TF", "Strategy", "Stage", "Entry", "Stop", "Open R",
                                           "Next action"], rows))
    if book.get("awaiting"):
        b.append("<h3>Waiting for the 5-minute confirmation</h3>" + table(
            ["Coin", "Side", "TF", "Strategy", "Stage", "5m bars", "Trigger"],
            [[esc(p["coin"]), esc(p["direction"]), esc(p["tf"]), esc(p["strategy"]), esc(p["stage"]),
              f'{esc(p.get("bars"))}/6', esc(p.get("trigger"))] for p in book["awaiting"]]))
    if book.get("closed_today"):
        b.append("<h3>Closed today</h3>" + table(
            ["Coin", "Side", "TF", "Strategy", "Reason", "Result", "Stage"],
            [[esc(p["coin"]), esc(p["direction"]), esc(p["tf"]), esc(p["strategy"]), esc(p.get("reason")),
              f'<span class="{_rclass(p.get("result_r"))}">{fr(p.get("result_r"))}</span>',
              "LIVE" if p.get("live") else "PAPER"] for p in book["closed_today"]]))
    charts = []
    for p in (book.get("active") or []) + (book.get("paper") or []):
        tf = p.get("sim_tf") or p["tf"]
        c = (candles.get(p["coin"]) or {}).get(tf)
        charts.append(svg_chart(c, [("entry", p.get("entry"), "entry"), ("stop", p.get("stop"), "stop"),
                                    ("TP1", p.get("tp1"), "tp")],
                                f'{p["coin"]} {tf} · {p["strategy"]} {p["direction"]} ({"LIVE" if p in (book.get("active") or []) else "PAPER"})'))
    if charts:
        b.append('<div class="grid">' + "".join(f'<div class="card">{c}</div>' for c in charts) + "</div>")
    S.append("".join(b) + "</section>")

    # ---------- 2. market ----------
    btc = daily.get("btc") or {}
    fg = daily.get("fear_greed")
    m = [f'<section id="market"><h2>2. Market</h2><p class="small">BTC trend: daily <b>{esc(btc.get("1d", "?"))}</b>, '
         f'4H <b>{esc(btc.get("4h", "?"))}</b>' + (f' · Fear &amp; Greed {esc(fg["value"])} ({esc(fg["label"])})' if fg else "")
         + "</p>"]
    m.append(table(["Coin", "Price", "24h vol (M)", "Regime 1W / 1D / 4H / 1H", "30m momentum", "15m setup", "5m trigger"],
                   [[f'<b>{esc(r["coin"])}</b>', price(r.get("price")), fnum(r.get("vol_24h_m"), "{:,.0f}"),
                     esc(" / ".join(r.get("regimes") or [])), esc(r.get("mom_30m")), esc(r.get("setup_15m")),
                     esc(r.get("trigger_5m"))] for r in daily.get("matrix") or []]))
    pos_by_coin = {}
    for p in (book.get("active") or []) + (book.get("paper") or []):
        if (p.get("sim_tf") or p["tf"]) == "1h":
            pos_by_coin.setdefault(p["coin"], p)
    grid = []
    for r in daily.get("matrix") or []:
        p = pos_by_coin.get(r["coin"])
        lv = [("entry", p.get("entry"), "entry"), ("stop", p.get("stop"), "stop"), ("TP1", p.get("tp1"), "tp")] if p else []
        grid.append(svg_chart((candles.get(r["coin"]) or {}).get("1h"), lv, f'{r["coin"]} 1h'))
    if grid:
        m.append('<div class="grid">' + "".join(f'<div class="card">{c}</div>' for c in grid) + "</div>")
    S.append("".join(m) + "</section>")

    # ---------- 3. signals ----------
    sg = ['<section id="signals"><h2>3. Signals</h2>']
    live = rep.get("signals") or []
    sg.append("<h3>LIVE (approved strategies - these are emailed)</h3>")
    sg.append(table(["Coin", "Side", "TF", "Strategy", "Entry", "Stop", "Targets", "Signal (UTC)"],
                    [[f'<b>{esc(p["coin"])}</b>', esc(p["direction"]), esc(p["timeframe"]),
                      f'{esc(p["strategy"])} v{esc(p.get("version"))}', price(p.get("entry")), price(p.get("stop")),
                      esc(", ".join(price(t["price"]) for t in p.get("targets") or [])), esc(p.get("signal_time_utc"))]
                     for p in live]) if live else '<p>No live signal. <span class="mut">No trade is a valid result.</span></p>')
    vs = rep.get("validation_signals") or []
    sg.append("<h3>PAPER / VALIDATION (logged; PAPER_TRADING ones get PAPER emails - practice, not for trading)</h3>")
    sg.append(table(["Coin", "Side", "TF", "Strategy", "Stage", "Entry", "Stop", "Signal (UTC)"],
                    [[esc(p["coin"]), esc(p["direction"]), esc(p["timeframe"]), esc(p["strategy"]),
                      f'<span class="badge warn">{esc(p.get("stage"))}</span>', price(p.get("entry")),
                      price(p.get("stop")), esc(p.get("signal_time_utc"))] for p in vs]))
    wt = rep.get("watching") or []
    sg.append("<h3>Watching (setups, not signals)</h3>")
    sg.append(table(["Coin", "Side", "TF", "Strategy", "Stage", "State", "Rules true", "Missing"],
                    [[esc(w["coin"]), esc(w["direction"]), esc(w["tf"]), esc(w["strategy"]), esc(w["stage"]),
                      esc(w["state"]), esc(w.get("rules_true")), f'<code>{esc(w.get("missing") or "-")}</code>']
                     for w in wt[:30]]))
    S.append("".join(sg) + "</section>")

    # ---------- 4. strategies ----------
    board = rep.get("strategy_scoreboard") or []
    counts = {}
    for x in board:
        counts[x["status"]] = counts.get(x["status"], 0) + 1
    st = [f'<section id="strategies"><h2>4. Strategies</h2><p class="small">'
          + " ".join(f'<span class="badge {"ok" if k == "APPROVED" else "warn" if k in ("PAPER_TRADING", "VALIDATION") else ""}">'
                     f'{esc(k)} {v}</span>' for k, v in sorted(counts.items(), key=lambda kv: STATUS_ORDER.index(kv[0])
                                                               if kv[0] in STATUS_ORDER else 99))
          + '</p><p class="small mut">BACKTEST = history (Layer B, all coins together). LIVE = real signals of approved '
            "strategies. They are never added together.</p>"]
    order = lambda x: (STATUS_ORDER.index(x["status"]) if x["status"] in STATUS_ORDER else 99, x["strategy"], x["tf"])
    charted = {(c["strategy"], str(c["version"]), c["tf"]) for c in (inp.get("charts") or {}).get("cells") or []}

    def chart_link(x):                                # Phase 18 D: the backtest chart page of this cell
        k = (x["strategy"], str(x["version"]), x["tf"])
        return (f'<a href="chart.html#s={esc(k[0])}&amp;v={esc(k[1])}&amp;tf={esc(k[2])}">chart</a>' if k in charted
                else '<span class="mut">-</span>')
    rows = []
    for x in sorted(board, key=order):
        rows.append([f'{esc(x["strategy"])} v{esc(x["version"])}', esc(x["tf"]), esc(x["status"]),
                     fnum(x.get("trades"), "{:.0f}"), f'<span class="{_rclass(x.get("avg_r"))}">{fr(x.get("avg_r"))}</span>',
                     fnum(x.get("profit_factor"), "{:.2f}"), esc(x.get("walk_forward") or "-"),
                     esc(x.get("live_signals") or 0), fr(x.get("live_avg_r")), chart_link(x)])
    top = [r for r, x in zip(rows, sorted(board, key=order)) if x["status"] in ("APPROVED", "PAPER_TRADING", "VALIDATION")]
    rest = [r for r, x in zip(rows, sorted(board, key=order)) if x["status"] not in ("APPROVED", "PAPER_TRADING", "VALIDATION")]
    hdr = ["Strategy", "TF", "Status", "BACKTEST trades", "BACKTEST avg", "PF", "Walk-forward", "LIVE signals", "LIVE avg",
           "Backtest chart"]
    st.append(table(hdr, top) if top else "<p>No strategy has passed the backtest bar yet - no paper or live signals.</p>")
    if rest:
        st.append(f"<details><summary>All other strategy versions ({len(rest)})</summary>{table(hdr, rest)}</details>")
    changes = (rep.get("lifecycle") or {}).get("changes") or []
    if changes:
        st.append("<h3>Status changes in the last research run</h3><ul class='small'>" + "".join(
            f'<li>{esc(c["key"])} {esc(c["tf"])}: {esc(c["old"])} → <b>{esc(c["new"])}</b></li>' for c in changes[:20])
            + "</ul>")
    S.append("".join(st) + "</section>")

    # ---------- 5. approval ----------
    appr = (rep.get("lifecycle") or {}).get("approval") or research.get("approval") or {}
    ap = ['<section id="approval"><h2>5. Approval packs (your yes / no)</h2>']
    for p in appr.get("eligible") or []:
        ap.append(f'<div class="card"><b>Approve {esc(p["strategy"])} v{esc(p["version"])} {esc(p["tf"])} for live emails? '
                  f'(yes/no)</b><br><span class="small">PAPER {esc(p["paper_signals"])} signals, average '
                  f'{fr(p.get("paper_avg_r"))} · BACKTEST unseen {fr(p.get("backtest_validate_avg_r"))} · '
                  f'<a href="{esc(blob(p["pack"]))}">read the pack</a> · '
                  f'<a href="chart.html#s={esc(p["strategy"])}&amp;v={esc(p["version"])}&amp;tf={esc(p["tf"])}">backtest '
                  'chart</a>' + (f' · <a href="{esc(blob(p["pine"]))}">Pine script</a>' if p.get("pine") else "")
                  + ' · to say yes, copy its line into <code>config.yaml</code> → <code>approvals:</code></span></div>')
    if not appr.get("eligible"):
        ap.append("<p>No strategy is ready: an approval pack appears after 20+ paper signals that meet the section 12 "
                  "numbers.</p>")
    ap += [f'<p class="small warn">⚠ {esc(w)}</p>' for w in (appr.get("warnings") or [])[:8]]
    pines = inp.get("pine_files") or []
    if pines:
        ap.append("<h3>TradingView scripts</h3><ul class='small'>" + "".join(
            f'<li><a href="{esc(blob(f))}">{esc(f.split("/")[-1])}</a></li>' for f in pines) + "</ul>")
    S.append("".join(ap) + "</section>")

    # ---------- 6. risk ----------
    rk = ['<section id="risk"><h2>6. Risk engine</h2>']
    halts = (risk.get("halts_text") or []) + [f"SUSPENDED {s}" for s in risk.get("suspended") or []]
    rk.append("<p>" + ("".join(f'<span class="badge bad">{esc(h)}</span>' for h in halts)
                       or '<span class="badge ok">no halt</span>')
              + f' <span class="small">risk per trade {esc(risk.get("risk_pct", "-"))}%</span></p>')
    if risk.get("blackout_now"):
        rk.append('<p><span class="badge bad">EVENT BLACKOUT NOW - no live entries</span></p>')
    ev = risk.get("upcoming_events") or []
    rk.append("<h3>Upcoming high-impact events (UTC)</h3>" + ("<ul class='small'>" + "".join(
        f"<li>{esc(e if isinstance(e, str) else json.dumps(e))}</li>" for e in ev) + "</ul>" if ev else
        '<p class="small">none listed</p>'))
    if risk.get("calendar_warning"):
        rk.append(f'<p><span class="badge warn">⚠ {esc(risk["calendar_warning"])}</span></p>')
    lim = risk.get("limits") or {}
    if lim:
        rk.append('<p class="small mut">Limits: day ' + esc(lim.get("day_r")) + "R · week " + esc(lim.get("week_r"))
                  + "R · max " + esc(lim.get("positions")) + " positions, " + esc(lim.get("per_coin")) + " per coin · TP1 ≥ "
                  + esc(lim.get("min_tp1_r")) + "R · leverage ≤ " + esc(lim.get("max_leverage")) + "x · blackout ±"
                  + esc(lim.get("blackout_minutes")) + " min</p>")
    groups = risk.get("groups") or []
    if groups:
        rk.append('<p class="small">Coins that move together (1 position per direction per group): '
                  + "; ".join(esc("+".join(g) if isinstance(g, list) else g) for g in groups) + "</p>")
    S.append("".join(rk) + "</section>")

    # ---------- 7. Claude ----------
    cl = ['<section id="claude"><h2>7. Claude (written by the AI - the numbers above are the facts)</h2>']
    for label, item in (("Latest briefing", inp.get("briefing")), ("Latest daily review", inp.get("review"))):
        if item:
            path, text = item
            cl.append(f'<details {"open" if label == "Latest briefing" else ""}><summary><span class="badge ai">AI</span>'
                      f'{esc(label)} - {esc(path.split("/")[-1][:-3])}</summary><div class="ai-box">{md(text)}</div>'
                      f'<p class="small"><a href="{esc(blob(path))}">open the file</a></p></details>')
        else:
            cl.append(f'<p class="small mut">{esc(label)}: none yet.</p>')
    mem = rep.get("memory") or {}
    if mem.get("due"):
        cl.append(f'<p class="small">Memory reviews due: {len(mem["due"])} (the daily review handles them).</p>')
    S.append("".join(cl) + "</section>")

    foot = (f'<footer>Built {esc(inp.get("built_utc", ""))} UTC from the engine\'s report files · '
            f'<a href="{esc(blob("reports/latest.md"))}">full report</a> · '
            "Research signal. Not financial advice.</footer>")
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<meta name=\"robots\" content=\"noindex\"><title>TradeSentry dashboard</title>"
            f"<style>{CSS}</style></head><body>{head}<main>{''.join(S)}</main>{foot}"
            f"<script>{JS % STALE_HOURS}</script></body></html>")
