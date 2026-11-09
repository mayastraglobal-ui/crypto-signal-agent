# Market weather

What kind of day it is, from the hourly scan's own numbers (engine/weather.py). Explains the market only: it never creates a signal or changes a rule.

- verdict (2026-11-09 22:44 UTC): **Downtrend - the strategies wait for a clean 4H / 1H** - BTC is falling on the daily chart (the price trend line below). The strategy filter is stricter: it trades a SHORT only when 4H and 1H both show a clean downtrend, because a grinding fall with bounces stops out early shorts. A SHORT alert comes once they agree.
- coins: BTC downtrend on the daily chart (not confirmed), ETH downtrend on the daily chart (not confirmed), SOL downtrend on the daily chart (not confirmed), SUI trend down, XRP trend down, ZEC turning down (not confirmed)
- fits: no longs, no buying the dip; checking the stop of any open long; waiting for a SHORT alert - it often comes after a bounce fails · avoid: buying the dip (catching a falling knife); shorting by hand right after a big red candle, at the lows
- BTC: daily price trend DOWN · -9.4% in 30 days; 1D RANGE / 4H WEAK_BEAR / 1H RANGE (timeframes disagree (1D RANGE, 4H WEAK_BEAR, 1H RANGE)); volatility normal (higher than 50% of the last year); usual 24h move ±1.0%, 8 of 10 similar days within ±2.2%; crowding neutral (funding +0.0056%/8h, OI +1.9% 24h)
- ETH: daily price trend DOWN · -14.5% in 30 days · lower highs and lower lows; 1D UNCLEAR / 4H STRONG_BEAR / 1H TRANSITION (timeframes disagree (1D UNCLEAR, 4H STRONG_BEAR, 1H TRANSITION)); volatility normal (higher than 55% of the last year); usual 24h move ±1.6%, 8 of 10 similar days within ±3.8%; crowding neutral (funding +0.0037%/8h, OI -1.3% 24h)
- SOL: daily price trend DOWN · -20.7% in 30 days · lower highs and lower lows; 1D TRANSITION / 4H STRONG_BEAR / 1H RANGE (timeframes disagree (1D TRANSITION, 4H STRONG_BEAR, 1H RANGE)); volatility normal (higher than 57% of the last year); usual 24h move ±2.0%, 8 of 10 similar days within ±4.5%; crowding neutral (funding +0.0046%/8h, OI +1.7% 24h)
- SUI: daily price trend DOWN · -23.2% in 30 days · lower highs and lower lows; 1D WEAK_BEAR / 4H WEAK_BEAR / 1H UNCLEAR (1D/4H bearish, 1W UNCLEAR); volatility normal (higher than 48% of the last year); usual 24h move ±2.6%, 8 of 10 similar days within ±5.3%; crowding neutral (funding +0.0083%/8h, OI +2.5% 24h)
- XRP: daily price trend DOWN · -20.2% in 30 days · lower highs and lower lows; 1D WEAK_BEAR / 4H STRONG_BEAR / 1H TRANSITION (1D/4H bearish, 1W UNCLEAR); volatility normal (higher than 60% of the last year); usual 24h move ±1.6%, 8 of 10 similar days within ±3.5%; crowding neutral (funding -0.0001%/8h, OI -3.2% 24h)
- ZEC: daily price trend SIDEWAYS · +0.6% in 30 days; 1D RANGE / 4H RANGE / 1H TRANSITION (timeframes disagree (1D RANGE, 4H RANGE, 1H TRANSITION)); volatility normal (higher than 52% of the last year); usual 24h move ±3.4%, 8 of 10 similar days within ±7.3%; crowding neutral (funding +0.0100%/8h, OI -4.9% 24h)
- altcoins vs BTC (24h, median): -0.7%
- BTC dominance (CoinGecko): 59.68%, 24h -0.48 pt, 7d +0.46 pt - BTC up + BTC.D down: money rotating into altcoins (alt longs favored)
- event: US CPI (Oct data) 2026-11-10 13:30 UTC
- warning: High-impact event within 24 hours: no new trades from 1 hour before to 1 hour after.
- Explains the market. It never creates a signal and never changes a rule, a size or an approval.
