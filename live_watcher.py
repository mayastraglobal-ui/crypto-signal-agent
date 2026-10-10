"""
Live watcher - instant Telegram alerts at every 5-minute candle close (operator request 2026-10-05).

The hourly GitHub scan checks the market once an hour, which is too late for scalping. This program runs all the
time on an always-on server (setup: docs/LIVE_WATCHER.md). Every 5 minutes, a few seconds after a candle closes,
it downloads the newest OKX USDT-perpetual candles and runs the SAME engine code as the hourly scan:

  1W / 1D / 4H / 1H regimes and timeframe permission  ->  the strategy rules on the timeframe that just closed
  ->  stop / targets (plan_trade)  ->  the 5m confirmation for cards with confirm_5m  ->  Telegram alert

Only strategy versions x timeframes whose research status allows it alert: APPROVED = LIVE alert, PAPER_TRADING =
PAPER alert (config.yaml -> live_watcher.stages). The hourly scan stays the official record: it logs the same
signals, emails them and keeps the risk book. This watcher never places orders and never needs exchange keys.

  python live_watcher.py                    run forever (the server service)
  python live_watcher.py --once             one pass now: print what would be sent (nothing is sent)
  python live_watcher.py --once --send      one pass now, and send the alerts
  python live_watcher.py --test-telegram    send one test message (checks the bot token and chat id)
  python live_watcher.py --status           which strategy versions x timeframes may alert right now
  python live_watcher.py --find-chat-id     your Telegram chat id (send the bot a message first)
  python live_watcher.py --setup-telegram   step-by-step Telegram setup (writes telegram.env)

TEST alerts (the Signal Center, Forward Test Program PR 2): program strategies positive on a coin in the 5-year backtest
(reports/program.json) also alert, labelled TEST, after a 5m confirmation, at most 10 a day (engine/signal_center.py).

  python live_watcher.py --replay 14        the Signal Center's safety check: the last 14 days with the TEST rules

While it runs, the bot answers the operator's commands (/status, /trades, /weather, /tests, /pause, /resume, /help)
and the buttons under each alert: "✅ Took it" makes the watcher follow that trade and say when TP1 / TP2, the stop or the time stop
is reached (engine/follow.py: the backtests' rules); every choice and result is written to journal/my_trades.csv.
Only the chat in TELEGRAM_CHAT_ID is answered.

Telegram settings come from the environment (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID) or from the file telegram.env
next to this script (python live_watcher.py --setup-telegram writes it). Never put them in the repository.
Without git (a Windows PC with the ZIP download, docs/WINDOWS_WATCHER.md), GitHub's newest decisions are downloaded
directly every hour (sync_files).
"""
import argparse
import base64
import csv
import datetime as dt
import json
import os
import subprocess
import sys
import time
import traceback
import warnings

import numpy as np
import pandas as pd
import requests
import socket
import yaml

import scanner as sc
from engine import confirm5m as c5m
from engine import data_quality as dq
from engine import flow_history as fh
from engine import follow as fl
from engine import journal as jr
from engine import lifecycle as lc
from engine import live as lv
from engine import regime_fit as rfit
from engine import scalp_playbook as spb
from engine import signal_center as scx
from engine import manage as mg
from engine import risk as rk
from engine import strategy_spec as sspec
from engine import timeframes as tfm

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)     # the scanner's feature tables
ROOT = sc.ROOT
STATE = os.path.join(ROOT, "reports", "live_watcher_state.json")     # local only (.gitignore)
SETTINGS_FILE = os.path.join(ROOT, "telegram.env")                  # local only (.gitignore): bot token + chat id
LOG_FILE = os.path.join(ROOT, "logs", "live_watcher.log")           # local only (.gitignore)
JOURNAL = os.path.join(ROOT, "journal", "my_trades.csv")            # local only (.gitignore): took / skipped / results
JOURNAL_COLS = ["time_utc", "alert_id", "event", "label", "coin", "side", "tf", "strategy", "version", "entry", "stop",
                "tp1", "tp2", "tp3", "price", "result_r"]
JOURNAL_BRANCH = "journal"           # journal sync: the GitHub branch that holds a copy of journal/my_trades.csv
DECISIONS = os.path.join(ROOT, "journal", "decisions.csv")   # PR 3: the operator's taps under the weekly review
SHADOW_DAYS = 14                     # a silent plan follow-up still open after 14 days is dropped
RESULT_HINT = ("\n📒 Send your real result: <b>/result 1.2</b> (in R after fees: -1 = full stop lost, 2 = twice your "
               "risk). It teaches the agent how the plan works for you.")
DATA_TFS = ["1w", "1d", "4h", "1h", "30m", "15m", "5m"]
REPO = os.environ.get("CRYPTO_AGENT_REPO", "mayastraglobal-ui/crypto-signal-agent")
RAW = "https://raw.githubusercontent.com/{repo}/{branch}/{path}"
# Without git (a Windows PC with the ZIP download): the files that carry GitHub's decisions, fetched every hour
SYNC_FILES = [("main", "config.yaml"), ("main", "events.yaml"), ("main", "strategies.yaml"),
              ("main", "strategies_lab.yaml"), ("main", "strategies_program.yaml"),
              ("main", "memory/strategy_registry.csv"),
              ("main", "reports/universe.json"), ("main", "reports/regime_fit.json"),
              ("main", "reports/market_weather.json"), ("main", "reports/program.json"),
              ("main", "reports/weekly_review.json"), ("main", "reports/promotions_state.json"),
              ("live-reports", "reports/derivs_hourly.csv.gz"), ("live-reports", "reports/funding.csv.gz")]
CODE_FILES = ["live_watcher.py", "scanner.py", "engine/live.py", "engine/follow.py", "engine/scalp_playbook.py",
              "engine/manage.py", "engine/flow_history.py", "engine/trend4h.py", "engine/regime_fit.py",
              "engine/journal.py", "engine/sessions.py", "engine/strategy_spec.py",
              "engine/lifecycle.py", "engine/signal_center.py", "engine/weather.py",
              "engine/weekly_review.py"]    # changed -> "run update.bat"


def trail_on_5m(m5, card, trail):
    """{trail_long, trail_short} for each closed 5m candle: the card timeframe's trailing ATR level of the newest card
    candle closed by then (no look-ahead). No card candles -> unknown (NaN: the stop just stays where it is)."""
    if card is None or not len(card):
        return dict(trail_long=np.full(len(m5), np.nan), trail_short=np.full(len(m5), np.nan))
    tl, ts = mg.trail_for(trail, card["high"].to_numpy(), card["low"].to_numpy(), card["close"].to_numpy())
    m = tfm.align_higher(m5, pd.DataFrame({"close_time": card["close_time"].to_numpy(), "tl": tl, "ts": ts}),
                         ["tl", "ts"])
    return dict(trail_long=m["tl"].to_numpy(dtype=float), trail_short=m["ts"].to_numpy(dtype=float))


def log(*a):
    line = " ".join([dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%S")] + [str(x) for x in a])
    print(line, flush=True)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 5_000_000:      # keep the log small
            os.replace(LOG_FILE, LOG_FILE + ".1")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d ") + line + "\n")
    except OSError:
        pass


def load_settings(path=SETTINGS_FILE):
    """KEY=VALUE lines (telegram.env) into the environment; a value already set in the environment wins."""
    try:
        with open(path, encoding="utf-8") as f:
            for raw in f:
                k, sep, v = raw.strip().partition("=")
                if sep and k and not k.startswith("#") and v.strip() and not os.environ.get(k.strip()):
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass


def _valid(path, data):
    """A downloaded file is only used when it looks right (never replace a good file with an error page)."""
    if not data:
        return False
    if path.endswith((".yaml", ".json")):
        try:
            (yaml.safe_load if path.endswith(".yaml") else json.loads)(data.decode("utf-8"))
        except (ValueError, yaml.YAMLError, UnicodeDecodeError):
            return False
    if path.endswith(".csv") and b"," not in data[:500]:
        return False
    if path.endswith(".gz") and data[:2] != b"\x1f\x8b":
        return False
    return True


def _fetch(get, url, path, deadline, tries=3, wait=(3, 8), sleep=None):
    """One file from GitHub, retried when the connection breaks or the download is incomplete (a slow VPN cuts
    downloads half way: ChunkedEncodingError / ConnectionError). Retries stop at the deadline (time.monotonic()), so a
    bad connection never holds up the 5-minute market check for long. Returns (data or None, problem or None)."""
    sleep = sleep or time.sleep
    problem = None
    for attempt in range(tries):
        try:
            r = get(url)
            data = r.content if r.status_code == 200 else None
            if r.status_code == 404:
                return None, f"{path}: not on GitHub (HTTP 404)"
            problem = None if _valid(path, data) else f"{path}: not downloaded (HTTP {r.status_code})"
        except requests.RequestException as e:
            data, problem = None, f"{path}: {e.__class__.__name__}"
        if problem is None:
            return data, None
        if attempt + 1 < tries:
            pause = wait[min(attempt, len(wait) - 1)]
            if time.monotonic() + pause >= deadline:
                break
            sleep(pause)
    return None, problem + (f" (after {attempt + 1} tries)" if attempt else "")


def sync_files(root=ROOT, repo=REPO, get=None, budget_s=120, sleep=None):
    """No git: download GitHub's newest decision files (statuses, coins, cards, settings, futures data).
    Returns (updated paths, problems). Each file is written only when it downloaded completely and looks valid;
    a broken download is tried again (up to 3 times, within budget_s seconds for all files together)."""
    get = get or (lambda url: requests.get(url, timeout=30))
    deadline = time.monotonic() + budget_s
    updated, problems = [], []
    for branch, path in SYNC_FILES:
        data, problem = _fetch(get, RAW.format(repo=repo, branch=branch, path=path), path, deadline, sleep=sleep)
        if problem:
            problems.append(problem)
            continue
        full = os.path.join(root, *path.split("/"))
        try:
            with open(full, "rb") as f:
                if f.read() == data:
                    continue
        except OSError:
            pass
        os.makedirs(os.path.dirname(full) or root, exist_ok=True)
        tmp = full + ".download"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, full)
        updated.append(path)
    return updated, problems


def code_outdated(root=ROOT, repo=REPO, get=None):
    """The watcher's own code files that differ from GitHub main ([] = up to date or unknown)."""
    get = get or (lambda url: requests.get(url, timeout=60))
    out = []
    for path in CODE_FILES:
        try:
            r = get(RAW.format(repo=repo, branch="main", path=path))
            if r.status_code != 200 or not r.content:
                continue
            with open(os.path.join(root, *path.split("/")), "rb") as f:
                if f.read().replace(b"\r\n", b"\n") != r.content.replace(b"\r\n", b"\n"):
                    out.append(path)
        except (requests.RequestException, OSError):
            continue
    return out


# ---------------------------------------------------------------- market data: OKX USDT perpetuals
class OKXSwap:
    """Candles of OKX USDT-margined perpetual swaps (what the operator trades). Volume = coin amount (volCcy)."""
    name = "OKX USDT perpetuals"
    BASE = "https://www.okx.com"

    def __init__(self):
        self.s = requests.Session()

    @staticmethod
    def inst(coin):
        return f"{coin}-USDT-SWAP"

    def _get(self, path, params):
        last = None
        for attempt in range(4):
            try:
                r = self.s.get(self.BASE + path, params=params, timeout=15)
                j = r.json() if r.status_code == 200 else {}
                if j.get("code") == "0":
                    return j["data"]
                last = f"HTTP {r.status_code} {r.text[:120]}"
            except (requests.RequestException, ValueError) as e:
                last = e.__class__.__name__
            time.sleep(1 + 2 * attempt)
        raise RuntimeError(f"OKX request failed: {last}")

    def candles(self, coin, tf, n, recent_only=False):
        """Newest n CLOSED candles (fewer when recent_only: one call to the fast endpoint, at most 300)."""
        bar = sc.OKX.BAR[tf]
        if recent_only:
            rows = self._get("/api/v5/market/candles", {"instId": self.inst(coin), "bar": bar, "limit": min(n, 300)})
        else:
            rows, after = [], None
            while len(rows) < n:
                p = {"instId": self.inst(coin), "bar": bar, "limit": 100}
                if after:
                    p["after"] = after
                data = self._get("/api/v5/market/history-candles", p)
                if not data:
                    break
                rows += data
                after = data[-1][0]
                time.sleep(0.12)
                if len(data) < 100:
                    break
        rows = [r for r in rows if len(r) < 9 or r[8] == "1"]                 # confirmed candles only
        if not rows:
            return pd.DataFrame(columns=["open_time", "open", "high", "low", "close", "volume", "quote_volume"])
        df = pd.DataFrame([[r[0], r[1], r[2], r[3], r[4], r[6], r[7] if len(r) > 7 else np.nan] for r in rows],
                          columns=["open_time", "open", "high", "low", "close", "volume", "quote_volume"])
        return sc._finish(df, tf)


class SyntheticSwap:
    """Offline test feed: the scanner's synthetic prices (no internet)."""
    name = "Synthetic (offline test)"

    def __init__(self, seed=7):
        self.f = sc.Synthetic(seed=seed)

    @staticmethod
    def inst(coin):
        return f"{coin}-USDT-SWAP"

    def candles(self, coin, tf, n, recent_only=False):
        return self.f.klines(coin + "USDT", tf, n)


# ---------------------------------------------------------------- Telegram
def tg_api(method, payload, token=None, timeout=15):
    """One Telegram Bot API call. Returns (ok, result or error text)."""
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        return False, "TELEGRAM_BOT_TOKEN not set"
    try:
        r = requests.post(f"https://api.telegram.org/bot{token}/{method}", json=payload, timeout=timeout)
        j = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        if r.status_code == 200 and j.get("ok"):
            return True, j.get("result")
        return False, f"HTTP {r.status_code}: {(j.get('description') or r.text)[:200]}"
    except (requests.RequestException, ValueError) as e:
        return False, e.__class__.__name__


def telegram_message(text, token=None, chat=None, timeout=15, buttons=None):
    """Send one message (with buttons = an inline keyboard). Returns (ok, error text, message id)."""
    chat = chat or os.environ.get("TELEGRAM_CHAT_ID")
    if not (token or os.environ.get("TELEGRAM_BOT_TOKEN")) or not chat:
        return False, "TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set", None
    p = dict(chat_id=chat, text=text[:4000], parse_mode="HTML", disable_web_page_preview=True)
    if buttons:
        p["reply_markup"] = buttons
    ok, res = tg_api("sendMessage", p, token, timeout)
    return (True, "", (res or {}).get("message_id")) if ok else (False, res, None)


def telegram(text, token=None, chat=None, timeout=15):
    """Send one message. Returns (ok, error text)."""
    return telegram_message(text, token, chat, timeout)[:2]


def find_chat_ids(token=None):
    """The chats that wrote to the bot recently (send the bot any message first): [(chat id, name)]."""
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set (put it in ~/.crypto-agent.env first)")
    r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=15).json()
    if not r.get("ok"):
        raise SystemExit(f"Telegram refused the token: {r.get('description')}")
    out = {}
    for u in r.get("result", []):
        c = (u.get("message") or u.get("channel_post") or {}).get("chat") or {}
        if c.get("id") is not None:
            out[c["id"]] = c.get("username") or c.get("title") or c.get("first_name") or ""
    return sorted(out.items())


# ---------------------------------------------------------------- the watcher
class JournalSync:
    """Journal sync (operator request 2026-10-06): a copy of journal/my_trades.csv on the GitHub branch `journal`, so the
    hourly scan can learn from the operator's own trades (journal_review.py). Needs JOURNAL_GITHUB_TOKEN in
    telegram.env: a fine-grained token for this repository only, permission Contents: read and write
    (python live_watcher.py --setup-github). Without it nothing is uploaded and the watcher works as before.
    Only this one file is ever written, on its own branch; main is never touched."""
    API = "https://api.github.com"

    def __init__(self, path=None, repo=REPO, http=None, remote="journal/my_trades.csv"):
        self.path, self.repo, self.remote = path, repo, remote
        self.http = http or (lambda method, url, **kw: requests.request(method, url, timeout=30, **kw))
        self.sent = None          # the bytes last uploaded
        self.sha = None           # the file's blob sha on the branch (needed to replace it)
        self.last = None          # (ms, ok, note)

    @staticmethod
    def token():
        return os.environ.get("JOURNAL_GITHUB_TOKEN", "").strip()

    def _call(self, method, path, **kw):
        h = {"Authorization": f"Bearer {self.token()}", "Accept": "application/vnd.github+json",
             "X-GitHub-Api-Version": "2022-11-28"}
        r = self.http(method, f"{self.API}/repos/{self.repo}{path}", headers=h, **kw)
        try:
            body = r.json()
        except ValueError:
            body = {}
        return r.status_code, body

    def _branch(self):
        """Make sure the branch exists: a branch of its own (no history from main) with a README."""
        code, _ = self._call("GET", f"/git/ref/heads/{JOURNAL_BRANCH}")
        if code == 200:
            return
        if code != 404:
            raise RuntimeError(f"GitHub answered HTTP {code} (check the token)")
        readme = ("# journal\n\nThe operator's own trade journal (journal/my_trades.csv), uploaded by the live "
                  "watcher's journal sync.\nThe hourly scan reads it (journal_review.py). Nothing else is kept here.\n")
        code, tree = self._call("POST", "/git/trees", json=dict(tree=[dict(path="README.md", mode="100644",
                                                                             type="blob", content=readme)]))
        if code != 201:
            raise RuntimeError(f"branch not created: HTTP {code} {tree.get('message', '')}")
        code, commit = self._call("POST", "/git/commits", json=dict(message="Journal branch", tree=tree["sha"],
                                                                     parents=[]))
        if code != 201:
            raise RuntimeError(f"branch not created: HTTP {code} {commit.get('message', '')}")
        code, ref = self._call("POST", "/git/refs", json=dict(ref=f"refs/heads/{JOURNAL_BRANCH}", sha=commit["sha"]))
        if code not in (201, 422):                       # 422: created meanwhile by another copy
            raise RuntimeError(f"branch not created: HTTP {code} {ref.get('message', '')}")

    def push(self, now_ms, force=False):
        """Upload the journal when it changed since the last upload. Returns (ok, note); never raises."""
        if not self.token():
            return False, "off"
        try:
            with open(self.path, "rb") as f:
                data = f.read()
        except OSError:
            data = ",".join(jr.COLS if self.remote.endswith("my_trades.csv") else jr.DECISION_COLS).encode() + b"\n" \
                if force else None
        if data is None or (data == self.sent and not force):
            return True, "unchanged"
        try:
            self._branch()
            for attempt in range(2):
                if self.sha is None:
                    code, cur = self._call("GET", f"/contents/{self.remote}?ref={JOURNAL_BRANCH}")
                    self.sha = cur.get("sha") if code == 200 else None
                body = dict(message=f"Journal {dt.datetime.fromtimestamp(now_ms / 1000, dt.timezone.utc):%Y-%m-%d %H:%M} UTC",
                            content=base64.b64encode(data).decode(), branch=JOURNAL_BRANCH)
                if self.sha:
                    body["sha"] = self.sha
                code, res = self._call("PUT", f"/contents/{self.remote}", json=body)
                if code in (200, 201):
                    self.sha, self.sent = (res.get("content") or {}).get("sha"), data
                    rows = max(0, data.count(b"\n") - 1)
                    self.last = (now_ms, True, f"{rows} rows")
                    return True, self.last[2]
                if code in (409, 422) and attempt == 0:   # the copy on GitHub changed: read its sha again
                    self.sha = None
                    continue
                raise RuntimeError(f"HTTP {code} {res.get('message', '')}".strip())
        except Exception as e:
            self.last = (now_ms, False, str(e)[:120])
            return False, self.last[2]
        return False, "not uploaded"

    def status(self, now_ms):
        """The /status line."""
        if not self.token():
            return "off (no JOURNAL_GITHUB_TOKEN - see docs/WINDOWS_WATCHER.md, Journal sync)"
        if not self.last:
            return "on, nothing uploaded yet"
        ms, ok, note = self.last
        return f"uploaded {lv.ago(ms, now_ms)} ({note})" if ok else f"⚠️ failing: {note}"


class Heartbeat(JournalSync):
    """"I am running" for GitHub (2026-10-10): every hour the watcher writes heartbeat.json to the branch
    `watcher-heartbeat` - ONE commit with no parent, replaced each time (no history builds up; main and the journal
    branch are never touched). The hourly scan reads it (journal_review.py -> reports/watcher_health.json) and emails
    an ALERT when it goes silent for 2 hours (the PC is off, asleep or offline), FIXED when it is back. Uses the
    journal-sync token (JOURNAL_GITHUB_TOKEN, Contents: read and write); without it nothing is sent."""
    BRANCH, FILE = "watcher-heartbeat", "heartbeat.json"

    def __init__(self, http=None, every_min=60):
        super().__init__(None, http=http)
        self.every_ms = int(every_min) * 60_000

    def push(self, now_ms, info=None, force=False):
        """Send the heartbeat when due (every_min after the last good one). Returns (ok, note); never raises."""
        if not self.token():
            return False, "off"
        if not force and self.last and self.last[1] and now_ms - self.last[0] < self.every_ms:
            return True, "not due"
        utc = dt.datetime.fromtimestamp(now_ms / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
        body = json.dumps(dict(utc=utc, **(info or {})), indent=1, default=str)
        try:
            code, tree = self._call("POST", "/git/trees", json=dict(tree=[dict(path=self.FILE, mode="100644",
                                                                               type="blob", content=body)]))
            if code != 201:
                raise RuntimeError(f"HTTP {code} {tree.get('message', '')}".strip())
            code, commit = self._call("POST", "/git/commits", json=dict(message=f"Heartbeat {utc} UTC",
                                                                         tree=tree["sha"], parents=[]))
            if code != 201:
                raise RuntimeError(f"HTTP {code} {commit.get('message', '')}".strip())
            code, res = self._call("PATCH", f"/git/refs/heads/{self.BRANCH}", json=dict(sha=commit["sha"], force=True))
            if code in (404, 422):                       # no branch yet: create it
                code, res = self._call("POST", "/git/refs", json=dict(ref=f"refs/heads/{self.BRANCH}",
                                                                      sha=commit["sha"]))
            if code not in (200, 201):
                raise RuntimeError(f"HTTP {code} {res.get('message', '')}".strip())
            self.last = (now_ms, True, "sent")
            return True, "sent"
        except Exception as e:
            self.last = (now_ms, False, str(e)[:120])
            return False, self.last[2]

    def status(self, now_ms):
        if not self.token():
            return None
        if not self.last:
            return "on, first one within 5 minutes"
        ms, ok, note = self.last
        return f"sent {lv.ago(ms, now_ms)} - GitHub emails you if it stops" if ok else f"⚠️ failing: {note}"


class Watcher:
    def __init__(self, feed, send=True, git=True, now_fn=None, also=()):
        self.feed, self.send, self.git, self.also = feed, send, git, list(also or ())
        self.now_fn = now_fn or (lambda: int(time.time() * 1000))
        self.frames = {}          # (coin, tf) -> candles (raw, newest last)
        self.pending = []         # 5m confirmations waiting for their bars
        self.state = self._load_state()
        self.fails = 0
        self.started_ms = self.now_fn()
        self.last_tick = None     # (ms, ok, note) of the newest market check, for /status
        self.last_refresh = None  # (ms, note) of the newest GitHub refresh
        self.code_old = []        # watcher code files that differ from GitHub main
        self._poll_err = None
        self.jsync = JournalSync(JOURNAL)
        self.dsync = JournalSync(DECISIONS, remote="journal/decisions.csv")     # PR 3: promote taps
        self.hb = Heartbeat()                                                 # "I am running" for GitHub
        self.reload()

    # ---- configuration, strategy statuses, coins ----
    def reload(self):
        self.cfg = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
        self.S = lv.settings(self.cfg.get("live_watcher"))
        for st in self.also:                                        # --also: a code test only, labelled CHECK
            self.S["stages"].setdefault(st, "CHECK")
        self.SC = scx.settings(self.cfg.get("signal_center"))
        self.dq_cfg = dq.settings(self.cfg.get("data_quality"))
        self.S5 = c5m.settings(self.cfg.get("confirm_5m"))
        try:
            self.RK = rk.settings(self.cfg.get("risk"), (self.cfg.get("events") or [])
                                  + rk.load_calendar(os.path.join(ROOT, rk.CALENDAR_FILE)))
            self.calendar_problem = None
        except ValueError as e:
            self.RK, self.calendar_problem = rk.settings(self.cfg.get("risk"), []), str(e)
        cards, _, _, _ = sc.load_cards()
        reg = (lc.registry_from_frame(pd.read_csv(sc.REGISTRY, dtype={"version": str}))
               if os.path.exists(sc.REGISTRY) else lc.empty_registry())
        self.watch = []           # (card, tf, label)
        for s in cards:
            for tf in s["timeframes"]:
                st = (reg["cells"].get(f"{sspec.key(s)}|{tf}") or {}).get("status")
                label = lv.alert_label(st, s.get("lab"), self.S)
                if label:
                    self.watch.append((s, tf, label))
        # the Signal Center (Forward Test Program PR 2): 🔵 TEST alerts for program cells positive on a coin in the
        # 5-year backtest (reports/program.json) - only where the cell does not already alert as PAPER / LIVE
        self.program = self._json("reports/program.json")
        self.weather = self._json("reports/market_weather.json")
        self.promoted = (self._json("reports/promotions_state.json") or {}).get("active") or {}   # PR 3
        self.tests = scx.test_list(self.program, reg["cells"], self.SC, self.promoted)
        have = {(sspec.key(s), tf) for s, tf, _ in self.watch}
        for s in cards:
            for tf in s["timeframes"]:
                if f"{sspec.key(s)}|{tf}" in self.tests and (sspec.key(s), tf) not in have:
                    self.watch.append((s, tf, "TEST"))
        self.cards = {sspec.key(s): s for s in cards}
        try:
            u = json.load(open(os.path.join(ROOT, "reports", "universe.json")))
            self.coins = list(u.get("signal") or [])
        except (OSError, ValueError):
            self.coins = ["BTC", "ETH"]
        if "BTC" not in self.coins:
            self.extra = ["BTC"]                                    # btc_ret building block
        else:
            self.extra = []
        try:                                                        # roadmap step 5: strategies by market type
            self.regime_fit = json.load(open(os.path.join(ROOT, "reports", "regime_fit.json")))
        except (OSError, ValueError):
            self.regime_fit = {}
        self.reloaded_ms = self.now_fn()
        log(f"watching {len(self.watch)} strategy timeframe(s) on {', '.join(self.coins)}: "
            + (", ".join(f"{s['id']} {tf} ({lab})" for s, tf, lab in self.watch) or "none yet (nothing is APPROVED "
               "or PAPER_TRADING - the watcher stays quiet until the daily research run promotes a strategy)"))

    @staticmethod
    def _json(rel):
        try:
            with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    def refresh_repo(self):
        """GitHub's newest decisions (statuses, cards, coins, settings) + the newest futures-data files:
        git pull in a git checkout (a server), else a direct download of those files (a PC with the ZIP)."""
        if not self.git:
            return
        if os.path.isdir(os.path.join(ROOT, ".git")):
            note = "git pull"
            for cmd in (["git", "pull", "--ff-only", "-q"], [sys.executable, "publish_live.py", "--refresh"]):
                try:
                    subprocess.run(cmd, cwd=ROOT, timeout=180, capture_output=True, check=False)
                except (OSError, subprocess.TimeoutExpired) as e:
                    log(f"refresh: {' '.join(cmd[:2])} failed: {e}")
                    note = f"{' '.join(cmd[:2])} failed"
        else:
            updated, problems = sync_files()
            note = (", ".join(updated) or "nothing new") + ("" if not problems else " · problems: " + "; ".join(problems))
            log("refresh from GitHub: " + note)
            day = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
            if self.state.get("update_note") != day:
                self.code_old = code_outdated()
                if self.code_old:
                    self.state["update_note"] = day
                    log(f"newer code on GitHub: {', '.join(self.code_old)} - run windows\\4_update.bat")
                    if self.send:
                        telegram("🔄 A newer version of the live watcher is on GitHub. On the PC, double-click "
                                 "<b>windows\\4_update.bat</b> (it stops the watcher, updates it and starts it again).")
        self.last_refresh = (self.now_fn(), note)
        self.reload()
        if self.send:
            self.weekly_review(self.now_fn())

    # ---- local state (duplicate guard, heartbeat) ----
    def _load_state(self):
        try:
            st = json.load(open(STATE))
        except (OSError, ValueError):
            st = {}
        # alerts: the buttons' memory (3 days) · trades: the ones being followed · paused_until: 0 = alerts on,
        # -1 = until /resume, else the end (ms) · tg_offset: the next Telegram update to read
        # shadow: every alert followed silently by the plan's rules (its "plan" result goes to the journal)
        # tests_on: 🔵 TEST alerts on / off (/tests) · test_sent: when each TEST alert went out (the daily cap)
        for k, v in dict(sent={}, heartbeat=None, alerts={}, trades={}, results=[], paused_until=0, tg_offset=None,
                         next_id=0, shadow={}, tests_on=True, test_sent=[], review_week=None, review=None).items():
            st.setdefault(k, v)
        return st

    def _save_state(self):
        now = self.now_fn()
        cut = now - 2 * 86_400_000                                   # the duplicate guard needs hours, not weeks
        self.state["sent"] = {k: v for k, v in self.state["sent"].items() if int(v) >= cut}
        self.state["alerts"] = {k: a for k, a in self.state["alerts"].items()
                                if k in self.state["trades"] or int(a["sent_ms"]) >= now - 3 * 86_400_000}
        self.state["results"] = self.state["results"][-200:]
        self.state["test_sent"] = [m for m in self.state["test_sent"] if int(m) >= now - 3 * 86_400_000]
        try:
            os.makedirs(os.path.dirname(STATE), exist_ok=True)
            with open(STATE, "w") as f:
                json.dump(self.state, f)
        except OSError as e:
            log(f"state not saved: {e}")

    # ---- data ----
    def update(self, coin, tf, now_ms):
        """Keep the newest S['bars'] closed candles of coin x tf (full download once, then the newest 100)."""
        key, n = (coin, tf), int(self.S["bars"])
        have = self.frames.get(key)
        if have is None or len(have) < 300:
            new = self.feed.candles(coin, tf, n)
        else:
            new = pd.concat([have, self.feed.candles(coin, tf, 100, recent_only=True)])
        new = new.drop_duplicates("open_time", keep="last").sort_values("open_time").tail(n).reset_index(drop=True)
        self.frames[key] = new
        return new

    def coin_data(self, coin, now_ms):
        """(data, quality) in the scanner's layout for prepare_coin; quality from the same data checks."""
        sym = coin + self.cfg["market"]["quote"]
        data, quality = {}, {}
        for tf in DATA_TFS:
            raw = self.frames.get((coin, tf))
            if raw is None or not len(raw):
                continue
            clean, rep = dq.check_candles(raw, sc.TF_MS[tf], now_ms, self.dq_cfg)
            data[(sym, tf)], quality[(coin, tf)] = clean, rep
        return sym, data, quality

    # ---- one pass, at a 5-minute boundary ----
    def tick(self, now_ms=None):
        """One pass: new trade alerts, then the trades the operator took. Returns the new alerts."""
        now_ms = now_ms or self.now_fn()
        b = lv.boundary(now_ms)
        closed = lv.closed_at(b)
        need_tfs = sorted({tf for _, tf, _ in self.watch if tf in closed} | ({"5m"} if self.pending else set()),
                          key=sc.TF_ORDER.index)
        alerts = self.scan(now_ms, b, closed, need_tfs) if need_tfs else []
        self.pause_check(now_ms)
        self.deliver(alerts, now_ms)
        self.follow(now_ms)
        self._save_state()
        return alerts

    def scan(self, now_ms, b, closed, need_tfs):
        alerts = []
        hourly = b % sc.TF_MS["1h"] == 0
        for coin in self.coins + self.extra:
            for tf in DATA_TFS:
                if (coin, tf) not in self.frames or tf in closed or (tf in ("1d", "1w") and hourly):
                    try:
                        self.update(coin, tf, now_ms)
                    except Exception as e:
                        log(f"{coin} {tf}: download failed: {e}")
        btc = sc.btc_frames(self.coin_data("BTC", now_ms)[1], self.cfg["market"]["quote"], sc.TF_ORDER)
        prep = sorted(set(need_tfs) | {"4h"}, key=sc.TF_ORDER.index)      # 4H: the h4_* context columns
        try:
            derivs = sc.load_derivs(False, self.coins, now_ms)
        except Exception:
            derivs = {}
        for coin in self.coins:
            sym, data, quality = self.coin_data(coin, now_ms)
            try:
                flow = None                          # step 3: today's order flow (CVD) for playbook strategies
                if any(s.get("gate") == "playbook" for s, _, _ in self.watch):
                    try:
                        flow = fh.okx_today(coin, now_ms)
                    except Exception as e:
                        log(f"{coin}: order flow not loaded ({e}) - CVD unknown")
                pc = sc.prepare_coin(sym, coin, data, quality, [t for t in prep if (sym, t) in data], self.cfg,
                                     derivs.get(coin), btc, flow)
            except Exception as e:
                log(f"{coin}: prepare failed: {e}")
                continue
            alerts += self.signals(coin, pc, quality, b, closed, now_ms)
            alerts += self.confirmations(coin, pc, now_ms)
        return alerts

    # ---- Telegram out: alerts with buttons, follow-ups, replies ----
    def say(self, text, buttons=None):
        if not self.send:
            print("\n" + text + "\n", flush=True)
            return True, "", None
        return telegram_message(text, buttons=buttons)

    def paused(self, now_ms):
        p = int(self.state.get("paused_until") or 0)
        return p < 0 or p > now_ms

    def pause_check(self, now_ms):
        p = int(self.state.get("paused_until") or 0)
        if 0 < p <= now_ms:
            self.state["paused_until"] = 0
            self.say("▶️ The pause is over: new trade alerts are on again.")

    def deliver(self, alerts, now_ms):
        tests = [a for a in alerts if a["label"] == "TEST"]
        if tests:                                    # the Signal Center: /tests off, then at most N a day
            if not self.state.get("tests_on", True):
                keep, drop = [], tests
            else:
                keep, drop = scx.cap(tests, scx.sent_today(self.state["test_sent"], now_ms), self.SC)
            for a in drop:
                log(f"ALERT TEST {a['coin']} {a['tf']} {a['strategy']}: not sent ("
                    + ("TEST alerts off" if not self.state.get("tests_on", True) else
                       f"daily maximum of {self.SC['max_per_day']} reached") + ") - GitHub still records it")
            alerts = [a for a in alerts if a["label"] != "TEST"] + keep
        for a in alerts:
            what = f"ALERT {a['label']} {a['coin']} {a['tf']} {a['strategy']}: "
            if self.send and self.paused(now_ms):
                log(what + "alerts are paused (/resume) - not sent")
                continue
            if a["label"] == "TEST":
                self.state["test_sent"].append(now_ms)
            aid = self._remember(a)
            ok, err, mid = self.say(lv.message(a), lv.choice_buttons(aid))
            self.state["alerts"][aid]["msg_id"] = mid
            if self.send:
                log(what + ("sent" if ok else f"NOT sent ({err})"))
                st = self.state["alerts"][aid]                  # journal sync: the alert and its silent plan follow-up
                self.journal(dict(st, id=aid), "alert", int(st["sent_ms"]))
                self.state["shadow"][aid] = fl.open_trade(st, aid, int(st["sent_ms"]), self.cfg.get("trade_plan"))

    def _remember(self, a):
        """Keep what the buttons and the follow-up need; returns the alert id (in the buttons' data)."""
        self.state["next_id"] = int(self.state["next_id"]) + 1
        aid = f"{int(a['sent_ms']) // 1000:x}{self.state['next_id'] % 1000:03d}"
        self.state["alerts"][aid] = dict({k: a.get(k) for k in ("label", "coin", "inst", "d", "tf", "strategy",
                                          "version", "entry", "R", "tps", "split", "max_hold", "close_ms", "sent_ms",
                                          "limit_bars", "manage", "inval", "be_frac", "test", "program", "market",
                                          "against")},
                                         choice=None, msg_id=None)
        return aid

    def journal(self, a, event, ms, price=None, result_r=None):
        """One row in journal/my_trades.csv (the operator's own record: took / skipped / closed / results)."""
        tps = list(a.get("tps") or []) + [None] * 3
        row = [dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M"), a.get("id", ""),
               event, a["label"], a["coin"], "LONG" if a["d"] == 1 else "SHORT", a["tf"], a["strategy"],
               a.get("version"), a["entry"], a["entry"] - a["d"] * a["R"], *tps[:3], price,
               None if result_r is None else round(result_r, 3)]
        try:
            os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)
            new = not os.path.exists(JOURNAL)
            with open(JOURNAL, "a", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                if new:
                    w.writerow(JOURNAL_COLS)
                w.writerow(["" if x is None else x for x in row])
        except OSError as e:
            log(f"journal not written: {e}")

    # ---- the trades the operator took ----
    def _advance(self, t, now_ms, cache):
        """Walk one trade through the 5m candles closed since its last check; None when the download failed."""
        if t["coin"] not in cache:
            try:
                raw = self.update(t["coin"], "5m", now_ms)
                cache[t["coin"]] = raw[raw["close_time"] < now_ms]
            except Exception as e:
                log(f"follow {t['coin']}: download failed: {e}")
                cache[t["coin"]] = None
        closed = cache[t["coin"]]
        if closed is None:
            return None
        tc = t.get("trail_cfg") or {}
        if t.get("trailing") and len(closed) and "atr_n" in tc:   # the trailing ATR exit: on the card's own candles
            key = (t["coin"], t["tf"])
            if key not in cache:
                try:
                    raw = self.update(t["coin"], t["tf"], now_ms)
                    cache[key] = raw[raw["close_time"] < now_ms]
                except Exception as e:
                    log(f"follow {t['coin']} {t['tf']}: download failed: {e}")
                    cache[key] = None
            closed = closed.assign(**trail_on_5m(closed, cache[key], tc))
        elif t.get("trailing") and len(closed):      # step 3: the playbook's trail (last 5m swing / EMA9)
            tl, ts = mg.trail_levels(closed["high"].to_numpy(), closed["low"].to_numpy(), closed["close"].to_numpy(),
                                     int(tc.get("swing_n", 3)), int(tc.get("ema", 9)))
            closed = closed.assign(trail_long=tl, trail_short=ts)
        return fl.step(t, closed[closed["open_time"] >= t["checked_ms"]].to_dict("records"))

    def follow(self, now_ms):
        cache = {}
        for tid, t in list(self.state["trades"].items()):
            evs = self._advance(t, now_ms, cache)
            for ev in evs or []:
                self.say(fl.text(t, ev) + (RESULT_HINT if ev.get("final") and ev["kind"] != "expired" else ""))
                name = f"tp{ev['n']}" if ev["kind"] == "tp" else ev["kind"]
                self.journal(t, name, ev["at_ms"], ev["px"], ev.get("result_r") if ev.get("final") else None)
                log(f"FOLLOW {t['coin']} {t['tf']} {t['strategy']}: {name}")
            if t["closed"]:
                filled = t.get("filled", True)
                self._end_trade(tid, "done", now_ms, t["realized"] if filled else None,
                                "finished" if filled else "limit not filled")
        for sid, t in list(self.state["shadow"].items()):     # every alert, silently: the plan's result
            evs = self._advance(t, now_ms, cache)
            fin = next((e for e in evs or [] if e.get("final")), None)
            if fin:
                self.journal(t, "plan" if t.get("filled", True) else "plan not filled", fin["at_ms"], fin["px"],
                             fin.get("result_r"))
                self.state["shadow"].pop(sid)
            elif now_ms - int(t["taken_ms"]) > SHADOW_DAYS * 86_400_000:
                self.state["shadow"].pop(sid)                  # no stop, target or time stop in 14 days: dropped

    def _end_trade(self, tid, choice, now_ms, r, how):
        t = self.state["trades"].pop(tid, None)
        if t:
            self.state["results"].append(dict(id=tid, coin=t["coin"], d=t["d"], tf=t["tf"], label=t["label"],
                                              strategy=t["strategy"], r=r, how=how, ended_ms=now_ms))
        a = self.state["alerts"].get(tid)
        if a:
            a["choice"] = choice
            if a.get("msg_id") and self.send:
                tg_api("editMessageReplyMarkup", dict(chat_id=os.environ.get("TELEGRAM_CHAT_ID"),
                                                      message_id=a["msg_id"],
                                                      reply_markup=lv.choice_buttons(tid, choice)))

    # ---- Telegram in: the operator's commands and button presses ----
    def commands_on(self):
        return bool(self.send and os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID"))

    def poll(self, wait_s):
        """Wait up to wait_s seconds for the operator's messages / button presses and answer them."""
        p = dict(timeout=int(wait_s), allowed_updates=["message", "callback_query"])
        if self.state.get("tg_offset") is not None:
            p["offset"] = int(self.state["tg_offset"])
        ok, res = tg_api("getUpdates", p, timeout=wait_s + 15)
        if not ok:
            if res != self._poll_err:
                log(f"Telegram commands: {res}")
            self._poll_err = res
            time.sleep(min(wait_s, 10))
            return
        self._poll_err = None
        for u in res or []:
            self.state["tg_offset"] = int(u["update_id"]) + 1
            try:
                self.on_update(u, self.now_fn())
            except Exception as e:
                log(f"command failed: {e}\n{traceback.format_exc()}")
        if res:
            self._save_state()

    def wait_until(self, ms):
        """Sleep until ms, answering Telegram commands meanwhile."""
        while True:
            rem = (ms - self.now_fn()) / 1000
            if rem <= 0:
                return
            if self.commands_on() and rem >= 2:
                self.poll(min(25, int(rem) - 1))
            else:
                time.sleep(rem)

    def on_update(self, u, now_ms):
        chat = str(os.environ.get("TELEGRAM_CHAT_ID", ""))
        cq = u.get("callback_query")
        m = (cq or {}).get("message") or u.get("message") or {}
        sender = str((m.get("chat") or {}).get("id", ""))
        if not chat or sender != chat:                               # only the operator's own chat is answered
            log(f"Telegram: ignored an update from chat {sender or '?'} (not TELEGRAM_CHAT_ID)")
            return
        if cq:
            return self.on_button(cq, now_ms)
        if int(m.get("date") or 0) * 1000 < now_ms - 10 * 60_000:  # sent while the watcher was off: too old
            return
        cmd, arg = lv.parse_command(m.get("text"))
        self.say(self.command(cmd, arg, now_ms))

    def command(self, cmd, arg, now_ms):
        if cmd in ("start", "help"):
            return lv.HELP
        if cmd == "status":
            return self.status_text(now_ms)
        if cmd == "trades":
            return self.trades_text(now_ms)
        if cmd == "pause":
            try:
                dur = lv.parse_duration(arg)
            except ValueError:
                return "Use /pause (until /resume), /pause 2h or /pause 30m (at most 7 days)."
            self.state["paused_until"] = -1 if dur is None else now_ms + dur
            self._save_state()
            return ("⏸ New trade alerts paused " + ("until /resume." if dur is None else f"until {lv.bj(now_ms + dur)}.")
                    + "\nYou still get the messages about trades you took and the daily 'running' message.")
        if cmd == "resume":
            self.state["paused_until"] = 0
            self._save_state()
            return "▶️ New trade alerts are on again."
        if cmd == "result":
            return self.result(arg, now_ms)
        if cmd == "review":
            rv = self._json("reports/weekly_review.json")
            return (rv or {}).get("telegram") or "📊 No weekly review yet - GitHub's hourly scan writes it."
        if cmd == "tests":
            arg = (arg or "").strip().lower()
            if arg in ("on", "off"):
                self.state["tests_on"] = arg == "on"
                self._save_state()
            on = self.state.get("tests_on", True)
            n = sum(1 for _, _, lab in self.watch if lab == "TEST")
            return (f"🔵 TEST alerts are <b>{'ON' if on else 'OFF'}</b>. "
                    + (f"{n} backtest-positive strategy timeframe(s) watched on their positive coins; at most "
                       f"{self.SC['max_per_day']} a day, each confirmed by a 5m candle. " if on else
                       "GitHub still records every TEST setup for the weekly review. ")
                    + ("/tests off to stop them." if on else "/tests on to switch them on."))
        if cmd == "weather":
            try:
                with open(os.path.join(ROOT, "reports", "market_weather.json"), encoding="utf-8") as f:
                    w = json.load(f)
            except (OSError, ValueError):
                w = None
            return lv.weather_text(w, now_ms)
        if cmd is None:
            return "I only understand commands. Send /help for the list."
        return f"I don't know /{cmd}. Send /help for the list."

    def on_button(self, cq, now_ms):
        action, _, aid = (cq.get("data") or "").partition("|")
        if action == "promo":                        # PR 3: a tap under the weekly review
            return self.on_promote(cq, aid, now_ms)
        a = self.state["alerts"].get(aid)
        toast = ""
        if a is None:
            toast = "This alert is too old (buttons work for 3 days)."
        elif action == "info":                       # ℹ️ Details: the strategy, its rules, its backtest on this coin
            self.say(lv.details_text(a, self.cards.get(f"{a['strategy']}@{a['version']}")))
            toast = "Details sent below."
        elif a.get("choice") in ("closed", "done") or action == "noop":
            toast = "This trade is already finished."
        elif action == "took" and a.get("choice") != "took":
            a["choice"] = "took"
            self.state["trades"][aid] = fl.open_trade(a, aid, now_ms, self.cfg.get("trade_plan"))
            self.journal(dict(a, id=aid), "took", now_ms)
            demo = a.get("label") == "TEST"
            toast = "Recorded as a demo trade (TEST)." if demo else "Recorded: you took it. I'll follow this trade."
            self.say(("🔵 Demo book: " if demo else "")
                     + f"👀 Following your {'LONG' if a['d'] == 1 else 'SHORT'} {a['coin']} "
                     + f"({a['tf']} {a['strategy']}). "
                     + ("It never counts in your loss limits. " if demo else "")
                     + ("Your limit order waits for a fill: I'll tell you when it fills or when to cancel it. "
                        if a.get("limit_bars") else "Put the stop-loss and the TPs on OKX now if you haven't. ")
                     + "I'll message you when a TP, the stop or the time stop is reached. Press 🏁 I closed it under "
                     "the alert if you close it yourself.")
        elif action == "skip" and a.get("choice") != "skip":
            a["choice"] = "skip"
            self.state["trades"].pop(aid, None)
            self.journal(dict(a, id=aid), "skipped", now_ms)
            toast = "Recorded: skipped."
        elif action == "closed" and a.get("choice") == "took":
            self.journal(dict(a, id=aid), "closed by you", now_ms)
            self._end_trade(aid, "closed", now_ms, None, "closed by you")
            toast = "Recorded: closed. I stopped following it."
            self.say(f"🏁 Closed by you · {a['coin']} {a['tf']} {a['strategy']}." + RESULT_HINT)
        msg = cq.get("message") or {}
        if self.send:
            tg_api("answerCallbackQuery", dict(callback_query_id=cq.get("id"), text=toast))
        if a is not None and msg.get("message_id") and self.send:
            tg_api("editMessageReplyMarkup", dict(chat_id=msg["chat"]["id"], message_id=msg["message_id"],
                                                  reply_markup=lv.choice_buttons(aid, a.get("choice"))))
        self._save_state()
        return toast

    def result(self, arg, now_ms):
        """/result 1.2 - the operator's real result (R, after fees) of their newest finished trade without one;
        /result <id> 1.2 for another (the id is in /trades). Written to the journal as 'your result'."""
        try:
            aid, r = jr.parse_result(arg)
        except ValueError:
            return ("Send your real result in R after fees, e.g. /result 1.2 or /result -1 (-1 = the full stop lost, "
                    "2 = twice what you risked). For an older trade: /result &lt;id&gt; 1.2 (ids in /trades).")
        done = [x for x in self.state["results"] if x.get("how") != "limit not filled"
                and (x.get("id") == aid if aid else x.get("your_r") is None)]
        if aid is None and not done and self.state["trades"]:
            return "Your trades are still open. Send /result when one is finished."
        if not done:
            return "No finished trade " + (f"with id {aid}" if aid else "is waiting for a result") + ". See /trades."
        x = done[-1]
        x["your_r"] = r
        a = dict(self.state["alerts"].get(x["id"]) or {}, id=x["id"])
        if a.get("entry") is not None:
            self.journal(a, "your result", now_ms, None, r)
        else:                                                  # the alert is older than 3 days: the short record
            self.journal(dict(a, label=x["label"], coin=x["coin"], d=x["d"], tf=x["tf"], strategy=x["strategy"],
                              entry=0.0, R=0.0, tps=[]), "your result", now_ms, None, r)
        self._save_state()
        plan = f" (plan: {x['r']:+.1f}R)" if x.get("r") is not None else ""
        return (f"📒 Recorded: your result {r:+.2f}R · {'LONG' if x['d'] == 1 else 'SHORT'} {x['coin']} {x['tf']} "
                f"{x['strategy']}{plan}. It goes into the weekly review of your trades.")

    # ---- PR 3: the weekly review in Telegram, and the operator's promote taps ----
    def weekly_review(self, now_ms):
        """Send the final weekly review once (Sunday, from 04:00 UTC), with one Promote button per candidate."""
        rv = self._json("reports/weekly_review.json")
        if not rv or not rv.get("final") or rv.get("week") == self.state.get("review_week"):
            return False
        self.state["review_week"] = rv["week"]
        self.state["review"] = dict(week=rv["week"], promote=[
            dict(key=p["key"], coin=p["coin"], name=f"{p['key'].split('@')[0]} {p['tf']} {p['coin']}")
            for p in rv.get("promote") or []])
        rows = [[{"text": f"🟡 Promote {i + 1}: {p['name']}"[:60], "callback_data": f"promo|{i}"}]
                for i, p in enumerate(self.state["review"]["promote"])]
        self.say(rv.get("telegram") or "📊 Weekly review ready.", {"inline_keyboard": rows} if rows else None)
        self._save_state()
        return True

    def on_promote(self, cq, idx, now_ms):
        rv = self.state.get("review") or {}
        try:
            p = (rv.get("promote") or [])[int(idx)]
        except (ValueError, IndexError):
            p = None
        if p is None:
            toast = "This weekly review is no longer current."
        else:
            row = [dt.datetime.fromtimestamp(now_ms / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M"), rv["week"],
                   "promote", p["key"], p["coin"]]
            try:
                os.makedirs(os.path.dirname(DECISIONS), exist_ok=True)
                new = not os.path.exists(DECISIONS)
                with open(DECISIONS, "a", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    if new:
                        w.writerow(jr.DECISION_COLS)
                    w.writerow(row)
            except OSError as e:
                log(f"decision not written: {e}")
            ok, note = self.dsync.push(now_ms)
            sid, rest = p["key"].split("@", 1)
            ver, tf = rest.split("|")
            if ok and note != "off":
                toast = "Promoted - GitHub applies it in the next research run."
                self.say(f"🟡 Promoted: {p['name']}. GitHub's next nightly research run makes it PAPER on {p['coin']} "
                         "(practice alerts, 🟡). LIVE still needs 20 good paper signals, the full pass bar and your "
                         "approval line.")
            else:
                toast = "Recorded on this PC - add the line to config.yaml (see the message)."
                self.say(f"🟡 Recorded on this PC, but GitHub cannot see it: journal sync is off "
                         f"({'no token' if note == 'off' else note}). Either set it up (windows\\6_journal_sync.bat) "
                         "or add this line under <code>promotions:</code> in config.yaml on GitHub:\n"
                         f"<code>  - {{strategy: {sid}, version: \"{ver}\", tf: {tf}, coin: {p['coin']}, "
                         f"date: {row[0][:10]}}}</code>")
        if self.send:
            tg_api("answerCallbackQuery", dict(callback_query_id=cq.get("id"), text=toast))
        self._save_state()
        return toast

    def status_text(self, now_ms):
        day = lv.boundary(now_ms, "1d")
        return lv.status_text(dict(
            feed=self.feed.name, started_ms=self.started_ms, now_ms=now_ms, last_tick=self.last_tick,
            paused_until=self.state.get("paused_until"), watch=[(s["id"], tf, lab) for s, tf, lab in self.watch],
            coins=self.coins, open_trades=len(self.state["trades"]),
            alerts_today=sum(1 for a in self.state["alerts"].values() if int(a["sent_ms"]) >= day),
            tests_on=self.state.get("tests_on", True), tests_today=scx.sent_today(self.state["test_sent"], now_ms),
            tests_max=self.SC["max_per_day"],
            refresh=self.last_refresh, code_old=self.code_old, journal_sync=self.jsync.status(now_ms),
            heartbeat=self.hb.status(now_ms)))

    def trades_text(self, now_ms):
        lines = ["📒 <b>Your trades</b>"]
        real = [t for t in self.state["trades"].values() if t.get("label") != "TEST"]
        demo = [t for t in self.state["trades"].values() if t.get("label") == "TEST"]
        if real:
            lines.append("Being followed:")
            lines += [fl.summary(t) for t in real]
        if demo:
            lines.append("🔵 Demo book (TEST trades - never in your loss limits):")
            lines += [fl.summary(t) for t in demo]
        if not real and not demo:
            lines.append("No trade is being followed. Press ✅ Took it under an alert and I'll follow it.")
        res_all = [r for r in self.state["results"] if int(r["ended_ms"]) >= now_ms - 30 * 86_400_000]
        for title, res in (("Last 30 days", [r for r in res_all if r.get("label") != "TEST"]),
                           ("Demo book, last 30 days", [r for r in res_all if r.get("label") == "TEST"])):
            if not res:
                continue
            known = [r["r"] for r in res if r["r"] is not None]
            lines.append(f"\n{title}: {len(res)} finished" + (
                f" · {sum(1 for r in known if r > 0)} won · total about {sum(known):+.1f}R before fees" if known else ""))
            for r in res[-5:]:
                when = dt.datetime.fromtimestamp(int(r["ended_ms"]) / 1000, dt.timezone.utc)
                lines.append(f"• {when:%d %b} {'LONG' if r['d'] == 1 else 'SHORT'} {r['coin']} {r['tf']} ({r['label']}): "
                             + (f"{r['r']:+.1f}R" if r["r"] is not None else r["how"])
                             + (f" · yours {r['your_r']:+.1f}R" if r.get("your_r") is not None else
                                f" · /result {r['id']} …" if r.get("id") else ""))
        lines.append("\nFull record on the PC: journal\\my_trades.csv")
        return "\n".join(lines)

    def _good(self, coin, tf, quality):
        for t in (tf, sc.HTF.get(tf)):
            r = quality.get((coin, t))
            if t and (r is None or r["state"] != dq.GOOD):
                return False
        return True

    def signals(self, coin, pc, quality, b, closed, now_ms):
        out, test_cands = [], []
        for s, tf, label in self.watch:
            fr = pc["frames"].get(tf)
            if tf not in closed or fr is None or not self._good(coin, tf, quality):
                continue
            stats = (self.tests.get(f"{sspec.key(s)}|{tf}") or {}).get(coin) if label == "TEST" else None
            if label == "TEST" and (stats is None or not self.state.get("tests_on", True)):
                continue                             # TEST: only on the coins where the backtest was positive
            promo = self.promoted.get(f"{sspec.key(s)}|{tf}")
            if label == "PAPER" and promo is not None and coin not in promo:
                continue                             # PR 3: PAPER by your tap - only on the promoted coins
            df, t = fr["df"], fr["n"] - 1
            if int(df["close_time"].iloc[t]) != b - 1:              # the candle that just closed must be there
                log(f"{coin} {tf}: newest candle not in yet - skipped this close")
                continue
            try:
                L, S, _, _, cols = sc.strategy_signals(s, tf, fr, self.cfg)
            except Exception as e:
                log(f"RULE ERROR {s['id']} {tf}: {e}")
                continue
            d = 1 if L[t] else (-1 if S[t] else 0)
            if d == 0:
                continue
            entry, atr = float(df["close"].iloc[t]), float(df["_atr"].iloc[t])
            lim, levs = sspec.limit_entry(s), sspec.limit_levels(s)
            if lim:                                  # roadmap step 2B: limit order at the close -/+ offset x ATR
                lpx = float(cols[levs[0 if d == 1 else 1]][t]) if levs else entry - d * lim[0] * atr
                if np.isfinite(lpx):                 # step 3: an unknown level = market entry (playbook)
                    entry = lpx
                else:
                    lim = None
            plan = sc.plan_trade(s, t, d, entry, atr, cols, self.cfg, maker=bool(lim))
            if plan is None:
                continue
            R, tps, split = plan
            reg_now = (pc["recs"].get(lc.regime_tf(tf)) or {}).get("label")
            why = rfit.blocked(self.regime_fit, f"{sspec.key(s)}|{tf}", reg_now)
            if why:                                  # roadmap step 5: not in a market type where it lost money
                log(f"{coin} {tf} {s['id']}: no alert - {why}")
                continue
            if s.get("gate") == "playbook":
                why = self.pb_coin_problem(coin, now_ms)
                if why:                              # playbook 2.5 / 5.4: skip the pair
                    log(f"{coin} {tf} {s['id']}: playbook filter - {why}")
                    continue
            if label == "TEST":                      # one per coin + direction + strategy within the TEST cooldown
                key = scx.group_key(dict(coin=coin, d=d, strategy=s["id"], test=stats))
                last = self.state["sent"].get(key)
                if (last is not None and now_ms - int(last) < self.SC["cooldown_minutes"] * 60_000) or \
                        any(p["key"] == key for p in self.pending):
                    continue
            else:
                key = lv.dedupe_key(coin, d, s["id"], s["version"], tf)
                if not lv.allowed(self.state["sent"], key, now_ms, self.S) or \
                        any(p["key"] == key for p in self.pending):
                    continue
            base = dict(label=label, coin=coin, inst=self.feed.inst(coin), d=d, tf=tf, strategy=s["id"],
                        version=s["version"], entry=entry, R=float(R), tps=[float(x) for x in tps], split=split,
                        zone_r=float(self.S["entry_zone_r"]), max_hold=s.get("time_stop_bars"),
                        limit_bars=lim[1] if lim else None, manage=s.get("manage"), gate=s.get("gate"),
                        pb_late=self._col(fr, "pb_late", t), pb_half=self._col(fr, f"pbB_half_{'long' if d == 1 else 'short'}", t)
                        if s["id"].startswith("PB-B") else False, pb_grade=sc.half_size_reason(s, fr.get("feats"), d, t),
                        inval=self._inval(s, d, cols, t), be_frac=self._be_frac(d, bool(lim)),
                        regimes={k: v["label"] for k, v in pc["recs"].items()}, close_ms=b - 1,
                        valid_bars=int(self.cfg["signals"]["lookback_bars"]), key=key)
            if label == "TEST":
                prog = s.get("program") or {}
                base.update(test=stats, program=dict(name=prog.get("name"), version=prog.get("version")),
                            against=scx.against_daily(d, pc["recs"]), market=scx.market_type(pc["recs"]),
                            weather=scx.weather_line(self.weather, coin))
                test_cands.append(base)
                continue
            if s.get("confirm_5m"):
                self.pending.append(dict(base, after_ms=b, coin=coin))
                log(f"{coin} {tf} {s['id']}: trigger - waiting for the 5m confirmation")
                continue
            out.append(self._finish(base, now_ms))
        recent = [a for a in self.state["alerts"].values() if a.get("coin") == coin] + \
            [p for p in self.pending if p.get("coin") == coin]
        for a in scx.merge(test_cands):             # the Signal Center: merged, then the 5m candle confirms
            a["agree"] = scx.agreement(a, recent, now_ms, self.SC, others=test_cands + out)
            if self.SC["confirm_5m"]:
                self.state["sent"][a["key"]] = now_ms          # reserved: no duplicate while it waits
                self.pending.append(dict(a, after_ms=b, reserved_ms=now_ms))
                log(f"{coin} {a['tf']} {a['strategy']}: TEST trigger - waiting for the 5m confirmation")
            else:
                out.append(self._finish(a, now_ms))
        return out

    def pb_coin_problem(self, coin, now_ms):
        """Playbook 2.5 / 5.4 on the exchange the operator trades: the coin must be on the playbook's coin list (24h
        volume, spread) and the spread right now at most 2x the normal maximum. None = fine; unknown data = fine."""
        if now_ms - getattr(self, "_pb_stats_ms", 0) > 5 * 60_000:
            self._pb_stats, self._pb_stats_ms = sc.okx_swap_stats(), now_ms
        sec = self.cfg.get("playbook") or {}
        coins = spb.coin_list(sec, self._pb_stats)
        if coins is not None and coin not in coins:
            return f"not on the playbook's coin list now ({', '.join(coins)})"
        sp = (self._pb_stats.get(coin) or (None, None))[1]
        if sp is not None and sp > 2 * float(sec.get("max_spread_pct", 0.02)):
            return f"spread {sp:.3f}% is above 2x normal"
        return None

    @staticmethod
    def _col(fr, name, t):
        f = fr.get("feats")
        return bool(f is not None and name in f and f[name].iloc[t] == 1)

    @staticmethod
    def _inval(s, d, cols, t):
        iv = (s.get("manage") or {}).get("invalidate")
        if not iv:
            return None
        v = float(cols[iv["long" if d == 1 else "short"]][t])
        return v if np.isfinite(v) else None

    def _be_frac(self, d, limit):
        """Breakeven + fees: the entry fee (maker for a limit) and a market exit, as a fraction of the entry."""
        k = sc.trade_costs(self.cfg, d)
        return (k["maker"] if limit else k["taker"]) + k["taker"] + k["slip"]

    def confirmations(self, coin, pc, now_ms):
        out, keep = [], []
        m5 = sc.m5_arrays(pc["frames"])
        for p in self.pending:
            if p["coin"] != coin:
                keep.append(p)
                continue
            if m5 is None:
                if now_ms - p["after_ms"] < 2 * sc.TF_MS["1h"]:      # no 5m data: give up after 2 hours
                    keep.append(p)
                continue
            res = c5m.check(m5, p["after_ms"], p["d"], p["entry"], p["entry"] - p["d"] * p["R"], self.S5)
            if res["state"] == c5m.AWAITING:
                keep.append(p)
            elif res["state"] == c5m.CONFIRMED:
                j = res["idx"]
                a = dict(p, entry=float(m5["close"][j]), close_ms=int(m5["close_time"][j]),
                         confirm=f"CONFIRMED on the {lv.bj(int(m5['close_time'][j]) + 1)} 5m bar close"
                         + (f" ({', '.join(res['smc'])})" if res["smc"] else ""))
                a["tps"] = [a["entry"] + (tp - p["entry"]) for tp in p["tps"]]   # same distances from the 5m entry
                out.append(self._finish(a, now_ms))
            else:
                log(f"{coin} {p['tf']} {p['strategy']}: 5m {res['state']} - {res['why']}")
                if p.get("reserved_ms") is not None and self.state["sent"].get(p["key"]) == p["reserved_ms"]:
                    self.state["sent"].pop(p["key"])            # a TEST setup that failed may alert again
        self.pending = keep
        return out

    def _finish(self, a, now_ms):
        RK = self.RK
        stop = a["entry"] - a["d"] * a["R"]
        warn = []
        pbook = a.get("gate") == "playbook"          # step 3: the operator's playbook rules for its PB-* strategies
        PB = rk.pb_settings(self.cfg.get("playbook"))
        mins = PB["blackout_minutes"] if pbook else RK["blackout_minutes"]
        ev = rk.blackout(now_ms, RK["events"], mins)
        if ev:
            warn.append(f"high-impact event within {mins} min ({ev[0][3]}) - the risk rules say NO live entry now")
        if self.calendar_problem:
            warn.append(f"event calendar unreadable: {self.calendar_problem}")
        if not pbook and a["tps"] and a["d"] * (a["tps"][0] - a["entry"]) / a["R"] < float(RK.get("min_tp1_r", 2.0)) - 1e-9:
            warn.append(f"reward to TP1 below {RK.get('min_tp1_r', 2.0):g}R")
        pct = float(self.cfg["account"]["risk_per_trade_pct"])
        notes = []
        if pbook:
            warn += self.pb_limits(now_ms, PB)
            fac, notes = self.pb_size(PB, a)
            pct *= fac
            a = dict(a, max_isolated_leverage=spb.max_isolated_leverage(a["entry"], a["R"], PB["liq_x"]))
        size = rk.size(float(self.cfg["account"]["size_usdt"]), pct, a["entry"], stop, float(RK["max_leverage"]))
        self.state["sent"][a["key"]] = now_ms
        return dict(a, size=size, risk_pct=pct, warnings=warn, size_note=notes, sent_ms=self.now_fn())

    def pb_journal(self, now_ms):
        """The operator's own trades (✅ Took it) today, from the buttons' record: (count, R today, losing streak,
        last loss ms, last result, last week's R)."""
        day = now_ms // 86_400_000 * 86_400_000
        res = sorted([r for r in self.state.get("results") or [] if r.get("label") != "TEST"],   # demo book: never
                     key=lambda r: int(r["ended_ms"]))                                          # in the limits
        took_today = sum(1 for a in self.state["alerts"].values() if a.get("choice") in ("took", "closed", "done")
                         and int(a["sent_ms"]) >= day and a.get("label") != "TEST")
        today = [r for r in res if int(r["ended_ms"]) >= day and r.get("r") is not None]
        streak, last = 0, None
        for r in today:
            streak, last = (streak + 1, int(r["ended_ms"])) if r["r"] < 0 else (0, last)
        wk = dt.datetime.fromtimestamp(now_ms / 1000, dt.timezone.utc)
        w1 = int((wk - dt.timedelta(days=wk.weekday())).replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)
        last_week = sum(r["r"] for r in res if r.get("r") is not None and w1 - 7 * 86_400_000 <= int(r["ended_ms"]) < w1)
        known = [r for r in res if r.get("r") is not None]
        return took_today, sum(r["r"] for r in today), streak, last, (known[-1]["r"] if known else None), last_week

    def pb_limits(self, now_ms, PB):
        n, day_r, streak, last, _, _ = self.pb_journal(now_ms)
        out = []
        if day_r <= PB["day_limit_r"]:
            out.append(f"playbook: your trades today are {day_r:+.1f}R - daily loss limit, stop for the day")
        if n >= PB["max_trades_day"]:
            out.append(f"playbook: {n} trades taken today - the maximum is {PB['max_trades_day']}")
        if streak >= PB["stop_after_losses"]:
            out.append(f"playbook: {streak} losses in a row - stop for the day")
        elif streak >= PB["pause_after_losses"] and last and now_ms - last < PB["pause_minutes"] * 60_000:
            out.append(f"playbook: {streak} losses in a row - {PB['pause_minutes']}-minute break")
        return out

    def pb_size(self, PB, a):
        _, _, _, _, last_r, last_week = self.pb_journal(self.now_fn())
        why = []
        if a.get("pb_late"):
            why.append("late US / weekend: half size (playbook 2.3)")
        if a.get("pb_half"):
            why.append("counter-trend sweep: half size (playbook 5.2)")
        if a.get("pb_grade"):
            why.append(f"{a['pb_grade']}: half size")
        if last_r is not None and last_r >= PB["big_win_r"]:
            why.append(f"after a win of {PB['big_win_r']:g}R or more: half size (playbook 11)")
        if last_week <= PB["week_limit_r"]:
            why.append(f"last week {last_week:+.1f}R: half size this week (playbook 6.1)")
        return (0.5 if why else 1.0), why

    # ---- forever ----
    def sync_journal(self, now_ms, force=False):
        """Journal sync: upload journal/my_trades.csv to the GitHub branch `journal` when it changed (token needed)."""
        ok, note = self.jsync.push(now_ms, force)
        if note in ("off", "unchanged"):
            return ok, note
        if ok:
            log(f"journal uploaded to GitHub ({note})")
        elif note != getattr(self, "_jsync_err", None):
            log(f"journal sync failed: {note}")
        self._jsync_err = None if ok else note
        return ok, note

    def beat(self, now_ms):
        """The hourly "I am running" note for GitHub (Heartbeat). Never raises; a failure is logged once."""
        lt = self.last_tick
        info = dict(started_utc=dt.datetime.fromtimestamp(self.started_ms / 1000, dt.timezone.utc)
                    .strftime("%Y-%m-%d %H:%M"), feed=self.feed.name, coins=list(self.coins),
                    last_check_utc=dt.datetime.fromtimestamp(lt[0] / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
                    if lt else None, last_check_ok=bool(lt[1]) if lt else None, fails=self.fails,
                    watching={lab: sum(1 for _, _, x in self.watch if x == lab) for lab in ("LIVE", "PAPER", "TEST")},
                    open_trades=len(self.state.get("trades") or {}), paused=bool(self.paused(now_ms)),
                    tests_on=bool(self.state.get("tests_on", True)), code_old=bool(self.code_old))
        ok, note = self.hb.push(now_ms, info)
        if note in ("off", "not due"):
            return ok, note
        if ok and getattr(self, "_hb_err", None):
            log("GitHub heartbeat works again")
        elif not ok and note != getattr(self, "_hb_err", None):
            log(f"GitHub heartbeat failed: {note}")
        self._hb_err = None if ok else note
        return ok, note

    def heartbeat(self, now_ms):
        day = dt.datetime.fromtimestamp(now_ms / 1000, dt.timezone.utc)
        if day.strftime("%H:%M") < self.S["heartbeat_utc"] or self.state.get("heartbeat") == day.strftime("%Y-%m-%d"):
            return
        self.state["heartbeat"] = day.strftime("%Y-%m-%d")
        n = {lab: sum(1 for _, _, l in self.watch if l == lab) for lab in ("LIVE", "PAPER", "TEST")}
        telegram(f"✅ Live watcher running · {day:%Y-%m-%d}\nWatching {n['LIVE']} LIVE, {n['PAPER']} PAPER and "
                 f"{n['TEST']} TEST strategy timeframe(s) on {', '.join(self.coins)}."
                 + ("" if self.state.get("tests_on", True) else "\n🔵 TEST alerts are off (/tests on).")
                 + (f"\nFollowing {len(self.state['trades'])} trade(s) you took." if self.state["trades"] else "")
                 + ("\n⏸ New trade alerts are paused (/resume)." if self.paused(now_ms) else "")
                 + "\nSend /status any time.")
        self._save_state()

    def run(self):
        try:                                         # one watcher per computer: a second copy would double alerts
            self._lock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._lock.bind(("127.0.0.1", 47613))
        except OSError:
            log("another live watcher is already running on this computer - this copy stops")
            sys.exit(3)
        for note in windows_guard():
            log(note)
        self.refresh_repo()                          # start from GitHub's newest decisions (a ZIP may be days old)
        self.sync_journal(self.now_fn())
        ok, err = telegram(f"▶️ Live watcher started on {self.feed.name}. Watching {len(self.watch)} strategy "
                           f"timeframe(s) on {', '.join(self.coins)}. Send /help for the commands.") \
            if self.send else (True, "")
        if not ok:
            log(f"Telegram not working: {err}")
        while True:
            now = self.now_fn()
            self.wait_until(lv.boundary(now) + sc.TF_MS["5m"] + int(self.S["poll_delay_s"]) * 1000)
            try:
                if self.now_fn() - self.reloaded_ms >= int(self.S["refresh_minutes"]) * 60_000:
                    self.refresh_repo()
                self.tick()
                self.sync_journal(self.now_fn())
                self.last_tick = (self.now_fn(), True, "")
                self.beat(self.now_fn())
                self.heartbeat(self.now_fn())
                if self.fails >= int(self.S["error_alert_after"]):
                    telegram("✅ Live watcher recovered.")
                self.fails = 0
            except Exception as e:
                self.fails += 1
                self.last_tick = (self.now_fn(), False, f"{type(e).__name__}: {str(e)[:100]}")
                log(f"pass failed ({self.fails}): {e}\n{traceback.format_exc()}")
                if self.fails == int(self.S["error_alert_after"]):
                    telegram(f"⚠️ Live watcher: {self.fails} passes failed in a row - no alerts until it recovers.\n"
                             f"{type(e).__name__}: {str(e)[:300]}")


# ---------------------------------------------------------------- the Signal Center's safety replay (PR 2, Idea C)
REPLAY_TFS = ["1w", "1d", "4h", "1h", "30m", "15m", "5m"]


def replay(w, days=14, now_ms=None, coins=None, log_fn=print):
    """Replay the last `days` days on real candles with the live rules of the 🔵 TEST alerts: the TEST list, the
    strategy rules, plan_trade, the market-type filter, merging per coin + direction + strategy, the TEST cooldown,
    the 5m confirmation and the daily cap - then follow each alert to its plan result on the 5m candles (stop / TPs /
    time stop; the V4 trail is not replayed). w: a Watcher (feed, cards, TEST list, settings). Returns dict(alerts,
    days, dropped, summary)."""
    now_ms = int(now_ms or w.now_fn())
    start = now_ms - int(days) * 86_400_000
    coins = coins or w.coins
    tests = [(s, tf) for s, tf, lab in w.watch if lab == "TEST"]
    cands = []
    for coin in coins:
        if not any(coin in (w.tests.get(f"{sspec.key(s)}|{tf}") or {}) for s, tf in tests):
            continue
        for tf in REPLAY_TFS:                        # enough candles: the replay window + the indicators' warm-up
            n = int((now_ms - start) // sc.TF_MS[tf]) + 600
            try:
                w.frames[(coin, tf)] = w.feed.candles(coin, tf, n if tf not in ("1w", "1d") else 600)
            except Exception as e:
                log_fn(f"{coin} {tf}: download failed: {e}")
        sym, data, quality = w.coin_data(coin, now_ms)
        try:
            pc = sc.prepare_coin(sym, coin, data, quality, [t for t in sc.TF_ORDER if (sym, t) in data], w.cfg,
                                 None, sc.btc_frames(data, w.cfg["market"]["quote"], sc.TF_ORDER) if coin == "BTC"
                                 else None)
        except Exception as e:
            log_fn(f"{coin}: prepare failed: {e}")
            continue
        m5 = sc.m5_arrays(pc["frames"])
        for s, tf in tests:
            stats = (w.tests.get(f"{sspec.key(s)}|{tf}") or {}).get(coin)
            fr = pc["frames"].get(tf)
            if stats is None or fr is None or m5 is None:
                continue
            L, S, _, _, cols = sc.strategy_signals(s, tf, fr, w.cfg)
            df = fr["df"]
            ct = df["close_time"].to_numpy()
            for t in np.flatnonzero((L | S) & (ct >= start) & (ct < now_ms)):
                d = 1 if L[t] else -1
                entry, atr = float(df["close"].iloc[t]), float(df["_atr"].iloc[t])
                plan = sc.plan_trade(s, t, d, entry, atr, cols, w.cfg)
                if plan is None:
                    continue
                reg_t = sc.regime_at(fr["reg"], tf, t)
                if rfit.blocked(w.regime_fit, f"{sspec.key(s)}|{tf}", reg_t):
                    continue
                R, tps, split = plan
                recs = {k: dict(label=v[0][t]) for k, v in fr["reg"].items()}
                prog = s.get("program") or {}
                cands.append(dict(label="TEST", coin=coin, d=d, tf=tf, strategy=s["id"], version=s["version"],
                                  entry=entry, R=float(R), tps=[float(x) for x in tps], split=split,
                                  max_hold=s.get("time_stop_bars"), test=stats, close_ms=int(ct[t]),
                                  program=dict(name=prog.get("name"), version=prog.get("version")),
                                  against=scx.against_daily(d, recs), m5=m5, key=None))
    # in time order, exactly as live: merged per close, cooldown, the 5m candle, the daily cap
    out, dropped, sent, reserved = [], [], [], {}
    for close_ms in sorted({c["close_ms"] for c in cands}):
        now_c = close_ms + 1
        batch = [c for c in cands if c["close_ms"] == close_ms]
        for c in batch:
            c["key"] = scx.group_key(c)
        batch = [c for c in batch if reserved.get(c["key"]) is None
                 or now_c - reserved[c["key"]] >= w.SC["cooldown_minutes"] * 60_000]
        for a in scx.merge(batch):
            a["agree"] = scx.agreement(a, out[-20:], now_c, w.SC, others=batch)
            m5 = a.pop("m5")
            o, h, l, c = (np.asarray(m5[k], dtype=float) for k in ("open", "high", "low", "close"))
            hold = int(a["max_hold"] or 0) * (sc.TF_MS[a["tf"]] // sc.TF_MS["5m"])

            def plan_result(j0, entry):                # the plan's result from 5m bar j0 on (None = still open)
                if j0 >= len(c):
                    return None
                tps = [x + entry - a["entry"] for x in a["tps"]]
                r = sc.simulate_trade(o, h, l, c, j0, a["d"], entry, a["R"], w.cfg, max(1, hold), 5 / 60, tps=tps,
                                      split=a["split"])
                return None if r is None else dict(r=round(float(r["r"]), 2), reason=r["reason"])
            res = c5m.check(m5, now_c, a["d"], a["entry"], a["entry"] - a["d"] * a["R"], w.S5) if w.SC["confirm_5m"] \
                else dict(state=c5m.CONFIRMED, idx=c5m.first_bar(m5, now_c) - 1)
            if res["state"] != c5m.CONFIRMED:          # what it would have done without the 5m check (next 5m open)
                j0 = c5m.first_bar(m5, now_c)
                dropped.append(dict(a, why=f"5m {res['state']}: {res['why']}",
                                    without_5m=plan_result(j0, float(o[j0])) if j0 < len(o) else None))
                continue
            j = res["idx"]
            shift = float(m5["close"][j]) - a["entry"]
            a.update(entry=float(m5["close"][j]), tps=[x + shift for x in a["tps"]],
                     sent_ms=int(m5["close_time"][j]) + 1)
            if scx.sent_today(sent, a["sent_ms"]) >= w.SC["max_per_day"]:
                dropped.append(dict(a, why="daily maximum reached"))
                continue
            reserved[a["key"]] = now_c
            sent.append(a["sent_ms"])
            a["result"] = plan_result(j + 1, a["entry"])
            out.append(a)
    for a in dropped:
        a.pop("m5", None)
    done = [a["result"]["r"] for a in out if a.get("result")]
    unc = [a["without_5m"]["r"] for a in dropped if a.get("without_5m")]
    days_seen = {scx.bj_day(a["sent_ms"]) for a in out}
    summary = dict(alerts=len(out), finished=len(done), open=len(out) - len(done),
                   won=sum(1 for r in done if r > 0), total_r=round(sum(done), 2),
                   max_day=max([scx.sent_today([x["sent_ms"] for x in out], a["sent_ms"]) for a in out] or [0]),
                   days_with_alerts=len(days_seen), not_confirmed=sum(1 for a in dropped if a["why"].startswith("5m")),
                   capped=sum(1 for a in dropped if a["why"] == "daily maximum reached"),
                   unconfirmed_finished=len(unc), unconfirmed_won=sum(1 for r in unc if r > 0),
                   unconfirmed_total_r=round(sum(unc), 2))
    return dict(alerts=out, dropped=dropped, days=days, summary=summary)


def replay_text(rep):
    s = rep["summary"]
    lines = [f"Replay of the last {rep['days']} days with the 🔵 TEST alert rules (real OKX candles):",
             f"  {s['alerts']} alert(s) on {s['days_with_alerts']} day(s), at most {s['max_day']} in one Beijing day; "
             f"{s['not_confirmed']} setup(s) not confirmed by a 5m candle, {s['capped']} over the daily maximum",
             f"  plan results: {s['finished']} finished ({s['won']} won, total {s['total_r']:+.2f}R after fees), "
             f"{s['open']} still open",
             f"  the setups the 5m check removed, if entered anyway: {s['unconfirmed_finished']} finished "
             f"({s['unconfirmed_won']} won, total {s['unconfirmed_total_r']:+.2f}R after fees)", ""]
    for a in rep["alerts"]:
        when = dt.datetime.fromtimestamp(a["sent_ms"] / 1000, scx.BJ).strftime("%m-%d %H:%M")
        res = a.get("result")
        lines.append(f"  {when} BJ  {'LONG ' if a['d'] == 1 else 'SHORT'} {a['coin']:<5} {a['tf']:<4} "
                     f"{a['strategy']:<24} " + (f"{res['r']:+.2f}R ({res['reason']})" if res else "open")
                     + (" ⭐" if a.get("agree") else "") + (" ⚠️ vs 1D" if a.get("against") else ""))
    return "\n".join(lines)


def windows_guard():
    """On Windows: keep the computer awake while the watcher runs (sleep blocked; the screen may still turn off), and
    switch off QuickEdit in its window (a mouse click there would freeze the watcher until a key is pressed). Returns
    what it did; does nothing elsewhere and never stops the watcher."""
    if os.name != "nt":
        return []
    done = []
    try:
        import ctypes
        k = ctypes.windll.kernel32
        if k.SetThreadExecutionState(0x80000000 | 0x00000001):       # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
            done.append("sleep blocked while the watcher runs")
        h, mode = k.GetStdHandle(-10), ctypes.c_uint32()               # the window's keyboard / mouse input
        if k.GetConsoleMode(h, ctypes.byref(mode)):
            k.SetConsoleMode(h, (mode.value & ~0x0040) | 0x0080)      # QuickEdit off (extended flags on)
            done.append("QuickEdit off")
    except Exception as e:
        done.append(f"Windows guard failed: {e}")
    return done


def setup_telegram(path=SETTINGS_FILE, ask=input, wait_s=180):
    """Interactive: bot token -> check it -> the operator presses Start in the bot -> chat id found -> telegram.env
    written -> a test message. Used by windows\\1_setup.bat; works on any computer."""
    print("\nTELEGRAM SETUP\n1. In Telegram, open @BotFather, send /newbot, choose a name and a username ending in 'bot'.\n"
          "2. BotFather answers with a token like 123456789:AAH... - copy it.\n")
    token = ask("Paste the bot token here and press Enter: ").strip()
    try:
        me = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=15).json()
    except (requests.RequestException, ValueError):
        me = {}
    if not me.get("ok"):
        print("\nThat token does not work (Telegram refused it). Copy it again from BotFather and run setup again.")
        return False
    user = me["result"].get("username")
    print(f"\nToken OK - your bot is @{user}.\n3. Now open https://t.me/{user} in Telegram and press START "
          "(or send it 'hi').\nWaiting for your message (up to 3 minutes)...")
    chat, end = None, time.time() + wait_s
    while chat is None and time.time() < end:
        try:
            ids = find_chat_ids(token)
        except SystemExit:
            ids = []
        chat = ids[-1][0] if ids else None
        if chat is None:
            time.sleep(3)
    if chat is None:
        print("\nNo message arrived. Press START in your bot, then run the setup again.")
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Telegram settings for the live watcher. Keep this file private.\n"
                f"TELEGRAM_BOT_TOKEN={token}\nTELEGRAM_CHAT_ID={chat}\n")
    ok, err = telegram("✅ Crypto Signal Agent: Telegram works. Live alerts will arrive here.", token, chat)
    print(f"\nSaved. Chat id {chat}. " + ("Test message sent - check Telegram." if ok else f"Test message NOT sent: {err}"))
    return ok


def setup_github(path=SETTINGS_FILE, ask=input, sync=None):
    """Interactive: a fine-grained GitHub token for the journal sync -> checked by a real upload -> telegram.env."""
    print("\nJOURNAL SYNC SETUP (optional) - your Telegram button choices and results go to GitHub, so the agent can\n"
          "learn from your own trades. Guide: docs/WINDOWS_WATCHER.md, 'Journal sync'.\n"
          "1. Open https://github.com/settings/personal-access-tokens/new (signed in to GitHub).\n"
          "2. Name: crypto journal · Expiration: 1 year · Repository access: Only select repositories -> "
          f"{REPO}\n3. Permissions -> Repository permissions -> Contents: Read and write. Nothing else.\n"
          "4. Generate token, copy it (it starts with github_pat_).\n")
    token = ask("Paste the token here and press Enter: ").strip()
    if not token:
        print("No token - nothing changed.")
        return False
    old = os.environ.get("JOURNAL_GITHUB_TOKEN")
    os.environ["JOURNAL_GITHUB_TOKEN"] = token
    ok, note = (sync or JournalSync(JOURNAL)).push(int(time.time() * 1000), force=True)
    if not ok:
        if old is None:
            os.environ.pop("JOURNAL_GITHUB_TOKEN", None)
        else:
            os.environ["JOURNAL_GITHUB_TOKEN"] = old
        print(f"\nThe upload did not work: {note}\nCheck the repository and the Contents: Read and write permission, "
              "then run this again. Nothing was saved.")
        return False
    try:
        with open(path, encoding="utf-8") as f:
            keep = [x for x in f.read().splitlines() if not x.strip().startswith("JOURNAL_GITHUB_TOKEN=")]
    except OSError:
        keep = []
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(keep + [f"JOURNAL_GITHUB_TOKEN={token}"]) + "\n")
    print(f"\nWorks: your journal is on GitHub (branch '{JOURNAL_BRANCH}', {note}). Token saved in telegram.env "
          "(private, never uploaded).\nRestart the watcher (2_start_watcher.bat) so it uses it.")
    return True


def main():
    for stream in (sys.stdout, sys.stderr):           # Windows consoles: never crash on an emoji or a coin name
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    load_settings()
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--once", action="store_true", help="one pass at the newest candle close, then stop")
    ap.add_argument("--send", action="store_true", help="with --once: send the alerts to Telegram")
    ap.add_argument("--test-telegram", action="store_true", help="send one test message")
    ap.add_argument("--find-chat-id", action="store_true", help="show your Telegram chat id (message the bot first)")
    ap.add_argument("--setup-telegram", action="store_true", help="interactive Telegram setup (writes telegram.env)")
    ap.add_argument("--setup-github", action="store_true",
                    help="journal sync: save a GitHub token so your trades reach the research (optional)")
    ap.add_argument("--sync", action="store_true", help="download GitHub's newest decision files now (no git)")
    ap.add_argument("--status", action="store_true", help="show which strategies may alert, then stop")
    ap.add_argument("--offline", action="store_true", help="synthetic prices (code test, no internet)")
    ap.add_argument("--no-git", action="store_true", help="do not git pull every hour")
    ap.add_argument("--also", action="append", default=[], metavar="STATUS",
                    help="code test only: also watch strategies with this status (e.g. BACKTESTING), labelled CHECK")
    ap.add_argument("--replay", type=int, default=None, metavar="DAYS",
                    help="the Signal Center's safety check: replay the last DAYS days with the TEST alert rules")
    args = ap.parse_args()
    if args.setup_telegram:
        sys.exit(0 if setup_telegram() else 1)
    if args.setup_github:
        sys.exit(0 if setup_github() else 1)
    if args.sync:
        updated, problems = sync_files()
        print("updated: " + (", ".join(updated) or "nothing new") + ("" if not problems else "\nproblems: " + "; ".join(problems)))
        return
    if args.find_chat_id:
        ids = find_chat_ids()
        print("\n".join(f"chat id {i}  ({name})" for i, name in ids) if ids else
              "No messages yet: open your bot in Telegram, press Start / send it 'hi', then run this again.")
        return
    if args.test_telegram:
        ok, err = telegram("✅ Crypto Signal Agent: Telegram works. Live alerts will arrive here.")
        print("sent" if ok else f"NOT sent: {err}")
        sys.exit(0 if ok else 1)
    feed = SyntheticSwap() if args.offline else OKXSwap()
    w = Watcher(feed, send=args.send or not args.once, git=not (args.no_git or args.offline or args.once),
                also=args.also)
    if args.status:
        return
    if args.replay:
        print(replay_text(replay(w, args.replay)))
        return
    if args.once:
        now = w.now_fn()
        b = lv.boundary(now)
        alerts = w.tick(now)
        print(f"{len(alerts)} alert(s) at the {lv.bj(b - 1)} close")
        return
    w.run()


if __name__ == "__main__":
    main()
