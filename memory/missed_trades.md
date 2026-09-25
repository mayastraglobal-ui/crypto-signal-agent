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
