# Crypto Signal Report

**Updated:** 2026-10-03 09:18 Beijing time (2026-10-03 01:18 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 10.0 MB (GitHub) · large files of this run 4.4 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-03 01:18 UTC / 2026-10-03 09:18 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · ⚠ calendar not maintained - no event listed for the next 7 days (events.yaml)
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.06% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| QNT | **DEGRADED** | 1d: DEGRADED: volume 60x normal on candle 09-30 00:00 UTC (possible bad data) |
- 73 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-03 01:18 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 899 h since 2026-08-26 | -0.0001% | 1.34 | 1.49 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 899 h since 2026-08-26 | +0.0007% | 1.86 | 1.35 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 899 h since 2026-08-26 | -0.0027% | 1.86 | 1.04 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 899 h since 2026-08-26 | -0.0091% | 3.05 | 0.86 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 899 h since 2026-08-26 | +0.0100% | 1.14 | 1.14 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 899 h since 2026-08-26 | -0.0095% | 2.58 | 1.50 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 899 h since 2026-08-26 | -0.0089% | 2.71 | 0.66 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| AVAX | GOOD | okx | 891 h since 2026-08-26 | -0.0215% | 2.81 | 0.83 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=AVAXUSDT&period=1h&limit=500 |
| LINK | GOOD | okx | 828 h since 2026-08-29 | +0.0013% | 2.28 | 0.89 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=LINKUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 899 h since 2026-08-26 | +0.0100% | 1.86 | 0.92 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **XRP**, **ZEC**, **SUI**, **BNB**
- **Research only** - backtested, never a signal: AVAX, LINK, UNI

| Not eligible | 24h volume | Why |
|---|---|---|
| QNT | $80M | order book too thin: $101k within 1% (need $250k) |
| SAND | $68M | 7-day average volume $10M < $50M; 24h move +56.5% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $21k within 1% (need $250k) |
| ADA | $61M | 7-day average volume $43M < $50M |
| PUMP | $58M | order book too thin: $181k within 1% (need $250k) |
| AAVE | $58M | 7-day average volume $38M < $50M; order book too thin: $240k within 1% (need $250k) |

**Flags (not excluded):** QNT: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, PEPE, RLUSD, TAO, USD1, USDC, WLD (see `config.yaml`)

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
| SUI | 178 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| BNB | 464 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| AVAX | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| LINK | 402 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-01 | OK (300 candles) |
| UNI | 315 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (HH/LL) | 87,220 / 83,888 | 0.89 | 0.26x | 1.01x | bull_engulf, bull_reject |
| ETH | down (LH/LL) | 2,769.68 / 2,650.88 | 0.85 | 0.34x | 0.95x | - |
| SOL | down (LH/LL) | 123.37 / 117.11 | 0.69 | 0.39x | 0.92x | - |
| XRP | mixed (HH/LL) | 1.555 / 1.4458 | 0.72 | 0.29x | 0.95x | retest_down |
| ZEC | mixed (HH/LL) | 1,412.12 / 1,271.09 | 0.69 | 0.73x | 0.99x | bull_reject |
| SUI | down (LH/LL) | 1.215 / 1.1032 | 0.92 | 1.66x | 1.02x | displacement_up, bull_reject, retest_down |
| BNB | mixed (HH/LL) | 784.46 / 760.35 | 0.95 | 0.51x | 0.90x | retest_down |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 467 | 48% | 34% | 27% | 80% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | displacement_down | 384 | 51% | 32% | 21% | 75% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1227 | 44% | 31% | 22% | 77% | 43% | 30% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1369 | 43% | 28% | 19% | 78% | 47% | 31% | worse than chance | 0.08R |
| 4h | bull_reject | 940 | 42% | 29% | 20% | 78% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | bear_reject | 856 | 47% | 32% | 22% | 74% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 647 | 44% | 30% | 22% | 76% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 681 | 45% | 30% | 20% | 78% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 280 | 46% | 28% | 21% | 82% | 44% | 30% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 247 | 49% | 35% | 24% | 71% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 94 | 53% | 35% | 26% | 82% | 46% | 31% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 91 | 42% | 23% | 13% | 78% | 49% | 33% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 652 | 44% | 28% | 21% | 78% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | smc_fvg_retrace_bear | 686 | 46% | 30% | 19% | 76% | 47% | 31% | can't tell from chance | 0.08R |
| 1h | displacement_up | 626 | 43% | 33% | 26% | 74% | 43% | 30% | can't tell from chance | 0.28R |
| 1h | displacement_down | 435 | 37% | 24% | 15% | 82% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | bull_engulf | 1723 | 40% | 28% | 22% | 75% | 42% | 29% | can't tell from chance | 0.32R |
| 1h | bear_engulf | 1873 | 38% | 24% | 17% | 80% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | bull_reject | 1393 | 40% | 28% | 21% | 75% | 42% | 30% | can't tell from chance | 0.31R |
| 1h | bear_reject | 1338 | 36% | 23% | 17% | 81% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_sweep_bull | 650 | 41% | 27% | 20% | 76% | 43% | 30% | can't tell from chance | 0.30R |
| 1h | smc_sweep_bear | 714 | 38% | 24% | 15% | 81% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 413 | 40% | 29% | 23% | 79% | 43% | 30% | can't tell from chance | 0.27R |
| 1h | smc_bos_down | 273 | 38% | 27% | 18% | 83% | 39% | 26% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 119 | 47% | 35% | 30% | 72% | 39% | 28% | can't tell from chance | 0.32R |
| 1h | smc_choch_down | 120 | 41% | 30% | 21% | 75% | 39% | 25% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 912 | 46% | 33% | 24% | 71% | 42% | 29% | can't tell from chance | 0.30R |
| 1h | smc_fvg_retrace_bear | 794 | 40% | 27% | 19% | 79% | 38% | 24% | can't tell from chance | 0.20R |
| 30m | displacement_up | 541 | 36% | 25% | 21% | 80% | 40% | 27% | worse than chance | 0.32R |
| 30m | displacement_down | 451 | 41% | 25% | 16% | 80% | 37% | 22% | can't tell from chance | 0.19R |
| 30m | bull_engulf | 1702 | 40% | 27% | 19% | 77% | 40% | 27% | can't tell from chance | 0.35R |
| 30m | bear_engulf | 1836 | 38% | 24% | 17% | 80% | 38% | 23% | can't tell from chance | 0.21R |
| 30m | bull_reject | 1354 | 43% | 28% | 20% | 76% | 40% | 27% | can't tell from chance | 0.35R |
| 30m | bear_reject | 1458 | 38% | 24% | 17% | 80% | 37% | 23% | can't tell from chance | 0.21R |
| 30m | smc_sweep_bull | 677 | 39% | 27% | 18% | 76% | 40% | 27% | can't tell from chance | 0.35R |
| 30m | smc_sweep_bear | 634 | 43% | 27% | 18% | 80% | 38% | 24% | beats chance | 0.20R |
| 30m | smc_bos_up | 403 | 35% | 27% | 22% | 80% | 41% | 28% | worse than chance | 0.33R |
| 30m | smc_bos_down | 272 | 33% | 21% | 12% | 86% | 38% | 23% | can't tell from chance | 0.22R |
| 30m | smc_choch_up | 104 | 36% | 21% | 15% | 85% | 41% | 27% | can't tell from chance | 0.37R |
| 30m | smc_choch_down | 104 | 40% | 26% | 20% | 78% | 38% | 22% | can't tell from chance | 0.20R |
| 30m | smc_fvg_retrace_bull | 977 | 39% | 26% | 19% | 78% | 40% | 27% | can't tell from chance | 0.35R |
| 30m | smc_fvg_retrace_bear | 809 | 39% | 23% | 16% | 80% | 37% | 23% | can't tell from chance | 0.23R |
| 15m | displacement_up | 488 | 37% | 27% | 21% | 82% | 35% | 25% | can't tell from chance | 0.44R |
| 15m | displacement_down | 439 | 33% | 23% | 13% | 84% | 36% | 22% | can't tell from chance | 0.28R |
| 15m | bull_engulf | 1672 | 36% | 26% | 18% | 80% | 35% | 25% | can't tell from chance | 0.49R |
| 15m | bear_engulf | 1627 | 35% | 22% | 15% | 79% | 36% | 22% | can't tell from chance | 0.29R |
| 15m | bull_reject | 1294 | 37% | 28% | 19% | 79% | 34% | 25% | beats chance | 0.48R |
| 15m | bear_reject | 1500 | 35% | 22% | 14% | 83% | 36% | 22% | can't tell from chance | 0.29R |
| 15m | smc_sweep_bull | 635 | 36% | 27% | 20% | 77% | 34% | 25% | can't tell from chance | 0.45R |
| 15m | smc_sweep_bear | 610 | 35% | 23% | 13% | 85% | 37% | 23% | can't tell from chance | 0.28R |
| 15m | smc_bos_up | 379 | 39% | 28% | 22% | 80% | 33% | 24% | can't tell from chance | 0.47R |
| 15m | smc_bos_down | 321 | 33% | 19% | 13% | 86% | 36% | 22% | can't tell from chance | 0.29R |
| 15m | smc_choch_up | 85 | 32% | 19% | 12% | 87% | 31% | 21% | can't tell from chance | 0.46R |
| 15m | smc_choch_down | 86 | 30% | 21% | 15% | 83% | 34% | 21% | can't tell from chance | 0.31R |
| 15m | smc_fvg_retrace_bull | 1115 | 35% | 25% | 17% | 79% | 34% | 25% | can't tell from chance | 0.48R |
| 15m | smc_fvg_retrace_bear | 938 | 35% | 23% | 15% | 81% | 36% | 22% | can't tell from chance | 0.30R |
| 5m | displacement_up | 1257 | 32% | 22% | 18% | 84% | 29% | 20% | beats chance | 0.80R |
| 5m | displacement_down | 1123 | 26% | 17% | 11% | 87% | 31% | 20% | worse than chance | 0.45R |
| 5m | bull_engulf | 4342 | 27% | 19% | 14% | 82% | 29% | 20% | worse than chance | 0.83R |
| 5m | bear_engulf | 4210 | 30% | 20% | 12% | 83% | 31% | 20% | can't tell from chance | 0.50R |
| 5m | bull_reject | 3204 | 28% | 20% | 15% | 80% | 28% | 20% | can't tell from chance | 0.86R |
| 5m | bear_reject | 3662 | 33% | 21% | 14% | 82% | 31% | 20% | beats chance | 0.49R |
| 5m | smc_sweep_bull | 1266 | 29% | 20% | 14% | 80% | 30% | 21% | can't tell from chance | 0.73R |
| 5m | smc_sweep_bear | 1281 | 34% | 24% | 15% | 81% | 32% | 21% | can't tell from chance | 0.45R |
| 5m | smc_bos_up | 847 | 31% | 23% | 19% | 83% | 29% | 21% | can't tell from chance | 0.83R |
| 5m | smc_bos_down | 862 | 28% | 18% | 11% | 87% | 31% | 21% | worse than chance | 0.50R |
| 5m | smc_choch_up | 217 | 33% | 24% | 19% | 86% | 29% | 20% | can't tell from chance | 0.90R |
| 5m | smc_choch_down | 217 | 23% | 13% | 8% | 88% | 31% | 19% | worse than chance | 0.51R |
| 5m | smc_fvg_retrace_bull | 3384 | 31% | 22% | 16% | 79% | 28% | 20% | beats chance | 0.86R |
| 5m | smc_fvg_retrace_bear | 2948 | 28% | 18% | 12% | 84% | 30% | 20% | worse than chance | 0.51R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (moderate) | STRONG_BULL (strong) | WEAK_BULL (moderate) | TRANSITION (weak) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (strong) | UNCLEAR (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H UNCLEAR)) |
| **SOL** | TRANSITION (weak) | STRONG_BULL (strong) | UNCLEAR (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H UNCLEAR)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | UNCLEAR (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H TRANSITION)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H TRANSITION)) |
| **SUI** | UNCLEAR (weak) | WEAK_BULL (weak) | UNCLEAR (weak) | EXPANSION up (weak) | LONG allowed (1D/1H bullish, 1W UNCLEAR) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (strong) | RANGE (moderate) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H UNCLEAR)) |
| **AVAX** | TRANSITION (weak) | WEAK_BULL (weak) | RANGE (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H UNCLEAR)) |
| **LINK** | WEAK_BULL (moderate) | WEAK_BULL (weak) | UNCLEAR (weak) | WEAK_BEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H UNCLEAR, 1H WEAK_BEAR)) |
| **UNI** | EXPANSION up (moderate) | WEAK_BULL (weak) | COMPRESSION (moderate) | RANGE (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H COMPRESSION, 1H RANGE)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (moderate)** - for: EMA-fast rising (+1.5 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.73x normal, Bollinger width above 56% of the last 100 candles · against: EMAs not lined up
- **1D STRONG_BULL (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.2 ATR in 10 candles); swing structure up (HH/HL); ADX 42 = strong trend; candle size 1.06x normal, Bollinger width above 76% of the last 100 candles; volume 1.19x normal · against: -
- **4H WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; swing structure up (HH/HL); ADX 28 = strong trend; candle size 1.12x normal, Bollinger width above 41% of the last 100 candles; volume 1.64x normal · against: EMA-fast flat (+0.5 ATR in 10 candles) (neutral)
- **1H TRANSITION (weak)** - for: ADX 26 = strong trend; candle size 1.01x normal, Bollinger width above 99% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.2 ATR in 10 candles); swing structure mixed; ADX 26 is close to a threshold

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **Asia**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (BOS 26 candles ago) | sell-side (bullish idea) 31 candles ago | bull 84,571.03-84,630.90 | bear 86,133.40-86,975.51 | discount (23%) | PDH 87,220.00 (5.4 ATR) | swing low 83,888.00 (1.63 ATR) |
| **ETH** | down (CHOCH 26 candles ago) | sell-side (bullish idea) 26 candles ago | bull 2,673.28-2,674.73 (retraced) | bull 2,652.20-2,695.38 | discount (22%) | swing high 2,769.68 (5.2 ATR) | equal lows 2,650.88 (1.45 ATR) |
| **SOL** | up (BOS 10 candles ago) | sell-side (bullish idea) 26 candles ago | bull 118.77-119.01 (retraced) | bull 115.86-117.34 | discount (31%) | swing high 123.37 (4.07 ATR) | swing low 117.11 (1.8 ATR) |
| **XRP** | down (CHOCH 43 candles ago) | sell-side (bullish idea) 26 candles ago | bull 1.4858-1.4888 (retraced) | bull 1.3773-1.3856 | discount (40%) | swing high 1.5550 (4.55 ATR) | swing low 1.4458 (2.99 ATR) |
| **ZEC** | down (CHOCH 27 candles ago) | buy-side (bearish idea) 8 candles ago | bull 1,305.44-1,314.05 | bear 1,397.89-1,447.60 | discount (35%) | swing high 1,412.12 (3.45 ATR) | swing low 1,271.09 (1.89 ATR) |
| **SUI** | up (BOS 7 candles ago) | sell-side (bullish idea) 25 candles ago | bull 1.1613-1.1751 | bull 1.0050-1.0598 | premium (75%) | swing high 1.2150 (1.24 ATR) | swing low 1.1032 (3.67 ATR) |
| **BNB** | up (BOS 7 candles ago) | buy-side (bearish idea) 10 candles ago | bull 767.07-767.76 | bear 774.08-780.19 | discount (37%) | PDH 784.46 (3.82 ATR) | swing low 760.35 (2.27 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 67 (Greed), yesterday 72  (extreme fear/greed = bigger, faster moves)

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
- **Event calendar (next 7 days):** none listed
- ⚠️ **calendar not maintained - no event listed for the next 7 days (events.yaml)**

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-10-03 00:53 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1128 | 38.9 | +0.164 | 1.3 | 34.8R | +0.15 / +0.19 | +0.20 / +0.13 | 5/5 | +0.13 | +0.11 | stable | 8 | 0.04R | 16, +0.25 (+0.43 / -1.07) | 93 / 54 of 269 | 0 | max drawdown 34.8R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1279 | 38.4 | +0.164 | 1.29 | 36.3R | +0.16 / +0.18 | +0.18 / +0.15 | 5/5 | +0.14 | +0.11 | stable | 9 | 0.04R | 17, +0.24 (+0.42 / -1.07) | 160 / 67 of 362 | 0 | max drawdown 36.3R |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1128 | 38.9 | +0.164 | 1.3 | 34.8R | +0.15 / +0.19 | +0.20 / +0.13 | 5/5 | +0.13 | +0.11 | stable | 8 | 0.04R | 16, +0.25 (+0.43 / -1.07) | 93 / 54 of 269 | 0 | max drawdown 34.8R |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1159 | 52.9 | +0.077 | 1.17 | 26.9R | +0.07 / +0.09 | +0.07 / +0.09 | 3/5 | +0.05 | +0.03 | stable | 6 | 0.04R | 18, -0.01 (+0.12 / -1.07) | 93 / 54 of 269 | 0 | avg +0.08R/trade (needs +0.10R); profit factor 1.17; max drawdown 26.9R |
| macd_trend_cross | 1.0 | 1h | **BACKTESTING** | 205 | 53.7 | +0.041 | 1.08 | 25.0R | -0.08 / +0.31 | -0.06 / +0.13 | 2/5 ✗ | -0.01 | -0.08 | ✗  stop atr 1.5→1.2: -0.02R | 5 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 218 / 4 of 225 | 0 | avg +0.04R/trade (needs +0.10R); profit factor 1.08; max drawdown 25.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.54 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.79 (+1.79 / +0.00) | 31 / 109 of 152 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 14 | 35.7 | +0.023 | 1.04 | 2.7R | +0.08 / -0.18 | -0.76 / +0.15 | 1/5 ✗ | -0.05 | +0.10 | ✗  stop max_width_atr 3.0→2.4: -0.32R | 0 | 0.10R | 0, +0.00 (+0.00 / +0.00) | 532 / 201 of 869 | 0 | only 14 trades; avg +0.02R/trade (needs +0.10R); profit factor 1.04; only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 6 / 5 of 11 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 67 / 14 of 84 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 48 / 11 of 65 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 6 / 5 of 11 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 15 / 7 of 23 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 3 | 33.3 | -0.018 | 0.98 | 2.3R | -1.13 / +2.21 | +2.21 / -1.13 | 0/5 ✗ | -0.10 | -0.17 | ✗  sweep_bars 8→10: -0.33R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 15 / 7 of 23 | 0 | only 3 trades; avg -0.02R/trade (needs +0.10R); profit factor 0.98; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 12 | 50.0 | -0.102 | 0.81 | 3.7R | -0.13 / +0.05 | -0.31 / +0.00 | 0/5 ✗ | -0.04 | -0.24 | ✗  time_stop_bars 30→24: -0.16R | 0 | 0.17R | 0, +0.00 (+0.00 / +0.00) | 492 / 199 of 841 | 0 | only 12 trades; avg -0.10R/trade (needs +0.10R); profit factor 0.81; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 14 | 35.7 | -0.358 | 0.63 | 9.7R | -0.87 / +0.56 | -0.09 / -0.63 | 0/5 ✗ | -0.76 | -0.95 | ✗  sweep_bars 8→10: -0.56R | 0 | 0.57R | 2, +0.31 (+0.31 / +0.00) | 55 / 21 of 85 | 0 | not cost-viable: fees + slippage 0.57R per trade (stop must be ≥ 4x the round-trip cost); only 14 trades; avg -0.36R/trade (needs +0.10R); profit factor 0.63; only 5 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 4 | 25.0 | -0.845 | 0.41 | 3.4R | -0.69 / -1.32 | -1.32 / -0.69 | 0/5 ✗ | -3.93 | -2.71 | ✗  stop buffer_atr 0.2→0.24: -3.68R | 0 | 0.33R | 1, -1.32 (-1.32 / +0.00) | 48 / 11 of 65 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); only 4 trades; avg -0.85R/trade (needs +0.10R); profit factor 0.41; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 5 | 0.0 | -1.187 | 0.0 | 5.9R | -1.19 / -1.16 | -1.42 / -1.13 | 0/5 ✗ | -1.19 | -1.25 | ✗  stop max_width_atr 3.0→2.4: -1.22R | 0 | 0.19R | 0, +0.00 (+0.00 / +0.00) | 67 / 14 of 84 | 0 | only 5 trades; avg -1.19R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL-S4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 17, +0.24 (+0.42 / -1.07) | 160 / 67 of 362 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT-VRVOL-S4 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 32, +0.27 (+0.46 / -0.74) | 210 / 121 of 545 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT-VRVOL-S4 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 52, +0.02 (+0.01 / +0.09) | 239 / 62 of 495 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 295 | 50.2 | -0.021 | 0.96 | 30.4R | +0.09 / -0.25 | +0.03 / -0.07 | 2/5 ✗ | -0.07 | -0.11 | ✗  rank_n 100→120: -0.03R | 5 | 0.07R | 2, +0.11 (+0.11 / +0.00) | 108 / 22 of 145 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 30.4R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 879 | 51.4 | -0.042 | 0.92 | 62.9R | -0.03 / -0.06 | -0.07 / -0.01 | 0/5 ✗ | -0.13 | -0.20 | ✗  stop atr 1.5→1.2: -0.07R | 3 | 0.14R | 7, +0.28 (+0.27 / +0.29) | 149 / 34 of 221 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.92; max drawdown 62.9R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1277 | 33.5 | -0.056 | 0.92 | 129.6R | -0.08 / +0.00 | +0.01 / -0.13 | 1/5 ✗ | -0.13 | -0.20 | ✗  stop atr 2.0→1.6: -0.13R | 3 | 0.13R | 45, -0.02 (+0.04 / -0.46) | 149 / 38 of 356 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.92; max drawdown 129.6R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FAILED** | 1277 | 33.5 | -0.056 | 0.92 | 129.6R | -0.08 / +0.00 | +0.01 / -0.13 | 1/5 ✗ | -0.13 | -0.20 | ✗  stop atr 2.0→1.6: -0.13R | 3 | 0.13R | 45, -0.02 (+0.04 / -0.46) | 149 / 38 of 356 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.92; max drawdown 129.6R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 3487 | 32.1 | -0.060 | 0.9 | 286.0R | -0.09 / -0.01 | -0.04 / -0.09 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.09R | 32, +0.27 (+0.46 / -0.74) | 210 / 121 of 545 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.90; max drawdown 286.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 3066 | 31.9 | -0.062 | 0.9 | 275.0R | -0.10 / +0.02 | -0.04 / -0.09 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.10R | 2 | 0.09R | 29, +0.23 (+0.38 / -1.06) | 123 / 85 of 388 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.90; max drawdown 275.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FAILED** | 3066 | 31.9 | -0.062 | 0.9 | 275.0R | -0.10 / +0.02 | -0.04 / -0.09 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.10R | 2 | 0.09R | 29, +0.23 (+0.38 / -1.06) | 123 / 85 of 388 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.90; max drawdown 275.0R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 3154 | 47.9 | -0.065 | 0.88 | 242.3R | -0.09 / -0.02 | -0.06 / -0.07 | 0/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.09R | 1 | 0.09R | 30, +0.28 (+0.38 / -0.68) | 123 / 85 of 388 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 242.3R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1288 | 48.4 | -0.069 | 0.87 | 140.1R | -0.01 / -0.19 | -0.00 / -0.15 | 2/5 ✗ | -0.11 | -0.14 | ✗  long_rsi_hi 65→52: -0.15R | 2 | 0.06R | 17, -0.09 (+0.02 / -0.20) | 671 / 197 of 1045 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; max drawdown 140.1R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 39 | 51.3 | -0.073 | 0.86 | 6.0R | +0.12 / -0.45 | +0.31 / -0.47 | 2/5 ✗ | -0.10 | -0.14 | ✗  stop atr 1.5→1.8: -0.09R | 2 | 0.06R | 1, +0.24 (+0.00 / +0.24) | 168 / 5 of 176 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.86; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1507 | 32.9 | -0.077 | 0.88 | 158.5R | -0.10 / -0.03 | -0.01 / -0.15 | 1/5 ✗ | -0.16 | -0.24 | ✗  stop atr 2.0→1.6: -0.15R | 2 | 0.13R | 52, +0.02 (+0.01 / +0.09) | 239 / 62 of 495 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.88; max drawdown 158.5R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1310 | 48.8 | -0.081 | 0.85 | 133.9R | -0.09 / -0.06 | -0.06 / -0.11 | 0/5 ✗ | -0.15 | -0.23 | ✗  stop atr 2.0→1.6: -0.15R | 2 | 0.13R | 45, +0.01 (+0.07 / -0.46) | 149 / 38 of 356 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.85; max drawdown 133.9R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 96 | 45.8 | -0.091 | 0.84 | 19.2R | +0.10 / -0.42 | -0.16 / +0.00 | 3/5 ✗ | -0.12 | -0.14 | ✗  st_n 10→8: -0.09R | 1 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 41 / 6 of 50 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.84; max drawdown 19.2R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1948 | 56.6 | -0.099 | 0.65 | 193.0R | -0.09 / -0.12 | -0.11 / -0.09 | 0/5 ✗ | -0.13 | -0.16 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.05R | 3, -0.01 (+0.00 / -0.01) | 732 / 3 of 995 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.65; max drawdown 193.0R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 7240 | 53.9 | -0.129 | 0.54 | 945.1R | -0.11 / -0.17 | -0.14 / -0.12 | 0/5 ✗ | -0.19 | -0.26 | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 45, -0.10 (-0.16 / +0.04) | 1050 / 9 of 1398 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.54; max drawdown 945.1R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6561 | 47.4 | -0.135 | 0.76 | 898.2R | -0.14 / -0.13 | -0.17 / -0.10 | 0/5 ✗ | -0.20 | -0.28 | ✗  stop atr 1.5→1.2: -0.17R | 0 | 0.13R | 54, -0.08 (-0.11 / +0.16) | 1152 / 289 of 1829 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 898.2R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 86 | 34.9 | -0.145 | 0.79 | 25.2R | -0.35 / +0.56 | -0.06 / -0.20 | 2/5 ✗ | -0.21 | -0.32 | ✗  depth 0.985→1.182: -0.45R | 2 | 0.16R | 4, +0.01 (+0.00 / +0.01) | 35 / 6 of 45 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.79; max drawdown 25.2R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 364 | 44.5 | -0.146 | 0.74 | 60.8R | -0.14 / -0.15 | -0.21 / -0.08 | 1/5 ✗ | -0.21 | -0.28 | ✗  slow 21→17: -0.21R | 2 | 0.12R | 3, -1.00 (-1.00 / +0.00) | 144 / 9 of 161 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.74; max drawdown 60.8R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 218 | 39.9 | -0.150 | 0.77 | 61.2R | -0.22 / +0.12 | +0.15 / -0.35 | 1/5 ✗ | -0.21 | -0.27 | ✗  depth 0.985→1.182: -0.29R | 1 | 0.12R | 7, +0.70 (+0.53 / +0.93) | 77 / 8 of 94 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.77; max drawdown 61.2R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 166 | 46.4 | -0.175 | 0.7 | 31.0R | -0.19 / -0.13 | -0.23 / -0.14 | 1/5 ✗ | -0.24 | -0.33 | ✗  stop atr 2.0→1.6: -0.21R | 2 | 0.13R | 7, -0.39 (-0.07 / -1.18) | 55 / 5 of 71 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.70; max drawdown 31.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 314 | 31.8 | -0.186 | 0.77 | 79.4R | -0.09 / -0.39 | -0.32 / -0.04 | 1/5 ✗ | -0.29 | -0.39 | ✗  time_stop_bars 30→36: -0.20R | 1 | 0.20R | 5, +0.69 (+1.94 / -0.14) | 81 / 230 of 323 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.77; max drawdown 79.4R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 449 | 43.9 | -0.197 | 0.68 | 89.4R | -0.19 / -0.21 | -0.28 / -0.15 | 0/5 ✗ | -0.34 | -0.48 | ✗  stop atr 1.5→1.2: -0.32R | 1 | 0.26R | 21, -0.33 (-0.31 / -0.75) | 80 / 13 of 115 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 89.4R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2811 | 46.4 | -0.199 | 0.39 | 565.0R | -0.17 / -0.26 | -0.24 / -0.16 | 0/5 ✗ | -0.30 | -0.41 | ✗  stop atr 2.0→1.6: -0.25R | 0 | 0.17R | 44, -0.18 (+0.02 / -0.47) | 1084 / 36 of 1297 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.39; max drawdown 565.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 293 | 45.4 | -0.199 | 0.66 | 63.3R | -0.20 / -0.19 | -0.32 / -0.09 | 0/5 ✗ | -0.26 | -0.31 | ✗  stop atr 2.0→1.6: -0.23R | 2 | 0.09R | 5, +0.39 (+0.39 / +0.00) | 56 / 4 of 68 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.66; max drawdown 63.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 315 | 47.3 | -0.201 | 0.67 | 63.8R | -0.18 / -0.24 | -0.26 / -0.12 | 0/5 ✗ | -0.29 | -0.38 | ✗  vol_x 1.2→1.44: -0.32R | 2 | 0.17R | 7, -0.43 (-0.41 / -0.47) | 100 / 195 of 306 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.67; max drawdown 63.8R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 301 | 46.8 | -0.205 | 0.67 | 70.9R | -0.14 / -0.40 | -0.32 / -0.10 | 0/5 ✗ | -0.33 | -0.43 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.20R | 5, -0.45 (-0.78 / +0.05) | 166 / 10 of 188 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.67; max drawdown 70.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3516 | 45.8 | -0.206 | 0.67 | 724.2R | -0.18 / -0.26 | -0.23 / -0.18 | 0/5 ✗ | -0.32 | -0.43 | ✗  stop atr 1.5→1.2: -0.26R | 0 | 0.19R | 112, -0.24 (-0.18 / -0.58) | 848 / 254 of 1651 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.67; max drawdown 724.2R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 866 | 30.8 | -0.209 | 0.75 | 196.1R | -0.18 / -0.26 | -0.26 / -0.16 | 1/5 ✗ | -0.31 | -0.41 | ✗  stop buffer_atr 0.2→0.16: -0.26R | 1 | 0.21R | 19, -0.23 (+0.19 / -0.70) | 449 / 1142 of 1687 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.75; max drawdown 196.1R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 496 | 45.2 | -0.235 | 0.64 | 118.2R | -0.26 / -0.17 | -0.25 / -0.22 | 1/5 ✗ | -0.34 | -0.47 | ✗  stop atr 1.5→1.2: -0.32R | 1 | 0.20R | 21, -0.35 (-0.41 / -0.04) | 115 / 36 of 198 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.64; max drawdown 118.2R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 3060 | 44.8 | -0.261 | 0.61 | 800.2R | -0.24 / -0.31 | -0.29 / -0.24 | 0/5 ✗ | -0.42 | -0.58 | ✗  stop atr 1.5→1.2: -0.35R | 0 | 0.27R | 201, -0.23 (-0.24 / -0.14) | 1385 / 216 of 2331 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 800.2R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 346 | 38.2 | -0.272 | 0.56 | 97.9R | -0.23 / -0.41 | -0.36 / -0.21 | 0/5 ✗ | -0.37 | -0.47 | ✗  slow 21→25: -0.35R | 0 | 0.17R | 11, +0.16 (+0.20 / -0.03) | 117 / 19 of 154 | 0 | avg -0.27R/trade (needs +0.10R); profit factor 0.56; max drawdown 97.9R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1515 | 31.9 | -0.305 | 0.62 | 467.2R | -0.32 / -0.27 | -0.31 / -0.30 | 0/5 ✗ | -0.43 | -0.56 | ✗  stop atr 1.5→1.2: -0.37R | 0 | 0.21R | 26, -0.06 (+0.26 / -0.39) | 626 / 36 of 770 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.62; max drawdown 467.2R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1287 | 29.1 | -0.318 | 0.6 | 411.5R | -0.35 / -0.24 | -0.30 / -0.33 | 0/5 ✗ | -0.40 | -0.47 | ✗  rsi_n 14→17: -0.41R | 1 | 0.14R | 5, +0.13 (-0.04 / +0.38) | 750 / 9 of 805 | 0 | avg -0.32R/trade (needs +0.10R); profit factor 0.60; max drawdown 411.5R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 39 | 33.3 | -0.337 | 0.55 | 14.0R | -0.11 / -0.66 | -0.59 / -0.07 | 0/5 ✗ | -0.50 | -0.64 | ✗  time_stop_bars 30→24: -0.41R | 2 | 0.17R | 6, -0.79 (-0.79 / +0.00) | 102 / 35 of 151 | 0 | avg -0.34R/trade (needs +0.10R); profit factor 0.55; max drawdown 14.0R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 2192 | 33.3 | -0.343 | 0.2 | 753.1R | -0.33 / -0.37 | -0.43 / -0.27 | 0/5 ✗ | -0.51 | -0.69 | ✗  hi 90→108: -0.43R | 0 | 0.29R | 90, -0.35 (-0.28 / -0.39) | 1264 / 49 of 1472 | 0 | not cost-viable: fees + slippage 0.29R per trade (stop must be ≥ 4x the round-trip cost); avg -0.34R/trade (needs +0.10R); profit factor 0.20; max drawdown 753.1R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 549 | 41.0 | -0.384 | 0.48 | 213.8R | -0.38 / -0.41 | -0.37 / -0.39 | 0/5 ✗ | -0.55 | -0.70 | ✗  stop atr 1.5→1.2: -0.46R | 0 | 0.31R | 40, -0.64 (-0.67 / -0.33) | 93 / 32 of 178 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); avg -0.38R/trade (needs +0.10R); profit factor 0.48; max drawdown 213.8R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 622 | 25.7 | -0.422 | 0.56 | 269.7R | -0.44 / -0.36 | -0.55 / -0.31 | 0/5 ✗ | -0.59 | -0.72 | ✗  n 20→24: -0.46R | 1 | 0.33R | 28, +0.12 (+0.40 / -0.25) | 481 / 1087 of 1764 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); avg -0.42R/trade (needs +0.10R); profit factor 0.56; max drawdown 269.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 343 | 38.8 | -0.449 | 0.4 | 153.9R | -0.40 / -0.60 | -0.47 / -0.43 | 0/5 ✗ | -0.60 | -0.76 | ✗  stop atr 1.0→0.8: -0.53R | 0 | 0.28R | 16, -0.90 (-0.70 / -1.24) | 116 / 221 of 364 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.45R/trade (needs +0.10R); profit factor 0.40; max drawdown 153.9R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 575 | 39.1 | -0.487 | 0.38 | 282.4R | -0.43 / -0.65 | -0.61 / -0.42 | 0/5 ✗ | -0.69 | -0.94 | ✗  stop atr 1.0→0.8: -0.55R | 0 | 0.38R | 42, -0.71 (-0.62 / -0.97) | 106 / 253 of 402 | 0 | not cost-viable: fees + slippage 0.38R per trade (stop must be ≥ 4x the round-trip cost); avg -0.49R/trade (needs +0.10R); profit factor 0.38; max drawdown 282.4R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 120 | 20.8 | -0.499 | 0.49 | 62.2R | -0.42 / -0.66 | -0.63 / -0.37 | 1/5 ✗ | -0.62 | -0.75 | ✗  stop max_width_atr 3.0→2.4: -0.50R | 1 | 0.26R | 5, +0.20 (+2.42 / -1.29) | 31 / 109 of 152 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.50R/trade (needs +0.10R); profit factor 0.49; max drawdown 62.2R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 286 | 29.4 | -0.738 | 0.25 | 212.0R | -0.87 / -0.55 | -0.69 / -1.05 | 0/5 ✗ | -1.13 | -1.50 | ✗  stop atr 1.5→1.2: -0.96R | 0 | 0.61R | 81, -0.56 (-0.55 / -0.70) | 193 / 48 of 327 | 0 | not cost-viable: fees + slippage 0.61R per trade (stop must be ≥ 4x the round-trip cost); avg -0.74R/trade (needs +0.10R); profit factor 0.25; max drawdown 212.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 481 | 24.7 | -1.156 | 0.15 | 556.9R | -1.20 / -1.10 | -1.06 / -1.94 | 0/5 ✗ | -1.80 | -2.45 | ✗  stop atr 1.0→0.8: -1.48R | 0 | 1.04R | 157, -1.15 (-1.18 / -0.97) | 222 / 666 of 1049 | 0 | not cost-viable: fees + slippage 1.04R per trade (stop must be ≥ 4x the round-trip cost); avg -1.16R/trade (needs +0.10R); profit factor 0.15; max drawdown 556.9R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **25** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 118 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.34** (Bonferroni: family-wise false-winner rate 0.05 over 118 trials; with 1 trial it would be 1.65).

**Research run duration:** 8.4 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 25 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (85.3 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 36 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: donchian_breakout-VEXIT-VRVOL-S4.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

0 of 59 strategy / timeframe tests would get a different verdict.

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (80% of 3,487 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (76% of 1,507 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (81% of 1,279 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 3,066 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (96% of 1,277 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 1,128 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 3,066 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (96% of 1,277 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 1,128 trades shared)

🧪 **Strategy lab:** 6 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S8-PDH-PDL-SWEEP-5M | 30m | 2 | +0.037 | +0.037 | -0.605 | -0.551 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.337 | -0.662 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +2.214 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET | 15m | 3 | -0.018 | +2.214 | -0.358 | +0.561 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 4 | -0.845 | -1.323 | -0.102 | +0.049 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 5 | -1.187 | -1.163 | +0.023 | -0.179 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 314 | -0.186 | -0.392 | -0.209 | -0.255 | no |
| S8-PDH-PDL-SWEEP | 30m | 120 | -0.499 | -0.659 | -0.422 | -0.360 | no |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): macd_trend_cross@1.0 1h FAILED → BACKTESTING

### 3c. Research layers (daily run)
Last run: **2026-10-03 00:53 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 10 | 2017-08-17 | 2026-10-02 | 19987 |  |
| 1h | 10 | 2017-08-17 | 2026-10-02 | 79884 |  |
| 30m | 10 | 2024-10-03 | 2026-10-03 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 10 | 2025-10-03 | 2026-10-03 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 10 | 2026-07-05 | 2026-10-03 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 1128 (689) | false_breakout, trend_reversal | false_breakout 64%, no_displacement 32% | +0.47R | -0.37R | +0.22 / +0.16 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 1279 (788) | false_breakout, trend_reversal | false_breakout 63%, no_displacement 33% | +0.48R | -0.36R | +0.22 / +0.16 |
| donchian_breakout-VEXIT-VRVOL | 4h | BACKTESTING | 1128 (689) | false_breakout, trend_reversal | false_breakout 64%, no_displacement 32% | +0.47R | -0.37R | +0.22 / +0.16 |
| donchian_breakout | 4h | BACKTESTING | 1159 (546) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 66%, stop_too_tight 35% | +0.36R | -0.37R | +0.13 / +0.08 |
| macd_trend_cross | 1h | BACKTESTING | 205 (95) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 92%, indicator_lag 40%, stop_too_tight 30% | +0.31R | -0.37R | +0.19 / +0.04 |
| bb_squeeze_breakout | 4h | FAILED | 295 (147) | false_breakout, stop_too_tight, structural_change | false_breakout 58%, stop_too_tight 44%, regime_mismatch 28% | +0.36R | -0.36R | +0.07 / -0.02 |
| bb_squeeze_breakout | 1h | FAILED | 879 (427) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 63%, no_displacement 53%, stop_too_tight 38%, regime_mismatch 35% | +0.36R | -0.44R | +0.13 / -0.04 |
| donchian_breakout-VEXIT | 30m | FAILED | 1277 (849) | false_breakout | false_breakout 72% | +0.45R | -0.39R | +0.10 / -0.06 |
| donchian_breakout-VEXIT-VRVOL | 30m | FAILED | 1277 (849) | false_breakout | false_breakout 72% | +0.45R | -0.39R | +0.10 / -0.06 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 3487 (2367) | htf_conflict, no_displacement, false_breakout, regime_mismatch | false_breakout 64% | +0.50R | -0.38R | +0.05 / -0.06 |
| donchian_breakout-VEXIT | 1h | FAILED | 3066 (2089) | no_displacement, false_breakout | false_breakout 63% | +0.51R | -0.39R | +0.04 / -0.06 |
| donchian_breakout-VEXIT-VRVOL | 1h | FAILED | 3066 (2089) | no_displacement, false_breakout | false_breakout 63% | +0.51R | -0.39R | +0.04 / -0.06 |
| donchian_breakout | 1h | FAILED | 3154 (1642) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 37%, stop_too_tight 31% | +0.36R | -0.39R | +0.04 / -0.07 |
| trend_pullback | 4h | FAILED | 1288 (664) | regime_mismatch, indicator_lag | regime_mismatch 81%, indicator_lag 38% | +0.36R | -0.42R | +0.01 / -0.07 |
| macd_trend_cross | 4h | FAILED | 39 (19) | structural_change | regime_mismatch 95%, no_displacement 90%, indicator_lag 58%, low_relative_volume 53% | +0.17R | -0.45R | +0.01 / -0.07 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1507 (1011) | range_market, false_breakout | false_breakout 72% | +0.45R | -0.40R | +0.09 / -0.08 |
| donchian_breakout | 30m | FAILED | 1310 (671) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 75%, stop_too_tight 34% | +0.29R | -0.40R | +0.08 / -0.08 |
| supertrend_flip | 4h | FAILED | 96 (52) | regime_mismatch, indicator_lag, structural_change | regime_mismatch 69%, indicator_lag 36% | +0.43R | -0.41R | -0.03 / -0.09 |
| rsi2_dip_buy | 4h | FAILED | 1948 (845) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 44% | +0.16R | -0.21R | -0.04 / -0.10 |
| rsi2_dip_buy | 1h | FAILED | 7240 (3341) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 42% | +0.16R | -0.20R | -0.00 / -0.13 |
| trend_pullback | 1h | FAILED | 6561 (3450) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 76%, indicator_lag 45%, stop_too_tight 28% | +0.29R | -0.42R | +0.02 / -0.14 |
| R4-CLUC | 15m | FAILED | 86 (56) | none | wrong_session 61% | +0.40R | -0.21R | +0.01 / -0.14 |
| ema_9_21_cross | 1h | FAILED | 364 (202) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 81%, indicator_lag 46%, stop_too_tight 27% | +0.29R | -0.37R | +0.00 / -0.15 |
| R4-CLUC | 30m | FAILED | 218 (131) | none | - | +0.32R | -0.49R | -0.03 / -0.15 |
| supertrend_flip | 30m | FAILED | 166 (89) | stop_too_tight, indicator_lag | regime_mismatch 43%, indicator_lag 43%, stop_too_tight 36%, late_entry 29% | +0.32R | -0.50R | -0.01 / -0.17 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 314 (214) | stop_too_tight, sweep_continued | sweep_continued 98%, range_market 56%, stop_too_tight 31% | +0.53R | -0.41R | +0.06 / -0.19 |
| ema_9_21_cross | 15m | FAILED | 449 (252) | htf_conflict, stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 29% | +0.28R | -0.42R | +0.12 / -0.20 |
| rsi2_dip_buy | 30m | FAILED | 2811 (1507) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 34% | +0.16R | -0.18R | +0.01 / -0.20 |
| supertrend_flip | 1h | FAILED | 293 (160) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 68%, stop_too_tight 35%, indicator_lag 34% | +0.38R | -0.38R | -0.09 / -0.20 |
| liquidity_sweep_reversal | 1h | FAILED | 315 (166) | stop_too_tight | stop_too_tight 54% | +0.28R | -0.47R | +0.00 / -0.20 |
| macd_trend_cross | 30m | FAILED | 301 (160) | overextended_entry, stop_too_tight, indicator_lag | no_displacement 87%, indicator_lag 44%, stop_too_tight 30% | +0.32R | -0.44R | +0.04 / -0.20 |
| trend_pullback | 30m | FAILED | 3516 (1905) | stop_too_tight, indicator_lag | indicator_lag 47%, stop_too_tight 30% | +0.27R | -0.43R | +0.03 / -0.21 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 866 (599) | stop_too_tight | range_market 47%, stop_too_tight 36% | +0.62R | -0.50R | +0.04 / -0.21 |
| bb_squeeze_breakout | 30m | FAILED | 496 (272) | false_breakout, stop_too_tight | false_breakout 63%, stop_too_tight 40% | +0.25R | -0.46R | +0.03 / -0.23 |
| trend_pullback | 15m | FAILED | 3060 (1688) | wrong_session, stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 31% | +0.25R | -0.44R | +0.07 / -0.26 |
| ema_9_21_cross | 30m | FAILED | 346 (214) | stop_too_tight, indicator_lag | indicator_lag 44%, low_relative_volume 40%, stop_too_tight 26% | +0.28R | -0.38R | -0.06 / -0.27 |
| R4-BBRSI | 30m | FAILED | 1515 (1031) | none | - | +0.42R | -0.44R | -0.04 / -0.30 |
| R4-BBRSI | 1h | FAILED | 1287 (913) | none | - | +0.45R | -0.45R | -0.15 / -0.32 |
| S6-OB-FVG-noSMC | 15m | FAILED | 39 (26) | none | - | +0.24R | -0.58R | -0.13 / -0.34 |
| rsi2_dip_buy | 15m | FAILED | 2192 (1462) | trend_reversal, fees_slippage | fees_slippage 45% | +0.17R | -0.18R | +0.00 / -0.34 |
| bb_squeeze_breakout | 15m | FAILED | 549 (324) | no_displacement, stop_too_tight | false_breakout 58%, no_displacement 57%, stop_too_tight 43% | +0.29R | -0.48R | -0.02 / -0.38 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 622 (462) | stop_too_tight | stop_too_tight 32% | +0.59R | -0.53R | -0.01 / -0.42 |
| liquidity_sweep_reversal | 30m | FAILED | 343 (210) | stop_too_tight | stop_too_tight 40%, range_market 34% | +0.34R | -0.47R | -0.13 / -0.45 |
| liquidity_sweep_reversal | 15m | FAILED | 575 (350) | stop_too_tight | stop_too_tight 37% | +0.39R | -0.47R | -0.01 / -0.49 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 120 (95) | low_relative_volume, trend_reversal, stop_too_tight, sweep_continued | sweep_continued 95%, stop_too_tight 25% | +0.52R | -0.63R | -0.16 / -0.50 |
| ema_9_21_cross | 5m | FAILED | 286 (202) | stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 32% | +0.24R | -0.43R | +0.01 / -0.74 |
| liquidity_sweep_reversal | 5m | FAILED | 481 (362) | htf_conflict, fees_slippage, stop_too_tight | stop_too_tight 38%, fees_slippage 26% | +0.32R | -0.48R | +0.16 / -1.16 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 26 strategy/timeframe tests); `false_breakout` (systematic in 15 strategy/timeframe tests); `regime_mismatch` (systematic in 13 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `trend_reversal` (systematic in 9 strategy/timeframe tests); `no_displacement` (systematic in 6 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `htf_conflict` (systematic in 3 strategy/timeframe tests); `fees_slippage` (systematic in 3 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- BTC down -2.9% (2026-10-02 12:00 → 2026-10-02 19:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- SOL up +5.4% (2026-10-01 16:00 → 2026-10-02 05:00 UTC): identifiable: at least one strategy had a valid signal before the move
- XRP down -4.8% (2026-10-02 09:00 → 2026-10-02 19:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- AVAX down -6.2% (2026-10-02 12:00 → 2026-10-02 21:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- LINK down -6.1% (2026-10-02 12:00 → 2026-10-02 21:00 UTC): not identifiable: no strategy had a setup before the move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 104.8 KB | - | - |
| `memory/cleanup_log.md` | 0.5 KB | - | - |
| `memory/coin_notes.md` | 6.8 KB | 7 | 2026-09-27 00:26 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 6.8 KB | 15 | 2026-10-02 04:20 UTC |
| `memory/experiments.md` | 48.1 KB | 19 | 2026-09-28 15:40 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 140.6 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 11.9 KB | - | - |
| `memory/missed_trades.md` | 21.3 KB | 29 | 2026-10-03 00:53 UTC |
| `memory/playbook.md` | 8.7 KB | - | - |
| `memory/research_sources.md` | 59.7 KB | 45 | 2026-09-28 15:40 UTC |
| `memory/smc_events.csv` | 662.7 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 16.4 KB | - | - |
| `memory/strategy_registry.csv` | 37.0 KB | - | - |
| `memory/trials.csv` | 9.2 KB | - | - |
| `memory/universe_log.md` | 18.2 KB | - | - |

**Reviews due** (review date passed; for the reviews): `missed_trades.md` LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00 (2026-10-02); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03); `missed_trades.md` SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells (2026-10-03); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03)
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*