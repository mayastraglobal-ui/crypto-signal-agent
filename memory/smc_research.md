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

## SMC strategies S5-S8 (Phase 7, strategy spec v3 - rules in `strategies.yaml`)
All four start as **FORMALIZED v1.0, NOT YET TESTED on live data**. Each has a control twin with the same gates,
regimes, exits and hold time but without the SMC ingredient. Phase 10 adds **S5-S8 -5M** (new ids, v1.0): the
same rules + the section 8 5-minute entry confirmation, each tested against its plain version (same period,
same 5m bars) - NOT YET TESTED.

| Strategy | Timeframes | Setup | Stop / targets | Control twin drops |
|---|---|---|---|---|
| S5-SWEEP-MSS-FVG | 30m, 15m | sweep ≤ 20 candles ago → CHoCH (not before the sweep) ≤ 10 candles ago → first retrace into a gap | beyond the sweep extreme + 0.2 ATR (max 3 ATR); target = next opposite pool, must be ≥ 2R | sweep, CHoCH, gap (entry on any displacement candle, stop beyond the 10-candle low/high) |
| S6-OB-FVG | 15m | newest active **4H** order block (from closed 4H candles) sits in the discount half of the 4H range, price traded into it within 20 candles, 15m CHoCH now | beyond the 10-candle low/high + 0.2 ATR (max 3 ATR); TP1 2R, TP2 max(3R, next pool) | the 4H order-block / discount filter |
| S7-SILVER-BULLET | 15m | inside London / NY AM / Silver Bullet: sweep ≤ 8 candles ago → displacement after it → first retrace into a gap | as S5 (pool ≥ 2R) | the killzone time filter |
| S8-PDH-PDL-SWEEP | 1H, 30m | the candle sweeps the prior-day low (high) and closes back inside the prior-day range | beyond the sweep extreme + 0.2 ATR; TP1 = prior-day middle (must be ≥ 1R - our assumption), TP2 = the opposite prior-day extreme | prior-day level (uses a plain 20-candle low/high) |

Gate types: S5-S7 = trend (2 of 1D/4H/1H + weekly veto); S8 = reversal (2 of 1D/4H/1H, no weekly veto).

## What must be proven before any SMC idea is used
- **Control twin:** the same strategy without the SMC filter; SMC is kept only if it adds out-of-sample edge (Phase 7/8).
- Segment results by killzone, regime, asset and direction (every logged event carries killzone and higher-timeframe regime).
- Known retail failure modes to test as filters: OBs drawn everywhere, ignoring HTF bias, no premium/discount filter, no session timing, no displacement, ignoring fees on low timeframes.

## Log
- 2026-09-24 · Phase 6 · definitions smc-1.0 built; sweeps, BOS, CHoCH and first FVG retrace added to the candle-evidence table (vs random entries, after costs). Live event log starts with the first live run (no backfill).
- 2026-09-24 · Phase 7 · S5-S8 v1.0 and their control twins written as spec v3 cards; new per-candle SMC context (dealing range position, active order blocks, prior-day sweeps, sweep extremes, nearest pools, killzones) and 4H context on lower timeframes, all known at candle close. Twin comparison shown in report section 3b.

### Liquidity sweeps vs stop-loss cascades - the evidence points both ways
- timestamp: 2026-09-27 02:00 UTC · source: Claude weekly research 2026-09-27; https://www.newyorkfed.org/research/staff_reports/sr150.html · evidence: RESEARCH_FINDING: Osler (NY Fed Staff Report 150) on currency stop-loss orders, plus the engine's BACKTEST numbers quoted from the fact sheet · confidence: medium · strategy: S8-PDH-PDL-SWEEP, liquidity_sweep_reversal, S5-SWEEP-MSS-FVG, S7-SILVER-BULLET · asset: all · timeframe: intraday · regime: - · review: 2026-12-26
  - ICT / SMC claim: price runs the stops resting beyond an obvious high / low (a 'liquidity sweep'), then reverses.
  - what the source shows: stop-loss orders do cluster and do move price - but the move ACCELERATES through the cluster (positive feedback, stronger and longer-lasting than take-profit orders). That supports 'stops matter', not 'sweeps reverse'.
  - our BACKTEST numbers: S8-PDH-PDL-SWEEP 30m -0.53R over 98 trades and does not beat its control twin; S8-PDH-PDL-SWEEP-noSMC 30m -0.45R over 518 trades; liquidity_sweep_reversal loses on 5m (374 trades, -1.14R), 15m (471, -0.44R), 30m (272, -0.51R) and 1h (241, -0.24R); the 'sweep_continued' loss tag is systematic in 2 tests.
  - why retail traders fail with it: every swing high looks like 'liquidity' after the fact; they fade the sweep at the moment stop orders are still pushing price; they put their own stop just beyond the sweep, where the next cluster sits.
  - status: unproven; no SMC card has beaten its control twin so far.

### Fair value gaps vs order flow imbalance - a gap shows where flow was one-sided, not where price must return
- timestamp: 2026-10-11 04:00 UTC · source: Claude weekly research 2026-10-11; https://arxiv.org/abs/1011.6402 · evidence: RESEARCH_FINDING: Cont, Kukanov, Stoikov (J. Financial Econometrics 2014) on order flow imbalance, plus the engine's BACKTEST numbers from memory/strategy_registry.csv (checked 2026-10-11 00:58 UTC) · confidence: medium · strategy: S5-SWEEP-MSS-FVG, S6-OB-FVG (+ -5M and -noSMC twins) · asset: all · timeframe: 15m, 30m · regime: - · review: 2027-01-09
  - ICT / SMC claim: a fair value gap (three candles where the wicks of candle 1 and 3 do not overlap) is an 'imbalance' that price tends to come back to and fill, and the fill is an entry with the trend.
  - what the source shows: one-sided order flow moves price, linearly, and more where the book is thin. That explains how a gap is made. It does not show that price returns to it later, or that a return gives an edge.
  - our BACKTEST numbers: S6-OB-FVG 15m 0 trades; S6-OB-FVG-noSMC 15m FAILED, 95 trades, -0.147R; S5-SWEEP-MSS-FVG 15m 12 trades -0.839R and 30m 9 trades -0.653R vs its noSMC twin 29 trades +0.074R and 13 trades -0.023R. The fact sheet says 'too few trades vs its twin' for the -5M cards. No FVG card has a sample big enough to judge.
  - why retail traders fail with it: gaps appear on every timeframe, so there is always one to 'justify' a trade; many gaps are never filled in a strong trend; the stop goes just past the gap, where a normal pullback reaches; on 5m-15m the stop is tight, so fees are a big share of R.
  - status: unproven; keep testing against the twins; no new card.

### Order blocks vs limit-order depth - a level shows where orders rest, not which way price goes
- timestamp: 2026-10-18 04:00 UTC · source: Claude weekly research 2026-10-18; https://ideas.repec.org/a/oup/rfinst/v17y2004i4p1043-1071.html; https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.html · evidence: RESEARCH_FINDING: Kavajecz and Odders-White (RFS 2004, US stocks) and Osler (NY Fed SR 125, currencies), plus the engine's BACKTEST numbers from memory/strategy_registry.csv (checked 2026-10-18 01:12 UTC) · confidence: medium · strategy: S6-OB-FVG, S5-SWEEP-MSS-FVG (+ -5M and -noSMC twins) · asset: all · timeframe: 15m, 30m · regime: - · review: 2027-01-16
  - ICT / SMC claim: an order block (the last opposite candle before a strong move) marks where 'institutions' placed orders; price returns to it and reacts in the direction of the original move.
  - what the sources show: support and resistance levels do coincide with peaks in resting limit-order depth, but technical rules only LOCATE depth that is already there. Osler: orders cluster at round numbers (take-profit = reversal at the level) and just beyond them (stop-loss = acceleration through it). So a level can stop price OR speed it up; the level alone does not say which.
  - our BACKTEST numbers: S6-OB-FVG 15m 0 trades; S6-OB-FVG-noSMC 15m FAILED, 94 trades, -0.159R; S5-SWEEP-MSS-FVG 15m 12 trades -0.839R, 30m 9 trades -0.653R (twin noSMC 29 trades +0.074R and 13 trades -0.023R). Too few trades to judge the SMC ingredient.
  - why retail traders fail with it: order blocks are drawn after the move, so every chart has one; they enter at the block with a stop just beyond it, exactly where Osler finds stop orders cluster; they read a level as a direction.
  - status: unproven; keep testing against the twins.

### Kill zones and the Silver Bullet - a fixed clock window is only as good as the hours that really behave differently
- timestamp: 2026-10-25 04:00 UTC · source: Claude weekly research 2026-10-25; https://ideas.repec.org:443/a/eee/ecofin/v62y2022ics1062940822000833.html · evidence: RESEARCH_FINDING: Wen, Bouri, Xu, Zhao (2022), abstract only, plus the engine's BACKTEST line from the fact sheet · confidence: low · strategy: S7-SILVER-BULLET · asset: BTC · timeframe: intraday · regime: - · review: 2027-01-23
  - ICT / SMC claim: price is "delivered" in fixed daily windows (kill zones, the one-hour Silver Bullet), so entries inside them have a better chance than the same setup at another hour.
  - what the source shows: Bitcoin has real intraday patterns, both momentum and reversal, and which one appears changes with big price jumps, FOMC announcements and liquidity levels. The abstract does not give the hours, so it neither confirms nor rejects the ICT windows. It does say the pattern is not fixed: it moves with conditions.
  - our BACKTEST numbers: S7-SILVER-BULLET-5M 15m: "too few trades vs its twin" (fact sheet, 2026-10-25). Nothing to judge yet.
  - why retail traders fail with it: a window with few trades hides that the sample is small; the window is learned from charts after the fact; the rule ignores that the same hour behaves differently on FOMC days or in thin liquidity (the paper's point); on 5m the fees are a large share of R.
  - status: unproven; keep testing against the twin. The matching hypothesis is in memory/experiments.md ('shock alarm moves reverse more often when the jump is large').
