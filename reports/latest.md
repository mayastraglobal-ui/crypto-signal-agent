# Crypto Signal Report

**Updated:** 2026-10-01 07:17 Beijing time (2026-09-30 23:17 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 8.2 MB (GitHub) · large files of this run 4.3 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-30 23:17 UTC / 2026-10-01 07:17 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US jobs report / Employment Situation (Sep data) 2026-10-02 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.04% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| QNT | **DEGRADED** | 1d: DEGRADED: volume 91x normal on candle 09-27 00:00 UTC (possible bad data); 1d: DEGRADED: volume 87x normal on candle 09-28 00:00 UTC (possible bad data); 1d: DEGRADED: volume 56x normal on candle 09-29 00:00 UTC (possible bad data) |
- 71 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-30 23:17 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 849 h since 2026-08-26 | +0.0037% | 1.37 | 1.20 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 849 h since 2026-08-26 | +0.0037% | 1.53 | 1.00 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 849 h since 2026-08-26 | +0.0041% | 1.80 | 1.24 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 849 h since 2026-08-26 | +0.0077% | 0.77 | 0.83 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 849 h since 2026-08-26 | +0.0075% | 2.93 | 1.28 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 849 h since 2026-08-26 | -0.0013% | 2.32 | 1.01 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| ENA | GOOD | okx | 849 h since 2026-08-26 | +0.0050% | 1.19 | 0.96 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ENAUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 849 h since 2026-08-26 | +0.0100% | 2.22 | 0.88 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| AVAX | GOOD | okx | 841 h since 2026-08-26 | -0.0051% | 2.02 | 0.59 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=AVAXUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 849 h since 2026-08-26 | +0.0100% | 1.88 | 1.01 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **ZEC**, **XRP**, **SUI**, **ENA**
- **Research only** - backtested, never a signal: BNB, AVAX, UNI

| Not eligible | 24h volume | Why |
|---|---|---|
| QNT | $201M | suspended for the rest of the UTC day (moved more than ±25% earlier today); order book too thin: $114k within 1% (need $250k) |
| MOVR | $56M | 7-day average volume $3M < $50M; 24h move +76.8% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $36k within 1% (need $250k) |
| PUMP | $56M | 7-day average volume $48M < $50M; order book too thin: $111k within 1% (need $250k) |

**Flags (not excluded):** QNT: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, RLUSD, USD1, USDC, WLD (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 476 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ETH | 476 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| SOL | 320 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| ZEC | 393 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| XRP | 439 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| SUI | 178 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| ENA | 130 | 911 | 905 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |
| BNB | 464 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| AVAX | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| UNI | 315 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | up (HH/HL) | 85,649.9 / 83,503.2 | 0.40 | 0.26x | 1.27x | - |
| ETH | mixed (HH/LL) | 2,738.51 / 2,667.94 | 0.61 | 0.33x | 1.11x | - |
| SOL | mixed (HH/LL) | 122.83 / 117.06 | 0.57 | 0.54x | 1.12x | failed_breakout_down |
| ZEC | up (HH/HL) | 1,494.52 / 1,409.42 | 0.86 | 0.66x | 1.19x | bull_engulf, bear_engulf |
| XRP | down (LH/LL) | 1.5443 / 1.4852 | 0.41 | 0.36x | 0.93x | bear_engulf |
| SUI | up (HH/HL) | 1.2124 / 1.1431 | 0.55 | 0.25x | 1.02x | bull_engulf |
| ENA | up (HH/HL) | 0.2811 / 0.2524 | 0.90 | 0.28x | 1.28x | bull_engulf |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 473 | 48% | 33% | 26% | 80% | 44% | 31% | can't tell from chance | 0.12R |
| 4h | displacement_down | 369 | 50% | 33% | 21% | 75% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1203 | 45% | 32% | 23% | 77% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | bear_engulf | 1366 | 43% | 28% | 19% | 78% | 47% | 31% | worse than chance | 0.08R |
| 4h | bull_reject | 925 | 42% | 29% | 20% | 79% | 44% | 30% | can't tell from chance | 0.12R |
| 4h | bear_reject | 894 | 46% | 31% | 21% | 74% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 650 | 44% | 30% | 22% | 76% | 44% | 30% | can't tell from chance | 0.12R |
| 4h | smc_sweep_bear | 681 | 44% | 29% | 19% | 79% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 280 | 45% | 28% | 21% | 82% | 45% | 32% | can't tell from chance | 0.13R |
| 4h | smc_bos_down | 239 | 47% | 33% | 21% | 72% | 48% | 33% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 89 | 49% | 31% | 26% | 83% | 44% | 31% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 89 | 44% | 29% | 18% | 74% | 49% | 33% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 674 | 44% | 28% | 21% | 78% | 44% | 31% | can't tell from chance | 0.12R |
| 4h | smc_fvg_retrace_bear | 686 | 47% | 31% | 20% | 76% | 47% | 31% | can't tell from chance | 0.08R |
| 1h | displacement_up | 616 | 45% | 34% | 27% | 73% | 43% | 30% | can't tell from chance | 0.26R |
| 1h | displacement_down | 435 | 37% | 24% | 15% | 82% | 39% | 26% | can't tell from chance | 0.18R |
| 1h | bull_engulf | 1716 | 39% | 28% | 22% | 76% | 42% | 29% | worse than chance | 0.31R |
| 1h | bear_engulf | 1858 | 39% | 25% | 17% | 79% | 38% | 25% | can't tell from chance | 0.19R |
| 1h | bull_reject | 1380 | 40% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.30R |
| 1h | bear_reject | 1366 | 37% | 25% | 18% | 80% | 39% | 25% | can't tell from chance | 0.17R |
| 1h | smc_sweep_bull | 643 | 42% | 27% | 20% | 77% | 41% | 29% | can't tell from chance | 0.29R |
| 1h | smc_sweep_bear | 722 | 39% | 25% | 16% | 80% | 39% | 25% | can't tell from chance | 0.18R |
| 1h | smc_bos_up | 400 | 44% | 32% | 25% | 77% | 43% | 29% | can't tell from chance | 0.25R |
| 1h | smc_bos_down | 275 | 39% | 28% | 19% | 83% | 39% | 25% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 112 | 46% | 35% | 30% | 72% | 43% | 29% | can't tell from chance | 0.32R |
| 1h | smc_choch_down | 112 | 42% | 29% | 20% | 74% | 39% | 26% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 901 | 44% | 31% | 24% | 73% | 42% | 30% | can't tell from chance | 0.28R |
| 1h | smc_fvg_retrace_bear | 817 | 40% | 28% | 19% | 79% | 39% | 26% | can't tell from chance | 0.19R |
| 30m | displacement_up | 571 | 39% | 28% | 22% | 81% | 42% | 28% | can't tell from chance | 0.27R |
| 30m | displacement_down | 433 | 43% | 26% | 15% | 81% | 38% | 23% | beats chance | 0.18R |
| 30m | bull_engulf | 1705 | 41% | 28% | 21% | 76% | 42% | 29% | can't tell from chance | 0.32R |
| 30m | bear_engulf | 1821 | 38% | 23% | 16% | 80% | 38% | 22% | can't tell from chance | 0.20R |
| 30m | bull_reject | 1341 | 45% | 29% | 21% | 75% | 42% | 29% | beats chance | 0.32R |
| 30m | bear_reject | 1451 | 38% | 23% | 16% | 80% | 37% | 23% | can't tell from chance | 0.19R |
| 30m | smc_sweep_bull | 651 | 40% | 27% | 18% | 76% | 42% | 29% | can't tell from chance | 0.33R |
| 30m | smc_sweep_bear | 634 | 43% | 27% | 18% | 80% | 37% | 22% | beats chance | 0.19R |
| 30m | smc_bos_up | 437 | 40% | 32% | 27% | 78% | 43% | 29% | can't tell from chance | 0.28R |
| 30m | smc_bos_down | 242 | 36% | 22% | 12% | 86% | 36% | 21% | can't tell from chance | 0.22R |
| 30m | smc_choch_up | 98 | 39% | 23% | 17% | 84% | 42% | 28% | can't tell from chance | 0.36R |
| 30m | smc_choch_down | 106 | 40% | 24% | 20% | 78% | 39% | 23% | can't tell from chance | 0.18R |
| 30m | smc_fvg_retrace_bull | 980 | 40% | 27% | 20% | 77% | 42% | 28% | can't tell from chance | 0.31R |
| 30m | smc_fvg_retrace_bear | 799 | 39% | 22% | 16% | 79% | 38% | 22% | can't tell from chance | 0.21R |
| 15m | displacement_up | 484 | 36% | 27% | 20% | 82% | 36% | 26% | can't tell from chance | 0.38R |
| 15m | displacement_down | 464 | 33% | 22% | 12% | 84% | 36% | 22% | can't tell from chance | 0.28R |
| 15m | bull_engulf | 1682 | 37% | 27% | 19% | 78% | 36% | 26% | can't tell from chance | 0.46R |
| 15m | bear_engulf | 1645 | 35% | 23% | 14% | 79% | 36% | 22% | can't tell from chance | 0.27R |
| 15m | bull_reject | 1279 | 37% | 26% | 18% | 79% | 36% | 25% | can't tell from chance | 0.47R |
| 15m | bear_reject | 1462 | 36% | 23% | 15% | 81% | 36% | 22% | can't tell from chance | 0.27R |
| 15m | smc_sweep_bull | 614 | 35% | 25% | 19% | 78% | 36% | 26% | can't tell from chance | 0.43R |
| 15m | smc_sweep_bear | 624 | 37% | 24% | 13% | 84% | 37% | 23% | can't tell from chance | 0.26R |
| 15m | smc_bos_up | 360 | 40% | 29% | 22% | 79% | 37% | 27% | can't tell from chance | 0.38R |
| 15m | smc_bos_down | 352 | 34% | 21% | 14% | 84% | 35% | 22% | can't tell from chance | 0.32R |
| 15m | smc_choch_up | 90 | 33% | 22% | 14% | 83% | 35% | 26% | can't tell from chance | 0.44R |
| 15m | smc_choch_down | 85 | 34% | 21% | 14% | 82% | 36% | 23% | can't tell from chance | 0.28R |
| 15m | smc_fvg_retrace_bull | 1085 | 35% | 25% | 17% | 79% | 36% | 25% | can't tell from chance | 0.46R |
| 15m | smc_fvg_retrace_bear | 963 | 35% | 24% | 16% | 81% | 36% | 23% | can't tell from chance | 0.30R |
| 5m | displacement_up | 1316 | 33% | 22% | 18% | 83% | 30% | 21% | can't tell from chance | 0.73R |
| 5m | displacement_down | 1161 | 27% | 17% | 11% | 87% | 31% | 20% | worse than chance | 0.44R |
| 5m | bull_engulf | 4219 | 29% | 21% | 15% | 81% | 30% | 21% | can't tell from chance | 0.78R |
| 5m | bear_engulf | 4168 | 31% | 20% | 12% | 83% | 31% | 20% | can't tell from chance | 0.48R |
| 5m | bull_reject | 3216 | 29% | 20% | 15% | 80% | 29% | 21% | can't tell from chance | 0.80R |
| 5m | bear_reject | 3701 | 33% | 21% | 14% | 82% | 32% | 21% | can't tell from chance | 0.44R |
| 5m | smc_sweep_bull | 1240 | 30% | 22% | 15% | 79% | 31% | 22% | can't tell from chance | 0.70R |
| 5m | smc_sweep_bear | 1277 | 35% | 24% | 16% | 81% | 32% | 21% | can't tell from chance | 0.41R |
| 5m | smc_bos_up | 916 | 32% | 24% | 19% | 82% | 30% | 21% | can't tell from chance | 0.76R |
| 5m | smc_bos_down | 802 | 28% | 17% | 11% | 87% | 31% | 21% | worse than chance | 0.51R |
| 5m | smc_choch_up | 230 | 35% | 26% | 19% | 84% | 29% | 20% | can't tell from chance | 0.82R |
| 5m | smc_choch_down | 236 | 26% | 16% | 10% | 87% | 32% | 21% | can't tell from chance | 0.51R |
| 5m | smc_fvg_retrace_bull | 3435 | 31% | 22% | 16% | 80% | 29% | 20% | beats chance | 0.80R |
| 5m | smc_fvg_retrace_bear | 2970 | 28% | 19% | 12% | 84% | 30% | 20% | worse than chance | 0.50R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (moderate) | WEAK_BULL (moderate) | WEAK_BULL (weak) | RANGE (weak) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (moderate) | RANGE (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H RANGE)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (moderate) | RANGE (strong) | RANGE (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H RANGE)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | UNCLEAR (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H RANGE)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | RANGE (strong) | RANGE (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H RANGE, 1H RANGE)) |
| **SUI** | UNCLEAR (weak) | EXPANSION down (weak) | UNCLEAR (weak) | WEAK_BULL (weak) | NO TRADE (timeframes disagree (1D EXPANSION, 4H UNCLEAR, 1H WEAK_BULL)) |
| **ENA** | TRANSITION (weak) | WEAK_BULL (weak) | TRANSITION (moderate) | WEAK_BULL (weak) | LONG allowed (1D/1H bullish, 1W TRANSITION) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (moderate) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H UNCLEAR)) |
| **AVAX** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (weak) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **UNI** | EXPANSION up (moderate) | STRONG_BULL (moderate) | UNCLEAR (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H RANGE)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (moderate)** - for: EMA-fast rising (+1.5 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.73x normal, Bollinger width above 56% of the last 100 candles · against: EMAs not lined up
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.5 ATR in 10 candles); ADX 42 = strong trend; candle size 1.03x normal, Bollinger width above 82% of the last 100 candles; volume 0.88x normal · against: swing structure mixed (neutral)
- **4H WEAK_BULL (weak)** - for: close above EMA-fast above EMA-slow; swing structure up (HH/HL); candle size 1.06x normal, Bollinger width above 16% of the last 100 candles; volume 1.37x normal · against: EMA-fast flat (+0.1 ATR in 10 candles) (neutral); ADX 12 = weak trend / ranging
- **1H RANGE (weak)** - for: EMAs not lined up; EMA-fast flat (+0.2 ATR in 10 candles); ADX 19 = weak trend / ranging; candle size 1.27x normal, Bollinger width above 83% of the last 100 candles · against: swing structure up (HH/HL); ADX 19 is close to a threshold

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | up (BOS 3 candles ago) | buy-side (bearish idea) 42 candles ago | bear 84,757.07-85,168.00 | bear 84,342.00-84,843.00 | discount (9%) | swing high 85,649.95 (3.99 ATR) | swing low 83,503.18 (0.37 ATR) |
| **ETH** | down (BOS 18 candles ago) | sell-side (bullish idea) 82 candles ago | bull 2,684.80-2,688.68 (retraced) | bull 2,652.20-2,695.38 | discount (27%) | swing high 2,738.51 (2.86 ATR) | equal lows 2,667.94 (1.06 ATR) |
| **SOL** | down (BOS 15 candles ago) | sell-side (bullish idea) 15 candles ago | bull 118.09-118.25 (retraced) | bull 115.86-117.34 | discount (19%) | swing high 122.83 (3.6 ATR) | swing low 117.06 (0.84 ATR) |
| **ZEC** | up (BOS 2 candles ago) | sell-side (bullish idea) 4 candles ago | bull 1,418.14-1,427.94 | bear 1,540.16-1,569.23 | discount (26%) | swing high 1,494.52 (2.18 ATR) | swing low 1,390.74 (1.42 ATR) |
| **XRP** | down (BOS 13 candles ago) | sell-side (bullish idea) 16 candles ago | bear 1.5059-1.5092 | bull 1.3773-1.3856 | discount (7%) | swing high 1.5443 (3.6 ATR) | equal lows 1.4852 (0.27 ATR) |
| **SUI** | up (BOS 2 candles ago) | sell-side (bullish idea) 13 candles ago | bull 1.1594-1.1677 (retraced) | bull 1.0050-1.0598 | discount (31%) | swing high 1.2124 (1.95 ATR) | swing low 1.1431 (0.88 ATR) |
| **ENA** | up (BOS 1 candles ago) | buy-side (bearish idea) 2 candles ago | bull 0.26410-0.26590 (retraced) | bull 0.16130-0.17050 | premium (53%) | swing high 0.28110 (1.87 ATR) | swing low 0.25240 (2.08 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 71 (Greed), yesterday 73  (extreme fear/greed = bigger, faster moves)

## 2. Signals right now
Only **APPROVED** strategy versions (your yes, after paper trading) give signals and emails.

**No trade passes all the checks right now. That is normal - no trade is also a position.**

### 2c. Watching - no signal yet (report only, never emailed)
No tracked strategy (VALIDATION or higher) has its market filters open right now.

### 2d. Risk engine (section 15 - independent of the strategies)
- **Live results:** today +0.00R (limit -3R), this week +0.00R (limit -6R) · **halts:** none
- **Suspended strategies** (live drawdown > 8R): none
- **Risk per trade:** 0.5% · leverage never above 3x (the position is made smaller instead)
- **Heat:** max 3 positions, 1 per coin, 1 per group of correlated coins and direction (1h correlation ≥ 0.7) · groups now: BTC+ETH+SOL+SUI+XRP
- **Every live entry also needs:** reward to TP1 ≥ 2R, no opposing level before TP1, no high-impact event within ±60 min, no duplicate
- **Event calendar (next 7 days):** US jobs report / Employment Situation (Sep data) 2026-10-02 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-09-30 00:55 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1104 | 39.5 | +0.169 | 1.31 | 31.9R | +0.16 / +0.19 | +0.21 / +0.12 | 5/5 | +0.14 | +0.11 | stable | 8 | 0.04R | 16, +0.74 (+0.86 / -1.03) | 92 / 47 of 267 | 0 | max drawdown 31.9R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1254 | 38.9 | +0.169 | 1.3 | 35.1R | +0.17 / +0.17 | +0.19 / +0.15 | 5/5 | +0.14 | +0.12 | stable | 9 | 0.04R | 17, +0.81 (+1.05 / -1.03) | 157 / 60 of 360 | 0 | max drawdown 35.1R |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1104 | 39.5 | +0.169 | 1.31 | 31.9R | +0.16 / +0.19 | +0.21 / +0.12 | 5/5 | +0.14 | +0.11 | stable | 8 | 0.04R | 16, +0.74 (+0.86 / -1.03) | 92 / 47 of 267 | 0 | max drawdown 31.9R |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 7 | 42.9 | +0.153 | 1.16 | 3.3R | +0.40 / -1.32 | -1.32 / +0.40 | 0/5 ✗ | -1.99 | -1.30 | ✗  stop buffer_atr 0.2→0.24: -1.78R | 0 | 0.27R | 1, -1.32 (-1.32 / +0.00) | 39 / 12 of 57 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 7 trades; profit factor 1.16; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1136 | 53.4 | +0.088 | 1.19 | 30.1R | +0.08 / +0.11 | +0.10 / +0.07 | 4/5 | +0.06 | +0.04 | stable | 6 | 0.04R | 18, +0.33 (+0.41 / -0.33) | 92 / 47 of 267 | 0 | avg +0.09R/trade (needs +0.10R); profit factor 1.19; max drawdown 30.1R |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.78 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.79 (+0.00 / +1.79) | 33 / 107 of 154 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 3 / 4 of 7 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 67 / 18 of 88 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 39 / 12 of 57 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 3 / 4 of 7 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 17 / 7 of 25 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 17 | 41.2 | -0.108 | 0.88 | 5.5R | -0.19 / +0.04 | -0.40 / +0.15 | 0/5 ✗ | -0.47 | -0.67 | ✗  sweep_bars 8→10: -0.33R | 0 | 0.39R | 2, +0.31 (+0.31 / +0.00) | 49 / 21 of 76 | 0 | not cost-viable: fees + slippage 0.39R per trade (stop must be ≥ 4x the round-trip cost); only 17 trades; avg -0.11R/trade (needs +0.10R); profit factor 0.88; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 15 | 46.7 | -0.196 | 0.65 | 4.3R | -0.15 / -0.37 | -0.37 / -0.11 | 0/5 ✗ | -0.18 | -0.37 | ✗  stop max_width_atr 3.0→3.6: -0.26R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 479 / 227 of 854 | 0 | only 15 trades; avg -0.20R/trade (needs +0.10R); profit factor 0.65; only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 14 | 35.7 | -0.235 | 0.57 | 3.9R | -0.31 / -0.11 | -0.24 / -0.23 | 0/5 ✗ | -0.33 | -0.22 | ✗  stop max_width_atr 3.0→2.4: -0.30R | 0 | 0.10R | 0, +0.00 (+0.00 / +0.00) | 546 / 202 of 890 | 0 | only 14 trades; avg -0.24R/trade (needs +0.10R); profit factor 0.57; only 5 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 40.0 | -0.396 | 0.59 | 2.6R | -0.55 / -0.17 | -0.17 / -0.55 | 0/5 ✗ | -0.54 | -0.66 | ✗  stop max_width_atr 3.0→2.4: -0.65R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 17 / 7 of 25 | 0 | only 5 trades; avg -0.40R/trade (needs +0.10R); profit factor 0.59; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 6 | 0.0 | -1.084 | 0.0 | 6.5R | -1.07 / -1.16 | -0.99 / -1.13 | 0/5 ✗ | -1.08 | -1.14 | ✗  stop max_width_atr 3.0→2.4: -1.22R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 67 / 18 of 88 | 0 | only 6 trades; avg -1.08R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 285 | 51.6 | +0.022 | 1.04 | 30.7R | +0.15 / -0.23 | +0.10 / -0.05 | 2/5 ✗ | -0.02 | -0.06 | ✗  stop atr 1.5→1.8: -0.01R | 6 | 0.07R | 2, +0.11 (+1.27 / -1.05) | 101 / 22 of 141 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.04; max drawdown 30.7R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 195 | 51.8 | -0.020 | 0.96 | 31.6R | -0.14 / +0.26 | -0.07 / +0.03 | 2/5 ✗ | -0.08 | -0.14 | ✗  stop atr 1.5→1.2: -0.11R | 4 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 222 / 6 of 230 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 31.6R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1285 | 34.0 | -0.033 | 0.95 | 85.6R | -0.04 / -0.01 | +0.05 / -0.12 | 1/5 ✗ | -0.11 | -0.18 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.13R | 51, +0.20 (+0.36 / -0.77) | 141 / 39 of 368 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; max drawdown 85.6R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FAILED** | 1285 | 34.0 | -0.033 | 0.95 | 85.6R | -0.04 / -0.01 | +0.05 / -0.12 | 1/5 ✗ | -0.11 | -0.18 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.13R | 51, +0.20 (+0.36 / -0.77) | 141 / 39 of 368 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; max drawdown 85.6R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 847 | 51.2 | -0.051 | 0.91 | 67.9R | -0.05 / -0.04 | -0.09 / -0.02 | 0/5 ✗ | -0.14 | -0.21 | ✗  stop atr 1.5→1.2: -0.09R | 3 | 0.14R | 7, +0.30 (-0.10 / +0.84) | 138 / 39 of 215 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 67.9R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 3431 | 32.4 | -0.054 | 0.91 | 258.1R | -0.09 / +0.02 | -0.03 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 35, +0.49 (+0.56 / +0.06) | 215 / 125 of 573 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 258.1R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 3009 | 32.2 | -0.057 | 0.91 | 248.7R | -0.10 / +0.04 | -0.04 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 33, +0.42 (+0.56 / -0.97) | 127 / 90 of 417 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 248.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1511 | 33.5 | -0.057 | 0.91 | 124.4R | -0.07 / -0.03 | +0.01 / -0.13 | 1/5 ✗ | -0.14 | -0.21 | ✗  stop atr 2.0→1.6: -0.14R | 2 | 0.13R | 56, +0.25 (+0.29 / +0.10) | 242 / 62 of 516 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 124.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FAILED** | 3009 | 32.2 | -0.057 | 0.91 | 248.7R | -0.10 / +0.04 | -0.04 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 33, +0.42 (+0.56 / -0.97) | 127 / 90 of 417 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 248.7R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 3095 | 48.5 | -0.058 | 0.89 | 209.3R | -0.08 / -0.02 | -0.06 / -0.05 | 0/5 ✗ | -0.11 | -0.15 | ✗  stop atr 2.0→1.6: -0.07R | 1 | 0.08R | 34, +0.36 (+0.45 / -0.59) | 127 / 90 of 417 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 209.3R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 96 | 46.9 | -0.061 | 0.89 | 16.1R | +0.10 / -0.36 | -0.12 / +0.01 | 3/5 ✗ | -0.09 | -0.11 | ✗  st_n 10→8: -0.07R | 2 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 44 / 6 of 52 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 16.1R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1321 | 49.2 | -0.068 | 0.87 | 115.9R | -0.07 / -0.08 | -0.04 / -0.10 | 0/5 ✗ | -0.14 | -0.21 | ✗  stop atr 2.0→1.6: -0.14R | 2 | 0.13R | 51, +0.17 (+0.28 / -0.54) | 141 / 39 of 368 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; max drawdown 115.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1276 | 48.4 | -0.073 | 0.87 | 136.2R | -0.03 / -0.16 | +0.01 / -0.16 | 1/5 ✗ | -0.11 | -0.15 | ✗  long_rsi_hi 65→52: -0.17R | 3 | 0.06R | 14, +0.07 (+1.04 / -0.89) | 674 / 200 of 1041 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; max drawdown 136.2R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 38 | 50.0 | -0.082 | 0.85 | 6.0R | +0.07 / -0.46 | +0.31 / -0.43 | 2/5 ✗ | -0.11 | -0.14 | ✗  time_stop_bars 40→32: -0.08R | 1 | 0.06R | 1, +0.24 (+0.00 / +0.24) | 154 / 4 of 161 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.85; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 214 | 41.1 | -0.102 | 0.84 | 51.0R | -0.14 / +0.08 | +0.12 / -0.26 | 2/5 ✗ | -0.16 | -0.21 | ✗  depth 0.985→1.182: -0.29R | 2 | 0.11R | 6, +0.50 (+0.50 / +0.00) | 89 / 8 of 109 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.84; max drawdown 51.0R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1917 | 56.5 | -0.105 | 0.63 | 201.6R | -0.10 / -0.11 | -0.12 / -0.09 | 0/5 ✗ | -0.14 | -0.16 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.05R | 2, -0.03 (+0.00 / -0.03) | 760 / 4 of 1011 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.63; max drawdown 201.6R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 367 | 45.2 | -0.119 | 0.78 | 51.7R | -0.12 / -0.11 | -0.18 / -0.06 | 0/5 ✗ | -0.18 | -0.25 | ✗  slow 21→17: -0.20R | 3 | 0.12R | 5, +0.01 (-1.00 / +1.52) | 147 / 9 of 166 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.78; max drawdown 51.7R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 7187 | 54.1 | -0.125 | 0.55 | 902.3R | -0.11 / -0.17 | -0.14 / -0.11 | 0/5 ✗ | -0.19 | -0.25 | ✗  stop atr 2.0→1.6: -0.15R | 0 | 0.11R | 44, -0.11 (-0.07 / -0.18) | 1057 / 7 of 1406 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.55; max drawdown 902.3R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 167 | 48.5 | -0.133 | 0.76 | 23.9R | -0.16 / -0.07 | -0.13 / -0.14 | 2/5 ✗ | -0.20 | -0.28 | ✗  adx_min 20→16: -0.17R | 2 | 0.14R | 6, -0.27 (-0.07 / -1.26) | 54 / 5 of 70 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.76; max drawdown 23.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6496 | 47.2 | -0.136 | 0.76 | 894.0R | -0.14 / -0.13 | -0.18 / -0.10 | 0/5 ✗ | -0.20 | -0.27 | ✗  stop atr 1.5→1.2: -0.17R | 0 | 0.13R | 49, -0.11 (+0.04 / -0.56) | 1140 / 283 of 1802 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 894.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 307 | 33.2 | -0.147 | 0.81 | 62.0R | -0.01 / -0.44 | -0.27 / -0.02 | 1/5 ✗ | -0.25 | -0.36 | ✗  time_stop_bars 30→36: -0.17R | 1 | 0.20R | 4, +0.34 (+2.70 / -0.44) | 88 / 214 of 313 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.81; max drawdown 62.0R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 81 | 34.6 | -0.168 | 0.77 | 23.2R | -0.31 / +0.40 | -0.17 / -0.17 | 1/5 ✗ | -0.23 | -0.34 | ✗  depth 0.985→1.182: -0.46R | 2 | 0.16R | 2, +1.30 (+1.30 / +0.00) | 41 / 6 of 49 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.77; max drawdown 23.2R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 274 | 45.6 | -0.184 | 0.68 | 55.3R | -0.18 / -0.18 | -0.29 / -0.10 | 1/5 ✗ | -0.25 | -0.30 | ✗  stop atr 2.0→1.6: -0.21R | 2 | 0.08R | 6, +0.53 (+0.39 / +1.25) | 58 / 2 of 70 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.68; max drawdown 55.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 309 | 48.2 | -0.192 | 0.68 | 59.5R | -0.17 / -0.24 | -0.20 / -0.19 | 0/5 ✗ | -0.29 | -0.38 | ✗  vol_x 1.2→1.44: -0.32R | 3 | 0.17R | 5, -0.41 (-0.41 / +0.00) | 102 / 202 of 314 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.68; max drawdown 59.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 469 | 45.0 | -0.192 | 0.68 | 92.2R | -0.19 / -0.19 | -0.26 / -0.16 | 0/5 ✗ | -0.34 | -0.48 | ✗  stop atr 1.5→1.2: -0.29R | 1 | 0.27R | 21, -0.32 (+0.04 / -1.04) | 82 / 15 of 120 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.19R/trade (needs +0.10R); profit factor 0.68; max drawdown 92.2R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 298 | 48.0 | -0.195 | 0.68 | 67.3R | -0.13 / -0.36 | -0.32 / -0.09 | 0/5 ✗ | -0.32 | -0.42 | ✗  stop atr 1.5→1.2: -0.27R | 1 | 0.20R | 5, -0.91 (-0.69 / -1.24) | 176 / 10 of 198 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 67.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2827 | 46.3 | -0.199 | 0.39 | 565.0R | -0.18 / -0.24 | -0.24 / -0.16 | 0/5 ✗ | -0.30 | -0.41 | ✗  stop atr 2.0→1.6: -0.25R | 0 | 0.17R | 45, -0.08 (+0.00 / -0.15) | 1040 / 29 of 1273 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.39; max drawdown 565.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3505 | 46.1 | -0.201 | 0.68 | 705.2R | -0.17 / -0.27 | -0.21 / -0.19 | 0/5 ✗ | -0.32 | -0.43 | ✗  stop atr 1.5→1.2: -0.25R | 0 | 0.18R | 100, -0.15 (+0.08 / -0.79) | 859 / 228 of 1607 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 705.2R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 877 | 30.8 | -0.207 | 0.75 | 199.8R | -0.17 / -0.27 | -0.24 / -0.18 | 1/5 ✗ | -0.31 | -0.42 | ✗  stop buffer_atr 0.2→0.16: -0.26R | 1 | 0.21R | 17, -0.40 (+0.36 / -1.25) | 467 / 1122 of 1680 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.75; max drawdown 199.8R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 492 | 45.9 | -0.227 | 0.64 | 113.1R | -0.23 / -0.21 | -0.23 / -0.23 | 0/5 ✗ | -0.34 | -0.46 | ✗  stop atr 1.5→1.2: -0.31R | 1 | 0.20R | 17, -0.44 (-0.41 / -0.53) | 118 / 36 of 198 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.64; max drawdown 113.1R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 347 | 39.8 | -0.243 | 0.6 | 86.8R | -0.22 / -0.32 | -0.31 / -0.20 | 0/5 ✗ | -0.34 | -0.43 | ✗  fast 9→11: -0.33R | 1 | 0.17R | 11, +0.04 (+0.21 / -0.76) | 113 / 20 of 152 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.60; max drawdown 86.8R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 3094 | 45.1 | -0.258 | 0.61 | 799.8R | -0.24 / -0.29 | -0.30 / -0.24 | 0/5 ✗ | -0.41 | -0.58 | ✗  stop atr 1.5→1.2: -0.34R | 0 | 0.27R | 187, -0.14 (+0.04 / -0.90) | 1353 / 197 of 2183 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 799.8R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 37 | 35.1 | -0.295 | 0.59 | 12.8R | -0.01 / -0.66 | -0.49 / -0.07 | 1/5 ✗ | -0.46 | -0.59 | ✗  time_stop_bars 30→24: -0.33R | 2 | 0.17R | 7, -0.82 (-0.59 / -1.40) | 102 / 37 of 153 | 0 | avg -0.29R/trade (needs +0.10R); profit factor 0.59; max drawdown 12.8R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1298 | 29.3 | -0.312 | 0.6 | 406.8R | -0.33 / -0.26 | -0.28 / -0.34 | 0/5 ✗ | -0.39 | -0.46 | ✗  rsi_n 14→17: -0.38R | 1 | 0.14R | 3, -0.04 (-0.41 / +0.69) | 775 / 8 of 829 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.60; max drawdown 406.8R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1534 | 31.9 | -0.312 | 0.61 | 486.2R | -0.31 / -0.31 | -0.33 / -0.29 | 0/5 ✗ | -0.44 | -0.56 | ✗  rsi_n 14→17: -0.36R | 0 | 0.22R | 25, +0.23 (+0.09 / +0.39) | 610 / 28 of 737 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.61; max drawdown 486.2R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 550 | 42.5 | -0.345 | 0.52 | 194.1R | -0.33 / -0.38 | -0.30 / -0.36 | 0/5 ✗ | -0.51 | -0.66 | ✗  stop atr 1.5→1.2: -0.42R | 0 | 0.31R | 39, -0.73 (-0.67 / -1.09) | 100 / 34 of 187 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); avg -0.34R/trade (needs +0.10R); profit factor 0.52; max drawdown 194.1R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 2186 | 33.2 | -0.351 | 0.2 | 767.7R | -0.34 / -0.38 | -0.44 / -0.28 | 0/5 ✗ | -0.52 | -0.70 | ✗  hi 90→108: -0.44R | 0 | 0.30R | 70, -0.36 (-0.30 / -0.42) | 1244 / 52 of 1440 | 0 | not cost-viable: fees + slippage 0.30R per trade (stop must be ≥ 4x the round-trip cost); avg -0.35R/trade (needs +0.10R); profit factor 0.20; max drawdown 767.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 330 | 37.3 | -0.475 | 0.38 | 156.7R | -0.43 / -0.59 | -0.49 / -0.46 | 0/5 ✗ | -0.62 | -0.77 | ✗  stop atr 1.0→0.8: -0.52R | 0 | 0.28R | 16, -0.65 (-0.59 / -0.75) | 123 / 221 of 370 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R); profit factor 0.38; max drawdown 156.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 623 | 24.2 | -0.483 | 0.51 | 300.7R | -0.52 / -0.39 | -0.65 / -0.35 | 0/5 ✗ | -0.65 | -0.78 | ✗  stop buffer_atr 0.2→0.16: -0.51R | 1 | 0.34R | 27, -0.27 (+0.37 / -1.06) | 492 / 1034 of 1714 | 0 | not cost-viable: fees + slippage 0.34R per trade (stop must be ≥ 4x the round-trip cost); avg -0.48R/trade (needs +0.10R); profit factor 0.51; max drawdown 300.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 590 | 39.3 | -0.486 | 0.38 | 286.6R | -0.46 / -0.56 | -0.59 / -0.43 | 0/5 ✗ | -0.70 | -0.94 | ✗  stop atr 1.0→0.8: -0.56R | 0 | 0.39R | 40, -0.69 (-0.63 / -0.77) | 109 / 243 of 393 | 0 | not cost-viable: fees + slippage 0.39R per trade (stop must be ≥ 4x the round-trip cost); avg -0.49R/trade (needs +0.10R); profit factor 0.38; max drawdown 286.6R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 123 | 19.5 | -0.571 | 0.43 | 74.4R | -0.51 / -0.68 | -0.67 / -0.49 | 0/5 ✗ | -0.70 | -0.83 | ✗  stop max_width_atr 3.0→2.4: -0.57R | 1 | 0.27R | 6, -0.04 (+0.51 / -0.32) | 33 / 107 of 154 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.57R/trade (needs +0.10R); profit factor 0.43; max drawdown 74.4R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 284 | 32.7 | -0.640 | 0.3 | 184.1R | -0.73 / -0.51 | -0.57 / -0.92 | 0/5 ✗ | -1.03 | -1.43 | ✗  stop atr 1.5→1.2: -0.86R | 0 | 0.62R | 79, -0.46 (-0.42 / -0.57) | 199 / 58 of 340 | 0 | not cost-viable: fees + slippage 0.62R per trade (stop must be ≥ 4x the round-trip cost); avg -0.64R/trade (needs +0.10R); profit factor 0.30; max drawdown 184.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 478 | 24.7 | -1.175 | 0.14 | 561.7R | -1.25 / -1.09 | -1.05 / -1.77 | 0/5 ✗ | -1.84 | -2.49 | ✗  stop atr 1.0→0.8: -1.50R | 0 | 1.07R | 150, -1.12 (-1.20 / -0.98) | 224 / 645 of 1025 | 0 | not cost-viable: fees + slippage 1.07R per trade (stop must be ≥ 4x the round-trip cost); avg -1.18R/trade (needs +0.10R); profit factor 0.14; max drawdown 561.7R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **25** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 118 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.34** (Bonferroni: family-wise false-winner rate 0.05 over 118 trials; with 1 trial it would be 1.65).

**Research run duration:** 8.8 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 25 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (85.5 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 34 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

0 of 59 strategy / timeframe tests would get a different verdict.

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (79% of 3,431 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (76% of 1,511 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (81% of 1,254 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 3,009 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,285 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 1,104 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 3,009 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,285 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 1,104 trades shared)

🧪 **Strategy lab:** 5 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S5-SWEEP-MSS-FVG | 15m | 7 | +0.153 | -1.323 | -0.196 | -0.366 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 2 | +0.037 | +0.037 | -0.691 | -0.473 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.295 | -0.662 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | -0.169 | -2.552 | too few trades to compare |
| S7-SILVER-BULLET | 15m | 5 | -0.396 | -0.169 | -0.108 | +0.042 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 6 | -1.084 | -1.163 | -0.235 | -0.106 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 307 | -0.147 | -0.444 | -0.207 | -0.273 | no |
| S8-PDH-PDL-SWEEP | 30m | 123 | -0.571 | -0.677 | -0.483 | -0.391 | no |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): macd_trend_cross@1.0 1h BACKTESTING → FAILED

### 3c. Research layers (daily run)
Last run: **2026-09-30 00:55 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 10 | 2017-08-17 | 2026-09-29 | 19969 |  |
| 1h | 10 | 2017-08-17 | 2026-09-29 | 79812 |  |
| 30m | 10 | 2024-09-30 | 2026-09-30 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 10 | 2025-09-30 | 2026-09-30 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 10 | 2026-07-02 | 2026-09-30 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 1104 (668) | no_displacement, false_breakout, trend_reversal | false_breakout 64%, no_displacement 34% | +0.47R | -0.38R | +0.23 / +0.17 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 1254 (766) | no_displacement, false_breakout, trend_reversal | false_breakout 63%, no_displacement 35% | +0.47R | -0.36R | +0.23 / +0.17 |
| donchian_breakout-VEXIT-VRVOL | 4h | BACKTESTING | 1104 (668) | no_displacement, false_breakout, trend_reversal | false_breakout 64%, no_displacement 34% | +0.47R | -0.38R | +0.23 / +0.17 |
| donchian_breakout | 4h | BACKTESTING | 1136 (529) | no_displacement, false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 67%, stop_too_tight 36%, no_displacement 35% | +0.33R | -0.38R | +0.14 / +0.09 |
| bb_squeeze_breakout | 4h | FAILED | 285 (138) | false_breakout, stop_too_tight, structural_change | false_breakout 59%, stop_too_tight 43%, regime_mismatch 30% | +0.36R | -0.35R | +0.11 / +0.02 |
| macd_trend_cross | 1h | FAILED | 195 (94) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 93%, indicator_lag 40%, stop_too_tight 31% | +0.31R | -0.42R | +0.13 / -0.02 |
| donchian_breakout-VEXIT | 30m | FAILED | 1285 (848) | false_breakout | false_breakout 72% | +0.44R | -0.41R | +0.12 / -0.03 |
| donchian_breakout-VEXIT-VRVOL | 30m | FAILED | 1285 (848) | false_breakout | false_breakout 72% | +0.44R | -0.41R | +0.12 / -0.03 |
| bb_squeeze_breakout | 1h | FAILED | 847 (413) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 62%, no_displacement 52%, stop_too_tight 37%, regime_mismatch 35% | +0.35R | -0.44R | +0.12 / -0.05 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 3431 (2319) | htf_conflict, no_displacement, false_breakout, regime_mismatch | false_breakout 64% | +0.49R | -0.40R | +0.05 / -0.05 |
| donchian_breakout-VEXIT | 1h | FAILED | 3009 (2039) | htf_conflict, no_displacement, false_breakout | false_breakout 63% | +0.51R | -0.40R | +0.05 / -0.06 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1511 (1005) | false_breakout | false_breakout 72% | +0.44R | -0.42R | +0.11 / -0.06 |
| donchian_breakout-VEXIT-VRVOL | 1h | FAILED | 3009 (2039) | htf_conflict, no_displacement, false_breakout | false_breakout 63% | +0.51R | -0.40R | +0.05 / -0.06 |
| donchian_breakout | 1h | FAILED | 3095 (1594) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 32% | +0.36R | -0.39R | +0.04 / -0.06 |
| supertrend_flip | 4h | FAILED | 96 (51) | regime_mismatch, stop_too_tight, indicator_lag, structural_change | regime_mismatch 69%, indicator_lag 35%, stop_too_tight 26% | +0.44R | -0.44R | +0.00 / -0.06 |
| donchian_breakout | 30m | FAILED | 1321 (671) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 76%, stop_too_tight 34% | +0.28R | -0.41R | +0.09 / -0.07 |
| trend_pullback | 4h | FAILED | 1276 (658) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 81%, indicator_lag 39%, stop_too_tight 26% | +0.36R | -0.43R | +0.01 / -0.07 |
| macd_trend_cross | 4h | FAILED | 38 (19) | structural_change | regime_mismatch 95%, no_displacement 90%, low_relative_volume 63%, indicator_lag 58% | +0.17R | -0.45R | -0.00 / -0.08 |
| R4-CLUC | 30m | FAILED | 214 (126) | none | wrong_session 67% | +0.33R | -0.48R | +0.02 / -0.10 |
| rsi2_dip_buy | 4h | FAILED | 1917 (834) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 45% | +0.16R | -0.21R | -0.04 / -0.10 |
| ema_9_21_cross | 1h | FAILED | 367 (201) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, wrong_session 68%, indicator_lag 49%, stop_too_tight 27% | +0.26R | -0.38R | +0.03 / -0.12 |
| rsi2_dip_buy | 1h | FAILED | 7187 (3298) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 43% | +0.16R | -0.20R | +0.00 / -0.12 |
| supertrend_flip | 30m | FAILED | 167 (86) | stop_too_tight, indicator_lag | indicator_lag 45%, regime_mismatch 43%, stop_too_tight 40% | +0.28R | -0.49R | +0.04 / -0.13 |
| trend_pullback | 1h | FAILED | 6496 (3427) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 76%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.43R | +0.02 / -0.14 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 307 (205) | stop_too_tight, sweep_continued | sweep_continued 98%, range_market 58%, stop_too_tight 33% | +0.54R | -0.39R | +0.10 / -0.15 |
| R4-CLUC | 15m | FAILED | 81 (53) | none | wrong_session 62% | +0.40R | -0.25R | -0.01 / -0.17 |
| supertrend_flip | 1h | FAILED | 274 (149) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 73%, regime_mismatch 66%, stop_too_tight 40%, indicator_lag 33% | +0.39R | -0.38R | -0.08 / -0.18 |
| liquidity_sweep_reversal | 1h | FAILED | 309 (160) | stop_too_tight | stop_too_tight 52% | +0.26R | -0.50R | +0.01 / -0.19 |
| ema_9_21_cross | 15m | FAILED | 469 (258) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 30% | +0.28R | -0.42R | +0.13 / -0.19 |
| macd_trend_cross | 30m | FAILED | 298 (155) | overextended_entry, stop_too_tight, indicator_lag | no_displacement 88%, low_relative_volume 45%, indicator_lag 43%, stop_too_tight 29% | +0.34R | -0.44R | +0.05 / -0.20 |
| rsi2_dip_buy | 30m | FAILED | 2827 (1517) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 34% | +0.17R | -0.19R | +0.01 / -0.20 |
| trend_pullback | 30m | FAILED | 3505 (1888) | trend_reversal, stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 29% | +0.28R | -0.43R | +0.03 / -0.20 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 877 (607) | range_market, trend_reversal, stop_too_tight | range_market 47%, stop_too_tight 36% | +0.61R | -0.51R | +0.04 / -0.21 |
| bb_squeeze_breakout | 30m | FAILED | 492 (266) | false_breakout, stop_too_tight | false_breakout 63%, stop_too_tight 40% | +0.26R | -0.45R | +0.03 / -0.23 |
| ema_9_21_cross | 30m | FAILED | 347 (209) | stop_too_tight, indicator_lag | indicator_lag 47%, low_relative_volume 40%, stop_too_tight 26% | +0.27R | -0.37R | -0.03 / -0.24 |
| trend_pullback | 15m | FAILED | 3094 (1699) | wrong_session, stop_too_tight, indicator_lag | wrong_session 71%, indicator_lag 50%, stop_too_tight 32% | +0.25R | -0.44R | +0.07 / -0.26 |
| S6-OB-FVG-noSMC | 15m | FAILED | 37 (24) | none | - | +0.24R | -0.59R | -0.08 / -0.29 |
| R4-BBRSI | 1h | FAILED | 1298 (918) | none | - | +0.45R | -0.43R | -0.14 / -0.31 |
| R4-BBRSI | 30m | FAILED | 1534 (1044) | none | - | +0.43R | -0.43R | -0.05 / -0.31 |
| bb_squeeze_breakout | 15m | FAILED | 550 (316) | no_displacement, stop_too_tight | false_breakout 59%, no_displacement 58%, stop_too_tight 44% | +0.31R | -0.45R | +0.02 / -0.34 |
| rsi2_dip_buy | 15m | FAILED | 2186 (1460) | low_relative_volume, trend_reversal, fees_slippage | low_relative_volume 45%, fees_slippage 44% | +0.16R | -0.19R | +0.00 / -0.35 |
| liquidity_sweep_reversal | 30m | FAILED | 330 (207) | stop_too_tight | stop_too_tight 40% | +0.36R | -0.49R | -0.15 / -0.47 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 623 (472) | stop_too_tight | stop_too_tight 31% | +0.59R | -0.49R | -0.07 / -0.48 |
| liquidity_sweep_reversal | 15m | FAILED | 590 (358) | stop_too_tight | stop_too_tight 37% | +0.39R | -0.47R | +0.00 / -0.49 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 123 (99) | stop_too_tight, sweep_continued | sweep_continued 96%, stop_too_tight 26% | +0.53R | -0.64R | -0.22 / -0.57 |
| ema_9_21_cross | 5m | FAILED | 284 (191) | stop_too_tight, indicator_lag | indicator_lag 53%, stop_too_tight 27% | +0.22R | -0.48R | +0.11 / -0.64 |
| liquidity_sweep_reversal | 5m | FAILED | 478 (360) | fees_slippage, stop_too_tight | stop_too_tight 37%, fees_slippage 25% | +0.27R | -0.49R | +0.15 / -1.18 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 28 strategy/timeframe tests); `false_breakout` (systematic in 15 strategy/timeframe tests); `regime_mismatch` (systematic in 13 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `no_displacement` (systematic in 10 strategy/timeframe tests); `trend_reversal` (systematic in 10 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `htf_conflict` (systematic in 3 strategy/timeframe tests); `fees_slippage` (systematic in 3 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- ZEC down -11.5% (2026-09-28 13:00 → 2026-09-29 02:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- AVAX up +14.3% (2026-09-29 02:00 → 2026-09-29 12:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 104.8 KB | - | - |
| `memory/coin_notes.md` | 6.8 KB | 7 | 2026-09-27 00:26 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 6.0 KB | 13 | 2026-09-30 08:22 UTC |
| `memory/experiments.md` | 48.1 KB | 19 | 2026-09-28 15:40 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 79.1 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 8.4 KB | - | - |
| `memory/missed_trades.md` | 16.5 KB | 22 | 2026-09-30 00:55 UTC |
| `memory/playbook.md` | 8.7 KB | - | - |
| `memory/research_sources.md` | 59.7 KB | 45 | 2026-09-28 15:40 UTC |
| `memory/smc_events.csv` | 514.5 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 16.2 KB | - | - |
| `memory/strategy_registry.csv` | 36.6 KB | - | - |
| `memory/trials.csv` | 9.2 KB | - | - |
| `memory/universe_log.md` | 13.4 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*