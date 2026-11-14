# Your own trades (journal sync)

From journal/my_trades.csv on the branch `journal` (the live watcher's Telegram buttons, the plan result of every alert and your /result replies). Plan = the backtest rules followed on 5m candles, before fees. Report only: nothing here changes a strategy, a gate or a cost.

Last journal entry: 2026-11-14 07:42 UTC
- Last 30 days: 28 alerts · took 27 · skipped 0 · no answer 1
  - plan result: took +0.94R avg over 14 · skipped no result yet · no answer -1.00R avg over 1
  - your real results: +1.16R avg over 13 · gap to the plan +0.28R per trade (13)
- All time: 30 alerts · took 29 · skipped 0 · no answer 1
  - plan result: took +0.70R avg over 16 · skipped no result yet · no answer -1.00R avg over 1
  - your real results: +0.85R avg over 15 · gap to the plan +0.22R per trade (15)
- Per strategy (all time): cell · alerts · took · plan avg · your avg
  - P01-BREAKOUT-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P01-BREAKOUT-V5 1h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P02-EMA-PULLBACK-V4 4h · 1 · 1 · - · -
  - P04-MACD-SUPERTREND-V5 30m · 1 · 1 · -1.00R (1) · -1.08R (1)
  - P05-RANGE-REVERSAL-V4 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P07-SQUEEZE-RETEST-V1 4h · 1 · 1 · +2.50R (1) · +2.50R (1)
  - P07-SQUEEZE-RETEST-V3 4h · 2 · 2 · +2.50R (1) · +2.50R (1)
  - P12-LEADER-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - TRD-H4-BREAKOUT-S3 1h · 5 · 5 · +1.42R (4) · +2.07R (3)
  - donchian_breakout-VEXIT 4h · 5 · 5 · +2.50R (2) · +2.50R (2)
  - donchian_breakout-VEXIT-FDISP 4h · 10 · 10 · +0.17R (3) · +0.83R (3)
  - donchian_breakout-VEXIT-S4 4h · 1 · 0 · -1.00R (1) · -
- With vs without the 5m check (the same setups):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) +0.59R over 11 (plan results, before fees)
- Findings:
  - Your real results are +0.22R per trade above the plan (15 trades) - your execution adds to the strategy.
