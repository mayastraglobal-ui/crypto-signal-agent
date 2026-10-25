# Regime playbook (generated - do not edit)

Written by the Sunday research run 2026-10-25 01:12 UTC (updated weekly) from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## Which families work where (family x timeframe x regime group)

| Family | TF | BULL | BEAR | RANGE | TRANSITION |
|---|---|---|---|---|---|
| breakout | 15m | -0.17R (10720) ✗ | -0.12R (9949) ✗ | -0.08R (1321) | -0.10R (3339) ✗ |
| breakout | 1h | -0.02R (10435) | -0.12R (8503) ✗ | +0.06R (684) ✓ | +0.12R (11489) ✓ |
| breakout | 30m | -0.07R (8956) | -0.04R (7964) | +0.02R (899) ✓ | -0.03R (4688) |
| breakout | 4h | +0.27R (3173) ✓ | +0.08R (2625) ✓ | -0.18R (40) ✗ | +0.14R (4299) ✓ |
| breakout | 5m | -0.02R (4196) | -0.15R (4273) ✗ | -0.15R (1287) ✗ | -0.18R (2272) ✗ |
| liquidity_reversal | 15m | -0.41R (808) ✗ | -0.41R (725) ✗ | -0.33R (550) ✗ | -0.27R (746) ✗ |
| liquidity_reversal | 1h | -0.01R (24) | +0.12R (32) ✓ | -0.27R (92) ✗ | -0.20R (146) ✗ |
| liquidity_reversal | 30m | -0.29R (156) ✗ | -0.43R (126) ✗ | -0.41R (120) ✗ | -0.25R (114) ✗ |
| liquidity_reversal | 4h | +0.41R (6) | -1.09R (2) | - | +0.06R (4) |
| liquidity_reversal | 5m | -0.70R (1654) ✗ | -0.68R (1439) ✗ | -0.49R (1028) ✗ | -0.35R (1312) ✗ |
| mean_reversion | 15m | - | - | -0.32R (22146) ✗ | - |
| mean_reversion | 1h | - | - | -0.16R (7810) ✗ | - |
| mean_reversion | 30m | - | - | -0.23R (12853) ✗ | - |
| mean_reversion | 4h | - | - | -0.09R (2250) | - |
| momentum | 15m | -0.18R (3457) ✗ | -0.07R (3455) | - | +0.02R (411) ✓ |
| momentum | 1h | -0.09R (2317) | -0.06R (1936) | -0.04R (1276) | -0.18R (1577) ✗ |
| momentum | 30m | -0.19R (4892) ✗ | -0.12R (5321) ✗ | -0.22R (7553) ✗ | -0.21R (8618) ✗ |
| momentum | 4h | +0.09R (1147) ✓ | -0.07R (848) | +0.12R (943) ✓ | +0.06R (1878) ✓ |
| mtf_pullback | 15m | -0.25R (23035) ✗ | -0.20R (22107) ✗ | -0.04R (1133) | -0.10R (2874) ✗ |
| mtf_pullback | 1h | -0.12R (12041) ✗ | -0.08R (11194) | +0.01R (558) ✓ | +0.06R (719) ✓ |
| mtf_pullback | 30m | -0.19R (13318) ✗ | -0.13R (12913) ✗ | -0.02R (661) | -0.07R (1153) |
| mtf_pullback | 4h | +0.02R (2422) ✓ | -0.02R (2243) | - | +0.39R (420) ✓ |
| mtf_pullback | 5m | -0.11R (2990) ✗ | -0.12R (2823) ✗ | -0.08R (921) | -0.01R (1817) |
| smc | 15m | +0.06R (94) ✓ | -0.34R (68) ✗ | - | -1.36R (4) |
| smc | 1h | -0.30R (29) | -0.09R (55) | -0.29R (364) ✗ | +0.10R (389) ✓ |
| smc | 30m | -0.51R (145) ✗ | -0.39R (165) ✗ | -0.40R (434) ✗ | -0.15R (334) ✗ |
| trend_following | 15m | -0.23R (729) ✗ | -0.18R (768) ✗ | - | -0.31R (23) |
| trend_following | 1h | -0.19R (210) ✗ | -0.10R (196) | - | -0.26R (73) ✗ |
| trend_following | 30m | -0.25R (335) ✗ | -0.14R (417) ✗ | - | -0.12R (39) ✗ |
| trend_following | 4h | -0.14R (30) ✗ | -0.15R (26) | - | +0.19R (14) |
| trend_following | 5m | -0.53R (787) ✗ | -0.46R (721) ✗ | - | -0.33R (127) ✗ |

✓ = made money with 30+ trades · ✗ = lost -0.10R or worse · fewer than 30 trades = no mark (too few to say).

## Each regime

### STRONG_BULL
- families (all their trades in this regime): breakout -0.03R (12193); momentum -0.12R (3295); mtf_pullback -0.18R (16027); trend_following -0.39R (631); liquidity_reversal -0.59R (788)
- made money here: TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.54R over 105 trades [BACKTESTING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.42R over 44 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.35R over 66 trades [BACKTESTING]; TRD-H4-BREAKOUT v1.0 30m +0.30R over 83 trades [BACKTESTING]; TRD-H4-BREAKOUT v1.0 1h +0.30R over 79 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.29R over 82 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.76R over 483 trades; PB-B-SWEEP v1.0 5m -0.62R over 42 trades; ema_9_21_cross v1.0 30m -0.50R over 56 trades; ema_9_21_cross v1.0 5m -0.47R over 322 trades; P11-MOMENTUM-V4 v1.0 30m (lab) -0.41R over 119 trades; liquidity_sweep_reversal v1.0 15m -0.39R over 189 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

### WEAK_BULL
- families (all their trades in this regime): breakout -0.06R (25144); momentum -0.15R (8425); mtf_pullback -0.19R (37586); trend_following -0.32R (1448); smc -0.37R (152); liquidity_reversal -0.62R (1631)
- made money here: P01-BREAKOUT-V3 v1.0 4h (lab) +0.51R over 85 trades [BACKTESTING]; P01-BREAKOUT-V4 v1.0 4h (lab) +0.51R over 203 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.45R over 127 trades [PAPER_TRADING]; donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.41R over 132 trades [PAPER_TRADING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.40R over 178 trades [PAPER_TRADING]; P04-MACD-SUPERTREND-V3 v1.0 4h (lab) +0.38R over 63 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.78R over 876 trades; PB-B-SWEEP v1.0 5m -0.69R over 91 trades; liquidity_sweep_reversal v1.0 30m -0.59R over 69 trades; ema_9_21_cross v1.0 5m -0.57R over 465 trades; liquidity_sweep_reversal v1.0 15m -0.50R over 348 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.45R over 104 trades
- no trade looks like: no setup, or the higher timeframes disagree

### RANGE
- families (all their trades in this regime): breakout -0.03R (3074); mtf_pullback -0.04R (2699); momentum -0.14R (7629); mean_reversion -0.25R (40082); smc -0.36R (771); liquidity_reversal -0.45R (1572)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.42R over 94 trades [VALIDATION]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 30m (lab) +0.34R over 58 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.30R over 49 trades [BACKTESTING]; P12-LEADER-V1 v1.0 4h (lab) +0.26R over 101 trades [BACKTESTING]; TRD-H4-PULLBACK v1.0 30m +0.25R over 93 trades [FAILED]; TRD-H4-BREAKOUT-S3-FDISP v1.0 30m (lab) +0.24R over 33 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.76R over 394 trades; PB-B-SWEEP v1.0 5m -0.56R over 228 trades; liquidity_sweep_reversal v1.0 15m -0.50R over 255 trades; PB-B-SWEEP-15M v1.0 15m -0.49R over 64 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.47R over 313 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.42R over 86 trades
- no trade looks like: price in the middle of the range; breakouts without volume

### HIGH_VOL_RANGE
- families (all their trades in this regime): momentum -0.06R (304); mean_reversion -0.15R (2226)
- made money here: R4-CLUC v1.0 15m (lab) +0.13R over 39 trades [FAILED]; P11-MOMENTUM-C v1.0 30m (lab) +0.01R over 161 trades [FAILED]
- lost money here: P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.32R over 58 trades; P06-VWAP-REVERSION-V2 v1.0 15m (lab) -0.32R over 205 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.23R over 436 trades; rsi2_dip_buy v1.0 15m -0.19R over 364 trades; P05-RANGE-REVERSAL-V2 v1.0 30m (lab) -0.18R over 185 trades; P11-MOMENTUM-V1 v1.0 30m (lab) -0.16R over 54 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise

### WEAK_BEAR
- families (all their trades in this regime): breakout -0.07R (23692); momentum -0.10R (8868); mtf_pullback -0.15R (37334); trend_following -0.23R (1507); smc -0.28R (172); liquidity_reversal -0.62R (1514)
- made money here: donchian_breakout-VEXIT-FDISP v1.0 4h (lab) +0.36R over 113 trades [PAPER_TRADING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.31R over 151 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 15m (lab) +0.27R over 34 trades [FAILED]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 15m (lab) +0.27R over 137 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 15m (lab) +0.24R over 98 trades [FAILED]; TRD-H4-BREAKOUT-FDISP-FNOTEXT v1.0 15m (lab) +0.24R over 32 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.86R over 127 trades; liquidity_sweep_reversal v1.0 5m -0.78R over 683 trades; PB-B-SWEEP-15M v1.0 15m -0.76R over 36 trades; liquidity_sweep_reversal v1.0 15m -0.57R over 263 trades; P09-SWEEP-MSS-V5 v1.0 30m (lab) -0.48R over 36 trades; PB-B-SWEEP-LIMIT v1.0 5m -0.45R over 31 trades
- no trade looks like: no setup, or the higher timeframes disagree

### STRONG_BEAR
- families (all their trades in this regime): momentum -0.06R (2622); breakout -0.13R (9357); mtf_pullback -0.15R (13802); trend_following -0.35R (575); liquidity_reversal -0.57R (569)
- made money here: TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.33R over 40 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 30m (lab) +0.30R over 41 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP-S2 v1.0 30m (lab) +0.19R over 56 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 15m (lab) +0.15R over 138 trades [BACKTESTING]; P07-SQUEEZE-RETEST-V4-S2 v1.0 4h (lab) +0.14R over 69 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.13R over 71 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.66R over 358 trades; PB-B-SWEEP v1.0 5m -0.55R over 38 trades; ema_9_21_cross v1.0 5m -0.53R over 272 trades; liquidity_sweep_reversal v1.0 15m -0.45R over 128 trades; P07-SQUEEZE-RETEST-V5 v1.0 30m (lab) -0.36R over 123 trades; P03-FIB-PULLBACK-V4 v1.0 4h (lab) -0.34R over 38 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend

### EXPANSION
- families (all their trades in this regime): breakout +0.06R (22728); momentum -0.06R (2062); mtf_pullback -0.06R (3716); liquidity_reversal -0.11R (83); trend_following -0.31R (200)
- made money here: TRD-H4-BREAKOUT-FDISP-S2 v1.0 1h (lab) +0.28R over 337 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 1h (lab) +0.28R over 279 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.23R over 391 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 1h (lab) +0.23R over 390 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.22R over 389 trades [PAPER_TRADING]; TRD-H4-BREAKOUT-S3-FDISP v1.0 1h (lab) +0.22R over 295 trades [BACKTESTING]
- lost money here: P11-MOMENTUM-V1 v1.0 30m (lab) -0.49R over 43 trades; P02-EMA-PULLBACK-V5 v1.0 30m (lab) -0.38R over 43 trades; P02-EMA-PULLBACK-V5 v1.0 1h (lab) -0.37R over 50 trades; supertrend_flip v1.0 1h -0.36R over 33 trades; P04-MACD-SUPERTREND-V2 v1.0 1h (lab) -0.35R over 68 trades; P08-SESSION-BREAKOUT-V2 v1.0 30m (lab) -0.33R over 64 trades
- no trade looks like: the move is already several ATRs old (late entry)

### COMPRESSION
- families (all their trades in this regime): mtf_pullback -0.02R (562); breakout -0.15R (579); momentum -0.32R (1743); mean_reversion -0.47R (2672); liquidity_reversal -0.92R (33)
- made money here: TRD-H4-PULLBACK-noT4 v1.0 1h +0.22R over 81 trades [FAILED]; P12-LEADER-C v1.0 4h (lab) +0.15R over 113 trades [FAILED]; donchian_breakout-VEXIT-S4 v1.1 30m (lab) +0.11R over 44 trades [FAILED]; bb_squeeze_breakout v1.0 1h +0.10R over 57 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3 v1.0 15m (lab) +0.08R over 40 trades [FAILED]; TRD-H4-PULLBACK-noT4 v1.0 30m +0.06R over 96 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.92R over 33 trades; bb_squeeze_breakout v1.0 15m -0.69R over 61 trades; P06-VWAP-REVERSION-V2 v1.0 30m (lab) -0.54R over 39 trades; P05-RANGE-REVERSAL-V2 v1.0 15m (lab) -0.51R over 1723 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.45R over 111 trades; P06-VWAP-REVERSION-V2 v1.0 15m (lab) -0.44R over 429 trades
- no trade looks like: before the break: wait for a close outside the range

### TRANSITION
- families (all their trades in this regime): mtf_pullback -0.01R (3083); smc -0.02R (719); breakout -0.09R (3195); momentum -0.15R (5737); liquidity_reversal -0.32R (1629)
- made money here: TRD-H4-BREAKOUT-FDISP-S2 v1.0 1h (lab) +0.62R over 59 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 1h (lab) +0.54R over 69 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3-FDISP-S2 v1.0 30m (lab) +0.46R over 54 trades [BACKTESTING]; TRD-H4-BREAKOUT-S3 v1.0 1h (lab) +0.43R over 62 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 30m (lab) +0.42R over 31 trades [BACKTESTING]; TRD-H4-BREAKOUT-FDISP v1.0 1h (lab) +0.40R over 41 trades [BACKTESTING]
- lost money here: TRD-H4-BREAKOUT-S3-FDISP-FNOTEXT v1.0 5m (lab) -0.73R over 38 trades; TRD-H4-BREAKOUT-FDISP-FNOTEXT v1.0 5m (lab) -0.68R over 34 trades; PB-B-SWEEP v1.0 5m -0.60R over 176 trades; PB-B-SWEEP-15M v1.0 15m -0.55R over 38 trades; TRD-H4-BREAKOUT-S3-FDISP v1.0 5m (lab) -0.54R over 106 trades; liquidity_sweep_reversal v1.0 5m -0.53R over 400 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

### UNCLEAR
- families (all their trades in this regime): momentum -0.21R (4621); liquidity_reversal -0.32R (509)
- made money here: P12-LEADER-V2 v1.0 4h (lab) +0.18R over 81 trades [VALIDATION]; P12-LEADER-V3 v1.0 1h (lab) +0.07R over 106 trades [FAILED]; P12-LEADER-V1 v1.0 4h (lab) +0.05R over 99 trades [BACKTESTING]
- lost money here: PB-B-SWEEP-15M v1.0 15m -0.74R over 30 trades; PB-B-SWEEP v1.0 5m -0.55R over 132 trades; P11-MOMENTUM-V2 v1.0 30m (lab) -0.32R over 203 trades; P11-MOMENTUM-V1 v1.0 30m (lab) -0.31R over 732 trades; P11-MOMENTUM-V4 v1.0 30m (lab) -0.26R over 630 trades; P11-MOMENTUM-C v1.0 30m (lab) -0.24R over 1835 trades
- no trade looks like: the data does not show a regime - stand aside

