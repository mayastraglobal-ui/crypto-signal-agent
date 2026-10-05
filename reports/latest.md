# Crypto Signal Report

**Updated:** 2026-10-06 07:17 Beijing time (2026-10-05 23:17 UTC) · data: Binance · 8 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 8.4 MB (GitHub) · large files of this run 4.4 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-05 23:17 UTC / 2026-10-06 07:17 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5%
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.04% (limit 0.5%)
- All 8 coins passed every check on every timeframe.
- 56 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-05 23:16 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 969 h since 2026-08-26 | +0.0027% | 1.21 | 0.82 | - |
| ETH | GOOD | okx | 969 h since 2026-08-26 | +0.0042% | 1.42 | 0.94 | - |
| SOL | GOOD | okx | 969 h since 2026-08-26 | -0.0005% | 1.73 | 0.75 | - |
| ZEC | GOOD | okx | 969 h since 2026-08-26 | +0.0100% | 0.90 | - | - |
| XRP | GOOD | okx | 969 h since 2026-08-26 | +0.0100% | 2.95 | 0.90 | - |
| BNB | GOOD | okx | 969 h since 2026-08-26 | +0.0100% | 2.32 | 1.21 | - |
| SUI | GOOD | okx | 969 h since 2026-08-26 | -0.0089% | 2.67 | 0.60 | - |
| ENA | GOOD | okx | 969 h since 2026-08-26 | +0.0050% | 2.54 | 1.25 | - |

*Binance futures API: blocked from GitHub's servers (HTTP 451) - expected, not a problem. The main series (OKX) is complete; Binance research history comes from the data.binance.vision files.*

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **ZEC**, **XRP**, **BNB**, **SUI**
- **Research only** - backtested, never a signal: ENA

| Not eligible | 24h volume | Why |
|---|---|---|
| ADA | $90M | 7-day average volume $43M < $50M |

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
| ENA | 131 | 916 | 910 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (HH/LL) | 86,725.1 / 84,972 | 0.45 | 0.69x | 1.03x | - |
| ETH | down (LH/LL) | 2,730.28 / 2,679.63 | 0.15 | 0.27x | 1.03x | bull_engulf |
| SOL | down (LH/LL) | 121.3 / 118.93 | 0.28 | 1.03x | 0.96x | bear_reject |
| ZEC | mixed (HH/LL) | 1,366.04 / 1,278 | 0.04 | 0.64x | 1.07x | - |
| XRP | down (LH/LL) | 1.5266 / 1.486 | 0.37 | 0.68x | 0.98x | - |
| BNB | down (LH/LL) | 793.62 / 784.7 | 0.48 | 0.40x | 0.92x | bull_engulf, bear_engulf |
| SUI | mixed (HH/LL) | 1.2545 / 1.176 | 0.13 | 0.38x | 0.96x | - |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 388 | 48% | 34% | 26% | 80% | 44% | 30% | can't tell from chance | 0.08R |
| 4h | displacement_down | 287 | 46% | 30% | 19% | 78% | 45% | 29% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 977 | 45% | 32% | 23% | 77% | 45% | 31% | can't tell from chance | 0.09R |
| 4h | bear_engulf | 1103 | 43% | 27% | 17% | 79% | 47% | 31% | worse than chance | 0.08R |
| 4h | bull_reject | 735 | 42% | 29% | 21% | 78% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | bear_reject | 723 | 46% | 31% | 21% | 75% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bull | 519 | 45% | 30% | 23% | 77% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | smc_sweep_bear | 550 | 42% | 27% | 18% | 80% | 44% | 29% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 235 | 45% | 29% | 21% | 82% | 46% | 33% | can't tell from chance | 0.08R |
| 4h | smc_bos_down | 189 | 51% | 36% | 23% | 70% | 49% | 33% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 75 | 52% | 35% | 28% | 81% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | smc_choch_down | 70 | 40% | 26% | 14% | 76% | 44% | 28% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 536 | 46% | 29% | 24% | 76% | 45% | 31% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bear | 543 | 47% | 31% | 20% | 76% | 47% | 31% | can't tell from chance | 0.08R |
| 1h | displacement_up | 487 | 46% | 32% | 26% | 75% | 45% | 31% | can't tell from chance | 0.18R |
| 1h | displacement_down | 345 | 37% | 24% | 14% | 81% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | bull_engulf | 1389 | 42% | 30% | 22% | 75% | 44% | 30% | can't tell from chance | 0.20R |
| 1h | bear_engulf | 1518 | 38% | 24% | 17% | 79% | 37% | 24% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1112 | 42% | 30% | 23% | 75% | 44% | 30% | can't tell from chance | 0.20R |
| 1h | bear_reject | 1137 | 36% | 24% | 18% | 81% | 38% | 25% | can't tell from chance | 0.18R |
| 1h | smc_sweep_bull | 512 | 41% | 25% | 19% | 78% | 43% | 30% | can't tell from chance | 0.19R |
| 1h | smc_sweep_bear | 550 | 38% | 24% | 15% | 81% | 38% | 24% | can't tell from chance | 0.19R |
| 1h | smc_bos_up | 325 | 46% | 34% | 28% | 76% | 46% | 31% | can't tell from chance | 0.16R |
| 1h | smc_bos_down | 218 | 42% | 31% | 22% | 80% | 39% | 26% | can't tell from chance | 0.22R |
| 1h | smc_choch_up | 83 | 47% | 33% | 29% | 76% | 41% | 28% | can't tell from chance | 0.21R |
| 1h | smc_choch_down | 84 | 43% | 31% | 18% | 71% | 37% | 23% | can't tell from chance | 0.18R |
| 1h | smc_fvg_retrace_bull | 705 | 45% | 31% | 24% | 73% | 44% | 31% | can't tell from chance | 0.19R |
| 1h | smc_fvg_retrace_bear | 642 | 38% | 27% | 19% | 78% | 37% | 24% | can't tell from chance | 0.21R |
| 30m | displacement_up | 427 | 38% | 27% | 21% | 81% | 44% | 29% | worse than chance | 0.22R |
| 30m | displacement_down | 329 | 43% | 29% | 18% | 79% | 36% | 22% | beats chance | 0.22R |
| 30m | bull_engulf | 1353 | 42% | 27% | 18% | 77% | 43% | 28% | can't tell from chance | 0.24R |
| 30m | bear_engulf | 1459 | 38% | 22% | 15% | 81% | 35% | 21% | can't tell from chance | 0.24R |
| 30m | bull_reject | 1037 | 46% | 30% | 22% | 73% | 43% | 29% | can't tell from chance | 0.24R |
| 30m | bear_reject | 1206 | 36% | 20% | 14% | 81% | 36% | 22% | can't tell from chance | 0.23R |
| 30m | smc_sweep_bull | 540 | 43% | 28% | 18% | 75% | 43% | 29% | can't tell from chance | 0.22R |
| 30m | smc_sweep_bear | 515 | 40% | 26% | 17% | 82% | 36% | 22% | can't tell from chance | 0.22R |
| 30m | smc_bos_up | 313 | 37% | 29% | 24% | 79% | 43% | 28% | worse than chance | 0.24R |
| 30m | smc_bos_down | 216 | 35% | 22% | 12% | 84% | 36% | 21% | can't tell from chance | 0.22R |
| 30m | smc_choch_up | 89 | 36% | 21% | 16% | 88% | 42% | 27% | can't tell from chance | 0.23R |
| 30m | smc_choch_down | 84 | 39% | 26% | 23% | 76% | 35% | 20% | can't tell from chance | 0.21R |
| 30m | smc_fvg_retrace_bull | 765 | 41% | 26% | 18% | 79% | 42% | 28% | can't tell from chance | 0.24R |
| 30m | smc_fvg_retrace_bear | 652 | 39% | 21% | 14% | 81% | 36% | 21% | can't tell from chance | 0.25R |
| 15m | displacement_up | 415 | 37% | 26% | 19% | 84% | 40% | 28% | can't tell from chance | 0.30R |
| 15m | displacement_down | 316 | 31% | 20% | 12% | 84% | 33% | 19% | can't tell from chance | 0.31R |
| 15m | bull_engulf | 1393 | 39% | 28% | 20% | 78% | 39% | 28% | can't tell from chance | 0.33R |
| 15m | bear_engulf | 1328 | 31% | 18% | 11% | 83% | 33% | 19% | can't tell from chance | 0.33R |
| 15m | bull_reject | 1025 | 40% | 30% | 21% | 76% | 38% | 28% | can't tell from chance | 0.33R |
| 15m | bear_reject | 1219 | 34% | 21% | 13% | 83% | 34% | 19% | can't tell from chance | 0.31R |
| 15m | smc_sweep_bull | 469 | 39% | 28% | 21% | 78% | 39% | 28% | can't tell from chance | 0.29R |
| 15m | smc_sweep_bear | 481 | 34% | 21% | 11% | 85% | 34% | 19% | can't tell from chance | 0.30R |
| 15m | smc_bos_up | 332 | 37% | 26% | 20% | 81% | 40% | 30% | can't tell from chance | 0.31R |
| 15m | smc_bos_down | 228 | 25% | 14% | 10% | 89% | 32% | 18% | worse than chance | 0.35R |
| 15m | smc_choch_up | 67 | 31% | 19% | 12% | 87% | 42% | 30% | can't tell from chance | 0.35R |
| 15m | smc_choch_down | 66 | 32% | 20% | 11% | 83% | 32% | 18% | can't tell from chance | 0.34R |
| 15m | smc_fvg_retrace_bull | 880 | 39% | 28% | 20% | 76% | 39% | 28% | can't tell from chance | 0.33R |
| 15m | smc_fvg_retrace_bear | 707 | 32% | 21% | 13% | 83% | 33% | 19% | can't tell from chance | 0.34R |
| 5m | displacement_up | 999 | 31% | 21% | 15% | 87% | 31% | 21% | can't tell from chance | 0.56R |
| 5m | displacement_down | 900 | 24% | 16% | 11% | 86% | 28% | 18% | worse than chance | 0.53R |
| 5m | bull_engulf | 3471 | 29% | 20% | 15% | 83% | 30% | 21% | can't tell from chance | 0.58R |
| 5m | bear_engulf | 3360 | 27% | 18% | 12% | 83% | 27% | 18% | can't tell from chance | 0.61R |
| 5m | bull_reject | 2668 | 29% | 21% | 15% | 81% | 30% | 20% | can't tell from chance | 0.63R |
| 5m | bear_reject | 3026 | 29% | 19% | 12% | 83% | 28% | 19% | can't tell from chance | 0.57R |
| 5m | smc_sweep_bull | 956 | 34% | 23% | 17% | 78% | 32% | 22% | can't tell from chance | 0.48R |
| 5m | smc_sweep_bear | 1008 | 31% | 22% | 14% | 83% | 29% | 19% | can't tell from chance | 0.52R |
| 5m | smc_bos_up | 706 | 29% | 21% | 16% | 86% | 31% | 21% | can't tell from chance | 0.60R |
| 5m | smc_bos_down | 643 | 23% | 15% | 11% | 87% | 28% | 18% | worse than chance | 0.60R |
| 5m | smc_choch_up | 178 | 34% | 25% | 18% | 85% | 30% | 21% | can't tell from chance | 0.65R |
| 5m | smc_choch_down | 180 | 20% | 12% | 7% | 89% | 28% | 19% | worse than chance | 0.52R |
| 5m | smc_fvg_retrace_bull | 2824 | 30% | 21% | 14% | 83% | 29% | 20% | can't tell from chance | 0.65R |
| 5m | smc_fvg_retrace_bear | 2435 | 25% | 17% | 11% | 84% | 27% | 18% | can't tell from chance | 0.65R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (strong) | STRONG_BULL (strong) | TRANSITION (weak) | RANGE (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H TRANSITION, 1H RANGE)) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (strong) | RANGE (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H RANGE)) |
| **SOL** | WEAK_BULL (moderate) | STRONG_BULL (strong) | UNCLEAR (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H UNCLEAR, 1H RANGE)) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (weak) | COMPRESSION (strong) | RANGE (strong) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H COMPRESSION, 1H RANGE)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | COMPRESSION (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H COMPRESSION, 1H RANGE)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (strong) | TRANSITION (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H TRANSITION, 1H RANGE)) |
| **SUI** | UNCLEAR (weak) | WEAK_BULL (weak) | WEAK_BULL (moderate) | UNCLEAR (weak) | LONG allowed (1D/4H bullish, 1W UNCLEAR) |
| **ENA** | WEAK_BULL (moderate) | WEAK_BULL (weak) | UNCLEAR (weak) | WEAK_BULL (weak) | LONG allowed (1D/1H bullish, 1W WEAK_BULL) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.8 ATR in 10 candles); swing structure down (LH/LL); ADX 28 = strong trend; candle size 0.71x normal, Bollinger width above 62% of the last 100 candles · against: -
- **1D STRONG_BULL (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.3 ATR in 10 candles); swing structure up (HH/HL); ADX 42 = strong trend; candle size 1.00x normal, Bollinger width above 72% of the last 100 candles; volume 0.94x normal · against: -
- **4H TRANSITION (weak)** - for: close above EMA-fast above EMA-slow; ADX 27 = strong trend; candle size 0.90x normal, Bollinger width above 32% of the last 100 candles · against: EMA-fast flat (+0.7 ATR in 10 candles); swing structure mixed; ADX 27 is close to a threshold
- **1H RANGE (moderate)** - for: EMA-fast flat (+0.1 ATR in 10 candles); swing structure mixed; ADX 18 = weak trend / ranging; candle size 1.03x normal, Bollinger width above 36% of the last 100 candles · against: close above EMA-fast above EMA-slow

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **none**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (BOS 30 candles ago) | buy-side (bearish idea) 11 candles ago | bear 85,769.53-86,262.92 (retraced) | bear 86,133.40-86,975.51 | premium (55%) | swing high 86,725.12 (2.14 ATR) | swing low 84,972.01 (2.56 ATR) |
| **ETH** | down (BOS 27 candles ago) | buy-side (bearish idea) 6 candles ago | bull 2,709.95-2,711.71 (retraced) | bull 2,652.20-2,695.38 | premium (72%) | swing high 2,730.28 (1.13 ATR) | equal lows 2,677.41 (3.06 ATR) |
| **SOL** | down (CHOCH 34 candles ago) | buy-side (bearish idea) 15 candles ago | bear 121.20-121.38 (retraced) | bull 115.86-117.34 | premium (88%) | swing high 122.08 (1.62 ATR) | swing low 118.93 (3.14 ATR) |
| **ZEC** | down (CHOCH 33 candles ago) | sell-side (bullish idea) 27 candles ago | bear 1,345.25-1,347.66 | bear 1,397.89-1,447.60 | premium (69%) | swing high 1,366.04 (1.44 ATR) | swing low 1,278.00 (3.26 ATR) |
| **XRP** | down (CHOCH 34 candles ago) | sell-side (bullish idea) 26 candles ago | bull 1.5068-1.5080 (retraced) | bull 1.3773-1.3856 | premium (61%) | swing high 1.5266 (1.73 ATR) | swing low 1.4860 (2.66 ATR) |
| **BNB** | up (CHOCH 3 candles ago) | buy-side (bearish idea) 4 candles ago | bull 787.08-788.22 (retraced) | bull 765.01-768.61 | discount (38%) | swing high 793.62 (1.68 ATR) | swing low 784.70 (1.01 ATR) |
| **SUI** | up (BOS 15 candles ago) | buy-side (bearish idea) 51 candles ago | bull 1.2045-1.2113 | bull 1.1707-1.1875 | premium (54%) | swing high 1.2528 (1.98 ATR) | swing low 1.1760 (2.41 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 70 (Greed), yesterday 65  (extreme fear/greed = bigger, faster moves)

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
**Status and long-history numbers** come from the daily research run (last run 2026-10-05 00:57 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 814 | 41.2 | +0.247 | 1.46 | 20.0R | +0.25 / +0.24 | +0.27 / +0.21 | 5/5 | +0.21 | +0.19 | stable | 7 | 0.05R | 7, -0.21 (-0.07 / -1.07) | 75 / 37 of 210 | 0 | max drawdown 20.0R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 926 | 40.4 | +0.235 | 1.43 | 19.0R | +0.25 / +0.21 | +0.24 / +0.23 | 5/5 | +0.20 | +0.17 | stable | 7 | 0.05R | 8, -0.31 (-0.20 / -1.07) | 127 / 49 of 284 | 0 | max drawdown 19.0R |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 837 | 55.7 | +0.151 | 1.35 | 16.6R | +0.15 / +0.15 | +0.15 / +0.15 | 5/5 | +0.11 | +0.09 | stable | 6 | 0.05R | 8, -0.08 (+0.07 / -1.07) | 75 / 37 of 210 | 0 | max drawdown 16.6R |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.54 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.97 (+1.97 / +0.00) | 34 / 83 of 124 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 6 | 33.3 | +0.010 | 1.02 | 2.2R | +0.25 / -0.47 | +0.00 / +0.01 | 0/5 ✗ | -0.04 | -0.08 | stable | 0 | 0.10R | 0, +0.00 (+0.00 / +0.00) | 409 / 152 of 673 | 0 | only 6 trades; avg +0.01R/trade (needs +0.10R); profit factor 1.02; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 6 / 2 of 8 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 54 / 16 of 72 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 29 / 7 of 43 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 6 / 2 of 8 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 9 / 3 of 14 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **BACKTESTING** | 29 | 51.7 | -0.032 | 0.94 | 4.6R | +0.12 / -0.43 | +0.28 / -0.37 | 1/5 ✗ | -0.07 | -0.10 | ✗  time_stop_bars 40→32: -0.06R | 2 | 0.07R | 1, +0.31 (+0.31 / +0.00) | 129 / 3 of 133 | 0 | only 29 trades; avg -0.03R/trade (needs +0.10R); profit factor 0.94; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 9 | 33.3 | -0.355 | 0.63 | 7.4R | -0.76 / +0.15 | -0.22 / -0.52 | 0/5 ✗ | -0.90 | -1.13 | ✗  sweep_bars 8→10: -0.64R | 0 | 0.74R | 1, -1.20 (-1.20 / +0.00) | 33 / 9 of 51 | 0 | not cost-viable: fees + slippage 0.74R per trade (stop must be ≥ 4x the round-trip cost); only 9 trades; avg -0.36R/trade (needs +0.10R); profit factor 0.63; only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 10 | 40.0 | -0.471 | 0.28 | 6.0R | -0.60 / +0.05 | -0.31 / -0.58 | 0/5 ✗ | -0.46 | -0.83 | ✗  stop max_width_atr 3.0→3.6: -0.57R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 383 / 144 of 662 | 0 | only 10 trades; avg -0.47R/trade (needs +0.10R); profit factor 0.28; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 4 | 25.0 | -0.845 | 0.41 | 3.4R | -0.69 / -1.32 | -1.32 / -0.69 | 0/5 ✗ | -0.99 | -1.11 | ✗  stop buffer_atr 0.2→0.16: -1.14R | 0 | 0.33R | 1, -1.20 (-1.20 / +0.00) | 29 / 7 of 43 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); only 4 trades; avg -0.85R/trade (needs +0.10R); profit factor 0.41; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 2 | 0.0 | -1.134 | 0.0 | 2.3R | -1.13 / +0.00 | +0.00 / -1.13 | 0/5 ✗ | -1.20 | -1.26 | ✗  sweep_bars 8→10: -1.18R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 9 / 3 of 14 | 0 | only 2 trades; avg -1.13R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 3 | 0.0 | -1.236 | 0.0 | 3.7R | -1.24 / +0.00 | -1.42 / -1.15 | 0/5 ✗ | -1.22 | -1.28 | ✗  stop buffer_atr 0.2→0.16: -1.25R | 0 | 0.19R | 0, +0.00 (+0.00 / +0.00) | 54 / 16 of 72 | 0 | only 3 trades; avg -1.24R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 215 | 52.1 | +0.021 | 1.04 | 27.9R | +0.21 / -0.38 | +0.13 / -0.08 | 2/5 ✗ | -0.03 | -0.08 | ✗  stop atr 1.5→1.8: -0.01R | 4 | 0.07R | 1, -1.04 (-1.04 / +0.00) | 90 / 20 of 122 | 0 | avg +0.02R/trade (needs +0.10R); profit factor 1.04; max drawdown 27.9R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 640 | 52.3 | -0.030 | 0.94 | 42.5R | -0.04 / -0.02 | -0.09 / +0.04 | 1/5 ✗ | -0.12 | -0.21 | ✗  bb_k 2→1: -0.08R | 3 | 0.15R | 8, +0.06 (+0.37 / -0.47) | 117 / 31 of 183 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.94; max drawdown 42.5R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 139 | 50.4 | -0.037 | 0.93 | 27.7R | -0.19 / +0.30 | -0.07 / +0.00 | 2/5 ✗ | -0.10 | -0.17 | ✗  stop atr 1.5→1.2: -0.11R | 3 | 0.14R | 0, +0.00 (+0.00 / +0.00) | 186 / 5 of 193 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.93; max drawdown 27.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2236 | 32.5 | -0.043 | 0.93 | 152.0R | -0.06 / -0.00 | -0.03 / -0.06 | 2/5 ✗ | -0.10 | -0.15 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.09R | 19, +0.09 (+0.21 / -0.24) | 103 / 61 of 324 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.93; max drawdown 152.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 2549 | 32.5 | -0.043 | 0.93 | 175.6R | -0.06 / -0.01 | -0.02 / -0.07 | 1/5 ✗ | -0.10 | -0.16 | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.10R | 24, -0.01 (+0.28 / -0.60) | 173 / 88 of 457 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.93; max drawdown 175.6R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 909 | 34.1 | -0.058 | 0.91 | 83.7R | -0.07 / -0.02 | -0.02 / -0.11 | 2/5 ✗ | -0.14 | -0.22 | ✗  stop atr 2.0→1.6: -0.13R | 2 | 0.14R | 37, -0.03 (+0.06 / -0.22) | 115 / 29 of 285 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 83.7R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2297 | 48.1 | -0.061 | 0.88 | 159.1R | -0.06 / -0.06 | -0.07 / -0.06 | 0/5 ✗ | -0.11 | -0.17 | ✗  stop atr 2.0→1.6: -0.08R | 1 | 0.09R | 19, +0.22 (+0.28 / +0.05) | 103 / 61 of 324 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.88; max drawdown 159.1R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 69 | 46.4 | -0.065 | 0.88 | 11.0R | +0.07 / -0.26 | -0.12 / +0.00 | 4/5 ✗ | -0.10 | -0.13 | ✗  time_stop_bars 60→48: -0.06R | 1 | 0.05R | 0, +0.00 (+0.00 / +0.00) | 30 / 5 of 38 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.88; max drawdown 11.0R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 931 | 48.1 | -0.081 | 0.85 | 109.3R | -0.03 / -0.19 | -0.03 / -0.15 | 1/5 ✗ | -0.13 | -0.16 | ✗  long_rsi_hi 65→52: -0.16R | 1 | 0.07R | 10, -0.42 (-0.60 / -0.15) | 549 / 158 of 847 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.85; max drawdown 109.3R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1073 | 33.2 | -0.090 | 0.87 | 116.2R | -0.11 / -0.04 | -0.06 / -0.13 | 1/5 ✗ | -0.18 | -0.27 | ✗  stop atr 2.0→1.6: -0.16R | 1 | 0.15R | 44, -0.01 (+0.09 / -0.24) | 186 / 48 of 401 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.87; max drawdown 116.2R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 932 | 48.7 | -0.091 | 0.84 | 96.7R | -0.09 / -0.09 | -0.08 / -0.10 | 1/5 ✗ | -0.17 | -0.25 | ✗  stop atr 2.0→1.6: -0.15R | 1 | 0.14R | 37, -0.07 (+0.09 / -0.40) | 115 / 29 of 285 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.84; max drawdown 96.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 229 | 35.4 | -0.107 | 0.86 | 45.9R | -0.00 / -0.34 | -0.32 / +0.16 | 1/5 ✗ | -0.21 | -0.33 | ✗  time_stop_bars 30→36: -0.13R | 1 | 0.20R | 3, +2.10 (+2.06 / +2.18) | 77 / 169 of 255 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.86; max drawdown 45.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 300 | 47.7 | -0.110 | 0.81 | 35.8R | -0.08 / -0.20 | -0.27 / -0.03 | 1/5 ✗ | -0.26 | -0.39 | ✗  stop atr 1.5→1.2: -0.26R | 1 | 0.26R | 10, -0.70 (-0.42 / -1.33) | 68 / 10 of 97 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.11R/trade (needs +0.10R); profit factor 0.81; max drawdown 35.8R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1418 | 56.2 | -0.112 | 0.61 | 159.2R | -0.11 / -0.12 | -0.14 / -0.09 | 0/5 ✗ | -0.14 | -0.18 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.06R | 5, +0.09 (+0.01 / +0.13) | 616 / 4 of 818 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.61; max drawdown 159.2R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 5244 | 52.8 | -0.140 | 0.51 | 742.5R | -0.12 / -0.20 | -0.15 / -0.13 | 0/5 ✗ | -0.21 | -0.28 | ✗  stop atr 2.0→1.6: -0.17R | 0 | 0.12R | 30, +0.02 (-0.04 / +0.62) | 871 / 10 of 1140 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.51; max drawdown 742.5R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 4778 | 46.8 | -0.152 | 0.74 | 741.9R | -0.16 / -0.14 | -0.17 / -0.12 | 0/5 ✗ | -0.23 | -0.30 | ✗  stop atr 1.5→1.2: -0.19R | 0 | 0.14R | 40, +0.20 (+0.10 / +0.39) | 923 / 205 of 1455 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.74; max drawdown 741.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 268 | 43.3 | -0.153 | 0.73 | 49.0R | -0.17 / -0.12 | -0.23 / -0.06 | 0/5 ✗ | -0.23 | -0.30 | ✗  slow 21→17: -0.21R | 1 | 0.12R | 4, +0.36 (+0.88 / -1.18) | 110 / 8 of 128 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.73; max drawdown 49.0R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 146 | 39.0 | -0.154 | 0.77 | 44.0R | -0.24 / +0.20 | +0.16 / -0.40 | 1/5 ✗ | -0.21 | -0.27 | ✗  depth 0.985→1.182: -0.33R | 1 | 0.12R | 4, +0.53 (+0.41 / +0.88) | 61 / 3 of 74 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.77; max drawdown 44.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 605 | 32.2 | -0.165 | 0.8 | 125.7R | -0.19 / -0.12 | -0.25 / -0.08 | 1/5 ✗ | -0.27 | -0.38 | ✗  stop buffer_atr 0.2→0.16: -0.21R | 1 | 0.23R | 10, -0.44 (-0.73 / +2.18) | 377 / 908 of 1361 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.80; max drawdown 125.7R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 339 | 46.3 | -0.210 | 0.67 | 73.0R | -0.24 / -0.13 | -0.24 / -0.17 | 1/5 ✗ | -0.34 | -0.48 | ✗  bb_n 20→16: -0.34R | 1 | 0.23R | 15, -0.09 (-0.27 / +0.18) | 88 / 27 of 158 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.67; max drawdown 73.0R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 242 | 47.5 | -0.214 | 0.65 | 52.7R | -0.22 / -0.19 | -0.22 / -0.20 | 0/5 ✗ | -0.30 | -0.39 | ✗  vol_x 1.2→1.44: -0.38R | 1 | 0.18R | 3, +0.10 (-0.41 / +1.11) | 68 / 148 of 225 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.65; max drawdown 52.7R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 2468 | 45.8 | -0.215 | 0.66 | 533.8R | -0.19 / -0.28 | -0.24 / -0.18 | 0/5 ✗ | -0.35 | -0.47 | ✗  stop atr 1.5→1.2: -0.28R | 0 | 0.20R | 84, -0.10 (-0.09 / -0.12) | 647 / 183 of 1304 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.66; max drawdown 533.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 208 | 44.7 | -0.230 | 0.61 | 51.3R | -0.23 / -0.24 | -0.31 / -0.15 | 0/5 ✗ | -0.30 | -0.35 | ✗  st_n 10→12: -0.26R | 1 | 0.09R | 4, +1.16 (+1.47 / +0.24) | 41 / 1 of 51 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.61; max drawdown 51.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 1949 | 43.6 | -0.234 | 0.34 | 456.9R | -0.21 / -0.29 | -0.28 / -0.18 | 0/5 ✗ | -0.35 | -0.47 | ✗  stop atr 2.0→1.6: -0.29R | 0 | 0.19R | 34, -0.19 (-0.09 / -0.46) | 889 / 38 of 1087 | 0 | avg -0.23R/trade (needs +0.10R); profit factor 0.34; max drawdown 456.9R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 201 | 46.3 | -0.236 | 0.63 | 55.5R | -0.18 / -0.44 | -0.40 / -0.07 | 0/5 ✗ | -0.36 | -0.46 | ✗  stop atr 1.5→1.2: -0.31R | 0 | 0.23R | 6, -0.93 (-1.13 / -0.54) | 133 / 8 of 151 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.63; max drawdown 55.5R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 225 | 40.0 | -0.240 | 0.61 | 55.8R | -0.19 / -0.41 | -0.34 / -0.15 | 1/5 ✗ | -0.35 | -0.46 | ✗  fast 9→11: -0.33R | 0 | 0.18R | 9, -0.66 (+0.32 / -1.15) | 84 / 20 of 121 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.61; max drawdown 55.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 110 | 45.5 | -0.241 | 0.58 | 27.6R | -0.23 / -0.28 | -0.17 / -0.30 | 0/5 ✗ | -0.31 | -0.42 | ✗  adx_min 20→24: -0.31R | 0 | 0.14R | 4, -0.57 (-1.16 / +0.01) | 44 / 4 of 57 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.58; max drawdown 27.6R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 2128 | 44.1 | -0.285 | 0.58 | 608.4R | -0.24 / -0.39 | -0.35 / -0.25 | 0/5 ✗ | -0.46 | -0.64 | ✗  stop atr 1.5→1.2: -0.38R | 0 | 0.28R | 137, -0.20 (-0.10 / -0.40) | 1077 / 139 of 1913 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.29R/trade (needs +0.10R); profit factor 0.58; max drawdown 608.4R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 62 | 30.6 | -0.303 | 0.6 | 21.3R | -0.40 / +0.01 | -0.24 / -0.35 | 1/5 ✗ | -0.37 | -0.49 | ✗  depth 0.985→1.182: -0.51R | 0 | 0.16R | 6, -0.30 (+1.30 / -0.62) | 25 / 2 of 33 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.60; max drawdown 21.3R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 31 | 32.3 | -0.319 | 0.58 | 11.0R | -0.11 / -0.65 | -0.59 / +0.01 | 0/5 ✗ | -0.48 | -0.59 | ✗  time_stop_bars 30→24: -0.40R | 2 | 0.16R | 6, -0.69 (-0.69 / +0.00) | 76 / 29 of 121 | 0 | avg -0.32R/trade (needs +0.10R); profit factor 0.58; max drawdown 11.0R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 987 | 29.4 | -0.319 | 0.6 | 317.0R | -0.34 / -0.27 | -0.31 / -0.33 | 0/5 ✗ | -0.40 | -0.48 | ✗  rsi_n 14→17: -0.43R | 1 | 0.15R | 4, +0.10 (+1.29 / -1.09) | 601 / 3 of 639 | 0 | avg -0.32R/trade (needs +0.10R); profit factor 0.60; max drawdown 317.0R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1074 | 31.1 | -0.346 | 0.58 | 383.7R | -0.37 / -0.30 | -0.34 / -0.35 | 0/5 ✗ | -0.49 | -0.63 | ✗  stop atr 1.5→1.2: -0.41R | 0 | 0.24R | 23, +0.19 (+0.61 / -0.78) | 488 / 22 of 599 | 0 | avg -0.35R/trade (needs +0.10R); profit factor 0.58; max drawdown 383.7R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 1482 | 30.2 | -0.389 | 0.17 | 576.6R | -0.37 / -0.42 | -0.49 / -0.30 | 0/5 ✗ | -0.58 | -0.77 | ✗  hi 90→108: -0.49R | 0 | 0.32R | 68, -0.33 (-0.38 / -0.26) | 1012 / 42 of 1155 | 0 | not cost-viable: fees + slippage 0.32R per trade (stop must be ≥ 4x the round-trip cost); avg -0.39R/trade (needs +0.10R); profit factor 0.17; max drawdown 576.6R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 384 | 39.6 | -0.408 | 0.47 | 160.8R | -0.37 / -0.48 | -0.38 / -0.42 | 0/5 ✗ | -0.57 | -0.74 | ✗  stop atr 1.5→1.2: -0.48R | 0 | 0.31R | 26, -0.68 (-0.84 / -0.24) | 72 / 22 of 140 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); avg -0.41R/trade (needs +0.10R); profit factor 0.47; max drawdown 160.8R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 414 | 25.6 | -0.462 | 0.53 | 195.9R | -0.51 / -0.35 | -0.65 / -0.26 | 0/5 ✗ | -0.64 | -0.78 | ✗  n 20→24: -0.51R | 1 | 0.36R | 20, -0.51 (-0.62 / -0.17) | 402 / 886 of 1422 | 0 | not cost-viable: fees + slippage 0.36R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.53; max drawdown 195.9R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 398 | 37.9 | -0.525 | 0.35 | 209.0R | -0.46 / -0.71 | -0.62 / -0.47 | 0/5 ✗ | -0.75 | -1.01 | ✗  stop atr 1.0→0.8: -0.60R | 0 | 0.40R | 23, -0.53 (-0.48 / -1.43) | 87 / 214 of 329 | 0 | not cost-viable: fees + slippage 0.40R per trade (stop must be ≥ 4x the round-trip cost); avg -0.53R/trade (needs +0.10R); profit factor 0.35; max drawdown 209.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 77 | 19.5 | -0.557 | 0.45 | 47.7R | -0.54 / -0.58 | -0.76 / -0.32 | 1/5 ✗ | -0.70 | -0.85 | ✗  time_stop_bars 30→36: -0.57R | 1 | 0.27R | 3, +1.32 (+1.32 / +0.00) | 34 / 83 of 124 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.56R/trade (needs +0.10R); profit factor 0.45; max drawdown 47.7R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 230 | 34.3 | -0.577 | 0.29 | 132.7R | -0.55 / -0.66 | -0.57 / -0.59 | 0/5 ✗ | -0.75 | -0.92 | ✗  long_rsi_max 45→36: -0.62R | 0 | 0.31R | 10, -0.67 (-0.59 / -1.34) | 90 / 183 of 292 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); avg -0.58R/trade (needs +0.10R); profit factor 0.29; max drawdown 132.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 202 | 29.2 | -0.867 | 0.21 | 175.3R | -0.86 / -0.87 | -0.84 / -1.05 | 0/5 ✗ | -1.33 | -1.81 | ✗  stop atr 1.5→1.2: -1.14R | 0 | 0.72R | 57, -0.64 (-0.44 / -1.07) | 159 / 29 of 248 | 0 | not cost-viable: fees + slippage 0.72R per trade (stop must be ≥ 4x the round-trip cost); avg -0.87R/trade (needs +0.10R); profit factor 0.21; max drawdown 175.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 346 | 24.9 | -1.313 | 0.13 | 454.5R | -1.29 / -1.35 | -1.20 / -2.17 | 0/5 ✗ | -2.09 | -2.84 | ✗  stop atr 1.0→0.8: -1.70R | 0 | 1.17R | 98, -0.79 (-0.64 / -1.64) | 199 / 508 of 824 | 0 | not cost-viable: fees + slippage 1.17R per trade (stop must be ≥ 4x the round-trip cost); avg -1.31R/trade (needs +0.10R); profit factor 0.13; max drawdown 454.5R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **28** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 136 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.38** (Bonferroni: family-wise false-winner rate 0.05 over 136 trials; with 1 trial it would be 1.65).

**Research run duration:** 8.9 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 28 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (115.1 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 40 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

4 of 68 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT-VRVOL-S5 v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 10.03 | 16.8R | 430 d (13%) | passes every gate |
| donchian_breakout-VEXIT-VRVOL v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 10.03 | 16.8R | 430 d (13%) | passes every gate |
| donchian_breakout-VEXIT v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 10.03 | 16.8R | 430 d (13%) | passes every gate |
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 7.62 | 14.2R | 592 d (18%) | passes every gate |

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (79% of 2,549 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (76% of 1,073 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 926 trades shared)

- donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (79% of 2,549 trades shared)

- donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (76% of 1,073 trades shared)

- donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 926 trades shared)

- donchian_breakout-VEXIT-VRVOL-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (79% of 2,549 trades shared)

- donchian_breakout-VEXIT-VRVOL-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (76% of 1,073 trades shared)

- donchian_breakout-VEXIT-VRVOL-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 926 trades shared)

- donchian_breakout-VEXIT-VRVOL-S5 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,236 trades shared)

- donchian_breakout-VEXIT-VRVOL-S5 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 909 trades shared)

- donchian_breakout-VEXIT-VRVOL-S5 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 814 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,236 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 909 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 814 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,236 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 909 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 814 trades shared)

🧪 **Strategy lab:** 4 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S8-PDH-PDL-SWEEP-5M | 30m | 2 | +0.037 | +0.037 | -0.018 | +0.427 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.319 | -0.645 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 4 | -0.845 | -1.323 | -0.471 | +0.049 | too few trades to compare |
| S7-SILVER-BULLET | 15m | 2 | -1.134 | +0.000 | -0.355 | +0.148 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 3 | -1.236 | +0.000 | +0.010 | -0.465 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 229 | -0.107 | -0.344 | -0.165 | -0.123 | no |
| S8-PDH-PDL-SWEEP | 30m | 77 | -0.557 | -0.584 | -0.462 | -0.348 | no |

**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): donchian_breakout-VEXIT-VRVOL-S4-S4@1.0 1h FORMALIZED → FAILED; donchian_breakout-VEXIT-VRVOL-S4-S4@1.0 30m FORMALIZED → FAILED; donchian_breakout-VEXIT-VRVOL-S4-S4@1.0 4h FORMALIZED → BACKTESTING; donchian_breakout-VEXIT-VRVOL-S5@1.0 1h FORMALIZED → FAILED; donchian_breakout-VEXIT-VRVOL-S5@1.0 30m FORMALIZED → FAILED; donchian_breakout-VEXIT-VRVOL-S5@1.0 4h FORMALIZED → BACKTESTING
- **Not tested (IDEA / RETIRED):** donchian_breakout-VEXIT-VRVOL v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S5 v1.0 (RETIRED)

### 3c. Research layers (daily run)
Last run: **2026-10-05 00:57 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 7 | 2017-08-17 | 2026-10-04 | 19999 |  |
| 1h | 7 | 2017-08-17 | 2026-10-04 | 79932 |  |
| 30m | 7 | 2024-10-05 | 2026-10-05 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 7 | 2025-10-05 | 2026-10-05 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 7 | 2026-07-07 | 2026-10-05 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 814 (479) | false_breakout, trend_reversal | false_breakout 63% | +0.47R | -0.37R | +0.31 / +0.25 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 926 (552) | false_breakout, trend_reversal | false_breakout 62% | +0.48R | -0.37R | +0.30 / +0.23 |
| donchian_breakout | 4h | BACKTESTING | 837 (371) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 66%, stop_too_tight 34%, no_displacement 33% | +0.33R | -0.37R | +0.21 / +0.15 |
| bb_squeeze_breakout | 4h | FAILED | 215 (103) | false_breakout, stop_too_tight, structural_change | false_breakout 59%, stop_too_tight 42%, regime_mismatch 32% | +0.33R | -0.36R | +0.12 / +0.02 |
| bb_squeeze_breakout | 1h | FAILED | 640 (305) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, no_displacement 51%, stop_too_tight 38%, regime_mismatch 35% | +0.36R | -0.47R | +0.16 / -0.03 |
| macd_trend_cross | 1h | FAILED | 139 (69) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 90%, indicator_lag 44%, stop_too_tight 33% | +0.29R | -0.39R | +0.13 / -0.04 |
| donchian_breakout-VEXIT | 1h | FAILED | 2236 (1510) | false_breakout | false_breakout 63% | +0.51R | -0.39R | +0.07 / -0.04 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2549 (1721) | false_breakout, regime_mismatch | false_breakout 64% | +0.50R | -0.39R | +0.07 / -0.04 |
| donchian_breakout-VEXIT | 30m | FAILED | 909 (599) | false_breakout | false_breakout 72% | +0.47R | -0.39R | +0.12 / -0.06 |
| donchian_breakout | 1h | FAILED | 2297 (1192) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 65%, no_displacement 37%, stop_too_tight 32%, regime_mismatch 26% | +0.37R | -0.40R | +0.05 / -0.06 |
| supertrend_flip | 4h | FAILED | 69 (37) | indicator_lag, structural_change | regime_mismatch 62%, indicator_lag 40% | +0.37R | -0.43R | +0.00 / -0.07 |
| trend_pullback | 4h | FAILED | 931 (483) | regime_mismatch, indicator_lag | regime_mismatch 80%, indicator_lag 38% | +0.36R | -0.43R | +0.00 / -0.08 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1073 (717) | false_breakout | false_breakout 73% | +0.45R | -0.41R | +0.10 / -0.09 |
| donchian_breakout | 30m | FAILED | 932 (478) | false_breakout, stop_too_tight | false_breakout 77%, stop_too_tight 33% | +0.29R | -0.39R | +0.09 / -0.09 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 229 (148) | stop_too_tight, sweep_continued | sweep_continued 97%, range_market 56%, stop_too_tight 30% | +0.56R | -0.40R | +0.15 / -0.11 |
| ema_9_21_cross | 15m | FAILED | 300 (157) | stop_too_tight, indicator_lag | indicator_lag 42%, stop_too_tight 28% | +0.31R | -0.40R | +0.21 / -0.11 |
| rsi2_dip_buy | 4h | FAILED | 1418 (621) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 45% | +0.16R | -0.20R | -0.05 / -0.11 |
| rsi2_dip_buy | 1h | FAILED | 5244 (2475) | trend_reversal, regime_mismatch, volatility_spike, fees_slippage | regime_mismatch 42%, fees_slippage 26% | +0.16R | -0.20R | +0.00 / -0.14 |
| trend_pullback | 1h | FAILED | 4778 (2542) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 77%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.43R | +0.02 / -0.15 |
| ema_9_21_cross | 1h | FAILED | 268 (152) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 48%, stop_too_tight 25% | +0.26R | -0.35R | +0.01 / -0.15 |
| R4-CLUC | 30m | FAILED | 146 (89) | none | wrong_session 66% | +0.30R | -0.45R | -0.03 / -0.15 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 605 (410) | range_market, stop_too_tight | range_market 47%, stop_too_tight 36% | +0.59R | -0.50R | +0.10 / -0.17 |
| bb_squeeze_breakout | 30m | FAILED | 339 (182) | false_breakout, stop_too_tight | false_breakout 64%, stop_too_tight 36% | +0.26R | -0.45R | +0.09 / -0.21 |
| liquidity_sweep_reversal | 1h | FAILED | 242 (127) | stop_too_tight | stop_too_tight 50% | +0.28R | -0.48R | -0.01 / -0.21 |
| trend_pullback | 30m | FAILED | 2468 (1338) | stop_too_tight, indicator_lag | indicator_lag 47%, stop_too_tight 30% | +0.27R | -0.43R | +0.04 / -0.21 |
| supertrend_flip | 1h | FAILED | 208 (115) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 70%, stop_too_tight 36%, indicator_lag 32% | +0.39R | -0.37R | -0.12 / -0.23 |
| rsi2_dip_buy | 30m | FAILED | 1949 (1100) | volatility_spike, fees_slippage | fees_slippage 36% | +0.17R | -0.18R | +0.00 / -0.23 |
| macd_trend_cross | 30m | FAILED | 201 (108) | stop_too_tight, indicator_lag | no_displacement 86%, indicator_lag 46%, low_relative_volume 44%, stop_too_tight 27% | +0.30R | -0.44R | +0.04 / -0.24 |
| ema_9_21_cross | 30m | FAILED | 225 (135) | indicator_lag | indicator_lag 44% | +0.27R | -0.36R | +0.00 / -0.24 |
| supertrend_flip | 30m | FAILED | 110 (60) | late_entry, stop_too_tight, indicator_lag | indicator_lag 40%, regime_mismatch 38%, overextended_entry 33%, stop_too_tight 33% | +0.32R | -0.45R | -0.05 / -0.24 |
| trend_pullback | 15m | FAILED | 2128 (1190) | range_market, wrong_session, stop_too_tight, indicator_lag | indicator_lag 49%, stop_too_tight 31% | +0.25R | -0.43R | +0.07 / -0.28 |
| R4-CLUC | 15m | FAILED | 62 (43) | none | - | +0.44R | -0.19R | -0.14 / -0.30 |
| S6-OB-FVG-noSMC | 15m | FAILED | 31 (21) | none | stop_too_wide 86% | +0.20R | -0.51R | -0.11 / -0.32 |
| R4-BBRSI | 1h | FAILED | 987 (697) | none | - | +0.45R | -0.46R | -0.13 / -0.32 |
| R4-BBRSI | 30m | FAILED | 1074 (740) | none | - | +0.42R | -0.45R | -0.06 / -0.35 |
| rsi2_dip_buy | 15m | FAILED | 1482 (1034) | trend_reversal, fees_slippage | fees_slippage 47% | +0.17R | -0.18R | -0.01 / -0.39 |
| bb_squeeze_breakout | 15m | FAILED | 384 (232) | no_displacement, stop_too_tight | false_breakout 62%, no_displacement 57%, stop_too_tight 42% | +0.31R | -0.50R | -0.02 / -0.41 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 414 (308) | stop_too_tight | stop_too_tight 32% | +0.60R | -0.48R | -0.02 / -0.46 |
| liquidity_sweep_reversal | 15m | FAILED | 398 (247) | stop_too_tight | stop_too_tight 38% | +0.38R | -0.46R | -0.01 / -0.53 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 77 (62) | stop_too_tight, sweep_continued | sweep_continued 95%, stop_too_tight 29% | +0.50R | -0.65R | -0.18 / -0.56 |
| liquidity_sweep_reversal | 30m | FAILED | 230 (151) | stop_too_tight | stop_too_tight 37% | +0.41R | -0.49R | -0.21 / -0.58 |
| ema_9_21_cross | 5m | FAILED | 202 (143) | stop_too_tight, indicator_lag | indicator_lag 54%, stop_too_tight 32% | +0.20R | -0.49R | +0.05 / -0.87 |
| liquidity_sweep_reversal | 5m | FAILED | 346 (260) | htf_conflict, fees_slippage, stop_too_tight | stop_too_tight 38%, fees_slippage 28% | +0.23R | -0.47R | +0.21 / -1.31 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 25 strategy/timeframe tests); `false_breakout` (systematic in 24 strategy/timeframe tests); `regime_mismatch` (systematic in 13 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `trend_reversal` (systematic in 10 strategy/timeframe tests); `fees_slippage` (systematic in 4 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `no_displacement` (systematic in 2 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `range_market` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- BTC up +1.6% (2026-10-04 12:00 → 2026-10-05 00:00 UTC): identifiable: at least one strategy had a valid signal before the move
- SUI up +6.8% (2026-10-04 08:00 → 2026-10-04 16:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 109.2 KB | - | - |
| `memory/cleanup_log.md` | 0.5 KB | - | - |
| `memory/coin_notes.md` | 14.3 KB | 14 | 2026-10-04 02:31 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 8.6 KB | 19 | 2026-10-05 21:32 UTC |
| `memory/experiments.md` | 54.7 KB | 23 | 2026-10-05 17:15 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 185.9 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 13.8 KB | - | - |
| `memory/missed_trades.md` | 30.9 KB | 42 | 2026-10-05 17:10 UTC |
| `memory/playbook.md` | 10.0 KB | - | - |
| `memory/research_sources.md` | 63.4 KB | 48 | 2026-10-05 00:57 UTC |
| `memory/smc_events.csv` | 836.3 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 18.3 KB | - | - |
| `memory/strategy_registry.csv` | 41.8 KB | - | - |
| `memory/trials.csv` | 10.6 KB | - | - |
| `memory/universe_log.md` | 18.9 KB | - | - |

**Reviews due** (review date passed; for the reviews): `missed_trades.md` LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00 (2026-10-02); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03); `missed_trades.md` SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells (2026-10-03); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03) … and 4 more
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG and SHORT = OKX futures fees + funding (always charged, never received). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*