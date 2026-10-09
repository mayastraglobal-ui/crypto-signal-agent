"""
The Forward Test Program (operator plan 2026-10-09): 10 different strategies x 4 versions (strategies_program.yaml).

The research run cannot backtest all 59 program cells every night on 10 coins and 5 years of history within its
time limit, so it tests them in batches:
  * every program strategy with a cell in VALIDATION / PAPER_TRADING / APPROVED is tested EVERY night (its paper
    record and pass bar stay checked daily);
  * plus `strategies_per_night` strategies (all 4 versions, every timeframe) - those tested longest ago first, never
    tested = first. The first full pass takes about 5 nights; then it keeps rotating.
A cell not tested tonight keeps its status (memory/strategy_registry.csv) and its last results are carried into
tonight's reports, marked with the run they came from.

reports/program.json / program.md: every program cell's result per coin, AFTER fees (the real result) and BEFORE
fees (what the rules alone made - the difference is what fees and funding cost), with the coins where it was
positive. The weekly Claude review and the TEST alerts (next steps of the plan) read this file.

Pure functions only: no internet, no files.
"""
import numpy as np

DEFAULTS = dict(strategies_per_night=2, skip_after_min=95)
ACTIVE = ("VALIDATION", "PAPER_TRADING", "APPROVED")


def settings(raw):
    s = dict(DEFAULTS)
    s.update(raw or {})
    s["strategies_per_night"] = max(0, int(s["strategies_per_night"]))
    s["skip_after_min"] = float(s["skip_after_min"])
    return s


def number(card):
    return int((card.get("program") or {}).get("strategy") or 0)


def is_program(card):
    """A card loaded from strategies_program.yaml (an engine variant of one, in the lab file, is a lab card)."""
    return bool(card.get("_program"))


def cell_keys(card):
    return [f"{card['id']}@{card['version']}|{tf}" for tf in card["timeframes"]]


def batch(cards, reg_cells, n, mode="auto"):
    """Which program strategies the research run tests tonight. cards: the runnable program cards; reg_cells: the
    registry's cells {'id@ver|tf': {status, last_checked_utc, ...}}; mode: 'auto', 'all', 'none' or '1,4,7'.
    Returns (sorted strategy numbers, {number: why})."""
    nums = sorted({number(c) for c in cards})
    if mode == "all":
        return nums, {k: "all strategies asked for (--program all)" for k in nums}
    if mode == "none":
        return [], {}
    if mode not in (None, "", "auto"):
        want = {int(x) for x in str(mode).split(",") if x.strip()}
        return sorted(want & set(nums)), {k: "asked for (--program)" for k in sorted(want & set(nums))}
    why, oldest = {}, {}
    for c in cards:
        k = number(c)
        for ck in cell_keys(c):
            cell = reg_cells.get(ck) or {}
            if cell.get("status") in ACTIVE:
                why[k] = f"{ck.replace('|', ' ')} is {cell['status']} - checked every night"
            last = str(cell.get("last_checked_utc") or "")
            oldest[k] = min(oldest.get(k, last), last)        # '' (never tested) sorts first
    rest = sorted((k for k in nums if k not in why), key=lambda k: (oldest.get(k, ""), k))
    for k in rest[:n]:
        why[k] = "never tested yet" if not oldest.get(k) else f"tested longest ago ({oldest[k]} UTC)"
    return sorted(why), why


def select(strategies, chosen):
    """(cards to run tonight, program cards skipped tonight)."""
    run = [s for s in strategies if not is_program(s) or number(s) in chosen]
    return run, [s for s in strategies if is_program(s) and number(s) not in chosen]


def carry(prev_cells, skipped, reg_cells, prev_run):
    """Tonight's report rows for the program cells NOT tested tonight: their last research results, marked with the
    run they came from, with the registry's current status. prev_cells: the previous research.json cells."""
    out = {}
    for card in skipped:
        for ck in cell_keys(card):
            c = (prev_cells or {}).get(ck)
            if not c:
                continue
            c = dict(c, carried_from=c.get("carried_from") or prev_run)
            st = (reg_cells.get(ck) or {}).get("status")
            if st:
                c["status"] = st
            out[ck] = c
    return out


def coin_rows(per_coin, min_trades):
    """{coin: {n, win_rate, avg_r, gross_avg_r, total_r, positive, test_n, test_avg_r}} from {coin: trades}. gross =
    before fees and funding (r + fees_r); test = the coin's unseen last 30% (trades marked oos)."""
    out = {}
    for coin, tr in sorted(per_coin.items()):
        r = np.array([t["r"] for t in tr], dtype=float)
        g = np.array([t["r"] + t.get("fees_r", 0.0) for t in tr], dtype=float)
        n = len(r)
        o = np.array([t["r"] for t in tr if t.get("oos")], dtype=float)     # the unseen last 30% of this coin
        out[coin] = dict(n=n, win_rate=round(float((r > 0).mean()) * 100, 1) if n else 0.0,
                         avg_r=round(float(r.mean()), 3) if n else 0.0,
                         gross_avg_r=round(float(g.mean()), 3) if n else 0.0,
                         total_r=round(float(r.sum()), 1), positive=bool(n >= min_trades and r.mean() > 0),
                         test_n=len(o), test_avg_r=round(float(o.mean()), 3) if len(o) else None)
    return out


def cell_row(card, tf, cell, per_coin, min_trades, now_txt):
    allt = [t for tr in per_coin.values() for t in tr]
    r = np.array([t["r"] for t in allt], dtype=float)
    g = np.array([t["r"] + t.get("fees_r", 0.0) for t in allt], dtype=float)
    ev = cell["evidence"]
    coins = coin_rows(per_coin, min_trades)
    p = card["program"]
    return dict(strategy=p["strategy"], name=p["name"], version=p["version"], id=card["id"], tf=tf,
                status=cell["status"], tested_utc=now_txt,
                trades=len(r), win_rate=ev["all"]["win_rate"], avg_r=ev["all"]["avg_r"],
                gross_avg_r=round(float(g.mean()), 3) if len(g) else 0.0, pf=ev["all"]["pf"],
                test_avg_r=ev["validate"]["avg_r"], test_trades=ev["validate"]["n"],
                long_avg_r=ev["long"]["avg_r"], short_avg_r=ev["short"]["avg_r"],
                fees_avg_r=round(float((g - r).mean()), 3) if len(g) else 0.0,
                coins=coins, positive_coins=[c for c, x in coins.items() if x["positive"]],
                why_not=(cell.get("reasons") or []) + (cell.get("paper_gate_failed") or []))


def table(prev, cards, cells, per, min_trades, now_txt, chosen, why, next_batch):
    """reports/program.json: prev (the last file or None) updated with tonight's tested cells.
    cards: every runnable program card; cells: tonight's research cells; per: {(id, ver, tf): {coin: trades}}."""
    rows = {}
    keep = {ck for c in cards for ck in cell_keys(c)}
    for ck, row in ((prev or {}).get("cells") or {}).items():
        if ck in keep:
            rows[ck] = row
    by_key = {f"{c['id']}@{c['version']}": c for c in cards}
    for ck, cell in cells.items():
        card = by_key.get(ck.split("|")[0])
        if card is None:
            continue
        rows[ck] = cell_row(card, cell["tf"], cell, per.get((cell["strategy"], cell["version"], cell["tf"]), {}),
                            min_trades, now_txt)
    names = {}
    for c in cards:
        names[number(c)] = c["program"]["name"]
    return dict(updated_utc=now_txt, tested_tonight=chosen, why={str(k): v for k, v in why.items()},
                next_night=next_batch, strategies={str(k): v for k, v in sorted(names.items())},
                cells=dict(sorted(rows.items(), key=lambda kv: (kv[1]["strategy"], kv[1]["version"],
                                                                  ["4h", "1h", "30m", "15m", "5m"].index(kv[1]["tf"])
                                                                  if kv[1]["tf"] in ("4h", "1h", "30m", "15m", "5m")
                                                                  else 9))),
                min_coin_trades=min_trades)


def _r(x):
    return "-" if x is None else f"{x:+.2f}R"


def render(t):
    """reports/program.md: one table per strategy, plus the coins where each version was positive."""
    L = ["# Forward Test Program - backtest results", "",
         f"Updated {t['updated_utc']} UTC. Tested tonight: strategies "
         f"{', '.join(str(x) for x in t['tested_tonight']) or 'none'}; next night: "
         f"{', '.join(str(x) for x in t['next_night']) or '-'}.", "",
         "10 strategies x 4 versions (strategies_program.yaml). Every number includes OKX fees and funding "
         "('after fees'); 'before fees' shows what the rules alone made. 'Test' = the unseen last 30% of each coin's "
         f"history. A coin counts as positive with >= {t['min_coin_trades']} trades and an average above 0R after fees.",
         "", "Versions: V1 base (4H) · V2 faster (1H / 30m / 15m) · V3 + daily agrees · V4 trailing ATR exit.", ""]
    by_s = {}
    for ck, row in t["cells"].items():
        by_s.setdefault(row["strategy"], []).append(row)
    for k in sorted(by_s):
        rows = by_s[k]
        L += [f"## {k}. {t['strategies'].get(str(k), rows[0]['name'])}", "",
              "| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |",
              "|---|---|---|---:|---:|---:|---:|---:|---|---|"]
        for r in rows:
            L.append(f"| {r['version']} | {r['tf']} | {r['status']} | {r['trades']} | {r['win_rate']:.0f} | "
                     f"{_r(r['avg_r'])} | {_r(r['gross_avg_r'])} | {_r(r['test_avg_r'])} | "
                     f"{', '.join(r['positive_coins']) or '-'} | {r['tested_utc']} |")
        L.append("")
    if not by_s:
        L.append("No program strategy has been tested yet - the first batch runs in the next research run.")
    return "\n".join(L) + "\n"
