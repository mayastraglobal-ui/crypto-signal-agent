# Market weather

What kind of day it is, from the hourly scan's own numbers (engine/weather.py). Explains the market only: it never creates a signal or changes a rule.

- verdict (2026-11-12 10:53 UTC): **Downtrend - the strategies wait for a clean 4H / 1H** - BTC is falling on the daily chart (the price trend line below). The strategy filter is stricter: it trades a SHORT only when 4H and 1H both show a clean downtrend, because a grinding fall with bounces stops out early shorts. A SHORT alert comes once they agree.
- coins: BTC downtrend on the daily chart (not confirmed), ETH downtrend on the daily chart (not confirmed), SOL trend down, XRP trend down, ZEC downtrend on the daily chart (not confirmed)
- fits: no longs, no buying the dip; checking the stop of any open long; waiting for a SHORT alert - it often comes after a bounce fails · avoid: buying the dip (catching a falling knife); shorting by hand right after a big red candle, at the lows
- BTC: daily price trend DOWN · -9.6% in 30 days · lower highs and lower lows; 1D UNCLEAR / 4H WEAK_BEAR / 1H UNCLEAR (timeframes disagree (1D UNCLEAR, 4H WEAK_BEAR, 1H UNCLEAR)); volatility normal (higher than 58% of the last year); usual 24h move ±1.1%, 8 of 10 similar days within ±2.4%; crowding neutral (funding +0.0092%/8h, OI -0.6% 24h)
- ETH: daily price trend DOWN · -16.0% in 30 days; 1D TRANSITION / 4H STRONG_BEAR / 1H UNCLEAR (timeframes disagree (1D TRANSITION, 4H STRONG_BEAR, 1H UNCLEAR)); volatility normal (higher than 65% of the last year); usual 24h move ±1.8%, 8 of 10 similar days within ±3.9%; crowding neutral (funding +0.0033%/8h, OI -1.3% 24h)
- SOL: daily price trend DOWN · -21.3% in 30 days · lower highs and lower lows; 1D WEAK_BEAR / 4H STRONG_BEAR / 1H TRANSITION (1D/4H bearish, 1W UNCLEAR); volatility normal (higher than 67% of the last year); usual 24h move ±2.2%, 8 of 10 similar days within ±4.6%; crowding neutral (funding +0.0042%/8h, OI -0.4% 24h)
- XRP: daily price trend DOWN · -21.6% in 30 days · lower highs and lower lows; 1D WEAK_BEAR / 4H STRONG_BEAR / 1H UNCLEAR (1D/4H bearish, 1W UNCLEAR); volatility normal (higher than 73% of the last year); usual 24h move ±1.7%, 8 of 10 similar days within ±4.1%; crowding neutral (funding +0.0100%/8h, OI +6.7% 24h)
- ZEC: daily price trend DOWN · -17.4% in 30 days; 1D RANGE / 4H STRONG_BEAR / 1H WEAK_BEAR (weekly veto: 1W STRONG_BULL against 4H/1H bearish); volatility high (higher than 85% of the last year); usual 24h move ±3.4%, 8 of 10 similar days within ±8.2%; crowding neutral (funding +0.0071%/8h, OI +1.8% 24h)
- altcoins vs BTC (24h, median): +0.0%
- BTC dominance (CoinGecko): 60.50%, 24h +0.68 pt, 7d +0.42 pt - BTC down + BTC.D up: flight to BTC - careful with altcoin longs
- Explains the market. It never creates a signal and never changes a rule, a size or an approval.
