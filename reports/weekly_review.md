# Weekly review · 2026-W45

Made 2026-11-04 09:11 UTC by the hourly scan (engine/weekly_review.py). Live = the program's 🔵 TEST setups (the GitHub record, no 5m check) and 🟡 PAPER signals, closed, after fees unless it says before fees. Promotion to PAPER needs the operator's tap; LIVE still needs the full pass bar and the approval line.

## System check

- ✅ nightly research ran on 7 of the last 7 days (last 2026-11-04)
- ✅ hourly scan: last run 2026-11-04 09:11 UTC
- ✅ program rotation: 93 of 93 strategy / timeframe tests re-tested in the last 7 days
- ✅ live watcher: last heartbeat 2026-11-04 07:45 UTC (14 min ago)
- ✅ TEST setups closed this week (GitHub record): 16

## Totals

- **Your alerts** (setups that could reach your Telegram): 7 closed since the start, -1.04R a trade; this week 1 (-1.06R)
- Silent research records (strategies NOT sent to you, kept to check the research): 51 closed, -0.66R a trade; this week 15 (-14.10R)
- TEST: 58 closed setups since the start, -0.71R a trade; this week 16 (-15.16R) (both groups)
- PAPER: 0 closed signals, - a trade; this week 0 (+0.00R)

## Promote to 🟡 PAPER (your tap)

None this week (each needs 10+ closed live TEST setups, positive after fees, and a positive backtest on that coin).

## In paper
- none

## With vs without the 5m check (before fees)

- watcher alerts (5m-confirmed): 4 plan results, -1.00R a trade
- every TEST setup (GitHub, no 5m check - your alerts and the silent records): 58, -0.62R a trade
- the same setups side by side (live watcher twins, `confirm_5m.compare_tfs`):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) -1.00R over 4 (plan results, before fees)

## 📈 Live track record and drift monitor

- **your alerts**: 4 closed, -1.01R a trade, -4.02R, worst drawdown 4.02R (after fees)
- silent research records: 51 closed, -0.66R a trade
- paused by the drift monitor: nothing
- the full table: reports/track_record.md

## Ideas for new versions

- none yet (each needs 10+ live trades)

## Failure Lab (repairs for the loss causes)

- P01-BREAKOUT-V2-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.22R vs parent +0.02R, unseen +0.34R vs +0.11R - helped
- P02-EMA-PULLBACK-V4-S6-FHTF@1.0 4h (HTF for regime_mismatch): +0.02R vs parent +0.13R, unseen +0.07R vs +0.19R - did not help
- TRD-H4-BREAKOUT-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.41R vs parent +0.19R, unseen +0.49R vs +0.36R - passed
- TRD-H4-BREAKOUT-FDISP@1.0 30m (DISP for false_breakout): +0.19R vs parent +0.10R, unseen +0.36R vs +0.25R - helped
- TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.40R vs parent +0.19R, unseen +0.55R vs +0.35R - passed
- repair record: DISP helped 5 of 6, NOTEXT helped 3 of 3, HTF helped 0 of 1
- 2 repair(s) waiting for their first test

## ⚡ Shock alarm (sudden moves between candle closes, information only)

- 72 shock(s) this week, 49 sent to Telegram (the rest: over the daily cap, paused or /shock off)
- by kind: fast move 25, broke yesterday's high 5, broke yesterday's low 19, volume spike 39
- by coin: ETH 15, SOL 14, XRP 11, ZEC 11, BTC 10, SUI 6, BNB 5
- 4 hours later: 33 kept going, 39 reversed (average -0.09% in the shock's direction)
- followed by a strategy alert in the same direction within 4h: 2 of 72 - the strategies missed most shocks: material for the research (a reversal or sweep version)
-   2026-10-29 20:43 UTC BNB DOWN -5.3% -> 4h later +1.0% (no strategy alert)
-   2026-10-29 20:47 UTC SUI DOWN -5.2% -> 4h later +2.4% (no strategy alert)
-   2026-10-29 20:44 UTC ZEC DOWN -4.1% -> 4h later +2.7% (no strategy alert)
-   2026-10-30 00:19 UTC SUI DOWN -3.6% -> 4h later -5.5% (no strategy alert)
-   2026-10-29 20:47 UTC SOL DOWN -3.5% -> 4h later +2.3% (no strategy alert)

## 🧭 Location at the entry (4H structure, information only)

- middle of the 4H range: 4 setup(s), +0.03R a trade after fees, 1 won
- at a zone or edge against the direction: 37 setup(s), -0.63R a trade after fees, 7 won
- outside the 4H range (breakout): 17 setup(s), -1.03R a trade after fees, 0 won
- a difference counts only with 30+ setups in a group; then it is tested on 5 years before any rule

## Every live strategy / version / coin

| Strategy | TF | Coin | Stage | Sent to you | Live | Win % | After fees | Before fees | This week | Backtest | Confidence |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P01-BREAKOUT-V1 | 4h | BTC | TEST | ✅ yes | 2 | 0 | -0.96R | -0.88R | 0 (+0.0R) | +0.36R | -0.96R over 2 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | ETH | TEST | ✅ yes | 1 | 0 | -1.05R | -1.01R | 0 (+0.0R) | +0.25R | -1.05R over 1 trade: too early to say anything |
| P01-BREAKOUT-V4 | 4h | ETH | TEST | ✅ yes | 1 | 0 | -1.05R | -1.01R | 0 (+0.0R) | +0.22R | -1.05R over 1 trade: too early to say anything |
| P05-RANGE-REVERSAL-V4 | 4h | SOL | TEST | ✅ yes | 1 | 0 | -1.06R | -1.01R | 1 (-1.1R) | +0.24R | -1.06R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | TEST | ✅ yes | 1 | 0 | -1.11R | -1.03R | 0 (+0.0R) | +0.23R | -1.11R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | TEST | ✅ yes | 1 | 0 | -1.11R | -1.03R | 0 (+0.0R) | +0.41R | -1.11R over 1 trade: too early to say anything |
| P03-FIB-PULLBACK-V5 | 1h | SOL | TEST | silent | 7 | 29 | -0.35R | -0.25R | 0 (+0.0R) | +0.04R | -0.35R over 7 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | TEST | silent | 6 | 17 | -0.56R | -0.46R | 0 (+0.0R) | +0.02R | -0.56R over 6 trades: too early to say anything |
| P01-BREAKOUT-V5 | 30m | SUI | TEST | silent | 5 | 0 | -0.94R | -0.88R | 2 (-1.4R) | +0.00R | -0.94R over 5 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | SUI | TEST | silent | 4 | 0 | -0.91R | -0.88R | 4 (-3.6R) | +0.08R | -0.91R over 4 trades: too early to say anything |
| P03-FIB-PULLBACK-V5 | 1h | SUI | TEST | silent | 4 | 25 | -0.57R | -0.52R | 1 (-1.1R) | +0.02R | -0.57R over 4 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | BTC | TEST | silent | 3 | 33 | -0.47R | -0.20R | 0 (+0.0R) | +0.07R | -0.47R over 3 trades: too early to say anything |
| P01-BREAKOUT-V2 | 30m | SOL | TEST | silent | 3 | 0 | -1.16R | -1.05R | 2 (-2.3R) | +0.06R | -1.16R over 3 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | TEST | silent | 3 | 33 | -0.42R | -0.36R | 0 (+0.0R) | +0.01R | -0.42R over 3 trades: too early to say anything |
| P01-BREAKOUT-V2 | 1h | BTC | TEST | silent | 2 | 0 | -0.96R | -0.84R | 0 (+0.0R) | +0.11R | -0.96R over 2 trades: too early to say anything |
| P01-BREAKOUT-V2 | 30m | BTC | TEST | silent | 2 | 50 | +0.12R | +0.27R | 0 (+0.0R) | +0.07R | +0.12R over 2 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | ETH | TEST | silent | 2 | 0 | -0.74R | -0.68R | 0 (+0.0R) | +0.01R | -0.74R over 2 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | XRP | TEST | silent | 1 | 0 | -1.19R | -1.06R | 0 (+0.0R) | -0.01R | -1.19R over 1 trade: too early to say anything |
| P01-BREAKOUT-V2 | 1h | SOL | TEST | silent | 1 | 0 | -1.08R | -1.03R | 1 (-1.1R) | +0.03R | -1.08R over 1 trade: too early to say anything |
| P01-BREAKOUT-V2 | 30m | SUI | TEST | silent | 1 | 0 | -1.09R | -1.03R | 1 (-1.1R) | +0.09R | -1.09R over 1 trade: too early to say anything |
| P01-BREAKOUT-V5 | 1h | BTC | TEST | silent | 1 | 0 | -1.15R | -1.05R | 0 (+0.0R) | +0.02R | -1.15R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V1 | 4h | ZEC | TEST | silent | 1 | 0 | -1.02R | -1.01R | 1 (-1.0R) | +0.14R | -1.02R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 15m | ETH | TEST | silent | 1 | 0 | -0.96R | -0.86R | 1 (-1.0R) | +0.00R | -0.96R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | TEST | silent | 1 | 0 | -1.07R | -1.02R | 0 (+0.0R) | +0.02R | -1.07R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | TEST | silent | 1 | 100 | +0.89R | +0.98R | 0 (+0.0R) | +0.16R | +0.89R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V4 | 4h | ZEC | TEST | silent | 1 | 0 | -1.02R | -1.01R | 1 (-1.0R) | +0.25R | -1.02R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V5 | 1h | ZEC | TEST | silent | 1 | 0 | -0.49R | -0.46R | 1 (-0.5R) | +0.03R | -0.49R over 1 trade: too early to say anything |
