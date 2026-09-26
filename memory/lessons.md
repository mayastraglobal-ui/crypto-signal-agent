# Lessons

Append-only (AGENT_PROMPT.md section 17.7). Only VALIDATED lessons, each with evidence counts (how many strategy / timeframe tests, how many trades, which samples). Written by the reviews (Claude, Phase 14) or the operator - **never by the engine automatically**. Candidate lessons (a tag that is systematic in 2 or more tests) are listed in the report (section 3d) until a review decides. Single stories and opinions are not lessons. A lesson that stops holding gets a NEW record (status REJECTED), the old one stays.

Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` (section 22), then its details. `-` = not applicable.

### A 20% wider stop did not rescue any failing cell (stop_too_tight is a symptom, not the fix)
- timestamp: 2026-09-26 06:22 UTC · source: Claude daily review 2026-09-26 · evidence: BACKTEST_EVIDENCE: 12 tests, 113 to 3022 trades each · confidence: medium · strategy: all · asset: all · timeframe: 5m, 15m, 30m, 1h · regime: - · review: 2026-10-26
  The engine tags many losses stop_too_tight (systematic in 27 strategy / timeframe tests): the stop was hit, then price reached TP1 anyway (5% to 50% of losses per cell in the list below). But in all 12 failing cells with 30+ backtest trades, the engine's measured stop change of +20% still left the average trade below 0R (BACKTEST):
  - liquidity_sweep_reversal@1.0|5m: 424 trades, -1.15R; atr 1.0->1.2 gives -0.96R
  - ema_9_21_cross@1.0|5m: 272 trades, -0.73R; atr 1.5->1.8 gives -0.60R
  - liquidity_sweep_reversal@1.0|15m: 563 trades, -0.51R; atr 1.0->1.2 gives -0.43R
  - S8-PDH-PDL-SWEEP@1.0|30m: 113 trades, -0.50R; buffer_atr 0.2->0.24 gives -0.49R, max_width_atr 3.0->3.6 gives -0.50R
  - liquidity_sweep_reversal@1.0|30m: 327 trades, -0.46R; atr 1.0->1.2 gives -0.39R
  - S8-PDH-PDL-SWEEP-noSMC@1.0|30m: 621 trades, -0.46R; buffer_atr 0.2->0.24 gives -0.45R, max_width_atr 3.0->3.6 gives -0.46R
  - bb_squeeze_breakout@1.0|15m: 551 trades, -0.35R; atr 1.5->1.8 gives -0.25R
  - rsi2_dip_buy@1.0|15m: 2181 trades, -0.34R; atr 2.0->2.4 gives -0.28R
  - trend_pullback@1.0|15m: 3022 trades, -0.26R; atr 1.5->1.8 gives -0.21R
  - liquidity_sweep_reversal@1.0|1h: 313 trades, -0.22R; atr 1.0->1.2 gives -0.14R
  - ema_9_21_cross@1.0|30m: 337 trades, -0.20R; atr 1.5->1.8 gives -0.11R
  - bb_squeeze_breakout@1.0|30m: 486 trades, -0.20R; atr 1.5->1.8 gives -0.17R
  Lesson: a stop_too_tight tag alone is not a reason to widen a stop. In these cells the entry had no edge; a wider stop only made the loss smaller. A refinement for these cells must change the entry or the regime, not the stop. Source: fact sheet 2026-09-26 06:21 UTC (research run 2026-09-26 00:50).
