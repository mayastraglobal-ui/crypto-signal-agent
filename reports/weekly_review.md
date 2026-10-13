# Weekly review · 2026-W42

Made 2026-10-13 00:32 UTC by the hourly scan (engine/weekly_review.py). Live = the program's 🔵 TEST setups (the GitHub record, no 5m check) and 🟡 PAPER signals, closed, after fees unless it says before fees. Promotion to PAPER needs the operator's tap; LIVE still needs the full pass bar and the approval line.

## System check

- ✅ nightly research ran on 6 of the last 7 days (last 2026-10-12)
- ✅ hourly scan: last run 2026-10-13 00:32 UTC
- ✅ program rotation: 48 of 48 strategy / timeframe tests re-tested in the last 7 days
- ✅ live watcher: last heartbeat 2026-10-12 23:15 UTC (6 min ago)
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

- 19 shock(s) this week, 12 sent to Telegram (the rest: over the daily cap, paused or /shock off)
- by kind: fast move 3, broke yesterday's high 4, broke yesterday's low 5, volume spike 12
- by coin: XRP 4, SOL 4, ETH 3, BTC 3, ZEC 3, SUI 2
- 4 hours later: 10 kept going, 9 reversed (average +0.24% in the shock's direction)
- followed by a strategy alert in the same direction within 4h: 0 of 19 - the strategies missed most shocks: material for the research (a reversal or sweep version)
-   2026-10-12 04:44 UTC ZEC UP +3.5% -> 4h later -2.1% (no strategy alert)
-   2026-10-12 04:36 UTC ZEC UP +1.7% -> 4h later +0.3% (no strategy alert)
-   2026-10-11 15:32 UTC SUI UP +1.4% -> 4h later +0.1% (no strategy alert)
-   2026-10-12 14:46 UTC SUI DOWN -1.4% -> 4h later +1.7% (no strategy alert)
-   2026-10-12 14:50 UTC XRP DOWN -1.2% -> 4h later +0.8% (no strategy alert)

## 🧭 Location at the entry (4H structure, information only)

- no closed setup with a recorded location yet (recorded from 2026-10-12)

## Every live strategy / version / coin

| Strategy | TF | Coin | Stage | Live | Win % | After fees | Before fees | This week | Backtest | Confidence |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P03-FIB-PULLBACK-V5 | 1h | SOL | TEST | 2 | 0 | -1.19R | -1.06R | 2 (-2.4R) | +0.04R | -1.19R over 2 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | TEST | 1 | 0 | -1.31R | -1.10R | 1 (-1.3R) | +0.01R | -1.31R over 1 trade: too early to say anything |
