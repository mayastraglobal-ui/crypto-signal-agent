#!/usr/bin/env python3
"""
Email alerts for the Crypto Signal Agent (works without Claude). Email format v2: every email is a short HTML card
with a plain-text copy (engine/emails.py) - a type pill first, an ACTION box always; the long text lives on the
dashboard.

  python notify.py          -> LIVE signal / update emails (APPROVED) and PAPER signal / update / complete emails
                               (PAPER_TRADING, at most 3 PAPER emails an hour) from reports/latest.json; every update
                               is a reply in its trade's email thread
  python notify.py daily    -> the fallbacks when Claude's report is missing: the 08:20 BRIEFING from engine numbers
                               only (from 01:00 UTC), and the DAILY review (from 18:00 UTC) - each once per day
  python notify.py weekly   -> the WEEKLY report, once per week (Sunday, first scan from 04:00 UTC)
  python notify.py system   -> ALERT once when market data turns unsafe (the system, or a SIGNAL coin), FIXED once when
                               it recovers; ALERT / FIXED when a risk halt starts / ends; reminders
  python notify.py brain result.json -> the BRIEFING (08:20; 14:20 / 21:20 only when something changed) and DAILY
                               emails for Claude's reports the Brain guard applied, and an ALERT when the guard refused
                               a Claude task's push (FIXED when that task's next push is applied)
  python notify.py watchdog -> (the Brain workflow, every 15 minutes) ALERT when no scan ran for 2 hours or a Claude
                               task (briefing, daily review, weekly research) is 60 minutes late; FIXED when it is back
  python notify.py failed | research_failed | brain_failed
                            -> ALERT, but only when the previous run of the same workflow failed too
                               (one failure = the agent retries silently)
  python notify.py tests_failed -> ALERT at the first red test run on main (tests are not flaky: one is enough)
  python notify.py recovered scan|research|brain|tests
                            -> FIXED, once, when a run works after the failures that sent the ALERT
  python notify.py test     -> one short email to check the setup
  python notify.py samples  -> one TEST email of each type (A LIVE signal, B TP1, B stop, C PAPER signal, D PAPER
                               update, E PAPER complete, F ALERT, G FIXED, H briefing, I changes briefing, J daily,
                               K weekly) from today's engine files; trade numbers are EXAMPLES

Needs 2 GitHub secrets: GMAIL_USER and GMAIL_APP_PASSWORD (optional 3rd: ALERT_TO = another address).
If the secrets are missing, it does nothing and never breaks the scan. DRY_RUN=1 prints instead of sending
(EMAIL_PREVIEW_DIR=<folder> also writes each email's HTML there).
"""
import datetime as dt
import glob
import hashlib
import json
import os
import re
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.utils import make_msgid

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from engine import emails as em  # noqa: E402  (standard library only: works before `pip install`)
from engine import mailkit as mk  # noqa: E402

REPORTS = os.path.join(ROOT, "reports")
MEMORY = os.path.join(ROOT, "memory")
STATE = os.path.join(REPORTS, "notified.json")
REMINDERS_SENT = os.path.join(REPORTS, "reminders_sent.json")
WEEKLY_SENT = os.path.join(REPORTS, "weekly_sent.json")
BRAIN_SENT = os.path.join(REPORTS, "brain_sent.json")            # Claude reports emailed (written by the Brain run)
FALLBACK_SENT = os.path.join(REPORTS, "fallback_sent.json")      # engine-only briefing / review emails (the scan)
CURRICULUM = os.path.join(MEMORY, "beginner_course.md")          # the operator's lessons (not the reading plan)
CURRICULUM_SENT = os.path.join(REPORTS, "curriculum_sent.json")
LESSONS = os.path.join(REPORTS, "claude", "lessons")             # the beginner lesson pages (engine-written)
# the state files are read from REPORTS when used (one file per workflow that writes it: two workflows never commit
# the same file, so no merge conflicts): alerts_<owner>.json, briefing_snapshot_<owner>.json, paper_sent.json (the
# scan's flood guard), paper_listed.json (the Brain), email_failed_<owner>.json, system_alert_state.json,
# risk_alert_sent.json
OWNER = os.environ.get("NOTIFY_OWNER", "scan")                  # which workflow runs this (brain.yml sets "brain")
OWNERS = ("scan", "brain")
BRIEFING_FALLBACK_HOURS = range(1, 6)        # UTC: 09:00-13:59 Beijing, when the 08:20 briefing did not arrive
REVIEW_FALLBACK_HOURS = range(18, 24)        # UTC: 02:00-07:59 Beijing, when the 23:30 review did not arrive
PAPER_PER_HOUR = 3                           # flood guard: at most 3 PAPER emails an hour; the rest in the next briefing
SCAN_STALE_H = 2                             # ALERT: no scan for 2 hours
TASK_LATE_MIN = 60                           # ALERT: a Claude task not delivered 60 minutes after its time
TASKS_DUE = [("briefing", "08:20", (0, 20)), ("briefing", "14:20", (6, 20)), ("briefing", "21:20", (13, 20)),
             ("daily", "23:30", (15, 30))]   # (task, Beijing slot, UTC hour / minute); the weekly: Sunday 02:00 UTC
WEEKLY_DUE = (2, 0)
WORKFLOWS = {"failed": "scan", "research_failed": "research", "brain_failed": "brain"}
THING = {"scan": "hourly scan", "research": "daily research run", "brain": "Brain workflow", "tests": "tests on main"}
TEST_NOTE = "TEST EMAIL - today's engine numbers; the trade numbers are EXAMPLES, not a signal."
DOMAIN = "crypto-signal-agent"


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


def rp(name):
    """A state file in REPORTS (looked up when used)."""
    return os.path.join(REPORTS, name)


def mem(name):
    return read_text(os.path.join(MEMORY, name))


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


def utc_text(t):
    return t.strftime("%Y-%m-%d %H:%M")


def latest():
    return load(os.path.join(REPORTS, "latest.json"), None)


def open_trades(rep):
    b = (rep or {}).get("position_book") or {}
    return f"{mk.val(b.get('heat'))} / {mk.val((b.get('limits') or {}).get('heat'))}"


# ---------------------------------------------------------------- sending -------------------------------------------
def thread_id(thread):
    """The Message-ID of a trade's entry email; every update of the trade replies to it (one trade = one thread)."""
    return f"<trade-{hashlib.sha1(str(thread).encode()).hexdigest()[:20]}@{DOMAIN}>"


def build_message(m, sender, to):
    """multipart/alternative (text + HTML); the chart image is shown inside the HTML (cid:chart). A trade email
    carries its thread: the entry email's Message-ID is the trade's id, updates reply to it."""
    msg = EmailMessage()
    msg["From"] = f"Crypto Signal Agent <{sender}>"
    msg["To"] = to
    msg["Subject"] = m["subject"]
    if m.get("thread"):
        tid = thread_id(m["thread"])
        if m.get("reply"):
            msg["Message-ID"] = make_msgid(domain=DOMAIN)
            msg["In-Reply-To"] = tid
            msg["References"] = tid
        else:
            msg["Message-ID"] = tid
    msg.set_content(m["text"])
    msg.add_alternative(m["html"], subtype="html")
    chart = m.get("chart")
    if chart and os.path.exists(os.path.join(ROOT, chart)):
        with open(os.path.join(ROOT, chart), "rb") as f:
            msg.get_payload()[1].add_related(f.read(), maintype="image", subtype="png", cid="<chart>",
                                             filename=os.path.basename(chart))
    return msg


def send_mail(m):
    """Send one email dict (subject, text, html, chart, thread). True = sent (or printed in a dry run).
    A send that fails (not the login) is written down; the next email that goes through reports it (ALERT)."""
    user = os.environ.get("GMAIL_USER", "").strip()
    pw = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "").strip()
    to = os.environ.get("ALERT_TO", "").strip() or user
    if os.environ.get("DRY_RUN"):
        chart = m.get("chart") if m.get("chart") and os.path.exists(os.path.join(ROOT, m["chart"])) else None
        print(f"--- DRY RUN (not sent) ---\nTo: {to}\nSubject: {m['subject']}\n"
              + (f"Thread: {thread_id(m['thread'])}{' (reply)' if m.get('reply') else ''}\n" if m.get("thread") else "")
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
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context(), timeout=30) as s:
            s.login(user, pw)
            s.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        raise
    except (smtplib.SMTPException, OSError) as e:
        lost = load(rp(f"email_failed_{OWNER}.json"), [])
        save(rp(f"email_failed_{OWNER}.json"), (lost + [dict(utc=utc_text(now_utc()), subject=m["subject"], error=str(e)[:120])])[-50:])
        print(f"Email NOT sent ({e}): {m['subject']}")
        return False
    print(f"Email sent to {to}: {m['subject']}")
    lost = load(rp(f"email_failed_{OWNER}.json"), [])
    if lost and not m.get("_email_alert"):
        save(rp(f"email_failed_{OWNER}.json"), [])
        send_mail(dict(em.alert(dict(
            title="Email sending failed", impact=f"{len(lost)} email{'s' if len(lost) != 1 else ''} lost",
            since_utc=lost[0]["utc"], utc=utc_text(now_utc()), auto="it works again now",
            nothing="Email works again. The lost emails are listed below – the dashboard has their numbers.",
            broke=f"Gmail refused or dropped {len(lost)} email(s): {lost[-1]['error']}",
            impact_long="Those emails never arrived. Signals, trades and reports were not affected.",
            tried="Each email is tried once; the next one worked.", open_trades=open_trades(latest()),
            meaning="Some emails were lost on the way. Check the dashboard for anything you missed.",
            details=[x["subject"] for x in lost], buttons=[("Dashboard", pages_base())])), _email_alert=True))
    return True


def as_mail(block):
    """The scan's email block (subject, text, html, chart, thread, reply, paper_mail), or None for a block written
    by an older engine version (no html: not sent)."""
    if not block.get("html"):
        return None
    return {k: block.get(k) for k in ("subject", "text", "html", "chart", "kind", "thread", "reply", "paper_mail",
                                      "key")}


# ---------------------------------------------------------------- the alert registry (F / G) ---------------------
def alert_open(owner, key, a):
    """ALERT once per problem: sent when `key` opens; the registry remembers when it started (for the FIXED email)."""
    reg = load(rp(f"alerts_{owner}.json"), {})
    if key in reg:
        return False
    a = dict(a, since_utc=a.get("since_utc") or a.get("utc"))
    if send_mail(em.alert(a)):
        reg[key] = dict(title=a["title"], since_utc=a["since_utc"], thing=a.get("thing"), cause=a.get("cause"),
                        file=a.get("file"))
        save(rp(f"alerts_{owner}.json"), reg)
        return True
    return False


def alert_close(owner, key, utc, missed=None, cause=None, buttons=()):
    """FIXED once, when an open problem is solved."""
    reg = load(rp(f"alerts_{owner}.json"), {})
    if key not in reg:
        return False
    x = reg[key]
    if send_mail(em.fixed(dict(thing=x.get("thing") or x["title"], title=x["title"], since_utc=x["since_utc"], utc=utc,
                               missed=missed, cause=cause or x.get("cause"), buttons=list(buttons)))):
        reg.pop(key)
        save(rp(f"alerts_{owner}.json"), reg)
        return True
    return False


# ---------------------------------------------------------------- signals (LIVE / PAPER) ----------------------------
def signal_id(p):
    return f"{p['coin']}-{p['timeframe']}-{p['strategy']}-{p['signal_time_utc']}"


def paper_allowed(now):
    """The flood guard: PAPER emails sent in the last hour < 3."""
    st = load(rp("paper_sent.json"), dict(sent=[], held=[]))
    hour_ago = utc_text(now - dt.timedelta(hours=1))
    return sum(t > hour_ago for t in st.get("sent") or []) < PAPER_PER_HOUR


def paper_note(now, m, sent):
    st = load(rp("paper_sent.json"), dict(sent=[], held=[]))
    if sent:
        st["sent"] = [t for t in st.get("sent") or [] if t > utc_text(now - dt.timedelta(days=1))] + [utc_text(now)]
    else:
        st["held"] = (st.get("held") or []) + [dict(key=m.get("key"), utc=utc_text(now), subject=m["subject"])]
        st["held"] = st["held"][-200:]
    save(rp("paper_sent.json"), st)


def signals_email():
    """LIVE entries (APPROVED, with the chart) and every trade email of latest.json's email_events: LIVE and PAPER
    updates, PAPER signals, PAPER complete. Each only once; PAPER emails at most 3 an hour (the rest are listed in
    the next briefing). PAPER complete is never held back."""
    rep = latest()
    if rep is None:
        print("No report yet.")
        return
    seen = load(STATE, [])
    now = em.to_dt(rep.get("generated_utc")) or now_utc()
    sent = 0
    items = [(signal_id(p), p["email"]) for p in rep.get("signals", []) if p.get("email")]
    items += [(ev["key"], ev) for ev in rep.get("email_events", [])]
    for key, block in items:
        if key in seen:
            continue
        m = as_mail(block)
        if m is None:
            seen.append(key)
            continue
        m["key"] = key
        guarded = m.get("paper_mail") and block.get("kind") != "PAPER_COMPLETE"
        if guarded and not paper_allowed(now):
            paper_note(now, m, False)
            seen.append(key)
            print(f"PAPER email held back (flood guard, listed in the next briefing): {m['subject']}")
            continue
        if send_mail(m):
            seen.append(key)
            sent += 1
            if guarded:
                paper_note(now, m, True)
    save(STATE, seen[-3000:])
    print(f"{sent} email(s) sent." if sent else "No new signals or position updates - no email.")


def held_paper(owner):
    """PAPER emails the flood guard held back and no briefing listed yet: [subject]; marks them listed."""
    st = load(rp("paper_sent.json"), dict(sent=[], held=[]))
    listed = set(load(rp("paper_listed.json"), []))
    new = [x for x in st.get("held") or [] if x.get("key") not in listed]
    if owner == "brain":
        save(rp("paper_listed.json"), (list(listed) + [x.get("key") for x in new])[-500:])
    return [x["subject"] for x in new]


# ---------------------------------------------------------------- briefing / daily review / weekly ------------------
def summary_of(rel):
    from engine import summary as esum
    return esum.parse(read_text(os.path.join(ROOT, rel)) or "") if rel else None


def lab_cards():
    try:
        import yaml
        return [c for c in (yaml.safe_load(read_text(os.path.join(ROOT, "strategies_lab.yaml")) or "") or [])
                if isinstance(c, dict)]
    except Exception:
        return []


def study():
    from engine import mailfacts as mf
    try:
        return mf.study_item(mem("curriculum.md"), mem("research_sources.md"))
    except Exception:
        return None


def research():
    return load(os.path.join(REPORTS, "research.json"), {})


def snapshot_now(rep):
    from engine import mailfacts as mf
    return mf.snapshot(rep, research(), mem("strategy_registry.csv"), lab_cards())


def last_snapshot():
    snaps = [s for s in (load(p, None) for p in (rp(f"briefing_snapshot_{o}.json") for o in OWNERS)) if s]
    return max(snaps, key=lambda s: s.get("saved_utc") or "") if snaps else None


def save_snapshot(owner, rep, slot):
    s = snapshot_now(rep)
    s.update(saved_utc=utc_text(now_utc()), slot=slot)
    save(rp(f"briefing_snapshot_{owner}.json"), s)


def briefing_mail(rel, rep, slot, utc, owner="scan", held=None):
    """The BRIEFING email of one briefing file (rel = None: engine numbers only). 08:20 = the full briefing; 14:20
    / 21:20 = what changed since the previous briefing, or None when nothing changed (then nothing is sent)."""
    from engine import mailfacts as mf
    held = held_paper(owner) if held is None else held
    if slot != "08:20":
        prev = last_snapshot()
        ch = mf.diff(prev, snapshot_now(rep)) + [("◆", f"PAPER signal not emailed (max {PAPER_PER_HOUR} an hour): {s}")
                                                  for s in held[:5]]
        if not ch:
            return None
        return em.changes(mf.changes(rep, slot, (prev or {}).get("slot") or "08:20", utc, ch,
                                     page_url(rel) if rel else None, research()))
    b = mf.briefing(rep, slot, utc, summary_of(rel), page_url(rel) if rel else None, pages_base(), research(),
                    mem("strategy_registry.csv"), load(os.path.join(REPORTS, "research_counts.json"), []), lab_cards(),
                    study())
    b["held"] = held                           # the flood guard's held-back PAPER emails
    return em.briefing(b)


def beginner_lesson(day):
    """The next lesson of memory/beginner_course.md as a page (reports/claude/lessons/<day>.md), linked from the
    daily email. Returns (the page's report path or None, its title, the sent list to store)."""
    try:
        from engine import curriculum as cur
        lessons = cur.parse(read_text(CURRICULUM) or "")
        lesson, after = cur.next_lesson(lessons, load(CURRICULUM_SENT, []))
        if not lesson:
            return None, None, None
        n = next(i for i, x in enumerate(lessons, 1) if x["id"] == lesson["id"])
        rel = f"reports/claude/lessons/{day}.md"
        os.makedirs(LESSONS, exist_ok=True)
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
            f.write(f"# Beginner lesson {n} of {len(lessons)}: {lesson['title']}\n\n" + "\n".join(lesson["lines"]) + "\n")
        return rel, lesson["title"], after
    except Exception as e:                       # a broken lesson file is not a reason to miss the email
        print(f"beginner lesson skipped: {e}")
        return None, None, None


def gh_api(path):
    import urllib.request
    token = os.environ.get("GITHUB_TOKEN", "")
    api = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    req = urllib.request.Request(api + path, headers={"Accept": "application/vnd.github+json",
                                                      **({"Authorization": f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def merged_prs():
    """[(merge date UTC, title)] of the last 30 closed pull requests that were merged ([] without GitHub access)."""
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo or not os.environ.get("GITHUB_TOKEN"):
        return []
    try:
        prs = gh_api(f"/repos/{repo}/pulls?state=closed&per_page=30&sort=updated&direction=desc")
    except Exception as e:
        print(f"could not read the merged pull requests: {e}")
        return []
    return [(p["merged_at"][:10], f"{p['title']} (#{p['number']})") for p in prs if p.get("merged_at")]


def tests_status():
    """(the SYSTEM HEALTH item, the weekly line) of the tests: how many there are (counted in tests/) and the
    newest run on main (GitHub, when it can be asked)."""
    n = sum(len(re.findall(r"^\s+def test_", read_text(p) or "", re.M)) for p in glob.glob(os.path.join(ROOT, "tests",
                                                                                                        "test_*.py")))
    concl = None
    repo = os.environ.get("GITHUB_REPOSITORY")
    if repo and os.environ.get("GITHUB_TOKEN"):
        try:
            runs = gh_api(f"/repos/{repo}/actions/workflows/tests.yml/runs?branch=main&status=completed&per_page=1")
            concl = ((runs.get("workflow_runs") or [{}])[0]).get("conclusion")
        except Exception as e:
            print(f"could not read the test runs: {e}")
    word = "✓ green on main" if concl == "success" else "! red on main" if concl == "failure" else "main: not checked"
    item = None if concl is None else (("Tests green", True) if concl == "success" else ("Tests red on main", False))
    return item, f"Tests: {n:,} · {word}"


def daily_mail(rel, rep, day, utc, lesson=None):
    from engine import mailfacts as mf
    item, _ = tests_status()
    d = mf.daily(rep, research(), load(os.path.join(REPORTS, "research_counts.json"), []), lab_cards(),
                 mem("lessons.md"), mem("experiments.md"), day, utc, summary_of(rel), page_url(rel) if rel else None,
                 pages_base(), mem("strategy_registry.csv"), mem("changelog.md"), merged_prs(),
                 load(os.path.join(REPORTS, "derivs_quality.json"), {}), item)
    d["lesson"] = lesson or {}
    return em.daily(d)


def send_daily_review(rel, rep, day, utc):
    """The DAILY email (with Claude's block when rel is given) + the beginner lesson page."""
    lesson_rel, title, after = beginner_lesson(day)
    if send_mail(daily_mail(rel, rep, day, utc, dict(title=title, url=page_url(lesson_rel)) if lesson_rel else None)):
        if after is not None:
            save(CURRICULUM_SENT, after)
        return True
    return False


def daily_email():
    """Fallbacks (the scan, hourly): Claude's 08:20 briefing or 23:30 daily review did not arrive -> the same email
    from the engine's numbers only, once. The Brain run sends the real ones (brain_email)."""
    rep = latest()
    if not rep:
        print("No report yet.")
        return
    now = em.to_dt(rep.get("generated_utc")) or now_utc()
    done, brain = load(FALLBACK_SENT, {}), load(BRAIN_SENT, [])
    bj_day = now.astimezone(em.BJ).strftime("%Y-%m-%d")
    rel = f"reports/claude/briefings/{bj_day}-0820.md"
    if now.hour in BRIEFING_FALLBACK_HOURS and rel not in brain and done.get("briefing") != bj_day \
            and not os.path.exists(os.path.join(ROOT, rel)):
        if send_mail(briefing_mail(None, rep, "08:20", rep.get("generated_utc"), "scan", held=[])):
            done["briefing"] = bj_day
            save(FALLBACK_SENT, done)
            save_snapshot("scan", rep, "08:20")
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
    _, tests = tests_status()
    w = mf.weekly(rep, research(), lab_cards(), mem("experiments.md"), now, summary_of(rel),
                  page_url(rel) if rel else None, pages_base(), pages_base(), repo_link() or None,
                  mem("strategy_registry.csv"), mem("changelog.md"), merged_prs(), mem("lessons.md"),
                  mem("research_sources.md"), load(os.path.join(REPORTS, "feeds.json"), {}), study(), tests)
    return em.weekly(w)


def weekly_email():
    """The WEEKLY report (the scan builds its numbers on Sunday from 04:00 UTC); sent once per ISO week."""
    rep = latest()
    w = (rep or {}).get("weekly")
    if not w:
        print("Not the weekly report time (Sunday from 04:00 UTC) - skipping.")
        return
    if load(WEEKLY_SENT, {}).get("week") == w["week"]:
        print(f"Weekly email already sent for {w['week']} - skipping.")
        return
    if send_mail(weekly_mail(rep, em.to_dt(rep.get("generated_utc")) or now_utc())):
        save(WEEKLY_SENT, {"week": w["week"]})


def task_of(branch):
    return {"briefing": "briefing", "daily": "daily review", "weekly": "weekly research"}.get(
        str(branch).split("brain-")[-1], str(branch).split("/")[-1])


def brain_email(result_path):
    """After the Brain guard (brain_guard.py): one BRIEFING email per new briefing it applied (08:20 in full; 14:20 /
    21:20 only when something changed), one DAILY email per new daily review (unless the scan's fallback already
    went out), one ALERT per refused push (FIXED when that task's next push is applied). Each only once."""
    results = load(result_path, [])
    rep = latest() or {}
    sent, done = load(BRAIN_SENT, []), load(FALLBACK_SENT, {})
    for r in results:
        task = task_of(r.get("branch", ""))
        if r["status"] == "rejected":
            alert_open("brain", f"refused|{task}", dict(
                title=f"Claude {task} refused", impact="nothing reached main", utc=r.get("when") or utc_text(now_utc()),
                thing=f"Claude {task}", cause="the Brain guard refused a push", auto="the next task run tries again",
                nothing="The guard kept everything out of main. The next task run tries again.",
                broke=f"The Brain guard refused {r.get('branch')} ({str(r.get('sha'))[:8]})",
                impact_long="Claude's work of this run is not on main and not emailed. Signals and engine emails are "
                            "not affected.",
                tried="Checked every file of the push against the rules; one or more broke them.",
                open_trades=open_trades(rep),
                meaning="Claude wrote something the rules do not allow, so none of it was used. That is the guard "
                        "working.",
                details=r.get("problems") or [], buttons=[("Open the Brain runs", repo_link("/actions/workflows/brain.yml"))]))
            continue
        if r["status"] == "applied":
            alert_close("brain", f"refused|{task}", r.get("when") or utc_text(now_utc()),
                        cause="the task's next push was applied")
        for path in r["applied"]:
            if path in sent:
                continue
            m = re.match(r"^reports/claude/briefings/(\d{4}-\d{2}-\d{2})-(\d{2})(\d{2})\.md$", path)
            ok = None
            if m:
                slot = f"{m.group(2)}:{m.group(3)}"
                mail = briefing_mail(path, rep, slot, rep.get("generated_utc"), "brain")
                ok = True if mail is None else send_mail(mail)
                if mail is None:
                    print(f"{slot} briefing: nothing changed since the last briefing - no email.")
                if ok:
                    save_snapshot("brain", rep, slot)
            m2 = re.match(r"^reports/claude/daily/(\d{4}-\d{2}-\d{2})\.md$", path)
            if m2:
                ok = True if done.get("review") == m2.group(1) else send_daily_review(
                    path, rep, m2.group(1), (r.get("when") or rep.get("generated_utc")))
            if ok:
                sent.append(path)
    save(BRAIN_SENT, sent[-500:])


# ---------------------------------------------------------------- watchdog (the Brain workflow) ---------------------
def due_times(now):
    """[(key, task, due UTC)] of the Claude tasks due in the last 24 hours (their time + 60 minutes has passed)."""
    out = []
    for back in (1, 0):
        d = (now - dt.timedelta(days=back)).date()
        for task, slot, (h, mi) in TASKS_DUE:
            t = dt.datetime(d.year, d.month, d.day, h, mi, tzinfo=dt.timezone.utc)
            bj_day = t.astimezone(em.BJ).strftime("%Y-%m-%d")
            rel = (f"reports/claude/briefings/{bj_day}-{slot.replace(':', '')}.md" if task == "briefing" else
                   f"reports/claude/daily/{t:%Y-%m-%d}.md")
            out.append((task, slot, t, rel))
        if d.weekday() == 6:
            t = dt.datetime(d.year, d.month, d.day, *WEEKLY_DUE, tzinfo=dt.timezone.utc)
            out.append(("weekly", "Sunday", t, f"reports/claude/weekly/{t:%Y-%m-%d}.md"))
    return [(task, slot, t, rel) for task, slot, t, rel in out if now - dt.timedelta(hours=24) < t
            and now >= t + dt.timedelta(minutes=TASK_LATE_MIN)]


def watchdog(now=None):
    """ALERT when no scan ran for 2 hours, or a Claude task (briefing, daily review, weekly research) was not delivered
    60 minutes after its time; FIXED when it is back. One ALERT per problem."""
    now = now or now_utc()
    rep = latest() or {}
    last = em.to_dt(rep.get("generated_utc"))
    utc = utc_text(now)
    if last is not None and now - last > dt.timedelta(hours=SCAN_STALE_H):
        alert_open("brain", "scan_stale", dict(
            title="No scan for 2 hours", impact="no signals, no trade updates", utc=utc, since_utc=utc_text(last),
            thing="hourly scan", cause="the scan did not run", auto="nothing the agent can restart",
            steps=["Open the scan runs (button below).", "Screenshot the newest run, or the empty list.",
                   "Send the screenshot to Claude."],
            broke=f"The newest scan report is from {em.bj(rep.get('generated_utc'), '%H:%M')} Beijing",
            impact_long="No new signals and no trade updates. Open trades keep the stops you set.",
            tried="The watchdog checks every 15 minutes.", open_trades=open_trades(rep),
            meaning="GitHub did not run the hourly scan, or it keeps failing before it saves. Set your stops by hand.",
            buttons=[("Open the scan runs", repo_link("/actions/workflows/scan.yml")), ("Dashboard", pages_base())]))
    elif last is not None:
        alert_close("brain", "scan_stale", utc, cause="the scan runs again")
    reg = load(rp("alerts_brain.json"), {})
    for task, slot, t, rel in due_times(now):
        key = f"missing|{task}"
        if os.path.exists(os.path.join(ROOT, rel)) or key in reg:
            continue
        name = {"briefing": f"{slot} briefing", "daily": "daily review", "weekly": "weekly research"}[task]
        alert_open("brain", key, dict(
            title=f"Claude {name} missing", impact="the engine sends its numbers", utc=utc, since_utc=utc_text(t),
            thing=f"Claude {task if task != 'daily' else 'daily review'}", cause="the task did not deliver",
            file=os.path.basename(rel),
            auto="the engine's own email goes out instead" if task != "weekly" else "the weekly numbers still go out",
            nothing="The engine's numbers still arrive. If it happens again tomorrow, open the Claude task.",
            broke=f"No {rel.split('/')[-1]} 60 minutes after {em.bj(utc_text(t), '%H:%M')} Beijing",
            impact_long="Claude's summary is missing from this email; signals and the engine's numbers are not affected.",
            tried="The Brain workflow looks for it every 15 minutes.", open_trades=open_trades(rep),
            meaning="The scheduled Claude task did not run, stopped early, or its push was refused.",
            buttons=[("Open the Brain runs", repo_link("/actions/workflows/brain.yml"))]))
    folder = {"missing|briefing": "briefings", "missing|daily": "daily", "missing|weekly": "weekly"}
    for key, sub in folder.items():
        x = load(rp("alerts_brain.json"), {}).get(key)
        if not x or not x.get("file"):
            continue
        names = [os.path.basename(p) for p in glob.glob(os.path.join(REPORTS, "claude", sub, "*.md"))]
        if any(n >= x["file"] for n in names):             # the missing report, or a newer one of the same task
            alert_close("brain", key, utc, cause="the task delivered again")


# ---------------------------------------------------------------- system: data, risk, reminders ---------------------
def reminders_email(rep):
    sent = load(REMINDERS_SENT, [])
    for r in (rep or {}).get("reminders", []):
        if r["key"] in sent:
            continue
        title = mk.plain(r["subject"]).replace("[SYSTEM] ", "")
        if send_mail(em.alert(dict(title=title, impact="action needed once", utc=(rep or {}).get("generated_utc"),
                                   steps=[mk.plain(x) for x in r["lines"]][-1:], broke=mk.plain(r["lines"][0]),
                                   impact_long=mk.plain(r["lines"][1]) if len(r["lines"]) > 1 else None,
                                   tried="A reminder, sent once.", open_trades=open_trades(rep),
                                   meaning=mk.plain(r["lines"][1]) if len(r["lines"]) > 1 else None))):
            sent.append(r["key"])
    save(REMINDERS_SENT, sent)


def unsafe_signal_coins(q, rep):
    signal = set(((rep or {}).get("universe") or {}).get("signal") or [])
    return sorted(c for c, x in (q.get("coins") or {}).items() if c in signal and x.get("state") == "UNSAFE")


def system_email():
    """Market data: ALERT when the system turns UNSAFE or a SIGNAL coin's data is UNSAFE (a candidate coin's bad data
    is only a line in the daily SYSTEM HEALTH), FIXED when it recovers - so a long outage gives 2 emails."""
    path = os.path.join(REPORTS, "data_quality.json")
    if not os.path.exists(path):
        print("No data-quality report yet.")
        return
    q = load(path, {})
    rep = latest() or {}
    coins = unsafe_signal_coins(q, rep)
    bad = q.get("system_state") == "UNSAFE" or bool(coins)
    if bad:
        detail = [f"{coin}: " + "; ".join(f"{tf} {p}" for tf, r in c["timeframes"].items() for p in r["problems"])
                  for coin, c in (q.get("coins") or {}).items() if c.get("state") == "UNSAFE"]
        detail += [f"{coin}: download failed" for coin in q.get("failed_downloads", [])]
        whole = q.get("system_state") == "UNSAFE"
        alert_open("scan", "data", dict(
            title="Market data unsafe", impact="signals paused" if whole else f"no signals on {', '.join(coins[:3])}",
            utc=q["checked_utc"], thing="market data", cause=mk.plain(q.get("reason"))[:60],
            auto="signals paused automatically" if whole else "those coins paused automatically",
            nothing="The agent paused new signals by itself." if whole else
                    f"The agent paused {', '.join(coins[:3])} by itself.",
            broke=mk.plain(q.get("reason")) if whole else f"Price data of {', '.join(coins)} failed the checks",
            impact_long="No new signals until the data is good again. Open trades keep their stops.",
            tried=f"Checked every candle, the second exchange ({q.get('second_exchange') or '–'}); it checks again "
                  "every hour.",
            open_trades=open_trades(rep),
            meaning="Prices from the exchange look wrong or old, so any signal could be wrong. Pausing is the safe choice.",
            details=detail, buttons=[("Dashboard", pages_base())]))
    else:
        reg = load(rp("alerts_scan.json"), {})
        if "data" in reg:
            missed = len(q.get("blocked_signals") or []) if isinstance(q.get("blocked_signals"), list) else None
            alert_close("scan", "data", q["checked_utc"], missed=missed, buttons=[("Dashboard", pages_base())])
    save(rp("system_alert_state.json"), {"state": q.get("system_state"), "since_utc": q.get("checked_utc")})


def risk_email():
    """ALERT when a risk halt / strategy suspension starts (this run), FIXED when it ends - one email per change."""
    rep = latest()
    if rep is None:
        return
    tr = (rep.get("risk") or {}).get("transitions") or []
    if not tr or load(rp("risk_alert_sent.json"), {}).get("run") == rep["generated_utc"]:
        print("No risk halt / suspension change - no risk email.")
        return
    for t in tr:
        key = f"halt|{t['what']}"
        if t["kind"] == "start":
            alert_open("scan", key, dict(
                title=f"Risk halt: {t['what']}", impact="no new live entries", utc=rep["generated_utc"],
                thing=f"risk halt ({t['what']})", cause="a loss limit was reached", auto="the halt ends by itself",
                nothing="The risk manager stopped new entries by itself. Do not add trades by hand to win it back.",
                broke=mk.plain(t["text"]), impact_long="No new live entries from the affected part until it ends.",
                tried="The loss limits of config.yaml (never loosened by the agent).", open_trades=open_trades(rep),
                meaning="The agent lost its daily or weekly loss limit, or a strategy broke its limits. Pausing protects "
                        "the account.", buttons=[("Dashboard", pages_base())]))
        else:
            alert_close("scan", key, rep["generated_utc"], cause=mk.plain(t["text"])[:60])
    save(rp("risk_alert_sent.json"), {"run": rep["generated_utc"]})


# ---------------------------------------------------------------- workflow failures ------------------------------
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


FAIL_WHAT = {
    "scan": ("no new signals or trade updates", "No new signals or trade updates are sent while it fails. Open trades "
                                                "keep the stops you set."),
    "research": ("strategy statuses frozen", "Strategy statuses stay as they were. Hourly scans and signals keep "
                                             "running."),
    "brain": ("Claude's reports not saved", "Claude's briefings and reviews are not saved or emailed. Signals from "
                                            "the engine are not affected."),
    "tests": ("a code change broke a test", "The last change to the code broke an automatic test. The running agent "
                                            "uses the same code, so a part of it may be wrong until it is fixed."),
}


def failure_alert(what, first_fail_utc, now, run_url):
    impact, meaning = FAIL_WHAT[what]
    title = f"{THING[what][0].upper() + THING[what][1:]} " + ("failing" if what == "tests" else "failed twice")
    return em.alert(dict(title=title, impact=impact, utc=now, since_utc=first_fail_utc,
                         auto="the agent retries every run" if what != "tests" else "the next push tests again",
                         steps=["Open the failed run (button below).", "Screenshot the step with the red ✕.",
                                "Send the screenshot to Claude."],
                         broke=f"The {THING[what]} ended with an error" + (" twice in a row" if what != "tests" else ""),
                         impact_long=impact[0].upper() + impact[1:] + ".", tried="Retried on the next run." if
                         what != "tests" else "The tests run on every push.", open_trades=open_trades(latest()),
                         meaning=meaning, buttons=[("Open the failed run", run_url), ("Dashboard", pages_base())]))


def failed_email(mode):
    """ALERT only when the previous run failed too (exactly the 2nd failure in a row: one email per problem); the
    tests on main: at the first red run (tests are not flaky)."""
    what = WORKFLOWS.get(mode, "tests")
    runs = earlier_runs()
    now = utc_text(now_utc())
    run_url = repo_link(f"/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}")
    streak = failures_in_a_row(runs) if runs is not None else None
    want = 0 if what == "tests" else 1
    if runs is not None and streak != want:
        print(f"{what}: {'first failure - the agent retries silently' if not streak else 'already reported'} - no email.")
        return
    first = runs[streak - 1][1] if runs and streak else now
    send_mail(failure_alert(what, first, now, run_url))


def recovered_email(what):
    """FIXED: this run worked after the failures that sent an ALERT (2+ in a row; tests: 1+)."""
    runs = earlier_runs()
    need = 1 if what == "tests" else 2
    if not runs or failures_in_a_row(runs) < need:
        print(f"{what}: no failure streak before this run - no email.")
        return
    n = failures_in_a_row(runs)
    send_mail(em.fixed(dict(thing=THING[what], title=f"{THING[what]} failing", since_utc=runs[n - 1][1],
                            utc=utc_text(now_utc()), cause=f"{n} failed runs in a row, then this run worked",
                            buttons=[("Open the run", repo_link(f"/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"))])))


# ---------------------------------------------------------------- test emails --------------------------------------
def mark_test(m):
    """A TEST email: 'TEST · ' before the subject and a note at the top (text and HTML)."""
    m = dict(m, subject=f"TEST · {m['subject']}", text=f"{TEST_NOTE}\n\n{m['text']}")
    note = (f'<tr><td style="padding:12px 24px 0;"><div style="background:{mk.AMBER_BG};color:{mk.AMBER};'
            f'border-radius:8px;padding:8px 12px;font-size:12px;font-weight:700;">{mk.e(TEST_NOTE)}</div></td></tr>')
    i = m["html"].index("<tr>", m["html"].index("max-width:600px"))
    m["html"] = m["html"][:i] + note + m["html"][i:]
    return m


def example_trade(rep, coin="BTC"):
    """An EXAMPLE long around today's real price of `coin` (the size uses the real account and risk settings)."""
    cfg = config()
    row = next((r for r in ((rep.get("daily") or {}).get("matrix") or []) if r["coin"] == coin), None)
    px = float(row["price"]) if row and row.get("price") else {"BTC": 84000.0, "ETH": 2700.0}.get(coin, 100.0)
    acct = float((cfg.get("account") or {}).get("size_usdt") or 1000)
    risk_pct = float((cfg.get("account") or {}).get("risk_per_trade_pct") or 0.5)
    entry, stop = mk_round(px), mk_round(px * (1 - 0.0077))
    R = entry - stop
    qty = acct * risk_pct / 100 / R
    return dict(entry=entry, stop=stop, tp=[entry + 2 * R, entry + 3 * R], zone=[entry - 0.15 * R, entry + 0.15 * R],
                qty=qty, usdt=qty * entry, risk_usdt=acct * risk_pct / 100, risk_pct=risk_pct, acct=acct, R=R)


def mk_round(x):
    return round(x) if x >= 1000 else round(x, 2)


def samples():
    """One TEST email of each type (A, B TP1, B stop, C, D, E, F, G, H, I, J, K) from today's engine files; trade
    numbers are EXAMPLES (marked so). Nothing is stored: no alert opens, no snapshot or flood-guard state changes."""
    from engine import btcharts
    from engine import mailfacts as mf
    rep = latest() or {}
    now = now_utc()
    utc = utc_text(now)
    ago = lambda h: utc_text(now - dt.timedelta(hours=h))  # noqa: E731
    st = mf.status(rep)
    base = pages_base()
    x = example_trade(rep)
    ex = "EXAMPLE"
    card = dict(coin="BTC", quote="USDT", direction="LONG", market="spot", tf="1h", strategy=ex, version="1.0", utc=utc,
                valid_until_utc=utc_text(now + dt.timedelta(hours=1)), entry=x["entry"], entry_zone=x["zone"],
                stop=x["stop"], targets=[dict(price=x["tp"][0], r=2.0, close_pct=50), dict(price=x["tp"][1], r=3.0,
                                                                                            close_pct=50)],
                size=dict(qty=x["qty"], usdt=x["usdt"], risk_usdt=x["risk_usdt"], risk_pct=x["risk_pct"]),
                account=x["acct"], data_state=(rep.get("data_quality") or {}).get("system_state"),
                why=["Setup: EXAMPLE - a pullback to the 1H EMA20 inside an up-trend",
                     "Trend: EXAMPLE - the 4H trend agrees (up)"],
                backtest=dict(trades=None, avg_r=None, streak95=None), live=dict(n=None, total_r=None),
                checks=dict(open=st["open"], max_open=st["max_open"],
                            no_event=not (rep.get("risk") or {}).get("blackout_now"), risk_ok=True),
                live_chart=em.tradingview("BTC", "USDT", "1h"),
                backtest_chart=btcharts.page_url(base, ex, "1.0", "1h", "BTC"))
    a = em.live_entry(card)
    upd = dict(coin="BTC", quote="USDT", direction="LONG", tf="1h", strategy=ex, version="1.0", utc=utc,
               entry=x["entry"], targets=x["tp"], tp_split=[50, 50], tp1_r=2.0, price_now=x["tp"][0],
               stop_now=x["entry"], signal_utc=ago(3.2), entered_utc=ago(3), entry_zone=x["zone"],
               risk_usdt=x["risk_usdt"], risk_pct=x["risk_pct"], live_chart=em.tradingview("BTC", "USDT", "1h"), **st)
    b1 = em.live_update(dict(upd, kind="TP1_HIT"))
    sol = next((float(r["price"]) for r in ((rep.get("daily") or {}).get("matrix") or []) if r["coin"] == "SOL"
                and r.get("price")), 120.0)
    b2 = em.live_update(dict(upd, coin="SOL", direction="SHORT", kind="CLOSED", close_reason="SL", result_r=-1.0,
                             entry=round(sol * 0.99, 2), exit_price=round(sol, 2), targets=[round(sol * 0.97, 2)],
                             tag="EXAMPLE: trend reversal - the 1H trend turned against the trade",
                             record=dict(n=None, won=None, total_r=None, streak=None, bt_streak=None),
                             live_chart=em.tradingview("SOL", "USDT", "1h", True)))
    y = example_trade(rep, "ETH")
    pcard = dict(card, coin="ETH", tf="4h", entry=y["entry"], entry_zone=y["zone"], stop=y["stop"],
                 targets=[dict(price=y["tp"][0], r=2.0, close_pct=50), dict(price=y["tp"][1], r=3.0, close_pct=50)],
                 stage="PAPER_TRADING", valid_until_utc=utc_text(now + dt.timedelta(hours=4)),
                 why=["Setup: EXAMPLE - a 4H close above the 20-candle high", "Trend: EXAMPLE - 1D and 4H up"],
                 paper=dict(number=4, needed=20, closed=3, won=2, total_r=2.2, avg_r=0.73, bt_avg_r=0.12, max_div=0.3),
                 live_chart=em.tradingview("ETH", "USDT", "4h"), journal_url=base)
    c = em.paper_signal(pcard)
    d = em.paper_update(dict(upd, coin="ETH", tf="4h", strategy=ex, entry=y["entry"], targets=y["tp"],
                             price_now=y["tp"][0], stop_now=y["entry"], kind="TP1_HIT", stage="PAPER_TRADING",
                             paper=pcard["paper"], live_chart=em.tradingview("ETH", "USDT", "4h"), journal_url=base))
    res = [2.0, 2.4, -1.0, 2.1, 2.0, -1.0, 2.5, 2.0, 2.2, -1.0, -1.0, 2.0, 2.3, -1.0, 2.0, 2.1, -1.0, 2.0, -1.0, 2.0]
    e = em.paper_complete(dict(strategy=ex, version="1.0", tf="4h", utc=utc, results=res, total_r=round(sum(res), 1),
                               passed=True, reasons=[], needed=20,
                               rows=[("Trades", "20", "–", True), ("Win rate", "65%", "–", None),
                                     ("Avg per trade", mk.signed(sum(res) / 20, "R", 2), "–", True),
                                     ("Worst losing streak", "2", "–", None), ("Max drawdown", "2.0R", "–", None)],
                               chips=[("All 20 closed and scored", True), ("No approval rule broken", True)],
                               pack_url=None, journal_url=base))
    q = load(os.path.join(REPORTS, "data_quality.json"), {})
    f = em.alert(dict(title="Market data unsafe", impact="signals paused", utc=utc, since_utc=utc,
                      auto="signals paused automatically", nothing="The agent paused new signals by itself.",
                      broke="EXAMPLE: the price feed is 2 hours old", impact_long="No new signals. Open trades keep "
                                                                                  "their stops.",
                      tried=f"EXAMPLE: refetched 3 times, cross-checked on {q.get('second_exchange') or 'OKX'}",
                      open_trades=open_trades(rep), meaning="Prices from the exchange are old, so any signal could be "
                                                            "wrong. Pausing is the safe choice.",
                      buttons=[("Dashboard", base)]))
    g = em.fixed(dict(thing="market data", title="Market data unsafe", since_utc=ago(1.1), utc=utc, missed=0,
                      cause="EXAMPLE: feed stale; fixed itself", buttons=[("Dashboard", base)]))
    brief_rel = newest_report("briefings", "0820")
    h = briefing_mail(brief_rel, rep, "08:20", utc, "scan", held=[])
    i = briefing_mail(newest_report("briefings"), rep, "14:20", utc, "scan", held=[]) or em.changes(
        mf.changes(rep, "14:20", "08:20", utc, [("◆", "No change since the last briefing - a real 14:20 email would "
                                                      "be skipped.")], None, research()))
    day = (now - dt.timedelta(hours=16)).strftime("%Y-%m-%d") if now.hour < 16 else now.strftime("%Y-%m-%d")
    drel = f"reports/claude/daily/{day}.md"
    j = daily_mail(drel if os.path.exists(os.path.join(ROOT, drel)) else None, rep, day, utc)
    wrep = dict(rep, weekly=rep.get("weekly") or dict(week="test", results=[], lifecycle=[], missed_moves=[], card=None))
    k = weekly_mail(wrep, now)
    for m in (a, b1, b2, c, d, e, f, g, h, i, j, k):
        send_mail(mark_test(m))


def newest_report(folder, slot=None):
    d = os.path.join(REPORTS, "claude", folder)
    names = sorted(x for x in os.listdir(d) if x.endswith(".md") and (slot is None or x.endswith(f"-{slot}.md"))) \
        if os.path.isdir(d) else []
    return f"reports/claude/{folder}/{names[-1]}" if names else None


def setup_check():
    blocks = [("header", ("FIXED", "SETUP CHECK", em.when(utc_text(now_utc())))),
              ("banner", dict(title="✓ Email works", tone="win",
                              sub="You get an email here for LIVE and PAPER signals and when something needs you.")),
              em.action_box("Do now", ["None. Nothing for you to do."], mk.GREY_LINE),
              ("buttons", [("Open the reports", repo_link("/blob/main/reports/latest.md"))]),
              ("footer", "Signals only – not financial advice.")]
    return mk.render(mk.subject(["✓ Crypto Signal Agent", "test email"]), blocks, (), "fixed")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "signals"
    try:
        if mode == "test":
            if not send_mail(setup_check()):
                sys.exit("Test failed: add the GMAIL_USER and GMAIL_APP_PASSWORD secrets first.")
        elif mode in WORKFLOWS or mode == "tests_failed":
            failed_email(mode)
        elif mode == "recovered":
            recovered_email(sys.argv[2] if len(sys.argv) > 2 else "scan")
        elif mode == "system":
            system_email()
            risk_email()
            reminders_email(latest())
        elif mode == "daily":
            daily_email()
        elif mode == "weekly":
            weekly_email()
        elif mode == "brain":
            brain_email(sys.argv[2] if len(sys.argv) > 2 else "brain_result.json")
        elif mode == "watchdog":
            watchdog()
        elif mode == "samples":
            samples()
        else:
            signals_email()
    except smtplib.SMTPAuthenticationError:
        sys.exit("Gmail refused the login. Check GMAIL_USER and that GMAIL_APP_PASSWORD is a 16-letter APP password.")


if __name__ == "__main__":
    main()
