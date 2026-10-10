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
| 2026-10-06 | Journal sync: the operator's trades reach GitHub (branch `journal`), plan result of every alert, `/result`, "Your own trades" in the weekly email |
| 2026-10-08 | Upgrade 10 "Market weather": `engine/weather.py`, `reports/market_weather.json`, Telegram `/weather`, the 08:20 briefing email, Claude's fact sheets |
| 2026-10-09 | Forward Test Program PR 1 "Strategy lab": 10 strategies × 4 versions (`strategies_program.yaml`), the 4H + 1H gate (1W / 1D context only), 5 years of 30m / 15m history, nightly batches, `reports/program.md` (per coin, after and before fees) - `docs/PROGRAM.md` |
| 2026-10-09 | Forward Test Program PR 3 "weekly review": `reports/weekly_review.md` (live TEST / PAPER per strategy / version / coin, after and before fees, by market type, honest confidence, 5m comparison, ideas, system check), promote with a Telegram tap (max 5, one per strategy per coin), automatic demotion, `/review`, weekly email part |
| 2026-10-10 | 👀 Watch notes: a Telegram note as soon as a TEST setup is found, while it waits for its 5m candle (information only, `/watch on|off`, at most 12 a day) |
| 2026-10-10 | "PC is off" alarm: the live watcher sends GitHub an hourly heartbeat (branch `watcher-heartbeat`, journal-sync token); the hourly scan emails an ALERT after 2 silent hours and a FIXED when it is back (`journal_review.py`, `notify.py system`, `reports/watcher_health.json`); weekly research Routine moved to Sunday 11:52 Beijing |
| 2026-10-10 | Failure Lab: the research run writes one repair card a night for a loss cause (30+ losing trades) of a testing or near-miss failed strategy, judges each repair against its parent and learns which repairs work (`engine/failure_lab.py`, `docs/FAILURE_LAB.md`) |
| 2026-10-09 | Forward Test Program V5: the fast 4H trend (4H EMA20 / EMA50) gate on the 7 trend strategies' faster timeframes (`gate: intraday_fast`) |
| 2026-10-09 | Forward Test Program PR 2 "Signal Center": 🔵 TEST alerts (positive pairs, 5m check, merged, ⭐, ⚠️ vs daily, max 10 a day), new alert layout with $ and ℹ️ Details, `/tests on|off`, demo book, `/weather` in Beijing time, TEST setups recorded on GitHub, `7_replay_test_alerts.bat` |

## The Forward Test Program (agreed 2026-10-09, `docs/PROGRAM.md`)

10 different strategies × 4 versions, backtested on 5 years per coin, then watched live; Claude's weekly review
promotes the best to 🟡 PAPER each week (the operator's one tap), 20 good paper trades + the operator's "yes" = 🟢 LIVE.
1. **PR 1 - strategy lab**: **built 2026-10-09** (see Done).
2. **PR 2 - Signal Center** (**built 2026-10-09**): silent live tracking of every positive strategy / version / coin, 🔵 TEST alerts for the
   best (max 10 a day, merged duplicates, 5m confirmation, ⭐ timeframe agreement, weather line, ⚠️ against-the-daily
   mark), the new alert layout (✅ Took it / ❌ Skip / ℹ️ Details, $ size, margin at 3x, stop / TP1 in $, past win
   chance), `/tests on|off`, demo book (TEST trades never touch the loss limits), market type saved per alert,
   `/weather` in Beijing time, a 2-week replay check before switching on.
3. **PR 3 - weekly review** (**built 2026-10-09**): per strategy / version / coin / market type before and after fees, honest confidence,
   automatic version ideas, promote (>= 10 live trades, positive after fees, one tap) / demote, max 5 in paper (one
   per strategy per coin), a system check at the top.
4. Still needed before the first real-money strategy: the $1000 account replay and the LIVE health check.

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
- Not yet: "trend turned" warnings and the strategy's own early-exit rule (not in the follow-up; the time stop is).
- **Journal sync** (built 2026-10-06, `engine/journal.py`, `journal_review.py`): with a GitHub token
  (`windows\6_journal_sync.bat`) the watcher uploads the journal to the branch `journal`; every alert is followed
  silently for its plan result (skipped ones too); `/result 1.2` records the operator's real result; the hourly scan
  writes `reports/journal_review.*` (took vs skipped by the plan, real vs plan gap, early closes) for the weekly
  email and Claude's fact sheets. Report only - nothing changes a gate, cost or approval.

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

### Optional upgrades - the operator picks one later (agreed 2026-10-07; 7-11 added the same day)
Nothing here is started until the operator names it. Suggested first, once PAPER alerts run (after 10 Oct): 1 or 4.
1. **Free Oracle cloud server**: run the live watcher there (guide: `docs/LIVE_WATCHER.md`), so alerts no longer
   depend on the lab PC.
2. **Live price stream**: OKX WebSocket for the trades being followed, so TP / stop messages come within a second
   instead of up to 5 minutes (entry signals stay at the candle close).
3. **Claude researches from the losses**: each week, new strategy ideas aimed at the main loss causes (the "still
   open" part of step 5), tested like any card. **Built 2026-10-10 as the engine's Failure Lab** (`docs/FAILURE_LAB.md`).
4. **Health check on live strategies**: alerts of a strategy pause by themselves when its recent results drift below
   its backtest (only ever pauses - never loosens a rule).
5. **More coins**: step 6 above (~15 coins instead of 7).
6. **TradingView alerts as a backup**: alert conditions added to the Pine export (`pine_export.py`) for the
   strategies in paper trading or approved.
7. **Controlled adaptive agent ("regime autopilot")** - the operator's idea (2026-10-07: track the market, understand
   the regime, upgrade itself fast, follow risk management) under one rule: *fast to protect, slow to change rules*.
   Ideas to build in parts, each one switchable by the operator (an `autopilot:` block in config.yaml + Telegram
   commands), every automatic action logged and announced:
   - autonomy levels: 0 report only · 1 automatic defence (pause / smaller size) · 2 switch between already-tested
     strategies by regime · 3 propose new rules (never live without the full tests and the operator's yes);
   - regime scoreboard: per market type, which tested strategies work; the agent turns them on / off when the regime
     changes;
   - drift check (upgrade 4) with a statistical test against the backtest, not "N losses in a row";
   - size dial between 0.25x and 1x only (never above the normal risk), lower when the regime is unclear, strategies
     disagree or volatility jumps;
   - champion / challenger: candidate strategies run in silent paper mode next to the live ones, so evidence for
     promotion collects from live data faster;
   - Telegram controls: `/autopilot on|off`, `/risk 0.5`, `/defensive` - the operator can always override.
8. **Local runner** (no GitHub Actions needed): research, scan and emails on the operator's own always-on computer -
   see `docs/BACKUP_AND_RESTORE.md`, Way 2.
9. **Crowding filter (funding + open interest)**: skip longs when the market is crowded long (high positive funding,
   rising open interest), shorts mirrored; liquidation-cascade setups as a second idea. Data already recorded hourly
   (`derivs.py`). Tested like any card (twin without the filter).
10. **"Market weather"** - **built 2026-10-08** (operator: "build number 10"): every hourly scan writes
    `reports/market_weather.json|md` (`engine/weather.py`): a verdict from the agent's own timeframe agreement (trend
    day up / down, mixed, range, choppy, news risk), per coin the 1D / 4H / 1H labels, volatility (daily ATR %
    percentile of the last year), the usual 24h move on similar past days (measured, not a forecast), crowding
    (funding, 24h open interest), altcoins vs BTC, Fear & Greed, events. Telegram `/weather`, the 08:20 briefing email
    (and "Market weather: x → y" in the 14:20 / 21:20 changes), Claude's fact sheets. Explains only - no signal, gate,
    size or approval reads it. Not included: BTC dominance (no data source in the agent yet) and a dashboard tile.
11. **Stock / gold research experiment (backtest only)**: run the existing strategies on gold and S&P 500 / Nasdaq
    ETFs (daily and 4H) to look for a second edge that doesn't move with crypto. Counted in the trials counter like
    every test; nothing is traded before it passes the same gates and paper trading. Notes from the 2026-10-07
    discussion: overnight gaps, the US pattern-day-trader rule under $25,000, broker access and data costs.

## The operator's to-do list

| When | What |
|---|---|
| Now | Double-click `windows\4_update.bat` once to get the Telegram commands and buttons |
| After the update | Optional: double-click `windows\6_journal_sync.bat` (GitHub token) so the agent learns from your trades; send `/result 1.2` after each trade |
| After the next research email | Compare the playbook versions (originals vs -LDN / -15M / -W20 / -LIMIT / -GRADED / -APLUS) |
| ~~On or after 2026-10-10~~ | **Done 2026-10-10:** family gates active (`mode: active`, `operator_ok: 2026-10-10`) - the 4H Donchian strategies can reach PAPER_TRADING from the next research run |
| After PR 1 is merged | Nothing to do: the research run tests 2 program strategies a night; read `reports/program.md` after ~5 nights |
| Sundays from 12:00 Beijing | Read the weekly review in Telegram (`/review` any time); tap "🟡 Promote" for a candidate you want in PAPER (journal sync on), or add its line under `promotions:` in `config.yaml` |
| After PR 2 is merged | `windows\4_update.bat`; TEST alerts start by themselves as the nightly research finds positive pairs (`/tests off` stops them). Optional: `windows\7_replay_test_alerts.bat` |
| Later | Approve a strategy when the weekly email shows 20 good paper trades (copy its approval line) |
| Optional | If the old Claude tasks still exist in the Claude desktop app, delete them (the cloud Routines replace them) |
