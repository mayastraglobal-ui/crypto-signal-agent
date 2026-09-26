"""
The engine's numbers for the report emails (format v2): briefing 08:20, the changes-only briefings 14:20 / 21:20, the
daily review and the weekly report. Taken from the engine's own files - passed in already loaded: latest.json (the
hourly scan), research.json (the daily research run), research_counts.json (one line per research day),
memory/strategy_registry.csv, strategies_lab.yaml, memory/lessons.md, memory/experiments.md, memory/changelog.md,
memory/research_sources.md, memory/curriculum.md, reports/feeds.json, reports/derivs_quality.json.

Nothing is computed that the engine did not measure: counts, statuses, prices and results are copied; a missing
value stays None and the email shows "–". Pure functions.
"""
import csv
import datetime as dt
import io
import re

from engine import btcharts
from engine import emails as em
from engine import idea_queue as iq

PASSED = ("VALIDATION", "PAPER_TRADING", "APPROVED")
NOT_PASSED = ("FORMALIZED", "BACKTESTING", "FAILED", "NEW")
BUCKET = {"APPROVED": "APPROVED", "PAPER_TRADING": "PAPER", "FAILED": "FAILED", "RETIRED": "FAILED",
          "BIASED": "FAILED"}                                  # everything else (IDEA ... VALIDATION) = TESTING
RESEARCH_UTC = "00:40"         # the daily research run (.github/workflows/research.yml cron "40 0 * * *")
SCAN_LATE_H = 2                # "scans on time": the newest scan is at most 2 hours old
VERDICT = {"identifiable": "real miss", "a setup existed": "filtered by a gate", "not identifiable": "correct skip"}


# ---------------------------------------------------------------- small readers --------------------------------------
def _move(row):
    """The 30-minute move of a coin row (the scan's rate of change, %): the number, or None."""
    if row.get("move_30m") is not None:
        return row["move_30m"]
    m = re.match(r"^([+-]?\d+(?:\.\d+)?)%", str(row.get("mom_30m") or ""))
    return float(m.group(1)) if m else None


def coin_rows(rep):
    """The signal coins (in the scan's order): price, daily regime, 24h change, 30-minute move."""
    rep = rep or {}
    uni = rep.get("universe") or {}
    change = {c["coin"]: c.get("change_24h") for c in uni.get("candidates") or [] if isinstance(c, dict)}
    signal = set(uni.get("signal") or [])
    out = []
    for r in (rep.get("daily") or {}).get("matrix") or []:
        if signal and r["coin"] not in signal:
            continue
        reg = r.get("regimes") or []
        out.append(dict(coin=r["coin"], price=r.get("price"), regime_1d=reg[1] if len(reg) > 1 else None,
                        change_24h=change.get(r["coin"]), move_30m=_move(r)))
    return out


def status(rep):
    """Open live trades, the limit, today's and this week's live R (the position book)."""
    b = (rep or {}).get("position_book") or {}
    lim = (b.get("limits") or {}).get("heat")
    return dict(open=b.get("heat"), max_open=lim, day_r=b.get("day_r"), week_r=b.get("week_r"))


def registry_cells(text):
    """memory/strategy_registry.csv -> {(id, version, tf): the newest row} (one row per strategy x timeframe cell)."""
    out = {}
    for r in csv.DictReader(io.StringIO(text or "")):
        if r.get("id") and r.get("tf"):
            out[(r["id"], str(r.get("version") or "1.0"), r["tf"])] = r
    return out


def progress_counts(cells):
    """Approved / Paper / Testing / Failed cells (+ Tested = all of them) from registry_cells()."""
    c = dict(APPROVED=0, PAPER=0, TESTING=0, FAILED=0)
    for r in (cells or {}).values():
        st = "BIASED" if str(r.get("bias") or "").strip() else r.get("status")
        c[BUCKET.get(st, "TESTING")] += 1
    c["TESTED"] = len(cells or {})
    return c


def decisions(research):
    return [f"{p['strategy']} v{p['version']} {p['tf']}" for p in
            ((research or {}).get("approval") or {}).get("eligible") or []]


def headings(text, since, until=None, rx=r"^### (.+)$"):
    """Titles of the memory records ('### title' + '- timestamp: YYYY-MM-DD ...') written in [since, until)."""
    out, title = [], None
    for line in (text or "").splitlines():
        m = re.match(rx, line)
        if m:
            title = m.group(1).strip()
            continue
        t = re.match(r"^- timestamp: (\d{4}-\d{2}-\d{2})", line)
        if t and title:
            if t.group(1) >= since and (until is None or t.group(1) < until):
                out.append(title)
            title = None
    return out


def changelog(text):
    """memory/changelog.md -> [(date, title)] ('## 2026-09-26 · who · title')."""
    out = []
    for line in (text or "").splitlines():
        m = re.match(r"^## (\d{4}-\d{2}-\d{2}) · [^·]+ · (.+)$", line)
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


def study_item(curriculum_text, sources_text):
    """Today's reading-plan item (memory/curriculum.md), as the daily review gets it: 'C01 Time Series Momentum'."""
    from engine import curriculum as cur
    item = cur.next_item(cur.parse_plan(curriculum_text or ""), cur.studied(sources_text or ""))
    return f"{item['id']} {item['title']}" if item else None


def next_events(rep, now, days=7, n=3):
    risk = (rep or {}).get("risk") or {}
    out = []
    for e in risk.get("upcoming_events") or []:
        t = em.to_dt(e.get("start_utc"))
        if t and now and dt.timedelta(0) <= t - now <= dt.timedelta(days=days):
            out.append(e)
    return out[:n]


def lab_ideas(lab_cards, research, day, queue_text=None):
    """The lab cards dated `day`: name + timeframe, what it does, a SOURCE chip and a STATUS chip."""
    cells = (research or {}).get("cells") or {}
    queued = {q["key"] for q in iq.parse(queue_text or "")}
    out = []
    for c in lab_cards or []:
        if not isinstance(c, dict) or str(c.get("added") or "") != day:
            continue
        st = [x["status"] for x in cells.values() if x.get("strategy") == c.get("id")
              and str(x.get("version")) == str(c.get("version"))]
        tfs = ", ".join(c.get("timeframes") or [])
        out.append(dict(name=f"{c.get('id')} v{c.get('version')}" + (f" · {tfs}" if tfs else ""),
                        what=re.sub(r"\s+", " ", str(c.get("description") or c.get("hypothesis") or "")).strip()[:140],
                        source=em.source_chip(c, queued), status=em.status_chip(st)))
    return out


def untested_lab(lab_cards, research):
    """Lab cards the research run has not tested yet (no cell in research.json)."""
    cells = (research or {}).get("cells") or {}
    seen = {(x.get("strategy"), str(x.get("version"))) for x in cells.values()}
    return [f"{c.get('id')}" for c in lab_cards or [] if isinstance(c, dict)
            and (c.get("id"), str(c.get("version"))) not in seen]


def lessons_on(text, day):
    """Records added to memory/lessons.md on `day` (their timestamp starts with it)."""
    return len(re.findall(r"^- timestamp: " + re.escape(day), text or "", re.M))


def counts_for(hist, day):
    return next((x for x in reversed(hist or []) if x.get("date") == day), None)


def closed_today(rep, live):
    return [t for t in ((rep or {}).get("position_book") or {}).get("closed_today") or []
            if bool(t.get("live")) == live and t.get("state") == "CLOSED"]


def _prev(day):
    try:
        return (dt.date.fromisoformat(day) - dt.timedelta(days=1)).isoformat()
    except ValueError:
        return None


def missed_line(moves, day):
    """'SUI +13.4% (correct skip), ENA +18.4% (real miss)' - the strong moves research found that day."""
    out = []
    for m in moves or []:
        if not str(m.get("start_utc") or "").startswith(day or "-"):
            continue
        v = next((w for k, w in VERDICT.items() if str(m.get("verdict") or "").startswith(k)), "–")
        sign = 1 if m.get("direction") == "up" else -1
        out.append(f"{m['coin']} {em.pct(sign * float(m['pct']), 1) if m.get('pct') is not None else '–'} ({v})")
    return ", ".join(out[:4]) + (f" and {len(out) - 4} more" if len(out) > 4 else "") if out else None


def health(rep, derivs, now, tests=None):
    """SYSTEM HEALTH: [(text, ok)] - data, scans on time, tests on main, candidate coins with bad data, blocked
    exchange data. The last two are warnings only (never an ALERT email)."""
    rep = rep or {}
    out = []
    dq = rep.get("data_quality") or {}
    state = dq.get("system_state") or (rep.get("daily") or {}).get("data_state")
    out.append((f"Data {state or '–'}", state == "GOOD"))
    last = em.to_dt(rep.get("generated_utc"))
    if last and now:
        out.append(("Scans on time" if now - last <= dt.timedelta(hours=SCAN_LATE_H) else
                    f"Last scan {em.bj(rep['generated_utc'], '%H:%M')}", now - last <= dt.timedelta(hours=SCAN_LATE_H)))
    if tests:
        out.append(tests)
    signal = set((rep.get("universe") or {}).get("signal") or [])
    bad = sorted(c for c, x in (dq.get("coins") or {}).items() if c not in signal and x.get("state") == "UNSAFE")
    if bad:
        out.append((f"Candidate coins with bad data: {', '.join(bad[:4])}", False))
    blocked = sorted({c for c, x in ((derivs or {}).get("coins") or {}).items()
                      if any("451" in str(e) for e in ((x.get("fetch") or {}).get("errors") or []))})
    if blocked:
        out.append(("Binance futures data blocked (451) – OKX used", False))
    return out


def plan_today(research, counts_hist, lab_cards, close, study):
    """AGENT PLAN TODAY: TEST (today's research run), CHECK (the card to watch), STUDY (the curriculum item)."""
    last = (counts_hist or [None])[-1] or {}
    new = untested_lab(lab_cards, research)
    test = (f"{em.plural(last.get('backtests'), 'backtest')} on {em.val(last.get('coins'))} coins at "
            f"{em.bj('2000-01-01 ' + RESEARCH_UTC, '%H:%M')}" if last else
            f"Research run at {em.bj('2000-01-01 ' + RESEARCH_UTC, '%H:%M')}")
    if new:
        test += ", incl. new " + ", ".join(new[:2])
    check = f"{close[0][0]} – {close[0][3]}" if close else None
    return dict(test=test, check=check, study=study)


# ---------------------------------------------------------------- H. briefing 08:20 ----------------------------------
def briefing(rep, slot, utc, summary, page_url, dashboard_url, research=None, registry_text=None, counts_hist=None,
             lab_cards=None, study=None):
    rep = rep or {}
    st = status(rep)
    coins = coin_rows(rep)
    btc = next((c for c in coins if c["coin"] == "BTC"), None) or next(
        (dict(price=r.get("price")) for r in (rep.get("daily") or {}).get("matrix") or [] if r["coin"] == "BTC"), {})
    cells = registry_cells(registry_text)
    close = em.closest((research or {}).get("cells"))
    counts = progress_counts(cells)
    return dict(slot=slot, utc=utc, signals=len(rep["signals"]) if isinstance(rep.get("signals"), list) else None,
                open=st["open"], max_open=st["max_open"],
                data_state=(rep.get("data_quality") or {}).get("system_state") or (rep.get("daily") or {}).get("data_state"),
                btc=dict(price=btc.get("price"), trend=(rep.get("market") or {}).get("btc_trend") or {}),
                fear_greed=(rep.get("market") or {}).get("fear_greed") or {}, coins=coins,
                events=next_events(rep, em.to_dt(utc)), plan=plan_today(research, counts_hist, lab_cards, close, study),
                progress=dict(counts=counts if cells else {}, closest=close), last_scan_utc=rep.get("generated_utc"),
                decisions=decisions(research), approved=counts["APPROVED"] if cells else None, summary=summary,
                page_url=page_url, dashboard_url=dashboard_url)


# ---------------------------------------------------------------- I. changes since the last briefing ------------------
def snapshot(rep, research, registry_text, lab_cards):
    """What the 14:20 / 21:20 briefings compare with (saved after each briefing)."""
    rep = rep or {}
    now = em.to_dt(rep.get("generated_utc"))
    return dict(utc=rep.get("generated_utc"),
                signals=sorted(f"{p['coin']} {p['direction']} {p['timeframe']} {p['strategy']}"
                               for p in rep.get("signals") or [] if isinstance(p, dict) and "coin" in p),
                regimes={c["coin"]: c["regime_1d"] for c in coin_rows(rep)},
                statuses={f"{k[0]} v{k[1]} {k[2]}": ("BIASED" if str(r.get("bias") or "").strip() else r.get("status"))
                          for k, r in registry_cells(registry_text).items()},
                lab=sorted(f"{c.get('id')}@{c.get('version')}" for c in lab_cards or [] if isinstance(c, dict)),
                events=sorted(f"{e.get('start_utc')}|{e.get('type') or em.short_event(e.get('name'))}"
                              for e in next_events(rep, now, 1, 9)),
                data=(rep.get("data_quality") or {}).get("system_state"),
                halts=sorted(str(h) for h in ((rep.get("risk") or {}).get("halts_text") or [])))


def diff(prev, now):
    """[(icon, text)] of what changed between two snapshots (prev None = nothing to compare: no changes)."""
    if not prev:
        return []
    out = []
    for s in sorted(set(now["signals"]) - set(prev.get("signals") or [])):
        out.append(("▲", f"New LIVE signal: {s}"))
    for c, r in now["regimes"].items():
        old = (prev.get("regimes") or {}).get(c)
        if old and r and old != r and em.TREND.get(old) != em.TREND.get(r):
            out.append(("◆", f"{c} daily trend: {em.TREND.get(old, old)} → {em.TREND.get(r, r)}"))
    for k, v in now["statuses"].items():
        old = (prev.get("statuses") or {}).get(k)
        if old and v and old != v:
            out.append(("✓" if v in PASSED else "✕" if v in ("FAILED", "RETIRED", "BIASED") else "◆",
                        f"{k}: {old} → {v}"))
    for c in sorted(set(now["lab"]) - set(prev.get("lab") or [])):
        out.append(("◆", f"New idea in the lab: {c.split('@')[0]}. Testing starts at the next research run."))
    for e in sorted(set(now["events"]) - set(prev.get("events") or [])):
        start, _, name = e.partition("|")
        out.append(("!", f"Within 24 hours: {name} {em.bj(start, '%a %H:%M')} – no new trades ±1 hour"))
    if now.get("data") != prev.get("data") and now.get("data"):
        out.append(("!" if now["data"] != "GOOD" else "✓", f"Data {prev.get('data') or '–'} → {now['data']}"))
    for h in sorted(set(now["halts"]) - set(prev.get("halts") or [])):
        out.append(("!", f"Risk halt: {h}"))
    for h in sorted(set(prev.get("halts") or []) - set(now["halts"])):
        out.append(("✓", f"Risk halt ended: {h}"))
    return out


def changes(rep, slot, prev_slot, utc, change_list, page_url, research=None):
    rep = rep or {}
    st = status(rep)
    now = em.to_dt(utc)
    return dict(slot=slot, prev_slot=prev_slot, utc=utc, changes=change_list,
                signals=len(rep["signals"]) if isinstance(rep.get("signals"), list) else None, open=st["open"],
                max_open=st["max_open"], btc_trend=(rep.get("market") or {}).get("btc_trend") or {},
                next_event=(next_events(rep, now) or [None])[0],
                data_state=(rep.get("data_quality") or {}).get("system_state"), decisions=decisions(research),
                page_url=page_url)


# ---------------------------------------------------------------- J. daily review ------------------------------------
def daily(rep, research, counts_hist, lab_cards, lessons_text, queue_text, day, utc, summary, page_url, dashboard_url,
          registry_text=None, changelog_text=None, merged=None, derivs=None, tests=None):
    """The daily review (the UTC day `day`, 23:30 Beijing). merged = [(date, PR title)] of merged pull requests."""
    rep = rep or {}
    st = status(rep)
    research = research or {}
    cells = registry_cells(registry_text)
    run_day = str(research.get("run_utc") or "")[:10]
    status_lines = [f"{c['key'].split('@')[0]} {c['tf']}: {c['old']} → {c['new']}" for c in research.get("changes") or []
                    if run_day == day and c.get("old") != c.get("new")]
    built = [t for d, t in changelog(changelog_text) if d == day] + [t for d, t in merged or [] if d == day]
    return dict(date=day, utc=utc, live_trades=closed_today(rep, True), paper_trades=closed_today(rep, False),
                day_r=st["day_r"], week_r=st["week_r"], open=st["open"],
                missed=missed_line(research.get("missed_moves"), day),
                counts=counts_for(counts_hist, day) or counts_for(counts_hist, _prev(day)),
                status_lines=status_lines[:4] + ([f"… and {len(status_lines) - 4} more"] if len(status_lines) > 4 else []),
                built_lines=built[:4], ideas=lab_ideas(lab_cards, research, day, queue_text),
                lessons_added=lessons_on(lessons_text, day), closest=em.closest(research.get("cells")),
                events=next_events(rep, em.to_dt(utc)), research_time=em.bj("2000-01-01 " + RESEARCH_UTC, "%H:%M"),
                decisions=decisions(research), approved=progress_counts(cells)["APPROVED"] if cells else None,
                health=health(rep, derivs, em.to_dt(utc), tests), summary=summary, page_url=page_url,
                dashboard_url=dashboard_url)


# ---------------------------------------------------------------- K. weekly -------------------------------------------
def passed_between(lifecycle_lines):
    """Strategy cells that moved UP to VALIDATION or better (lines of the lifecycle log, 'x: OLD → NEW (...)')."""
    n = 0
    for ln in lifecycle_lines or []:
        m = re.search(r"(\w+) → (\w+)", ln)
        if m and m.group(2) in PASSED and m.group(1) in NOT_PASSED:
            n += 1
    return n


def _stage(results, stage):
    x = next((r for r in results or [] if r.get("stage") == stage), None) or {}
    return dict(n=x.get("n"), total_r=x.get("total_r"))


def weekly(rep, research, lab_cards, queue_text, now, summary, page_url, dashboard_url, pages_base=None, repo_url=None,
           registry_text=None, changelog_text=None, merged=None, lessons_text=None, sources_text=None, feeds=None,
           study=None, tests=None):
    """The weekly report of the 7 days ending `now` (UTC datetime). merged = [(date, PR title)]."""
    rep = rep or {}
    research = research or {}
    wk = rep.get("weekly") or {}
    days = [(now.date() - dt.timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    since = days[0]
    moves = wk.get("missed_moves") or []
    by = {}
    for m in moves:
        v = next((w for k, w in VERDICT.items() if str(m.get("verdict") or "").startswith(k)), "other")
        by[v] = by.get(v, 0) + 1
    appr = (research.get("approval") or {}).get("eligible") or []
    dec = []
    for p in appr:
        cell = f"{p['strategy']} v{p['version']} {p['tf']}"
        dec.append(dict(cell=cell, pack_url=f"{repo_url}/blob/main/{p['pack']}" if repo_url and p.get("pack") else None,
                        chart_url=p.get("chart") or (btcharts.page_url(pages_base, p["strategy"], p["version"], p["tf"])
                                                     if pages_base else None)))
    log = changelog(changelog_text)
    prs = list(merged or [])
    history = []
    for d in days:
        items = [t for x, t in log if x == d] + [t for x, t in prs if x == d]
        if items:
            history.append((em.bj(d + " 12:00", "%a %d"), "; ".join(items[:3]) + (f" (+{len(items) - 3} more)"
                                                                                    if len(items) > 3 else "")))
    mistakes = [re.sub(r"^Fix:\s*", "", t) for x, t in log + prs if x >= since and re.match(r"^Fix\b", t)]
    bad_feeds = sorted(k for k, v in ((feeds or {}).get("sources") or {}).items()
                       if isinstance(v, dict) and v.get("status") not in (None, "ok"))
    queued = [q["key"].split("@")[0] for q in iq.parse(queue_text or "")]
    in_lab = {c.get("id") for c in lab_cards or [] if isinstance(c, dict)}
    close = em.closest(research.get("cells"))
    cells = registry_cells(registry_text)
    ev = next_events(rep, now)
    return dict(week_no=now.isocalendar()[1], utc=now.strftime("%Y-%m-%d %H:%M"),
                days=(f"{int(days[0][8:])}–{now.day} {now:%b}" if days[0][5:7] == f"{now.month:02d}" else
                      f"{int(days[0][8:])} {dt.date.fromisoformat(days[0]):%b} – {now.day} {now:%b}"),
                live=_stage(wk.get("results"), "APPROVED"), paper=_stage(wk.get("results"), "PAPER_TRADING"),
                week_r=status(rep)["week_r"],
                missed=dict(n=len(moves) if wk else None, text=", ".join(f"{n} {k}" for k, n in sorted(by.items()))),
                funnel=progress_counts(cells) if cells else {}, closest=close,
                passed=passed_between(wk.get("lifecycle")), decision=dec,
                learned=dict(mistakes=mistakes[:3], testing=headings(lessons_text, since)[:3],
                             online=headings(sources_text, since)[:3],
                             blocked=f"Feeds failing: {', '.join(bad_feeds)}" if bad_feeds else None),
                history=history, tests=tests, card=wk.get("card"),
                next=dict(test=", ".join([q for q in queued if q not in in_lab][:2]) or None,
                          fix=f"{close[0][0]} – {close[0][3]}" if close else None, study=study,
                          events=" · ".join(f"{e.get('type') or em.short_event(e.get('name'))} "
                                            f"{em.bj(e.get('start_utc'), '%a %d')}" for e in ev) or None),
                summary=summary, page_url=page_url, dashboard_url=dashboard_url)
