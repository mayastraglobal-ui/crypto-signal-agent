# reports/

| On main (history kept) | On branch `live-reports` (newest copy only, replaced every run) |
|---|---|
| `latest.md` - the newest report | `latest.json` - the whole report as data |
| `daily/YYYY-MM-DD.md` - the last report of each day | `data_quality.json`, `features.json`, `feature_evidence.json`, `regime.json`, `smc.json` |
| `signals_log.csv` - every signal, its state and how it ended | `research.json` - the daily research run |
| `positions.json` - the position book now; `position_events.csv` - every state change | |
| `strategy_scoreboard.csv` - status per strategy version and timeframe | |
| `universe.json`, `*_state.json`, `notified.json` - small state the engine needs next run | |
| `pine/` - TradingView Pine scripts (APPROVED strategies daily; others via Actions → Pine export) | |
| `approval/` - approval packs of strategies ready for your yes / no (daily research run) | |
| `claude/briefings|daily|weekly/` - Claude's task outputs, checked by the Brain guard; `claude/state.json` - the last push handled per task branch | |

Why: the large files are rewritten completely every hour; committing them to main would make the repository
grow by megabytes a day. `publish_live.py` puts them on `live-reports` as ONE commit (force-pushed, no history).
Links: https://github.com/mayastraglobal-ui/crypto-signal-agent/tree/live-reports/reports

The dashboard page (`build_dashboard.py`) is published to its own branch `gh-pages` the same way (one commit,
no history) and shown at https://mayastraglobal-ui.github.io/crypto-signal-agent/ ; its chart candles come from
`dashboard_data.json` on `live-reports`.
