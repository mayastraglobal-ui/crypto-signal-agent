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

While it runs, the bot answers the operator's commands (/status, /trades, /pause, /resume, /help) and the buttons
under each alert: "✅ Took it" makes the watcher follow that trade and say when TP1 / TP2, the stop or the time stop
is reached (engine/follow.py: the backtests' rules); every choice and result is written to journal/my_trades.csv.
Only the chat in TELEGRAM_CHAT_ID is answered.

Telegram settings come from the environment (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID) or from the file telegram.env
next to this script (python live_watcher.py --setup-telegram writes it). Never put them in the repository.
Without git (a Windows PC with the ZIP download, docs/WINDOWS_WATCHER.md), GitHub's newest decisions are downloaded
directly every hour (sync_files).
"""
import argparse
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
from engine import lifecycle as lc
from engine import live as lv
from engine import regime_fit as rfit
from engine import scalp_playbook as spb
from engine import manage as mg
from engine import risk as rk
from engine import strategy_spec as sspec

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)     # the scanner's feature tables
ROOT = sc.ROOT
STATE = os.path.join(ROOT, "reports", "live_watcher_state.json")     # local only (.gitignore)
SETTINGS_FILE = os.path.join(ROOT, "telegram.env")                  # local only (.gitignore): bot token + chat id
LOG_FILE = os.path.join(ROOT, "logs", "live_watcher.log")           # local only (.gitignore)
JOURNAL = os.path.join(ROOT, "journal", "my_trades.csv")            # local only (.gitignore): took / skipped / results
JOURNAL_COLS = ["time_utc", "alert_id", "event", "label", "coin", "side", "tf", "strategy", "version", "entry", "stop",
                "tp1", "tp2", "tp3", "price", "result_r"]
DATA_TFS = ["1w", "1d", "4h", "1h", "30m", "15m", "5m"]
REPO = os.environ.get("CRYPTO_AGENT_REPO", "mayastraglobal-ui/crypto-signal-agent")
RAW = "https://raw.githubusercontent.com/{repo}/{branch}/{path}"
# Without git (a Windows PC with the ZIP download): the files that carry GitHub's decisions, fetched every hour
SYNC_FILES = [("main", "config.yaml"), ("main", "events.yaml"), ("main", "strategies.yaml"),
              ("main", "strategies_lab.yaml"), ("main", "memory/strategy_registry.csv"),
              ("main", "reports/universe.json"), ("main", "reports/regime_fit.json"),
              ("live-reports", "reports/derivs_hourly.csv.gz"), ("live-reports", "reports/funding.csv.gz")]
CODE_FILES = ["live_watcher.py", "scanner.py", "engine/live.py", "engine/follow.py", "engine/scalp_playbook.py",
              "engine/manage.py", "engine/flow_history.py", "engine/trend4h.py", "engine/regime_fit.py"]      # changed on GitHub -> "run update.bat"


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


def sync_files(root=ROOT, repo=REPO, get=None):
    """No git: download GitHub's newest decision files (statuses, coins, cards, settings, futures data).
    Returns (updated paths, problems). Each file is written only when it downloaded completely and looks valid."""
    get = get or (lambda url: requests.get(url, timeout=60))
    updated, problems = [], []
    for branch, path in SYNC_FILES:
        try:
            r = get(RAW.format(repo=repo, branch=branch, path=path))
            data = r.content if r.status_code == 200 else None
        except requests.RequestException as e:
            problems.append(f"{path}: {e.__class__.__name__}")
            continue
        if not _valid(path, data):
            problems.append(f"{path}: not downloaded (HTTP {getattr(r, 'status_code', '?')})")
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
        self.reload()

    # ---- configuration, strategy statuses, coins ----
    def reload(self):
        self.cfg = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
        self.S = lv.settings(self.cfg.get("live_watcher"))
        for st in self.also:                                        # --also: a code test only, labelled TEST
            self.S["stages"].setdefault(st, "TEST")
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

    # ---- local state (duplicate guard, heartbeat) ----
    def _load_state(self):
        try:
            st = json.load(open(STATE))
        except (OSError, ValueError):
            st = {}
        # alerts: the buttons' memory (3 days) · trades: the ones being followed · paused_until: 0 = alerts on,
        # -1 = until /resume, else the end (ms) · tg_offset: the next Telegram update to read
        for k, v in dict(sent={}, heartbeat=None, alerts={}, trades={}, results=[], paused_until=0, tg_offset=None,
                         next_id=0).items():
            st.setdefault(k, v)
        return st

    def _save_state(self):
        now = self.now_fn()
        cut = now - 2 * 86_400_000                                   # the duplicate guard needs hours, not weeks
        self.state["sent"] = {k: v for k, v in self.state["sent"].items() if int(v) >= cut}
        self.state["alerts"] = {k: a for k, a in self.state["alerts"].items()
                                if k in self.state["trades"] or int(a["sent_ms"]) >= now - 3 * 86_400_000}
        self.state["results"] = self.state["results"][-200:]
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
        for a in alerts:
            what = f"ALERT {a['label']} {a['coin']} {a['tf']} {a['strategy']}: "
            if self.send and self.paused(now_ms):
                log(what + "alerts are paused (/resume) - not sent")
                continue
            aid = self._remember(a)
            ok, err, mid = self.say(lv.message(a), lv.choice_buttons(aid))
            self.state["alerts"][aid]["msg_id"] = mid
            if self.send:
                log(what + ("sent" if ok else f"NOT sent ({err})"))

    def _remember(self, a):
        """Keep what the buttons and the follow-up need; returns the alert id (in the buttons' data)."""
        self.state["next_id"] = int(self.state["next_id"]) + 1
        aid = f"{int(a['sent_ms']) // 1000:x}{self.state['next_id'] % 1000:03d}"
        self.state["alerts"][aid] = dict({k: a.get(k) for k in ("label", "coin", "inst", "d", "tf", "strategy",
                                          "version", "entry", "R", "tps", "split", "max_hold", "close_ms", "sent_ms",
                                          "limit_bars", "manage", "inval", "be_frac")},
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
    def follow(self, now_ms):
        for tid, t in list(self.state["trades"].items()):
            try:
                raw = self.update(t["coin"], "5m", now_ms)
            except Exception as e:
                log(f"follow {t['coin']}: download failed: {e}")
                continue
            closed = raw[raw["close_time"] < now_ms]
            if t.get("trailing") and len(closed):    # step 3: the playbook's trail (last 5m swing / EMA9)
                tc = t.get("trail_cfg") or {}
                tl, ts = mg.trail_levels(closed["high"].to_numpy(), closed["low"].to_numpy(), closed["close"].to_numpy(),
                                         int(tc.get("swing_n", 3)), int(tc.get("ema", 9)))
                closed = closed.assign(trail_long=tl, trail_short=ts)
            bars = closed[closed["open_time"] >= t["checked_ms"]].to_dict("records")
            for ev in fl.step(t, bars):
                self.say(fl.text(t, ev))
                name = f"tp{ev['n']}" if ev["kind"] == "tp" else ev["kind"]
                self.journal(t, name, ev["at_ms"], ev["px"], ev.get("result_r") if ev.get("final") else None)
                log(f"FOLLOW {t['coin']} {t['tf']} {t['strategy']}: {name}")
            if t["closed"]:
                filled = t.get("filled", True)
                self._end_trade(tid, "done", now_ms, t["realized"] if filled else None,
                                "finished" if filled else "limit not filled")

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
            return ("⏸ New trade alerts paused " + ("until /resume." if dur is None else f"until {lv.utc(now_ms + dur)}.")
                    + "\nYou still get the messages about trades you took and the daily 'running' message.")
        if cmd == "resume":
            self.state["paused_until"] = 0
            self._save_state()
            return "▶️ New trade alerts are on again."
        if cmd is None:
            return "I only understand commands. Send /help for the list."
        return f"I don't know /{cmd}. Send /help for the list."

    def on_button(self, cq, now_ms):
        action, _, aid = (cq.get("data") or "").partition("|")
        a = self.state["alerts"].get(aid)
        toast = ""
        if a is None:
            toast = "This alert is too old (buttons work for 3 days)."
        elif a.get("choice") in ("closed", "done") or action == "noop":
            toast = "This trade is already finished."
        elif action == "took" and a.get("choice") != "took":
            a["choice"] = "took"
            self.state["trades"][aid] = fl.open_trade(a, aid, now_ms, self.cfg.get("trade_plan"))
            self.journal(dict(a, id=aid), "took", now_ms)
            toast = "Recorded: you took it. I'll follow this trade."
            self.say(f"👀 Following your {'LONG' if a['d'] == 1 else 'SHORT'} {a['coin']} ({a['tf']} {a['strategy']}). "
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
        msg = cq.get("message") or {}
        if self.send:
            tg_api("answerCallbackQuery", dict(callback_query_id=cq.get("id"), text=toast))
        if a is not None and msg.get("message_id") and self.send:
            tg_api("editMessageReplyMarkup", dict(chat_id=msg["chat"]["id"], message_id=msg["message_id"],
                                                  reply_markup=lv.choice_buttons(aid, a.get("choice"))))
        self._save_state()
        return toast

    def status_text(self, now_ms):
        day = lv.boundary(now_ms, "1d")
        return lv.status_text(dict(
            feed=self.feed.name, started_ms=self.started_ms, now_ms=now_ms, last_tick=self.last_tick,
            paused_until=self.state.get("paused_until"), watch=[(s["id"], tf, lab) for s, tf, lab in self.watch],
            coins=self.coins, open_trades=len(self.state["trades"]),
            alerts_today=sum(1 for a in self.state["alerts"].values() if int(a["sent_ms"]) >= day),
            refresh=self.last_refresh, code_old=self.code_old))

    def trades_text(self, now_ms):
        lines = ["📒 <b>Your trades</b>"]
        if self.state["trades"]:
            lines.append("Being followed:")
            lines += [fl.summary(t) for t in self.state["trades"].values()]
        else:
            lines.append("No trade is being followed. Press ✅ Took it under an alert and I'll follow it.")
        res = [r for r in self.state["results"] if int(r["ended_ms"]) >= now_ms - 30 * 86_400_000]
        if res:
            known = [r["r"] for r in res if r["r"] is not None]
            lines.append(f"\nLast 30 days: {len(res)} finished" + (
                f" · {sum(1 for r in known if r > 0)} won · total about {sum(known):+.1f}R before fees" if known else ""))
            for r in res[-5:]:
                when = dt.datetime.fromtimestamp(int(r["ended_ms"]) / 1000, dt.timezone.utc)
                lines.append(f"• {when:%d %b} {'LONG' if r['d'] == 1 else 'SHORT'} {r['coin']} {r['tf']} ({r['label']}): "
                             + (f"{r['r']:+.1f}R" if r["r"] is not None else r["how"]))
        lines.append("\nFull record on the PC: journal\\my_trades.csv")
        return "\n".join(lines)

    def _good(self, coin, tf, quality):
        for t in (tf, sc.HTF.get(tf)):
            r = quality.get((coin, t))
            if t and (r is None or r["state"] != dq.GOOD):
                return False
        return True

    def signals(self, coin, pc, quality, b, closed, now_ms):
        out = []
        for s, tf, label in self.watch:
            fr = pc["frames"].get(tf)
            if tf not in closed or fr is None or not self._good(coin, tf, quality):
                continue
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
            key = lv.dedupe_key(coin, d, s["id"], s["version"], tf)
            if not lv.allowed(self.state["sent"], key, now_ms, self.S) or any(p["key"] == key for p in self.pending):
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
            if s.get("confirm_5m"):
                self.pending.append(dict(base, after_ms=b, coin=coin))
                log(f"{coin} {tf} {s['id']}: trigger - waiting for the 5m confirmation")
                continue
            out.append(self._finish(base, now_ms))
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
                         confirm=f"CONFIRMED on the {lv.utc(int(m5['close_time'][j]) + 1)} 5m bar close"
                         + (f" ({', '.join(res['smc'])})" if res["smc"] else ""))
                a["tps"] = [a["entry"] + (tp - p["entry"]) for tp in p["tps"]]   # same distances from the 5m entry
                out.append(self._finish(a, now_ms))
            else:
                log(f"{coin} {p['tf']} {p['strategy']}: 5m {res['state']} - {res['why']}")
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
        res = sorted(self.state.get("results") or [], key=lambda r: int(r["ended_ms"]))
        took_today = sum(1 for a in self.state["alerts"].values() if a.get("choice") in ("took", "closed", "done")
                         and int(a["sent_ms"]) >= day)
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
    def heartbeat(self, now_ms):
        day = dt.datetime.fromtimestamp(now_ms / 1000, dt.timezone.utc)
        if day.strftime("%H:%M") < self.S["heartbeat_utc"] or self.state.get("heartbeat") == day.strftime("%Y-%m-%d"):
            return
        self.state["heartbeat"] = day.strftime("%Y-%m-%d")
        n = {lab: sum(1 for _, _, l in self.watch if l == lab) for lab in ("LIVE", "PAPER")}
        telegram(f"✅ Live watcher running · {day:%Y-%m-%d}\nWatching {n['LIVE']} LIVE and {n['PAPER']} PAPER "
                 f"strategy timeframe(s) on {', '.join(self.coins)}."
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
        self.refresh_repo()                          # start from GitHub's newest decisions (a ZIP may be days old)
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
                self.last_tick = (self.now_fn(), True, "")
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
    ap.add_argument("--sync", action="store_true", help="download GitHub's newest decision files now (no git)")
    ap.add_argument("--status", action="store_true", help="show which strategies may alert, then stop")
    ap.add_argument("--offline", action="store_true", help="synthetic prices (code test, no internet)")
    ap.add_argument("--no-git", action="store_true", help="do not git pull every hour")
    ap.add_argument("--also", action="append", default=[], metavar="STATUS",
                    help="code test only: also watch strategies with this status (e.g. BACKTESTING), labelled TEST")
    args = ap.parse_args()
    if args.setup_telegram:
        sys.exit(0 if setup_telegram() else 1)
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
    if args.once:
        now = w.now_fn()
        b = lv.boundary(now)
        alerts = w.tick(now)
        print(f"{len(alerts)} alert(s) at the {lv.utc(b - 1)} close")
        return
    w.run()


if __name__ == "__main__":
    main()
