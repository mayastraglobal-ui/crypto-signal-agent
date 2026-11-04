# 📈 Live track record

Updated 2026-11-04 07:58 UTC by the hourly scan (engine/track_record.py). Every TEST / PAPER / LIVE setup the hourly scan recorded (entry at the signal close, after fees). 'Your alerts' = the setups that could reach your Telegram (versions of one setup counted once); the silent research records are the other positive program pairs GitHub keeps for the research. The alerts actually sent and your ✅ / ❌ are in the journal review.

| Stage | Closed | Win % | Average | Total | Worst drawdown | Longest losing run |
|---|---:|---:|---:|---:|---:|---:|
| **Your alerts** (could reach your Telegram) | 4 | 0 | -1.01R | -4.02R | 4.02R | 4 |
| Silent research records (never sent to you) | 51 | 16 | -0.66R | -33.87R | 33.87R | 16 |
| 🔵 TEST | 58 | 14 | -0.71R | -41.17R | 41.17R | 18 |
| 🟡 PAPER | 3 | 0 | -1.08R | -3.25R | 3.25R | 3 |
| 🟢 LIVE | 0 | - | - | +0.00R | 0.00R | 0 |
| **All** | 61 | 13 | -0.73R | -44.42R | 44.42R | 18 |

## 🚨 Drift monitor

- nothing paused: every strategy's live results are inside what its backtest calls normal.

Warning signs (no pause yet):
- P01-BREAKOUT-V5@1.0 30m on SUI: 5 losses in a row - in its backtest (35% won) a run that long shows up in 12% of 5-trade periods
- P01-BREAKOUT-V5@1.0 1h on SUI: 4 losses in a row - in its backtest (34% won) a run that long shows up in 19% of 4-trade periods
- P03-FIB-PULLBACK-V5@1.0 1h on SUI: 3 losses in a row - in its backtest (38% won) a run that long shows up in 43% of 4-trade periods
- P01-BREAKOUT-V2@1.0 30m on SOL: 3 losses in a row - in its backtest (37% won) a run that long shows up in 25% of 3-trade periods

## Per strategy and coin (live vs 5-year backtest)

| Strategy | TF | Coin | Stage | Sent to you | Closed | Win % | Live avg | Backtest avg | Total | Worst DD | Check |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P01-BREAKOUT-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 2 | 0 | -0.96R | +0.36R | -1.92R | 1.92R | ✅ |
| P01-BREAKOUT-V1 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.25R | -1.05R | 1.05R | ✅ |
| P01-BREAKOUT-V4 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.22R | -1.05R | 1.05R | ✅ |
| P05-RANGE-REVERSAL-V4 | 4h | SOL | 🔵 TEST | ✅ yes | 1 | 0 | -1.06R | +0.24R | -1.06R | 1.06R | ✅ |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.23R | -1.11R | 1.11R | ✅ |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.41R | -1.11R | 1.11R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.51R | -1.08R | 1.08R | ✅ |
| donchian_breakout-VEXIT | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.51R | -1.08R | 1.08R | ✅ |
| donchian_breakout | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.26R | -1.08R | 1.08R | ✅ |
| P01-BREAKOUT-V5 | 30m | SUI | 🔵 TEST | silent | 5 | 0 | -0.94R | +0.00R | -4.69R | 4.69R | ⚠️ watch |
| P01-BREAKOUT-V5 | 1h | SUI | 🔵 TEST | silent | 4 | 0 | -0.91R | +0.08R | -3.62R | 3.62R | ⚠️ watch |
| P03-FIB-PULLBACK-V5 | 1h | SUI | 🔵 TEST | silent | 4 | 25 | -0.57R | +0.02R | -2.28R | 3.24R | ⚠️ watch |
| P01-BREAKOUT-V2 | 30m | SOL | 🔵 TEST | silent | 3 | 0 | -1.16R | +0.06R | -3.47R | 3.47R | ⚠️ watch |
| P03-FIB-PULLBACK-V5 | 1h | SOL | 🔵 TEST | silent | 7 | 29 | -0.35R | +0.04R | -2.42R | 2.46R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | 🔵 TEST | silent | 6 | 17 | -0.56R | +0.02R | -3.37R | 4.58R | ✅ |
| P01-BREAKOUT-V2 | 15m | BTC | 🔵 TEST | silent | 3 | 33 | -0.47R | +0.07R | -1.41R | 2.04R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | 🔵 TEST | silent | 3 | 33 | -0.42R | +0.01R | -1.27R | 2.16R | ✅ |
| P01-BREAKOUT-V2 | 1h | BTC | 🔵 TEST | silent | 2 | 0 | -0.96R | +0.11R | -1.92R | 1.92R | ✅ |
| P01-BREAKOUT-V2 | 30m | BTC | 🔵 TEST | silent | 2 | 50 | +0.12R | +0.07R | +0.24R | 0.91R | ✅ |
| P01-BREAKOUT-V5 | 1h | ETH | 🔵 TEST | silent | 2 | 0 | -0.74R | +0.01R | -1.49R | 1.49R | ✅ |
| P01-BREAKOUT-V2 | 15m | XRP | 🔵 TEST | silent | 1 | 0 | -1.19R | -0.01R | -1.19R | 1.19R | ✅ |
| P01-BREAKOUT-V2 | 1h | SOL | 🔵 TEST | silent | 1 | 0 | -1.08R | +0.03R | -1.08R | 1.08R | ✅ |
| P01-BREAKOUT-V2 | 30m | SUI | 🔵 TEST | silent | 1 | 0 | -1.09R | +0.09R | -1.09R | 1.09R | ✅ |
| P01-BREAKOUT-V5 | 1h | BTC | 🔵 TEST | silent | 1 | 0 | -1.15R | +0.02R | -1.15R | 1.15R | ✅ |
| P04-MACD-SUPERTREND-V1 | 4h | ZEC | 🔵 TEST | silent | 1 | 0 | -1.02R | +0.14R | -1.02R | 1.02R | ✅ |
| P04-MACD-SUPERTREND-V2 | 15m | ETH | 🔵 TEST | silent | 1 | 0 | -0.96R | +0.00R | -0.96R | 0.96R | ✅ |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | 🔵 TEST | silent | 1 | 0 | -1.07R | +0.02R | -1.07R | 1.07R | ✅ |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | 🔵 TEST | silent | 1 | 100 | +0.89R | +0.16R | +0.89R | 0.00R | ✅ |
| P04-MACD-SUPERTREND-V4 | 4h | ZEC | 🔵 TEST | silent | 1 | 0 | -1.02R | +0.25R | -1.02R | 1.02R | ✅ |
| P07-SQUEEZE-RETEST-V5 | 1h | ZEC | 🔵 TEST | silent | 1 | 0 | -0.49R | +0.03R | -0.49R | 0.49R | ✅ |

## Equity curve (all stages, R after fees)

| Closed | Running total |
|---|---:|
| 2026-10-25 16:59 | -28.12R |
| 2026-10-25 16:59 | -27.23R |
| 2026-10-27 12:59 | -28.42R |
| 2026-10-27 23:59 | -29.26R |
| 2026-10-29 10:59 | -30.03R |
| 2026-10-29 13:59 | -30.76R |
| 2026-10-29 13:59 | -31.58R |
| 2026-10-29 14:59 | -32.66R |
| 2026-10-29 14:59 | -33.79R |
| 2026-10-29 23:59 | -34.81R |
| 2026-10-29 23:59 | -35.83R |
| 2026-10-30 04:29 | -36.46R |
| 2026-10-30 05:59 | -37.49R |
| 2026-10-30 15:14 | -38.45R |
| 2026-10-31 00:59 | -39.50R |
| 2026-11-01 23:59 | -40.55R |
| 2026-11-02 00:29 | -41.75R |
| 2026-11-03 10:59 | -42.24R |
| 2026-11-03 12:59 | -43.33R |
| 2026-11-04 04:29 | -44.42R |
