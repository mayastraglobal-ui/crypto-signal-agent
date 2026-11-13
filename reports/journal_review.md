# Your own trades (journal sync)

From journal/my_trades.csv on the branch `journal` (the live watcher's Telegram buttons, the plan result of every alert and your /result replies). Plan = the backtest rules followed on 5m candles, before fees. Report only: nothing here changes a strategy, a gate or a cost.

Last journal entry: 2026-11-13 04:00 UTC
- Last 30 days: 25 alerts · took 20 · skipped 0 · no answer 5
  - plan result: took +0.38R avg over 7 · skipped no result yet · no answer -1.00R avg over 1
  - your real results: -0.46R avg over 5 · gap to the plan -0.16R per trade (5)
- All time: 27 alerts · took 22 · skipped 0 · no answer 5
  - plan result: took +0.07R avg over 9 · skipped no result yet · no answer -1.00R avg over 1
  - your real results: -0.65R avg over 7 · gap to the plan -0.15R per trade (7)
- Per strategy (all time): cell · alerts · took · plan avg · your avg
  - P01-BREAKOUT-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P01-BREAKOUT-V5 1h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P02-EMA-PULLBACK-V4 4h · 1 · 1 · - · -
  - P04-MACD-SUPERTREND-V5 30m · 1 · 1 · -1.00R (1) · -1.08R (1)
  - P05-RANGE-REVERSAL-V4 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P07-SQUEEZE-RETEST-V1 4h · 1 · 1 · - · -
  - P07-SQUEEZE-RETEST-V3 4h · 2 · 2 · +2.50R (1) · +2.50R (1)
  - P12-LEADER-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - TRD-H4-BREAKOUT-S3 1h · 4 · 4 · +2.09R (2) · -
  - donchian_breakout-VEXIT 4h · 3 · 3 · - · -
  - donchian_breakout-VEXIT-FDISP 4h · 10 · 6 · -1.00R (1) · -1.20R (1)
  - donchian_breakout-VEXIT-S4 4h · 1 · 0 · -1.00R (1) · -
- With vs without the 5m check (the same setups):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) -0.42R over 6 (plan results, before fees)
- Findings:
  - Your real results are -0.15R per trade below the plan (7 trades). That is fees, slippage, late entries or early exits the backtest does not see: enter close to the alert price, use the limit entries, keep the stop and TPs on OKX. If it stays, the backtest costs may be too low for you - a decision for you, the agent never changes them.
  - 14 of 22 trades you took have no real result: send /result 1.2 (your result in R) after each trade so the agent can compare you with the plan.
