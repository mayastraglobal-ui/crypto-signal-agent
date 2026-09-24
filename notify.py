#!/usr/bin/env python3
"""
Email alerts for the Crypto Signal Agent (works without Claude).

  python notify.py          -> email NEW [ENTRY] signals (one email each, with a chart) and [EXIT] updates
                               of APPROVED positions from reports/latest.json (+ [WATCH] if email_watching)
  python notify.py daily    -> the daily report email, once per UTC day (first scan after 00:00 UTC = 08:00 Beijing)
  python notify.py test     -> send a test email (to check your setup)
  python notify.py failed   -> email a warning that the scan failed
  python notify.py research_failed -> email a warning that the daily research run failed
  python notify.py system   -> email [SYSTEM] once when data turns UNSAFE, and once when it recovers;
                               also once when a risk halt / strategy suspension starts or ends (Phase 11)

Needs 2 GitHub secrets: GMAIL_USER and GMAIL_APP_PASSWORD
(optional 3rd: ALERT_TO = a different address to receive alerts).
If the secrets are missing, it does nothing and never breaks the scan.
"""
import json
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(ROOT, "reports")
STATE = os.path.join(REPORTS, "notified.json")
SYSTEM_STATE = os.path.join(REPORTS, "system_alert_state.json")
RISK_SENT = os.path.join(REPORTS, "risk_alert_sent.json")
DAILY_SENT = os.path.join(REPORTS, "daily_sent.json")
REMINDERS_SENT = os.path.join(REPORTS, "reminders_sent.json")
FOOTER = "Research signal. Not financial advice."


def repo_link(path=""):
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    return f"{server}/{repo}{path}" if repo else ""


def load(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def save(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f)


def mail(rep, subject, lines, attachments=()):
    """Section 20: every email opens with the position book and ends with the research disclaimer."""
    book = rep.get("position_book_text") or []
    body = [*book, *([""] if book else []), *lines, "", "Full report: " + repo_link("/blob/main/reports/latest.md"),
            "", FOOTER]
    files = [os.path.join(ROOT, a) for a in attachments if a and os.path.exists(os.path.join(ROOT, a))]
    return send(subject, "\n".join(body), files)


def send(subject, body, attachments=()):
    user = os.environ.get("GMAIL_USER", "").strip()
    pw = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "").strip()
    to = os.environ.get("ALERT_TO", "").strip() or user
    if os.environ.get("DRY_RUN"):
        print(f"--- DRY RUN (not sent) ---\nTo: {to}\nSubject: {subject}\n"
              + "".join(f"Attachment: {os.path.basename(a)}\n" for a in attachments) + f"\n{body}")
        return True
    if not user or not pw:
        print("Email alerts not set up (no GMAIL_USER / GMAIL_APP_PASSWORD secret) - skipping.")
        return False
    msg = EmailMessage()
    msg["From"] = f"Crypto Signal Agent <{user}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    for a in attachments:
        with open(a, "rb") as f:
            msg.add_attachment(f.read(), maintype="image", subtype="png", filename=os.path.basename(a))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context(), timeout=30) as s:
        s.login(user, pw)
        s.send_message(msg)
    print(f"Email sent to {to}: {subject}")
    return True


def signal_id(p):
    return f"{p['coin']}-{p['timeframe']}-{p['strategy']}-{p['signal_time_utc']}"


def signals_email():
    """[ENTRY] (one email per new APPROVED signal, with its chart), [EXIT] (TP1 / close of an APPROVED position,
    and the 5m-confirmed entries) and, if email_watching is on, one [WATCH] digest. Each only once."""
    rep = load(os.path.join(REPORTS, "latest.json"), None)
    if rep is None:
        print("No report yet.")
        return
    seen = load(STATE, [])
    sent = 0
    for p in rep.get("signals", []):
        if signal_id(p) in seen or not p.get("email"):
            continue
        e = p["email"]
        if mail(rep, e["subject"], e["lines"], [e.get("chart")]):
            seen.append(signal_id(p))
            sent += 1
    for ev in rep.get("email_events", []):
        if ev["key"] in seen:
            continue
        if mail(rep, ev["subject"], ev["lines"], [ev.get("chart")]):
            seen.append(ev["key"])
            sent += 1
    if (rep.get("email_settings") or {}).get("email_watching"):
        items = [(f"watch|{w['coin']}|{w['tf']}|{w['strategy']}|{w['direction']}|{rep['generated_utc'][:13]}",
                  f"{w['coin']} {w['direction']} {w['tf']} {w['strategy']}: {w['state']}"
                  + (f" - missing `{w['missing']}`" if w.get("missing") else ""))
                 for w in rep.get("watching", []) if w["stage"] == "APPROVED" and w["state"] == "SETUP_FORMING"]
        items += [(f"watch|{a['id']}", f"{a['coin']} {a['direction']} {a['tf']} {a['strategy']}: AWAITING_5M "
                   f"({a['bars']}/6 bars)") for a in rep["position_book"]["awaiting"] if a["stage"] == "APPROVED"]
        new = [x for x in items if x[0] not in seen]
        if new and mail(rep, f"[WATCH] {len(new)} setup(s) forming - no entry yet",
                        ["Setups of APPROVED strategies that are NOT signals yet (email_watching is on):"]
                        + [f"- {t}" for _, t in new]):
            seen += [k for k, _ in new]
            sent += 1
    save(STATE, seen[-3000:])
    print(f"{sent} email(s) sent." if sent else "No new signals or position updates - no email.")


def daily_email():
    """The daily report (section 20, 08:00 Beijing): sent by the first scan of each UTC day (before 06:00 UTC,
    so a late-merged change never sends one in the middle of the day)."""
    rep = load(os.path.join(REPORTS, "latest.json"), None)
    d = (rep or {}).get("daily")
    if not d:
        print("No daily block in the report.")
        return
    if load(DAILY_SENT, {}).get("date") == d["date"] or int(d["utc"][11:13]) >= 6:
        print(f"Daily email already sent for {d['date']} or not the morning run - skipping.")
        return
    lines = rep.get("daily_lines") or []
    if mail(rep, rep.get("daily_subject") or f"[DAILY] {d['date']}", lines):
        save(DAILY_SENT, {"date": d["date"]})


def reminders_email(rep):
    sent = load(REMINDERS_SENT, [])
    for r in (rep or {}).get("reminders", []):
        if r["key"] not in sent and mail(rep, r["subject"], r["lines"]):
            sent.append(r["key"])
    save(REMINDERS_SENT, sent)


def system_email():
    """[SYSTEM] data-quality alert. Sends only when the state CHANGES to or from UNSAFE,
    so a long outage gives you 2 emails (start + recovery), not one every hour."""
    path = os.path.join(REPORTS, "data_quality.json")
    if not os.path.exists(path):
        print("No data-quality report yet.")
        return
    q = json.load(open(path))
    now = q["system_state"]
    before = json.load(open(SYSTEM_STATE))["state"] if os.path.exists(SYSTEM_STATE) else "GOOD"
    if (now == "UNSAFE") == (before == "UNSAFE"):
        print(f"Data state {now} (was {before}) - no system email.")
        return
    if now == "UNSAFE":
        bad = [f"- {coin}: " + "; ".join(f"{tf} {p}" for tf, r in c["timeframes"].items()
                                          for p in r["problems"])
               for coin, c in q["coins"].items() if c["state"] == "UNSAFE"]
        bad += [f"- {coin}: download failed" for coin in q.get("failed_downloads", [])]
        subject = "[SYSTEM] DATA_STALE / SIGNAL_DISABLED"
        body = [f"Checked {q['checked_utc']} UTC. Market data failed the safety checks.",
                f"Reason: {q['reason']}", "",
                "What this means: the agent sends NO signals until the data is good again.",
                "What you should do: nothing. Do not trade from this agent's old signals meanwhile.",
                "", "Problems found:"] + bad
    else:
        subject = "[SYSTEM] Data recovered - signals allowed again"
        body = [f"Checked {q['checked_utc']} UTC. Data state is now {now}: {q['reason']}.",
                "Normal signal checks are running again."]
    if mail(load(os.path.join(REPORTS, "latest.json"), {}), subject, body):
        json.dump({"state": now, "since_utc": q["checked_utc"]}, open(SYSTEM_STATE, "w"))


def risk_email():
    """[SYSTEM] risk alert (section 15): the scan lists what started or ended THIS run (daily / weekly loss halt,
    strategy suspension), so each change gives exactly one email."""
    path = os.path.join(REPORTS, "latest.json")
    if not os.path.exists(path):
        return
    rep = json.load(open(path))
    risk = rep.get("risk") or {}
    tr = risk.get("transitions") or []
    sent = json.load(open(RISK_SENT)).get("run") if os.path.exists(RISK_SENT) else None
    if not tr or sent == rep["generated_utc"]:
        print("No risk halt / suspension change - no risk email.")
        return
    starts = [t for t in tr if t["kind"] == "start"]
    subject = "[SYSTEM] Risk " + ("HALT: " if starts else "halt lifted: ") + ", ".join(t["what"] for t in tr[:3])
    body = [f"Risk engine, {rep['generated_utc']} UTC:"] + [f"- {t['text']}" for t in tr]
    if starts:
        body += ["", "What this means: no new live entries from the affected part until the halt ends.",
                 "Open positions keep their stops and targets. Do not add trades by hand to 'win it back'."]
    if mail(rep, subject, body):
        json.dump({"run": rep["generated_utc"]}, open(RISK_SENT, "w"))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "signals"
    try:
        if mode == "test":
            ok = send("Crypto Signal Agent - test email",
                      "It works! You will get an email here whenever a NEW trade signal appears,\n"
                      "and a warning if the hourly scan fails.\n\nReport: " + repo_link("/blob/main/reports/latest.md"))
            if not ok:
                sys.exit("Test failed: add the GMAIL_USER and GMAIL_APP_PASSWORD secrets first.")
        elif mode == "failed":
            run = os.environ.get("GITHUB_RUN_ID", "")
            send("[SYSTEM] Crypto Signal Agent - scan FAILED",
                 "The hourly scan failed. It will try again next hour.\n"
                 "If this keeps happening, open this link, take a screenshot and show it to Claude:\n"
                 + repo_link(f"/actions/runs/{run}"))
        elif mode == "research_failed":
            run = os.environ.get("GITHUB_RUN_ID", "")
            send("[SYSTEM] Crypto Signal Agent - daily research FAILED",
                 "The daily research run (long-history tests) failed. Strategy statuses stay as they were;\n"
                 "hourly scans and signals keep running. It will try again tomorrow.\n"
                 "If this keeps happening, open this link, take a screenshot and show it to Claude:\n"
                 + repo_link(f"/actions/runs/{run}"))
        elif mode == "system":
            system_email()
            risk_email()
            reminders_email(load(os.path.join(REPORTS, "latest.json"), None))
        elif mode == "daily":
            daily_email()
        else:
            signals_email()
    except smtplib.SMTPAuthenticationError:
        sys.exit("Gmail refused the login. Check GMAIL_USER and that GMAIL_APP_PASSWORD is a 16-letter APP password.")


if __name__ == "__main__":
    main()
