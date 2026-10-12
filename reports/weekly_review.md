# Weekly review · 2026-W42

Made 2026-10-12 04:22 UTC by the hourly scan (engine/weekly_review.py). Live = the program's 🔵 TEST setups (the GitHub record, no 5m check) and 🟡 PAPER signals, closed, after fees unless it says before fees. Promotion to PAPER needs the operator's tap; LIVE still needs the full pass bar and the approval line.

## System check

- ✅ nightly research ran on 7 of the last 7 days (last 2026-10-12)
- ✅ hourly scan: last run 2026-10-12 04:22 UTC
- ✅ program rotation: 48 of 48 strategy / timeframe tests re-tested in the last 7 days
- ✅ live watcher: last heartbeat 2026-10-12 02:50 UTC (33 min ago)
- ✅ TEST setups closed this week (GitHub record): 3

## Totals

- TEST: 3 closed setups since the start, -1.23R a trade; this week 3 (-3.69R)
- PAPER: 0 closed signals, - a trade; this week 0 (+0.00R)

## Promote to 🟡 PAPER (your tap)

None this week (each needs 10+ closed live TEST setups, positive after fees, and a positive backtest on that coin).

## In paper
- none

## With vs without the 5m check (before fees)

- watcher alerts (5m-confirmed): 1 plan results, -1.00R a trade
- every TEST setup (GitHub, no 5m check): 3, -1.07R a trade

## Ideas for new versions

- none yet (each needs 10+ live trades)

## Failure Lab (repairs for the loss causes)

- new repair TRD-H4-BREAKOUT-S3-FDISP: TRD-H4-BREAKOUT-S3@1.0 30m lost on false_breakout - testing DISP
- P02-EMA-PULLBACK-V4-S6-FHTF@1.0 4h (HTF for regime_mismatch): +0.04R vs parent +0.14R, unseen +0.11R vs +0.22R - did not help
- repair record: HTF helped 0 of 1

## ⚡ Shock alarm (sudden moves between candle closes, information only)

- no shock log on GitHub yet (the live watcher writes journal/shocks.csv; it needs journal sync)

## 🧭 Location at the entry (4H structure, information only)

- no closed setup with a recorded location yet (recorded from 2026-10-12)

## Every live strategy / version / coin

| Strategy | TF | Coin | Stage | Live | Win % | After fees | Before fees | This week | Backtest | Confidence |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P03-FIB-PULLBACK-V5 | 1h | SOL | TEST | 2 | 0 | -1.19R | -1.06R | 2 (-2.4R) | +0.04R | -1.19R over 2 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | TEST | 1 | 0 | -1.31R | -1.10R | 1 (-1.3R) | +0.01R | -1.31R over 1 trade: too early to say anything |
