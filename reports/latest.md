# Crypto Signal Report

**Updated:** 2026-09-30 01:19 Beijing time (2026-09-29 17:19 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 8.1 MB (GitHub) · large files of this run 4.1 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-29 17:19 UTC / 2026-09-30 01:19 Beijing
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
| QNT | **DEGRADED** | 1d: DEGRADED: volume 91x normal on candle 09-27 00:00 UTC (possible bad data); 1d: DEGRADED: volume 87x normal on candle 09-28 00:00 UTC (possible bad data) |
| BABY | **DEGRADED** | 1d: DEGRADED: volume 51x normal on candle 09-26 00:00 UTC (possible bad data) |
- 75 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-29 17:18 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 819 h since 2026-08-26 | +0.0033% | 1.39 | 1.02 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 819 h since 2026-08-26 | +0.0060% | 1.36 | 1.15 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 819 h since 2026-08-26 | +0.0016% | 0.75 | 1.00 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 819 h since 2026-08-26 | -0.0014% | 1.60 | 1.25 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 819 h since 2026-08-26 | +0.0100% | 2.75 | 0.75 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 819 h since 2026-08-26 | +0.0057% | 1.96 | 0.91 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| LINK | GOOD | okx | 748 h since 2026-08-29 | +0.0100% | 1.55 | 0.73 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=LINKUSDT&period=1h&limit=500 |
| AVAX | GOOD | okx | 811 h since 2026-08-26 | +0.0100% | 1.78 | 0.82 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=AVAXUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 819 h since 2026-08-26 | +0.0066% | 2.19 | 1.53 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 819 h since 2026-08-26 | +0.0100% | 1.70 | 1.01 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **ZEC**, **SOL**, **XRP**, **SUI**, **LINK**
- **Research only** - backtested, never a signal: AVAX, BNB, UNI
- **Waiting to join:** AVAX (1/2 runs)
- **Outside the top, may leave:** LINK (1/2 runs)
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** HBAR - 7-day average volume $44M < $50M; suspended for the rest of the UTC day (moved more than ±25% earlier today); order book too thin: $204k within 1% (need $250k)

| Not eligible | 24h volume | Why |
|---|---|---|
| QNT | $151M | order book too thin: $169k within 1% (need $250k) |
| HBAR | $121M | 7-day average volume $44M < $50M; suspended for the rest of the UTC day (moved more than ±25% earlier today); order book too thin: $204k within 1% (need $250k) |
| BABY | $111M | 7-day average volume $39M < $50M; order book too thin: $67k within 1% (need $250k) |
| PUMP | $74M | 7-day average volume $41M < $50M; order book too thin: $161k within 1% (need $250k) |
| AAVE | $69M | 7-day average volume $23M < $50M; order book too thin: $146k within 1% (need $250k) |
| XLM | $56M | 7-day average volume $36M < $50M |

**Flags (not excluded):** QNT: price data DEGRADED - stays in the list, but no signals; BABY: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, RLUSD, USD1, USDC, WLD (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 476 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ETH | 476 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ZEC | 393 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| SOL | 320 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| XRP | 439 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| SUI | 178 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| LINK | 402 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-01 | OK (300 candles) |
| AVAX | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| BNB | 464 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| UNI | 315 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | up (HH/HL) | 84,564 / 82,775.9 | 0.41 | 1.19x | 1.31x | displacement_down |
| ETH | mixed (HH/LL) | 2,748.6 / 2,652.2 | 0.48 | 0.72x | 1.42x | displacement_down |
| ZEC | down (LH/LL) | 1,460.16 / 1,356 | 0.57 | 1.02x | 1.31x | displacement_down |
| SOL | mixed (HH/LL) | 121.69 / 116.32 | 0.45 | 1.29x | 1.07x | displacement_down, bear_engulf, failed_breakout_up |
| XRP | down (LH/LL) | 1.5038 / 1.4663 | 0.12 | 2.39x | 1.33x | displacement_down, bear_engulf, bear_reject, failed_breakout_up |
| SUI | mixed (HH/LL) | 1.1904 / 1.0922 | 0.47 | 0.89x | 0.99x | bear_engulf |
| LINK | mixed (LH/HL) | 15.614 / 14.631 | 0.42 | 0.90x | 1.45x | - |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 465 | 48% | 34% | 27% | 80% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | displacement_down | 386 | 51% | 32% | 21% | 75% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1221 | 44% | 31% | 22% | 77% | 44% | 30% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1365 | 43% | 29% | 19% | 78% | 48% | 32% | worse than chance | 0.08R |
| 4h | bull_reject | 926 | 42% | 29% | 20% | 78% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | bear_reject | 859 | 47% | 33% | 23% | 74% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 648 | 44% | 30% | 22% | 76% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 680 | 45% | 30% | 20% | 79% | 48% | 31% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 275 | 47% | 29% | 21% | 81% | 43% | 31% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 261 | 49% | 36% | 26% | 71% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 93 | 54% | 35% | 26% | 82% | 45% | 31% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 90 | 41% | 22% | 12% | 79% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 659 | 44% | 28% | 21% | 78% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | smc_fvg_retrace_bear | 697 | 45% | 29% | 19% | 77% | 47% | 31% | can't tell from chance | 0.08R |
| 1h | displacement_up | 609 | 44% | 33% | 27% | 73% | 42% | 30% | can't tell from chance | 0.29R |
| 1h | displacement_down | 424 | 39% | 26% | 16% | 81% | 37% | 23% | can't tell from chance | 0.19R |
| 1h | bull_engulf | 1730 | 40% | 29% | 22% | 75% | 42% | 30% | can't tell from chance | 0.33R |
| 1h | bear_engulf | 1878 | 38% | 24% | 17% | 80% | 38% | 24% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1410 | 40% | 28% | 21% | 75% | 42% | 29% | can't tell from chance | 0.31R |
| 1h | bear_reject | 1342 | 35% | 23% | 17% | 82% | 38% | 24% | worse than chance | 0.19R |
| 1h | smc_sweep_bull | 641 | 41% | 27% | 20% | 77% | 42% | 30% | can't tell from chance | 0.31R |
| 1h | smc_sweep_bear | 724 | 36% | 23% | 15% | 81% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 422 | 41% | 30% | 24% | 78% | 42% | 29% | can't tell from chance | 0.28R |
| 1h | smc_bos_down | 272 | 38% | 28% | 18% | 83% | 38% | 23% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 115 | 45% | 35% | 30% | 70% | 43% | 29% | can't tell from chance | 0.32R |
| 1h | smc_choch_down | 119 | 45% | 31% | 21% | 75% | 36% | 24% | can't tell from chance | 0.18R |
| 1h | smc_fvg_retrace_bull | 915 | 46% | 34% | 25% | 71% | 43% | 30% | can't tell from chance | 0.30R |
| 1h | smc_fvg_retrace_bear | 772 | 40% | 27% | 19% | 79% | 38% | 25% | can't tell from chance | 0.20R |
| 30m | displacement_up | 607 | 41% | 30% | 25% | 77% | 41% | 28% | can't tell from chance | 0.30R |
| 30m | displacement_down | 429 | 43% | 26% | 16% | 80% | 37% | 21% | beats chance | 0.19R |
| 30m | bull_engulf | 1706 | 41% | 30% | 22% | 74% | 41% | 29% | can't tell from chance | 0.34R |
| 30m | bear_engulf | 1832 | 38% | 23% | 16% | 80% | 37% | 22% | can't tell from chance | 0.21R |
| 30m | bull_reject | 1374 | 44% | 30% | 22% | 74% | 41% | 29% | beats chance | 0.33R |
| 30m | bear_reject | 1439 | 38% | 24% | 16% | 81% | 38% | 22% | can't tell from chance | 0.20R |
| 30m | smc_sweep_bull | 655 | 39% | 28% | 18% | 75% | 41% | 29% | can't tell from chance | 0.35R |
| 30m | smc_sweep_bear | 636 | 42% | 26% | 17% | 82% | 37% | 22% | beats chance | 0.20R |
| 30m | smc_bos_up | 473 | 41% | 33% | 28% | 75% | 41% | 29% | can't tell from chance | 0.31R |
| 30m | smc_bos_down | 241 | 36% | 23% | 12% | 85% | 37% | 22% | can't tell from chance | 0.23R |
| 30m | smc_choch_up | 90 | 38% | 24% | 19% | 80% | 40% | 28% | can't tell from chance | 0.39R |
| 30m | smc_choch_down | 96 | 45% | 29% | 23% | 76% | 33% | 19% | beats chance | 0.21R |
| 30m | smc_fvg_retrace_bull | 1005 | 42% | 29% | 23% | 75% | 41% | 29% | can't tell from chance | 0.34R |
| 30m | smc_fvg_retrace_bear | 783 | 38% | 22% | 16% | 80% | 37% | 22% | can't tell from chance | 0.22R |
| 15m | displacement_up | 462 | 37% | 28% | 21% | 81% | 34% | 23% | can't tell from chance | 0.42R |
| 15m | displacement_down | 460 | 33% | 23% | 14% | 84% | 38% | 23% | can't tell from chance | 0.31R |
| 15m | bull_engulf | 1690 | 36% | 25% | 18% | 79% | 33% | 24% | can't tell from chance | 0.51R |
| 15m | bear_engulf | 1649 | 37% | 24% | 16% | 77% | 37% | 23% | can't tell from chance | 0.30R |
| 15m | bull_reject | 1323 | 35% | 25% | 17% | 80% | 34% | 24% | can't tell from chance | 0.50R |
| 15m | bear_reject | 1439 | 36% | 23% | 15% | 81% | 38% | 23% | can't tell from chance | 0.30R |
| 15m | smc_sweep_bull | 630 | 34% | 23% | 18% | 79% | 34% | 24% | can't tell from chance | 0.47R |
| 15m | smc_sweep_bear | 621 | 37% | 24% | 14% | 84% | 37% | 23% | can't tell from chance | 0.28R |
| 15m | smc_bos_up | 350 | 39% | 27% | 23% | 80% | 34% | 24% | can't tell from chance | 0.46R |
| 15m | smc_bos_down | 362 | 38% | 23% | 16% | 83% | 36% | 22% | can't tell from chance | 0.32R |
| 15m | smc_choch_up | 83 | 33% | 23% | 16% | 83% | 33% | 23% | can't tell from chance | 0.45R |
| 15m | smc_choch_down | 87 | 32% | 23% | 16% | 82% | 37% | 25% | can't tell from chance | 0.33R |
| 15m | smc_fvg_retrace_bull | 1074 | 33% | 23% | 15% | 81% | 35% | 24% | can't tell from chance | 0.50R |
| 15m | smc_fvg_retrace_bear | 997 | 36% | 25% | 18% | 79% | 37% | 23% | can't tell from chance | 0.32R |
| 5m | displacement_up | 1286 | 32% | 22% | 18% | 84% | 28% | 20% | beats chance | 0.83R |
| 5m | displacement_down | 1193 | 26% | 17% | 11% | 88% | 30% | 20% | worse than chance | 0.52R |
| 5m | bull_engulf | 4254 | 27% | 19% | 14% | 82% | 28% | 20% | worse than chance | 0.89R |
| 5m | bear_engulf | 4229 | 30% | 19% | 12% | 84% | 30% | 20% | can't tell from chance | 0.54R |
| 5m | bull_reject | 3274 | 27% | 19% | 14% | 81% | 28% | 20% | can't tell from chance | 0.92R |
| 5m | bear_reject | 3653 | 32% | 20% | 13% | 82% | 30% | 20% | beats chance | 0.54R |
| 5m | smc_sweep_bull | 1247 | 28% | 19% | 14% | 81% | 30% | 21% | can't tell from chance | 0.80R |
| 5m | smc_sweep_bear | 1255 | 33% | 23% | 15% | 82% | 31% | 20% | can't tell from chance | 0.48R |
| 5m | smc_bos_up | 857 | 30% | 23% | 19% | 83% | 29% | 20% | can't tell from chance | 0.87R |
| 5m | smc_bos_down | 852 | 28% | 17% | 10% | 88% | 30% | 20% | can't tell from chance | 0.57R |
| 5m | smc_choch_up | 223 | 32% | 25% | 18% | 86% | 26% | 18% | beats chance | 0.95R |
| 5m | smc_choch_down | 226 | 23% | 12% | 8% | 89% | 29% | 19% | worse than chance | 0.59R |
| 5m | smc_fvg_retrace_bull | 3420 | 30% | 21% | 16% | 80% | 28% | 20% | beats chance | 0.90R |
| 5m | smc_fvg_retrace_bear | 3051 | 26% | 18% | 12% | 85% | 29% | 19% | worse than chance | 0.57R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (moderate) | WEAK_BULL (moderate) | RANGE (moderate) | HIGH_VOL_RANGE (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H HIGH_VOL_RANGE)) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (weak) | EXPANSION down (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H EXPANSION)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (weak) | UNCLEAR (weak) | STRONG_BEAR (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H STRONG_BEAR)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (moderate) | RANGE (weak) | RANGE (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H RANGE)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | RANGE (weak) | EXPANSION down (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H RANGE, 1H EXPANSION)) |
| **SUI** | UNCLEAR (weak) | EXPANSION down (weak) | TRANSITION (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D EXPANSION, 4H TRANSITION, 1H UNCLEAR)) |
| **LINK** | WEAK_BULL (moderate) | WEAK_BULL (weak) | TRANSITION (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H UNCLEAR)) |
| **AVAX** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (weak) | STRONG_BULL (moderate) | LONG allowed (1D/4H/1H bullish, 1W TRANSITION) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (moderate) | WEAK_BEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H WEAK_BEAR)) |
| **UNI** | EXPANSION up (moderate) | STRONG_BULL (moderate) | TRANSITION (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H TRANSITION, 1H TRANSITION)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (moderate)** - for: EMA-fast rising (+1.5 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.73x normal, Bollinger width above 56% of the last 100 candles · against: EMAs not lined up
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.5 ATR in 10 candles); ADX 43 = strong trend; candle size 1.05x normal, Bollinger width above 83% of the last 100 candles; volume 0.95x normal · against: swing structure mixed (neutral)
- **4H RANGE (moderate)** - for: EMAs not lined up; EMA-fast flat (-0.0 ATR in 10 candles); ADX 12 = weak trend / ranging; candle size 1.04x normal, Bollinger width above 35% of the last 100 candles · against: swing structure down (LH/LL)
- **1H HIGH_VOL_RANGE (weak)** - for: EMAs not lined up; EMA-fast flat (+0.1 ATR in 10 candles); ADX 19 = weak trend / ranging; candle size 1.31x normal, Bollinger width above 87% of the last 100 candles · against: swing structure up (HH/HL); ADX 19 is close to a threshold

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (BOS 12 candles ago) | sell-side (bullish idea) 7 candles ago | bear 83,242.40-83,364.00 (retraced) | bear 84,342.00-84,843.00 | discount (16%) | swing high 84,563.99 (3.08 ATR) | swing low 82,775.94 (0.58 ATR) |
| **ETH** | down (CHOCH 8 candles ago) | sell-side (bullish idea) 10 candles ago | bear 2,685.36-2,690.47 (retraced) | bull 2,652.20-2,695.38 | discount (25%) | swing high 2,748.60 (3.39 ATR) | equal lows 2,651.68 (1.14 ATR) |
| **ZEC** | up (CHOCH 22 candles ago) | buy-side (bearish idea) 35 candles ago | bear 1,406.91-1,417.37 | bear 1,540.16-1,569.23 | discount (35%) | swing high 1,460.16 (2.3 ATR) | swing low 1,356.00 (1.25 ATR) |
| **SOL** | down (BOS 7 candles ago) | sell-side (bullish idea) 1 candles ago | bear 118.76-119.14 (retraced) | bull 115.86-117.34 | discount (32%) | swing high 121.69 (2.92 ATR) | swing low 116.32 (1.4 ATR) |
| **XRP** | down (BOS 2 candles ago) | buy-side (bearish idea) 11 candles ago | bear 1.4922-1.5150 | bull 1.3773-1.3856 | premium (52%) | swing high 1.5810 (4.31 ATR) | swing low 1.4663 (0.89 ATR) |
| **SUI** | up (CHOCH 30 candles ago) | buy-side (bearish idea) 29 candles ago | bear 1.1570-1.1638 | bull 1.0050-1.0598 | discount (45%) | swing high 1.1904 (2.2 ATR) | swing low 1.0922 (1.83 ATR) |
| **LINK** | up (BOS 70 candles ago) | sell-side (bullish idea) 1 candles ago | bear 14.736-14.787 (retraced) | bull 13.642-13.992 | discount (8%) | swing high 15.614 (3.1 ATR) | swing low 13.476 (4.25 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **SIDEWAYS**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 73 (Greed), yesterday 74  (extreme fear/greed = bigger, faster moves)

## 2. Signals right now
Only **APPROVED** strategy versions (your yes, after paper trading) give signals and emails.

**No trade passes all the checks right now. That is normal - no trade is also a position.**

### 2c. Watching - no signal yet (report only, never emailed)
No tracked strategy (VALIDATION or higher) has its market filters open right now.

### 2d. Risk engine (section 15 - independent of the strategies)
- **Live results:** today +0.00R (limit -3R), this week +0.00R (limit -6R) · **halts:** none
- **Suspended strategies** (live drawdown > 8R): none
- **Risk per trade:** 0.5% · leverage never above 3x (the position is made smaller instead)
- **Heat:** max 3 positions, 1 per coin, 1 per group of correlated coins and direction (1h correlation ≥ 0.7) · groups now: BTC+ETH+LINK+SOL+SUI+XRP
- **Every live entry also needs:** reward to TP1 ≥ 2R, no opposing level before TP1, no high-impact event within ±60 min, no duplicate
- **Event calendar (next 7 days):** US GDP (Third Estimate), 2nd Quarter 2026 2026-09-30 12:30 UTC, US PCE / Personal Income and Outlays (Aug data) 2026-09-30 12:30 UTC, US jobs report / Employment Situation (Sep data) 2026-10-02 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-09-29 00:53 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 60.0 | +1.221 | 3.69 | 2.3R | +0.97 / +2.21 | +2.21 / +0.97 | 0/5 ✗ | +1.10 | +0.98 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 25 / 10 of 36 | 0 | only 5 trades; only 1 unseen-test trades |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.206 | 1.21 | 3.3R | +0.51 / -1.32 | -1.32 / +0.51 | 0/5 ✗ | +0.08 | -0.03 | ✗  sweep_bars 20→24: -0.16R | 0 | 0.26R | 1, -1.32 (-1.32 / +0.00) | 44 / 13 of 64 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 6 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 16 | 43.8 | +0.202 | 1.25 | 5.9R | +0.04 / +0.56 | +0.18 / +0.21 | 0/5 ✗ | -0.11 | -0.29 | ✗  sweep_bars 8→10: -0.10R | 0 | 0.34R | 2, +0.31 (+0.31 / +0.00) | 58 / 26 of 90 | 0 | not cost-viable: fees + slippage 0.34R per trade (stop must be ≥ 4x the round-trip cost); only 16 trades; only 5 unseen-test trades |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1060 | 39.5 | +0.197 | 1.36 | 26.1R | +0.17 / +0.24 | +0.23 / +0.15 | 5/5 | +0.17 | +0.14 | stable | 9 | 0.04R | 15, +0.46 (+0.56 / -1.03) | 93 / 54 of 269 | 0 | max drawdown 26.1R |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1060 | 39.5 | +0.197 | 1.36 | 26.1R | +0.17 / +0.24 | +0.23 / +0.15 | 5/5 | +0.17 | +0.14 | stable | 9 | 0.04R | 15, +0.46 (+0.56 / -1.03) | 93 / 54 of 269 | 0 | max drawdown 26.1R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1205 | 39.3 | +0.195 | 1.36 | 28.7R | +0.18 / +0.22 | +0.21 / +0.17 | 5/5 | +0.17 | +0.14 | stable | 10 | 0.04R | 16, +0.55 (+0.77 / -1.03) | 160 / 67 of 362 | 0 | max drawdown 28.7R |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1092 | 53.7 | +0.099 | 1.22 | 21.6R | +0.09 / +0.12 | +0.10 / +0.10 | 4/5 | +0.07 | +0.05 | stable | 7 | 0.04R | 17, +0.14 (+0.20 / -0.33) | 93 / 54 of 269 | 0 | avg +0.10R/trade (needs +0.10R); max drawdown 21.6R |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 14 | 35.7 | +0.088 | 1.2 | 2.5R | +0.07 / +0.14 | -0.76 / +0.23 | 1/5 ✗ | +0.02 | +0.08 | ✗  stop max_width_atr 3.0→3.6: -0.11R | 0 | 0.08R | 0, +0.00 (+0.00 / +0.00) | 554 / 203 of 901 | 0 | only 14 trades; avg +0.09R/trade (needs +0.10R); only 4 unseen-test trades |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.78 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.79 (+0.00 / +1.79) | 31 / 111 of 153 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **BACKTESTING** | 189 | 51.9 | +0.005 | 1.01 | 24.1R | -0.10 / +0.24 | -0.08 / +0.09 | 2/5 ✗ | -0.05 | -0.12 | ✗  stop atr 1.5→1.2: -0.06R | 4 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 213 / 4 of 220 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.01; max drawdown 24.1R; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 4 / 6 of 10 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 63 / 12 of 78 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 44 / 13 of 64 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 4 / 6 of 10 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 25 / 10 of 36 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 13 | 46.2 | -0.308 | 0.48 | 5.9R | -0.37 / +0.05 | -0.31 / -0.31 | 0/5 ✗ | -0.30 | -0.54 | ✗  time_stop_bars 30→24: -0.36R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 478 / 228 of 851 | 0 | only 13 trades; avg -0.31R/trade (needs +0.10R); profit factor 0.48; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 4 | 0.0 | -1.218 | 0.0 | 4.9R | -1.24 / -1.16 | -1.42 / -1.15 | 0/5 ✗ | -1.22 | -1.29 | ✗  sweep_bars 20→16: -1.22R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 63 / 12 of 78 | 0 | only 4 trades; avg -1.22R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 284 | 50.7 | +0.001 | 1.0 | 24.0R | +0.13 / -0.27 | +0.05 / -0.04 | 2/5 ✗ | -0.05 | -0.09 | ✗  stop atr 1.5→1.8: -0.02R | 6 | 0.07R | 3, -0.30 (+0.08 / -1.05) | 105 / 22 of 142 | 0 | avg +0.00R/trade (needs +0.10R); profit factor 1.00; max drawdown 24.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 838 | 53.0 | -0.012 | 0.98 | 37.2R | -0.01 / -0.02 | -0.06 / +0.03 | 2/5 ✗ | -0.09 | -0.17 | ✗  bb_k 2→1: -0.06R | 4 | 0.14R | 6, +0.53 (-0.23 / +1.29) | 143 / 33 of 213 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 37.2R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1286 | 34.2 | -0.037 | 0.94 | 112.3R | -0.06 / +0.01 | +0.02 / -0.10 | 2/5 ✗ | -0.12 | -0.19 | ✗  stop atr 2.0→1.6: -0.12R | 4 | 0.12R | 51, +0.00 (+0.15 / -0.77) | 150 / 37 of 364 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; max drawdown 112.3R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FAILED** | 1286 | 34.2 | -0.037 | 0.94 | 112.3R | -0.06 / +0.01 | +0.02 / -0.10 | 2/5 ✗ | -0.12 | -0.19 | ✗  stop atr 2.0→1.6: -0.12R | 4 | 0.12R | 51, +0.00 (+0.15 / -0.77) | 150 / 37 of 364 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; max drawdown 112.3R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 3323 | 32.2 | -0.055 | 0.91 | 268.9R | -0.08 / +0.01 | -0.03 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 32, +0.53 (+0.58 / +0.08) | 211 / 126 of 549 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 268.9R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1519 | 33.7 | -0.056 | 0.92 | 132.4R | -0.07 / -0.02 | -0.01 / -0.11 | 1/5 ✗ | -0.14 | -0.22 | ✗  stop atr 2.0→1.6: -0.13R | 3 | 0.13R | 56, +0.04 (+0.08 / -0.12) | 246 / 59 of 510 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.92; max drawdown 132.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2925 | 31.8 | -0.061 | 0.9 | 264.4R | -0.10 / +0.02 | -0.04 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.09R | 30, +0.46 (+0.57 / -1.08) | 126 / 93 of 400 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.90; max drawdown 264.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FAILED** | 2925 | 31.8 | -0.061 | 0.9 | 265.2R | -0.10 / +0.02 | -0.04 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.09R | 30, +0.46 (+0.57 / -1.08) | 126 / 93 of 400 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.90; max drawdown 265.2R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1320 | 49.2 | -0.066 | 0.88 | 117.2R | -0.07 / -0.04 | -0.04 / -0.09 | 1/5 ✗ | -0.14 | -0.21 | ✗  stop atr 2.0→1.6: -0.14R | 3 | 0.12R | 51, +0.04 (+0.12 / -0.40) | 150 / 37 of 364 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 117.2R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 3011 | 47.7 | -0.069 | 0.87 | 238.5R | -0.09 / -0.03 | -0.07 / -0.06 | 0/5 ✗ | -0.12 | -0.17 | ✗  stop atr 2.0→1.6: -0.09R | 1 | 0.09R | 32, +0.41 (+0.51 / -0.60) | 126 / 93 of 400 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; max drawdown 238.5R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1202 | 47.9 | -0.075 | 0.86 | 141.4R | -0.02 / -0.20 | -0.02 / -0.14 | 2/5 ✗ | -0.12 | -0.15 | ✗  long_rsi_hi 65→52: -0.14R | 3 | 0.06R | 13, +0.39 (+1.03 / -0.36) | 653 / 194 of 1013 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.86; max drawdown 141.4R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 34 | 50.0 | -0.094 | 0.82 | 5.6R | +0.03 / -0.40 | +0.23 / -0.45 | 2/5 ✗ | -0.12 | -0.15 | ✗  time_stop_bars 40→32: -0.11R | 1 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 166 / 6 of 174 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.82; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1836 | 56.2 | -0.103 | 0.64 | 189.0R | -0.09 / -0.13 | -0.12 / -0.09 | 0/5 ✗ | -0.13 | -0.16 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.05R | 8, -0.25 (-0.32 / -0.03) | 729 / 3 of 987 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.64; max drawdown 189.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 90 | 46.7 | -0.110 | 0.8 | 18.5R | +0.05 / -0.38 | -0.13 / -0.08 | 3/5 ✗ | -0.14 | -0.16 | ✗  st_n 10→8: -0.12R | 1 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 43 / 6 of 51 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.80; max drawdown 18.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 344 | 44.5 | -0.127 | 0.77 | 53.2R | -0.13 / -0.12 | -0.19 / -0.06 | 1/5 ✗ | -0.19 | -0.26 | ✗  slow 21→17: -0.19R | 3 | 0.12R | 3, -1.00 (-1.00 / +0.00) | 150 / 9 of 167 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.77; max drawdown 53.2R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 6905 | 53.7 | -0.131 | 0.54 | 910.8R | -0.11 / -0.17 | -0.14 / -0.12 | 0/5 ✗ | -0.20 | -0.26 | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 37, -0.16 (-0.20 / -0.12) | 1055 / 9 of 1398 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.54; max drawdown 910.8R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6220 | 47.4 | -0.135 | 0.77 | 850.9R | -0.14 / -0.13 | -0.17 / -0.10 | 0/5 ✗ | -0.20 | -0.28 | ✗  stop atr 1.5→1.2: -0.17R | 1 | 0.13R | 51, -0.14 (-0.03 / -0.41) | 1167 / 298 of 1856 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.77; max drawdown 850.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 447 | 45.0 | -0.162 | 0.72 | 72.3R | -0.15 / -0.20 | -0.22 / -0.13 | 0/5 ✗ | -0.30 | -0.44 | ✗  stop atr 1.5→1.2: -0.29R | 1 | 0.25R | 21, -0.28 (+0.04 / -1.09) | 79 / 14 of 117 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.72; max drawdown 72.3R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 259 | 39.0 | -0.167 | 0.74 | 66.8R | -0.18 / -0.12 | +0.14 / -0.36 | 1/5 ✗ | -0.22 | -0.28 | ✗  depth 0.985→1.182: -0.29R | 1 | 0.10R | 4, +0.53 (+0.48 / +0.69) | 75 / 6 of 87 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.74; max drawdown 66.8R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 91 | 35.2 | -0.170 | 0.76 | 27.0R | -0.34 / +0.33 | -0.17 / -0.17 | 1/5 ✗ | -0.23 | -0.33 | ✗  depth 0.985→1.182: -0.45R | 2 | 0.15R | 0, +0.00 (+0.00 / +0.00) | 39 / 6 of 45 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.76; max drawdown 27.0R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 44 | 36.4 | -0.181 | 0.74 | 12.5R | -0.00 / -0.47 | -0.43 / +0.05 | 1/5 ✗ | -0.38 | -0.47 | ✗  time_stop_bars 30→24: -0.19R | 3 | 0.16R | 6, -0.79 (-0.48 / -1.40) | 104 / 33 of 152 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.74; max drawdown 12.5R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2796 | 47.5 | -0.188 | 0.42 | 527.8R | -0.17 / -0.24 | -0.24 / -0.14 | 0/5 ✗ | -0.29 | -0.39 | ✗  stop atr 2.0→1.6: -0.24R | 0 | 0.16R | 33, -0.11 (+0.01 / -0.17) | 1068 / 26 of 1272 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.42; max drawdown 527.8R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 288 | 31.9 | -0.190 | 0.76 | 74.7R | -0.09 / -0.42 | -0.38 / +0.03 | 1/5 ✗ | -0.29 | -0.40 | ✗  time_stop_bars 30→36: -0.21R | 1 | 0.20R | 4, +0.34 (+2.70 / -0.44) | 85 / 236 of 332 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.76; max drawdown 74.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3534 | 46.3 | -0.191 | 0.69 | 678.6R | -0.18 / -0.22 | -0.21 / -0.17 | 0/5 ✗ | -0.30 | -0.41 | ✗  stop atr 1.5→1.2: -0.26R | 0 | 0.18R | 106, -0.14 (+0.15 / -0.67) | 855 / 253 of 1690 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.69; max drawdown 678.6R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 509 | 46.4 | -0.191 | 0.7 | 98.9R | -0.22 / -0.09 | -0.24 / -0.14 | 1/5 ✗ | -0.30 | -0.42 | ✗  stop atr 1.5→1.2: -0.27R | 1 | 0.18R | 21, -0.45 (-0.45 / -0.43) | 119 / 35 of 201 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.70; max drawdown 98.9R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 298 | 47.7 | -0.202 | 0.67 | 60.5R | -0.19 / -0.22 | -0.26 / -0.12 | 0/5 ✗ | -0.29 | -0.38 | ✗  vol_x 1.2→1.44: -0.34R | 2 | 0.17R | 6, -0.54 (-0.41 / -1.20) | 109 / 198 of 317 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.67; max drawdown 60.5R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 165 | 45.5 | -0.206 | 0.64 | 34.0R | -0.22 / -0.17 | -0.21 / -0.20 | 1/5 ✗ | -0.27 | -0.35 | ✗  adx_min 20→24: -0.30R | 1 | 0.13R | 8, -0.48 (-0.25 / -1.18) | 56 / 6 of 73 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.64; max drawdown 34.0R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 294 | 46.6 | -0.217 | 0.65 | 70.0R | -0.13 / -0.44 | -0.34 / -0.10 | 0/5 ✗ | -0.34 | -0.43 | ✗  stop atr 1.5→1.2: -0.30R | 1 | 0.19R | 4, -0.16 (+0.23 / -1.33) | 184 / 8 of 205 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.65; max drawdown 70.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 334 | 40.1 | -0.224 | 0.62 | 78.7R | -0.20 / -0.31 | -0.29 / -0.17 | 0/5 ✗ | -0.32 | -0.42 | ✗  fast 9→11: -0.29R | 0 | 0.16R | 11, +0.08 (+0.20 / -0.44) | 117 / 18 of 151 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.62; max drawdown 78.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 808 | 30.3 | -0.241 | 0.71 | 210.4R | -0.24 / -0.24 | -0.33 / -0.16 | 0/5 ✗ | -0.34 | -0.44 | ✗  stop buffer_atr 0.2→0.16: -0.28R | 1 | 0.22R | 17, -0.41 (+0.05 / -1.26) | 480 / 1162 of 1737 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.71; max drawdown 210.4R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 288 | 43.1 | -0.256 | 0.58 | 77.4R | -0.27 / -0.23 | -0.34 / -0.17 | 0/5 ✗ | -0.31 | -0.36 | ✗  st_n 10→12: -0.28R | 1 | 0.08R | 5, +0.39 (+0.39 / +0.00) | 60 / 3 of 71 | 0 | avg -0.26R/trade (needs +0.10R); profit factor 0.58; max drawdown 77.4R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 3129 | 44.6 | -0.263 | 0.61 | 830.3R | -0.24 / -0.31 | -0.30 / -0.24 | 0/5 ✗ | -0.42 | -0.57 | ✗  stop atr 1.5→1.2: -0.34R | 0 | 0.26R | 203, -0.22 (-0.03 / -0.82) | 1337 / 218 of 2218 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 830.3R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1505 | 32.2 | -0.295 | 0.63 | 445.9R | -0.30 / -0.29 | -0.29 / -0.30 | 0/5 ✗ | -0.42 | -0.55 | ✗  stop atr 1.5→1.2: -0.35R | 0 | 0.21R | 28, -0.15 (-0.25 / -0.00) | 624 / 28 of 744 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.63; max drawdown 445.9R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1245 | 29.8 | -0.300 | 0.62 | 376.5R | -0.32 / -0.24 | -0.28 / -0.31 | 0/5 ✗ | -0.38 | -0.45 | ✗  rsi_n 14→17: -0.39R | 1 | 0.14R | 7, -0.16 (-0.44 / +0.54) | 745 / 10 of 799 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.62; max drawdown 376.5R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 2199 | 35.1 | -0.323 | 0.22 | 711.0R | -0.30 / -0.36 | -0.42 / -0.25 | 0/5 ✗ | -0.49 | -0.66 | ✗  hi 90→108: -0.42R | 0 | 0.28R | 54, -0.37 (-0.22 / -0.55) | 1314 / 40 of 1474 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.32R/trade (needs +0.10R); profit factor 0.22; max drawdown 711.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 567 | 40.7 | -0.376 | 0.48 | 219.0R | -0.34 / -0.45 | -0.36 / -0.39 | 0/5 ✗ | -0.52 | -0.66 | ✗  stop atr 1.5→1.2: -0.45R | 0 | 0.29R | 39, -0.64 (-0.68 / -0.41) | 89 / 35 of 182 | 0 | not cost-viable: fees + slippage 0.29R per trade (stop must be ≥ 4x the round-trip cost); avg -0.38R/trade (needs +0.10R); profit factor 0.48; max drawdown 219.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 628 | 24.8 | -0.449 | 0.54 | 286.1R | -0.46 / -0.43 | -0.54 / -0.36 | 0/5 ✗ | -0.62 | -0.75 | ✗  n 20→24: -0.49R | 1 | 0.32R | 26, +0.02 (+0.26 / -0.37) | 482 / 1061 of 1736 | 0 | not cost-viable: fees + slippage 0.32R per trade (stop must be ≥ 4x the round-trip cost); avg -0.45R/trade (needs +0.10R); profit factor 0.54; max drawdown 286.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 342 | 37.4 | -0.469 | 0.38 | 160.3R | -0.42 / -0.58 | -0.48 / -0.46 | 0/5 ✗ | -0.62 | -0.78 | ✗  stop atr 1.0→0.8: -0.55R | 0 | 0.27R | 16, -0.90 (-0.80 / -1.04) | 122 / 224 of 376 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R); profit factor 0.38; max drawdown 160.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 579 | 38.7 | -0.486 | 0.39 | 283.5R | -0.43 / -0.64 | -0.61 / -0.42 | 0/5 ✗ | -0.69 | -0.93 | ✗  stop atr 1.0→0.8: -0.55R | 0 | 0.36R | 43, -0.66 (-0.63 / -0.71) | 111 / 259 of 416 | 0 | not cost-viable: fees + slippage 0.36R per trade (stop must be ≥ 4x the round-trip cost); avg -0.49R/trade (needs +0.10R); profit factor 0.39; max drawdown 283.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 114 | 20.2 | -0.489 | 0.5 | 59.5R | -0.38 / -0.71 | -0.54 / -0.44 | 0/5 ✗ | -0.63 | -0.76 | ✗  stop max_width_atr 3.0→2.4: -0.49R | 1 | 0.25R | 5, +0.20 (+0.51 / +0.00) | 31 / 111 of 153 | 0 | avg -0.49R/trade (needs +0.10R); profit factor 0.50; max drawdown 59.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 311 | 28.6 | -0.749 | 0.23 | 233.0R | -0.83 / -0.61 | -0.72 / -0.95 | 0/5 ✗ | -1.13 | -1.48 | ✗  stop atr 1.5→1.2: -0.96R | 0 | 0.58R | 83, -0.51 (-0.53 / -0.47) | 204 / 65 of 354 | 0 | not cost-viable: fees + slippage 0.58R per trade (stop must be ≥ 4x the round-trip cost); avg -0.75R/trade (needs +0.10R); profit factor 0.23; max drawdown 233.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 492 | 25.2 | -1.159 | 0.15 | 572.4R | -1.25 / -1.06 | -1.06 / -1.98 | 0/5 ✗ | -1.80 | -2.44 | ✗  stop atr 1.0→0.8: -1.48R | 0 | 1.03R | 152, -1.13 (-1.17 / -1.04) | 224 / 632 of 1015 | 0 | not cost-viable: fees + slippage 1.03R per trade (stop must be ≥ 4x the round-trip cost); avg -1.16R/trade (needs +0.10R); profit factor 0.15; max drawdown 572.4R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **25** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 118 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.34** (Bonferroni: family-wise false-winner rate 0.05 over 118 trials; with 1 trial it would be 1.65).

**Research run duration:** 7.8 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 25 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (74.4 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 35 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

0 of 59 strategy / timeframe tests would get a different verdict.

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (80% of 3,323 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (75% of 1,519 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 1,205 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,925 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,286 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (95% of 1,060 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,925 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,286 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (95% of 1,060 trades shared)

🧪 **Strategy lab:** 5 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 15m | 5 | +1.221 | +2.214 | +0.202 | +0.561 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 6 | +0.206 | -1.323 | -0.308 | +0.049 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 2 | +0.037 | +0.037 | -0.632 | -0.616 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.181 | -0.467 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +2.214 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 4 | -1.218 | -1.163 | +0.088 | +0.138 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 288 | -0.190 | -0.423 | -0.241 | -0.243 | no |
| S8-PDH-PDL-SWEEP | 30m | 114 | -0.489 | -0.712 | -0.449 | -0.428 | no |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): macd_trend_cross@1.0 1h FAILED → BACKTESTING

### 3c. Research layers (daily run)
Last run: **2026-09-29 00:53 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 10 | 2017-08-17 | 2026-09-28 | 19963 |  |
| 1h | 10 | 2017-08-17 | 2026-09-28 | 79788 |  |
| 30m | 10 | 2024-09-29 | 2026-09-29 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 10 | 2025-09-29 | 2026-09-29 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 10 | 2026-07-01 | 2026-09-29 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 1060 (641) | false_breakout, trend_reversal | false_breakout 62% | +0.47R | -0.38R | +0.26 / +0.20 |
| donchian_breakout-VEXIT-VRVOL | 4h | BACKTESTING | 1060 (641) | false_breakout, trend_reversal | false_breakout 62% | +0.47R | -0.38R | +0.26 / +0.20 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 1205 (732) | false_breakout, trend_reversal | false_breakout 62% | +0.48R | -0.37R | +0.26 / +0.20 |
| donchian_breakout | 4h | BACKTESTING | 1092 (506) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 65%, stop_too_tight 35% | +0.35R | -0.37R | +0.15 / +0.10 |
| macd_trend_cross | 1h | BACKTESTING | 189 (91) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 91%, indicator_lag 37%, stop_too_tight 31% | +0.32R | -0.35R | +0.16 / +0.01 |
| bb_squeeze_breakout | 4h | FAILED | 284 (140) | false_breakout, stop_too_tight, structural_change | false_breakout 56%, stop_too_tight 42% | +0.35R | -0.33R | +0.09 / +0.00 |
| bb_squeeze_breakout | 1h | FAILED | 838 (394) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, no_displacement 53%, stop_too_tight 36%, regime_mismatch 36% | +0.36R | -0.43R | +0.16 / -0.01 |
| donchian_breakout-VEXIT | 30m | FAILED | 1286 (846) | false_breakout | false_breakout 72% | +0.48R | -0.39R | +0.12 / -0.04 |
| donchian_breakout-VEXIT-VRVOL | 30m | FAILED | 1286 (846) | false_breakout | false_breakout 72% | +0.48R | -0.39R | +0.12 / -0.04 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 3323 (2254) | htf_conflict, no_displacement, false_breakout, regime_mismatch | false_breakout 64% | +0.51R | -0.38R | +0.05 / -0.06 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1519 (1007) | false_breakout | false_breakout 72% | +0.47R | -0.40R | +0.11 / -0.06 |
| donchian_breakout-VEXIT | 1h | FAILED | 2925 (1994) | false_breakout | false_breakout 63% | +0.52R | -0.38R | +0.04 / -0.06 |
| donchian_breakout-VEXIT-VRVOL | 1h | FAILED | 2925 (1994) | no_displacement, false_breakout | false_breakout 63% | +0.52R | -0.38R | +0.04 / -0.06 |
| donchian_breakout | 30m | FAILED | 1320 (671) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 75%, stop_too_tight 34% | +0.30R | -0.41R | +0.09 / -0.07 |
| donchian_breakout | 1h | FAILED | 3011 (1574) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 32% | +0.37R | -0.39R | +0.04 / -0.07 |
| trend_pullback | 4h | FAILED | 1202 (626) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 38%, stop_too_tight 25% | +0.36R | -0.42R | +0.00 / -0.07 |
| macd_trend_cross | 4h | FAILED | 34 (17) | structural_change | regime_mismatch 94%, no_displacement 88%, indicator_lag 53%, low_relative_volume 47% | +0.17R | -0.40R | -0.01 / -0.09 |
| rsi2_dip_buy | 4h | FAILED | 1836 (804) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 44% | +0.16R | -0.21R | -0.04 / -0.10 |
| supertrend_flip | 4h | FAILED | 90 (48) | regime_mismatch, stop_too_tight, indicator_lag, structural_change | regime_mismatch 69%, indicator_lag 40%, stop_too_tight 25% | +0.39R | -0.43R | -0.04 / -0.11 |
| ema_9_21_cross | 1h | FAILED | 344 (191) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 46%, stop_too_tight 27% | +0.29R | -0.38R | +0.02 / -0.13 |
| rsi2_dip_buy | 1h | FAILED | 6905 (3199) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 42% | +0.16R | -0.20R | -0.00 / -0.13 |
| trend_pullback | 1h | FAILED | 6220 (3273) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 76%, indicator_lag 45%, stop_too_tight 28% | +0.29R | -0.42R | +0.02 / -0.14 |
| ema_9_21_cross | 15m | FAILED | 447 (246) | stop_too_tight, indicator_lag | indicator_lag 47%, stop_too_tight 27% | +0.27R | -0.44R | +0.14 / -0.16 |
| R4-CLUC | 30m | FAILED | 259 (158) | none | - | +0.35R | -0.49R | -0.06 / -0.17 |
| R4-CLUC | 15m | FAILED | 91 (59) | none | - | +0.40R | -0.25R | -0.02 / -0.17 |
| S6-OB-FVG-noSMC | 15m | FAILED | 44 (28) | none | - | +0.24R | -0.50R | +0.01 / -0.18 |
| rsi2_dip_buy | 30m | FAILED | 2796 (1468) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 34% | +0.16R | -0.19R | +0.02 / -0.19 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 288 (196) | stop_too_tight, sweep_continued | sweep_continued 97%, range_market 56%, stop_too_tight 29% | +0.55R | -0.44R | +0.06 / -0.19 |
| trend_pullback | 30m | FAILED | 3534 (1897) | stop_too_tight, indicator_lag | indicator_lag 47%, stop_too_tight 31% | +0.27R | -0.42R | +0.04 / -0.19 |
| bb_squeeze_breakout | 30m | FAILED | 509 (273) | false_breakout, stop_too_tight | false_breakout 62%, stop_too_tight 40% | +0.28R | -0.43R | +0.06 / -0.19 |
| liquidity_sweep_reversal | 1h | FAILED | 298 (156) | stop_too_tight | stop_too_tight 53% | +0.30R | -0.46R | -0.00 / -0.20 |
| supertrend_flip | 30m | FAILED | 165 (90) | stop_too_tight, indicator_lag | regime_mismatch 43%, indicator_lag 41%, stop_too_tight 34%, late_entry 27% | +0.32R | -0.46R | -0.04 / -0.21 |
| macd_trend_cross | 30m | FAILED | 294 (157) | overextended_entry, stop_too_tight, indicator_lag | no_displacement 86%, indicator_lag 46%, low_relative_volume 45%, stop_too_tight 29% | +0.30R | -0.44R | +0.02 / -0.22 |
| ema_9_21_cross | 30m | FAILED | 334 (200) | indicator_lag | indicator_lag 45%, low_relative_volume 38% | +0.27R | -0.42R | -0.01 / -0.22 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 808 (563) | range_market, stop_too_tight | range_market 47%, stop_too_tight 35% | +0.62R | -0.51R | +0.01 / -0.24 |
| supertrend_flip | 1h | FAILED | 288 (164) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 69%, stop_too_tight 34%, indicator_lag 34% | +0.38R | -0.37R | -0.15 / -0.26 |
| trend_pullback | 15m | FAILED | 3129 (1732) | wrong_session, stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 32% | +0.25R | -0.44R | +0.06 / -0.26 |
| R4-BBRSI | 30m | FAILED | 1505 (1021) | none | - | +0.43R | -0.44R | -0.04 / -0.29 |
| R4-BBRSI | 1h | FAILED | 1245 (874) | none | - | +0.44R | -0.45R | -0.13 / -0.30 |
| rsi2_dip_buy | 15m | FAILED | 2199 (1427) | trend_reversal, fees_slippage | fees_slippage 44% | +0.17R | -0.19R | +0.01 / -0.32 |
| bb_squeeze_breakout | 15m | FAILED | 567 (336) | stop_too_tight | false_breakout 58%, no_displacement 57%, stop_too_tight 40% | +0.29R | -0.48R | -0.03 / -0.38 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 628 (472) | stop_too_tight | stop_too_tight 33% | +0.60R | -0.54R | -0.05 / -0.45 |
| liquidity_sweep_reversal | 30m | FAILED | 342 (214) | stop_too_tight | stop_too_tight 40% | +0.40R | -0.45R | -0.15 / -0.47 |
| liquidity_sweep_reversal | 15m | FAILED | 579 (355) | stop_too_tight | stop_too_tight 38% | +0.37R | -0.45R | -0.02 / -0.49 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 114 (91) | stop_too_tight, sweep_continued | sweep_continued 96%, stop_too_tight 26% | +0.50R | -0.65R | -0.15 / -0.49 |
| ema_9_21_cross | 5m | FAILED | 311 (222) | stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 31% | +0.24R | -0.42R | -0.04 / -0.75 |
| liquidity_sweep_reversal | 5m | FAILED | 492 (368) | htf_conflict, fees_slippage, stop_too_tight | stop_too_tight 37%, fees_slippage 25% | +0.29R | -0.48R | +0.14 / -1.16 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 27 strategy/timeframe tests); `false_breakout` (systematic in 15 strategy/timeframe tests); `regime_mismatch` (systematic in 13 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `trend_reversal` (systematic in 8 strategy/timeframe tests); `no_displacement` (systematic in 4 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `fees_slippage` (systematic in 3 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `htf_conflict` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- BTC down -2.4% (2026-09-27 21:00 → 2026-09-28 10:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ZEC down -8.9% (2026-09-28 12:00 → 2026-09-28 20:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- SOL down -4.1% (2026-09-27 21:00 → 2026-09-28 10:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- LINK up +13.0% (2026-09-28 09:00 → 2026-09-28 21:00 UTC): identifiable: at least one strategy had a valid signal before the move
- UNI down -8.6% (2026-09-27 23:00 → 2026-09-28 10:00 UTC): not identifiable: no strategy had a setup before the move
- BNB down -2.6% (2026-09-27 21:00 → 2026-09-28 10:00 UTC): not identifiable: no strategy had a setup before the move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 104.8 KB | - | - |
| `memory/coin_notes.md` | 6.8 KB | 7 | 2026-09-27 00:26 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 5.7 KB | 12 | 2026-09-29 07:21 UTC |
| `memory/experiments.md` | 48.1 KB | 19 | 2026-09-28 15:40 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 58.5 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 7.2 KB | - | - |
| `memory/missed_trades.md` | 15.1 KB | 20 | 2026-09-29 00:53 UTC |
| `memory/playbook.md` | 8.7 KB | - | - |
| `memory/research_sources.md` | 59.7 KB | 45 | 2026-09-28 15:40 UTC |
| `memory/smc_events.csv` | 350.6 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 16.0 KB | - | - |
| `memory/strategy_registry.csv` | 36.9 KB | - | - |
| `memory/trials.csv` | 9.2 KB | - | - |
| `memory/universe_log.md` | 11.5 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*