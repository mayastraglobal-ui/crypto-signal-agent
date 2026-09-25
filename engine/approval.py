"""
Approval packs and the operator's yes (AGENT_PROMPT.md sections 12 and 21) - Phase 14.

  PAPER_TRADING -> APPROVED needs (section 12):
    * >= 20 closed paper signals (config.yaml approval.min_paper_signals)
    * paper expectancy >= 0R
    * no material divergence from the backtest: the paper average may be at most 0.30R below the
      backtest's average on unseen data (approval.max_divergence_r)
    * AND the operator's explicit yes: a line under `approvals:` in config.yaml

A strategy that meets the numbers gets an approval pack (reports/approval/) with everything section 21 lists,
and the weekly email asks "Approve ... for live emails? (yes/no)". The engine NEVER approves by itself:
without the operator's line nothing changes. Removing the line moves the strategy back to PAPER_TRADING.

Pure functions; no internet.
"""
import datetime as dt
import re

from engine import debate
from engine import strategy_spec as sspec

DEFAULTS = dict(min_paper_signals=20, min_paper_avg_r=0.0, max_divergence_r=0.30)


def settings(section):
    S = dict(DEFAULTS)
    S.update({k: v for k, v in (section or {}).items() if k in DEFAULTS})
    return S


def cell_key(strategy, version, tf):
    return f"{strategy}@{version}|{tf}"


def parse_approvals(entries):
    """config.yaml `approvals:` -> ({cell key: entry}, [problems]). Each entry needs strategy, version, tf and
    date (YYYY-MM-DD, the day you said yes)."""
    out, problems = {}, []
    for i, e in enumerate(entries or [], 1):
        if not isinstance(e, dict):
            problems.append(f"approvals entry {i}: not a strategy / version / tf / date block")
            continue
        miss = [k for k in ("strategy", "version", "tf", "date") if not str(e.get(k) or "").strip()]
        if miss:
            problems.append(f"approvals entry {i}: missing {', '.join(miss)}")
            continue
        day = str(e["date"]).strip()
        try:
            dt.datetime.strptime(day, "%Y-%m-%d")
        except ValueError:
            problems.append(f"approvals entry {i}: date {day!r} is not YYYY-MM-DD")
            continue
        k = cell_key(str(e["strategy"]).strip(), str(e["version"]).strip(), str(e["tf"]).strip())
        out[k] = dict(strategy=str(e["strategy"]).strip(), version=str(e["version"]).strip(),
                      tf=str(e["tf"]).strip(), date=day, note=str(e.get("note") or "").strip())
    return out, problems


def eligible(status, paper, backtest_avg_r, S):
    """Section 12 numbers for PAPER_TRADING -> APPROVED. paper = lifecycle.paper_record() (n, avg_r ...);
    backtest_avg_r = average R of the backtest on unseen data (Layer B validate part). Returns (ok, reasons)."""
    reasons = []
    if status not in ("PAPER_TRADING", "APPROVED"):
        reasons.append(f"status is {status or 'not tested'}, not PAPER_TRADING")
    n, avg = int(paper.get("n") or 0), paper.get("avg_r")
    if n < S["min_paper_signals"]:
        reasons.append(f"{n} closed paper signals, needs {S['min_paper_signals']}")
    if avg is None or avg < S["min_paper_avg_r"]:
        reasons.append("paper average " + ("unknown" if avg is None else f"{avg:+.2f}R")
                       + f" (needs >= {S['min_paper_avg_r']:+.2f}R)")
    if backtest_avg_r is None:
        reasons.append("no backtest average on unseen data to compare with")
    elif avg is not None and round(backtest_avg_r - avg, 9) > S["max_divergence_r"]:
        reasons.append(f"paper {avg:+.2f}R is {backtest_avg_r - avg:.2f}R below the backtest's {backtest_avg_r:+.2f}R "
                       f"(material divergence, limit {S['max_divergence_r']:.2f}R)")
    return not reasons, reasons


def decide(status, listed, ok, reasons, lab=False):
    """The status after the operator's approvals list is applied (after the automatic lifecycle move).
    listed = this cell's approvals entry or None; lab = a strategies_lab.yaml card (Phase 17), which is never
    approved - the operator moves it into strategies.yaml by pull request first. Returns (status, note, warning)."""
    if lab:
        if status == "APPROVED":
            status = "PAPER_TRADING"
        return status, "", ("approval not applied - a lab card (strategies_lab.yaml) is never approved: copy the card "
                            "unchanged into strategies.yaml by pull request first" if listed else None)
    if status == "PAPER_TRADING" and listed:
        if ok:
            return "APPROVED", f"operator approved on {listed['date']}", None
        return status, "", "approval not applied - not eligible: " + "; ".join(reasons)
    if status == "APPROVED" and not listed:
        return "PAPER_TRADING", "operator approval removed from config.yaml - back to paper", None
    if listed and status != "APPROVED":
        return status, "", f"approval not applied - status is {status or 'not tested'} (only PAPER_TRADING can be approved)"
    return status, "", None


def _f(x, fmt="+.2f", unit="R"):
    return "-" if x is None else f"{x:{fmt}}{unit}"


def _kv(x):
    if isinstance(x, dict):
        return ", ".join(f"{k} {_kv(v)}" for k, v in x.items())
    if isinstance(x, list):
        return " / ".join(_kv(v) for v in x)
    return str(x)


def _stat(st):
    return (f"{st['n']} trades · avg {_f(st['avg_r'], '+.3f')} · win rate {st['win_rate']:.0f}% · "
            f"profit factor {st['pf']:.2f} · max drawdown {st['max_dd_r']:.1f}R")


def pack(cell, spec, lineage, board_row, S, now_txt, risk=None):
    """The approval pack (section 21) of one strategy version x timeframe as markdown lines.
    cell = research.json cell; spec = the strategy card; lineage = [(version, first tested, status)] of the same
    idea; board_row = its scoreboard row (Layer A) or {}; risk = debate.risk_manager() on today's hourly report
    (None = conditions unknown, which is a veto)."""
    ev, att, paper = cell["evidence"], cell.get("attribution") or {}, cell.get("paper") or {}
    k = f"{cell['strategy']} v{cell['version']} {cell['tf']}"
    L = [f"# Approval pack: {k}", "",
         f"Written by the engine on {now_txt} UTC (AGENT_PROMPT.md section 21). Numbers only - the decision is yours.",
         "", "**Question: Approve " + k + " for live emails? (yes/no)**", "",
         *(["**This is a LAB card** (`strategies_lab.yaml`, written by Claude's reviews). A lab card never sends "
            "emails and is never approved. To say yes: FIRST copy the card unchanged into `strategies.yaml` by pull "
            "request (same id and version - its results carry over), THEN add the line below.", ""]
           if spec.get("lab") else []),
         "To say yes, add this under `approvals:` in `config.yaml` (on GitHub: open the file, pencil icon, commit):",
         "```", f"  - {{strategy: {cell['strategy']}, version: \"{cell['version']}\", tf: {cell['tf']}, "
                f"date: {now_txt[:10]}}}", "```",
         "The next daily research run moves it to APPROVED. To undo, delete the line. Saying nothing = no.",
         "To look at it on TradingView first: GitHub → Actions → \"Pine export\" → Run workflow with "
         f"`{cell['strategy']}` / `{cell['version']}` / `{cell['tf']}`, then paste `reports/pine/"
         f"{re.sub(r'[^A-Za-z0-9_.-]+', '_', cell['strategy'] + '_v' + cell['version'] + '_' + cell['tf'])}.pine` into "
         "TradingView's Pine Editor.", "",
         "## 0. Bull vs bear (the engine's numbers only - Phase 18)",
         *[f"- {x}" for x in debate.case_lines(*debate.cell_cases(cell), risk or debate.risk_manager(None, None))],
         "- A veto means \"not now\": wait until the risk manager has no veto before you say yes. No veto is never "
         "a reason to say yes - the decision stays yours.", "",
         "## 1. Definition and lineage",
         f"- family: {spec.get('family', '-')} · gate: {spec.get('gate', '-')} · regimes: "
         f"{', '.join(spec.get('regimes') or []) or '-'}",
         f"- hypothesis: {' '.join(str(spec.get('hypothesis') or '-').split())}",
         f"- source: {' '.join(str(spec.get('source') or '-').split())}",
         f"- long: {'; '.join(spec.get('long') or []) or '-'}",
         f"- short: {'; '.join(spec.get('short') or []) or '-'}",
         f"- stop: {_kv(spec.get('stop'))} · targets: {_kv(spec.get('targets')) if spec.get('targets') else 'config default'} · "
         f"5m confirmation: {'yes' if spec.get('confirm_5m') else 'no'}",
         "- lineage: " + ("; ".join(f"v{v} first tested {d} ({s})" for v, d, s in lineage) or "this is the first version"),
         "- edge (why it should work - a hypothesis; sections 2-7 test it): "
         + (" · ".join(sspec.edge_lines(spec)) or "NOT WRITTEN - ask for an edge block before saying yes"),
         "", "## 2. Backtest (Layers A / B)",
         "- Layer B, whole history: " + _stat(ev["all"]),
         "- Layer B, develop part (first 70%): " + _stat(ev["develop"]),
         "- Layer B, unseen part (last 30%): " + _stat(ev["validate"]),
         f"- long / short: {_f(ev['long']['avg_r'], '+.3f')} ({ev['long']['n']}) / {_f(ev['short']['avg_r'], '+.3f')} "
         f"({ev['short']['n']})",
         f"- coins with an edge: {', '.join(ev['positive_coins']) or 'none'}"]
    if board_row.get("layer_a_trades") not in (None, ""):
        L.append(f"- Layer A (last 15 days): {board_row.get('layer_a_trades')} trades, avg "
                 f"{_f(board_row.get('layer_a_avg_r'), '+.3f')}")
    wf = ev["walk_forward"]
    L += ["", "## 3. Walk-forward (Layer C)",
          f"- {wf['positive']} of {wf['judged']} windows profitable, all judged windows together "
          f"{_f(wf['pooled_avg_r'], '+.3f')} over {wf['pooled_n']} trades - {'passed' if wf['passed'] else 'NOT passed'}"]
    L += [f"  - window {w['window']}: {w['n']} trades, {_f(w['avg_r'], '+.3f')} ({w['verdict']})" for w in wf["windows"]]
    L += ["", "## 4. Paper trading",
          f"- {paper.get('n', 0)} closed paper signals, average {_f(paper.get('avg_r'))}, last 20 average "
          f"{_f(paper.get('last_avg_r'))}, drawdown {paper.get('max_dd_r', 0):.1f}R",
          f"- backtest on unseen data {_f(ev['validate']['avg_r'])} vs paper {_f(paper.get('avg_r'))} "
          f"(allowed gap {S['max_divergence_r']:.2f}R)"]
    tw = cell.get("twin_same_window")
    L += ["", "## 5. Control twin (the same idea without its special ingredient)",
          f"- {spec.get('control_twin') or ('the same strategy without the 5m check' if spec.get('confirm_5m') else 'none')}: "
          + {True: "beaten", False: "NOT beaten", None: "too few trades to compare"}.get(cell.get("beats_twin"), "no twin")]
    if tw:
        L.append(f"- twin over the same period: {_stat(tw['all'])}")
    pv = ev["perturbation"]
    L += ["", "## 6. Sensitivity (every parameter -20% / +20%)",
          f"- {'stable: every variant stays profitable' if pv['stable'] else 'NOT stable'}"
          + (f" · worst: {pv['worst']['change']} {_f(pv['worst']['avg_r'], '+.3f')}" if pv["worst"] else "")]
    L += [f"  - {v['change']}: {v['n']} trades, {_f(v['avg_r'], '+.3f')}" for v in pv["variants"]]
    L += ["", "## 7. Cost stress test",
          f"- fees, slippage and funding +50%: {_stat(ev['stress'])}",
          f"- median cost per trade: {_f(ev['median_cost_r'], '.3f')}"]
    L += ["", "## 8. Risk metrics",
          f"- max drawdown (backtest): {ev['all']['max_dd_r']:.1f}R · average hold {ev['all']['avg_bars']:.0f} candles",
          "- live risk per trade: 0.5% of the account for the first 30 days, then at most 1% (risk engine, section 15)"]
    tags = sorted(((t, v) for t, v in (att.get("tags") or {}).items() if v.get("losers")),
                  key=lambda x: -x[1]["losers"])[:6]
    L += ["", "## 9. Why it loses (failure attribution)",
          f"- {att.get('losses', 0)} losing / {att.get('wins', 0)} winning backtest trades; systematic tags: "
          f"{', '.join(att.get('systematic') or []) or 'none'}"]
    L += [f"  - {t}: {v['losers']} losers ({v['loss_share'] * 100:.0f}% of losses)" for t, v in tags]
    L += [f"  - {d}" for d in (att.get("diagnosis") or [])[:6]]
    L += ["", "## 10. Known limitations",
          "- backtests and paper results are history, not a promise; the future can differ",
          "- the agent never trades: real fills, slippage and funding can be worse than assumed"]
    if spec.get("known_weaknesses"):
        L.append(f"- known weaknesses (card): {' '.join(str(spec['known_weaknesses']).split())}")
    L += [f"- {o}" for o in ev.get("overfit") or []]
    if cell.get("history_from"):
        L.append(f"- history starts {cell['history_from']} - " + ("short history" if cell["history_from"] > "2024" else
                                                                     "check it covers a bull and a bear market"))
    L += ["", "Research signal. Not financial advice."]
    return L


def filename(strategy, version, tf):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{strategy}_v{version}_{tf}") + ".md"
