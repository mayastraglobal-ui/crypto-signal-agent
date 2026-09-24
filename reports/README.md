# reports/

| On main (history kept) | On branch `live-reports` (newest copy only, replaced every run) |
|---|---|
| `latest.md` - the newest report | `latest.json` - the whole report as data |
| `daily/YYYY-MM-DD.md` - the last report of each day | `data_quality.json`, `features.json`, `feature_evidence.json`, `regime.json`, `smc.json` |
| `signals_log.csv` - every signal and how it ended | `research.json` - the daily research run |
| `strategy_scoreboard.csv` - status per strategy version and timeframe | |
| `universe.json`, `*_state.json`, `notified.json` - small state the engine needs next run | |

Why: the large files are rewritten completely every hour; committing them to main would make the repository
grow by megabytes a day. `publish_live.py` puts them on `live-reports` as ONE commit (force-pushed, no history).
Links: https://github.com/mayastraglobal-ui/crypto-signal-agent/tree/live-reports/reports
