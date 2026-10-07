# Backup and restore (if GitHub is ever not available)

Written 2026-10-07 at the operator's request: "make a full backup file so that if GitHub is suspended I can build
the agent again with this data".

## What the backup file contains

`crypto-agent-backup-<date>.zip` holds:

| File | What it is |
|---|---|
| `crypto-signal-agent.bundle` | The **whole repository with its full history and every branch**: `main` (all code, `config.yaml`, `strategies.yaml`, `strategies_lab.yaml`, `memory/` = everything the agent learned, `reports/` incl. `signals_log.csv` = the paper record), `live-reports` (the large report files), `journal` (your own trades), `gh-pages` (the dashboard), `claude/brain-*` (Claude's task outputs) and the work branches |
| `main-snapshot.zip` | The newest `main` as plain files (no git needed) - for the Windows watcher, or just to read |
| `BACKUP_AND_RESTORE.md` | This guide |

It does **not** contain passwords and tokens (on purpose - they never go into the repository). Keep them yourself:

| Secret | Where it is used | Where to get it again |
|---|---|---|
| `GMAIL_USER`, `GMAIL_APP_PASSWORD`, `ALERT_TO` | the emails (GitHub → Settings → Secrets → Actions) | your Gmail address; a new app password at https://myaccount.google.com/apppasswords |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | the watcher (`telegram.env` on the PC) | @BotFather in Telegram (`/mybots` → your bot → API token); `windows\1_setup.bat` finds the chat id |
| `JOURNAL_GITHUB_TOKEN` | journal sync (`telegram.env`) | a new fine-grained token (`docs/WINDOWS_WATCHER.md`, Journal sync) |
| Claude's scheduled tasks | briefings, daily review, weekly research | their prompts are in the repository: `tasks/*.md` |

Not in the backup either, and not needed: `data/` (downloaded market candles - the agent downloads them again) and
the PC's `logs/`.

**Make a new backup now and then** (ask Claude: "make a backup file") and keep it in **two places outside GitHub**,
e.g. Google Drive and a USB stick / the lab PC.

## If GitHub has a problem

1. **Don't panic and don't delete anything.** Your copy is in the backup, the lab PC watcher keeps sending Telegram
   alerts with the last decisions it downloaded (it only stops getting new ones).
2. **Appeal first**: a suspended account or disabled Actions can be appealed at https://support.github.com
   (explain it is a personal research project; offer to reduce how often the workflows run). Don't open a new
   account to get around a suspension - that breaks GitHub's terms.
3. While it is sorted out, or if it can't be, use one of the ways below.

## Way 1: restore the repository somewhere else (another git host, or your account after an appeal)

Needs `git` (Windows: https://git-scm.com/download/win; Linux: `sudo apt install git`).

```
git clone crypto-signal-agent.bundle crypto-signal-agent
cd crypto-signal-agent
git branch -a                       # every branch is there (remotes/origin/...)
for b in live-reports journal gh-pages; do git branch $b origin/$b; done     # Linux / Git Bash
git remote set-url origin <the new empty repository's URL>
git push origin --all               # all branches with their full history
```

Then on the new place:
- add the three email secrets again (table above);
- the workflows in `.github/workflows/` are GitHub Actions files: on GitHub (an appeal that worked, or an
  organisation account) they run as before; another host needs its own scheduler (Way 2);
- tell the watcher the new address: in `telegram.env` add `CRYPTO_AGENT_REPO=<owner>/<repo>`, and change the
  download address in `windows\4_update.bat` (the line with `archive/refs/heads/main.zip`);
- re-create Claude's scheduled tasks pointing at the new repository (prompts in `tasks/*.md`).

## Way 2: run everything on your own always-on computer (no GitHub Actions)

The agent is plain Python; GitHub only gives it a free scheduler, storage and email sending. On the lab PC or a free
Oracle server (`docs/LIVE_WATCHER.md`, `deploy/install_oracle.sh`) the same jobs can run on a timer:

| Job | GitHub schedule now | Command (from `.github/workflows/`) |
|---|---|---|
| Research | daily 00:40 UTC | `python research.py`, `python memory_guard.py`, then save `reports memory strategies_lab.yaml` |
| Scan + emails | hourly at :07 | `python derivs.py`, `python scanner.py`, `python journal_review.py`, `python notify.py` (+ `daily`, `weekly`, `system`), `python feeds.py`, `python memory_guard.py` |
| Live watcher | always on | `python live_watcher.py` (already runs on the lab PC) |
| Claude's tasks | briefing / daily / weekly | Claude Code on the computer with the prompts in `tasks/*.md` |

Status: the **live watcher already works without GitHub** (it only stops receiving new research decisions). For the
research, scan and emails a small **local runner** is still to be built (a script + Windows Task Scheduler / Linux
cron entries that run the table above in order and commit the results to the local repository; `publish_live.py`
must then keep its branch locally). Ask Claude: "build the local runner from docs/BACKUP_AND_RESTORE.md".

## Check a backup file (optional)

```
git bundle verify crypto-signal-agent.bundle      # "The bundle records a complete history" = good
```
