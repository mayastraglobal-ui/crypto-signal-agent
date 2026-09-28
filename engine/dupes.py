"""
Near-duplicate strategies (Phase 20 lite, item 4). Two strategy cells on the SAME timeframe that take (almost) the
same trades are one idea, not two: when at least 70% of the trades are shared - same coin, same entry candle, same
direction, measured against the cell with MORE trades, so a small cell inside a big one is not a duplicate - the
newer cell is marked "near-duplicate of <older cell>" and reports count the pair as one idea.

Report only: no status, gate or rule changes. Pure functions (no files, no internet).
"""

DEFAULTS = dict(min_overlap=0.70, min_trades=20)


def settings(cfg):
    return dict(DEFAULTS, **(cfg or {}))


def trade_keys(by_coin):
    """{coin: [trades]} -> {(coin, entry candle time, direction)}."""
    return {(coin, int(t["entry_time"]), int(t.get("dir", 0))) for coin, trs in (by_coin or {}).items() for t in trs}


def overlap(a, b):
    """Shared trades / trades of the bigger cell (0 when either is empty)."""
    return len(a & b) / max(len(a), len(b)) if a and b else 0.0


def find(per, order, D=DEFAULTS, skip=()):
    """per: {(id, version, tf): {coin: [trades]}}; order: {"id@version": sort key} - older ideas first (the one
    kept); skip: card keys never compared (control twins: benchmarks, not ideas).
    Returns {"id@version|tf": dict(of="id@version|tf", overlap=0.xx, shared=n, trades=n)} for each duplicate."""
    out = {}
    by_tf = {}
    for k3, by_coin in per.items():
        card = f"{k3[0]}@{k3[1]}"
        if card in skip:
            continue
        keys = trade_keys(by_coin)
        if len(keys) >= int(D["min_trades"]):
            by_tf.setdefault(k3[2], []).append((order.get(card, (1, card)), card, keys))
    for tf, rows in by_tf.items():
        rows.sort(key=lambda r: (r[0], r[1]))
        kept = []                                   # the cells that stay "the idea" on this timeframe
        for _, card, keys in rows:
            best = max(((overlap(keys, k2), c2, k2) for c2, k2 in kept), default=None, key=lambda x: x[0])
            if best and best[0] >= float(D["min_overlap"]):
                out[f"{card}|{tf}"] = dict(of=f"{best[1]}|{tf}", overlap=round(best[0], 3),
                                           shared=len(keys & best[2]), trades=len(keys))
            else:
                kept.append((card, keys))
    return out


def age_order(versions, cards):
    """Sort keys: cards first tested earlier come first (the registry's first_tested_utc, versions = {"id@version":
    row}); untested cards after, by name. cards: iterable of "id@version"."""
    first = {c: str((row or {}).get("first_tested_utc") or "") for c, row in (versions or {}).items()}
    return {c: (0, first[c], c) if first.get(c) else (1, "", c) for c in cards}


def ideas(tested_cards, dupes):
    """Cards tested, counting near-duplicates as one idea: a card is left out only when ALL its tested cells are
    near-duplicates of other cards. tested_cards: {"id@version": [tf, ...]}."""
    return sum(1 for card, tfs in tested_cards.items() if not tfs or not all(f"{card}|{tf}" in dupes for tf in tfs))


def report_lines(research):
    """Report section 3b lines."""
    d = (research or {}).get("near_duplicates") or {}
    if not d:
        return []
    pct = round(100 * float((research.get("near_duplicate_settings") or DEFAULTS)["min_overlap"]))
    L = [f"**Near-duplicates** (same timeframe, >= {pct}% of trades shared - counted as one idea, nothing else "
         "changes):\n"]
    for ck, x in sorted(d.items()):
        L.append(f"- {label(ck)} = near-duplicate of {label(x['of'])} ({round(100 * x['overlap'])}% of "
                 f"{x['trades']:,} trades shared)\n")
    return L


def label(ck):
    """'donchian_breakout-VEXIT@1.0|4h' -> 'donchian_breakout-VEXIT v1.0 4h'."""
    card, _, tf = ck.partition("|")
    sid, _, ver = card.rpartition("@")
    return f"{sid} v{ver} {tf}"
