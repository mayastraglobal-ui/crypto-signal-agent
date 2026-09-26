# Crypto Signal Report

**Updated:** 2026-09-27 03:16 Beijing time (2026-09-26 19:16 UTC) · data: Binance · 8 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 5.8 MB (GitHub) · large files of this run 2.4 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-26 19:16 UTC / 2026-09-27 03:16 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US PCE / Personal Income and Outlays (Aug data) 2026-09-30 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.04% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| BABY | **DEGRADED** | 1d: DEGRADED: volume 65x normal on candle 09-23 00:00 UTC (possible bad data); 1d: DEGRADED: volume 67x normal on candle 09-25 00:00 UTC (possible bad data) |
- 58 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-26 19:15 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 749 h since 2026-08-26 | -0.0006% | 1.32 | 0.89 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 749 h since 2026-08-26 | +0.0018% | 1.36 | 1.18 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 749 h since 2026-08-26 | +0.0066% | 1.43 | 0.79 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 749 h since 2026-08-26 | +0.0100% | 2.50 | 0.53 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 749 h since 2026-08-26 | +0.0022% | 0.54 | 1.06 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 749 h since 2026-08-26 | +0.0087% | 1.88 | 0.57 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| ENA | GOOD | okx | 749 h since 2026-08-26 | +0.0060% | 1.01 | 1.60 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ENAUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 749 h since 2026-08-26 | +0.0100% | 1.83 | 1.47 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |
| LTC | GOOD | okx | 749 h since 2026-08-26 | +0.0092% | 2.28 | 1.03 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=LTCUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **XRP**, **ZEC**, **SUI**, **ENA**
- **Research only** - backtested, never a signal: UNI
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** BABY - 7-day average volume $25M < $50M; order book too thin: $48k within 1% (need $250k)

| Not eligible | 24h volume | Why |
|---|---|---|
| BABY | $51M | 7-day average volume $25M < $50M; order book too thin: $48k within 1% (need $250k) |

**Flags (not excluded):** BABY: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, TAO, USD1, USDC, WLD (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 475 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ETH | 475 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| SOL | 319 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| XRP | 438 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| ZEC | 392 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| SUI | 177 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| ENA | 129 | 907 | 901 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |
| UNI | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | up (HH/HL) | 84,337 / 83,856.2 | 0.05 | 1.24x | 0.47x | bear_engulf, bull_reject |
| ETH | mixed (LH/HL) | 2,696 / 2,682 | 0.19 | 0.53x | 0.47x | bull_reject |
| SOL | down (LH/LL) | 122.1 / 119.82 | 0.29 | 0.77x | 0.85x | bull_reject |
| XRP | mixed (LH/HL) | 1.5541 / 1.5371 | 0.14 | 1.82x | 0.60x | breakout_down, retest_down |
| ZEC | down (LH/LL) | 1,540.22 / 1,517.41 | 0.10 | 2.83x | 0.62x | bear_reject, breakout_up, retest_up |
| SUI | mixed (LH/HL) | 1.1925 / 1.155 | 0.04 | 0.49x | 0.94x | bear_engulf, bull_reject |
| ENA | up (HH/HL) | 0.2857 / 0.2632 | 0.66 | 0.29x | 1.10x | - |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 390 | 50% | 35% | 28% | 78% | 44% | 32% | beats chance | 0.11R |
| 4h | displacement_down | 295 | 49% | 34% | 22% | 74% | 46% | 31% | can't tell from chance | 0.07R |
| 4h | bull_engulf | 974 | 44% | 31% | 22% | 78% | 44% | 30% | can't tell from chance | 0.12R |
| 4h | bear_engulf | 1082 | 45% | 30% | 21% | 76% | 48% | 32% | can't tell from chance | 0.07R |
| 4h | bull_reject | 731 | 42% | 29% | 21% | 79% | 43% | 30% | can't tell from chance | 0.12R |
| 4h | bear_reject | 745 | 47% | 33% | 23% | 73% | 48% | 32% | can't tell from chance | 0.07R |
| 4h | smc_sweep_bull | 530 | 42% | 28% | 21% | 78% | 43% | 29% | can't tell from chance | 0.11R |
| 4h | smc_sweep_bear | 527 | 42% | 28% | 17% | 80% | 49% | 32% | worse than chance | 0.07R |
| 4h | smc_bos_up | 229 | 46% | 31% | 23% | 81% | 46% | 32% | can't tell from chance | 0.12R |
| 4h | smc_bos_down | 202 | 52% | 40% | 27% | 66% | 47% | 32% | can't tell from chance | 0.07R |
| 4h | smc_choch_up | 70 | 51% | 33% | 29% | 80% | 45% | 31% | can't tell from chance | 0.11R |
| 4h | smc_choch_down | 63 | 41% | 25% | 13% | 76% | 49% | 32% | can't tell from chance | 0.07R |
| 4h | smc_fvg_retrace_bull | 522 | 44% | 29% | 23% | 76% | 43% | 29% | can't tell from chance | 0.11R |
| 4h | smc_fvg_retrace_bear | 543 | 48% | 33% | 21% | 74% | 48% | 32% | can't tell from chance | 0.07R |
| 1h | displacement_up | 513 | 47% | 34% | 28% | 73% | 43% | 30% | can't tell from chance | 0.24R |
| 1h | displacement_down | 348 | 39% | 24% | 15% | 81% | 40% | 26% | can't tell from chance | 0.16R |
| 1h | bull_engulf | 1377 | 40% | 28% | 22% | 75% | 42% | 29% | can't tell from chance | 0.29R |
| 1h | bear_engulf | 1468 | 40% | 25% | 17% | 79% | 39% | 25% | can't tell from chance | 0.18R |
| 1h | bull_reject | 1123 | 41% | 29% | 22% | 75% | 43% | 30% | can't tell from chance | 0.28R |
| 1h | bear_reject | 1125 | 37% | 24% | 17% | 82% | 39% | 25% | can't tell from chance | 0.16R |
| 1h | smc_sweep_bull | 505 | 42% | 28% | 20% | 76% | 42% | 29% | can't tell from chance | 0.27R |
| 1h | smc_sweep_bear | 591 | 38% | 24% | 15% | 81% | 39% | 25% | can't tell from chance | 0.16R |
| 1h | smc_bos_up | 327 | 45% | 31% | 25% | 78% | 44% | 30% | can't tell from chance | 0.22R |
| 1h | smc_bos_down | 220 | 37% | 27% | 18% | 83% | 38% | 24% | can't tell from chance | 0.20R |
| 1h | smc_choch_up | 97 | 48% | 37% | 33% | 69% | 42% | 29% | can't tell from chance | 0.31R |
| 1h | smc_choch_down | 97 | 46% | 30% | 16% | 74% | 39% | 24% | can't tell from chance | 0.16R |
| 1h | smc_fvg_retrace_bull | 700 | 45% | 33% | 26% | 70% | 42% | 30% | can't tell from chance | 0.26R |
| 1h | smc_fvg_retrace_bear | 648 | 42% | 29% | 19% | 78% | 40% | 25% | can't tell from chance | 0.18R |
| 30m | displacement_up | 521 | 43% | 32% | 26% | 76% | 44% | 31% | can't tell from chance | 0.26R |
| 30m | displacement_down | 330 | 42% | 25% | 14% | 82% | 37% | 21% | can't tell from chance | 0.15R |
| 30m | bull_engulf | 1403 | 42% | 29% | 22% | 75% | 43% | 30% | can't tell from chance | 0.31R |
| 30m | bear_engulf | 1400 | 37% | 21% | 14% | 82% | 36% | 21% | can't tell from chance | 0.18R |
| 30m | bull_reject | 1053 | 47% | 31% | 23% | 72% | 43% | 30% | beats chance | 0.29R |
| 30m | bear_reject | 1142 | 37% | 23% | 15% | 82% | 37% | 21% | can't tell from chance | 0.18R |
| 30m | smc_sweep_bull | 505 | 42% | 29% | 19% | 74% | 41% | 29% | can't tell from chance | 0.30R |
| 30m | smc_sweep_bear | 519 | 43% | 28% | 18% | 81% | 37% | 21% | beats chance | 0.18R |
| 30m | smc_bos_up | 387 | 43% | 34% | 28% | 75% | 43% | 30% | can't tell from chance | 0.28R |
| 30m | smc_bos_down | 178 | 37% | 22% | 11% | 85% | 36% | 21% | can't tell from chance | 0.21R |
| 30m | smc_choch_up | 82 | 38% | 22% | 17% | 84% | 44% | 31% | can't tell from chance | 0.32R |
| 30m | smc_choch_down | 81 | 41% | 22% | 16% | 80% | 39% | 22% | can't tell from chance | 0.14R |
| 30m | smc_fvg_retrace_bull | 773 | 44% | 30% | 23% | 73% | 43% | 30% | can't tell from chance | 0.29R |
| 30m | smc_fvg_retrace_bear | 629 | 38% | 22% | 16% | 82% | 37% | 21% | can't tell from chance | 0.20R |
| 15m | displacement_up | 368 | 36% | 27% | 20% | 82% | 37% | 25% | can't tell from chance | 0.34R |
| 15m | displacement_down | 367 | 35% | 20% | 13% | 85% | 37% | 24% | can't tell from chance | 0.25R |
| 15m | bull_engulf | 1317 | 38% | 27% | 19% | 78% | 36% | 25% | can't tell from chance | 0.44R |
| 15m | bear_engulf | 1285 | 36% | 24% | 15% | 79% | 37% | 23% | can't tell from chance | 0.25R |
| 15m | bull_reject | 1053 | 35% | 23% | 15% | 80% | 36% | 25% | can't tell from chance | 0.44R |
| 15m | bear_reject | 1119 | 35% | 22% | 15% | 81% | 37% | 23% | can't tell from chance | 0.25R |
| 15m | smc_sweep_bull | 478 | 37% | 24% | 20% | 78% | 36% | 25% | can't tell from chance | 0.41R |
| 15m | smc_sweep_bear | 520 | 38% | 26% | 14% | 82% | 37% | 23% | can't tell from chance | 0.24R |
| 15m | smc_bos_up | 279 | 39% | 29% | 22% | 81% | 37% | 25% | can't tell from chance | 0.32R |
| 15m | smc_bos_down | 295 | 33% | 18% | 13% | 85% | 38% | 23% | can't tell from chance | 0.29R |
| 15m | smc_choch_up | 73 | 32% | 25% | 18% | 82% | 39% | 27% | can't tell from chance | 0.41R |
| 15m | smc_choch_down | 73 | 36% | 22% | 14% | 81% | 37% | 25% | can't tell from chance | 0.27R |
| 15m | smc_fvg_retrace_bull | 802 | 34% | 25% | 17% | 81% | 36% | 25% | can't tell from chance | 0.42R |
| 15m | smc_fvg_retrace_bear | 764 | 38% | 26% | 18% | 79% | 37% | 22% | can't tell from chance | 0.26R |
| 5m | displacement_up | 964 | 32% | 21% | 16% | 84% | 29% | 20% | beats chance | 0.68R |
| 5m | displacement_down | 922 | 28% | 17% | 12% | 86% | 31% | 21% | worse than chance | 0.45R |
| 5m | bull_engulf | 3356 | 27% | 18% | 13% | 83% | 29% | 20% | worse than chance | 0.77R |
| 5m | bear_engulf | 3302 | 32% | 22% | 14% | 82% | 32% | 21% | can't tell from chance | 0.48R |
| 5m | bull_reject | 2753 | 27% | 18% | 13% | 82% | 28% | 20% | can't tell from chance | 0.81R |
| 5m | bear_reject | 2988 | 33% | 22% | 15% | 81% | 32% | 21% | can't tell from chance | 0.45R |
| 5m | smc_sweep_bull | 978 | 31% | 22% | 15% | 79% | 29% | 20% | can't tell from chance | 0.70R |
| 5m | smc_sweep_bear | 1031 | 35% | 25% | 17% | 81% | 34% | 22% | can't tell from chance | 0.39R |
| 5m | smc_bos_up | 632 | 31% | 22% | 18% | 85% | 29% | 20% | can't tell from chance | 0.67R |
| 5m | smc_bos_down | 713 | 28% | 19% | 11% | 87% | 32% | 21% | can't tell from chance | 0.51R |
| 5m | smc_choch_up | 177 | 36% | 27% | 18% | 85% | 27% | 19% | beats chance | 0.80R |
| 5m | smc_choch_down | 182 | 26% | 15% | 11% | 87% | 31% | 21% | can't tell from chance | 0.49R |
| 5m | smc_fvg_retrace_bull | 2572 | 30% | 21% | 15% | 81% | 28% | 19% | beats chance | 0.77R |
| 5m | smc_fvg_retrace_bear | 2305 | 29% | 19% | 12% | 83% | 32% | 21% | worse than chance | 0.47R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (weak) | WEAK_BULL (moderate) | WEAK_BULL (weak) | COMPRESSION (moderate) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ETH** | UNCLEAR (weak) | WEAK_BULL (moderate) | RANGE (weak) | COMPRESSION (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H COMPRESSION)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (weak) | STRONG_BULL (moderate) | TRANSITION (weak) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | TRANSITION (weak) | RANGE (strong) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H RANGE)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | COMPRESSION (weak) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |
| **SUI** | RANGE (weak) | EXPANSION up (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | LONG allowed (1D/4H/1H bullish, 1W RANGE) |
| **ENA** | TRANSITION (weak) | WEAK_BULL (weak) | STRONG_BULL (moderate) | STRONG_BULL (moderate) | LONG allowed (1D/4H/1H bullish, 1W TRANSITION) |
| **UNI** | EXPANSION up (weak) | STRONG_BULL (moderate) | TRANSITION (weak) | COMPRESSION (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H TRANSITION, 1H COMPRESSION)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (weak)** - for: EMA-fast rising (+1.1 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.72x normal, Bollinger width above 52% of the last 100 candles · against: EMAs not lined up; ADX 27 is close to a threshold
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.2 ATR in 10 candles); ADX 44 = strong trend; candle size 1.15x normal, Bollinger width above 80% of the last 100 candles; volume 1.48x normal · against: swing structure mixed (neutral)
- **4H WEAK_BULL (weak)** - for: close above EMA-fast above EMA-slow; swing structure up (HH/HL); candle size 0.93x normal, Bollinger width above 7% of the last 100 candles · against: EMA-fast flat (+0.6 ATR in 10 candles) (neutral); ADX 16 = weak trend / ranging; volume only 0.40x normal (weak participation)
- **1H COMPRESSION (moderate)** - for: EMAs not lined up; EMA-fast flat (-0.2 ATR in 10 candles); ADX 14 = weak trend / ranging; candle size 0.47x normal, Bollinger width above 1% of the last 100 candles · against: swing structure up (HH/HL)

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | up (BOS 42 candles ago) | sell-side (bullish idea) 24 candles ago | bear 84,020.76-84,063.18 (retraced) | bear 86,133.40-86,975.51 | discount (30%) | swing high 84,336.96 (1.45 ATR) | equal lows 83,848.91 (0.64 ATR) |
| **ETH** | down (BOS 2 candles ago) | buy-side (bearish idea) 30 candles ago | bear 2,685.41-2,687.58 (retraced) | bear 2,745.99-2,784.40 | discount (22%) | swing high 2,696.00 (1.14 ATR) | swing low 2,682.00 (0.31 ATR) |
| **SOL** | up (BOS 15 candles ago) | sell-side (bullish idea) 1 candles ago | bull 120.04-120.28 (retraced) | bull 115.86-117.34 | premium (54%) | swing high 122.10 (1.07 ATR) | swing low 119.82 (1.28 ATR) |
| **XRP** | down (CHOCH 2 candles ago) | sell-side (bullish idea) 1 candles ago | bear 1.5241-1.5344 (retraced) | bull 1.3773-1.3856 | below the range (-94%) | swing high 1.5541 (2.41 ATR) | swing low 1.5191 (0.15 ATR) |
| **ZEC** | down (BOS 40 candles ago) | buy-side (bearish idea) 2 candles ago | bull 1,542.93-1,545.92 | bull 1,098.88-1,133.82 | above the range (193%) | swing high 1,625.00 (3.62 ATR) | swing low 1,517.41 (2.51 ATR) |
| **SUI** | up (BOS 13 candles ago) | buy-side (bearish idea) 15 candles ago | bear 1.1649-1.1717 (retraced) | bull 1.0050-1.0598 | discount (6%) | swing high 1.1925 (1.87 ATR) | swing low 1.1550 (0.12 ATR) |
| **ENA** | up (BOS 35 candles ago) | sell-side (bullish idea) 10 candles ago | bull 0.25770-0.25950 (retraced) | bull 0.16130-0.17050 | discount (39%) | swing high 0.28570 (2.14 ATR) | swing low 0.26320 (1.35 ATR) |

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

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.839 | 2.51 | 2.3R | +0.56 / +2.21 | +2.21 / +0.56 | 0/5 ✗ | +0.73 | - | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 18 / 12 of 31 | 0 | only 6 trades; only 1 unseen-test trades |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 16 | 43.8 | +0.250 | 1.33 | 4.5R | +0.11 / +0.56 | +0.18 / +0.29 | 0/5 ✗ | -0.05 | - | ✗  sweep_bars 8→10: -0.13R | 0 | 0.26R | 1, -1.32 (+0.00 / -1.32) | 35 / 24 of 64 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 16 trades; only 5 unseen-test trades |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1105 | 54.5 | +0.123 | 1.28 | 22.5R | +0.11 / +0.15 | +0.11 / +0.14 | 5/5 | +0.09 | - | stable | 8 | 0.04R | 11, +0.39 (+0.54 / -1.03) | 75 / 36 of 214 | 0 | max drawdown 22.5R |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 8 | 50.0 | +0.108 | 1.13 | 3.3R | +0.31 / -1.32 | -1.32 / +0.31 | 0/5 ✗ | -0.00 | - | ✗  sweep_bars 20→24: -0.16R | 0 | 0.21R | 1, -1.32 (+0.00 / -1.32) | 26 / 9 of 42 | 0 | only 8 trades; profit factor 1.13; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | - | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 1 of 2 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | - | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 48 / 13 of 64 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | - | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 26 / 9 of 42 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | - | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 1 of 2 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | - | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 18 / 12 of 31 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 18 | 50.0 | -0.001 | 1.0 | 4.9R | +0.08 / -0.41 | -0.31 / +0.09 | 1/5 ✗ | +0.12 | - | ✗  stop max_width_atr 3.0→3.6: -0.09R | 1 | 0.16R | 1, +1.21 (+1.21 / +0.00) | 336 / 180 of 628 | 0 | only 18 trades; avg -0.00R/trade (needs +0.10R); profit factor 1.00; only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 13 | 23.1 | -0.340 | 0.44 | 4.4R | -0.40 / -0.27 | -1.11 / -0.20 | 0/5 ✗ | -0.45 | - | ✗  stop buffer_atr 0.2→0.24: -0.35R | 0 | 0.09R | 0, +0.00 (+0.00 / +0.00) | 420 / 150 of 717 | 0 | only 13 trades; avg -0.34R/trade (needs +0.10R); profit factor 0.44; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 4 | 0.0 | -1.218 | 0.0 | 4.9R | -1.24 / -1.16 | -1.42 / -1.15 | 0/5 ✗ | -1.22 | - | ✗  sweep_bars 20→16: -1.22R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 48 / 13 of 64 | 0 | only 4 trades; avg -1.22R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.712 | 0.0 | 1.7R | +0.00 / -1.71 | -1.71 / +0.00 | 0/5 ✗ | -2.00 | - | ✗  stop buffer_atr 0.2→0.16: -1.75R | 0 | 0.86R | 0, +0.00 (+0.00 / +0.00) | 24 / 80 of 114 | 0 | not cost-viable: fees + slippage 0.86R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.71R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 9, -0.38 (-0.47 / +0.40) | 620 / 4 of 661 | 0 | waiting for the first daily research run (Layers B/C) |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 26, -0.22 (-0.48 / +0.48) | 518 / 12 of 600 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 9, +0.87 (+0.87 / +0.00) | 75 / 36 of 214 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 26, +0.31 (+0.50 / -0.20) | 103 / 68 of 335 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 42, +0.06 (+0.33 / -0.55) | 106 / 30 of 320 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 277 | 51.6 | +0.025 | 1.05 | 26.5R | +0.19 / -0.27 | +0.13 / -0.07 | 2/5 ✗ | -0.03 | - | ✗  stop atr 1.5→1.8: -0.02R | 6 | 0.07R | 2, +0.08 (-1.11 / +1.27) | 84 / 20 of 117 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.05; max drawdown 26.5R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 832 | 53.4 | -0.010 | 0.98 | 38.5R | -0.01 / +0.00 | -0.07 / +0.04 | 2/5 ✗ | -0.09 | - | ✗  bb_k 2→1: -0.05R | 4 | 0.14R | 2, +1.05 (+0.00 / +1.05) | 109 / 33 of 174 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 38.5R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 3064 | 48.9 | -0.046 | 0.91 | 173.9R | -0.06 / -0.02 | -0.06 / -0.03 | 0/5 ✗ | -0.09 | - | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.09R | 27, +0.22 (+0.27 / +0.08) | 103 / 68 of 335 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 173.9R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 92 | 47.8 | -0.057 | 0.89 | 15.1R | +0.07 / -0.29 | -0.09 / -0.02 | 2/5 ✗ | -0.08 | - | ✗  time_stop_bars 60→48: -0.06R | 2 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 33 / 5 of 40 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 15.1R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 38 | 50.0 | -0.063 | 0.88 | 5.6R | +0.10 / -0.46 | +0.20 / -0.33 | 2/5 ✗ | -0.10 | - | ✗  stop atr 1.5→1.8: -0.08R | 1 | 0.07R | 0, +0.00 (+0.00 / +0.00) | 117 / 5 of 123 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.88; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1329 | 48.5 | -0.067 | 0.88 | 114.7R | -0.08 / -0.04 | -0.03 / -0.11 | 1/5 ✗ | -0.14 | - | ✗  stop atr 2.0→1.6: -0.14R | 3 | 0.12R | 42, +0.01 (+0.13 / -0.25) | 106 / 30 of 320 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 114.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1218 | 47.9 | -0.068 | 0.88 | 129.2R | -0.03 / -0.14 | -0.01 / -0.13 | 1/5 ✗ | -0.11 | - | ✗  long_rsi_hi 65→52: -0.14R | 3 | 0.06R | 5, +1.14 (+1.10 / +1.27) | 512 / 163 of 802 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 129.2R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 186 | 48.4 | -0.088 | 0.84 | 34.0R | -0.20 / +0.15 | -0.11 / -0.07 | 2/5 ✗ | -0.15 | - | ✗  stop atr 1.5→1.2: -0.15R | 3 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 178 / 4 of 184 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.84; max drawdown 34.0R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1841 | 55.9 | -0.107 | 0.63 | 197.3R | -0.10 / -0.11 | -0.13 / -0.09 | 0/5 ✗ | -0.14 | - | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.05R | 6, -0.17 (-0.17 / +0.00) | 624 / 4 of 830 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.63; max drawdown 197.3R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 283 | 33.2 | -0.125 | 0.84 | 64.3R | -0.04 / -0.31 | -0.38 / +0.14 | 1/5 ✗ | -0.23 | - | ✗  time_stop_bars 30→36: -0.15R | 1 | 0.19R | 1, +2.70 (+0.00 / +2.70) | 75 / 175 of 259 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.84; max drawdown 64.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 6989 | 53.6 | -0.129 | 0.54 | 906.7R | -0.11 / -0.17 | -0.14 / -0.12 | 0/5 ✗ | -0.19 | - | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 35, -0.15 (-0.31 / +0.09) | 828 / 1 of 1117 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.54; max drawdown 906.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 335 | 43.6 | -0.134 | 0.76 | 56.3R | -0.15 / -0.10 | -0.21 / -0.05 | 0/5 ✗ | -0.20 | - | ✗  slow 21→17: -0.22R | 3 | 0.12R | 3, -1.00 (-1.25 / -0.52) | 113 / 6 of 127 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.76; max drawdown 56.3R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6338 | 47.2 | -0.138 | 0.76 | 900.0R | -0.14 / -0.13 | -0.18 / -0.10 | 0/5 ✗ | -0.21 | - | ✗  stop atr 1.5→1.2: -0.18R | 1 | 0.13R | 37, +0.04 (-0.09 / +0.25) | 917 / 218 of 1454 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 900.0R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 41 | 36.6 | -0.149 | 0.78 | 10.8R | +0.05 / -0.44 | -0.28 / -0.04 | 1/5 ✗ | -0.31 | - | ✗  stop buffer_atr 0.2→0.16: -0.15R | 3 | 0.15R | 7, -0.41 (+0.17 / -0.64) | 80 / 25 of 118 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.78; max drawdown 10.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 163 | 47.9 | -0.162 | 0.7 | 26.9R | -0.18 / -0.10 | -0.16 / -0.17 | 2/5 ✗ | -0.23 | - | ✗  adx_min 20→24: -0.21R | 1 | 0.13R | 5, -0.93 (-0.85 / -1.26) | 44 / 3 of 55 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.70; max drawdown 26.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 457 | 44.4 | -0.164 | 0.73 | 77.7R | -0.15 / -0.21 | -0.25 / -0.13 | 0/5 ✗ | -0.30 | - | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.25R | 17, +0.12 (+0.33 / -0.86) | 49 / 11 of 80 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.73; max drawdown 77.7R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 503 | 47.1 | -0.179 | 0.71 | 90.2R | -0.23 / -0.05 | -0.21 / -0.15 | 1/5 ✗ | -0.28 | - | ✗  stop atr 1.5→1.2: -0.25R | 1 | 0.19R | 18, -0.42 (-0.33 / -0.54) | 95 / 29 of 169 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.71; max drawdown 90.2R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3534 | 46.3 | -0.190 | 0.69 | 692.8R | -0.18 / -0.22 | -0.22 / -0.16 | 0/5 ✗ | -0.30 | - | ✗  stop atr 1.5→1.2: -0.25R | 0 | 0.17R | 68, +0.21 (+0.50 / -0.24) | 663 / 166 of 1347 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.69; max drawdown 692.8R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2827 | 47.6 | -0.193 | 0.41 | 545.8R | -0.18 / -0.23 | -0.25 / -0.14 | 0/5 ✗ | -0.29 | - | ✗  hi 90→108: -0.25R | 0 | 0.16R | 35, -0.15 (-0.16 / -0.11) | 846 / 13 of 1018 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.41; max drawdown 545.8R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 296 | 47.6 | -0.199 | 0.67 | 65.9R | -0.13 / -0.37 | -0.28 / -0.13 | 0/5 ✗ | -0.32 | - | ✗  stop atr 1.5→1.2: -0.27R | 1 | 0.19R | 6, -0.28 (+0.66 / -1.23) | 153 / 10 of 180 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.67; max drawdown 65.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 339 | 41.3 | -0.210 | 0.64 | 75.5R | -0.20 / -0.25 | -0.28 / -0.16 | 1/5 ✗ | -0.30 | - | ✗  fast 9→11: -0.28R | 0 | 0.17R | 8, +0.04 (-0.08 / +0.23) | 87 / 12 of 114 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.64; max drawdown 75.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 795 | 30.7 | -0.214 | 0.74 | 206.8R | -0.20 / -0.24 | -0.26 / -0.17 | 0/5 ✗ | -0.32 | - | ✗  stop buffer_atr 0.2→0.16: -0.25R | 1 | 0.21R | 8, +0.09 (+0.37 / -0.20) | 381 / 922 of 1378 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.74; max drawdown 206.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 280 | 43.9 | -0.227 | 0.62 | 67.7R | -0.22 / -0.24 | -0.33 / -0.14 | 0/5 ✗ | -0.28 | - | ✗  stop atr 2.0→1.6: -0.24R | 1 | 0.08R | 4, +0.17 (-0.19 / +1.24) | 46 / 0 of 54 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.62; max drawdown 67.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 294 | 46.9 | -0.239 | 0.61 | 71.2R | -0.26 / -0.19 | -0.25 / -0.22 | 0/5 ✗ | -0.33 | - | ✗  vol_x 1.2→1.44: -0.38R | 2 | 0.17R | 3, -0.85 (-1.58 / -0.48) | 89 / 168 of 264 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.61; max drawdown 71.2R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 3140 | 45.1 | -0.251 | 0.62 | 793.3R | -0.24 / -0.28 | -0.29 / -0.23 | 0/5 ✗ | -0.40 | - | ✗  stop atr 1.5→1.2: -0.33R | 0 | 0.25R | 142, -0.05 (+0.08 / -0.29) | 1015 / 258 of 1801 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.25R/trade (needs +0.10R); profit factor 0.62; max drawdown 793.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 2173 | 35.6 | -0.320 | 0.23 | 695.1R | -0.31 / -0.34 | -0.43 / -0.24 | 0/5 ✗ | -0.48 | - | ✗  hi 90→108: -0.43R | 0 | 0.27R | 55, -0.33 (-0.32 / -0.38) | 990 / 21 of 1119 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.32R/trade (needs +0.10R); profit factor 0.23; max drawdown 695.1R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 575 | 42.1 | -0.344 | 0.52 | 200.9R | -0.32 / -0.41 | -0.31 / -0.36 | 0/5 ✗ | -0.49 | - | ✗  stop atr 1.5→1.2: -0.42R | 0 | 0.29R | 37, -0.66 (-0.46 / -0.93) | 83 / 40 of 179 | 0 | not cost-viable: fees + slippage 0.29R per trade (stop must be ≥ 4x the round-trip cost); avg -0.34R/trade (needs +0.10R); profit factor 0.52; max drawdown 200.9R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 605 | 26.0 | -0.424 | 0.56 | 265.0R | -0.41 / -0.45 | -0.55 / -0.32 | 1/5 ✗ | -0.60 | - | ✗  n 20→24: -0.49R | 2 | 0.32R | 15, +0.13 (+0.45 / -0.24) | 367 / 801 of 1330 | 0 | not cost-viable: fees + slippage 0.32R per trade (stop must be ≥ 4x the round-trip cost); avg -0.42R/trade (needs +0.10R); profit factor 0.56; max drawdown 265.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 333 | 38.7 | -0.434 | 0.41 | 144.7R | -0.42 / -0.46 | -0.46 / -0.41 | 0/5 ✗ | -0.58 | - | ✗  stop atr 1.0→0.8: -0.49R | 1 | 0.26R | 8, -0.40 (-0.10 / -0.59) | 95 / 166 of 282 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.43R/trade (needs +0.10R); profit factor 0.41; max drawdown 144.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 582 | 39.5 | -0.466 | 0.4 | 272.9R | -0.44 / -0.55 | -0.61 / -0.40 | 0/5 ✗ | -0.67 | - | ✗  stop atr 1.0→0.8: -0.54R | 0 | 0.37R | 22, -0.47 (-0.73 / -0.25) | 75 / 192 of 292 | 0 | not cost-viable: fees + slippage 0.37R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R); profit factor 0.40; max drawdown 272.9R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 111 | 18.9 | -0.556 | 0.44 | 64.0R | -0.44 / -0.79 | -0.66 / -0.46 | 1/5 ✗ | -0.70 | - | ✗  stop buffer_atr 0.2→0.16: -0.56R | 0 | 0.24R | 3, -0.07 (-1.25 / +2.29) | 24 / 80 of 114 | 0 | avg -0.56R/trade (needs +0.10R); profit factor 0.44; max drawdown 64.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 276 | 29.7 | -0.716 | 0.25 | 197.6R | -0.78 / -0.61 | -0.68 / -0.86 | 0/5 ✗ | -1.08 | - | ✗  stop atr 1.5→1.2: -0.90R | 0 | 0.55R | 53, -0.48 (-0.30 / -0.70) | 163 / 54 of 273 | 0 | not cost-viable: fees + slippage 0.55R per trade (stop must be ≥ 4x the round-trip cost); avg -0.72R/trade (needs +0.10R); profit factor 0.25; max drawdown 197.6R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 423 | 26.5 | -1.137 | 0.16 | 484.2R | -1.18 / -1.09 | -1.05 / -1.66 | 0/5 ✗ | -1.79 | - | ✗  stop atr 1.0→0.8: -1.47R | 0 | 1.02R | 96, -1.23 (-1.48 / -0.91) | 159 / 507 of 769 | 0 | not cost-viable: fees + slippage 1.02R per trade (stop must be ≥ 4x the round-trip cost); avg -1.14R/trade (needs +0.10R); profit factor 0.16; max drawdown 484.2R; not profitable in BOTH train and unseen test |

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
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 100.8 KB | - | - |
| `memory/coin_notes.md` | 0.6 KB | - | - |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 3.6 KB | 7 | 2026-09-26 13:17 UTC |
| `memory/experiments.md` | 36.0 KB | 11 | 2026-09-26 06:40 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 10.0 KB | 11 | 2026-09-25 14:00 UTC |
| `memory/market_regime_log.md` | 3.7 KB | - | - |
| `memory/missed_trades.md` | 8.6 KB | 10 | 2026-09-26 06:28 UTC |
| `memory/playbook.md` | 8.5 KB | - | - |
| `memory/research_sources.md` | 40.2 KB | 32 | 2026-09-26 06:40 UTC |
| `memory/smc_events.csv` | 111.3 KB | - | - |
| `memory/smc_research.md` | 5.7 KB | - | - |
| `memory/strategy_lifecycle.md` | 13.0 KB | - | - |
| `memory/strategy_registry.csv` | 27.2 KB | - | - |
| `memory/trials.csv` | 4.0 KB | - | - |
| `memory/universe_log.md` | 5.5 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*