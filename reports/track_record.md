# 📈 Live track record

Updated 2026-10-14 02:16 UTC by the hourly scan (engine/track_record.py). Every TEST / PAPER / LIVE setup the hourly scan recorded (entry at the signal close, after fees). The alerts actually sent (5m-confirmed) are in the journal review.

| Stage | Closed | Win % | Average | Total | Worst drawdown | Longest losing run |
|---|---:|---:|---:|---:|---:|---:|
| 🔵 TEST | 5 | 0 | -1.19R | -5.94R | 5.94R | 5 |
| 🟡 PAPER | 0 | - | - | +0.00R | 0.00R | 0 |
| 🟢 LIVE | 0 | - | - | +0.00R | 0.00R | 0 |
| **All** | 5 | 0 | -1.19R | -5.94R | 5.94R | 5 |

## 🚨 Drift monitor

- nothing paused: every strategy's live results are inside what its backtest calls normal.

## Per strategy and coin (live vs 5-year backtest)

| Strategy | TF | Coin | Stage | Closed | Win % | Live avg | Backtest avg | Total | Worst DD | Check |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P03-FIB-PULLBACK-V5 | 1h | SOL | 🔵 TEST | 2 | 0 | -1.19R | +0.04R | -2.38R | 2.38R | ✅ |
| P01-BREAKOUT-V5 | 1h | BTC | 🔵 TEST | 1 | 0 | -1.15R | +0.02R | -1.15R | 1.15R | ✅ |
| P01-BREAKOUT-V5 | 1h | ETH | 🔵 TEST | 1 | 0 | -1.10R | +0.01R | -1.10R | 1.10R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | 🔵 TEST | 1 | 0 | -1.31R | +0.01R | -1.31R | 1.31R | ✅ |

## Equity curve (all stages, R after fees)

| Closed | Running total |
|---|---:|
| 2026-10-11 14:59 | -1.31R |
| 2026-10-11 15:59 | -2.49R |
| 2026-10-11 15:59 | -3.69R |
| 2026-10-13 02:59 | -4.84R |
| 2026-10-13 02:59 | -5.94R |
