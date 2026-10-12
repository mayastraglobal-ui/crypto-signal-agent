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
