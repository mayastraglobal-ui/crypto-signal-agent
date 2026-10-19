# Weekly review · 2026-W43

Made 2026-10-19 17:30 UTC by the hourly scan (engine/weekly_review.py). Live = the program's 🔵 TEST setups (the GitHub record, no 5m check) and 🟡 PAPER signals, closed, after fees unless it says before fees. Promotion to PAPER needs the operator's tap; LIVE still needs the full pass bar and the approval line.

## System check

- ✅ nightly research ran on 7 of the last 7 days (last 2026-10-19)
- ✅ hourly scan: last run 2026-10-19 17:30 UTC
- ✅ program rotation: 89 of 89 strategy / timeframe tests re-tested in the last 7 days
- ✅ live watcher: last heartbeat 2026-10-19 16:20 UTC (15 min ago)
- ✅ TEST setups closed this week (GitHub record): 23

## Totals

- **Your alerts** (setups that could reach your Telegram): 2 closed since the start, -1.05R a trade; this week 2 (-2.10R)
- Silent research records (strategies NOT sent to you, kept to check the research): 24 closed, -0.62R a trade; this week 21 (-11.29R)
- TEST: 26 closed setups since the start, -0.66R a trade; this week 23 (-13.39R) (both groups)
- PAPER: 0 closed signals, - a trade; this week 0 (+0.00R)

## Promote to 🟡 PAPER (your tap)

None this week (each needs 10+ closed live TEST setups, positive after fees, and a positive backtest on that coin).

## In paper
- none

## With vs without the 5m check (before fees)

- watcher alerts (5m-confirmed): 2 plan results, -1.00R a trade
- every TEST setup (GitHub, no 5m check - your alerts and the silent records): 26, -0.58R a trade
- the same setups side by side (live watcher twins, `confirm_5m.compare_tfs`):
  - 4h: every setup without the 5m check -1.00R over 1 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 1 · alerts sent (5m entry) none yet (plan results, before fees)

## 📈 Live track record and drift monitor

- **your alerts**: 1 closed, -1.05R a trade, -1.05R, worst drawdown 1.05R (after fees)
- silent research records: 24 closed, -0.62R a trade
- paused by the drift monitor: nothing
- the full table: reports/track_record.md

## Ideas for new versions

- none yet (each needs 10+ live trades)

## Failure Lab (repairs for the loss causes)

- new repair TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT: TRD-H4-BREAKOUT-S3-FDISP@1.0 30m lost on overextended_entry - testing NOTEXT
- P02-EMA-PULLBACK-V4-S6-FHTF@1.0 4h (HTF for regime_mismatch): +0.04R vs parent +0.14R, unseen +0.11R vs +0.22R - did not help
- TRD-H4-BREAKOUT-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.41R vs parent +0.19R, unseen +0.49R vs +0.38R - passed
- TRD-H4-BREAKOUT-FDISP@1.0 30m (DISP for false_breakout): +0.19R vs parent +0.10R, unseen +0.38R vs +0.26R - helped
- TRD-H4-BREAKOUT-S3-FDISP@1.0 30m (DISP for false_breakout): +0.19R vs parent +0.01R, unseen +0.36R vs +0.19R - helped
- repair record: DISP helped 2 of 2, HTF helped 0 of 1, NOTEXT helped 1 of 1

## ⚡ Shock alarm (sudden moves between candle closes, information only)

- 72 shock(s) this week, 57 sent to Telegram (the rest: over the daily cap, paused or /shock off)
- by kind: fast move 31, broke yesterday's high 7, broke yesterday's low 14, volume spike 35
- by coin: ETH 15, BTC 15, XRP 12, ZEC 11, SOL 10, SUI 9
- 4 hours later: 36 kept going, 36 reversed (average -0.17% in the shock's direction)
- followed by a strategy alert in the same direction within 4h: 2 of 72 - the strategies missed most shocks: material for the research (a reversal or sweep version)
-   2026-10-15 02:29 UTC ETH DOWN -3.6% -> 4h later -1.4% (no strategy alert)
-   2026-10-15 02:25 UTC SUI DOWN -3.5% -> 4h later -0.6% (no strategy alert)
-   2026-10-14 12:31 UTC SUI DOWN -3.3% -> 4h later +1.1% (no strategy alert)
-   2026-10-12 21:46 UTC ZEC DOWN -3.2% -> 4h later +1.4% (no strategy alert)
-   2026-10-16 16:52 UTC ZEC DOWN -3.0% -> 4h later +0.3% (no strategy alert)

## 🧭 Location at the entry (4H structure, information only)

- middle of the 4H range: 1 setup(s), +2.42R a trade after fees, 1 won
- at a zone or edge against the direction: 12 setup(s), -0.41R a trade after fees, 3 won
- outside the 4H range (breakout): 10 setup(s), -1.08R a trade after fees, 0 won
- a difference counts only with 30+ setups in a group; then it is tested on 5 years before any rule

## Every live strategy / version / coin

| Strategy | TF | Coin | Stage | Sent to you | Live | Win % | After fees | Before fees | This week | Backtest | Confidence |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P01-BREAKOUT-V1 | 4h | ETH | TEST | ✅ yes | 1 | 0 | -1.05R | -1.01R | 1 (-1.1R) | +0.25R | -1.05R over 1 trade: too early to say anything |
| P01-BREAKOUT-V4 | 4h | ETH | TEST | ✅ yes | 1 | 0 | -1.05R | -1.01R | 1 (-1.1R) | +0.22R | -1.05R over 1 trade: too early to say anything |
| P03-FIB-PULLBACK-V5 | 1h | SOL | TEST | silent | 6 | 33 | -0.20R | -0.12R | 4 (+1.1R) | +0.04R | -0.20R over 6 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | TEST | silent | 5 | 20 | -0.44R | -0.34R | 4 (-0.9R) | +0.01R | -0.44R over 5 trades: too early to say anything |
| P03-FIB-PULLBACK-V5 | 1h | SUI | TEST | silent | 3 | 33 | -0.40R | -0.35R | 3 (-1.2R) | +0.01R | -0.40R over 3 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | ETH | TEST | silent | 2 | 0 | -0.74R | -0.68R | 2 (-1.5R) | +0.01R | -0.74R over 2 trades: too early to say anything |
| P01-BREAKOUT-V5 | 30m | SUI | TEST | silent | 2 | 0 | -1.09R | -1.03R | 2 (-2.2R) | +0.02R | -1.09R over 2 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | TEST | silent | 2 | 0 | -1.08R | -1.03R | 2 (-2.2R) | +0.01R | -1.08R over 2 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | XRP | TEST | silent | 1 | 0 | -1.19R | -1.06R | 1 (-1.2R) | +0.00R | -1.19R over 1 trade: too early to say anything |
| P01-BREAKOUT-V2 | 30m | SOL | TEST | silent | 1 | 0 | -1.14R | -1.05R | 1 (-1.1R) | +0.07R | -1.14R over 1 trade: too early to say anything |
| P01-BREAKOUT-V5 | 1h | BTC | TEST | silent | 1 | 0 | -1.15R | -1.05R | 1 (-1.1R) | +0.02R | -1.15R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | TEST | silent | 1 | 0 | -1.07R | -1.02R | 1 (-1.1R) | +0.02R | -1.07R over 1 trade: too early to say anything |
