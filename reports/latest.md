# Crypto Signal Report

**Updated:** 2026-09-25 02:21 Beijing time (2026-09-24 18:21 UTC) · data: Binance · 8 coins scanned

> Signals only - not financial advice. Paper-trade first. Never risk money you cannot afford to lose.

## 0. Data check
- **System: GOOD** - all data passed the checks - signals allowed (all checks passed)
- **Price cross-check** Binance vs OKX: largest difference 0.01% (limit 0.5%)

| Coin | Data state | Problem |
|---|---|---|
| PROVE | **DEGRADED** | 1d: DEGRADED: volume 52x normal on candle 09-23 00:00 UTC (possible bad data) |
- 59 small note(s) (e.g. unfinished candles ignored) - see `reports/data_quality.json`

## 0b. Coins this run
- **Signal coins (7/7)** - only these can give signals: **BTC**, **ETH**, **ZEC**, **XRP**, **SOL**, **BNB**, **UNI**
- **Research only** - backtested, never a signal: SUI
- **Changes this run** (also written to `memory/universe_log.md`):
  - **EXCLUDED** PROVE - 7-day average volume $36M < $50M; order book too thin: $64k within 1% (need $250k)
  - **FLAG** PROVE - price data DEGRADED - stays in the list, but no signals
  - **EXCLUDED** LTC - 7-day average volume $34M < $50M
  - **EXCLUDED** ONDO - 7-day average volume $30M < $50M; order book too thin: $181k within 1% (need $250k)
  - **JOIN** BTC - starting list (no members yet): rank #1
  - **JOIN** ETH - starting list (no members yet): rank #2
  - **JOIN** ZEC - starting list (no members yet): rank #3
  - **JOIN** XRP - starting list (no members yet): rank #4
  - **JOIN** SOL - starting list (no members yet): rank #5
  - **JOIN** BNB - starting list (no members yet): rank #6
  - **JOIN** UNI - starting list (no members yet): rank #7

| Not eligible | 24h volume | Why |
|---|---|---|
| PROVE | $180M | 7-day average volume $36M < $50M; order book too thin: $64k within 1% (need $250k) |
| LTC | $142M | 7-day average volume $34M < $50M |
| ONDO | $107M | 7-day average volume $30M < $50M; order book too thin: $181k within 1% (need $250k) |

**Flags (not excluded):** PROVE: price data DEGRADED - stays in the list, but no signals

*Skipped by your exclusion lists:* DOGE, NEAR, PEPE, RLUSD, USD1, USDC, WLD (see `config.yaml`)

## 0c. Timeframes loaded
- **Timeframe model B (active):** 1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry. Higher timeframes give permission, lower ones give timing; a candle only ever uses higher-timeframe candles that had already closed.
- Models to test later: D (needs 2h)

| Coin | 1W | 1D | 7D | 4H | 1H | 30M | 15M | 5M | Weekly history from | Cross-check |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 475 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2017-08 | OK (300 candles) |
| ETH | 475 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2017-08 | OK (300 candles) |
| ZEC | 392 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2019-03 | OK (300 candles) |
| XRP | 438 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2018-04 | OK (300 candles) |
| SOL | 319 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2020-08 | OK (300 candles) |
| BNB | 463 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2017-11 | OK (300 candles) |
| UNI | 314 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2020-09 | OK (300 candles) |
| SUI | 177 | 999 | 993 | 1499 | 1999 | 1999 | 1999 | 1999 | 2023-05 | OK (300 candles) |

*Candle counts per timeframe. 7D = rolling 7-day candles built from the daily candles. Cross-check = do the bigger candles agree with the smaller candles inside them?*

## 0d. Market features now (1H, newest closed candle)
Measurements only - nothing trades on these yet. Structure = the last confirmed swing labels (HH/HL = up, LH/LL = down). Close location: 0 = closed at the low, 1 = at the high.

| Coin | Structure | Last swing high / low | Close location | Volume vs normal | Candle size vs normal | Last 3 candles |
|---|---|---|---|---|---|---|
| BTC | mixed (HH/LL) | 84,942.4 / 82,874.9 | 0.17 | 0.88x | 1.18x | displacement_up, bull_engulf |
| ETH | mixed (HH/LL) | 2,704.08 / 2,600.15 | 0.12 | 0.98x | 1.18x | bull_engulf |
| ZEC | mixed (HH/LL) | 1,539.7 / 1,456.92 | 0.45 | 2.25x | 1.18x | breakout_up, retest_up |
| XRP | mixed (HH/LL) | 1.5194 / 1.4517 | 0.27 | 1.54x | 1.05x | bull_engulf, breakout_up, retest_up |
| SOL | down (LH/LL) | 116.13 / 112.52 | 0.34 | 1.21x | 1.11x | bull_engulf, breakout_up, retest_up |
| BNB | mixed (HH/LL) | 777.62 / 763.04 | 0.21 | 0.57x | 0.98x | bear_engulf |
| UNI | down (LH/LL) | 9.401 / 8.787 | 0.41 | 0.44x | 0.96x | bull_engulf, bear_engulf |

## 0e. Candle evidence - RESEARCH EVIDENCE, NOT A SIGNAL
If you had entered at the NEXT candle's open after each pattern, with a stop 1 ATR away: how often did price reach +1R / +2R / +3R **after costs** before the stop (max 30 candles)? **Random** = the same test on random candles (same coins, same direction, 10x as many). **Verdict** compares +1R with random: 'beats chance' only if better by more than 2 standard errors. **Stopped** = the stop was hit within the time limit (it can happen after +1R was reached, so the columns can add up to more than 100%). Many rows are compared at once, so an occasional 'beats chance' can still be luck - and none of this includes the other rules a real strategy needs.

| TF | Pattern | Entries | +1R | +2R | +3R | Stopped | Random +1R | Random +2R | Verdict | Cost per trade |
|---|---|---|---|---|---|---|---|---|---|---|
| 4h | displacement_up | 375 | 48% | 34% | 27% | 79% | 43% | 30% | can't tell from chance | 0.13R |
| 4h | displacement_down | 308 | 49% | 32% | 22% | 75% | 48% | 32% | can't tell from chance | 0.08R |
| 4h | bull_engulf | 979 | 44% | 30% | 20% | 78% | 43% | 29% | can't tell from chance | 0.14R |
| 4h | bear_engulf | 1099 | 44% | 30% | 21% | 76% | 48% | 33% | worse than chance | 0.09R |
| 4h | bull_reject | 734 | 41% | 28% | 19% | 79% | 43% | 29% | can't tell from chance | 0.13R |
| 4h | bear_reject | 717 | 48% | 34% | 24% | 73% | 47% | 32% | can't tell from chance | 0.08R |
| 1h | displacement_up | 503 | 47% | 35% | 27% | 72% | 42% | 29% | beats chance | 0.29R |
| 1h | displacement_down | 343 | 38% | 24% | 15% | 83% | 37% | 23% | can't tell from chance | 0.20R |
| 1h | bull_engulf | 1364 | 41% | 29% | 22% | 75% | 42% | 29% | can't tell from chance | 0.34R |
| 1h | bear_engulf | 1532 | 39% | 25% | 18% | 79% | 37% | 24% | can't tell from chance | 0.20R |
| 1h | bull_reject | 1146 | 40% | 28% | 22% | 75% | 42% | 29% | can't tell from chance | 0.33R |
| 1h | bear_reject | 1068 | 35% | 23% | 17% | 83% | 37% | 24% | can't tell from chance | 0.19R |
| 30m | displacement_up | 497 | 41% | 31% | 26% | 76% | 41% | 29% | can't tell from chance | 0.35R |
| 30m | displacement_down | 323 | 40% | 24% | 14% | 83% | 36% | 22% | can't tell from chance | 0.22R |
| 30m | bull_engulf | 1402 | 40% | 28% | 20% | 76% | 40% | 28% | can't tell from chance | 0.39R |
| 30m | bear_engulf | 1451 | 35% | 22% | 15% | 82% | 36% | 21% | can't tell from chance | 0.24R |
| 30m | bull_reject | 1072 | 42% | 28% | 21% | 74% | 40% | 28% | can't tell from chance | 0.37R |
| 30m | bear_reject | 1136 | 37% | 23% | 16% | 81% | 36% | 21% | can't tell from chance | 0.23R |
| 15m | displacement_up | 373 | 35% | 26% | 19% | 82% | 33% | 23% | can't tell from chance | 0.48R |
| 15m | displacement_down | 366 | 35% | 21% | 14% | 84% | 35% | 22% | can't tell from chance | 0.33R |
| 15m | bull_engulf | 1333 | 36% | 25% | 17% | 79% | 33% | 23% | can't tell from chance | 0.58R |
| 15m | bear_engulf | 1307 | 35% | 24% | 15% | 79% | 35% | 22% | can't tell from chance | 0.34R |
| 15m | bull_reject | 1076 | 34% | 22% | 15% | 80% | 33% | 23% | can't tell from chance | 0.58R |
| 15m | bear_reject | 1163 | 35% | 22% | 15% | 81% | 36% | 22% | can't tell from chance | 0.33R |
| 5m | displacement_up | 418 | 34% | 22% | 18% | 84% | 31% | 22% | can't tell from chance | 0.81R |
| 5m | displacement_down | 342 | 28% | 17% | 12% | 86% | 31% | 20% | can't tell from chance | 0.44R |
| 5m | bull_engulf | 1365 | 30% | 21% | 16% | 81% | 30% | 22% | can't tell from chance | 0.81R |
| 5m | bear_engulf | 1294 | 31% | 19% | 12% | 84% | 30% | 19% | can't tell from chance | 0.50R |
| 5m | bull_reject | 1009 | 31% | 22% | 17% | 77% | 30% | 21% | can't tell from chance | 0.83R |
| 5m | bear_reject | 1168 | 34% | 20% | 13% | 82% | 30% | 19% | beats chance | 0.50R |

## 1. Market mood
- **BTC trend:** daily = **UP**, 4H = **UP**  (most coins follow BTC - trading against BTC's trend is harder)
- **Fear & Greed index:** 71 (Greed), yesterday 71  (extreme fear/greed = bigger, faster moves)

## 2. Signals right now
**No trade passes all the checks right now. That is normal - no trade is also a position.**

## 3. Strategy scoreboard (auto backtest)
WORKS = passed every test -> can give signals · WEAK = positive but not proven -> watch only · FAILS = ignored

| Strategy | TF | Status | Trades | Win % | Avg R/trade | PF | Train R | Unseen-test R | Avg hold | Live signals (avg R) | Why not |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bb_squeeze_breakout | 1h | **WEAK** | 108 | 57.4 | +0.011 | 1.02 | -0.044 | +0.160 | 8.9 h | 0 | avg +0.01R/trade; profit factor 1.02; not profitable in BOTH train and unseen test |
| donchian_breakout | 30m | **FAILS** | 196 | 54.1 | +0.090 | 1.18 | +0.205 | -0.123 | 4.9 h | 0 | not profitable in BOTH train and unseen test |
| donchian_breakout | 1h | **FAILS** | 184 | 50.5 | +0.004 | 1.01 | +0.017 | -0.020 | 11.5 h | 0 | avg +0.00R/trade; profit factor 1.01; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 4h | **FAILS** | 440 | 56.8 | -0.061 | 0.73 | -0.041 | -0.099 | 14.4 h | 0 | avg -0.06R/trade; profit factor 0.73; not profitable in BOTH train and unseen test |
| supertrend_flip | 1h | **FAILS** | 53 | 52.8 | -0.071 | 0.87 | -0.296 | +0.301 | 12.5 h | 0 | avg -0.07R/trade; profit factor 0.87; not profitable in BOTH train and unseen test |
| donchian_breakout | 4h | **FAILS** | 128 | 42.2 | -0.099 | 0.83 | -0.131 | -0.057 | 44.8 h | 0 | avg -0.10R/trade; profit factor 0.83; not profitable in BOTH train and unseen test |
| macd_trend_cross | 4h | **FAILS** | 124 | 42.7 | -0.144 | 0.77 | -0.238 | +0.032 | 40.8 h | 0 | avg -0.14R/trade; profit factor 0.77; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 30m | **FAILS** | 592 | 47.5 | -0.187 | 0.39 | -0.194 | -0.177 | 97 min | 0 | avg -0.19R/trade; profit factor 0.39; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 4h | **FAILS** | 83 | 45.8 | -0.188 | 0.68 | -0.157 | -0.235 | 36.0 h | 0 | avg -0.19R/trade; profit factor 0.68; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 1h | **FAILS** | 620 | 44.4 | -0.206 | 0.36 | -0.208 | -0.201 | 3.5 h | 0 | avg -0.21R/trade; profit factor 0.36; not profitable in BOTH train and unseen test |
| macd_trend_cross | 1h | **FAILS** | 159 | 46.5 | -0.220 | 0.66 | -0.227 | -0.206 | 10.7 h | 0 | avg -0.22R/trade; profit factor 0.66; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 15m | **FAILS** | 87 | 47.1 | -0.236 | 0.61 | -0.242 | -0.222 | 2.4 h | 0 | avg -0.24R/trade; profit factor 0.61; not profitable in BOTH train and unseen test |
| rsi2_dip_buy | 15m | **FAILS** | 635 | 37.5 | -0.241 | 0.32 | -0.249 | -0.226 | 49 min | 0 | avg -0.24R/trade; profit factor 0.32; not profitable in BOTH train and unseen test |
| trend_pullback | 4h | **FAILS** | 292 | 41.8 | -0.242 | 0.61 | -0.352 | -0.075 | 39.3 h | 0 | avg -0.24R/trade; profit factor 0.61; not profitable in BOTH train and unseen test |
| supertrend_flip | 30m | **FAILS** | 58 | 43.1 | -0.244 | 0.62 | -0.164 | -0.330 | 7.6 h | 0 | avg -0.24R/trade; profit factor 0.62; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 30m | **FAILS** | 110 | 40.0 | -0.245 | 0.62 | -0.332 | -0.093 | 4.0 h | 0 | avg -0.25R/trade; profit factor 0.62; not profitable in BOTH train and unseen test |
| trend_pullback | 30m | **FAILS** | 434 | 44.2 | -0.250 | 0.62 | -0.279 | -0.192 | 4.8 h | 0 | avg -0.25R/trade; profit factor 0.62; not profitable in BOTH train and unseen test |
| macd_trend_cross | 30m | **FAILS** | 146 | 46.6 | -0.269 | 0.57 | -0.253 | -0.305 | 5.9 h | 0 | avg -0.27R/trade; profit factor 0.57; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 30m | **FAILS** | 122 | 37.7 | -0.317 | 0.55 | -0.410 | -0.140 | 3.4 h | 0 | avg -0.32R/trade; profit factor 0.55; not profitable in BOTH train and unseen test |
| trend_pullback | 15m | **FAILS** | 548 | 44.5 | -0.329 | 0.53 | -0.366 | -0.257 | 2.3 h | 0 | avg -0.33R/trade; profit factor 0.53; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 1h | **FAILS** | 124 | 39.5 | -0.331 | 0.51 | -0.370 | -0.261 | 9.0 h | 0 | avg -0.33R/trade; profit factor 0.51; not profitable in BOTH train and unseen test |
| supertrend_flip | 4h | **FAILS** | 41 | 39.0 | -0.332 | 0.49 | -0.356 | -0.266 | 73.8 h | 0 | avg -0.33R/trade; profit factor 0.49; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 1h | **FAILS** | 251 | 40.2 | -0.343 | 0.51 | -0.285 | -0.450 | 5.5 h | 0 | avg -0.34R/trade; profit factor 0.51; not profitable in BOTH train and unseen test |
| trend_pullback | 1h | **FAILS** | 512 | 39.1 | -0.397 | 0.45 | -0.465 | -0.241 | 9.1 h | 0 | avg -0.40R/trade; profit factor 0.45; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 30m | **FAILS** | 268 | 38.4 | -0.403 | 0.45 | -0.338 | -0.552 | 2.6 h | 0 | avg -0.40R/trade; profit factor 0.45; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 15m | **FAILS** | 300 | 39.3 | -0.482 | 0.43 | -0.588 | -0.290 | 76 min | 0 | avg -0.48R/trade; profit factor 0.43; not profitable in BOTH train and unseen test |
| bb_squeeze_breakout | 15m | **FAILS** | 132 | 36.4 | -0.512 | 0.37 | -0.367 | -0.802 | 87 min | 0 | avg -0.51R/trade; profit factor 0.37; not profitable in BOTH train and unseen test |
| ema_9_21_cross | 5m | **FAILS** | 75 | 34.7 | -0.536 | 0.39 | -0.537 | -0.533 | 47 min | 0 | avg -0.54R/trade; profit factor 0.39; not profitable in BOTH train and unseen test |
| liquidity_sweep_reversal | 5m | **FAILS** | 305 | 28.5 | -0.853 | 0.23 | -0.936 | -0.684 | 25 min | 0 | avg -0.85R/trade; profit factor 0.23; not profitable in BOTH train and unseen test |

## 4. Live track record (real signals, checked after they happened)
- 0 signals logged, none finished yet. Give it a few weeks before trusting anything.

**Costs used in every backtest:** LONG = spot fees; SHORT = futures fees + funding (shorts are **futures only**). Details in `config.yaml` → `costs`.

---
*R = your risk on the trade. +2R means you made twice what you risked. Full explanation in the beginner guide.*