# Market weather

What kind of day it is, from the hourly scan's own numbers (engine/weather.py). Explains the market only: it never creates a signal or changes a rule.

- verdict (2026-11-27 04:11 UTC): **Range day** - No trend: price moves sideways between levels on 4H and 1H.
- coins: BTC downtrend on the daily chart (not confirmed), ETH downtrend on the daily chart (not confirmed), SOL downtrend on the daily chart (not confirmed), XRP downtrend on the daily chart (not confirmed), ZEC trend down
- fits: waiting - the trend strategies don't trade a range · avoid: breakout trades without a retest; trend trades
- BTC: daily price trend DOWN · -25.1% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H RANGE / 1H RANGE (timeframes disagree (1D STRONG_BEAR, 4H RANGE, 1H RANGE)); volatility extreme (higher than 95% of the last year); usual 24h move ±1.6%, 8 of 10 similar days within ±3.5%; crowding neutral (funding +0.0005%/8h, OI +2.6% 24h)
- ETH: daily price trend DOWN · -28.1% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H RANGE / 1H RANGE (timeframes disagree (1D STRONG_BEAR, 4H RANGE, 1H RANGE)); volatility high (higher than 92% of the last year); usual 24h move ±2.0%, 8 of 10 similar days within ±4.3%; crowding neutral (funding +0.0080%/8h, OI +1.5% 24h)
- SOL: daily price trend DOWN · -29.9% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H RANGE / 1H RANGE (timeframes disagree (1D STRONG_BEAR, 4H RANGE, 1H RANGE)); volatility high (higher than 92% of the last year); usual 24h move ±2.6%, 8 of 10 similar days within ±4.9%; crowding neutral (funding +0.0042%/8h, OI -1.5% 24h)
- XRP: daily price trend DOWN · -29.1% in 30 days · lower highs and lower lows; 1D WEAK_BEAR / 4H RANGE / 1H COMPRESSION (timeframes disagree (1D WEAK_BEAR, 4H RANGE, 1H COMPRESSION)); volatility high (higher than 88% of the last year); usual 24h move ±1.9%, 8 of 10 similar days within ±4.5%; crowding neutral (funding +0.0091%/8h, OI -0.9% 24h)
- ZEC: daily price trend DOWN · -47.9% in 30 days · lower highs and lower lows; 1D WEAK_BEAR / 4H WEAK_BEAR / 1H TRANSITION (1D/4H bearish, 1W TRANSITION); volatility high (higher than 92% of the last year); usual 24h move ±3.7%, 8 of 10 similar days within ±9.5%; crowding neutral (funding +0.0079%/8h, OI +1.5% 24h)
- altcoins vs BTC (24h, median): -0.0%
- BTC dominance (CoinGecko): 57.96%, 24h +0.08 pt, 7d -0.08 pt - BTC.D flat - no clear rotation between BTC and the altcoins
- warning: BTC's daily range is extreme (top 5% of the year): stops need room - the alerts' size at your fixed % risk already gets smaller when the stop is wider.
- Explains the market. It never creates a signal and never changes a rule, a size or an approval.
