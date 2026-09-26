#!/usr/bin/env python3
"""
Email alerts for the Crypto Signal Agent (works without Claude). Email redesign: every email is a short HTML card
with a plain-text copy (engine/emails.py); the long text lives on the dashboard.

  python notify.py          -> ENTRY SIGNAL emails (one per NEW signal of an APPROVED strategy, with its chart) and
                               TRADE UPDATE emails (TP1, close, cancelled) from reports/latest.json (+ WATCH if on)
  python notify.py daily    -> the fallbacks when Claude's report is missing: the 08:20 BRIEFING from engine numbers
                               only (from 01:00 UTC), and the DAILY REVIEW (from 18:00 UTC) - each once per day
  python notify.py weekly   -> the WEEKLY REPORT, once per week (Sunday, first scan from 04:00 UTC)
  python notify.py system   -> ACTION NEEDED once when market data turns UNSAFE, FIXED once when it recovers; a
                               RISK NOTICE when a risk halt / strategy suspension starts or ends; reminders
  python notify.py brain result.json -> the BRIEFING and DAILY REVIEW emails for Claude's reports the Brain guard
                               applied, and ACTION NEEDED when the guard refused a Claude task's push
  python notify.py failed | research_failed | brain_failed
                            -> ACTION NEEDED, but only when the previous run of the same workflow failed too
                               (one failure = the agent retries silently)
  python notify.py recovered scan|research|brain
                            -> FIXED, once, when a run works after 2+ failed runs in a row
  python notify.py test     -> one short email to check the setup
  python notify.py samples  -> one TEST email of each type (entry, TP1 update, stop hit, action, briefing, daily,
                               weekly) from today's engine files; trade numbers are EXAMPLES

Needs 2 GitHub secrets: GMAIL_USER and GMAIL_APP_PASSWORD (optional 3rd: ALERT_TO = another address).
If the secrets are missing, it does nothing and never breaks the scan. DRY_RUN=1 prints instead of sending
(EMAIL_PREVIEW_DIR=<folder> also writes each email's HTML there).
"""
import datetime as dt
import json
import os
import re
import smtplib
import ssl
import sys
from email.message import EmailMessage

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from engine import emails as em  # noqa: E402  (standard library only: works before `pip install`)
from engine import mailkit as mk  # noqa: E402

REPORTS = os.path.join(ROOT, "reports")
STATE = os.path.join(REPORTS, "notified.json")
SYSTEM_STATE = os.path.join(REPORTS, "system_alert_state.json")
RISK_SENT = os.path.join(REPORTS, "risk_alert_sent.json")
REMINDERS_SENT = os.path.join(REPORTS, "reminders_sent.json")
WEEKLY_SENT = os.path.join(REPORTS, "weekly_sent.json")
BRAIN_SENT = os.path.join(REPORTS, "brain_sent.json")            # Claude reports emailed (written by the Brain run)
FALLBACK_SENT = os.path.join(REPORTS, "fallback_sent.json")      # engine-only briefing / review emails (the scan)
CURRICULUM = os.path.join(ROOT, "memory", "beginner_course.md")  # the operator's lessons (not the reading plan)
CURRICULUM_SENT = os.path.join(REPORTS, "curriculum_sent.json")
LESSONS = os.path.join(REPORTS, "claude", "lessons")             # the beginner lesson pages (engine-written)
BRIEFING_FALLBACK_HOURS = range(1, 6)        # UTC: 09:00-13:59 Beijing, when the 08:20 briefing did not arrive
REVIEW_FALLBACK_HOURS = range(18, 24)        # UTC: 02:00-07:59 Beijing, when the 23:30 review did not arrive
WORKFLOWS = {"failed": "scan", "research_failed": "research", "brain_failed": "brain"}
TEST_NOTE = "TEST EMAIL - today's engine numbers; the trade numbers are EXAMPLES, not a signal."


# ---------------------------------------------------------------- files and links -----------------------------------
def repo_link(path=""):
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    return f"{server}/{repo}{path}" if repo else ""


def load(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path) as f:
            return json.load(f)
    except ValueError:
        return default


def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f)


def read_text(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def config():
    try:
        import yaml
        with open(os.path.join(ROOT, "config.yaml")) as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def pages_base():
    from engine import btcharts
    return btcharts.pages_base(config(), os.environ.get("GITHUB_REPOSITORY") or None)


def page_url(report_rel):
    """The dashboard page of a Claude report (build_dashboard.py publishes every report as a page)."""
    from engine import mdpage
    return pages_base().rstrip("/") + "/" + mdpage.page_path(report_rel)


def now_utc():
    return dt.datetime.now(dt.timezone.utc)


# ---------------------------------------------------------------- sending -------------------------------------------
def build_message(m, sender, to):
    """multipart/alternative (text + HTML); the chart image is shown inside the HTML (cid:chart)."""
    msg = EmailMessage()
    msg["From"] = f"Crypto Signal Agent <{sender}>"
    msg["To"] = to
    msg["Subject"] = m["subject"]
    msg.set_content(m["text"])
    msg.add_alternative(m["html"], subtype="html")
    chart = m.get("chart")
    if chart and os.path.exists(os.path.join(ROOT, chart)):
        with open(os.path.join(ROOT, chart), "rb") as f:
            msg.get_payload()[1].add_related(f.read(), maintype="image", subtype="png", cid="<chart>",
                                             filename=os.path.basename(chart))
    return msg


def send_mail(m):
    """Send one email dict (subject, text, html, chart). True = sent (or printed in a dry run)."""
    user = os.environ.get("GMAIL_USER", "").strip()
    pw = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "").strip()
    to = os.environ.get("ALERT_TO", "").strip() or user
    if os.environ.get("DRY_RUN"):
        chart = m.get("chart") if m.get("chart") and os.path.exists(os.path.join(ROOT, m["chart"])) else None
        print(f"--- DRY RUN (not sent) ---\nTo: {to}\nSubject: {m['subject']}\n"
              + (f"Inline image: {os.path.basename(chart)}\n" if chart else "") + f"\n{m['text']}")
        folder = os.environ.get("EMAIL_PREVIEW_DIR")
        if folder:
            os.makedirs(folder, exist_ok=True)
            name = re.sub(r"[^A-Za-z0-9]+", "_", m["subject"]).strip("_")[:60] or "email"
            with open(os.path.join(folder, f"{m.get('kind') or 'email'}_{name}.html"), "w", encoding="utf-8") as f:
                f.write(m["html"])
        return True
    if not user or not pw:
        print("Email alerts not set up (no GMAIL_USER / GMAIL_APP_PASSWORD secret) - skipping.")
        return False
    msg = build_message(m, user, to)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context(), timeout=30) as s:
        s.login(user, pw)
        s.send_message(msg)
    print(f"Email sent to {to}: {m['subject']}")
    return True


def legacy(subject, lines, chart=None):
    """An email block written by an older engine version (subject + lines): shown as plain lines in the new frame."""
    m = mk.render(mk.subject([subject]), [("header", ("ALERT", "")), ("box", dict(lines=[mk.plain(x) for x in lines
                                                                                       if str(x).strip()][:40])),
                                          ("footer", em.TRADE_FOOTER)])
    m["chart"] = chart
    return m


def as_mail(block):
    """The scan's email block (new: subject, text, html, chart - or an old one with lines)."""
    if block.get("html"):
        return dict(subject=block["subject"], text=block["text"], html=block["html"], chart=block.get("chart"),
                    kind=block.get("kind", ""))
    return legacy(block["subject"], block.get("lines") or [], block.get("chart"))


# ---------------------------------------------------------------- signals (ENTRY / TRADE UPDATE / WATCH) ------------
def signal_id(p):
    return f"{p['coin']}-{p['timeframe']}-{p['strategy']}-{p['signal_time_utc']}"


def signals_email():
    """ENTRY (one email per new APPROVED signal, with its chart), TRADE UPDATE (TP1, close, cancelled of an APPROVED
    position, and the 5m-confirmed entries) and, if email_watching is on, one WATCH notice. Each only once."""
    rep = load(os.path.join(REPORTS, "latest.json"), None)
    if rep is None:
        print("No report yet.")
        return
    seen = load(STATE, [])
    sent = 0
    for p in rep.get("signals", []):
        if signal_id(p) in seen or not p.get("email"):
            continue
        if send_mail(as_mail(p["email"])):
            seen.append(signal_id(p))
            sent += 1
    for ev in rep.get("email_events", []):
        if ev["key"] in seen:
            continue
        if send_mail(as_mail(ev)):
            seen.append(ev["key"])
            sent += 1
    if (rep.get("email_settings") or {}).get("email_watching"):
        items = [(f"watch|{w['coin']}|{w['tf']}|{w['strategy']}|{w['direction']}|{rep['generated_utc'][:13]}",
                  f"{w['coin']} {w['direction']} {w['tf']} {w['strategy']}: setup forming"
                  + (f" (missing {w['missing']})" if w.get("missing") else ""))
                 for w in rep.get("watching", []) if w["stage"] == "APPROVED" and w["state"] == "SETUP_FORMING"]
        items += [(f"watch|{a['id']}", f"{a['coin']} {a['direction']} {a['tf']} {a['strategy']}: waiting for the 5m "
                   f"bar ({a['bars']}/6)") for a in (rep.get("position_book") or {}).get("awaiting", [])
                  if a["stage"] == "APPROVED"]
        new = [x for x in items if x[0] not in seen]
        if new and send_mail(em.notice(dict(label="WATCH · LIVE", utc=rep.get("generated_utc"), tone="teal",
                                            title=f"{len(new)} setup{'s' if len(new) != 1 else ''} forming",
                                            sub="No entry yet - wait for the ENTRY SIGNAL email.",
                                            subject=["◇ Watch", f"{len(new)} setup{'s' if len(new) != 1 else ''} "
                                                                "forming", "no entry yet"],
                                            lines=[t for _, t in new]))):
            seen += [k for k, _ in new]
            sent += 1
    save(STATE, seen[-3000:])
    print(f"{sent} email(s) sent." if sent else "No new signals or position updates - no email.")


# ---------------------------------------------------------------- briefing / daily review / weekly ------------------
def summary_of(rel):
    from engine import summary as esum
    return esum.parse(read_text(os.path.join(ROOT, rel)) or "") if rel else None


def briefing_mail(rel, rep, slot, utc):
    """The BRIEFING email of one briefing file (rel = None: engine numbers only)."""
    from engine import mailfacts as mf
    base = pages_base()
    b = mf.briefing(rep, slot, utc, summary_of(rel), page_url(rel) if rel else None, base)
    return em.briefing(b)


def lab_cards():
    try:
        import yaml
        return [c for c in (yaml.safe_load(read_text(os.path.join(ROOT, "strategies_lab.yaml")) or "") or [])
                if isinstance(c, dict)]
    except Exception:
        return []


def beginner_lesson(day):
    """The next lesson of memory/beginner_course.md as a page (reports/claude/lessons/<day>.md), linked from the
    daily review email. Returns (the page's report path or None, the sent list to store)."""
    try:
        from engine import curriculum as cur
        lessons = cur.parse(read_text(CURRICULUM) or "")
        lesson, after = cur.next_lesson(lessons, load(CURRICULUM_SENT, []))
        if not lesson:
            return None, None
        n = next(i for i, x in enumerate(lessons, 1) if x["id"] == lesson["id"])
        rel = f"reports/claude/lessons/{day}.md"
        os.makedirs(LESSONS, exist_ok=True)
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
            f.write(f"# Beginner lesson {n} of {len(lessons)}: {lesson['title']}\n\n" + "\n".join(lesson["lines"]) + "\n")
        return rel, after
    except Exception as e:                       # a broken lesson file is not a reason to miss the email
        print(f"beginner lesson skipped: {e}")
        return None, None


def daily_mail(rel, rep, day, utc, lesson_rel=None):
    from engine import mailfacts as mf
    research = load(os.path.join(REPORTS, "research.json"), {})
    d = mf.daily(rep, research, load(os.path.join(REPORTS, "research_counts.json"), []), lab_cards(),
                 read_text(os.path.join(ROOT, "memory", "lessons.md")), read_text(os.path.join(ROOT, "memory",
                                                                                              "experiments.md")),
                 day, utc, summary_of(rel), page_url(rel) if rel else None, pages_base())
    d["lesson_url"] = page_url(lesson_rel) if lesson_rel else None
    return em.daily(d)


def send_daily_review(rel, rep, day, utc):
    """The DAILY REVIEW email (with Claude's block when rel is given) + the beginner lesson page."""
    lesson_rel, after = beginner_lesson(day)
    if send_mail(daily_mail(rel, rep, day, utc, lesson_rel)):
        if after is not None:
            save(CURRICULUM_SENT, after)
        return True
    return False


def daily_email():
    """Fallbacks (the scan, hourly): Claude's 08:20 briefing or 23:30 daily review did not arrive -> the same email
    from the engine's numbers only, once. The Brain run sends the real ones (brain_email)."""
    rep = load(os.path.join(REPORTS, "latest.json"), None)
    if not rep:
        print("No report yet.")
        return
    now = em.to_dt(rep.get("generated_utc")) or now_utc()
    done, brain = load(FALLBACK_SENT, {}), load(BRAIN_SENT, [])
    bj_day = now.astimezone(em.BJ).strftime("%Y-%m-%d")
    rel = f"reports/claude/briefings/{bj_day}-0820.md"
    if now.hour in BRIEFING_FALLBACK_HOURS and rel not in brain and done.get("briefing") != bj_day \
            and not os.path.exists(os.path.join(ROOT, rel)):
        if send_mail(briefing_mail(None, rep, "08:20", rep.get("generated_utc"))):
            done["briefing"] = bj_day
            save(FALLBACK_SENT, done)
    day = now.strftime("%Y-%m-%d")
    rel = f"reports/claude/daily/{day}.md"
    if now.hour in REVIEW_FALLBACK_HOURS and rel not in brain and done.get("review") != day \
            and not os.path.exists(os.path.join(ROOT, rel)):
        if send_daily_review(None, rep, day, rep.get("generated_utc")):
            done["review"] = day
            save(FALLBACK_SENT, done)
    print("Fallback emails checked.")


def weekly_mail(rep, now):
    from engine import mailfacts as mf
    rel = f"reports/claude/weekly/{now:%Y-%m-%d}.md"
    rel = rel if os.path.exists(os.path.join(ROOT, rel)) else None
    w = mf.weekly(rep, load(os.path.join(REPORTS, "research.json"), {}), load(os.path.join(REPORTS,
                                                                                         "research_counts.json"), []),
                  lab_cards(), read_text(os.path.join(ROOT, "memory", "experiments.md")),
                  ((rep or {}).get("weekly") or {}).get("lifecycle") or [], now, summary_of(rel),
                  page_url(rel) if rel else None, pages_base(), pages_base(), repo_link() or None)
    return em.weekly(w)


def weekly_email():
    """The WEEKLY REPORT (the scan builds its numbers on Sunday from 04:00 UTC); sent once per ISO week."""
    rep = load(os.path.join(REPORTS, "latest.json"), None)
    w = (rep or {}).get("weekly")
    if not w:
        print("Not the weekly report time (Sunday from 04:00 UTC) - skipping.")
        return
    if load(WEEKLY_SENT, {}).get("week") == w["week"]:
        print(f"Weekly email already sent for {w['week']} - skipping.")
        return
    if send_mail(weekly_mail(rep, em.to_dt(rep.get("generated_utc")) or now_utc())):
        save(WEEKLY_SENT, {"week": w["week"]})


def brain_email(result_path):
    """After the Brain guard (brain_guard.py): one BRIEFING email per new briefing it applied, one DAILY REVIEW email
    per new daily review (unless the scan's fallback already went out), and one ACTION NEEDED email per refused push.
    Each only once."""
    results = load(result_path, [])
    rep = load(os.path.join(REPORTS, "latest.json"), {})
    sent, done = load(BRAIN_SENT, []), load(FALLBACK_SENT, {})
    for r in results:
        if r["status"] == "rejected":
            key = f"rejected|{r['sha']}"
            if key not in sent and send_mail(em.action(dict(
                    what="guard", utc=r.get("when"), title="! Claude's work was refused",
                    subject=f"Claude task refused ({r['branch'].split('/')[-1]})",
                    sub=f"{r['branch']} · {r['sha'][:8]}",
                    meaning="The Brain guard refused all of it - nothing reached main. Signals and engine emails are "
                            "not affected. The next task run tries again.",
                    reasons=r["problems"], steps=["If it happens again tomorrow, send this email to Claude in a chat."],
                    steps_title="What to do", buttons=[("Open the Brain runs", repo_link("/actions/workflows/brain.yml"))]))):
                sent.append(key)
            continue
        for path in r["applied"]:
            if path in sent:
                continue
            m = re.match(r"^reports/claude/briefings/(\d{4}-\d{2}-\d{2})-(\d{2})(\d{2})\.md$", path)
            ok = None
            if m:
                ok = send_mail(briefing_mail(path, rep, f"{m.group(2)}:{m.group(3)}", rep.get("generated_utc")))
            m2 = re.match(r"^reports/claude/daily/(\d{4}-\d{2}-\d{2})\.md$", path)
            if m2:
                ok = True if done.get("review") == m2.group(1) else send_daily_review(
                    path, rep, m2.group(1), (r.get("when") or rep.get("generated_utc")))
            if ok:
                sent.append(path)
    save(BRAIN_SENT, sent[-500:])


# ---------------------------------------------------------------- system: data, risk, reminders ---------------------
def reminders_email(rep):
    sent = load(REMINDERS_SENT, [])
    for r in (rep or {}).get("reminders", []):
        if r["key"] not in sent and send_mail(em.notice(dict(label="REMINDER", utc=(rep or {}).get("generated_utc"),
                                                             title=mk.plain(r["subject"]).replace("[SYSTEM] ", ""),
                                                             subject=["! Reminder", mk.plain(r["subject"]).replace(
                                                                 "[SYSTEM] ", "")], lines=r["lines"]))):
            sent.append(r["key"])
    save(REMINDERS_SENT, sent)


def system_email():
    """Market data: ACTION NEEDED when the state CHANGES to UNSAFE, FIXED when it recovers - so a long outage gives
    2 emails, not one every hour."""
    path = os.path.join(REPORTS, "data_quality.json")
    if not os.path.exists(path):
        print("No data-quality report yet.")
        return
    q = load(path, {})
    now = q["system_state"]
    before = load(SYSTEM_STATE, {}).get("state", "GOOD")
    if (now == "UNSAFE") == (before == "UNSAFE"):
        print(f"Data state {now} (was {before}) - no system email.")
        return
    if now == "UNSAFE":
        bad = [f"{coin}: " + "; ".join(f"{tf} {p}" for tf, r in c["timeframes"].items() for p in r["problems"])
               for coin, c in q["coins"].items() if c["state"] == "UNSAFE"]
        bad += [f"{coin}: download failed" for coin in q.get("failed_downloads", [])]
        m = em.action(dict(what="data", utc=q["checked_utc"], title="! Market data failed the checks",
                           subject="market data unsafe - signals paused", sub=mk.plain(q["reason"])[:90],
                           meaning="The agent sends NO signals until the data is good again. Do not trade from this "
                                   "agent's old signals meanwhile.",
                           reasons=bad, steps=["Nothing - the agent checks again every hour."], steps_title="What to do",
                           buttons=[("Open the dashboard", pages_base())]))
    else:
        m = em.fixed(dict(what="data", name="market data", utc=q["checked_utc"],
                          detail=f"Data state is now {now}: {mk.plain(q['reason'])}"[:120], run_url=pages_base()))
    if send_mail(m):
        save(SYSTEM_STATE, {"state": now, "since_utc": q["checked_utc"]})


def risk_email():
    """RISK NOTICE (section 15): what started or ended THIS run (daily / weekly loss halt, strategy suspension),
    so each change gives exactly one email."""
    rep = load(os.path.join(REPORTS, "latest.json"), None)
    if rep is None:
        return
    tr = (rep.get("risk") or {}).get("transitions") or []
    if not tr or load(RISK_SENT, {}).get("run") == rep["generated_utc"]:
        print("No risk halt / suspension change - no risk email.")
        return
    starts = [t for t in tr if t["kind"] == "start"]
    what = ", ".join(t["what"] for t in tr[:3])
    m = em.notice(dict(label="RISK NOTICE · LIVE", utc=rep["generated_utc"], tone="amber" if starts else "win",
                       title=("! Risk halt: " if starts else "✓ Halt lifted: ") + what,
                       sub="No new live entries from the affected part until it ends." if starts else "",
                       subject=["! Risk halt" if starts else "✓ Risk halt lifted", what],
                       lines=[t["text"] for t in tr] + (["Open trades keep their stops and targets. Do not add trades "
                                                         "by hand to win it back."] if starts else [])))
    if send_mail(m):
        save(RISK_SENT, {"run": rep["generated_utc"]})


# ---------------------------------------------------------------- workflow failures: 2 in a row ---------------------
def gh_api(path):
    import urllib.request
    token = os.environ.get("GITHUB_TOKEN", "")
    api = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    req = urllib.request.Request(api + path, headers={"Accept": "application/vnd.github+json",
                                                      **({"Authorization": f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def earlier_runs():
    """The completed runs of THIS workflow before the current one, newest first: [(conclusion, started UTC, url)].
    None when GitHub cannot be asked (then the email is sent - a silent failure is worse than one extra email)."""
    repo, run = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_RUN_ID")
    if not repo or not run:
        return None
    try:
        cur = gh_api(f"/repos/{repo}/actions/runs/{run}")
        runs = gh_api(f"/repos/{repo}/actions/workflows/{cur['workflow_id']}/runs?status=completed&per_page=20"
                      f"&branch={cur.get('head_branch') or 'main'}").get("workflow_runs") or []
    except Exception as e:
        print(f"could not read the earlier runs: {e}")
        return None
    runs = [r for r in runs if str(r["id"]) != str(run) and r.get("conclusion") not in ("cancelled", "skipped")]
    runs.sort(key=lambda r: r.get("run_started_at") or r.get("created_at") or "", reverse=True)
    return [(r.get("conclusion"), (r.get("run_started_at") or r.get("created_at") or "").replace("T", " ")[:16],
             r.get("html_url")) for r in runs]


def failures_in_a_row(runs):
    n = 0
    for concl, _, _ in runs or []:
        if concl != "failure":
            break
        n += 1
    return n


def failed_email(mode):
    """ACTION NEEDED only when the previous run failed too (exactly the 2nd failure in a row: one email per problem)."""
    what = WORKFLOWS[mode]
    runs = earlier_runs()
    now = now_utc().strftime("%Y-%m-%d %H:%M")
    run_url = repo_link(f"/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}")
    if runs is not None and failures_in_a_row(runs) != 1:
        print(f"{what}: {'first failure - the agent retries silently' if not failures_in_a_row(runs) else 'already reported'}"
              " - no email.")
        return
    times = ([runs[0][1]] if runs else []) + [now]
    send_mail(em.action(dict(what=what, utc=now, times_utc=times, run_url=run_url)))


def recovered_email(what):
    """FIXED: this run worked after 2+ failed runs in a row (= an ACTION NEEDED email went out)."""
    runs = earlier_runs()
    if not runs or failures_in_a_row(runs) < 2:
        print(f"{what}: no failure streak before this run - no email.")
        return
    send_mail(em.fixed(dict(what=what, utc=now_utc().strftime("%Y-%m-%d %H:%M"),
                            detail=f"After {failures_in_a_row(runs)} failed runs in a row.",
                            run_url=repo_link(f"/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"))))


# ---------------------------------------------------------------- test emails --------------------------------------
def mark_test(m):
    """A TEST email: 'TEST · ' before the subject and a note at the top (text and HTML)."""
    m = dict(m, subject=f"TEST · {m['subject']}", text=f"{TEST_NOTE}\n\n{m['text']}")
    note = (f'<tr><td style="padding:12px 24px 0;"><div style="background:{mk.AMBER_BG};color:{mk.AMBER};'
            f'border-radius:8px;padding:8px 12px;font-size:12px;font-weight:700;">{mk.e(TEST_NOTE)}</div></td></tr>')
    i = m["html"].index("<tr>", m["html"].index("max-width:600px"))
    m["html"] = m["html"][:i] + note + m["html"][i:]
    return m


def example_trade(rep):
    """An EXAMPLE long on BTC around today's real price (the size uses the real account and risk settings)."""
    cfg = config()
    row = next((r for r in ((rep.get("daily") or {}).get("matrix") or []) if r["coin"] == "BTC"), None)
    px = float(row["price"]) if row and row.get("price") else 84000.0
    acct = float((cfg.get("account") or {}).get("size_usdt") or 1000)
    risk_pct = float((cfg.get("account") or {}).get("risk_per_trade_pct") or 0.5)
    entry, stop = round(px), round(px * (1 - 0.0077))
    R = entry - stop
    qty = acct * risk_pct / 100 / R
    return dict(entry=entry, stop=stop, tp=[entry + 2 * R, entry + 3 * R], zone=[entry - 0.15 * R, entry + 0.15 * R],
                qty=qty, usdt=qty * entry, risk_usdt=acct * risk_pct / 100, risk_pct=risk_pct, acct=acct, R=R)


def samples():
    """One TEST email of each type from today's engine files; trade numbers are EXAMPLES (and say so)."""
    rep = load(os.path.join(REPORTS, "latest.json"), {}) or {}
    now = now_utc()
    utc = now.strftime("%Y-%m-%d %H:%M")
    from engine import mailfacts as mf
    st = mf.status(rep)
    x = example_trade(rep)
    base = pages_base()
    from engine import btcharts
    entry = em.entry(dict(coin="BTC", quote="USDT", direction="LONG", market="spot", tf="1h", strategy="EXAMPLE",
                          version="1.0", utc=utc, valid_until_utc=(now + dt.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
                          entry=x["entry"], entry_zone=x["zone"], stop=x["stop"],
                          targets=[dict(price=x["tp"][0], r=2.0, close_pct=50), dict(price=x["tp"][1], r=3.0, close_pct=50)],
                          size=dict(qty=x["qty"], usdt=x["usdt"], risk_usdt=x["risk_usdt"], risk_pct=x["risk_pct"]),
                          account=x["acct"], data_state=(rep.get("data_quality") or {}).get("system_state"),
                          why=["Setup: EXAMPLE - a pullback to the 1H EMA20 inside an up-trend",
                               "Trend: EXAMPLE - the 4H trend agrees (up)"],
                          backtest=dict(trades=None, avg_r=None, streak95=None),
                          checks=dict(open=st["open"], max_open=st["max_open"],
                                      no_event=not (rep.get("risk") or {}).get("blackout_now"), risk_ok=True),
                          live_chart=em.tradingview("BTC", "USDT", "1h"),
                          backtest_chart=btcharts.page_url(base, "EXAMPLE", "1.0", "1h", "BTC")))
    upd = dict(coin="BTC", quote="USDT", direction="LONG", tf="1h", strategy="EXAMPLE", version="1.0", utc=utc,
               entry=x["entry"], targets=x["tp"], tp_split=[50, 50], tp1_r=2.0, price_now=x["tp"][0],
               stop_now=x["entry"], entered_utc=(now - dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
               live_chart=em.tradingview("BTC", "USDT", "1h"), **st)
    tp1 = em.update(dict(upd, kind="TP1_HIT"))
    sol = next((float(r["price"]) for r in ((rep.get("daily") or {}).get("matrix") or []) if r["coin"] == "SOL"
                and r.get("price")), 120.0)
    stop = em.update(dict(upd, coin="SOL", direction="SHORT", kind="CLOSED", close_reason="SL", result_r=-1.0,
                          entry=round(sol * 0.99, 2), price_now=sol, targets=[round(sol * 0.97, 2)],
                          live_chart=em.tradingview("SOL", "USDT", "1h", True)))
    act = em.action(dict(what="scan", utc=utc, run_url=repo_link("/actions/workflows/scan.yml"),
                         times_utc=[(now - dt.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"), utc]))
    brief_rel = newest_report("briefings")
    slot = f"{brief_rel[-7:-5]}:{brief_rel[-5:-3]}" if brief_rel else "08:20"
    brief = briefing_mail(brief_rel, rep, slot, utc)
    day = (now - dt.timedelta(hours=16)).strftime("%Y-%m-%d") if now.hour < 16 else now.strftime("%Y-%m-%d")
    drel = f"reports/claude/daily/{day}.md"
    daily = daily_mail(drel if os.path.exists(os.path.join(ROOT, drel)) else None, rep, day, utc)
    wrep = dict(rep, weekly=rep.get("weekly") or dict(week="test", lifecycle=[], card=None))
    weekly = weekly_mail(wrep, now)
    for m in (entry, tp1, stop, act, brief, daily, weekly):
        send_mail(mark_test(m))


def newest_report(folder):
    d = os.path.join(REPORTS, "claude", folder)
    names = sorted(x for x in os.listdir(d) if x.endswith(".md")) if os.path.isdir(d) else []
    return f"reports/claude/{folder}/{names[-1]}" if names else None


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "signals"
    try:
        if mode == "test":
            m = em.notice(dict(label="SETUP CHECK", utc=now_utc().strftime("%Y-%m-%d %H:%M"), tone="win",
                               title="✓ Email works", subject=["✓ Crypto Signal Agent", "test email"],
                               sub="You will get an email here for new LIVE signals and when something needs you.",
                               lines=[], buttons=[("Open the reports", repo_link("/blob/main/reports/latest.md"))]))
            if not send_mail(m):
                sys.exit("Test failed: add the GMAIL_USER and GMAIL_APP_PASSWORD secrets first.")
        elif mode in WORKFLOWS:
            failed_email(mode)
        elif mode == "recovered":
            recovered_email(sys.argv[2] if len(sys.argv) > 2 else "scan")
        elif mode == "system":
            system_email()
            risk_email()
            reminders_email(load(os.path.join(REPORTS, "latest.json"), None))
        elif mode == "daily":
            daily_email()
        elif mode == "weekly":
            weekly_email()
        elif mode == "brain":
            brain_email(sys.argv[2] if len(sys.argv) > 2 else "brain_result.json")
        elif mode == "samples":
            samples()
        else:
            signals_email()
    except smtplib.SMTPAuthenticationError:
        sys.exit("Gmail refused the login. Check GMAIL_USER and that GMAIL_APP_PASSWORD is a 16-letter APP password.")


if __name__ == "__main__":
    main()
