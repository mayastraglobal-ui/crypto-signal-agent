# Crypto Signal Report

**Updated:** 2026-09-28 17:22 Beijing time (2026-09-28 09:22 UTC) · data: Binance · 9 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 7.0 MB (GitHub) · large files of this run 3.5 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-28 09:22 UTC / 2026-09-28 17:22 Beijing
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
- 68 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-28 09:22 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 787 h since 2026-08-26 | -0.0008% | 1.34 | 1.04 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 787 h since 2026-08-26 | -0.0006% | 1.53 | 0.90 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 787 h since 2026-08-26 | -0.0003% | 1.56 | 1.18 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 787 h since 2026-08-26 | +0.0100% | 0.53 | 1.16 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 787 h since 2026-08-26 | +0.0062% | 2.58 | 1.44 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 787 h since 2026-08-26 | +0.0100% | 1.77 | 1.14 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 787 h since 2026-08-26 | +0.0100% | 1.51 | 0.77 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 787 h since 2026-08-26 | +0.0019% | 2.24 | 1.95 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| ENA | GOOD | okx | 787 h since 2026-08-26 | +0.0050% | 1.12 | 0.70 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ENAUSDT&period=1h&limit=500 |
| AVAX | GOOD | okx | 779 h since 2026-08-26 | +0.0100% | 1.90 | 1.26 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=AVAXUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **ZEC**, **XRP**, **SUI**, **UNI**
- **Research only** - backtested, never a signal: BNB, ENA
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** HBAR - 7-day average volume $19M < $50M; order book too thin: $115k within 1% (need $250k)

| Not eligible | 24h volume | Why |
|---|---|---|
| QNT | $257M | 7-day average volume $38M < $50M; 24h move +25.2% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $80k within 1% (need $250k) |
| VTHO | $80M | 7-day average volume $34M < $50M; spread 0.139% > 0.1%; order book too thin: $30k within 1% (need $250k) |
| PUMP | $78M | 7-day average volume $31M < $50M; order book too thin: $192k within 1% (need $250k) |
| ONDO | $73M | 7-day average volume $49M < $50M; order book too thin: $174k within 1% (need $250k) |
| HBAR | $55M | 7-day average volume $19M < $50M; order book too thin: $115k within 1% (need $250k) |

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
| BNB | 464 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| ENA | 130 | 909 | 903 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (HH/LL) | 84,999 / 82,705 | 0.47 | 3.55x | 1.00x | retest_down |
| ETH | mixed (HH/LL) | 2,703.51 / 2,635.69 | 0.88 | 2.48x | 0.99x | bull_engulf |
| SOL | mixed (LH/HL) | 123.45 / 121.28 | 0.58 | 0.72x | 1.06x | breakout_down, retest_down, failed_breakout_down |
| ZEC | down (LH/LL) | 1,615.13 / 1,575.3 | 0.62 | 0.36x | 0.85x | - |
| XRP | mixed (LH/HL) | 1.5368 / 1.509 | 0.75 | 1.23x | 0.96x | - |
| SUI | up (HH/HL) | 1.2947 / 1.2467 | 0.27 | 1.06x | 1.23x | bear_reject, breakout_down, retest_down |
| UNI | down (LH/LL) | 9.809 / 9.5 | 0.06 | 2.46x | 1.05x | displacement_down, breakout_down, retest_down |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 435 | 49% | 35% | 27% | 79% | 46% | 32% | can't tell from chance | 0.12R |
| 4h | displacement_down | 332 | 49% | 33% | 22% | 74% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1077 | 45% | 32% | 22% | 77% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | bear_engulf | 1237 | 44% | 30% | 20% | 77% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | bull_reject | 814 | 42% | 29% | 21% | 78% | 43% | 30% | can't tell from chance | 0.12R |
| 4h | bear_reject | 824 | 47% | 33% | 22% | 73% | 48% | 32% | can't tell from chance | 0.07R |
| 4h | smc_sweep_bull | 581 | 43% | 29% | 22% | 77% | 44% | 30% | can't tell from chance | 0.12R |
| 4h | smc_sweep_bear | 610 | 43% | 28% | 18% | 80% | 48% | 32% | worse than chance | 0.08R |
| 4h | smc_bos_up | 261 | 45% | 29% | 21% | 82% | 46% | 31% | can't tell from chance | 0.13R |
| 4h | smc_bos_down | 222 | 52% | 39% | 26% | 68% | 47% | 31% | can't tell from chance | 0.07R |
| 4h | smc_choch_up | 77 | 52% | 35% | 29% | 81% | 42% | 29% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 70 | 43% | 26% | 13% | 76% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 602 | 45% | 29% | 23% | 76% | 43% | 30% | can't tell from chance | 0.12R |
| 4h | smc_fvg_retrace_bear | 615 | 48% | 33% | 20% | 75% | 47% | 31% | can't tell from chance | 0.08R |
| 1h | displacement_up | 550 | 47% | 35% | 28% | 72% | 42% | 30% | beats chance | 0.27R |
| 1h | displacement_down | 377 | 38% | 24% | 15% | 81% | 38% | 24% | can't tell from chance | 0.18R |
| 1h | bull_engulf | 1531 | 40% | 29% | 22% | 74% | 42% | 30% | can't tell from chance | 0.31R |
| 1h | bear_engulf | 1699 | 39% | 25% | 17% | 79% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | bull_reject | 1274 | 40% | 29% | 22% | 75% | 42% | 30% | can't tell from chance | 0.30R |
| 1h | bear_reject | 1234 | 36% | 24% | 17% | 82% | 38% | 24% | can't tell from chance | 0.17R |
| 1h | smc_sweep_bull | 565 | 41% | 27% | 20% | 76% | 43% | 30% | can't tell from chance | 0.30R |
| 1h | smc_sweep_bear | 648 | 37% | 23% | 15% | 81% | 38% | 24% | can't tell from chance | 0.18R |
| 1h | smc_bos_up | 367 | 43% | 31% | 25% | 77% | 43% | 30% | can't tell from chance | 0.24R |
| 1h | smc_bos_down | 242 | 40% | 29% | 19% | 81% | 37% | 24% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 102 | 48% | 35% | 31% | 71% | 45% | 30% | can't tell from chance | 0.33R |
| 1h | smc_choch_down | 99 | 43% | 28% | 17% | 76% | 39% | 24% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 798 | 45% | 33% | 25% | 71% | 43% | 30% | can't tell from chance | 0.29R |
| 1h | smc_fvg_retrace_bear | 718 | 41% | 28% | 19% | 78% | 38% | 24% | can't tell from chance | 0.20R |
| 30m | displacement_up | 584 | 42% | 31% | 26% | 77% | 43% | 30% | can't tell from chance | 0.27R |
| 30m | displacement_down | 366 | 41% | 26% | 15% | 82% | 37% | 22% | can't tell from chance | 0.17R |
| 30m | bull_engulf | 1558 | 42% | 30% | 22% | 75% | 42% | 30% | can't tell from chance | 0.33R |
| 30m | bear_engulf | 1616 | 36% | 21% | 15% | 82% | 36% | 21% | can't tell from chance | 0.20R |
| 30m | bull_reject | 1205 | 46% | 30% | 23% | 73% | 42% | 29% | beats chance | 0.33R |
| 30m | bear_reject | 1307 | 37% | 22% | 15% | 82% | 36% | 21% | can't tell from chance | 0.20R |
| 30m | smc_sweep_bull | 563 | 40% | 28% | 18% | 75% | 42% | 29% | can't tell from chance | 0.34R |
| 30m | smc_sweep_bear | 571 | 41% | 26% | 17% | 82% | 36% | 21% | beats chance | 0.19R |
| 30m | smc_bos_up | 420 | 42% | 34% | 29% | 75% | 43% | 30% | can't tell from chance | 0.28R |
| 30m | smc_bos_down | 209 | 39% | 24% | 12% | 85% | 38% | 21% | can't tell from chance | 0.23R |
| 30m | smc_choch_up | 94 | 37% | 23% | 18% | 83% | 44% | 29% | can't tell from chance | 0.37R |
| 30m | smc_choch_down | 89 | 38% | 22% | 18% | 80% | 38% | 23% | can't tell from chance | 0.16R |
| 30m | smc_fvg_retrace_bull | 878 | 43% | 30% | 23% | 74% | 43% | 30% | can't tell from chance | 0.32R |
| 30m | smc_fvg_retrace_bear | 706 | 38% | 21% | 15% | 81% | 37% | 21% | can't tell from chance | 0.22R |
| 15m | displacement_up | 419 | 35% | 26% | 19% | 81% | 36% | 25% | can't tell from chance | 0.41R |
| 15m | displacement_down | 416 | 30% | 19% | 12% | 87% | 36% | 22% | worse than chance | 0.31R |
| 15m | bull_engulf | 1504 | 36% | 25% | 18% | 79% | 34% | 24% | can't tell from chance | 0.50R |
| 15m | bear_engulf | 1475 | 36% | 24% | 15% | 79% | 37% | 23% | can't tell from chance | 0.29R |
| 15m | bull_reject | 1188 | 35% | 23% | 15% | 80% | 35% | 24% | can't tell from chance | 0.50R |
| 15m | bear_reject | 1307 | 37% | 24% | 16% | 81% | 37% | 23% | can't tell from chance | 0.29R |
| 15m | smc_sweep_bull | 532 | 36% | 25% | 19% | 78% | 35% | 24% | can't tell from chance | 0.47R |
| 15m | smc_sweep_bear | 582 | 38% | 25% | 14% | 83% | 36% | 23% | can't tell from chance | 0.26R |
| 15m | smc_bos_up | 336 | 38% | 27% | 21% | 80% | 36% | 25% | can't tell from chance | 0.39R |
| 15m | smc_bos_down | 320 | 33% | 19% | 13% | 85% | 35% | 21% | can't tell from chance | 0.33R |
| 15m | smc_choch_up | 77 | 30% | 21% | 17% | 81% | 34% | 26% | can't tell from chance | 0.46R |
| 15m | smc_choch_down | 79 | 33% | 24% | 16% | 80% | 36% | 22% | can't tell from chance | 0.33R |
| 15m | smc_fvg_retrace_bull | 950 | 34% | 24% | 16% | 81% | 34% | 24% | can't tell from chance | 0.49R |
| 15m | smc_fvg_retrace_bear | 870 | 37% | 25% | 17% | 80% | 37% | 22% | can't tell from chance | 0.32R |
| 5m | displacement_up | 1142 | 32% | 22% | 17% | 84% | 28% | 19% | beats chance | 0.79R |
| 5m | displacement_down | 1057 | 27% | 16% | 11% | 87% | 30% | 20% | worse than chance | 0.53R |
| 5m | bull_engulf | 3787 | 26% | 18% | 13% | 83% | 27% | 19% | worse than chance | 0.87R |
| 5m | bear_engulf | 3751 | 30% | 20% | 13% | 83% | 30% | 20% | can't tell from chance | 0.54R |
| 5m | bull_reject | 2983 | 27% | 18% | 14% | 81% | 27% | 19% | can't tell from chance | 0.90R |
| 5m | bear_reject | 3347 | 32% | 21% | 14% | 82% | 30% | 20% | can't tell from chance | 0.51R |
| 5m | smc_sweep_bull | 1095 | 29% | 21% | 14% | 80% | 29% | 21% | can't tell from chance | 0.78R |
| 5m | smc_sweep_bear | 1150 | 32% | 23% | 15% | 82% | 31% | 20% | can't tell from chance | 0.45R |
| 5m | smc_bos_up | 741 | 31% | 23% | 18% | 83% | 29% | 20% | can't tell from chance | 0.80R |
| 5m | smc_bos_down | 826 | 27% | 17% | 10% | 88% | 29% | 19% | can't tell from chance | 0.58R |
| 5m | smc_choch_up | 200 | 36% | 28% | 18% | 85% | 29% | 20% | can't tell from chance | 0.92R |
| 5m | smc_choch_down | 204 | 23% | 13% | 8% | 89% | 30% | 19% | worse than chance | 0.56R |
| 5m | smc_fvg_retrace_bull | 3084 | 29% | 20% | 15% | 82% | 27% | 19% | can't tell from chance | 0.90R |
| 5m | smc_fvg_retrace_bear | 2716 | 27% | 18% | 12% | 85% | 29% | 20% | worse than chance | 0.57R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (moderate) | WEAK_BULL (moderate) | RANGE (strong) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H UNCLEAR)) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (moderate) | COMPRESSION (moderate) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H COMPRESSION, 1H UNCLEAR)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (moderate) | UNCLEAR (weak) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | UNCLEAR (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H TRANSITION)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | UNCLEAR (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H UNCLEAR)) |
| **SUI** | UNCLEAR (weak) | EXPANSION up (weak) | STRONG_BULL (moderate) | TRANSITION (weak) | LONG allowed (1D/4H bullish, 1W UNCLEAR) |
| **UNI** | EXPANSION up (moderate) | STRONG_BULL (moderate) | UNCLEAR (weak) | EXPANSION down (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H EXPANSION)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (strong) | RANGE (strong) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H UNCLEAR)) |
| **ENA** | TRANSITION (weak) | EXPANSION up (moderate) | STRONG_BULL (strong) | RANGE (strong) | LONG allowed (1D/4H bullish, 1W TRANSITION) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (moderate)** - for: EMA-fast rising (+1.5 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.73x normal, Bollinger width above 56% of the last 100 candles · against: EMAs not lined up
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.5 ATR in 10 candles); ADX 44 = strong trend; candle size 1.05x normal, Bollinger width above 82% of the last 100 candles; volume 0.97x normal · against: swing structure mixed (neutral)
- **4H RANGE (strong)** - for: EMAs not lined up; EMA-fast flat (+0.5 ATR in 10 candles); swing structure mixed; ADX 15 = weak trend / ranging; candle size 0.88x normal, Bollinger width above 19% of the last 100 candles · against: -
- **1H UNCLEAR (weak)** - for: candle size 1.00x normal, Bollinger width above 100% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.9 ATR in 10 candles); swing structure mixed; ADX 24 = in between (20-25); ADX 24 is close to a threshold; signals are mixed and trend strength is in between

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (BOS 15 candles ago) | sell-side (bullish idea) 0 candles ago | bear 83,354.34-83,436.58 | bear 84,342.00-84,843.00 | discount (11%) | swing high 84,999.00 (5.39 ATR) | swing low 82,705.02 (0.68 ATR) |
| **ETH** | down (BOS 23 candles ago) | sell-side (bullish idea) 2 candles ago | bear 2,694.95-2,704.41 (retraced) | bear 2,745.99-2,784.40 | discount (23%) | swing high 2,703.51 (3.49 ATR) | swing low 2,635.69 (1.05 ATR) |
| **SOL** | down (BOS 5 candles ago) | sell-side (bullish idea) 0 candles ago | bear 119.63-119.84 | bull 115.86-117.34 | below the range (-135%) | swing high 123.45 (4.33 ATR) | swing low 115.86 (2.13 ATR) |
| **ZEC** | down (BOS 7 candles ago) | buy-side (bearish idea) 2 candles ago | bear 1,608.30-1,618.45 (retraced) | bull 1,527.56-1,540.22 | below the range (-56%) | swing high 1,615.13 (3.06 ATR) | swing low 1,517.41 (1.74 ATR) |
| **XRP** | down (BOS 15 candles ago) | sell-side (bullish idea) 22 candles ago | bear 1.4884-1.4940 (retraced) | bull 1.3773-1.3856 | below the range (-100%) | swing high 1.5368 (3.36 ATR) | swing low 1.4517 (1.79 ATR) |
| **SUI** | down (BOS 8 candles ago) | sell-side (bullish idea) 0 candles ago | bear 1.2025-1.2069 (retraced) | bull 1.0050-1.0598 | below the range (-131%) | PDH 1.2947 (4.16 ATR) | swing low 1.1543 (1.1 ATR) |
| **UNI** | down (CHOCH 2 candles ago) | sell-side (bullish idea) 0 candles ago | bear 8.8920-8.9870 | bull 8.6780-9.0640 | below the range (-203%) | swing high 9.8090 (5.4 ATR) | swing low 8.7870 (0.5 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **SIDEWAYS**  (most coins follow BTC - trading against BTC's trend is harder)
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
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 60.0 | +1.221 | 3.69 | 2.3R | +0.97 / +2.21 | +2.21 / +0.97 | 0/5 ✗ | +1.10 | +0.98 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 22 / 9 of 32 | 0 | only 5 trades; only 1 unseen-test trades |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 15 | 46.7 | +0.338 | 1.46 | 4.1R | +0.23 / +0.56 | +0.18 / +0.44 | 0/5 ✗ | +0.03 | -0.15 | ✗  sweep_bars 8→10: -0.00R | 0 | 0.31R | 2, +0.31 (+0.31 / +0.00) | 45 / 22 of 73 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); only 15 trades; only 5 unseen-test trades |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 939 | 40.6 | +0.226 | 1.42 | 24.2R | +0.21 / +0.26 | +0.26 / +0.18 | 5/5 | +0.19 | +0.17 | stable | 9 | 0.04R | 12, +0.75 (+0.68 / +1.44) | 85 / 44 of 243 | 0 | max drawdown 24.2R |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **BACKTESTING** | 939 | 40.6 | +0.226 | 1.42 | 24.2R | +0.21 / +0.26 | +0.26 / +0.18 | 5/5 | +0.19 | +0.17 | stable | 9 | 0.04R | 12, +0.75 (+0.68 / +1.44) | 85 / 44 of 243 | 0 | max drawdown 24.2R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1067 | 40.1 | +0.220 | 1.4 | 23.7R | +0.21 / +0.23 | +0.23 / +0.21 | 5/5 | +0.19 | +0.16 | stable | 9 | 0.05R | 13, +0.84 (+0.95 / +0.20) | 141 / 57 of 323 | 0 | max drawdown 23.7R |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.206 | 1.21 | 3.3R | +0.51 / -1.32 | -1.32 / +0.51 | 0/5 ✗ | +0.08 | -0.03 | ✗  sweep_bars 20→24: -0.16R | 0 | 0.26R | 1, -1.32 (-1.32 / +0.00) | 34 / 11 of 52 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 6 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 965 | 54.8 | +0.129 | 1.29 | 21.2R | +0.12 / +0.15 | +0.13 / +0.13 | 5/5 | +0.10 | +0.07 | stable | 7 | 0.04R | 15, +0.26 (+0.27 / +0.20) | 85 / 44 of 243 | 0 | max drawdown 21.2R |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.78 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.79 (+0.00 / +1.79) | 31 / 92 of 136 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 2 of 3 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 54 / 15 of 72 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 34 / 11 of 52 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 2 of 3 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 22 / 9 of 32 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 11 | 27.3 | -0.198 | 0.62 | 2.7R | -0.39 / +0.14 | -1.11 / -0.11 | 0/5 ✗ | -0.30 | -0.24 | ✗  stop max_width_atr 3.0→3.6: -0.20R | 0 | 0.08R | 0, +0.00 (+0.00 / +0.00) | 503 / 173 of 812 | 0 | only 11 trades; avg -0.20R/trade (needs +0.10R); profit factor 0.62; only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 13 | 46.2 | -0.308 | 0.48 | 5.9R | -0.37 / +0.05 | -0.31 / -0.31 | 0/5 ✗ | -0.30 | -0.54 | ✗  time_stop_bars 30→24: -0.36R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 403 / 218 of 749 | 0 | only 13 trades; avg -0.31R/trade (needs +0.10R); profit factor 0.48; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 4 | 0.0 | -1.218 | 0.0 | 4.9R | -1.24 / -1.16 | -1.42 / -1.15 | 0/5 ✗ | -1.22 | -1.29 | ✗  stop buffer_atr 0.2→0.16: -1.23R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 54 / 15 of 72 | 0 | only 4 trades; avg -1.22R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 248 | 52.4 | +0.048 | 1.09 | 24.8R | +0.23 / -0.29 | +0.13 / -0.03 | 3/5 | -0.00 | -0.05 | ✗  stop atr 1.5→1.8: -0.00R | 6 | 0.07R | 3, -0.30 (+0.08 / -1.05) | 91 / 21 of 126 | 0 | avg +0.05R/trade (needs +0.10R); profit factor 1.09; max drawdown 24.8R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 748 | 52.9 | -0.009 | 0.98 | 43.2R | -0.02 / +0.02 | -0.07 / +0.06 | 2/5 ✗ | -0.09 | -0.17 | ✗  bb_k 2→1: -0.06R | 4 | 0.14R | 6, +0.05 (-0.23 / +0.33) | 132 / 37 of 205 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 43.2R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1168 | 34.8 | -0.019 | 0.97 | 82.5R | -0.04 / +0.04 | +0.04 / -0.08 | 2/5 ✗ | -0.10 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 4 | 0.12R | 48, -0.01 (+0.10 / -0.48) | 134 / 34 of 334 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 82.5R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FAILED** | 1168 | 34.8 | -0.019 | 0.97 | 82.5R | -0.04 / +0.04 | +0.04 / -0.08 | 2/5 ✗ | -0.10 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 4 | 0.12R | 48, -0.01 (+0.10 / -0.48) | 134 / 34 of 334 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 82.5R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1379 | 34.3 | -0.040 | 0.94 | 101.7R | -0.06 / +0.03 | +0.01 / -0.09 | 2/5 ✗ | -0.12 | -0.20 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.13R | 53, -0.03 (+0.03 / -0.24) | 235 / 49 of 478 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; max drawdown 101.7R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 31 | 51.6 | -0.047 | 0.91 | 5.6R | +0.07 / -0.33 | +0.22 / -0.37 | 1/5 ✗ | -0.08 | -0.11 | ✗  time_stop_bars 40→32: -0.07R | 1 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 131 / 5 of 137 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; only 9 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 2952 | 32.3 | -0.048 | 0.92 | 232.5R | -0.08 / +0.02 | -0.03 / -0.07 | 2/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.09R | 32, +0.41 (+0.48 / +0.10) | 198 / 111 of 523 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 232.5R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 167 | 49.7 | -0.050 | 0.91 | 29.8R | -0.17 / +0.21 | -0.09 / -0.01 | 2/5 ✗ | -0.11 | -0.18 | ✗  stop atr 1.5→1.2: -0.14R | 3 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 198 / 5 of 205 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 29.8R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1199 | 49.8 | -0.051 | 0.9 | 91.4R | -0.06 / -0.03 | -0.02 / -0.08 | 1/5 ✗ | -0.13 | -0.20 | ✗  stop atr 2.0→1.6: -0.13R | 3 | 0.12R | 48, -0.04 (+0.04 / -0.36) | 134 / 34 of 334 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.90; max drawdown 91.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2599 | 32.1 | -0.054 | 0.92 | 214.7R | -0.09 / +0.03 | -0.04 / -0.07 | 1/5 ✗ | -0.10 | -0.15 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 29, +0.38 (+0.47 / -0.19) | 117 / 81 of 380 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 214.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FAILED** | 2599 | 32.1 | -0.054 | 0.92 | 215.6R | -0.09 / +0.03 | -0.04 / -0.07 | 1/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 29, +0.38 (+0.47 / -0.19) | 117 / 81 of 380 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 215.6R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2669 | 48.1 | -0.060 | 0.89 | 188.0R | -0.07 / -0.03 | -0.07 / -0.05 | 0/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.07R | 1 | 0.09R | 30, +0.26 (+0.35 / -0.34) | 117 / 81 of 380 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 188.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1063 | 48.4 | -0.065 | 0.88 | 115.0R | -0.01 / -0.18 | -0.01 / -0.13 | 1/5 ✗ | -0.11 | -0.14 | ✗  long_rsi_hi 65→52: -0.14R | 3 | 0.06R | 10, +0.53 (+1.14 / -0.39) | 579 / 181 of 903 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 115.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 83 | 47.0 | -0.093 | 0.83 | 16.4R | +0.05 / -0.34 | -0.10 / -0.08 | 3/5 ✗ | -0.12 | -0.14 | ✗  time_stop_bars 60→48: -0.09R | 1 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 38 / 6 of 46 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.83; max drawdown 16.4R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1612 | 55.8 | -0.111 | 0.62 | 179.7R | -0.10 / -0.13 | -0.13 / -0.09 | 0/5 ✗ | -0.14 | -0.17 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.05R | 7, -0.11 (-0.11 / +0.00) | 702 / 4 of 934 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.62; max drawdown 179.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 310 | 44.2 | -0.115 | 0.79 | 47.9R | -0.13 / -0.09 | -0.18 / -0.04 | 0/5 ✗ | -0.18 | -0.26 | ✗  slow 21→17: -0.20R | 3 | 0.12R | 4, -0.30 (-1.00 / +1.82) | 134 / 7 of 150 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.79; max drawdown 47.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 6112 | 53.6 | -0.132 | 0.54 | 811.5R | -0.11 / -0.18 | -0.14 / -0.12 | 0/5 ✗ | -0.20 | -0.27 | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 42, -0.13 (-0.08 / -0.17) | 966 / 3 of 1301 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.54; max drawdown 811.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 255 | 33.3 | -0.138 | 0.82 | 53.6R | -0.02 / -0.41 | -0.37 / +0.12 | 1/5 ✗ | -0.24 | -0.35 | ✗  time_stop_bars 30→36: -0.17R | 1 | 0.20R | 3, +0.86 (+0.00 / +0.86) | 82 / 196 of 288 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.82; max drawdown 53.6R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 5541 | 47.3 | -0.139 | 0.76 | 778.8R | -0.14 / -0.13 | -0.17 / -0.10 | 0/5 ✗ | -0.21 | -0.28 | ✗  stop atr 1.5→1.2: -0.18R | 1 | 0.13R | 48, -0.04 (+0.08 / -0.38) | 1052 / 253 of 1662 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 778.8R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 85 | 36.5 | -0.147 | 0.79 | 22.0R | -0.32 / +0.32 | -0.20 / -0.12 | 1/5 ✗ | -0.21 | -0.31 | ✗  depth 0.985→1.182: -0.45R | 2 | 0.15R | 2, +1.30 (+1.34 / +1.27) | 42 / 6 of 50 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.79; max drawdown 22.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 412 | 45.4 | -0.155 | 0.74 | 65.3R | -0.14 / -0.20 | -0.23 / -0.12 | 1/5 ✗ | -0.30 | -0.43 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.25R | 21, -0.16 (+0.12 / -1.06) | 59 / 13 of 95 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.74; max drawdown 65.3R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 41 | 36.6 | -0.161 | 0.77 | 11.3R | +0.11 / -0.50 | -0.40 / +0.06 | 1/5 ✗ | -0.33 | -0.41 | ✗  stop buffer_atr 0.2→0.16: -0.16R | 3 | 0.15R | 7, -0.82 (-0.59 / -1.40) | 92 / 30 of 136 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.77; max drawdown 11.3R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 235 | 38.7 | -0.165 | 0.75 | 59.0R | -0.18 / -0.12 | +0.12 / -0.35 | 1/5 ✗ | -0.21 | -0.27 | ✗  depth 0.985→1.182: -0.29R | 1 | 0.10R | 5, +0.67 (+0.70 / +0.66) | 84 / 7 of 105 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.75; max drawdown 59.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 147 | 46.9 | -0.174 | 0.69 | 26.0R | -0.18 / -0.15 | -0.14 / -0.20 | 2/5 ✗ | -0.24 | -0.33 | ✗  adx_min 20→24: -0.25R | 1 | 0.13R | 6, -0.74 (-0.74 / +0.00) | 52 / 5 of 66 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.69; max drawdown 26.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 461 | 46.9 | -0.180 | 0.71 | 84.7R | -0.23 / -0.05 | -0.24 / -0.12 | 1/5 ✗ | -0.29 | -0.41 | ✗  stop atr 1.5→1.2: -0.25R | 1 | 0.18R | 18, -0.40 (-0.28 / -0.65) | 120 / 33 of 196 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.71; max drawdown 84.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3200 | 46.2 | -0.195 | 0.68 | 630.5R | -0.18 / -0.23 | -0.22 / -0.17 | 0/5 ✗ | -0.31 | -0.42 | ✗  stop atr 1.5→1.2: -0.26R | 0 | 0.18R | 92, -0.03 (+0.24 / -0.64) | 802 / 179 of 1519 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 630.5R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2514 | 46.8 | -0.198 | 0.4 | 498.6R | -0.18 / -0.24 | -0.25 / -0.15 | 0/5 ✗ | -0.30 | -0.41 | ✗  hi 90→108: -0.25R | 0 | 0.17R | 38, -0.02 (-0.03 / -0.01) | 956 / 22 of 1172 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.40; max drawdown 498.6R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 268 | 47.4 | -0.208 | 0.66 | 62.1R | -0.13 / -0.41 | -0.35 / -0.08 | 0/5 ✗ | -0.33 | -0.42 | ✗  stop atr 1.5→1.2: -0.29R | 1 | 0.19R | 6, -0.48 (-0.10 / -1.24) | 175 / 8 of 200 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.66; max drawdown 62.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 273 | 47.6 | -0.211 | 0.65 | 58.6R | -0.22 / -0.20 | -0.23 / -0.19 | 0/5 ✗ | -0.29 | -0.38 | ✗  vol_x 1.2→1.44: -0.36R | 2 | 0.17R | 4, -0.23 (+0.01 / -0.48) | 95 / 183 of 286 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.65; max drawdown 58.6R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 300 | 40.7 | -0.219 | 0.63 | 69.5R | -0.20 / -0.29 | -0.29 / -0.16 | 1/5 ✗ | -0.32 | -0.41 | ✗  fast 9→11: -0.30R | 0 | 0.17R | 8, +0.04 (+0.04 / +0.00) | 96 / 16 of 126 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.63; max drawdown 69.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 718 | 30.8 | -0.221 | 0.73 | 183.8R | -0.22 / -0.23 | -0.31 / -0.14 | 1/5 ✗ | -0.33 | -0.43 | ✗  stop buffer_atr 0.2→0.16: -0.26R | 1 | 0.22R | 15, -0.29 (+0.87 / -0.87) | 432 / 1032 of 1548 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.73; max drawdown 183.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 249 | 43.4 | -0.239 | 0.61 | 63.0R | -0.26 / -0.20 | -0.34 / -0.14 | 0/5 ✗ | -0.30 | -0.35 | ✗  st_n 10→12: -0.25R | 1 | 0.08R | 4, +0.17 (+0.17 / +0.00) | 51 / 1 of 60 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.61; max drawdown 63.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 2822 | 44.7 | -0.258 | 0.61 | 733.4R | -0.24 / -0.31 | -0.30 / -0.24 | 0/5 ✗ | -0.41 | -0.57 | ✗  stop atr 1.5→1.2: -0.34R | 0 | 0.25R | 181, -0.18 (-0.03 / -0.75) | 1188 / 279 of 2062 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 733.4R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1123 | 29.6 | -0.308 | 0.61 | 347.5R | -0.33 / -0.26 | -0.31 / -0.31 | 0/5 ✗ | -0.39 | -0.46 | ✗  rsi_n 14→17: -0.38R | 1 | 0.14R | 9, -0.17 (-0.37 / +0.54) | 695 / 5 of 741 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.61; max drawdown 347.5R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1364 | 31.7 | -0.313 | 0.61 | 433.6R | -0.32 / -0.30 | -0.31 / -0.31 | 0/5 ✗ | -0.44 | -0.57 | ✗  stop atr 1.5→1.2: -0.35R | 0 | 0.21R | 30, -0.17 (-0.31 / -0.02) | 540 / 23 of 650 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.61; max drawdown 433.6R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 1952 | 35.0 | -0.325 | 0.22 | 636.0R | -0.31 / -0.36 | -0.42 / -0.25 | 0/5 ✗ | -0.49 | -0.67 | ✗  hi 90→108: -0.42R | 0 | 0.28R | 59, -0.21 (-0.15 / -0.36) | 1111 / 33 of 1244 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.33R/trade (needs +0.10R); profit factor 0.22; max drawdown 636.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 524 | 41.6 | -0.350 | 0.51 | 191.5R | -0.32 / -0.42 | -0.32 / -0.37 | 0/5 ✗ | -0.50 | -0.64 | ✗  stop atr 1.5→1.2: -0.42R | 0 | 0.28R | 38, -0.72 (-0.71 / -0.77) | 92 / 49 of 196 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.35R/trade (needs +0.10R); profit factor 0.51; max drawdown 191.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 559 | 24.9 | -0.461 | 0.53 | 266.0R | -0.48 / -0.41 | -0.56 / -0.36 | 1/5 ✗ | -0.63 | -0.76 | ✗  n 20→24: -0.51R | 1 | 0.33R | 23, -0.10 (+0.73 / -0.86) | 425 / 921 of 1536 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.53; max drawdown 266.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 525 | 39.2 | -0.476 | 0.4 | 250.2R | -0.45 / -0.57 | -0.57 / -0.42 | 0/5 ✗ | -0.68 | -0.92 | ✗  stop atr 1.0→0.8: -0.54R | 0 | 0.37R | 33, -0.62 (-0.48 / -0.77) | 97 / 220 of 354 | 0 | not cost-viable: fees + slippage 0.37R per trade (stop must be ≥ 4x the round-trip cost); avg -0.48R/trade (needs +0.10R); profit factor 0.40; max drawdown 250.2R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 103 | 20.4 | -0.481 | 0.51 | 56.1R | -0.40 / -0.65 | -0.56 / -0.40 | 0/5 ✗ | -0.63 | -0.77 | ✗  stop max_width_atr 3.0→2.4: -0.48R | 1 | 0.25R | 6, -0.04 (-1.25 / +0.56) | 31 / 92 of 136 | 0 | avg -0.48R/trade (needs +0.10R); profit factor 0.51; max drawdown 56.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 297 | 35.7 | -0.510 | 0.35 | 151.5R | -0.49 / -0.57 | -0.51 / -0.51 | 0/5 ✗ | -0.66 | -0.81 | ✗  stop atr 1.0→0.8: -0.56R | 0 | 0.28R | 13, -0.74 (-0.52 / -1.01) | 107 / 199 of 332 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.51R/trade (needs +0.10R); profit factor 0.35; max drawdown 151.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 266 | 30.5 | -0.711 | 0.25 | 189.2R | -0.78 / -0.60 | -0.68 / -0.92 | 0/5 ✗ | -1.07 | -1.42 | ✗  stop atr 1.5→1.2: -0.91R | 0 | 0.54R | 71, -0.54 (-0.59 / -0.43) | 196 / 48 of 315 | 0 | not cost-viable: fees + slippage 0.54R per trade (stop must be ≥ 4x the round-trip cost); avg -0.71R/trade (needs +0.10R); profit factor 0.25; max drawdown 189.2R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 426 | 25.4 | -1.188 | 0.15 | 505.9R | -1.24 / -1.13 | -1.08 / -1.96 | 0/5 ✗ | -1.85 | -2.51 | ✗  stop atr 1.0→0.8: -1.51R | 0 | 1.05R | 131, -1.22 (-1.33 / -1.01) | 202 / 550 of 887 | 0 | not cost-viable: fees + slippage 1.05R per trade (stop must be ≥ 4x the round-trip cost); avg -1.19R/trade (needs +0.10R); profit factor 0.15; max drawdown 505.9R; not profitable in BOTH train and unseen test |

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
| `memory/smc_events.csv` | 244.2 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 15.8 KB | - | - |
| `memory/strategy_registry.csv` | 36.7 KB | - | - |
| `memory/trials.csv` | 9.2 KB | - | - |
| `memory/universe_log.md` | 7.2 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*