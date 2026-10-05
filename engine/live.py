"""
Live watcher helpers (operator request 2026-10-05: scalping alerts within seconds of a candle close).

The hourly GitHub scan stays the official record (signals log, emails, risk book). The live watcher
(live_watcher.py, on an always-on server) evaluates the SAME strategy cards with the SAME engine code at every
5-minute candle close and sends a Telegram alert at once. These are the pure parts: settings, which timeframes
closed, which strategy versions may alert, the alert text and the duplicate guard. No internet, no files.
"""
import datetime as dt

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


def message(a):
    """Telegram text (HTML) of one alert. a = dict(label, coin, inst, d, tf, strategy, version, entry, R, tps, split,
    zone_r, size, risk_pct, max_hold, regimes, why, close_ms, sent_ms, confirm, valid_bars, warnings)."""
    side = "LONG" if a["d"] == 1 else "SHORT"
    icon = ("🟢" if a["d"] == 1 else "🔴") if a["label"] == "LIVE" else ("📝" if a["label"] == "PAPER" else "🧪")
    stop = a["entry"] - a["d"] * a["R"]
    zlo, zhi = sorted((a["entry"] - a["zone_r"] * a["R"], a["entry"] + a["zone_r"] * a["R"]))
    pct = abs(stop / a["entry"] - 1) * 100
    head = (f"{icon} <b>{a['label']} {side} {a['coin']}</b> · {a['inst']}\n"
            f"{a['tf']} · {a['strategy']} v{a['version']}"
            + ("" if a["label"] == "LIVE" else "\n<i>PAPER = practice only: this strategy is still being proven</i>"
               if a["label"] == "PAPER" else "\n<i>TEST = code test of the watcher - NOT a trade signal</i>"))
    lines = [head, "",
             f"Entry zone: <b>{fmt_px(zlo, a['entry'])} – {fmt_px(zhi, a['entry'])}</b> (planned {fmt_px(a['entry'])})",
             f"Stop-loss: <b>{fmt_px(stop, a['entry'])}</b> ({pct:.2f}% away = 1R)"]
    for i, tp in enumerate(a["tps"]):
        share = a["split"][i] if a.get("split") and i < len(a["split"]) else None
        lines.append(f"TP{i + 1}: <b>{fmt_px(tp, a['entry'])}</b> ({a['d'] * (tp - a['entry']) / a['R']:.1f}R"
                     + (f", close {share * 100:.0f}%" if share is not None else "") + ")")
    z = a.get("size") or {}
    if z.get("qty"):
        lines.append(f"Size at {a['risk_pct']:g}% risk (${z['risk_usdt']:,.2f}): {z['qty']:.6g} {a['coin']} ≈ "
                     f"${z['notional']:,.0f}, {z['leverage']:.2f}x" + (" (capped by max leverage)" if z.get("capped") else ""))
    lines.append(f"Max hold: {hold_text(a['tf'], a.get('max_hold'))}")
    if a.get("confirm"):
        lines.append(f"5m check: {a['confirm']}")
    if a.get("regimes"):
        lines.append("Trend: " + " · ".join(f"{k.upper()} {v}" for k, v in a["regimes"].items()))
    for w in a.get("why") or []:
        lines.append(f"• {w}")
    for w in a.get("warnings") or []:
        lines.append(f"⚠️ {w}")
    lines += ["",
              f"Valid for {a.get('valid_bars', 2)} {a['tf']} candles. Skip it if price reaches the stop or TP1 first.",
              f"Candle closed {utc(a['close_ms'] + 1)} · sent {utc(a['sent_ms'])}",
              "<i>Signal only - not financial advice. You place the order yourself.</i>"]
    return "\n".join(lines)
