# Crypto Signal Report

**Updated:** 2026-10-11 09:55 Beijing time (2026-10-11 01:55 UTC) · data: Binance · 5 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

**Storage:** repository 16.8 MB (GitHub) · large files of this run 5.4 MB, published to branch `live-reports` (replaced every run, no history)

```
POSITION BOOK — 2026-10-11 01:55 UTC / 2026-10-11 09:55 Beijing
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
| MAGIC | **DEGRADED** | 1d: DEGRADED: volume 56x normal on candle 10-10 00:00 UTC (possible bad data) |
- 37 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

### 0b. Futures market data (funding, open interest, long/short, taker) - Phase 17 C
Checked 2026-10-11 01:55 UTC. History is saved every hour from now on (exchanges keep only ~30 days).

Every building block reads ONE series, the main source (OKX), in backtests and live; Binance is kept as a separate research series and never mixed in (their levels differ).

| Coin | State | Main source | Main history | Funding now | Long/short | Taker buy/sell | Problems |
|---|---|---|---|---|---|---|---|
| BTC | GOOD | okx | 1091 h since 2026-08-26 | -0.0022% | 1.47 | 0.61 | - |
| ETH | GOOD | okx | 1091 h since 2026-08-26 | -0.0044% | 1.89 | 0.77 | - |
| SOL | GOOD | okx | 1091 h since 2026-08-26 | +0.0075% | 2.40 | 0.93 | - |
| ZEC | GOOD | okx | 1091 h since 2026-08-26 | +0.0063% | 0.77 | 0.96 | - |
| XRP | GOOD | okx | 1091 h since 2026-08-26 | -0.0013% | 3.00 | 0.50 | - |
| SUI | GOOD | okx | 1091 h since 2026-08-26 | +0.0053% | 2.80 | 0.66 | - |

*Binance futures API: blocked from GitHub's servers (HTTP 451) - expected, not a problem. The main series (OKX) is complete; Binance research history comes from the data.binance.vision files.*

## 0b. Coins this run
- **Signal coins (5/7)** - only these can give signals: **BTC**, **ETH**, **SOL**, **ZEC**, **XRP**
- 2 empty slot(s): waiting for a coin to hold a top-7 rank for 2 runs in a row
- **Research only** - backtested, never a signal: none
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** MAGIC - 7-day average volume $15M < $50M; 24h move -26.2% is beyond ±25% - suspended for the rest of the UTC day; spread 0.103% > 0.1%; order book too thin: $17k within 1% (need $250k)
  - **LEAVE** SUI - not eligible: 24h volume below $50M or no longer listed

| Not eligible | 24h volume | Why |
|---|---|---|
| STRK | $84M | 7-day average volume $31M < $50M; 24h move +51.0% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $40k within 1% (need $250k) |
| MAGIC | $55M | 7-day average volume $15M < $50M; 24h move -26.2% is beyond ±25% - suspended for the rest of the UTC day; spread 0.103% > 0.1%; order book too thin: $17k within 1% (need $250k) |

**Flags (not excluded):** MAGIC: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* NEAR, USDC (see `config.yaml`)

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

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | up (HH/HL) | 83,173.3 / 82,778 | 0.27 | 0.53x | 0.41x | bear_engulf, bull_reject |
| ETH | mixed (HH/LL) | 2,519.51 / 2,474.34 | 0.03 | 1.44x | 0.46x | bull_reject |
| SOL | mixed (LH/HL) | 110.62 / 109.88 | 0.10 | 1.04x | 0.59x | bull_engulf, bear_engulf |
| ZEC | up (HH/HL) | 1,242.25 / 1,221.9 | 0.59 | 0.35x | 0.49x | bull_reject |
| XRP | mixed (LH/HL) | 1.4092 / 1.4025 | 0.03 | 1.06x | 0.49x | breakout_down |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
Patterns: candle patterns (displacement, engulfing, pin bar) and SMC events (smc_*: sweep of sell-side (bull) / buy-side (bear) liquidity, BOS, CHoCH with displacement, first retrace into a fair value gap).

If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 253 | 49% | 33% | 25% | 80% | 47% | 32% | can't tell from chance | 0.08R |
| 4h | displacement_down | 189 | 45% | 27% | 17% | 79% | 44% | 28% | can't tell from chance | 0.09R |
| 4h | bull_engulf | 632 | 45% | 30% | 21% | 77% | 48% | 32% | can't tell from chance | 0.09R |
| 4h | bear_engulf | 651 | 42% | 26% | 17% | 81% | 44% | 29% | can't tell from chance | 0.09R |
| 4h | bull_reject | 449 | 45% | 32% | 24% | 76% | 47% | 31% | can't tell from chance | 0.09R |
| 4h | bear_reject | 447 | 45% | 32% | 21% | 74% | 44% | 28% | can't tell from chance | 0.09R |
| 4h | smc_sweep_bull | 310 | 45% | 31% | 22% | 75% | 47% | 31% | can't tell from chance | 0.09R |
| 4h | smc_sweep_bear | 343 | 42% | 27% | 17% | 80% | 43% | 28% | can't tell from chance | 0.09R |
| 4h | smc_bos_up | 163 | 47% | 30% | 21% | 81% | 49% | 33% | can't tell from chance | 0.09R |
| 4h | smc_bos_down | 102 | 46% | 29% | 17% | 76% | 44% | 29% | can't tell from chance | 0.10R |
| 4h | smc_choch_up | 49 | 51% | 35% | 31% | 82% | 46% | 32% | can't tell from chance | 0.09R |
| 4h | smc_choch_down | 46 | 37% | 22% | 13% | 78% | 43% | 29% | can't tell from chance | 0.09R |
| 4h | smc_fvg_retrace_bull | 328 | 43% | 27% | 22% | 77% | 46% | 31% | can't tell from chance | 0.08R |
| 4h | smc_fvg_retrace_bear | 341 | 42% | 27% | 16% | 81% | 45% | 29% | can't tell from chance | 0.09R |
| 1h | displacement_up | 311 | 47% | 33% | 28% | 75% | 45% | 31% | can't tell from chance | 0.19R |
| 1h | displacement_down | 229 | 41% | 26% | 16% | 80% | 37% | 25% | can't tell from chance | 0.21R |
| 1h | bull_engulf | 881 | 40% | 29% | 21% | 76% | 44% | 30% | can't tell from chance | 0.21R |
| 1h | bear_engulf | 912 | 36% | 23% | 17% | 80% | 37% | 24% | can't tell from chance | 0.21R |
| 1h | bull_reject | 690 | 42% | 29% | 22% | 74% | 44% | 30% | can't tell from chance | 0.21R |
| 1h | bear_reject | 697 | 35% | 23% | 18% | 81% | 36% | 23% | can't tell from chance | 0.20R |
| 1h | smc_sweep_bull | 311 | 41% | 27% | 20% | 75% | 43% | 30% | can't tell from chance | 0.20R |
| 1h | smc_sweep_bear | 330 | 37% | 24% | 16% | 81% | 37% | 24% | can't tell from chance | 0.20R |
| 1h | smc_bos_up | 214 | 46% | 34% | 29% | 76% | 45% | 30% | can't tell from chance | 0.18R |
| 1h | smc_bos_down | 149 | 43% | 33% | 24% | 78% | 38% | 25% | can't tell from chance | 0.23R |
| 1h | smc_choch_up | 50 | 52% | 38% | 34% | 76% | 43% | 30% | can't tell from chance | 0.25R |
| 1h | smc_choch_down | 54 | 46% | 30% | 17% | 74% | 36% | 24% | can't tell from chance | 0.20R |
| 1h | smc_fvg_retrace_bull | 444 | 46% | 32% | 24% | 73% | 44% | 30% | can't tell from chance | 0.21R |
| 1h | smc_fvg_retrace_bear | 405 | 39% | 26% | 22% | 77% | 38% | 25% | can't tell from chance | 0.23R |
| 30m | displacement_up | 240 | 37% | 28% | 21% | 78% | 42% | 28% | can't tell from chance | 0.25R |
| 30m | displacement_down | 216 | 45% | 28% | 19% | 81% | 37% | 22% | beats chance | 0.26R |
| 30m | bull_engulf | 837 | 40% | 25% | 16% | 78% | 41% | 26% | can't tell from chance | 0.27R |
| 30m | bear_engulf | 884 | 37% | 22% | 16% | 81% | 35% | 22% | can't tell from chance | 0.28R |
| 30m | bull_reject | 632 | 44% | 27% | 19% | 75% | 42% | 27% | can't tell from chance | 0.28R |
| 30m | bear_reject | 751 | 36% | 22% | 17% | 79% | 36% | 22% | can't tell from chance | 0.27R |
| 30m | smc_sweep_bull | 339 | 40% | 27% | 18% | 78% | 43% | 27% | can't tell from chance | 0.26R |
| 30m | smc_sweep_bear | 317 | 39% | 25% | 17% | 81% | 35% | 22% | can't tell from chance | 0.26R |
| 30m | smc_bos_up | 197 | 35% | 26% | 23% | 79% | 41% | 26% | can't tell from chance | 0.28R |
| 30m | smc_bos_down | 148 | 36% | 22% | 14% | 85% | 37% | 22% | can't tell from chance | 0.26R |
| 30m | smc_choch_up | 49 | 35% | 20% | 14% | 88% | 39% | 25% | can't tell from chance | 0.32R |
| 30m | smc_choch_down | 50 | 38% | 22% | 20% | 78% | 36% | 24% | can't tell from chance | 0.26R |
| 30m | smc_fvg_retrace_bull | 455 | 39% | 24% | 17% | 80% | 41% | 27% | can't tell from chance | 0.28R |
| 30m | smc_fvg_retrace_bear | 422 | 40% | 24% | 17% | 79% | 36% | 22% | can't tell from chance | 0.27R |
| 15m | displacement_up | 223 | 29% | 18% | 13% | 90% | 36% | 25% | worse than chance | 0.36R |
| 15m | displacement_down | 220 | 35% | 26% | 19% | 81% | 33% | 21% | can't tell from chance | 0.36R |
| 15m | bull_engulf | 848 | 36% | 24% | 15% | 78% | 36% | 25% | can't tell from chance | 0.41R |
| 15m | bear_engulf | 833 | 29% | 21% | 14% | 80% | 31% | 20% | can't tell from chance | 0.41R |
| 15m | bull_reject | 681 | 37% | 26% | 17% | 79% | 36% | 25% | can't tell from chance | 0.42R |
| 15m | bear_reject | 743 | 28% | 17% | 11% | 84% | 32% | 21% | worse than chance | 0.38R |
| 15m | smc_sweep_bull | 290 | 39% | 28% | 19% | 77% | 36% | 24% | can't tell from chance | 0.35R |
| 15m | smc_sweep_bear | 273 | 33% | 21% | 11% | 85% | 33% | 21% | can't tell from chance | 0.36R |
| 15m | smc_bos_up | 169 | 27% | 21% | 16% | 85% | 35% | 24% | worse than chance | 0.44R |
| 15m | smc_bos_down | 165 | 28% | 20% | 15% | 84% | 30% | 19% | can't tell from chance | 0.41R |
| 15m | smc_choch_up | 50 | 20% | 10% | 0% | 98% | 37% | 26% | worse than chance | 0.49R |
| 15m | smc_choch_down | 51 | 41% | 29% | 14% | 78% | 31% | 21% | can't tell from chance | 0.38R |
| 15m | smc_fvg_retrace_bull | 568 | 36% | 26% | 18% | 78% | 36% | 25% | can't tell from chance | 0.41R |
| 15m | smc_fvg_retrace_bear | 456 | 32% | 23% | 15% | 80% | 32% | 21% | can't tell from chance | 0.40R |
| 5m | displacement_up | 555 | 24% | 15% | 12% | 88% | 26% | 17% | can't tell from chance | 0.82R |
| 5m | displacement_down | 595 | 25% | 19% | 14% | 85% | 24% | 16% | can't tell from chance | 0.70R |
| 5m | bull_engulf | 2171 | 25% | 16% | 11% | 85% | 25% | 17% | can't tell from chance | 0.80R |
| 5m | bear_engulf | 2154 | 24% | 17% | 13% | 84% | 24% | 17% | can't tell from chance | 0.81R |
| 5m | bull_reject | 1841 | 23% | 16% | 11% | 85% | 25% | 17% | worse than chance | 0.82R |
| 5m | bear_reject | 1930 | 24% | 16% | 11% | 85% | 24% | 17% | can't tell from chance | 0.83R |
| 5m | smc_sweep_bull | 589 | 28% | 19% | 13% | 81% | 25% | 17% | can't tell from chance | 0.68R |
| 5m | smc_sweep_bear | 602 | 26% | 20% | 12% | 85% | 26% | 18% | can't tell from chance | 0.71R |
| 5m | smc_bos_up | 402 | 21% | 15% | 13% | 88% | 25% | 17% | can't tell from chance | 0.92R |
| 5m | smc_bos_down | 460 | 21% | 15% | 11% | 88% | 24% | 17% | can't tell from chance | 0.76R |
| 5m | smc_choch_up | 109 | 24% | 16% | 14% | 85% | 23% | 15% | can't tell from chance | 0.91R |
| 5m | smc_choch_down | 110 | 28% | 19% | 12% | 86% | 23% | 16% | can't tell from chance | 0.76R |
| 5m | smc_fvg_retrace_bull | 1784 | 24% | 16% | 11% | 85% | 24% | 16% | can't tell from chance | 0.88R |
| 5m | smc_fvg_retrace_bear | 1623 | 22% | 15% | 10% | 85% | 23% | 16% | can't tell from chance | 0.86R |

## 0f. Market regime
The market's 'mood' per timeframe, from closed candles. Confidence = how much of the evidence agrees (strong / moderate / weak - never a %). **Permission:** LONG needs at least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W (weekly veto); SHORT is the mirror image. *Regimes now gate every strategy: each trades only in its allowed regimes and with timeframe permission (strategy spec v3).*

| Coin | 1W | 1D | 4H | 1H | Permission |
|---|---|---|---|---|---|
| **BTC** | TRANSITION (strong) | TRANSITION (weak) | TRANSITION (weak) | COMPRESSION (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H COMPRESSION)) |
| **ETH** | WEAK_BULL (weak) | TRANSITION (weak) | TRANSITION (weak) | RANGE (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H RANGE)) |
| **SOL** | WEAK_BULL (moderate) | TRANSITION (weak) | TRANSITION (weak) | COMPRESSION (moderate) | NO TRADE (timeframes disagree (1D TRANSITION, 4H TRANSITION, 1H COMPRESSION)) |
| **ZEC** | WEAK_BULL (weak) | TRANSITION (weak) | UNCLEAR (weak) | COMPRESSION (weak) | NO TRADE (timeframes disagree (1D TRANSITION, 4H UNCLEAR, 1H COMPRESSION)) |
| **XRP** | TRANSITION (weak) | WEAK_BULL (weak) | TRANSITION (moderate) | COMPRESSION (moderate) | NO TRADE (timeframes disagree (1D WEAK_BULL, 4H TRANSITION, 1H COMPRESSION)) |

**BTC evidence** (most coins follow BTC):
- **1W TRANSITION (strong)** - for: close above EMA-fast above EMA-slow; EMA-fast rising (+1.8 ATR in 10 candles); swing structure down (LH/LL); ADX 28 = strong trend; candle size 0.71x normal, Bollinger width above 62% of the last 100 candles · against: -
- **1D TRANSITION (weak)** - for: close above EMA-fast above EMA-slow; ADX 35 = strong trend; candle size 0.98x normal, Bollinger width above 21% of the last 100 candles · against: EMA-fast flat (+1.0 ATR in 10 candles); swing structure mixed
- **4H TRANSITION (weak)** - for: swing structure down (LH/LL); ADX 26 = strong trend; candle size 0.75x normal, Bollinger width above 30% of the last 100 candles · against: EMAs not lined up; EMA-fast flat (-0.6 ATR in 10 candles); ADX 26 is close to a threshold
- **1H COMPRESSION (moderate)** - for: EMAs not lined up; EMA-fast flat (+0.6 ATR in 10 candles); ADX 16 = weak trend / ranging; candle size 0.41x normal, Bollinger width above 0% of the last 100 candles · against: swing structure up (HH/HL)

*Full evidence for every coin: `reports/regime.json`. Daily history: `memory/market_regime_log.md`.*

## 0g. SMC now (Smart Money Concepts - hypotheses to test, not doctrine)
Killzone right now (New York time): **Asia**. Nothing trades on SMC yet; every detection is logged live in `memory/smc_events.csv` (signal coins, 4H/1H/30m/15m). Liquidity = where stop-losses likely sit. Discount = lower half of the 1H dealing range.

| Coin | 15m trend (last break) | Last 15m sweep | Newest open 15m gap (FVG) | 4H order block | 1H range position | Liquidity above (1H) | Liquidity below (1H) |
|---|---|---|---|---|---|---|---|
| **BTC** | up (BOS 32 candles ago) | sell-side (bullish idea) 11 candles ago | bull 82,995.13-83,012.68 | bear 85,550.00-86,378.24 | discount (48%) | swing high 83,173.29 (1.29 ATR) | swing low 82,778.00 (1.19 ATR) |
| **ETH** | up (BOS 26 candles ago) | sell-side (bullish idea) 2 candles ago | bull 2,507.13-2,508.74 | bear 2,690.78-2,700.54 | premium (67%) | PDH 2,519.51 (2.06 ATR) | PDL 2,486.03 (2.53 ATR) |
| **SOL** | up (BOS 45 candles ago) | buy-side (bearish idea) 49 candles ago | bull 110.00-110.10 | bear 120.13-121.29 | discount (4%) | swing high 110.62 (1.44 ATR) | swing low 109.88 (0.06 ATR) |
| **ZEC** | up (CHOCH 1 candles ago) | buy-side (bearish idea) 3 candles ago | bull 1,226.63-1,227.70 | bear 1,302.50-1,348.00 | discount (8%) | swing high 1,242.25 (2.04 ATR) | swing low 1,202.41 (2.29 ATR) |
| **XRP** | down (CHOCH 4 candles ago) | sell-side (bullish idea) 5 candles ago | bull 1.3994-1.4002 | bull 1.2202-1.3441 | below the range (-70%) | swing high 1.4092 (2.03 ATR) | PDL 1.3957 (0.37 ATR) |

*Full SMC state and the newest events per coin and timeframe: `reports/smc.json`. Definitions: `memory/smc_research.md`.*

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **SIDEWAYS**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 61 (Greed), yesterday 64  (extreme fear/greed = bigger, faster moves)

## 2. Signals right now
Only **APPROVED** strategy versions (your yes, after paper trading) give signals and emails.

**No trade passes all the checks right now. That is normal - no trade is also a position.**

### 2c. Watching - no signal yet (report only, never emailed)
No tracked strategy (VALIDATION or higher) has its market filters open right now.

### 2d. Risk engine (section 15 - independent of the strategies)
- **Live results:** today +0.00R (limit -3R), this week +0.00R (limit -6R) · **halts:** none
- **Suspended strategies** (live drawdown > 8R): none
- **Risk per trade:** 0.5% · leverage never above 3x (the position is made smaller instead)
- **Heat:** max 3 positions, 1 per coin, 1 per group of correlated coins and direction (1h correlation ≥ 0.7) · groups now: BTC+ETH+SOL+XRP
- **Every live entry also needs:** reward to TP1 ≥ 2R, no opposing level before TP1, no high-impact event within ±60 min, no duplicate
- **Event calendar (next 7 days):** US CPI (Sep data) 2026-10-14 12:30 UTC

## 3. Strategy scoreboard (after fees)
**Status and long-history numbers** come from the daily research run (last run 2026-10-11 00:58 UTC); **Layer A** (the last 15 days) is recalculated every hour. Only trades inside each strategy's allowed regimes and with timeframe permission are counted.

- **VALIDATION** = long history (Layer B): ≥ 30 trades, ≥ +0.10R per trade (+0.02R per re-tuned version), profit factor ≥ 1.2, max drawdown ≤ 10R, profitable in both the develop and the validate part, and cost-viable (fees + slippage ≤ 0.25R, i.e. stop ≥ 4x the round-trip cost).
- **PAPER_TRADING** (automatic) = VALIDATION + walk-forward (≥ 3 of 5 windows profitable and together profitable) + edge on ≥ 3 coins + still profitable with costs +50% + every ±20% change still profitable + no overfitting flag + beats its control twin. Paper signals are logged and get PAPER emails (practice only, at most 3 an hour).
- **BACKTESTING** = not good enough (yet) · **FAILED** = enough trades and losing · **RETIRED** = paper results broke the limits; only a new version can be tested again.

| Strategy | Ver | TF | Status | Trades | Win % | Avg R | PF | Max DD | Develop / validate R | Long / short R | Walk-fwd | Costs +50% | Costs +100% (shown only) | ±20% worst | Coins + | Cost/trade | Layer A: trades, R (days 1-10 / 11-15) | Stood down (regime / permission) | Paper+live signals | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PB-C-BREAKOUT-W20 | 1.0 | 5m | **BACKTESTING** | 1 | 100.0 | +0.351 | 99.0 | 0.0R | +0.35 / +0.00 | +0.35 / +0.00 | 0/5 ✗ | +0.30 | +0.25 | stable | 0 | 0.85R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | not cost-viable: fees + slippage 0.85R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; Monte Carlo 95% worst drawdown per 100 trades - - limit 17R; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 4h | **BACKTESTING** | 814 | 41.2 | +0.253 | 1.48 | 19.8R | +0.26 / +0.24 | +0.28 / +0.21 | 5/5 | +0.22 | +0.20 | stable | 7 | 0.04R | 1, -1.07 (-1.07 / +0.00) | 48 / 23 of 130 | 0 |  |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 926 | 40.4 | +0.242 | 1.45 | 18.6R | +0.25 / +0.22 | +0.26 / +0.23 | 5/5 | +0.21 | +0.19 | stable | 7 | 0.04R | 2, -1.05 (-1.05 / +0.00) | 78 / 31 of 174 | 0 | Monte Carlo 95% worst drawdown per 100 trades 17.4R - limit 17R |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 4h | **BACKTESTING** | 633 | 40.8 | +0.234 | 1.44 | 16.0R | +0.24 / +0.22 | +0.24 / +0.23 | 5/5 | +0.21 | +0.18 | stable | 6 | 0.04R | 1, -1.03 (-1.03 / +0.00) | 46 / 16 of 112 | 0 |  |
| P01-BREAKOUT-V3 🧪 lab | 1.0 | 4h | **BACKTESTING** | 333 | 40.5 | +0.209 | 1.39 | 12.9R | +0.21 / +0.21 | +0.34 / +0.01 | 4/5 | +0.18 | +0.16 | stable | 5 | 0.04R | 2, -1.05 (-1.05 / +0.00) | 20 / 28 of 63 | 0 | max drawdown 12.9R |
| P01-BREAKOUT-V1 🧪 lab | 1.0 | 4h | **BACKTESTING** | 1058 | 39.6 | +0.186 | 1.34 | 24.3R | +0.21 / +0.13 | +0.26 / +0.09 | 5/5 | +0.15 | +0.13 | stable | 5 | 0.04R | 3, -1.05 (-1.05 / -1.06) | 119 / 78 of 243 | 0 | max drawdown 24.3R |
| P01-BREAKOUT-V4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 900 | 39.6 | +0.184 | 1.29 | 24.7R | +0.23 / +0.09 | +0.24 / +0.11 | 5/5 | +0.15 | +0.12 | stable | 5 | 0.04R | 3, -1.05 (-1.05 / -1.06) | 119 / 78 of 243 | 0 | max drawdown 24.7R |
| donchian_breakout | 1.0 | 4h | **BACKTESTING** | 837 | 55.7 | +0.159 | 1.37 | 16.3R | +0.16 / +0.16 | +0.17 / +0.15 | 5/5 | +0.13 | +0.11 | stable | 6 | 0.04R | 2, -1.05 (-1.05 / +0.00) | 48 / 23 of 130 | 0 |  |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 15m | **BACKTESTING** | 2 | 50.0 | +0.130 | 1.21 | 1.2R | +0.13 / +0.00 | -1.22 / +1.47 | 0/5 ✗ | +0.02 | +0.00 | stable | 0 | 0.27R | 0, +0.00 (+0.00 / +0.00) | 24 / 6 of 33 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 2 trades; longest drawdown 59 days = 100% of the tested period (limit 60%); only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 1h | **BACKTESTING** | 821 | 38.2 | +0.109 | 1.17 | 46.2R | +0.03 / +0.26 | +0.17 / +0.04 | 4/5 | +0.09 | +0.07 | stable | 6 | 0.04R | 1, -1.04 (-1.04 / +0.00) | 6 / 2 of 63 | 0 | profit factor 1.17; recovery factor 1.93 (net +89.4R / max drawdown 46.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 23.2R - limit 17R |
| TRD-H4-BREAKOUT | 1.0 | 30m | **BACKTESTING** | 559 | 39.7 | +0.100 | 1.16 | 28.0R | -0.04 / +0.26 | +0.18 / +0.02 | 3/5 | +0.10 | +0.05 | stable | 6 | 0.06R | 1, +2.46 (+2.46 / +0.00) | 9 / 8 of 61 | 0 | profit factor 1.16; recovery factor 2.00 (net +56.0R / max drawdown 28.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 24.8R - limit 17R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V4 🧪 lab | 1.0 | 4h | **BACKTESTING** | 297 | 35.0 | +0.096 | 1.14 | 19.3R | +0.13 / +0.03 | +0.09 / +0.10 | 2/5 ✗ | +0.06 | +0.01 | ✗  rsi_hi 65→52: -0.04R | 4 | 0.06R | 1, -1.08 (-1.08 / +0.00) | 416 / 123 of 543 | 0 | avg +0.10R/trade (needs +0.10R); profit factor 1.14; max drawdown 19.3R |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 15m | **BACKTESTING** | 29 | 48.3 | +0.074 | 1.14 | 6.8R | +0.51 / -0.54 | +0.72 / -0.45 | 1/5 ✗ | +0.01 | -0.05 | ✗  stop max_width_atr 3.0→2.4: -0.09R | 3 | 0.17R | 0, +0.00 (+0.00 / +0.00) | 264 / 74 of 381 | 0 | only 29 trades; avg +0.07R/trade (needs +0.10R); profit factor 1.14; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 1h | **BACKTESTING** | 2641 | 36.8 | +0.029 | 1.04 | 77.2R | +0.01 / +0.06 | +0.09 / -0.05 | 4/5 | +0.01 | -0.03 | ✗  stop atr 2.0→1.6: -0.01R | 4 | 0.05R | 11, -0.44 (-0.73 / +2.47) | 91 / 269 of 511 | 0 | avg +0.03R/trade (needs +0.10R); profit factor 1.04; recovery factor 0.98 (net +75.5R / max drawdown 77.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 28.9R - limit 17R |
| bb_squeeze_breakout | 1.0 | 1h | **BACKTESTING** | 640 | 52.7 | +0.010 | 1.02 | 27.4R | +0.00 / +0.03 | -0.01 / +0.04 | 2/5 ✗ | -0.06 | -0.13 | ✗  bb_k 2→1: -0.04R | 3 | 0.12R | 4, +0.11 (+0.11 / +0.00) | 75 / 17 of 117 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.02; recovery factor 0.24 (net +6.5R / max drawdown 27.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 24.3R - limit 17R |
| P01-BREAKOUT-V2 🧪 lab | 1.0 | 30m | **BACKTESTING** | 873 | 36.2 | +0.005 | 1.01 | 56.0R | -0.06 / +0.08 | +0.04 / -0.04 | 1/5 ✗ | -0.07 | -0.14 | ✗  stop atr 2.0→1.6: -0.02R | 3 | 0.13R | 9, +0.29 (+0.18 / +0.51) | 162 / 83 of 305 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.01; max drawdown 56.0R; not profitable in BOTH train and unseen test |
| S6-OB-FVG | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 1 of 8 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S6-OB-FVG-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  ob_bars 20→16: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 7 / 1 of 8 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-5M | 1.0 | 15m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  sweep_bars 8→6: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 6 / 3 of 10 | 0 | only 0 trades; avg +0.00R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; recovery factor - (net +0.0R / max drawdown 0.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades - - limit 17R; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-BREAKOUT-noCVD | 1.0 | 5m | **BACKTESTING** | 0 | 0.0 | +0.000 | 0.0 | 0.0R | +0.00 / +0.00 | +0.00 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: +0.00R | 0 | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 0 trades; avg +0.00R/trade (needs +0.15R); profit factor 0.00; recovery factor - (net +0.0R / max drawdown 0.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades - - limit 17R; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET | 1.0 | 15m | **BACKTESTING** | 7 | 28.6 | -0.001 | 1.0 | 3.6R | +0.89 / -1.19 | +1.65 / -1.24 | 0/5 ✗ | -0.14 | -0.27 | ✗  sweep_bars 8→6: -0.59R | 0 | 0.33R | 0, +0.00 (+0.00 / +0.00) | 6 / 3 of 10 | 0 | not cost-viable: fees + slippage 0.33R per trade (stop must be ≥ 4x the round-trip cost); only 7 trades; avg -0.00R/trade (needs +0.10R); profit factor 1.00; longest drawdown 626 days = 69% of the tested period (limit 60%); only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 1h | **BACKTESTING** | 139 | 51.8 | -0.006 | 0.99 | 25.9R | -0.16 / +0.33 | -0.01 / -0.00 | 2/5 ✗ | -0.06 | -0.11 | ✗  stop atr 1.5→1.2: -0.07R | 3 | 0.11R | 0, +0.00 (+0.00 / +0.00) | 123 / 2 of 127 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; recovery factor -0.03 (net -0.8R / max drawdown 25.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 24.2R - limit 17R; longest drawdown 1862 days = 58% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 15m | **BACKTESTING** | 1950 | 38.1 | -0.006 | 0.99 | 121.2R | -0.07 / +0.12 | -0.07 / +0.06 | 2/5 ✗ | -0.04 | -0.06 | ✗  stop atr 2.0→1.6: -0.02R | 2 | 0.09R | 5, +0.32 (+0.32 / +0.00) | 14 / 12 of 96 | 0 | avg -0.01R/trade (needs +0.10R); profit factor 0.99; recovery factor -0.10 (net -12.6R / max drawdown 121.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 29.3R - limit 17R; longest drawdown 1818 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 30m | **BACKTESTING** | 1280 | 35.0 | -0.006 | 0.99 | 73.8R | -0.06 / +0.06 | +0.04 / -0.06 | 2/5 ✗ | -0.07 | -0.12 | ✗  stop atr 2.0→1.6: -0.03R | 2 | 0.10R | 7, +0.27 (+0.47 / +0.12) | 65 / 25 of 143 | 0 | avg -0.01R/trade (needs +0.12R); profit factor 0.99; recovery factor -0.10 (net -7.3R / max drawdown 73.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 29.2R - limit 17R; longest drawdown 1719 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 4h | **BACKTESTING** | 29 | 51.7 | -0.018 | 0.97 | 4.5R | +0.13 / -0.42 | +0.31 / -0.37 | 1/5 ✗ | -0.04 | -0.07 | ✗  time_stop_bars 40→32: -0.04R | 2 | 0.06R | 1, +0.31 (+0.31 / +0.00) | 78 / 0 of 79 | 0 | only 29 trades; avg -0.02R/trade (needs +0.10R); profit factor 0.97; recovery factor -0.11 (net -0.5R / max drawdown 4.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 24.9R - limit 17R; only 8 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-noSMC | 1.0 | 30m | **BACKTESTING** | 13 | 46.2 | -0.023 | 0.95 | 2.8R | +0.07 / -0.10 | -0.20 / +0.13 | 0/5 ✗ | -0.20 | -0.27 | ✗  stop buffer_atr 0.2→0.24: -0.13R | 0 | 0.12R | 0, +0.00 (+0.00 / +0.00) | 247 / 84 of 385 | 0 | only 13 trades; avg -0.02R/trade (needs +0.10R); profit factor 0.95; only 7 unseen-test trades; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 15m | **BACKTESTING** | 983 | 35.3 | -0.032 | 0.95 | 64.8R | -0.09 / +0.03 | -0.05 / -0.01 | 1/5 ✗ | -0.06 | -0.11 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.09R | 3, -1.11 (-1.11 / +0.00) | 4 / 4 of 24 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; recovery factor -0.49 (net -31.9R / max drawdown 64.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 34.6R - limit 17R; longest drawdown 1562 days = 87% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| PB-B-SWEEP-LIMIT | 1.0 | 5m | **BACKTESTING** | 215 | 39.1 | -0.129 | 0.73 | 33.8R | -0.17 / +0.04 | -0.18 / -0.08 | 1/5 ✗ | -0.28 | -0.25 | ✗  stop max_width_atr 3.0→3.6: -0.13R | 3 | 0.19R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 25 | 0 | avg -0.13R/trade (needs +0.15R); profit factor 0.73; max drawdown 33.8R; longest drawdown 684 days = 96% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 5m | **BACKTESTING** | 183 | 36.6 | -0.137 | 0.72 | 29.9R | -0.17 / -0.00 | -0.19 / -0.08 | 1/5 ✗ | -0.24 | -0.15 | ✗  stop max_width_atr 3.0→3.6: -0.14R | 2 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 23 | 0 | avg -0.14R/trade (needs +0.15R); profit factor 0.72; max drawdown 29.9R; longest drawdown 684 days = 96% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| S7-SILVER-BULLET-noSMC | 1.0 | 15m | **BACKTESTING** | 21 | 38.1 | -0.138 | 0.83 | 7.9R | -0.11 / -0.16 | +1.42 / -0.76 | 2/5 ✗ | -0.96 | -0.79 | ✗  stop buffer_atr 0.2→0.24: -0.54R | 0 | 0.28R | 0, +0.00 (+0.00 / +0.00) | 22 / 5 of 28 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); only 21 trades; avg -0.14R/trade (needs +0.10R); profit factor 0.83; longest drawdown 1566 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| PB-B-APLUS | 1.0 | 15m | **BACKTESTING** | 79 | 45.6 | -0.142 | 0.74 | 17.8R | -0.26 / -0.07 | -0.11 / -0.17 | 1/5 ✗ | -0.25 | -0.31 | ✗  stop buffer_atr 0.0→0.0: -0.14R | 2 | 0.17R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 11 | 0 | only 79 trades; avg -0.14R/trade (needs +0.15R); profit factor 0.74; max drawdown 17.8R; longest drawdown 673 days = 95% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-5M | 1.0 | 30m | **BACKTESTING** | 5 | 40.0 | -0.172 | 0.79 | 2.6R | +1.21 / -0.52 | -0.30 / +0.03 | 0/5 ✗ | -0.37 | -0.49 | ✗  stop buffer_atr 0.2→0.24: -0.43R | 0 | 0.34R | 0, +0.00 (+0.00 / +0.00) | 20 / 55 of 78 | 0 | not cost-viable: fees + slippage 0.34R per trade (stop must be ≥ 4x the round-trip cost); only 5 trades; avg -0.17R/trade (needs +0.10R); profit factor 0.79; longest drawdown 318 days = 100% of the tested period (limit 60%); only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-GRADED | 1.0 | 5m | **BACKTESTING** | 65 | 41.5 | -0.253 | 0.59 | 16.9R | -0.21 / -0.47 | -0.24 / -0.26 | 1/5 ✗ | -0.43 | -0.43 | ✗  time_stop_bars 48→38: -0.28R | 1 | 0.18R | 1, +1.53 (+0.00 / +1.53) | 0 / 0 of 1 | 0 | only 65 trades; avg -0.25R/trade (needs +0.15R); profit factor 0.59; recovery factor -0.97 (net -16.5R / max drawdown 16.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 42.6R - limit 17R; longest drawdown 705 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| PB-A-APLUS | 1.0 | 5m | **BACKTESTING** | 53 | 37.7 | -0.308 | 0.53 | 16.8R | -0.27 / -0.50 | -0.19 / -0.38 | 0/5 ✗ | -0.39 | -0.46 | ✗  time_stop_bars 48→38: -0.34R | 1 | 0.18R | 1, +1.53 (+0.00 / +1.53) | 0 / 0 of 1 | 0 | only 53 trades; avg -0.31R/trade (needs +0.15R); profit factor 0.53; recovery factor -0.97 (net -16.3R / max drawdown 16.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 48.9R - limit 17R; longest drawdown 705 days = 100% of the tested period (limit 55%); only 9 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-GRADED | 1.0 | 5m | **BACKTESTING** | 8 | 37.5 | -0.336 | 0.49 | 4.4R | -0.22 / -1.15 | -0.60 / +0.47 | 0/5 ✗ | +0.32 | +0.21 | ✗  stop buffer_atr 0.0→0.0: -0.34R | 0 | 0.20R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 1 | 0 | only 8 trades; avg -0.34R/trade (needs +0.15R); profit factor 0.49; recovery factor -0.61 (net -2.7R / max drawdown 4.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 52.9R - limit 17R; longest drawdown 664 days = 100% of the tested period (limit 55%); only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-B-SWEEP-noCVD | 1.0 | 5m | **BACKTESTING** | 19 | 42.1 | -0.375 | 0.46 | 7.5R | +0.00 / -0.38 | -0.48 / -0.23 | 0/5 ✗ | -0.33 | -0.20 | ✗  stop max_width_atr 3.0→2.4: -0.38R | 0 | 0.53R | 6, -0.46 (-0.46 / +0.00) | 0 / 0 of 25 | 0 | not cost-viable: fees + slippage 0.53R per trade (stop must be ≥ 4x the round-trip cost); only 19 trades; avg -0.37R/trade (needs +0.15R); profit factor 0.46; longest drawdown 34 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-LDN | 1.0 | 5m | **BACKTESTING** | 21 | 42.9 | -0.461 | 0.34 | 11.5R | -0.44 / -0.56 | -0.50 / -0.44 | 0/5 ✗ | -0.57 | -0.67 | ✗  stop buffer_atr 0.0→0.0: -0.46R | 1 | 0.25R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 21 trades; avg -0.46R/trade (needs +0.15R); profit factor 0.34; recovery factor -0.84 (net -9.7R / max drawdown 11.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 61.9R - limit 17R; longest drawdown 601 days = 100% of the tested period (limit 55%); only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK | 1.0 | 5m | **BACKTESTING** | 12 | 41.7 | -0.497 | 0.28 | 6.7R | -0.44 / -1.10 | -0.62 / -0.46 | 0/5 ✗ | -0.69 | -0.44 | ✗  stop buffer_atr 0.0→0.0: -0.50R | 0 | 0.19R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 12 trades; avg -0.50R/trade (needs +0.15R); profit factor 0.28; recovery factor -0.89 (net -6.0R / max drawdown 6.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 64.1R - limit 17R; longest drawdown 468 days = 100% of the tested period (limit 55%); only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-A-PULLBACK-CVD | 1.0 | 5m | **BACKTESTING** | 10 | 40.0 | -0.520 | 0.26 | 6.0R | -0.46 / -1.10 | -1.16 / -0.36 | 0/5 ✗ | -0.69 | -0.44 | ✗  stop buffer_atr 0.0→0.0: -0.52R | 0 | 0.18R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 10 trades; avg -0.52R/trade (needs +0.15R); profit factor 0.26; recovery factor -0.87 (net -5.2R / max drawdown 6.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 65.1R - limit 17R; longest drawdown 468 days = 100% of the tested period (limit 55%); only 1 unseen-test trades; not profitable in BOTH train and unseen test |
| PB-C-APLUS | 1.0 | 5m | **BACKTESTING** | 1 | 0.0 | -0.641 | 0.0 | 0.6R | -0.64 / +0.00 | -0.64 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.0→0.0: -0.64R | 0 | 0.23R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | only 1 trades; avg -0.64R/trade (needs +0.15R); profit factor 0.00; recovery factor -1.00 (net -0.6R / max drawdown 0.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades - - limit 17R; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 30m | **BACKTESTING** | 9 | 11.1 | -0.653 | 0.38 | 5.9R | -0.24 / -1.17 | -1.22 / -0.37 | 0/5 ✗ | -0.67 | -0.75 | ✗  sweep_bars 20→24: -0.73R | 0 | 0.24R | 0, +0.00 (+0.00 / +0.00) | 32 / 10 of 43 | 0 | only 9 trades; avg -0.65R/trade (needs +0.10R); profit factor 0.38; longest drawdown 916 days = 100% of the tested period (limit 60%); only 4 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG | 1.0 | 15m | **BACKTESTING** | 12 | 25.0 | -0.839 | 0.34 | 10.1R | -0.25 / -2.60 | -0.88 / -0.79 | 0/5 ✗ | -0.96 | -1.31 | ✗  stop buffer_atr 0.2→0.16: -3.30R | 0 | 0.34R | 0, +0.00 (+0.00 / +0.00) | 24 / 6 of 33 | 0 | not cost-viable: fees + slippage 0.34R per trade (stop must be ≥ 4x the round-trip cost); only 12 trades; avg -0.84R/trade (needs +0.10R); profit factor 0.34; max drawdown 10.1R; longest drawdown 1063 days = 100% of the tested period (limit 60%); only 3 unseen-test trades; not profitable in BOTH train and unseen test |
| S5-SWEEP-MSS-FVG-5M | 1.0 | 30m | **BACKTESTING** | 1 | 0.0 | -1.208 | 0.0 | 1.2R | -1.21 / +0.00 | -1.21 / +0.00 | 0/5 ✗ | +0.00 | +0.00 | ✗  stop buffer_atr 0.2→0.16: -1.21R | 0 | 0.27R | 0, +0.00 (+0.00 / +0.00) | 32 / 10 of 43 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); only 1 trades; avg -1.21R/trade (needs +0.10R); profit factor 0.00; only 0 unseen-test trades; not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | 150 | 38.7 | +0.195 | 1.33 | 10.7R | +0.30 / +0.00 | +0.30 / +0.04 | 3/5 | +0.17 | +0.15 | stable | 6 | 0.04R | 2, -1.09 (-1.09 / +0.00) | 27 / 8 of 40 | 0 | recovery factor 2.73 (net +29.2R / max drawdown 10.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 19.5R - limit 17R |
| P02-EMA-PULLBACK-V4-S6 🧪 lab | 1.0 | 4h | **FORMALIZED** | 365 | 35.9 | +0.145 | 1.21 | 19.9R | +0.11 / +0.21 | +0.19 / +0.09 | 4/5 | +0.11 | +0.06 | stable | 4 | 0.06R | 1, -1.08 (-1.08 / +0.00) | 431 / 128 of 566 | 0 | recovery factor 2.66 (net +52.9R / max drawdown 19.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 27.1R - limit 17R |
| P04-MACD-SUPERTREND-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | 372 | 37.4 | +0.134 | 1.21 | 32.9R | +0.28 / -0.20 | +0.28 / -0.04 | 4/5 | +0.10 | +0.07 | stable | 5 | 0.04R | 2, -1.09 (-1.09 / +0.00) | 118 / 22 of 151 | 0 | recovery factor 1.52 (net +50.0R / max drawdown 32.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 25.8R - limit 17R; not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | 383 | 36.0 | +0.113 | 1.18 | 33.7R | +0.24 / -0.19 | +0.19 / +0.02 | 4/5 | +0.09 | +0.06 | stable | 5 | 0.04R | 2, -1.09 (-1.09 / +0.00) | 118 / 22 of 151 | 0 | profit factor 1.18; recovery factor 1.28 (net +43.3R / max drawdown 33.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 23.3R - limit 17R; not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | 250 | 31.2 | -0.025 | 0.97 | 47.3R | +0.05 / -0.15 | +0.04 / -0.07 | 2/5 ✗ | -0.06 | -0.11 | ✗  stop max_width_atr 3.0→2.4: -0.05R | 2 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 281 / 131 of 418 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; recovery factor -0.13 (net -6.2R / max drawdown 47.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 36.3R - limit 17R; longest drawdown 2013 days = 62% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | 1199 | 33.4 | -0.033 | 0.95 | 92.4R | -0.05 / +0.01 | -0.08 / +0.03 | 2/5 ✗ | -0.07 | -0.12 | ✗  st_n 10→8: -0.04R | 3 | 0.08R | 1, +2.44 (+0.00 / +2.44) | 137 / 30 of 188 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.95; recovery factor -0.42 (net -39.2R / max drawdown 92.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 33.4R - limit 17R; longest drawdown 2003 days = 61% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | 1450 | 34.8 | -0.036 | 0.95 | 115.8R | -0.08 / +0.07 | -0.03 / -0.04 | 2/5 ✗ | -0.11 | -0.18 | ✗  stop atr 2.0→1.6: -0.07R | 2 | 0.12R | 4, +0.54 (+0.54 / +0.00) | 134 / 52 of 216 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.95; recovery factor -0.45 (net -52.1R / max drawdown 115.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.9R - limit 17R; longest drawdown 1797 days = 99% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | 2287 | 34.1 | -0.079 | 0.89 | 216.7R | -0.11 / -0.01 | -0.13 / -0.02 | 1/5 ✗ | -0.17 | -0.27 | ✗  stop atr 2.0→1.6: -0.15R | 0 | 0.17R | 9, -0.11 (-0.33 / +0.66) | 156 / 53 of 227 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.89; recovery factor -0.83 (net -180.9R / max drawdown 216.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 38.4R - limit 17R; longest drawdown 1829 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | 253 | 34.8 | -0.083 | 0.88 | 41.5R | -0.07 / -0.10 | -0.18 / -0.01 | 2/5 ✗ | -0.11 | -0.15 | ✗  stop max_width_atr 3.0→2.4: -0.12R | 2 | 0.06R | 0, +0.00 (+0.00 / +0.00) | 281 / 131 of 418 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.88; recovery factor -0.50 (net -20.9R / max drawdown 41.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 35.6R - limit 17R; not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | 2388 | 34.5 | -0.089 | 0.87 | 215.2R | -0.08 / -0.11 | -0.10 / -0.07 | 1/5 ✗ | -0.14 | -0.21 | ✗  stop buffer_atr 0.2→0.16: -0.09R | 0 | 0.11R | 6, -0.94 (-1.15 / -0.51) | 408 / 93 of 576 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.87; recovery factor -0.99 (net -212.0R / max drawdown 215.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 37.4R - limit 17R; longest drawdown 3264 days = 99% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V5 🧪 lab | 1.0 | 1h | **FORMALIZED** | 2387 | 31.7 | -0.100 | 0.86 | 273.4R | -0.12 / -0.06 | -0.14 / -0.06 | 1/5 ✗ | -0.15 | -0.19 | ✗  stop atr 2.0→1.6: -0.12R | 1 | 0.08R | 8, +0.08 (-0.47 / +0.41) | 137 / 2 of 188 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.86; recovery factor -0.87 (net -238.2R / max drawdown 273.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 38.2R - limit 17R; longest drawdown 2130 days = 64% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | 3360 | 32.9 | -0.106 | 0.85 | 417.3R | -0.15 / +0.00 | -0.16 / -0.06 | 1/5 ✗ | -0.19 | -0.27 | ✗  stop atr 2.0→1.6: -0.14R | 2 | 0.13R | 18, +0.54 (+0.14 / +0.85) | 134 / 14 of 216 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.85; recovery factor -0.85 (net -356.4R / max drawdown 417.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 38.2R - limit 17R; longest drawdown 1794 days = 98% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V5 🧪 lab | 1.0 | 1h | **FORMALIZED** | 5109 | 33.6 | -0.122 | 0.83 | 638.9R | -0.12 / -0.12 | -0.14 / -0.10 | 0/5 ✗ | -0.18 | -0.26 | ✗  stop buffer_atr 0.2→0.16: -0.13R | 2 | 0.12R | 21, -0.17 (-0.79 / +1.07) | 408 / 17 of 576 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.83; recovery factor -0.98 (net -623.5R / max drawdown 638.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 40.4R - limit 17R; longest drawdown 3056 days = 92% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P04-MACD-SUPERTREND-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | 5024 | 32.9 | -0.135 | 0.82 | 715.3R | -0.17 / -0.07 | -0.19 / -0.08 | 1/5 ✗ | -0.24 | -0.35 | ✗  stop atr 2.0→1.6: -0.19R | 0 | 0.19R | 27, +0.23 (-0.35 / +0.77) | 156 / 21 of 227 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.82; recovery factor -0.95 (net -676.7R / max drawdown 715.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 42.0R - limit 17R; longest drawdown 1829 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | 2812 | 34.6 | -0.143 | 0.8 | 414.7R | -0.17 / -0.09 | -0.18 / -0.11 | 0/5 ✗ | -0.25 | -0.33 | ✗  stop max_width_atr 3.0→2.4: -0.15R | 0 | 0.18R | 11, -0.97 (-0.91 / -1.27) | 428 / 143 of 658 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.80; recovery factor -0.97 (net -403.5R / max drawdown 414.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 40.4R - limit 17R; longest drawdown 1825 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | 87 | 31.0 | -0.145 | 0.8 | 16.1R | -0.14 / -0.16 | -0.44 / +0.09 | 1/5 ✗ | -0.18 | -0.23 | ✗  stop max_width_atr 3.0→2.4: -0.21R | 2 | 0.05R | 0, +0.00 (+0.00 / +0.00) | 64 / 44 of 110 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.80; recovery factor -0.78 (net -12.6R / max drawdown 16.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 40.8R - limit 17R; longest drawdown 2120 days = 69% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | 6226 | 33.5 | -0.188 | 0.75 | 1175.3R | -0.21 / -0.14 | -0.23 / -0.15 | 0/5 ✗ | -0.29 | -0.39 | ✗  stop max_width_atr 3.0→2.4: -0.19R | 0 | 0.20R | 30, -0.30 (-0.76 / +0.77) | 428 / 41 of 658 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.75; recovery factor -1.00 (net -1169.7R / max drawdown 1175.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 46.0R - limit 17R; longest drawdown 1826 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | 4763 | 33.6 | -0.234 | 0.7 | 1161.6R | -0.26 / -0.19 | -0.25 / -0.22 | 0/5 ✗ | -0.36 | -0.49 | ✗  stop max_width_atr 3.0→2.4: -0.25R | 0 | 0.25R | 20, -0.52 (-0.55 / -0.43) | 451 / 147 of 667 | 0 | not cost-viable: fees + slippage 0.25R per trade (stop must be ≥ 4x the round-trip cost); avg -0.23R/trade (needs +0.10R); profit factor 0.70; recovery factor -0.96 (net -1112.5R / max drawdown 1161.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 49.9R - limit 17R; longest drawdown 1830 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P03-FIB-PULLBACK-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | 10470 | 32.6 | -0.277 | 0.66 | 2912.8R | -0.28 / -0.26 | -0.30 / -0.26 | 0/5 ✗ | -0.41 | -0.55 | ✗  stop buffer_atr 0.2→0.16: -0.29R | 0 | 0.28R | 57, -0.20 (-0.58 / +0.28) | 451 / 51 of 667 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.28R/trade (needs +0.10R); profit factor 0.66; recovery factor -1.00 (net -2901.2R / max drawdown 2912.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 52.7R - limit 17R; longest drawdown 1830 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P05-RANGE-REVERSAL-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -0.11 (-0.11 / +0.00) | 214 / 0 of 238 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 10, +0.22 (+0.29 / -0.09) | 269 / 0 of 301 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 45, -0.26 (-0.24 / -0.31) | 239 / 1 of 315 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 96, -0.35 (-0.43 / -0.08) | 171 / 1 of 284 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -0.11 (-0.11 / +0.00) | 27 / 0 of 36 | 0 | waiting for the first daily research run (Layers B/C) |
| P05-RANGE-REVERSAL-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.06 (-1.06 / +0.00) | 214 / 0 of 238 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 132 / 0 of 132 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 11, +0.55 (+0.79 / -0.52) | 238 / 1 of 261 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 54, -0.24 (-0.35 / +0.61) | 237 / 4 of 319 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | waiting for the first daily research run (Layers B/C) |
| P06-VWAP-REVERSION-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.05 (-1.03 / -1.07) | 121 / 48 of 185 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 3, +1.57 (+1.15 / +2.43) | 145 / 38 of 209 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 8, +0.06 (+0.26 / -0.14) | 144 / 51 of 217 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 11, -0.57 (-0.81 / +0.08) | 173 / 51 of 239 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.03 (-1.03 / +0.00) | 16 / 19 of 43 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.05 (-1.03 / -1.07) | 121 / 48 of 185 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V1 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, +0.59 (-1.24 / +2.42) | 212 / 43 of 286 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 3, -0.04 (-1.35 / +0.62) | 128 / 42 of 187 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 6, -0.58 (-1.03 / +0.29) | 79 / 20 of 106 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V3 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.24 (-1.24 / +0.00) | 61 / 11 of 81 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V4 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, +0.49 (-1.24 / +2.22) | 212 / 43 of 286 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 34 / 9 of 43 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.07 (-1.07 / +0.00) | 25 / 15 of 41 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.10 (-1.11 / -1.10) | 33 / 16 of 51 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, +0.86 (+0.86 / +0.00) | 30 / 7 of 38 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 6 / 0 of 6 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 34 / 9 of 43 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V1 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 5 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V2 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 6 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V2 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.10 (-1.10 / +0.00) | 0 / 0 of 10 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V2 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 0 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V3 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 5 | 0 | waiting for the first daily research run (Layers B/C) |
| P10-CROWDING-FADE-V4 🧪 lab | 1.0 | 4h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 5 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V5 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 7, +0.34 (-0.23 / +1.79) | 145 / 19 of 209 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 17, +0.12 (-0.05 / +0.22) | 144 / 29 of 217 | 0 | waiting for the first daily research run (Layers B/C) |
| P07-SQUEEZE-RETEST-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 26, -0.43 (-0.84 / -0.02) | 173 / 33 of 239 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 12, -0.10 (-1.21 / +0.27) | 128 / 21 of 187 | 0 | waiting for the first daily research run (Layers B/C) |
| P08-SESSION-BREAKOUT-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 14, -0.22 (-1.08 / +0.43) | 79 / 10 of 106 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V5 🧪 lab | 1.0 | 1h | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, -1.07 (-1.07 / +0.00) | 25 / 15 of 41 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V5 🧪 lab | 1.0 | 30m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 2, -1.10 (-1.11 / -1.10) | 33 / 14 of 51 | 0 | waiting for the first daily research run (Layers B/C) |
| P09-SWEEP-MSS-V5 🧪 lab | 1.0 | 15m | **FORMALIZED** | - | - | - | - | - | - / - | - / - | - | - | - | - | - | - | 1, +0.86 (+0.86 / +0.00) | 30 / 7 of 38 | 0 | waiting for the first daily research run (Layers B/C) |
| bb_squeeze_breakout | 1.0 | 4h | **FAILED** | 215 | 52.1 | +0.036 | 1.07 | 26.8R | +0.22 / -0.35 | +0.16 / -0.08 | 2/5 ✗ | -0.01 | -0.05 | ✗  stop atr 1.5→1.8: -0.00R | 4 | 0.07R | 1, -1.04 (-1.04 / +0.00) | 63 / 14 of 84 | 0 | avg +0.04R/trade (needs +0.10R); profit factor 1.07; recovery factor 0.29 (net +7.7R / max drawdown 26.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 21.6R - limit 17R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 1h | **FAILED** | 803 | 37.4 | +0.015 | 1.03 | 44.3R | +0.03 / -0.02 | -0.04 / +0.08 | 3/5 | -0.01 | -0.04 | ✗  stop atr 2.0→1.6: -0.01R | 3 | 0.04R | 0, +0.00 (+0.00 / +0.00) | 19 / 20 of 124 | 0 | avg +0.01R/trade (needs +0.10R); profit factor 1.03; recovery factor 0.27 (net +12.0R / max drawdown 44.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 26.3R - limit 17R; longest drawdown 1994 days = 61% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.1 | 1h | **FAILED** | 1795 | 32.8 | -0.010 | 0.98 | 98.1R | -0.04 / +0.05 | +0.03 / -0.05 | 2/5 ✗ | -0.05 | -0.09 | ✗  stop atr 2.0→1.6: -0.03R | 3 | 0.07R | 4, +0.82 (+0.95 / +0.68) | 72 / 41 of 192 | 0 | avg -0.01R/trade (needs +0.12R); profit factor 0.98; recovery factor -0.18 (net -18.0R / max drawdown 98.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 30.1R - limit 17R; longest drawdown 2004 days = 62% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 1h | **FAILED** | 3699 | 37.6 | -0.017 | 0.97 | 178.5R | +0.00 / -0.06 | -0.03 / -0.00 | 1/5 ✗ | -0.05 | -0.08 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.05R | 13, +0.02 (+0.02 / +0.00) | 351 / 1369 of 1970 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; recovery factor -0.35 (net -63.0R / max drawdown 178.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 29.4R - limit 17R; longest drawdown 1856 days = 56% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 1h | **FAILED** | 2241 | 32.6 | -0.019 | 0.97 | 125.2R | -0.04 / +0.03 | +0.01 / -0.06 | 2/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.05R | 4 | 0.07R | 6, -0.12 (-0.51 / +0.68) | 60 / 42 of 189 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.97; recovery factor -0.35 (net -43.3R / max drawdown 125.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.0R - limit 17R; not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 1h | **FAILED** | 2554 | 32.7 | -0.019 | 0.97 | 141.1R | -0.04 / +0.02 | +0.02 / -0.07 | 2/5 ✗ | -0.07 | -0.11 | ✗  stop atr 2.0→1.6: -0.04R | 3 | 0.08R | 9, -0.07 (-0.28 / +0.68) | 120 / 60 of 294 | 0 | avg -0.02R/trade (needs +0.12R); profit factor 0.97; recovery factor -0.34 (net -48.6R / max drawdown 141.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 29.6R - limit 17R; longest drawdown 2004 days = 61% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V2 🧪 lab | 1.0 | 1h | **FAILED** | 1849 | 32.3 | -0.023 | 0.96 | 100.0R | -0.06 / +0.06 | +0.02 / -0.08 | 1/5 ✗ | -0.06 | -0.10 | ✗  stop atr 2.0→1.6: -0.04R | 2 | 0.07R | 5, +0.08 (-0.32 / +0.68) | 168 / 80 of 335 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 100.0R; not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V5 🧪 lab | 1.0 | 1h | **FAILED** | 3762 | 33.0 | -0.023 | 0.96 | 226.0R | -0.04 / +0.02 | -0.01 / -0.03 | 1/5 ✗ | -0.07 | -0.12 | ✗  stop atr 2.0→1.6: -0.05R | 2 | 0.08R | 12, +0.16 (-0.51 / +0.49) | 168 / 38 of 335 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 226.0R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V1 🧪 lab | 1.0 | 4h | **FAILED** | 299 | 31.4 | -0.024 | 0.96 | 23.4R | +0.03 / -0.13 | -0.03 / -0.02 | 2/5 ✗ | -0.06 | -0.09 | ✗  rsi_hi 65→52: -0.39R | 2 | 0.06R | 1, -1.08 (-1.08 / +0.00) | 416 / 123 of 543 | 0 | avg -0.02R/trade (needs +0.10R); profit factor 0.96; max drawdown 23.4R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 5m | **FAILED** | 2179 | 38.1 | -0.027 | 0.96 | 178.6R | -0.05 / +0.05 | -0.05 / +0.00 | 2/5 ✗ | -0.03 | -0.10 | ✗  stop atr 2.0→2.4: -0.04R | 1 | 0.13R | 13, -0.32 (-0.32 / +0.00) | 17 / 13 of 116 | 0 | avg -0.03R/trade (needs +0.10R); profit factor 0.96; recovery factor -0.33 (net -59.8R / max drawdown 178.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.2R - limit 17R; longest drawdown 679 days = 94% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 30m | **FAILED** | 1939 | 35.8 | -0.035 | 0.95 | 143.0R | -0.09 / +0.03 | -0.04 / -0.03 | 1/5 ✗ | -0.07 | -0.10 | ✗  stop atr 2.0→1.6: -0.04R | 1 | 0.07R | 14, -0.07 (-0.13 / +0.13) | 63 / 263 of 443 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.95; recovery factor -0.48 (net -68.7R / max drawdown 143.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 35.2R - limit 17R; longest drawdown 1614 days = 89% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 1h | **FAILED** | 2301 | 48.2 | -0.036 | 0.93 | 110.5R | -0.04 / -0.03 | -0.02 / -0.06 | 1/5 ✗ | -0.08 | -0.12 | ✗  adx_min 20→24: -0.05R | 2 | 0.07R | 6, -0.02 (-0.23 / +0.38) | 60 / 42 of 189 | 0 | avg -0.04R/trade (needs +0.10R); profit factor 0.93; recovery factor -0.75 (net -83.3R / max drawdown 110.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 25.5R - limit 17R; longest drawdown 3167 days = 96% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK | 1.0 | 30m | **FAILED** | 1053 | 35.7 | -0.051 | 0.92 | 109.1R | -0.12 / +0.07 | -0.10 / -0.00 | 1/5 ✗ | -0.07 | -0.10 | ✗  entry offset_atr 0.25→0.3: -0.07R | 2 | 0.06R | 1, +2.46 (+2.46 / +0.00) | 21 / 21 of 146 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; recovery factor -0.49 (net -53.8R / max drawdown 109.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 31.2R - limit 17R; longest drawdown 1808 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT-S4 🧪 lab | 1.0 | 30m | **FAILED** | 1778 | 33.8 | -0.052 | 0.92 | 144.8R | -0.10 / +0.02 | -0.03 / -0.07 | 1/5 ✗ | -0.12 | -0.19 | ✗  stop atr 2.0→1.6: -0.08R | 1 | 0.12R | 16, +0.11 (+0.11 / +0.12) | 103 / 46 of 234 | 0 | avg -0.05R/trade (needs +0.12R); profit factor 0.92; recovery factor -0.64 (net -92.1R / max drawdown 144.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 33.2R - limit 17R; longest drawdown 1719 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| donchian_breakout-VEXIT 🧪 lab | 1.0 | 30m | **FAILED** | 1500 | 33.4 | -0.054 | 0.92 | 140.1R | -0.12 / +0.02 | -0.03 / -0.08 | 1/5 ✗ | -0.12 | -0.18 | ✗  stop atr 2.0→1.6: -0.08R | 2 | 0.12R | 12, -0.09 (-0.29 / +0.51) | 63 / 35 of 169 | 0 | avg -0.05R/trade (needs +0.10R); profit factor 0.92; recovery factor -0.58 (net -81.1R / max drawdown 140.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 34.6R - limit 17R; longest drawdown 1722 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V2 🧪 lab | 1.0 | 15m | **FAILED** | 1330 | 34.4 | -0.057 | 0.91 | 116.0R | -0.10 / -0.01 | -0.06 / -0.05 | 1/5 ✗ | -0.15 | -0.26 | ✗  stop atr 2.0→1.6: -0.10R | 2 | 0.18R | 15, -0.26 (-0.46 / +0.29) | 171 / 82 of 284 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.91; max drawdown 116.0R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 1h | **FAILED** | 229 | 35.4 | -0.058 | 0.92 | 35.9R | +0.04 / -0.28 | -0.23 / +0.16 | 1/5 ✗ | -0.14 | -0.24 | ✗  time_stop_bars 30→36: -0.08R | 3 | 0.16R | 1, +2.18 (+2.18 / +0.00) | 46 / 106 of 159 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.92; max drawdown 35.9R; longest drawdown 2498 days = 82% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| donchian_breakout | 1.0 | 30m | **FAILED** | 1553 | 48.2 | -0.065 | 0.88 | 132.7R | -0.09 / -0.03 | -0.06 / -0.07 | 0/5 ✗ | -0.13 | -0.20 | ✗  stop atr 2.0→1.6: -0.10R | 1 | 0.11R | 12, -0.21 (-0.46 / +0.54) | 63 / 35 of 169 | 0 | avg -0.06R/trade (needs +0.10R); profit factor 0.88; recovery factor -0.76 (net -100.8R / max drawdown 132.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 28.8R - limit 17R; longest drawdown 1722 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT | 1.0 | 5m | **FAILED** | 1363 | 36.6 | -0.068 | 0.9 | 111.1R | -0.08 / -0.02 | -0.01 / -0.13 | 2/5 ✗ | -0.15 | -0.19 | ✗  stop atr 2.0→1.6: -0.09R | 3 | 0.13R | 7, +0.42 (+0.42 / +0.00) | 1 / 3 of 30 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.90; recovery factor -0.84 (net -92.9R / max drawdown 111.1R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 35.0R - limit 17R; longest drawdown 713 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 4h | **FAILED** | 934 | 48.1 | -0.073 | 0.87 | 103.8R | -0.02 / -0.18 | -0.01 / -0.15 | 1/5 ✗ | -0.11 | -0.14 | ✗  long_rsi_hi 65→52: -0.15R | 1 | 0.05R | 6, -0.02 (-0.02 / +0.00) | 340 / 93 of 533 | 0 | avg -0.07R/trade (needs +0.10R); profit factor 0.87; recovery factor -0.65 (net -67.7R / max drawdown 103.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 29.0R - limit 17R; longest drawdown 1978 days = 60% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 4h | **FAILED** | 70 | 45.7 | -0.076 | 0.86 | 10.9R | +0.08 / -0.29 | -0.13 / +0.00 | 4/5 ✗ | -0.12 | -0.14 | ✗  time_stop_bars 60→48: -0.07R | 1 | 0.04R | 1, -1.14 (-1.14 / +0.00) | 19 / 3 of 25 | 0 | avg -0.08R/trade (needs +0.10R); profit factor 0.86; recovery factor -0.49 (net -5.3R / max drawdown 10.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 29.2R - limit 17R; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 15m | **FAILED** | 3341 | 34.2 | -0.086 | 0.88 | 326.2R | -0.11 / -0.05 | -0.09 / -0.09 | 0/5 ✗ | -0.13 | -0.18 | ✗  stop atr 2.0→1.6: -0.11R | 1 | 0.10R | 29, -0.53 (-0.56 / -0.43) | 59 / 303 of 448 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.88; recovery factor -0.88 (net -286.9R / max drawdown 326.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 37.2R - limit 17R; longest drawdown 1562 days = 86% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 15m | **FAILED** | 7330 | 36.2 | -0.089 | 0.87 | 701.9R | -0.11 / -0.04 | -0.11 / -0.07 | 0/5 ✗ | -0.13 | -0.14 | ✗  stop atr 2.0→1.6: -0.09R | 0 | 0.10R | 39, -0.30 (-0.29 / -0.35) | 273 / 1477 of 2032 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.87; recovery factor -0.93 (net -650.2R / max drawdown 701.9R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 36.2R - limit 17R; longest drawdown 1830 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V2 🧪 lab | 1.0 | 1h | **FAILED** | 2302 | 31.1 | -0.090 | 0.86 | 236.6R | -0.09 / -0.10 | -0.11 / -0.07 | 0/5 ✗ | -0.15 | -0.21 | ✗  stop atr 1.5→1.2: -0.11R | 0 | 0.11R | 7, -1.04 (-1.07 / -0.83) | 593 / 72 of 727 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.86; max drawdown 236.6R; not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V5 🧪 lab | 1.0 | 30m | **FAILED** | 1938 | 32.9 | -0.095 | 0.86 | 207.3R | -0.11 / -0.07 | -0.11 / -0.08 | 1/5 ✗ | -0.19 | -0.26 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.15R | 21, -0.04 (-0.38 / +0.26) | 162 / 40 of 305 | 0 | avg -0.09R/trade (needs +0.10R); profit factor 0.86; max drawdown 207.3R; not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 30m | **FAILED** | 4260 | 34.3 | -0.098 | 0.86 | 431.3R | -0.12 / -0.04 | -0.11 / -0.09 | 0/5 ✗ | -0.14 | -0.17 | ✗  stop atr 2.0→1.6: -0.12R | 1 | 0.07R | 26, -0.20 (-0.00 / -1.04) | 259 / 1370 of 1925 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.86; recovery factor -0.97 (net -418.5R / max drawdown 431.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 37.3R - limit 17R; longest drawdown 1815 days = 99% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 4h | **FAILED** | 1421 | 56.8 | -0.104 | 0.64 | 147.8R | -0.10 / -0.12 | -0.12 / -0.09 | 0/5 ✗ | -0.13 | -0.16 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.05R | 6, -0.49 (+0.06 / -1.05) | 388 / 6 of 535 | 0 | avg -0.10R/trade (needs +0.10R); profit factor 0.64; max drawdown 147.8R; longest drawdown 3278 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| TRD-H4-PULLBACK-noT4 | 1.0 | 5m | **FAILED** | 6309 | 36.5 | -0.107 | 0.85 | 697.5R | -0.12 / -0.07 | -0.10 / -0.11 | 0/5 ✗ | -0.13 | -0.16 | ✗  stop atr 2.0→2.4: -0.12R | 0 | 0.15R | 45, -0.39 (-0.42 / -0.28) | 667 / 3959 of 5289 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.85; recovery factor -0.97 (net -676.6R / max drawdown 697.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 36.9R - limit 17R; longest drawdown 724 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V5 🧪 lab | 1.0 | 1h | **FAILED** | 4852 | 30.1 | -0.110 | 0.83 | 569.3R | -0.11 / -0.11 | -0.12 / -0.10 | 0/5 ✗ | -0.18 | -0.24 | ✗  stop atr 1.5→1.2: -0.14R | 0 | 0.12R | 14, -0.92 (-0.91 / -0.95) | 593 / 14 of 727 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.83; max drawdown 569.3R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 1h | **FAILED** | 5256 | 55.4 | -0.114 | 0.59 | 604.8R | -0.09 / -0.17 | -0.10 / -0.13 | 0/5 ✗ | -0.17 | -0.23 | ✗  stop atr 2.0→1.6: -0.14R | 0 | 0.10R | 16, +0.01 (-0.06 / +0.09) | 531 / 7 of 711 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.59; max drawdown 604.8R; longest drawdown 3154 days = 95% of the tested period (limit 60%); loss clustering: 21 losses in a row as it happened, random orders stay at or below 13 in 95% of cases; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 1h | **FAILED** | 608 | 32.7 | -0.115 | 0.85 | 101.3R | -0.15 / -0.06 | -0.16 / -0.07 | 1/5 ✗ | -0.20 | -0.29 | ✗  stop buffer_atr 0.2→0.16: -0.17R | 1 | 0.19R | 3, +0.76 (+0.51 / +1.25) | 234 / 560 of 841 | 0 | avg -0.11R/trade (needs +0.10R); profit factor 0.85; max drawdown 101.3R; longest drawdown 2713 days = 87% of the tested period (limit 60%); loss clustering: 21 losses in a row as it happened, random orders stay at or below 20 in 95% of cases; not profitable in BOTH train and unseen test |
| TRD-H4-BREAKOUT-noT4 | 1.0 | 5m | **FAILED** | 3770 | 35.2 | -0.119 | 0.84 | 463.3R | -0.13 / -0.08 | -0.09 / -0.15 | 0/5 ✗ | -0.16 | -0.20 | ✗  stop atr 2.0→1.6: -0.13R | 0 | 0.15R | 28, -0.29 (-0.10 / -0.69) | 146 / 872 of 1209 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.84; recovery factor -0.97 (net -450.2R / max drawdown 463.3R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 40.4R - limit 17R; longest drawdown 728 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 1h | **FAILED** | 4792 | 46.8 | -0.120 | 0.79 | 587.6R | -0.13 / -0.11 | -0.11 / -0.13 | 0/5 ✗ | -0.18 | -0.24 | ✗  stop atr 1.5→1.2: -0.14R | 0 | 0.11R | 19, -0.26 (+0.13 / -1.12) | 588 / 117 of 904 | 0 | avg -0.12R/trade (needs +0.10R); profit factor 0.79; recovery factor -0.98 (net -576.2R / max drawdown 587.6R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 33.6R - limit 17R; longest drawdown 3090 days = 94% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 1h | **FAILED** | 270 | 43.3 | -0.128 | 0.77 | 42.7R | -0.14 / -0.11 | -0.18 / -0.07 | 0/5 ✗ | -0.18 | -0.25 | ✗  slow 21→17: -0.19R | 2 | 0.11R | 2, -1.03 (-1.18 / -0.88) | 60 / 5 of 69 | 0 | avg -0.13R/trade (needs +0.10R); profit factor 0.77; recovery factor -0.81 (net -34.5R / max drawdown 42.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 32.9R - limit 17R; longest drawdown 2361 days = 72% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V2 🧪 lab | 1.0 | 30m | **FAILED** | 1692 | 30.3 | -0.136 | 0.8 | 236.7R | -0.14 / -0.13 | -0.12 / -0.15 | 0/5 ✗ | -0.24 | -0.34 | ✗  rsi_hi 65→52: -0.30R | 0 | 0.19R | 14, -0.57 (-0.36 / -0.93) | 536 / 109 of 738 | 0 | avg -0.14R/trade (needs +0.10R); profit factor 0.80; max drawdown 236.7R; not profitable in BOTH train and unseen test |
| S6-OB-FVG-noSMC | 1.0 | 15m | **FAILED** | 95 | 33.7 | -0.147 | 0.77 | 21.4R | -0.25 / +0.01 | -0.19 / -0.05 | 2/5 ✗ | -0.23 | -0.24 | ✗  stop buffer_atr 0.2→0.16: -0.18R | 2 | 0.13R | 2, -0.78 (-1.18 / -0.39) | 68 / 18 of 93 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.77; max drawdown 21.4R; longest drawdown 1625 days = 90% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 30m | **FAILED** | 240 | 37.9 | -0.148 | 0.78 | 54.6R | -0.10 / -0.22 | +0.10 / -0.39 | 1/5 ✗ | -0.20 | -0.26 | ✗  depth 0.985→1.182: -0.25R | 1 | 0.10R | 1, -1.07 (+0.00 / -1.07) | 31 / 3 of 35 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.78; max drawdown 54.6R; longest drawdown 1600 days = 90% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P01-BREAKOUT-V5 🧪 lab | 1.0 | 15m | **FAILED** | 2971 | 31.6 | -0.149 | 0.79 | 461.9R | -0.16 / -0.14 | -0.18 / -0.12 | 0/5 ✗ | -0.26 | -0.38 | ✗  stop atr 2.0→1.6: -0.22R | 0 | 0.20R | 33, -0.20 (-0.74 / +0.37) | 171 / 47 of 284 | 0 | avg -0.15R/trade (needs +0.10R); profit factor 0.79; max drawdown 461.9R; not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 5m | **FAILED** | 901 | 36.5 | -0.153 | 0.66 | 143.8R | -0.20 / +0.01 | -0.20 / -0.11 | 1/5 ✗ | -0.20 | -0.21 | ✗  stop max_width_atr 3.0→3.6: -0.16R | 0 | 0.18R | 1, +0.46 (+0.46 / +0.00) | 0 / 0 of 202 | 0 | avg -0.15R/trade (needs +0.15R); profit factor 0.66; max drawdown 143.8R; longest drawdown 687 days = 96% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 1h | **FAILED** | 243 | 47.7 | -0.158 | 0.73 | 40.8R | -0.17 / -0.12 | -0.14 / -0.20 | 0/5 ✗ | -0.22 | -0.28 | ✗  vol_x 1.2→1.44: -0.32R | 2 | 0.14R | 1, +1.11 (+1.11 / +0.00) | 45 / 93 of 144 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.73; max drawdown 40.8R; longest drawdown 3227 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V5 🧪 lab | 1.0 | 30m | **FAILED** | 3703 | 30.0 | -0.163 | 0.77 | 602.5R | -0.16 / -0.17 | -0.19 / -0.13 | 0/5 ✗ | -0.28 | -0.40 | ✗  rsi_hi 65→52: -0.26R | 0 | 0.22R | 35, -0.28 (-0.45 / +0.03) | 536 / 28 of 738 | 0 | avg -0.16R/trade (needs +0.10R); profit factor 0.77; max drawdown 602.5R; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 30m | **FAILED** | 657 | 47.5 | -0.165 | 0.73 | 112.7R | -0.19 / -0.13 | -0.18 / -0.15 | 0/5 ✗ | -0.28 | -0.40 | ✗  stop atr 1.5→1.2: -0.23R | 1 | 0.19R | 9, -0.14 (+0.07 / -0.87) | 48 / 19 of 98 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.73; recovery factor -0.96 (net -108.5R / max drawdown 112.7R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 37.5R - limit 17R; longest drawdown 1815 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| PB-B-GRADED | 1.0 | 15m | **FAILED** | 821 | 39.7 | -0.169 | 0.69 | 146.5R | -0.17 / -0.17 | -0.13 / -0.21 | 0/5 ✗ | -0.19 | -0.13 | ✗  stop max_width_atr 3.0→2.4: -0.17R | 0 | 0.17R | 0, +0.00 (+0.00 / +0.00) | 0 / 0 of 128 | 0 | avg -0.17R/trade (needs +0.15R); profit factor 0.69; max drawdown 146.5R; longest drawdown 1808 days = 99% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 30m | **FAILED** | 4642 | 48.5 | -0.173 | 0.44 | 804.2R | -0.16 / -0.21 | -0.17 / -0.17 | 0/5 ✗ | -0.26 | -0.35 | ✗  stop atr 2.0→1.6: -0.22R | 0 | 0.15R | 29, -0.16 (-0.23 / -0.04) | 587 / 22 of 701 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.44; max drawdown 804.2R; longest drawdown 1827 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 30m | **FAILED** | 240 | 45.0 | -0.174 | 0.71 | 50.0R | -0.20 / -0.13 | -0.31 / -0.07 | 1/5 ✗ | -0.22 | -0.28 | ✗  adx_min 20→16: -0.24R | 1 | 0.12R | 2, -0.03 (-0.03 / +0.00) | 27 / 2 of 34 | 0 | avg -0.17R/trade (needs +0.10R); profit factor 0.71; recovery factor -0.84 (net -41.8R / max drawdown 50.0R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 38.2R - limit 17R; longest drawdown 1691 days = 93% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 30m | **FAILED** | 5648 | 46.2 | -0.179 | 0.7 | 1011.4R | -0.20 / -0.14 | -0.19 / -0.16 | 0/5 ✗ | -0.27 | -0.37 | ✗  stop atr 1.5→1.2: -0.23R | 0 | 0.17R | 36, -0.53 (-0.38 / -1.16) | 416 / 145 of 836 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.70; recovery factor -1.00 (net -1011.4R / max drawdown 1011.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 39.0R - limit 17R; longest drawdown 1826 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| macd_trend_cross | 1.0 | 30m | **FAILED** | 441 | 48.1 | -0.180 | 0.7 | 82.4R | -0.14 / -0.25 | -0.24 / -0.13 | 0/5 ✗ | -0.26 | -0.36 | ✗  stop atr 1.5→1.2: -0.20R | 0 | 0.18R | 5, -0.91 (-0.76 / -1.14) | 98 / 6 of 113 | 0 | avg -0.18R/trade (needs +0.10R); profit factor 0.70; recovery factor -0.96 (net -79.4R / max drawdown 82.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 39.1R - limit 17R; longest drawdown 1719 days = 94% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 30m | **FAILED** | 557 | 41.7 | -0.185 | 0.68 | 110.5R | -0.23 / -0.09 | -0.24 / -0.15 | 0/5 ✗ | -0.27 | -0.34 | ✗  slow 21→25: -0.29R | 0 | 0.16R | 6, -1.16 (-1.16 / -1.17) | 52 / 17 of 81 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.68; recovery factor -0.93 (net -103.1R / max drawdown 110.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 37.8R - limit 17R; longest drawdown 1723 days = 95% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| R4-CLUC 🧪 lab | 1.0 | 15m | **FAILED** | 199 | 34.7 | -0.190 | 0.73 | 41.8R | -0.14 / -0.28 | -0.05 / -0.32 | 2/5 ✗ | -0.24 | -0.28 | ✗  depth 0.985→1.182: -0.36R | 1 | 0.11R | 3, -0.80 (-0.20 / -1.09) | 8 / 2 of 13 | 0 | avg -0.19R/trade (needs +0.10R); profit factor 0.73; max drawdown 41.8R; not profitable in BOTH train and unseen test |
| supertrend_flip | 1.0 | 1h | **FAILED** | 209 | 45.0 | -0.208 | 0.64 | 47.4R | -0.21 / -0.20 | -0.27 / -0.15 | 0/5 ✗ | -0.26 | -0.32 | ✗  st_n 10→12: -0.24R | 2 | 0.08R | 1, +0.24 (+0.24 / +0.00) | 27 / 0 of 32 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.64; recovery factor -0.92 (net -43.5R / max drawdown 47.4R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 39.6R - limit 17R; longest drawdown 3105 days = 97% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 15m | **FAILED** | 1534 | 42.4 | -0.210 | 0.65 | 324.5R | -0.24 / -0.13 | -0.24 / -0.18 | 0/5 ✗ | -0.33 | -0.46 | ✗  stop atr 1.5→1.2: -0.30R | 0 | 0.23R | 8, -0.90 (-1.00 / -0.73) | 52 / 10 of 70 | 0 | avg -0.21R/trade (needs +0.10R); profit factor 0.65; recovery factor -0.99 (net -322.2R / max drawdown 324.5R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 40.9R - limit 17R; longest drawdown 1829 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V2 🧪 lab | 1.0 | 15m | **FAILED** | 3121 | 28.5 | -0.214 | 0.7 | 693.9R | -0.19 / -0.25 | -0.23 / -0.18 | 0/5 ✗ | -0.37 | -0.52 | ✗  stop atr 1.5→1.2: -0.27R | 0 | 0.28R | 23, -0.69 (-0.62 / -0.95) | 532 / 148 of 737 | 0 | not cost-viable: fees + slippage 0.28R per trade (stop must be ≥ 4x the round-trip cost); avg -0.21R/trade (needs +0.10R); profit factor 0.70; max drawdown 693.9R; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1.0 | 15m | **FAILED** | 7420 | 39.9 | -0.240 | 0.3 | 1782.9R | -0.21 / -0.30 | -0.25 / -0.23 | 0/5 ✗ | -0.38 | -0.52 | ✗  stop atr 2.0→1.6: -0.31R | 0 | 0.23R | 70, -0.40 (-0.40 / -0.41) | 589 / 25 of 721 | 0 | avg -0.24R/trade (needs +0.10R); profit factor 0.30; max drawdown 1782.9R; longest drawdown 1828 days = 100% of the tested period (limit 60%); loss clustering: 24 losses in a row as it happened, random orders stay at or below 21 in 95% of cases; not profitable in BOTH train and unseen test |
| trend_pullback | 1.0 | 15m | **FAILED** | 9637 | 44.8 | -0.248 | 0.62 | 2387.8R | -0.25 / -0.24 | -0.27 / -0.22 | 0/5 ✗ | -0.38 | -0.52 | ✗  stop atr 1.5→1.2: -0.32R | 0 | 0.24R | 51, -0.71 (-0.68 / -0.86) | 802 / 147 of 1180 | 0 | avg -0.25R/trade (needs +0.10R); profit factor 0.62; recovery factor -1.00 (net -2387.8R / max drawdown 2387.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 45.1R - limit 17R; longest drawdown 1830 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V3 🧪 lab | 1.0 | 4h | **FAILED** | 117 | 23.1 | -0.261 | 0.62 | 30.9R | -0.24 / -0.30 | -0.25 / -0.29 | 0/5 ✗ | -0.29 | -0.33 | ✗  fast 20→24: -0.31R | 1 | 0.06R | 1, -1.08 (-1.08 / +0.00) | 117 / 57 of 177 | 0 | avg -0.26R/trade (needs +0.10R); profit factor 0.62; max drawdown 30.9R; not profitable in BOTH train and unseen test |
| P02-EMA-PULLBACK-V5 🧪 lab | 1.0 | 15m | **FAILED** | 6894 | 27.9 | -0.263 | 0.65 | 1817.7R | -0.23 / -0.31 | -0.30 / -0.22 | 0/5 ✗ | -0.44 | -0.61 | ✗  stop atr 1.5→1.2: -0.33R | 0 | 0.31R | 69, -0.36 (-0.59 / +0.02) | 532 / 51 of 737 | 0 | not cost-viable: fees + slippage 0.31R per trade (stop must be ≥ 4x the round-trip cost); avg -0.26R/trade (needs +0.10R); profit factor 0.65; max drawdown 1817.7R; not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP | 1.0 | 30m | **FAILED** | 200 | 28.0 | -0.269 | 0.69 | 56.0R | -0.19 / -0.42 | -0.45 / +0.01 | 0/5 ✗ | -0.38 | -0.48 | ✗  time_stop_bars 30→24: -0.32R | 1 | 0.23R | 0, +0.00 (+0.00 / +0.00) | 20 / 55 of 78 | 0 | avg -0.27R/trade (needs +0.10R); profit factor 0.69; max drawdown 56.0R; longest drawdown 1816 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 1h | **FAILED** | 991 | 29.4 | -0.296 | 0.62 | 294.2R | -0.32 / -0.24 | -0.25 / -0.33 | 0/5 ✗ | -0.37 | -0.43 | ✗  rsi_n 14→17: -0.41R | 1 | 0.13R | 6, -0.34 (+0.48 / -1.17) | 373 / 3 of 402 | 0 | avg -0.30R/trade (needs +0.10R); profit factor 0.62; max drawdown 294.2R; longest drawdown 3312 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 1.0 | 15m | **FAILED** | 1409 | 43.1 | -0.307 | 0.56 | 435.2R | -0.30 / -0.32 | -0.32 / -0.29 | 0/5 ✗ | -0.45 | -0.58 | ✗  stop atr 1.5→1.2: -0.38R | 0 | 0.27R | 8, -1.21 (-1.43 / -0.57) | 48 / 20 of 81 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.31R/trade (needs +0.10R); profit factor 0.56; recovery factor -1.00 (net -433.1R / max drawdown 435.2R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 50.4R - limit 17R; longest drawdown 1815 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| R4-BBRSI 🧪 lab | 1.0 | 30m | **FAILED** | 2699 | 30.6 | -0.315 | 0.6 | 850.6R | -0.32 / -0.30 | -0.33 / -0.30 | 0/5 ✗ | -0.42 | -0.53 | ✗  bb_k 2→3: -0.36R | 0 | 0.19R | 19, -0.32 (+0.22 / -1.25) | 304 / 14 of 364 | 0 | avg -0.31R/trade (needs +0.10R); profit factor 0.60; max drawdown 850.6R; longest drawdown 1826 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| S8-PDH-PDL-SWEEP-noSMC | 1.0 | 30m | **FAILED** | 862 | 28.3 | -0.364 | 0.59 | 321.5R | -0.28 / -0.53 | -0.45 / -0.27 | 0/5 ✗ | -0.49 | -0.60 | ✗  stop buffer_atr 0.2→0.16: -0.39R | 0 | 0.27R | 7, +0.13 (-0.17 / +1.92) | 268 / 562 of 908 | 0 | not cost-viable: fees + slippage 0.27R per trade (stop must be ≥ 4x the round-trip cost); avg -0.36R/trade (needs +0.10R); profit factor 0.59; max drawdown 321.5R; longest drawdown 1573 days = 86% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 30m | **FAILED** | 394 | 41.1 | -0.393 | 0.45 | 159.8R | -0.39 / -0.40 | -0.41 / -0.37 | 1/5 ✗ | -0.51 | -0.63 | ✗  vol_x 1.2→1.44: -0.43R | 0 | 0.25R | 3, -1.25 (-1.25 / +0.00) | 55 / 104 of 170 | 0 | avg -0.39R/trade (needs +0.10R); profit factor 0.45; max drawdown 159.8R; longest drawdown 1738 days = 96% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 15m | **FAILED** | 1440 | 39.7 | -0.455 | 0.42 | 658.9R | -0.38 / -0.56 | -0.43 / -0.49 | 0/5 ✗ | -0.66 | -0.87 | ✗  stop atr 1.0→0.8: -0.55R | 0 | 0.37R | 7, -0.95 (-1.36 / +0.10) | 36 / 139 of 186 | 0 | not cost-viable: fees + slippage 0.37R per trade (stop must be ≥ 4x the round-trip cost); avg -0.46R/trade (needs +0.10R); profit factor 0.42; max drawdown 658.9R; longest drawdown 1691 days = 93% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1.0 | 5m | **FAILED** | 1659 | 35.8 | -0.491 | 0.39 | 815.8R | -0.47 / -0.55 | -0.51 / -0.46 | 0/5 ✗ | -0.73 | -0.97 | ✗  stop atr 1.5→1.2: -0.61R | 0 | 0.41R | 21, -1.16 (-1.19 / -1.10) | 127 / 32 of 187 | 0 | not cost-viable: fees + slippage 0.41R per trade (stop must be ≥ 4x the round-trip cost); avg -0.49R/trade (needs +0.10R); profit factor 0.39; recovery factor -1.00 (net -814.9R / max drawdown 815.8R) - needs 3; Monte Carlo 95% worst drawdown per 100 trades 70.0R - limit 17R; longest drawdown 726 days = 100% of the tested period (limit 55%); not profitable in BOTH train and unseen test |
| PB-B-SWEEP-15M | 1.0 | 15m | **FAILED** | 208 | 38.0 | -0.531 | 0.33 | 112.2R | -0.50 / -0.55 | -0.52 / -0.54 | 0/5 ✗ | -0.60 | -0.74 | ✗  time_stop_bars 16→13: -0.53R | 0 | 0.48R | 3, -1.32 (-1.32 / +0.00) | 0 / 0 of 14 | 0 | not cost-viable: fees + slippage 0.48R per trade (stop must be ≥ 4x the round-trip cost); avg -0.53R/trade (needs +0.15R); profit factor 0.33; max drawdown 112.2R; longest drawdown 701 days = 98% of the tested period (limit 60%); loss clustering: 15 losses in a row as it happened, random orders stay at or below 14 in 95% of cases; not profitable in BOTH train and unseen test |
| PB-B-SWEEP | 1.0 | 5m | **FAILED** | 886 | 34.7 | -0.647 | 0.25 | 575.4R | -0.67 / -0.57 | -0.63 / -0.66 | 0/5 ✗ | -0.76 | -0.84 | ✗  stop max_width_atr 3.0→2.4: -0.65R | 0 | 0.62R | 6, -0.46 (-0.46 / +0.00) | 0 / 0 of 25 | 0 | not cost-viable: fees + slippage 0.62R per trade (stop must be ≥ 4x the round-trip cost); avg -0.65R/trade (needs +0.15R); profit factor 0.25; max drawdown 575.4R; longest drawdown 722 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1.0 | 5m | **FAILED** | 3258 | 32.6 | -0.725 | 0.28 | 2363.9R | -0.70 / -0.79 | -0.73 / -0.71 | 0/5 ✗ | -1.13 | -1.54 | ✗  stop atr 1.0→0.8: -0.92R | 0 | 0.67R | 37, -1.43 (-1.52 / -1.16) | 124 / 319 of 484 | 0 | not cost-viable: fees + slippage 0.67R per trade (stop must be ≥ 4x the round-trip cost); avg -0.72R/trade (needs +0.10R); profit factor 0.28; max drawdown 2363.9R; longest drawdown 728 days = 100% of the tested period (limit 60%); not profitable in BOTH train and unseen test |

### 3b. Strategy lifecycle and control twins
IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING (automatic) → APPROVED (only with your yes). Strategy versions tested so far: **59** (`memory/experiments.md`); full record per version and timeframe in `memory/strategy_registry.csv`.

**Trials counter:** 284 strategy / version / timeframe tests so far (`memory/trials.csv`). The more ideas are tested, the more one looks good by luck, so PAPER_TRADING now also needs a t-statistic of the average trade ≥ **3.57** (Bonferroni: family-wise false-winner rate 0.05 over 284 trials; with 1 trial it would be 1.65).

**Research run duration:** 56.3 min (budget 90 min).

**Lookahead / recursive check** (on BTC): 56 cards checked - history cut after 6 signal candles, and started 500 candles later; 0 BIASED (426.9 s).

**Monte Carlo** (1000 shuffles of each cell's trades): PAPER_TRADING also needs the 95% worst drawdown ≤ 8R.

| Strategy | TF | Status | Trades | Drawdown as it happened | 95% worst drawdown | Expected worst losing streak |
|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT-S4 v1.1 | 4h | PAPER_TRADING | 633 | 25.9R | 24.2R ✗ | 15 |
| donchian_breakout-VEXIT v1.0 | 4h | PAPER_TRADING | 814 | 17.9R | 24.4R ✗ | 16 |
| donchian_breakout v1.0 | 4h | PAPER_TRADING | 837 | 10.7R | 22.3R ✗ | 11 |

**Rule significance:** in 69 strategy / timeframe cell(s) an entry rule adds nothing (the card does at least as well without it). Simpler cards queued in the lab: TRD-H4-BREAKOUT-S3, P02-EMA-PULLBACK-V4-S6-S6.

**Family gates (Phase 19 A, rules v1) - active since your yes on 2026-10-10.** The single max-drawdown gate is being replaced by a family table (config.yaml → family_gates). Old and new verdicts side by side; until you say yes after the shadow period, only the OLD verdict moves anything.

3 of 130 strategy / timeframe tests would get a different verdict.

| Strategy | TF | Group | Old verdict | New verdict | Recovery | 95% DD per 100 trades | Longest DD | Why (new rule) |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT-S4 v1.1 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 9.28 | 16.1R | 478 d (15%) | passes every gate |
| donchian_breakout-VEXIT v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 10.41 | 16.6R | 430 d (13%) | passes every gate |
| donchian_breakout v1.0 | 4h | trend | BACKTESTING | **PAPER_TRADING** | 8.2 | 13.9R | 584 d (18%) | passes every gate |

**Near-duplicates** (same timeframe, >= 70% of trades shared - counted as one idea, nothing else changes):

- P03-FIB-PULLBACK-V4 v1.0 4h = near-duplicate of P03-FIB-PULLBACK-V1 v1.0 4h (99% of 250 trades shared)

- P04-MACD-SUPERTREND-V4 v1.0 4h = near-duplicate of P04-MACD-SUPERTREND-V1 v1.0 4h (97% of 372 trades shared)

- PB-A-GRADED v1.0 5m = near-duplicate of PB-A-APLUS v1.0 5m (82% of 65 trades shared)

- PB-B-SWEEP-LIMIT v1.0 5m = near-duplicate of PB-B-APLUS v1.0 5m (80% of 215 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (79% of 2,554 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (75% of 1,778 trades shared)

- donchian_breakout-VEXIT-S4 v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (80% of 926 trades shared)

- donchian_breakout-VEXIT v1.0 1h = near-duplicate of donchian_breakout v1.0 1h (96% of 2,241 trades shared)

- donchian_breakout-VEXIT v1.0 30m = near-duplicate of donchian_breakout v1.0 30m (95% of 1,500 trades shared)

- donchian_breakout-VEXIT v1.0 4h = near-duplicate of donchian_breakout v1.0 4h (96% of 814 trades shared)

🧪 **Strategy lab:** 53 card(s) from `strategies_lab.yaml` (written by Claude's reviews). They are tested exactly like the library and can reach PAPER_TRADING, but never send emails (not even PAPER ones) and are never APPROVED - to approve one, move the card into `strategies.yaml` by pull request.

**SMC vs control twin** (the same idea without the SMC part; SMC is only kept if it wins overall AND in the validate part, with enough trades on both sides):

| Strategy | TF | Trades | Avg R | Validate R | Twin avg R | Twin validate R | Beats twin? |
|---|---|---|---|---|---|---|---|
| S5-SWEEP-MSS-FVG-5M | 15m | 2 | +0.130 | +0.000 | -0.616 | -4.320 | too few trades to compare |
| TRD-H4-BREAKOUT | 1h | 821 | +0.109 | +0.255 | +0.029 | +0.056 | yes |
| TRD-H4-BREAKOUT | 30m | 559 | +0.100 | +0.255 | -0.035 | +0.034 | yes |
| S6-OB-FVG | 15m | 0 | +0.000 | +0.000 | -0.147 | +0.007 | too few trades to compare |
| S6-OB-FVG-5M | 15m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET-5M | 15m | 0 | +0.000 | +0.000 | -0.218 | +0.000 | too few trades to compare |
| PB-C-BREAKOUT | 5m | 0 | +0.000 | +0.000 | +0.000 | +0.000 | too few trades to compare |
| S7-SILVER-BULLET | 15m | 7 | -0.001 | -1.190 | -0.138 | -0.163 | too few trades to compare |
| TRD-H4-PULLBACK | 15m | 1950 | -0.006 | +0.123 | -0.089 | -0.044 | yes |
| TRD-H4-BREAKOUT | 15m | 983 | -0.032 | +0.032 | -0.086 | -0.052 | yes |
| S8-PDH-PDL-SWEEP-5M | 30m | 5 | -0.172 | -0.517 | -0.504 | -0.581 | too few trades to compare |
| PB-A-PULLBACK-CVD | 5m | 10 | -0.520 | -1.097 | -0.497 | -1.097 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 30m | 9 | -0.653 | -1.173 | -0.023 | -0.100 | too few trades to compare |
| S5-SWEEP-MSS-FVG | 15m | 12 | -0.839 | -2.597 | +0.074 | -0.542 | too few trades to compare |
| S5-SWEEP-MSS-FVG-5M | 30m | 1 | -1.208 | +0.000 | -0.487 | -1.179 | too few trades to compare |
| TRD-H4-PULLBACK | 1h | 803 | +0.015 | -0.018 | -0.017 | -0.064 | yes |
| TRD-H4-PULLBACK | 5m | 2179 | -0.027 | +0.047 | -0.107 | -0.071 | yes |
| TRD-H4-PULLBACK | 30m | 1053 | -0.051 | +0.074 | -0.098 | -0.039 | yes |
| S8-PDH-PDL-SWEEP | 1h | 229 | -0.058 | -0.280 | -0.115 | -0.062 | no |
| TRD-H4-BREAKOUT | 5m | 1363 | -0.068 | -0.020 | -0.119 | -0.080 | yes |
| S8-PDH-PDL-SWEEP | 30m | 200 | -0.269 | -0.418 | -0.364 | -0.525 | yes |
| PB-B-SWEEP | 5m | 886 | -0.647 | -0.573 | -0.375 | -0.375 | too few trades to compare |

- **donchian_breakout-VEXIT v1.0 4h:** passed every Phase 8 test - paper signals start (logged, PAPER emails)
- **donchian_breakout-VEXIT-S4 v1.1 4h:** passed every Phase 8 test - paper signals start (logged, PAPER emails)
- **donchian_breakout v1.0 4h:** passed every Phase 8 test - paper signals start (logged, PAPER emails)
**Status changes in the last research run** (all of them in `memory/strategy_lifecycle.md`): P02-EMA-PULLBACK-V4-S6@1.0 4h FORMALIZED → BACKTESTING; P03-FIB-PULLBACK-V1@1.0 4h FORMALIZED → FAILED; P03-FIB-PULLBACK-V2@1.0 15m FORMALIZED → FAILED; P03-FIB-PULLBACK-V2@1.0 1h FORMALIZED → FAILED; P03-FIB-PULLBACK-V2@1.0 30m FORMALIZED → FAILED; P03-FIB-PULLBACK-V3@1.0 4h FORMALIZED → FAILED; P03-FIB-PULLBACK-V4@1.0 4h FORMALIZED → FAILED; P03-FIB-PULLBACK-V5@1.0 15m FORMALIZED → FAILED; P03-FIB-PULLBACK-V5@1.0 1h FORMALIZED → FAILED; P03-FIB-PULLBACK-V5@1.0 30m FORMALIZED → FAILED; P04-MACD-SUPERTREND-V1@1.0 4h FORMALIZED → FAILED; P04-MACD-SUPERTREND-V2@1.0 15m FORMALIZED → FAILED; ... and 16 more
- **Not tested (IDEA / RETIRED):** donchian_breakout-VEXIT-VRVOL v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S4-S4 v1.0 (RETIRED); donchian_breakout-VEXIT-VRVOL-S5 v1.0 (RETIRED)

### 3c. Research layers (daily run)
Last run: **2026-10-11 00:58 UTC**. History used per timeframe (all research coins pooled; develop = first 70% of each coin, validate = last 30%; walk-forward = the history cut into equal time windows, the first one only warms up):

| TF | Coins | From | To | Candles (largest coin) | Note |
|---|---|---|---|---|---|
| 4h | 7 | 2017-08-17 | 2026-10-10 | 20035 |  |
| 1h | 7 | 2017-08-17 | 2026-10-10 | 80076 |  |
| 30m | 7 | 2021-10-03 | 2026-10-11 | 87600 |  |
| 15m | 7 | 2021-10-03 | 2026-10-11 | 175200 |  |
| 5m | 7 | 2024-10-11 | 2026-10-11 | 210240 |  |

*Everything per strategy (walk-forward windows, every ±20% variant, results per coin): `reports/research.json`.*

### 3d. Why trades lose (failure attribution)
Every backtest trade gets reason tags by fixed rules (section 17; rules and numbers in `config.yaml` → `attribution`). A tag is **systematic** (✓) only if it is clearly more common among losing trades than among winning ones (more than 2 standard errors, at least 30 losses) - or, for tags that only exist for losers, if it is in at least 25% of them. **Best point of losers** (MFE) = how far the typical loser was in profit first; **worst point of winners** (MAE) = how much heat the typical winner took. Only strategy / timeframe tests with 30+ trades are shown.

| Strategy | TF | Status | Trades (losers) | Systematic causes ✓ | Common in losers (more than in winners) | Losers' best point | Winners' worst point | R before / after costs |
|---|---|---|---|---|---|---|---|---|
| donchian_breakout-VEXIT | 4h | BACKTESTING | 814 (479) | false_breakout, trend_reversal | false_breakout 63% | +0.47R | -0.37R | +0.31 / +0.25 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 926 (552) | false_breakout, trend_reversal | false_breakout 62% | +0.48R | -0.37R | +0.30 / +0.24 |
| donchian_breakout-VEXIT-S4 | 4h | BACKTESTING | 633 (375) | no_displacement, false_breakout | false_breakout 63%, no_displacement 36% | +0.46R | -0.36R | +0.28 / +0.23 |
| P01-BREAKOUT-V3 | 4h | BACKTESTING | 333 (198) | false_breakout | false_breakout 68%, no_displacement 33% | +0.43R | -0.37R | +0.26 / +0.21 |
| P01-BREAKOUT-V1 | 4h | BACKTESTING | 1058 (639) | htf_conflict, false_breakout, trend_reversal | false_breakout 62% | +0.53R | -0.41R | +0.24 / +0.19 |
| P01-BREAKOUT-V4 | 4h | BACKTESTING | 900 (544) | htf_conflict, false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, regime_mismatch 39%, stop_too_tight 38% | +0.53R | -0.43R | +0.25 / +0.18 |
| donchian_breakout | 4h | BACKTESTING | 837 (371) | false_breakout, trend_reversal, regime_mismatch, stop_too_tight | false_breakout 66%, stop_too_tight 34%, no_displacement 33% | +0.33R | -0.37R | +0.21 / +0.16 |
| TRD-H4-BREAKOUT | 1h | BACKTESTING | 821 (507) | false_breakout | false_breakout 65% | +0.54R | -0.44R | +0.16 / +0.11 |
| TRD-H4-BREAKOUT | 30m | BACKTESTING | 559 (337) | false_breakout | false_breakout 75%, no_displacement 46% | +0.52R | -0.43R | +0.18 / +0.10 |
| P02-EMA-PULLBACK-V4 | 4h | BACKTESTING | 297 (193) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 84%, indicator_lag 36%, stop_too_tight 28% | +0.43R | -0.50R | +0.18 / +0.10 |
| TRD-H4-BREAKOUT-noT4 | 1h | BACKTESTING | 2641 (1670) | false_breakout | false_breakout 65% | +0.51R | -0.44R | +0.09 / +0.03 |
| bb_squeeze_breakout | 1h | BACKTESTING | 640 (303) | false_breakout, regime_mismatch, stop_too_tight | false_breakout 64%, no_displacement 51%, stop_too_tight 38%, regime_mismatch 35% | +0.35R | -0.47R | +0.16 / +0.01 |
| P01-BREAKOUT-V2 | 30m | BACKTESTING | 873 (557) | no_displacement, false_breakout | false_breakout 75%, no_displacement 38% | +0.45R | -0.42R | +0.16 / +0.01 |
| macd_trend_cross | 1h | BACKTESTING | 139 (67) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 91%, indicator_lag 45%, stop_too_tight 34% | +0.28R | -0.39R | +0.13 / -0.01 |
| TRD-H4-PULLBACK | 15m | BACKTESTING | 1950 (1207) | none | - | +0.50R | -0.39R | +0.10 / -0.01 |
| donchian_breakout-VEXIT-S4 | 30m | BACKTESTING | 1280 (832) | no_displacement, false_breakout | false_breakout 70%, no_displacement 39% | +0.48R | -0.40R | +0.12 / -0.01 |
| TRD-H4-BREAKOUT | 15m | BACKTESTING | 983 (636) | false_breakout | false_breakout 75% | +0.44R | -0.49R | +0.07 / -0.03 |
| PB-B-SWEEP-LIMIT | 5m | BACKTESTING | 215 (131) | none | - | +0.23R | -0.21R | +0.05 / -0.13 |
| PB-B-APLUS | 5m | BACKTESTING | 183 (116) | none | - | +0.20R | -0.28R | +0.04 / -0.14 |
| PB-B-APLUS | 15m | BACKTESTING | 79 (43) | stop_too_tight | regime_mismatch 46%, stop_too_tight 44% | +0.29R | -0.34R | +0.02 / -0.14 |
| PB-A-GRADED | 5m | BACKTESTING | 65 (38) | stop_too_tight, indicator_lag | stop_too_tight 37%, indicator_lag 26% | +0.43R | -0.24R | -0.08 / -0.25 |
| PB-A-APLUS | 5m | BACKTESTING | 53 (33) | stop_too_tight, indicator_lag | stop_too_tight 42%, indicator_lag 30% | +0.42R | -0.27R | -0.13 / -0.31 |
| P04-MACD-SUPERTREND-V3 | 4h | FORMALIZED | 150 (92) | false_breakout, indicator_lag | regime_mismatch 49%, false_breakout 47%, indicator_lag 30% | +0.37R | -0.36R | +0.26 / +0.20 |
| P02-EMA-PULLBACK-V4-S6 | 4h | FORMALIZED | 365 (234) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 77%, indicator_lag 33%, stop_too_tight 28% | +0.45R | -0.50R | +0.23 / +0.14 |
| P04-MACD-SUPERTREND-V4 | 4h | FORMALIZED | 372 (233) | overextended_entry, false_breakout, regime_mismatch, stop_too_tight, indicator_lag, structural_change | regime_mismatch 49%, overextended_entry 48%, false_breakout 46%, stop_too_tight 36% | +0.41R | -0.38R | +0.20 / +0.13 |
| P04-MACD-SUPERTREND-V1 | 4h | FORMALIZED | 383 (245) | overextended_entry, false_breakout, indicator_lag, structural_change | regime_mismatch 49%, overextended_entry 49%, false_breakout 46%, indicator_lag 31% | +0.43R | -0.37R | +0.18 / +0.11 |
| P03-FIB-PULLBACK-V4 | 4h | FORMALIZED | 250 (172) | late_entry, stop_too_tight, indicator_lag, structural_change | regime_mismatch 58%, stop_too_tight 33%, indicator_lag 28% | +0.48R | -0.43R | +0.07 / -0.03 |
| P04-MACD-SUPERTREND-V2 | 1h | FORMALIZED | 1199 (798) | false_breakout, regime_mismatch, indicator_lag | regime_mismatch 51%, false_breakout 42%, indicator_lag 34% | +0.46R | -0.39R | +0.07 / -0.03 |
| P04-MACD-SUPERTREND-V2 | 30m | FORMALIZED | 1450 (946) | no_displacement, false_breakout, regime_mismatch, indicator_lag | no_displacement 75%, false_breakout 36%, indicator_lag 34%, regime_mismatch 30% | +0.48R | -0.45R | +0.11 / -0.04 |
| P04-MACD-SUPERTREND-V2 | 15m | FORMALIZED | 2287 (1507) | range_market, indicator_lag | range_market 37%, indicator_lag 34% | +0.47R | -0.44R | +0.13 / -0.08 |
| P03-FIB-PULLBACK-V1 | 4h | FORMALIZED | 253 (165) | indicator_lag | indicator_lag 30% | +0.43R | -0.44R | +0.00 / -0.08 |
| P03-FIB-PULLBACK-V2 | 1h | FORMALIZED | 2388 (1563) | regime_mismatch, indicator_lag | regime_mismatch 66%, indicator_lag 36% | +0.42R | -0.45R | +0.05 / -0.09 |
| P04-MACD-SUPERTREND-V5 | 1h | FORMALIZED | 2387 (1631) | htf_conflict, false_breakout, regime_mismatch, indicator_lag | regime_mismatch 57%, false_breakout 40%, indicator_lag 35% | +0.45R | -0.42R | +0.01 / -0.10 |
| P04-MACD-SUPERTREND-V5 | 30m | FORMALIZED | 3360 (2253) | false_breakout, regime_mismatch, indicator_lag | false_breakout 34%, regime_mismatch 33%, indicator_lag 33% | +0.48R | -0.42R | +0.06 / -0.11 |
| P03-FIB-PULLBACK-V5 | 1h | FORMALIZED | 5109 (3393) | regime_mismatch, indicator_lag | regime_mismatch 69%, indicator_lag 35% | +0.42R | -0.46R | +0.03 / -0.12 |
| P04-MACD-SUPERTREND-V5 | 15m | FORMALIZED | 5024 (3371) | range_market, false_breakout, indicator_lag | indicator_lag 35% | +0.45R | -0.45R | +0.10 / -0.14 |
| P03-FIB-PULLBACK-V2 | 30m | FORMALIZED | 2812 (1840) | regime_mismatch, indicator_lag | indicator_lag 37% | +0.41R | -0.46R | +0.08 / -0.14 |
| P03-FIB-PULLBACK-V3 | 4h | FORMALIZED | 87 (60) | indicator_lag | indicator_lag 32% | +0.49R | -0.42R | -0.07 / -0.14 |
| P03-FIB-PULLBACK-V5 | 30m | FORMALIZED | 6226 (4141) | range_market, regime_mismatch, indicator_lag | indicator_lag 38% | +0.40R | -0.47R | +0.06 / -0.19 |
| P03-FIB-PULLBACK-V2 | 15m | FORMALIZED | 4763 (3163) | indicator_lag | indicator_lag 40% | +0.39R | -0.48R | +0.08 / -0.23 |
| P03-FIB-PULLBACK-V5 | 15m | FORMALIZED | 10470 (7057) | indicator_lag | indicator_lag 40% | +0.38R | -0.48R | +0.07 / -0.28 |
| bb_squeeze_breakout | 4h | FAILED | 215 (103) | false_breakout, stop_too_tight, structural_change | false_breakout 59%, stop_too_tight 42%, regime_mismatch 32% | +0.33R | -0.36R | +0.12 / +0.04 |
| TRD-H4-PULLBACK | 1h | FAILED | 803 (503) | low_relative_volume, indicator_lag, structural_change | low_relative_volume 56%, indicator_lag 25% | +0.45R | -0.41R | +0.07 / +0.01 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 1795 (1207) | false_breakout, regime_mismatch | false_breakout 62%, regime_mismatch 31% | +0.50R | -0.39R | +0.07 / -0.01 |
| TRD-H4-PULLBACK-noT4 | 1h | FAILED | 3699 (2307) | structural_change | - | +0.50R | -0.42R | +0.05 / -0.02 |
| donchian_breakout-VEXIT | 1h | FAILED | 2241 (1511) | false_breakout | false_breakout 63% | +0.51R | -0.39R | +0.07 / -0.02 |
| donchian_breakout-VEXIT-S4 | 1h | FAILED | 2554 (1720) | false_breakout, regime_mismatch | false_breakout 64%, regime_mismatch 32% | +0.50R | -0.40R | +0.08 / -0.02 |
| P01-BREAKOUT-V2 | 1h | FAILED | 1849 (1251) | false_breakout | false_breakout 64% | +0.52R | -0.38R | +0.07 / -0.02 |
| P01-BREAKOUT-V5 | 1h | FAILED | 3762 (2521) | false_breakout | false_breakout 61% | +0.50R | -0.41R | +0.08 / -0.02 |
| P02-EMA-PULLBACK-V1 | 4h | FAILED | 299 (205) | regime_mismatch, indicator_lag, structural_change | regime_mismatch 85%, indicator_lag 38% | +0.41R | -0.42R | +0.06 / -0.02 |
| TRD-H4-PULLBACK | 5m | FAILED | 2179 (1348) | overextended_entry | - | +0.52R | -0.43R | +0.11 / -0.03 |
| TRD-H4-BREAKOUT-noT4 | 30m | FAILED | 1939 (1245) | false_breakout | false_breakout 71% | +0.50R | -0.43R | +0.05 / -0.04 |
| donchian_breakout | 1h | FAILED | 2301 (1193) | no_displacement, false_breakout, regime_mismatch, stop_too_tight | false_breakout 66%, no_displacement 37%, stop_too_tight 32%, regime_mismatch 26% | +0.37R | -0.40R | +0.05 / -0.04 |
| TRD-H4-PULLBACK | 30m | FAILED | 1053 (677) | none | - | +0.48R | -0.41R | +0.03 / -0.05 |
| donchian_breakout-VEXIT-S4 | 30m | FAILED | 1778 (1177) | false_breakout | false_breakout 71% | +0.47R | -0.41R | +0.10 / -0.05 |
| donchian_breakout-VEXIT | 30m | FAILED | 1500 (999) | false_breakout | false_breakout 71% | +0.47R | -0.41R | +0.08 / -0.05 |
| P01-BREAKOUT-V2 | 15m | FAILED | 1330 (872) | false_breakout | false_breakout 71% | +0.47R | -0.43R | +0.15 / -0.06 |
| S8-PDH-PDL-SWEEP | 1h | FAILED | 229 (148) | stop_too_tight, sweep_continued, structural_change | sweep_continued 97%, range_market 56%, stop_too_tight 30% | +0.56R | -0.40R | +0.15 / -0.06 |
| donchian_breakout | 30m | FAILED | 1553 (805) | no_displacement, false_breakout, stop_too_tight | false_breakout 75%, no_displacement 39%, stop_too_tight 33% | +0.29R | -0.40R | +0.07 / -0.07 |
| TRD-H4-BREAKOUT | 5m | FAILED | 1363 (864) | false_breakout | false_breakout 74% | +0.43R | -0.44R | +0.07 / -0.07 |
| trend_pullback | 4h | FAILED | 934 (485) | regime_mismatch, indicator_lag | regime_mismatch 80%, indicator_lag 38% | +0.36R | -0.43R | +0.00 / -0.07 |
| supertrend_flip | 4h | FAILED | 70 (38) | indicator_lag, structural_change | regime_mismatch 63%, indicator_lag 40% | +0.39R | -0.43R | -0.01 / -0.08 |
| TRD-H4-BREAKOUT-noT4 | 15m | FAILED | 3341 (2199) | false_breakout | false_breakout 74% | +0.45R | -0.45R | +0.03 / -0.09 |
| TRD-H4-PULLBACK-noT4 | 15m | FAILED | 7330 (4679) | none | - | +0.50R | -0.40R | +0.03 / -0.09 |
| P02-EMA-PULLBACK-V2 | 1h | FAILED | 2302 (1585) | low_relative_volume, regime_mismatch, indicator_lag | regime_mismatch 82%, low_relative_volume 52%, indicator_lag 37% | +0.40R | -0.42R | +0.04 / -0.09 |
| P01-BREAKOUT-V5 | 30m | FAILED | 1938 (1301) | false_breakout | false_breakout 70% | +0.46R | -0.42R | +0.08 / -0.10 |
| TRD-H4-PULLBACK-noT4 | 30m | FAILED | 4260 (2798) | none | - | +0.51R | -0.40R | -0.01 / -0.10 |
| rsi2_dip_buy | 4h | FAILED | 1421 (614) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 45% | +0.16R | -0.21R | -0.05 / -0.10 |
| TRD-H4-PULLBACK-noT4 | 5m | FAILED | 6309 (4006) | overextended_entry | - | +0.51R | -0.43R | +0.04 / -0.11 |
| P02-EMA-PULLBACK-V5 | 1h | FAILED | 4852 (3391) | low_relative_volume, regime_mismatch, indicator_lag | regime_mismatch 84%, indicator_lag 38% | +0.40R | -0.41R | +0.04 / -0.11 |
| rsi2_dip_buy | 1h | FAILED | 5256 (2342) | trend_reversal, regime_mismatch, volatility_spike | regime_mismatch 43% | +0.15R | -0.21R | -0.00 / -0.11 |
| S8-PDH-PDL-SWEEP-noSMC | 1h | FAILED | 608 (409) | range_market, stop_too_tight | range_market 47%, stop_too_tight 36% | +0.59R | -0.50R | +0.10 / -0.12 |
| TRD-H4-BREAKOUT-noT4 | 5m | FAILED | 3770 (2444) | false_breakout | false_breakout 73% | +0.48R | -0.44R | +0.04 / -0.12 |
| trend_pullback | 1h | FAILED | 4792 (2547) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 77%, indicator_lag 44%, stop_too_tight 28% | +0.30R | -0.43R | +0.02 / -0.12 |
| ema_9_21_cross | 1h | FAILED | 270 (153) | regime_mismatch, indicator_lag | regime_mismatch 81%, indicator_lag 48% | +0.26R | -0.35R | +0.00 / -0.13 |
| P02-EMA-PULLBACK-V2 | 30m | FAILED | 1692 (1180) | range_market, low_relative_volume, indicator_lag | low_relative_volume 59%, indicator_lag 40%, range_market 37% | +0.37R | -0.40R | +0.09 / -0.14 |
| S6-OB-FVG-noSMC | 15m | FAILED | 95 (63) | none | stop_too_wide 89%, range_market 52% | +0.35R | -0.28R | +0.01 / -0.15 |
| R4-CLUC | 30m | FAILED | 240 (149) | none | - | +0.31R | -0.41R | -0.05 / -0.15 |
| P01-BREAKOUT-V5 | 15m | FAILED | 2971 (2032) | false_breakout | false_breakout 70% | +0.44R | -0.42R | +0.09 / -0.15 |
| PB-B-GRADED | 5m | FAILED | 901 (572) | none | - | +0.21R | -0.24R | +0.02 / -0.15 |
| liquidity_sweep_reversal | 1h | FAILED | 243 (127) | stop_too_tight | stop_too_tight 50% | +0.28R | -0.49R | +0.00 / -0.16 |
| P02-EMA-PULLBACK-V5 | 30m | FAILED | 3703 (2593) | range_market, low_relative_volume, indicator_lag | indicator_lag 40% | +0.37R | -0.42R | +0.09 / -0.16 |
| bb_squeeze_breakout | 30m | FAILED | 657 (345) | false_breakout, stop_too_tight | false_breakout 61%, stop_too_tight 36% | +0.27R | -0.46R | +0.07 / -0.17 |
| PB-B-GRADED | 15m | FAILED | 821 (495) | stop_too_tight | stop_too_tight 36% | +0.32R | -0.32R | -0.00 / -0.17 |
| rsi2_dip_buy | 30m | FAILED | 4642 (2391) | trend_reversal, volatility_spike, fees_slippage | fees_slippage 32% | +0.16R | -0.20R | +0.01 / -0.17 |
| supertrend_flip | 30m | FAILED | 240 (132) | regime_mismatch, stop_too_tight, indicator_lag | regime_mismatch 44%, stop_too_tight 36%, indicator_lag 36%, late_entry 32% | +0.40R | -0.39R | -0.02 / -0.17 |
| trend_pullback | 30m | FAILED | 5648 (3036) | stop_too_tight, indicator_lag | indicator_lag 46%, stop_too_tight 30% | +0.28R | -0.43R | +0.02 / -0.18 |
| macd_trend_cross | 30m | FAILED | 441 (229) | stop_too_tight, indicator_lag | regime_mismatch 72%, indicator_lag 44%, stop_too_tight 37%, low_relative_volume 37% | +0.30R | -0.46R | +0.03 / -0.18 |
| ema_9_21_cross | 30m | FAILED | 557 (325) | indicator_lag | indicator_lag 47% | +0.27R | -0.38R | +0.01 / -0.18 |
| R4-CLUC | 15m | FAILED | 199 (130) | none | - | +0.38R | -0.31R | -0.07 / -0.19 |
| supertrend_flip | 1h | FAILED | 209 (115) | regime_mismatch, stop_too_tight, indicator_lag | wrong_session 71%, regime_mismatch 70%, stop_too_tight 36%, indicator_lag 32% | +0.39R | -0.37R | -0.11 / -0.21 |
| ema_9_21_cross | 15m | FAILED | 1534 (883) | stop_too_tight, indicator_lag | indicator_lag 50%, stop_too_tight 25% | +0.25R | -0.44R | +0.06 / -0.21 |
| P02-EMA-PULLBACK-V2 | 15m | FAILED | 3121 (2231) | range_market, htf_conflict, indicator_lag | range_market 47%, indicator_lag 43% | +0.34R | -0.39R | +0.11 / -0.21 |
| rsi2_dip_buy | 15m | FAILED | 7420 (4457) | wrong_session, trend_reversal, regime_mismatch, volatility_spike, fees_slippage | fees_slippage 42% | +0.16R | -0.20R | +0.03 / -0.24 |
| trend_pullback | 15m | FAILED | 9637 (5319) | range_market, stop_too_tight, indicator_lag | indicator_lag 48%, stop_too_tight 30% | +0.27R | -0.43R | +0.04 / -0.25 |
| P02-EMA-PULLBACK-V3 | 4h | FAILED | 117 (90) | indicator_lag | indicator_lag 39% | +0.40R | -0.41R | -0.18 / -0.26 |
| P02-EMA-PULLBACK-V5 | 15m | FAILED | 6894 (4974) | range_market, wrong_session, indicator_lag | indicator_lag 45% | +0.32R | -0.40R | +0.10 / -0.26 |
| S8-PDH-PDL-SWEEP | 30m | FAILED | 200 (144) | stop_too_tight, sweep_continued | sweep_continued 98%, stop_too_tight 28% | +0.46R | -0.49R | +0.01 / -0.27 |
| R4-BBRSI | 1h | FAILED | 991 (700) | none | - | +0.45R | -0.46R | -0.14 / -0.30 |
| bb_squeeze_breakout | 15m | FAILED | 1409 (802) | false_breakout, stop_too_tight | false_breakout 63%, stop_too_tight 36% | +0.30R | -0.47R | +0.02 / -0.31 |
| R4-BBRSI | 30m | FAILED | 2699 (1872) | none | - | +0.42R | -0.46R | -0.08 / -0.32 |
| S8-PDH-PDL-SWEEP-noSMC | 30m | FAILED | 862 (618) | stop_too_tight | stop_too_tight 34% | +0.56R | -0.50R | -0.02 / -0.36 |
| liquidity_sweep_reversal | 30m | FAILED | 394 (232) | stop_too_tight | stop_too_tight 41% | +0.31R | -0.52R | -0.11 / -0.39 |
| liquidity_sweep_reversal | 15m | FAILED | 1440 (868) | stop_too_tight | stop_too_tight 40% | +0.29R | -0.48R | -0.01 / -0.46 |
| ema_9_21_cross | 5m | FAILED | 1659 (1065) | stop_too_tight, indicator_lag | indicator_lag 52%, stop_too_tight 30% | +0.21R | -0.44R | +0.02 / -0.49 |
| PB-B-SWEEP-15M | 15m | FAILED | 208 (129) | stop_too_tight | stop_too_tight 33%, low_relative_volume 26% | +0.22R | -0.44R | -0.02 / -0.53 |
| PB-B-SWEEP | 5m | FAILED | 886 (579) | stop_too_tight | stop_too_tight 35%, range_market 27% | +0.13R | -0.37R | +0.07 / -0.65 |
| liquidity_sweep_reversal | 5m | FAILED | 3258 (2197) | range_market, stop_too_tight | stop_too_tight 40% | +0.25R | -0.51R | +0.10 / -0.72 |

**Candidate lessons** (systematic in 2+ tests - NOT yet lessons: they need a review before anything changes, and any change is a new version): `indicator_lag` (systematic in 35 strategy/timeframe tests); `stop_too_tight` (systematic in 33 strategy/timeframe tests); `false_breakout` (systematic in 32 strategy/timeframe tests); `regime_mismatch` (systematic in 24 strategy/timeframe tests); `trend_reversal` (systematic in 7 strategy/timeframe tests); `range_market` (systematic in 6 strategy/timeframe tests); `no_displacement` (systematic in 5 strategy/timeframe tests); `volatility_spike` (systematic in 4 strategy/timeframe tests); `overextended_entry` (systematic in 4 strategy/timeframe tests); `sweep_continued` (systematic in 2 strategy/timeframe tests); `fees_slippage` (systematic in 2 strategy/timeframe tests)

**Missed moves:** no strong move in the last 24 hours at the last research run.

*The 8 questions of section 17.3 (wrong strategy? wrong regime? timing? stop / target? sample size? costs? other timeframe? systematic or random?) are answered per test in `reports/research.json` → `cells` → `attribution` → `diagnosis`. Losing paper / live signals: `memory/failure_journal.md`.*

### 3e. Memory (section 22)
| File | Size | Records | Newest record |
|---|---|---|---|
| `memory/README.md` | 4.6 KB | - | - |
| `memory/beginner_course.md` | 5.1 KB | - | - |
| `memory/changelog.md` | 149.6 KB | - | - |
| `memory/cleanup_log.md` | 0.5 KB | - | - |
| `memory/coin_notes.md` | 20.2 KB | 20 | 2026-10-11 00:29 UTC |
| `memory/curriculum.md` | 12.6 KB | - | - |
| `memory/execution_notes.md` | 16.5 KB | 37 | 2026-10-11 00:29 UTC |
| `memory/experiments.md` | 73.2 KB | 30 | 2026-10-10 15:30 UTC |
| `memory/failure_journal.md` | 0.6 KB | - | - |
| `memory/family_gates_calibration.md` | 14.4 KB | - | - |
| `memory/family_gates_shadow.csv` | 343.8 KB | - | - |
| `memory/feature_notes.md` | 3.6 KB | - | - |
| `memory/lessons.md` | 2.8 KB | 1 | 2026-09-26 06:22 UTC |
| `memory/market_mechanics.md` | 13.2 KB | 14 | 2026-10-10 15:30 UTC |
| `memory/market_regime_log.md` | 19.9 KB | - | - |
| `memory/missed_trades.md` | 60.2 KB | 77 | 2026-10-10 15:30 UTC |
| `memory/playbook.md` | 10.0 KB | - | - |
| `memory/research_sources.md` | 110.8 KB | 84 | 2026-10-10 15:30 UTC |
| `memory/smc_events.csv` | 1308.4 KB | - | - |
| `memory/smc_research.md` | 7.2 KB | 1 | 2026-09-27 02:00 UTC |
| `memory/strategy_lifecycle.md` | 31.1 KB | - | - |
| `memory/strategy_registry.csv` | 76.6 KB | - | - |
| `memory/trials.csv` | 17.5 KB | - | - |
| `memory/universe_log.md` | 28.5 KB | - | - |

**Reviews due** (review date passed; for the reviews): `missed_trades.md` LTC up +14.2% (8.0x ATR), 2026-09-24 01:00 -> 2026-09-24 14:00 (2026-10-02); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03); `missed_trades.md` SOL and ENA 2026-09-25 moves: "identifiable" only through failing cells (2026-10-03); `missed_trades.md` SOL up +4.8% (5.5x ATR), 2026-09-25 07:00 -> 2026-09-25 19:00 (2026-10-03); `missed_trades.md` SUI up +13.4% (7.3x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` ENA up +18.4% (7.5x ATR), 2026-09-25 08:00 -> 2026-09-25 21:00 (2026-10-03); `missed_trades.md` UNI up +8.2% (5.3x ATR), 2026-09-25 07:00 -> 2026-09-25 13:00 (2026-10-03) … and 20 more
Append-only files may only grow: `memory_guard.py` stops the run before anything else is saved.

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG and SHORT = OKX futures fees + funding (always charged, never received). Details in `config.yaml` → `costs`.

**Full data** (branch `live-reports`, newest copy only): [latest.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) · [smc.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) · [features.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) · [regime.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) · [feature_evidence.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) · [data_quality.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) · [research.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) · [dashboard_data.json](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/dashboard_data.json) · [derivs_hourly.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/derivs_hourly.csv.gz) · [funding.csv.gz](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/funding.csv.gz)

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*