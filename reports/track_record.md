# 📈 Live track record

Updated 2026-10-29 23:11 UTC by the hourly scan (engine/track_record.py). Every TEST / PAPER / LIVE setup the hourly scan recorded (entry at the signal close, after fees). 'Your alerts' = the setups that could reach your Telegram (versions of one setup counted once); the silent research records are the other positive program pairs GitHub keeps for the research. The alerts actually sent and your ✅ / ❌ are in the journal review.

| Stage | Closed | Win % | Average | Total | Worst drawdown | Longest losing run |
|---|---:|---:|---:|---:|---:|---:|
| **Your alerts** (could reach your Telegram) | 3 | 0 | -0.99R | -2.97R | 2.97R | 3 |
| Silent research records (never sent to you) | 41 | 20 | -0.59R | -24.30R | 24.30R | 6 |
| 🔵 TEST | 47 | 17 | -0.65R | -30.54R | 30.54R | 7 |
| 🟡 PAPER | 3 | 0 | -1.08R | -3.25R | 3.25R | 3 |
| 🟢 LIVE | 0 | - | - | +0.00R | 0.00R | 0 |
| **All** | 50 | 16 | -0.68R | -33.79R | 33.79R | 10 |

## 🚨 Drift monitor

- nothing paused: every strategy's live results are inside what its backtest calls normal.

Warning signs (no pause yet):
- P01-BREAKOUT-V5@1.0 30m on SUI: 4 losses in a row - in its backtest (35% won) a run that long shows up in 18% of 4-trade periods

## Per strategy and coin (live vs 5-year backtest)

| Strategy | TF | Coin | Stage | Sent to you | Closed | Win % | Live avg | Backtest avg | Total | Worst DD | Check |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P01-BREAKOUT-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 2 | 0 | -0.96R | +0.37R | -1.92R | 1.92R | ✅ |
| P01-BREAKOUT-V1 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.25R | -1.05R | 1.05R | ✅ |
| P01-BREAKOUT-V4 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.22R | -1.05R | 1.05R | ✅ |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.23R | -1.11R | 1.11R | ✅ |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.41R | -1.11R | 1.11R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.51R | -1.08R | 1.08R | ✅ |
| donchian_breakout-VEXIT | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.51R | -1.08R | 1.08R | ✅ |
| donchian_breakout | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.26R | -1.08R | 1.08R | ✅ |
| P01-BREAKOUT-V5 | 30m | SUI | 🔵 TEST | silent | 4 | 0 | -1.01R | +0.01R | -4.05R | 4.05R | ⚠️ watch |
| P03-FIB-PULLBACK-V5 | 1h | SOL | 🔵 TEST | silent | 7 | 29 | -0.35R | +0.03R | -2.42R | 2.46R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | 🔵 TEST | silent | 6 | 17 | -0.56R | +0.01R | -3.37R | 4.58R | ✅ |
| P01-BREAKOUT-V2 | 15m | BTC | 🔵 TEST | silent | 3 | 33 | -0.47R | +0.07R | -1.41R | 2.04R | ✅ |
| P03-FIB-PULLBACK-V5 | 1h | SUI | 🔵 TEST | silent | 3 | 33 | -0.40R | +0.02R | -1.19R | 2.15R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | 🔵 TEST | silent | 3 | 33 | -0.42R | +0.01R | -1.27R | 2.16R | ✅ |
| P01-BREAKOUT-V2 | 1h | BTC | 🔵 TEST | silent | 2 | 0 | -0.96R | +0.11R | -1.92R | 1.92R | ✅ |
| P01-BREAKOUT-V2 | 30m | BTC | 🔵 TEST | silent | 2 | 50 | +0.12R | +0.07R | +0.24R | 0.91R | ✅ |
| P01-BREAKOUT-V2 | 30m | SOL | 🔵 TEST | silent | 2 | 0 | -1.13R | +0.06R | -2.27R | 2.27R | ✅ |
| P01-BREAKOUT-V5 | 1h | ETH | 🔵 TEST | silent | 2 | 0 | -0.74R | +0.01R | -1.49R | 1.49R | ✅ |
| P01-BREAKOUT-V5 | 1h | SUI | 🔵 TEST | silent | 2 | 0 | -0.78R | +0.09R | -1.55R | 1.55R | ✅ |
| P01-BREAKOUT-V2 | 15m | XRP | 🔵 TEST | silent | 1 | 0 | -1.19R | -0.01R | -1.19R | 1.19R | ✅ |
| P01-BREAKOUT-V2 | 1h | SOL | 🔵 TEST | silent | 1 | 0 | -1.08R | +0.03R | -1.08R | 1.08R | ✅ |
| P01-BREAKOUT-V5 | 1h | BTC | 🔵 TEST | silent | 1 | 0 | -1.15R | +0.02R | -1.15R | 1.15R | ✅ |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | 🔵 TEST | silent | 1 | 0 | -1.07R | +0.02R | -1.07R | 1.07R | ✅ |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | 🔵 TEST | silent | 1 | 100 | +0.89R | +0.17R | +0.89R | 0.00R | ✅ |

## Equity curve (all stages, R after fees)

| Closed | Running total |
|---|---:|
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
| 2026-10-27 12:59 | -28.42R |
| 2026-10-27 23:59 | -29.26R |
| 2026-10-29 10:59 | -30.03R |
| 2026-10-29 13:59 | -30.76R |
| 2026-10-29 13:59 | -31.58R |
| 2026-10-29 14:59 | -32.66R |
| 2026-10-29 14:59 | -33.79R |
