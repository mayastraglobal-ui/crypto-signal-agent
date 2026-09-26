# Crypto Signal Report

**Updated:** 2026-09-26 14:23 Beijing time (2026-09-26 06:23 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 5.2 MB (GitHub) · large files of this run 2.3 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-26 06:23 UTC / 2026-09-26 14:23 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US PCE / Personal Income and Outlays (Aug data) 2026-09-30 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked, never emailed). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.02% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| VTHO | **DEGRADED** | 1d: DEGRADED: volume 269x normal on candle 09-25 00:00 UTC (possible bad data) |
| BABY | **DEGRADED** | 1d: DEGRADED: volume 65x normal on candle 09-23 00:00 UTC (possible bad data); 1d: DEGRADED: volume 67x normal on candle 09-25 00:00 UTC (possible bad data) |
- 75 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-26 06:22 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 736 h since 2026-08-26 | +0.0017% | 1.35 | 0.86 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 736 h since 2026-08-26 | +0.0034% | 1.35 | 1.17 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 736 h since 2026-08-26 | +0.0100% | 2.31 | 0.74 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 736 h since 2026-08-26 | +0.0038% | 1.44 | 1.27 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 736 h since 2026-08-26 | +0.0062% | 0.57 | 1.18 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 736 h since 2026-08-26 | +0.0015% | 1.75 | 1.13 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| ENA | GOOD | okx | 736 h since 2026-08-26 | +0.0050% | 0.92 | 0.91 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ENAUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 736 h since 2026-08-26 | +0.0100% | 1.82 | 1.15 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 736 h since 2026-08-26 | +0.0100% | 2.46 | 0.39 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| ADA | GOOD | okx | 723 h since 2026-08-27 | +0.0100% | 1.94 | 0.81 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ADAUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **XRP**, **SOL**, **ZEC**, **SUI**, **ENA**
- **Research only** - backtested, never a signal: UNI, BNB, ADA

| Not eligible | 24h volume | Why |
|---|---|---|
| VTHO | $123M | 7-day average volume $21M < $50M; spread 0.124% > 0.1%; order book too thin: $50k within 1% (need $250k) |
| LINK | $81M | 7-day average volume $50M < $50M |
| BABY | $68M | 7-day average volume $25M < $50M; order book too thin: $68k within 1% (need $250k) |
| ONDO | $58M | 7-day average volume $49M < $50M; order book too thin: $226k within 1% (need $250k) |
| XPL | $52M | 7-day average volume $25M < $50M; order book too thin: $181k within 1% (need $250k) |

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
| BTC | mixed (LH/HL) | 84,145.3 / 83,632 | 0.23 | 0.27x | 0.66x | bear_engulf |
| ETH | mixed (LH/HL) | 2,696.44 / 2,677.16 | 0.21 | 0.33x | 0.67x | bear_engulf |
| XRP | mixed (LH/HL) | 1.581 / 1.5492 | 0.19 | 0.35x | 0.79x | - |
| SOL | up (HH/HL) | 122.94 / 120.82 | 0.56 | 0.27x | 0.98x | bear_engulf |
| ZEC | mixed (LH/HL) | 1,560.64 / 1,524.79 | 0.51 | 0.18x | 0.75x | - |
| SUI | up (HH/HL) | 1.2179 / 1.0901 | 0.08 | 0.31x | 1.22x | - |
| ENA | up (HH/HL) | 0.2735 / 0.2632 | 0.06 | 1.67x | 1.30x | displacement_down, bear_engulf, breakout_up, failed_breakout_up |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 471 | 48% | 34% | 27% | 79% | 44% | 31% | can't tell from chance | 0.12R |
| 4h | displacement_down | 370 | 48% | 31% | 21% | 75% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1195 | 45% | 31% | 22% | 77% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | bear_engulf | 1382 | 45% | 30% | 20% | 77% | 48% | 32% | worse than chance | 0.08R |
| 4h | bull_reject | 913 | 41% | 28% | 20% | 79% | 43% | 29% | can't tell from chance | 0.12R |
| 4h | bear_reject | 927 | 48% | 34% | 24% | 73% | 48% | 32% | can't tell from chance | 0.07R |
| 4h | smc_sweep_bull | 655 | 42% | 28% | 21% | 78% | 43% | 29% | can't tell from chance | 0.12R |
| 4h | smc_sweep_bear | 671 | 43% | 29% | 19% | 80% | 48% | 32% | worse than chance | 0.08R |
| 4h | smc_bos_up | 269 | 44% | 29% | 22% | 82% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | smc_bos_down | 248 | 53% | 39% | 27% | 67% | 48% | 32% | can't tell from chance | 0.07R |
| 4h | smc_choch_up | 86 | 52% | 33% | 27% | 81% | 43% | 30% | can't tell from chance | 0.12R |
| 4h | smc_choch_down | 79 | 42% | 23% | 11% | 78% | 50% | 35% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 662 | 44% | 29% | 23% | 77% | 43% | 29% | can't tell from chance | 0.12R |
| 4h | smc_fvg_retrace_bear | 676 | 49% | 34% | 22% | 74% | 48% | 32% | can't tell from chance | 0.08R |
| 1h | displacement_up | 618 | 48% | 36% | 29% | 72% | 43% | 30% | beats chance | 0.26R |
| 1h | displacement_down | 431 | 37% | 24% | 15% | 81% | 40% | 26% | can't tell from chance | 0.17R |
| 1h | bull_engulf | 1689 | 40% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.30R |
| 1h | bear_engulf | 1852 | 40% | 26% | 18% | 79% | 38% | 25% | can't tell from chance | 0.18R |
| 1h | bull_reject | 1400 | 40% | 29% | 22% | 76% | 42% | 29% | can't tell from chance | 0.29R |
| 1h | bear_reject | 1371 | 37% | 25% | 17% | 82% | 39% | 25% | can't tell from chance | 0.17R |
| 1h | smc_sweep_bull | 633 | 40% | 25% | 19% | 78% | 42% | 29% | can't tell from chance | 0.28R |
| 1h | smc_sweep_bear | 700 | 38% | 25% | 16% | 80% | 39% | 25% | can't tell from chance | 0.17R |
| 1h | smc_bos_up | 398 | 43% | 31% | 24% | 78% | 42% | 29% | can't tell from chance | 0.25R |
| 1h | smc_bos_down | 270 | 39% | 27% | 19% | 81% | 38% | 25% | can't tell from chance | 0.20R |
| 1h | smc_choch_up | 117 | 48% | 37% | 32% | 71% | 42% | 30% | can't tell from chance | 0.32R |
| 1h | smc_choch_down | 118 | 45% | 29% | 17% | 75% | 39% | 25% | can't tell from chance | 0.16R |
| 1h | smc_fvg_retrace_bull | 887 | 46% | 33% | 25% | 71% | 42% | 29% | beats chance | 0.28R |
| 1h | smc_fvg_retrace_bear | 827 | 41% | 29% | 19% | 78% | 39% | 25% | can't tell from chance | 0.18R |
| 30m | displacement_up | 654 | 41% | 30% | 25% | 78% | 43% | 30% | can't tell from chance | 0.28R |
| 30m | displacement_down | 426 | 39% | 23% | 13% | 83% | 36% | 21% | can't tell from chance | 0.18R |
| 30m | bull_engulf | 1709 | 42% | 29% | 21% | 75% | 42% | 30% | can't tell from chance | 0.33R |
| 30m | bear_engulf | 1744 | 36% | 22% | 15% | 82% | 36% | 21% | can't tell from chance | 0.20R |
| 30m | bull_reject | 1340 | 45% | 30% | 22% | 74% | 42% | 30% | can't tell from chance | 0.33R |
| 30m | bear_reject | 1428 | 37% | 23% | 15% | 82% | 37% | 22% | can't tell from chance | 0.20R |
| 30m | smc_sweep_bull | 618 | 41% | 28% | 19% | 75% | 42% | 29% | can't tell from chance | 0.33R |
| 30m | smc_sweep_bear | 634 | 41% | 26% | 18% | 82% | 37% | 21% | beats chance | 0.19R |
| 30m | smc_bos_up | 452 | 42% | 34% | 28% | 76% | 41% | 29% | can't tell from chance | 0.30R |
| 30m | smc_bos_down | 242 | 38% | 23% | 14% | 85% | 37% | 21% | can't tell from chance | 0.23R |
| 30m | smc_choch_up | 104 | 36% | 23% | 17% | 83% | 42% | 31% | can't tell from chance | 0.37R |
| 30m | smc_choch_down | 99 | 39% | 22% | 16% | 81% | 37% | 22% | can't tell from chance | 0.16R |
| 30m | smc_fvg_retrace_bull | 978 | 44% | 30% | 23% | 74% | 42% | 30% | can't tell from chance | 0.33R |
| 30m | smc_fvg_retrace_bear | 833 | 38% | 22% | 16% | 82% | 36% | 21% | can't tell from chance | 0.22R |
| 15m | displacement_up | 478 | 35% | 26% | 19% | 82% | 36% | 24% | can't tell from chance | 0.40R |
| 15m | displacement_down | 464 | 34% | 21% | 14% | 85% | 37% | 23% | can't tell from chance | 0.27R |
| 15m | bull_engulf | 1655 | 38% | 27% | 19% | 79% | 36% | 25% | can't tell from chance | 0.46R |
| 15m | bear_engulf | 1618 | 36% | 24% | 15% | 79% | 36% | 22% | can't tell from chance | 0.27R |
| 15m | bull_reject | 1323 | 35% | 23% | 16% | 80% | 36% | 25% | can't tell from chance | 0.47R |
| 15m | bear_reject | 1437 | 35% | 22% | 15% | 82% | 37% | 23% | can't tell from chance | 0.27R |
| 15m | smc_sweep_bull | 599 | 38% | 27% | 21% | 77% | 36% | 25% | can't tell from chance | 0.43R |
| 15m | smc_sweep_bear | 636 | 38% | 25% | 14% | 83% | 37% | 23% | can't tell from chance | 0.26R |
| 15m | smc_bos_up | 377 | 39% | 28% | 21% | 80% | 37% | 26% | can't tell from chance | 0.40R |
| 15m | smc_bos_down | 353 | 33% | 20% | 14% | 86% | 36% | 22% | can't tell from chance | 0.30R |
| 15m | smc_choch_up | 89 | 30% | 22% | 18% | 82% | 34% | 26% | can't tell from chance | 0.42R |
| 15m | smc_choch_down | 89 | 31% | 20% | 12% | 82% | 38% | 24% | can't tell from chance | 0.27R |
| 15m | smc_fvg_retrace_bull | 1008 | 34% | 24% | 16% | 81% | 36% | 24% | can't tell from chance | 0.45R |
| 15m | smc_fvg_retrace_bear | 983 | 36% | 25% | 17% | 80% | 37% | 23% | can't tell from chance | 0.28R |
| 5m | displacement_up | 1213 | 31% | 21% | 16% | 85% | 28% | 19% | beats chance | 0.76R |
| 5m | displacement_down | 1142 | 28% | 18% | 12% | 86% | 31% | 20% | can't tell from chance | 0.49R |
| 5m | bull_engulf | 4113 | 27% | 18% | 13% | 83% | 28% | 19% | worse than chance | 0.83R |
| 5m | bear_engulf | 4058 | 32% | 21% | 13% | 83% | 31% | 21% | can't tell from chance | 0.50R |
| 5m | bull_reject | 3397 | 27% | 18% | 13% | 82% | 28% | 19% | can't tell from chance | 0.83R |
| 5m | bear_reject | 3725 | 33% | 22% | 15% | 81% | 32% | 21% | can't tell from chance | 0.48R |
| 5m | smc_sweep_bull | 1196 | 31% | 22% | 15% | 79% | 29% | 20% | can't tell from chance | 0.74R |
| 5m | smc_sweep_bear | 1264 | 35% | 24% | 16% | 81% | 32% | 21% | can't tell from chance | 0.44R |
| 5m | smc_bos_up | 842 | 29% | 21% | 16% | 85% | 29% | 20% | can't tell from chance | 0.76R |
| 5m | smc_bos_down | 864 | 28% | 19% | 11% | 87% | 31% | 21% | can't tell from chance | 0.55R |
| 5m | smc_choch_up | 217 | 38% | 26% | 17% | 86% | 27% | 19% | beats chance | 0.81R |
| 5m | smc_choch_down | 223 | 26% | 15% | 12% | 87% | 33% | 21% | worse than chance | 0.50R |
| 5m | smc_fvg_retrace_bull | 3285 | 29% | 20% | 14% | 82% | 27% | 19% | can't tell from chance | 0.82R |
| 5m | smc_fvg_retrace_bear | 2938 | 28% | 19% | 12% | 84% | 31% | 20% | worse than chance | 0.51R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (weak) | WEAK_BULL (moderate) | WEAK_BULL (weak) | RANGE (strong) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ETH** | UNCLEAR (weak) | WEAK_BULL (moderate) | UNCLEAR (weak) | RANGE (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H UNCLEAR, 1H RANGE)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | TRANSITION (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (moderate) | WEAK_BULL (weak) | LONG allowed (1D/4H/1H bullish, 1W TRANSITION) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | RANGE (strong) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |
| **SUI** | RANGE (weak) | EXPANSION up (weak) | WEAK_BULL (weak) | STRONG_BULL (moderate) | LONG allowed (1D/4H/1H bullish, 1W RANGE) |
| **ENA** | TRANSITION (weak) | WEAK_BULL (weak) | STRONG_BULL (moderate) | STRONG_BULL (strong) | LONG allowed (1D/4H/1H bullish, 1W TRANSITION) |
| **UNI** | EXPANSION up (weak) | STRONG_BULL (moderate) | TRANSITION (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H TRANSITION, 1H UNCLEAR)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | COMPRESSION (strong) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |
| **ADA** | UNCLEAR (weak) | TRANSITION (weak) | TRANSITION (weak) | WEAK_BULL (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H WEAK_BULL)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (weak)** - for: EMA-fast rising (+1.1 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.72x normal, Bollinger width above 52% of the last 100 candles · against: EMAs not lined up; ADX 27 is close to a threshold
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.2 ATR in 10 candles); ADX 44 = strong trend; candle size 1.15x normal, Bollinger width above 80% of the last 100 candles; volume 1.48x normal · against: swing structure mixed (neutral)
- **4H WEAK_BULL (weak)** - for: close above EMA-fast above EMA-slow; swing structure up (HH/HL); candle size 1.07x normal, Bollinger width above 43% of the last 100 candles; volume 0.87x normal · against: EMA-fast flat (+0.6 ATR in 10 candles) (neutral); ADX 19 = weak trend / ranging; ADX 19 is close to a threshold
- **1H RANGE (strong)** - for: EMAs not lined up; EMA-fast flat (-0.3 ATR in 10 candles); swing structure mixed; ADX 18 = weak trend / ranging; candle size 0.66x normal, Bollinger width above 12% of the last 100 candles · against: -

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **London**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | up (BOS 38 candles ago) | sell-side (bullish idea) 64 candles ago | bear 84,744.74-84,841.04 | bear 86,133.40-86,975.51 | premium (56%) | equal highs 84,193.39 (0.78 ATR) | swing low 83,632.03 (0.82 ATR) |
| **ETH** | up (BOS 16 candles ago) | sell-side (bullish idea) 0 candles ago | bear 2,760.00-2,765.00 (retraced) | bear 2,745.99-2,784.40 | discount (48%) | swing high 2,696.44 (0.7 ATR) | swing low 2,677.16 (0.65 ATR) |
| **XRP** | up (CHOCH 72 candles ago) | sell-side (bullish idea) 2 candles ago | bear 1.6015-1.6117 (retraced) | bull 1.3773-1.3856 | discount (3%) | swing high 1.5810 (1.69 ATR) | swing low 1.5492 (0.04 ATR) |
| **SOL** | down (CHOCH 12 candles ago) | sell-side (bullish idea) 3 candles ago | bear 121.02-121.57 | bull 115.86-117.34 | below the range (-14%) | swing high 122.94 (2.01 ATR) | swing low 118.27 (1.87 ATR) |
| **ZEC** | down (BOS 12 candles ago) | sell-side (bullish idea) 7 candles ago | bear 1,549.43-1,552.00 (retraced) | bull 1,098.88-1,133.82 | discount (30%) | swing high 1,560.64 (1.18 ATR) | swing low 1,524.79 (0.51 ATR) |
| **SUI** | up (BOS 31 candles ago) | buy-side (bearish idea) 40 candles ago | bull 1.0755-1.0969 (retraced) | bull 1.0050-1.0598 | premium (52%) | PDH 1.2179 (2.5 ATR) | swing low 1.0901 (2.7 ATR) |
| **ENA** | up (BOS 9 candles ago) | sell-side (bullish idea) 16 candles ago | bull 0.25770-0.25950 (retraced) | bull 0.16130-0.17050 | premium (60%) | - | swing low 0.26320 (0.82 ATR) |

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
**Status and long-history numbers** come from the daily research run (last run 2026-09-26 00:50 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged, never emailed.
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 60.0 | +1.221 | 3.69 | 2.3R | +0.97 / +2.21 | +2.21 / +0.97 | 0/5 ✗ | +1.10 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 25 / 14 of 40 | 0 | only 5 trades; only 1 unseen-test trades |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 15 | 46.7 | +0.338 | 1.46 | 4.1R | +0.23 / +0.56 | +0.18 / +0.44 | 0/5 ✗ | +0.03 | ✗  sweep_bars 8→10: -0.00R | 0 | 0.31R | 2, +0.31 (+1.94 / -1.32) | 48 / 28 of 83 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); only 15 trades; only 5 unseen-test trades |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.206 | 1.21 | 3.3R | +0.51 / -1.32 | -1.32 / +0.51 | 0/5 ✗ | +0.08 | ✗  sweep_bars 20→24: -0.16R | 0 | 0.26R | 1, -1.32 (+0.00 / -1.32) | 40 / 13 of 59 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 6 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 3 of 4 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 56 / 14 of 73 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 40 / 13 of 59 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 3 of 4 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 25 / 14 of 40 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 13 | 23.1 | -0.353 | 0.44 | 5.1R | -0.51 / -0.10 | -1.17 / -0.11 | 0/5 ✗ | -0.47 | ✗  stop buffer_atr 0.2→0.24: -0.36R | 0 | 0.09R | 0, +0.00 (+0.00 / +0.00) | 537 / 217 of 924 | 0 | only 13 trades; avg -0.35R/trade (needs +0.10R); profit factor 0.44; only 5 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 14 | 42.9 | -0.365 | 0.42 | 6.5R | -0.43 / +0.05 | -0.31 / -0.39 | 0/5 ✗ | -0.30 | ✗  time_stop_bars 30→24: -0.42R | 0 | 0.16R | 1, +1.21 (+1.21 / +0.00) | 450 / 232 of 810 | 0 | only 14 trades; avg -0.37R/trade (needs +0.10R); profit factor 0.42; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 5 | 0.0 | -1.422 | 0.0 | 7.1R | -1.24 / -1.70 | -1.42 / -1.42 | 0/5 ✗ | -1.55 | ✗  stop buffer_atr 0.2→0.16: -1.48R | 0 | 0.21R | 0, +0.00 (+0.00 / +0.00) | 56 / 14 of 73 | 0 | only 5 trades; avg -1.42R/trade (needs +0.10R); profit factor 0.00; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.712 | 0.0 | 1.7R | +0.00 / -1.71 | -1.71 / +0.00 | 0/5 ✗ | -2.00 | ✗  stop buffer_atr 0.2→0.16: -1.75R | 0 | 0.86R | 0, +0.00 (+0.00 / +0.00) | 32 / 108 of 150 | 0 | not cost-viable: fees + slippage 0.86R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.71R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 4h | **FAILED** | 1097 | 54.2 | +0.110 | 1.25 | 21.1R | +0.10 / +0.14 | +0.09 / +0.13 | 5/5 | +0.08 | stable | 7 | 0.04R | 13, +0.17 (+0.42 / -0.40) | 98 / 50 of 271 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); max drawdown 21.1R |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 283 | 53.7 | +0.069 | 1.14 | 22.7R | +0.21 / -0.23 | +0.14 / +0.00 | 3/5 | +0.02 | stable | 7 | 0.07R | 2, +0.08 (-1.11 / +1.27) | 103 / 24 of 144 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg +0.07R/trade (needs +0.10R); profit factor 1.14; max drawdown 22.7R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 35 | 54.3 | +0.016 | 1.03 | 4.5R | +0.14 / -0.33 | +0.19 / -0.22 | 2/5 ✗ | -0.01 | ✗  time_stop_bars 40→32: -0.03R | 1 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 156 / 5 of 163 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg +0.02R/trade (needs +0.10R); profit factor 1.03; only 9 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 832 | 52.6 | -0.019 | 0.96 | 51.7R | -0.04 / +0.02 | -0.07 / +0.04 | 2/5 ✗ | -0.10 | ✗  bb_k 2→1: -0.07R | 4 | 0.14R | 5, -0.30 (-1.18 / +0.29) | 136 / 44 of 214 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 51.7R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 90 | 48.9 | -0.039 | 0.93 | 17.4R | +0.14 / -0.36 | +0.03 / -0.13 | 3/5 ✗ | -0.06 | ✗  st_n 10→12: -0.06R | 2 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 43 / 6 of 51 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.04R/trade (needs +0.10R); profit factor 0.93; max drawdown 17.4R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 193 | 49.7 | -0.048 | 0.91 | 33.0R | -0.15 / +0.17 | -0.05 / -0.05 | 2/5 ✗ | -0.11 | ✗  stop atr 1.5→1.2: -0.10R | 3 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 217 / 7 of 226 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 33.0R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 42 | 38.1 | -0.064 | 0.9 | 9.5R | +0.14 / -0.39 | -0.28 / +0.10 | 1/5 ✗ | -0.21 | ✗  time_stop_bars 30→24: -0.04R | 3 | 0.15R | 6, -0.26 (+0.17 / -0.48) | 103 / 35 of 150 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.90; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1294 | 49.1 | -0.065 | 0.88 | 113.8R | -0.08 / -0.04 | -0.04 / -0.09 | 1/5 ✗ | -0.14 | ✗  stop atr 2.0→1.6: -0.14R | 3 | 0.12R | 49, -0.06 (-0.23 / +0.15) | 140 / 60 of 422 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.06R/trade (needs +0.10R); profit factor 0.88; max drawdown 113.8R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2977 | 47.9 | -0.066 | 0.87 | 222.8R | -0.08 / -0.04 | -0.08 / -0.05 | 0/5 ✗ | -0.12 | ✗  stop atr 2.0→1.6: -0.08R | 1 | 0.09R | 31, +0.26 (+0.23 / +0.33) | 134 / 105 of 425 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.07R/trade (needs +0.10R); profit factor 0.87; max drawdown 222.8R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1213 | 47.6 | -0.085 | 0.85 | 135.9R | -0.04 / -0.19 | -0.01 / -0.17 | 1/5 ✗ | -0.12 | ✗  long_rsi_hi 65→52: -0.18R | 3 | 0.06R | 6, +1.14 (+1.12 / +1.27) | 637 / 203 of 994 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.08R/trade (needs +0.10R); profit factor 0.85; max drawdown 135.9R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 302 | 34.1 | -0.103 | 0.87 | 53.4R | -0.08 / -0.15 | -0.37 / +0.17 | 1/5 ✗ | -0.21 | ✗  time_stop_bars 30→36: -0.14R | 2 | 0.20R | 1, +2.70 (+0.00 / +2.70) | 90 / 234 of 333 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.87; max drawdown 53.4R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1864 | 56.0 | -0.104 | 0.63 | 194.5R | -0.10 / -0.11 | -0.13 / -0.08 | 0/5 ✗ | -0.14 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.05R | 9, -0.18 (-0.18 / +0.00) | 764 / 4 of 1030 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.63; max drawdown 194.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 344 | 45.1 | -0.112 | 0.79 | 46.4R | -0.11 / -0.11 | -0.15 / -0.07 | 0/5 ✗ | -0.18 | ✗  slow 21→17: -0.21R | 3 | 0.12R | 3, -1.00 (-1.25 / -0.52) | 152 / 7 of 167 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.79; max drawdown 46.4R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 7001 | 53.9 | -0.125 | 0.55 | 883.1R | -0.10 / -0.17 | -0.14 / -0.11 | 0/5 ✗ | -0.19 | ✗  stop atr 2.0→1.6: -0.15R | 0 | 0.11R | 42, -0.15 (-0.26 / +0.00) | 1040 / 7 of 1400 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.55; max drawdown 883.1R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6248 | 47.1 | -0.146 | 0.75 | 931.0R | -0.15 / -0.14 | -0.18 / -0.10 | 0/5 ✗ | -0.22 | ✗  stop atr 1.5→1.2: -0.18R | 1 | 0.13R | 44, +0.09 (-0.00 / +0.23) | 1214 / 303 of 1883 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.15R/trade (needs +0.10R); profit factor 0.75; max drawdown 931.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 443 | 45.1 | -0.159 | 0.73 | 76.2R | -0.17 / -0.14 | -0.19 / -0.14 | 1/5 ✗ | -0.30 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.25R | 19, +0.12 (+0.14 / +0.02) | 66 / 14 of 103 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.73; max drawdown 76.2R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 158 | 46.8 | -0.180 | 0.68 | 28.7R | -0.18 / -0.17 | -0.20 / -0.17 | 2/5 ✗ | -0.24 | ✗  adx_min 20→24: -0.28R | 1 | 0.13R | 6, -0.74 (-0.64 / -1.26) | 57 / 6 of 73 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.18R/trade (needs +0.10R); profit factor 0.68; max drawdown 28.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3465 | 46.3 | -0.189 | 0.69 | 677.0R | -0.18 / -0.22 | -0.21 / -0.17 | 0/5 ✗ | -0.30 | ✗  stop atr 1.5→1.2: -0.25R | 0 | 0.18R | 83, +0.14 (+0.28 / -0.10) | 849 / 263 of 1716 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.19R/trade (needs +0.10R); profit factor 0.69; max drawdown 677.0R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 296 | 48.0 | -0.192 | 0.69 | 64.1R | -0.14 / -0.31 | -0.33 / -0.08 | 0/5 ✗ | -0.32 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.20R | 5, -0.08 (+0.66 / -1.18) | 186 / 11 of 215 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.19R/trade (needs +0.10R); profit factor 0.69; max drawdown 64.1R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 813 | 32.1 | -0.198 | 0.76 | 196.7R | -0.17 / -0.25 | -0.28 / -0.13 | 1/5 ✗ | -0.30 | ✗  stop buffer_atr 0.2→0.16: -0.23R | 1 | 0.21R | 10, +0.20 (+0.87 / -0.48) | 452 / 1180 of 1715 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.76; max drawdown 196.7R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 280 | 45.4 | -0.200 | 0.66 | 59.7R | -0.20 / -0.21 | -0.23 / -0.17 | 1/5 ✗ | -0.27 | ✗  st_n 10→12: -0.22R | 2 | 0.08R | 4, +0.17 (-0.19 / +1.24) | 58 / 2 of 68 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.20R/trade (needs +0.10R); profit factor 0.66; max drawdown 59.7R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2792 | 46.8 | -0.201 | 0.39 | 564.0R | -0.18 / -0.24 | -0.25 / -0.15 | 0/5 ✗ | -0.30 | ✗  hi 90→108: -0.25R | 0 | 0.17R | 43, -0.14 (-0.19 / -0.02) | 1024 / 24 of 1258 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.39; max drawdown 564.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 486 | 45.7 | -0.202 | 0.68 | 98.4R | -0.27 / -0.02 | -0.26 / -0.15 | 1/5 ✗ | -0.31 | ✗  stop atr 1.5→1.2: -0.27R | 1 | 0.19R | 17, -0.47 (-0.41 / -0.58) | 125 / 42 of 212 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 98.4R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 337 | 41.5 | -0.204 | 0.65 | 73.1R | -0.19 / -0.26 | -0.32 / -0.11 | 2/5 ✗ | -0.30 | ✗  fast 9→11: -0.29R | 0 | 0.17R | 10, +0.01 (-0.03 / +0.06) | 108 / 20 of 145 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.65; max drawdown 73.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 313 | 47.9 | -0.222 | 0.63 | 71.0R | -0.23 / -0.20 | -0.25 / -0.19 | 0/5 ✗ | -0.32 | ✗  vol_x 1.2→1.44: -0.35R | 2 | 0.17R | 4, -0.23 (+0.01 / -0.48) | 101 / 220 of 329 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.63; max drawdown 71.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 3022 | 44.7 | -0.256 | 0.61 | 774.9R | -0.24 / -0.29 | -0.30 / -0.23 | 0/5 ✗ | -0.41 | ✗  stop atr 1.5→1.2: -0.33R | 0 | 0.25R | 168, -0.06 (-0.03 / -0.11) | 1356 / 369 of 2323 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 774.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 2181 | 34.6 | -0.336 | 0.21 | 732.7R | -0.32 / -0.36 | -0.43 / -0.26 | 0/5 ✗ | -0.51 | ✗  hi 90→108: -0.43R | 0 | 0.28R | 68, -0.29 (-0.27 / -0.36) | 1192 / 31 of 1365 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.34R/trade (needs +0.10R); profit factor 0.21; max drawdown 732.7R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 551 | 41.9 | -0.347 | 0.51 | 199.9R | -0.32 / -0.41 | -0.30 / -0.37 | 0/5 ✗ | -0.49 | ✗  stop atr 1.5→1.2: -0.41R | 0 | 0.28R | 41, -0.67 (-0.47 / -0.93) | 100 / 52 of 212 | 0 | BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00); not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.35R/trade (needs +0.10R); profit factor 0.51; max drawdown 199.9R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 621 | 25.0 | -0.458 | 0.53 | 292.8R | -0.47 / -0.43 | -0.55 / -0.38 | 0/5 ✗ | -0.63 | ✗  n 20→24: -0.49R | 1 | 0.35R | 17, +0.15 (+0.64 / -0.41) | 436 / 1062 of 1683 | 0 | not cost-viable: fees + slippage 0.35R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.53; max drawdown 292.8R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 327 | 37.9 | -0.462 | 0.39 | 151.5R | -0.43 / -0.54 | -0.45 / -0.48 | 0/5 ✗ | -0.62 | ✗  long_rsi_max 45→36: -0.51R | 0 | 0.28R | 10, -0.44 (-0.29 / -0.59) | 110 / 225 of 358 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.39; max drawdown 151.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 113 | 21.2 | -0.500 | 0.49 | 62.1R | -0.39 / -0.70 | -0.56 / -0.45 | 1/5 ✗ | -0.64 | ✗  stop max_width_atr 3.0→2.4: -0.50R | 0 | 0.25R | 3, -0.07 (-1.25 / +2.29) | 32 / 108 of 150 | 0 | avg -0.50R/trade (needs +0.10R); profit factor 0.49; max drawdown 62.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 563 | 38.0 | -0.505 | 0.38 | 284.7R | -0.48 / -0.58 | -0.59 / -0.46 | 0/5 ✗ | -0.71 | ✗  stop atr 1.0→0.8: -0.56R | 0 | 0.37R | 27, -0.43 (-0.51 / -0.34) | 97 / 259 of 386 | 0 | not cost-viable: fees + slippage 0.37R per trade (stop must be ≥ 4x the round-trip cost); avg -0.50R/trade (needs +0.10R); profit factor 0.38; max drawdown 284.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 272 | 29.4 | -0.730 | 0.24 | 198.6R | -0.81 / -0.61 | -0.69 / -0.93 | 0/5 ✗ | -1.09 | ✗  stop atr 1.5→1.2: -0.92R | 0 | 0.58R | 64, -0.52 (-0.51 / -0.55) | 200 / 74 of 339 | 0 | not cost-viable: fees + slippage 0.58R per trade (stop must be ≥ 4x the round-trip cost); avg -0.73R/trade (needs +0.10R); profit factor 0.24; max drawdown 198.6R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 424 | 26.4 | -1.147 | 0.16 | 491.1R | -1.22 / -1.06 | -1.05 / -1.74 | 0/5 ✗ | -1.81 | ✗  stop atr 1.0→0.8: -1.49R | 0 | 1.05R | 114, -1.17 (-1.37 / -0.96) | 186 / 624 of 931 | 0 | not cost-viable: fees + slippage 1.05R per trade (stop must be ≥ 4x the round-trip cost); avg -1.15R/trade (needs +0.10R); profit factor 0.16; max drawdown 491.1R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **20** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 46 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.06** (Bonferroni: family-wise false-winner rate 0.05 over 46 trials; with 1 trial it would be 1.65).

**Research run duration:** 10.0 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 20 cards checked - history cut after 6 signal candles, and started 500 candles later; 5 BIASED (114.8 s).

- ⛔ **bb_squeeze_breakout@1.0 BIASED** - FAILED on every timeframe, for good: recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- ⛔ **donchian_breakout@1.0 BIASED** - FAILED on every timeframe, for good: recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- ⛔ **macd_trend_cross@1.0 BIASED** - FAILED on every timeframe, for good: recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- ⛔ **supertrend_flip@1.0 BIASED** - FAILED on every timeframe, for good: recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- ⛔ **trend_pullback@1.0 BIASED** - FAILED on every timeframe, for good: recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 26 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 15m | 5 | +1.221 | +2.214 | +0.338 | +0.561 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 6 | +0.206 | -1.323 | -0.365 | +0.049 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.064 | -0.390 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +2.214 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 5 | -1.422 | -1.701 | -0.353 | -0.101 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 1 | -1.712 | -1.712 | -0.566 | -0.550 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 302 | -0.103 | -0.154 | -0.198 | -0.248 | yes |
| S8-PDH-PDL-SWEEP | 30m | 113 | -0.500 | -0.700 | -0.458 | -0.428 | no |

- **donchian_breakout v1.0 4h:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **bb_squeeze_breakout v1.0 4h:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **macd_trend_cross v1.0 4h:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **bb_squeeze_breakout v1.0 1h:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **supertrend_flip v1.0 4h:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **macd_trend_cross v1.0 1h:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **donchian_breakout v1.0 30m:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **donchian_breakout v1.0 1h:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **trend_pullback v1.0 4h:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **trend_pullback v1.0 1h:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **supertrend_flip v1.0 30m:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **trend_pullback v1.0 30m:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **macd_trend_cross v1.0 30m:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **supertrend_flip v1.0 1h:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **bb_squeeze_breakout v1.0 30m:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **trend_pullback v1.0 15m:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
- **bb_squeeze_breakout v1.0 15m:** BIASED - recursive on 1h: long: htf_up (489 of 78216 candles differ, first 2017-10-18 22:00); recursive on 1h: short: htf_down (108 of 78216 candles differ, first 2017-10-25 15:00)
**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): donchian_breakout@1.0 4h BACKTESTING → FAILED

### 3c. Research layers (daily run)
Last run: **2026-09-26 00:50 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 10 | 2017-08-17 | 2026-09-25 | 19945 |  |
| 1h | 10 | 2017-08-17 | 2026-09-25 | 79716 |  |
| 30m | 10 | 2024-09-26 | 2026-09-26 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 10 | 2025-09-26 | 2026-09-26 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 10 | 2026-06-28 | 2026-09-26 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout | 4h | FAILED | 1097 (502) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 66%, stop_too_tight 34% | +0.35R | -0.38R | +0.17 / +0.11 |
| bb_squeeze_breakout | 4h | FAILED | 283 (131) | false_breakout, stop_too_tight, structural_change | false_breakout 56%, stop_too_tight 41%, regime_mismatch 29% | +0.32R | -0.33R | +0.16 / +0.07 |
| macd_trend_cross | 4h | FAILED | 35 (16) | none | regime_mismatch 94%, no_displacement 88%, indicator_lag 56%, low_relative_volume 50% | +0.18R | -0.44R | +0.10 / +0.02 |
| bb_squeeze_breakout | 1h | FAILED | 832 (394) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 61%, no_displacement 53%, stop_too_tight 36%, regime_mismatch 35% | +0.34R | -0.43R | +0.15 / -0.02 |
| supertrend_flip | 4h | FAILED | 90 (46) | stop_too_tight, indicator_lag, structural_change | regime_mismatch 67%, indicator_lag 37%, stop_too_tight 28% | +0.45R | -0.47R | +0.03 / -0.04 |
| macd_trend_cross | 1h | FAILED | 193 (97) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 93%, wrong_session 72%, indicator_lag 37%, stop_too_tight 32% | +0.32R | -0.39R | +0.11 / -0.05 |
| S6-OB-FVG-noSMC | 15m | FAILED | 42 (26) | structural_change | - | +0.37R | -0.46R | +0.11 / -0.06 |
| donchian_breakout | 30m | FAILED | 1294 (658) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 76%, stop_too_tight 34% | +0.30R | -0.41R | +0.09 / -0.07 |
| donchian_breakout | 1h | FAILED | 2977 (1551) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 31% | +0.37R | -0.40R | +0.04 / -0.07 |
| trend_pullback | 4h | FAILED | 1213 (636) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 39%, stop_too_tight 26% | +0.35R | -0.42R | -0.01 / -0.09 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 302 (199) | stop_too_tight, sweep_continued | sweep_continued 97%, range_market 54%, stop_too_tight 30% | +0.56R | -0.45R | +0.14 / -0.10 |
| rsi2_dip_buy | 4h | FAILED | 1864 (821) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 45% | +0.16R | -0.20R | -0.04 / -0.10 |
| ema_9_21_cross | 1h | FAILED | 344 (189) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 79%, indicator_lag 48%, stop_too_tight 26% | +0.28R | -0.38R | +0.04 / -0.11 |
| rsi2_dip_buy | 1h | FAILED | 7001 (3226) | trend_reversal, regime_mismatch, volatility_spike, fees_slippage | regime_mismatch 41%, fees_slippage 25% | +0.16R | -0.20R | +0.01 / -0.12 |
| trend_pullback | 1h | FAILED | 6248 (3308) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 77%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.42R | +0.01 / -0.15 |
| ema_9_21_cross | 15m | FAILED | 443 (243) | stop_too_tight, indicator_lag | indicator_lag 47%, stop_too_tight 28% | +0.26R | -0.42R | +0.14 / -0.16 |
| supertrend_flip | 30m | FAILED | 158 (84) | stop_too_tight, indicator_lag | regime_mismatch 45%, indicator_lag 43%, stop_too_tight 36%, late_entry 29% | +0.29R | -0.43R | -0.02 / -0.18 |
| trend_pullback | 30m | FAILED | 3465 (1859) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 31% | +0.28R | -0.42R | +0.04 / -0.19 |
| macd_trend_cross | 30m | FAILED | 296 (154) | stop_too_tight, indicator_lag | no_displacement 86%, low_relative_volume 46%, indicator_lag 46%, stop_too_tight 30% | +0.30R | -0.44R | +0.05 / -0.19 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 813 (552) | range_market, stop_too_tight | range_market 47%, stop_too_tight 36% | +0.62R | -0.50R | +0.06 / -0.20 |
| supertrend_flip | 1h | FAILED | 280 (153) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 71%, regime_mismatch 70%, stop_too_tight 37%, indicator_lag 34% | +0.38R | -0.37R | -0.09 / -0.20 |
| rsi2_dip_buy | 30m | FAILED | 2792 (1485) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 34% | +0.17R | -0.19R | +0.01 / -0.20 |
| bb_squeeze_breakout | 30m | FAILED | 486 (264) | false_breakout, stop_too_tight | false_breakout 62%, stop_too_tight 39% | +0.27R | -0.43R | +0.05 / -0.20 |
| ema_9_21_cross | 30m | FAILED | 337 (197) | indicator_lag | indicator_lag 48%, low_relative_volume 40% | +0.26R | -0.39R | +0.01 / -0.20 |
| liquidity_sweep_reversal | 1h | FAILED | 313 (163) | trend_reversal, stop_too_tight | stop_too_tight 50% | +0.27R | -0.46R | -0.02 / -0.22 |
| trend_pullback | 15m | FAILED | 3022 (1671) | wrong_session, stop_too_tight, indicator_lag | wrong_session 71%, indicator_lag 49%, stop_too_tight 32% | +0.25R | -0.44R | +0.07 / -0.26 |
| rsi2_dip_buy | 15m | FAILED | 2181 (1426) | trend_reversal, fees_slippage | fees_slippage 45% | +0.17R | -0.19R | +0.01 / -0.34 |
| bb_squeeze_breakout | 15m | FAILED | 551 (320) | stop_too_tight | false_breakout 57%, no_displacement 57%, range_market 52%, stop_too_tight 40% | +0.31R | -0.46R | +0.00 / -0.35 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 621 (466) | stop_too_tight | stop_too_tight 33% | +0.60R | -0.49R | -0.04 / -0.46 |
| liquidity_sweep_reversal | 30m | FAILED | 327 (203) | trend_reversal, stop_too_tight | stop_too_tight 40% | +0.41R | -0.45R | -0.14 / -0.46 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 113 (89) | stop_too_tight, sweep_continued | sweep_continued 97%, stop_too_tight 30% | +0.50R | -0.67R | -0.17 / -0.50 |
| liquidity_sweep_reversal | 15m | FAILED | 563 (349) | stop_too_tight | stop_too_tight 40% | +0.37R | -0.45R | -0.03 / -0.51 |
| ema_9_21_cross | 5m | FAILED | 272 (192) | stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 30% | +0.24R | -0.43R | -0.02 / -0.73 |
| liquidity_sweep_reversal | 5m | FAILED | 424 (312) | stop_too_tight | stop_too_tight 36% | +0.27R | -0.46R | +0.17 / -1.15 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 27 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `regime_mismatch` (systematic in 11 strategy/timeframe tests); `trend_reversal` (systematic in 7 strategy/timeframe tests); `false_breakout` (systematic in 6 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `fees_slippage` (systematic in 3 strategy/timeframe tests); `no_displacement` (systematic in 2 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests)

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
| `memory/changelog.md` | 88.3 KB | - | - |
| `memory/coin_notes.md` | 0.6 KB | - | - |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 3.3 KB | 6 | 2026-09-26 00:24 UTC |
| `memory/experiments.md` | 34.8 KB | 10 | 2026-09-25 18:45 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 0.8 KB | - | - |
| `memory/market_mechanics.md` | 10.0 KB | 11 | 2026-09-25 14:00 UTC |
| `memory/market_regime_log.md` | 3.7 KB | - | - |
| `memory/missed_trades.md` | 4.4 KB | 5 | 2026-09-26 00:50 UTC |
| `memory/playbook.md` | 8.5 KB | - | - |
| `memory/research_sources.md` | 34.2 KB | 28 | 2026-09-25 19:10 UTC |
| `memory/smc_events.csv` | 81.7 KB | - | - |
| `memory/smc_research.md` | 5.7 KB | - | - |
| `memory/strategy_lifecycle.md` | 12.9 KB | - | - |
| `memory/strategy_registry.csv` | 32.8 KB | - | - |
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