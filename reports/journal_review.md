# Your own trades (journal sync)

From journal/my_trades.csv on the branch `journal` (the live watcher's Telegram buttons, the plan result of every alert and your /result replies). Plan = the backtest rules followed on 5m candles, before fees. Report only: nothing here changes a strategy, a gate or a cost.

Last journal entry: 2026-11-21 03:00 UTC
- Last 30 days: 51 alerts · took 48 · skipped 0 · no answer 3
  - plan result: took +1.65R avg over 30 · skipped no result yet · no answer -1.00R avg over 2
  - your real results: +2.02R avg over 29 · gap to the plan +0.37R per trade (29)
- All time: 54 alerts · took 51 · skipped 0 · no answer 3
  - plan result: took +1.41R avg over 33 · skipped no result yet · no answer -1.00R avg over 2
  - your real results: +1.72R avg over 32 · gap to the plan +0.32R per trade (32)
- Per strategy (all time): cell · alerts · took · plan avg · your avg
  - P01-BREAKOUT-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P01-BREAKOUT-V5 1h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P02-EMA-PULLBACK-V4 4h · 1 · 1 · +3.88R (1) · +3.90R (1)
  - P03-FIB-PULLBACK-V5 1h · 1 · 1 · +2.50R (1) · +2.50R (1)
  - P04-MACD-SUPERTREND-V5 30m · 1 · 1 · -1.00R (1) · -1.08R (1)
  - P05-RANGE-REVERSAL-V4 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P07-SQUEEZE-RETEST-V1 4h · 2 · 2 · +2.50R (1) · +2.50R (1)
  - P07-SQUEEZE-RETEST-V3 4h · 2 · 2 · +2.50R (1) · +2.50R (1)
  - P12-LEADER-V1 4h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - TRD-H4-BREAKOUT-S3 1h · 9 · 9 · +1.96R (8) · +2.31R (7)
  - donchian_breakout-VEXIT 4h · 10 · 8 · +1.10R (5) · +2.50R (4)
  - donchian_breakout-VEXIT-FDISP 4h · 15 · 15 · +1.48R (12) · +1.94R (12)
  - donchian_breakout-VEXIT-FRETEST 4h · 8 · 8 · - · -
  - donchian_breakout-VEXIT-S4 4h · 1 · 0 · -1.00R (1) · -
- With vs without the 5m check (the same setups):
  - 4h: every setup without the 5m check -1.00R over 2 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 2 · alerts sent (5m entry) +1.17R over 24 (plan results, before fees)
- Findings:
  - Your real results are +0.32R per trade above the plan (32 trades) - your execution adds to the strategy.
