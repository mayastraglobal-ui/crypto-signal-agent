# Trend portfolio (paper)

Daily close 2026-10-30 (updated 2026-10-31 00:42 UTC). 9 trend signals per coin (lookbacks 5, 10, 20, 30, 60, 90, 150, 250, 360 days): ON at a close above the lookback's high, OFF below its ratcheting mid-line. Target = the share ON. Long only, no leverage, equal parts. Paper only (`docs/TREND_PORTFOLIO.md`).

| Coin | Trends up | Target | Yesterday | Paper position | Change today | Price |
|---|---|---:|---:|---:|---:|---:|
| BNB | 2/9 | 22% | 22% | $31 | - | 704.42 |
| BTC | 2/9 | 22% | 22% | $31 | - | 77,368.8 |
| ETH | 1/9 | 11% | 11% | $16 | - | 2,245.54 |
| SOL | 1/9 | 11% | 11% | $16 | - | 96.38 |
| SUI | 0/9 | 0% | 0% | $0.00 | - | 0.9052 |
| XRP | 0/9 | 0% | 0% | $0.00 | - | 1.2567 |
| ZEC | 4/9 | 44% | 44% | $63 | - | 1,269.94 |

**Paper account: $988** (-1.21% since 2026-10-28, start $1,000) · invested $157.

Backtest on the candles the scan has (since 2024-02-05, 999 days, costs included): portfolio +28.8% a year, Sharpe 1.35, worst drop 17.2% · holding the same coins +56.4% a year, Sharpe 1.03, worst drop 51.5%.

## Paper account, last 30 days

| Day | Account | Day's result |
|---|---:|---:|
| 2026-10-30 | $988 | +0.25% |
| 2026-10-29 | $985 | -1.44% |
| 2026-10-28 | $1,000 | -0.02% |
