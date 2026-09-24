# Crypto Signal Report

**Updated:** 2026-09-25 03:16 Beijing time (2026-09-24 19:16 UTC) · data: Binance · 8 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.04% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| PROVE | **DEGRADED** | 1d: DEGRADED: volume 52x normal on candle 09-23 00:00 UTC (possible bad data) |
- 59 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **ZEC**, **XRP**, **SOL**, **BNB**, **UNI**
- **Research only** - backtested, never a signal: SUI
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** ONDO - 7-day average volume $30M < $50M; 24h move +25.5% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $199k within 1% (need $250k)

| Not eligible | 24h volume | Why |
|---|---|---|
| PROVE | $180M | 7-day average volume $36M < $50M; order book too thin: $33k within 1% (need $250k) |
| LTC | $145M | 7-day average volume $34M < $50M |
| ONDO | $111M | 7-day average volume $30M < $50M; 24h move +25.5% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $199k within 1% (need $250k) |

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
| BTC | mixed (HH/LL) | 84,942.4 / 82,874.9 | 0.88 | 0.63x | 1.17x | - |
| ETH | mixed (HH/LL) | 2,704.08 / 2,600.15 | 0.87 | 1.20x | 1.19x | bull_engulf |
| ZEC | mixed (HH/LL) | 1,539.7 / 1,456.92 | 0.43 | 1.76x | 1.16x | breakout_up, retest_up |
| XRP | mixed (HH/LL) | 1.5194 / 1.4517 | 0.85 | 0.87x | 1.05x | breakout_up, retest_up |
| SOL | down (LH/LL) | 116.13 / 112.52 | 0.86 | 0.97x | 1.10x | bull_engulf, breakout_up, retest_up |
| BNB | mixed (HH/LL) | 777.62 / 763.04 | 0.93 | 0.52x | 0.98x | bull_engulf, bear_engulf |
| UNI | down (LH/LL) | 9.401 / 8.787 | 0.76 | 0.41x | 0.94x | bear_engulf |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 375 | 48% | 34% | 27% | 79% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | displacement_down | 308 | 49% | 32% | 22% | 75% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 979 | 44% | 30% | 20% | 78% | 43% | 29% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1099 | 44% | 30% | 21% | 76% | 48% | 33% | worse than chance | 0.09R |
| 4h | bull_reject | 734 | 41% | 28% | 19% | 79% | 43% | 29% | can't tell from chance | 0.13R |
| 4h | bear_reject | 717 | 48% | 34% | 24% | 73% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 529 | 43% | 29% | 21% | 77% | 43% | 29% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 528 | 44% | 29% | 18% | 81% | 48% | 33% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 228 | 44% | 29% | 21% | 81% | 45% | 31% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 201 | 51% | 39% | 28% | 68% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 68 | 51% | 35% | 28% | 81% | 42% | 30% | can't tell from chance | 0.14R |
| 4h | smc_choch_down | 63 | 43% | 24% | 13% | 78% | 49% | 34% | can't tell from chance | 0.09R |
| 4h | smc_fvg_retrace_bull | 523 | 44% | 28% | 22% | 77% | 43% | 29% | can't tell from chance | 0.13R |
| 4h | smc_fvg_retrace_bear | 535 | 48% | 32% | 21% | 74% | 48% | 33% | can't tell from chance | 0.08R |
| 1h | displacement_up | 503 | 47% | 35% | 27% | 72% | 42% | 29% | beats chance | 0.29R |
| 1h | displacement_down | 343 | 38% | 24% | 15% | 83% | 37% | 24% | can't tell from chance | 0.20R |
| 1h | bull_engulf | 1364 | 41% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.34R |
| 1h | bear_engulf | 1532 | 39% | 25% | 18% | 79% | 37% | 24% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1146 | 40% | 28% | 21% | 75% | 42% | 29% | can't tell from chance | 0.33R |
| 1h | bear_reject | 1064 | 35% | 23% | 17% | 83% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_sweep_bull | 489 | 41% | 27% | 19% | 77% | 42% | 29% | can't tell from chance | 0.33R |
| 1h | smc_sweep_bear | 564 | 35% | 23% | 15% | 81% | 38% | 25% | can't tell from chance | 0.20R |
| 1h | smc_bos_up | 333 | 43% | 30% | 23% | 79% | 43% | 30% | can't tell from chance | 0.28R |
| 1h | smc_bos_down | 219 | 39% | 28% | 19% | 82% | 38% | 26% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 97 | 48% | 37% | 30% | 71% | 43% | 30% | can't tell from chance | 0.34R |
| 1h | smc_choch_down | 96 | 45% | 28% | 16% | 77% | 36% | 25% | can't tell from chance | 0.18R |
| 1h | smc_fvg_retrace_bull | 719 | 45% | 33% | 25% | 71% | 42% | 29% | can't tell from chance | 0.32R |
| 1h | smc_fvg_retrace_bear | 652 | 40% | 27% | 18% | 80% | 38% | 25% | can't tell from chance | 0.21R |
| 30m | displacement_up | 496 | 41% | 31% | 26% | 76% | 42% | 29% | can't tell from chance | 0.35R |
| 30m | displacement_down | 323 | 40% | 24% | 14% | 83% | 36% | 21% | can't tell from chance | 0.22R |
| 30m | bull_engulf | 1402 | 40% | 28% | 20% | 76% | 40% | 28% | can't tell from chance | 0.39R |
| 30m | bear_engulf | 1455 | 35% | 22% | 15% | 82% | 36% | 21% | can't tell from chance | 0.24R |
| 30m | bull_reject | 1073 | 42% | 28% | 21% | 74% | 40% | 28% | can't tell from chance | 0.37R |
| 30m | bear_reject | 1136 | 37% | 23% | 16% | 81% | 36% | 21% | can't tell from chance | 0.23R |
| 30m | smc_sweep_bull | 497 | 38% | 27% | 17% | 77% | 40% | 28% | can't tell from chance | 0.40R |
| 30m | smc_sweep_bear | 508 | 40% | 25% | 17% | 82% | 36% | 21% | can't tell from chance | 0.23R |
| 30m | smc_bos_up | 378 | 42% | 34% | 29% | 75% | 41% | 29% | can't tell from chance | 0.34R |
| 30m | smc_bos_down | 188 | 34% | 23% | 14% | 85% | 37% | 22% | can't tell from chance | 0.26R |
| 30m | smc_choch_up | 78 | 35% | 21% | 15% | 82% | 39% | 28% | can't tell from chance | 0.42R |
| 30m | smc_choch_down | 76 | 41% | 25% | 18% | 79% | 35% | 20% | can't tell from chance | 0.22R |
| 30m | smc_fvg_retrace_bull | 786 | 42% | 29% | 22% | 74% | 41% | 29% | can't tell from chance | 0.40R |
| 30m | smc_fvg_retrace_bear | 644 | 36% | 22% | 16% | 80% | 35% | 21% | can't tell from chance | 0.26R |
| 15m | displacement_up | 372 | 35% | 26% | 20% | 82% | 34% | 24% | can't tell from chance | 0.47R |
| 15m | displacement_down | 366 | 35% | 21% | 14% | 84% | 36% | 23% | can't tell from chance | 0.33R |
| 15m | bull_engulf | 1328 | 36% | 25% | 17% | 79% | 34% | 23% | can't tell from chance | 0.58R |
| 15m | bear_engulf | 1307 | 36% | 24% | 16% | 79% | 35% | 22% | can't tell from chance | 0.34R |
| 15m | bull_reject | 1075 | 34% | 22% | 15% | 80% | 33% | 23% | can't tell from chance | 0.58R |
| 15m | bear_reject | 1166 | 35% | 22% | 15% | 81% | 36% | 22% | can't tell from chance | 0.33R |
| 15m | smc_sweep_bull | 485 | 36% | 25% | 20% | 79% | 34% | 23% | can't tell from chance | 0.52R |
| 15m | smc_sweep_bear | 499 | 36% | 24% | 14% | 83% | 36% | 23% | can't tell from chance | 0.32R |
| 15m | smc_bos_up | 270 | 42% | 29% | 22% | 79% | 34% | 24% | beats chance | 0.47R |
| 15m | smc_bos_down | 288 | 34% | 20% | 14% | 86% | 34% | 21% | can't tell from chance | 0.37R |
| 15m | smc_choch_up | 73 | 29% | 18% | 11% | 88% | 36% | 25% | can't tell from chance | 0.54R |
| 15m | smc_choch_down | 77 | 32% | 19% | 13% | 81% | 37% | 23% | can't tell from chance | 0.30R |
| 15m | smc_fvg_retrace_bull | 830 | 30% | 21% | 15% | 82% | 34% | 24% | worse than chance | 0.55R |
| 15m | smc_fvg_retrace_bear | 765 | 35% | 24% | 17% | 79% | 35% | 22% | can't tell from chance | 0.35R |
| 5m | displacement_up | 418 | 33% | 22% | 18% | 85% | 31% | 22% | can't tell from chance | 0.81R |
| 5m | displacement_down | 338 | 28% | 17% | 12% | 86% | 30% | 19% | can't tell from chance | 0.44R |
| 5m | bull_engulf | 1361 | 30% | 21% | 16% | 81% | 31% | 22% | can't tell from chance | 0.81R |
| 5m | bear_engulf | 1296 | 31% | 19% | 12% | 84% | 29% | 18% | can't tell from chance | 0.50R |
| 5m | bull_reject | 1010 | 32% | 23% | 18% | 77% | 30% | 22% | can't tell from chance | 0.83R |
| 5m | bear_reject | 1171 | 34% | 20% | 13% | 82% | 29% | 19% | beats chance | 0.49R |
| 5m | smc_sweep_bull | 383 | 34% | 25% | 16% | 75% | 31% | 22% | can't tell from chance | 0.70R |
| 5m | smc_sweep_bear | 416 | 36% | 24% | 16% | 81% | 31% | 20% | can't tell from chance | 0.42R |
| 5m | smc_bos_up | 309 | 32% | 25% | 20% | 83% | 32% | 22% | can't tell from chance | 0.83R |
| 5m | smc_bos_down | 224 | 31% | 20% | 12% | 83% | 31% | 20% | can't tell from chance | 0.46R |
| 5m | smc_choch_up | 63 | 33% | 24% | 16% | 87% | 29% | 20% | can't tell from chance | 0.91R |
| 5m | smc_choch_down | 62 | 23% | 8% | 3% | 90% | 28% | 18% | can't tell from chance | 0.51R |
| 5m | smc_fvg_retrace_bull | 1054 | 33% | 23% | 17% | 79% | 30% | 21% | beats chance | 0.82R |
| 5m | smc_fvg_retrace_bear | 833 | 27% | 17% | 11% | 84% | 29% | 18% | can't tell from chance | 0.52R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Shown only - regimes do not block signals yet (strategy spec v3, Phase 7).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (weak) | TRANSITION (strong) | TRANSITION (strong) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)) |
| **ETH** | UNCLEAR (weak) | WEAK_BULL (weak) | TRANSITION (moderate) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H UNCLEAR)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | RANGE (weak) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | WEAK_BULL (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BULL, 1H UNCLEAR)) |
| **SOL** | TRANSITION (weak) | TRANSITION (strong) | TRANSITION (moderate) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | UNCLEAR (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H UNCLEAR)) |
| **UNI** | EXPANSION up (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W EXPANSION) |
| **SUI** | RANGE (weak) | EXPANSION up (weak) | TRANSITION (moderate) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D EXPANSION, 4H TRANSITION, 1H TRANSITION)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (weak)** - for: EMA-fast rising (+1.1 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.72x normal, Bollinger width above 52% of the last 100 candles · against: EMAs not lined up; ADX 27 is close to a threshold
- **1D TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.0 ATR in 10 candles); swing structure down (LH/LL); ADX 45 = strong trend; candle size 1.18x normal, Bollinger width above 78% of the last 100 candles · against: -
- **4H TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.0 ATR in 10 candles); swing structure down (LH/LL); ADX 34 = strong trend; candle size 1.30x normal, Bollinger width above 55% of the last 100 candles · against: -
- **1H TRANSITION (weak)** - for: ADX 27 = strong trend; candle size 1.17x normal, Bollinger width above 27% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.4 ATR in 10 candles); swing structure mixed; ADX 27 is close to a threshold

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (CHOCH 43 candles ago) | buy-side (bearish idea) 27 candles ago | bear 84,886.92-85,550.30 (retraced) | bear 86,133.40-86,975.51 | premium (77%) | swing high 84,942.45 (0.72 ATR) | swing low 82,874.93 (2.48 ATR) |
| **ETH** | down (BOS 43 candles ago) | buy-side (bearish idea) 10 candles ago | bull 2,675.72-2,679.23 | bear 2,745.99-2,784.40 | premium (87%) | swing high 2,704.08 (0.52 ATR) | swing low 2,600.15 (3.32 ATR) |
| **ZEC** | up (CHOCH 11 candles ago) | buy-side (bearish idea) 11 candles ago | bull 1,517.23-1,526.13 | bull 1,098.88-1,133.82 | above the range (122%) | swing high 1,679.83 (3.76 ATR) | swing low 1,456.92 (3.11 ATR) |
| **XRP** | up (BOS 11 candles ago) | buy-side (bearish idea) 9 candles ago | bull 1.5156-1.5195 (retraced) | bull 1.3773-1.3856 | above the range (126%) | swing high 1.6581 (5.13 ATR) | swing low 1.4517 (3.62 ATR) |
| **SOL** | up (BOS 11 candles ago) | buy-side (bearish idea) 10 candles ago | bull 115.10-115.59 | bear 117.85-119.66 | above the range (135%) | swing high 119.77 (1.8 ATR) | swing low 112.52 (3.65 ATR) |
| **BNB** | up (BOS 11 candles ago) | buy-side (bearish idea) 22 candles ago | bear 781.33-782.43 (retraced) | bear 787.07-797.61 | above the range (128%) | swing high 799.00 (2.93 ATR) | equal lows 763.04 (3.17 ATR) |
| **UNI** | down (BOS 43 candles ago) | sell-side (bullish idea) 38 candles ago | bull 8.9510-9.0010 (retraced) | bull 8.6780-9.0640 | premium (77%) | swing high 9.4010 (0.69 ATR) | swing low 8.7870 (2.32 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 71 (Greed), yesterday 71  (extreme fear/greed = bigger, faster moves)

## 2. Signals right now
**No trade passes all the checks right now. That is normal - no trade is also a position.**

## 3. Strategy scoreboard (auto backtest)
WORKS = passed every test -> can give signals · WEAK = positive but not proven -> watch only · FAILS = ignored

| Strategy | TF | Status | Trades | Win % | Avg R/trade | PF | Train R | Unseen-test R | Avg hold | Live signals (avg R) | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bb_squeeze_breakout | 1h | **WEAK** | 109 | 57.8 | +0.013 | 1.02 | -0.044 | +0.161 | 8.9 h | 0 | avg +0.01R/trade; profit factor 1.02; not profitable in BOTH train and unseen test |
| donchian_breakout | 30m | **FAILS** | 197 | 53.8 | +0.083 | 1.16 | +0.205 | -0.138 | 4.9 h | 0 | not profitable in BOTH train and unseen test |
| donchian_breakout | 1h | **FAILS** | 184 | 50.5 | +0.004 | 1.01 | +0.017 | -0.020 | 11.5 h | 0 | avg +0.00R/trade; profit factor 1.01; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 4h | **FAILS** | 440 | 56.8 | -0.061 | 0.73 | -0.041 | -0.099 | 14.4 h | 0 | avg -0.06R/trade; profit factor 0.73; not profitable in BOTH train and unseen test |
| supertrend_flip | 1h | **FAILS** | 53 | 52.8 | -0.071 | 0.87 | -0.296 | +0.301 | 12.5 h | 0 | avg -0.07R/trade; profit factor 0.87; not profitable in BOTH train and unseen test |
| donchian_breakout | 4h | **FAILS** | 128 | 42.2 | -0.099 | 0.83 | -0.131 | -0.057 | 44.8 h | 0 | avg -0.10R/trade; profit factor 0.83; not profitable in BOTH train and unseen test |
| macd_trend_cross | 4h | **FAILS** | 124 | 42.7 | -0.144 | 0.77 | -0.238 | +0.032 | 40.8 h | 0 | avg -0.14R/trade; profit factor 0.77; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 30m | **FAILS** | 592 | 47.5 | -0.187 | 0.39 | -0.194 | -0.177 | 97 min | 0 | avg -0.19R/trade; profit factor 0.39; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 4h | **FAILS** | 83 | 45.8 | -0.188 | 0.68 | -0.157 | -0.235 | 36.0 h | 0 | avg -0.19R/trade; profit factor 0.68; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1h | **FAILS** | 620 | 44.4 | -0.206 | 0.36 | -0.208 | -0.201 | 3.5 h | 0 | avg -0.21R/trade; profit factor 0.36; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1h | **FAILS** | 159 | 46.5 | -0.220 | 0.66 | -0.227 | -0.206 | 10.7 h | 0 | avg -0.22R/trade; profit factor 0.66; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 15m | **FAILS** | 631 | 37.4 | -0.236 | 0.32 | -0.242 | -0.225 | 50 min | 0 | avg -0.24R/trade; profit factor 0.32; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 15m | **FAILS** | 87 | 47.1 | -0.236 | 0.61 | -0.242 | -0.222 | 2.4 h | 0 | avg -0.24R/trade; profit factor 0.61; not profitable in BOTH train and unseen test |
| trend_pullback | 4h | **FAILS** | 292 | 41.8 | -0.242 | 0.61 | -0.352 | -0.075 | 39.3 h | 0 | avg -0.24R/trade; profit factor 0.61; not profitable in BOTH train and unseen test |
| supertrend_flip | 30m | **FAILS** | 58 | 43.1 | -0.244 | 0.62 | -0.164 | -0.330 | 7.6 h | 0 | avg -0.24R/trade; profit factor 0.62; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 30m | **FAILS** | 110 | 40.0 | -0.245 | 0.62 | -0.332 | -0.093 | 4.0 h | 0 | avg -0.25R/trade; profit factor 0.62; not profitable in BOTH train and unseen test |
| trend_pullback | 30m | **FAILS** | 431 | 44.5 | -0.248 | 0.62 | -0.277 | -0.192 | 4.8 h | 0 | avg -0.25R/trade; profit factor 0.62; not profitable in BOTH train and unseen test |
| macd_trend_cross | 30m | **FAILS** | 145 | 46.9 | -0.263 | 0.58 | -0.244 | -0.305 | 6.0 h | 0 | avg -0.26R/trade; profit factor 0.58; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 30m | **FAILS** | 122 | 38.5 | -0.304 | 0.57 | -0.390 | -0.140 | 3.4 h | 0 | avg -0.30R/trade; profit factor 0.57; not profitable in BOTH train and unseen test |
| trend_pullback | 15m | **FAILS** | 546 | 44.5 | -0.328 | 0.53 | -0.359 | -0.267 | 2.3 h | 0 | avg -0.33R/trade; profit factor 0.53; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1h | **FAILS** | 124 | 39.5 | -0.331 | 0.51 | -0.370 | -0.261 | 9.0 h | 0 | avg -0.33R/trade; profit factor 0.51; not profitable in BOTH train and unseen test |
| supertrend_flip | 4h | **FAILS** | 41 | 39.0 | -0.332 | 0.49 | -0.356 | -0.266 | 73.8 h | 0 | avg -0.33R/trade; profit factor 0.49; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1h | **FAILS** | 251 | 40.2 | -0.343 | 0.51 | -0.269 | -0.485 | 5.5 h | 0 | avg -0.34R/trade; profit factor 0.51; not profitable in BOTH train and unseen test |
| trend_pullback | 1h | **FAILS** | 512 | 39.1 | -0.397 | 0.45 | -0.465 | -0.241 | 9.1 h | 0 | avg -0.40R/trade; profit factor 0.45; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 30m | **FAILS** | 270 | 38.9 | -0.398 | 0.45 | -0.326 | -0.561 | 2.6 h | 0 | avg -0.40R/trade; profit factor 0.45; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 15m | **FAILS** | 300 | 40.0 | -0.463 | 0.44 | -0.572 | -0.273 | 77 min | 0 | avg -0.46R/trade; profit factor 0.44; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 15m | **FAILS** | 132 | 36.4 | -0.512 | 0.37 | -0.367 | -0.802 | 87 min | 0 | avg -0.51R/trade; profit factor 0.37; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 5m | **FAILS** | 74 | 33.8 | -0.565 | 0.37 | -0.581 | -0.533 | 45 min | 0 | avg -0.56R/trade; profit factor 0.37; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 5m | **FAILS** | 305 | 28.5 | -0.852 | 0.23 | -0.941 | -0.671 | 25 min | 0 | avg -0.85R/trade; profit factor 0.23; not profitable in BOTH train and unseen test |

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*