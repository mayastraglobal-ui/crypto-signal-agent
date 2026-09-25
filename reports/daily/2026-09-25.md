# Crypto Signal Report

**Updated:** 2026-09-25 10:17 Beijing time (2026-09-25 02:17 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 1.5 MB (GitHub) · large files of this run 1.6 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-25 02:17 UTC / 2026-09-25 10:17 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · ⚠ calendar not maintained - no event listed for the next 7 days (config.yaml -> events)
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked, never emailed). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.07% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| PROVE | **DEGRADED** | 1d: DEGRADED: volume 52x normal on candle 09-23 00:00 UTC (possible bad data); 1d: DEGRADED: volume 245x normal on candle 09-24 00:00 UTC (possible bad data) |
- 72 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **XRP**, **SOL**, **ZEC**, **LTC**, **BNB**
- **Research only** - backtested, never a signal: UNI, SUI, ENA
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** PROVE - order book too thin: $67k within 1% (need $250k)
  - **EXCLUDED** SAGA - 7-day average volume $21M < $50M; order book too thin: $19k within 1% (need $250k)
  - **EXCLUDED** LINK - 7-day average volume $44M < $50M

| Not eligible | 24h volume | Why |
|---|---|---|
| PROVE | $161M | order book too thin: $67k within 1% (need $250k) |
| ONDO | $128M | 7-day average volume $43M < $50M; 24h move +28.7% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $184k within 1% (need $250k) |
| SAGA | $53M | 7-day average volume $21M < $50M; order book too thin: $19k within 1% (need $250k) |
| LINK | $52M | 7-day average volume $44M < $50M |

**Flags (not excluded):** PROVE: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, PEPE, RLUSD, TAO, USD1, USDC (see `config.yaml`)

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
| LTC | 458 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-12 | OK (300 candles) |
| BNB | 463 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| UNI | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| SUI | 177 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| ENA | 129 | 906 | 900 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | up (HH/HL) | 84,942.4 / 83,948.4 | 0.57 | 0.66x | 0.92x | bull_engulf |
| ETH | up (HH/HL) | 2,706 / 2,676.03 | 0.44 | 0.39x | 0.92x | bull_engulf, bear_reject |
| XRP | mixed (HH/LL) | 1.5435 / 1.4517 | 0.29 | 0.71x | 0.92x | - |
| SOL | up (HH/HL) | 117.79 / 116.12 | 0.41 | 0.74x | 0.89x | - |
| ZEC | up (HH/HL) | 1,574.6 / 1,523.32 | 0.37 | 0.53x | 0.96x | bear_reject |
| LTC | mixed (LH/HL) | 72.42 / 70.38 | 0.44 | 0.30x | 1.65x | bull_engulf, bear_engulf |
| BNB | up (HH/HL) | 786.29 / 775.35 | 0.73 | 0.52x | 0.78x | bear_reject |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 450 | 48% | 35% | 28% | 79% | 44% | 30% | can't tell from chance | 0.12R |
| 4h | displacement_down | 365 | 48% | 32% | 22% | 75% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1228 | 44% | 30% | 21% | 78% | 43% | 29% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1378 | 44% | 29% | 20% | 77% | 48% | 32% | worse than chance | 0.08R |
| 4h | bull_reject | 914 | 41% | 27% | 19% | 80% | 43% | 29% | can't tell from chance | 0.13R |
| 4h | bear_reject | 919 | 47% | 33% | 24% | 73% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 672 | 43% | 29% | 21% | 78% | 43% | 28% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 674 | 43% | 29% | 19% | 79% | 48% | 32% | worse than chance | 0.08R |
| 4h | smc_bos_up | 290 | 44% | 28% | 20% | 82% | 45% | 31% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 244 | 53% | 40% | 27% | 67% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 81 | 49% | 33% | 27% | 80% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 75 | 40% | 24% | 12% | 77% | 47% | 33% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 653 | 44% | 29% | 23% | 77% | 43% | 30% | can't tell from chance | 0.12R |
| 4h | smc_fvg_retrace_bear | 663 | 48% | 33% | 21% | 75% | 48% | 32% | can't tell from chance | 0.08R |
| 1h | displacement_up | 610 | 47% | 34% | 26% | 74% | 42% | 29% | beats chance | 0.27R |
| 1h | displacement_down | 433 | 37% | 23% | 14% | 81% | 38% | 24% | can't tell from chance | 0.18R |
| 1h | bull_engulf | 1720 | 40% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.32R |
| 1h | bear_engulf | 1884 | 39% | 25% | 17% | 80% | 38% | 25% | can't tell from chance | 0.19R |
| 1h | bull_reject | 1415 | 40% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.31R |
| 1h | bear_reject | 1336 | 35% | 24% | 17% | 82% | 39% | 25% | worse than chance | 0.18R |
| 1h | smc_sweep_bull | 640 | 40% | 26% | 18% | 78% | 42% | 30% | can't tell from chance | 0.31R |
| 1h | smc_sweep_bear | 706 | 37% | 24% | 16% | 81% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 409 | 43% | 31% | 23% | 78% | 42% | 29% | can't tell from chance | 0.27R |
| 1h | smc_bos_down | 278 | 37% | 27% | 18% | 82% | 39% | 25% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 114 | 50% | 37% | 30% | 71% | 43% | 31% | can't tell from chance | 0.33R |
| 1h | smc_choch_down | 112 | 46% | 29% | 16% | 73% | 39% | 25% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 885 | 45% | 32% | 24% | 72% | 42% | 29% | can't tell from chance | 0.30R |
| 1h | smc_fvg_retrace_bear | 806 | 41% | 28% | 19% | 78% | 38% | 25% | can't tell from chance | 0.20R |
| 30m | displacement_up | 628 | 42% | 32% | 26% | 77% | 42% | 30% | can't tell from chance | 0.30R |
| 30m | displacement_down | 408 | 39% | 24% | 14% | 83% | 37% | 22% | can't tell from chance | 0.20R |
| 30m | bull_engulf | 1727 | 41% | 28% | 20% | 76% | 41% | 29% | can't tell from chance | 0.36R |
| 30m | bear_engulf | 1760 | 35% | 21% | 15% | 82% | 36% | 21% | can't tell from chance | 0.22R |
| 30m | bull_reject | 1346 | 44% | 29% | 21% | 74% | 41% | 29% | can't tell from chance | 0.36R |
| 30m | bear_reject | 1401 | 37% | 23% | 15% | 81% | 36% | 22% | can't tell from chance | 0.21R |
| 30m | smc_sweep_bull | 625 | 39% | 26% | 16% | 76% | 40% | 28% | can't tell from chance | 0.37R |
| 30m | smc_sweep_bear | 630 | 41% | 26% | 17% | 83% | 36% | 21% | beats chance | 0.21R |
| 30m | smc_bos_up | 464 | 40% | 33% | 27% | 77% | 43% | 30% | can't tell from chance | 0.33R |
| 30m | smc_bos_down | 233 | 35% | 22% | 13% | 85% | 36% | 21% | can't tell from chance | 0.24R |
| 30m | smc_choch_up | 97 | 37% | 23% | 16% | 84% | 42% | 30% | can't tell from chance | 0.39R |
| 30m | smc_choch_down | 100 | 36% | 21% | 16% | 82% | 34% | 21% | can't tell from chance | 0.19R |
| 30m | smc_fvg_retrace_bull | 980 | 41% | 28% | 21% | 76% | 41% | 29% | can't tell from chance | 0.37R |
| 30m | smc_fvg_retrace_bear | 821 | 38% | 22% | 16% | 81% | 35% | 21% | can't tell from chance | 0.24R |
| 15m | displacement_up | 483 | 36% | 27% | 20% | 82% | 36% | 25% | can't tell from chance | 0.43R |
| 15m | displacement_down | 461 | 34% | 21% | 13% | 85% | 35% | 22% | can't tell from chance | 0.28R |
| 15m | bull_engulf | 1660 | 38% | 27% | 19% | 78% | 35% | 24% | beats chance | 0.51R |
| 15m | bear_engulf | 1606 | 36% | 24% | 15% | 79% | 36% | 22% | can't tell from chance | 0.30R |
| 15m | bull_reject | 1339 | 35% | 23% | 16% | 80% | 35% | 24% | can't tell from chance | 0.52R |
| 15m | bear_reject | 1467 | 36% | 22% | 14% | 81% | 36% | 23% | can't tell from chance | 0.29R |
| 15m | smc_sweep_bull | 591 | 37% | 25% | 20% | 78% | 35% | 24% | can't tell from chance | 0.47R |
| 15m | smc_sweep_bear | 630 | 38% | 25% | 15% | 83% | 37% | 23% | can't tell from chance | 0.29R |
| 15m | smc_bos_up | 342 | 39% | 28% | 22% | 80% | 36% | 24% | can't tell from chance | 0.42R |
| 15m | smc_bos_down | 349 | 33% | 20% | 13% | 85% | 35% | 21% | can't tell from chance | 0.33R |
| 15m | smc_choch_up | 91 | 36% | 24% | 19% | 79% | 37% | 26% | can't tell from chance | 0.46R |
| 15m | smc_choch_down | 90 | 33% | 21% | 13% | 81% | 36% | 23% | can't tell from chance | 0.27R |
| 15m | smc_fvg_retrace_bull | 1017 | 33% | 23% | 16% | 80% | 36% | 25% | can't tell from chance | 0.49R |
| 15m | smc_fvg_retrace_bear | 976 | 37% | 25% | 16% | 80% | 36% | 22% | can't tell from chance | 0.31R |
| 5m | displacement_up | 1193 | 31% | 21% | 16% | 84% | 28% | 19% | beats chance | 0.80R |
| 5m | displacement_down | 1145 | 29% | 19% | 13% | 86% | 31% | 21% | can't tell from chance | 0.54R |
| 5m | bull_engulf | 4139 | 26% | 18% | 13% | 83% | 27% | 19% | can't tell from chance | 0.89R |
| 5m | bear_engulf | 4066 | 32% | 21% | 14% | 83% | 31% | 20% | can't tell from chance | 0.55R |
| 5m | bull_reject | 3477 | 27% | 18% | 14% | 81% | 27% | 19% | can't tell from chance | 0.91R |
| 5m | bear_reject | 3669 | 32% | 21% | 15% | 82% | 31% | 21% | can't tell from chance | 0.52R |
| 5m | smc_sweep_bull | 1231 | 31% | 22% | 16% | 79% | 29% | 21% | can't tell from chance | 0.79R |
| 5m | smc_sweep_bear | 1282 | 35% | 24% | 17% | 81% | 32% | 21% | can't tell from chance | 0.45R |
| 5m | smc_bos_up | 816 | 29% | 20% | 16% | 85% | 27% | 19% | can't tell from chance | 0.83R |
| 5m | smc_bos_down | 883 | 29% | 19% | 12% | 86% | 31% | 21% | can't tell from chance | 0.57R |
| 5m | smc_choch_up | 212 | 36% | 24% | 17% | 86% | 28% | 20% | beats chance | 0.89R |
| 5m | smc_choch_down | 217 | 28% | 18% | 14% | 85% | 30% | 20% | can't tell from chance | 0.52R |
| 5m | smc_fvg_retrace_bull | 3248 | 28% | 19% | 13% | 82% | 27% | 19% | can't tell from chance | 0.90R |
| 5m | smc_fvg_retrace_bear | 2961 | 28% | 19% | 12% | 85% | 31% | 21% | worse than chance | 0.55R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (weak) | WEAK_BULL (moderate) | TRANSITION (moderate) | WEAK_BULL (weak) | LONG allowed (1D/1H bullish, 1W TRANSITION) |
| **ETH** | UNCLEAR (weak) | WEAK_BULL (weak) | TRANSITION (moderate) | RANGE (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H RANGE)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | WEAK_BULL (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BULL, 1H TRANSITION)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (weak) | UNCLEAR (weak) | WEAK_BULL (weak) | LONG allowed (1D/1H bullish, 1W TRANSITION) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | WEAK_BULL (weak) | LONG allowed (1D/4H/1H bullish, 1W WEAK_BULL) |
| **LTC** | TRANSITION (weak) | EXPANSION up (weak) | EXPANSION up (moderate) | WEAK_BULL (weak) | LONG allowed (1D/4H/1H bullish, 1W TRANSITION) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | UNCLEAR (weak) | WEAK_BULL (weak) | LONG allowed (1D/1H bullish, 1W WEAK_BULL) |
| **UNI** | EXPANSION up (weak) | EXPANSION up (strong) | TRANSITION (weak) | RANGE (strong) | NO TRADE (timeframes disagree (1D EXPANSION, 4H TRANSITION, 1H RANGE)) |
| **SUI** | RANGE (weak) | TRANSITION (weak) | TRANSITION (weak) | WEAK_BULL (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H WEAK_BULL)) |
| **ENA** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (weak) | EXPANSION up (weak) | LONG allowed (1D/4H/1H bullish, 1W TRANSITION) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (weak)** - for: EMA-fast rising (+1.1 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.72x normal, Bollinger width above 52% of the last 100 candles · against: EMAs not lined up; ADX 27 is close to a threshold
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.1 ATR in 10 candles); ADX 44 = strong trend; candle size 1.16x normal, Bollinger width above 79% of the last 100 candles; volume 1.40x normal · against: swing structure mixed (neutral)
- **4H TRANSITION (moderate)** - for: close above EMA-fast above EMA-slow; swing structure down (LH/LL); ADX 29 = strong trend; candle size 1.24x normal, Bollinger width above 56% of the last 100 candles · against: EMA-fast flat (+0.8 ATR in 10 candles)
- **1H WEAK_BULL (weak)** - for: close above EMA-fast above EMA-slow; swing structure up (HH/HL); candle size 0.92x normal, Bollinger width above 50% of the last 100 candles · against: EMA-fast flat (-0.1 ATR in 10 candles) (neutral); ADX 21 = in between (20-25); ADX 21 is close to a threshold; volume only 0.56x normal (weak participation)

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **Asia**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (BOS 15 candles ago) | buy-side (bearish idea) 4 candles ago | bull 84,193.62-84,269.99 | bear 86,133.40-86,975.51 | premium (67%) | swing high 84,942.45 (0.64 ATR) | swing low 83,948.43 (1.28 ATR) |
| **ETH** | down (BOS 15 candles ago) | buy-side (bearish idea) 4 candles ago | bull 2,675.72-2,679.23 (retraced) | bear 2,745.99-2,784.40 | discount (45%) | equal highs 2,706.00 (0.78 ATR) | swing low 2,676.03 (0.64 ATR) |
| **XRP** | up (BOS 8 candles ago) | buy-side (bearish idea) 17 candles ago | bull 1.5156-1.5195 (retraced) | bull 1.3773-1.3856 | premium (97%) | swing high 1.6581 (5.61 ATR) | swing low 1.4517 (4.29 ATR) |
| **SOL** | up (BOS 0 candles ago) | buy-side (bearish idea) 4 candles ago | bull 116.84-116.97 | bear 117.85-119.66 | premium (81%) | swing high 119.77 (2.13 ATR) | swing low 116.12 (1.25 ATR) |
| **ZEC** | up (BOS 8 candles ago) | buy-side (bearish idea) 39 candles ago | bull 1,517.23-1,526.13 (retraced) | bull 1,098.88-1,133.82 | discount (41%) | swing high 1,574.60 (1.11 ATR) | swing low 1,523.32 (0.78 ATR) |
| **LTC** | up (BOS 18 candles ago) | sell-side (bullish idea) 15 candles ago | bear 72.340-72.720 (retraced) | bull 58.800-63.080 | premium (62%) | swing high 72.420 (0.47 ATR) | swing low 70.380 (0.77 ATR) |
| **BNB** | up (BOS 39 candles ago) | sell-side (bullish idea) 15 candles ago | bear 781.33-782.43 (retraced) | bear 787.07-797.61 | discount (26%) | swing high 786.29 (1.73 ATR) | swing low 775.35 (0.62 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 71 (Greed), yesterday 71  (extreme fear/greed = bigger, faster moves)

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
- ⚠️ **calendar not maintained - no event listed for the next 7 days (config.yaml -> events)**

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-09-25 00:49 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged, never emailed.
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1162 | 53.5 | +0.090 | 1.2 | 25.3R | +0.08 / +0.11 | +0.07 / +0.11 | 4/5 | +0.06 | stable | 6 | 0.04R | 14, +0.18 (+0.60 / -0.38) | 89 / 51 of 262 | 0 | avg +0.09R/trade (needs +0.10R); profit factor 1.20; max drawdown 25.3R |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 2 / 4 of 6 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 54 / 15 of 74 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 34 / 11 of 51 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 2 / 4 of 6 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 22 / 13 of 36 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 3 | 33.3 | -0.018 | 0.98 | 2.3R | -1.13 / +2.21 | +2.21 / -1.13 | 0/5 ✗ | -0.10 | ✗  sweep_bars 8→10: -0.33R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 22 / 13 of 36 | 0 | only 3 trades; avg -0.02R/trade (needs +0.10R); profit factor 0.98; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 13 | 46.2 | -0.180 | 0.69 | 4.7R | -0.47 / +0.78 | -0.31 / -0.12 | 0/5 ✗ | -0.04 | ✗  stop max_width_atr 3.0→3.6: -0.25R | 0 | 0.16R | 2, +0.05 (+0.05 / +0.00) | 486 / 227 of 842 | 0 | only 13 trades; avg -0.18R/trade (needs +0.10R); profit factor 0.69; only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 13 | 38.5 | -0.244 | 0.73 | 7.9R | -0.75 / +0.56 | -0.09 / -0.42 | 0/5 ✗ | -0.64 | ✗  sweep_bars 8→10: -0.49R | 0 | 0.39R | 2, +0.31 (+1.94 / -1.32) | 49 / 29 of 84 | 0 | not cost-viable: fees + slippage 0.39R per trade (stop must be ≥ 4x the round-trip cost); only 13 trades; avg -0.24R/trade (needs +0.10R); profit factor 0.73; only 5 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 13 | 23.1 | -0.424 | 0.39 | 6.1R | -0.63 / -0.10 | -1.17 / -0.20 | 0/5 ✗ | -0.55 | ✗  stop buffer_atr 0.2→0.24: -0.49R | 0 | 0.11R | 0, +0.00 (+0.00 / +0.00) | 524 / 223 of 947 | 0 | only 13 trades; avg -0.42R/trade (needs +0.10R); profit factor 0.39; only 5 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 4 | 25.0 | -0.845 | 0.41 | 3.4R | -0.69 / -1.32 | -1.32 / -0.69 | 0/5 ✗ | -3.93 | ✗  stop buffer_atr 0.2→0.24: -3.68R | 0 | 0.33R | 1, -1.32 (+0.00 / -1.32) | 34 / 11 of 51 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); only 4 trades; avg -0.85R/trade (needs +0.10R); profit factor 0.41; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 6 | 0.0 | -1.363 | 0.0 | 8.2R | -1.19 / -1.70 | -1.42 / -1.35 | 0/5 ✗ | -1.46 | ✗  stop max_width_atr 3.0→2.4: -1.42R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 54 / 15 of 74 | 0 | only 6 trades; avg -1.36R/trade (needs +0.10R); profit factor 0.00; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.712 | 0.0 | 1.7R | +0.00 / -1.71 | -1.71 / +0.00 | 0/5 ✗ | -2.00 | ✗  stop buffer_atr 0.2→0.16: -1.75R | 0 | 0.86R | 0, +0.00 (+0.00 / +0.00) | 33 / 99 of 143 | 0 | not cost-viable: fees + slippage 0.86R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.71R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 294 | 53.1 | +0.044 | 1.09 | 26.9R | +0.17 / -0.22 | +0.12 / -0.02 | 3/5 ✗ | +0.00 | stable | 6 | 0.07R | 2, +0.08 (-1.11 / +1.27) | 98 / 22 of 134 | 0 | avg +0.04R/trade (needs +0.10R); profit factor 1.09; max drawdown 26.9R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 39 | 53.8 | +0.016 | 1.03 | 6.0R | +0.20 / -0.46 | +0.27 / -0.28 | 2/5 ✗ | -0.01 | ✗  time_stop_bars 40→32: -0.01R | 1 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 157 / 5 of 164 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.03; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 209 | 51.7 | -0.009 | 0.98 | 33.9R | -0.12 / +0.23 | -0.03 / +0.01 | 3/5 ✗ | -0.07 | ✗  stop atr 1.5→1.2: -0.06R | 4 | 0.13R | 1, -0.02 (+0.00 / -0.02) | 210 / 6 of 218 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 33.9R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 96 | 47.9 | -0.025 | 0.95 | 18.2R | +0.18 / -0.40 | -0.01 / -0.04 | 3/5 ✗ | -0.05 | ✗  st_k 3→2: -0.08R | 2 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 42 / 7 of 51 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.95; max drawdown 18.2R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 871 | 51.0 | -0.051 | 0.91 | 65.5R | -0.06 / -0.04 | -0.09 / -0.01 | 0/5 ✗ | -0.14 | ✗  stop atr 1.5→1.2: -0.09R | 3 | 0.14R | 4, -0.44 (-1.18 / +0.29) | 127 / 46 of 205 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.91; max drawdown 65.5R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 3117 | 48.2 | -0.061 | 0.88 | 225.5R | -0.08 / -0.03 | -0.07 / -0.05 | 0/5 ✗ | -0.11 | ✗  stop atr 2.0→1.6: -0.08R | 1 | 0.09R | 31, +0.26 (+0.13 / +0.39) | 129 / 110 of 428 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.88; max drawdown 225.5R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1289 | 48.2 | -0.076 | 0.86 | 130.5R | -0.03 / -0.19 | +0.01 / -0.17 | 1/5 ✗ | -0.12 | ✗  long_rsi_hi 65→52: -0.18R | 3 | 0.06R | 7, +1.25 (+1.35 / +1.17) | 632 / 199 of 998 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.86; max drawdown 130.5R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1282 | 48.7 | -0.080 | 0.85 | 130.7R | -0.09 / -0.05 | -0.05 / -0.11 | 1/5 ✗ | -0.15 | ✗  stop atr 2.0→1.6: -0.15R | 2 | 0.13R | 44, -0.06 (-0.06 / -0.06) | 134 / 65 of 449 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.85; max drawdown 130.7R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1975 | 56.4 | -0.101 | 0.64 | 198.5R | -0.10 / -0.10 | -0.13 / -0.08 | 0/5 ✗ | -0.13 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.05R | 12, -0.20 (-0.20 / +0.00) | 772 / 5 of 1042 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.64; max drawdown 198.5R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 325 | 33.5 | -0.118 | 0.85 | 55.7R | -0.09 / -0.19 | -0.35 / +0.10 | 1/5 ✗ | -0.22 | ✗  time_stop_bars 30→36: -0.14R | 2 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 91 / 235 of 335 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.85; max drawdown 55.7R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 7315 | 54.0 | -0.125 | 0.55 | 916.8R | -0.10 / -0.17 | -0.14 / -0.11 | 0/5 ✗ | -0.19 | ✗  stop atr 2.0→1.6: -0.15R | 0 | 0.11R | 34, -0.20 (-0.28 / -0.01) | 1012 / 6 of 1362 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.55; max drawdown 916.8R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 365 | 45.2 | -0.126 | 0.77 | 54.0R | -0.12 / -0.13 | -0.16 / -0.09 | 0/5 ✗ | -0.19 | ✗  slow 21→17: -0.23R | 2 | 0.12R | 3, -1.00 (+0.00 / -1.00) | 149 / 11 of 168 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.77; max drawdown 54.0R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 285 | 47.7 | -0.142 | 0.75 | 46.6R | -0.13 / -0.17 | -0.20 / -0.09 | 2/5 ✗ | -0.22 | ✗  stop atr 2.0→1.6: -0.18R | 3 | 0.09R | 4, +0.17 (+0.00 / +0.17) | 55 / 2 of 66 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.75; max drawdown 46.6R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 158 | 48.1 | -0.142 | 0.75 | 24.9R | -0.18 / -0.03 | -0.20 / -0.10 | 2/5 ✗ | -0.21 | ✗  adx_min 20→16: -0.18R | 2 | 0.14R | 6, -0.74 (-0.69 / -0.80) | 54 / 5 of 69 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.75; max drawdown 24.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6580 | 47.1 | -0.146 | 0.75 | 977.2R | -0.14 / -0.15 | -0.19 / -0.10 | 0/5 ✗ | -0.22 | ✗  stop atr 1.5→1.2: -0.18R | 0 | 0.13R | 45, +0.07 (-0.22 / +0.35) | 1201 / 316 of 1883 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.75; max drawdown 977.2R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 868 | 32.3 | -0.176 | 0.78 | 182.4R | -0.13 / -0.26 | -0.22 / -0.14 | 1/5 ✗ | -0.28 | ✗  stop buffer_atr 0.2→0.16: -0.22R | 1 | 0.21R | 10, -0.18 (-1.32 / +0.31) | 486 / 1185 of 1751 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.78; max drawdown 182.4R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 304 | 48.0 | -0.187 | 0.7 | 66.8R | -0.15 / -0.28 | -0.32 / -0.07 | 0/5 ✗ | -0.33 | ✗  stop atr 1.5→1.2: -0.27R | 1 | 0.21R | 5, -0.08 (+0.66 / -1.18) | 172 / 11 of 202 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.70; max drawdown 66.8R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 449 | 44.3 | -0.195 | 0.68 | 94.2R | -0.21 / -0.15 | -0.26 / -0.16 | 1/5 ✗ | -0.35 | ✗  stop atr 1.5→1.2: -0.30R | 1 | 0.27R | 21, +0.00 (+0.14 / -0.34) | 65 / 18 of 110 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.19R/trade (needs +0.10R); profit factor 0.68; max drawdown 94.2R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3435 | 46.0 | -0.201 | 0.68 | 711.9R | -0.19 / -0.23 | -0.23 / -0.17 | 0/5 ✗ | -0.32 | ✗  stop atr 1.5→1.2: -0.25R | 0 | 0.19R | 76, +0.20 (+0.15 / +0.25) | 804 / 247 of 1668 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 711.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2795 | 45.9 | -0.211 | 0.37 | 592.4R | -0.19 / -0.25 | -0.25 / -0.17 | 0/5 ✗ | -0.32 | ✗  stop atr 2.0→1.6: -0.27R | 0 | 0.18R | 34, -0.11 (-0.17 / +0.08) | 1042 / 24 of 1253 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.37; max drawdown 592.4R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 37 | 35.1 | -0.212 | 0.69 | 11.1R | +0.05 / -0.59 | -0.46 / -0.00 | 1/5 ✗ | -0.32 | ✗  time_stop_bars 30→24: -0.26R | 2 | 0.16R | 6, -0.26 (+1.40 / -0.59) | 111 / 36 of 161 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.69; max drawdown 11.1R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 329 | 47.4 | -0.221 | 0.64 | 73.6R | -0.23 / -0.21 | -0.24 / -0.19 | 0/5 ✗ | -0.32 | ✗  vol_x 1.2→1.44: -0.33R | 2 | 0.17R | 5, -0.41 (-1.11 / -0.23) | 109 / 221 of 338 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.64; max drawdown 73.6R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 471 | 44.4 | -0.251 | 0.62 | 118.7R | -0.30 / -0.13 | -0.28 / -0.23 | 0/5 ✗ | -0.36 | ✗  stop atr 1.5→1.2: -0.33R | 0 | 0.20R | 14, -0.32 (-0.45 / -0.08) | 115 / 29 of 186 | 0 | avg -0.25R/trade (needs +0.10R); profit factor 0.62; max drawdown 118.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 2983 | 45.0 | -0.256 | 0.61 | 771.7R | -0.25 / -0.28 | -0.30 / -0.23 | 0/5 ✗ | -0.42 | ✗  stop atr 1.5→1.2: -0.34R | 0 | 0.27R | 157, -0.06 (-0.16 / +0.07) | 1342 / 345 of 2272 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.61; max drawdown 771.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 348 | 39.4 | -0.257 | 0.58 | 91.2R | -0.26 / -0.25 | -0.40 / -0.15 | 0/5 ✗ | -0.35 | ✗  slow 21→25: -0.36R | 0 | 0.17R | 9, -0.10 (-0.08 / -0.11) | 101 / 17 of 134 | 0 | avg -0.26R/trade (needs +0.10R); profit factor 0.58; max drawdown 91.2R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 2143 | 32.7 | -0.356 | 0.19 | 763.4R | -0.35 / -0.38 | -0.44 / -0.28 | 0/5 ✗ | -0.53 | ✗  hi 90→108: -0.44R | 0 | 0.30R | 57, -0.24 (-0.28 / -0.07) | 1193 / 35 of 1376 | 0 | not cost-viable: fees + slippage 0.30R per trade (stop must be ≥ 4x the round-trip cost); avg -0.36R/trade (needs +0.10R); profit factor 0.19; max drawdown 763.4R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 540 | 41.9 | -0.357 | 0.5 | 193.9R | -0.35 / -0.37 | -0.32 / -0.38 | 0/5 ✗ | -0.52 | ✗  stop atr 1.5→1.2: -0.43R | 0 | 0.31R | 36, -0.72 (-0.47 / -1.05) | 110 / 46 of 215 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); avg -0.36R/trade (needs +0.10R); profit factor 0.50; max drawdown 193.9R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 616 | 25.5 | -0.442 | 0.55 | 280.8R | -0.46 / -0.40 | -0.58 / -0.34 | 0/5 ✗ | -0.61 | ✗  n 20→24: -0.47R | 1 | 0.35R | 18, +0.08 (-1.41 / +0.65) | 458 / 1074 of 1710 | 0 | not cost-viable: fees + slippage 0.35R per trade (stop must be ≥ 4x the round-trip cost); avg -0.44R/trade (needs +0.10R); profit factor 0.55; max drawdown 280.8R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 329 | 39.2 | -0.444 | 0.4 | 146.5R | -0.41 / -0.54 | -0.44 / -0.45 | 0/5 ✗ | -0.60 | ✗  stop atr 1.0→0.8: -0.48R | 0 | 0.29R | 13, -0.50 (-0.19 / -0.59) | 116 / 212 of 353 | 0 | not cost-viable: fees + slippage 0.29R per trade (stop must be ≥ 4x the round-trip cost); avg -0.44R/trade (needs +0.10R); profit factor 0.40; max drawdown 146.5R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 567 | 38.6 | -0.507 | 0.37 | 289.3R | -0.50 / -0.52 | -0.59 / -0.47 | 0/5 ✗ | -0.72 | ✗  stop atr 1.0→0.8: -0.55R | 0 | 0.39R | 27, -0.52 (-0.68 / -0.43) | 102 / 234 of 369 | 0 | not cost-viable: fees + slippage 0.39R per trade (stop must be ≥ 4x the round-trip cost); avg -0.51R/trade (needs +0.10R); profit factor 0.37; max drawdown 289.3R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 117 | 21.4 | -0.527 | 0.46 | 64.7R | -0.43 / -0.71 | -0.71 / -0.38 | 0/5 ✗ | -0.65 | ✗  stop max_width_atr 3.0→2.4: -0.53R | 0 | 0.26R | 4, +0.38 (-1.25 / +2.00) | 33 / 99 of 143 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.53R/trade (needs +0.10R); profit factor 0.46; max drawdown 64.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 256 | 29.3 | -0.745 | 0.25 | 192.4R | -0.88 / -0.56 | -0.66 / -1.10 | 0/5 ✗ | -1.13 | ✗  stop atr 1.5→1.2: -0.94R | 0 | 0.63R | 61, -0.57 (-0.53 / -0.65) | 200 / 78 of 346 | 0 | not cost-viable: fees + slippage 0.63R per trade (stop must be ≥ 4x the round-trip cost); avg -0.74R/trade (needs +0.10R); profit factor 0.25; max drawdown 192.4R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 419 | 26.0 | -1.175 | 0.15 | 495.0R | -1.26 / -1.07 | -1.08 / -1.65 | 0/5 ✗ | -1.86 | ✗  stop atr 1.0→0.8: -1.53R | 0 | 1.08R | 109, -1.16 (-1.25 / -1.09) | 187 / 628 of 932 | 0 | not cost-viable: fees + slippage 1.08R per trade (stop must be ≥ 4x the round-trip cost); avg -1.17R/trade (needs +0.10R); profit factor 0.15; max drawdown 495.0R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **20** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.212 | -0.592 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +2.214 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET | 15m | 3 | -0.018 | +2.214 | -0.244 | +0.561 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 4 | -0.845 | -1.323 | -0.180 | +0.779 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 6 | -1.363 | -1.701 | -0.424 | -0.101 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 1 | -1.712 | -1.712 | -0.732 | -0.931 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 325 | -0.118 | -0.191 | -0.176 | -0.264 | yes |
| S8-PDH-PDL-SWEEP | 30m | 117 | -0.527 | -0.710 | -0.442 | -0.404 | no |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): S5-SWEEP-MSS-FVG-5M@1.0 15m FORMALIZED → BACKTESTING; S5-SWEEP-MSS-FVG-5M@1.0 30m FORMALIZED → BACKTESTING; S6-OB-FVG-5M@1.0 15m FORMALIZED → BACKTESTING; S6-OB-FVG-noSMC@1.0 15m BACKTESTING → FAILED; S7-SILVER-BULLET-5M@1.0 15m FORMALIZED → BACKTESTING; S8-PDH-PDL-SWEEP@1.0 1h BACKTESTING → FAILED; S8-PDH-PDL-SWEEP@1.0 30m BACKTESTING → FAILED; S8-PDH-PDL-SWEEP-5M@1.0 30m FORMALIZED → BACKTESTING; S8-PDH-PDL-SWEEP-noSMC@1.0 1h BACKTESTING → FAILED; S8-PDH-PDL-SWEEP-noSMC@1.0 30m BACKTESTING → FAILED; bb_squeeze_breakout@1.0 1h BACKTESTING → FAILED; bb_squeeze_breakout@1.0 4h BACKTESTING → FAILED; ... and 14 more

### 3c. Research layers (daily run)
Last run: **2026-09-25 00:49 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 10 | 2017-08-17 | 2026-09-24 | 19939 |  |
| 1h | 10 | 2017-08-17 | 2026-09-24 | 79692 |  |
| 30m | 10 | 2024-09-25 | 2026-09-25 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 10 | 2025-09-25 | 2026-09-25 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 10 | 2026-06-27 | 2026-09-25 | 25918 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout | 4h | BACKTESTING | 1162 (540) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 67%, stop_too_tight 35% | +0.35R | -0.39R | +0.15 / +0.09 |
| bb_squeeze_breakout | 4h | FAILED | 294 (138) | false_breakout, stop_too_tight, structural_change | false_breakout 59%, stop_too_tight 43%, regime_mismatch 28% | +0.33R | -0.35R | +0.13 / +0.04 |
| macd_trend_cross | 4h | FAILED | 39 (18) | structural_change | regime_mismatch 94%, no_displacement 89%, indicator_lag 61%, low_relative_volume 56% | +0.18R | -0.45R | +0.10 / +0.02 |
| macd_trend_cross | 1h | FAILED | 209 (101) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 93%, wrong_session 72%, indicator_lag 40%, stop_too_tight 32% | +0.32R | -0.40R | +0.15 / -0.01 |
| supertrend_flip | 4h | FAILED | 96 (50) | stop_too_tight, indicator_lag, structural_change | regime_mismatch 68%, indicator_lag 34%, stop_too_tight 26% | +0.47R | -0.44R | +0.04 / -0.03 |
| bb_squeeze_breakout | 1h | FAILED | 871 (427) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 61%, no_displacement 53%, stop_too_tight 38%, regime_mismatch 35% | +0.35R | -0.44R | +0.12 / -0.05 |
| donchian_breakout | 1h | FAILED | 3117 (1616) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 37%, stop_too_tight 31% | +0.36R | -0.40R | +0.04 / -0.06 |
| trend_pullback | 4h | FAILED | 1289 (668) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 81%, indicator_lag 39%, stop_too_tight 25% | +0.35R | -0.42R | +0.00 / -0.08 |
| donchian_breakout | 30m | FAILED | 1282 (658) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 76%, stop_too_tight 33% | +0.29R | -0.41R | +0.08 / -0.08 |
| rsi2_dip_buy | 4h | FAILED | 1975 (862) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 45% | +0.16R | -0.21R | -0.04 / -0.10 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 325 (216) | stop_too_tight, sweep_continued | sweep_continued 97%, range_market 54%, stop_too_tight 32% | +0.54R | -0.40R | +0.13 / -0.12 |
| rsi2_dip_buy | 1h | FAILED | 7315 (3362) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 42% | +0.16R | -0.20R | +0.01 / -0.12 |
| ema_9_21_cross | 1h | FAILED | 365 (200) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 48%, stop_too_tight 26% | +0.27R | -0.38R | +0.02 / -0.13 |
| supertrend_flip | 1h | FAILED | 285 (149) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 72%, regime_mismatch 69%, stop_too_tight 38%, indicator_lag 34% | +0.38R | -0.38R | -0.03 / -0.14 |
| supertrend_flip | 30m | FAILED | 158 (82) | stop_too_tight, indicator_lag | indicator_lag 45%, regime_mismatch 44%, stop_too_tight 38%, late_entry 30% | +0.28R | -0.47R | +0.03 / -0.14 |
| trend_pullback | 1h | FAILED | 6580 (3482) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 77%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.42R | +0.01 / -0.15 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 868 (588) | range_market, stop_too_tight | range_market 47%, stop_too_tight 36% | +0.62R | -0.49R | +0.08 / -0.18 |
| macd_trend_cross | 30m | FAILED | 304 (158) | stop_too_tight, indicator_lag | no_displacement 87%, low_relative_volume 46%, indicator_lag 44%, stop_too_tight 32% | +0.33R | -0.44R | +0.06 / -0.19 |
| ema_9_21_cross | 15m | FAILED | 449 (250) | htf_conflict, stop_too_tight, indicator_lag | indicator_lag 47%, stop_too_tight 30% | +0.27R | -0.41R | +0.12 / -0.20 |
| trend_pullback | 30m | FAILED | 3435 (1856) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 30% | +0.28R | -0.43R | +0.03 / -0.20 |
| rsi2_dip_buy | 30m | FAILED | 2795 (1512) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 34% | +0.17R | -0.19R | +0.00 / -0.21 |
| S6-OB-FVG-noSMC | 15m | FAILED | 37 (24) | structural_change | regime_mismatch 29% | +0.37R | -0.58R | -0.02 / -0.21 |
| liquidity_sweep_reversal | 1h | FAILED | 329 (173) | stop_too_tight | stop_too_tight 51% | +0.26R | -0.47R | -0.02 / -0.22 |
| bb_squeeze_breakout | 30m | FAILED | 471 (262) | false_breakout, stop_too_tight | false_breakout 64%, stop_too_tight 39% | +0.23R | -0.46R | +0.01 / -0.25 |
| trend_pullback | 15m | FAILED | 2983 (1642) | htf_conflict, wrong_session, stop_too_tight, indicator_lag | wrong_session 71%, indicator_lag 50%, stop_too_tight 31% | +0.25R | -0.44R | +0.07 / -0.26 |
| ema_9_21_cross | 30m | FAILED | 348 (211) | stop_too_tight, indicator_lag | indicator_lag 47%, low_relative_volume 40%, stop_too_tight 28% | +0.26R | -0.36R | -0.04 / -0.26 |
| rsi2_dip_buy | 15m | FAILED | 2143 (1443) | trend_reversal, fees_slippage | fees_slippage 45% | +0.17R | -0.18R | -0.00 / -0.36 |
| bb_squeeze_breakout | 15m | FAILED | 540 (314) | no_displacement, stop_too_tight | false_breakout 58%, no_displacement 57%, range_market 52%, stop_too_tight 44% | +0.32R | -0.45R | +0.01 / -0.36 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 616 (459) | stop_too_tight | stop_too_tight 32% | +0.59R | -0.49R | -0.02 / -0.44 |
| liquidity_sweep_reversal | 30m | FAILED | 329 (200) | stop_too_tight | stop_too_tight 41% | +0.36R | -0.47R | -0.11 / -0.44 |
| liquidity_sweep_reversal | 15m | FAILED | 567 (348) | stop_too_tight | stop_too_tight 38% | +0.37R | -0.46R | -0.01 / -0.51 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 117 (92) | trend_reversal, stop_too_tight, sweep_continued | sweep_continued 96%, stop_too_tight 29% | +0.52R | -0.66R | -0.19 / -0.53 |
| ema_9_21_cross | 5m | FAILED | 256 (181) | stop_too_tight, indicator_lag | indicator_lag 51%, stop_too_tight 30% | +0.22R | -0.42R | +0.01 / -0.74 |
| liquidity_sweep_reversal | 5m | FAILED | 419 (310) | stop_too_tight | stop_too_tight 37% | +0.26R | -0.48R | +0.17 / -1.18 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 28 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `regime_mismatch` (systematic in 11 strategy/timeframe tests); `false_breakout` (systematic in 6 strategy/timeframe tests); `trend_reversal` (systematic in 6 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `no_displacement` (systematic in 3 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests); `htf_conflict` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- LTC up +14.2% (2026-09-24 01:00 → 2026-09-24 14:00 UTC): identifiable: at least one strategy had a valid signal before the move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 3.7 KB | - | - |
| `memory/changelog.md` | 51.6 KB | - | - |
| `memory/coin_notes.md` | 0.6 KB | - | - |
| `memory/execution_notes.md` | 1.4 KB | 2 | 2026-09-24 23:16 UTC |
| `memory/experiments.md` | 4.5 KB | - | - |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 0.8 KB | - | - |
| `memory/market_regime_log.md` | 2.5 KB | - | - |
| `memory/missed_trades.md` | 1.4 KB | 1 | 2026-09-25 00:49 UTC |
| `memory/research_sources.md` | 21.1 KB | 20 | 2026-09-25 00:49 UTC |
| `memory/smc_events.csv` | 8.4 KB | - | - |
| `memory/smc_research.md` | 5.7 KB | - | - |
| `memory/strategy_lifecycle.md` | 12.6 KB | - | - |
| `memory/strategy_registry.csv` | 22.2 KB | - | - |
| `memory/universe_log.md` | 1.9 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*