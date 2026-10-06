# Crypto Signal Report

**Updated:** 2026-10-06 17:21 Beijing time (2026-10-06 09:21 UTC) · data: Binance · 8 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 10.0 MB (GitHub) · large files of this run 4.2 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-06 09:21 UTC / 2026-10-06 17:21 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5%
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.02% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| RLC | **DEGRADED** | 1d: DEGRADED: volume 85x normal on candle 10-05 00:00 UTC (possible bad data) |
- 57 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-06 09:21 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 979 h since 2026-08-26 | +0.0044% | 1.12 | 1.28 | - |
| ETH | GOOD | okx | 979 h since 2026-08-26 | +0.0035% | 1.38 | 1.03 | - |
| ZEC | GOOD | okx | 979 h since 2026-08-26 | +0.0100% | 0.78 | 0.96 | - |
| SOL | GOOD | okx | 979 h since 2026-08-26 | +0.0003% | 1.73 | 1.24 | - |
| XRP | GOOD | okx | 979 h since 2026-08-26 | +0.0091% | 2.87 | 1.27 | - |
| SUI | GOOD | okx | 979 h since 2026-08-26 | -0.0054% | 2.84 | 1.06 | - |
| BNB | GOOD | okx | 979 h since 2026-08-26 | +0.0093% | 2.36 | 2.59 | - |
| ENA | GOOD | okx | 979 h since 2026-08-26 | -0.0008% | 2.56 | 0.66 | - |

*Binance futures API: blocked from GitHub's servers (HTTP 451) - expected, not a problem. The main series (OKX) is complete; Binance research history comes from the data.binance.vision files.*

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **ZEC**, **SOL**, **XRP**, **SUI**, **BNB**
- **Research only** - backtested, never a signal: ENA

| Not eligible | 24h volume | Why |
|---|---|---|
| ADA | $67M | 7-day average volume $47M < $50M |
| RLC | $55M | 7-day average volume $5M < $50M; 24h move +127.0% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $32k within 1% (need $250k) |

**Flags (not excluded):** RLC: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* NEAR, RLUSD, USD1, USDC (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 477 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ETH | 477 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ZEC | 394 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| SOL | 321 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| XRP | 440 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| SUI | 179 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| BNB | 465 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| ENA | 131 | 917 | 911 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | down (LH/LL) | 86,130.4 / 84,972 | 0.92 | 1.04x | 1.03x | bull_engulf |
| ETH | down (LH/LL) | 2,723.56 / 2,679.63 | 1.00 | 1.21x | 0.95x | bull_engulf, bull_reject |
| ZEC | mixed (LH/HL) | 1,360.4 / 1,330.11 | 0.82 | 0.94x | 1.00x | bull_engulf |
| SOL | mixed (HH/LL) | 121.59 / 118.93 | 0.52 | 1.09x | 0.95x | bull_reject |
| XRP | down (LH/LL) | 1.5095 / 1.486 | 0.56 | 0.86x | 0.92x | bear_engulf, bull_reject |
| SUI | down (LH/LL) | 1.2323 / 1.176 | 0.72 | 0.79x | 0.82x | - |
| BNB | down (LH/LL) | 789.48 / 780.1 | 1.00 | 0.88x | 0.88x | breakout_down, retest_down, failed_breakout_down |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 388 | 48% | 34% | 26% | 80% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | displacement_down | 283 | 46% | 29% | 18% | 78% | 44% | 29% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 977 | 45% | 32% | 23% | 77% | 45% | 31% | can't tell from chance | 0.09R |
| 4h | bear_engulf | 1108 | 43% | 27% | 17% | 79% | 47% | 31% | worse than chance | 0.08R |
| 4h | bull_reject | 735 | 42% | 29% | 21% | 78% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | bear_reject | 725 | 46% | 31% | 21% | 75% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 517 | 45% | 31% | 23% | 77% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bear | 550 | 42% | 27% | 18% | 80% | 45% | 29% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 235 | 45% | 29% | 21% | 82% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_bos_down | 182 | 49% | 34% | 20% | 73% | 47% | 33% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 75 | 52% | 35% | 28% | 81% | 43% | 31% | can't tell from chance | 0.08R |
| 4h | smc_choch_down | 70 | 40% | 26% | 14% | 76% | 46% | 30% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 535 | 46% | 30% | 24% | 76% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bear | 538 | 47% | 31% | 20% | 76% | 46% | 31% | can't tell from chance | 0.08R |
| 1h | displacement_up | 486 | 45% | 32% | 27% | 75% | 44% | 30% | can't tell from chance | 0.18R |
| 1h | displacement_down | 341 | 37% | 23% | 14% | 82% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | bull_engulf | 1388 | 42% | 29% | 22% | 75% | 44% | 30% | can't tell from chance | 0.20R |
| 1h | bear_engulf | 1514 | 38% | 24% | 17% | 79% | 38% | 24% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1116 | 42% | 30% | 23% | 75% | 44% | 31% | can't tell from chance | 0.20R |
| 1h | bear_reject | 1140 | 36% | 24% | 17% | 81% | 38% | 24% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bull | 508 | 41% | 25% | 19% | 78% | 44% | 30% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bear | 554 | 38% | 24% | 15% | 81% | 37% | 24% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 327 | 45% | 35% | 28% | 76% | 44% | 30% | can't tell from chance | 0.17R |
| 1h | smc_bos_down | 215 | 42% | 31% | 22% | 80% | 40% | 25% | can't tell from chance | 0.22R |
| 1h | smc_choch_up | 82 | 49% | 33% | 29% | 76% | 43% | 30% | can't tell from chance | 0.21R |
| 1h | smc_choch_down | 82 | 43% | 30% | 17% | 72% | 40% | 25% | can't tell from chance | 0.18R |
| 1h | smc_fvg_retrace_bull | 703 | 45% | 31% | 24% | 73% | 45% | 31% | can't tell from chance | 0.19R |
| 1h | smc_fvg_retrace_bear | 643 | 38% | 27% | 19% | 78% | 37% | 24% | can't tell from chance | 0.21R |
| 30m | displacement_up | 430 | 37% | 27% | 21% | 81% | 43% | 29% | worse than chance | 0.22R |
| 30m | displacement_down | 335 | 43% | 29% | 18% | 79% | 36% | 21% | beats chance | 0.22R |
| 30m | bull_engulf | 1351 | 42% | 28% | 19% | 77% | 43% | 29% | can't tell from chance | 0.24R |
| 30m | bear_engulf | 1454 | 37% | 22% | 15% | 81% | 35% | 21% | can't tell from chance | 0.24R |
| 30m | bull_reject | 1036 | 47% | 30% | 22% | 74% | 43% | 29% | beats chance | 0.25R |
| 30m | bear_reject | 1203 | 35% | 20% | 14% | 82% | 36% | 21% | can't tell from chance | 0.23R |
| 30m | smc_sweep_bull | 537 | 43% | 28% | 19% | 75% | 43% | 28% | can't tell from chance | 0.23R |
| 30m | smc_sweep_bear | 515 | 40% | 26% | 17% | 82% | 36% | 21% | can't tell from chance | 0.22R |
| 30m | smc_bos_up | 325 | 36% | 29% | 24% | 79% | 43% | 29% | worse than chance | 0.24R |
| 30m | smc_bos_down | 208 | 34% | 22% | 12% | 85% | 36% | 22% | can't tell from chance | 0.23R |
| 30m | smc_choch_up | 86 | 37% | 22% | 16% | 87% | 39% | 26% | can't tell from chance | 0.23R |
| 30m | smc_choch_down | 87 | 40% | 25% | 22% | 77% | 36% | 23% | can't tell from chance | 0.22R |
| 30m | smc_fvg_retrace_bull | 774 | 41% | 26% | 18% | 79% | 43% | 29% | can't tell from chance | 0.24R |
| 30m | smc_fvg_retrace_bear | 655 | 38% | 21% | 15% | 81% | 34% | 20% | beats chance | 0.26R |
| 15m | displacement_up | 421 | 36% | 25% | 18% | 84% | 39% | 28% | can't tell from chance | 0.30R |
| 15m | displacement_down | 308 | 32% | 21% | 12% | 84% | 33% | 19% | can't tell from chance | 0.31R |
| 15m | bull_engulf | 1393 | 39% | 29% | 20% | 77% | 39% | 28% | can't tell from chance | 0.33R |
| 15m | bear_engulf | 1329 | 30% | 18% | 11% | 82% | 32% | 18% | can't tell from chance | 0.32R |
| 15m | bull_reject | 1027 | 39% | 29% | 20% | 76% | 39% | 28% | can't tell from chance | 0.34R |
| 15m | bear_reject | 1220 | 34% | 20% | 13% | 82% | 34% | 19% | can't tell from chance | 0.31R |
| 15m | smc_sweep_bull | 457 | 39% | 28% | 21% | 76% | 38% | 27% | can't tell from chance | 0.29R |
| 15m | smc_sweep_bear | 473 | 34% | 21% | 11% | 85% | 34% | 19% | can't tell from chance | 0.30R |
| 15m | smc_bos_up | 340 | 37% | 26% | 20% | 80% | 39% | 28% | can't tell from chance | 0.30R |
| 15m | smc_bos_down | 209 | 25% | 15% | 10% | 88% | 32% | 18% | worse than chance | 0.35R |
| 15m | smc_choch_up | 69 | 29% | 17% | 10% | 88% | 40% | 30% | can't tell from chance | 0.37R |
| 15m | smc_choch_down | 68 | 32% | 19% | 10% | 84% | 33% | 18% | can't tell from chance | 0.34R |
| 15m | smc_fvg_retrace_bull | 882 | 39% | 27% | 20% | 76% | 38% | 28% | can't tell from chance | 0.33R |
| 15m | smc_fvg_retrace_bear | 689 | 32% | 21% | 13% | 83% | 32% | 19% | can't tell from chance | 0.34R |
| 5m | displacement_up | 1001 | 30% | 20% | 15% | 87% | 30% | 21% | can't tell from chance | 0.58R |
| 5m | displacement_down | 919 | 23% | 16% | 11% | 86% | 28% | 18% | worse than chance | 0.54R |
| 5m | bull_engulf | 3469 | 29% | 19% | 14% | 83% | 30% | 20% | can't tell from chance | 0.58R |
| 5m | bear_engulf | 3351 | 27% | 18% | 12% | 83% | 27% | 18% | can't tell from chance | 0.62R |
| 5m | bull_reject | 2661 | 29% | 20% | 14% | 82% | 29% | 20% | can't tell from chance | 0.63R |
| 5m | bear_reject | 3042 | 29% | 19% | 12% | 83% | 28% | 19% | can't tell from chance | 0.58R |
| 5m | smc_sweep_bull | 947 | 33% | 22% | 16% | 79% | 31% | 21% | can't tell from chance | 0.48R |
| 5m | smc_sweep_bear | 1002 | 31% | 22% | 14% | 83% | 29% | 19% | can't tell from chance | 0.52R |
| 5m | smc_bos_up | 693 | 29% | 20% | 15% | 87% | 30% | 20% | can't tell from chance | 0.62R |
| 5m | smc_bos_down | 654 | 23% | 16% | 11% | 87% | 28% | 18% | worse than chance | 0.60R |
| 5m | smc_choch_up | 178 | 33% | 24% | 17% | 86% | 31% | 21% | can't tell from chance | 0.65R |
| 5m | smc_choch_down | 180 | 20% | 12% | 7% | 89% | 27% | 19% | worse than chance | 0.52R |
| 5m | smc_fvg_retrace_bull | 2820 | 30% | 20% | 14% | 83% | 29% | 20% | can't tell from chance | 0.67R |
| 5m | smc_fvg_retrace_bear | 2459 | 25% | 18% | 11% | 84% | 27% | 18% | can't tell from chance | 0.66R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (strong) | WEAK_BULL (moderate) | UNCLEAR (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H UNCLEAR, 1H RANGE)) |
| **ETH** | WEAK_BULL (weak) | WEAK_BULL (moderate) | COMPRESSION (moderate) | RANGE (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H COMPRESSION, 1H RANGE)) |
| **ZEC** | WEAK_BULL (weak) | WEAK_BULL (weak) | COMPRESSION (moderate) | RANGE (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H COMPRESSION, 1H RANGE)) |
| **SOL** | WEAK_BULL (moderate) | WEAK_BULL (weak) | UNCLEAR (weak) | RANGE (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H UNCLEAR, 1H RANGE)) |
| **XRP** | TRANSITION (weak) | WEAK_BULL (weak) | COMPRESSION (strong) | RANGE (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H COMPRESSION, 1H RANGE)) |
| **SUI** | UNCLEAR (weak) | WEAK_BULL (weak) | TRANSITION (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H RANGE)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (strong) | TRANSITION (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H TRANSITION, 1H RANGE)) |
| **ENA** | WEAK_BULL (moderate) | STRONG_BULL (weak) | WEAK_BULL (weak) | RANGE (strong) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.8 ATR in 10 candles); swing structure down (LH/LL); ADX 28 = strong trend; candle size 0.71x normal, Bollinger width above 62% of the last 100 candles · against: -
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.2 ATR in 10 candles); ADX 43 = strong trend; candle size 1.00x normal, Bollinger width above 64% of the last 100 candles; volume 0.90x normal · against: swing structure mixed (neutral)
- **4H UNCLEAR (weak)** - for: candle size 0.88x normal, Bollinger width above 24% of the last 100 candles · against: close above EMA-fast above EMA-slow; EMA-fast flat (+0.7 ATR in 10 candles); swing structure mixed; ADX 23 = in between (20-25); ADX 23 is close to a threshold; signals are mixed and trend strength is in between
- **1H RANGE (weak)** - for: EMA-fast flat (+0.0 ATR in 10 candles); ADX 14 = weak trend / ranging; candle size 1.03x normal, Bollinger width above 36% of the last 100 candles · against: close above EMA-fast above EMA-slow; swing structure down (LH/LL)

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | up (CHOCH 4 candles ago) | sell-side (bullish idea) 22 candles ago | bull 85,636.32-85,768.02 | bear 86,133.40-86,975.51 | premium (91%) | swing high 86,130.45 (0.29 ATR) | swing low 84,972.01 (3.0 ATR) |
| **ETH** | up (CHOCH 6 candles ago) | buy-side (bearish idea) 32 candles ago | bull 2,699.44-2,706.99 | bull 2,652.20-2,695.38 | premium (85%) | swing high 2,723.56 (0.59 ATR) | PDL 2,679.63 (3.29 ATR) |
| **ZEC** | up (BOS 2 candles ago) | buy-side (bearish idea) 3 candles ago | bull 1,336.75-1,339.01 | bear 1,397.89-1,447.60 | premium (67%) | swing high 1,360.40 (0.59 ATR) | swing low 1,278.00 (4.25 ATR) |
| **SOL** | down (BOS 12 candles ago) | buy-side (bearish idea) 55 candles ago | bull 119.88-120.13 | bull 115.86-117.34 | premium (59%) | swing high 121.59 (1.73 ATR) | swing low 118.93 (2.52 ATR) |
| **XRP** | down (CHOCH 12 candles ago) | sell-side (bullish idea) 22 candles ago | bull 1.4981-1.4998 | bull 1.3773-1.3856 | premium (75%) | swing high 1.5095 (0.71 ATR) | swing low 1.4860 (2.12 ATR) |
| **SUI** | down (CHOCH 12 candles ago) | buy-side (bearish idea) 4 candles ago | bear 1.2016-1.2069 (retraced) | bull 1.1707-1.1875 | discount (47%) | swing high 1.2323 (2.03 ATR) | swing low 1.1760 (1.83 ATR) |
| **BNB** | down (CHOCH 12 candles ago) | buy-side (bearish idea) 0 candles ago | bear 784.04-785.35 | bull 765.01-768.61 | discount (31%) | swing high 789.48 (2.11 ATR) | swing low 764.83 (5.97 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 73 (Greed), yesterday 70  (extreme fear/greed = bigger, faster moves)

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
- **Event calendar (next 7 days):** none listed

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-10-06 00:56 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 4 | 50.0 | +0.973 | 2.72 | 2.3R | +0.97 / +0.00 | +0.00 / +0.97 | 0/5 ✗ | +0.85 | +0.73 | stable | 0 | 0.19R | 0, +0.00 (+0.00 / +0.00) | 9 / 3 of 14 | 0 | only 4 trades; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 13 | 46.2 | +0.407 | 1.57 | 3.8R | +0.41 / +0.40 | +0.04 / +0.64 | 0/5 ✗ | +0.11 | -0.04 | stable | 0 | 0.31R | 1, -1.20 (-1.20 / +0.00) | 35 / 9 of 53 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); only 13 trades; only 4 unseen-test trades |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.259 | 1.36 | 1.5R | -1.45 / +1.97 | +0.26 / +0.00 | 0/5 ✗ | +0.05 | -0.14 | ✗  time_stop_bars 30→36: -0.08R | 0 | 0.47R | 1, +1.97 (+1.97 / +0.00) | 33 / 82 of 122 | 0 | not cost-viable: fees + slippage 0.47R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 853 | 41.0 | +0.251 | 1.48 | 23.4R | +0.24 / +0.27 | +0.30 / +0.19 | 5/5 | +0.22 | +0.20 | stable | 8 | 0.04R | 6, -0.25 (-0.09 / -1.07) | 75 / 37 of 210 | 0 | max drawdown 23.4R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 968 | 40.6 | +0.245 | 1.46 | 21.9R | +0.25 / +0.24 | +0.27 / +0.22 | 5/5 | +0.21 | +0.19 | stable | 8 | 0.04R | 7, -0.36 (-0.24 / -1.07) | 127 / 49 of 284 | 0 | max drawdown 21.9R |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.226 | 1.24 | 3.3R | +0.51 / -1.20 | -1.20 / +0.51 | 0/5 ✗ | +0.10 | +0.00 | ✗  sweep_bars 20→24: -0.15R | 0 | 0.25R | 1, -1.20 (-1.20 / +0.00) | 31 / 7 of 45 | 0 | only 6 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 877 | 55.8 | +0.159 | 1.37 | 18.9R | +0.16 / +0.17 | +0.17 / +0.15 | 5/5 | +0.13 | +0.11 | stable | 7 | 0.04R | 7, -0.14 (+0.01 / -1.07) | 75 / 37 of 210 | 0 | max drawdown 18.9R |
| bb_squeeze_breakout | 1.0 | 1h | **BACKTESTING** | 678 | 53.5 | +0.024 | 1.05 | 28.5R | +0.01 / +0.05 | -0.00 / +0.05 | 2/5 ✗ | -0.04 | -0.11 | ✗  bb_k 2→1: -0.04R | 4 | 0.12R | 8, +0.06 (+0.37 / -0.47) | 117 / 31 of 183 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.05; max drawdown 28.5R |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 6 / 1 of 7 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 55 / 16 of 73 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 31 / 7 of 45 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 6 / 1 of 7 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 9 / 3 of 14 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **BACKTESTING** | 29 | 51.7 | -0.018 | 0.97 | 4.5R | +0.13 / -0.42 | +0.31 / -0.37 | 1/5 ✗ | -0.04 | -0.07 | ✗  time_stop_bars 40→32: -0.04R | 2 | 0.06R | 1, +0.31 (+0.31 / +0.00) | 129 / 3 of 133 | 0 | only 29 trades; avg -0.02R/trade (needs +0.10R); profit factor 0.97; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 8 | 25.0 | -0.149 | 0.73 | 2.4R | -0.04 / -0.47 | +0.00 / -0.15 | 0/5 ✗ | -0.19 | -0.23 | ✗  stop buffer_atr 0.2→0.24: -0.03R | 0 | 0.08R | 0, +0.00 (+0.00 / +0.00) | 404 / 151 of 664 | 0 | only 8 trades; avg -0.15R/trade (needs +0.10R); profit factor 0.73; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 12 | 41.7 | -0.396 | 0.36 | 6.9R | -0.51 / +0.16 | -0.19 / -0.50 | 0/5 ✗ | -0.39 | -0.69 | ✗  time_stop_bars 30→24: -0.49R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 393 / 141 of 666 | 0 | only 12 trades; avg -0.40R/trade (needs +0.10R); profit factor 0.36; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 3 | 0.0 | -1.186 | 0.0 | 3.6R | -1.19 / +0.00 | -1.26 / -1.15 | 0/5 ✗ | -1.22 | -1.28 | ✗  stop buffer_atr 0.2→0.16: -1.19R | 0 | 0.19R | 0, +0.00 (+0.00 / +0.00) | 55 / 16 of 73 | 0 | only 3 trades; avg -1.19R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 227 | 52.4 | +0.045 | 1.09 | 25.5R | +0.24 / -0.36 | +0.15 / -0.05 | 2/5 ✗ | -0.00 | -0.04 | ✗  stop atr 1.5→1.8: -0.01R | 5 | 0.06R | 1, -1.04 (-1.04 / +0.00) | 90 / 20 of 122 | 0 | avg +0.05R/trade (needs +0.10R); profit factor 1.09; max drawdown 25.5R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1051 | 34.8 | -0.003 | 1.0 | 57.0R | -0.01 / +0.01 | +0.06 / -0.08 | 2/5 ✗ | -0.07 | -0.12 | ✗  stop atr 2.0→1.6: -0.07R | 3 | 0.11R | 32, -0.27 (-0.33 / -0.15) | 106 / 29 of 273 | 0 | avg -0.00R/trade (needs +0.10R); profit factor 1.00; max drawdown 57.0R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 144 | 51.4 | -0.017 | 0.97 | 27.0R | -0.18 / +0.32 | -0.04 / +0.01 | 2/5 ✗ | -0.07 | -0.12 | ✗  stop atr 1.5→1.2: -0.07R | 3 | 0.11R | 0, +0.00 (+0.00 / +0.00) | 188 / 5 of 195 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 27.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1236 | 34.4 | -0.017 | 0.97 | 69.7R | -0.03 / +0.01 | +0.04 / -0.08 | 2/5 ✗ | -0.08 | -0.15 | ✗  stop atr 2.0→1.6: -0.08R | 3 | 0.11R | 39, -0.21 (-0.22 / -0.17) | 176 / 46 of 384 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 69.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 2689 | 32.5 | -0.022 | 0.96 | 158.0R | -0.04 / +0.02 | +0.01 / -0.06 | 2/5 ✗ | -0.07 | -0.11 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.07R | 19, -0.38 (-0.23 / -0.60) | 173 / 88 of 457 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 158.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2364 | 32.3 | -0.028 | 0.96 | 144.9R | -0.05 / +0.03 | -0.00 / -0.06 | 3/5 ✗ | -0.07 | -0.11 | ✗  stop atr 2.0→1.6: -0.05R | 4 | 0.07R | 14, -0.37 (-0.44 / -0.24) | 103 / 61 of 324 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.96; max drawdown 144.9R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2426 | 48.1 | -0.039 | 0.92 | 118.4R | -0.04 / -0.03 | -0.03 / -0.05 | 1/5 ✗ | -0.08 | -0.12 | ✗  adx_min 20→24: -0.05R | 2 | 0.07R | 14, -0.08 (-0.15 / +0.05) | 103 / 61 of 324 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.92; max drawdown 118.4R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1077 | 48.7 | -0.040 | 0.92 | 66.6R | -0.03 / -0.06 | +0.01 / -0.09 | 1/5 ✗ | -0.10 | -0.15 | ✗  stop atr 2.0→1.6: -0.10R | 2 | 0.11R | 32, -0.24 (-0.18 / -0.34) | 106 / 29 of 273 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.92; max drawdown 66.6R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 238 | 34.9 | -0.061 | 0.92 | 37.3R | +0.05 / -0.31 | -0.25 / +0.17 | 1/5 ✗ | -0.15 | -0.24 | ✗  time_stop_bars 30→36: -0.09R | 3 | 0.16R | 3, +2.10 (+2.06 / +2.18) | 77 / 169 of 255 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.92; max drawdown 37.3R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 976 | 48.3 | -0.065 | 0.88 | 99.3R | -0.02 / -0.17 | -0.02 / -0.12 | 1/5 ✗ | -0.10 | -0.14 | ✗  long_rsi_hi 65→52: -0.13R | 2 | 0.05R | 10, -0.42 (-0.35 / -1.10) | 553 / 159 of 851 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.88; max drawdown 99.3R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 73 | 46.6 | -0.075 | 0.86 | 12.2R | +0.04 / -0.26 | -0.11 / -0.04 | 3/5 ✗ | -0.11 | -0.14 | ✗  time_stop_bars 60→48: -0.07R | 1 | 0.04R | 0, +0.00 (+0.00 / +0.00) | 30 / 5 of 38 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.86; max drawdown 12.2R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 350 | 47.4 | -0.093 | 0.83 | 39.2R | -0.08 / -0.14 | -0.16 / -0.06 | 1/5 ✗ | -0.21 | -0.32 | ✗  stop atr 1.5→1.2: -0.23R | 1 | 0.21R | 9, -0.97 (-0.79 / -1.33) | 70 / 10 of 98 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.83; max drawdown 39.2R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1474 | 56.9 | -0.102 | 0.64 | 150.7R | -0.10 / -0.11 | -0.12 / -0.09 | 0/5 ✗ | -0.13 | -0.15 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.04R | 5, +0.09 (+0.01 / +0.13) | 616 / 4 of 815 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.64; max drawdown 150.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 280 | 44.3 | -0.103 | 0.81 | 41.7R | -0.12 / -0.07 | -0.16 / -0.04 | 0/5 ✗ | -0.16 | -0.22 | ✗  slow 21→17: -0.17R | 3 | 0.11R | 4, +0.36 (+0.88 / -1.18) | 110 / 8 of 128 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.81; max drawdown 41.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 5012 | 47.4 | -0.109 | 0.81 | 563.6R | -0.12 / -0.09 | -0.11 / -0.11 | 0/5 ✗ | -0.17 | -0.23 | ✗  stop atr 1.5→1.2: -0.13R | 1 | 0.11R | 37, +0.09 (+0.03 / +0.19) | 930 / 204 of 1455 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.81; max drawdown 563.6R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 402 | 48.3 | -0.110 | 0.81 | 51.4R | -0.11 / -0.10 | -0.12 / -0.09 | 1/5 ✗ | -0.20 | -0.29 | ✗  bb_n 20→16: -0.22R | 3 | 0.17R | 15, -0.09 (-0.38 / +0.48) | 89 / 26 of 158 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.81; max drawdown 51.4R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 5498 | 55.6 | -0.111 | 0.6 | 618.3R | -0.09 / -0.16 | -0.10 / -0.12 | 0/5 ✗ | -0.17 | -0.22 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.09R | 35, +0.00 (-0.03 / +0.13) | 866 / 10 of 1143 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.60; max drawdown 618.3R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 39 | 35.9 | -0.118 | 0.83 | 9.7R | +0.03 / -0.38 | -0.37 / +0.12 | 1/5 ✗ | -0.30 | -0.38 | ✗  time_stop_bars 30→24: -0.12R | 3 | 0.13R | 6, -0.69 (-0.69 / +0.00) | 85 / 29 of 130 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.83; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 649 | 31.7 | -0.143 | 0.82 | 121.7R | -0.17 / -0.10 | -0.20 / -0.09 | 1/5 ✗ | -0.23 | -0.32 | ✗  stop buffer_atr 0.2→0.16: -0.19R | 1 | 0.18R | 12, -0.36 (-0.73 / +0.74) | 377 / 907 of 1361 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.82; max drawdown 121.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 2846 | 47.5 | -0.144 | 0.76 | 420.2R | -0.12 / -0.20 | -0.12 / -0.17 | 1/5 ✗ | -0.24 | -0.32 | ✗  stop atr 1.5→1.2: -0.19R | 0 | 0.15R | 78, -0.24 (-0.31 / -0.11) | 648 / 183 of 1304 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 420.2R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 209 | 37.8 | -0.161 | 0.76 | 53.9R | -0.19 / -0.07 | +0.18 / -0.38 | 1/5 ✗ | -0.20 | -0.25 | ✗  depth 0.985→1.182: -0.25R | 1 | 0.09R | 4, +0.53 (+0.41 / +0.88) | 61 / 3 of 74 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.76; max drawdown 53.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2230 | 49.2 | -0.173 | 0.45 | 387.4R | -0.15 / -0.22 | -0.19 / -0.16 | 0/5 ✗ | -0.26 | -0.35 | ✗  stop atr 2.0→1.6: -0.21R | 0 | 0.14R | 40, -0.21 (-0.09 / -0.46) | 883 / 38 of 1088 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.45; max drawdown 387.4R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 258 | 47.3 | -0.173 | 0.71 | 47.1R | -0.18 / -0.15 | -0.14 / -0.22 | 0/5 ✗ | -0.23 | -0.29 | ✗  vol_x 1.2→1.44: -0.34R | 2 | 0.14R | 3, +0.10 (-0.41 / +1.11) | 68 / 148 of 225 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.71; max drawdown 47.1R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 268 | 41.0 | -0.173 | 0.7 | 49.9R | -0.12 / -0.33 | -0.21 / -0.14 | 1/5 ✗ | -0.25 | -0.33 | ✗  fast 9→11: -0.28R | 0 | 0.15R | 9, -0.66 (+0.32 / -1.15) | 81 / 19 of 117 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.70; max drawdown 49.9R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 130 | 46.9 | -0.190 | 0.66 | 25.9R | -0.18 / -0.22 | -0.07 / -0.29 | 1/5 ✗ | -0.23 | -0.31 | ✗  adx_min 20→24: -0.33R | 1 | 0.12R | 4, -0.57 (-1.16 / +0.01) | 43 / 4 of 56 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.66; max drawdown 25.9R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 74 | 35.1 | -0.193 | 0.72 | 21.4R | -0.29 / +0.03 | -0.10 / -0.26 | 1/5 ✗ | -0.24 | -0.35 | ✗  depth 0.985→1.182: -0.39R | 0 | 0.13R | 6, -0.30 (+1.30 / -0.62) | 25 / 2 of 33 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.72; max drawdown 21.4R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 232 | 46.6 | -0.206 | 0.67 | 57.3R | -0.13 / -0.45 | -0.29 / -0.12 | 0/5 ✗ | -0.30 | -0.37 | ✗  stop atr 1.5→1.2: -0.26R | 1 | 0.17R | 6, -0.93 (-0.88 / -1.21) | 139 / 8 of 157 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.67; max drawdown 57.3R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 2479 | 45.9 | -0.214 | 0.67 | 531.4R | -0.20 / -0.25 | -0.19 / -0.23 | 0/5 ✗ | -0.34 | -0.48 | ✗  stop atr 1.5→1.2: -0.28R | 0 | 0.23R | 130, -0.30 (-0.24 / -0.40) | 1067 / 136 of 1896 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.67; max drawdown 531.4R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 226 | 43.8 | -0.226 | 0.62 | 56.2R | -0.23 / -0.21 | -0.26 / -0.20 | 0/5 ✗ | -0.28 | -0.33 | ✗  st_n 10→12: -0.26R | 2 | 0.08R | 3, +0.93 (+1.27 / +0.24) | 41 / 1 of 51 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.62; max drawdown 56.2R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1215 | 31.7 | -0.274 | 0.65 | 344.1R | -0.30 / -0.22 | -0.21 / -0.33 | 0/5 ✗ | -0.39 | -0.49 | ✗  stop atr 1.5→1.2: -0.32R | 0 | 0.18R | 24, +0.12 (+0.61 / -0.85) | 471 / 22 of 579 | 0 | avg -0.27R/trade (needs +0.10R); profit factor 0.65; max drawdown 344.1R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1023 | 29.8 | -0.286 | 0.63 | 294.1R | -0.31 / -0.23 | -0.24 / -0.32 | 0/5 ✗ | -0.35 | -0.42 | ✗  rsi_n 14→17: -0.37R | 1 | 0.13R | 4, +0.10 (+1.29 / -1.09) | 598 / 3 of 636 | 0 | avg -0.29R/trade (needs +0.10R); profit factor 0.63; max drawdown 294.1R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 1706 | 37.3 | -0.288 | 0.26 | 491.2R | -0.28 / -0.31 | -0.32 / -0.26 | 0/5 ✗ | -0.43 | -0.58 | ✗  stop atr 2.0→1.6: -0.35R | 0 | 0.25R | 82, -0.36 (-0.42 / -0.26) | 983 / 45 of 1146 | 0 | avg -0.29R/trade (needs +0.10R); profit factor 0.26; max drawdown 491.2R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 455 | 41.5 | -0.336 | 0.53 | 159.3R | -0.35 / -0.31 | -0.20 / -0.41 | 0/5 ✗ | -0.46 | -0.58 | ✗  stop atr 1.5→1.2: -0.37R | 0 | 0.27R | 26, -0.68 (-0.78 / -0.34) | 70 / 22 of 138 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.34R/trade (needs +0.10R); profit factor 0.53; max drawdown 159.3R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 495 | 26.1 | -0.395 | 0.57 | 197.5R | -0.41 / -0.35 | -0.47 / -0.32 | 0/5 ✗ | -0.54 | -0.64 | ✗  n 20→24: -0.45R | 1 | 0.28R | 21, -0.54 (-0.50 / -0.66) | 395 / 887 of 1419 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.39R/trade (needs +0.10R); profit factor 0.57; max drawdown 197.5R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 449 | 40.3 | -0.416 | 0.44 | 187.0R | -0.38 / -0.52 | -0.40 / -0.42 | 0/5 ✗ | -0.60 | -0.80 | ✗  stop atr 1.0→0.8: -0.48R | 0 | 0.35R | 25, -0.46 (-0.48 / -0.29) | 81 / 214 of 325 | 0 | not cost-viable: fees + slippage 0.35R per trade (stop must be ≥ 4x the round-trip cost); avg -0.42R/trade (needs +0.10R); profit factor 0.44; max drawdown 187.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 274 | 39.1 | -0.439 | 0.4 | 120.4R | -0.42 / -0.48 | -0.38 / -0.51 | 0/5 ✗ | -0.56 | -0.68 | ✗  long_rsi_max 45→36: -0.52R | 1 | 0.24R | 10, -0.67 (-0.59 / -1.34) | 89 / 180 of 288 | 0 | avg -0.44R/trade (needs +0.10R); profit factor 0.40; max drawdown 120.4R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 89 | 19.1 | -0.472 | 0.5 | 46.0R | -0.43 / -0.54 | -0.56 / -0.37 | 1/5 ✗ | -0.60 | -0.72 | ✗  time_stop_bars 30→36: -0.49R | 1 | 0.22R | 3, +1.32 (+1.32 / +0.00) | 33 / 82 of 122 | 0 | avg -0.47R/trade (needs +0.10R); profit factor 0.50; max drawdown 46.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 231 | 33.3 | -0.593 | 0.33 | 138.7R | -0.64 / -0.53 | -0.53 / -1.10 | 0/5 ✗ | -0.89 | -1.21 | ✗  stop atr 1.5→1.2: -0.80R | 0 | 0.44R | 55, -0.65 (-0.44 / -1.07) | 163 / 29 of 252 | 0 | not cost-viable: fees + slippage 0.44R per trade (stop must be ≥ 4x the round-trip cost); avg -0.59R/trade (needs +0.10R); profit factor 0.33; max drawdown 138.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 384 | 33.1 | -0.817 | 0.27 | 313.7R | -0.81 / -0.83 | -0.66 / -2.09 | 0/5 ✗ | -1.34 | -1.84 | ✗  stop atr 1.0→0.8: -1.09R | 0 | 0.78R | 97, -0.81 (-0.65 / -1.63) | 201 / 508 of 819 | 0 | not cost-viable: fees + slippage 0.78R per trade (stop must be ≥ 4x the round-trip cost); avg -0.82R/trade (needs +0.10R); profit factor 0.27; max drawdown 313.7R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **28** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 136 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.38** (Bonferroni: family-wise false-winner rate 0.05 over 136 trials; with 1 trial it would be 1.65).

**Research run duration:** 8.6 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 24 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (114.1 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 32 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

3 of 56 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT-S4 v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 10.83 | 17.0R | 504 d (15%) | passes every gate |
| donchian_breakout-VEXIT v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 9.14 | 16.6R | 430 d (13%) | passes every gate |
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 7.38 | 14.4R | 529 d (16%) | passes every gate |

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (79% of 2,689 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (75% of 1,236 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 968 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,364 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,051 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 853 trades shared)

🧪 **Strategy lab:** 4 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 15m | 4 | +0.973 | +0.000 | +0.407 | +0.404 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 2 | +0.259 | +1.969 | -0.209 | +0.688 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 6 | +0.226 | -1.203 | -0.396 | +0.164 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.118 | -0.381 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.202 | -1.202 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 3 | -1.186 | +0.000 | -0.149 | -0.465 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 238 | -0.061 | -0.313 | -0.143 | -0.101 | no |
| S8-PDH-PDL-SWEEP | 30m | 89 | -0.472 | -0.542 | -0.395 | -0.349 | no |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): bb_squeeze_breakout@1.0 1h FAILED → BACKTESTING
- **Not tested (IDEA / RETIRED):** donchian_breakout-VEXIT-VRVOL v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S5 v1.0 (RETIRED)

### 3c. Research layers (daily run)
Last run: **2026-10-06 00:56 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 8 | 2017-08-17 | 2026-10-05 | 20005 |  |
| 1h | 8 | 2017-08-17 | 2026-10-05 | 79956 |  |
| 30m | 8 | 2024-10-06 | 2026-10-06 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 8 | 2025-10-06 | 2026-10-06 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 8 | 2026-07-08 | 2026-10-06 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 853 (503) | false_breakout, trend_reversal | false_breakout 63%, no_displacement 32% | +0.48R | -0.37R | +0.31 / +0.25 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 968 (575) | false_breakout, trend_reversal | false_breakout 61% | +0.49R | -0.37R | +0.30 / +0.24 |
| donchian_breakout | 4h | BACKTESTING | 877 (388) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 66%, stop_too_tight 34%, no_displacement 33% | +0.33R | -0.37R | +0.21 / +0.16 |
| bb_squeeze_breakout | 1h | BACKTESTING | 678 (315) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, no_displacement 51%, stop_too_tight 37%, regime_mismatch 35% | +0.35R | -0.44R | +0.17 / +0.02 |
| bb_squeeze_breakout | 4h | FAILED | 227 (108) | false_breakout, stop_too_tight, structural_change | false_breakout 58%, stop_too_tight 43%, regime_mismatch 32% | +0.32R | -0.34R | +0.12 / +0.04 |
| donchian_breakout-VEXIT | 30m | FAILED | 1051 (685) | false_breakout | false_breakout 73% | +0.48R | -0.40R | +0.13 / -0.00 |
| macd_trend_cross | 1h | FAILED | 144 (70) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 91%, indicator_lag 43%, stop_too_tight 34% | +0.29R | -0.39R | +0.12 / -0.02 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1236 (811) | false_breakout | false_breakout 73% | +0.46R | -0.41R | +0.12 / -0.02 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2689 (1814) | false_breakout, regime_mismatch | false_breakout 64%, regime_mismatch 32% | +0.50R | -0.39R | +0.07 / -0.02 |
| donchian_breakout-VEXIT | 1h | FAILED | 2364 (1600) | false_breakout | false_breakout 63% | +0.51R | -0.39R | +0.06 / -0.03 |
| donchian_breakout | 1h | FAILED | 2426 (1258) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 32%, regime_mismatch 26% | +0.37R | -0.40R | +0.05 / -0.04 |
| donchian_breakout | 30m | FAILED | 1077 (553) | false_breakout, stop_too_tight | false_breakout 77%, stop_too_tight 34% | +0.30R | -0.41R | +0.09 / -0.04 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 238 (155) | stop_too_tight, sweep_continued, structural_change | sweep_continued 97%, range_market 56%, stop_too_tight 30% | +0.55R | -0.41R | +0.14 / -0.06 |
| trend_pullback | 4h | FAILED | 976 (505) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 38%, stop_too_tight 26% | +0.36R | -0.43R | +0.01 / -0.07 |
| supertrend_flip | 4h | FAILED | 73 (39) | stop_too_tight, indicator_lag, structural_change | regime_mismatch 64%, indicator_lag 38%, late_entry 26%, stop_too_tight 26% | +0.37R | -0.44R | -0.01 / -0.07 |
| ema_9_21_cross | 15m | FAILED | 350 (184) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 28% | +0.28R | -0.43R | +0.17 / -0.09 |
| rsi2_dip_buy | 4h | FAILED | 1474 (635) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 45% | +0.16R | -0.21R | -0.05 / -0.10 |
| ema_9_21_cross | 1h | FAILED | 280 (156) | regime_mismatch, indicator_lag | regime_mismatch 80%, indicator_lag 49% | +0.26R | -0.38R | +0.02 / -0.10 |
| trend_pullback | 1h | FAILED | 5012 (2638) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 77%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.43R | +0.03 / -0.11 |
| bb_squeeze_breakout | 30m | FAILED | 402 (208) | false_breakout, stop_too_tight | false_breakout 62%, stop_too_tight 38%, overextended_entry 30% | +0.27R | -0.43R | +0.11 / -0.11 |
| rsi2_dip_buy | 1h | FAILED | 5498 (2439) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 42% | +0.15R | -0.21R | +0.00 / -0.11 |
| S6-OB-FVG-noSMC | 15m | FAILED | 39 (25) | structural_change | stop_too_wide 88% | +0.28R | -0.46R | +0.04 / -0.12 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 649 (443) | range_market, stop_too_tight | range_market 46%, stop_too_tight 36% | +0.61R | -0.50R | +0.07 / -0.14 |
| trend_pullback | 30m | FAILED | 2846 (1493) | stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 31% | +0.27R | -0.43R | +0.05 / -0.14 |
| R4-CLUC | 30m | FAILED | 209 (130) | volatility_spike | - | +0.37R | -0.45R | -0.07 / -0.16 |
| rsi2_dip_buy | 30m | FAILED | 2230 (1133) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 29% | +0.15R | -0.19R | +0.00 / -0.17 |
| liquidity_sweep_reversal | 1h | FAILED | 258 (136) | stop_too_tight | stop_too_tight 52% | +0.30R | -0.48R | -0.01 / -0.17 |
| ema_9_21_cross | 30m | FAILED | 268 (158) | indicator_lag | indicator_lag 45%, low_relative_volume 37% | +0.27R | -0.36R | +0.01 / -0.17 |
| supertrend_flip | 30m | FAILED | 130 (69) | late_entry, stop_too_tight, indicator_lag | indicator_lag 41%, overextended_entry 35%, stop_too_tight 35%, late_entry 32% | +0.32R | -0.42R | -0.05 / -0.19 |
| R4-CLUC | 15m | FAILED | 74 (48) | none | - | +0.45R | -0.27R | -0.06 / -0.19 |
| macd_trend_cross | 30m | FAILED | 232 (124) | stop_too_tight, indicator_lag | no_displacement 85%, indicator_lag 48%, low_relative_volume 43%, stop_too_tight 28% | +0.28R | -0.44R | +0.00 / -0.21 |
| trend_pullback | 15m | FAILED | 2479 (1341) | wrong_session, stop_too_tight, indicator_lag | indicator_lag 51%, stop_too_tight 33% | +0.24R | -0.43R | +0.07 / -0.21 |
| supertrend_flip | 1h | FAILED | 226 (127) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 70%, stop_too_tight 35%, indicator_lag 33% | +0.39R | -0.36R | -0.14 / -0.23 |
| R4-BBRSI | 30m | FAILED | 1215 (830) | none | - | +0.43R | -0.45R | -0.04 / -0.27 |
| R4-BBRSI | 1h | FAILED | 1023 (718) | none | - | +0.45R | -0.47R | -0.13 / -0.29 |
| rsi2_dip_buy | 15m | FAILED | 1706 (1070) | trend_reversal, fees_slippage | fees_slippage 42% | +0.15R | -0.20R | +0.01 / -0.29 |
| bb_squeeze_breakout | 15m | FAILED | 455 (266) | stop_too_tight | stop_too_tight 42% | +0.28R | -0.47R | -0.03 / -0.34 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 495 (366) | stop_too_tight | stop_too_tight 33% | +0.59R | -0.49R | -0.05 / -0.40 |
| liquidity_sweep_reversal | 15m | FAILED | 449 (268) | stop_too_tight | stop_too_tight 39% | +0.36R | -0.46R | +0.00 / -0.42 |
| liquidity_sweep_reversal | 30m | FAILED | 274 (167) | stop_too_tight | stop_too_tight 39% | +0.41R | -0.48R | -0.17 / -0.44 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 89 (72) | stop_too_tight, sweep_continued | sweep_continued 96%, stop_too_tight 29% | +0.48R | -0.65R | -0.19 / -0.47 |
| ema_9_21_cross | 5m | FAILED | 231 (154) | stop_too_tight, indicator_lag | indicator_lag 54%, stop_too_tight 34% | +0.20R | -0.49R | +0.02 / -0.59 |
| liquidity_sweep_reversal | 5m | FAILED | 384 (257) | htf_conflict, stop_too_tight | wrong_session 73%, stop_too_tight 41% | +0.20R | -0.48R | +0.21 / -0.82 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 26 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `false_breakout` (systematic in 12 strategy/timeframe tests); `regime_mismatch` (systematic in 11 strategy/timeframe tests); `trend_reversal` (systematic in 7 strategy/timeframe tests); `volatility_spike` (systematic in 4 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- BTC up +1.6% (2026-10-04 13:00 → 2026-10-05 02:00 UTC): identifiable: at least one strategy had a valid signal before the move
- ENA up +9.5% (2026-10-05 05:00 → 2026-10-05 12:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 110.5 KB | - | - |
| `memory/cleanup_log.md` | 0.5 KB | - | - |
| `memory/coin_notes.md` | 14.3 KB | 14 | 2026-10-04 02:31 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 9.0 KB | 20 | 2026-10-06 07:21 UTC |
| `memory/experiments.md` | 54.7 KB | 23 | 2026-10-05 17:15 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 204.5 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 14.8 KB | - | - |
| `memory/missed_trades.md` | 32.2 KB | 44 | 2026-10-06 00:56 UTC |
| `memory/playbook.md` | 10.0 KB | - | - |
| `memory/research_sources.md` | 63.4 KB | 48 | 2026-10-05 00:57 UTC |
| `memory/smc_events.csv` | 867.4 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 18.4 KB | - | - |
| `memory/strategy_registry.csv` | 41.5 KB | - | - |
| `memory/trials.csv` | 10.6 KB | - | - |
| `memory/universe_log.md` | 19.2 KB | - | - |

**Reviews due** (review date passed; for the reviews): `missed_trades.md` LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00 (2026-10-02); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03); `missed_trades.md` SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells (2026-10-03); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03) … and 10 more
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG and SHORT = OKX futures fees + funding (always charged, never received). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*