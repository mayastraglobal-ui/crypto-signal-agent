"""
Risk engine (AGENT_PROMPT.md sections 14 steps 9-13 and 15) - Phase 11.

Independent of signal generation: the strategies find signals, this module decides whether the account
may take one NOW and how big it may be. Fixed rules only; it never changes a strategy, never increases a
size because of "confidence", and never looks at earlier wins or losses to size a trade.

  blackout        no entry within +-60 min of a high-impact event (calendar: events.yaml + config.yaml -> events)
  day / week      closed LIVE results today <= -3R or this week <= -6R -> no new entries
  suspended       a strategy version x timeframe whose live drawdown exceeds 8R (until the operator resumes it)
  heat            <= 3 open live positions, <= 1 per coin, <= 1 per group of correlated coins and direction
  rr_tp1          reward to TP1 >= 2R (never widen the stop to get there)
  path            no opposing liquidity pool / support-resistance level between entry and TP1
  duplicate       no second signal of the same strategy / coin / timeframe while one is open or cooling down
Position size = equity x risk% / |entry - stop|; risk% capped (0.5% in the first live month, never above 1%),
leverage capped at 3x by making the position SMALLER.

Pure functions: no internet, no files.
"""
import datetime as dt
import os

import numpy as np
import pandas as pd

DEFAULTS = dict(
    blackout_minutes=60,          # section 14 step 11
    day_limit_r=-3.0,             # section 15 drawdown controls
    week_limit_r=-6.0,
    strategy_max_dd_r=8.0,
    strategy_dd_limits={},        # Phase 19 A: "id@version|tf": limit in R from the family table (only when it is active)
    max_positions=3,              # portfolio heat
    max_per_coin=1,
    corr_threshold=0.7,           # 1h returns over corr_bars: >= 0.7 -> one exposure
    corr_bars=720,                # 30 days of 1h candles
    min_tp1_r=2.0,                # section 14 step 9
    path_margin_r=0.05,           # a level within 0.05R of TP1 counts as the target itself, not in the way
    max_risk_pct=1.0,             # section 15: never above 1%
    first_month_risk_pct=0.5,     # 0.5% while validating and in the first live month
    first_month_days=30,
    max_leverage=3.0,
    calendar_horizon_days=7,      # warn when no event is listed for the coming 7 days
    resume={},                    # "id@version|tf": "YYYY-MM-DD" - operator resumes a suspended strategy
)
STEPS = {   # step name -> text (section 14 numbering)
    "blackout": "14.11 high-impact event within ±60 min",
    "day_halt": "15 daily loss limit reached (-3R) - no new entries today",
    "week_halt": "15 weekly loss limit reached (-6R) - no new entries this week",
    "suspended": "15 strategy suspended (live drawdown > 8R)",
    "heat": "14.12 portfolio heat: 3 positions already open",
    "coin": "14.12 already a position on this coin",
    "correlated": "14.12 already exposed in the same direction through a correlated coin",
    "rr_tp1": "14.9 reward to TP1 below 2R",
    "path": "14.10 opposing level between entry and TP1",
    "duplicate": "14.13 same strategy / coin / timeframe still open or cooling down",
}
LIVE_OPEN = ("AWAITING_5M", "ENTRY_TRIGGERED", "POSITION_ACTIVE", "TP1_HIT")


def settings(risk_section, events=None):
    s = dict(DEFAULTS)
    s.update(risk_section or {})
    s["resume"] = dict(s.get("resume") or {})
    s["strategy_dd_limits"] = dict(s.get("strategy_dd_limits") or {})
    s["events"] = parse_events(events)
    return s


def _ms(txt):
    return int(pd.Timestamp(str(txt), tz="UTC").value // 1_000_000)


CALENDAR_FILE = "events.yaml"       # the event calendar file at the repository root (read with config.yaml -> events)


def load_calendar(path):
    """The events list of events.yaml ([] when the file does not exist). A file that cannot be read raises
    ValueError, which the scan reports (the blackout is then off - never silently)."""
    import yaml
    if not os.path.exists(path):
        return []
    try:
        with open(path) as f:
            doc = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"{os.path.basename(path)} is not valid YAML: {e}")
    items = doc.get("events") if isinstance(doc, dict) else None
    if items is None:
        return []
    if not isinstance(items, list) or not all(isinstance(e, dict) for e in items):
        raise ValueError(f"{os.path.basename(path)}: 'events' must be a list of {{utc, type, name}} entries")
    return items


def parse_events(items):
    """config.yaml -> events: [{utc: "2026-10-14 12:30", type: CPI, name: ...}] or, for an exchange incident,
    {from: ..., until: ..., type: exchange_incident, name: ...}. Returns [(start_ms, end_ms, type, name)];
    a bad entry raises ValueError (shown in the report, never silently skipped)."""
    out = []
    for i, e in enumerate(items or []):
        try:
            if "utc" in e:
                a = b = _ms(e["utc"])
            else:
                a, b = _ms(e["from"]), _ms(e["until"])
            if b < a:
                raise ValueError("until is before from")
            out.append((a, b, str(e.get("type", "event")), str(e.get("name", e.get("type", "event")))))
        except Exception as x:
            raise ValueError(f"events entry {i + 1} ({e}): {x}")
    return sorted(out)


def blackout(t_ms, events, minutes):
    """Events whose +-minutes window contains t_ms (an incident: its whole from-until span, +- minutes)."""
    w = minutes * 60_000
    return [e for e in events if e[0] - w <= t_ms <= e[1] + w]


def upcoming(events, now_ms, days):
    return [e for e in events if e[1] >= now_ms and e[0] <= now_ms + days * 86_400_000]


def _live(logdf):
    if logdf is None or logdf.empty:
        return pd.DataFrame(columns=list(logdf.columns) if logdf is not None else [])
    return logdf[logdf["stage"] == "APPROVED"]


def _closed_r(live):
    d = live[(live["state"] == "CLOSED") & live["result_r"].notna()].copy()
    d["result_r"] = d["result_r"].astype(float)
    return d


def day_week_r(logdf, now):
    """Closed LIVE (APPROVED) results today and this week (Monday-Sunday, UTC)."""
    d = _closed_r(_live(logdf))
    today = now.strftime("%Y-%m-%d")
    week0 = (now - dt.timedelta(days=now.weekday())).strftime("%Y-%m-%d")
    day = d.loc[d["closed_time_utc"].astype(str).str[:10] == today, "result_r"].sum()
    week = d.loc[d["closed_time_utc"].astype(str).str[:10] >= week0, "result_r"].sum()
    return round(float(day), 3), round(float(week), 3)


def drawdowns(logdf, resume=None):
    """Live drawdown (R, from the best point) per 'id@version|tf', counting only trades closed after the
    operator's resume date for that key."""
    resume = resume or {}
    d = _closed_r(_live(logdf))
    out = {}
    if d.empty:
        return out
    d["version"] = d["version"].fillna("1.0").astype(str)
    for (s, v, tf), g in d.sort_values("closed_time_utc").groupby(["strategy", "version", "tf"]):
        key = f"{s}@{v}|{tf}"
        if key in resume:
            g = g[g["closed_time_utc"].astype(str).str[:10] >= str(resume[key])]
        eq = np.cumsum(np.r_[0.0, g["result_r"].to_numpy()])
        out[key] = round(float((np.maximum.accumulate(eq) - eq).max()), 3)
    return out


def corr_groups(closes, threshold, bars):
    """Groups of coins whose 1h returns (last `bars`) correlate >= threshold, joined transitively.
    closes: {coin: pd.Series of 1h closes indexed by close time}. Returns {coin: group name}."""
    coins = sorted(closes)
    rets = pd.DataFrame({c: closes[c].iloc[-(bars + 1):].pct_change() for c in coins}).dropna(how="all")
    parent = {c: c for c in coins}

    def root(c):
        while parent[c] != c:
            c = parent[c]
        return c
    if len(coins) > 1 and len(rets) > 30:
        cm = rets.corr(min_periods=30)
        for i, a in enumerate(coins):
            for b in coins[i + 1:]:
                if np.isfinite(cm.at[a, b]) and cm.at[a, b] >= threshold:
                    parent[root(b)] = root(a)
    groups = {}
    for c in coins:
        groups.setdefault(root(c), []).append(c)
    return {c: "+".join(sorted(groups[root(c)])) for c in coins}


def risk_pct(cfg_pct, logdf, now, S):
    """The risk % actually used: the config value, capped at 1%, and at 0.5% until 30 days after the first
    LIVE entry (no live entry yet = still validating). Returns (pct, note)."""
    pct, notes = float(cfg_pct), []
    if pct > S["max_risk_pct"]:
        notes.append(f"config risk {pct:g}% is above the {S['max_risk_pct']:g}% maximum - capped")
        pct = S["max_risk_pct"]
    live = _live(logdf)
    started = live["entry_time_utc"].dropna().astype(str) if "entry_time_utc" in live else pd.Series(dtype=str)
    started = started[started != ""]
    first = pd.Timestamp(started.min(), tz="UTC") if len(started) else None
    if first is None or now - first.to_pydatetime() < dt.timedelta(days=S["first_month_days"]):
        if pct > S["first_month_risk_pct"]:
            notes.append(f"first live month: {S['first_month_risk_pct']:g}% maximum")
            pct = S["first_month_risk_pct"]
    return pct, "; ".join(notes)


def size(equity, pct, entry, stop, max_leverage):
    """Position size (section 15). Never larger than max_leverage x equity: a tighter stop gives a SMALLER
    risk instead. Returns dict(qty, notional, leverage, risk_usdt, capped)."""
    R = abs(entry - stop)
    qty = equity * pct / 100 / R if R > 0 else 0.0
    capped = qty * entry > max_leverage * equity
    if capped:
        qty = max_leverage * equity / entry
    return dict(qty=qty, notional=qty * entry, leverage=qty * entry / equity, risk_usdt=qty * R, capped=capped)


def path_blocked(d, entry, tp1, R, levels, margin_r):
    """True when an OPPOSING level (long: pools / resistance above, short: below) lies between entry and TP1."""
    lim = tp1 - d * margin_r * R
    for x in levels:
        if x is not None and np.isfinite(x) and d * (x - entry) > 0 and d * (lim - x) > 0:
            return True
    return False


class Book:
    """The account's risk state during one run: what is open live, and what this run already accepted."""

    def __init__(self, logdf, now, S, groups):
        self.S, self.now, self.groups = S, now, groups
        self.day_r, self.week_r = day_week_r(logdf, now)
        self.dd = drawdowns(logdf, S["resume"])
        live = _live(logdf)
        is_open = live["state"].isin(LIVE_OPEN) if "state" in live else pd.Series(False, index=live.index)
        self.open = [dict(coin=r["coin"], direction=r["direction"]) for _, r in live[is_open].iterrows()]
        self.logdf = logdf

    def dd_limit(self, key):
        """The live drawdown limit of one strategy version x timeframe: its family-table limit when the family table
        is active (Phase 19 A: the card's own Monte Carlo 95% drawdown per 100 trades), else strategy_max_dd_r."""
        return float(self.S.get("strategy_dd_limits", {}).get(key, self.S["strategy_max_dd_r"]))

    def suspended(self):
        return sorted(k for k, v in self.dd.items() if v > self.dd_limit(k))

    def halts(self):
        out = []
        if self.day_r <= self.S["day_limit_r"]:
            out.append("day_halt")
        if self.week_r <= self.S["week_limit_r"]:
            out.append("week_halt")
        return out

    def check(self, p, cooldown_ms=0):
        """Section 14 steps 9-13 + section 15 for one plan (dict with coin, timeframe, strategy, version,
        direction, entry, stop, tp1, signal_ms, levels). Returns the failed steps (empty = allowed)."""
        S, fails = self.S, []
        d = 1 if p["direction"] == "LONG" else -1
        R = abs(p["entry"] - p["stop"])
        if blackout(p["signal_ms"], S["events"], S["blackout_minutes"]) or \
                blackout(int(self.now.timestamp() * 1000), S["events"], S["blackout_minutes"]):
            fails.append("blackout")
        fails += self.halts()
        if f"{p['strategy']}@{p['version']}|{p['timeframe']}" in self.suspended():
            fails.append("suspended")
        if len(self.open) >= S["max_positions"]:
            fails.append("heat")
        if sum(o["coin"] == p["coin"] for o in self.open) >= S["max_per_coin"]:
            fails.append("coin")
        g = self.groups.get(p["coin"], p["coin"])
        if any(o["coin"] != p["coin"] and self.groups.get(o["coin"], o["coin"]) == g and o["direction"] == p["direction"]
               for o in self.open):
            fails.append("correlated")
        if R <= 0 or d * (p["tp1"] - p["entry"]) < S["min_tp1_r"] * R - 1e-12:
            fails.append("rr_tp1")
        if path_blocked(d, p["entry"], p["tp1"], R, p.get("levels") or [], S["path_margin_r"]):
            fails.append("path")
        if self.duplicate(p, cooldown_ms):
            fails.append("duplicate")
        return fails

    def duplicate(self, p, cooldown_ms):
        lg = self.logdf
        if lg is None or lg.empty:
            return False
        same = lg[(lg["strategy"] == p["strategy"]) & (lg["coin"] == p["coin"]) & (lg["tf"] == p["timeframe"])
                  & (lg["stage"] == "APPROVED")]
        if same["state"].isin(LIVE_OPEN).any():
            return True
        done = same.loc[same["state"] == "CLOSED", "closed_time_utc"].dropna().astype(str)   # real trades only
        done = done[done != ""]
        return bool(len(done)) and p["signal_ms"] < _ms(done.max()) + 60_000 + cooldown_ms

    def accept(self, p):
        self.open.append(dict(coin=p["coin"], direction=p["direction"]))
