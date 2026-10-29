# Trend portfolio (paper)

Daily close 2026-10-28 (updated 2026-10-29 01:57 UTC). 9 trend signals per coin (lookbacks 5, 10, 20, 30, 60, 90, 150, 250, 360 days): ON at a close above the lookback's high, OFF below its ratcheting mid-line. Target = the share ON. Long only, no leverage, equal parts. Paper only (`docs/TREND_PORTFOLIO.md`).

| Coin | Trends up | Target | Yesterday | Paper position | Change today | Price |
|---|---|---:|---:|---:|---:|---:|
| BNB | 4/9 | 44% | 33% | $63 | +$16 | 759.85 |
| BTC | 2/9 | 22% | 22% | $32 | - | 81,343.5 |
| ETH | 2/9 | 22% | 22% | $32 | - | 2,359.68 |
| SOL | 2/9 | 22% | 22% | $32 | - | 102.44 |
| SUI | 0/9 | 0% | 0% | $0.00 | - | 0.9433 |
| XRP | 0/9 | 0% | 0% | $0.00 | - | 1.326 |
| ZEC | 4/9 | 44% | 44% | $63 | - | 1,311.01 |

**Paper account: $1,000** (-0.02% since 2026-10-28, start $1,000) · invested $222.

Backtest on the candles the scan has (since 2024-02-03, 999 days, costs included): portfolio +29.7% a year, Sharpe 1.39, worst drop 17.2% · holding the same coins +59.5% a year, Sharpe 1.06, worst drop 51.5%.

## Paper account, last 30 days

| Day | Account | Day's result |
|---|---:|---:|
| 2026-10-28 | $1,000 | -0.02% |
