# Your own trades (journal sync)

From journal/my_trades.csv on the branch `journal` (the live watcher's Telegram buttons, the plan result of every alert and your /result replies). Plan = the backtest rules followed on 5m candles, before fees. Report only: nothing here changes a strategy, a gate or a cost.

Last journal entry: 2026-11-23 16:56 UTC
- Last 30 days: 58 alerts · took 54 · skipped 0 · no answer 4
  - plan result: took +1.14R avg over 50 · skipped no result yet · no answer -1.00R avg over 4
  - your real results: +1.43R avg over 49 · gap to the plan +0.31R per trade (49)
- All time: 62 alerts · took 58 · skipped 0 · no answer 4
  - plan result: took +0.98R avg over 54 · skipped no result yet · no answer -1.00R avg over 4
  - your real results: +1.24R avg over 53 · gap to the plan +0.27R per trade (53)
- Per strategy (all time): cell · alerts · took · plan avg · your avg
  - P01-BREAKOUT-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P01-BREAKOUT-V5 1h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P02-EMA-PULLBACK-V4 4h · 1 · 1 · +3.88R (1) · +3.90R (1)
  - P03-FIB-PULLBACK-V5 1h · 1 · 1 · +2.50R (1) · +2.50R (1)
  - P04-MACD-SUPERTREND-V5 30m · 1 · 1 · -1.00R (1) · -1.08R (1)
  - P05-RANGE-REVERSAL-V4 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P07-SQUEEZE-RETEST-V1 4h · 2 · 2 · +2.50R (2) · +2.50R (2)
  - P07-SQUEEZE-RETEST-V3 4h · 2 · 2 · +2.50R (1) · +2.50R (1)
  - P12-LEADER-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - TRD-H4-BREAKOUT-S3 1h · 11 · 11 · +1.15R (11) · +1.52R (10)
  - donchian_breakout-VEXIT 4h · 10 · 8 · +0.85R (10) · +1.75R (8)
  - donchian_breakout-VEXIT-FDISP 4h · 15 · 15 · +1.59R (15) · +1.95R (15)
  - donchian_breakout-VEXIT-FDISP-S2 4h · 4 · 3 · -1.00R (4) · -1.00R (3)
  - donchian_breakout-VEXIT-FRETEST 4h · 10 · 10 · +0.00R (7) · +0.29R (7)
  - donchian_breakout-VEXIT-S4 4h · 1 · 0 · -1.00R (1) · -
- With vs without the 5m check (the same setups):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) +0.81R over 44 (plan results, before fees)
- Findings:
  - Your real results are +0.27R per trade above the plan (53 trades) - your execution adds to the strategy.
