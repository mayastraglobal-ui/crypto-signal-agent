# Crypto Signal Report

**Updated:** 2026-10-03 05:19 Beijing time (2026-10-02 21:19 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 9.4 MB (GitHub) · large files of this run 4.3 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-02 21:19 UTC / 2026-10-03 05:19 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · ⚠ calendar not maintained - no event listed for the next 7 days (events.yaml)
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.05% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| QNT | **DEGRADED** | 1d: DEGRADED: volume 56x normal on candle 09-29 00:00 UTC (possible bad data); 1d: DEGRADED: volume 60x normal on candle 09-30 00:00 UTC (possible bad data) |
- 72 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-02 21:19 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 895 h since 2026-08-26 | +0.0046% | 1.20 | 0.91 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 895 h since 2026-08-26 | +0.0021% | 1.68 | 0.81 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 895 h since 2026-08-26 | +0.0100% | 1.79 | 1.26 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 895 h since 2026-08-26 | +0.0100% | 3.10 | 1.04 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 895 h since 2026-08-26 | +0.0100% | 0.99 | 1.03 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 895 h since 2026-08-26 | +0.0061% | 2.49 | 1.11 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 895 h since 2026-08-26 | +0.0040% | 2.92 | 1.38 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| AVAX | GOOD | okx | 887 h since 2026-08-26 | +0.0058% | 2.90 | 1.10 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=AVAXUSDT&period=1h&limit=500 |
| LINK | GOOD | okx | 824 h since 2026-08-29 | +0.0054% | 2.24 | 0.92 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=LINKUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 895 h since 2026-08-26 | +0.0068% | 1.96 | 0.81 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **XRP**, **ZEC**, **BNB**, **SUI**
- **Research only** - backtested, never a signal: AVAX, LINK, UNI

| Not eligible | 24h volume | Why |
|---|---|---|
| QNT | $81M | order book too thin: $68k within 1% (need $250k) |
| AAVE | $60M | 7-day average volume $34M < $50M; order book too thin: $186k within 1% (need $250k) |
| ADA | $59M | 7-day average volume $42M < $50M |
| SAND | $58M | 7-day average volume $2M < $50M; 24h move +42.2% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $11k within 1% (need $250k) |
| PUMP | $56M | order book too thin: $159k within 1% (need $250k) |

**Flags (not excluded):** QNT: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, PEPE, RLUSD, TAO, USD1, USDC, WLD, XAUT (see `config.yaml`)

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
| LINK | 402 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-01 | OK (300 candles) |
| UNI | 315 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | up (HH/HL) | 87,220 / 84,520 | 0.76 | 0.49x | 1.25x | bull_reject, breakout_down, failed_breakout_down |
| ETH | mixed (LH/HL) | 2,769.68 / 2,689.47 | 0.22 | 0.28x | 1.12x | bear_engulf, breakout_down, retest_down |
| SOL | mixed (LH/HL) | 123.37 / 117.41 | 0.12 | 0.45x | 1.05x | - |
| XRP | mixed (HH/LL) | 1.555 / 1.4859 | 0.29 | 0.73x | 1.09x | displacement_down, bear_reject, breakout_down |
| ZEC | up (HH/HL) | 1,412.12 / 1,317.22 | 0.07 | 0.86x | 1.08x | displacement_down, bear_reject, breakout_down |
| BNB | up (HH/HL) | 784.46 / 774.36 | 0.11 | 0.57x | 1.03x | displacement_down, bear_engulf, breakout_down |
| SUI | mixed (LH/HL) | 1.215 / 1.1723 | 0.09 | 0.72x | 0.99x | displacement_down, bear_engulf, bear_reject, breakout_down |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 467 | 48% | 34% | 27% | 80% | 44% | 31% | can't tell from chance | 0.13R |
| 4h | displacement_down | 383 | 51% | 32% | 21% | 75% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1229 | 44% | 31% | 22% | 77% | 44% | 30% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1368 | 43% | 28% | 19% | 78% | 47% | 31% | worse than chance | 0.08R |
| 4h | bull_reject | 938 | 42% | 29% | 20% | 78% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | bear_reject | 856 | 47% | 32% | 22% | 74% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 647 | 44% | 30% | 22% | 76% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 681 | 45% | 30% | 20% | 78% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 280 | 46% | 28% | 21% | 82% | 44% | 30% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 244 | 48% | 34% | 23% | 72% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 94 | 53% | 35% | 26% | 82% | 44% | 29% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 94 | 44% | 26% | 16% | 76% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 652 | 44% | 28% | 21% | 78% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | smc_fvg_retrace_bear | 684 | 45% | 30% | 19% | 76% | 47% | 31% | can't tell from chance | 0.08R |
| 1h | displacement_up | 620 | 44% | 33% | 26% | 74% | 42% | 29% | can't tell from chance | 0.28R |
| 1h | displacement_down | 435 | 38% | 24% | 15% | 82% | 39% | 25% | can't tell from chance | 0.18R |
| 1h | bull_engulf | 1721 | 40% | 28% | 22% | 75% | 42% | 29% | can't tell from chance | 0.32R |
| 1h | bear_engulf | 1876 | 38% | 24% | 16% | 80% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | bull_reject | 1398 | 40% | 28% | 21% | 75% | 42% | 30% | can't tell from chance | 0.31R |
| 1h | bear_reject | 1331 | 36% | 23% | 17% | 81% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_sweep_bull | 654 | 41% | 27% | 20% | 77% | 42% | 29% | can't tell from chance | 0.30R |
| 1h | smc_sweep_bear | 711 | 38% | 24% | 15% | 80% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 411 | 40% | 29% | 23% | 79% | 43% | 31% | can't tell from chance | 0.28R |
| 1h | smc_bos_down | 273 | 38% | 27% | 18% | 83% | 39% | 24% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 117 | 47% | 35% | 30% | 72% | 40% | 28% | can't tell from chance | 0.32R |
| 1h | smc_choch_down | 120 | 42% | 30% | 21% | 75% | 39% | 25% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 913 | 46% | 33% | 24% | 72% | 42% | 29% | can't tell from chance | 0.30R |
| 1h | smc_fvg_retrace_bear | 797 | 40% | 27% | 19% | 79% | 38% | 24% | can't tell from chance | 0.20R |
| 30m | displacement_up | 540 | 36% | 25% | 21% | 80% | 41% | 27% | worse than chance | 0.32R |
| 30m | displacement_down | 447 | 41% | 25% | 16% | 81% | 38% | 22% | can't tell from chance | 0.19R |
| 30m | bull_engulf | 1696 | 39% | 27% | 19% | 77% | 40% | 27% | can't tell from chance | 0.35R |
| 30m | bear_engulf | 1838 | 38% | 24% | 16% | 80% | 38% | 23% | can't tell from chance | 0.21R |
| 30m | bull_reject | 1355 | 43% | 28% | 20% | 75% | 40% | 27% | can't tell from chance | 0.35R |
| 30m | bear_reject | 1457 | 38% | 24% | 17% | 80% | 38% | 23% | can't tell from chance | 0.21R |
| 30m | smc_sweep_bull | 679 | 39% | 27% | 18% | 76% | 40% | 27% | can't tell from chance | 0.35R |
| 30m | smc_sweep_bear | 636 | 43% | 27% | 19% | 80% | 38% | 23% | beats chance | 0.20R |
| 30m | smc_bos_up | 403 | 35% | 27% | 22% | 80% | 40% | 27% | can't tell from chance | 0.32R |
| 30m | smc_bos_down | 272 | 33% | 21% | 12% | 86% | 39% | 24% | can't tell from chance | 0.22R |
| 30m | smc_choch_up | 104 | 36% | 21% | 15% | 85% | 42% | 28% | can't tell from chance | 0.37R |
| 30m | smc_choch_down | 104 | 40% | 26% | 20% | 78% | 38% | 21% | can't tell from chance | 0.20R |
| 30m | smc_fvg_retrace_bull | 975 | 39% | 26% | 19% | 78% | 40% | 27% | can't tell from chance | 0.35R |
| 30m | smc_fvg_retrace_bear | 804 | 39% | 23% | 16% | 80% | 37% | 23% | can't tell from chance | 0.22R |
| 15m | displacement_up | 492 | 37% | 28% | 21% | 82% | 37% | 27% | can't tell from chance | 0.44R |
| 15m | displacement_down | 436 | 32% | 22% | 13% | 85% | 36% | 22% | can't tell from chance | 0.28R |
| 15m | bull_engulf | 1693 | 36% | 26% | 18% | 79% | 35% | 25% | can't tell from chance | 0.50R |
| 15m | bear_engulf | 1624 | 34% | 21% | 14% | 80% | 35% | 21% | can't tell from chance | 0.30R |
| 15m | bull_reject | 1287 | 38% | 28% | 19% | 79% | 35% | 25% | can't tell from chance | 0.49R |
| 15m | bear_reject | 1508 | 35% | 21% | 13% | 83% | 36% | 21% | can't tell from chance | 0.29R |
| 15m | smc_sweep_bull | 622 | 37% | 28% | 20% | 77% | 36% | 26% | can't tell from chance | 0.45R |
| 15m | smc_sweep_bear | 616 | 35% | 22% | 12% | 85% | 35% | 22% | can't tell from chance | 0.28R |
| 15m | smc_bos_up | 374 | 40% | 28% | 23% | 79% | 37% | 26% | can't tell from chance | 0.47R |
| 15m | smc_bos_down | 338 | 33% | 19% | 13% | 86% | 35% | 21% | can't tell from chance | 0.31R |
| 15m | smc_choch_up | 86 | 33% | 20% | 13% | 86% | 37% | 25% | can't tell from chance | 0.47R |
| 15m | smc_choch_down | 81 | 28% | 19% | 14% | 84% | 35% | 18% | can't tell from chance | 0.30R |
| 15m | smc_fvg_retrace_bull | 1118 | 35% | 25% | 17% | 79% | 36% | 26% | can't tell from chance | 0.48R |
| 15m | smc_fvg_retrace_bear | 939 | 35% | 23% | 15% | 82% | 35% | 21% | can't tell from chance | 0.31R |
| 5m | displacement_up | 1272 | 32% | 22% | 18% | 84% | 29% | 21% | can't tell from chance | 0.79R |
| 5m | displacement_down | 1138 | 26% | 17% | 12% | 87% | 31% | 21% | worse than chance | 0.45R |
| 5m | bull_engulf | 4318 | 27% | 19% | 14% | 82% | 29% | 20% | worse than chance | 0.82R |
| 5m | bear_engulf | 4223 | 31% | 20% | 13% | 83% | 31% | 20% | can't tell from chance | 0.50R |
| 5m | bull_reject | 3223 | 28% | 20% | 15% | 80% | 28% | 20% | can't tell from chance | 0.85R |
| 5m | bear_reject | 3672 | 34% | 21% | 14% | 82% | 31% | 21% | beats chance | 0.49R |
| 5m | smc_sweep_bull | 1267 | 29% | 20% | 14% | 80% | 31% | 21% | can't tell from chance | 0.73R |
| 5m | smc_sweep_bear | 1278 | 34% | 24% | 16% | 81% | 32% | 20% | can't tell from chance | 0.45R |
| 5m | smc_bos_up | 857 | 31% | 23% | 19% | 83% | 29% | 20% | can't tell from chance | 0.83R |
| 5m | smc_bos_down | 845 | 28% | 18% | 12% | 87% | 32% | 21% | worse than chance | 0.50R |
| 5m | smc_choch_up | 223 | 33% | 24% | 19% | 86% | 28% | 20% | can't tell from chance | 0.88R |
| 5m | smc_choch_down | 223 | 23% | 14% | 8% | 88% | 32% | 20% | worse than chance | 0.50R |
| 5m | smc_fvg_retrace_bull | 3412 | 31% | 22% | 16% | 80% | 28% | 20% | beats chance | 0.86R |
| 5m | smc_fvg_retrace_bear | 2960 | 28% | 18% | 12% | 84% | 31% | 20% | worse than chance | 0.51R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (moderate) | STRONG_BULL (strong) | WEAK_BULL (moderate) | EXPANSION down (weak) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (strong) | UNCLEAR (weak) | EXPANSION down (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H EXPANSION)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (moderate) | TRANSITION (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H TRANSITION)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | UNCLEAR (weak) | EXPANSION down (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H EXPANSION)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (moderate) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H TRANSITION)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (strong) | RANGE (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H UNCLEAR)) |
| **SUI** | UNCLEAR (weak) | TRANSITION (weak) | UNCLEAR (weak) | EXPANSION down (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H EXPANSION)) |
| **AVAX** | TRANSITION (weak) | WEAK_BULL (weak) | RANGE (moderate) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H UNCLEAR)) |
| **LINK** | WEAK_BULL (moderate) | WEAK_BULL (weak) | UNCLEAR (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H UNCLEAR, 1H TRANSITION)) |
| **UNI** | EXPANSION up (moderate) | WEAK_BULL (weak) | RANGE (moderate) | WEAK_BEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H WEAK_BEAR)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (moderate)** - for: EMA-fast rising (+1.5 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.73x normal, Bollinger width above 56% of the last 100 candles · against: EMAs not lined up
- **1D STRONG_BULL (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.4 ATR in 10 candles); swing structure up (HH/HL); ADX 41 = strong trend; candle size 1.03x normal, Bollinger width above 78% of the last 100 candles; volume 0.98x normal · against: -
- **4H WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; swing structure up (HH/HL); ADX 29 = strong trend; candle size 1.17x normal, Bollinger width above 45% of the last 100 candles; volume 1.72x normal · against: EMA-fast flat (+0.4 ATR in 10 candles) (neutral)
- **1H EXPANSION down (weak)** - for: ADX 32 = strong trend; candle size 1.25x normal, Bollinger width above 100% of the last 100 candles; volume 1.37x normal; range expansion + displacement / breakout down in the last 3 candles · against: EMAs not lined up (neutral); EMA-fast flat (+0.3 ATR in 10 candles) (neutral); swing structure up (HH/HL)

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (BOS 10 candles ago) | sell-side (bullish idea) 15 candles ago | bear 84,296.01-84,556.75 (retraced) | bear 86,133.40-86,975.51 | below the range (-2%) | equal highs 87,278.54 (4.8 ATR) | swing low 83,400.00 (1.8 ATR) |
| **ETH** | down (CHOCH 10 candles ago) | sell-side (bullish idea) 10 candles ago | bear 2,666.82-2,677.50 (retraced) | bull 2,652.20-2,695.38 | below the range (-35%) | swing high 2,769.68 (5.12 ATR) | equal lows 2,651.68 (0.48 ATR) |
| **SOL** | up (BOS 33 candles ago) | sell-side (bullish idea) 10 candles ago | bear 118.19-118.82 (retraced) | bull 115.86-117.34 | discount (6%) | swing high 123.37 (4.54 ATR) | swing low 116.73 (0.84 ATR) |
| **XRP** | down (CHOCH 27 candles ago) | sell-side (bullish idea) 10 candles ago | bear 1.4650-1.4865 (retraced) | bull 1.3773-1.3856 | below the range (-20%) | swing high 1.5550 (4.89 ATR) | PWL 1.4035 (4.07 ATR) |
| **ZEC** | down (CHOCH 11 candles ago) | sell-side (bullish idea) 10 candles ago | bear 1,306.24-1,327.08 (retraced) | bear 1,397.89-1,447.60 | below the range (-41%) | swing high 1,412.12 (4.64 ATR) | swing low 1,234.32 (1.52 ATR) |
| **BNB** | up (BOS 33 candles ago) | sell-side (bullish idea) 25 candles ago | bear 764.38-768.98 (retraced) | bear 774.08-780.19 | below the range (-102%) | equal highs 784.55 (4.49 ATR) | swing low 756.17 (1.74 ATR) |
| **SUI** | up (BOS 33 candles ago) | sell-side (bullish idea) 9 candles ago | bear 1.1221-1.1435 (retraced) | bull 1.0050-1.0598 | below the range (-124%) | swing high 1.2150 (4.26 ATR) | swing low 1.0922 (1.22 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 72 (Greed), yesterday 74  (extreme fear/greed = bigger, faster moves)

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
**Status and long-history numbers** come from the daily research run (last run 2026-10-02 00:53 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 60.0 | +1.221 | 3.69 | 2.3R | +0.97 / +2.21 | +2.21 / +0.97 | 0/5 ✗ | +1.10 | +0.98 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 15 / 7 of 23 | 0 | only 5 trades; only 1 unseen-test trades |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 15 | 46.7 | +0.338 | 1.46 | 4.1R | +0.23 / +0.56 | +0.18 / +0.44 | 0/5 ✗ | +0.03 | -0.15 | ✗  sweep_bars 8→10: -0.00R | 0 | 0.31R | 2, +0.31 (+0.31 / +0.00) | 55 / 21 of 85 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); only 15 trades; only 5 unseen-test trades |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 941 | 40.6 | +0.226 | 1.42 | 24.2R | +0.21 / +0.26 | +0.26 / +0.18 | 5/5 | +0.19 | +0.17 | stable | 9 | 0.04R | 16, +0.25 (+0.43 / -1.07) | 93 / 54 of 269 | 0 | max drawdown 24.2R |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **BACKTESTING** | 941 | 40.6 | +0.226 | 1.42 | 24.2R | +0.21 / +0.26 | +0.26 / +0.18 | 5/5 | +0.19 | +0.17 | stable | 9 | 0.04R | 16, +0.25 (+0.43 / -1.07) | 93 / 54 of 269 | 0 | max drawdown 24.2R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1070 | 40.1 | +0.219 | 1.4 | 23.7R | +0.21 / +0.23 | +0.23 / +0.21 | 5/5 | +0.19 | +0.16 | stable | 9 | 0.05R | 17, +0.24 (+0.42 / -1.07) | 160 / 67 of 362 | 0 | max drawdown 23.7R |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.206 | 1.21 | 3.3R | +0.51 / -1.32 | -1.32 / +0.51 | 0/5 ✗ | +0.08 | -0.03 | ✗  sweep_bars 20→24: -0.16R | 0 | 0.26R | 1, -1.32 (-1.32 / +0.00) | 48 / 11 of 65 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 6 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 968 | 54.9 | +0.130 | 1.29 | 21.2R | +0.12 / +0.15 | +0.13 / +0.13 | 5/5 | +0.10 | +0.07 | stable | 7 | 0.04R | 18, -0.01 (+0.12 / -1.07) | 93 / 54 of 269 | 0 | max drawdown 21.2R |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.54 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.79 (+1.79 / +0.00) | 31 / 109 of 152 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 6 / 5 of 11 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 67 / 14 of 84 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 48 / 11 of 65 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 6 / 5 of 11 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 15 / 7 of 23 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 11 | 27.3 | -0.198 | 0.62 | 2.7R | -0.39 / +0.14 | -1.11 / -0.11 | 0/5 ✗ | -0.30 | -0.24 | ✗  stop max_width_atr 3.0→3.6: -0.20R | 0 | 0.08R | 0, +0.00 (+0.00 / +0.00) | 532 / 201 of 870 | 0 | only 11 trades; avg -0.20R/trade (needs +0.10R); profit factor 0.62; only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 13 | 46.2 | -0.308 | 0.48 | 5.9R | -0.37 / +0.05 | -0.31 / -0.31 | 0/5 ✗ | -0.30 | -0.54 | ✗  time_stop_bars 30→24: -0.36R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 494 / 203 of 849 | 0 | only 13 trades; avg -0.31R/trade (needs +0.10R); profit factor 0.48; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 4 | 0.0 | -1.218 | 0.0 | 4.9R | -1.24 / -1.16 | -1.42 / -1.15 | 0/5 ✗ | -1.22 | -1.29 | ✗  stop buffer_atr 0.2→0.16: -1.23R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 67 / 14 of 84 | 0 | only 4 trades; avg -1.22R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 249 | 52.2 | +0.044 | 1.09 | 24.8R | +0.23 / -0.30 | +0.12 / -0.03 | 3/5 | -0.01 | -0.05 | ✗  stop atr 1.5→1.8: -0.01R | 6 | 0.07R | 2, +0.11 (+0.11 / +0.00) | 108 / 22 of 145 | 0 | avg +0.04R/trade (needs +0.10R); profit factor 1.09; max drawdown 24.8R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 748 | 52.9 | -0.009 | 0.98 | 43.2R | -0.02 / +0.02 | -0.07 / +0.06 | 2/5 ✗ | -0.09 | -0.17 | ✗  bb_k 2→1: -0.06R | 4 | 0.14R | 7, +0.28 (+0.27 / +0.29) | 149 / 34 of 221 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 43.2R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1168 | 34.9 | -0.019 | 0.97 | 82.5R | -0.03 / +0.02 | +0.04 / -0.08 | 3/5 ✗ | -0.10 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 4 | 0.12R | 46, +0.03 (+0.09 / -0.46) | 150 / 38 of 358 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 82.5R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FAILED** | 1168 | 34.9 | -0.019 | 0.97 | 82.5R | -0.03 / +0.02 | +0.04 / -0.08 | 3/5 ✗ | -0.10 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 4 | 0.12R | 46, +0.03 (+0.09 / -0.46) | 150 / 38 of 358 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 82.5R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 32 | 53.1 | -0.038 | 0.92 | 5.6R | +0.07 / -0.27 | +0.22 / -0.37 | 1/5 ✗ | -0.07 | -0.10 | ✗  time_stop_bars 40→32: -0.06R | 2 | 0.06R | 1, +0.24 (+0.00 / +0.24) | 168 / 5 of 176 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.92; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1379 | 34.4 | -0.038 | 0.94 | 101.7R | -0.05 / +0.01 | +0.00 / -0.08 | 2/5 ✗ | -0.12 | -0.20 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.13R | 53, +0.06 (+0.09 / -0.09) | 240 / 62 of 497 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; max drawdown 101.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 2954 | 32.3 | -0.049 | 0.92 | 232.5R | -0.08 / +0.02 | -0.03 / -0.07 | 2/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.09R | 32, +0.27 (+0.46 / -0.74) | 210 / 121 of 545 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 232.5R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 167 | 49.7 | -0.050 | 0.91 | 29.8R | -0.17 / +0.21 | -0.09 / -0.01 | 2/5 ✗ | -0.11 | -0.18 | ✗  stop atr 1.5→1.2: -0.14R | 3 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 218 / 4 of 225 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 29.8R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1198 | 49.7 | -0.052 | 0.9 | 91.4R | -0.06 / -0.04 | -0.02 / -0.08 | 1/5 ✗ | -0.13 | -0.20 | ✗  stop atr 2.0→1.6: -0.13R | 3 | 0.12R | 46, +0.04 (+0.11 / -0.46) | 150 / 38 of 358 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.90; max drawdown 91.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2601 | 32.0 | -0.054 | 0.92 | 214.7R | -0.09 / +0.03 | -0.04 / -0.07 | 1/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 29, +0.23 (+0.38 / -1.06) | 123 / 85 of 388 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 214.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FAILED** | 2601 | 32.0 | -0.055 | 0.91 | 215.6R | -0.09 / +0.03 | -0.04 / -0.07 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 29, +0.23 (+0.38 / -1.06) | 123 / 85 of 388 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 215.6R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2671 | 48.1 | -0.060 | 0.88 | 188.0R | -0.07 / -0.03 | -0.07 / -0.05 | 0/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.07R | 1 | 0.09R | 30, +0.28 (+0.38 / -0.68) | 123 / 85 of 388 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.88; max drawdown 188.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1070 | 48.4 | -0.068 | 0.87 | 115.0R | -0.02 / -0.18 | -0.01 / -0.13 | 1/5 ✗ | -0.11 | -0.15 | ✗  long_rsi_hi 65→52: -0.14R | 3 | 0.06R | 17, -0.09 (+0.02 / -0.20) | 671 / 197 of 1045 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; max drawdown 115.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 83 | 47.0 | -0.093 | 0.83 | 16.4R | +0.05 / -0.34 | -0.10 / -0.08 | 3/5 ✗ | -0.12 | -0.14 | ✗  time_stop_bars 60→48: -0.09R | 1 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 41 / 6 of 50 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.83; max drawdown 16.4R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1614 | 55.8 | -0.111 | 0.62 | 179.8R | -0.10 / -0.13 | -0.13 / -0.09 | 0/5 ✗ | -0.14 | -0.17 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.05R | 3, -0.01 (+0.00 / -0.01) | 734 / 3 of 997 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.62; max drawdown 179.8R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 311 | 44.4 | -0.111 | 0.8 | 47.9R | -0.13 / -0.07 | -0.17 / -0.04 | 0/5 ✗ | -0.18 | -0.25 | ✗  slow 21→17: -0.20R | 3 | 0.12R | 3, -1.00 (-1.00 / +0.00) | 144 / 9 of 161 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.80; max drawdown 47.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 6123 | 53.5 | -0.132 | 0.54 | 813.9R | -0.11 / -0.18 | -0.14 / -0.12 | 0/5 ✗ | -0.20 | -0.27 | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 45, -0.10 (-0.12 / -0.07) | 1048 / 9 of 1397 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.54; max drawdown 813.9R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 257 | 33.5 | -0.138 | 0.82 | 53.6R | -0.02 / -0.40 | -0.37 / +0.12 | 1/5 ✗ | -0.24 | -0.36 | ✗  time_stop_bars 30→36: -0.17R | 1 | 0.20R | 5, +0.69 (+1.94 / -0.14) | 81 / 230 of 323 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.82; max drawdown 53.6R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 5543 | 47.3 | -0.139 | 0.76 | 778.8R | -0.14 / -0.13 | -0.17 / -0.10 | 0/5 ✗ | -0.21 | -0.28 | ✗  stop atr 1.5→1.2: -0.18R | 1 | 0.13R | 54, -0.08 (-0.08 / -0.08) | 1157 / 290 of 1835 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 778.8R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 85 | 36.5 | -0.147 | 0.79 | 22.0R | -0.29 / +0.32 | -0.20 / -0.12 | 1/5 ✗ | -0.21 | -0.31 | ✗  depth 0.985→1.182: -0.45R | 2 | 0.15R | 0, +0.00 (+0.00 / +0.00) | 35 / 6 of 44 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.79; max drawdown 22.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 409 | 45.5 | -0.152 | 0.74 | 63.5R | -0.13 / -0.21 | -0.22 / -0.12 | 0/5 ✗ | -0.29 | -0.42 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.24R | 21, -0.33 (-0.27 / -0.94) | 80 / 13 of 115 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.74; max drawdown 63.5R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 41 | 36.6 | -0.161 | 0.77 | 11.3R | +0.06 / -0.47 | -0.40 / +0.06 | 1/5 ✗ | -0.33 | -0.41 | ✗  stop buffer_atr 0.2→0.16: -0.16R | 3 | 0.15R | 6, -0.79 (-0.64 / -1.51) | 102 / 35 of 151 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.77; max drawdown 11.3R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 231 | 38.5 | -0.171 | 0.74 | 59.0R | -0.19 / -0.12 | +0.13 / -0.37 | 1/5 ✗ | -0.22 | -0.28 | ✗  depth 0.985→1.182: -0.29R | 1 | 0.10R | 4, +0.53 (+0.53 / +0.00) | 77 / 8 of 94 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.74; max drawdown 59.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 148 | 46.6 | -0.181 | 0.68 | 27.2R | -0.14 / -0.31 | -0.16 / -0.20 | 2/5 ✗ | -0.25 | -0.34 | ✗  adx_min 20→24: -0.26R | 1 | 0.13R | 7, -0.39 (-0.07 / -1.18) | 54 / 5 of 70 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.68; max drawdown 27.2R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 460 | 46.7 | -0.182 | 0.71 | 83.7R | -0.21 / -0.10 | -0.24 / -0.12 | 1/5 ✗ | -0.29 | -0.41 | ✗  stop atr 1.5→1.2: -0.26R | 2 | 0.18R | 21, -0.35 (-0.41 / -0.04) | 115 / 36 of 198 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.71; max drawdown 83.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3197 | 46.1 | -0.196 | 0.68 | 630.1R | -0.17 / -0.26 | -0.22 / -0.17 | 0/5 ✗ | -0.31 | -0.42 | ✗  stop atr 1.5→1.2: -0.26R | 0 | 0.18R | 113, -0.23 (-0.16 / -0.57) | 852 / 261 of 1673 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 630.1R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2517 | 46.7 | -0.198 | 0.4 | 499.9R | -0.18 / -0.24 | -0.25 / -0.15 | 0/5 ✗ | -0.30 | -0.41 | ✗  hi 90→108: -0.25R | 0 | 0.17R | 43, -0.16 (-0.06 / -0.27) | 1057 / 36 of 1268 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.40; max drawdown 499.9R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 267 | 46.8 | -0.211 | 0.66 | 62.2R | -0.13 / -0.43 | -0.34 / -0.09 | 0/5 ✗ | -0.34 | -0.43 | ✗  stop atr 1.5→1.2: -0.29R | 1 | 0.19R | 5, -0.45 (-0.78 / +0.05) | 165 / 10 of 187 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.66; max drawdown 62.2R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 273 | 47.6 | -0.211 | 0.65 | 58.6R | -0.22 / -0.20 | -0.23 / -0.19 | 0/5 ✗ | -0.29 | -0.38 | ✗  vol_x 1.2→1.44: -0.36R | 2 | 0.17R | 7, -0.43 (-0.41 / -0.47) | 100 / 195 of 306 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.65; max drawdown 58.6R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 300 | 40.7 | -0.219 | 0.63 | 69.5R | -0.18 / -0.37 | -0.29 / -0.16 | 0/5 ✗ | -0.32 | -0.41 | ✗  fast 9→11: -0.31R | 0 | 0.17R | 11, +0.16 (+0.20 / -0.03) | 116 / 19 of 152 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.63; max drawdown 69.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 723 | 30.6 | -0.228 | 0.73 | 183.8R | -0.22 / -0.24 | -0.32 / -0.14 | 1/5 ✗ | -0.33 | -0.44 | ✗  stop buffer_atr 0.2→0.16: -0.27R | 1 | 0.22R | 19, -0.23 (+0.19 / -0.70) | 449 / 1142 of 1687 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.73; max drawdown 183.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 250 | 43.6 | -0.233 | 0.61 | 63.0R | -0.26 / -0.18 | -0.33 / -0.14 | 0/5 ✗ | -0.29 | -0.34 | ✗  st_n 10→12: -0.24R | 1 | 0.08R | 5, +0.39 (+0.39 / +0.00) | 56 / 4 of 68 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.61; max drawdown 63.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 2773 | 44.8 | -0.255 | 0.61 | 707.6R | -0.23 / -0.31 | -0.29 / -0.24 | 0/5 ✗ | -0.41 | -0.56 | ✗  stop atr 1.5→1.2: -0.33R | 0 | 0.25R | 204, -0.21 (-0.20 / -0.31) | 1382 / 214 of 2330 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 707.6R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1125 | 29.7 | -0.305 | 0.61 | 347.5R | -0.33 / -0.25 | -0.31 / -0.30 | 0/5 ✗ | -0.38 | -0.46 | ✗  rsi_n 14→17: -0.38R | 1 | 0.14R | 5, +0.13 (-0.04 / +0.38) | 750 / 9 of 805 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.61; max drawdown 347.5R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1362 | 31.8 | -0.309 | 0.62 | 433.3R | -0.33 / -0.27 | -0.32 / -0.30 | 0/5 ✗ | -0.44 | -0.56 | ✗  stop atr 1.5→1.2: -0.36R | 0 | 0.21R | 26, -0.06 (+0.26 / -0.39) | 627 / 36 of 771 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.62; max drawdown 433.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 1978 | 35.0 | -0.327 | 0.22 | 649.8R | -0.31 / -0.36 | -0.42 / -0.25 | 0/5 ✗ | -0.49 | -0.67 | ✗  hi 90→108: -0.42R | 0 | 0.28R | 88, -0.34 (-0.32 / -0.34) | 1220 / 48 of 1424 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.33R/trade (needs +0.10R); profit factor 0.22; max drawdown 649.8R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 515 | 41.7 | -0.355 | 0.51 | 191.5R | -0.33 / -0.42 | -0.33 / -0.37 | 0/5 ✗ | -0.50 | -0.64 | ✗  stop atr 1.5→1.2: -0.41R | 0 | 0.28R | 41, -0.65 (-0.69 / -0.33) | 94 / 32 of 181 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.35R/trade (needs +0.10R); profit factor 0.51; max drawdown 191.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 567 | 24.7 | -0.468 | 0.52 | 266.3R | -0.48 / -0.44 | -0.58 / -0.36 | 0/5 ✗ | -0.64 | -0.77 | ✗  n 20→24: -0.52R | 1 | 0.33R | 28, +0.12 (+0.40 / -0.25) | 480 / 1090 of 1766 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R); profit factor 0.52; max drawdown 266.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 525 | 39.0 | -0.480 | 0.39 | 252.4R | -0.43 / -0.62 | -0.58 / -0.42 | 0/5 ✗ | -0.68 | -0.91 | ✗  stop atr 1.0→0.8: -0.55R | 0 | 0.36R | 42, -0.71 (-0.61 / -0.94) | 108 / 256 of 407 | 0 | not cost-viable: fees + slippage 0.36R per trade (stop must be ≥ 4x the round-trip cost); avg -0.48R/trade (needs +0.10R); profit factor 0.39; max drawdown 252.4R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 105 | 20.0 | -0.496 | 0.5 | 56.1R | -0.40 / -0.68 | -0.59 / -0.40 | 0/5 ✗ | -0.65 | -0.78 | ✗  stop max_width_atr 3.0→2.4: -0.50R | 1 | 0.25R | 5, +0.20 (+2.42 / -1.29) | 31 / 109 of 152 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.50R/trade (needs +0.10R); profit factor 0.50; max drawdown 56.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 301 | 35.5 | -0.515 | 0.34 | 155.2R | -0.49 / -0.59 | -0.52 / -0.51 | 0/5 ✗ | -0.67 | -0.82 | ✗  stop atr 1.0→0.8: -0.56R | 0 | 0.28R | 16, -0.90 (-0.80 / -1.04) | 116 / 222 of 365 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.51R/trade (needs +0.10R); profit factor 0.34; max drawdown 155.2R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 255 | 30.6 | -0.711 | 0.25 | 181.3R | -0.79 / -0.59 | -0.68 / -0.92 | 0/5 ✗ | -1.06 | -1.41 | ✗  stop atr 1.5→1.2: -0.91R | 0 | 0.52R | 82, -0.54 (-0.50 / -0.92) | 197 / 50 of 333 | 0 | not cost-viable: fees + slippage 0.52R per trade (stop must be ≥ 4x the round-trip cost); avg -0.71R/trade (needs +0.10R); profit factor 0.25; max drawdown 181.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 433 | 26.3 | -1.156 | 0.15 | 500.5R | -1.18 / -1.13 | -1.05 / -2.00 | 0/5 ✗ | -1.82 | -2.46 | ✗  stop atr 1.0→0.8: -1.50R | 0 | 1.01R | 157, -1.15 (-1.20 / -0.93) | 218 / 668 of 1048 | 0 | not cost-viable: fees + slippage 1.01R per trade (stop must be ≥ 4x the round-trip cost); avg -1.16R/trade (needs +0.10R); profit factor 0.15; max drawdown 500.5R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **25** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 118 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.34** (Bonferroni: family-wise false-winner rate 0.05 over 118 trials; with 1 trial it would be 1.65).

**Research run duration:** 9.4 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 25 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (108.4 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 34 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

1 of 59 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 5.91 | 15.3R | 592 d (18%) | passes every gate |

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (80% of 2,954 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (75% of 1,379 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 1,070 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,601 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,168 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 941 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,601 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,168 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 941 trades shared)

🧪 **Strategy lab:** 5 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 15m | 5 | +1.221 | +2.214 | +0.338 | +0.561 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 6 | +0.206 | -1.323 | -0.308 | +0.049 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 2 | +0.037 | +0.037 | -0.595 | -0.535 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.161 | -0.467 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +2.214 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 4 | -1.218 | -1.163 | -0.198 | +0.138 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 257 | -0.138 | -0.402 | -0.228 | -0.242 | no |
| S8-PDH-PDL-SWEEP | 30m | 105 | -0.496 | -0.683 | -0.468 | -0.439 | no |


### 3c. Research layers (daily run)
Last run: **2026-10-02 00:53 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 9 | 2017-08-17 | 2026-10-01 | 19981 |  |
| 1h | 9 | 2017-08-17 | 2026-10-01 | 79860 |  |
| 30m | 9 | 2024-10-02 | 2026-10-02 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 9 | 2025-10-02 | 2026-10-02 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 9 | 2026-07-04 | 2026-10-02 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 941 (559) | false_breakout, trend_reversal | false_breakout 63%, no_displacement 32% | +0.47R | -0.37R | +0.28 / +0.23 |
| donchian_breakout-VEXIT-VRVOL | 4h | BACKTESTING | 941 (559) | false_breakout, trend_reversal | false_breakout 63%, no_displacement 32% | +0.47R | -0.37R | +0.28 / +0.23 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 1070 (641) | false_breakout | false_breakout 62% | +0.47R | -0.37R | +0.28 / +0.22 |
| donchian_breakout | 4h | BACKTESTING | 968 (437) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 65%, stop_too_tight 34% | +0.33R | -0.37R | +0.19 / +0.13 |
| bb_squeeze_breakout | 4h | FAILED | 249 (119) | false_breakout, stop_too_tight, structural_change | false_breakout 56%, stop_too_tight 41% | +0.33R | -0.33R | +0.13 / +0.04 |
| bb_squeeze_breakout | 1h | FAILED | 748 (352) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, no_displacement 52%, stop_too_tight 37%, regime_mismatch 35% | +0.35R | -0.44R | +0.17 / -0.01 |
| donchian_breakout-VEXIT | 30m | FAILED | 1168 (760) | false_breakout | false_breakout 72% | +0.48R | -0.40R | +0.14 / -0.02 |
| donchian_breakout-VEXIT-VRVOL | 30m | FAILED | 1168 (760) | false_breakout | false_breakout 72% | +0.48R | -0.40R | +0.14 / -0.02 |
| macd_trend_cross | 4h | FAILED | 32 (15) | structural_change | regime_mismatch 93%, no_displacement 87%, low_relative_volume 53%, indicator_lag 53% | +0.17R | -0.44R | +0.05 / -0.04 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1379 (905) | false_breakout | false_breakout 73% | +0.47R | -0.40R | +0.13 / -0.04 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2954 (2000) | false_breakout, regime_mismatch | false_breakout 64% | +0.51R | -0.38R | +0.06 / -0.05 |
| macd_trend_cross | 1h | FAILED | 167 (84) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 92%, indicator_lag 37%, stop_too_tight 31% | +0.32R | -0.40R | +0.11 / -0.05 |
| donchian_breakout | 30m | FAILED | 1198 (602) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 76%, stop_too_tight 33% | +0.30R | -0.41R | +0.10 / -0.05 |
| donchian_breakout-VEXIT | 1h | FAILED | 2601 (1768) | false_breakout | false_breakout 63% | +0.52R | -0.38R | +0.05 / -0.05 |
| donchian_breakout-VEXIT-VRVOL | 1h | FAILED | 2601 (1768) | false_breakout | false_breakout 63% | +0.52R | -0.38R | +0.05 / -0.06 |
| donchian_breakout | 1h | FAILED | 2671 (1387) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 32%, regime_mismatch 25% | +0.37R | -0.39R | +0.04 / -0.06 |
| trend_pullback | 4h | FAILED | 1070 (552) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 38%, stop_too_tight 26% | +0.35R | -0.43R | +0.01 / -0.07 |
| supertrend_flip | 4h | FAILED | 83 (44) | stop_too_tight, indicator_lag, structural_change | regime_mismatch 68%, indicator_lag 39%, stop_too_tight 25% | +0.39R | -0.45R | -0.03 / -0.09 |
| rsi2_dip_buy | 4h | FAILED | 1614 (714) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 44% | +0.16R | -0.21R | -0.05 / -0.11 |
| ema_9_21_cross | 1h | FAILED | 311 (173) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 79%, indicator_lag 47%, stop_too_tight 25% | +0.28R | -0.41R | +0.04 / -0.11 |
| rsi2_dip_buy | 1h | FAILED | 6123 (2845) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 42% | +0.16R | -0.20R | +0.00 / -0.13 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 257 (171) | stop_too_tight, sweep_continued | sweep_continued 97%, range_market 57%, stop_too_tight 30% | +0.57R | -0.43R | +0.11 / -0.14 |
| trend_pullback | 1h | FAILED | 5543 (2922) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 76%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.43R | +0.02 / -0.14 |
| R4-CLUC | 15m | FAILED | 85 (54) | none | - | +0.42R | -0.27R | +0.01 / -0.15 |
| ema_9_21_cross | 15m | FAILED | 409 (223) | stop_too_tight, indicator_lag | indicator_lag 47%, stop_too_tight 27% | +0.26R | -0.44R | +0.15 / -0.15 |
| S6-OB-FVG-noSMC | 15m | FAILED | 41 (26) | structural_change | stop_too_wide 88% | +0.24R | -0.47R | +0.03 / -0.16 |
| R4-CLUC | 30m | FAILED | 231 (142) | volatility_spike | - | +0.36R | -0.45R | -0.06 / -0.17 |
| supertrend_flip | 30m | FAILED | 148 (79) | stop_too_tight, indicator_lag | regime_mismatch 43%, indicator_lag 42%, stop_too_tight 35%, late_entry 28% | +0.29R | -0.44R | -0.02 / -0.18 |
| bb_squeeze_breakout | 30m | FAILED | 460 (245) | false_breakout, stop_too_tight | false_breakout 62%, stop_too_tight 39% | +0.28R | -0.43R | +0.07 / -0.18 |
| trend_pullback | 30m | FAILED | 3197 (1723) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 31% | +0.28R | -0.43R | +0.03 / -0.20 |
| rsi2_dip_buy | 30m | FAILED | 2517 (1341) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 34% | +0.16R | -0.19R | +0.01 / -0.20 |
| macd_trend_cross | 30m | FAILED | 267 (142) | stop_too_tight, indicator_lag | no_displacement 87%, indicator_lag 46%, low_relative_volume 44%, stop_too_tight 28% | +0.31R | -0.45R | +0.03 / -0.21 |
| liquidity_sweep_reversal | 1h | FAILED | 273 (143) | stop_too_tight | stop_too_tight 52% | +0.29R | -0.46R | -0.01 / -0.21 |
| ema_9_21_cross | 30m | FAILED | 300 (178) | indicator_lag | indicator_lag 47%, low_relative_volume 40% | +0.26R | -0.39R | -0.01 / -0.22 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 723 (502) | range_market, trend_reversal, stop_too_tight | range_market 46%, stop_too_tight 36% | +0.63R | -0.51R | +0.03 / -0.23 |
| supertrend_flip | 1h | FAILED | 250 (141) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 70%, stop_too_tight 38%, indicator_lag 33% | +0.39R | -0.37R | -0.13 / -0.23 |
| trend_pullback | 15m | FAILED | 2773 (1531) | wrong_session, stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 31% | +0.25R | -0.44R | +0.06 / -0.26 |
| R4-BBRSI | 1h | FAILED | 1125 (791) | none | - | +0.44R | -0.45R | -0.13 / -0.30 |
| R4-BBRSI | 30m | FAILED | 1362 (929) | none | - | +0.43R | -0.44R | -0.05 / -0.31 |
| rsi2_dip_buy | 15m | FAILED | 1978 (1285) | trend_reversal, fees_slippage | fees_slippage 45% | +0.17R | -0.19R | +0.01 / -0.33 |
| bb_squeeze_breakout | 15m | FAILED | 515 (300) | stop_too_tight | no_displacement 58%, false_breakout 58%, stop_too_tight 41% | +0.31R | -0.47R | -0.01 / -0.35 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 567 (427) | stop_too_tight | stop_too_tight 33% | +0.60R | -0.49R | -0.06 / -0.47 |
| liquidity_sweep_reversal | 15m | FAILED | 525 (320) | stop_too_tight | stop_too_tight 38% | +0.37R | -0.46R | -0.01 / -0.48 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 105 (84) | stop_too_tight, sweep_continued | sweep_continued 96%, stop_too_tight 29% | +0.49R | -0.67R | -0.15 / -0.50 |
| liquidity_sweep_reversal | 30m | FAILED | 301 (194) | stop_too_tight | stop_too_tight 39% | +0.41R | -0.47R | -0.19 / -0.52 |
| ema_9_21_cross | 5m | FAILED | 255 (177) | stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 32% | +0.25R | -0.46R | -0.02 / -0.71 |
| liquidity_sweep_reversal | 5m | FAILED | 433 (319) | htf_conflict, stop_too_tight | stop_too_tight 38% | +0.29R | -0.50R | +0.15 / -1.16 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 27 strategy/timeframe tests); `false_breakout` (systematic in 15 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `regime_mismatch` (systematic in 12 strategy/timeframe tests); `trend_reversal` (systematic in 8 strategy/timeframe tests); `volatility_spike` (systematic in 4 strategy/timeframe tests); `no_displacement` (systematic in 2 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests)

**Missed moves:** no strong move in the last 24 hours at the last research run.

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
| `memory/family_gates_shadow.csv` | 120.0 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 10.7 KB | - | - |
| `memory/missed_trades.md` | 18.0 KB | 24 | 2026-10-01 00:55 UTC |
| `memory/playbook.md` | 8.7 KB | - | - |
| `memory/research_sources.md` | 59.7 KB | 45 | 2026-09-28 15:40 UTC |
| `memory/smc_events.csv` | 657.4 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 16.2 KB | - | - |
| `memory/strategy_registry.csv` | 36.5 KB | - | - |
| `memory/trials.csv` | 9.2 KB | - | - |
| `memory/universe_log.md` | 18.0 KB | - | - |

**Reviews due** (review date passed; for the reviews): `missed_trades.md` LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00 (2026-10-02)
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*