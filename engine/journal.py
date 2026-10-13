"""
Journal sync (operator request 2026-10-06): the operator's own trades teach the agent.

The live watcher writes journal/my_trades.csv on the operator's PC: every alert it sent ("alert"), the Telegram
buttons ("took", "skipped", "closed by you"), the follow-up of a trade they took ("tp1", "stop", ...), the PLAN
result of EVERY alert ("plan" - the same rules as the backtests, followed silently, also for skipped alerts) and the
operator's real result in R ("your result", the /result command). With a GitHub token it uploads that file to the
branch `journal`; the hourly scan reads it back (journal_review.py) and this module turns it into facts:

  * which alerts the operator takes and skips, and how both groups did by the plan
  * the gap between the operator's real results and the plan for the same trades (fees, slippage, late entries,
    early exits): the part of the backtest the operator does not get
  * what closing early did, and the same per strategy

It only REPORTS (weekly email, Claude's fact sheet, reports/journal_review.md). It never changes a gate, a cost, a
strategy or an approval: a finding that the real costs look higher than the backtest's is a suggestion for the
operator. Findings need MIN_N trades in the group (a few trades say nothing).
Pure: no internet, no files.
"""
import csv
import datetime as dt
import io

MIN_N = 5                 # trades in a group before a finding is written
GAP_R = 0.15              # real result this much below the plan (per trade) -> "the backtest is too optimistic for you"
SKIP_R = 0.20             # skipped alerts this much better / worse than the taken ones -> a finding
COLS = ["time_utc", "alert_id", "event", "label", "coin", "side", "tf", "strategy", "version", "entry", "stop",
        "tp1", "tp2", "tp3", "price", "result_r"]
FOLLOW_FINAL = ("tp1", "tp2", "tp3", "stop", "time", "invalid")
TWIN_EVENT = "plan no5m"     # 2026-10-13: the watcher's silent twin of a 4H setup, entered without the 5m check


def _num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if v == v else None


def read(text):
    """The CSV text -> list of row dicts (unknown columns kept, bad lines skipped)."""
    if not text:
        return []
    return [r for r in csv.DictReader(io.StringIO(text)) if r.get("alert_id") and r.get("event")]


def trades(rows):
    """One dict per alert id, in the order first seen: what happened to it."""
    out = {}
    for r in rows:
        aid, ev = r["alert_id"], r["event"].strip()
        if ev.startswith(TWIN_EVENT):                 # the 5m side-by-side twins are not alerts (compare_5m)
            continue
        t = out.get(aid)
        if t is None:
            t = out[aid] = dict(id=aid, time=r.get("time_utc"), label=r.get("label"), coin=r.get("coin"),
                                side=r.get("side"), tf=r.get("tf"), strategy=r.get("strategy"),
                                version=r.get("version"), choice=None, closed_by_you=False, plan_r=None,
                                plan_state=None, follow_r=None, your_r=None)
        if ev in ("took", "skipped"):
            t["choice"] = ev
        elif ev == "closed by you":
            t["choice"], t["closed_by_you"] = "took", True
        elif ev == "plan":
            t["plan_state"], t["plan_r"] = "done", _num(r.get("result_r"))
        elif ev == "plan not filled":
            t["plan_state"] = "not filled"
        elif ev == "your result":
            t["your_r"] = _num(r.get("result_r"))
        elif ev in FOLLOW_FINAL and _num(r.get("result_r")) is not None:
            t["follow_r"] = _num(r.get("result_r"))
    for t in out.values():
        if t["plan_r"] is None and t["follow_r"] is not None:   # older journals: the follow-up's result is the plan's
            t["plan_r"] = t["follow_r"]
    return list(out.values())


def _stats(vals):
    vals = [v for v in vals if v is not None]
    return dict(n=len(vals), total_r=round(sum(vals), 3) if vals else 0.0,
                avg_r=round(sum(vals) / len(vals), 3) if vals else None,
                wins=sum(1 for v in vals if v > 0))


def _group(ts):
    took = [t for t in ts if t["choice"] == "took"]
    skipped = [t for t in ts if t["choice"] == "skipped"]
    silent = [t for t in ts if t["choice"] is None]
    both = [t for t in took if t["your_r"] is not None and t["plan_r"] is not None]
    early = [t for t in took if t["closed_by_you"] and t["plan_r"] is not None and t["your_r"] is not None]
    return dict(alerts=len(ts), took=len(took), skipped=len(skipped), no_answer=len(silent),
                plan_took=_stats([t["plan_r"] for t in took]), plan_skipped=_stats([t["plan_r"] for t in skipped]),
                plan_no_answer=_stats([t["plan_r"] for t in silent]), plan_all=_stats([t["plan_r"] for t in ts]),
                yours=_stats([t["your_r"] for t in took]),
                gap=_stats([t["your_r"] - t["plan_r"] for t in both]),
                early=dict(n=len(early), plan=_stats([t["plan_r"] for t in early]),
                           yours=_stats([t["your_r"] for t in early])),
                missing_result=sum(1 for t in took if t["your_r"] is None and t["plan_state"] != "not filled"))


def findings(g):
    """Plain sentences from one group's numbers (each needs MIN_N trades)."""
    out = []
    pt, ps = g["plan_took"], g["plan_skipped"]
    if pt["n"] >= MIN_N and ps["n"] >= MIN_N:
        diff = ps["avg_r"] - pt["avg_r"]
        if diff >= SKIP_R:
            out.append(f"The alerts you skipped did better than the ones you took ({ps['avg_r']:+.2f}R vs "
                       f"{pt['avg_r']:+.2f}R per trade by the plan, {ps['n']} vs {pt['n']} trades): your own filter is "
                       "costing you. Consider taking every alert of the strategies you follow.")
        elif diff <= -SKIP_R:
            out.append(f"Your skips helped: the alerts you skipped did worse ({ps['avg_r']:+.2f}R vs "
                       f"{pt['avg_r']:+.2f}R per trade by the plan). Note what made you skip them - it may become a "
                       "filter worth testing.")
    gp = g["gap"]
    if gp["n"] >= MIN_N:
        if gp["avg_r"] <= -GAP_R:
            out.append(f"Your real results are {gp['avg_r']:+.2f}R per trade below the plan ({gp['n']} trades). "
                       "That is fees, slippage, late entries or early exits the backtest does not see: enter close to "
                       "the alert price, use the limit entries, keep the stop and TPs on OKX. If it stays, the "
                       "backtest costs may be too low for you - a decision for you, the agent never changes them.")
        elif gp["avg_r"] >= GAP_R:
            out.append(f"Your real results are {gp['avg_r']:+.2f}R per trade above the plan ({gp['n']} trades) - "
                       "your execution adds to the strategy.")
        else:
            out.append(f"Your real results match the plan ({gp['avg_r']:+.2f}R per trade difference, {gp['n']} "
                       "trades): the backtest's numbers hold for you.")
    e = g["early"]
    if e["n"] >= MIN_N:
        d = e["yours"]["avg_r"] - e["plan"]["avg_r"]
        out.append(f"Closing early {'cost' if d < 0 else 'saved'} you {abs(d):.2f}R per trade ({e['n']} trades: you "
                   f"made {e['yours']['avg_r']:+.2f}R, the plan {e['plan']['avg_r']:+.2f}R).")
    if g["alerts"] >= 2 * MIN_N and g["no_answer"] > g["alerts"] / 2:
        out.append(f"{g['no_answer']} of {g['alerts']} alerts got no button: press ✅ Took it or ❌ Skipped under each "
                   "alert so the agent can learn from your choices.")
    if g["took"] >= MIN_N and g["missing_result"] > g["took"] / 2:
        out.append(f"{g['missing_result']} of {g['took']} trades you took have no real result: send /result 1.2 "
                   "(your result in R) after each trade so the agent can compare you with the plan.")
    return out


def review(rows, now_ms, days=30):
    """Facts for the last `days` days and for all time; per strategy for all time."""
    ts = trades(rows)
    cut = dt.datetime.fromtimestamp(now_ms / 1000 - days * 86400, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
    recent = [t for t in ts if (t["time"] or "") >= cut]
    by = {}
    for t in ts:
        by.setdefault(f"{t['strategy']} {t['tf']}", []).append(t)
    per = []
    for key, g in sorted(by.items()):
        s = _group(g)
        per.append(dict(cell=key, alerts=s["alerts"], took=s["took"], skipped=s["skipped"],
                        plan_avg_r=s["plan_all"]["avg_r"], plan_n=s["plan_all"]["n"],
                        your_avg_r=s["yours"]["avg_r"], your_n=s["yours"]["n"]))
    a, r = _group(ts), _group(recent)
    last = max((x.get("time_utc") or "" for x in rows), default="") or None
    tests = {}                                      # PR 3: the 🔵 TEST alerts' plan results (5m-confirmed, before fees)
    for t in ts:
        if t.get("label") == "TEST" and t.get("plan_r") is not None:
            x = tests.setdefault(t["strategy"], dict(n=0, sum=0.0))
            x["n"] += 1
            x["sum"] += float(t["plan_r"])
    tests = {k: dict(n=x["n"], avg_r=round(x["sum"] / x["n"], 3)) for k, x in sorted(tests.items())}
    return dict(last_entry_utc=last, days=days, all=a, recent=r, per_strategy=per, tests=tests,
                compare_5m=compare_5m(rows),
                findings=findings(a) or ([] if ts else ["No alert in your journal yet."]))


def compare_5m(rows):
    """The 4H side-by-side record (operator 2026-10-13: "test 4H without 5m check"), per timeframe:
      twin_all       every setup that waited for its 5m candle, entered at the signal close (no 5m check)
      twin_passed    ... of those, the setups the 5m check passed
      twin_rejected  ... the setups the 5m check rejected (no alert was sent for them)
      sent           the alerts actually sent (5m-confirmed entry), their plan result
    All plan results before fees, the same follow-up rules. {tf: {name: stats}}."""
    tw = {}
    for r in rows:
        ev = (r.get("event") or "").strip()
        if not ev.startswith(TWIN_EVENT):
            continue
        tf, v, x = r.get("tf") or "?", ev[len(TWIN_EVENT):].strip(), _num(r.get("result_r"))
        g = tw.setdefault(tf, dict(all=[], passed=[], rejected=[]))
        g["all"].append(x)
        if v in ("passed", "rejected"):
            g[v].append(x)
    sent = {}
    for t in trades(rows):
        if t["tf"] in tw and t["plan_r"] is not None:
            sent.setdefault(t["tf"], []).append(t["plan_r"])
    return {tf: dict(twin_all=_stats(g["all"]), twin_passed=_stats(g["passed"]), twin_rejected=_stats(g["rejected"]),
                     sent=_stats(sent.get(tf, []))) for tf, g in sorted(tw.items())}


def compare_lines(cmp):
    """Plain lines for the side-by-side record (empty when there is none yet)."""
    out = []

    def f(s):
        return f"{s['avg_r']:+.2f}R over {s['n']}" if s["n"] else "none yet"
    for tf, c in (cmp or {}).items():
        out.append(f"{tf}: every setup without the 5m check {f(c['twin_all'])} · the ones the 5m check passed "
                   f"{f(c['twin_passed'])} · the ones it rejected {f(c['twin_rejected'])} · alerts sent (5m entry) "
                   f"{f(c['sent'])} (plan results, before fees)")
    return out


DECISION_COLS = ["time_utc", "week", "action", "key", "coin"]


def read_decisions(text):
    """journal/decisions.csv (the operator's taps under the weekly review: promote / unpromote) -> [dict]."""
    if not text:
        return []
    return [dict(r) for r in csv.DictReader(io.StringIO(text))
            if r.get("action") in ("promote", "unpromote") and r.get("key") and r.get("coin")]


def lines(rv):
    """Markdown lines (reports/journal_review.md and Claude's fact sheet)."""
    if not rv:
        return ["- journal sync is not set up (no branch `journal` on GitHub)"]
    out = [f"Last journal entry: {rv.get('last_entry_utc') or 'none'} UTC"]
    for name, g in ((f"Last {rv['days']} days", rv["recent"]), ("All time", rv["all"])):
        def f(s):
            return f"{s['avg_r']:+.2f}R avg over {s['n']}" if s["n"] else "no result yet"
        out += [f"- {name}: {g['alerts']} alerts · took {g['took']} · skipped {g['skipped']} · no answer "
                f"{g['no_answer']}",
                f"  - plan result: took {f(g['plan_took'])} · skipped {f(g['plan_skipped'])} · no answer "
                f"{f(g['plan_no_answer'])}",
                f"  - your real results: {f(g['yours'])}" + (f" · gap to the plan {g['gap']['avg_r']:+.2f}R per "
                                                              f"trade ({g['gap']['n']})" if g["gap"]["n"] else "")]
    if rv.get("per_strategy"):
        out += ["- Per strategy (all time): cell · alerts · took · plan avg · your avg"]
        out += [f"  - {p['cell']} · {p['alerts']} · {p['took']} · "
                + (f"{p['plan_avg_r']:+.2f}R ({p['plan_n']})" if p["plan_n"] else "-") + " · "
                + (f"{p['your_avg_r']:+.2f}R ({p['your_n']})" if p["your_n"] else "-") for p in rv["per_strategy"]]
    cl = compare_lines(rv.get("compare_5m"))
    if cl:
        out += ["- With vs without the 5m check (the same setups):"] + [f"  - {x}" for x in cl]
    out += ["- Findings:"] + [f"  - {x}" for x in rv.get("findings") or ["none yet (each needs "
                                                                         f"{MIN_N}+ trades)"]]
    return out


def parse_result(arg):
    """'/result' argument -> (alert id or None, R). '1.2', '+1.2R', '-1', 'a1b2c3001 0.8'. ValueError when wrong."""
    parts = (arg or "").replace(",", ".").split()
    if not parts or len(parts) > 2:
        raise ValueError("expected: /result 1.2  or  /result <id> 1.2")
    aid = parts[0] if len(parts) == 2 else None
    txt = parts[-1].strip().rstrip("Rr")
    r = float(txt)
    if r != r or not -10 <= r <= 20:
        raise ValueError("a result in R between -10 and +20")
    return aid, r
