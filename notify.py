#!/usr/bin/env python3
"""
Email alerts for the Crypto Signal Agent (works without Claude).

  python notify.py          -> email any NEW signals from reports/latest.json
  python notify.py test     -> send a test email (to check your setup)
  python notify.py failed   -> email a warning that the scan failed
  python notify.py research_failed -> email a warning that the daily research run failed
  python notify.py system   -> email [SYSTEM] once when data turns UNSAFE, and once when it recovers

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


def repo_link(path=""):
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    return f"{server}/{repo}{path}" if repo else ""


def fmt(x):
    x = float(x)
    if x >= 1000:
        return f"{x:,.2f}"
    if x >= 1:
        return f"{x:,.4f}"
    return f"{x:.6g}"


def send(subject, body):
    user = os.environ.get("GMAIL_USER", "").strip()
    pw = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "").strip()
    to = os.environ.get("ALERT_TO", "").strip() or user
    if os.environ.get("DRY_RUN"):
        print(f"--- DRY RUN (not sent) ---\nTo: {to}\nSubject: {subject}\n\n{body}")
        return True
    if not user or not pw:
        print("Email alerts not set up (no GMAIL_USER / GMAIL_APP_PASSWORD secret) - skipping.")
        return False
    msg = EmailMessage()
    msg["From"] = f"Crypto Signal Agent <{user}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context(), timeout=30) as s:
        s.login(user, pw)
        s.send_message(msg)
    print(f"Email sent to {to}: {subject}")
    return True


def signal_id(p):
    return f"{p['coin']}-{p['timeframe']}-{p['strategy']}-{p['signal_time_utc']}"


def target_lines(p, split):
    """TP1..TPn lines. Spec v3 plans carry their own targets; older reports used TP1-TP3 + the config split."""
    tg = p.get("targets") or [dict(price=p[k], close_pct=int(x * 100))
                              for k, x in zip(("tp1", "tp2", "tp3"), split) if p.get(k) is not None]
    out = []
    for j, t in enumerate(tg, 1):
        if j == len(tg):
            what = "close the rest"
        else:
            what = f"close {t['close_pct']}%, " + ("move stop to entry" if j == 1 else "move stop to TP1")
        out.append(f"TP{j}        : {fmt(t['price'])}  -> {what}")
    return out


def signals_email():
    path = os.path.join(REPORTS, "latest.json")
    if not os.path.exists(path):
        print("No report yet.")
        return
    rep = json.load(open(path))
    seen = json.load(open(STATE)) if os.path.exists(STATE) else []
    new = [p for p in rep.get("signals", []) if signal_id(p) not in seen]
    if not new:
        print("No new signals - no email.")
        return
    split = rep["settings"]["tp_split"]
    bt = rep["market"]["btc_trend"]
    lines = [f"{len(new)} new signal(s) - {rep['generated_beijing']} Beijing time", "",
             f"BTC trend: daily {bt.get('1d', '?')}, 4H {bt.get('4h', '?')}", ""]
    for i, p in enumerate(new, 1):
        z = sorted(p["entry_zone"])
        lines += [
            f"=== {i}. {p['coin']} {p['direction']} ({p.get('market', '?')}) | {p['timeframe']} | "
            f"{p['strategy']} v{p.get('version', '1.0')} ===",
            f"Entry zone : {fmt(z[0])} - {fmt(z[1])}   (skip if price already left it)",
            f"Stop-loss  : {fmt(p['stop'])}  ({p['risk_pct_of_price']:.2f}% away)",
            *target_lines(p, split),
            f"Hold       : ~{p['expected_hold']} (max {p['max_hold']})",
            f"Size       : {p['position_qty']:.6g} {p['coin']} (~{p['position_usdt']:.0f} USDT, "
            f"risk {p['risk_usdt']:.2f} USDT)",
            f"Why        : {p['why']}",
            f"Backtest   : {p['backtest_coin']['trades']} trades on {p['coin']}, "
            f"{p['backtest_coin']['win_rate']*100:.0f}% win, {p['backtest_coin']['avg_r']:+.2f}R avg",
            ("WARNING    : against BTC trend" if p["context"]["against_btc_trend"] else ""),
            ""]
    lines += ["Full report: " + repo_link("/blob/main/reports/latest.md"), "",
              "Signals only - not financial advice. Check the news and your checklist before any trade."]
    subject = "[ENTRY] Crypto signal: " + ", ".join(f"{p['coin']} {p['direction']} {p['timeframe']}" for p in new[:3])
    if send(subject, "\n".join(l for l in lines if l is not None)):
        seen = (seen + [signal_id(p) for p in new])[-1000:]
        json.dump(seen, open(STATE, "w"))


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
    body += ["", "Details: " + repo_link("/blob/main/reports/latest.md"), "",
             "Research signal. Not financial advice."]
    if send(subject, "\n".join(body)):
        json.dump({"state": now, "since_utc": q["checked_utc"]}, open(SYSTEM_STATE, "w"))


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
        else:
            signals_email()
    except smtplib.SMTPAuthenticationError:
        sys.exit("Gmail refused the login. Check GMAIL_USER and that GMAIL_APP_PASSWORD is a 16-letter APP password.")


if __name__ == "__main__":
    main()
