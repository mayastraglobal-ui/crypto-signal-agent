# Weekly review · 2026-W42

Made 2026-10-15 05:30 UTC by the hourly scan (engine/weekly_review.py). Live = the program's 🔵 TEST setups (the GitHub record, no 5m check) and 🟡 PAPER signals, closed, after fees unless it says before fees. Promotion to PAPER needs the operator's tap; LIVE still needs the full pass bar and the approval line.

## System check

- ✅ nightly research ran on 7 of the last 7 days (last 2026-10-15)
- ✅ hourly scan: last run 2026-10-15 05:30 UTC
- ✅ program rotation: 89 of 89 strategy / timeframe tests re-tested in the last 7 days
- ✅ live watcher: last heartbeat 2026-10-15 04:25 UTC (7 min ago)
- ✅ TEST setups closed this week (GitHub record): 7

## Totals

- TEST: 7 closed setups since the start, -0.66R a trade; this week 7 (-4.61R)
- PAPER: 0 closed signals, - a trade; this week 0 (+0.00R)

## Promote to 🟡 PAPER (your tap)

None this week (each needs 10+ closed live TEST setups, positive after fees, and a positive backtest on that coin).

## In paper
- none

## With vs without the 5m check (before fees)

- watcher alerts (5m-confirmed): 2 plan results, -1.00R a trade
- every TEST setup (GitHub, no 5m check): 7, -0.55R a trade
- the same setups side by side (live watcher twins, `confirm_5m.compare_tfs`):
  - none yet (each 4H setup that waits for its 5m candle adds one)

## 📈 Live track record and drift monitor

- every live setup: 7 closed, -0.66R a trade, -4.61R, worst drawdown 5.94R (after fees)
- paused by the drift monitor: nothing
- the full table: reports/track_record.md

## Ideas for new versions

- none yet (each needs 10+ live trades)

## Failure Lab (repairs for the loss causes)

- P02-EMA-PULLBACK-V4-S6-FHTF@1.0 4h (HTF for regime_mismatch): +0.04R vs parent +0.14R, unseen +0.11R vs +0.22R - did not help
- TRD-H4-BREAKOUT-FDISP@1.0 30m (DISP for false_breakout): +0.19R vs parent +0.10R, unseen +0.38R vs +0.26R - helped
- TRD-H4-BREAKOUT-S3-FDISP@1.0 30m (DISP for false_breakout): +0.19R vs parent +0.01R, unseen +0.36R vs +0.19R - helped
- repair record: DISP helped 2 of 2, HTF helped 0 of 1

## ⚡ Shock alarm (sudden moves between candle closes, information only)

- 41 shock(s) this week, 31 sent to Telegram (the rest: over the daily cap, paused or /shock off)
- by kind: fast move 14, broke yesterday's high 6, broke yesterday's low 9, volume spike 26
- by coin: ETH 9, SOL 8, BTC 7, ZEC 7, XRP 6, SUI 4
- 4 hours later: 22 kept going, 19 reversed (average +0.12% in the shock's direction)
- followed by a strategy alert in the same direction within 4h: 2 of 41 - the strategies missed most shocks: material for the research (a reversal or sweep version)
-   2026-10-12 04:44 UTC ZEC UP +3.5% -> 4h later -2.1% (no strategy alert)
-   2026-10-14 12:31 UTC SUI DOWN -3.3% -> 4h later +1.1% (no strategy alert)
-   2026-10-12 21:46 UTC ZEC DOWN -3.2% -> 4h later +1.4% (no strategy alert)
-   2026-10-12 21:46 UTC SUI DOWN -2.4% -> 4h later +1.5% (no strategy alert)
-   2026-10-14 01:50 UTC ZEC UP +2.3% -> 4h later -2.0% (no strategy alert)

## 🧭 Location at the entry (4H structure, information only)

- middle of the 4H range: 1 setup(s), +2.42R a trade after fees, 1 won
- at a zone or edge against the direction: 1 setup(s), -1.09R a trade after fees, 0 won
- outside the 4H range (breakout): 2 setup(s), -1.13R a trade after fees, 0 won
- a difference counts only with 30+ setups in a group; then it is tested on 5 years before any rule

## Every live strategy / version / coin

| Strategy | TF | Coin | Stage | Live | Win % | After fees | Before fees | This week | Backtest | Confidence |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P03-FIB-PULLBACK-V5 | 1h | SOL | TEST | 3 | 33 | +0.01R | +0.13R | 3 (+0.0R) | +0.04R | +0.01R over 3 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | TEST | 2 | 0 | -1.20R | -1.06R | 2 (-2.4R) | +0.01R | -1.20R over 2 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | BTC | TEST | 1 | 0 | -1.15R | -1.05R | 1 (-1.1R) | +0.02R | -1.15R over 1 trade: too early to say anything |
| P01-BREAKOUT-V5 | 1h | ETH | TEST | 1 | 0 | -1.10R | -1.03R | 1 (-1.1R) | +0.01R | -1.10R over 1 trade: too early to say anything |
