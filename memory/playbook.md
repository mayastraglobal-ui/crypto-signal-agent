# Regime playbook (generated - do not edit)

Written by the Sunday research run 2026-10-04 03:56 UTC (updated weekly) from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## Which families work where (family x timeframe x regime group)

| Family | TF | BULL | BEAR | RANGE | TRANSITION |
|---|---|---|---|---|---|
| breakout | 15m | -0.33R (137) ✗ | -0.44R (227) ✗ | -0.64R (15) | -0.38R (6) |
| breakout | 1h | -0.09R (4285) | -0.13R (3412) ✗ | +0.02R (112) ✓ | +0.06R (4693) ✓ |
| breakout | 30m | -0.05R (2235) | -0.07R (1810) | -0.44R (122) ✗ | -0.15R (1051) ✗ |
| breakout | 4h | +0.30R (1375) ✓ | +0.14R (1157) ✓ | -0.22R (42) ✗ | +0.20R (1958) ✓ |
| liquidity_reversal | 15m | -0.72R (97) ✗ | -0.52R (149) ✗ | -0.54R (73) ✗ | -0.29R (79) ✗ |
| liquidity_reversal | 1h | +0.12R (11) | +0.13R (10) | -0.33R (92) ✗ | -0.19R (129) ✗ |
| liquidity_reversal | 30m | -0.71R (59) ✗ | -0.69R (41) ✗ | -0.52R (69) ✗ | -0.43R (61) ✗ |
| liquidity_reversal | 5m | -1.25R (234) ✗ | -2.07R (29) | -1.63R (46) ✗ | -0.71R (36) ✗ |
| mean_reversion | 15m | - | - | -0.38R (1549) ✗ | - |
| mean_reversion | 1h | - | - | -0.17R (6231) ✗ | - |
| mean_reversion | 30m | - | - | -0.27R (3172) ✗ | - |
| mean_reversion | 4h | - | - | -0.11R (1418) ✗ | - |
| momentum | 1h | -0.06R (77) | -0.01R (62) | - | - |
| momentum | 30m | -0.40R (102) ✗ | -0.07R (99) | - | - |
| momentum | 4h | +0.28R (15) | -0.37R (14) | - | - |
| mtf_pullback | 15m | -0.33R (774) ✗ | -0.25R (1341) ✗ | - | - |
| mtf_pullback | 1h | -0.18R (2565) ✗ | -0.13R (2210) ✗ | - | - |
| mtf_pullback | 30m | -0.24R (1331) ✗ | -0.18R (1126) ✗ | - | - |
| mtf_pullback | 4h | -0.03R (519) | -0.15R (412) ✗ | - | - |
| smc | 15m | -0.48R (26) | -0.35R (28) | - | -0.54R (2) |
| smc | 1h | -0.42R (29) | -0.12R (54) ✗ | -0.35R (363) ✗ | +0.06R (388) ✓ |
| smc | 30m | -0.79R (64) ✗ | -0.24R (84) ✗ | -0.60R (189) ✗ | -0.33R (165) ✗ |
| trend_following | 15m | -0.26R (99) ✗ | -0.03R (200) | - | -0.89R (4) |
| trend_following | 1h | -0.24R (208) ✗ | -0.09R (195) | - | -0.28R (73) ✗ |
| trend_following | 30m | -0.23R (146) ✗ | -0.19R (168) ✗ | - | -0.71R (18) |
| trend_following | 4h | -0.11R (29) | -0.15R (26) | - | +0.19R (14) |
| trend_following | 5m | -0.73R (148) ✗ | -0.98R (27) | - | -0.83R (18) |

✓ = made money with 30+ trades · ✗ = lost -0.10R or worse · fewer than 30 trades = no mark (too few to say).

## Each regime

### STRONG_BULL
- families (all their trades in this regime): breakout -0.06R (2193); mtf_pullback -0.23R (1432); trend_following -0.44R (106); liquidity_reversal -1.03R (115)
- made money here: donchian_breakout-VEXIT v1.0 4h (lab) +0.23R over 54 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.23R over 54 trades [BACKTESTING]; donchian_breakout-VEXIT-VRVOL v1.0 4h (lab) +0.23R over 54 trades [BACKTESTING]; donchian_breakout-VEXIT-VRVOL-S4 v1.0 4h (lab) +0.23R over 54 trades [BACKTESTING]; donchian_breakout v1.0 4h +0.22R over 56 trades [BACKTESTING]; bb_squeeze_breakout v1.0 1h +0.07R over 33 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -1.21R over 83 trades; ema_9_21_cross v1.0 5m -0.66R over 59 trades; liquidity_sweep_reversal v1.0 15m -0.58R over 32 trades; bb_squeeze_breakout v1.0 15m -0.50R over 50 trades; trend_pullback v1.0 15m -0.34R over 318 trades; bb_squeeze_breakout v1.0 30m -0.28R over 56 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

### WEAK_BULL
- families (all their trades in this regime): breakout +0.00R (5833); mtf_pullback -0.19R (3757); momentum -0.25R (178); trend_following -0.34R (465); smc -0.70R (54); liquidity_reversal -1.07R (257)
- made money here: donchian_breakout-VEXIT v1.0 4h (lab) +0.40R over 177 trades [BACKTESTING]; donchian_breakout-VEXIT-VRVOL v1.0 4h (lab) +0.40R over 177 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.34R over 235 trades [BACKTESTING]; donchian_breakout-VEXIT-VRVOL-S4 v1.0 4h (lab) +0.34R over 235 trades [BACKTESTING]; donchian_breakout v1.0 4h +0.23R over 181 trades [BACKTESTING]; bb_squeeze_breakout v1.0 4h +0.13R over 92 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -1.27R over 151 trades; liquidity_sweep_reversal v1.0 30m -0.79R over 41 trades; liquidity_sweep_reversal v1.0 15m -0.79R over 65 trades; ema_9_21_cross v1.0 5m -0.77R over 89 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.70R over 54 trades; macd_trend_cross v1.0 30m -0.39R over 101 trades
- no trade looks like: no setup, or the higher timeframes disagree

### RANGE
- families (all their trades in this regime): mean_reversion -0.22R (11636); smc -0.45R (537); liquidity_reversal -0.65R (276)
- made money here: NOTHING - no tested strategy made money in this regime
- lost money here: liquidity_sweep_reversal v1.0 5m -1.63R over 46 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.72R over 145 trades; liquidity_sweep_reversal v1.0 30m -0.54R over 66 trades; liquidity_sweep_reversal v1.0 15m -0.54R over 73 trades; rsi2_dip_buy v1.0 15m -0.39R over 1395 trades; R4-CLUC v1.0 15m (lab) -0.39R over 54 trades
- no trade looks like: price in the middle of the range; breakouts without volume; and here NO strategy has shown an edge - standing aside IS the playbook

### HIGH_VOL_RANGE
- families (all their trades in this regime): mean_reversion -0.08R (698)
- made money here: R4-BBRSI v1.0 30m (lab) +0.13R over 71 trades [FAILED]; R4-BBRSI v1.0 1h (lab) +0.04R over 75 trades [FAILED]
- lost money here: rsi2_dip_buy v1.0 15m -0.32R over 90 trades; rsi2_dip_buy v1.0 4h -0.12R over 89 trades; rsi2_dip_buy v1.0 30m -0.12R over 116 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise

### WEAK_BEAR
- families (all their trades in this regime): momentum -0.03R (159); breakout -0.04R (5140); trend_following -0.12R (464); smc -0.17R (110); mtf_pullback -0.17R (3827); liquidity_reversal -0.57R (101)
- made money here: donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.23R over 199 trades [BACKTESTING]; donchian_breakout-VEXIT-VRVOL-S4 v1.0 4h (lab) +0.23R over 199 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.22R over 160 trades [BACKTESTING]; donchian_breakout-VEXIT-VRVOL v1.0 4h (lab) +0.22R over 160 trades [BACKTESTING]; donchian_breakout v1.0 4h +0.13R over 166 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 30m (lab) +0.01R over 217 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 15m -0.57R over 101 trades; bb_squeeze_breakout v1.0 15m -0.43R over 159 trades; supertrend_flip v1.0 30m -0.32R over 45 trades; trend_pullback v1.0 15m -0.28R over 909 trades; trend_pullback v1.0 30m -0.18R over 813 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 1h -0.18R over 48 trades
- no trade looks like: no setup, or the higher timeframes disagree

### STRONG_BEAR
- families (all their trades in this regime): trend_following +0.12R (65); mtf_pullback -0.17R (1262); breakout -0.23R (1419); liquidity_reversal -0.42R (48)
- made money here: ema_9_21_cross v1.0 15m +0.12R over 65 trades [FAILED]; donchian_breakout v1.0 4h +0.01R over 39 trades [BACKTESTING]
- lost money here: bb_squeeze_breakout v1.0 15m -0.46R over 68 trades; liquidity_sweep_reversal v1.0 15m -0.42R over 48 trades; donchian_breakout-VEXIT-S4 v1.0 1h (lab) -0.30R over 138 trades; donchian_breakout-VEXIT-VRVOL-S4 v1.0 1h (lab) -0.30R over 138 trades; donchian_breakout-VEXIT v1.0 1h (lab) -0.28R over 140 trades; donchian_breakout-VEXIT-VRVOL v1.0 1h (lab) -0.28R over 140 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend

### EXPANSION
- families (all their trades in this regime): breakout +0.07R (7682); trend_following -0.28R (73)
- made money here: donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.23R over 391 trades [BACKTESTING]; donchian_breakout-VEXIT-VRVOL-S4 v1.0 4h (lab) +0.23R over 391 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.22R over 389 trades [BACKTESTING]; donchian_breakout-VEXIT-VRVOL v1.0 4h (lab) +0.22R over 389 trades [BACKTESTING]; donchian_breakout v1.0 4h +0.13R over 395 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 1h (lab) +0.07R over 928 trades [FAILED]
- lost money here: supertrend_flip v1.0 1h -0.38R over 33 trades; ema_9_21_cross v1.0 1h -0.20R over 40 trades; donchian_breakout-VEXIT v1.0 30m (lab) -0.16R over 206 trades; donchian_breakout-VEXIT-VRVOL v1.0 30m (lab) -0.16R over 206 trades; donchian_breakout v1.0 30m -0.14R over 213 trades; donchian_breakout-VEXIT-S4 v1.0 30m (lab) -0.13R over 209 trades
- no trade looks like: the move is already several ATRs old (late entry)

### COMPRESSION
- families (all their trades in this regime): breakout -0.16R (128)
- made money here: bb_squeeze_breakout v1.0 1h +0.03R over 56 trades [FAILED]
- lost money here: donchian_breakout-VEXIT-S4 v1.0 30m (lab) -0.31R over 36 trades; donchian_breakout-VEXIT-VRVOL-S4 v1.0 30m (lab) -0.31R over 36 trades
- no trade looks like: before the break: wait for a close outside the range

### TRANSITION
- families (all their trades in this regime): smc -0.02R (522); liquidity_reversal -0.32R (305)
- made money here: S8-PDH-PDL-SWEEP v1.0 1h +0.11R over 101 trades [FAILED]; S8-PDH-PDL-SWEEP-noSMC v1.0 1h +0.04R over 287 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.71R over 36 trades; liquidity_sweep_reversal v1.0 30m -0.43R over 61 trades; liquidity_sweep_reversal v1.0 15m -0.29R over 79 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.26R over 134 trades; liquidity_sweep_reversal v1.0 1h -0.19R over 129 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

### UNCLEAR
- no strategy has 30+ backtest trades in this regime yet - no evidence either way
- no trade looks like: the data does not show a regime - stand aside

