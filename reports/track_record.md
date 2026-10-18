# 📈 Live track record

Updated 2026-10-18 15:25 UTC by the hourly scan (engine/track_record.py). Every TEST / PAPER / LIVE setup the hourly scan recorded (entry at the signal close, after fees). 'Your alerts' = the setups that could reach your Telegram (versions of one setup counted once); the silent research records are the other positive program pairs GitHub keeps for the research. The alerts actually sent and your ✅ / ❌ are in the journal review.

| Stage | Closed | Win % | Average | Total | Worst drawdown | Longest losing run |
|---|---:|---:|---:|---:|---:|---:|
| **Your alerts** (could reach your Telegram) | 1 | 0 | -1.05R | -1.05R | 1.05R | 1 |
| Silent research records (never sent to you) | 20 | 15 | -0.70R | -13.95R | 13.95R | 5 |
| 🔵 TEST | 22 | 14 | -0.73R | -16.04R | 16.04R | 6 |
| 🟡 PAPER | 0 | - | - | +0.00R | 0.00R | 0 |
| 🟢 LIVE | 0 | - | - | +0.00R | 0.00R | 0 |
| **All** | 22 | 14 | -0.73R | -16.04R | 16.04R | 6 |

## 🚨 Drift monitor

- nothing paused: every strategy's live results are inside what its backtest calls normal.

Warning signs (no pause yet):
- P04-MACD-SUPERTREND-V5@1.0 30m on XRP: 4 losses in a row - in its backtest (36% won) a run that long shows up in 17% of 4-trade periods

## Per strategy and coin (live vs 5-year backtest)

| Strategy | TF | Coin | Stage | Sent to you | Closed | Win % | Live avg | Backtest avg | Total | Worst DD | Check |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P01-BREAKOUT-V1 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.25R | -1.05R | 1.05R | ✅ |
| P01-BREAKOUT-V4 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.22R | -1.05R | 1.05R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | 🔵 TEST | silent | 4 | 0 | -1.15R | +0.01R | -4.58R | 4.58R | ⚠️ watch |
| P03-FIB-PULLBACK-V5 | 1h | SOL | 🔵 TEST | silent | 6 | 33 | -0.20R | +0.04R | -1.22R | 2.38R | ✅ |
| P03-FIB-PULLBACK-V5 | 1h | SUI | 🔵 TEST | silent | 3 | 33 | -0.40R | +0.01R | -1.19R | 2.15R | ✅ |
| P01-BREAKOUT-V5 | 1h | ETH | 🔵 TEST | silent | 2 | 0 | -0.74R | +0.01R | -1.49R | 1.49R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | 🔵 TEST | silent | 2 | 0 | -1.08R | +0.01R | -2.16R | 2.16R | ✅ |
| P01-BREAKOUT-V5 | 1h | BTC | 🔵 TEST | silent | 1 | 0 | -1.15R | +0.02R | -1.15R | 1.15R | ✅ |
| P01-BREAKOUT-V5 | 30m | SUI | 🔵 TEST | silent | 1 | 0 | -1.09R | +0.02R | -1.09R | 1.09R | ✅ |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | 🔵 TEST | silent | 1 | 0 | -1.07R | +0.02R | -1.07R | 1.07R | ✅ |

## Equity curve (all stages, R after fees)

| Closed | Running total |
|---|---:|
| 2026-10-11 15:59 | -3.69R |
| 2026-10-13 02:59 | -4.84R |
| 2026-10-13 02:59 | -5.94R |
| 2026-10-15 02:59 | -3.52R |
| 2026-10-15 02:59 | -4.61R |
| 2026-10-15 14:29 | -5.68R |
| 2026-10-15 14:59 | -6.07R |
| 2026-10-15 14:59 | -7.12R |
| 2026-10-15 14:59 | -6.24R |
| 2026-10-15 14:59 | -7.33R |
| 2026-10-15 14:59 | -8.40R |
| 2026-10-15 14:59 | -9.49R |
| 2026-10-15 15:29 | -10.58R |
| 2026-10-15 15:59 | -9.62R |
| 2026-10-15 15:59 | -10.67R |
| 2026-10-15 15:59 | -11.72R |
| 2026-10-15 15:59 | -12.75R |
| 2026-10-18 01:29 | -13.84R |
| 2026-10-18 01:29 | -14.93R |
| 2026-10-18 09:59 | -16.04R |
