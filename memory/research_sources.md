# Research sources

Append-only (AGENT_PROMPT.md section 18). Every source behind a strategy idea: title, URL (only if known - **citations are never invented**), date, claim, evidence class (FACT · RESEARCH_FINDING · BACKTEST_EVIDENCE · CLAIM · HYPOTHESIS · MODEL_OUTPUT · UNVERIFIED_OPINION), derived hypothesis and limitations. The engine adds one record when a strategy version is first tested (from its card); the reviews add external sources. Test results live in `memory/strategy_registry.csv`.

Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` (section 22), then its details. `-` = not applicable.

### trend_pullback@1.0 - Buy the dip inside an up-trend: price pulls back to the 20 EMA and bounces.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card trend_pullback@1.0 · evidence: HYPOTHESIS: not tested when recorded · confidence: untested idea · strategy: trend_pullback v1.0 · asset: research coins · timeframe: 4h, 1h, 30m, 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - title / source: Existing library (before v3), re-versioned under spec v3
  - URL: none recorded
  - claim: In a trend confirmed by the higher timeframe, a pullback to the 20 EMA that closes strong again continues the trend.
  - derived hypothesis (tested): trend_pullback@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR on 4h, 1h, 30m, 15m
  - limitations: Fails in ranges (every touch of the EMA looks like a pullback); late in a trend the bounce is often the last one.
  - test results: `memory/strategy_registry.csv` / report section 3

### donchian_breakout@1.0 - Turtle-style breakout: price closes above the highest high of the last 20 candles with strong volume.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card donchian_breakout@1.0 · evidence: HYPOTHESIS: not tested when recorded · confidence: untested idea · strategy: donchian_breakout v1.0 · asset: research coins · timeframe: 4h, 1h, 30m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION, COMPRESSION · review: 2026-12-24
  - title / source: Existing library (before v3), re-versioned under spec v3
  - URL: none recorded
  - claim: A close beyond the 20-candle range with 1.5x volume and ADX > 20 starts a move that is worth following.
  - derived hypothesis (tested): donchian_breakout@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION, COMPRESSION on 4h, 1h, 30m
  - limitations: Many false breakouts in chop; wide stops; most of the profit comes from a few big trends.
  - test results: `memory/strategy_registry.csv` / report section 3

### rsi2_dip_buy@1.0 - Connors RSI(2): in a long-term up-trend, buy a sharp 1-2 candle dip, sell the bounce.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card rsi2_dip_buy@1.0 · evidence: HYPOTHESIS: not tested when recorded · confidence: untested idea · strategy: rsi2_dip_buy v1.0 · asset: research coins · timeframe: 4h, 1h, 30m, 15m · regime: RANGE, HIGH_VOL_RANGE · review: 2026-12-24
  - title / source: Existing library (before v3), re-versioned under spec v3
  - URL: none recorded
  - claim: A sharp 1-2 candle dip (RSI(2) < 10) snaps back towards the short-term average.
  - derived hypothesis (tested): rsi2_dip_buy@1.0 makes money after fees in regimes RANGE, HIGH_VOL_RANGE on 4h, 1h, 30m, 15m
  - limitations: Catching a falling knife in a real breakdown; many small wins, rare large losses.
  - test results: `memory/strategy_registry.csv` / report section 3

### bb_squeeze_breakout@1.0 - Volatility squeeze: Bollinger Bands get very tight, then price breaks out with volume.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card bb_squeeze_breakout@1.0 · evidence: HYPOTHESIS: not tested when recorded · confidence: untested idea · strategy: bb_squeeze_breakout v1.0 · asset: research coins · timeframe: 4h, 1h, 30m, 15m · regime: COMPRESSION, EXPANSION, STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - title / source: Existing library (before v3), re-versioned under spec v3
  - URL: none recorded
  - claim: After a volatility squeeze (bandwidth in its lowest 20%), a band break with volume in the higher-timeframe direction runs.
  - derived hypothesis (tested): bb_squeeze_breakout@1.0 makes money after fees in regimes COMPRESSION, EXPANSION, STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR on 4h, 1h, 30m, 15m
  - limitations: Squeezes can break both ways (head fakes); rare signals.
  - test results: `memory/strategy_registry.csv` / report section 3

### macd_trend_cross@1.0 - MACD crosses up below zero while price is above the 200 EMA (trend resumes after a pullback).
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card macd_trend_cross@1.0 · evidence: HYPOTHESIS: not tested when recorded · confidence: untested idea · strategy: macd_trend_cross v1.0 · asset: research coins · timeframe: 4h, 1h, 30m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - title / source: Existing library (before v3), re-versioned under spec v3
  - URL: none recorded
  - claim: A MACD cross below zero inside a 200-EMA trend marks the end of a pullback and momentum resuming.
  - derived hypothesis (tested): macd_trend_cross@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR on 4h, 1h, 30m
  - limitations: Lagging; in sideways markets the crosses whipsaw.
  - test results: `memory/strategy_registry.csv` / report section 3

### supertrend_flip@1.0 - Supertrend(10,3) flips to up-trend while ADX shows a real trend.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card supertrend_flip@1.0 · evidence: HYPOTHESIS: not tested when recorded · confidence: untested idea · strategy: supertrend_flip v1.0 · asset: research coins · timeframe: 4h, 1h, 30m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-24
  - title / source: Existing library (before v3), re-versioned under spec v3
  - URL: none recorded
  - claim: A Supertrend flip in the higher-timeframe direction with ADX > 20 catches a new leg of the trend.
  - derived hypothesis (tested): supertrend_flip@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION on 4h, 1h, 30m
  - limitations: Flips late; gives back a lot before the exit flip.
  - test results: `memory/strategy_registry.csv` / report section 3

### liquidity_sweep_reversal@1.0 - Stop-hunt reversal: price dips below the 20-candle low, then closes back above it.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card liquidity_sweep_reversal@1.0 · evidence: HYPOTHESIS: not tested when recorded · confidence: untested idea · strategy: liquidity_sweep_reversal v1.0 · asset: research coins · timeframe: 1h, 30m, 15m, 5m · regime: RANGE, HIGH_VOL_RANGE, WEAK_BULL, WEAK_BEAR, STRONG_BULL, STRONG_BEAR, TRANSITION · review: 2026-12-24
  - title / source: Existing library (before v3), re-versioned under spec v3
  - URL: none recorded
  - claim: A wick through the 20-candle low (high) that closes back inside, with volume, means the stop-hunt failed and price reverses.
  - derived hypothesis (tested): liquidity_sweep_reversal@1.0 makes money after fees in regimes RANGE, HIGH_VOL_RANGE, WEAK_BULL, WEAK_BEAR, STRONG_BULL, STRONG_BEAR, TRANSITION on 1h, 30m, 15m, 5m
  - limitations: Strong trends keep sweeping lows without reversing; low timeframes are expensive after fees.
  - test results: `memory/strategy_registry.csv` / report section 3

### ema_9_21_cross@1.0 - Classic 9/21 EMA crossover, only with the 200 EMA trend and ADX filter.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card ema_9_21_cross@1.0 · evidence: HYPOTHESIS: not tested when recorded · confidence: untested idea · strategy: ema_9_21_cross v1.0 · asset: research coins · timeframe: 1h, 30m, 15m, 5m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-24
  - title / source: Existing library (before v3), re-versioned under spec v3
  - URL: none recorded
  - claim: A 9/21 EMA cross with the 200 EMA trend and ADX > 20 catches trend moves.
  - derived hypothesis (tested): ema_9_21_cross@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION on 1h, 30m, 15m, 5m
  - limitations: Whipsaws a lot; kept mainly as a simple benchmark.
  - test results: `memory/strategy_registry.csv` / report section 3

### S5-SWEEP-MSS-FVG@1.0 - Sweep of liquidity -> structure shift (CHoCH with displacement) -> first pullback into the gap.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S5-SWEEP-MSS-FVG@1.0 · evidence: CLAIM: not tested when recorded · confidence: untested idea · strategy: S5-SWEEP-MSS-FVG v1.0 · asset: research coins · timeframe: 30m, 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-24
  - title / source: ICT material (CLAIM), AGENT_PROMPT.md section 9 S5
  - URL: none recorded
  - claim: With the higher timeframes aligned, a sell-side sweep followed by a market-structure shift with displacement, entered on the first retrace into a fair value gap, continues to the opposing liquidity pool.
  - derived hypothesis (tested): S5-SWEEP-MSS-FVG@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION on 30m, 15m, and beats its control twin S5-SWEEP-MSS-FVG-noSMC
  - limitations: Needs a clean sweep and shift; in chop the shift fails. Low timeframes pay a lot of fees per R.
  - test results: `memory/strategy_registry.csv` / report section 3

### S5-SWEEP-MSS-FVG-noSMC@1.0 - S5 without the sweep, structure shift and gap: enter after any strong candle in the trend direction.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S5-SWEEP-MSS-FVG-noSMC@1.0 · evidence: HYPOTHESIS: control twin - a benchmark, not an idea · confidence: untested idea · strategy: S5-SWEEP-MSS-FVG-noSMC v1.0 · asset: research coins · timeframe: 30m, 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-24
  - title / source: Control twin of S5 (AGENT_PROMPT.md section 9 control-twin rule)
  - URL: none recorded
  - claim: Control: a plain displacement candle in the aligned direction, same exits. S5 must beat this to keep its SMC filter.
  - derived hypothesis (tested): S5-SWEEP-MSS-FVG-noSMC@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION on 30m, 15m
  - limitations: A benchmark, not an idea to trade.
  - test results: `memory/strategy_registry.csv` / report section 3

### S6-OB-FVG@1.0 - Price pulls back into a 4H order block in the cheap half of the 4H range, then 15m structure turns up.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S6-OB-FVG@1.0 · evidence: CLAIM: not tested when recorded · confidence: untested idea · strategy: S6-OB-FVG v1.0 · asset: research coins · timeframe: 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - title / source: ICT material (CLAIM), AGENT_PROMPT.md section 9 S6
  - URL: none recorded
  - claim: HTF-aligned retracements into a 4H order block inside discount (premium for shorts), triggered by a 15m CHoCH, continue in the HTF direction.
  - derived hypothesis (tested): S6-OB-FVG@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR on 15m, and beats its control twin S6-OB-FVG-noSMC
  - limitations: Fails in ranges; order blocks are easy to over-use.
  - test results: `memory/strategy_registry.csv` / report section 3

### S6-OB-FVG-noSMC@1.0 - S6 without the 4H order block and discount filter.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S6-OB-FVG-noSMC@1.0 · evidence: HYPOTHESIS: control twin - a benchmark, not an idea · confidence: untested idea · strategy: S6-OB-FVG-noSMC v1.0 · asset: research coins · timeframe: 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - title / source: Control twin of S6 (AGENT_PROMPT.md section 9 control-twin rule)
  - URL: none recorded
  - claim: Control: the same 15m CHoCH without the 4H order-block / discount filter. S6 must beat this.
  - derived hypothesis (tested): S6-OB-FVG-noSMC@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR on 15m
  - limitations: A benchmark, not an idea to trade.
  - test results: `memory/strategy_registry.csv` / report section 3

### S7-SILVER-BULLET@1.0 - Killzone only: liquidity sweep -> strong candle -> entry on the first pullback into its gap.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S7-SILVER-BULLET@1.0 · evidence: CLAIM: not tested when recorded · confidence: untested idea · strategy: S7-SILVER-BULLET v1.0 · asset: research coins · timeframe: 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-24
  - title / source: ICT Silver Bullet / killzone material (CLAIM), AGENT_PROMPT.md section 9 S7
  - URL: none recorded
  - claim: Inside the London / New York killzones, a sweep followed by displacement and a first retrace into the new gap moves on to the next pool at least 2R away.
  - derived hypothesis (tested): S7-SILVER-BULLET@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION on 15m, and beats its control twin S7-SILVER-BULLET-noSMC
  - limitations: Few signals (short windows); 15m fees are large compared with the stop.
  - test results: `memory/strategy_registry.csv` / report section 3

### S7-SILVER-BULLET-noSMC@1.0 - S7 without the killzone time filter.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S7-SILVER-BULLET-noSMC@1.0 · evidence: HYPOTHESIS: control twin - a benchmark, not an idea · confidence: untested idea · strategy: S7-SILVER-BULLET-noSMC v1.0 · asset: research coins · timeframe: 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-24
  - title / source: Control twin of S7 (AGENT_PROMPT.md section 9 control-twin rule)
  - URL: none recorded
  - claim: Control: the same rules at any hour. S7 must beat this to keep its killzone filter.
  - derived hypothesis (tested): S7-SILVER-BULLET-noSMC@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION on 15m
  - limitations: A benchmark, not an idea to trade.
  - test results: `memory/strategy_registry.csv` / report section 3

### S8-PDH-PDL-SWEEP@1.0 - Price pokes below yesterday's low, then closes back inside yesterday's range: aim for the middle, then yesterday's high.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S8-PDH-PDL-SWEEP@1.0 · evidence: CLAIM: not tested when recorded · confidence: untested idea · strategy: S8-PDH-PDL-SWEEP v1.0 · asset: research coins · timeframe: 1h, 30m · regime: RANGE, HIGH_VOL_RANGE, WEAK_BULL, WEAK_BEAR, STRONG_BULL, STRONG_BEAR, TRANSITION · review: 2026-12-24
  - title / source: ICT material (CLAIM), AGENT_PROMPT.md section 9 S8
  - URL: none recorded
  - claim: A sweep of the prior-day low (high) that closes back inside the prior-day range reverses to the daily middle and then the opposite extreme.
  - derived hypothesis (tested): S8-PDH-PDL-SWEEP@1.0 makes money after fees in regimes RANGE, HIGH_VOL_RANGE, WEAK_BULL, WEAK_BEAR, STRONG_BULL, STRONG_BEAR, TRANSITION on 1h, 30m, and beats its control twin S8-PDH-PDL-SWEEP-noSMC
  - limitations: Trend days break through yesterday's levels and never come back.
  - test results: `memory/strategy_registry.csv` / report section 3

### S8-PDH-PDL-SWEEP-noSMC@1.0 - S8 with an ordinary 20-candle low/high instead of yesterday's low/high.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S8-PDH-PDL-SWEEP-noSMC@1.0 · evidence: HYPOTHESIS: control twin - a benchmark, not an idea · confidence: untested idea · strategy: S8-PDH-PDL-SWEEP-noSMC v1.0 · asset: research coins · timeframe: 1h, 30m · regime: RANGE, HIGH_VOL_RANGE, WEAK_BULL, WEAK_BEAR, STRONG_BULL, STRONG_BEAR, TRANSITION · review: 2026-12-24
  - title / source: Control twin of S8 (AGENT_PROMPT.md section 9 control-twin rule)
  - URL: none recorded
  - claim: Control: the same reversal from a plain 20-candle low (high) instead of the prior-day level. S8 must beat this.
  - derived hypothesis (tested): S8-PDH-PDL-SWEEP-noSMC@1.0 makes money after fees in regimes RANGE, HIGH_VOL_RANGE, WEAK_BULL, WEAK_BEAR, STRONG_BULL, STRONG_BEAR, TRANSITION on 1h, 30m
  - limitations: A benchmark, not an idea to trade.
  - test results: `memory/strategy_registry.csv` / report section 3

### S5-SWEEP-MSS-FVG-5M@1.0 - S5-SWEEP-MSS-FVG + 5-minute entry confirmation.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S5-SWEEP-MSS-FVG-5M@1.0 · evidence: CLAIM: not tested when recorded · confidence: untested idea · strategy: S5-SWEEP-MSS-FVG-5M v1.0 · asset: research coins · timeframe: 30m, 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-24
  - title / source: AGENT_PROMPT.md section 8 (5-minute entry confirmation) on top of S5-SWEEP-MSS-FVG v1.0
  - URL: none recorded
  - claim: Waiting for a closed 5m bar that confirms the direction (section 8) improves S5-SWEEP-MSS-FVG: fewer false entries and a better price, enough to beat the same strategy without the 5m check.
  - derived hypothesis (tested): S5-SWEEP-MSS-FVG-5M@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION on 30m, 15m, and beats its control twin S5-SWEEP-MSS-FVG
  - limitations: Misses fast moves that never look back; only 90 days of 5m history to test on; 5m fees are the same per trade but the stop is not smaller.
  - test results: `memory/strategy_registry.csv` / report section 3

### S6-OB-FVG-5M@1.0 - S6-OB-FVG + 5-minute entry confirmation.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S6-OB-FVG-5M@1.0 · evidence: CLAIM: not tested when recorded · confidence: untested idea · strategy: S6-OB-FVG-5M v1.0 · asset: research coins · timeframe: 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - title / source: AGENT_PROMPT.md section 8 (5-minute entry confirmation) on top of S6-OB-FVG v1.0
  - URL: none recorded
  - claim: Waiting for a closed 5m bar that confirms the direction (section 8) improves S6-OB-FVG: fewer false entries and a better price, enough to beat the same strategy without the 5m check.
  - derived hypothesis (tested): S6-OB-FVG-5M@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR on 15m, and beats its control twin S6-OB-FVG
  - limitations: Misses fast moves that never look back; only 90 days of 5m history to test on; 5m fees are the same per trade but the stop is not smaller.
  - test results: `memory/strategy_registry.csv` / report section 3

### S7-SILVER-BULLET-5M@1.0 - S7-SILVER-BULLET + 5-minute entry confirmation.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S7-SILVER-BULLET-5M@1.0 · evidence: CLAIM: not tested when recorded · confidence: untested idea · strategy: S7-SILVER-BULLET-5M v1.0 · asset: research coins · timeframe: 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-24
  - title / source: AGENT_PROMPT.md section 8 (5-minute entry confirmation) on top of S7-SILVER-BULLET v1.0
  - URL: none recorded
  - claim: Waiting for a closed 5m bar that confirms the direction (section 8) improves S7-SILVER-BULLET: fewer false entries and a better price, enough to beat the same strategy without the 5m check.
  - derived hypothesis (tested): S7-SILVER-BULLET-5M@1.0 makes money after fees in regimes STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION on 15m, and beats its control twin S7-SILVER-BULLET
  - limitations: Misses fast moves that never look back; only 90 days of 5m history to test on; 5m fees are the same per trade but the stop is not smaller.
  - test results: `memory/strategy_registry.csv` / report section 3

### S8-PDH-PDL-SWEEP-5M@1.0 - S8-PDH-PDL-SWEEP + 5-minute entry confirmation.
- timestamp: 2026-09-25 00:49 UTC · source: strategies.yaml card S8-PDH-PDL-SWEEP-5M@1.0 · evidence: CLAIM: not tested when recorded · confidence: untested idea · strategy: S8-PDH-PDL-SWEEP-5M v1.0 · asset: research coins · timeframe: 30m · regime: RANGE, HIGH_VOL_RANGE, WEAK_BULL, WEAK_BEAR, STRONG_BULL, STRONG_BEAR, TRANSITION · review: 2026-12-24
  - title / source: AGENT_PROMPT.md section 8 (5-minute entry confirmation) on top of S8-PDH-PDL-SWEEP v1.0
  - URL: none recorded
  - claim: Waiting for a closed 5m bar that confirms the direction (section 8) improves S8-PDH-PDL-SWEEP: fewer false entries and a better price, enough to beat the same strategy without the 5m check.
  - derived hypothesis (tested): S8-PDH-PDL-SWEEP-5M@1.0 makes money after fees in regimes RANGE, HIGH_VOL_RANGE, WEAK_BULL, WEAK_BEAR, STRONG_BULL, STRONG_BEAR, TRANSITION on 30m, and beats its control twin S8-PDH-PDL-SWEEP
  - limitations: Misses fast moves that never look back; only 90 days of 5m history to test on; 5m fees are the same per trade but the stop is not smaller.
  - test results: `memory/strategy_registry.csv` / report section 3

### [R1] Microsoft RD-Agent - the research loop (hypothesis -> experiment -> feedback -> next hypothesis)
- timestamp: 2026-09-25 16:00 UTC · source: https://github.com/microsoft/RD-Agent (commit 484776c211e4fbbeef03e0ec00d6bbee7362a4f4, 2026-09-23) · evidence: FACT: read in the project's own code and docs at that commit · confidence: high for what the code does; its results were not checked · strategy: - · asset: - · timeframe: - · regime: - · review: 2026-12-24
  - opened (Phase 18 build session): the repository at the commit above - docs/scens/quant_agent_fin.rst, rdagent/core/proposal.py, rdagent/scenarios/qlib/proposal/bandit.py and quant_proposal.py. NOT opened: the paper arxiv.org/abs/2505.15155 and the readthedocs page (this environment could not reach them) - nothing from them is cited.
  - what it does (code): a Hypothesis has a reason; after each experiment a HypothesisFeedback records observations, an evaluation of the hypothesis, a new hypothesis, a decision (yes / no) and a reason. A Trace keeps every experiment with links to its parent experiments (a tree), so the next idea starts from a known result. In the finance scenario a bandit (Thompson sampling) chooses whether the next step works on factors or on the model.
  - what we take (Phase 18 A): every lab card names its `parent:`; after a card is tested the daily review writes a `Feedback: <id>@<version>` record in memory/experiments.md (hypothesis -> result -> what it teaches -> next hypothesis or "stop this line"); the weekly email shows the chains.
  - what we deliberately do NOT take: code written by a language model and run automatically; machine-learning forecast models; the bandit choosing the next step by itself (our idea factories keep the operator's quotas); any copied code (none was copied).
  - licence: MIT.

### [R2] TradingAgents (Tauric Research) - bull vs bear debate and a risk team
- timestamp: 2026-09-25 16:00 UTC · source: https://github.com/TauricResearch/TradingAgents (commit 35543d0248bf89fcb92b17a15858ad0c0e940687, 2026-09-24) · evidence: FACT: read in the project's own code at that commit · confidence: high for what the code does; its results were not checked · strategy: - · asset: - · timeframe: - · regime: - · review: 2026-12-24
  - opened (Phase 18 build session): tradingagents/agents/researchers/bull_researcher.py and bear_researcher.py, managers/research_manager.py and portfolio_manager.py, the risk_mgmt folder (aggressive, conservative and neutral debators), graph/conditional_logic.py. NOT opened: the paper arxiv.org/abs/2412.20138 (not reachable from this environment) - nothing from it is cited.
  - what it does (code): a bull analyst and a bear analyst (language-model prompts) argue in turns for a set number of rounds; a research manager judges the debate and gives a rating (Buy / Overweight / Hold / Underweight / Sell); then three risk debators argue and a portfolio manager makes the final rating. The risk team debates - it has no hard veto; the manager weighs it.
  - what we take (Phase 18 A): every briefing verdict and every approval pack shows a Bull case and a Bear case, and a Risk manager line.
  - what we deliberately do NOT take: free-text arguments and ratings from a language model - our cases contain ONLY the engine's numbers; news / sentiment analysts as evidence; a manager who can overrule risk - our risk manager is a fixed VETO (event within 60 min, heat full, regime against, data not GOOD, day / week limit near) that only ever says "not now"; any copied code (none was copied).
  - licence: Apache-2.0.

### [R8] Microsoft Qlib - how professionals organise factor research (reading only)
- timestamp: 2026-09-25 16:00 UTC · source: https://github.com/microsoft/qlib (commit be725493eb1a6bbb42bf11b37aa7669f59610ff1, 2026-09-16) · evidence: FACT: read in the project's README and code at that commit · confidence: high for what the project describes; its results were not checked · strategy: - · asset: - · timeframe: - · regime: - · review: 2026-12-24
  - opened (Phase 18 build session): README.md and qlib/workflow/recorder.py.
  - what it does: `qrun` runs a whole research workflow (dataset, model, backtest, analysis) from ONE config file; a Recorder logs every experiment with its parameters, metrics, files and a status (SCHEDULED, RUNNING, FINISHED, FAILED), modelled on mlflow; the README lists a point-in-time database so old data is seen as it was known then.
  - what we take: nothing new to build in Part A - it confirms our design: every test is recorded with its exact rules (memory/strategy_registry.csv, fingerprinted), counted (memory/trials.csv) and linked to where it came from (the research loop's `parent:`).
  - what we deliberately do NOT take: forecasting models (LightGBM and the neural networks), the Alpha158 feature set as a black box, mlflow as a dependency; any copied code (none was copied).
  - licence: MIT.

### [R3] freqtrade - lookahead-analysis and recursive-analysis (ideas only, GPL-3.0)
- timestamp: 2026-09-25 17:30 UTC · source: https://github.com/freqtrade/freqtrade (commit c0a991f5632cb900075ff2864b6671ed71a319d7, 2026-09-24) · evidence: FACT: read in the project's own documentation at that commit · confidence: high for what the tools do; their results were not checked · strategy: - · asset: - · timeframe: - · regime: - · review: 2026-12-24
  - opened (Phase 18 B build session): docs/lookahead-analysis.md and docs/recursive-analysis.md in the repository (the same text the freqtrade.io pages show). The website itself was not opened.
  - what it does: lookahead-analysis runs a baseline backtest, then re-runs it separately for each entry / exit signal and compares the indicator values and signals; any change means the strategy looked at future candles (examples it names: shift(-10), whole-column mean / min / max without a rolling window). recursive-analysis computes the indicators with different amounts of start-up history and reports how much the last values differ (EMA-type indicators need enough history to settle; zero difference is not always reachable).
  - what we take (Phase 18 B): engine/bias.py - the history is cut right after 6 signal candles and every rule and stop / target level must answer exactly the same on every shared candle; the history is started 500 candles later and, after 1000 settling candles, at most 0.1% of candles may flip. A card that fails is BIASED: FAILED on every timeframe, for good.
  - what we deliberately do NOT take: its code (GPL-3.0 - nothing was copied); per-signal re-runs of the full backtest (we cut the history once per chosen signal candle and compare every rule at once, which is cheaper); reporting only percentage differences - a lookahead difference here is a hard failure.
  - licence: GPL-3.0 (ideas only).

### [R5] Jesse - Monte Carlo trade-order shuffling and rule significance testing
- timestamp: 2026-09-25 17:30 UTC · source: https://github.com/jesse-ai/docs (commit dbd653d3dea5b0c513b4a6dbcbc971e42ab50196, 2026-09-23) and https://github.com/jesse-ai/jesse (commit b6d89c21386f2d6db7403bb06f1cfadf08e4fea2) · evidence: FACT: read in the project's own documentation at that commit · confidence: high for what the tools do; their results were not checked · strategy: - · asset: - · timeframe: - · regime: - · review: 2026-12-24
  - opened (Phase 18 B build session): docs/docs/monte-carlo/trade-order-shuffling.md and interpreting-results.md, docs/docs/rule-significance-testing/index.md and interpreting-results.md (the source of docs.jesse.trade). The website itself was not opened.
  - what it does: trade-order shuffling keeps every trade's result and only shuffles their order (at least 1000 scenarios recommended), rebuilds the equity curve and shows worst 5% / median / best 5% of drawdown and other metrics; an original result far better than the best 5% is read as overfitting. Its rule significance test is DIFFERENT from our Part B item 6: it asks whether an entry rule's signals predict the NEXT bar's detrended return, with a stationary-bootstrap p-value.
  - what we take (Phase 18 B): 1000 shuffles of each cell's trades -> 95% worst drawdown and the longest losing streak at the 95% level ("expected worst losing streak" in approval packs); PAPER_TRADING also needs the 95% worst drawdown within the risk limit. For rule significance we follow the operator's plan instead (each entry rule removed in turn, the whole backtest re-run; a rule that does not improve the average trade is flagged and the simpler card queued in the lab).
  - what we deliberately do NOT take: its code (nothing was copied), candle-based Monte Carlo (synthetic price paths), the next-bar bootstrap p-value (a possible later hypothesis - it would be one more trial for the trials counter).
  - licence: MIT.
