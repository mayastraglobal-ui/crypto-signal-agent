"""
Roadmap upgrade 10 (operator, 2026-10-08): the "market weather" - what kind of day it is, in plain words.

The hourly scan already measures everything this needs; this module only puts it together:

  * the verdict per coin from the agent's own timeframe agreement (engine/regime.py permission), so the weather
    never disagrees with the signals: UP / DOWN (a trend the strategies may follow), RANGE (4H and 1H both
    sideways), CHOPPY (timeframes disagree)
  * one market verdict: TREND_UP / TREND_DOWN (BTC and at least half the coins agree), MIXED (BTC trends, most coins
    don't), RANGE, CHOPPY, NEWS (inside an event blackout)
  * volatility: today's 14-day average daily range (ATR %) against the last 365 days (percentile)
  * the usual 24h move: on past days with a similar ATR % (last 3 years), how far the next daily close moved - the
    middle day and 8 of 10 days. Measured from history, not a forecast, and with no direction
  * crowding: the newest funding rate and the 24h open-interest change (rules of thumb, settings `weather:` in
    config.yaml; upgrade 9 will TEST them as a filter)
  * BTC's lead: the median altcoin's 24h change minus BTC's; Fear & Greed; the next events

It EXPLAINS the market. It never creates or removes a signal and never changes a gate, a cost, a size or an approval.

  daily_stats(high, low, close)      -> volatility and usual move of one coin (daily candles, oldest first)
  crowding(hourly, funding, s)       -> funding / open interest facts and a label
  build(...)                         -> the whole weather (reports/market_weather.json)
  telegram(w), md_lines(w)           -> the /weather reply and the fact-sheet / .md lines
Pure: no internet, no files.
"""
import datetime as dt
import html

import numpy as np

DEFAULTS = dict(funding_long_pct=0.03,      # funding per 8h at or above this = longs pay a lot (crowded long)
                funding_short_pct=-0.01,    # at or below this = shorts pay (crowded short)
                oi_rise_pct=5.0,            # open interest up this much in 24h = new money piling in
                similar_atr=0.2,            # "similar day" = ATR % within +-20% of today's
                min_similar=30)             # fewer similar days than this -> all days of the period are used
RANGE_LABELS = {"RANGE", "HIGH_VOL_RANGE", "COMPRESSION"}
ATR_N, PCT_DAYS, HIST_DAYS = 14, 365, 3 * 365
COIN_WORD = {"UP": "trend up", "DOWN": "trend down", "RANGE": "range", "CHOPPY": "choppy"}
COIN_ICON = {"UP": "🟢", "DOWN": "🔴", "RANGE": "🟡", "CHOPPY": "⚪"}
VERDICTS = {
    "TREND_UP": ("☀️", "Trend day ↑",
                 "BTC and most coins point up on 1D / 4H / 1H.",
                 ["longs with the trend, on pullbacks", "only coins marked trend up"],
                 ["shorts", "chasing a candle that already ran"]),
    "TREND_DOWN": ("🌧", "Trend day ↓",
                   "BTC and most coins point down on 1D / 4H / 1H.",
                   ["shorts with the trend, on bounces", "only coins marked trend down"],
                   ["longs / buying the dip", "chasing a candle that already fell"]),
    "MIXED": ("⛅", "Mixed day",
              "BTC has a direction, but most coins don't follow it.",
              ["only coins whose own timeframes agree", "smaller expectations"],
              ["trading coins marked choppy"]),
    "RANGE": ("🌥", "Range day",
              "No trend: price moves sideways between levels on 4H and 1H.",
              ["waiting - the trend strategies don't trade a range"],
              ["breakout trades without a retest", "trend trades"]),
    "CHOPPY": ("🌫", "Choppy - stay out",
               "The timeframes disagree (for example 1D up, 1H down). Longs and shorts both get stopped out.",
               ["waiting until 1D, 4H and 1H agree - no trade is the right trade"],
               ["any trade", "trading on feeling or headlines"]),
    "NEWS": ("⛈", "News risk - stay out",
             "A high-impact event is close. Price can jump both ways in seconds.",
             ["waiting until the event has passed"], ["any new trade"]),
}


def settings(cfg_section):
    s = dict(DEFAULTS)
    s.update({k: v for k, v in (cfg_section or {}).items() if k in DEFAULTS})
    return s


def _f(x, nd=2):
    return None if x is None or x != x else round(float(x), nd)


def daily_stats(high, low, close, s=None):
    """Volatility now and the usual 24h move, from closed daily candles (oldest first). None with < 60 days."""
    s = s or DEFAULTS
    h, lo, c = (np.asarray(a, dtype=float) for a in (high, low, close))
    if len(c) < 60:
        return None
    prev = np.concatenate([[c[0]], c[:-1]])
    tr = np.maximum(h - lo, np.maximum(abs(h - prev), abs(lo - prev)))
    atr = np.convolve(tr, np.ones(ATR_N) / ATR_N, mode="full")[:len(tr)]
    atr[:ATR_N - 1] = np.nan
    atr_pct = atr / c * 100
    now = atr_pct[-1]
    if now != now:
        return None
    last = atr_pct[-PCT_DAYS:]
    last = last[~np.isnan(last)]
    pctile = float((last < now).mean() * 100) if len(last) else None
    move = np.abs(c[1:] / c[:-1] - 1) * 100          # move[i] = the close-to-close move the day after day i
    a = atr_pct[:-1][-HIST_DAYS:]
    m = move[-HIST_DAYS:]
    ok = ~np.isnan(a)
    a, m = a[ok], m[ok]
    sim = np.abs(a / now - 1) <= s["similar_atr"]
    basis = "similar days"
    if sim.sum() < s["min_similar"]:
        sim, basis = np.ones(len(a), dtype=bool), "all days"
    mv = m[sim]
    p50, p80 = (float(np.percentile(mv, q)) for q in (50, 80)) if len(mv) else (None, None)
    price = float(c[-1])
    return dict(atr_pct=_f(now), vol_pctile=_f(pctile, 0), vol_label=vol_label(pctile),
                usual_move_pct=_f(p50), move_8of10_pct=_f(p80), days=int(len(mv)), basis=basis,
                price=price, band=[_f(price * (1 - p80 / 100), 6), _f(price * (1 + p80 / 100), 6)]
                if p80 is not None else None)


def vol_label(pctile):
    if pctile is None:
        return "unknown"
    return "quiet" if pctile < 20 else "normal" if pctile < 80 else "high" if pctile < 95 else "extreme"


def crowding(hourly, funding, s=None):
    """hourly / funding = this coin's recorded futures rows (engine/derivs columns). Funding in % per settlement."""
    s = s or DEFAULTS
    out = dict(funding_pct=None, oi_24h_pct=None, label="unknown")
    try:
        if funding is not None and len(funding):
            out["funding_pct"] = _f(float(funding.sort_values("time")["rate"].iloc[-1]) * 100, 4)
        if hourly is not None and len(hourly):
            oi = hourly.dropna(subset=["oi_usd"]).sort_values("ts")
            if len(oi) >= 2:
                last_ts, last = int(oi["ts"].iloc[-1]), float(oi["oi_usd"].iloc[-1])
                old = oi[oi["ts"] <= last_ts - 24 * 3_600_000]
                if len(old) and float(old["oi_usd"].iloc[-1]) > 0:
                    out["oi_24h_pct"] = _f((last / float(old["oi_usd"].iloc[-1]) - 1) * 100, 1)
    except (KeyError, ValueError, TypeError):
        return out
    f, oi = out["funding_pct"], out["oi_24h_pct"]
    rising = oi is not None and oi >= s["oi_rise_pct"]
    if f is None:
        out["label"] = "unknown"
    elif f >= s["funding_long_pct"]:
        out["label"] = "crowded long" if rising else "leaning long"
    elif f <= s["funding_short_pct"]:
        out["label"] = "crowded short" if rising else "leaning short"
    else:
        out["label"] = "neutral"
    return out


def coin_verdict(recs, permission):
    """UP / DOWN / RANGE / CHOPPY from the agent's own permission (regime.permission) and the 4H / 1H labels."""
    p = (permission or "").upper()
    if p.startswith("LONG"):
        return "UP"
    if p.startswith("SHORT"):
        return "DOWN"
    labels = [((recs or {}).get(tf) or {}).get("label") for tf in ("4h", "1h")]
    if all(lb in RANGE_LABELS for lb in labels):
        return "RANGE"
    return "CHOPPY"


def market_verdict(coins, blackout_now):
    """coins = [dict(coin, verdict)] with BTC among them."""
    if blackout_now:
        return "NEWS"
    v = {c["coin"]: c["verdict"] for c in coins}
    btc, n = v.get("BTC"), max(1, len(v))
    ups, downs = sum(x == "UP" for x in v.values()), sum(x == "DOWN" for x in v.values())
    if btc == "UP":
        return "TREND_UP" if ups >= n / 2 else "MIXED"
    if btc == "DOWN":
        return "TREND_DOWN" if downs >= n / 2 else "MIXED"
    return "RANGE" if btc == "RANGE" else "CHOPPY"


def _when(start_utc, now):
    try:
        t = dt.datetime.strptime(start_utc, "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return None
    return (t - now).total_seconds() / 3600


def build(now, regimes, daily, derivs, snap, events, blackout_now=None, fear_greed=None, s=None):
    """now = aware UTC datetime; regimes = {coin: dict(timeframes, permission, permission_reason)} (scanner);
    daily = {coin: (high, low, close)} closed 1D candles; derivs = {coin: (hourly rows, funding rows)};
    snap = {coin: dict(price, change_24h, ...)}; events = risk upcoming_events [dict(start_utc, type, name)]."""
    s = s or DEFAULTS
    coins = []
    order = ["BTC"] + sorted(c for c in regimes if c != "BTC")
    for c in order:
        r = regimes.get(c)
        if not r:
            continue
        recs = r.get("timeframes") or {}
        d = daily.get(c)
        hourly, fund = (derivs or {}).get(c) or (None, None)
        coins.append(dict(
            coin=c, verdict=coin_verdict(recs, r.get("permission")), permission=r.get("permission"),
            why=r.get("permission_reason"),
            labels={tf: (recs.get(tf) or {}).get("label") for tf in ("1w", "1d", "4h", "1h")},
            adx={tf: _f(((recs.get(tf) or {}).get("values") or {}).get("adx"), 0) for tf in ("1d", "4h", "1h")},
            vol=daily_stats(*d, s=s) if d is not None else None,
            crowd=crowding(hourly, fund, s),
            change_24h=_f((snap.get(c) or {}).get("change_24h"))))
    code = market_verdict(coins, blackout_now)
    icon, title, meaning, fits, avoid = VERDICTS[code]
    alts = [x["change_24h"] for x in coins if x["coin"] != "BTC" and x["change_24h"] is not None]
    btc = next((x for x in coins if x["coin"] == "BTC"), None)
    lead = None
    if alts and btc and btc["change_24h"] is not None:
        lead = _f(float(np.median(alts)) - btc["change_24h"])
    soon = []
    for e in events or []:
        h = _when(e.get("start_utc"), now)
        if h is not None and -1 <= h <= 7 * 24:
            soon.append(dict(start_utc=e.get("start_utc"), name=e.get("name") or e.get("type"), hours=_f(h, 1)))
    warnings = []
    if any(e["hours"] <= 24 for e in soon):
        warnings.append("High-impact event within 24 hours: no new trades from 1 hour before to 1 hour after.")
    if btc and btc.get("vol") and btc["vol"]["vol_label"] in ("high", "extreme"):
        warnings.append(f"BTC's daily range is {btc['vol']['vol_label']} (top {100 - btc['vol']['vol_pctile']:.0f}% "
                        "of the year): stops need room - the alerts' size at your fixed % risk already gets smaller "
                        "when the stop is wider.")
    for x in coins:
        if x["crowd"]["label"] in ("crowded long", "crowded short"):
            side = "long" if x["crowd"]["label"] == "crowded long" else "short"
            warnings.append(f"{x['coin']} is {x['crowd']['label']}: many traders are {side} and paying for it - a "
                            f"sharp move against them (a squeeze) is more likely than usual.")
    breadth = {k: sum(x["verdict"] == k for x in coins) for k in ("UP", "DOWN", "RANGE", "CHOPPY")}
    w = dict(utc=now.strftime("%Y-%m-%d %H:%M"), verdict=dict(code=code, icon=icon, title=title, meaning=meaning,
                                                              fits=fits, avoid=avoid),
             breadth=breadth, coins=coins, alts_vs_btc_24h=lead, fear_greed=fear_greed or None, events=soon,
             blackout_now=list(blackout_now or []), warnings=warnings, settings=s,
             note="Explains the market. It never creates a signal and never changes a rule, a size or an approval.")
    w["telegram"] = telegram(w)
    return w


def _pct(x, nd=1, sign=True):
    return "?" if x is None else (f"{x:+.{nd}f}%" if sign else f"{x:.{nd}f}%")


def _price(x):
    if x is None:
        return "?"
    return f"{x:,.0f}" if x >= 1000 else f"{x:,.2f}" if x >= 1 else f"{x:.4g}"


def _usual(c):
    v = c.get("vol")
    if not v or v.get("move_8of10_pct") is None:
        return None
    band = v.get("band") or [None, None]
    return (f"{c['coin']} usually moves ±{v['usual_move_pct']:.1f}% in 24h; on 8 of 10 {v['basis']} it closed within "
            f"±{v['move_8of10_pct']:.1f}% ({_price(band[0])} – {_price(band[1])})")


def telegram(w):
    """The /weather reply (Telegram HTML)."""
    v = w["verdict"]
    out = [f"{v['icon']} <b>Market weather · {w['utc']} UTC</b>", f"Verdict: <b>{v['title']}</b>", v["meaning"], ""]
    btc = next((c for c in w["coins"] if c["coin"] == "BTC"), None)
    if btc:
        lb = btc["labels"]
        out.append(f"BTC trend: 1D {lb.get('1d') or '?'} · 4H {lb.get('4h') or '?'} · 1H {lb.get('1h') or '?'}")
        if btc.get("vol"):
            out.append(f"Volatility: {btc['vol']['vol_label']} (daily range {btc['vol']['atr_pct']:.1f}%, "
                       f"higher than {btc['vol']['vol_pctile']:.0f}% of the last year)")
        u = _usual(btc)
        if u:
            out.append("Usual range: " + u + " - measured from the past, not a forecast")
        cr = btc["crowd"]
        if cr["funding_pct"] is not None:
            out.append(f"Crowding: {cr['label']} (funding {cr['funding_pct']:+.4f}%/8h"
                       + (f", open interest {_pct(cr['oi_24h_pct'])} in 24h" if cr["oi_24h_pct"] is not None else "")
                       + ")")
    if w.get("alts_vs_btc_24h") is not None:
        out.append(f"Altcoins vs BTC (24h): {_pct(w['alts_vs_btc_24h'])}")
    fg = w.get("fear_greed") or {}
    if fg.get("value") is not None:
        out.append(f"Mood (Fear & Greed): {fg.get('label') or ''} {fg['value']}".rstrip())
    out += ["", "<b>Coins</b>"]
    out += [f"{COIN_ICON[c['verdict']]} {c['coin']}: {COIN_WORD[c['verdict']]}"
            + (f" · {c['crowd']['label']}" if c["crowd"]["label"] not in ("neutral", "unknown") else "")
            for c in w["coins"]]
    if w.get("events"):
        out += ["", "<b>Events</b>"] + [f"• {html.escape(str(e['name']))} {e['start_utc']} UTC" for e in w["events"][:4]]
    if w.get("warnings"):
        out += [""] + [f"⚠️ {html.escape(x)}" for x in w["warnings"]]
    out += ["", "Fits today: " + "; ".join(v["fits"]), "Avoid: " + "; ".join(v["avoid"]), "",
            "<i>Explains the market only - it never creates a signal or changes your risk rules.</i>"]
    return "\n".join(out)


def md_lines(w):
    """Markdown lines (reports/market_weather.md and Claude's fact sheet)."""
    if not w:
        return ["- market weather not available (no reports/market_weather.json)"]
    v = w["verdict"]
    out = [f"- verdict ({w['utc']} UTC): **{v['title']}** - {v['meaning']}",
           f"- coins: " + ", ".join(f"{c['coin']} {COIN_WORD[c['verdict']]}" for c in w["coins"]),
           f"- fits: {'; '.join(v['fits'])} · avoid: {'; '.join(v['avoid'])}"]
    for c in w["coins"]:
        vol = c.get("vol") or {}
        cr = c["crowd"]
        out.append(f"- {c['coin']}: 1D {c['labels'].get('1d')} / 4H {c['labels'].get('4h')} / 1H "
                   f"{c['labels'].get('1h')} ({c.get('why') or '-'}); volatility {vol.get('vol_label', 'unknown')}"
                   + (f" (higher than {vol['vol_pctile']:.0f}% of the last year)" if vol.get("vol_pctile") is not None
                      else "")
                   + (f"; usual 24h move ±{vol['usual_move_pct']:.1f}%, 8 of 10 {vol['basis']} within "
                      f"±{vol['move_8of10_pct']:.1f}%" if vol.get("move_8of10_pct") is not None else "")
                   + f"; crowding {cr['label']}"
                   + (f" (funding {cr['funding_pct']:+.4f}%/8h" if cr["funding_pct"] is not None else "")
                   + (f", OI {_pct(cr['oi_24h_pct'])} 24h" if cr["oi_24h_pct"] is not None else "")
                   + (")" if cr["funding_pct"] is not None else ""))
    if w.get("alts_vs_btc_24h") is not None:
        out.append(f"- altcoins vs BTC (24h, median): {_pct(w['alts_vs_btc_24h'])}")
    out += [f"- event: {e['name']} {e['start_utc']} UTC" for e in w.get("events") or []]
    out += [f"- warning: {x}" for x in w.get("warnings") or []]
    out.append(f"- {w['note']}")
    return out
