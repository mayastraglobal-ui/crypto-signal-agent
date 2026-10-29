# 📊 Trend portfolio (paper, since 29 Oct 2026)

**What it is:** a slow, always-on trend system for your 7 coins. Once a day it says how much of each coin to hold.
It is **paper only**: GitHub keeps a practice account that starts with $1,000 and follows every change after fees.
You decide later whether to use real money.

**Where it comes from:** the multi-lookback Donchian idea of Zarattini, Pagani & Barbon (2025, "Catching Crypto
Trends", SSRN 5209907), in our own version (their exact rules were not checked).

## The rules
For each coin there are **9 trend signals**, one per lookback: 5, 10, 20, 30, 60, 90, 150, 250 and 360 days (daily
candles).
- A signal turns **ON** when a day closes above the highest high of its lookback.
- It turns **OFF** when a day closes below its **mid-line**: (highest high + lowest low) / 2 of the lookback. The
  mid-line only moves up while the signal is on.
- **Target for the coin = the share of its 9 signals that are ON.** For example, 6 of 9 ON = hold 67% of that
  coin's part.
- Each coin gets an equal part of the account (1/7).
- Long only, no leverage. Decided at the daily close (00:00 UTC = 08:00 Beijing), held the next day.

The short lookbacks (5–20 days) get in early when a move starts. The long ones (150–360 days) keep you in a big
trend, and they all step out one by one when it ends.

## The test (2026-10-29)
Binance daily candles since 2018, the 7 coins, 0.10% a side on every change plus funding 0.01% / 8 h on what is held:

| | Yearly return | Sharpe | Worst drop | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Buy and hold (with funding) | 36% | 0.81 | −75% | −37% | −67% | +15% |
| Single Turtle (like strategy 13) | 9% | 0.97 | −21% | −4% | −8% | +7% |
| **Trend portfolio** | **35%** | **1.40** | **−26%** | +1% | −11% | +29% |

How robust it is:
- **Lookbacks:** other sets (10–320 days, or 20 / 55 / 120 / 250) gave Sharpe 1.30–1.40.
- **Costs:** doubled costs gave Sharpe 1.36.
- **Single coins:** one coin alone drops 40–60% at worst. Spreading over the 7 coins is what makes it work.
- **Without ZEC:** 2025 was −4% and 2026 −6% so far. It earns in big trends, and the last 2 years had few.
- **Recent stretch:** the last 1,000 days (Feb 2024 – Oct 2026) made +30% a year with a 17% worst drop. Holding made
  +59% a year with a 52% worst drop.

The study's lookbacks were fixed before testing (the paper uses 9 horizons) and are never tuned on results.

## What you get
- **One Telegram message a day** after the daily close, from about 08:00 Beijing. It shows every coin's target as
  🟩 trends up out of 9, today's changes (buy / sell how many $), and the paper account.
- **`/portfolio`** shows it any time. **`/portfolio off`** stops the daily message and `/portfolio on` starts it
  again.
- **On GitHub:** `reports/trend_portfolio.md` (targets, paper account, the last 30 days) and
  `reports/trend_portfolio.json`.

## How it runs
- `trend_portfolio.py` runs in the hourly scan, after `scanner.py`. Once per new daily close it downloads the daily
  candles (1,000 per coin) and books the new day in the paper account.
  - A missed day is caught up, and a day is never booked twice.
  - Any other hour it does nothing.
- **Paper account arithmetic:** the same as the backtest. The weights held over the day earn the coins' returns,
  every change costs 0.10%, and funding is charged on what is held.
- **The live watcher** downloads `reports/trend_portfolio.json` with its hourly update and sends the message once per
  new day. It sends it even during `/pause`, because it is a daily plan, not a trade alert.
- **Settings:** `config.yaml` → `trend_portfolio` (enabled, telegram, lookbacks, paper_capital).

## Limits (honest)
- **Long only:** in a bear market it mostly holds cash. It protects you but does not profit.
- **A 26% drop can happen:** $1,000 → $740 at the worst point of the test.
- **Some years are flat:** it depends on big trends.
- **Small daily changes:** positions are $0–143 per coin on $1,000, and changing them by hand takes about 15 minutes a
  day.
- **Backtest only so far:** the paper account is the real test. Give it 1–2 months before deciding anything.
- **Strategy 13 and the alerts are separate:** this does not change them. The portfolio is the slow "core", and the
  alerts are extra trades.
