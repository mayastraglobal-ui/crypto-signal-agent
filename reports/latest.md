# Crypto Signal Report

**Updated:** 2026-10-09 01:19 Beijing time (2026-10-08 17:19 UTC) · data: Binance · 9 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 13.9 MB (GitHub) · large files of this run 5.0 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-08 17:19 UTC / 2026-10-09 01:19 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US CPI (Sep data) 2026-10-14 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.05% (limit 0.5%)
- All 9 coins passed every check on every timeframe.
- 68 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-08 17:19 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 1035 h since 2026-08-26 | +0.0062% | 1.65 | 0.97 | - |
| ETH | GOOD | okx | 1035 h since 2026-08-26 | +0.0034% | 2.35 | 1.02 | - |
| SOL | GOOD | okx | 1035 h since 2026-08-26 | -0.0020% | 2.28 | 0.90 | - |
| ZEC | GOOD | okx | 1035 h since 2026-08-26 | +0.0100% | 1.13 | 1.03 | - |
| XRP | GOOD | okx | 1035 h since 2026-08-26 | -0.0029% | 3.13 | 0.81 | - |
| BNB | GOOD | okx | 1035 h since 2026-08-26 | -0.0031% | 2.54 | 0.61 | - |
| SUI | GOOD | okx | 1035 h since 2026-08-26 | +0.0081% | 2.82 | 0.99 | - |
| UNI | GOOD | okx | 1035 h since 2026-08-26 | +0.0100% | 1.90 | 0.94 | - |
| ADA | GOOD | okx | 1022 h since 2026-08-27 | +0.0042% | 2.44 | 0.96 | - |

*Binance futures API: blocked from GitHub's servers (HTTP 451) - expected, not a problem. The main series (OKX) is complete; Binance research history comes from the data.binance.vision files.*

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **ZEC**, **XRP**, **BNB**, **SUI**
- **Research only** - backtested, never a signal: UNI, ADA
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** ENA - 7-day average volume $43M < $50M

| Not eligible | 24h volume | Why |
|---|---|---|
| PUMP | $70M | 7-day average volume $40M < $50M; order book too thin: $152k within 1% (need $250k) |
| AVAX | $64M | 7-day average volume $50M < $50M |
| MET | $53M | 7-day average volume $5M < $50M; suspended for the rest of the UTC day (moved more than ±25% earlier today); order book too thin: $43k within 1% (need $250k) |
| ENA | $53M | 7-day average volume $43M < $50M |

*Skipped by your exclusion lists:* DOGE, NEAR, RLUSD, USD1, USDC (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 477 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 5000 | 2017-08 | OK (300 candles) |
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
| BTC | down (LH/LL) | 83,283.3 / 82,227.6 | 0.23 | 2.42x | 1.54x | displacement_down, bull_engulf, bear_engulf, bear_reject, breakout_down |
| ETH | mixed (LH/HL) | 2,577.39 / 2,545.19 | 0.16 | 2.57x | 1.93x | displacement_down, bull_engulf, bear_engulf, breakout_down |
| SOL | down (LH/LL) | 115.86 / 114.22 | 0.06 | 2.38x | 1.61x | displacement_down, bull_engulf, breakout_down |
| ZEC | down (LH/LL) | 1,344.62 / 1,194.47 | 0.30 | 2.26x | 1.48x | displacement_down, bear_reject, breakout_down |
| XRP | down (LH/LL) | 1.4182 / 1.389 | 0.46 | 2.59x | 1.80x | displacement_down, breakout_down |
| BNB | down (LH/LL) | 771.88 / 762.39 | 0.10 | 3.78x | 1.77x | displacement_down, bear_engulf, breakout_down, retest_down |
| SUI | mixed (LH/HL) | 1.1408 / 1.1165 | 0.22 | 2.33x | 1.42x | displacement_down, bear_reject, breakout_down |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 433 | 48% | 34% | 27% | 80% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | displacement_down | 329 | 46% | 26% | 17% | 78% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1088 | 46% | 32% | 22% | 76% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | bear_engulf | 1245 | 41% | 27% | 17% | 80% | 46% | 30% | worse than chance | 0.08R |
| 4h | bull_reject | 812 | 43% | 30% | 21% | 77% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | bear_reject | 810 | 47% | 32% | 22% | 74% | 46% | 30% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 576 | 44% | 31% | 23% | 75% | 46% | 30% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bear | 634 | 45% | 29% | 19% | 80% | 46% | 30% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 257 | 46% | 30% | 22% | 82% | 46% | 32% | can't tell from chance | 0.08R |
| 4h | smc_bos_down | 201 | 47% | 32% | 20% | 73% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 82 | 51% | 34% | 27% | 83% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_choch_down | 78 | 40% | 21% | 12% | 81% | 46% | 30% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 600 | 46% | 29% | 23% | 76% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bear | 607 | 47% | 30% | 19% | 76% | 46% | 30% | can't tell from chance | 0.08R |
| 1h | displacement_up | 548 | 47% | 34% | 28% | 73% | 45% | 32% | can't tell from chance | 0.17R |
| 1h | displacement_down | 397 | 37% | 23% | 15% | 81% | 38% | 22% | can't tell from chance | 0.17R |
| 1h | bull_engulf | 1520 | 43% | 30% | 23% | 75% | 44% | 31% | can't tell from chance | 0.19R |
| 1h | bear_engulf | 1676 | 38% | 24% | 16% | 80% | 37% | 24% | can't tell from chance | 0.19R |
| 1h | bull_reject | 1247 | 43% | 30% | 23% | 76% | 45% | 31% | can't tell from chance | 0.18R |
| 1h | bear_reject | 1237 | 36% | 24% | 18% | 81% | 38% | 24% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bull | 570 | 44% | 28% | 20% | 76% | 45% | 31% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bear | 616 | 37% | 25% | 17% | 80% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 365 | 46% | 34% | 27% | 77% | 44% | 31% | can't tell from chance | 0.16R |
| 1h | smc_bos_down | 234 | 41% | 28% | 20% | 80% | 39% | 25% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 96 | 46% | 32% | 29% | 76% | 46% | 32% | can't tell from chance | 0.20R |
| 1h | smc_choch_down | 101 | 41% | 29% | 20% | 76% | 38% | 24% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 814 | 48% | 34% | 25% | 72% | 45% | 32% | can't tell from chance | 0.18R |
| 1h | smc_fvg_retrace_bear | 724 | 38% | 26% | 19% | 78% | 38% | 24% | can't tell from chance | 0.20R |
| 30m | displacement_up | 465 | 37% | 26% | 21% | 80% | 42% | 27% | worse than chance | 0.21R |
| 30m | displacement_down | 389 | 41% | 24% | 17% | 80% | 36% | 22% | can't tell from chance | 0.21R |
| 30m | bull_engulf | 1475 | 41% | 27% | 18% | 78% | 42% | 28% | can't tell from chance | 0.23R |
| 30m | bear_engulf | 1597 | 38% | 23% | 16% | 81% | 36% | 22% | can't tell from chance | 0.23R |
| 30m | bull_reject | 1185 | 44% | 28% | 19% | 76% | 42% | 27% | can't tell from chance | 0.23R |
| 30m | bear_reject | 1337 | 38% | 23% | 16% | 80% | 37% | 22% | can't tell from chance | 0.22R |
| 30m | smc_sweep_bull | 606 | 43% | 30% | 20% | 75% | 43% | 28% | can't tell from chance | 0.22R |
| 30m | smc_sweep_bear | 575 | 40% | 26% | 17% | 81% | 37% | 22% | can't tell from chance | 0.21R |
| 30m | smc_bos_up | 361 | 34% | 25% | 22% | 81% | 44% | 29% | worse than chance | 0.22R |
| 30m | smc_bos_down | 244 | 34% | 20% | 13% | 84% | 36% | 21% | can't tell from chance | 0.22R |
| 30m | smc_choch_up | 92 | 34% | 22% | 16% | 84% | 42% | 26% | can't tell from chance | 0.24R |
| 30m | smc_choch_down | 90 | 37% | 23% | 19% | 79% | 37% | 23% | can't tell from chance | 0.21R |
| 30m | smc_fvg_retrace_bull | 872 | 42% | 27% | 19% | 78% | 42% | 28% | can't tell from chance | 0.22R |
| 30m | smc_fvg_retrace_bear | 755 | 37% | 22% | 16% | 80% | 37% | 23% | can't tell from chance | 0.24R |
| 15m | displacement_up | 425 | 35% | 24% | 18% | 85% | 38% | 26% | can't tell from chance | 0.29R |
| 15m | displacement_down | 384 | 34% | 25% | 17% | 80% | 34% | 22% | can't tell from chance | 0.30R |
| 15m | bull_engulf | 1533 | 38% | 26% | 19% | 79% | 38% | 27% | can't tell from chance | 0.32R |
| 15m | bear_engulf | 1504 | 33% | 22% | 15% | 79% | 35% | 22% | can't tell from chance | 0.32R |
| 15m | bull_reject | 1178 | 39% | 29% | 20% | 77% | 38% | 27% | can't tell from chance | 0.34R |
| 15m | bear_reject | 1377 | 33% | 20% | 13% | 83% | 35% | 22% | can't tell from chance | 0.30R |
| 15m | smc_sweep_bull | 551 | 41% | 31% | 21% | 74% | 39% | 27% | can't tell from chance | 0.28R |
| 15m | smc_sweep_bear | 501 | 36% | 24% | 14% | 82% | 35% | 23% | can't tell from chance | 0.30R |
| 15m | smc_bos_up | 329 | 37% | 26% | 20% | 81% | 38% | 28% | can't tell from chance | 0.32R |
| 15m | smc_bos_down | 272 | 28% | 19% | 14% | 84% | 36% | 24% | worse than chance | 0.30R |
| 15m | smc_choch_up | 77 | 30% | 16% | 10% | 91% | 38% | 28% | can't tell from chance | 0.34R |
| 15m | smc_choch_down | 83 | 33% | 24% | 13% | 80% | 33% | 22% | can't tell from chance | 0.34R |
| 15m | smc_fvg_retrace_bull | 967 | 38% | 28% | 20% | 77% | 38% | 26% | can't tell from chance | 0.33R |
| 15m | smc_fvg_retrace_bear | 815 | 33% | 23% | 15% | 82% | 34% | 22% | can't tell from chance | 0.33R |
| 5m | displacement_up | 1028 | 28% | 19% | 14% | 89% | 30% | 20% | can't tell from chance | 0.56R |
| 5m | displacement_down | 1086 | 25% | 18% | 13% | 85% | 29% | 20% | worse than chance | 0.52R |
| 5m | bull_engulf | 3862 | 28% | 18% | 13% | 84% | 29% | 19% | can't tell from chance | 0.58R |
| 5m | bear_engulf | 3730 | 29% | 20% | 14% | 82% | 29% | 19% | can't tell from chance | 0.61R |
| 5m | bull_reject | 2934 | 28% | 18% | 13% | 83% | 29% | 19% | can't tell from chance | 0.62R |
| 5m | bear_reject | 3368 | 29% | 20% | 13% | 82% | 29% | 20% | can't tell from chance | 0.59R |
| 5m | smc_sweep_bull | 1150 | 31% | 19% | 13% | 82% | 30% | 20% | can't tell from chance | 0.50R |
| 5m | smc_sweep_bear | 1060 | 32% | 23% | 15% | 82% | 31% | 21% | can't tell from chance | 0.51R |
| 5m | smc_bos_up | 682 | 27% | 19% | 14% | 88% | 28% | 19% | can't tell from chance | 0.66R |
| 5m | smc_bos_down | 829 | 25% | 17% | 13% | 86% | 30% | 20% | worse than chance | 0.55R |
| 5m | smc_choch_up | 194 | 32% | 21% | 16% | 85% | 30% | 21% | can't tell from chance | 0.62R |
| 5m | smc_choch_down | 197 | 24% | 15% | 11% | 88% | 29% | 19% | can't tell from chance | 0.52R |
| 5m | smc_fvg_retrace_bull | 3111 | 28% | 19% | 14% | 83% | 28% | 19% | can't tell from chance | 0.64R |
| 5m | smc_fvg_retrace_bear | 2785 | 26% | 19% | 12% | 82% | 28% | 19% | worse than chance | 0.62R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (strong) | WEAK_BULL (moderate) | TRANSITION (weak) | STRONG_BEAR (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H STRONG_BEAR)) |
| **ETH** | WEAK_BULL (weak) | WEAK_BULL (moderate) | EXPANSION down (moderate) | EXPANSION down (moderate) | SHORT allowed (4H/1H bearish, 1W WEAK_BULL) |
| **SOL** | WEAK_BULL (moderate) | WEAK_BULL (weak) | TRANSITION (weak) | EXPANSION down (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H EXPANSION)) |
| **ZEC** | WEAK_BULL (weak) | WEAK_BULL (weak) | RANGE (moderate) | EXPANSION down (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H EXPANSION)) |
| **XRP** | TRANSITION (weak) | WEAK_BULL (weak) | TRANSITION (weak) | EXPANSION down (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H EXPANSION)) |
| **BNB** | WEAK_BULL (weak) | WEAK_BULL (moderate) | TRANSITION (weak) | EXPANSION down (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H EXPANSION)) |
| **SUI** | UNCLEAR (weak) | TRANSITION (weak) | UNCLEAR (weak) | EXPANSION down (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H EXPANSION)) |
| **UNI** | EXPANSION up (moderate) | WEAK_BULL (weak) | EXPANSION down (weak) | STRONG_BEAR (moderate) | SHORT allowed (4H/1H bearish, 1W EXPANSION) |
| **ADA** | UNCLEAR (weak) | TRANSITION (weak) | UNCLEAR (weak) | STRONG_BEAR (strong) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H STRONG_BEAR)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.8 ATR in 10 candles); swing structure down (LH/LL); ADX 28 = strong trend; candle size 0.71x normal, Bollinger width above 62% of the last 100 candles · against: -
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.1 ATR in 10 candles); ADX 42 = strong trend; candle size 1.00x normal, Bollinger width above 38% of the last 100 candles; volume 0.78x normal · against: swing structure mixed (neutral)
- **4H TRANSITION (weak)** - for: ADX 31 = strong trend; candle size 1.04x normal, Bollinger width above 85% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.7 ATR in 10 candles); swing structure mixed
- **1H STRONG_BEAR (moderate)** - for: close below EMA-fast below EMA-slow; EMA-fast falling (-1.0 ATR in 10 candles); swing structure down (LH/LL); ADX 51 = strong trend; volume 2.47x normal · against: candle size 1.54x normal, Bollinger width above 84% of the last 100 candles (unusually wild for a trend)

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (CHOCH 7 candles ago) | sell-side (bullish idea) 0 candles ago | bear 81,537.04-82,163.10 | bear 85,550.00-86,378.24 | below the range (-121%) | swing high 83,283.28 (4.1 ATR) | swing low 80,579.43 (0.66 ATR) |
| **ETH** | down (BOS 7 candles ago) | sell-side (bullish idea) 6 candles ago | bear 2,468.88-2,509.26 | bear 2,690.78-2,700.54 | below the range (-400%) | swing high 2,577.39 (6.52 ATR) | swing low 2,369.11 (1.92 ATR) |
| **SOL** | down (BOS 8 candles ago) | sell-side (bullish idea) 0 candles ago | bear 108.00-108.37 | bear 120.13-121.29 | below the range (-398%) | swing high 115.86 (6.76 ATR) | swing low 107.40 (0.24 ATR) |
| **ZEC** | down (CHOCH 8 candles ago) | sell-side (bullish idea) 26 candles ago | bear 1,148.00-1,159.87 (retraced) | bear 1,302.50-1,348.00 | below the range (-44%) | swing high 1,344.62 (7.73 ATR) | swing low 1,101.93 (0.92 ATR) |
| **XRP** | down (BOS 8 candles ago) | sell-side (bullish idea) 14 candles ago | bear 1.3463-1.3503 | bull 1.2202-1.3441 | below the range (-154%) | swing high 1.4182 (4.3 ATR) | swing low 1.3163 (1.61 ATR) |
| **BNB** | down (BOS 8 candles ago) | sell-side (bullish idea) 7 candles ago | bear 725.47-729.20 | bear 768.61-773.99 | below the range (-397%) | swing high 771.88 (7.66 ATR) | swing low 720.89 (0.62 ATR) |
| **SUI** | down (CHOCH 8 candles ago) | sell-side (bullish idea) 0 candles ago | bear 1.0275-1.0336 | bear 1.1264-1.1468 | below the range (-377%) | swing high 1.1408 (5.58 ATR) | swing low 1.0056 (0.93 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **SIDEWAYS**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 64 (Greed), yesterday 71  (extreme fear/greed = bigger, faster moves)

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
- **Event calendar (next 7 days):** US CPI (Sep data) 2026-10-14 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-10-08 00:58 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PB-C-BREAKOUT-W20 | 1.0 | 5m | **BACKTESTING** | 1 | 100.0 | +0.351 | 99.0 | 0.0R | +0.35 / +0.00 | +0.35 / +0.00 | 0/5 ✗ | +0.30 | +0.25 | stable | 0 | 0.85R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | not cost-viable: fees + slippage 0.85R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1042 | 40.2 | +0.210 | 1.39 | 24.4R | +0.21 / +0.21 | +0.22 / +0.20 | 5/5 | +0.18 | +0.16 | stable | 9 | 0.04R | 3, -1.05 (-1.05 / -1.04) | 89 / 50 of 244 | 0 | max drawdown 24.4R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1187 | 39.6 | +0.206 | 1.37 | 22.0R | +0.21 / +0.19 | +0.20 / +0.21 | 5/5 | +0.18 | +0.15 | stable | 9 | 0.04R | 4, -1.04 (-1.04 / -1.04) | 153 / 63 of 333 | 0 | max drawdown 22.0R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 4h | **BACKTESTING** | 861 | 39.6 | +0.196 | 1.36 | 19.5R | +0.20 / +0.19 | +0.17 / +0.22 | 5/5 | +0.17 | +0.15 | stable | 8 | 0.03R | 3, -1.03 (-1.03 / -1.04) | 103 / 43 of 240 | 0 | max drawdown 19.5R |
| TRD-H4-BREAKOUT | 1.0 | 30m | **BACKTESTING** | 445 | 40.7 | +0.141 | 1.22 | 21.1R | +0.08 / +0.32 | +0.22 / +0.06 | 4/5 | +0.13 | +0.10 | stable | 7 | 0.06R | 4, +1.04 (+1.74 / -1.05) | 9 / 9 of 84 | 0 | max drawdown 21.1R |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1070 | 54.3 | +0.127 | 1.29 | 20.2R | +0.12 / +0.14 | +0.12 / +0.14 | 5/5 | +0.10 | +0.08 | stable | 7 | 0.04R | 4, -0.69 (-0.57 / -1.04) | 89 / 50 of 244 | 0 | max drawdown 20.2R |
| TRD-H4-BREAKOUT | 1.0 | 1h | **BACKTESTING** | 1024 | 38.4 | +0.112 | 1.18 | 50.8R | +0.04 / +0.25 | +0.17 / +0.05 | 4/5 | +0.09 | +0.07 | stable | 7 | 0.04R | 3, +0.09 (+0.09 / +0.00) | 6 / 2 of 93 | 0 | profit factor 1.18; max drawdown 50.8R |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 6 | 33.3 | +0.051 | 1.07 | 4.6R | -0.39 / +2.24 | +1.21 / -1.11 | 0/5 ✗ | -0.02 | -37.79 | stable | 0 | 0.15R | 0, +0.00 (+0.00 / +0.00) | 14 / 4 of 20 | 0 | only 6 trades; avg +0.05R/trade (needs +0.10R); profit factor 1.07; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 15m | **BACKTESTING** | 1161 | 39.7 | +0.049 | 1.08 | 75.0R | -0.02 / +0.27 | +0.03 / +0.07 | 3/5 | +0.03 | +0.01 | stable | 5 | 0.08R | 16, +0.20 (+0.24 / -0.07) | 51 / 41 of 379 | 0 | avg +0.05R/trade (needs +0.10R); profit factor 1.08; max drawdown 75.0R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 1h | **BACKTESTING** | 1015 | 38.3 | +0.040 | 1.07 | 40.4R | +0.06 / +0.00 | -0.04 / +0.13 | 3/5 | +0.02 | -0.01 | stable | 5 | 0.04R | 3, +0.10 (+0.68 / -1.05) | 25 / 26 of 190 | 0 | avg +0.04R/trade (needs +0.10R); profit factor 1.07; max drawdown 40.4R |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 1h | **BACKTESTING** | 3341 | 37.3 | +0.040 | 1.06 | 88.2R | +0.03 / +0.07 | +0.09 / -0.02 | 4/5 | +0.02 | -0.01 | stable | 5 | 0.04R | 18, -0.31 (-0.69 / +0.66) | 157 / 524 of 918 | 0 | avg +0.04R/trade (needs +0.10R); profit factor 1.06; max drawdown 88.2R |
| bb_squeeze_breakout | 1.0 | 1h | **BACKTESTING** | 799 | 52.8 | +0.011 | 1.02 | 29.8R | +0.01 / +0.02 | -0.01 / +0.03 | 2/5 ✗ | -0.06 | -0.12 | ✗  bb_k 2→1: -0.02R | 5 | 0.12R | 5, +0.16 (+0.34 / -0.12) | 137 / 31 of 202 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.02; max drawdown 29.8R |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 4 of 11 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 4 of 11 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-noCVD | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 11, -0.44 (-0.44 / +0.00) | 0 / 0 of 48 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT-noCVD | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 22 | 36.4 | -0.005 | 0.99 | 11.3R | -0.80 / +1.39 | +0.88 / -0.42 | 1/5 ✗ | -0.90 | -13.25 | ✗  stop buffer_atr 0.2→0.24: -0.40R | 1 | 0.17R | 0, +0.00 (+0.00 / +0.00) | 42 / 11 of 61 | 0 | only 22 trades; avg -0.00R/trade (needs +0.10R); profit factor 0.99; max drawdown 11.3R; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-CVD | 1.0 | 5m | **BACKTESTING** | 12 | 50.0 | -0.013 | 0.98 | 4.8R | +0.09 / -1.10 | +0.42 / -0.16 | 0/5 ✗ | -0.11 | +0.53 | ✗  stop buffer_atr 0.0→0.0: -0.01R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 12 trades; avg -0.01R/trade (needs +0.15R); profit factor 0.98; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK | 1.0 | 5m | **BACKTESTING** | 15 | 46.7 | -0.137 | 0.78 | 6.7R | -0.07 / -1.10 | +0.43 / -0.34 | 0/5 ✗ | -0.20 | +0.27 | ✗  stop buffer_atr 0.0→0.0: -0.14R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 15 trades; avg -0.14R/trade (needs +0.15R); profit factor 0.78; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-APLUS | 1.0 | 5m | **BACKTESTING** | 71 | 42.3 | -0.181 | 0.7 | 18.4R | -0.18 / -0.18 | +0.07 / -0.35 | 0/5 ✗ | -0.24 | -0.37 | ✗  time_stop_bars 48→38: -0.20R | 3 | 0.18R | 1, +1.53 (+0.00 / +1.53) | 0 / 0 of 1 | 0 | only 71 trades; avg -0.18R/trade (needs +0.15R); profit factor 0.70; max drawdown 18.4R; not profitable in BOTH train and unseen test |
| PB-A-GRADED | 1.0 | 5m | **BACKTESTING** | 89 | 43.8 | -0.183 | 0.69 | 20.8R | -0.18 / -0.18 | -0.03 / -0.27 | 1/5 ✗ | -0.26 | -0.37 | ✗  time_stop_bars 48→38: -0.20R | 2 | 0.18R | 1, +1.53 (+0.00 / +1.53) | 0 / 0 of 1 | 0 | only 89 trades; avg -0.18R/trade (needs +0.15R); profit factor 0.69; max drawdown 20.8R; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 13 | 38.5 | -0.202 | 0.81 | 9.3R | +0.14 / -4.33 | -0.70 / +0.11 | 1/5 ✗ | -0.33 | -0.53 | ✗  stop buffer_atr 0.2→0.16: -2.45R | 0 | 0.24R | 0, +0.00 (+0.00 / +0.00) | 44 / 8 of 59 | 0 | only 13 trades; avg -0.20R/trade (needs +0.10R); profit factor 0.81; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 3 | 33.3 | -0.266 | 0.65 | 1.2R | -0.27 / +0.00 | -1.22 / +0.21 | 0/5 ✗ | -0.35 | -1.12 | ✗  stop buffer_atr 0.2→0.24: -0.27R | 0 | 0.26R | 0, +0.00 (+0.00 / +0.00) | 44 / 8 of 59 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 3 trades; avg -0.27R/trade (needs +0.10R); profit factor 0.65; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 6 | 33.3 | -0.328 | 0.62 | 3.2R | +1.21 / -0.64 | -0.50 / +0.03 | 0/5 ✗ | -0.47 | -0.58 | ✗  stop buffer_atr 0.2→0.24: -0.53R | 0 | 0.27R | 1, +1.97 (+1.97 / +0.00) | 34 / 105 of 148 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 6 trades; avg -0.33R/trade (needs +0.10R); profit factor 0.62; only 5 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-LDN | 1.0 | 5m | **BACKTESTING** | 27 | 40.7 | -0.368 | 0.5 | 15.7R | -0.22 / -0.88 | -0.11 / -0.50 | 0/5 ✗ | -0.44 | -0.49 | ✗  stop buffer_atr 0.0→0.0: -0.37R | 2 | 0.23R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 27 trades; avg -0.37R/trade (needs +0.15R); profit factor 0.50; max drawdown 15.7R; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 13 | 30.8 | -0.383 | 0.39 | 6.0R | -0.29 / -0.44 | -0.38 / -0.38 | 0/5 ✗ | -0.56 | -0.50 | ✗  stop buffer_atr 0.2→0.24: -0.49R | 0 | 0.12R | 0, +0.00 (+0.00 / +0.00) | 481 / 187 of 773 | 0 | only 13 trades; avg -0.38R/trade (needs +0.10R); profit factor 0.39; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-GRADED | 1.0 | 5m | **BACKTESTING** | 11 | 27.3 | -0.566 | 0.3 | 7.9R | -0.43 / -1.16 | -0.75 / -0.08 | 0/5 ✗ | +0.32 | +0.21 | ✗  stop buffer_atr 0.0→0.0: -0.57R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 2 | 0 | only 11 trades; avg -0.57R/trade (needs +0.15R); profit factor 0.30; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 8 | 12.5 | -0.570 | 0.45 | 5.8R | -0.37 / -1.17 | -1.22 / -0.35 | 0/5 ✗ | -0.55 | -0.63 | ✗  stop max_width_atr 3.0→3.6: -0.58R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 61 / 16 of 79 | 0 | only 8 trades; avg -0.57R/trade (needs +0.10R); profit factor 0.45; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-APLUS | 1.0 | 5m | **BACKTESTING** | 1 | 0.0 | -0.641 | 0.0 | 0.6R | -0.64 / +0.00 | -0.64 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: -0.64R | 0 | 0.23R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 1 trades; avg -0.64R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 1 | 0.0 | -1.059 | 0.0 | 1.1R | -1.06 / +0.00 | +0.00 / -1.06 | 0/5 ✗ | -1.09 | -1.12 | ✗  stop buffer_atr 0.2→0.16: -1.06R | 0 | 0.07R | 0, +0.00 (+0.00 / +0.00) | 14 / 4 of 20 | 0 | only 1 trades; avg -1.06R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.208 | 0.0 | 1.2R | -1.21 / +0.00 | -1.21 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.2→0.16: -1.21R | 0 | 0.27R | 0, +0.00 (+0.00 / +0.00) | 61 / 16 of 79 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.21R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **FAILED** | 33 | 54.5 | +0.415 | 1.91 | 3.7R | +0.73 / -0.32 | +0.81 / +0.04 | 2/5 ✗ | +0.41 | +0.38 | stable | 2 | 0.15R | 0, +0.00 (+0.00 / +0.00) | 475 / 170 of 744 | 0 | not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 266 | 51.1 | +0.026 | 1.05 | 28.0R | +0.18 / -0.26 | +0.16 / -0.09 | 2/5 ✗ | -0.01 | -0.05 | ✗  stop atr 1.5→1.8: -0.01R | 5 | 0.06R | 1, -1.04 (-1.04 / +0.00) | 106 / 23 of 144 | 0 | avg +0.03R/trade (needs +0.10R); profit factor 1.05; max drawdown 28.0R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 30m | **FAILED** | 618 | 36.1 | -0.008 | 0.99 | 72.4R | -0.05 / +0.13 | -0.03 / +0.01 | 3/5 | -0.02 | -0.02 | ✗  time_stop_bars 48→38: -0.03R | 4 | 0.06R | 5, +0.95 (+0.95 / +0.95) | 32 / 26 of 255 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; max drawdown 72.4R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 30m | **FAILED** | 1457 | 36.7 | -0.009 | 0.99 | 88.9R | -0.04 / +0.09 | +0.05 / -0.07 | 2/5 ✗ | -0.04 | -0.07 | ✗  stop atr 2.0→1.6: -0.03R | 5 | 0.07R | 24, -0.14 (-0.22 / +0.10) | 121 / 549 of 883 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; max drawdown 88.9R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 1h | **FAILED** | 2414 | 33.1 | -0.010 | 0.98 | 159.9R | -0.04 / +0.06 | +0.03 / -0.05 | 2/5 ✗ | -0.05 | -0.09 | ✗  stop atr 2.0→1.6: -0.03R | 4 | 0.07R | 6, +0.51 (+0.12 / +0.91) | 144 / 100 of 383 | 0 | avg -0.01R/trade (needs +0.12R); profit factor 0.98; max drawdown 159.9R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 3240 | 33.2 | -0.012 | 0.98 | 192.4R | -0.03 / +0.03 | +0.03 / -0.06 | 3/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.04R | 4 | 0.07R | 12, -0.16 (-0.59 / +0.44) | 202 / 130 of 521 | 0 | avg -0.01R/trade (needs +0.12R); profit factor 0.98; max drawdown 192.4R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 1h | **FAILED** | 4759 | 37.4 | -0.014 | 0.98 | 214.0R | +0.00 / -0.06 | -0.04 / +0.01 | 1/5 ✗ | -0.04 | -0.08 | ✗  stop atr 2.0→1.6: -0.03R | 3 | 0.05R | 29, -0.09 (+0.04 / -0.71) | 620 / 2629 of 3666 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 214.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2862 | 32.8 | -0.015 | 0.98 | 164.0R | -0.05 / +0.05 | +0.02 / -0.05 | 2/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.05R | 5 | 0.07R | 8, -0.11 (-1.09 / +0.87) | 116 / 101 of 375 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.98; max drawdown 164.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 30m | **FAILED** | 1056 | 34.3 | -0.016 | 0.98 | 71.7R | -0.03 / +0.03 | +0.11 / -0.13 | 2/5 ✗ | -0.07 | -0.12 | ✗  stop atr 2.0→1.6: -0.05R | 3 | 0.10R | 14, -0.14 (-0.40 / +0.21) | 150 / 56 of 319 | 0 | avg -0.02R/trade (needs +0.12R); profit factor 0.98; max drawdown 71.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1140 | 34.2 | -0.021 | 0.97 | 85.7R | -0.04 / +0.03 | +0.08 / -0.12 | 2/5 ✗ | -0.08 | -0.14 | ✗  stop atr 2.0→1.6: -0.06R | 4 | 0.11R | 19, -0.24 (-0.47 / -0.04) | 122 / 66 of 330 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 85.7R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2944 | 48.9 | -0.024 | 0.95 | 114.9R | -0.04 / +0.00 | -0.01 / -0.03 | 1/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.07R | 8, -0.00 (-1.09 / +1.08) | 116 / 101 of 375 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.95; max drawdown 114.9R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1341 | 34.0 | -0.039 | 0.94 | 98.7R | -0.05 / -0.00 | +0.05 / -0.14 | 1/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.08R | 3 | 0.11R | 24, -0.14 (-0.20 / -0.04) | 214 / 85 of 461 | 0 | avg -0.04R/trade (needs +0.12R); profit factor 0.94; max drawdown 98.7R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 39 | 51.3 | -0.043 | 0.92 | 5.5R | +0.12 / -0.46 | +0.23 / -0.33 | 2/5 ✗ | -0.07 | -0.10 | ✗  stop atr 1.5→1.8: -0.07R | 2 | 0.06R | 1, +0.31 (+0.31 / +0.00) | 137 / 4 of 142 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.92; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1175 | 47.8 | -0.048 | 0.91 | 85.1R | -0.05 / -0.05 | +0.02 / -0.12 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.10R | 19, -0.30 (-0.42 / -0.19) | 122 / 66 of 330 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 85.1R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 89 | 47.2 | -0.052 | 0.9 | 13.7R | +0.08 / -0.29 | -0.10 / +0.01 | 3/5 ✗ | -0.07 | -0.10 | ✗  time_stop_bars 60→48: -0.05R | 2 | 0.04R | 1, -1.14 (-1.14 / +0.00) | 36 / 6 of 45 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.90; max drawdown 13.7R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 5m | **FAILED** | 2897 | 37.5 | -0.052 | 0.92 | 274.0R | -0.07 / +0.02 | -0.06 / -0.04 | 1/5 ✗ | -0.06 | -0.12 | ✗  time_stop_bars 48→38: -0.06R | 1 | 0.12R | 43, -0.26 (-0.23 / -0.44) | 101 / 86 of 703 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 274.0R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 70 | 41.4 | -0.053 | 0.91 | 9.3R | -0.10 / +0.06 | +0.01 / -0.19 | 3/5 | -0.13 | -0.13 | ✗  time_stop_bars 30→24: -0.09R | 5 | 0.11R | 2, -1.24 (-1.24 / +0.00) | 108 / 34 of 156 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 181 | 49.7 | -0.054 | 0.9 | 31.8R | -0.16 / +0.17 | -0.03 / -0.07 | 2/5 ✗ | -0.10 | -0.16 | ✗  stop atr 1.5→1.2: -0.12R | 3 | 0.11R | 0, +0.00 (+0.00 / +0.00) | 205 / 7 of 214 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.90; max drawdown 31.8R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 15m | **FAILED** | 793 | 34.3 | -0.054 | 0.92 | 57.5R | -0.04 / -0.09 | -0.01 / -0.10 | 2/5 ✗ | -0.07 | -0.13 | ✗  stop atr 2.0→1.6: -0.08R | 3 | 0.08R | 11, -0.62 (-0.52 / -1.09) | 12 / 15 of 115 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 57.5R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 15m | **FAILED** | 4142 | 36.6 | -0.064 | 0.9 | 345.2R | -0.07 / -0.04 | -0.04 / -0.08 | 1/5 ✗ | -0.10 | -0.13 | ✗  time_stop_bars 48→58: -0.07R | 1 | 0.10R | 69, -0.24 (-0.13 / -0.74) | 503 / 2654 of 3764 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.90; max drawdown 345.2R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1188 | 47.6 | -0.068 | 0.87 | 125.0R | -0.03 / -0.15 | +0.01 / -0.15 | 1/5 ✗ | -0.11 | -0.14 | ✗  long_rsi_hi 65→52: -0.16R | 2 | 0.05R | 14, -0.41 (-0.36 / -1.04) | 623 / 181 of 962 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; max drawdown 125.0R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 30m | **FAILED** | 2346 | 34.9 | -0.069 | 0.9 | 198.6R | -0.05 / -0.12 | -0.04 / -0.10 | 1/5 ✗ | -0.10 | -0.14 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.07R | 46, -0.18 (-0.07 / -0.55) | 489 / 2578 of 3595 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.90; max drawdown 198.6R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 277 | 33.9 | -0.071 | 0.9 | 51.3R | +0.02 / -0.27 | -0.26 / +0.13 | 1/5 ✗ | -0.16 | -0.25 | ✗  time_stop_bars 30→36: -0.10R | 4 | 0.16R | 4, +1.28 (+1.28 / +0.00) | 78 / 207 of 295 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.90; max drawdown 51.3R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 15m | **FAILED** | 2541 | 33.6 | -0.090 | 0.87 | 269.6R | -0.10 / -0.07 | -0.04 / -0.14 | 0/5 ✗ | -0.13 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 1 | 0.10R | 43, -0.44 (-0.35 / -0.77) | 109 / 616 of 922 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.87; max drawdown 269.6R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 5m | **FAILED** | 1787 | 35.5 | -0.097 | 0.86 | 204.3R | -0.12 / -0.03 | -0.04 / -0.14 | 1/5 ✗ | -0.16 | -0.20 | ✗  stop atr 2.0→1.6: -0.11R | 3 | 0.13R | 22, +0.16 (+0.18 / +0.05) | 19 / 18 of 167 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.86; max drawdown 204.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1796 | 56.6 | -0.099 | 0.65 | 178.3R | -0.10 / -0.10 | -0.11 / -0.09 | 0/5 ✗ | -0.12 | -0.15 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.04R | 13, -0.37 (+0.21 / -1.04) | 696 / 6 of 926 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.65; max drawdown 178.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 6765 | 55.9 | -0.106 | 0.61 | 728.8R | -0.09 / -0.14 | -0.10 / -0.12 | 0/5 ✗ | -0.16 | -0.21 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.09R | 36, -0.07 (-0.03 / -0.20) | 913 / 12 of 1236 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.61; max drawdown 728.8R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 5m | **FAILED** | 8701 | 36.3 | -0.112 | 0.84 | 987.5R | -0.12 / -0.09 | -0.10 / -0.12 | 0/5 ✗ | -0.15 | -0.16 | ✗  time_stop_bars 48→38: -0.12R | 0 | 0.15R | 119, -0.34 (-0.43 / +0.14) | 1266 / 7119 of 9739 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.84; max drawdown 987.5R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 195 | 41.0 | -0.112 | 0.82 | 42.3R | -0.18 / +0.18 | +0.13 / -0.29 | 2/5 ✗ | -0.17 | -0.22 | ✗  bb_k 2→3: -0.28R | 2 | 0.10R | 4, +0.50 (+1.02 / -1.07) | 83 / 7 of 96 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.82; max drawdown 42.3R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6141 | 46.9 | -0.117 | 0.79 | 745.8R | -0.12 / -0.10 | -0.13 / -0.10 | 0/5 ✗ | -0.17 | -0.23 | ✗  stop atr 1.5→1.2: -0.15R | 0 | 0.11R | 30, -0.09 (-0.10 / -0.08) | 1087 / 251 of 1680 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.79; max drawdown 745.8R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 327 | 43.4 | -0.117 | 0.78 | 48.1R | -0.14 / -0.07 | -0.17 / -0.07 | 0/5 ✗ | -0.17 | -0.23 | ✗  slow 21→17: -0.21R | 3 | 0.10R | 1, -1.18 (+0.00 / -1.18) | 117 / 6 of 130 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.78; max drawdown 48.1R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 5m | **FAILED** | 5098 | 34.7 | -0.125 | 0.83 | 666.9R | -0.14 / -0.09 | -0.09 / -0.16 | 0/5 ✗ | -0.17 | -0.18 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.15R | 61, -0.23 (-0.24 / -0.16) | 282 / 1677 of 2320 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.83; max drawdown 666.9R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 483 | 47.8 | -0.146 | 0.76 | 74.5R | -0.17 / -0.09 | -0.09 / -0.20 | 2/5 ✗ | -0.24 | -0.35 | ✗  stop atr 1.5→1.2: -0.21R | 2 | 0.18R | 11, -0.06 (-0.16 / +1.00) | 95 / 35 of 173 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.76; max drawdown 74.5R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3166 | 47.3 | -0.152 | 0.74 | 487.1R | -0.14 / -0.19 | -0.13 / -0.17 | 0/5 ✗ | -0.25 | -0.33 | ✗  stop atr 1.5→1.2: -0.20R | 0 | 0.16R | 61, -0.40 (-0.43 / -0.35) | 772 / 241 of 1476 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.74; max drawdown 487.1R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 266 | 47.7 | -0.154 | 0.74 | 52.2R | -0.09 / -0.35 | -0.19 / -0.12 | 1/5 ✗ | -0.25 | -0.33 | ✗  stop atr 1.5→1.2: -0.19R | 2 | 0.18R | 4, -0.49 (-0.53 / -0.45) | 147 / 8 of 167 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.74; max drawdown 52.2R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2552 | 49.7 | -0.158 | 0.47 | 404.7R | -0.14 / -0.21 | -0.17 / -0.15 | 0/5 ✗ | -0.24 | -0.33 | ✗  stop atr 2.0→1.6: -0.21R | 0 | 0.14R | 44, -0.27 (-0.26 / -0.33) | 954 / 36 of 1156 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.47; max drawdown 404.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 760 | 31.4 | -0.158 | 0.8 | 158.0R | -0.15 / -0.17 | -0.15 / -0.17 | 1/5 ✗ | -0.25 | -0.33 | ✗  stop buffer_atr 0.2→0.16: -0.20R | 1 | 0.18R | 7, +0.18 (+0.28 / -0.07) | 389 / 1059 of 1524 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.80; max drawdown 158.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 314 | 42.7 | -0.165 | 0.71 | 54.7R | -0.12 / -0.31 | -0.21 / -0.13 | 2/5 ✗ | -0.26 | -0.33 | ✗  slow 21→25: -0.26R | 0 | 0.15R | 7, -0.94 (-1.08 / -0.91) | 89 / 24 of 133 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.71; max drawdown 54.7R; not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 5m | **FAILED** | 1268 | 36.4 | -0.169 | 0.63 | 216.5R | -0.20 / -0.07 | -0.21 / -0.13 | 0/5 ✗ | -0.21 | -0.21 | ✗  stop max_width_atr 3.0→2.4: -0.17R | 0 | 0.18R | 21, -0.07 (-0.01 / -1.23) | 0 / 0 of 394 | 0 | avg -0.17R/trade (needs +0.15R); profit factor 0.63; max drawdown 216.5R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-LIMIT | 1.0 | 5m | **FAILED** | 319 | 38.2 | -0.177 | 0.63 | 61.4R | -0.19 / -0.14 | -0.23 / -0.13 | 0/5 ✗ | -0.35 | -0.37 | ✗  stop buffer_atr 0.0→0.0: -0.18R | 2 | 0.19R | 4, -0.09 (-0.09 / +0.00) | 0 / 0 of 49 | 0 | avg -0.18R/trade (needs +0.15R); profit factor 0.63; max drawdown 61.4R; not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 15m | **FAILED** | 103 | 43.7 | -0.177 | 0.68 | 20.3R | -0.16 / -0.25 | -0.17 / -0.18 | 1/5 ✗ | -0.19 | -0.09 | ✗  stop buffer_atr 0.0→0.0: -0.18R | 3 | 0.18R | 3, -0.52 (-0.52 / +0.00) | 0 / 0 of 23 | 0 | avg -0.18R/trade (needs +0.15R); profit factor 0.68; max drawdown 20.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 280 | 47.5 | -0.178 | 0.7 | 54.4R | -0.21 / -0.10 | -0.16 / -0.20 | 0/5 ✗ | -0.24 | -0.30 | ✗  vol_x 1.2→1.44: -0.31R | 3 | 0.14R | 1, +1.11 (+0.00 / +1.11) | 79 / 177 of 264 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.70; max drawdown 54.4R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 809 | 44.4 | -0.183 | 0.69 | 150.8R | -0.19 / -0.15 | -0.23 / -0.14 | 0/5 ✗ | -0.30 | -0.42 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.21R | 9, -0.82 (-0.91 / -0.70) | 87 / 17 of 117 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.69; max drawdown 150.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 265 | 45.3 | -0.188 | 0.67 | 54.5R | -0.18 / -0.20 | -0.28 / -0.10 | 0/5 ✗ | -0.24 | -0.28 | ✗  stop atr 2.0→1.6: -0.22R | 2 | 0.08R | 1, +0.24 (+0.00 / +0.24) | 47 / 2 of 57 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.67; max drawdown 54.5R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 144 | 45.8 | -0.198 | 0.66 | 29.3R | -0.13 / -0.42 | -0.20 / -0.19 | 1/5 ✗ | -0.24 | -0.31 | ✗  adx_min 20→16: -0.21R | 0 | 0.12R | 4, -0.55 (-1.16 / -0.35) | 46 / 6 of 63 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.66; max drawdown 29.3R; not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 5m | **FAILED** | 265 | 35.5 | -0.201 | 0.6 | 57.6R | -0.21 / -0.17 | -0.24 / -0.16 | 0/5 ✗ | -0.32 | -0.28 | ✗  stop max_width_atr 3.0→2.4: -0.20R | 2 | 0.18R | 4, -0.09 (-0.09 / +0.00) | 0 / 0 of 41 | 0 | avg -0.20R/trade (needs +0.15R); profit factor 0.60; max drawdown 57.6R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 161 | 32.9 | -0.201 | 0.71 | 45.8R | -0.27 / +0.12 | -0.08 / -0.28 | 1/5 ✗ | -0.25 | -0.29 | ✗  depth 0.985→1.182: -0.35R | 1 | 0.11R | 6, -0.39 (-0.04 / -1.09) | 31 / 5 of 42 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.71; max drawdown 45.8R; not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 15m | **FAILED** | 500 | 37.6 | -0.219 | 0.61 | 113.9R | -0.23 / -0.20 | -0.20 / -0.24 | 0/5 ✗ | -0.20 | -0.23 | ✗  stop max_width_atr 3.0→2.4: -0.22R | 0 | 0.18R | 11, +0.16 (+0.16 / +0.00) | 0 / 0 of 242 | 0 | avg -0.22R/trade (needs +0.15R); profit factor 0.61; max drawdown 113.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 5369 | 45.7 | -0.220 | 0.66 | 1179.8R | -0.23 / -0.19 | -0.22 / -0.22 | 0/5 ✗ | -0.34 | -0.47 | ✗  stop atr 1.5→1.2: -0.29R | 0 | 0.22R | 93, -0.56 (-0.48 / -0.65) | 1394 / 295 of 2240 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.66; max drawdown 1179.8R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 4043 | 42.3 | -0.242 | 0.32 | 981.6R | -0.22 / -0.30 | -0.26 / -0.23 | 0/5 ✗ | -0.37 | -0.50 | ✗  stop atr 2.0→1.6: -0.31R | 0 | 0.21R | 112, -0.33 (-0.31 / -0.38) | 1021 / 49 of 1244 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.32; max drawdown 981.6R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 1082 | 45.0 | -0.288 | 0.57 | 312.2R | -0.28 / -0.32 | -0.26 / -0.32 | 0/5 ✗ | -0.42 | -0.54 | ✗  stop atr 1.5→1.2: -0.38R | 0 | 0.25R | 12, -0.22 (-0.25 / -0.11) | 99 / 42 of 178 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.29R/trade (needs +0.10R); profit factor 0.57; max drawdown 312.2R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1379 | 31.5 | -0.290 | 0.63 | 407.2R | -0.31 / -0.25 | -0.27 / -0.31 | 0/5 ✗ | -0.41 | -0.51 | ✗  stop atr 1.5→1.2: -0.33R | 0 | 0.18R | 34, -0.25 (+0.27 / -1.08) | 593 / 29 of 711 | 0 | avg -0.29R/trade (needs +0.10R); profit factor 0.63; max drawdown 407.2R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1242 | 28.7 | -0.300 | 0.62 | 372.5R | -0.33 / -0.23 | -0.28 / -0.32 | 0/5 ✗ | -0.37 | -0.43 | ✗  rsi_n 14→17: -0.40R | 1 | 0.12R | 9, -0.15 (+0.68 / -1.20) | 698 / 5 of 744 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.62; max drawdown 372.5R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 322 | 41.3 | -0.376 | 0.46 | 121.1R | -0.33 / -0.49 | -0.37 / -0.38 | 0/5 ✗ | -0.49 | -0.58 | ✗  vol_x 1.2→1.44: -0.42R | 1 | 0.23R | 6, -1.17 (-1.14 / -1.34) | 104 / 218 of 341 | 0 | avg -0.38R/trade (needs +0.10R); profit factor 0.46; max drawdown 121.1R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 114 | 21.9 | -0.419 | 0.55 | 48.8R | -0.27 / -0.74 | -0.65 / -0.13 | 1/5 ✗ | -0.52 | -0.63 | ✗  time_stop_bars 30→24: -0.46R | 1 | 0.22R | 4, +0.62 (+1.31 / -1.47) | 34 / 105 of 148 | 0 | avg -0.42R/trade (needs +0.10R); profit factor 0.55; max drawdown 48.8R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-15M | 1.0 | 15m | **FAILED** | 271 | 39.5 | -0.449 | 0.4 | 127.2R | -0.40 / -0.60 | -0.42 / -0.47 | 0/5 ✗ | -0.54 | -0.64 | ✗  time_stop_bars 16→13: -0.45R | 0 | 0.43R | 7, -0.86 (-0.86 / +0.00) | 0 / 0 of 30 | 0 | not cost-viable: fees + slippage 0.43R per trade (stop must be ≥ 4x the round-trip cost); avg -0.45R/trade (needs +0.15R); profit factor 0.40; max drawdown 127.2R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 523 | 26.4 | -0.452 | 0.5 | 236.3R | -0.41 / -0.56 | -0.45 / -0.45 | 0/5 ✗ | -0.60 | -0.70 | ✗  stop buffer_atr 0.2→0.16: -0.48R | 0 | 0.28R | 12, -0.59 (-0.50 / -0.71) | 413 / 1002 of 1572 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.45R/trade (needs +0.10R); profit factor 0.50; max drawdown 236.3R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 2111 | 36.4 | -0.469 | 0.41 | 990.9R | -0.46 / -0.48 | -0.49 / -0.45 | 0/5 ✗ | -0.69 | -0.91 | ✗  stop atr 1.5→1.2: -0.58R | 0 | 0.39R | 39, -0.69 (-0.34 / -1.24) | 200 / 55 of 303 | 0 | not cost-viable: fees + slippage 0.39R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R); profit factor 0.41; max drawdown 990.9R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 1139 | 39.3 | -0.471 | 0.4 | 536.9R | -0.44 / -0.57 | -0.43 / -0.52 | 0/5 ✗ | -0.66 | -0.87 | ✗  stop atr 1.0→0.8: -0.55R | 0 | 0.34R | 17, -0.72 (-0.46 / -1.56) | 88 / 259 of 375 | 0 | not cost-viable: fees + slippage 0.34R per trade (stop must be ≥ 4x the round-trip cost); avg -0.47R/trade (needs +0.10R); profit factor 0.40; max drawdown 536.9R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP | 1.0 | 5m | **FAILED** | 1190 | 34.3 | -0.630 | 0.25 | 750.3R | -0.65 / -0.57 | -0.62 / -0.64 | 0/5 ✗ | -0.77 | -0.86 | ✗  stop max_width_atr 3.0→2.4: -0.63R | 0 | 0.59R | 11, -0.44 (-0.44 / +0.00) | 0 / 0 of 49 | 0 | not cost-viable: fees + slippage 0.59R per trade (stop must be ≥ 4x the round-trip cost); avg -0.63R/trade (needs +0.15R); profit factor 0.25; max drawdown 750.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 4042 | 33.9 | -0.673 | 0.3 | 2719.8R | -0.66 / -0.71 | -0.68 / -0.66 | 0/5 ✗ | -1.05 | -1.42 | ✗  stop atr 1.0→0.8: -0.85R | 0 | 0.63R | 58, -0.94 (-0.80 / -1.34) | 207 / 607 of 902 | 0 | not cost-viable: fees + slippage 0.63R per trade (stop must be ≥ 4x the round-trip cost); avg -0.67R/trade (needs +0.10R); profit factor 0.30; max drawdown 2719.8R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **49** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 210 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.49** (Bonferroni: family-wise false-winner rate 0.05 over 210 trials; with 1 trial it would be 1.65).

**Research run duration:** 53.6 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 45 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (302.4 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 59 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

1 of 93 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 6.74 | 15.1R | 592 d (18%) | passes every gate |

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- PB-A-GRADED v1.0 5m = near-duplicate of PB-A-APLUS v1.0 5m (80% of 89 trades shared)

- PB-B-SWEEP-LIMIT v1.0 5m = near-duplicate of PB-B-APLUS v1.0 5m (78% of 319 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (80% of 3,240 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (76% of 1,341 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 1,187 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,862 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,140 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 1,042 trades shared)

🧪 **Strategy lab:** 5 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| TRD-H4-BREAKOUT | 30m | 445 | +0.141 | +0.321 | -0.009 | +0.086 | yes |
| TRD-H4-BREAKOUT | 1h | 1024 | +0.112 | +0.248 | +0.040 | +0.069 | yes |
| S7-SILVER-BULLET | 15m | 6 | +0.051 | +2.244 | -0.005 | +1.394 | too few trades to compare |
| TRD-H4-PULLBACK | 15m | 1161 | +0.049 | +0.271 | -0.064 | -0.040 | yes |
| TRD-H4-PULLBACK | 1h | 1015 | +0.040 | +0.002 | -0.014 | -0.056 | yes |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.053 | +0.061 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| PB-C-BREAKOUT | 5m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| PB-A-PULLBACK-CVD | 5m | 12 | -0.013 | -1.097 | -0.137 | -1.097 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 13 | -0.202 | -4.325 | +0.415 | -0.317 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 3 | -0.266 | +0.000 | -0.201 | -4.320 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 6 | -0.328 | -0.635 | -0.402 | -0.684 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 8 | -0.570 | -1.166 | -0.383 | -0.441 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 1 | -1.059 | +0.000 | +0.051 | +2.244 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 1 | -1.208 | +0.000 | -0.570 | -1.166 | too few trades to compare |
| TRD-H4-PULLBACK | 30m | 618 | -0.008 | +0.132 | -0.069 | -0.119 | yes |
| TRD-H4-PULLBACK | 5m | 2897 | -0.052 | +0.016 | -0.112 | -0.085 | yes |
| TRD-H4-BREAKOUT | 15m | 793 | -0.054 | -0.094 | -0.090 | -0.073 | no |
| S8-PDH-PDL-SWEEP | 1h | 277 | -0.071 | -0.272 | -0.158 | -0.175 | no |
| TRD-H4-BREAKOUT | 5m | 1787 | -0.097 | -0.033 | -0.125 | -0.086 | yes |
| S8-PDH-PDL-SWEEP | 30m | 114 | -0.419 | -0.738 | -0.452 | -0.557 | no |
| PB-B-SWEEP | 5m | 1190 | -0.630 | -0.574 | +0.000 | +0.000 | too few trades to compare |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): PB-B-APLUS@1.0 15m BACKTESTING → FAILED; S5-SWEEP-MSS-FVG-noSMC@1.0 15m BACKTESTING → FAILED; TRD-H4-PULLBACK@1.0 1h FAILED → BACKTESTING; TRD-H4-PULLBACK@1.0 30m BACKTESTING → FAILED; donchian_breakout-VEXIT-S4@1.1 30m BACKTESTING → FAILED
- **Not tested (IDEA / RETIRED):** donchian_breakout-VEXIT-VRVOL v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S5 v1.0 (RETIRED)

### 3c. Research layers (daily run)
Last run: **2026-10-08 00:58 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 9 | 2017-08-17 | 2026-10-07 | 20017 |  |
| 1h | 9 | 2017-08-17 | 2026-10-07 | 80004 |  |
| 30m | 9 | 2024-10-08 | 2026-10-08 | 35040 |  |
| 15m | 9 | 2024-10-08 | 2026-10-08 | 70080 |  |
| 5m | 9 | 2024-10-08 | 2026-10-08 | 210240 |  |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 1042 (623) | false_breakout, trend_reversal | false_breakout 63% | +0.47R | -0.37R | +0.26 / +0.21 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 1187 (717) | false_breakout | false_breakout 62% | +0.48R | -0.36R | +0.26 / +0.21 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 861 (520) | no_displacement, false_breakout | false_breakout 62%, no_displacement 35% | +0.47R | -0.36R | +0.24 / +0.20 |
| TRD-H4-BREAKOUT | 30m | BACKTESTING | 445 (264) | false_breakout | false_breakout 77%, no_displacement 42% | +0.55R | -0.47R | +0.21 / +0.14 |
| donchian_breakout | 4h | BACKTESTING | 1070 (489) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 65%, stop_too_tight 33% | +0.33R | -0.37R | +0.18 / +0.13 |
| TRD-H4-BREAKOUT | 1h | BACKTESTING | 1024 (631) | false_breakout | false_breakout 65% | +0.55R | -0.43R | +0.16 / +0.11 |
| TRD-H4-PULLBACK | 15m | BACKTESTING | 1161 (700) | none | - | +0.48R | -0.37R | +0.14 / +0.05 |
| TRD-H4-PULLBACK | 1h | BACKTESTING | 1015 (626) | low_relative_volume, indicator_lag | low_relative_volume 56%, indicator_lag 26% | +0.46R | -0.40R | +0.10 / +0.04 |
| TRD-H4-BREAKOUT-noT4 | 1h | BACKTESTING | 3341 (2096) | no_displacement, false_breakout | false_breakout 66% | +0.52R | -0.44R | +0.10 / +0.04 |
| bb_squeeze_breakout | 1h | BACKTESTING | 799 (377) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 63%, no_displacement 52%, stop_too_tight 37%, regime_mismatch 34% | +0.35R | -0.47R | +0.15 / +0.01 |
| PB-A-APLUS | 5m | BACKTESTING | 71 (41) | stop_too_tight, indicator_lag | low_relative_volume 51%, stop_too_tight 44%, indicator_lag 27% | +0.44R | -0.33R | -0.01 / -0.18 |
| PB-A-GRADED | 5m | BACKTESTING | 89 (50) | stop_too_tight | stop_too_tight 38% | +0.44R | -0.31R | -0.01 / -0.18 |
| S5-SWEEP-MSS-FVG-noSMC | 15m | FAILED | 33 (15) | structural_change | range_market 27% | +0.42R | -0.47R | +0.59 / +0.41 |
| bb_squeeze_breakout | 4h | FAILED | 266 (130) | false_breakout, stop_too_tight, structural_change | false_breakout 58%, stop_too_tight 39%, regime_mismatch 30% | +0.35R | -0.35R | +0.10 / +0.03 |
| TRD-H4-PULLBACK | 30m | FAILED | 618 (395) | none | - | +0.46R | -0.42R | +0.07 / -0.01 |
| TRD-H4-BREAKOUT-noT4 | 30m | FAILED | 1457 (922) | range_market, false_breakout | false_breakout 72%, range_market 29% | +0.50R | -0.47R | +0.07 / -0.01 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2414 (1615) | false_breakout, regime_mismatch | false_breakout 62% | +0.53R | -0.40R | +0.07 / -0.01 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 3240 (2165) | no_displacement, false_breakout, regime_mismatch | false_breakout 64% | +0.51R | -0.40R | +0.08 / -0.01 |
| TRD-H4-PULLBACK-noT4 | 1h | FAILED | 4759 (2978) | structural_change | - | +0.50R | -0.42R | +0.05 / -0.01 |
| donchian_breakout-VEXIT | 1h | FAILED | 2862 (1922) | false_breakout | false_breakout 63% | +0.52R | -0.40R | +0.07 / -0.01 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1056 (694) | false_breakout | false_breakout 72% | +0.44R | -0.40R | +0.10 / -0.02 |
| donchian_breakout-VEXIT | 30m | FAILED | 1140 (750) | false_breakout | false_breakout 71% | +0.45R | -0.41R | +0.11 / -0.02 |
| donchian_breakout | 1h | FAILED | 2944 (1505) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 31%, regime_mismatch 25% | +0.37R | -0.40R | +0.06 / -0.02 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1341 (885) | false_breakout | false_breakout 72% | +0.46R | -0.41R | +0.10 / -0.04 |
| macd_trend_cross | 4h | FAILED | 39 (19) | structural_change | no_displacement 90%, regime_mismatch 90%, low_relative_volume 53%, indicator_lag 53% | +0.21R | -0.46R | +0.04 / -0.04 |
| donchian_breakout | 30m | FAILED | 1175 (613) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 75%, no_displacement 38%, stop_too_tight 33% | +0.28R | -0.41R | +0.08 / -0.05 |
| supertrend_flip | 4h | FAILED | 89 (47) | regime_mismatch, stop_too_tight, indicator_lag, structural_change | regime_mismatch 68%, indicator_lag 43%, stop_too_tight 26% | +0.37R | -0.43R | +0.01 / -0.05 |
| TRD-H4-PULLBACK | 5m | FAILED | 2897 (1812) | overextended_entry | - | +0.51R | -0.42R | +0.08 / -0.05 |
| S6-OB-FVG-noSMC | 15m | FAILED | 70 (41) | none | stop_too_wide 90%, regime_mismatch 34% | +0.35R | -0.48R | +0.09 / -0.05 |
| macd_trend_cross | 1h | FAILED | 181 (91) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 92%, indicator_lag 40%, stop_too_tight 31% | +0.30R | -0.41R | +0.08 / -0.05 |
| TRD-H4-BREAKOUT | 15m | FAILED | 793 (521) | false_breakout | false_breakout 79% | +0.44R | -0.49R | +0.04 / -0.05 |
| TRD-H4-PULLBACK-noT4 | 15m | FAILED | 4142 (2624) | none | - | +0.49R | -0.41R | +0.05 / -0.06 |
| trend_pullback | 4h | FAILED | 1188 (622) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 81%, indicator_lag 38%, stop_too_tight 25% | +0.35R | -0.42R | +0.00 / -0.07 |
| TRD-H4-PULLBACK-noT4 | 30m | FAILED | 2346 (1528) | none | - | +0.50R | -0.41R | +0.02 / -0.07 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 277 (183) | stop_too_tight, sweep_continued, structural_change | sweep_continued 97%, range_market 56%, stop_too_tight 33% | +0.56R | -0.44R | +0.14 / -0.07 |
| TRD-H4-BREAKOUT-noT4 | 15m | FAILED | 2541 (1686) | range_market, false_breakout | false_breakout 76%, range_market 39% | +0.45R | -0.44R | +0.02 / -0.09 |
| TRD-H4-BREAKOUT | 5m | FAILED | 1787 (1153) | false_breakout | false_breakout 76% | +0.44R | -0.44R | +0.04 / -0.10 |
| rsi2_dip_buy | 4h | FAILED | 1796 (780) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 44% | +0.16R | -0.21R | -0.05 / -0.10 |
| rsi2_dip_buy | 1h | FAILED | 6765 (2986) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 42% | +0.15R | -0.21R | +0.00 / -0.11 |
| TRD-H4-PULLBACK-noT4 | 5m | FAILED | 8701 (5545) | none | - | +0.50R | -0.43R | +0.04 / -0.11 |
| R4-CLUC | 30m | FAILED | 195 (115) | none | wrong_session 69% | +0.29R | -0.45R | -0.01 / -0.11 |
| trend_pullback | 1h | FAILED | 6141 (3261) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 77%, indicator_lag 44%, stop_too_tight 27% | +0.30R | -0.43R | +0.01 / -0.12 |
| ema_9_21_cross | 1h | FAILED | 327 (185) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 79%, indicator_lag 48%, stop_too_tight 26% | +0.27R | -0.37R | +0.01 / -0.12 |
| TRD-H4-BREAKOUT-noT4 | 5m | FAILED | 5098 (3329) | false_breakout | false_breakout 74% | +0.48R | -0.44R | +0.03 / -0.12 |
| bb_squeeze_breakout | 30m | FAILED | 483 (252) | false_breakout, stop_too_tight | false_breakout 60%, stop_too_tight 39% | +0.25R | -0.47R | +0.07 / -0.15 |
| trend_pullback | 30m | FAILED | 3166 (1668) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 31% | +0.28R | -0.43R | +0.04 / -0.15 |
| macd_trend_cross | 30m | FAILED | 266 (139) | overextended_entry, stop_too_tight, indicator_lag | low_relative_volume 45%, indicator_lag 41%, stop_too_tight 30% | +0.34R | -0.47R | +0.05 / -0.15 |
| rsi2_dip_buy | 30m | FAILED | 2552 (1284) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 30% | +0.16R | -0.19R | +0.01 / -0.16 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 760 (521) | range_market, trend_reversal, stop_too_tight | range_market 46%, stop_too_tight 37% | +0.63R | -0.52R | +0.06 / -0.16 |
| ema_9_21_cross | 30m | FAILED | 314 (180) | stop_too_tight, indicator_lag | indicator_lag 47%, low_relative_volume 39%, stop_too_tight 25% | +0.26R | -0.38R | +0.02 / -0.17 |
| PB-B-GRADED | 5m | FAILED | 1268 (807) | none | - | +0.23R | -0.26R | +0.00 / -0.17 |
| PB-B-SWEEP-LIMIT | 5m | FAILED | 319 (197) | low_relative_volume | - | +0.24R | -0.27R | +0.00 / -0.18 |
| PB-B-APLUS | 15m | FAILED | 103 (58) | stop_too_tight | regime_mismatch 52%, stop_too_tight 43% | +0.36R | -0.36R | -0.01 / -0.18 |
| liquidity_sweep_reversal | 1h | FAILED | 280 (147) | stop_too_tight | stop_too_tight 48% | +0.29R | -0.48R | -0.02 / -0.18 |
| ema_9_21_cross | 15m | FAILED | 809 (450) | stop_too_tight, indicator_lag | indicator_lag 53%, stop_too_tight 26% | +0.23R | -0.42R | +0.07 / -0.18 |
| supertrend_flip | 1h | FAILED | 265 (145) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 71%, stop_too_tight 38%, indicator_lag 30% | +0.39R | -0.40R | -0.10 / -0.19 |
| supertrend_flip | 30m | FAILED | 144 (78) | stop_too_tight, indicator_lag | regime_mismatch 45%, indicator_lag 44%, stop_too_tight 36%, overextended_entry 31% | +0.28R | -0.46R | -0.06 / -0.20 |
| PB-B-APLUS | 5m | FAILED | 265 (171) | low_relative_volume | - | +0.23R | -0.34R | -0.03 / -0.20 |
| R4-CLUC | 15m | FAILED | 161 (108) | none | - | +0.36R | -0.31R | -0.08 / -0.20 |
| PB-B-GRADED | 15m | FAILED | 500 (312) | stop_too_tight | stop_too_tight 36% | +0.35R | -0.36R | -0.05 / -0.22 |
| trend_pullback | 15m | FAILED | 5369 (2914) | stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 31% | +0.27R | -0.44R | +0.05 / -0.22 |
| rsi2_dip_buy | 15m | FAILED | 4043 (2333) | wrong_session, trend_reversal, volatility_spike, fees_slippage | fees_slippage 37% | +0.15R | -0.19R | +0.01 / -0.24 |
| bb_squeeze_breakout | 15m | FAILED | 1082 (595) | false_breakout, stop_too_tight | false_breakout 62%, stop_too_tight 39% | +0.27R | -0.48R | +0.02 / -0.29 |
| R4-BBRSI | 30m | FAILED | 1379 (944) | none | - | +0.42R | -0.43R | -0.07 / -0.29 |
| R4-BBRSI | 1h | FAILED | 1242 (885) | none | - | +0.44R | -0.46R | -0.15 / -0.30 |
| liquidity_sweep_reversal | 30m | FAILED | 322 (189) | stop_too_tight | stop_too_tight 40% | +0.40R | -0.51R | -0.12 / -0.38 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 114 (89) | low_relative_volume, sweep_continued | sweep_continued 98% | +0.52R | -0.62R | -0.14 / -0.42 |
| PB-B-SWEEP-15M | 15m | FAILED | 271 (164) | low_relative_volume, stop_too_tight | stop_too_tight 31%, low_relative_volume 28% | +0.24R | -0.45R | +0.04 / -0.45 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 523 (385) | stop_too_tight | stop_too_tight 34% | +0.60R | -0.48R | -0.11 / -0.45 |
| ema_9_21_cross | 5m | FAILED | 2111 (1342) | stop_too_tight, indicator_lag | indicator_lag 53%, stop_too_tight 31% | +0.21R | -0.45R | +0.01 / -0.47 |
| liquidity_sweep_reversal | 15m | FAILED | 1139 (691) | stop_too_tight | stop_too_tight 40% | +0.29R | -0.48R | -0.06 / -0.47 |
| PB-B-SWEEP | 5m | FAILED | 1190 (782) | range_market, stop_too_tight | stop_too_tight 35%, range_market 28% | +0.14R | -0.40R | +0.05 / -0.63 |
| liquidity_sweep_reversal | 5m | FAILED | 4042 (2670) | range_market, stop_too_tight | stop_too_tight 40% | +0.25R | -0.50R | +0.09 / -0.67 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 33 strategy/timeframe tests); `false_breakout` (systematic in 24 strategy/timeframe tests); `indicator_lag` (systematic in 15 strategy/timeframe tests); `regime_mismatch` (systematic in 14 strategy/timeframe tests); `trend_reversal` (systematic in 7 strategy/timeframe tests); `no_displacement` (systematic in 5 strategy/timeframe tests); `range_market` (systematic in 5 strategy/timeframe tests); `low_relative_volume` (systematic in 5 strategy/timeframe tests); `volatility_spike` (systematic in 4 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests); `overextended_entry` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- BTC down -3.1% (2026-10-06 14:00 → 2026-10-07 03:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ETH down -4.6% (2026-10-07 00:00 → 2026-10-07 13:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- XRP down -4.0% (2026-10-06 14:00 → 2026-10-07 03:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- SOL down -3.5% (2026-10-07 00:00 → 2026-10-07 13:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- BNB down -2.7% (2026-10-06 14:00 → 2026-10-07 03:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- UNI down -7.9% (2026-10-06 14:00 → 2026-10-07 03:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ADA down -8.3% (2026-10-06 14:00 → 2026-10-07 03:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move

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
| `memory/execution_notes.md` | 12.7 KB | 28 | 2026-10-07 05:20 UTC |
| `memory/experiments.md` | 66.6 KB | 27 | 2026-10-08 15:30 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 270.2 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 17.0 KB | - | - |
| `memory/missed_trades.md` | 45.6 KB | 61 | 2026-10-08 15:30 UTC |
| `memory/playbook.md` | 10.0 KB | - | - |
| `memory/research_sources.md` | 94.1 KB | 72 | 2026-10-08 15:30 UTC |
| `memory/smc_events.csv` | 1182.8 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 26.1 KB | - | - |
| `memory/strategy_registry.csv` | 64.3 KB | - | - |
| `memory/trials.csv` | 15.2 KB | - | - |
| `memory/universe_log.md` | 23.1 KB | - | - |

**Reviews due** (review date passed; for the reviews): `missed_trades.md` LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00 (2026-10-02); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03); `missed_trades.md` SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells (2026-10-03); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03) … and 14 more
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG and SHORT = OKX futures fees + funding (always charged, never received). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*