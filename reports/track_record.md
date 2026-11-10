# 📈 Live track record

Updated 2026-11-10 19:58 UTC by the hourly scan (engine/track_record.py). Every TEST / PAPER / LIVE setup the hourly scan recorded (entry at the signal close, after fees). 'Your alerts' = the setups that could reach your Telegram (versions of one setup counted once); the silent research records are the other positive program pairs GitHub keeps for the research. The alerts actually sent and your ✅ / ❌ are in the journal review.

| Stage | Closed | Win % | Average | Total | Worst drawdown | Longest losing run |
|---|---:|---:|---:|---:|---:|---:|
| **Your alerts** (could reach your Telegram) | 9 | 11 | -0.64R | -5.72R | 7.15R | 7 |
| Silent research records (never sent to you) | 65 | 22 | -0.51R | -33.10R | 38.60R | 17 |
| 🔵 TEST | 77 | 20 | -0.55R | -42.09R | 46.92R | 20 |
| 🟡 PAPER | 3 | 0 | -1.08R | -3.25R | 3.25R | 3 |
| 🟢 LIVE | 0 | - | - | +0.00R | 0.00R | 0 |
| **All** | 80 | 19 | -0.57R | -45.34R | 50.17R | 20 |

## 🚨 Drift monitor

- nothing paused: every strategy's live results are inside what its backtest calls normal.

Warning signs (no pause yet):
- P01-BREAKOUT-V5@1.0 1h on SUI: 5 losses in a row - in its backtest (34% won) a run that long shows up in 13% of 5-trade periods
- P01-BREAKOUT-V5@1.0 30m on SUI: 5 losses in a row - in its backtest (35% won) a run that long shows up in 12% of 5-trade periods
- P01-BREAKOUT-V2@1.0 30m on SOL: 4 losses in a row - in its backtest (36% won) a run that long shows up in 16% of 4-trade periods
- P03-FIB-PULLBACK-V5@1.0 1h on SUI: 3 losses in a row - in its backtest (38% won) a run that long shows up in 43% of 4-trade periods
- TRD-H4-BREAKOUT-S3@1.0 1h on XRP: 3 losses in a row - in its backtest (44% won) a run that long shows up in 17% of 3-trade periods

## Per strategy and coin (live vs 5-year backtest)

| Strategy | TF | Coin | Stage | Sent to you | Closed | Win % | Live avg | Backtest avg | Total | Worst DD | Check |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| TRD-H4-BREAKOUT-S3 | 1h | XRP | 🔵 TEST | ✅ yes | 3 | 0 | -1.05R | +0.28R | -3.14R | 3.14R | ⚠️ watch |
| P01-BREAKOUT-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 2 | 0 | -0.96R | +0.36R | -1.92R | 1.92R | ✅ |
| P01-BREAKOUT-V1 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.25R | -1.05R | 1.05R | ✅ |
| P01-BREAKOUT-V4 | 4h | ETH | 🔵 TEST | ✅ yes | 1 | 0 | -1.05R | +0.22R | -1.05R | 1.05R | ✅ |
| P05-RANGE-REVERSAL-V4 | 4h | SOL | 🔵 TEST | ✅ yes | 1 | 0 | -1.06R | +0.24R | -1.06R | 1.06R | ✅ |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.23R | -1.11R | 1.11R | ✅ |
| P07-SQUEEZE-RETEST-V3 | 4h | XRP | 🔵 TEST | ✅ yes | 1 | 100 | +2.47R | +0.18R | +2.47R | 0.00R | ✅ |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | 🔵 TEST | ✅ yes | 1 | 0 | -1.11R | +0.41R | -1.11R | 1.11R | ✅ |
| P12-LEADER-V1 | 4h | ZEC | 🔵 TEST | ✅ yes | 1 | 0 | -1.02R | +0.41R | -1.02R | 1.02R | ✅ |
| donchian_breakout-VEXIT-FDISP | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.51R | -1.08R | 1.08R | ✅ |
| donchian_breakout-VEXIT | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.51R | -1.08R | 1.08R | ✅ |
| donchian_breakout | 4h | BTC | 🟡 PAPER | ✅ yes | 1 | 0 | -1.08R | +0.26R | -1.08R | 1.08R | ✅ |
| P01-BREAKOUT-V5 | 1h | SUI | 🔵 TEST | silent | 5 | 0 | -0.81R | +0.08R | -4.02R | 4.02R | ⚠️ watch |
| P01-BREAKOUT-V5 | 30m | SUI | 🔵 TEST | silent | 5 | 0 | -0.94R | +0.00R | -4.69R | 4.69R | ⚠️ watch |
| P01-BREAKOUT-V2 | 30m | SOL | 🔵 TEST | silent | 4 | 0 | -1.18R | +0.05R | -4.71R | 4.71R | ⚠️ watch |
| P03-FIB-PULLBACK-V5 | 1h | SUI | 🔵 TEST | silent | 4 | 25 | -0.57R | +0.01R | -2.28R | 3.24R | ⚠️ watch |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | 🔵 TEST | silent | 10 | 20 | -0.48R | +0.01R | -4.84R | 5.69R | ✅ |
| P03-FIB-PULLBACK-V5 | 1h | SOL | 🔵 TEST | silent | 9 | 33 | -0.13R | +0.04R | -1.16R | 3.63R | ✅ |
| P01-BREAKOUT-V2 | 15m | BTC | 🔵 TEST | silent | 3 | 33 | -0.47R | +0.06R | -1.41R | 2.04R | ✅ |
| P01-BREAKOUT-V2 | 1h | BTC | 🔵 TEST | silent | 3 | 33 | -0.61R | +0.11R | -1.82R | 1.92R | ✅ |
| P01-BREAKOUT-V2 | 30m | BTC | 🔵 TEST | silent | 3 | 33 | +0.00R | +0.07R | +0.00R | 1.14R | ✅ |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | 🔵 TEST | silent | 3 | 33 | -0.42R | +0.01R | -1.27R | 2.16R | ✅ |
| P01-BREAKOUT-V5 | 1h | ETH | 🔵 TEST | silent | 2 | 0 | -0.74R | +0.01R | -1.49R | 1.49R | ✅ |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | 🔵 TEST | silent | 2 | 50 | +0.69R | +0.03R | +1.38R | 1.07R | ✅ |
| P01-BREAKOUT-V2 | 15m | XRP | 🔵 TEST | silent | 1 | 0 | -1.19R | -0.01R | -1.19R | 1.19R | ✅ |
| P01-BREAKOUT-V2 | 1h | SOL | 🔵 TEST | silent | 1 | 0 | -1.08R | +0.02R | -1.08R | 1.08R | ✅ |
| P01-BREAKOUT-V2 | 30m | SUI | 🔵 TEST | silent | 1 | 0 | -1.09R | +0.08R | -1.09R | 1.09R | ✅ |
| P01-BREAKOUT-V5 | 1h | BTC | 🔵 TEST | silent | 1 | 0 | -1.15R | +0.02R | -1.15R | 1.15R | ✅ |
| P04-MACD-SUPERTREND-V1 | 4h | ZEC | 🔵 TEST | silent | 1 | 0 | -1.02R | +0.14R | -1.02R | 1.02R | ✅ |
| P04-MACD-SUPERTREND-V2 | 15m | ETH | 🔵 TEST | silent | 1 | 0 | -0.96R | +0.00R | -0.96R | 0.96R | ✅ |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | 🔵 TEST | silent | 1 | 100 | +0.89R | +0.17R | +0.89R | 0.00R | ✅ |
| P04-MACD-SUPERTREND-V2 | 30m | XRP | 🔵 TEST | silent | 1 | 100 | +0.85R | +0.14R | +0.85R | 0.00R | ✅ |
| P04-MACD-SUPERTREND-V4 | 4h | ZEC | 🔵 TEST | silent | 1 | 0 | -1.02R | +0.25R | -1.02R | 1.02R | ✅ |
| P07-SQUEEZE-RETEST-V2 | 30m | ETH | 🔵 TEST | silent | 1 | 100 | +0.55R | +0.07R | +0.55R | 0.00R | ✅ |
| P07-SQUEEZE-RETEST-V5 | 1h | ZEC | 🔵 TEST | silent | 1 | 0 | -0.49R | +0.03R | -0.49R | 0.49R | ✅ |
| P08-SESSION-BREAKOUT-V4 | 1h | XRP | 🔵 TEST | silent | 1 | 0 | -1.07R | +0.07R | -1.07R | 1.07R | ✅ |

## Equity curve (all stages, R after fees)

| Closed | Running total |
|---|---:|
| 2026-11-04 04:29 | -44.42R |
| 2026-11-05 15:59 | -45.44R |
| 2026-11-06 09:29 | -45.68R |
| 2026-11-06 09:29 | -45.13R |
| 2026-11-06 09:29 | -46.23R |
| 2026-11-06 11:59 | -46.63R |
| 2026-11-07 08:29 | -47.02R |
| 2026-11-07 08:29 | -47.85R |
| 2026-11-07 23:59 | -49.10R |
| 2026-11-08 03:59 | -49.00R |
| 2026-11-08 18:59 | -50.17R |
| 2026-11-08 21:29 | -49.32R |
| 2026-11-08 21:29 | -48.47R |
| 2026-11-08 21:59 | -46.04R |
| 2026-11-08 21:59 | -43.60R |
| 2026-11-09 12:59 | -44.65R |
| 2026-11-09 12:59 | -45.70R |
| 2026-11-09 12:59 | -46.77R |
| 2026-11-10 15:59 | -44.30R |
| 2026-11-10 18:59 | -45.34R |
