# Regime playbook (generated - do not edit)

Written by the daily research run 2026-09-25 00:49 UTC from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## Which families work where (family x timeframe x regime group)

| Family | TF | BULL | BEAR | RANGE | TRANSITION |
|---|---|---|---|---|---|
| breakout | 15m | -0.30R (173) ✗ | -0.39R (337) ✗ | -0.29R (23) | -0.28R (7) |
| breakout | 1h | -0.13R (1336) ✗ | -0.07R (1301) | -0.14R (68) ✗ | +0.03R (1283) ✓ |
| breakout | 30m | -0.11R (689) ✗ | -0.10R (703) ✗ | -0.72R (53) ✗ | -0.12R (308) ✗ |
| breakout | 4h | +0.12R (446) ✓ | +0.05R (446) ✓ | -0.07R (24) | +0.08R (540) ✓ |
| liquidity_reversal | 15m | -0.78R (130) ✗ | -0.49R (217) ✗ | -0.40R (112) ✗ | -0.32R (108) ✗ |
| liquidity_reversal | 1h | +0.27R (14) | -0.15R (13) | -0.32R (126) ✗ | -0.19R (176) ✗ |
| liquidity_reversal | 30m | -0.58R (70) ✗ | -0.60R (67) ✗ | -0.38R (105) ✗ | -0.29R (87) ✗ |
| liquidity_reversal | 5m | -1.18R (265) ✗ | -1.68R (53) ✗ | -1.07R (53) ✗ | -0.69R (48) ✗ |
| mean_reversion | 15m | - | - | -0.36R (2143) ✗ | - |
| mean_reversion | 1h | - | - | -0.12R (7315) ✗ | - |
| mean_reversion | 30m | - | - | -0.21R (2795) ✗ | - |
| mean_reversion | 4h | - | - | -0.10R (1975) ✗ | - |
| momentum | 1h | -0.00R (113) | -0.01R (96) | - | - |
| momentum | 30m | -0.32R (138) ✗ | -0.07R (166) | - | - |
| momentum | 4h | +0.27R (21) | -0.28R (18) | - | - |
| mtf_pullback | 15m | -0.30R (1008) ✗ | -0.23R (1975) ✗ | - | - |
| mtf_pullback | 1h | -0.19R (3366) ✗ | -0.10R (3214) ✗ | - | - |
| mtf_pullback | 30m | -0.23R (1694) ✗ | -0.17R (1741) ✗ | - | - |
| mtf_pullback | 4h | +0.01R (671) ✓ | -0.17R (618) ✗ | - | - |
| smc | 15m | -0.26R (29) | -0.24R (38) ✗ | - | +0.06R (3) |
| smc | 1h | -0.36R (41) ✗ | -0.05R (82) | -0.32R (528) ✗ | -0.01R (542) |
| smc | 30m | -0.82R (91) ✗ | -0.40R (139) ✗ | -0.53R (296) ✗ | -0.27R (227) ✗ |
| trend_following | 15m | -0.25R (148) ✗ | -0.16R (294) ✗ | - | -0.59R (7) |
| trend_following | 1h | -0.16R (276) ✗ | -0.06R (276) | - | -0.24R (98) ✗ |
| trend_following | 30m | -0.30R (208) ✗ | -0.12R (275) ✗ | - | -0.72R (23) |
| trend_following | 4h | +0.00R (45) | -0.21R (35) ✗ | - | +0.30R (16) |
| trend_following | 5m | -0.67R (185) ✗ | -1.06R (43) ✗ | - | -0.79R (28) |

✓ = made money with 30+ trades · ✗ = lost -0.10R or worse · fewer than 30 trades = no mark (too few to say).

## Each regime

### STRONG_BULL
- families (all their trades in this regime): breakout -0.11R (689); mtf_pullback -0.23R (1837); trend_following -0.45R (189); liquidity_reversal -1.01R (142)
- made money here: donchian_breakout v1.0 4h +0.12R over 68 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -1.18R over 96 trades; liquidity_sweep_reversal v1.0 15m -0.67R over 46 trades; ema_9_21_cross v1.0 5m -0.58R over 85 trades; ema_9_21_cross v1.0 30m -0.56R over 35 trades; bb_squeeze_breakout v1.0 15m -0.35R over 65 trades; trend_pullback v1.0 15m -0.28R over 431 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

### WEAK_BULL
- families (all their trades in this regime): breakout -0.09R (1947); momentum -0.17R (250); mtf_pullback -0.18R (4902); trend_following -0.28R (657); smc -0.71R (104); liquidity_reversal -1.00R (303)
- made money here: donchian_breakout v1.0 4h +0.13R over 247 trades [BACKTESTING]; bb_squeeze_breakout v1.0 4h +0.12R over 123 trades [FAILED]; trend_pullback v1.0 4h +0.03R over 540 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -1.19R over 169 trades; liquidity_sweep_reversal v1.0 15m -0.84R over 84 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.80R over 72 trades; ema_9_21_cross v1.0 5m -0.73R over 100 trades; liquidity_sweep_reversal v1.0 30m -0.65R over 50 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 1h -0.51R over 32 trades
- no trade looks like: no setup, or the higher timeframes disagree

### RANGE
- families (all their trades in this regime): mean_reversion -0.18R (13487); smc -0.41R (794); liquidity_reversal -0.46R (388)
- made money here: NOTHING - no tested strategy made money in this regime
- lost money here: liquidity_sweep_reversal v1.0 5m -1.07R over 53 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.59R over 231 trades; liquidity_sweep_reversal v1.0 15m -0.40R over 112 trades; liquidity_sweep_reversal v1.0 30m -0.39R over 101 trades; rsi2_dip_buy v1.0 15m -0.36R over 2018 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 1h -0.35R over 354 trades
- no trade looks like: price in the middle of the range; breakouts without volume; and here NO strategy has shown an edge - standing aside IS the playbook

### HIGH_VOL_RANGE
- families (all their trades in this regime): mean_reversion -0.11R (741)
- made money here: NOTHING - no tested strategy made money in this regime
- lost money here: rsi2_dip_buy v1.0 15m -0.26R over 125 trades; rsi2_dip_buy v1.0 30m -0.12R over 146 trades; rsi2_dip_buy v1.0 4h -0.12R over 131 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise; and here NO strategy has shown an edge - standing aside IS the playbook

### WEAK_BEAR
- families (all their trades in this regime): momentum -0.05R (258); breakout -0.08R (2189); mtf_pullback -0.16R (5674); trend_following -0.17R (767); smc -0.25R (170); liquidity_reversal -0.76R (241)
- made money here: donchian_breakout v1.0 4h +0.11R over 249 trades [BACKTESTING]; bb_squeeze_breakout v1.0 4h +0.04R over 124 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -1.83R over 43 trades; ema_9_21_cross v1.0 5m -1.00R over 35 trades; liquidity_sweep_reversal v1.0 30m -0.54R over 48 trades; liquidity_sweep_reversal v1.0 15m -0.53R over 150 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.40R over 100 trades; bb_squeeze_breakout v1.0 15m -0.39R over 240 trades
- no trade looks like: no setup, or the higher timeframes disagree

### STRONG_BEAR
- families (all their trades in this regime): trend_following -0.07R (135); mtf_pullback -0.17R (1874); breakout -0.19R (558); liquidity_reversal -0.42R (67)
- made money here: NOTHING - no tested strategy made money in this regime
- lost money here: liquidity_sweep_reversal v1.0 15m -0.42R over 67 trades; bb_squeeze_breakout v1.0 15m -0.41R over 97 trades; bb_squeeze_breakout v1.0 30m -0.35R over 47 trades; trend_pullback v1.0 15m -0.23R over 654 trades; ema_9_21_cross v1.0 30m -0.22R over 39 trades; trend_pullback v1.0 4h -0.20R over 110 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend; and here NO strategy has shown an edge - standing aside IS the playbook

### EXPANSION
- families (all their trades in this regime): breakout +0.02R (2105); trend_following -0.24R (98)
- made money here: donchian_breakout v1.0 4h +0.08R over 537 trades [BACKTESTING]; donchian_breakout v1.0 1h +0.03R over 1271 trades [FAILED]
- lost money here: supertrend_flip v1.0 1h -0.30R over 41 trades; ema_9_21_cross v1.0 1h -0.20R over 57 trades
- no trade looks like: the move is already several ATRs old (late entry)

### COMPRESSION
- families (all their trades in this regime): breakout -0.42R (106)
- made money here: NOTHING - no tested strategy made money in this regime
- lost money here: bb_squeeze_breakout v1.0 30m -0.90R over 38 trades; bb_squeeze_breakout v1.0 1h -0.14R over 68 trades
- no trade looks like: before the break: wait for a close outside the range; and here NO strategy has shown an edge - standing aside IS the playbook

### TRANSITION
- families (all their trades in this regime): smc -0.09R (766); liquidity_reversal -0.30R (419)
- made money here: S8-PDH-PDL-SWEEP v1.0 1h +0.07R over 146 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.69R over 48 trades; S8-PDH-PDL-SWEEP v1.0 30m -0.59R over 41 trades; liquidity_sweep_reversal v1.0 15m -0.32R over 108 trades; liquidity_sweep_reversal v1.0 30m -0.29R over 87 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.21R over 183 trades; liquidity_sweep_reversal v1.0 1h -0.19R over 176 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

### UNCLEAR
- no strategy has 30+ backtest trades in this regime yet - no evidence either way
- no trade looks like: the data does not show a regime - stand aside

