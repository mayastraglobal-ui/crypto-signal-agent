# Forward Test Program - backtest results

Updated 2026-10-17 01:12 UTC. Tested tonight: strategies 3, 4, 12; next night: 5, 6, 12.

10 strategies x 4 versions (strategies_program.yaml). Every number includes OKX fees and funding ('after fees'); 'before fees' shows what the rules alone made. 'Test' = the unseen last 30% of each coin's history. A coin counts as positive with >= 5 trades and an average above 0R after fees.

Versions: V1 base (4H) · V2 faster (1H / 30m / 15m) · V3 + daily agrees · V4 trailing ATR exit.

## 1. Breakout (Donchian + volume + ADX)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1133 | 39 | +0.18R | +0.21R | +0.14R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-10-16 01:10 |
| V2 | 1h | FAILED | 1972 | 32 | -0.01R | +0.03R | +0.06R | BTC, SOL, SUI | 2026-10-16 01:10 |
| V2 | 30m | FAILED | 1257 | 35 | -0.01R | +0.06R | +0.07R | BTC, ETH, SOL, SUI | 2026-10-16 01:10 |
| V2 | 15m | FAILED | 1954 | 34 | -0.05R | +0.03R | +0.01R | BTC, XRP | 2026-10-16 01:10 |
| V3 | 4h | BACKTESTING | 353 | 40 | +0.21R | +0.24R | +0.24R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-10-16 01:10 |
| V4 | 4h | BACKTESTING | 962 | 39 | +0.18R | +0.22R | +0.13R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-10-16 01:10 |
| V5 | 1h | FAILED | 4029 | 33 | -0.02R | +0.03R | +0.02R | BTC, ETH, SUI | 2026-10-16 01:10 |
| V5 | 30m | FAILED | 2792 | 33 | -0.08R | -0.00R | -0.06R | SUI | 2026-10-16 01:10 |
| V5 | 15m | FAILED | 4311 | 32 | -0.12R | -0.02R | -0.12R | - | 2026-10-16 01:10 |

## 2. EMA trend pullback (EMA20/50 + RSI + VWAP)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 319 | 31 | -0.03R | +0.01R | -0.12R | XRP, ZEC | 2026-10-16 01:10 |
| V2 | 1h | FAILED | 2475 | 31 | -0.09R | -0.03R | -0.10R | - | 2026-10-16 01:10 |
| V2 | 30m | FAILED | 2574 | 29 | -0.15R | -0.05R | -0.13R | - | 2026-10-16 01:10 |
| V2 | 15m | FAILED | 4793 | 28 | -0.21R | -0.08R | -0.22R | - | 2026-10-16 01:10 |
| V3 | 4h | FAILED | 124 | 23 | -0.25R | -0.20R | -0.27R | BNB | 2026-10-16 01:10 |
| V4 | 4h | BACKTESTING | 317 | 35 | +0.08R | +0.14R | +0.05R | BTC, ETH, SOL, XRP | 2026-10-16 01:10 |
| V5 | 1h | FAILED | 5197 | 30 | -0.11R | -0.04R | -0.11R | - | 2026-10-16 01:10 |
| V5 | 30m | FAILED | 5569 | 29 | -0.17R | -0.07R | -0.16R | - | 2026-10-16 01:10 |
| V5 | 15m | FAILED | 10399 | 27 | -0.25R | -0.10R | -0.27R | - | 2026-10-16 01:10 |

## 3. Fibonacci pullback (50-61.8% of the last swing)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 254 | 35 | -0.09R | -0.04R | -0.11R | XRP, ZEC | 2026-10-17 01:12 |
| V2 | 1h | FAILED | 2393 | 34 | -0.09R | -0.02R | -0.11R | SOL | 2026-10-17 01:12 |
| V2 | 30m | FAILED | 2813 | 35 | -0.14R | -0.03R | -0.08R | - | 2026-10-17 01:12 |
| V2 | 15m | FAILED | 4753 | 34 | -0.23R | -0.08R | -0.18R | - | 2026-10-17 01:12 |
| V3 | 4h | FAILED | 87 | 31 | -0.14R | -0.10R | -0.16R | XRP, ZEC | 2026-10-17 01:12 |
| V4 | 4h | FAILED | 251 | 31 | -0.03R | +0.02R | -0.16R | XRP, ZEC | 2026-10-17 01:12 |
| V5 | 1h | FAILED | 5120 | 34 | -0.12R | -0.05R | -0.12R | SOL, SUI | 2026-10-17 01:12 |
| V5 | 30m | FAILED | 6225 | 34 | -0.18R | -0.07R | -0.13R | - | 2026-10-17 01:12 |
| V5 | 15m | FAILED | 10463 | 33 | -0.28R | -0.11R | -0.26R | - | 2026-10-17 01:12 |

## 4. Trend momentum (MACD + Supertrend)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 383 | 36 | +0.11R | +0.15R | -0.19R | BNB, ETH, SOL, SUI, ZEC | 2026-10-17 01:12 |
| V2 | 1h | FAILED | 1202 | 33 | -0.04R | +0.01R | +0.01R | BNB, SOL, XRP | 2026-10-17 01:12 |
| V2 | 30m | FAILED | 1452 | 35 | -0.04R | +0.03R | +0.06R | SUI, XRP | 2026-10-17 01:12 |
| V2 | 15m | FAILED | 2290 | 34 | -0.08R | +0.02R | -0.01R | XRP | 2026-10-17 01:12 |
| V3 | 4h | BACKTESTING | 150 | 39 | +0.20R | +0.23R | +0.00R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-10-17 01:12 |
| V4 | 4h | FAILED | 372 | 37 | +0.13R | +0.18R | -0.20R | BNB, ETH, SOL, SUI, ZEC | 2026-10-17 01:12 |
| V5 | 1h | FAILED | 2392 | 32 | -0.10R | -0.05R | -0.07R | SUI | 2026-10-17 01:12 |
| V5 | 30m | FAILED | 3367 | 33 | -0.11R | -0.03R | -0.01R | SUI, XRP | 2026-10-17 01:12 |
| V5 | 15m | FAILED | 5031 | 33 | -0.13R | -0.02R | -0.06R | - | 2026-10-17 01:12 |

## 5. Range reversal (RSI + Bollinger)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 385 | 49 | -0.14R | -0.09R | -0.12R | SOL | 2026-10-12 01:01 |
| V2 | 1h | FAILED | 1428 | 46 | -0.23R | -0.15R | -0.24R | - | 2026-10-12 01:01 |
| V2 | 30m | FAILED | 4268 | 46 | -0.26R | -0.13R | -0.33R | - | 2026-10-12 01:01 |
| V2 | 15m | FAILED | 10548 | 42 | -0.38R | -0.19R | -0.42R | - | 2026-10-12 01:01 |
| V3 | 4h | FAILED | 75 | 52 | -0.13R | -0.08R | +0.07R | BTC, XRP | 2026-10-12 01:01 |
| V4 | 4h | BACKTESTING | 362 | 36 | +0.05R | +0.11R | +0.16R | BNB, BTC, ETH, SOL, XRP | 2026-10-12 01:01 |

## 6. VWAP reversion

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-10-12 01:01 |
| V2 | 1h | FAILED | 83 | 43 | -0.20R | -0.13R | -0.11R | SOL | 2026-10-12 01:01 |
| V2 | 30m | FAILED | 937 | 40 | -0.23R | -0.11R | -0.28R | ZEC | 2026-10-12 01:01 |
| V2 | 15m | FAILED | 3911 | 34 | -0.34R | -0.17R | -0.38R | - | 2026-10-12 01:01 |
| V3 | 4h | BACKTESTING | 0 | 0 | +0.00R | +0.00R | +0.00R | - | 2026-10-12 01:01 |
| V4 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-10-12 01:01 |

## 7. Squeeze breakout & retest

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 794 | 35 | +0.02R | +0.06R | +0.17R | BTC, ETH, SOL, XRP | 2026-10-13 01:02 |
| V2 | 1h | BACKTESTING | 1045 | 34 | +0.01R | +0.07R | +0.02R | BNB, BTC, SOL, XRP | 2026-10-13 01:02 |
| V2 | 30m | FAILED | 854 | 32 | -0.11R | -0.02R | -0.18R | ETH, SUI | 2026-10-13 01:02 |
| V2 | 15m | FAILED | 1686 | 29 | -0.22R | -0.09R | -0.27R | - | 2026-10-13 01:02 |
| V3 | 4h | BACKTESTING | 249 | 36 | +0.05R | +0.09R | +0.03R | BTC, ETH, SOL, XRP | 2026-10-13 01:02 |
| V4 | 4h | BACKTESTING | 722 | 34 | +0.06R | +0.11R | +0.33R | BNB, BTC, ETH, SOL, XRP | 2026-10-13 01:02 |
| V5 | 1h | FAILED | 2496 | 32 | -0.05R | +0.02R | -0.05R | ZEC | 2026-10-13 01:02 |
| V5 | 30m | FAILED | 1947 | 31 | -0.17R | -0.07R | -0.17R | - | 2026-10-13 01:02 |
| V5 | 15m | FAILED | 3732 | 29 | -0.25R | -0.11R | -0.27R | - | 2026-10-13 01:02 |

## 8. Session open breakout (Asia range -> London / New York)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 1h | FAILED | 1210 | 35 | -0.08R | -0.02R | -0.07R | BTC, XRP | 2026-10-13 01:02 |
| V2 | 30m | FAILED | 707 | 36 | -0.13R | -0.04R | -0.06R | SOL, SUI, XRP | 2026-10-13 01:02 |
| V2 | 15m | FAILED | 841 | 33 | -0.22R | -0.09R | -0.18R | SUI | 2026-10-13 01:02 |
| V3 | 1h | FAILED | 420 | 35 | -0.05R | +0.01R | -0.03R | BNB, SOL, XRP | 2026-10-13 01:02 |
| V4 | 1h | FAILED | 1164 | 33 | -0.08R | -0.02R | -0.06R | BTC, XRP | 2026-10-13 01:02 |
| V5 | 30m | FAILED | 1622 | 34 | -0.19R | -0.09R | -0.20R | SUI | 2026-10-13 01:02 |
| V5 | 15m | FAILED | 1893 | 32 | -0.26R | -0.12R | -0.26R | - | 2026-10-13 01:02 |

## 9. Liquidity sweep + structure shift

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 4 | 25 | -0.61R | -0.58R | -1.03R | - | 2026-10-14 01:13 |
| V2 | 1h | BACKTESTING | 13 | 46 | +0.12R | +0.16R | +0.61R | - | 2026-10-14 01:13 |
| V2 | 30m | FAILED | 35 | 34 | -0.04R | +0.01R | -0.04R | UNI | 2026-10-14 01:13 |
| V2 | 15m | FAILED | 102 | 32 | -0.24R | -0.16R | -0.41R | UNI, XRP | 2026-10-14 01:13 |
| V3 | 4h | BACKTESTING | 1 | 0 | -1.02R | -1.00R | -1.02R | - | 2026-10-14 01:13 |
| V4 | 4h | BACKTESTING | 4 | 25 | -0.38R | -0.35R | -1.03R | - | 2026-10-14 01:13 |
| V5 | 1h | FAILED | 44 | 36 | -0.18R | -0.13R | -0.45R | UNI | 2026-10-14 01:13 |
| V5 | 30m | FAILED | 103 | 29 | -0.29R | -0.23R | -0.40R | SOL | 2026-10-14 01:13 |
| V5 | 15m | FAILED | 225 | 31 | -0.28R | -0.18R | -0.50R | XRP | 2026-10-14 01:13 |

## 10. Crowding fade (funding + open interest)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1 | 100 | +1.97R | +1.99R | +1.97R | - | 2026-10-14 01:13 |
| V2 | 1h | BACKTESTING | 2 | 100 | +1.63R | +1.65R | +1.63R | - | 2026-10-14 01:13 |
| V2 | 30m | BACKTESTING | 6 | 67 | +0.43R | +0.46R | +0.43R | ZEC | 2026-10-14 01:13 |
| V2 | 15m | BACKTESTING | 7 | 29 | -0.20R | -0.17R | -0.20R | - | 2026-10-14 01:13 |
| V3 | 4h | BACKTESTING | 1 | 100 | +1.97R | +1.99R | +1.97R | - | 2026-10-14 01:13 |
| V4 | 4h | BACKTESTING | 1 | 100 | +1.59R | +1.61R | +1.59R | - | 2026-10-14 01:13 |

## 11. Early momentum (market-wide break, early steps only)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 30m | FAILED | 11724 | 33 | -0.19R | -0.07R | -0.20R | - | 2026-10-15 01:11 |
| V1 | 30m | FAILED | 4210 | 32 | -0.22R | -0.11R | -0.23R | - | 2026-10-15 01:11 |
| V2 | 30m | FAILED | 1128 | 30 | -0.26R | -0.14R | -0.24R | - | 2026-10-15 01:11 |
| V3 | 1h | FAILED | 2514 | 32 | -0.13R | -0.05R | -0.18R | - | 2026-10-15 01:11 |
| V4 | 30m | FAILED | 3989 | 30 | -0.27R | -0.14R | -0.23R | - | 2026-10-15 01:11 |

## 12. Follow the leader (buy the strongest coin when BTC jumps)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 4h | FAILED | 2810 | 42 | -0.00R | +0.03R | -0.07R | BTC, SOL, ZEC | 2026-10-17 01:12 |
| V1 | 4h | BACKTESTING | 573 | 44 | +0.11R | +0.14R | +0.21R | ETH, SOL, SUI, XRP, ZEC | 2026-10-17 01:12 |
| V2 | 4h | VALIDATION | 497 | 47 | +0.19R | +0.22R | +0.35R | BNB, ETH, SOL, SUI, XRP, ZEC | 2026-10-17 01:12 |
| V3 | 1h | FAILED | 835 | 35 | -0.03R | +0.01R | -0.04R | XRP, ZEC | 2026-10-17 01:12 |

