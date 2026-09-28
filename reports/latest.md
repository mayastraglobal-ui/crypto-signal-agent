# Crypto Signal Report

**Updated:** 2026-09-28 11:20 Beijing time (2026-09-28 03:20 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 6.5 MB (GitHub) · large files of this run 3.4 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-28 03:20 UTC / 2026-09-28 11:20 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US GDP (Third Estimate), 2nd Quarter 2026 2026-09-30 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.04% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| QNT | **DEGRADED** | 1d: DEGRADED: volume 91x normal on candle 09-27 00:00 UTC (possible bad data) |
| VTHO | **DEGRADED** | 1d: DEGRADED: volume 269x normal on candle 09-25 00:00 UTC (possible bad data); 1d: DEGRADED: volume 149x normal on candle 09-27 00:00 UTC (possible bad data) |
- 75 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-28 03:20 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 781 h since 2026-08-26 | +0.0046% | 1.24 | 0.78 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 781 h since 2026-08-26 | +0.0038% | 1.51 | 0.97 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 781 h since 2026-08-26 | -0.0035% | 1.52 | 0.85 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 781 h since 2026-08-26 | +0.0100% | 0.50 | 1.04 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 781 h since 2026-08-26 | +0.0067% | 2.68 | 0.82 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 781 h since 2026-08-26 | +0.0100% | 1.58 | 0.94 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 781 h since 2026-08-26 | +0.0056% | 1.57 | 0.61 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |
| ENA | GOOD | okx | 781 h since 2026-08-26 | +0.0050% | 1.15 | 0.93 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ENAUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 781 h since 2026-08-26 | +0.0100% | 2.26 | 1.52 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **ZEC**, **XRP**, **SUI**, **UNI**
- **Research only** - backtested, never a signal: ENA, BNB, AVAX
- **Changes this run** (also written to `memory/universe_log.md`):
  - **ELIGIBLE** AVAX - passes every rule again

| Not eligible | 24h volume | Why |
|---|---|---|
| QNT | $235M | 7-day average volume $38M < $50M; 24h move +51.4% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $68k within 1% (need $250k) |
| VTHO | $76M | 7-day average volume $34M < $50M; spread 0.136% > 0.1%; order book too thin: $62k within 1% (need $250k) |
| PUMP | $55M | 7-day average volume $31M < $50M; order book too thin: $181k within 1% (need $250k) |

**Flags (not excluded):** QNT: price data DEGRADED - stays in the list, but no signals; VTHO: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, TAO, USD1, USDC, WLD (see `config.yaml`)

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
| UNI | 315 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| ENA | 130 | 909 | 903 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |
| BNB | 464 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| AVAX | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (LH/HL) | 84,843 / 84,342 | 0.07 | 1.76x | 0.85x | displacement_down, bear_engulf, breakout_down, retest_down |
| ETH | down (LH/LL) | 2,699.67 / 2,682.05 | 0.33 | 1.51x | 0.85x | bear_engulf, breakout_down |
| SOL | mixed (LH/HL) | 123.45 / 121.28 | 0.11 | 1.35x | 1.06x | bear_reject, breakout_down |
| ZEC | down (LH/LL) | 1,615.13 / 1,575.3 | 0.23 | 0.80x | 0.83x | bear_reject, breakout_down, retest_down |
| XRP | mixed (LH/HL) | 1.5416 / 1.509 | 0.14 | 1.64x | 0.81x | bear_reject |
| SUI | up (HH/HL) | 1.2947 / 1.2467 | 0.20 | 1.33x | 1.22x | bear_reject, bear_div |
| UNI | down (LH/LL) | 9.809 / 9.5 | 0.21 | 3.46x | 0.94x | displacement_down, breakout_down |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 473 | 48% | 34% | 26% | 80% | 44% | 31% | beats chance | 0.12R |
| 4h | displacement_down | 370 | 49% | 33% | 21% | 75% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1202 | 44% | 31% | 22% | 77% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | bear_engulf | 1372 | 44% | 29% | 20% | 77% | 48% | 32% | worse than chance | 0.08R |
| 4h | bull_reject | 940 | 42% | 28% | 20% | 79% | 43% | 30% | can't tell from chance | 0.12R |
| 4h | bear_reject | 907 | 47% | 33% | 23% | 74% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 657 | 44% | 29% | 21% | 77% | 43% | 30% | can't tell from chance | 0.12R |
| 4h | smc_sweep_bear | 677 | 44% | 29% | 19% | 79% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 271 | 45% | 28% | 21% | 82% | 44% | 31% | can't tell from chance | 0.13R |
| 4h | smc_bos_down | 259 | 50% | 37% | 25% | 69% | 49% | 33% | can't tell from chance | 0.07R |
| 4h | smc_choch_up | 88 | 50% | 32% | 26% | 83% | 44% | 28% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 80 | 42% | 26% | 14% | 76% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 665 | 44% | 28% | 22% | 78% | 44% | 30% | can't tell from chance | 0.12R |
| 4h | smc_fvg_retrace_bear | 689 | 46% | 31% | 20% | 76% | 47% | 32% | can't tell from chance | 0.08R |
| 1h | displacement_up | 608 | 46% | 34% | 28% | 72% | 43% | 30% | can't tell from chance | 0.26R |
| 1h | displacement_down | 427 | 38% | 25% | 15% | 81% | 38% | 24% | can't tell from chance | 0.18R |
| 1h | bull_engulf | 1722 | 40% | 29% | 22% | 75% | 42% | 30% | worse than chance | 0.31R |
| 1h | bear_engulf | 1887 | 39% | 25% | 17% | 79% | 39% | 25% | can't tell from chance | 0.19R |
| 1h | bull_reject | 1412 | 40% | 29% | 22% | 75% | 42% | 30% | can't tell from chance | 0.30R |
| 1h | bear_reject | 1367 | 36% | 24% | 17% | 81% | 39% | 25% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bull | 638 | 42% | 27% | 20% | 76% | 43% | 30% | can't tell from chance | 0.30R |
| 1h | smc_sweep_bear | 720 | 38% | 24% | 15% | 80% | 39% | 25% | can't tell from chance | 0.18R |
| 1h | smc_bos_up | 398 | 44% | 31% | 25% | 77% | 43% | 30% | can't tell from chance | 0.25R |
| 1h | smc_bos_down | 274 | 39% | 28% | 18% | 83% | 39% | 26% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 115 | 48% | 36% | 31% | 70% | 41% | 28% | can't tell from chance | 0.32R |
| 1h | smc_choch_down | 112 | 43% | 29% | 19% | 75% | 38% | 24% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 882 | 45% | 32% | 25% | 72% | 42% | 29% | can't tell from chance | 0.29R |
| 1h | smc_fvg_retrace_bear | 804 | 41% | 28% | 19% | 78% | 38% | 24% | can't tell from chance | 0.19R |
| 30m | displacement_up | 645 | 41% | 31% | 25% | 77% | 43% | 31% | can't tell from chance | 0.28R |
| 30m | displacement_down | 412 | 41% | 25% | 14% | 83% | 37% | 21% | can't tell from chance | 0.19R |
| 30m | bull_engulf | 1751 | 42% | 29% | 22% | 75% | 42% | 30% | can't tell from chance | 0.33R |
| 30m | bear_engulf | 1783 | 36% | 21% | 15% | 82% | 36% | 21% | can't tell from chance | 0.21R |
| 30m | bull_reject | 1329 | 45% | 30% | 22% | 73% | 42% | 30% | beats chance | 0.33R |
| 30m | bear_reject | 1454 | 37% | 22% | 15% | 82% | 36% | 21% | can't tell from chance | 0.20R |
| 30m | smc_sweep_bull | 615 | 41% | 28% | 19% | 75% | 42% | 29% | can't tell from chance | 0.34R |
| 30m | smc_sweep_bear | 643 | 42% | 26% | 18% | 82% | 37% | 21% | beats chance | 0.19R |
| 30m | smc_bos_up | 468 | 43% | 34% | 29% | 75% | 43% | 30% | can't tell from chance | 0.30R |
| 30m | smc_bos_down | 234 | 37% | 22% | 12% | 86% | 36% | 20% | can't tell from chance | 0.24R |
| 30m | smc_choch_up | 101 | 38% | 24% | 19% | 82% | 43% | 32% | can't tell from chance | 0.38R |
| 30m | smc_choch_down | 96 | 36% | 22% | 18% | 80% | 34% | 20% | can't tell from chance | 0.20R |
| 30m | smc_fvg_retrace_bull | 986 | 43% | 30% | 23% | 74% | 42% | 30% | can't tell from chance | 0.33R |
| 30m | smc_fvg_retrace_bear | 790 | 38% | 21% | 15% | 81% | 37% | 21% | can't tell from chance | 0.22R |
| 15m | displacement_up | 466 | 37% | 28% | 20% | 81% | 36% | 26% | can't tell from chance | 0.40R |
| 15m | displacement_down | 454 | 33% | 21% | 12% | 85% | 37% | 23% | can't tell from chance | 0.30R |
| 15m | bull_engulf | 1660 | 36% | 26% | 18% | 79% | 35% | 24% | can't tell from chance | 0.50R |
| 15m | bear_engulf | 1622 | 37% | 24% | 15% | 78% | 37% | 23% | can't tell from chance | 0.29R |
| 15m | bull_reject | 1320 | 35% | 23% | 16% | 80% | 35% | 24% | can't tell from chance | 0.50R |
| 15m | bear_reject | 1440 | 37% | 23% | 15% | 81% | 37% | 23% | can't tell from chance | 0.29R |
| 15m | smc_sweep_bull | 597 | 36% | 25% | 19% | 78% | 36% | 25% | can't tell from chance | 0.47R |
| 15m | smc_sweep_bear | 646 | 38% | 25% | 14% | 83% | 38% | 24% | can't tell from chance | 0.27R |
| 15m | smc_bos_up | 374 | 39% | 28% | 22% | 80% | 36% | 25% | can't tell from chance | 0.39R |
| 15m | smc_bos_down | 346 | 35% | 21% | 14% | 84% | 37% | 24% | can't tell from chance | 0.33R |
| 15m | smc_choch_up | 86 | 33% | 22% | 16% | 81% | 35% | 24% | can't tell from chance | 0.45R |
| 15m | smc_choch_down | 92 | 34% | 23% | 15% | 80% | 38% | 24% | can't tell from chance | 0.32R |
| 15m | smc_fvg_retrace_bull | 1066 | 34% | 24% | 16% | 80% | 35% | 24% | can't tell from chance | 0.48R |
| 15m | smc_fvg_retrace_bear | 983 | 37% | 25% | 17% | 80% | 37% | 23% | can't tell from chance | 0.30R |
| 5m | displacement_up | 1288 | 33% | 22% | 18% | 83% | 29% | 21% | beats chance | 0.78R |
| 5m | displacement_down | 1166 | 27% | 17% | 11% | 87% | 30% | 19% | worse than chance | 0.51R |
| 5m | bull_engulf | 4178 | 27% | 19% | 14% | 82% | 28% | 20% | can't tell from chance | 0.86R |
| 5m | bear_engulf | 4162 | 30% | 20% | 13% | 83% | 30% | 20% | can't tell from chance | 0.52R |
| 5m | bull_reject | 3336 | 27% | 18% | 14% | 81% | 28% | 20% | can't tell from chance | 0.88R |
| 5m | bear_reject | 3691 | 32% | 20% | 13% | 83% | 31% | 20% | can't tell from chance | 0.51R |
| 5m | smc_sweep_bull | 1200 | 30% | 21% | 15% | 80% | 30% | 21% | can't tell from chance | 0.79R |
| 5m | smc_sweep_bear | 1292 | 32% | 23% | 15% | 82% | 31% | 21% | can't tell from chance | 0.45R |
| 5m | smc_bos_up | 830 | 31% | 23% | 18% | 83% | 29% | 20% | can't tell from chance | 0.79R |
| 5m | smc_bos_down | 894 | 28% | 18% | 11% | 88% | 31% | 21% | can't tell from chance | 0.58R |
| 5m | smc_choch_up | 221 | 35% | 26% | 18% | 85% | 29% | 20% | can't tell from chance | 0.90R |
| 5m | smc_choch_down | 222 | 23% | 13% | 8% | 89% | 30% | 19% | worse than chance | 0.56R |
| 5m | smc_fvg_retrace_bull | 3411 | 29% | 20% | 15% | 81% | 28% | 20% | can't tell from chance | 0.87R |
| 5m | smc_fvg_retrace_bear | 3022 | 27% | 18% | 12% | 84% | 30% | 20% | worse than chance | 0.55R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (moderate) | WEAK_BULL (moderate) | COMPRESSION (weak) | RANGE (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H COMPRESSION, 1H RANGE)) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (moderate) | COMPRESSION (weak) | EXPANSION down (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H COMPRESSION, 1H EXPANSION)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (weak) | STRONG_BULL (strong) | RANGE (strong) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | UNCLEAR (weak) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | UNCLEAR (weak) | RANGE (strong) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H RANGE)) |
| **SUI** | UNCLEAR (weak) | EXPANSION up (weak) | STRONG_BULL (moderate) | STRONG_BULL (strong) | LONG allowed (1D/4H/1H bullish, 1W UNCLEAR) |
| **UNI** | EXPANSION up (moderate) | STRONG_BULL (moderate) | WEAK_BULL (weak) | RANGE (weak) | LONG allowed (1D/4H bullish, 1W EXPANSION) |
| **ENA** | TRANSITION (weak) | EXPANSION up (moderate) | STRONG_BULL (moderate) | WEAK_BULL (weak) | LONG allowed (1D/4H/1H bullish, 1W TRANSITION) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (strong) | RANGE (moderate) | RANGE (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H RANGE)) |
| **AVAX** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (weak) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W TRANSITION) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (moderate)** - for: EMA-fast rising (+1.5 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.73x normal, Bollinger width above 56% of the last 100 candles · against: EMAs not lined up
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.5 ATR in 10 candles); ADX 44 = strong trend; candle size 1.05x normal, Bollinger width above 82% of the last 100 candles; volume 0.97x normal · against: swing structure mixed (neutral)
- **4H COMPRESSION (weak)** - for: EMA-fast flat (+0.7 ATR in 10 candles); ADX 15 = weak trend / ranging; candle size 0.79x normal, Bollinger width above 8% of the last 100 candles · against: close above EMA-fast above EMA-slow; swing structure up (HH/HL)
- **1H RANGE (strong)** - for: EMAs not lined up; EMA-fast flat (-0.1 ATR in 10 candles); swing structure mixed; ADX 14 = weak trend / ranging; candle size 0.85x normal, Bollinger width above 85% of the last 100 candles · against: -

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **Asia**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (CHOCH 8 candles ago) | sell-side (bullish idea) 4 candles ago | bear 84,886.92-85,550.30 (retraced) | bear 86,133.40-86,975.51 | below the range (-184%) | swing high 85,159.03 (4.82 ATR) | swing low 83,183.00 (0.65 ATR) |
| **ETH** | down (BOS 8 candles ago) | sell-side (bullish idea) 1 candles ago | bear 2,694.95-2,704.41 (retraced) | bear 2,745.99-2,784.40 | below the range (-165%) | swing high 2,724.12 (4.8 ATR) | swing low 2,600.15 (3.57 ATR) |
| **SOL** | down (BOS 5 candles ago) | buy-side (bearish idea) 78 candles ago | bear 120.37-120.61 (retraced) | bull 115.86-117.34 | below the range (-57%) | swing high 123.45 (2.9 ATR) | swing low 119.82 (0.2 ATR) |
| **ZEC** | down (BOS 0 candles ago) | sell-side (bullish idea) 4 candles ago | bear 1,608.30-1,618.45 (retraced) | bull 1,527.56-1,540.22 | below the range (-14%) | swing high 1,615.13 (2.17 ATR) | swing low 1,517.41 (2.49 ATR) |
| **XRP** | down (BOS 2 candles ago) | sell-side (bullish idea) 5 candles ago | bear 1.6015-1.6117 (retraced) | bull 1.3773-1.3856 | below the range (-38%) | swing high 1.5416 (2.89 ATR) | swing low 1.4517 (2.88 ATR) |
| **SUI** | down (BOS 0 candles ago) | sell-side (bullish idea) 1 candles ago | bull 1.2013-1.2278 (retraced) | bull 1.0050-1.0598 | discount (5%) | PDH 1.2947 (1.79 ATR) | swing low 1.2247 (0.96 ATR) |
| **UNI** | up (BOS 35 candles ago) | sell-side (bullish idea) 2 candles ago | bear 9.4590-9.4880 (retraced) | bull 8.6780-9.0640 | below the range (-26%) | swing high 9.8090 (2.49 ATR) | swing low 9.3730 (0.31 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 74 (Greed), yesterday 70  (extreme fear/greed = bigger, faster moves)

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
- **Event calendar (next 7 days):** US GDP (Third Estimate), 2nd Quarter 2026 2026-09-30 12:30 UTC, US PCE / Personal Income and Outlays (Aug data) 2026-09-30 12:30 UTC, US jobs report / Employment Situation (Sep data) 2026-10-02 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-09-28 00:52 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 60.0 | +1.221 | 3.69 | 2.3R | +0.97 / +2.21 | +2.21 / +0.97 | 0/5 ✗ | +1.10 | +0.98 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 25 / 12 of 38 | 0 | only 5 trades; only 1 unseen-test trades |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 15 | 46.7 | +0.338 | 1.46 | 4.1R | +0.23 / +0.56 | +0.18 / +0.44 | 0/5 ✗ | +0.03 | -0.15 | ✗  sweep_bars 8→10: -0.00R | 0 | 0.31R | 2, +0.31 (+0.31 / +0.00) | 53 / 26 of 85 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); only 15 trades; only 5 unseen-test trades |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 939 | 40.6 | +0.226 | 1.42 | 24.2R | +0.21 / +0.26 | +0.26 / +0.18 | 5/5 | +0.19 | +0.17 | stable | 9 | 0.04R | 14, +0.81 (+0.81 / +0.00) | 93 / 47 of 266 | 0 | max drawdown 24.2R |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **BACKTESTING** | 939 | 40.6 | +0.226 | 1.42 | 24.2R | +0.21 / +0.26 | +0.26 / +0.18 | 5/5 | +0.19 | +0.17 | stable | 9 | 0.04R | 14, +0.81 (+0.81 / +0.00) | 93 / 47 of 266 | 0 | max drawdown 24.2R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1067 | 40.1 | +0.220 | 1.4 | 23.7R | +0.21 / +0.23 | +0.23 / +0.21 | 5/5 | +0.19 | +0.16 | stable | 9 | 0.05R | 14, +1.02 (+1.02 / +0.00) | 157 / 60 of 358 | 0 | max drawdown 23.7R |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.206 | 1.21 | 3.3R | +0.51 / -1.32 | -1.32 / +0.51 | 0/5 ✗ | +0.08 | -0.03 | ✗  sweep_bars 20→24: -0.16R | 0 | 0.26R | 1, -1.32 (-1.32 / +0.00) | 39 / 15 of 61 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 6 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 965 | 54.8 | +0.129 | 1.29 | 21.2R | +0.12 / +0.15 | +0.13 / +0.13 | 5/5 | +0.10 | +0.07 | stable | 7 | 0.04R | 15, +0.35 (+0.35 / +0.00) | 93 / 47 of 266 | 0 | max drawdown 21.2R |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.78 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.79 (+0.00 / +1.79) | 33 / 106 of 151 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 3 / 5 of 8 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 62 / 15 of 80 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 39 / 15 of 61 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 3 / 5 of 8 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 25 / 12 of 38 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 11 | 27.3 | -0.198 | 0.62 | 2.7R | -0.39 / +0.14 | -1.11 / -0.11 | 0/5 ✗ | -0.30 | -0.24 | ✗  stop max_width_atr 3.0→3.6: -0.20R | 0 | 0.08R | 0, +0.00 (+0.00 / +0.00) | 554 / 193 of 896 | 0 | only 11 trades; avg -0.20R/trade (needs +0.10R); profit factor 0.62; only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 13 | 46.2 | -0.308 | 0.48 | 5.9R | -0.37 / +0.05 | -0.31 / -0.31 | 0/5 ✗ | -0.30 | -0.54 | ✗  time_stop_bars 30→24: -0.36R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 446 / 248 of 840 | 0 | only 13 trades; avg -0.31R/trade (needs +0.10R); profit factor 0.48; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 4 | 0.0 | -1.218 | 0.0 | 4.9R | -1.24 / -1.16 | -1.42 / -1.15 | 0/5 ✗ | -1.22 | -1.29 | ✗  stop buffer_atr 0.2→0.16: -1.23R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 62 / 15 of 80 | 0 | only 4 trades; avg -1.22R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 248 | 52.4 | +0.048 | 1.09 | 24.8R | +0.23 / -0.29 | +0.13 / -0.03 | 3/5 | -0.00 | -0.05 | ✗  stop atr 1.5→1.8: -0.00R | 6 | 0.07R | 2, +0.08 (+0.08 / +0.00) | 100 / 22 of 140 | 0 | avg +0.05R/trade (needs +0.10R); profit factor 1.09; max drawdown 24.8R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 748 | 52.9 | -0.009 | 0.98 | 43.2R | -0.02 / +0.02 | -0.07 / +0.06 | 2/5 ✗ | -0.09 | -0.17 | ✗  bb_k 2→1: -0.06R | 4 | 0.14R | 6, +0.05 (+0.28 / -0.07) | 143 / 42 of 222 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 43.2R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1168 | 34.8 | -0.019 | 0.97 | 82.5R | -0.04 / +0.04 | +0.04 / -0.08 | 2/5 ✗ | -0.10 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 4 | 0.12R | 53, +0.12 (+0.27 / -0.51) | 147 / 39 of 369 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 82.5R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FAILED** | 1168 | 34.8 | -0.019 | 0.97 | 82.5R | -0.04 / +0.04 | +0.04 / -0.08 | 2/5 ✗ | -0.10 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 4 | 0.12R | 53, +0.12 (+0.27 / -0.51) | 147 / 39 of 369 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 82.5R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1379 | 34.3 | -0.040 | 0.94 | 101.7R | -0.06 / +0.03 | +0.01 / -0.09 | 2/5 ✗ | -0.12 | -0.20 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.13R | 58, +0.09 (+0.27 / -0.41) | 257 / 61 of 529 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; max drawdown 101.7R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 31 | 51.6 | -0.047 | 0.91 | 5.6R | +0.07 / -0.33 | +0.22 / -0.37 | 1/5 ✗ | -0.08 | -0.11 | ✗  time_stop_bars 40→32: -0.07R | 1 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 160 / 5 of 167 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; only 9 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 2952 | 32.3 | -0.048 | 0.92 | 232.5R | -0.08 / +0.02 | -0.03 / -0.07 | 2/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.09R | 36, +0.47 (+0.55 / +0.10) | 216 / 131 of 575 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 232.5R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 167 | 49.7 | -0.050 | 0.91 | 29.8R | -0.17 / +0.21 | -0.09 / -0.01 | 2/5 ✗ | -0.11 | -0.18 | ✗  stop atr 1.5→1.2: -0.14R | 3 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 218 / 6 of 226 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 29.8R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1199 | 49.8 | -0.051 | 0.9 | 91.4R | -0.06 / -0.03 | -0.02 / -0.08 | 1/5 ✗ | -0.13 | -0.20 | ✗  stop atr 2.0→1.6: -0.13R | 3 | 0.12R | 53, +0.07 (+0.16 / -0.29) | 147 / 39 of 369 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.90; max drawdown 91.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2599 | 32.1 | -0.054 | 0.92 | 214.7R | -0.09 / +0.03 | -0.04 / -0.07 | 1/5 ✗ | -0.10 | -0.15 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 33, +0.45 (+0.54 / -0.19) | 128 / 94 of 418 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 214.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FAILED** | 2599 | 32.1 | -0.054 | 0.92 | 215.6R | -0.09 / +0.03 | -0.04 / -0.07 | 1/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 33, +0.45 (+0.54 / -0.19) | 128 / 94 of 418 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 215.6R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2669 | 48.1 | -0.060 | 0.89 | 188.0R | -0.07 / -0.03 | -0.07 / -0.05 | 0/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.07R | 1 | 0.09R | 34, +0.36 (+0.45 / -0.34) | 128 / 94 of 418 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 188.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1063 | 48.4 | -0.065 | 0.88 | 115.0R | -0.01 / -0.18 | -0.01 / -0.13 | 1/5 ✗ | -0.11 | -0.14 | ✗  long_rsi_hi 65→52: -0.14R | 3 | 0.06R | 6, +1.14 (+1.14 / +0.00) | 665 / 198 of 1027 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 115.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 83 | 47.0 | -0.093 | 0.83 | 16.4R | +0.05 / -0.34 | -0.10 / -0.08 | 3/5 ✗ | -0.12 | -0.14 | ✗  time_stop_bars 60→48: -0.09R | 1 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 44 / 6 of 52 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.83; max drawdown 16.4R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1612 | 55.8 | -0.111 | 0.62 | 179.7R | -0.10 / -0.13 | -0.13 / -0.09 | 0/5 ✗ | -0.14 | -0.17 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.05R | 9, -0.07 (-0.07 / +0.00) | 744 / 4 of 1003 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.62; max drawdown 179.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 310 | 44.2 | -0.115 | 0.79 | 47.9R | -0.13 / -0.09 | -0.18 / -0.04 | 0/5 ✗ | -0.18 | -0.26 | ✗  slow 21→17: -0.20R | 3 | 0.12R | 4, -0.30 (-1.00 / +1.82) | 151 / 9 of 169 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.79; max drawdown 47.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 6112 | 53.6 | -0.132 | 0.54 | 811.5R | -0.11 / -0.18 | -0.14 / -0.12 | 0/5 ✗ | -0.20 | -0.27 | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 44, -0.12 (-0.14 / -0.10) | 1056 / 4 of 1400 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.54; max drawdown 811.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 255 | 33.3 | -0.138 | 0.82 | 53.6R | -0.02 / -0.41 | -0.37 / +0.12 | 1/5 ✗ | -0.24 | -0.35 | ✗  time_stop_bars 30→36: -0.17R | 1 | 0.20R | 3, +0.86 (+0.00 / +0.86) | 91 / 216 of 317 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.82; max drawdown 53.6R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 5541 | 47.3 | -0.139 | 0.76 | 778.8R | -0.14 / -0.13 | -0.17 / -0.10 | 0/5 ✗ | -0.21 | -0.28 | ✗  stop atr 1.5→1.2: -0.18R | 1 | 0.13R | 53, -0.06 (+0.07 / -0.39) | 1161 / 296 of 1837 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 778.8R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 85 | 36.5 | -0.147 | 0.79 | 22.0R | -0.32 / +0.32 | -0.20 / -0.12 | 1/5 ✗ | -0.21 | -0.31 | ✗  depth 0.985→1.182: -0.45R | 2 | 0.15R | 2, +1.30 (+1.34 / +1.27) | 47 / 6 of 55 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.79; max drawdown 22.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 412 | 45.4 | -0.155 | 0.74 | 65.3R | -0.14 / -0.20 | -0.23 / -0.12 | 1/5 ✗ | -0.30 | -0.43 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.25R | 22, -0.21 (+0.12 / -1.09) | 66 / 15 of 105 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.74; max drawdown 65.3R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 41 | 36.6 | -0.161 | 0.77 | 11.3R | +0.11 / -0.50 | -0.40 / +0.06 | 1/5 ✗ | -0.33 | -0.41 | ✗  stop buffer_atr 0.2→0.16: -0.16R | 3 | 0.15R | 7, -0.82 (-0.59 / -1.40) | 101 / 37 of 152 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.77; max drawdown 11.3R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 235 | 38.7 | -0.165 | 0.75 | 59.0R | -0.18 / -0.12 | +0.12 / -0.35 | 1/5 ✗ | -0.21 | -0.27 | ✗  depth 0.985→1.182: -0.29R | 1 | 0.10R | 6, +0.50 (+0.70 / +0.46) | 90 / 7 of 112 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.75; max drawdown 59.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 147 | 46.9 | -0.174 | 0.69 | 26.0R | -0.18 / -0.15 | -0.14 / -0.20 | 2/5 ✗ | -0.24 | -0.33 | ✗  adx_min 20→24: -0.25R | 1 | 0.13R | 7, -0.37 (-0.37 / +0.00) | 57 / 5 of 72 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.69; max drawdown 26.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 461 | 46.9 | -0.180 | 0.71 | 84.7R | -0.23 / -0.05 | -0.24 / -0.12 | 1/5 ✗ | -0.29 | -0.41 | ✗  stop atr 1.5→1.2: -0.25R | 1 | 0.18R | 20, -0.47 (-0.37 / -0.63) | 126 / 35 of 207 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.71; max drawdown 84.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3200 | 46.2 | -0.195 | 0.68 | 630.5R | -0.18 / -0.23 | -0.22 / -0.17 | 0/5 ✗ | -0.31 | -0.42 | ✗  stop atr 1.5→1.2: -0.26R | 0 | 0.18R | 102, -0.08 (+0.25 / -0.74) | 907 / 236 of 1730 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 630.5R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2514 | 46.8 | -0.198 | 0.4 | 498.6R | -0.18 / -0.24 | -0.25 / -0.15 | 0/5 ✗ | -0.30 | -0.41 | ✗  hi 90→108: -0.25R | 0 | 0.17R | 47, +0.02 (+0.03 / +0.01) | 1046 / 22 of 1279 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.40; max drawdown 498.6R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 268 | 47.4 | -0.208 | 0.66 | 62.1R | -0.13 / -0.41 | -0.35 / -0.08 | 0/5 ✗ | -0.33 | -0.42 | ✗  stop atr 1.5→1.2: -0.29R | 1 | 0.19R | 6, -0.48 (-0.10 / -1.24) | 194 / 11 of 224 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.66; max drawdown 62.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 273 | 47.6 | -0.211 | 0.65 | 58.6R | -0.22 / -0.20 | -0.23 / -0.19 | 0/5 ✗ | -0.29 | -0.38 | ✗  vol_x 1.2→1.44: -0.36R | 2 | 0.17R | 5, -0.41 (+0.01 / -0.69) | 101 / 212 of 322 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.65; max drawdown 58.6R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 300 | 40.7 | -0.219 | 0.63 | 69.5R | -0.20 / -0.29 | -0.29 / -0.16 | 1/5 ✗ | -0.32 | -0.41 | ✗  fast 9→11: -0.30R | 0 | 0.17R | 12, -0.01 (+0.09 / -1.18) | 110 / 17 of 145 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.63; max drawdown 69.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 718 | 30.8 | -0.221 | 0.73 | 183.8R | -0.22 / -0.23 | -0.31 / -0.14 | 1/5 ✗ | -0.33 | -0.43 | ✗  stop buffer_atr 0.2→0.16: -0.26R | 1 | 0.22R | 12, -0.05 (+0.87 / -0.70) | 464 / 1138 of 1684 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.73; max drawdown 183.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 249 | 43.4 | -0.239 | 0.61 | 63.0R | -0.26 / -0.20 | -0.34 / -0.14 | 0/5 ✗ | -0.30 | -0.35 | ✗  st_n 10→12: -0.25R | 1 | 0.08R | 5, +0.39 (+0.39 / +0.00) | 56 / 3 of 68 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.61; max drawdown 63.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 2822 | 44.7 | -0.258 | 0.61 | 733.4R | -0.24 / -0.31 | -0.30 / -0.24 | 0/5 ✗ | -0.41 | -0.57 | ✗  stop atr 1.5→1.2: -0.34R | 0 | 0.25R | 196, -0.16 (+0.08 / -0.81) | 1318 / 341 of 2301 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 733.4R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1123 | 29.6 | -0.308 | 0.61 | 347.5R | -0.33 / -0.26 | -0.31 / -0.31 | 0/5 ✗ | -0.39 | -0.46 | ✗  rsi_n 14→17: -0.38R | 1 | 0.14R | 11, -0.35 (-0.54 / +0.54) | 766 / 9 of 820 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.61; max drawdown 347.5R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1364 | 31.7 | -0.313 | 0.61 | 433.6R | -0.32 / -0.30 | -0.31 / -0.31 | 0/5 ✗ | -0.44 | -0.57 | ✗  stop atr 1.5→1.2: -0.35R | 0 | 0.21R | 34, -0.12 (-0.40 / +0.33) | 602 / 24 of 719 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.61; max drawdown 433.6R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 1952 | 35.0 | -0.325 | 0.22 | 636.0R | -0.31 / -0.36 | -0.42 / -0.25 | 0/5 ✗ | -0.49 | -0.67 | ✗  hi 90→108: -0.42R | 0 | 0.28R | 69, -0.25 (-0.21 / -0.36) | 1254 / 33 of 1405 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.33R/trade (needs +0.10R); profit factor 0.22; max drawdown 636.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 524 | 41.6 | -0.350 | 0.51 | 191.5R | -0.32 / -0.42 | -0.32 / -0.37 | 0/5 ✗ | -0.50 | -0.64 | ✗  stop atr 1.5→1.2: -0.42R | 0 | 0.28R | 41, -0.63 (-0.58 / -0.81) | 101 / 55 of 216 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.35R/trade (needs +0.10R); profit factor 0.51; max drawdown 191.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 559 | 24.9 | -0.461 | 0.53 | 266.0R | -0.48 / -0.41 | -0.56 / -0.36 | 1/5 ✗ | -0.63 | -0.76 | ✗  n 20→24: -0.51R | 1 | 0.33R | 20, +0.07 (+0.96 / -0.83) | 454 / 1032 of 1678 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.53; max drawdown 266.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 525 | 39.2 | -0.476 | 0.4 | 250.2R | -0.45 / -0.57 | -0.57 / -0.42 | 0/5 ✗ | -0.68 | -0.92 | ✗  stop atr 1.0→0.8: -0.54R | 0 | 0.37R | 31, -0.58 (-0.46 / -0.73) | 104 / 243 of 382 | 0 | not cost-viable: fees + slippage 0.37R per trade (stop must be ≥ 4x the round-trip cost); avg -0.48R/trade (needs +0.10R); profit factor 0.40; max drawdown 250.2R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 103 | 20.4 | -0.481 | 0.51 | 56.1R | -0.40 / -0.65 | -0.56 / -0.40 | 0/5 ✗ | -0.63 | -0.77 | ✗  stop max_width_atr 3.0→2.4: -0.48R | 1 | 0.25R | 5, +0.20 (-1.25 / +1.17) | 33 / 106 of 151 | 0 | avg -0.48R/trade (needs +0.10R); profit factor 0.51; max drawdown 56.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 297 | 35.7 | -0.510 | 0.35 | 151.5R | -0.49 / -0.57 | -0.51 / -0.51 | 0/5 ✗ | -0.66 | -0.81 | ✗  stop atr 1.0→0.8: -0.56R | 0 | 0.28R | 12, -0.59 (-0.37 / -0.80) | 113 / 224 of 363 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.51R/trade (needs +0.10R); profit factor 0.35; max drawdown 151.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 266 | 30.5 | -0.711 | 0.25 | 189.2R | -0.78 / -0.60 | -0.68 / -0.92 | 0/5 ✗ | -1.07 | -1.42 | ✗  stop atr 1.5→1.2: -0.91R | 0 | 0.54R | 80, -0.47 (-0.46 / -0.51) | 234 / 58 of 372 | 0 | not cost-viable: fees + slippage 0.54R per trade (stop must be ≥ 4x the round-trip cost); avg -0.71R/trade (needs +0.10R); profit factor 0.25; max drawdown 189.2R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 426 | 25.4 | -1.188 | 0.15 | 505.9R | -1.24 / -1.13 | -1.08 / -1.96 | 0/5 ✗ | -1.85 | -2.51 | ✗  stop atr 1.0→0.8: -1.51R | 0 | 1.05R | 138, -1.20 (-1.37 / -0.94) | 224 / 608 of 974 | 0 | not cost-viable: fees + slippage 1.05R per trade (stop must be ≥ 4x the round-trip cost); avg -1.19R/trade (needs +0.10R); profit factor 0.15; max drawdown 505.9R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **25** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 118 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.34** (Bonferroni: family-wise false-winner rate 0.05 over 118 trials; with 1 trial it would be 1.65).

**Research run duration:** 9.2 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 25 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (107.2 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 36 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

1 of 59 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 5.88 | 15.9R | 592 d (18%) | passes every gate |

🧪 **Strategy lab:** 5 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 15m | 5 | +1.221 | +2.214 | +0.338 | +0.561 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 6 | +0.206 | -1.323 | -0.308 | +0.049 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 2 | +0.037 | +0.037 | -0.535 | -0.443 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.161 | -0.502 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +2.214 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 4 | -1.218 | -1.163 | -0.198 | +0.138 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 255 | -0.138 | -0.411 | -0.221 | -0.227 | no |
| S8-PDH-PDL-SWEEP | 30m | 103 | -0.481 | -0.646 | -0.461 | -0.409 | no |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): R4-CLUC@1.0 15m FORMALIZED → FAILED; R4-CLUC@1.0 30m FORMALIZED → FAILED; bb_squeeze_breakout@1.0 1h BACKTESTING → FAILED; donchian_breakout-VEXIT-S4@1.0 1h FORMALIZED → FAILED; donchian_breakout-VEXIT-S4@1.0 30m FORMALIZED → FAILED; donchian_breakout-VEXIT-S4@1.0 4h FORMALIZED → BACKTESTING; donchian_breakout-VEXIT-VRVOL@1.0 1h FORMALIZED → FAILED; donchian_breakout-VEXIT-VRVOL@1.0 30m FORMALIZED → FAILED; donchian_breakout-VEXIT-VRVOL@1.0 4h FORMALIZED → BACKTESTING; macd_trend_cross@1.0 4h BACKTESTING → FAILED

### 3c. Research layers (daily run)
Last run: **2026-09-28 00:52 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 9 | 2017-08-17 | 2026-09-27 | 19957 |  |
| 1h | 9 | 2017-08-17 | 2026-09-27 | 79764 |  |
| 30m | 9 | 2024-09-28 | 2026-09-28 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 9 | 2025-09-28 | 2026-09-28 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 9 | 2026-06-30 | 2026-09-28 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 939 (558) | false_breakout, trend_reversal | false_breakout 63%, no_displacement 32% | +0.47R | -0.37R | +0.28 / +0.23 |
| donchian_breakout-VEXIT-VRVOL | 4h | BACKTESTING | 939 (558) | false_breakout, trend_reversal | false_breakout 63%, no_displacement 32% | +0.47R | -0.37R | +0.28 / +0.23 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 1067 (639) | false_breakout | false_breakout 62% | +0.47R | -0.37R | +0.28 / +0.22 |
| donchian_breakout | 4h | BACKTESTING | 965 (436) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 65%, stop_too_tight 34% | +0.33R | -0.37R | +0.19 / +0.13 |
| bb_squeeze_breakout | 4h | FAILED | 248 (118) | false_breakout, stop_too_tight, structural_change | false_breakout 56%, stop_too_tight 42% | +0.34R | -0.33R | +0.14 / +0.05 |
| bb_squeeze_breakout | 1h | FAILED | 748 (352) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, no_displacement 52%, stop_too_tight 37%, regime_mismatch 35% | +0.35R | -0.44R | +0.17 / -0.01 |
| donchian_breakout-VEXIT | 30m | FAILED | 1168 (761) | false_breakout | false_breakout 72% | +0.49R | -0.39R | +0.14 / -0.02 |
| donchian_breakout-VEXIT-VRVOL | 30m | FAILED | 1168 (761) | false_breakout | false_breakout 72% | +0.49R | -0.39R | +0.14 / -0.02 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1379 (906) | false_breakout | false_breakout 73% | +0.47R | -0.40R | +0.12 / -0.04 |
| macd_trend_cross | 4h | FAILED | 31 (15) | none | regime_mismatch 93%, no_displacement 87%, low_relative_volume 53%, indicator_lag 53% | +0.17R | -0.39R | +0.04 / -0.05 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2952 (1998) | false_breakout, regime_mismatch | false_breakout 64% | +0.51R | -0.38R | +0.06 / -0.05 |
| macd_trend_cross | 1h | FAILED | 167 (84) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 92%, indicator_lag 37%, stop_too_tight 31% | +0.32R | -0.40R | +0.11 / -0.05 |
| donchian_breakout | 30m | FAILED | 1199 (602) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 76%, stop_too_tight 33% | +0.30R | -0.41R | +0.11 / -0.05 |
| donchian_breakout-VEXIT | 1h | FAILED | 2599 (1766) | false_breakout | false_breakout 63% | +0.52R | -0.38R | +0.05 / -0.05 |
| donchian_breakout-VEXIT-VRVOL | 1h | FAILED | 2599 (1766) | false_breakout | false_breakout 63% | +0.52R | -0.38R | +0.05 / -0.05 |
| donchian_breakout | 1h | FAILED | 2669 (1385) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 32%, regime_mismatch 25% | +0.37R | -0.39R | +0.05 / -0.06 |
| trend_pullback | 4h | FAILED | 1063 (548) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 39%, stop_too_tight 26% | +0.35R | -0.42R | +0.01 / -0.07 |
| supertrend_flip | 4h | FAILED | 83 (44) | stop_too_tight, indicator_lag, structural_change | regime_mismatch 68%, indicator_lag 39%, stop_too_tight 25% | +0.39R | -0.45R | -0.03 / -0.09 |
| rsi2_dip_buy | 4h | FAILED | 1612 (713) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 45% | +0.16R | -0.21R | -0.05 / -0.11 |
| ema_9_21_cross | 1h | FAILED | 310 (173) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 79%, indicator_lag 47%, stop_too_tight 25% | +0.28R | -0.41R | +0.04 / -0.12 |
| rsi2_dip_buy | 1h | FAILED | 6112 (2839) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 42% | +0.16R | -0.20R | +0.00 / -0.13 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 255 (170) | stop_too_tight, sweep_continued | sweep_continued 97%, range_market 56%, stop_too_tight 30% | +0.57R | -0.44R | +0.11 / -0.14 |
| trend_pullback | 1h | FAILED | 5541 (2920) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 76%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.43R | +0.02 / -0.14 |
| R4-CLUC | 15m | FAILED | 85 (54) | none | - | +0.42R | -0.27R | +0.01 / -0.15 |
| ema_9_21_cross | 15m | FAILED | 412 (225) | stop_too_tight, indicator_lag | indicator_lag 47%, stop_too_tight 27% | +0.26R | -0.44R | +0.15 / -0.15 |
| S6-OB-FVG-noSMC | 15m | FAILED | 41 (26) | structural_change | stop_too_wide 88% | +0.24R | -0.47R | +0.03 / -0.16 |
| R4-CLUC | 30m | FAILED | 235 (144) | volatility_spike | - | +0.36R | -0.45R | -0.06 / -0.17 |
| supertrend_flip | 30m | FAILED | 147 (78) | stop_too_tight, indicator_lag | regime_mismatch 44%, indicator_lag 41%, stop_too_tight 35%, late_entry 27% | +0.31R | -0.44R | -0.01 / -0.17 |
| bb_squeeze_breakout | 30m | FAILED | 461 (245) | false_breakout, stop_too_tight | false_breakout 62%, stop_too_tight 38% | +0.28R | -0.43R | +0.08 / -0.18 |
| trend_pullback | 30m | FAILED | 3200 (1723) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 31% | +0.28R | -0.42R | +0.03 / -0.20 |
| rsi2_dip_buy | 30m | FAILED | 2514 (1338) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 34% | +0.17R | -0.19R | +0.01 / -0.20 |
| macd_trend_cross | 30m | FAILED | 268 (141) | stop_too_tight, indicator_lag | no_displacement 86%, indicator_lag 46%, low_relative_volume 45%, stop_too_tight 28% | +0.30R | -0.45R | +0.03 / -0.21 |
| liquidity_sweep_reversal | 1h | FAILED | 273 (143) | stop_too_tight | stop_too_tight 52% | +0.29R | -0.46R | -0.01 / -0.21 |
| ema_9_21_cross | 30m | FAILED | 300 (178) | indicator_lag | indicator_lag 47%, low_relative_volume 40% | +0.26R | -0.39R | -0.01 / -0.22 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 718 (497) | range_market, trend_reversal, stop_too_tight | range_market 46%, stop_too_tight 36% | +0.62R | -0.51R | +0.04 / -0.22 |
| supertrend_flip | 1h | FAILED | 249 (141) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 71%, regime_mismatch 70%, stop_too_tight 38%, indicator_lag 33% | +0.39R | -0.37R | -0.13 / -0.24 |
| trend_pullback | 15m | FAILED | 2822 (1560) | wrong_session, stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 31% | +0.25R | -0.44R | +0.07 / -0.26 |
| R4-BBRSI | 1h | FAILED | 1123 (791) | none | - | +0.44R | -0.45R | -0.13 / -0.31 |
| R4-BBRSI | 30m | FAILED | 1364 (931) | none | - | +0.43R | -0.44R | -0.05 / -0.31 |
| rsi2_dip_buy | 15m | FAILED | 1952 (1269) | low_relative_volume, trend_reversal, fees_slippage | fees_slippage 45% | +0.16R | -0.19R | +0.01 / -0.33 |
| bb_squeeze_breakout | 15m | FAILED | 524 (306) | stop_too_tight | no_displacement 58%, false_breakout 57%, stop_too_tight 41% | +0.31R | -0.47R | +0.00 / -0.35 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 559 (420) | stop_too_tight | stop_too_tight 34% | +0.60R | -0.49R | -0.06 / -0.46 |
| liquidity_sweep_reversal | 15m | FAILED | 525 (319) | stop_too_tight | stop_too_tight 38% | +0.37R | -0.45R | +0.00 / -0.48 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 103 (82) | stop_too_tight, sweep_continued | sweep_continued 96%, stop_too_tight 29% | +0.48R | -0.67R | -0.14 / -0.48 |
| liquidity_sweep_reversal | 30m | FAILED | 297 (191) | stop_too_tight | stop_too_tight 39% | +0.42R | -0.47R | -0.18 / -0.51 |
| ema_9_21_cross | 5m | FAILED | 266 (185) | stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 30% | +0.24R | -0.44R | -0.01 / -0.71 |
| liquidity_sweep_reversal | 5m | FAILED | 426 (318) | htf_conflict, stop_too_tight | stop_too_tight 37% | +0.29R | -0.48R | +0.14 / -1.19 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 27 strategy/timeframe tests); `false_breakout` (systematic in 15 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `regime_mismatch` (systematic in 12 strategy/timeframe tests); `trend_reversal` (systematic in 8 strategy/timeframe tests); `volatility_spike` (systematic in 4 strategy/timeframe tests); `no_displacement` (systematic in 2 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- ZEC up +7.1% (2026-09-26 13:00 → 2026-09-27 02:00 UTC): identifiable: at least one strategy had a valid signal before the move
- SUI up +10.7% (2026-09-26 20:00 → 2026-09-27 09:00 UTC): identifiable: at least one strategy had a valid signal before the move
- ENA up +9.0% (2026-09-27 08:00 → 2026-09-27 19:00 UTC): identifiable: at least one strategy had a valid signal before the move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 101.7 KB | - | - |
| `memory/coin_notes.md` | 6.8 KB | 7 | 2026-09-27 00:26 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 4.8 KB | 10 | 2026-09-28 00:28 UTC |
| `memory/experiments.md` | 43.1 KB | 15 | 2026-09-27 15:40 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 38.2 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 5.9 KB | - | - |
| `memory/missed_trades.md` | 11.3 KB | 14 | 2026-09-28 00:52 UTC |
| `memory/playbook.md` | 8.7 KB | - | - |
| `memory/research_sources.md` | 57.5 KB | 44 | 2026-09-28 00:52 UTC |
| `memory/smc_events.csv` | 227.7 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 15.8 KB | - | - |
| `memory/strategy_registry.csv` | 36.7 KB | - | - |
| `memory/trials.csv` | 9.2 KB | - | - |
| `memory/universe_log.md` | 6.9 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*