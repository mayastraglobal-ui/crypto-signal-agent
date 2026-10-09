# Crypto Signal Report

**Updated:** 2026-10-09 23:20 Beijing time (2026-10-09 15:20 UTC) · data: Binance · 9 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 13.7 MB (GitHub) · large files of this run 5.1 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-09 15:20 UTC / 2026-10-09 23:20 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US CPI (Sep data) 2026-10-14 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.03% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| RLC | **DEGRADED** | 1d: DEGRADED: volume 103x normal on candle 10-06 00:00 UTC (possible bad data); 1d: DEGRADED: volume 50x normal on candle 10-08 00:00 UTC (possible bad data) |
- 65 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-09 15:19 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 1057 h since 2026-08-26 | +0.0007% | 1.42 | 1.05 | - |
| ETH | GOOD | okx | 1057 h since 2026-08-26 | -0.0085% | 1.84 | 1.23 | - |
| SOL | GOOD | okx | 1057 h since 2026-08-26 | -0.0052% | 2.33 | 1.18 | - |
| ZEC | GOOD | okx | 1057 h since 2026-08-26 | -0.0032% | 0.69 | 1.02 | - |
| XRP | GOOD | okx | 1057 h since 2026-08-26 | -0.0084% | 2.95 | 1.37 | - |
| BNB | GOOD | okx | 1057 h since 2026-08-26 | -0.0186% | 2.79 | 1.01 | - |
| SUI | GOOD | okx | 1057 h since 2026-08-26 | -0.0059% | 2.98 | 1.01 | - |
| UNI | GOOD | okx | 1057 h since 2026-08-26 | -0.0004% | 1.46 | 1.40 | - |
| ADA | GOOD | okx | 1044 h since 2026-08-27 | +0.0004% | 2.44 | 1.05 | - |
| AVAX | GOOD | okx | 1049 h since 2026-08-26 | -0.0032% | 1.94 | 0.98 | - |

*Binance futures API: blocked from GitHub's servers (HTTP 451) - expected, not a problem. The main series (OKX) is complete; Binance research history comes from the data.binance.vision files.*

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **ZEC**, **XRP**, **BNB**, **SUI**
- **Research only** - backtested, never a signal: UNI, ADA

| Not eligible | 24h volume | Why |
|---|---|---|
| ENA | $64M | 7-day average volume $44M < $50M |
| STRK | $58M | 7-day average volume $15M < $50M; suspended for the rest of the UTC day (moved more than ±25% earlier today); order book too thin: $71k within 1% (need $250k) |
| RLC | $53M | 7-day average volume $18M < $50M; 24h move +37.3% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $41k within 1% (need $250k) |

**Flags (not excluded):** RLC: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, RLUSD, USD1, USDC (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 477 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ETH | 477 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| SOL | 321 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| ZEC | 394 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| XRP | 440 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| BNB | 465 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| SUI | 179 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| UNI | 316 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| ADA | 442 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | up (HH/HL) | 83,529 / 82,400 | 0.68 | 1.55x | 1.21x | bull_engulf, retest_up, failed_breakout_up |
| ETH | up (HH/HL) | 2,520.54 / 2,471.05 | 0.53 | 1.18x | 1.21x | - |
| SOL | up (HH/HL) | 112.06 / 108.8 | 0.57 | 1.15x | 1.46x | - |
| ZEC | down (LH/LL) | 1,247.58 / 1,112.77 | 0.63 | 0.93x | 1.01x | - |
| XRP | down (LH/LL) | 1.4074 / 1.3189 | 0.54 | 1.11x | 1.33x | - |
| BNB | up (HH/HL) | 746.01 / 733.34 | 0.62 | 0.80x | 1.26x | bear_div |
| SUI | up (HH/HL) | 1.0797 / 1.0389 | 0.61 | 1.13x | 1.09x | - |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 434 | 48% | 34% | 27% | 80% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | displacement_down | 329 | 46% | 26% | 17% | 79% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1092 | 46% | 32% | 22% | 76% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | bear_engulf | 1232 | 41% | 26% | 16% | 80% | 46% | 30% | worse than chance | 0.08R |
| 4h | bull_reject | 799 | 44% | 30% | 21% | 77% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | bear_reject | 814 | 47% | 32% | 22% | 74% | 46% | 30% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 569 | 45% | 31% | 23% | 75% | 45% | 30% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bear | 637 | 44% | 29% | 19% | 80% | 46% | 30% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 256 | 46% | 30% | 22% | 82% | 47% | 33% | can't tell from chance | 0.08R |
| 4h | smc_bos_down | 199 | 46% | 31% | 20% | 74% | 46% | 30% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 83 | 52% | 35% | 27% | 83% | 47% | 33% | can't tell from chance | 0.08R |
| 4h | smc_choch_down | 78 | 40% | 21% | 12% | 81% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 601 | 46% | 29% | 23% | 77% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bear | 610 | 47% | 30% | 19% | 76% | 45% | 30% | can't tell from chance | 0.08R |
| 1h | displacement_up | 546 | 47% | 35% | 29% | 73% | 44% | 30% | can't tell from chance | 0.17R |
| 1h | displacement_down | 399 | 37% | 24% | 16% | 81% | 40% | 25% | can't tell from chance | 0.17R |
| 1h | bull_engulf | 1518 | 43% | 30% | 22% | 75% | 44% | 30% | can't tell from chance | 0.19R |
| 1h | bear_engulf | 1682 | 39% | 24% | 17% | 79% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | bull_reject | 1241 | 43% | 30% | 23% | 76% | 45% | 31% | can't tell from chance | 0.18R |
| 1h | bear_reject | 1243 | 37% | 25% | 19% | 80% | 38% | 25% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bull | 570 | 44% | 28% | 20% | 77% | 44% | 30% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bear | 610 | 38% | 25% | 17% | 80% | 38% | 25% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 360 | 46% | 34% | 27% | 77% | 45% | 32% | can't tell from chance | 0.16R |
| 1h | smc_bos_down | 240 | 41% | 29% | 21% | 79% | 38% | 26% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 95 | 45% | 33% | 29% | 77% | 43% | 30% | can't tell from chance | 0.20R |
| 1h | smc_choch_down | 102 | 40% | 28% | 20% | 76% | 36% | 22% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 811 | 47% | 34% | 24% | 72% | 45% | 30% | can't tell from chance | 0.18R |
| 1h | smc_fvg_retrace_bear | 729 | 38% | 27% | 20% | 78% | 38% | 24% | can't tell from chance | 0.20R |
| 30m | displacement_up | 461 | 37% | 26% | 21% | 80% | 43% | 28% | worse than chance | 0.21R |
| 30m | displacement_down | 403 | 42% | 25% | 18% | 81% | 37% | 22% | beats chance | 0.20R |
| 30m | bull_engulf | 1480 | 41% | 26% | 18% | 78% | 43% | 28% | can't tell from chance | 0.23R |
| 30m | bear_engulf | 1587 | 38% | 23% | 17% | 80% | 37% | 23% | can't tell from chance | 0.23R |
| 30m | bull_reject | 1180 | 43% | 28% | 20% | 78% | 42% | 28% | can't tell from chance | 0.23R |
| 30m | bear_reject | 1343 | 38% | 23% | 16% | 80% | 37% | 23% | can't tell from chance | 0.22R |
| 30m | smc_sweep_bull | 619 | 41% | 29% | 20% | 77% | 43% | 28% | can't tell from chance | 0.22R |
| 30m | smc_sweep_bear | 564 | 39% | 25% | 17% | 81% | 38% | 23% | can't tell from chance | 0.21R |
| 30m | smc_bos_up | 352 | 34% | 26% | 22% | 80% | 42% | 27% | worse than chance | 0.23R |
| 30m | smc_bos_down | 248 | 35% | 22% | 15% | 83% | 38% | 24% | can't tell from chance | 0.22R |
| 30m | smc_choch_up | 91 | 35% | 23% | 18% | 82% | 43% | 30% | can't tell from chance | 0.24R |
| 30m | smc_choch_down | 89 | 36% | 24% | 19% | 81% | 40% | 23% | can't tell from chance | 0.22R |
| 30m | smc_fvg_retrace_bull | 878 | 42% | 27% | 19% | 78% | 43% | 29% | can't tell from chance | 0.22R |
| 30m | smc_fvg_retrace_bear | 755 | 37% | 23% | 17% | 81% | 37% | 23% | can't tell from chance | 0.24R |
| 15m | displacement_up | 401 | 33% | 22% | 16% | 87% | 36% | 25% | can't tell from chance | 0.29R |
| 15m | displacement_down | 398 | 37% | 28% | 20% | 79% | 36% | 24% | can't tell from chance | 0.29R |
| 15m | bull_engulf | 1508 | 38% | 26% | 19% | 79% | 37% | 26% | can't tell from chance | 0.32R |
| 15m | bear_engulf | 1509 | 34% | 23% | 16% | 78% | 35% | 23% | can't tell from chance | 0.32R |
| 15m | bull_reject | 1183 | 39% | 29% | 20% | 77% | 37% | 26% | can't tell from chance | 0.34R |
| 15m | bear_reject | 1364 | 33% | 20% | 14% | 82% | 36% | 23% | worse than chance | 0.30R |
| 15m | smc_sweep_bull | 579 | 39% | 30% | 21% | 75% | 37% | 26% | can't tell from chance | 0.29R |
| 15m | smc_sweep_bear | 495 | 37% | 24% | 14% | 82% | 36% | 24% | can't tell from chance | 0.30R |
| 15m | smc_bos_up | 291 | 35% | 24% | 18% | 85% | 38% | 27% | can't tell from chance | 0.31R |
| 15m | smc_bos_down | 295 | 31% | 22% | 18% | 81% | 37% | 24% | worse than chance | 0.31R |
| 15m | smc_choch_up | 80 | 29% | 14% | 9% | 92% | 36% | 26% | can't tell from chance | 0.38R |
| 15m | smc_choch_down | 85 | 35% | 27% | 15% | 79% | 34% | 21% | can't tell from chance | 0.34R |
| 15m | smc_fvg_retrace_bull | 956 | 37% | 27% | 19% | 78% | 37% | 26% | can't tell from chance | 0.33R |
| 15m | smc_fvg_retrace_bear | 829 | 33% | 23% | 16% | 81% | 35% | 23% | can't tell from chance | 0.32R |
| 5m | displacement_up | 1018 | 28% | 19% | 15% | 88% | 29% | 20% | can't tell from chance | 0.59R |
| 5m | displacement_down | 1090 | 26% | 19% | 14% | 84% | 28% | 19% | can't tell from chance | 0.53R |
| 5m | bull_engulf | 3850 | 28% | 18% | 13% | 84% | 29% | 19% | can't tell from chance | 0.59R |
| 5m | bear_engulf | 3730 | 29% | 20% | 14% | 82% | 28% | 20% | can't tell from chance | 0.62R |
| 5m | bull_reject | 2966 | 27% | 19% | 13% | 83% | 28% | 19% | can't tell from chance | 0.63R |
| 5m | bear_reject | 3364 | 28% | 20% | 14% | 82% | 29% | 20% | can't tell from chance | 0.60R |
| 5m | smc_sweep_bull | 1139 | 30% | 19% | 13% | 82% | 29% | 19% | can't tell from chance | 0.51R |
| 5m | smc_sweep_bear | 1082 | 31% | 23% | 15% | 81% | 30% | 21% | can't tell from chance | 0.53R |
| 5m | smc_bos_up | 673 | 26% | 18% | 13% | 88% | 29% | 19% | can't tell from chance | 0.70R |
| 5m | smc_bos_down | 835 | 26% | 19% | 14% | 85% | 29% | 20% | can't tell from chance | 0.56R |
| 5m | smc_choch_up | 195 | 32% | 21% | 18% | 85% | 29% | 19% | can't tell from chance | 0.63R |
| 5m | smc_choch_down | 192 | 26% | 15% | 11% | 89% | 28% | 19% | can't tell from chance | 0.54R |
| 5m | smc_fvg_retrace_bull | 3093 | 28% | 19% | 13% | 83% | 28% | 19% | can't tell from chance | 0.65R |
| 5m | smc_fvg_retrace_bear | 2808 | 26% | 19% | 12% | 83% | 28% | 19% | worse than chance | 0.64R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (strong) | WEAK_BULL (moderate) | TRANSITION (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H UNCLEAR)) |
| **ETH** | WEAK_BULL (weak) | TRANSITION (weak) | WEAK_BEAR (moderate) | TRANSITION (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BEAR, 1H TRANSITION)) |
| **SOL** | WEAK_BULL (moderate) | WEAK_BULL (moderate) | WEAK_BEAR (moderate) | TRANSITION (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H WEAK_BEAR, 1H TRANSITION)) |
| **ZEC** | WEAK_BULL (weak) | WEAK_BULL (weak) | WEAK_BEAR (weak) | WEAK_BEAR (weak) | SHORT allowed (4H/1H bearish, 1W WEAK_BULL) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | WEAK_BEAR (moderate) | WEAK_BEAR (weak) | SHORT allowed (4H/1H bearish, 1W TRANSITION) |
| **BNB** | WEAK_BULL (weak) | WEAK_BULL (moderate) | TRANSITION (weak) | TRANSITION (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H TRANSITION)) |
| **SUI** | UNCLEAR (weak) | TRANSITION (weak) | TRANSITION (weak) | TRANSITION (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)) |
| **UNI** | EXPANSION up (moderate) | TRANSITION (weak) | WEAK_BEAR (moderate) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BEAR, 1H TRANSITION)) |
| **ADA** | UNCLEAR (weak) | TRANSITION (weak) | TRANSITION (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.8 ATR in 10 candles); swing structure down (LH/LL); ADX 28 = strong trend; candle size 0.71x normal, Bollinger width above 62% of the last 100 candles · against: -
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.0 ATR in 10 candles); ADX 40 = strong trend; candle size 1.03x normal, Bollinger width above 37% of the last 100 candles; volume 0.95x normal · against: swing structure mixed (neutral)
- **4H TRANSITION (weak)** - for: swing structure down (LH/LL); ADX 36 = strong trend; candle size 1.03x normal, Bollinger width above 87% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.9 ATR in 10 candles)
- **1H UNCLEAR (weak)** - for: candle size 1.21x normal, Bollinger width above 59% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.1 ATR in 10 candles); swing structure up (HH/HL); ADX 23 = in between (20-25); signals are mixed and trend strength is in between

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | up (CHOCH 14 candles ago) | buy-side (bearish idea) 13 candles ago | bull 82,767.99-82,866.00 (retraced) | bear 85,550.00-86,378.24 | premium (57%) | PDH 83,521.15 (1.0 ATR) | swing low 82,400.00 (1.33 ATR) |
| **ETH** | down (BOS 6 candles ago) | sell-side (bullish idea) 6 candles ago | bull 2,419.83-2,436.13 | bear 2,690.78-2,700.54 | discount (41%) | swing high 2,520.54 (1.56 ATR) | swing low 2,471.05 (1.08 ATR) |
| **SOL** | up (CHOCH 14 candles ago) | sell-side (bullish idea) 6 candles ago | bear 110.72-110.98 (retraced) | bear 120.13-121.29 | discount (40%) | swing high 112.06 (1.66 ATR) | swing low 108.80 (1.08 ATR) |
| **ZEC** | up (BOS 14 candles ago) | sell-side (bullish idea) 17 candles ago | bear 1,228.60-1,233.12 (retraced) | bear 1,302.50-1,348.00 | premium (78%) | swing high 1,247.58 (1.48 ATR) | swing low 1,112.77 (5.34 ATR) |
| **XRP** | down (BOS 6 candles ago) | sell-side (bullish idea) 6 candles ago | bear 1.3915-1.3940 (retraced) | bull 1.2202-1.3441 | premium (73%) | equal highs 1.4088 (1.72 ATR) | swing low 1.3189 (4.47 ATR) |
| **BNB** | down (CHOCH 6 candles ago) | buy-side (bearish idea) 13 candles ago | bull 723.55-725.66 | bear 768.61-773.99 | premium (59%) | swing high 746.01 (1.13 ATR) | swing low 733.34 (1.61 ATR) |
| **SUI** | down (BOS 18 candles ago) | sell-side (bullish idea) 6 candles ago | bear 1.0651-1.0675 (retraced) | bear 1.1264-1.1468 | discount (47%) | swing high 1.0797 (1.36 ATR) | swing low 1.0389 (1.2 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **SIDEWAYS**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 59 (Greed), yesterday 64  (extreme fear/greed = bigger, faster moves)

## 2. Signals right now
Only **APPROVED** strategy versions (your yes, after paper trading) give signals and emails.

**No trade passes all the checks right now. That is normal - no trade is also a position.**

### 2c. Watching - no signal yet (report only, never emailed)
No tracked strategy (VALIDATION or higher) has its market filters open right now.

### 2d. Risk engine (section 15 - independent of the strategies)
- **Live results:** today +0.00R (limit -3R), this week +0.00R (limit -6R) · **halts:** none
- **Suspended strategies** (live drawdown > 8R): none
- **Risk per trade:** 0.5% · leverage never above 3x (the position is made smaller instead)
- **Heat:** max 3 positions, 1 per coin, 1 per group of correlated coins and direction (1h correlation ≥ 0.7) · groups now: BNB+BTC+ETH+SOL+XRP
- **Every live entry also needs:** reward to TP1 ≥ 2R, no opposing level before TP1, no high-impact event within ±60 min, no duplicate
- **Event calendar (next 7 days):** US CPI (Sep data) 2026-10-14 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-10-09 01:00 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PB-C-BREAKOUT-W20 | 1.0 | 5m | **BACKTESTING** | 1 | 100.0 | +0.351 | 99.0 | 0.0R | +0.35 / +0.00 | +0.35 / +0.00 | 0/5 ✗ | +0.30 | +0.25 | stable | 0 | 0.85R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | not cost-viable: fees + slippage 0.85R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1147 | 39.6 | +0.180 | 1.33 | 31.3R | +0.18 / +0.18 | +0.20 / +0.16 | 5/5 | +0.15 | +0.13 | stable | 9 | 0.04R | 3, -1.05 (-1.05 / -1.04) | 89 / 50 of 244 | 0 | max drawdown 31.3R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1301 | 39.0 | +0.180 | 1.33 | 29.4R | +0.19 / +0.17 | +0.18 / +0.18 | 5/5 | +0.15 | +0.13 | stable | 9 | 0.04R | 4, -1.04 (-1.04 / -1.04) | 153 / 63 of 333 | 0 | max drawdown 29.4R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 4h | **BACKTESTING** | 967 | 38.9 | +0.165 | 1.3 | 25.1R | +0.17 / +0.16 | +0.15 / +0.18 | 4/5 | +0.14 | +0.12 | stable | 8 | 0.03R | 3, -1.03 (-1.03 / -1.04) | 103 / 43 of 240 | 0 | max drawdown 25.1R |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1176 | 53.7 | +0.106 | 1.24 | 26.1R | +0.10 / +0.12 | +0.10 / +0.12 | 5/5 | +0.08 | +0.06 | stable | 7 | 0.04R | 4, -0.69 (-0.57 / -1.04) | 89 / 50 of 244 | 0 | max drawdown 26.1R |
| TRD-H4-BREAKOUT | 1.0 | 30m | **BACKTESTING** | 490 | 39.2 | +0.099 | 1.15 | 28.1R | +0.05 / +0.26 | +0.19 / +0.02 | 4/5 | +0.09 | +0.06 | stable | 7 | 0.05R | 4, +1.04 (+1.74 / -1.05) | 9 / 9 of 84 | 0 | avg +0.10R/trade (needs +0.10R); profit factor 1.15; max drawdown 28.1R |
| TRD-H4-BREAKOUT | 1.0 | 1h | **BACKTESTING** | 1119 | 37.4 | +0.083 | 1.13 | 60.8R | +0.01 / +0.23 | +0.13 / +0.03 | 4/5 | +0.06 | +0.04 | stable | 7 | 0.04R | 3, +0.09 (+0.09 / +0.00) | 6 / 2 of 93 | 0 | avg +0.08R/trade (needs +0.10R); profit factor 1.13; max drawdown 60.8R |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 1h | **BACKTESTING** | 3660 | 37.1 | +0.034 | 1.05 | 89.3R | +0.02 / +0.07 | +0.08 / -0.01 | 4/5 | +0.01 | -0.02 | ✗  stop atr 2.0→1.6: -0.00R | 5 | 0.04R | 18, -0.31 (-0.43 / +0.62) | 156 / 514 of 908 | 0 | avg +0.03R/trade (needs +0.10R); profit factor 1.05; max drawdown 89.3R |
| TRD-H4-PULLBACK | 1.0 | 15m | **BACKTESTING** | 1277 | 39.1 | +0.031 | 1.05 | 93.4R | -0.04 / +0.25 | +0.01 / +0.05 | 3/5 | +0.01 | -0.01 | stable | 6 | 0.08R | 14, +0.13 (+0.16 / -0.07) | 40 / 26 of 303 | 0 | avg +0.03R/trade (needs +0.10R); profit factor 1.05; max drawdown 93.4R; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-CVD | 1.0 | 5m | **BACKTESTING** | 13 | 53.8 | +0.026 | 1.05 | 4.8R | +0.12 / -1.10 | +0.42 / -0.09 | 0/5 ✗ | -0.06 | +0.52 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 13 trades; avg +0.03R/trade (needs +0.15R); profit factor 1.05; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 4 of 11 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 4 of 11 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-noCVD | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 10, -0.66 (-0.66 / +0.00) | 0 / 0 of 44 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT-noCVD | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 25 | 36.0 | -0.063 | 0.92 | 12.7R | -0.75 / +1.39 | +0.88 / -0.43 | 1/5 ✗ | -0.86 | -12.20 | ✗  stop buffer_atr 0.2→0.24: -0.41R | 1 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 37 / 14 of 57 | 0 | only 25 trades; avg -0.06R/trade (needs +0.10R); profit factor 0.92; max drawdown 12.7R; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK | 1.0 | 5m | **BACKTESTING** | 16 | 50.0 | -0.099 | 0.83 | 6.2R | -0.03 / -1.10 | +0.43 / -0.27 | 0/5 ✗ | -0.15 | +0.30 | ✗  stop buffer_atr 0.0→0.0: -0.10R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 16 trades; avg -0.10R/trade (needs +0.15R); profit factor 0.83; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 7 | 28.6 | -0.116 | 0.86 | 4.6R | -0.51 / +2.24 | +1.21 / -1.11 | 0/5 ✗ | -0.19 | -33.22 | ✗  stop buffer_atr 0.2→0.24: -0.13R | 0 | 0.15R | 0, +0.00 (+0.00 / +0.00) | 12 / 8 of 22 | 0 | only 7 trades; avg -0.12R/trade (needs +0.10R); profit factor 0.86; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-APLUS | 1.0 | 5m | **BACKTESTING** | 79 | 43.0 | -0.193 | 0.68 | 19.8R | -0.18 / -0.26 | +0.10 / -0.39 | 0/5 ✗ | -0.28 | -0.33 | ✗  time_stop_bars 48→38: -0.21R | 3 | 0.18R | 1, +1.53 (+0.00 / +1.53) | 0 / 0 of 1 | 0 | only 79 trades; avg -0.19R/trade (needs +0.15R); profit factor 0.68; max drawdown 19.8R; not profitable in BOTH train and unseen test |
| PB-A-GRADED | 1.0 | 5m | **BACKTESTING** | 98 | 43.9 | -0.196 | 0.67 | 23.7R | -0.19 / -0.24 | +0.01 / -0.31 | 0/5 ✗ | -0.29 | -0.33 | ✗  time_stop_bars 48→38: -0.21R | 2 | 0.18R | 1, +1.53 (+0.00 / +1.53) | 0 / 0 of 1 | 0 | only 98 trades; avg -0.20R/trade (needs +0.15R); profit factor 0.67; max drawdown 23.7R; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 13 | 38.5 | -0.202 | 0.81 | 9.3R | +0.14 / -4.33 | -0.70 / +0.11 | 1/5 ✗ | -0.33 | -2.25 | ✗  stop buffer_atr 0.2→0.16: -2.45R | 0 | 0.24R | 0, +0.00 (+0.00 / +0.00) | 44 / 9 of 58 | 0 | only 13 trades; avg -0.20R/trade (needs +0.10R); profit factor 0.81; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 3 | 33.3 | -0.266 | 0.65 | 1.2R | -0.27 / +0.00 | -1.22 / +0.21 | 0/5 ✗ | -0.35 | -1.12 | ✗  stop buffer_atr 0.2→0.24: -0.27R | 0 | 0.26R | 0, +0.00 (+0.00 / +0.00) | 44 / 9 of 58 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 3 trades; avg -0.27R/trade (needs +0.10R); profit factor 0.65; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-LDN | 1.0 | 5m | **BACKTESTING** | 30 | 40.0 | -0.405 | 0.47 | 17.9R | -0.29 / -0.88 | -0.23 / -0.49 | 0/5 ✗ | -0.50 | -0.51 | ✗  stop buffer_atr 0.0→0.0: -0.41R | 2 | 0.24R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 30 trades; avg -0.40R/trade (needs +0.15R); profit factor 0.47; max drawdown 17.9R; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 14 | 28.6 | -0.433 | 0.34 | 7.1R | -0.42 / -0.44 | -0.38 / -0.45 | 0/5 ✗ | -0.61 | -0.57 | ✗  stop buffer_atr 0.2→0.24: -0.54R | 0 | 0.12R | 0, +0.00 (+0.00 / +0.00) | 476 / 185 of 768 | 0 | only 14 trades; avg -0.43R/trade (needs +0.10R); profit factor 0.34; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 7 | 28.6 | -0.440 | 0.51 | 3.2R | +0.05 / -0.64 | -0.50 / -0.35 | 0/5 ✗ | -0.47 | -0.57 | ✗  stop buffer_atr 0.2→0.24: -0.60R | 0 | 0.20R | 1, +1.97 (+1.97 / +0.00) | 34 / 100 of 142 | 0 | only 7 trades; avg -0.44R/trade (needs +0.10R); profit factor 0.51; only 5 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-GRADED | 1.0 | 5m | **BACKTESTING** | 12 | 25.0 | -0.609 | 0.26 | 9.0R | -0.50 / -1.16 | -0.75 / -0.33 | 0/5 ✗ | -0.04 | -0.24 | ✗  stop buffer_atr 0.0→0.0: -0.61R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 2 | 0 | only 12 trades; avg -0.61R/trade (needs +0.15R); profit factor 0.26; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 9 | 11.1 | -0.625 | 0.39 | 6.9R | -0.47 / -1.17 | -1.22 / -0.45 | 0/5 ✗ | -0.62 | -0.69 | ✗  sweep_bars 20→16: -0.62R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 61 / 16 of 79 | 0 | only 9 trades; avg -0.62R/trade (needs +0.10R); profit factor 0.39; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-APLUS | 1.0 | 5m | **BACKTESTING** | 2 | 0.0 | -0.858 | 0.0 | 1.7R | -0.86 / +0.00 | -0.64 / -1.07 | 0/5 ✗ | -1.11 | -1.15 | ✗  stop buffer_atr 0.0→0.0: -0.86R | 0 | 0.15R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 2 trades; avg -0.86R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 1 | 0.0 | -1.059 | 0.0 | 1.1R | -1.06 / +0.00 | +0.00 / -1.06 | 0/5 ✗ | -1.09 | -1.12 | ✗  stop buffer_atr 0.2→0.16: -1.06R | 0 | 0.07R | 0, +0.00 (+0.00 / +0.00) | 12 / 8 of 22 | 0 | only 1 trades; avg -1.06R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.208 | 0.0 | 1.2R | -1.21 / +0.00 | -1.21 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.2→0.16: -1.21R | 0 | 0.27R | 0, +0.00 (+0.00 / +0.00) | 61 / 16 of 79 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.21R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **FAILED** | 36 | 55.6 | +0.455 | 2.01 | 3.7R | +0.68 / -0.05 | +0.92 / +0.04 | 3/5 | +0.36 | +0.31 | stable | 2 | 0.15R | 0, +0.00 (+0.00 / +0.00) | 443 / 169 of 698 | 0 | not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 1h | **FAILED** | 1109 | 37.8 | +0.028 | 1.05 | 51.1R | +0.05 / -0.02 | -0.05 / +0.11 | 2/5 ✗ | +0.01 | -0.02 | ✗  stop atr 2.0→1.6: -0.01R | 5 | 0.04R | 2, -0.04 (+0.97 / -1.05) | 25 / 26 of 190 | 0 | avg +0.03R/trade (needs +0.10R); profit factor 1.05; max drawdown 51.1R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 289 | 50.9 | +0.011 | 1.02 | 31.5R | +0.14 / -0.24 | +0.12 / -0.09 | 2/5 ✗ | -0.03 | -0.07 | ✗  stop atr 1.5→1.8: -0.02R | 5 | 0.06R | 1, -1.04 (-1.04 / +0.00) | 106 / 23 of 144 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.02; max drawdown 31.5R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 30m | **FAILED** | 1624 | 36.7 | -0.006 | 0.99 | 101.5R | -0.04 / +0.10 | +0.06 / -0.07 | 3/5 | -0.04 | -0.06 | ✗  stop atr 2.0→1.6: -0.03R | 6 | 0.07R | 25, -0.18 (-0.22 / -0.01) | 113 / 549 of 878 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; max drawdown 101.5R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 30m | **FAILED** | 1192 | 34.3 | -0.006 | 0.99 | 64.4R | -0.02 / +0.04 | +0.14 / -0.13 | 3/5 | -0.06 | -0.11 | ✗  stop atr 2.0→1.6: -0.04R | 4 | 0.10R | 16, -0.21 (-0.44 / +0.18) | 149 / 59 of 324 | 0 | avg -0.01R/trade (needs +0.12R); profit factor 0.99; max drawdown 64.4R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 877 | 52.0 | -0.008 | 0.99 | 44.3R | -0.01 / -0.01 | -0.01 / -0.00 | 2/5 ✗ | -0.08 | -0.14 | ✗  bb_n 20→24: -0.03R | 5 | 0.12R | 5, +0.16 (+0.16 / +0.00) | 137 / 31 of 202 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; max drawdown 44.3R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 1h | **FAILED** | 5197 | 37.6 | -0.009 | 0.99 | 189.3R | +0.01 / -0.06 | -0.02 / +0.01 | 1/5 ✗ | -0.04 | -0.07 | ✗  stop atr 2.0→1.6: -0.03R | 4 | 0.05R | 28, -0.11 (+0.06 / -1.10) | 617 / 2647 of 3687 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; max drawdown 189.3R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 202 | 51.5 | -0.018 | 0.97 | 32.6R | -0.14 / +0.24 | -0.03 / -0.01 | 2/5 ✗ | -0.06 | -0.12 | ✗  stop atr 1.5→1.2: -0.07R | 4 | 0.10R | 0, +0.00 (+0.00 / +0.00) | 205 / 7 of 214 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 32.6R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1271 | 34.1 | -0.018 | 0.97 | 96.3R | -0.04 / +0.04 | +0.09 / -0.12 | 2/5 ✗ | -0.07 | -0.13 | ✗  stop atr 2.0→1.6: -0.05R | 5 | 0.10R | 21, -0.29 (-0.57 / +0.09) | 122 / 70 of 336 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 96.3R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 3538 | 33.0 | -0.019 | 0.97 | 223.6R | -0.04 / +0.03 | +0.02 / -0.06 | 3/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.04R | 4 | 0.07R | 13, -0.23 (-0.52 / +0.70) | 200 / 124 of 514 | 0 | avg -0.02R/trade (needs +0.12R); profit factor 0.97; max drawdown 223.6R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 1h | **FAILED** | 2686 | 32.9 | -0.019 | 0.97 | 189.4R | -0.05 / +0.05 | +0.02 / -0.06 | 2/5 ✗ | -0.06 | -0.09 | ✗  stop atr 2.0→1.6: -0.04R | 4 | 0.07R | 7, +0.28 (+0.13 / +0.68) | 142 / 94 of 376 | 0 | avg -0.02R/trade (needs +0.12R); profit factor 0.97; max drawdown 189.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 3127 | 32.7 | -0.022 | 0.96 | 192.6R | -0.05 / +0.05 | +0.01 / -0.06 | 2/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.06R | 5 | 0.07R | 9, -0.22 (-0.68 / +0.70) | 114 / 95 of 368 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 192.6R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 3214 | 49.1 | -0.023 | 0.95 | 123.8R | -0.04 / +0.01 | -0.01 / -0.03 | 1/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.07R | 10, -0.07 (-0.49 / +0.56) | 114 / 95 of 368 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.95; max drawdown 123.8R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1492 | 34.1 | -0.026 | 0.96 | 96.3R | -0.04 / +0.01 | +0.08 / -0.12 | 2/5 ✗ | -0.09 | -0.15 | ✗  stop atr 2.0→1.6: -0.07R | 4 | 0.11R | 26, -0.18 (-0.32 / +0.09) | 212 / 89 of 466 | 0 | avg -0.03R/trade (needs +0.12R); profit factor 0.96; max drawdown 96.3R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 43 | 51.2 | -0.036 | 0.93 | 6.7R | +0.19 / -0.55 | +0.31 / -0.37 | 3/5 ✗ | -0.06 | -0.09 | ✗  stop atr 1.5→1.8: -0.07R | 2 | 0.06R | 1, +0.31 (+0.31 / +0.00) | 137 / 4 of 142 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.93; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 30m | **FAILED** | 679 | 34.9 | -0.040 | 0.94 | 95.8R | -0.08 / +0.10 | -0.06 / -0.02 | 3/5 ✗ | -0.05 | -0.06 | ✗  time_stop_bars 48→38: -0.06R | 4 | 0.06R | 4, +0.57 (+0.44 / +0.95) | 32 / 25 of 254 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; max drawdown 95.8R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1310 | 48.2 | -0.043 | 0.92 | 94.3R | -0.05 / -0.03 | +0.03 / -0.11 | 2/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.10R | 21, -0.30 (-0.51 / -0.03) | 122 / 70 of 336 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.92; max drawdown 94.3R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 99 | 46.5 | -0.048 | 0.91 | 15.8R | +0.08 / -0.31 | -0.13 / +0.06 | 2/5 ✗ | -0.07 | -0.09 | ✗  time_stop_bars 60→48: -0.05R | 2 | 0.04R | 1, -1.14 (-1.14 / +0.00) | 36 / 6 of 45 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 15.8R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 5m | **FAILED** | 3217 | 37.5 | -0.054 | 0.92 | 316.1R | -0.08 / +0.02 | -0.07 / -0.04 | 1/5 ✗ | -0.06 | -0.10 | ✗  time_stop_bars 48→38: -0.07R | 1 | 0.12R | 41, -0.31 (-0.28 / -0.44) | 46 / 65 of 404 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 316.1R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1312 | 48.2 | -0.058 | 0.89 | 118.4R | -0.02 / -0.15 | +0.02 / -0.14 | 1/5 ✗ | -0.10 | -0.13 | ✗  long_rsi_hi 65→52: -0.15R | 3 | 0.05R | 13, -0.47 (-0.42 / -1.04) | 623 / 181 of 962 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 118.4R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 78 | 41.0 | -0.065 | 0.89 | 10.2R | -0.09 / +0.01 | -0.03 / -0.14 | 3/5 | -0.12 | -0.12 | ✗  stop max_width_atr 3.0→3.6: -0.08R | 5 | 0.11R | 2, -1.24 (-1.24 / +0.00) | 104 / 35 of 151 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.89; max drawdown 10.2R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 30m | **FAILED** | 2625 | 35.0 | -0.066 | 0.9 | 213.6R | -0.04 / -0.13 | -0.04 / -0.09 | 1/5 ✗ | -0.10 | -0.13 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.07R | 46, -0.27 (+0.02 / -0.92) | 469 / 2552 of 3565 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.90; max drawdown 213.6R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 15m | **FAILED** | 4646 | 36.3 | -0.070 | 0.9 | 409.5R | -0.08 / -0.05 | -0.05 / -0.09 | 1/5 ✗ | -0.11 | -0.14 | ✗  time_stop_bars 48→58: -0.08R | 1 | 0.10R | 70, -0.31 (-0.15 / -0.75) | 484 / 2659 of 3716 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.90; max drawdown 409.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 311 | 33.1 | -0.085 | 0.89 | 56.8R | +0.01 / -0.30 | -0.23 / +0.06 | 1/5 ✗ | -0.17 | -0.26 | ✗  time_stop_bars 30→36: -0.10R | 4 | 0.16R | 3, +0.80 (+0.80 / +0.00) | 77 / 201 of 288 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.89; max drawdown 56.8R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 15m | **FAILED** | 2826 | 33.6 | -0.091 | 0.87 | 301.9R | -0.10 / -0.06 | -0.04 / -0.14 | 0/5 ✗ | -0.14 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 1 | 0.10R | 47, -0.50 (-0.35 / -0.87) | 97 / 605 of 870 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.87; max drawdown 301.9R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 15m | **FAILED** | 870 | 33.1 | -0.093 | 0.87 | 87.1R | -0.09 / -0.09 | -0.02 / -0.16 | 1/5 ✗ | -0.12 | -0.16 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.08R | 11, -0.62 (-0.52 / -1.09) | 5 / 8 of 79 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.87; max drawdown 87.1R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1967 | 56.9 | -0.096 | 0.66 | 189.7R | -0.10 / -0.10 | -0.11 / -0.09 | 0/5 ✗ | -0.12 | -0.15 | ✗  stop atr 2.0→1.6: -0.12R | 0 | 0.04R | 13, -0.37 (+0.21 / -1.04) | 689 / 6 of 919 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.66; max drawdown 189.7R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 7343 | 56.1 | -0.104 | 0.62 | 769.5R | -0.09 / -0.14 | -0.10 / -0.11 | 0/5 ✗ | -0.16 | -0.21 | ✗  stop atr 2.0→1.6: -0.12R | 0 | 0.09R | 34, -0.07 (-0.03 / -0.20) | 934 / 12 of 1257 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.62; max drawdown 769.5R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 5m | **FAILED** | 1961 | 35.4 | -0.106 | 0.85 | 248.9R | -0.13 / -0.02 | -0.04 / -0.16 | 1/5 ✗ | -0.16 | -0.19 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.13R | 21, +0.22 (+0.25 / +0.05) | 8 / 14 of 94 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.85; max drawdown 248.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6705 | 47.3 | -0.111 | 0.8 | 762.5R | -0.11 / -0.10 | -0.13 / -0.09 | 0/5 ✗ | -0.17 | -0.22 | ✗  stop atr 1.5→1.2: -0.14R | 0 | 0.11R | 33, -0.18 (+0.23 / -0.82) | 1098 / 253 of 1703 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.80; max drawdown 762.5R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 5m | **FAILED** | 9790 | 36.3 | -0.111 | 0.84 | 1100.9R | -0.12 / -0.08 | -0.10 / -0.12 | 0/5 ✗ | -0.15 | -0.16 | ✗  time_stop_bars 48→38: -0.12R | 0 | 0.15R | 117, -0.32 (-0.44 / +0.04) | 1177 / 7188 of 9577 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.84; max drawdown 1100.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 357 | 44.0 | -0.124 | 0.77 | 52.2R | -0.14 / -0.10 | -0.18 / -0.07 | 0/5 ✗ | -0.18 | -0.23 | ✗  slow 21→17: -0.21R | 3 | 0.10R | 1, -1.18 (+0.00 / -1.18) | 112 / 6 of 126 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.77; max drawdown 52.2R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 216 | 39.8 | -0.126 | 0.8 | 47.8R | -0.18 / +0.13 | +0.10 / -0.29 | 2/5 ✗ | -0.20 | -0.25 | ✗  bb_k 2→3: -0.28R | 2 | 0.10R | 3, +0.17 (+0.79 / -1.07) | 83 / 7 of 95 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.80; max drawdown 47.8R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 5m | **FAILED** | 5755 | 34.5 | -0.133 | 0.82 | 789.6R | -0.15 / -0.08 | -0.10 / -0.16 | 0/5 ✗ | -0.17 | -0.17 | ✗  time_stop_bars 48→58: -0.14R | 0 | 0.15R | 62, -0.25 (-0.09 / -0.55) | 269 / 1721 of 2308 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.82; max drawdown 789.6R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 300 | 48.3 | -0.139 | 0.76 | 54.6R | -0.08 / -0.33 | -0.18 / -0.10 | 1/5 ✗ | -0.24 | -0.33 | ✗  stop atr 1.5→1.2: -0.17R | 3 | 0.18R | 6, -0.71 (-0.53 / -0.80) | 154 / 9 of 176 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 54.6R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 860 | 31.3 | -0.149 | 0.81 | 163.1R | -0.11 / -0.22 | -0.11 / -0.18 | 1/5 ✗ | -0.24 | -0.32 | ✗  stop buffer_atr 0.2→0.16: -0.20R | 1 | 0.18R | 6, -0.24 (-0.33 / -0.07) | 383 / 1045 of 1506 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.81; max drawdown 163.1R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 286 | 46.5 | -0.151 | 0.73 | 49.3R | -0.14 / -0.17 | -0.26 / -0.07 | 1/5 ✗ | -0.21 | -0.25 | ✗  stop atr 2.0→1.6: -0.18R | 3 | 0.08R | 1, +0.24 (+0.24 / +0.00) | 45 / 2 of 55 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.73; max drawdown 49.3R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3522 | 47.1 | -0.155 | 0.74 | 550.0R | -0.14 / -0.20 | -0.14 / -0.17 | 0/5 ✗ | -0.25 | -0.33 | ✗  stop atr 1.5→1.2: -0.19R | 0 | 0.15R | 66, -0.43 (-0.39 / -0.51) | 788 / 241 of 1508 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.74; max drawdown 550.0R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2847 | 49.9 | -0.157 | 0.47 | 450.4R | -0.14 / -0.20 | -0.16 / -0.15 | 0/5 ✗ | -0.24 | -0.32 | ✗  stop atr 2.0→1.6: -0.20R | 0 | 0.14R | 44, -0.27 (-0.26 / -0.33) | 1007 / 36 of 1207 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.47; max drawdown 450.4R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 527 | 47.4 | -0.162 | 0.73 | 88.1R | -0.18 / -0.12 | -0.12 / -0.20 | 1/5 ✗ | -0.26 | -0.36 | ✗  stop atr 1.5→1.2: -0.23R | 2 | 0.17R | 11, -0.06 (-0.16 / +1.00) | 95 / 34 of 174 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.73; max drawdown 88.1R; not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 5m | **FAILED** | 1415 | 36.5 | -0.165 | 0.64 | 237.0R | -0.19 / -0.08 | -0.20 / -0.13 | 0/5 ✗ | -0.21 | -0.19 | ✗  stop max_width_atr 3.0→2.4: -0.17R | 0 | 0.18R | 16, -0.18 (-0.11 / -1.23) | 0 / 0 of 375 | 0 | avg -0.17R/trade (needs +0.15R); profit factor 0.64; max drawdown 237.0R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-LIMIT | 1.0 | 5m | **FAILED** | 359 | 39.0 | -0.171 | 0.65 | 65.3R | -0.18 / -0.13 | -0.21 / -0.13 | 0/5 ✗ | -0.32 | -0.29 | ✗  stop max_width_atr 3.0→2.4: -0.17R | 2 | 0.19R | 3, -0.76 (-0.76 / +0.00) | 0 / 0 of 44 | 0 | avg -0.17R/trade (needs +0.15R); profit factor 0.65; max drawdown 65.3R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 162 | 46.3 | -0.175 | 0.7 | 30.3R | -0.14 / -0.29 | -0.20 / -0.16 | 1/5 ✗ | -0.22 | -0.28 | ✗  st_k 3→4: -0.19R | 1 | 0.11R | 4, -0.55 (-0.03 / -1.07) | 46 / 6 of 63 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.70; max drawdown 30.3R; not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 15m | **FAILED** | 118 | 43.2 | -0.187 | 0.67 | 25.1R | -0.15 / -0.30 | -0.20 / -0.17 | 0/5 ✗ | -0.26 | -0.15 | ✗  stop buffer_atr 0.0→0.0: -0.19R | 3 | 0.18R | 2, -1.16 (-1.16 / +0.00) | 0 / 0 of 22 | 0 | avg -0.19R/trade (needs +0.15R); profit factor 0.67; max drawdown 25.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 312 | 46.8 | -0.188 | 0.69 | 62.5R | -0.20 / -0.15 | -0.17 / -0.22 | 0/5 ✗ | -0.25 | -0.32 | ✗  vol_x 1.2→1.44: -0.31R | 3 | 0.14R | 1, +1.11 (+0.00 / +1.11) | 77 / 175 of 260 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.69; max drawdown 62.5R; not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 5m | **FAILED** | 300 | 36.3 | -0.189 | 0.62 | 59.6R | -0.20 / -0.17 | -0.21 / -0.17 | 0/5 ✗ | -0.30 | -0.22 | ✗  stop max_width_atr 3.0→2.4: -0.20R | 2 | 0.18R | 3, -0.76 (-0.76 / +0.00) | 0 / 0 of 38 | 0 | avg -0.19R/trade (needs +0.15R); profit factor 0.62; max drawdown 59.6R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 178 | 33.1 | -0.194 | 0.72 | 46.8R | -0.25 / +0.04 | -0.03 / -0.30 | 1/5 ✗ | -0.24 | -0.29 | ✗  depth 0.985→1.182: -0.34R | 2 | 0.11R | 6, -0.39 (-0.04 / -1.09) | 27 / 4 of 37 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.72; max drawdown 46.8R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 363 | 40.5 | -0.201 | 0.65 | 74.9R | -0.18 / -0.27 | -0.23 / -0.18 | 1/5 ✗ | -0.29 | -0.36 | ✗  slow 21→25: -0.28R | 0 | 0.15R | 8, -0.97 (-1.08 / -0.95) | 89 / 24 of 134 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.65; max drawdown 74.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 5984 | 45.9 | -0.214 | 0.66 | 1279.0R | -0.22 / -0.18 | -0.21 / -0.21 | 0/5 ✗ | -0.34 | -0.46 | ✗  stop atr 1.5→1.2: -0.28R | 0 | 0.22R | 99, -0.59 (-0.53 / -0.73) | 1344 / 291 of 2143 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.66; max drawdown 1279.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 897 | 43.0 | -0.215 | 0.64 | 196.1R | -0.23 / -0.18 | -0.27 / -0.16 | 0/5 ✗ | -0.33 | -0.45 | ✗  stop atr 1.5→1.2: -0.30R | 1 | 0.22R | 14, -0.84 (-0.91 / -0.81) | 87 / 19 of 122 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.64; max drawdown 196.1R; not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 15m | **FAILED** | 564 | 37.6 | -0.218 | 0.61 | 126.8R | -0.23 / -0.17 | -0.23 / -0.20 | 0/5 ✗ | -0.18 | -0.20 | ✗  stop max_width_atr 3.0→2.4: -0.22R | 0 | 0.18R | 8, -0.14 (-0.14 / +0.00) | 0 / 0 of 220 | 0 | avg -0.22R/trade (needs +0.15R); profit factor 0.61; max drawdown 126.8R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 4492 | 42.5 | -0.241 | 0.32 | 1083.2R | -0.22 / -0.30 | -0.25 / -0.23 | 0/5 ✗ | -0.37 | -0.49 | ✗  stop atr 2.0→1.6: -0.30R | 0 | 0.21R | 112, -0.33 (-0.32 / -0.38) | 1140 / 49 of 1361 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.32; max drawdown 1083.2R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1532 | 31.9 | -0.277 | 0.64 | 430.3R | -0.29 / -0.24 | -0.25 / -0.30 | 0/5 ✗ | -0.39 | -0.49 | ✗  bb_k 2→3: -0.33R | 0 | 0.18R | 33, -0.31 (+0.12 / -1.06) | 590 / 29 of 705 | 0 | avg -0.28R/trade (needs +0.10R); profit factor 0.64; max drawdown 430.3R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 1203 | 44.9 | -0.291 | 0.57 | 351.7R | -0.29 / -0.29 | -0.26 / -0.32 | 0/5 ✗ | -0.42 | -0.55 | ✗  stop atr 1.5→1.2: -0.37R | 0 | 0.25R | 14, -0.27 (-0.45 / +0.20) | 99 / 43 of 181 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.29R/trade (needs +0.10R); profit factor 0.57; max drawdown 351.7R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1318 | 28.4 | -0.309 | 0.6 | 408.7R | -0.34 / -0.23 | -0.28 / -0.33 | 0/5 ✗ | -0.38 | -0.44 | ✗  rsi_n 14→17: -0.40R | 1 | 0.12R | 9, -0.15 (+0.68 / -1.20) | 690 / 5 of 736 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.60; max drawdown 408.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 360 | 43.1 | -0.329 | 0.52 | 118.3R | -0.28 / -0.46 | -0.33 / -0.33 | 0/5 ✗ | -0.44 | -0.53 | ✗  vol_x 1.2→1.44: -0.36R | 2 | 0.23R | 5, -1.18 (-1.14 / -1.34) | 101 / 213 of 332 | 0 | avg -0.33R/trade (needs +0.10R); profit factor 0.52; max drawdown 118.3R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 595 | 27.1 | -0.416 | 0.54 | 247.4R | -0.38 / -0.53 | -0.46 / -0.38 | 0/5 ✗ | -0.56 | -0.66 | ✗  stop buffer_atr 0.2→0.16: -0.43R | 0 | 0.28R | 12, -0.59 (-0.50 / -0.71) | 407 / 1018 of 1593 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.42R/trade (needs +0.10R); profit factor 0.54; max drawdown 247.4R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 133 | 22.6 | -0.430 | 0.54 | 58.9R | -0.36 / -0.59 | -0.63 / -0.21 | 1/5 ✗ | -0.54 | -0.64 | ✗  time_stop_bars 30→24: -0.46R | 1 | 0.23R | 3, +0.04 (+0.80 / -1.47) | 34 / 100 of 142 | 0 | avg -0.43R/trade (needs +0.10R); profit factor 0.54; max drawdown 58.9R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-15M | 1.0 | 15m | **FAILED** | 303 | 39.3 | -0.448 | 0.4 | 141.8R | -0.40 / -0.60 | -0.43 / -0.46 | 0/5 ✗ | -0.54 | -0.65 | ✗  stop buffer_atr 0.0→0.0: -0.45R | 0 | 0.43R | 6, -1.29 (-1.29 / +0.00) | 0 / 0 of 25 | 0 | not cost-viable: fees + slippage 0.43R per trade (stop must be ≥ 4x the round-trip cost); avg -0.45R/trade (needs +0.15R); profit factor 0.40; max drawdown 141.8R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 2349 | 37.1 | -0.460 | 0.41 | 1081.8R | -0.45 / -0.49 | -0.48 / -0.44 | 0/5 ✗ | -0.69 | -0.90 | ✗  stop atr 1.5→1.2: -0.57R | 0 | 0.39R | 47, -0.69 (-0.59 / -0.88) | 200 / 63 of 311 | 0 | not cost-viable: fees + slippage 0.39R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.41; max drawdown 1081.8R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 1260 | 39.8 | -0.464 | 0.4 | 585.2R | -0.43 / -0.56 | -0.44 / -0.49 | 0/5 ✗ | -0.65 | -0.85 | ✗  stop atr 1.0→0.8: -0.54R | 0 | 0.34R | 16, -0.69 (-0.60 / -0.89) | 77 / 255 of 361 | 0 | not cost-viable: fees + slippage 0.34R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.40; max drawdown 585.2R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP | 1.0 | 5m | **FAILED** | 1341 | 34.3 | -0.621 | 0.25 | 833.1R | -0.63 / -0.59 | -0.62 / -0.62 | 0/5 ✗ | -0.77 | -0.88 | ✗  stop max_width_atr 3.0→2.4: -0.62R | 0 | 0.59R | 10, -0.66 (-0.66 / +0.00) | 0 / 0 of 44 | 0 | not cost-viable: fees + slippage 0.59R per trade (stop must be ≥ 4x the round-trip cost); avg -0.62R/trade (needs +0.15R); profit factor 0.25; max drawdown 833.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 4484 | 34.3 | -0.652 | 0.31 | 2921.6R | -0.64 / -0.70 | -0.66 / -0.65 | 0/5 ✗ | -1.03 | -1.39 | ✗  stop atr 1.0→0.8: -0.83R | 0 | 0.61R | 63, -0.98 (-0.92 / -1.08) | 209 / 607 of 903 | 0 | not cost-viable: fees + slippage 0.61R per trade (stop must be ≥ 4x the round-trip cost); avg -0.65R/trade (needs +0.10R); profit factor 0.31; max drawdown 2921.6R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **49** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 210 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.49** (Bonferroni: family-wise false-winner rate 0.05 over 210 trials; with 1 trial it would be 1.65).

**Research run duration:** 57.6 min (budget 90 min); rule test skipped for AVAX to stay inside it.

**Lookahead / recursive check** (on BTC): 45 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (310.0 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 54 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

1 of 93 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **VALIDATION** | 4.78 | 16.8R | 630 d (19%) | multiple-testing bar: t-statistic 3.29 of the average trade, needs 3.49 after 210 trials |

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- PB-A-GRADED v1.0 5m = near-duplicate of PB-A-APLUS v1.0 5m (81% of 98 trades shared)

- PB-B-SWEEP-LIMIT v1.0 5m = near-duplicate of PB-B-APLUS v1.0 5m (79% of 359 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (80% of 3,538 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (77% of 1,492 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (81% of 1,301 trades shared)

- donchian_breakout-VEXIT-S4 v1.1 30m = near-duplicate of donchian_breakout v1.0 30m (70% of 1,192 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 3,127 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,271 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 1,147 trades shared)

🧪 **Strategy lab:** 5 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| TRD-H4-BREAKOUT | 30m | 490 | +0.099 | +0.259 | -0.006 | +0.098 | yes |
| TRD-H4-BREAKOUT | 1h | 1119 | +0.083 | +0.231 | +0.034 | +0.068 | yes |
| TRD-H4-PULLBACK | 15m | 1277 | +0.031 | +0.254 | -0.070 | -0.047 | yes |
| PB-A-PULLBACK-CVD | 5m | 13 | +0.026 | -1.097 | -0.099 | -1.097 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.065 | +0.006 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| PB-C-BREAKOUT | 5m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET | 15m | 7 | -0.116 | +2.244 | -0.063 | +1.394 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 13 | -0.202 | -4.325 | +0.455 | -0.053 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 3 | -0.266 | +0.000 | -0.201 | -4.320 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 7 | -0.440 | -0.635 | -0.416 | -0.542 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 9 | -0.625 | -1.166 | -0.433 | -0.441 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 1 | -1.059 | +0.000 | -0.116 | +2.244 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 1 | -1.208 | +0.000 | -0.625 | -1.166 | too few trades to compare |
| TRD-H4-PULLBACK | 1h | 1109 | +0.028 | -0.021 | -0.009 | -0.061 | yes |
| TRD-H4-PULLBACK | 30m | 679 | -0.040 | +0.099 | -0.066 | -0.127 | yes |
| TRD-H4-PULLBACK | 5m | 3217 | -0.054 | +0.021 | -0.111 | -0.081 | yes |
| S8-PDH-PDL-SWEEP | 1h | 311 | -0.085 | -0.304 | -0.149 | -0.223 | no |
| TRD-H4-BREAKOUT | 15m | 870 | -0.093 | -0.088 | -0.091 | -0.058 | no |
| TRD-H4-BREAKOUT | 5m | 1961 | -0.106 | -0.022 | -0.133 | -0.082 | yes |
| S8-PDH-PDL-SWEEP | 30m | 133 | -0.430 | -0.588 | -0.416 | -0.525 | no |
| PB-B-SWEEP | 5m | 1341 | -0.621 | -0.587 | +0.000 | +0.000 | too few trades to compare |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): TRD-H4-PULLBACK@1.0 1h BACKTESTING → FAILED; bb_squeeze_breakout@1.0 1h BACKTESTING → FAILED
- **Not tested (IDEA / RETIRED):** donchian_breakout-VEXIT-VRVOL v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S5 v1.0 (RETIRED)

### 3c. Research layers (daily run)
Last run: **2026-10-09 01:00 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 10 | 2017-08-17 | 2026-10-08 | 20023 |  |
| 1h | 10 | 2017-08-17 | 2026-10-09 | 80029 |  |
| 30m | 10 | 2024-10-09 | 2026-10-09 | 35040 |  |
| 15m | 10 | 2024-10-09 | 2026-10-09 | 70080 |  |
| 5m | 10 | 2024-10-09 | 2026-10-09 | 210240 |  |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 1147 (693) | no_displacement, false_breakout, trend_reversal | false_breakout 64%, no_displacement 33% | +0.47R | -0.37R | +0.23 / +0.18 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 1301 (794) | no_displacement, false_breakout | false_breakout 63%, no_displacement 34% | +0.48R | -0.35R | +0.23 / +0.18 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 967 (591) | no_displacement, false_breakout | false_breakout 63%, no_displacement 36% | +0.47R | -0.35R | +0.21 / +0.17 |
| donchian_breakout | 4h | BACKTESTING | 1176 (545) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 66%, stop_too_tight 34% | +0.34R | -0.37R | +0.15 / +0.11 |
| TRD-H4-BREAKOUT | 30m | BACKTESTING | 490 (298) | false_breakout | false_breakout 76%, range_market 26% | +0.54R | -0.47R | +0.17 / +0.10 |
| TRD-H4-BREAKOUT | 1h | BACKTESTING | 1119 (700) | false_breakout | false_breakout 64% | +0.57R | -0.44R | +0.13 / +0.08 |
| TRD-H4-BREAKOUT-noT4 | 1h | BACKTESTING | 3660 (2301) | no_displacement, false_breakout | false_breakout 66% | +0.52R | -0.44R | +0.09 / +0.03 |
| TRD-H4-PULLBACK | 15m | BACKTESTING | 1277 (778) | none | - | +0.48R | -0.37R | +0.13 / +0.03 |
| PB-A-APLUS | 5m | BACKTESTING | 79 (45) | stop_too_tight | range_market 47%, stop_too_tight 44% | +0.45R | -0.33R | -0.02 / -0.19 |
| PB-A-GRADED | 5m | BACKTESTING | 98 (55) | stop_too_tight | range_market 51%, stop_too_tight 38% | +0.46R | -0.31R | -0.02 / -0.20 |
| PB-A-PULLBACK-LDN | 5m | BACKTESTING | 30 (18) | none | range_market 56%, wrong_session 33%, stop_too_tight 33%, bad_target 28% | +0.57R | -0.45R | -0.16 / -0.41 |
| S5-SWEEP-MSS-FVG-noSMC | 15m | FAILED | 36 (16) | structural_change | range_market 31% | +0.40R | -0.47R | +0.63 / +0.46 |
| TRD-H4-PULLBACK | 1h | FAILED | 1109 (690) | low_relative_volume, indicator_lag, structural_change | low_relative_volume 56%, indicator_lag 26% | +0.45R | -0.40R | +0.08 / +0.03 |
| bb_squeeze_breakout | 4h | FAILED | 289 (142) | false_breakout, stop_too_tight, structural_change | false_breakout 59%, stop_too_tight 42%, regime_mismatch 29% | +0.36R | -0.35R | +0.09 / +0.01 |
| TRD-H4-BREAKOUT-noT4 | 30m | FAILED | 1624 (1028) | range_market, false_breakout | false_breakout 73%, range_market 29% | +0.49R | -0.47R | +0.08 / -0.01 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1192 (783) | false_breakout | false_breakout 72% | +0.45R | -0.39R | +0.11 / -0.01 |
| bb_squeeze_breakout | 1h | FAILED | 877 (421) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 62%, no_displacement 52%, stop_too_tight 37%, regime_mismatch 34% | +0.35R | -0.46R | +0.13 / -0.01 |
| TRD-H4-PULLBACK-noT4 | 1h | FAILED | 5197 (3245) | structural_change | - | +0.50R | -0.42R | +0.06 / -0.01 |
| macd_trend_cross | 1h | FAILED | 202 (98) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 93%, wrong_session 71%, indicator_lag 41%, stop_too_tight 31% | +0.30R | -0.43R | +0.11 / -0.02 |
| donchian_breakout-VEXIT | 30m | FAILED | 1271 (838) | false_breakout | false_breakout 70% | +0.45R | -0.40R | +0.11 / -0.02 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 3538 (2369) | no_displacement, wrong_session, false_breakout, regime_mismatch | false_breakout 64% | +0.51R | -0.40R | +0.07 / -0.02 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2686 (1801) | no_displacement, false_breakout, regime_mismatch | false_breakout 62% | +0.52R | -0.40R | +0.06 / -0.02 |
| donchian_breakout-VEXIT | 1h | FAILED | 3127 (2105) | no_displacement, false_breakout | false_breakout 63% | +0.52R | -0.40R | +0.07 / -0.02 |
| donchian_breakout | 1h | FAILED | 3214 (1637) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 31%, regime_mismatch 25% | +0.37R | -0.40R | +0.06 / -0.02 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1492 (983) | false_breakout | false_breakout 72% | +0.46R | -0.41R | +0.11 / -0.03 |
| macd_trend_cross | 4h | FAILED | 43 (21) | structural_change | no_displacement 90%, regime_mismatch 90%, low_relative_volume 57%, indicator_lag 57% | +0.20R | -0.46R | +0.04 / -0.04 |
| TRD-H4-PULLBACK | 30m | FAILED | 679 (442) | none | - | +0.46R | -0.44R | +0.04 / -0.04 |
| donchian_breakout | 30m | FAILED | 1310 (679) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 76%, no_displacement 38%, stop_too_tight 33% | +0.28R | -0.41R | +0.08 / -0.04 |
| supertrend_flip | 4h | FAILED | 99 (53) | regime_mismatch, indicator_lag, structural_change | regime_mismatch 70%, indicator_lag 38% | +0.37R | -0.42R | +0.01 / -0.05 |
| TRD-H4-PULLBACK | 5m | FAILED | 3217 (2011) | none | - | +0.51R | -0.42R | +0.08 / -0.05 |
| trend_pullback | 4h | FAILED | 1312 (679) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 81%, indicator_lag 39%, stop_too_tight 25% | +0.35R | -0.42R | +0.01 / -0.06 |
| S6-OB-FVG-noSMC | 15m | FAILED | 78 (46) | none | stop_too_wide 89%, regime_mismatch 33% | +0.38R | -0.49R | +0.08 / -0.07 |
| TRD-H4-PULLBACK-noT4 | 30m | FAILED | 2625 (1707) | htf_conflict | - | +0.50R | -0.42R | +0.02 / -0.07 |
| TRD-H4-PULLBACK-noT4 | 15m | FAILED | 4646 (2958) | none | - | +0.49R | -0.40R | +0.04 / -0.07 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 311 (208) | stop_too_tight, sweep_continued, structural_change | sweep_continued 97%, range_market 56%, stop_too_tight 34% | +0.54R | -0.40R | +0.12 / -0.09 |
| TRD-H4-BREAKOUT-noT4 | 15m | FAILED | 2826 (1876) | range_market, false_breakout | false_breakout 76%, range_market 39% | +0.45R | -0.44R | +0.02 / -0.09 |
| TRD-H4-BREAKOUT | 15m | FAILED | 870 (582) | false_breakout | false_breakout 78%, range_market 38% | +0.45R | -0.49R | +0.00 / -0.09 |
| rsi2_dip_buy | 4h | FAILED | 1967 (847) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 44% | +0.16R | -0.21R | -0.04 / -0.10 |
| rsi2_dip_buy | 1h | FAILED | 7343 (3224) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 42% | +0.15R | -0.21R | +0.00 / -0.10 |
| TRD-H4-BREAKOUT | 5m | FAILED | 1961 (1267) | false_breakout | false_breakout 76% | +0.44R | -0.44R | +0.03 / -0.11 |
| trend_pullback | 1h | FAILED | 6705 (3536) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 76%, indicator_lag 44%, stop_too_tight 28% | +0.29R | -0.43R | +0.02 / -0.11 |
| TRD-H4-PULLBACK-noT4 | 5m | FAILED | 9790 (6232) | none | - | +0.50R | -0.43R | +0.04 / -0.11 |
| ema_9_21_cross | 1h | FAILED | 357 (200) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 49%, stop_too_tight 26% | +0.26R | -0.38R | -0.00 / -0.12 |
| R4-CLUC | 30m | FAILED | 216 (130) | none | wrong_session 69% | +0.29R | -0.45R | -0.02 / -0.13 |
| TRD-H4-BREAKOUT-noT4 | 5m | FAILED | 5755 (3769) | false_breakout | false_breakout 74% | +0.48R | -0.44R | +0.02 / -0.13 |
| macd_trend_cross | 30m | FAILED | 300 (155) | overextended_entry, stop_too_tight, indicator_lag | indicator_lag 41%, stop_too_tight 32% | +0.34R | -0.46R | +0.06 / -0.14 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 860 (591) | trend_reversal, stop_too_tight | range_market 46%, stop_too_tight 37% | +0.63R | -0.50R | +0.07 / -0.15 |
| supertrend_flip | 1h | FAILED | 286 (153) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 73%, regime_mismatch 70%, stop_too_tight 38%, indicator_lag 31% | +0.39R | -0.40R | -0.06 / -0.15 |
| trend_pullback | 30m | FAILED | 3522 (1863) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 31% | +0.28R | -0.42R | +0.03 / -0.15 |
| rsi2_dip_buy | 30m | FAILED | 2847 (1425) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 30% | +0.16R | -0.19R | +0.01 / -0.16 |
| bb_squeeze_breakout | 30m | FAILED | 527 (277) | false_breakout, stop_too_tight | false_breakout 61%, stop_too_tight 41% | +0.24R | -0.46R | +0.05 / -0.16 |
| PB-B-GRADED | 5m | FAILED | 1415 (898) | none | - | +0.23R | -0.26R | +0.01 / -0.17 |
| PB-B-SWEEP-LIMIT | 5m | FAILED | 359 (219) | none | - | +0.23R | -0.29R | +0.01 / -0.17 |
| supertrend_flip | 30m | FAILED | 162 (87) | stop_too_tight, indicator_lag | regime_mismatch 46%, indicator_lag 44%, stop_too_tight 38%, late_entry 32% | +0.28R | -0.47R | -0.04 / -0.17 |
| PB-B-APLUS | 15m | FAILED | 118 (67) | stop_too_tight | regime_mismatch 51%, stop_too_tight 40% | +0.40R | -0.36R | -0.01 / -0.19 |
| liquidity_sweep_reversal | 1h | FAILED | 312 (166) | stop_too_tight | stop_too_tight 51% | +0.28R | -0.48R | -0.03 / -0.19 |
| PB-B-APLUS | 5m | FAILED | 300 (191) | none | - | +0.22R | -0.33R | -0.01 / -0.19 |
| R4-CLUC | 15m | FAILED | 178 (119) | none | wrong_session 72% | +0.35R | -0.31R | -0.07 / -0.19 |
| ema_9_21_cross | 30m | FAILED | 363 (216) | stop_too_tight, indicator_lag | indicator_lag 47%, low_relative_volume 38%, stop_too_tight 28% | +0.26R | -0.35R | -0.02 / -0.20 |
| trend_pullback | 15m | FAILED | 5984 (3236) | wrong_session, stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 31% | +0.27R | -0.43R | +0.05 / -0.21 |
| ema_9_21_cross | 15m | FAILED | 897 (511) | stop_too_tight, indicator_lag | indicator_lag 53%, low_relative_volume 41%, stop_too_tight 27% | +0.23R | -0.42R | +0.04 / -0.21 |
| PB-B-GRADED | 15m | FAILED | 564 (352) | stop_too_tight | stop_too_tight 35% | +0.35R | -0.35R | -0.05 / -0.22 |
| rsi2_dip_buy | 15m | FAILED | 4492 (2581) | wrong_session, trend_reversal, regime_mismatch, volatility_spike, fees_slippage | fees_slippage 37% | +0.15R | -0.19R | +0.01 / -0.24 |
| R4-BBRSI | 30m | FAILED | 1532 (1044) | none | - | +0.42R | -0.44R | -0.06 / -0.28 |
| bb_squeeze_breakout | 15m | FAILED | 1203 (663) | false_breakout, stop_too_tight | false_breakout 61%, stop_too_tight 40% | +0.27R | -0.47R | +0.01 / -0.29 |
| R4-BBRSI | 1h | FAILED | 1318 (944) | none | - | +0.45R | -0.45R | -0.16 / -0.31 |
| liquidity_sweep_reversal | 30m | FAILED | 360 (205) | stop_too_tight | stop_too_tight 40% | +0.37R | -0.50R | -0.07 / -0.33 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 595 (434) | stop_too_tight | stop_too_tight 33% | +0.59R | -0.49R | -0.07 / -0.42 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 133 (103) | low_relative_volume, trend_reversal, stop_too_tight, sweep_continued | sweep_continued 97%, stop_too_tight 26% | +0.56R | -0.51R | -0.15 / -0.43 |
| PB-B-SWEEP-15M | 15m | FAILED | 303 (184) | low_relative_volume, stop_too_tight | wrong_session 43%, stop_too_tight 30%, low_relative_volume 27% | +0.24R | -0.45R | +0.04 / -0.45 |
| ema_9_21_cross | 5m | FAILED | 2349 (1478) | low_relative_volume, stop_too_tight, indicator_lag | indicator_lag 53%, stop_too_tight 31% | +0.21R | -0.46R | +0.01 / -0.46 |
| liquidity_sweep_reversal | 15m | FAILED | 1260 (759) | stop_too_tight | stop_too_tight 39% | +0.29R | -0.49R | -0.06 / -0.46 |
| PB-B-SWEEP | 5m | FAILED | 1341 (881) | range_market, stop_too_tight | stop_too_tight 34%, range_market 28% | +0.15R | -0.41R | +0.06 / -0.62 |
| liquidity_sweep_reversal | 5m | FAILED | 4484 (2946) | range_market, stop_too_tight | stop_too_tight 39% | +0.27R | -0.50R | +0.10 / -0.65 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 33 strategy/timeframe tests); `false_breakout` (systematic in 24 strategy/timeframe tests); `regime_mismatch` (systematic in 15 strategy/timeframe tests); `indicator_lag` (systematic in 14 strategy/timeframe tests); `no_displacement` (systematic in 10 strategy/timeframe tests); `trend_reversal` (systematic in 8 strategy/timeframe tests); `volatility_spike` (systematic in 4 strategy/timeframe tests); `low_relative_volume` (systematic in 4 strategy/timeframe tests); `range_market` (systematic in 4 strategy/timeframe tests); `wrong_session` (systematic in 3 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- BTC down -2.9% (2026-10-08 09:00 → 2026-10-08 18:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ETH down -5.9% (2026-10-08 09:00 → 2026-10-08 17:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- SOL down -7.7% (2026-10-08 09:00 → 2026-10-08 18:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ZEC down -14.0% (2026-10-08 03:00 → 2026-10-08 16:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- XRP down -6.3% (2026-10-08 09:00 → 2026-10-08 18:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- BNB down -6.1% (2026-10-08 09:00 → 2026-10-08 18:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- SUI down -11.6% (2026-10-08 09:00 → 2026-10-08 18:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- UNI down -10.1% (2026-10-08 09:00 → 2026-10-08 18:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ADA down -11.4% (2026-10-08 09:00 → 2026-10-08 18:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- AVAX down -9.0% (2026-10-08 03:00 → 2026-10-08 16:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 128.0 KB | - | - |
| `memory/cleanup_log.md` | 0.5 KB | - | - |
| `memory/coin_notes.md` | 14.3 KB | 14 | 2026-10-04 02:31 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 13.9 KB | 31 | 2026-10-09 14:23 UTC |
| `memory/experiments.md` | 66.6 KB | 27 | 2026-10-08 15:30 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 303.1 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 18.3 KB | - | - |
| `memory/missed_trades.md` | 55.5 KB | 71 | 2026-10-09 01:00 UTC |
| `memory/playbook.md` | 10.0 KB | - | - |
| `memory/research_sources.md` | 94.1 KB | 72 | 2026-10-08 15:30 UTC |
| `memory/smc_events.csv` | 1242.6 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 26.5 KB | - | - |
| `memory/strategy_registry.csv` | 63.7 KB | - | - |
| `memory/trials.csv` | 15.2 KB | - | - |
| `memory/universe_log.md` | 25.6 KB | - | - |

**Reviews due** (review date passed; for the reviews): `missed_trades.md` LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00 (2026-10-02); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03); `missed_trades.md` SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells (2026-10-03); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03) … and 14 more
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG and SHORT = OKX futures fees + funding (always charged, never received). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*