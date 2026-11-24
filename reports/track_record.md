# 📈 Live track record

Updated 2026-11-24 21:11 UTC by the hourly scan (engine/track_record.py). Every TEST / PAPER / LIVE setup the hourly scan recorded (entry at the signal close, after fees). 'Your alerts' = the setups that could reach your Telegram (versions of one setup counted once); the silent research records are the other positive program pairs GitHub keeps for the research. The alerts actually sent and your ✅ / ❌ are in the journal review.

| Stage | Closed | Win % | Average | Total | Worst drawdown | Longest losing run |
|---|---:|---:|---:|---:|---:|---:|
| **Your alerts** (could reach your Telegram) | 54 | 57 | +0.45R | +24.39R | 5.47R | 6 |
| Silent research records (never sent to you) | 200 | 34 | -0.04R | -9.06R | 41.01R | 17 |
| 🔵 TEST | 262 | 36 | +0.05R | +12.40R | 47.91R | 20 |
| 🟡 PAPER | 140 | 51 | +0.34R | +47.62R | 34.80R | 19 |
| 🟢 LIVE | 0 | - | - | +0.00R | 0.00R | 0 |
| **All** | 402 | 41 | +0.15R | +60.02R | 59.17R | 30 |

## 🚨 Drift monitor

- nothing paused: every strategy's live results are inside what its backtest calls normal.

Warning signs (no pause yet):
- TRD-H4-BREAKOUT-S3@1.0 1h on ETH: 4 losses in a row - in its backtest (36% won) a run that long shows up in 89% of 15-trade periods
- P01-BREAKOUT-V1@1.0 4h on BTC: 3 losses in a row - in its backtest (45% won) a run that long shows up in 72% of 9-trade periods
- donchian_breakout-VEXIT-FDISP@1.0 4h on BTC: 3 losses in a row - in its backtest (47% won) a run that long shows up in 68% of 9-trade periods
- donchian_breakout-VEXIT@1.0 4h on BTC: 3 losses in a row - in its backtest (47% won) a run that long shows up in 68% of 9-trade periods
- donchian_breakout-VEXIT-S4@1.0 4h on BTC: 3 losses in a row - in its backtest (45% won) a run that long shows up in 59% of 7-trade periods
- P04-MACD-SUPERTREND-V2@1.0 15m on ETH: 4 losses in a row - in its backtest (38% won) a run that long shows up in 37% of 6-trade periods
- P07-SQUEEZE-RETEST-V2@1.0 30m on ETH: 4 losses in a row - in its backtest (34% won) a run that long shows up in 34% of 5-trade periods
- P01-BREAKOUT-V2@1.0 1h on SOL: 3 losses in a row - in its backtest (34% won) a run that long shows up in 28% of 3-trade periods
- P01-BREAKOUT-V2@1.0 30m on SUI: 3 losses in a row - in its backtest (39% won) a run that long shows up in 23% of 3-trade periods
- P01-BREAKOUT-V3@1.0 4h on BTC: 3 losses in a row - in its backtest (51% won) a run that long shows up in 12% of 3-trade periods
- P01-BREAKOUT-V3@1.0 4h on ETH: 3 losses in a row - in its backtest (44% won) a run that long shows up in 18% of 3-trade periods
- P01-BREAKOUT-V5@1.0 1h on ETH: 3 losses in a row - in its backtest (34% won) a run that long shows up in 29% of 3-trade periods
- donchian_breakout-VEXIT-FDISP-S2@1.0 4h on SUI: 3 losses in a row - in its backtest (38% won) a run that long shows up in 24% of 3-trade periods

## Per strategy and coin (live vs 5-year backtest)

| Strategy | TF | Coin | Stage | Sent to you | Closed | Win % | Live avg | Backtest avg | Total | Worst DD | Check |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P01-BREAKOUT-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 9 | 44 | +0.60R | +0.38R | +5.38R | 2.51R | ⚠️ watch |
| donchian_breakout-VEXIT-FDISP | 4h | BTC | 🟡 PAPER | ✅ yes | 9 | 56 | +0.93R | +0.53R | +8.35R | 2.80R | ⚠️ watch |
| donchian_breakout-VEXIT | 4h | BTC | 🟡 PAPER | ✅ yes | 9 | 56 | +0.93R | +0.53R | +8.35R | 2.80R | ⚠️ watch |
| donchian_breakout-VEXIT-S4 | 4h | BTC | 🟡 PAPER | ✅ yes | 7 | 57 | +1.00R | +0.46R | +6.98R | 2.80R | ⚠️ watch |
| P01-BREAKOUT-V3 | 4h | BTC | 🔵 TEST | ✅ yes | 3 | 0 | -0.84R | +0.55R | -2.51R | 2.51R | ⚠️ watch |
| P01-BREAKOUT-V3 | 4h | ETH | 🔵 TEST | ✅ yes | 3 | 0 | -1.03R | +0.20R | -3.08R | 3.08R | ⚠️ watch |
| donchian_breakout-VEXIT-FDISP-S2 | 4h | SUI | 🟡 PAPER | ✅ yes | 3 | 0 | -0.86R | +0.14R | -2.59R | 2.59R | ⚠️ watch |
| TRD-H4-BREAKOUT-S3 | 1h | BTC | 🟡 PAPER | ✅ yes | 20 | 50 | +0.47R | +0.34R | +9.50R | 5.32R | ✅ |
| donchian_breakout-VEXIT | 4h | XRP | 🟡 PAPER | ✅ yes | 10 | 70 | +0.96R | +0.13R | +9.57R | 1.03R | ✅ |
| donchian_breakout | 4h | BTC | 🟡 PAPER | ✅ yes | 9 | 78 | +0.64R | +0.27R | +5.78R | 1.08R | ✅ |
| P01-BREAKOUT-V3 | 4h | XRP | 🔵 TEST | ✅ yes | 8 | 62 | +1.17R | +0.26R | +9.39R | 1.02R | ✅ |
| donchian_breakout-VEXIT | 4h | ETH | 🟡 PAPER | ✅ yes | 8 | 50 | +0.52R | +0.32R | +4.14R | 3.10R | ✅ |
| donchian_breakout | 4h | ETH | 🟡 PAPER | ✅ yes | 8 | 62 | +0.18R | +0.19R | +1.42R | 2.06R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | ETH | 🟡 PAPER | ✅ yes | 7 | 43 | +0.24R | +0.38R | +1.68R | 3.10R | ✅ |
| donchian_breakout-VEXIT | 4h | SOL | 🟡 PAPER | ✅ yes | 7 | 43 | -0.05R | +0.22R | -0.37R | 2.08R | ✅ |
| donchian_breakout | 4h | SOL | 🟡 PAPER | ✅ yes | 7 | 57 | -0.16R | +0.21R | -1.10R | 2.08R | ✅ |
| P01-BREAKOUT-V1 | 4h | ETH | 🔵 TEST | ✅ yes | 6 | 33 | -0.12R | +0.24R | -0.73R | 3.08R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | XRP | 🟡 PAPER | ✅ yes | 6 | 83 | +1.50R | +0.23R | +9.03R | 1.03R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | ETH | 🟡 PAPER | ✅ yes | 5 | 40 | +0.06R | +0.38R | +0.28R | 3.10R | ✅ |
| P01-BREAKOUT-V1 | 4h | SUI | 🔵 TEST | ✅ yes | 4 | 25 | -0.20R | +0.20R | -0.80R | 1.08R | ✅ |
| P01-BREAKOUT-V3 | 4h | SUI | 🔵 TEST | ✅ yes | 4 | 25 | -0.20R | +0.40R | -0.80R | 1.08R | ✅ |
| P01-BREAKOUT-V4 | 4h | ETH | 🔵 TEST | ✅ yes | 4 | 50 | +0.31R | +0.21R | +1.25R | 1.05R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | SUI | 🟡 PAPER | ✅ yes | 4 | 25 | -0.28R | +0.19R | -1.13R | 1.35R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | SUI | 🟡 PAPER | ✅ yes | 4 | 25 | -0.28R | +0.20R | -1.13R | 1.35R | ✅ |
| donchian_breakout-VEXIT | 4h | SUI | 🟡 PAPER | ✅ yes | 4 | 25 | -0.28R | +0.15R | -1.13R | 1.35R | ✅ |
| P01-BREAKOUT-V4 | 4h | SUI | 🔵 TEST | ✅ yes | 3 | 33 | -0.18R | +0.25R | -0.54R | 2.06R | ✅ |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 3 | 67 | +1.28R | +0.25R | +3.83R | 1.11R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | SOL | 🟡 PAPER | ✅ yes | 3 | 33 | -0.58R | +0.19R | -1.75R | 2.08R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | SOL | 🟡 PAPER | ✅ yes | 3 | 33 | +0.12R | +0.29R | +0.37R | 2.08R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | XRP | 🟡 PAPER | ✅ yes | 3 | 100 | +1.38R | +0.12R | +4.14R | 0.00R | ✅ |
| P01-BREAKOUT-V1 | 4h | SOL | 🔵 TEST | ✅ yes | 2 | 50 | -0.09R | +0.31R | -0.18R | 0.65R | ✅ |
| P01-BREAKOUT-V4 | 4h | SOL | 🔵 TEST | ✅ yes | 2 | 50 | +0.23R | +0.32R | +0.47R | 1.03R | ✅ |
| P07-SQUEEZE-RETEST-V3 | 4h | BTC | 🔵 TEST | ✅ yes | 2 | 100 | +2.47R | +0.44R | +4.94R | 0.00R | ✅ |
| donchian_breakout-VEXIT-FDISP-S2 | 4h | BTC | 🟡 PAPER | ✅ yes | 2 | 0 | -1.03R | +0.48R | -2.07R | 2.07R | ✅ |
| donchian_breakout-VEXIT-FDISP-S2 | 4h | ETH | 🟡 PAPER | ✅ yes | 2 | 0 | -1.03R | +0.44R | -2.06R | 2.06R | ✅ |
| donchian_breakout-VEXIT-FRETEST | 4h | BTC | 🟡 PAPER | ✅ yes | 2 | 0 | -0.90R | +0.56R | -1.80R | 1.80R | ✅ |
| donchian_breakout-VEXIT-FRETEST | 4h | ETH | 🟡 PAPER | ✅ yes | 2 | 0 | -1.03R | +0.46R | -2.05R | 2.05R | ✅ |
| donchian_breakout-VEXIT-FRETEST | 4h | SUI | 🟡 PAPER | ✅ yes | 2 | 0 | -0.79R | +0.10R | -1.58R | 1.58R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | SOL | 🟡 PAPER | ✅ yes | 2 | 50 | -0.22R | +0.22R | -0.44R | 0.78R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | ETH | 🟡 PAPER | ✅ yes | 2 | 50 | +0.70R | +0.43R | +1.40R | 1.05R | ✅ |
| P01-BREAKOUT-V4 | 4h | BNB | 🔵 TEST | ✅ yes | 1 | 100 | +1.80R | +0.18R | +1.80R | 0.00R | ✅ |
| P02-EMA-PULLBACK-V4 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 100 | +3.77R | +0.21R | +3.77R | 0.00R | ✅ |
| P04-MACD-SUPERTREND-V3 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.03R | +0.27R | -1.03R | 1.03R | ✅ |
| P05-RANGE-REVERSAL-V4 | 4h | SOL | 🔵 TEST | ✅ yes | 1 | 0 | -1.06R | +0.24R | -1.06R | 1.06R | ✅ |
| P07-SQUEEZE-RETEST-V1 | 4h | SOL | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.13R | -1.05R | 1.05R | ✅ |
| P07-SQUEEZE-RETEST-V3 | 4h | XRP | 🔵 TEST | ✅ yes | 1 | 100 | +2.47R | +0.18R | +2.47R | 0.00R | ✅ |
| P07-SQUEEZE-RETEST-V4 | 4h | BNB | 🔵 TEST | ✅ yes | 1 | 100 | +2.07R | +0.13R | +2.07R | 0.00R | ✅ |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.41R | -1.11R | 1.11R | ✅ |
| P12-LEADER-V1 | 4h | ZEC | 🔵 TEST | ✅ yes | 1 | 0 | -1.02R | +0.41R | -1.02R | 1.02R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | BNB | 🟡 PAPER | ✅ yes | 1 | 100 | +0.93R | +0.16R | +0.93R | 0.00R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | BNB | 🟡 PAPER | ✅ yes | 1 | 100 | +0.93R | +0.24R | +0.93R | 0.00R | ✅ |
| donchian_breakout-VEXIT | 4h | BNB | 🟡 PAPER | ✅ yes | 1 | 100 | +0.93R | +0.29R | +0.93R | 0.00R | ✅ |
| donchian_breakout-VEXIT | 4h | ZEC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.01R | +0.07R | -1.01R | 1.01R | ✅ |
| donchian_breakout | 4h | BNB | 🟡 PAPER | ✅ yes | 1 | 100 | +1.24R | +0.21R | +1.24R | 0.00R | ✅ |
| P01-BREAKOUT-V5 | 30m | SUI | 🔵 TEST | silent | 8 | 0 | -0.98R | +0.02R | -7.86R | 7.86R | 🚨 paused |
| TRD-H4-BREAKOUT-S3 | 1h | ETH | 🔵 TEST | silent | 15 | 33 | +0.11R | +0.07R | +1.61R | 3.17R | ⚠️ watch |
| P04-MACD-SUPERTREND-V2 | 15m | ETH | 🔵 TEST | silent | 6 | 17 | -0.50R | +0.03R | -2.99R | 4.43R | ⚠️ watch |
| P07-SQUEEZE-RETEST-V2 | 30m | ETH | 🔵 TEST | silent | 5 | 20 | -0.80R | +0.04R | -3.98R | 4.53R | ⚠️ watch |
| P01-BREAKOUT-V2 | 1h | SOL | 🔵 TEST | silent | 3 | 0 | -1.05R | +0.02R | -3.15R | 3.15R | ⚠️ watch |
| P01-BREAKOUT-V2 | 30m | SUI | 🔵 TEST | silent | 3 | 0 | -1.06R | +0.12R | -3.20R | 3.20R | ⚠️ watch |
| P01-BREAKOUT-V5 | 1h | ETH | 🔵 TEST | silent | 3 | 0 | -0.84R | +0.02R | -2.52R | 2.52R | ⚠️ watch |
| P01-BREAKOUT-V2 | 30m | BTC | 🔵 TEST | silent | 12 | 50 | +0.53R | +0.10R | +6.31R | 1.28R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | 🔵 TEST | silent | 11 | 27 | -0.22R | +0.01R | -2.39R | 5.69R | ✅ |
| P01-BREAKOUT-V2 | 1h | BTC | 🔵 TEST | silent | 10 | 40 | -0.01R | +0.12R | -0.14R | 2.17R | ✅ |
| P03-FIB-PULLBACK-V5 | 1h | SOL | 🔵 TEST | silent | 10 | 40 | +0.13R | +0.04R | +1.30R | 3.63R | ✅ |
| TRD-H4-BREAKOUT-S3 | 1h | XRP | 🔵 TEST | silent | 10 | 30 | -0.14R | +0.30R | -1.39R | 4.20R | ✅ |
| P01-BREAKOUT-V2 | 30m | ETH | 🔵 TEST | silent | 9 | 33 | -0.08R | +0.14R | -0.74R | 3.19R | ✅ |
| P01-BREAKOUT-V2 | 30m | SOL | 🔵 TEST | silent | 9 | 22 | -0.44R | +0.07R | -3.97R | 4.88R | ✅ |
| P01-BREAKOUT-V5 | 1h | SUI | 🔵 TEST | silent | 7 | 14 | -0.57R | +0.08R | -4.01R | 5.05R | ✅ |
| P03-FIB-PULLBACK-V5 | 1h | SUI | 🔵 TEST | silent | 7 | 43 | +0.23R | +0.03R | +1.57R | 4.31R | ✅ |
| TRD-H4-BREAKOUT-S3 | 1h | SOL | 🔵 TEST | silent | 7 | 29 | -0.25R | +0.17R | -1.78R | 2.15R | ✅ |
| P01-BREAKOUT-V2 | 15m | BTC | 🔵 TEST | silent | 6 | 33 | -0.59R | +0.09R | -3.57R | 3.57R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | 🔵 TEST | silent | 4 | 50 | +0.30R | +0.01R | +1.19R | 2.16R | ✅ |
| P08-SESSION-BREAKOUT-V4 | 1h | BTC | 🔵 TEST | silent | 4 | 50 | +0.38R | +0.04R | +1.51R | 1.12R | ✅ |
| TRD-H4-BREAKOUT-S3 | 1h | SUI | 🔵 TEST | silent | 4 | 50 | +0.35R | +0.07R | +1.39R | 2.07R | ✅ |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | 🔵 TEST | silent | 3 | 33 | +0.10R | +0.04R | +0.31R | 1.07R | ✅ |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | 🔵 TEST | silent | 3 | 67 | +0.82R | +0.19R | +2.45R | 0.90R | ✅ |
| P08-SESSION-BREAKOUT-V1 | 1h | BTC | 🔵 TEST | silent | 3 | 33 | +0.16R | +0.05R | +0.48R | 2.00R | ✅ |
| P01-BREAKOUT-V2 | 1h | SUI | 🔵 TEST | silent | 2 | 50 | +0.01R | +0.15R | +0.02R | 1.03R | ✅ |
| P04-MACD-SUPERTREND-V1 | 4h | ETH | 🔵 TEST | silent | 2 | 50 | +0.72R | +0.17R | +1.44R | 1.03R | ✅ |
| P04-MACD-SUPERTREND-V1 | 4h | ZEC | 🔵 TEST | silent | 2 | 0 | -1.02R | +0.12R | -2.04R | 2.04R | ✅ |
| P04-MACD-SUPERTREND-V2 | 30m | XRP | 🔵 TEST | silent | 2 | 100 | +1.65R | +0.15R | +3.31R | 0.00R | ✅ |
| P01-BREAKOUT-V2 | 15m | SUI | 🔵 TEST | silent | 1 | 0 | -1.19R | +0.01R | -1.19R | 1.19R | ✅ |
| P01-BREAKOUT-V2 | 15m | XRP | 🔵 TEST | silent | 1 | 0 | -1.19R | -0.01R | -1.19R | 1.19R | ✅ |
| P01-BREAKOUT-V5 | 1h | BTC | 🔵 TEST | silent | 1 | 0 | -1.15R | +0.02R | -1.15R | 1.15R | ✅ |
| P03-FIB-PULLBACK-V2 | 1h | SUI | 🔵 TEST | silent | 1 | 100 | +2.48R | +0.04R | +2.48R | 0.00R | ✅ |
| P04-MACD-SUPERTREND-V2 | 1h | XRP | 🔵 TEST | silent | 1 | 0 | -1.05R | +0.05R | -1.05R | 1.05R | ✅ |
| P04-MACD-SUPERTREND-V4 | 4h | ZEC | 🔵 TEST | silent | 1 | 0 | -1.02R | +0.22R | -1.02R | 1.02R | ✅ |
| P07-SQUEEZE-RETEST-V1 | 4h | ETH | 🔵 TEST | silent | 1 | 100 | +2.48R | +0.09R | +2.48R | 0.00R | ✅ |
| P07-SQUEEZE-RETEST-V2 | 1h | BTC | 🔵 TEST | silent | 1 | 0 | -1.05R | +0.04R | -1.05R | 1.05R | ✅ |
| P07-SQUEEZE-RETEST-V5 | 1h | ZEC | 🔵 TEST | silent | 1 | 0 | -0.49R | +0.02R | -0.49R | 0.49R | ✅ |
| P08-SESSION-BREAKOUT-V2 | 30m | SOL | 🔵 TEST | silent | 1 | 100 | +2.44R | +0.07R | +2.44R | 0.00R | ✅ |
| P08-SESSION-BREAKOUT-V2 | 30m | SUI | 🔵 TEST | silent | 1 | 100 | +2.46R | +0.12R | +2.46R | 0.00R | ✅ |
| P08-SESSION-BREAKOUT-V2 | 30m | XRP | 🔵 TEST | silent | 1 | 100 | +2.44R | +0.06R | +2.44R | 0.00R | ✅ |
| P08-SESSION-BREAKOUT-V3 | 1h | SOL | 🔵 TEST | silent | 1 | 100 | +1.53R | +0.19R | +1.53R | 0.00R | ✅ |
| P08-SESSION-BREAKOUT-V4 | 1h | XRP | 🔵 TEST | silent | 1 | 0 | -1.07R | +0.08R | -1.07R | 1.07R | ✅ |
| P12-LEADER-V1 | 4h | SUI | 🔵 TEST | silent | 1 | 0 | -1.03R | +0.01R | -1.03R | 1.03R | ✅ |

## Equity curve (all stages, R after fees)

| Closed | Running total |
|---|---:|
| 2026-11-21 07:59 | +105.97R |
| 2026-11-21 07:59 | +105.15R |
| 2026-11-21 11:59 | +103.85R |
| 2026-11-21 11:59 | +97.67R |
| 2026-11-21 13:59 | +95.45R |
| 2026-11-21 15:59 | +104.17R |
| 2026-11-21 15:59 | +102.48R |
| 2026-11-21 15:59 | +96.29R |
| 2026-11-21 15:59 | +90.12R |
| 2026-11-22 08:29 | +83.42R |
| 2026-11-22 11:59 | +83.46R |
| 2026-11-22 11:59 | +78.07R |
| 2026-11-22 11:59 | +72.03R |
| 2026-11-22 15:59 | +65.88R |
| 2026-11-23 03:59 | +59.64R |
| 2026-11-23 11:59 | +62.59R |
| 2026-11-23 11:59 | +61.36R |
| 2026-11-23 11:59 | +57.29R |
| 2026-11-23 15:59 | +61.30R |
| 2026-11-24 18:29 | +60.02R |
