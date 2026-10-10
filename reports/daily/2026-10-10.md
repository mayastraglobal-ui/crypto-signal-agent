# Crypto Signal Report

**Updated:** 2026-10-10 13:18 Beijing time (2026-10-10 05:18 UTC) · data: Binance · 6 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 14.1 MB (GitHub) · large files of this run 5.1 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-10 05:18 UTC / 2026-10-10 13:18 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US CPI (Sep data) 2026-10-14 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.01% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| RLC | **DEGRADED** | 1d: DEGRADED: volume 50x normal on candle 10-08 00:00 UTC (possible bad data); 1d: DEGRADED: volume 73x normal on candle 10-09 00:00 UTC (possible bad data) |
- 44 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-10 05:18 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 1071 h since 2026-08-26 | +0.0017% | 1.51 | 1.03 | - |
| ETH | GOOD | okx | 1071 h since 2026-08-26 | +0.0032% | 1.94 | 1.32 | - |
| SOL | GOOD | okx | 1071 h since 2026-08-26 | +0.0084% | 2.41 | 0.61 | - |
| ZEC | GOOD | okx | 1071 h since 2026-08-26 | +0.0100% | 0.77 | 1.07 | - |
| XRP | GOOD | okx | 1071 h since 2026-08-26 | -0.0006% | 3.07 | 1.26 | - |
| BNB | GOOD | okx | 1071 h since 2026-08-26 | +0.0080% | 2.90 | 1.94 | - |

*Binance futures API: blocked from GitHub's servers (HTTP 451) - expected, not a problem. The main series (OKX) is complete; Binance research history comes from the data.binance.vision files.*

## 0b. Coins this run
- **Signal coins (6/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **ZEC**, **XRP**, **BNB**
- 1 empty slot(s): waiting for a coin to hold a top-7 rank for 2 runs in a row
- **Research only** - backtested, never a signal: none

| Not eligible | 24h volume | Why |
|---|---|---|
| MAGIC | $53M | 7-day average volume $7M < $50M; 24h move +129.3% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $46k within 1% (need $250k) |
| RLC | $51M | 7-day average volume $25M < $50M; suspended for the rest of the UTC day (moved more than ±25% earlier today); order book too thin: $22k within 1% (need $250k) |

**Flags (not excluded):** RLC: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* NEAR, USD1, USDC (see `config.yaml`)

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

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | down (LH/LL) | 82,767.7 / 82,285.7 | 0.70 | 0.38x | 0.72x | - |
| ETH | mixed (HH/LL) | 2,520.54 / 2,474.34 | 0.82 | 0.36x | 0.71x | - |
| SOL | mixed (HH/LL) | 112.06 / 108.45 | 0.63 | 0.51x | 0.95x | - |
| ZEC | mixed (LH/HL) | 1,225.31 / 1,202.41 | 0.66 | 0.84x | 0.78x | - |
| XRP | up (HH/HL) | 1.41 / 1.3741 | 0.78 | 0.74x | 0.85x | retest_up, failed_breakout_up |
| BNB | up (HH/HL) | 746.01 / 737.24 | 0.89 | 0.76x | 0.88x | bear_engulf, breakout_up |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 297 | 48% | 33% | 25% | 81% | 46% | 32% | can't tell from chance | 0.09R |
| 4h | displacement_down | 226 | 45% | 26% | 16% | 80% | 44% | 29% | can't tell from chance | 0.10R |
| 4h | bull_engulf | 736 | 46% | 31% | 21% | 77% | 46% | 32% | can't tell from chance | 0.10R |
| 4h | bear_engulf | 805 | 41% | 26% | 16% | 81% | 44% | 29% | can't tell from chance | 0.10R |
| 4h | bull_reject | 535 | 44% | 31% | 23% | 76% | 47% | 31% | can't tell from chance | 0.09R |
| 4h | bear_reject | 534 | 46% | 32% | 22% | 75% | 45% | 29% | can't tell from chance | 0.10R |
| 4h | smc_sweep_bull | 371 | 45% | 32% | 23% | 75% | 46% | 31% | can't tell from chance | 0.09R |
| 4h | smc_sweep_bear | 422 | 41% | 27% | 19% | 80% | 45% | 29% | can't tell from chance | 0.10R |
| 4h | smc_bos_up | 193 | 46% | 28% | 19% | 82% | 48% | 34% | can't tell from chance | 0.09R |
| 4h | smc_bos_down | 124 | 47% | 31% | 19% | 76% | 45% | 29% | can't tell from chance | 0.09R |
| 4h | smc_choch_up | 57 | 53% | 39% | 30% | 82% | 45% | 30% | can't tell from chance | 0.10R |
| 4h | smc_choch_down | 53 | 40% | 23% | 13% | 77% | 48% | 32% | can't tell from chance | 0.10R |
| 4h | smc_fvg_retrace_bull | 408 | 44% | 28% | 23% | 76% | 47% | 32% | can't tell from chance | 0.09R |
| 4h | smc_fvg_retrace_bear | 416 | 43% | 27% | 17% | 80% | 44% | 29% | can't tell from chance | 0.09R |
| 1h | displacement_up | 373 | 47% | 33% | 27% | 74% | 45% | 31% | can't tell from chance | 0.21R |
| 1h | displacement_down | 275 | 40% | 26% | 16% | 81% | 37% | 24% | can't tell from chance | 0.22R |
| 1h | bull_engulf | 1024 | 41% | 29% | 22% | 76% | 43% | 30% | can't tell from chance | 0.23R |
| 1h | bear_engulf | 1145 | 36% | 24% | 17% | 80% | 36% | 24% | can't tell from chance | 0.24R |
| 1h | bull_reject | 836 | 42% | 29% | 22% | 75% | 44% | 30% | can't tell from chance | 0.23R |
| 1h | bear_reject | 812 | 34% | 24% | 18% | 81% | 37% | 24% | can't tell from chance | 0.22R |
| 1h | smc_sweep_bull | 383 | 40% | 26% | 19% | 77% | 43% | 30% | can't tell from chance | 0.22R |
| 1h | smc_sweep_bear | 399 | 36% | 23% | 17% | 82% | 36% | 23% | can't tell from chance | 0.22R |
| 1h | smc_bos_up | 251 | 45% | 35% | 29% | 76% | 43% | 29% | can't tell from chance | 0.20R |
| 1h | smc_bos_down | 175 | 45% | 35% | 26% | 77% | 39% | 25% | can't tell from chance | 0.24R |
| 1h | smc_choch_up | 63 | 52% | 33% | 29% | 78% | 39% | 27% | beats chance | 0.26R |
| 1h | smc_choch_down | 64 | 44% | 30% | 19% | 75% | 34% | 21% | can't tell from chance | 0.21R |
| 1h | smc_fvg_retrace_bull | 541 | 45% | 32% | 24% | 74% | 44% | 30% | can't tell from chance | 0.23R |
| 1h | smc_fvg_retrace_bear | 501 | 37% | 25% | 21% | 78% | 37% | 24% | can't tell from chance | 0.25R |
| 30m | displacement_up | 300 | 37% | 28% | 22% | 79% | 42% | 28% | can't tell from chance | 0.29R |
| 30m | displacement_down | 269 | 44% | 29% | 20% | 80% | 35% | 22% | beats chance | 0.28R |
| 30m | bull_engulf | 997 | 40% | 26% | 17% | 79% | 41% | 27% | can't tell from chance | 0.30R |
| 30m | bear_engulf | 1082 | 37% | 23% | 17% | 80% | 35% | 22% | can't tell from chance | 0.30R |
| 30m | bull_reject | 791 | 42% | 27% | 19% | 78% | 40% | 26% | can't tell from chance | 0.31R |
| 30m | bear_reject | 886 | 36% | 23% | 17% | 80% | 35% | 22% | can't tell from chance | 0.30R |
| 30m | smc_sweep_bull | 413 | 38% | 26% | 17% | 79% | 41% | 27% | can't tell from chance | 0.28R |
| 30m | smc_sweep_bear | 377 | 38% | 26% | 17% | 82% | 35% | 22% | can't tell from chance | 0.29R |
| 30m | smc_bos_up | 230 | 36% | 28% | 24% | 80% | 42% | 27% | can't tell from chance | 0.29R |
| 30m | smc_bos_down | 176 | 36% | 23% | 14% | 85% | 36% | 23% | can't tell from chance | 0.28R |
| 30m | smc_choch_up | 61 | 36% | 23% | 16% | 87% | 40% | 26% | can't tell from chance | 0.32R |
| 30m | smc_choch_down | 63 | 38% | 25% | 22% | 78% | 35% | 23% | can't tell from chance | 0.28R |
| 30m | smc_fvg_retrace_bull | 583 | 38% | 25% | 17% | 81% | 41% | 27% | can't tell from chance | 0.31R |
| 30m | smc_fvg_retrace_bear | 520 | 38% | 23% | 17% | 80% | 36% | 23% | can't tell from chance | 0.30R |
| 15m | displacement_up | 271 | 28% | 18% | 13% | 89% | 35% | 24% | worse than chance | 0.40R |
| 15m | displacement_down | 274 | 35% | 27% | 19% | 80% | 34% | 22% | can't tell from chance | 0.38R |
| 15m | bull_engulf | 1009 | 35% | 24% | 16% | 79% | 34% | 24% | can't tell from chance | 0.43R |
| 15m | bear_engulf | 1021 | 30% | 22% | 14% | 79% | 32% | 21% | can't tell from chance | 0.44R |
| 15m | bull_reject | 847 | 37% | 26% | 18% | 79% | 35% | 24% | can't tell from chance | 0.45R |
| 15m | bear_reject | 880 | 30% | 19% | 13% | 83% | 33% | 22% | worse than chance | 0.41R |
| 15m | smc_sweep_bull | 374 | 35% | 26% | 17% | 78% | 34% | 23% | can't tell from chance | 0.40R |
| 15m | smc_sweep_bear | 316 | 35% | 24% | 14% | 83% | 35% | 22% | can't tell from chance | 0.40R |
| 15m | smc_bos_up | 173 | 25% | 18% | 13% | 88% | 32% | 22% | can't tell from chance | 0.46R |
| 15m | smc_bos_down | 212 | 29% | 21% | 16% | 83% | 32% | 21% | can't tell from chance | 0.43R |
| 15m | smc_choch_up | 64 | 20% | 11% | 3% | 95% | 35% | 25% | worse than chance | 0.49R |
| 15m | smc_choch_down | 64 | 34% | 27% | 14% | 80% | 35% | 24% | can't tell from chance | 0.44R |
| 15m | smc_fvg_retrace_bull | 662 | 34% | 24% | 18% | 79% | 34% | 24% | can't tell from chance | 0.44R |
| 15m | smc_fvg_retrace_bear | 577 | 32% | 23% | 15% | 81% | 32% | 21% | can't tell from chance | 0.43R |
| 5m | displacement_up | 665 | 24% | 15% | 12% | 89% | 25% | 17% | can't tell from chance | 0.87R |
| 5m | displacement_down | 729 | 25% | 19% | 15% | 84% | 25% | 17% | can't tell from chance | 0.75R |
| 5m | bull_engulf | 2607 | 24% | 15% | 11% | 85% | 25% | 17% | can't tell from chance | 0.84R |
| 5m | bear_engulf | 2607 | 24% | 17% | 13% | 84% | 24% | 17% | can't tell from chance | 0.85R |
| 5m | bull_reject | 2134 | 23% | 16% | 11% | 84% | 25% | 16% | can't tell from chance | 0.86R |
| 5m | bear_reject | 2289 | 26% | 18% | 12% | 84% | 25% | 17% | can't tell from chance | 0.85R |
| 5m | smc_sweep_bull | 709 | 27% | 17% | 12% | 82% | 26% | 17% | can't tell from chance | 0.71R |
| 5m | smc_sweep_bear | 697 | 27% | 21% | 13% | 84% | 26% | 18% | can't tell from chance | 0.74R |
| 5m | smc_bos_up | 468 | 22% | 16% | 13% | 88% | 25% | 17% | can't tell from chance | 0.93R |
| 5m | smc_bos_down | 557 | 21% | 15% | 11% | 88% | 25% | 17% | worse than chance | 0.79R |
| 5m | smc_choch_up | 131 | 23% | 15% | 13% | 87% | 25% | 17% | can't tell from chance | 0.94R |
| 5m | smc_choch_down | 130 | 27% | 18% | 12% | 86% | 26% | 18% | can't tell from chance | 0.79R |
| 5m | smc_fvg_retrace_bull | 2190 | 24% | 17% | 11% | 85% | 24% | 16% | can't tell from chance | 0.92R |
| 5m | smc_fvg_retrace_bear | 1975 | 23% | 16% | 11% | 85% | 24% | 17% | can't tell from chance | 0.90R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (strong) | TRANSITION (weak) | TRANSITION (weak) | COMPRESSION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H COMPRESSION)) |
| **ETH** | WEAK_BULL (weak) | TRANSITION (weak) | WEAK_BEAR (weak) | COMPRESSION (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BEAR, 1H COMPRESSION)) |
| **SOL** | WEAK_BULL (moderate) | TRANSITION (weak) | WEAK_BEAR (weak) | WEAK_BEAR (weak) | SHORT allowed (4H/1H bearish, 1W WEAK_BULL) |
| **ZEC** | WEAK_BULL (weak) | TRANSITION (weak) | WEAK_BEAR (weak) | COMPRESSION (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BEAR, 1H COMPRESSION)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | TRANSITION (weak) | RANGE (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H RANGE)) |
| **BNB** | WEAK_BULL (weak) | WEAK_BULL (moderate) | WEAK_BEAR (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H WEAK_BEAR, 1H UNCLEAR)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.8 ATR in 10 candles); swing structure down (LH/LL); ADX 28 = strong trend; candle size 0.71x normal, Bollinger width above 62% of the last 100 candles · against: -
- **1D TRANSITION (weak)** - for: close above EMA-fast above EMA-slow; ADX 38 = strong trend; candle size 1.02x normal, Bollinger width above 32% of the last 100 candles · against: EMA-fast flat (+1.0 ATR in 10 candles); swing structure mixed
- **4H TRANSITION (weak)** - for: swing structure down (LH/LL); ADX 32 = strong trend; candle size 0.93x normal, Bollinger width above 76% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.9 ATR in 10 candles)
- **1H COMPRESSION (weak)** - for: EMA-fast flat (-0.3 ATR in 10 candles); ADX 13 = weak trend / ranging; candle size 0.72x normal, Bollinger width above 1% of the last 100 candles · against: close below EMA-fast below EMA-slow; swing structure down (LH/LL)

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | up (BOS 13 candles ago) | buy-side (bearish idea) 15 candles ago | bull 82,600.00-82,659.02 (retraced) | bear 85,550.00-86,378.24 | premium (83%) | swing high 82,767.71 (0.28 ATR) | swing low 82,285.71 (1.41 ATR) |
| **ETH** | down (BOS 37 candles ago) | buy-side (bearish idea) 0 candles ago | bull 2,419.83-2,436.13 | bear 2,690.78-2,700.54 | discount (45%) | swing high 2,520.54 (2.28 ATR) | swing low 2,474.34 (1.84 ATR) |
| **SOL** | up (BOS 0 candles ago) | buy-side (bearish idea) 0 candles ago | bear 110.72-110.98 (retraced) | bear 120.13-121.29 | discount (39%) | swing high 112.06 (2.75 ATR) | swing low 108.45 (1.76 ATR) |
| **ZEC** | down (BOS 37 candles ago) | sell-side (bullish idea) 21 candles ago | bear 1,228.60-1,233.12 (retraced) | bear 1,302.50-1,348.00 | premium (80%) | swing high 1,225.31 (0.31 ATR) | swing low 1,202.41 (1.22 ATR) |
| **XRP** | down (BOS 38 candles ago) | buy-side (bearish idea) 13 candles ago | bull 1.3975-1.3991 (retraced) | bull 1.2202-1.3441 | premium (93%) | swing high 1.4100 (0.26 ATR) | swing low 1.3741 (3.43 ATR) |
| **BNB** | down (BOS 37 candles ago) | buy-side (bearish idea) 4 candles ago | bull 746.24-746.94 | bear 768.61-773.99 | above the range (115%) | swing high 771.88 (7.51 ATR) | equal lows 736.65 (3.27 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **SIDEWAYS**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 64 (Greed), yesterday 59  (extreme fear/greed = bigger, faster moves)

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
**Status and long-history numbers** come from the daily research run (last run 2026-10-10 00:59 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 3 | 33.3 | +0.270 | 1.29 | 1.5R | +1.05 / -1.30 | +1.13 / -1.45 | 0/5 ✗ | +0.06 | -0.13 | ✗  sweep_bars 8→6: -1.38R | 0 | 0.47R | 0, +0.00 (+0.00 / +0.00) | 7 / 4 of 13 | 0 | not cost-viable: fees + slippage 0.47R per trade (stop must be ≥ 4x the round-trip cost); only 3 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 765 | 41.4 | +0.260 | 1.5 | 17.2R | +0.27 / +0.24 | +0.31 / +0.20 | 5/5 | +0.23 | +0.21 | stable | 6 | 0.04R | 1, -1.07 (-1.07 / +0.00) | 58 / 31 of 158 | 0 | max drawdown 17.2R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 871 | 40.5 | +0.245 | 1.46 | 20.8R | +0.26 / +0.22 | +0.27 / +0.22 | 5/5 | +0.21 | +0.19 | stable | 6 | 0.04R | 2, -1.05 (-1.05 / +0.00) | 97 / 39 of 212 | 0 | max drawdown 20.8R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 4h | **BACKTESTING** | 579 | 40.9 | +0.239 | 1.45 | 17.1R | +0.25 / +0.22 | +0.27 / +0.21 | 4/5 | +0.21 | +0.19 | stable | 5 | 0.04R | 1, -1.03 (-1.03 / +0.00) | 60 / 20 of 135 | 0 | max drawdown 17.1R |
| P01-BREAKOUT-V3 🧪 lab | 1.0 | 4h | **BACKTESTING** | 333 | 40.5 | +0.209 | 1.39 | 12.9R | +0.21 / +0.21 | +0.34 / +0.01 | 4/5 | +0.18 | +0.16 | stable | 5 | 0.04R | 2, -1.05 (-1.05 / +0.00) | 23 / 30 of 70 | 0 | max drawdown 12.9R |
| P01-BREAKOUT-V1 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1058 | 39.6 | +0.186 | 1.34 | 24.3R | +0.21 / +0.13 | +0.26 / +0.09 | 5/5 | +0.15 | +0.13 | stable | 5 | 0.04R | 3, -1.05 (-1.05 / -1.06) | 142 / 96 of 294 | 0 | max drawdown 24.3R |
| P01-BREAKOUT-V4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 900 | 39.6 | +0.184 | 1.29 | 24.7R | +0.23 / +0.09 | +0.24 / +0.11 | 5/5 | +0.15 | +0.12 | stable | 5 | 0.04R | 3, -1.05 (-1.05 / -1.06) | 142 / 96 of 294 | 0 | max drawdown 24.7R |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 787 | 56.4 | +0.171 | 1.4 | 13.1R | +0.18 / +0.16 | +0.19 / +0.15 | 5/5 | +0.14 | +0.12 | stable | 6 | 0.04R | 2, -1.05 (-1.05 / +0.00) | 58 / 31 of 158 | 0 | max drawdown 13.1R |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 2 | 50.0 | +0.130 | 1.21 | 1.2R | +0.13 / +0.00 | -1.22 / +1.47 | 0/5 ✗ | +0.02 | +0.00 | stable | 0 | 0.27R | 0, +0.00 (+0.00 / +0.00) | 34 / 7 of 46 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 1h | **BACKTESTING** | 776 | 38.4 | +0.114 | 1.18 | 46.2R | +0.05 / +0.25 | +0.18 / +0.04 | 4/5 | +0.09 | +0.07 | stable | 5 | 0.04R | 1, -1.04 (-1.04 / +0.00) | 6 / 2 of 73 | 0 | profit factor 1.18; max drawdown 46.2R |
| TRD-H4-BREAKOUT | 1.0 | 30m | **BACKTESTING** | 403 | 40.0 | +0.112 | 1.17 | 22.8R | -0.03 / +0.26 | +0.13 / +0.09 | 2/5 ✗ | +0.13 | +0.06 | stable | 5 | 0.08R | 1, +2.46 (+2.46 / +0.00) | 9 / 8 of 64 | 0 | profit factor 1.17; max drawdown 22.8R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 297 | 35.0 | +0.096 | 1.14 | 19.3R | +0.13 / +0.03 | +0.09 / +0.10 | 2/5 ✗ | +0.06 | +0.01 | ✗  rsi_hi 65→52: -0.04R | 4 | 0.06R | 1, -1.08 (+0.00 / -1.08) | 502 / 144 of 650 | 0 | avg +0.10R/trade (needs +0.10R); profit factor 1.14; max drawdown 19.3R |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 1h | **BACKTESTING** | 2475 | 37.0 | +0.031 | 1.05 | 76.6R | +0.02 / +0.06 | +0.09 / -0.04 | 4/5 | +0.01 | -0.02 | ✗  stop atr 2.0→1.6: -0.01R | 4 | 0.05R | 16, -0.43 (-0.63 / +2.47) | 113 / 321 of 609 | 0 | avg +0.03R/trade (needs +0.10R); profit factor 1.05; max drawdown 76.6R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 30m | **BACKTESTING** | 796 | 36.7 | +0.031 | 1.05 | 33.6R | -0.01 / +0.08 | +0.07 / -0.02 | 3/5 | -0.04 | -0.11 | ✗  stop atr 2.0→1.6: -0.02R | 2 | 0.12R | 13, +0.03 (-0.01 / +0.12) | 72 / 28 of 168 | 0 | avg +0.03R/trade (needs +0.12R); profit factor 1.05; max drawdown 33.6R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **BACKTESTING** | 127 | 52.8 | +0.030 | 1.06 | 24.0R | -0.11 / +0.31 | +0.03 / +0.03 | 3/5 | -0.02 | -0.07 | ✗  stop atr 1.5→1.2: -0.05R | 3 | 0.11R | 0, +0.00 (+0.00 / +0.00) | 143 / 3 of 148 | 0 | avg +0.03R/trade (needs +0.10R); profit factor 1.06; max drawdown 24.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **BACKTESTING** | 597 | 53.1 | +0.021 | 1.04 | 22.7R | +0.01 / +0.04 | +0.00 / +0.05 | 3/5 | -0.05 | -0.12 | ✗  bb_k 2→1: -0.04R | 3 | 0.12R | 5, +0.16 (+0.16 / +0.00) | 90 / 18 of 136 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.04; max drawdown 22.7R |
| TRD-H4-PULLBACK | 1.0 | 15m | **BACKTESTING** | 1456 | 38.9 | +0.005 | 1.01 | 72.0R | -0.06 / +0.14 | -0.05 / +0.07 | 2/5 ✗ | -0.03 | -0.01 | ✗  stop atr 2.0→1.6: -0.02R | 2 | 0.10R | 6, +0.09 (+0.09 / +0.00) | 29 / 22 of 177 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.01; max drawdown 72.0R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 15m | **BACKTESTING** | 684 | 36.5 | +0.005 | 1.01 | 34.3R | -0.05 / +0.06 | -0.03 / +0.06 | 2/5 ✗ | -0.02 | -0.07 | ✗  stop atr 2.0→1.6: -0.03R | 3 | 0.10R | 3, -1.11 (-1.11 / +0.00) | 5 / 6 of 39 | 0 | avg +0.00R/trade (needs +0.10R); profit factor 1.01; max drawdown 34.3R; not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V2 🧪 lab | 1.0 | 30m | **BACKTESTING** | 873 | 36.2 | +0.005 | 1.01 | 56.0R | -0.06 / +0.08 | +0.04 / -0.04 | 1/5 ✗ | -0.07 | -0.14 | ✗  stop atr 2.0→1.6: -0.02R | 3 | 0.13R | 10, +0.15 (+0.00 / +0.51) | 199 / 116 of 383 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.01; max drawdown 56.0R; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 2 of 9 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 2 of 9 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 4 of 13 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT-noCVD | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT-W20 | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-APLUS | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 9 | 44.4 | -0.034 | 0.93 | 2.3R | -0.24 / +0.07 | -0.02 / -0.05 | 0/5 ✗ | -0.29 | -0.38 | ✗  stop buffer_atr 0.2→0.24: -0.20R | 0 | 0.13R | 0, +0.00 (+0.00 / +0.00) | 295 / 111 of 475 | 0 | only 9 trades; avg -0.03R/trade (needs +0.10R); profit factor 0.93; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 22 | 45.5 | -0.045 | 0.92 | 8.2R | +0.55 / -0.54 | +0.54 / -0.45 | 0/5 ✗ | -0.12 | -0.21 | ✗  time_stop_bars 30→36: -0.08R | 2 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 306 / 104 of 470 | 0 | only 22 trades; avg -0.04R/trade (needs +0.10R); profit factor 0.92; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-LIMIT | 1.0 | 5m | **BACKTESTING** | 90 | 42.2 | -0.099 | 0.77 | 10.6R | -0.09 / -0.12 | -0.11 / -0.09 | 2/5 ✗ | -0.21 | -0.43 | ✗  stop max_width_atr 3.0→2.4: -0.11R | 3 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 29 | 0 | only 90 trades; avg -0.10R/trade (needs +0.15R); profit factor 0.77; max drawdown 10.6R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **BACKTESTING** | 27 | 48.1 | -0.103 | 0.81 | 4.8R | +0.03 / -0.42 | +0.18 / -0.37 | 1/5 ✗ | -0.13 | -0.16 | ✗  time_stop_bars 40→32: -0.13R | 2 | 0.06R | 1, +0.31 (+0.31 / +0.00) | 96 / 0 of 97 | 0 | only 27 trades; avg -0.10R/trade (needs +0.10R); profit factor 0.81; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 5m | **BACKTESTING** | 67 | 37.3 | -0.120 | 0.73 | 9.0R | -0.09 / -0.22 | -0.14 / -0.09 | 2/5 ✗ | -0.10 | -0.02 | ✗  stop max_width_atr 3.0→2.4: -0.13R | 2 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 23 | 0 | only 67 trades; avg -0.12R/trade (needs +0.15R); profit factor 0.73; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 14 | 42.9 | -0.164 | 0.79 | 5.6R | -0.02 / -0.27 | +0.79 / -0.55 | 1/5 ✗ | -1.38 | -1.12 | ✗  stop buffer_atr 0.2→0.24: -0.75R | 0 | 0.43R | 0, +0.00 (+0.00 / +0.00) | 26 / 7 of 38 | 0 | not cost-viable: fees + slippage 0.43R per trade (stop must be ≥ 4x the round-trip cost); only 14 trades; avg -0.16R/trade (needs +0.10R); profit factor 0.79; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-GRADED | 1.0 | 5m | **BACKTESTING** | 33 | 42.4 | -0.288 | 0.56 | 10.9R | -0.29 / +0.00 | -0.02 / -0.41 | 0/5 ✗ | -0.75 | -0.20 | ✗  time_stop_bars 48→38: -0.34R | 0 | 0.20R | 1, +1.53 (+0.00 / +1.53) | 0 / 0 of 1 | 0 | only 33 trades; avg -0.29R/trade (needs +0.15R); profit factor 0.56; max drawdown 10.9R; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 3 | 33.3 | -0.303 | 0.68 | 1.4R | +0.00 / -0.30 | -0.30 / +0.00 | 0/5 ✗ | -0.50 | -0.63 | ✗  stop buffer_atr 0.2→0.24: -0.65R | 0 | 0.53R | 1, +1.97 (+1.97 / +0.00) | 26 / 66 of 97 | 0 | not cost-viable: fees + slippage 0.53R per trade (stop must be ≥ 4x the round-trip cost); only 3 trades; avg -0.30R/trade (needs +0.10R); profit factor 0.68; only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-APLUS | 1.0 | 5m | **BACKTESTING** | 27 | 37.0 | -0.335 | 0.53 | 10.4R | -0.34 / +0.00 | -0.08 / -0.46 | 0/5 ✗ | -1.00 | -0.65 | ✗  time_stop_bars 48→38: -0.39R | 0 | 0.20R | 1, +1.53 (+0.00 / +1.53) | 0 / 0 of 1 | 0 | only 27 trades; avg -0.33R/trade (needs +0.15R); profit factor 0.53; max drawdown 10.4R; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 10 | 30.0 | -0.345 | 0.6 | 5.1R | -0.25 / -1.17 | -0.30 / -0.41 | 0/5 ✗ | -0.48 | -0.77 | ✗  mss_bars 10→12: -0.42R | 0 | 0.32R | 0, +0.00 (+0.00 / +0.00) | 34 / 7 of 46 | 0 | not cost-viable: fees + slippage 0.32R per trade (stop must be ≥ 4x the round-trip cost); only 10 trades; avg -0.34R/trade (needs +0.10R); profit factor 0.60; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 15m | **BACKTESTING** | 34 | 38.2 | -0.489 | 0.28 | 18.5R | -0.49 / -0.49 | -0.33 / -0.67 | 0/5 ✗ | -0.57 | -0.82 | ✗  stop buffer_atr 0.0→0.0: -0.49R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 12 | 0 | only 34 trades; avg -0.49R/trade (needs +0.15R); profit factor 0.28; max drawdown 18.5R; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 7 | 14.3 | -0.505 | 0.51 | 4.8R | -0.24 / -1.17 | -1.24 / -0.21 | 0/5 ✗ | -0.47 | -0.56 | ✗  sweep_bars 20→16: -0.51R | 0 | 0.28R | 0, +0.00 (+0.00 / +0.00) | 39 / 13 of 53 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); only 7 trades; avg -0.50R/trade (needs +0.10R); profit factor 0.51; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-LDN | 1.0 | 5m | **BACKTESTING** | 14 | 35.7 | -0.553 | 0.3 | 9.1R | -0.60 / -0.38 | -0.83 / -0.44 | 0/5 ✗ | -0.62 | -0.84 | ✗  stop buffer_atr 0.0→0.0: -0.55R | 1 | 0.24R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 14 trades; avg -0.55R/trade (needs +0.15R); profit factor 0.30; only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-GRADED | 1.0 | 5m | **BACKTESTING** | 3 | 33.3 | -0.613 | 0.2 | 1.8R | -0.61 / +0.00 | -1.15 / +0.46 | 0/5 ✗ | -1.17 | -1.23 | ✗  stop buffer_atr 0.0→0.0: -0.61R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 1 | 0 | only 3 trades; avg -0.61R/trade (needs +0.15R); profit factor 0.20; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-noCVD | 1.0 | 5m | **BACKTESTING** | 13 | 30.8 | -0.700 | 0.26 | 9.5R | +0.00 / -0.70 | -0.70 / -0.70 | 0/5 ✗ | -0.57 | -0.35 | ✗  stop buffer_atr 0.0→0.0: -0.70R | 0 | 0.56R | 6, -0.46 (-0.46 / +0.00) | 0 / 0 of 28 | 0 | not cost-viable: fees + slippage 0.56R per trade (stop must be ≥ 4x the round-trip cost); only 13 trades; avg -0.70R/trade (needs +0.15R); profit factor 0.26; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-CVD | 1.0 | 5m | **BACKTESTING** | 7 | 28.6 | -0.718 | 0.16 | 6.0R | -0.72 / +0.00 | -1.23 / -0.63 | 0/5 ✗ | -1.00 | -1.41 | ✗  stop buffer_atr 0.0→0.0: -0.72R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 7 trades; avg -0.72R/trade (needs +0.15R); profit factor 0.16; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK | 1.0 | 5m | **BACKTESTING** | 8 | 25.0 | -0.781 | 0.13 | 7.2R | -0.78 / +0.00 | -1.23 / -0.72 | 0/5 ✗ | -1.00 | -1.41 | ✗  stop buffer_atr 0.0→0.0: -0.78R | 0 | 0.19R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 8 trades; avg -0.78R/trade (needs +0.15R); profit factor 0.13; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.208 | 0.0 | 1.2R | -1.21 / +0.00 | -1.21 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.2→0.16: -1.21R | 0 | 0.27R | 0, +0.00 (+0.00 / +0.00) | 39 / 13 of 53 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.21R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V4-S6 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.08 (+0.00 / -1.08) | 522 / 149 of 678 | 0 | waiting for the first daily research run (Layers B/C) |
| P03-FIB-PULLBACK-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 330 / 150 of 487 | 0 | waiting for the first daily research run (Layers B/C) |
| P03-FIB-PULLBACK-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 7, -0.98 (-1.15 / -0.55) | 489 / 126 of 702 | 0 | waiting for the first daily research run (Layers B/C) |
| P03-FIB-PULLBACK-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 14, -0.74 (-0.59 / -1.29) | 480 / 184 of 764 | 0 | waiting for the first daily research run (Layers B/C) |
| P03-FIB-PULLBACK-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 25, -0.53 (-0.47 / -0.68) | 523 / 174 of 785 | 0 | waiting for the first daily research run (Layers B/C) |
| P03-FIB-PULLBACK-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 72 / 49 of 123 | 0 | waiting for the first daily research run (Layers B/C) |
| P03-FIB-PULLBACK-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 330 / 150 of 487 | 0 | waiting for the first daily research run (Layers B/C) |
| P04-MACD-SUPERTREND-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.09 (-1.09 / +0.00) | 139 / 27 of 178 | 0 | waiting for the first daily research run (Layers B/C) |
| P04-MACD-SUPERTREND-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, +2.44 (+0.00 / +2.44) | 167 / 40 of 235 | 0 | waiting for the first daily research run (Layers B/C) |
| P04-MACD-SUPERTREND-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 6, -0.05 (-0.05 / +0.00) | 160 / 62 of 257 | 0 | waiting for the first daily research run (Layers B/C) |
| P04-MACD-SUPERTREND-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 11, -0.01 (-0.15 / +0.66) | 172 / 62 of 260 | 0 | waiting for the first daily research run (Layers B/C) |
| P04-MACD-SUPERTREND-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.09 (-1.09 / +0.00) | 30 / 8 of 44 | 0 | waiting for the first daily research run (Layers B/C) |
| P04-MACD-SUPERTREND-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.09 (-1.09 / +0.00) | 139 / 27 of 178 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -0.11 (-0.11 / +0.00) | 257 / 0 of 284 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 14, +0.07 (+0.05 / +0.14) | 322 / 0 of 363 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 52, -0.29 (-0.35 / +0.03) | 292 / 1 of 381 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 115, -0.28 (-0.40 / +0.21) | 212 / 1 of 344 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -0.11 (-0.11 / +0.00) | 33 / 0 of 42 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.06 (-1.06 / +0.00) | 257 / 0 of 284 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 170 / 0 of 171 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 14, +0.17 (+0.17 / +0.00) | 317 / 1 of 349 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 66, -0.29 (-0.44 / +0.98) | 282 / 4 of 386 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.05 (-1.03 / -1.07) | 148 / 53 of 226 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 5, +0.49 (+0.01 / +2.43) | 170 / 49 of 248 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 9, -0.10 (-0.06 / -0.14) | 172 / 66 of 265 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 13, -0.39 (-0.53 / +0.08) | 200 / 70 of 293 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.03 (-1.03 / +0.00) | 18 / 19 of 47 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.05 (-1.03 / -1.07) | 148 / 53 of 226 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V1 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 3, +0.03 (-1.16 / +2.42) | 248 / 52 of 333 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 4, -0.31 (-1.23 / +0.62) | 154 / 50 of 223 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 7, -0.37 (-0.64 / +0.29) | 86 / 29 of 124 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V3 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.24 (-1.24 / +0.00) | 71 / 14 of 94 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V4 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 3, -0.03 (-1.16 / +2.22) | 248 / 52 of 333 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 37 / 12 of 49 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.07 (-1.07 / +0.00) | 30 / 17 of 48 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.10 (+0.00 / -1.10) | 43 / 19 of 64 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, +0.86 (+0.86 / +0.00) | 39 / 10 of 50 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 6 / 0 of 6 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 37 / 12 of 49 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 5 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 6 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.10 (-1.10 / +0.00) | 0 / 0 of 10 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 5 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 5 | 0 | waiting for the first daily research run (Layers B/C) |
| P03-FIB-PULLBACK-V5 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 27, -0.06 (-0.33 / +0.40) | 489 / 29 of 702 | 0 | waiting for the first daily research run (Layers B/C) |
| P03-FIB-PULLBACK-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 37, -0.22 (-0.45 / +0.26) | 480 / 50 of 764 | 0 | waiting for the first daily research run (Layers B/C) |
| P03-FIB-PULLBACK-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 69, -0.33 (-0.62 / +0.07) | 523 / 66 of 785 | 0 | waiting for the first daily research run (Layers B/C) |
| P04-MACD-SUPERTREND-V5 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 14, +0.20 (+0.11 / +0.27) | 167 / 3 of 235 | 0 | waiting for the first daily research run (Layers B/C) |
| P04-MACD-SUPERTREND-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 23, +0.47 (+0.28 / +0.68) | 160 / 17 of 257 | 0 | waiting for the first daily research run (Layers B/C) |
| P04-MACD-SUPERTREND-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 30, +0.34 (-0.20 / +0.87) | 172 / 28 of 260 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V5 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 10, +0.25 (-0.49 / +1.99) | 170 / 21 of 248 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 21, +0.14 (-0.10 / +0.28) | 172 / 35 of 265 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 32, -0.28 (-0.53 / +0.07) | 200 / 49 of 293 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 15, -0.18 (-0.80 / +0.13) | 154 / 26 of 223 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 19, +0.12 (-0.26 / +0.47) | 86 / 13 of 124 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V5 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.07 (-1.07 / +0.00) | 30 / 17 of 48 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.10 (+0.00 / -1.10) | 43 / 16 of 64 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -0.19 (-0.19 / +0.00) | 39 / 9 of 50 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 199 | 52.3 | +0.042 | 1.08 | 21.1R | +0.20 / -0.30 | +0.18 / -0.09 | 2/5 ✗ | -0.00 | -0.04 | ✗  stop atr 1.5→1.8: -0.00R | 4 | 0.07R | 1, -1.04 (-1.04 / +0.00) | 71 / 15 of 93 | 0 | avg +0.04R/trade (needs +0.10R); profit factor 1.08; max drawdown 21.1R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 1h | **FAILED** | 753 | 37.6 | +0.019 | 1.03 | 40.6R | +0.04 / -0.03 | -0.03 / +0.08 | 2/5 ✗ | -0.01 | -0.04 | ✗  stop atr 2.0→1.6: -0.01R | 3 | 0.04R | 0, +0.00 (+0.00 / +0.00) | 21 / 20 of 131 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.03; max drawdown 40.6R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 1h | **FAILED** | 3457 | 38.0 | -0.006 | 0.99 | 142.1R | +0.02 / -0.06 | -0.01 / +0.00 | 1/5 ✗ | -0.04 | -0.07 | ✗  stop atr 2.0→1.6: -0.03R | 3 | 0.05R | 19, +0.01 (+0.15 / -1.14) | 452 / 1644 of 2387 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; max drawdown 142.1R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 1h | **FAILED** | 1654 | 32.7 | -0.014 | 0.98 | 102.5R | -0.04 / +0.05 | +0.02 / -0.05 | 2/5 ✗ | -0.05 | -0.09 | ✗  stop atr 2.0→1.6: -0.03R | 2 | 0.07R | 6, +0.51 (+0.42 / +0.68) | 87 / 54 of 230 | 0 | avg -0.01R/trade (needs +0.12R); profit factor 0.98; max drawdown 102.5R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 5m | **FAILED** | 890 | 38.9 | -0.015 | 0.98 | 62.8R | -0.02 / -0.00 | +0.07 / -0.09 | 2/5 ✗ | -0.11 | -0.18 | ✗  stop atr 2.0→1.6: -0.03R | 3 | 0.15R | 7, +0.42 (+0.42 / +0.00) | 5 / 8 of 41 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.98; max drawdown 62.8R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 30m | **FAILED** | 1336 | 36.3 | -0.019 | 0.97 | 71.6R | -0.04 / +0.01 | -0.02 / -0.02 | 1/5 ✗ | -0.05 | -0.10 | ✗  stop atr 2.0→1.6: -0.03R | 1 | 0.09R | 20, -0.20 (-0.30 / +0.68) | 79 / 326 of 551 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 71.6R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 2400 | 32.7 | -0.020 | 0.97 | 134.1R | -0.04 / +0.02 | +0.02 / -0.07 | 2/5 ✗ | -0.07 | -0.11 | ✗  stop atr 2.0→1.6: -0.04R | 2 | 0.08R | 12, -0.17 (-0.34 / +0.68) | 139 / 80 of 355 | 0 | avg -0.02R/trade (needs +0.12R); profit factor 0.97; max drawdown 134.1R; not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V2 🧪 lab | 1.0 | 1h | **FAILED** | 1849 | 32.3 | -0.023 | 0.96 | 100.0R | -0.06 / +0.06 | +0.02 / -0.08 | 1/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.04R | 2 | 0.07R | 6, -0.11 (-0.50 / +0.68) | 203 / 105 of 409 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 100.0R; not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V5 🧪 lab | 1.0 | 1h | **FAILED** | 3762 | 33.0 | -0.023 | 0.96 | 226.0R | -0.04 / +0.02 | -0.01 / -0.03 | 1/5 ✗ | -0.07 | -0.12 | ✗  stop atr 2.0→1.6: -0.05R | 2 | 0.08R | 16, +0.20 (-0.38 / +0.55) | 203 / 41 of 409 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 226.0R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V1 🧪 lab | 1.0 | 4h | **FAILED** | 299 | 31.4 | -0.024 | 0.96 | 23.4R | +0.03 / -0.13 | -0.03 / -0.02 | 2/5 ✗ | -0.06 | -0.09 | ✗  rsi_hi 65→52: -0.39R | 2 | 0.06R | 1, -1.08 (+0.00 / -1.08) | 502 / 144 of 650 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 23.4R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2107 | 32.4 | -0.026 | 0.96 | 127.0R | -0.05 / +0.03 | +0.00 / -0.06 | 2/5 ✗ | -0.07 | -0.11 | ✗  stop atr 2.0→1.6: -0.05R | 3 | 0.08R | 8, -0.12 (-0.38 / +0.68) | 76 / 59 of 241 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.96; max drawdown 127.0R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 5m | **FAILED** | 1389 | 38.2 | -0.029 | 0.96 | 133.0R | -0.07 / +0.11 | -0.04 / -0.02 | 2/5 ✗ | -0.00 | -0.10 | ✗  stop atr 2.0→2.4: -0.05R | 1 | 0.15R | 14, -0.13 (-0.13 / +0.00) | 25 / 49 of 168 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.96; max drawdown 133.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 66 | 47.0 | -0.040 | 0.93 | 7.8R | +0.10 / -0.24 | -0.10 / +0.04 | 4/5 ✗ | -0.08 | -0.11 | ✗  time_stop_bars 60→48: -0.04R | 1 | 0.05R | 1, -1.14 (-1.14 / +0.00) | 23 / 4 of 30 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.93; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2162 | 48.0 | -0.042 | 0.92 | 116.2R | -0.05 / -0.03 | -0.03 / -0.06 | 1/5 ✗ | -0.08 | -0.12 | ✗  stop atr 2.0→1.6: -0.05R | 1 | 0.08R | 8, -0.01 (-0.14 / +0.38) | 76 / 59 of 241 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.92; max drawdown 116.2R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1247 | 34.6 | -0.045 | 0.93 | 88.7R | -0.08 / +0.00 | -0.04 / -0.06 | 1/5 ✗ | -0.13 | -0.21 | ✗  stop atr 2.0→1.6: -0.09R | 1 | 0.14R | 23, -0.04 (-0.08 / +0.12) | 126 / 54 of 288 | 0 | avg -0.04R/trade (needs +0.12R); profit factor 0.93; max drawdown 88.7R; not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V2 🧪 lab | 1.0 | 15m | **FAILED** | 1330 | 34.4 | -0.057 | 0.91 | 116.0R | -0.10 / -0.01 | -0.06 / -0.05 | 1/5 ✗ | -0.15 | -0.26 | ✗  stop atr 2.0→1.6: -0.10R | 2 | 0.18R | 17, -0.25 (-0.41 / +0.29) | 209 / 107 of 354 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 116.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1052 | 33.6 | -0.062 | 0.91 | 100.5R | -0.12 / +0.01 | -0.06 / -0.07 | 1/5 ✗ | -0.14 | -0.21 | ✗  stop atr 2.0→1.6: -0.10R | 1 | 0.14R | 17, -0.08 (-0.21 / +0.51) | 80 / 44 of 214 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 100.5R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 15m | **FAILED** | 2224 | 34.9 | -0.074 | 0.9 | 185.5R | -0.10 / -0.05 | -0.08 / -0.07 | 0/5 ✗ | -0.12 | -0.18 | ✗  stop atr 2.0→1.6: -0.11R | 1 | 0.12R | 35, -0.48 (-0.47 / -0.54) | 75 / 366 of 557 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.90; max drawdown 185.5R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 874 | 48.1 | -0.076 | 0.86 | 104.0R | -0.02 / -0.19 | -0.00 / -0.17 | 1/5 ✗ | -0.11 | -0.15 | ✗  long_rsi_hi 65→52: -0.17R | 1 | 0.06R | 8, -0.29 (-0.29 / +0.00) | 413 / 111 of 641 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.86; max drawdown 104.0R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 15m | **FAILED** | 5340 | 36.6 | -0.080 | 0.88 | 453.7R | -0.09 / -0.06 | -0.11 / -0.05 | 0/5 ✗ | -0.12 | -0.11 | ✗  stop atr 2.0→1.6: -0.09R | 0 | 0.12R | 50, -0.28 (-0.13 / -0.68) | 341 / 1686 of 2419 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.88; max drawdown 453.7R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 61 | 34.4 | -0.089 | 0.87 | 13.9R | -0.37 / +0.24 | -0.11 / -0.02 | 1/5 ✗ | -0.18 | -0.18 | ✗  time_stop_bars 30→24: -0.14R | 2 | 0.16R | 3, -0.96 (-1.24 / -0.39) | 79 / 25 of 117 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.87; max drawdown 13.9R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1095 | 47.5 | -0.090 | 0.84 | 120.4R | -0.12 / -0.06 | -0.10 / -0.08 | 0/5 ✗ | -0.17 | -0.25 | ✗  stop atr 2.0→1.6: -0.12R | 0 | 0.14R | 17, -0.10 (-0.23 / +0.54) | 80 / 44 of 214 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.84; max drawdown 120.4R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V2 🧪 lab | 1.0 | 1h | **FAILED** | 2302 | 31.1 | -0.090 | 0.86 | 236.6R | -0.09 / -0.10 | -0.11 / -0.07 | 0/5 ✗ | -0.15 | -0.21 | ✗  stop atr 1.5→1.2: -0.11R | 0 | 0.11R | 8, -0.82 (-0.68 / -1.22) | 710 / 96 of 884 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.86; max drawdown 236.6R; not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V5 🧪 lab | 1.0 | 30m | **FAILED** | 1938 | 32.9 | -0.095 | 0.86 | 207.3R | -0.11 / -0.07 | -0.11 / -0.08 | 1/5 ✗ | -0.19 | -0.26 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.15R | 28, +0.03 (-0.27 / +0.39) | 199 / 53 of 383 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.86; max drawdown 207.3R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 30m | **FAILED** | 817 | 34.4 | -0.097 | 0.86 | 107.6R | -0.17 / +0.04 | -0.15 / -0.04 | 1/5 ✗ | -0.12 | -0.15 | ✗  entry offset_atr 0.25→0.3: -0.12R | 0 | 0.07R | 1, +2.46 (+2.46 / +0.00) | 24 / 21 of 158 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.86; max drawdown 107.6R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 213 | 34.3 | -0.099 | 0.87 | 43.7R | -0.02 / -0.28 | -0.31 / +0.17 | 1/5 ✗ | -0.19 | -0.28 | ✗  time_stop_bars 30→36: -0.12R | 2 | 0.17R | 2, +1.78 (+1.78 / +0.00) | 56 / 127 of 191 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.87; max drawdown 43.7R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 5m | **FAILED** | 3649 | 37.4 | -0.102 | 0.85 | 415.6R | -0.12 / -0.04 | -0.10 / -0.10 | 0/5 ✗ | -0.10 | -0.14 | ✗  stop atr 2.0→2.4: -0.12R | 0 | 0.17R | 55, -0.39 (-0.41 / -0.28) | 857 / 4586 of 6281 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.85; max drawdown 415.6R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1318 | 56.8 | -0.104 | 0.64 | 137.7R | -0.10 / -0.12 | -0.12 / -0.09 | 0/5 ✗ | -0.13 | -0.16 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.05R | 8, -0.34 (+0.09 / -1.05) | 457 / 6 of 631 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.64; max drawdown 137.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 248 | 44.0 | -0.105 | 0.81 | 37.8R | -0.12 / -0.07 | -0.17 / -0.03 | 0/5 ✗ | -0.16 | -0.22 | ✗  slow 21→17: -0.16R | 2 | 0.12R | 2, -1.03 (+0.00 / -1.03) | 80 / 6 of 90 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.81; max drawdown 37.8R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 30m | **FAILED** | 3194 | 34.1 | -0.107 | 0.84 | 344.3R | -0.13 / -0.05 | -0.12 / -0.10 | 0/5 ✗ | -0.15 | -0.19 | ✗  stop atr 2.0→1.6: -0.12R | 0 | 0.09R | 35, -0.17 (+0.18 / -1.04) | 308 / 1617 of 2299 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.84; max drawdown 344.3R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V5 🧪 lab | 1.0 | 1h | **FAILED** | 4852 | 30.1 | -0.110 | 0.83 | 569.3R | -0.11 / -0.11 | -0.12 / -0.10 | 0/5 ✗ | -0.18 | -0.24 | ✗  stop atr 1.5→1.2: -0.14R | 0 | 0.12R | 21, -0.49 (-0.44 / -0.58) | 710 / 20 of 884 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.83; max drawdown 569.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 4918 | 55.3 | -0.116 | 0.58 | 576.8R | -0.10 / -0.16 | -0.11 / -0.13 | 0/5 ✗ | -0.17 | -0.23 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.10R | 22, +0.01 (+0.02 / -0.04) | 644 / 10 of 859 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.58; max drawdown 576.8R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 5m | **FAILED** | 2284 | 35.6 | -0.116 | 0.84 | 295.6R | -0.12 / -0.09 | -0.10 / -0.13 | 0/5 ✗ | -0.14 | -0.20 | ✗  stop atr 2.0→1.6: -0.12R | 0 | 0.17R | 33, -0.21 (-0.03 / -0.69) | 192 / 1068 of 1497 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.84; max drawdown 295.6R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 4491 | 46.9 | -0.119 | 0.79 | 551.2R | -0.12 / -0.11 | -0.11 / -0.13 | 0/5 ✗ | -0.18 | -0.24 | ✗  stop atr 1.5→1.2: -0.15R | 0 | 0.12R | 24, -0.09 (+0.56 / -1.17) | 699 / 153 of 1097 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.79; max drawdown 551.2R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 549 | 32.4 | -0.124 | 0.84 | 98.6R | -0.14 / -0.09 | -0.17 / -0.07 | 1/5 ✗ | -0.22 | -0.31 | ✗  stop buffer_atr 0.2→0.16: -0.15R | 1 | 0.19R | 4, +0.21 (+0.51 / -0.09) | 281 / 679 of 1013 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.84; max drawdown 98.6R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V2 🧪 lab | 1.0 | 30m | **FAILED** | 1692 | 30.3 | -0.136 | 0.8 | 236.7R | -0.14 / -0.13 | -0.12 / -0.15 | 0/5 ✗ | -0.24 | -0.34 | ✗  rsi_hi 65→52: -0.30R | 0 | 0.19R | 19, -0.50 (-0.02 / -1.03) | 626 / 156 of 886 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.80; max drawdown 236.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 219 | 48.4 | -0.142 | 0.76 | 34.5R | -0.16 / -0.10 | -0.12 / -0.18 | 1/5 ✗ | -0.21 | -0.27 | ✗  vol_x 1.2→1.44: -0.32R | 2 | 0.14R | 1, +1.11 (+1.11 / +0.00) | 49 / 106 of 162 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 34.5R; not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V5 🧪 lab | 1.0 | 15m | **FAILED** | 2971 | 31.6 | -0.149 | 0.79 | 461.9R | -0.16 / -0.14 | -0.18 / -0.12 | 0/5 ✗ | -0.26 | -0.38 | ✗  stop atr 2.0→1.6: -0.22R | 0 | 0.20R | 40, -0.04 (-0.51 / +0.53) | 209 / 61 of 354 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.79; max drawdown 461.9R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 319 | 49.8 | -0.150 | 0.74 | 51.3R | -0.13 / -0.20 | -0.21 / -0.09 | 1/5 ✗ | -0.25 | -0.36 | ✗  stop atr 1.5→1.2: -0.17R | 0 | 0.20R | 5, -0.91 (-0.53 / -1.17) | 102 / 7 of 118 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.74; max drawdown 51.3R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 460 | 48.7 | -0.163 | 0.73 | 78.2R | -0.20 / -0.11 | -0.21 / -0.09 | 0/5 ✗ | -0.30 | -0.44 | ✗  stop atr 1.5→1.2: -0.27R | 1 | 0.23R | 11, -0.01 (+0.18 / -0.87) | 64 / 21 of 121 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.73; max drawdown 78.2R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V5 🧪 lab | 1.0 | 30m | **FAILED** | 3703 | 30.0 | -0.163 | 0.77 | 602.5R | -0.16 / -0.17 | -0.19 / -0.13 | 0/5 ✗ | -0.28 | -0.40 | ✗  rsi_hi 65→52: -0.26R | 0 | 0.22R | 48, -0.27 (-0.18 / -0.39) | 626 / 38 of 886 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.77; max drawdown 602.5R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 183 | 46.4 | -0.172 | 0.7 | 38.6R | -0.26 / +0.01 | -0.32 / -0.03 | 1/5 ✗ | -0.22 | -0.28 | ✗  adx_min 20→16: -0.27R | 1 | 0.14R | 2, -0.03 (-0.03 / +0.00) | 31 / 4 of 41 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.70; max drawdown 38.6R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 4228 | 45.8 | -0.192 | 0.69 | 811.6R | -0.21 / -0.16 | -0.21 / -0.17 | 0/5 ✗ | -0.30 | -0.40 | ✗  stop atr 1.5→1.2: -0.25R | 0 | 0.19R | 51, -0.49 (-0.31 / -1.09) | 495 / 170 of 1032 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.69; max drawdown 811.6R; not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 5m | **FAILED** | 411 | 35.5 | -0.194 | 0.56 | 81.7R | -0.21 / -0.10 | -0.22 / -0.17 | 0/5 ✗ | -0.29 | -0.36 | ✗  stop max_width_atr 3.0→2.4: -0.21R | 0 | 0.19R | 1, +0.46 (+0.46 / +0.00) | 0 / 0 of 246 | 0 | avg -0.19R/trade (needs +0.15R); profit factor 0.56; max drawdown 81.7R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 3363 | 45.7 | -0.195 | 0.39 | 658.2R | -0.17 / -0.24 | -0.19 / -0.20 | 0/5 ✗ | -0.30 | -0.40 | ✗  stop atr 2.0→1.6: -0.25R | 0 | 0.18R | 29, -0.21 (-0.23 / -0.18) | 718 / 35 of 846 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.39; max drawdown 658.2R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 196 | 45.9 | -0.196 | 0.66 | 42.3R | -0.20 / -0.18 | -0.28 / -0.11 | 0/5 ✗ | -0.25 | -0.30 | ✗  st_n 10→12: -0.23R | 2 | 0.08R | 1, +0.24 (+0.24 / +0.00) | 33 / 1 of 39 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.66; max drawdown 42.3R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V2 🧪 lab | 1.0 | 15m | **FAILED** | 3121 | 28.5 | -0.214 | 0.7 | 693.9R | -0.19 / -0.25 | -0.23 / -0.18 | 0/5 ✗ | -0.37 | -0.52 | ✗  stop atr 1.5→1.2: -0.27R | 0 | 0.28R | 34, -0.55 (-0.36 / -1.08) | 603 / 183 of 880 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.21R/trade (needs +0.10R); profit factor 0.70; max drawdown 693.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 407 | 40.3 | -0.218 | 0.63 | 92.3R | -0.25 / -0.14 | -0.32 / -0.14 | 0/5 ✗ | -0.33 | -0.40 | ✗  slow 21→25: -0.30R | 0 | 0.18R | 6, -1.16 (-1.01 / -1.23) | 59 / 20 of 93 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.63; max drawdown 92.3R; not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 15m | **FAILED** | 462 | 37.4 | -0.226 | 0.59 | 111.5R | -0.22 / -0.24 | -0.18 / -0.27 | 0/5 ✗ | -0.23 | -0.21 | ✗  stop max_width_atr 3.0→2.4: -0.23R | 0 | 0.18R | 1, +0.46 (+0.46 / +0.00) | 0 / 0 of 148 | 0 | avg -0.23R/trade (needs +0.15R); profit factor 0.59; max drawdown 111.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 1150 | 41.5 | -0.237 | 0.62 | 277.9R | -0.26 / -0.18 | -0.27 / -0.20 | 0/5 ✗ | -0.37 | -0.52 | ✗  stop atr 1.5→1.2: -0.35R | 0 | 0.26R | 9, -0.97 (-0.84 / -1.03) | 57 / 14 of 82 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.24R/trade (needs +0.10R); profit factor 0.62; max drawdown 277.9R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V3 🧪 lab | 1.0 | 4h | **FAILED** | 117 | 23.1 | -0.261 | 0.62 | 30.9R | -0.24 / -0.30 | -0.25 / -0.29 | 0/5 ✗ | -0.29 | -0.33 | ✗  fast 20→24: -0.31R | 1 | 0.06R | 1, -1.08 (+0.00 / -1.08) | 132 / 66 of 201 | 0 | avg -0.26R/trade (needs +0.10R); profit factor 0.62; max drawdown 30.9R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V5 🧪 lab | 1.0 | 15m | **FAILED** | 6894 | 27.9 | -0.263 | 0.65 | 1817.7R | -0.23 / -0.31 | -0.30 / -0.22 | 0/5 ✗ | -0.44 | -0.61 | ✗  stop atr 1.5→1.2: -0.33R | 0 | 0.31R | 91, -0.42 (-0.51 / -0.27) | 603 / 67 of 880 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.65; max drawdown 1817.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 7220 | 44.4 | -0.268 | 0.6 | 1937.2R | -0.27 / -0.28 | -0.30 / -0.23 | 0/5 ✗ | -0.41 | -0.57 | ✗  stop atr 1.5→1.2: -0.35R | 0 | 0.28R | 73, -0.69 (-0.60 / -1.06) | 963 / 171 of 1486 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.27R/trade (needs +0.10R); profit factor 0.60; max drawdown 1937.2R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 5362 | 36.0 | -0.277 | 0.25 | 1483.6R | -0.25 / -0.35 | -0.28 / -0.27 | 0/5 ✗ | -0.43 | -0.59 | ✗  stop atr 2.0→1.6: -0.35R | 0 | 0.26R | 75, -0.39 (-0.38 / -0.42) | 757 / 44 of 913 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.28R/trade (needs +0.10R); profit factor 0.25; max drawdown 1483.6R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 147 | 29.3 | -0.278 | 0.68 | 40.9R | -0.28 / -0.28 | -0.52 / +0.11 | 1/5 ✗ | -0.40 | -0.50 | ✗  time_stop_bars 30→24: -0.34R | 1 | 0.26R | 2, +0.66 (+2.79 / -1.47) | 26 / 66 of 97 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.28R/trade (needs +0.10R); profit factor 0.68; max drawdown 40.9R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 940 | 29.3 | -0.304 | 0.61 | 285.8R | -0.32 / -0.27 | -0.24 / -0.35 | 0/5 ✗ | -0.37 | -0.44 | ✗  rsi_n 14→17: -0.43R | 1 | 0.13R | 7, -0.47 (+0.48 / -1.20) | 455 / 3 of 488 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.61; max drawdown 285.8R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 2027 | 29.6 | -0.353 | 0.57 | 715.8R | -0.38 / -0.29 | -0.40 / -0.31 | 0/5 ✗ | -0.48 | -0.60 | ✗  bb_k 2→3: -0.43R | 0 | 0.22R | 22, -0.35 (+0.11 / -1.02) | 379 / 21 of 451 | 0 | avg -0.35R/trade (needs +0.10R); profit factor 0.57; max drawdown 715.8R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 974 | 41.5 | -0.359 | 0.51 | 351.3R | -0.34 / -0.38 | -0.37 / -0.34 | 0/5 ✗ | -0.53 | -0.68 | ✗  stop atr 1.5→1.2: -0.43R | 0 | 0.33R | 11, -0.50 (-0.48 / -0.57) | 66 / 23 of 114 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); avg -0.36R/trade (needs +0.10R); profit factor 0.51; max drawdown 351.3R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 639 | 29.0 | -0.376 | 0.58 | 245.5R | -0.29 / -0.57 | -0.47 / -0.29 | 0/5 ✗ | -0.52 | -0.63 | ✗  stop buffer_atr 0.2→0.16: -0.38R | 0 | 0.31R | 9, -0.05 (-0.31 / +0.27) | 298 / 681 of 1086 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); avg -0.38R/trade (needs +0.10R); profit factor 0.58; max drawdown 245.5R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 85 | 27.1 | -0.403 | 0.49 | 38.1R | -0.41 / -0.39 | +0.03 / -0.83 | 0/5 ✗ | -0.45 | -0.51 | ✗  bb_k 2→3: -0.59R | 0 | 0.12R | 1, -1.07 (+0.00 / -1.07) | 33 / 3 of 37 | 0 | avg -0.40R/trade (needs +0.10R); profit factor 0.49; max drawdown 38.1R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 67 | 23.9 | -0.452 | 0.44 | 36.2R | -0.40 / -0.57 | -0.29 / -0.56 | 1/5 ✗ | -0.50 | -0.55 | ✗  bb_k 2→3: -0.77R | 1 | 0.14R | 3, -0.80 (-0.20 / -1.09) | 8 / 2 of 13 | 0 | avg -0.45R/trade (needs +0.10R); profit factor 0.44; max drawdown 36.2R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 282 | 38.7 | -0.468 | 0.38 | 134.0R | -0.49 / -0.44 | -0.48 / -0.45 | 0/5 ✗ | -0.60 | -0.73 | ✗  stop atr 1.0→0.8: -0.51R | 0 | 0.29R | 3, -1.25 (-1.25 / +0.00) | 66 / 130 of 209 | 0 | not cost-viable: fees + slippage 0.29R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R); profit factor 0.38; max drawdown 134.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 1055 | 37.4 | -0.529 | 0.36 | 560.1R | -0.44 / -0.63 | -0.53 / -0.52 | 0/5 ✗ | -0.77 | -1.00 | ✗  stop atr 1.0→0.8: -0.62R | 0 | 0.43R | 9, -0.81 (-0.91 / -0.61) | 52 / 167 of 236 | 0 | not cost-viable: fees + slippage 0.43R per trade (stop must be ≥ 4x the round-trip cost); avg -0.53R/trade (needs +0.10R); profit factor 0.36; max drawdown 560.1R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 1134 | 33.3 | -0.569 | 0.35 | 647.7R | -0.53 / -0.67 | -0.62 / -0.51 | 0/5 ✗ | -0.86 | -1.14 | ✗  stop atr 1.5→1.2: -0.71R | 0 | 0.51R | 36, -0.86 (-0.85 / -0.88) | 140 / 37 of 213 | 0 | not cost-viable: fees + slippage 0.51R per trade (stop must be ≥ 4x the round-trip cost); avg -0.57R/trade (needs +0.10R); profit factor 0.35; max drawdown 647.7R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-15M | 1.0 | 15m | **FAILED** | 137 | 34.3 | -0.675 | 0.22 | 94.8R | -0.55 / -0.73 | -0.67 / -0.68 | 0/5 ✗ | -0.74 | -0.81 | ✗  stop buffer_atr 0.0→0.0: -0.68R | 0 | 0.53R | 3, -1.32 (-1.32 / +0.00) | 0 / 0 of 16 | 0 | not cost-viable: fees + slippage 0.53R per trade (stop must be ≥ 4x the round-trip cost); avg -0.67R/trade (needs +0.15R); profit factor 0.22; max drawdown 94.8R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP | 1.0 | 5m | **FAILED** | 559 | 34.3 | -0.736 | 0.2 | 412.0R | -0.76 / -0.67 | -0.74 / -0.73 | 0/5 ✗ | -0.83 | -0.90 | ✗  stop max_width_atr 3.0→2.4: -0.74R | 0 | 0.73R | 7, -0.70 (-0.46 / -2.13) | 0 / 0 of 29 | 0 | not cost-viable: fees + slippage 0.73R per trade (stop must be ≥ 4x the round-trip cost); avg -0.74R/trade (needs +0.15R); profit factor 0.20; max drawdown 412.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 2376 | 29.0 | -0.848 | 0.23 | 2014.8R | -0.80 / -1.02 | -0.90 / -0.77 | 0/5 ✗ | -1.31 | -1.79 | ✗  stop atr 1.0→0.8: -1.08R | 0 | 0.81R | 47, -1.27 (-1.27 / -1.29) | 146 / 385 of 580 | 0 | not cost-viable: fees + slippage 0.81R per trade (stop must be ≥ 4x the round-trip cost); avg -0.85R/trade (needs +0.10R); profit factor 0.23; max drawdown 2014.8R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **59** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 246 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.54** (Bonferroni: family-wise false-winner rate 0.05 over 246 trials; with 1 trial it would be 1.65).

**Research run duration:** 48.8 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 55 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (425.8 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 65 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: P02-EMA-PULLBACK-V4-S6.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

3 of 111 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT-S4 v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 10.29 | 16.7R | 529 d (16%) | passes every gate |
| donchian_breakout-VEXIT-S4 v1.1 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 8.11 | 16.5R | 514 d (16%) | passes every gate |
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 10.28 | 13.9R | 506 d (15%) | passes every gate |

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- P01-BREAKOUT-V2 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (76% of 1,849 trades shared)

- P01-BREAKOUT-V2 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (71% of 873 trades shared)

- P01-BREAKOUT-V4 v1.0 4h = near-duplicate of P01-BREAKOUT-V1 v1.0 4h (83% of 900 trades shared)

- P02-EMA-PULLBACK-V4 v1.0 4h = near-duplicate of P02-EMA-PULLBACK-V1 v1.0 4h (99% of 297 trades shared)

- PB-A-GRADED v1.0 5m = near-duplicate of PB-A-APLUS v1.0 5m (82% of 33 trades shared)

- PB-B-SWEEP-LIMIT v1.0 5m = near-duplicate of PB-B-APLUS v1.0 5m (72% of 90 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (79% of 2,400 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (74% of 1,247 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 871 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,107 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (94% of 1,052 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (95% of 765 trades shared)

🧪 **Strategy lab:** 53 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 15m | 3 | +0.270 | -1.301 | -0.164 | -0.273 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 2 | +0.130 | +0.000 | +0.281 | +0.000 | too few trades to compare |
| TRD-H4-BREAKOUT | 1h | 776 | +0.114 | +0.247 | +0.031 | +0.061 | yes |
| TRD-H4-BREAKOUT | 30m | 403 | +0.112 | +0.264 | -0.019 | +0.011 | yes |
| TRD-H4-PULLBACK | 15m | 1456 | +0.005 | +0.144 | -0.080 | -0.058 | yes |
| TRD-H4-BREAKOUT | 15m | 684 | +0.005 | +0.057 | -0.074 | -0.047 | yes |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.089 | +0.241 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | -1.300 | +0.000 | too few trades to compare |
| PB-C-BREAKOUT | 5m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 3 | -0.303 | -0.303 | -0.446 | -0.504 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 10 | -0.345 | -1.171 | -0.045 | -0.542 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 7 | -0.505 | -1.174 | -0.034 | +0.067 | too few trades to compare |
| PB-A-PULLBACK-CVD | 5m | 7 | -0.718 | +0.000 | -0.781 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 1 | -1.208 | +0.000 | -0.213 | +0.000 | too few trades to compare |
| TRD-H4-PULLBACK | 1h | 753 | +0.019 | -0.028 | -0.006 | -0.058 | yes |
| TRD-H4-BREAKOUT | 5m | 890 | -0.015 | -0.003 | -0.116 | -0.089 | yes |
| TRD-H4-PULLBACK | 5m | 1389 | -0.029 | +0.110 | -0.102 | -0.042 | yes |
| TRD-H4-PULLBACK | 30m | 817 | -0.097 | +0.044 | -0.107 | -0.053 | yes |
| S8-PDH-PDL-SWEEP | 1h | 213 | -0.099 | -0.277 | -0.124 | -0.094 | no |
| S8-PDH-PDL-SWEEP | 30m | 147 | -0.278 | -0.280 | -0.376 | -0.574 | yes |
| PB-B-SWEEP | 5m | 559 | -0.736 | -0.672 | -0.700 | -0.700 | too few trades to compare |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): P01-BREAKOUT-V1@1.0 4h FORMALIZED → BACKTESTING; P01-BREAKOUT-V2@1.0 15m FORMALIZED → FAILED; P01-BREAKOUT-V2@1.0 1h FORMALIZED → FAILED; P01-BREAKOUT-V2@1.0 30m FORMALIZED → BACKTESTING; P01-BREAKOUT-V3@1.0 4h FORMALIZED → BACKTESTING; P01-BREAKOUT-V4@1.0 4h FORMALIZED → BACKTESTING; P01-BREAKOUT-V5@1.0 15m FORMALIZED → FAILED; P01-BREAKOUT-V5@1.0 1h FORMALIZED → FAILED; P01-BREAKOUT-V5@1.0 30m FORMALIZED → FAILED; P02-EMA-PULLBACK-V1@1.0 4h FORMALIZED → FAILED; P02-EMA-PULLBACK-V2@1.0 15m FORMALIZED → FAILED; P02-EMA-PULLBACK-V2@1.0 1h FORMALIZED → FAILED; ... and 15 more
- **Not tested (IDEA / RETIRED):** donchian_breakout-VEXIT-VRVOL v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S5 v1.0 (RETIRED)

### 3c. Research layers (daily run)
Last run: **2026-10-10 00:59 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 6 | 2017-08-17 | 2026-10-09 | 20029 |  |
| 1h | 6 | 2017-08-17 | 2026-10-09 | 80052 |  |
| 30m | 5 | 2021-10-02 | 2026-10-10 | 87600 |  |
| 15m | 5 | 2021-10-02 | 2026-10-10 | 175200 |  |
| 5m | 5 | 2024-10-10 | 2026-10-10 | 210240 |  |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 765 (448) | false_breakout, trend_reversal | false_breakout 64% | +0.48R | -0.37R | +0.32 / +0.26 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 871 (518) | false_breakout, trend_reversal | false_breakout 62% | +0.52R | -0.37R | +0.31 / +0.24 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 579 (342) | no_displacement, false_breakout | false_breakout 64%, no_displacement 37% | +0.49R | -0.36R | +0.29 / +0.24 |
| P01-BREAKOUT-V3 | 4h | BACKTESTING | 333 (198) | false_breakout | false_breakout 68%, no_displacement 33% | +0.43R | -0.37R | +0.26 / +0.21 |
| P01-BREAKOUT-V1 | 4h | BACKTESTING | 1058 (639) | htf_conflict, false_breakout, trend_reversal | false_breakout 62% | +0.53R | -0.41R | +0.24 / +0.19 |
| P01-BREAKOUT-V4 | 4h | BACKTESTING | 900 (544) | htf_conflict, false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, regime_mismatch 39%, stop_too_tight 38% | +0.53R | -0.43R | +0.25 / +0.18 |
| donchian_breakout | 4h | BACKTESTING | 787 (343) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 67%, stop_too_tight 34%, no_displacement 34% | +0.33R | -0.37R | +0.23 / +0.17 |
| TRD-H4-BREAKOUT | 1h | BACKTESTING | 776 (478) | false_breakout | false_breakout 64% | +0.53R | -0.44R | +0.17 / +0.11 |
| TRD-H4-BREAKOUT | 30m | BACKTESTING | 403 (242) | false_breakout, trend_reversal | false_breakout 77%, no_displacement 46% | +0.53R | -0.45R | +0.20 / +0.11 |
| P02-EMA-PULLBACK-V4 | 4h | BACKTESTING | 297 (193) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 84%, indicator_lag 36%, stop_too_tight 28% | +0.43R | -0.50R | +0.18 / +0.10 |
| TRD-H4-BREAKOUT-noT4 | 1h | BACKTESTING | 2475 (1559) | false_breakout | false_breakout 65% | +0.51R | -0.45R | +0.10 / +0.03 |
| donchian_breakout-VEXIT-S4 | 30m | BACKTESTING | 796 (504) | no_displacement, false_breakout | false_breakout 74%, no_displacement 37% | +0.46R | -0.41R | +0.18 / +0.03 |
| macd_trend_cross | 1h | BACKTESTING | 127 (60) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 90%, indicator_lag 45%, stop_too_tight 35% | +0.28R | -0.40R | +0.17 / +0.03 |
| bb_squeeze_breakout | 1h | BACKTESTING | 597 (280) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, no_displacement 51%, stop_too_tight 39%, regime_mismatch 34% | +0.38R | -0.47R | +0.17 / +0.02 |
| TRD-H4-PULLBACK | 15m | BACKTESTING | 1456 (890) | none | - | +0.48R | -0.41R | +0.12 / +0.01 |
| TRD-H4-BREAKOUT | 15m | BACKTESTING | 684 (434) | false_breakout | false_breakout 76% | +0.47R | -0.48R | +0.12 / +0.01 |
| P01-BREAKOUT-V2 | 30m | BACKTESTING | 873 (557) | no_displacement, false_breakout | false_breakout 75%, no_displacement 38% | +0.45R | -0.42R | +0.16 / +0.01 |
| PB-B-SWEEP-LIMIT | 5m | BACKTESTING | 90 (52) | none | low_relative_volume 25% | +0.24R | -0.26R | +0.09 / -0.10 |
| PB-B-APLUS | 5m | BACKTESTING | 67 (42) | none | - | +0.18R | -0.32R | +0.07 / -0.12 |
| PB-A-GRADED | 5m | BACKTESTING | 33 (19) | none | stop_too_tight 37% | +0.48R | -0.26R | -0.10 / -0.29 |
| PB-B-APLUS | 15m | BACKTESTING | 34 (21) | none | regime_mismatch 52%, stop_too_tight 38% | +0.29R | -0.34R | -0.31 / -0.49 |
| bb_squeeze_breakout | 4h | FAILED | 199 (95) | false_breakout, stop_too_tight, structural_change | false_breakout 60%, range_market 50%, stop_too_tight 42%, regime_mismatch 32% | +0.33R | -0.36R | +0.13 / +0.04 |
| TRD-H4-PULLBACK | 1h | FAILED | 753 (470) | low_relative_volume, indicator_lag, structural_change | low_relative_volume 56%, indicator_lag 26% | +0.45R | -0.41R | +0.08 / +0.02 |
| TRD-H4-PULLBACK-noT4 | 1h | FAILED | 3457 (2144) | structural_change | - | +0.50R | -0.42R | +0.06 / -0.01 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 1654 (1113) | false_breakout, regime_mismatch | false_breakout 62%, regime_mismatch 30% | +0.50R | -0.40R | +0.07 / -0.01 |
| TRD-H4-BREAKOUT | 5m | FAILED | 890 (544) | false_breakout | false_breakout 74% | +0.43R | -0.45R | +0.14 / -0.01 |
| TRD-H4-BREAKOUT-noT4 | 30m | FAILED | 1336 (851) | false_breakout | false_breakout 72% | +0.49R | -0.43R | +0.09 / -0.02 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2400 (1616) | false_breakout, regime_mismatch | false_breakout 64%, regime_mismatch 32% | +0.50R | -0.40R | +0.08 / -0.02 |
| P01-BREAKOUT-V2 | 1h | FAILED | 1849 (1251) | false_breakout | false_breakout 64% | +0.52R | -0.38R | +0.07 / -0.02 |
| P01-BREAKOUT-V5 | 1h | FAILED | 3762 (2521) | false_breakout | false_breakout 61% | +0.50R | -0.41R | +0.08 / -0.02 |
| P02-EMA-PULLBACK-V1 | 4h | FAILED | 299 (205) | regime_mismatch, indicator_lag, structural_change | regime_mismatch 85%, indicator_lag 38% | +0.41R | -0.42R | +0.06 / -0.02 |
| donchian_breakout-VEXIT | 1h | FAILED | 2107 (1424) | false_breakout | false_breakout 64% | +0.51R | -0.40R | +0.07 / -0.03 |
| TRD-H4-PULLBACK | 5m | FAILED | 1389 (858) | none | - | +0.51R | -0.41R | +0.12 / -0.03 |
| supertrend_flip | 4h | FAILED | 66 (35) | indicator_lag, structural_change | regime_mismatch 63%, indicator_lag 37% | +0.58R | -0.44R | +0.03 / -0.04 |
| donchian_breakout | 1h | FAILED | 2162 (1124) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 32%, regime_mismatch 26% | +0.37R | -0.41R | +0.05 / -0.04 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1247 (815) | false_breakout | false_breakout 72%, no_displacement 38% | +0.46R | -0.43R | +0.12 / -0.04 |
| P01-BREAKOUT-V2 | 15m | FAILED | 1330 (872) | false_breakout | false_breakout 71% | +0.47R | -0.43R | +0.15 / -0.06 |
| donchian_breakout-VEXIT | 30m | FAILED | 1052 (699) | no_displacement, false_breakout | false_breakout 72%, no_displacement 36% | +0.44R | -0.42R | +0.10 / -0.06 |
| TRD-H4-BREAKOUT-noT4 | 15m | FAILED | 2224 (1448) | no_displacement, false_breakout | false_breakout 74% | +0.46R | -0.45R | +0.06 / -0.07 |
| trend_pullback | 4h | FAILED | 874 (454) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 81%, indicator_lag 38%, stop_too_tight 25% | +0.36R | -0.43R | +0.00 / -0.08 |
| TRD-H4-PULLBACK-noT4 | 15m | FAILED | 5340 (3383) | none | - | +0.49R | -0.39R | +0.05 / -0.08 |
| S6-OB-FVG-noSMC | 15m | FAILED | 61 (40) | none | range_market 55% | +0.35R | -0.28R | +0.10 / -0.09 |
| donchian_breakout | 30m | FAILED | 1095 (575) | no_displacement, false_breakout, trend_reversal, stop_too_tight | false_breakout 76%, no_displacement 37%, stop_too_tight 35% | +0.28R | -0.40R | +0.07 / -0.09 |
| P02-EMA-PULLBACK-V2 | 1h | FAILED | 2302 (1585) | low_relative_volume, regime_mismatch, indicator_lag | regime_mismatch 82%, low_relative_volume 52%, indicator_lag 37% | +0.40R | -0.42R | +0.04 / -0.09 |
| P01-BREAKOUT-V5 | 30m | FAILED | 1938 (1301) | false_breakout | false_breakout 70% | +0.46R | -0.42R | +0.08 / -0.10 |
| TRD-H4-PULLBACK | 30m | FAILED | 817 (536) | none | - | +0.46R | -0.39R | -0.01 / -0.10 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 213 (140) | range_market, stop_too_tight, sweep_continued | sweep_continued 96%, range_market 57%, stop_too_tight 29% | +0.59R | -0.39R | +0.12 / -0.10 |
| TRD-H4-PULLBACK-noT4 | 5m | FAILED | 3649 (2286) | overextended_entry | - | +0.50R | -0.42R | +0.06 / -0.10 |
| rsi2_dip_buy | 4h | FAILED | 1318 (569) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 46% | +0.15R | -0.21R | -0.05 / -0.10 |
| ema_9_21_cross | 1h | FAILED | 248 (139) | regime_mismatch, indicator_lag | regime_mismatch 81%, indicator_lag 48% | +0.27R | -0.35R | +0.03 / -0.10 |
| TRD-H4-PULLBACK-noT4 | 30m | FAILED | 3194 (2104) | none | - | +0.50R | -0.38R | -0.00 / -0.11 |
| P02-EMA-PULLBACK-V5 | 1h | FAILED | 4852 (3391) | low_relative_volume, regime_mismatch, indicator_lag | regime_mismatch 84%, indicator_lag 38% | +0.40R | -0.41R | +0.04 / -0.11 |
| rsi2_dip_buy | 1h | FAILED | 4918 (2199) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 43% | +0.16R | -0.21R | +0.00 / -0.12 |
| TRD-H4-BREAKOUT-noT4 | 5m | FAILED | 2284 (1470) | false_breakout | false_breakout 71% | +0.47R | -0.42R | +0.05 / -0.12 |
| trend_pullback | 1h | FAILED | 4491 (2385) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 77%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.43R | +0.02 / -0.12 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 549 (371) | range_market, htf_conflict, stop_too_tight | range_market 47%, stop_too_tight 37% | +0.58R | -0.50R | +0.10 / -0.12 |
| P02-EMA-PULLBACK-V2 | 30m | FAILED | 1692 (1180) | range_market, low_relative_volume, indicator_lag | low_relative_volume 59%, indicator_lag 40%, range_market 37% | +0.37R | -0.40R | +0.09 / -0.14 |
| liquidity_sweep_reversal | 1h | FAILED | 219 (113) | stop_too_tight | stop_too_tight 51%, range_market 43% | +0.29R | -0.49R | +0.02 / -0.14 |
| P01-BREAKOUT-V5 | 15m | FAILED | 2971 (2032) | false_breakout | false_breakout 70% | +0.44R | -0.42R | +0.09 / -0.15 |
| macd_trend_cross | 30m | FAILED | 319 (160) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 74%, indicator_lag 42%, stop_too_tight 37%, low_relative_volume 35% | +0.30R | -0.45R | +0.08 / -0.15 |
| bb_squeeze_breakout | 30m | FAILED | 460 (236) | false_breakout, stop_too_tight | false_breakout 61%, stop_too_tight 36% | +0.28R | -0.52R | +0.10 / -0.16 |
| P02-EMA-PULLBACK-V5 | 30m | FAILED | 3703 (2593) | range_market, low_relative_volume, indicator_lag | indicator_lag 40% | +0.37R | -0.42R | +0.09 / -0.16 |
| supertrend_flip | 30m | FAILED | 183 (98) | stop_too_tight, indicator_lag | regime_mismatch 42%, stop_too_tight 38%, indicator_lag 36%, late_entry 34% | +0.42R | -0.41R | -0.00 / -0.17 |
| trend_pullback | 30m | FAILED | 4228 (2290) | stop_too_tight, indicator_lag | indicator_lag 47%, stop_too_tight 29% | +0.27R | -0.44R | +0.04 / -0.19 |
| PB-B-GRADED | 5m | FAILED | 411 (265) | none | low_relative_volume 28% | +0.20R | -0.23R | -0.01 / -0.19 |
| rsi2_dip_buy | 30m | FAILED | 3363 (1827) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 35% | +0.16R | -0.20R | +0.01 / -0.20 |
| supertrend_flip | 1h | FAILED | 196 (106) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 72%, regime_mismatch 71%, stop_too_tight 35%, indicator_lag 32% | +0.40R | -0.37R | -0.10 / -0.20 |
| P02-EMA-PULLBACK-V2 | 15m | FAILED | 3121 (2231) | range_market, htf_conflict, indicator_lag | range_market 47%, indicator_lag 43% | +0.34R | -0.39R | +0.11 / -0.21 |
| ema_9_21_cross | 30m | FAILED | 407 (243) | indicator_lag | indicator_lag 47% | +0.27R | -0.36R | -0.00 / -0.22 |
| PB-B-GRADED | 15m | FAILED | 462 (289) | stop_too_tight | stop_too_tight 35% | +0.33R | -0.31R | -0.05 / -0.23 |
| ema_9_21_cross | 15m | FAILED | 1150 (673) | indicator_lag | indicator_lag 51% | +0.24R | -0.45R | +0.07 / -0.24 |
| P02-EMA-PULLBACK-V3 | 4h | FAILED | 117 (90) | indicator_lag | indicator_lag 39% | +0.40R | -0.41R | -0.18 / -0.26 |
| P02-EMA-PULLBACK-V5 | 15m | FAILED | 6894 (4974) | range_market, wrong_session, indicator_lag | indicator_lag 45% | +0.32R | -0.40R | +0.10 / -0.26 |
| trend_pullback | 15m | FAILED | 7220 (4017) | range_market, stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 29% | +0.27R | -0.44R | +0.06 / -0.27 |
| rsi2_dip_buy | 15m | FAILED | 5362 (3429) | low_relative_volume, wrong_session, trend_reversal, regime_mismatch, fees_slippage | fees_slippage 47% | +0.16R | -0.20R | +0.04 / -0.28 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 147 (104) | stop_too_tight, sweep_continued | sweep_continued 97%, stop_too_tight 26% | +0.43R | -0.50R | +0.03 / -0.28 |
| R4-BBRSI | 1h | FAILED | 940 (665) | none | - | +0.45R | -0.48R | -0.14 / -0.30 |
| R4-BBRSI | 30m | FAILED | 2027 (1426) | none | - | +0.40R | -0.45R | -0.09 / -0.35 |
| bb_squeeze_breakout | 15m | FAILED | 974 (570) | false_breakout, stop_too_tight | false_breakout 64%, stop_too_tight 37% | +0.28R | -0.48R | +0.02 / -0.36 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 639 (454) | stop_too_tight | stop_too_tight 35% | +0.54R | -0.54R | -0.00 / -0.38 |
| R4-CLUC | 30m | FAILED | 85 (62) | none | - | +0.32R | -0.31R | -0.28 / -0.40 |
| R4-CLUC | 15m | FAILED | 67 (51) | none | wrong_session 69% | +0.42R | -0.16R | -0.32 / -0.45 |
| liquidity_sweep_reversal | 30m | FAILED | 282 (173) | stop_too_tight | stop_too_tight 42% | +0.31R | -0.51R | -0.15 / -0.47 |
| liquidity_sweep_reversal | 15m | FAILED | 1055 (660) | stop_too_tight | stop_too_tight 41% | +0.29R | -0.48R | -0.02 / -0.53 |
| ema_9_21_cross | 5m | FAILED | 1134 (756) | stop_too_tight, indicator_lag | indicator_lag 54%, stop_too_tight 29% | +0.20R | -0.45R | +0.03 / -0.57 |
| PB-B-SWEEP-15M | 15m | FAILED | 137 (90) | stop_too_tight | stop_too_tight 32% | +0.23R | -0.48R | -0.09 / -0.68 |
| PB-B-SWEEP | 5m | FAILED | 559 (367) | stop_too_tight | stop_too_tight 33% | +0.13R | -0.42R | +0.09 / -0.74 |
| liquidity_sweep_reversal | 5m | FAILED | 2376 (1688) | range_market, stop_too_tight | stop_too_tight 39%, range_market 32% | +0.24R | -0.52R | +0.10 / -0.85 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `false_breakout` (systematic in 33 strategy/timeframe tests); `stop_too_tight` (systematic in 29 strategy/timeframe tests); `indicator_lag` (systematic in 23 strategy/timeframe tests); `regime_mismatch` (systematic in 19 strategy/timeframe tests); `trend_reversal` (systematic in 10 strategy/timeframe tests); `range_market` (systematic in 8 strategy/timeframe tests); `no_displacement` (systematic in 7 strategy/timeframe tests); `low_relative_volume` (systematic in 6 strategy/timeframe tests); `htf_conflict` (systematic in 4 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests); `wrong_session` (systematic in 2 strategy/timeframe tests)

**Missed moves:** no strong move in the last 24 hours at the last research run.

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 138.1 KB | - | - |
| `memory/cleanup_log.md` | 0.5 KB | - | - |
| `memory/coin_notes.md` | 14.3 KB | 14 | 2026-10-04 02:31 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 15.6 KB | 35 | 2026-10-10 01:48 UTC |
| `memory/experiments.md` | 70.3 KB | 28 | 2026-10-09 15:30 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 343.8 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 19.1 KB | - | - |
| `memory/missed_trades.md` | 55.5 KB | 71 | 2026-10-09 01:00 UTC |
| `memory/playbook.md` | 10.0 KB | - | - |
| `memory/research_sources.md` | 108.9 KB | 83 | 2026-10-10 00:59 UTC |
| `memory/smc_events.csv` | 1272.5 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 31.1 KB | - | - |
| `memory/strategy_registry.csv` | 76.6 KB | - | - |
| `memory/trials.csv` | 17.5 KB | - | - |
| `memory/universe_log.md` | 26.5 KB | - | - |

**Reviews due** (review date passed; for the reviews): `missed_trades.md` LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00 (2026-10-02); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03); `missed_trades.md` SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells (2026-10-03); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03) … and 19 more
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG and SHORT = OKX futures fees + funding (always charged, never received). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*