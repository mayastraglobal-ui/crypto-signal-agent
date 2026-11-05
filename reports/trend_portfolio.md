# Trend portfolio (paper)

Daily close 2026-11-04 (updated 2026-11-05 00:12 UTC). 9 trend signals per coin (lookbacks 5, 10, 20, 30, 60, 90, 150, 250, 360 days): ON at a close above the lookback's high, OFF below its ratcheting mid-line. Target = the share ON. Long only, no leverage, equal parts. Paper only (`docs/TREND_PORTFOLIO.md`).

| Coin | Trends up | Target | Yesterday | Paper position | Change today | Price |
|---|---|---:|---:|---:|---:|---:|
| BNB | 2/9 | 22% | 22% | $31 | - | 719.99 |
| BTC | 3/9 | 33% | 22% | $47 | +$16 | 80,504 |
| ETH | 3/9 | 33% | 11% | $47 | +$31 | 2,424.61 |
| SOL | 0/9 | 0% | 0% | $0.00 | - | 95.61 |
| SUI | 1/9 | 11% | 0% | $16 | +$16 | 0.9292 |
| XRP | 1/9 | 11% | 0% | $16 | +$16 | 1.3052 |
| ZEC | 4/9 | 44% | 44% | $63 | - | 1,296.78 |

**Paper account: $992** (-0.82% since 2026-10-28, start $1,000) · invested $220.

Backtest on the candles the scan has (since 2024-02-10, 999 days, costs included): portfolio +27.3% a year, Sharpe 1.3, worst drop 17.2% · holding the same coins +54.0% a year, Sharpe 1.01, worst drop 51.5%.

## Paper account, last 30 days

| Day | Account | Day's result |
|---|---:|---:|
| 2026-11-04 | $992 | +0.72% |
| 2026-11-03 | $985 | +0.51% |
| 2026-11-02 | $980 | -0.70% |
| 2026-11-01 | $987 | -0.02% |
| 2026-10-31 | $987 | -0.10% |
| 2026-10-30 | $988 | +0.25% |
| 2026-10-29 | $985 | -1.44% |
| 2026-10-28 | $1,000 | -0.02% |
