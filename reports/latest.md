# Crypto Signal Report

**Updated:** 2026-09-26 17:16 Beijing time (2026-09-26 09:16 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 4.2 MB (GitHub) · large files of this run 2.4 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-26 09:16 UTC / 2026-09-26 17:16 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US PCE / Personal Income and Outlays (Aug data) 2026-09-30 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.05% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| VTHO | **DEGRADED** | 1d: DEGRADED: volume 269x normal on candle 09-25 00:00 UTC (possible bad data) |
| BABY | **DEGRADED** | 1d: DEGRADED: volume 65x normal on candle 09-23 00:00 UTC (possible bad data); 1d: DEGRADED: volume 67x normal on candle 09-25 00:00 UTC (possible bad data) |
- 74 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-26 09:16 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 739 h since 2026-08-26 | +0.0021% | 1.32 | 1.30 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 739 h since 2026-08-26 | +0.0026% | 1.34 | 0.88 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 739 h since 2026-08-26 | +0.0100% | 2.38 | 0.90 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 739 h since 2026-08-26 | +0.0027% | 1.46 | 1.08 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 739 h since 2026-08-26 | +0.0100% | 0.60 | 1.07 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 739 h since 2026-08-26 | +0.0096% | 1.90 | 1.13 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| ENA | GOOD | okx | 739 h since 2026-08-26 | +0.0050% | 0.84 | 1.00 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ENAUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 739 h since 2026-08-26 | +0.0100% | 1.78 | 0.84 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 739 h since 2026-08-26 | +0.0100% | 2.45 | 1.63 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| ADA | GOOD | okx | 726 h since 2026-08-27 | +0.0100% | 1.95 | 0.80 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ADAUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **XRP**, **SOL**, **ZEC**, **SUI**, **ENA**
- **Research only** - backtested, never a signal: UNI, BNB, ADA

| Not eligible | 24h volume | Why |
|---|---|---|
| VTHO | $96M | 7-day average volume $21M < $50M; spread 0.123% > 0.1%; order book too thin: $52k within 1% (need $250k) |
| BABY | $90M | 7-day average volume $25M < $50M; order book too thin: $68k within 1% (need $250k) |
| LINK | $67M | 7-day average volume $50M < $50M |

**Flags (not excluded):** VTHO: price data DEGRADED - stays in the list, but no signals; BABY: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, RLUSD, TAO, USD1, USDC, WLD (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 475 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ETH | 475 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| XRP | 438 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| SOL | 319 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| ZEC | 392 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| SUI | 177 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| ENA | 129 | 907 | 901 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |
| UNI | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| BNB | 463 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| ADA | 440 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (LH/HL) | 84,145.3 / 83,848.9 | 0.62 | 0.62x | 0.62x | - |
| ETH | mixed (LH/HL) | 2,696.44 / 2,677.16 | 0.35 | 0.62x | 0.60x | bull_engulf |
| XRP | mixed (LH/HL) | 1.581 / 1.5492 | 0.39 | 0.33x | 0.71x | - |
| SOL | up (HH/HL) | 122.94 / 120.82 | 0.43 | 0.64x | 0.92x | - |
| ZEC | mixed (LH/HL) | 1,560.64 / 1,524.79 | 0.19 | 0.24x | 0.67x | bear_engulf, bear_reject |
| SUI | up (HH/HL) | 1.2179 / 1.0901 | 0.72 | 0.45x | 1.11x | bull_engulf, bull_reject |
| ENA | up (HH/HL) | 0.28 / 0.2632 | 0.75 | 0.63x | 1.31x | bull_engulf, retest_up |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 471 | 48% | 34% | 27% | 79% | 43% | 31% | can't tell from chance | 0.12R |
| 4h | displacement_down | 370 | 48% | 31% | 21% | 75% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1187 | 45% | 31% | 22% | 77% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | bear_engulf | 1385 | 45% | 30% | 20% | 77% | 48% | 32% | worse than chance | 0.08R |
| 4h | bull_reject | 913 | 41% | 28% | 20% | 79% | 43% | 30% | can't tell from chance | 0.12R |
| 4h | bear_reject | 927 | 48% | 34% | 24% | 73% | 48% | 32% | can't tell from chance | 0.07R |
| 4h | smc_sweep_bull | 654 | 43% | 28% | 21% | 78% | 43% | 29% | can't tell from chance | 0.12R |
| 4h | smc_sweep_bear | 672 | 43% | 29% | 19% | 80% | 48% | 32% | worse than chance | 0.08R |
| 4h | smc_bos_up | 269 | 44% | 29% | 22% | 82% | 45% | 30% | can't tell from chance | 0.13R |
| 4h | smc_bos_down | 248 | 53% | 39% | 27% | 67% | 49% | 32% | can't tell from chance | 0.07R |
| 4h | smc_choch_up | 86 | 52% | 33% | 27% | 81% | 45% | 30% | can't tell from chance | 0.12R |
| 4h | smc_choch_down | 79 | 42% | 23% | 11% | 78% | 49% | 33% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 662 | 45% | 29% | 23% | 77% | 43% | 29% | can't tell from chance | 0.12R |
| 4h | smc_fvg_retrace_bear | 676 | 49% | 34% | 22% | 74% | 48% | 32% | can't tell from chance | 0.08R |
| 1h | displacement_up | 620 | 47% | 35% | 29% | 72% | 43% | 30% | can't tell from chance | 0.26R |
| 1h | displacement_down | 432 | 37% | 23% | 15% | 81% | 40% | 26% | can't tell from chance | 0.17R |
| 1h | bull_engulf | 1686 | 40% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.30R |
| 1h | bear_engulf | 1855 | 40% | 26% | 18% | 79% | 39% | 25% | can't tell from chance | 0.18R |
| 1h | bull_reject | 1393 | 40% | 28% | 22% | 75% | 42% | 29% | can't tell from chance | 0.29R |
| 1h | bear_reject | 1375 | 37% | 25% | 17% | 82% | 39% | 25% | can't tell from chance | 0.17R |
| 1h | smc_sweep_bull | 634 | 40% | 26% | 19% | 78% | 43% | 30% | can't tell from chance | 0.28R |
| 1h | smc_sweep_bear | 703 | 38% | 25% | 16% | 80% | 39% | 25% | can't tell from chance | 0.17R |
| 1h | smc_bos_up | 399 | 43% | 31% | 24% | 78% | 43% | 30% | can't tell from chance | 0.24R |
| 1h | smc_bos_down | 267 | 39% | 28% | 19% | 81% | 40% | 25% | can't tell from chance | 0.20R |
| 1h | smc_choch_up | 116 | 47% | 36% | 32% | 71% | 44% | 30% | can't tell from chance | 0.32R |
| 1h | smc_choch_down | 118 | 45% | 28% | 16% | 76% | 39% | 26% | can't tell from chance | 0.16R |
| 1h | smc_fvg_retrace_bull | 888 | 46% | 33% | 25% | 71% | 42% | 29% | beats chance | 0.28R |
| 1h | smc_fvg_retrace_bear | 828 | 41% | 29% | 19% | 78% | 40% | 26% | can't tell from chance | 0.18R |
| 30m | displacement_up | 653 | 41% | 30% | 25% | 78% | 42% | 30% | can't tell from chance | 0.28R |
| 30m | displacement_down | 425 | 39% | 23% | 13% | 83% | 36% | 21% | can't tell from chance | 0.18R |
| 30m | bull_engulf | 1716 | 42% | 29% | 21% | 75% | 42% | 30% | can't tell from chance | 0.33R |
| 30m | bear_engulf | 1747 | 36% | 22% | 15% | 82% | 36% | 21% | can't tell from chance | 0.20R |
| 30m | bull_reject | 1345 | 45% | 30% | 22% | 73% | 42% | 30% | can't tell from chance | 0.32R |
| 30m | bear_reject | 1436 | 37% | 23% | 15% | 82% | 37% | 21% | can't tell from chance | 0.20R |
| 30m | smc_sweep_bull | 617 | 41% | 28% | 18% | 75% | 42% | 29% | can't tell from chance | 0.33R |
| 30m | smc_sweep_bear | 633 | 41% | 26% | 18% | 82% | 37% | 21% | beats chance | 0.19R |
| 30m | smc_bos_up | 450 | 42% | 34% | 28% | 76% | 42% | 29% | can't tell from chance | 0.30R |
| 30m | smc_bos_down | 238 | 38% | 22% | 13% | 85% | 36% | 22% | can't tell from chance | 0.22R |
| 30m | smc_choch_up | 105 | 35% | 23% | 17% | 83% | 43% | 32% | can't tell from chance | 0.38R |
| 30m | smc_choch_down | 99 | 39% | 22% | 16% | 81% | 35% | 20% | can't tell from chance | 0.16R |
| 30m | smc_fvg_retrace_bull | 975 | 44% | 30% | 23% | 74% | 42% | 30% | can't tell from chance | 0.33R |
| 30m | smc_fvg_retrace_bear | 825 | 37% | 22% | 16% | 82% | 37% | 21% | can't tell from chance | 0.22R |
| 15m | displacement_up | 468 | 35% | 27% | 20% | 82% | 36% | 25% | can't tell from chance | 0.40R |
| 15m | displacement_down | 465 | 34% | 21% | 14% | 85% | 37% | 23% | can't tell from chance | 0.27R |
| 15m | bull_engulf | 1658 | 37% | 26% | 18% | 79% | 35% | 25% | can't tell from chance | 0.46R |
| 15m | bear_engulf | 1623 | 36% | 24% | 15% | 79% | 37% | 23% | can't tell from chance | 0.27R |
| 15m | bull_reject | 1324 | 35% | 23% | 16% | 80% | 35% | 25% | can't tell from chance | 0.47R |
| 15m | bear_reject | 1442 | 35% | 22% | 15% | 82% | 37% | 23% | can't tell from chance | 0.27R |
| 15m | smc_sweep_bull | 593 | 38% | 27% | 20% | 77% | 36% | 25% | can't tell from chance | 0.43R |
| 15m | smc_sweep_bear | 631 | 38% | 25% | 14% | 83% | 37% | 23% | can't tell from chance | 0.26R |
| 15m | smc_bos_up | 371 | 38% | 27% | 21% | 81% | 38% | 26% | can't tell from chance | 0.39R |
| 15m | smc_bos_down | 354 | 33% | 19% | 14% | 86% | 37% | 22% | can't tell from chance | 0.30R |
| 15m | smc_choch_up | 89 | 30% | 22% | 18% | 82% | 34% | 25% | can't tell from chance | 0.42R |
| 15m | smc_choch_down | 89 | 31% | 20% | 12% | 82% | 36% | 22% | can't tell from chance | 0.27R |
| 15m | smc_fvg_retrace_bull | 1019 | 34% | 24% | 16% | 81% | 35% | 25% | can't tell from chance | 0.45R |
| 15m | smc_fvg_retrace_bear | 984 | 36% | 25% | 17% | 80% | 36% | 22% | can't tell from chance | 0.28R |
| 5m | displacement_up | 1206 | 32% | 21% | 16% | 85% | 28% | 19% | beats chance | 0.74R |
| 5m | displacement_down | 1144 | 28% | 18% | 12% | 86% | 31% | 21% | worse than chance | 0.49R |
| 5m | bull_engulf | 4118 | 26% | 18% | 13% | 83% | 28% | 19% | worse than chance | 0.83R |
| 5m | bear_engulf | 4080 | 32% | 21% | 13% | 83% | 31% | 20% | can't tell from chance | 0.51R |
| 5m | bull_reject | 3397 | 27% | 18% | 13% | 82% | 28% | 19% | can't tell from chance | 0.83R |
| 5m | bear_reject | 3731 | 33% | 22% | 15% | 81% | 32% | 21% | can't tell from chance | 0.48R |
| 5m | smc_sweep_bull | 1203 | 31% | 22% | 15% | 79% | 29% | 20% | can't tell from chance | 0.75R |
| 5m | smc_sweep_bear | 1258 | 35% | 24% | 16% | 81% | 32% | 21% | can't tell from chance | 0.44R |
| 5m | smc_bos_up | 830 | 29% | 21% | 17% | 85% | 28% | 19% | can't tell from chance | 0.75R |
| 5m | smc_bos_down | 879 | 28% | 19% | 11% | 87% | 31% | 21% | can't tell from chance | 0.55R |
| 5m | smc_choch_up | 219 | 38% | 26% | 17% | 86% | 28% | 19% | beats chance | 0.81R |
| 5m | smc_choch_down | 222 | 26% | 15% | 11% | 87% | 33% | 23% | worse than chance | 0.50R |
| 5m | smc_fvg_retrace_bull | 3284 | 29% | 20% | 14% | 82% | 27% | 19% | can't tell from chance | 0.82R |
| 5m | smc_fvg_retrace_bear | 2943 | 28% | 19% | 12% | 84% | 31% | 21% | worse than chance | 0.51R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (weak) | WEAK_BULL (moderate) | WEAK_BULL (weak) | COMPRESSION (moderate) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ETH** | UNCLEAR (weak) | WEAK_BULL (moderate) | RANGE (weak) | COMPRESSION (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H COMPRESSION)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | TRANSITION (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H UNCLEAR)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (moderate) | WEAK_BULL (weak) | LONG allowed (1D/4H/1H bullish, 1W TRANSITION) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | COMPRESSION (moderate) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |
| **SUI** | RANGE (weak) | EXPANSION up (weak) | WEAK_BULL (weak) | STRONG_BULL (moderate) | LONG allowed (1D/4H/1H bullish, 1W RANGE) |
| **ENA** | TRANSITION (weak) | WEAK_BULL (weak) | STRONG_BULL (moderate) | STRONG_BULL (moderate) | LONG allowed (1D/4H/1H bullish, 1W TRANSITION) |
| **UNI** | EXPANSION up (weak) | STRONG_BULL (moderate) | TRANSITION (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H TRANSITION, 1H UNCLEAR)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | COMPRESSION (strong) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |
| **ADA** | UNCLEAR (weak) | TRANSITION (weak) | TRANSITION (weak) | WEAK_BULL (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H WEAK_BULL)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (weak)** - for: EMA-fast rising (+1.1 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.72x normal, Bollinger width above 52% of the last 100 candles · against: EMAs not lined up; ADX 27 is close to a threshold
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.2 ATR in 10 candles); ADX 44 = strong trend; candle size 1.15x normal, Bollinger width above 80% of the last 100 candles; volume 1.48x normal · against: swing structure mixed (neutral)
- **4H WEAK_BULL (weak)** - for: close above EMA-fast above EMA-slow; swing structure up (HH/HL); candle size 1.01x normal, Bollinger width above 32% of the last 100 candles; volume 0.72x normal · against: EMA-fast flat (+0.6 ATR in 10 candles) (neutral); ADX 18 = weak trend / ranging
- **1H COMPRESSION (moderate)** - for: EMA-fast flat (-0.3 ATR in 10 candles); swing structure mixed; ADX 17 = weak trend / ranging; candle size 0.62x normal, Bollinger width above 0% of the last 100 candles · against: close above EMA-fast above EMA-slow

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | up (BOS 2 candles ago) | sell-side (bullish idea) 76 candles ago | bull 83,930.00-83,995.76 (retraced) | bear 86,133.40-86,975.51 | above the range (125%) | swing high 85,255.00 (3.2 ATR) | swing low 83,848.91 (1.15 ATR) |
| **ETH** | down (CHOCH 0 candles ago) | sell-side (bullish idea) 0 candles ago | bear 2,760.00-2,765.00 (retraced) | bear 2,745.99-2,784.40 | premium (72%) | swing high 2,699.50 (0.66 ATR) | swing low 2,677.16 (1.08 ATR) |
| **XRP** | up (CHOCH 84 candles ago) | sell-side (bullish idea) 14 candles ago | bear 1.6015-1.6117 (retraced) | bull 1.3773-1.3856 | discount (0%) | swing high 1.5810 (1.93 ATR) | swing low 1.5444 (0.3 ATR) |
| **SOL** | up (CHOCH 2 candles ago) | sell-side (bullish idea) 0 candles ago | bear 121.02-121.57 (retraced) | bull 115.86-117.34 | below the range (-6%) | swing high 122.94 (2.04 ATR) | swing low 118.27 (2.19 ATR) |
| **ZEC** | down (BOS 0 candles ago) | sell-side (bullish idea) 9 candles ago | bear 1,530.74-1,534.21 | bull 1,098.88-1,133.82 | discount (17%) | swing high 1,560.64 (1.58 ATR) | swing low 1,524.79 (0.31 ATR) |
| **SUI** | up (BOS 43 candles ago) | buy-side (bearish idea) 52 candles ago | bull 1.0755-1.0969 (retraced) | bull 1.0050-1.0598 | premium (58%) | PDH 1.2179 (2.43 ATR) | swing low 1.0901 (3.3 ATR) |
| **ENA** | up (BOS 21 candles ago) | buy-side (bearish idea) 0 candles ago | bull 0.26750-0.26890 | bull 0.16130-0.17050 | premium (86%) | swing high 0.28000 (0.3 ATR) | swing low 0.26320 (1.9 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 74 (Greed), yesterday 71  (extreme fear/greed = bigger, faster moves)

## 2. Signals right now
Only **APPROVED** strategy versions (your yes, after paper trading) give signals and emails.

**No trade passes all the checks right now. That is normal - no trade is also a position.**

### 2c. Watching - no signal yet (report only, never emailed)
No tracked strategy (VALIDATION or higher) has its market filters open right now.

### 2d. Risk engine (section 15 - independent of the strategies)
- **Live results:** today +0.00R (limit -3R), this week +0.00R (limit -6R) · **halts:** none
- **Suspended strategies** (live drawdown > 8R): none
- **Risk per trade:** 0.5% · leverage never above 3x (the position is made smaller instead)
- **Heat:** max 3 positions, 1 per coin, 1 per group of correlated coins and direction (1h correlation ≥ 0.7) · groups now: BTC+ETH+SOL+XRP
- **Every live entry also needs:** reward to TP1 ≥ 2R, no opposing level before TP1, no high-impact event within ±60 min, no duplicate
- **Event calendar (next 7 days):** US PCE / Personal Income and Outlays (Aug data) 2026-09-30 12:30 UTC, US jobs report / Employment Situation (Sep data) 2026-10-02 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-09-26 06:28 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.839 | 2.51 | 2.3R | +0.56 / +2.21 | +2.21 / +0.56 | 0/5 ✗ | +0.73 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 25 / 14 of 40 | 0 | only 6 trades; only 1 unseen-test trades |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 16 | 43.8 | +0.250 | 1.33 | 4.5R | +0.11 / +0.56 | +0.18 / +0.29 | 0/5 ✗ | -0.05 | ✗  sweep_bars 8→10: -0.13R | 0 | 0.26R | 2, +0.31 (+1.94 / -1.32) | 47 / 28 of 82 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 16 trades; only 5 unseen-test trades |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1105 | 54.5 | +0.123 | 1.28 | 22.5R | +0.11 / +0.15 | +0.11 / +0.14 | 5/5 | +0.09 | stable | 8 | 0.04R | 13, +0.17 (+0.42 / -0.40) | 98 / 50 of 271 | 0 | max drawdown 22.5R |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 8 | 50.0 | +0.108 | 1.13 | 3.3R | +0.31 / -1.32 | -1.32 / +0.31 | 0/5 ✗ | -0.00 | ✗  sweep_bars 20→24: -0.16R | 0 | 0.21R | 1, -1.32 (+0.00 / -1.32) | 39 / 13 of 58 | 0 | only 8 trades; profit factor 1.13; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 3 of 4 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 56 / 14 of 73 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 39 / 13 of 58 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 3 of 4 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 25 / 14 of 40 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 18 | 50.0 | -0.001 | 1.0 | 4.9R | +0.08 / -0.41 | -0.31 / +0.09 | 1/5 ✗ | +0.12 | ✗  stop max_width_atr 3.0→3.6: -0.09R | 1 | 0.16R | 1, +1.21 (+1.21 / +0.00) | 446 / 233 of 808 | 0 | only 18 trades; avg -0.00R/trade (needs +0.10R); profit factor 1.00; only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 13 | 23.1 | -0.340 | 0.44 | 4.4R | -0.40 / -0.27 | -1.11 / -0.20 | 0/5 ✗ | -0.45 | ✗  stop buffer_atr 0.2→0.24: -0.35R | 0 | 0.09R | 0, +0.00 (+0.00 / +0.00) | 537 / 217 of 924 | 0 | only 13 trades; avg -0.34R/trade (needs +0.10R); profit factor 0.44; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 4 | 0.0 | -1.218 | 0.0 | 4.9R | -1.24 / -1.16 | -1.42 / -1.15 | 0/5 ✗ | -1.22 | ✗  sweep_bars 20→16: -1.22R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 56 / 14 of 73 | 0 | only 4 trades; avg -1.22R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.712 | 0.0 | 1.7R | +0.00 / -1.71 | -1.71 / +0.00 | 0/5 ✗ | -2.00 | ✗  stop buffer_atr 0.2→0.16: -1.75R | 0 | 0.86R | 0, +0.00 (+0.00 / +0.00) | 32 / 108 of 150 | 0 | not cost-viable: fees + slippage 0.86R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.71R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 8, -0.47 (-0.47 / +0.00) | 773 / 4 of 818 | 0 | waiting for the first daily research run (Layers B/C) |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 28, -0.22 (-0.52 / +0.52) | 675 / 14 of 769 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 11, +0.52 (+0.83 / -0.30) | 98 / 50 of 271 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 30, +0.33 (+0.56 / -0.32) | 134 / 105 of 424 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 50, -0.06 (+0.12 / -0.35) | 140 / 60 of 420 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 277 | 51.6 | +0.025 | 1.05 | 26.5R | +0.19 / -0.27 | +0.13 / -0.07 | 2/5 ✗ | -0.03 | ✗  stop atr 1.5→1.8: -0.02R | 6 | 0.07R | 2, +0.08 (-1.11 / +1.27) | 103 / 24 of 144 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.05; max drawdown 26.5R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 832 | 53.4 | -0.010 | 0.98 | 38.5R | -0.01 / +0.00 | -0.07 / +0.04 | 2/5 ✗ | -0.09 | ✗  bb_k 2→1: -0.05R | 4 | 0.14R | 5, -0.30 (-1.18 / +0.29) | 136 / 44 of 214 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 38.5R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 3064 | 48.9 | -0.046 | 0.91 | 173.9R | -0.06 / -0.02 | -0.06 / -0.03 | 0/5 ✗ | -0.09 | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.09R | 31, +0.26 (+0.32 / +0.10) | 134 / 105 of 424 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 173.9R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 92 | 47.8 | -0.057 | 0.89 | 15.1R | +0.07 / -0.29 | -0.09 / -0.02 | 2/5 ✗ | -0.08 | ✗  time_stop_bars 60→48: -0.06R | 2 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 43 / 6 of 51 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 15.1R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 38 | 50.0 | -0.063 | 0.88 | 5.6R | +0.10 / -0.46 | +0.20 / -0.33 | 2/5 ✗ | -0.10 | ✗  stop atr 1.5→1.8: -0.08R | 1 | 0.07R | 0, +0.00 (+0.00 / +0.00) | 156 / 5 of 163 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.88; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1329 | 48.5 | -0.067 | 0.88 | 114.7R | -0.08 / -0.04 | -0.03 / -0.11 | 1/5 ✗ | -0.14 | ✗  stop atr 2.0→1.6: -0.14R | 3 | 0.12R | 50, -0.08 (-0.01 / -0.19) | 140 / 60 of 420 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 114.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1218 | 47.9 | -0.068 | 0.88 | 129.2R | -0.03 / -0.14 | -0.01 / -0.13 | 1/5 ✗ | -0.11 | ✗  long_rsi_hi 65→52: -0.14R | 3 | 0.06R | 6, +1.14 (+1.12 / +1.27) | 638 / 203 of 995 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 129.2R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 186 | 48.4 | -0.088 | 0.84 | 34.0R | -0.20 / +0.15 | -0.11 / -0.07 | 2/5 ✗ | -0.15 | ✗  stop atr 1.5→1.2: -0.15R | 3 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 217 / 7 of 226 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.84; max drawdown 34.0R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1841 | 55.9 | -0.107 | 0.63 | 197.3R | -0.10 / -0.11 | -0.13 / -0.09 | 0/5 ✗ | -0.14 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.05R | 9, -0.18 (-0.18 / +0.00) | 764 / 4 of 1030 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.63; max drawdown 197.3R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 283 | 33.2 | -0.125 | 0.84 | 64.3R | -0.04 / -0.31 | -0.38 / +0.14 | 1/5 ✗ | -0.23 | ✗  time_stop_bars 30→36: -0.15R | 1 | 0.19R | 1, +2.70 (+0.00 / +2.70) | 90 / 233 of 332 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.84; max drawdown 64.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 6989 | 53.6 | -0.129 | 0.54 | 906.7R | -0.11 / -0.17 | -0.14 / -0.12 | 0/5 ✗ | -0.19 | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 43, -0.15 (-0.26 / -0.01) | 1043 / 7 of 1404 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.54; max drawdown 906.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 335 | 43.6 | -0.134 | 0.76 | 56.3R | -0.15 / -0.10 | -0.21 / -0.05 | 0/5 ✗ | -0.20 | ✗  slow 21→17: -0.22R | 3 | 0.12R | 3, -1.00 (-1.25 / -0.52) | 152 / 7 of 167 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.76; max drawdown 56.3R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6338 | 47.2 | -0.138 | 0.76 | 900.0R | -0.14 / -0.13 | -0.18 / -0.10 | 0/5 ✗ | -0.21 | ✗  stop atr 1.5→1.2: -0.18R | 1 | 0.13R | 43, +0.07 (+0.01 / +0.17) | 1209 / 303 of 1879 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 900.0R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 41 | 36.6 | -0.149 | 0.78 | 10.8R | +0.05 / -0.44 | -0.28 / -0.04 | 1/5 ✗ | -0.31 | ✗  stop buffer_atr 0.2→0.16: -0.15R | 3 | 0.15R | 7, -0.41 (+0.17 / -0.64) | 104 / 35 of 152 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.78; max drawdown 10.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 163 | 47.9 | -0.162 | 0.7 | 26.9R | -0.18 / -0.10 | -0.16 / -0.17 | 2/5 ✗ | -0.23 | ✗  adx_min 20→24: -0.21R | 1 | 0.13R | 6, -0.74 (-0.64 / -1.26) | 57 / 6 of 73 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.70; max drawdown 26.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 457 | 44.4 | -0.164 | 0.73 | 77.7R | -0.15 / -0.21 | -0.25 / -0.13 | 0/5 ✗ | -0.30 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.25R | 19, +0.12 (+0.23 / -0.77) | 64 / 14 of 101 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.73; max drawdown 77.7R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 503 | 47.1 | -0.179 | 0.71 | 90.2R | -0.23 / -0.05 | -0.21 / -0.15 | 1/5 ✗ | -0.28 | ✗  stop atr 1.5→1.2: -0.25R | 1 | 0.19R | 17, -0.47 (-0.41 / -0.58) | 125 / 42 of 213 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.71; max drawdown 90.2R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3534 | 46.3 | -0.190 | 0.69 | 692.8R | -0.18 / -0.22 | -0.22 / -0.16 | 0/5 ✗ | -0.30 | ✗  stop atr 1.5→1.2: -0.25R | 0 | 0.17R | 82, +0.12 (+0.30 / -0.20) | 846 / 263 of 1708 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.69; max drawdown 692.8R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2827 | 47.6 | -0.193 | 0.41 | 545.8R | -0.18 / -0.23 | -0.25 / -0.14 | 0/5 ✗ | -0.29 | ✗  hi 90→108: -0.25R | 0 | 0.16R | 43, -0.14 (-0.19 / -0.02) | 1026 / 24 of 1260 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.41; max drawdown 545.8R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 296 | 47.6 | -0.199 | 0.67 | 65.9R | -0.13 / -0.37 | -0.28 / -0.13 | 0/5 ✗ | -0.32 | ✗  stop atr 1.5→1.2: -0.27R | 1 | 0.19R | 5, -0.08 (+0.66 / -1.18) | 188 / 11 of 217 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.67; max drawdown 65.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 339 | 41.3 | -0.210 | 0.64 | 75.5R | -0.20 / -0.25 | -0.28 / -0.16 | 1/5 ✗ | -0.30 | ✗  fast 9→11: -0.28R | 0 | 0.17R | 10, +0.01 (-0.03 / +0.06) | 108 / 20 of 145 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.64; max drawdown 75.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 795 | 30.7 | -0.214 | 0.74 | 206.8R | -0.20 / -0.24 | -0.26 / -0.17 | 0/5 ✗ | -0.32 | ✗  stop buffer_atr 0.2→0.16: -0.25R | 1 | 0.21R | 10, +0.20 (+0.87 / -0.48) | 451 / 1179 of 1713 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.74; max drawdown 206.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 280 | 43.9 | -0.227 | 0.62 | 67.7R | -0.22 / -0.24 | -0.33 / -0.14 | 0/5 ✗ | -0.28 | ✗  stop atr 2.0→1.6: -0.24R | 1 | 0.08R | 4, +0.17 (-0.19 / +1.24) | 58 / 2 of 68 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.62; max drawdown 67.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 294 | 46.9 | -0.239 | 0.61 | 71.2R | -0.26 / -0.19 | -0.25 / -0.22 | 0/5 ✗ | -0.33 | ✗  vol_x 1.2→1.44: -0.38R | 2 | 0.17R | 4, -0.23 (+0.01 / -0.48) | 101 / 220 of 329 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.61; max drawdown 71.2R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 3140 | 45.1 | -0.251 | 0.62 | 793.3R | -0.24 / -0.28 | -0.29 / -0.23 | 0/5 ✗ | -0.40 | ✗  stop atr 1.5→1.2: -0.33R | 0 | 0.25R | 166, -0.06 (+0.01 / -0.17) | 1356 / 369 of 2327 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.25R/trade (needs +0.10R); profit factor 0.62; max drawdown 793.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 2173 | 35.6 | -0.320 | 0.23 | 695.1R | -0.31 / -0.34 | -0.43 / -0.24 | 0/5 ✗ | -0.48 | ✗  hi 90→108: -0.43R | 0 | 0.27R | 68, -0.29 (-0.27 / -0.36) | 1190 / 31 of 1358 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.32R/trade (needs +0.10R); profit factor 0.23; max drawdown 695.1R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 575 | 42.1 | -0.344 | 0.52 | 200.9R | -0.32 / -0.41 | -0.31 / -0.36 | 0/5 ✗ | -0.49 | ✗  stop atr 1.5→1.2: -0.42R | 0 | 0.29R | 42, -0.69 (-0.47 / -0.96) | 100 / 54 of 215 | 0 | not cost-viable: fees + slippage 0.29R per trade (stop must be ≥ 4x the round-trip cost); avg -0.34R/trade (needs +0.10R); profit factor 0.52; max drawdown 200.9R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 605 | 26.0 | -0.424 | 0.56 | 265.0R | -0.41 / -0.45 | -0.55 / -0.32 | 1/5 ✗ | -0.60 | ✗  n 20→24: -0.49R | 2 | 0.32R | 17, +0.15 (+0.64 / -0.41) | 438 / 1060 of 1683 | 0 | not cost-viable: fees + slippage 0.32R per trade (stop must be ≥ 4x the round-trip cost); avg -0.42R/trade (needs +0.10R); profit factor 0.56; max drawdown 265.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 333 | 38.7 | -0.434 | 0.41 | 144.7R | -0.42 / -0.46 | -0.46 / -0.41 | 0/5 ✗ | -0.58 | ✗  stop atr 1.0→0.8: -0.49R | 1 | 0.26R | 10, -0.44 (-0.29 / -0.59) | 111 / 225 of 359 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.43R/trade (needs +0.10R); profit factor 0.41; max drawdown 144.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 582 | 39.5 | -0.466 | 0.4 | 272.9R | -0.44 / -0.55 | -0.61 / -0.40 | 0/5 ✗ | -0.67 | ✗  stop atr 1.0→0.8: -0.54R | 0 | 0.37R | 27, -0.43 (-0.51 / -0.34) | 96 / 259 of 385 | 0 | not cost-viable: fees + slippage 0.37R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R); profit factor 0.40; max drawdown 272.9R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 111 | 18.9 | -0.556 | 0.44 | 64.0R | -0.44 / -0.79 | -0.66 / -0.46 | 1/5 ✗ | -0.70 | ✗  stop buffer_atr 0.2→0.16: -0.56R | 0 | 0.24R | 3, -0.07 (-1.25 / +2.29) | 32 / 108 of 150 | 0 | avg -0.56R/trade (needs +0.10R); profit factor 0.44; max drawdown 64.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 276 | 29.7 | -0.716 | 0.25 | 197.6R | -0.78 / -0.61 | -0.68 / -0.86 | 0/5 ✗ | -1.08 | ✗  stop atr 1.5→1.2: -0.90R | 0 | 0.55R | 65, -0.51 (-0.47 / -0.58) | 203 / 74 of 344 | 0 | not cost-viable: fees + slippage 0.55R per trade (stop must be ≥ 4x the round-trip cost); avg -0.72R/trade (needs +0.10R); profit factor 0.25; max drawdown 197.6R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 423 | 26.5 | -1.137 | 0.16 | 484.2R | -1.18 / -1.09 | -1.05 / -1.66 | 0/5 ✗ | -1.79 | ✗  stop atr 1.0→0.8: -1.47R | 0 | 1.02R | 116, -1.19 (-1.38 / -1.00) | 185 / 620 of 927 | 0 | not cost-viable: fees + slippage 1.02R per trade (stop must be ≥ 4x the round-trip cost); avg -1.14R/trade (needs +0.10R); profit factor 0.16; max drawdown 484.2R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **20** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 46 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.06** (Bonferroni: family-wise false-winner rate 0.05 over 46 trials; with 1 trial it would be 1.65).

**Research run duration:** 10.1 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 20 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (113.9 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 25 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

🧪 **Strategy lab:** 2 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 15m | 6 | +0.839 | +2.214 | +0.250 | +0.561 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 8 | +0.108 | -1.323 | -0.001 | -0.408 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.149 | -0.436 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +2.214 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 4 | -1.218 | -1.163 | -0.340 | -0.274 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 1 | -1.712 | -1.712 | -0.673 | -0.871 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 283 | -0.125 | -0.307 | -0.214 | -0.240 | no |
| S8-PDH-PDL-SWEEP | 30m | 111 | -0.556 | -0.791 | -0.424 | -0.450 | no |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): donchian_breakout@1.0 4h FAILED → BACKTESTING

### 3c. Research layers (daily run)
Last run: **2026-09-26 06:28 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 10 | 2017-08-17 | 2026-09-26 | 19946 |  |
| 1h | 10 | 2017-08-17 | 2026-09-26 | 79722 |  |
| 30m | 10 | 2024-09-26 | 2026-09-26 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 10 | 2025-09-26 | 2026-09-26 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 10 | 2026-06-28 | 2026-09-26 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout | 4h | BACKTESTING | 1105 (503) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 64%, stop_too_tight 34% | +0.33R | -0.37R | +0.18 / +0.12 |
| bb_squeeze_breakout | 4h | FAILED | 277 (134) | false_breakout, stop_too_tight, structural_change | false_breakout 57%, stop_too_tight 40% | +0.35R | -0.33R | +0.11 / +0.03 |
| bb_squeeze_breakout | 1h | FAILED | 832 (388) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 62%, no_displacement 52%, stop_too_tight 36%, regime_mismatch 34% | +0.35R | -0.45R | +0.16 / -0.01 |
| donchian_breakout | 1h | FAILED | 3064 (1567) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 31%, regime_mismatch 25% | +0.37R | -0.40R | +0.06 / -0.05 |
| supertrend_flip | 4h | FAILED | 92 (48) | regime_mismatch, stop_too_tight, indicator_lag, structural_change | regime_mismatch 69%, indicator_lag 42%, stop_too_tight 27% | +0.36R | -0.44R | +0.01 / -0.06 |
| macd_trend_cross | 4h | FAILED | 38 (19) | structural_change | no_displacement 90%, regime_mismatch 90%, low_relative_volume 53%, indicator_lag 53% | +0.21R | -0.44R | +0.02 / -0.06 |
| donchian_breakout | 30m | FAILED | 1329 (685) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 76%, stop_too_tight 33% | +0.29R | -0.41R | +0.09 / -0.07 |
| trend_pullback | 4h | FAILED | 1218 (635) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 39%, stop_too_tight 26% | +0.35R | -0.42R | +0.01 / -0.07 |
| macd_trend_cross | 1h | FAILED | 186 (96) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 92%, indicator_lag 38%, stop_too_tight 30% | +0.31R | -0.41R | +0.07 / -0.09 |
| rsi2_dip_buy | 4h | FAILED | 1841 (811) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 44% | +0.16R | -0.21R | -0.05 / -0.11 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 283 (189) | stop_too_tight, sweep_continued | sweep_continued 97%, range_market 56%, stop_too_tight 33% | +0.55R | -0.44R | +0.12 / -0.12 |
| rsi2_dip_buy | 1h | FAILED | 6989 (3243) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 41% | +0.16R | -0.20R | +0.00 / -0.13 |
| ema_9_21_cross | 1h | FAILED | 335 (189) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 78%, indicator_lag 49%, stop_too_tight 25% | +0.26R | -0.39R | +0.01 / -0.13 |
| trend_pullback | 1h | FAILED | 6338 (3348) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 76%, indicator_lag 44%, stop_too_tight 27% | +0.29R | -0.43R | +0.02 / -0.14 |
| S6-OB-FVG-noSMC | 15m | FAILED | 41 (26) | structural_change | - | +0.32R | -0.47R | +0.03 / -0.15 |
| supertrend_flip | 30m | FAILED | 163 (85) | stop_too_tight, indicator_lag | regime_mismatch 46%, indicator_lag 44%, stop_too_tight 33%, overextended_entry 29% | +0.28R | -0.46R | -0.00 / -0.16 |
| ema_9_21_cross | 15m | FAILED | 457 (254) | stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 28% | +0.26R | -0.45R | +0.13 / -0.16 |
| bb_squeeze_breakout | 30m | FAILED | 503 (266) | false_breakout, stop_too_tight | false_breakout 61%, stop_too_tight 40% | +0.28R | -0.43R | +0.07 / -0.18 |
| trend_pullback | 30m | FAILED | 3534 (1896) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 31% | +0.28R | -0.43R | +0.03 / -0.19 |
| rsi2_dip_buy | 30m | FAILED | 2827 (1482) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 33% | +0.17R | -0.19R | +0.01 / -0.19 |
| macd_trend_cross | 30m | FAILED | 296 (155) | overextended_entry, stop_too_tight, indicator_lag | no_displacement 86%, low_relative_volume 46%, indicator_lag 46%, stop_too_tight 29% | +0.30R | -0.45R | +0.04 / -0.20 |
| ema_9_21_cross | 30m | FAILED | 339 (199) | stop_too_tight, indicator_lag | indicator_lag 48%, low_relative_volume 39%, stop_too_tight 27% | +0.26R | -0.41R | -0.00 / -0.21 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 795 (551) | range_market, trend_reversal, stop_too_tight | range_market 46%, stop_too_tight 37% | +0.64R | -0.51R | +0.04 / -0.21 |
| supertrend_flip | 1h | FAILED | 280 (157) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 71%, stop_too_tight 37%, indicator_lag 31% | +0.39R | -0.38R | -0.12 / -0.23 |
| liquidity_sweep_reversal | 1h | FAILED | 294 (156) | trend_reversal, stop_too_tight | stop_too_tight 50% | +0.30R | -0.47R | -0.04 / -0.24 |
| trend_pullback | 15m | FAILED | 3140 (1724) | wrong_session, stop_too_tight, indicator_lag | wrong_session 71%, indicator_lag 49%, stop_too_tight 32% | +0.26R | -0.44R | +0.07 / -0.25 |
| rsi2_dip_buy | 15m | FAILED | 2173 (1400) | trend_reversal, fees_slippage | fees_slippage 44% | +0.16R | -0.19R | +0.01 / -0.32 |
| bb_squeeze_breakout | 15m | FAILED | 575 (333) | stop_too_tight | no_displacement 59%, false_breakout 58%, stop_too_tight 40% | +0.28R | -0.46R | +0.01 / -0.34 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 605 (448) | stop_too_tight | stop_too_tight 33% | +0.59R | -0.48R | -0.03 / -0.42 |
| liquidity_sweep_reversal | 30m | FAILED | 333 (204) | stop_too_tight | stop_too_tight 39% | +0.41R | -0.46R | -0.12 / -0.43 |
| liquidity_sweep_reversal | 15m | FAILED | 582 (352) | stop_too_tight | stop_too_tight 39% | +0.36R | -0.45R | +0.00 / -0.47 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 111 (90) | trend_reversal, stop_too_tight, sweep_continued | sweep_continued 97%, stop_too_tight 30% | +0.46R | -0.67R | -0.23 / -0.56 |
| ema_9_21_cross | 5m | FAILED | 276 (194) | stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 31% | +0.26R | -0.47R | -0.02 / -0.72 |
| liquidity_sweep_reversal | 5m | FAILED | 423 (311) | fees_slippage, stop_too_tight | stop_too_tight 36%, fees_slippage 25% | +0.29R | -0.48R | +0.17 / -1.14 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 28 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `regime_mismatch` (systematic in 12 strategy/timeframe tests); `trend_reversal` (systematic in 8 strategy/timeframe tests); `false_breakout` (systematic in 6 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `fees_slippage` (systematic in 3 strategy/timeframe tests); `no_displacement` (systematic in 2 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- SOL up +4.8% (2026-09-25 07:00 → 2026-09-25 19:00 UTC): identifiable: at least one strategy had a valid signal before the move
- SUI up +13.4% (2026-09-25 08:00 → 2026-09-25 21:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ENA up +18.4% (2026-09-25 08:00 → 2026-09-25 21:00 UTC): identifiable: at least one strategy had a valid signal before the move
- UNI up +8.2% (2026-09-25 07:00 → 2026-09-25 13:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.0 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 95.6 KB | - | - |
| `memory/coin_notes.md` | 0.6 KB | - | - |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 3.3 KB | 6 | 2026-09-26 00:24 UTC |
| `memory/experiments.md` | 36.0 KB | 11 | 2026-09-26 06:40 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 10.0 KB | 11 | 2026-09-25 14:00 UTC |
| `memory/market_regime_log.md` | 3.7 KB | - | - |
| `memory/missed_trades.md` | 8.6 KB | 10 | 2026-09-26 06:28 UTC |
| `memory/playbook.md` | 8.5 KB | - | - |
| `memory/research_sources.md` | 40.2 KB | 32 | 2026-09-26 06:40 UTC |
| `memory/smc_events.csv` | 84.4 KB | - | - |
| `memory/smc_research.md` | 5.7 KB | - | - |
| `memory/strategy_lifecycle.md` | 13.0 KB | - | - |
| `memory/strategy_registry.csv` | 27.2 KB | - | - |
| `memory/trials.csv` | 4.0 KB | - | - |
| `memory/universe_log.md` | 5.2 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*