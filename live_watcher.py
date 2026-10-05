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

Telegram settings come from the environment: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID (never put them in the
repository - the server keeps them in ~/.crypto-agent.env).
"""
import argparse
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
import yaml

import scanner as sc
from engine import confirm5m as c5m
from engine import data_quality as dq
from engine import lifecycle as lc
from engine import live as lv
from engine import risk as rk
from engine import strategy_spec as sspec

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)     # the scanner's feature tables
ROOT = sc.ROOT
STATE = os.path.join(ROOT, "reports", "live_watcher_state.json")     # local only (.gitignore)
DATA_TFS = ["1w", "1d", "4h", "1h", "30m", "15m", "5m"]


def log(*a):
    print(dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%S"), *a, flush=True)


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
def telegram(text, token=None, chat=None, timeout=15):
    """Send one message. Returns (ok, error text)."""
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = chat or os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        return False, "TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set"
    try:
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", timeout=timeout,
                          json=dict(chat_id=chat, text=text[:4000], parse_mode="HTML", disable_web_page_preview=True))
        return (True, "") if r.status_code == 200 else (False, f"HTTP {r.status_code}: {r.text[:200]}")
    except requests.RequestException as e:
        return False, e.__class__.__name__


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
        self.reloaded_ms = self.now_fn()
        log(f"watching {len(self.watch)} strategy timeframe(s) on {', '.join(self.coins)}: "
            + (", ".join(f"{s['id']} {tf} ({lab})" for s, tf, lab in self.watch) or "none yet (nothing is APPROVED "
               "or PAPER_TRADING - the watcher stays quiet until the daily research run promotes a strategy)"))

    def refresh_repo(self):
        """git pull (new statuses, new cards, newest universe) + the newest futures-data files."""
        if not self.git:
            return
        for cmd in (["git", "pull", "--ff-only", "-q"], [sys.executable, "publish_live.py", "--refresh"]):
            try:
                subprocess.run(cmd, cwd=ROOT, timeout=180, capture_output=True, check=False)
            except (OSError, subprocess.TimeoutExpired) as e:
                log(f"refresh: {' '.join(cmd[:2])} failed: {e}")
        self.reload()

    # ---- local state (duplicate guard, heartbeat) ----
    def _load_state(self):
        try:
            return json.load(open(STATE))
        except (OSError, ValueError):
            return dict(sent={}, heartbeat=None, alerts_today={})

    def _save_state(self):
        cut = self.now_fn() - 2 * 86_400_000                         # the duplicate guard needs hours, not weeks
        self.state["sent"] = {k: v for k, v in self.state["sent"].items() if int(v) >= cut}
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
        now_ms = now_ms or self.now_fn()
        b = lv.boundary(now_ms)
        closed = lv.closed_at(b)
        need_tfs = sorted({tf for _, tf, _ in self.watch if tf in closed} | ({"5m"} if self.pending else set()),
                          key=sc.TF_ORDER.index)
        alerts = []
        if not need_tfs:
            return alerts
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
                pc = sc.prepare_coin(sym, coin, data, quality, [t for t in prep if (sym, t) in data], self.cfg,
                                     derivs.get(coin), btc)
            except Exception as e:
                log(f"{coin}: prepare failed: {e}")
                continue
            alerts += self.signals(coin, pc, quality, b, closed, now_ms)
            alerts += self.confirmations(coin, pc, now_ms)
        for a in alerts:
            text = lv.message(a)
            if self.send:
                ok, err = telegram(text)
                log(f"ALERT {a['label']} {a['coin']} {a['tf']} {a['strategy']}: " + ("sent" if ok else f"NOT sent ({err})"))
            else:
                print("\n" + text + "\n", flush=True)
        self._save_state()
        return alerts

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
            plan = sc.plan_trade(s, t, d, entry, atr, cols, self.cfg)
            if plan is None:
                continue
            R, tps, split = plan
            key = lv.dedupe_key(coin, d, s["id"], s["version"], tf)
            if not lv.allowed(self.state["sent"], key, now_ms, self.S) or any(p["key"] == key for p in self.pending):
                continue
            base = dict(label=label, coin=coin, inst=self.feed.inst(coin), d=d, tf=tf, strategy=s["id"],
                        version=s["version"], entry=entry, R=float(R), tps=[float(x) for x in tps], split=split,
                        zone_r=float(self.S["entry_zone_r"]), max_hold=s.get("time_stop_bars"),
                        regimes={k: v["label"] for k, v in pc["recs"].items()}, close_ms=b - 1,
                        valid_bars=int(self.cfg["signals"]["lookback_bars"]), key=key)
            if s.get("confirm_5m"):
                self.pending.append(dict(base, after_ms=b, coin=coin))
                log(f"{coin} {tf} {s['id']}: trigger - waiting for the 5m confirmation")
                continue
            out.append(self._finish(base, now_ms))
        return out

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
        ev = rk.blackout(now_ms, RK["events"], RK["blackout_minutes"])
        if ev:
            warn.append(f"high-impact event within {RK['blackout_minutes']} min ({ev[0][3]}) - the risk rules say NO "
                        "live entry now")
        if self.calendar_problem:
            warn.append(f"event calendar unreadable: {self.calendar_problem}")
        if a["tps"] and a["d"] * (a["tps"][0] - a["entry"]) / a["R"] < float(RK.get("min_tp1_r", 2.0)) - 1e-9:
            warn.append(f"reward to TP1 below {RK.get('min_tp1_r', 2.0):g}R")
        pct = float(self.cfg["account"]["risk_per_trade_pct"])
        size = rk.size(float(self.cfg["account"]["size_usdt"]), pct, a["entry"], stop, float(RK["max_leverage"]))
        self.state["sent"][a["key"]] = now_ms
        return dict(a, size=size, risk_pct=pct, warnings=warn, sent_ms=self.now_fn())

    # ---- forever ----
    def heartbeat(self, now_ms):
        day = dt.datetime.fromtimestamp(now_ms / 1000, dt.timezone.utc)
        if day.strftime("%H:%M") < self.S["heartbeat_utc"] or self.state.get("heartbeat") == day.strftime("%Y-%m-%d"):
            return
        self.state["heartbeat"] = day.strftime("%Y-%m-%d")
        n = {lab: sum(1 for _, _, l in self.watch if l == lab) for lab in ("LIVE", "PAPER")}
        telegram(f"✅ Live watcher running · {day:%Y-%m-%d}\nWatching {n['LIVE']} LIVE and {n['PAPER']} PAPER "
                 f"strategy timeframe(s) on {', '.join(self.coins)}.")
        self._save_state()

    def run(self):
        ok, err = telegram(f"▶️ Live watcher started on {self.feed.name}. Watching {len(self.watch)} strategy "
                           f"timeframe(s) on {', '.join(self.coins)}.") if self.send else (True, "")
        if not ok:
            log(f"Telegram not working: {err}")
        while True:
            now = self.now_fn()
            nxt = lv.boundary(now) + sc.TF_MS["5m"] + int(self.S["poll_delay_s"]) * 1000
            time.sleep(max(1.0, (nxt - now) / 1000))
            try:
                if self.now_fn() - self.reloaded_ms >= int(self.S["refresh_minutes"]) * 60_000:
                    self.refresh_repo()
                self.tick()
                self.heartbeat(self.now_fn())
                if self.fails >= int(self.S["error_alert_after"]):
                    telegram("✅ Live watcher recovered.")
                self.fails = 0
            except Exception as e:
                self.fails += 1
                log(f"pass failed ({self.fails}): {e}\n{traceback.format_exc()}")
                if self.fails == int(self.S["error_alert_after"]):
                    telegram(f"⚠️ Live watcher: {self.fails} passes failed in a row - no alerts until it recovers.\n"
                             f"{type(e).__name__}: {str(e)[:300]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--once", action="store_true", help="one pass at the newest candle close, then stop")
    ap.add_argument("--send", action="store_true", help="with --once: send the alerts to Telegram")
    ap.add_argument("--test-telegram", action="store_true", help="send one test message")
    ap.add_argument("--find-chat-id", action="store_true", help="show your Telegram chat id (message the bot first)")
    ap.add_argument("--status", action="store_true", help="show which strategies may alert, then stop")
    ap.add_argument("--offline", action="store_true", help="synthetic prices (code test, no internet)")
    ap.add_argument("--no-git", action="store_true", help="do not git pull every hour")
    ap.add_argument("--also", action="append", default=[], metavar="STATUS",
                    help="code test only: also watch strategies with this status (e.g. BACKTESTING), labelled TEST")
    args = ap.parse_args()
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
