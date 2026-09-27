# Crypto Signal Report

**Updated:** 2026-09-27 17:18 Beijing time (2026-09-27 09:18 UTC) · data: Binance · 8 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 4.6 MB (GitHub) · large files of this run 2.9 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-27 09:18 UTC / 2026-09-27 17:18 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US GDP (Third Estimate), 2nd Quarter 2026 2026-09-30 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.03% (limit 0.5%)
- All 8 coins passed every check on every timeframe.
- 57 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-09-27 09:17 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 763 h since 2026-08-26 | -0.0018% | 1.33 | 0.92 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 763 h since 2026-08-26 | +0.0042% | 1.28 | 1.01 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 763 h since 2026-08-26 | -0.0125% | 0.37 | 0.83 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 763 h since 2026-08-26 | +0.0079% | 1.41 | 1.11 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 763 h since 2026-08-26 | +0.0066% | 2.75 | 0.86 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 763 h since 2026-08-26 | +0.0076% | 1.71 | 0.91 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 763 h since 2026-08-26 | +0.0100% | 1.72 | 0.93 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |
| AVAX | GOOD | okx | 755 h since 2026-08-26 | +0.0080% | 2.32 | 0.65 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=AVAXUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 763 h since 2026-08-26 | +0.0076% | 2.51 | 1.48 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **ZEC**, **SOL**, **XRP**, **SUI**, **UNI**
- **Research only** - backtested, never a signal: BNB
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** AVAX - order book too thin: $227k within 1% (need $250k)
  - **JOIN** UNI - in the top 7 for 2 runs in a row (now #7)

| Not eligible | 24h volume | Why |
|---|---|---|
| QNT | $88M | 7-day average volume $8M < $50M; 24h move +69.0% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $52k within 1% (need $250k) |
| AVAX | $57M | order book too thin: $227k within 1% (need $250k) |

*Skipped by your exclusion lists:* DOGE, NEAR, TAO, USD1, USDC, WLD (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 475 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ETH | 475 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ZEC | 392 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| SOL | 319 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| XRP | 438 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| SUI | 177 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| UNI | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| BNB | 463 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (HH/LL) | 84,571.1 / 83,838 | 0.56 | 2.79x | 0.45x | bear_reject, breakout_up, retest_up |
| ETH | mixed (LH/HL) | 2,696 / 2,691.01 | 0.09 | 2.92x | 0.53x | bear_reject, breakout_up, retest_up |
| ZEC | up (HH/HL) | 1,698 / 1,631.78 | 0.40 | 0.54x | 0.74x | bear_reject |
| SOL | mixed (LH/HL) | 121.83 / 120.1 | 0.16 | 4.37x | 0.93x | displacement_up, bear_reject, breakout_up |
| XRP | mixed (LH/HL) | 1.5303 / 1.506 | 0.07 | 1.32x | 0.59x | - |
| SUI | up (HH/HL) | 1.1907 / 1.1543 | 0.19 | 3.55x | 1.19x | displacement_up, bear_reject, breakout_up, retest_up |
| UNI | up (HH/HL) | 10 / 9.666 | 0.21 | 1.42x | 0.88x | bear_engulf, bear_reject |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 380 | 49% | 35% | 27% | 79% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | displacement_down | 307 | 49% | 32% | 22% | 75% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 974 | 44% | 31% | 21% | 77% | 43% | 30% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1092 | 44% | 30% | 21% | 76% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | bull_reject | 737 | 42% | 29% | 20% | 78% | 43% | 29% | can't tell from chance | 0.13R |
| 4h | bear_reject | 710 | 48% | 33% | 22% | 74% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 523 | 43% | 29% | 21% | 77% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 537 | 43% | 28% | 18% | 81% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 232 | 45% | 29% | 22% | 81% | 44% | 30% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 196 | 50% | 37% | 27% | 69% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 69 | 52% | 36% | 29% | 81% | 46% | 30% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 63 | 43% | 24% | 13% | 78% | 48% | 33% | can't tell from chance | 0.09R |
| 4h | smc_fvg_retrace_bull | 530 | 44% | 29% | 22% | 77% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | smc_fvg_retrace_bear | 541 | 47% | 31% | 20% | 75% | 48% | 33% | can't tell from chance | 0.08R |
| 1h | displacement_up | 489 | 47% | 35% | 28% | 71% | 43% | 30% | can't tell from chance | 0.29R |
| 1h | displacement_down | 340 | 39% | 25% | 15% | 82% | 38% | 24% | can't tell from chance | 0.20R |
| 1h | bull_engulf | 1363 | 40% | 29% | 22% | 74% | 42% | 29% | can't tell from chance | 0.34R |
| 1h | bear_engulf | 1546 | 39% | 25% | 17% | 79% | 37% | 24% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1149 | 40% | 28% | 21% | 75% | 42% | 29% | can't tell from chance | 0.33R |
| 1h | bear_reject | 1076 | 35% | 22% | 16% | 83% | 37% | 24% | can't tell from chance | 0.19R |
| 1h | smc_sweep_bull | 504 | 41% | 27% | 19% | 77% | 42% | 30% | can't tell from chance | 0.32R |
| 1h | smc_sweep_bear | 571 | 36% | 23% | 15% | 81% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 333 | 44% | 31% | 24% | 77% | 44% | 31% | can't tell from chance | 0.28R |
| 1h | smc_bos_down | 216 | 39% | 28% | 19% | 82% | 38% | 23% | can't tell from chance | 0.22R |
| 1h | smc_choch_up | 93 | 47% | 35% | 31% | 70% | 44% | 30% | can't tell from chance | 0.34R |
| 1h | smc_choch_down | 95 | 45% | 29% | 16% | 76% | 38% | 24% | can't tell from chance | 0.18R |
| 1h | smc_fvg_retrace_bull | 722 | 46% | 34% | 25% | 70% | 42% | 29% | can't tell from chance | 0.32R |
| 1h | smc_fvg_retrace_bear | 635 | 40% | 27% | 19% | 79% | 37% | 24% | can't tell from chance | 0.21R |
| 30m | displacement_up | 495 | 42% | 32% | 26% | 76% | 42% | 29% | can't tell from chance | 0.32R |
| 30m | displacement_down | 328 | 41% | 25% | 14% | 83% | 36% | 21% | can't tell from chance | 0.21R |
| 30m | bull_engulf | 1401 | 41% | 29% | 21% | 75% | 42% | 29% | can't tell from chance | 0.37R |
| 30m | bear_engulf | 1444 | 36% | 22% | 15% | 82% | 36% | 21% | can't tell from chance | 0.23R |
| 30m | bull_reject | 1092 | 44% | 29% | 22% | 73% | 41% | 29% | beats chance | 0.36R |
| 30m | bear_reject | 1142 | 37% | 23% | 16% | 81% | 36% | 21% | can't tell from chance | 0.22R |
| 30m | smc_sweep_bull | 497 | 39% | 29% | 19% | 75% | 41% | 29% | can't tell from chance | 0.37R |
| 30m | smc_sweep_bear | 512 | 41% | 26% | 18% | 81% | 36% | 22% | beats chance | 0.21R |
| 30m | smc_bos_up | 390 | 42% | 34% | 29% | 74% | 41% | 29% | can't tell from chance | 0.33R |
| 30m | smc_bos_down | 176 | 36% | 23% | 13% | 84% | 37% | 21% | can't tell from chance | 0.25R |
| 30m | smc_choch_up | 76 | 37% | 24% | 18% | 80% | 42% | 28% | can't tell from chance | 0.40R |
| 30m | smc_choch_down | 78 | 41% | 26% | 19% | 79% | 36% | 20% | can't tell from chance | 0.22R |
| 30m | smc_fvg_retrace_bull | 802 | 44% | 30% | 22% | 74% | 41% | 29% | can't tell from chance | 0.37R |
| 30m | smc_fvg_retrace_bear | 624 | 36% | 21% | 16% | 81% | 36% | 21% | can't tell from chance | 0.24R |
| 15m | displacement_up | 368 | 35% | 26% | 19% | 82% | 33% | 23% | can't tell from chance | 0.46R |
| 15m | displacement_down | 368 | 34% | 21% | 14% | 85% | 35% | 22% | can't tell from chance | 0.34R |
| 15m | bull_engulf | 1335 | 35% | 24% | 17% | 80% | 33% | 23% | can't tell from chance | 0.56R |
| 15m | bear_engulf | 1302 | 36% | 24% | 15% | 78% | 36% | 22% | can't tell from chance | 0.33R |
| 15m | bull_reject | 1095 | 34% | 22% | 15% | 80% | 33% | 23% | can't tell from chance | 0.56R |
| 15m | bear_reject | 1147 | 35% | 23% | 15% | 81% | 37% | 23% | can't tell from chance | 0.33R |
| 15m | smc_sweep_bull | 488 | 36% | 24% | 19% | 78% | 34% | 23% | can't tell from chance | 0.52R |
| 15m | smc_sweep_bear | 515 | 37% | 24% | 13% | 83% | 36% | 24% | can't tell from chance | 0.30R |
| 15m | smc_bos_up | 271 | 40% | 28% | 21% | 80% | 34% | 24% | can't tell from chance | 0.48R |
| 15m | smc_bos_down | 293 | 34% | 19% | 14% | 86% | 37% | 22% | can't tell from chance | 0.35R |
| 15m | smc_choch_up | 73 | 27% | 18% | 12% | 85% | 34% | 24% | can't tell from chance | 0.49R |
| 15m | smc_choch_down | 76 | 32% | 21% | 14% | 82% | 35% | 22% | can't tell from chance | 0.34R |
| 15m | smc_fvg_retrace_bull | 842 | 32% | 23% | 15% | 81% | 33% | 23% | can't tell from chance | 0.56R |
| 15m | smc_fvg_retrace_bear | 789 | 35% | 25% | 17% | 80% | 36% | 22% | can't tell from chance | 0.35R |
| 5m | displacement_up | 986 | 30% | 21% | 16% | 84% | 26% | 18% | beats chance | 0.87R |
| 5m | displacement_down | 924 | 26% | 16% | 10% | 87% | 29% | 20% | can't tell from chance | 0.60R |
| 5m | bull_engulf | 3405 | 25% | 18% | 13% | 83% | 26% | 18% | can't tell from chance | 0.98R |
| 5m | bear_engulf | 3414 | 30% | 20% | 13% | 83% | 29% | 19% | can't tell from chance | 0.61R |
| 5m | bull_reject | 2745 | 26% | 17% | 12% | 82% | 26% | 18% | can't tell from chance | 1.00R |
| 5m | bear_reject | 2931 | 31% | 20% | 13% | 83% | 29% | 19% | can't tell from chance | 0.60R |
| 5m | smc_sweep_bull | 967 | 29% | 20% | 14% | 80% | 28% | 19% | can't tell from chance | 0.85R |
| 5m | smc_sweep_bear | 1017 | 33% | 23% | 15% | 81% | 30% | 20% | can't tell from chance | 0.49R |
| 5m | smc_bos_up | 632 | 29% | 21% | 17% | 84% | 27% | 18% | can't tell from chance | 0.90R |
| 5m | smc_bos_down | 727 | 26% | 17% | 10% | 88% | 29% | 20% | can't tell from chance | 0.66R |
| 5m | smc_choch_up | 181 | 31% | 24% | 15% | 86% | 28% | 19% | can't tell from chance | 1.04R |
| 5m | smc_choch_down | 176 | 22% | 11% | 7% | 90% | 29% | 20% | worse than chance | 0.64R |
| 5m | smc_fvg_retrace_bull | 2685 | 27% | 19% | 14% | 81% | 25% | 18% | beats chance | 1.03R |
| 5m | smc_fvg_retrace_bear | 2403 | 26% | 17% | 11% | 85% | 28% | 19% | worse than chance | 0.65R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (weak) | WEAK_BULL (moderate) | WEAK_BULL (weak) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ETH** | UNCLEAR (weak) | WEAK_BULL (moderate) | COMPRESSION (weak) | RANGE (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H COMPRESSION, 1H RANGE)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | STRONG_BULL (strong) | LONG allowed (1D/4H/1H bullish, 1W WEAK_BULL) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (weak) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | TRANSITION (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)) |
| **SUI** | RANGE (weak) | EXPANSION up (weak) | STRONG_BULL (weak) | WEAK_BULL (moderate) | LONG allowed (1D/4H/1H bullish, 1W RANGE) |
| **UNI** | EXPANSION up (weak) | STRONG_BULL (moderate) | TRANSITION (weak) | WEAK_BULL (weak) | LONG allowed (1D/1H bullish, 1W EXPANSION) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (strong) | WEAK_BULL (weak) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (weak)** - for: EMA-fast rising (+1.1 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.72x normal, Bollinger width above 52% of the last 100 candles · against: EMAs not lined up; ADX 27 is close to a threshold
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.4 ATR in 10 candles); ADX 44 = strong trend; candle size 1.09x normal, Bollinger width above 81% of the last 100 candles; volume 1.13x normal · against: swing structure mixed (neutral)
- **4H WEAK_BULL (weak)** - for: close above EMA-fast above EMA-slow; swing structure up (HH/HL); candle size 0.81x normal, Bollinger width above 7% of the last 100 candles · against: EMA-fast flat (+0.6 ATR in 10 candles) (neutral); ADX 15 = weak trend / ranging; volume only 0.51x normal (weak participation)
- **1H RANGE (moderate)** - for: EMA-fast flat (+0.5 ATR in 10 candles); swing structure mixed; ADX 13 = weak trend / ranging; candle size 0.45x normal, Bollinger width above 35% of the last 100 candles · against: close above EMA-fast above EMA-slow

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | up (BOS 5 candles ago) | buy-side (bearish idea) 14 candles ago | bull 84,550.06-84,614.00 (retraced) | bear 86,133.40-86,975.51 | above the range (131%) | swing high 85,255.00 (2.08 ATR) | equal lows 83,838.00 (4.39 ATR) |
| **ETH** | up (BOS 5 candles ago) | buy-side (bearish idea) 2 candles ago | bull 2,697.89-2,704.48 | bear 2,745.99-2,784.40 | above the range (473%) | swing high 2,743.00 (2.69 ATR) | swing low 2,691.01 (2.23 ATR) |
| **ZEC** | down (BOS 21 candles ago) | sell-side (bullish idea) 0 candles ago | bull 1,637.34-1,644.71 | bull 1,527.56-1,540.22 | discount (46%) | PDH 1,698.00 (1.77 ATR) | swing low 1,631.78 (1.51 ATR) |
| **SOL** | down (BOS 23 candles ago) | buy-side (bearish idea) 6 candles ago | bull 122.36-123.96 (retraced) | bull 115.86-117.34 | above the range (232%) | - | equal lows 120.07 (3.84 ATR) |
| **XRP** | down (BOS 19 candles ago) | sell-side (bullish idea) 20 candles ago | bull 1.5265-1.5315 (retraced) | bull 1.3773-1.3856 | above the range (118%) | swing high 1.5541 (1.53 ATR) | swing low 1.5060 (2.26 ATR) |
| **SUI** | up (BOS 7 candles ago) | buy-side (bearish idea) 11 candles ago | bull 1.2346-1.2484 (retraced) | bull 1.0050-1.0598 | above the range (306%) | - | swing low 1.1543 (4.77 ATR) |
| **UNI** | up (BOS 16 candles ago) | buy-side (bearish idea) 12 candles ago | bull 9.7480-9.7700 | bull 8.6780-9.0640 | premium (93%) | swing high 10.942 (5.91 ATR) | swing low 9.6660 (1.91 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 70 (Greed), yesterday 74  (extreme fear/greed = bigger, faster moves)

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
**Status and long-history numbers** come from the daily research run (last run 2026-09-27 00:50 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 60.0 | +1.221 | 3.69 | 2.3R | +0.97 / +2.21 | +2.21 / +0.97 | 0/5 ✗ | +1.10 | +0.98 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 21 / 11 of 33 | 0 | only 5 trades; only 1 unseen-test trades |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 14 | 42.9 | +0.224 | 1.28 | 4.1R | +0.23 / +0.22 | -0.17 / +0.44 | 0/5 ✗ | -0.09 | -0.25 | ✗  sweep_bars 8→10: -0.11R | 0 | 0.26R | 2, +0.31 (+0.31 / +0.00) | 38 / 22 of 66 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 14 trades; only 4 unseen-test trades |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 803 | 40.2 | +0.222 | 1.42 | 23.7R | +0.20 / +0.28 | +0.27 / +0.17 | 5/5 | +0.19 | +0.17 | stable | 8 | 0.04R | 9, +0.48 (+0.48 / +0.00) | 76 / 43 of 213 | 0 | max drawdown 23.7R |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.206 | 1.21 | 3.3R | +0.51 / -1.32 | -1.32 / +0.51 | 0/5 ✗ | +0.08 | -0.03 | ✗  sweep_bars 20→24: -0.16R | 0 | 0.26R | 1, -1.32 (-1.32 / +0.00) | 30 / 10 of 47 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 6 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 828 | 54.5 | +0.123 | 1.28 | 23.1R | +0.10 / +0.16 | +0.14 / +0.11 | 4/5 | +0.09 | +0.07 | stable | 6 | 0.04R | 11, +0.18 (+0.30 / -1.03) | 76 / 43 of 213 | 0 | max drawdown 23.1R |
| macd_trend_cross | 1.0 | 4h | **BACKTESTING** | 26 | 57.7 | +0.040 | 1.09 | 4.6R | +0.24 / -0.33 | +0.20 / -0.17 | 1/5 ✗ | +0.01 | -0.02 | stable | 1 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 121 / 5 of 127 | 0 | only 26 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.09; only 9 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **BACKTESTING** | 660 | 53.2 | +0.004 | 1.01 | 37.4R | -0.01 / +0.04 | -0.06 / +0.07 | 2/5 ✗ | -0.08 | -0.16 | ✗  bb_k 2→1: -0.05R | 4 | 0.14R | 5, +0.27 (-1.27 / +0.66) | 121 / 31 of 183 | 0 | avg +0.00R/trade (needs +0.10R); profit factor 1.01; max drawdown 37.4R; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 2 of 3 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 48 / 9 of 60 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 30 / 10 of 47 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 1 / 2 of 3 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 21 / 11 of 33 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 11 | 27.3 | -0.198 | 0.62 | 2.7R | -0.39 / +0.14 | -1.11 / -0.11 | 0/5 ✗ | -0.30 | -0.24 | ✗  stop max_width_atr 3.0→3.6: -0.20R | 0 | 0.08R | 0, +0.00 (+0.00 / +0.00) | 431 / 145 of 700 | 0 | only 11 trades; avg -0.20R/trade (needs +0.10R); profit factor 0.62; only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 13 | 46.2 | -0.308 | 0.48 | 5.9R | -0.37 / +0.05 | -0.31 / -0.31 | 0/5 ✗ | -0.30 | -0.54 | ✗  time_stop_bars 30→24: -0.36R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 358 / 177 of 652 | 0 | only 13 trades; avg -0.31R/trade (needs +0.10R); profit factor 0.48; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 4 | 0.0 | -1.218 | 0.0 | 4.9R | -1.24 / -1.16 | -1.42 / -1.15 | 0/5 ✗ | -1.22 | -1.29 | ✗  stop buffer_atr 0.2→0.16: -1.23R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 48 / 9 of 60 | 0 | only 4 trades; avg -1.22R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.712 | 0.0 | 1.7R | +0.00 / -1.71 | -1.71 / +0.00 | 0/5 ✗ | -2.00 | -2.25 | ✗  stop buffer_atr 0.2→0.16: -1.75R | 0 | 0.86R | 0, +0.00 (+0.00 / +0.00) | 29 / 82 of 120 | 0 | not cost-viable: fees + slippage 0.86R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.71R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 10, +0.80 (+0.80 / +0.00) | 128 / 55 of 286 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 25, +0.60 (+0.71 / +0.14) | 175 / 100 of 449 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 44, -0.09 (+0.08 / -0.55) | 206 / 39 of 433 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 9, +0.48 (+0.48 / +0.00) | 76 / 43 of 213 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 23, +0.51 (+0.71 / -0.43) | 103 / 72 of 322 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 41, -0.09 (+0.08 / -0.70) | 120 / 28 of 310 | 0 | waiting for the first daily research run (Layers B/C) |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, +1.07 (+0.00 / +1.07) | 66 / 6 of 77 | 0 | waiting for the first daily research run (Layers B/C) |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 34 / 6 of 40 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 220 | 52.3 | +0.043 | 1.08 | 24.2R | +0.23 / -0.30 | +0.11 / -0.02 | 3/5 | -0.00 | -0.05 | ✗  stop atr 1.5→1.8: -0.01R | 5 | 0.07R | 2, +0.08 (-1.11 / +1.27) | 87 / 19 of 117 | 0 | avg +0.04R/trade (needs +0.10R); profit factor 1.08; max drawdown 24.2R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1050 | 35.0 | -0.006 | 0.99 | 69.3R | -0.03 / +0.06 | +0.07 / -0.08 | 3/5 | -0.09 | -0.16 | ✗  stop atr 2.0→1.6: -0.10R | 4 | 0.12R | 41, -0.09 (+0.08 / -0.70) | 120 / 28 of 310 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; max drawdown 69.3R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2223 | 32.7 | -0.037 | 0.94 | 151.2R | -0.08 / +0.05 | -0.01 / -0.07 | 2/5 ✗ | -0.09 | -0.14 | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.08R | 23, +0.51 (+0.71 / -0.43) | 103 / 72 of 322 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; max drawdown 151.2R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1080 | 50.0 | -0.041 | 0.92 | 75.3R | -0.05 / -0.02 | +0.01 / -0.09 | 2/5 ✗ | -0.11 | -0.18 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.12R | 41, -0.03 (+0.06 / -0.36) | 120 / 28 of 310 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.92; max drawdown 75.3R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 142 | 49.3 | -0.041 | 0.93 | 23.0R | -0.22 / +0.29 | -0.12 / +0.03 | 2/5 ✗ | -0.10 | -0.18 | ✗  stop atr 1.5→1.2: -0.14R | 3 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 176 / 3 of 181 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.93; max drawdown 23.0R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2287 | 48.4 | -0.049 | 0.91 | 140.1R | -0.07 / -0.01 | -0.05 / -0.05 | 1/5 ✗ | -0.10 | -0.15 | ✗  stop atr 2.0→1.6: -0.06R | 1 | 0.08R | 24, +0.41 (+0.52 / -0.14) | 103 / 72 of 322 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 140.1R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 902 | 47.9 | -0.085 | 0.84 | 101.2R | -0.03 / -0.20 | -0.04 / -0.14 | 1/5 ✗ | -0.12 | -0.16 | ✗  long_rsi_hi 65→52: -0.15R | 2 | 0.06R | 6, +1.14 (+1.12 / +1.27) | 509 / 163 of 808 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.84; max drawdown 101.2R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 39 | 38.5 | -0.096 | 0.85 | 9.8R | +0.17 / -0.44 | -0.28 / +0.06 | 1/5 ✗ | -0.26 | -0.37 | ✗  stop buffer_atr 0.2→0.16: -0.10R | 3 | 0.15R | 5, -0.64 (-0.27 / -1.19) | 82 / 25 of 120 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.85; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1348 | 55.9 | -0.103 | 0.64 | 139.1R | -0.10 / -0.12 | -0.12 / -0.08 | 0/5 ✗ | -0.13 | -0.16 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.05R | 7, -0.11 (-0.11 / +0.00) | 607 / 3 of 816 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.64; max drawdown 139.1R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 365 | 46.8 | -0.121 | 0.79 | 48.7R | -0.12 / -0.14 | -0.17 / -0.10 | 1/5 ✗ | -0.27 | -0.39 | ✗  stop atr 1.5→1.2: -0.25R | 1 | 0.24R | 17, +0.13 (+0.21 / -0.44) | 54 / 11 of 85 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.79; max drawdown 48.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 4720 | 47.8 | -0.124 | 0.78 | 595.9R | -0.12 / -0.13 | -0.17 / -0.07 | 0/5 ✗ | -0.19 | -0.26 | ✗  stop atr 1.5→1.2: -0.16R | 1 | 0.13R | 37, -0.03 (-0.02 / -0.03) | 962 / 231 of 1499 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.78; max drawdown 595.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 5234 | 53.7 | -0.132 | 0.54 | 694.2R | -0.11 / -0.18 | -0.14 / -0.12 | 0/5 ✗ | -0.20 | -0.26 | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 32, -0.16 (-0.28 / -0.04) | 853 / 3 of 1142 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.54; max drawdown 694.2R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 269 | 43.9 | -0.138 | 0.75 | 44.7R | -0.18 / -0.07 | -0.22 / -0.06 | 0/5 ✗ | -0.21 | -0.28 | ✗  slow 21→17: -0.20R | 3 | 0.12R | 3, -1.00 (-1.25 / -0.52) | 117 / 5 of 129 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.75; max drawdown 44.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 226 | 32.7 | -0.145 | 0.82 | 49.7R | -0.06 / -0.32 | -0.44 / +0.18 | 1/5 ✗ | -0.26 | -0.37 | ✗  time_stop_bars 30→36: -0.18R | 1 | 0.20R | 1, +2.70 (+0.00 / +2.70) | 72 / 178 of 258 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.82; max drawdown 49.7R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 245 | 49.4 | -0.161 | 0.73 | 45.7R | -0.06 / -0.40 | -0.30 / -0.03 | 1/5 ✗ | -0.28 | -0.37 | ✗  stop atr 1.5→1.2: -0.24R | 1 | 0.19R | 4, -0.16 (+0.99 / -1.31) | 153 / 8 of 177 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.73; max drawdown 45.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 2877 | 46.7 | -0.179 | 0.71 | 538.9R | -0.16 / -0.22 | -0.20 / -0.15 | 0/5 ✗ | -0.28 | -0.39 | ✗  stop atr 1.5→1.2: -0.23R | 0 | 0.17R | 74, +0.06 (+0.21 / -0.23) | 736 / 171 of 1404 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.71; max drawdown 538.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2242 | 48.3 | -0.180 | 0.44 | 404.8R | -0.17 / -0.21 | -0.23 / -0.14 | 0/5 ✗ | -0.28 | -0.37 | ✗  stop atr 2.0→1.6: -0.23R | 0 | 0.16R | 26, -0.06 (-0.03 / -0.12) | 855 / 22 of 1029 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.44; max drawdown 404.8R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 272 | 42.6 | -0.180 | 0.68 | 53.3R | -0.16 / -0.24 | -0.29 / -0.10 | 1/5 ✗ | -0.26 | -0.34 | ✗  fast 9→11: -0.27R | 0 | 0.16R | 7, +0.20 (+0.18 / +0.22) | 88 / 14 of 113 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.68; max drawdown 53.3R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 133 | 45.9 | -0.189 | 0.67 | 25.5R | -0.19 / -0.19 | -0.20 / -0.18 | 2/5 ✗ | -0.26 | -0.35 | ✗  adx_min 20→24: -0.26R | 1 | 0.12R | 6, -0.74 (-0.64 / -1.26) | 47 / 5 of 60 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.67; max drawdown 25.5R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 425 | 46.4 | -0.192 | 0.69 | 82.7R | -0.23 / -0.08 | -0.26 / -0.13 | 1/5 ✗ | -0.30 | -0.41 | ✗  stop atr 1.5→1.2: -0.25R | 1 | 0.18R | 16, -0.41 (-0.22 / -0.73) | 108 / 26 of 176 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.69; max drawdown 82.7R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 64 | 43.8 | -0.196 | 0.66 | 16.1R | -0.04 / -0.47 | -0.26 / -0.12 | 1/5 ✗ | -0.22 | -0.24 | ✗  st_n 10→12: -0.20R | 0 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 33 / 6 of 41 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.66; max drawdown 16.1R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 634 | 30.4 | -0.215 | 0.74 | 164.8R | -0.24 / -0.18 | -0.33 / -0.12 | 1/5 ✗ | -0.32 | -0.42 | ✗  stop buffer_atr 0.2→0.16: -0.25R | 1 | 0.21R | 10, +0.20 (+0.87 / -0.48) | 390 / 928 of 1392 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.74; max drawdown 164.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 218 | 44.0 | -0.227 | 0.62 | 53.9R | -0.24 / -0.20 | -0.35 / -0.12 | 2/5 ✗ | -0.29 | -0.34 | ✗  adx_min 20→16: -0.24R | 1 | 0.08R | 4, +0.17 (-0.19 / +1.24) | 48 / 1 of 56 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.62; max drawdown 53.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 2514 | 45.6 | -0.231 | 0.64 | 588.5R | -0.22 / -0.25 | -0.26 / -0.21 | 0/5 ✗ | -0.38 | -0.52 | ✗  stop atr 1.5→1.2: -0.30R | 0 | 0.24R | 147, -0.13 (-0.06 / -0.34) | 1079 / 249 of 1847 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.64; max drawdown 588.5R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 241 | 46.5 | -0.240 | 0.62 | 58.9R | -0.23 / -0.27 | -0.29 / -0.17 | 0/5 ✗ | -0.33 | -0.41 | ✗  vol_x 1.2→1.44: -0.42R | 1 | 0.17R | 4, -0.23 (+0.01 / -0.48) | 85 / 162 of 254 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.62; max drawdown 58.9R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 948 | 30.4 | -0.287 | 0.63 | 273.5R | -0.29 / -0.27 | -0.30 / -0.28 | 0/5 ✗ | -0.36 | -0.43 | ✗  rsi_n 14→17: -0.37R | 1 | 0.14R | 8, -0.54 (-0.68 / +0.40) | 603 / 5 of 646 | 0 | avg -0.29R/trade (needs +0.10R); profit factor 0.63; max drawdown 273.5R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 1736 | 36.6 | -0.303 | 0.24 | 526.6R | -0.29 / -0.33 | -0.40 / -0.23 | 0/5 ✗ | -0.46 | -0.62 | ✗  hi 90→108: -0.40R | 0 | 0.26R | 44, -0.27 (-0.19 / -0.66) | 997 / 33 of 1129 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.30R/trade (needs +0.10R); profit factor 0.24; max drawdown 526.6R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1206 | 31.1 | -0.320 | 0.6 | 390.4R | -0.33 / -0.29 | -0.34 / -0.30 | 0/5 ✗ | -0.44 | -0.55 | ✗  stop atr 1.5→1.2: -0.36R | 0 | 0.20R | 22, -0.23 (-0.56 / +0.66) | 518 / 20 of 607 | 0 | avg -0.32R/trade (needs +0.10R); profit factor 0.60; max drawdown 390.4R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 488 | 42.6 | -0.325 | 0.54 | 166.7R | -0.27 / -0.43 | -0.28 / -0.35 | 0/5 ✗ | -0.47 | -0.61 | ✗  stop atr 1.5→1.2: -0.40R | 0 | 0.28R | 34, -0.73 (-0.67 / -0.92) | 79 / 43 of 175 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.33R/trade (needs +0.10R); profit factor 0.54; max drawdown 166.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 471 | 40.3 | -0.441 | 0.42 | 210.9R | -0.43 / -0.48 | -0.51 / -0.41 | 0/5 ✗ | -0.64 | -0.86 | ✗  stop atr 1.0→0.8: -0.49R | 0 | 0.36R | 25, -0.43 (-0.55 / -0.24) | 90 / 191 of 310 | 0 | not cost-viable: fees + slippage 0.36R per trade (stop must be ≥ 4x the round-trip cost); avg -0.44R/trade (needs +0.10R); profit factor 0.42; max drawdown 210.9R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 518 | 24.7 | -0.449 | 0.54 | 240.4R | -0.46 / -0.41 | -0.55 / -0.36 | 0/5 ✗ | -0.62 | -0.75 | ✗  n 20→24: -0.49R | 1 | 0.32R | 17, +0.15 (+0.90 / -0.94) | 374 / 804 of 1336 | 0 | not cost-viable: fees + slippage 0.32R per trade (stop must be ≥ 4x the round-trip cost); avg -0.45R/trade (needs +0.10R); profit factor 0.54; max drawdown 240.4R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 272 | 35.7 | -0.507 | 0.35 | 137.9R | -0.50 / -0.52 | -0.51 / -0.50 | 0/5 ✗ | -0.66 | -0.80 | ✗  stop atr 1.0→0.8: -0.57R | 0 | 0.27R | 8, -0.75 (-0.70 / -0.83) | 93 / 169 of 282 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.51R/trade (needs +0.10R); profit factor 0.35; max drawdown 137.9R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 98 | 19.4 | -0.533 | 0.47 | 54.5R | -0.44 / -0.73 | -0.69 / -0.37 | 1/5 ✗ | -0.69 | -0.82 | ✗  stop max_width_atr 3.0→2.4: -0.53R | 0 | 0.25R | 3, -0.07 (-1.25 / +2.29) | 29 / 82 of 120 | 0 | avg -0.53R/trade (needs +0.10R); profit factor 0.47; max drawdown 54.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 236 | 30.5 | -0.684 | 0.25 | 161.3R | -0.73 / -0.60 | -0.65 / -0.88 | 0/5 ✗ | -1.02 | -1.37 | ✗  stop atr 1.5→1.2: -0.86R | 0 | 0.51R | 59, -0.56 (-0.51 / -0.67) | 173 / 52 of 287 | 0 | not cost-viable: fees + slippage 0.51R per trade (stop must be ≥ 4x the round-trip cost); avg -0.68R/trade (needs +0.10R); profit factor 0.25; max drawdown 161.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 374 | 26.7 | -1.140 | 0.16 | 426.2R | -1.23 / -1.04 | -1.04 / -1.87 | 0/5 ✗ | -1.78 | -2.41 | ✗  stop atr 1.0→0.8: -1.48R | 0 | 0.96R | 110, -1.27 (-1.44 / -1.00) | 183 / 499 of 796 | 0 | not cost-viable: fees + slippage 0.96R per trade (stop must be ≥ 4x the round-trip cost); avg -1.14R/trade (needs +0.10R); profit factor 0.16; max drawdown 426.2R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **22** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 102 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.30** (Bonferroni: family-wise false-winner rate 0.05 over 102 trials; with 1 trial it would be 1.65).

**Research run duration:** 8.2 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 22 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (112.9 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 30 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: donchian_breakout-VEXIT-S4.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

1 of 51 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **VALIDATION** | 4.39 | 16.4R | 626 d (19%) | multiple-testing bar: t-statistic 3.18 of the average trade, needs 3.30 after 102 trials |

🧪 **Strategy lab:** 5 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 15m | 5 | +1.221 | +2.214 | +0.224 | +0.217 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 6 | +0.206 | -1.323 | -0.308 | +0.049 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.096 | -0.443 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +2.214 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 4 | -1.218 | -1.163 | -0.198 | +0.138 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 1 | -1.712 | -1.712 | -0.635 | -0.871 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 226 | -0.145 | -0.316 | -0.215 | -0.181 | no |
| S8-PDH-PDL-SWEEP | 30m | 98 | -0.533 | -0.730 | -0.449 | -0.411 | no |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): R4-BBRSI@1.0 1h FORMALIZED → FAILED; R4-BBRSI@1.0 30m FORMALIZED → FAILED; bb_squeeze_breakout@1.0 1h FAILED → BACKTESTING; donchian_breakout-VEXIT@1.0 1h FORMALIZED → FAILED; donchian_breakout-VEXIT@1.0 30m FORMALIZED → FAILED; donchian_breakout-VEXIT@1.0 4h FORMALIZED → BACKTESTING; macd_trend_cross@1.0 4h FAILED → BACKTESTING

### 3c. Research layers (daily run)
Last run: **2026-09-27 00:50 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 8 | 2017-08-17 | 2026-09-26 | 19951 |  |
| 1h | 8 | 2017-08-17 | 2026-09-26 | 79740 |  |
| 30m | 8 | 2024-09-27 | 2026-09-27 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 8 | 2025-09-27 | 2026-09-27 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 8 | 2026-06-29 | 2026-09-27 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 803 (480) | no_displacement, false_breakout, trend_reversal | false_breakout 63%, no_displacement 32% | +0.47R | -0.37R | +0.28 / +0.22 |
| donchian_breakout | 4h | BACKTESTING | 828 (377) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 65%, stop_too_tight 33%, no_displacement 32% | +0.33R | -0.37R | +0.18 / +0.12 |
| bb_squeeze_breakout | 1h | BACKTESTING | 660 (309) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 63%, no_displacement 52%, stop_too_tight 36%, regime_mismatch 35% | +0.36R | -0.47R | +0.17 / +0.00 |
| bb_squeeze_breakout | 4h | FAILED | 220 (105) | stop_too_tight, structural_change | false_breakout 54%, stop_too_tight 39% | +0.34R | -0.34R | +0.13 / +0.04 |
| donchian_breakout-VEXIT | 30m | FAILED | 1050 (682) | false_breakout | false_breakout 72% | +0.50R | -0.39R | +0.14 / -0.01 |
| donchian_breakout-VEXIT | 1h | FAILED | 2223 (1497) | no_displacement, false_breakout | false_breakout 62%, no_displacement 34% | +0.52R | -0.38R | +0.07 / -0.04 |
| donchian_breakout | 30m | FAILED | 1080 (540) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 75%, stop_too_tight 34% | +0.31R | -0.41R | +0.10 / -0.04 |
| macd_trend_cross | 1h | FAILED | 142 (72) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 92%, indicator_lag 35%, stop_too_tight 26% | +0.37R | -0.40R | +0.11 / -0.04 |
| donchian_breakout | 1h | FAILED | 2287 (1179) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 65%, no_displacement 37%, stop_too_tight 32%, regime_mismatch 25% | +0.38R | -0.39R | +0.05 / -0.05 |
| trend_pullback | 4h | FAILED | 902 (470) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 79%, indicator_lag 38%, stop_too_tight 28% | +0.36R | -0.43R | -0.01 / -0.09 |
| S6-OB-FVG-noSMC | 15m | FAILED | 39 (24) | structural_change | stop_too_wide 92% | +0.32R | -0.47R | +0.08 / -0.10 |
| rsi2_dip_buy | 4h | FAILED | 1348 (595) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 44% | +0.16R | -0.20R | -0.04 / -0.10 |
| ema_9_21_cross | 15m | FAILED | 365 (194) | stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 28% | +0.26R | -0.45R | +0.17 / -0.12 |
| trend_pullback | 1h | FAILED | 4720 (2462) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 76%, indicator_lag 44%, stop_too_tight 27% | +0.30R | -0.42R | +0.03 / -0.12 |
| rsi2_dip_buy | 1h | FAILED | 5234 (2424) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 41% | +0.16R | -0.20R | -0.00 / -0.13 |
| ema_9_21_cross | 1h | FAILED | 269 (151) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 79%, wrong_session 66%, indicator_lag 46%, stop_too_tight 26% | +0.29R | -0.42R | +0.01 / -0.14 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 226 (152) | stop_too_tight, sweep_continued | sweep_continued 97%, range_market 55%, stop_too_tight 30% | +0.57R | -0.44R | +0.10 / -0.14 |
| macd_trend_cross | 30m | FAILED | 245 (124) | stop_too_tight, indicator_lag | no_displacement 87%, indicator_lag 48%, low_relative_volume 44%, stop_too_tight 29% | +0.30R | -0.45R | +0.07 / -0.16 |
| trend_pullback | 30m | FAILED | 2877 (1534) | stop_too_tight, indicator_lag | indicator_lag 45%, stop_too_tight 31% | +0.28R | -0.41R | +0.03 / -0.18 |
| rsi2_dip_buy | 30m | FAILED | 2242 (1158) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 32% | +0.16R | -0.19R | +0.01 / -0.18 |
| ema_9_21_cross | 30m | FAILED | 272 (156) | indicator_lag | indicator_lag 47%, low_relative_volume 42% | +0.26R | -0.40R | +0.02 / -0.18 |
| supertrend_flip | 30m | FAILED | 133 (72) | stop_too_tight, indicator_lag | indicator_lag 44%, stop_too_tight 38%, overextended_entry 31%, late_entry 28% | +0.28R | -0.41R | -0.04 / -0.19 |
| bb_squeeze_breakout | 30m | FAILED | 425 (228) | false_breakout, stop_too_tight | false_breakout 62%, stop_too_tight 38% | +0.28R | -0.42R | +0.05 / -0.19 |
| supertrend_flip | 4h | FAILED | 64 (36) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 72%, indicator_lag 42%, stop_too_tight 28% | +0.36R | -0.44R | -0.13 / -0.20 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 634 (441) | range_market, stop_too_tight | range_market 46%, stop_too_tight 36% | +0.62R | -0.52R | +0.04 / -0.21 |
| supertrend_flip | 1h | FAILED | 218 (122) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 72%, regime_mismatch 69%, stop_too_tight 41%, indicator_lag 29% | +0.40R | -0.35R | -0.12 / -0.23 |
| trend_pullback | 15m | FAILED | 2514 (1368) | late_entry, wrong_session, stop_too_tight, indicator_lag | wrong_session 71%, indicator_lag 50%, stop_too_tight 31% | +0.25R | -0.45R | +0.07 / -0.23 |
| liquidity_sweep_reversal | 1h | FAILED | 241 (129) | trend_reversal, stop_too_tight | stop_too_tight 54% | +0.29R | -0.46R | -0.04 / -0.24 |
| R4-BBRSI | 1h | FAILED | 948 (660) | none | - | +0.45R | -0.46R | -0.11 / -0.29 |
| rsi2_dip_buy | 15m | FAILED | 1736 (1101) | low_relative_volume, trend_reversal, fees_slippage | low_relative_volume 45%, fees_slippage 44% | +0.17R | -0.19R | +0.01 / -0.30 |
| R4-BBRSI | 30m | FAILED | 1206 (831) | none | - | +0.43R | -0.43R | -0.07 / -0.32 |
| bb_squeeze_breakout | 15m | FAILED | 488 (280) | stop_too_tight | no_displacement 57%, false_breakout 57%, range_market 52%, stop_too_tight 41% | +0.31R | -0.47R | +0.01 / -0.33 |
| liquidity_sweep_reversal | 15m | FAILED | 471 (281) | stop_too_tight | stop_too_tight 38% | +0.37R | -0.46R | +0.01 / -0.44 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 518 (390) | stop_too_tight | stop_too_tight 33% | +0.60R | -0.54R | -0.06 / -0.45 |
| liquidity_sweep_reversal | 30m | FAILED | 272 (175) | stop_too_tight | stop_too_tight 39% | +0.41R | -0.47R | -0.19 / -0.51 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 98 (79) | stop_too_tight, sweep_continued | sweep_continued 96%, stop_too_tight 30% | +0.46R | -0.67R | -0.20 / -0.53 |
| ema_9_21_cross | 5m | FAILED | 236 (164) | stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 29% | +0.26R | -0.48R | -0.02 / -0.68 |
| liquidity_sweep_reversal | 5m | FAILED | 374 (274) | htf_conflict, stop_too_tight | stop_too_tight 38% | +0.26R | -0.47R | +0.14 / -1.14 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 27 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `regime_mismatch` (systematic in 12 strategy/timeframe tests); `false_breakout` (systematic in 8 strategy/timeframe tests); `trend_reversal` (systematic in 7 strategy/timeframe tests); `no_displacement` (systematic in 4 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- ZEC up +10.4% (2026-09-26 09:00 → 2026-09-26 22:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 100.8 KB | - | - |
| `memory/coin_notes.md` | 6.8 KB | 7 | 2026-09-27 00:26 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 4.1 KB | 8 | 2026-09-27 06:23 UTC |
| `memory/experiments.md` | 37.9 KB | 12 | 2026-09-27 02:00 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 17.8 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 4.8 KB | - | - |
| `memory/missed_trades.md` | 9.3 KB | 11 | 2026-09-27 00:50 UTC |
| `memory/playbook.md` | 8.7 KB | - | - |
| `memory/research_sources.md` | 51.5 KB | 40 | 2026-09-27 02:00 UTC |
| `memory/smc_events.csv` | 151.4 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 14.2 KB | - | - |
| `memory/strategy_registry.csv` | 31.4 KB | - | - |
| `memory/trials.csv` | 8.1 KB | - | - |
| `memory/universe_log.md` | 6.0 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*