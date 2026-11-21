# Weekly review · 2026-W47

Made 2026-11-21 06:16 UTC by the hourly scan (engine/weekly_review.py). Live = the program's 🔵 TEST setups (the GitHub record, no 5m check) and 🟡 PAPER signals, closed, after fees unless it says before fees. Promotion to PAPER needs the operator's tap; LIVE still needs the full pass bar and the approval line.

## System check

- ✅ nightly research ran on 6 of the last 7 days (last 2026-11-20)
- ✅ hourly scan: last run 2026-11-21 06:16 UTC
- ✅ program rotation: 93 of 93 strategy / timeframe tests re-tested in the last 7 days
- ✅ live watcher: last heartbeat 2026-11-21 05:01 UTC (11 min ago)
- ✅ TEST setups closed this week (GitHub record): 86

## Totals

- **Your alerts** (setups that could reach your Telegram): 32 closed since the start, +0.93R a trade; this week 20 (+31.65R)
- Silent research records (strategies NOT sent to you, kept to check the research): 164 closed, +0.03R a trade; this week 67 (+39.19R)
- TEST: 195 closed setups since the start, +0.17R a trade; this week 86 (+68.37R) (both groups)
- PAPER: 1 closed signals, +2.47R a trade; this week 1 (+2.47R)

## Promote to 🟡 PAPER (your tap)

1. TRD-H4-BREAKOUT-S3 1.0 1h on ETH - 10 live TEST setups, +0.36R a trade after fees (40% won); 5-year backtest on ETH +0.06R over 207 trades. +0.36R over 10 trades: still uncertain - could be luck.

## In paper
- P03-FIB-PULLBACK-V5@1.0 1h on SOL
- TRD-H4-BREAKOUT-S3@1.0 1h on BTC

## With vs without the 5m check (before fees)

- watcher alerts (5m-confirmed): 16 plan results, +1.22R a trade
- every TEST setup (GitHub, no 5m check - your alerts and the silent records): 195, +0.22R a trade
- the same setups side by side (live watcher twins, `confirm_5m.compare_tfs`):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) +1.40R over 29 (plan results, before fees)

## 📈 Live track record and drift monitor

- **your alerts**: 36 closed, +0.77R a trade, +27.77R, worst drawdown 5.05R (after fees)
- silent research records: 164 closed, +0.03R a trade
- paused by the drift monitor: nothing
- the full table: reports/track_record.md

## Ideas for new versions

- none yet (each needs 10+ live trades)

## Failure Lab (repairs for the loss causes)

- P01-BREAKOUT-V2-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.29R vs parent +0.04R, unseen +0.46R vs +0.16R - helped
- P01-BREAKOUT-V2-FDISP-FRETEST@1.0 30m (RETEST for overextended_entry): +0.14R vs parent +0.04R, unseen +0.27R vs +0.16R - helped
- P02-EMA-PULLBACK-V4-S6-FHTF@1.0 4h (HTF for regime_mismatch): +0.02R vs parent +0.14R, unseen +0.09R vs +0.23R - did not help
- P11-MOMENTUM-V1-FRETEST-FDISP@1.0 30m (DISP for false_breakout): -0.09R vs parent -0.10R, unseen -0.14R vs -0.14R - did not help
- TRD-H4-BREAKOUT-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.37R vs parent +0.20R, unseen +0.42R vs +0.43R - passed
- repair record: DISP helped 6 of 9, NOTEXT helped 3 of 4, RETEST helped 3 of 3, HTF helped 0 of 1
- 1 repair(s) waiting for their first test

## ⚡ Shock alarm (sudden moves between candle closes, information only)

- 39 shock(s) this week, 30 sent to Telegram (the rest: over the daily cap, paused or /shock off)
- by kind: fast move 21, broke yesterday's high 1, broke yesterday's low 5, volume spike 19
- by coin: ETH 12, BTC 9, XRP 8, SOL 7, ZEC 2, SUI 1
- 4 hours later: 17 kept going, 22 reversed (average +0.07% in the shock's direction)
- followed by a strategy alert in the same direction within 4h: 10 of 39 - the strategies missed most shocks: material for the research (a reversal or sweep version)
-   2026-11-15 02:17 UTC SOL UP +4.7% -> 4h later -0.8% (no strategy alert)
-   2026-11-15 02:17 UTC XRP UP +4.5% -> 4h later +0.7% (no strategy alert)
-   2026-11-20 15:17 UTC SUI DOWN -2.7% -> 4h later +3.0% (a strategy alerted)
-   2026-11-15 02:12 UTC BTC UP +2.6% -> 4h later +0.4% (no strategy alert)
-   2026-11-20 15:19 UTC SOL DOWN -2.6% -> 4h later +1.2% (no strategy alert)

## 🧭 Location at the entry (4H structure, information only)

- at a zone or edge that fits the direction: 2 setup(s), +0.70R a trade after fees, 1 won
- middle of the 4H range: 4 setup(s), +0.03R a trade after fees, 1 won
- at a zone or edge against the direction: 142 setup(s), +0.36R a trade after fees, 70 won
- outside the 4H range (breakout): 118 setup(s), +0.43R a trade after fees, 53 won
- a difference counts only with 30+ setups in a group; then it is tested on 5 years before any rule

## Every live strategy / version / coin

| Strategy | TF | Coin | Stage | Sent to you | Live | Win % | After fees | Before fees | This week | Backtest | Confidence |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| TRD-H4-BREAKOUT-S3 | 1h | BTC | PAPER | ✅ yes | 1 | 100 | +2.47R | +2.50R | 1 (+2.5R) | +0.34R | +2.47R over 1 trade: too early to say anything |
| P01-BREAKOUT-V3 | 4h | XRP | TEST | ✅ yes | 8 | 62 | +1.17R | +1.21R | 7 (+6.9R) | +0.27R | +1.17R over 8 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | BTC | TEST | ✅ yes | 6 | 67 | +1.31R | +1.37R | 3 (+7.4R) | +0.38R | +1.31R over 6 trades: too early to say anything |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | TEST | ✅ yes | 3 | 67 | +1.28R | +1.32R | 2 (+4.9R) | +0.23R | +1.28R over 3 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | ETH | TEST | ✅ yes | 2 | 50 | +0.70R | +0.74R | 1 (+2.5R) | +0.24R | +0.70R over 2 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | SOL | TEST | ✅ yes | 2 | 50 | -0.09R | -0.06R | 2 (-0.2R) | +0.31R | -0.09R over 2 trades: too early to say anything |
| P07-SQUEEZE-RETEST-V3 | 4h | BTC | TEST | ✅ yes | 2 | 100 | +2.47R | +2.50R | 2 (+4.9R) | +0.39R | +2.47R over 2 trades: too early to say anything |
| P01-BREAKOUT-V4 | 4h | ETH | TEST | ✅ yes | 1 | 0 | -1.05R | -1.01R | 0 (+0.0R) | +0.21R | -1.05R over 1 trade: too early to say anything |
| P01-BREAKOUT-V4 | 4h | SOL | TEST | ✅ yes | 1 | 0 | -1.03R | -1.01R | 1 (-1.0R) | +0.30R | -1.03R over 1 trade: too early to say anything |
| P02-EMA-PULLBACK-V4 | 4h | BTC | TEST | ✅ yes | 1 | 100 | +3.77R | +3.89R | 1 (+3.8R) | +0.21R | +3.77R over 1 trade: too early to say anything |
| P05-RANGE-REVERSAL-V4 | 4h | SOL | TEST | ✅ yes | 1 | 0 | -1.06R | -1.01R | 0 (+0.0R) | +0.24R | -1.06R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V1 | 4h | SOL | TEST | ✅ yes | 1 | 0 | -1.05R | -1.02R | 0 (+0.0R) | +0.13R | -1.05R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V3 | 4h | XRP | TEST | ✅ yes | 1 | 100 | +2.47R | +2.50R | 0 (+0.0R) | +0.18R | +2.47R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | TEST | ✅ yes | 1 | 0 | -1.11R | -1.03R | 0 (+0.0R) | +0.41R | -1.11R over 1 trade: too early to say anything |
| P12-LEADER-V1 | 4h | ZEC | TEST | ✅ yes | 1 | 0 | -1.02R | -1.01R | 0 (+0.0R) | +0.41R | -1.02R over 1 trade: too early to say anything |
| TRD-H4-BREAKOUT-S3 | 1h | BTC | TEST | silent | 15 | 47 | +0.48R | +0.52R | 10 (+5.5R) | +0.34R | +0.48R over 15 trades: promising, not proven |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | TEST | silent | 11 | 27 | -0.22R | -0.12R | 1 (+2.5R) | +0.01R | -0.22R over 11 trades: not working so far |
| P03-FIB-PULLBACK-V5 | 1h | SOL | TEST | silent | 10 | 40 | +0.13R | +0.22R | 0 (+0.0R) | +0.04R | +0.13R over 10 trades: still uncertain - could be luck |
| TRD-H4-BREAKOUT-S3 | 1h | ETH | TEST | silent | 10 | 40 | +0.36R | +0.39R | 7 (+6.8R) | +0.06R | +0.36R over 10 trades: still uncertain - could be luck |
| TRD-H4-BREAKOUT-S3 | 1h | XRP | TEST | silent | 10 | 30 | -0.14R | -0.11R | 6 (+2.8R) | +0.30R | -0.14R over 10 trades: not working so far |
| P01-BREAKOUT-V2 | 30m | SOL | TEST | silent | 9 | 22 | -0.44R | -0.36R | 3 (+0.9R) | +0.07R | -0.44R over 9 trades: too early to say anything |
| P01-BREAKOUT-V2 | 30m | BTC | TEST | silent | 8 | 50 | +0.64R | +0.73R | 2 (+1.4R) | +0.09R | +0.64R over 8 trades: too early to say anything |
| P01-BREAKOUT-V2 | 1h | BTC | TEST | silent | 7 | 43 | +0.14R | +0.21R | 2 (+1.4R) | +0.11R | +0.14R over 7 trades: too early to say anything |
| P03-FIB-PULLBACK-V5 | 1h | SUI | TEST | silent | 7 | 43 | +0.23R | +0.27R | 1 (+2.5R) | +0.02R | +0.23R over 7 trades: too early to say anything |
| TRD-H4-BREAKOUT-S3 | 1h | SOL | TEST | silent | 7 | 29 | -0.25R | -0.23R | 5 (+0.3R) | +0.17R | -0.25R over 7 trades: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 15m | ETH | TEST | silent | 6 | 17 | -0.50R | -0.42R | 5 (-2.0R) | +0.02R | -0.50R over 6 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | BTC | TEST | silent | 5 | 40 | -0.49R | -0.30R | 2 (-1.1R) | +0.08R | -0.49R over 5 trades: too early to say anything |
| P01-BREAKOUT-V2 | 30m | ETH | TEST | silent | 5 | 20 | -0.09R | -0.04R | 3 (-2.3R) | +0.12R | -0.09R over 5 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | SUI | TEST | silent | 5 | 0 | -0.81R | -0.78R | 0 (+0.0R) | +0.08R | -0.81R over 5 trades: too early to say anything |
| P01-BREAKOUT-V5 | 30m | SUI | TEST | silent | 5 | 0 | -0.94R | -0.88R | 0 (+0.0R) | +0.01R | -0.94R over 5 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | TEST | silent | 4 | 50 | +0.30R | +0.36R | 1 (+2.5R) | +0.01R | +0.30R over 4 trades: too early to say anything |
| P07-SQUEEZE-RETEST-V2 | 30m | ETH | TEST | silent | 4 | 25 | -0.70R | -0.62R | 2 (-2.2R) | +0.07R | -0.70R over 4 trades: too early to say anything |
| P01-BREAKOUT-V2 | 1h | SOL | TEST | silent | 3 | 0 | -1.05R | -1.02R | 2 (-2.1R) | +0.02R | -1.05R over 3 trades: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | TEST | silent | 3 | 33 | +0.10R | +0.15R | 0 (+0.0R) | +0.04R | +0.10R over 3 trades: too early to say anything |
| P08-SESSION-BREAKOUT-V1 | 1h | BTC | TEST | silent | 3 | 33 | +0.16R | +0.21R | 2 (+1.4R) | +0.04R | +0.16R over 3 trades: too early to say anything |
| P08-SESSION-BREAKOUT-V4 | 1h | BTC | TEST | silent | 3 | 33 | -0.07R | -0.01R | 2 (+0.9R) | +0.04R | -0.07R over 3 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | ETH | TEST | silent | 2 | 0 | -0.74R | -0.68R | 0 (+0.0R) | +0.01R | -0.74R over 2 trades: too early to say anything |
| P04-MACD-SUPERTREND-V1 | 4h | ZEC | TEST | silent | 2 | 0 | -1.02R | -1.01R | 1 (-1.0R) | +0.12R | -1.02R over 2 trades: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | TEST | silent | 2 | 100 | +1.68R | +1.74R | 1 (+2.5R) | +0.18R | +1.68R over 2 trades: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 30m | XRP | TEST | silent | 2 | 100 | +1.65R | +1.75R | 1 (+2.5R) | +0.15R | +1.65R over 2 trades: too early to say anything |
| TRD-H4-BREAKOUT-S3 | 1h | SUI | TEST | silent | 2 | 50 | +0.72R | +0.74R | 2 (+1.4R) | +0.04R | +0.72R over 2 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | XRP | TEST | silent | 1 | 0 | -1.19R | -1.06R | 0 (+0.0R) | -0.01R | -1.19R over 1 trade: too early to say anything |
| P01-BREAKOUT-V2 | 30m | SUI | TEST | silent | 1 | 0 | -1.09R | -1.03R | 0 (+0.0R) | +0.12R | -1.09R over 1 trade: too early to say anything |
| P01-BREAKOUT-V5 | 1h | BTC | TEST | silent | 1 | 0 | -1.15R | -1.05R | 0 (+0.0R) | +0.02R | -1.15R over 1 trade: too early to say anything |
| P03-FIB-PULLBACK-V2 | 1h | SUI | TEST | silent | 1 | 100 | +2.48R | +2.50R | 1 (+2.5R) | +0.03R | +2.48R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V1 | 4h | ETH | TEST | silent | 1 | 100 | +2.48R | +2.50R | 1 (+2.5R) | +0.15R | +2.48R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 1h | XRP | TEST | silent | 1 | 0 | -1.05R | -1.02R | 0 (+0.0R) | +0.05R | -1.05R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V4 | 4h | ZEC | TEST | silent | 1 | 0 | -1.02R | -1.01R | 0 (+0.0R) | +0.22R | -1.02R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V1 | 4h | ETH | TEST | silent | 1 | 100 | +2.48R | +2.50R | 1 (+2.5R) | +0.09R | +2.48R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V5 | 1h | ZEC | TEST | silent | 1 | 0 | -0.49R | -0.46R | 0 (+0.0R) | +0.02R | -0.49R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V2 | 30m | SOL | TEST | silent | 1 | 100 | +2.44R | +2.50R | 1 (+2.4R) | +0.07R | +2.44R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V2 | 30m | SUI | TEST | silent | 1 | 100 | +2.46R | +2.50R | 1 (+2.5R) | +0.12R | +2.46R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V2 | 30m | XRP | TEST | silent | 1 | 100 | +2.44R | +2.50R | 1 (+2.4R) | +0.06R | +2.44R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V3 | 1h | SOL | TEST | silent | 1 | 100 | +1.53R | +1.58R | 0 (+0.0R) | +0.19R | +1.53R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V4 | 1h | XRP | TEST | silent | 1 | 0 | -1.07R | -1.03R | 0 (+0.0R) | +0.08R | -1.07R over 1 trade: too early to say anything |
