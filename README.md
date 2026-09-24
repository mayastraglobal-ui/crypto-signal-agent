# Crypto Signal Agent

This agent runs by itself on GitHub's free servers every hour, whether your PC is on or off. Each run it:

1. **Picks coins.** It takes the ~25 highest-volume USDT coins and skips meme, AI and stable coins, plus any coin with less than 180 days of history.
2. **Downloads charts.** It gets 4H, 1H, 30m, 15m and 5m candles for every coin.
3. **Backtests every strategy** in `strategies.yaml` on every coin, including fees and slippage.
4. **Throws away strategies that fail.** Each strategy has to be profitable in both the "training" period and an "unseen test" period, and has to pass the rules in `config.yaml`.
5. **Gives signals** from the strategies that pass. Each signal has an entry zone, stop-loss, TP1, TP2, TP3, hold time, position size and the reasons behind it.
6. **Checks old signals** against what the price actually did afterwards. A strategy whose real results turn bad gets paused automatically.
7. **Writes the report** to `reports/latest.md`, which you can read on the GitHub website or app.

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
| `config.yaml` | Account size, risk %, coin filters, fees, TP1/2/3 split, pass/fail rules | Yes, this is your control panel |
| `strategies.yaml` | Every strategy, written as simple rules | Yes, add new ideas here |
| `scanner.py` | The engine | Not needed |
| `reports/latest.md` | Newest report (for you) | No, it's generated |
| `reports/latest.json` | Same report in data form (for Claude) | No |
| `reports/signals_log.csv` | Every signal ever given and how it ended | No, it's the live track record |
| `reports/strategy_scoreboard.csv` | Pass/fail table for every strategy and timeframe | No |

## Adding a strategy

1. Open `strategies.yaml` → click the pencil icon ✏️.
2. Copy an existing block to the bottom, give it a new `name`, set `status: candidate`, and change the rules.
3. Commit. The next hourly run backtests it. If it passes, it starts giving signals. If not, the scoreboard tells you why.

If a rule has a typo, the run log (Actions tab) shows `RULE ERROR` and the strategy is skipped. Nothing else breaks.

## Notes

- If GitHub ever pauses the schedule, open the Actions tab and re-enable it. This can happen after 60 days with no activity; the hourly report commits normally count as activity.
- Data source: Binance public market data, with OKX as a backup. The coin filters are in `config.yaml`.
