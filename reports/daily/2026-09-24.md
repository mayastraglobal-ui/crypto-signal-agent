# Crypto Signal Report

**Updated:** 2026-09-25 07:16 Beijing time (2026-09-24 23:16 UTC) · data: Binance · 9 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 0.8 MB (GitHub) · large files of this run 0.8 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-09-24 23:16 UTC / 2026-09-25 07:16 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · ⚠ calendar not maintained - no event listed for the next 7 days (config.yaml -> events)
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked, never emailed). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.01% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| PROVE | **DEGRADED** | 1d: DEGRADED: volume 52x normal on candle 09-23 00:00 UTC (possible bad data) |
- 67 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **ZEC**, **XRP**, **SOL**, **BNB**, **UNI**
- **Research only** - backtested, never a signal: SUI, AVAX

| Not eligible | 24h volume | Why |
|---|---|---|
| PROVE | $172M | 7-day average volume $36M < $50M; order book too thin: $53k within 1% (need $250k) |
| LTC | $151M | 7-day average volume $34M < $50M |
| ONDO | $118M | 7-day average volume $30M < $50M; 24h move +25.7% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $214k within 1% (need $250k) |

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
| XRP | 438 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| SOL | 319 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| BNB | 463 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| UNI | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| SUI | 177 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2023-05 | OK (300 candles) |
| AVAX | 313 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (HH/LL) | 84,942.4 / 82,874.9 | 0.78 | 0.62x | 1.01x | bull_reject, bear_reject |
| ETH | mixed (HH/LL) | 2,706 / 2,600.15 | 0.78 | 0.75x | 1.03x | bull_reject, bear_reject |
| ZEC | mixed (HH/LL) | 1,574.6 / 1,456.92 | 0.93 | 0.46x | 1.04x | bull_engulf, bull_reject |
| XRP | mixed (HH/LL) | 1.5435 / 1.4517 | 0.32 | 0.81x | 0.94x | - |
| SOL | mixed (HH/LL) | 117.79 / 112.52 | 0.57 | 0.75x | 0.96x | bear_reject |
| BNB | mixed (HH/LL) | 786.29 / 763.04 | 0.37 | 0.48x | 0.86x | bull_reject |
| UNI | down (LH/LL) | 9.401 / 8.787 | 0.63 | 0.50x | 0.83x | - |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 411 | 46% | 33% | 26% | 81% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | displacement_down | 346 | 49% | 32% | 22% | 75% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1100 | 44% | 30% | 21% | 78% | 43% | 29% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1238 | 44% | 30% | 21% | 76% | 48% | 33% | worse than chance | 0.08R |
| 4h | bull_reject | 851 | 41% | 28% | 19% | 79% | 42% | 29% | can't tell from chance | 0.13R |
| 4h | bear_reject | 800 | 48% | 33% | 24% | 73% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 599 | 43% | 29% | 21% | 76% | 42% | 29% | can't tell from chance | 0.13R |
| 4h | smc_sweep_bear | 595 | 46% | 30% | 20% | 79% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 238 | 44% | 29% | 21% | 81% | 44% | 30% | can't tell from chance | 0.14R |
| 4h | smc_bos_down | 238 | 50% | 37% | 26% | 69% | 50% | 33% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 79 | 49% | 32% | 25% | 84% | 42% | 28% | can't tell from chance | 0.14R |
| 4h | smc_choch_down | 73 | 42% | 25% | 14% | 78% | 51% | 35% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 584 | 42% | 27% | 20% | 79% | 42% | 29% | can't tell from chance | 0.13R |
| 4h | smc_fvg_retrace_bear | 606 | 47% | 31% | 20% | 76% | 48% | 33% | can't tell from chance | 0.08R |
| 1h | displacement_up | 560 | 46% | 34% | 27% | 73% | 42% | 28% | beats chance | 0.29R |
| 1h | displacement_down | 396 | 38% | 24% | 15% | 82% | 38% | 25% | can't tell from chance | 0.19R |
| 1h | bull_engulf | 1550 | 40% | 28% | 22% | 76% | 42% | 29% | can't tell from chance | 0.33R |
| 1h | bear_engulf | 1716 | 39% | 26% | 18% | 79% | 38% | 25% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1284 | 40% | 28% | 22% | 75% | 42% | 29% | can't tell from chance | 0.32R |
| 1h | bear_reject | 1188 | 35% | 23% | 18% | 82% | 38% | 25% | worse than chance | 0.19R |
| 1h | smc_sweep_bull | 563 | 41% | 27% | 20% | 77% | 41% | 29% | can't tell from chance | 0.31R |
| 1h | smc_sweep_bear | 641 | 36% | 24% | 16% | 80% | 38% | 25% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 361 | 44% | 31% | 24% | 79% | 42% | 29% | can't tell from chance | 0.28R |
| 1h | smc_bos_down | 252 | 38% | 27% | 18% | 83% | 38% | 25% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 110 | 48% | 37% | 30% | 71% | 44% | 32% | can't tell from chance | 0.33R |
| 1h | smc_choch_down | 110 | 45% | 30% | 17% | 75% | 39% | 28% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 811 | 44% | 32% | 24% | 72% | 42% | 29% | can't tell from chance | 0.31R |
| 1h | smc_fvg_retrace_bear | 739 | 40% | 27% | 18% | 80% | 37% | 25% | can't tell from chance | 0.20R |
| 30m | displacement_up | 552 | 41% | 31% | 26% | 76% | 40% | 29% | can't tell from chance | 0.35R |
| 30m | displacement_down | 369 | 40% | 25% | 14% | 82% | 37% | 22% | can't tell from chance | 0.22R |
| 30m | bull_engulf | 1583 | 39% | 28% | 21% | 76% | 40% | 28% | can't tell from chance | 0.38R |
| 30m | bear_engulf | 1621 | 36% | 22% | 16% | 81% | 36% | 21% | can't tell from chance | 0.24R |
| 30m | bull_reject | 1204 | 43% | 28% | 20% | 74% | 40% | 28% | can't tell from chance | 0.37R |
| 30m | bear_reject | 1282 | 38% | 24% | 16% | 80% | 36% | 21% | can't tell from chance | 0.23R |
| 30m | smc_sweep_bull | 545 | 39% | 27% | 17% | 77% | 40% | 28% | can't tell from chance | 0.39R |
| 30m | smc_sweep_bear | 576 | 40% | 26% | 18% | 82% | 36% | 21% | beats chance | 0.22R |
| 30m | smc_bos_up | 430 | 42% | 34% | 29% | 75% | 41% | 30% | can't tell from chance | 0.34R |
| 30m | smc_bos_down | 206 | 36% | 24% | 15% | 85% | 37% | 24% | can't tell from chance | 0.26R |
| 30m | smc_choch_up | 85 | 35% | 21% | 16% | 81% | 40% | 29% | can't tell from chance | 0.44R |
| 30m | smc_choch_down | 87 | 37% | 23% | 17% | 80% | 34% | 21% | can't tell from chance | 0.23R |
| 30m | smc_fvg_retrace_bull | 900 | 42% | 29% | 22% | 75% | 40% | 28% | can't tell from chance | 0.39R |
| 30m | smc_fvg_retrace_bear | 729 | 36% | 22% | 16% | 80% | 36% | 22% | can't tell from chance | 0.25R |
| 15m | displacement_up | 434 | 36% | 27% | 20% | 82% | 35% | 25% | can't tell from chance | 0.47R |
| 15m | displacement_down | 415 | 36% | 22% | 14% | 85% | 36% | 22% | can't tell from chance | 0.32R |
| 15m | bull_engulf | 1479 | 36% | 25% | 18% | 79% | 34% | 24% | can't tell from chance | 0.57R |
| 15m | bear_engulf | 1466 | 36% | 24% | 16% | 79% | 35% | 22% | can't tell from chance | 0.34R |
| 15m | bull_reject | 1195 | 35% | 24% | 17% | 79% | 34% | 24% | can't tell from chance | 0.58R |
| 15m | bear_reject | 1311 | 35% | 22% | 14% | 82% | 36% | 22% | can't tell from chance | 0.33R |
| 15m | smc_sweep_bull | 542 | 36% | 26% | 20% | 78% | 35% | 24% | can't tell from chance | 0.53R |
| 15m | smc_sweep_bear | 561 | 35% | 24% | 15% | 83% | 35% | 21% | can't tell from chance | 0.32R |
| 15m | smc_bos_up | 304 | 43% | 30% | 24% | 78% | 36% | 26% | beats chance | 0.47R |
| 15m | smc_bos_down | 316 | 35% | 21% | 15% | 85% | 35% | 22% | can't tell from chance | 0.36R |
| 15m | smc_choch_up | 82 | 30% | 20% | 11% | 87% | 35% | 25% | can't tell from chance | 0.56R |
| 15m | smc_choch_down | 87 | 36% | 21% | 14% | 83% | 36% | 21% | can't tell from chance | 0.32R |
| 15m | smc_fvg_retrace_bull | 960 | 32% | 23% | 16% | 80% | 34% | 24% | can't tell from chance | 0.53R |
| 15m | smc_fvg_retrace_bear | 878 | 34% | 24% | 17% | 80% | 35% | 21% | can't tell from chance | 0.34R |
| 5m | displacement_up | 1098 | 30% | 20% | 16% | 85% | 27% | 19% | beats chance | 0.87R |
| 5m | displacement_down | 1051 | 29% | 19% | 13% | 85% | 30% | 20% | can't tell from chance | 0.58R |
| 5m | bull_engulf | 3775 | 25% | 18% | 13% | 83% | 27% | 18% | can't tell from chance | 0.97R |
| 5m | bear_engulf | 3783 | 31% | 21% | 14% | 83% | 30% | 20% | can't tell from chance | 0.58R |
| 5m | bull_reject | 3125 | 26% | 17% | 12% | 82% | 27% | 18% | can't tell from chance | 0.97R |
| 5m | bear_reject | 3239 | 31% | 20% | 14% | 82% | 31% | 21% | can't tell from chance | 0.59R |
| 5m | smc_sweep_bull | 1117 | 29% | 21% | 15% | 79% | 28% | 19% | can't tell from chance | 0.85R |
| 5m | smc_sweep_bear | 1160 | 33% | 23% | 16% | 81% | 31% | 21% | can't tell from chance | 0.50R |
| 5m | smc_bos_up | 740 | 27% | 20% | 16% | 86% | 27% | 18% | can't tell from chance | 0.93R |
| 5m | smc_bos_down | 793 | 29% | 19% | 13% | 86% | 31% | 21% | can't tell from chance | 0.62R |
| 5m | smc_choch_up | 185 | 32% | 21% | 14% | 88% | 27% | 18% | can't tell from chance | 0.99R |
| 5m | smc_choch_down | 190 | 28% | 16% | 11% | 86% | 29% | 20% | can't tell from chance | 0.64R |
| 5m | smc_fvg_retrace_bull | 2944 | 28% | 19% | 13% | 81% | 26% | 18% | can't tell from chance | 0.99R |
| 5m | smc_fvg_retrace_bear | 2668 | 27% | 18% | 12% | 84% | 30% | 20% | worse than chance | 0.62R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (weak) | TRANSITION (strong) | TRANSITION (moderate) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H UNCLEAR)) |
| **ETH** | UNCLEAR (weak) | WEAK_BULL (weak) | TRANSITION (moderate) | RANGE (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H RANGE)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | RANGE (weak) | LONG allowed (1D/4H bullish, 1W WEAK_BULL) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | WEAK_BULL (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H WEAK_BULL, 1H UNCLEAR)) |
| **SOL** | TRANSITION (weak) | TRANSITION (strong) | TRANSITION (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H UNCLEAR)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | UNCLEAR (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H UNCLEAR)) |
| **UNI** | EXPANSION up (weak) | STRONG_BULL (moderate) | WEAK_BULL (weak) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W EXPANSION) |
| **SUI** | RANGE (weak) | EXPANSION up (weak) | TRANSITION (moderate) | TRANSITION (weak) | NO TRADE (timeframes disagree (1D EXPANSION, 4H TRANSITION, 1H TRANSITION)) |
| **AVAX** | TRANSITION (weak) | EXPANSION down (weak) | TRANSITION (moderate) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D EXPANSION, 4H TRANSITION, 1H UNCLEAR)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (weak)** - for: EMA-fast rising (+1.1 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.72x normal, Bollinger width above 52% of the last 100 candles · against: EMAs not lined up; ADX 27 is close to a threshold
- **1D TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.0 ATR in 10 candles); swing structure down (LH/LL); ADX 45 = strong trend; candle size 1.18x normal, Bollinger width above 78% of the last 100 candles · against: -
- **4H TRANSITION (moderate)** - for: close above EMA-fast above EMA-slow; swing structure down (LH/LL); ADX 32 = strong trend; candle size 1.28x normal, Bollinger width above 56% of the last 100 candles · against: EMA-fast flat (+0.9 ATR in 10 candles)
- **1H UNCLEAR (weak)** - for: candle size 1.01x normal, Bollinger width above 38% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.2 ATR in 10 candles); swing structure mixed; ADX 24 = in between (20-25); ADX 24 is close to a threshold; signals are mixed and trend strength is in between

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (BOS 3 candles ago) | buy-side (bearish idea) 43 candles ago | bull 84,193.62-84,269.99 | bear 86,133.40-86,975.51 | premium (68%) | swing high 84,942.45 (1.18 ATR) | swing low 82,874.93 (2.48 ATR) |
| **ETH** | down (BOS 3 candles ago) | buy-side (bearish idea) 26 candles ago | bull 2,675.72-2,679.23 (retraced) | bear 2,745.99-2,784.40 | premium (81%) | equal highs 2,706.00 (0.87 ATR) | swing low 2,600.15 (3.63 ATR) |
| **ZEC** | up (CHOCH 27 candles ago) | buy-side (bearish idea) 27 candles ago | bull 1,517.23-1,526.13 (retraced) | bull 1,098.88-1,133.82 | premium (76%) | swing high 1,574.60 (0.95 ATR) | swing low 1,456.92 (3.02 ATR) |
| **XRP** | up (BOS 27 candles ago) | buy-side (bearish idea) 5 candles ago | bull 1.5156-1.5195 (retraced) | bull 1.3773-1.3856 | premium (89%) | swing high 1.6581 (5.89 ATR) | swing low 1.4517 (3.83 ATR) |
| **SOL** | up (BOS 27 candles ago) | sell-side (bullish idea) 3 candles ago | bull 115.10-115.59 | bear 117.85-119.66 | premium (77%) | swing high 117.79 (1.01 ATR) | swing low 112.52 (3.47 ATR) |
| **BNB** | up (BOS 27 candles ago) | sell-side (bullish idea) 3 candles ago | bear 777.24-778.60 (retraced) | bear 787.07-797.61 | premium (58%) | swing high 786.29 (1.89 ATR) | equal lows 763.04 (2.63 ATR) |
| **UNI** | down (BOS 4 candles ago) | sell-side (bullish idea) 54 candles ago | bull 8.9510-9.0010 (retraced) | bull 8.6780-9.0640 | premium (59%) | swing high 9.4010 (1.39 ATR) | swing low 8.7870 (2.02 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 71 (Greed), yesterday 71  (extreme fear/greed = bigger, faster moves)

## 2. Signals right now
Only **APPROVED** strategy versions (your yes, after paper trading) give signals and emails.

**No trade passes all the checks right now. That is normal - no trade is also a position.**

### 2c. Watching - no signal yet (report only, never emailed)
WATCH = the strategy's trend / regime filters are open; SETUP_FORMING = all entry rules but one are true.

| Coin | TF | Strategy | Stage | Side | State | Rules true | Still missing |
|---|---|---|---|---|---|---|---|
| UNI | 4h | donchian_breakout v1.0 | VALIDATION | LONG | WATCH | 2/4 | - |
| ZEC | 4h | donchian_breakout v1.0 | VALIDATION | LONG | WATCH | 2/4 | - |

### 2d. Risk engine (section 15 - independent of the strategies)
- **Live results:** today +0.00R (limit -3R), this week +0.00R (limit -6R) · **halts:** none
- **Suspended strategies** (live drawdown > 8R): none
- **Risk per trade:** 0.5% · leverage never above 3x (the position is made smaller instead)
- **Heat:** max 3 positions, 1 per coin, 1 per group of correlated coins and direction (1h correlation ≥ 0.7) · groups now: BNB+BTC+ETH+SOL+XRP
- **Every live entry also needs:** reward to TP1 ≥ 2R, no opposing level before TP1, no high-impact event within ±60 min, no duplicate
- **Event calendar (next 7 days):** none listed
- ⚠️ **calendar not maintained - no event listed for the next 7 days (config.yaml -> events)**

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (not run yet); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged, never emailed.
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian_breakout | 1.0 | 4h | **VALIDATION** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 14, +0.29 (+0.79 / -0.38) | 81 / 47 of 232 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout | 1.0 | 1h | **VALIDATION** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 29, +0.46 (+0.41 / +0.50) | 114 / 84 of 361 | 0 | waiting for the first daily research run (Layers B/C) |
| trend_pullback | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 72, +0.15 (+0.24 / +0.06) | 756 / 230 of 1535 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 4h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 2, +0.08 (-1.11 / +1.27) | 95 / 21 of 130 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 4, -0.44 (-1.18 / +0.29) | 122 / 38 of 188 | 0 | waiting for the first daily research run (Layers B/C) |
| macd_trend_cross | 1.0 | 4h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 152 / 5 of 161 | 0 | waiting for the first daily research run (Layers B/C) |
| macd_trend_cross | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 1, -0.02 (+0.00 / -0.02) | 183 / 4 of 189 | 0 | waiting for the first daily research run (Layers B/C) |
| macd_trend_cross | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 4, +0.18 (+0.85 / -0.50) | 154 / 10 of 179 | 0 | waiting for the first daily research run (Layers B/C) |
| supertrend_flip | 1.0 | 4h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 1, +1.82 (+1.82 / +0.00) | 38 / 7 of 47 | 0 | waiting for the first daily research run (Layers B/C) |
| supertrend_flip | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 5, +0.39 (+0.00 / +0.39) | 55 / 2 of 65 | 0 | waiting for the first daily research run (Layers B/C) |
| supertrend_flip | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 7, -0.37 (-0.69 / -0.14) | 50 / 5 of 65 | 0 | waiting for the first daily research run (Layers B/C) |
| liquidity_sweep_reversal | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 6, -0.53 (-1.11 / -0.41) | 94 / 188 of 290 | 0 | waiting for the first daily research run (Layers B/C) |
| liquidity_sweep_reversal | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 12, -0.64 (-0.19 / -0.80) | 100 / 185 of 306 | 0 | waiting for the first daily research run (Layers B/C) |
| ema_9_21_cross | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 3, -1.00 (+0.00 / -1.00) | 136 / 7 of 150 | 0 | waiting for the first daily research run (Layers B/C) |
| ema_9_21_cross | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 10, +0.21 (+0.29 / +0.17) | 99 / 15 of 128 | 0 | waiting for the first daily research run (Layers B/C) |
| ema_9_21_cross | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 17, +0.28 (+0.36 / +0.10) | 58 / 13 of 95 | 0 | waiting for the first daily research run (Layers B/C) |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 55 / 10 of 68 | 0 | waiting for the first daily research run (Layers B/C) |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 1, -1.32 (+0.00 / -1.32) | 36 / 13 of 55 | 0 | waiting for the first daily research run (Layers B/C) |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 484 / 205 of 869 | 0 | waiting for the first daily research run (Layers B/C) |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 2, +0.05 (+0.05 / +0.00) | 435 / 198 of 761 | 0 | waiting for the first daily research run (Layers B/C) |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 4 / 5 of 9 | 0 | waiting for the first daily research run (Layers B/C) |
| S6-OB-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 5, -0.10 (+1.40 / -0.48) | 104 / 31 of 149 | 0 | waiting for the first daily research run (Layers B/C) |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 25 / 12 of 38 | 0 | waiting for the first daily research run (Layers B/C) |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 2, +0.31 (+1.94 / -1.32) | 49 / 24 of 80 | 0 | waiting for the first daily research run (Layers B/C) |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 83 / 200 of 291 | 0 | waiting for the first daily research run (Layers B/C) |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 2, -1.25 (-1.25 / +0.00) | 29 / 97 of 134 | 0 | waiting for the first daily research run (Layers B/C) |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 10, -0.18 (-1.18 / +0.07) | 434 / 1026 of 1538 | 0 | waiting for the first daily research run (Layers B/C) |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **BACKTESTING** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 18, +0.08 (-1.35 / +0.48) | 397 / 921 of 1475 | 0 | waiting for the first daily research run (Layers B/C) |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 55 / 10 of 68 | 0 | waiting for the first daily research run (Layers B/C) |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 36 / 13 of 55 | 0 | waiting for the first daily research run (Layers B/C) |
| S6-OB-FVG-5M | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 4 / 5 of 9 | 0 | waiting for the first daily research run (Layers B/C) |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 25 / 12 of 38 | 0 | waiting for the first daily research run (Layers B/C) |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 29 / 97 of 134 | 0 | waiting for the first daily research run (Layers B/C) |
| trend_pullback | 1.0 | 4h | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 6, +1.14 (+1.35 / +0.94) | 577 / 183 of 913 | 0 | waiting for the first daily research run (Layers B/C) |
| trend_pullback | 1.0 | 1h | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 40, -0.04 (-0.35 / +0.28) | 1079 / 280 of 1676 | 0 | waiting for the first daily research run (Layers B/C) |
| trend_pullback | 1.0 | 15m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 145, -0.01 (-0.15 / +0.18) | 1208 / 282 of 2040 | 0 | waiting for the first daily research run (Layers B/C) |
| donchian_breakout | 1.0 | 30m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 43, +0.09 (-0.06 / +0.25) | 132 / 55 of 415 | 0 | waiting for the first daily research run (Layers B/C) |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 13, -0.24 (-0.24 / +0.00) | 671 / 3 of 916 | 0 | waiting for the first daily research run (Layers B/C) |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 26, -0.30 (-0.37 / -0.20) | 945 / 4 of 1249 | 0 | waiting for the first daily research run (Layers B/C) |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 29, -0.11 (-0.15 / -0.03) | 928 / 20 of 1107 | 0 | waiting for the first daily research run (Layers B/C) |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 49, -0.29 (-0.31 / -0.17) | 1107 / 35 of 1280 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 16, -0.42 (-0.45 / -0.38) | 108 / 24 of 173 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 35, -0.63 (-0.38 / -0.87) | 101 / 39 of 200 | 0 | waiting for the first daily research run (Layers B/C) |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 29, -0.48 (-0.52 / -0.46) | 96 / 204 of 332 | 0 | waiting for the first daily research run (Layers B/C) |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 111, -1.18 (-1.10 / -1.24) | 189 / 555 of 864 | 0 | waiting for the first daily research run (Layers B/C) |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | 60, -0.49 (-0.40 / -0.68) | 206 / 65 of 337 | 0 | waiting for the first daily research run (Layers B/C) |

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
| S5-SWEEP-MSS-FVG-5M | 30m | - | - | - | - | - | waiting for research |
| S5-SWEEP-MSS-FVG-5M | 15m | - | - | - | - | - | waiting for research |
| S6-OB-FVG-5M | 15m | - | - | - | - | - | waiting for research |
| S7-SILVER-BULLET-5M | 15m | - | - | - | - | - | waiting for research |
| S8-PDH-PDL-SWEEP-5M | 30m | - | - | - | - | - | waiting for research |


### 3c. Research layers (daily run)
The daily research run (Layers B/C, costs +50%, ±20% test) has not run yet. It runs once a day on GitHub (workflow **Research**) and can be started by hand from the Actions tab.

### 3d. Why trades lose (failure attribution)
Filled in by the daily research run.

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 3.2 KB | - | - |
| `memory/changelog.md` | 41.3 KB | - | - |
| `memory/coin_notes.md` | 0.6 KB | - | - |
| `memory/execution_notes.md` | 1.4 KB | 2 | 2026-09-24 23:16 UTC |
| `memory/experiments.md` | 3.5 KB | - | - |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 0.8 KB | - | - |
| `memory/market_regime_log.md` | 1.3 KB | - | - |
| `memory/missed_trades.md` | 0.6 KB | - | - |
| `memory/research_sources.md` | 0.7 KB | - | - |
| `memory/smc_events.csv` | 2.1 KB | - | - |
| `memory/smc_research.md` | 5.7 KB | - | - |
| `memory/strategy_lifecycle.md` | 7.5 KB | - | - |
| `memory/strategy_registry.csv` | 15.4 KB | - | - |
| `memory/universe_log.md` | 1.5 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*