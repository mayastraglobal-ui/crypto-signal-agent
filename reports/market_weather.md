# Market weather

What kind of day it is, from the hourly scan's own numbers (engine/weather.py). Explains the market only: it never creates a signal or changes a rule.

- verdict (2026-11-23 18:11 UTC): **Downtrend - the strategies wait for a clean 4H / 1H** - BTC is falling on the daily chart (the price trend line below). The strategy filter is stricter: it trades a SHORT only when 4H and 1H both show a clean downtrend, because a grinding fall with bounces stops out early shorts. A SHORT alert comes once they agree.
- coins: BTC downtrend on the daily chart (not confirmed), ETH downtrend on the daily chart (not confirmed), SOL bounce in a downtrend (daily), SUI bounce in a downtrend (daily), XRP bounce in a downtrend (daily), ZEC downtrend on the daily chart (not confirmed)
- fits: no longs, no buying the dip; checking the stop of any open long; waiting for a SHORT alert - it often comes after a bounce fails · avoid: buying the dip (catching a falling knife); shorting by hand right after a big red candle, at the lows
- BTC: daily price trend DOWN · -24.5% in 30 days · lower highs and lower lows; 1D EXPANSION / 4H TRANSITION / 1H TRANSITION (timeframes disagree (1D EXPANSION, 4H TRANSITION, 1H TRANSITION)); volatility high (higher than 95% of the last year); usual 24h move ±1.6%, 8 of 10 similar days within ±3.4%; crowding neutral (funding +0.0033%/8h, OI -1.4% 24h)
- ETH: daily price trend DOWN · -27.8% in 30 days; 1D EXPANSION / 4H TRANSITION / 1H TRANSITION (timeframes disagree (1D EXPANSION, 4H TRANSITION, 1H TRANSITION)); volatility high (higher than 92% of the last year); usual 24h move ±2.1%, 8 of 10 similar days within ±4.2%; crowding neutral (funding +0.0020%/8h, OI +1.9% 24h)
- SOL: daily price trend DOWN · -31.2% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H TRANSITION / 1H TRANSITION (timeframes disagree (1D STRONG_BEAR, 4H TRANSITION, 1H TRANSITION)); volatility high (higher than 87% of the last year); usual 24h move ±2.4%, 8 of 10 similar days within ±4.7%; crowding neutral (funding +0.0008%/8h, OI +0.6% 24h)
- SUI: daily price trend DOWN · -31.7% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H TRANSITION / 1H TRANSITION (timeframes disagree (1D STRONG_BEAR, 4H TRANSITION, 1H TRANSITION)); volatility high (higher than 81% of the last year); usual 24h move ±2.9%, 8 of 10 similar days within ±5.6%; crowding neutral (funding -0.0034%/8h, OI +3.5% 24h)
- XRP: daily price trend DOWN · -28.3% in 30 days · lower highs and lower lows; 1D STRONG_BEAR / 4H UNCLEAR / 1H TRANSITION (timeframes disagree (1D STRONG_BEAR, 4H UNCLEAR, 1H TRANSITION)); volatility high (higher than 85% of the last year); usual 24h move ±1.9%, 8 of 10 similar days within ±4.5%; crowding neutral (funding +0.0037%/8h, OI -0.1% 24h)
- ZEC: daily price trend DOWN · -32.5% in 30 days · lower highs and lower lows; 1D TRANSITION / 4H TRANSITION / 1H TRANSITION (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)); volatility high (higher than 86% of the last year); usual 24h move ±3.4%, 8 of 10 similar days within ±8.1%; crowding neutral (funding +0.0063%/8h, OI +0.3% 24h)
- altcoins vs BTC (24h, median): +1.2%
- BTC dominance (CoinGecko): 57.92%, 24h -0.85 pt, 7d -0.70 pt - BTC up + BTC.D down: money rotating into altcoins (alt longs favored)
- event: US GDP (Second Estimate), 3rd Quarter 2026 2026-11-25 13:30 UTC
- event: US PCE / Personal Income and Outlays (Oct data) 2026-11-25 13:30 UTC
- warning: BTC's daily range is high (top 5% of the year): stops need room - the alerts' size at your fixed % risk already gets smaller when the stop is wider.
- Explains the market. It never creates a signal and never changes a rule, a size or an approval.
