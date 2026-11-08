# Regime playbook (generated - do not edit)

Written by the Sunday research run 2026-11-08 06:38 UTC (updated weekly) from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## Which families work where (family x timeframe x regime group)

| Family | TF | BULL | BEAR | RANGE | TRANSITION |
|---|---|---|---|---|---|
| breakout | 15m | -0.16R (14097) ✗ | -0.11R (13801) ✗ | -0.07R (1573) | -0.09R (4607) |
| breakout | 1h | -0.02R (12909) | -0.11R (10902) ✗ | +0.06R (834) ✓ | +0.10R (15222) ✓ |
| breakout | 30m | -0.06R (11238) | -0.04R (10445) | +0.02R (1068) ✓ | -0.04R (6229) |
| breakout | 4h | +0.26R (3769) ✓ | +0.10R (3208) ✓ | -0.23R (43) ✗ | +0.14R (5411) ✓ |
| breakout | 5m | -0.03R (5181) | -0.14R (5223) ✗ | -0.12R (1586) ✗ | -0.14R (2829) ✗ |
| liquidity_reversal | 15m | -0.41R (822) ✗ | -0.39R (766) ✗ | -0.33R (556) ✗ | -0.27R (746) ✗ |
| liquidity_reversal | 1h | +0.20R (28) | +0.18R (37) ✓ | -0.27R (92) ✗ | -0.20R (146) ✗ |
| liquidity_reversal | 30m | -0.31R (162) ✗ | -0.37R (147) ✗ | -0.41R (120) ✗ | -0.28R (115) ✗ |
| liquidity_reversal | 4h | +0.41R (6) | +0.02R (6) | - | +0.06R (4) |
| liquidity_reversal | 5m | -0.72R (1631) ✗ | -0.67R (1454) ✗ | -0.48R (1041) ✗ | -0.35R (1315) ✗ |
| mean_reversion | 15m | - | - | -0.32R (22162) ✗ | - |
| mean_reversion | 1h | - | - | -0.16R (7837) ✗ | - |
| mean_reversion | 30m | - | - | -0.24R (12842) ✗ | - |
| mean_reversion | 4h | - | - | -0.09R (2265) | - |
| momentum | 15m | -0.18R (3432) ✗ | -0.07R (3482) | - | +0.02R (407) ✓ |
| momentum | 1h | -0.10R (2676) | -0.05R (2354) | -0.03R (2006) | -0.17R (2198) ✗ |
| momentum | 30m | -0.18R (5593) ✗ | -0.12R (6278) ✗ | -0.22R (8486) ✗ | -0.22R (9663) ✗ |
| momentum | 4h | +0.09R (1150) ✓ | -0.07R (850) | +0.11R (949) ✓ | +0.06R (1881) ✓ |
| mtf_pullback | 15m | -0.24R (23637) ✗ | -0.20R (23227) ✗ | +0.01R (1415) ✓ | -0.06R (3539) |
| mtf_pullback | 1h | -0.11R (12603) ✗ | -0.08R (11738) | +0.04R (674) ✓ | +0.18R (1188) ✓ |
| mtf_pullback | 30m | -0.18R (13620) ✗ | -0.13R (13517) ✗ | +0.03R (815) ✓ | +0.01R (1633) ✓ |
| mtf_pullback | 4h | +0.05R (3435) ✓ | -0.01R (3179) | - | +0.41R (506) ✓ |
| mtf_pullback | 5m | -0.10R (3913) | -0.09R (3727) | -0.04R (1198) | -0.00R (2443) |
| smc | 15m | +0.06R (94) ✓ | -0.35R (70) ✗ | - | -1.36R (4) |
| smc | 1h | -0.30R (29) | -0.01R (57) | -0.30R (365) ✗ | +0.10R (393) ✓ |
| smc | 30m | -0.50R (142) ✗ | -0.40R (171) ✗ | -0.39R (423) ✗ | -0.19R (332) ✗ |
| trend_following | 15m | -0.24R (712) ✗ | -0.18R (779) ✗ | - | -0.31R (23) |
| trend_following | 1h | -0.12R (335) ✗ | +0.02R (333) ✓ | - | -0.29R (84) ✗ |
| trend_following | 30m | -0.26R (328) ✗ | -0.12R (428) ✗ | - | -0.20R (44) ✗ |
| trend_following | 4h | +0.28R (380) ✓ | -0.21R (43) ✗ | +1.17R (81) ✓ | +1.43R (488) ✓ |
| trend_following | 5m | -0.53R (768) ✗ | -0.45R (727) ✗ | - | -0.31R (121) ✗ |

✓ = made money with 30+ trades · ✗ = lost -0.10R or worse · fewer than 30 trades = no mark (too few to say).

## Each regime

### STRONG_BULL
- families (all their trades in this regime): breakout -0.02R (15468); momentum -0.12R (3414); mtf_pullback -0.16R (17193); trend_following -0.34R (653); liquidity_reversal -0.60R (814)
- made money here: TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.54R over 105 trades [BACKTESTING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.42R over 44 trades [PAPER_TRADING]; P01-BREAKOUT-V4-S1 v1.0 4h (lab) +0.36R over 69 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.35R over 66 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.31R over 81 trades [BACKTESTING]; TRD-H4-BREAKOUT v1.0 30m +0.30R over 83 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.77R over 477 trades; PB-B-SWEEP v1.0 5m -0.65R over 41 trades; ema_9_21_cross v1.0 30m -0.51R over 53 trades; ema_9_21_cross v1.0 5m -0.46R over 306 trades; P09-SWEEP-MSS-V5 v1.0 15m (lab) -0.43R over 35 trades; P07-SQUEEZE-RETEST-V3 v1.0 4h (lab) -0.41R over 32 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

### WEAK_BULL
- families (all their trades in this regime): breakout -0.06R (31522); momentum -0.15R (9342); mtf_pullback -0.18R (39787); trend_following -0.26R (1737); smc -0.37R (150); liquidity_reversal -0.63R (1651)
- made money here: P01-BREAKOUT-V3 v1.0 4h (lab) +0.54R over 86 trades [BACKTESTING]; P01-BREAKOUT-V4 v1.0 4h (lab) +0.47R over 222 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.44R over 128 trades [BACKTESTING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.41R over 132 trades [PAPER_TRADING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.40R over 178 trades [PAPER_TRADING]; donchian_breakout-VEXIT-S4-FDISP v1.0 4h (lab) +0.39R over 93 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.79R over 864 trades; PB-B-SWEEP v1.0 5m -0.69R over 90 trades; liquidity_sweep_reversal v1.0 30m -0.60R over 68 trades; ema_9_21_cross v1.0 5m -0.57R over 462 trades; liquidity_sweep_reversal v1.0 15m -0.52R over 343 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.45R over 102 trades
- no trade looks like: no setup, or the higher timeframes disagree

### RANGE
- families (all their trades in this regime): trend_following +0.35R (41); mtf_pullback -0.00R (3371); breakout -0.02R (3758); momentum -0.13R (8996); mean_reversion -0.25R (40107); smc -0.36R (761); liquidity_reversal -0.44R (1584)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.41R over 95 trades [VALIDATION]; P13-TURTLE-C v1.0 4h (lab) +0.35R over 41 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 30m (lab) +0.34R over 58 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.30R over 49 trades [BACKTESTING]; TRD-H4-PULLBACK v1.0 30m +0.27R over 92 trades [FAILED]; TRD-H4-PULLBACK-S2 v1.0 30m (lab) +0.26R over 127 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.76R over 394 trades; PB-B-SWEEP v1.0 5m -0.55R over 231 trades; liquidity_sweep_reversal v1.0 15m -0.49R over 256 trades; PB-B-SWEEP-15M v1.0 15m -0.49R over 64 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.47R over 305 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.42R over 86 trades
- no trade looks like: price in the middle of the range; breakouts without volume

### HIGH_VOL_RANGE
- families (all their trades in this regime): momentum -0.08R (345); mean_reversion -0.15R (2247)
- made money here: R4-CLUC v1.0 15m (lab) +0.17R over 40 trades [FAILED]; R4-CLUC v1.0 30m (lab) +0.02R over 40 trades [FAILED]; P11-MOMENTUM-C v1.0 30m (lab) +0.01R over 161 trades [FAILED]
- lost money here: P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.32R over 58 trades; P06-VWAP-REVERSION-V2 v1.0 15m (lab) -0.31R over 206 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.27R over 39 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.23R over 439 trades; rsi2_dip_buy v1.0 15m -0.19R over 368 trades; P05-RANGE-REVERSAL-V2 v1.0 30m (lab) -0.17R over 188 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise

### WEAK_BEAR
- families (all their trades in this regime): breakout -0.07R (30799); momentum -0.10R (10105); mtf_pullback -0.14R (39997); trend_following -0.20R (1651); smc -0.26R (176); liquidity_reversal -0.58R (1593)
- made money here: donchian_breakout-VEXIT-S4-FDISP v1.0 4h (lab) +0.45R over 108 trades [BACKTESTING]; P01-BREAKOUT-V2-FDISP-FNOTEXT v1.0 30m (lab) +0.45R over 40 trades [BACKTESTING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.36R over 113 trades [PAPER_TRADING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.31R over 151 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 15m (lab) +0.27R over 34 trades [FAILED]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 15m (lab) +0.27R over 137 trades [BACKTESTING]
- lost money here: PB-B-SWEEP v1.0 5m -0.88R over 126 trades; PB-B-SWEEP-15M v1.0 15m -0.76R over 38 trades; liquidity_sweep_reversal v1.0 5m -0.76R over 688 trades; liquidity_sweep_reversal v1.0 15m -0.56R over 268 trades; PB-B-SWEEP-LIMIT v1.0 5m -0.45R over 31 trades; ema_9_21_cross v1.0 5m -0.42R over 454 trades
- no trade looks like: no setup, or the higher timeframes disagree

### STRONG_BEAR
- families (all their trades in this regime): momentum -0.06R (2785); breakout -0.11R (12500); mtf_pullback -0.14R (15223); trend_following -0.34R (580); liquidity_reversal -0.58R (580)
- made money here: TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.33R over 40 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 30m (lab) +0.30R over 41 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.19R over 56 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 15m (lab) +0.15R over 138 trades [BACKTESTING]; donchian_breakout-VEXIT-S4-FDISP v1.0 30m (lab) +0.15R over 79 trades [BACKTESTING]; P07-SQUEEZE-RETEST-V4-S2 v1.0 4h (lab) +0.14R over 69 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.67R over 366 trades; PB-B-SWEEP v1.0 5m -0.54R over 38 trades; ema_9_21_cross v1.0 5m -0.51R over 273 trades; liquidity_sweep_reversal v1.0 15m -0.47R over 130 trades; P03-FIB-PULLBACK-V4 v1.0 4h (lab) -0.34R over 38 trades; P08-SESSION-BREAKOUT-V3 v1.0 1h (lab) -0.33R over 38 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend

### EXPANSION
- families (all their trades in this regime): trend_following +0.83R (515); breakout +0.05R (30147); mtf_pullback +0.00R (5157); momentum -0.08R (2115); liquidity_reversal -0.10R (84)
- made money here: P13-TURTLE-V2 v1.0 4h (lab) +2.65R over 57 trades [VALIDATION]; P13-TURTLE-V1 v1.0 4h (lab) +2.44R over 64 trades [VALIDATION]; P13-TURTLE-V3 v1.0 4h (lab) +2.36R over 59 trades [VALIDATION]; P02-EMA-PULLBACK-V4-S6-FHTF-S4-S6 v1.0 4h (lab) +0.91R over 30 trades [BACKTESTING]; TRD-H4-PULLBACK-S2 v1.0 1h (lab) +0.40R over 344 trades [BACKTESTING]; P13-TURTLE-C v1.0 4h (lab) +0.33R over 130 trades [PAPER_TRADING]
- lost money here: P11-MOMENTUM-V1 v1.0 30m (lab) -0.52R over 45 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.47R over 36 trades; supertrend_flip v1.0 1h -0.40R over 37 trades; P02-EMA-PULLBACK-V5 v1.0 30m (lab) -0.38R over 43 trades; P02-EMA-PULLBACK-V5 v1.0 1h (lab) -0.37R over 50 trades; P08-SESSION-BREAKOUT-V5 v1.0 30m (lab) -0.36R over 138 trades
- no trade looks like: the move is already several ATRs old (late entry)

### COMPRESSION
- families (all their trades in this regime): mtf_pullback -0.00R (704); breakout -0.16R (678); momentum -0.32R (1983); mean_reversion -0.47R (2673); liquidity_reversal -0.92R (33)
- made money here: TRD-H4-PULLBACK-noT4 v1.0 1h +0.20R over 82 trades [FAILED]; P12-LEADER-C v1.0 4h (lab) +0.15R over 113 trades [FAILED]; donchian_breakout-VEXIT-S4 v1.1 30m (lab) +0.11R over 44 trades [FAILED]; TRD-H4-BREAKOUT-S3 v1.0 15m (lab) +0.11R over 39 trades [FAILED]; bb_squeeze_breakout v1.0 1h +0.10R over 57 trades [BACKTESTING]; TRD-H4-PULLBACK-noT4 v1.0 30m +0.06R over 98 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.92R over 33 trades; bb_squeeze_breakout v1.0 15m -0.70R over 62 trades; P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.54R over 39 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.51R over 1725 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.44R over 112 trades; P06-VWAP-REVERSION-V2 v1.0 15m (lab) -0.44R over 428 trades
- no trade looks like: before the break: wait for a close outside the range

### TRANSITION
- families (all their trades in this regime): trend_following +0.20R (49); mtf_pullback +0.02R (3951); smc -0.03R (721); breakout -0.04R (3974); momentum -0.17R (6567); liquidity_reversal -0.32R (1627)
- made money here: TRD-H4-BREAKOUT-FDISP-S2 v1.0 1h (lab) +0.62R over 59 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 1h (lab) +0.54R over 69 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 30m (lab) +0.46R over 54 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.43R over 62 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.42R over 31 trades [BACKTESTING]; TRD-H4-BREAKOUT-S2 v1.0 1h (lab) +0.40R over 141 trades [BACKTESTING]
- lost money here: TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 5m (lab) -0.72R over 37 trades; TRD-H4-BREAKOUT-FDISP-FNOTEXT v1.0 5m (lab) -0.68R over 34 trades; PB-B-SWEEP v1.0 5m -0.60R over 179 trades; PB-B-SWEEP-15M v1.0 15m -0.55R over 38 trades; liquidity_sweep_reversal v1.0 5m -0.53R over 400 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.53R over 104 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

### UNCLEAR
- families (all their trades in this regime): trend_following -0.12R (49); momentum -0.21R (5390); liquidity_reversal -0.30R (480)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.18R over 81 trades [VALIDATION]; P12-LEADER-V3 v1.0 1h (lab) +0.07R over 106 trades [FAILED]; P12-LEADER-V1 v1.0 4h (lab) +0.05R over 99 trades [BACKTESTING]
- lost money here: PB-B-SWEEP v1.0 5m -0.55R over 133 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.40R over 429 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.31R over 204 trades; P11-MOMENTUM-V1 v1.0 30m (lab) -0.29R over 740 trades; P11-MOMENTUM-V4 v1.0 30m (lab) -0.27R over 629 trades; PB-B-GRADED v1.0 15m -0.24R over 144 trades
- no trade looks like: the data does not show a regime - stand aside

