# Forward Test Program - backtest results

Updated 2026-11-03 07:11 UTC. Tested tonight: strategies 3, 4, 12, 13; next night: 5, 6, 12, 13.

10 strategies x 4 versions (strategies_program.yaml). Every number includes OKX fees and funding ('after fees'); 'before fees' shows what the rules alone made. 'Test' = the unseen last 30% of each coin's history. A coin counts as positive with >= 5 trades and an average above 0R after fees.

Versions: V1 base (4H) · V2 faster (1H / 30m / 15m) · V3 + daily agrees · V4 trailing ATR exit.

## 1. Breakout (Donchian + volume + ADX)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1323 | 38 | +0.15R | +0.19R | +0.10R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-01 06:46 |
| V2 | 1h | FAILED | 2317 | 32 | -0.03R | +0.03R | +0.04R | BTC, SOL, SUI | 2026-11-01 06:46 |
| V2 | 30m | FAILED | 1465 | 35 | -0.03R | +0.05R | +0.03R | BTC, ETH, SOL, SUI | 2026-11-01 06:46 |
| V2 | 15m | FAILED | 2297 | 34 | -0.07R | +0.04R | -0.02R | BTC | 2026-11-01 06:46 |
| V3 | 4h | BACKTESTING | 416 | 39 | +0.17R | +0.20R | +0.14R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-01 06:46 |
| V4 | 4h | BACKTESTING | 1122 | 39 | +0.16R | +0.21R | +0.12R | BNB, BTC, ETH, SOL, SUI, TRX, XRP | 2026-11-01 06:46 |
| V5 | 1h | FAILED | 4686 | 33 | -0.03R | +0.03R | +0.00R | BTC, ETH, SUI | 2026-11-01 06:46 |
| V5 | 30m | FAILED | 3191 | 33 | -0.09R | -0.01R | -0.10R | SUI | 2026-11-01 06:46 |
| V5 | 15m | FAILED | 4940 | 32 | -0.14R | -0.02R | -0.15R | - | 2026-11-01 06:46 |

## 2. EMA trend pullback (EMA20/50 + RSI + VWAP)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 323 | 31 | -0.04R | +0.00R | -0.15R | ZEC | 2026-11-02 06:44 |
| V2 | 1h | FAILED | 2484 | 31 | -0.10R | -0.03R | -0.09R | - | 2026-11-02 06:44 |
| V2 | 30m | FAILED | 2581 | 29 | -0.15R | -0.06R | -0.14R | - | 2026-11-02 06:44 |
| V2 | 15m | FAILED | 4810 | 28 | -0.21R | -0.08R | -0.21R | - | 2026-11-02 06:44 |
| V3 | 4h | FAILED | 126 | 23 | -0.25R | -0.21R | -0.27R | BNB | 2026-11-02 06:44 |
| V4 | 4h | BACKTESTING | 320 | 35 | +0.07R | +0.13R | +0.03R | BTC, ETH, XRP | 2026-11-02 06:44 |
| V5 | 1h | FAILED | 5223 | 30 | -0.11R | -0.04R | -0.11R | - | 2026-11-02 06:44 |
| V5 | 30m | FAILED | 5604 | 29 | -0.17R | -0.07R | -0.16R | - | 2026-11-02 06:44 |
| V5 | 15m | FAILED | 10468 | 27 | -0.25R | -0.10R | -0.27R | - | 2026-11-02 06:44 |

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
| V1 | 4h | FAILED | 387 | 49 | -0.14R | -0.09R | -0.10R | SOL | 2026-10-29 06:23 |
| V2 | 1h | FAILED | 1442 | 46 | -0.23R | -0.16R | -0.26R | - | 2026-10-29 06:23 |
| V2 | 30m | FAILED | 4290 | 46 | -0.26R | -0.13R | -0.33R | - | 2026-10-29 06:23 |
| V2 | 15m | FAILED | 10573 | 42 | -0.38R | -0.19R | -0.42R | - | 2026-10-29 06:23 |
| V3 | 4h | FAILED | 75 | 52 | -0.13R | -0.08R | +0.12R | BTC, XRP | 2026-10-29 06:23 |
| V4 | 4h | BACKTESTING | 363 | 36 | +0.05R | +0.11R | +0.16R | BNB, BTC, ETH, SOL, XRP | 2026-10-29 06:23 |

## 6. VWAP reversion

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-10-30 06:22 |
| V2 | 1h | FAILED | 84 | 43 | -0.20R | -0.13R | -0.14R | SOL | 2026-10-30 06:22 |
| V2 | 30m | FAILED | 950 | 40 | -0.23R | -0.11R | -0.29R | ZEC | 2026-10-30 06:22 |
| V2 | 15m | FAILED | 3946 | 34 | -0.34R | -0.17R | -0.40R | - | 2026-10-30 06:22 |
| V3 | 4h | BACKTESTING | 0 | 0 | +0.00R | +0.00R | +0.00R | - | 2026-10-30 06:22 |
| V4 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-10-30 06:22 |

## 7. Squeeze breakout & retest

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 795 | 35 | +0.02R | +0.06R | +0.16R | BTC, ETH, SOL, XRP | 2026-10-30 06:22 |
| V2 | 1h | BACKTESTING | 1050 | 35 | +0.02R | +0.08R | +0.02R | BNB, BTC, SOL, XRP | 2026-10-30 06:22 |
| V2 | 30m | FAILED | 848 | 32 | -0.11R | -0.02R | -0.17R | ETH, SOL, SUI | 2026-10-30 06:22 |
| V2 | 15m | FAILED | 1678 | 29 | -0.22R | -0.09R | -0.28R | - | 2026-10-30 06:22 |
| V3 | 4h | BACKTESTING | 249 | 36 | +0.05R | +0.09R | +0.03R | BTC, ETH, SOL, XRP | 2026-10-30 06:22 |
| V4 | 4h | BACKTESTING | 723 | 34 | +0.06R | +0.11R | +0.31R | BNB, BTC, ETH, SOL, XRP | 2026-10-30 06:22 |
| V5 | 1h | FAILED | 2510 | 33 | -0.05R | +0.02R | -0.06R | ZEC | 2026-10-30 06:22 |
| V5 | 30m | FAILED | 1938 | 31 | -0.17R | -0.07R | -0.18R | - | 2026-10-30 06:22 |
| V5 | 15m | FAILED | 3735 | 29 | -0.26R | -0.11R | -0.27R | - | 2026-10-30 06:22 |

## 8. Session open breakout (Asia range -> London / New York)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 1h | FAILED | 1273 | 36 | -0.06R | -0.00R | -0.05R | BTC, ENA, XRP | 2026-10-31 06:13 |
| V2 | 30m | FAILED | 775 | 37 | -0.09R | -0.01R | -0.02R | ENA, SOL, SUI, XRP | 2026-10-31 06:13 |
| V2 | 15m | FAILED | 918 | 34 | -0.20R | -0.07R | -0.15R | ENA, SUI | 2026-10-31 06:13 |
| V3 | 1h | FAILED | 442 | 36 | -0.04R | +0.01R | -0.00R | BNB, ENA, SOL, XRP | 2026-10-31 06:13 |
| V4 | 1h | FAILED | 1223 | 34 | -0.06R | +0.00R | -0.03R | BTC, ENA, XRP | 2026-10-31 06:13 |
| V5 | 30m | FAILED | 1791 | 34 | -0.18R | -0.09R | -0.18R | SUI | 2026-10-31 06:13 |
| V5 | 15m | FAILED | 2084 | 32 | -0.24R | -0.11R | -0.25R | - | 2026-10-31 06:13 |

## 9. Liquidity sweep + structure shift

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 5 | 40 | -0.48R | -0.44R | -1.03R | - | 2026-11-01 06:46 |
| V2 | 1h | BACKTESTING | 15 | 33 | -0.27R | -0.22R | -0.11R | - | 2026-11-01 06:46 |
| V2 | 30m | FAILED | 38 | 37 | -0.01R | +0.07R | +0.08R | SOL, TRX | 2026-11-01 06:46 |
| V2 | 15m | FAILED | 99 | 28 | -0.39R | -0.29R | -0.43R | XRP | 2026-11-01 06:46 |
| V3 | 4h | BACKTESTING | 1 | 0 | -1.02R | -1.00R | -1.02R | - | 2026-11-01 06:46 |
| V4 | 4h | BACKTESTING | 5 | 40 | -0.22R | -0.17R | -1.03R | - | 2026-11-01 06:46 |
| V5 | 1h | FAILED | 45 | 36 | -0.25R | -0.20R | -0.61R | TRX | 2026-11-01 06:46 |
| V5 | 30m | FAILED | 100 | 32 | -0.21R | -0.14R | -0.31R | SOL, TRX | 2026-11-01 06:46 |
| V5 | 15m | FAILED | 218 | 29 | -0.37R | -0.26R | -0.52R | XRP | 2026-11-01 06:46 |

## 10. Crowding fade (funding + open interest)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 3 | 33 | +0.06R | +0.21R | +0.06R | - | 2026-11-01 06:46 |
| V2 | 1h | BACKTESTING | 7 | 71 | +0.41R | +0.49R | +0.41R | - | 2026-11-01 06:46 |
| V2 | 30m | BACKTESTING | 10 | 60 | +0.24R | +0.31R | +0.24R | ZEC | 2026-11-01 06:46 |
| V2 | 15m | BACKTESTING | 11 | 36 | +0.04R | +0.08R | +0.04R | - | 2026-11-01 06:46 |
| V3 | 4h | BACKTESTING | 1 | 100 | +1.97R | +1.99R | +1.97R | - | 2026-11-01 06:46 |
| V4 | 4h | BACKTESTING | 3 | 33 | -0.33R | -0.17R | -0.33R | - | 2026-11-01 06:46 |

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
| C | 4h | FAILED | 2810 | 42 | -0.00R | +0.03R | -0.08R | BTC, SOL, ZEC | 2026-11-03 07:11 |
| V1 | 4h | BACKTESTING | 573 | 44 | +0.11R | +0.14R | +0.21R | ETH, SOL, SUI, XRP, ZEC | 2026-11-03 07:11 |
| V2 | 4h | VALIDATION | 497 | 47 | +0.19R | +0.22R | +0.37R | BNB, ETH, SOL, SUI, XRP, ZEC | 2026-11-03 07:11 |
| V3 | 1h | FAILED | 835 | 35 | -0.03R | +0.01R | -0.03R | XRP, ZEC | 2026-11-03 07:11 |

## 13. Daily Turtle (55-day breakout, ride the trend)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 4h | PAPER_TRADING | 467 | 51 | +0.21R | +0.23R | +0.21R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-03 07:11 |
| V1 | 4h | VALIDATION | 157 | 41 | +1.83R | +1.95R | +1.29R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-03 07:11 |
| V2 | 4h | VALIDATION | 124 | 46 | +2.00R | +2.12R | +1.86R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-03 07:11 |
| V3 | 4h | VALIDATION | 128 | 41 | +1.92R | +2.04R | +1.55R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-03 07:11 |

