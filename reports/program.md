# Forward Test Program - backtest results

Updated 2026-11-07 06:31 UTC. Tested tonight: strategies 2, 10, 12, 13; next night: 3, 11, 12, 13.

10 strategies x 4 versions (strategies_program.yaml). Every number includes OKX fees and funding ('after fees'); 'before fees' shows what the rules alone made. 'Test' = the unseen last 30% of each coin's history. A coin counts as positive with >= 5 trades and an average above 0R after fees.

Versions: V1 base (4H) · V2 faster (1H / 30m / 15m) · V3 + daily agrees · V4 trailing ATR exit.

## 1. Breakout (Donchian + volume + ADX)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1265 | 39 | +0.17R | +0.20R | +0.14R | BNB, BTC, ETH, SOL, SUI, UNI, XRP | 2026-11-06 07:20 |
| V2 | 1h | FAILED | 2200 | 32 | -0.03R | +0.02R | +0.06R | BTC, SOL, SUI | 2026-11-06 07:20 |
| V2 | 30m | FAILED | 1441 | 35 | -0.01R | +0.05R | +0.06R | BTC, ETH, SOL, SUI, UNI | 2026-11-06 07:20 |
| V2 | 15m | FAILED | 2236 | 33 | -0.06R | +0.02R | -0.01R | BTC | 2026-11-06 07:20 |
| V3 | 4h | BACKTESTING | 383 | 41 | +0.21R | +0.24R | +0.23R | BNB, BTC, ETH, SOL, SUI, UNI, XRP | 2026-11-06 07:20 |
| V4 | 4h | BACKTESTING | 1079 | 39 | +0.17R | +0.21R | +0.13R | BNB, BTC, ETH, SOL, SUI, UNI, XRP | 2026-11-06 07:20 |
| V5 | 1h | FAILED | 4511 | 33 | -0.03R | +0.02R | +0.01R | BTC, ETH, SUI | 2026-11-06 07:20 |
| V5 | 30m | FAILED | 3162 | 33 | -0.07R | -0.00R | -0.06R | SUI, UNI | 2026-11-06 07:20 |
| V5 | 15m | FAILED | 4893 | 32 | -0.12R | -0.02R | -0.12R | - | 2026-11-06 07:20 |

## 2. EMA trend pullback (EMA20/50 + RSI + VWAP)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 323 | 31 | -0.04R | +0.00R | -0.15R | ZEC | 2026-11-07 06:31 |
| V2 | 1h | FAILED | 2485 | 31 | -0.09R | -0.03R | -0.09R | - | 2026-11-07 06:31 |
| V2 | 30m | FAILED | 2581 | 29 | -0.15R | -0.05R | -0.14R | - | 2026-11-07 06:31 |
| V2 | 15m | FAILED | 4814 | 28 | -0.21R | -0.08R | -0.21R | - | 2026-11-07 06:31 |
| V3 | 4h | FAILED | 126 | 23 | -0.25R | -0.21R | -0.27R | BNB | 2026-11-07 06:31 |
| V4 | 4h | BACKTESTING | 321 | 35 | +0.07R | +0.12R | +0.02R | BTC, ETH, XRP | 2026-11-07 06:31 |
| V5 | 1h | FAILED | 5228 | 30 | -0.11R | -0.04R | -0.11R | - | 2026-11-07 06:31 |
| V5 | 30m | FAILED | 5622 | 29 | -0.17R | -0.07R | -0.17R | - | 2026-11-07 06:31 |
| V5 | 15m | FAILED | 10504 | 27 | -0.25R | -0.10R | -0.27R | - | 2026-11-07 06:31 |

## 3. Fibonacci pullback (50-61.8% of the last swing)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 257 | 35 | -0.07R | -0.02R | -0.06R | XRP, ZEC | 2026-11-03 07:11 |
| V2 | 1h | FAILED | 2406 | 34 | -0.09R | -0.02R | -0.11R | - | 2026-11-03 07:11 |
| V2 | 30m | FAILED | 2803 | 35 | -0.14R | -0.03R | -0.08R | - | 2026-11-03 07:11 |
| V2 | 15m | FAILED | 4736 | 34 | -0.23R | -0.08R | -0.17R | - | 2026-11-03 07:11 |
| V3 | 4h | FAILED | 87 | 31 | -0.14R | -0.10R | -0.17R | XRP, ZEC | 2026-11-03 07:11 |
| V4 | 4h | FAILED | 254 | 32 | -0.02R | +0.03R | -0.11R | XRP, ZEC | 2026-11-03 07:11 |
| V5 | 1h | FAILED | 5149 | 34 | -0.12R | -0.05R | -0.12R | SOL, SUI | 2026-11-03 07:11 |
| V5 | 30m | FAILED | 6225 | 34 | -0.19R | -0.07R | -0.13R | - | 2026-11-03 07:11 |
| V5 | 15m | FAILED | 10455 | 33 | -0.28R | -0.11R | -0.25R | - | 2026-11-03 07:11 |

## 4. Trend momentum (MACD + Supertrend)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 386 | 36 | +0.11R | +0.14R | -0.20R | BNB, ETH, SOL, SUI, ZEC | 2026-11-03 07:11 |
| V2 | 1h | FAILED | 1204 | 33 | -0.04R | +0.01R | +0.01R | BNB, SOL, XRP | 2026-11-03 07:11 |
| V2 | 30m | FAILED | 1448 | 34 | -0.04R | +0.03R | +0.06R | SUI, XRP | 2026-11-03 07:11 |
| V2 | 15m | FAILED | 2286 | 34 | -0.08R | +0.02R | -0.01R | ETH | 2026-11-03 07:11 |
| V3 | 4h | BACKTESTING | 151 | 38 | +0.19R | +0.22R | +0.00R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-03 07:11 |
| V4 | 4h | FAILED | 375 | 37 | +0.12R | +0.17R | -0.21R | BNB, ETH, SOL, SUI, ZEC | 2026-11-03 07:11 |
| V5 | 1h | FAILED | 2409 | 32 | -0.11R | -0.05R | -0.08R | - | 2026-11-03 07:11 |
| V5 | 30m | FAILED | 3368 | 33 | -0.11R | -0.03R | +0.00R | SUI, XRP | 2026-11-03 07:11 |
| V5 | 15m | FAILED | 5035 | 33 | -0.13R | -0.02R | -0.07R | - | 2026-11-03 07:11 |

## 5. Range reversal (RSI + Bollinger)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 390 | 49 | -0.13R | -0.09R | -0.09R | - | 2026-11-04 06:56 |
| V2 | 1h | FAILED | 1445 | 46 | -0.23R | -0.16R | -0.26R | - | 2026-11-04 06:56 |
| V2 | 30m | FAILED | 4297 | 46 | -0.26R | -0.13R | -0.34R | - | 2026-11-04 06:56 |
| V2 | 15m | FAILED | 10587 | 42 | -0.38R | -0.19R | -0.43R | - | 2026-11-04 06:56 |
| V3 | 4h | FAILED | 75 | 52 | -0.13R | -0.08R | +0.12R | BTC, XRP | 2026-11-04 06:56 |
| V4 | 4h | BACKTESTING | 366 | 36 | +0.05R | +0.11R | +0.15R | BNB, BTC, ETH, SOL, XRP | 2026-11-04 06:56 |

## 6. VWAP reversion

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-11-04 06:56 |
| V2 | 1h | FAILED | 84 | 43 | -0.20R | -0.13R | -0.14R | SOL | 2026-11-04 06:56 |
| V2 | 30m | FAILED | 957 | 40 | -0.23R | -0.12R | -0.30R | ZEC | 2026-11-04 06:56 |
| V2 | 15m | FAILED | 3954 | 34 | -0.34R | -0.17R | -0.40R | - | 2026-11-04 06:56 |
| V3 | 4h | BACKTESTING | 0 | 0 | +0.00R | +0.00R | +0.00R | - | 2026-11-04 06:56 |
| V4 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-11-04 06:56 |

## 7. Squeeze breakout & retest

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 875 | 34 | +0.01R | +0.05R | +0.16R | BTC, ETH, SOL, XRP | 2026-11-05 07:18 |
| V2 | 1h | FAILED | 1180 | 34 | -0.01R | +0.05R | -0.00R | BNB, BTC, SOL, XRP | 2026-11-05 07:18 |
| V2 | 30m | FAILED | 1001 | 31 | -0.12R | -0.04R | -0.13R | ETH, SUI | 2026-11-05 07:18 |
| V2 | 15m | FAILED | 1988 | 29 | -0.23R | -0.10R | -0.25R | - | 2026-11-05 07:18 |
| V3 | 4h | BACKTESTING | 267 | 36 | +0.05R | +0.09R | +0.04R | BTC, ETH, SOL, XRP | 2026-11-05 07:18 |
| V4 | 4h | BACKTESTING | 795 | 35 | +0.06R | +0.10R | +0.32R | BNB, BTC, ETH, SOL, UNI, XRP | 2026-11-05 07:18 |
| V5 | 1h | FAILED | 2827 | 32 | -0.06R | +0.01R | -0.07R | ZEC | 2026-11-05 07:18 |
| V5 | 30m | FAILED | 2272 | 31 | -0.16R | -0.07R | -0.14R | - | 2026-11-05 07:18 |
| V5 | 15m | FAILED | 4364 | 29 | -0.25R | -0.11R | -0.26R | - | 2026-11-05 07:18 |

## 8. Session open breakout (Asia range -> London / New York)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 1h | FAILED | 1335 | 35 | -0.07R | -0.01R | -0.07R | BTC, UNI, XRP | 2026-11-05 07:18 |
| V2 | 30m | FAILED | 788 | 36 | -0.11R | -0.02R | +0.00R | SOL, SUI, UNI, XRP | 2026-11-05 07:18 |
| V2 | 15m | FAILED | 945 | 33 | -0.20R | -0.08R | -0.13R | SUI | 2026-11-05 07:18 |
| V3 | 1h | FAILED | 451 | 34 | -0.07R | -0.01R | -0.03R | BNB, SOL, XRP | 2026-11-05 07:18 |
| V4 | 1h | FAILED | 1283 | 33 | -0.07R | -0.01R | -0.04R | BTC, UNI, XRP | 2026-11-05 07:18 |
| V5 | 30m | FAILED | 1814 | 34 | -0.18R | -0.08R | -0.13R | SUI | 2026-11-05 07:18 |
| V5 | 15m | FAILED | 2131 | 32 | -0.25R | -0.11R | -0.21R | - | 2026-11-05 07:18 |

## 9. Liquidity sweep + structure shift

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 5 | 40 | -0.18R | -0.14R | -0.16R | - | 2026-11-06 07:20 |
| V2 | 1h | BACKTESTING | 13 | 46 | +0.12R | +0.16R | +0.61R | - | 2026-11-06 07:20 |
| V2 | 30m | FAILED | 37 | 35 | -0.04R | +0.01R | -0.04R | SOL, UNI | 2026-11-06 07:20 |
| V2 | 15m | FAILED | 104 | 33 | -0.25R | -0.16R | -0.40R | UNI, XRP | 2026-11-06 07:20 |
| V3 | 4h | BACKTESTING | 1 | 0 | -1.02R | -1.00R | -1.02R | - | 2026-11-06 07:20 |
| V4 | 4h | BACKTESTING | 5 | 40 | -0.01R | +0.03R | -0.19R | - | 2026-11-06 07:20 |
| V5 | 1h | FAILED | 44 | 36 | -0.18R | -0.13R | -0.45R | UNI | 2026-11-06 07:20 |
| V5 | 30m | FAILED | 105 | 30 | -0.28R | -0.22R | -0.37R | SOL | 2026-11-06 07:20 |
| V5 | 15m | FAILED | 230 | 31 | -0.28R | -0.19R | -0.48R | XRP | 2026-11-06 07:20 |

## 10. Crowding fade (funding + open interest)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 2 | 100 | +1.15R | +1.19R | +1.15R | - | 2026-11-07 06:31 |
| V2 | 1h | BACKTESTING | 3 | 100 | +1.11R | +1.14R | +1.11R | - | 2026-11-07 06:31 |
| V2 | 30m | BACKTESTING | 7 | 57 | +0.24R | +0.27R | +0.24R | ZEC | 2026-11-07 06:31 |
| V2 | 15m | BACKTESTING | 8 | 38 | -0.05R | -0.01R | -0.05R | - | 2026-11-07 06:31 |
| V3 | 4h | BACKTESTING | 1 | 100 | +1.97R | +1.99R | +1.97R | - | 2026-11-07 06:31 |
| V4 | 4h | BACKTESTING | 2 | 50 | +0.26R | +0.30R | +0.26R | - | 2026-11-07 06:31 |

## 11. Early momentum (market-wide break, early steps only)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 30m | FAILED | 11837 | 33 | -0.19R | -0.08R | -0.20R | - | 2026-11-02 06:44 |
| V1 | 30m | FAILED | 4271 | 32 | -0.22R | -0.11R | -0.23R | - | 2026-11-02 06:44 |
| V2 | 30m | FAILED | 1143 | 30 | -0.26R | -0.14R | -0.23R | - | 2026-11-02 06:44 |
| V3 | 1h | FAILED | 2544 | 32 | -0.13R | -0.05R | -0.19R | - | 2026-11-02 06:44 |
| V4 | 30m | FAILED | 3994 | 30 | -0.27R | -0.14R | -0.22R | - | 2026-11-02 06:44 |

## 12. Follow the leader (buy the strongest coin when BTC jumps)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 4h | FAILED | 2817 | 42 | -0.01R | +0.03R | -0.09R | BTC, SOL, ZEC | 2026-11-07 06:31 |
| V1 | 4h | BACKTESTING | 574 | 44 | +0.11R | +0.14R | +0.20R | ETH, SOL, SUI, XRP, ZEC | 2026-11-07 06:31 |
| V2 | 4h | VALIDATION | 498 | 47 | +0.19R | +0.22R | +0.35R | BNB, ETH, SOL, SUI, XRP, ZEC | 2026-11-07 06:31 |
| V3 | 1h | FAILED | 837 | 35 | -0.03R | +0.01R | -0.05R | XRP, ZEC | 2026-11-07 06:31 |

## 13. Daily Turtle (55-day breakout, ride the trend)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 4h | PAPER_TRADING | 467 | 51 | +0.21R | +0.23R | +0.21R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-07 06:31 |
| V1 | 4h | VALIDATION | 157 | 41 | +1.83R | +1.95R | +1.29R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-07 06:31 |
| V2 | 4h | VALIDATION | 124 | 46 | +2.00R | +2.12R | +1.86R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-07 06:31 |
| V3 | 4h | VALIDATION | 128 | 41 | +1.92R | +2.04R | +1.55R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-07 06:31 |

