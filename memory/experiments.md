# Experiments

Append-only count of every strategy version ever tested (AGENT_PROMPT.md section 11). Each new version of the same idea raises its bar by +0.02R per trade.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0001 | 2026-09-24 20:19 | trend_pullback@1.0 | mtf_pullback | 4h, 1h, 30m, 15m | In a trend confirmed by the higher timeframe, a pullback to the 20 EMA that closes strong again continues the trend. |
| EXP-0002 | 2026-09-24 20:19 | donchian_breakout@1.0 | breakout | 4h, 1h, 30m | A close beyond the 20-candle range with 1.5x volume and ADX > 20 starts a move that is worth following. |
| EXP-0003 | 2026-09-24 20:19 | rsi2_dip_buy@1.0 | mean_reversion | 4h, 1h, 30m, 15m | A sharp 1-2 candle dip (RSI(2) < 10) snaps back towards the short-term average. |
| EXP-0004 | 2026-09-24 20:19 | bb_squeeze_breakout@1.0 | breakout | 4h, 1h, 30m, 15m | After a volatility squeeze (bandwidth in its lowest 20%), a band break with volume in the higher-timeframe direction runs. |
| EXP-0005 | 2026-09-24 20:19 | macd_trend_cross@1.0 | momentum | 4h, 1h, 30m | A MACD cross below zero inside a 200-EMA trend marks the end of a pullback and momentum resuming. |
| EXP-0006 | 2026-09-24 20:19 | supertrend_flip@1.0 | trend_following | 4h, 1h, 30m | A Supertrend flip in the higher-timeframe direction with ADX > 20 catches a new leg of the trend. |
| EXP-0007 | 2026-09-24 20:19 | liquidity_sweep_reversal@1.0 | liquidity_reversal | 1h, 30m, 15m, 5m | A wick through the 20-candle low (high) that closes back inside, with volume, means the stop-hunt failed and price reverses. |
| EXP-0008 | 2026-09-24 20:19 | ema_9_21_cross@1.0 | trend_following | 1h, 30m, 15m, 5m | A 9/21 EMA cross with the 200 EMA trend and ADX > 20 catches trend moves. |
| EXP-0009 | 2026-09-24 20:19 | S5-SWEEP-MSS-FVG@1.0 | smc | 30m, 15m | With the higher timeframes aligned, a sell-side sweep followed by a market-structure shift with displacement, entered on the first retrace into a fair value gap, continues to the opposing liquidity pool. |
| EXP-0010 | 2026-09-24 20:19 | S5-SWEEP-MSS-FVG-noSMC@1.0 (control twin of S5-SWEEP-MSS-FVG) | smc | 30m, 15m | Control: a plain displacement candle in the aligned direction, same exits. S5 must beat this to keep its SMC filter. |
| EXP-0011 | 2026-09-24 20:19 | S6-OB-FVG@1.0 | smc | 15m | HTF-aligned retracements into a 4H order block inside discount (premium for shorts), triggered by a 15m CHoCH, continue in the HTF direction. |
| EXP-0012 | 2026-09-24 20:19 | S6-OB-FVG-noSMC@1.0 (control twin of S6-OB-FVG) | smc | 15m | Control: the same 15m CHoCH without the 4H order-block / discount filter. S6 must beat this. |
| EXP-0013 | 2026-09-24 20:19 | S7-SILVER-BULLET@1.0 | smc | 15m | Inside the London / New York killzones, a sweep followed by displacement and a first retrace into the new gap moves on to the next pool at least 2R away. |
| EXP-0014 | 2026-09-24 20:19 | S7-SILVER-BULLET-noSMC@1.0 (control twin of S7-SILVER-BULLET) | smc | 15m | Control: the same rules at any hour. S7 must beat this to keep its killzone filter. |
| EXP-0015 | 2026-09-24 20:19 | S8-PDH-PDL-SWEEP@1.0 | smc | 1h, 30m | A sweep of the prior-day low (high) that closes back inside the prior-day range reverses to the daily middle and then the opposite extreme. |
| EXP-0016 | 2026-09-24 20:19 | S8-PDH-PDL-SWEEP-noSMC@1.0 (control twin of S8-PDH-PDL-SWEEP) | smc | 1h, 30m | Control: the same reversal from a plain 20-candle low (high) instead of the prior-day level. S8 must beat this. |
| EXP-0017 | 2026-09-25 00:49 | S5-SWEEP-MSS-FVG-5M@1.0 | smc | 30m, 15m | Waiting for a closed 5m bar that confirms the direction (section 8) improves S5-SWEEP-MSS-FVG: fewer false entries and a better price, enough to beat the same strategy without the 5m check. |
| EXP-0018 | 2026-09-25 00:49 | S6-OB-FVG-5M@1.0 | smc | 15m | Waiting for a closed 5m bar that confirms the direction (section 8) improves S6-OB-FVG: fewer false entries and a better price, enough to beat the same strategy without the 5m check. |
| EXP-0019 | 2026-09-25 00:49 | S7-SILVER-BULLET-5M@1.0 | smc | 15m | Waiting for a closed 5m bar that confirms the direction (section 8) improves S7-SILVER-BULLET: fewer false entries and a better price, enough to beat the same strategy without the 5m check. |
| EXP-0020 | 2026-09-25 00:49 | S8-PDH-PDL-SWEEP-5M@1.0 | smc | 30m | Waiting for a closed 5m bar that confirms the direction (section 8) improves S8-PDH-PDL-SWEEP: fewer false entries and a better price, enough to beat the same strategy without the 5m check. |
