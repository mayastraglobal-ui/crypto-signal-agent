# Approval pack: donchian_breakout-VEXIT-FDISP v1.0 4h

Written by the engine on 2026-11-22 07:23 UTC (AGENT_PROMPT.md section 21). Numbers only - the decision is yours.

**Question: Approve donchian_breakout-VEXIT-FDISP v1.0 4h for live emails? (yes/no)**

**This is a LAB card** (`strategies_lab.yaml`, written by Claude's reviews). A lab card never sends emails and is never approved. To say yes: FIRST copy the card unchanged into `strategies.yaml` by pull request (same id and version - its results carry over), THEN add the line below.

To say yes, add this under `approvals:` in `config.yaml` (on GitHub: open the file, pencil icon, commit):
```
  - {strategy: donchian_breakout-VEXIT-FDISP, version: "1.0", tf: 4h, date: 2026-11-22}
```
The next daily research run moves it to APPROVED. To undo, delete the line. Saying nothing = no.
**Check the trades before you say yes:**
- backtest chart (every trade on the candles, stop and targets, equity and drawdown): https://mayastraglobal-ui.github.io/crypto-signal-agent/chart.html#s=donchian_breakout-VEXIT-FDISP&v=1.0&tf=4h
- TradingView: open https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/main/reports/pine/donchian_breakout-VEXIT-FDISP_v1.0_4h.pine (`reports/pine/donchian_breakout-VEXIT-FDISP_v1.0_4h.pine`), copy it into TradingView's Pine Editor and add it to a chart - it draws the same signals and trades

## 0. Bull vs bear (the engine's numbers only - Phase 18)
- Bull case: unseen part of the backtest (last 30%): +0.268R per trade over 221 trades; whole history: +0.273R per trade over 637 trades, profit factor 1.51; walk-forward: 4 of 5 time windows profitable, together +0.277R; costs +50%: +0.238R per trade; every parameter -20% / +20% stays profitable (12 variants); an edge on 7 coin(s): BNB, BTC, ETH, SOL, SUI, XRP, ZEC; paper trading: +0.91R per signal over 21 closed signals
- Bear case: worst drawdown in the backtest: 22.8R · wins 42% of trades; by bad luck alone (Monte Carlo): 95% worst drawdown 21.9R, expected worst losing streak 15 in a row; systematic loss tags: false_breakout, trend_reversal (367 losing trades)
- Risk manager: no veto (no high-impact event within 60 min; heat 0 of 3 open live positions; data GOOD, report 0.2 h old; day +0.0R / week +0.0R, no halt; 5 of 5 signal coins are in one of its regimes on 4H now (BTC, ETH, SOL, XRP, ZEC))
- A veto means "not now": wait until the risk manager has no veto before you say yes. No veto is never a reason to say yes - the decision stays yours.

## 1. Definition and lineage
- family: breakout · gate: trend · regimes: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION, COMPRESSION
- hypothesis: donchian_breakout-VEXIT@1.0 loses on false_breakout (-0.36R a trade with it, +0.43R without). One change - a strong candle (displacement) in the trade direction within the last 3 candles - should remove part of those losses and keep the rest.
- source: engine failure lab: a repair of donchian_breakout-VEXIT@1.0 for its loss tag false_breakout
- long: htf_up; close > prev(highest(high,20)); volume > vol_sma(20) * 1.5; adx(14) > 20; within(displacement_up, 3)
- short: htf_down; close < prev(lowest(low,20)); volume > vol_sma(20) * 1.5; adx(14) > 20; within(displacement_down, 3)
- stop: method atr, atr 2.0 · targets: long 2R / 3R, short 2R / 3R, split 0.5 / 0.5 · 5m confirmation: no
- lineage: v1.0 first tested 2026-10-21 (PAPER_TRADING)
- edge (why it should work - a hypothesis; sections 2-7 test it): Type: forced_flow · Works in: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION, COMPRESSION · Who pays: traders fading the breakout (short at the range top) whose stops then add fuel to the move · Mechanism: a close outside a 20-candle range with 1.5x volume marks new participation; trend-following has the longest published record of the idea families · Fails when: choppy ranges and low volume: most breakouts fall back inside · Kill rule: retired by the engine's paper rules (last 20 paper signals below -0.10R or 8R drawdown), or FAILED when the unseen-data part of the backtest turns negative

## 2. Backtest (Layers A / B)
- Layer B, whole history: 637 trades · avg +0.273R · win rate 42% · profit factor 1.51 · max drawdown 22.8R
- Layer B, develop part (first 70%): 416 trades · avg +0.276R · win rate 43% · profit factor 1.53 · max drawdown 10.7R
- Layer B, unseen part (last 30%): 221 trades · avg +0.268R · win rate 42% · profit factor 1.49 · max drawdown 15.9R
- long / short: +0.289R (346) / +0.254R (291)
- coins with an edge: BNB, BTC, ETH, SOL, SUI, XRP, ZEC
- Layer A (last 15 days): 14 trades, avg +0.947R

## 3. Walk-forward (Layer C)
- 4 of 5 windows profitable, all judged windows together +0.277R over 580 trades - passed
  - window 0: 57 trades, +0.232R (warm-up)
  - window 1: 83 trades, +0.621R (profitable)
  - window 2: 124 trades, +0.257R (profitable)
  - window 3: 91 trades, +0.237R (profitable)
  - window 4: 132 trades, -0.015R (losing)
  - window 5: 150 trades, +0.385R (profitable)

## 4. Paper trading
- 21 closed paper signals, average +0.91R, last 20 average +1.01R, drawdown 3.2R
- backtest on unseen data +0.27R vs paper +0.91R (allowed gap 0.30R)

## 5. Control twin (the same idea without its special ingredient)
- none: too few trades to compare

## 6. Sensitivity (every parameter -20% / +20%)
- stable: every variant stays profitable · worst: stop atr 2.0→1.6 +0.186R
  - n 20→16: 642 trades, +0.272R
  - vol_x 1.5→1.2: 693 trades, +0.286R
  - adx_min 20→16: 691 trades, +0.265R
  - exit_n 10→8: 642 trades, +0.237R
  - stop atr 2.0→1.6: 712 trades, +0.186R
  - time_stop_bars 60→48: 638 trades, +0.271R
  - n 20→24: 632 trades, +0.279R
  - vol_x 1.5→1.8: 553 trades, +0.299R
  - adx_min 20→24: 568 trades, +0.261R
  - exit_n 10→12: 636 trades, +0.271R
  - stop atr 2.0→2.4: 600 trades, +0.324R
  - time_stop_bars 60→72: 636 trades, +0.269R

## 6b. Rule significance (the card with ONE entry rule removed at a time)
- without rule 1 (htf_up / htf_down): 882 trades, +0.242R - the rule improves the result
- without rule 2 (close > prev(highest(high,20)) / close < prev(lowest(low,20))): 809 trades, +0.261R - the rule improves the result
- without rule 3 (volume > vol_sma(20) * 1.5 / volume > vol_sma(20) * 1.5): 711 trades, +0.266R - the rule improves the result
- without rule 4 (adx(14) > 20 / adx(14) > 20): 721 trades, +0.240R - the rule improves the result
- without rule 5 (within(displacement_up, 3) / within(displacement_down, 3)): 829 trades, +0.268R - the rule improves the result

## 7. Cost stress test
- fees, slippage and funding +50%: 638 trades · avg +0.238R · win rate 41% · profit factor 1.43 · max drawdown 23.3R
- fees, slippage and funding +100% (shown only, not a gate): 638 trades · avg +0.214R · win rate 41% · profit factor 1.38 · max drawdown 25.4R
- median cost per trade: 0.039R

## 8. Risk metrics
- max drawdown (backtest): 22.8R · average hold 15 candles
- live risk per trade: 0.5% of the account for the first 30 days, then at most 1% (risk engine, section 15)
- Monte Carlo (1000 random orders of the same 637 trades): 95% worst drawdown 21.9R (median 14.4R, as it happened 18.6R)
- **expected worst losing streak: 15 losses in a row** (95% of the random orders stay at or below it; median 10, as it happened 10) - expect it before you judge the strategy broken
- family table (trend group, active mode): verdict PAPER_TRADING (old rule: BACKTESTING)
  - recovery factor 7.64 (net +174.0R / max drawdown 22.8R) · Monte Carlo 95% worst drawdown per 100 trades 15.8R · longest drawdown 529 days (16% of the tested period)
  - **if approved, suspended at a live drawdown of 15.8R; paper retired at 15.8R** (own Monte Carlo 95% worst drawdown per 100 trades (cap 17R))
- lookahead / recursive check: passed

## 9. Why it loses (failure attribution)
- 367 losing / 270 winning backtest trades; systematic tags: false_breakout, trend_reversal
  - overextended_entry: 350 losers (95% of losses)
  - late_entry: 269 losers (73% of losses)
  - false_breakout: 225 losers (61% of losses)
  - volatility_spike: 90 losers (24% of losses)
  - stop_too_tight: 83 losers (23% of losses)
  - regime_mismatch: 78 losers (21% of losses)
  - Sample: 637 trades, +0.27R per trade - clearly above zero.
  - Regime: profitable in EXPANSION, STRONG_BULL, WEAK_BEAR, WEAK_BULL; losing in STRONG_BEAR.
  - Timing: losers rarely went our way (median best point +0.48R).
  - Stop / target: stopped out and then TP1 reached anyway in 23% of losses; target nearly reached (≥ 80%) in 6%. Measured stop changes (±20% test): stop atr 2.0→1.6 → +0.19R; stop atr 2.0→2.4 → +0.32R.
  - Costs: +0.33R per trade before fees and slippage, +0.27R after.
  - Other timeframes: best is 1h at +0.02R per trade.

## 10. Known limitations
- backtests and paper results are history, not a promise; the future can differ
- the agent never trades: real fills, slippage and funding can be worse than assumed
- known weaknesses (card): Many false breakouts in chop; wide stops; most of the profit comes from a few big trends.
- history starts 2017-10-12 - check it covers a bull and a bear market

Research signal. Not financial advice.
