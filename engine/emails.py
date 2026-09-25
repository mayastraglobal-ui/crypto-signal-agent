"""
The six email templates of the email redesign (approved design: "Signal Agent Email Templates").

Each builder takes the engine's numbers as a dict and returns mailkit.render(): subject, text part, HTML part.
Every email has the same frame: header row -> one big headline / banner -> 3-4 tiles or a short table -> at most
3 reasons or 1 lesson -> 1-2 buttons -> grey footer. Longer text (news, regimes, bull vs bear, idea chains, research
details) stays in Claude's full report on the dashboard, linked with a button.

Numbers come only from the engine's files (the callers read them); a missing value is shown as "–". Claude's
sentences (headline, do / don't, lesson ...) come from the '## Email summary' block of its report (summary.py),
which the Brain guard checked. Nothing here changes a signal, a fee, a risk limit, a gate or an approval.

  entry(e)          ENTRY SIGNAL · LIVE        (APPROVED strategies only - as before)
  update(x)         TRADE UPDATE · LIVE        TP1 / TP2 / stop / time exit / exit rule / cancelled
  action(a)         ACTION NEEDED              a workflow failed twice in a row, data unsafe, Claude's push refused
  fixed(a)          FIXED                      the one "it works again" email
  notice(n)         RISK NOTICE                a risk halt started or ended, a reminder
  briefing(b)       BRIEFING · 08:20 / 14:20 / 21:20
  daily(d)          DAILY REVIEW · 23:30
  weekly(w)         WEEKLY REPORT · WEEK nn

Pure functions: no internet, no files.
"""
import datetime as dt

from engine import mailkit as mk
from engine.mailkit import DASH, pct, price, signed, val

BJ = dt.timezone(dt.timedelta(hours=8))
SIGNAL_FOOTER = "Skip this signal if price has already left the entry zone. Signals only – not financial advice."
TRADE_FOOTER = "Signals only – not financial advice. The agent never places orders."
ACTION_FOOTER = ("The agent retries by itself. You get one email per problem, and one 'fixed' email when it works "
                 "again.")
TF_WORD = {"5m": "5M", "15m": "15M", "30m": "30M", "1h": "1H", "4h": "4H", "1d": "1D", "1w": "1W"}
TV_INTERVAL = {"5m": "5", "15m": "15", "30m": "30", "1h": "60", "4h": "240", "1d": "D", "1w": "W"}
TREND = {"STRONG_BULL": "▲▲ Strong up", "WEAK_BULL": "▲ Up", "BULL": "▲ Up", "STRONG_BEAR": "▼▼ Strong down",
         "WEAK_BEAR": "▼ Down", "BEAR": "▼ Down", "RANGE": "◆ Sideways", "HIGH_VOL_RANGE": "◆ Sideways",
         "TRANSITION": "◆ Changing", "UNCLEAR": "◆ Changing", "EXPANSION": "⚡ Fast move"}
MOODS = ("Calm", "Busy", "Volatile", "Risk-off")
FAST_MOVE_PCT = 3.0            # a 30-minute move this large (any signal coin) makes the mood "Volatile"
SOURCE_CHIP = {"literature": "RESEARCH", "variant_search": "VARIANT", "failure": "LOSS PATTERN",
               "missed_move": "MISSED MOVE", "market_structure": "FUTURES DATA", "lead_lag": "LEAD-LAG"}


# ---------------------------------------------------------------- small helpers -------------------------------------
def to_dt(utc_text):
    """'2026-09-26 01:07' (UTC) -> an aware datetime, or None."""
    try:
        return dt.datetime.strptime(str(utc_text)[:16], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def bj(utc_text, fmt="%d %b · %H:%M"):
    """A UTC time as Beijing time text ('26 Sep · 09:07'), or '–'."""
    t = to_dt(utc_text)
    if t is None:
        return DASH
    t = t.astimezone(BJ)
    return t.strftime(fmt.replace("%d", str(t.day)))          # '5 Oct', not '05 Oct'; times keep '09:07'


def when(utc_text):
    return f"{bj(utc_text)} Beijing"


def tf_word(tf):
    return TF_WORD.get(tf, str(tf).upper())


def tradingview(coin, quote, tf, futures=False):
    """The live chart of the pair on TradingView (Binance prices; the perpetual for a futures-only trade)."""
    sym = f"BINANCE:{coin}{quote}" + (".P" if futures else "")
    return f"https://www.tradingview.com/chart/?symbol={sym}&interval={TV_INTERVAL.get(tf, '60')}"


def arrow(direction):
    return "▲" if direction == "LONG" else "▼"


def move_pct(frm, to):
    try:
        return (float(to) / float(frm) - 1) * 100
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def short_event(name):
    """'US PCE / Personal Income and Outlays (Aug data)' -> 'US PCE'."""
    return str(name or "").split(" / ")[0].split(" (")[0].strip()


# ---------------------------------------------------------------- 1. entry ------------------------------------------
def entry(e):
    """ENTRY SIGNAL · LIVE. e = the scan's entry card (scanner.EmailContext) with the plan, the size, the reasons,
    the checks at the signal (open trades, event blackout, data, risk manager) and the links."""
    d = 1 if e["direction"] == "LONG" else -1
    side, act = ("LONG", "Buy") if d == 1 else ("SHORT", "Sell")
    z = sorted(e["entry_zone"])
    zone = f"{price(z[0])}–{price(z[1])}"
    subj = mk.subject([f"{arrow(e['direction'])} {side} {e['coin']}", tf_word(e["tf"]), f"Enter {zone}",
                       f"Stop {price(e['stop'])}"])
    until = e.get("valid_until_utc")
    right = f"Valid until {bj(until, '%H:%M')}" if until else e.get("valid_note") or ""
    market = "Futures only" if d == -1 or "futures" in str(e.get("market", "")).lower() else "Spot"
    rows, tones = [["Entry zone", zone, DASH, f"{act} only inside this zone"]], [[None, None, None, None]]
    sp = move_pct(e["entry"], e["stop"])
    rows.append(["Stop-loss", price(e["stop"]), f"{pct(sp)} · −1R", "Exit everything if hit"])
    tones.append([None, None, "down", None])
    tg = e.get("targets") or []
    for i, t in enumerate(tg, 1):
        last = i == len(tg)
        what = "Close the rest" if last else f"Close {t.get('close_pct', DASH)}%, " + (
            "move stop to entry" if i == 1 else "move stop to TP1")
        rows.append([f"TP{i}", price(t["price"]), f"{pct(move_pct(e['entry'], t['price']))} · {signed(t.get('r'))}", what])
        tones.append([None, None, "up", None])
    sz = e.get("size") or {}
    acct = e.get("account")
    size_tiles = [(f"Your size ({val(acct, '{:,.0f}')} USDT account)",
                   f"{val(sz.get('qty'), '{:.4g}')} {e['coin']} ≈ {val(sz.get('usdt'), '{:,.0f}')} USDT",
                   "made smaller: more would need over 3x leverage" if sz.get("capped") else ""),
                  ("Loss if stopped", f"{val(sz.get('risk_usdt'), '{:.2f}')} USDT ({val(sz.get('risk_pct'), '{:g}')}%)",
                   "")]
    ck = e.get("checks") or {}
    chips = [("No big news ±60 min" if ck.get("no_event", True) else "Big news within 60 min", ck.get("no_event", True)),
             ("Data OK" if e.get("data_state") == "GOOD" else f"Data {e.get('data_state') or DASH}",
              e.get("data_state") == "GOOD"),
             (f"Open trades {val(ck.get('open'))} / {val(ck.get('max_open'))}",
              ck.get("open") is not None and ck.get("max_open") is not None and ck["open"] < ck["max_open"]),
             ("Risk manager: go" if ck.get("risk_ok", True) else "Risk manager: stop", ck.get("risk_ok", True))]
    blocks = [("header", ("ENTRY SIGNAL · LIVE", when(e.get("utc")))),
              ("banner", dict(title=f"{arrow(e['direction'])} {side} {e['coin']}", tone="long" if d == 1 else "short",
                              sub=f"{e['coin']}/{e.get('quote', 'USDT')} · {tf_word(e['tf'])} · {market} · "
                                  f"{e['strategy']} v{e['version']}", right=right)),
              ("table", dict(cols=["Step", "Price", "Distance", "What to do"], rows=rows, tones=tones, mono=[1, 2])),
              ("tiles", ("grey", size_tiles)),
              ("section", "Why (3 reasons)"), ("list", reasons(e)[:3]),
              ("chips", chips)]
    if e.get("chart_cid"):
        blocks.append(("image", e["chart_cid"]))
    blocks += [("buttons", [("Open live chart", e.get("live_chart")), ("Backtest chart", e.get("backtest_chart"))]),
               ("footer", SIGNAL_FOOTER)]
    return mk.render(subj, blocks, [e.get("chart")], "entry")


def reasons(e):
    """At most 3 one-line reasons, all from the engine: the setup, the trend agreement, the backtest."""
    why = [mk.plain(w) for w in e.get("why") or []]
    trend = next((w for w in why if w.startswith("Trend:")), None)
    caution = next((w for w in why if w.startswith("Caution:")), None)
    setup = next((w for w in why if not w.startswith(("Trend:", "Caution:"))), None)
    bt = e.get("backtest") or {}
    line = (f"Backtest: {val(bt.get('trades'), '{:,}')} trades, average {signed(bt.get('avg_r'), 'R', 2)} per trade "
            f"after fees, 95% worst losing streak {val(bt.get('streak95'))} trades")
    return [x for x in (setup, caution or trend) if x] + [line]     # a caution is never cut: it replaces the trend


# ---------------------------------------------------------------- 2. trade update -----------------------------------
UPDATE = {  # kind -> (icon, banner word, subject tail, tone)
    "TP1_HIT": ("✓", "TP1 HIT", "move stop to entry", "win"),
    "TP": ("✓", "TARGET HIT", "trade closed", "win"),
    "SL": ("✕", "STOP HIT", "trade closed", "loss"),
    "BE": ("✓", "REST STOPPED AT ENTRY", "trade closed", "win"),
    "TRAIL": ("✓", "REST STOPPED AT TP1", "trade closed", "win"),
    "TIME": ("⏱", "TIME EXIT", "close the rest", "plain"),
    "EXIT_RULE": ("⏹", "EXIT RULE", "close the rest", "plain"),
    "CANCELLED": ("⊘", "CANCELLED", "", "plain"),
}


def update_kind(x):
    if x["kind"] == "TP1_HIT":
        return "TP1_HIT"
    if x["kind"] == "CANCELLED":
        return "CANCELLED"
    r = str(x.get("close_reason") or "")
    return "TP" if r.startswith("TP") else r if r in UPDATE else "EXIT_RULE"


def update(x):
    """TRADE UPDATE · LIVE: x = dict(coin, quote, direction, tf, strategy, version, kind TP1_HIT / CLOSED / CANCELLED,
    close_reason, result_r, entry, stop_now, targets [prices], tp_split [%], tp1_r, price_now, entered_utc, utc,
    open, max_open, day_r, week_r, cancel_reason, live_chart, backtest_chart, chart)."""
    k = update_kind(x)
    icon, word, tail, tone = UPDATE[k]
    coin, side = x["coin"], x["direction"]
    tg = [t for t in x.get("targets") or [] if t is not None]
    if k == "TP":
        n = str(x.get("close_reason"))[2:] or str(len(tg))
        word, head = f"TP{n} HIT", f"TP{n} hit"
    else:
        head = {"TP1_HIT": "TP1 hit", "SL": "Stop hit", "BE": "Rest stopped at entry", "TRAIL": "Rest stopped at TP1",
                "TIME": "Time exit", "EXIT_RULE": "Exit rule", "CANCELLED": "Cancelled"}[k]
    big = signed(x.get("tp1_r")) if k == "TP1_HIT" else DASH if k == "CANCELLED" else signed(x.get("result_r"))
    if k == "SL" and x.get("result_r") is not None and x["result_r"] >= 0:
        tone = "plain"
    if k in ("TIME", "EXIT_RULE"):
        tone = "win" if (x.get("result_r") or 0) > 0 else "loss" if (x.get("result_r") or 0) < 0 else "plain"
    tail_txt = tail if k != "CANCELLED" else (x.get("cancel_reason") or "no entry")
    subj = mk.subject([f"{icon} {head}", f"{coin} {side}" + ("" if k == "CANCELLED" else f" {big}"), tail_txt])
    sub = f"{coin} {side} · {tf_word(x['tf'])} · " + (f"entered {bj(x.get('entered_utc'), '%H:%M')}"
                                                     if k != "CANCELLED" else "no entry was made")
    split = x.get("tp_split") or []
    if k == "TP1_HIT":
        do = [f"Close {val(split[0] if split else None)}% at {price(tg[0] if tg else None)}",
              f"Move stop to {price(x.get('entry'))} (your entry) – the rest is protected at entry"]
    elif k in ("TIME", "EXIT_RULE"):
        do = ["Close what is left at the market price – the trade is over."]
    elif k == "CANCELLED":
        do = ["Nothing to do – do not enter this trade any more."]
    else:
        do = ["Nothing to do – the trade is closed."]
    closed = x["kind"] != "TP1_HIT"
    nxt = tg[1] if k == "TP1_HIT" and len(tg) > 1 else None
    tiles = [("Entry", price(x.get("entry")), ""), ("Price now", price(x.get("price_now")), ""),
             ("New stop", DASH if closed else price(x.get("stop_now")), ""),
             ("Next target", price(nxt), pct(move_pct(x.get("price_now"), nxt)) if nxt else "")]
    blocks = [("header", ("TRADE UPDATE · LIVE", when(x.get("utc")))),
              ("banner", dict(title=f"{icon} {word}", sub=sub, big=big if k != "CANCELLED" else "", tone=tone)),
              ("box", dict(title="Do now", lines=[f"{i}. {t}" for i, t in enumerate(do, 1)], strong=True)),
              ("tiles", ("grey", tiles)),
              ("line", f"Open trades {val(x.get('open'))} / {val(x.get('max_open'))} · Today {signed(x.get('day_r'))} · "
                       f"This week {signed(x.get('week_r'))}")]
    if x.get("chart_cid"):
        blocks.append(("image", x["chart_cid"]))
    blocks += [("buttons", [("Open live chart", x.get("live_chart")), ("Backtest chart", x.get("backtest_chart"))]),
               ("footer", TRADE_FOOTER)]
    return mk.render(subj, blocks, [x.get("chart")], "update")


# ---------------------------------------------------------------- 3. action needed / fixed / notice -----------------
WHAT = {
    "scan": ("hourly scan", "No new signals or trade updates are sent while it fails. Open trades keep the stops "
                            "you set."),
    "research": ("daily research run", "Strategy statuses stay as they were. Hourly scans and signals keep running."),
    "brain": ("Brain workflow", "Claude's briefings and reviews are not saved or emailed. Signals from the engine are "
                                "not affected."),
}


def action(a):
    """ACTION NEEDED: a = dict(what scan/research/brain/data/guard, times_utc [the failed runs], run_url, reasons,
    title, meaning, steps)."""
    w = a["what"]
    if w in WHAT:
        name, meaning = WHAT[w]
        times = [bj(t, "%H:%M") for t in a.get("times_utc") or []]
        count = len(times) or 2
        title = f"! {name[0].upper() + name[1:]} failed {'twice' if count == 2 else f'{count}×'}"
        subj = mk.subject([f"! Action needed", f"{name} failed {count}× in a row"])
        sub = ("At " + " and ".join(times) + " Beijing") if times else ""
        steps = ["Open the failed run (button below).", "Screenshot the step with the red ✕.",
                 "Send the screenshot to Claude."]
        button = [("Open the failed run", a.get("run_url"))]
    else:
        title, meaning, sub = a["title"], a["meaning"], a.get("sub", "")
        subj = mk.subject(["! Action needed", a.get("subject") or title.lstrip("! ")])
        steps, button = a.get("steps") or [], a.get("buttons") or []
    blocks = [("header", ("ACTION NEEDED", when(a.get("utc")))),
              ("banner", dict(title=title, sub=sub, tone="amber")),
              ("section", "What it means"), ("line", meaning)]
    if a.get("reasons"):
        rs = [mk.plain(r) for r in a["reasons"]]
        blocks += [("section", "What was found"), ("list", rs[:3] + ([f"… and {len(rs) - 3} more"] if len(rs) > 3 else []))]
    if steps:
        blocks += [("section", a.get("steps_title", "What to do (2 minutes)")), ("list", steps)]
    blocks += [("buttons", button), ("footer", a.get("footer", ACTION_FOOTER))]
    return mk.render(subj, blocks, (), "action")


def fixed(a):
    """The one 'fixed' email after an ACTION NEEDED email: a = dict(what, utc, detail, run_url)."""
    name = WHAT.get(a["what"], (a.get("name") or a["what"], ""))[0]
    subj = mk.subject([f"✓ Fixed", f"{name} works again"])
    blocks = [("header", ("FIXED", when(a.get("utc")))),
              ("banner", dict(title=f"✓ {name[0].upper() + name[1:]} works again", sub=a.get("detail", ""), tone="win")),
              ("line", "Nothing to do. Normal checks and emails are running again."),
              ("buttons", [("Open the run", a.get("run_url"))]),
              ("footer", "You get one email per problem, and one 'fixed' email when it works again.")]
    return mk.render(subj, blocks, (), "fixed")


def notice(n):
    """RISK NOTICE (a risk halt starts or ends) and reminders: n = dict(label, title, sub, lines, tone, subject, utc)."""
    blocks = [("header", (n.get("label", "NOTICE"), when(n.get("utc")))),
              ("banner", dict(title=n["title"], sub=n.get("sub", ""), tone=n.get("tone", "amber"))),
              ("list", [mk.plain(x) for x in n.get("lines") or []][:3]),
              ("buttons", n.get("buttons") or []),
              ("footer", n.get("footer", TRADE_FOOTER))]
    return mk.render(mk.subject(n["subject"]), blocks, (), "notice")


# ---------------------------------------------------------------- 4. briefing ---------------------------------------
def mood(b):
    """The engine's mood word: Risk-off (data not GOOD, a risk halt or an event blackout now), Volatile (a signal
    coin moved 3% or more in 30 minutes, or 2+ coins in a daily EXPANSION), Busy (a live signal, an open trade or a
    high-impact event within 24 hours), else Calm."""
    if b.get("data_state") not in (None, "GOOD") or b.get("halts") or b.get("blackout_now"):
        return "Risk-off"
    moves = [abs(c["move_30m"]) for c in b.get("coins") or [] if c.get("move_30m") is not None]
    if (moves and max(moves) >= FAST_MOVE_PCT) or sum(c.get("regime_1d") == "EXPANSION" for c in b.get("coins") or []) >= 2:
        return "Volatile"
    if b.get("signals") or b.get("open") or b.get("event_24h"):
        return "Busy"
    return "Calm"


def market_bias(coins):
    up = sum(TREND.get(c.get("regime_1d"), "").startswith("▲") for c in coins)
    down = sum(TREND.get(c.get("regime_1d"), "").startswith("▼") for c in coins)
    if coins and up > len(coins) / 2:
        return "▲ Up bias"
    if coins and down > len(coins) / 2:
        return "▼ Down bias"
    return "◆ Mixed" if coins else DASH


def event_rows(events, n=3):
    out = []
    for ev in (events or [])[:n]:
        t = to_dt(ev.get("start_utc"))
        out.append([bj(ev.get("start_utc"), "%a %d · %H:%M"),
                    short_event(ev.get("name")) + (f" ({ev['type']})" if ev.get("type") and ev["type"] not in
                                                   short_event(ev.get("name")) else "")])
    return out


def briefing(b):
    """BRIEFING · 08:20: b = dict(slot '08:20', utc, signals, open, max_open, data_state, coins [dict(coin, price,
    regime_1d, move_30m)], events [dict(start_utc, name, type)], halts, blackout_now, event_24h, summary (Claude's
    block or None), page_url, dashboard_url)."""
    s = b.get("summary") or {}
    m = mood(b)
    ev = (b.get("events") or [])[:3]
    nxt = ev[0] if ev else None
    subj = mk.subject([b["slot"], m, f"{val(b.get('signals'))} signal" + ("" if b.get("signals") == 1 else "s"),
                       f"Next: {short_event(nxt['name'])} {bj(nxt['start_utc'], '%a %H:%M')}" if nxt else None])
    head = s.get("headline") or ("No signal. No trade." if not b.get("signals") else
                                 "A live signal – see its entry email.")
    sub = s.get("sub") or ("Claude's summary is missing – engine numbers only." if not s else "")
    coins = b.get("coins") or []
    rows, tones = [], []
    for c in coins:
        mv = c.get("move_30m")
        rows.append([c["coin"], price(c.get("price")), TREND.get(c.get("regime_1d"), DASH), pct(mv, 1)])
        tones.append([None, None, None, None if mv is None or mv == 0 else "up" if mv > 0 else "down"])
    data_ok = b.get("data_state") == "GOOD"
    blocks = [("header", (f"BRIEFING · {b['slot']}", bj(b.get("utc"), "%a %d %b") + " · Beijing")),
              ("headline", (head, sub)),
              ("tiles", ("grey", [("Signals", val(b.get("signals")), "live"),
                                  ("Open trades", f"{val(b.get('open'))} / {val(b.get('max_open'))}", ""),
                                  ("Market", market_bias(coins), "daily trend"),
                                  ("Data", "✓ OK" if data_ok else "! issue", "" if data_ok else val(b.get("data_state")))])),
              ("table", dict(cols=["Coin", "Price", "Daily trend", "30 min"], rows=rows, tones=tones, mono=[1, 3]))]
    if ev:
        blocks += [("section", "Next events (no new trades ±1 hour)"), ("table", dict(cols=None, rows=event_rows(ev)))]
    blocks += [("box", dict(title="Do", lines=[s.get("do") or "Wait for a LIVE entry email before any trade."],
                            tone="win")),
               ("box", dict(title="Don't", lines=[s.get("dont") or "Don't trade from headlines or fast candles."],
                            tone="loss")),
               ("buttons", [("Full analysis by Claude", b.get("page_url")), ("Dashboard", b.get("dashboard_url"))]),
               ("footer", "News, regimes, bull vs bear and all numbers are in the full analysis. Not financial advice.")]
    return mk.render(subj, blocks, (), "briefing")


# ---------------------------------------------------------------- 5. daily review -----------------------------------
def source_chip(card, queued=()):
    f = card.get("factory")
    if f == "literature" and ("freqtrade" in str(card.get("source", "")).lower()
                              or "freqtrade" in str(card.get("source_url", "")).lower()
                              or f"{card.get('id')}@{card.get('version')}" in queued):
        return "FREQTRADE"
    return SOURCE_CHIP.get(f, "RESEARCH" if f is None else str(f).upper().replace("_", " "))


def status_chip(statuses):
    """The lab card's research status over its timeframes: PASSED (any VALIDATION or better), FAILED (all FAILED /
    BIASED), else TESTING (not tested yet, or still BACKTESTING)."""
    if any(s in ("VALIDATION", "PAPER_TRADING", "APPROVED") for s in statuses):
        return "PASSED"
    if statuses and all(s in ("FAILED", "BIASED", "RETIRED") for s in statuses):
        return "FAILED"
    return "TESTING"


def closest(cells, n=3):
    """The cells nearest to the average-R bar that have not passed: [(label, value text, fraction, note)]."""
    out = []
    for c in (cells or {}).values():
        if c.get("status") not in ("BACKTESTING", "FAILED") or c.get("bias"):
            continue
        ev = (c.get("evidence") or {}).get("all") or {}
        avg, need = ev.get("avg_r"), c.get("required_avg_r")
        if avg is None or need is None or ev.get("n", 0) < 1:
            continue
        gap = max(0.0, float(need) - float(avg))
        out.append((gap, -ev.get("n", 0), c, float(avg), float(need)))
    out.sort(key=lambda x: (x[0], x[1]))
    rows = []
    for gap, _, c, avg, need in out[:n]:
        note = (f"needs {signed(gap, 'R', 2)} per trade" if gap > 0 else
                "average met – still: " + mk.plain((c.get("reasons") or c.get("paper_gate_failed") or [DASH])[0])[:70])
        rows.append((f"{c['strategy']} v{c['version']} {c['tf']}", f"{signed(avg, 'R', 2)} of {signed(need, 'R', 2)}",
                     max(0.0, avg) / need if need > 0 else 0.0, note))
    return rows


def daily(d):
    """DAILY REVIEW · 23:30: d = dict(date, utc, trades [dict(result_r)], day_r, counts (research counts of today),
    signal_coins, ideas [dict(name, what, source, status)], lessons_added, closest [bars rows], summary, page_url,
    lesson_url = the beginner lesson page, dashboard_url)."""
    s = d.get("summary") or {}
    c = d.get("counts") or {}
    tr = d.get("trades") or []
    wins = sum(1 for t in tr if (t.get("result_r") or 0) > 0)
    losses = sum(1 for t in tr if (t.get("result_r") or 0) < 0)
    ideas = d.get("ideas") or []
    nl = d.get("lessons_added")
    trades_txt = "No trades today." if not tr else f"{len(tr)} trade{'s' if len(tr) != 1 else ''} today."
    head = (f"{trades_txt} {val(c.get('backtests'), '{:,}')} backtests, {len(ideas)} new idea"
            f"{'s' if len(ideas) != 1 else ''}, {val(nl)} lesson{'s' if nl != 1 else ''}.")
    subj = mk.subject(["Daily", f"{len(tr)} trade{'s' if len(tr) != 1 else ''}",
                       f"{val(c.get('backtests'), '{:,}')} backtests", f"{len(ideas)} new idea" + ("s" if len(ideas) != 1 else "")])
    per = c.get("per_coin") or {}
    sig = set(d.get("signal_coins") or [])
    grid = [f"{'●' if k in sig else '○'} {k} {v}" for k, v in sorted(per.items(), key=lambda x: (x[0] not in sig, x[0]))]
    blocks = [("header", ("DAILY REVIEW · 23:30", bj(d.get("utc"), "%a %d %b"))),
              ("headline", (head, s.get("sub") or "")),
              ("section", "Trading today (live)"),
              ("tiles", ("grey", [("Trades", str(len(tr)), ""), ("Win / loss", f"{wins} / {losses}", ""),
                                  ("Day result", signed(d.get("day_r")), "")])),
              ("section", "Testing today"),
              ("tiles", ("teal", [("Backtests", val(c.get("backtests"), "{:,}"), "runs"),
                                  ("Strategies", val(c.get("strategies")), "applied"),
                                  ("Coins", val(c.get("coins")), "tested"), ("New ideas", str(len(ideas)), "built")])),
              ("line", f"{val(c.get('strategies'))} strategies × their timeframes = {val(c.get('tests_per_coin'))} "
                       "tests per coin" if c else "No research run today – the numbers above are missing."),
              ("section", "Backtests per coin")]
    blocks.append(("grid", (grid, 5, "● signal coin · ○ research only")) if grid else ("line", DASH))
    blocks += [("section", "New ideas built today"),
               ("ideas", ideas) if ideas else ("line", "None today.")]
    close = d.get("closest") or []
    if close:
        blocks += [("section", "Closest to passing" + (f" (needs {close[0][3].split('needs ')[-1]})"
                                                        if close[0][3].startswith("needs") else "")),
                   ("bars", close)]
    blocks += [("box", dict(title="Lesson of the day", lines=[s.get("lesson") or DASH], tone="teal")),
               ("section", "Tomorrow"), ("line", s.get("tomorrow") or DASH),
               ("buttons", [("Full review by Claude", d.get("page_url")),
                            ("Beginner lesson", d["lesson_url"]) if d.get("lesson_url") else ("Dashboard",
                                                                                               d.get("dashboard_url"))]),
               ("footer", "Losses, missed moves, idea chains and your beginner lesson are in the full review. "
                          "Not financial advice.")]
    return mk.render(subj, blocks, (), "daily")


# ---------------------------------------------------------------- 6. weekly -----------------------------------------
def weekly(w):
    """WEEKLY REPORT: w = dict(week_no, utc, days (from, to), counts (7-day sums), passed, close, ideas_by_source
    {chip: n}, coins_tested, decision [dict(cell, pack_url, chart_url)], card (sources, tasks_done, tasks_expected,
    data_problems []), summary, page_url, dashboard_url)."""
    s = w.get("summary") or {}
    c = w.get("counts") or {}
    by = w.get("ideas_by_source") or {}
    n_ideas = sum(by.values())
    subj = mk.subject([f"Week {w['week_no']}", f"{val(c.get('backtests'), '{:,}')} backtests",
                       f"{n_ideas} new idea" + ("s" if n_ideas != 1 else ""), f"{val(w.get('passed'))} passed"])
    words = {"RESEARCH": "from research papers", "FREQTRADE": "from freqtrade", "VARIANT": "engine variants",
             "LOSS PATTERN": "from a loss pattern", "MISSED MOVE": "from a missed move", "FUTURES DATA": "from futures data",
             "LEAD-LAG": "from lead-lag"}
    parts = " · ".join(f"{v} {words.get(k, k.lower())}" for k, v in sorted(by.items(), key=lambda x: -x[1]))
    dec = w.get("decision") or []
    if dec:
        x = dec[0]
        dec_lines = [f"Approve {x['cell']} for live signals? Reply yes or no."] + (
            [f"{len(dec) - 1} more waiting - see the dashboard."] if len(dec) > 1 else [])
        dec_buttons = [("Approval pack", x.get("pack_url")), ("Backtest chart", x.get("chart_url"))]
    else:
        dec_lines, dec_buttons = ["None this week."], []
    card = w.get("card") or {}
    dp = card.get("data_problems")
    rows = [["Research sources read", val(card.get("sources"))],
            ["Claude tasks delivered", f"{val(card.get('tasks_done'))} of {val(card.get('tasks_expected'))}"],
            ["Data sources", DASH if dp is None else "✓ All OK" if not dp else "! " + ", ".join(dp[:3])],
            ["Self-improvement idea", s.get("improvement") or DASH]]
    blocks = [("header", (f"WEEKLY REPORT · WEEK {w['week_no']}", w.get("days") or DASH)),
              ("headline", (s.get("headline") or f"{val(w.get('passed'))} strategies passed this week.",
                            s.get("sub") or ("No decision needed from you." if not dec else "One decision for you below."))),
              ("section", "Testing this week"),
              ("tiles", ("teal", [("Backtests", val(c.get("backtests"), "{:,}"), "7 days"),
                                  ("Strategies", val(c.get("strategies")), "applied"),
                                  ("Passed", val(w.get("passed")), "to VALIDATION+"), ("Close", val(w.get("close")),
                                                                                        "≤ 0.10R away")])),
              ("line", f"{n_ideas} new idea{'s' if n_ideas != 1 else ''} built" + (f": {parts}" if parts else "") + "."),
              ("line", f"{val(w.get('coins_tested'))} coins tested · per-coin numbers are in each daily review."),
              ("box", dict(title="Your decision", lines=dec_lines, strong=True))]
    if dec_buttons:
        blocks.append(("buttons", dec_buttons))
    blocks += [("section", "Agent report card"), ("table", dict(cols=None, rows=rows)),
               ("section", "Next week"), ("line", s.get("next") or DASH),
               ("buttons", [("Full weekly research", w.get("page_url")), ("Dashboard", w.get("dashboard_url"))]),
               ("footer", "Sources, candidates, the event calendar and idea chains are in the full weekly research. "
                          "Not financial advice.")]
    return mk.render(subj, blocks, (), "weekly")
