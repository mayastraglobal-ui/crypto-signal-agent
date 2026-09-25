# memory/ - what the agent remembers

AGENT_PROMPT.md section 22. **Read memory before every decision.** Failed experiments are valuable knowledge.
Append-only files may only grow: `memory_guard.py` runs in both workflows before anything is committed and
stops the run if an earlier line was changed or removed (section 17).

| File | Contents | Written by | When | Append-only |
|---|---|---|---|---|
| `strategy_registry.csv` | Per strategy version × timeframe: status, metrics, gates, dates | engine (research run) | daily | no - statuses update |
| `experiments.md` | Every strategy version ever tested (EXP-ID, hypothesis) | engine (research run) | first test of a version | yes |
| `trials.csv` | Every strategy version × timeframe ever tested (one row each) - the trials counter that raises the PAPER_TRADING bar | engine (research run) | first test of a cell | yes |
| `strategy_lifecycle.md` | Every status change and why | engine (research run) | on change | yes |
| `failure_journal.md` | Every logged signal that lost: conditions, tags, MAE / MFE | engine (hourly scan) + reviews | on a loss | yes |
| `missed_trades.md` | Strong moves and whether they were identifiable before | engine (research run) | daily, if any | yes |
| `lessons.md` | Validated lessons with evidence counts | reviews (Claude) / operator only | after a review | yes |
| `research_sources.md` | Sources, claims, evidence classes, derived hypotheses | engine (research run, from the cards) + reviews | first test of a version | yes |
| `coin_notes.md` | How each signal coin behaves (measured facts + review notes) | engine (hourly scan) + reviews | weekly (Sunday) | yes |
| `execution_notes.md` | Data problems (start / end), fee settings, slippage | engine (hourly scan) | on change | yes |
| `feature_notes.md` | What each feature means and whether it is proven | Claude (build / reviews) | when features change | no - living definitions |
| `smc_research.md` | The SMC definitions used and what has been proven | Claude (build / reviews) | when SMC rules change | no - living definitions |
| `smc_events.csv` | Every SMC detection, logged live | engine (hourly scan) | every scan | yes |
| `market_regime_log.md` | Daily regime per coin, BTC context | engine (hourly scan) | once a day | yes |
| `universe_log.md` | Coins that joined, left or were excluded, and why | engine (hourly scan) | on change | yes |
| `changelog.md` | Every rule / config / engine change (who, when, why) | Claude + operator | every change | yes |

Also on main: `reports/signals_log.csv` (every signal, state and outcome), `reports/position_events.csv` (every
state change, append-only), `reports/positions.json` (the position book).

**Record format** (the knowledge files: failure journal, missed trades, lessons, research sources, coin notes,
execution notes): a `###` title, then one line
`- timestamp: … · source: … · evidence: <CLASS>: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD`
and the details. Evidence classes (section 18): FACT · RESEARCH_FINDING · BACKTEST_EVIDENCE · CLAIM ·
HYPOTHESIS · MODEL_OUTPUT · UNVERIFIED_OPINION. Records whose review date has passed are listed in the report
(section 3e) for the reviews. Review periods: `config.yaml` → `memory`.

The engine writes **facts only**; it never writes lessons and never invents sources or citations.

**Claude's tasks** (Phase 14, `tasks/`) add to the knowledge files only through the Brain guard (`brain_guard.py`,
`engine/brain.py`): records added at the end of `lessons.md`, `failure_journal.md`, `missed_trades.md`,
`research_sources.md`, `coin_notes.md`, `feature_notes.md`, `smc_research.md` and `experiments.md` - nothing else,
never an edit. A lesson needs FACT / RESEARCH_FINDING / BACKTEST_EVIDENCE with counts. A review of a due record is
a NEW record ("Review: <title>", CONFIRMED / REJECTED / KEEP); the old one stays.
