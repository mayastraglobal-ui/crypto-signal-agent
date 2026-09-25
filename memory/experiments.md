# Experiments

Append-only count of every strategy version ever tested (AGENT_PROMPT.md section 11). Each new version of the same idea raises its bar by +0.02R per trade.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0001 | 2026-09-24 20:19 | trend_pullback@1.0 | mtf_pullback | 4h, 1h, 30m, 15m | In a trend confirmed by the higher timeframe, a pullback to the 20 EMA that closes strong again continues the trend. |
| EXP-0002 | 2026-09-24 20:19 | donchian_breakout@1.0 | breakout | 4h, 1h, 30m | A close beyond the 20-candle range with 1.5x volume and ADX > 20 starts a move that is worth following. |
| EXP-0003 | 2026-09-24 20:19 | rsi2_dip_buy@1.0 | mean_reversion | 4h, 1h, 30m, 15m | A sharp 1-2 candle dip (RSI(2) < 10) snaps back towards the short-term average. |
| EXP-0004 | 2026-09-24 20:19 | bb_squeeze_breakout@1.0 | breakout | 4h, 1h, 30m, 15m | After a volatility squeeze (bandwidth in its lowest 20%), a band break with volume in the higher-timeframe direction runs. |
| EXP-0005 | 2026-09-24 20:19 | macd_trend_cross@1.0 | momentum | 4h, 1h, 30m | A MACD cross below zero inside a 200-EMA trend marks the end of a pullback and momentum resuming. |
| EXP-0006 | 2026-09-24 20:19 | supertrend_flip@1.0 | trend_following | 4h, 1h, 30m | A Supertrend flip in the higher-timeframe direction with ADX > 20 catches a new leg of the trend. |
| EXP-0007 | 2026-09-24 20:19 | liquidity_sweep_reversal@1.0 | liquidity_reversal | 1h, 30m, 15m, 5m | A wick through the 20-candle low (high) that closes back inside, with volume, means the stop-hunt failed and price reverses. |
| EXP-0008 | 2026-09-24 20:19 | ema_9_21_cross@1.0 | trend_following | 1h, 30m, 15m, 5m | A 9/21 EMA cross with the 200 EMA trend and ADX > 20 catches trend moves. |
| EXP-0009 | 2026-09-24 20:19 | S5-SWEEP-MSS-FVG@1.0 | smc | 30m, 15m | With the higher timeframes aligned, a sell-side sweep followed by a market-structure shift with displacement, entered on the first retrace into a fair value gap, continues to the opposing liquidity pool. |
| EXP-0010 | 2026-09-24 20:19 | S5-SWEEP-MSS-FVG-noSMC@1.0 (control twin of S5-SWEEP-MSS-FVG) | smc | 30m, 15m | Control: a plain displacement candle in the aligned direction, same exits. S5 must beat this to keep its SMC filter. |
| EXP-0011 | 2026-09-24 20:19 | S6-OB-FVG@1.0 | smc | 15m | HTF-aligned retracements into a 4H order block inside discount (premium for shorts), triggered by a 15m CHoCH, continue in the HTF direction. |
| EXP-0012 | 2026-09-24 20:19 | S6-OB-FVG-noSMC@1.0 (control twin of S6-OB-FVG) | smc | 15m | Control: the same 15m CHoCH without the 4H order-block / discount filter. S6 must beat this. |
| EXP-0013 | 2026-09-24 20:19 | S7-SILVER-BULLET@1.0 | smc | 15m | Inside the London / New York killzones, a sweep followed by displacement and a first retrace into the new gap moves on to the next pool at least 2R away. |
| EXP-0014 | 2026-09-24 20:19 | S7-SILVER-BULLET-noSMC@1.0 (control twin of S7-SILVER-BULLET) | smc | 15m | Control: the same rules at any hour. S7 must beat this to keep its killzone filter. |
| EXP-0015 | 2026-09-24 20:19 | S8-PDH-PDL-SWEEP@1.0 | smc | 1h, 30m | A sweep of the prior-day low (high) that closes back inside the prior-day range reverses to the daily middle and then the opposite extreme. |
| EXP-0016 | 2026-09-24 20:19 | S8-PDH-PDL-SWEEP-noSMC@1.0 (control twin of S8-PDH-PDL-SWEEP) | smc | 1h, 30m | Control: the same reversal from a plain 20-candle low (high) instead of the prior-day level. S8 must beat this. |
| EXP-0017 | 2026-09-25 00:49 | S5-SWEEP-MSS-FVG-5M@1.0 | smc | 30m, 15m | Waiting for a closed 5m bar that confirms the direction (section 8) improves S5-SWEEP-MSS-FVG: fewer false entries and a better price, enough to beat the same strategy without the 5m check. |
| EXP-0018 | 2026-09-25 00:49 | S6-OB-FVG-5M@1.0 | smc | 15m | Waiting for a closed 5m bar that confirms the direction (section 8) improves S6-OB-FVG: fewer false entries and a better price, enough to beat the same strategy without the 5m check. |
| EXP-0019 | 2026-09-25 00:49 | S7-SILVER-BULLET-5M@1.0 | smc | 15m | Waiting for a closed 5m bar that confirms the direction (section 8) improves S7-SILVER-BULLET: fewer false entries and a better price, enough to beat the same strategy without the 5m check. |
| EXP-0020 | 2026-09-25 00:49 | S8-PDH-PDL-SWEEP-5M@1.0 | smc | 30m | Waiting for a closed 5m bar that confirms the direction (section 8) improves S8-PDH-PDL-SWEEP: fewer false entries and a better price, enough to beat the same strategy without the 5m check. |

### Queue: R4-BBRSI@1.0
- timestamp: 2026-09-25 18:45 UTC · source: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/berlinguyinca/BbandRsi.py · evidence: HYPOTHESIS: a community strategy idea, not tested here yet · confidence: untested idea · strategy: R4-BBRSI v1.0 · asset: research coins · timeframe: 1h, 30m · regime: RANGE, HIGH_VOL_RANGE · review: 2026-12-24
  - queue: R4 (freqtrade-strategies), 1 of 10 - the weekly research copies it into strategies_lab.yaml unchanged (added = that day) when the literature quota allows
  - card:
```yaml
- id: R4-BBRSI
  version: '1.0'
  status: FORMALIZED
  family: mean_reversion
  gate: mean_reversion
  regimes:
  - RANGE
  - HIGH_VOL_RANGE
  source: R4 freqtrade-strategies, file user_data/strategies/berlinguyinca/BbandRsi.py (commit f3340ce) - the idea
    rewritten in our building blocks; no code copied (GPL-3.0)
  source_url: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/berlinguyinca/BbandRsi.py
  evidence_class: 'UNVERIFIED_OPINION: a community strategy file, published without evidence; tested here like any
    idea'
  factory: literature
  factory_evidence: 'freqtrade-strategies berlinguyinca/BbandRsi.py: long entry as in the file (RSI < 30, close
    < lower band), plus the mirror-image short; exits kept (RSI > 70 / < 30); first target 2R instead of the file''s
    10% ROI'
  parent: 'source: [R4] freqtrade-strategies'
  hypothesis: In a range, a close below the lower Bollinger band with RSI(14) under 30 is an over-reaction that
    snaps back.
  timeframes:
  - 1h
  - 30m
  description: Buy when RSI is oversold AND price closes below the lower Bollinger band; sell the mirror image.
  params:
    rsi_n: 14
    lo: 30
    hi: 70
    bb_n: 20
    bb_k: 2
  long:
  - rsi(close,{rsi_n}) < {lo}
  - close < bb_lower(close,{bb_n},{bb_k})
  short:
  - rsi(close,{rsi_n}) > {hi}
  - close > bb_upper(close,{bb_n},{bb_k})
  exit_long:
  - rsi(close,{rsi_n}) > {hi}
  exit_short:
  - rsi(close,{rsi_n}) < {lo}
  stop:
    method: atr
    atr: 1.5
  targets:
    long:
    - 2R
    - 3R
    short:
    - 2R
    - 3R
    split:
    - 0.5
    - 0.5
  time_stop_bars: 24
  cooldown_bars: 0
  known_weaknesses: Catches falling knives when a range breaks into a trend; the original has no trend filter.
  edge:
    type: behavioural
    works_in:
    - RANGE
    - HIGH_VOL_RANGE
    who_pays: traders who panic-sell (or chase) a stretched candle at the edge of a range
    mechanism: in a range, extremes beyond the Bollinger band with an extreme RSI tend to revert to the mean
    fails_when: 'a range breaks into a trend: the band keeps being walked and every entry is early'
    kill_rule: unseen-data average below 0R, or it fails the costs +50% test
  changelog:
  - '1.0: rewritten from freqtrade-strategies BbandRsi.py (R4) - long entry as in the file (RSI < 30, close < lower
    band), plus the mirror-image short; exits kept (RSI > 70 / < 30); first target 2R instead of the file''s 10%
    ROI'
```

### Queue: R4-CLUC@1.0
- timestamp: 2026-09-25 18:45 UTC · source: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/berlinguyinca/ClucMay72018.py · evidence: HYPOTHESIS: a community strategy idea, not tested here yet · confidence: untested idea · strategy: R4-CLUC v1.0 · asset: research coins · timeframe: 30m, 15m · regime: RANGE, HIGH_VOL_RANGE · review: 2026-12-24
  - queue: R4 (freqtrade-strategies), 2 of 10 - the weekly research copies it into strategies_lab.yaml unchanged (added = that day) when the literature quota allows
  - card:
```yaml
- id: R4-CLUC
  version: '1.0'
  status: FORMALIZED
  family: mean_reversion
  gate: mean_reversion
  regimes:
  - RANGE
  - HIGH_VOL_RANGE
  source: R4 freqtrade-strategies, file user_data/strategies/berlinguyinca/ClucMay72018.py (commit f3340ce) - the
    idea rewritten in our building blocks; no code copied (GPL-3.0)
  source_url: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/berlinguyinca/ClucMay72018.py
  evidence_class: 'UNVERIFIED_OPINION: a community strategy file, published without evidence; tested here like any
    idea'
  factory: literature
  factory_evidence: 'freqtrade-strategies berlinguyinca/ClucMay72018.py: long entry as in the file (its ''ema100''
    column is really an EMA 50); mirror-image short; exit at the band''s middle kept; first target 2R'
  parent: 'source: [R4] freqtrade-strategies'
  hypothesis: A close 1.5% below the lower Bollinger band, under the 50 EMA and without a 20x volume spike, is a
    temporary over-extension that returns to the band's middle.
  timeframes:
  - 30m
  - 15m
  description: 'Buy a deep dip: close 1.5% below the lower Bollinger band while under the 50 EMA, volume not a blow-off.'
  params:
    ema_n: 50
    bb_n: 20
    bb_k: 2
    depth: 0.985
    vol_x: 20
  long:
  - close < ema(close,{ema_n})
  - close < bb_lower(close,{bb_n},{bb_k}) * {depth}
  - volume < prev(vol_sma(30)) * {vol_x}
  short:
  - close > ema(close,{ema_n})
  - close > bb_upper(close,{bb_n},{bb_k}) * (2 - {depth})
  - volume < prev(vol_sma(30)) * {vol_x}
  exit_long:
  - close > bb_mid(close,{bb_n})
  exit_short:
  - close < bb_mid(close,{bb_n})
  stop:
    method: atr
    atr: 1.5
  targets:
    long:
    - 2R
    - 3R
    short:
    - 2R
    - 3R
    split:
    - 0.5
    - 0.5
  time_stop_bars: 24
  cooldown_bars: 0
  known_weaknesses: Built for 5m altcoin dips; a strong trend can keep closing below the band.
  edge:
    type: behavioural
    works_in:
    - RANGE
    - HIGH_VOL_RANGE
    who_pays: sellers who dump into an already stretched move without a real news shock (no volume blow-off)
    mechanism: an over-extension far outside the Bollinger band tends to return to the band's middle
    fails_when: news-driven trends and liquidation cascades, where the stretch keeps growing
    kill_rule: unseen-data average below 0R, or it fails the costs +50% test
  changelog:
  - '1.0: rewritten from freqtrade-strategies ClucMay72018.py (R4) - long entry as in the file (its ''ema100'' column
    is really an EMA 50); mirror-image short; exit at the band''s middle kept; first target 2R'
```

### Queue: R4-HLHB@1.0
- timestamp: 2026-09-25 18:45 UTC · source: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/hlhb.py · evidence: HYPOTHESIS: a community strategy idea, not tested here yet · confidence: untested idea · strategy: R4-HLHB v1.0 · asset: research coins · timeframe: 4h, 1h · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - queue: R4 (freqtrade-strategies), 3 of 10 - the weekly research copies it into strategies_lab.yaml unchanged (added = that day) when the literature quota allows
  - card:
```yaml
- id: R4-HLHB
  version: '1.0'
  status: FORMALIZED
  family: trend_following
  gate: trend
  regimes:
  - STRONG_BULL
  - WEAK_BULL
  - STRONG_BEAR
  - WEAK_BEAR
  source: R4 freqtrade-strategies, file user_data/strategies/hlhb.py (commit f3340ce) - the idea rewritten in our
    building blocks; no code copied (GPL-3.0)
  source_url: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/hlhb.py
  evidence_class: 'UNVERIFIED_OPINION: a community strategy file, published without evidence; tested here like any
    idea'
  factory: literature
  factory_evidence: 'freqtrade-strategies hlhb.py: entries as in the file (RSI on the high-low midpoint, 4H as in
    the file); its mirror-image exits are left to the stop, targets and time stop; first target 2R'
  parent: 'source: [R4] freqtrade-strategies'
  hypothesis: When a fast EMA cross and an RSI cross of 50 happen together with ADX above 25, a new trend leg starts.
  timeframes:
  - 4h
  - 1h
  description: 'The ''HLHB'' system: EMA 5 crosses EMA 10 while RSI(10) crosses 50 and ADX is above 25.'
  params:
    fast: 5
    slow: 10
    rsi_n: 10
    adx_min: 25
  long:
  - cross_up(ema(close,{fast}), ema(close,{slow}))
  - cross_up(rsi((high+low)/2,{rsi_n}), 50)
  - adx(14) > {adx_min}
  short:
  - cross_down(ema(close,{fast}), ema(close,{slow}))
  - cross_down(rsi((high+low)/2,{rsi_n}), 50)
  - adx(14) > {adx_min}
  stop:
    method: atr
    atr: 2.0
  targets:
    long:
    - 2R
    - 3R
    short:
    - 2R
    - 3R
    split:
    - 0.5
    - 0.5
  time_stop_bars: 30
  cooldown_bars: 0
  known_weaknesses: Two crosses on the same candle are rare - few trades; whipsaws when ADX is high but fading.
  edge:
    type: behavioural
    works_in:
    - STRONG_BULL
    - WEAK_BULL
    - STRONG_BEAR
    - WEAK_BEAR
    who_pays: traders who fade the start of a move that momentum and trend strength already confirm
    mechanism: trends persist once momentum (RSI 50) and direction (EMA cross) turn together with ADX > 25
    fails_when: choppy markets where the EMAs cross back and forth
    kill_rule: unseen-data average below 0R, or walk-forward fails
  changelog:
  - '1.0: rewritten from freqtrade-strategies hlhb.py (R4) - entries as in the file (RSI on the high-low midpoint,
    4H as in the file); its mirror-image exits are left to the stop, targets and time stop; first target 2R'
```

### Queue: R4-AOMACD@1.0
- timestamp: 2026-09-25 18:45 UTC · source: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/berlinguyinca/AwesomeMacd.py · evidence: HYPOTHESIS: a community strategy idea, not tested here yet · confidence: untested idea · strategy: R4-AOMACD v1.0 · asset: research coins · timeframe: 1h, 30m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - queue: R4 (freqtrade-strategies), 4 of 10 - the weekly research copies it into strategies_lab.yaml unchanged (added = that day) when the literature quota allows
  - card:
```yaml
- id: R4-AOMACD
  version: '1.0'
  status: FORMALIZED
  family: momentum
  gate: trend
  regimes:
  - STRONG_BULL
  - WEAK_BULL
  - STRONG_BEAR
  - WEAK_BEAR
  source: R4 freqtrade-strategies, file user_data/strategies/berlinguyinca/AwesomeMacd.py (commit f3340ce) - the
    idea rewritten in our building blocks; no code copied (GPL-3.0)
  source_url: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/berlinguyinca/AwesomeMacd.py
  evidence_class: 'UNVERIFIED_OPINION: a community strategy file, published without evidence; tested here like any
    idea'
  factory: literature
  factory_evidence: 'freqtrade-strategies berlinguyinca/AwesomeMacd.py: entry as in the file (AO = SMA5 - SMA34
    of the high-low midpoint); mirror-image short; first target 2R'
  parent: 'source: [R4] freqtrade-strategies'
  hypothesis: When the Awesome Oscillator turns positive while MACD is already above zero, momentum resumes in the
    trend.
  timeframes:
  - 1h
  - 30m
  description: MACD above zero and the Awesome Oscillator crossing above zero.
  params:
    ao_fast: 5
    ao_slow: 34
  long:
  - macd_line(close) > 0
  - cross_up(sma((high+low)/2,{ao_fast}) - sma((high+low)/2,{ao_slow}), 0)
  short:
  - macd_line(close) < 0
  - cross_down(sma((high+low)/2,{ao_fast}) - sma((high+low)/2,{ao_slow}), 0)
  stop:
    method: atr
    atr: 1.5
  targets:
    long:
    - 2R
    - 3R
    short:
    - 2R
    - 3R
    split:
    - 0.5
    - 0.5
  time_stop_bars: 24
  cooldown_bars: 0
  known_weaknesses: Two lagging momentum indicators - late entries after the move is under way.
  edge:
    type: behavioural
    works_in:
    - STRONG_BULL
    - WEAK_BULL
    - STRONG_BEAR
    - WEAK_BEAR
    who_pays: late sellers who keep fading a trend whose momentum is turning back up
    mechanism: 'momentum is persistent: a zero cross of the Awesome Oscillator inside a positive MACD marks a new
      push'
    fails_when: ranges, where both oscillators hover around zero
    kill_rule: unseen-data average below 0R, or walk-forward fails
  changelog:
  - '1.0: rewritten from freqtrade-strategies AwesomeMacd.py (R4) - entry as in the file (AO = SMA5 - SMA34 of the
    high-low midpoint); mirror-image short; first target 2R'
```

### Queue: R4-VOLSYS@1.0
- timestamp: 2026-09-25 18:45 UTC · source: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/futures/VolatilitySystem.py · evidence: HYPOTHESIS: a community strategy idea, not tested here yet · confidence: untested idea · strategy: R4-VOLSYS v1.0 · asset: research coins · timeframe: 4h, 1h · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-24
  - queue: R4 (freqtrade-strategies), 5 of 10 - the weekly research copies it into strategies_lab.yaml unchanged (added = that day) when the literature quota allows
  - card:
```yaml
- id: R4-VOLSYS
  version: '1.0'
  status: FORMALIZED
  family: breakout
  gate: trend
  regimes:
  - STRONG_BULL
  - WEAK_BULL
  - STRONG_BEAR
  - WEAK_BEAR
  - EXPANSION
  source: R4 freqtrade-strategies, file user_data/strategies/futures/VolatilitySystem.py (commit f3340ce) - the
    idea rewritten in our building blocks; no code copied (GPL-3.0)
  source_url: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/futures/VolatilitySystem.py
  evidence_class: 'UNVERIFIED_OPINION: a community strategy file, published without evidence; tested here like any
    idea'
  factory: literature
  factory_evidence: 'freqtrade-strategies futures/VolatilitySystem.py: the file resamples to 3x the timeframe; here
    the same rule runs on 4H and 1H (close change > 2x the previous ATR, long and short); its stop-and-reverse exits
    are left to our stop and targets; first target 2R'
  parent: 'source: [R4] freqtrade-strategies'
  hypothesis: A single close-to-close move larger than 2x the previous ATR(14) marks the start of a directional
    move.
  timeframes:
  - 4h
  - 1h
  description: 'Volatility system: a candle that moves more than twice the previous ATR starts a move.'
  params:
    atr_x: 2.0
  long:
  - close - prev(close) > prev(atr(14)) * {atr_x}
  short:
  - prev(close) - close > prev(atr(14)) * {atr_x}
  stop:
    method: atr
    atr: 2.0
  targets:
    long:
    - 2R
    - 3R
    short:
    - 2R
    - 3R
    split:
    - 0.5
    - 0.5
  time_stop_bars: 20
  cooldown_bars: 0
  known_weaknesses: Enters after a big candle - buys highs; exhaustion candles look the same.
  edge:
    type: forced_flow
    works_in:
    - STRONG_BULL
    - WEAK_BULL
    - STRONG_BEAR
    - WEAK_BEAR
    - EXPANSION
    who_pays: traders stopped out or liquidated by the large move, whose forced orders keep pushing price
    mechanism: a volatility shock triggers stops and liquidations that continue the move for a while
    fails_when: one-candle spikes that reverse at once (exhaustion) and quiet ranges
    kill_rule: unseen-data average below 0R, or it fails the costs +50% test
  changelog:
  - '1.0: rewritten from freqtrade-strategies VolatilitySystem.py (R4) - the file resamples to 3x the timeframe;
    here the same rule runs on 4H and 1H (close change > 2x the previous ATR, long and short); its stop-and-reverse
    exits are left to our stop and targets; first target 2R'
```

### Queue: R4-EMAOBV@1.0
- timestamp: 2026-09-25 18:45 UTC · source: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/futures/TrendFollowingStrategy.py · evidence: HYPOTHESIS: a community strategy idea, not tested here yet · confidence: untested idea · strategy: R4-EMAOBV v1.0 · asset: research coins · timeframe: 1h, 30m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - queue: R4 (freqtrade-strategies), 6 of 10 - the weekly research copies it into strategies_lab.yaml unchanged (added = that day) when the literature quota allows
  - card:
```yaml
- id: R4-EMAOBV
  version: '1.0'
  status: FORMALIZED
  family: trend_following
  gate: trend
  regimes:
  - STRONG_BULL
  - WEAK_BULL
  - STRONG_BEAR
  - WEAK_BEAR
  source: R4 freqtrade-strategies, file user_data/strategies/futures/TrendFollowingStrategy.py (commit f3340ce)
    - the idea rewritten in our building blocks; no code copied (GPL-3.0)
  source_url: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/futures/TrendFollowingStrategy.py
  evidence_class: 'UNVERIFIED_OPINION: a community strategy file, published without evidence; tested here like any
    idea'
  factory: literature
  factory_evidence: 'freqtrade-strategies futures/TrendFollowingStrategy.py: entries as in the file (long and short);
    its cross-back exits are left to our stop and targets; the file runs on 5m, here 1H / 30M; first target 2R'
  parent: 'source: [R4] freqtrade-strategies'
  hypothesis: A close crossing the 20 EMA with rising on-balance volume starts a trend move backed by volume.
  timeframes:
  - 1h
  - 30m
  description: Close crosses the 20 EMA with on-balance volume rising.
  params:
    ema_n: 20
  long:
  - cross_up(close, ema(close,{ema_n}))
  - obv > prev(obv)
  short:
  - cross_down(close, ema(close,{ema_n}))
  - obv < prev(obv)
  stop:
    method: atr
    atr: 1.5
  targets:
    long:
    - 2R
    - 3R
    short:
    - 2R
    - 3R
    split:
    - 0.5
    - 0.5
  time_stop_bars: 24
  cooldown_bars: 0
  known_weaknesses: The 20 EMA is crossed often in ranges; volume confirmation from one candle is weak.
  edge:
    type: behavioural
    works_in:
    - STRONG_BULL
    - WEAK_BULL
    - STRONG_BEAR
    - WEAK_BEAR
    who_pays: traders on the wrong side of a trend change that volume already confirms
    mechanism: price crossing its short average with rising volume flow tends to start a trend leg
    fails_when: ranges around the 20 EMA (many crosses, no follow-through)
    kill_rule: unseen-data average below 0R, or walk-forward fails
  changelog:
  - '1.0: rewritten from freqtrade-strategies TrendFollowingStrategy.py (R4) - entries as in the file (long and
    short); its cross-back exits are left to our stop and targets; the file runs on 5m, here 1H / 30M; first target
    2R'
```

### Queue: R4-SUPER3@1.0
- timestamp: 2026-09-25 18:45 UTC · source: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/Supertrend.py · evidence: HYPOTHESIS: a community strategy idea, not tested here yet · confidence: untested idea · strategy: R4-SUPER3 v1.0 · asset: research coins · timeframe: 1h, 30m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - queue: R4 (freqtrade-strategies), 7 of 10 - the weekly research copies it into strategies_lab.yaml unchanged (added = that day) when the literature quota allows
  - card:
```yaml
- id: R4-SUPER3
  version: '1.0'
  status: FORMALIZED
  family: trend_following
  gate: trend
  regimes:
  - STRONG_BULL
  - WEAK_BULL
  - STRONG_BEAR
  - WEAK_BEAR
  source: R4 freqtrade-strategies, file user_data/strategies/Supertrend.py (commit f3340ce) - the idea rewritten
    in our building blocks; no code copied (GPL-3.0)
  source_url: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/Supertrend.py
  evidence_class: 'UNVERIFIED_OPINION: a community strategy file, published without evidence; tested here like any
    idea'
  factory: literature
  factory_evidence: 'freqtrade-strategies Supertrend.py: the buy settings of the file (8/4, 9/7, 8/1); an entry
    needs the fastest one to have JUST flipped (the file enters on the state); mirror-image short; first target
    2R'
  parent: 'source: [R4] freqtrade-strategies'
  hypothesis: When three Supertrends with different settings agree, the trend is established; entering when the
    fastest one flips back catches the next leg.
  timeframes:
  - 1h
  - 30m
  description: Three Supertrends (different settings) all point the same way, and the fastest one just flipped.
  params:
    p1: 8
    m1: 4
    p2: 9
    m2: 7
    p3: 8
    m3: 1
  long:
  - supertrend_dir({p1},{m1}) == 1
  - supertrend_dir({p2},{m2}) == 1
  - supertrend_dir({p3},{m3}) == 1
  - prev(supertrend_dir({p3},{m3})) == -1
  short:
  - supertrend_dir({p1},{m1}) == -1
  - supertrend_dir({p2},{m2}) == -1
  - supertrend_dir({p3},{m3}) == -1
  - prev(supertrend_dir({p3},{m3})) == 1
  stop:
    method: atr
    atr: 2.0
  targets:
    long:
    - 2R
    - 3R
    short:
    - 2R
    - 3R
    split:
    - 0.5
    - 0.5
  time_stop_bars: 30
  cooldown_bars: 0
  known_weaknesses: Its settings came from the author's hyperopt (over-fitting risk); all three lag at turning points.
  edge:
    type: behavioural
    works_in:
    - STRONG_BULL
    - WEAK_BULL
    - STRONG_BEAR
    - WEAK_BEAR
    who_pays: counter-trend traders who bet on the end of a trend that three trend filters still confirm
    mechanism: trends persist; a short pullback that flips only the fastest Supertrend usually resumes
    fails_when: ranges and sharp V-reversals
    kill_rule: unseen-data average below 0R, or the ±20% test fails (sign of over-fitted settings)
  changelog:
  - '1.0: rewritten from freqtrade-strategies Supertrend.py (R4) - the buy settings of the file (8/4, 9/7, 8/1);
    an entry needs the fastest one to have JUST flipped (the file enters on the state); mirror-image short; first
    target 2R'
```

### Queue: R4-S001@1.0
- timestamp: 2026-09-25 18:45 UTC · source: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/Strategy001.py · evidence: HYPOTHESIS: a community strategy idea, not tested here yet · confidence: untested idea · strategy: R4-S001 v1.0 · asset: research coins · timeframe: 1h, 30m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - queue: R4 (freqtrade-strategies), 8 of 10 - the weekly research copies it into strategies_lab.yaml unchanged (added = that day) when the literature quota allows
  - card:
```yaml
- id: R4-S001
  version: '1.0'
  status: FORMALIZED
  family: trend_following
  gate: trend
  regimes:
  - STRONG_BULL
  - WEAK_BULL
  - STRONG_BEAR
  - WEAK_BEAR
  source: R4 freqtrade-strategies, file user_data/strategies/Strategy001.py (commit f3340ce) - the idea rewritten
    in our building blocks; no code copied (GPL-3.0)
  source_url: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/Strategy001.py
  evidence_class: 'UNVERIFIED_OPINION: a community strategy file, published without evidence; tested here like any
    idea'
  factory: literature
  factory_evidence: 'freqtrade-strategies Strategy001.py: the Heikin-Ashi close is the candle''s OHLC average, the
    Heikin-Ashi green bar is approximated by a green candle (the HA open has no building block); mirror-image short;
    first target 2R'
  parent: 'source: [R4] freqtrade-strategies'
  hypothesis: A 20/50 EMA cross confirmed by a strong candle above the 20 EMA starts a trend leg.
  timeframes:
  - 1h
  - 30m
  description: EMA 20 crosses above EMA 50, with a green candle closing above EMA 20 (Heikin-Ashi close approximated).
  params:
    fast: 20
    slow: 50
  long:
  - cross_up(ema(close,{fast}), ema(close,{slow}))
  - (open + high + low + close) / 4 > ema(close,{fast})
  - close > open
  short:
  - cross_down(ema(close,{fast}), ema(close,{slow}))
  - (open + high + low + close) / 4 < ema(close,{fast})
  - close < open
  stop:
    method: atr
    atr: 1.5
  targets:
    long:
    - 2R
    - 3R
    short:
    - 2R
    - 3R
    split:
    - 0.5
    - 0.5
  time_stop_bars: 30
  cooldown_bars: 0
  known_weaknesses: Moving-average crosses are late and whipsaw in ranges.
  edge:
    type: behavioural
    works_in:
    - STRONG_BULL
    - WEAK_BULL
    - STRONG_BEAR
    - WEAK_BEAR
    who_pays: traders who keep fading a new trend after the averages have turned
    mechanism: trend persistence after a medium-term moving-average cross
    fails_when: ranges (repeated crosses) and late crosses at the end of a move
    kill_rule: unseen-data average below 0R, or walk-forward fails
  changelog:
  - '1.0: rewritten from freqtrade-strategies Strategy001.py (R4) - the Heikin-Ashi close is the candle''s OHLC
    average, the Heikin-Ashi green bar is approximated by a green candle (the HA open has no building block); mirror-image
    short; first target 2R'
```

### Queue: R4-ADXSMA@1.0
- timestamp: 2026-09-25 18:45 UTC · source: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/berlinguyinca/AdxSmas.py · evidence: HYPOTHESIS: a community strategy idea, not tested here yet · confidence: untested idea · strategy: R4-ADXSMA v1.0 · asset: research coins · timeframe: 1h, 30m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-24
  - queue: R4 (freqtrade-strategies), 9 of 10 - the weekly research copies it into strategies_lab.yaml unchanged (added = that day) when the literature quota allows
  - card:
```yaml
- id: R4-ADXSMA
  version: '1.0'
  status: FORMALIZED
  family: trend_following
  gate: trend
  regimes:
  - STRONG_BULL
  - WEAK_BULL
  - STRONG_BEAR
  - WEAK_BEAR
  source: R4 freqtrade-strategies, file user_data/strategies/berlinguyinca/AdxSmas.py (commit f3340ce) - the idea
    rewritten in our building blocks; no code copied (GPL-3.0)
  source_url: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/berlinguyinca/AdxSmas.py
  evidence_class: 'UNVERIFIED_OPINION: a community strategy file, published without evidence; tested here like any
    idea'
  factory: literature
  factory_evidence: 'freqtrade-strategies berlinguyinca/AdxSmas.py: entry as in the file (1H as in the file); ADX
    alone does not give the direction, so the engine''s trend gate decides it; its exits are left to our stop and
    targets; first target 2R'
  parent: 'source: [R4] freqtrade-strategies'
  hypothesis: A very fast SMA cross while ADX shows a strong trend catches the next push of that trend.
  timeframes:
  - 1h
  - 30m
  description: SMA 3 crosses SMA 6 while ADX is above 25.
  params:
    fast: 3
    slow: 6
    adx_min: 25
  long:
  - adx(14) > {adx_min}
  - cross_up(sma(close,{fast}), sma(close,{slow}))
  short:
  - adx(14) > {adx_min}
  - cross_down(sma(close,{fast}), sma(close,{slow}))
  stop:
    method: atr
    atr: 1.5
  targets:
    long:
    - 2R
    - 3R
    short:
    - 2R
    - 3R
    split:
    - 0.5
    - 0.5
  time_stop_bars: 20
  cooldown_bars: 0
  known_weaknesses: SMA 3/6 crosses are very frequent; ADX says strong but not which way.
  edge:
    type: behavioural
    works_in:
    - STRONG_BULL
    - WEAK_BULL
    - STRONG_BEAR
    - WEAK_BEAR
    who_pays: short-term faders of a strong trend (ADX > 25) when price turns back its way
    mechanism: in strong trends, a short-term cross in the trend's direction continues the move
    fails_when: ADX high but falling (trend ending) and ranges
    kill_rule: unseen-data average below 0R, or it fails the costs +50% test
  changelog:
  - '1.0: rewritten from freqtrade-strategies AdxSmas.py (R4) - entry as in the file (1H as in the file); ADX alone
    does not give the direction, so the engine''s trend gate decides it; its exits are left to our stop and targets;
    first target 2R'
```

### Queue: R4-SIMPLE@1.0
- timestamp: 2026-09-25 18:45 UTC · source: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/berlinguyinca/Simple.py · evidence: HYPOTHESIS: a community strategy idea, not tested here yet · confidence: untested idea · strategy: R4-SIMPLE v1.0 · asset: research coins · timeframe: 30m, 15m · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-24
  - queue: R4 (freqtrade-strategies), 10 of 10 - the weekly research copies it into strategies_lab.yaml unchanged (added = that day) when the literature quota allows
  - card:
```yaml
- id: R4-SIMPLE
  version: '1.0'
  status: FORMALIZED
  family: momentum
  gate: trend
  regimes:
  - STRONG_BULL
  - WEAK_BULL
  - STRONG_BEAR
  - WEAK_BEAR
  - EXPANSION
  source: R4 freqtrade-strategies, file user_data/strategies/berlinguyinca/Simple.py (commit f3340ce) - the idea
    rewritten in our building blocks; no code copied (GPL-3.0)
  source_url: https://github.com/freqtrade/freqtrade-strategies/blob/f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/berlinguyinca/Simple.py
  evidence_class: 'UNVERIFIED_OPINION: a community strategy file, published without evidence; tested here like any
    idea'
  factory: literature
  factory_evidence: 'freqtrade-strategies berlinguyinca/Simple.py: entry as in the file (Bollinger 12 / 2 as in
    the file); mirror-image short; its exit is left to our stop and targets; the file runs on 5m, here 30M / 15M;
    first target 2R'
  parent: 'source: [R4] freqtrade-strategies'
  hypothesis: Strong momentum (RSI > 70) with MACD above its signal and an expanding upper band continues for a
    while.
  timeframes:
  - 30m
  - 15m
  description: '''Simple'': MACD above zero and its signal, the upper Bollinger band rising, RSI above 70.'
  params:
    rsi_hi: 70
    rsi_lo: 30
    bb_n: 12
    bb_k: 2
  long:
  - macd_line(close) > 0
  - macd_line(close) > macd_signal(close)
  - bb_upper(close,{bb_n},{bb_k}) > prev(bb_upper(close,{bb_n},{bb_k}))
  - rsi(close,14) > {rsi_hi}
  short:
  - macd_line(close) < 0
  - macd_line(close) < macd_signal(close)
  - bb_lower(close,{bb_n},{bb_k}) < prev(bb_lower(close,{bb_n},{bb_k}))
  - rsi(close,14) < {rsi_lo}
  stop:
    method: atr
    atr: 1.5
  targets:
    long:
    - 2R
    - 3R
    short:
    - 2R
    - 3R
    split:
    - 0.5
    - 0.5
  time_stop_bars: 16
  cooldown_bars: 0
  known_weaknesses: Buys overbought markets - fails badly at blow-off tops.
  edge:
    type: behavioural
    works_in:
    - STRONG_BULL
    - WEAK_BULL
    - STRONG_BEAR
    - WEAK_BEAR
    - EXPANSION
    who_pays: traders who short 'overbought' markets too early in a strong move
    mechanism: 'momentum persistence: strong moves with expanding volatility continue in the short run'
    fails_when: blow-off tops and ranges where RSI > 70 marks the end of the move
    kill_rule: unseen-data average below 0R, or it fails the costs +50% test
  changelog:
  - '1.0: rewritten from freqtrade-strategies Simple.py (R4) - entry as in the file (Bollinger 12 / 2 as in the
    file); mirror-image short; its exit is left to our stop and targets; the file runs on 5m, here 30M / 15M; first
    target 2R'
```
