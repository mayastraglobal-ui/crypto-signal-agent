# Forward Test Program - backtest results

Updated 2026-10-25 01:12 UTC. Tested tonight: strategies 8, 9, 12; next night: 1, 10, 12.

10 strategies x 4 versions (strategies_program.yaml). Every number includes OKX fees and funding ('after fees'); 'before fees' shows what the rules alone made. 'Test' = the unseen last 30% of each coin's history. A coin counts as positive with >= 5 trades and an average above 0R after fees.

Versions: V1 base (4H) · V2 faster (1H / 30m / 15m) · V3 + daily agrees · V4 trailing ATR exit.

## 1. Breakout (Donchian + volume + ADX)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1133 | 39 | +0.18R | +0.21R | +0.14R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-10-21 01:16 |
| V2 | 1h | FAILED | 1975 | 32 | -0.01R | +0.03R | +0.06R | BTC, SOL, SUI | 2026-10-21 01:16 |
| V2 | 30m | FAILED | 1258 | 35 | -0.01R | +0.05R | +0.07R | BTC, ETH, SOL, SUI | 2026-10-21 01:16 |
| V2 | 15m | FAILED | 1952 | 34 | -0.06R | +0.03R | +0.00R | BTC | 2026-10-21 01:16 |
| V3 | 4h | BACKTESTING | 353 | 40 | +0.21R | +0.24R | +0.24R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-10-21 01:16 |
| V4 | 4h | BACKTESTING | 962 | 39 | +0.18R | +0.22R | +0.13R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-10-21 01:16 |
| V5 | 1h | FAILED | 4035 | 33 | -0.02R | +0.03R | +0.02R | BTC, ETH, SUI | 2026-10-21 01:16 |
| V5 | 30m | FAILED | 2795 | 33 | -0.08R | -0.01R | -0.07R | SUI | 2026-10-21 01:16 |
| V5 | 15m | FAILED | 4314 | 32 | -0.12R | -0.02R | -0.12R | - | 2026-10-21 01:16 |

## 2. EMA trend pullback (EMA20/50 + RSI + VWAP)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 320 | 31 | -0.04R | +0.01R | -0.12R | ZEC | 2026-10-22 01:13 |
| V2 | 1h | FAILED | 2475 | 31 | -0.09R | -0.03R | -0.09R | - | 2026-10-22 01:13 |
| V2 | 30m | FAILED | 2572 | 29 | -0.15R | -0.06R | -0.13R | - | 2026-10-22 01:13 |
| V2 | 15m | FAILED | 4787 | 28 | -0.21R | -0.08R | -0.22R | - | 2026-10-22 01:13 |
| V3 | 4h | FAILED | 124 | 23 | -0.25R | -0.20R | -0.27R | BNB | 2026-10-22 01:13 |
| V4 | 4h | BACKTESTING | 318 | 35 | +0.08R | +0.13R | +0.05R | BTC, ETH, SOL, XRP | 2026-10-22 01:13 |
| V5 | 1h | FAILED | 5206 | 30 | -0.11R | -0.04R | -0.11R | - | 2026-10-22 01:13 |
| V5 | 30m | FAILED | 5578 | 29 | -0.17R | -0.07R | -0.16R | - | 2026-10-22 01:13 |
| V5 | 15m | FAILED | 10408 | 27 | -0.25R | -0.10R | -0.27R | - | 2026-10-22 01:13 |

## 3. Fibonacci pullback (50-61.8% of the last swing)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 254 | 35 | -0.09R | -0.04R | -0.10R | XRP, ZEC | 2026-10-22 01:13 |
| V2 | 1h | FAILED | 2393 | 34 | -0.09R | -0.02R | -0.11R | SOL | 2026-10-22 01:13 |
| V2 | 30m | FAILED | 2806 | 35 | -0.14R | -0.03R | -0.09R | - | 2026-10-22 01:13 |
| V2 | 15m | FAILED | 4735 | 34 | -0.23R | -0.08R | -0.18R | - | 2026-10-22 01:13 |
| V3 | 4h | FAILED | 87 | 31 | -0.14R | -0.10R | -0.16R | XRP, ZEC | 2026-10-22 01:13 |
| V4 | 4h | FAILED | 251 | 31 | -0.03R | +0.02R | -0.15R | XRP, ZEC | 2026-10-22 01:13 |
| V5 | 1h | FAILED | 5126 | 34 | -0.12R | -0.05R | -0.13R | SOL, SUI | 2026-10-22 01:13 |
| V5 | 30m | FAILED | 6223 | 34 | -0.19R | -0.07R | -0.14R | - | 2026-10-22 01:13 |
| V5 | 15m | FAILED | 10447 | 33 | -0.28R | -0.11R | -0.26R | - | 2026-10-22 01:13 |

## 4. Trend momentum (MACD + Supertrend)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 384 | 36 | +0.11R | +0.15R | -0.19R | BNB, ETH, SOL, SUI, ZEC | 2026-10-23 01:18 |
| V2 | 1h | FAILED | 1202 | 33 | -0.04R | +0.01R | +0.01R | BNB, SOL, XRP | 2026-10-23 01:18 |
| V2 | 30m | FAILED | 1449 | 34 | -0.04R | +0.03R | +0.05R | SUI, XRP | 2026-10-23 01:18 |
| V2 | 15m | FAILED | 2286 | 34 | -0.08R | +0.02R | -0.01R | - | 2026-10-23 01:18 |
| V3 | 4h | BACKTESTING | 150 | 39 | +0.20R | +0.23R | +0.00R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-10-23 01:18 |
| V4 | 4h | FAILED | 373 | 37 | +0.13R | +0.17R | -0.21R | BNB, ETH, SOL, SUI, ZEC | 2026-10-23 01:18 |
| V5 | 1h | FAILED | 2398 | 32 | -0.10R | -0.05R | -0.07R | - | 2026-10-23 01:18 |
| V5 | 30m | FAILED | 3369 | 33 | -0.11R | -0.03R | -0.01R | SUI, XRP | 2026-10-23 01:18 |
| V5 | 15m | FAILED | 5037 | 33 | -0.14R | -0.03R | -0.07R | - | 2026-10-23 01:18 |

## 5. Range reversal (RSI + Bollinger)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 386 | 48 | -0.14R | -0.09R | -0.11R | SOL | 2026-10-23 01:18 |
| V2 | 1h | FAILED | 1441 | 46 | -0.23R | -0.15R | -0.26R | - | 2026-10-23 01:18 |
| V2 | 30m | FAILED | 4295 | 46 | -0.26R | -0.13R | -0.32R | - | 2026-10-23 01:18 |
| V2 | 15m | FAILED | 10572 | 42 | -0.37R | -0.19R | -0.42R | - | 2026-10-23 01:18 |
| V3 | 4h | FAILED | 75 | 52 | -0.13R | -0.08R | +0.12R | BTC, XRP | 2026-10-23 01:18 |
| V4 | 4h | BACKTESTING | 363 | 36 | +0.05R | +0.11R | +0.16R | BNB, BTC, ETH, SOL, XRP | 2026-10-23 01:18 |

## 6. VWAP reversion

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-10-24 01:21 |
| V2 | 1h | FAILED | 84 | 43 | -0.20R | -0.13R | -0.14R | SOL | 2026-10-24 01:21 |
| V2 | 30m | FAILED | 948 | 40 | -0.23R | -0.12R | -0.29R | ZEC | 2026-10-24 01:21 |
| V2 | 15m | FAILED | 3940 | 35 | -0.33R | -0.17R | -0.39R | - | 2026-10-24 01:21 |
| V3 | 4h | BACKTESTING | 0 | 0 | +0.00R | +0.00R | +0.00R | - | 2026-10-24 01:21 |
| V4 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-10-24 01:21 |

## 7. Squeeze breakout & retest

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 795 | 35 | +0.02R | +0.06R | +0.17R | BTC, ETH, SOL, XRP | 2026-10-24 01:21 |
| V2 | 1h | BACKTESTING | 1046 | 35 | +0.02R | +0.08R | +0.03R | BNB, BTC, SOL, XRP | 2026-10-24 01:21 |
| V2 | 30m | FAILED | 850 | 32 | -0.11R | -0.02R | -0.17R | ETH, SUI | 2026-10-24 01:21 |
| V2 | 15m | FAILED | 1675 | 29 | -0.23R | -0.10R | -0.28R | - | 2026-10-24 01:21 |
| V3 | 4h | BACKTESTING | 249 | 36 | +0.05R | +0.09R | +0.03R | BTC, ETH, SOL, XRP | 2026-10-24 01:21 |
| V4 | 4h | BACKTESTING | 723 | 34 | +0.06R | +0.11R | +0.33R | BNB, BTC, ETH, SOL, XRP | 2026-10-24 01:21 |
| V5 | 1h | FAILED | 2504 | 32 | -0.05R | +0.02R | -0.06R | ZEC | 2026-10-24 01:21 |
| V5 | 30m | FAILED | 1939 | 31 | -0.17R | -0.07R | -0.19R | - | 2026-10-24 01:21 |
| V5 | 15m | FAILED | 3729 | 28 | -0.26R | -0.12R | -0.28R | - | 2026-10-24 01:21 |

## 8. Session open breakout (Asia range -> London / New York)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 1h | FAILED | 1211 | 35 | -0.08R | -0.02R | -0.06R | BTC, XRP | 2026-10-25 01:12 |
| V2 | 30m | FAILED | 706 | 36 | -0.13R | -0.04R | -0.05R | SOL, SUI, XRP | 2026-10-25 01:12 |
| V2 | 15m | FAILED | 842 | 33 | -0.22R | -0.09R | -0.17R | SUI | 2026-10-25 01:12 |
| V3 | 1h | FAILED | 420 | 35 | -0.05R | +0.01R | -0.03R | BNB, SOL, XRP | 2026-10-25 01:12 |
| V4 | 1h | FAILED | 1165 | 33 | -0.08R | -0.02R | -0.05R | BTC, XRP | 2026-10-25 01:12 |
| V5 | 30m | FAILED | 1626 | 34 | -0.19R | -0.09R | -0.18R | SUI | 2026-10-25 01:12 |
| V5 | 15m | FAILED | 1896 | 32 | -0.26R | -0.12R | -0.26R | - | 2026-10-25 01:12 |

## 9. Liquidity sweep + structure shift

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 4 | 25 | -0.61R | -0.58R | -1.03R | - | 2026-10-25 01:12 |
| V2 | 1h | BACKTESTING | 11 | 36 | -0.31R | -0.27R | +0.15R | - | 2026-10-25 01:12 |
| V2 | 30m | BACKTESTING | 28 | 36 | -0.07R | -0.01R | +0.05R | - | 2026-10-25 01:12 |
| V2 | 15m | FAILED | 85 | 29 | -0.32R | -0.23R | -0.45R | XRP | 2026-10-25 01:12 |
| V3 | 4h | BACKTESTING | 1 | 0 | -1.02R | -1.00R | -1.02R | - | 2026-10-25 01:12 |
| V4 | 4h | BACKTESTING | 4 | 25 | -0.38R | -0.35R | -1.03R | - | 2026-10-25 01:12 |
| V5 | 1h | FAILED | 38 | 34 | -0.30R | -0.26R | -0.62R | - | 2026-10-25 01:12 |
| V5 | 30m | FAILED | 88 | 30 | -0.29R | -0.22R | -0.38R | SOL | 2026-10-25 01:12 |
| V5 | 15m | FAILED | 195 | 29 | -0.31R | -0.21R | -0.51R | XRP | 2026-10-25 01:12 |

## 10. Crowding fade (funding + open interest)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1 | 100 | +1.97R | +1.99R | +1.97R | - | 2026-10-20 01:15 |
| V2 | 1h | BACKTESTING | 2 | 100 | +1.63R | +1.65R | +1.63R | - | 2026-10-20 01:15 |
| V2 | 30m | BACKTESTING | 6 | 67 | +0.43R | +0.46R | +0.43R | ZEC | 2026-10-20 01:15 |
| V2 | 15m | BACKTESTING | 7 | 29 | -0.20R | -0.17R | -0.20R | - | 2026-10-20 01:15 |
| V3 | 4h | BACKTESTING | 1 | 100 | +1.97R | +1.99R | +1.97R | - | 2026-10-20 01:15 |
| V4 | 4h | BACKTESTING | 1 | 100 | +1.59R | +1.61R | +1.59R | - | 2026-10-20 01:15 |

## 11. Early momentum (market-wide break, early steps only)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 30m | FAILED | 11765 | 33 | -0.19R | -0.07R | -0.20R | - | 2026-10-21 01:16 |
| V1 | 30m | FAILED | 4235 | 32 | -0.22R | -0.11R | -0.23R | - | 2026-10-21 01:16 |
| V2 | 30m | FAILED | 1136 | 30 | -0.26R | -0.14R | -0.23R | - | 2026-10-21 01:16 |
| V3 | 1h | FAILED | 2532 | 32 | -0.13R | -0.05R | -0.18R | - | 2026-10-21 01:16 |
| V4 | 30m | FAILED | 3994 | 30 | -0.27R | -0.14R | -0.22R | - | 2026-10-21 01:16 |

## 12. Follow the leader (buy the strongest coin when BTC jumps)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 4h | FAILED | 2810 | 42 | -0.00R | +0.03R | -0.09R | BTC, SOL, ZEC | 2026-10-25 01:12 |
| V1 | 4h | BACKTESTING | 573 | 44 | +0.11R | +0.14R | +0.20R | ETH, SOL, SUI, XRP, ZEC | 2026-10-25 01:12 |
| V2 | 4h | VALIDATION | 497 | 47 | +0.19R | +0.22R | +0.37R | BNB, ETH, SOL, SUI, XRP, ZEC | 2026-10-25 01:12 |
| V3 | 1h | FAILED | 835 | 35 | -0.03R | +0.01R | -0.04R | XRP, ZEC | 2026-10-25 01:12 |

