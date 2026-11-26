# Approval pack: donchian_breakout v1.0 4h

Written by the engine on 2026-11-26 08:50 UTC (AGENT_PROMPT.md section 21). Numbers only - the decision is yours.

**Question: Approve donchian_breakout v1.0 4h for live emails? (yes/no)**

To say yes, add this under `approvals:` in `config.yaml` (on GitHub: open the file, pencil icon, commit):
```
  - {strategy: donchian_breakout, version: "1.0", tf: 4h, date: 2026-11-26}
```
The next daily research run moves it to APPROVED. To undo, delete the line. Saying nothing = no.
**Check the trades before you say yes:**
- backtest chart (every trade on the candles, stop and targets, equity and drawdown): https://mayastraglobal-ui.github.io/crypto-signal-agent/chart.html#s=donchian_breakout&v=1.0&tf=4h
- TradingView: open https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/main/reports/pine/donchian_breakout_v1.0_4h.pine (`reports/pine/donchian_breakout_v1.0_4h.pine`), copy it into TradingView's Pine Editor and add it to a chart - it draws the same signals and trades

## 0. Bull vs bear (the engine's numbers only - Phase 18)
- Bull case: unseen part of the backtest (last 30%): +0.154R per trade over 284 trades; whole history: +0.162R per trade over 857 trades, profit factor 1.38; walk-forward: 5 of 5 time windows profitable, together +0.162R; costs +50%: +0.129R per trade; every parameter -20% / +20% stays profitable (12 variants); an edge on 6 coin(s): BNB, BTC, ETH, SOL, XRP, ZEC; paper trading: +0.29R per signal over 25 closed signals
- Bear case: worst drawdown in the backtest: 16.3R · wins 56% of trades; by bad luck alone (Monte Carlo): 95% worst drawdown 22.1R, expected worst losing streak 10 in a row; systematic loss tags: false_breakout, trend_reversal, regime_mismatch, stop_too_tight (377 losing trades)
- Risk manager: VETO - 0 of 6 signal coins are in one of its regimes on 4H now - regime against
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
- Layer B, whole history: 857 trades · avg +0.162R · win rate 56% · profit factor 1.38 · max drawdown 16.3R
- Layer B, develop part (first 70%): 573 trades · avg +0.166R · win rate 57% · profit factor 1.40 · max drawdown 16.3R
- Layer B, unseen part (last 30%): 284 trades · avg +0.154R · win rate 55% · profit factor 1.34 · max drawdown 14.3R
- long / short: +0.165R (457) / +0.159R (400)
- coins with an edge: BNB, BTC, ETH, SOL, XRP, ZEC
- Layer A (last 15 days): 14 trades, avg +0.342R

## 3. Walk-forward (Layer C)
- 5 of 5 windows profitable, all judged windows together +0.162R over 779 trades - passed
  - window 0: 78 trades, +0.162R (warm-up)
  - window 1: 117 trades, +0.379R (profitable)
  - window 2: 165 trades, +0.148R (profitable)
  - window 3: 131 trades, +0.156R (profitable)
  - window 4: 179 trades, +0.007R (profitable)
  - window 5: 187 trades, +0.192R (profitable)

## 4. Paper trading
- 25 closed paper signals, average +0.29R, last 20 average +0.42R, drawdown 2.8R
- backtest on unseen data +0.15R vs paper +0.29R (allowed gap 0.30R)

## 5. Control twin (the same idea without its special ingredient)
- none: too few trades to compare

## 6. Sensitivity (every parameter -20% / +20%)
- stable: every variant stays profitable · worst: stop atr 2.0→1.6 +0.067R
  - n 20→16: 865 trades, +0.158R
  - vol_x 1.5→1.2: 989 trades, +0.151R
  - adx_min 20→16: 929 trades, +0.158R
  - exit_n 10→8: 861 trades, +0.153R
  - stop atr 2.0→1.6: 961 trades, +0.067R
  - time_stop_bars 60→48: 857 trades, +0.162R
  - n 20→24: 847 trades, +0.172R
  - vol_x 1.5→1.8: 715 trades, +0.179R
  - adx_min 20→24: 762 trades, +0.156R
  - exit_n 10→12: 856 trades, +0.162R
  - stop atr 2.0→2.4: 797 trades, +0.198R
  - time_stop_bars 60→72: 855 trades, +0.163R

## 6b. Rule significance (the card with ONE entry rule removed at a time)
- without rule 1 (htf_up / htf_down): 1176 trades, +0.125R - the rule improves the result
- without rule 2 (close > prev(highest(high,20)) / close < prev(lowest(low,20))): 1522 trades, +0.091R - the rule improves the result
- without rule 3 (volume > vol_sma(20) * 1.5 / volume > vol_sma(20) * 1.5): 1096 trades, +0.135R - the rule improves the result
- without rule 4 (adx(14) > 20 / adx(14) > 20): 968 trades, +0.157R - the rule improves the result

## 7. Cost stress test
- fees, slippage and funding +50%: 858 trades · avg +0.129R · win rate 55% · profit factor 1.29 · max drawdown 17.1R
- fees, slippage and funding +100% (shown only, not a gate): 858 trades · avg +0.110R · win rate 55% · profit factor 1.24 · max drawdown 20.8R
- median cost per trade: 0.038R

## 8. Risk metrics
- max drawdown (backtest): 16.3R · average hold 11 candles
- live risk per trade: 0.5% of the account for the first 30 days, then at most 1% (risk engine, section 15)
- Monte Carlo (1000 random orders of the same 857 trades): 95% worst drawdown 22.1R (median 14.0R, as it happened 10.9R)
- **expected worst losing streak: 10 losses in a row** (95% of the random orders stay at or below it; median 8, as it happened 6) - expect it before you judge the strategy broken
- family table (trend group, active mode): verdict PAPER_TRADING (old rule: BACKTESTING)
  - recovery factor 8.55 (net +139.0R / max drawdown 16.3R) · Monte Carlo 95% worst drawdown per 100 trades 14.1R · longest drawdown 584 days (18% of the tested period)
  - **if approved, suspended at a live drawdown of 14.1R; paper retired at 14.1R** (own Monte Carlo 95% worst drawdown per 100 trades (cap 17R))
- lookahead / recursive check: passed

## 9. Why it loses (failure attribution)
- 377 losing / 480 winning backtest trades; systematic tags: false_breakout, trend_reversal, regime_mismatch, stop_too_tight
  - overextended_entry: 333 losers (88% of losses)
  - false_breakout: 250 losers (66% of losses)
  - late_entry: 241 losers (64% of losses)
  - stop_too_tight: 128 losers (34% of losses)
  - no_displacement: 126 losers (33% of losses)
  - regime_mismatch: 89 losers (24% of losses)
  - Sample: 857 trades, +0.16R per trade - clearly above zero.
  - Regime: profitable in every regime with 10+ trades (EXPANSION, STRONG_BEAR, STRONG_BULL, WEAK_BEAR, WEAK_BULL).
  - Timing: losers rarely went our way (median best point +0.32R).
  - Stop / target: stopped out and then TP1 reached anyway in 34% of losses; target nearly reached (≥ 80%) in 9%. Measured stop changes (±20% test): stop atr 2.0→1.6 → +0.07R; stop atr 2.0→2.4 → +0.20R.
  - Costs: +0.21R per trade before fees and slippage, +0.16R after.
  - Other timeframes: best is 1h at -0.03R per trade.

## 10. Known limitations
- backtests and paper results are history, not a promise; the future can differ
- the agent never trades: real fills, slippage and funding can be worse than assumed
- known weaknesses (card): Many false breakouts in chop; wide stops; most of the profit comes from a few big trends.
- history starts 2017-10-09 - check it covers a bull and a bear market

Research signal. Not financial advice.
