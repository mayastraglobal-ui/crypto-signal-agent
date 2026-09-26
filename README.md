# live-reports

The newest copy of the large report files of the Crypto Signal Agent, replaced on every run
(one commit, force-pushed - this branch has no history on purpose).

| File | Written by | What |
|---|---|---|
| reports/latest.json | hourly scan | the whole report as data (signals, scoreboard, regimes, SMC ...) |
| reports/data_quality.json | hourly scan | data check per coin and timeframe |
| reports/features.json | hourly scan | newest features per coin and timeframe |
| reports/feature_evidence.json | hourly scan | candle / SMC patterns vs random entries |
| reports/regime.json | hourly scan | market regime per coin and timeframe, with evidence |
| reports/smc.json | hourly scan | SMC state and newest events |
| reports/research.json | daily research run | Layers A/B/C, stress, +-20%, failure attribution, missed moves |
| reports/derivs_hourly.csv.gz | hourly scan (derivs.py) | futures data history: open interest, long/short, taker ratio |
| reports/funding.csv.gz | hourly scan (derivs.py) | funding rate history (every settlement) |

The history that matters (memory/, signals_log.csv, strategy_scoreboard.csv, daily reports, latest.md)
is on the main branch.
