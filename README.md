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
8. Send Claude your repo link (`https://github.com/<your-username>/crypto-signal-agent`). Claude will then set up your news and market briefings.

## Files

| File | What it is | Should you edit it? |
|---|---|---|
| `config.yaml` | Account size, risk %, coin rules, fees, data checks, TP1/2/3 split, pass/fail rules | Yes, this is your control panel |
| `strategies.yaml` | Every strategy, written as simple rules | Yes, add new ideas here |
| `scanner.py` | The engine | Not needed |
| `reports/latest.md` | Newest report (for you) | No, it's generated |
| `reports/latest.json` | Same report in data form (for Claude) | No |
| `reports/signals_log.csv` | Every signal ever given and how it ended | No, it's the live track record |
| `reports/strategy_scoreboard.csv` | Status table for every strategy version and timeframe | No |
| `reports/data_quality.json` | Result of the data check, per coin and timeframe | No |
| `reports/universe.json` | Every candidate coin this run: rank, numbers, pass/fail reasons | No |
| `reports/features.json` | Newest features per coin and timeframe | No |
| `reports/regime.json` | Market regime per coin and timeframe, with evidence | No |
| `reports/smc.json` | SMC state and newest events per coin and timeframe | No |
| `memory/smc_events.csv` | Every SMC detection, logged live when it happened | Read it |
| `memory/smc_research.md` | Exact SMC definitions and what has been proven | Read it |
| `memory/market_regime_log.md` | One regime entry per day, BTC context first | Read it |
| `reports/feature_evidence.json` | Candle patterns vs random entries (research evidence, not a signal) | No |
| `memory/feature_notes.md` | What each feature means and whether it has been proven useful | Read it |
| `reports/universe_state.json` | The agent's memory of the 2-run counts | No |
| `memory/universe_log.md` | Every coin that joined, left or was excluded, and why | Read it |
| `engine/` | Parts of the engine (data check, coins, timeframes, features, evidence, regime, SMC, more later) | Not needed |
| `tests/` | Automatic tests | Not needed |
| `memory/changelog.md` | Log of every rule / setting change | Read it; Claude updates it |

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

`python -m unittest discover -s tests -v` runs the automatic tests (no internet needed).
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
| **Control twin** | For SMC strategies: better than the same idea without the SMC part, overall and in the validate part |

Passing everything moves a strategy to **PAPER_TRADING** automatically: its signals are logged as paper trades,
never emailed. A paper strategy is **RETIRED** if its last 20 paper signals average below -0.10R or it loses more
than 8R, and leaves paper if it fails Layer B two days in a row. **APPROVED** only ever comes from you.
Results: report sections 3 / 3b / 3c and `reports/research.json`. Long price history is kept in GitHub's Actions
cache (not in the repo) and only new candles are downloaded each day. Settings: `config.yaml` → `research`.

## Adding a strategy

1. Open `strategies.yaml` → click the pencil icon ✏️.
2. Copy an existing block to the bottom, give it a new `id`, `version: "1.0"`, `status: FORMALIZED`, fill in the card and change the rules.
3. Commit. The next hourly run backtests it and the scoreboard tells you its status and why.

If a card is incomplete, the report lists it under "not run". If a rule has a typo, the run log (Actions tab) shows `RULE ERROR` and the strategy is skipped. Nothing else breaks.

## Notes

- If GitHub ever pauses the schedule, open the Actions tab and re-enable it. This can happen after 60 days with no activity; the hourly report commits normally count as activity.
- Data source: Binance public market data, with OKX as a backup. The coin filters are in `config.yaml`.
