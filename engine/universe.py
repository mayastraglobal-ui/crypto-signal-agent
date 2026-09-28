"""
Tradable universe (AGENT_PROMPT.md section 4).

  - SIGNAL coins   : the top 7 eligible coins by 24h quote volume. Only these may give signals.
  - RESEARCH coins : the signal coins + the next 3 eligible coins. The extra 3 are backtested only.
  - Hysteresis     : a new coin must rank in the top 7 for 2 runs in a row before it joins, and a
                     member must rank outside the top 7 for 2 runs in a row before it leaves.
                     A member that stops being ELIGIBLE (safety rules) is removed at once.

Everything here is pure (no internet, no files): the same numbers always give the same list.
"""
import numpy as np

DEFAULTS = dict(
    signal_coins=7,
    research_coins=10,
    hysteresis_runs=2,
    candidate_pool=20,
    min_24h_volume_usdt=50_000_000,
    min_7d_avg_volume_usdt=50_000_000,
    max_volume_spike_x=3.0,
    max_abs_24h_move_pct=25.0,
    max_spread_pct=0.10,
    min_depth_usdt_1pct=250_000,
    stablecoin_band_pct=2.0,
    stablecoin_days=30,
    wash_volume_flag_ratio=1000,
)
LEVERAGED_SUFFIXES = ("UP", "DOWN", "BULL", "BEAR")


def settings(cfg_section):
    out = dict(DEFAULTS)
    out.update(cfg_section or {})
    return out


def usd(x):
    return f"${x / 1e6:,.0f}M" if x >= 1e6 else f"${x / 1e3:,.0f}k"


# ---------------------------------------------------------------------
# 1. Fast pre-filter on the ticker list (names, leveraged tokens, volume)
# ---------------------------------------------------------------------
def prefilter(tickers, market, u):
    """Returns (candidates sorted by 24h volume, excluded {base: reason}).
    Only coins over the 24h volume floor are considered; excluded = those removed by the
    exclusion lists or as leveraged / multiplier tokens."""
    q = market["quote"]
    lists = [("exclude_meme", "meme coin"), ("exclude_ai", "AI/compute-narrative token"),
             ("exclude_other", "stablecoin / wrapped / staked token"), ("exclude_gold", "gold token")]
    named = {}
    for key, why in lists:
        for t in market.get(key, []):
            named[str(t).upper()] = f"{why} (exclusion list)"
    cands, excluded = [], {}
    for t in tickers:
        s = t["symbol"]
        if not s.endswith(q):
            continue
        base = s[: -len(q)]
        if t["quote_volume"] < u["min_24h_volume_usdt"]:
            continue    # the long tail of small coins: not worth listing one by one
        if base in named:
            excluded[base] = named[base]
        elif base.endswith(LEVERAGED_SUFFIXES):
            excluded[base] = "leveraged token"
        elif base.startswith("1000"):
            excluded[base] = "multiplier token (1000x units)"
        else:
            cands.append(dict(t, base=base))
    cands.sort(key=lambda r: -r["quote_volume"])
    return cands, excluded


def candidate_pool(cands, always, size):
    """The coins worth checking in detail: always-include coins (and current members) first,
    then the rest by volume."""
    must = [c for c in cands if c["base"] in always]
    rest = [c for c in cands if c["base"] not in always]
    return (must + rest)[:max(size, len(must))]


# ---------------------------------------------------------------------
# 2. Measurements for one coin
# ---------------------------------------------------------------------
def depth_within(levels, mid, pct=1.0):
    """USD value of order-book levels [(price, qty)] within pct% of mid."""
    lo, hi = mid * (1 - pct / 100), mid * (1 + pct / 100)
    return float(sum(p * q for p, q in levels if lo <= p <= hi))


def measure(ticker, daily, book=None, depth=None, u=DEFAULTS):
    """Collect the numbers the eligibility rules need.
    daily : closed daily candles (needs close; quote_volume if available)
    book  : (best_bid, best_ask) or None if unavailable
    depth : (bids, asks) lists of (price, qty) or None if unavailable"""
    m = dict(coin=ticker["base"], vol_24h=float(ticker["quote_volume"]),
             change_24h=float(ticker["change_pct"]), listing_days=int(len(daily)))
    if len(daily):
        qv = daily["quote_volume"] if "quote_volume" in daily else daily["volume"] * daily["close"]
        m["vol_7d_avg"] = float(qv.iloc[-7:].mean())
        c = daily["close"].iloc[-int(u["stablecoin_days"]):].to_numpy(dtype=float)
        m["stable_dev_pct"] = float(np.max(np.abs(c / c.mean() - 1)) * 100) if len(c) else None
    else:
        m["vol_7d_avg"], m["stable_dev_pct"] = 0.0, None
    m["spread_pct"] = None
    if book and book[0] > 0 and book[1] >= book[0]:
        mid = (book[0] + book[1]) / 2
        m["spread_pct"] = (book[1] - book[0]) / mid * 100
    m["depth_bid_usdt"] = m["depth_ask_usdt"] = None
    if depth and depth[0] and depth[1]:
        mid = (depth[0][0][0] + depth[1][0][0]) / 2
        m["depth_bid_usdt"] = depth_within(depth[0], mid)
        m["depth_ask_usdt"] = depth_within(depth[1], mid)
    return m


# ---------------------------------------------------------------------
# 3. Eligibility (all rules must pass)
# ---------------------------------------------------------------------
def eligibility(m, u, min_listing_days, data_state="GOOD", suspended_today=False):
    """Returns a dict:
      ok      -> True when every rule passes
      reasons -> why the coin is NOT eligible, in words (empty = eligible)
      flags   -> worth knowing, but do not exclude (data not available, wash-volume suspicion...)
      codes   -> short fixed names of the failed rules / flags, used to log only real CHANGES"""
    reasons, flags, codes, fcodes = [], [], [], []

    def fail(code, text):
        codes.append(code)
        reasons.append(text)

    def flag(code, text):
        fcodes.append(code)
        flags.append(text)

    if m["listing_days"] < min_listing_days:
        fail("history", f"only {m['listing_days']} days of history (need {min_listing_days})")
    if m["vol_24h"] < u["min_24h_volume_usdt"]:
        fail("volume_24h", f"24h volume {usd(m['vol_24h'])} < {usd(u['min_24h_volume_usdt'])}")
    if m["vol_7d_avg"] < u["min_7d_avg_volume_usdt"]:
        fail("volume_7d", f"7-day average volume {usd(m['vol_7d_avg'])} < {usd(u['min_7d_avg_volume_usdt'])}")
    elif m["vol_24h"] > u["max_volume_spike_x"] * m["vol_7d_avg"]:
        fail("volume_spike", f"one-day volume spike: 24h {usd(m['vol_24h'])} is "
                             f"{m['vol_24h'] / m['vol_7d_avg']:.1f}x the 7-day average")
    if abs(m["change_24h"]) > u["max_abs_24h_move_pct"]:
        fail("big_move", f"24h move {m['change_24h']:+.1f}% is beyond ±{u['max_abs_24h_move_pct']:.0f}% "
                         "- suspended for the rest of the UTC day")
    elif suspended_today:
        fail("big_move", f"suspended for the rest of the UTC day (moved more than "
                         f"±{u['max_abs_24h_move_pct']:.0f}% earlier today)")
    if m["stable_dev_pct"] is not None and m["listing_days"] >= u["stablecoin_days"] \
            and m["stable_dev_pct"] <= u["stablecoin_band_pct"]:
        fail("stablecoin", f"behaves like a stablecoin (price stayed within ±{m['stable_dev_pct']:.2f}% "
                           f"for {u['stablecoin_days']} days)")
    if m["spread_pct"] is None:
        flag("no_spread_data", "spread not available")
    elif m["spread_pct"] > u["max_spread_pct"]:
        fail("spread", f"spread {m['spread_pct']:.3f}% > {u['max_spread_pct']}%")
    if m["depth_bid_usdt"] is None:
        flag("no_depth_data", "order-book depth not available")
    else:
        thin = min(m["depth_bid_usdt"], m["depth_ask_usdt"])
        if thin < u["min_depth_usdt_1pct"]:
            fail("thin_book", f"order book too thin: {usd(thin)} within 1% "
                              f"(need {usd(u['min_depth_usdt_1pct'])})")
        elif m["vol_24h"] / thin > u["wash_volume_flag_ratio"]:
            flag("wash_volume", f"possible wash volume: 24h volume is {m['vol_24h'] / thin:,.0f}x the 1% "
                                "order-book depth (flag only, not excluded)")
    if data_state == "UNSAFE":
        fail("data_unsafe", "price data UNSAFE")
    elif data_state == "DEGRADED":
        flag("data_degraded", "price data DEGRADED - stays in the list, but no signals")
    return dict(ok=not reasons, reasons=reasons, flags=flags, codes=codes, flag_codes=fcodes)


def update_suspensions(state, moves, u, today):
    """Coins that moved more than ±25% are suspended until the end of the UTC day.
    moves: {coin: 24h change %}. Returns (new_state, set of coins suspended today)."""
    sus = {c: d for c, d in state.get("suspended", {}).items() if d == today}
    for c, chg in moves.items():
        if abs(chg) > u["max_abs_24h_move_pct"]:
            sus[c] = today
    return dict(state, suspended=sus), set(sus)


# ---------------------------------------------------------------------
# 4. Membership with hysteresis
# ---------------------------------------------------------------------
def empty_state():
    return dict(members=[], in_streak={}, out_streak={}, suspended={}, runs=0,
                last_eligibility={}, last_flags={})


def rank(eligible_coins_by_volume, always):
    """Eligible coins ordered for ranking: always-include coins first, then by volume."""
    return ([c for c in eligible_coins_by_volume if c in always] +
            [c for c in eligible_coins_by_volume if c not in always])


def update_membership(state, ranked, u, always, not_eligible=None):
    """One run of the membership rules.

    state        : previous state (empty_state() on the first run)
    ranked       : ELIGIBLE coins, best first (use rank())
    not_eligible : {coin: [reasons]} for coins that failed eligibility (used in the log text)
    Returns (new_state, events, view). events are dicts {coin, action, why} for the universe log.
    """
    size, need = int(u["signal_coins"]), int(u["hysteresis_runs"])
    extra = int(u["research_coins"]) - size
    not_eligible = not_eligible or {}
    top = ranked[:size]
    pos = {c: i + 1 for i, c in enumerate(ranked)}
    st = dict(state, members=list(state["members"]), in_streak=dict(state["in_streak"]),
              out_streak=dict(state["out_streak"]))
    events = []

    if st["runs"] == 0 or not st["members"]:
        st["members"] = list(top)
        st["in_streak"], st["out_streak"] = {}, {}
        for c in top:
            events.append(dict(coin=c, action="JOIN", why=f"starting list (no members yet): rank #{pos[c]}"))
    else:
        eligible = set(ranked)
        # (1) safety first: a member that is no longer eligible leaves immediately
        for c in list(st["members"]):
            if c not in eligible:
                st["members"].remove(c)
                st["out_streak"].pop(c, None)
                why = "; ".join(not_eligible.get(c, ["no longer in the candidate list"]))
                events.append(dict(coin=c, action="LEAVE", why=f"not eligible: {why}"))
        # (2) members ranked outside the top: count runs, leave after `need` runs in a row
        for c in list(st["members"]):
            if c in top:
                st["out_streak"].pop(c, None)
                continue
            st["out_streak"][c] = st["out_streak"].get(c, 0) + 1
            if st["out_streak"][c] >= need and c not in always:
                st["members"].remove(c)
                st["out_streak"].pop(c)
                events.append(dict(coin=c, action="LEAVE",
                                   why=f"outside the top {size} for {need} runs in a row (now #{pos[c]})"))
        # (3) non-members ranked inside the top: count runs in a row
        for c in list(st["in_streak"]):
            if c not in top or c in st["members"]:
                st["in_streak"].pop(c)
        for c in top:
            if c not in st["members"]:
                st["in_streak"][c] = st["in_streak"].get(c, 0) + 1
        # (4) BTC / ETH: always included when eligible, no waiting
        for c in top:
            if c in always and c not in st["members"]:
                st["members"].append(c)
                st["in_streak"].pop(c, None)
                events.append(dict(coin=c, action="JOIN", why="always included when eligible"))
        while len(st["members"]) > size:          # made room for BTC/ETH: drop the worst-ranked other
            worst = max((c for c in st["members"] if c not in always), key=lambda c: pos.get(c, 1e9))
            st["members"].remove(worst)
            st["out_streak"].pop(worst, None)
            events.append(dict(coin=worst, action="LEAVE", why="made room for an always-included coin"))
        # (5) fill free slots with coins that held a top rank for `need` runs, best rank first
        for c in top:
            if len(st["members"]) >= size:
                break
            if c not in st["members"] and st["in_streak"].get(c, 0) >= need:
                st["members"].append(c)
                st["in_streak"].pop(c)
                events.append(dict(coin=c, action="JOIN",
                                   why=f"in the top {size} for {need} runs in a row (now #{pos[c]})"))

    st["members"].sort(key=lambda c: pos.get(c, 1e9))
    st["runs"] = st["runs"] + 1
    research_extra = [c for c in ranked if c not in st["members"]][:extra]
    waiting = {c: n for c, n in st["in_streak"].items() if c not in st["members"]}
    view = dict(signal=list(st["members"]), research_only=research_extra,
                research=list(st["members"]) + research_extra, waiting=waiting,
                leaving=dict(st["out_streak"]), empty_slots=size - len(st["members"]))
    return st, events, view


def remove_members(state, coins_why):
    """Remove members immediately (e.g. data turned UNSAFE after the full download).
    coins_why: {coin: reason}. Returns (new_state, events)."""
    st = dict(state, members=list(state["members"]), out_streak=dict(state["out_streak"]))
    events = []
    for c, why in coins_why.items():
        if c in st["members"]:
            st["members"].remove(c)
            st["out_streak"].pop(c, None)
            events.append(dict(coin=c, action="LEAVE", why=why))
    return st, events


NOT_LOGGED_FLAGS = {"no_spread_data", "no_depth_data"}


def eligibility_changes(state, results):
    """Log-worthy CHANGES in eligibility and flags since the last run (not the same news every hour).
    results: {coin: eligibility dict}. Returns (new_state, events)."""
    st = dict(state, last_eligibility=dict(state.get("last_eligibility", {})),
              last_flags=dict(state.get("last_flags", {})))
    events = []
    for c, r in results.items():
        before = st["last_eligibility"].get(c)
        now = sorted(set(r["codes"]))
        if before != now:
            if r["ok"] and before:
                events.append(dict(coin=c, action="ELIGIBLE", why="passes every rule again"))
            elif not r["ok"]:
                events.append(dict(coin=c, action="EXCLUDED", why="; ".join(r["reasons"])))
        st["last_eligibility"][c] = now
        f_now = [(code, text) for code, text in zip(r["flag_codes"], r["flags"])
                 if code not in NOT_LOGGED_FLAGS]
        for code, text in f_now:
            if code not in st["last_flags"].get(c, []):
                events.append(dict(coin=c, action="FLAG", why=text))
        st["last_flags"][c] = sorted(code for code, _ in f_now)
    return st, events
