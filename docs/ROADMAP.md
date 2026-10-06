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
| 2026-10-06 | Step 1 built: Windows watcher (`windows/*.bat`, `docs/WINDOWS_WATCHER.md`) |
| 2026-10-06 | Windows watcher installed and running on the operator's PC |
| 2026-10-06 | Step 4 built: Telegram commands, ✅/❌ buttons, trade follow-up, `journal/my_trades.csv` |
| 2026-10-06 | Step 2 part A: 2 years of OKX USDT-perpetual 30m / 15m / 5m candles for research; longs pay real funding |
| 2026-10-06 | Step 2 part B: limit-order entries (`entry: limit` on a card) in backtests, paper trades, emails, Telegram, Pine |
| 2026-10-06 | Step 3a-3c: the operator's playbook (strategies A / B / C, its risk rules and pass bar) (`docs/PLAYBOOK.md`) |
| 2026-10-06 | Step 3d: flexible playbook versions - graded setups, A in London, B on 15m, C's wider box, the fee fix |
| 2026-10-06 | Step 5: the 4H trend window + faster entries (TRD-H4-*), strategies by market type, scalping variants |

## Next steps, in order

### Step 1: Windows watcher (live alerts on the operator's Windows PC, 24/7)
Oracle Cloud sign-up failed for the operator, and the Windows PC can run 24 hours. `windows\1_setup.bat`
(Python, packages, Telegram bot, sleep = never, start with Windows via the Startup folder), start / stop / update
buttons, restart after a crash, guide `docs/WINDOWS_WATCHER.md`.
Status: **done 2026-10-06** (no git needed: GitHub's decision files are downloaded every hour; `4_update.bat`
for code). Installed and running on the operator's PC.

### Step 2: make scalping testable (biggest impact on signals)
1. **Done (part A, 2026-10-06):** more short-timeframe history for research: 30m / 15m / 5m = 2 years (5m was 90
   days, 15m 1 year), from OKX's own monthly / daily candle files (faster than data.binance.vision and the right
   market), cached; a later run downloads only new days.
2. **Done (part B, 2026-10-06):** limit-order entries - a card option `entry: {type: limit, offset_atr, valid_bars}`:
   maker fee, no slippage, a trade only counts when price comes back to the limit price within valid_bars candles
   (no fill = no trade; only the stop counts in the fill candle). The same rules in the hourly paper record
   (`AWAITING_FILL`), the emails, the Telegram alert ("BUY LIMIT x · cancel at hh:mm") and its follow-up (filled /
   not filled - cancel), and the Pine export (REPLAY at the engine's limit prices). No card uses it yet: Step 3's
   scalping cards and Step 5's automatic variants will.
3. **Done (part A):** backtests on OKX perpetual candles (30m / 15m / 5m; 1W-1H stay Binance spot since 2017) with
   real funding: longs now pay the higher of 0.01% / 8h and the real rate, like shorts already did.

### Step 3: focused scalping strategies (5-8 cards, each with a control twin, in the lab first)
- 4H trend → 15m pullback to EMA20 / VWAP → 5m confirmation
- 15m breakout and retest
- London / New York session open
- Liquidity sweep in the trend direction
- Funding / open-interest filter (skip crowded trades)
- **The operator's own rules** - done: the operator's scalping playbook, `docs/PLAYBOOK.md` (3a-3c), and its
  flexible versions (3d: graded setups, the three rule changes the operator asked to test, the fee fix).

### Step 4: help during a trade (Telegram)
Status: **built 2026-10-06** (`engine/follow.py`, `engine/live.py`, `live_watcher.py`):
- Commands `/status`, `/trades`, `/pause` (`/pause 2h`), `/resume`, `/help` - only the operator's chat is answered.
- Buttons "✅ Took it / ❌ Skipped / 🏁 I closed it" under each alert; recorded in `journal/my_trades.csv` on the PC.
- Follow-up of taken trades on 5m candles with the backtests' rules (a test checks they match
  `scanner.simulate_trade`): TP1 → stop to entry, TP2 → stop to TP1, last TP, stop, time stop, result in R.
- Not yet: "trend turned" warnings and the strategy's own early-exit rule (not in the follow-up; the time stop is),
  and sending the journal to GitHub (it stays on the PC for now).

### Step 5: the agent improves itself more
Status: **built 2026-10-06** (operator: "start step 5"):
1. **The proven trend, a faster entry** (`engine/trend4h.py`): `trend4h_long` / `trend4h_short` = the 4H Donchian
   breakout (the library's measured edge) would hold a trade now - frozen rules, from the newest closed 4H candle,
   readable on 1H / 30m / 15m / 5m (and by lab cards). Cards `TRD-H4-PULLBACK` (dip to the EMA20 and close back)
   and `TRD-H4-BREAKOUT` (a new 20-candle high with volume) trade only inside that window, limit entries, 2R / 3R,
   the fee cap; each has a control twin without the window (`-noT4`).
2. **Strategies by market type** (`engine/regime_fit.py`): the research run writes `reports/regime_fit.json` (each
   cell's backtest result per market regime); the hourly scan and the live watcher send no alert in a regime where
   that cell lost money (30+ trades, -0.10R or worse). It only removes alerts.
3. **Automatic scalping variants** (`engine/ideas.py`): for a 1H-5m cell whose fees cost a median > 0.15R, the
   variant search first tries a limit entry (`-VLIMIT`) and the fee cap (`-VFEECAP`), one change each, tested like
   any card.
- Still open: Claude's daily / weekly research focused on scalping ideas from the main loss causes.

### Step 6 (optional): more coins
Top ~15 liquid OKX perpetuals instead of 7, with the spread and depth rules kept.

## The operator's to-do list

| When | What |
|---|---|
| Now | Double-click `windows\4_update.bat` once to get the Telegram commands and buttons |
| After the next research email | Compare the playbook versions (originals vs -LDN / -15M / -W20 / -LIMIT / -GRADED / -APLUS) |
| On or after 2026-10-10 | `config.yaml` → `family_gates`: `mode: active`, `operator_ok: 2026-10-10` (lets the 4H Donchian strategies reach PAPER_TRADING) |
| Later | Approve a strategy when the weekly email shows 20 good paper trades (copy its approval line) |
| Optional | If the old Claude tasks still exist in the Claude desktop app, delete them (the cloud Routines replace them) |
