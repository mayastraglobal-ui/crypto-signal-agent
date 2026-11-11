# Forward Test Program - backtest results

Updated 2026-11-11 07:00 UTC. Tested tonight: strategies 1, 8, 12, 13; next night: 2, 9, 12, 13.

10 strategies x 4 versions (strategies_program.yaml). Every number includes OKX fees and funding ('after fees'); 'before fees' shows what the rules alone made. 'Test' = the unseen last 30% of each coin's history. A coin counts as positive with >= 5 trades and an average above 0R after fees.

Versions: V1 base (4H) · V2 faster (1H / 30m / 15m) · V3 + daily agrees · V4 trailing ATR exit.

## 1. Breakout (Donchian + volume + ADX)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1136 | 39 | +0.18R | +0.21R | +0.12R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-11 07:00 |
| V2 | 1h | FAILED | 1986 | 32 | -0.02R | +0.03R | +0.05R | BTC, SOL, SUI | 2026-11-11 07:00 |
| V2 | 30m | FAILED | 1270 | 35 | -0.02R | +0.04R | +0.04R | BTC, ETH, SOL, SUI | 2026-11-11 07:00 |
| V2 | 15m | FAILED | 1987 | 33 | -0.07R | +0.02R | -0.05R | BTC | 2026-11-11 07:00 |
| V3 | 4h | BACKTESTING | 353 | 40 | +0.21R | +0.24R | +0.25R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-11 07:00 |
| V4 | 4h | BACKTESTING | 965 | 39 | +0.18R | +0.22R | +0.10R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-11 07:00 |
| V5 | 1h | FAILED | 4061 | 33 | -0.02R | +0.03R | +0.00R | BTC, ETH, SUI | 2026-11-11 07:00 |
| V5 | 30m | FAILED | 2822 | 33 | -0.09R | -0.01R | -0.08R | SUI | 2026-11-11 07:00 |
| V5 | 15m | FAILED | 4374 | 32 | -0.13R | -0.03R | -0.15R | - | 2026-11-11 07:00 |

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
| V1 | 4h | FAILED | 257 | 35 | -0.07R | -0.02R | -0.06R | XRP, ZEC | 2026-11-08 06:38 |
| V2 | 1h | FAILED | 2408 | 34 | -0.09R | -0.02R | -0.10R | SOL | 2026-11-08 06:38 |
| V2 | 30m | FAILED | 2805 | 35 | -0.14R | -0.03R | -0.10R | - | 2026-11-08 06:38 |
| V2 | 15m | FAILED | 4741 | 34 | -0.23R | -0.08R | -0.19R | - | 2026-11-08 06:38 |
| V3 | 4h | FAILED | 87 | 31 | -0.14R | -0.10R | -0.17R | XRP, ZEC | 2026-11-08 06:38 |
| V4 | 4h | FAILED | 254 | 32 | -0.02R | +0.03R | -0.11R | XRP, ZEC | 2026-11-08 06:38 |
| V5 | 1h | FAILED | 5159 | 34 | -0.12R | -0.05R | -0.13R | SOL, SUI | 2026-11-08 06:38 |
| V5 | 30m | FAILED | 6233 | 34 | -0.18R | -0.07R | -0.14R | - | 2026-11-08 06:38 |
| V5 | 15m | FAILED | 10467 | 33 | -0.28R | -0.11R | -0.26R | - | 2026-11-08 06:38 |

## 4. Trend momentum (MACD + Supertrend)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 387 | 36 | +0.10R | +0.14R | -0.23R | BNB, ETH, SOL, SUI, ZEC | 2026-11-09 07:06 |
| V2 | 1h | FAILED | 1207 | 33 | -0.04R | +0.01R | +0.01R | BNB, SOL, XRP | 2026-11-09 07:06 |
| V2 | 30m | FAILED | 1450 | 34 | -0.04R | +0.03R | +0.05R | SUI, XRP | 2026-11-09 07:06 |
| V2 | 15m | FAILED | 2288 | 34 | -0.08R | +0.02R | -0.05R | ETH | 2026-11-09 07:06 |
| V3 | 4h | FAILED | 151 | 38 | +0.19R | +0.22R | -0.04R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-11-09 07:06 |
| V4 | 4h | FAILED | 376 | 37 | +0.12R | +0.16R | -0.24R | BNB, ETH, SOL, SUI, ZEC | 2026-11-09 07:06 |
| V5 | 1h | FAILED | 2413 | 32 | -0.10R | -0.05R | -0.08R | - | 2026-11-09 07:06 |
| V5 | 30m | FAILED | 3373 | 33 | -0.11R | -0.03R | -0.01R | SUI, XRP | 2026-11-09 07:06 |
| V5 | 15m | FAILED | 5038 | 33 | -0.14R | -0.03R | -0.08R | - | 2026-11-09 07:06 |

## 5. Range reversal (RSI + Bollinger)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 392 | 49 | -0.12R | -0.08R | -0.06R | - | 2026-11-09 07:06 |
| V2 | 1h | FAILED | 1446 | 46 | -0.23R | -0.15R | -0.26R | - | 2026-11-09 07:06 |
| V2 | 30m | FAILED | 4283 | 46 | -0.26R | -0.13R | -0.34R | - | 2026-11-09 07:06 |
| V2 | 15m | FAILED | 10577 | 42 | -0.38R | -0.19R | -0.43R | - | 2026-11-09 07:06 |
| V3 | 4h | FAILED | 77 | 53 | -0.08R | -0.04R | +0.24R | BTC, XRP | 2026-11-09 07:06 |
| V4 | 4h | BACKTESTING | 367 | 36 | +0.05R | +0.11R | +0.17R | BNB, BTC, ETH, SOL, XRP | 2026-11-09 07:06 |

## 6. VWAP reversion

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-11-10 07:41 |
| V2 | 1h | FAILED | 84 | 43 | -0.20R | -0.13R | -0.14R | SOL | 2026-11-10 07:41 |
| V2 | 30m | FAILED | 956 | 40 | -0.23R | -0.12R | -0.29R | ZEC | 2026-11-10 07:41 |
| V2 | 15m | FAILED | 3963 | 35 | -0.33R | -0.17R | -0.39R | - | 2026-11-10 07:41 |
| V3 | 4h | BACKTESTING | 0 | 0 | +0.00R | +0.00R | +0.00R | - | 2026-11-10 07:41 |
| V4 | 4h | BACKTESTING | 1 | 0 | -1.09R | -1.03R | -1.09R | - | 2026-11-10 07:41 |

## 7. Squeeze breakout & retest

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 798 | 35 | +0.02R | +0.06R | +0.16R | BTC, ETH, SOL, XRP | 2026-11-10 07:41 |
| V2 | 1h | BACKTESTING | 1055 | 35 | +0.01R | +0.07R | +0.01R | BNB, BTC, SOL, XRP | 2026-11-10 07:41 |
| V2 | 30m | FAILED | 850 | 32 | -0.11R | -0.02R | -0.17R | ETH, SUI | 2026-11-10 07:41 |
| V2 | 15m | FAILED | 1681 | 29 | -0.23R | -0.10R | -0.32R | - | 2026-11-10 07:41 |
| V3 | 4h | BACKTESTING | 252 | 36 | +0.05R | +0.09R | +0.02R | BTC, ETH, SOL, XRP | 2026-11-10 07:41 |
| V4 | 4h | BACKTESTING | 725 | 34 | +0.06R | +0.10R | +0.29R | BNB, BTC, ETH, SOL, XRP | 2026-11-10 07:41 |
| V5 | 1h | FAILED | 2518 | 32 | -0.05R | +0.02R | -0.07R | ZEC | 2026-11-10 07:41 |
| V5 | 30m | FAILED | 1936 | 31 | -0.17R | -0.07R | -0.18R | - | 2026-11-10 07:41 |
| V5 | 15m | FAILED | 3741 | 28 | -0.26R | -0.12R | -0.29R | - | 2026-11-10 07:41 |

## 8. Session open breakout (Asia range -> London / New York)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 1h | FAILED | 1216 | 35 | -0.08R | -0.02R | -0.07R | BTC, XRP | 2026-11-11 07:00 |
| V2 | 30m | FAILED | 709 | 36 | -0.12R | -0.03R | -0.03R | SOL, SUI, XRP | 2026-11-11 07:00 |
| V2 | 15m | FAILED | 847 | 33 | -0.22R | -0.10R | -0.17R | SUI | 2026-11-11 07:00 |
| V3 | 1h | FAILED | 423 | 35 | -0.05R | +0.01R | -0.02R | BNB, SOL, XRP | 2026-11-11 07:00 |
| V4 | 1h | FAILED | 1169 | 33 | -0.08R | -0.02R | -0.06R | BTC, XRP | 2026-11-11 07:00 |
| V5 | 30m | FAILED | 1635 | 34 | -0.19R | -0.09R | -0.17R | SUI | 2026-11-11 07:00 |
| V5 | 15m | FAILED | 1906 | 32 | -0.27R | -0.12R | -0.25R | - | 2026-11-11 07:00 |

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
| C | 30m | FAILED | 11874 | 33 | -0.19R | -0.07R | -0.20R | - | 2026-11-08 06:38 |
| V1 | 30m | FAILED | 4295 | 32 | -0.22R | -0.10R | -0.22R | - | 2026-11-08 06:38 |
| V2 | 30m | FAILED | 1146 | 30 | -0.26R | -0.14R | -0.24R | - | 2026-11-08 06:38 |
| V3 | 1h | FAILED | 2545 | 32 | -0.13R | -0.05R | -0.19R | - | 2026-11-08 06:38 |
| V4 | 30m | FAILED | 3996 | 31 | -0.27R | -0.14R | -0.23R | - | 2026-11-08 06:38 |

## 12. Follow the leader (buy the strongest coin when BTC jumps)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 4h | FAILED | 2817 | 42 | -0.01R | +0.03R | -0.09R | BTC, SOL, ZEC | 2026-11-11 07:00 |
| V1 | 4h | BACKTESTING | 574 | 44 | +0.11R | +0.14R | +0.20R | ETH, SOL, SUI, XRP, ZEC | 2026-11-11 07:00 |
| V2 | 4h | VALIDATION | 498 | 47 | +0.19R | +0.22R | +0.36R | BNB, ETH, SOL, SUI, XRP, ZEC | 2026-11-11 07:00 |
| V3 | 1h | FAILED | 837 | 35 | -0.03R | +0.01R | -0.04R | XRP, ZEC | 2026-11-11 07:00 |

## 13. Daily Turtle (55-day breakout, ride the trend)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| C | 4h | PAPER_TRADING | 467 | 51 | +0.21R | +0.23R | +0.21R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-11 07:00 |
| V1 | 4h | VALIDATION | 157 | 41 | +1.83R | +1.95R | +1.29R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-11 07:00 |
| V2 | 4h | VALIDATION | 124 | 46 | +2.00R | +2.12R | +1.86R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-11 07:00 |
| V3 | 4h | VALIDATION | 128 | 41 | +1.92R | +2.04R | +1.55R | BNB, BTC, ETH, SOL, SUI, XRP, ZEC | 2026-11-11 07:00 |

