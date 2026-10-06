# Roadmap: the scalping upgrade plan

Agreed with the operator on 2026-10-05/06. Update a step's status whenever it changes, so any later session (or
Claude's scheduled tasks) can pick up from here.

**The operator's trading style:** OKX USDT-perpetual futures, long and short, $1000 account, scalping with trend.
1W / 1D = trend → 4H / 1H = bull or bear → strategy on 1H / 30m / 15m → 5m entry → alert with entry zone, stop
and targets, instantly.

**Fixed decisions (do not change without the operator):**
- Live signals keep needing the operator's yes (`approvals:` in `config.yaml`). No automatic approval.
- Never lower the pass rules (gates, trials bar, costs) to get more signals.
- The agent never places orders and never needs exchange keys.
- GitHub stays the brain (research, backtests, coins, strategy statuses, emails, official record); the live
  watcher is the fast eyes (5-minute checks, Telegram).

## Done

| Date | What |
|---|---|
| 2026-10-05 | Lab duplicate variants fixed; Binance 451 noise and false calendar warning removed (PR #42) |
| 2026-10-05 | Claude's briefing / daily review / weekly research Routines recreated; cloud network set to Full |
| 2026-10-05 | Costs = OKX futures fees + funding for longs and shorts (PR #43) |
| 2026-10-05 | Live watcher with Telegram alerts built (`live_watcher.py`, `docs/LIVE_WATCHER.md`) (PR #43) |
| 2026-10-06 | Step 1 built: Windows watcher (`windows/*.bat`, `docs/WINDOWS_WATCHER.md`) - the operator still has to run `windows\1_setup.bat` on the Windows PC |

## Next steps, in order

### Step 1: Windows watcher (live alerts on the operator's Windows PC, 24/7)
Oracle Cloud sign-up failed for the operator, and the Windows PC can run 24 hours. `windows\1_setup.bat`
(Python, packages, Telegram bot, sleep = never, start with Windows via the Startup folder), start / stop / update
buttons, restart after a crash, guide `docs/WINDOWS_WATCHER.md`.
Status: **built 2026-10-06** (no git needed: GitHub's decision files are downloaded every hour; `4_update.bat`
for code). Waiting for the operator to install it on the Windows PC.

### Step 2: make scalping testable (biggest impact on signals)
1. More short-timeframe history for research: 5m from 90 days to ~2 years, 15m to ~2 years (bulk files from
   data.binance.vision), within the research time budget.
2. Limit-order entries in backtests: maker fee, no slippage, and a trade only counts when price comes back to
   the limit price (no fill = no trade).
3. Backtests on OKX perpetual candles with real funding (the market the operator trades).

### Step 3: focused scalping strategies (5-8 cards, each with a control twin, in the lab first)
- 4H trend → 15m pullback to EMA20 / VWAP → 5m confirmation
- 15m breakout and retest
- London / New York session open
- Liquidity sweep in the trend direction
- Funding / open-interest filter (skip crowded trades)
- **The operator's own rules** - waiting for the operator to write them down.

### Step 4: help during a trade (Telegram)
- Trade-management alerts: TP1 hit → stop to entry, trend turned, time stop reached
- Buttons "✅ took it / ❌ skipped" → the operator's real results are recorded
- Commands `/status`, `/pause`

### Step 5: the agent improves itself more
- Choose strategies by market regime (bull / bear / range), from what the research already measures
- Automatic scalping variants of near-passing 15m cells (5m confirmation, limit entry, session filter)
- Claude's daily / weekly research focused on scalping ideas from the main loss causes

### Step 6 (optional): more coins
Top ~15 liquid OKX perpetuals instead of 7, with the spread and depth rules kept.

## The operator's to-do list

| When | What |
|---|---|
| Now | Install the Windows watcher: download the ZIP, double-click `windows\1_setup.bat` (`docs/WINDOWS_WATCHER.md`) |
| Now | Write down the scalping rules (for Step 3) |
| On or after 2026-10-10 | `config.yaml` → `family_gates`: `mode: active`, `operator_ok: 2026-10-10` (lets the 4H Donchian strategies reach PAPER_TRADING) |
| Later | Approve a strategy when the weekly email shows 20 good paper trades (copy its approval line) |
| Optional | If the old Claude tasks still exist in the Claude desktop app, delete them (the cloud Routines replace them) |
