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
