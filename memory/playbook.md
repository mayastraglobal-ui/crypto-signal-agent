# Regime playbook (generated - do not edit)

Written by the Sunday research run 2026-11-15 07:06 UTC (updated weekly) from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## Which families work where (family x timeframe x regime group)

| Family | TF | BULL | BEAR | RANGE | TRANSITION |
|---|---|---|---|---|---|
| breakout | 15m | -0.15R (15238) ✗ | -0.09R (15066) | -0.03R (2015) | -0.05R (5603) |
| breakout | 1h | -0.02R (13732) | -0.10R (11638) ✗ | +0.08R (969) ✓ | +0.12R (16450) ✓ |
| breakout | 30m | -0.05R (12006) | -0.00R (11196) | +0.05R (1276) ✓ | -0.02R (7091) |
| breakout | 4h | +0.27R (3693) ✓ | +0.10R (3141) ✓ | -0.25R (45) ✗ | +0.15R (5197) ✓ |
| breakout | 5m | -0.03R (5939) | -0.11R (6869) ✗ | -0.06R (1948) | -0.12R (3675) ✗ |
| liquidity_reversal | 15m | -0.42R (797) ✗ | -0.42R (744) ✗ | -0.34R (553) ✗ | -0.28R (752) ✗ |
| liquidity_reversal | 1h | -0.01R (24) | +0.12R (33) ✓ | -0.27R (92) ✗ | -0.20R (146) ✗ |
| liquidity_reversal | 30m | -0.30R (155) ✗ | -0.40R (133) ✗ | -0.39R (122) ✗ | -0.28R (114) ✗ |
| liquidity_reversal | 4h | +0.41R (6) | +0.02R (6) | - | +0.06R (4) |
| liquidity_reversal | 5m | -0.74R (1582) ✗ | -0.65R (1490) ✗ | -0.49R (1016) ✗ | -0.35R (1274) ✗ |
| mean_reversion | 15m | - | - | -0.32R (22124) ✗ | - |
| mean_reversion | 1h | - | - | -0.16R (7848) ✗ | - |
| mean_reversion | 30m | - | - | -0.24R (12817) ✗ | - |
| mean_reversion | 4h | - | - | -0.08R (2273) | - |
| momentum | 15m | -0.18R (3405) ✗ | -0.06R (3554) | - | +0.04R (403) ✓ |
| momentum | 1h | -0.10R (2676) | -0.05R (2378) | -0.03R (2008) | -0.17R (2201) ✗ |
| momentum | 30m | -0.18R (6131) ✗ | -0.11R (7062) ✗ | -0.20R (10553) ✗ | -0.20R (11845) ✗ |
| momentum | 4h | +0.09R (1150) ✓ | -0.07R (853) | +0.11R (949) ✓ | +0.06R (1881) ✓ |
| mtf_pullback | 15m | -0.24R (23537) ✗ | -0.19R (23627) ✗ | +0.03R (1414) ✓ | -0.06R (3573) |
| mtf_pullback | 1h | -0.11R (12605) ✗ | -0.07R (11830) | +0.04R (677) ✓ | +0.18R (1200) ✓ |
| mtf_pullback | 30m | -0.18R (13580) ✗ | -0.12R (13687) ✗ | +0.05R (819) ✓ | +0.01R (1643) ✓ |
| mtf_pullback | 4h | +0.05R (3435) ✓ | -0.00R (3187) | - | +0.41R (508) ✓ |
| mtf_pullback | 5m | -0.11R (3671) ✗ | -0.08R (3952) | -0.03R (1191) | -0.02R (2471) |
| smc | 15m | +0.06R (94) ✓ | -0.35R (70) ✗ | - | -1.36R (4) |
| smc | 1h | -0.30R (29) | -0.01R (57) | -0.30R (365) ✗ | +0.10R (395) ✓ |
| smc | 30m | -0.50R (142) ✗ | -0.41R (170) ✗ | -0.38R (418) ✗ | -0.19R (333) ✗ |
| trend_following | 15m | -0.25R (708) ✗ | -0.18R (787) ✗ | - | -0.34R (22) |
| trend_following | 1h | -0.12R (335) ✗ | +0.01R (334) ✓ | - | -0.29R (84) ✗ |
| trend_following | 30m | -0.26R (327) ✗ | -0.11R (431) ✗ | - | -0.20R (44) ✗ |
| trend_following | 4h | +0.33R (419) ✓ | -0.21R (43) ✗ | +1.14R (90) ✓ | +1.60R (569) ✓ |
| trend_following | 5m | -0.53R (746) ✗ | -0.45R (759) ✗ | - | -0.32R (119) ✗ |

✓ = made money with 30+ trades · ✗ = lost -0.10R or worse · fewer than 30 trades = no mark (too few to say).

## Each regime

### STRONG_BULL
- families (all their trades in this regime): breakout -0.01R (17012); momentum -0.12R (3524); mtf_pullback -0.16R (17033); trend_following -0.34R (643); liquidity_reversal -0.62R (761)
- made money here: TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.54R over 105 trades [BACKTESTING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.42R over 44 trades [PAPER_TRADING]; P01-BREAKOUT-V4-S1 v1.0 4h (lab) +0.36R over 69 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.35R over 66 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.31R over 81 trades [BACKTESTING]; TRD-H4-BREAKOUT v1.0 30m +0.30R over 83 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.80R over 460 trades; PB-B-SWEEP v1.0 5m -0.61R over 40 trades; ema_9_21_cross v1.0 30m -0.50R over 52 trades; ema_9_21_cross v1.0 5m -0.47R over 299 trades; liquidity_sweep_reversal v1.0 15m -0.39R over 189 trades; P07-SQUEEZE-RETEST-V3 v1.0 4h (lab) -0.39R over 31 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

### WEAK_BULL
- families (all their trades in this regime): breakout -0.06R (33342); momentum -0.15R (9743); mtf_pullback -0.18R (39567); trend_following -0.26R (1720); smc -0.37R (150); liquidity_reversal -0.64R (1578)
- made money here: P01-BREAKOUT-V3 v1.0 4h (lab) +0.51R over 85 trades [BACKTESTING]; P01-BREAKOUT-V4 v1.0 4h (lab) +0.50R over 204 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.44R over 128 trades [BACKTESTING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.41R over 132 trades [PAPER_TRADING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.40R over 178 trades [PAPER_TRADING]; donchian_breakout-VEXIT-S4-FDISP v1.0 4h (lab) +0.39R over 93 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.81R over 839 trades; PB-B-SWEEP v1.0 5m -0.71R over 88 trades; liquidity_sweep_reversal v1.0 30m -0.60R over 68 trades; ema_9_21_cross v1.0 5m -0.58R over 447 trades; liquidity_sweep_reversal v1.0 15m -0.52R over 343 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.45R over 102 trades
- no trade looks like: no setup, or the higher timeframes disagree

### RANGE
- families (all their trades in this regime): trend_following +0.35R (41); breakout +0.03R (4694); mtf_pullback +0.02R (3367); momentum -0.13R (10564); mean_reversion -0.25R (40066); smc -0.36R (757); liquidity_reversal -0.44R (1568)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.41R over 95 trades [VALIDATION]; P13-TURTLE-C v1.0 4h (lab) +0.35R over 41 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 30m (lab) +0.34R over 58 trades [BACKTESTING]; TRD-H4-PULLBACK v1.0 30m +0.30R over 94 trades [FAILED]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.30R over 49 trades [BACKTESTING]; TRD-H4-PULLBACK-S2 v1.0 30m (lab) +0.28R over 129 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.75R over 385 trades; PB-B-SWEEP v1.0 5m -0.57R over 230 trades; PB-B-SWEEP-15M v1.0 15m -0.51R over 63 trades; liquidity_sweep_reversal v1.0 15m -0.50R over 255 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.47R over 302 trades; liquidity_sweep_reversal v1.0 30m -0.41R over 116 trades
- no trade looks like: price in the middle of the range; breakouts without volume

### HIGH_VOL_RANGE
- families (all their trades in this regime): momentum -0.10R (422); mean_reversion -0.15R (2250)
- made money here: R4-CLUC v1.0 15m (lab) +0.17R over 40 trades [FAILED]; R4-CLUC v1.0 30m (lab) +0.02R over 40 trades [FAILED]; P11-MOMENTUM-C v1.0 30m (lab) +0.01R over 161 trades [FAILED]
- lost money here: P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.32R over 58 trades; P06-VWAP-REVERSION-V2 v1.0 15m (lab) -0.30R over 209 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.27R over 39 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.23R over 441 trades; P11-MOMENTUM-V1-FRETEST-FDISP v1.0 30m (lab) -0.21R over 33 trades; rsi2_dip_buy v1.0 15m -0.19R over 368 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise

### WEAK_BEAR
- families (all their trades in this regime): breakout -0.06R (33174); momentum -0.09R (10803); mtf_pullback -0.13R (40580); trend_following -0.20R (1679); smc -0.26R (175); liquidity_reversal -0.60R (1523)
- made money here: P01-BREAKOUT-V2-FDISP-FNOTEXT v1.0 30m (lab) +0.59R over 43 trades [BACKTESTING]; donchian_breakout-VEXIT-S4-FDISP-FNOTEXT v1.0 30m (lab) +0.54R over 61 trades [BACKTESTING]; donchian_breakout-VEXIT-S4-FDISP v1.0 4h (lab) +0.45R over 108 trades [BACKTESTING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.40R over 115 trades [PAPER_TRADING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.30R over 152 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 15m (lab) +0.30R over 38 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.88R over 125 trades; PB-B-SWEEP-15M v1.0 15m -0.76R over 38 trades; liquidity_sweep_reversal v1.0 5m -0.73R over 708 trades; liquidity_sweep_reversal v1.0 15m -0.58R over 270 trades; P09-SWEEP-MSS-V5 v1.0 30m (lab) -0.46R over 38 trades; ema_9_21_cross v1.0 5m -0.41R over 473 trades
- no trade looks like: no setup, or the higher timeframes disagree

### STRONG_BEAR
- families (all their trades in this regime): momentum -0.06R (2970); breakout -0.06R (14467); mtf_pullback -0.13R (15535); trend_following -0.34R (595); liquidity_reversal -0.56R (600)
- made money here: TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.53R over 44 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 30m (lab) +0.49R over 45 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.34R over 60 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-FNOTEXT v1.0 15m (lab) +0.34R over 33 trades [FAILED]; TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 15m (lab) +0.34R over 33 trades [FAILED]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 30m (lab) +0.28R over 67 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.63R over 384 trades; PB-B-SWEEP v1.0 5m -0.56R over 39 trades; ema_9_21_cross v1.0 5m -0.51R over 286 trades; liquidity_sweep_reversal v1.0 15m -0.47R over 131 trades; P07-SQUEEZE-RETEST-V5 v1.0 30m (lab) -0.35R over 125 trades; P03-FIB-PULLBACK-V4 v1.0 4h (lab) -0.34R over 38 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend

### EXPANSION
- families (all their trades in this regime): trend_following +0.99R (574); breakout +0.06R (32616); mtf_pullback +0.01R (5222); momentum -0.08R (2185); liquidity_reversal -0.09R (85)
- made money here: P13-TURTLE-V2 v1.0 4h (lab) +2.65R over 57 trades [VALIDATION]; P13-TURTLE-V1 v1.0 4h (lab) +2.44R over 64 trades [VALIDATION]; P13-TURTLE-V3 v1.0 4h (lab) +2.36R over 59 trades [VALIDATION]; P13-TURTLE-V3-S2 v1.0 4h (lab) +2.35R over 61 trades [VALIDATION]; P02-EMA-PULLBACK-V4-S6-FHTF-S4-S6 v1.0 4h (lab) +0.91R over 30 trades [BACKTESTING]; TRD-H4-PULLBACK-S2 v1.0 1h (lab) +0.40R over 351 trades [BACKTESTING]
- lost money here: P11-MOMENTUM-V1 v1.0 30m (lab) -0.52R over 45 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.47R over 36 trades; supertrend_flip v1.0 1h -0.40R over 37 trades; P02-EMA-PULLBACK-V5 v1.0 30m (lab) -0.38R over 43 trades; P02-EMA-PULLBACK-V5 v1.0 1h (lab) -0.37R over 50 trades; P08-SESSION-BREAKOUT-V5 v1.0 30m (lab) -0.36R over 127 trades
- no trade looks like: the move is already several ATRs old (late entry)

### COMPRESSION
- families (all their trades in this regime): mtf_pullback -0.01R (707); breakout -0.15R (852); momentum -0.29R (2407); mean_reversion -0.47R (2667); liquidity_reversal -0.92R (33)
- made money here: TRD-H4-PULLBACK-noT4 v1.0 1h +0.19R over 83 trades [FAILED]; P12-LEADER-C v1.0 4h (lab) +0.15R over 113 trades [FAILED]; donchian_breakout-VEXIT-S4 v1.1 30m (lab) +0.13R over 45 trades [FAILED]; TRD-H4-BREAKOUT-S3 v1.0 15m (lab) +0.11R over 39 trades [FAILED]; bb_squeeze_breakout v1.0 1h +0.10R over 57 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-S2 v1.0 30m (lab) +0.07R over 30 trades [BACKTESTING]
- lost money here: PB-B-SWEEP v1.0 5m -0.92R over 33 trades; bb_squeeze_breakout v1.0 15m -0.70R over 62 trades; P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.59R over 38 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.52R over 1721 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.44R over 173 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.44R over 112 trades
- no trade looks like: before the break: wait for a close outside the range

### TRANSITION
- families (all their trades in this regime): trend_following +0.20R (49); mtf_pullback +0.01R (3971); breakout -0.01R (5212); smc -0.03R (724); momentum -0.14R (7684); liquidity_reversal -0.31R (1595)
- made money here: TRD-H4-BREAKOUT-FDISP-S2 v1.0 1h (lab) +0.59R over 60 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 1h (lab) +0.52R over 70 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.43R over 62 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 30m (lab) +0.43R over 55 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.42R over 31 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 1h (lab) +0.40R over 41 trades [BACKTESTING]
- lost money here: TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 5m (lab) -0.69R over 36 trades; TRD-H4-BREAKOUT-FDISP-FNOTEXT v1.0 5m (lab) -0.65R over 33 trades; PB-B-SWEEP v1.0 5m -0.60R over 174 trades; PB-B-SWEEP-15M v1.0 15m -0.55R over 38 trades; liquidity_sweep_reversal v1.0 5m -0.51R over 389 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.50R over 100 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

### UNCLEAR
- families (all their trades in this regime): trend_following -0.12R (49); momentum -0.21R (6384); liquidity_reversal -0.36R (475)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.18R over 81 trades [VALIDATION]; P12-LEADER-V3 v1.0 1h (lab) +0.07R over 106 trades [FAILED]; P12-LEADER-V1 v1.0 4h (lab) +0.05R over 99 trades [BACKTESTING]
- lost money here: PB-B-SWEEP-15M v1.0 15m -0.74R over 30 trades; PB-B-SWEEP v1.0 5m -0.57R over 133 trades; P11-MOMENTUM-V1-FDISP v1.0 30m (lab) -0.40R over 430 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.32R over 205 trades; P11-MOMENTUM-V1 v1.0 30m (lab) -0.30R over 743 trades; P11-MOMENTUM-V4 v1.0 30m (lab) -0.27R over 634 trades
- no trade looks like: the data does not show a regime - stand aside

