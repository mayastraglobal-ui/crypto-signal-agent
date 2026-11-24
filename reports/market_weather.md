# Market weather

What kind of day it is, from the hourly scan's own numbers (engine/weather.py). Explains the market only: it never creates a signal or changes a rule.

- verdict (2026-11-24 02:11 UTC): **Downtrend - the strategies wait for a clean 4H / 1H** - BTC is falling on the daily chart (the price trend line below). The strategy filter is stricter: it trades a SHORT only when 4H and 1H both show a clean downtrend, because a grinding fall with bounces stops out early shorts. A SHORT alert comes once they agree.
- coins: BTC downtrend on the daily chart (not confirmed), ETH downtrend on the daily chart (not confirmed), SOL downtrend on the daily chart (not confirmed), SUI downtrend on the daily chart (not confirmed), XRP downtrend on the daily chart (not confirmed), ZEC downtrend on the daily chart (not confirmed)
- fits: no longs, no buying the dip; checking the stop of any open long; waiting for a SHORT alert - it often comes after a bounce fails · avoid: buying the dip (catching a falling knife); shorting by hand right after a big red candle, at the lows
- BTC: daily price trend DOWN · -24.3% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H TRANSITION / 1H TRANSITION (timeframes disagree (1D STRONG_BEAR, 4H TRANSITION, 1H TRANSITION)); volatility extreme (higher than 96% of the last year); usual 24h move ±1.7%, 8 of 10 similar days within ±3.6%; crowding neutral (funding +0.0054%/8h, OI -3.9% 24h)
- ETH: daily price trend DOWN · -27.5% in 30 days; 1D WEAK_BEAR / 4H TRANSITION / 1H TRANSITION (timeframes disagree (1D WEAK_BEAR, 4H TRANSITION, 1H TRANSITION)); volatility high (higher than 93% of the last year); usual 24h move ±1.8%, 8 of 10 similar days within ±4.0%; crowding neutral (funding -0.0069%/8h, OI -3.1% 24h)
- SOL: daily price trend DOWN · -29.6% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H TRANSITION / 1H TRANSITION (timeframes disagree (1D STRONG_BEAR, 4H TRANSITION, 1H TRANSITION)); volatility high (higher than 92% of the last year); usual 24h move ±2.6%, 8 of 10 similar days within ±4.9%; crowding neutral (funding -0.0081%/8h, OI +0.3% 24h)
- SUI: daily price trend DOWN · -28.2% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H TRANSITION / 1H UNCLEAR (timeframes disagree (1D STRONG_BEAR, 4H TRANSITION, 1H UNCLEAR)); volatility high (higher than 84% of the last year); usual 24h move ±2.9%, 8 of 10 similar days within ±5.6%; crowding neutral (funding -0.0016%/8h, OI +2.5% 24h)
- XRP: daily price trend DOWN · -27.6% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H TRANSITION / 1H UNCLEAR (timeframes disagree (1D STRONG_BEAR, 4H TRANSITION, 1H UNCLEAR)); volatility high (higher than 90% of the last year); usual 24h move ±1.9%, 8 of 10 similar days within ±4.6%; crowding neutral (funding -0.0089%/8h, OI -0.8% 24h)
- ZEC: daily price trend DOWN · -35.7% in 30 days · lower highs and lower lows; 1D TRANSITION / 4H TRANSITION / 1H UNCLEAR (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H UNCLEAR)); volatility high (higher than 88% of the last year); usual 24h move ±3.3%, 8 of 10 similar days within ±8.4%; crowding neutral (funding +0.0092%/8h, OI -2.4% 24h)
- altcoins vs BTC (24h, median): +2.0%
- BTC dominance (CoinGecko): 57.94%, 24h -0.91 pt, 7d -0.62 pt - BTC up + BTC.D down: money rotating into altcoins (alt longs favored)
- event: US GDP (Second Estimate), 3rd Quarter 2026 2026-11-25 13:30 UTC
- event: US PCE / Personal Income and Outlays (Oct data) 2026-11-25 13:30 UTC
- warning: BTC's daily range is extreme (top 4% of the year): stops need room - the alerts' size at your fixed % risk already gets smaller when the stop is wider.
- Explains the market. It never creates a signal and never changes a rule, a size or an approval.
