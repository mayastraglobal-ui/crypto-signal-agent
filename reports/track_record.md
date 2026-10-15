# 📈 Live track record

Updated 2026-10-15 15:35 UTC by the hourly scan (engine/track_record.py). Every TEST / PAPER / LIVE setup the hourly scan recorded (entry at the signal close, after fees). The alerts actually sent (5m-confirmed) are in the journal review.

| Stage | Closed | Win % | Average | Total | Worst drawdown | Longest losing run |
|---|---:|---:|---:|---:|---:|---:|
| 🔵 TEST | 15 | 13 | -0.70R | -10.58R | 10.58R | 5 |
| 🟡 PAPER | 0 | - | - | +0.00R | 0.00R | 0 |
| 🟢 LIVE | 0 | - | - | +0.00R | 0.00R | 0 |
| **All** | 15 | 13 | -0.70R | -10.58R | 10.58R | 5 |

## 🚨 Drift monitor

- nothing paused: every strategy's live results are inside what its backtest calls normal.

Warning signs (no pause yet):
- P04-MACD-SUPERTREND-V5@1.0 30m on XRP: 4 losses in a row - in its backtest (36% won) a run that long shows up in 16% of 4-trade periods

## Per strategy and coin (live vs 5-year backtest)

| Strategy | TF | Coin | Stage | Closed | Win % | Live avg | Backtest avg | Total | Worst DD | Check |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P04-MACD-SUPERTREND-V5 | 30m | XRP | 🔵 TEST | 4 | 0 | -1.15R | +0.01R | -4.58R | 4.58R | ⚠️ watch |
| P03-FIB-PULLBACK-V5 | 1h | SOL | 🔵 TEST | 6 | 33 | -0.20R | +0.04R | -1.22R | 2.38R | ✅ |
| P01-BREAKOUT-V5 | 1h | ETH | 🔵 TEST | 2 | 0 | -0.74R | +0.01R | -1.49R | 1.49R | ✅ |
| P01-BREAKOUT-V5 | 1h | BTC | 🔵 TEST | 1 | 0 | -1.15R | +0.02R | -1.15R | 1.15R | ✅ |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | 🔵 TEST | 1 | 0 | -1.07R | +0.03R | -1.07R | 1.07R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | 🔵 TEST | 1 | 0 | -1.07R | +0.01R | -1.07R | 1.07R | ✅ |

## Equity curve (all stages, R after fees)

| Closed | Running total |
|---|---:|
| 2026-10-11 14:59 | -1.31R |
| 2026-10-11 15:59 | -2.49R |
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
