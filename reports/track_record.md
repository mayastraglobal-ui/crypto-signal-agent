# 📈 Live track record

Updated 2026-10-26 22:35 UTC by the hourly scan (engine/track_record.py). Every TEST / PAPER / LIVE setup the hourly scan recorded (entry at the signal close, after fees). 'Your alerts' = the setups that could reach your Telegram (versions of one setup counted once); the silent research records are the other positive program pairs GitHub keeps for the research. The alerts actually sent and your ✅ / ❌ are in the journal review.

| Stage | Closed | Win % | Average | Total | Worst drawdown | Longest losing run |
|---|---:|---:|---:|---:|---:|---:|
| **Your alerts** (could reach your Telegram) | 2 | 0 | -1.06R | -2.13R | 2.13R | 2 |
| Silent research records (never sent to you) | 35 | 23 | -0.53R | -18.58R | 20.98R | 6 |
| 🔵 TEST | 40 | 20 | -0.60R | -23.98R | 26.38R | 7 |
| 🟡 PAPER | 3 | 0 | -1.08R | -3.25R | 3.25R | 3 |
| 🟢 LIVE | 0 | - | - | +0.00R | 0.00R | 0 |
| **All** | 43 | 19 | -0.63R | -27.23R | 29.63R | 10 |

## 🚨 Drift monitor

- nothing paused: every strategy's live results are inside what its backtest calls normal.

Warning signs (no pause yet):
- P01-BREAKOUT-V5@1.0 30m on SUI: 3 losses in a row - in its backtest (35% won) a run that long shows up in 27% of 3-trade periods

## Per strategy and coin (live vs 5-year backtest)

| Strategy | TF | Coin | Stage | Sent to you | Closed | Win % | Live avg | Backtest avg | Total | Worst DD | Check |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P01-BREAKOUT-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.08R | +0.37R | -1.08R | 1.08R | ✅ |
| P01-BREAKOUT-V1 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.25R | -1.05R | 1.05R | ✅ |
| P01-BREAKOUT-V4 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.22R | -1.05R | 1.05R | ✅ |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.23R | -1.11R | 1.11R | ✅ |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.41R | -1.11R | 1.11R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.51R | -1.08R | 1.08R | ✅ |
| donchian_breakout-VEXIT | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.51R | -1.08R | 1.08R | ✅ |
| donchian_breakout | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.26R | -1.08R | 1.08R | ✅ |
| P01-BREAKOUT-V5 | 30m | SUI | 🔵 TEST | silent | 3 | 0 | -1.10R | +0.01R | -3.29R | 3.29R | ⚠️ watch |
| P03-FIB-PULLBACK-V5 | 1h | SOL | 🔵 TEST | silent | 6 | 33 | -0.20R | +0.04R | -1.22R | 2.38R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | 🔵 TEST | silent | 6 | 17 | -0.56R | +0.01R | -3.37R | 4.58R | ✅ |
| P01-BREAKOUT-V2 | 15m | BTC | 🔵 TEST | silent | 3 | 33 | -0.47R | +0.07R | -1.41R | 2.04R | ✅ |
| P03-FIB-PULLBACK-V5 | 1h | SUI | 🔵 TEST | silent | 3 | 33 | -0.40R | +0.01R | -1.19R | 2.15R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | 🔵 TEST | silent | 3 | 33 | -0.42R | +0.00R | -1.27R | 2.16R | ✅ |
| P01-BREAKOUT-V2 | 1h | BTC | 🔵 TEST | silent | 2 | 0 | -0.96R | +0.11R | -1.92R | 1.92R | ✅ |
| P01-BREAKOUT-V2 | 30m | BTC | 🔵 TEST | silent | 2 | 50 | +0.12R | +0.07R | +0.24R | 0.91R | ✅ |
| P01-BREAKOUT-V5 | 1h | ETH | 🔵 TEST | silent | 2 | 0 | -0.74R | +0.01R | -1.49R | 1.49R | ✅ |
| P01-BREAKOUT-V2 | 15m | XRP | 🔵 TEST | silent | 1 | 0 | -1.19R | -0.01R | -1.19R | 1.19R | ✅ |
| P01-BREAKOUT-V2 | 30m | SOL | 🔵 TEST | silent | 1 | 0 | -1.14R | +0.06R | -1.14R | 1.14R | ✅ |
| P01-BREAKOUT-V5 | 1h | BTC | 🔵 TEST | silent | 1 | 0 | -1.15R | +0.02R | -1.15R | 1.15R | ✅ |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | 🔵 TEST | silent | 1 | 0 | -1.07R | +0.02R | -1.07R | 1.07R | ✅ |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | 🔵 TEST | silent | 1 | 100 | +0.89R | +0.15R | +0.89R | 0.00R | ✅ |

## Equity curve (all stages, R after fees)

| Closed | Running total |
|---|---:|
| 2026-10-18 21:29 | -14.83R |
| 2026-10-18 21:59 | -15.97R |
| 2026-10-18 21:59 | -17.06R |
| 2026-10-20 13:59 | -18.25R |
| 2026-10-21 13:44 | -19.61R |
| 2026-10-21 19:14 | -20.29R |
| 2026-10-21 23:59 | -19.14R |
| 2026-10-21 23:59 | -20.05R |
| 2026-10-22 01:59 | -20.80R |
| 2026-10-22 01:59 | -21.96R |
| 2026-10-22 03:59 | -23.05R |
| 2026-10-22 03:59 | -24.13R |
| 2026-10-22 03:59 | -25.22R |
| 2026-10-22 03:59 | -26.30R |
| 2026-10-22 03:59 | -27.41R |
| 2026-10-22 03:59 | -28.52R |
| 2026-10-23 02:59 | -29.63R |
| 2026-10-25 11:44 | -29.01R |
| 2026-10-25 16:59 | -28.12R |
| 2026-10-25 16:59 | -27.23R |
