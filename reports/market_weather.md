# Market weather

What kind of day it is, from the hourly scan's own numbers (engine/weather.py). Explains the market only: it never creates a signal or changes a rule.

- verdict (2026-11-27 20:16 UTC): **Downtrend - the strategies wait for a clean 4H / 1H** - BTC is falling on the daily chart (the price trend line below). The strategy filter is stricter: it trades a SHORT only when 4H and 1H both show a clean downtrend, because a grinding fall with bounces stops out early shorts. A SHORT alert comes once they agree.
- coins: BTC downtrend on the daily chart (not confirmed), ETH downtrend on the daily chart (not confirmed), SOL downtrend on the daily chart (not confirmed), XRP downtrend on the daily chart (not confirmed), ZEC trend down
- fits: no longs, no buying the dip; checking the stop of any open long; waiting for a SHORT alert - it often comes after a bounce fails · avoid: buying the dip (catching a falling knife); shorting by hand right after a big red candle, at the lows
- BTC: daily price trend DOWN · -25.1% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H RANGE / 1H TRANSITION (timeframes disagree (1D STRONG_BEAR, 4H RANGE, 1H TRANSITION)); volatility extreme (higher than 95% of the last year); usual 24h move ±1.6%, 8 of 10 similar days within ±3.5%; crowding neutral (funding -0.0001%/8h, OI -0.8% 24h)
- ETH: daily price trend DOWN · -28.1% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H RANGE / 1H TRANSITION (timeframes disagree (1D STRONG_BEAR, 4H RANGE, 1H TRANSITION)); volatility high (higher than 92% of the last year); usual 24h move ±2.0%, 8 of 10 similar days within ±4.3%; crowding neutral (funding -0.0008%/8h, OI +0.8% 24h)
- SOL: daily price trend DOWN · -29.9% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H RANGE / 1H TRANSITION (timeframes disagree (1D STRONG_BEAR, 4H RANGE, 1H TRANSITION)); volatility high (higher than 92% of the last year); usual 24h move ±2.6%, 8 of 10 similar days within ±4.9%; crowding neutral (funding +0.0052%/8h, OI +6.6% 24h)
- XRP: daily price trend DOWN · -29.1% in 30 days · lower highs and lower lows; 1D WEAK_BEAR / 4H RANGE / 1H TRANSITION (timeframes disagree (1D WEAK_BEAR, 4H RANGE, 1H TRANSITION)); volatility high (higher than 88% of the last year); usual 24h move ±1.9%, 8 of 10 similar days within ±4.5%; crowding neutral (funding +0.0009%/8h, OI -7.7% 24h)
- ZEC: daily price trend DOWN · -47.9% in 30 days · lower highs and lower lows; 1D WEAK_BEAR / 4H WEAK_BEAR / 1H RANGE (1D/4H bearish, 1W TRANSITION); volatility high (higher than 92% of the last year); usual 24h move ±3.7%, 8 of 10 similar days within ±9.5%; crowding neutral (funding +0.0075%/8h, OI +0.9% 24h)
- altcoins vs BTC (24h, median): +1.9%
- BTC dominance (CoinGecko): 57.70%, 24h -0.21 pt, 7d -0.10 pt - BTC down + BTC.D down: altcoins falling less than BTC
- event: US jobs report / Employment Situation (Nov data) 2026-12-04 13:30 UTC
- warning: BTC's daily range is extreme (top 5% of the year): stops need room - the alerts' size at your fixed % risk already gets smaller when the stop is wider.
- Explains the market. It never creates a signal and never changes a rule, a size or an approval.
