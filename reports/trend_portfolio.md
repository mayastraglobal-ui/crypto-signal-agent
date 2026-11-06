# Trend portfolio (paper)

Daily close 2026-11-05 (updated 2026-11-06 00:06 UTC). 9 trend signals per coin (lookbacks 5, 10, 20, 30, 60, 90, 150, 250, 360 days): ON at a close above the lookback's high, OFF below its ratcheting mid-line. Target = the share ON. Long only, no leverage, equal parts. Paper only (`docs/TREND_PORTFOLIO.md`).

| Coin | Trends up | Target | Yesterday | Paper position | Change today | Price |
|---|---|---:|---:|---:|---:|---:|
| BNB | 1/9 | 11% | 22% | $16 | $-16 | 689.72 |
| BTC | 2/9 | 22% | 33% | $31 | $-16 | 76,088 |
| ETH | 1/9 | 11% | 33% | $16 | $-31 | 2,238.01 |
| SOL | 0/9 | 0% | 0% | $0.00 | - | 89.33 |
| SUI | 0/9 | 0% | 11% | $0.00 | $-16 | 0.8415 |
| XRP | 0/9 | 0% | 11% | $0.00 | $-16 | 1.2072 |
| ZEC | 4/9 | 44% | 44% | $62 | - | 1,281.11 |

**Paper account: $981** (-1.93% since 2026-10-28, start $1,000) · invested $125.

Backtest on the candles the scan has (since 2024-02-11, 999 days, costs included): portfolio +27.0% a year, Sharpe 1.29, worst drop 17.2% · holding the same coins +50.9% a year, Sharpe 0.97, worst drop 51.5%.

## Paper account, last 30 days

| Day | Account | Day's result |
|---|---:|---:|
| 2026-11-05 | $981 | -1.12% |
| 2026-11-04 | $992 | +0.72% |
| 2026-11-03 | $985 | +0.51% |
| 2026-11-02 | $980 | -0.70% |
| 2026-11-01 | $987 | -0.02% |
| 2026-10-31 | $987 | -0.10% |
| 2026-10-30 | $988 | +0.25% |
| 2026-10-29 | $985 | -1.44% |
| 2026-10-28 | $1,000 | -0.02% |
