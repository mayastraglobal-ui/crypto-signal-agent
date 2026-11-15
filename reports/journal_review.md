# Your own trades (journal sync)

From journal/my_trades.csv on the branch `journal` (the live watcher's Telegram buttons, the plan result of every alert and your /result replies). Plan = the backtest rules followed on 5m candles, before fees. Report only: nothing here changes a strategy, a gate or a cost.

Last journal entry: 2026-11-15 00:00 UTC
- Last 30 days: 40 alerts · took 37 · skipped 0 · no answer 3
  - plan result: took +1.29R avg over 18 · skipped no result yet · no answer -1.00R avg over 1
  - your real results: +1.48R avg over 17 · gap to the plan +0.21R per trade (17)
- All time: 42 alerts · took 39 · skipped 0 · no answer 3
  - plan result: took +1.06R avg over 20 · skipped no result yet · no answer -1.00R avg over 1
  - your real results: +1.20R avg over 19 · gap to the plan +0.17R per trade (19)
- Per strategy (all time): cell · alerts · took · plan avg · your avg
  - P01-BREAKOUT-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P01-BREAKOUT-V5 1h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P02-EMA-PULLBACK-V4 4h · 1 · 1 · - · -
  - P04-MACD-SUPERTREND-V5 30m · 1 · 1 · -1.00R (1) · -1.08R (1)
  - P05-RANGE-REVERSAL-V4 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P07-SQUEEZE-RETEST-V1 4h · 1 · 1 · +2.50R (1) · +2.50R (1)
  - P07-SQUEEZE-RETEST-V3 4h · 2 · 2 · +2.50R (1) · +2.50R (1)
  - P12-LEADER-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - TRD-H4-BREAKOUT-S3 1h · 7 · 7 · +1.64R (5) · +2.17R (4)
  - donchian_breakout-VEXIT 4h · 10 · 8 · +2.50R (2) · +2.50R (2)
  - donchian_breakout-VEXIT-FDISP 4h · 15 · 15 · +1.33R (6) · +1.67R (6)
  - donchian_breakout-VEXIT-S4 4h · 1 · 0 · -1.00R (1) · -
- With vs without the 5m check (the same setups):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) +1.00R over 14 (plan results, before fees)
- Findings:
  - Your real results are +0.17R per trade above the plan (19 trades) - your execution adds to the strategy.
