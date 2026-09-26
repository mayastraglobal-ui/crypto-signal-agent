# Family gates - calibration (Phase 19 A)

Rules version 1. Written by `family_calibrate.py` from the research run of 2026-09-26 06:28 UTC (per-trade results: branch gh-pages `charts/t`; evidence: branch live-reports `reports/research.json`). Research only - no fee, risk-per-trade or trials-bar change.

## 1. The method (fixed before any card's verdict was computed)

- **Groups** (by the card's `family`): trend = trend_following, momentum, breakout, mtf_pullback; tight = mean_reversion, liquidity_reversal, smc, price_action and any family not listed.
- **Reference** = every historical trade of every card of the group (all timeframes, all coins, the whole tested history), with the average moved to the pass bar (+0.10R). It is "a strategy of this family with exactly the minimum acceptable edge": the family's real spread of wins and losses, no better and no worse an edge. No card is fitted: the losing cards count as much as the winning ones.
- **Every limit = the 95th percentile of the reference** (the same 95% the engine already uses for Monte Carlo), rounded UP (0.5R, 0.05).
  - `max_mc_dd95_per_100_r`: 20,000 random sequences of 100 reference trades -> their worst drawdown -> the 95th percentile.
  - `max_dd_duration_share`: every group cell with >= 30 trades, its OWN time-ordered trades moved to the pass bar (keeps its real bunching of losses in time) -> longest time below a previous peak as a share of its tested period -> the 95th percentile over the cells.
  - `min_recovery_factor: 3` is the operator's number; below is what it means for a pass-bar strategy.
  - loss clustering (tight group): the real longest losing streak must not exceed the 95th percentile of 1,000 random orders of the same trades.
- A card is then measured the same way on its own trades: Monte Carlo 95% worst drawdown of 100 trades drawn from ITS trades (does not grow with the number of trades), its longest drawdown in days / share, its recovery factor.

## 2a. trend group

- 21 cells, 24,377 trades; raw average -0.138R, spread (sd) 1.13R, win rate 47% -> moved to +0.10R
- worst drawdown in 100 trades of the reference: median 8.53R · 75% 11.34R · 90% 14.7R · **95% 16.96R** · 99% 22.11R
  -> `trend max_mc_dd95_per_100_r: 17.0`
- longest drawdown as a share of the tested period (21 cells with >= 30 trades, each at the pass bar): median 30% · 75% 42% · **95% 54%** · max 59%
  -> `trend max_dd_duration_share: 0.55`
- recovery factor of those cells at the pass bar: 25% 1.77 · median 2.31 · 43% reach 3 - so RF >= 3 asks for MORE than the minimum edge (or a long, steady record)
- real histories with clustered losses (streak above 95% of random orders): 33% of the cells
- robustness: leaving out one cell at a time gives [17.0, 17.5]R and [0.55, 0.55] (duration); other random seeds give 95% = 17.17, 17.20, 17.19, 17.07, 17.16R - the limit used is the stricter end

| Cell (moved to the pass bar) | Trades | Moved by | Longest DD | Share | RF | Real streak / 95% random |
|---|---|---|---|---|---|---|
| bb_squeeze_breakout@1.0 15m | 575 | +0.444R | 107 d | 30% | 2.31 | 11 / 15 |
| bb_squeeze_breakout@1.0 1h | 832 | +0.110R | 972 d | 30% | 4.39 | 8 / 11 |
| bb_squeeze_breakout@1.0 30m | 503 | +0.279R | 285 d | 39% | 2.34 | 6 / 13 |
| bb_squeeze_breakout@1.0 4h | 277 | +0.075R | 811 d | 25% | 1.45 | 12 / 10 |
| donchian_breakout@1.0 1h | 3064 | +0.146R | 215 d | 6% | 13.48 | 12 / 14 |
| donchian_breakout@1.0 30m | 1329 | +0.167R | 136 d | 19% | 4.65 | 15 / 14 |
| donchian_breakout@1.0 4h | 1105 | -0.023R | 626 d | 19% | 4.64 | 14 / 11 |
| ema_9_21_cross@1.0 15m | 457 | +0.264R | 95 d | 26% | 2.17 | 14 / 13 |
| ema_9_21_cross@1.0 1h | 335 | +0.234R | 1352 d | 42% | 2.11 | 8 / 13 |
| ema_9_21_cross@1.0 30m | 339 | +0.310R | 427 d | 59% | 2.21 | 11 / 14 |
| ema_9_21_cross@1.0 5m | 276 | +0.816R | 46 d | 52% | 1.66 | 11 / 19 |
| macd_trend_cross@1.0 1h | 186 | +0.188R | 1636 d | 51% | 0.9 | 10 / 10 |
| macd_trend_cross@1.0 30m | 296 | +0.299R | 240 d | 33% | 2.13 | 7 / 11 |
| macd_trend_cross@1.0 4h | 38 | +0.163R | 1657 d | 54% | 1.12 | 3 / 7 |
| supertrend_flip@1.0 1h | 280 | +0.327R | 451 d | 14% | 3.54 | 8 / 13 |
| supertrend_flip@1.0 30m | 163 | +0.262R | 262 d | 37% | 1.77 | 8 / 10 |
| supertrend_flip@1.0 4h | 92 | +0.157R | 1632 d | 50% | 0.92 | 7 / 9 |
| trend_pullback@1.0 15m | 3140 | +0.351R | 112 d | 31% | 3.34 | 22 / 17 |
| trend_pullback@1.0 1h | 6338 | +0.238R | 499 d | 15% | 11.54 | 21 / 17 |
| trend_pullback@1.0 30m | 3534 | +0.290R | 125 d | 17% | 4.76 | 20 / 16 |
| trend_pullback@1.0 4h | 1218 | +0.168R | 658 d | 20% | 4.31 | 10 / 14 |

## 2b. tight group

- 25 cells, 17,363 trades; raw average -0.221R, spread (sd) 0.90R, win rate 46% -> moved to +0.10R
- worst drawdown in 100 trades of the reference: median 5.81R · 75% 7.78R · 90% 10.16R · **95% 12.08R** · 99% 17.34R
  -> `tight max_mc_dd95_per_100_r: 12.5` (computed, not used: the tight group keeps 10R / 8R)
- longest drawdown as a share of the tested period (13 cells with >= 30 trades, each at the pass bar): median 29% · 75% 39% · **95% 58%** · max 59%
  -> `tight max_dd_duration_share: 0.6`
- recovery factor of those cells at the pass bar: 25% 1.17 · median 2.31 · 46% reach 3 - so RF >= 3 asks for MORE than the minimum edge (or a long, steady record)
- real histories with clustered losses (streak above 95% of random orders): 15% of the cells
- robustness: leaving out one cell at a time gives [11.0, 15.0]R and [0.6, 0.6] (duration); other random seeds give 95% = 12.17, 12.11, 12.10, 12.15, 12.11R - the limit used is the stricter end

| Cell (moved to the pass bar) | Trades | Moved by | Longest DD | Share | RF | Real streak / 95% random |
|---|---|---|---|---|---|---|
| S6-OB-FVG-noSMC@1.0 15m | 41 | +0.249R | 184 d | 56% | 0.51 | 9 / 10 |
| S8-PDH-PDL-SWEEP-noSMC@1.0 1h | 795 | +0.314R | 803 d | 26% | 2.0 | 32 / 22 |
| S8-PDH-PDL-SWEEP-noSMC@1.0 30m | 605 | +0.524R | 259 d | 36% | 1.56 | 14 / 26 |
| S8-PDH-PDL-SWEEP@1.0 1h | 283 | +0.225R | 1761 d | 58% | 1.16 | 10 / 18 |
| S8-PDH-PDL-SWEEP@1.0 30m | 111 | +0.656R | 229 d | 33% | 1.17 | 14 / 25 |
| liquidity_sweep_reversal@1.0 15m | 582 | +0.566R | 211 d | 59% | 2.31 | 14 / 16 |
| liquidity_sweep_reversal@1.0 1h | 294 | +0.339R | 919 d | 29% | 3.35 | 11 / 12 |
| liquidity_sweep_reversal@1.0 30m | 333 | +0.534R | 174 d | 24% | 3.7 | 8 / 15 |
| liquidity_sweep_reversal@1.0 5m | 423 | +1.237R | 35 d | 39% | 0.92 | 16 / 24 |
| rsi2_dip_buy@1.0 15m | 2173 | +0.420R | 64 d | 18% | 8.89 | 18 / 22 |
| rsi2_dip_buy@1.0 1h | 6989 | +0.229R | 109 d | 3% | 44.58 | 16 / 14 |
| rsi2_dip_buy@1.0 30m | 2827 | +0.293R | 86 d | 12% | 11.85 | 14 / 15 |
| rsi2_dip_buy@1.0 4h | 1841 | +0.207R | 696 d | 21% | 13.62 | 10 / 12 |

## 3. Old vs new verdict of every cell (the same research run)

Trials bar after the re-evaluation rows (92 trials): t >= 3.267. The new verdict is SHOWN only (shadow mode) - nothing moves on it until the operator's yes after the shadow period.

| Cell | Group | Old | New | Trades | RF | 95% DD / 100 | Longest DD | Live / paper limit | New rule: why not |
|---|---|---|---|---|---|---|---|---|---|
| S5-SWEEP-MSS-FVG-5M@1.0 15m | tight | BACKTESTING | BACKTESTING | 0 | - | -R | 0 d (0%) | 8R | only 0 trades; avg +0.00R/trade (needs +0.10R) |
| S5-SWEEP-MSS-FVG-5M@1.0 30m | tight | BACKTESTING | BACKTESTING | 0 | - | -R | 0 d (0%) | 8R | only 0 trades; avg +0.00R/trade (needs +0.10R) |
| S5-SWEEP-MSS-FVG-noSMC@1.0 15m | tight | BACKTESTING | BACKTESTING | 18 | -0.0 | 27.0R | 212 d (76%) | 8R | only 18 trades; avg -0.00R/trade (needs +0.10R) |
| S5-SWEEP-MSS-FVG-noSMC@1.0 30m | tight | BACKTESTING | BACKTESTING | 13 | -1.0 | 50.1R | 368 d (100%) | 8R | only 13 trades; avg -0.34R/trade (needs +0.10R) |
| S5-SWEEP-MSS-FVG@1.0 15m | tight | BACKTESTING | BACKTESTING | 8 | 0.27 | 34.6R | 233 d (74%) | 8R | only 8 trades; profit factor 1.13 |
| S5-SWEEP-MSS-FVG@1.0 30m | tight | BACKTESTING | BACKTESTING | 4 | -1.0 | 123.6R | 416 d (100%) | 8R | only 4 trades; avg -1.22R/trade (needs +0.10R) |
| S6-OB-FVG-5M@1.0 15m | tight | BACKTESTING | BACKTESTING | 0 | - | -R | 0 d (0%) | 8R | only 0 trades; avg +0.00R/trade (needs +0.10R) |
| S6-OB-FVG-noSMC@1.0 15m | tight | FAILED | FAILED | 41 | -0.57 | 40.3R | 184 d (56%) | 8R | avg -0.15R/trade (needs +0.10R); profit factor 0.78 |
| S6-OB-FVG@1.0 15m | tight | BACKTESTING | BACKTESTING | 0 | - | -R | 0 d (0%) | 8R | only 0 trades; avg +0.00R/trade (needs +0.10R) |
| S7-SILVER-BULLET-5M@1.0 15m | tight | BACKTESTING | BACKTESTING | 0 | - | -R | 0 d (0%) | 8R | only 0 trades; avg +0.00R/trade (needs +0.10R) |
| S7-SILVER-BULLET-noSMC@1.0 15m | tight | BACKTESTING | BACKTESTING | 16 | 0.89 | 24.0R | 265 d (78%) | 8R | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 16 trades |
| S7-SILVER-BULLET@1.0 15m | tight | BACKTESTING | BACKTESTING | 6 | 2.22 | 11.2R | 168 d (76%) | 8R | only 6 trades; longest drawdown 168 days = 76% of the tested period (limit 60%) |
| S8-PDH-PDL-SWEEP-5M@1.0 30m | tight | BACKTESTING | BACKTESTING | 1 | -1.0 | -R | 0 d (0%) | 8R | not cost-viable: fees + slippage 0.86R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades |
| S8-PDH-PDL-SWEEP-noSMC@1.0 1h | tight | FAILED | FAILED | 795 | -0.82 | 54.0R | 2698 d (87%) | 8R | avg -0.21R/trade (needs +0.10R); profit factor 0.74 |
| S8-PDH-PDL-SWEEP-noSMC@1.0 30m | tight | FAILED | FAILED | 605 | -0.97 | 74.0R | 720 d (100%) | 8R | not cost-viable: fees + slippage 0.32R per trade (stop must be ≥ 4x the round-trip cost); avg -0.42R/trade (needs +0.10R) |
| S8-PDH-PDL-SWEEP@1.0 1h | tight | FAILED | FAILED | 283 | -0.55 | 46.2R | 2755 d (91%) | 8R | avg -0.12R/trade (needs +0.10R); profit factor 0.84 |
| S8-PDH-PDL-SWEEP@1.0 30m | tight | FAILED | FAILED | 111 | -0.96 | 81.0R | 689 d (100%) | 8R | avg -0.56R/trade (needs +0.10R); profit factor 0.44 |
| bb_squeeze_breakout@1.0 15m | trend | FAILED | FAILED | 575 | -0.98 | 54.3R | 326 d (90%) | 17R | not cost-viable: fees + slippage 0.29R per trade (stop must be ≥ 4x the round-trip cost); avg -0.34R/trade (needs +0.10R) |
| bb_squeeze_breakout@1.0 1h | trend | FAILED | FAILED | 832 | -0.22 | 24.4R | 2968 d (91%) | 17R | avg -0.01R/trade (needs +0.10R); profit factor 0.98 |
| bb_squeeze_breakout@1.0 30m | trend | FAILED | FAILED | 503 | -1.0 | 39.2R | 723 d (100%) | 17R | avg -0.18R/trade (needs +0.10R); profit factor 0.71 |
| bb_squeeze_breakout@1.0 4h | trend | FAILED | FAILED | 277 | 0.26 | 21.7R | 811 d (25%) | 17R | avg +0.03R/trade (needs +0.10R); profit factor 1.05 |
| donchian_breakout@1.0 1h | trend | FAILED | FAILED | 3064 | -0.82 | 26.4R | 3154 d (96%) | 17R | avg -0.05R/trade (needs +0.10R); profit factor 0.91 |
| donchian_breakout@1.0 30m | trend | FAILED | FAILED | 1329 | -0.78 | 28.7R | 724 d (100%) | 17R | avg -0.07R/trade (needs +0.10R); profit factor 0.88 |
| donchian_breakout@1.0 4h | trend | BACKTESTING | **PAPER_TRADING** | 1105 | 6.02 | 15.7R | 592 d (18%) | 15.7R | passes every gate |
| ema_9_21_cross@1.0 15m | trend | FAILED | FAILED | 457 | -0.96 | 38.0R | 358 d (100%) | 17R | avg -0.16R/trade (needs +0.10R); profit factor 0.73 |
| ema_9_21_cross@1.0 1h | trend | FAILED | FAILED | 335 | -0.8 | 33.6R | 2984 d (92%) | 17R | avg -0.13R/trade (needs +0.10R); profit factor 0.76 |
| ema_9_21_cross@1.0 30m | trend | FAILED | FAILED | 339 | -0.94 | 40.8R | 708 d (98%) | 17R | avg -0.21R/trade (needs +0.10R); profit factor 0.64 |
| ema_9_21_cross@1.0 5m | trend | FAILED | FAILED | 276 | -1.0 | 91.2R | 87 d (100%) | 17R | not cost-viable: fees + slippage 0.55R per trade (stop must be ≥ 4x the round-trip cost); avg -0.72R/trade (needs +0.10R) |
| liquidity_sweep_reversal@1.0 15m | tight | FAILED | FAILED | 582 | -0.99 | 66.8R | 360 d (100%) | 8R | not cost-viable: fees + slippage 0.37R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R) |
| liquidity_sweep_reversal@1.0 1h | tight | FAILED | FAILED | 294 | -0.99 | 43.3R | 3216 d (100%) | 8R | avg -0.24R/trade (needs +0.10R); profit factor 0.61 |
| liquidity_sweep_reversal@1.0 30m | tight | FAILED | FAILED | 333 | -1.0 | 60.1R | 723 d (100%) | 8R | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.43R/trade (needs +0.10R) |
| liquidity_sweep_reversal@1.0 5m | tight | FAILED | FAILED | 423 | -0.99 | 143.6R | 89 d (100%) | 8R | not cost-viable: fees + slippage 1.02R per trade (stop must be ≥ 4x the round-trip cost); avg -1.14R/trade (needs +0.10R) |
| macd_trend_cross@1.0 1h | trend | FAILED | FAILED | 186 | -0.48 | 31.9R | 1862 d (58%) | 17R | avg -0.09R/trade (needs +0.10R); profit factor 0.84 |
| macd_trend_cross@1.0 30m | trend | FAILED | FAILED | 296 | -0.89 | 40.3R | 654 d (91%) | 17R | avg -0.20R/trade (needs +0.10R); profit factor 0.67 |
| macd_trend_cross@1.0 4h | trend | FAILED | FAILED | 38 | -0.5 | 29.0R | 1985 d (65%) | 17R | avg -0.06R/trade (needs +0.10R); profit factor 0.88 |
| rsi2_dip_buy@1.0 15m | tight | FAILED | FAILED | 2173 | -1.0 | 43.2R | 361 d (100%) | 8R | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.32R/trade (needs +0.10R) |
| rsi2_dip_buy@1.0 1h | tight | FAILED | FAILED | 6989 | -0.99 | 23.1R | 3139 d (95%) | 8R | avg -0.13R/trade (needs +0.10R); profit factor 0.54 |
| rsi2_dip_buy@1.0 30m | tight | FAILED | FAILED | 2827 | -1.0 | 29.8R | 725 d (100%) | 8R | avg -0.19R/trade (needs +0.10R); profit factor 0.41 |
| rsi2_dip_buy@1.0 4h | tight | FAILED | FAILED | 1841 | -1.0 | 22.1R | 3257 d (100%) | 8R | avg -0.11R/trade (needs +0.10R); profit factor 0.63 |
| supertrend_flip@1.0 1h | trend | FAILED | FAILED | 280 | -0.94 | 41.0R | 2934 d (92%) | 17R | avg -0.23R/trade (needs +0.10R); profit factor 0.62 |
| supertrend_flip@1.0 30m | trend | FAILED | FAILED | 163 | -0.98 | 34.7R | 680 d (96%) | 17R | avg -0.16R/trade (needs +0.10R); profit factor 0.70 |
| supertrend_flip@1.0 4h | trend | FAILED | FAILED | 92 | -0.35 | 29.2R | 1789 d (55%) | 17R | avg -0.06R/trade (needs +0.10R); profit factor 0.89 |
| trend_pullback@1.0 15m | trend | FAILED | FAILED | 3140 | -0.99 | 45.9R | 362 d (100%) | 17R | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.25R/trade (needs +0.10R) |
| trend_pullback@1.0 1h | trend | FAILED | FAILED | 6338 | -0.97 | 34.6R | 2850 d (87%) | 17R | avg -0.14R/trade (needs +0.10R); profit factor 0.76 |
| trend_pullback@1.0 30m | trend | FAILED | FAILED | 3534 | -0.97 | 39.5R | 722 d (100%) | 17R | avg -0.19R/trade (needs +0.10R); profit factor 0.69 |
| trend_pullback@1.0 4h | trend | FAILED | FAILED | 1218 | -0.64 | 27.5R | 1964 d (60%) | 17R | avg -0.07R/trade (needs +0.10R); profit factor 0.88 |

