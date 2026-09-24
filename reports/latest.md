# Crypto Signal Report

**Updated:** 2026-09-25 05:17 Beijing time (2026-09-24 21:17 UTC) · data: Binance · 8 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.08% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| PROVE | **DEGRADED** | 1d: DEGRADED: volume 52x normal on candle 09-23 00:00 UTC (possible bad data) |
- 59 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **ZEC**, **SOL**, **XRP**, **BNB**, **UNI**
- **Research only** - backtested, never a signal: SUI
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** PROVE - 7-day average volume $36M < $50M; spread 0.128% > 0.1%; order book too thin: $49k within 1% (need $250k)

| Not eligible | 24h volume | Why |
|---|---|---|
| PROVE | $179M | 7-day average volume $36M < $50M; spread 0.128% > 0.1%; order book too thin: $49k within 1% (need $250k) |
| LTC | $148M | 7-day average volume $34M < $50M |
| ONDO | $114M | 7-day average volume $30M < $50M; 24h move +25.7% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $216k within 1% (need $250k) |

**Flags (not excluded):** PROVE: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, PEPE, RLUSD, USD1, USDC (see `config.yaml`)

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
| BNB | 463 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| UNI | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| SUI | 177 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (HH/LL) | 84,942.4 / 82,874.9 | 0.61 | 0.72x | 1.09x | - |
| ETH | mixed (HH/LL) | 2,706 / 2,600.15 | 0.41 | 0.87x | 1.12x | bull_engulf |
| ZEC | mixed (HH/LL) | 1,539.7 / 1,456.92 | 0.53 | 0.94x | 1.10x | bear_reject |
| SOL | mixed (HH/LL) | 117.79 / 112.52 | 0.22 | 0.67x | 1.02x | bull_engulf |
| XRP | mixed (HH/LL) | 1.5435 / 1.4517 | 0.68 | 0.67x | 0.97x | - |
| BNB | mixed (HH/LL) | 786.29 / 763.04 | 0.72 | 0.63x | 0.92x | bull_engulf, bull_reject |
| UNI | down (LH/LL) | 9.401 / 8.787 | 0.18 | 0.36x | 0.88x | - |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 375 | 47% | 34% | 27% | 79% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | displacement_down | 308 | 49% | 32% | 22% | 75% | 46% | 32% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 979 | 44% | 30% | 20% | 78% | 43% | 30% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1100 | 44% | 30% | 21% | 76% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | bull_reject | 734 | 41% | 28% | 19% | 79% | 43% | 29% | can't tell from chance | 0.13R |
| 4h | bear_reject | 718 | 48% | 34% | 24% | 73% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 529 | 43% | 29% | 21% | 77% | 42% | 29% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 528 | 44% | 29% | 18% | 81% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 228 | 44% | 29% | 21% | 81% | 44% | 31% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 201 | 51% | 38% | 28% | 68% | 49% | 32% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 68 | 51% | 35% | 28% | 81% | 42% | 28% | can't tell from chance | 0.14R |
| 4h | smc_choch_down | 63 | 43% | 24% | 13% | 78% | 50% | 35% | can't tell from chance | 0.09R |
| 4h | smc_fvg_retrace_bull | 524 | 44% | 28% | 22% | 77% | 42% | 29% | can't tell from chance | 0.13R |
| 4h | smc_fvg_retrace_bear | 535 | 49% | 32% | 21% | 74% | 48% | 33% | can't tell from chance | 0.08R |
| 1h | displacement_up | 501 | 47% | 35% | 27% | 72% | 42% | 29% | can't tell from chance | 0.29R |
| 1h | displacement_down | 345 | 39% | 24% | 14% | 82% | 37% | 24% | can't tell from chance | 0.20R |
| 1h | bull_engulf | 1366 | 41% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.34R |
| 1h | bear_engulf | 1531 | 39% | 26% | 18% | 79% | 37% | 24% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1147 | 40% | 28% | 21% | 75% | 42% | 29% | can't tell from chance | 0.33R |
| 1h | bear_reject | 1064 | 35% | 23% | 17% | 83% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_sweep_bull | 493 | 40% | 27% | 19% | 77% | 42% | 29% | can't tell from chance | 0.33R |
| 1h | smc_sweep_bear | 564 | 35% | 23% | 15% | 81% | 38% | 24% | can't tell from chance | 0.20R |
| 1h | smc_bos_up | 333 | 43% | 30% | 23% | 79% | 44% | 30% | can't tell from chance | 0.28R |
| 1h | smc_bos_down | 219 | 39% | 28% | 19% | 82% | 39% | 25% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 97 | 48% | 37% | 30% | 71% | 42% | 31% | can't tell from chance | 0.34R |
| 1h | smc_choch_down | 97 | 45% | 29% | 15% | 76% | 36% | 24% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 723 | 45% | 33% | 25% | 71% | 42% | 29% | can't tell from chance | 0.32R |
| 1h | smc_fvg_retrace_bear | 649 | 40% | 27% | 18% | 80% | 37% | 24% | can't tell from chance | 0.21R |
| 30m | displacement_up | 493 | 42% | 31% | 26% | 76% | 40% | 29% | can't tell from chance | 0.35R |
| 30m | displacement_down | 323 | 40% | 24% | 14% | 83% | 36% | 22% | can't tell from chance | 0.22R |
| 30m | bull_engulf | 1396 | 40% | 28% | 20% | 76% | 40% | 28% | can't tell from chance | 0.39R |
| 30m | bear_engulf | 1457 | 35% | 22% | 15% | 82% | 35% | 21% | can't tell from chance | 0.24R |
| 30m | bull_reject | 1077 | 43% | 28% | 21% | 74% | 40% | 28% | can't tell from chance | 0.37R |
| 30m | bear_reject | 1136 | 37% | 24% | 16% | 81% | 36% | 21% | can't tell from chance | 0.23R |
| 30m | smc_sweep_bull | 497 | 37% | 27% | 17% | 77% | 40% | 28% | can't tell from chance | 0.40R |
| 30m | smc_sweep_bear | 513 | 41% | 26% | 18% | 82% | 36% | 21% | beats chance | 0.23R |
| 30m | smc_bos_up | 374 | 42% | 35% | 29% | 74% | 41% | 28% | can't tell from chance | 0.33R |
| 30m | smc_bos_down | 196 | 34% | 23% | 14% | 85% | 36% | 21% | can't tell from chance | 0.27R |
| 30m | smc_choch_up | 77 | 35% | 21% | 16% | 82% | 39% | 28% | can't tell from chance | 0.42R |
| 30m | smc_choch_down | 75 | 41% | 25% | 19% | 79% | 34% | 21% | can't tell from chance | 0.21R |
| 30m | smc_fvg_retrace_bull | 791 | 42% | 29% | 22% | 75% | 40% | 28% | can't tell from chance | 0.40R |
| 30m | smc_fvg_retrace_bear | 641 | 36% | 21% | 16% | 81% | 36% | 21% | can't tell from chance | 0.26R |
| 15m | displacement_up | 372 | 35% | 27% | 20% | 82% | 34% | 24% | can't tell from chance | 0.47R |
| 15m | displacement_down | 365 | 35% | 21% | 14% | 84% | 35% | 22% | can't tell from chance | 0.33R |
| 15m | bull_engulf | 1331 | 36% | 25% | 18% | 79% | 34% | 24% | can't tell from chance | 0.57R |
| 15m | bear_engulf | 1305 | 35% | 24% | 15% | 79% | 35% | 22% | can't tell from chance | 0.34R |
| 15m | bull_reject | 1079 | 34% | 23% | 16% | 80% | 34% | 24% | can't tell from chance | 0.58R |
| 15m | bear_reject | 1171 | 35% | 22% | 15% | 81% | 35% | 22% | can't tell from chance | 0.33R |
| 15m | smc_sweep_bull | 485 | 36% | 26% | 20% | 79% | 36% | 25% | can't tell from chance | 0.53R |
| 15m | smc_sweep_bear | 505 | 35% | 24% | 14% | 84% | 37% | 23% | can't tell from chance | 0.32R |
| 15m | smc_bos_up | 266 | 43% | 30% | 23% | 79% | 36% | 26% | beats chance | 0.45R |
| 15m | smc_bos_down | 286 | 34% | 20% | 14% | 86% | 35% | 22% | can't tell from chance | 0.37R |
| 15m | smc_choch_up | 74 | 28% | 19% | 12% | 86% | 31% | 23% | can't tell from chance | 0.52R |
| 15m | smc_choch_down | 78 | 32% | 19% | 13% | 81% | 34% | 24% | can't tell from chance | 0.29R |
| 15m | smc_fvg_retrace_bull | 824 | 30% | 21% | 15% | 82% | 34% | 24% | can't tell from chance | 0.55R |
| 15m | smc_fvg_retrace_bear | 771 | 35% | 24% | 16% | 80% | 35% | 22% | can't tell from chance | 0.36R |
| 5m | displacement_up | 957 | 29% | 20% | 15% | 85% | 27% | 19% | can't tell from chance | 0.88R |
| 5m | displacement_down | 948 | 29% | 19% | 13% | 85% | 30% | 20% | can't tell from chance | 0.60R |
| 5m | bull_engulf | 3356 | 25% | 17% | 12% | 83% | 26% | 18% | can't tell from chance | 0.98R |
| 5m | bear_engulf | 3360 | 31% | 21% | 14% | 83% | 30% | 20% | can't tell from chance | 0.60R |
| 5m | bull_reject | 2797 | 25% | 17% | 12% | 82% | 26% | 18% | can't tell from chance | 0.99R |
| 5m | bear_reject | 2885 | 31% | 20% | 14% | 82% | 30% | 20% | can't tell from chance | 0.60R |
| 5m | smc_sweep_bull | 986 | 29% | 21% | 15% | 79% | 27% | 19% | can't tell from chance | 0.84R |
| 5m | smc_sweep_bear | 1033 | 33% | 23% | 16% | 81% | 31% | 21% | can't tell from chance | 0.49R |
| 5m | smc_bos_up | 635 | 27% | 20% | 15% | 86% | 26% | 18% | can't tell from chance | 0.93R |
| 5m | smc_bos_down | 727 | 30% | 20% | 13% | 85% | 30% | 20% | can't tell from chance | 0.63R |
| 5m | smc_choch_up | 172 | 33% | 22% | 14% | 88% | 26% | 17% | can't tell from chance | 1.02R |
| 5m | smc_choch_down | 169 | 27% | 15% | 11% | 86% | 29% | 19% | can't tell from chance | 0.64R |
| 5m | smc_fvg_retrace_bull | 2626 | 27% | 18% | 13% | 81% | 25% | 17% | can't tell from chance | 1.02R |
| 5m | smc_fvg_retrace_bear | 2383 | 27% | 18% | 12% | 85% | 30% | 20% | worse than chance | 0.63R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (weak) | TRANSITION (strong) | TRANSITION (moderate) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)) |
| **ETH** | UNCLEAR (weak) | WEAK_BULL (weak) | TRANSITION (moderate) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H UNCLEAR)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | UNCLEAR (weak) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |
| **SOL** | TRANSITION (weak) | TRANSITION (strong) | TRANSITION (weak) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H TRANSITION)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | WEAK_BULL (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BULL, 1H UNCLEAR)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | UNCLEAR (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H UNCLEAR)) |
| **UNI** | EXPANSION up (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W EXPANSION) |
| **SUI** | RANGE (weak) | EXPANSION up (weak) | TRANSITION (moderate) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D EXPANSION, 4H TRANSITION, 1H TRANSITION)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (weak)** - for: EMA-fast rising (+1.1 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.72x normal, Bollinger width above 52% of the last 100 candles · against: EMAs not lined up; ADX 27 is close to a threshold
- **1D TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.0 ATR in 10 candles); swing structure down (LH/LL); ADX 45 = strong trend; candle size 1.18x normal, Bollinger width above 78% of the last 100 candles · against: -
- **4H TRANSITION (moderate)** - for: close above EMA-fast above EMA-slow; swing structure down (LH/LL); ADX 32 = strong trend; candle size 1.28x normal, Bollinger width above 56% of the last 100 candles · against: EMA-fast flat (+0.9 ATR in 10 candles)
- **1H TRANSITION (weak)** - for: ADX 26 = strong trend; candle size 1.09x normal, Bollinger width above 31% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.3 ATR in 10 candles); swing structure mixed; ADX 26 is close to a threshold

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (CHOCH 51 candles ago) | buy-side (bearish idea) 35 candles ago | bear 84,886.92-85,550.30 (retraced) | bear 86,133.40-86,975.51 | premium (72%) | swing high 84,942.45 (0.95 ATR) | swing low 82,874.93 (2.48 ATR) |
| **ETH** | down (BOS 51 candles ago) | buy-side (bearish idea) 18 candles ago | bull 2,675.72-2,679.23 | bear 2,745.99-2,784.40 | premium (83%) | equal highs 2,706.00 (0.69 ATR) | swing low 2,600.15 (3.43 ATR) |
| **ZEC** | up (CHOCH 19 candles ago) | buy-side (bearish idea) 19 candles ago | bull 1,517.23-1,526.13 | bull 1,098.88-1,133.82 | above the range (108%) | swing high 1,679.83 (4.29 ATR) | swing low 1,456.92 (2.88 ATR) |
| **SOL** | up (BOS 19 candles ago) | buy-side (bearish idea) 18 candles ago | bull 115.10-115.59 | bear 117.85-119.66 | premium (82%) | swing high 117.79 (0.77 ATR) | swing low 112.52 (3.47 ATR) |
| **XRP** | up (BOS 19 candles ago) | buy-side (bearish idea) 17 candles ago | bull 1.5156-1.5195 (retraced) | bull 1.3773-1.3856 | premium (86%) | swing high 1.5435 (0.58 ATR) | swing low 1.4517 (3.59 ATR) |
| **BNB** | up (BOS 19 candles ago) | buy-side (bearish idea) 30 candles ago | bear 781.33-782.43 (retraced) | bear 787.07-797.61 | premium (71%) | swing high 786.29 (1.24 ATR) | equal lows 763.04 (2.98 ATR) |
| **UNI** | down (BOS 51 candles ago) | sell-side (bullish idea) 46 candles ago | bull 8.9510-9.0010 (retraced) | bull 8.6780-9.0640 | premium (76%) | swing high 9.4010 (0.77 ATR) | swing low 8.7870 (2.41 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 71 (Greed), yesterday 71  (extreme fear/greed = bigger, faster moves)

## 2. Signals right now
Only **APPROVED** strategy versions (your yes, after paper trading) give signals and emails.

**No trade passes all the checks right now. That is normal - no trade is also a position.**

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (not run yet); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged, never emailed.
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian_breakout | 1.0 | 4h | **VALIDATION** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 11, +0.18 (+0.54 / -0.25) | 73 / 44 of 209 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout | 1.0 | 1h | **VALIDATION** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 24, +0.41 (+0.30 / +0.52) | 100 / 73 of 322 | 0 | waiting for the first daily research run (Layers B/C) |
| trend_pullback | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 67, +0.16 (+0.24 / +0.07) | 660 / 175 of 1359 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 4h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 2, +0.08 (-1.11 / +1.27) | 86 / 20 of 116 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 4, -0.44 (-1.18 / +0.29) | 111 / 33 of 171 | 0 | waiting for the first daily research run (Layers B/C) |
| macd_trend_cross | 1.0 | 4h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 125 / 5 of 132 | 0 | waiting for the first daily research run (Layers B/C) |
| macd_trend_cross | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 1, -0.02 (+0.00 / -0.02) | 166 / 3 of 171 | 0 | waiting for the first daily research run (Layers B/C) |
| macd_trend_cross | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 4, +0.18 (+0.85 / -0.50) | 139 / 8 of 162 | 0 | waiting for the first daily research run (Layers B/C) |
| supertrend_flip | 1.0 | 4h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 1, +1.82 (+1.82 / +0.00) | 32 / 7 of 41 | 0 | waiting for the first daily research run (Layers B/C) |
| supertrend_flip | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 4, +0.17 (+0.00 / +0.17) | 48 / 1 of 56 | 0 | waiting for the first daily research run (Layers B/C) |
| supertrend_flip | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 6, -0.74 (-0.69 / -0.80) | 45 / 5 of 59 | 0 | waiting for the first daily research run (Layers B/C) |
| liquidity_sweep_reversal | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 5, -0.41 (-1.11 / -0.23) | 86 / 163 of 256 | 0 | waiting for the first daily research run (Layers B/C) |
| liquidity_sweep_reversal | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 11, -0.59 (-0.19 / -0.75) | 91 / 162 of 273 | 0 | waiting for the first daily research run (Layers B/C) |
| ema_9_21_cross | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 3, -1.00 (+0.00 / -1.00) | 117 / 5 of 129 | 0 | waiting for the first daily research run (Layers B/C) |
| ema_9_21_cross | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 7, +0.20 (+0.29 / +0.13) | 86 / 14 of 111 | 0 | waiting for the first daily research run (Layers B/C) |
| ema_9_21_cross | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 17, +0.28 (+0.48 / -0.08) | 54 / 11 of 89 | 0 | waiting for the first daily research run (Layers B/C) |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 46 / 9 of 58 | 0 | waiting for the first daily research run (Layers B/C) |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 1, -1.32 (+0.00 / -1.32) | 30 / 10 of 46 | 0 | waiting for the first daily research run (Layers B/C) |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 428 / 178 of 774 | 0 | waiting for the first daily research run (Layers B/C) |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 2, +0.05 (+0.05 / +0.00) | 390 / 177 of 677 | 0 | waiting for the first daily research run (Layers B/C) |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 2 / 3 of 5 | 0 | waiting for the first daily research run (Layers B/C) |
| S6-OB-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 5, -0.10 (+1.40 / -0.48) | 94 / 27 of 134 | 0 | waiting for the first daily research run (Layers B/C) |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 21 / 10 of 32 | 0 | waiting for the first daily research run (Layers B/C) |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 2, +0.31 (+1.94 / -1.32) | 39 / 22 of 67 | 0 | waiting for the first daily research run (Layers B/C) |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 73 / 179 of 260 | 0 | waiting for the first daily research run (Layers B/C) |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 2, -1.25 (-1.25 / +0.00) | 26 / 82 of 116 | 0 | waiting for the first daily research run (Layers B/C) |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 10, -0.18 (-1.18 / +0.07) | 392 / 926 of 1394 | 0 | waiting for the first daily research run (Layers B/C) |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 18, +0.08 (-1.35 / +0.48) | 356 / 819 of 1326 | 0 | waiting for the first daily research run (Layers B/C) |
| trend_pullback | 1.0 | 4h | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 6, +1.14 (+1.35 / +0.94) | 499 / 166 of 800 | 0 | waiting for the first daily research run (Layers B/C) |
| trend_pullback | 1.0 | 1h | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 37, -0.03 (-0.25 / +0.17) | 965 / 241 of 1507 | 0 | waiting for the first daily research run (Layers B/C) |
| trend_pullback | 1.0 | 15m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 135, -0.08 (-0.22 / +0.13) | 1065 / 241 of 1817 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout | 1.0 | 30m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 38, -0.05 (-0.19 / +0.11) | 119 / 39 of 369 | 0 | waiting for the first daily research run (Layers B/C) |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 11, -0.29 (-0.29 / +0.00) | 616 / 3 of 831 | 0 | waiting for the first daily research run (Layers B/C) |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 24, -0.27 (-0.37 / -0.08) | 853 / 3 of 1141 | 0 | waiting for the first daily research run (Layers B/C) |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 24, -0.16 (-0.25 / +0.13) | 835 / 20 of 996 | 0 | waiting for the first daily research run (Layers B/C) |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 44, -0.25 (-0.29 / +0.03) | 986 / 35 of 1141 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 14, -0.32 (-0.45 / -0.08) | 102 / 21 of 162 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 32, -0.74 (-0.38 / -1.15) | 86 / 33 of 173 | 0 | waiting for the first daily research run (Layers B/C) |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 27, -0.43 (-0.16 / -0.56) | 86 / 185 of 301 | 0 | waiting for the first daily research run (Layers B/C) |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 106, -1.18 (-1.04 / -1.29) | 161 / 511 of 787 | 0 | waiting for the first daily research run (Layers B/C) |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 52, -0.60 (-0.47 / -0.86) | 172 / 61 of 291 | 0 | waiting for the first daily research run (Layers B/C) |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **16** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S5-SWEEP-MSS-FVG | 30m | - | - | - | - | - | waiting for research |
| S5-SWEEP-MSS-FVG | 15m | - | - | - | - | - | waiting for research |
| S6-OB-FVG | 15m | - | - | - | - | - | waiting for research |
| S7-SILVER-BULLET | 15m | - | - | - | - | - | waiting for research |
| S8-PDH-PDL-SWEEP | 1h | - | - | - | - | - | waiting for research |
| S8-PDH-PDL-SWEEP | 30m | - | - | - | - | - | waiting for research |


### 3c. Research layers (daily run)
The daily research run (Layers B/C, costs +50%, ±20% test) has not run yet. It runs once a day on GitHub (workflow **Research**) and can be started by hand from the Actions tab.

### 3d. Why trades lose (failure attribution)
Filled in by the daily research run.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*