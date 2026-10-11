# Regime playbook (generated - do not edit)

Written by the Sunday research run 2026-10-11 00:58 UTC (updated weekly) from backtest trades only (all coins, all history, fees included), split by the market regime at entry. A cell or family needs 30+ trades in a regime to be listed. [status] = its lifecycle status now.

**A map, not a signal.** "Made money here" is measured history, not a forecast, and is not significance-tested per regime; only APPROVED strategies send emails. Nothing here is advice.

## Which families work where (family x timeframe x regime group)

| Family | TF | BULL | BEAR | RANGE | TRANSITION |
|---|---|---|---|---|---|
| breakout | 15m | -0.15R (4207) ✗ | -0.10R (3718) ✗ | -0.15R (637) ✗ | -0.11R (1472) ✗ |
| breakout | 1h | -0.03R (6035) | -0.12R (5013) ✗ | +0.08R (394) ✓ | +0.09R (7162) ✓ |
| breakout | 30m | -0.05R (4813) | -0.04R (4098) | -0.05R (553) | -0.06R (2613) |
| breakout | 4h | +0.34R (1644) ✓ | +0.11R (1367) ✓ | -0.18R (40) ✗ | +0.17R (2665) ✓ |
| breakout | 5m | -0.04R (1833) | -0.14R (1781) ✗ | -0.11R (547) ✗ | -0.16R (982) ✗ |
| liquidity_reversal | 15m | -0.42R (678) ✗ | -0.46R (569) ✗ | -0.33R (553) ✗ | -0.26R (748) ✗ |
| liquidity_reversal | 1h | +0.20R (11) | +0.14R (10) | -0.27R (92) ✗ | -0.13R (130) ✗ |
| liquidity_reversal | 30m | -0.47R (98) ✗ | -0.45R (66) ✗ | -0.41R (120) ✗ | -0.27R (110) ✗ |
| liquidity_reversal | 5m | -0.71R (1705) ✗ | -0.68R (1415) ✗ | -0.50R (1041) ✗ | -0.34R (1301) ✗ |
| mean_reversion | 15m | - | - | -0.24R (7619) ✗ | - |
| mean_reversion | 1h | - | - | -0.14R (6247) ✗ | - |
| mean_reversion | 30m | - | - | -0.22R (7581) ✗ | - |
| mean_reversion | 4h | - | - | -0.10R (1421) ✗ | - |
| momentum | 15m | -0.19R (3487) ✗ | -0.06R (3414) | - | +0.03R (410) ✓ |
| momentum | 1h | -0.09R (1888) | -0.03R (1653) | - | -0.26R (184) ✗ |
| momentum | 30m | -0.13R (2353) ✗ | -0.06R (2537) | - | -0.09R (361) |
| momentum | 4h | +0.23R (494) ✓ | -0.01R (406) | - | +0.41R (34) ✓ |
| mtf_pullback | 15m | -0.26R (20957) ✗ | -0.20R (19304) ✗ | -0.04R (1149) | -0.09R (2755) |
| mtf_pullback | 1h | -0.11R (11831) ✗ | -0.08R (10845) | +0.01R (558) ✓ | +0.07R (711) ✓ |
| mtf_pullback | 30m | -0.19R (12130) ✗ | -0.13R (11457) ✗ | -0.02R (670) | -0.06R (1137) |
| mtf_pullback | 4h | -0.04R (1338) | -0.06R (1224) | - | +1.66R (40) ✓ |
| mtf_pullback | 5m | -0.11R (3087) ✗ | -0.12R (2800) ✗ | -0.08R (932) | -0.01R (1830) |
| smc | 15m | +0.07R (95) ✓ | -0.38R (67) ✗ | - | -1.36R (4) |
| smc | 1h | -0.30R (29) | -0.09R (55) | -0.29R (364) ✗ | +0.10R (389) ✓ |
| smc | 30m | -0.51R (145) ✗ | -0.40R (166) ✗ | -0.41R (442) ✗ | -0.16R (337) ✗ |
| trend_following | 15m | -0.24R (746) ✗ | -0.18R (765) ✗ | - | -0.31R (23) |
| trend_following | 1h | -0.19R (210) ✗ | -0.10R (196) | - | -0.26R (73) ✗ |
| trend_following | 30m | -0.24R (341) ✗ | -0.14R (417) ✗ | - | -0.12R (39) ✗ |
| trend_following | 4h | -0.14R (30) ✗ | -0.15R (26) | - | +0.19R (14) |
| trend_following | 5m | -0.54R (817) ✗ | -0.47R (716) ✗ | - | -0.35R (126) ✗ |

✓ = made money with 30+ trades · ✗ = lost -0.10R or worse · fewer than 30 trades = no mark (too few to say).

## Each regime

### STRONG_BULL
- families (all their trades in this regime): breakout -0.01R (5717); momentum -0.10R (2406); mtf_pullback -0.18R (14960); trend_following -0.38R (649); liquidity_reversal -0.59R (796)
- made money here: TRD-H4-BREAKOUT v1.0 1h +0.30R over 79 trades [BACKTESTING]; TRD-H4-BREAKOUT v1.0 30m +0.29R over 84 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.24R over 54 trades [PAPER_TRADING]; donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.24R over 54 trades [BACKTESTING]; donchian_breakout v1.0 4h +0.23R over 56 trades [PAPER_TRADING]; P01-BREAKOUT-V1 v1.0 4h (lab) +0.19R over 58 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.76R over 491 trades; PB-B-SWEEP v1.0 5m -0.62R over 42 trades; ema_9_21_cross v1.0 5m -0.48R over 329 trades; ema_9_21_cross v1.0 30m -0.42R over 58 trades; liquidity_sweep_reversal v1.0 15m -0.39R over 189 trades; bb_squeeze_breakout v1.0 15m -0.28R over 263 trades
- no trade looks like: no long setup from a strategy that fits, or price far above its averages (chasing)

### WEAK_BULL
- families (all their trades in this regime): breakout -0.04R (12780); momentum -0.13R (5773); mtf_pullback -0.19R (34214); trend_following -0.33R (1483); smc -0.36R (153); liquidity_reversal -0.66R (1581)
- made money here: P01-BREAKOUT-V3 v1.0 4h (lab) +0.56R over 82 trades [BACKTESTING]; P01-BREAKOUT-V4 v1.0 4h (lab) +0.55R over 197 trades [BACKTESTING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.45R over 127 trades [PAPER_TRADING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.41R over 177 trades [PAPER_TRADING]; P01-BREAKOUT-V1 v1.0 4h (lab) +0.40R over 213 trades [BACKTESTING]; P04-MACD-SUPERTREND-V3 v1.0 4h (lab) +0.38R over 63 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.78R over 915 trades; PB-B-SWEEP v1.0 5m -0.72R over 94 trades; liquidity_sweep_reversal v1.0 30m -0.59R over 69 trades; ema_9_21_cross v1.0 5m -0.57R over 488 trades; liquidity_sweep_reversal v1.0 15m -0.50R over 348 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.45R over 104 trades
- no trade looks like: no setup, or the higher timeframes disagree

### RANGE
- families (all their trades in this regime): mtf_pullback -0.05R (2732); breakout -0.06R (1446); mean_reversion -0.21R (21628); smc -0.37R (779); liquidity_reversal -0.44R (1588)
- made money here: TRD-H4-PULLBACK v1.0 30m +0.24R over 94 trades [FAILED]; TRD-H4-BREAKOUT v1.0 1h +0.16R over 57 trades [BACKTESTING]; TRD-H4-PULLBACK v1.0 15m +0.14R over 181 trades [FAILED]; TRD-H4-PULLBACK v1.0 1h +0.07R over 80 trades [FAILED]; TRD-H4-BREAKOUT-noT4 v1.0 1h +0.04R over 203 trades [BACKTESTING]; TRD-H4-BREAKOUT v1.0 30m +0.02R over 58 trades [BACKTESTING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.75R over 404 trades; PB-B-SWEEP v1.0 5m -0.57R over 229 trades; liquidity_sweep_reversal v1.0 15m -0.49R over 256 trades; S8-PDH-PDL-SWEEP-noSMC v1.0 30m -0.48R over 317 trades; PB-B-SWEEP-15M v1.0 15m -0.46R over 64 trades; liquidity_sweep_reversal v1.0 30m -0.41R over 116 trades
- no trade looks like: price in the middle of the range; breakouts without volume

### HIGH_VOL_RANGE
- families (all their trades in this regime): mean_reversion -0.09R (1240)
- made money here: R4-CLUC v1.0 15m (lab) +0.13R over 39 trades [FAILED]; R4-BBRSI v1.0 1h (lab) +0.05R over 76 trades [FAILED]
- lost money here: rsi2_dip_buy v1.0 15m -0.19R over 360 trades; rsi2_dip_buy v1.0 4h -0.11R over 89 trades
- no trade looks like: candles several ATRs wide: stops get hit by noise

### WEAK_BEAR
- families (all their trades in this regime): breakout -0.05R (11788); momentum -0.07R (5932); mtf_pullback -0.15R (33003); trend_following -0.24R (1507); smc -0.29R (173); liquidity_reversal -0.65R (1343)
- made money here: donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.31R over 151 trades [PAPER_TRADING]; donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.23R over 199 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.22R over 160 trades [PAPER_TRADING]; TRD-H4-PULLBACK v1.0 1h +0.19R over 151 trades [FAILED]; TRD-H4-BREAKOUT v1.0 15m +0.14R over 150 trades [FAILED]; donchian_breakout v1.0 4h +0.13R over 166 trades [PAPER_TRADING]
- lost money here: PB-B-SWEEP v1.0 5m -0.88R over 123 trades; liquidity_sweep_reversal v1.0 5m -0.77R over 672 trades; PB-B-SWEEP-15M v1.0 15m -0.74R over 33 trades; liquidity_sweep_reversal v1.0 15m -0.57R over 263 trades; ema_9_21_cross v1.0 5m -0.42R over 450 trades; liquidity_sweep_reversal v1.0 30m -0.42R over 53 trades
- no trade looks like: no setup, or the higher timeframes disagree

### STRONG_BEAR
- families (all their trades in this regime): momentum -0.01R (2040); mtf_pullback -0.15R (12508); breakout -0.15R (4113); trend_following -0.35R (567); liquidity_reversal -0.57R (566)
- made money here: P04-MACD-SUPERTREND-V2 v1.0 15m (lab) +0.09R over 359 trades [FAILED]; P04-MACD-SUPERTREND-V2 v1.0 30m (lab) +0.08R over 202 trades [FAILED]; donchian_breakout v1.0 4h +0.01R over 39 trades [PAPER_TRADING]
- lost money here: liquidity_sweep_reversal v1.0 5m -0.66R over 353 trades; PB-B-SWEEP v1.0 5m -0.55R over 39 trades; ema_9_21_cross v1.0 5m -0.53R over 266 trades; liquidity_sweep_reversal v1.0 15m -0.45R over 128 trades; P03-FIB-PULLBACK-V4 v1.0 4h (lab) -0.34R over 38 trades; P01-BREAKOUT-V2 v1.0 1h (lab) -0.31R over 124 trades
- no trade looks like: no short setup from a strategy that fits, or buying dips against the trend

### EXPANSION
- families (all their trades in this regime): breakout +0.06R (13383); mtf_pullback -0.07R (3197); momentum -0.07R (955); liquidity_reversal -0.12R (84); trend_following -0.32R (199)
- made money here: donchian_breakout-VEXIT-S4 v1.0 4h (lab) +0.23R over 391 trades [BACKTESTING]; donchian_breakout-VEXIT v1.0 4h (lab) +0.22R over 389 trades [PAPER_TRADING]; donchian_breakout-VEXIT-S4 v1.1 4h (lab) +0.22R over 280 trades [PAPER_TRADING]; TRD-H4-BREAKOUT v1.0 1h +0.21R over 314 trades [BACKTESTING]; P01-BREAKOUT-V1 v1.0 4h (lab) +0.15R over 588 trades [BACKTESTING]; donchian_breakout v1.0 4h +0.13R over 395 trades [PAPER_TRADING]
- lost money here: supertrend_flip v1.0 1h -0.36R over 33 trades; ema_9_21_cross v1.0 5m -0.35R over 126 trades; P04-MACD-SUPERTREND-V2 v1.0 1h (lab) -0.35R over 68 trades; P02-EMA-PULLBACK-V5 v1.0 1h (lab) -0.33R over 46 trades; P04-MACD-SUPERTREND-V5 v1.0 1h (lab) -0.21R over 116 trades; P02-EMA-PULLBACK-V2 v1.0 15m (lab) -0.21R over 94 trades
- no trade looks like: the move is already several ATRs old (late entry)

### COMPRESSION
- families (all their trades in this regime): mtf_pullback -0.02R (565); breakout -0.13R (513); liquidity_reversal -0.90R (34)
- made money here: TRD-H4-PULLBACK-noT4 v1.0 1h +0.22R over 81 trades [FAILED]; donchian_breakout-VEXIT-S4 v1.1 30m (lab) +0.11R over 44 trades [FAILED]; bb_squeeze_breakout v1.0 1h +0.10R over 57 trades [BACKTESTING]; TRD-H4-PULLBACK-noT4 v1.0 30m +0.05R over 97 trades [FAILED]; donchian_breakout-VEXIT-S4 v1.0 30m (lab) +0.02R over 75 trades [FAILED]; TRD-H4-PULLBACK v1.0 5m +0.01R over 33 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.90R over 34 trades; bb_squeeze_breakout v1.0 15m -0.65R over 62 trades; bb_squeeze_breakout v1.0 30m -0.22R over 63 trades; TRD-H4-PULLBACK-noT4 v1.0 5m -0.21R over 109 trades; TRD-H4-BREAKOUT-noT4 v1.0 5m -0.21R over 74 trades; TRD-H4-PULLBACK v1.0 30m -0.15R over 35 trades
- no trade looks like: before the break: wait for a close outside the range

### TRANSITION
- families (all their trades in this regime): mtf_pullback -0.01R (3105); smc -0.02R (722); breakout -0.14R (1459); liquidity_reversal -0.32R (1626)
- made money here: TRD-H4-PULLBACK v1.0 1h +0.30R over 82 trades [FAILED]; TRD-H4-BREAKOUT v1.0 30m +0.29R over 50 trades [BACKTESTING]; TRD-H4-BREAKOUT v1.0 1h +0.29R over 51 trades [BACKTESTING]; TRD-H4-BREAKOUT-noT4 v1.0 1h +0.20R over 150 trades [BACKTESTING]; S8-PDH-PDL-SWEEP v1.0 1h +0.14R over 101 trades [FAILED]; TRD-H4-PULLBACK v1.0 5m +0.10R over 270 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.62R over 175 trades; liquidity_sweep_reversal v1.0 5m -0.53R over 400 trades; PB-B-SWEEP-15M v1.0 15m -0.52R over 37 trades; TRD-H4-BREAKOUT-noT4 v1.0 5m -0.29R over 437 trades; liquidity_sweep_reversal v1.0 15m -0.29R over 245 trades; liquidity_sweep_reversal v1.0 30m -0.27R over 110 trades
- no trade looks like: the trend is changing: most trend and range strategies are unreliable here

### UNCLEAR
- families (all their trades in this regime): liquidity_reversal -0.26R (480)
- made money here: PB-B-SWEEP-LIMIT v1.0 5m +0.02R over 31 trades [FAILED]
- lost money here: PB-B-SWEEP v1.0 5m -0.54R over 127 trades; PB-B-GRADED v1.0 15m -0.22R over 146 trades; PB-B-GRADED v1.0 5m -0.19R over 140 trades
- no trade looks like: the data does not show a regime - stand aside

