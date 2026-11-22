# Regime playbook (generated - do not edit)

Written by the Sunday research run 2026-11-22 07:23 UTC (updated weekly) from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## Which families work where (family x timeframe x regime group)

| Family | TF | BULL | BEAR | RANGE | TRANSITION |
|---|---|---|---|---|---|
| breakout | 15m | -0.14R (16481) ✗ | -0.06R (16878) | -0.05R (2259) | -0.04R (6150) |
| breakout | 1h | -0.01R (15954) | -0.09R (13625) | +0.08R (1001) ✓ | +0.13R (20041) ✓ |
| breakout | 30m | -0.04R (13918) | +0.02R (13232) ✓ | +0.03R (1419) ✓ | -0.01R (8562) |
| breakout | 4h | +0.28R (4111) ✓ | +0.13R (3556) ✓ | -0.25R (45) ✗ | +0.17R (6019) ✓ |
| breakout | 5m | -0.03R (5660) | -0.10R (7318) ✗ | -0.09R (2112) | -0.16R (3724) ✗ |
| liquidity_reversal | 15m | -0.42R (797) ✗ | -0.42R (755) ✗ | -0.35R (562) ✗ | -0.28R (749) ✗ |
| liquidity_reversal | 1h | -0.01R (24) | +0.12R (33) ✓ | -0.23R (94) ✗ | -0.20R (146) ✗ |
| liquidity_reversal | 30m | -0.30R (155) ✗ | -0.41R (132) ✗ | -0.38R (125) ✗ | -0.29R (113) ✗ |
| liquidity_reversal | 4h | +0.41R (6) | +0.02R (6) | - | -0.31R (6) |
| liquidity_reversal | 5m | -0.74R (1535) ✗ | -0.65R (1528) ✗ | -0.49R (992) ✗ | -0.35R (1268) ✗ |
| mean_reversion | 15m | - | - | -0.32R (22187) ✗ | - |
| mean_reversion | 1h | - | - | -0.16R (7876) ✗ | - |
| mean_reversion | 30m | - | - | -0.23R (12853) ✗ | - |
| mean_reversion | 4h | - | - | -0.05R (2701) | - |
| momentum | 15m | -0.19R (3402) ✗ | -0.05R (3597) | - | +0.04R (407) ✓ |
| momentum | 1h | -0.10R (2676) | -0.04R (2394) | -0.04R (2015) | -0.17R (2205) ✗ |
| momentum | 30m | -0.19R (6113) ✗ | -0.10R (7114) ✗ | -0.20R (10633) ✗ | -0.20R (11848) ✗ |
| momentum | 4h | +0.09R (1150) ✓ | -0.06R (861) | +0.11R (949) ✓ | +0.06R (1881) ✓ |
| mtf_pullback | 15m | -0.24R (23428) ✗ | -0.19R (24007) ✗ | +0.03R (1501) ✓ | -0.06R (3616) |
| mtf_pullback | 1h | -0.11R (12605) ✗ | -0.07R (11960) | +0.06R (699) ✓ | +0.17R (1213) ✓ |
| mtf_pullback | 30m | -0.18R (13531) ✗ | -0.12R (13907) ✗ | +0.06R (865) ✓ | +0.02R (1666) ✓ |
| mtf_pullback | 4h | +0.05R (3704) ✓ | +0.02R (3538) ✓ | - | +0.47R (523) ✓ |
| mtf_pullback | 5m | -0.12R (3511) ✗ | -0.07R (4124) | -0.04R (1257) | -0.03R (2510) |
| smc | 15m | +0.06R (94) ✓ | -0.35R (70) ✗ | - | -1.36R (4) |
| smc | 1h | -0.30R (29) | -0.01R (57) | -0.28R (371) ✗ | +0.10R (395) ✓ |
| smc | 30m | -0.50R (142) ✗ | -0.41R (170) ✗ | -0.36R (428) ✗ | -0.19R (331) ✗ |
| trend_following | 15m | -0.24R (706) ✗ | -0.18R (798) ✗ | - | -0.34R (22) |
| trend_following | 1h | -0.12R (335) ✗ | +0.01R (335) ✓ | - | -0.29R (84) ✗ |
| trend_following | 30m | -0.26R (326) ✗ | -0.11R (436) ✗ | - | -0.20R (44) ✗ |
| trend_following | 4h | +0.33R (419) ✓ | -0.15R (44) ✗ | +1.14R (90) ✓ | +1.60R (569) ✓ |
| trend_following | 5m | -0.54R (725) ✗ | -0.45R (779) ✗ | - | -0.35R (121) ✗ |

✓ = made money with 30+ trades · ✗ = lost -0.10R or worse · fewer than 30 trades = no mark (too few to say).

## Each regime

### STRONG_BULL
- families (all their trades in this regime): breakout -0.01R (18799); momentum -0.12R (3520); mtf_pullback -0.16R (16972); trend_following -0.34R (634); liquidity_reversal -0.62R (748)
- made money here: TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.54R over 105 trades [PAPER_TRADING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.42R over 44 trades [PAPER_TRADING]; P01-BREAKOUT-V4-S1 v1.0 4h (lab) +0.36R over 69 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.35R over 66 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.31R over 81 trades [BACKTESTING]; P01-BREAKOUT-V2-FDISP-FRETEST v1.0 30m (lab) +0.31R over 123 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.81R over 447 trades; PB-B-SWEEP v1.0 5m -0.61R over 40 trades; ema_9_21_cross v1.0 30m -0.50R over 52 trades; ema_9_21_cross v1.0 5m -0.47R over 291 trades; liquidity_sweep_reversal v1.0 15m -0.39R over 189 trades; P07-SQUEEZE-RETEST-V3 v1.0 4h (lab) -0.39R over 31 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

### WEAK_BULL
- families (all their trades in this regime): breakout -0.05R (37071); momentum -0.15R (9726); mtf_pullback -0.18R (39579); trend_following -0.26R (1705); smc -0.37R (150); liquidity_reversal -0.64R (1544)
- made money here: P01-BREAKOUT-V3 v1.0 4h (lab) +0.51R over 85 trades [BACKTESTING]; P01-BREAKOUT-V4 v1.0 4h (lab) +0.50R over 204 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.44R over 128 trades [PAPER_TRADING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.41R over 132 trades [PAPER_TRADING]; donchian_breakout-VEXIT-FDISP-S2 v1.0 4h (lab) +0.40R over 168 trades [PAPER_TRADING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.40R over 178 trades [PAPER_TRADING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.81R over 810 trades; PB-B-SWEEP v1.0 5m -0.65R over 85 trades; liquidity_sweep_reversal v1.0 30m -0.60R over 68 trades; ema_9_21_cross v1.0 5m -0.59R over 434 trades; liquidity_sweep_reversal v1.0 15m -0.52R over 343 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.45R over 102 trades
- no trade looks like: no setup, or the higher timeframes disagree

### RANGE
- families (all their trades in this regime): trend_following +0.35R (41); mtf_pullback +0.03R (3594); breakout +0.00R (5210); momentum -0.13R (10640); mean_reversion -0.25R (40584); smc -0.34R (773); liquidity_reversal -0.44R (1556)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.41R over 95 trades [VALIDATION]; P13-TURTLE-C v1.0 4h (lab) +0.35R over 41 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3-S2 v1.0 1h (lab) +0.32R over 111 trades [BACKTESTING]; TRD-H4-PULLBACK v1.0 30m +0.31R over 107 trades [FAILED]; TRD-H4-PULLBACK-S2 v1.0 30m (lab) +0.30R over 143 trades [BACKTESTING]; P12-LEADER-V1 v1.0 4h (lab) +0.25R over 102 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.73R over 379 trades; PB-B-SWEEP v1.0 5m -0.59R over 232 trades; PB-B-SWEEP-15M v1.0 15m -0.52R over 64 trades; liquidity_sweep_reversal v1.0 15m -0.51R over 264 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.45R over 311 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.41R over 98 trades
- no trade looks like: price in the middle of the range; breakouts without volume

### HIGH_VOL_RANGE
- families (all their trades in this regime): momentum -0.10R (422); mean_reversion -0.15R (2247)
- made money here: R4-CLUC v1.0 15m (lab) +0.17R over 40 trades [FAILED]; R4-CLUC v1.0 30m (lab) +0.02R over 40 trades [FAILED]; P11-MOMENTUM-C v1.0 30m (lab) +0.01R over 161 trades [FAILED]
- lost money here: P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.32R over 58 trades; P06-VWAP-REVERSION-V2 v1.0 15m (lab) -0.30R over 209 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.27R over 39 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.23R over 439 trades; P11-MOMENTUM-V1-FRETEST-FDISP v1.0 30m (lab) -0.21R over 33 trades; rsi2_dip_buy v1.0 15m -0.19R over 367 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise

### WEAK_BEAR
- families (all their trades in this regime): breakout -0.04R (37920); momentum -0.09R (10872); mtf_pullback -0.13R (41475); trend_following -0.20R (1705); smc -0.26R (175); liquidity_reversal -0.59R (1590)
- made money here: P01-BREAKOUT-V2-FDISP-FNOTEXT v1.0 30m (lab) +0.59R over 43 trades [BACKTESTING]; donchian_breakout-VEXIT-S4-FDISP-FNOTEXT v1.0 30m (lab) +0.52R over 62 trades [BACKTESTING]; donchian_breakout-VEXIT-S4-FDISP v1.0 4h (lab) +0.47R over 109 trades [BACKTESTING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.42R over 116 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 15m (lab) +0.38R over 43 trades [FAILED]; TRD-H4-BREAKOUT-FDISP-FNOTEXT v1.0 15m (lab) +0.37R over 41 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.88R over 125 trades; PB-B-SWEEP-15M v1.0 15m -0.76R over 38 trades; liquidity_sweep_reversal v1.0 5m -0.73R over 740 trades; liquidity_sweep_reversal v1.0 15m -0.59R over 275 trades; P09-SWEEP-MSS-V5 v1.0 30m (lab) -0.48R over 37 trades; ema_9_21_cross v1.0 5m -0.41R over 488 trades
- no trade looks like: no setup, or the higher timeframes disagree

### STRONG_BEAR
- families (all their trades in this regime): momentum -0.04R (3017); breakout -0.04R (16470); mtf_pullback -0.12R (15891); trend_following -0.34R (606); liquidity_reversal -0.57R (610)
- made money here: TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.53R over 44 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 30m (lab) +0.49R over 45 trades [BACKTESTING]; donchian_breakout-VEXIT-FRETEST v1.0 4h (lab) +0.41R over 36 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-FDISP-FNOTEXT v1.0 15m (lab) +0.40R over 34 trades [FAILED]; TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 15m (lab) +0.40R over 34 trades [FAILED]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.34R over 60 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.64R over 390 trades; PB-B-SWEEP v1.0 5m -0.56R over 39 trades; ema_9_21_cross v1.0 5m -0.51R over 291 trades; liquidity_sweep_reversal v1.0 15m -0.48R over 135 trades; P07-SQUEEZE-RETEST-V5 v1.0 30m (lab) -0.28R over 128 trades; donchian_breakout-VEXIT-S4 v1.0 1h (lab) -0.27R over 148 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend

### EXPANSION
- families (all their trades in this regime): trend_following +0.98R (576); breakout +0.07R (39076); mtf_pullback +0.01R (5309); momentum -0.08R (2195); liquidity_reversal -0.10R (84)
- made money here: P13-TURTLE-V2 v1.0 4h (lab) +2.65R over 57 trades [VALIDATION]; P13-TURTLE-V1 v1.0 4h (lab) +2.44R over 64 trades [VALIDATION]; P13-TURTLE-V3 v1.0 4h (lab) +2.36R over 59 trades [VALIDATION]; P13-TURTLE-V3-S2 v1.0 4h (lab) +2.35R over 61 trades [VALIDATION]; P02-EMA-PULLBACK-V4-S6-FHTF-S4-S6 v1.0 4h (lab) +1.00R over 31 trades [BACKTESTING]; TRD-H4-PULLBACK-S2 v1.0 1h (lab) +0.39R over 357 trades [BACKTESTING]
- lost money here: P11-MOMENTUM-V1 v1.0 30m (lab) -0.52R over 45 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.47R over 36 trades; supertrend_flip v1.0 1h -0.40R over 37 trades; P02-EMA-PULLBACK-V5 v1.0 30m (lab) -0.38R over 43 trades; P02-EMA-PULLBACK-V5 v1.0 1h (lab) -0.37R over 50 trades; P08-SESSION-BREAKOUT-V5 v1.0 30m (lab) -0.36R over 127 trades
- no trade looks like: the move is already several ATRs old (late entry)

### COMPRESSION
- families (all their trades in this regime): mtf_pullback -0.03R (671); breakout -0.16R (837); momentum -0.29R (2418); mean_reversion -0.47R (2667); liquidity_reversal -0.91R (32)
- made money here: TRD-H4-PULLBACK-noT4 v1.0 1h +0.17R over 84 trades [FAILED]; P12-LEADER-C v1.0 4h (lab) +0.15R over 113 trades [FAILED]; donchian_breakout-VEXIT-S4 v1.1 30m (lab) +0.10R over 46 trades [FAILED]; bb_squeeze_breakout v1.0 1h +0.10R over 57 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-S2 v1.0 30m (lab) +0.06R over 32 trades [BACKTESTING]; TRD-H4-PULLBACK-noT4 v1.0 30m +0.05R over 99 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.91R over 32 trades; bb_squeeze_breakout v1.0 15m -0.73R over 65 trades; P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.59R over 38 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.52R over 1721 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.45R over 175 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.44R over 112 trades
- no trade looks like: before the break: wait for a close outside the range

### TRANSITION
- families (all their trades in this regime): trend_following +0.20R (49); mtf_pullback +0.01R (4007); breakout -0.01R (5231); smc -0.03R (722); momentum -0.14R (7682); liquidity_reversal -0.32R (1589)
- made money here: TRD-H4-BREAKOUT-FDISP-S2 v1.0 1h (lab) +0.59R over 60 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 1h (lab) +0.52R over 70 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.47R over 30 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.47R over 63 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 30m (lab) +0.45R over 54 trades [BACKTESTING]; TRD-H4-BREAKOUT-S2 v1.0 1h (lab) +0.41R over 143 trades [BACKTESTING]
- lost money here: TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 5m (lab) -0.73R over 35 trades; TRD-H4-BREAKOUT-FDISP-FNOTEXT v1.0 5m (lab) -0.69R over 32 trades; PB-B-SWEEP v1.0 5m -0.60R over 171 trades; PB-B-SWEEP-15M v1.0 15m -0.55R over 38 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.53R over 101 trades; TRD-H4-BREAKOUT-FDISP v1.0 5m (lab) -0.52R over 100 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

### UNCLEAR
- families (all their trades in this regime): trend_following -0.12R (49); momentum -0.21R (6387); liquidity_reversal -0.33R (445)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.18R over 81 trades [VALIDATION]; P12-LEADER-V3 v1.0 1h (lab) +0.07R over 106 trades [FAILED]; P12-LEADER-V1 v1.0 4h (lab) +0.05R over 99 trades [BACKTESTING]
- lost money here: PB-B-SWEEP v1.0 5m -0.56R over 135 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.40R over 429 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.31R over 204 trades; P11-MOMENTUM-V1 v1.0 30m (lab) -0.30R over 742 trades; P11-MOMENTUM-V4 v1.0 30m (lab) -0.27R over 637 trades; PB-B-GRADED v1.0 5m -0.26R over 132 trades
- no trade looks like: the data does not show a regime - stand aside

