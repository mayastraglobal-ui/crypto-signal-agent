# Crypto Signal Agent

This agent runs by itself on GitHub's free servers every hour, whether your PC is on or off. Each run it:

1. **Picks coins.** 7 "signal" coins + 3 "research" coins (see "Which coins" below). It skips meme, AI, stable, wrapped, gold and leveraged coins, coins with less than 180 days of history, and coins that fail the volume, spread, order-book or ±25% rules.
2. **Downloads charts.** It gets 1W, 1D, 4H, 1H, 30m, 15m and 5m candles for every coin, and builds rolling 7-day candles (see "Timeframes" below).
3. **Checks the data is trustworthy** (see "Data check" below). Bad data = no signals.
4. **Backtests every strategy** in `strategies.yaml` on every coin, including fees and slippage - but only in the market regimes each strategy allows, and only when the bigger timeframes agree (see "Strategies" below).
5. **Once a day, tests every strategy on years of history** (see "Daily research run" below) and moves it along its lifecycle: BACKTESTING, VALIDATION, FAILED, PAPER_TRADING or RETIRED.
6. **Gives signals only from strategies you APPROVED** (after paper trading). Strategies in PAPER_TRADING or VALIDATION show "paper / validation signals" in the report, which are logged but never emailed. Each signal has an entry zone, stop-loss, targets, hold time, position size and the reasons behind it.
7. **Checks old signals** against what the price actually did afterwards. A strategy whose real results turn bad gets paused automatically.
8. **Writes the report** to `reports/latest.md`, which you can read on the GitHub website or app.

It **never trades for you** and never needs your exchange password or API keys.

## One-time setup (about 15 minutes, no coding)

1. Create a free account at https://github.com.
2. Click **+** (top right) → **New repository**.
   - Name: `crypto-signal-agent`
   - Choose **Public**. Public repos get unlimited free running time, and there are no secrets in this project.
   - Click **Create repository**.
3. On the new repo page, click **uploading an existing file**. Drag in **all the files and folders** from the zip, including the `.github` folder, then click **Commit changes**.
   - The `.github` folder is hidden on Mac/Windows. If it doesn't upload, do this instead:
     - Click **Add file → Create new file**.
     - Type the name `.github/workflows/scan.yml`.
     - Paste in the contents of `scan.yml` and commit.
4. Go to **Settings → Actions → General → Workflow permissions**, choose **Read and write permissions**, and click **Save**.
5. Go to the **Actions** tab. If asked, click **I understand my workflows, go ahead and enable them**.
6. Click **Crypto Signal Scan → Run workflow** to start the first run now. It takes about 3–6 minutes.
7. Open `reports/latest.md` to see your first report. From now on it updates every hour.
8. Send Claude your repo link (`https://github.com/<your-username>/crypto-signal-agent`). Claude then sets up its
   three scheduled tasks for you (briefings, daily review, weekly research - see "Claude's tasks" below).

## Files

| File | What it is | Should you edit it? |
|---|---|---|
| `config.yaml` | Account size, risk %, coin rules, fees, data checks, TP1/2/3 split, pass/fail rules | Yes, this is your control panel |
| `strategies.yaml` | Every strategy, written as simple rules | Yes, add new ideas here |
| `scanner.py` | The engine | Not needed |
| `reports/latest.md` | Newest report (for you) | No, it's generated |
| [`reports/latest.json`](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/latest.json) ⓛ | Same report in data form (for Claude) | No |
| `tasks/` | What Claude's scheduled tasks do (briefing, daily review, weekly research) + their rules | Read it |
| `reports/claude/` | Claude's briefings, daily reviews and weekly research (checked by the Brain guard) | No |
| `reports/approval/` | Approval packs of strategies ready for your yes / no | Read it |
| `brain_guard.py`, `brain_pack.py` | The guard that checks Claude's work before main; the fact sheet Claude reads | Not needed |
| `reports/signals_log.csv` | Every signal ever given, its current state and how it ended | No, it's the live track record |
| `reports/positions.json` | The position book right now (active, awaiting 5m, paper, closed today) + what is being watched | No |
| `reports/position_events.csv` | Every state change of every signal, one line each (never rewritten) | No |
| `reports/risk_state.json` | Current risk halts and suspended strategies (so each change is emailed once) | No |
| `reports/strategy_scoreboard.csv` | Status table for every strategy version and timeframe | No |
| [`reports/data_quality.json`](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/data_quality.json) ⓛ | Result of the data check, per coin and timeframe | No |
| `reports/universe.json` | Every candidate coin this run: rank, numbers, pass/fail reasons | No |
| [`reports/features.json`](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/features.json) ⓛ | Newest features per coin and timeframe | No |
| [`reports/regime.json`](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/regime.json) ⓛ | Market regime per coin and timeframe, with evidence | No |
| [`reports/smc.json`](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/smc.json) ⓛ | SMC state and newest events per coin and timeframe | No |
| `memory/smc_events.csv` | Every SMC detection, logged live when it happened | Read it |
| `memory/smc_research.md` | Exact SMC definitions and what has been proven | Read it |
| `memory/market_regime_log.md` | One regime entry per day, BTC context first | Read it |
| [`reports/feature_evidence.json`](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/feature_evidence.json) ⓛ | Candle patterns vs random entries (research evidence, not a signal) | No |
| `memory/feature_notes.md` | What each feature means and whether it has been proven useful | Read it |
| `reports/universe_state.json` | The agent's memory of the 2-run counts | No |
| `memory/universe_log.md` | Every coin that joined, left or was excluded, and why | Read it |
| `engine/` | Parts of the engine (data check, coins, timeframes, features, evidence, regime, SMC, more later) | Not needed |
| `tests/` | Automatic tests | Not needed |
| `memory/changelog.md` | Log of every rule / setting change | Read it; Claude updates it |
| `memory/README.md` | Index of every memory file: contents, who writes it, when, append-only or not | Read it |
| [`reports/research.json`](https://github.com/mayastraglobal-ui/crypto-signal-agent/blob/live-reports/reports/research.json) ⓛ | Daily research run: Layers A/B/C, stress, ±20%, why trades lose, missed moves | No |

ⓛ = **on the branch `live-reports`**, not on main. These large files are fully replaced every run, so they are
published there as one single commit (`publish_live.py`) and do not pile up in the repository's history.
Main keeps the history that matters: `memory/`, `reports/signals_log.csv`, `reports/position_events.csv`,
`reports/positions.json`, `reports/strategy_scoreboard.csv`, `reports/daily/` and `reports/latest.md`. The report's top line shows the repository size.

## Which coins (every run)

- **Signal coins (7):** the 7 eligible coins with the most trading in the last 24 hours.
  Only these can give signals. BTC and ETH are always included when eligible.
- **Research coins (3 more):** the next 3. They are backtested, but never give a signal.
- **Eligible** means ALL of: 180+ days of history · $50M+ volume in 24h and on average over 7 days ·
  no one-day volume spike (24h > 3x the 7-day average) · moved less than ±25% in 24h (otherwise
  suspended for the rest of the UTC day) · spread ≤ 0.10% · $250k+ of orders within 1% of the price
  on each side · price data not UNSAFE · not on an exclusion list · does not behave like a stablecoin.
- **No jumping around:** a new coin must be in the top 7 for **2 runs in a row** to join, and a member
  must be outside the top 7 for 2 runs in a row to leave. A member that breaks a rule leaves at once.
- Every join, leave and exclusion is written to `memory/universe_log.md` with its reason.
  The limits are in `config.yaml` → `universe`.

## Timeframes

A timeframe is how long one candle lasts (1W = one week, 5m = five minutes). The agent works
**top-down**: slow timeframes give **permission** (which direction is allowed), fast timeframes give
**timing** (when to act). The default model (Model B, `config.yaml` → `timeframe_model`) is:
**1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry**.

- A candle only ever uses higher-timeframe candles that had **already closed** (a Wednesday candle
  sees last week's weekly candle, never the unfinished current week). Tests check this every push.
- **7D** = a rolling "week" that ends today, built from the daily candles.
- **Cross-check:** every bigger candle must agree with the smaller candles inside it (a 4H high must
  equal the highest of its four 1H highs). If not, that timeframe is DEGRADED - no signals from it.
- The report section "0c. Timeframes loaded" shows the candle counts per coin and the cross-check.

## Features and candle evidence

- **Features** (`engine/features.py`, limits in `config.yaml` → `features`): exact measurements of each
  closed candle - candle shape, momentum, relative volume, displacement / engulfing / pin-bar candles,
  confirmed swings and HH/HL/LH/LL structure, support/resistance, breakouts, retests, impulses,
  pullbacks, RSI divergence, and extra indicators (Stochastic RSI, ROC, Keltner, VWAP, OBV).
  A swing only "exists" once the 3 candles after it have closed. Nothing trades on features yet;
  report section "0d" shows them for the signal coins on 1H. Definitions: `memory/feature_notes.md`.
- **Candle evidence** (report section "0e", `reports/feature_evidence.json`) - **research evidence, not a
  signal**: after each displacement / engulfing / pin-bar candle, how often did price reach +1R / +2R /
  +3R after costs before a 1-ATR stop - compared with the same test on **random** candles. Only a clear
  gap over random ("beats chance") is interesting.

## Market regime

The market's "mood" per timeframe (1W, 1D, 4H, 1H) for every coin: STRONG_BULL, WEAK_BULL, RANGE,
HIGH_VOL_RANGE, WEAK_BEAR, STRONG_BEAR, EXPANSION, COMPRESSION, TRANSITION or UNCLEAR - with the evidence
for and against, and a confidence of strong / moderate / weak (never a %). **Permission:** LONG needs at
least 2 of 1D/4H/1H bullish and no STRONG_BEAR on 1W; SHORT is the mirror image; otherwise NO TRADE.
Report section "0f"; full evidence in `reports/regime.json`; one entry per day in
`memory/market_regime_log.md`. Regimes and permission **gate every strategy** (see "Strategies").
Rules and limits: `config.yaml` → `regime`.

## SMC (Smart Money Concepts) - hypotheses, not doctrine

Liquidity pools (swing highs/lows, equal highs/lows, previous day/week high/low), sweeps, BOS, CHoCH
(needs a displacement candle), fair value gaps, order blocks, breakers, premium/discount, OTE,
killzones (New York time) and power of 3 - each an exact rule on closed candles
(`engine/smc.py`, limits in `config.yaml` → `smc`, definitions in `memory/smc_research.md`).
Every detection on the signal coins (4H/1H/30m/15m) is logged live in `memory/smc_events.csv`, so no
label can be drawn in afterwards. Report section "0g" shows the current SMC picture; sweeps, BOS, CHoCH
and FVG retraces also appear in the candle-evidence table vs random entries. Strategies S5-S8 are built
from these rules and must beat a "control twin" (the same idea without the SMC part).

## Data check (every run)

Before anything else, every candle table is checked for missing, duplicate or unfinished
candles, impossible prices (zero, negative, high below low), a feed that has stopped updating,
freak volume, and a price difference of more than 0.5% between Binance and OKX.
The result is one of three states, shown at the top of `reports/latest.md`:

| State | Meaning |
|---|---|
| **GOOD** | Signals allowed |
| **DEGRADED** | That coin/timeframe is analysis only - no signals from it |
| **UNSAFE** | No signals from it. If BTC is UNSAFE, or more than 30% of coins are, **all** signals stop (`DATA_STALE / SIGNAL_DISABLED`) and you get one `[SYSTEM]` email - plus one more when the data recovers |

The limits are in `config.yaml` → `data_quality`. Full details are in `reports/data_quality.json`.

## Costs

Every backtest pays realistic costs (`config.yaml` → `costs`): **LONG** trades use Binance
**spot** fees; **SHORT** trades are **futures only** and use Binance futures fees plus a
funding fee that is always counted against you.

## Tests

`python tests/run_all.py` runs the automatic tests, several test files at a time (about 3 minutes; no
internet needed). `python -m unittest discover -s tests -v` runs the same tests one after another.
They also run on GitHub on every push: see the **Tests** workflow in the Actions tab
(green tick = OK, red cross = something broke).
`python scanner.py --offline --fault stale_btc` shows what happens when data goes bad
(offline test data only).

## Strategies (spec v3)

Every strategy in `strategies.yaml` is an "ID card": id, version, family, the idea it tests (hypothesis),
allowed market regimes, a gate type, rules, stop, targets, time stop, cooldown, known weaknesses and a
changelog. The comments at the top of the file explain every field.

- **Lifecycle:** IDEA → FORMALIZED → BACKTESTING → VALIDATION → PAPER_TRADING → APPROVED. You set IDEA,
  FORMALIZED or RETIRED; the engine sets the rest per version and timeframe, once a day
  (`memory/strategy_registry.csv`, changes in `memory/strategy_lifecycle.md`). **APPROVED always needs your
  yes**. Only APPROVED strategies send `[ENTRY]` emails.
- **Market gates:** a strategy only trades in the regimes it lists. Trend, breakout and SMC strategies
  need 2 of 1D/4H/1H in their direction and never trade against a STRONG weekly trend; reversal types
  skip the weekly veto; mean-reversion strategies trade only in ranges and never against a STRONG
  1W/1D/4H trend.
- **Pass bar (VALIDATION):** see "Daily research run". Each re-tuned version of the same idea needs +0.02R
  more (`memory/experiments.md` counts every version tested). **params:** the numbers in a rule have names
  (`{fast}` with `fast: 20`) so the research run can move them ±20%.
- **A tested version never changes.** To change rules, copy the block, raise the version
  ("1.0" → "1.1") and add a changelog line. If a tested version's rules are edited in place, the engine
  refuses to run it and the report says why.

## Daily research run

Once a day (00:40 UTC, workflow **Research** - you can also start it by hand in the Actions tab), `research.py`
tests every strategy version on every timeframe on years of history (AGENT_PROMPT.md sections 11-12):

| Test | What it asks |
|---|---|
| **Layer A** (hourly) | How did it do in the last 15 days (days 1-10 vs 11-15)? Shown only - never enough alone |
| **Layer B** | On all history since the coin was listed (1D/4H/1H; 30m 2 years, 15m 1 year, 5m 90 days): ≥ 30 trades, ≥ +0.10R per trade, PF ≥ 1.2, drawdown ≤ 10R, profitable in the first 70% ("develop") AND the last 30% ("validate") of every coin, and fees ≤ 1/4 of the stop |
| **Layer C** (walk-forward) | History cut into 6 time windows (the first only warms up): at least 3 of the other 5 profitable, and all 5 together |
| **Costs +50%** | Still profitable when fees, slippage and funding are 50% higher? |
| **±20% test** | Still profitable when each number in the rules (and the stop and hold time) is moved 20% down or up, one at a time? |
| **Coins / overfitting** | Profitable on ≥ 3 coins, and no more than half of the profit from one coin or one window |
| **Control twin** | For SMC strategies: better than the same idea without the SMC part, overall and in the validate part. For `-5M` strategies: better than the same strategy without the 5m check (tested on the 90 days of 5m history, which also sets their develop / validate split and walk-forward windows) |

Passing everything moves a strategy to **PAPER_TRADING** automatically: its signals are logged as paper trades,
never emailed. A paper strategy is **RETIRED** if its last 20 paper signals average below -0.10R or it loses more
than 8R, and leaves paper if it fails Layer B two days in a row. **APPROVED** only ever comes from you.
Results: report sections 3 / 3b / 3c and `reports/research.json`. Long price history is kept in GitHub's Actions
cache (not in the repo) and only new candles are downloaded each day. Settings: `config.yaml` → `research`.

## Signal states, 5-minute confirmation and the position book

Every signal of a strategy in VALIDATION or higher is followed through fixed states (AGENT_PROMPT.md
sections 8, 13, 16; `engine/positions.py`, `engine/confirm5m.py`):

`WATCH → SETUP_FORMING → AWAITING_5M → ENTRY_TRIGGERED → POSITION_ACTIVE → TP1_HIT (stop to breakeven) → CLOSED`,
or `EXPIRED` (no 5m confirmation) / `INVALIDATED` (stop or 5m structure broken before entry).

- **WATCH / SETUP_FORMING** (report section 2c only): the strategy's trend / regime filters are open, or all its
  entry rules but one are true - the missing rule is shown.
- **5-minute confirmation:** strategies whose card says `confirm_5m: true` (the `-5M` versions of S5-S8) do not
  enter at the 15m / 30m candle. They wait up to 6 closed 5m bars for one that closes in the trade direction
  (body ≥ 50%, volume ≥ average, price still within entry ± 0.2R); none → EXPIRED, no trade. Each is compared
  with the same strategy without the check, over the same period on the same 5m bars - the check is kept only if
  it helps. Settings: `config.yaml` → `confirm_5m`.
- **Open positions** are managed exactly like the backtest: stop, targets, breakeven after TP1, time stop and the
  strategy's exit rule. An opposite structure break, a strong opposite candle, a regime change or a volatility
  spike only adds a **"watch: ..."** note - they were never tested, so they never close a position.
- **Position book:** the first thing in every report and email - active (APPROVED) positions, setups
  awaiting 5m, paper positions, today's closed ones with R, and day / week R and heat against the limits
  (-3R / -6R / 3; shown now, enforced by the risk engine in Phase 11).

The scan runs hourly, so each run replays the 5m and other candles since the previous run: the recorded result is
exact, but a live alert can be up to an hour late (a faster schedule is a later decision).

## Memory

What the agent remembers is in `memory/` (AGENT_PROMPT.md section 22; index: `memory/README.md`). The engine
writes facts only - losing signals (`failure_journal.md`), missed strong moves (`missed_trades.md`), the source
and claim behind every strategy version (`research_sources.md`, never an invented citation), data problems when
they start and end plus fee settings (`execution_notes.md`) and weekly measured facts per signal coin
(`coin_notes.md`). `lessons.md` is written only after a review (Claude or you), never automatically. Each of these
entries carries timestamp, source, evidence class, confidence, strategy, coin, timeframe, regime and a review date;
report section 3e lists the files and the reviews that are due. **Append-only files can only grow:**
`memory_guard.py` stops a run before anything is committed if an earlier line was changed or removed.

## Emails

All emails are written by the engine itself (no AI), open with the position book and end with
"Research signal. Not financial advice." (AGENT_PROMPT.md section 20; `notify.py`, content from `engine/briefs.py`).
Setup: the `GMAIL_USER` / `GMAIL_APP_PASSWORD` secrets (see One-time setup). Without them nothing is sent and
nothing breaks.

| Email | When | What |
|---|---|---|
| `[ENTRY] LONG ETH/USDT \| 15m \| S6-OB-FVG v1.0 \| R:R 2.4` | a new signal of an **APPROVED** strategy passes the risk engine (-5M strategies: when the 5m bar confirms) | UTC + Beijing time, data state, spot / futures only, regime 1W → 5m, entry zone, stop, targets, R:R, 5m bar, size, expiry, 3-5 reasons measured at the signal, what cancels it, evidence (Layers A/B/C, paper, live), **chart image** |
| `[EXIT] ETH/USDT LONG \| TP1 / TP2 / BE / TRAIL / SL / TIME / EXIT_RULE` | an APPROVED position reaches TP1 or closes | realised R, reason, next action, chart |
| `[SYSTEM]` | data unsafe / recovered, scan or research failed, risk halt or suspension starts / ends, a strategy is APPROVED while scans are still hourly | what happened and what to do |
| `[DAILY]` | first scan after 00:00 UTC (08:00 Beijing) | BTC context, the signal coins (price, 24h volume, regimes 1W/1D/4H/1H, 30m momentum, 15m setup, 5m trigger), position book, strategy status changes, event calendar |
| `[WATCH]` | only if `signals` → `email_watching: true` | setups of APPROVED strategies that are forming or waiting for 5m - not signals |
| `[WEEKLY] 2026-W39 - live ... paper ...` | Sunday, first scan from 04:00 UTC (12:00 Beijing) | results of the week (LIVE / PAPER / VALIDATION apart), scoreboard, lifecycle changes, why trades lost, SMC control-twin findings, missed moves, **approval packs with the yes/no question**, then Claude's weekly research (if it ran) |
| `[BRIEFING] 2026-09-25 08:20 Beijing - ...` | after each Claude briefing (08:20 / 14:20 / 21:20 Beijing, about 15-30 min later) | written by Claude: position book, regime, news with sources, signals explained, do / don't today |

Each email is sent once. Waiting-for-5m, expired and invalidated setups are shown in the report only (no noisy
alerts), and a signal found late whose trade already ended in the same run is not emailed. Chart images are email
attachments only (not stored in the repository). `[DAILY]` also shows the summary of yesterday's Claude daily
review, marked as written by the AI. Everything except `[BRIEFING]` and Claude's part of `[WEEKLY]` works without
Claude.

## Claude's tasks (the "Brain")

Three scheduled Claude tasks (Routines in your Claude account; AGENT_PROMPT.md section 19). Claude **explains and
researches**; every number comes from the engine (`brain_pack.py` prints the fact sheet it must quote).

| Task | When | Instructions | Output |
|---|---|---|---|
| Briefing | 08:20 / 14:20 / 21:20 Beijing | `tasks/briefing.md` | `reports/claude/briefings/` + `[BRIEFING]` email |
| Daily review | 23:30 Beijing | `tasks/daily_review.md` | `reports/claude/daily/` (summary in the next `[DAILY]`), memory records: root causes, reviews due, validated lessons, queued refinements (max one per failing strategy) |
| Weekly research | Sunday 10:00 Beijing | `tasks/weekly_research.md` | `reports/claude/weekly/` (in `[WEEKLY]`), sources, 1-2 candidate strategies **as pull requests for you to merge** |

**How Claude's work reaches main safely:** a task never writes to main. It pushes to its own branch
(`claude/brain-briefing`, `-daily`, `-weekly`). Every 15 minutes the **Brain workflow** (`brain.yml`, always run
from main) checks new pushes with `brain_guard.py`:
- allowed: new files in `reports/claude/` with the expected name, and new records **added at the end** of the
  knowledge files (lessons, failure journal, missed trades, sources, coin notes, feature notes, SMC research,
  experiments);
- refused: any code, `config.yaml`, `strategies.yaml`, workflow or engine file; any change or deletion of an
  earlier line; records without the section 22 fields; lessons without strong evidence and counts; profit
  promises or win probabilities ("guaranteed", "risk-free", "high probability", "70% chance this trade wins").

One problem refuses the whole push - nothing is half-applied - and you get one `[SYSTEM]` email saying why.
New strategy ideas never enter testing by themselves: they arrive as pull requests, tested only after you merge.
Two runs adding to the same memory file at the same time keep both sides' lines (`.gitattributes`, union merge).

## Approving a strategy (your yes)

A strategy goes live (its signals get `[ENTRY]` emails) only with your explicit yes (AGENT_PROMPT.md sections 12,
21). The daily research run writes an **approval pack** (`reports/approval/`) for every PAPER_TRADING strategy
version × timeframe with at least 20 closed paper signals, a paper average of 0R or better, and a paper average
no more than 0.30R below the backtest on unseen data (`config.yaml` → `approval`). The pack shows the rules and
lineage, Layers A/B/C, walk-forward, paper results, the control twin, the ±20% test, the cost stress test, risk,
why it loses and its limitations. The `[WEEKLY]` email asks *"Approve S6-OB-FVG v1.0 15m for live emails?
(yes/no)"*.

- **Yes:** copy the line from the pack into `config.yaml` → `approvals:` (on GitHub: open the file, pencil icon,
  commit). The next daily research run moves it to APPROVED and logs it in `memory/strategy_lifecycle.md`.
- **No:** do nothing. **Changed your mind:** delete the line - it goes back to PAPER_TRADING.
- An approval for a strategy that is not (or no longer) eligible is not applied; the report says why. The
  retirement rules keep watching approved strategies, now on their live results too.

## Risk engine and news blackout

A separate part of the engine (`engine/risk.py`, AGENT_PROMPT.md sections 14-15; settings `config.yaml` → `risk`)
decides whether the account may take a live trade **now** and how big it may be. It never changes a strategy.

| Rule | What happens |
|---|---|
| High-impact event within ±60 min | no live entry (calendar: `config.yaml` → `events`) |
| Today's closed live results ≤ −3R / this week's ≤ −6R | no new live entries for the rest of the day / week; one `[SYSTEM]` email when it starts and one when it ends |
| A live strategy (version × timeframe) more than 8R below its best | SUSPENDED until you add it to `risk` → `resume` with a date |
| Heat | at most 3 open live positions, 1 per coin, 1 per direction in a group of coins that move together (1h correlation ≥ 0.7 over 30 days) |
| Reward to TP1 | at least 2R - the stop is never widened to get there |
| Path to TP1 | no opposing liquidity pool or support / resistance level before TP1 |
| Duplicate | not while the same strategy / coin / timeframe is open or in its cooldown |
| Size | account × risk% ÷ distance to the stop; risk 0.5% until 30 days after the first live entry, never above 1%; never more than 3x leverage (the position is made smaller instead) |

An APPROVED signal that fails a rule is logged as **NO_TRADE** with the reason and is not emailed. Paper and
validation signals are still logged in full (their record must stay comparable with the backtest); the
`risk_blocks` column notes which rules would have blocked them live, so each rule's value can be measured.
Report section 2d and the "Risk:" line of the position book show the state.

**Keep the event calendar filled in.** The agent does not invent dates. Add US CPI, NFP (bls.gov schedule), FOMC
(federalreserve.gov) and exchange incidents to `config.yaml` → `events` in UTC; the report warns
"calendar not maintained" when nothing is listed for the next 7 days.

Note: the older strategies take their first target at 1R, so none of them can send a live signal until a new
version with TP1 at 2R or more is written and tested.

## Why trades lose (failure attribution)

Every backtest trade, and every logged paper / live signal, gets **reason tags** by fixed rules
(AGENT_PROMPT.md section 17; `engine/attribution.py`, numbers in `config.yaml` → `attribution`): the market
at entry (choppy, against a strong higher timeframe, low volume, overextended, late, no strong candle, outside the
main sessions) and what happened (stopped then reversed, target nearly reached, false breakout, regime flipped,
volatility spike, fees ate it, ...). A tag only counts as a **systematic** cause when it is clearly more common
among losing trades than among winners. Also measured: **MAE / MFE** (how far each trade went against / for you),
results by regime, session and direction, and the 8 questions of section 17.3 per strategy (report section 3d,
`reports/research.json`). Losing paper / live signals are written to `memory/failure_journal.md`; strong moves
the strategies missed (≥ 5x the 1H ATR within 12 hours) to `memory/missed_trades.md`. Turning this into lessons
and new versions is a review step - rules are never changed automatically.

## Adding a strategy

1. Open `strategies.yaml` → click the pencil icon ✏️.
2. Copy an existing block to the bottom, give it a new `id`, `version: "1.0"`, `status: FORMALIZED`, fill in the card and change the rules.
3. Commit. The next hourly run backtests it and the scoreboard tells you its status and why.

If a card is incomplete, the report lists it under "not run". If a rule has a typo, the run log (Actions tab) shows `RULE ERROR` and the strategy is skipped. Nothing else breaks.

## Notes

- If GitHub ever pauses the schedule, open the Actions tab and re-enable it. This can happen after 60 days with no activity; the hourly report commits normally count as activity.
- Data source: Binance public market data, with OKX as a backup. The coin filters are in `config.yaml`.
