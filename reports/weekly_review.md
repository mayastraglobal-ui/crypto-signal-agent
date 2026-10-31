# Weekly review · 2026-W44

Made 2026-10-31 12:46 UTC by the hourly scan (engine/weekly_review.py). Live = the program's 🔵 TEST setups (the GitHub record, no 5m check) and 🟡 PAPER signals, closed, after fees unless it says before fees. Promotion to PAPER needs the operator's tap; LIVE still needs the full pass bar and the approval line.

## System check

- ✅ nightly research ran on 7 of the last 7 days (last 2026-10-31)
- ✅ hourly scan: last run 2026-10-31 12:46 UTC
- ✅ program rotation: 93 of 93 strategy / timeframe tests re-tested in the last 7 days
- ✅ live watcher: last heartbeat 2026-10-31 10:50 UTC (27 min ago)
- ✅ TEST setups closed this week (GitHub record): 16

## Totals

- **Your alerts** (setups that could reach your Telegram): 6 closed since the start, -1.04R a trade; this week 1 (-0.84R)
- Silent research records (strategies NOT sent to you, kept to check the research): 47 closed, -0.64R a trade; this week 15 (-9.03R)
- TEST: 53 closed setups since the start, -0.68R a trade; this week 16 (-9.87R) (both groups)
- PAPER: 0 closed signals, - a trade; this week 0 (+0.00R)

## Promote to 🟡 PAPER (your tap)

None this week (each needs 10+ closed live TEST setups, positive after fees, and a positive backtest on that coin).

## In paper
- none

## With vs without the 5m check (before fees)

- watcher alerts (5m-confirmed): 3 plan results, -1.00R a trade
- every TEST setup (GitHub, no 5m check - your alerts and the silent records): 53, -0.60R a trade
- the same setups side by side (live watcher twins, `confirm_5m.compare_tfs`):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) -1.00R over 3 (plan results, before fees)

## 📈 Live track record and drift monitor

- **your alerts**: 3 closed, -0.99R a trade, -2.97R, worst drawdown 2.97R (after fees)
- silent research records: 47 closed, -0.64R a trade
- paused by the drift monitor: nothing
- the full table: reports/track_record.md

## Ideas for new versions

- none yet (each needs 10+ live trades)

## Failure Lab (repairs for the loss causes)

- P02-EMA-PULLBACK-V4-S6-FHTF@1.0 4h (HTF for regime_mismatch): +0.06R vs parent +0.16R, unseen +0.06R vs +0.16R - did not help
- TRD-H4-BREAKOUT-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.38R vs parent +0.17R, unseen +0.45R vs +0.35R - passed
- TRD-H4-BREAKOUT-FDISP@1.0 30m (DISP for false_breakout): +0.17R vs parent +0.10R, unseen +0.35R vs +0.26R - helped
- TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.36R vs parent +0.16R, unseen +0.47R vs +0.34R - passed
- TRD-H4-BREAKOUT-S3-FDISP@1.0 30m (DISP for false_breakout): +0.16R vs parent +0.03R, unseen +0.34R vs +0.21R - helped
- repair record: DISP helped 4 of 4, NOTEXT helped 2 of 2, HTF helped 0 of 1
- 2 repair(s) waiting for their first test

## ⚡ Shock alarm (sudden moves between candle closes, information only)

- 70 shock(s) this week, 51 sent to Telegram (the rest: over the daily cap, paused or /shock off)
- by kind: fast move 23, broke yesterday's high 6, broke yesterday's low 17, volume spike 40
- by coin: ETH 14, BTC 13, SOL 13, XRP 10, ZEC 8, SUI 7, BNB 5
- 4 hours later: 29 kept going, 41 reversed (average +0.06% in the shock's direction)
- followed by a strategy alert in the same direction within 4h: 4 of 70 - the strategies missed most shocks: material for the research (a reversal or sweep version)
-   2026-10-29 20:43 UTC BNB DOWN -5.3% -> 4h later +1.0% (no strategy alert)
-   2026-10-29 20:47 UTC SUI DOWN -5.2% -> 4h later +2.4% (no strategy alert)
-   2026-10-29 20:44 UTC ZEC DOWN -4.1% -> 4h later +2.7% (no strategy alert)
-   2026-10-30 00:19 UTC SUI DOWN -3.6% -> 4h later -5.5% (no strategy alert)
-   2026-10-29 20:47 UTC SOL DOWN -3.5% -> 4h later +2.3% (no strategy alert)

## 🧭 Location at the entry (4H structure, information only)

- middle of the 4H range: 4 setup(s), +0.03R a trade after fees, 1 won
- at a zone or edge against the direction: 35 setup(s), -0.60R a trade after fees, 7 won
- outside the 4H range (breakout): 14 setup(s), -1.06R a trade after fees, 0 won
- a difference counts only with 30+ setups in a group; then it is tested on 5 years before any rule

## Every live strategy / version / coin

| Strategy | TF | Coin | Stage | Sent to you | Live | Win % | After fees | Before fees | This week | Backtest | Confidence |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P01-BREAKOUT-V1 | 4h | BTC | TEST | ✅ yes | 2 | 0 | -0.96R | -0.88R | 1 (-0.8R) | +0.37R | -0.96R over 2 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | ETH | TEST | ✅ yes | 1 | 0 | -1.05R | -1.01R | 0 (+0.0R) | +0.25R | -1.05R over 1 trade: too early to say anything |
| P01-BREAKOUT-V4 | 4h | ETH | TEST | ✅ yes | 1 | 0 | -1.05R | -1.01R | 0 (+0.0R) | +0.22R | -1.05R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | TEST | ✅ yes | 1 | 0 | -1.11R | -1.03R | 0 (+0.0R) | +0.23R | -1.11R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | TEST | ✅ yes | 1 | 0 | -1.11R | -1.03R | 0 (+0.0R) | +0.41R | -1.11R over 1 trade: too early to say anything |
| P03-FIB-PULLBACK-V5 | 1h | SOL | TEST | silent | 7 | 29 | -0.35R | -0.25R | 1 (-1.2R) | +0.03R | -0.35R over 7 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | TEST | silent | 6 | 17 | -0.56R | -0.46R | 0 (+0.0R) | +0.01R | -0.56R over 6 trades: too early to say anything |
| P01-BREAKOUT-V5 | 30m | SUI | TEST | silent | 5 | 0 | -0.94R | -0.88R | 2 (-1.4R) | +0.01R | -0.94R over 5 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | SUI | TEST | silent | 4 | 0 | -0.91R | -0.88R | 4 (-3.6R) | +0.09R | -0.91R over 4 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | BTC | TEST | silent | 3 | 33 | -0.47R | -0.20R | 1 (+0.6R) | +0.07R | -0.47R over 3 trades: too early to say anything |
| P03-FIB-PULLBACK-V5 | 1h | SUI | TEST | silent | 3 | 33 | -0.40R | -0.35R | 0 (+0.0R) | +0.02R | -0.40R over 3 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | TEST | silent | 3 | 33 | -0.42R | -0.36R | 1 (+0.9R) | +0.01R | -0.42R over 3 trades: too early to say anything |
| P01-BREAKOUT-V2 | 1h | BTC | TEST | silent | 2 | 0 | -0.96R | -0.84R | 0 (+0.0R) | +0.11R | -0.96R over 2 trades: too early to say anything |
| P01-BREAKOUT-V2 | 30m | BTC | TEST | silent | 2 | 50 | +0.12R | +0.27R | 0 (+0.0R) | +0.07R | +0.12R over 2 trades: too early to say anything |
| P01-BREAKOUT-V2 | 30m | SOL | TEST | silent | 2 | 0 | -1.13R | -1.04R | 1 (-1.1R) | +0.06R | -1.13R over 2 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | ETH | TEST | silent | 2 | 0 | -0.74R | -0.68R | 0 (+0.0R) | +0.01R | -0.74R over 2 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | XRP | TEST | silent | 1 | 0 | -1.19R | -1.06R | 0 (+0.0R) | -0.01R | -1.19R over 1 trade: too early to say anything |
| P01-BREAKOUT-V2 | 1h | SOL | TEST | silent | 1 | 0 | -1.08R | -1.03R | 1 (-1.1R) | +0.03R | -1.08R over 1 trade: too early to say anything |
| P01-BREAKOUT-V5 | 1h | BTC | TEST | silent | 1 | 0 | -1.15R | -1.05R | 0 (+0.0R) | +0.02R | -1.15R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V1 | 4h | ZEC | TEST | silent | 1 | 0 | -1.02R | -1.01R | 1 (-1.0R) | +0.17R | -1.02R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 15m | ETH | TEST | silent | 1 | 0 | -0.96R | -0.86R | 1 (-1.0R) | +0.00R | -0.96R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | TEST | silent | 1 | 0 | -1.07R | -1.02R | 0 (+0.0R) | +0.02R | -1.07R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | TEST | silent | 1 | 100 | +0.89R | +0.98R | 1 (+0.9R) | +0.17R | +0.89R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V4 | 4h | ZEC | TEST | silent | 1 | 0 | -1.02R | -1.01R | 1 (-1.0R) | +0.28R | -1.02R over 1 trade: too early to say anything |
