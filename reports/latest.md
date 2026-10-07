# Crypto Signal Report

**Updated:** 2026-10-07 22:22 Beijing time (2026-10-07 14:22 UTC) · data: Binance · 8 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 11.7 MB (GitHub) · large files of this run 4.9 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-07 14:22 UTC / 2026-10-07 22:22 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US CPI (Sep data) 2026-10-14 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.04% (limit 0.5%)
- All 8 coins passed every check on every timeframe.
- 56 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-07 14:21 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 1008 h since 2026-08-26 | +0.0025% | 1.51 | 0.69 | - |
| ETH | GOOD | okx | 1008 h since 2026-08-26 | +0.0009% | 2.19 | 0.75 | - |
| SOL | GOOD | okx | 1008 h since 2026-08-26 | -0.0055% | 1.92 | 0.67 | - |
| XRP | GOOD | okx | 1008 h since 2026-08-26 | -0.0059% | 3.14 | 0.63 | - |
| ZEC | GOOD | okx | 1008 h since 2026-08-26 | +0.0070% | 0.93 | 0.95 | - |
| BNB | GOOD | okx | 1008 h since 2026-08-26 | -0.0127% | 2.44 | 0.65 | - |
| SUI | GOOD | okx | 1008 h since 2026-08-26 | +0.0024% | 2.71 | 0.96 | - |
| UNI | GOOD | okx | 1008 h since 2026-08-26 | +0.0029% | 1.98 | 0.73 | - |

*Binance futures API: blocked from GitHub's servers (HTTP 451) - expected, not a problem. The main series (OKX) is complete; Binance research history comes from the data.binance.vision files.*

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **XRP**, **ZEC**, **BNB**, **SUI**
- **Research only** - backtested, never a signal: UNI
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** AVAX - 7-day average volume $49M < $50M; order book too thin: $244k within 1% (need $250k)

| Not eligible | 24h volume | Why |
|---|---|---|
| AVAX | $75M | 7-day average volume $49M < $50M; order book too thin: $244k within 1% (need $250k) |
| ADA | $62M | 7-day average volume $50M < $50M |

*Skipped by your exclusion lists:* DOGE, NEAR, RLUSD, USD1, USDC (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 477 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ETH | 477 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| SOL | 321 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| XRP | 440 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| ZEC | 394 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| BNB | 465 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| SUI | 179 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| UNI | 316 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | down (LH/LL) | 84,379.3 / 83,577 | 0.53 | 2.49x | 1.15x | bull_reject, breakout_down |
| ETH | down (LH/LL) | 2,623.83 / 2,591.71 | 0.69 | 1.62x | 1.44x | bull_reject |
| SOL | down (LH/LL) | 119.08 / 117.02 | 0.66 | 2.66x | 1.28x | displacement_down, breakout_down, retest_down |
| XRP | down (LH/LL) | 1.4778 / 1.4345 | 0.42 | 2.14x | 1.28x | breakout_down |
| ZEC | down (LH/LL) | 1,372.15 / 1,300 | 0.79 | 2.20x | 1.11x | bull_engulf, bull_reject |
| BNB | down (LH/LL) | 775.7 / 758.57 | 0.80 | 2.18x | 1.15x | bull_reject |
| SUI | down (LH/LL) | 1.2066 / 1.1125 | 0.64 | 2.56x | 0.89x | bear_engulf |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 385 | 49% | 34% | 27% | 80% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | displacement_down | 292 | 47% | 28% | 17% | 78% | 45% | 30% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 980 | 46% | 32% | 22% | 77% | 45% | 31% | can't tell from chance | 0.09R |
| 4h | bear_engulf | 1097 | 41% | 27% | 17% | 80% | 46% | 30% | worse than chance | 0.08R |
| 4h | bull_reject | 729 | 43% | 30% | 21% | 77% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | bear_reject | 712 | 46% | 32% | 21% | 74% | 46% | 30% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 523 | 45% | 31% | 22% | 75% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bear | 557 | 44% | 29% | 18% | 80% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 240 | 46% | 29% | 21% | 82% | 47% | 32% | can't tell from chance | 0.09R |
| 4h | smc_bos_down | 180 | 46% | 32% | 21% | 74% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 72 | 50% | 36% | 28% | 82% | 44% | 31% | can't tell from chance | 0.08R |
| 4h | smc_choch_down | 67 | 42% | 24% | 13% | 78% | 50% | 32% | can't tell from chance | 0.09R |
| 4h | smc_fvg_retrace_bull | 536 | 46% | 29% | 23% | 76% | 46% | 32% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bear | 531 | 46% | 29% | 18% | 77% | 45% | 30% | can't tell from chance | 0.08R |
| 1h | displacement_up | 494 | 47% | 34% | 27% | 74% | 44% | 31% | can't tell from chance | 0.18R |
| 1h | displacement_down | 345 | 36% | 23% | 14% | 83% | 37% | 24% | can't tell from chance | 0.19R |
| 1h | bull_engulf | 1368 | 43% | 30% | 22% | 74% | 45% | 31% | can't tell from chance | 0.20R |
| 1h | bear_engulf | 1529 | 38% | 23% | 15% | 80% | 37% | 23% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1128 | 44% | 30% | 23% | 75% | 45% | 31% | can't tell from chance | 0.19R |
| 1h | bear_reject | 1102 | 35% | 23% | 16% | 82% | 37% | 23% | can't tell from chance | 0.19R |
| 1h | smc_sweep_bull | 495 | 46% | 29% | 21% | 74% | 45% | 31% | can't tell from chance | 0.19R |
| 1h | smc_sweep_bear | 557 | 36% | 23% | 15% | 81% | 37% | 23% | can't tell from chance | 0.20R |
| 1h | smc_bos_up | 324 | 46% | 35% | 28% | 77% | 47% | 33% | can't tell from chance | 0.17R |
| 1h | smc_bos_down | 216 | 40% | 29% | 19% | 82% | 37% | 23% | can't tell from chance | 0.22R |
| 1h | smc_choch_up | 89 | 46% | 30% | 27% | 78% | 45% | 32% | can't tell from chance | 0.21R |
| 1h | smc_choch_down | 86 | 40% | 28% | 17% | 76% | 40% | 25% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 726 | 47% | 33% | 24% | 72% | 45% | 31% | can't tell from chance | 0.19R |
| 1h | smc_fvg_retrace_bear | 630 | 37% | 25% | 18% | 79% | 38% | 24% | can't tell from chance | 0.22R |
| 30m | displacement_up | 421 | 37% | 27% | 21% | 80% | 43% | 29% | worse than chance | 0.23R |
| 30m | displacement_down | 354 | 43% | 27% | 18% | 80% | 35% | 21% | beats chance | 0.22R |
| 30m | bull_engulf | 1342 | 42% | 28% | 18% | 77% | 42% | 28% | can't tell from chance | 0.25R |
| 30m | bear_engulf | 1446 | 37% | 22% | 16% | 81% | 36% | 22% | can't tell from chance | 0.25R |
| 30m | bull_reject | 1041 | 46% | 29% | 21% | 75% | 43% | 28% | can't tell from chance | 0.25R |
| 30m | bear_reject | 1190 | 37% | 23% | 16% | 81% | 36% | 22% | can't tell from chance | 0.24R |
| 30m | smc_sweep_bull | 533 | 43% | 29% | 20% | 75% | 43% | 28% | can't tell from chance | 0.23R |
| 30m | smc_sweep_bear | 512 | 41% | 27% | 18% | 81% | 35% | 22% | beats chance | 0.23R |
| 30m | smc_bos_up | 333 | 36% | 29% | 24% | 79% | 42% | 28% | can't tell from chance | 0.23R |
| 30m | smc_bos_down | 203 | 33% | 22% | 14% | 85% | 35% | 22% | can't tell from chance | 0.25R |
| 30m | smc_choch_up | 84 | 35% | 21% | 17% | 85% | 43% | 28% | can't tell from chance | 0.25R |
| 30m | smc_choch_down | 86 | 41% | 27% | 22% | 76% | 37% | 23% | can't tell from chance | 0.22R |
| 30m | smc_fvg_retrace_bull | 786 | 41% | 26% | 17% | 79% | 43% | 29% | can't tell from chance | 0.24R |
| 30m | smc_fvg_retrace_bear | 671 | 37% | 22% | 16% | 80% | 35% | 22% | can't tell from chance | 0.26R |
| 15m | displacement_up | 404 | 36% | 24% | 18% | 85% | 38% | 27% | can't tell from chance | 0.31R |
| 15m | displacement_down | 329 | 33% | 23% | 16% | 81% | 33% | 20% | can't tell from chance | 0.32R |
| 15m | bull_engulf | 1369 | 37% | 27% | 19% | 78% | 38% | 27% | can't tell from chance | 0.34R |
| 15m | bear_engulf | 1316 | 32% | 21% | 13% | 80% | 33% | 20% | can't tell from chance | 0.34R |
| 15m | bull_reject | 1052 | 40% | 29% | 21% | 75% | 38% | 27% | can't tell from chance | 0.36R |
| 15m | bear_reject | 1204 | 32% | 19% | 13% | 83% | 34% | 20% | can't tell from chance | 0.34R |
| 15m | smc_sweep_bull | 479 | 42% | 31% | 22% | 73% | 38% | 27% | can't tell from chance | 0.30R |
| 15m | smc_sweep_bear | 453 | 33% | 21% | 11% | 84% | 34% | 21% | can't tell from chance | 0.32R |
| 15m | smc_bos_up | 323 | 37% | 25% | 20% | 80% | 39% | 27% | can't tell from chance | 0.34R |
| 15m | smc_bos_down | 220 | 27% | 17% | 13% | 86% | 34% | 21% | worse than chance | 0.34R |
| 15m | smc_choch_up | 69 | 29% | 16% | 9% | 91% | 36% | 26% | can't tell from chance | 0.41R |
| 15m | smc_choch_down | 74 | 32% | 23% | 12% | 78% | 31% | 18% | can't tell from chance | 0.36R |
| 15m | smc_fvg_retrace_bull | 877 | 38% | 27% | 20% | 76% | 37% | 26% | can't tell from chance | 0.35R |
| 15m | smc_fvg_retrace_bear | 716 | 31% | 21% | 14% | 83% | 33% | 20% | can't tell from chance | 0.35R |
| 5m | displacement_up | 959 | 29% | 20% | 15% | 87% | 30% | 20% | can't tell from chance | 0.60R |
| 5m | displacement_down | 938 | 23% | 16% | 12% | 86% | 28% | 18% | worse than chance | 0.54R |
| 5m | bull_engulf | 3517 | 28% | 19% | 14% | 84% | 29% | 20% | can't tell from chance | 0.62R |
| 5m | bear_engulf | 3315 | 27% | 19% | 13% | 83% | 27% | 18% | can't tell from chance | 0.64R |
| 5m | bull_reject | 2638 | 28% | 19% | 13% | 83% | 29% | 19% | can't tell from chance | 0.65R |
| 5m | bear_reject | 2964 | 29% | 19% | 12% | 83% | 28% | 19% | can't tell from chance | 0.63R |
| 5m | smc_sweep_bull | 975 | 31% | 20% | 14% | 80% | 30% | 21% | can't tell from chance | 0.51R |
| 5m | smc_sweep_bear | 969 | 30% | 22% | 14% | 83% | 29% | 19% | can't tell from chance | 0.54R |
| 5m | smc_bos_up | 649 | 26% | 18% | 14% | 88% | 28% | 19% | can't tell from chance | 0.70R |
| 5m | smc_bos_down | 709 | 25% | 17% | 12% | 86% | 29% | 19% | can't tell from chance | 0.57R |
| 5m | smc_choch_up | 169 | 32% | 22% | 17% | 85% | 28% | 18% | can't tell from chance | 0.75R |
| 5m | smc_choch_down | 168 | 21% | 12% | 8% | 89% | 28% | 20% | worse than chance | 0.59R |
| 5m | smc_fvg_retrace_bull | 2778 | 29% | 20% | 14% | 83% | 28% | 19% | can't tell from chance | 0.70R |
| 5m | smc_fvg_retrace_bear | 2456 | 25% | 18% | 12% | 84% | 27% | 18% | worse than chance | 0.68R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (strong) | WEAK_BULL (moderate) | UNCLEAR (weak) | EXPANSION down (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H UNCLEAR, 1H EXPANSION)) |
| **ETH** | WEAK_BULL (weak) | WEAK_BULL (moderate) | UNCLEAR (weak) | STRONG_BEAR (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H UNCLEAR, 1H STRONG_BEAR)) |
| **SOL** | WEAK_BULL (moderate) | WEAK_BULL (weak) | UNCLEAR (weak) | EXPANSION down (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H UNCLEAR, 1H EXPANSION)) |
| **XRP** | TRANSITION (weak) | WEAK_BULL (weak) | RANGE (strong) | EXPANSION down (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H EXPANSION)) |
| **ZEC** | WEAK_BULL (weak) | WEAK_BULL (weak) | COMPRESSION (strong) | WEAK_BEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H COMPRESSION, 1H WEAK_BEAR)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (strong) | TRANSITION (weak) | WEAK_BEAR (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H TRANSITION, 1H WEAK_BEAR)) |
| **SUI** | UNCLEAR (weak) | WEAK_BULL (weak) | TRANSITION (weak) | WEAK_BEAR (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H WEAK_BEAR)) |
| **UNI** | EXPANSION up (moderate) | WEAK_BULL (weak) | UNCLEAR (weak) | STRONG_BEAR (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H UNCLEAR, 1H STRONG_BEAR)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.8 ATR in 10 candles); swing structure down (LH/LL); ADX 28 = strong trend; candle size 0.71x normal, Bollinger width above 62% of the last 100 candles · against: -
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.2 ATR in 10 candles); ADX 44 = strong trend; candle size 0.98x normal, Bollinger width above 46% of the last 100 candles; volume 0.85x normal · against: swing structure mixed (neutral)
- **4H UNCLEAR (weak)** - for: candle size 0.91x normal, Bollinger width above 54% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (+0.2 ATR in 10 candles); swing structure mixed; ADX 22 = in between (20-25); ADX 22 is close to a threshold; signals are mixed and trend strength is in between
- **1H EXPANSION down (moderate)** - for: EMA-fast falling (-1.4 ATR in 10 candles); swing structure down (LH/LL); ADX 43 = strong trend; candle size 1.15x normal, Bollinger width above 99% of the last 100 candles; volume 1.63x normal; range expansion + displacement / breakout down in the last 3 candles · against: EMAs not lined up (neutral)

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **Silver Bullet**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (BOS 4 candles ago) | sell-side (bullish idea) 1 candles ago | bear 84,150.00-84,228.00 (retraced) | bear 85,550.00-86,378.24 | below the range (-48%) | swing high 84,379.31 (3.03 ATR) | swing low 82,775.94 (1.06 ATR) |
| **ETH** | down (BOS 6 candles ago) | sell-side (bullish idea) 16 candles ago | bear 2,600.51-2,604.41 | bear 2,690.78-2,700.54 | below the range (-69%) | swing high 2,623.83 (3.26 ATR) | swing low 2,494.37 (4.5 ATR) |
| **SOL** | down (CHOCH 7 candles ago) | sell-side (bullish idea) 5 candles ago | bear 117.90-118.02 (retraced) | bear 120.13-121.29 | below the range (-39%) | swing high 119.08 (3.39 ATR) | swing low 112.52 (4.36 ATR) |
| **XRP** | down (BOS 4 candles ago) | sell-side (bullish idea) 20 candles ago | bear 1.4603-1.4620 | bull 1.3773-1.3856 | below the range (-2%) | swing high 1.4778 (3.94 ATR) | swing low 1.3920 (3.73 ATR) |
| **ZEC** | up (CHOCH 1 candles ago) | buy-side (bearish idea) 1 candles ago | bull 1,319.49-1,324.01 | bear 1,397.89-1,447.60 | discount (37%) | swing high 1,372.15 (2.39 ATR) | swing low 1,278.00 (2.58 ATR) |
| **BNB** | up (CHOCH 26 candles ago) | sell-side (bullish idea) 7 candles ago | bear 771.26-772.56 (retraced) | bull 765.01-768.61 | premium (53%) | swing high 775.70 (2.14 ATR) | swing low 758.57 (2.4 ATR) |
| **SUI** | down (BOS 2 candles ago) | sell-side (bullish idea) 2 candles ago | bear 1.1304-1.1323 (retraced) | bull 1.0050-1.0598 | discount (7%) | equal highs 1.2067 (6.64 ATR) | swing low 1.1032 (1.18 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **SIDEWAYS**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 71 (Greed), yesterday 73  (extreme fear/greed = bigger, faster moves)

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
**Status and long-history numbers** come from the daily research run (last run 2026-10-07 00:58 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PB-C-BREAKOUT-W20 | 1.0 | 5m | **BACKTESTING** | 1 | 100.0 | +0.351 | 99.0 | 0.0R | +0.35 / +0.00 | +0.35 / +0.00 | 0/5 ✗ | +0.30 | +0.25 | stable | 0 | 0.85R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | not cost-viable: fees + slippage 0.85R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 29 | 51.7 | +0.284 | 1.59 | 7.3R | +0.60 / -0.54 | +0.81 / -0.37 | 0/5 ✗ | +0.28 | +0.30 | stable | 2 | 0.15R | 0, +0.00 (+0.00 / +0.00) | 420 / 141 of 663 | 0 | only 29 trades; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 40.0 | +0.274 | 1.38 | 3.6R | -0.22 / +2.24 | +1.21 / -1.13 | 0/5 ✗ | +0.19 | +0.11 | stable | 0 | 0.15R | 0, +0.00 (+0.00 / +0.00) | 10 / 3 of 15 | 0 | only 5 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 903 | 40.6 | +0.230 | 1.43 | 21.6R | +0.22 / +0.25 | +0.26 / +0.20 | 5/5 | +0.20 | +0.18 | stable | 8 | 0.04R | 2, -1.05 (-1.05 / +0.00) | 76 / 43 of 213 | 0 | max drawdown 21.6R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1029 | 39.8 | +0.220 | 1.4 | 21.3R | +0.22 / +0.23 | +0.23 / +0.21 | 5/5 | +0.19 | +0.17 | stable | 8 | 0.04R | 3, -1.04 (-1.04 / +0.00) | 130 / 56 of 289 | 0 | max drawdown 21.3R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 4h | **BACKTESTING** | 722 | 40.3 | +0.213 | 1.4 | 17.3R | +0.20 / +0.25 | +0.22 / +0.21 | 5/5 | +0.19 | +0.17 | stable | 7 | 0.03R | 2, -1.03 (-1.03 / +0.00) | 85 / 36 of 201 | 0 | max drawdown 17.3R |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 19 | 42.1 | +0.168 | 1.24 | 8.0R | -0.72 / +1.39 | +1.20 / -0.31 | 1/5 ✗ | -0.86 | -0.63 | ✗  stop buffer_atr 0.2→0.24: -0.30R | 1 | 0.17R | 0, +0.00 (+0.00 / +0.00) | 38 / 9 of 55 | 0 | only 19 trades; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 30m | **BACKTESTING** | 405 | 40.5 | +0.139 | 1.22 | 17.6R | +0.09 / +0.27 | +0.21 / +0.07 | 4/5 | +0.13 | +0.10 | stable | 6 | 0.06R | 8, +0.22 (+0.22 / +0.00) | 9 / 8 of 86 | 0 | max drawdown 17.6R |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 929 | 54.7 | +0.135 | 1.31 | 20.2R | +0.13 / +0.15 | +0.14 / +0.13 | 5/5 | +0.11 | +0.09 | stable | 6 | 0.04R | 4, -0.69 (-0.69 / +0.00) | 76 / 43 of 213 | 0 | max drawdown 20.2R |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 2 | 50.0 | +0.130 | 1.21 | 1.2R | +0.13 / +0.00 | -1.22 / +1.47 | 0/5 ✗ | +0.02 | +0.00 | stable | 0 | 0.27R | 0, +0.00 (+0.00 / +0.00) | 37 / 7 of 51 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 1h | **BACKTESTING** | 899 | 37.9 | +0.094 | 1.15 | 50.8R | +0.01 / +0.25 | +0.14 / +0.04 | 4/5 | +0.07 | +0.05 | stable | 6 | 0.04R | 4, -0.11 (-0.11 / +0.00) | 6 / 2 of 93 | 0 | avg +0.09R/trade (needs +0.10R); profit factor 1.15; max drawdown 50.8R |
| TRD-H4-PULLBACK | 1.0 | 15m | **BACKTESTING** | 1061 | 40.2 | +0.061 | 1.1 | 56.0R | -0.01 / +0.26 | +0.04 / +0.09 | 4/5 | +0.04 | +0.03 | stable | 6 | 0.08R | 25, +0.20 (+0.20 / +0.00) | 55 / 52 of 437 | 0 | avg +0.06R/trade (needs +0.10R); profit factor 1.10; max drawdown 56.0R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 1h | **BACKTESTING** | 2922 | 36.6 | +0.022 | 1.03 | 93.8R | +0.00 / +0.07 | +0.08 / -0.04 | 4/5 | +0.00 | -0.03 | ✗  stop atr 2.0→1.6: -0.02R | 4 | 0.05R | 19, -0.54 (-0.73 / +0.21) | 143 / 431 of 803 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.03; max drawdown 93.8R |
| bb_squeeze_breakout | 1.0 | 1h | **BACKTESTING** | 713 | 52.3 | +0.012 | 1.02 | 31.3R | +0.00 / +0.04 | -0.01 / +0.04 | 2/5 ✗ | -0.06 | -0.12 | ✗  bb_k 2→1: -0.03R | 4 | 0.12R | 6, -0.06 (-0.03 / -0.12) | 124 / 26 of 184 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.02; max drawdown 31.3R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 30m | **BACKTESTING** | 923 | 35.3 | +0.012 | 1.02 | 55.2R | -0.01 / +0.08 | +0.12 / -0.10 | 2/5 ✗ | -0.04 | -0.10 | ✗  stop atr 2.0→1.6: -0.03R | 3 | 0.10R | 16, -0.38 (-0.49 / -0.02) | 130 / 24 of 259 | 0 | avg +0.01R/trade (needs +0.12R); profit factor 1.02; max drawdown 55.2R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 30m | **BACKTESTING** | 560 | 36.8 | +0.008 | 1.01 | 58.0R | -0.02 / +0.10 | -0.00 / +0.02 | 3/5 | +0.00 | -0.00 | ✗  time_stop_bars 48→38: -0.01R | 4 | 0.06R | 8, +0.38 (+0.38 / +0.00) | 32 / 26 of 255 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.01; max drawdown 58.0R; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 2 of 9 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 2 of 9 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 10 / 3 of 15 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-noCVD | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 11, -0.35 (-0.35 / +0.00) | 0 / 0 of 44 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT-noCVD | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-CVD | 1.0 | 5m | **BACKTESTING** | 12 | 50.0 | -0.013 | 0.98 | 4.8R | +0.09 / -1.10 | +0.42 / -0.16 | 0/5 ✗ | -0.11 | +0.53 | ✗  stop buffer_atr 0.0→0.0: -0.01R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 12 trades; avg -0.01R/trade (needs +0.15R); profit factor 0.98; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 5 | 40.0 | -0.108 | 0.85 | 2.6R | +1.21 / -0.44 | -0.20 / +0.03 | 0/5 ✗ | -0.31 | -0.41 | ✗  stop buffer_atr 0.2→0.24: -0.38R | 0 | 0.20R | 1, +1.97 (+1.97 / +0.00) | 32 / 84 of 125 | 0 | only 5 trades; avg -0.11R/trade (needs +0.10R); profit factor 0.85; only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 10 | 40.0 | -0.117 | 0.9 | 7.8R | +0.35 / -4.33 | -0.59 / +0.20 | 0/5 ✗ | -0.26 | -0.51 | ✗  stop buffer_atr 0.2→0.16: -3.04R | 0 | 0.33R | 0, +0.00 (+0.00 / +0.00) | 37 / 7 of 51 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); only 10 trades; avg -0.12R/trade (needs +0.10R); profit factor 0.90; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK | 1.0 | 5m | **BACKTESTING** | 15 | 46.7 | -0.137 | 0.78 | 6.7R | -0.07 / -1.10 | +0.43 / -0.34 | 0/5 ✗ | -0.20 | +0.27 | ✗  stop buffer_atr 0.0→0.0: -0.14R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 15 trades; avg -0.14R/trade (needs +0.15R); profit factor 0.78; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 10 | 40.0 | -0.166 | 0.65 | 3.7R | +0.24 / -0.34 | -0.15 / -0.17 | 0/5 ✗ | -0.31 | -0.39 | ✗  stop buffer_atr 0.2→0.24: -0.22R | 0 | 0.12R | 0, +0.00 (+0.00 / +0.00) | 433 / 151 of 688 | 0 | only 10 trades; avg -0.17R/trade (needs +0.10R); profit factor 0.65; only 7 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 15m | **BACKTESTING** | 96 | 42.7 | -0.208 | 0.64 | 22.0R | -0.20 / -0.25 | -0.19 / -0.22 | 1/5 ✗ | -0.28 | -0.29 | ✗  stop buffer_atr 0.0→0.0: -0.21R | 2 | 0.18R | 3, -0.52 (-0.52 / +0.00) | 0 / 0 of 17 | 0 | only 96 trades; avg -0.21R/trade (needs +0.15R); profit factor 0.64; max drawdown 22.0R; not profitable in BOTH train and unseen test |
| PB-A-GRADED | 1.0 | 5m | **BACKTESTING** | 77 | 41.6 | -0.225 | 0.64 | 21.4R | -0.19 / -0.38 | -0.11 / -0.29 | 1/5 ✗ | -0.34 | -0.47 | ✗  time_stop_bars 48→38: -0.25R | 1 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 77 trades; avg -0.22R/trade (needs +0.15R); profit factor 0.64; max drawdown 21.4R; not profitable in BOTH train and unseen test |
| PB-A-APLUS | 1.0 | 5m | **BACKTESTING** | 63 | 39.7 | -0.236 | 0.63 | 18.9R | -0.22 / -0.32 | -0.00 / -0.37 | 0/5 ✗ | -0.32 | -0.50 | ✗  time_stop_bars 48→38: -0.26R | 2 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 63 trades; avg -0.24R/trade (needs +0.15R); profit factor 0.63; max drawdown 18.9R; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-LDN | 1.0 | 5m | **BACKTESTING** | 26 | 42.3 | -0.340 | 0.53 | 14.6R | -0.18 / -0.88 | +0.01 / -0.50 | 0/5 ✗ | -0.40 | -0.43 | ✗  stop buffer_atr 0.0→0.0: -0.34R | 2 | 0.24R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 26 trades; avg -0.34R/trade (needs +0.15R); profit factor 0.53; max drawdown 14.6R; only 6 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-GRADED | 1.0 | 5m | **BACKTESTING** | 10 | 30.0 | -0.503 | 0.34 | 6.7R | -0.34 / -1.16 | -0.69 / -0.08 | 0/5 ✗ | +0.32 | +0.21 | ✗  stop buffer_atr 0.0→0.0: -0.50R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 2 | 0 | only 10 trades; avg -0.50R/trade (needs +0.15R); profit factor 0.34; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 8 | 12.5 | -0.570 | 0.45 | 5.8R | -0.37 / -1.17 | -1.22 / -0.35 | 0/5 ✗ | -0.55 | -0.63 | ✗  stop max_width_atr 3.0→3.6: -0.62R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 57 / 16 of 75 | 0 | only 8 trades; avg -0.57R/trade (needs +0.10R); profit factor 0.45; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-APLUS | 1.0 | 5m | **BACKTESTING** | 1 | 0.0 | -0.641 | 0.0 | 0.6R | -0.64 / +0.00 | -0.64 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: -0.64R | 0 | 0.23R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 1 trades; avg -0.64R/trade (needs +0.15R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.208 | 0.0 | 1.2R | -1.21 / +0.00 | -1.21 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.2→0.16: -1.21R | 0 | 0.27R | 0, +0.00 (+0.00 / +0.00) | 57 / 16 of 75 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.21R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 237 | 51.9 | +0.050 | 1.1 | 25.1R | +0.21 / -0.28 | +0.16 / -0.06 | 3/5 | +0.01 | -0.03 | stable | 5 | 0.06R | 2, +0.12 (+0.12 / +0.00) | 93 / 20 of 124 | 0 | avg +0.05R/trade (needs +0.10R); profit factor 1.10; max drawdown 25.1R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 1h | **FAILED** | 892 | 37.9 | +0.028 | 1.05 | 34.6R | +0.06 / -0.03 | -0.04 / +0.10 | 3/5 | +0.00 | -0.03 | ✗  stop atr 2.0→1.6: -0.00R | 4 | 0.04R | 4, -0.19 (-0.19 / +0.00) | 25 / 23 of 181 | 0 | avg +0.03R/trade (needs +0.10R); profit factor 1.05; max drawdown 34.6R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 64 | 42.2 | -0.004 | 0.99 | 7.5R | -0.08 / +0.22 | +0.07 / -0.17 | 3/5 | -0.10 | -0.08 | ✗  time_stop_bars 30→24: -0.06R | 5 | 0.11R | 3, -1.18 (-1.18 / +0.00) | 97 / 30 of 141 | 0 | avg -0.00R/trade (needs +0.10R); profit factor 0.99; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1019 | 34.8 | -0.006 | 0.99 | 70.6R | -0.03 / +0.05 | +0.09 / -0.11 | 2/5 ✗ | -0.07 | -0.12 | ✗  stop atr 2.0→1.6: -0.04R | 4 | 0.11R | 21, -0.42 (-0.54 / -0.22) | 111 / 33 of 278 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; max drawdown 70.6R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 30m | **FAILED** | 1307 | 36.6 | -0.008 | 0.99 | 74.7R | -0.04 / +0.08 | +0.04 / -0.06 | 2/5 ✗ | -0.04 | -0.07 | ✗  stop atr 2.0→1.6: -0.03R | 5 | 0.07R | 27, -0.30 (-0.32 / -0.20) | 113 / 457 of 780 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; max drawdown 74.7R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 162 | 51.2 | -0.012 | 0.98 | 27.7R | -0.13 / +0.24 | -0.01 / -0.02 | 2/5 ✗ | -0.06 | -0.12 | ✗  stop atr 1.5→1.2: -0.11R | 3 | 0.11R | 0, +0.00 (+0.00 / +0.00) | 186 / 3 of 191 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 27.7R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 1h | **FAILED** | 4122 | 37.6 | -0.016 | 0.97 | 189.3R | +0.00 / -0.06 | -0.04 / +0.01 | 1/5 ✗ | -0.05 | -0.08 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.05R | 28, -0.06 (-0.15 / +0.22) | 580 / 2278 of 3257 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 189.3R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1200 | 34.8 | -0.021 | 0.97 | 79.8R | -0.04 / +0.03 | +0.06 / -0.11 | 2/5 ✗ | -0.08 | -0.15 | ✗  stop atr 2.0→1.6: -0.07R | 3 | 0.11R | 28, -0.35 (-0.34 / -0.37) | 190 / 48 of 393 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 79.8R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 32 | 53.1 | -0.025 | 0.95 | 5.5R | +0.09 / -0.33 | +0.24 / -0.37 | 1/5 ✗ | -0.05 | -0.08 | ✗  time_stop_bars 40→32: -0.05R | 2 | 0.06R | 1, +0.31 (+0.31 / +0.00) | 123 / 3 of 127 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.95; only 9 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 1h | **FAILED** | 2049 | 32.4 | -0.026 | 0.96 | 141.0R | -0.07 / +0.07 | +0.01 / -0.07 | 1/5 ✗ | -0.07 | -0.10 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.07R | 7, -0.13 (-0.23 / +0.14) | 124 / 67 of 322 | 0 | avg -0.03R/trade (needs +0.12R); profit factor 0.96; max drawdown 141.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 2825 | 32.5 | -0.027 | 0.96 | 178.0R | -0.06 / +0.03 | +0.01 / -0.07 | 2/5 ✗ | -0.07 | -0.12 | ✗  stop atr 2.0→1.6: -0.05R | 3 | 0.07R | 13, -0.46 (-0.63 / -0.07) | 179 / 90 of 450 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.96; max drawdown 178.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2481 | 32.3 | -0.028 | 0.96 | 154.6R | -0.07 / +0.06 | +0.01 / -0.07 | 2/5 ✗ | -0.07 | -0.11 | ✗  stop atr 2.0→1.6: -0.05R | 4 | 0.07R | 9, -0.54 (-0.98 / +0.34) | 101 / 63 of 314 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.96; max drawdown 154.6R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1053 | 49.0 | -0.033 | 0.94 | 69.7R | -0.04 / -0.02 | +0.03 / -0.11 | 2/5 ✗ | -0.10 | -0.15 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.11R | 21, -0.37 (-0.40 / -0.33) | 111 / 33 of 278 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.94; max drawdown 69.7R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2549 | 48.1 | -0.037 | 0.93 | 129.0R | -0.05 / -0.00 | -0.02 / -0.05 | 1/5 ✗ | -0.08 | -0.12 | ✗  stop atr 2.0→1.6: -0.05R | 2 | 0.07R | 9, -0.28 (-0.84 / +0.83) | 101 / 63 of 314 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.93; max drawdown 129.0R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 5m | **FAILED** | 2610 | 37.6 | -0.044 | 0.93 | 221.8R | -0.06 / +0.00 | -0.06 / -0.03 | 1/5 ✗ | -0.04 | -0.12 | ✗  time_stop_bars 48→38: -0.05R | 1 | 0.13R | 68, -0.30 (-0.30 / +0.00) | 117 / 80 of 949 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.93; max drawdown 221.8R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 15m | **FAILED** | 723 | 34.6 | -0.054 | 0.92 | 59.5R | -0.05 / -0.07 | -0.03 / -0.08 | 2/5 ✗ | -0.07 | -0.12 | ✗  stop atr 2.0→1.6: -0.09R | 3 | 0.08R | 17, -0.47 (-0.47 / +0.00) | 12 / 13 of 118 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; max drawdown 59.5R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 15m | **FAILED** | 3699 | 36.9 | -0.056 | 0.92 | 286.8R | -0.06 / -0.04 | -0.04 / -0.07 | 1/5 ✗ | -0.08 | -0.11 | ✗  time_stop_bars 48→58: -0.06R | 1 | 0.10R | 77, -0.19 (-0.07 / -0.94) | 491 / 2222 of 3349 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.92; max drawdown 286.8R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1029 | 48.3 | -0.064 | 0.88 | 111.3R | -0.01 / -0.18 | +0.01 / -0.15 | 1/5 ✗ | -0.10 | -0.13 | ✗  long_rsi_hi 65→52: -0.16R | 2 | 0.05R | 14, -0.24 (-0.14 / -0.62) | 556 / 167 of 870 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.88; max drawdown 111.3R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 30m | **FAILED** | 2097 | 34.9 | -0.070 | 0.9 | 180.3R | -0.04 / -0.14 | -0.04 / -0.10 | 2/5 ✗ | -0.11 | -0.14 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.07R | 49, -0.21 (-0.13 / -0.47) | 467 / 2207 of 3195 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.90; max drawdown 180.3R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 79 | 46.8 | -0.076 | 0.86 | 15.0R | +0.07 / -0.31 | -0.10 / -0.05 | 3/5 ✗ | -0.10 | -0.12 | ✗  time_stop_bars 60→48: -0.07R | 1 | 0.04R | 1, -1.14 (-1.14 / +0.00) | 31 / 6 of 40 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.86; max drawdown 15.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 249 | 34.1 | -0.080 | 0.89 | 41.5R | +0.01 / -0.28 | -0.25 / +0.12 | 1/5 ✗ | -0.17 | -0.26 | ✗  time_stop_bars 30→36: -0.10R | 3 | 0.17R | 4, +1.28 (+1.28 / +0.00) | 71 / 178 of 259 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.89; max drawdown 41.5R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 15m | **FAILED** | 2282 | 33.7 | -0.092 | 0.87 | 246.7R | -0.10 / -0.07 | -0.06 / -0.13 | 1/5 ✗ | -0.14 | -0.17 | ✗  stop atr 2.0→1.6: -0.11R | 1 | 0.10R | 48, -0.47 (-0.35 / -1.18) | 100 / 511 of 807 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.87; max drawdown 246.7R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 5m | **FAILED** | 1608 | 35.8 | -0.098 | 0.86 | 185.3R | -0.12 / -0.03 | -0.04 / -0.15 | 1/5 ✗ | -0.17 | -0.21 | ✗  stop atr 2.0→1.6: -0.11R | 3 | 0.13R | 33, +0.01 (+0.01 / +0.00) | 21 / 12 of 250 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.86; max drawdown 185.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1562 | 56.5 | -0.101 | 0.65 | 159.5R | -0.10 / -0.11 | -0.11 / -0.09 | 0/5 ✗ | -0.13 | -0.15 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.04R | 7, +0.02 (+0.02 / +0.02) | 617 / 4 of 817 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.65; max drawdown 159.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 301 | 43.9 | -0.104 | 0.81 | 40.4R | -0.12 / -0.07 | -0.14 / -0.06 | 0/5 ✗ | -0.16 | -0.22 | ✗  slow 21→17: -0.19R | 3 | 0.11R | 2, -0.84 (-0.49 / -1.18) | 107 / 6 of 121 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.81; max drawdown 40.4R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 5875 | 55.9 | -0.109 | 0.6 | 647.3R | -0.09 / -0.15 | -0.10 / -0.12 | 0/5 ✗ | -0.16 | -0.22 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.09R | 35, -0.08 (-0.04 / -0.20) | 819 / 10 of 1103 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.60; max drawdown 647.3R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 5m | **FAILED** | 7640 | 36.3 | -0.112 | 0.84 | 872.7R | -0.12 / -0.09 | -0.11 / -0.12 | 0/5 ✗ | -0.14 | -0.16 | ✗  stop atr 2.0→2.4: -0.12R | 0 | 0.14R | 142, -0.39 (-0.42 / +0.05) | 1225 / 5921 of 8729 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.84; max drawdown 872.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 5331 | 47.0 | -0.116 | 0.8 | 636.7R | -0.12 / -0.10 | -0.12 / -0.11 | 0/5 ✗ | -0.17 | -0.23 | ✗  stop atr 1.5→1.2: -0.14R | 0 | 0.11R | 31, -0.05 (-0.07 / -0.03) | 958 / 200 of 1477 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.80; max drawdown 636.7R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 5m | **FAILED** | 4503 | 34.9 | -0.125 | 0.83 | 602.0R | -0.14 / -0.08 | -0.09 / -0.16 | 0/5 ✗ | -0.17 | -0.18 | ✗  time_stop_bars 48→58: -0.13R | 0 | 0.15R | 68, -0.26 (-0.23 / -0.55) | 261 / 1386 of 2086 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.83; max drawdown 602.0R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 431 | 48.7 | -0.128 | 0.78 | 59.5R | -0.15 / -0.06 | -0.10 / -0.15 | 2/5 ✗ | -0.23 | -0.34 | ✗  stop atr 1.5→1.2: -0.21R | 2 | 0.18R | 13, -0.12 (-0.21 / +0.17) | 87 / 24 of 156 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.78; max drawdown 59.5R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 172 | 39.5 | -0.144 | 0.78 | 47.6R | -0.22 / +0.14 | +0.14 / -0.36 | 1/5 ✗ | -0.19 | -0.24 | ✗  bb_k 2→3: -0.28R | 1 | 0.10R | 3, +1.02 (+1.09 / +0.88) | 66 / 7 of 76 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.78; max drawdown 47.6R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 259 | 48.3 | -0.145 | 0.75 | 42.0R | -0.16 / -0.10 | -0.13 / -0.16 | 0/5 ✗ | -0.21 | -0.27 | ✗  vol_x 1.2→1.44: -0.29R | 3 | 0.14R | 3, +0.10 (-0.41 / +1.11) | 74 / 150 of 232 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.75; max drawdown 42.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 2833 | 47.6 | -0.147 | 0.75 | 427.2R | -0.13 / -0.19 | -0.12 / -0.18 | 0/5 ✗ | -0.25 | -0.33 | ✗  stop atr 1.5→1.2: -0.20R | 0 | 0.16R | 68, -0.28 (-0.26 / -0.32) | 699 / 161 of 1312 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.75; max drawdown 427.2R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 236 | 47.9 | -0.156 | 0.74 | 47.7R | -0.09 / -0.36 | -0.24 / -0.07 | 1/5 ✗ | -0.26 | -0.35 | ✗  stop atr 1.5→1.2: -0.20R | 2 | 0.18R | 3, -0.76 (-0.53 / -1.21) | 133 / 7 of 150 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.74; max drawdown 47.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 681 | 31.7 | -0.158 | 0.8 | 136.6R | -0.16 / -0.15 | -0.18 / -0.14 | 1/5 ✗ | -0.25 | -0.33 | ✗  stop buffer_atr 0.2→0.16: -0.20R | 1 | 0.18R | 11, -0.31 (-0.36 / -0.07) | 369 / 924 of 1367 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.80; max drawdown 136.6R; not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 5m | **FAILED** | 1131 | 36.7 | -0.158 | 0.65 | 182.9R | -0.18 / -0.06 | -0.21 / -0.11 | 0/5 ✗ | -0.20 | -0.19 | ✗  stop max_width_atr 3.0→2.4: -0.16R | 0 | 0.18R | 23, -0.14 (-0.09 / -1.23) | 0 / 0 of 364 | 0 | avg -0.16R/trade (needs +0.15R); profit factor 0.65; max drawdown 182.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2227 | 49.1 | -0.162 | 0.47 | 364.0R | -0.14 / -0.21 | -0.17 / -0.16 | 0/5 ✗ | -0.25 | -0.34 | ✗  stop atr 2.0→1.6: -0.21R | 0 | 0.15R | 37, -0.23 (-0.18 / -0.34) | 832 / 39 of 1020 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.47; max drawdown 364.0R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 272 | 42.6 | -0.171 | 0.7 | 50.5R | -0.11 / -0.40 | -0.21 / -0.14 | 1/5 ✗ | -0.27 | -0.34 | ✗  slow 21→25: -0.27R | 0 | 0.16R | 7, -0.72 (+1.86 / -1.15) | 77 / 18 of 112 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.70; max drawdown 50.5R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-LIMIT | 1.0 | 5m | **FAILED** | 290 | 38.6 | -0.171 | 0.64 | 53.8R | -0.18 / -0.15 | -0.22 / -0.12 | 0/5 ✗ | -0.35 | -0.35 | ✗  stop max_width_atr 3.0→3.6: -0.17R | 2 | 0.19R | 5, +0.22 (+0.22 / +0.00) | 0 / 0 of 45 | 0 | avg -0.17R/trade (needs +0.15R); profit factor 0.64; max drawdown 53.8R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 717 | 44.8 | -0.176 | 0.7 | 129.9R | -0.20 / -0.11 | -0.23 / -0.12 | 0/5 ✗ | -0.30 | -0.42 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.21R | 8, -1.07 (-0.91 / -1.33) | 74 / 10 of 99 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.70; max drawdown 129.9R; not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 5m | **FAILED** | 246 | 36.6 | -0.182 | 0.63 | 49.2R | -0.18 / -0.19 | -0.23 / -0.13 | 0/5 ✗ | -0.32 | -0.25 | ✗  stop max_width_atr 3.0→2.4: -0.18R | 2 | 0.18R | 4, +0.15 (+0.15 / +0.00) | 0 / 0 of 37 | 0 | avg -0.18R/trade (needs +0.15R); profit factor 0.63; max drawdown 49.2R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 234 | 44.9 | -0.196 | 0.66 | 50.0R | -0.22 / -0.15 | -0.30 / -0.10 | 0/5 ✗ | -0.25 | -0.30 | ✗  stop atr 2.0→1.6: -0.22R | 2 | 0.08R | 1, +0.24 (+0.00 / +0.24) | 44 / 1 of 53 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.66; max drawdown 50.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 127 | 45.7 | -0.211 | 0.64 | 27.6R | -0.14 / -0.46 | -0.21 / -0.21 | 1/5 ✗ | -0.25 | -0.32 | ✗  adx_min 20→16: -0.23R | 0 | 0.12R | 3, -0.38 (-1.16 / +0.01) | 41 / 4 of 55 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.64; max drawdown 27.6R; not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 15m | **FAILED** | 446 | 37.7 | -0.215 | 0.62 | 101.0R | -0.23 / -0.16 | -0.19 / -0.24 | 0/5 ✗ | -0.23 | -0.28 | ✗  stop max_width_atr 3.0→2.4: -0.22R | 0 | 0.17R | 10, -0.05 (-0.05 / +0.00) | 0 / 0 of 213 | 0 | avg -0.22R/trade (needs +0.15R); profit factor 0.62; max drawdown 101.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 4800 | 45.6 | -0.220 | 0.66 | 1056.5R | -0.23 / -0.19 | -0.23 / -0.21 | 0/5 ✗ | -0.35 | -0.48 | ✗  stop atr 1.5→1.2: -0.29R | 0 | 0.23R | 106, -0.47 (-0.32 / -0.77) | 1209 / 147 of 1920 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.66; max drawdown 1056.5R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 145 | 31.0 | -0.244 | 0.66 | 44.5R | -0.30 / -0.07 | -0.16 / -0.29 | 1/5 ✗ | -0.29 | -0.34 | ✗  depth 0.985→1.182: -0.36R | 0 | 0.11R | 3, -0.30 (+0.00 / -0.30) | 19 / 5 of 27 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.66; max drawdown 44.5R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 3551 | 41.5 | -0.250 | 0.31 | 887.9R | -0.22 / -0.31 | -0.26 / -0.24 | 0/5 ✗ | -0.38 | -0.52 | ✗  stop atr 2.0→1.6: -0.32R | 0 | 0.22R | 101, -0.35 (-0.32 / -0.41) | 928 / 47 of 1134 | 0 | avg -0.25R/trade (needs +0.10R); profit factor 0.31; max drawdown 887.9R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1091 | 29.4 | -0.287 | 0.63 | 315.9R | -0.31 / -0.23 | -0.25 / -0.31 | 0/5 ✗ | -0.35 | -0.42 | ✗  rsi_n 14→17: -0.38R | 1 | 0.12R | 8, -0.37 (+0.46 / -1.20) | 605 / 5 of 650 | 0 | avg -0.29R/trade (needs +0.10R); profit factor 0.63; max drawdown 315.9R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 986 | 44.7 | -0.292 | 0.57 | 289.2R | -0.29 / -0.30 | -0.27 / -0.32 | 0/5 ✗ | -0.43 | -0.55 | ✗  stop atr 1.5→1.2: -0.38R | 0 | 0.25R | 13, -0.48 (-0.43 / -0.76) | 89 / 26 of 151 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.29R/trade (needs +0.10R); profit factor 0.57; max drawdown 289.2R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1228 | 31.4 | -0.296 | 0.63 | 372.6R | -0.33 / -0.23 | -0.26 / -0.32 | 0/5 ✗ | -0.41 | -0.52 | ✗  bb_k 2→3: -0.34R | 0 | 0.18R | 29, -0.15 (+0.26 / -0.82) | 506 / 29 of 619 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.63; max drawdown 372.6R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 106 | 21.7 | -0.398 | 0.58 | 44.6R | -0.25 / -0.70 | -0.65 / -0.09 | 1/5 ✗ | -0.50 | -0.61 | ✗  time_stop_bars 30→24: -0.44R | 1 | 0.22R | 4, +0.62 (+1.31 / -1.47) | 32 / 84 of 125 | 0 | avg -0.40R/trade (needs +0.10R); profit factor 0.58; max drawdown 44.6R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 286 | 38.8 | -0.449 | 0.39 | 128.4R | -0.42 / -0.53 | -0.42 / -0.48 | 0/5 ✗ | -0.57 | -0.67 | ✗  vol_x 1.2→1.44: -0.50R | 0 | 0.24R | 8, -1.00 (-0.96 / -1.34) | 94 / 186 of 299 | 0 | avg -0.45R/trade (needs +0.10R); profit factor 0.39; max drawdown 128.4R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 1898 | 36.1 | -0.481 | 0.4 | 915.9R | -0.47 / -0.50 | -0.50 / -0.46 | 0/5 ✗ | -0.71 | -0.93 | ✗  stop atr 1.5→1.2: -0.59R | 0 | 0.39R | 43, -0.67 (-0.40 / -1.23) | 169 / 35 of 257 | 0 | not cost-viable: fees + slippage 0.39R per trade (stop must be ≥ 4x the round-trip cost); avg -0.48R/trade (needs +0.10R); profit factor 0.40; max drawdown 915.9R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-15M | 1.0 | 15m | **FAILED** | 243 | 38.3 | -0.482 | 0.37 | 120.7R | -0.43 / -0.64 | -0.46 / -0.50 | 0/5 ✗ | -0.59 | -0.68 | ✗  time_stop_bars 16→13: -0.48R | 0 | 0.44R | 7, -0.86 (-0.86 / +0.00) | 0 / 0 of 22 | 0 | not cost-viable: fees + slippage 0.44R per trade (stop must be ≥ 4x the round-trip cost); avg -0.48R/trade (needs +0.15R); profit factor 0.37; max drawdown 120.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 1030 | 38.6 | -0.483 | 0.39 | 499.6R | -0.45 / -0.59 | -0.45 / -0.53 | 0/5 ✗ | -0.67 | -0.89 | ✗  stop atr 1.0→0.8: -0.56R | 0 | 0.35R | 20, -0.75 (-0.59 / -1.68) | 79 / 215 of 328 | 0 | not cost-viable: fees + slippage 0.35R per trade (stop must be ≥ 4x the round-trip cost); avg -0.48R/trade (needs +0.10R); profit factor 0.39; max drawdown 499.6R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 473 | 25.6 | -0.483 | 0.48 | 229.0R | -0.46 / -0.55 | -0.47 / -0.49 | 0/5 ✗ | -0.62 | -0.73 | ✗  stop buffer_atr 0.2→0.16: -0.51R | 0 | 0.29R | 18, -0.62 (-0.59 / -0.71) | 377 / 885 of 1410 | 0 | not cost-viable: fees + slippage 0.29R per trade (stop must be ≥ 4x the round-trip cost); avg -0.48R/trade (needs +0.10R); profit factor 0.48; max drawdown 229.0R; not profitable in BOTH train and unseen test |
| PB-B-SWEEP | 1.0 | 5m | **FAILED** | 1042 | 34.6 | -0.624 | 0.25 | 651.0R | -0.65 / -0.55 | -0.59 / -0.65 | 0/5 ✗ | -0.76 | -0.85 | ✗  stop max_width_atr 3.0→2.4: -0.63R | 0 | 0.59R | 12, -0.44 (-0.35 / -1.48) | 0 / 0 of 45 | 0 | not cost-viable: fees + slippage 0.59R per trade (stop must be ≥ 4x the round-trip cost); avg -0.62R/trade (needs +0.15R); profit factor 0.25; max drawdown 651.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 3683 | 33.6 | -0.689 | 0.29 | 2539.2R | -0.68 / -0.72 | -0.69 / -0.69 | 0/5 ✗ | -1.08 | -1.46 | ✗  stop atr 1.0→0.8: -0.88R | 0 | 0.64R | 78, -0.82 (-0.61 / -1.63) | 198 / 518 of 813 | 0 | not cost-viable: fees + slippage 0.64R per trade (stop must be ≥ 4x the round-trip cost); avg -0.69R/trade (needs +0.10R); profit factor 0.29; max drawdown 2539.2R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **49** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 210 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.49** (Bonferroni: family-wise false-winner rate 0.05 over 210 trials; with 1 trial it would be 1.65).

**Research run duration:** 55.7 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 45 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (310.8 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 60 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

2 of 93 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 9.65 | 16.4R | 510 d (16%) | passes every gate |
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 6.24 | 15.9R | 592 d (18%) | passes every gate |

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- PB-A-GRADED v1.0 5m = near-duplicate of PB-A-APLUS v1.0 5m (82% of 77 trades shared)

- PB-B-SWEEP-LIMIT v1.0 5m = near-duplicate of PB-B-APLUS v1.0 5m (79% of 290 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (80% of 2,825 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (76% of 1,200 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 1,029 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,481 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,019 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 903 trades shared)

🧪 **Strategy lab:** 5 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 15m | 5 | +0.274 | +2.244 | +0.168 | +1.394 | too few trades to compare |
| TRD-H4-BREAKOUT | 30m | 405 | +0.139 | +0.272 | -0.008 | +0.084 | yes |
| S5-SWEEP-MSS-FVG-5M | 15m | 2 | +0.130 | +0.000 | -0.116 | -4.320 | too few trades to compare |
| TRD-H4-BREAKOUT | 1h | 899 | +0.094 | +0.248 | +0.022 | +0.065 | yes |
| TRD-H4-PULLBACK | 15m | 1061 | +0.061 | +0.256 | -0.056 | -0.039 | yes |
| TRD-H4-PULLBACK | 30m | 560 | +0.008 | +0.099 | -0.070 | -0.141 | yes |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.004 | +0.218 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +0.274 | +2.244 | too few trades to compare |
| PB-C-BREAKOUT | 5m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| PB-A-PULLBACK-CVD | 5m | 12 | -0.013 | -1.097 | -0.137 | -1.097 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 5 | -0.108 | -0.438 | -0.379 | -0.645 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 10 | -0.117 | -4.325 | +0.284 | -0.536 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 8 | -0.570 | -1.166 | -0.166 | -0.342 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 1 | -1.208 | +0.000 | -0.570 | -1.166 | too few trades to compare |
| TRD-H4-PULLBACK | 1h | 892 | +0.028 | -0.025 | -0.016 | -0.059 | yes |
| TRD-H4-PULLBACK | 5m | 2610 | -0.044 | +0.003 | -0.112 | -0.087 | yes |
| TRD-H4-BREAKOUT | 15m | 723 | -0.054 | -0.070 | -0.092 | -0.074 | yes |
| S8-PDH-PDL-SWEEP | 1h | 249 | -0.080 | -0.283 | -0.158 | -0.150 | no |
| TRD-H4-BREAKOUT | 5m | 1608 | -0.098 | -0.025 | -0.125 | -0.081 | yes |
| S8-PDH-PDL-SWEEP | 30m | 106 | -0.398 | -0.702 | -0.483 | -0.546 | no |
| PB-B-SWEEP | 5m | 1042 | -0.624 | -0.554 | +0.000 | +0.000 | too few trades to compare |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): PB-A-APLUS@1.0 5m FORMALIZED → BACKTESTING; PB-A-GRADED@1.0 5m FORMALIZED → BACKTESTING; PB-A-PULLBACK@1.0 5m FORMALIZED → BACKTESTING; PB-A-PULLBACK-CVD@1.0 5m FORMALIZED → BACKTESTING; PB-A-PULLBACK-LDN@1.0 5m FORMALIZED → BACKTESTING; PB-B-APLUS@1.0 15m FORMALIZED → BACKTESTING; PB-B-APLUS@1.0 5m FORMALIZED → FAILED; PB-B-GRADED@1.0 15m FORMALIZED → FAILED; PB-B-GRADED@1.0 5m FORMALIZED → FAILED; PB-B-SWEEP@1.0 5m FORMALIZED → FAILED; PB-B-SWEEP-15M@1.0 15m FORMALIZED → FAILED; PB-B-SWEEP-LIMIT@1.0 5m FORMALIZED → FAILED; ... and 26 more
- **Not tested (IDEA / RETIRED):** donchian_breakout-VEXIT-VRVOL v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S5 v1.0 (RETIRED)

### 3c. Research layers (daily run)
Last run: **2026-10-07 00:58 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 8 | 2017-08-17 | 2026-10-06 | 20011 |  |
| 1h | 8 | 2017-08-17 | 2026-10-06 | 79980 |  |
| 30m | 8 | 2024-10-07 | 2026-10-07 | 35040 |  |
| 15m | 8 | 2024-10-07 | 2026-10-07 | 70080 |  |
| 5m | 8 | 2024-10-07 | 2026-10-07 | 210240 |  |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 903 (536) | false_breakout, trend_reversal | false_breakout 63% | +0.47R | -0.37R | +0.29 / +0.23 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 1029 (619) | false_breakout | false_breakout 62% | +0.47R | -0.37R | +0.28 / +0.22 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 722 (431) | no_displacement, false_breakout | false_breakout 63%, no_displacement 36% | +0.46R | -0.36R | +0.26 / +0.21 |
| TRD-H4-BREAKOUT | 30m | BACKTESTING | 405 (241) | false_breakout, trend_reversal | false_breakout 76%, overextended_entry 70%, no_displacement 43%, late_entry 39% | +0.52R | -0.45R | +0.21 / +0.14 |
| donchian_breakout | 4h | BACKTESTING | 929 (421) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 66%, stop_too_tight 33%, no_displacement 33% | +0.33R | -0.37R | +0.19 / +0.14 |
| TRD-H4-BREAKOUT | 1h | BACKTESTING | 899 (558) | false_breakout | false_breakout 64% | +0.55R | -0.44R | +0.15 / +0.09 |
| TRD-H4-PULLBACK | 15m | BACKTESTING | 1061 (634) | none | - | +0.48R | -0.37R | +0.16 / +0.06 |
| TRD-H4-BREAKOUT-noT4 | 1h | BACKTESTING | 2922 (1853) | no_displacement, false_breakout | false_breakout 65% | +0.51R | -0.44R | +0.09 / +0.02 |
| bb_squeeze_breakout | 1h | BACKTESTING | 713 (340) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, no_displacement 52%, stop_too_tight 38%, regime_mismatch 35% | +0.35R | -0.47R | +0.16 / +0.01 |
| donchian_breakout-VEXIT-S4 | 30m | BACKTESTING | 923 (597) | false_breakout | false_breakout 70% | +0.46R | -0.39R | +0.13 / +0.01 |
| TRD-H4-PULLBACK | 30m | BACKTESTING | 560 (354) | none | - | +0.46R | -0.41R | +0.09 / +0.01 |
| PB-B-APLUS | 15m | BACKTESTING | 96 (55) | stop_too_tight | regime_mismatch 53%, stop_too_tight 46% | +0.33R | -0.36R | -0.04 / -0.21 |
| PB-A-GRADED | 5m | BACKTESTING | 77 (45) | stop_too_tight | stop_too_tight 40% | +0.45R | -0.30R | -0.05 / -0.23 |
| PB-A-APLUS | 5m | BACKTESTING | 63 (38) | stop_too_tight, indicator_lag | low_relative_volume 50%, stop_too_tight 47%, indicator_lag 26% | +0.44R | -0.33R | -0.06 / -0.24 |
| bb_squeeze_breakout | 4h | FAILED | 237 (114) | false_breakout, stop_too_tight, structural_change | false_breakout 57%, stop_too_tight 40%, regime_mismatch 30% | +0.34R | -0.34R | +0.13 / +0.05 |
| TRD-H4-PULLBACK | 1h | FAILED | 892 (554) | low_relative_volume, indicator_lag, structural_change | low_relative_volume 55%, indicator_lag 25% | +0.45R | -0.40R | +0.08 / +0.03 |
| S6-OB-FVG-noSMC | 15m | FAILED | 64 (37) | none | stop_too_wide 89%, regime_mismatch 35% | +0.35R | -0.42R | +0.14 / -0.00 |
| donchian_breakout-VEXIT | 30m | FAILED | 1019 (664) | false_breakout | false_breakout 70% | +0.46R | -0.39R | +0.13 / -0.01 |
| TRD-H4-BREAKOUT-noT4 | 30m | FAILED | 1307 (829) | false_breakout | false_breakout 71% | +0.51R | -0.46R | +0.08 / -0.01 |
| macd_trend_cross | 1h | FAILED | 162 (79) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 92%, indicator_lag 39%, stop_too_tight 32% | +0.31R | -0.40R | +0.12 / -0.01 |
| TRD-H4-PULLBACK-noT4 | 1h | FAILED | 4122 (2573) | structural_change | - | +0.50R | -0.42R | +0.05 / -0.02 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1200 (783) | false_breakout | false_breakout 71% | +0.47R | -0.41R | +0.12 / -0.02 |
| macd_trend_cross | 4h | FAILED | 32 (15) | none | regime_mismatch 93%, no_displacement 87%, low_relative_volume 53%, indicator_lag 53% | +0.17R | -0.44R | +0.05 / -0.03 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2049 (1386) | false_breakout, regime_mismatch | false_breakout 62% | +0.52R | -0.38R | +0.06 / -0.03 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2825 (1908) | false_breakout, regime_mismatch | false_breakout 63% | +0.50R | -0.39R | +0.07 / -0.03 |
| donchian_breakout-VEXIT | 1h | FAILED | 2481 (1680) | false_breakout | false_breakout 63% | +0.51R | -0.39R | +0.06 / -0.03 |
| donchian_breakout | 30m | FAILED | 1053 (537) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 75%, stop_too_tight 33% | +0.28R | -0.40R | +0.10 / -0.03 |
| donchian_breakout | 1h | FAILED | 2549 (1323) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 37%, stop_too_tight 32%, regime_mismatch 26% | +0.37R | -0.39R | +0.05 / -0.04 |
| TRD-H4-PULLBACK | 5m | FAILED | 2610 (1628) | overextended_entry | - | +0.51R | -0.42R | +0.09 / -0.04 |
| TRD-H4-BREAKOUT | 15m | FAILED | 723 (473) | false_breakout | false_breakout 78%, range_market 38% | +0.44R | -0.51R | +0.04 / -0.05 |
| TRD-H4-PULLBACK-noT4 | 15m | FAILED | 3699 (2334) | none | - | +0.49R | -0.41R | +0.06 / -0.06 |
| trend_pullback | 4h | FAILED | 1029 (532) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 38%, stop_too_tight 26% | +0.36R | -0.43R | +0.01 / -0.06 |
| TRD-H4-PULLBACK-noT4 | 30m | FAILED | 2097 (1365) | htf_conflict | - | +0.50R | -0.41R | +0.02 / -0.07 |
| supertrend_flip | 4h | FAILED | 79 (42) | indicator_lag, structural_change | regime_mismatch 67%, indicator_lag 40% | +0.39R | -0.44R | -0.01 / -0.08 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 249 (164) | stop_too_tight, sweep_continued, structural_change | sweep_continued 97%, range_market 57%, stop_too_tight 30% | +0.57R | -0.41R | +0.13 / -0.08 |
| TRD-H4-BREAKOUT-noT4 | 15m | FAILED | 2282 (1513) | range_market, false_breakout | false_breakout 76%, range_market 39% | +0.44R | -0.44R | +0.02 / -0.09 |
| TRD-H4-BREAKOUT | 5m | FAILED | 1608 (1033) | false_breakout | false_breakout 75% | +0.44R | -0.44R | +0.04 / -0.10 |
| rsi2_dip_buy | 4h | FAILED | 1562 (680) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 45% | +0.16R | -0.21R | -0.05 / -0.10 |
| ema_9_21_cross | 1h | FAILED | 301 (169) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 47%, stop_too_tight 26% | +0.29R | -0.38R | +0.02 / -0.10 |
| rsi2_dip_buy | 1h | FAILED | 5875 (2590) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 42% | +0.15R | -0.21R | +0.00 / -0.11 |
| TRD-H4-PULLBACK-noT4 | 5m | FAILED | 7640 (4868) | none | - | +0.50R | -0.43R | +0.04 / -0.11 |
| trend_pullback | 1h | FAILED | 5331 (2823) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 76%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.43R | +0.02 / -0.12 |
| TRD-H4-BREAKOUT-noT4 | 5m | FAILED | 4503 (2933) | false_breakout | false_breakout 74% | +0.48R | -0.44R | +0.03 / -0.12 |
| bb_squeeze_breakout | 30m | FAILED | 431 (221) | false_breakout, stop_too_tight | false_breakout 60%, stop_too_tight 37% | +0.25R | -0.47R | +0.10 / -0.13 |
| R4-CLUC | 30m | FAILED | 172 (104) | none | wrong_session 66% | +0.30R | -0.42R | -0.04 / -0.14 |
| liquidity_sweep_reversal | 1h | FAILED | 259 (134) | stop_too_tight | stop_too_tight 51% | +0.26R | -0.47R | +0.02 / -0.14 |
| trend_pullback | 30m | FAILED | 2833 (1484) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 31% | +0.27R | -0.43R | +0.05 / -0.15 |
| macd_trend_cross | 30m | FAILED | 236 (123) | stop_too_tight, indicator_lag | low_relative_volume 46%, indicator_lag 40%, stop_too_tight 28% | +0.34R | -0.48R | +0.05 / -0.16 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 681 (465) | range_market, stop_too_tight | range_market 47%, stop_too_tight 36% | +0.62R | -0.51R | +0.06 / -0.16 |
| PB-B-GRADED | 5m | FAILED | 1131 (716) | none | - | +0.22R | -0.25R | +0.01 / -0.16 |
| rsi2_dip_buy | 30m | FAILED | 2227 (1134) | volatility_spike, fees_slippage | fees_slippage 31% | +0.16R | -0.19R | +0.01 / -0.16 |
| ema_9_21_cross | 30m | FAILED | 272 (156) | indicator_lag | indicator_lag 46%, low_relative_volume 39% | +0.27R | -0.37R | +0.01 / -0.17 |
| PB-B-SWEEP-LIMIT | 5m | FAILED | 290 (178) | low_relative_volume | - | +0.23R | -0.27R | +0.01 / -0.17 |
| ema_9_21_cross | 15m | FAILED | 717 (396) | late_entry, stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 26% | +0.25R | -0.41R | +0.08 / -0.18 |
| PB-B-APLUS | 5m | FAILED | 246 (156) | low_relative_volume | - | +0.20R | -0.33R | -0.01 / -0.18 |
| supertrend_flip | 1h | FAILED | 234 (129) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 72%, regime_mismatch 70%, stop_too_tight 39%, indicator_lag 32% | +0.39R | -0.38R | -0.10 / -0.20 |
| supertrend_flip | 30m | FAILED | 127 (69) | stop_too_tight, indicator_lag | regime_mismatch 44%, indicator_lag 41%, stop_too_tight 38%, overextended_entry 32% | +0.28R | -0.47R | -0.07 / -0.21 |
| PB-B-GRADED | 15m | FAILED | 446 (278) | stop_too_tight | stop_too_tight 37% | +0.34R | -0.35R | -0.05 / -0.21 |
| trend_pullback | 15m | FAILED | 4800 (2610) | range_market, stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 32% | +0.26R | -0.44R | +0.06 / -0.22 |
| R4-CLUC | 15m | FAILED | 145 (100) | none | wrong_session 71% | +0.35R | -0.28R | -0.13 / -0.24 |
| rsi2_dip_buy | 15m | FAILED | 3551 (2079) | wrong_session, trend_reversal, regime_mismatch, fees_slippage | fees_slippage 38% | +0.15R | -0.19R | +0.01 / -0.25 |
| R4-BBRSI | 1h | FAILED | 1091 (770) | none | - | +0.44R | -0.45R | -0.13 / -0.29 |
| bb_squeeze_breakout | 15m | FAILED | 986 (545) | false_breakout, stop_too_tight | false_breakout 62%, stop_too_tight 38% | +0.28R | -0.48R | +0.02 / -0.29 |
| R4-BBRSI | 30m | FAILED | 1228 (843) | none | - | +0.42R | -0.43R | -0.07 / -0.30 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 106 (83) | stop_too_tight, sweep_continued | sweep_continued 98%, stop_too_tight 25% | +0.57R | -0.62R | -0.11 / -0.40 |
| liquidity_sweep_reversal | 30m | FAILED | 286 (175) | stop_too_tight | stop_too_tight 39% | +0.38R | -0.51R | -0.18 / -0.45 |
| ema_9_21_cross | 5m | FAILED | 1898 (1213) | stop_too_tight, indicator_lag | indicator_lag 52%, stop_too_tight 31% | +0.22R | -0.45R | +0.01 / -0.48 |
| PB-B-SWEEP-15M | 15m | FAILED | 243 (150) | low_relative_volume, stop_too_tight | stop_too_tight 32%, low_relative_volume 27% | +0.24R | -0.45R | +0.01 / -0.48 |
| liquidity_sweep_reversal | 15m | FAILED | 1030 (632) | stop_too_tight | stop_too_tight 39% | +0.29R | -0.48R | -0.06 / -0.48 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 473 (352) | stop_too_tight | stop_too_tight 34% | +0.59R | -0.51R | -0.13 / -0.48 |
| PB-B-SWEEP | 5m | FAILED | 1042 (681) | range_market, low_relative_volume, stop_too_tight | stop_too_tight 34%, range_market 28% | +0.14R | -0.38R | +0.06 / -0.62 |
| liquidity_sweep_reversal | 5m | FAILED | 3683 (2446) | range_market, stop_too_tight | stop_too_tight 40% | +0.26R | -0.50R | +0.10 / -0.69 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 32 strategy/timeframe tests); `false_breakout` (systematic in 24 strategy/timeframe tests); `indicator_lag` (systematic in 15 strategy/timeframe tests); `regime_mismatch` (systematic in 14 strategy/timeframe tests); `trend_reversal` (systematic in 6 strategy/timeframe tests); `range_market` (systematic in 5 strategy/timeframe tests); `low_relative_volume` (systematic in 5 strategy/timeframe tests); `no_displacement` (systematic in 4 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests)

**Missed moves:** no strong move in the last 24 hours at the last research run.

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 126.7 KB | - | - |
| `memory/cleanup_log.md` | 0.5 KB | - | - |
| `memory/coin_notes.md` | 14.3 KB | 14 | 2026-10-04 02:31 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 12.7 KB | 28 | 2026-10-07 05:20 UTC |
| `memory/experiments.md` | 61.5 KB | 24 | 2026-10-06 15:30 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 237.4 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 15.8 KB | - | - |
| `memory/missed_trades.md` | 36.1 KB | 50 | 2026-10-06 15:30 UTC |
| `memory/playbook.md` | 10.0 KB | - | - |
| `memory/research_sources.md` | 89.1 KB | 70 | 2026-10-07 00:58 UTC |
| `memory/smc_events.csv` | 1092.9 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 25.3 KB | - | - |
| `memory/strategy_registry.csv` | 64.5 KB | - | - |
| `memory/trials.csv` | 15.2 KB | - | - |
| `memory/universe_log.md` | 20.6 KB | - | - |

**Reviews due** (review date passed; for the reviews): `missed_trades.md` LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00 (2026-10-02); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03); `missed_trades.md` SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells (2026-10-03); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03) … and 12 more
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG and SHORT = OKX futures fees + funding (always charged, never received). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*