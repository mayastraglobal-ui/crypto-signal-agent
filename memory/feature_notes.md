# Feature notes

Which features exist, exactly how they are defined, and - once tested - whether they add value
(AGENT_PROMPT.md section 7). **More indicators is not better analysis.** A feature earns its place only
if it adds out-of-sample value, is not redundant with another feature, and we know in which regimes it helps.

Status key: **NOT YET TESTED** (defined only) · **RAW EVIDENCE** (candle-evidence table only, no strategy rules)
· **TESTED** (out-of-sample, Phase 8+) · **REDUNDANT** · **REJECTED**.
All thresholds live in `config.yaml` → `features`. Code: `engine/features.py`. ATR = average candle size (14).

| Feature | Definition (closed candles only) | Status | Evidence |
|---|---|---|---|
| body_pct, upper/lower_wick_pct | body / range, wicks / range | NOT YET TESTED | - |
| close_loc | (close - low) / range: 0 = closed at the low, 1 = at the high | NOT YET TESTED | - |
| consec_up / consec_down | closes in a row above / below the previous close | NOT YET TESTED | - |
| range_atr, expansion, contraction | range / ATR of the previous candle; ≥ 1.5 expansion, ≤ 0.5 contraction | NOT YET TESTED | - |
| atr_ratio | ATR / its 100-candle median | NOT YET TESTED | - |
| momentum_persist | share of the last 10 closes that were up | NOT YET TESTED | - |
| rel_vol | volume / mean of the previous 20 candles | NOT YET TESTED | - |
| vol_accel | mean volume of the last 3 candles / the 3 before | NOT YET TESTED | - |
| displacement_up / down | range ≥ 1.5×ATR, body ≥ 60% of range, rel_vol ≥ 1.3 | RAW EVIDENCE | `reports/feature_evidence.json` |
| bull_engulf / bear_engulf | body covers the previous opposite candle's body and is bigger | RAW EVIDENCE | `reports/feature_evidence.json` |
| bull_reject / bear_reject (pin bar) | wick ≥ 2×body and ≥ 60% of range; close in the far third | RAW EVIDENCE | `reports/feature_evidence.json` |
| swing_high / swing_low | highest high / lowest low with 3 candles each side; known only 3 candles LATER | NOT YET TESTED | - |
| structure (HH/HL/LH/LL) | labels of the last confirmed swing high and low; up = HH+HL, down = LH+LL | NOT YET TESTED | - |
| bull_div / bear_div | at a confirmed swing: price makes a lower low (higher high) but RSI(14) does not | NOT YET TESTED | - |
| support / resistance (+ distance, touches) | nearest confirmed swing low below / high above the close; touches within 0.25 ATR | NOT YET TESTED | - |
| consolidation | 20-candle range ≤ 3×ATR | NOT YET TESTED | - |
| breakout_up / down | close beyond the previous 20-candle high / low | NOT YET TESTED | - |
| retest_up / down | within 5 candles, back to the broken level (± 0.25 ATR) and closes beyond it | NOT YET TESTED | - |
| failed_breakout_up / down | within 3 candles, closes back inside the broken level | NOT YET TESTED | - |
| impulse_up / down | move ≥ 2.5×ATR within 5 candles | NOT YET TESTED | - |
| pullback_up / down | gives back 38.2–61.8% of the last impulse leg without breaking its start | NOT YET TESTED | - |
| stoch_rsi_k / d | Stochastic RSI (14, 14, 3, 3) | NOT YET TESTED | - |
| roc | 10-candle rate of change, % | NOT YET TESTED | - |
| keltner_mid / upper / lower | EMA(20) ± 2 × ATR(10) | NOT YET TESTED | - |
| vwap | volume-weighted average price, resets each UTC day (below 1D only) | NOT YET TESTED | - |
| obv | on-balance volume | NOT YET TESTED | - |
| volume profile | not built: Binance's free data does not include the trades needed | - | - |

## Log
- 2026-09-24 · Phase 4 · all features defined; candle evidence tool started (patterns vs random entries,
  after costs, research evidence only). First offline check on random synthetic data: every pattern
  "can't tell from chance" - as it should be on random data.
