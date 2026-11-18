# 📈 Live track record

Updated 2026-11-18 22:11 UTC by the hourly scan (engine/track_record.py). Every TEST / PAPER / LIVE setup the hourly scan recorded (entry at the signal close, after fees). 'Your alerts' = the setups that could reach your Telegram (versions of one setup counted once); the silent research records are the other positive program pairs GitHub keeps for the research. The alerts actually sent and your ✅ / ❌ are in the journal review.

| Stage | Closed | Win % | Average | Total | Worst drawdown | Longest losing run |
|---|---:|---:|---:|---:|---:|---:|
| **Your alerts** (could reach your Telegram) | 52 | 48 | +0.28R | +14.80R | 10.35R | 7 |
| Silent research records (never sent to you) | 113 | 31 | -0.10R | -11.53R | 38.60R | 17 |
| 🔵 TEST | 167 | 34 | +0.03R | +4.63R | 47.91R | 20 |
| 🟡 PAPER | 63 | 64 | +0.63R | +39.87R | 11.26R | 8 |
| 🟢 LIVE | 0 | - | - | +0.00R | 0.00R | 0 |
| **All** | 230 | 42 | +0.19R | +44.51R | 59.17R | 20 |

## 🚨 Drift monitor

- nothing paused: every strategy's live results are inside what its backtest calls normal.

Warning signs (no pause yet):
- TRD-H4-BREAKOUT-S3@1.0 1h on BTC: 3 losses in a row - in its backtest (46% won) a run that long shows up in 84% of 13-trade periods
- P01-BREAKOUT-V5@1.0 1h on SUI: 5 losses in a row - in its backtest (34% won) a run that long shows up in 13% of 5-trade periods
- P01-BREAKOUT-V5@1.0 30m on SUI: 5 losses in a row - in its backtest (35% won) a run that long shows up in 11% of 5-trade periods
- P01-BREAKOUT-V2@1.0 30m on ETH: 3 losses in a row - in its backtest (39% won) a run that long shows up in 40% of 4-trade periods
- P01-BREAKOUT-V2@1.0 1h on SOL: 3 losses in a row - in its backtest (34% won) a run that long shows up in 28% of 3-trade periods

## Per strategy and coin (live vs 5-year backtest)

| Strategy | TF | Coin | Stage | Sent to you | Closed | Win % | Live avg | Backtest avg | Total | Worst DD | Check |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| TRD-H4-BREAKOUT-S3 | 1h | BTC | 🔵 TEST | ✅ yes | 13 | 54 | +0.72R | +0.35R | +9.35R | 3.17R | ⚠️ watch |
| TRD-H4-BREAKOUT-S3 | 1h | XRP | 🔵 TEST | ✅ yes | 10 | 30 | -0.14R | +0.30R | -1.39R | 4.20R | ✅ |
| donchian_breakout-VEXIT | 4h | XRP | 🟡 PAPER | ✅ yes | 10 | 70 | +0.96R | +0.13R | +9.57R | 1.03R | ✅ |
| P01-BREAKOUT-V3 | 4h | XRP | 🔵 TEST | ✅ yes | 8 | 62 | +1.17R | +0.27R | +9.39R | 1.02R | ✅ |
| TRD-H4-BREAKOUT-S3 | 1h | SOL | 🔵 TEST | ✅ yes | 7 | 29 | -0.25R | +0.17R | -1.78R | 2.15R | ✅ |
| donchian_breakout-VEXIT | 4h | SOL | 🟡 PAPER | ✅ yes | 7 | 43 | -0.05R | +0.22R | -0.37R | 2.08R | ✅ |
| donchian_breakout | 4h | SOL | 🟡 PAPER | ✅ yes | 7 | 57 | -0.16R | +0.21R | -1.10R | 2.08R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | XRP | 🟡 PAPER | ✅ yes | 6 | 83 | +1.50R | +0.23R | +9.03R | 1.03R | ✅ |
| donchian_breakout | 4h | BTC | 🟡 PAPER | ✅ yes | 5 | 80 | +0.85R | +0.27R | +4.24R | 1.08R | ✅ |
| P01-BREAKOUT-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 4 | 50 | +0.75R | +0.38R | +3.00R | 1.92R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | BTC | 🟡 PAPER | ✅ yes | 4 | 75 | +1.57R | +0.53R | +6.28R | 1.08R | ✅ |
| donchian_breakout-VEXIT | 4h | BTC | 🟡 PAPER | ✅ yes | 4 | 75 | +1.57R | +0.52R | +6.28R | 1.08R | ✅ |
| donchian_breakout | 4h | ETH | 🟡 PAPER | ✅ yes | 4 | 75 | +0.47R | +0.19R | +1.86R | 1.05R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | SOL | 🟡 PAPER | ✅ yes | 3 | 33 | -0.58R | +0.19R | -1.75R | 2.08R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | SOL | 🟡 PAPER | ✅ yes | 3 | 33 | +0.12R | +0.29R | +0.37R | 2.08R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | XRP | 🟡 PAPER | ✅ yes | 3 | 100 | +1.38R | +0.12R | +4.14R | 0.00R | ✅ |
| P01-BREAKOUT-V1 | 4h | SOL | 🔵 TEST | ✅ yes | 2 | 50 | -0.09R | +0.31R | -0.18R | 0.65R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | BTC | 🟡 PAPER | ✅ yes | 2 | 100 | +2.45R | +0.45R | +4.90R | 0.00R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | SOL | 🟡 PAPER | ✅ yes | 2 | 50 | -0.22R | +0.22R | -0.44R | 0.78R | ✅ |
| P01-BREAKOUT-V1 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.24R | -1.05R | 1.05R | ✅ |
| P01-BREAKOUT-V4 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.21R | -1.05R | 1.05R | ✅ |
| P01-BREAKOUT-V4 | 4h | SOL | 🔵 TEST | ✅ yes | 1 | 0 | -1.03R | +0.30R | -1.03R | 1.03R | ✅ |
| P02-EMA-PULLBACK-V4 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 100 | +3.77R | +0.21R | +3.77R | 0.00R | ✅ |
| P05-RANGE-REVERSAL-V4 | 4h | SOL | 🔵 TEST | ✅ yes | 1 | 0 | -1.06R | +0.24R | -1.06R | 1.06R | ✅ |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.23R | -1.11R | 1.11R | ✅ |
| P07-SQUEEZE-RETEST-V1 | 4h | SOL | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.13R | -1.05R | 1.05R | ✅ |
| P07-SQUEEZE-RETEST-V3 | 4h | XRP | 🔵 TEST | ✅ yes | 1 | 100 | +2.47R | +0.18R | +2.47R | 0.00R | ✅ |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.41R | -1.11R | 1.11R | ✅ |
| P12-LEADER-V1 | 4h | ZEC | 🔵 TEST | ✅ yes | 1 | 0 | -1.02R | +0.41R | -1.02R | 1.02R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | ETH | 🟡 PAPER | ✅ yes | 1 | 0 | -1.05R | +0.38R | -1.05R | 1.05R | ✅ |
| donchian_breakout-VEXIT-S4 | 4h | ETH | 🟡 PAPER | ✅ yes | 1 | 0 | -1.05R | +0.42R | -1.05R | 1.05R | ✅ |
| donchian_breakout-VEXIT | 4h | ETH | 🟡 PAPER | ✅ yes | 1 | 0 | -1.05R | +0.32R | -1.05R | 1.05R | ✅ |
| P01-BREAKOUT-V5 | 1h | SUI | 🔵 TEST | silent | 5 | 0 | -0.81R | +0.08R | -4.02R | 4.02R | ⚠️ watch |
| P01-BREAKOUT-V5 | 30m | SUI | 🔵 TEST | silent | 5 | 0 | -0.94R | +0.01R | -4.69R | 4.69R | ⚠️ watch |
| P01-BREAKOUT-V2 | 30m | ETH | 🔵 TEST | silent | 4 | 25 | +0.07R | +0.12R | +0.28R | 2.16R | ⚠️ watch |
| P01-BREAKOUT-V2 | 1h | SOL | 🔵 TEST | silent | 3 | 0 | -1.05R | +0.02R | -3.15R | 3.15R | ⚠️ watch |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | 🔵 TEST | silent | 11 | 27 | -0.22R | +0.01R | -2.39R | 5.69R | ✅ |
| P03-FIB-PULLBACK-V5 | 1h | SOL | 🔵 TEST | silent | 10 | 40 | +0.13R | +0.04R | +1.30R | 3.63R | ✅ |
| P01-BREAKOUT-V2 | 30m | SOL | 🔵 TEST | silent | 9 | 22 | -0.44R | +0.07R | -3.97R | 4.88R | ✅ |
| P01-BREAKOUT-V2 | 30m | BTC | 🔵 TEST | silent | 8 | 50 | +0.64R | +0.09R | +5.13R | 1.14R | ✅ |
| P01-BREAKOUT-V2 | 1h | BTC | 🔵 TEST | silent | 7 | 43 | +0.14R | +0.11R | +0.98R | 1.92R | ✅ |
| TRD-H4-BREAKOUT-S3 | 1h | ETH | 🔵 TEST | silent | 7 | 29 | -0.04R | +0.06R | -0.30R | 3.17R | ✅ |
| P03-FIB-PULLBACK-V5 | 1h | SUI | 🔵 TEST | silent | 6 | 33 | -0.15R | +0.03R | -0.90R | 4.31R | ✅ |
| P01-BREAKOUT-V2 | 15m | BTC | 🔵 TEST | silent | 3 | 33 | -0.47R | +0.08R | -1.41R | 2.04R | ✅ |
| P04-MACD-SUPERTREND-V2 | 15m | ETH | 🔵 TEST | silent | 3 | 33 | +0.13R | +0.01R | +0.38R | 1.06R | ✅ |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | 🔵 TEST | silent | 3 | 33 | +0.10R | +0.03R | +0.31R | 1.07R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | 🔵 TEST | silent | 3 | 33 | -0.42R | +0.01R | -1.27R | 2.16R | ✅ |
| P08-SESSION-BREAKOUT-V4 | 1h | BTC | 🔵 TEST | silent | 3 | 33 | -0.07R | +0.04R | -0.21R | 1.12R | ✅ |
| P01-BREAKOUT-V5 | 1h | ETH | 🔵 TEST | silent | 2 | 0 | -0.74R | +0.01R | -1.49R | 1.49R | ✅ |
| P04-MACD-SUPERTREND-V1 | 4h | ZEC | 🔵 TEST | silent | 2 | 0 | -1.02R | +0.14R | -2.04R | 2.04R | ✅ |
| P04-MACD-SUPERTREND-V2 | 30m | XRP | 🔵 TEST | silent | 2 | 100 | +1.65R | +0.14R | +3.31R | 0.00R | ✅ |
| P07-SQUEEZE-RETEST-V2 | 30m | ETH | 🔵 TEST | silent | 2 | 50 | -0.28R | +0.07R | -0.57R | 1.12R | ✅ |
| P08-SESSION-BREAKOUT-V1 | 1h | BTC | 🔵 TEST | silent | 2 | 0 | -1.00R | +0.04R | -2.00R | 2.00R | ✅ |
| P01-BREAKOUT-V2 | 15m | XRP | 🔵 TEST | silent | 1 | 0 | -1.19R | -0.01R | -1.19R | 1.19R | ✅ |
| P01-BREAKOUT-V2 | 30m | SUI | 🔵 TEST | silent | 1 | 0 | -1.09R | +0.12R | -1.09R | 1.09R | ✅ |
| P01-BREAKOUT-V5 | 1h | BTC | 🔵 TEST | silent | 1 | 0 | -1.15R | +0.02R | -1.15R | 1.15R | ✅ |
| P04-MACD-SUPERTREND-V1 | 4h | ETH | 🔵 TEST | silent | 1 | 100 | +2.48R | +0.15R | +2.48R | 0.00R | ✅ |
| P04-MACD-SUPERTREND-V2 | 1h | XRP | 🔵 TEST | silent | 1 | 0 | -1.05R | +0.03R | -1.05R | 1.05R | ✅ |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | 🔵 TEST | silent | 1 | 100 | +0.89R | +0.17R | +0.89R | 0.00R | ✅ |
| P04-MACD-SUPERTREND-V4 | 4h | ZEC | 🔵 TEST | silent | 1 | 0 | -1.02R | +0.25R | -1.02R | 1.02R | ✅ |
| P07-SQUEEZE-RETEST-V1 | 4h | ETH | 🔵 TEST | silent | 1 | 100 | +2.48R | +0.09R | +2.48R | 0.00R | ✅ |
| P07-SQUEEZE-RETEST-V5 | 1h | ZEC | 🔵 TEST | silent | 1 | 0 | -0.49R | +0.02R | -0.49R | 0.49R | ✅ |
| P08-SESSION-BREAKOUT-V2 | 30m | SOL | 🔵 TEST | silent | 1 | 100 | +2.44R | +0.07R | +2.44R | 0.00R | ✅ |
| P08-SESSION-BREAKOUT-V2 | 30m | XRP | 🔵 TEST | silent | 1 | 100 | +2.44R | +0.06R | +2.44R | 0.00R | ✅ |
| P08-SESSION-BREAKOUT-V3 | 1h | SOL | 🔵 TEST | silent | 1 | 100 | +1.53R | +0.19R | +1.53R | 0.00R | ✅ |
| P08-SESSION-BREAKOUT-V4 | 1h | XRP | 🔵 TEST | silent | 1 | 0 | -1.07R | +0.08R | -1.07R | 1.07R | ✅ |

## Equity curve (all stages, R after fees)

| Closed | Running total |
|---|---:|
| 2026-11-15 02:59 | +35.77R |
| 2026-11-15 02:59 | +32.64R |
| 2026-11-15 03:59 | +32.44R |
| 2026-11-15 03:59 | +39.83R |
| 2026-11-15 07:59 | +39.04R |
| 2026-11-15 09:59 | +37.95R |
| 2026-11-15 09:59 | +34.80R |
| 2026-11-15 11:59 | +39.31R |
| 2026-11-15 12:59 | +37.60R |
| 2026-11-17 11:59 | +39.80R |
| 2026-11-17 11:59 | +40.94R |
| 2026-11-17 11:59 | +41.07R |
| 2026-11-17 11:59 | +38.73R |
| 2026-11-17 23:59 | +41.12R |
| 2026-11-17 23:59 | +45.49R |
| 2026-11-17 23:59 | +49.07R |
| 2026-11-17 23:59 | +50.13R |
| 2026-11-17 23:59 | +48.76R |
| 2026-11-17 23:59 | +45.60R |
| 2026-11-17 23:59 | +44.51R |
