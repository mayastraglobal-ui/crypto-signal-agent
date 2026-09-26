"""
The email templates, format v2 (approved design: the canvas "Signal Agent Emails v2").

Each builder takes the engine's numbers as a dict and returns mailkit.render(): subject, text part, HTML part.
Every email has the same order: header (type pill + label + time) -> banner / headline -> ACTION box (always; "None."
is a valid action) -> numbers (plan table or tiles) -> at most 3 reasons or 1 lesson -> score line -> 1-2 buttons ->
footer. Subjects start with the type: "LIVE ...", "PAPER ...", "! ..." (alert), "✓ Fixed ...", "08:20 ...",
"Daily ...", "Week nn ...".

Numbers come only from the engine's files (the callers read them); a missing value is shown as "–". Claude's
sentences (headline, do / don't, lesson ...) come from the '## Email summary' block of its report (summary.py),
which the Brain guard checked. Nothing here changes a signal, a fee, a risk limit, a gate or an approval.

  live_entry(e)       A  LIVE signal            APPROVED strategies only
  live_update(x)      B  LIVE update            FILLED / TP1 / TP / BE / TRAIL / SL / TIME / EXIT_RULE / CANCELLED /
                                                WARNING - a reply in the entry email's thread
  paper_signal(e)     C  PAPER signal           PAPER_TRADING versions: practice only, a dashed blue card
  paper_update(x)     D  PAPER update           the same kinds as B, in the paper signal's thread
  paper_complete(c)   E  PAPER complete         once, when a version's 20th paper signal closes
  alert(a)            F  ALERT                  one layout for every system problem (one email per problem)
  fixed(a)            G  FIXED                  one per alert, when it works again
  briefing(b)         H  BRIEFING 08:20
  changes(b)          I  BRIEFING 14:20 / 21:20 changes only (not sent when nothing changed)
  daily(d)            J  DAILY 23:30
  weekly(w)           K  WEEKLY (Sunday)

Pure functions: no internet, no files.
"""
import datetime as dt

from engine import mailkit as mk
from engine.mailkit import DASH, pct, price, signed, val

BJ = dt.timezone(dt.timedelta(hours=8))
SIGNAL_FOOTER = "Skip this signal if price has already left the entry zone. Signals only – not financial advice."
TRADE_FOOTER = "Every update for this trade arrives in the same email thread. Signals only – not financial advice."
PAPER_FOOTER = ("Practice only – no real money. Paper signals test a strategy before it can send real-money signals. "
                "Not financial advice.")
TF_WORD = {"5m": "5M", "15m": "15M", "30m": "30M", "1h": "1H", "4h": "4H", "1d": "1D", "1w": "1W"}
TV_INTERVAL = {"5m": "5", "15m": "15", "30m": "30", "1h": "60", "4h": "240", "1d": "D", "1w": "W"}
TREND = {"STRONG_BULL": "▲▲ Strong up", "WEAK_BULL": "▲ Up", "BULL": "▲ Up", "STRONG_BEAR": "▼▼ Strong down",
         "WEAK_BEAR": "▼ Down", "BEAR": "▼ Down", "RANGE": "◆ Sideways", "HIGH_VOL_RANGE": "◆ Sideways",
         "TRANSITION": "◆ Changing", "UNCLEAR": "◆ Changing", "EXPANSION": "⚡ Fast move"}
BTC_WORD = {"UP": "up", "DOWN": "down"}
SOURCE_CHIP = {"literature": "RESEARCH", "variant_search": "VARIANT", "failure": "LOSS PATTERN",
               "missed_move": "MISSED MOVE", "market_structure": "FUTURES DATA", "lead_lag": "LEAD-LAG"}
PAPER_NEEDED = 20              # closed paper signals before approval (config.yaml approval.min_paper_signals)
ALERT_FIX_HOURS = 6            # "No 'Fixed' email by <time + 6 h>? Forward this email to the builder."


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


def utc_text(t):
    return t.strftime("%Y-%m-%d %H:%M")


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


def rtxt(r):
    """A target in R as the plan shows it: +2R, +2.5R, −1R."""
    if mk.missing(r):
        return DASH
    s = signed(r)
    return s[:-3] + "R" if s.endswith(".0R") else s


def held(a_utc, b_utc):
    a, b = to_dt(a_utc), to_dt(b_utc)
    if a is None or b is None or b < a:
        return DASH
    m = int((b - a).total_seconds() // 60)
    return f"{m // 60} h {m % 60} m" if m >= 60 else f"{m} min"


def plural(n, word, many=None):
    return f"{val(n)} {word if n == 1 else many or word + 's'}"


def action_box(title, lines, color=mk.TEAL, numbered=False):
    """The ACTION box (DO NOW / PRACTICE NOW / ACTION / YOUR DECISION): always there, 2 px border."""
    return ("box", dict(title=title, lines=[mk.plain(x) for x in lines if x] or ["None."], strong=True, color=color,
                        numbered=numbered and len([x for x in lines if x]) > 1))


# ---------------------------------------------------------------- the trade plan (A and C) --------------------------
def plan_table(e, paper=False):
    d = 1 if e["direction"] == "LONG" else -1
    z = sorted(e["entry_zone"])
    zone = f"{price(z[0])}–{price(z[1])}"
    rows = [["Entry", zone, ("Buy" if d == 1 else "Sell") + (" inside this zone" if paper else " only inside this zone")]]
    tones = [[None, None, None]]
    rows.append(["Stop", f"{price(e['stop'])} −1R", "Exit all if hit" if paper else "Exit everything if hit"])
    tones.append(["down", "down", None])
    tg = e.get("targets") or []
    for i, t in enumerate(tg, 1):
        last = i == len(tg)
        if last:
            what = "Close the rest"
        else:
            what = f"Close {t.get('close_pct', DASH)}%, " + (("stop to entry" if paper else "move stop to entry")
                                                              if i == 1 else "move stop to TP1")
        rows.append([f"TP{i}", f"{price(t.get('price'))} {rtxt(t.get('r'))}", what])
        tones.append(["up", "up", None])
    return ("table", dict(cols=["Step", "Price", "On paper" if paper else "What to do"], rows=rows, tones=tones,
                          mono=[1]))


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


def valid_right(e):
    until = e.get("valid_until_utc")
    return f"Valid until {bj(until, '%H:%M')}" if until else e.get("valid_note") or ""


# ---------------------------------------------------------------- A. LIVE signal ------------------------------------
def live_entry(e):
    """A. LIVE signal (APPROVED strategies only). e = the scan's entry card (scanner.EmailContext): the plan, the size,
    the reasons, the checks at the signal, the live record (live = dict(n, total_r)) and the links."""
    d = 1 if e["direction"] == "LONG" else -1
    side = "LONG" if d == 1 else "SHORT"
    z = sorted(e["entry_zone"])
    zone = f"{price(z[0])}–{price(z[1])}"
    subj = mk.subject([f"LIVE {arrow(e['direction'])} {side} {e['coin']} {tf_word(e['tf'])}", f"Enter {zone}",
                       f"Stop {price(e['stop'])}"])
    market = "Futures only" if d == -1 or "futures" in str(e.get("market", "")).lower() else "Spot"
    if e.get("valid_note"):                                  # a 5m-confirmed entry: the bar already closed
        do = [f"{'Buy' if d == 1 else 'Sell (futures)'} now near {price(e.get('entry'))} – the 5m bar confirmed it. "
              f"Set the stop at {price(e['stop'])} right away."]
    else:
        do = [f"Place a limit {'BUY' if d == 1 else 'SELL (futures)'} between {price(z[0])} and {price(z[1])}. "
              f"Set the stop at {price(e['stop'])} right away."]
    sz = e.get("size") or {}
    size_tiles = [(f"Your size ({val(e.get('account'), '{:,.0f}')} USDT account)",
                   f"{val(sz.get('qty'), '{:.4g}')} {e['coin']}",
                   f"≈ {val(sz.get('usdt'), '{:,.0f}')} USDT" + (" · made smaller: more would need over 3x leverage"
                                                                 if sz.get("capped") else "")),
                  ("Loss if stopped", f"{val(sz.get('risk_usdt'), '{:.2f}')} USDT",
                   f"{val(sz.get('risk_pct'), '{:g}')}% of account", "down")]
    ck = e.get("checks") or {}
    chips = [("No big news ±60 min" if ck.get("no_event", True) else "Big news within 60 min", ck.get("no_event", True)),
             ("Data OK" if e.get("data_state") == "GOOD" else f"Data {e.get('data_state') or DASH}",
              e.get("data_state") == "GOOD"),
             (f"Open trades {val(ck.get('open'))} / {val(ck.get('max_open'))}",
              ck.get("open") is not None and ck.get("max_open") is not None and ck["open"] < ck["max_open"]),
             ("Risk manager: go" if ck.get("risk_ok", True) else "Risk manager: stop", ck.get("risk_ok", True))]
    live = e.get("live") or {}
    blocks = [("header", ("LIVE", "ENTRY SIGNAL", when(e.get("utc")))),
              ("banner", dict(title=f"{arrow(e['direction'])} {side} {e['coin']}", tone="long" if d == 1 else "short",
                              sub=f"{e['coin']}/{e.get('quote', 'USDT')} · {tf_word(e['tf'])} · {market} · "
                                  f"{e['strategy']} v{e['version']}", right=valid_right(e))),
              action_box("Do now", do, mk.GREEN),
              ("section", "The plan"), plan_table(e),
              ("tiles", ("grey", size_tiles))]
    if e.get("chart_cid"):
        blocks.append(("image", e["chart_cid"]))
    blocks += [("section", "Why (3 reasons)"), ("list", reasons(e)[:3]),
               ("chips", chips),
               ("score", [f"APPROVED · live {plural(live.get('n'), 'trade')}", f"{signed(live.get('total_r'))} so far"]),
               ("buttons", [("Open live chart", e.get("live_chart")), ("Backtest chart", e.get("backtest_chart"))]),
               ("footer", SIGNAL_FOOTER)]
    return mk.render(subj, blocks, [e.get("chart")], "entry")


# ---------------------------------------------------------------- B / D. trade updates ------------------------------
UPDATE = {  # kind -> (icon, banner word, subject head, subject tail, tone)
    "FILLED": ("●", "FILLED", "Filled", "stop active", "teal"),
    "TP1_HIT": ("✓", "TP1 HIT", "TP1 hit", "move stop to entry", "win"),
    "TP": ("✓", "TARGET HIT", "Target hit", "trade closed", "win"),
    "BE": ("=", "REST STOPPED AT ENTRY", "Rest stopped at entry", "closed", "plain"),
    "TRAIL": ("=", "REST STOPPED AT TP1", "Rest stopped at TP1", "closed", "win"),
    "SL": ("✕", "STOP HIT", "Stop hit", "trade closed", "loss"),
    "TIME": ("⏱", "TIME EXIT", "Time exit", "close the rest", "plain"),
    "EXIT_RULE": ("⏹", "EXIT RULE", "Exit rule", "close the rest", "plain"),
    "CANCELLED": ("⊘", "CANCELLED", "Cancelled", "", "plain"),
    "WARNING": ("!", "WARNING", "Warning", "", "amber"),
}
CLOSED_KINDS = ("TP", "BE", "TRAIL", "SL", "TIME", "EXIT_RULE")


def update_kind(x):
    if x["kind"] in ("TP1_HIT", "CANCELLED", "FILLED", "WARNING"):
        return x["kind"]
    r = str(x.get("close_reason") or "")
    return "TP" if r.startswith("TP") else r if r in UPDATE else "EXIT_RULE"


def _update_parts(x, paper):
    """(kind, icon, banner word, subject head, subject tail, tone, big) of one update."""
    k = update_kind(x)
    icon, word, head, tail, tone = UPDATE[k]
    tg = [t for t in x.get("targets") or [] if t is not None]
    if k == "TP":
        n = str(x.get("close_reason"))[2:] or str(len(tg))
        word, head = f"TP{n} HIT", f"TP{n} hit"
    if k == "TRAIL":
        n = max(1, len(tg) - 1)
        word, head = f"REST STOPPED AT TP{n}", f"Rest stopped at TP{n}"
    res = x.get("result_r")
    if k in ("TIME", "EXIT_RULE"):
        tone = "win" if (res or 0) > 0 else "loss" if (res or 0) < 0 else "plain"
    if k == "SL" and res is not None and res >= 0:
        tone = "plain"
    big = signed(x.get("tp1_r")) if k == "TP1_HIT" else signed(res) if k in CLOSED_KINDS else ""
    return k, icon, word, head, tail, ("paper" if paper else tone), big


def _update_do(x, k, paper):
    tg = [t for t in x.get("targets") or [] if t is not None]
    split = x.get("tp_split") or []
    stop_word = "the paper stop" if paper else "the stop"
    if k == "FILLED":
        return [f"Nothing. Check {stop_word} is set at {price(x.get('stop_now'))}."], False
    if k == "TP1_HIT":
        pre = "In your journal: close" if paper else "Close"
        return [f"{pre} {val(split[0] if split else None)}% at {price(tg[0] if tg else None)}.",
                f"Move {stop_word} to {price(x.get('entry'))} (your entry). The rest is then protected at entry."], True
    if k in ("TIME", "EXIT_RULE"):
        why = "The setup ran out of time." if k == "TIME" else "The strategy's exit rule fired."
        return [("In your journal: close" if paper else "Close") + f" the rest at the market price. {why}"], True
    if k == "CANCELLED":
        return [("In your journal: cross it out. " if paper else "Cancel your limit order. ") + "Do not enter."], True
    if k == "WARNING":
        return [f"Your choice – hold with {stop_word}, or close early. The agent does not move your stop."], True
    if k == "SL":
        return ["Nothing. The trade is closed. This was the planned 1R loss."], False
    if k == "BE":
        return ["Nothing. Half won, half closed at break-even."], False
    return ["Nothing. The trade is closed with a win." if (x.get("result_r") or 0) > 0 else
            "Nothing. The trade is closed."], False


def _update_tiles(x, k, paper):
    tg = [t for t in x.get("targets") or [] if t is not None]
    p = "Paper entry" if paper else "Entry"
    if k in CLOSED_KINDS:
        res = x.get("result_r")
        usdt = None if res is None or x.get("risk_usdt") is None else res * float(x["risk_usdt"])
        tiles = [(p, price(x.get("entry")), ""),
                 ("Stopped at" if k in ("SL", "BE", "TRAIL") else "Closed at", price(x.get("exit_price")), ""),
                 ("Held", held(x.get("entered_utc"), x.get("utc")), "")]
        if paper:
            tiles.append(("Result", signed(res, "R", 2), "", "up" if (res or 0) > 0 else "down" if (res or 0) < 0 else None))
        else:
            tiles.append(("Result", signed(usdt, " USDT", 2),
                          "" if res is None or x.get("risk_pct") is None else f"{abs(res) * float(x['risk_pct']):.2g}% of "
                                                                                "account",
                          "up" if (usdt or 0) > 0 else "down" if (usdt or 0) < 0 else None))
        return tiles
    if k == "TP1_HIT":
        nxt = tg[1] if len(tg) > 1 else None
    elif k == "CANCELLED":
        nxt = None
    else:
        nxt = tg[0] if tg else None
        if x.get("tp1_done") and len(tg) > 1:
            nxt = tg[1]
    mv = move_pct(x.get("entry"), x.get("price_now"))
    if mv is not None and x.get("direction") == "SHORT":
        mv = -mv
    n_next = tg.index(nxt) + 1 if nxt in tg else None
    return [(p, price(x.get("entry")), ""),
            ("Price now", price(x.get("price_now")), pct(mv) + " for you" if mv is not None else "",
             "up" if (mv or 0) > 0 else "down" if (mv or 0) < 0 else None),
            ("New paper stop" if paper else "New stop", DASH if k == "CANCELLED" else price(x.get("stop_now")),
             "= entry" if x.get("stop_now") is not None and x.get("stop_now") == x.get("entry") else ""),
            (f"Next target TP{n_next}" if n_next else "Next target", price(nxt),
             (pct(abs(move_pct(x.get("price_now"), nxt) or 0)) + " away") if nxt and x.get("price_now") else "")]


def _timeline(x):
    """TP1: the trade so far - signal, filled, TP1, next."""
    tg = [t for t in x.get("targets") or [] if t is not None]
    z = x.get("entry_zone")
    return [(bj(x.get("signal_utc"), "%H:%M"), "Signal sent" + (f" · entry zone {price(min(z))}–{price(max(z))}" if z
                                                                else ""), "done"),
            (bj(x.get("entered_utc"), "%H:%M"), f"Filled at {price(x.get('entry'))}", "done"),
            (bj(x.get("utc"), "%H:%M"), f"TP1 hit at {price(tg[0] if tg else None)} · "
                                        f"{val((x.get('tp_split') or [None])[0])}% closed", "now"),
            ("next", (f"TP2 {price(tg[1])}, or " if len(tg) > 1 else "") + "stop at entry (no loss)", "next")]


def live_update(x):
    """B. LIVE update: x = dict(coin, quote, direction, tf, strategy, version, kind FILLED / TP1_HIT / CLOSED /
    CANCELLED / WARNING, close_reason, result_r, entry, exit_price, stop_now, targets [prices], tp_split [%], tp1_r,
    price_now, signal_utc, entered_utc, utc, entry_zone, risk_usdt, risk_pct, open, max_open, day_r, week_r,
    cancel_reason, event (WARNING: dict(name, minutes)), tag (why it lost), record (dict(n, won, total_r, streak,
    bt_streak)), live_chart, backtest_chart, chart)."""
    k, icon, word, head, tail, tone, big = _update_parts(x, False)
    coin, side = x["coin"], x["direction"]
    if k == "FILLED":
        mid, tail_txt = f"{coin} {side} at {price(x.get('entry'))}", tail
    elif k == "CANCELLED":
        mid, tail_txt = f"{coin} {side}", x.get("cancel_reason") or "no entry"
    elif k == "WARNING":
        ev = x.get("event") or {}
        mid, tail_txt = f"{coin} {side} open", f"{short_event(ev.get('name'))} in {val(ev.get('minutes'))} min"
    else:
        mid, tail_txt = f"{coin} {side} {big}", tail
    subj = mk.subject([f"LIVE {icon} {head}", mid, tail_txt])
    sub = f"{coin} {side} · {tf_word(x['tf'])} · " + ("no entry was made" if k == "CANCELLED" else
                                                      f"entered {bj(x.get('entered_utc'), '%H:%M')}")
    do, act = _update_do(x, k, False)
    blocks = [("header", ("LIVE", "TRADE UPDATE", when(x.get("utc")))),
              ("banner", dict(title=f"{icon} {word}", sub=sub, big=big, tone=tone)),
              action_box("Do now", do, mk.GREEN if act else mk.GREY_LINE, numbered=True),
              ("tiles", ("grey", _update_tiles(x, k, False)))]
    if k == "TP1_HIT":
        blocks += [("section", "This trade so far"), ("timeline", _timeline(x))]
    if k == "WARNING":
        ev = x.get("event") or {}
        blocks += [("section", "Why this warning"),
                   ("line", f"{short_event(ev.get('name'))} at {bj(ev.get('start_utc'), '%H:%M')} Beijing – big news "
                            "can jump the price through a stop. New trades are blocked ±1 hour; open trades keep their "
                            "stops.")]
    if k == "SL":
        rec = x.get("record") or {}
        ok = None if rec.get("streak") is None or rec.get("bt_streak") is None else rec["streak"] <= rec["bt_streak"]
        blocks += [("section", "Why it lost (engine tag)"),
                   ("line", mk.plain(x.get("tag")) or "No failure tag yet – the daily review looks at it."),
                   ("section", "Is the strategy still OK?"),
                   ("line", ("Yes. " if ok else "Watch it. " if ok is False else "")
                    + f"Live {plural(rec.get('n'), 'trade')}, {val(rec.get('won'))} won, {signed(rec.get('total_r'))}. "
                      f"Losing streak {val(rec.get('streak'))} (backtest worst: {val(rec.get('bt_streak'))}).")]
    if x.get("chart_cid"):
        blocks.append(("image", x["chart_cid"]))
    blocks += [("score", [f"Today {signed(x.get('day_r'))}", f"Week {signed(x.get('week_r'))}",
                          f"Open {val(x.get('open'))} / {val(x.get('max_open'))}"]),
               ("buttons", [("Open live chart", x.get("live_chart")), ("Backtest chart", x.get("backtest_chart"))]),
               ("footer", TRADE_FOOTER)]
    return mk.render(subj, blocks, [x.get("chart")], "update")


# ---------------------------------------------------------------- C. PAPER signal -----------------------------------
def paper_progress(p):
    """The road to real money: (progress block, score block, verdict line) of a paper record p = dict(number (this
    signal's number), closed, won, total_r, avg_r, bt_avg_r, max_div, needed)."""
    need = p.get("needed") or PAPER_NEEDED
    num = p.get("number")
    left = None if num is None else max(0, need - num)
    closed = p.get("closed")
    avg, bt = p.get("avg_r"), p.get("bt_avg_r")
    if not closed:
        verdict = "No paper trade closed yet."
    elif avg is None or bt is None:
        verdict = "Paper average or backtest average missing – no verdict yet."
    else:
        on = avg >= 0 and bt - avg <= (p.get("max_div") if p.get("max_div") is not None else 0.30)
        verdict = f"Paper averages {signed(avg, 'R', 2)} per trade. Paper is {'on track' if on else 'behind'}."
    return (("progress", (f"Paper signal {val(num)} of {need}", f"{val(left)} to go", (num or 0) / need)),
            ("score", [f"Paper so far {val(closed)} · {val(p.get('won'))} won", signed(p.get("total_r"))]),
            ("line", f"Backtest expects {signed(bt, 'R', 2)} per trade. {verdict}"))


def paper_signal(e):
    """C. PAPER signal: the same card as live_entry (a PAPER_TRADING version) + paper = paper_progress()'s record.
    Practice only: no size or USDT, a dashed blue card, never the LIVE green or the word."""
    d = 1 if e["direction"] == "LONG" else -1
    side = "LONG" if d == 1 else "SHORT"
    p = e.get("paper") or {}
    subj = mk.subject([f"PAPER {arrow(e['direction'])} {side} {e['coin']} {tf_word(e['tf'])}",
                       f"#{val(p.get('number'))} of {p.get('needed') or PAPER_NEEDED}", "practice only"])
    prog, score, verdict = paper_progress(p)
    blocks = [("header", ("PAPER", "PRACTICE SIGNAL", when(e.get("utc")))),
              ("banner", dict(title=f"{arrow(e['direction'])} {side} {e['coin']}", tone="paper",
                              sub=f"{e['coin']}/{e.get('quote', 'USDT')} · {tf_word(e['tf'])} · {e['strategy']} "
                                  f"v{e['version']} · PAPER_TRADING",
                              note="PRACTICE ONLY – DO NOT USE REAL MONEY", right=valid_right(e))),
              action_box("Practice now", ["Write it in your paper journal: time, entry, stop, targets.",
                                          "Watch the chart. Would you have entered? Write yes or no and why."],
                         mk.PAPER_BLUE, numbered=True),
              ("section", "The plan"), plan_table(e, paper=True)]
    if e.get("chart_cid"):
        blocks.append(("image", e["chart_cid"]))
    blocks += [("section", "Why (3 reasons)"), ("list", reasons(e)[:3]),
               ("section", "Road to real money"), prog, score, verdict,
               ("buttons", [("Open chart", e.get("live_chart")), ("Paper journal", e.get("journal_url"))]),
               ("footer", PAPER_FOOTER)]
    return mk.render(subj, blocks, [e.get("chart")], "paper", frame="paper")


# ---------------------------------------------------------------- D. PAPER update -----------------------------------
def paper_update(x):
    """D. PAPER update: the same kinds and fields as live_update (a PAPER_TRADING trade) + paper (paper_progress)."""
    k, icon, word, head, tail, tone, big = _update_parts(x, True)
    coin, side = x["coin"], x["direction"]
    p = x.get("paper") or {}
    num = f"#{val(p.get('number'))} of {p.get('needed') or PAPER_NEEDED}"
    if k == "FILLED":
        mid = f"{coin} {side} at {price(x.get('entry'))}"
    elif k in ("CANCELLED", "WARNING"):
        mid = f"{coin} {side}"
    else:
        mid = f"{coin} {side} {big}"
    subj = mk.subject([f"PAPER {icon} {head}", mid, num])
    sub = f"{coin} {side} · {tf_word(x['tf'])} · " + ("no entry was made" if k == "CANCELLED" else
                                                      f"paper entry {price(x.get('entry'))}")
    do, _ = _update_do(x, k, True)
    prog, score, verdict = paper_progress(p)
    blocks = [("header", ("PAPER", "PRACTICE UPDATE", when(x.get("utc")))),
              ("banner", dict(title=f"{icon} {word}", sub=sub, big=big, tone=tone)),
              action_box("Practice now", do, mk.PAPER_BLUE, numbered=True),
              ("tiles", ("grey", _update_tiles(x, k, True)))]
    if k == "WARNING":
        ev = x.get("event") or {}
        blocks += [("line", f"{short_event(ev.get('name'))} in {val(ev.get('minutes'))} min – big news can jump the price "
                            "through a stop.")]
    blocks += [("section", "Strategy paper score"), prog, score, verdict,
               ("buttons", [("Open chart", x.get("live_chart")), ("Paper journal", x.get("journal_url"))]),
               ("footer", PAPER_FOOTER)]
    return mk.render(subj, blocks, [x.get("chart")], "paper", frame="paper")


# ---------------------------------------------------------------- E. PAPER complete ---------------------------------
def paper_complete(c):
    """E. PAPER complete: once, when a version's 20th paper signal closes. c = dict(strategy, version, tf, utc,
    results [R, oldest first], total_r, passed (the engine's approval rules), reasons [why not], rows [(check,
    paper, backtest, ok)], chips [(text, ok)], pack_url, journal_url)."""
    res = c.get("results") or []
    n = len(res)
    passed = bool(c.get("passed"))
    subj = mk.subject([f"PAPER ● {n} of {c.get('needed') or PAPER_NEEDED} done",
                       f"{c['strategy']} {tf_word(c['tf'])} {signed(c.get('total_r'))}",
                       "your decision" if passed else "not passed"])
    if passed:
        dec = [f"Approve {c['strategy']} v{c['version']} {tf_word(c['tf'])} for real-money signals? Reply YES or NO.",
               "Nothing changes until you reply. To say yes, copy the line from the approval pack into config.yaml."]
    else:
        dec = ["None – " + "; ".join(mk.plain(r) for r in (c.get("reasons") or ["the approval rules did not pass"])[:2])
               + "."]
    rows = [[a, b, bt, "✓" if ok else "✗" if ok is False else DASH] for a, b, bt, ok in c.get("rows") or []]
    tones = [[None, None, None, "up" if ok else "down" if ok is False else None] for *_, ok in c.get("rows") or []]
    blocks = [("header", ("PAPER", "PAPER COMPLETE", when(c.get("utc")))),
              ("banner", dict(title=f"{n} paper signals done. " + ("It passed." if passed else "It did not pass."),
                              sub=f"{c['strategy']} v{c['version']} · {tf_word(c['tf'])}", tone="teal_solid")),
              ("squares", ([r > 0 for r in res], "Light = win · dark = loss")),
              action_box("Your decision", dec, mk.TEAL),
              ("section", "Paper vs backtest"),
              ("table", dict(cols=["Check", "Paper", "Backtest", ""], rows=rows, tones=tones, mono=[1, 2])),
              ("chips", c.get("chips") or []),
              ("buttons", [("Approval pack", c.get("pack_url")), ("Paper journal", c.get("journal_url"))]),
              ("footer", "Real money only after YOUR yes. Not financial advice.")]
    return mk.render(subj, blocks, (), "paper", frame="paper")


# ---------------------------------------------------------------- F. ALERT / G. FIXED -------------------------------
def alert(a):
    """F. ALERT (one layout for every system problem): a = dict(title 'Market data unsafe', impact 'signals paused',
    since_utc, auto 'signals paused automatically', utc, nothing (the agent handles it: text after 'Nothing. ') or
    steps [..], broke, impact_long, tried, open_trades, meaning, buttons [(label, url)])."""
    subj = mk.subject([f"! {a['title']}", a.get("impact")])
    since = a.get("since_utc") or a.get("utc")
    fix_by = to_dt(since)
    fix_by = bj(utc_text(fix_by + dt.timedelta(hours=ALERT_FIX_HOURS)), "%H:%M") if fix_by else DASH
    if a.get("steps"):
        do = list(a["steps"])
    else:
        do = [f"Nothing. {a.get('nothing') or 'The agent retries by itself.'}"]
    do.append(f"No 'Fixed' email by {fix_by}? Forward this email to the builder.")
    rows = [("What broke", mk.plain(a.get("broke")) or DASH), ("Impact", mk.plain(a.get("impact_long")) or DASH),
            ("Agent tried", mk.plain(a.get("tried")) or DASH), ("Open trades", a.get("open_trades") or DASH)]
    blocks = [("header", ("ALERT", "SYSTEM", when(a.get("utc")))),
              ("banner", dict(title=f"! {a['title']}", tone="amber",
                              sub=f"Since {bj(since, '%H:%M')} Beijing" + (f" · {a['auto']}" if a.get("auto") else ""))),
              action_box("Do now", do, mk.AMBER, numbered=bool(a.get("steps"))),
              ("kv", rows),
              ("section", "What it means"), ("line", mk.plain(a.get("meaning")) or DASH)]
    if a.get("details"):
        blocks += [("section", "What was found"), ("bullets", [mk.plain(x) for x in a["details"][:3]]
                                                   + ([f"… and {len(a['details']) - 3} more"] if len(a["details"]) > 3
                                                      else []))]
    blocks += [("buttons", a.get("buttons") or []),
               ("footer", "One email per problem, and one 'Fixed' email when it works again. The agent retries by "
                          "itself.")]
    return mk.render(subj, blocks, (), "alert")


def fixed(a):
    """G. FIXED (one per alert): a = dict(thing 'market data', title (the alert's), since_utc, utc, missed, cause,
    buttons)."""
    thing = a.get("thing") or "system"
    missed = a.get("missed")
    subj = mk.subject(["✓ Fixed", f"{thing} OK", f"{val(missed)} signals missed" if missed is not None else None])
    down = held(a.get("since_utc"), a.get("utc"))
    blocks = [("header", ("FIXED", "SYSTEM", when(a.get("utc")))),
              ("banner", dict(title=f"✓ {thing[0].upper() + thing[1:]} OK again", tone="win",
                              sub="It works again. Nothing for you to do.")),
              action_box("Do now", ["None. Nothing for you to do."], mk.GREY_LINE),
              ("tiles", ("grey", [("Down", f"{bj(a.get('since_utc'), '%H:%M')}–{bj(a.get('utc'), '%H:%M')}", "Beijing"),
                                  ("Duration", down, ""), ("Signals missed", val(missed), ""),
                                  ("Cause", mk.plain(a.get("cause")) or DASH, "")])),
              ("buttons", a.get("buttons") or []),
              ("footer", f"Closes the alert '{a.get('title') or thing}' from {bj(a.get('since_utc'), '%H:%M')}.")]
    return mk.render(subj, blocks, (), "fixed")


# ---------------------------------------------------------------- H. BRIEFING 08:20 ---------------------------------
def market_word(btc_trend):
    """BTC up / down / mixed (the daily trend; mixed when 1D and 4H disagree or either is missing)."""
    d, h = (btc_trend or {}).get("1d"), (btc_trend or {}).get("4h")
    if d in BTC_WORD and d == h:
        return BTC_WORD[d]
    return BTC_WORD.get(d, "mixed") if d and not h else "mixed"


def event_rows(events, n=3):
    return [[bj(ev.get("start_utc"), "%a %d · %H:%M"),
             short_event(ev.get("name")) + (f" ({ev['type']})" if ev.get("type") and ev["type"] not in
                                            short_event(ev.get("name")) else "")] for ev in (events or [])[:n]]


def engine_action(b):
    """The ACTION of a report from the engine's state (no guess): open signals, open trades, an approval decision."""
    out = []
    if b.get("signals"):
        out.append(f"Follow the LIVE entry email ({plural(b['signals'], 'signal')}).")
    if b.get("open"):
        out.append(f"Check the stops of your {plural(b['open'], 'open trade')}.")
    for x in (b.get("decisions") or [])[:1]:
        out.append(f"Reply YES or NO: approve {x} for real-money signals?")
    if not out:
        out.append("None." + (" No approved strategy yet." if not b.get("approved") else ""))
    return out


def progress_blocks(sp, one=True):
    """STRATEGY PROGRESS: the status counts per cell and the closest candidate."""
    c = sp.get("counts") or {}
    out = [("line", f"Approved {val(c.get('APPROVED'))} · Paper {val(c.get('PAPER'))} · Testing {val(c.get('TESTING'))} "
                    f"· Failed {val(c.get('FAILED'))}")]
    close = (sp.get("closest") or [])[:1 if one else 3]
    if close:
        out.append(("bars", [(f"Closest: {lab}", v, fr, note) for lab, v, fr, note in close] if one else close))
    return out


def briefing(b):
    """H. BRIEFING 08:20: b = mailfacts.briefing(): slot, utc, signals, open, max_open, data_state, btc (dict(price,
    trend 1d / 4h)), fear_greed, coins [dict(coin, price, regime_1d, change_24h)], events, plan (dict(test, check,
    study)), progress (dict(counts, closest)), last_scan_utc, decisions, approved, summary, page_url, dashboard_url."""
    s = b.get("summary") or {}
    ev = (b.get("events") or [])[:3]
    nxt = ev[0] if ev else None
    btc = b.get("btc") or {}
    n_sig = b.get("signals")
    subj = mk.subject([b.get("slot") or "08:20", "No trade" if not n_sig else plural(n_sig, "signal"),
                       f"BTC {market_word(btc.get('trend'))}",
                       f"{nxt.get('type') or short_event(nxt.get('name'))} {bj(nxt.get('start_utc'), '%a %H:%M')}"
                       if nxt else None])
    head = s.get("headline") or ("Nothing to trade. Wait." if not n_sig else "A LIVE signal – see its entry email.")
    sub = s.get("sub") or ("Claude's summary is missing – engine numbers only." if not s else "")
    tr = btc.get("trend") or {}
    fg = b.get("fear_greed") or {}
    rows, tones = [], []
    for c in b.get("coins") or []:
        ch = c.get("change_24h")
        rows.append([c["coin"], price(c.get("price")), TREND.get(c.get("regime_1d"), DASH), pct(ch, 1)])
        tones.append([None, None, None, None if ch is None or ch == 0 else "up" if ch > 0 else "down"])
    plan = b.get("plan") or {}
    data_ok = b.get("data_state") == "GOOD"
    blocks = [("header", ("BRIEFING", b.get("slot") or "08:20", bj(b.get("utc"), "%a %d %b") + " · Beijing")),
              ("headline", (head, sub)),
              action_box("Action", engine_action(b), mk.GREY_LINE if not (n_sig or b.get("open")) else mk.TEAL),
              ("section", "Market now"),
              ("tiles", ("grey", [("BTC", price(btc.get("price")),
                                   f"1D {BTC_WORD.get(tr.get('1d'), (tr.get('1d') or DASH).lower())} · "
                                   f"4H {BTC_WORD.get(tr.get('4h'), (tr.get('4h') or DASH).lower())}"),
                                  ("Mood (Fear & Greed)", f"{fg.get('label') or ''} {val(fg.get('value'))}".strip(),
                                   f"yesterday {val(fg.get('yesterday'))}")])),
              ("table", dict(cols=["Coin", "Price", "Trend", "24h"], rows=rows, tones=tones, mono=[1, 3]))]
    if ev:
        blocks += [("section", "Next events · no new trades ±1 hour"), ("table", dict(cols=None, rows=event_rows(ev)))]
    blocks += [("section", "Agent plan today"),
               ("kv", [("Test", plan.get("test") or DASH), ("Check", plan.get("check") or DASH),
                       ("Study", plan.get("study") or DASH)]),
               ("section", "Strategy progress")] + progress_blocks(b.get("progress") or {})
    if b.get("held"):
        blocks += [("section", "PAPER signals not emailed (max 3 an hour)"),
                   ("bullets", [mk.plain(x) for x in b["held"][:5]] + ([f"… and {len(b['held']) - 5} more"]
                                                                       if len(b["held"]) > 5 else []))]
    blocks += [("box", dict(title="Do", lines=[s.get("do") or "Wait for a LIVE entry email before any trade."],
                            tone="win")),
               ("box", dict(title="Don't", lines=[s.get("dont") or "Don't trade from headlines or fast candles."],
                            tone="loss")),
               ("line", f"System {'✓ OK' if data_ok else '! check'} · last scan {bj(b.get('last_scan_utc'), '%H:%M')} · "
                        f"data {val(b.get('data_state'))}"),
               ("buttons", [("Full analysis", b.get("page_url")), ("Dashboard", b.get("dashboard_url"))]),
               ("footer", "News, regimes and bull vs bear are in the full analysis. Not financial advice.")]
    return mk.render(subj, blocks, (), "briefing")


# ---------------------------------------------------------------- I. BRIEFING 14:20 / 21:20 ---------------------------
def changes(b):
    """I. BRIEFING 14:20 / 21:20 - changes only: b = dict(slot, prev_slot, utc, changes [(icon, text)], signals, open,
    max_open, btc_trend, next_event, data_state, decisions, approved, page_url). The caller does not send it when
    `changes` is empty."""
    ch = b.get("changes") or []
    n_sig = b.get("signals")
    still = "still no trade" if not n_sig else plural(n_sig, "signal")
    subj = mk.subject([b.get("slot") or "14:20", plural(len(ch), "change"), still])
    nxt = b.get("next_event")
    unchanged = (f"Signals {val(n_sig)} · Open trades {val(b.get('open'))} / {val(b.get('max_open'))} · "
                 f"BTC {market_word(b.get('btc_trend'))}"
                 + (f" · Next event: {nxt.get('type') or short_event(nxt.get('name'))} "
                    f"{bj(nxt.get('start_utc'), '%a %H:%M')}" if nxt else "")
                 + f" · System {'✓ OK' if b.get('data_state') == 'GOOD' else '! check'}")
    blocks = [("header", ("BRIEFING", f"{b.get('slot') or '14:20'} update", bj(b.get("utc"), "%a %d %b") + " · Beijing")),
              ("headline", (f"{plural(len(ch), 'change')} since {b.get('prev_slot') or '08:20'}. "
                            + ("Still no trade." if not n_sig else f"{plural(n_sig, 'signal')}."),
                            f"Only what changed. The {b.get('prev_slot') or '08:20'} briefing still holds for the rest.")),
              action_box("Action", engine_action(b), mk.GREY_LINE if not (n_sig or b.get("open")) else mk.TEAL),
              ("section", "What changed"), ("bullets", [f"{i} {mk.plain(t)}" for i, t in ch]),
              ("section", "Unchanged"), ("line", unchanged),
              ("buttons", [("Full analysis", b.get("page_url"))]),
              ("footer", "No changes at all? This email is skipped. Not financial advice.")]
    return mk.render(subj, blocks, (), "briefing")


# ---------------------------------------------------------------- J. DAILY 23:30 ------------------------------------
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
                "average met – still fails: " + mk.plain((c.get("reasons") or c.get("paper_gate_failed") or [DASH])[0])[:70])
        rows.append((f"{c['strategy']} v{c['version']} {c['tf']}", f"{signed(avg, 'R', 2)} of {signed(need, 'R', 2)}",
                     max(0.0, avg) / need if need > 0 else 0.0, note))
    return rows


def health_line(items):
    """SYSTEM HEALTH: [(text, ok)] -> '✓ Data GOOD · ! 8 tests failing'."""
    return " · ".join(("✓ " if ok else "! ") + mk.plain(t) for t, ok in items) if items else DASH


def daily(d):
    """J. DAILY 23:30: d = mailfacts.daily(): date, utc, live_trades, paper_trades, day_r, week_r, missed (line),
    counts (research counts), status_lines, built_lines, ideas, closest, lessons_added, events, decisions, approved,
    health [(text, ok)], summary, page_url, lesson (dict(title, url)), dashboard_url."""
    s = d.get("summary") or {}
    c = d.get("counts") or {}
    tr = d.get("live_trades") or []
    ideas = d.get("ideas") or []
    nl = d.get("lessons_added")
    subj = mk.subject(["Daily", plural(len(tr), "trade"), f"{val(c.get('backtests'), '{:,}')} backtests",
                       f"{val(nl)} new lesson" + ("" if nl == 1 else "s")])
    head = ("No trades. " if not tr else f"{plural(len(tr), 'trade')}. ") + (
        f"{val(c.get('backtests'), '{:,}')} backtests, {plural(len(ideas), 'new idea')}, {plural(nl, 'lesson')}.")
    act = engine_action(dict(d, signals=None))
    if act == ["None."] or act[0].startswith("None."):
        act = [act[0] + " Read the lesson when you have 2 minutes."]
    lesson = d.get("lesson") or {}
    nxt_ev = (d.get("events") or [None])[0]
    watch = s.get("watch") or ("; ".join(x for x in [
        f"{nxt_ev.get('type') or short_event(nxt_ev.get('name'))} {bj(nxt_ev.get('start_utc'), '%a %H:%M')}" if nxt_ev
        else None, d.get("research_time") and f"research run {d['research_time']}"] if x) or DASH)
    blocks = [("header", ("DAILY", "23:30 review", bj(d.get("utc"), "%a %d %b") + " · Beijing")),
              ("headline", (head, s.get("sub") or "")),
              action_box("Action", act, mk.GREY_LINE if act[0].startswith("None.") else mk.TEAL),
              ("section", "1 · Trading today"),
              ("tiles", ("grey", [("Live", str(len(tr)), "closed trades"), ("Paper", str(len(d.get("paper_trades") or [])),
                                                                              "closed"),
                                  ("Day", signed(d.get("day_r")), "live R"), ("Week", signed(d.get("week_r")), "live R")])),
              ("line", "Missed moves: " + (d.get("missed") or "none recorded today.")),
              ("section", "2 · What the agent did"),
              ("tiles", ("teal", [("Backtests", val(c.get("backtests"), "{:,}"), "runs"),
                                  ("Strategies", val(c.get("strategies")), "applied"),
                                  ("Coins", val(c.get("coins")), "tested"), ("New ideas", str(len(ideas)), "built")])),
              ("kv", [("Status", "; ".join(d.get("status_lines") or []) or "no status change today"),
                      ("Built", "; ".join(d.get("built_lines") or []) or "nothing new today")])]
    if ideas:
        blocks.append(("ideas", ideas))
    close = d.get("closest") or []
    blocks += [("section", "3 · Closest to passing"), ("bars", close[:3]) if close else ("line", DASH),
               ("section", "4 · Learned today"),
               ("box", dict(title="Lesson of the day", lines=[s.get("lesson") or DASH], tone="teal")),
               ("section", "5 · Tomorrow"),
               ("kv", [("Watch", watch), ("Avoid", s.get("avoid") or s.get("tomorrow") or DASH),
                       ("Learn", f"Your 2-min lesson: {lesson['title']}" if lesson.get("title") else DASH)]),
               ("section", "System health"), ("line", health_line(d.get("health"))),
               ("buttons", [("Full review", d.get("page_url")),
                            ("Beginner lesson", lesson["url"]) if lesson.get("url") else ("Dashboard", d.get("dashboard_url"))]),
               ("footer", "Losses, missed moves and idea chains are in the full review. Not financial advice.")]
    return mk.render(subj, blocks, (), "daily")


# ---------------------------------------------------------------- K. WEEKLY -----------------------------------------
def weekly(w):
    """K. WEEKLY (Sunday): w = mailfacts.weekly(): week_no, utc, days, live (dict(n, total_r)), paper (dict(n,
    total_r)), week_r, missed (dict(n, text)), funnel (counts), closest, decision [dict(cell, pack_url, chart_url)],
    learned (dict(mistakes, testing, online, blocked)), history [(day, text)], tests (line), card (dict(sources,
    data_ok, data_problems)), next (dict(test, fix, study, events)), summary, page_url, dashboard_url."""
    s = w.get("summary") or {}
    f = w.get("funnel") or {}
    close = w.get("closest") or []
    subj = mk.subject([f"Week {w.get('week_no', DASH)}", f"{val(f.get('APPROVED'))} approved",
                       f"closest: {close[0][0].split(' v')[0]} {close[0][0].split(' ')[-1].upper()}" if close else None])
    dec = w.get("decision") or []
    if dec:
        x = dec[0]
        dec_lines = [f"Approve {x['cell']} for real-money signals? Reply YES or NO."] + (
            [f"{len(dec) - 1} more waiting – see the dashboard."] if len(dec) > 1 else [])
    else:
        dec_lines = ["None this week."]
    live, paper, missed = w.get("live") or {}, w.get("paper") or {}, w.get("missed") or {}
    le = w.get("learned") or {}
    card = w.get("card") or {}
    dp = card.get("data_problems")
    nx = w.get("next") or {}
    blocks = [("header", ("WEEKLY", f"Week {w.get('week_no', DASH)}", w.get("days") or DASH)),
              ("headline", (s.get("headline") or f"{val(f.get('APPROVED'))} strategies approved so far.",
                            s.get("sub") or "The agent's report card for the week.")),
              action_box("Your decision", dec_lines, mk.TEAL if dec else mk.GREY_LINE)]
    if dec:
        blocks.append(("buttons", [("Approval pack", dec[0].get("pack_url")), ("Backtest chart", dec[0].get("chart_url"))]))
    blocks += [("section", "1 · Results"),
               ("tiles", ("grey", [("Live", val(live.get("n")), signed(live.get("total_r"))),
                                   ("Paper", val(paper.get("n")), signed(paper.get("total_r"))),
                                   ("Week", signed(w.get("week_r")), "live R"),
                                   ("Missed", val(missed.get("n")), missed.get("text") or "")])),
               ("section", "2 · Road to real signals"),
               ("tiles", ("teal", [("Tested", val(f.get("TESTED")), "cells"), ("Testing", val(f.get("TESTING")), ""),
                                   ("Paper", val(f.get("PAPER")), ""), ("Approved", val(f.get("APPROVED")), "")])),
               ("line", f"Strategy × timeframe cells. {val(f.get('FAILED'))} failed for real reasons.")]
    if close:
        blocks.append(("bars", close[:3]))
    blocks += [("section", "3 · Learned this week"),
               ("label", "From mistakes"), ("bullets", le.get("mistakes") or ["none recorded"]),
               ("label", "From testing"), ("bullets", le.get("testing") or ["no new lesson"]),
               ("label", "From online"), ("bullets", (le.get("online") or ["no new source"])
                                          + ([f"! {le['blocked']}"] if le.get("blocked") else [])),
               ("section", "4 · Agent progress history"),
               ("table", dict(cols=None, rows=[[a, b] for a, b in (w.get("history") or [])] or [[DASH, "no entries"]])),
               ("line", w.get("tests") or DASH),
               ("section", "5 · Agent report card"),
               ("kv", [("Research sources read", val(card.get("sources"))),
                       ("Data sources", DASH if dp is None else "✓ All OK" if not dp else "! " + ", ".join(dp[:3])),
                       ("Self-improvement idea", s.get("improvement") or DASH)]),
               ("section", "6 · Next week"),
               ("kv", [("Test", s.get("test") or nx.get("test") or DASH), ("Fix", s.get("fix") or nx.get("fix") or DASH),
                       ("Study", s.get("study") or nx.get("study") or DASH), ("Events", nx.get("events") or DASH)]
                + ([("Plan", s["next"])] if s.get("next") else [])),
               ("buttons", [("Full weekly research", w.get("page_url")), ("Dashboard", w.get("dashboard_url"))]),
               ("footer", "Progress history comes from memory/changelog.md and merged PRs. Not financial advice.")]
    return mk.render(subj, blocks, (), "weekly")
