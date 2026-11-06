# Your own trades (journal sync)

From journal/my_trades.csv on the branch `journal` (the live watcher's Telegram buttons, the plan result of every alert and your /result replies). Plan = the backtest rules followed on 5m candles, before fees. Report only: nothing here changes a strategy, a gate or a cost.

Last journal entry: 2026-11-06 08:20 UTC
- Last 30 days: 9 alerts · took 8 · skipped 0 · no answer 1
  - plan result: took -1.00R avg over 6 · skipped no result yet · no answer -1.00R avg over 1
  - your real results: -1.18R avg over 6 · gap to the plan -0.18R per trade (6)
- All time: 9 alerts · took 8 · skipped 0 · no answer 1
  - plan result: took -1.00R avg over 6 · skipped no result yet · no answer -1.00R avg over 1
  - your real results: -1.18R avg over 6 · gap to the plan -0.18R per trade (6)
- Per strategy (all time): cell · alerts · took · plan avg · your avg
  - P01-BREAKOUT-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P01-BREAKOUT-V5 1h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P02-EMA-PULLBACK-V4 4h · 1 · 1 · - · -
  - P04-MACD-SUPERTREND-V5 30m · 1 · 1 · -1.00R (1) · -1.08R (1)
  - P05-RANGE-REVERSAL-V4 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P07-SQUEEZE-RETEST-V3 4h · 1 · 1 · - · -
  - P12-LEADER-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - donchian_breakout-VEXIT-FDISP 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - donchian_breakout-VEXIT-S4 4h · 1 · 0 · -1.00R (1) · -
- With vs without the 5m check (the same setups):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) -1.00R over 5 (plan results, before fees)
- Findings:
  - Your real results are -0.18R per trade below the plan (6 trades). That is fees, slippage, late entries or early exits the backtest does not see: enter close to the alert price, use the limit entries, keep the stop and TPs on OKX. If it stays, the backtest costs may be too low for you - a decision for you, the agent never changes them.
