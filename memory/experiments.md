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

### Hypothesis: cost share filter for mean reversion
- timestamp: 2026-09-26 06:40 UTC · source: Claude weekly research 2026-09-26 (loss case study; https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md) · evidence: HYPOTHESIS: derived from the engine's fees_slippage tag (systematic in 3 tests: rsi2_dip_buy 1h, 30m, 15m) · confidence: low · strategy: rsi2_dip_buy, R4-BBRSI · asset: research coins · timeframe: 15m, 30m, 1h · regime: RANGE, HIGH_VOL_RANGE · review: 2026-12-25
  - hypothesis: mean-reversion trades lose most where the stop is narrow compared with the round-trip cost; keeping only entries where the ATR stop is wide compared with price would lift the average trade.
  - how to test: a one-change version of a mean-reversion card with an extra entry rule on the stop width (ATR as a share of price above a threshold), compared with its parent on the same period; judge on unseen data and the costs +50% test.
  - blocked on: check that the building blocks can express ATR as a share of price before writing the card; if not, it waits for the operator.
  - stop if: the filtered version keeps fewer than 30 unseen-data trades, or it is not better than its parent after costs.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0021 | 2026-09-27 00:50 | R4-BBRSI@1.0 | mean_reversion | 1h, 30m | In a range, a close below the lower Bollinger band with RSI(14) under 30 is an over-reaction that snaps back. |
| EXP-0022 | 2026-09-27 00:50 | donchian_breakout-VEXIT@1.0 | breakout | 4h, 1h, 30m | One change to donchian_breakout@1.0: targets 2R / 3R (50 / 50) instead of a first target below 2R. It should keep the edge of donchian_breakout@1.0 and remove part of its losses; tested because it was the strongest BACKTESTING cell this week. |

### Hypothesis: taker-flow filter for mean reversion
- timestamp: 2026-09-27 02:00 UTC · source: Claude weekly research 2026-09-27 (loss case study; https://arxiv.org/abs/2608.21888) · evidence: HYPOTHESIS: derived from a preprint finding (reversal concentrates after aggressive taker flow) and our failed oscillator cards (R4-BBRSI 1h 948 trades -0.29R, 30m 1206 trades -0.32R; rsi2_dip_buy 15m 1736 trades -0.30R) · confidence: low · strategy: R4-BBRSI, R4-CLUC · asset: research coins · timeframe: 1h · regime: RANGE, HIGH_VOL_RANGE · review: 2026-12-26
  - hypothesis: a mean-reversion entry only pays for its costs when the move it fades was driven by unusually one-sided aggressive (taker) flow; entries after quiet drifts are the ones that lose.
  - how to test: a market_structure card, one change to a mean-reversion parent on 1h: add 'taker_ratio < X' to the long entry (aggressive selling) and 'taker_ratio > 1/X' to the short entry; compare with the parent on the same period; judge on unseen data and the costs +50% test.
  - blocked on: the futures data has only about 755 hours of history (fact sheet), so a 1h test would have few trades; wait until the history is long enough for 30+ unseen-data trades, or the operator backfills it.
  - stop if: fewer than 30 unseen-data trades, or not better than the parent after costs.

### Feedback: R4-BBRSI@1.0
- timestamp: 2026-09-27 15:40 UTC · source: Claude daily review 2026-09-27 · evidence: BACKTEST_EVIDENCE: 2 cells, 2154 trades (948 + 1206) · confidence: high · strategy: R4-BBRSI@1.0 · asset: research coins · timeframe: 1h, 30m · regime: RANGE, HIGH_VOL_RANGE · review: 2026-12-26
- parent: source: [R4] freqtrade-strategies
- hypothesis: In a range, a close below the lower Bollinger band with RSI(14) under 30 is an over-reaction that snaps back.
- result: BACKTEST 1h FAILED 948 trades -0.287R (unseen -0.265R), profit factor 0.63, max drawdown 273.5R; 30m FAILED 1206 trades -0.320R (unseen -0.294R), profit factor 0.60, max drawdown 390.4R; the diagnosis finds no systematic loss tag in either cell
- teaches: the hypothesis did not hold. Both cells lose about the same in the train part and the unseen part, and no single failure tag explains the losses, so there is no one change that fixes it; a band-plus-RSI entry in a range has no edge after our costs.
- next: stop this line

### Feedback: donchian_breakout-VEXIT@1.0
- timestamp: 2026-09-27 15:40 UTC · source: Claude daily review 2026-09-27 · evidence: BACKTEST_EVIDENCE: 3 cells, 4076 trades (803 + 2223 + 1050) · confidence: medium · strategy: donchian_breakout-VEXIT@1.0 · asset: research coins · timeframe: 4h, 1h, 30m · regime: STRONG_BULL, WEAK_BULL · review: 2026-12-26
- parent: result: donchian_breakout@1.0 4h
- hypothesis: One change to donchian_breakout@1.0: targets 2R / 3R (50 / 50) instead of a first target below 2R. It should keep the edge of donchian_breakout@1.0 and remove part of its losses; tested because it was the strongest BACKTESTING cell this week.
- result: BACKTEST 4h BACKTESTING 803 trades +0.222R (unseen +0.275R), t 4.303, held back only by max drawdown 23.7R; 1h FAILED 2223 trades -0.037R (unseen +0.051R), profit factor 0.94; 30m FAILED 1050 trades -0.006R (unseen +0.057R), profit factor 0.99; playbook: 4h +0.38R over 166 trades in WEAK_BULL and +0.25R over 50 trades in STRONG_BULL
- teaches: the wider 2R / 3R targets kept the 4h result positive in both the train and the unseen part, but they did not rescue 1h or 30m. The edge of this breakout idea lives on the slow 4h timeframe only; the remaining blocker on 4h is the drawdown, not the average trade.
- next: stop the 1h and 30m cells of this line. On 4h the engine's two one-change children (donchian_breakout-VEXIT-S4@1.0 and donchian_breakout-VEXIT-VRVOL@1.0) are already queued and untested; wait for their results before any new 4h card. Also check that the 4h cell does not carry the higher-timeframe history bias that failed donchian_breakout@1.0 4h on 2026-09-26.

### Hypothesis: slow own-trend filter for the 4h breakout (from C01, time series momentum)
- timestamp: 2026-09-27 15:40 UTC · source: Claude daily review 2026-09-27 ([C01] https://pages.stern.nyu.edu/~lpederse/papers/TimeSeriesMomentum.pdf) · evidence: HYPOTHESIS: derived from a published finding in futures markets (58 instruments, 1985-2009) and our 4h breakout cell (donchian_breakout-VEXIT@1.0 4h, 803 trades, +0.222R) · confidence: low · strategy: donchian_breakout-VEXIT · asset: research coins · timeframe: 4h · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR · review: 2026-12-26
  - hypothesis: a 4h breakout pays more when it agrees with the coin's own slow trend. Longs only when close > shift(close,180) (the close about 30 days ago on 4h candles), shorts only when close < shift(close,180).
  - why: the paper finds that an instrument's own past return (1 to 12 months) predicts its next month in every one of 58 futures; our breakout edge exists only on the slowest timeframe we test (4h), which fits "slow trends persist".
  - how to test: a one-change version of the best 4h breakout card (a new entry rule, nothing else), compared with its parent on the same period; judge on the unseen part, the costs +50% test and the drawdown gate.
  - blocked on: the lab quota (0 cards left today) and the two untested VEXIT children; a card waits for the weekly research or a later daily review, with parent "source: [C01] Time Series Momentum (Moskowitz, Ooi, Pedersen 2012)".
  - stop if: fewer than 30 unseen-data trades, or not better than the parent after costs. The paper's horizon is months and its markets are futures from 1985-2009, so a null result on 4h crypto is a real possibility.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0023 | 2026-09-28 00:52 | donchian_breakout-VEXIT-S4@1.0 | breakout | 4h, 1h, 30m | The rule 'adx(14) > 20 / adx(14) > 20' adds nothing to donchian_breakout-VEXIT@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting). |
| EXP-0024 | 2026-09-28 00:52 | donchian_breakout-VEXIT-VRVOL@1.0 | breakout | 4h, 1h, 30m | One change to donchian_breakout-VEXIT@1.0: only when volume is at least 1.2x normal (rel_vol filter). It should keep the edge of donchian_breakout-VEXIT@1.0 and remove part of its losses; tested because it was the strongest BACKTESTING cell this week. |
| EXP-0025 | 2026-09-28 00:52 | R4-CLUC@1.0 | mean_reversion | 30m, 15m | A close 1.5% below the lower Bollinger band, under the 50 EMA and without a 20x volume spike, is a temporary over-extension that returns to the band's middle. |

### Feedback: R4-CLUC@1.0
- timestamp: 2026-09-28 15:40 UTC · source: Claude daily review 2026-09-28 · evidence: BACKTEST_EVIDENCE: 2 cells, 320 trades (85 + 235) · confidence: medium · strategy: R4-CLUC@1.0 · asset: research coins · timeframe: 15m, 30m · regime: RANGE, HIGH_VOL_RANGE · review: 2026-12-27
- parent: source: [R4] freqtrade-strategies
- hypothesis: A close 1.5% below the lower Bollinger band, under the 50 EMA and without a 20x volume spike, is a temporary over-extension that returns to the band's middle.
- result: BACKTEST 15m FAILED 85 trades -0.147R (unseen +0.317R), profit factor 0.79, max drawdown 22.0R; 30m FAILED 235 trades -0.165R (unseen -0.115R), profit factor 0.75, max drawdown 59.0R; volatility_spike is systematic in R4-CLUC@1.0|30m
- teaches: the hypothesis did not hold. It is the third range mean-reversion card from this source to fail after costs (with R4-BBRSI 1h and 30m); the positive unseen part on 15m rests on very few trades and the train part is negative, so it is not an edge.
- next: stop this line

### Feedback: donchian_breakout-VEXIT-S4@1.0
- timestamp: 2026-09-28 15:40 UTC · source: Claude daily review 2026-09-28 · evidence: BACKTEST_EVIDENCE: 3 cells, 5398 trades (1067 + 2952 + 1379) · confidence: medium · strategy: donchian_breakout-VEXIT-S4@1.0 · asset: research coins · timeframe: 4h, 1h, 30m · regime: WEAK_BULL, EXPANSION, STRONG_BULL · review: 2026-12-27
- parent: result: donchian_breakout-VEXIT@1.0 4h
- hypothesis: The rule 'adx(14) > 20 / adx(14) > 20' adds nothing to donchian_breakout-VEXIT@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting).
- result: BACKTEST 4h BACKTESTING 1067 trades +0.220R (unseen +0.235R), t 4.856, held back by max drawdown 23.7R; 1h FAILED 2952 trades -0.048R; 30m FAILED 1379 trades -0.040R. Parent 4h today: 939 trades +0.226R (unseen +0.259R), t 4.709
- teaches: the hypothesis held on 4h: without the ADX rule the card takes 1067 instead of 939 trades at almost the same average (+0.220R vs +0.226R), so the ADX rule does no measurable work. The unseen part is a little lower without it (+0.235R vs +0.259R), so the two are equal within noise, not better. The drawdown gate is still the blocker.
- next: prefer the simpler 4h card (without ADX) as the base for any later one-change test, because it has more trades for the same result; stop the 1h and 30m cells. The open question on 4h is the drawdown, not the entry filter.

### Feedback: donchian_breakout-VEXIT-VRVOL@1.0
- timestamp: 2026-09-28 15:40 UTC · source: Claude daily review 2026-09-28 · evidence: BACKTEST_EVIDENCE: 3 cells, 4706 trades (939 + 2599 + 1168) · confidence: high · strategy: donchian_breakout-VEXIT-VRVOL@1.0 · asset: research coins · timeframe: 4h, 1h, 30m · regime: WEAK_BULL, EXPANSION, STRONG_BULL · review: 2026-12-27
- parent: result: donchian_breakout-VEXIT@1.0 4h
- hypothesis: One change to donchian_breakout-VEXIT@1.0: only when volume is at least 1.2x normal (rel_vol filter). It should keep the edge of donchian_breakout-VEXIT@1.0 and remove part of its losses; tested because it was the strongest BACKTESTING cell this week.
- result: BACKTEST 4h BACKTESTING 939 trades +0.226R (unseen +0.259R), max drawdown 24.2R; 1h FAILED 2599 trades -0.054R; 30m FAILED 1168 trades -0.019R. The parent's cells today have the same trade counts and averages (4h 939 trades +0.226R, 1h 2599 trades, 30m 1168 trades)
- teaches: the 1.2x volume filter removed no trades: the parent's edge block already requires a breakout with 1.5x volume, so a weaker volume rule is redundant. The test only added one to the trials counter. Before a one-change variant is queued, check that the new rule is not already implied by an existing rule.
- next: stop this line

### Hypothesis: 1-week own-trend filter for the 4h breakout (from C02)
- timestamp: 2026-09-28 15:40 UTC · source: Claude daily review 2026-09-28 ([C02] https://www.nber.org/papers/w24877) · evidence: HYPOTHESIS: derived from a working-paper finding (Bitcoin weekly returns predict 1 to 4 weeks ahead, 2011-2018) and our 4h breakout cell (donchian_breakout-VEXIT-S4@1.0 4h, 1067 trades, +0.220R) · confidence: low · strategy: donchian_breakout-VEXIT-S4 · asset: research coins · timeframe: 4h · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2026-12-27
  - hypothesis: a 4h breakout pays more when the coin's own last week agrees with it: longs only when close > shift(close,42) (the close 7 days ago on 4h candles), shorts only when close < shift(close,42).
  - relation to the C01 hypothesis (30-day filter, queued 2026-09-27): same idea, the horizon the crypto paper found. Test at most ONE of the two first, to keep the trials counter low; this one matches the crypto evidence better.
  - how to test: a one-change version of donchian_breakout-VEXIT-S4@1.0 (the simpler 4h base, see its Feedback record), same period; judge on the unseen part, the costs +50% test and the drawdown gate.
  - stop if: fewer than 30 unseen-data trades, or not better than the parent after costs.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0026 | 2026-10-04 03:56 | donchian_breakout-VEXIT-VRVOL-S4@1.0 | breakout | 4h, 1h, 30m | The rule 'adx(14) > 20 / adx(14) > 20' adds nothing to donchian_breakout-VEXIT-VRVOL@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting). |
| EXP-0027 | 2026-10-05 00:57 | donchian_breakout-VEXIT-VRVOL-S4-S4@1.0 | breakout | 4h, 1h, 30m | The rule 'rel_vol > 1.2 / rel_vol > 1.2' adds nothing to donchian_breakout-VEXIT-VRVOL-S4@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting). |
| EXP-0028 | 2026-10-05 00:57 | donchian_breakout-VEXIT-VRVOL-S5@1.0 | breakout | 4h, 1h, 30m | The rule 'rel_vol > 1.2 / rel_vol > 1.2' adds nothing to donchian_breakout-VEXIT-VRVOL@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting). |

### Feedback: donchian_breakout-VEXIT-VRVOL-S4@1.0
- timestamp: 2026-10-05 17:15 UTC · source: Claude daily review 2026-10-05 · evidence: BACKTEST_EVIDENCE: 3 cells, 4548 trades (926 + 2549 + 1073) · confidence: high · strategy: donchian_breakout-VEXIT-VRVOL-S4@1.0 · asset: research coins · timeframe: 4h, 1h, 30m · regime: WEAK_BULL, WEAK_BEAR · review: 2027-01-03
- parent: result: donchian_breakout-VEXIT-VRVOL@1.0 4h
- hypothesis: The rule 'adx(14) > 20 / adx(14) > 20' adds nothing to donchian_breakout-VEXIT-VRVOL@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting).
- result: BACKTEST 4h BACKTESTING 926 trades +0.235R (unseen +0.213R), t 4.803, held back by max drawdown 19.0R; 1h FAILED 2549 trades -0.043R (unseen -0.015R), profit factor 0.93; 30m FAILED 1073 trades -0.090R (unseen -0.039R), profit factor 0.87. These are exactly the numbers of donchian_breakout-VEXIT-S4@1.0 in every cell (4h 926 trades +0.23R t 4.803; 1h 2549 trades; 30m 1073 trades)
- teaches: this card is a duplicate of donchian_breakout-VEXIT-S4@1.0. Its parent VRVOL was already identical to VEXIT (the 1.2x volume rule is implied by the 1.5x volume breakout), so removing ADX from VRVOL gives the same trades as removing ADX from VEXIT. The test taught nothing new and raised the trials counter (now 136 tests).
- next: stop this line

### Feedback: donchian_breakout-VEXIT-VRVOL-S4-S4@1.0
- timestamp: 2026-10-05 17:15 UTC · source: Claude daily review 2026-10-05 · evidence: BACKTEST_EVIDENCE: 3 cells, 4548 trades (926 + 2549 + 1073) · confidence: high · strategy: donchian_breakout-VEXIT-VRVOL-S4-S4@1.0 · asset: research coins · timeframe: 4h, 1h, 30m · regime: WEAK_BULL, WEAK_BEAR · review: 2027-01-03
- parent: result: donchian_breakout-VEXIT-VRVOL-S4@1.0 4h
- hypothesis: The rule 'rel_vol > 1.2 / rel_vol > 1.2' adds nothing to donchian_breakout-VEXIT-VRVOL-S4@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting).
- result: BACKTEST 4h BACKTESTING 926 trades +0.235R (unseen +0.213R), t 4.803, held back by max drawdown 19.0R; 1h FAILED 2549 trades -0.043R (unseen -0.015R), profit factor 0.93, max drawdown 175.6R; 30m FAILED 1073 trades -0.090R (unseen -0.039R), profit factor 0.87, max drawdown 116.2R. Identical to its parent and to donchian_breakout-VEXIT-S4@1.0 in every cell
- teaches: the hypothesis held in the trivial way: removing the 1.2x volume rule changed no trade, because that rule was redundant (already shown in Feedback: donchian_breakout-VEXIT-VRVOL@1.0). The card is the same strategy as donchian_breakout-VEXIT-S4@1.0 under a new name.
- next: stop this line

### Feedback: donchian_breakout-VEXIT-VRVOL-S5@1.0
- timestamp: 2026-10-05 17:15 UTC · source: Claude daily review 2026-10-05 · evidence: BACKTEST_EVIDENCE: 3 cells, 3959 trades (814 + 2236 + 909) · confidence: high · strategy: donchian_breakout-VEXIT-VRVOL-S5@1.0 · asset: research coins · timeframe: 4h, 1h, 30m · regime: WEAK_BULL, WEAK_BEAR · review: 2027-01-03
- parent: result: donchian_breakout-VEXIT-VRVOL@1.0 4h
- hypothesis: The rule 'rel_vol > 1.2 / rel_vol > 1.2' adds nothing to donchian_breakout-VEXIT-VRVOL@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting).
- result: BACKTEST 4h BACKTESTING 814 trades +0.247R (unseen +0.242R), t 4.743, held back by max drawdown 20.0R; 1h FAILED 2236 trades -0.043R (unseen -0.000R), profit factor 0.93; 30m FAILED 909 trades -0.058R (unseen -0.024R), profit factor 0.91. Identical to donchian_breakout-VEXIT@1.0 and donchian_breakout-VEXIT-VRVOL@1.0 in every cell
- teaches: removing a redundant rule gives back the grandparent card, donchian_breakout-VEXIT@1.0. Three of the engine's variant-search cards this week (VRVOL-S4, VRVOL-S4-S4, VRVOL-S5) are copies of two cards that were already tested. The 4h breakout is unchanged: positive in train and unseen parts, blocked only by the drawdown gate.
- next: stop this line. The useful next test on the 4h breakout is a real change to the base donchian_breakout-VEXIT-S4@1.0 (for example the queued 'Hypothesis: 1-week own-trend filter for the 4h breakout (from C02)'), not more rule removals in the VRVOL branch.

### Hypothesis: break-even stop for the prior-day sweep reversal (S8)
- timestamp: 2026-10-05 17:15 UTC · source: Claude daily review 2026-10-05 · evidence: HYPOTHESIS: from the engine's diagnosis of S8-PDH-PDL-SWEEP@1.0|30m (77 trades, -0.56R; half the losers were at least +0.50R in profit first) and S8-PDH-PDL-SWEEP-noSMC@1.0|30m (414 trades, -0.46R; half the losers were at least +0.60R in profit first) · confidence: low · strategy: S8-PDH-PDL-SWEEP · asset: research coins · timeframe: 30m · regime: RANGE, TRANSITION · review: 2027-01-03
  - hypothesis: v1.1: move the stop to the entry price once the trade is +0.5R in profit (one change: the exit, not the entry), because half of the losers were at least +0.50R in profit before they turned into a full loss.
  - why not a card today: both cells lose in every regime with 10+ trades, and the existing lesson says the fix for these cells is more likely in the entry than in the stop. A break-even stop cuts some losses but also cuts winners that dip back, so it may not lift a -0.46R average to above +0.10R. The 'stop_too_tight' tag is not the reason here; the MFE (best point) is.
  - how to test: a one-change version of S8-PDH-PDL-SWEEP-noSMC@1.0 (the control with more trades), 30m, same period, first target still at least 2R; judge on the unseen part and the costs +50% test.
  - stop if: the average stays below 0R, or fewer than 30 unseen-data trades.

### Hypothesis: relative-strength filter for the 4h breakout (from C03)
- timestamp: 2026-10-06 15:30 UTC · source: Claude daily review 2026-10-06 ([C03] https://www.nber.org/papers/w25882) · evidence: HYPOTHESIS: derived from a working-paper finding (1- to 4-week cross-sectional momentum among large coins, 2014-2018, before costs) and our 4h breakout cell (donchian_breakout-VEXIT-S4@1.0 4h, 968 trades, +0.24R, BACKTEST) · confidence: low · strategy: donchian_breakout-VEXIT-S4 · asset: research coins · timeframe: 4h · regime: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION · review: 2027-01-04
  - hypothesis: a 4h long breakout pays more when the coin has been stronger than BTC over the last 3 weeks: longs only when the coin's own 3-week return is above btc_ret(126) (126 candles of 4h = 21 days); shorts only when it is below.
  - why: the paper finds that coins that rose more than other coins over 1 to 4 weeks kept rising more in the next week, and only among the larger coins. btc_ret(n) is the only cross-coin building block we have, so 'stronger than BTC' is the nearest test of 'stronger than the market'.
  - relation to the queued C01 and C02 hypotheses: those filter on the coin's own trend (time-series momentum); this one filters on strength against BTC (relative momentum). Test at most ONE of the three first, to keep the trials counter low (136 tests now).
  - how to test: a lead_lag card, one change to donchian_breakout-VEXIT-S4@1.0 (a new entry rule, nothing else), same period; judge on the unseen part, the costs +50% test and the drawdown gate. The engine must also check that the coin's 3-week return can be written with the building blocks (close / shift(close,126)).
  - stop if: fewer than 30 unseen-data trades, or not better than the parent after costs. The paper uses weekly rebalancing of thousands of coins, not breakouts on a few large coins, so a null result is a real possibility.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0029 | 2026-10-07 00:58 | PB-A-PULLBACK@1.0 | mtf_pullback | 5m | In a 1H trend with a matching bias, a 15m pullback into the EMA21 / VWAP zone at a marked level that ends with a 5m rejection or engulfing candle resumes the trend. |
| EXP-0030 | 2026-10-07 00:58 | PB-A-PULLBACK-CVD@1.0 | mtf_pullback | 5m | Strategy A is better when the trigger candle's order flow agrees (aggressive buyers on a long trigger). |
| EXP-0031 | 2026-10-07 00:58 | PB-B-SWEEP@1.0 | liquidity_reversal | 5m | A sweep of a marked low (high) that closes back inside within 3 candles, confirmed by order flow or an OI flush, reverses toward VWAP and the range middle. |
| EXP-0032 | 2026-10-07 00:58 | PB-B-SWEEP-noCVD@1.0 (control twin of PB-B-SWEEP) | liquidity_reversal | 5m | Control: Strategy B confirmed only by the OI drop. PB-B-SWEEP must beat this for CVD to stay. |
| EXP-0033 | 2026-10-07 00:58 | PB-C-BREAKOUT@1.0 | breakout | 5m | A strong 5m breakout of a level after 15m compression, then a retest of the level zone with a rejection candle, continues by the range height. |
| EXP-0034 | 2026-10-07 00:58 | PB-C-BREAKOUT-noCVD@1.0 (control twin of PB-C-BREAKOUT) | breakout | 5m | Control: Strategy C without the CVD check. PB-C-BREAKOUT must beat this for CVD to stay. |
| EXP-0035 | 2026-10-07 00:58 | PB-A-PULLBACK-LDN@1.0 | mtf_pullback | 5m | Strategy A works in the London session (07:00-10:00 UTC) as well as in New York, so it gives more trades without losing its edge. |
| EXP-0036 | 2026-10-07 00:58 | PB-B-SWEEP-15M@1.0 | liquidity_reversal | 15m | Strategy B on 15m candles has wider stops, so the fees are a smaller part of each trade, and keeps its edge. |
| EXP-0037 | 2026-10-07 00:58 | PB-B-SWEEP-LIMIT@1.0 | liquidity_reversal | 5m | Strategy B loses mostly to fees (median cost 0.84R on BTC 5m); a limit entry and skipping trades whose stop is too close for the fees leave the trades that can pay. |
| EXP-0038 | 2026-10-07 00:58 | PB-C-BREAKOUT-W20@1.0 | breakout | 5m | A looser compression (the last 8 x 15m candles inside 2.0 x ATR instead of 1.2) still stores the energy for the breakout and gives Strategy C trades. |
| EXP-0039 | 2026-10-07 00:58 | PB-A-GRADED@1.0 | mtf_pullback | 5m | Strategy A's must-haves (1H trend and bias, the pullback into the EMA21 / VWAP zone at a level, the higher low intact, the trigger candle) carry the edge; the other conditions only make it stronger, so a setup with most of them is still worth a (smaller) trade. |
| EXP-0040 | 2026-10-07 00:58 | PB-A-APLUS@1.0 | mtf_pullback | 5m | Measures the A+ setups alone: if PB-A-GRADED does no better than this, its grade B trades add nothing. |
| EXP-0041 | 2026-10-07 00:58 | PB-B-GRADED@1.0 | liquidity_reversal | 5m, 15m | The sweep of a marked level and the close back inside, in a regime the playbook allows, carry the edge; the confirmations make it stronger, so a sweep with 2 of them is still worth a half-size trade. |
| EXP-0042 | 2026-10-07 00:58 | PB-B-APLUS@1.0 | liquidity_reversal | 5m, 15m | Measures the A+ sweeps alone: if PB-B-GRADED does no better than this, its grade B trades add nothing. |
| EXP-0043 | 2026-10-07 00:58 | PB-C-GRADED@1.0 | breakout | 5m | A strong breakout of a level out of a quiet box and a held retest carry the edge; the playbook's tight compression, the volume spike, the CVD, the session and its regime rule make it stronger. |
| EXP-0044 | 2026-10-07 00:58 | PB-C-APLUS@1.0 | breakout | 5m | Measures the A+ breakouts alone: if PB-C-GRADED does no better than this, its grade B trades add nothing. |
| EXP-0045 | 2026-10-07 00:58 | TRD-H4-PULLBACK@1.0 | mtf_pullback | 1h, 30m, 15m, 5m | While the 4H Donchian breakout trade is open, a pullback to the EMA20 on a faster timeframe that closes back in the trend direction is a better-priced entry into the same trend. |
| EXP-0046 | 2026-10-07 00:58 | TRD-H4-PULLBACK-noT4@1.0 (control twin of TRD-H4-PULLBACK) | mtf_pullback | 1h, 30m, 15m, 5m | Control: the pullback entry alone. TRD-H4-PULLBACK must beat it for the 4H window to count. |
| EXP-0047 | 2026-10-07 00:58 | TRD-H4-BREAKOUT@1.0 | breakout | 1h, 30m, 15m, 5m | While the 4H Donchian breakout trade is open, a new 20-candle high on a faster timeframe with volume is the trend's next leg starting. |
| EXP-0048 | 2026-10-07 00:58 | TRD-H4-BREAKOUT-noT4@1.0 (control twin of TRD-H4-BREAKOUT) | breakout | 1h, 30m, 15m, 5m | Control: the faster breakout alone. TRD-H4-BREAKOUT must beat it for the 4H window to count. |
| EXP-0049 | 2026-10-07 00:58 | donchian_breakout-VEXIT-S4@1.1 | breakout | 4h, 1h, 30m | One change to donchian_breakout-VEXIT-S4@1.0: longs only when the coin rose more than BTC over the last 126 candles (21 days on 4h), shorts only when it rose less. Coins that beat the market over 1 to 4 weeks kept beating it in the paper, among large coins; the filter should drop breakouts that go against relative strength. |

### Feedback: donchian_breakout-VEXIT-S4@1.1
- timestamp: 2026-10-07 15:30 UTC · source: Claude daily review 2026-10-07 · evidence: BACKTEST_EVIDENCE: 3 cells, 3694 trades (722 + 2049 + 923) · confidence: medium · strategy: donchian_breakout-VEXIT-S4@1.1 · asset: research coins · timeframe: 4h, 1h, 30m · regime: WEAK_BEAR, EXPANSION, STRONG_BEAR · review: 2027-01-05
- parent: source: [C03] Common Risk Factors in Cryptocurrency (Liu, Tsyvinski, Wu)
- hypothesis: One change to donchian_breakout-VEXIT-S4@1.0: longs only when the coin rose more than BTC over the last 126 candles (21 days on 4h), shorts only when it rose less. Coins that beat the market over 1 to 4 weeks kept beating it in the paper, among large coins; the filter should drop breakouts that go against relative strength.
- result: BACKTEST 4h BACKTESTING 722 trades +0.213R (unseen +0.248R), t 3.93, held back by max drawdown 17.3R; 1h FAILED 2049 trades -0.026R (unseen +0.067R); 30m BACKTESTING 923 trades +0.012R (unseen +0.083R), avg below the +0.12R bar. Parent today: 4h 1029 trades +0.220R (unseen +0.226R), t 4.758. Playbook: v1.1 4h +0.33R over 177 trades in WEAK_BEAR (parent +0.26R over 226) but -0.41R over 34 trades in STRONG_BEAR.
- teaches: the relative-strength rule removed about 30% of the 4h trades and left the average where it was (+0.213R vs +0.220R). The unseen part is a little higher (+0.248R vs +0.226R) and the drawdown a little lower (17.3R; the identical VRVOL-S4 card had 19.0R on 2026-10-05), but with fewer trades the t value fell from 4.758 to 3.93. That is equal within noise, not better. The paper's weekly cross-coin effect does not show up as a clear filter on our 4h breakouts; the drawdown gate still blocks both versions.
- next: stop this line. Tuning the 126-candle window would be curve-fitting. The queued C01 and C02 own-trend filters test a close cousin of this idea; expect a similar null result and give them low priority. The open problem on the 4h breakout is still the drawdown, so a change to the exit or the stop is the better next test there.

### Hypothesis: count identical trials once in the trials counter (from C04)
- timestamp: 2026-10-07 15:30 UTC · source: Claude daily review 2026-10-07 ([C04] https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf) · evidence: HYPOTHESIS: derived from the paper's Appendix 3 (implied number of independent trials) and our trials counter (210 tests, PAPER_TRADING bar t >= 3.49 on 2026-10-07) · confidence: low · strategy: all (engine/trials.py) · asset: - · timeframe: - · regime: - · review: 2027-01-05
  - hypothesis: a trial whose backtest trades are identical to an already counted trial (same entries and exits) adds no new chance of a lucky result, so it should not raise the bar. Counting such clones once would lower N without loosening the test for any genuinely new idea.
  - evidence that clones exist: donchian_breakout-VEXIT-VRVOL@1.0 = donchian_breakout-VEXIT@1.0, and -VRVOL-S4 / -VRVOL-S4-S4 = donchian_breakout-VEXIT-S4@1.0, cell for cell (Feedback records of 2026-09-28 and 2026-10-05; the operator retired them on 2026-10-05 for this reason).
  - how to test: an engine change, not a lab card - for the operator. Compare, for every past research run, the bar with N = all trials and with N = trials with distinct trade lists; report how many cells would change verdict. Nothing should pass only because of this change without also passing every other gate.
  - stop if: no cell changes verdict, or the count of distinct trials is close to the total (clones are rare).
  - not tested here: the paper's skewness / kurtosis correction. It needs the return distribution per cell, which the fact sheet does not give.

### Feedback: donchian_breakout-VEXIT-S4@1.1
- timestamp: 2026-10-08 15:30 UTC · source: Claude daily review 2026-10-08 (update: a cell changed status since the 2026-10-07 feedback) · evidence: BACKTEST_EVIDENCE: 3 cells, 4331 trades (861 + 2414 + 1056) · confidence: medium · strategy: donchian_breakout-VEXIT-S4@1.1 · asset: research coins · timeframe: 4h, 1h, 30m · regime: WEAK_BEAR, EXPANSION · review: 2027-01-06
- parent: source: [C03] Common Risk Factors in Cryptocurrency (Liu, Tsyvinski, Wu)
- hypothesis: One change to donchian_breakout-VEXIT-S4@1.0: longs only when the coin rose more than BTC over the last 126 candles (21 days on 4h), shorts only when it rose less. Coins that beat the market over 1 to 4 weeks kept beating it in the paper, among large coins; the filter should drop breakouts that go against relative strength.
- result: BACKTEST 4h BACKTESTING 861 trades +0.196R (unseen +0.191R), t 3.94, held back by max drawdown 19.5R; 1h FAILED 2414 trades -0.010R (unseen +0.055R); 30m BACKTESTING -> FAILED today, 1056 trades -0.016R (unseen +0.029R), max drawdown 71.7R. Parent today: 4h 1187 trades +0.206R (unseen +0.186R), t 4.799.
- teaches: with one more day of data the picture is the same: on 4h the filter keeps about 73% of the parent's trades at about the same average (+0.196R vs +0.206R), and its drawdown (19.5R) is no lower than before. The 30m cell, which looked flat yesterday, has now failed. The relative-strength rule adds nothing measurable.
- next: stop this line

### Hypothesis: mark candle-source switches in the backtest data (from C06)
- timestamp: 2026-10-09 15:30 UTC · source: Claude daily review 2026-10-09 ([C06] https://researchonline.lse.ac.uk/id/eprint/100409) · evidence: HYPOTHESIS: derived from a published finding (price gaps between exchanges, usually below 1% within a country, larger in fast markets; 34 exchanges, 2017-2018) and our data setup (Binance candles with an OKX fallback) · confidence: low · strategy: all · asset: research coins · timeframe: all · regime: - · review: 2027-01-07
  - hypothesis: where a candle series switches from Binance to OKX (or back), the step between the two sources can create a fake breakout or trigger a stop that never happened on either exchange. Backtest trades that open or close within a few candles of such a switch should be rarer than 1% of trades; if they are more common, they can bias results.
  - how to test: an engine check, not a lab card - for the operator. Count the trades of the main cells (for example donchian_breakout-VEXIT-S4@1.0 4h) that touch a source switch, and compare their average R with the rest. The futures data already keeps its source per row (the engine refuses to compare funding or open interest across exchanges); the candles would need the same mark.
  - stop if: switches are rare and the trades near them look like the rest.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0050 | 2026-10-10 00:59 | P01-BREAKOUT-V1@1.0 | breakout | 4h | When 4H and 1H trend the same way, a close outside the 20-candle range with strong volume and a trending ADX starts a move worth following. |
| EXP-0051 | 2026-10-10 00:59 | P01-BREAKOUT-V2@1.0 | breakout | 1h, 30m, 15m | When 4H and 1H trend the same way, a close outside the 20-candle range with strong volume and a trending ADX starts a move worth following. |
| EXP-0052 | 2026-10-10 00:59 | P01-BREAKOUT-V3@1.0 | breakout | 4h | When 4H and 1H trend the same way, a close outside the 20-candle range with strong volume and a trending ADX starts a move worth following. |
| EXP-0053 | 2026-10-10 00:59 | P01-BREAKOUT-V4@1.0 | breakout | 4h | When 4H and 1H trend the same way, a close outside the 20-candle range with strong volume and a trending ADX starts a move worth following. |
| EXP-0054 | 2026-10-10 00:59 | P02-EMA-PULLBACK-V1@1.0 | mtf_pullback | 4h | A pullback to the 20 EMA inside a 4H + 1H trend, with momentum reset but not broken and buyers since the last swing low still in profit, continues the trend. |
| EXP-0055 | 2026-10-10 00:59 | P02-EMA-PULLBACK-V2@1.0 | mtf_pullback | 1h, 30m, 15m | A pullback to the 20 EMA inside a 4H + 1H trend, with momentum reset but not broken and buyers since the last swing low still in profit, continues the trend. |
| EXP-0056 | 2026-10-10 00:59 | P02-EMA-PULLBACK-V3@1.0 | mtf_pullback | 4h | A pullback to the 20 EMA inside a 4H + 1H trend, with momentum reset but not broken and buyers since the last swing low still in profit, continues the trend. |
| EXP-0057 | 2026-10-10 00:59 | P02-EMA-PULLBACK-V4@1.0 | mtf_pullback | 4h | A pullback to the 20 EMA inside a 4H + 1H trend, with momentum reset but not broken and buyers since the last swing low still in profit, continues the trend. |
| EXP-0058 | 2026-10-10 00:59 | P01-BREAKOUT-V5@1.0 | breakout | 1h, 30m, 15m | When 4H and 1H trend the same way, a close outside the 20-candle range with strong volume and a trending ADX starts a move worth following. |
| EXP-0059 | 2026-10-10 00:59 | P02-EMA-PULLBACK-V5@1.0 | mtf_pullback | 1h, 30m, 15m | A pullback to the 20 EMA inside a 4H + 1H trend, with momentum reset but not broken and buyers since the last swing low still in profit, continues the trend. |

### Feedback: donchian_breakout-VEXIT-S4@1.1
- timestamp: 2026-10-10 15:30 UTC · source: Claude daily review 2026-10-10 (update: the 30m cell changed status again) · evidence: BACKTEST_EVIDENCE: 3 cells, 3029 trades (579 + 1654 + 796) · confidence: medium · strategy: donchian_breakout-VEXIT-S4@1.1 · asset: research coins · timeframe: 4h, 1h, 30m · regime: WEAK_BEAR, COMPRESSION · review: 2027-01-08
- parent: source: [C03] Common Risk Factors in Cryptocurrency (Liu, Tsyvinski, Wu)
- hypothesis: One change to donchian_breakout-VEXIT-S4@1.0: longs only when the coin rose more than BTC over the last 126 candles (21 days on 4h), shorts only when it rose less. Coins that beat the market over 1 to 4 weeks kept beating it in the paper, among large coins; the filter should drop breakouts that go against relative strength.
- result: BACKTEST 4h BACKTESTING 579 trades +0.239R (unseen +0.224R), t 3.917, max drawdown 17.1R; 30m FAILED -> BACKTESTING, 796 trades +0.031R (unseen +0.077R), avg below the +0.12R bar; 1h FAILED 1654 trades -0.014R. Parent today: 4h 871 trades +0.24R, t 4.862. The trade counts of both cards fell sharply since 2026-10-09 (parent 4h 1301 -> 871 trades), so the test sample itself changed.
- teaches: on the new, smaller sample the two cards have the same 4h average again (+0.239R vs +0.24R) and the filter still costs about a third of the trades. The 30m flip from FAILED back to BACKTESTING comes with an average of +0.031R, far below the bar, so it is noise around zero, not a change in the verdict.
- next: stop this line

### Hypothesis: rebound after a forced-selling day (from C07)
- timestamp: 2026-10-10 15:30 UTC · source: Claude daily review 2026-10-10 ([C07] https://www.princeton.edu/~markus/research/papers/liquidity.pdf) · evidence: HYPOTHESIS: derived from a theory paper (margin and loss spirals; liquidity dries up and prices overshoot when speculators must de-lever) and one observed event (the 2026-10-08 sell-off, ten coins at 5.9x to 12.7x ATR, followed on 2026-10-09 by open interest -10.6% on ETH and -11.1% on XRP in 24h) · confidence: low · strategy: none yet · asset: research coins · timeframe: 1h, 4h · regime: STRONG_BEAR, TRANSITION · review: 2027-01-08
  - hypothesis: when a large fall comes WITH a large drop in open interest (positions closed by force, not by choice), part of the fall is an overshoot that reverses within one to two days; when open interest stays flat during the fall, it does not.
  - how to test: a market_structure card (uses oi_chg(n)), compared with the same entry without the open-interest rule (a control). Long only after a fall of several ATR with oi_chg(24) below a threshold; first target at least 2R.
  - blocked on: the futures history is about 1081 hours (about 45 days), so there are only a handful of such days; a test now would have far fewer than 30 trades. Wait for longer history or a backfill.
  - stop if: fewer than 30 unseen-data trades, or the open-interest rule does not beat its control after costs.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0060 | 2026-10-11 00:58 | P02-EMA-PULLBACK-V4-S6@1.0 | mtf_pullback | 4h | The rule 'rsi(close,14) < 65 / rsi(close,14) > 100 - 65' adds nothing to P02-EMA-PULLBACK-V4@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting). |
| EXP-0061 | 2026-10-11 00:58 | P03-FIB-PULLBACK-V1@1.0 | mtf_pullback | 4h | Inside a 4H + 1H trend, a retracement that holds the 61.8% level of the last swing leg is a pullback, not a reversal: the leg resumes. |
| EXP-0062 | 2026-10-11 00:58 | P03-FIB-PULLBACK-V2@1.0 | mtf_pullback | 1h, 30m, 15m | Inside a 4H + 1H trend, a retracement that holds the 61.8% level of the last swing leg is a pullback, not a reversal: the leg resumes. |
| EXP-0063 | 2026-10-11 00:58 | P03-FIB-PULLBACK-V3@1.0 | mtf_pullback | 4h | Inside a 4H + 1H trend, a retracement that holds the 61.8% level of the last swing leg is a pullback, not a reversal: the leg resumes. |
| EXP-0064 | 2026-10-11 00:58 | P03-FIB-PULLBACK-V4@1.0 | mtf_pullback | 4h | Inside a 4H + 1H trend, a retracement that holds the 61.8% level of the last swing leg is a pullback, not a reversal: the leg resumes. |
| EXP-0065 | 2026-10-11 00:58 | P04-MACD-SUPERTREND-V1@1.0 | momentum | 4h | A fresh MACD momentum push in the direction of the Supertrend and of the 4H + 1H trend starts the next leg of the trend. |
| EXP-0066 | 2026-10-11 00:58 | P04-MACD-SUPERTREND-V2@1.0 | momentum | 1h, 30m, 15m | A fresh MACD momentum push in the direction of the Supertrend and of the 4H + 1H trend starts the next leg of the trend. |
| EXP-0067 | 2026-10-11 00:58 | P04-MACD-SUPERTREND-V3@1.0 | momentum | 4h | A fresh MACD momentum push in the direction of the Supertrend and of the 4H + 1H trend starts the next leg of the trend. |
| EXP-0068 | 2026-10-11 00:58 | P04-MACD-SUPERTREND-V4@1.0 | momentum | 4h | A fresh MACD momentum push in the direction of the Supertrend and of the 4H + 1H trend starts the next leg of the trend. |
| EXP-0069 | 2026-10-11 00:58 | P03-FIB-PULLBACK-V5@1.0 | mtf_pullback | 1h, 30m, 15m | Inside a 4H + 1H trend, a retracement that holds the 61.8% level of the last swing leg is a pullback, not a reversal: the leg resumes. |
| EXP-0070 | 2026-10-11 00:58 | P04-MACD-SUPERTREND-V5@1.0 | momentum | 1h, 30m, 15m | A fresh MACD momentum push in the direction of the Supertrend and of the 4H + 1H trend starts the next leg of the trend. |

### Hypothesis: intraday momentum after a high-volume session (from Shen, Urquhart, Wang)
- timestamp: 2026-10-11 04:00 UTC · source: Claude weekly research 2026-10-11 (https://research.birmingham.ac.uk/en/publications/bitcoin-intraday-time-series-momentum/) · evidence: HYPOTHESIS: derived from a peer-reviewed finding on bitcoin (first half-hour return predicts the last half-hour return; strongest when the first session has the highest volume or volatility) · confidence: low · strategy: none yet · asset: BTC, ETH · timeframe: 1h · regime: TRANSITION, COMPRESSION, WEAK_BULL, WEAK_BEAR · review: 2027-01-09
  - hypothesis: after a 1h candle with very high relative volume (rel_vol well above 1.5) and a clear direction, the next hours continue in that direction more often than a plain trend rule says.
  - how to test: a literature card on 1h (not 30m: costs), long after a high-volume green 1h candle, short mirrored, first target at least 2R, time stop of a few candles; compare with the same entry without the volume rule.
  - blocked on: the literature quota and the lab limit (0 cards left today); the R4 queue is ahead of it.
  - stop if: below +0.10R per trade after costs on unseen data, or the volume rule adds nothing.

### Hypothesis: record the engine commit and data window with every test (from R8)
- timestamp: 2026-10-11 04:00 UTC · source: Claude weekly research 2026-10-11 ([R8] https://github.com/microsoft/qlib, commit 54355232463878d2eebb91fe0ee5fa7fa1f5976c) · evidence: HYPOTHESIS: a process idea from Qlib's recorder (it logs the command, the commit and uncommitted code with each run) and our own problem (2026-10-10: many cells' trade counts fell at once, e.g. 4h breakout 1301 -> 871, and nobody could say why) · confidence: medium · strategy: all · asset: - · timeframe: - · regime: - · review: 2027-01-09
  - hypothesis: if each row of memory/strategy_registry.csv also stores the engine commit and the last candle used, a sudden jump in a cell's trade count can be traced to a code change or a data change within one day.
  - how to test: an engine change for the operator (pull request), not a lab card. Check after a month: every jump of more than 20% in a cell's trade count is explained by a commit or a data-window change.
  - stop if: the extra columns explain nothing.

### Feedback: donchian_breakout-VEXIT-S4@1.1
- timestamp: 2026-10-11 15:30 UTC · source: Claude daily review 2026-10-11 (update: the 4h cell reached PAPER_TRADING) · evidence: BACKTEST_EVIDENCE: 3 cells, 3708 trades (633 + 1795 + 1280) · confidence: medium · strategy: donchian_breakout-VEXIT-S4@1.1 · asset: research coins · timeframe: 4h, 1h, 30m · regime: WEAK_BEAR, EXPANSION · review: 2027-01-09
- parent: source: [C03] Common Risk Factors in Cryptocurrency (Liu, Tsyvinski, Wu)
- hypothesis: One change to donchian_breakout-VEXIT-S4@1.0: longs only when the coin rose more than BTC over the last 126 candles (21 days on 4h), shorts only when it rose less. Coins that beat the market over 1 to 4 weeks kept beating it in the paper, among large coins; the filter should drop breakouts that go against relative strength.
- result: BACKTEST 4h PAPER_TRADING 633 trades +0.234R (unseen +0.220R) - "passed every Phase 8 test"; 1h FAILED 1795 trades -0.010R; 30m FAILED 1280 trades -0.006R (Monte Carlo 95% worst drawdown per 100 trades 29.2R, limit 17R). Its parent donchian_breakout-VEXIT@1.0 4h also reached PAPER_TRADING today (814 trades +0.253R, unseen +0.244R).
- teaches: the 4h cell cleared the gates in the first research run after the operator switched on the family gates (2026-10-10): for trend strategies they judge recovery factor, Monte Carlo drawdown per 100 trades and drawdown duration instead of the raw maximum drawdown that blocked it before. Its edge over the parent is still nil: same average, fewer trades. PAPER_TRADING means signals are logged and emailed as PAPER; it is not approval, and paper results, not more backtests, now decide.
- next: stop this line (no more tuning of the relative-strength rule). Let the paper-trading results of the 4h cell decide; compare them with the parent's paper results after 20 or more paper signals each.

### Feedback: donchian_breakout-VEXIT@1.0
- timestamp: 2026-10-11 15:30 UTC · source: Claude daily review 2026-10-11 (update: the 4h cell reached PAPER_TRADING) · evidence: BACKTEST_EVIDENCE: 3 cells, 4555 trades (814 + 2241 + 1500) · confidence: medium · strategy: donchian_breakout-VEXIT@1.0 · asset: research coins · timeframe: 4h, 1h, 30m · regime: WEAK_BEAR, WEAK_BULL, EXPANSION · review: 2027-01-09
- parent: result: donchian_breakout@1.0 4h
- hypothesis: One change to donchian_breakout@1.0: targets 2R / 3R (50 / 50) instead of a first target below 2R. It should keep the edge of donchian_breakout@1.0 and remove part of its losses; tested because it was the strongest BACKTESTING cell this week.
- result: BACKTEST 4h PAPER_TRADING 814 trades +0.253R (unseen +0.244R) - "passed every Phase 8 test"; 1h FAILED 2241 trades -0.019R; 30m FAILED 1500 trades -0.054R (longest drawdown 95% of the tested period, limit 55%). Its parent donchian_breakout@1.0 4h also reached PAPER_TRADING today.
- teaches: after two weeks blocked only by the drawdown gate, the 4h breakout passed once the family gates (switched on 2026-10-10) measured drawdown per 100 trades (Monte Carlo) and the recovery factor instead of the raw maximum. The 2R / 3R targets kept the 4h edge in the train and the unseen part; 1h and 30m never had one. Three closely related cards (donchian_breakout, VEXIT, VEXIT-S4 v1.1) are now in paper trading at once: their paper signals will mostly be the same trades, so they are one test, not three.
- next: no new backtest variant of this line until the paper results come in. Judge it on its paper signals (the engine's kill rule: last 20 paper signals below -0.10R or 8R drawdown).

### Feedback: P02-EMA-PULLBACK-V4-S6@1.0
- timestamp: 2026-10-11 15:30 UTC · source: Claude daily review 2026-10-11 · evidence: BACKTEST_EVIDENCE: 1 cell, 365 trades · confidence: low · strategy: P02-EMA-PULLBACK-V4-S6@1.0 · asset: research coins · timeframe: 4h · regime: - · review: 2027-01-09
- parent: result: P02-EMA-PULLBACK-V4@1.0 4h
- hypothesis: The rule 'rsi(close,14) < 65 / rsi(close,14) > 100 - 65' adds nothing to P02-EMA-PULLBACK-V4@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting).
- result: BACKTEST 4h BACKTESTING 365 trades +0.145R (unseen +0.209R), t 1.518; held back by recovery factor 2.66 (net +52.9R / max drawdown 19.9R, needs 3) and Monte Carlo 95% worst drawdown per 100 trades 27.1R (limit 17R). Parent on 2026-10-10: 297 trades +0.10R, t 0.939.
- teaches: the hypothesis held: without the RSI rule the card takes more trades (365 vs 297) at a higher average (+0.145R vs +0.10R), so the RSI cap was cutting good pullbacks. But the t value (1.518) is far below the trials bar (3.57), and the drawdown per 100 trades is well above the limit; this is a weak cell, not a near-pass.
- next: stop this line until it has more trades. A further rule removal would be a third look at the same 300-odd trades and would only raise the trials counter.

### Hypothesis: judge paper trend signals by market weather (from C08)
- timestamp: 2026-10-11 15:30 UTC · source: Claude daily review 2026-10-11 ([C08] https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/AQR-JPM-Fall-2017.pdf) · evidence: HYPOTHESIS: derived from a published finding (time-series momentum 1880-2016 in 67 markets: positive in every decade, worst in periods without clear trends and in sharp reversals) and today's state (three 4h breakout cells entered PAPER_TRADING while the engine's market weather says "Choppy - stay out") · confidence: low · strategy: donchian_breakout, donchian_breakout-VEXIT, donchian_breakout-VEXIT-S4@1.1 · asset: research coins · timeframe: 4h · regime: TRANSITION, RANGE, COMPRESSION · review: 2027-01-09
  - hypothesis: the first paper signals of the 4h breakout cards come in a trendless market, the condition in which the paper finds trend following loses. Their early paper results will therefore be worse than the backtest average, and that alone is not evidence that the edge is gone.
  - how to test: when the paper signals close, split them by the engine's market-weather verdict at entry (choppy vs trending) and by regime; compare each group with the backtest average of the same regime in the playbook. If the paper losses come only in choppy entries, the backtest still describes the strategy; if they also come in trending entries, the edge is in doubt.
  - stop if: after 20 or more paper signals, trending-weather entries are also below the backtest average.
  - not a rule change: the engine's own kill rule (last 20 paper signals below -0.10R or 8R drawdown) stays as it is.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0071 | 2026-10-12 01:01 | TRD-H4-BREAKOUT-S3@1.0 | breakout | 1h, 30m, 15m, 5m | The rule 'volume > vol_sma(20) * 1.5 / volume > vol_sma(20) * 1.5' adds nothing to TRD-H4-BREAKOUT@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting). |
| EXP-0072 | 2026-10-12 01:01 | P02-EMA-PULLBACK-V4-S6-S6@1.0 | mtf_pullback | 4h | The rule 'close > avwap_swing_low / close < avwap_swing_high' adds nothing to P02-EMA-PULLBACK-V4-S6@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting). |
| EXP-0073 | 2026-10-12 01:01 | P02-EMA-PULLBACK-V4-S6-FHTF@1.0 | mtf_pullback | 4h | P02-EMA-PULLBACK-V4-S6@1.0 loses on regime_mismatch (-0.09R a trade with it, +0.72R without). One change - only when the higher timeframe trends the same way (htf_up / htf_down) - should remove part of those losses and keep the rest. |
| EXP-0074 | 2026-10-12 01:01 | P05-RANGE-REVERSAL-V1@1.0 | mean_reversion | 4h | In a range, a close back inside the Bollinger band after an RSI extreme is the over-reaction ending: price returns to the middle band. |
| EXP-0075 | 2026-10-12 01:01 | P05-RANGE-REVERSAL-V2@1.0 | mean_reversion | 1h, 30m, 15m | In a range, a close back inside the Bollinger band after an RSI extreme is the over-reaction ending: price returns to the middle band. |
| EXP-0076 | 2026-10-12 01:01 | P05-RANGE-REVERSAL-V3@1.0 | mean_reversion | 4h | In a range, a close back inside the Bollinger band after an RSI extreme is the over-reaction ending: price returns to the middle band. |
| EXP-0077 | 2026-10-12 01:01 | P05-RANGE-REVERSAL-V4@1.0 | mean_reversion | 4h | In a range, a close back inside the Bollinger band after an RSI extreme is the over-reaction ending: price returns to the middle band. |
| EXP-0078 | 2026-10-12 01:01 | P06-VWAP-REVERSION-V1@1.0 | mean_reversion | 4h | In a range, a stretch far from the day's volume-weighted average price snaps back to it. |
| EXP-0079 | 2026-10-12 01:01 | P06-VWAP-REVERSION-V2@1.0 | mean_reversion | 1h, 30m, 15m | In a range, a stretch far from the day's volume-weighted average price snaps back to it. |
| EXP-0080 | 2026-10-12 01:01 | P06-VWAP-REVERSION-V3@1.0 | mean_reversion | 4h | In a range, a stretch far from the day's volume-weighted average price snaps back to it. |
| EXP-0081 | 2026-10-12 01:01 | P06-VWAP-REVERSION-V4@1.0 | mean_reversion | 4h | In a range, a stretch far from the day's volume-weighted average price snaps back to it. |

### Feedback: P02-EMA-PULLBACK-V4-S6-FHTF@1.0
- timestamp: 2026-10-12 15:30 UTC · source: Claude daily review 2026-10-12 · evidence: BACKTEST_EVIDENCE: 1 cell, 291 trades · confidence: low · strategy: P02-EMA-PULLBACK-V4-S6-FHTF@1.0 · asset: research coins · timeframe: 4h · regime: - · review: 2027-01-10
- parent: result: P02-EMA-PULLBACK-V4-S6@1.0 4h
- hypothesis: P02-EMA-PULLBACK-V4-S6@1.0 loses on regime_mismatch (-0.09R a trade with it, +0.72R without). One change - only when the higher timeframe trends the same way (htf_up / htf_down) - should remove part of those losses and keep the rest.
- result: BACKTEST 4h BACKTESTING 291 trades +0.036R (unseen +0.108R), t 0.347; profit factor 1.05, recovery factor 0.45 (needs 3), Monte Carlo 95% worst drawdown per 100 trades 33.7R (limit 17R). Parent: 365 trades +0.145R (unseen +0.209R).
- teaches: the hypothesis did not hold. The higher-timeframe filter removed 74 trades and cut the average from +0.145R to +0.036R, so it removed winners, not mainly the regime_mismatch losers. The regime_mismatch tag describes the losers after the fact; the htf filter is not the same thing at entry.
- next: stop this line

### Feedback: P02-EMA-PULLBACK-V4-S6-S6@1.0
- timestamp: 2026-10-12 15:30 UTC · source: Claude daily review 2026-10-12 · evidence: BACKTEST_EVIDENCE: 1 cell, 403 trades · confidence: low · strategy: P02-EMA-PULLBACK-V4-S6-S6@1.0 · asset: research coins · timeframe: 4h · regime: - · review: 2027-01-10
- parent: result: P02-EMA-PULLBACK-V4-S6@1.0 4h
- hypothesis: The rule 'close > avwap_swing_low / close < avwap_swing_high' adds nothing to P02-EMA-PULLBACK-V4-S6@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting).
- result: BACKTEST 4h BACKTESTING 403 trades +0.159R (unseen +0.174R), t 1.751; held back by Monte Carlo 95% worst drawdown per 100 trades 26.6R (limit 17R). Parent: 365 trades +0.145R (unseen +0.209R), t 1.518.
- teaches: the hypothesis held: without the anchored-VWAP rule the card takes 38 more trades at about the same average (+0.159R vs +0.145R). It is the second rule removal in a row that did no harm (the RSI cap first), so the P02 4h pullback works as well with fewer rules. But t 1.751 is far below the bar (3.60) and the drawdown per 100 trades is well above the limit.
- next: stop removing rules from this card (a third removal on the same 400 trades is curve-fitting). Wait for more data before any change; the open problem is the drawdown, not the entry.

### Feedback: TRD-H4-BREAKOUT-S3@1.0
- timestamp: 2026-10-12 15:30 UTC · source: Claude daily review 2026-10-12 · evidence: BACKTEST_EVIDENCE: 4 cells, 4845 trades (939 + 837 + 1458 + 1611) · confidence: low · strategy: TRD-H4-BREAKOUT-S3@1.0 · asset: research coins · timeframe: 1h, 30m, 15m, 5m · regime: TRANSITION · review: 2027-01-10
- parent: result: TRD-H4-BREAKOUT@1.0 1h
- hypothesis: The rule 'volume > vol_sma(20) * 1.5 / volume > vol_sma(20) * 1.5' adds nothing to TRD-H4-BREAKOUT@1.0: the simpler card without it should do at least as well on new data (fewer rules = less room for overfitting).
- result: BACKTEST 1h BACKTESTING 939 trades +0.152R (unseen +0.273R), held back only by Monte Carlo 95% worst drawdown per 100 trades 22.0R (limit 17R); 30m BACKTESTING 837 trades +0.005R; 15m FAILED 1458 trades -0.024R; 5m FAILED 1611 trades -0.044R. Playbook: 1h +0.43R over 62 trades in TRANSITION. The parent 1h was +0.09R a trade with max drawdown 50.8R in the fact sheet of 2026-10-07 (today's parent numbers are not in the fact sheet).
- teaches: on 1h, dropping the 1.5x volume rule did not hurt and may have helped (+0.152R now vs the parent's +0.09R a week ago - different samples, so not a clean comparison). The shorter timeframes stay near zero or negative, as for every breakout card so far.
- next: no new variant; let the 1h cell gather data. If it later clears the drawdown gate, compare it with its parent on the same day's sample before trusting the difference.

### Hypothesis: TEST alerts of strategies that fail overall will lose on average (from the 2026-10-11 TEST losses, C04, C05)
- timestamp: 2026-10-12 15:30 UTC · source: Claude daily review 2026-10-12 · evidence: HYPOTHESIS: derived from config.yaml -> signal_center (a TEST alert needs only a positive backtest on that one coin) and the multiple-testing papers [C04] and [C05]; three TEST losses on 2026-10-11 are an example, not evidence · confidence: low · strategy: all TEST-stage cells · asset: signal coins · timeframe: all · regime: - · review: 2027-01-10
  - hypothesis: when a strategy is FAILED across all coins but positive on one coin, its TEST alerts on that coin will on average do no better than the strategy's all-coin backtest average, because the coin was picked after the fact from many coin x strategy x timeframe cells.
  - how to test: no lab card - an engine report for the operator. Once 30 or more TEST signals have closed, compare their average R with (a) the per-coin backtest average that qualified them and (b) the strategy's all-coin average. If (a) is far above the result and (b) is close, the per-coin selection adds nothing.
  - stop if: TEST results match the per-coin backtest averages after 30 or more closed signals.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0082 | 2026-10-13 01:02 | TRD-H4-BREAKOUT-S3-FDISP@1.0 | breakout | 1h, 30m, 15m, 5m | TRD-H4-BREAKOUT-S3@1.0 loses on false_breakout (-0.24R a trade with it, +0.57R without). One change - a strong candle (displacement) in the trade direction within the last 3 candles - should remove part of those losses and keep the rest. |
| EXP-0083 | 2026-10-13 01:02 | P07-SQUEEZE-RETEST-V1@1.0 | breakout | 4h | A breakout out of a volatility squeeze that survives its first retest is real: the new move continues. |
| EXP-0084 | 2026-10-13 01:02 | P07-SQUEEZE-RETEST-V2@1.0 | breakout | 1h, 30m, 15m | A breakout out of a volatility squeeze that survives its first retest is real: the new move continues. |
| EXP-0085 | 2026-10-13 01:02 | P07-SQUEEZE-RETEST-V3@1.0 | breakout | 4h | A breakout out of a volatility squeeze that survives its first retest is real: the new move continues. |
| EXP-0086 | 2026-10-13 01:02 | P07-SQUEEZE-RETEST-V4@1.0 | breakout | 4h | A breakout out of a volatility squeeze that survives its first retest is real: the new move continues. |
| EXP-0087 | 2026-10-13 01:02 | P08-SESSION-BREAKOUT-V1@1.0 | breakout | 1h | The quiet Asia session builds a range; the first break of it when London / New York volume arrives, in the 4H + 1H trend direction, runs. |
| EXP-0088 | 2026-10-13 01:02 | P08-SESSION-BREAKOUT-V2@1.0 | breakout | 30m, 15m | The quiet Asia session builds a range; the first break of it when London / New York volume arrives, in the 4H + 1H trend direction, runs. |
| EXP-0089 | 2026-10-13 01:02 | P08-SESSION-BREAKOUT-V3@1.0 | breakout | 1h | The quiet Asia session builds a range; the first break of it when London / New York volume arrives, in the 4H + 1H trend direction, runs. |
| EXP-0090 | 2026-10-13 01:02 | P08-SESSION-BREAKOUT-V4@1.0 | breakout | 1h | The quiet Asia session builds a range; the first break of it when London / New York volume arrives, in the 4H + 1H trend direction, runs. |
| EXP-0091 | 2026-10-13 01:02 | P07-SQUEEZE-RETEST-V5@1.0 | breakout | 1h, 30m, 15m | A breakout out of a volatility squeeze that survives its first retest is real: the new move continues. |
| EXP-0092 | 2026-10-13 01:02 | P08-SESSION-BREAKOUT-V5@1.0 | breakout | 30m, 15m | The quiet Asia session builds a range; the first break of it when London / New York volume arrives, in the 4H + 1H trend direction, runs. |

### Feedback: TRD-H4-BREAKOUT-S3-FDISP@1.0
- timestamp: 2026-10-13 15:30 UTC · source: Claude daily review 2026-10-13 · evidence: BACKTEST_EVIDENCE: 4 cells, 2800 trades (412 + 679 + 708 + 1001) · confidence: low · strategy: TRD-H4-BREAKOUT-S3-FDISP@1.0 · asset: research coins · timeframe: 30m, 1h, 15m, 5m · regime: - · review: 2027-01-11
- parent: result: TRD-H4-BREAKOUT-S3@1.0 30m
- hypothesis: TRD-H4-BREAKOUT-S3@1.0 loses on false_breakout (-0.24R a trade with it, +0.57R without). One change - a strong candle (displacement) in the trade direction within the last 3 candles - should remove part of those losses and keep the rest.
- result: BACKTEST 30m BACKTESTING 412 trades +0.187R (unseen +0.364R), held back by recovery factor 2.32 (needs 3) and Monte Carlo 95% worst drawdown per 100 trades 19.9R (limit 17R); 1h BACKTESTING 679 trades +0.126R (unseen +0.271R), recovery factor 2.88, Monte Carlo 22.7R; 15m BACKTESTING 708 trades +0.005R; 5m FAILED 1001 trades -0.180R. Parent (2026-10-12): 30m 837 trades +0.005R, 1h 939 trades +0.152R.
- teaches: on 30m the displacement filter halved the trades and lifted the average from +0.005R to +0.187R, with a stronger unseen part (+0.364R) - the biggest one-change gain in the lab so far. On 1h it took a third of the trades away for a slightly lower average (+0.126R vs +0.152R), so it does not help everywhere. Caution: the filter was chosen from the parent's own loss tags on the same history, so part of the 30m gain may be fitted to that history; the unseen part is the better guide and it held up.
- next: no further change to this card. Let it gather data; if the 30m cell clears the recovery factor and drawdown gates, it goes to paper trading by the engine's rules, and the paper results decide.

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0093 | 2026-10-14 01:13 | TRD-H4-BREAKOUT-FDISP@1.0 | breakout | 1h, 30m, 15m, 5m | TRD-H4-BREAKOUT@1.0 loses on false_breakout (-0.18R a trade with it, +0.64R without). One change - a strong candle (displacement) in the trade direction within the last 3 candles - should remove part of those losses and keep the rest. |
| EXP-0094 | 2026-10-14 01:13 | P09-SWEEP-MSS-V1@1.0 | liquidity_reversal | 4h | A sweep of the stops under a pullback low followed by a strong close above the recent highs is the end of the pullback: the trend resumes. |
| EXP-0095 | 2026-10-14 01:13 | P09-SWEEP-MSS-V2@1.0 | liquidity_reversal | 1h, 30m, 15m | A sweep of the stops under a pullback low followed by a strong close above the recent highs is the end of the pullback: the trend resumes. |
| EXP-0096 | 2026-10-14 01:13 | P09-SWEEP-MSS-V3@1.0 | liquidity_reversal | 4h | A sweep of the stops under a pullback low followed by a strong close above the recent highs is the end of the pullback: the trend resumes. |
| EXP-0097 | 2026-10-14 01:13 | P09-SWEEP-MSS-V4@1.0 | liquidity_reversal | 4h | A sweep of the stops under a pullback low followed by a strong close above the recent highs is the end of the pullback: the trend resumes. |
| EXP-0098 | 2026-10-14 01:13 | P10-CROWDING-FADE-V1@1.0 | liquidity_reversal | 4h | When one side is crowded (high funding, rising open interest) and price turns against it, their forced exits push price further the other way. |
| EXP-0099 | 2026-10-14 01:13 | P10-CROWDING-FADE-V2@1.0 | liquidity_reversal | 1h, 30m, 15m | When one side is crowded (high funding, rising open interest) and price turns against it, their forced exits push price further the other way. |
| EXP-0100 | 2026-10-14 01:13 | P10-CROWDING-FADE-V3@1.0 | liquidity_reversal | 4h | When one side is crowded (high funding, rising open interest) and price turns against it, their forced exits push price further the other way. |
| EXP-0101 | 2026-10-14 01:13 | P10-CROWDING-FADE-V4@1.0 | liquidity_reversal | 4h | When one side is crowded (high funding, rising open interest) and price turns against it, their forced exits push price further the other way. |
| EXP-0102 | 2026-10-14 01:13 | P09-SWEEP-MSS-V5@1.0 | liquidity_reversal | 1h, 30m, 15m | A sweep of the stops under a pullback low followed by a strong close above the recent highs is the end of the pullback: the trend resumes. |

### Feedback: TRD-H4-BREAKOUT-FDISP@1.0
- timestamp: 2026-10-14 15:30 UTC · source: Claude daily review 2026-10-14 · evidence: BACKTEST_EVIDENCE: 4 cells, 3036 trades (449 + 703 + 777 + 1107) · confidence: low · strategy: TRD-H4-BREAKOUT-FDISP@1.0 · asset: research coins · timeframe: 30m, 1h, 15m, 5m · regime: - · review: 2027-01-12
- parent: result: TRD-H4-BREAKOUT@1.0 30m
- hypothesis: TRD-H4-BREAKOUT@1.0 loses on false_breakout (-0.18R a trade with it, +0.64R without). One change - a strong candle (displacement) in the trade direction within the last 3 candles - should remove part of those losses and keep the rest.
- result: BACKTEST 30m BACKTESTING 449 trades +0.177R (unseen +0.306R) and 1h BACKTESTING 703 trades +0.132R (unseen +0.257R), each held back only by Monte Carlo 95% worst drawdown per 100 trades (21.6R and 22.5R, limit 17R); 15m FAILED 777 trades -0.021R; 5m FAILED 1107 trades -0.177R.
- teaches: the same displacement rule gives almost the same result on the parent with the volume rule (this card) as on the parent without it (TRD-H4-BREAKOUT-S3-FDISP: 30m 467 trades +0.169R, 1h 747 trades +0.125R today). So the gain comes from the displacement rule, not from the volume rule, and it repeats on two related parents (not independent tests: they share most trades). It helps on 30m and 1h, not on 15m or 5m.
- next: no further change. Two near-copies now wait on the same drawdown gate; if both reach PAPER_TRADING, treat their paper signals as one test.

### Feedback: TRD-H4-BREAKOUT-S3-FDISP@1.0
- timestamp: 2026-10-14 15:30 UTC · source: Claude daily review 2026-10-14 (update: the 15m cell changed status) · evidence: BACKTEST_EVIDENCE: 4 cells, 3169 trades (467 + 747 + 803 + 1152) · confidence: low · strategy: TRD-H4-BREAKOUT-S3-FDISP@1.0 · asset: research coins · timeframe: 30m, 1h, 15m, 5m · regime: - · review: 2027-01-12
- parent: result: TRD-H4-BREAKOUT-S3@1.0 30m
- hypothesis: TRD-H4-BREAKOUT-S3@1.0 loses on false_breakout (-0.24R a trade with it, +0.57R without). One change - a strong candle (displacement) in the trade direction within the last 3 candles - should remove part of those losses and keep the rest.
- result: BACKTEST 30m BACKTESTING 467 trades +0.169R (unseen +0.299R); 1h BACKTESTING 747 trades +0.125R (unseen +0.263R), Monte Carlo 95% worst drawdown per 100 trades 23.4R (limit 17R); 15m BACKTESTING -> FAILED, 803 trades -0.017R; 5m FAILED 1152 trades -0.175R.
- teaches: one more day of data left the 30m and 1h results almost unchanged (30m +0.187R -> +0.169R, 1h +0.126R -> +0.125R) and confirmed that the rule does nothing for 15m. The pattern "works on 30m and 1h, not below" now holds for both FDISP cards.
- next: no further change; same as yesterday.

### Feedback: donchian_breakout-VEXIT-S4@1.1
- timestamp: 2026-10-14 15:30 UTC · source: Claude daily review 2026-10-14 (update: the 30m cell changed status) · evidence: BACKTEST_EVIDENCE: 3 cells, 4265 trades (722 + 2052 + 1491) · confidence: medium · strategy: donchian_breakout-VEXIT-S4@1.1 · asset: research coins · timeframe: 4h, 1h, 30m · regime: - · review: 2027-01-12
- parent: source: [C03] Common Risk Factors in Cryptocurrency (Liu, Tsyvinski, Wu)
- hypothesis: One change to donchian_breakout-VEXIT-S4@1.0: longs only when the coin rose more than BTC over the last 126 candles (21 days on 4h), shorts only when it rose less. Coins that beat the market over 1 to 4 weeks kept beating it in the paper, among large coins; the filter should drop breakouts that go against relative strength.
- result: BACKTEST 4h PAPER_TRADING 722 trades +0.213R (unseen +0.244R); 30m FAILED -> BACKTESTING, 1491 trades +0.003R (needs +0.12R); 1h FAILED 2052 trades -0.026R. No paper signal has closed yet.
- teaches: the 30m cell keeps flipping between FAILED and BACKTESTING at an average of about 0R; the flips are noise around zero, not information. Only the 4h cell matters, and it is now judged by paper results.
- next: stop this line (unchanged); ignore 30m status flips in future reviews unless its average moves clearly above the bar.

### Hypothesis: score TEST and PAPER signals by correlated group, as the risk engine does (from C11)
- timestamp: 2026-10-14 15:30 UTC · source: Claude daily review 2026-10-14 ([C11] https://www.shortform.com/pdf/market-wizards-pdf-jack-d-schwager and https://www.ninjatrader.com/futures/blogs/futures-trading-book-review-5-takeaways-from-the-little-book-of-market-wizards/) · evidence: HYPOTHESIS: derived from secondary summaries of a trading book (CLAIM: the interviewed traders cap the risk of each trade and never let one idea decide the account) and one observed case (BTC and ETH TEST shorts from the same strategy at 2026-10-12 23:59 UTC, -1.15R and -1.10R) · confidence: low · strategy: TEST and PAPER stages · asset: signal coins · timeframe: all · regime: - · review: 2027-01-12
  - hypothesis: when two TEST or PAPER signals of the same strategy and direction fire within the same hour on coins whose returns move together, they are one idea. Counting them as two inflates both the number of samples and the measured losses or wins.
  - what exists already: for LIVE positions the risk engine allows only 1 position per direction in a group of coins whose 1h returns correlate at 0.7 or more (config.yaml -> risk -> corr_threshold). The TEST alerts' cooldown is per coin, so this grouping does not reach TEST and PAPER results.
  - how to test: an engine report, not a lab card - for the operator. Re-count closed TEST and PAPER results with same-hour, same-direction, correlated signals merged into one; compare the sample size and the average R with the plain count.
  - stop if: such clusters turn out to be rare (under 10% of TEST and PAPER signals).

| # | First tested (UTC) | Strategy | Family | Timeframes | Hypothesis |
|---|---|---|---|---|---|
| EXP-0103 | 2026-10-15 01:11 | P11-MOMENTUM-V1@1.0 | momentum | 30m | When most of the coins break their 20-candle low (high) together, BTC moves the same way and the 1H is already moving, the first one or two breaks of the move still run - before the 4H has turned. |
| EXP-0104 | 2026-10-15 01:11 | P11-MOMENTUM-V2@1.0 | momentum | 30m | V1 is stronger when the break also takes out the 24-hour low (high), where many stops sit, and comes out of a quiet squeeze (fresh energy). |
| EXP-0105 | 2026-10-15 01:11 | P11-MOMENTUM-V3@1.0 | momentum | 1h | The same as V2 on 1H closes: later than 30m but steadier, fewer fake breaks. |
| EXP-0106 | 2026-10-15 01:11 | P11-MOMENTUM-V4@1.0 | momentum | 30m | After a fresh market-wide break, the first pullback to the 30m EMA20 that is rejected continues the move at a better price - instead of selling the low (buying the high). |
| EXP-0107 | 2026-10-15 01:11 | P11-MOMENTUM-C@1.0 (control twin of P11-MOMENTUM-V1) | momentum | 30m | Control: the plain 30m breakout under the same gate - V1 must beat it, or its extras add nothing. |
| EXP-0108 | 2026-10-15 01:11 | P12-LEADER-V1@1.0 | momentum | 4h | When BTC jumps, the coin already leading the jump keeps rising for a day or two - more than BTC and more than the coins that have not moved yet. |
| EXP-0109 | 2026-10-15 01:11 | P12-LEADER-V2@1.0 | momentum | 4h | A sharper BTC jump (3% in 12 hours) shows the leader more clearly than a slow 24-hour rise. |
| EXP-0110 | 2026-10-15 01:11 | P12-LEADER-V3@1.0 | momentum | 1h | The same leader effect, entered at the 1H close: earlier than V1. |
| EXP-0111 | 2026-10-15 01:11 | P12-LEADER-C@1.0 (control twin of P12-LEADER-V1) | momentum | 4h | Control: buying any coin after a BTC jump - the benchmark the leader pick must beat. |

### Feedback: TRD-H4-BREAKOUT-S3-FDISP@1.0
- timestamp: 2026-10-15 15:30 UTC · source: Claude daily review 2026-10-15 (update: the 15m cell changed status) · evidence: BACKTEST_EVIDENCE: 4 cells, 2797 trades (412 + 679 + 708 + 998) · confidence: low · strategy: TRD-H4-BREAKOUT-S3-FDISP@1.0 · asset: research coins · timeframe: 30m, 1h, 15m, 5m · regime: - · review: 2027-01-13
- parent: result: TRD-H4-BREAKOUT-S3@1.0 30m
- hypothesis: TRD-H4-BREAKOUT-S3@1.0 loses on false_breakout (-0.24R a trade with it, +0.57R without). One change - a strong candle (displacement) in the trade direction within the last 3 candles - should remove part of those losses and keep the rest.
- result: BACKTEST 30m BACKTESTING 412 trades +0.187R (unseen +0.364R); 1h BACKTESTING 679 trades +0.126R (unseen +0.271R); 15m FAILED -> BACKTESTING at 708 trades +0.005R (needs +0.10R); 5m FAILED 998 trades -0.182R.
- teaches: the 15m flip back to BACKTESTING comes with an average of +0.005R - noise around zero, the same as the 30m flips of the v1.1 card. The 30m and 1h numbers are back to the 2026-10-13 sample.
- next: no change (as on 2026-10-14). Future reviews should not write a new Feedback for a status flip whose average stays within 0.05R of zero.

### Feedback: donchian_breakout-VEXIT-S4@1.1
- timestamp: 2026-10-15 15:30 UTC · source: Claude daily review 2026-10-15 (update: the 30m cell changed status) · evidence: BACKTEST_EVIDENCE: 3 cells, 3707 trades (633 + 1795 + 1279) · confidence: medium · strategy: donchian_breakout-VEXIT-S4@1.1 · asset: research coins · timeframe: 4h, 1h, 30m · regime: - · review: 2027-01-13
- parent: source: [C03] Common Risk Factors in Cryptocurrency (Liu, Tsyvinski, Wu)
- hypothesis: One change to donchian_breakout-VEXIT-S4@1.0: longs only when the coin rose more than BTC over the last 126 candles (21 days on 4h), shorts only when it rose less. Coins that beat the market over 1 to 4 weeks kept beating it in the paper, among large coins; the filter should drop breakouts that go against relative strength.
- result: BACKTEST 4h PAPER_TRADING 633 trades +0.234R (unseen +0.225R); 30m BACKTESTING -> FAILED, 1279 trades -0.005R; 1h FAILED 1795 trades -0.010R. Paper: no closed signal yet; the 4h cell is on the watch list for ETH and SOL shorts today.
- teaches: nothing new; the 30m cell flips around 0R.
- next: stop this line (unchanged).

### Hypothesis: who_pays lines should name a forced or utilitarian counterparty (from C12)
- timestamp: 2026-10-15 15:30 UTC · source: Claude daily review 2026-10-15 ([C12] https://dailyspeculations.com/reviews/books/trading-exchanges-harris.html and https://www.turtletrader.com/larry-harris-review) · evidence: HYPOTHESIS: derived from two book reviews (CLAIM: Harris sorts traders into profit-motivated ones, who cannot profit from each other in total, and utilitarian ones such as hedgers and investors, who trade for other reasons and pay for it) and our edge blocks · confidence: low · strategy: all lab and library cards with an edge block · asset: - · timeframe: - · regime: - · review: 2027-01-13
  - hypothesis: cards whose edge block names a counterparty who must trade (liquidated or stopped-out traders, hedgers, index or mandate flows - "forced_flow" or "risk_premium") hold up better on unseen data than cards whose who_pays line names other profit-seeking traders who are merely "wrong" (most "behavioural" mean-reversion cards).
  - how to test: no new card - a tally from the existing registry for the operator or the weekly research: group every tested cell by its edge type and compare the share that reached BACKTESTING or better, and the unseen-part average. Our current evidence fits the idea (the only cells in PAPER are forced_flow breakouts; the behavioural R4 mean-reversion cards all FAILED), but that is a handful of cards.
  - stop if: the edge types show no difference once 20 or more cards per type have been tested.
