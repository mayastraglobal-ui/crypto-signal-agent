# Crypto Signal Report

**Updated:** 2026-09-29 17:21 Beijing time (2026-09-29 09:21 UTC) · data: Binance · 9 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 7.3 MB (GitHub) · large files of this run 3.9 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-29 09:21 UTC / 2026-09-29 17:21 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US GDP (Third Estimate), 2nd Quarter 2026 2026-09-30 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.06% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| QNT | **DEGRADED** | 1d: DEGRADED: volume 91x normal on candle 09-27 00:00 UTC (possible bad data); 1d: DEGRADED: volume 87x normal on candle 09-28 00:00 UTC (possible bad data) |
| BABY | **DEGRADED** | 1d: DEGRADED: volume 51x normal on candle 09-26 00:00 UTC (possible bad data) |
- 68 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-29 09:21 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 811 h since 2026-08-26 | +0.0025% | 1.30 | 0.95 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 811 h since 2026-08-26 | +0.0057% | 1.07 | 1.14 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 811 h since 2026-08-26 | +0.0100% | 0.80 | 0.79 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 811 h since 2026-08-26 | +0.0058% | 1.59 | 0.81 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 811 h since 2026-08-26 | +0.0098% | 2.76 | 0.77 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 811 h since 2026-08-26 | +0.0100% | 1.98 | 0.80 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| LINK | GOOD | okx | 740 h since 2026-08-29 | -0.0039% | 1.38 | 1.04 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=LINKUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 811 h since 2026-08-26 | +0.0031% | 1.82 | 1.00 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 811 h since 2026-08-26 | +0.0061% | 2.12 | 0.85 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| AVAX | GOOD | okx | 803 h since 2026-08-26 | +0.0065% | 1.81 | 0.88 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=AVAXUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (6/7)** - only these can give signals: **BTC**, **ETH**, **ZEC**, **SOL**, **XRP**, **SUI**
- 1 empty slot(s): waiting for a coin to hold a top-7 rank for 2 runs in a row
- **Research only** - backtested, never a signal: BNB, AVAX, ENA
- **Waiting to join:** BNB (1/2 runs)
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** LINK - order book too thin: $226k within 1% (need $250k)
  - **EXCLUDED** UNI - order book too thin: $201k within 1% (need $250k)
  - **LEAVE** LINK - not eligible: order book too thin: $226k within 1% (need $250k)

| Not eligible | 24h volume | Why |
|---|---|---|
| LINK | $149M | order book too thin: $226k within 1% (need $250k) |
| QNT | $204M | order book too thin: $52k within 1% (need $250k) |
| HBAR | $189M | 7-day average volume $44M < $50M; suspended for the rest of the UTC day (moved more than ±25% earlier today) |
| BABY | $104M | 7-day average volume $39M < $50M; order book too thin: $75k within 1% (need $250k) |
| UNI | $99M | order book too thin: $201k within 1% (need $250k) |
| XLM | $78M | 7-day average volume $36M < $50M |
| PUMP | $70M | 7-day average volume $41M < $50M; order book too thin: $50k within 1% (need $250k) |
| ONDO | $52M | order book too thin: $192k within 1% (need $250k) |

**Flags (not excluded):** QNT: price data DEGRADED - stays in the list, but no signals; BABY: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, RLUSD, TAO, USD1, USDC, WLD, XAUT (see `config.yaml`)

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
| BNB | 464 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| AVAX | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| ENA | 130 | 910 | 904 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (LH/HL) | 84,381.3 / 82,775.9 | 0.13 | 0.99x | 1.21x | bear_reject |
| ETH | down (LH/LL) | 2,695.38 / 2,652.2 | 0.09 | 2.51x | 1.35x | displacement_up, bear_reject |
| ZEC | down (LH/LL) | 1,489.14 / 1,356 | 0.13 | 0.79x | 1.32x | bear_engulf |
| SOL | mixed (HH/LL) | 120.73 / 116.32 | 0.25 | 0.83x | 1.06x | bear_engulf |
| XRP | down (LH/LL) | 1.5038 / 1.4663 | 0.17 | 0.65x | 1.08x | bear_engulf |
| SUI | down (LH/LL) | 1.17 / 1.0922 | 0.22 | 0.56x | 1.01x | - |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 423 | 47% | 33% | 26% | 81% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | displacement_down | 337 | 50% | 34% | 22% | 75% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1091 | 44% | 31% | 22% | 78% | 43% | 30% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1230 | 44% | 29% | 20% | 78% | 48% | 32% | worse than chance | 0.08R |
| 4h | bull_reject | 847 | 41% | 28% | 20% | 79% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | bear_reject | 807 | 47% | 32% | 22% | 74% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 584 | 44% | 29% | 22% | 77% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 608 | 44% | 29% | 20% | 79% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 240 | 45% | 28% | 21% | 82% | 44% | 31% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 231 | 51% | 37% | 23% | 71% | 49% | 33% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 82 | 51% | 33% | 27% | 83% | 45% | 32% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 80 | 39% | 25% | 14% | 78% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 600 | 42% | 27% | 21% | 78% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | smc_fvg_retrace_bear | 632 | 45% | 31% | 20% | 77% | 47% | 32% | can't tell from chance | 0.08R |
| 1h | displacement_up | 538 | 44% | 33% | 27% | 73% | 42% | 29% | can't tell from chance | 0.29R |
| 1h | displacement_down | 374 | 38% | 25% | 16% | 82% | 37% | 24% | can't tell from chance | 0.20R |
| 1h | bull_engulf | 1571 | 39% | 29% | 21% | 75% | 42% | 29% | can't tell from chance | 0.33R |
| 1h | bear_engulf | 1678 | 38% | 25% | 17% | 80% | 38% | 24% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1265 | 39% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.32R |
| 1h | bear_reject | 1253 | 36% | 25% | 18% | 81% | 38% | 25% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bull | 574 | 40% | 25% | 19% | 78% | 41% | 29% | can't tell from chance | 0.31R |
| 1h | smc_sweep_bear | 651 | 38% | 24% | 15% | 80% | 37% | 24% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 369 | 43% | 32% | 25% | 76% | 42% | 30% | can't tell from chance | 0.27R |
| 1h | smc_bos_down | 247 | 38% | 28% | 19% | 83% | 38% | 24% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 99 | 48% | 36% | 31% | 70% | 40% | 29% | can't tell from chance | 0.34R |
| 1h | smc_choch_down | 99 | 43% | 31% | 19% | 73% | 37% | 22% | can't tell from chance | 0.19R |
| 1h | smc_fvg_retrace_bull | 796 | 43% | 30% | 24% | 73% | 42% | 29% | can't tell from chance | 0.31R |
| 1h | smc_fvg_retrace_bear | 718 | 40% | 28% | 19% | 78% | 38% | 24% | can't tell from chance | 0.21R |
| 30m | displacement_up | 568 | 41% | 30% | 25% | 77% | 42% | 29% | can't tell from chance | 0.30R |
| 30m | displacement_down | 373 | 43% | 27% | 16% | 81% | 36% | 21% | beats chance | 0.21R |
| 30m | bull_engulf | 1545 | 42% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.35R |
| 30m | bear_engulf | 1640 | 37% | 23% | 16% | 80% | 36% | 22% | can't tell from chance | 0.22R |
| 30m | bull_reject | 1195 | 44% | 28% | 21% | 74% | 41% | 29% | can't tell from chance | 0.35R |
| 30m | bear_reject | 1298 | 37% | 22% | 15% | 81% | 37% | 22% | can't tell from chance | 0.21R |
| 30m | smc_sweep_bull | 590 | 39% | 26% | 17% | 77% | 42% | 29% | can't tell from chance | 0.36R |
| 30m | smc_sweep_bear | 575 | 42% | 27% | 18% | 81% | 37% | 21% | beats chance | 0.21R |
| 30m | smc_bos_up | 403 | 41% | 33% | 28% | 75% | 41% | 29% | can't tell from chance | 0.32R |
| 30m | smc_bos_down | 216 | 37% | 22% | 12% | 85% | 37% | 22% | can't tell from chance | 0.24R |
| 30m | smc_choch_up | 88 | 39% | 25% | 20% | 82% | 44% | 30% | can't tell from chance | 0.41R |
| 30m | smc_choch_down | 88 | 40% | 25% | 22% | 78% | 41% | 23% | can't tell from chance | 0.22R |
| 30m | smc_fvg_retrace_bull | 894 | 41% | 28% | 22% | 76% | 42% | 29% | can't tell from chance | 0.36R |
| 30m | smc_fvg_retrace_bear | 706 | 39% | 22% | 16% | 80% | 37% | 22% | can't tell from chance | 0.23R |
| 15m | displacement_up | 414 | 36% | 27% | 20% | 82% | 35% | 25% | can't tell from chance | 0.44R |
| 15m | displacement_down | 408 | 32% | 21% | 13% | 84% | 37% | 22% | can't tell from chance | 0.32R |
| 15m | bull_engulf | 1514 | 35% | 25% | 18% | 79% | 34% | 23% | can't tell from chance | 0.52R |
| 15m | bear_engulf | 1485 | 37% | 24% | 15% | 78% | 37% | 23% | can't tell from chance | 0.31R |
| 15m | bull_reject | 1204 | 33% | 23% | 15% | 81% | 34% | 23% | can't tell from chance | 0.53R |
| 15m | bear_reject | 1330 | 36% | 23% | 14% | 80% | 37% | 23% | can't tell from chance | 0.30R |
| 15m | smc_sweep_bull | 551 | 33% | 22% | 17% | 80% | 34% | 24% | can't tell from chance | 0.50R |
| 15m | smc_sweep_bear | 569 | 37% | 24% | 14% | 84% | 37% | 23% | can't tell from chance | 0.29R |
| 15m | smc_bos_up | 324 | 37% | 27% | 22% | 79% | 34% | 24% | can't tell from chance | 0.44R |
| 15m | smc_bos_down | 325 | 35% | 22% | 15% | 82% | 37% | 24% | can't tell from chance | 0.33R |
| 15m | smc_choch_up | 77 | 34% | 23% | 16% | 81% | 33% | 25% | can't tell from chance | 0.48R |
| 15m | smc_choch_down | 79 | 34% | 23% | 18% | 81% | 37% | 24% | can't tell from chance | 0.33R |
| 15m | smc_fvg_retrace_bull | 954 | 33% | 24% | 16% | 81% | 33% | 24% | can't tell from chance | 0.52R |
| 15m | smc_fvg_retrace_bear | 873 | 36% | 25% | 17% | 79% | 36% | 22% | can't tell from chance | 0.33R |
| 5m | displacement_up | 1171 | 31% | 21% | 17% | 84% | 28% | 20% | beats chance | 0.84R |
| 5m | displacement_down | 1075 | 25% | 16% | 11% | 88% | 29% | 19% | worse than chance | 0.56R |
| 5m | bull_engulf | 3797 | 26% | 19% | 14% | 82% | 28% | 20% | can't tell from chance | 0.93R |
| 5m | bear_engulf | 3777 | 29% | 19% | 12% | 84% | 29% | 19% | can't tell from chance | 0.57R |
| 5m | bull_reject | 2946 | 26% | 18% | 13% | 81% | 27% | 19% | can't tell from chance | 0.96R |
| 5m | bear_reject | 3374 | 31% | 19% | 13% | 83% | 30% | 19% | can't tell from chance | 0.54R |
| 5m | smc_sweep_bull | 1101 | 28% | 20% | 13% | 81% | 28% | 20% | can't tell from chance | 0.83R |
| 5m | smc_sweep_bear | 1132 | 33% | 24% | 16% | 82% | 31% | 20% | can't tell from chance | 0.50R |
| 5m | smc_bos_up | 787 | 30% | 22% | 18% | 83% | 28% | 20% | can't tell from chance | 0.87R |
| 5m | smc_bos_down | 783 | 26% | 16% | 9% | 89% | 28% | 19% | can't tell from chance | 0.62R |
| 5m | smc_choch_up | 205 | 32% | 24% | 17% | 86% | 29% | 21% | can't tell from chance | 0.98R |
| 5m | smc_choch_down | 203 | 23% | 14% | 8% | 88% | 31% | 20% | worse than chance | 0.60R |
| 5m | smc_fvg_retrace_bull | 3101 | 29% | 20% | 15% | 81% | 27% | 19% | beats chance | 0.94R |
| 5m | smc_fvg_retrace_bear | 2715 | 26% | 17% | 11% | 85% | 29% | 19% | worse than chance | 0.61R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (moderate) | WEAK_BULL (moderate) | RANGE (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H UNCLEAR)) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (weak) | HIGH_VOL_RANGE (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H HIGH_VOL_RANGE)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (weak) | UNCLEAR (weak) | STRONG_BEAR (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H STRONG_BEAR)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (moderate) | RANGE (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H UNCLEAR)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | RANGE (weak) | RANGE (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H RANGE, 1H RANGE)) |
| **SUI** | UNCLEAR (weak) | EXPANSION down (weak) | WEAK_BULL (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D EXPANSION, 4H WEAK_BULL, 1H TRANSITION)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (moderate) | HIGH_VOL_RANGE (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H HIGH_VOL_RANGE)) |
| **AVAX** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (weak) | EXPANSION up (weak) | LONG allowed (1D/4H/1H bullish, 1W TRANSITION) |
| **ENA** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (moderate) | TRANSITION (weak) | LONG allowed (1D/4H bullish, 1W TRANSITION) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (moderate)** - for: EMA-fast rising (+1.5 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.73x normal, Bollinger width above 56% of the last 100 candles · against: EMAs not lined up
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.5 ATR in 10 candles); ADX 43 = strong trend; candle size 1.05x normal, Bollinger width above 83% of the last 100 candles; volume 0.95x normal · against: swing structure mixed (neutral)
- **4H RANGE (weak)** - for: EMA-fast flat (+0.1 ATR in 10 candles); ADX 13 = weak trend / ranging; candle size 0.98x normal, Bollinger width above 31% of the last 100 candles · against: close above EMA-fast above EMA-slow; swing structure down (LH/LL)
- **1H UNCLEAR (weak)** - for: candle size 1.21x normal, Bollinger width above 74% of the last 100 candles · against: close above EMA-fast above EMA-slow; EMA-fast flat (-0.3 ATR in 10 candles); swing structure mixed; ADX 20 = in between (20-25); ADX 20 is close to a threshold; signals are mixed and trend strength is in between

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (CHOCH 32 candles ago) | buy-side (bearish idea) 7 candles ago | bear 83,882.01-84,044.75 | bear 84,342.00-84,843.00 | premium (68%) | swing high 84,381.30 (1.12 ATR) | swing low 82,775.94 (2.43 ATR) |
| **ETH** | up (BOS 13 candles ago) | buy-side (bearish idea) 3 candles ago | bear 2,712.71-2,715.79 | bear 2,745.99-2,784.40 | above the range (131%) | swing high 2,743.00 (1.68 ATR) | equal lows 2,651.68 (2.8 ATR) |
| **ZEC** | down (BOS 17 candles ago) | buy-side (bearish idea) 3 candles ago | bear 1,410.17-1,418.76 (retraced) | bear 1,540.16-1,569.23 | discount (38%) | swing high 1,489.14 (2.79 ATR) | swing low 1,356.00 (1.71 ATR) |
| **SOL** | down (CHOCH 31 candles ago) | buy-side (bearish idea) 10 candles ago | bear 119.23-119.39 | bull 115.86-117.34 | premium (65%) | swing high 120.73 (1.29 ATR) | swing low 116.32 (2.37 ATR) |
| **XRP** | down (CHOCH 31 candles ago) | sell-side (bullish idea) 30 candles ago | bear 1.5020-1.5052 (retraced) | bull 1.3773-1.3856 | premium (92%) | swing high 1.5324 (1.76 ATR) | swing low 1.4663 (1.92 ATR) |
| **SUI** | down (BOS 32 candles ago) | buy-side (bearish idea) 40 candles ago | bear 1.1447-1.1501 (retraced) | bull 1.0050-1.0598 | premium (67%) | swing high 1.1700 (1.05 ATR) | swing low 1.0922 (2.08 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
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
- **Heat:** max 3 positions, 1 per coin, 1 per group of correlated coins and direction (1h correlation ≥ 0.7) · groups now: BTC+ETH+SOL+SUI+XRP
- **Every live entry also needs:** reward to TP1 ≥ 2R, no opposing level before TP1, no high-impact event within ±60 min, no duplicate
- **Event calendar (next 7 days):** US GDP (Third Estimate), 2nd Quarter 2026 2026-09-30 12:30 UTC, US PCE / Personal Income and Outlays (Aug data) 2026-09-30 12:30 UTC, US jobs report / Employment Situation (Sep data) 2026-10-02 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-09-29 00:53 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 60.0 | +1.221 | 3.69 | 2.3R | +0.97 / +2.21 | +2.21 / +0.97 | 0/5 ✗ | +1.10 | +0.98 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 22 / 11 of 34 | 0 | only 5 trades; only 1 unseen-test trades |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.206 | 1.21 | 3.3R | +0.51 / -1.32 | -1.32 / +0.51 | 0/5 ✗ | +0.08 | -0.03 | ✗  sweep_bars 20→24: -0.16R | 0 | 0.26R | 1, -1.32 (-1.32 / +0.00) | 37 / 15 of 59 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 6 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 16 | 43.8 | +0.202 | 1.25 | 5.9R | +0.04 / +0.56 | +0.18 / +0.21 | 0/5 ✗ | -0.11 | -0.29 | ✗  sweep_bars 8→10: -0.10R | 0 | 0.34R | 2, +0.31 (+0.31 / +0.00) | 49 / 26 of 81 | 0 | not cost-viable: fees + slippage 0.34R per trade (stop must be ≥ 4x the round-trip cost); only 16 trades; only 5 unseen-test trades |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1060 | 39.5 | +0.197 | 1.36 | 26.1R | +0.17 / +0.24 | +0.23 / +0.15 | 5/5 | +0.17 | +0.14 | stable | 9 | 0.04R | 15, +0.71 (+0.78 / +0.21) | 84 / 40 of 235 | 0 | max drawdown 26.1R |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1060 | 39.5 | +0.197 | 1.36 | 26.1R | +0.17 / +0.24 | +0.23 / +0.15 | 5/5 | +0.17 | +0.14 | stable | 9 | 0.04R | 15, +0.71 (+0.78 / +0.21) | 84 / 40 of 235 | 0 | max drawdown 26.1R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1205 | 39.3 | +0.195 | 1.36 | 28.7R | +0.18 / +0.22 | +0.21 / +0.17 | 5/5 | +0.17 | +0.14 | stable | 10 | 0.04R | 16, +0.78 (+1.01 / -0.21) | 141 / 51 of 317 | 0 | max drawdown 28.7R |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1092 | 53.7 | +0.099 | 1.22 | 21.6R | +0.09 / +0.12 | +0.10 / +0.10 | 4/5 | +0.07 | +0.05 | stable | 7 | 0.04R | 16, +0.41 (+0.46 / +0.20) | 84 / 40 of 235 | 0 | avg +0.10R/trade (needs +0.10R); max drawdown 21.6R |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 14 | 35.7 | +0.088 | 1.2 | 2.5R | +0.07 / +0.14 | -0.76 / +0.23 | 1/5 ✗ | +0.02 | +0.08 | ✗  stop max_width_atr 3.0→3.6: -0.11R | 0 | 0.08R | 0, +0.00 (+0.00 / +0.00) | 498 / 175 of 804 | 0 | only 14 trades; avg +0.09R/trade (needs +0.10R); only 4 unseen-test trades |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.78 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.79 (+0.00 / +1.79) | 31 / 99 of 141 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **BACKTESTING** | 189 | 51.9 | +0.005 | 1.01 | 24.1R | -0.10 / +0.24 | -0.08 / +0.09 | 2/5 ✗ | -0.05 | -0.12 | ✗  stop atr 1.5→1.2: -0.06R | 4 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 201 / 6 of 209 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.01; max drawdown 24.1R; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 2 / 5 of 7 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 56 / 14 of 73 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 37 / 15 of 59 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 2 / 5 of 7 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 22 / 11 of 34 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 13 | 46.2 | -0.308 | 0.48 | 5.9R | -0.37 / +0.05 | -0.31 / -0.31 | 0/5 ✗ | -0.30 | -0.54 | ✗  time_stop_bars 30→24: -0.36R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 406 / 215 of 757 | 0 | only 13 trades; avg -0.31R/trade (needs +0.10R); profit factor 0.48; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 4 | 0.0 | -1.218 | 0.0 | 4.9R | -1.24 / -1.16 | -1.42 / -1.15 | 0/5 ✗ | -1.22 | -1.29 | ✗  sweep_bars 20→16: -1.22R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 56 / 14 of 73 | 0 | only 4 trades; avg -1.22R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 284 | 50.7 | +0.001 | 1.0 | 24.0R | +0.13 / -0.27 | +0.05 / -0.04 | 2/5 ✗ | -0.05 | -0.09 | ✗  stop atr 1.5→1.8: -0.02R | 6 | 0.07R | 2, -1.08 (-1.11 / -1.05) | 92 / 20 of 128 | 0 | avg +0.00R/trade (needs +0.10R); profit factor 1.00; max drawdown 24.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 838 | 53.0 | -0.012 | 0.98 | 37.2R | -0.01 / -0.02 | -0.06 / +0.03 | 2/5 ✗ | -0.09 | -0.17 | ✗  bb_k 2→1: -0.06R | 4 | 0.14R | 6, +0.05 (-0.23 / +0.33) | 121 / 42 of 197 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 37.2R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1286 | 34.2 | -0.037 | 0.94 | 112.3R | -0.06 / +0.01 | +0.02 / -0.10 | 2/5 ✗ | -0.12 | -0.19 | ✗  stop atr 2.0→1.6: -0.12R | 4 | 0.12R | 48, +0.11 (+0.28 / -0.55) | 125 / 35 of 318 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; max drawdown 112.3R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FAILED** | 1286 | 34.2 | -0.037 | 0.94 | 112.3R | -0.06 / +0.01 | +0.02 / -0.10 | 2/5 ✗ | -0.12 | -0.19 | ✗  stop atr 2.0→1.6: -0.12R | 4 | 0.12R | 48, +0.11 (+0.28 / -0.55) | 125 / 35 of 318 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; max drawdown 112.3R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 3323 | 32.2 | -0.055 | 0.91 | 268.9R | -0.08 / +0.01 | -0.03 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 33, +0.44 (+0.52 / +0.10) | 189 / 117 of 510 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 268.9R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1519 | 33.7 | -0.056 | 0.92 | 132.4R | -0.07 / -0.02 | -0.01 / -0.11 | 1/5 ✗ | -0.14 | -0.22 | ✗  stop atr 2.0→1.6: -0.13R | 3 | 0.13R | 53, +0.08 (+0.20 / -0.31) | 209 / 56 of 452 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.92; max drawdown 132.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2925 | 31.8 | -0.061 | 0.9 | 264.4R | -0.10 / +0.02 | -0.04 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.09R | 30, +0.41 (+0.51 / -0.19) | 114 / 82 of 367 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.90; max drawdown 264.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FAILED** | 2925 | 31.8 | -0.061 | 0.9 | 265.2R | -0.10 / +0.02 | -0.04 / -0.08 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.09R | 30, +0.41 (+0.51 / -0.19) | 114 / 82 of 367 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.90; max drawdown 265.2R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1320 | 49.2 | -0.066 | 0.88 | 117.2R | -0.07 / -0.04 | -0.04 / -0.09 | 1/5 ✗ | -0.14 | -0.21 | ✗  stop atr 2.0→1.6: -0.14R | 3 | 0.12R | 48, +0.05 (+0.18 / -0.44) | 125 / 35 of 318 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 117.2R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 3011 | 47.7 | -0.069 | 0.87 | 238.5R | -0.09 / -0.03 | -0.07 / -0.06 | 0/5 ✗ | -0.12 | -0.17 | ✗  stop atr 2.0→1.6: -0.09R | 1 | 0.09R | 30, +0.35 (+0.46 / -0.34) | 114 / 82 of 367 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; max drawdown 238.5R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1202 | 47.9 | -0.075 | 0.86 | 141.4R | -0.02 / -0.20 | -0.02 / -0.14 | 2/5 ✗ | -0.12 | -0.15 | ✗  long_rsi_hi 65→52: -0.14R | 3 | 0.06R | 9, -0.03 (+0.93 / -0.81) | 601 / 174 of 920 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.86; max drawdown 141.4R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 34 | 50.0 | -0.094 | 0.82 | 5.6R | +0.03 / -0.40 | +0.23 / -0.45 | 2/5 ✗ | -0.12 | -0.15 | ✗  time_stop_bars 40→32: -0.11R | 1 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 149 / 4 of 155 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.82; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1836 | 56.2 | -0.103 | 0.64 | 189.0R | -0.09 / -0.13 | -0.12 / -0.09 | 0/5 ✗ | -0.13 | -0.16 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.05R | 7, -0.23 (-0.31 / -0.03) | 674 / 4 of 909 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.64; max drawdown 189.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 90 | 46.7 | -0.110 | 0.8 | 18.5R | +0.05 / -0.38 | -0.13 / -0.08 | 3/5 ✗ | -0.14 | -0.16 | ✗  st_n 10→8: -0.12R | 1 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 38 / 5 of 45 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.80; max drawdown 18.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 344 | 44.5 | -0.127 | 0.77 | 53.2R | -0.13 / -0.12 | -0.19 / -0.06 | 1/5 ✗ | -0.19 | -0.26 | ✗  slow 21→17: -0.19R | 3 | 0.12R | 4, -0.30 (-1.00 / +1.82) | 134 / 9 of 152 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.77; max drawdown 53.2R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 6905 | 53.7 | -0.131 | 0.54 | 910.8R | -0.11 / -0.17 | -0.14 / -0.12 | 0/5 ✗ | -0.20 | -0.26 | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 39, -0.19 (-0.30 / -0.08) | 945 / 7 of 1252 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.54; max drawdown 910.8R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6220 | 47.4 | -0.135 | 0.77 | 850.9R | -0.14 / -0.13 | -0.17 / -0.10 | 0/5 ✗ | -0.20 | -0.28 | ✗  stop atr 1.5→1.2: -0.17R | 1 | 0.13R | 45, -0.06 (-0.01 / -0.21) | 1026 / 268 of 1631 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.77; max drawdown 850.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 447 | 45.0 | -0.162 | 0.72 | 72.3R | -0.15 / -0.20 | -0.22 / -0.13 | 0/5 ✗ | -0.30 | -0.44 | ✗  stop atr 1.5→1.2: -0.29R | 1 | 0.25R | 18, -0.28 (+0.03 / -1.10) | 68 / 17 of 106 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.72; max drawdown 72.3R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 259 | 39.0 | -0.167 | 0.74 | 66.8R | -0.18 / -0.12 | +0.14 / -0.36 | 1/5 ✗ | -0.22 | -0.28 | ✗  depth 0.985→1.182: -0.29R | 1 | 0.10R | 4, +0.21 (+0.64 / -1.06) | 67 / 3 of 81 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.74; max drawdown 66.8R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 91 | 35.2 | -0.170 | 0.76 | 27.0R | -0.34 / +0.33 | -0.17 / -0.17 | 1/5 ✗ | -0.23 | -0.33 | ✗  depth 0.985→1.182: -0.45R | 2 | 0.15R | 2, +1.30 (+1.30 / +0.00) | 38 / 2 of 42 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.76; max drawdown 27.0R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 44 | 36.4 | -0.181 | 0.74 | 12.5R | -0.00 / -0.47 | -0.43 / +0.05 | 1/5 ✗ | -0.38 | -0.47 | ✗  time_stop_bars 30→24: -0.19R | 3 | 0.16R | 7, -0.82 (-0.59 / -1.40) | 97 / 32 of 144 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.74; max drawdown 12.5R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2796 | 47.5 | -0.188 | 0.42 | 527.8R | -0.17 / -0.24 | -0.24 / -0.14 | 0/5 ✗ | -0.29 | -0.39 | ✗  stop atr 2.0→1.6: -0.24R | 0 | 0.16R | 35, -0.09 (-0.20 / -0.02) | 960 / 24 of 1180 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.42; max drawdown 527.8R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 288 | 31.9 | -0.190 | 0.76 | 74.7R | -0.09 / -0.42 | -0.38 / +0.03 | 1/5 ✗ | -0.29 | -0.40 | ✗  time_stop_bars 30→36: -0.21R | 1 | 0.20R | 3, +0.89 (+0.00 / +0.89) | 85 / 198 of 292 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.76; max drawdown 74.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3534 | 46.3 | -0.191 | 0.69 | 678.6R | -0.18 / -0.22 | -0.21 / -0.17 | 0/5 ✗ | -0.30 | -0.41 | ✗  stop atr 1.5→1.2: -0.26R | 0 | 0.18R | 94, -0.08 (+0.27 / -0.76) | 771 / 215 of 1504 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.69; max drawdown 678.6R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 509 | 46.4 | -0.191 | 0.7 | 98.9R | -0.22 / -0.09 | -0.24 / -0.14 | 1/5 ✗ | -0.30 | -0.42 | ✗  stop atr 1.5→1.2: -0.27R | 1 | 0.18R | 18, -0.48 (-0.40 / -0.65) | 110 / 30 of 178 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.70; max drawdown 98.9R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 298 | 47.7 | -0.202 | 0.67 | 60.5R | -0.19 / -0.22 | -0.26 / -0.12 | 0/5 ✗ | -0.29 | -0.38 | ✗  vol_x 1.2→1.44: -0.34R | 2 | 0.17R | 5, -0.41 (-0.41 / +0.00) | 88 / 176 of 273 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.67; max drawdown 60.5R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 165 | 45.5 | -0.206 | 0.64 | 34.0R | -0.22 / -0.17 | -0.21 / -0.20 | 1/5 ✗ | -0.27 | -0.35 | ✗  adx_min 20→24: -0.30R | 1 | 0.13R | 6, -0.28 (-0.08 / -1.26) | 52 / 5 of 66 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.64; max drawdown 34.0R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 294 | 46.6 | -0.217 | 0.65 | 70.0R | -0.13 / -0.44 | -0.34 / -0.10 | 0/5 ✗ | -0.34 | -0.43 | ✗  stop atr 1.5→1.2: -0.30R | 1 | 0.19R | 5, -0.63 (-0.23 / -1.24) | 165 / 8 of 185 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.65; max drawdown 70.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 334 | 40.1 | -0.224 | 0.62 | 78.7R | -0.20 / -0.31 | -0.29 / -0.17 | 0/5 ✗ | -0.32 | -0.42 | ✗  fast 9→11: -0.29R | 0 | 0.16R | 11, -0.04 (+0.07 / -1.18) | 104 / 16 of 137 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.62; max drawdown 78.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 808 | 30.3 | -0.241 | 0.71 | 210.4R | -0.24 / -0.24 | -0.33 / -0.16 | 0/5 ✗ | -0.34 | -0.44 | ✗  stop buffer_atr 0.2→0.16: -0.28R | 1 | 0.22R | 16, -0.35 (+0.05 / -0.76) | 431 / 1024 of 1537 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.71; max drawdown 210.4R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 288 | 43.1 | -0.256 | 0.58 | 77.4R | -0.27 / -0.23 | -0.34 / -0.17 | 0/5 ✗ | -0.31 | -0.36 | ✗  st_n 10→12: -0.28R | 1 | 0.08R | 5, +0.39 (+0.39 / +0.00) | 52 / 2 of 62 | 0 | avg -0.26R/trade (needs +0.10R); profit factor 0.58; max drawdown 77.4R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 3129 | 44.6 | -0.263 | 0.61 | 830.3R | -0.24 / -0.31 | -0.30 / -0.24 | 0/5 ✗ | -0.42 | -0.57 | ✗  stop atr 1.5→1.2: -0.34R | 0 | 0.26R | 172, -0.16 (+0.06 / -0.84) | 1203 / 194 of 1983 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 830.3R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1505 | 32.2 | -0.295 | 0.63 | 445.9R | -0.30 / -0.29 | -0.29 / -0.30 | 0/5 ✗ | -0.42 | -0.55 | ✗  stop atr 1.5→1.2: -0.35R | 0 | 0.21R | 29, -0.23 (-0.19 / -0.31) | 537 / 16 of 636 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.63; max drawdown 445.9R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1245 | 29.8 | -0.300 | 0.62 | 376.5R | -0.32 / -0.24 | -0.28 / -0.31 | 0/5 ✗ | -0.38 | -0.45 | ✗  rsi_n 14→17: -0.39R | 1 | 0.14R | 7, -0.08 (-0.21 / +0.69) | 692 / 7 of 737 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.62; max drawdown 376.5R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 2199 | 35.1 | -0.323 | 0.22 | 711.0R | -0.30 / -0.36 | -0.42 / -0.25 | 0/5 ✗ | -0.49 | -0.66 | ✗  hi 90→108: -0.42R | 0 | 0.28R | 53, -0.31 (-0.27 / -0.38) | 1174 / 37 of 1315 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.32R/trade (needs +0.10R); profit factor 0.22; max drawdown 711.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 567 | 40.7 | -0.376 | 0.48 | 219.0R | -0.34 / -0.45 | -0.36 / -0.39 | 0/5 ✗ | -0.52 | -0.66 | ✗  stop atr 1.5→1.2: -0.45R | 0 | 0.29R | 34, -0.59 (-0.56 / -0.71) | 80 / 33 of 167 | 0 | not cost-viable: fees + slippage 0.29R per trade (stop must be ≥ 4x the round-trip cost); avg -0.38R/trade (needs +0.10R); profit factor 0.48; max drawdown 219.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 628 | 24.8 | -0.449 | 0.54 | 286.1R | -0.46 / -0.43 | -0.54 / -0.36 | 0/5 ✗ | -0.62 | -0.75 | ✗  n 20→24: -0.49R | 1 | 0.32R | 23, -0.28 (+0.41 / -1.04) | 440 / 938 of 1545 | 0 | not cost-viable: fees + slippage 0.32R per trade (stop must be ≥ 4x the round-trip cost); avg -0.45R/trade (needs +0.10R); profit factor 0.54; max drawdown 286.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 342 | 37.4 | -0.469 | 0.38 | 160.3R | -0.42 / -0.58 | -0.48 / -0.46 | 0/5 ✗ | -0.62 | -0.78 | ✗  stop atr 1.0→0.8: -0.55R | 0 | 0.27R | 15, -0.61 (-0.52 / -0.75) | 105 / 201 of 333 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R); profit factor 0.38; max drawdown 160.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 579 | 38.7 | -0.486 | 0.39 | 283.5R | -0.43 / -0.64 | -0.61 / -0.42 | 0/5 ✗ | -0.69 | -0.93 | ✗  stop atr 1.0→0.8: -0.55R | 0 | 0.36R | 33, -0.79 (-0.76 / -0.83) | 103 / 227 of 365 | 0 | not cost-viable: fees + slippage 0.36R per trade (stop must be ≥ 4x the round-trip cost); avg -0.49R/trade (needs +0.10R); profit factor 0.39; max drawdown 283.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 114 | 20.2 | -0.489 | 0.5 | 59.5R | -0.38 / -0.71 | -0.54 / -0.44 | 0/5 ✗ | -0.63 | -0.76 | ✗  stop max_width_atr 3.0→2.4: -0.49R | 1 | 0.25R | 5, +0.23 (-1.21 / +0.59) | 31 / 99 of 141 | 0 | avg -0.49R/trade (needs +0.10R); profit factor 0.50; max drawdown 59.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 311 | 28.6 | -0.749 | 0.23 | 233.0R | -0.83 / -0.61 | -0.72 / -0.95 | 0/5 ✗ | -1.13 | -1.48 | ✗  stop atr 1.5→1.2: -0.96R | 0 | 0.58R | 72, -0.48 (-0.47 / -0.49) | 200 / 59 of 332 | 0 | not cost-viable: fees + slippage 0.58R per trade (stop must be ≥ 4x the round-trip cost); avg -0.75R/trade (needs +0.10R); profit factor 0.23; max drawdown 233.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 492 | 25.2 | -1.159 | 0.15 | 572.4R | -1.25 / -1.06 | -1.06 / -1.98 | 0/5 ✗ | -1.80 | -2.44 | ✗  stop atr 1.0→0.8: -1.48R | 0 | 1.03R | 129, -1.23 (-1.34 / -1.01) | 204 / 567 of 901 | 0 | not cost-viable: fees + slippage 1.03R per trade (stop must be ≥ 4x the round-trip cost); avg -1.16R/trade (needs +0.10R); profit factor 0.15; max drawdown 572.4R; not profitable in BOTH train and unseen test |

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
| `memory/smc_events.csv` | 319.4 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 16.0 KB | - | - |
| `memory/strategy_registry.csv` | 36.9 KB | - | - |
| `memory/trials.csv` | 9.2 KB | - | - |
| `memory/universe_log.md` | 10.3 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*