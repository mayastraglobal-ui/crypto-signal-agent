"""
Failure Lab (operator request 2026-10-10: "build the failure lab"): the engine turns WHY trades lose into new
strategy versions by itself, and learns which repairs work.

Every research run measures, per strategy x timeframe, the loss tags of section 17 (engine/attribution.py): e.g.
the 4H Donchian breakout loses -0.09R a trade when the breakout fails within 5 candles (false_breakout) and makes
+0.49R without them. Before this, only Claude's daily review could turn such a tag into a card (factory "failure"),
and it wrote none. Now the engine does it:

  1. candidates - BACKTESTING cells and NEAR-MISS FAILED cells (positive before fees) with enough trades, whose
     tag hurts (the trades with it average less than those without it) in at least min_losers losing trades;
  2. repair      - one fixed, one-change repair per tag (REPAIRS below, the existing building blocks only);
  3. learning    - every repair card is compared with its parent on the same timeframe once tested (results());
     the scoreboard (repair kind -> tried / helped / passed) orders the repairs of a tag (the best first) and
     stops a kind that was tried retire_after times without helping once;
  4. limits      - the "failure" factory quota per 7 days (config.yaml lab.factory_quota, shared with Claude),
     at most per_run cards a night, one per parent; every card is a normal lab card: same checks, one change,
     counted in the trials file (luck bar), never edits a running card, never approval-eligible on its own.
Pure functions; research.py writes the cards and reports/failure_lab.json.
"""
import copy

from engine import attribution as att
from engine import ideas
from engine import strategy_spec as sspec

DEFAULTS = dict(enabled=True, per_run=1, min_trades=100, min_losers=30, min_share=0.25, near_miss_gross_r=0.0,
                retire_after=4, max_depth=2)
PASSED = ("VALIDATION", "PAPER_TRADING", "APPROVED")
LOSS_TAGS = att.CONDITIONS + att.PATH_TAGS + att.LOSER_TAGS

# tag -> repair kinds, in the order tried before the scoreboard knows better
REPAIRS = {
    "false_breakout": ["DISP", "RVOL", "RETEST"],
    "no_displacement": ["DISP"],
    "low_relative_volume": ["RVOL"],
    "range_market": ["ADX", "REGIME"],
    "htf_conflict": ["HTF", "DAILY"],
    "trend_reversal": ["REGIME", "HTF"],
    "regime_mismatch": ["REGIME", "HTF"],
    "overextended_entry": ["NOTEXT", "RETEST"],
    "late_entry": ["NOTLATE", "RETEST"],
    "stop_too_tight": ["WIDESTOP"],
    "stop_too_wide": ["TIGHTSTOP"],
    "fees_slippage": ["LIMIT", "FEECAP"],
    "wrong_session": ["SESSION"],
    "bad_target": ["NEARTP"],
}
INTRADAY = ("1h", "30m", "15m", "5m")
HINDSIGHT = 0.5      # weight of the expected gain of a tag measured after the entry (vs a tag known at entry)


def settings(cfg_block):
    return dict(DEFAULTS, **(cfg_block or {}))


def _both(raw, long_rule, short_rule, params):
    return dict(long=list(raw["long"]) + [long_rule], short=list(raw["short"]) + [short_rule],
                params=dict(raw.get("params") or {}, **params))


def _stop_x(raw, x):
    st = dict(raw["stop"])
    if st.get("method") == "atr" and isinstance(st.get("atr"), (int, float)):
        st["atr"] = round(float(st["atr"]) * x, 2)
        return st, f"{raw['stop']['atr']:g} -> {st['atr']:g} ATR"
    if st.get("method") == "structure" and x > 1 and isinstance(st.get("buffer_atr", 0), (int, float)):
        st["buffer_atr"] = round(float(st.get("buffer_atr", 0)) + 0.25, 2)
        return st, f"buffer {raw['stop'].get('buffer_atr', 0):g} -> {st['buffer_atr']:g} ATR beyond the level"
    return None, None


def repair(kind, raw, cell):
    """(what changes, the new card fields) of one repair kind, or None when it does not apply to this card."""
    used = sspec.rule_names(raw)
    params = raw.get("params") or {}
    special = raw.get("confirm_5m")
    if kind == "DISP" and not used & {"displacement_up", "displacement_down"}:
        return ("a strong candle (displacement) in the trade direction within the last 3 candles",
                _both(raw, "within(displacement_up, 3)", "within(displacement_down, 3)", {}))
    if kind == "RVOL" and not used & {"rel_vol", "volume", "vol_sma"} and "f_rv" not in params:
        return ("volume at least 1.5x normal on the signal candle",
                _both(raw, "rel_vol > {f_rv}", "rel_vol > {f_rv}", dict(f_rv=1.5)))
    if kind == "ADX" and "adx" not in used and "f_adx" not in params:
        return ("only when ADX(14) > 20 (a trending market, not a range)",
                _both(raw, "adx(14) > {f_adx}", "adx(14) > {f_adx}", dict(f_adx=20)))
    if kind == "HTF" and not used & {"htf_up", "htf_down"}:
        return "only when the higher timeframe trends the same way (htf_up / htf_down)", \
            _both(raw, "htf_up", "htf_down", {})
    if kind == "DAILY" and "dir_1d" not in used and cell["tf"] not in ("1d", "1w"):
        return "never against the daily regime (dir_1d)", _both(raw, "dir_1d >= 0", "dir_1d <= 0", {})
    if kind == "REGIME":
        seg = (cell.get("attribution") or {}).get("by_regime") or {}
        bad = [g for g in raw["regimes"] if (seg.get(g) or {}).get("n", 0) >= 30 and seg[g]["avg_r"] <= -0.10]
        if bad and len(bad) < len(raw["regimes"]):
            return (f"no longer trades in {', '.join(bad)} (lost there: "
                    + "; ".join(f"{g} {seg[g]['avg_r']:+.2f}R over {seg[g]['n']}" for g in bad) + ")",
                    dict(regimes=[g for g in raw["regimes"] if g not in bad]))
        return None
    if kind == "NOTEXT" and "f_ext" not in params:
        return ("no entry more than 2 ATR beyond the 20 EMA (not overextended)",
                _both(raw, "close - ema(close,20) < {f_ext} * atr(14)", "ema(close,20) - close < {f_ext} * atr(14)",
                      dict(f_ext=2.0)))
    if kind == "NOTLATE" and "f_late" not in params:
        return ("no entry after a move of 3 ATR or more over the last 10 candles (not late)",
                _both(raw, "close - shift(close,10) < {f_late} * atr(14)",
                      "shift(close,10) - close < {f_late} * atr(14)", dict(f_late=3.0)))
    if kind == "RETEST" and not raw.get("entry") and not special:
        return ("wait for a retest: limit order 0.5 ATR back from the signal close, valid 5 candles",
                dict(entry=dict(type="limit", offset_atr=0.5, valid_bars=5)))
    if kind in ("WIDESTOP", "TIGHTSTOP"):
        st, txt = _stop_x(raw, 1.25 if kind == "WIDESTOP" else 0.8)
        return (f"stop {'wider' if kind == 'WIDESTOP' else 'tighter'}: {txt}", dict(stop=st)) if st else None
    if kind == "LIMIT" and not raw.get("entry") and not special and cell["tf"] in INTRADAY:
        return ("limit entry 0.25 ATR behind the signal close, valid 3 candles (maker fee, no slippage)",
                dict(entry=dict(type="limit", offset_atr=0.25, valid_bars=3)))
    if kind == "FEECAP" and not (raw.get("stop") or {}).get("max_cost_r"):
        return ("no trade when fees + slippage would cost more than 0.25R",
                dict(stop=dict(raw["stop"], max_cost_r=0.25)))
    if kind == "SESSION" and cell["tf"] in INTRADAY and not used & {"sess_asia", "sess_london", "sess_ny"}:
        return "only in the London and New York sessions", \
            _both(raw, "sess_london + sess_ny >= 1", "sess_london + sess_ny >= 1", {})
    if kind == "NEARTP" and raw.get("targets"):
        r = sspec.render(raw)
        tp1 = min((sspec.tp1_r(r, s) or 0) for s in ("long", "short"))
        if tp1 > sspec.MIN_TP1_R + 0.01:
            return f"targets 2R / 3R instead of a first target at {tp1:g}R (trades came close but missed it)", \
                dict(targets=ideas._desc_targets())
    return None


def scoreboard(rows):
    """{kind: dict(tried, helped, passed)} and {tag: ...} from the results rows."""
    by_kind, by_tag = {}, {}
    for r in rows:
        for key, d in ((r["kind"], by_kind), (r["tag"], by_tag)):
            s = d.setdefault(key, dict(tried=0, helped=0, passed=0))
            s["tried"] += 1
            s["helped"] += bool(r["helped"])
            s["passed"] += bool(r["passed"])
    return by_kind, by_tag


def prior(board, kind, S):
    """How likely a repair kind helps, from its record ((helped + 1) / (tried + 2)); None = retired (tried
    retire_after times or more without helping once)."""
    s = board.get(kind) or dict(tried=0, helped=0)
    if s["tried"] >= int(S["retire_after"]) and s["helped"] == 0:
        return None
    return (s["helped"] + 1) / (s["tried"] + 2)


def _depth(card_id):
    return card_id.count("-F")


def candidates(cells, cards, S):
    """[(cell, tag row, tag)] - the cells a repair is tried on, with the tags that hurt them."""
    out = []
    for ck, cell in cells.items():
        a, ev = cell.get("attribution") or {}, (cell.get("evidence") or {}).get("all") or {}
        if not a or ev.get("n", 0) < int(S["min_trades"]) or cell.get("bias"):
            continue
        st = cell.get("status")
        if st == "FAILED":
            if (a.get("gross_avg_r") is None) or a["gross_avg_r"] <= float(S["near_miss_gross_r"]):
                continue                                          # no edge even before fees: not a near miss
        elif st != "BACKTESTING":
            continue
        card = cards.get(f"{cell['strategy']}@{cell['version']}")
        if card is None or card.get("twin_of") or sspec.special(card) or _depth(card["id"]) >= int(S["max_depth"]):
            continue
        for tag, row in (a.get("tags") or {}).items():
            if tag not in REPAIRS or row.get("losers", 0) < int(S["min_losers"]):
                continue
            if not (row.get("flag") or row.get("loss_share", 0) >= float(S["min_share"])):
                continue
            w, wo = row.get("avg_r_with"), row.get("avg_r_without")
            if w is None or wo is None or wo <= w or (st == "FAILED" and wo <= 0):
                continue
            out.append((cell, row, tag))
    return out


def cards_for(cells, cards, today, n_max, labels, trade_order, board, S, existing=()):
    """Up to n_max new repair cards (factory failure), the best expected gain x repair record first, one per
    parent. Returns (cards, considered) - considered = how many (cell, tag) pairs qualified."""
    if n_max <= 0:
        return [], 0
    by_id = {c["id"]: c for c in cards.values()}
    ids, fps = ideas.known(cards, existing)
    pool = candidates(cells, cards, S)
    ranked = []
    for cell, row, tag in pool:
        gain = row["avg_r_without"] - cell["evidence"]["all"]["avg_r"]
        if tag not in att.CONDITIONS:            # known only after the trade (path / loser tags): hindsight, so the
            gain *= HINDSIGHT                    # 'without' average overstates what any entry filter can reach
        for kind in REPAIRS[tag]:
            p = prior(board, kind, S)
            if p is not None:
                ranked.append((gain * p, cell, row, tag, kind))
    ranked.sort(key=lambda x: -x[0])
    out, parents = [], set()
    for score, cell, row, tag, kind in ranked:
        key = f"{cell['strategy']}@{cell['version']}"
        if key in parents:
            continue
        parent = cards[key]
        raw = {k: copy.deepcopy(v) for k, v in (parent.get("_raw") or parent).items()
               if not k.startswith("_") and k not in ("lab", "control_twin", "twin_of", "program", "repair")}
        got = repair(kind, raw, cell)
        if got is None:
            continue
        what, change = got
        vid = f"{parent['id']}-F{kind}"
        if vid in ids:
            continue
        ev = cell["evidence"]
        card = dict(raw, **change)
        edge = copy.deepcopy(raw.get("edge") or {})
        if isinstance(edge.get("works_in"), list):
            edge["works_in"] = [g for g in edge["works_in"] if g in card["regimes"]] or list(card["regimes"])
        ck = f"{key}|{cell['tf']}"
        card.update(
            id=vid, version="1.0", status="FORMALIZED", added=str(today), factory="failure", variant_of=key,
            parent=f"result: {key} {cell['tf']}", edge=edge, evidence_class="BACKTEST_EVIDENCE",
            source=f"engine failure lab: a repair of {key} for its loss tag {tag}",
            factory_evidence=(f"{tag} in {row['loss_share']:.0%} of losses, n={row['losers']} losing trades "
                              f"({key} {cell['tf']}: {ev['all']['n']} trades, avg {ev['all']['avg_r']:+.3f}R, "
                              f"{cell['status']}; trades with {tag} {row['avg_r_with']:+.3f}R, without "
                              f"{row['avg_r_without']:+.3f}R); repair {kind}: {what}"),
            hypothesis=(f"{key} loses on {tag} ({row['avg_r_with']:+.2f}R a trade with it, {row['avg_r_without']:+.2f}R "
                        f"without). One change - {what} - should remove part of those losses and keep the rest."),
            repair=dict(tag=tag, kind=kind, tf=cell["tf"], parent_cell=ck),
            changelog=[f"1.0 ({today}): engine failure lab - {key} repaired for {tag}: {what}"])
        others = {k: v for k, v in by_id.items() if k != vid}
        if sspec.lab_card_problems(card, others, labels, trade_order) or \
                sspec.factory_problems(card, LOSS_TAGS, engine=True):
            continue
        if len(sspec.change_count(raw, card)) != 1:
            continue
        fp = ideas._fp(card)
        if fp is None or fp in fps:
            continue
        out.append(card)
        ids.add(vid)
        fps.add(fp)
        parents.add(key)
        if len(out) >= n_max:
            break
    return out, len(pool)


def results(cells, cards, prev_rows, now_txt):
    """Each tested repair card vs its parent on the same timeframe. helped = better on the unseen part AND overall;
    passed = the repair reached VALIDATION or better. Rows of earlier runs are kept (a retired card's lesson stays).
    Returns (rows, pending ids)."""
    rows = {r["child"]: r for r in prev_rows or [] if isinstance(r, dict) and r.get("child")}
    pending = []
    for card in cards.values():
        rp = card.get("repair")
        if card.get("factory") != "failure" or not isinstance(rp, dict):
            continue
        child = f"{card['id']}@{card['version']}|{rp.get('tf')}"
        c, p = cells.get(child), cells.get(rp.get("parent_cell"))
        if not c or not p or not (c.get("evidence") or {}).get("all", {}).get("n"):
            if child not in rows:
                pending.append(card["id"])
            continue
        ce, pe = c["evidence"], p["evidence"]
        helped = (ce["validate"]["avg_r"] > pe["validate"]["avg_r"]) and (ce["all"]["avg_r"] > pe["all"]["avg_r"])
        rows[child] = dict(child=child, parent=rp["parent_cell"], tag=rp.get("tag"), kind=rp.get("kind"),
                           status=c.get("status"), trades=ce["all"]["n"], avg_r=ce["all"]["avg_r"],
                           test_r=ce["validate"]["avg_r"], parent_avg_r=pe["all"]["avg_r"],
                           parent_test_r=pe["validate"]["avg_r"], helped=bool(helped),
                           passed=c.get("status") in PASSED, checked=now_txt)
    return sorted(rows.values(), key=lambda r: r["child"]), pending


def summary(rows, new_cards, pending, considered, allowed, S):
    by_kind, by_tag = scoreboard(rows)
    return dict(enabled=bool(S["enabled"]), allowed=allowed, considered=considered,
                new=[dict(id=c["id"], tag=c["repair"]["tag"], kind=c["repair"]["kind"], parent=c["repair"]["parent_cell"],
                          evidence=c["factory_evidence"]) for c in new_cards],
                pending=pending, results=rows, by_kind=by_kind, by_tag=by_tag,
                retired=sorted(k for k in by_kind if prior(by_kind, k, S) is None), settings=S)


def lines(fl, n=5):
    """Plain-English lines for the weekly review, the emails and Claude's fact sheet."""
    if not fl:
        return []
    out = []
    for c in fl.get("new") or []:
        out.append(f"new repair {c['id']}: {c['parent'].replace('|', ' ')} lost on {c['tag']} - testing {c['kind']}")
    rows = sorted(fl.get("results") or [], key=lambda r: r.get("checked") or "", reverse=True)[:n]
    for r in rows:
        verdict = "passed" if r["passed"] else ("helped" if r["helped"] else "did not help")
        out.append(f"{r['child'].replace('|', ' ')} ({r['kind']} for {r['tag']}): {r['avg_r']:+.2f}R vs parent "
                   f"{r['parent_avg_r']:+.2f}R, unseen {r['test_r']:+.2f}R vs {r['parent_test_r']:+.2f}R - {verdict}")
    bk = fl.get("by_kind") or {}
    if bk:
        out.append("repair record: " + ", ".join(f"{k} helped {v['helped']} of {v['tried']}"
                                                 for k, v in sorted(bk.items(), key=lambda x: -x[1]["tried"])))
    if fl.get("retired"):
        out.append("stopped trying (never helped): " + ", ".join(fl["retired"]))
    if fl.get("pending"):
        out.append(f"{len(fl['pending'])} repair(s) waiting for their first test")
    return out
