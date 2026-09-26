"""
The engine's numbers for the briefing, daily review and weekly emails (email redesign), taken from the engine's own
files - passed in already loaded: latest.json (the hourly scan), research.json (the daily research run),
research_counts.json (one line per research day), strategies_lab.yaml, memory/lessons.md, memory/experiments.md.

Nothing is computed that the engine did not measure: counts, statuses, prices and results are copied; a missing
value stays None and the email shows "–". Pure functions.
"""
import datetime as dt
import re

from engine import btcharts
from engine import emails as em
from engine import idea_queue as iq

PASSED = ("VALIDATION", "PAPER_TRADING", "APPROVED")
NOT_PASSED = ("FORMALIZED", "BACKTESTING", "FAILED", "NEW")
CLOSE_R = 0.10                   # the weekly "Close" tile: cells within 0.10R per trade of the average-R bar


def _move(row):
    """The 30-minute move of a coin row (the scan's rate of change, %): the number, or None."""
    if row.get("move_30m") is not None:
        return row["move_30m"]
    m = re.match(r"^([+-]?\d+(?:\.\d+)?)%", str(row.get("mom_30m") or ""))
    return float(m.group(1)) if m else None


def coin_rows(rep):
    out = []
    for r in ((rep or {}).get("daily") or {}).get("matrix") or []:
        reg = r.get("regimes") or []
        out.append(dict(coin=r["coin"], price=r.get("price"), regime_1d=reg[1] if len(reg) > 1 else None,
                        move_30m=_move(r)))
    return out


def status(rep):
    """Open live trades, the limit, today's and this week's live R (the position book)."""
    b = (rep or {}).get("position_book") or {}
    lim = (b.get("limits") or {}).get("heat")
    return dict(open=b.get("heat"), max_open=lim, day_r=b.get("day_r"), week_r=b.get("week_r"))


def briefing(rep, slot, utc, summary, page_url, dashboard_url):
    rep = rep or {}
    risk = rep.get("risk") or {}
    events = risk.get("upcoming_events") or []
    now = em.to_dt(utc)
    soon = [e for e in events if now and em.to_dt(e.get("start_utc"))
            and dt.timedelta(0) <= em.to_dt(e["start_utc"]) - now <= dt.timedelta(hours=24)]
    st = status(rep)
    return dict(slot=slot, utc=utc, signals=len(rep["signals"]) if isinstance(rep.get("signals"), list) else None,
                open=st["open"], max_open=st["max_open"],
                data_state=(rep.get("data_quality") or {}).get("system_state") or (rep.get("daily") or {}).get("data_state"),
                coins=coin_rows(rep), events=events[:3], halts=risk.get("halts") or [],
                blackout_now=risk.get("blackout_now") or [], event_24h=bool(soon), summary=summary,
                page_url=page_url, dashboard_url=dashboard_url)


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


def lessons_on(text, day):
    """Records added to memory/lessons.md on `day` (their timestamp starts with it)."""
    return len(re.findall(r"^- timestamp: " + re.escape(day), text or "", re.M))


def counts_for(hist, day):
    return next((x for x in reversed(hist or []) if x.get("date") == day), None)


def live_closed_today(rep):
    return [t for t in ((rep or {}).get("position_book") or {}).get("closed_today") or []
            if t.get("live") and t.get("state") == "CLOSED"]


def daily(rep, research, counts_hist, lab_cards, lessons_text, queue_text, day, utc, summary, page_url, dashboard_url):
    """The daily review (the UTC day `day`, 23:30 Beijing)."""
    return dict(date=day, utc=utc, trades=live_closed_today(rep), day_r=status(rep)["day_r"],
                counts=counts_for(counts_hist, day) or counts_for(counts_hist, _prev(day)),
                signal_coins=((rep or {}).get("universe") or {}).get("signal") or [r["coin"] for r in coin_rows(rep)],
                ideas=lab_ideas(lab_cards, research, day, queue_text), lessons_added=lessons_on(lessons_text, day),
                closest=em.closest((research or {}).get("cells")), summary=summary, page_url=page_url,
                dashboard_url=dashboard_url)


def _prev(day):
    try:
        return (dt.date.fromisoformat(day) - dt.timedelta(days=1)).isoformat()
    except ValueError:
        return None


def passed_between(lifecycle_lines):
    """Strategy cells that moved UP to VALIDATION or better (lines of the lifecycle log, 'x: OLD → NEW (...)')."""
    n = 0
    for ln in lifecycle_lines or []:
        m = re.search(r"(\w+) → (\w+)", ln)
        if m and m.group(2) in PASSED and m.group(1) in NOT_PASSED:
            n += 1
    return n


def close_cells(research, limit=CLOSE_R):
    """Cells not passed yet whose average R is within `limit` of the bar (BIASED ones never count)."""
    n = 0
    for c in ((research or {}).get("cells") or {}).values():
        ev = (c.get("evidence") or {}).get("all") or {}
        if c.get("status") in ("BACKTESTING", "FAILED") and not c.get("bias") and ev.get("avg_r") is not None \
                and c.get("required_avg_r") is not None and 0 <= float(c["required_avg_r"]) - float(ev["avg_r"]) <= limit:
            n += 1
    return n


def weekly(rep, research, counts_hist, lab_cards, queue_text, lifecycle_lines, now, summary, page_url, dashboard_url,
           pages_base=None, repo_url=None):
    """The weekly report of the 7 days ending `now` (UTC datetime)."""
    days = [(now.date() - dt.timedelta(days=i)).isoformat() for i in range(7)]
    week = [x for x in counts_hist or [] if x.get("date") in days]
    counts = dict(backtests=sum(int(x.get("backtests") or 0) for x in week),
                  strategies=max((int(x.get("strategies") or 0) for x in week), default=None)) if week else {}
    by = {}
    for d in days:
        for i in lab_ideas(lab_cards, research, d, queue_text):
            by[i["source"]] = by.get(i["source"], 0) + 1
    wk = (rep or {}).get("weekly") or {}
    appr = ((research or {}).get("approval") or {}).get("eligible") or []
    dec = []
    for p in appr:
        cell = f"{p['strategy']} v{p['version']} {p['tf']}"
        dec.append(dict(cell=cell, pack_url=f"{repo_url}/blob/main/{p['pack']}" if repo_url and p.get("pack") else None,
                        chart_url=p.get("chart") or (btcharts.page_url(pages_base, p["strategy"], p["version"], p["tf"])
                                                     if pages_base else None)))
    a = now - dt.timedelta(days=6)
    return dict(week_no=now.isocalendar()[1], utc=now.strftime("%Y-%m-%d %H:%M"),
                days=f"{a.day}–{now.day} {now:%b}" if a.month == now.month else f"{a:%d %b} – {now:%d %b}",
                counts=counts, passed=passed_between(lifecycle_lines), close=close_cells(research), ideas_by_source=by,
                coins_tested=max((int(x.get("coins") or 0) for x in week), default=None) if week else None,
                decision=dec, card=wk.get("card"), summary=summary, page_url=page_url, dashboard_url=dashboard_url)
