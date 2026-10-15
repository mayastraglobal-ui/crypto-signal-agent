"""
The Signal Center (Forward Test Program PR 2, operator plan 2026-10-09): 🔵 TEST alerts on the live chart.

A TEST alert is a setup of a Forward Test Program strategy (strategies_program.yaml) on a coin where that strategy /
version / timeframe was POSITIVE in the 5-year backtest after fees (reports/program.json, written by the research
run). It is not paper trading and not a proven strategy: it shows the setup as it forms, so the operator can watch
it, and every TEST setup is recorded (the hourly scan's signals log, stage TEST) so the weekly review (PR 3) can
measure the live results and promote the best to PAPER with the operator's tap.

  * which pairs qualify: the coin had >= min_coin_trades backtest trades, an average above 0R after fees, and its
    unseen-test part was not negative (test_list);
  * a cell that is already PAPER / APPROVED alerts with its own label instead (VALIDATION cells send TEST alerts);
    a FAILED cell still qualifies on a positive coin (it may have failed on other coins), but never once its live
    results failed it (the same live record that pauses any strategy: 20 signals averaging below -0.10R);
  * one alert per coin + direction + strategy (the best version / timeframe; the others are named) - merge();
  * at most max_per_day TEST alerts per Beijing day, the best first; on 30m and faster a 5m candle must confirm first
    (live watcher; 4H / 1H alert at the candle close since 2026-10-15 - needs_5m);
  * 🌊 at most wave_max alerts per wave: the same direction within wave_hours (wave_filter);
  * ⭐ when another timeframe or strategy gave the same coin and direction within agree_hours;
  * ⚠️ when the trade goes against the daily regime (1W / 1D never block a TEST alert - they are context).
Pure functions only: no internet, no files.
"""
import datetime as dt
import math

DEFAULTS = dict(enabled=True, min_coin_trades=20, min_avg_r=0.0, test_min_trades=5, max_per_day=10,
                cooldown_minutes=240, confirm_5m=True, agree_hours=4, watch_notes=True, watch_max_per_day=12,
                alert_skip_failed=True, alert_min_avg_r=0.10, library_tests=(),
                confirm_5m_tfs=("30m", "15m", "5m"), wave_max=2, wave_hours=8)
BJ = dt.timezone(dt.timedelta(hours=8))
OWN_LABEL = ("PAPER_TRADING", "APPROVED")      # these alert as 🟡 PAPER / 🟢 LIVE instead (VALIDATION does not alert)


def settings(section):
    s = dict(DEFAULTS)
    s.update({k: v for k, v in (section or {}).items() if k in DEFAULTS})
    for k in ("min_coin_trades", "test_min_trades", "max_per_day", "cooldown_minutes", "agree_hours",
              "watch_max_per_day"):
        s[k] = int(s[k])
    s["min_avg_r"] = float(s["min_avg_r"])
    s["alert_min_avg_r"] = float(s["alert_min_avg_r"])
    s["alert_skip_failed"] = bool(s["alert_skip_failed"])
    s["library_tests"] = [str(x) for x in (s.get("library_tests") or [])]
    s["confirm_5m_tfs"] = [str(x) for x in (s.get("confirm_5m_tfs") or [])]
    s["wave_max"], s["wave_hours"] = int(s["wave_max"]), float(s["wave_hours"])
    return s


def needs_5m(tf, S):
    """Does a TEST setup on this timeframe wait for its 5m candle? 2026-10-15 (operator: "remove 5m check for 4H and
    1H"): only the timeframes in confirm_5m_tfs (default 30m and faster). The 4H / 1H strategies were proven in the
    5-year backtest WITHOUT a 5m check, and over the 90 days to 15 Oct the setups it threw away did as well as the
    ones it kept (4H +0.65R vs +0.52R a trade) while it removed 5 of 6."""
    return bool(S.get("confirm_5m")) and tf in (S.get("confirm_5m_tfs") or [])


def wave_filter(tests, waves, now_ms, S):
    """🌊 One alert per wave (2026-10-15): TEST alerts in the same direction within wave_hours of the first one are a
    wave (a market-wide move gives 8-11 setups at once); only the first wave_max are sent, the strongest backtest
    evidence first when several come together. The 90 days to 15 Oct: 2 per wave kept +29R of +43R with a worst drop
    of 6.8R instead of 17.5R. waves: {"1" / "-1": {start, n, note}} (changed in place). wave_max 0 = off.
    Returns (send, over) - each sent alert gets a['wave'] = (number in the wave, wave_max)."""
    if int(S.get("wave_max") or 0) <= 0:
        return list(tests), []
    send, over = [], []
    span = float(S["wave_hours"]) * 3_600_000
    for a in sorted(tests, key=lambda x: -float((x.get("test") or {}).get("score") or 0)):
        k = str(int(a["d"]))
        w = waves.get(k)
        if w is None or now_ms - int(w["start"]) > span:
            w = waves[k] = dict(start=int(now_ms), n=0, note=False)
        if w["n"] < S["wave_max"]:
            w["n"] += 1
            a["wave"] = (w["n"], S["wave_max"])
            send.append(a)
        else:
            over.append(a)
    return send, over


def wave_text(over, wave_max):
    """The one note per wave for the setups over the wave maximum (information only, no buttons)."""
    d = int(over[0]["d"])
    side = "LONG" if d == 1 else "SHORT"
    items = ", ".join(f"{a['coin']} ({a['strategy']} {a['tf']})" for a in over)
    return (f"🌊 <b>Wave: more {side} setups</b>\n"
            f"Also signalling {side}: {items}.\n"
            f"You already got the first {wave_max} alerts of this wave - the market moves together, so more of the same "
            f"trade mostly adds risk. Not sent as trades; GitHub records them.\n"
            "<i>Information only.</i>")


def score(n, avg_r):
    """How strong the backtest evidence is: the average after fees times the square root of the trades (a t-like
    number: +0.3R over 100 trades beats +0.5R over 10)."""
    return round(float(avg_r) * math.sqrt(max(0, int(n))), 3)


def qualifies(row, S):
    """True when one coin row of reports/program.json is positive enough for TEST alerts."""
    if not row or int(row.get("n") or 0) < S["min_coin_trades"] or float(row.get("avg_r") or 0) <= S["min_avg_r"]:
        return False
    tn, ta = int(row.get("test_n") or 0), row.get("test_avg_r")
    return not (tn >= S["test_min_trades"] and ta is not None and float(ta) < 0)


def library_rows(research, keys):
    """🔵 TEST rows for library strategies the operator named (signal_center.library_tests, e.g. the 6 Oct
    "4H trend + 1H entry" TRD-H4-BREAKOUT-S3@1.0|1h: +0.15R over 939 trades, blocked from PAPER only by its drawdown).
    research: reports/research.json (the nightly 5-year results). Returns {'id@ver|tf': row} in the layout of
    reports/program.json, so test_list / alert_list treat them like program cells (the same per-coin bar). The coins'
    unseen-test part is not split per coin in research.json, so that check is skipped for these rows."""
    out = {}
    cells = (research or {}).get("cells") or {}
    for ck in keys or []:
        c = cells.get(ck)
        if not c:
            continue
        ev = c.get("evidence") or {}
        sid, rest = ck.split("@", 1)
        coins = {coin: dict(n=int(x.get("n") or 0), avg_r=float(x.get("avg_r") or 0), win_rate=x.get("win_rate"),
                            test_n=0, test_avg_r=None, positive=bool(float(x.get("avg_r") or 0) > 0))
                 for coin, x in (ev.get("by_coin") or {}).items()}
        out[ck] = dict(strategy=sid, name=sid, version=rest.split("|")[0], tf=c.get("tf") or rest.split("|")[1],
                       status=c.get("status"), trades=int((ev.get("all") or {}).get("n") or 0),
                       avg_r=float((ev.get("all") or {}).get("avg_r") or 0),
                       test_avg_r=(ev.get("validate") or {}).get("avg_r"), tested_utc=research.get("run_utc"),
                       library=True, coins=coins)
    return out


def with_library(program, lib):
    """reports/program.json with the library TEST rows added (a copy; program.json itself never changes)."""
    if not lib:
        return program
    p = dict(program or {})
    p["cells"] = dict((program or {}).get("cells") or {}, **lib)
    return p


def alert_list(tests, program, reg_cells, S):
    """Which of test_list() reach Telegram (2026-10-13, operator: "too many messages", a TEST SHORT at the bottom).
    18 of the 30 TEST cells were FAILED overall and alerted only because one or two coins came out slightly positive
    (e.g. P01-BREAKOUT-V5 1h: -0.02R over 3,762 trades, ETH +0.01R over 717 - a coin flip). Telegram now gets only
    cells that are not FAILED and positive overall, on coins averaging >= alert_min_avg_r after fees. GitHub keeps
    recording every TEST setup of test_list() (the weekly review is unchanged)."""
    out = {}
    for ck, coins in (tests or {}).items():
        row = ((program or {}).get("cells") or {}).get(ck) or {}
        st = (reg_cells.get(ck) or {}).get("status") or row.get("status")
        if S["alert_skip_failed"] and (st == "FAILED" or float(row.get("avg_r") or 0) <= 0):
            continue
        keep = {c: x for c, x in coins.items() if float(x["avg_r"]) >= S["alert_min_avg_r"]}
        if keep:
            out[ck] = keep
    return out


def test_list(program, reg_cells, S, promoted=None):
    """{'id@ver|tf': {coin: stats}} - the program cells x coins that may send TEST alerts.
    program: reports/program.json (or None); reg_cells: the registry's cells (status, gates_failed);
    promoted: {'id@ver|tf': [coins]} promoted to PAPER by the operator (PR 3) - PAPER only on those coins, so the
    cell's other positive coins stay TEST."""
    out = {}
    if not S.get("enabled") or not program:
        return out
    for ck, row in (program.get("cells") or {}).items():
        if row.get("version") == "C":                     # a control version is a benchmark, never an alert
            continue
        cell = reg_cells.get(ck) or {}
        st = cell.get("status") or row.get("status")
        promo = (promoted or {}).get(ck)
        if (st in OWN_LABEL and promo is None) or st == "RETIRED" or \
                "LIVE results bad" in str(cell.get("gates_failed") or ""):
            continue
        coins = {}
        for coin, x in (row.get("coins") or {}).items():
            if promo is not None and coin in promo:
                continue                                   # 🟡 PAPER on this coin (promoted)
            if qualifies(x, S):
                coins[coin] = dict(n=int(x["n"]), win_rate=float(x.get("win_rate") or 0), avg_r=float(x["avg_r"]),
                                   test_avg_r=x.get("test_avg_r"), score=score(x["n"], x["avg_r"]),
                                   strategy=row.get("strategy"), name=row.get("name"), version=row.get("version"))
        if coins:
            out[ck] = coins
    return out


def scan_stage(status, tests, cell_key, coin, promoted=None):
    """The hourly scan's record stage of one signal: (stage, TEST stats). VALIDATION / PAPER / APPROVED keep their
    stage - except a cell promoted to PAPER by the operator (PR 3), which is PAPER only on its promoted coins; a TEST
    pair (positive on this coin) is recorded as TEST; anything else is not recorded (None, None)."""
    promo = (promoted or {}).get(cell_key)
    if status in ("VALIDATION", "PAPER_TRADING", "APPROVED") and not (promo is not None and coin not in promo):
        return status, None
    tst = ((tests or {}).get(cell_key) or {}).get(coin)
    return ("TEST", tst) if tst is not None else (None, None)


def group_key(a):
    """One TEST alert per coin + direction + program strategy."""
    return f"TEST|{a['coin']}|{a['d']}|{(a.get('test') or {}).get('strategy') or a['strategy']}"


def merge(cands):
    """TEST candidates of one pass -> one per coin + direction + strategy (the best score), the others listed in
    'also' as 'V2 1h'. Returns the kept candidates, best first."""
    groups = {}
    for a in cands:
        groups.setdefault(group_key(a), []).append(a)
    out = []
    for g in groups.values():
        g = sorted(g, key=lambda a: -float((a.get("test") or {}).get("score") or 0))
        best = dict(g[0])
        best["also"] = [f"{(a.get('test') or {}).get('version') or a['strategy']} {a['tf']}" for a in g[1:]]
        out.append(best)
    return sorted(out, key=lambda a: -float((a.get("test") or {}).get("score") or 0))


def agreement(a, recent, now_ms, S, others=()):
    """Other timeframes / strategies that gave the same coin and direction within agree_hours (recent: remembered
    alerts [{coin, d, tf, strategy, sent_ms}], others: this pass's candidates). ['1h P01', ...]"""
    cut = now_ms - S["agree_hours"] * 3_600_000
    seen = set()
    for x in list(recent) + list(others):
        if x is a or x.get("coin") != a["coin"] or int(x.get("d") or 0) != a["d"]:
            continue
        if int(x.get("sent_ms") or now_ms) < cut:
            continue
        if x.get("tf") == a["tf"] and x.get("strategy") == a["strategy"]:
            continue
        seen.add(f"{x['tf']} {str(x.get('strategy') or '').split('-')[0]}")
    return sorted(seen)


def bj_day(ms):
    return dt.datetime.fromtimestamp(ms / 1000, BJ).strftime("%Y-%m-%d")


def sent_today(sent_ms_list, now_ms):
    day = bj_day(now_ms)
    return sum(1 for m in sent_ms_list if bj_day(int(m)) == day)


def cap(cands, already_today, S):
    """(sent now, dropped) - at most max_per_day TEST alerts per Beijing day, the strongest evidence first."""
    room = max(0, S["max_per_day"] - int(already_today))
    ranked = sorted(cands, key=lambda a: -float((a.get("test") or {}).get("score") or 0))
    return ranked[:room], ranked[room:]


def direction_of(label):
    from engine import regime as rg
    return 1 if label in rg.BULL else (-1 if label in rg.BEAR else 0)


def against_daily(d, recs):
    """'1D WEAK_BULL' when the trade goes against the daily regime (context only - it never blocks)."""
    lab = ((recs or {}).get("1d") or {}).get("label")
    return f"1D {lab}" if lab and direction_of(lab) == -d else None


def market_type(recs, permission=None):
    """Idea 1: the market at the alert, saved with it - the coin's verdict (UP / DOWN / RANGE / CHOPPY, the same as
    the market weather) and the 1D / 4H / 1H labels, e.g. 'DOWN (1D WEAK_BULL, 4H WEAK_BEAR, 1H STRONG_BEAR)'."""
    from engine import regime as rg
    from engine import weather as wx
    if permission is None:
        permission = rg.permission(recs)[0] if recs else None
    v = wx.coin_verdict(recs, permission)
    labs = ", ".join(f"{tf.upper()} {((recs or {}).get(tf) or {}).get('label') or '?'}" for tf in ("1d", "4h", "1h"))
    return f"{v} ({labs})"


def weather_line(w, coin):
    """'Choppy day · BTC: down' from reports/market_weather.json (None when there is no file)."""
    if not w or not w.get("verdict"):
        return None
    c = next((x for x in w.get("coins") or [] if x.get("coin") == coin), None)
    from engine import weather as wx
    return f"{w['verdict'].get('icon', '')} {w['verdict'].get('title', '')}".strip() + \
        (f" · {coin}: {wx.coin_word(c)}" if c else "")
