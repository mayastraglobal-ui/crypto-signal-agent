# Crypto Signal Report

**Updated:** 2026-09-29 06:18 Beijing time (2026-09-28 22:18 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 6.7 MB (GitHub) · large files of this run 3.8 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-28 22:18 UTC / 2026-09-29 06:18 Beijing
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
| QNT | **DEGRADED** | 1d: DEGRADED: volume 91x normal on candle 09-27 00:00 UTC (possible bad data) |
- 74 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-28 22:18 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 800 h since 2026-08-26 | +0.0071% | 1.35 | 1.21 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 800 h since 2026-08-26 | +0.0029% | 1.32 | 0.83 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 800 h since 2026-08-26 | +0.0006% | 0.67 | 0.97 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 800 h since 2026-08-26 | -0.0009% | 1.67 | 0.70 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 800 h since 2026-08-26 | +0.0000% | 2.87 | 1.14 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 800 h since 2026-08-26 | +0.0100% | 2.04 | - | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| LINK | GOOD | okx | 729 h since 2026-08-29 | -0.0021% | 1.37 | 1.19 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=LINKUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 800 h since 2026-08-26 | +0.0022% | 1.81 | 0.61 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 800 h since 2026-08-26 | +0.0027% | 2.28 | 0.55 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| ENA | GOOD | okx | 800 h since 2026-08-26 | +0.0050% | - | 0.63 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ENAUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **ZEC**, **SOL**, **XRP**, **SUI**, **LINK**
- **Research only** - backtested, never a signal: UNI, BNB, ENA

| Not eligible | 24h volume | Why |
|---|---|---|
| QNT | $305M | 7-day average volume $38M < $50M; suspended for the rest of the UTC day (moved more than ±25% earlier today); order book too thin: $46k within 1% (need $250k) |
| HBAR | $195M | 7-day average volume $19M < $50M; 24h move +30.7% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $171k within 1% (need $250k) |
| PUMP | $96M | 7-day average volume $31M < $50M; order book too thin: $142k within 1% (need $250k) |
| ONDO | $87M | 7-day average volume $49M < $50M; order book too thin: $185k within 1% (need $250k) |
| XLM | $69M | 7-day average volume $32M < $50M |
| MARSCOIN | $62M | only 24 days of history (need 180); 7-day average volume $23M < $50M; suspended for the rest of the UTC day (moved more than ±25% earlier today); order book too thin: $59k within 1% (need $250k) |

**Flags (not excluded):** QNT: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, TAO, USD1, USDC, WLD, XAUT (see `config.yaml`)

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
| UNI | 315 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| BNB | 464 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| ENA | 130 | 909 | 903 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | down (LH/LL) | 84,381.3 / 82,563 | 0.01 | 0.22x | 1.36x | bear_engulf |
| ETH | up (HH/HL) | 2,721.42 / 2,651.68 | 0.00 | 0.45x | 1.35x | bear_engulf |
| ZEC | down (LH/LL) | 1,599.73 / 1,536.63 | 0.99 | 0.95x | 1.23x | displacement_down, breakout_down |
| SOL | mixed (HH/LL) | 120.73 / 117.36 | 0.03 | 0.74x | 1.22x | bear_engulf |
| XRP | mixed (LH/HL) | 1.5324 / 1.474 | 0.10 | 0.77x | 1.26x | bear_engulf |
| SUI | down (LH/LL) | 1.2051 / 1.133 | 0.13 | 0.36x | 1.13x | bear_engulf |
| LINK | mixed (HH/LL) | 15.489 / 13.476 | 0.14 | 0.50x | 1.71x | bull_engulf, bear_engulf, bear_div |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 480 | 50% | 35% | 28% | 79% | 44% | 31% | beats chance | 0.12R |
| 4h | displacement_down | 382 | 49% | 32% | 21% | 75% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1199 | 45% | 32% | 23% | 77% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | bear_engulf | 1371 | 44% | 29% | 20% | 77% | 47% | 31% | worse than chance | 0.08R |
| 4h | bull_reject | 897 | 42% | 29% | 21% | 78% | 44% | 30% | can't tell from chance | 0.12R |
| 4h | bear_reject | 894 | 47% | 33% | 23% | 74% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 644 | 43% | 29% | 22% | 77% | 44% | 30% | can't tell from chance | 0.12R |
| 4h | smc_sweep_bear | 679 | 43% | 29% | 18% | 80% | 47% | 31% | worse than chance | 0.08R |
| 4h | smc_bos_up | 291 | 46% | 29% | 22% | 82% | 44% | 31% | can't tell from chance | 0.13R |
| 4h | smc_bos_down | 248 | 53% | 39% | 27% | 69% | 48% | 33% | can't tell from chance | 0.07R |
| 4h | smc_choch_up | 90 | 56% | 38% | 28% | 79% | 42% | 30% | beats chance | 0.13R |
| 4h | smc_choch_down | 87 | 41% | 23% | 11% | 77% | 51% | 32% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 667 | 45% | 29% | 23% | 77% | 44% | 31% | can't tell from chance | 0.12R |
| 4h | smc_fvg_retrace_bear | 683 | 47% | 32% | 21% | 75% | 48% | 31% | can't tell from chance | 0.08R |
| 1h | displacement_up | 619 | 45% | 34% | 27% | 73% | 43% | 31% | can't tell from chance | 0.27R |
| 1h | displacement_down | 409 | 39% | 25% | 16% | 81% | 37% | 23% | can't tell from chance | 0.18R |
| 1h | bull_engulf | 1720 | 40% | 29% | 22% | 74% | 43% | 30% | worse than chance | 0.31R |
| 1h | bear_engulf | 1861 | 38% | 24% | 16% | 80% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | bull_reject | 1401 | 41% | 29% | 22% | 75% | 43% | 30% | can't tell from chance | 0.30R |
| 1h | bear_reject | 1375 | 36% | 24% | 17% | 82% | 38% | 24% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bull | 636 | 41% | 28% | 20% | 76% | 42% | 30% | can't tell from chance | 0.30R |
| 1h | smc_sweep_bear | 721 | 37% | 22% | 14% | 81% | 38% | 23% | can't tell from chance | 0.18R |
| 1h | smc_bos_up | 423 | 41% | 30% | 24% | 77% | 44% | 31% | can't tell from chance | 0.25R |
| 1h | smc_bos_down | 273 | 38% | 27% | 18% | 82% | 38% | 24% | can't tell from chance | 0.20R |
| 1h | smc_choch_up | 115 | 49% | 36% | 31% | 70% | 43% | 31% | can't tell from chance | 0.32R |
| 1h | smc_choch_down | 109 | 44% | 29% | 19% | 75% | 38% | 22% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 899 | 46% | 34% | 25% | 70% | 43% | 31% | can't tell from chance | 0.29R |
| 1h | smc_fvg_retrace_bear | 774 | 41% | 28% | 19% | 78% | 37% | 23% | can't tell from chance | 0.20R |
| 30m | displacement_up | 627 | 42% | 32% | 26% | 77% | 42% | 29% | can't tell from chance | 0.28R |
| 30m | displacement_down | 413 | 43% | 27% | 17% | 80% | 37% | 22% | beats chance | 0.17R |
| 30m | bull_engulf | 1719 | 43% | 30% | 22% | 74% | 42% | 29% | can't tell from chance | 0.32R |
| 30m | bear_engulf | 1822 | 37% | 22% | 15% | 81% | 37% | 21% | can't tell from chance | 0.20R |
| 30m | bull_reject | 1340 | 45% | 30% | 23% | 73% | 42% | 29% | beats chance | 0.31R |
| 30m | bear_reject | 1446 | 37% | 23% | 16% | 81% | 37% | 22% | can't tell from chance | 0.19R |
| 30m | smc_sweep_bull | 647 | 39% | 27% | 17% | 75% | 42% | 30% | can't tell from chance | 0.33R |
| 30m | smc_sweep_bear | 636 | 42% | 26% | 17% | 82% | 37% | 21% | beats chance | 0.19R |
| 30m | smc_bos_up | 472 | 40% | 32% | 26% | 77% | 42% | 30% | can't tell from chance | 0.29R |
| 30m | smc_bos_down | 232 | 37% | 23% | 11% | 84% | 36% | 21% | can't tell from chance | 0.22R |
| 30m | smc_choch_up | 96 | 40% | 25% | 19% | 82% | 44% | 32% | can't tell from chance | 0.36R |
| 30m | smc_choch_down | 99 | 44% | 28% | 22% | 76% | 39% | 22% | can't tell from chance | 0.16R |
| 30m | smc_fvg_retrace_bull | 970 | 43% | 30% | 23% | 74% | 41% | 29% | can't tell from chance | 0.31R |
| 30m | smc_fvg_retrace_bear | 759 | 38% | 21% | 16% | 80% | 37% | 22% | can't tell from chance | 0.21R |
| 15m | displacement_up | 451 | 36% | 27% | 20% | 81% | 35% | 25% | can't tell from chance | 0.40R |
| 15m | displacement_down | 453 | 31% | 20% | 13% | 86% | 37% | 23% | worse than chance | 0.29R |
| 15m | bull_engulf | 1681 | 36% | 25% | 18% | 79% | 35% | 24% | can't tell from chance | 0.48R |
| 15m | bear_engulf | 1635 | 37% | 24% | 15% | 78% | 37% | 23% | can't tell from chance | 0.29R |
| 15m | bull_reject | 1323 | 35% | 23% | 15% | 80% | 34% | 24% | can't tell from chance | 0.48R |
| 15m | bear_reject | 1461 | 37% | 23% | 15% | 81% | 37% | 23% | can't tell from chance | 0.29R |
| 15m | smc_sweep_bull | 624 | 35% | 24% | 18% | 79% | 34% | 24% | can't tell from chance | 0.45R |
| 15m | smc_sweep_bear | 624 | 37% | 24% | 13% | 84% | 38% | 24% | can't tell from chance | 0.26R |
| 15m | smc_bos_up | 361 | 38% | 27% | 22% | 80% | 34% | 23% | can't tell from chance | 0.39R |
| 15m | smc_bos_down | 374 | 34% | 21% | 13% | 84% | 36% | 22% | can't tell from chance | 0.32R |
| 15m | smc_choch_up | 84 | 29% | 21% | 17% | 81% | 35% | 24% | can't tell from chance | 0.45R |
| 15m | smc_choch_down | 83 | 33% | 24% | 16% | 81% | 36% | 24% | can't tell from chance | 0.29R |
| 15m | smc_fvg_retrace_bull | 1041 | 34% | 23% | 15% | 81% | 35% | 24% | can't tell from chance | 0.49R |
| 15m | smc_fvg_retrace_bear | 962 | 37% | 26% | 18% | 79% | 37% | 23% | can't tell from chance | 0.30R |
| 5m | displacement_up | 1231 | 31% | 22% | 17% | 84% | 28% | 20% | beats chance | 0.79R |
| 5m | displacement_down | 1164 | 27% | 17% | 11% | 88% | 30% | 20% | worse than chance | 0.51R |
| 5m | bull_engulf | 4242 | 26% | 19% | 14% | 83% | 28% | 20% | worse than chance | 0.85R |
| 5m | bear_engulf | 4148 | 30% | 20% | 13% | 83% | 30% | 20% | can't tell from chance | 0.53R |
| 5m | bull_reject | 3273 | 27% | 19% | 14% | 81% | 28% | 20% | can't tell from chance | 0.89R |
| 5m | bear_reject | 3729 | 32% | 21% | 14% | 82% | 31% | 20% | can't tell from chance | 0.51R |
| 5m | smc_sweep_bull | 1228 | 28% | 20% | 14% | 81% | 30% | 21% | can't tell from chance | 0.77R |
| 5m | smc_sweep_bear | 1270 | 33% | 23% | 16% | 82% | 32% | 21% | can't tell from chance | 0.45R |
| 5m | smc_bos_up | 833 | 31% | 23% | 19% | 83% | 28% | 20% | can't tell from chance | 0.80R |
| 5m | smc_bos_down | 899 | 28% | 17% | 10% | 88% | 31% | 21% | worse than chance | 0.56R |
| 5m | smc_choch_up | 227 | 34% | 26% | 18% | 86% | 28% | 19% | can't tell from chance | 0.90R |
| 5m | smc_choch_down | 225 | 24% | 14% | 9% | 88% | 30% | 20% | worse than chance | 0.53R |
| 5m | smc_fvg_retrace_bull | 3386 | 30% | 21% | 15% | 81% | 28% | 19% | beats chance | 0.87R |
| 5m | smc_fvg_retrace_bear | 3009 | 27% | 18% | 12% | 84% | 30% | 20% | worse than chance | 0.54R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (moderate) | WEAK_BULL (moderate) | RANGE (strong) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H UNCLEAR)) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (moderate) | HIGH_VOL_RANGE (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H HIGH_VOL_RANGE)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | UNCLEAR (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H TRANSITION)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (weak) | UNCLEAR (weak) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | RANGE (weak) | RANGE (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H RANGE, 1H RANGE)) |
| **SUI** | UNCLEAR (weak) | EXPANSION up (weak) | STRONG_BULL (moderate) | UNCLEAR (weak) | LONG allowed (1D/4H bullish, 1W UNCLEAR) |
| **LINK** | WEAK_BULL (moderate) | WEAK_BULL (weak) | TRANSITION (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H TRANSITION)) |
| **UNI** | EXPANSION up (moderate) | STRONG_BULL (moderate) | TRANSITION (weak) | WEAK_BEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H TRANSITION, 1H WEAK_BEAR)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (strong) | RANGE (moderate) | HIGH_VOL_RANGE (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H HIGH_VOL_RANGE)) |
| **ENA** | TRANSITION (weak) | EXPANSION up (moderate) | STRONG_BULL (strong) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W TRANSITION) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (moderate)** - for: EMA-fast rising (+1.5 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.73x normal, Bollinger width above 56% of the last 100 candles · against: EMAs not lined up
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.5 ATR in 10 candles); ADX 44 = strong trend; candle size 1.05x normal, Bollinger width above 82% of the last 100 candles; volume 0.97x normal · against: swing structure mixed (neutral)
- **4H RANGE (strong)** - for: EMAs not lined up; EMA-fast flat (+0.3 ATR in 10 candles); swing structure mixed; ADX 15 = weak trend / ranging; candle size 0.97x normal, Bollinger width above 24% of the last 100 candles · against: -
- **1H UNCLEAR (weak)** - for: candle size 1.36x normal, Bollinger width above 69% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.3 ATR in 10 candles); swing structure down (LH/LL); ADX 21 = in between (20-25); ADX 21 is close to a threshold; signals are mixed and trend strength is in between

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | up (BOS 23 candles ago) | sell-side (bullish idea) 29 candles ago | bear 83,236.01-83,400.00 | bear 84,342.00-84,843.00 | discount (36%) | swing high 84,381.30 (2.3 ATR) | equal lows 82,563.00 (1.3 ATR) |
| **ETH** | up (CHOCH 20 candles ago) | sell-side (bullish idea) 54 candles ago | bear 2,675.27-2,678.56 | bear 2,745.99-2,784.40 | discount (33%) | equal highs 2,724.12 (2.44 ATR) | swing low 2,651.68 (1.11 ATR) |
| **ZEC** | down (BOS 13 candles ago) | sell-side (bullish idea) 3 candles ago | bear 1,490.19-1,510.34 | bear 1,540.16-1,569.23 | below the range (-108%) | swing high 1,599.73 (4.78 ATR) | swing low 1,445.85 (0.81 ATR) |
| **SOL** | up (CHOCH 20 candles ago) | sell-side (bullish idea) 0 candles ago | bear 117.82-118.05 | bull 115.86-117.34 | discount (11%) | swing high 120.73 (2.22 ATR) | swing low 117.36 (0.27 ATR) |
| **XRP** | up (CHOCH 40 candles ago) | buy-side (bearish idea) 42 candles ago | bear 1.4987-1.5070 (retraced) | bull 1.3773-1.3856 | discount (21%) | swing high 1.5324 (2.21 ATR) | swing low 1.4740 (0.57 ATR) |
| **SUI** | down (BOS 10 candles ago) | sell-side (bullish idea) 31 candles ago | bear 1.1507-1.1542 (retraced) | bull 1.0050-1.0598 | discount (19%) | swing high 1.2051 (2.26 ATR) | swing low 1.1330 (0.53 ATR) |
| **LINK** | up (BOS 23 candles ago) | buy-side (bearish idea) 6 candles ago | bull 14.469-14.641 (retraced) | bull 13.642-13.992 | premium (83%) | swing high 15.489 (0.99 ATR) | swing low 13.476 (4.89 ATR) |

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
- **Heat:** max 3 positions, 1 per coin, 1 per group of correlated coins and direction (1h correlation ≥ 0.7) · groups now: BTC+ETH+LINK+SOL+SUI+XRP
- **Every live entry also needs:** reward to TP1 ≥ 2R, no opposing level before TP1, no high-impact event within ±60 min, no duplicate
- **Event calendar (next 7 days):** US GDP (Third Estimate), 2nd Quarter 2026 2026-09-30 12:30 UTC, US PCE / Personal Income and Outlays (Aug data) 2026-09-30 12:30 UTC, US jobs report / Employment Situation (Sep data) 2026-10-02 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-09-28 00:52 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 60.0 | +1.221 | 3.69 | 2.3R | +0.97 / +2.21 | +2.21 / +0.97 | 0/5 ✗ | +1.10 | +0.98 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 23 / 8 of 32 | 0 | only 5 trades; only 1 unseen-test trades |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 15 | 46.7 | +0.338 | 1.46 | 4.1R | +0.23 / +0.56 | +0.18 / +0.44 | 0/5 ✗ | +0.03 | -0.15 | ✗  sweep_bars 8→10: -0.00R | 0 | 0.31R | 2, +0.31 (+0.31 / +0.00) | 54 / 26 of 86 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); only 15 trades; only 5 unseen-test trades |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 939 | 40.6 | +0.226 | 1.42 | 24.2R | +0.21 / +0.26 | +0.26 / +0.18 | 5/5 | +0.19 | +0.17 | stable | 9 | 0.04R | 13, +0.61 (+0.54 / +1.44) | 94 / 52 of 274 | 0 | max drawdown 24.2R |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **BACKTESTING** | 939 | 40.6 | +0.226 | 1.42 | 24.2R | +0.21 / +0.26 | +0.26 / +0.18 | 5/5 | +0.19 | +0.17 | stable | 9 | 0.04R | 13, +0.61 (+0.54 / +1.44) | 94 / 52 of 274 | 0 | max drawdown 24.2R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1067 | 40.1 | +0.220 | 1.4 | 23.7R | +0.21 / +0.23 | +0.23 / +0.21 | 5/5 | +0.19 | +0.16 | stable | 9 | 0.05R | 14, +0.70 (+0.78 / +0.20) | 156 / 66 of 361 | 0 | max drawdown 23.7R |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.206 | 1.21 | 3.3R | +0.51 / -1.32 | -1.32 / +0.51 | 0/5 ✗ | +0.08 | -0.03 | ✗  sweep_bars 20→24: -0.16R | 0 | 0.26R | 1, -1.32 (-1.32 / +0.00) | 39 / 11 of 57 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 6 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 965 | 54.8 | +0.129 | 1.29 | 21.2R | +0.12 / +0.15 | +0.13 / +0.13 | 5/5 | +0.10 | +0.07 | stable | 7 | 0.04R | 16, +0.17 (+0.17 / +0.20) | 94 / 52 of 274 | 0 | max drawdown 21.2R |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.78 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.79 (+0.00 / +1.79) | 31 / 103 of 147 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 4 of 5 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 58 / 16 of 77 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 39 / 11 of 57 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 4 of 5 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 23 / 8 of 32 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 11 | 27.3 | -0.198 | 0.62 | 2.7R | -0.39 / +0.14 | -1.11 / -0.11 | 0/5 ✗ | -0.30 | -0.24 | ✗  stop max_width_atr 3.0→3.6: -0.20R | 0 | 0.08R | 0, +0.00 (+0.00 / +0.00) | 552 / 191 of 894 | 0 | only 11 trades; avg -0.20R/trade (needs +0.10R); profit factor 0.62; only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 13 | 46.2 | -0.308 | 0.48 | 5.9R | -0.37 / +0.05 | -0.31 / -0.31 | 0/5 ✗ | -0.30 | -0.54 | ✗  time_stop_bars 30→24: -0.36R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 452 / 239 of 832 | 0 | only 13 trades; avg -0.31R/trade (needs +0.10R); profit factor 0.48; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 4 | 0.0 | -1.218 | 0.0 | 4.9R | -1.24 / -1.16 | -1.42 / -1.15 | 0/5 ✗ | -1.22 | -1.29 | ✗  stop buffer_atr 0.2→0.16: -1.23R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 58 / 16 of 77 | 0 | only 4 trades; avg -1.22R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 248 | 52.4 | +0.048 | 1.09 | 24.8R | +0.23 / -0.29 | +0.13 / -0.03 | 3/5 | -0.00 | -0.05 | ✗  stop atr 1.5→1.8: -0.00R | 6 | 0.07R | 3, -0.30 (+0.08 / -1.05) | 99 / 23 of 136 | 0 | avg +0.05R/trade (needs +0.10R); profit factor 1.09; max drawdown 24.8R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 748 | 52.9 | -0.009 | 0.98 | 43.2R | -0.02 / +0.02 | -0.07 / +0.06 | 2/5 ✗ | -0.09 | -0.17 | ✗  bb_k 2→1: -0.06R | 4 | 0.14R | 6, +0.05 (-0.23 / +0.33) | 146 / 39 of 225 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 43.2R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1168 | 34.8 | -0.019 | 0.97 | 82.5R | -0.04 / +0.04 | +0.04 / -0.08 | 2/5 ✗ | -0.10 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 4 | 0.12R | 51, -0.03 (+0.07 / -0.48) | 153 / 38 of 372 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 82.5R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FAILED** | 1168 | 34.8 | -0.019 | 0.97 | 82.5R | -0.04 / +0.04 | +0.04 / -0.08 | 2/5 ✗ | -0.10 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 4 | 0.12R | 51, -0.03 (+0.07 / -0.48) | 153 / 38 of 372 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 82.5R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1379 | 34.3 | -0.040 | 0.94 | 101.7R | -0.06 / +0.03 | +0.01 / -0.09 | 2/5 ✗ | -0.12 | -0.20 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.13R | 56, -0.05 (+0.01 / -0.26) | 254 / 57 of 521 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; max drawdown 101.7R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 31 | 51.6 | -0.047 | 0.91 | 5.6R | +0.07 / -0.33 | +0.22 / -0.37 | 1/5 ✗ | -0.08 | -0.11 | ✗  time_stop_bars 40→32: -0.07R | 1 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 153 / 6 of 160 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; only 9 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 2952 | 32.3 | -0.048 | 0.92 | 232.5R | -0.08 / +0.02 | -0.03 / -0.07 | 2/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.09R | 34, +0.36 (+0.42 / +0.10) | 215 / 120 of 569 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 232.5R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 167 | 49.7 | -0.050 | 0.91 | 29.8R | -0.17 / +0.21 | -0.09 / -0.01 | 2/5 ✗ | -0.11 | -0.18 | ✗  stop atr 1.5→1.2: -0.14R | 3 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 218 / 5 of 226 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 29.8R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1199 | 49.8 | -0.051 | 0.9 | 91.4R | -0.06 / -0.03 | -0.02 / -0.08 | 1/5 ✗ | -0.13 | -0.20 | ✗  stop atr 2.0→1.6: -0.13R | 3 | 0.12R | 51, -0.06 (+0.02 / -0.37) | 153 / 38 of 372 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.90; max drawdown 91.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2599 | 32.1 | -0.054 | 0.92 | 214.7R | -0.09 / +0.03 | -0.04 / -0.07 | 1/5 ✗ | -0.10 | -0.15 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 31, +0.33 (+0.41 / -0.19) | 130 / 88 of 417 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 214.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FAILED** | 2599 | 32.1 | -0.054 | 0.92 | 215.6R | -0.09 / +0.03 | -0.04 / -0.07 | 1/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 31, +0.33 (+0.41 / -0.19) | 130 / 88 of 417 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 215.6R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2669 | 48.1 | -0.060 | 0.89 | 188.0R | -0.07 / -0.03 | -0.07 / -0.05 | 0/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.07R | 1 | 0.09R | 32, +0.23 (+0.31 / -0.34) | 130 / 88 of 417 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 188.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1063 | 48.4 | -0.065 | 0.88 | 115.0R | -0.01 / -0.18 | -0.01 / -0.13 | 1/5 ✗ | -0.11 | -0.14 | ✗  long_rsi_hi 65→52: -0.14R | 3 | 0.06R | 10, +0.53 (+1.14 / -0.39) | 635 / 193 of 986 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 115.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 83 | 47.0 | -0.093 | 0.83 | 16.4R | +0.05 / -0.34 | -0.10 / -0.08 | 3/5 ✗ | -0.12 | -0.14 | ✗  time_stop_bars 60→48: -0.09R | 1 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 42 / 6 of 50 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.83; max drawdown 16.4R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1612 | 55.8 | -0.111 | 0.62 | 179.7R | -0.10 / -0.13 | -0.13 / -0.09 | 0/5 ✗ | -0.14 | -0.17 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.05R | 6, -0.31 (-0.35 / -0.13) | 764 / 4 of 1015 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.62; max drawdown 179.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 310 | 44.2 | -0.115 | 0.79 | 47.9R | -0.13 / -0.09 | -0.18 / -0.04 | 0/5 ✗ | -0.18 | -0.26 | ✗  slow 21→17: -0.20R | 3 | 0.12R | 4, -0.30 (-1.00 / +1.82) | 151 / 9 of 170 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.79; max drawdown 47.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 6112 | 53.6 | -0.132 | 0.54 | 811.5R | -0.11 / -0.18 | -0.14 / -0.12 | 0/5 ✗ | -0.20 | -0.27 | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 46, -0.15 (-0.19 / -0.11) | 1052 / 5 of 1407 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.54; max drawdown 811.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 255 | 33.3 | -0.138 | 0.82 | 53.6R | -0.02 / -0.41 | -0.37 / +0.12 | 1/5 ✗ | -0.24 | -0.35 | ✗  time_stop_bars 30→36: -0.17R | 1 | 0.20R | 3, +0.86 (+0.00 / +0.86) | 86 / 231 of 328 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.82; max drawdown 53.6R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 5541 | 47.3 | -0.139 | 0.76 | 778.8R | -0.14 / -0.13 | -0.17 / -0.10 | 0/5 ✗ | -0.21 | -0.28 | ✗  stop atr 1.5→1.2: -0.18R | 1 | 0.13R | 52, +0.01 (+0.09 / -0.23) | 1167 / 284 of 1861 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 778.8R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 85 | 36.5 | -0.147 | 0.79 | 22.0R | -0.32 / +0.32 | -0.20 / -0.12 | 1/5 ✗ | -0.21 | -0.31 | ✗  depth 0.985→1.182: -0.45R | 2 | 0.15R | 2, +1.30 (+1.30 / +0.00) | 43 / 6 of 51 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.79; max drawdown 22.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 412 | 45.4 | -0.155 | 0.74 | 65.3R | -0.14 / -0.20 | -0.23 / -0.12 | 1/5 ✗ | -0.30 | -0.43 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.25R | 21, -0.28 (-0.04 / -1.06) | 73 / 16 of 113 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.74; max drawdown 65.3R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 41 | 36.6 | -0.161 | 0.77 | 11.3R | +0.11 / -0.50 | -0.40 / +0.06 | 1/5 ✗ | -0.33 | -0.41 | ✗  stop buffer_atr 0.2→0.16: -0.16R | 3 | 0.15R | 7, -0.82 (-0.59 / -1.40) | 99 / 33 of 148 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.77; max drawdown 11.3R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 235 | 38.7 | -0.165 | 0.75 | 59.0R | -0.18 / -0.12 | +0.12 / -0.35 | 1/5 ✗ | -0.21 | -0.27 | ✗  depth 0.985→1.182: -0.29R | 1 | 0.10R | 6, +0.61 (+0.86 / +0.36) | 86 / 6 of 108 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.75; max drawdown 59.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 147 | 46.9 | -0.174 | 0.69 | 26.0R | -0.18 / -0.15 | -0.14 / -0.20 | 2/5 ✗ | -0.24 | -0.33 | ✗  adx_min 20→24: -0.25R | 1 | 0.13R | 7, -0.82 (-0.74 / -1.26) | 60 / 6 of 76 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.69; max drawdown 26.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 461 | 46.9 | -0.180 | 0.71 | 84.7R | -0.23 / -0.05 | -0.24 / -0.12 | 1/5 ✗ | -0.29 | -0.41 | ✗  stop atr 1.5→1.2: -0.25R | 1 | 0.18R | 20, -0.41 (-0.35 / -0.53) | 128 / 40 of 216 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.71; max drawdown 84.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3200 | 46.2 | -0.195 | 0.68 | 630.5R | -0.18 / -0.23 | -0.22 / -0.17 | 0/5 ✗ | -0.31 | -0.42 | ✗  stop atr 1.5→1.2: -0.26R | 0 | 0.18R | 102, -0.01 (+0.25 / -0.55) | 848 / 220 of 1681 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 630.5R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2514 | 46.8 | -0.198 | 0.4 | 498.6R | -0.18 / -0.24 | -0.25 / -0.15 | 0/5 ✗ | -0.30 | -0.41 | ✗  hi 90→108: -0.25R | 0 | 0.17R | 36, -0.04 (-0.09 / +0.01) | 1071 / 22 of 1287 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.40; max drawdown 498.6R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 268 | 47.4 | -0.208 | 0.66 | 62.1R | -0.13 / -0.41 | -0.35 / -0.08 | 0/5 ✗ | -0.33 | -0.42 | ✗  stop atr 1.5→1.2: -0.29R | 1 | 0.19R | 6, -0.48 (-0.10 / -1.24) | 189 / 9 of 215 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.66; max drawdown 62.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 273 | 47.6 | -0.211 | 0.65 | 58.6R | -0.22 / -0.20 | -0.23 / -0.19 | 0/5 ✗ | -0.29 | -0.38 | ✗  vol_x 1.2→1.44: -0.36R | 2 | 0.17R | 5, -0.43 (-0.23 / -1.20) | 109 / 199 of 318 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.65; max drawdown 58.6R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 300 | 40.7 | -0.219 | 0.63 | 69.5R | -0.20 / -0.29 | -0.29 / -0.16 | 1/5 ✗ | -0.32 | -0.41 | ✗  fast 9→11: -0.30R | 0 | 0.17R | 8, +0.04 (+0.04 / +0.00) | 113 / 17 of 144 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.63; max drawdown 69.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 718 | 30.8 | -0.221 | 0.73 | 183.8R | -0.22 / -0.23 | -0.31 / -0.14 | 1/5 ✗ | -0.33 | -0.43 | ✗  stop buffer_atr 0.2→0.16: -0.26R | 1 | 0.22R | 18, -0.45 (-0.21 / -0.74) | 482 / 1160 of 1738 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.73; max drawdown 183.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 249 | 43.4 | -0.239 | 0.61 | 63.0R | -0.26 / -0.20 | -0.34 / -0.14 | 0/5 ✗ | -0.30 | -0.35 | ✗  st_n 10→12: -0.25R | 1 | 0.08R | 4, +0.17 (+0.17 / +0.00) | 56 / 2 of 66 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.61; max drawdown 63.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 2822 | 44.7 | -0.258 | 0.61 | 733.4R | -0.24 / -0.31 | -0.30 / -0.24 | 0/5 ✗ | -0.41 | -0.57 | ✗  stop atr 1.5→1.2: -0.34R | 0 | 0.25R | 205, -0.19 (-0.03 / -0.69) | 1291 / 295 of 2264 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 733.4R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1123 | 29.6 | -0.308 | 0.61 | 347.5R | -0.33 / -0.26 | -0.31 / -0.31 | 0/5 ✗ | -0.39 | -0.46 | ✗  rsi_n 14→17: -0.38R | 1 | 0.14R | 7, +0.14 (-0.03 / +0.54) | 755 / 6 of 803 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.61; max drawdown 347.5R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1364 | 31.7 | -0.313 | 0.61 | 433.6R | -0.32 / -0.30 | -0.31 / -0.31 | 0/5 ✗ | -0.44 | -0.57 | ✗  stop atr 1.5→1.2: -0.35R | 0 | 0.21R | 29, -0.13 (+0.01 / -0.32) | 595 / 27 of 717 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.61; max drawdown 433.6R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 1952 | 35.0 | -0.325 | 0.22 | 636.0R | -0.31 / -0.36 | -0.42 / -0.25 | 0/5 ✗ | -0.49 | -0.67 | ✗  hi 90→108: -0.42R | 0 | 0.28R | 63, -0.20 (-0.14 / -0.39) | 1285 / 36 of 1426 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.33R/trade (needs +0.10R); profit factor 0.22; max drawdown 636.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 524 | 41.6 | -0.350 | 0.51 | 191.5R | -0.32 / -0.42 | -0.32 / -0.37 | 0/5 ✗ | -0.50 | -0.64 | ✗  stop atr 1.5→1.2: -0.42R | 0 | 0.28R | 40, -0.74 (-0.78 / -0.60) | 88 / 37 of 184 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.35R/trade (needs +0.10R); profit factor 0.51; max drawdown 191.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 559 | 24.9 | -0.461 | 0.53 | 266.0R | -0.48 / -0.41 | -0.56 / -0.36 | 1/5 ✗ | -0.63 | -0.76 | ✗  n 20→24: -0.51R | 1 | 0.33R | 28, -0.07 (+0.17 / -0.46) | 472 / 1054 of 1736 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.53; max drawdown 266.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 525 | 39.2 | -0.476 | 0.4 | 250.2R | -0.45 / -0.57 | -0.57 / -0.42 | 0/5 ✗ | -0.68 | -0.92 | ✗  stop atr 1.0→0.8: -0.54R | 0 | 0.37R | 41, -0.57 (-0.63 / -0.49) | 104 / 245 of 392 | 0 | not cost-viable: fees + slippage 0.37R per trade (stop must be ≥ 4x the round-trip cost); avg -0.48R/trade (needs +0.10R); profit factor 0.40; max drawdown 250.2R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 103 | 20.4 | -0.481 | 0.51 | 56.1R | -0.40 / -0.65 | -0.56 / -0.40 | 0/5 ✗ | -0.63 | -0.77 | ✗  stop max_width_atr 3.0→2.4: -0.48R | 1 | 0.25R | 6, -0.04 (-1.25 / +0.56) | 31 / 103 of 147 | 0 | avg -0.48R/trade (needs +0.10R); profit factor 0.51; max drawdown 56.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 297 | 35.7 | -0.510 | 0.35 | 151.5R | -0.49 / -0.57 | -0.51 / -0.51 | 0/5 ✗ | -0.66 | -0.81 | ✗  stop atr 1.0→0.8: -0.56R | 0 | 0.28R | 15, -0.81 (-0.44 / -1.23) | 115 / 220 of 367 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.51R/trade (needs +0.10R); profit factor 0.35; max drawdown 151.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 266 | 30.5 | -0.711 | 0.25 | 189.2R | -0.78 / -0.60 | -0.68 / -0.92 | 0/5 ✗ | -1.07 | -1.42 | ✗  stop atr 1.5→1.2: -0.91R | 0 | 0.54R | 81, -0.55 (-0.59 / -0.43) | 209 / 59 of 349 | 0 | not cost-viable: fees + slippage 0.54R per trade (stop must be ≥ 4x the round-trip cost); avg -0.71R/trade (needs +0.10R); profit factor 0.25; max drawdown 189.2R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 426 | 25.4 | -1.188 | 0.15 | 505.9R | -1.24 / -1.13 | -1.08 / -1.96 | 0/5 ✗ | -1.85 | -2.51 | ✗  stop atr 1.0→0.8: -1.51R | 0 | 1.05R | 149, -1.14 (-1.18 / -1.07) | 227 / 606 of 987 | 0 | not cost-viable: fees + slippage 1.05R per trade (stop must be ≥ 4x the round-trip cost); avg -1.19R/trade (needs +0.10R); profit factor 0.15; max drawdown 505.9R; not profitable in BOTH train and unseen test |

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
| `memory/changelog.md` | 104.8 KB | - | - |
| `memory/coin_notes.md` | 6.8 KB | 7 | 2026-09-27 00:26 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 5.3 KB | 11 | 2026-09-28 11:19 UTC |
| `memory/experiments.md` | 48.1 KB | 19 | 2026-09-28 15:40 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 38.2 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 5.9 KB | - | - |
| `memory/missed_trades.md` | 11.3 KB | 14 | 2026-09-28 00:52 UTC |
| `memory/playbook.md` | 8.7 KB | - | - |
| `memory/research_sources.md` | 59.7 KB | 45 | 2026-09-28 15:40 UTC |
| `memory/smc_events.csv` | 282.8 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 15.8 KB | - | - |
| `memory/strategy_registry.csv` | 36.7 KB | - | - |
| `memory/trials.csv` | 9.2 KB | - | - |
| `memory/universe_log.md` | 8.7 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*