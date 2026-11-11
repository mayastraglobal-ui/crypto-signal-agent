# Weekly review · 2026-W46

Made 2026-11-11 06:49 UTC by the hourly scan (engine/weekly_review.py). Live = the program's 🔵 TEST setups (the GitHub record, no 5m check) and 🟡 PAPER signals, closed, after fees unless it says before fees. Promotion to PAPER needs the operator's tap; LIVE still needs the full pass bar and the approval line.

## System check

- ✅ nightly research ran on 6 of the last 7 days (last 2026-11-10)
- ✅ hourly scan: last run 2026-11-11 06:49 UTC
- ✅ program rotation: 93 of 93 strategy / timeframe tests re-tested in the last 7 days
- ⚠️ live watcher SILENT: no heartbeat for 57h47m (last 2026-11-08 20:10 UTC) - the PC may be off, asleep or offline
- ✅ TEST setups closed this week (GitHub record): 20

## Totals

- **Your alerts** (setups that could reach your Telegram): 12 closed since the start, -0.75R a trade; this week 5 (-1.69R)
- Silent research records (strategies NOT sent to you, kept to check the research): 66 closed, -0.48R a trade; this week 15 (+2.30R)
- TEST: 78 closed setups since the start, -0.52R a trade; this week 20 (+0.61R) (both groups)
- PAPER: 0 closed signals, - a trade; this week 0 (+0.00R)

## Promote to 🟡 PAPER (your tap)

None this week (each needs 10+ closed live TEST setups, positive after fees, and a positive backtest on that coin).

## In paper
- none

## With vs without the 5m check (before fees)

- watcher alerts (5m-confirmed): 5 plan results, -1.00R a trade
- every TEST setup (GitHub, no 5m check - your alerts and the silent records): 78, -0.44R a trade
- the same setups side by side (live watcher twins, `confirm_5m.compare_tfs`):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) -1.00R over 5 (plan results, before fees)

## 📈 Live track record and drift monitor

- **your alerts**: 9 closed, -0.64R a trade, -5.72R, worst drawdown 7.15R (after fees)
- silent research records: 66 closed, -0.48R a trade
- paused by the drift monitor: nothing
- the full table: reports/track_record.md

## Ideas for new versions

- none yet (each needs 10+ live trades)

## Failure Lab (repairs for the loss causes)

- new repair donchian_breakout-VEXIT-S4-FDISP-FNOTEXT: donchian_breakout-VEXIT-S4-FDISP@1.0 30m lost on overextended_entry - testing NOTEXT
- P01-BREAKOUT-V2-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.24R vs parent +0.02R, unseen +0.37R vs +0.10R - helped
- P02-EMA-PULLBACK-V4-S6-FHTF@1.0 4h (HTF for regime_mismatch): +0.02R vs parent +0.13R, unseen +0.07R vs +0.19R - did not help
- P11-MOMENTUM-V1-FRETEST-FDISP@1.0 30m (DISP for false_breakout): -0.09R vs parent -0.10R, unseen -0.15R vs -0.15R - did not help
- TRD-H4-BREAKOUT-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.41R vs parent +0.19R, unseen +0.49R vs +0.42R - passed
- TRD-H4-BREAKOUT-FDISP@1.0 30m (DISP for false_breakout): +0.19R vs parent +0.10R, unseen +0.42R vs +0.27R - helped
- repair record: DISP helped 7 of 9, NOTEXT helped 3 of 3, HTF helped 0 of 1
- 1 repair(s) waiting for their first test

## ⚡ Shock alarm (sudden moves between candle closes, information only)

- 49 shock(s) this week, 27 sent to Telegram (the rest: over the daily cap, paused or /shock off)
- by kind: fast move 20, broke yesterday's high 2, broke yesterday's low 5, volume spike 33
- by coin: BTC 10, ETH 9, SOL 9, XRP 6, SUI 6, ZEC 6, BNB 3
- 4 hours later: 24 kept going, 25 reversed (average +0.67% in the shock's direction)
- followed by a strategy alert in the same direction within 4h: 4 of 49 - the strategies missed most shocks: material for the research (a reversal or sweep version)
-   2026-11-06 14:39 UTC ZEC UP +3.6% -> 4h later -0.2% (no strategy alert)
-   2026-11-05 16:20 UTC ZEC UP +3.6% -> 4h later -3.2% (no strategy alert)
-   2026-11-05 15:12 UTC ZEC DOWN -3.1% -> 4h later +0.3% (no strategy alert)
-   2026-11-06 12:28 UTC ZEC UP +3.0% -> 4h later +2.3% (no strategy alert)
-   2026-11-04 15:14 UTC SOL UP +2.8% -> 4h later -2.4% (no strategy alert)

## 🧭 Location at the entry (4H structure, information only)

- middle of the 4H range: 4 setup(s), +0.03R a trade after fees, 1 won
- at a zone or edge against the direction: 55 setup(s), -0.43R a trade after fees, 14 won
- outside the 4H range (breakout): 19 setup(s), -0.86R a trade after fees, 1 won
- a difference counts only with 30+ setups in a group; then it is tested on 5 years before any rule

## Every live strategy / version / coin

| Strategy | TF | Coin | Stage | Sent to you | Live | Win % | After fees | Before fees | This week | Backtest | Confidence |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| TRD-H4-BREAKOUT-S3 | 1h | XRP | TEST | ✅ yes | 3 | 0 | -1.05R | -1.02R | 3 (-3.1R) | +0.28R | -1.05R over 3 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | BTC | TEST | ✅ yes | 2 | 0 | -0.96R | -0.88R | 0 (+0.0R) | +0.36R | -0.96R over 2 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | ETH | TEST | ✅ yes | 1 | 0 | -1.05R | -1.01R | 0 (+0.0R) | +0.25R | -1.05R over 1 trade: too early to say anything |
| P01-BREAKOUT-V4 | 4h | ETH | TEST | ✅ yes | 1 | 0 | -1.05R | -1.01R | 0 (+0.0R) | +0.22R | -1.05R over 1 trade: too early to say anything |
| P05-RANGE-REVERSAL-V4 | 4h | SOL | TEST | ✅ yes | 1 | 0 | -1.06R | -1.01R | 0 (+0.0R) | +0.24R | -1.06R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | TEST | ✅ yes | 1 | 0 | -1.11R | -1.03R | 0 (+0.0R) | +0.23R | -1.11R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V3 | 4h | XRP | TEST | ✅ yes | 1 | 100 | +2.47R | +2.50R | 1 (+2.5R) | +0.18R | +2.47R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | TEST | ✅ yes | 1 | 0 | -1.11R | -1.03R | 0 (+0.0R) | +0.41R | -1.11R over 1 trade: too early to say anything |
| P12-LEADER-V1 | 4h | ZEC | TEST | ✅ yes | 1 | 0 | -1.02R | -1.01R | 1 (-1.0R) | +0.41R | -1.02R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | TEST | silent | 10 | 20 | -0.48R | -0.39R | 4 (-1.5R) | +0.01R | -0.48R over 10 trades: not working so far |
| P03-FIB-PULLBACK-V5 | 1h | SOL | TEST | silent | 9 | 33 | -0.13R | -0.04R | 2 (+1.3R) | +0.04R | -0.13R over 9 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | SUI | TEST | silent | 5 | 0 | -0.81R | -0.78R | 1 (-0.4R) | +0.08R | -0.81R over 5 trades: too early to say anything |
| P01-BREAKOUT-V5 | 30m | SUI | TEST | silent | 5 | 0 | -0.94R | -0.88R | 0 (+0.0R) | +0.00R | -0.94R over 5 trades: too early to say anything |
| P01-BREAKOUT-V2 | 30m | SOL | TEST | silent | 4 | 0 | -1.18R | -1.06R | 1 (-1.2R) | +0.05R | -1.18R over 4 trades: too early to say anything |
| P03-FIB-PULLBACK-V5 | 1h | SUI | TEST | silent | 4 | 25 | -0.57R | -0.52R | 0 (+0.0R) | +0.01R | -0.57R over 4 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | BTC | TEST | silent | 3 | 33 | -0.47R | -0.20R | 0 (+0.0R) | +0.06R | -0.47R over 3 trades: too early to say anything |
| P01-BREAKOUT-V2 | 1h | BTC | TEST | silent | 3 | 33 | -0.61R | -0.50R | 1 (+0.1R) | +0.11R | -0.61R over 3 trades: too early to say anything |
| P01-BREAKOUT-V2 | 30m | BTC | TEST | silent | 3 | 33 | +0.00R | +0.13R | 1 (-0.2R) | +0.07R | +0.00R over 3 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | TEST | silent | 3 | 33 | -0.42R | -0.36R | 0 (+0.0R) | +0.01R | -0.42R over 3 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | ETH | TEST | silent | 2 | 0 | -0.74R | -0.68R | 0 (+0.0R) | +0.01R | -0.74R over 2 trades: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | TEST | silent | 2 | 50 | +0.69R | +0.74R | 1 (+2.4R) | +0.03R | +0.69R over 2 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | XRP | TEST | silent | 1 | 0 | -1.19R | -1.06R | 0 (+0.0R) | -0.01R | -1.19R over 1 trade: too early to say anything |
| P01-BREAKOUT-V2 | 1h | SOL | TEST | silent | 1 | 0 | -1.08R | -1.03R | 0 (+0.0R) | +0.02R | -1.08R over 1 trade: too early to say anything |
| P01-BREAKOUT-V2 | 30m | SUI | TEST | silent | 1 | 0 | -1.09R | -1.03R | 0 (+0.0R) | +0.08R | -1.09R over 1 trade: too early to say anything |
| P01-BREAKOUT-V5 | 1h | BTC | TEST | silent | 1 | 0 | -1.15R | -1.05R | 0 (+0.0R) | +0.02R | -1.15R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V1 | 4h | ZEC | TEST | silent | 1 | 0 | -1.02R | -1.01R | 0 (+0.0R) | +0.14R | -1.02R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 15m | ETH | TEST | silent | 1 | 0 | -0.96R | -0.86R | 0 (+0.0R) | +0.00R | -0.96R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | TEST | silent | 1 | 100 | +0.89R | +0.98R | 0 (+0.0R) | +0.17R | +0.89R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 30m | XRP | TEST | silent | 1 | 100 | +0.85R | +0.99R | 1 (+0.8R) | +0.14R | +0.85R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V4 | 4h | ZEC | TEST | silent | 1 | 0 | -1.02R | -1.01R | 0 (+0.0R) | +0.25R | -1.02R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V2 | 30m | ETH | TEST | silent | 1 | 100 | +0.55R | +0.63R | 1 (+0.6R) | +0.07R | +0.55R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V5 | 1h | ZEC | TEST | silent | 1 | 0 | -0.49R | -0.46R | 0 (+0.0R) | +0.03R | -0.49R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V3 | 1h | SOL | TEST | silent | 1 | 100 | +1.53R | +1.58R | 1 (+1.5R) | +0.11R | +1.53R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V4 | 1h | XRP | TEST | silent | 1 | 0 | -1.07R | -1.03R | 1 (-1.1R) | +0.07R | -1.07R over 1 trade: too early to say anything |
