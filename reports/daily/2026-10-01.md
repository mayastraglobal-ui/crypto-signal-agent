# Crypto Signal Report

**Updated:** 2026-10-01 21:24 Beijing time (2026-10-01 13:24 UTC) · data: Binance · 10 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 7.9 MB (GitHub) · large files of this run 4.3 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-01 13:24 UTC / 2026-10-01 21:24 Beijing
No open or pending positions.
Day: +0.00R (limit -3R) · Week: +0.00R (limit -6R) · Heat: 0/3
Risk:      no halt · risk per trade 0.5% · NEXT EVENT US jobs report / Employment Situation (Sep data) 2026-10-02 12:30 UTC
```
Paper = signals of PAPER_TRADING / VALIDATION versions (tracked; PAPER_TRADING ones get PAPER emails). The day / week limits, heat and event blackout are enforced on live (APPROVED) entries by the risk engine (section 2d). Every state change: `reports/position_events.csv`.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.10% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| QNT | **DEGRADED** | 1d: DEGRADED: volume 87x normal on candle 09-28 00:00 UTC (possible bad data); 1d: DEGRADED: volume 56x normal on candle 09-29 00:00 UTC (possible bad data); 1d: DEGRADED: volume 60x normal on candle 09-30 00:00 UTC (possible bad data) |
- 70 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-01 13:24 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 863 h since 2026-08-26 | +0.0021% | 1.44 | 0.60 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=500 |
| ETH | GOOD | okx | 863 h since 2026-08-26 | +0.0081% | 1.34 | 0.69 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ETHUSDT&period=1h&limit=500 |
| SOL | GOOD | okx | 863 h since 2026-08-26 | +0.0037% | 1.96 | 0.80 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SOLUSDT&period=1h&limit=500 |
| ZEC | GOOD | okx | 863 h since 2026-08-26 | +0.0053% | 0.86 | 0.88 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ZECUSDT&period=1h&limit=500 |
| XRP | GOOD | okx | 863 h since 2026-08-26 | +0.0026% | 3.08 | 0.64 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=XRPUSDT&period=1h&limit=500 |
| SUI | GOOD | okx | 863 h since 2026-08-26 | -0.0003% | 2.32 | 0.74 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=SUIUSDT&period=1h&limit=500 |
| ENA | GOOD | okx | 863 h since 2026-08-26 | +0.0050% | 1.26 | 0.85 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=ENAUSDT&period=1h&limit=500 |
| BNB | GOOD | okx | 863 h since 2026-08-26 | +0.0100% | 2.20 | 0.89 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=BNBUSDT&period=1h&limit=500 |
| UNI | GOOD | okx | 863 h since 2026-08-26 | +0.0100% | 1.96 | 1.44 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=UNIUSDT&period=1h&limit=500 |
| AVAX | GOOD | okx | 855 h since 2026-08-26 | +0.0098% | 2.05 | 0.68 | binance: HTTPError: 451 Client Error:  for url: https://fapi.binance.com/futures/data/openInterestHist?symbol=AVAXUSDT&period=1h&limit=500 |

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **ZEC**, **XRP**, **SUI**, **ENA**
- **Research only** - backtested, never a signal: BNB, UNI, AVAX

| Not eligible | 24h volume | Why |
|---|---|---|
| QNT | $145M | order book too thin: $113k within 1% (need $250k) |
| MOVR | $87M | 7-day average volume $11M < $50M; 24h move +78.5% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $34k within 1% (need $250k) |
| VTHO | $66M | 7-day average volume $40M < $50M; spread 0.151% > 0.1%; order book too thin: $93k within 1% (need $250k) |
| HYPE | $54M | only 7 days of history (need 180); 7-day average volume $24M < $50M |

**Flags (not excluded):** QNT: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, RLUSD, USD1, USDC, WLD (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 476 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| ETH | 476 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-08 | OK (300 candles) |
| SOL | 320 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-08 | OK (300 candles) |
| ZEC | 393 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2019-03 | OK (300 candles) |
| XRP | 439 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2018-04 | OK (300 candles) |
| SUI | 178 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 5000 | 2023-05 | OK (300 candles) |
| ENA | 130 | 912 | 906 | 1499 | 1999 | 1999 | 1999 | 4999 | 2024-04 | OK (300 candles) |
| BNB | 464 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2017-11 | OK (300 candles) |
| UNI | 315 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |
| AVAX | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 4999 | 2020-09 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | down (LH/LL) | 84,419.7 / 83,186 | 0.20 | 0.75x | 1.00x | bull_div |
| ETH | mixed (LH/HL) | 2,722 / 2,673.13 | 0.18 | 1.39x | 1.03x | bear_engulf |
| SOL | up (HH/HL) | 119.63 / 117.77 | 0.20 | 1.15x | 0.87x | bull_engulf, bull_reject |
| ZEC | up (HH/HL) | 1,449.75 / 1,407 | 0.16 | 0.87x | 0.97x | bear_engulf, bull_reject, breakout_down, retest_down, failed_breakout_down |
| XRP | down (LH/LL) | 1.5103 / 1.4852 | 0.33 | 0.89x | 0.78x | bull_reject |
| SUI | down (LH/LL) | 1.1821 / 1.139 | 0.15 | 0.97x | 0.88x | bear_engulf, bull_div |
| ENA | mixed (LH/HL) | 0.2783 / 0.2618 | 0.54 | 1.04x | 1.03x | - |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 473 | 48% | 33% | 26% | 80% | 44% | 31% | can't tell from chance | 0.12R |
| 4h | displacement_down | 369 | 50% | 33% | 21% | 75% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 1206 | 45% | 32% | 23% | 77% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | bear_engulf | 1370 | 43% | 28% | 19% | 78% | 47% | 32% | worse than chance | 0.08R |
| 4h | bull_reject | 928 | 42% | 29% | 20% | 79% | 43% | 30% | can't tell from chance | 0.12R |
| 4h | bear_reject | 890 | 46% | 31% | 21% | 74% | 48% | 31% | can't tell from chance | 0.07R |
| 4h | smc_sweep_bull | 649 | 44% | 30% | 22% | 76% | 43% | 30% | can't tell from chance | 0.12R |
| 4h | smc_sweep_bear | 681 | 44% | 29% | 19% | 79% | 47% | 31% | can't tell from chance | 0.08R |
| 4h | smc_bos_up | 280 | 45% | 28% | 21% | 82% | 45% | 30% | can't tell from chance | 0.13R |
| 4h | smc_bos_down | 239 | 47% | 33% | 21% | 72% | 48% | 33% | can't tell from chance | 0.08R |
| 4h | smc_choch_up | 89 | 49% | 31% | 26% | 83% | 44% | 30% | can't tell from chance | 0.13R |
| 4h | smc_choch_down | 89 | 44% | 29% | 18% | 74% | 47% | 33% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bull | 670 | 44% | 28% | 21% | 77% | 44% | 31% | can't tell from chance | 0.12R |
| 4h | smc_fvg_retrace_bear | 688 | 47% | 31% | 20% | 76% | 47% | 31% | can't tell from chance | 0.08R |
| 1h | displacement_up | 617 | 45% | 34% | 27% | 73% | 42% | 29% | can't tell from chance | 0.26R |
| 1h | displacement_down | 431 | 38% | 25% | 16% | 81% | 38% | 25% | can't tell from chance | 0.18R |
| 1h | bull_engulf | 1722 | 39% | 28% | 21% | 75% | 42% | 29% | worse than chance | 0.31R |
| 1h | bear_engulf | 1859 | 38% | 25% | 17% | 80% | 38% | 25% | can't tell from chance | 0.19R |
| 1h | bull_reject | 1378 | 40% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.30R |
| 1h | bear_reject | 1373 | 37% | 25% | 18% | 80% | 39% | 25% | can't tell from chance | 0.17R |
| 1h | smc_sweep_bull | 641 | 42% | 27% | 20% | 77% | 42% | 29% | can't tell from chance | 0.29R |
| 1h | smc_sweep_bear | 717 | 39% | 25% | 16% | 80% | 39% | 25% | can't tell from chance | 0.18R |
| 1h | smc_bos_up | 400 | 44% | 31% | 25% | 78% | 43% | 30% | can't tell from chance | 0.25R |
| 1h | smc_bos_down | 271 | 38% | 28% | 19% | 83% | 38% | 25% | can't tell from chance | 0.21R |
| 1h | smc_choch_up | 111 | 47% | 36% | 32% | 72% | 42% | 29% | can't tell from chance | 0.31R |
| 1h | smc_choch_down | 112 | 43% | 30% | 20% | 74% | 40% | 25% | can't tell from chance | 0.17R |
| 1h | smc_fvg_retrace_bull | 899 | 43% | 31% | 23% | 73% | 43% | 30% | can't tell from chance | 0.28R |
| 1h | smc_fvg_retrace_bear | 827 | 40% | 27% | 18% | 79% | 39% | 25% | can't tell from chance | 0.19R |
| 30m | displacement_up | 572 | 38% | 27% | 21% | 82% | 42% | 29% | can't tell from chance | 0.27R |
| 30m | displacement_down | 439 | 42% | 26% | 15% | 81% | 38% | 23% | can't tell from chance | 0.18R |
| 30m | bull_engulf | 1688 | 40% | 27% | 19% | 77% | 41% | 28% | can't tell from chance | 0.32R |
| 30m | bear_engulf | 1821 | 39% | 23% | 16% | 80% | 38% | 23% | can't tell from chance | 0.20R |
| 30m | bull_reject | 1345 | 44% | 28% | 20% | 75% | 41% | 28% | beats chance | 0.32R |
| 30m | bear_reject | 1438 | 39% | 24% | 16% | 80% | 38% | 23% | can't tell from chance | 0.19R |
| 30m | smc_sweep_bull | 655 | 41% | 27% | 18% | 76% | 41% | 28% | can't tell from chance | 0.33R |
| 30m | smc_sweep_bear | 635 | 44% | 28% | 19% | 80% | 39% | 23% | beats chance | 0.18R |
| 30m | smc_bos_up | 424 | 39% | 30% | 25% | 79% | 42% | 29% | can't tell from chance | 0.29R |
| 30m | smc_bos_down | 245 | 35% | 22% | 12% | 86% | 38% | 23% | can't tell from chance | 0.22R |
| 30m | smc_choch_up | 103 | 39% | 23% | 17% | 84% | 42% | 27% | can't tell from chance | 0.35R |
| 30m | smc_choch_down | 108 | 39% | 23% | 19% | 79% | 40% | 23% | can't tell from chance | 0.17R |
| 30m | smc_fvg_retrace_bull | 984 | 40% | 26% | 19% | 78% | 41% | 27% | can't tell from chance | 0.32R |
| 30m | smc_fvg_retrace_bear | 798 | 39% | 22% | 16% | 79% | 38% | 23% | can't tell from chance | 0.21R |
| 15m | displacement_up | 486 | 36% | 27% | 20% | 82% | 38% | 28% | can't tell from chance | 0.38R |
| 15m | displacement_down | 450 | 33% | 21% | 12% | 84% | 35% | 21% | can't tell from chance | 0.27R |
| 15m | bull_engulf | 1691 | 37% | 27% | 19% | 78% | 36% | 26% | can't tell from chance | 0.46R |
| 15m | bear_engulf | 1638 | 35% | 22% | 13% | 79% | 36% | 21% | can't tell from chance | 0.27R |
| 15m | bull_reject | 1287 | 38% | 27% | 18% | 78% | 35% | 25% | can't tell from chance | 0.46R |
| 15m | bear_reject | 1472 | 36% | 22% | 14% | 81% | 36% | 22% | can't tell from chance | 0.27R |
| 15m | smc_sweep_bull | 602 | 37% | 27% | 20% | 77% | 36% | 25% | can't tell from chance | 0.43R |
| 15m | smc_sweep_bear | 617 | 36% | 23% | 12% | 85% | 36% | 21% | can't tell from chance | 0.26R |
| 15m | smc_bos_up | 366 | 40% | 29% | 22% | 79% | 37% | 26% | can't tell from chance | 0.37R |
| 15m | smc_bos_down | 334 | 33% | 19% | 12% | 85% | 34% | 21% | can't tell from chance | 0.30R |
| 15m | smc_choch_up | 90 | 34% | 22% | 14% | 83% | 34% | 25% | can't tell from chance | 0.44R |
| 15m | smc_choch_down | 85 | 34% | 21% | 14% | 82% | 34% | 22% | can't tell from chance | 0.28R |
| 15m | smc_fvg_retrace_bull | 1088 | 36% | 25% | 17% | 79% | 36% | 26% | can't tell from chance | 0.46R |
| 15m | smc_fvg_retrace_bear | 935 | 34% | 22% | 14% | 82% | 35% | 21% | can't tell from chance | 0.29R |
| 5m | displacement_up | 1314 | 32% | 22% | 18% | 84% | 30% | 21% | can't tell from chance | 0.73R |
| 5m | displacement_down | 1173 | 27% | 17% | 12% | 87% | 31% | 21% | worse than chance | 0.44R |
| 5m | bull_engulf | 4218 | 29% | 20% | 15% | 82% | 30% | 21% | can't tell from chance | 0.76R |
| 5m | bear_engulf | 4181 | 31% | 20% | 12% | 83% | 31% | 20% | can't tell from chance | 0.48R |
| 5m | bull_reject | 3234 | 29% | 20% | 15% | 80% | 30% | 21% | can't tell from chance | 0.80R |
| 5m | bear_reject | 3688 | 33% | 21% | 14% | 82% | 32% | 21% | can't tell from chance | 0.43R |
| 5m | smc_sweep_bull | 1246 | 30% | 22% | 15% | 80% | 31% | 22% | can't tell from chance | 0.69R |
| 5m | smc_sweep_bear | 1284 | 35% | 25% | 16% | 81% | 33% | 21% | can't tell from chance | 0.41R |
| 5m | smc_bos_up | 908 | 32% | 23% | 19% | 83% | 30% | 22% | can't tell from chance | 0.73R |
| 5m | smc_bos_down | 820 | 27% | 17% | 11% | 87% | 31% | 20% | worse than chance | 0.51R |
| 5m | smc_choch_up | 229 | 34% | 27% | 19% | 84% | 29% | 21% | can't tell from chance | 0.80R |
| 5m | smc_choch_down | 231 | 26% | 16% | 10% | 87% | 31% | 20% | can't tell from chance | 0.49R |
| 5m | smc_fvg_retrace_bull | 3425 | 31% | 22% | 16% | 81% | 29% | 20% | beats chance | 0.79R |
| 5m | smc_fvg_retrace_bear | 2950 | 29% | 19% | 12% | 84% | 31% | 20% | worse than chance | 0.49R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (moderate) | WEAK_BULL (moderate) | WEAK_BULL (weak) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ETH** | WEAK_BULL (weak) | STRONG_BULL (strong) | RANGE (moderate) | RANGE (moderate) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H RANGE)) |
| **SOL** | TRANSITION (weak) | WEAK_BULL (moderate) | WEAK_BULL (weak) | RANGE (moderate) | LONG allowed (1D/4H bullish, 1W TRANSITION) |
| **ZEC** | WEAK_BULL (weak) | STRONG_BULL (weak) | RANGE (moderate) | RANGE (weak) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H RANGE)) |
| **XRP** | TRANSITION (weak) | TRANSITION (weak) | RANGE (weak) | COMPRESSION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H RANGE, 1H COMPRESSION)) |
| **SUI** | UNCLEAR (weak) | EXPANSION down (weak) | WEAK_BULL (weak) | RANGE (moderate) | NO TRADE (timeframes disagree (1D EXPANSION, 4H WEAK_BULL, 1H RANGE)) |
| **ENA** | TRANSITION (weak) | WEAK_BULL (weak) | TRANSITION (weak) | UNCLEAR (weak) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H UNCLEAR)) |
| **BNB** | WEAK_BULL (weak) | STRONG_BULL (moderate) | RANGE (moderate) | RANGE (strong) | NO TRADE (timeframes disagree (1D STRONG_BULL, 4H RANGE, 1H RANGE)) |
| **UNI** | EXPANSION up (moderate) | WEAK_BULL (weak) | RANGE (moderate) | RANGE (strong) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H RANGE, 1H RANGE)) |
| **AVAX** | TRANSITION (weak) | WEAK_BULL (weak) | WEAK_BULL (weak) | COMPRESSION (strong) | LONG allowed (1D/4H bullish, 1W TRANSITION) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (moderate)** - for: EMA-fast rising (+1.5 ATR in 10 candles); swing structure down (LH/LL); ADX 27 = strong trend; candle size 0.73x normal, Bollinger width above 56% of the last 100 candles · against: EMAs not lined up
- **1D WEAK_BULL (moderate)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.4 ATR in 10 candles); ADX 42 = strong trend; candle size 1.04x normal, Bollinger width above 79% of the last 100 candles; volume 0.88x normal · against: swing structure mixed (neutral)
- **4H WEAK_BULL (weak)** - for: close above EMA-fast above EMA-slow; swing structure up (HH/HL); candle size 0.99x normal, Bollinger width above 10% of the last 100 candles; volume 0.78x normal · against: EMA-fast flat (+0.1 ATR in 10 candles) (neutral); ADX 17 = weak trend / ranging
- **1H RANGE (moderate)** - for: EMAs not lined up; EMA-fast flat (+0.1 ATR in 10 candles); ADX 12 = weak trend / ranging; candle size 1.00x normal, Bollinger width above 9% of the last 100 candles · against: swing structure down (LH/LL)

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **NY AM**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | down (CHOCH 23 candles ago) | sell-side (bullish idea) 18 candles ago | bear 83,744.01-83,840.00 | bear 84,342.00-84,843.00 | discount (45%) | swing high 84,419.69 (1.56 ATR) | swing low 83,186.00 (1.25 ATR) |
| **ETH** | down (BOS 23 candles ago) | sell-side (bullish idea) 138 candles ago | bear 2,693.71-2,702.95 | bull 2,652.20-2,695.38 | discount (40%) | swing high 2,722.00 (1.63 ATR) | swing low 2,673.13 (1.09 ATR) |
| **SOL** | down (BOS 1 candles ago) | sell-side (bullish idea) 12 candles ago | bear 117.38-117.60 | bull 115.86-117.34 | below the range (-22%) | swing high 119.63 (2.26 ATR) | swing low 117.06 (0.3 ATR) |
| **ZEC** | down (BOS 12 candles ago) | sell-side (bullish idea) 12 candles ago | bear 1,397.13-1,405.17 | bear 1,540.16-1,569.23 | below the range (-29%) | swing high 1,447.60 (2.19 ATR) | swing low 1,356.00 (1.6 ATR) |
| **XRP** | down (BOS 0 candles ago) | sell-side (bullish idea) 1 candles ago | bear 1.4925-1.5022 (retraced) | bull 1.3773-1.3856 | discount (9%) | swing high 1.5103 (1.79 ATR) | swing low 1.4764 (0.87 ATR) |
| **SUI** | down (CHOCH 23 candles ago) | buy-side (bearish idea) 9 candles ago | bear 1.1635-1.1673 | bull 1.0050-1.0598 | discount (45%) | swing high 1.1821 (1.13 ATR) | equal lows 1.1383 (0.95 ATR) |
| **ENA** | up (BOS 27 candles ago) | buy-side (bearish idea) 3 candles ago | bear 0.27070-0.27210 | bull 0.16130-0.17050 | discount (2%) | swing high 0.27830 (2.61 ATR) | swing low 0.25240 (1.59 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 74 (Greed), yesterday 71  (extreme fear/greed = bigger, faster moves)

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
- **Event calendar (next 7 days):** US jobs report / Employment Situation (Sep data) 2026-10-02 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-10-01 00:55 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 5 | 60.0 | +1.221 | 3.69 | 2.3R | +0.97 / +2.21 | +2.21 / +0.97 | 0/5 ✗ | +1.10 | +0.98 | stable | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 16 / 7 of 24 | 0 | only 5 trades; only 1 unseen-test trades |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 17 | 47.1 | +0.236 | 1.31 | 5.8R | +0.10 / +0.56 | -0.09 / +0.46 | 0/5 ✗ | -0.07 | -0.24 | ✗  sweep_bars 8→10: -0.06R | 0 | 0.31R | 2, +0.31 (+0.31 / +0.00) | 48 / 21 of 75 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); only 17 trades; only 5 unseen-test trades |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 6 | 50.0 | +0.206 | 1.21 | 3.3R | +0.51 / -1.32 | -1.32 / +0.51 | 0/5 ✗ | -2.17 | -1.32 | ✗  stop buffer_atr 0.2→0.24: -1.98R | 0 | 0.26R | 1, -1.32 (-1.32 / +0.00) | 40 / 12 of 58 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); only 6 trades; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1045 | 39.9 | +0.192 | 1.35 | 34.2R | +0.18 / +0.22 | +0.24 / +0.14 | 5/5 | +0.16 | +0.13 | stable | 9 | 0.04R | 16, +0.74 (+0.74 / +0.00) | 92 / 47 of 267 | 0 | max drawdown 34.2R |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1045 | 39.9 | +0.192 | 1.35 | 34.2R | +0.18 / +0.22 | +0.24 / +0.14 | 5/5 | +0.16 | +0.13 | stable | 9 | 0.04R | 16, +0.74 (+0.74 / +0.00) | 92 / 47 of 267 | 0 | max drawdown 34.2R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1183 | 39.4 | +0.190 | 1.35 | 34.4R | +0.18 / +0.21 | +0.20 / +0.17 | 5/5 | +0.16 | +0.14 | stable | 9 | 0.04R | 17, +0.81 (+0.92 / -1.04) | 157 / 60 of 360 | 0 | max drawdown 34.4R |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 1073 | 54.1 | +0.107 | 1.24 | 28.0R | +0.10 / +0.12 | +0.11 / +0.11 | 4/5 | +0.08 | +0.05 | stable | 7 | 0.04R | 18, +0.33 (+0.41 / -1.04) | 92 / 47 of 267 | 0 | max drawdown 28.0R |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 2 | 50.0 | +0.037 | 1.04 | 1.7R | +0.00 / +0.04 | +0.04 / +0.00 | 0/5 ✗ | -0.27 | -0.54 | ✗  time_stop_bars 30→36: -0.30R | 0 | 0.70R | 1, +1.79 (+0.00 / +1.79) | 30 / 107 of 151 | 0 | not cost-viable: fees + slippage 0.70R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; avg +0.04R/trade (needs +0.10R); profit factor 1.04; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop max_width_atr 3.0→3.6: -1.14R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 4 / 4 of 8 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 69 / 18 of 90 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 40 / 12 of 58 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 4 / 4 of 8 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 16 / 7 of 24 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 14 | 50.0 | -0.126 | 0.77 | 4.8R | -0.15 / +0.05 | -0.31 / -0.05 | 0/5 ✗ | -0.09 | -0.28 | ✗  time_stop_bars 30→24: -0.22R | 0 | 0.16R | 0, +0.00 (+0.00 / +0.00) | 487 / 222 of 858 | 0 | only 14 trades; avg -0.13R/trade (needs +0.10R); profit factor 0.77; only 2 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 13 | 23.1 | -0.334 | 0.45 | 4.9R | -0.54 / +0.14 | -1.11 / -0.27 | 0/5 ✗ | -0.44 | -0.34 | ✗  stop buffer_atr 0.2→0.24: -0.34R | 0 | 0.09R | 0, +0.00 (+0.00 / +0.00) | 548 / 202 of 892 | 0 | only 13 trades; avg -0.33R/trade (needs +0.10R); profit factor 0.45; only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 5 | 0.0 | -1.187 | 0.0 | 5.9R | -1.19 / -1.16 | -1.42 / -1.13 | 0/5 ✗ | -1.19 | -1.25 | ✗  stop max_width_atr 3.0→2.4: -1.22R | 0 | 0.19R | 0, +0.00 (+0.00 / +0.00) | 69 / 18 of 90 | 0 | only 5 trades; avg -1.19R/trade (needs +0.10R); profit factor 0.00; only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 272 | 51.8 | +0.025 | 1.05 | 26.7R | +0.19 / -0.28 | +0.09 / -0.03 | 3/5 ✗ | -0.03 | -0.07 | ✗  stop atr 1.5→1.8: -0.02R | 6 | 0.07R | 2, +0.11 (+1.27 / -1.05) | 101 / 22 of 141 | 0 | avg +0.03R/trade (needs +0.10R); profit factor 1.05; max drawdown 26.7R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **FAILED** | 188 | 51.6 | -0.013 | 0.98 | 30.7R | -0.15 / +0.28 | -0.08 / +0.05 | 2/5 ✗ | -0.07 | -0.14 | ✗  stop atr 1.5→1.2: -0.09R | 4 | 0.13R | 1, -0.02 (-0.02 / +0.00) | 222 / 6 of 230 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.98; max drawdown 30.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1294 | 34.6 | -0.022 | 0.97 | 97.8R | -0.04 / +0.02 | +0.05 / -0.09 | 2/5 ✗ | -0.10 | -0.17 | ✗  stop atr 2.0→1.6: -0.12R | 4 | 0.12R | 52, +0.18 (+0.30 / -0.74) | 143 / 39 of 371 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 97.8R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 30m | **FAILED** | 1294 | 34.6 | -0.022 | 0.97 | 97.8R | -0.04 / +0.02 | +0.05 / -0.09 | 2/5 ✗ | -0.10 | -0.17 | ✗  stop atr 2.0→1.6: -0.12R | 4 | 0.12R | 52, +0.18 (+0.30 / -0.74) | 143 / 39 of 371 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; max drawdown 97.8R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 1h | **FAILED** | 826 | 52.1 | -0.028 | 0.95 | 53.4R | -0.04 / -0.01 | -0.08 / +0.02 | 1/5 ✗ | -0.11 | -0.19 | ✗  stop atr 1.5→1.2: -0.06R | 4 | 0.14R | 7, +0.30 (-0.10 / +0.84) | 140 / 38 of 216 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; max drawdown 53.4R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **FAILED** | 36 | 52.8 | -0.032 | 0.94 | 6.0R | +0.15 / -0.40 | +0.30 / -0.41 | 2/5 ✗ | -0.06 | -0.10 | ✗  stop atr 1.5→1.8: -0.04R | 2 | 0.06R | 1, +0.24 (+0.00 / +0.24) | 158 / 4 of 165 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.94; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1522 | 34.3 | -0.034 | 0.95 | 109.3R | -0.05 / +0.02 | +0.02 / -0.09 | 2/5 ✗ | -0.12 | -0.19 | ✗  stop atr 2.0→1.6: -0.12R | 3 | 0.12R | 57, +0.23 (+0.23 / +0.21) | 247 / 62 of 522 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; max drawdown 109.3R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1328 | 49.5 | -0.055 | 0.9 | 110.0R | -0.06 / -0.04 | -0.02 / -0.09 | 1/5 ✗ | -0.13 | -0.20 | ✗  stop atr 2.0→1.6: -0.14R | 3 | 0.12R | 52, +0.14 (+0.22 / -0.48) | 143 / 39 of 371 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.90; max drawdown 110.0R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 3250 | 32.2 | -0.055 | 0.91 | 266.6R | -0.09 / +0.01 | -0.04 / -0.07 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.09R | 35, +0.49 (+0.56 / +0.06) | 208 / 125 of 566 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 266.6R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 1192 | 49.1 | -0.056 | 0.89 | 108.3R | -0.01 / -0.17 | +0.00 / -0.12 | 1/5 ✗ | -0.10 | -0.13 | ✗  long_rsi_hi 65→52: -0.13R | 4 | 0.06R | 13, -0.06 (+0.61 / -0.85) | 677 / 201 of 1051 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 108.3R; not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2938 | 48.3 | -0.057 | 0.89 | 199.7R | -0.07 / -0.02 | -0.07 / -0.04 | 0/5 ✗ | -0.11 | -0.15 | ✗  stop atr 2.0→1.6: -0.07R | 1 | 0.08R | 34, +0.36 (+0.45 / -0.59) | 122 / 90 of 412 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.89; max drawdown 199.7R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2864 | 31.9 | -0.060 | 0.91 | 245.8R | -0.10 / +0.02 | -0.05 / -0.07 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.09R | 33, +0.42 (+0.56 / -0.97) | 122 / 90 of 412 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 245.8R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-VRVOL 🧪 lab | 1.0 | 1h | **FAILED** | 2864 | 31.9 | -0.060 | 0.91 | 246.7R | -0.10 / +0.02 | -0.05 / -0.07 | 1/5 ✗ | -0.11 | -0.16 | ✗  stop atr 2.0→1.6: -0.09R | 2 | 0.09R | 33, +0.42 (+0.56 / -0.97) | 122 / 90 of 412 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 246.7R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 93 | 46.2 | -0.085 | 0.85 | 18.5R | +0.08 / -0.38 | -0.14 / -0.02 | 3/5 ✗ | -0.11 | -0.13 | ✗  time_stop_bars 60→48: -0.08R | 1 | 0.05R | 1, +1.82 (+1.82 / +0.00) | 42 / 6 of 50 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.85; max drawdown 18.5R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 90 | 37.8 | -0.101 | 0.85 | 21.8R | -0.25 / +0.39 | -0.08 / -0.12 | 2/5 ✗ | -0.16 | -0.26 | ✗  depth 0.985→1.182: -0.44R | 3 | 0.15R | 2, +1.30 (+1.30 / +0.00) | 41 / 6 of 49 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.85; max drawdown 21.8R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1781 | 56.3 | -0.106 | 0.63 | 189.4R | -0.10 / -0.12 | -0.13 / -0.09 | 0/5 ✗ | -0.14 | -0.17 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.05R | 2, -0.03 (+0.00 / -0.03) | 760 / 4 of 1012 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.63; max drawdown 189.4R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 341 | 44.9 | -0.119 | 0.78 | 51.7R | -0.13 / -0.10 | -0.19 / -0.05 | 0/5 ✗ | -0.18 | -0.25 | ✗  slow 21→17: -0.20R | 3 | 0.12R | 5, +0.01 (-1.00 / +1.52) | 140 / 9 of 159 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.78; max drawdown 51.7R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 6696 | 53.8 | -0.128 | 0.55 | 864.6R | -0.11 / -0.18 | -0.14 / -0.11 | 0/5 ✗ | -0.19 | -0.26 | ✗  stop atr 2.0→1.6: -0.16R | 0 | 0.11R | 46, -0.08 (-0.08 / -0.08) | 1060 / 7 of 1409 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.55; max drawdown 864.6R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 6104 | 47.7 | -0.130 | 0.77 | 803.9R | -0.13 / -0.13 | -0.17 / -0.09 | 0/5 ✗ | -0.20 | -0.27 | ✗  stop atr 1.5→1.2: -0.17R | 1 | 0.13R | 50, -0.13 (+0.05 / -0.73) | 1135 / 287 of 1803 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.77; max drawdown 803.9R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 167 | 47.9 | -0.135 | 0.76 | 25.1R | -0.15 / -0.09 | -0.13 / -0.14 | 1/5 ✗ | -0.20 | -0.28 | ✗  adx_min 20→24: -0.17R | 2 | 0.13R | 6, -0.27 (-0.07 / -1.26) | 55 / 5 of 71 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.76; max drawdown 25.1R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 291 | 32.6 | -0.147 | 0.81 | 59.7R | -0.02 / -0.42 | -0.34 / +0.05 | 1/5 ✗ | -0.25 | -0.36 | ✗  time_stop_bars 30→36: -0.17R | 1 | 0.20R | 4, +0.34 (+2.70 / -0.44) | 87 / 212 of 310 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.81; max drawdown 59.7R; not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 252 | 38.1 | -0.168 | 0.74 | 63.8R | -0.18 / -0.14 | +0.10 / -0.33 | 1/5 ✗ | -0.22 | -0.27 | ✗  depth 0.985→1.182: -0.28R | 1 | 0.10R | 6, +0.50 (+0.50 / +0.00) | 89 / 8 of 109 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.74; max drawdown 63.8R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 44 | 36.4 | -0.181 | 0.74 | 12.5R | +0.05 / -0.51 | -0.44 / +0.05 | 1/5 ✗ | -0.35 | -0.45 | ✗  stop buffer_atr 0.2→0.16: -0.18R | 3 | 0.16R | 7, -0.82 (-0.71 / -1.51) | 105 / 37 of 156 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.74; max drawdown 12.5R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 271 | 45.0 | -0.191 | 0.68 | 56.8R | -0.20 / -0.16 | -0.30 / -0.10 | 1/5 ✗ | -0.26 | -0.30 | ✗  stop atr 2.0→2.4: -0.20R | 2 | 0.08R | 6, +0.53 (+0.39 / +1.25) | 54 / 3 of 67 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.68; max drawdown 56.8R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 464 | 43.8 | -0.192 | 0.68 | 90.5R | -0.18 / -0.23 | -0.29 / -0.15 | 0/5 ✗ | -0.33 | -0.47 | ✗  stop atr 1.5→1.2: -0.31R | 1 | 0.25R | 21, -0.32 (-0.04 / -1.04) | 88 / 15 of 126 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.19R/trade (needs +0.10R); profit factor 0.68; max drawdown 90.5R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 2820 | 47.0 | -0.196 | 0.41 | 552.9R | -0.18 / -0.24 | -0.24 / -0.15 | 0/5 ✗ | -0.30 | -0.40 | ✗  stop atr 2.0→1.6: -0.25R | 0 | 0.16R | 46, -0.08 (-0.05 / -0.11) | 1039 / 32 of 1275 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.41; max drawdown 552.9R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 3540 | 45.9 | -0.198 | 0.68 | 702.9R | -0.17 / -0.27 | -0.23 / -0.17 | 0/5 ✗ | -0.31 | -0.41 | ✗  stop atr 1.5→1.2: -0.25R | 0 | 0.17R | 101, -0.17 (+0.05 / -0.86) | 868 / 231 of 1622 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 702.9R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 507 | 46.2 | -0.201 | 0.68 | 103.6R | -0.22 / -0.16 | -0.26 / -0.14 | 1/5 ✗ | -0.31 | -0.43 | ✗  stop atr 1.5→1.2: -0.27R | 2 | 0.18R | 18, -0.50 (-0.60 / -0.03) | 125 / 36 of 206 | 0 | avg -0.20R/trade (needs +0.10R); profit factor 0.68; max drawdown 103.6R; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 302 | 46.7 | -0.214 | 0.66 | 73.3R | -0.12 / -0.47 | -0.33 / -0.12 | 0/5 ✗ | -0.34 | -0.43 | ✗  stop atr 1.5→1.2: -0.28R | 1 | 0.19R | 6, -0.78 (-0.85 / -0.63) | 165 / 10 of 187 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.66; max drawdown 73.3R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 822 | 30.4 | -0.214 | 0.74 | 190.9R | -0.17 / -0.29 | -0.28 / -0.16 | 1/5 ✗ | -0.32 | -0.42 | ✗  stop buffer_atr 0.2→0.16: -0.27R | 1 | 0.21R | 18, -0.35 (+0.36 / -1.07) | 462 / 1123 of 1674 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.74; max drawdown 190.9R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 304 | 46.7 | -0.222 | 0.64 | 67.7R | -0.21 / -0.26 | -0.23 / -0.21 | 0/5 ✗ | -0.30 | -0.39 | ✗  vol_x 1.2→1.44: -0.36R | 2 | 0.17R | 6, -0.30 (-0.41 / +0.27) | 102 / 200 of 312 | 0 | avg -0.22R/trade (needs +0.10R); profit factor 0.64; max drawdown 67.7R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 352 | 38.9 | -0.249 | 0.59 | 90.3R | -0.22 / -0.34 | -0.33 / -0.19 | 0/5 ✗ | -0.34 | -0.44 | ✗  fast 9→11: -0.34R | 0 | 0.16R | 11, +0.04 (+0.21 / -0.76) | 116 / 20 of 155 | 0 | avg -0.25R/trade (needs +0.10R); profit factor 0.59; max drawdown 90.3R; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 3098 | 44.8 | -0.252 | 0.62 | 781.0R | -0.23 / -0.31 | -0.31 / -0.22 | 0/5 ✗ | -0.40 | -0.55 | ✗  stop atr 1.5→1.2: -0.33R | 0 | 0.25R | 187, -0.12 (+0.04 / -0.91) | 1357 / 197 of 2195 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.25R/trade (needs +0.10R); profit factor 0.62; max drawdown 781.0R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 1520 | 31.9 | -0.303 | 0.62 | 470.7R | -0.32 / -0.26 | -0.31 / -0.30 | 0/5 ✗ | -0.43 | -0.55 | ✗  stop atr 1.5→1.2: -0.35R | 0 | 0.21R | 25, +0.23 (+0.09 / +0.39) | 608 / 31 of 738 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.62; max drawdown 470.7R; not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 1199 | 29.1 | -0.320 | 0.6 | 386.2R | -0.34 / -0.26 | -0.32 / -0.32 | 0/5 ✗ | -0.40 | -0.47 | ✗  rsi_n 14→17: -0.38R | 1 | 0.14R | 4, +0.44 (-0.41 / +1.29) | 774 / 8 of 825 | 0 | avg -0.32R/trade (needs +0.10R); profit factor 0.60; max drawdown 386.2R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 2154 | 34.7 | -0.328 | 0.22 | 706.8R | -0.31 / -0.36 | -0.43 / -0.25 | 0/5 ✗ | -0.49 | -0.67 | ✗  hi 90→108: -0.43R | 0 | 0.28R | 80, -0.42 (-0.35 / -0.46) | 1205 / 52 of 1417 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.33R/trade (needs +0.10R); profit factor 0.22; max drawdown 706.8R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 573 | 41.9 | -0.356 | 0.5 | 206.9R | -0.35 / -0.36 | -0.34 / -0.36 | 0/5 ✗ | -0.51 | -0.65 | ✗  stop atr 1.5→1.2: -0.41R | 0 | 0.28R | 40, -0.71 (-0.70 / -0.76) | 101 / 29 of 184 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.36R/trade (needs +0.10R); profit factor 0.50; max drawdown 206.9R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 344 | 38.1 | -0.452 | 0.4 | 155.7R | -0.42 / -0.55 | -0.47 / -0.43 | 0/5 ✗ | -0.60 | -0.73 | ✗  stop atr 1.0→0.8: -0.51R | 0 | 0.26R | 16, -0.65 (-0.59 / -0.75) | 115 / 229 of 369 | 0 | not cost-viable: fees + slippage 0.26R per trade (stop must be ≥ 4x the round-trip cost); avg -0.45R/trade (needs +0.10R); profit factor 0.40; max drawdown 155.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 633 | 25.0 | -0.456 | 0.53 | 288.4R | -0.46 / -0.46 | -0.60 / -0.34 | 0/5 ✗ | -0.62 | -0.75 | ✗  n 20→24: -0.50R | 1 | 0.32R | 28, -0.11 (+0.48 / -0.70) | 479 / 1055 of 1722 | 0 | not cost-viable: fees + slippage 0.32R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.53; max drawdown 288.4R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 587 | 39.9 | -0.463 | 0.4 | 272.6R | -0.42 / -0.60 | -0.59 / -0.40 | 0/5 ✗ | -0.66 | -0.89 | ✗  stop atr 1.0→0.8: -0.53R | 0 | 0.37R | 40, -0.69 (-0.63 / -0.77) | 105 / 255 of 401 | 0 | not cost-viable: fees + slippage 0.37R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.40; max drawdown 272.6R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 122 | 20.5 | -0.495 | 0.49 | 61.9R | -0.43 / -0.62 | -0.63 / -0.36 | 0/5 ✗ | -0.63 | -0.77 | ✗  stop max_width_atr 3.0→2.4: -0.49R | 1 | 0.25R | 6, -0.04 (+0.51 / -0.32) | 30 / 107 of 151 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.49R/trade (needs +0.10R); profit factor 0.49; max drawdown 61.9R; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 279 | 30.5 | -0.704 | 0.26 | 196.3R | -0.82 / -0.55 | -0.66 / -0.95 | 0/5 ✗ | -1.05 | -1.39 | ✗  stop atr 1.5→1.2: -0.90R | 0 | 0.54R | 79, -0.48 (-0.47 / -0.50) | 201 / 58 of 341 | 0 | not cost-viable: fees + slippage 0.54R per trade (stop must be ≥ 4x the round-trip cost); avg -0.70R/trade (needs +0.10R); profit factor 0.26; max drawdown 196.3R; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 465 | 26.0 | -1.135 | 0.16 | 527.8R | -1.20 / -1.06 | -1.03 / -1.89 | 0/5 ✗ | -1.77 | -2.40 | ✗  stop atr 1.0→0.8: -1.46R | 0 | 0.98R | 150, -1.13 (-1.21 / -0.95) | 221 / 659 of 1035 | 0 | not cost-viable: fees + slippage 0.98R per trade (stop must be ≥ 4x the round-trip cost); avg -1.13R/trade (needs +0.10R); profit factor 0.16; max drawdown 527.8R; not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **25** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 118 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.34** (Bonferroni: family-wise false-winner rate 0.05 over 118 trials; with 1 trial it would be 1.65).

**Research run duration:** 10.7 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 25 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (114.6 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

**Rule significance:** in 34 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: none.

**Family gates (Phase 19 A, rules v1) - shadow mode: new verdicts are shown only.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

1 of 59 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **VALIDATION** | 4.09 | 16.5R | 705 d (22%) | multiple-testing bar: t-statistic 3.17 of the average trade, needs 3.34 after 118 trials |

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (80% of 3,250 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (76% of 1,522 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (81% of 1,183 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,864 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,294 trades shared)

- donchian_breakout-VEXIT-VRVOL v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 1,045 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,864 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,294 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 1,045 trades shared)

🧪 **Strategy lab:** 5 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S7-SILVER-BULLET | 15m | 5 | +1.221 | +2.214 | +0.236 | +0.561 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 6 | +0.206 | -1.323 | -0.126 | +0.049 | too few trades to compare |
| S8-PDH-PDL-SWEEP-5M | 30m | 2 | +0.037 | +0.037 | -0.665 | -0.603 | too few trades to compare |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.181 | -0.511 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 15m | 0 | +0.000 | +0.000 | -1.323 | -1.323 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | +2.214 | +0.000 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 5 | -1.187 | -1.163 | -0.334 | +0.138 | too few trades to compare |
| S8-PDH-PDL-SWEEP | 1h | 291 | -0.147 | -0.421 | -0.214 | -0.290 | no |
| S8-PDH-PDL-SWEEP | 30m | 122 | -0.495 | -0.621 | -0.456 | -0.458 | no |


### 3c. Research layers (daily run)
Last run: **2026-10-01 00:55 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 10 | 2017-08-17 | 2026-09-30 | 19975 |  |
| 1h | 10 | 2017-08-17 | 2026-09-30 | 79836 |  |
| 30m | 10 | 2024-10-01 | 2026-10-01 | 35039 | only 2.0 years - may miss a full bull/bear cycle |
| 15m | 10 | 2025-10-01 | 2026-10-01 | 35039 | only 1.0 years - may miss a full bull/bear cycle |
| 5m | 10 | 2026-07-03 | 2026-10-01 | 25919 | only 0.2 years - may miss a full bull/bear cycle |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 1045 (628) | no_displacement, false_breakout, trend_reversal | false_breakout 64%, no_displacement 33% | +0.48R | -0.37R | +0.25 / +0.19 |
| donchian_breakout-VEXIT-VRVOL | 4h | BACKTESTING | 1045 (628) | no_displacement, false_breakout, trend_reversal | false_breakout 64%, no_displacement 33% | +0.48R | -0.37R | +0.25 / +0.19 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 1183 (717) | no_displacement, false_breakout, trend_reversal | false_breakout 63%, no_displacement 34% | +0.47R | -0.36R | +0.25 / +0.19 |
| donchian_breakout | 4h | BACKTESTING | 1073 (492) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 66%, stop_too_tight 35%, no_displacement 33% | +0.35R | -0.37R | +0.16 / +0.11 |
| bb_squeeze_breakout | 4h | FAILED | 272 (131) | false_breakout, stop_too_tight, structural_change | false_breakout 58%, stop_too_tight 44% | +0.34R | -0.34R | +0.11 / +0.03 |
| macd_trend_cross | 1h | FAILED | 188 (91) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 92%, wrong_session 72%, indicator_lag 38%, stop_too_tight 31% | +0.32R | -0.42R | +0.14 / -0.01 |
| donchian_breakout-VEXIT | 30m | FAILED | 1294 (846) | false_breakout | false_breakout 72% | +0.47R | -0.39R | +0.13 / -0.02 |
| donchian_breakout-VEXIT-VRVOL | 30m | FAILED | 1294 (846) | false_breakout | false_breakout 72% | +0.47R | -0.39R | +0.13 / -0.02 |
| bb_squeeze_breakout | 1h | FAILED | 826 (396) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 62%, no_displacement 52%, stop_too_tight 37%, regime_mismatch 35% | +0.35R | -0.44R | +0.14 / -0.03 |
| macd_trend_cross | 4h | FAILED | 36 (17) | structural_change | regime_mismatch 94%, no_displacement 88%, low_relative_volume 59%, indicator_lag 59% | +0.17R | -0.45R | +0.05 / -0.03 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1522 (1000) | false_breakout | false_breakout 72% | +0.46R | -0.40R | +0.13 / -0.03 |
| donchian_breakout | 30m | FAILED | 1328 (671) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 75%, stop_too_tight 34% | +0.29R | -0.41R | +0.10 / -0.06 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 3250 (2203) | htf_conflict, no_displacement, false_breakout, regime_mismatch | false_breakout 64% | +0.50R | -0.39R | +0.05 / -0.06 |
| trend_pullback | 4h | FAILED | 1192 (607) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 39%, stop_too_tight 26% | +0.35R | -0.43R | +0.02 / -0.06 |
| donchian_breakout | 1h | FAILED | 2938 (1518) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 36%, stop_too_tight 32% | +0.37R | -0.40R | +0.05 / -0.06 |
| donchian_breakout-VEXIT | 1h | FAILED | 2864 (1950) | no_displacement, false_breakout | false_breakout 63% | +0.52R | -0.39R | +0.04 / -0.06 |
| donchian_breakout-VEXIT-VRVOL | 1h | FAILED | 2864 (1950) | no_displacement, false_breakout | false_breakout 63% | +0.52R | -0.39R | +0.04 / -0.06 |
| supertrend_flip | 4h | FAILED | 93 (50) | indicator_lag, structural_change | regime_mismatch 70%, indicator_lag 34% | +0.43R | -0.44R | -0.02 / -0.09 |
| R4-CLUC | 15m | FAILED | 90 (56) | none | - | +0.42R | -0.25R | +0.05 / -0.10 |
| rsi2_dip_buy | 4h | FAILED | 1781 (779) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 45% | +0.16R | -0.21R | -0.04 / -0.11 |
| ema_9_21_cross | 1h | FAILED | 341 (188) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 80%, indicator_lag 48%, stop_too_tight 25% | +0.26R | -0.39R | +0.03 / -0.12 |
| rsi2_dip_buy | 1h | FAILED | 6696 (3092) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 42% | +0.16R | -0.20R | +0.00 / -0.13 |
| trend_pullback | 1h | FAILED | 6104 (3194) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 76%, indicator_lag 44%, stop_too_tight 28% | +0.29R | -0.43R | +0.03 / -0.13 |
| supertrend_flip | 30m | FAILED | 167 (87) | stop_too_tight, indicator_lag | regime_mismatch 42%, indicator_lag 42%, stop_too_tight 38%, late_entry 30% | +0.29R | -0.46R | +0.03 / -0.14 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 291 (196) | stop_too_tight, sweep_continued | sweep_continued 97%, range_market 56%, stop_too_tight 31% | +0.54R | -0.39R | +0.10 / -0.15 |
| R4-CLUC | 30m | FAILED | 252 (156) | none | - | +0.36R | -0.46R | -0.06 / -0.17 |
| S6-OB-FVG-noSMC | 15m | FAILED | 44 (28) | structural_change | stop_too_wide 89% | +0.32R | -0.53R | +0.01 / -0.18 |
| supertrend_flip | 1h | FAILED | 271 (149) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 72%, regime_mismatch 68%, stop_too_tight 38%, indicator_lag 33% | +0.39R | -0.37R | -0.09 / -0.19 |
| ema_9_21_cross | 15m | FAILED | 464 (261) | htf_conflict, stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 28% | +0.26R | -0.42R | +0.11 / -0.19 |
| rsi2_dip_buy | 30m | FAILED | 2820 (1496) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 33% | +0.16R | -0.19R | +0.01 / -0.20 |
| trend_pullback | 30m | FAILED | 3540 (1915) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 31% | +0.28R | -0.43R | +0.03 / -0.20 |
| bb_squeeze_breakout | 30m | FAILED | 507 (273) | false_breakout, stop_too_tight | false_breakout 63%, stop_too_tight 40% | +0.27R | -0.43R | +0.05 / -0.20 |
| macd_trend_cross | 30m | FAILED | 302 (161) | stop_too_tight, indicator_lag | no_displacement 87%, indicator_lag 45%, low_relative_volume 44%, stop_too_tight 30% | +0.31R | -0.43R | +0.03 / -0.21 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 822 (572) | range_market, trend_reversal, stop_too_tight | range_market 46%, stop_too_tight 37% | +0.63R | -0.50R | +0.04 / -0.21 |
| liquidity_sweep_reversal | 1h | FAILED | 304 (162) | stop_too_tight | stop_too_tight 54% | +0.28R | -0.46R | -0.02 / -0.22 |
| ema_9_21_cross | 30m | FAILED | 352 (215) | stop_too_tight, indicator_lag | indicator_lag 46%, low_relative_volume 40%, stop_too_tight 26% | +0.26R | -0.37R | -0.04 / -0.25 |
| trend_pullback | 15m | FAILED | 3098 (1710) | wrong_session, stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 31% | +0.25R | -0.44R | +0.06 / -0.25 |
| R4-BBRSI | 30m | FAILED | 1520 (1035) | none | - | +0.43R | -0.44R | -0.05 / -0.30 |
| R4-BBRSI | 1h | FAILED | 1199 (850) | none | - | +0.45R | -0.45R | -0.15 / -0.32 |
| rsi2_dip_buy | 15m | FAILED | 2154 (1407) | wrong_session, trend_reversal, fees_slippage | fees_slippage 44% | +0.17R | -0.19R | +0.01 / -0.33 |
| bb_squeeze_breakout | 15m | FAILED | 573 (333) | stop_too_tight | no_displacement 58%, false_breakout 56%, stop_too_tight 43% | +0.31R | -0.46R | -0.01 / -0.36 |
| liquidity_sweep_reversal | 30m | FAILED | 344 (213) | stop_too_tight | stop_too_tight 39% | +0.39R | -0.47R | -0.14 / -0.45 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 633 (475) | stop_too_tight | stop_too_tight 32% | +0.59R | -0.49R | -0.06 / -0.46 |
| liquidity_sweep_reversal | 15m | FAILED | 587 (353) | stop_too_tight | stop_too_tight 38% | +0.37R | -0.47R | +0.00 / -0.46 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 122 (97) | trend_reversal, stop_too_tight, sweep_continued | sweep_continued 96%, stop_too_tight 28% | +0.50R | -0.65R | -0.16 / -0.49 |
| ema_9_21_cross | 5m | FAILED | 279 (194) | stop_too_tight, indicator_lag | indicator_lag 49%, stop_too_tight 30% | +0.26R | -0.44R | -0.01 / -0.70 |
| liquidity_sweep_reversal | 5m | FAILED | 465 (344) | htf_conflict, stop_too_tight | stop_too_tight 37% | +0.28R | -0.48R | +0.14 / -1.14 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `stop_too_tight` (systematic in 27 strategy/timeframe tests); `false_breakout` (systematic in 15 strategy/timeframe tests); `indicator_lag` (systematic in 13 strategy/timeframe tests); `regime_mismatch` (systematic in 12 strategy/timeframe tests); `trend_reversal` (systematic in 10 strategy/timeframe tests); `no_displacement` (systematic in 8 strategy/timeframe tests); `volatility_spike` (systematic in 3 strategy/timeframe tests); `htf_conflict` (systematic in 3 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests); `wrong_session` (systematic in 2 strategy/timeframe tests)

**Missed moves** (last 24h, ≥ 5x the 1H ATR within 12 hours; also in `memory/missed_trades.md`). Never change a rule just because a missed move became large:
- BTC up +2.7% (2026-09-30 06:00 → 2026-09-30 13:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move
- ENA up +12.9% (2026-09-30 06:00 → 2026-09-30 14:00 UTC): a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 104.8 KB | - | - |
| `memory/cleanup_log.md` | 0.5 KB | - | - |
| `memory/coin_notes.md` | 6.8 KB | 7 | 2026-09-27 00:26 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 6.0 KB | 13 | 2026-09-30 08:22 UTC |
| `memory/experiments.md` | 48.1 KB | 19 | 2026-09-28 15:40 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 99.5 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 11.9 KB | 13 | 2026-09-27 02:00 UTC |
| `memory/market_regime_log.md` | 9.6 KB | - | - |
| `memory/missed_trades.md` | 18.0 KB | 24 | 2026-10-01 00:55 UTC |
| `memory/playbook.md` | 8.7 KB | - | - |
| `memory/research_sources.md` | 59.7 KB | 45 | 2026-09-28 15:40 UTC |
| `memory/smc_events.csv` | 546.1 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 16.2 KB | - | - |
| `memory/strategy_registry.csv` | 36.7 KB | - | - |
| `memory/trials.csv` | 9.2 KB | - | - |
| `memory/universe_log.md` | 14.7 KB | - | - |

**Reviews due** (review date passed; for the reviews): none
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*