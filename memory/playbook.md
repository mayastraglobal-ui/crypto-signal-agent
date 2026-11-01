# Regime playbook (generated - do not edit)

Written by the Sunday research run 2026-11-01 06:46 UTC (updated weekly) from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## Which families work where (family x timeframe x regime group)

| Family | TF | BULL | BEAR | RANGE | TRANSITION |
|---|---|---|---|---|---|
| breakout | 15m | -0.17R (12359) ✗ | -0.12R (11274) ✗ | -0.07R (1367) | -0.06R (3887) |
| breakout | 1h | -0.02R (12863) | -0.12R (10120) ✗ | +0.06R (766) ✓ | +0.10R (14709) ✓ |
| breakout | 30m | -0.07R (10952) | -0.03R (9332) | +0.02R (1001) ✓ | -0.05R (5813) |
| breakout | 4h | +0.26R (3925) ✓ | +0.06R (3041) ✓ | -0.29R (49) ✗ | +0.12R (5055) ✓ |
| breakout | 5m | -0.02R (4307) | -0.16R (4347) ✗ | -0.14R (1290) ✗ | -0.13R (2387) ✗ |
| liquidity_reversal | 15m | -0.48R (919) ✗ | -0.46R (807) ✗ | -0.39R (609) ✗ | -0.30R (807) ✗ |
| liquidity_reversal | 1h | +0.06R (29) | +0.04R (39) ✓ | -0.25R (100) ✗ | -0.21R (171) ✗ |
| liquidity_reversal | 30m | -0.34R (182) ✗ | -0.39R (157) ✗ | -0.41R (154) ✗ | -0.36R (132) ✗ |
| liquidity_reversal | 4h | +0.41R (6) | -0.41R (4) | -1.10R (4) | +0.06R (4) |
| liquidity_reversal | 5m | -0.85R (1882) ✗ | -0.73R (1565) ✗ | -0.57R (1110) ✗ | -0.38R (1406) ✗ |
| mean_reversion | 15m | - | - | -0.33R (23339) ✗ | - |
| mean_reversion | 1h | - | - | -0.17R (8796) ✗ | - |
| mean_reversion | 30m | - | - | -0.25R (14013) ✗ | - |
| mean_reversion | 4h | - | - | -0.09R (2476) | - |
| momentum | 15m | -0.18R (3441) ✗ | -0.07R (3473) | - | +0.02R (409) ✓ |
| momentum | 1h | -0.08R (2676) | -0.05R (2234) | -0.04R (1281) | -0.18R (1578) ✗ |
| momentum | 30m | -0.19R (5769) ✗ | -0.12R (6322) ✗ | -0.22R (8470) ✗ | -0.22R (9612) ✗ |
| momentum | 4h | +0.09R (1230) ✓ | -0.07R (896) | +0.10R (1069) ✓ | +0.06R (2070) ✓ |
| mtf_pullback | 15m | -0.26R (25377) ✗ | -0.21R (23732) ✗ | -0.02R (1491) | -0.07R (3802) |
| mtf_pullback | 1h | -0.10R (13504) ✗ | -0.08R (12164) | +0.02R (737) ✓ | +0.13R (1338) ✓ |
| mtf_pullback | 30m | -0.20R (14803) ✗ | -0.13R (13851) ✗ | +0.01R (879) ✓ | +0.00R (1808) |
| mtf_pullback | 4h | +0.06R (3258) ✓ | -0.02R (2805) | - | +0.31R (561) ✓ |
| mtf_pullback | 5m | -0.09R (4086) | -0.09R (3768) | -0.04R (1210) | +0.00R (2539) |
| smc | 15m | -0.09R (115) | -0.35R (72) ✗ | - | -1.80R (6) |
| smc | 1h | -0.48R (36) ✗ | -0.06R (65) | -0.28R (417) ✗ | +0.04R (456) ✓ |
| smc | 30m | -0.49R (176) ✗ | -0.42R (194) ✗ | -0.49R (522) ✗ | -0.31R (406) ✗ |
| trend_following | 15m | -0.28R (896) ✗ | -0.23R (860) ✗ | - | -0.34R (27) |
| trend_following | 1h | -0.09R (400) | +0.02R (373) ✓ | - | -0.25R (99) ✗ |
| trend_following | 30m | -0.27R (428) ✗ | -0.17R (471) ✗ | - | -0.15R (52) ✗ |
| trend_following | 4h | +0.41R (456) ✓ | -0.30R (48) ✗ | +1.08R (87) ✓ | +1.24R (580) ✓ |
| trend_following | 5m | -0.68R (965) ✗ | -0.54R (814) ✗ | - | -0.42R (148) ✗ |

✓ = made money with 30+ trades · ✗ = lost -0.10R or worse · fewer than 30 trades = no mark (too few to say).

## Each regime

### STRONG_BULL
- families (all their trades in this regime): breakout -0.03R (14630); momentum -0.12R (3467); mtf_pullback -0.17R (18474); trend_following -0.39R (863); liquidity_reversal -0.71R (954)
- made money here: donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.50R over 52 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.46R over 125 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.33R over 67 trades [PAPER_TRADING]; P13-TURTLE-C v1.0 4h (lab) +0.32R over 57 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.32R over 72 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.31R over 68 trades [PAPER_TRADING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.92R over 552 trades; P09-SWEEP-MSS-V5 v1.0 15m (lab) -0.65R over 33 trades; PB-B-SWEEP v1.0 5m -0.62R over 44 trades; ema_9_21_cross v1.0 5m -0.59R over 385 trades; ema_9_21_cross v1.0 30m -0.47R over 81 trades; liquidity_sweep_reversal v1.0 15m -0.47R over 218 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

### WEAK_BULL
- families (all their trades in this regime): breakout -0.06R (29641); momentum -0.15R (9551); mtf_pullback -0.18R (42311); trend_following -0.30R (2174); smc -0.42R (178); liquidity_reversal -0.74R (1904)
- made money here: P13-TURTLE-V3 v1.0 4h (lab) +0.83R over 32 trades [VALIDATION]; P01-BREAKOUT-V4 v1.0 4h (lab) +0.49R over 251 trades [BACKTESTING]; P01-BREAKOUT-V3 v1.0 4h (lab) +0.39R over 105 trades [BACKTESTING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.39R over 161 trades [PAPER_TRADING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.38R over 169 trades [PAPER_TRADING]; P04-MACD-SUPERTREND-V3 v1.0 4h (lab) +0.38R over 63 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.95R over 1028 trades; ema_9_21_cross v1.0 5m -0.74R over 580 trades; PB-B-SWEEP v1.0 5m -0.70R over 96 trades; liquidity_sweep_reversal v1.0 30m -0.62R over 85 trades; liquidity_sweep_reversal v1.0 15m -0.57R over 406 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.51R over 123 trades
- no trade looks like: no setup, or the higher timeframes disagree

### RANGE
- families (all their trades in this regime): trend_following +0.29R (47); mtf_pullback -0.02R (3546); breakout -0.03R (3150); momentum -0.14R (8436); mean_reversion -0.26R (43454); smc -0.40R (886); liquidity_reversal -0.50R (1723)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.42R over 94 trades [VALIDATION]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 30m (lab) +0.31R over 59 trades [BACKTESTING]; P13-TURTLE-C v1.0 4h (lab) +0.29R over 47 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.27R over 50 trades [BACKTESTING]; P12-LEADER-V1 v1.0 4h (lab) +0.26R over 101 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 30m (lab) +0.24R over 33 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.88R over 435 trades; PB-B-SWEEP v1.0 5m -0.59R over 245 trades; liquidity_sweep_reversal v1.0 15m -0.56R over 294 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.54R over 372 trades; PB-B-SWEEP-15M v1.0 15m -0.51R over 65 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.42R over 86 trades
- no trade looks like: price in the middle of the range; breakouts without volume

### HIGH_VOL_RANGE
- families (all their trades in this regime): momentum -0.09R (357); mean_reversion -0.16R (2425); liquidity_reversal -0.64R (31)
- made money here: R4-CLUC v1.0 15m (lab) +0.13R over 39 trades [FAILED]; P11-MOMENTUM-C v1.0 30m (lab) +0.01R over 161 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.64R over 31 trades; P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.32R over 58 trades; P06-VWAP-REVERSION-V2 v1.0 15m (lab) -0.31R over 206 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.29R over 40 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.23R over 436 trades; rsi2_dip_buy v1.0 15m -0.21R over 434 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise

### WEAK_BEAR
- families (all their trades in this regime): breakout -0.08R (26889); momentum -0.10R (10061); mtf_pullback -0.14R (40488); smc -0.24R (199); trend_following -0.25R (1811); liquidity_reversal -0.66R (1677)
- made money here: donchian_breakout-VEXIT-S4-FDISP v1.0 4h (lab) +0.37R over 119 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 15m (lab) +0.26R over 140 trades [BACKTESTING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.26R over 127 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-FDISP v1.0 15m (lab) +0.25R over 100 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.24R over 166 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 15m (lab) +0.23R over 35 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.90R over 130 trades; liquidity_sweep_reversal v1.0 5m -0.85R over 753 trades; PB-B-SWEEP-15M v1.0 15m -0.74R over 38 trades; liquidity_sweep_reversal v1.0 15m -0.65R over 298 trades; ema_9_21_cross v1.0 5m -0.51R over 497 trades; liquidity_sweep_reversal v1.0 30m -0.46R over 61 trades
- no trade looks like: no setup, or the higher timeframes disagree

### STRONG_BEAR
- families (all their trades in this regime): momentum -0.06R (2790); breakout -0.12R (11014); mtf_pullback -0.15R (15659); trend_following -0.39R (661); liquidity_reversal -0.62R (674)
- made money here: TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.26R over 42 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 30m (lab) +0.23R over 43 trades [BACKTESTING]; donchian_breakout-VEXIT-S4-FDISP v1.0 30m (lab) +0.18R over 94 trades [BACKTESTING]; P07-SQUEEZE-RETEST-V4-S2 v1.0 4h (lab) +0.14R over 76 trades [BACKTESTING]; P01-BREAKOUT-V2-FDISP v1.0 30m (lab) +0.11R over 119 trades [FAILED]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 15m (lab) +0.11R over 144 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.73R over 409 trades; ema_9_21_cross v1.0 5m -0.58R over 317 trades; PB-B-SWEEP v1.0 5m -0.54R over 38 trades; liquidity_sweep_reversal v1.0 15m -0.53R over 150 trades; donchian_breakout-VEXIT-S4 v1.1 4h (lab) -0.44R over 32 trades; P07-SQUEEZE-RETEST-V5 v1.0 30m (lab) -0.35R over 125 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend

### EXPANSION
- families (all their trades in this regime): trend_following +0.67R (626); breakout +0.06R (28377); mtf_pullback +0.00R (5582); momentum -0.07R (2121); liquidity_reversal -0.11R (92)
- made money here: P13-TURTLE-V2 v1.0 4h (lab) +2.32R over 69 trades [VALIDATION]; P13-TURTLE-V1 v1.0 4h (lab) +2.02R over 79 trades [VALIDATION]; P13-TURTLE-V3 v1.0 4h (lab) +1.93R over 75 trades [VALIDATION]; P02-EMA-PULLBACK-V4-S6-FHTF-S4-S6 v1.0 4h (lab) +0.56R over 38 trades [BACKTESTING]; TRD-H4-PULLBACK-S2 v1.0 1h (lab) +0.32R over 405 trades [BACKTESTING]; P13-TURTLE-C v1.0 4h (lab) +0.29R over 156 trades [PAPER_TRADING]
- lost money here: P11-MOMENTUM-V1 v1.0 30m (lab) -0.49R over 43 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.47R over 36 trades; ema_9_21_cross v1.0 5m -0.42R over 148 trades; P02-EMA-PULLBACK-V5 v1.0 30m (lab) -0.38R over 43 trades; P02-EMA-PULLBACK-V5 v1.0 1h (lab) -0.37R over 50 trades; P08-SESSION-BREAKOUT-V5 v1.0 30m (lab) -0.35R over 141 trades
- no trade looks like: the move is already several ATRs old (late entry)

### COMPRESSION
- families (all their trades in this regime): mtf_pullback -0.02R (744); breakout -0.12R (698); momentum -0.32R (1930); mean_reversion -0.47R (2666); liquidity_reversal -0.99R (36)
- made money here: P12-LEADER-C v1.0 4h (lab) +0.19R over 128 trades [FAILED]; TRD-H4-PULLBACK-noT4 v1.0 1h +0.18R over 88 trades [FAILED]; bb_squeeze_breakout v1.0 1h +0.14R over 67 trades [FAILED]; donchian_breakout-VEXIT-S4-FDISP v1.0 30m (lab) +0.11R over 30 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.1 30m (lab) +0.10R over 51 trades [FAILED]; TRD-H4-BREAKOUT-S3 v1.0 15m (lab) +0.09R over 44 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.99R over 36 trades; bb_squeeze_breakout v1.0 15m -0.61R over 68 trades; P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.54R over 39 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.51R over 1719 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.45R over 111 trades; P06-VWAP-REVERSION-V2 v1.0 15m (lab) -0.44R over 428 trades
- no trade looks like: before the break: wait for a close outside the range

### TRANSITION
- families (all their trades in this regime): trend_following +0.23R (53); mtf_pullback +0.01R (4238); breakout -0.09R (3301); smc -0.13R (855); momentum -0.16R (6356); liquidity_reversal -0.35R (1765)
- made money here: TRD-H4-BREAKOUT-FDISP-S2 v1.0 1h (lab) +0.59R over 64 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 1h (lab) +0.49R over 75 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.42R over 31 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 30m (lab) +0.42R over 56 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 1h (lab) +0.39R over 43 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 1h (lab) +0.39R over 44 trades [BACKTESTING]
- lost money here: TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 5m (lab) -0.73R over 38 trades; TRD-H4-BREAKOUT-FDISP-FNOTEXT v1.0 5m (lab) -0.68R over 34 trades; liquidity_sweep_reversal v1.0 5m -0.59R over 436 trades; PB-B-SWEEP v1.0 5m -0.58R over 186 trades; PB-B-SWEEP-15M v1.0 15m -0.55R over 40 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.50R over 106 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

### UNCLEAR
- families (all their trades in this regime): trend_following -0.16R (56); momentum -0.22R (5128); liquidity_reversal -0.34R (538)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.18R over 81 trades [VALIDATION]; P12-LEADER-V3 v1.0 1h (lab) +0.07R over 106 trades [FAILED]; P12-LEADER-V1 v1.0 4h (lab) +0.05R over 99 trades [BACKTESTING]; P12-LEADER-C v1.0 4h (lab) +0.03R over 494 trades [FAILED]
- lost money here: PB-B-SWEEP-15M v1.0 15m -0.68R over 33 trades; PB-B-SWEEP v1.0 5m -0.62R over 147 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.39R over 435 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.32R over 203 trades; P11-MOMENTUM-V1 v1.0 30m (lab) -0.31R over 733 trades; P11-MOMENTUM-V4 v1.0 30m (lab) -0.27R over 629 trades
- no trade looks like: the data does not show a regime - stand aside

