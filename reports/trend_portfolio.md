# Trend portfolio (paper)

Daily close 2026-10-29 (updated 2026-10-30 00:38 UTC). 9 trend signals per coin (lookbacks 5, 10, 20, 30, 60, 90, 150, 250, 360 days): ON at a close above the lookback's high, OFF below its ratcheting mid-line. Target = the share ON. Long only, no leverage, equal parts. Paper only (`docs/TREND_PORTFOLIO.md`).

| Coin | Trends up | Target | Yesterday | Paper position | Change today | Price |
|---|---|---:|---:|---:|---:|---:|
| BNB | 2/9 | 22% | 44% | $31 | $-31 | 698.46 |
| BTC | 2/9 | 22% | 22% | $31 | - | 77,991.9 |
| ETH | 1/9 | 11% | 22% | $16 | $-16 | 2,253.13 |
| SOL | 1/9 | 11% | 22% | $16 | $-16 | 95.64 |
| SUI | 0/9 | 0% | 0% | $0.00 | - | 0.8695 |
| XRP | 0/9 | 0% | 0% | $0.00 | - | 1.2377 |
| ZEC | 4/9 | 44% | 44% | $63 | - | 1,223 |

**Paper account: $985** (-1.46% since 2026-10-28, start $1,000) · invested $156.

Backtest on the candles the scan has (since 2024-02-04, 999 days, costs included): portfolio +28.8% a year, Sharpe 1.35, worst drop 17.2% · holding the same coins +56.2% a year, Sharpe 1.03, worst drop 51.5%.

## Paper account, last 30 days

| Day | Account | Day's result |
|---|---:|---:|
| 2026-10-29 | $985 | -1.44% |
| 2026-10-28 | $1,000 | -0.02% |
