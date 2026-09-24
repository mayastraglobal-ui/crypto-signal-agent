# SMC / ICT research

Smart Money Concepts are treated as **testable hypotheses, not doctrine** (AGENT_PROMPT.md §9).
Every concept below is an exact rule on **closed candles**, stamped at the candle where it became
knowable. Labels come only from logged detections (`memory/smc_events.csv`), never drawn afterwards.
Code: `engine/smc.py` (version smc-1.0). Limits: `config.yaml` → `smc`. ATR = average candle size (14).

Status key: **NOT YET TESTED** · **RAW EVIDENCE** (candle-evidence table vs random entries only) ·
**TESTED** (vs control twin, out-of-sample, Phase 8+) · **ADDS EDGE** · **NO EDGE**.

## Definitions (smc-1.0)

| Concept | Exact rule | Status |
|---|---|---|
| Swing high / low | Highest high / lowest low with 3 candles on each side; known only 3 candles LATER (Phase 4) | NOT YET TESTED |
| Liquidity pools | Above confirmed swing highs, below confirmed swing lows; **equal highs/lows** = two swings within 0.1%; **PDH/PDL** = previous UTC day's high/low; **PWH/PWL** = previous week's high/low (Binance weeks start Monday 00:00 UTC). The newest 30 swing pools per side are kept | NOT YET TESTED |
| Liquidity sweep | The wick goes through a pool by ≥ 0.1×ATR and the candle **closes back inside**. Buy-side swept = bearish idea; sell-side swept = bullish idea. A pool is used up once price trades through it | RAW EVIDENCE |
| BOS | A close beyond the last confirmed swing in the trend direction. The first break in the data sets the trend | RAW EVIDENCE |
| CHoCH / MSS | The first close beyond the last swing **against** the trend, **with a displacement candle** in the last 3 candles. Without displacement it is logged as WEAK_BREAK and the trend does not change | RAW EVIDENCE |
| Fair Value Gap | Bullish: `low[i] > high[i-2]`; bearish: `high[i] < low[i-2]`; size ≥ 0.25×ATR. First retrace = first candle trading into it; filled = price trades through it | RAW EVIDENCE (first retrace) |
| Order block | The last opposite-colour candle within 10 candles before the displacement that caused a BOS/CHoCH (only breaks with displacement create one). OB_RETEST = first return into it. Invalid once a candle closes through it | NOT YET TESTED |
| Breaker | An invalidated order block, retested from the other side | NOT YET TESTED |
| Premium / discount | Position of the close in the range between the last confirmed swing high and swing low: above 50% = premium, below = discount | NOT YET TESTED |
| OTE | 62–79% retracement of the displacement leg (break candle extreme vs the extreme of the 10 candles before it) | NOT YET TESTED |
| Killzones (New York time, DST handled) | Asia 20:00–00:00 · London 02:00–05:00 · NY AM 07:00–10:00 · Silver Bullet 10:00–11:00; by the candle's OPEN time; timeframes up to 1H only | NOT YET TESTED |
| Power of 3 (AMD) | Consolidation within 5 candles before a sweep, then a CHoCH (with displacement) the opposite way within 10 candles | NOT YET TESTED |
| Inducement | **Not implemented** - research only until defined and validated (§9) | - |

## What must be proven before any SMC idea is used
- **Control twin:** the same strategy without the SMC filter; SMC is kept only if it adds out-of-sample edge (Phase 7/8).
- Segment results by killzone, regime, asset and direction (every logged event carries killzone and higher-timeframe regime).
- Known retail failure modes to test as filters: OBs drawn everywhere, ignoring HTF bias, no premium/discount filter, no session timing, no displacement, ignoring fees on low timeframes.

## Log
- 2026-09-24 · Phase 6 · definitions smc-1.0 built; sweeps, BOS, CHoCH and first FVG retrace added to the candle-evidence table (vs random entries, after costs). Live event log starts with the first live run (no backfill).
