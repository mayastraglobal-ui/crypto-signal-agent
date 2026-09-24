# Changelog

Every change to the rules, config, prompt or engine is logged here (AGENT_PROMPT.md §0, §22).
Newest entries at the bottom. Format: date · who · what · why.

## 2026-09-24 · Operator (Maya) + Claude (BUILD mode) · Phase 0 — operator settings
- **Risk per trade:** 1.0% → **0.5%** (`config.yaml` → `account.risk_per_trade_pct`). Why: AGENT_PROMPT.md §15/§26 — 0.5% during validation and the first live month, max 1% after. Operator decision.
- **Costs split by direction** (`config.yaml` → `costs`). Why: §11 "longs use spot costs, shorts use futures costs" + funding. Exchange not decided yet, so Binance VIP 0 fees are used. Operator decision.
  - LONG (spot): taker 0.10%, maker 0.10%, slippage 0.05% — unchanged from before.
  - SHORT (futures only): taker 0.05%, maker 0.02%, slippage 0.05%, **funding 0.01% per 8h always charged against the short** (cautious: real funding history is not fetched, and it can be positive or negative).
  - Note: shorts now pay lower fees than before (futures fees are lower than spot fees). This is more accurate, not a lower bar. Validation gates are unchanged.
- Shorts are labelled **"futures only"** in reports and emails.
- Added `tests/test_costs.py`, including guard tests that fail if costs are set to 0, risk goes above 1%, or the validation bar is lowered.
