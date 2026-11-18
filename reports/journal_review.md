# Your own trades (journal sync)

From journal/my_trades.csv on the branch `journal` (the live watcher's Telegram buttons, the plan result of every alert and your /result replies). Plan = the backtest rules followed on 5m candles, before fees. Report only: nothing here changes a strategy, a gate or a cost.

Last journal entry: 2026-11-18 20:00 UTC
- Last 30 days: 42 alerts · took 38 · skipped 0 · no answer 4
  - plan result: took +1.34R avg over 25 · skipped no result yet · no answer -1.00R avg over 2
  - your real results: +1.67R avg over 21 · gap to the plan +0.17R per trade (21)
- All time: 44 alerts · took 40 · skipped 0 · no answer 4
  - plan result: took +1.17R avg over 27 · skipped no result yet · no answer -1.00R avg over 2
  - your real results: +1.42R avg over 23 · gap to the plan +0.14R per trade (23)
- Per strategy (all time): cell · alerts · took · plan avg · your avg
  - P01-BREAKOUT-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P01-BREAKOUT-V5 1h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P02-EMA-PULLBACK-V4 4h · 1 · 1 · +3.88R (1) · +3.90R (1)
  - P04-MACD-SUPERTREND-V5 30m · 1 · 1 · -1.00R (1) · -1.08R (1)
  - P05-RANGE-REVERSAL-V4 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P07-SQUEEZE-RETEST-V1 4h · 1 · 1 · +2.50R (1) · +2.50R (1)
  - P07-SQUEEZE-RETEST-V3 4h · 2 · 2 · +2.50R (1) · +2.50R (1)
  - P12-LEADER-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - TRD-H4-BREAKOUT-S3 1h · 7 · 7 · +1.88R (7) · +2.24R (5)
  - donchian_breakout-VEXIT 4h · 10 · 8 · +0.75R (4) · +2.50R (2)
  - donchian_breakout-VEXIT-FDISP 4h · 15 · 15 · +1.17R (9) · +1.69R (8)
  - donchian_breakout-VEXIT-FRETEST 4h · 2 · 1 · - · -
  - donchian_breakout-VEXIT-S4 4h · 1 · 0 · -1.00R (1) · -
- With vs without the 5m check (the same setups):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) +0.92R over 20 (plan results, before fees)
- Findings:
  - Your real results match the plan (+0.14R per trade difference, 23 trades): the backtest's numbers hold for you.
