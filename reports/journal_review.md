# Your own trades (journal sync)

From journal/my_trades.csv on the branch `journal` (the live watcher's Telegram buttons, the plan result of every alert and your /result replies). Plan = the backtest rules followed on 5m candles, before fees. Report only: nothing here changes a strategy, a gate or a cost.

Last journal entry: 2026-11-14 17:12 UTC
- Last 30 days: 34 alerts · took 33 · skipped 0 · no answer 1
  - plan result: took +1.14R avg over 16 · skipped no result yet · no answer -1.00R avg over 1
  - your real results: +1.34R avg over 15 · gap to the plan +0.24R per trade (15)
- All time: 36 alerts · took 35 · skipped 0 · no answer 1
  - plan result: took +0.90R avg over 18 · skipped no result yet · no answer -1.00R avg over 1
  - your real results: +1.05R avg over 17 · gap to the plan +0.20R per trade (17)
- Per strategy (all time): cell · alerts · took · plan avg · your avg
  - P01-BREAKOUT-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P01-BREAKOUT-V5 1h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P02-EMA-PULLBACK-V4 4h · 1 · 1 · - · -
  - P04-MACD-SUPERTREND-V5 30m · 1 · 1 · -1.00R (1) · -1.08R (1)
  - P05-RANGE-REVERSAL-V4 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P07-SQUEEZE-RETEST-V1 4h · 1 · 1 · +2.50R (1) · +2.50R (1)
  - P07-SQUEEZE-RETEST-V3 4h · 2 · 2 · +2.50R (1) · +2.50R (1)
  - P12-LEADER-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - TRD-H4-BREAKOUT-S3 1h · 7 · 7 · +1.42R (4) · +2.07R (3)
  - donchian_breakout-VEXIT 4h · 7 · 7 · +2.50R (2) · +2.50R (2)
  - donchian_breakout-VEXIT-FDISP 4h · 12 · 12 · +1.10R (5) · +1.50R (5)
  - donchian_breakout-VEXIT-S4 4h · 1 · 0 · -1.00R (1) · -
- With vs without the 5m check (the same setups):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) +0.89R over 13 (plan results, before fees)
- Findings:
  - Your real results are +0.20R per trade above the plan (17 trades) - your execution adds to the strategy.
