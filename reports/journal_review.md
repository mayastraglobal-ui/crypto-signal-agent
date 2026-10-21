# Your own trades (journal sync)

From journal/my_trades.csv on the branch `journal` (the live watcher's Telegram buttons, the plan result of every alert and your /result replies). Plan = the backtest rules followed on 5m candles, before fees. Report only: nothing here changes a strategy, a gate or a cost.

Last journal entry: 2026-10-21 16:00 UTC
- Last 30 days: 3 alerts · took 2 · skipped 0 · no answer 1
  - plan result: took -1.00R avg over 2 · skipped no result yet · no answer no result yet
  - your real results: -1.14R avg over 2 · gap to the plan -0.14R per trade (2)
- All time: 3 alerts · took 2 · skipped 0 · no answer 1
  - plan result: took -1.00R avg over 2 · skipped no result yet · no answer no result yet
  - your real results: -1.14R avg over 2 · gap to the plan -0.14R per trade (2)
- Per strategy (all time): cell · alerts · took · plan avg · your avg
  - P01-BREAKOUT-V5 1h · 1 · 1 · -1.00R (1) · -1.20R (1)
  - P04-MACD-SUPERTREND-V5 30m · 1 · 1 · -1.00R (1) · -1.08R (1)
  - donchian_breakout-VEXIT-FDISP 4h · 1 · 0 · - · -
- With vs without the 5m check (the same setups):
  - 4h: every setup without the 5m check -1.00R over 1 · the ones the 5m check passed none yet · the ones it rejected -1.00R over 1 · alerts sent (5m entry) none yet (plan results, before fees)
- Findings:
  - none yet (each needs 5+ trades)
