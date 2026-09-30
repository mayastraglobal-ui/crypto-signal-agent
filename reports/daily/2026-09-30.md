# Crypto Signal Report

**Updated:** 2026-09-30 20:28 Beijing time (2026-09-30 12:28 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 8.6 MB (GitHub) · large files of this run 4.2 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-30 12:28 UTC / 2026-09-30 20:28 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US GDP (Third Estimate), 2nd Quarter 2026 2026-09-30 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.05% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| QNT | **DEGRADED** | 1d: DEGRADED: volume 91x normal on candle 09-27 00:00 UTC (possible bad data); 1d: DEGRADED: volume 87x normal on candle 09-28 00:00 UTC (possible bad data); 1d: DEGRADED: volume 56x normal on candle 09-29 00:00 UTC (possible bad data) |
- 72 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-30 12:28 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 838 h since 2026-08-26 | +0.0034% | 1.37 | 0.81 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 838 h since 2026-08-26 | +0.0062% | 1.42 | 0.91 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 838 h since 2026-08-26 | +0.0020% | 2.86 | 0.98 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 838 h since 2026-08-26 | +0.0002% | 1.55 | 0.92 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 838 h since 2026-08-26 | +0.0100% | 0.80 | 0.96 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 838 h since 2026-08-26 | +0.0036% | 2.32 | 0.89 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| AVAX | GOOD | okx | 830 h since 2026-08-26 | +0.0038% | 2.07 | 0.60 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=AVAXUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 838 h since 2026-08-26 | +0.0100% | 2.14 | 0.78 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| HBAR | GOOD | okx | 731 h since 2026-08-31 | -0.0118% | 1.87 | 1.12 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=HBARUSDT&period=1h&limit=500 |
| ENA | GOOD | okx | 838 h since 2026-08-26 | +0.0050% | 1.24 | 0.54 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ENAUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **XRP**, **ZEC**, **BNB**, **SUI**
- **Research only** - backtested, never a signal: AVAX, HBAR, ENA
- **Changes this run** (also written to `memory/universe_log.md`):
  - **LEAVE** AVAX - outside the top 7 for 2 runs in a row (now #8)
  - **JOIN** BNB - in the top 7 for 2 runs in a row (now #6)

| Not eligible | 24h volume | Why |
|---|---|---|
| QNT | $185M | suspended for the rest of the UTC day (moved more than ±25% earlier today); order book too thin: $111k within 1% (need $250k) |
| PUMP | $76M | 7-day average volume $48M < $50M; order book too thin: $130k within 1% (need $250k) |
| AAVE | $56M | 7-day average volume $31M < $50M; order book too thin: $222k within 1% (need $250k) |

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
| XRP | 439 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| ZEC | 393 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| BNB | 464 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| SUI | 178 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| AVAX | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| HBAR | 366 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-09 | OK (300 candles) |
| ENA | 130 | 911 | 905 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (LH/HL) | 83,849 / 82,956.1 | 0.77 | 0.92x | 1.04x | bull_engulf, bull_reject |
| ETH | down (LH/LL) | 2,680.62 / 2,656.92 | 0.85 | 0.94x | 1.04x | bull_engulf, bull_reject |
| SOL | down (LH/LL) | 120.07 / 117.81 | 0.45 | 2.05x | 0.93x | - |
| XRP | up (HH/HL) | 1.5617 / 1.4897 | 0.66 | 0.80x | 0.90x | bull_engulf |
| ZEC | mixed (LH/HL) | 1,433.91 / 1,390.74 | 0.30 | 0.71x | 0.97x | - |
| BNB | mixed (LH/HL) | 765.57 / 756.17 | 0.76 | 0.96x | 1.04x | displacement_up, bull_reject, breakout_up |
| SUI | up (HH/HL) | 1.1778 / 1.1415 | 0.30 | 1.11x | 0.80x | bear_engulf, bear_reject |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 466 | 47% | 33% | 26% | 81% | 44% | 31% | can't tell from chance | 0.13R |
| 4h | displacement_down | 365 | 49% | 33% | 21% | 75% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1234 | 43% | 30% | 22% | 78% | 43% | 30% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1366 | 44% | 29% | 19% | 77% | 47% | 32% | worse than chance | 0.08R |
| 4h | bull_reject | 953 | 41% | 27% | 20% | 80% | 43% | 29% | can't tell from chance | 0.13R |
| 4h | bear_reject | 903 | 46% | 31% | 21% | 75% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 663 | 44% | 29% | 21% | 77% | 43% | 29% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 688 | 44% | 29% | 20% | 78% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 268 | 43% | 27% | 20% | 83% | 43% | 30% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 244 | 48% | 33% | 20% | 74% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 92 | 53% | 35% | 27% | 82% | 45% | 31% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 92 | 41% | 28% | 18% | 74% | 51% | 32% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 662 | 42% | 27% | 21% | 78% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | smc_fvg_retrace_bear | 688 | 45% | 30% | 20% | 77% | 47% | 31% | can't tell from chance | 0.08R |
| 1h | displacement_up | 594 | 43% | 31% | 25% | 75% | 42% | 30% | can't tell from chance | 0.28R |
| 1h | displacement_down | 426 | 36% | 24% | 14% | 82% | 38% | 25% | can't tell from chance | 0.19R |
| 1h | bull_engulf | 1709 | 39% | 28% | 21% | 76% | 42% | 29% | worse than chance | 0.33R |
| 1h | bear_engulf | 1825 | 38% | 24% | 17% | 80% | 39% | 25% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1373 | 39% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.32R |
| 1h | bear_reject | 1414 | 37% | 25% | 18% | 81% | 39% | 25% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bull | 651 | 39% | 24% | 18% | 79% | 42% | 29% | can't tell from chance | 0.31R |
| 1h | smc_sweep_bear | 705 | 39% | 25% | 15% | 80% | 39% | 26% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 416 | 43% | 30% | 24% | 77% | 42% | 29% | can't tell from chance | 0.26R |
| 1h | smc_bos_down | 285 | 39% | 28% | 19% | 82% | 39% | 26% | can't tell from chance | 0.22R |
| 1h | smc_choch_up | 104 | 47% | 37% | 30% | 72% | 40% | 28% | can't tell from chance | 0.33R |
| 1h | smc_choch_down | 108 | 42% | 30% | 17% | 75% | 40% | 27% | can't tell from chance | 0.18R |
| 1h | smc_fvg_retrace_bull | 899 | 43% | 30% | 23% | 74% | 42% | 30% | can't tell from chance | 0.31R |
| 1h | smc_fvg_retrace_bear | 818 | 40% | 28% | 18% | 78% | 38% | 25% | can't tell from chance | 0.21R |
| 30m | displacement_up | 590 | 37% | 28% | 22% | 80% | 42% | 29% | worse than chance | 0.29R |
| 30m | displacement_down | 431 | 42% | 26% | 15% | 82% | 36% | 22% | beats chance | 0.20R |
| 30m | bull_engulf | 1716 | 42% | 29% | 21% | 75% | 42% | 29% | can't tell from chance | 0.34R |
| 30m | bear_engulf | 1784 | 38% | 23% | 16% | 79% | 37% | 23% | can't tell from chance | 0.22R |
| 30m | bull_reject | 1340 | 44% | 28% | 21% | 75% | 42% | 29% | can't tell from chance | 0.35R |
| 30m | bear_reject | 1460 | 38% | 23% | 16% | 81% | 37% | 22% | can't tell from chance | 0.21R |
| 30m | smc_sweep_bull | 636 | 40% | 26% | 17% | 77% | 42% | 30% | can't tell from chance | 0.36R |
| 30m | smc_sweep_bear | 622 | 42% | 27% | 19% | 81% | 38% | 23% | can't tell from chance | 0.20R |
| 30m | smc_bos_up | 436 | 39% | 31% | 26% | 77% | 42% | 29% | can't tell from chance | 0.32R |
| 30m | smc_bos_down | 239 | 37% | 23% | 13% | 85% | 38% | 22% | can't tell from chance | 0.23R |
| 30m | smc_choch_up | 104 | 38% | 26% | 19% | 83% | 43% | 30% | can't tell from chance | 0.37R |
| 30m | smc_choch_down | 104 | 39% | 23% | 20% | 80% | 37% | 21% | can't tell from chance | 0.21R |
| 30m | smc_fvg_retrace_bull | 1009 | 40% | 27% | 20% | 78% | 41% | 29% | can't tell from chance | 0.35R |
| 30m | smc_fvg_retrace_bear | 810 | 39% | 22% | 15% | 79% | 37% | 22% | can't tell from chance | 0.22R |
| 15m | displacement_up | 472 | 36% | 27% | 20% | 82% | 34% | 24% | can't tell from chance | 0.44R |
| 15m | displacement_down | 462 | 33% | 21% | 12% | 84% | 34% | 21% | can't tell from chance | 0.31R |
| 15m | bull_engulf | 1671 | 36% | 25% | 18% | 78% | 35% | 25% | can't tell from chance | 0.50R |
| 15m | bear_engulf | 1643 | 36% | 23% | 14% | 79% | 36% | 22% | can't tell from chance | 0.30R |
| 15m | bull_reject | 1282 | 34% | 23% | 15% | 80% | 34% | 24% | can't tell from chance | 0.52R |
| 15m | bear_reject | 1470 | 36% | 23% | 14% | 80% | 36% | 22% | can't tell from chance | 0.30R |
| 15m | smc_sweep_bull | 585 | 33% | 23% | 17% | 79% | 34% | 24% | can't tell from chance | 0.48R |
| 15m | smc_sweep_bear | 614 | 36% | 23% | 13% | 85% | 36% | 23% | can't tell from chance | 0.29R |
| 15m | smc_bos_up | 360 | 37% | 27% | 21% | 80% | 36% | 25% | can't tell from chance | 0.42R |
| 15m | smc_bos_down | 347 | 33% | 20% | 14% | 84% | 36% | 23% | can't tell from chance | 0.33R |
| 15m | smc_choch_up | 85 | 34% | 24% | 15% | 82% | 34% | 24% | can't tell from chance | 0.46R |
| 15m | smc_choch_down | 85 | 33% | 21% | 15% | 82% | 38% | 25% | can't tell from chance | 0.31R |
| 15m | smc_fvg_retrace_bull | 1082 | 34% | 24% | 17% | 80% | 35% | 24% | can't tell from chance | 0.50R |
| 15m | smc_fvg_retrace_bear | 990 | 34% | 24% | 16% | 81% | 36% | 22% | can't tell from chance | 0.32R |
| 5m | displacement_up | 1330 | 33% | 22% | 17% | 84% | 30% | 22% | beats chance | 0.80R |
| 5m | displacement_down | 1153 | 27% | 18% | 12% | 86% | 30% | 20% | can't tell from chance | 0.51R |
| 5m | bull_engulf | 4216 | 29% | 21% | 15% | 81% | 29% | 21% | can't tell from chance | 0.85R |
| 5m | bear_engulf | 4114 | 31% | 20% | 13% | 83% | 30% | 20% | can't tell from chance | 0.52R |
| 5m | bull_reject | 3217 | 29% | 20% | 15% | 80% | 29% | 21% | can't tell from chance | 0.89R |
| 5m | bear_reject | 3753 | 32% | 21% | 14% | 82% | 31% | 20% | can't tell from chance | 0.49R |
| 5m | smc_sweep_bull | 1227 | 30% | 22% | 16% | 79% | 30% | 22% | can't tell from chance | 0.74R |
| 5m | smc_sweep_bear | 1261 | 34% | 24% | 15% | 82% | 31% | 21% | beats chance | 0.46R |
| 5m | smc_bos_up | 923 | 30% | 23% | 18% | 83% | 30% | 21% | can't tell from chance | 0.82R |
| 5m | smc_bos_down | 802 | 27% | 16% | 10% | 89% | 29% | 19% | can't tell from chance | 0.56R |
| 5m | smc_choch_up | 226 | 34% | 25% | 18% | 85% | 31% | 22% | can't tell from chance | 0.93R |
| 5m | smc_choch_down | 227 | 27% | 18% | 11% | 86% | 29% | 19% | can't tell from chance | 0.59R |
| 5m | smc_fvg_retrace_bull | 3500 | 30% | 21% | 16% | 81% | 29% | 21% | can't tell from chance | 0.88R |
| 5m | smc_fvg_retrace_bear | 3025 | 28% | 18% | 12% | 84% | 30% | 20% | worse than chance | 0.55R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (moderate) | WEAK_BULL (moderate) | WEAK_BULL (weak) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (moderate) | RANGE (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H RANGE)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (moderate) | RANGE (moderate) | RANGE (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H RANGE)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | RANGE (moderate) | WEAK_BULL (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H RANGE, 1H WEAK_BULL)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | UNCLEAR (weak) | RANGE (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H RANGE)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (weak) | RANGE (strong) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H RANGE)) |
| **SUI** | UNCLEAR (weak) | EXPANSION down (weak) | UNCLEAR (weak) | COMPRESSION (moderate) | NO TRADE (timeframes disagree (1D EXPANSION, 4H UNCLEAR, 1H COMPRESSION)) |
| **AVAX** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (moderate) | RANGE (weak) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **HBAR** | RANGE (weak) | EXPANSION up (weak) | STRONG_BULL (moderate) | TRANSITION (weak) | LONG allowed (1D/4H bullish, 1W RANGE) |
| **ENA** | TRANSITION (weak) | WEAK_BULL (weak) | TRANSITION (moderate) | WEAK_BULL (weak) | LONG allowed (1D/1H bullish, 1W TRANSITION) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (moderate)** - for: EMA-fast rising (+1.5 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.73x normal, Bollinger width above 56% of the last 100 candles · against: EMAs not lined up
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.5 ATR in 10 candles); ADX 42 = strong trend; candle size 1.03x normal, Bollinger width above 82% of the last 100 candles; volume 0.88x normal · against: swing structure mixed (neutral)
- **4H WEAK_BULL (weak)** - for: close above EMA-fast above EMA-slow; swing structure up (HH/HL); candle size 0.95x normal, Bollinger width above 30% of the last 100 candles; volume 0.74x normal · against: EMA-fast flat (+0.0 ATR in 10 candles) (neutral); ADX 10 = weak trend / ranging
- **1H RANGE (moderate)** - for: EMA-fast flat (-0.2 ATR in 10 candles); swing structure mixed; ADX 14 = weak trend / ranging; candle size 1.04x normal, Bollinger width above 37% of the last 100 candles · against: close above EMA-fast above EMA-slow

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **NY AM**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (CHOCH 24 candles ago) | buy-side (bearish idea) 10 candles ago | bull 83,440.99-83,537.21 | bear 84,342.00-84,843.00 | above the range (107%) | swing high 84,563.99 (1.68 ATR) | equal lows 82,900.00 (2.62 ATR) |
| **ETH** | down (BOS 24 candles ago) | sell-side (bullish idea) 38 candles ago | bull 2,680.00-2,684.70 | bull 2,652.20-2,695.38 | above the range (172%) | swing high 2,700.00 (0.14 ATR) | swing low 2,656.92 (2.59 ATR) |
| **SOL** | down (BOS 22 candles ago) | buy-side (bearish idea) 10 candles ago | bull 118.70-118.98 | bull 115.86-117.34 | premium (75%) | swing high 120.07 (0.56 ATR) | swing low 117.81 (1.67 ATR) |
| **XRP** | down (BOS 50 candles ago) | sell-side (bullish idea) 20 candles ago | bull 1.5039-1.5070 (retraced) | bull 1.3773-1.3856 | discount (36%) | swing high 1.5617 (3.21 ATR) | swing low 1.4897 (1.84 ATR) |
| **ZEC** | up (BOS 6 candles ago) | buy-side (bearish idea) 10 candles ago | bull 1,418.00-1,421.41 (retraced) | bear 1,540.16-1,569.23 | premium (79%) | swing high 1,433.91 (0.41 ATR) | swing low 1,390.74 (1.55 ATR) |
| **BNB** | up (BOS 12 candles ago) | buy-side (bearish idea) 6 candles ago | bull 765.88-766.80 | bear 774.08-780.19 | above the range (147%) | swing high 773.45 (0.78 ATR) | swing low 756.17 (3.1 ATR) |
| **SUI** | up (BOS 44 candles ago) | sell-side (bullish idea) 4 candles ago | bear 1.2025-1.2069 (retraced) | bull 1.0050-1.0598 | discount (26%) | swing high 1.1778 (1.47 ATR) | swing low 1.1415 (0.51 ATR) |

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
- **Heat:** max 3 positions, 1 per coin, 1 per group of correlated coins and direction (1h correlation ≥ 0.7) · groups now: BNB+BTC+ETH+SOL+SUI+XRP
- **Every live entry also needs:** reward to TP1 ≥ 2R, no opposing level before TP1, no high-impact event within ±60 min, no duplicate
- **Event calendar (next 7 days):** US GDP (Third Estimate), 2nd Quarter 2026 2026-09-30 12:30 UTC, US PCE / Personal Income and Outlays (Aug data) 2026-09-30 12:30 UTC, US jobs report / Employment Situation (Sep data) 2026-10-02 12:30 UTC · **BLACKOUT NOW:** US GDP (Third Estimate), 2nd Quarter 2026, US PCE / Personal Income and Outlays (Aug data)

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-09-30 00:55 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1104 | 39.5 | +0.169 | 1.31 | 31.9R | +0.16 / +0.19 | +0.21 / +0.12 | 5/5 | +0.14 | +0.11 | stable | 8 | 0.04R | 17, +0.64 (+0.86 / -1.03) | 87 / 45 of 255 | 0 | max drawdown 31.9R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1254 | 38.9 | +0.169 | 1.3 | 35.1R | +0.17 / +0.17 | +0.19 / +0.15 | 5/5 | +0.14 | +0.12 | stable | 9 | 0.04R | 18, +0.71 (+1.06 / -1.03) | 148 / 56 of 344 | 0 | max drawdown 35.1R |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1104 | 39.5 | +0.169 | 1.31 | 31.9R | +0.16 / +0.19 | +0.21 / +0.12 | 5/5 | +0.14 | +0.11 | stable | 8 | 0.04R | 17, +0.64 (+0.86 / -1.03) | 87 / 45 of 255 | 0 | max drawdown 31.9R |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 7 | 42.9 | +0.153 | 1.16 | 3.3R | +0.40 / -1.32 | -1.32 / +0.40 | 0/5 ✗ | -1.99 | -1.30 | ✗  stop buffer_atr 0.2→0.24: -1.78R | 0 | 0.27R | 1, -1.32 (-1.32 / +0.00) | 40 / 14 of 61 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 7 trades; profit factor 1.16; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1136 | 53.4 | +0.088 | 1.19 | 30.1R | +0.08 / +0.11 | +0.10 / +0.07 | 4/5 | +0.06 | +0.04 | stable | 6 | 0.04R | 18, +0.46 (+0.57 / -0.10) | 87 / 45 of 255 | 0 | avg +0.09R/trade (needs +0.10R); profit factor 1.19; max drawdown 30.1R |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.78 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.79 (+0.00 / +1.79) | 36 / 109 of 157 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 2 / 4 of 6 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 60 / 18 of 81 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 40 / 14 of 61 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 2 / 4 of 6 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 18 / 7 of 28 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 17 | 41.2 | -0.108 | 0.88 | 5.5R | -0.19 / +0.04 | -0.40 / +0.15 | 0/5 ✗ | -0.47 | -0.67 | ✗  sweep_bars 8→10: -0.33R | 0 | 0.39R | 3, -0.65 (+0.31 / -2.55) | 51 / 22 of 81 | 0 | not cost-viable: fees + slippage 0.39R per trade (stop must be ≥ 4x the round-trip cost); only 17 trades; avg -0.11R/trade (needs +0.10R); profit factor 0.88; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 15 | 46.7 | -0.196 | 0.65 | 4.3R | -0.15 / -0.37 | -0.37 / -0.11 | 0/5 ✗ | -0.18 | -0.37 | ✗  stop max_width_atr 3.0→3.6: -0.26R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 480 / 222 of 851 | 0 | only 15 trades; avg -0.20R/trade (needs +0.10R); profit factor 0.65; only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 14 | 35.7 | -0.235 | 0.57 | 3.9R | -0.31 / -0.11 | -0.24 / -0.23 | 0/5 ✗ | -0.33 | -0.22 | ✗  stop max_width_atr 3.0→2.4: -0.30R | 0 | 0.10R | 0, +0.00 (+0.00 / +0.00) | 543 / 200 of 879 | 0 | only 14 trades; avg -0.24R/trade (needs +0.10R); profit factor 0.57; only 5 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 40.0 | -0.396 | 0.59 | 2.6R | -0.55 / -0.17 | -0.17 / -0.55 | 0/5 ✗ | -0.54 | -0.66 | ✗  stop max_width_atr 3.0→2.4: -0.65R | 0 | 0.18R | 1, -2.55 (+0.00 / -2.55) | 18 / 7 of 28 | 0 | only 5 trades; avg -0.40R/trade (needs +0.10R); profit factor 0.59; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 6 | 0.0 | -1.084 | 0.0 | 6.5R | -1.07 / -1.16 | -0.99 / -1.13 | 0/5 ✗ | -1.08 | -1.14 | ✗  stop max_width_atr 3.0→2.4: -1.22R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 60 / 18 of 81 | 0 | only 6 trades; avg -1.08R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 285 | 51.6 | +0.022 | 1.04 | 30.7R | +0.15 / -0.23 | +0.10 / -0.05 | 2/5 ✗ | -0.02 | -0.06 | ✗  stop atr 1.5→1.8: -0.01R | 6 | 0.07R | 2, +0.10 (+0.00 / +0.10) | 97 / 23 of 139 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.04; max drawdown 30.7R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 195 | 51.8 | -0.020 | 0.96 | 31.6R | -0.14 / +0.26 | -0.07 / +0.03 | 2/5 ✗ | -0.08 | -0.14 | ✗  stop atr 1.5→1.2: -0.11R | 4 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 220 / 6 of 228 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 31.6R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1285 | 34.0 | -0.033 | 0.95 | 85.6R | -0.04 / -0.01 | +0.05 / -0.12 | 1/5 ✗ | -0.11 | -0.18 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.13R | 54, +0.12 (+0.24 / -0.61) | 149 / 41 of 365 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; max drawdown 85.6R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FAILED** | 1285 | 34.0 | -0.033 | 0.95 | 85.6R | -0.04 / -0.01 | +0.05 / -0.12 | 1/5 ✗ | -0.11 | -0.18 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.13R | 54, +0.12 (+0.24 / -0.61) | 149 / 41 of 365 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; max drawdown 85.6R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 847 | 51.2 | -0.051 | 0.91 | 67.9R | -0.05 / -0.04 | -0.09 / -0.02 | 0/5 ✗ | -0.14 | -0.21 | ✗  stop atr 1.5→1.2: -0.09R | 3 | 0.14R | 8, +0.30 (-0.02 / +0.84) | 136 / 42 of 215 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 67.9R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 3431 | 32.4 | -0.054 | 0.91 | 258.1R | -0.09 / +0.02 | -0.03 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 36, +0.53 (+0.53 / +0.50) | 209 / 118 of 556 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 258.1R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 3009 | 32.2 | -0.057 | 0.91 | 248.7R | -0.10 / +0.04 | -0.04 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 33, +0.46 (+0.53 / -0.24) | 127 / 83 of 400 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 248.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1511 | 33.5 | -0.057 | 0.91 | 124.4R | -0.07 / -0.03 | +0.01 / -0.13 | 1/5 ✗ | -0.14 | -0.21 | ✗  stop atr 2.0→1.6: -0.14R | 2 | 0.13R | 59, +0.14 (+0.18 / -0.00) | 236 / 67 of 506 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 124.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FAILED** | 3009 | 32.2 | -0.057 | 0.91 | 248.7R | -0.10 / +0.04 | -0.04 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 33, +0.46 (+0.53 / -0.24) | 127 / 83 of 400 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 248.7R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 3095 | 48.5 | -0.058 | 0.89 | 209.3R | -0.08 / -0.02 | -0.06 / -0.05 | 0/5 ✗ | -0.11 | -0.15 | ✗  stop atr 2.0→1.6: -0.07R | 1 | 0.08R | 35, +0.32 (+0.39 / -0.29) | 127 / 83 of 400 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 209.3R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 96 | 46.9 | -0.061 | 0.89 | 16.1R | +0.10 / -0.36 | -0.12 / +0.01 | 3/5 ✗ | -0.09 | -0.11 | ✗  st_n 10→8: -0.07R | 2 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 42 / 6 of 51 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 16.1R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1321 | 49.2 | -0.068 | 0.87 | 115.9R | -0.07 / -0.08 | -0.04 / -0.10 | 0/5 ✗ | -0.14 | -0.21 | ✗  stop atr 2.0→1.6: -0.14R | 2 | 0.13R | 54, +0.07 (+0.17 / -0.53) | 149 / 41 of 365 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; max drawdown 115.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1276 | 48.4 | -0.073 | 0.87 | 136.2R | -0.03 / -0.16 | +0.01 / -0.16 | 1/5 ✗ | -0.11 | -0.15 | ✗  long_rsi_hi 65→52: -0.17R | 3 | 0.06R | 10, +0.02 (+1.12 / -1.08) | 683 / 209 of 1059 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; max drawdown 136.2R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 38 | 50.0 | -0.082 | 0.85 | 6.0R | +0.07 / -0.46 | +0.31 / -0.43 | 2/5 ✗ | -0.11 | -0.14 | ✗  time_stop_bars 40→32: -0.08R | 1 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 156 / 4 of 163 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.85; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 214 | 41.1 | -0.102 | 0.84 | 51.0R | -0.14 / +0.08 | +0.12 / -0.26 | 2/5 ✗ | -0.16 | -0.21 | ✗  depth 0.985→1.182: -0.29R | 2 | 0.11R | 4, +0.21 (+0.21 / +0.00) | 75 / 3 of 88 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.84; max drawdown 51.0R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1917 | 56.5 | -0.105 | 0.63 | 201.6R | -0.10 / -0.11 | -0.12 / -0.09 | 0/5 ✗ | -0.14 | -0.16 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.05R | 6, -0.08 (-0.10 / -0.03) | 741 / 4 of 1002 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.63; max drawdown 201.6R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 367 | 45.2 | -0.119 | 0.78 | 51.7R | -0.12 / -0.11 | -0.18 / -0.06 | 0/5 ✗ | -0.18 | -0.25 | ✗  slow 21→17: -0.20R | 3 | 0.12R | 4, -0.30 (-1.00 / +1.82) | 149 / 9 of 168 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.78; max drawdown 51.7R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 7187 | 54.1 | -0.125 | 0.55 | 902.3R | -0.11 / -0.17 | -0.14 / -0.11 | 0/5 ✗ | -0.19 | -0.25 | ✗  stop atr 2.0→1.6: -0.15R | 0 | 0.11R | 42, -0.14 (-0.21 / -0.07) | 1049 / 6 of 1412 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.55; max drawdown 902.3R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 167 | 48.5 | -0.133 | 0.76 | 23.9R | -0.16 / -0.07 | -0.13 / -0.14 | 2/5 ✗ | -0.20 | -0.28 | ✗  adx_min 20→16: -0.17R | 2 | 0.14R | 6, -0.28 (-0.08 / -1.26) | 63 / 5 of 77 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.76; max drawdown 23.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6496 | 47.2 | -0.136 | 0.76 | 894.0R | -0.14 / -0.13 | -0.18 / -0.10 | 0/5 ✗ | -0.20 | -0.27 | ✗  stop atr 1.5→1.2: -0.17R | 0 | 0.13R | 49, -0.04 (+0.09 / -0.44) | 1136 / 292 of 1807 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 894.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 307 | 33.2 | -0.147 | 0.81 | 62.0R | -0.01 / -0.44 | -0.27 / -0.02 | 1/5 ✗ | -0.25 | -0.36 | ✗  time_stop_bars 30→36: -0.17R | 1 | 0.20R | 3, +0.89 (+2.70 / -0.01) | 91 / 220 of 322 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.81; max drawdown 62.0R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 81 | 34.6 | -0.168 | 0.77 | 23.2R | -0.31 / +0.40 | -0.17 / -0.17 | 1/5 ✗ | -0.23 | -0.34 | ✗  depth 0.985→1.182: -0.46R | 2 | 0.16R | 2, +1.30 (+1.30 / +0.00) | 42 / 2 of 46 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.77; max drawdown 23.2R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 274 | 45.6 | -0.184 | 0.68 | 55.3R | -0.18 / -0.18 | -0.29 / -0.10 | 1/5 ✗ | -0.25 | -0.30 | ✗  stop atr 2.0→1.6: -0.21R | 2 | 0.08R | 5, +0.39 (+0.39 / +0.00) | 60 / 2 of 71 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.68; max drawdown 55.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 309 | 48.2 | -0.192 | 0.68 | 59.5R | -0.17 / -0.24 | -0.20 / -0.19 | 0/5 ✗ | -0.29 | -0.38 | ✗  vol_x 1.2→1.44: -0.32R | 3 | 0.17R | 5, -0.41 (-0.41 / +0.00) | 95 / 201 of 306 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.68; max drawdown 59.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 469 | 45.0 | -0.192 | 0.68 | 92.2R | -0.19 / -0.19 | -0.26 / -0.16 | 0/5 ✗ | -0.34 | -0.48 | ✗  stop atr 1.5→1.2: -0.29R | 1 | 0.27R | 20, -0.21 (+0.14 / -1.04) | 78 / 16 of 116 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.19R/trade (needs +0.10R); profit factor 0.68; max drawdown 92.2R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 298 | 48.0 | -0.195 | 0.68 | 67.3R | -0.13 / -0.36 | -0.32 / -0.09 | 0/5 ✗ | -0.32 | -0.42 | ✗  stop atr 1.5→1.2: -0.27R | 1 | 0.20R | 4, -1.21 (-1.18 / -1.24) | 175 / 9 of 193 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 67.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2827 | 46.3 | -0.199 | 0.39 | 565.0R | -0.18 / -0.24 | -0.24 / -0.16 | 0/5 ✗ | -0.30 | -0.41 | ✗  stop atr 2.0→1.6: -0.25R | 0 | 0.17R | 40, -0.04 (+0.03 / -0.07) | 1066 / 26 of 1300 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.39; max drawdown 565.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3505 | 46.1 | -0.201 | 0.68 | 705.2R | -0.17 / -0.27 | -0.21 / -0.19 | 0/5 ✗ | -0.32 | -0.43 | ✗  stop atr 1.5→1.2: -0.25R | 0 | 0.18R | 105, -0.07 (+0.27 / -0.85) | 836 / 263 of 1613 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 705.2R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 877 | 30.8 | -0.207 | 0.75 | 199.8R | -0.17 / -0.27 | -0.24 / -0.18 | 1/5 ✗ | -0.31 | -0.42 | ✗  stop buffer_atr 0.2→0.16: -0.26R | 1 | 0.21R | 18, -0.13 (+0.75 / -1.24) | 473 / 1125 of 1687 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.75; max drawdown 199.8R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 492 | 45.9 | -0.227 | 0.64 | 113.1R | -0.23 / -0.21 | -0.23 / -0.23 | 0/5 ✗ | -0.34 | -0.46 | ✗  stop atr 1.5→1.2: -0.31R | 1 | 0.20R | 19, -0.52 (-0.51 / -0.53) | 117 / 32 of 189 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.64; max drawdown 113.1R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 347 | 39.8 | -0.243 | 0.6 | 86.8R | -0.22 / -0.32 | -0.31 / -0.20 | 0/5 ✗ | -0.34 | -0.43 | ✗  fast 9→11: -0.33R | 1 | 0.17R | 12, -0.07 (+0.07 / -0.76) | 120 / 20 of 158 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.60; max drawdown 86.8R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 3094 | 45.1 | -0.258 | 0.61 | 799.8R | -0.24 / -0.29 | -0.30 / -0.24 | 0/5 ✗ | -0.41 | -0.58 | ✗  stop atr 1.5→1.2: -0.34R | 0 | 0.27R | 189, -0.12 (+0.07 / -0.75) | 1345 / 210 of 2200 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 799.8R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 37 | 35.1 | -0.295 | 0.59 | 12.8R | -0.01 / -0.66 | -0.49 / -0.07 | 1/5 ✗ | -0.46 | -0.59 | ✗  time_stop_bars 30→24: -0.33R | 2 | 0.17R | 7, -0.82 (-0.59 / -1.40) | 103 / 35 of 151 | 0 | avg -0.29R/trade (needs +0.10R); profit factor 0.59; max drawdown 12.8R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1298 | 29.3 | -0.312 | 0.6 | 406.8R | -0.33 / -0.26 | -0.28 / -0.34 | 0/5 ✗ | -0.39 | -0.46 | ✗  rsi_n 14→17: -0.38R | 1 | 0.14R | 3, -0.57 (-1.20 / +0.69) | 759 / 6 of 807 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.60; max drawdown 406.8R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1534 | 31.9 | -0.312 | 0.61 | 486.2R | -0.31 / -0.31 | -0.33 / -0.29 | 0/5 ✗ | -0.44 | -0.56 | ✗  rsi_n 14→17: -0.36R | 0 | 0.22R | 24, -0.13 (-0.41 / +0.34) | 584 / 16 of 693 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.61; max drawdown 486.2R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 550 | 42.5 | -0.345 | 0.52 | 194.1R | -0.33 / -0.38 | -0.30 / -0.36 | 0/5 ✗ | -0.51 | -0.66 | ✗  stop atr 1.5→1.2: -0.42R | 0 | 0.31R | 33, -0.66 (-0.56 / -1.09) | 91 / 34 of 176 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); avg -0.34R/trade (needs +0.10R); profit factor 0.52; max drawdown 194.1R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 2186 | 33.2 | -0.351 | 0.2 | 767.7R | -0.34 / -0.38 | -0.44 / -0.28 | 0/5 ✗ | -0.52 | -0.70 | ✗  hi 90→108: -0.44R | 0 | 0.30R | 65, -0.37 (-0.31 / -0.43) | 1277 / 42 of 1467 | 0 | not cost-viable: fees + slippage 0.30R per trade (stop must be ≥ 4x the round-trip cost); avg -0.35R/trade (needs +0.10R); profit factor 0.20; max drawdown 767.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 330 | 37.3 | -0.475 | 0.38 | 156.7R | -0.43 / -0.59 | -0.49 / -0.46 | 0/5 ✗ | -0.62 | -0.77 | ✗  stop atr 1.0→0.8: -0.52R | 0 | 0.28R | 15, -0.61 (-0.52 / -0.75) | 120 / 220 of 364 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R); profit factor 0.38; max drawdown 156.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 623 | 24.2 | -0.483 | 0.51 | 300.7R | -0.52 / -0.39 | -0.65 / -0.35 | 0/5 ✗ | -0.65 | -0.78 | ✗  stop buffer_atr 0.2→0.16: -0.51R | 1 | 0.34R | 25, -0.38 (+0.25 / -1.05) | 494 / 1045 of 1709 | 0 | not cost-viable: fees + slippage 0.34R per trade (stop must be ≥ 4x the round-trip cost); avg -0.48R/trade (needs +0.10R); profit factor 0.51; max drawdown 300.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 590 | 39.3 | -0.486 | 0.38 | 286.6R | -0.46 / -0.56 | -0.59 / -0.43 | 0/5 ✗ | -0.70 | -0.94 | ✗  stop atr 1.0→0.8: -0.56R | 0 | 0.39R | 36, -0.78 (-0.76 / -0.81) | 106 / 255 of 397 | 0 | not cost-viable: fees + slippage 0.39R per trade (stop must be ≥ 4x the round-trip cost); avg -0.49R/trade (needs +0.10R); profit factor 0.38; max drawdown 286.6R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 123 | 19.5 | -0.571 | 0.43 | 74.4R | -0.51 / -0.68 | -0.67 / -0.49 | 0/5 ✗ | -0.70 | -0.83 | ✗  stop max_width_atr 3.0→2.4: -0.57R | 1 | 0.27R | 5, +0.52 (+1.28 / +0.02) | 36 / 109 of 157 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.57R/trade (needs +0.10R); profit factor 0.43; max drawdown 74.4R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 284 | 32.7 | -0.640 | 0.3 | 184.1R | -0.73 / -0.51 | -0.57 / -0.92 | 0/5 ✗ | -1.03 | -1.43 | ✗  stop atr 1.5→1.2: -0.86R | 0 | 0.62R | 81, -0.48 (-0.46 / -0.51) | 205 / 55 of 344 | 0 | not cost-viable: fees + slippage 0.62R per trade (stop must be ≥ 4x the round-trip cost); avg -0.64R/trade (needs +0.10R); profit factor 0.30; max drawdown 184.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 478 | 24.7 | -1.175 | 0.14 | 561.7R | -1.25 / -1.09 | -1.05 / -1.77 | 0/5 ✗ | -1.84 | -2.49 | ✗  stop atr 1.0→0.8: -1.50R | 0 | 1.07R | 140, -1.18 (-1.31 / -0.92) | 216 / 651 of 1010 | 0 | not cost-viable: fees + slippage 1.07R per trade (stop must be ≥ 4x the round-trip cost); avg -1.18R/trade (needs +0.10R); profit factor 0.14; max drawdown 561.7R; not profitable in BOTH train and unseen test |

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
| `memory/smc_events.csv` | 391.8 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 16.2 KB | - | - |
| `memory/strategy_registry.csv` | 36.6 KB | - | - |
| `memory/trials.csv` | 9.2 KB | - | - |
| `memory/universe_log.md` | 12.7 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*