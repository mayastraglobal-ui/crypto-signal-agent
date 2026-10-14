# Crypto Signal Report

**Updated:** 2026-10-14 08:39 Beijing time (2026-10-14 00:39 UTC) · data: Binance · 8 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 15.6 MB (GitHub) · large files of this run 6.2 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-14 00:39 UTC / 2026-10-14 08:39 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US CPI (Sep data) 2026-10-14 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.04% (limit 0.5%)
- All 8 coins passed every check on every timeframe.
- 58 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-14 00:38 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 1162 h since 2026-08-26 | -0.0031% | 1.31 | 0.77 | - |
| ETH | GOOD | okx | 1162 h since 2026-08-26 | +0.0069% | 1.74 | 0.71 | - |
| SOL | GOOD | okx | 1162 h since 2026-08-26 | +0.0100% | 2.44 | 0.74 | - |
| XRP | GOOD | okx | 1162 h since 2026-08-26 | -0.0033% | 3.05 | 0.46 | - |
| ZEC | GOOD | okx | 1162 h since 2026-08-26 | +0.0036% | 0.80 | 0.76 | - |
| SUI | GOOD | okx | 1162 h since 2026-08-26 | +0.0060% | 3.16 | 0.79 | - |
| BNB | GOOD | okx | 1162 h since 2026-08-26 | +0.0100% | 2.74 | 1.80 | - |
| UNI | GOOD | okx | 1162 h since 2026-08-26 | +0.0081% | 1.32 | 0.63 | - |

*Binance futures API: blocked from GitHub's servers (HTTP 451) - expected, not a problem. The main series (OKX) is complete; Binance research history comes from the data.binance.vision files.*

## 0b. Coins this run
- **Signal coins (6/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **XRP**, **ZEC**, **SUI**
- **Your coins only:** BTC, ETH, SOL, BNB, XRP, ZEC, SUI - another coin never gives a signal. Each must pass every rule (volume, spread and depth on OKX USDT perpetuals); a coin that failed joins again after 2 runs in a row.
- **Your coins out this run:** BNB
- **Research only** - backtested, never a signal: BNB, UNI

*Skipped by your exclusion lists:* NEAR, RLUSD, USD1, USDC (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 478 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ETH | 478 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| SOL | 322 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| XRP | 441 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| ZEC | 395 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| SUI | 180 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| BNB | 466 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| UNI | 317 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | down (LH/LL) | 83,850 / 82,972.7 | 0.08 | 0.71x | 1.32x | bull_reject |
| ETH | mixed (LH/HL) | 2,528.38 / 2,495.17 | 0.05 | 0.37x | 1.34x | bull_reject |
| SOL | mixed (LH/HL) | 108.27 / 105.63 | 0.47 | 0.34x | 1.22x | - |
| XRP | mixed (LH/HL) | 1.381 / 1.3492 | 0.27 | 0.47x | 1.21x | - |
| ZEC | up (HH/HL) | 1,230.39 / 1,174.8 | 0.29 | 0.23x | 1.14x | - |
| SUI | mixed (LH/HL) | 1.061 / 1.0321 | 0.40 | 0.20x | 0.95x | bull_reject |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 386 | 49% | 34% | 27% | 80% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | displacement_down | 300 | 46% | 27% | 17% | 77% | 46% | 29% | can't tell from chance | 0.09R |
| 4h | bull_engulf | 981 | 46% | 32% | 22% | 77% | 46% | 31% | can't tell from chance | 0.09R |
| 4h | bear_engulf | 1101 | 41% | 26% | 17% | 80% | 46% | 31% | worse than chance | 0.09R |
| 4h | bull_reject | 712 | 44% | 30% | 22% | 77% | 46% | 31% | can't tell from chance | 0.09R |
| 4h | bear_reject | 713 | 46% | 31% | 21% | 75% | 45% | 30% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 507 | 45% | 31% | 23% | 75% | 46% | 30% | can't tell from chance | 0.09R |
| 4h | smc_sweep_bear | 558 | 44% | 29% | 18% | 80% | 45% | 30% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 244 | 46% | 29% | 20% | 82% | 46% | 30% | can't tell from chance | 0.09R |
| 4h | smc_bos_down | 171 | 43% | 29% | 18% | 78% | 45% | 30% | can't tell from chance | 0.09R |
| 4h | smc_choch_up | 72 | 50% | 38% | 28% | 82% | 47% | 30% | can't tell from chance | 0.08R |
| 4h | smc_choch_down | 71 | 44% | 25% | 15% | 76% | 44% | 29% | can't tell from chance | 0.09R |
| 4h | smc_fvg_retrace_bull | 537 | 46% | 30% | 23% | 76% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bear | 539 | 45% | 29% | 18% | 77% | 45% | 29% | can't tell from chance | 0.08R |
| 1h | displacement_up | 488 | 47% | 34% | 28% | 75% | 45% | 31% | can't tell from chance | 0.18R |
| 1h | displacement_down | 367 | 37% | 25% | 16% | 80% | 38% | 25% | can't tell from chance | 0.18R |
| 1h | bull_engulf | 1366 | 43% | 30% | 22% | 75% | 45% | 31% | can't tell from chance | 0.20R |
| 1h | bear_engulf | 1511 | 38% | 24% | 17% | 79% | 38% | 24% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1079 | 44% | 31% | 23% | 75% | 45% | 31% | can't tell from chance | 0.19R |
| 1h | bear_reject | 1106 | 37% | 25% | 19% | 80% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_sweep_bull | 503 | 44% | 28% | 20% | 76% | 44% | 30% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bear | 521 | 38% | 25% | 17% | 79% | 37% | 24% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 322 | 45% | 34% | 28% | 78% | 45% | 31% | can't tell from chance | 0.17R |
| 1h | smc_bos_down | 226 | 43% | 33% | 24% | 77% | 39% | 24% | can't tell from chance | 0.22R |
| 1h | smc_choch_up | 87 | 46% | 31% | 28% | 80% | 45% | 31% | can't tell from chance | 0.21R |
| 1h | smc_choch_down | 84 | 42% | 31% | 21% | 74% | 39% | 24% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 733 | 46% | 32% | 23% | 74% | 44% | 31% | can't tell from chance | 0.19R |
| 1h | smc_fvg_retrace_bear | 637 | 39% | 27% | 21% | 77% | 38% | 24% | can't tell from chance | 0.21R |
| 30m | displacement_up | 405 | 36% | 27% | 21% | 79% | 42% | 28% | worse than chance | 0.24R |
| 30m | displacement_down | 355 | 44% | 26% | 21% | 81% | 37% | 24% | beats chance | 0.22R |
| 30m | bull_engulf | 1336 | 41% | 27% | 18% | 78% | 42% | 27% | can't tell from chance | 0.25R |
| 30m | bear_engulf | 1414 | 37% | 23% | 17% | 80% | 36% | 24% | can't tell from chance | 0.26R |
| 30m | bull_reject | 984 | 44% | 29% | 20% | 76% | 42% | 27% | can't tell from chance | 0.25R |
| 30m | bear_reject | 1198 | 37% | 24% | 18% | 79% | 37% | 24% | can't tell from chance | 0.25R |
| 30m | smc_sweep_bull | 543 | 39% | 27% | 20% | 76% | 43% | 27% | can't tell from chance | 0.24R |
| 30m | smc_sweep_bear | 481 | 40% | 26% | 18% | 80% | 36% | 22% | can't tell from chance | 0.25R |
| 30m | smc_bos_up | 319 | 36% | 27% | 23% | 78% | 41% | 27% | can't tell from chance | 0.24R |
| 30m | smc_bos_down | 210 | 35% | 24% | 18% | 84% | 38% | 25% | can't tell from chance | 0.25R |
| 30m | smc_choch_up | 78 | 33% | 21% | 14% | 88% | 43% | 27% | can't tell from chance | 0.30R |
| 30m | smc_choch_down | 80 | 39% | 24% | 21% | 80% | 36% | 22% | can't tell from chance | 0.23R |
| 30m | smc_fvg_retrace_bull | 783 | 39% | 25% | 17% | 80% | 41% | 27% | can't tell from chance | 0.26R |
| 30m | smc_fvg_retrace_bear | 680 | 37% | 24% | 18% | 80% | 36% | 23% | can't tell from chance | 0.26R |
| 15m | displacement_up | 337 | 31% | 22% | 16% | 90% | 35% | 24% | can't tell from chance | 0.36R |
| 15m | displacement_down | 349 | 38% | 29% | 22% | 81% | 35% | 24% | can't tell from chance | 0.34R |
| 15m | bull_engulf | 1333 | 34% | 23% | 15% | 80% | 34% | 23% | can't tell from chance | 0.39R |
| 15m | bear_engulf | 1349 | 34% | 24% | 17% | 78% | 34% | 23% | can't tell from chance | 0.40R |
| 15m | bull_reject | 1066 | 36% | 25% | 17% | 79% | 34% | 23% | can't tell from chance | 0.41R |
| 15m | bear_reject | 1233 | 34% | 22% | 16% | 79% | 35% | 24% | can't tell from chance | 0.38R |
| 15m | smc_sweep_bull | 492 | 33% | 24% | 15% | 80% | 35% | 24% | can't tell from chance | 0.35R |
| 15m | smc_sweep_bear | 418 | 34% | 23% | 16% | 80% | 36% | 24% | can't tell from chance | 0.35R |
| 15m | smc_bos_up | 207 | 28% | 19% | 15% | 88% | 35% | 23% | worse than chance | 0.46R |
| 15m | smc_bos_down | 287 | 34% | 26% | 20% | 82% | 35% | 24% | can't tell from chance | 0.37R |
| 15m | smc_choch_up | 80 | 24% | 14% | 5% | 96% | 34% | 24% | worse than chance | 0.48R |
| 15m | smc_choch_down | 77 | 38% | 30% | 21% | 81% | 31% | 20% | can't tell from chance | 0.38R |
| 15m | smc_fvg_retrace_bull | 903 | 33% | 24% | 17% | 80% | 34% | 23% | can't tell from chance | 0.40R |
| 15m | smc_fvg_retrace_bear | 814 | 33% | 23% | 16% | 81% | 35% | 23% | can't tell from chance | 0.38R |
| 5m | displacement_up | 909 | 26% | 19% | 15% | 86% | 26% | 17% | can't tell from chance | 0.70R |
| 5m | displacement_down | 950 | 24% | 19% | 14% | 86% | 28% | 20% | worse than chance | 0.64R |
| 5m | bull_engulf | 3468 | 26% | 16% | 11% | 84% | 26% | 17% | can't tell from chance | 0.71R |
| 5m | bear_engulf | 3343 | 27% | 20% | 14% | 82% | 27% | 19% | can't tell from chance | 0.75R |
| 5m | bull_reject | 2781 | 24% | 16% | 11% | 84% | 25% | 17% | can't tell from chance | 0.78R |
| 5m | bear_reject | 3075 | 27% | 20% | 13% | 83% | 27% | 19% | can't tell from chance | 0.73R |
| 5m | smc_sweep_bull | 972 | 26% | 17% | 13% | 84% | 27% | 18% | can't tell from chance | 0.60R |
| 5m | smc_sweep_bear | 936 | 28% | 21% | 13% | 83% | 29% | 20% | can't tell from chance | 0.63R |
| 5m | smc_bos_up | 642 | 23% | 15% | 11% | 88% | 25% | 16% | can't tell from chance | 0.83R |
| 5m | smc_bos_down | 763 | 26% | 19% | 15% | 85% | 27% | 19% | can't tell from chance | 0.67R |
| 5m | smc_choch_up | 163 | 29% | 21% | 19% | 84% | 26% | 16% | can't tell from chance | 0.78R |
| 5m | smc_choch_down | 162 | 27% | 19% | 13% | 87% | 29% | 20% | can't tell from chance | 0.72R |
| 5m | smc_fvg_retrace_bull | 2715 | 25% | 17% | 11% | 85% | 25% | 17% | can't tell from chance | 0.81R |
| 5m | smc_fvg_retrace_bear | 2651 | 25% | 18% | 12% | 84% | 26% | 18% | can't tell from chance | 0.78R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | WEAK_BULL (moderate) | TRANSITION (moderate) | UNCLEAR (weak) | WEAK_BEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H WEAK_BEAR)) |
| **ETH** | WEAK_BULL (weak) | TRANSITION (weak) | WEAK_BEAR (moderate) | HIGH_VOL_RANGE (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BEAR, 1H HIGH_VOL_RANGE)) |
| **SOL** | WEAK_BULL (moderate) | TRANSITION (weak) | TRANSITION (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H UNCLEAR)) |
| **XRP** | WEAK_BULL (moderate) | TRANSITION (weak) | WEAK_BEAR (moderate) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BEAR, 1H UNCLEAR)) |
| **ZEC** | WEAK_BULL (weak) | TRANSITION (moderate) | UNCLEAR (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H RANGE)) |
| **SUI** | UNCLEAR (weak) | TRANSITION (weak) | UNCLEAR (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H TRANSITION)) |
| **BNB** | WEAK_BULL (weak) | UNCLEAR (weak) | TRANSITION (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D UNCLEAR, 4H TRANSITION, 1H UNCLEAR)) |
| **UNI** | EXPANSION up (moderate) | TRANSITION (moderate) | TRANSITION (weak) | RANGE (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H RANGE)) |

**BTC evidence** (most coins follow BTC):
- **1W WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+2.1 ATR in 10 candles); ADX 27 = strong trend; candle size 0.71x normal, Bollinger width above 68% of the last 100 candles; volume 0.95x normal · against: swing structure mixed (neutral)
- **1D TRANSITION (moderate)** - for: close above EMA-fast above EMA-slow; swing structure down (LH/LL); ADX 30 = strong trend; candle size 1.01x normal, Bollinger width above 12% of the last 100 candles · against: EMA-fast flat (+0.8 ATR in 10 candles)
- **4H UNCLEAR (weak)** - for: candle size 1.01x normal, Bollinger width above 19% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.2 ATR in 10 candles); swing structure down (LH/LL); ADX 22 = in between (20-25); ADX 22 is close to a threshold; signals are mixed and trend strength is in between
- **1H WEAK_BEAR (weak)** - for: close below EMA-fast below EMA-slow; swing structure down (LH/LL) · against: EMA-fast flat (+0.1 ATR in 10 candles) (neutral); ADX 12 = weak trend / ranging; candle size 1.32x normal, Bollinger width above 33% of the last 100 candles (unusually wild for a trend); volume only 0.52x normal (weak participation)

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **Asia**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (BOS 29 candles ago) | sell-side (bullish idea) 4 candles ago | bull 83,255.01-83,394.01 | bear 83,500.00-84,352.00 | discount (22%) | swing high 83,850.00 (1.72 ATR) | swing low 82,972.74 (0.49 ATR) |
| **ETH** | down (BOS 5 candles ago) | buy-side (bearish idea) 21 candles ago | bull 2,501.62-2,506.17 | bear 2,542.50-2,579.88 | discount (8%) | swing high 2,528.38 (1.83 ATR) | swing low 2,495.17 (0.17 ATR) |
| **SOL** | up (BOS 0 candles ago) | sell-side (bullish idea) 5 candles ago | bull 106.89-107.10 | bear 111.39-113.40 | discount (45%) | swing high 108.27 (1.46 ATR) | swing low 105.63 (1.22 ATR) |
| **XRP** | up (CHOCH 41 candles ago) | sell-side (bullish idea) 14 candles ago | bull 1.3672-1.3695 | bear 1.4036-1.4214 | premium (53%) | swing high 1.3810 (1.39 ATR) | swing low 1.3492 (1.58 ATR) |
| **ZEC** | down (BOS 58 candles ago) | buy-side (bearish idea) 7 candles ago | bull 1,221.39-1,223.71 | bear 1,282.27-1,349.30 | premium (79%) | swing high 1,230.39 (0.63 ATR) | swing low 1,174.80 (2.35 ATR) |
| **SUI** | up (BOS 0 candles ago) | sell-side (bullish idea) 12 candles ago | bull 1.0484-1.0527 | bear 1.1264-1.1468 | premium (54%) | swing high 1.0610 (1.04 ATR) | swing low 1.0321 (1.2 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **SIDEWAYS**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 62 (Greed), yesterday 57  (extreme fear/greed = bigger, faster moves)

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
- **Event calendar (next 7 days):** US CPI (Sep data) 2026-10-14 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-10-13 01:02 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **PAPER_TRADING** | 814 | 41.2 | +0.253 | 1.48 | 19.8R | +0.25 / +0.25 | +0.28 / +0.21 | 5/5 | +0.22 | +0.20 | stable | 7 | 0.04R | 1, -1.07 (-1.07 / +0.00) | 72 / 44 of 208 | 0 |  |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 4h | **PAPER_TRADING** | 633 | 40.8 | +0.234 | 1.44 | 16.0R | +0.24 / +0.23 | +0.24 / +0.23 | 5/5 | +0.21 | +0.18 | stable | 6 | 0.04R | 0, +0.00 (+0.00 / +0.00) | 83 / 38 of 198 | 0 |  |
| donchian_breakout | 1.0 | 4h | **PAPER_TRADING** | 837 | 55.7 | +0.159 | 1.37 | 16.3R | +0.16 / +0.16 | +0.17 / +0.15 | 5/5 | +0.13 | +0.11 | stable | 6 | 0.04R | 1, -1.07 (-1.07 / +0.00) | 72 / 44 of 208 | 0 |  |
| PB-C-BREAKOUT-W20 | 1.0 | 5m | **BACKTESTING** | 1 | 100.0 | +0.351 | 99.0 | 0.0R | +0.35 / +0.00 | +0.35 / +0.00 | 0/5 ✗ | +0.30 | +0.25 | stable | 0 | 0.85R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | not cost-viable: fees + slippage 0.85R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; Monte Carlo 95% worst drawdown per 100 trades - - limit 17R; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 926 | 40.4 | +0.242 | 1.45 | 18.6R | +0.25 / +0.22 | +0.26 / +0.23 | 5/5 | +0.21 | +0.19 | stable | 7 | 0.04R | 1, -1.07 (-1.07 / +0.00) | 126 / 58 of 284 | 0 | Monte Carlo 95% worst drawdown per 100 trades 17.4R - limit 17R |
| P01-BREAKOUT-V3 🧪 lab | 1.0 | 4h | **BACKTESTING** | 333 | 40.5 | +0.209 | 1.39 | 12.9R | +0.21 / +0.21 | +0.34 / +0.01 | 4/5 | +0.18 | +0.16 | stable | 5 | 0.04R | 1, -1.07 (-1.07 / +0.00) | 31 / 41 of 95 | 0 | max drawdown 12.9R |
| P04-MACD-SUPERTREND-V3 🧪 lab | 1.0 | 4h | **BACKTESTING** | 150 | 38.7 | +0.195 | 1.33 | 10.7R | +0.30 / +0.00 | +0.30 / +0.04 | 3/5 | +0.17 | +0.15 | stable | 6 | 0.04R | 1, -1.15 (-1.15 / +0.00) | 38 / 15 of 61 | 0 | recovery factor 2.73 (net +29.2R / max drawdown 10.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 19.5R - limit 17R |
| TRD-H4-BREAKOUT-S3-FDISP 🧪 lab | 1.0 | 30m | **BACKTESTING** | 412 | 42.0 | +0.187 | 1.3 | 33.2R | +0.01 / +0.36 | +0.25 / +0.12 | 3/5 | +0.18 | +0.15 | stable | 6 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 8 / 5 of 52 | 0 | recovery factor 2.32 (net +76.9R / max drawdown 33.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 19.9R - limit 17R |
| P01-BREAKOUT-V1 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1058 | 39.6 | +0.186 | 1.34 | 24.3R | +0.21 / +0.13 | +0.26 / +0.09 | 5/5 | +0.15 | +0.13 | stable | 5 | 0.04R | 4, -0.98 (-0.98 / +0.00) | 191 / 122 of 396 | 0 | max drawdown 24.3R |
| P01-BREAKOUT-V4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 900 | 39.6 | +0.184 | 1.29 | 24.7R | +0.23 / +0.09 | +0.24 / +0.11 | 5/5 | +0.15 | +0.12 | stable | 5 | 0.04R | 4, -1.06 (-1.06 / +0.00) | 191 / 122 of 396 | 0 | max drawdown 24.7R |
| P02-EMA-PULLBACK-V4-S6-S6 🧪 lab | 1.0 | 4h | **BACKTESTING** | 403 | 36.5 | +0.159 | 1.24 | 21.1R | +0.15 / +0.17 | +0.21 / +0.10 | 4/5 | +0.12 | +0.07 | stable | 5 | 0.06R | 3, -0.33 (-0.33 / +0.00) | 859 / 295 of 1166 | 0 | Monte Carlo 95% worst drawdown per 100 trades 26.6R - limit 17R |
| TRD-H4-BREAKOUT-S3 🧪 lab | 1.0 | 1h | **BACKTESTING** | 939 | 39.8 | +0.152 | 1.25 | 31.6R | +0.09 / +0.27 | +0.20 / +0.09 | 4/5 | +0.13 | +0.11 | stable | 6 | 0.04R | 0, +0.00 (+0.00 / +0.00) | 9 / 3 of 139 | 0 | Monte Carlo 95% worst drawdown per 100 trades 22.0R - limit 17R |
| P02-EMA-PULLBACK-V4-S6 🧪 lab | 1.0 | 4h | **BACKTESTING** | 365 | 35.9 | +0.145 | 1.21 | 19.9R | +0.11 / +0.22 | +0.19 / +0.09 | 4/5 | +0.11 | +0.06 | stable | 4 | 0.06R | 2, -1.06 (-1.06 / +0.00) | 733 / 189 of 931 | 0 | recovery factor 2.66 (net +52.9R / max drawdown 19.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 27.1R - limit 17R |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 2 | 50.0 | +0.130 | 1.21 | 1.2R | +0.13 / +0.00 | -1.22 / +1.47 | 0/5 ✗ | +0.02 | +0.00 | stable | 0 | 0.27R | 0, +0.00 (+0.00 / +0.00) | 36 / 12 of 50 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; longest drawdown 59 days = 100% of the tested period (limit 60%); only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-S3-FDISP 🧪 lab | 1.0 | 1h | **BACKTESTING** | 679 | 38.7 | +0.126 | 1.2 | 29.6R | +0.05 / +0.27 | +0.15 / +0.10 | 4/5 | +0.10 | +0.09 | stable | 4 | 0.04R | 0, +0.00 (+0.00 / +0.00) | 6 / 1 of 77 | 0 | recovery factor 2.88 (net +85.3R / max drawdown 29.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 22.7R - limit 17R |
| TRD-H4-BREAKOUT | 1.0 | 1h | **BACKTESTING** | 821 | 38.2 | +0.109 | 1.17 | 46.2R | +0.03 / +0.26 | +0.17 / +0.04 | 4/5 | +0.09 | +0.07 | stable | 6 | 0.04R | 0, +0.00 (+0.00 / +0.00) | 6 / 2 of 92 | 0 | profit factor 1.17; recovery factor 1.93 (net +89.4R / max drawdown 46.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 22.9R - limit 17R |
| TRD-H4-BREAKOUT | 1.0 | 30m | **BACKTESTING** | 559 | 39.7 | +0.100 | 1.16 | 28.0R | -0.04 / +0.26 | +0.18 / +0.02 | 3/5 | +0.10 | +0.05 | stable | 6 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 9 / 8 of 75 | 0 | profit factor 1.16; recovery factor 2.00 (net +56.0R / max drawdown 28.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 24.5R - limit 17R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 297 | 35.0 | +0.096 | 1.14 | 19.3R | +0.13 / +0.03 | +0.09 / +0.10 | 2/5 ✗ | +0.06 | +0.01 | ✗  rsi_hi 65→52: -0.04R | 4 | 0.06R | 2, -1.06 (-1.06 / +0.00) | 704 / 184 of 893 | 0 | avg +0.10R/trade (needs +0.10R); profit factor 1.14; max drawdown 19.3R |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 29 | 48.3 | +0.074 | 1.14 | 6.8R | +0.51 / -0.54 | +0.72 / -0.45 | 1/5 ✗ | +0.01 | -0.05 | ✗  stop max_width_atr 3.0→2.4: -0.09R | 3 | 0.17R | 0, +0.00 (+0.00 / +0.00) | 403 / 140 of 593 | 0 | only 29 trades; avg +0.07R/trade (needs +0.10R); profit factor 1.14; not profitable in BOTH train and unseen test |
| P07-SQUEEZE-RETEST-V4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 722 | 34.5 | +0.062 | 1.09 | 37.6R | -0.06 / +0.33 | +0.10 / +0.01 | 3/5 | +0.03 | -0.01 | stable | 5 | 0.06R | 2, -1.06 (-1.06 / +0.00) | 195 / 69 of 300 | 0 | avg +0.06R/trade (needs +0.10R); profit factor 1.09; recovery factor 1.19 (net +44.8R / max drawdown 37.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 30.5R - limit 17R; not profitable in BOTH train and unseen test |
| P07-SQUEEZE-RETEST-V3 🧪 lab | 1.0 | 4h | **BACKTESTING** | 249 | 35.7 | +0.054 | 1.09 | 19.4R | +0.07 / +0.03 | +0.07 / +0.02 | 3/5 | +0.03 | -0.00 | stable | 4 | 0.05R | 1, -0.83 (-0.83 / +0.00) | 23 / 26 of 61 | 0 | avg +0.05R/trade (needs +0.10R); profit factor 1.09; recovery factor 0.69 (net +13.3R / max drawdown 19.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 26.3R - limit 17R |
| P05-RANGE-REVERSAL-V4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 362 | 35.6 | +0.050 | 1.07 | 25.3R | +0.01 / +0.16 | +0.13 / -0.02 | 4/5 | +0.00 | -0.04 | ✗  bb_k 2.0→2.4: -0.03R | 5 | 0.07R | 1, -1.06 (-1.06 / +0.00) | 340 / 0 of 377 | 0 | avg +0.05R/trade (needs +0.10R); profit factor 1.07; max drawdown 25.3R |
| P02-EMA-PULLBACK-V4-S6-FHTF 🧪 lab | 1.0 | 4h | **BACKTESTING** | 291 | 32.3 | +0.036 | 1.05 | 23.4R | -0.00 / +0.11 | +0.02 / +0.05 | 2/5 ✗ | +0.00 | -0.06 | ✗  fast 20→24: -0.02R | 3 | 0.06R | 2, -1.06 (-1.06 / +0.00) | 413 / 153 of 574 | 0 | avg +0.04R/trade (needs +0.10R); profit factor 1.05; recovery factor 0.45 (net +10.5R / max drawdown 23.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 33.7R - limit 17R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 1h | **BACKTESTING** | 2641 | 36.8 | +0.029 | 1.04 | 77.2R | +0.01 / +0.06 | +0.09 / -0.05 | 4/5 | +0.01 | -0.03 | ✗  stop atr 2.0→1.6: -0.01R | 4 | 0.05R | 12, -0.20 (-0.20 / +0.00) | 146 / 442 of 817 | 0 | avg +0.03R/trade (needs +0.10R); profit factor 1.04; recovery factor 0.98 (net +75.5R / max drawdown 77.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 28.9R - limit 17R |
| P07-SQUEEZE-RETEST-V1 🧪 lab | 1.0 | 4h | **BACKTESTING** | 794 | 35.1 | +0.023 | 1.04 | 35.2R | -0.05 / +0.17 | +0.05 / -0.02 | 2/5 ✗ | -0.01 | -0.05 | ✗  stop atr 1.5→1.2: -0.03R | 4 | 0.06R | 2, -0.95 (-0.95 / +0.00) | 195 / 69 of 300 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.04; recovery factor 0.52 (net +18.2R / max drawdown 35.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 27.8R - limit 17R; not profitable in BOTH train and unseen test |
| P07-SQUEEZE-RETEST-V2 🧪 lab | 1.0 | 1h | **BACKTESTING** | 1045 | 34.5 | +0.015 | 1.02 | 62.6R | +0.01 / +0.02 | +0.07 / -0.07 | 3/5 | -0.04 | -0.09 | ✗  stop atr 1.5→1.2: -0.04R | 4 | 0.10R | 4, +0.88 (+0.88 / +0.00) | 225 / 63 of 325 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.02; recovery factor 0.25 (net +15.4R / max drawdown 62.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 28.7R - limit 17R |
| bb_squeeze_breakout | 1.0 | 1h | **BACKTESTING** | 640 | 52.7 | +0.010 | 1.02 | 27.4R | +0.00 / +0.03 | -0.01 / +0.04 | 2/5 ✗ | -0.06 | -0.13 | ✗  bb_k 2→1: -0.04R | 3 | 0.12R | 3, -0.47 (-0.47 / +0.00) | 118 / 23 of 175 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.02; recovery factor 0.24 (net +6.5R / max drawdown 27.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 24.3R - limit 17R |
| TRD-H4-BREAKOUT-S3 🧪 lab | 1.0 | 30m | **BACKTESTING** | 837 | 36.2 | +0.005 | 1.01 | 76.3R | -0.10 / +0.19 | -0.02 / +0.03 | 3/5 | -0.00 | -0.03 | ✗  time_stop_bars 48→38: -0.00R | 2 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 13 / 9 of 105 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.01; recovery factor 0.06 (net +4.2R / max drawdown 76.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 29.5R - limit 17R; longest drawdown 1709 days = 94% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-S3-FDISP 🧪 lab | 1.0 | 15m | **BACKTESTING** | 708 | 37.0 | +0.005 | 1.01 | 37.1R | -0.05 / +0.06 | -0.04 / +0.06 | 2/5 ✗ | -0.03 | -0.05 | stable | 4 | 0.09R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 10 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.01; recovery factor 0.10 (net +3.6R / max drawdown 37.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 31.4R - limit 17R; longest drawdown 1368 days = 76% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V2 🧪 lab | 1.0 | 30m | **BACKTESTING** | 873 | 36.2 | +0.005 | 1.01 | 56.0R | -0.06 / +0.08 | +0.04 / -0.04 | 1/5 ✗ | -0.07 | -0.14 | ✗  stop atr 2.0→1.6: -0.02R | 3 | 0.13R | 9, +0.30 (+0.40 / -0.52) | 282 / 172 of 530 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.01; max drawdown 56.0R; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 8 / 3 of 11 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 8 / 3 of 11 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 6 / 5 of 12 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; recovery factor - (net +0.0R / max drawdown 0.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades - - limit 17R; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT-noCVD | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; recovery factor - (net +0.0R / max drawdown 0.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades - - limit 17R; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| P06-VWAP-REVERSION-V3 🧪 lab | 1.0 | 4h | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  dev 2.0→1.6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 7 | 28.6 | -0.001 | 1.0 | 3.6R | +0.89 / -1.19 | +1.65 / -1.24 | 0/5 ✗ | -0.14 | -0.27 | ✗  sweep_bars 8→6: -0.59R | 0 | 0.33R | 0, +0.00 (+0.00 / +0.00) | 6 / 5 of 12 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); only 7 trades; avg -0.00R/trade (needs +0.10R); profit factor 1.00; longest drawdown 626 days = 69% of the tested period (limit 60%); only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **BACKTESTING** | 29 | 51.7 | -0.018 | 0.97 | 4.5R | +0.13 / -0.42 | +0.31 / -0.37 | 1/5 ✗ | -0.04 | -0.07 | ✗  time_stop_bars 40→32: -0.04R | 2 | 0.06R | 1, +0.31 (+0.31 / +0.00) | 120 / 4 of 125 | 0 | only 29 trades; avg -0.02R/trade (needs +0.10R); profit factor 0.97; recovery factor -0.11 (net -0.5R / max drawdown 4.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 24.9R - limit 17R; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 13 | 46.2 | -0.023 | 0.95 | 2.8R | +0.07 / -0.10 | -0.20 / +0.13 | 0/5 ✗ | -0.20 | -0.27 | ✗  stop buffer_atr 0.2→0.24: -0.13R | 0 | 0.12R | 0, +0.00 (+0.00 / +0.00) | 420 / 160 of 657 | 0 | only 13 trades; avg -0.02R/trade (needs +0.10R); profit factor 0.95; only 7 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 21 | 38.1 | -0.138 | 0.83 | 7.9R | -0.11 / -0.16 | +1.42 / -0.76 | 2/5 ✗ | -0.96 | -0.79 | ✗  stop buffer_atr 0.2→0.24: -0.54R | 0 | 0.28R | 0, +0.00 (+0.00 / +0.00) | 25 / 10 of 39 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); only 21 trades; avg -0.14R/trade (needs +0.10R); profit factor 0.83; longest drawdown 1566 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 15m | **BACKTESTING** | 79 | 45.6 | -0.142 | 0.74 | 17.8R | -0.26 / -0.07 | -0.11 / -0.17 | 1/5 ✗ | -0.25 | -0.31 | ✗  stop buffer_atr 0.0→0.0: -0.14R | 2 | 0.17R | 2, -0.79 (-1.22 / -0.36) | 0 / 0 of 11 | 0 | only 79 trades; avg -0.14R/trade (needs +0.15R); profit factor 0.74; max drawdown 17.8R; longest drawdown 673 days = 95% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 5 | 40.0 | -0.172 | 0.79 | 2.6R | +1.21 / -0.52 | -0.30 / +0.03 | 0/5 ✗ | -0.37 | -0.49 | ✗  stop buffer_atr 0.2→0.24: -0.43R | 0 | 0.34R | 0, +0.00 (+0.00 / +0.00) | 40 / 80 of 128 | 0 | not cost-viable: fees + slippage 0.34R per trade (stop must be ≥ 4x the round-trip cost); only 5 trades; avg -0.17R/trade (needs +0.10R); profit factor 0.79; longest drawdown 318 days = 100% of the tested period (limit 60%); only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-GRADED | 1.0 | 5m | **BACKTESTING** | 64 | 40.6 | -0.264 | 0.58 | 16.9R | -0.22 / -0.47 | -0.27 / -0.26 | 1/5 ✗ | -0.43 | -0.43 | ✗  time_stop_bars 48→38: -0.29R | 1 | 0.18R | 1, +1.53 (+1.53 / +0.00) | 0 / 0 of 1 | 0 | only 64 trades; avg -0.26R/trade (needs +0.15R); profit factor 0.58; recovery factor -1.00 (net -16.9R / max drawdown 16.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 44.7R - limit 17R; longest drawdown 647 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| PB-A-APLUS | 1.0 | 5m | **BACKTESTING** | 52 | 36.5 | -0.323 | 0.52 | 16.8R | -0.29 / -0.50 | -0.22 / -0.38 | 0/5 ✗ | -0.39 | -0.46 | ✗  time_stop_bars 48→38: -0.35R | 1 | 0.18R | 1, +1.53 (+1.53 / +0.00) | 0 / 0 of 1 | 0 | only 52 trades; avg -0.32R/trade (needs +0.15R); profit factor 0.52; recovery factor -1.00 (net -16.8R / max drawdown 16.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 50.9R - limit 17R; longest drawdown 647 days = 100% of the tested period (limit 55%); only 9 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-GRADED | 1.0 | 5m | **BACKTESTING** | 8 | 37.5 | -0.336 | 0.49 | 4.4R | -0.22 / -1.15 | -0.60 / +0.47 | 0/5 ✗ | +0.32 | +0.21 | ✗  stop buffer_atr 0.0→0.0: -0.34R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 1 | 0 | only 8 trades; avg -0.34R/trade (needs +0.15R); profit factor 0.49; recovery factor -0.61 (net -2.7R / max drawdown 4.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 52.9R - limit 17R; longest drawdown 664 days = 100% of the tested period (limit 55%); only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-noCVD | 1.0 | 5m | **BACKTESTING** | 19 | 42.1 | -0.375 | 0.46 | 7.5R | +0.00 / -0.38 | -0.48 / -0.23 | 0/5 ✗ | -0.33 | -0.20 | ✗  stop max_width_atr 3.0→2.4: -0.38R | 0 | 0.53R | 3, -1.13 (-1.45 / -0.49) | 0 / 0 of 28 | 0 | not cost-viable: fees + slippage 0.53R per trade (stop must be ≥ 4x the round-trip cost); only 19 trades; avg -0.37R/trade (needs +0.15R); profit factor 0.46; longest drawdown 34 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| PB-A-PULLBACK | 1.0 | 5m | **BACKTESTING** | 12 | 41.7 | -0.497 | 0.28 | 6.7R | -0.44 / -1.10 | -0.62 / -0.46 | 0/5 ✗ | -0.69 | -0.44 | ✗  stop buffer_atr 0.0→0.0: -0.50R | 0 | 0.19R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 12 trades; avg -0.50R/trade (needs +0.15R); profit factor 0.28; recovery factor -0.89 (net -6.0R / max drawdown 6.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 64.1R - limit 17R; longest drawdown 468 days = 100% of the tested period (limit 55%); only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-LDN | 1.0 | 5m | **BACKTESTING** | 20 | 40.0 | -0.507 | 0.31 | 11.5R | -0.49 / -0.56 | -0.66 / -0.44 | 0/5 ✗ | -0.57 | -0.67 | ✗  stop buffer_atr 0.0→0.0: -0.51R | 1 | 0.25R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 20 trades; avg -0.51R/trade (needs +0.15R); profit factor 0.31; recovery factor -0.88 (net -10.1R / max drawdown 11.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 66.3R - limit 17R; longest drawdown 527 days = 100% of the tested period (limit 55%); only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-CVD | 1.0 | 5m | **BACKTESTING** | 10 | 40.0 | -0.520 | 0.26 | 6.0R | -0.46 / -1.10 | -1.16 / -0.36 | 0/5 ✗ | -0.69 | -0.44 | ✗  stop buffer_atr 0.0→0.0: -0.52R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 10 trades; avg -0.52R/trade (needs +0.15R); profit factor 0.26; recovery factor -0.87 (net -5.2R / max drawdown 6.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 65.1R - limit 17R; longest drawdown 468 days = 100% of the tested period (limit 55%); only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-APLUS | 1.0 | 5m | **BACKTESTING** | 1 | 0.0 | -0.641 | 0.0 | 0.6R | -0.64 / +0.00 | -0.64 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: -0.64R | 0 | 0.23R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 1 trades; avg -0.64R/trade (needs +0.15R); profit factor 0.00; recovery factor -1.00 (net -0.6R / max drawdown 0.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades - - limit 17R; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 9 | 11.1 | -0.653 | 0.38 | 5.9R | -0.24 / -1.17 | -1.22 / -0.37 | 0/5 ✗ | -0.67 | -0.75 | ✗  sweep_bars 20→24: -0.73R | 0 | 0.24R | 0, +0.00 (+0.00 / +0.00) | 49 / 14 of 65 | 0 | only 9 trades; avg -0.65R/trade (needs +0.10R); profit factor 0.38; longest drawdown 916 days = 100% of the tested period (limit 60%); only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 12 | 25.0 | -0.839 | 0.34 | 10.1R | -0.25 / -2.60 | -0.88 / -0.79 | 0/5 ✗ | -0.96 | -1.31 | ✗  stop buffer_atr 0.2→0.16: -3.30R | 0 | 0.34R | 0, +0.00 (+0.00 / +0.00) | 36 / 12 of 50 | 0 | not cost-viable: fees + slippage 0.34R per trade (stop must be ≥ 4x the round-trip cost); only 12 trades; avg -0.84R/trade (needs +0.10R); profit factor 0.34; max drawdown 10.1R; longest drawdown 1063 days = 100% of the tested period (limit 60%); only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| P06-VWAP-REVERSION-V1 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1 | 0.0 | -1.089 | 0.0 | 1.1R | +0.00 / -1.09 | +0.00 / -1.09 | 0/5 ✗ | -1.13 | -1.18 | ✗  stop atr 1.5→1.2: -1.11R | 0 | 0.11R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 1 trades; avg -1.09R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| P06-VWAP-REVERSION-V4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1 | 0.0 | -1.089 | 0.0 | 1.1R | +0.00 / -1.09 | +0.00 / -1.09 | 0/5 ✗ | -1.13 | -1.18 | ✗  stop atr 1.5→1.2: -1.11R | 0 | 0.11R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 1 trades; avg -1.09R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.208 | 0.0 | 1.2R | -1.21 / +0.00 | -1.21 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.2→0.16: -1.21R | 0 | 0.27R | 0, +0.00 (+0.00 / +0.00) | 49 / 14 of 65 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.21R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-FDISP 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 5 / 1 of 60 | 0 | waiting for the first daily research run (Layers B/C) |
| TRD-H4-BREAKOUT-FDISP 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 7 / 5 of 46 | 0 | waiting for the first daily research run (Layers B/C) |
| TRD-H4-BREAKOUT-FDISP 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 10 | 0 | waiting for the first daily research run (Layers B/C) |
| TRD-H4-BREAKOUT-FDISP 🧪 lab | 1.0 | 5m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 4 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 57 / 14 of 71 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 45 / 18 of 64 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.10 (-1.11 / -1.10) | 57 / 22 of 81 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 41 / 12 of 54 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 9 / 2 of 11 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 57 / 14 of 71 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 5 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 6 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 10 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 5 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 5 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V5 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 45 / 18 of 64 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.10 (-1.11 / -1.10) | 57 / 18 of 81 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.25 (-1.25 / +0.00) | 41 / 11 of 54 | 0 | waiting for the first daily research run (Layers B/C) |
| P11-MOMENTUM-V1 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 53, -0.13 (-0.24 / +0.13) | 0 / 27 of 165 | 0 | waiting for the first daily research run (Layers B/C) |
| P11-MOMENTUM-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 11, -0.25 (-0.45 / +0.30) | 0 / 7 of 42 | 0 | waiting for the first daily research run (Layers B/C) |
| P11-MOMENTUM-V3 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 26, -0.24 (-0.55 / +0.11) | 0 / 13 of 106 | 0 | waiting for the first daily research run (Layers B/C) |
| P11-MOMENTUM-V4 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 44, -0.72 (-0.56 / -1.06) | 0 / 70 of 214 | 0 | waiting for the first daily research run (Layers B/C) |
| P11-MOMENTUM-C 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 150, -0.11 (-0.20 / +0.09) | 0 / 81 of 774 | 0 | waiting for the first daily research run (Layers B/C) |
| P04-MACD-SUPERTREND-V4 🧪 lab | 1.0 | 4h | **FAILED** | 372 | 37.4 | +0.134 | 1.21 | 32.9R | +0.28 / -0.20 | +0.28 / -0.04 | 4/5 | +0.10 | +0.07 | stable | 5 | 0.04R | 1, -1.15 (-1.15 / +0.00) | 193 / 43 of 253 | 0 | recovery factor 1.52 (net +50.0R / max drawdown 32.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 25.8R - limit 17R; not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V1 🧪 lab | 1.0 | 4h | **FAILED** | 383 | 36.0 | +0.113 | 1.18 | 33.7R | +0.24 / -0.19 | +0.19 / +0.02 | 4/5 | +0.09 | +0.06 | stable | 5 | 0.04R | 1, -1.15 (-1.15 / +0.00) | 193 / 43 of 253 | 0 | profit factor 1.18; recovery factor 1.28 (net +43.3R / max drawdown 33.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 23.3R - limit 17R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 215 | 52.1 | +0.036 | 1.07 | 26.8R | +0.22 / -0.35 | +0.16 / -0.08 | 2/5 ✗ | -0.01 | -0.05 | ✗  stop atr 1.5→1.8: -0.00R | 4 | 0.07R | 0, +0.00 (+0.00 / +0.00) | 93 / 20 of 124 | 0 | avg +0.04R/trade (needs +0.10R); profit factor 1.07; recovery factor 0.29 (net +7.7R / max drawdown 26.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 21.9R - limit 17R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 1h | **FAILED** | 803 | 37.4 | +0.015 | 1.03 | 44.3R | +0.03 / -0.02 | -0.04 / +0.08 | 3/5 | -0.01 | -0.04 | ✗  stop atr 2.0→1.6: -0.01R | 3 | 0.04R | 0, +0.00 (+0.00 / +0.00) | 24 / 22 of 179 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.03; recovery factor 0.27 (net +12.0R / max drawdown 44.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 26.3R - limit 17R; longest drawdown 1994 days = 61% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 15m | **FAILED** | 1941 | 38.2 | -0.004 | 0.99 | 114.3R | -0.07 / +0.12 | -0.06 / +0.06 | 2/5 ✗ | -0.04 | -0.05 | ✗  stop atr 2.0→1.6: -0.02R | 2 | 0.09R | 0, +0.00 (+0.00 / +0.00) | 7 / 3 of 65 | 0 | avg -0.00R/trade (needs +0.10R); profit factor 0.99; recovery factor -0.06 (net -7.0R / max drawdown 114.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 29.4R - limit 17R; longest drawdown 1816 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 30m | **FAILED** | 1279 | 35.0 | -0.005 | 0.99 | 73.8R | -0.05 / +0.05 | +0.04 / -0.06 | 2/5 ✗ | -0.07 | -0.12 | ✗  stop atr 2.0→1.6: -0.03R | 2 | 0.10R | 9, -0.07 (+0.13 / -0.78) | 121 / 66 of 266 | 0 | avg -0.01R/trade (needs +0.12R); profit factor 0.99; recovery factor -0.09 (net -6.6R / max drawdown 73.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 30.1R - limit 17R; longest drawdown 1719 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 139 | 51.8 | -0.006 | 0.99 | 25.9R | -0.16 / +0.33 | -0.01 / -0.00 | 2/5 ✗ | -0.06 | -0.11 | ✗  stop atr 1.5→1.2: -0.07R | 3 | 0.11R | 0, +0.00 (+0.00 / +0.00) | 193 / 4 of 199 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; recovery factor -0.03 (net -0.8R / max drawdown 25.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 24.2R - limit 17R; longest drawdown 1862 days = 58% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 1h | **FAILED** | 1795 | 32.8 | -0.010 | 0.98 | 98.1R | -0.04 / +0.05 | +0.03 / -0.05 | 2/5 ✗ | -0.05 | -0.09 | ✗  stop atr 2.0→1.6: -0.03R | 3 | 0.07R | 5, +0.24 (+0.24 / +0.00) | 118 / 85 of 334 | 0 | avg -0.01R/trade (needs +0.12R); profit factor 0.98; recovery factor -0.18 (net -18.0R / max drawdown 98.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 30.3R - limit 17R; longest drawdown 2004 days = 62% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 1h | **FAILED** | 3703 | 37.6 | -0.018 | 0.97 | 178.5R | +0.00 / -0.07 | -0.03 / -0.00 | 1/5 ✗ | -0.05 | -0.08 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.05R | 16, -0.03 (+0.25 / -0.64) | 557 / 2322 of 3275 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; recovery factor -0.37 (net -65.1R / max drawdown 178.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 31.7R - limit 17R; longest drawdown 1861 days = 56% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2241 | 32.6 | -0.019 | 0.97 | 125.2R | -0.04 / +0.03 | +0.01 / -0.06 | 2/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.05R | 4 | 0.07R | 8, -0.04 (-0.04 / +0.00) | 95 / 84 of 330 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; recovery factor -0.35 (net -43.3R / max drawdown 125.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.1R - limit 17R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 2554 | 32.7 | -0.019 | 0.97 | 141.1R | -0.04 / +0.02 | +0.02 / -0.07 | 2/5 ✗ | -0.07 | -0.11 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.08R | 11, -0.35 (-0.35 / +0.00) | 172 / 111 of 464 | 0 | avg -0.02R/trade (needs +0.12R); profit factor 0.97; recovery factor -0.34 (net -48.6R / max drawdown 141.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 29.5R - limit 17R; longest drawdown 2004 days = 61% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-S3 🧪 lab | 1.0 | 15m | **FAILED** | 1455 | 34.9 | -0.022 | 0.97 | 83.2R | -0.07 / +0.07 | -0.05 / +0.01 | 1/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.06R | 3 | 0.08R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 24 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; recovery factor -0.39 (net -32.4R / max drawdown 83.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 31.9R - limit 17R; longest drawdown 1708 days = 94% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V2 🧪 lab | 1.0 | 1h | **FAILED** | 1849 | 32.3 | -0.023 | 0.96 | 100.0R | -0.06 / +0.06 | +0.02 / -0.08 | 1/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.04R | 2 | 0.07R | 6, -0.00 (-0.00 / +0.00) | 263 / 154 of 562 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 100.0R; not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V5 🧪 lab | 1.0 | 1h | **FAILED** | 3762 | 33.0 | -0.023 | 0.96 | 226.0R | -0.04 / +0.02 | -0.01 / -0.03 | 1/5 ✗ | -0.07 | -0.12 | ✗  stop atr 2.0→1.6: -0.05R | 2 | 0.08R | 26, -0.05 (+0.33 / -1.10) | 263 / 64 of 562 | 2 (-1.13) | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 226.0R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V1 🧪 lab | 1.0 | 4h | **FAILED** | 299 | 31.4 | -0.024 | 0.96 | 23.4R | +0.03 / -0.13 | -0.03 / -0.02 | 2/5 ✗ | -0.06 | -0.09 | ✗  rsi_hi 65→52: -0.39R | 2 | 0.06R | 2, -1.06 (-1.06 / +0.00) | 704 / 184 of 893 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 23.4R; not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V4 🧪 lab | 1.0 | 4h | **FAILED** | 250 | 31.2 | -0.025 | 0.97 | 47.3R | +0.05 / -0.15 | +0.04 / -0.07 | 2/5 ✗ | -0.06 | -0.11 | ✗  stop max_width_atr 3.0→2.4: -0.05R | 2 | 0.06R | 2, -1.04 (-1.04 / -1.03) | 459 / 212 of 679 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; recovery factor -0.13 (net -6.2R / max drawdown 47.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 36.3R - limit 17R; longest drawdown 2013 days = 62% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 5m | **FAILED** | 2179 | 38.1 | -0.027 | 0.96 | 178.6R | -0.05 / +0.04 | -0.05 / +0.00 | 2/5 ✗ | -0.03 | -0.10 | ✗  stop atr 2.0→2.4: -0.04R | 1 | 0.13R | 0, +0.00 (+0.00 / +0.00) | 23 / 2 of 88 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.96; recovery factor -0.33 (net -59.8R / max drawdown 178.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.3R - limit 17R; longest drawdown 679 days = 94% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 15m | **FAILED** | 983 | 35.3 | -0.032 | 0.95 | 64.8R | -0.09 / +0.03 | -0.05 / -0.01 | 1/5 ✗ | -0.06 | -0.11 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.09R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 16 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; recovery factor -0.49 (net -31.9R / max drawdown 64.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 33.8R - limit 17R; longest drawdown 1562 days = 87% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V2 🧪 lab | 1.0 | 1h | **FAILED** | 1199 | 33.4 | -0.033 | 0.95 | 92.4R | -0.05 / +0.01 | -0.08 / +0.03 | 2/5 ✗ | -0.07 | -0.12 | ✗  st_n 10→8: -0.04R | 3 | 0.08R | 2, +0.69 (+0.69 / +0.00) | 213 / 53 of 307 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; recovery factor -0.42 (net -39.2R / max drawdown 92.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 33.4R - limit 17R; longest drawdown 2003 days = 61% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 30m | **FAILED** | 1938 | 35.8 | -0.035 | 0.95 | 143.0R | -0.09 / +0.03 | -0.04 / -0.03 | 1/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.04R | 1 | 0.07R | 14, -0.19 (-0.05 / -1.03) | 113 / 499 of 774 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; recovery factor -0.47 (net -67.6R / max drawdown 143.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.9R - limit 17R; longest drawdown 1614 days = 89% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2301 | 48.2 | -0.036 | 0.93 | 110.5R | -0.04 / -0.03 | -0.02 / -0.06 | 1/5 ✗ | -0.08 | -0.12 | ✗  adx_min 20→24: -0.05R | 2 | 0.07R | 8, +0.17 (+0.17 / +0.00) | 95 / 84 of 330 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.93; recovery factor -0.75 (net -83.3R / max drawdown 110.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 25.4R - limit 17R; longest drawdown 3167 days = 96% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V2 🧪 lab | 1.0 | 30m | **FAILED** | 1450 | 34.8 | -0.036 | 0.95 | 115.8R | -0.08 / +0.07 | -0.03 / -0.04 | 2/5 ✗ | -0.11 | -0.18 | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.12R | 7, -0.19 (-0.19 / +0.00) | 236 / 89 of 368 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.95; recovery factor -0.45 (net -52.1R / max drawdown 115.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.9R - limit 17R; longest drawdown 1797 days = 99% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-S3 🧪 lab | 1.0 | 5m | **FAILED** | 1611 | 37.4 | -0.044 | 0.94 | 86.8R | -0.05 / -0.02 | -0.00 / -0.09 | 1/5 ✗ | -0.12 | -0.18 | ✗  stop atr 2.0→1.6: -0.06R | 3 | 0.13R | 0, +0.00 (+0.00 / +0.00) | 3 / 0 of 23 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.94; recovery factor -0.81 (net -70.3R / max drawdown 86.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 34.2R - limit 17R; longest drawdown 679 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P07-SQUEEZE-RETEST-V5 🧪 lab | 1.0 | 1h | **FAILED** | 2496 | 32.5 | -0.046 | 0.93 | 209.8R | -0.04 / -0.05 | -0.04 / -0.05 | 1/5 ✗ | -0.11 | -0.17 | ✗  stop atr 1.5→1.2: -0.10R | 1 | 0.11R | 11, +0.30 (+0.40 / -0.14) | 225 / 25 of 325 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.93; recovery factor -0.55 (net -114.9R / max drawdown 209.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.1R - limit 17R; longest drawdown 2057 days = 62% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 30m | **FAILED** | 1051 | 35.8 | -0.049 | 0.93 | 109.1R | -0.11 / +0.07 | -0.09 / -0.00 | 1/5 ✗ | -0.07 | -0.09 | ✗  entry offset_atr 0.25→0.3: -0.06R | 2 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 32 / 21 of 213 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.93; recovery factor -0.47 (net -51.6R / max drawdown 109.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 33.5R - limit 17R; longest drawdown 1808 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1777 | 33.8 | -0.051 | 0.92 | 144.8R | -0.10 / +0.01 | -0.03 / -0.07 | 1/5 ✗ | -0.12 | -0.19 | ✗  stop atr 2.0→1.6: -0.08R | 1 | 0.12R | 18, -0.16 (-0.08 / -0.78) | 185 / 97 of 399 | 0 | avg -0.05R/trade (needs +0.12R); profit factor 0.92; recovery factor -0.63 (net -91.4R / max drawdown 144.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 34.9R - limit 17R; longest drawdown 1719 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P08-SESSION-BREAKOUT-V3 🧪 lab | 1.0 | 1h | **FAILED** | 420 | 35.0 | -0.052 | 0.92 | 25.8R | -0.07 / -0.03 | -0.03 / -0.09 | 2/5 ✗ | -0.10 | -0.15 | ✗  stop atr 1.5→1.2: -0.13R | 3 | 0.10R | 1, -1.24 (-1.24 / +0.00) | 88 / 18 of 118 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; recovery factor -0.84 (net -21.6R / max drawdown 25.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 33.3R - limit 17R; longest drawdown 2000 days = 64% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1499 | 33.4 | -0.054 | 0.92 | 140.1R | -0.12 / +0.02 | -0.03 / -0.08 | 1/5 ✗ | -0.12 | -0.18 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.12R | 15, -0.08 (-0.04 / -0.52) | 119 / 80 of 300 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; recovery factor -0.57 (net -80.4R / max drawdown 140.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.8R - limit 17R; longest drawdown 1722 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V2 🧪 lab | 1.0 | 15m | **FAILED** | 1330 | 34.4 | -0.057 | 0.91 | 116.0R | -0.10 / -0.01 | -0.06 / -0.05 | 1/5 ✗ | -0.15 | -0.26 | ✗  stop atr 2.0→1.6: -0.10R | 2 | 0.18R | 14, -0.19 (-0.09 / -0.81) | 328 / 153 of 517 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 116.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 229 | 35.4 | -0.058 | 0.92 | 35.9R | +0.04 / -0.28 | -0.23 / +0.16 | 1/5 ✗ | -0.14 | -0.24 | ✗  time_stop_bars 30→36: -0.08R | 3 | 0.16R | 1, +2.18 (+2.18 / +0.00) | 77 / 168 of 255 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.92; max drawdown 35.9R; longest drawdown 2498 days = 82% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1552 | 48.2 | -0.065 | 0.88 | 132.7R | -0.09 / -0.03 | -0.06 / -0.07 | 0/5 ✗ | -0.13 | -0.20 | ✗  stop atr 2.0→1.6: -0.10R | 1 | 0.11R | 15, -0.21 (-0.19 / -0.52) | 119 / 80 of 300 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.88; recovery factor -0.75 (net -100.1R / max drawdown 132.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 28.9R - limit 17R; longest drawdown 1722 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 5m | **FAILED** | 1363 | 36.6 | -0.068 | 0.9 | 111.1R | -0.08 / -0.02 | -0.01 / -0.13 | 2/5 ✗ | -0.15 | -0.19 | ✗  stop atr 2.0→1.6: -0.09R | 3 | 0.13R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 12 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.90; recovery factor -0.84 (net -92.9R / max drawdown 111.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 35.0R - limit 17R; longest drawdown 713 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 934 | 48.1 | -0.073 | 0.87 | 103.8R | -0.02 / -0.18 | -0.01 / -0.15 | 1/5 ✗ | -0.11 | -0.14 | ✗  long_rsi_hi 65→52: -0.15R | 1 | 0.05R | 8, -0.27 (-0.27 / +0.00) | 563 / 160 of 868 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; recovery factor -0.65 (net -67.7R / max drawdown 103.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 28.9R - limit 17R; longest drawdown 1978 days = 60% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 70 | 45.7 | -0.076 | 0.86 | 10.9R | +0.08 / -0.29 | -0.13 / +0.00 | 4/5 ✗ | -0.12 | -0.14 | ✗  time_stop_bars 60→48: -0.07R | 1 | 0.04R | 1, -1.14 (-1.14 / +0.00) | 29 / 6 of 38 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.86; recovery factor -0.49 (net -5.3R / max drawdown 10.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 29.2R - limit 17R; not profitable in BOTH train and unseen test |
| P08-SESSION-BREAKOUT-V1 🧪 lab | 1.0 | 1h | **FAILED** | 1210 | 35.0 | -0.078 | 0.88 | 129.6R | -0.08 / -0.07 | -0.10 / -0.06 | 1/5 ✗ | -0.13 | -0.19 | ✗  stop atr 1.5→1.2: -0.12R | 2 | 0.10R | 2, +0.59 (+0.59 / +0.00) | 329 / 73 of 450 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.88; recovery factor -0.73 (net -94.8R / max drawdown 129.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 35.1R - limit 17R; longest drawdown 3138 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V2 🧪 lab | 1.0 | 15m | **FAILED** | 2287 | 34.1 | -0.079 | 0.89 | 216.7R | -0.11 / -0.01 | -0.13 / -0.02 | 1/5 ✗ | -0.17 | -0.27 | ✗  stop atr 2.0→1.6: -0.15R | 0 | 0.17R | 13, -0.17 (+0.00 / -1.12) | 253 / 81 of 355 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.89; recovery factor -0.83 (net -180.9R / max drawdown 216.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 38.4R - limit 17R; longest drawdown 1829 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P08-SESSION-BREAKOUT-V4 🧪 lab | 1.0 | 1h | **FAILED** | 1164 | 32.9 | -0.081 | 0.89 | 142.3R | -0.09 / -0.06 | -0.10 / -0.06 | 2/5 ✗ | -0.14 | -0.19 | ✗  stop atr 1.5→1.2: -0.11R | 2 | 0.10R | 2, +0.49 (+0.49 / +0.00) | 329 / 73 of 450 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.89; recovery factor -0.67 (net -94.6R / max drawdown 142.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 39.1R - limit 17R; longest drawdown 3168 days = 96% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V1 🧪 lab | 1.0 | 4h | **FAILED** | 253 | 34.8 | -0.083 | 0.88 | 41.5R | -0.07 / -0.10 | -0.18 / -0.01 | 2/5 ✗ | -0.11 | -0.15 | ✗  stop max_width_atr 3.0→2.4: -0.12R | 2 | 0.06R | 2, -1.04 (-1.04 / -1.03) | 459 / 212 of 679 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.88; recovery factor -0.50 (net -20.9R / max drawdown 41.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 35.6R - limit 17R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 15m | **FAILED** | 3338 | 34.2 | -0.086 | 0.88 | 326.2R | -0.11 / -0.05 | -0.09 / -0.09 | 0/5 ✗ | -0.13 | -0.18 | ✗  stop atr 2.0→1.6: -0.11R | 1 | 0.10R | 25, -0.57 (-0.50 / -0.98) | 111 / 566 of 782 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.88; recovery factor -0.88 (net -286.4R / max drawdown 326.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 37.4R - limit 17R; longest drawdown 1562 days = 86% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 15m | **FAILED** | 7314 | 36.2 | -0.088 | 0.87 | 693.3R | -0.11 / -0.04 | -0.11 / -0.07 | 0/5 ✗ | -0.13 | -0.14 | ✗  stop atr 2.0→1.6: -0.09R | 0 | 0.10R | 39, -0.22 (-0.16 / -0.37) | 569 / 2366 of 3279 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.87; recovery factor -0.93 (net -641.8R / max drawdown 693.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 35.7R - limit 17R; longest drawdown 1827 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V2 🧪 lab | 1.0 | 1h | **FAILED** | 2388 | 34.5 | -0.089 | 0.87 | 215.2R | -0.08 / -0.11 | -0.10 / -0.07 | 1/5 ✗ | -0.14 | -0.21 | ✗  stop buffer_atr 0.2→0.16: -0.09R | 0 | 0.11R | 6, -0.94 (-0.92 / -1.08) | 669 / 151 of 947 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.87; recovery factor -0.99 (net -212.0R / max drawdown 215.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 37.4R - limit 17R; longest drawdown 3264 days = 99% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V2 🧪 lab | 1.0 | 1h | **FAILED** | 2302 | 31.1 | -0.090 | 0.86 | 236.6R | -0.09 / -0.10 | -0.11 / -0.07 | 0/5 ✗ | -0.15 | -0.21 | ✗  stop atr 1.5→1.2: -0.11R | 0 | 0.11R | 9, -0.66 (-0.72 / -0.44) | 1014 / 119 of 1244 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.86; max drawdown 236.6R; not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V5 🧪 lab | 1.0 | 30m | **FAILED** | 1938 | 32.9 | -0.095 | 0.86 | 207.3R | -0.11 / -0.07 | -0.11 / -0.08 | 1/5 ✗ | -0.19 | -0.26 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.15R | 39, -0.03 (+0.21 / -0.83) | 282 / 70 of 530 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.86; max drawdown 207.3R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 30m | **FAILED** | 4253 | 34.4 | -0.097 | 0.86 | 431.3R | -0.12 / -0.04 | -0.11 / -0.09 | 0/5 ✗ | -0.14 | -0.17 | ✗  stop atr 2.0→1.6: -0.12R | 1 | 0.07R | 27, -0.31 (-0.18 / -1.03) | 501 / 2246 of 3177 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.86; recovery factor -0.96 (net -413.5R / max drawdown 431.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 36.9R - limit 17R; longest drawdown 1815 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V5 🧪 lab | 1.0 | 1h | **FAILED** | 2387 | 31.7 | -0.100 | 0.86 | 273.4R | -0.12 / -0.06 | -0.14 / -0.06 | 1/5 ✗ | -0.15 | -0.19 | ✗  stop atr 2.0→1.6: -0.12R | 1 | 0.08R | 17, -0.09 (-0.09 / +0.00) | 213 / 7 of 307 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.86; recovery factor -0.87 (net -238.2R / max drawdown 273.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 38.2R - limit 17R; longest drawdown 2130 days = 64% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1422 | 56.8 | -0.105 | 0.64 | 148.9R | -0.10 / -0.12 | -0.12 / -0.09 | 0/5 ✗ | -0.13 | -0.16 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.05R | 11, -0.56 (-0.45 / -1.03) | 608 / 9 of 814 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.64; max drawdown 148.9R; longest drawdown 3281 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V5 🧪 lab | 1.0 | 30m | **FAILED** | 3360 | 32.9 | -0.106 | 0.85 | 417.3R | -0.15 / +0.00 | -0.16 / -0.06 | 1/5 ✗ | -0.19 | -0.27 | ✗  stop atr 2.0→1.6: -0.14R | 2 | 0.13R | 30, +0.25 (+0.42 / -1.26) | 236 / 26 of 368 | 1 (-1.31) | avg -0.11R/trade (needs +0.10R); profit factor 0.85; recovery factor -0.85 (net -356.4R / max drawdown 417.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 38.2R - limit 17R; longest drawdown 1794 days = 98% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 5m | **FAILED** | 6288 | 36.5 | -0.107 | 0.84 | 697.5R | -0.12 / -0.07 | -0.10 / -0.11 | 0/5 ✗ | -0.13 | -0.16 | ✗  stop atr 2.0→2.4: -0.12R | 0 | 0.15R | 40, -0.14 (+0.15 / -0.63) | 1404 / 6337 of 8453 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.84; recovery factor -0.97 (net -675.7R / max drawdown 697.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 37.8R - limit 17R; longest drawdown 724 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P07-SQUEEZE-RETEST-V2 🧪 lab | 1.0 | 30m | **FAILED** | 854 | 32.1 | -0.110 | 0.84 | 117.4R | -0.07 / -0.18 | -0.19 / -0.01 | 0/5 ✗ | -0.20 | -0.29 | ✗  stop atr 1.5→1.2: -0.16R | 2 | 0.16R | 9, -0.10 (+0.14 / -0.93) | 238 / 84 of 349 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.84; recovery factor -0.80 (net -94.0R / max drawdown 117.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 38.8R - limit 17R; longest drawdown 1719 days = 94% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V5 🧪 lab | 1.0 | 1h | **FAILED** | 4852 | 30.1 | -0.110 | 0.83 | 569.3R | -0.11 / -0.11 | -0.12 / -0.10 | 0/5 ✗ | -0.18 | -0.24 | ✗  stop atr 1.5→1.2: -0.14R | 0 | 0.12R | 24, -0.46 (-0.35 / -0.89) | 1014 / 29 of 1244 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.83; max drawdown 569.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 5262 | 55.5 | -0.114 | 0.59 | 605.8R | -0.09 / -0.17 | -0.10 / -0.13 | 0/5 ✗ | -0.17 | -0.23 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.10R | 24, -0.12 (+0.00 / -0.27) | 837 / 10 of 1120 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.59; max drawdown 605.8R; longest drawdown 3156 days = 95% of the tested period (limit 60%); loss clustering: 21 losses in a row as it happened, random orders stay at or below 13 in 95% of cases; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 608 | 32.7 | -0.115 | 0.85 | 101.3R | -0.15 / -0.06 | -0.16 / -0.07 | 1/5 ✗ | -0.20 | -0.29 | ✗  stop buffer_atr 0.2→0.16: -0.17R | 1 | 0.19R | 4, +0.82 (+0.68 / +1.25) | 362 / 900 of 1334 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.85; max drawdown 101.3R; longest drawdown 2713 days = 87% of the tested period (limit 60%); loss clustering: 21 losses in a row as it happened, random orders stay at or below 20 in 95% of cases; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 4793 | 46.8 | -0.120 | 0.79 | 587.6R | -0.13 / -0.11 | -0.11 / -0.13 | 0/5 ✗ | -0.18 | -0.24 | ✗  stop atr 1.5→1.2: -0.14R | 0 | 0.11R | 24, -0.19 (+0.20 / -0.98) | 975 / 181 of 1470 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.79; recovery factor -0.98 (net -576.3R / max drawdown 587.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 33.8R - limit 17R; longest drawdown 3090 days = 94% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 5m | **FAILED** | 3759 | 35.1 | -0.120 | 0.83 | 462.2R | -0.13 / -0.08 | -0.09 / -0.15 | 0/5 ✗ | -0.16 | -0.20 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.15R | 24, -0.44 (-0.33 / -0.96) | 325 / 1534 of 2049 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.83; recovery factor -0.98 (net -451.3R / max drawdown 462.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 41.2R - limit 17R; longest drawdown 726 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V5 🧪 lab | 1.0 | 1h | **FAILED** | 5109 | 33.6 | -0.122 | 0.83 | 638.9R | -0.12 / -0.12 | -0.14 / -0.10 | 0/5 ✗ | -0.18 | -0.26 | ✗  stop buffer_atr 0.2→0.16: -0.13R | 2 | 0.12R | 29, -0.19 (-0.04 / -1.18) | 669 / 39 of 947 | 2 (-1.19) | avg -0.12R/trade (needs +0.10R); profit factor 0.83; recovery factor -0.98 (net -623.5R / max drawdown 638.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 40.4R - limit 17R; longest drawdown 3056 days = 92% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P05-RANGE-REVERSAL-V3 🧪 lab | 1.0 | 4h | **FAILED** | 75 | 52.0 | -0.127 | 0.74 | 14.4R | -0.23 / +0.07 | -0.12 / -0.13 | 1/5 ✗ | -0.16 | -0.20 | ✗  rsi_lo 35→28: -0.31R | 2 | 0.06R | 1, -0.11 (-0.11 / +0.00) | 43 / 0 of 53 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.74; max drawdown 14.4R; longest drawdown 2574 days = 83% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 270 | 43.3 | -0.128 | 0.77 | 42.7R | -0.14 / -0.11 | -0.18 / -0.07 | 0/5 ✗ | -0.18 | -0.25 | ✗  slow 21→17: -0.19R | 2 | 0.11R | 2, -1.03 (-1.18 / -0.88) | 99 / 6 of 113 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.77; recovery factor -0.81 (net -34.5R / max drawdown 42.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.9R - limit 17R; longest drawdown 2361 days = 72% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P08-SESSION-BREAKOUT-V2 🧪 lab | 1.0 | 30m | **FAILED** | 707 | 35.6 | -0.128 | 0.82 | 107.4R | -0.18 / -0.06 | -0.13 / -0.13 | 1/5 ✗ | -0.23 | -0.31 | ✗  stop atr 1.5→1.2: -0.18R | 3 | 0.16R | 3, -0.04 (+0.52 / -1.16) | 193 / 65 of 280 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.82; recovery factor -0.84 (net -90.5R / max drawdown 107.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 39.0R - limit 17R; longest drawdown 1779 days = 98% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| PB-B-SWEEP-LIMIT | 1.0 | 5m | **FAILED** | 215 | 39.1 | -0.129 | 0.73 | 33.8R | -0.17 / +0.04 | -0.18 / -0.08 | 1/5 ✗ | -0.28 | -0.25 | ✗  stop max_width_atr 3.0→3.6: -0.13R | 3 | 0.19R | 2, -0.82 (-1.22 / -0.41) | 0 / 0 of 28 | 0 | avg -0.13R/trade (needs +0.15R); profit factor 0.73; max drawdown 33.8R; longest drawdown 684 days = 96% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V5 🧪 lab | 1.0 | 15m | **FAILED** | 5024 | 32.9 | -0.135 | 0.82 | 715.3R | -0.17 / -0.07 | -0.19 / -0.08 | 1/5 ✗ | -0.24 | -0.35 | ✗  stop atr 2.0→1.6: -0.19R | 0 | 0.19R | 39, +0.34 (+0.52 / -0.64) | 253 / 41 of 355 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.82; recovery factor -0.95 (net -676.7R / max drawdown 715.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 42.0R - limit 17R; longest drawdown 1829 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V2 🧪 lab | 1.0 | 30m | **FAILED** | 1692 | 30.3 | -0.136 | 0.8 | 236.7R | -0.14 / -0.13 | -0.12 / -0.15 | 0/5 ✗ | -0.24 | -0.34 | ✗  rsi_hi 65→52: -0.30R | 0 | 0.19R | 19, -0.38 (-0.31 / -0.79) | 915 / 205 of 1245 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.80; max drawdown 236.7R; not profitable in BOTH train and unseen test |
| P05-RANGE-REVERSAL-V1 🧪 lab | 1.0 | 4h | **FAILED** | 385 | 48.6 | -0.136 | 0.74 | 57.6R | -0.14 / -0.12 | -0.06 / -0.20 | 0/5 ✗ | -0.18 | -0.23 | ✗  bb_k 2.0→2.4: -0.15R | 1 | 0.07R | 1, -0.11 (-0.11 / +0.00) | 340 / 0 of 377 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.74; max drawdown 57.6R; longest drawdown 3249 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 5m | **FAILED** | 183 | 36.6 | -0.137 | 0.72 | 29.9R | -0.17 / -0.00 | -0.19 / -0.08 | 1/5 ✗ | -0.24 | -0.15 | ✗  stop max_width_atr 3.0→3.6: -0.14R | 2 | 0.18R | 2, -0.82 (-1.22 / -0.41) | 0 / 0 of 23 | 0 | avg -0.14R/trade (needs +0.15R); profit factor 0.72; max drawdown 29.9R; longest drawdown 684 days = 96% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V2 🧪 lab | 1.0 | 30m | **FAILED** | 2812 | 34.6 | -0.143 | 0.8 | 414.7R | -0.17 / -0.09 | -0.18 / -0.11 | 0/5 ✗ | -0.25 | -0.33 | ✗  stop max_width_atr 3.0→2.4: -0.15R | 0 | 0.18R | 15, -0.76 (-0.59 / -1.22) | 697 / 228 of 1034 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.80; recovery factor -0.97 (net -403.5R / max drawdown 414.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 40.4R - limit 17R; longest drawdown 1825 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V3 🧪 lab | 1.0 | 4h | **FAILED** | 87 | 31.0 | -0.145 | 0.8 | 16.1R | -0.14 / -0.16 | -0.44 / +0.09 | 1/5 ✗ | -0.18 | -0.23 | ✗  stop max_width_atr 3.0→2.4: -0.21R | 2 | 0.05R | 1, -1.04 (-1.04 / +0.00) | 95 / 74 of 172 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.80; recovery factor -0.78 (net -12.6R / max drawdown 16.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 40.8R - limit 17R; longest drawdown 2120 days = 69% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 95 | 33.7 | -0.147 | 0.77 | 21.4R | -0.25 / +0.01 | -0.19 / -0.05 | 2/5 ✗ | -0.23 | -0.24 | ✗  stop buffer_atr 0.2→0.16: -0.18R | 2 | 0.13R | 1, -0.39 (+0.00 / -0.39) | 101 / 31 of 139 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.77; max drawdown 21.4R; longest drawdown 1625 days = 90% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 240 | 37.9 | -0.148 | 0.78 | 54.6R | -0.10 / -0.22 | +0.10 / -0.39 | 1/5 ✗ | -0.20 | -0.26 | ✗  depth 0.985→1.182: -0.26R | 1 | 0.10R | 2, -0.09 (-0.09 / +0.00) | 60 / 7 of 71 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.78; max drawdown 54.6R; longest drawdown 1600 days = 90% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V5 🧪 lab | 1.0 | 15m | **FAILED** | 2971 | 31.6 | -0.149 | 0.79 | 461.9R | -0.16 / -0.14 | -0.18 / -0.12 | 0/5 ✗ | -0.26 | -0.38 | ✗  stop atr 2.0→1.6: -0.22R | 0 | 0.20R | 58, -0.16 (+0.04 / -0.67) | 328 / 67 of 517 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.79; max drawdown 461.9R; not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 5m | **FAILED** | 901 | 36.5 | -0.153 | 0.66 | 143.8R | -0.20 / +0.01 | -0.20 / -0.11 | 1/5 ✗ | -0.20 | -0.21 | ✗  stop max_width_atr 3.0→3.6: -0.16R | 0 | 0.18R | 6, -0.74 (-0.79 / -0.65) | 0 / 0 of 269 | 0 | avg -0.15R/trade (needs +0.15R); profit factor 0.66; max drawdown 143.8R; longest drawdown 687 days = 96% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 243 | 47.7 | -0.158 | 0.73 | 40.8R | -0.17 / -0.12 | -0.14 / -0.20 | 0/5 ✗ | -0.22 | -0.28 | ✗  vol_x 1.2→1.44: -0.32R | 2 | 0.14R | 1, +1.11 (+1.11 / +0.00) | 78 / 150 of 236 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.73; max drawdown 40.8R; longest drawdown 3227 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V5 🧪 lab | 1.0 | 30m | **FAILED** | 3703 | 30.0 | -0.163 | 0.77 | 602.5R | -0.16 / -0.17 | -0.19 / -0.13 | 0/5 ✗ | -0.28 | -0.40 | ✗  rsi_hi 65→52: -0.26R | 0 | 0.22R | 57, -0.30 (-0.05 / -0.94) | 915 / 58 of 1245 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.77; max drawdown 602.5R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 657 | 47.5 | -0.165 | 0.73 | 112.7R | -0.19 / -0.13 | -0.18 / -0.15 | 0/5 ✗ | -0.28 | -0.40 | ✗  stop atr 1.5→1.2: -0.23R | 1 | 0.19R | 8, -0.08 (+0.18 / -0.87) | 71 / 31 of 139 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.73; recovery factor -0.96 (net -108.5R / max drawdown 112.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 37.6R - limit 17R; longest drawdown 1815 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P07-SQUEEZE-RETEST-V5 🧪 lab | 1.0 | 30m | **FAILED** | 1947 | 30.6 | -0.168 | 0.76 | 340.7R | -0.16 / -0.17 | -0.19 / -0.14 | 0/5 ✗ | -0.26 | -0.35 | ✗  stop atr 1.5→1.2: -0.21R | 0 | 0.17R | 24, +0.13 (+0.23 / -0.93) | 238 / 50 of 349 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.76; recovery factor -0.96 (net -326.2R / max drawdown 340.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 41.6R - limit 17R; longest drawdown 1719 days = 94% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 15m | **FAILED** | 818 | 39.5 | -0.173 | 0.68 | 146.5R | -0.17 / -0.17 | -0.13 / -0.21 | 0/5 ✗ | -0.19 | -0.13 | ✗  stop max_width_atr 3.0→2.4: -0.17R | 0 | 0.17R | 4, -0.34 (-0.10 / -0.58) | 0 / 0 of 148 | 0 | avg -0.17R/trade (needs +0.15R); profit factor 0.68; max drawdown 146.5R; longest drawdown 1808 days = 99% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 4637 | 48.4 | -0.174 | 0.44 | 805.3R | -0.16 / -0.21 | -0.17 / -0.17 | 0/5 ✗ | -0.26 | -0.35 | ✗  stop atr 2.0→1.6: -0.22R | 0 | 0.15R | 35, -0.37 (-0.40 / -0.32) | 974 / 36 of 1154 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.44; max drawdown 805.3R; longest drawdown 1827 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 240 | 45.0 | -0.174 | 0.71 | 50.0R | -0.20 / -0.13 | -0.31 / -0.07 | 0/5 ✗ | -0.22 | -0.28 | ✗  adx_min 20→16: -0.24R | 1 | 0.12R | 2, +0.01 (+0.01 / +0.00) | 47 / 7 of 63 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.71; recovery factor -0.84 (net -41.8R / max drawdown 50.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 38.2R - limit 17R; longest drawdown 1691 days = 93% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 5641 | 46.3 | -0.179 | 0.7 | 1011.9R | -0.20 / -0.15 | -0.19 / -0.16 | 0/5 ✗ | -0.27 | -0.37 | ✗  stop atr 1.5→1.2: -0.23R | 0 | 0.17R | 40, -0.37 (-0.28 / -1.15) | 678 / 226 of 1276 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.70; recovery factor -1.00 (net -1010.7R / max drawdown 1011.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 38.1R - limit 17R; longest drawdown 1825 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 441 | 48.1 | -0.180 | 0.7 | 82.4R | -0.14 / -0.25 | -0.24 / -0.13 | 0/5 ✗ | -0.26 | -0.36 | ✗  stop atr 1.5→1.2: -0.20R | 0 | 0.18R | 4, -0.84 (-0.54 / -1.14) | 158 / 11 of 178 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.70; recovery factor -0.96 (net -79.4R / max drawdown 82.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 39.2R - limit 17R; longest drawdown 1719 days = 94% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-S3-FDISP 🧪 lab | 1.0 | 5m | **FAILED** | 1001 | 33.1 | -0.180 | 0.76 | 196.9R | -0.20 / -0.11 | -0.08 / -0.28 | 2/5 ✗ | -0.25 | -0.31 | ✗  stop atr 2.0→1.6: -0.23R | 0 | 0.13R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 5 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.76; recovery factor -0.91 (net -180.0R / max drawdown 196.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 45.1R - limit 17R; longest drawdown 713 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 556 | 41.5 | -0.188 | 0.67 | 110.5R | -0.23 / -0.09 | -0.24 / -0.15 | 0/5 ✗ | -0.28 | -0.35 | ✗  slow 21→25: -0.29R | 0 | 0.16R | 7, -1.15 (-1.15 / -1.17) | 71 / 26 of 111 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.67; recovery factor -0.94 (net -104.3R / max drawdown 110.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 37.7R - limit 17R; longest drawdown 1723 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V5 🧪 lab | 1.0 | 30m | **FAILED** | 6226 | 33.5 | -0.188 | 0.75 | 1175.3R | -0.21 / -0.14 | -0.23 / -0.15 | 0/5 ✗ | -0.29 | -0.39 | ✗  stop max_width_atr 3.0→2.4: -0.19R | 0 | 0.20R | 39, -0.39 (-0.14 / -1.24) | 697 / 75 of 1034 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.75; recovery factor -1.00 (net -1169.7R / max drawdown 1175.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 46.0R - limit 17R; longest drawdown 1826 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 199 | 34.7 | -0.190 | 0.73 | 41.8R | -0.14 / -0.28 | -0.05 / -0.32 | 2/5 ✗ | -0.24 | -0.28 | ✗  depth 0.985→1.182: -0.36R | 1 | 0.11R | 5, -0.61 (-0.61 / +0.00) | 13 / 2 of 20 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.73; max drawdown 41.8R; not profitable in BOTH train and unseen test |
| P08-SESSION-BREAKOUT-V5 🧪 lab | 1.0 | 30m | **FAILED** | 1622 | 33.8 | -0.193 | 0.73 | 321.2R | -0.19 / -0.20 | -0.21 / -0.18 | 0/5 ✗ | -0.29 | -0.38 | ✗  stop atr 1.5→1.2: -0.23R | 1 | 0.18R | 16, +0.05 (+0.13 / -1.16) | 193 / 36 of 280 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.73; recovery factor -0.97 (net -312.7R / max drawdown 321.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 44.5R - limit 17R; longest drawdown 1795 days = 99% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P06-VWAP-REVERSION-V2 🧪 lab | 1.0 | 1h | **FAILED** | 83 | 43.4 | -0.199 | 0.55 | 19.4R | -0.22 / -0.11 | -0.21 / -0.19 | 1/5 ✗ | -0.26 | -0.32 | ✗  rsi_lo 35→28: -0.82R | 1 | 0.11R | 2, +0.60 (+1.79 / -0.60) | 208 / 0 of 211 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.55; max drawdown 19.4R; longest drawdown 3296 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 209 | 45.0 | -0.208 | 0.64 | 47.4R | -0.21 / -0.20 | -0.27 / -0.15 | 0/5 ✗ | -0.26 | -0.32 | ✗  st_n 10→12: -0.24R | 2 | 0.08R | 1, +0.24 (+0.24 / +0.00) | 41 / 1 of 50 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.64; recovery factor -0.92 (net -43.5R / max drawdown 47.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 39.6R - limit 17R; longest drawdown 3105 days = 97% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 1530 | 42.5 | -0.210 | 0.65 | 322.4R | -0.24 / -0.13 | -0.24 / -0.18 | 0/5 ✗ | -0.33 | -0.46 | ✗  stop atr 1.5→1.2: -0.30R | 0 | 0.23R | 7, -1.04 (-1.27 / -0.73) | 79 / 25 of 116 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.65; recovery factor -1.00 (net -321.1R / max drawdown 322.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 41.4R - limit 17R; longest drawdown 1818 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V2 🧪 lab | 1.0 | 15m | **FAILED** | 3121 | 28.5 | -0.214 | 0.7 | 693.9R | -0.19 / -0.25 | -0.23 / -0.18 | 0/5 ✗ | -0.37 | -0.52 | ✗  stop atr 1.5→1.2: -0.27R | 0 | 0.28R | 26, -0.48 (-0.32 / -1.01) | 865 / 243 of 1182 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.21R/trade (needs +0.10R); profit factor 0.70; max drawdown 693.9R; not profitable in BOTH train and unseen test |
| P08-SESSION-BREAKOUT-V2 🧪 lab | 1.0 | 15m | **FAILED** | 841 | 32.8 | -0.217 | 0.72 | 190.7R | -0.25 / -0.18 | -0.25 / -0.18 | 0/5 ✗ | -0.34 | -0.46 | ✗  stop atr 1.5→1.2: -0.23R | 1 | 0.22R | 4, -0.28 (+0.03 / -1.23) | 108 / 27 of 143 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.72; recovery factor -0.96 (net -182.4R / max drawdown 190.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 49.1R - limit 17R; longest drawdown 1799 days = 99% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P07-SQUEEZE-RETEST-V2 🧪 lab | 1.0 | 15m | **FAILED** | 1686 | 29.4 | -0.224 | 0.7 | 391.0R | -0.20 / -0.27 | -0.24 / -0.21 | 0/5 ✗ | -0.36 | -0.51 | ✗  stop atr 1.5→1.2: -0.27R | 0 | 0.23R | 10, -0.17 (-0.06 / -1.14) | 270 / 120 of 406 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.70; recovery factor -0.96 (net -377.3R / max drawdown 391.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 47.4R - limit 17R; longest drawdown 1692 days = 93% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P06-VWAP-REVERSION-V2 🧪 lab | 1.0 | 30m | **FAILED** | 937 | 40.4 | -0.227 | 0.64 | 232.5R | -0.19 / -0.28 | -0.26 / -0.20 | 0/5 ✗ | -0.34 | -0.44 | ✗  rsi_lo 35→28: -0.32R | 1 | 0.19R | 14, +0.66 (+0.98 / +0.09) | 412 / 1 of 454 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.64; max drawdown 232.5R; longest drawdown 1671 days = 92% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P05-RANGE-REVERSAL-V2 🧪 lab | 1.0 | 1h | **FAILED** | 1428 | 45.8 | -0.231 | 0.59 | 335.0R | -0.23 / -0.24 | -0.26 / -0.21 | 0/5 ✗ | -0.31 | -0.39 | ✗  rsi_lo 35→28: -0.39R | 0 | 0.13R | 11, +0.57 (+0.57 / +0.00) | 435 / 0 of 486 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.59; max drawdown 335.0R; longest drawdown 3306 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V2 🧪 lab | 1.0 | 15m | **FAILED** | 4763 | 33.6 | -0.234 | 0.7 | 1161.6R | -0.26 / -0.19 | -0.25 / -0.22 | 0/5 ✗ | -0.36 | -0.49 | ✗  stop max_width_atr 3.0→2.4: -0.25R | 0 | 0.25R | 23, -0.17 (+0.14 / -1.29) | 715 / 222 of 1017 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.23R/trade (needs +0.10R); profit factor 0.70; recovery factor -0.96 (net -1112.5R / max drawdown 1161.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 49.9R - limit 17R; longest drawdown 1830 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 7426 | 39.9 | -0.241 | 0.3 | 1788.3R | -0.21 / -0.30 | -0.25 / -0.23 | 0/5 ✗ | -0.38 | -0.52 | ✗  stop atr 2.0→1.6: -0.31R | 0 | 0.23R | 116, -0.34 (-0.38 / -0.26) | 1088 / 37 of 1329 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.30; max drawdown 1788.3R; longest drawdown 1830 days = 100% of the tested period (limit 60%); loss clustering: 24 losses in a row as it happened, random orders stay at or below 21 in 95% of cases; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 9622 | 44.8 | -0.247 | 0.62 | 2379.7R | -0.25 / -0.24 | -0.27 / -0.22 | 0/5 ✗ | -0.38 | -0.52 | ✗  stop atr 1.5→1.2: -0.32R | 0 | 0.24R | 62, -0.55 (-0.45 / -1.23) | 1284 / 280 of 1863 | 0 | avg -0.25R/trade (needs +0.10R); profit factor 0.62; recovery factor -1.00 (net -2379.0R / max drawdown 2379.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 45.4R - limit 17R; longest drawdown 1827 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P07-SQUEEZE-RETEST-V5 🧪 lab | 1.0 | 15m | **FAILED** | 3732 | 28.7 | -0.253 | 0.67 | 953.2R | -0.24 / -0.27 | -0.27 / -0.24 | 0/5 ✗ | -0.40 | -0.55 | ✗  stop atr 1.5→1.2: -0.31R | 0 | 0.25R | 44, -0.32 (-0.20 / -0.67) | 270 / 73 of 406 | 0 | avg -0.25R/trade (needs +0.10R); profit factor 0.67; recovery factor -0.99 (net -945.0R / max drawdown 953.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 50.8R - limit 17R; longest drawdown 1822 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P05-RANGE-REVERSAL-V2 🧪 lab | 1.0 | 30m | **FAILED** | 4268 | 46.1 | -0.256 | 0.57 | 1109.4R | -0.23 / -0.33 | -0.26 / -0.25 | 0/5 ✗ | -0.38 | -0.50 | ✗  stop atr 1.5→1.2: -0.31R | 0 | 0.20R | 47, -0.26 (-0.07 / -0.83) | 399 / 3 of 515 | 0 | avg -0.26R/trade (needs +0.10R); profit factor 0.57; max drawdown 1109.4R; longest drawdown 1659 days = 91% of the tested period (limit 60%); loss clustering: 18 losses in a row as it happened, random orders stay at or below 16 in 95% of cases; not profitable in BOTH train and unseen test |
| P08-SESSION-BREAKOUT-V5 🧪 lab | 1.0 | 15m | **FAILED** | 1893 | 32.0 | -0.258 | 0.67 | 505.3R | -0.26 / -0.26 | -0.28 / -0.23 | 0/5 ✗ | -0.40 | -0.54 | ✗  stop atr 1.5→1.2: -0.29R | 0 | 0.25R | 17, +0.30 (+0.40 / -1.23) | 108 / 13 of 143 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.67; recovery factor -0.97 (net -489.3R / max drawdown 505.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 50.5R - limit 17R; longest drawdown 1793 days = 99% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V3 🧪 lab | 1.0 | 4h | **FAILED** | 117 | 23.1 | -0.261 | 0.62 | 30.9R | -0.24 / -0.30 | -0.25 / -0.29 | 0/5 ✗ | -0.29 | -0.33 | ✗  fast 20→24: -0.31R | 1 | 0.06R | 1, -1.08 (-1.08 / +0.00) | 178 / 81 of 262 | 0 | avg -0.26R/trade (needs +0.10R); profit factor 0.62; max drawdown 30.9R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V5 🧪 lab | 1.0 | 15m | **FAILED** | 6894 | 27.9 | -0.263 | 0.65 | 1817.7R | -0.23 / -0.31 | -0.30 / -0.22 | 0/5 ✗ | -0.44 | -0.61 | ✗  stop atr 1.5→1.2: -0.33R | 0 | 0.31R | 93, -0.36 (-0.19 / -1.21) | 865 / 103 of 1182 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.65; max drawdown 1817.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 200 | 28.0 | -0.269 | 0.69 | 56.0R | -0.19 / -0.42 | -0.45 / +0.01 | 0/5 ✗ | -0.38 | -0.48 | ✗  time_stop_bars 30→24: -0.32R | 1 | 0.23R | 1, -1.47 (-1.47 / +0.00) | 40 / 80 of 128 | 0 | avg -0.27R/trade (needs +0.10R); profit factor 0.69; max drawdown 56.0R; longest drawdown 1816 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V5 🧪 lab | 1.0 | 15m | **FAILED** | 10470 | 32.6 | -0.277 | 0.66 | 2912.8R | -0.28 / -0.26 | -0.30 / -0.26 | 0/5 ✗ | -0.41 | -0.55 | ✗  stop buffer_atr 0.2→0.16: -0.29R | 0 | 0.28R | 81, -0.20 (+0.01 / -1.30) | 715 / 89 of 1017 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.28R/trade (needs +0.10R); profit factor 0.66; recovery factor -1.00 (net -2901.2R / max drawdown 2912.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 52.7R - limit 17R; longest drawdown 1830 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 995 | 29.4 | -0.296 | 0.62 | 296.9R | -0.32 / -0.24 | -0.25 / -0.33 | 0/5 ✗ | -0.37 | -0.43 | ✗  rsi_n 14→17: -0.41R | 1 | 0.13R | 10, -0.51 (-0.67 / -0.26) | 615 / 5 of 663 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.62; max drawdown 296.9R; longest drawdown 3316 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 1409 | 43.1 | -0.307 | 0.56 | 435.2R | -0.30 / -0.32 | -0.32 / -0.29 | 0/5 ✗ | -0.45 | -0.58 | ✗  stop atr 1.5→1.2: -0.38R | 0 | 0.27R | 8, -0.39 (-0.34 / -0.57) | 77 / 39 of 133 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.31R/trade (needs +0.10R); profit factor 0.56; recovery factor -1.00 (net -433.1R / max drawdown 435.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 50.5R - limit 17R; longest drawdown 1815 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 2698 | 30.6 | -0.316 | 0.6 | 854.1R | -0.32 / -0.30 | -0.33 / -0.30 | 0/5 ✗ | -0.43 | -0.53 | ✗  bb_k 2→3: -0.36R | 0 | 0.19R | 27, -0.52 (-0.35 / -0.84) | 531 / 29 of 651 | 0 | avg -0.32R/trade (needs +0.10R); profit factor 0.60; max drawdown 854.1R; longest drawdown 1826 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P06-VWAP-REVERSION-V2 🧪 lab | 1.0 | 15m | **FAILED** | 3911 | 34.5 | -0.335 | 0.56 | 1312.2R | -0.30 / -0.38 | -0.35 / -0.32 | 0/5 ✗ | -0.50 | -0.67 | ✗  stop atr 1.5→1.2: -0.42R | 0 | 0.27R | 64, -0.14 (+0.10 / -0.84) | 405 / 4 of 528 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.34R/trade (needs +0.10R); profit factor 0.56; max drawdown 1312.2R; longest drawdown 1822 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 861 | 28.3 | -0.363 | 0.59 | 321.5R | -0.28 / -0.53 | -0.45 / -0.27 | 0/5 ✗ | -0.49 | -0.60 | ✗  stop buffer_atr 0.2→0.16: -0.39R | 0 | 0.27R | 8, -0.20 (-0.38 / +0.35) | 385 / 884 of 1405 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.36R/trade (needs +0.10R); profit factor 0.59; max drawdown 321.5R; longest drawdown 1573 days = 86% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P05-RANGE-REVERSAL-V2 🧪 lab | 1.0 | 15m | **FAILED** | 10548 | 42.1 | -0.375 | 0.45 | 3960.2R | -0.35 / -0.42 | -0.37 / -0.38 | 0/5 ✗ | -0.56 | -0.73 | ✗  stop atr 1.5→1.2: -0.47R | 0 | 0.29R | 130, -0.24 (-0.14 / -0.56) | 309 / 1 of 477 | 0 | not cost-viable: fees + slippage 0.29R per trade (stop must be ≥ 4x the round-trip cost); avg -0.38R/trade (needs +0.10R); profit factor 0.45; max drawdown 3960.2R; longest drawdown 1829 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 394 | 41.1 | -0.393 | 0.45 | 159.8R | -0.39 / -0.40 | -0.41 / -0.37 | 1/5 ✗ | -0.51 | -0.63 | ✗  vol_x 1.2→1.44: -0.43R | 0 | 0.25R | 1, -1.34 (-1.34 / +0.00) | 87 / 173 of 276 | 0 | avg -0.39R/trade (needs +0.10R); profit factor 0.45; max drawdown 159.8R; longest drawdown 1738 days = 96% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 1439 | 39.7 | -0.455 | 0.42 | 658.9R | -0.38 / -0.56 | -0.43 / -0.49 | 0/5 ✗ | -0.66 | -0.87 | ✗  stop atr 1.0→0.8: -0.55R | 0 | 0.37R | 4, -0.81 (-1.68 / +1.79) | 78 / 193 of 285 | 0 | not cost-viable: fees + slippage 0.37R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.42; max drawdown 658.9R; longest drawdown 1691 days = 93% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 1658 | 35.8 | -0.491 | 0.39 | 815.8R | -0.47 / -0.55 | -0.51 / -0.46 | 0/5 ✗ | -0.73 | -0.97 | ✗  stop atr 1.5→1.2: -0.61R | 0 | 0.41R | 29, -1.02 (-0.98 / -1.13) | 198 / 67 of 298 | 0 | not cost-viable: fees + slippage 0.41R per trade (stop must be ≥ 4x the round-trip cost); avg -0.49R/trade (needs +0.10R); profit factor 0.39; recovery factor -1.00 (net -814.2R / max drawdown 815.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 69.1R - limit 17R; longest drawdown 726 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| PB-B-SWEEP-15M | 1.0 | 15m | **FAILED** | 208 | 38.0 | -0.531 | 0.33 | 112.2R | -0.50 / -0.55 | -0.52 / -0.54 | 0/5 ✗ | -0.60 | -0.74 | ✗  time_stop_bars 16→13: -0.53R | 0 | 0.48R | 3, -1.09 (-1.43 / -0.44) | 0 / 0 of 14 | 0 | not cost-viable: fees + slippage 0.48R per trade (stop must be ≥ 4x the round-trip cost); avg -0.53R/trade (needs +0.15R); profit factor 0.33; max drawdown 112.2R; longest drawdown 701 days = 98% of the tested period (limit 60%); loss clustering: 15 losses in a row as it happened, random orders stay at or below 14 in 95% of cases; not profitable in BOTH train and unseen test |
| PB-B-SWEEP | 1.0 | 5m | **FAILED** | 886 | 34.7 | -0.646 | 0.25 | 574.6R | -0.67 / -0.57 | -0.63 / -0.66 | 0/5 ✗ | -0.76 | -0.84 | ✗  time_stop_bars 48→38: -0.65R | 0 | 0.62R | 3, -1.13 (-1.45 / -0.49) | 0 / 0 of 28 | 0 | not cost-viable: fees + slippage 0.62R per trade (stop must be ≥ 4x the round-trip cost); avg -0.65R/trade (needs +0.15R); profit factor 0.25; max drawdown 574.6R; longest drawdown 722 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 3254 | 32.5 | -0.725 | 0.28 | 2363.0R | -0.70 / -0.79 | -0.73 / -0.71 | 0/5 ✗ | -1.13 | -1.54 | ✗  stop atr 1.0→0.8: -0.92R | 0 | 0.67R | 33, -1.35 (-1.40 / -1.19) | 216 / 519 of 785 | 0 | not cost-viable: fees + slippage 0.67R per trade (stop must be ≥ 4x the round-trip cost); avg -0.72R/trade (needs +0.10R); profit factor 0.28; max drawdown 2363.0R; longest drawdown 725 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **92** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 360 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.63** (Bonferroni: family-wise false-winner rate 0.05 over 360 trials; with 1 trial it would be 1.65).

**Research run duration:** 57.5 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 60 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (446.7 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

| Strategy | TF | Status | Trades | Drawdown as it happened | 95% worst drawdown | Expected worst losing streak |
|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT-S4 v1.1 | 4h | PAPER_TRADING | 633 | 25.9R | 23.8R ✗ | 16 |
| donchian_breakout-VEXIT v1.0 | 4h | PAPER_TRADING | 814 | 17.9R | 23.9R ✗ | 15 |
| donchian_breakout v1.0 | 4h | PAPER_TRADING | 837 | 10.7R | 22.1R ✗ | 11 |

**Rule significance:** in 77 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - active since your yes on 2026-10-10.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

3 of 168 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT-S4 v1.1 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 9.28 | 16.1R | 478 d (15%) | passes every gate |
| donchian_breakout-VEXIT v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 10.41 | 16.7R | 430 d (13%) | passes every gate |
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 8.2 | 13.7R | 584 d (18%) | passes every gate |

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- P02-EMA-PULLBACK-V4-S6-FHTF v1.0 4h = near-duplicate of P02-EMA-PULLBACK-V4-S6 v1.0 4h (80% of 291 trades shared)

- P02-EMA-PULLBACK-V4-S6-S6 v1.0 4h = near-duplicate of P02-EMA-PULLBACK-V4-S6 v1.0 4h (89% of 403 trades shared)

- P07-SQUEEZE-RETEST-V4 v1.0 4h = near-duplicate of P07-SQUEEZE-RETEST-V1 v1.0 4h (91% of 722 trades shared)

- P08-SESSION-BREAKOUT-V4 v1.0 1h = near-duplicate of P08-SESSION-BREAKOUT-V1 v1.0 1h (96% of 1,164 trades shared)

- PB-A-GRADED v1.0 5m = near-duplicate of PB-A-APLUS v1.0 5m (81% of 64 trades shared)

- PB-B-SWEEP-LIMIT v1.0 5m = near-duplicate of PB-B-APLUS v1.0 5m (80% of 215 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (79% of 2,554 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (75% of 1,777 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 926 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,241 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,499 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 814 trades shared)

🧪 **Strategy lab:** 63 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S5-SWEEP-MSS-FVG-5M | 15m | 2 | +0.130 | +0.000 | -0.616 | -4.320 | too few trades to compare |
| TRD-H4-BREAKOUT | 1h | 821 | +0.109 | +0.255 | +0.029 | +0.056 | yes |
| TRD-H4-BREAKOUT | 30m | 559 | +0.100 | +0.255 | -0.035 | +0.033 | yes |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.147 | +0.007 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | -0.218 | +0.000 | too few trades to compare |
| PB-C-BREAKOUT | 5m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET | 15m | 7 | -0.001 | -1.190 | -0.138 | -0.163 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 5 | -0.172 | -0.517 | -0.504 | -0.581 | too few trades to compare |
| PB-A-PULLBACK-CVD | 5m | 10 | -0.520 | -1.097 | -0.497 | -1.097 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 9 | -0.653 | -1.173 | -0.023 | -0.100 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 12 | -0.839 | -2.597 | +0.074 | -0.542 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 1 | -1.208 | +0.000 | -0.487 | -1.179 | too few trades to compare |
| P11-MOMENTUM-V1 | 30m | - | - | - | - | - | waiting for research |
| TRD-H4-PULLBACK | 1h | 803 | +0.015 | -0.018 | -0.018 | -0.065 | yes |
| TRD-H4-PULLBACK | 15m | 1941 | -0.004 | +0.123 | -0.088 | -0.043 | yes |
| TRD-H4-PULLBACK | 5m | 2179 | -0.027 | +0.044 | -0.107 | -0.070 | yes |
| TRD-H4-BREAKOUT | 15m | 983 | -0.032 | +0.032 | -0.086 | -0.053 | yes |
| TRD-H4-PULLBACK | 30m | 1051 | -0.049 | +0.074 | -0.097 | -0.038 | yes |
| S8-PDH-PDL-SWEEP | 1h | 229 | -0.058 | -0.280 | -0.115 | -0.062 | no |
| TRD-H4-BREAKOUT | 5m | 1363 | -0.068 | -0.020 | -0.120 | -0.081 | yes |
| S8-PDH-PDL-SWEEP | 30m | 200 | -0.269 | -0.418 | -0.363 | -0.525 | yes |
| PB-B-SWEEP | 5m | 886 | -0.646 | -0.570 | -0.375 | -0.375 | too few trades to compare |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): P07-SQUEEZE-RETEST-V1@1.0 4h FORMALIZED → BACKTESTING; P07-SQUEEZE-RETEST-V2@1.0 15m FORMALIZED → FAILED; P07-SQUEEZE-RETEST-V2@1.0 1h FORMALIZED → BACKTESTING; P07-SQUEEZE-RETEST-V2@1.0 30m FORMALIZED → FAILED; P07-SQUEEZE-RETEST-V3@1.0 4h FORMALIZED → BACKTESTING; P07-SQUEEZE-RETEST-V4@1.0 4h FORMALIZED → BACKTESTING; P07-SQUEEZE-RETEST-V5@1.0 15m FORMALIZED → FAILED; P07-SQUEEZE-RETEST-V5@1.0 1h FORMALIZED → FAILED; P07-SQUEEZE-RETEST-V5@1.0 30m FORMALIZED → FAILED; P08-SESSION-BREAKOUT-V1@1.0 1h FORMALIZED → FAILED; P08-SESSION-BREAKOUT-V2@1.0 15m FORMALIZED → FAILED; P08-SESSION-BREAKOUT-V2@1.0 30m FORMALIZED → FAILED; ... and 8 more
- **Not tested (IDEA / RETIRED):** donchian_breakout-VEXIT-VRVOL v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S5 v1.0 (RETIRED)

### 3c. Research layers (daily run)
Last run: **2026-10-13 01:02 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 7 | 2017-08-17 | 2026-10-12 | 20047 |  |
| 1h | 7 | 2017-08-17 | 2026-10-13 | 80125 |  |
| 30m | 7 | 2021-10-05 | 2026-10-13 | 87600 |  |
| 15m | 7 | 2021-10-05 | 2026-10-13 | 175200 |  |
| 5m | 7 | 2024-10-13 | 2026-10-13 | 210240 |  |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | PAPER_TRADING | 814 (479) | false_breakout, trend_reversal | false_breakout 63% | +0.47R | -0.37R | +0.31 / +0.25 |
| donchian_breakout-VEXIT-S4 | 4h | PAPER_TRADING | 633 (375) | no_displacement, false_breakout | false_breakout 63%, no_displacement 36% | +0.46R | -0.36R | +0.28 / +0.23 |
| donchian_breakout | 4h | PAPER_TRADING | 837 (371) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 66%, stop_too_tight 34%, no_displacement 33% | +0.33R | -0.37R | +0.21 / +0.16 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 926 (552) | false_breakout, trend_reversal | false_breakout 62% | +0.48R | -0.37R | +0.30 / +0.24 |
| P01-BREAKOUT-V3 | 4h | BACKTESTING | 333 (198) | false_breakout | false_breakout 68%, no_displacement 33% | +0.43R | -0.37R | +0.26 / +0.21 |
| P04-MACD-SUPERTREND-V3 | 4h | BACKTESTING | 150 (92) | false_breakout, indicator_lag | regime_mismatch 49%, false_breakout 47%, indicator_lag 30% | +0.37R | -0.36R | +0.26 / +0.20 |
| TRD-H4-BREAKOUT-S3-FDISP | 30m | BACKTESTING | 412 (239) | overextended_entry, late_entry, false_breakout | overextended_entry 85%, false_breakout 72%, late_entry 56% | +0.53R | -0.42R | +0.26 / +0.19 |
| P01-BREAKOUT-V1 | 4h | BACKTESTING | 1058 (639) | htf_conflict, false_breakout, trend_reversal | false_breakout 62% | +0.53R | -0.41R | +0.24 / +0.19 |
| P01-BREAKOUT-V4 | 4h | BACKTESTING | 900 (544) | htf_conflict, false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, regime_mismatch 39%, stop_too_tight 38% | +0.53R | -0.43R | +0.25 / +0.18 |
| P02-EMA-PULLBACK-V4-S6-S6 | 4h | BACKTESTING | 403 (256) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 78%, indicator_lag 32%, stop_too_tight 28% | +0.47R | -0.49R | +0.25 / +0.16 |
| TRD-H4-BREAKOUT-S3 | 1h | BACKTESTING | 939 (565) | false_breakout | false_breakout 70% | +0.51R | -0.42R | +0.21 / +0.15 |
| P02-EMA-PULLBACK-V4-S6 | 4h | BACKTESTING | 365 (234) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 77%, indicator_lag 33%, stop_too_tight 28% | +0.45R | -0.50R | +0.23 / +0.14 |
| TRD-H4-BREAKOUT-S3-FDISP | 1h | BACKTESTING | 679 (416) | false_breakout | false_breakout 62% | +0.54R | -0.48R | +0.18 / +0.13 |
| TRD-H4-BREAKOUT | 1h | BACKTESTING | 821 (507) | false_breakout | false_breakout 65% | +0.54R | -0.44R | +0.16 / +0.11 |
| TRD-H4-BREAKOUT | 30m | BACKTESTING | 559 (337) | false_breakout | false_breakout 75%, no_displacement 46% | +0.52R | -0.43R | +0.18 / +0.10 |
| P02-EMA-PULLBACK-V4 | 4h | BACKTESTING | 297 (193) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 84%, indicator_lag 36%, stop_too_tight 28% | +0.43R | -0.50R | +0.18 / +0.10 |
| P07-SQUEEZE-RETEST-V4 | 4h | BACKTESTING | 722 (473) | false_breakout, stop_too_tight | false_breakout 53%, stop_too_tight 41% | +0.49R | -0.47R | +0.14 / +0.06 |
| P07-SQUEEZE-RETEST-V3 | 4h | BACKTESTING | 249 (160) | false_breakout | no_displacement 62%, false_breakout 58% | +0.42R | -0.36R | +0.12 / +0.05 |
| P05-RANGE-REVERSAL-V4 | 4h | BACKTESTING | 362 (233) | stop_too_tight | stop_too_tight 30% | +0.49R | -0.43R | +0.15 / +0.05 |
| P02-EMA-PULLBACK-V4-S6-FHTF | 4h | BACKTESTING | 291 (197) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 79%, indicator_lag 32%, stop_too_tight 28% | +0.46R | -0.50R | +0.12 / +0.04 |
| TRD-H4-BREAKOUT-noT4 | 1h | BACKTESTING | 2641 (1670) | false_breakout | false_breakout 65% | +0.51R | -0.44R | +0.09 / +0.03 |
| P07-SQUEEZE-RETEST-V1 | 4h | BACKTESTING | 794 (515) | false_breakout | false_breakout 52% | +0.45R | -0.41R | +0.10 / +0.02 |
| P07-SQUEEZE-RETEST-V2 | 1h | BACKTESTING | 1045 (684) | no_displacement, false_breakout, regime_mismatch | no_displacement 64%, false_breakout 53% | +0.47R | -0.47R | +0.14 / +0.01 |
| bb_squeeze_breakout | 1h | BACKTESTING | 640 (303) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, no_displacement 51%, stop_too_tight 38%, regime_mismatch 35% | +0.35R | -0.47R | +0.16 / +0.01 |
| TRD-H4-BREAKOUT-S3 | 30m | BACKTESTING | 837 (534) | no_displacement, false_breakout | false_breakout 78%, no_displacement 67% | +0.44R | -0.42R | +0.08 / +0.01 |
| TRD-H4-BREAKOUT-S3-FDISP | 15m | BACKTESTING | 708 (446) | false_breakout | false_breakout 72% | +0.44R | -0.48R | +0.11 / +0.01 |
| P01-BREAKOUT-V2 | 30m | BACKTESTING | 873 (557) | no_displacement, false_breakout | false_breakout 75%, no_displacement 38% | +0.45R | -0.42R | +0.16 / +0.01 |
| PB-B-APLUS | 15m | BACKTESTING | 79 (43) | stop_too_tight | regime_mismatch 46%, stop_too_tight 44% | +0.29R | -0.34R | +0.02 / -0.14 |
| PB-A-GRADED | 5m | BACKTESTING | 64 (38) | stop_too_tight, indicator_lag | stop_too_tight 37%, indicator_lag 26% | +0.43R | -0.24R | -0.09 / -0.26 |
| PB-A-APLUS | 5m | BACKTESTING | 52 (33) | stop_too_tight, indicator_lag | stop_too_tight 42%, indicator_lag 30% | +0.42R | -0.24R | -0.15 / -0.32 |
| P04-MACD-SUPERTREND-V4 | 4h | FAILED | 372 (233) | overextended_entry, false_breakout, regime_mismatch, stop_too_tight, indicator_lag, structural_change | regime_mismatch 49%, overextended_entry 48%, false_breakout 46%, stop_too_tight 36% | +0.41R | -0.38R | +0.20 / +0.13 |
| P04-MACD-SUPERTREND-V1 | 4h | FAILED | 383 (245) | overextended_entry, false_breakout, indicator_lag, structural_change | regime_mismatch 49%, overextended_entry 49%, false_breakout 46%, indicator_lag 31% | +0.43R | -0.37R | +0.18 / +0.11 |
| bb_squeeze_breakout | 4h | FAILED | 215 (103) | false_breakout, stop_too_tight, structural_change | false_breakout 59%, stop_too_tight 42%, regime_mismatch 32% | +0.33R | -0.36R | +0.12 / +0.04 |
| TRD-H4-PULLBACK | 1h | FAILED | 803 (503) | low_relative_volume, indicator_lag, structural_change | low_relative_volume 56%, indicator_lag 25% | +0.45R | -0.41R | +0.07 / +0.01 |
| TRD-H4-PULLBACK | 15m | FAILED | 1941 (1199) | none | - | +0.50R | -0.40R | +0.10 / -0.00 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1279 (831) | no_displacement, false_breakout | false_breakout 70%, no_displacement 39% | +0.48R | -0.40R | +0.12 / -0.01 |
| macd_trend_cross | 1h | FAILED | 139 (67) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 91%, indicator_lag 45%, stop_too_tight 34% | +0.28R | -0.39R | +0.13 / -0.01 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 1795 (1207) | false_breakout, regime_mismatch | false_breakout 62%, regime_mismatch 31% | +0.50R | -0.39R | +0.07 / -0.01 |
| TRD-H4-PULLBACK-noT4 | 1h | FAILED | 3703 (2311) | structural_change | - | +0.50R | -0.42R | +0.05 / -0.02 |
| donchian_breakout-VEXIT | 1h | FAILED | 2241 (1511) | false_breakout | false_breakout 63% | +0.51R | -0.39R | +0.07 / -0.02 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2554 (1720) | false_breakout, regime_mismatch | false_breakout 64%, regime_mismatch 32% | +0.50R | -0.40R | +0.08 / -0.02 |
| TRD-H4-BREAKOUT-S3 | 15m | FAILED | 1455 (947) | false_breakout | false_breakout 77% | +0.48R | -0.50R | +0.08 / -0.02 |
| P01-BREAKOUT-V2 | 1h | FAILED | 1849 (1251) | false_breakout | false_breakout 64% | +0.52R | -0.38R | +0.07 / -0.02 |
| P01-BREAKOUT-V5 | 1h | FAILED | 3762 (2521) | false_breakout | false_breakout 61% | +0.50R | -0.41R | +0.08 / -0.02 |
| P02-EMA-PULLBACK-V1 | 4h | FAILED | 299 (205) | regime_mismatch, indicator_lag, structural_change | regime_mismatch 85%, indicator_lag 38% | +0.41R | -0.42R | +0.06 / -0.02 |
| P03-FIB-PULLBACK-V4 | 4h | FAILED | 250 (172) | late_entry, stop_too_tight, indicator_lag, structural_change | regime_mismatch 58%, stop_too_tight 33%, indicator_lag 28% | +0.48R | -0.43R | +0.07 / -0.03 |
| TRD-H4-PULLBACK | 5m | FAILED | 2179 (1348) | overextended_entry | - | +0.52R | -0.43R | +0.11 / -0.03 |
| TRD-H4-BREAKOUT | 15m | FAILED | 983 (636) | false_breakout | false_breakout 75% | +0.44R | -0.49R | +0.07 / -0.03 |
| P04-MACD-SUPERTREND-V2 | 1h | FAILED | 1199 (798) | false_breakout, regime_mismatch, indicator_lag | regime_mismatch 51%, false_breakout 42%, indicator_lag 34% | +0.46R | -0.39R | +0.07 / -0.03 |
| TRD-H4-BREAKOUT-noT4 | 30m | FAILED | 1938 (1244) | false_breakout | false_breakout 71% | +0.49R | -0.43R | +0.05 / -0.04 |
| donchian_breakout | 1h | FAILED | 2301 (1193) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 37%, stop_too_tight 32%, regime_mismatch 26% | +0.37R | -0.40R | +0.05 / -0.04 |
| P04-MACD-SUPERTREND-V2 | 30m | FAILED | 1450 (946) | no_displacement, false_breakout, regime_mismatch, indicator_lag | no_displacement 75%, false_breakout 36%, indicator_lag 34%, regime_mismatch 30% | +0.48R | -0.45R | +0.11 / -0.04 |
| TRD-H4-BREAKOUT-S3 | 5m | FAILED | 1611 (1009) | false_breakout | false_breakout 80% | +0.44R | -0.43R | +0.10 / -0.04 |
| P07-SQUEEZE-RETEST-V5 | 1h | FAILED | 2496 (1684) | low_relative_volume, no_displacement, false_breakout, regime_mismatch | no_displacement 66%, false_breakout 52% | +0.48R | -0.46R | +0.09 / -0.05 |
| TRD-H4-PULLBACK | 30m | FAILED | 1051 (675) | none | - | +0.48R | -0.41R | +0.03 / -0.05 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1777 (1176) | false_breakout | false_breakout 71% | +0.47R | -0.41R | +0.10 / -0.05 |
| P08-SESSION-BREAKOUT-V3 | 1h | FAILED | 420 (273) | overextended_entry, false_breakout | false_breakout 60%, overextended_entry 59% | +0.44R | -0.48R | +0.07 / -0.05 |
| donchian_breakout-VEXIT | 30m | FAILED | 1499 (998) | false_breakout | false_breakout 71% | +0.47R | -0.41R | +0.08 / -0.05 |
| P01-BREAKOUT-V2 | 15m | FAILED | 1330 (872) | false_breakout | false_breakout 71% | +0.47R | -0.43R | +0.15 / -0.06 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 229 (148) | stop_too_tight, sweep_continued, structural_change | sweep_continued 97%, range_market 56%, stop_too_tight 30% | +0.56R | -0.40R | +0.15 / -0.06 |
| donchian_breakout | 30m | FAILED | 1552 (804) | no_displacement, false_breakout, stop_too_tight | false_breakout 75%, no_displacement 39%, stop_too_tight 33% | +0.29R | -0.40R | +0.07 / -0.07 |
| TRD-H4-BREAKOUT | 5m | FAILED | 1363 (864) | false_breakout | false_breakout 74% | +0.43R | -0.44R | +0.07 / -0.07 |
| trend_pullback | 4h | FAILED | 934 (485) | regime_mismatch, indicator_lag | regime_mismatch 80%, indicator_lag 38% | +0.36R | -0.43R | +0.00 / -0.07 |
| supertrend_flip | 4h | FAILED | 70 (38) | indicator_lag, structural_change | regime_mismatch 63%, indicator_lag 40% | +0.39R | -0.43R | -0.01 / -0.08 |
| P08-SESSION-BREAKOUT-V1 | 1h | FAILED | 1210 (786) | overextended_entry, false_breakout | false_breakout 60%, overextended_entry 59% | +0.47R | -0.45R | +0.05 / -0.08 |
| P04-MACD-SUPERTREND-V2 | 15m | FAILED | 2287 (1507) | range_market, indicator_lag | range_market 37%, indicator_lag 34% | +0.47R | -0.44R | +0.13 / -0.08 |
| P08-SESSION-BREAKOUT-V4 | 1h | FAILED | 1164 (781) | false_breakout | false_breakout 60% | +0.50R | -0.50R | +0.05 / -0.08 |
| P03-FIB-PULLBACK-V1 | 4h | FAILED | 253 (165) | indicator_lag | indicator_lag 30% | +0.43R | -0.44R | +0.00 / -0.08 |
| TRD-H4-BREAKOUT-noT4 | 15m | FAILED | 3338 (2197) | false_breakout | false_breakout 74% | +0.45R | -0.45R | +0.03 / -0.09 |
| TRD-H4-PULLBACK-noT4 | 15m | FAILED | 7314 (4666) | none | - | +0.50R | -0.40R | +0.03 / -0.09 |
| P03-FIB-PULLBACK-V2 | 1h | FAILED | 2388 (1563) | regime_mismatch, indicator_lag | regime_mismatch 66%, indicator_lag 36% | +0.42R | -0.45R | +0.05 / -0.09 |
| P02-EMA-PULLBACK-V2 | 1h | FAILED | 2302 (1585) | low_relative_volume, regime_mismatch, indicator_lag | regime_mismatch 82%, low_relative_volume 52%, indicator_lag 37% | +0.40R | -0.42R | +0.04 / -0.09 |
| P01-BREAKOUT-V5 | 30m | FAILED | 1938 (1301) | false_breakout | false_breakout 70% | +0.46R | -0.42R | +0.08 / -0.10 |
| TRD-H4-PULLBACK-noT4 | 30m | FAILED | 4253 (2792) | none | - | +0.51R | -0.40R | -0.00 / -0.10 |
| P04-MACD-SUPERTREND-V5 | 1h | FAILED | 2387 (1631) | htf_conflict, false_breakout, regime_mismatch, indicator_lag | regime_mismatch 57%, false_breakout 40%, indicator_lag 35% | +0.45R | -0.42R | +0.01 / -0.10 |
| rsi2_dip_buy | 4h | FAILED | 1422 (615) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 46% | +0.16R | -0.21R | -0.05 / -0.10 |
| P04-MACD-SUPERTREND-V5 | 30m | FAILED | 3360 (2253) | false_breakout, regime_mismatch, indicator_lag | false_breakout 34%, regime_mismatch 33%, indicator_lag 33% | +0.48R | -0.42R | +0.06 / -0.11 |
| TRD-H4-PULLBACK-noT4 | 5m | FAILED | 6288 (3992) | overextended_entry | - | +0.51R | -0.43R | +0.04 / -0.11 |
| P07-SQUEEZE-RETEST-V2 | 30m | FAILED | 854 (580) | false_breakout | false_breakout 52% | +0.44R | -0.37R | +0.07 / -0.11 |
| P02-EMA-PULLBACK-V5 | 1h | FAILED | 4852 (3391) | low_relative_volume, regime_mismatch, indicator_lag | regime_mismatch 84%, indicator_lag 38% | +0.40R | -0.41R | +0.04 / -0.11 |
| rsi2_dip_buy | 1h | FAILED | 5262 (2344) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 43% | +0.15R | -0.21R | +0.00 / -0.11 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 608 (409) | range_market, stop_too_tight | range_market 47%, stop_too_tight 36% | +0.59R | -0.50R | +0.10 / -0.12 |
| trend_pullback | 1h | FAILED | 4793 (2548) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 77%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.43R | +0.02 / -0.12 |
| TRD-H4-BREAKOUT-noT4 | 5m | FAILED | 3759 (2438) | false_breakout | false_breakout 73% | +0.48R | -0.44R | +0.04 / -0.12 |
| P03-FIB-PULLBACK-V5 | 1h | FAILED | 5109 (3393) | regime_mismatch, indicator_lag | regime_mismatch 69%, indicator_lag 35% | +0.42R | -0.46R | +0.03 / -0.12 |
| P05-RANGE-REVERSAL-V3 | 4h | FAILED | 75 (36) | regime_mismatch | regime_mismatch 58%, htf_conflict 39% | +0.34R | -0.40R | -0.05 / -0.13 |
| ema_9_21_cross | 1h | FAILED | 270 (153) | regime_mismatch, indicator_lag | regime_mismatch 81%, indicator_lag 48% | +0.26R | -0.35R | +0.00 / -0.13 |
| P08-SESSION-BREAKOUT-V2 | 30m | FAILED | 707 (455) | late_entry, false_breakout | false_breakout 62%, late_entry 29% | +0.44R | -0.47R | +0.06 / -0.13 |
| PB-B-SWEEP-LIMIT | 5m | FAILED | 215 (131) | none | - | +0.23R | -0.21R | +0.05 / -0.13 |
| P04-MACD-SUPERTREND-V5 | 15m | FAILED | 5024 (3371) | range_market, false_breakout, indicator_lag | indicator_lag 35% | +0.45R | -0.45R | +0.10 / -0.14 |
| P02-EMA-PULLBACK-V2 | 30m | FAILED | 1692 (1180) | range_market, low_relative_volume, indicator_lag | low_relative_volume 59%, indicator_lag 40%, range_market 37% | +0.37R | -0.40R | +0.09 / -0.14 |
| P05-RANGE-REVERSAL-V1 | 4h | FAILED | 385 (198) | regime_mismatch | regime_mismatch 42% | +0.32R | -0.40R | -0.05 / -0.14 |
| PB-B-APLUS | 5m | FAILED | 183 (116) | none | - | +0.20R | -0.28R | +0.04 / -0.14 |
| P03-FIB-PULLBACK-V2 | 30m | FAILED | 2812 (1840) | regime_mismatch, indicator_lag | indicator_lag 37% | +0.41R | -0.46R | +0.08 / -0.14 |
| P03-FIB-PULLBACK-V3 | 4h | FAILED | 87 (60) | indicator_lag | indicator_lag 32% | +0.49R | -0.42R | -0.07 / -0.14 |
| S6-OB-FVG-noSMC | 15m | FAILED | 95 (63) | none | stop_too_wide 89%, range_market 52% | +0.35R | -0.28R | +0.01 / -0.15 |
| R4-CLUC | 30m | FAILED | 240 (149) | none | - | +0.31R | -0.41R | -0.05 / -0.15 |
| P01-BREAKOUT-V5 | 15m | FAILED | 2971 (2032) | false_breakout | false_breakout 70% | +0.44R | -0.42R | +0.09 / -0.15 |
| PB-B-GRADED | 5m | FAILED | 901 (572) | none | - | +0.21R | -0.24R | +0.02 / -0.15 |
| liquidity_sweep_reversal | 1h | FAILED | 243 (127) | stop_too_tight | stop_too_tight 50% | +0.28R | -0.49R | +0.00 / -0.16 |
| P02-EMA-PULLBACK-V5 | 30m | FAILED | 3703 (2593) | range_market, low_relative_volume, indicator_lag | indicator_lag 40% | +0.37R | -0.42R | +0.09 / -0.16 |
| bb_squeeze_breakout | 30m | FAILED | 657 (345) | false_breakout, stop_too_tight | false_breakout 61%, stop_too_tight 36% | +0.27R | -0.46R | +0.07 / -0.17 |
| P07-SQUEEZE-RETEST-V5 | 30m | FAILED | 1947 (1351) | htf_conflict, false_breakout | false_breakout 51% | +0.43R | -0.39R | +0.03 / -0.17 |
| PB-B-GRADED | 15m | FAILED | 818 (495) | stop_too_tight | stop_too_tight 36% | +0.32R | -0.32R | -0.01 / -0.17 |
| rsi2_dip_buy | 30m | FAILED | 4637 (2391) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 32% | +0.16R | -0.20R | +0.01 / -0.17 |
| supertrend_flip | 30m | FAILED | 240 (132) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 44%, stop_too_tight 36%, indicator_lag 36%, late_entry 32% | +0.40R | -0.39R | -0.02 / -0.17 |
| trend_pullback | 30m | FAILED | 5641 (3032) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 30% | +0.28R | -0.43R | +0.02 / -0.18 |
| macd_trend_cross | 30m | FAILED | 441 (229) | stop_too_tight, indicator_lag | regime_mismatch 72%, indicator_lag 44%, stop_too_tight 37%, low_relative_volume 37% | +0.30R | -0.46R | +0.03 / -0.18 |
| TRD-H4-BREAKOUT-S3-FDISP | 5m | FAILED | 1001 (670) | false_breakout | false_breakout 72% | +0.49R | -0.50R | -0.04 / -0.18 |
| ema_9_21_cross | 30m | FAILED | 556 (325) | indicator_lag | indicator_lag 47% | +0.27R | -0.38R | +0.00 / -0.19 |
| P03-FIB-PULLBACK-V5 | 30m | FAILED | 6226 (4141) | range_market, regime_mismatch, indicator_lag | indicator_lag 38% | +0.40R | -0.47R | +0.06 / -0.19 |
| R4-CLUC | 15m | FAILED | 199 (130) | none | - | +0.38R | -0.31R | -0.07 / -0.19 |
| P08-SESSION-BREAKOUT-V5 | 30m | FAILED | 1622 (1074) | late_entry, false_breakout | false_breakout 58%, late_entry 27% | +0.42R | -0.46R | +0.02 / -0.19 |
| P06-VWAP-REVERSION-V2 | 1h | FAILED | 83 (47) | volatility_spike | trend_reversal 47%, regime_mismatch 47% | +0.22R | -0.21R | -0.06 / -0.20 |
| supertrend_flip | 1h | FAILED | 209 (115) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 71%, regime_mismatch 70%, stop_too_tight 36%, indicator_lag 32% | +0.39R | -0.37R | -0.11 / -0.21 |
| ema_9_21_cross | 15m | FAILED | 1530 (880) | stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 25% | +0.25R | -0.44R | +0.06 / -0.21 |
| P02-EMA-PULLBACK-V2 | 15m | FAILED | 3121 (2231) | range_market, htf_conflict, indicator_lag | range_market 47%, indicator_lag 43% | +0.34R | -0.39R | +0.11 / -0.21 |
| P08-SESSION-BREAKOUT-V2 | 15m | FAILED | 841 (565) | wrong_session, false_breakout | false_breakout 56%, wrong_session 39% | +0.40R | -0.47R | +0.05 / -0.22 |
| P07-SQUEEZE-RETEST-V2 | 15m | FAILED | 1686 (1191) | false_breakout | false_breakout 56% | +0.43R | -0.44R | +0.05 / -0.22 |
| P06-VWAP-REVERSION-V2 | 30m | FAILED | 937 (558) | regime_mismatch | regime_mismatch 37% | +0.30R | -0.34R | +0.00 / -0.23 |
| P05-RANGE-REVERSAL-V2 | 1h | FAILED | 1428 (774) | regime_mismatch, volatility_spike | regime_mismatch 43% | +0.27R | -0.38R | -0.08 / -0.23 |
| P03-FIB-PULLBACK-V2 | 15m | FAILED | 4763 (3163) | indicator_lag | indicator_lag 40% | +0.39R | -0.48R | +0.08 / -0.23 |
| rsi2_dip_buy | 15m | FAILED | 7426 (4460) | wrong_session, trend_reversal, regime_mismatch, volatility_spike, fees_slippage | fees_slippage 42% | +0.16R | -0.20R | +0.03 / -0.24 |
| trend_pullback | 15m | FAILED | 9622 (5309) | range_market, stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 30% | +0.27R | -0.43R | +0.04 / -0.25 |
| P07-SQUEEZE-RETEST-V5 | 15m | FAILED | 3732 (2661) | false_breakout | false_breakout 55% | +0.43R | -0.44R | +0.05 / -0.25 |
| P05-RANGE-REVERSAL-V2 | 30m | FAILED | 4268 (2299) | regime_mismatch, volatility_spike | - | +0.27R | -0.41R | -0.01 / -0.26 |
| P08-SESSION-BREAKOUT-V5 | 15m | FAILED | 1893 (1288) | false_breakout | false_breakout 52% | +0.42R | -0.48R | +0.04 / -0.26 |
| P02-EMA-PULLBACK-V3 | 4h | FAILED | 117 (90) | indicator_lag | indicator_lag 39% | +0.40R | -0.41R | -0.18 / -0.26 |
| P02-EMA-PULLBACK-V5 | 15m | FAILED | 6894 (4974) | range_market, wrong_session, indicator_lag | indicator_lag 45% | +0.32R | -0.40R | +0.10 / -0.26 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 200 (144) | stop_too_tight, sweep_continued | sweep_continued 98%, stop_too_tight 28% | +0.46R | -0.49R | +0.01 / -0.27 |
| P03-FIB-PULLBACK-V5 | 15m | FAILED | 10470 (7057) | indicator_lag | indicator_lag 40% | +0.38R | -0.48R | +0.07 / -0.28 |
| R4-BBRSI | 1h | FAILED | 995 (702) | none | - | +0.45R | -0.46R | -0.14 / -0.30 |
| bb_squeeze_breakout | 15m | FAILED | 1409 (802) | false_breakout, stop_too_tight | false_breakout 63%, stop_too_tight 36% | +0.30R | -0.47R | +0.02 / -0.31 |
| R4-BBRSI | 30m | FAILED | 2698 (1872) | none | - | +0.42R | -0.46R | -0.08 / -0.32 |
| P06-VWAP-REVERSION-V2 | 15m | FAILED | 3911 (2561) | none | - | +0.37R | -0.43R | +0.00 / -0.34 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 861 (617) | stop_too_tight | stop_too_tight 34% | +0.56R | -0.50R | -0.02 / -0.36 |
| P05-RANGE-REVERSAL-V2 | 15m | FAILED | 10548 (6105) | volatility_spike | - | +0.26R | -0.41R | -0.01 / -0.38 |
| liquidity_sweep_reversal | 30m | FAILED | 394 (232) | stop_too_tight | stop_too_tight 41% | +0.31R | -0.52R | -0.11 / -0.39 |
| liquidity_sweep_reversal | 15m | FAILED | 1439 (868) | stop_too_tight | stop_too_tight 40% | +0.29R | -0.48R | -0.01 / -0.46 |
| ema_9_21_cross | 5m | FAILED | 1658 (1064) | stop_too_tight, indicator_lag | indicator_lag 52%, stop_too_tight 30% | +0.21R | -0.44R | +0.02 / -0.49 |
| PB-B-SWEEP-15M | 15m | FAILED | 208 (129) | stop_too_tight | stop_too_tight 33%, low_relative_volume 26% | +0.22R | -0.44R | -0.02 / -0.53 |
| PB-B-SWEEP | 5m | FAILED | 886 (579) | stop_too_tight | stop_too_tight 35%, range_market 27% | +0.13R | -0.37R | +0.07 / -0.65 |
| liquidity_sweep_reversal | 5m | FAILED | 3254 (2195) | range_market, stop_too_tight | stop_too_tight 40% | +0.25R | -0.51R | +0.10 / -0.72 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `false_breakout` (systematic in 48 strategy/timeframe tests); `stop_too_tight` (systematic in 34 strategy/timeframe tests); `regime_mismatch` (systematic in 19 strategy/timeframe tests); `indicator_lag` (systematic in 19 strategy/timeframe tests); `trend_reversal` (systematic in 7 strategy/timeframe tests); `no_displacement` (systematic in 7 strategy/timeframe tests); `overextended_entry` (systematic in 5 strategy/timeframe tests); `volatility_spike` (systematic in 4 strategy/timeframe tests); `range_market` (systematic in 3 strategy/timeframe tests); `late_entry` (systematic in 3 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `low_relative_volume` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests); `wrong_session` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- BTC down -1.9% (2026-10-12 04:00 → 2026-10-12 17:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ETH up +1.6% (2026-10-11 14:00 → 2026-10-12 03:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ETH down -4.7% (2026-10-12 13:00 → 2026-10-13 01:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- SOL down -6.8% (2026-10-12 13:00 → 2026-10-13 01:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- XRP down -5.0% (2026-10-12 13:00 → 2026-10-13 01:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ZEC up +7.0% (2026-10-11 21:00 → 2026-10-12 05:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ZEC down -11.2% (2026-10-12 13:00 → 2026-10-13 01:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- SUI down -8.7% (2026-10-12 13:00 → 2026-10-13 01:00 UTC): identifiable: at least one strategy had a valid signal before the move
- BNB down -2.9% (2026-10-12 12:00 → 2026-10-13 01:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 166.6 KB | - | - |
| `memory/cleanup_log.md` | 0.5 KB | - | - |
| `memory/coin_notes.md` | 20.2 KB | 20 | 2026-10-11 00:29 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 16.8 KB | 38 | 2026-10-11 03:20 UTC |
| `memory/experiments.md` | 96.3 KB | 41 | 2026-10-13 15:30 UTC |
| `memory/failure_journal.md` | 7.3 KB | 7 | 2026-10-13 15:30 UTC |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 466.8 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 15.2 KB | 16 | 2026-10-11 04:00 UTC |
| `memory/market_regime_log.md` | 21.8 KB | - | - |
| `memory/missed_trades.md` | 77.3 KB | 93 | 2026-10-13 01:02 UTC |
| `memory/playbook.md` | 11.8 KB | - | - |
| `memory/research_sources.md` | 166.0 KB | 125 | 2026-10-13 15:30 UTC |
| `memory/smc_events.csv` | 1528.9 KB | - | - |
| `memory/smc_research.md` | 8.9 KB | 2 | 2026-10-11 04:00 UTC |
| `memory/strategy_lifecycle.md` | 50.9 KB | - | - |
| `memory/strategy_registry.csv` | 129.8 KB | - | - |
| `memory/trials.csv` | 25.1 KB | - | - |
| `memory/universe_log.md` | 31.4 KB | - | - |

**Reviews due** (review date passed; for the reviews): `missed_trades.md` LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00 (2026-10-02); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03); `missed_trades.md` SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells (2026-10-03); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03) … and 42 more
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 5 signals logged · 5 finished · 0 still open
- Win rate **0%**, average **-1.19R** per trade, total **-5.9R** (at 0.5% risk, +1R = +0.5% of account)

**Costs used in every backtest:** LONG and SHORT = OKX futures fees + funding (always charged, never received). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*