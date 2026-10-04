# Coin notes

Append-only. How each signal coin tends to behave. The engine adds one block of measured FACTS per coin every week (first scan on Sunday, UTC): daily range, time spent in each regime, which coins it moves with, volume, which strategies were profitable on it. Interpretation is added by the reviews.

Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` (section 22), then its details. `-` = not applicable.

### BTC - weekly facts 2026-09-27
- timestamp: 2026-09-27 00:26 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: BTC · timeframe: 1d, 1h · regime: - · review: 2026-10-27
  - daily range (last 90 days): median 2.5%, 90th percentile 5.0%
  - 1D regime (last 90 days): UNCLEAR 26%, TRANSITION 21%, WEAK_BULL 19%, COMPRESSION 13%, WEAK_BEAR 11%, STRONG_BEAR 8%, RANGE 1%, EXPANSION 1%
  - moves with (1h correlation >= 0.7): BTC+ETH+SOL+XRP
  - 24h volume now: 673M
  - strategies profitable on it in the research run (>= 5 trades): bb_squeeze_breakout@1.0 4h (42 trades, +0.34R); donchian_breakout@1.0 4h (149 trades, +0.26R); ema_9_21_cross@1.0 1h (50 trades, +0.05R); macd_trend_cross@1.0 1h (16 trades, +0.20R)
  - interpretation: (review)

### ETH - weekly facts 2026-09-27
- timestamp: 2026-09-27 00:26 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: ETH · timeframe: 1d, 1h · regime: - · review: 2026-10-27
  - daily range (last 90 days): median 3.3%, 90th percentile 6.0%
  - 1D regime (last 90 days): WEAK_BULL 30%, UNCLEAR 29%, COMPRESSION 14%, STRONG_BEAR 6%, WEAK_BEAR 6%, RANGE 4%, EXPANSION 4%, STRONG_BULL 3%, TRANSITION 3%
  - moves with (1h correlation >= 0.7): BTC+ETH+SOL+XRP
  - 24h volume now: 234M
  - strategies profitable on it in the research run (>= 5 trades): bb_squeeze_breakout@1.0 1h (120 trades, +0.04R); bb_squeeze_breakout@1.0 4h (40 trades, +0.03R); donchian_breakout@1.0 4h (155 trades, +0.18R)
  - interpretation: (review)

### ZEC - weekly facts 2026-09-27
- timestamp: 2026-09-27 00:26 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: ZEC · timeframe: 1d, 1h · regime: - · review: 2026-10-27
  - daily range (last 90 days): median 7.3%, 90th percentile 14.1%
  - 1D regime (last 90 days): STRONG_BULL 36%, WEAK_BULL 27%, COMPRESSION 23%, RANGE 8%, UNCLEAR 3%, EXPANSION 3%
  - moves with (1h correlation >= 0.7): no other signal coin
  - 24h volume now: 247M
  - strategies profitable on it in the research run (>= 5 trades): bb_squeeze_breakout@1.0 1h (79 trades, +0.16R); donchian_breakout@1.0 4h (121 trades, +0.06R); macd_trend_cross@1.0 4h (6 trades, +0.01R); supertrend_flip@1.0 1h (23 trades, +0.28R)
  - interpretation: (review)

### SOL - weekly facts 2026-09-27
- timestamp: 2026-09-27 00:26 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: SOL · timeframe: 1d, 1h · regime: - · review: 2026-10-27
  - daily range (last 90 days): median 3.5%, 90th percentile 7.6%
  - 1D regime (last 90 days): RANGE 21%, WEAK_BULL 18%, TRANSITION 17%, COMPRESSION 16%, WEAK_BEAR 12%, UNCLEAR 12%, EXPANSION 4%
  - moves with (1h correlation >= 0.7): BTC+ETH+SOL+XRP
  - 24h volume now: 221M
  - strategies profitable on it in the research run (>= 5 trades): S6-OB-FVG-noSMC@1.0 15m (5 trades, +0.37R); bb_squeeze_breakout@1.0 4h (26 trades, +0.02R); donchian_breakout@1.0 4h (99 trades, +0.21R); ema_9_21_cross@1.0 15m (46 trades, +0.08R); macd_trend_cross@1.0 1h (14 trades, +0.32R)
  - interpretation: (review)

### XRP - weekly facts 2026-09-27
- timestamp: 2026-09-27 00:26 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: XRP · timeframe: 1d, 1h · regime: - · review: 2026-10-27
  - daily range (last 90 days): median 3.7%, 90th percentile 9.9%
  - 1D regime (last 90 days): TRANSITION 33%, RANGE 27%, WEAK_BEAR 11%, COMPRESSION 8%, UNCLEAR 7%, WEAK_BULL 7%, STRONG_BEAR 4%, EXPANSION 3%
  - moves with (1h correlation >= 0.7): BTC+ETH+SOL+XRP
  - 24h volume now: 181M
  - strategies profitable on it in the research run (>= 5 trades): S8-PDH-PDL-SWEEP-noSMC@1.0 1h (87 trades, +0.10R); S8-PDH-PDL-SWEEP-noSMC@1.0 30m (49 trades, +0.07R); donchian_breakout@1.0 4h (124 trades, +0.08R); macd_trend_cross@1.0 1h (23 trades, +0.25R)
  - interpretation: (review)

### SUI - weekly facts 2026-09-27
- timestamp: 2026-09-27 00:26 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: SUI · timeframe: 1d, 1h · regime: - · review: 2026-10-27
  - daily range (last 90 days): median 5.0%, 90th percentile 10.3%
  - 1D regime (last 90 days): RANGE 27%, TRANSITION 22%, WEAK_BEAR 16%, UNCLEAR 16%, COMPRESSION 10%, EXPANSION 6%, STRONG_BEAR 4%
  - moves with (1h correlation >= 0.7): no other signal coin
  - 24h volume now: 85M
  - strategies profitable on it in the research run (>= 5 trades): S6-OB-FVG-noSMC@1.0 15m (6 trades, +0.31R); S8-PDH-PDL-SWEEP@1.0 1h (16 trades, +0.45R); donchian_breakout@1.0 1h (138 trades, +0.04R); donchian_breakout@1.0 30m (130 trades, +0.05R); trend_pullback@1.0 4h (57 trades, +0.02R)
  - interpretation: (review)

### ENA - weekly facts 2026-09-27
- timestamp: 2026-09-27 00:26 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: ENA · timeframe: 1d, 1h · regime: - · review: 2026-10-27
  - daily range (last 90 days): median 7.6%, 90th percentile 17.8%
  - 1D regime (last 90 days): RANGE 27%, COMPRESSION 20%, TRANSITION 18%, WEAK_BULL 16%, UNCLEAR 11%, EXPANSION 8%, WEAK_BEAR 1%
  - moves with (1h correlation >= 0.7): no other signal coin
  - 24h volume now: 76M
  - strategies profitable on it in the research run (>= 5 trades): S6-OB-FVG-noSMC@1.0 15m (8 trades, +0.47R); bb_squeeze_breakout@1.0 1h (37 trades, +0.28R); bb_squeeze_breakout@1.0 30m (63 trades, +0.01R); bb_squeeze_breakout@1.0 4h (12 trades, +0.21R); donchian_breakout@1.0 30m (139 trades, +0.04R); donchian_breakout@1.0 4h (39 trades, +0.12R); ema_9_21_cross@1.0 1h (9 trades, +0.16R); trend_pullback@1.0 1h (225 trades, +0.10R)
  - interpretation: (review)

### BTC - weekly facts 2026-10-04
- timestamp: 2026-10-04 02:31 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: BTC · timeframe: 1d, 1h · regime: - · review: 2026-11-03
  - daily range (last 90 days): median 2.4%, 90th percentile 4.7%
  - 1D regime (last 90 days): UNCLEAR 26%, WEAK_BULL 23%, TRANSITION 21%, COMPRESSION 13%, WEAK_BEAR 11%, STRONG_BULL 3%, RANGE 1%, EXPANSION 1%
  - moves with (1h correlation >= 0.7): BNB+BTC+ETH+SOL+SUI+XRP
  - 24h volume now: 591M
  - strategies profitable on it in the research run (>= 5 trades): bb_squeeze_breakout@1.0 4h (42 trades, +0.34R); donchian_breakout-VEXIT-S4@1.0 1h (439 trades, +0.01R); donchian_breakout-VEXIT-S4@1.0 4h (159 trades, +0.44R); donchian_breakout-VEXIT-VRVOL@1.0 4h (141 trades, +0.51R); donchian_breakout-VEXIT@1.0 4h (141 trades, +0.51R); donchian_breakout@1.0 4h (150 trades, +0.25R); ema_9_21_cross@1.0 1h (50 trades, +0.05R); macd_trend_cross@1.0 1h (16 trades, +0.20R)
  - interpretation: (review)

### ETH - weekly facts 2026-10-04
- timestamp: 2026-10-04 02:31 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: ETH · timeframe: 1d, 1h · regime: - · review: 2026-11-03
  - daily range (last 90 days): median 3.2%, 90th percentile 6.0%
  - 1D regime (last 90 days): WEAK_BULL 30%, UNCLEAR 29%, COMPRESSION 14%, STRONG_BULL 11%, RANGE 4%, EXPANSION 4%, WEAK_BEAR 3%, TRANSITION 3%
  - moves with (1h correlation >= 0.7): BNB+BTC+ETH+SOL+SUI+XRP
  - 24h volume now: 199M
  - strategies profitable on it in the research run (>= 5 trades): bb_squeeze_breakout@1.0 1h (121 trades, +0.03R); bb_squeeze_breakout@1.0 4h (40 trades, +0.03R); donchian_breakout-VEXIT-S4@1.0 4h (164 trades, +0.38R); donchian_breakout-VEXIT-VRVOL@1.0 4h (153 trades, +0.32R); donchian_breakout-VEXIT@1.0 4h (153 trades, +0.32R); donchian_breakout@1.0 4h (155 trades, +0.18R)
  - interpretation: (review)

### SOL - weekly facts 2026-10-04
- timestamp: 2026-10-04 02:31 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: SOL · timeframe: 1d, 1h · regime: - · review: 2026-11-03
  - daily range (last 90 days): median 3.6%, 90th percentile 7.4%
  - 1D regime (last 90 days): WEAK_BULL 23%, RANGE 21%, TRANSITION 17%, COMPRESSION 16%, WEAK_BEAR 10%, UNCLEAR 7%, EXPANSION 4%, STRONG_BULL 2%
  - moves with (1h correlation >= 0.7): BNB+BTC+ETH+SOL+SUI+XRP
  - 24h volume now: 104M
  - strategies profitable on it in the research run (>= 5 trades): R4-BBRSI@1.0 1h (99 trades, +0.07R); S6-OB-FVG-noSMC@1.0 15m (6 trades, +0.09R); bb_squeeze_breakout@1.0 4h (26 trades, +0.02R); donchian_breakout-VEXIT-S4@1.0 4h (112 trades, +0.20R); donchian_breakout-VEXIT-VRVOL@1.0 4h (95 trades, +0.19R); donchian_breakout-VEXIT@1.0 4h (95 trades, +0.19R); donchian_breakout@1.0 4h (99 trades, +0.21R); ema_9_21_cross@1.0 15m (46 trades, +0.08R)
  - interpretation: (review)

### ZEC - weekly facts 2026-10-04
- timestamp: 2026-10-04 02:31 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: ZEC · timeframe: 1d, 1h · regime: - · review: 2026-11-03
  - daily range (last 90 days): median 7.3%, 90th percentile 14.1%
  - 1D regime (last 90 days): STRONG_BULL 43%, WEAK_BULL 23%, COMPRESSION 23%, RANGE 7%, EXPANSION 3%
  - moves with (1h correlation >= 0.7): no other signal coin
  - 24h volume now: 96M
  - strategies profitable on it in the research run (>= 5 trades): bb_squeeze_breakout@1.0 1h (80 trades, +0.18R); donchian_breakout-VEXIT-S4@1.0 4h (131 trades, +0.07R); donchian_breakout-VEXIT-VRVOL@1.0 4h (119 trades, +0.08R); donchian_breakout-VEXIT@1.0 4h (119 trades, +0.08R); donchian_breakout@1.0 4h (122 trades, +0.06R); macd_trend_cross@1.0 4h (6 trades, +0.01R); supertrend_flip@1.0 1h (23 trades, +0.28R)
  - interpretation: (review)

### BNB - weekly facts 2026-10-04
- timestamp: 2026-10-04 02:31 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: BNB · timeframe: 1d, 1h · regime: - · review: 2026-11-03
  - daily range (last 90 days): median 2.5%, 90th percentile 5.0%
  - 1D regime (last 90 days): RANGE 29%, STRONG_BULL 26%, WEAK_BEAR 11%, TRANSITION 11%, WEAK_BULL 11%, UNCLEAR 9%, COMPRESSION 2%, EXPANSION 1%
  - moves with (1h correlation >= 0.7): BNB+BTC+ETH+SOL+SUI+XRP
  - 24h volume now: 78M
  - strategies profitable on it in the research run (>= 5 trades): S8-PDH-PDL-SWEEP@1.0 30m (5 trades, +0.55R); bb_squeeze_breakout@1.0 4h (28 trades, +0.09R); donchian_breakout-VEXIT-S4@1.0 4h (163 trades, +0.20R); donchian_breakout-VEXIT-VRVOL@1.0 4h (135 trades, +0.24R); donchian_breakout-VEXIT@1.0 4h (135 trades, +0.24R); donchian_breakout@1.0 4h (137 trades, +0.17R); liquidity_sweep_reversal@1.0 1h (32 trades, +0.00R); supertrend_flip@1.0 4h (19 trades, +0.25R)
  - interpretation: (review)

### XRP - weekly facts 2026-10-04
- timestamp: 2026-10-04 02:31 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: XRP · timeframe: 1d, 1h · regime: - · review: 2026-11-03
  - daily range (last 90 days): median 3.5%, 90th percentile 9.9%
  - 1D regime (last 90 days): TRANSITION 41%, RANGE 27%, WEAK_BEAR 9%, COMPRESSION 8%, WEAK_BULL 7%, UNCLEAR 6%, EXPANSION 3%
  - moves with (1h correlation >= 0.7): BNB+BTC+ETH+SOL+SUI+XRP
  - 24h volume now: 67M
  - strategies profitable on it in the research run (>= 5 trades): S8-PDH-PDL-SWEEP-noSMC@1.0 1h (87 trades, +0.10R); S8-PDH-PDL-SWEEP-noSMC@1.0 30m (49 trades, +0.07R); bb_squeeze_breakout@1.0 30m (52 trades, +0.02R); donchian_breakout-VEXIT-S4@1.0 1h (391 trades, +0.03R); donchian_breakout-VEXIT-S4@1.0 30m (142 trades, +0.05R); donchian_breakout-VEXIT-S4@1.0 4h (142 trades, +0.09R); donchian_breakout-VEXIT-VRVOL@1.0 1h (348 trades, +0.00R); donchian_breakout-VEXIT-VRVOL@1.0 30m (127 trades, +0.01R)
  - interpretation: (review)

### SUI - weekly facts 2026-10-04
- timestamp: 2026-10-04 02:31 UTC · source: engine: hourly scan + daily research run · evidence: FACT: measured on closed candles / BACKTEST_EVIDENCE for the strategy lines · confidence: measured · strategy: - · asset: SUI · timeframe: 1d, 1h · regime: - · review: 2026-11-03
  - daily range (last 90 days): median 5.2%, 90th percentile 10.9%
  - 1D regime (last 90 days): RANGE 27%, TRANSITION 23%, UNCLEAR 16%, WEAK_BEAR 12%, COMPRESSION 10%, EXPANSION 10%, WEAK_BULL 2%
  - moves with (1h correlation >= 0.7): BNB+BTC+ETH+SOL+SUI+XRP
  - 24h volume now: 54M
  - strategies profitable on it in the research run (>= 5 trades): R4-CLUC@1.0 30m (30 trades, +0.20R); S6-OB-FVG-noSMC@1.0 15m (6 trades, +0.31R); S8-PDH-PDL-SWEEP@1.0 1h (16 trades, +0.45R); donchian_breakout-VEXIT-S4@1.0 4h (55 trades, +0.18R); donchian_breakout-VEXIT-VRVOL@1.0 1h (134 trades, +0.07R); donchian_breakout-VEXIT-VRVOL@1.0 30m (124 trades, +0.02R); donchian_breakout-VEXIT-VRVOL@1.0 4h (49 trades, +0.13R); donchian_breakout-VEXIT@1.0 1h (134 trades, +0.07R)
  - interpretation: (review)
