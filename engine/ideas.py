"""
Idea factories (Phase 17 C, item 9): where new strategy cards come from, and how each factory is doing.

  a) literature        - Claude, from the reading plan (memory/curriculum.md)
  b) failure           - Claude, from loss tags with >= 30 losing trades
  c) missed_move       - Claude, from strong moves no strategy caught
  d) market_structure  - Claude, from the futures data (funding, open interest, long/short, taker)
  e) variant_search    - THE ENGINE: one-change variants of the best BACKTESTING cells (variant_cards below), at most
                         the factory quota per 7 days; every one is tested and counted in memory/trials.csv like any card.
                         Phase 18 B: the simpler version of a card whose entry rule adds nothing (simpler_cards) comes
                         first, from the same quota
  f) lead_lag          - Claude, from the BTC -> alt lead-lag measurement (lead_lag below)

Every lab card names its factory (strategy_spec.factory_problems); the weekly email shows the pass rate per factory.
Pure functions; research.py writes the cards.
"""
import copy

import numpy as np

from engine import strategy_spec as sspec

PASSED = ("VALIDATION", "PAPER_TRADING", "APPROVED")
MIN_TRADES = 30


def lead_lag(df, lags=(1, 2, 3)):
    """Does BTC move first? Correlation of this coin's 1-candle return with BTC's return 1..3 candles EARLIER
    (both known at the time - no look-ahead). n = candles used; 'clear' when |corr| > 2 / sqrt(n)."""
    if "_btc_close" not in df:
        return None
    r = df["close"].astype(float).pct_change()
    b = df["_btc_close"].astype(float).pct_change()
    out = dict(same=None, lags={})
    both = r.notna() & b.notna()
    if both.sum() > 50:
        out["same"] = round(float(np.corrcoef(r[both], b[both])[0, 1]), 3)
    for k in lags:
        bk = b.shift(k)
        m = r.notna() & bk.notna()
        n = int(m.sum())
        if n < 50:
            continue
        c = float(np.corrcoef(r[m], bk[m])[0, 1])
        out["lags"][k] = dict(corr=round(c, 4), n=n, clear=bool(abs(c) > 2 / np.sqrt(n)))
    return out


def factory_stats(cells, cards):
    """Pass rate per factory: lab cards written, strategy/timeframe cells tested, cells that reached VALIDATION or
    better. cards: {'id@version': card}."""
    out = {f: dict(cards=0, cells=0, passed=0) for f in sspec.FACTORIES}
    for c in cards.values():
        if c.get("lab") and c.get("factory") in out:
            out[c["factory"]]["cards"] += 1
    for cell in cells.values():
        card = cards.get(f"{cell['strategy']}@{cell['version']}") or {}
        f = card.get("factory") if card.get("lab") else None
        if f in out:
            out[f]["cells"] += 1
            out[f]["passed"] += cell.get("status") in PASSED
    for v in out.values():
        v["pass_rate"] = round(v["passed"] / v["cells"], 3) if v["cells"] else None
    return out


def _desc_targets():
    return {"long": ["2R", "3R"], "short": ["2R", "3R"], "split": [0.5, 0.5]}


def _variants(raw, cell, trade_order):
    """(kind, what changes, the new card fields) - one change each, in the order tried."""
    r = sspec.render(raw)
    tp1 = min((sspec.tp1_r(r, s) or 0) for s in ("long", "short")) if raw.get("targets") else 0
    if tp1 < sspec.MIN_TP1_R:
        yield "EXIT", "targets 2R / 3R (50 / 50) instead of a first target below 2R", dict(targets=_desc_targets())
        return                                   # every other variant would fail the 2R rule
    seg = ((cell.get("attribution") or {}).get("by_regime")) or {}
    bad = [g for g in raw["regimes"] if (seg.get(g) or {}).get("n", 0) >= MIN_TRADES and seg[g]["avg_r"] <= -0.10]
    if bad and len(bad) < len(raw["regimes"]):
        yield ("REGIME", f"no longer trades in {', '.join(bad)} (lost there: "
               + "; ".join(f"{g} {seg[g]['avg_r']:+.2f}R over {seg[g]['n']}" for g in bad) + ")",
               dict(regimes=[g for g in raw["regimes"] if g not in bad]))
    used = sspec.rule_names(raw)
    params = dict(raw.get("params") or {})
    if "adx" not in used and "v_adx" not in params:
        yield ("ADX", "only when ADX(14) > 20 (trend strength filter)",
               dict(long=list(raw["long"]) + ["adx(14) > {v_adx}"], short=list(raw["short"]) + ["adx(14) > {v_adx}"],
                    params=dict(params, v_adx=20)))
    if "rel_vol" not in used and "v_rv" not in params:
        yield ("RVOL", "only when volume is at least 1.2x normal (rel_vol filter)",
               dict(long=list(raw["long"]) + ["rel_vol > {v_rv}"], short=list(raw["short"]) + ["rel_vol > {v_rv}"],
                    params=dict(params, v_rv=1.2)))
    order = [t for t in trade_order if t != "5m"]
    i = order.index(cell["tf"]) if cell["tf"] in order else -1
    for j in (i - 1, i + 1):
        if 0 <= j < len(order) and order[j] not in raw["timeframes"] and not raw.get("confirm_5m"):
            yield "TF", f"also on {order[j]} (next to {cell['tf']}, its best timeframe)", \
                dict(timeframes=list(raw["timeframes"]) + [order[j]])
            break


def variant_cards(cells, cards, today, n_max, labels, trade_order):
    """Factory e: up to n_max new lab cards - one-change variants of the strongest BACKTESTING cells (30+ trades,
    best average R on unseen data first). Parents with a special ingredient (SMC / 5m) or control twins are skipped
    (a variant would need its own twin). Every card passes the same checks as a Claude card."""
    if n_max <= 0:
        return []
    by_id = {c["id"]: c for c in cards.values()}
    ids = set(by_id)
    ranked = sorted((c for c in cells.values() if c.get("status") == "BACKTESTING"
                     and c["evidence"]["all"]["n"] >= MIN_TRADES and c["evidence"]["validate"]["n"] > 0),
                    key=lambda c: (-c["evidence"]["validate"]["avg_r"], -c["evidence"]["all"]["avg_r"]))
    out, parents = [], set()
    for cell in ranked:
        key = f"{cell['strategy']}@{cell['version']}"
        parent = cards.get(key)
        if parent is None or key in parents or parent.get("twin_of") or sspec.special(parent):
            continue
        raw = {k: copy.deepcopy(v) for k, v in (parent.get("_raw") or parent).items()
               if not k.startswith("_") and k not in ("lab", "control_twin", "twin_of")}
        for kind, what, change in _variants(raw, cell, trade_order):
            vid = f"{parent['id']}-V{kind}"
            if vid in ids:
                continue
            ev = cell["evidence"]
            card = dict(raw, **change)
            edge = copy.deepcopy(raw.get("edge") or {})
            if isinstance(edge.get("works_in"), list):
                edge["works_in"] = [g for g in edge["works_in"] if g in card["regimes"]] or list(card["regimes"])
            card.update(
                id=vid, version="1.0", status="FORMALIZED", added=str(today), factory="variant_search",
                variant_of=key, parent=f"result: {key} {cell['tf']}", edge=edge, evidence_class="BACKTEST_EVIDENCE",
                source=f"engine variant search: one change to {key}",
                factory_evidence=(f"{key} {cell['tf']}: {ev['all']['n']} trades, avg {ev['all']['avg_r']:+.3f}R, "
                                  f"unseen part {ev['validate']['avg_r']:+.3f}R ({ev['validate']['n']} trades); "
                                  f"change: {what}"),
                hypothesis=f"One change to {key}: {what}. It should keep the edge of {key} and remove part of its "
                           "losses; tested because it was the strongest BACKTESTING cell this week.",
                changelog=[f"1.0 ({today}): engine variant of {key} - {what}"])
            others = {k: v for k, v in by_id.items() if k != vid}
            if sspec.lab_card_problems(card, others, labels, trade_order) or \
                    sspec.factory_problems(card, [], engine=True):
                continue
            if len(sspec.change_count(raw, card)) != 1:
                continue
            out.append(card)
            ids.add(vid)
            parents.add(key)
            break
        if len(out) >= n_max:
            break
    return out


def simpler_cards(cells, cards, today, n_max, labels, trade_order):
    """Phase 18 B (rule significance): for a cell where removing ONE entry rule gave at least as good an average per
    trade (with enough trades), queue the simpler card - the same card without that rule - as a lab card (factory
    variant_search, parent = that result). The strongest evidence first; one card per parent; every card passes the
    same checks as a Claude card (a parent whose first target is below 2R cannot be queued - it would need a second
    change). Returns (new cards (at most n_max), {cell key: why its simpler card was not queued})."""
    skipped = {}
    ids = {c["id"] for c in cards.values()}
    rows = [(cell, r) for cell in cells.values() for r in cell.get("rules_adding_nothing") or []
            if cell.get("status") not in ("FAILED", "RETIRED") and not cell.get("bias")]
    rows.sort(key=lambda x: (-(x[1]["avg_r"] - x[0]["evidence"]["all"]["avg_r"]), -x[1]["n"]))
    by_id = {c["id"]: c for c in cards.values()}
    out, parents = [], set()
    for cell, r in rows:
        key = f"{cell['strategy']}@{cell['version']}"
        parent = cards.get(key)
        ck = f"{key}|{cell['tf']}"
        if parent is None or key in parents or parent.get("twin_of") or sspec.special(parent):
            skipped.setdefault(ck, "a control twin / SMC or 5m card needs its own twin - not queued automatically"
                               if parent is not None and key not in parents else "one simpler card per strategy a run")
            continue
        if len(out) >= n_max:
            skipped.setdefault(ck, "the week's variant_search quota is used up - queued again next run")
            continue
        raw = {k: copy.deepcopy(v) for k, v in (parent.get("_raw") or parent).items()
               if not k.startswith("_") and k not in ("lab", "control_twin", "twin_of")}
        drop = next((d for d in sspec.rule_drops(dict(parent, _raw=raw)) if d[0] == r["label"]), None)
        if drop is None:
            continue
        nraw = drop[2]
        vid = f"{parent['id']}-S{r['label'].split()[-1]}"
        if vid in ids:
            skipped.setdefault(ck, f"{vid} is already in the lab")
            continue
        ev = cell["evidence"]["all"]
        card = dict(nraw, id=vid, version="1.0", status="FORMALIZED", added=str(today), factory="variant_search",
                    variant_of=key, parent=f"result: {key} {cell['tf']}", evidence_class="BACKTEST_EVIDENCE",
                    source=f"engine rule-significance test: {key} without one entry rule",
                    factory_evidence=(f"{key} {cell['tf']}: with the rule {ev['n']} trades avg {ev['avg_r']:+.3f}R; "
                                      f"{r['label']} ({r['rule']}): {r['n']} trades avg {r['avg_r']:+.3f}R - the rule "
                                      "does not improve the result"),
                    hypothesis=(f"The rule '{r['rule']}' adds nothing to {key}: the simpler card without it should do "
                                "at least as well on new data (fewer rules = less room for overfitting)."),
                    changelog=[f"1.0 ({today}): {key} without entry rule '{r['rule']}' (rule significance test)"])
        others = {k: v for k, v in by_id.items() if k != vid}
        probs = (sspec.lab_card_problems(card, others, labels, trade_order) + sspec.factory_problems(card, [], engine=True)
                 or (["more than one change"] if len(sspec.change_count(raw, card)) != 1 else []))
        if probs:
            skipped.setdefault(ck, f"the simpler card would break a lab rule: {probs[0]}")
            continue
        out.append(card)
        ids.add(vid)
        parents.add(key)
    return out, skipped
