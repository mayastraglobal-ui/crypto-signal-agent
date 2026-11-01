# Trend portfolio (paper)

Daily close 2026-10-31 (updated 2026-11-01 00:12 UTC). 9 trend signals per coin (lookbacks 5, 10, 20, 30, 60, 90, 150, 250, 360 days): ON at a close above the lookback's high, OFF below its ratcheting mid-line. Target = the share ON. Long only, no leverage, equal parts. Paper only (`docs/TREND_PORTFOLIO.md`).

| Coin | Trends up | Target | Yesterday | Paper position | Change today | Price |
|---|---|---:|---:|---:|---:|---:|
| BNB | 2/9 | 22% | 22% | $31 | - | 703.95 |
| BTC | 2/9 | 22% | 22% | $31 | - | 77,582 |
| ETH | 1/9 | 11% | 11% | $16 | - | 2,255.66 |
| SOL | 1/9 | 11% | 11% | $16 | - | 95.54 |
| SUI | 0/9 | 0% | 0% | $0.00 | - | 0.8994 |
| XRP | 0/9 | 0% | 0% | $0.00 | - | 1.2519 |
| ZEC | 4/9 | 44% | 44% | $63 | - | 1,251.42 |

**Paper account: $987** (-1.31% since 2026-10-28, start $1,000) · invested $157.

Backtest on the candles the scan has (since 2024-02-06, 999 days, costs included): portfolio +28.6% a year, Sharpe 1.34, worst drop 17.2% · holding the same coins +56.9% a year, Sharpe 1.04, worst drop 51.5%.

## Paper account, last 30 days

| Day | Account | Day's result |
|---|---:|---:|
| 2026-10-31 | $987 | -0.10% |
| 2026-10-30 | $988 | +0.25% |
| 2026-10-29 | $985 | -1.44% |
| 2026-10-28 | $1,000 | -0.02% |
