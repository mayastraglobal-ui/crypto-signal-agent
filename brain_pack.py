#!/usr/bin/env python3
"""
The fact sheet for Claude's scheduled tasks (Phase 14; tasks/*.md).

Claude explains and researches - it never computes prices, results or statistics itself (AGENT_PROMPT.md
section 1). This prints every number a task needs, taken from the engine's own files:

  python publish_live.py --refresh      (first: fetch the NEWEST large report files, e.g. latest.json, research.json)
  python brain_pack.py briefing         (position book, market, signals, risk, events)
  python brain_pack.py daily            (+ last 24 hours: closed signals, losses and tags, lifecycle, reviews due,
                                          the strategy lab and the trials counter)
  python brain_pack.py weekly           (+ last 7 days, missed moves, candidate lessons, approval packs, SMC twins,
                                          the lab, the event calendar)

Read-only: it writes nothing (it only fetches the live-reports branch to check that the local copies are the newest).
If they are not, the fact sheet starts with "!!! STALE ENGINE FILES".
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

import pandas as pd

from engine import digest
from engine import memory as mem

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(ROOT, "reports")
MEMORY = os.path.join(ROOT, "memory")


def load_json(name):
    p = os.path.join(REPORTS, name)
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)


def read(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def recent_files(folder, n=3):
    d = os.path.join(REPORTS, "claude", folder)
    names = sorted(x for x in os.listdir(d) if x.endswith(".md")) if os.path.isdir(d) else []
    return [f"reports/claude/{folder}/{x}" for x in names[-n:]]


def fmt_r(x):
    return "-" if x is None or x != x else f"{float(x):+.2f}R"


def target(kind, now):
    """Where this run's output goes (the Brain guard only accepts these names).
    briefing: Beijing date + the nearest slot 0820 / 1420 / 2120; daily and weekly: the UTC date (the morning
    [DAILY] email reads yesterday's review, the Sunday [WEEKLY] email reads that Sunday's research)."""
    if kind == "briefing":
        bj = now + dt.timedelta(hours=8)
        mins = bj.hour * 60 + bj.minute
        slot = min(("0820", 500), ("1420", 860), ("2120", 1280), key=lambda s: abs(mins - s[1]))[0]
        return f"reports/claude/briefings/{bj:%Y-%m-%d}-{slot}.md"
    return f"reports/claude/{kind}/{now:%Y-%m-%d}.md"


def calendar_lines(now, days=90):
    """events.yaml as the weekly task needs it: what is listed for the next 90 days, how each date was checked,
    and which months have no NFP / CPI / PCE / FOMC entry yet."""
    from engine import risk as rk
    out = ["", f"## Event calendar (events.yaml) - next {days} days, and what looks missing"]
    try:
        items = rk.load_calendar(os.path.join(ROOT, rk.CALENDAR_FILE))
    except ValueError as e:
        return out + [f"- ! {e}"]
    t0, t1 = now.strftime("%Y-%m-%d"), (now + dt.timedelta(days=days)).strftime("%Y-%m-%d")
    listed = [e for e in items if t0 <= str(e.get("utc", ""))[:10] <= t1]
    out += [f"- {e.get('utc')} UTC {e.get('type')}: {e.get('name')} (check: {e.get('check', '-')})" for e in listed] \
        or ["- nothing listed"]
    months = sorted({(now + dt.timedelta(days=d)).strftime("%Y-%m") for d in range(0, days + 1, 7)}
                    - {now.strftime("%Y-%m")})             # the current month may already be past its releases
    for m in months:
        have = {e.get("type") for e in items if str(e.get("utc", "")).startswith(m)}
        miss = [t for t in ("NFP", "CPI", "PCE") if t not in have]
        if miss:
            out.append(f"- {m}: no {', '.join(miss)} entry yet (FOMC meets 8 times a year - check its calendar)")
    return out


def lab_lines(now, research):
    """Phase 17: where candidates go (strategies_lab.yaml), how many may still be added, what exists already, the
    trials counter, and how the lab cards are doing."""
    import yaml
    from engine import brain
    from engine import strategy_spec as sspec
    out = ["", "## Strategy lab (strategies_lab.yaml) - where your candidate cards go"]
    try:
        lab = brain._cards(read(os.path.join(ROOT, sspec.LAB_FILE)))
        lib = brain._cards(read(os.path.join(ROOT, sspec.LIBRARY_FILE)))
    except (yaml.YAMLError, ValueError) as e:
        return out + [f"- ! the lab or library file is not readable ({e}) - add no card, say so in your output"]
    days = [brain._day(c.get("added")) for c in lab if isinstance(c, dict)]
    today = now.date()
    n_day = sum(d == today for d in days)
    n_week = sum(d is not None and today - dt.timedelta(days=6) <= d <= today for d in days)
    left = max(0, min(brain.LAB_PER_DAY - n_day, brain.LAB_PER_WEEK - n_week))
    out += [f"- cards in the lab: {len(lab)} · added today: {n_day} of {brain.LAB_PER_DAY} · last 7 days: {n_week} of "
            f"{brain.LAB_PER_WEEK} · you may add at most {left} card(s) now (a control twin counts)",
            f"- write each card with added: \"{today}\", status: FORMALIZED, evidence_class, source, targets (first "
            f">= {sspec.MIN_TP1_R:g}R), a changelog line, and a control twin (twin_of) for an SMC / 5m ingredient"]
    latest = {}
    for c, where in [(c, "library") for c in lib] + [(c, "lab") for c in lab]:
        if isinstance(c, dict) and c.get("id"):
            old = latest.get(c["id"])
            try:
                if old is None or sspec._vkey(c.get("version")) > sspec._vkey(old[0]):
                    latest[c["id"]] = (str(c.get("version")), where)
            except ValueError:
                pass
    out += ["- existing ids (latest version): " + "; ".join(f"{k} v{v} ({w})" for k, (v, w) in sorted(latest.items()))]
    tr = (research or {}).get("trials")
    out += [f"- trials counter: {tr['total']} tests so far; PAPER_TRADING needs t >= {tr['need_t']:.2f} - every new "
            "card raises this bar for all" if tr else "- trials counter: not available yet (next research run)"]
    cells = [(k, c) for k, c in ((research or {}).get("cells") or {}).items() if c.get("lab")]
    out += [f"- lab cell {k}: {c['status']} · {c['evidence']['all']['n']} trades, {fmt_r(c['evidence']['all']['avg_r'])}"
            f" · t {c.get('t_stat') if c.get('t_stat') is not None else '-'}" for k, c in sorted(cells)[:30]] \
        or ["- no lab card has been researched yet"]
    return out


def feed_lines(now, kind):
    """reports/feeds.json (fetched hourly by GitHub Actions - this environment cannot open news sites)."""
    f = load_json("feeds.json")
    out = ["", "## Outside feeds (reports/feeds.json - fetched by GitHub Actions every hour)"]
    if f is None:
        return out + ["- not available yet (the hourly scan writes it) - say so; do not guess the news"]
    age = (now - pd.Timestamp(f["generated_utc"], tz="UTC").to_pydatetime()).total_seconds() / 3600
    out += [f"- fetched {f['generated_utc']} UTC ({age:.1f} hours ago)" + (" - STALE: say so" if age > 2.5 else ""),
            f"- ! {f.get('note')}"]
    out += [f"- source {k}: {v['status']}" + (f" ({v.get('error')})" if v.get("error") else "")
            for k, v in (f.get("sources") or {}).items() if v["status"] != "ok"]
    fg = f.get("fear_greed")
    out.append(f"- Fear & Greed: {fg['value']} ({fg['label']}), yesterday {fg.get('yesterday')}; last 7 days "
               + ", ".join(str(d["value"]) for d in fg.get("last_7_days") or []) if fg else "- Fear & Greed: not available")
    hours = 12 if kind == "briefing" else 24 if kind == "daily" else 24 * 7
    since = (now - dt.timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M")
    news = [x for x in f.get("news") or [] if (x.get("utc") or "") >= since][:25 if kind != "weekly" else 40]
    out += [f"### Headlines, last {hours} hours (CLAIMs - quote with source and link, never as evidence)"]
    out += [f"- {x['utc']} {x['source']}: {x['title']}" + (f" [coins: {', '.join(x['coins'])}]" if x.get("coins") else "")
            + (f" - {x['link']}" if x.get("link") else "") for x in news] or ["- none in this period"]
    b = f.get("binance") or {}
    out += ["### Binance announcements (newest first)"]
    for k in ("listing", "delisting", "maintenance"):
        out += [f"- {k}: {x['utc']} {x['title']}" + (f" [coins: {', '.join(x['coins'])}]" if x.get("coins") else "")
                + (f" - {x['link']}" if x.get("link") else "") for x in (b.get(k) or [])[:5]]
    if not any(b.get(k) for k in ("listing", "delisting", "maintenance")):
        out.append("- none (or not available - see the sources above)")
    out += ["### Deribit options: next expiries (08:00 UTC; open interest in coins; max pain = the strike where "
            "option buyers would get the least)"]
    out += [f"- {x['currency']} {x['expiry_utc']} ({x['hours_left']:.0f} h): open interest {x['open_interest']:,} "
            f"(calls {x['calls']:,} / puts {x['puts']:,}, put/call {x['put_call']}), "
            + (f"~${x['notional_usd'] / 1e9:.2f}bn, " if x.get("notional_usd") else "") + f"max pain {x['max_pain']:,.0f}"
            for x in f.get("deribit") or []] or ["- not available"]
    return out


LIVE_FILES = ["reports/latest.json", "reports/research.json", "reports/smc.json", "reports/regime.json",
              "reports/features.json", "reports/data_quality.json", "reports/feature_evidence.json"]


def live_status(root=ROOT, remote="origin", branch="live-reports"):
    """The newest live-reports commit vs the local copies: dict(commit, differs=[paths], missing=[paths]),
    or None when the branch cannot be fetched."""
    def git(*a):
        return subprocess.run(["git", *a], cwd=root, capture_output=True, text=True)
    if git("fetch", "--quiet", "--depth=1", remote, branch).returncode != 0:
        return None
    out = dict(commit=git("log", "-1", "--format=%s", "FETCH_HEAD").stdout.strip(), differs=[], missing=[])
    for path in LIVE_FILES:
        remote_blob = git("rev-parse", "--verify", "--quiet", f"FETCH_HEAD:{path}").stdout.strip()
        if not remote_blob:
            continue
        if not os.path.exists(os.path.join(root, path)):
            out["missing"].append(path)
        elif git("hash-object", path).stdout.strip() != remote_blob:
            out["differs"].append(path)
    return out


def md_updated(text):
    """'2026-09-25 10:18' from the '**Updated:** ... (2026-09-25 10:18 UTC)' line of reports/latest.md."""
    m = re.search(r"\*\*Updated:\*\*.*?\((\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC\)", text or "")
    return m.group(1) if m else None


def stale_warnings(rep, md_text, live):
    """Why the local engine files may be old copies (Claude's task sessions keep files from earlier runs)."""
    w = []
    gen, upd = (rep or {}).get("generated_utc"), md_updated(md_text)
    if rep is not None and gen and upd and upd > gen:
        w.append(f"reports/latest.json is from {gen} UTC, but reports/latest.md on main was updated {upd} UTC - "
                 "the local latest.json is an OLD copy")
    if live:
        for p in live["differs"]:
            w.append(f"{p} is not the newest copy on live-reports ({live['commit']})")
        for p in live["missing"]:
            w.append(f"{p} is missing locally but exists on live-reports ({live['commit']})")
    return w


def pack(kind, now, live=None):
    """live: live_status() (main() checks it; None = not checked)."""
    rep, research = load_json("latest.json"), load_json("research.json")
    warn = stale_warnings(rep, read(os.path.join(REPORTS, "latest.md")), live)
    head = (["!!! STALE ENGINE FILES - read this first !!!"] + [f"!!! {x}" for x in warn]
            + [f"!!! Run `python publish_live.py --refresh`, then `python brain_pack.py {kind}` again. If this "
               "stays, say so at the top of your output and do not present these numbers as current.", ""]
            if warn else [])
    out = head + [f"# Fact sheet for the {kind} task - {now:%Y-%m-%d %H:%M} UTC",
           "All numbers below come from the engine. Quote them; never recompute or invent numbers.",
           f"WRITE YOUR OUTPUT TO: {target(kind, now)}", ""]
    if rep is None:
        return out + ["reports/latest.json is missing - run `python publish_live.py --refresh` first. "
                      "If it is still missing, say in your output that the engine report was not available."]
    age_h = (now - pd.Timestamp(rep["generated_utc"], tz="UTC").to_pydatetime()).total_seconds() / 3600
    out += [f"Engine report: {rep['generated_utc']} UTC ({age_h:.1f} hours old)"
            + (" - STALE: say so, the hourly scan may have failed" if age_h > 2.5 else ""),
            f"Data state: {rep['daily'].get('data_state', '?')}", "", "## Position book (copy as is)"]
    out += rep.get("position_book_text") or ["(none)"]
    out += ["", "## Market, top coins, strategy health, event calendar (the engine's daily block)"]
    out += (rep.get("daily_lines") or [])[1:]
    out += ["", "## Signals this run"]
    sig = rep.get("signals") or []
    out += [f"- LIVE {(p.get('email') or {}).get('subject') or p['coin'] + ' ' + p['direction']}: entry {p.get('entry')}, "
            f"stop {p.get('stop')}, targets {', '.join(str(t['price']) for t in p.get('targets') or [])}"
            for p in sig] or ["- no live signal"]
    vs = rep.get("validation_signals") or []
    out += [f"- {len(vs)} paper / validation signal(s) (logged, not emailed): "
            + "; ".join(f"{p['coin']} {p['direction']} {p['timeframe']} {p['strategy']} ({p.get('stage')})" for p in vs[:10])]
    out += [f"- watching (not signals): " + ("; ".join(f"{w['coin']} {w['direction']} {w['tf']} {w['strategy']} "
                                                       f"{w['state']} ({w['stage']})" for w in (rep.get('watching') or [])[:10])
                                             or "none")]
    risk = rep.get("risk") or {}
    out += ["", "## Risk engine", f"- halts: {'; '.join(risk.get('halts_text') or []) or 'none'}",
            f"- suspended strategies: {', '.join(map(str, risk.get('suspended') or [])) or 'none'}",
            f"- next events: {'; '.join(map(str, risk.get('upcoming_events') or [])) or 'none listed'}"
            + (f" (! {risk['calendar_warning']})" if risk.get("calendar_warning") else "")]
    out += feed_lines(now, kind)
    if kind == "briefing":
        out += ["", "## Your earlier outputs (read the newest for continuity)"] + [f"- {p}" for p in
                                                                                    recent_files("briefings", 2)]
        return out

    days = 1 if kind == "daily" else 7
    a, b = pd.Timestamp(now - dt.timedelta(days=days)), pd.Timestamp(now)
    logp = os.path.join(REPORTS, "signals_log.csv")
    logdf = pd.read_csv(logp, dtype=str) if os.path.exists(logp) else pd.DataFrame()
    rows = digest.closed_between(logdf, a, b)
    out += ["", f"## Closed signals, last {days} day(s) (LIVE / PAPER / VALIDATION kept apart)"]
    out += [f"- {r['label']}: {r['n']} closed, {r['wins']} won, total {r['total_r']:+.2f}R" for r in digest.results_by_stage(rows)]
    out += [f"  - {x['coin']} {x['tf']} {x['strategy']} v{x.get('version')} {x.get('direction')} ({x.get('stage')}): "
            f"{fmt_r(float(x['result_r']))} {x.get('close_reason') or ''} · tags: {x.get('tags') or '-'} · "
            f"MAE {x.get('mae_r') or '-'} MFE {x.get('mfe_r') or '-'}" for x in rows[:40]]
    exp = logdf[logdf["state"].isin(["EXPIRED", "INVALIDATED", "NO_TRADE"])] if not logdf.empty and "state" in logdf else []
    if len(exp):
        t = pd.to_datetime(exp["signal_time_utc"], utc=True, errors="coerce")
        exp = exp[(t >= a) & (t < b)]
        out += [f"- {x['state']}: {x['coin']} {x['tf']} {x['strategy']} - {x.get('state_note') or ''}"
                for x in exp.to_dict("records")[:20]]
    out += ["", "## Failure tags on losing signals"] + ([f"- {t}: {n}" for t, n in digest.loss_tags(rows)] or ["- none"])
    life = digest.lifecycle_between(read(os.path.join(MEMORY, "strategy_lifecycle.md")), a, b)
    out += ["", f"## Lifecycle changes, last {days} day(s)"] + ([f"- {x}" for x in life[:40]] or ["- none"])
    research = research or {}
    out += ["", f"## Daily research run: {research.get('run_utc', 'not available')}"]
    out += ["### Candidate lessons (systematic in 2+ backtests)"] + (
        [f"- {c['tag']}: {c['evidence']} ({', '.join(c['cells'][:6])})" for c in research.get("candidate_lessons") or []]
        or ["- none"])
    moves = [m for m in research.get("missed_moves") or [] if pd.Timestamp(m["start_utc"], tz="UTC") >= a]
    out += ["### Missed strong moves"] + ([f"- {m['coin']} {m['direction']} {m['size_atr']}x ATR from {m['start_utc']} "
                                          f"(regime before: {m.get('regime')}): {m['verdict']}" for m in moves[:20]]
                                         or ["- none in this period"])
    failing = [(k, c) for k, c in (research.get("cells") or {}).items()
               if c["status"] in ("FAILED", "BACKTESTING") and c["evidence"]["all"]["n"] >= 30]
    out += ["### Failing strategy cells with 30+ backtest trades (diagnosis from engine/attribution.py)"]
    for k, c in sorted(failing, key=lambda x: x[1]["evidence"]["all"]["avg_r"])[:12]:
        att = c.get("attribution") or {}
        out += [f"- {k}: {c['evidence']['all']['n']} trades, {fmt_r(c['evidence']['all']['avg_r'])}; systematic tags: "
                f"{', '.join(att.get('systematic') or []) or 'none'}"] + [f"  - {d}" for d in (att.get("diagnosis") or [])[:4]]
    appr = research.get("approval") or {}
    out += ["### Approval packs"] + ([f"- {p['key']}: {p['pack']}" for p in appr.get("eligible") or []] or ["- none eligible"])
    out += [f"- ! {w}" for w in appr.get("warnings") or []]
    if kind == "weekly":
        cells = research.get("cells") or {}
        out += ["### Control-twin comparisons (does the special ingredient add anything?)"]
        out += [f"- {k}: {'beats' if c.get('beats_twin') else 'does not beat' if c.get('beats_twin') is False else 'too few trades vs'} "
                f"its twin" for k, c in sorted(cells.items()) if c.get("beats_twin") is not None or c.get("twin_same_window")][:30]
    out += lab_lines(now, research)
    if kind == "weekly":
        out += calendar_lines(now)
    st = mem.status(MEMORY, now)
    out += ["", "## Memory reviews due (write a NEW review record for each; never edit the old one)"]
    out += [f"- {d['file']}: {d['title']} (due {d['review']})" for d in st["due"][:30]] or ["- none"]
    lessons = mem.parse(read(os.path.join(MEMORY, "lessons.md")) or "")
    out += ["", "## Existing lessons"] + ([f"- {r['title']} ({r.get('evidence')})" for r in lessons] or ["- none yet"])
    out += ["", "## Your earlier outputs (read them first)"] + [f"- {p}" for p in
                                                                 recent_files("daily") + recent_files("weekly", 2)]
    return out


def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "briefing"
    if kind not in ("briefing", "daily", "weekly"):
        sys.exit("usage: python brain_pack.py briefing|daily|weekly")
    live = live_status()
    lines = pack(kind, dt.datetime.now(dt.timezone.utc), live)
    if live is None:
        lines.insert(lines.index(next(x for x in lines if x.startswith("# Fact sheet"))) + 1,
                     "(could not reach the live-reports branch to check that the engine files are the newest)")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
