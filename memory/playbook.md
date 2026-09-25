# Regime playbook (generated - do not edit)

Written by the daily research run 2026-09-25 00:49 UTC from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## STRONG_BULL
- families (all their trades in this regime): breakout -0.11R (689); mtf_pullback -0.23R (1837); trend_following -0.45R (189); liquidity_reversal -1.01R (142)
- made money here: donchian_breakout v1.0 4h +0.12R over 68 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -1.18R over 96 trades; liquidity_sweep_reversal v1.0 15m -0.67R over 46 trades; ema_9_21_cross v1.0 5m -0.58R over 85 trades; ema_9_21_cross v1.0 30m -0.56R over 35 trades; bb_squeeze_breakout v1.0 15m -0.35R over 65 trades; trend_pullback v1.0 15m -0.28R over 431 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

## WEAK_BULL
- families (all their trades in this regime): breakout -0.09R (1947); momentum -0.17R (250); mtf_pullback -0.18R (4902); trend_following -0.28R (657); smc -0.71R (104); liquidity_reversal -1.00R (303)
- made money here: donchian_breakout v1.0 4h +0.13R over 247 trades [BACKTESTING]; bb_squeeze_breakout v1.0 4h +0.12R over 123 trades [FAILED]; trend_pullback v1.0 4h +0.03R over 540 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -1.19R over 169 trades; liquidity_sweep_reversal v1.0 15m -0.84R over 84 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.80R over 72 trades; ema_9_21_cross v1.0 5m -0.73R over 100 trades; liquidity_sweep_reversal v1.0 30m -0.65R over 50 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 1h -0.51R over 32 trades
- no trade looks like: no setup, or the higher timeframes disagree

## RANGE
- families (all their trades in this regime): mean_reversion -0.18R (13487); smc -0.41R (794); liquidity_reversal -0.46R (388)
- made money here: NOTHING - no tested strategy made money in this regime
- lost money here: liquidity_sweep_reversal v1.0 5m -1.07R over 53 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.59R over 231 trades; liquidity_sweep_reversal v1.0 15m -0.40R over 112 trades; liquidity_sweep_reversal v1.0 30m -0.39R over 101 trades; rsi2_dip_buy v1.0 15m -0.36R over 2018 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 1h -0.35R over 354 trades
- no trade looks like: price in the middle of the range; breakouts without volume; and here NO strategy has shown an edge - standing aside IS the playbook

## HIGH_VOL_RANGE
- families (all their trades in this regime): mean_reversion -0.11R (741)
- made money here: NOTHING - no tested strategy made money in this regime
- lost money here: rsi2_dip_buy v1.0 15m -0.26R over 125 trades; rsi2_dip_buy v1.0 30m -0.12R over 146 trades; rsi2_dip_buy v1.0 4h -0.12R over 131 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise; and here NO strategy has shown an edge - standing aside IS the playbook

## WEAK_BEAR
- families (all their trades in this regime): momentum -0.05R (258); breakout -0.08R (2189); mtf_pullback -0.16R (5674); trend_following -0.17R (767); smc -0.25R (170); liquidity_reversal -0.76R (241)
- made money here: donchian_breakout v1.0 4h +0.11R over 249 trades [BACKTESTING]; bb_squeeze_breakout v1.0 4h +0.04R over 124 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -1.83R over 43 trades; ema_9_21_cross v1.0 5m -1.00R over 35 trades; liquidity_sweep_reversal v1.0 30m -0.54R over 48 trades; liquidity_sweep_reversal v1.0 15m -0.53R over 150 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.40R over 100 trades; bb_squeeze_breakout v1.0 15m -0.39R over 240 trades
- no trade looks like: no setup, or the higher timeframes disagree

## STRONG_BEAR
- families (all their trades in this regime): trend_following -0.07R (135); mtf_pullback -0.17R (1874); breakout -0.19R (558); liquidity_reversal -0.42R (67)
- made money here: NOTHING - no tested strategy made money in this regime
- lost money here: liquidity_sweep_reversal v1.0 15m -0.42R over 67 trades; bb_squeeze_breakout v1.0 15m -0.41R over 97 trades; bb_squeeze_breakout v1.0 30m -0.35R over 47 trades; trend_pullback v1.0 15m -0.23R over 654 trades; ema_9_21_cross v1.0 30m -0.22R over 39 trades; trend_pullback v1.0 4h -0.20R over 110 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend; and here NO strategy has shown an edge - standing aside IS the playbook

## EXPANSION
- families (all their trades in this regime): breakout +0.02R (2105); trend_following -0.24R (98)
- made money here: donchian_breakout v1.0 4h +0.08R over 537 trades [BACKTESTING]; donchian_breakout v1.0 1h +0.03R over 1271 trades [FAILED]
- lost money here: supertrend_flip v1.0 1h -0.30R over 41 trades; ema_9_21_cross v1.0 1h -0.20R over 57 trades
- no trade looks like: the move is already several ATRs old (late entry)

## COMPRESSION
- families (all their trades in this regime): breakout -0.42R (106)
- made money here: NOTHING - no tested strategy made money in this regime
- lost money here: bb_squeeze_breakout v1.0 30m -0.90R over 38 trades; bb_squeeze_breakout v1.0 1h -0.14R over 68 trades
- no trade looks like: before the break: wait for a close outside the range; and here NO strategy has shown an edge - standing aside IS the playbook

## TRANSITION
- families (all their trades in this regime): smc -0.09R (766); liquidity_reversal -0.30R (419)
- made money here: S8-PDH-PDL-SWEEP v1.0 1h +0.07R over 146 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.69R over 48 trades; S8-PDH-PDL-SWEEP v1.0 30m -0.59R over 41 trades; liquidity_sweep_reversal v1.0 15m -0.32R over 108 trades; liquidity_sweep_reversal v1.0 30m -0.29R over 87 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.21R over 183 trades; liquidity_sweep_reversal v1.0 1h -0.19R over 176 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

## UNCLEAR
- no strategy has 30+ backtest trades in this regime yet - no evidence either way
- no trade looks like: the data does not show a regime - stand aside

