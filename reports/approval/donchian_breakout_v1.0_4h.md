# Approval pack: donchian_breakout v1.0 4h

Written by the engine on 2026-11-22 07:23 UTC (AGENT_PROMPT.md section 21). Numbers only - the decision is yours.

**Question: Approve donchian_breakout v1.0 4h for live emails? (yes/no)**

To say yes, add this under `approvals:` in `config.yaml` (on GitHub: open the file, pencil icon, commit):
```
  - {strategy: donchian_breakout, version: "1.0", tf: 4h, date: 2026-11-22}
```
The next daily research run moves it to APPROVED. To undo, delete the line. Saying nothing = no.
**Check the trades before you say yes:**
- backtest chart (every trade on the candles, stop and targets, equity and drawdown): https://mayastraglobal-ui.github.io/crypto-signal-agent/chart.html#s=donchian_breakout&v=1.0&tf=4h
- TradingView: open https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/main/reports/pine/donchian_breakout_v1.0_4h.pine (`reports/pine/donchian_breakout_v1.0_4h.pine`), copy it into TradingView's Pine Editor and add it to a chart - it draws the same signals and trades

## 0. Bull vs bear (the engine's numbers only - Phase 18)
- Bull case: unseen part of the backtest (last 30%): +0.158R per trade over 289 trades; whole history: +0.164R per trade over 856 trades, profit factor 1.38; walk-forward: 5 of 5 time windows profitable, together +0.162R; costs +50%: +0.130R per trade; every parameter -20% / +20% stays profitable (12 variants); an edge on 6 coin(s): BNB, BTC, ETH, SOL, XRP, ZEC; paper trading: +0.25R per signal over 24 closed signals
- Bear case: worst drawdown in the backtest: 16.3R · wins 56% of trades; by bad luck alone (Monte Carlo): 95% worst drawdown 21.9R, expected worst losing streak 10 in a row; systematic loss tags: false_breakout, trend_reversal, regime_mismatch, stop_too_tight (376 losing trades)
- Risk manager: no veto (no high-impact event within 60 min; heat 0 of 3 open live positions; data GOOD, report 0.2 h old; day +0.0R / week +0.0R, no halt; 5 of 5 signal coins are in one of its regimes on 4H now (BTC, ETH, SOL, XRP, ZEC))
- A veto means "not now": wait until the risk manager has no veto before you say yes. No veto is never a reason to say yes - the decision stays yours.

## 1. Definition and lineage
- family: breakout · gate: trend · regimes: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION, COMPRESSION
- hypothesis: A close beyond the 20-candle range with 1.5x volume and ADX > 20 starts a move that is worth following.
- source: Existing library (before v3), re-versioned under spec v3
- long: htf_up; close > prev(highest(high,20)); volume > vol_sma(20) * 1.5; adx(14) > 20
- short: htf_down; close < prev(lowest(low,20)); volume > vol_sma(20) * 1.5; adx(14) > 20
- stop: method atr, atr 2.0 · targets: config default · 5m confirmation: no
- lineage: v1.0 first tested 2026-09-24 (PAPER_TRADING)
- edge (why it should work - a hypothesis; sections 2-7 test it): Type: forced_flow · Works in: STRONG_BULL, WEAK_BULL, STRONG_BEAR, WEAK_BEAR, EXPANSION, COMPRESSION · Who pays: traders fading the breakout (short at the range top) whose stops then add fuel to the move · Mechanism: a close outside a 20-candle range with 1.5x volume marks new participation; trend-following has the longest published record of the idea families · Fails when: choppy ranges and low volume: most breakouts fall back inside · Kill rule: retired by the engine's paper rules (last 20 paper signals below -0.10R or 8R drawdown), or FAILED when the unseen-data part of the backtest turns negative

## 2. Backtest (Layers A / B)
- Layer B, whole history: 856 trades · avg +0.164R · win rate 56% · profit factor 1.38 · max drawdown 16.3R
- Layer B, develop part (first 70%): 567 trades · avg +0.166R · win rate 57% · profit factor 1.39 · max drawdown 15.6R
- Layer B, unseen part (last 30%): 289 trades · avg +0.158R · win rate 55% · profit factor 1.36 · max drawdown 14.3R
- long / short: +0.165R (457) / +0.162R (399)
- coins with an edge: BNB, BTC, ETH, SOL, XRP, ZEC
- Layer A (last 15 days): 18 trades, avg +0.432R

## 3. Walk-forward (Layer C)
- 5 of 5 windows profitable, all judged windows together +0.162R over 779 trades - passed
  - window 0: 77 trades, +0.178R (warm-up)
  - window 1: 118 trades, +0.367R (profitable)
  - window 2: 165 trades, +0.148R (profitable)
  - window 3: 129 trades, +0.164R (profitable)
  - window 4: 181 trades, +0.004R (profitable)
  - window 5: 186 trades, +0.198R (profitable)

## 4. Paper trading
- 24 closed paper signals, average +0.25R, last 20 average +0.45R, drawdown 2.8R
- backtest on unseen data +0.16R vs paper +0.25R (allowed gap 0.30R)

## 5. Control twin (the same idea without its special ingredient)
- none: too few trades to compare

## 6. Sensitivity (every parameter -20% / +20%)
- stable: every variant stays profitable · worst: stop atr 2.0→1.6 +0.068R
  - n 20→16: 863 trades, +0.161R
  - vol_x 1.5→1.2: 988 trades, +0.152R
  - adx_min 20→16: 928 trades, +0.159R
  - exit_n 10→8: 860 trades, +0.154R
  - stop atr 2.0→1.6: 960 trades, +0.068R
  - time_stop_bars 60→48: 856 trades, +0.164R
  - n 20→24: 846 trades, +0.174R
  - vol_x 1.5→1.8: 714 trades, +0.181R
  - adx_min 20→24: 762 trades, +0.156R
  - exit_n 10→12: 855 trades, +0.163R
  - stop atr 2.0→2.4: 795 trades, +0.200R
  - time_stop_bars 60→72: 854 trades, +0.164R

## 6b. Rule significance (the card with ONE entry rule removed at a time)
- without rule 1 (htf_up / htf_down): 1175 trades, +0.126R - the rule improves the result
- without rule 2 (close > prev(highest(high,20)) / close < prev(lowest(low,20))): 1518 trades, +0.092R - the rule improves the result
- without rule 3 (volume > vol_sma(20) * 1.5 / volume > vol_sma(20) * 1.5): 1095 trades, +0.136R - the rule improves the result
- without rule 4 (adx(14) > 20 / adx(14) > 20): 967 trades, +0.158R - the rule improves the result

## 7. Cost stress test
- fees, slippage and funding +50%: 857 trades · avg +0.130R · win rate 55% · profit factor 1.29 · max drawdown 17.1R
- fees, slippage and funding +100% (shown only, not a gate): 857 trades · avg +0.111R · win rate 55% · profit factor 1.24 · max drawdown 20.8R
- median cost per trade: 0.038R

## 8. Risk metrics
- max drawdown (backtest): 16.3R · average hold 11 candles
- live risk per trade: 0.5% of the account for the first 30 days, then at most 1% (risk engine, section 15)
- Monte Carlo (1000 random orders of the same 856 trades): 95% worst drawdown 21.9R (median 13.8R, as it happened 10.7R)
- **expected worst losing streak: 10 losses in a row** (95% of the random orders stay at or below it; median 7, as it happened 6) - expect it before you judge the strategy broken
- family table (trend group, active mode): verdict PAPER_TRADING (old rule: BACKTESTING)
  - recovery factor 8.61 (net +140.0R / max drawdown 16.3R) · Monte Carlo 95% worst drawdown per 100 trades 14.4R · longest drawdown 584 days (18% of the tested period)
  - **if approved, suspended at a live drawdown of 14.4R; paper retired at 14.4R** (own Monte Carlo 95% worst drawdown per 100 trades (cap 17R))
- lookahead / recursive check: passed

## 9. Why it loses (failure attribution)
- 376 losing / 480 winning backtest trades; systematic tags: false_breakout, trend_reversal, regime_mismatch, stop_too_tight
  - overextended_entry: 333 losers (89% of losses)
  - false_breakout: 249 losers (66% of losses)
  - late_entry: 241 losers (64% of losses)
  - stop_too_tight: 128 losers (34% of losses)
  - no_displacement: 125 losers (33% of losses)
  - regime_mismatch: 89 losers (24% of losses)
  - Sample: 856 trades, +0.16R per trade - clearly above zero.
  - Regime: profitable in every regime with 10+ trades (EXPANSION, STRONG_BEAR, STRONG_BULL, WEAK_BEAR, WEAK_BULL).
  - Timing: losers rarely went our way (median best point +0.33R).
  - Stop / target: stopped out and then TP1 reached anyway in 34% of losses; target nearly reached (≥ 80%) in 9%. Measured stop changes (±20% test): stop atr 2.0→1.6 → +0.07R; stop atr 2.0→2.4 → +0.20R.
  - Costs: +0.22R per trade before fees and slippage, +0.16R after.
  - Other timeframes: best is 1h at -0.03R per trade.

## 10. Known limitations
- backtests and paper results are history, not a promise; the future can differ
- the agent never trades: real fills, slippage and funding can be worse than assumed
- known weaknesses (card): Many false breakouts in chop; wide stops; most of the profit comes from a few big trends.
- history starts 2017-10-09 - check it covers a bull and a bear market

Research signal. Not financial advice.
