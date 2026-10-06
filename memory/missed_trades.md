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

### SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells
- timestamp: 2026-09-26 06:22 UTC · source: Claude daily review 2026-09-26 · evidence: MODEL_OUTPUT: reading of the engine's two missed-move entries and the failing-cell diagnosis of the same research run · confidence: medium · strategy: liquidity_sweep_reversal v1.0, trend_pullback v1.0 · asset: SOL, ENA · timeframe: 5m, 15m, 1h · regime: WEAK_BULL, TRANSITION · review: 2026-10-03
  The engine marks SOL (+4.8%, 5.5x ATR, from 2026-09-25 07:00) and ENA (+18.4%, 7.5x ATR, from 2026-09-25 08:00) as identifiable. The signals it names came from:
  - liquidity_sweep_reversal v1.0 5m (both moves): 424 backtest trades, -1.15R per trade, loses in every regime with 10+ trades (BACKTEST);
  - trend_pullback v1.0 15m (SOL): 3022 backtest trades, -0.26R per trade (BACKTEST); trend_pullback v1.0 1h (SOL): its numbers are not in today's fact sheet.
  So "identifiable" here does not mean a tested edge saw the move coming. Nothing to change: a signal from a cell that loses over hundreds of trades is not a missed trade.
### SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00
- timestamp: 2026-09-26 06:28 UTC · source: engine: daily research run · evidence: FACT: move of 5.5x the 1H ATR within 12 hours; 46 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: SOL · timeframe: 1h · regime: WEAK_BULL · review: 2026-10-03
  - verdict: identifiable: at least one strategy had a valid signal before the move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: no valid stop / target
  - liquidity_sweep_reversal v1.0 5m: signal
  - rsi2_dip_buy v1.0 1h: blocked by the regime gate
  - rsi2_dip_buy v1.0 30m: blocked by the regime gate
  - trend_pullback v1.0 15m: signal
  - trend_pullback v1.0 1h: signal

### SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00
- timestamp: 2026-09-26 06:28 UTC · source: engine: daily research run · evidence: FACT: move of 7.3x the 1H ATR within 12 hours; 46 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: SUI · timeframe: 1h · regime: WEAK_BULL · review: 2026-10-03
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
- timestamp: 2026-09-26 06:28 UTC · source: engine: daily research run · evidence: FACT: move of 7.5x the 1H ATR within 12 hours; 46 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: ENA · timeframe: 1h · regime: TRANSITION · review: 2026-10-03
  - verdict: identifiable: at least one strategy had a valid signal before the move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: no valid stop / target
  - liquidity_sweep_reversal v1.0 5m: signal
  - rsi2_dip_buy v1.0 15m: blocked by the regime gate
  - trend_pullback v1.0 15m: blocked by the regime gate
  - trend_pullback v1.0 1h: blocked by the regime gate
  - trend_pullback v1.0 30m: blocked by the regime gate

### UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00
- timestamp: 2026-09-26 06:28 UTC · source: engine: daily research run · evidence: FACT: move of 5.3x the 1H ATR within 12 hours; 46 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: UNI · timeframe: 1h · regime: COMPRESSION · review: 2026-10-03
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move (research-only coin)
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: blocked by the regime gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the regime gate

### ZEC up +10.4% (8.6x ATR), 2026-09-26 09:00 -> 2026-09-26 22:00
- timestamp: 2026-09-27 00:50 UTC · source: engine: daily research run · evidence: FACT: move of 8.6x the 1H ATR within 12 hours; 51 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: ZEC · timeframe: 1h · regime: COMPRESSION · review: 2026-10-04
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: blocked by the regime gate
  - liquidity_sweep_reversal v1.0 15m: blocked by the regime gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the regime gate
  - macd_trend_cross v1.0 30m: blocked by the regime gate
  - rsi2_dip_buy v1.0 1h: blocked by the regime gate

### ZEC up +7.1% (6.3x ATR), 2026-09-26 13:00 -> 2026-09-27 02:00
- timestamp: 2026-09-28 00:52 UTC · source: engine: daily research run · evidence: FACT: move of 6.3x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: ZEC · timeframe: 1h · regime: COMPRESSION · review: 2026-10-05
  - verdict: identifiable: at least one strategy had a valid signal before the move
  - macd_trend_cross v1.0 1h: blocked by the regime gate
  - trend_pullback v1.0 4h: signal

### SUI up +10.7% (6.4x ATR), 2026-09-26 20:00 -> 2026-09-27 09:00
- timestamp: 2026-09-28 00:52 UTC · source: engine: daily research run · evidence: FACT: move of 6.4x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: SUI · timeframe: 1h · regime: WEAK_BULL · review: 2026-10-05
  - verdict: identifiable: at least one strategy had a valid signal before the move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: no valid stop / target
  - liquidity_sweep_reversal v1.0 15m: signal
  - rsi2_dip_buy v1.0 15m: blocked by the regime gate
  - rsi2_dip_buy v1.0 1h: blocked by the regime gate
  - rsi2_dip_buy v1.0 30m: blocked by the regime gate

### ENA up +9.0% (5.1x ATR), 2026-09-27 08:00 -> 2026-09-27 19:00
- timestamp: 2026-09-28 00:52 UTC · source: engine: daily research run · evidence: FACT: move of 5.1x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: ENA · timeframe: 1h · regime: UNCLEAR · review: 2026-10-05
  - verdict: identifiable: at least one strategy had a valid signal before the move (research-only coin)
  - S5-SWEEP-MSS-FVG-noSMC v1.0 30m: no valid stop / target
  - bb_squeeze_breakout v1.0 15m: signal
  - ema_9_21_cross v1.0 1h: signal
  - ema_9_21_cross v1.0 5m: blocked by the regime gate
  - macd_trend_cross v1.0 30m: signal
  - trend_pullback v1.0 1h: signal
  - trend_pullback v1.0 30m: signal

### BTC down -2.4% (7.6x ATR), 2026-09-27 21:00 -> 2026-09-28 10:00
- timestamp: 2026-09-29 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 7.6x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: BTC · timeframe: 1h · regime: WEAK_BULL · review: 2026-10-06
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - ema_9_21_cross v1.0 5m: blocked by the regime gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the permission gate

### ZEC down -8.9% (7.0x ATR), 2026-09-28 12:00 -> 2026-09-28 20:00
- timestamp: 2026-09-29 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 7.0x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: ZEC · timeframe: 1h · regime: TRANSITION · review: 2026-10-06
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: blocked by the permission gate
  - liquidity_sweep_reversal v1.0 15m: blocked by the permission gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the permission gate
  - rsi2_dip_buy v1.0 15m: blocked by the regime gate
  - rsi2_dip_buy v1.0 30m: blocked by the regime gate
  - trend_pullback v1.0 15m: blocked by the regime gate

### SOL down -4.1% (5.1x ATR), 2026-09-27 21:00 -> 2026-09-28 10:00
- timestamp: 2026-09-29 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 5.1x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: SOL · timeframe: 1h · regime: WEAK_BULL · review: 2026-10-06
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - liquidity_sweep_reversal v1.0 5m: blocked by the permission gate

### LINK up +13.0% (9.3x ATR), 2026-09-28 09:00 -> 2026-09-28 21:00
- timestamp: 2026-09-29 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 9.3x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: LINK · timeframe: 1h · regime: UNCLEAR · review: 2026-10-06
  - verdict: identifiable: at least one strategy had a valid signal before the move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 1h: blocked by the regime gate
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: signal
  - liquidity_sweep_reversal v1.0 15m: signal
  - liquidity_sweep_reversal v1.0 1h: blocked by the regime gate
  - liquidity_sweep_reversal v1.0 30m: blocked by the regime gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the regime gate
  - rsi2_dip_buy v1.0 1h: blocked by the regime gate
  - rsi2_dip_buy v1.0 4h: blocked by the regime gate

### UNI down -8.6% (5.9x ATR), 2026-09-27 23:00 -> 2026-09-28 10:00
- timestamp: 2026-09-29 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 5.9x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: UNI · timeframe: 1h · regime: RANGE · review: 2026-10-06
  - verdict: not identifiable: no strategy had a setup before the move (research-only coin)

### BNB down -2.6% (7.2x ATR), 2026-09-27 21:00 -> 2026-09-28 10:00
- timestamp: 2026-09-29 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 7.2x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: BNB · timeframe: 1h · regime: WEAK_BULL · review: 2026-10-06
  - verdict: not identifiable: no strategy had a setup before the move (research-only coin)

### ZEC down -11.5% (9.0x ATR), 2026-09-28 13:00 -> 2026-09-29 02:00
- timestamp: 2026-09-30 00:55 UTC · source: engine: daily research run · evidence: FACT: move of 9.0x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: ZEC · timeframe: 1h · regime: TRANSITION · review: 2026-10-07
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: blocked by the permission gate
  - liquidity_sweep_reversal v1.0 15m: blocked by the permission gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the permission gate
  - rsi2_dip_buy v1.0 15m: blocked by the regime gate
  - rsi2_dip_buy v1.0 30m: blocked by the regime gate

### AVAX up +14.3% (7.0x ATR), 2026-09-29 02:00 -> 2026-09-29 12:00
- timestamp: 2026-09-30 00:55 UTC · source: engine: daily research run · evidence: FACT: move of 7.0x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: AVAX · timeframe: 1h · regime: UNCLEAR · review: 2026-10-07
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - S5-SWEEP-MSS-FVG-noSMC v1.0 15m: blocked by the regime gate
  - donchian_breakout-VEXIT-S4 v1.0 30m: blocked by the regime gate

### BTC up +2.7% (6.1x ATR), 2026-09-30 06:00 -> 2026-09-30 13:00
- timestamp: 2026-10-01 00:55 UTC · source: engine: daily research run · evidence: FACT: move of 6.1x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: BTC · timeframe: 1h · regime: RANGE · review: 2026-10-08
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - S5-SWEEP-MSS-FVG v1.0 15m: blocked by the regime gate
  - S5-SWEEP-MSS-FVG-5M v1.0 15m: blocked by the regime gate
  - S5-SWEEP-MSS-FVG-noSMC v1.0 15m: blocked by the regime gate
  - S6-OB-FVG-noSMC v1.0 15m: blocked by the regime gate
  - liquidity_sweep_reversal v1.0 15m: blocked by the permission gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the permission gate

### ENA up +12.9% (7.5x ATR), 2026-09-30 06:00 -> 2026-09-30 14:00
- timestamp: 2026-10-01 00:55 UTC · source: engine: daily research run · evidence: FACT: move of 7.5x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: ENA · timeframe: 1h · regime: UNCLEAR · review: 2026-10-08
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: blocked by the regime gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the permission gate
  - rsi2_dip_buy v1.0 1h: blocked by the regime gate
  - rsi2_dip_buy v1.0 4h: blocked by the regime gate

### BTC down -2.9% (5.2x ATR), 2026-10-02 12:00 -> 2026-10-02 19:00
- timestamp: 2026-10-03 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 5.2x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: BTC · timeframe: 1h · regime: STRONG_BULL · review: 2026-10-10
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 1h: blocked by the permission gate
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: blocked by the permission gate
  - liquidity_sweep_reversal v1.0 15m: blocked by the permission gate

### SOL up +5.4% (6.0x ATR), 2026-10-01 16:00 -> 2026-10-02 05:00
- timestamp: 2026-10-03 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 6.0x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: SOL · timeframe: 1h · regime: RANGE · review: 2026-10-10
  - verdict: identifiable: at least one strategy had a valid signal before the move
  - S5-SWEEP-MSS-FVG-noSMC v1.0 15m: blocked by the regime gate
  - S5-SWEEP-MSS-FVG-noSMC v1.0 30m: blocked by the regime gate
  - S8-PDH-PDL-SWEEP v1.0 1h: signal
  - S8-PDH-PDL-SWEEP-noSMC v1.0 1h: signal
  - liquidity_sweep_reversal v1.0 5m: blocked by the permission gate

### XRP down -4.8% (5.8x ATR), 2026-10-02 09:00 -> 2026-10-02 19:00
- timestamp: 2026-10-03 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 5.8x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: XRP · timeframe: 1h · regime: RANGE · review: 2026-10-10
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 1h: blocked by the permission gate
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: blocked by the permission gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the permission gate

### AVAX down -6.2% (5.5x ATR), 2026-10-02 12:00 -> 2026-10-02 21:00
- timestamp: 2026-10-03 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 5.5x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: AVAX · timeframe: 1h · regime: RANGE · review: 2026-10-10
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move (research-only coin)
  - S8-PDH-PDL-SWEEP-noSMC v1.0 1h: blocked by the permission gate
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: blocked by the permission gate
  - liquidity_sweep_reversal v1.0 1h: blocked by the permission gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the permission gate

### LINK down -6.1% (5.4x ATR), 2026-10-02 12:00 -> 2026-10-02 21:00
- timestamp: 2026-10-03 00:53 UTC · source: engine: daily research run · evidence: FACT: move of 5.4x the 1H ATR within 12 hours; 59 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: LINK · timeframe: 1h · regime: RANGE · review: 2026-10-10
  - verdict: not identifiable: no strategy had a setup before the move (research-only coin)

### BNB up +3.2% (8.0x ATR), 2026-10-03 07:00 -> 2026-10-03 20:00
- timestamp: 2026-10-04 03:56 UTC · source: engine: daily research run · evidence: FACT: move of 8.0x the 1H ATR within 12 hours; 62 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: BNB · timeframe: 1h · regime: UNCLEAR · review: 2026-10-11
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - liquidity_sweep_reversal v1.0 15m: blocked by the regime gate
  - liquidity_sweep_reversal v1.0 5m: blocked by the regime gate

### BTC up +1.6% (7.7x ATR), 2026-10-04 12:00 -> 2026-10-05 00:00
- timestamp: 2026-10-05 00:57 UTC · source: engine: daily research run · evidence: FACT: move of 7.7x the 1H ATR within 12 hours; 68 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: BTC · timeframe: 1h · regime: WEAK_BULL · review: 2026-10-12
  - verdict: identifiable: at least one strategy had a valid signal before the move
  - S5-SWEEP-MSS-FVG-noSMC v1.0 15m: no valid stop / target
  - S5-SWEEP-MSS-FVG-noSMC v1.0 30m: no valid stop / target
  - rsi2_dip_buy v1.0 15m: blocked by the regime gate
  - rsi2_dip_buy v1.0 30m: blocked by the regime gate
  - trend_pullback v1.0 15m: signal

### SUI up +6.8% (7.3x ATR), 2026-10-04 08:00 -> 2026-10-04 16:00
- timestamp: 2026-10-05 00:57 UTC · source: engine: daily research run · evidence: FACT: move of 7.3x the 1H ATR within 12 hours; 68 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: SUI · timeframe: 1h · regime: UNCLEAR · review: 2026-10-12
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
  - S8-PDH-PDL-SWEEP-noSMC v1.0 30m: blocked by the regime gate
  - ema_9_21_cross v1.0 5m: blocked by the regime gate
  - rsi2_dip_buy v1.0 15m: blocked by the regime gate
  - trend_pullback v1.0 15m: blocked by the regime gate
  - trend_pullback v1.0 1h: blocked by the regime gate
  - trend_pullback v1.0 30m: blocked by the regime gate

### Review: LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00
- timestamp: 2026-10-05 17:10 UTC · source: Claude daily review 2026-10-05 · evidence: FACT: the engine's missed-move record (8.0x ATR, 46 tests checked) and today's fact sheet · confidence: medium · strategy: trend_pullback v1.0 · asset: LTC · timeframe: 1h · regime: UNCLEAR · review: 2026-10-12
  - status: KEEP
  - today's evidence: no new information on this move. LTC is a research-only coin, so no live signal could have been sent. The only 'signal' named was trend_pullback v1.0 4h; the other cells were blocked by the regime gate, which is the gate doing its job.
  - action: none. One large move is not a reason to change a rule (section 17.4).

### Review: SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00
- timestamp: 2026-10-05 17:10 UTC · source: Claude daily review 2026-10-05 · evidence: FACT: the engine's missed-move record and the failing-cell diagnosis in today's fact sheet · confidence: medium · strategy: liquidity_sweep_reversal v1.0, trend_pullback v1.0 · asset: SOL · timeframe: 5m, 15m, 1h · regime: WEAK_BULL · review: 2026-10-12
  - status: KEEP
  - today's evidence: the 'signal' that made this move identifiable came from liquidity_sweep_reversal@1.0|5m is still a failing cell today: 346 backtest trades, -1.31R per trade, losing in every regime with 10+ trades (BACKTEST, fact sheet 2026-10-05). A signal from a cell that loses over hundreds of trades is not a missed trade.
  - action: none. (The engine wrote this move twice; this review covers both entries with the same title.)

### Review: ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00
- timestamp: 2026-10-05 17:10 UTC · source: Claude daily review 2026-10-05 · evidence: FACT: the engine's missed-move record and the failing-cell diagnosis in today's fact sheet · confidence: medium · strategy: liquidity_sweep_reversal v1.0, trend_pullback v1.0 · asset: ENA · timeframe: 5m, 15m, 1h · regime: TRANSITION · review: 2026-10-12
  - status: KEEP
  - today's evidence: the 'signal' that made this move identifiable came from liquidity_sweep_reversal@1.0|5m is still a failing cell today: 346 backtest trades, -1.31R per trade, losing in every regime with 10+ trades (BACKTEST, fact sheet 2026-10-05). A signal from a cell that loses over hundreds of trades is not a missed trade.
  - action: none. (The engine wrote this move twice; this review covers both entries with the same title.)

### Review: SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00
- timestamp: 2026-10-05 17:10 UTC · source: Claude daily review 2026-10-05 · evidence: FACT: the engine's missed-move record (setups blocked by the permission gate) · confidence: medium · strategy: S5, S7, bb_squeeze_breakout, trend_pullback v1.0 · asset: SUI · timeframe: 15m, 30m, 1h · regime: WEAK_BULL · review: 2026-10-12
  - status: KEEP
  - today's evidence: every setup was blocked by the permission gate (no approved strategy). Today no strategy is approved either (no approval pack eligible), so the gate would block the same setups again. That is intended.
  - action: none. (The engine wrote this move twice; this review covers both entries.)

### Review: UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00
- timestamp: 2026-10-05 17:10 UTC · source: Claude daily review 2026-10-05 · evidence: FACT: the engine's missed-move record (research-only coin, regime gate) · confidence: medium · strategy: S8-PDH-PDL-SWEEP-noSMC v1.0, liquidity_sweep_reversal v1.0 · asset: UNI · timeframe: 5m, 30m · regime: COMPRESSION · review: 2026-10-12
  - status: KEEP
  - today's evidence: both setups came from failing cells: liquidity_sweep_reversal@1.0|5m is still a failing cell today: 346 backtest trades, -1.31R per trade, losing in every regime with 10+ trades (BACKTEST, fact sheet 2026-10-05); S8-PDH-PDL-SWEEP-noSMC@1.0|30m has 414 trades at -0.46R (BACKTEST). The regime gate blocking them cost nothing.
  - action: none. (The engine wrote this move twice; this review covers both entries.)

### Review: SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells
- timestamp: 2026-10-05 17:10 UTC · source: Claude daily review 2026-10-05 · evidence: MODEL_OUTPUT: today's failing-cell diagnosis re-read against the 2026-09-26 record · confidence: medium · strategy: liquidity_sweep_reversal v1.0, trend_pullback v1.0 · asset: SOL, ENA · timeframe: 5m, 15m, 1h · regime: WEAK_BULL, TRANSITION · review: 2026-10-12
  - status: CONFIRMED
  - today's evidence: liquidity_sweep_reversal@1.0|5m is still a failing cell today: 346 backtest trades, -1.31R per trade, losing in every regime with 10+ trades (BACKTEST, fact sheet 2026-10-05). It is now worse per trade than in the 2026-09-26 record (-1.15R over 424 trades then; the trade count differs because the engine's test window moved). The reading still holds.
  - action: none.

### Review: ZEC up +10.4% (8.6x ATR), 2026-09-26 09:00 -> 2026-09-26 22:00
- timestamp: 2026-10-05 17:10 UTC · source: Claude daily review 2026-10-05 · evidence: FACT: the engine's missed-move record (all setups blocked by the regime gate) · confidence: medium · strategy: S8-PDH-PDL-SWEEP-noSMC, liquidity_sweep_reversal, macd_trend_cross, rsi2_dip_buy v1.0 · asset: ZEC · timeframe: 5m, 15m, 30m, 1h · regime: COMPRESSION · review: 2026-10-12
  - status: KEEP
  - today's evidence: the blocked setups came from cells that fail in today's diagnosis (liquidity_sweep_reversal@1.0|15m is still a failing cell today: 398 backtest trades, -0.53R per trade (BACKTEST, fact sheet 2026-10-05); rsi2_dip_buy@1.0|15m 1482 trades -0.39R, BACKTEST). The regime gate did not cost a tested edge.
  - action: none.

### Review: ZEC up +7.1% (6.3x ATR), 2026-09-26 13:00 -> 2026-09-27 02:00
- timestamp: 2026-10-05 17:10 UTC · source: Claude daily review 2026-10-05 · evidence: FACT: the engine's missed-move record (trend_pullback v1.0 4h signal) · confidence: low · strategy: trend_pullback v1.0 · asset: ZEC · timeframe: 4h · regime: COMPRESSION · review: 2026-10-12
  - status: KEEP
  - today's evidence: the only signal was trend_pullback v1.0 4h, which is not approved, and its 4h numbers are not in today's fact sheet (not available). Nothing shows it is an edge.
  - action: none.

### Review: SUI up +10.7% (6.4x ATR), 2026-09-26 20:00 -> 2026-09-27 09:00
- timestamp: 2026-10-05 17:10 UTC · source: Claude daily review 2026-10-05 · evidence: FACT: the engine's missed-move record (liquidity_sweep_reversal v1.0 15m signal) · confidence: medium · strategy: liquidity_sweep_reversal v1.0 · asset: SUI · timeframe: 15m · regime: WEAK_BULL · review: 2026-10-12
  - status: KEEP
  - today's evidence: the signal came from a failing cell: liquidity_sweep_reversal@1.0|15m is still a failing cell today: 398 backtest trades, -0.53R per trade (BACKTEST, fact sheet 2026-10-05); it loses in every regime with 10+ trades.
  - action: none.

### Review: ENA up +9.0% (5.1x ATR), 2026-09-27 08:00 -> 2026-09-27 19:00
- timestamp: 2026-10-05 17:10 UTC · source: Claude daily review 2026-10-05 · evidence: FACT: the engine's missed-move record (research-only coin) · confidence: medium · strategy: bb_squeeze_breakout, ema_9_21_cross, macd_trend_cross, trend_pullback v1.0 · asset: ENA · timeframe: 15m, 30m, 1h · regime: UNCLEAR · review: 2026-10-12
  - status: KEEP
  - today's evidence: ENA is a research-only coin and its regime was UNCLEAR, where the playbook says no strategy has 30+ backtest trades. Of the cells that signalled, bb_squeeze_breakout@1.0|15m is failing today (384 trades, -0.41R, BACKTEST).
  - action: none.

### BTC up +1.6% (7.5x ATR), 2026-10-04 13:00 -> 2026-10-05 02:00
- timestamp: 2026-10-06 00:56 UTC · source: engine: daily research run · evidence: FACT: move of 7.5x the 1H ATR within 12 hours; 56 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: BTC · timeframe: 1h · regime: WEAK_BULL · review: 2026-10-13
  - verdict: identifiable: at least one strategy had a valid signal before the move
  - S5-SWEEP-MSS-FVG-noSMC v1.0 15m: no valid stop / target
  - S5-SWEEP-MSS-FVG-noSMC v1.0 30m: no valid stop / target
  - ema_9_21_cross v1.0 5m: signal
  - rsi2_dip_buy v1.0 15m: blocked by the regime gate
  - rsi2_dip_buy v1.0 30m: blocked by the regime gate
  - trend_pullback v1.0 15m: signal
  - trend_pullback v1.0 1h: signal
  - trend_pullback v1.0 30m: signal

### ENA up +9.5% (7.8x ATR), 2026-10-05 05:00 -> 2026-10-05 12:00
- timestamp: 2026-10-06 00:56 UTC · source: engine: daily research run · evidence: FACT: move of 7.8x the 1H ATR within 12 hours; 56 strategy / timeframe tests checked · confidence: measured on closed candles · strategy: all · asset: ENA · timeframe: 1h · regime: RANGE · review: 2026-10-13
  - verdict: a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move (research-only coin)
  - liquidity_sweep_reversal v1.0 5m: blocked by the permission gate
