"""
Live watcher helpers (operator request 2026-10-05: scalping alerts within seconds of a candle close).

The hourly GitHub scan stays the official record (signals log, emails, risk book). The live watcher
(live_watcher.py, on an always-on server) evaluates the SAME strategy cards with the SAME engine code at every
5-minute candle close and sends a Telegram alert at once. These are the pure parts: settings, which timeframes
closed, which strategy versions may alert, the alert text and the duplicate guard. No internet, no files.
"""
import datetime as dt
import html

from engine import timeframes as tfm

DEFAULTS = dict(
    stages={"APPROVED": "LIVE", "PAPER_TRADING": "PAPER"},   # strategy status -> alert label (others: no alert)
    bars=500,                 # candles kept per timeframe (indicators warm up in 250)
    entry_zone_r=0.2,         # entry zone = planned entry +- 0.2R (the 5m protocol's zone)
    poll_delay_s=8,           # wait this long after a candle close (the exchange finalises the candle)
    refresh_minutes=60,       # git pull + newest engine files + strategy statuses, this often
    cooldown_minutes=60,      # the same coin + direction + strategy + timeframe alerts at most once per hour
    heartbeat_utc="00:05",    # one "still running" message a day
    error_alert_after=3,      # Telegram alert after this many failed passes in a row
)
CLOSE_ORDER = ["5m", "15m", "30m", "1h", "4h", "1d", "1w"]


def settings(section):
    s = dict(DEFAULTS)
    s.update({k: v for k, v in (section or {}).items() if k in DEFAULTS})
    s["stages"] = dict(s["stages"] or {})
    return s


def boundary(now_ms, tf="5m"):
    """The newest candle boundary (open time of the candle now forming) for tf."""
    return now_ms // tfm.TF_MS[tf] * tfm.TF_MS[tf]


def closed_at(boundary_ms):
    """Intraday timeframes whose candle closed exactly at boundary_ms (1d / 1w are refreshed separately)."""
    return [tf for tf in CLOSE_ORDER[:5] if boundary_ms % tfm.TF_MS[tf] == 0]


def alert_label(status, lab, S):
    """'LIVE' / 'PAPER' / None for a strategy version x timeframe with this registry status. A lab card is never
    LIVE (the operator moves it into strategies.yaml first) - it alerts as PAPER at most."""
    if lab and status == "APPROVED":
        status = "PAPER_TRADING"
    return S["stages"].get(status)


def dedupe_key(coin, d, strategy, version, tf):
    return f"{coin}|{d}|{strategy}@{version}|{tf}"


def allowed(sent, key, now_ms, S):
    """True when this key has not alerted within the cooldown."""
    last = sent.get(key)
    return last is None or now_ms - int(last) >= int(S["cooldown_minutes"]) * 60_000


def fmt_px(x, ref=None):
    """A price with the decimals of its size - or of ref (the entry), so every price of one alert matches."""
    if x is None or x != x:
        return "-"
    a = abs(ref if ref else x)
    return f"{x:,.2f}" if a >= 100 else (f"{x:,.4f}" if a >= 1 else f"{x:.6f}")


def utc(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime("%H:%M UTC")


def hold_text(tf, bars):
    if not bars:
        return "-"
    mins = tfm.TF_MS[tf] // 60_000 * int(bars)
    return f"{int(bars)} candles (~{mins // 60}h{mins % 60:02d}m)" if mins >= 60 else f"{int(bars)} candles (~{mins}m)"


LABEL_ICON = {"LIVE": "🟢", "PAPER": "🟡", "TEST": "🔵"}
LABEL_NOTE = {
    "PAPER": "🟡 PAPER = practice only: this strategy passed the backtest and is being proven on paper.",
    "TEST": "🔵 TEST = a setup of a strategy that was positive on this coin in the 5-year backtest. Not proven live "
            "yet - watch it or take it as a demo trade (✅ Took it): it never counts in your loss limits.",
    "CHECK": "🧪 CHECK = code test of the watcher - NOT a trade signal.",
}
SEP = "━━━━━━━━━━━━━━"
BJ = dt.timezone(dt.timedelta(hours=8))


def bj(ms):
    return dt.datetime.fromtimestamp(ms / 1000, BJ).strftime("%H:%M Beijing")


def _usd(x):
    return f"${x:,.2f}" if abs(x) < 1000 else f"${x:,.0f}"


def message(a):
    """Telegram text (HTML) of one alert (Forward Test Program layout, 2026-10-09). a = dict(label, coin, inst, d, tf,
    strategy, version, entry, R, tps, split, zone_r, size, risk_pct, max_hold, regimes, close_ms, sent_ms, confirm,
    valid_bars, warnings; TEST alerts also: test (backtest on this coin), program, also, agree, against, weather,
    market)."""
    side = "LONG" if a["d"] == 1 else "SHORT"
    lab = a["label"]
    stop = a["entry"] - a["d"] * a["R"]
    pct = abs(stop / a["entry"] - 1) * 100
    z = a.get("size") or {}
    risk = float(z.get("risk_usdt") or 0)
    prog = a.get("program") or {}
    name = (f"{prog['name']} · {prog['version']}" if prog.get("name") else f"{a['strategy']} v{a['version']}")
    lines = [f"{LABEL_ICON.get(lab, '🧪')} <b>{lab} · {side} {a['coin']}</b> · {a['tf'].upper()}"
             + (" ⭐" if a.get("agree") else "") + f" · {a.get('inst') or a['coin']}",
             name + (f" ({a['strategy']})" if prog.get("name") else "")]
    if a.get("agree"):
        lines.append("⭐ Same direction on: " + ", ".join(a["agree"]))
    lines.append(SEP)
    lim = a.get("limit_bars")
    if lim:                                  # roadmap step 2B: a limit-entry strategy
        until = a["close_ms"] + 1 + int(lim) * tfm.TF_MS[a["tf"]]
        lines.append(f"Entry: <b>{'BUY' if a['d'] == 1 else 'SELL'} LIMIT {fmt_px(a['entry'])}</b> · cancel at "
                     f"{utc(until)} if not filled ({int(lim)} {a['tf']} candles)")
    else:
        zlo, zhi = sorted((a["entry"] - a["zone_r"] * a["R"], a["entry"] + a["zone_r"] * a["R"]))
        lines.append(f"Entry: <b>{fmt_px(a['entry'])}</b> (zone {fmt_px(zlo, a['entry'])} – {fmt_px(zhi, a['entry'])})")
    lines.append(f"Stop: <b>{fmt_px(stop, a['entry'])}</b> ({pct:.2f}% away)" + (f" · −{_usd(risk)}" if risk else ""))
    for i, tp in enumerate(a["tps"]):
        share = a["split"][i] if a.get("split") and i < len(a["split"]) else None
        r_mult = a["d"] * (tp - a["entry"]) / a["R"]
        money = f" · +{_usd(r_mult * risk * share)} on the {share * 100:.0f}% closed" if risk and share else \
            (f" · +{_usd(r_mult * risk)}" if risk else "")
        lines.append(f"TP{i + 1}: <b>{fmt_px(tp, a['entry'])}</b> ({r_mult:.1f}R){money}")
    lines.append(SEP)
    if z.get("qty"):
        cap_note = " (capped by max leverage)" if z.get("capped") else ""
        lines.append(f"Size: {z['qty']:.6g} {a['coin']} ≈ <b>{_usd(z['notional'])}</b> · "
                     f"margin {_usd(z['notional'] / 3)} at 3x{cap_note}")
        acct = risk / (float(a["risk_pct"]) / 100) if a.get("risk_pct") else None
        lines.append(f"Risk: <b>{_usd(risk)}</b> ({a['risk_pct']:g}%" + (f" of {_usd(acct)})" if acct else ")"))
    t = a.get("test") or a.get("past")
    if t and t.get("n"):
        lines.append(f"Past: {a['coin']} won {t['win_rate']:.0f}% of {t['n']} backtest trades · "
                     f"{t['avg_r']:+.2f}R a trade after fees")
    if a.get("weather"):
        lines.append(f"Market: {a['weather']}")
    if a.get("regimes"):
        lines.append("Trend: " + " · ".join(f"{k.upper()} {v}" for k, v in a["regimes"].items()))
    if a.get("against"):
        lines.append(f"⚠️ Against the daily trend ({a['against']}) - context only, it does not block")
    if a.get("confirm"):
        lines.append(f"5m check: ✓ {a['confirm']}")
    lines.append(f"Max hold: {hold_text(a['tf'], a.get('max_hold'))}")
    man = a.get("manage") or {}
    if man:                                  # step 3 / the program's V4: trade management after TP1
        after = "stop to entry + fees" if man.get("be_plus_fees") else "stop to entry"
        if (man.get("trail") or {}).get("atr_n"):
            tr = man["trail"]
            after += (f", trail the rest {tr['atr_x']:g} ATR behind the highest high / lowest low of the last "
                      f"{tr['atr_n']} {a['tf']} candles")
        elif man.get("trail"):
            after += f", trail the rest behind the last {a['tf']} swing / EMA{man['trail']['ema']}"
        lines.append(f"After TP1: {after}")
        if man.get("progress"):
            pg = man["progress"]
            lines.append(f"Time stop: exit at market if +{pg['r']:g}R is not reached within {pg['bars']} {a['tf']} "
                         f"candles ({hold_text(a['tf'], pg['bars']).split('(~')[-1].rstrip(')')})")
        iv = man.get("invalidate")
        if iv and a.get("inval") is not None:
            lines.append(f"Invalidation: exit on a {iv.get('every') or a['tf']} close "
                         f"{'below' if a['d'] == 1 else 'above'} {fmt_px(a['inval'], a['entry'])}")
    for w in a.get("why") or []:
        lines.append(f"• {w}")
    if a.get("max_isolated_leverage"):            # step 3: the operator's playbook (6.1)
        lines.append(f"Isolated margin, leverage at most {a['max_isolated_leverage']}x (liquidation >= 2x the stop "
                     "distance beyond the stop)")
    for w in a.get("size_note") or []:
        lines.append(f"½ {w}")
    for w in a.get("warnings") or []:
        lines.append(f"⚠️ {w}")
    lines.append(SEP)
    if LABEL_NOTE.get(lab):
        lines.append(f"<i>{LABEL_NOTE[lab]}</i>")
    lines += ["No fill = no trade. Skip it if price reaches TP1 before your order fills." if lim else
              f"Valid for {a.get('valid_bars', 2)} {a['tf']} candles. Skip it if price reaches the stop or TP1 first.",
              f"Candle closed {utc(a['close_ms'] + 1)} ({bj(a['close_ms'] + 1)}) · sent {utc(a['sent_ms'])}",
              "<i>Signal only - not financial advice. You place the order yourself.</i>"]
    return "\n".join(lines)


def details_text(a, card):
    """The ℹ️ Details reply: what the strategy looks for, its rules, why it should work, when it fails, and the
    backtest on this coin. card: the strategy card (or None when it is no longer loaded)."""
    side = "long" if a["d"] == 1 else "short"
    prog = (card or {}).get("program") or a.get("program") or {}
    out = [f"ℹ️ <b>{prog.get('name') or a['strategy']}</b>" + (f" · {prog['version']}" if prog.get("version") else ""),
           f"{a['strategy']} v{a.get('version')} · {a['tf']} · {a['coin']} {side.upper()}"]
    if card:
        out += ["", html.escape(" ".join(str(card.get("description") or card.get("hypothesis") or "").split()))]
        rules = card.get(side) or []
        if rules:
            out += ["", f"<b>Rules ({side}, all true on a closed candle)</b>"]
            out += [f"• <code>{html.escape(str(r))}</code>" for r in rules]
        gate = card.get("gate")
        if gate in ("intraday", "intraday_reversal"):
            out.append("• market gate: " + ("4H and 1H trend the same way" if gate == "intraday" else
                                            "its range regimes, never against a strong 4H trend")
                       + " (1W / 1D are context only)")
        e = card.get("edge") or {}
        if e.get("mechanism"):
            out += ["", f"<b>Why it can work:</b> {html.escape(str(e['mechanism']))}"]
        if e.get("fails_when"):
            out.append(f"<b>When it fails:</b> {html.escape(str(e['fails_when']))}")
    t = a.get("test") or a.get("past")
    if t and t.get("n"):
        out += ["", f"<b>Backtest on {a['coin']}</b> (5 years, after fees): {t['n']} trades, {t['win_rate']:.0f}% won, "
                    f"{t['avg_r']:+.2f}R a trade"
                + (f", unseen last part {t['test_avg_r']:+.2f}R" if t.get("test_avg_r") is not None else "")]
    if a.get("market"):
        out.append(f"Market at the alert: {a['market']}")
    if a["label"] == "TEST":
        out += ["", "TEST alerts are tracked on GitHub too. The weekly review promotes a strategy to 🟡 PAPER only "
                    "after enough live TEST trades stay positive after fees - and only with your tap."]
    return "\n".join(out)


# ---------------------------------------------------------------- Telegram commands and buttons (roadmap step 4)
CHOICES = {"took": "✅ Took it", "skip": "❌ Skip"}
INFO = {"text": "ℹ️ Details", "callback_data": "info|{aid}"}


def choice_buttons(aid, choice=None):
    """The buttons under an alert. choice: None / 'took' / 'skip' (can still be changed) / 'closed' / 'done'.
    ℹ️ Details is always there."""
    info = [{"text": INFO["text"], "callback_data": INFO["callback_data"].format(aid=aid)}]
    if choice in ("closed", "done"):
        return {"inline_keyboard": [[{"text": "🏁 Trade finished" if choice == "done" else "🏁 You closed it",
                                      "callback_data": f"noop|{aid}"}], info]}
    row = [{"text": label + (" ✓" if choice == key else ""), "callback_data": f"{key}|{aid}"}
           for key, label in CHOICES.items()]
    rows = [row]
    if choice == "took":
        rows.append([{"text": "🏁 I closed it", "callback_data": f"closed|{aid}"}])
    rows.append(info)
    return {"inline_keyboard": rows}


def parse_command(text):
    """'/Pause@my_bot 2h' -> ('pause', '2h'); not a command -> (None, text)."""
    text = (text or "").strip()
    if not text.startswith("/"):
        return None, text
    head, _, arg = text.partition(" ")
    return head[1:].split("@")[0].lower(), arg.strip()


def parse_duration(arg):
    """'2' / '2h' / '90m' -> milliseconds; '' -> None (until /resume); unreadable -> ValueError."""
    arg = (arg or "").strip().lower()
    if not arg:
        return None
    unit = 60_000 if arg.endswith("m") else 3_600_000
    num = float(arg.rstrip("hm").strip())
    if not 0 < num * unit <= 7 * 86_400_000:
        raise ValueError(arg)
    return int(num * unit)


HELP = ("🤖 <b>Crypto watcher commands</b>\n"
        "/status - is it running, what it watches, the last check\n"
        "/trades - the trades you took (open ones are followed) and your results\n"
        "/result 1.2 - your real result of the last finished trade, in R after fees (-1 = full stop lost)\n"
        "/weather - what kind of market day it is (trend, range or choppy), the usual 24h move, crowding, events\n"
        "/tests on · /tests off - 🔵 TEST alerts (strategies positive in the 5-year backtest) on or off\n"
        "/pause - stop new trade alerts until /resume (/pause 2h = for 2 hours)\n"
        "/resume - new trade alerts on again\n"
        "/help - this list\n\n"
        "Under each alert: <b>✅ Took it</b> = I follow the trade and tell you when TP1 / TP2, the stop or the time "
        "stop is reached (same rules as the backtests; a 🔵 TEST trade goes to the demo book, never your loss limits). "
        "<b>❌ Skip</b> = only recorded. <b>ℹ️ Details</b> = the strategy, its rules and its backtest. "
        "<b>🏁 I closed it</b> = stop following.\n"
        "Pausing never stops the messages about trades you already took.")


def weather_text(w, now_ms):
    """/weather reply from reports/market_weather.json (GitHub's hourly scan, downloaded every hour). Upgrade 10."""
    if not w or not w.get("telegram"):
        return ("🌫 No market weather yet. GitHub's hourly scan writes it and the watcher downloads it every hour - "
                "try again later.")
    try:
        made = int(dt.datetime.strptime(w["utc"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc).timestamp() * 1000)
    except (KeyError, TypeError, ValueError):
        return w["telegram"]
    age = f"\nMade by GitHub's hourly scan {ago(made, now_ms)}."
    if now_ms - made > 3 * 3_600_000:
        age += " ⚠️ Older than 3 hours - the scan or the download may be late."
    return w["telegram"] + age


def ago(ms, now_ms):
    mins = max(0, (now_ms - ms) // 60_000)
    return f"{mins}m ago" if mins < 60 else f"{mins // 60}h{mins % 60:02d}m ago"


def status_text(i):
    """/status reply. i = dict(feed, started_ms, now_ms, last_tick=(ms, ok, note) or None, paused_until (0 = on,
    -1 = until /resume, else ms), watch=[(id, tf, label)], coins, open_trades, alerts_today, refresh=(ms, note) or
    None, code_old=[...], journal_sync=text or None)."""
    now = i["now_ms"]
    lines = [f"✅ <b>Live watcher running</b> · {i['feed']}", f"Started {ago(i['started_ms'], now)}"]
    lt = i.get("last_tick")
    lines.append("Last market check: waiting for the first 5m candle close" if not lt else
                 f"Last market check: {utc(lt[0])} ({ago(lt[0], now)}) " + ("✓" if lt[1] else f"⚠️ failed: {lt[2]}"))
    p = i.get("paused_until") or 0
    lines.append("New trade alerts: ON" if p == 0 or (p > 0 and p <= now) else
                 "⏸ New trade alerts: PAUSED until /resume" if p < 0 else
                 f"⏸ New trade alerts: PAUSED until {utc(p)} (/resume to switch on now)")
    real = [w for w in i["watch"] if w[2] != "TEST"]
    tests = [w for w in i["watch"] if w[2] == "TEST"]
    if tests or "tests_on" in i:
        lines.append(f"🔵 TEST alerts: {'ON' if i.get('tests_on', True) else 'OFF (/tests on)'} · "
                     f"{len(tests)} backtest-positive strategy timeframe(s) on their positive coins"
                     + (f" · {i['tests_today']} sent today (max {i['tests_max']})" if "tests_today" in i else ""))
    if real:
        lines.append(f"Watching {len(real)} strategy timeframe(s):")
        lines += [f"• {sid} {tf} ({lab})" for sid, tf, lab in real]
    elif tests:
        lines.append("LIVE / PAPER: none yet - the weekly review promotes the best TEST strategies to PAPER.")
    else:
        lines.append("Watching 0 strategies: none is PAPER_TRADING or APPROVED yet. GitHub's daily research "
                     "promotes them; the watcher picks them up within an hour.")
    lines.append("Coins: " + ", ".join(i["coins"]))
    lines.append(f"Trades you took, being followed: {i['open_trades']}" + (" (/trades)" if i["open_trades"] else ""))
    lines.append(f"Trade alerts sent today (UTC): {i['alerts_today']}")
    if i.get("refresh"):
        lines.append(f"GitHub decisions refreshed {ago(i['refresh'][0], now)}: {i['refresh'][1]}")
    if i.get("journal_sync"):
        lines.append(f"Journal sync to GitHub: {i['journal_sync']}")
    if i.get("code_old"):
        lines.append("🔄 A newer watcher version is on GitHub: double-click windows\\4_update.bat on the PC.")
    return "\n".join(lines)
