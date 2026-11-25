# Forward Test Program - backtest results

Updated 2026-11-25 09:03 UTC. Tested tonight: strategies 1, 3, 5, 6, 12, 13; next night: 1, 2, 3, 7, 12, 13.

10 strategies x 4 versions (strategies_program.yaml). Every number includes OKX fees and funding ('after fees'); 'before fees' shows what the rules alone made. 'Test' = the unseen last 30% of each coin's history. A coin counts as positive with >= 5 trades and an average above 0R after fees.

Versions: V1 base (4H) · V2 faster (1H / 30m / 15m) · V3 + daily agrees · V4 trailing ATR exit.

## 1. Breakout (Donchian + volume + ADX)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1152 | 40 | +0.19R | +0.23R | +0.16R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-25 09:03 |
| V2 | 1h | FAILED | 2016 | 33 | -0.01R | +0.04R | +0.08R | BTC, SOL, SUI | 2026-11-25 09:03 |
| V2 | 30m | PAPER_TRADING | 1303 | 36 | +0.01R | +0.07R | +0.10R | BTC, ETH, SOL, SUI | 2026-11-25 09:03 |
| V2 | 15m | FAILED | 2039 | 34 | -0.05R | +0.04R | -0.00R | BTC, SUI | 2026-11-25 09:03 |
| V3 | 4h | VALIDATION | 361 | 41 | +0.23R | +0.26R | +0.28R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-25 09:03 |
| V4 | 4h | BACKTESTING | 977 | 40 | +0.19R | +0.23R | +0.14R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-25 09:03 |
| V5 | 1h | FAILED | 4095 | 33 | -0.02R | +0.03R | +0.01R | BTC, ETH, SUI | 2026-11-25 09:03 |
| V5 | 30m | FAILED | 2864 | 33 | -0.07R | +0.00R | -0.05R | SUI | 2026-11-25 09:03 |
| V5 | 15m | FAILED | 4441 | 32 | -0.12R | -0.02R | -0.13R | - | 2026-11-25 09:03 |

## 2. EMA trend pullback (EMA20/50 + RSI + VWAP)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 324 | 31 | -0.04R | +0.01R | -0.15R | ZEC | 2026-11-22 07:23 |
| V2 | 1h | FAILED | 2511 | 31 | -0.09R | -0.02R | -0.06R | - | 2026-11-22 07:23 |
| V2 | 30m | FAILED | 2640 | 29 | -0.14R | -0.05R | -0.14R | - | 2026-11-22 07:23 |
| V2 | 15m | FAILED | 4943 | 28 | -0.21R | -0.08R | -0.21R | - | 2026-11-22 07:23 |
| V3 | 4h | FAILED | 126 | 23 | -0.25R | -0.21R | -0.31R | BNB | 2026-11-22 07:23 |
| V4 | 4h | BACKTESTING | 322 | 35 | +0.08R | +0.13R | +0.02R | BTC, ETH, XRP | 2026-11-22 07:23 |
| V5 | 1h | FAILED | 5261 | 30 | -0.11R | -0.04R | -0.09R | - | 2026-11-22 07:23 |
| V5 | 30m | FAILED | 5688 | 29 | -0.17R | -0.07R | -0.17R | - | 2026-11-22 07:23 |
| V5 | 15m | FAILED | 10647 | 27 | -0.25R | -0.10R | -0.26R | - | 2026-11-22 07:23 |

## 3. Fibonacci pullback (50-61.8% of the last swing)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 262 | 36 | -0.03R | +0.02R | +0.08R | SOL, XRP, ZEC | 2026-11-25 09:03 |
| V2 | 1h | FAILED | 2440 | 35 | -0.09R | -0.02R | -0.09R | SUI | 2026-11-25 09:03 |
| V2 | 30m | FAILED | 2839 | 35 | -0.13R | -0.02R | -0.06R | - | 2026-11-25 09:03 |
| V2 | 15m | FAILED | 4811 | 34 | -0.23R | -0.08R | -0.17R | - | 2026-11-25 09:03 |
| V3 | 4h | FAILED | 90 | 33 | -0.08R | -0.04R | +0.04R | XRP, ZEC | 2026-11-25 09:03 |
| V4 | 4h | BACKTESTING | 259 | 33 | +0.04R | +0.09R | +0.08R | SOL, XRP, ZEC | 2026-11-25 09:03 |
| V5 | 1h | PAPER_TRADING | 5198 | 34 | -0.12R | -0.05R | -0.12R | SOL, SUI | 2026-11-25 09:03 |
| V5 | 30m | FAILED | 6255 | 34 | -0.18R | -0.06R | -0.12R | - | 2026-11-25 09:03 |
| V5 | 15m | FAILED | 10531 | 33 | -0.28R | -0.11R | -0.24R | - | 2026-11-25 09:03 |

## 4. Trend momentum (MACD + Supertrend)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 395 | 36 | +0.13R | +0.17R | -0.16R | BNB, ETH, SOL, SUI, ZEC | 2026-11-24 10:14 |
| V2 | 1h | FAILED | 1223 | 34 | -0.02R | +0.03R | +0.05R | BNB, BTC, SOL, XRP | 2026-11-24 10:14 |
| V2 | 30m | FAILED | 1468 | 35 | -0.03R | +0.04R | +0.12R | SUI, XRP | 2026-11-24 10:14 |
| V2 | 15m | FAILED | 2337 | 35 | -0.05R | +0.05R | +0.03R | ETH, XRP | 2026-11-24 10:14 |
| V3 | 4h | BACKTESTING | 156 | 40 | +0.23R | +0.26R | +0.04R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-24 10:14 |
| V4 | 4h | FAILED | 384 | 38 | +0.14R | +0.18R | -0.20R | BNB, BTC, ETH, SOL, SUI, ZEC | 2026-11-24 10:14 |
| V5 | 1h | FAILED | 2432 | 32 | -0.10R | -0.04R | -0.06R | - | 2026-11-24 10:14 |
| V5 | 30m | FAILED | 3381 | 33 | -0.10R | -0.02R | +0.02R | SUI, XRP | 2026-11-24 10:14 |
| V5 | 15m | FAILED | 5074 | 33 | -0.12R | -0.01R | -0.04R | - | 2026-11-24 10:14 |

## 5. Range reversal (RSI + Bollinger)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 392 | 49 | -0.12R | -0.08R | -0.05R | - | 2026-11-25 09:03 |
| V2 | 1h | FAILED | 1450 | 46 | -0.23R | -0.15R | -0.26R | - | 2026-11-25 09:03 |
| V2 | 30m | FAILED | 4285 | 46 | -0.26R | -0.13R | -0.34R | - | 2026-11-25 09:03 |
| V2 | 15m | FAILED | 10583 | 42 | -0.38R | -0.19R | -0.43R | - | 2026-11-25 09:03 |
| V3 | 4h | FAILED | 77 | 53 | -0.08R | -0.04R | +0.22R | BTC, XRP | 2026-11-25 09:03 |
| V4 | 4h | BACKTESTING | 369 | 36 | +0.07R | +0.13R | +0.22R | BNB, BTC, ETH, SOL, XRP | 2026-11-25 09:03 |

## 6. VWAP reversion

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-11-25 09:03 |
| V2 | 1h | FAILED | 84 | 43 | -0.20R | -0.13R | -0.14R | SOL | 2026-11-25 09:03 |
| V2 | 30m | FAILED | 960 | 41 | -0.22R | -0.10R | -0.27R | SUI, ZEC | 2026-11-25 09:03 |
| V2 | 15m | FAILED | 3981 | 35 | -0.33R | -0.16R | -0.39R | - | 2026-11-25 09:03 |
| V3 | 4h | BACKTESTING | 0 | 0 | +0.00R | +0.00R | +0.00R | - | 2026-11-25 09:03 |
| V4 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-11-25 09:03 |

## 7. Squeeze breakout & retest

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 805 | 35 | +0.04R | +0.07R | +0.19R | BNB, BTC, ETH, SOL, XRP | 2026-11-21 07:39 |
| V2 | 1h | BACKTESTING | 1063 | 34 | +0.01R | +0.07R | +0.00R | BNB, BTC, SOL, XRP | 2026-11-21 07:39 |
| V2 | 30m | FAILED | 870 | 32 | -0.11R | -0.02R | -0.16R | ETH, SUI | 2026-11-21 07:39 |
| V2 | 15m | FAILED | 1725 | 30 | -0.21R | -0.08R | -0.26R | - | 2026-11-21 07:39 |
| V3 | 4h | BACKTESTING | 255 | 36 | +0.07R | +0.10R | +0.06R | BNB, BTC, ETH, SOL, XRP | 2026-11-21 07:39 |
| V4 | 4h | BACKTESTING | 730 | 35 | +0.07R | +0.12R | +0.31R | BNB, BTC, ETH, SOL, XRP | 2026-11-21 07:39 |
| V5 | 1h | FAILED | 2529 | 32 | -0.05R | +0.02R | -0.07R | ZEC | 2026-11-21 07:39 |
| V5 | 30m | FAILED | 1960 | 31 | -0.17R | -0.07R | -0.18R | - | 2026-11-21 07:39 |
| V5 | 15m | FAILED | 3781 | 29 | -0.25R | -0.11R | -0.26R | - | 2026-11-21 07:39 |

## 8. Session open breakout (Asia range -> London / New York)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 1h | FAILED | 1230 | 36 | -0.06R | +0.00R | -0.01R | BNB, BTC, XRP | 2026-11-22 07:23 |
| V2 | 30m | FAILED | 720 | 36 | -0.10R | -0.01R | +0.02R | SOL, SUI, XRP | 2026-11-22 07:23 |
| V2 | 15m | FAILED | 856 | 33 | -0.20R | -0.07R | -0.10R | SUI | 2026-11-22 07:23 |
| V3 | 1h | FAILED | 431 | 36 | -0.02R | +0.04R | +0.07R | BNB, SOL, SUI, XRP | 2026-11-22 07:23 |
| V4 | 1h | FAILED | 1184 | 34 | -0.07R | -0.00R | +0.00R | BNB, BTC, XRP | 2026-11-22 07:23 |
| V5 | 30m | FAILED | 1648 | 34 | -0.18R | -0.08R | -0.14R | SUI | 2026-11-22 07:23 |
| V5 | 15m | FAILED | 1918 | 32 | -0.25R | -0.11R | -0.22R | - | 2026-11-22 07:23 |

## 9. Liquidity sweep + structure shift

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 5 | 40 | -0.18R | -0.14R | +0.27R | - | 2026-11-23 08:07 |
| V2 | 1h | BACKTESTING | 11 | 36 | -0.31R | -0.27R | +0.15R | - | 2026-11-23 08:07 |
| V2 | 30m | FAILED | 30 | 37 | -0.07R | -0.00R | +0.04R | SOL | 2026-11-23 08:07 |
| V2 | 15m | FAILED | 87 | 31 | -0.28R | -0.19R | -0.34R | XRP | 2026-11-23 08:07 |
| V3 | 4h | BACKTESTING | 1 | 0 | -1.02R | -1.00R | +0.00R | - | 2026-11-23 08:07 |
| V4 | 4h | BACKTESTING | 5 | 40 | -0.01R | +0.03R | +0.22R | - | 2026-11-23 08:07 |
| V5 | 1h | FAILED | 39 | 36 | -0.25R | -0.20R | -0.44R | XRP | 2026-11-23 08:07 |
| V5 | 30m | FAILED | 89 | 29 | -0.29R | -0.22R | -0.36R | SOL | 2026-11-23 08:07 |
| V5 | 15m | FAILED | 199 | 30 | -0.30R | -0.20R | -0.46R | XRP | 2026-11-23 08:07 |

## 10. Crowding fade (funding + open interest)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 3 | 67 | +0.42R | +0.45R | +0.42R | - | 2026-11-23 08:07 |
| V2 | 1h | BACKTESTING | 3 | 100 | +1.11R | +1.14R | +1.11R | - | 2026-11-23 08:07 |
| V2 | 30m | BACKTESTING | 10 | 50 | +0.19R | +0.23R | +0.19R | ZEC | 2026-11-23 08:07 |
| V2 | 15m | BACKTESTING | 11 | 27 | -0.27R | -0.23R | -0.27R | - | 2026-11-23 08:07 |
| V3 | 4h | BACKTESTING | 1 | 100 | +1.97R | +1.99R | +1.97R | - | 2026-11-23 08:07 |
| V4 | 4h | BACKTESTING | 3 | 33 | -0.17R | -0.14R | -0.17R | - | 2026-11-23 08:07 |

## 11. Early momentum (market-wide break, early steps only)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 30m | FAILED | 11979 | 33 | -0.19R | -0.07R | -0.19R | - | 2026-11-24 10:14 |
| V1 | 30m | FAILED | 4342 | 32 | -0.22R | -0.10R | -0.21R | - | 2026-11-24 10:14 |
| V2 | 30m | FAILED | 1160 | 30 | -0.25R | -0.14R | -0.22R | - | 2026-11-24 10:14 |
| V3 | 1h | FAILED | 2554 | 32 | -0.14R | -0.06R | -0.20R | - | 2026-11-24 10:14 |
| V4 | 30m | FAILED | 4025 | 31 | -0.27R | -0.14R | -0.22R | - | 2026-11-24 10:14 |

## 12. Follow the leader (buy the strongest coin when BTC jumps)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 4h | FAILED | 2824 | 42 | -0.00R | +0.03R | -0.09R | BTC, SOL, ZEC | 2026-11-25 09:03 |
| V1 | 4h | BACKTESTING | 576 | 44 | +0.10R | +0.13R | +0.19R | ETH, SOL, SUI, XRP, ZEC | 2026-11-25 09:03 |
| V2 | 4h | VALIDATION | 498 | 47 | +0.19R | +0.22R | +0.38R | BNB, ETH, SOL, SUI, XRP, ZEC | 2026-11-25 09:03 |
| V3 | 1h | FAILED | 839 | 35 | -0.03R | +0.01R | -0.04R | XRP, ZEC | 2026-11-25 09:03 |

## 13. Daily Turtle (55-day breakout, ride the trend)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 4h | PAPER_TRADING | 467 | 51 | +0.21R | +0.23R | +0.20R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-25 09:03 |
| V1 | 4h | VALIDATION | 157 | 41 | +1.83R | +1.95R | +1.31R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-25 09:03 |
| V2 | 4h | VALIDATION | 124 | 46 | +2.00R | +2.12R | +1.92R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-25 09:03 |
| V3 | 4h | VALIDATION | 128 | 41 | +1.92R | +2.04R | +1.58R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-25 09:03 |

