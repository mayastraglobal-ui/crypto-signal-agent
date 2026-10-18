# Regime playbook (generated - do not edit)

Written by the Sunday research run 2026-10-18 01:12 UTC (updated weekly) from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## Which families work where (family x timeframe x regime group)

| Family | TF | BULL | BEAR | RANGE | TRANSITION |
|---|---|---|---|---|---|
| breakout | 15m | -0.18R (9873) ✗ | -0.14R (9210) ✗ | -0.10R (1003) ✗ | -0.10R (2910) ✗ |
| breakout | 1h | -0.03R (9485) | -0.11R (7734) ✗ | +0.08R (551) ✓ | +0.10R (9826) ✓ |
| breakout | 30m | -0.08R (8079) | -0.06R (7207) | -0.04R (739) | -0.04R (4063) |
| breakout | 4h | +0.28R (2308) ✓ | +0.07R (1852) ✓ | -0.18R (40) ✗ | +0.14R (3438) ✓ |
| breakout | 5m | -0.03R (3032) | -0.15R (3069) ✗ | -0.15R (908) ✗ | -0.17R (1662) ✗ |
| liquidity_reversal | 15m | -0.41R (833) ✗ | -0.39R (749) ✗ | -0.33R (549) ✗ | -0.27R (748) ✗ |
| liquidity_reversal | 1h | +0.20R (28) | +0.18R (36) ✓ | -0.27R (92) ✗ | -0.20R (146) ✗ |
| liquidity_reversal | 30m | -0.31R (164) ✗ | -0.40R (140) ✗ | -0.41R (120) ✗ | -0.25R (114) ✗ |
| liquidity_reversal | 4h | +0.41R (6) | -1.09R (2) | - | +0.06R (4) |
| liquidity_reversal | 5m | -0.71R (1681) ✗ | -0.67R (1434) ✗ | -0.50R (1035) ✗ | -0.35R (1312) ✗ |
| mean_reversion | 15m | - | - | -0.32R (22144) ✗ | - |
| mean_reversion | 1h | - | - | -0.16R (7794) ✗ | - |
| mean_reversion | 30m | - | - | -0.23R (12837) ✗ | - |
| mean_reversion | 4h | - | - | -0.09R (2249) | - |
| momentum | 15m | -0.19R (3473) ✗ | -0.06R (3437) | - | +0.02R (411) ✓ |
| momentum | 1h | -0.09R (2315) | -0.06R (1930) | -0.05R (1263) | -0.18R (1574) ✗ |
| momentum | 30m | -0.18R (4910) ✗ | -0.12R (5300) ✗ | -0.22R (7507) ✗ | -0.21R (8592) ✗ |
| momentum | 4h | +0.09R (1147) ✓ | -0.07R (846) | +0.12R (943) ✓ | +0.06R (1878) ✓ |
| mtf_pullback | 15m | -0.25R (23169) ✗ | -0.20R (22043) ✗ | -0.04R (1145) | -0.10R (2886) ✗ |
| mtf_pullback | 1h | -0.12R (12040) ✗ | -0.08R (11170) | +0.01R (558) ✓ | +0.06R (719) ✓ |
| mtf_pullback | 30m | -0.19R (13393) ✗ | -0.13R (12878) ✗ | -0.03R (668) | -0.07R (1161) |
| mtf_pullback | 4h | +0.02R (2421) ✓ | -0.01R (2236) | - | +0.39R (420) ✓ |
| mtf_pullback | 5m | -0.11R (3028) ✗ | -0.12R (2816) ✗ | -0.08R (924) | -0.02R (1825) |
| smc | 15m | +0.06R (94) ✓ | -0.38R (67) ✗ | - | -1.36R (4) |
| smc | 1h | -0.30R (29) | -0.09R (55) | -0.29R (364) ✗ | +0.10R (389) ✓ |
| smc | 30m | -0.51R (145) ✗ | -0.40R (166) ✗ | -0.41R (441) ✗ | -0.16R (335) ✗ |
| trend_following | 15m | -0.23R (735) ✗ | -0.18R (766) ✗ | - | -0.31R (23) |
| trend_following | 1h | -0.19R (210) ✗ | -0.10R (196) | - | -0.26R (73) ✗ |
| trend_following | 30m | -0.26R (338) ✗ | -0.14R (417) ✗ | - | -0.12R (39) ✗ |
| trend_following | 4h | -0.14R (30) ✗ | -0.15R (26) | - | +0.19R (14) |
| trend_following | 5m | -0.54R (798) ✗ | -0.46R (720) ✗ | - | -0.34R (128) ✗ |

✓ = made money with 30+ trades · ✗ = lost -0.10R or worse · fewer than 30 trades = no mark (too few to say).

## Each regime

### STRONG_BULL
- families (all their trades in this regime): breakout -0.04R (10451); momentum -0.12R (3312); mtf_pullback -0.18R (16103); trend_following -0.38R (636); liquidity_reversal -0.59R (825)
- made money here: TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.54R over 105 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.35R over 66 trades [BACKTESTING]; TRD-H4-BREAKOUT v1.0 1h +0.30R over 79 trades [BACKTESTING]; TRD-H4-BREAKOUT v1.0 30m +0.29R over 84 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.24R over 54 trades [PAPER_TRADING]; donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.24R over 54 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.76R over 485 trades; PB-B-SWEEP v1.0 5m -0.62R over 42 trades; ema_9_21_cross v1.0 30m -0.50R over 56 trades; ema_9_21_cross v1.0 5m -0.47R over 323 trades; P09-SWEEP-MSS-V5 v1.0 15m (lab) -0.43R over 35 trades; P11-MOMENTUM-V4 v1.0 30m (lab) -0.41R over 120 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

### WEAK_BULL
- families (all their trades in this regime): breakout -0.08R (22290); momentum -0.15R (8440); mtf_pullback -0.19R (37755); trend_following -0.33R (1463); smc -0.37R (152); liquidity_reversal -0.63R (1700)
- made money here: P01-BREAKOUT-V3 v1.0 4h (lab) +0.51R over 85 trades [BACKTESTING]; P01-BREAKOUT-V4 v1.0 4h (lab) +0.51R over 203 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.45R over 127 trades [PAPER_TRADING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.41R over 177 trades [PAPER_TRADING]; P04-MACD-SUPERTREND-V3 v1.0 4h (lab) +0.38R over 63 trades [BACKTESTING]; P01-BREAKOUT-V1 v1.0 4h (lab) +0.37R over 220 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.79R over 898 trades; PB-B-SWEEP v1.0 5m -0.72R over 94 trades; liquidity_sweep_reversal v1.0 30m -0.59R over 69 trades; ema_9_21_cross v1.0 5m -0.58R over 475 trades; liquidity_sweep_reversal v1.0 15m -0.50R over 348 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.45R over 104 trades
- no trade looks like: no setup, or the higher timeframes disagree

### RANGE
- families (all their trades in this regime): mtf_pullback -0.05R (2718); breakout -0.06R (2341); momentum -0.14R (7577); mean_reversion -0.25R (40039); smc -0.37R (778); liquidity_reversal -0.45R (1578)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.42R over 94 trades [VALIDATION]; P12-LEADER-V1 v1.0 4h (lab) +0.26R over 101 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 30m (lab) +0.24R over 33 trades [BACKTESTING]; TRD-H4-PULLBACK v1.0 30m +0.24R over 94 trades [FAILED]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.18R over 33 trades [BACKTESTING]; TRD-H4-BREAKOUT v1.0 1h +0.16R over 57 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.76R over 398 trades; PB-B-SWEEP v1.0 5m -0.57R over 229 trades; liquidity_sweep_reversal v1.0 15m -0.50R over 255 trades; PB-B-SWEEP-15M v1.0 15m -0.49R over 64 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.48R over 316 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.42R over 86 trades
- no trade looks like: price in the middle of the range; breakouts without volume

### HIGH_VOL_RANGE
- families (all their trades in this regime): momentum -0.07R (302); mean_reversion -0.15R (2225)
- made money here: R4-CLUC v1.0 15m (lab) +0.13R over 39 trades [FAILED]
- lost money here: P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.32R over 58 trades; P06-VWAP-REVERSION-V2 v1.0 15m (lab) -0.32R over 205 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.23R over 436 trades; rsi2_dip_buy v1.0 15m -0.19R over 364 trades; P05-RANGE-REVERSAL-V2 v1.0 30m (lab) -0.18R over 185 trades; P11-MOMENTUM-V1 v1.0 30m (lab) -0.16R over 54 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise

### WEAK_BEAR
- families (all their trades in this regime): breakout -0.09R (21083); momentum -0.10R (8827); mtf_pullback -0.15R (37226); trend_following -0.24R (1508); smc -0.29R (173); liquidity_reversal -0.59R (1565)
- made money here: donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.31R over 151 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-FDISP v1.0 15m (lab) +0.24R over 98 trades [FAILED]; donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.23R over 199 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.22R over 160 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 15m (lab) +0.20R over 101 trades [BACKTESTING]; TRD-H4-PULLBACK v1.0 1h +0.19R over 151 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.86R over 127 trades; liquidity_sweep_reversal v1.0 5m -0.77R over 675 trades; PB-B-SWEEP-15M v1.0 15m -0.76R over 36 trades; liquidity_sweep_reversal v1.0 15m -0.57R over 263 trades; PB-B-SWEEP-LIMIT v1.0 5m -0.45R over 31 trades; ema_9_21_cross v1.0 5m -0.42R over 450 trades
- no trade looks like: no setup, or the higher timeframes disagree

### STRONG_BEAR
- families (all their trades in this regime): momentum -0.06R (2616); breakout -0.14R (7891); mtf_pullback -0.15R (13773); trend_following -0.34R (571); liquidity_reversal -0.58R (570)
- made money here: TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.33R over 40 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 30m (lab) +0.30R over 41 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.13R over 71 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 15m (lab) +0.13R over 94 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3 v1.0 30m (lab) +0.12R over 90 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 15m (lab) +0.12R over 95 trades [FAILED]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.67R over 357 trades; PB-B-SWEEP v1.0 5m -0.55R over 39 trades; ema_9_21_cross v1.0 5m -0.52R over 270 trades; liquidity_sweep_reversal v1.0 15m -0.45R over 128 trades; P07-SQUEEZE-RETEST-V5 v1.0 30m (lab) -0.38R over 122 trades; P03-FIB-PULLBACK-V4 v1.0 4h (lab) -0.34R over 38 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend

### EXPANSION
- families (all their trades in this regime): breakout +0.05R (19437); momentum -0.06R (2062); mtf_pullback -0.06R (3730); liquidity_reversal -0.12R (84); trend_following -0.31R (201)
- made money here: TRD-H4-BREAKOUT-FDISP v1.0 1h (lab) +0.28R over 279 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.23R over 391 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.22R over 389 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 1h (lab) +0.22R over 295 trades [BACKTESTING]; P12-LEADER-C v1.0 4h (lab) +0.22R over 135 trades [FAILED]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.22R over 280 trades [PAPER_TRADING]
- lost money here: P11-MOMENTUM-V1 v1.0 30m (lab) -0.49R over 43 trades; P02-EMA-PULLBACK-V5 v1.0 30m (lab) -0.38R over 43 trades; P02-EMA-PULLBACK-V5 v1.0 1h (lab) -0.37R over 50 trades; supertrend_flip v1.0 1h -0.36R over 33 trades; P04-MACD-SUPERTREND-V2 v1.0 1h (lab) -0.35R over 68 trades; ema_9_21_cross v1.0 5m -0.34R over 128 trades
- no trade looks like: the move is already several ATRs old (late entry)

### COMPRESSION
- families (all their trades in this regime): mtf_pullback -0.02R (565); breakout -0.15R (579); momentum -0.32R (1739); mean_reversion -0.47R (2681); liquidity_reversal -0.92R (33)
- made money here: TRD-H4-PULLBACK-noT4 v1.0 1h +0.22R over 81 trades [FAILED]; P12-LEADER-C v1.0 4h (lab) +0.15R over 113 trades [FAILED]; donchian_breakout-VEXIT-S4 v1.1 30m (lab) +0.11R over 44 trades [FAILED]; bb_squeeze_breakout v1.0 1h +0.10R over 57 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3 v1.0 15m (lab) +0.08R over 40 trades [FAILED]; TRD-H4-PULLBACK-noT4 v1.0 30m +0.05R over 97 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.92R over 33 trades; bb_squeeze_breakout v1.0 15m -0.69R over 61 trades; P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.54R over 39 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.52R over 1729 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.45R over 111 trades; P06-VWAP-REVERSION-V2 v1.0 15m (lab) -0.44R over 431 trades
- no trade looks like: before the break: wait for a close outside the range

### TRANSITION
- families (all their trades in this regime): mtf_pullback -0.01R (3097); smc -0.02R (720); breakout -0.12R (2410); momentum -0.16R (5724); liquidity_reversal -0.32R (1632)
- made money here: TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.43R over 62 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.42R over 31 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 1h (lab) +0.40R over 41 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 1h (lab) +0.40R over 42 trades [BACKTESTING]; P12-LEADER-V2 v1.0 4h (lab) +0.36R over 105 trades [VALIDATION]; TRD-H4-BREAKOUT-S3-FDISP v1.0 30m (lab) +0.33R over 33 trades [BACKTESTING]
- lost money here: PB-B-SWEEP v1.0 5m -0.61R over 177 trades; PB-B-SWEEP-15M v1.0 15m -0.55R over 38 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.54R over 106 trades; liquidity_sweep_reversal v1.0 5m -0.53R over 400 trades; TRD-H4-BREAKOUT-FDISP v1.0 5m (lab) -0.52R over 104 trades; TRD-H4-BREAKOUT-noT4 v1.0 5m -0.29R over 433 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

### UNCLEAR
- families (all their trades in this regime): momentum -0.21R (4605); liquidity_reversal -0.29R (479)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.18R over 81 trades [VALIDATION]; P12-LEADER-V3 v1.0 1h (lab) +0.07R over 106 trades [FAILED]; P12-LEADER-V1 v1.0 4h (lab) +0.05R over 99 trades [BACKTESTING]
- lost money here: PB-B-SWEEP v1.0 5m -0.54R over 129 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.32R over 203 trades; P11-MOMENTUM-V1 v1.0 30m (lab) -0.31R over 727 trades; P11-MOMENTUM-V4 v1.0 30m (lab) -0.27R over 631 trades; P11-MOMENTUM-C v1.0 30m (lab) -0.24R over 1824 trades; PB-B-GRADED v1.0 15m -0.23R over 144 trades
- no trade looks like: the data does not show a regime - stand aside

