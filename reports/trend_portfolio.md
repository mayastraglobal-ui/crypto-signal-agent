# Trend portfolio (paper)

Daily close 2026-11-01 (updated 2026-11-02 00:34 UTC). 9 trend signals per coin (lookbacks 5, 10, 20, 30, 60, 90, 150, 250, 360 days): ON at a close above the lookback's high, OFF below its ratcheting mid-line. Target = the share ON. Long only, no leverage, equal parts. Paper only (`docs/TREND_PORTFOLIO.md`).

| Coin | Trends up | Target | Yesterday | Paper position | Change today | Price |
|---|---|---:|---:|---:|---:|---:|
| BNB | 2/9 | 22% | 22% | $31 | - | 712.69 |
| BTC | 2/9 | 22% | 22% | $31 | - | 78,354 |
| ETH | 1/9 | 11% | 11% | $16 | - | 2,275.31 |
| SOL | 1/9 | 11% | 11% | $16 | - | 94.53 |
| SUI | 0/9 | 0% | 0% | $0.00 | - | 0.9007 |
| XRP | 0/9 | 0% | 0% | $0.00 | - | 1.2507 |
| ZEC | 4/9 | 44% | 44% | $63 | - | 1,234.56 |

**Paper account: $987** (-1.33% since 2026-10-28, start $1,000) · invested $157.

Backtest on the candles the scan has (since 2024-02-07, 999 days, costs included): portfolio +28.1% a year, Sharpe 1.33, worst drop 17.2% · holding the same coins +55.1% a year, Sharpe 1.02, worst drop 51.5%.

## Paper account, last 30 days

| Day | Account | Day's result |
|---|---:|---:|
| 2026-11-01 | $987 | -0.02% |
| 2026-10-31 | $987 | -0.10% |
| 2026-10-30 | $988 | +0.25% |
| 2026-10-29 | $985 | -1.44% |
| 2026-10-28 | $1,000 | -0.02% |
