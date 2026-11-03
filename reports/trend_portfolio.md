# Trend portfolio (paper)

Daily close 2026-11-02 (updated 2026-11-03 00:05 UTC). 9 trend signals per coin (lookbacks 5, 10, 20, 30, 60, 90, 150, 250, 360 days): ON at a close above the lookback's high, OFF below its ratcheting mid-line. Target = the share ON. Long only, no leverage, equal parts. Paper only (`docs/TREND_PORTFOLIO.md`).

| Coin | Trends up | Target | Yesterday | Paper position | Change today | Price |
|---|---|---:|---:|---:|---:|---:|
| BNB | 2/9 | 22% | 22% | $31 | - | 699.25 |
| BTC | 2/9 | 22% | 22% | $31 | - | 76,816 |
| ETH | 1/9 | 11% | 11% | $16 | - | 2,253.29 |
| SOL | 0/9 | 0% | 11% | $0.00 | $-16 | 91.98 |
| SUI | 0/9 | 0% | 0% | $0.00 | - | 0.8729 |
| XRP | 0/9 | 0% | 0% | $0.00 | - | 1.2502 |
| ZEC | 4/9 | 44% | 44% | $62 | - | 1,134.55 |

**Paper account: $980** (-2.02% since 2026-10-28, start $1,000) · invested $140.

Backtest on the candles the scan has (since 2024-02-08, 999 days, costs included): portfolio +27.4% a year, Sharpe 1.3, worst drop 17.2% · holding the same coins +53.0% a year, Sharpe 1.0, worst drop 51.5%.

## Paper account, last 30 days

| Day | Account | Day's result |
|---|---:|---:|
| 2026-11-02 | $980 | -0.70% |
| 2026-11-01 | $987 | -0.02% |
| 2026-10-31 | $987 | -0.10% |
| 2026-10-30 | $988 | +0.25% |
| 2026-10-29 | $985 | -1.44% |
| 2026-10-28 | $1,000 | -0.02% |
