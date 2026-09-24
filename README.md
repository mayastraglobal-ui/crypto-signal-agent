# Crypto Signal Agent

This agent runs by itself on GitHub's free servers every hour, whether your PC is on or off. Each run it:

1. **Picks coins.** 7 "signal" coins + 3 "research" coins (see "Which coins" below). It skips meme, AI, stable, wrapped, gold and leveraged coins, coins with less than 180 days of history, and coins that fail the volume, spread, order-book or ±25% rules.
2. **Downloads charts.** It gets 1W, 1D, 4H, 1H, 30m, 15m and 5m candles for every coin, and builds rolling 7-day candles (see "Timeframes" below).
3. **Checks the data is trustworthy** (see "Data check" below). Bad data = no signals.
4. **Backtests every strategy** in `strategies.yaml` on every coin, including fees and slippage.
5. **Throws away strategies that fail.** Each strategy has to be profitable in both the "training" period and an "unseen test" period, and has to pass the rules in `config.yaml`.
6. **Gives signals** from the strategies that pass. Each signal has an entry zone, stop-loss, TP1, TP2, TP3, hold time, position size and the reasons behind it.
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
| `reports/strategy_scoreboard.csv` | Pass/fail table for every strategy and timeframe | No |
| `reports/data_quality.json` | Result of the data check, per coin and timeframe | No |
| `reports/universe.json` | Every candidate coin this run: rank, numbers, pass/fail reasons | No |
| `reports/features.json` | Newest features per coin and timeframe | No |
| `reports/feature_evidence.json` | Candle patterns vs random entries (research evidence, not a signal) | No |
| `memory/feature_notes.md` | What each feature means and whether it has been proven useful | Read it |
| `reports/universe_state.json` | The agent's memory of the 2-run counts | No |
| `memory/universe_log.md` | Every coin that joined, left or was excluded, and why | Read it |
| `engine/` | Parts of the engine (data check, coins, timeframes, features, evidence, more later) | Not needed |
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

## Adding a strategy

1. Open `strategies.yaml` → click the pencil icon ✏️.
2. Copy an existing block to the bottom, give it a new `name`, set `status: candidate`, and change the rules.
3. Commit. The next hourly run backtests it. If it passes, it starts giving signals. If not, the scoreboard tells you why.

If a rule has a typo, the run log (Actions tab) shows `RULE ERROR` and the strategy is skipped. Nothing else breaks.

## Notes

- If GitHub ever pauses the schedule, open the Actions tab and re-enable it. This can happen after 60 days with no activity; the hourly report commits normally count as activity.
- Data source: Binance public market data, with OKX as a backup. The coin filters are in `config.yaml`.
