# Forward Test Program - backtest results

Updated 2026-10-13 01:02 UTC. Tested tonight: strategies 7, 8; next night: 9, 10.

10 strategies x 4 versions (strategies_program.yaml). Every number includes OKX fees and funding ('after fees'); 'before fees' shows what the rules alone made. 'Test' = the unseen last 30% of each coin's history. A coin counts as positive with >= 5 trades and an average above 0R after fees.

Versions: V1 base (4H) · V2 faster (1H / 30m / 15m) · V3 + daily agrees · V4 trailing ATR exit.

## 1. Breakout (Donchian + volume + ADX)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | BACKTESTING | 1058 | 40 | +0.19R | +0.22R | +0.13R | BNB, BTC, ETH, SOL, XRP | 2026-10-10 00:59 |
| V2 | 1h | FAILED | 1849 | 32 | -0.02R | +0.02R | +0.06R | BTC, SOL | 2026-10-10 00:59 |
| V2 | 30m | BACKTESTING | 873 | 36 | +0.01R | +0.08R | +0.08R | BTC, ETH, SOL | 2026-10-10 00:59 |
| V2 | 15m | FAILED | 1330 | 34 | -0.06R | +0.04R | -0.01R | BTC, XRP | 2026-10-10 00:59 |
| V3 | 4h | BACKTESTING | 333 | 40 | +0.21R | +0.24R | +0.21R | BNB, BTC, ETH, SOL, XRP | 2026-10-10 00:59 |
| V4 | 4h | BACKTESTING | 900 | 40 | +0.18R | +0.23R | +0.09R | BNB, BTC, ETH, SOL, XRP | 2026-10-10 00:59 |
| V5 | 1h | FAILED | 3762 | 33 | -0.02R | +0.03R | +0.02R | BTC, ETH | 2026-10-10 00:59 |
| V5 | 30m | FAILED | 1938 | 33 | -0.10R | -0.01R | -0.07R | - | 2026-10-10 00:59 |
| V5 | 15m | FAILED | 2971 | 32 | -0.15R | -0.04R | -0.14R | - | 2026-10-10 00:59 |

## 2. EMA trend pullback (EMA20/50 + RSI + VWAP)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 299 | 31 | -0.02R | +0.02R | -0.13R | XRP, ZEC | 2026-10-10 00:59 |
| V2 | 1h | FAILED | 2302 | 31 | -0.09R | -0.02R | -0.10R | - | 2026-10-10 00:59 |
| V2 | 30m | FAILED | 1692 | 30 | -0.14R | -0.03R | -0.13R | - | 2026-10-10 00:59 |
| V2 | 15m | FAILED | 3121 | 28 | -0.21R | -0.06R | -0.25R | - | 2026-10-10 00:59 |
| V3 | 4h | FAILED | 117 | 23 | -0.26R | -0.21R | -0.30R | BNB | 2026-10-10 00:59 |
| V4 | 4h | BACKTESTING | 297 | 35 | +0.10R | +0.15R | +0.03R | BTC, ETH, SOL, XRP | 2026-10-10 00:59 |
| V5 | 1h | FAILED | 4852 | 30 | -0.11R | -0.04R | -0.11R | - | 2026-10-10 00:59 |
| V5 | 30m | FAILED | 3703 | 30 | -0.16R | -0.04R | -0.17R | - | 2026-10-10 00:59 |
| V5 | 15m | FAILED | 6894 | 28 | -0.26R | -0.09R | -0.31R | - | 2026-10-10 00:59 |

## 3. Fibonacci pullback (50-61.8% of the last swing)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 253 | 35 | -0.08R | -0.03R | -0.10R | XRP, ZEC | 2026-10-11 00:58 |
| V2 | 1h | FAILED | 2388 | 34 | -0.09R | -0.02R | -0.11R | - | 2026-10-11 00:58 |
| V2 | 30m | FAILED | 2812 | 35 | -0.14R | -0.04R | -0.09R | - | 2026-10-11 00:58 |
| V2 | 15m | FAILED | 4763 | 34 | -0.23R | -0.08R | -0.19R | - | 2026-10-11 00:58 |
| V3 | 4h | FAILED | 87 | 31 | -0.14R | -0.10R | -0.16R | XRP, ZEC | 2026-10-11 00:58 |
| V4 | 4h | FAILED | 250 | 31 | -0.03R | +0.03R | -0.15R | XRP, ZEC | 2026-10-11 00:58 |
| V5 | 1h | FAILED | 5109 | 34 | -0.12R | -0.05R | -0.12R | SOL, SUI | 2026-10-11 00:58 |
| V5 | 30m | FAILED | 6226 | 34 | -0.19R | -0.07R | -0.14R | - | 2026-10-11 00:58 |
| V5 | 15m | FAILED | 10470 | 33 | -0.28R | -0.11R | -0.26R | - | 2026-10-11 00:58 |

## 4. Trend momentum (MACD + Supertrend)

| Version | TF | Status | Trades | Win % | After fees | Before fees | Test | Positive coins | Tested |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| V1 | 4h | FAILED | 383 | 36 | +0.11R | +0.15R | -0.19R | BNB, ETH, SOL, SUI, ZEC | 2026-10-11 00:58 |
| V2 | 1h | FAILED | 1199 | 33 | -0.03R | +0.02R | +0.01R | BNB, SOL, XRP | 2026-10-11 00:58 |
| V2 | 30m | FAILED | 1450 | 35 | -0.04R | +0.04R | +0.07R | SUI, XRP | 2026-10-11 00:58 |
| V2 | 15m | FAILED | 2287 | 34 | -0.08R | +0.02R | -0.01R | XRP | 2026-10-11 00:58 |
| V3 | 4h | BACKTESTING | 150 | 39 | +0.20R | +0.23R | +0.00R | BNB, BTC, ETH, SOL, SUI, XRP | 2026-10-11 00:58 |
| V4 | 4h | FAILED | 372 | 37 | +0.13R | +0.18R | -0.20R | BNB, ETH, SOL, SUI, ZEC | 2026-10-11 00:58 |
| V5 | 1h | FAILED | 2387 | 32 | -0.10R | -0.04R | -0.06R | SUI | 2026-10-11 00:58 |
| V5 | 30m | FAILED | 3360 | 33 | -0.11R | -0.03R | +0.00R | SUI, XRP | 2026-10-11 00:58 |
| V5 | 15m | FAILED | 5024 | 33 | -0.14R | -0.02R | -0.07R | - | 2026-10-11 00:58 |

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

