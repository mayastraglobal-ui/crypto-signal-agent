# Crypto Signal Report

**Updated:** 2026-09-25 04:19 Beijing time (2026-09-24 20:19 UTC) · data: Binance · 8 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.06% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| PROVE | **DEGRADED** | 1d: DEGRADED: volume 52x normal on candle 09-23 00:00 UTC (possible bad data) |
- 59 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **ZEC**, **XRP**, **SOL**, **BNB**, **UNI**
- **Research only** - backtested, never a signal: SUI

| Not eligible | 24h volume | Why |
|---|---|---|
| PROVE | $179M | 7-day average volume $36M < $50M; order book too thin: $65k within 1% (need $250k) |
| LTC | $147M | 7-day average volume $34M < $50M |
| ONDO | $113M | 7-day average volume $30M < $50M; suspended for the rest of the UTC day (moved more than ±25% earlier today); order book too thin: $188k within 1% (need $250k) |

**Flags (not excluded):** PROVE: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, PEPE, RLUSD, USD1, USDC (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 475 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2017-08 | OK (300 candles) |
| ETH | 475 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2017-08 | OK (300 candles) |
| ZEC | 392 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2019-03 | OK (300 candles) |
| XRP | 438 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2018-04 | OK (300 candles) |
| SOL | 319 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2020-08 | OK (300 candles) |
| BNB | 463 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2017-11 | OK (300 candles) |
| UNI | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2020-09 | OK (300 candles) |
| SUI | 177 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2023-05 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (HH/LL) | 84,942.4 / 82,874.9 | 0.32 | 0.79x | 1.13x | - |
| ETH | mixed (HH/LL) | 2,706 / 2,600.15 | 0.77 | 1.46x | 1.16x | bull_engulf |
| ZEC | mixed (HH/LL) | 1,539.7 / 1,456.92 | 0.31 | 0.84x | 1.13x | bear_reject, retest_up |
| XRP | mixed (HH/LL) | 1.5194 / 1.4517 | 0.24 | 0.58x | 1.00x | retest_up |
| SOL | mixed (HH/LL) | 117.79 / 112.52 | 0.33 | 0.94x | 1.05x | bull_engulf, retest_up |
| BNB | mixed (HH/LL) | 786.29 / 763.04 | 0.25 | 0.55x | 0.95x | bull_engulf, bear_engulf |
| UNI | down (LH/LL) | 9.401 / 8.787 | 0.86 | 0.43x | 0.91x | bear_engulf |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 375 | 47% | 34% | 27% | 79% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | displacement_down | 308 | 49% | 32% | 22% | 75% | 46% | 32% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 979 | 44% | 30% | 20% | 78% | 43% | 30% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1100 | 44% | 30% | 21% | 76% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | bull_reject | 734 | 41% | 28% | 19% | 79% | 43% | 29% | can't tell from chance | 0.13R |
| 4h | bear_reject | 718 | 48% | 34% | 24% | 73% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 529 | 43% | 29% | 21% | 77% | 42% | 29% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 528 | 44% | 29% | 18% | 81% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 228 | 44% | 29% | 21% | 81% | 44% | 31% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 201 | 51% | 38% | 28% | 68% | 49% | 32% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 68 | 51% | 35% | 28% | 81% | 42% | 28% | can't tell from chance | 0.14R |
| 4h | smc_choch_down | 63 | 43% | 24% | 13% | 78% | 50% | 35% | can't tell from chance | 0.09R |
| 4h | smc_fvg_retrace_bull | 524 | 44% | 28% | 22% | 77% | 42% | 29% | can't tell from chance | 0.13R |
| 4h | smc_fvg_retrace_bear | 535 | 49% | 32% | 21% | 74% | 48% | 33% | can't tell from chance | 0.08R |
| 1h | displacement_up | 502 | 47% | 35% | 27% | 72% | 42% | 29% | beats chance | 0.29R |
| 1h | displacement_down | 343 | 38% | 24% | 15% | 83% | 39% | 25% | can't tell from chance | 0.20R |
| 1h | bull_engulf | 1366 | 40% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.34R |
| 1h | bear_engulf | 1527 | 39% | 25% | 18% | 79% | 37% | 24% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1147 | 40% | 28% | 21% | 75% | 42% | 29% | can't tell from chance | 0.33R |
| 1h | bear_reject | 1064 | 35% | 23% | 17% | 83% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_sweep_bull | 491 | 41% | 27% | 19% | 77% | 42% | 29% | can't tell from chance | 0.33R |
| 1h | smc_sweep_bear | 564 | 35% | 23% | 15% | 81% | 38% | 24% | can't tell from chance | 0.20R |
| 1h | smc_bos_up | 333 | 43% | 30% | 23% | 79% | 44% | 30% | can't tell from chance | 0.28R |
| 1h | smc_bos_down | 219 | 39% | 28% | 19% | 82% | 39% | 26% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 97 | 48% | 37% | 30% | 71% | 42% | 30% | can't tell from chance | 0.34R |
| 1h | smc_choch_down | 96 | 45% | 28% | 16% | 77% | 38% | 26% | can't tell from chance | 0.18R |
| 1h | smc_fvg_retrace_bull | 719 | 45% | 33% | 25% | 71% | 41% | 29% | can't tell from chance | 0.32R |
| 1h | smc_fvg_retrace_bear | 652 | 40% | 27% | 18% | 80% | 38% | 25% | can't tell from chance | 0.21R |
| 30m | displacement_up | 495 | 41% | 31% | 26% | 76% | 40% | 28% | can't tell from chance | 0.35R |
| 30m | displacement_down | 323 | 40% | 24% | 14% | 83% | 35% | 21% | can't tell from chance | 0.22R |
| 30m | bull_engulf | 1400 | 40% | 28% | 20% | 76% | 40% | 28% | can't tell from chance | 0.39R |
| 30m | bear_engulf | 1455 | 35% | 22% | 15% | 82% | 35% | 21% | can't tell from chance | 0.24R |
| 30m | bull_reject | 1078 | 43% | 28% | 21% | 74% | 40% | 28% | can't tell from chance | 0.37R |
| 30m | bear_reject | 1136 | 37% | 23% | 16% | 81% | 36% | 21% | can't tell from chance | 0.23R |
| 30m | smc_sweep_bull | 497 | 38% | 27% | 17% | 77% | 40% | 28% | can't tell from chance | 0.40R |
| 30m | smc_sweep_bear | 508 | 40% | 25% | 17% | 82% | 35% | 20% | beats chance | 0.23R |
| 30m | smc_bos_up | 377 | 42% | 34% | 29% | 75% | 41% | 28% | can't tell from chance | 0.34R |
| 30m | smc_bos_down | 191 | 34% | 23% | 14% | 85% | 36% | 21% | can't tell from chance | 0.26R |
| 30m | smc_choch_up | 77 | 35% | 21% | 16% | 82% | 42% | 29% | can't tell from chance | 0.42R |
| 30m | smc_choch_down | 75 | 41% | 25% | 19% | 79% | 35% | 21% | can't tell from chance | 0.21R |
| 30m | smc_fvg_retrace_bull | 787 | 42% | 29% | 22% | 74% | 40% | 28% | can't tell from chance | 0.40R |
| 30m | smc_fvg_retrace_bear | 641 | 36% | 21% | 16% | 81% | 35% | 21% | can't tell from chance | 0.26R |
| 15m | displacement_up | 372 | 35% | 26% | 20% | 82% | 34% | 23% | can't tell from chance | 0.47R |
| 15m | displacement_down | 365 | 35% | 21% | 14% | 84% | 34% | 21% | can't tell from chance | 0.33R |
| 15m | bull_engulf | 1328 | 35% | 25% | 17% | 79% | 34% | 23% | can't tell from chance | 0.58R |
| 15m | bear_engulf | 1308 | 35% | 24% | 15% | 79% | 35% | 22% | can't tell from chance | 0.34R |
| 15m | bull_reject | 1079 | 34% | 23% | 16% | 80% | 34% | 24% | can't tell from chance | 0.58R |
| 15m | bear_reject | 1166 | 35% | 22% | 15% | 81% | 35% | 22% | can't tell from chance | 0.33R |
| 15m | smc_sweep_bull | 484 | 36% | 25% | 20% | 79% | 35% | 24% | can't tell from chance | 0.52R |
| 15m | smc_sweep_bear | 498 | 36% | 24% | 14% | 83% | 36% | 22% | can't tell from chance | 0.32R |
| 15m | smc_bos_up | 270 | 42% | 29% | 22% | 79% | 34% | 25% | beats chance | 0.46R |
| 15m | smc_bos_down | 288 | 34% | 20% | 14% | 86% | 35% | 22% | can't tell from chance | 0.37R |
| 15m | smc_choch_up | 73 | 29% | 18% | 11% | 88% | 36% | 25% | can't tell from chance | 0.54R |
| 15m | smc_choch_down | 77 | 31% | 19% | 13% | 81% | 37% | 25% | can't tell from chance | 0.30R |
| 15m | smc_fvg_retrace_bull | 826 | 30% | 21% | 15% | 82% | 34% | 24% | can't tell from chance | 0.55R |
| 15m | smc_fvg_retrace_bear | 766 | 35% | 24% | 16% | 79% | 34% | 22% | can't tell from chance | 0.36R |
| 5m | displacement_up | 418 | 33% | 22% | 18% | 84% | 30% | 22% | can't tell from chance | 0.81R |
| 5m | displacement_down | 339 | 28% | 17% | 12% | 86% | 31% | 20% | can't tell from chance | 0.44R |
| 5m | bull_engulf | 1361 | 30% | 21% | 16% | 81% | 31% | 22% | can't tell from chance | 0.81R |
| 5m | bear_engulf | 1298 | 31% | 19% | 12% | 84% | 29% | 18% | can't tell from chance | 0.49R |
| 5m | bull_reject | 1016 | 31% | 23% | 17% | 77% | 30% | 21% | can't tell from chance | 0.82R |
| 5m | bear_reject | 1162 | 34% | 21% | 13% | 81% | 30% | 18% | beats chance | 0.49R |
| 5m | smc_sweep_bull | 382 | 34% | 24% | 16% | 75% | 31% | 22% | can't tell from chance | 0.70R |
| 5m | smc_sweep_bear | 415 | 36% | 24% | 16% | 80% | 32% | 20% | can't tell from chance | 0.41R |
| 5m | smc_bos_up | 325 | 32% | 25% | 20% | 82% | 31% | 23% | can't tell from chance | 0.85R |
| 5m | smc_bos_down | 217 | 32% | 20% | 12% | 83% | 31% | 19% | can't tell from chance | 0.42R |
| 5m | smc_choch_up | 60 | 33% | 25% | 17% | 87% | 31% | 22% | can't tell from chance | 0.87R |
| 5m | smc_choch_down | 63 | 22% | 8% | 3% | 90% | 30% | 18% | can't tell from chance | 0.52R |
| 5m | smc_fvg_retrace_bull | 1045 | 33% | 23% | 17% | 79% | 30% | 22% | beats chance | 0.81R |
| 5m | smc_fvg_retrace_bear | 827 | 27% | 17% | 11% | 84% | 30% | 18% | can't tell from chance | 0.51R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (weak) | TRANSITION (strong) | TRANSITION (moderate) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)) |
| **ETH** | UNCLEAR (weak) | WEAK_BULL (weak) | TRANSITION (moderate) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H UNCLEAR)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | UNCLEAR (weak) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | WEAK_BULL (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BULL, 1H UNCLEAR)) |
| **SOL** | TRANSITION (weak) | TRANSITION (strong) | TRANSITION (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | UNCLEAR (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H UNCLEAR)) |
| **UNI** | EXPANSION up (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | RANGE (weak) | LONG allowed (1D/4H bullish, 1W EXPANSION) |
| **SUI** | RANGE (weak) | EXPANSION up (weak) | TRANSITION (moderate) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D EXPANSION, 4H TRANSITION, 1H TRANSITION)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (weak)** - for: EMA-fast rising (+1.1 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.72x normal, Bollinger width above 52% of the last 100 candles · against: EMAs not lined up; ADX 27 is close to a threshold
- **1D TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.0 ATR in 10 candles); swing structure down (LH/LL); ADX 45 = strong trend; candle size 1.18x normal, Bollinger width above 78% of the last 100 candles · against: -
- **4H TRANSITION (moderate)** - for: close above EMA-fast above EMA-slow; swing structure down (LH/LL); ADX 32 = strong trend; candle size 1.28x normal, Bollinger width above 56% of the last 100 candles · against: EMA-fast flat (+0.9 ATR in 10 candles)
- **1H TRANSITION (weak)** - for: ADX 27 = strong trend; candle size 1.13x normal, Bollinger width above 29% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.3 ATR in 10 candles); swing structure mixed; ADX 27 is close to a threshold

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (CHOCH 47 candles ago) | buy-side (bearish idea) 31 candles ago | bear 84,886.92-85,550.30 (retraced) | bear 86,133.40-86,975.51 | premium (74%) | swing high 84,942.45 (0.85 ATR) | swing low 82,874.93 (2.46 ATR) |
| **ETH** | down (BOS 47 candles ago) | buy-side (bearish idea) 14 candles ago | bull 2,675.72-2,679.23 | bear 2,745.99-2,784.40 | premium (91%) | equal highs 2,706.00 (0.34 ATR) | swing low 2,600.15 (3.66 ATR) |
| **ZEC** | up (CHOCH 15 candles ago) | buy-side (bearish idea) 15 candles ago | bull 1,517.23-1,526.13 | bull 1,098.88-1,133.82 | above the range (119%) | swing high 1,679.83 (3.89 ATR) | swing low 1,456.92 (3.11 ATR) |
| **XRP** | up (BOS 15 candles ago) | buy-side (bearish idea) 13 candles ago | bull 1.5156-1.5195 (retraced) | bull 1.3773-1.3856 | above the range (113%) | swing high 1.6581 (5.69 ATR) | swing low 1.4517 (3.36 ATR) |
| **SOL** | up (BOS 15 candles ago) | buy-side (bearish idea) 14 candles ago | bull 115.10-115.59 | bear 117.85-119.66 | premium (91%) | swing high 117.79 (0.38 ATR) | swing low 112.52 (3.74 ATR) |
| **BNB** | up (BOS 15 candles ago) | buy-side (bearish idea) 26 candles ago | bear 781.33-782.43 (retraced) | bear 787.07-797.61 | premium (72%) | swing high 786.29 (1.16 ATR) | equal lows 763.04 (2.93 ATR) |
| **UNI** | down (BOS 47 candles ago) | sell-side (bullish idea) 42 candles ago | bull 8.9510-9.0010 (retraced) | bull 8.6780-9.0640 | premium (90%) | swing high 9.4010 (0.32 ATR) | swing low 8.7870 (2.78 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 71 (Greed), yesterday 71  (extreme fear/greed = bigger, faster moves)

## 2. Signals right now
Only **APPROVED** strategy versions (your yes, after paper trading) give signals and emails.

**No trade passes all the checks right now. That is normal - no trade is also a position.**

## 3. Strategy scoreboard (auto backtest, after fees)
**VALIDATION** = passed the backtest gate: ≥ 30 trades, ≥ +0.10R per trade (+0.02R for every re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the train and the unseen-test part · **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing. Only trades inside each strategy's allowed regimes and with timeframe permission are counted; **Stood down** = signal candles blocked by the regime / permission gate · **Skipped** = setups with no valid stop (missing, or wider than the strategy allows) / no valid target (e.g. next pool closer than 2R).

| Strategy | Ver | TF | Status | Trades | Win % | Avg R/trade | PF | Max DD | Train R | Unseen-test R | Avg hold | Stood down (regime / permission) | Skipped (stop / target) | Live signals (avg R) | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian_breakout | 1.0 | 1h | **VALIDATION** | 84 | 54.8 | +0.225 | 1.48 | 5.8R | +0.180 | +0.276 | 11.2 h | 100 / 73 of 322 | 0 / 0 | 0 |  |
| donchian_breakout | 1.0 | 4h | **VALIDATION** | 49 | 53.1 | +0.169 | 1.37 | 5.3R | +0.171 | +0.168 | 39.0 h | 73 / 44 of 209 | 0 / 0 | 0 |  |
| macd_trend_cross | 1.0 | 1h | **BACKTESTING** | 2 | 50.0 | +0.573 | 70.76 | 0.0R | +1.163 | -0.016 | 17.5 h | 166 / 3 of 171 | 0 / 0 | 0 | only 2 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **BACKTESTING** | 2 | 50.0 | +0.364 | 1.67 | 1.1R | +0.000 | +0.364 | 50.0 h | 32 / 7 of 41 | 0 / 0 | 0 | only 2 trades; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 2 | 50.0 | +0.307 | 1.46 | 1.3R | +0.000 | +0.307 | 5.0 h | 39 / 22 of 67 | 3 / 1 | 0 | only 2 trades; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **BACKTESTING** | 7 | 57.1 | +0.295 | 1.6 | 1.3R | -1.057 | +0.520 | 14.1 h | 48 / 1 of 56 | 0 / 0 | 0 | only 7 trades; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **BACKTESTING** | 24 | 41.7 | +0.173 | 1.22 | 5.9R | +0.927 | -0.466 | 13.3 h | 393 / 924 of 1394 | 0 / 46 | 0 | only 24 trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **BACKTESTING** | 21 | 57.1 | +0.162 | 1.34 | 5.0R | +0.043 | +0.236 | 6.9 h | 111 / 33 of 171 | 0 / 0 | 0 | only 21 trades |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 2 | 50.0 | +0.049 | 1.09 | 1.1R | +0.049 | +0.000 | 5.1 h | 390 / 177 of 677 | 86 / 21 | 0 | only 2 trades; avg +0.05R/trade (needs +0.10R); profit factor 1.09; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **BACKTESTING** | 194 | 54.1 | +0.013 | 1.02 | 13.4R | -0.067 | +0.187 | 5.2 h | 661 / 175 of 1360 | 0 / 0 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.02; max drawdown 13.4R; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.000 | +0.000 | - | 46 / 9 of 58 | 2 / 1 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.000 | +0.000 | - | 428 / 178 of 774 | 140 / 28 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.000 | +0.000 | - | 2 / 3 of 5 | 0 / 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.000 | +0.000 | - | 21 / 10 of 32 | 0 / 1 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **BACKTESTING** | 24 | 62.5 | -0.014 | 0.97 | 3.5R | -0.065 | +0.047 | 2.1 h | 52 / 11 of 87 | 0 / 0 | 0 | only 24 trades; avg -0.01R/trade (needs +0.10R); profit factor 0.97; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **BACKTESTING** | 7 | 42.9 | -0.128 | 0.79 | 3.0R | -0.094 | -0.154 | 18.3 h | 86 / 20 of 116 | 0 / 0 | 0 | only 7 trades; avg -0.13R/trade (needs +0.10R); profit factor 0.79; only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **BACKTESTING** | 11 | 36.4 | -0.247 | 0.6 | 4.8R | -1.022 | +0.195 | 2.5 h | 87 / 14 of 112 | 0 / 0 | 0 | only 11 trades; avg -0.25R/trade (needs +0.10R); profit factor 0.60; only 7 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **BACKTESTING** | 28 | 35.7 | -0.266 | 0.71 | 11.5R | -0.903 | +0.146 | 5.8 h | 356 / 818 of 1325 | 1 / 104 | 0 | only 28 trades; avg -0.27R/trade (needs +0.10R); profit factor 0.71; max drawdown 11.5R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 6 | 33.3 | -0.266 | 0.59 | 3.4R | +0.155 | -0.477 | 5.8 h | 94 / 27 of 134 | 7 / 0 | 0 | only 6 trades; avg -0.27R/trade (needs +0.10R); profit factor 0.59; only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **BACKTESTING** | 9 | 33.3 | -0.285 | 0.55 | 3.2R | +0.631 | -0.743 | 4.9 h | 45 / 5 of 59 | 0 / 0 | 0 | only 9 trades; avg -0.28R/trade (needs +0.10R); profit factor 0.55; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **BACKTESTING** | 15 | 46.7 | -0.407 | 0.38 | 6.1R | -0.566 | +0.229 | 6.6 h | 139 / 8 of 162 | 0 / 0 | 0 | only 15 trades; avg -0.41R/trade (needs +0.10R); profit factor 0.38; only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **BACKTESTING** | 20 | 30.0 | -0.619 | 0.16 | 13.0R | -0.532 | -0.748 | 3.5 h | 91 / 162 of 273 | 0 / 0 | 0 | only 20 trades; avg -0.62R/trade (needs +0.10R); profit factor 0.16; max drawdown 13.0R; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **BACKTESTING** | 7 | 28.6 | -0.638 | 0.28 | 5.0R | -1.100 | -0.562 | 10.9 h | 86 / 163 of 256 | 0 / 0 | 0 | only 7 trades; avg -0.64R/trade (needs +0.10R); profit factor 0.28; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **BACKTESTING** | 7 | 14.3 | -0.829 | 0.05 | 5.8R | -0.985 | -0.767 | 4.9 h | 117 / 5 of 129 | 0 / 0 | 0 | only 7 trades; avg -0.83R/trade (needs +0.10R); profit factor 0.05; only 5 unseen-test trades; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **BACKTESTING** | 2 | 0.0 | -1.040 | 0.0 | 2.1R | -1.040 | +0.000 | 28.0 h | 125 / 5 of 132 | 0 / 0 | 0 | only 2 trades; avg -1.04R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **BACKTESTING** | 7 | 14.3 | -1.196 | 0.03 | 8.7R | -1.177 | -1.245 | 5.3 h | 26 / 82 of 116 | 0 / 0 | 0 | only 7 trades; avg -1.20R/trade (needs +0.10R); profit factor 0.03; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 1 | 0.0 | -1.323 | 0.0 | 1.3R | +0.000 | -1.323 | 5.5 h | 30 / 10 of 46 | 4 / 1 | 0 | only 1 trades; avg -1.32R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **BACKTESTING** | 5 | 0.0 | -1.410 | 0.0 | 7.1R | -1.327 | -1.466 | 7.2 h | 73 / 179 of 260 | 0 / 1 | 0 | only 5 trades; avg -1.41R/trade (needs +0.10R); profit factor 0.00; only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 111 | 57.7 | +0.194 | 1.41 | 7.6R | +0.299 | -0.017 | 5.2 h | 119 / 39 of 369 | 0 / 0 | 0 | not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 127 | 54.3 | -0.113 | 0.6 | 15.9R | -0.054 | -0.218 | 13.3 h | 616 / 3 of 831 | 0 / 0 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.60; max drawdown 15.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 155 | 49.0 | -0.119 | 0.81 | 21.6R | -0.104 | -0.127 | 2.4 h | 1065 / 241 of 1817 | 0 / 0 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.81; max drawdown 21.6R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 90 | 47.8 | -0.197 | 0.42 | 19.2R | -0.241 | -0.020 | 91 min | 835 / 20 of 996 | 0 / 0 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.42; max drawdown 19.2R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 71 | 33.8 | -0.224 | 0.31 | 15.9R | -0.247 | +0.030 | 48 min | 982 / 35 of 1136 | 0 / 0 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.31; max drawdown 15.9R; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 30 | 46.7 | -0.253 | 0.59 | 9.7R | -0.235 | -0.280 | 2.9 h | 102 / 21 of 162 | 0 / 0 | 0 | avg -0.25R/trade (needs +0.10R); profit factor 0.59; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 148 | 41.9 | -0.275 | 0.59 | 41.8R | -0.380 | -0.135 | 10.6 h | 965 / 241 of 1507 | 0 / 0 | 0 | avg -0.28R/trade (needs +0.10R); profit factor 0.59; max drawdown 41.8R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 169 | 33.1 | -0.333 | 0.2 | 56.3R | -0.352 | -0.284 | 3.6 h | 853 / 3 of 1141 | 0 / 0 | 0 | avg -0.33R/trade (needs +0.10R); profit factor 0.20; max drawdown 56.3R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 64 | 39.1 | -0.373 | 0.43 | 24.5R | -0.550 | -0.195 | 47.3 h | 499 / 166 of 800 | 0 / 0 | 0 | avg -0.37R/trade (needs +0.10R); profit factor 0.43; max drawdown 24.5R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 30 | 33.3 | -0.548 | 0.37 | 18.3R | -0.286 | -0.660 | 96 min | 86 / 185 of 301 | 0 / 0 | 0 | avg -0.55R/trade (needs +0.10R); profit factor 0.37; max drawdown 18.3R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 39 | 28.2 | -0.640 | 0.3 | 27.8R | -0.019 | -1.073 | 87 min | 86 / 33 of 173 | 0 / 0 | 0 | avg -0.64R/trade (needs +0.10R); profit factor 0.30; max drawdown 27.8R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 30 | 23.3 | -0.931 | 0.18 | 27.9R | -0.905 | -1.034 | 42 min | 30 / 12 of 72 | 0 / 0 | 0 | avg -0.93R/trade (needs +0.10R); profit factor 0.18; max drawdown 27.9R; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 78 | 16.7 | -1.337 | 0.1 | 107.1R | -1.623 | -0.798 | 26 min | 40 / 197 of 315 | 0 / 0 | 0 | avg -1.34R/trade (needs +0.10R); profit factor 0.10; max drawdown 107.1R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING → APPROVED (your yes). PAPER_TRADING needs the Phase 8 tests (walk-forward, costs +50%, ±20% parameters, beating the control twin), so no strategy can get there yet. Strategy versions tested so far: **16** (`memory/experiments.md`).

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins out of sample):

| Strategy | TF | Trades | Avg R | Unseen-test R | Twin avg R | Twin unseen-test R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S5-SWEEP-MSS-FVG | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.266 | -0.477 | too few trades to compare |
| S7-SILVER-BULLET | 15m | 0 | +0.000 | +0.000 | +0.307 | +0.307 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 30m | 7 | -1.196 | -1.245 | -0.266 | +0.146 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 1 | -1.323 | -1.323 | +0.049 | +0.000 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 5 | -1.410 | -1.466 | +0.173 | -0.466 | too few trades to compare |

**Status changes this run** (all of them in `memory/strategy_lifecycle.md`): S5-SWEEP-MSS-FVG@1.0 15m FORMALIZED → BACKTESTING; S5-SWEEP-MSS-FVG@1.0 30m FORMALIZED → BACKTESTING; S5-SWEEP-MSS-FVG-noSMC@1.0 15m FORMALIZED → BACKTESTING; S5-SWEEP-MSS-FVG-noSMC@1.0 30m FORMALIZED → BACKTESTING; S6-OB-FVG@1.0 15m FORMALIZED → BACKTESTING; S6-OB-FVG-noSMC@1.0 15m FORMALIZED → BACKTESTING; S7-SILVER-BULLET@1.0 15m FORMALIZED → BACKTESTING; S7-SILVER-BULLET-noSMC@1.0 15m FORMALIZED → BACKTESTING; S8-PDH-PDL-SWEEP@1.0 1h FORMALIZED → BACKTESTING; S8-PDH-PDL-SWEEP@1.0 30m FORMALIZED → BACKTESTING; S8-PDH-PDL-SWEEP-noSMC@1.0 1h FORMALIZED → BACKTESTING; S8-PDH-PDL-SWEEP-noSMC@1.0 30m FORMALIZED → BACKTESTING; ... and 29 more

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*