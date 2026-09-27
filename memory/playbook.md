# Regime playbook (generated - do not edit)

Written by the Sunday research run 2026-09-27 00:50 UTC (updated weekly) from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## Which families work where (family x timeframe x regime group)

| Family | TF | BULL | BEAR | RANGE | TRANSITION |
|---|---|---|---|---|---|
| breakout | 15m | -0.26R (166) ✗ | -0.37R (299) ✗ | -0.31R (17) | -0.06R (6) |
| breakout | 1h | -0.09R (1663) | -0.07R (1632) | +0.02R (49) ✓ | +0.04R (1826) ✓ |
| breakout | 30m | -0.03R (997) | -0.05R (1033) | -0.75R (45) ✗ | -0.04R (480) |
| breakout | 4h | +0.25R (537) ✓ | +0.10R (545) ✓ | +0.03R (19) | +0.13R (750) ✓ |
| liquidity_reversal | 15m | -0.64R (107) ✗ | -0.42R (185) ✗ | -0.50R (89) ✗ | -0.19R (90) ✗ |
| liquidity_reversal | 1h | +0.26R (12) | -0.20R (17) | -0.26R (88) ✗ | -0.28R (124) ✗ |
| liquidity_reversal | 30m | -0.62R (63) ✗ | -0.64R (57) ✗ | -0.41R (81) ✗ | -0.41R (71) ✗ |
| liquidity_reversal | 5m | -1.14R (242) ✗ | -1.83R (36) ✗ | -1.04R (51) ✗ | -0.72R (45) ✗ |
| mean_reversion | 15m | - | - | -0.30R (1736) ✗ | - |
| mean_reversion | 1h | - | - | -0.16R (6182) ✗ | - |
| mean_reversion | 30m | - | - | -0.23R (3448) ✗ | - |
| mean_reversion | 4h | - | - | -0.10R (1348) ✗ | - |
| momentum | 1h | -0.00R (76) | -0.08R (66) | - | - |
| momentum | 30m | -0.30R (116) ✗ | -0.03R (129) | - | - |
| momentum | 4h | +0.20R (15) | -0.17R (11) | - | - |
| mtf_pullback | 15m | -0.26R (875) ✗ | -0.21R (1639) ✗ | - | - |
| mtf_pullback | 1h | -0.17R (2397) ✗ | -0.07R (2323) | - | - |
| mtf_pullback | 30m | -0.20R (1405) ✗ | -0.15R (1472) ✗ | - | - |
| mtf_pullback | 4h | -0.04R (467) | -0.14R (435) ✗ | - | - |
| smc | 15m | -0.18R (28) | +0.17R (46) ✓ | - | +0.06R (3) |
| smc | 1h | -0.33R (39) ✗ | -0.26R (54) ✗ | -0.39R (373) ✗ | +0.01R (394) ✓ |
| smc | 30m | -0.83R (88) ✗ | -0.39R (100) ✗ | -0.60R (238) ✗ | -0.19R (206) ✗ |
| trend_following | 15m | -0.16R (116) ✗ | -0.09R (242) | - | -0.69R (7) |
| trend_following | 1h | -0.24R (201) ✗ | -0.05R (211) | - | -0.37R (75) ✗ |
| trend_following | 30m | -0.22R (165) ✗ | -0.12R (223) ✗ | - | -0.74R (17) |
| trend_following | 4h | -0.23R (25) | -0.18R (27) | - | -0.17R (12) |
| trend_following | 5m | -0.65R (180) ✗ | -0.86R (36) ✗ | - | -0.67R (20) |

✓ = made money with 30+ trades · ✗ = lost -0.10R or worse · fewer than 30 trades = no mark (too few to say).

## Each regime

### STRONG_BULL
- families (all their trades in this regime): breakout -0.09R (967); mtf_pullback -0.21R (1468); trend_following -0.42R (125); liquidity_reversal -1.00R (124)
- made money here: donchian_breakout-VEXIT v1.0 4h (lab) +0.25R over 50 trades [BACKTESTING]; donchian_breakout v1.0 4h +0.22R over 51 trades [BACKTESTING]; bb_squeeze_breakout v1.0 1h +0.10R over 31 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -1.20R over 88 trades; ema_9_21_cross v1.0 5m -0.63R over 74 trades; liquidity_sweep_reversal v1.0 15m -0.50R over 36 trades; bb_squeeze_breakout v1.0 30m -0.34R over 57 trades; bb_squeeze_breakout v1.0 15m -0.31R over 67 trades; trend_pullback v1.0 15m -0.25R over 380 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

### WEAK_BULL
- families (all their trades in this regime): breakout +0.00R (2389); mtf_pullback -0.17R (3676); momentum -0.18R (191); trend_following -0.32R (503); smc -0.70R (103); liquidity_reversal -0.93R (270)
- made money here: donchian_breakout-VEXIT v1.0 4h (lab) +0.38R over 166 trades [BACKTESTING]; donchian_breakout v1.0 4h +0.23R over 172 trades [BACKTESTING]; bb_squeeze_breakout v1.0 4h +0.09R over 91 trades [FAILED]; donchian_breakout-VEXIT v1.0 30m (lab) +0.07R over 265 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -1.10R over 154 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.79R over 72 trades; liquidity_sweep_reversal v1.0 30m -0.72R over 45 trades; liquidity_sweep_reversal v1.0 15m -0.71R over 71 trades; ema_9_21_cross v1.0 5m -0.67R over 106 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 1h -0.50R over 31 trades
- no trade looks like: no setup, or the higher timeframes disagree

### RANGE
- families (all their trades in this regime): mean_reversion -0.20R (12020); smc -0.48R (593); liquidity_reversal -0.50R (305)
- made money here: NOTHING - no tested strategy made money in this regime
- lost money here: liquidity_sweep_reversal v1.0 5m -1.04R over 51 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.68R over 181 trades; liquidity_sweep_reversal v1.0 15m -0.50R over 89 trades; liquidity_sweep_reversal v1.0 30m -0.41R over 77 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 1h -0.41R over 255 trades; S8-PDH-PDL-SWEEP v1.0 1h -0.37R over 110 trades
- no trade looks like: price in the middle of the range; breakouts without volume; and here NO strategy has shown an edge - standing aside IS the playbook

### HIGH_VOL_RANGE
- families (all their trades in this regime): mean_reversion -0.08R (694)
- made money here: R4-BBRSI v1.0 1h (lab) +0.02R over 77 trades [FAILED]
- lost money here: rsi2_dip_buy v1.0 15m -0.23R over 97 trades; rsi2_dip_buy v1.0 4h -0.11R over 82 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise

### WEAK_BEAR
- families (all their trades in this regime): breakout -0.04R (2700); momentum -0.05R (190); trend_following -0.09R (554); mtf_pullback -0.13R (4423); smc -0.36R (115); liquidity_reversal -0.46R (164)
- made money here: donchian_breakout-VEXIT v1.0 4h (lab) +0.19R over 173 trades [BACKTESTING]; donchian_breakout v1.0 4h +0.13R over 179 trades [BACKTESTING]; bb_squeeze_breakout v1.0 1h +0.04R over 284 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 30m (lab) +0.03R over 291 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 30m -0.61R over 40 trades; liquidity_sweep_reversal v1.0 15m -0.42R over 124 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.40R over 69 trades; bb_squeeze_breakout v1.0 15m -0.33R over 214 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 1h -0.30R over 46 trades; trend_pullback v1.0 15m -0.21R over 1124 trades
- no trade looks like: no setup, or the higher timeframes disagree

### STRONG_BEAR
- families (all their trades in this regime): trend_following -0.06R (108); mtf_pullback -0.15R (1446); breakout -0.17R (773); liquidity_reversal -0.41R (61)
- made money here: donchian_breakout v1.0 4h +0.02R over 49 trades [BACKTESTING]
- lost money here: bb_squeeze_breakout v1.0 15m -0.47R over 85 trades; liquidity_sweep_reversal v1.0 15m -0.41R over 61 trades; donchian_breakout-VEXIT v1.0 1h (lab) -0.27R over 153 trades; trend_pullback v1.0 15m -0.21R over 515 trades; bb_squeeze_breakout v1.0 30m -0.21R over 37 trades; trend_pullback v1.0 30m -0.19R over 394 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend

### EXPANSION
- families (all their trades in this regime): breakout +0.05R (3036); trend_following -0.37R (75)
- made money here: donchian_breakout-VEXIT v1.0 4h (lab) +0.19R over 370 trades [BACKTESTING]; donchian_breakout v1.0 4h +0.07R over 377 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 1h (lab) +0.06R over 897 trades [FAILED]; donchian_breakout v1.0 1h +0.03R over 921 trades [FAILED]
- lost money here: supertrend_flip v1.0 1h -0.48R over 34 trades; ema_9_21_cross v1.0 1h -0.27R over 41 trades
- no trade looks like: the move is already several ATRs old (late entry)

### COMPRESSION
- families (all their trades in this regime): breakout +0.02R (49)
- made money here: bb_squeeze_breakout v1.0 1h +0.02R over 49 trades [BACKTESTING]
- lost money here: none below -0.10R
- no trade looks like: before the break: wait for a close outside the range

### TRANSITION
- families (all their trades in this regime): smc -0.06R (597); liquidity_reversal -0.34R (330)
- made money here: S8-PDH-PDL-SWEEP v1.0 1h +0.08R over 101 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.72R over 45 trades; S8-PDH-PDL-SWEEP v1.0 30m -0.58R over 36 trades; liquidity_sweep_reversal v1.0 30m -0.41R over 71 trades; liquidity_sweep_reversal v1.0 1h -0.28R over 124 trades; liquidity_sweep_reversal v1.0 15m -0.19R over 90 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.11R over 167 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

### UNCLEAR
- no strategy has 30+ backtest trades in this regime yet - no evidence either way
- no trade looks like: the data does not show a regime - stand aside

