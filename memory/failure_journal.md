# Failure journal

Append-only (AGENT_PROMPT.md section 17), written by the engine. One entry per logged signal (validation / paper / live) that closed with a loss. Tags are measured by fixed rules (`engine/attribution.py`); root causes and fixes are added by the reviews - never by changing rules mid-trade. MAE / MFE = worst / best point of the trade, in R.

Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` (section 22), then its details. `-` = not applicable.

### XRP SHORT 30m P04-MACD-SUPERTREND-V5 v1.0 - SL -1.31R
- timestamp: 2026-10-11 15:18 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.31R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P04-MACD-SUPERTREND-V5 v1.0 · asset: XRP · timeframe: 30m · regime: WEAK_BEAR · review: 2026-10-18
  - signal 2026-10-11 10:29 UTC, closed 2026-10-11 14:59 UTC, stage TEST
  - MAE -1.52R / MFE +0.31R
  - at entry: session outside killzones, conditions: low_relative_volume, no_displacement, wrong_session
  - what happened: regime_mismatch
  - root cause / fix: (review)

### SOL SHORT 1h P03-FIB-PULLBACK-V5 v1.0 - SL -1.18R
- timestamp: 2026-10-11 16:19 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.18R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P03-FIB-PULLBACK-V5 v1.0 · asset: SOL · timeframe: 1h · regime: WEAK_BEAR · review: 2026-10-18
  - signal 2026-10-11 07:59 UTC, closed 2026-10-11 15:59 UTC, stage TEST
  - MAE -2.77R / MFE +0.17R
  - at entry: session London, conditions: range_market, low_relative_volume
  - what happened: volatility_spike, regime_mismatch, indicator_lag
  - root cause / fix: (review)

### SOL SHORT 1h P03-FIB-PULLBACK-V5 v1.0 - SL -1.20R
- timestamp: 2026-10-11 16:19 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.20R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P03-FIB-PULLBACK-V5 v1.0 · asset: SOL · timeframe: 1h · regime: WEAK_BEAR · review: 2026-10-18
  - signal 2026-10-11 09:59 UTC, closed 2026-10-11 15:59 UTC, stage TEST
  - MAE -2.96R / MFE +0.28R
  - at entry: session outside killzones, conditions: range_market, wrong_session
  - what happened: volatility_spike, regime_mismatch
  - root cause / fix: (review)

### Root cause: three TEST losses on 2026-10-11 came from cells that fail overall (selection by coin)
- timestamp: 2026-10-12 15:30 UTC · source: Claude daily review 2026-10-12 · evidence: MODEL_OUTPUT: reading of the three engine entries of 2026-10-11 (SOL SHORT 1h P03-FIB-PULLBACK-V5 -1.18R and -1.20R; XRP SHORT 30m P04-MACD-SUPERTREND-V5 -1.31R) with the backtest verdicts of 2026-10-11 and config.yaml -> signal_center · confidence: medium · strategy: P03-FIB-PULLBACK-V5 v1.0, P04-MACD-SUPERTREND-V5 v1.0 · asset: SOL, XRP · timeframe: 1h, 30m · regime: WEAK_BEAR · review: 2026-10-19
  The engine's tags are not changed. My reading of the root cause:
  - strategy: both strategies FAILED as a whole on 2026-10-11 (P03-FIB-PULLBACK-V5 1h -0.12R a trade, P04-MACD-SUPERTREND-V5 30m -0.11R a trade, BACKTEST). A TEST alert needs only that the cell was positive on that one coin (config.yaml -> signal_center: at least 20 backtest trades on the coin, average above 0R, unseen part not negative). Picking the coins where a losing strategy happened to do well is a selection effect (C04 and C05: the more cells are searched, the more look good by luck).
  - regime and timing: all three were shorts in a WEAK_BEAR hour while the engine's market weather said "Choppy - stay out"; the at-entry conditions were range_market, low_relative_volume and wrong_session, and the tags say regime_mismatch.
  - stop / target: the two SOL losses had MAE -2.77R and -2.96R, far beyond the 1R stop, and volatility_spike: one large 1h candle went through the stop (the loss after costs was -1.18R and -1.20R). The XRP loss had MAE -1.52R. MFE was small in all three (+0.17R to +0.31R): the trades never went their way.
  - sample size: three trades - an example, not a pattern. Systematic or random cannot be told from three trades; the selection effect is the systematic part to watch.

### BTC SHORT 1h P01-BREAKOUT-V5 v1.0 - SL -1.15R
- timestamp: 2026-10-13 03:20 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.15R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P01-BREAKOUT-V5 v1.0 · asset: BTC · timeframe: 1h · regime: EXPANSION · review: 2026-10-20
  - signal 2026-10-12 23:59 UTC, closed 2026-10-13 02:59 UTC, stage TEST
  - MAE -1.47R / MFE +0.96R
  - at entry: session outside killzones, conditions: overextended_entry, no_displacement, wrong_session
  - what happened: false_breakout
  - root cause / fix: (review)

### ETH SHORT 1h P01-BREAKOUT-V5 v1.0 - SL -1.10R
- timestamp: 2026-10-13 03:20 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.10R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P01-BREAKOUT-V5 v1.0 · asset: ETH · timeframe: 1h · regime: WEAK_BEAR · review: 2026-10-20
  - signal 2026-10-12 23:59 UTC, closed 2026-10-13 02:59 UTC, stage TEST
  - MAE -1.37R / MFE +1.02R
  - at entry: session outside killzones, conditions: overextended_entry, late_entry, wrong_session
  - what happened: false_breakout
  - root cause / fix: (review)

### Root cause: BTC and ETH TEST shorts of 2026-10-12 23:59 UTC - one breakout signal on two correlated coins
- timestamp: 2026-10-13 15:30 UTC · source: Claude daily review 2026-10-13 · evidence: MODEL_OUTPUT: reading of the two engine entries (BTC SHORT 1h P01-BREAKOUT-V5 -1.15R, MAE -1.47R / MFE +0.96R; ETH SHORT 1h P01-BREAKOUT-V5 -1.10R, MAE -1.37R / MFE +1.02R) with the backtest verdict of 2026-10-10 and config.yaml -> signal_center · confidence: medium · strategy: P01-BREAKOUT-V5 v1.0 · asset: BTC, ETH · timeframe: 1h · regime: TRANSITION · review: 2026-10-20
  The engine's tag (false_breakout) is not changed. My reading:
  - strategy: P01-BREAKOUT-V5 1h FAILED across all coins (-0.02R a trade, profit factor 0.96, on 2026-10-10, BACKTEST); the alerts came from the per-coin TEST selection, as with the three TEST losses of 2026-10-11 (see 'Root cause: three TEST losses on 2026-10-11 ...').
  - timing: both signals fired at the same candle (2026-10-12 23:59 UTC), outside the killzones, with overextended_entry and wrong_session at entry. BTC and ETH move together, so this was one bet taken twice, not two independent trades.
  - stop / target: both went about +1R in favour (MFE +0.96R and +1.02R) and then reversed to the stop. The first target of a lab card is at least 2R, so neither reached it. One trade's worth of evidence, but it fits the false_breakout tag that is systematic in many breakout backtests (32 tests in the fact sheet of 2026-10-11).
  - regime: the market weather said "Choppy - stay out" on both coins; breakouts fail most in such markets (C08).
  - sample size: two trades on one signal; not a pattern. Five TEST losses are now in the journal (2026-10-11 and 2026-10-13).

### XRP SHORT 30m P04-MACD-SUPERTREND-V5 v1.0 - SL -1.09R
- timestamp: 2026-10-15 03:30 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.09R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P04-MACD-SUPERTREND-V5 v1.0 · asset: XRP · timeframe: 30m · regime: WEAK_BEAR · review: 2026-10-22
  - signal 2026-10-15 02:29 UTC, closed 2026-10-15 02:59 UTC, stage TEST
  - MAE -1.09R / MFE +0.35R
  - at entry: session Asia, conditions: range_market, overextended_entry, late_entry, no_displacement, wrong_session
  - what happened: -
  - root cause / fix: (review)

### SUI SHORT 30m P04-MACD-SUPERTREND-V5 v1.0 - SL -1.07R
- timestamp: 2026-10-15 14:34 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.07R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P04-MACD-SUPERTREND-V5 v1.0 · asset: SUI · timeframe: 30m · regime: WEAK_BEAR · review: 2026-10-22
  - signal 2026-10-15 12:59 UTC, closed 2026-10-15 14:29 UTC, stage TEST
  - MAE -1.06R / MFE +0.47R
  - at entry: session NY AM, conditions: no_displacement
  - what happened: false_breakout
  - root cause / fix: (review)

### ETH SHORT 1h P01-BREAKOUT-V5 v1.0 - exit-rule -0.39R
- timestamp: 2026-10-15 15:35 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -0.39R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P01-BREAKOUT-V5 v1.0 · asset: ETH · timeframe: 1h · regime: EXPANSION · review: 2026-10-22
  - signal 2026-10-15 02:59 UTC, closed 2026-10-15 14:59 UTC, stage TEST
  - MAE -0.37R / MFE +1.11R
  - at entry: session Asia, conditions: overextended_entry, no_displacement, wrong_session
  - what happened: -
  - root cause / fix: (review)

### XRP SHORT 30m P04-MACD-SUPERTREND-V5 v1.0 - SL -1.09R
- timestamp: 2026-10-15 15:35 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.09R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P04-MACD-SUPERTREND-V5 v1.0 · asset: XRP · timeframe: 30m · regime: WEAK_BEAR · review: 2026-10-22
  - signal 2026-10-15 05:29 UTC, closed 2026-10-15 15:29 UTC, stage TEST
  - MAE -1.42R / MFE +0.89R
  - at entry: session outside killzones, conditions: wrong_session
  - what happened: -
  - root cause / fix: (review)

### SOL SHORT 1h P03-FIB-PULLBACK-V5 v1.0 - SL -1.06R
- timestamp: 2026-10-15 15:35 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.06R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P03-FIB-PULLBACK-V5 v1.0 · asset: SOL · timeframe: 1h · regime: WEAK_BEAR · review: 2026-10-22
  - signal 2026-10-15 05:59 UTC, closed 2026-10-15 14:59 UTC, stage TEST
  - MAE -1.30R / MFE +0.20R
  - at entry: session outside killzones, conditions: overextended_entry, wrong_session
  - what happened: indicator_lag
  - root cause / fix: (review)

### SOL SHORT 1h P03-FIB-PULLBACK-V5 v1.0 - SL -1.09R
- timestamp: 2026-10-15 15:35 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.09R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P03-FIB-PULLBACK-V5 v1.0 · asset: SOL · timeframe: 1h · regime: WEAK_BEAR · review: 2026-10-22
  - signal 2026-10-15 10:59 UTC, closed 2026-10-15 14:59 UTC, stage TEST
  - MAE -1.46R / MFE +0.80R
  - at entry: session outside killzones, conditions: low_relative_volume, wrong_session
  - what happened: -
  - root cause / fix: (review)

### SOL SHORT 1h P04-MACD-SUPERTREND-V2 v1.0 - SL -1.07R
- timestamp: 2026-10-15 15:35 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.07R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P04-MACD-SUPERTREND-V2 v1.0 · asset: SOL · timeframe: 1h · regime: WEAK_BEAR · review: 2026-10-22
  - signal 2026-10-15 11:59 UTC, closed 2026-10-15 14:59 UTC, stage TEST
  - MAE -1.18R / MFE +0.52R
  - at entry: session NY AM, conditions: low_relative_volume, no_displacement
  - what happened: volatility_spike
  - root cause / fix: (review)

### XRP SHORT 30m P04-MACD-SUPERTREND-V5 v1.0 - SL -1.10R
- timestamp: 2026-10-15 15:35 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.10R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P04-MACD-SUPERTREND-V5 v1.0 · asset: XRP · timeframe: 30m · regime: STRONG_BEAR · review: 2026-10-22
  - signal 2026-10-15 13:29 UTC, closed 2026-10-15 14:59 UTC, stage TEST
  - MAE -1.49R / MFE +0.56R
  - at entry: session NY AM, conditions: no_displacement
  - what happened: false_breakout
  - root cause / fix: (review)

### ETH SHORT 4h P01-BREAKOUT-V1 v1.0 - SL -1.05R
- timestamp: 2026-10-15 16:33 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.05R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P01-BREAKOUT-V1 v1.0 · asset: ETH · timeframe: 4h · regime: WEAK_BEAR · review: 2026-10-22
  - signal 2026-10-15 03:59 UTC, closed 2026-10-15 15:59 UTC, stage TEST
  - MAE -1.02R / MFE +0.41R
  - at entry: session -, conditions: overextended_entry, late_entry, no_displacement
  - what happened: false_breakout
  - root cause / fix: (review)

### ETH SHORT 4h P01-BREAKOUT-V4 v1.0 - SL -1.05R
- timestamp: 2026-10-15 16:33 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.05R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P01-BREAKOUT-V4 v1.0 · asset: ETH · timeframe: 4h · regime: WEAK_BEAR · review: 2026-10-22
  - signal 2026-10-15 03:59 UTC, closed 2026-10-15 15:59 UTC, stage TEST
  - MAE -1.02R / MFE +0.41R
  - at entry: session -, conditions: overextended_entry, late_entry, no_displacement
  - what happened: false_breakout
  - root cause / fix: (review)

### SUI SHORT 1h P03-FIB-PULLBACK-V5 v1.0 - SL -1.04R
- timestamp: 2026-10-15 16:33 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.04R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P03-FIB-PULLBACK-V5 v1.0 · asset: SUI · timeframe: 1h · regime: WEAK_BEAR · review: 2026-10-22
  - signal 2026-10-15 05:59 UTC, closed 2026-10-15 15:59 UTC, stage TEST
  - MAE -1.37R / MFE +0.43R
  - at entry: session outside killzones, conditions: overextended_entry, wrong_session
  - what happened: regime_mismatch
  - root cause / fix: (review)

### SUI SHORT 30m P01-BREAKOUT-V5 v1.0 - SL -1.09R
- timestamp: 2026-10-18 02:09 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.09R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P01-BREAKOUT-V5 v1.0 · asset: SUI · timeframe: 30m · regime: WEAK_BEAR · review: 2026-10-25
  - signal 2026-10-17 21:59 UTC, closed 2026-10-18 01:29 UTC, stage TEST
  - MAE -1.07R / MFE +0.00R
  - at entry: session outside killzones, conditions: overextended_entry, wrong_session
  - what happened: false_breakout
  - root cause / fix: (review)

### SUI SHORT 30m P04-MACD-SUPERTREND-V5 v1.0 - SL -1.09R
- timestamp: 2026-10-18 02:09 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.09R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P04-MACD-SUPERTREND-V5 v1.0 · asset: SUI · timeframe: 30m · regime: WEAK_BEAR · review: 2026-10-25
  - signal 2026-10-17 21:59 UTC, closed 2026-10-18 01:29 UTC, stage TEST
  - MAE -1.07R / MFE +0.00R
  - at entry: session outside killzones, conditions: overextended_entry, wrong_session
  - what happened: false_breakout, indicator_lag
  - root cause / fix: (review)

### SUI SHORT 1h P03-FIB-PULLBACK-V5 v1.0 - SL -1.11R
- timestamp: 2026-10-18 10:25 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.11R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P03-FIB-PULLBACK-V5 v1.0 · asset: SUI · timeframe: 1h · regime: WEAK_BEAR · review: 2026-10-25
  - signal 2026-10-18 05:59 UTC, closed 2026-10-18 09:59 UTC, stage TEST
  - MAE -1.26R / MFE +0.11R
  - at entry: session outside killzones, conditions: low_relative_volume, wrong_session
  - what happened: regime_mismatch, indicator_lag
  - root cause / fix: (review)

### SOL SHORT 30m P01-BREAKOUT-V2 v1.0 - SL -1.14R
- timestamp: 2026-10-18 22:24 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.14R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P01-BREAKOUT-V2 v1.0 · asset: SOL · timeframe: 30m · regime: WEAK_BEAR · review: 2026-10-25
  - signal 2026-10-18 19:59 UTC, closed 2026-10-18 21:59 UTC, stage TEST
  - MAE -1.21R / MFE +0.31R
  - at entry: session outside killzones, conditions: overextended_entry, wrong_session
  - what happened: -
  - root cause / fix: (review)

### XRP SHORT 15m P01-BREAKOUT-V2 v1.0 - SL -1.19R
- timestamp: 2026-10-18 22:24 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.19R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P01-BREAKOUT-V2 v1.0 · asset: XRP · timeframe: 15m · regime: WEAK_BEAR · review: 2026-10-25
  - signal 2026-10-18 19:44 UTC, closed 2026-10-18 21:29 UTC, stage TEST
  - MAE -1.15R / MFE +0.33R
  - at entry: session outside killzones, conditions: overextended_entry, wrong_session
  - what happened: -
  - root cause / fix: (review)

### SUI SHORT 30m P01-BREAKOUT-V5 v1.0 - SL -1.09R
- timestamp: 2026-10-18 22:24 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.09R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P01-BREAKOUT-V5 v1.0 · asset: SUI · timeframe: 30m · regime: WEAK_BEAR · review: 2026-10-25
  - signal 2026-10-18 19:59 UTC, closed 2026-10-18 21:59 UTC, stage TEST
  - MAE -1.16R / MFE +0.03R
  - at entry: session outside killzones, conditions: overextended_entry, wrong_session
  - what happened: -
  - root cause / fix: (review)

### XRP SHORT 30m P04-MACD-SUPERTREND-V5 v1.0 - SL -1.19R
- timestamp: 2026-10-20 14:33 UTC · source: engine: hourly scan (reports/signals_log.csv) · evidence: FACT: TEST result -1.19R after costs; tags by fixed rules · confidence: one trade - an example, not a pattern · strategy: P04-MACD-SUPERTREND-V5 v1.0 · asset: XRP · timeframe: 30m · regime: WEAK_BEAR · review: 2026-10-27
  - signal 2026-10-20 07:29 UTC, closed 2026-10-20 13:59 UTC, stage TEST
  - MAE -1.05R / MFE +0.82R
  - at entry: session London, conditions: range_market, low_relative_volume, no_displacement
  - what happened: regime_mismatch
  - root cause / fix: (review)
