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

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 1 — data quality
- New `engine/data_quality.py` (AGENT_PROMPT.md §3). Checks every candle table: order, duplicates, unfinished candles (dropped, never used), zero/negative/missing prices, high < low, open/close outside the range, negative volume, off-grid timestamps, missing candles, stale feed, volume spikes on the newest candles, Binance-vs-OKX price difference.
- States: GOOD (signals allowed) · DEGRADED (analysis only) · UNSAFE (no signals). System UNSAFE when BTC is UNSAFE, BTC is missing, or > 30% of coins are UNSAFE/failed → `DATA_STALE / SIGNAL_DISABLED`, all signals stop.
- A signal now also needs GOOD data on its timeframe, its higher timeframe and the cross-exchange check. UNSAFE data is not backtested; open forward-test signals are not scored on UNSAFE data.
- `scanner.py`: `_finish` no longer silently cleans candles; all downloads go through `fetch_checked()` so problems are reported, not hidden. New report section "0. Data check" and `reports/data_quality.json`. New `--fault` option (offline only) to plant bad data for testing.
- `notify.py system`: one `[SYSTEM] DATA_STALE / SIGNAL_DISABLED` email when data turns UNSAFE, one "Data recovered" email when it recovers (state kept in `reports/system_alert_state.json`). Scan-failure email now starts with `[SYSTEM]`.
- Thresholds in `config.yaml` → `data_quality`. Refinement vs the plan: old gaps (outside the newest 300 candles, under 1% of history) are only a note, because they do not affect current indicators.
- Workflows: `scan.yml` runs `notify.py system`; new `tests.yml` runs all tests on every push/PR.
- Tests: `tests/test_data_quality.py` (planted faults, look-ahead tests, end-to-end offline runs, email once-only behaviour).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 2 — tradable universe
- New `engine/universe.py` (AGENT_PROMPT.md §4): **7 signal coins** (only these can give signals) + **3 research-only coins** (backtested, never a signal), ranked by 24h quote volume; BTC and ETH always included when eligible.
- **Eligibility** (all must pass; limits in `config.yaml` → `universe`): ≥ 180 days history · 24h volume ≥ $50M · 7-day average volume ≥ $50M · 24h volume ≤ 3× the 7-day average · 24h move within ±25% (else suspended for the rest of the UTC day) · spread ≤ 0.10% · ≥ $250k order-book depth within 1% on each side · daily price data not UNSAFE · not on an exclusion list · does not behave like a stablecoin (price within ±2% for 30 days — measurable, not by name).
- **Hysteresis:** a newcomer must rank top 7 for 2 runs in a row to join; a member must rank outside the top 7 for 2 runs in a row to leave. A member that breaks a rule, or whose data turns UNSAFE, leaves at once. A freed slot stays empty until a coin qualifies (BTC/ETH re-join at once).
- **Operator decisions (2026-09-24):** NEAR added to `exclude_ai` ("the blockchain for AI"); a member with DEGRADED data stays in the list but gets no signals (Phase 1 gate); suspected wash volume (24h volume > 1000× the 1% depth) is **flag only** for now — review the threshold after a week of live data.
- Config: `always_include` reduced to BTC, ETH (SOL, BNB, XRP must now earn their place); `top_n_coins` and `market.min_24h_volume_usdt` ($30M) replaced by the `universe` section ($50M); new `exclude_gold` (PAXG moved there, XAUT added).
- Engine: only the 10 research coins get full downloads (was ~25 coins) → faster runs, fewer backtest trades; the validation bar is unchanged, so passing is slightly harder.
- New outputs: report section "0b. Coins this run", `reports/universe.json`, `reports/universe_state.json`, append-only `memory/universe_log.md` (changes only). `scan.yml` now also saves `memory/`.
- Offline test feed: extra coins (a hidden stablecoin FAKEUSD, a +40% mover PUMP), `--scenario` option, deterministic random numbers.
- Tests: `tests/test_universe.py` (22 tests: every rule, hysteresis sequences, log-only-changes, 3-run end-to-end rotation).
