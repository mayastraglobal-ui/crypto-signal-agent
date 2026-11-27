# Approval pack: donchian_breakout-VEXIT v1.0 4h

Written by the engine on 2026-11-27 09:00 UTC (AGENT_PROMPT.md section 21). Numbers only - the decision is yours.

**Question: Approve donchian_breakout-VEXIT v1.0 4h for live emails? (yes/no)**

**This is a LAB card** (`strategies_lab.yaml`, written by Claude's reviews). A lab card never sends emails and is never approved. To say yes: FIRST copy the card unchanged into `strategies.yaml` by pull request (same id and version - its results carry over), THEN add the line below.

To say yes, add this under `approvals:` in `config.yaml` (on GitHub: open the file, pencil icon, commit):
```
  - {strategy: donchian_breakout-VEXIT, version: "1.0", tf: 4h, date: 2026-11-27}
```
The next daily research run moves it to APPROVED. To undo, delete the line. Saying nothing = no.
**Check the trades before you say yes:**
- backtest chart (every trade on the candles, stop and targets, equity and drawdown): https://mayastraglobal-ui.github.io/crypto-signal-agent/chart.html#s=donchian_breakout-VEXIT&v=1.0&tf=4h
- TradingView: open https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/main/reports/pine/donchian_breakout-VEXIT_v1.0_4h.pine (`reports/pine/donchian_breakout-VEXIT_v1.0_4h.pine`), copy it into TradingView's Pine Editor and add it to a chart - it draws the same signals and trades

## 0. Bull vs bear (the engine's numbers only - Phase 18)
- Bull case: unseen part of the backtest (last 30%): +0.245R per trade over 277 trades; whole history: +0.263R per trade over 832 trades, profit factor 1.50; walk-forward: 5 of 5 time windows profitable, together +0.256R; costs +50%: +0.232R per trade; every parameter -20% / +20% stays profitable (12 variants); an edge on 7 coin(s): BNB, BTC, ETH, SOL, SUI, XRP, ZEC; paper trading: +0.51R per signal over 40 closed signals
- Bear case: worst drawdown in the backtest: 19.8R · wins 42% of trades; by bad luck alone (Monte Carlo): 95% worst drawdown 23.1R, expected worst losing streak 16 in a row; systematic loss tags: false_breakout, trend_reversal (487 losing trades)
- Risk manager: no veto (no high-impact event within 60 min; heat 0 of 3 open live positions; data GOOD, report 0.9 h old; day +0.0R / week +0.0R, no halt; 1 of 5 signal coins are in one of its regimes on 4H now (ZEC))
- A veto means "not now": wait until the risk manager has no veto before you say yes. No veto is never a reason to say yes - the decision stays yours.

## 1. Definition and lineage
- family: breakout · gate: trend · regimes: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION, COMPRESSION
- hypothesis: One change to donchian_breakout@1.0: targets 2R / 3R (50 / 50) instead of a first target below 2R. It should keep the edge of donchian_breakout@1.0 and remove part of its losses; tested because it was the strongest BACKTESTING cell this week.
- source: engine variant search: one change to donchian_breakout@1.0
- long: htf_up; close > prev(highest(high,20)); volume > vol_sma(20) * 1.5; adx(14) > 20
- short: htf_down; close < prev(lowest(low,20)); volume > vol_sma(20) * 1.5; adx(14) > 20
- stop: method atr, atr 2.0 · targets: long 2R / 3R, short 2R / 3R, split 0.5 / 0.5 · 5m confirmation: no
- lineage: v1.0 first tested 2026-09-27 (PAPER_TRADING)
- edge (why it should work - a hypothesis; sections 2-7 test it): Type: forced_flow · Works in: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION, COMPRESSION · Who pays: traders fading the breakout (short at the range top) whose stops then add fuel to the move · Mechanism: a close outside a 20-candle range with 1.5x volume marks new participation; trend-following has the longest published record of the idea families · Fails when: choppy ranges and low volume: most breakouts fall back inside · Kill rule: retired by the engine's paper rules (last 20 paper signals below -0.10R or 8R drawdown), or FAILED when the unseen-data part of the backtest turns negative

## 2. Backtest (Layers A / B)
- Layer B, whole history: 832 trades · avg +0.263R · win rate 42% · profit factor 1.50 · max drawdown 19.8R
- Layer B, develop part (first 70%): 555 trades · avg +0.272R · win rate 42% · profit factor 1.53 · max drawdown 16.8R
- Layer B, unseen part (last 30%): 277 trades · avg +0.245R · win rate 41% · profit factor 1.45 · max drawdown 16.9R
- long / short: +0.282R (445) / +0.241R (387)
- coins with an edge: BNB, BTC, ETH, SOL, SUI, XRP, ZEC
- Layer A (last 15 days): 12 trades, avg +0.759R

## 3. Walk-forward (Layer C)
- 5 of 5 windows profitable, all judged windows together +0.256R over 757 trades - passed
  - window 0: 75 trades, +0.333R (warm-up)
  - window 1: 111 trades, +0.566R (profitable)
  - window 2: 160 trades, +0.233R (profitable)
  - window 3: 129 trades, +0.178R (profitable)
  - window 4: 175 trades, +0.056R (profitable)
  - window 5: 182 trades, +0.335R (profitable)

## 4. Paper trading
- 40 closed paper signals, average +0.51R, last 20 average +0.36R, drawdown 8.0R
- backtest on unseen data +0.24R vs paper +0.51R (allowed gap 0.30R)

## 5. Control twin (the same idea without its special ingredient)
- none: too few trades to compare

## 6. Sensitivity (every parameter -20% / +20%)
- stable: every variant stays profitable · worst: stop atr 2.0→1.6 +0.166R
  - n 20→16: 840 trades, +0.258R
  - vol_x 1.5→1.2: 957 trades, +0.246R
  - adx_min 20→16: 906 trades, +0.259R
  - exit_n 10→8: 839 trades, +0.239R
  - stop atr 2.0→1.6: 935 trades, +0.166R
  - time_stop_bars 60→48: 833 trades, +0.261R
  - n 20→24: 824 trades, +0.273R
  - vol_x 1.5→1.8: 701 trades, +0.284R
  - adx_min 20→24: 738 trades, +0.266R
  - exit_n 10→12: 830 trades, +0.259R
  - stop atr 2.0→2.4: 772 trades, +0.295R
  - time_stop_bars 60→72: 830 trades, +0.261R

## 6b. Rule significance (the card with ONE entry rule removed at a time)
- without rule 1 (htf_up / htf_down): 1146 trades, +0.206R - the rule improves the result
- without rule 2 (close > prev(highest(high,20)) / close < prev(lowest(low,20))): 1393 trades, +0.170R - the rule improves the result
- without rule 3 (volume > vol_sma(20) * 1.5 / volume > vol_sma(20) * 1.5): 1052 trades, +0.226R - the rule improves the result
- without rule 4 (adx(14) > 20 / adx(14) > 20): 945 trades, +0.250R - the rule improves the result

## 7. Cost stress test
- fees, slippage and funding +50%: 832 trades · avg +0.232R · win rate 41% · profit factor 1.43 · max drawdown 21.8R
- fees, slippage and funding +100% (shown only, not a gate): 832 trades · avg +0.209R · win rate 40% · profit factor 1.38 · max drawdown 26.5R
- median cost per trade: 0.039R

## 8. Risk metrics
- max drawdown (backtest): 19.8R · average hold 15 candles
- live risk per trade: 0.5% of the account for the first 30 days, then at most 1% (risk engine, section 15)
- Monte Carlo (1000 random orders of the same 832 trades): 95% worst drawdown 23.1R (median 15.3R, as it happened 17.9R)
- **expected worst losing streak: 16 losses in a row** (95% of the random orders stay at or below it; median 11, as it happened 11) - expect it before you judge the strategy broken
- family table (trend group, active mode): verdict PAPER_TRADING (old rule: BACKTESTING)
  - recovery factor 11.08 (net +218.8R / max drawdown 19.8R) · Monte Carlo 95% worst drawdown per 100 trades 16.3R · longest drawdown 430 days (13% of the tested period)
  - **if approved, suspended at a live drawdown of 16.3R; paper retired at 16.3R** (own Monte Carlo 95% worst drawdown per 100 trades (cap 17R))
- lookahead / recursive check: passed

## 9. Why it loses (failure attribution)
- 487 losing / 345 winning backtest trades; systematic tags: false_breakout, trend_reversal
  - overextended_entry: 435 losers (89% of losses)
  - late_entry: 321 losers (66% of losses)
  - false_breakout: 311 losers (64% of losses)
  - no_displacement: 156 losers (32% of losses)
  - regime_mismatch: 133 losers (27% of losses)
  - stop_too_tight: 102 losers (21% of losses)
  - Sample: 832 trades, +0.26R per trade - clearly above zero.
  - Regime: profitable in every regime with 10+ trades (EXPANSION, STRONG_BEAR, STRONG_BULL, WEAK_BEAR, WEAK_BULL).
  - Timing: losers rarely went our way (median best point +0.47R).
  - Stop / target: stopped out and then TP1 reached anyway in 21% of losses; target nearly reached (≥ 80%) in 7%. Measured stop changes (±20% test): stop atr 2.0→1.6 → +0.17R; stop atr 2.0→2.4 → +0.29R.
  - Costs: +0.32R per trade before fees and slippage, +0.26R after.
  - Other timeframes: best is 1h at -0.02R per trade.

## 10. Known limitations
- backtests and paper results are history, not a promise; the future can differ
- the agent never trades: real fills, slippage and funding can be worse than assumed
- known weaknesses (card): Many false breakouts in chop; wide stops; most of the profit comes from a few big trends.
- history starts 2017-10-09 - check it covers a bull and a bear market

Research signal. Not financial advice.
