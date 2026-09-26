# Missed trades

Append-only (AGENT_PROMPT.md section 17.4), written by the daily research run. A strong move = at least 5x the 1H ATR within 12 hours on a research coin. For each: did any strategy have a signal before it started - and if it was filtered out, by what? **Never change a rule just because a missed move became large.**

Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` (section 22), then its details. `-` = not applicable.

### LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00
- timestamp: 2026-09-25 00:49 UTC · source: engine: daily research run · evidence: FACT: move of 8.0x the 1H ATR within 12 hours; 46 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: LTC · timeframe: 1h · regime: UNCLEAR · review: 2026-10-02
  - verdict: identifiable: at least one strategy had a valid signal before the move (research-only coin)
  - bb_squeeze_breakout v1.0 15m: blocked by the regime gate
  - ema_9_21_cross v1.0 30m: blocked by the regime gate
  - macd_trend_cross v1.0 1h: blocked by the regime gate
  - trend_pullback v1.0 15m: blocked by the regime gate
  - trend_pullback v1.0 1h: blocked by the regime gate
  - trend_pullback v1.0 4h: signal

### SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00
- timestamp: 2026-09-26 00:50 UTC · source: engine: daily research run · evidence: FACT: move of 5.5x the 1H ATR within 12 hours; 46 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: SOL · timeframe: 1h · regime: WEAK_BULL · review: 2026-10-03
  - verdict: identifiable: at least one strategy had a valid signal before the move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: no valid stop / target
  - liquidity_sweep_reversal v1.0 5m: signal
  - rsi2_dip_buy v1.0 1h: blocked by the regime gate
  - rsi2_dip_buy v1.0 30m: blocked by the regime gate
  - trend_pullback v1.0 15m: signal
  - trend_pullback v1.0 1h: signal

### SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00
- timestamp: 2026-09-26 00:50 UTC · source: engine: daily research run · evidence: FACT: move of 7.3x the 1H ATR within 12 hours; 46 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: SUI · timeframe: 1h · regime: WEAK_BULL · review: 2026-10-03
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - S5-SWEEP-MSS-FVG-noSMC v1.0 15m: blocked by the permission gate
  - S7-SILVER-BULLET v1.0 15m: blocked by the permission gate
  - S7-SILVER-BULLET-5M v1.0 15m: blocked by the permission gate
  - S7-SILVER-BULLET-noSMC v1.0 15m: blocked by the permission gate
  - bb_squeeze_breakout v1.0 15m: blocked by the permission gate
  - trend_pullback v1.0 15m: blocked by the permission gate
  - trend_pullback v1.0 1h: blocked by the permission gate
  - trend_pullback v1.0 30m: blocked by the permission gate

### ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00
- timestamp: 2026-09-26 00:50 UTC · source: engine: daily research run · evidence: FACT: move of 7.5x the 1H ATR within 12 hours; 46 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: ENA · timeframe: 1h · regime: TRANSITION · review: 2026-10-03
  - verdict: identifiable: at least one strategy had a valid signal before the move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: no valid stop / target
  - liquidity_sweep_reversal v1.0 5m: signal
  - rsi2_dip_buy v1.0 15m: blocked by the regime gate
  - trend_pullback v1.0 15m: blocked by the regime gate
  - trend_pullback v1.0 1h: blocked by the regime gate
  - trend_pullback v1.0 30m: blocked by the regime gate

### UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00
- timestamp: 2026-09-26 00:50 UTC · source: engine: daily research run · evidence: FACT: move of 5.3x the 1H ATR within 12 hours; 46 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: UNI · timeframe: 1h · regime: COMPRESSION · review: 2026-10-03
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move (research-only coin)
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: blocked by the regime gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the regime gate
