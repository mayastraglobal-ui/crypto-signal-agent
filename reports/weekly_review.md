# Weekly review · 2026-W48

Made 2026-11-25 08:20 UTC by the hourly scan (engine/weekly_review.py). Live = the program's 🔵 TEST setups (the GitHub record, no 5m check) and 🟡 PAPER signals, closed, after fees unless it says before fees. Promotion to PAPER needs the operator's tap; LIVE still needs the full pass bar and the approval line.

## System check

- ✅ nightly research ran on 6 of the last 7 days (last 2026-11-24)
- ✅ hourly scan: last run 2026-11-25 08:20 UTC
- ✅ program rotation: 93 of 93 strategy / timeframe tests re-tested in the last 7 days
- ✅ live watcher: last heartbeat 2026-11-25 06:25 UTC (47 min ago)
- ✅ TEST setups closed this week (GitHub record): 95

## Totals

- **Your alerts** (setups that could reach your Telegram): 67 closed since the start, +0.35R a trade; this week 43 (+13.80R)
- Silent research records (strategies NOT sent to you, kept to check the research): 200 closed, -0.04R a trade; this week 57 (-3.69R)
- TEST: 262 closed setups since the start, +0.05R a trade; this week 95 (+7.80R) (both groups)
- PAPER: 5 closed signals, +0.46R a trade; this week 5 (+2.31R)

## Promote to 🟡 PAPER (your tap)

None this week (each needs 10+ closed live TEST setups, positive after fees, and a positive backtest on that coin).

## In paper
- P01-BREAKOUT-V2@1.0 30m on BTC
- P03-FIB-PULLBACK-V5@1.0 1h on SOL
- TRD-H4-BREAKOUT-S3@1.0 1h on BTC, ETH

## With vs without the 5m check (before fees)

- watcher alerts (5m-confirmed): 16 plan results, +1.22R a trade
- every TEST setup (GitHub, no 5m check - your alerts and the silent records): 262, +0.10R a trade
- the same setups side by side (live watcher twins, `confirm_5m.compare_tfs`):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) +0.81R over 44 (plan results, before fees)

## 📈 Live track record and drift monitor

- **your alerts**: 54 closed, +0.45R a trade, +24.39R, worst drawdown 5.47R (after fees)
- silent research records: 200 closed, -0.04R a trade
- paused by the drift monitor: nothing
- the full table: reports/track_record.md

## Ideas for new versions

- none yet (each needs 10+ live trades)

## Failure Lab (repairs for the loss causes)

- new repair P11-MOMENTUM-V3-FRETEST: P11-MOMENTUM-V3@1.0 1h lost on false_breakout - testing RETEST
- P01-BREAKOUT-V2-FDISP-FNOTEXT@1.0 30m (NOTEXT for overextended_entry): +0.28R vs parent +0.05R, unseen +0.43R vs +0.18R - helped
- P01-BREAKOUT-V2-FDISP-FRETEST@1.0 30m (RETEST for overextended_entry): +0.14R vs parent +0.05R, unseen +0.28R vs +0.18R - helped
- P01-BREAKOUT-V2-FDISP@1.0 30m (DISP for false_breakout): +0.05R vs parent +0.01R, unseen +0.18R vs +0.10R - helped
- P01-BREAKOUT-V2-FRETEST@1.0 30m (RETEST for false_breakout): +0.06R vs parent +0.01R, unseen +0.15R vs +0.10R - helped
- P01-BREAKOUT-V5-FDISP@1.0 15m (DISP for false_breakout): -0.12R vs parent -0.12R, unseen -0.11R vs -0.12R - did not help
- repair record: DISP helped 6 of 9, RETEST helped 6 of 6, NOTEXT helped 3 of 4, HTF helped 0 of 1

## ⚡ Shock alarm (sudden moves between candle closes, information only)

- 55 shock(s) this week, 43 sent to Telegram (the rest: over the daily cap, paused or /shock off)
- by kind: fast move 32, broke yesterday's high 6, broke yesterday's low 11, volume spike 30
- by coin: ETH 14, BTC 12, SOL 10, XRP 9, ZEC 6, SUI 4
- 4 hours later: 18 kept going, 37 reversed (average -0.84% in the shock's direction)
- followed by a strategy alert in the same direction within 4h: 7 of 55 - the strategies missed most shocks: material for the research (a reversal or sweep version)
-   2026-11-23 14:00 UTC ZEC UP +6.3% -> 4h later -3.2% (no strategy alert)
-   2026-11-23 14:00 UTC SOL UP +5.5% -> 4h later -3.9% (no strategy alert)
-   2026-11-23 14:30 UTC ZEC UP +5.2% -> 4h later -9.2% (no strategy alert)
-   2026-11-23 14:00 UTC XRP UP +5.0% -> 4h later -3.1% (no strategy alert)
-   2026-11-23 14:00 UTC ETH UP +4.9% -> 4h later -3.7% (no strategy alert)

## 🧭 Location at the entry (4H structure, information only)

- at a zone or edge that fits the direction: 4 setup(s), -0.23R a trade after fees, 1 won
- middle of the 4H range: 4 setup(s), +0.03R a trade after fees, 1 won
- at a zone or edge against the direction: 165 setup(s), +0.30R a trade after fees, 78 won
- outside the 4H range (breakout): 226 setup(s), +0.06R a trade after fees, 84 won
- a difference counts only with 30+ setups in a group; then it is tested on 5 years before any rule

## Every live strategy / version / coin

| Strategy | TF | Coin | Stage | Sent to you | Live | Win % | After fees | Before fees | This week | Backtest | Confidence |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| TRD-H4-BREAKOUT-S3 | 1h | BTC | PAPER | ✅ yes | 5 | 60 | +0.46R | +0.49R | 5 (+2.3R) | +0.34R | +0.46R over 5 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | BTC | TEST | ✅ yes | 9 | 44 | +0.60R | +0.65R | 5 (+2.4R) | +0.38R | +0.60R over 9 trades: too early to say anything |
| P01-BREAKOUT-V3 | 4h | XRP | TEST | ✅ yes | 8 | 62 | +1.17R | +1.21R | 0 (+0.0R) | +0.26R | +1.17R over 8 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | ETH | TEST | ✅ yes | 6 | 33 | -0.12R | -0.09R | 5 (+0.3R) | +0.24R | -0.12R over 6 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | SUI | TEST | ✅ yes | 4 | 25 | -0.20R | -0.17R | 4 (-0.8R) | +0.20R | -0.20R over 4 trades: too early to say anything |
| P01-BREAKOUT-V3 | 4h | SUI | TEST | ✅ yes | 4 | 25 | -0.20R | -0.17R | 4 (-0.8R) | +0.40R | -0.20R over 4 trades: too early to say anything |
| P01-BREAKOUT-V4 | 4h | ETH | TEST | ✅ yes | 4 | 50 | +0.31R | +0.35R | 3 (+2.3R) | +0.21R | +0.31R over 4 trades: too early to say anything |
| P01-BREAKOUT-V3 | 4h | BTC | TEST | ✅ yes | 3 | 0 | -0.84R | -0.81R | 3 (-2.5R) | +0.55R | -0.84R over 3 trades: too early to say anything |
| P01-BREAKOUT-V3 | 4h | ETH | TEST | ✅ yes | 3 | 0 | -1.03R | -1.01R | 3 (-3.1R) | +0.20R | -1.03R over 3 trades: too early to say anything |
| P01-BREAKOUT-V4 | 4h | SUI | TEST | ✅ yes | 3 | 33 | -0.18R | -0.15R | 3 (-0.5R) | +0.25R | -0.18R over 3 trades: too early to say anything |
| P07-SQUEEZE-RETEST-V1 | 4h | BTC | TEST | ✅ yes | 3 | 67 | +1.28R | +1.32R | 2 (+4.9R) | +0.25R | +1.28R over 3 trades: too early to say anything |
| P01-BREAKOUT-V1 | 4h | SOL | TEST | ✅ yes | 2 | 50 | -0.09R | -0.06R | 0 (+0.0R) | +0.31R | -0.09R over 2 trades: too early to say anything |
| P01-BREAKOUT-V4 | 4h | SOL | TEST | ✅ yes | 2 | 50 | +0.23R | +0.27R | 1 (+1.5R) | +0.32R | +0.23R over 2 trades: too early to say anything |
| P07-SQUEEZE-RETEST-V3 | 4h | BTC | TEST | ✅ yes | 2 | 100 | +2.47R | +2.50R | 2 (+4.9R) | +0.44R | +2.47R over 2 trades: too early to say anything |
| P01-BREAKOUT-V4 | 4h | BNB | TEST | ✅ yes | 1 | 100 | +1.80R | +1.86R | 1 (+1.8R) | +0.18R | +1.80R over 1 trade: too early to say anything |
| P02-EMA-PULLBACK-V4 | 4h | BTC | TEST | ✅ yes | 1 | 100 | +3.77R | +3.89R | 0 (+0.0R) | +0.21R | +3.77R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V3 | 4h | ETH | TEST | ✅ yes | 1 | 0 | -1.03R | -1.01R | 1 (-1.0R) | +0.27R | -1.03R over 1 trade: too early to say anything |
| P05-RANGE-REVERSAL-V4 | 4h | SOL | TEST | ✅ yes | 1 | 0 | -1.06R | -1.01R | 0 (+0.0R) | +0.24R | -1.06R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V1 | 4h | SOL | TEST | ✅ yes | 1 | 0 | -1.05R | -1.02R | 0 (+0.0R) | +0.13R | -1.05R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V3 | 4h | XRP | TEST | ✅ yes | 1 | 100 | +2.47R | +2.50R | 0 (+0.0R) | +0.18R | +2.47R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V4 | 4h | BNB | TEST | ✅ yes | 1 | 100 | +2.07R | +2.14R | 1 (+2.1R) | +0.13R | +2.07R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V4 | 4h | BTC | TEST | ✅ yes | 1 | 0 | -1.11R | -1.03R | 0 (+0.0R) | +0.41R | -1.11R over 1 trade: too early to say anything |
| P12-LEADER-V1 | 4h | ZEC | TEST | ✅ yes | 1 | 0 | -1.02R | -1.01R | 0 (+0.0R) | +0.41R | -1.02R over 1 trade: too early to say anything |
| TRD-H4-BREAKOUT-S3 | 1h | BTC | TEST | silent | 15 | 47 | +0.48R | +0.52R | 2 (-2.2R) | +0.34R | +0.48R over 15 trades: promising, not proven |
| TRD-H4-BREAKOUT-S3 | 1h | ETH | TEST | silent | 15 | 33 | +0.11R | +0.14R | 8 (+1.9R) | +0.07R | +0.11R over 15 trades: still uncertain - could be luck |
| P01-BREAKOUT-V2 | 30m | BTC | TEST | silent | 12 | 50 | +0.53R | +0.60R | 4 (+1.2R) | +0.10R | +0.53R over 12 trades: promising, not proven |
| P04-MACD-SUPERTREND-V5 | 30m | XRP | TEST | silent | 11 | 27 | -0.22R | -0.12R | 0 (+0.0R) | +0.01R | -0.22R over 11 trades: not working so far |
| P01-BREAKOUT-V2 | 1h | BTC | TEST | silent | 10 | 40 | -0.01R | +0.04R | 3 (-1.1R) | +0.12R | -0.01R over 10 trades: not working so far |
| P03-FIB-PULLBACK-V5 | 1h | SOL | TEST | silent | 10 | 40 | +0.13R | +0.22R | 0 (+0.0R) | +0.04R | +0.13R over 10 trades: still uncertain - could be luck |
| TRD-H4-BREAKOUT-S3 | 1h | XRP | TEST | silent | 10 | 30 | -0.14R | -0.11R | 0 (+0.0R) | +0.30R | -0.14R over 10 trades: not working so far |
| P01-BREAKOUT-V2 | 30m | ETH | TEST | silent | 9 | 33 | -0.08R | -0.03R | 5 (-1.0R) | +0.14R | -0.08R over 9 trades: too early to say anything |
| P01-BREAKOUT-V2 | 30m | SOL | TEST | silent | 9 | 22 | -0.44R | -0.36R | 0 (+0.0R) | +0.07R | -0.44R over 9 trades: too early to say anything |
| P01-BREAKOUT-V5 | 30m | SUI | TEST | silent | 8 | 0 | -0.98R | -0.93R | 3 (-3.2R) | +0.02R | -0.98R over 8 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | SUI | TEST | silent | 7 | 14 | -0.57R | -0.55R | 2 (+0.0R) | +0.08R | -0.57R over 7 trades: too early to say anything |
| P03-FIB-PULLBACK-V5 | 1h | SUI | TEST | silent | 7 | 43 | +0.23R | +0.27R | 1 (+2.5R) | +0.03R | +0.23R over 7 trades: too early to say anything |
| TRD-H4-BREAKOUT-S3 | 1h | SOL | TEST | silent | 7 | 29 | -0.25R | -0.23R | 0 (+0.0R) | +0.17R | -0.25R over 7 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | BTC | TEST | silent | 6 | 33 | -0.59R | -0.43R | 3 (-2.1R) | +0.09R | -0.59R over 6 trades: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 15m | ETH | TEST | silent | 6 | 17 | -0.50R | -0.42R | 3 (-3.4R) | +0.03R | -0.50R over 6 trades: too early to say anything |
| P07-SQUEEZE-RETEST-V2 | 30m | ETH | TEST | silent | 5 | 20 | -0.80R | -0.71R | 3 (-3.4R) | +0.04R | -0.80R over 5 trades: too early to say anything |
| P04-MACD-SUPERTREND-V5 | 30m | SUI | TEST | silent | 4 | 50 | +0.30R | +0.36R | 1 (+2.5R) | +0.01R | +0.30R over 4 trades: too early to say anything |
| P08-SESSION-BREAKOUT-V4 | 1h | BTC | TEST | silent | 4 | 50 | +0.38R | +0.43R | 1 (+1.7R) | +0.04R | +0.38R over 4 trades: too early to say anything |
| TRD-H4-BREAKOUT-S3 | 1h | SUI | TEST | silent | 4 | 50 | +0.35R | +0.37R | 4 (+1.4R) | +0.07R | +0.35R over 4 trades: too early to say anything |
| P01-BREAKOUT-V2 | 1h | SOL | TEST | silent | 3 | 0 | -1.05R | -1.02R | 0 (+0.0R) | +0.02R | -1.05R over 3 trades: too early to say anything |
| P01-BREAKOUT-V2 | 30m | SUI | TEST | silent | 3 | 0 | -1.06R | -1.02R | 2 (-2.1R) | +0.12R | -1.06R over 3 trades: too early to say anything |
| P01-BREAKOUT-V5 | 1h | ETH | TEST | silent | 3 | 0 | -0.84R | -0.79R | 1 (-1.0R) | +0.02R | -0.84R over 3 trades: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 1h | SOL | TEST | silent | 3 | 33 | +0.10R | +0.15R | 0 (+0.0R) | +0.04R | +0.10R over 3 trades: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 30m | SUI | TEST | silent | 3 | 67 | +0.82R | +0.87R | 2 (+1.6R) | +0.19R | +0.82R over 3 trades: too early to say anything |
| P08-SESSION-BREAKOUT-V1 | 1h | BTC | TEST | silent | 3 | 33 | +0.16R | +0.21R | 1 (+2.5R) | +0.05R | +0.16R over 3 trades: too early to say anything |
| P01-BREAKOUT-V2 | 1h | SUI | TEST | silent | 2 | 50 | +0.01R | +0.03R | 2 (+0.0R) | +0.15R | +0.01R over 2 trades: too early to say anything |
| P04-MACD-SUPERTREND-V1 | 4h | ETH | TEST | silent | 2 | 50 | +0.72R | +0.74R | 1 (-1.0R) | +0.17R | +0.72R over 2 trades: too early to say anything |
| P04-MACD-SUPERTREND-V1 | 4h | ZEC | TEST | silent | 2 | 0 | -1.02R | -1.01R | 0 (+0.0R) | +0.12R | -1.02R over 2 trades: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 30m | XRP | TEST | silent | 2 | 100 | +1.65R | +1.75R | 0 (+0.0R) | +0.15R | +1.65R over 2 trades: too early to say anything |
| P01-BREAKOUT-V2 | 15m | SUI | TEST | silent | 1 | 0 | -1.19R | -1.06R | 1 (-1.2R) | +0.01R | -1.19R over 1 trade: too early to say anything |
| P01-BREAKOUT-V2 | 15m | XRP | TEST | silent | 1 | 0 | -1.19R | -1.06R | 0 (+0.0R) | -0.01R | -1.19R over 1 trade: too early to say anything |
| P01-BREAKOUT-V5 | 1h | BTC | TEST | silent | 1 | 0 | -1.15R | -1.05R | 0 (+0.0R) | +0.02R | -1.15R over 1 trade: too early to say anything |
| P03-FIB-PULLBACK-V2 | 1h | SUI | TEST | silent | 1 | 100 | +2.48R | +2.50R | 1 (+2.5R) | +0.04R | +2.48R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V2 | 1h | XRP | TEST | silent | 1 | 0 | -1.05R | -1.02R | 0 (+0.0R) | +0.05R | -1.05R over 1 trade: too early to say anything |
| P04-MACD-SUPERTREND-V4 | 4h | ZEC | TEST | silent | 1 | 0 | -1.02R | -1.01R | 0 (+0.0R) | +0.22R | -1.02R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V1 | 4h | ETH | TEST | silent | 1 | 100 | +2.48R | +2.50R | 0 (+0.0R) | +0.09R | +2.48R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V2 | 1h | BTC | TEST | silent | 1 | 0 | -1.05R | -1.02R | 1 (-1.1R) | +0.04R | -1.05R over 1 trade: too early to say anything |
| P07-SQUEEZE-RETEST-V5 | 1h | ZEC | TEST | silent | 1 | 0 | -0.49R | -0.46R | 0 (+0.0R) | +0.02R | -0.49R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V2 | 30m | SOL | TEST | silent | 1 | 100 | +2.44R | +2.50R | 0 (+0.0R) | +0.07R | +2.44R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V2 | 30m | SUI | TEST | silent | 1 | 100 | +2.46R | +2.50R | 1 (+2.5R) | +0.12R | +2.46R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V2 | 30m | XRP | TEST | silent | 1 | 100 | +2.44R | +2.50R | 0 (+0.0R) | +0.06R | +2.44R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V3 | 1h | SOL | TEST | silent | 1 | 100 | +1.53R | +1.58R | 0 (+0.0R) | +0.19R | +1.53R over 1 trade: too early to say anything |
| P08-SESSION-BREAKOUT-V4 | 1h | XRP | TEST | silent | 1 | 0 | -1.07R | -1.03R | 0 (+0.0R) | +0.08R | -1.07R over 1 trade: too early to say anything |
| P12-LEADER-V1 | 4h | SUI | TEST | silent | 1 | 0 | -1.03R | -1.01R | 1 (-1.0R) | +0.01R | -1.03R over 1 trade: too early to say anything |
