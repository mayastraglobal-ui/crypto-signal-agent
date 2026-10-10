# Forward Test Program - backtest results

Updated 2026-10-10 00:59 UTC. Tested tonight: strategies 1, 2; next night: 3, 4.

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

