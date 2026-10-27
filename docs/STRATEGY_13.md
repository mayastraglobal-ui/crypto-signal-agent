# Strategy 13: the daily Turtle (2026-10-27)

**The request (operator, 27 Oct):** a strategy most trend traders in the world use, made more advanced and more
profitable, long only.

**What it is:** the classic Turtle trend follower.
- Buy when price breaks its **55-day high**.
- Hold while the trend runs.
- Exit when price closes below its **20-day low**.
- **No fixed target.** Most trades lose a little; a few big trends pay for all of them.

## The rules

| Step | |
|---|---|
| Entry | a 4H close above the highest high of the last 55 days (330 candles): buy at the next open (market) |
| Stop | 5 ATR(14) of 4H below the entry, about 2 daily ATR (median ratio 2.65 on the 7 coins). This is your 1R |
| Exit | a 4H close below the lowest low of the last 20 days (120 candles). In an uptrend this line keeps rising |
| Target | none. A far 40R safety target only, so the trade rides the trend |
| Max hold | 1200 candles (200 days) |
| One trade at a time | per coin (see below) |
| Direction | **long only** (the short rule `close < 0` never fires: shorts lost in the study, −0.14R) |
| Gate | `intraday_reversal` with every regime: never while the 4H is in a STRONG bear |

The agent trades 4H / 1H (the daily is context only), so the windows are day-sized on 4H candles:
- 55 days = 330 candles;
- 20 days = 120 candles;
- 200 days = 1200 candles.

## The versions

| Version | What changes |
|---|---|
| **V1** | the rules above |
| **V2** | V1 only while **BTC closes above its 200-day average** (`btc_close > sma(btc_close,1200)`): the bull-market filter |
| **V3** | V1 after a **strong breakout day**, with the coin above its **own 200-day average**. "Strong" means the last 24 hours closed in the top 25% of their range, and that range is bigger than its 20-day average |
| **C** | **control**: the same breakout with quick fixed targets (2R / 3R, 5-day hold), no 20-day exit. It shows whether riding the trend is what makes the money. **Never alerts.** |

## The tests

**1. The study** (daily candles since 2017, 7 coins, long only, 0.1% a side plus funding). 24 versions were compared,
so expect less than these numbers:

| Version | Avg / trade | Trades | Win rate | 2018 | 2022 |
|---|---|---|---|---|---|
| Plain | +2.28R | 223 | 33% | −11R | −13R |
| BTC above its 200-day average | **+2.92R** | 166 | 38% | **0R** | **0R** |
| Strong day + own 200-day average | +2.67R | 123 | — | — | — |

- The strong-day version had the smallest drawdown, 14R.
- A chandelier exit was worse (+1.08R), so it is not built.

**2. These cards through the agent's own engine** (4H since 2017, 7 coins, the nightly costs):

| Version | Trades | Won | Avg after fees | Unseen last 30% | Worst drawdown | 2018 / 2022 | Coins positive |
|---|---|---|---|---|---|---|---|
| V1 | 156 | 40% | **+1.83R** | +1.27R | 20.5R | −7R / −9R | 7 of 7 |
| V2 | 123 | 46% | **+2.01R** | **+1.89R** | **14.9R** | **0R / 0R** | 7 of 7 |
| V3 | 127 | 40% | +1.93R | +1.56R | 16.0R | −2R / −2R | 7 of 7 |
| C | 467 | 51% | +0.21R | +0.21R | 8.1R | −1R / +2R | 7 of 7 |

Riding the trend made about 9 times more per trade than taking quick profits on the same entries.

**Not built: a retest limit** at the broken level.
- It made +1.91R a trade, but only +0.99R on the unseen part.
- Its backtest moves the limit higher at every new high, which a live order cannot do. Its live record would not
  match the test.

## One trade at a time (`one_trade: true`)

- The breakout rule is true on **every new 4H high** of a rally, but the backtest holds one trade per coin.
- With `one_trade: true`, the live watcher and the hourly GitHub record count a signal only when the card's own
  backtest on the same candles takes it (`scanner.backtest_takes`).
- So a rally is **one** alert, not one every 4 hours.
- Checked on BTC, SOL and ETH since mid-2022, rebuilt from only the candles the watcher has: 224 signal candles,
  1 difference.
- A rule-only alternative ("new trend only": a close below the 20-day low since the last break) blocked the
  re-entries after a stop. It lost a lot: +1.51R a trade instead of +1.83R.

## What changed in the engine

- **`btc_close`**: BTC's close on the same candle (a new building block).
- **`entry: {type: market}`**: a card that says this keeps the market entry. The 🎯 pullback wait of TEST alerts is
  not used, because the big trends rarely come back.
- **4H history:** the hourly scan (`config.yaml` → `timeframes`) and the live watcher (`bars_tf`) keep **2700** 4H
  candles instead of 1500 / 500. That is the 200-day average (1200 candles) plus room to see the open trade. The
  other timeframes are unchanged.
- **A limit level may use `{params}`** (the entry block is filled in like the rules).

## The alert and the follow-up

The alert shows:
- the stop (your 1R);
- **"Target: none - ride the trend"**;
- the exit line now ("a 4H close below the lowest low of the last 20 days (now X)").

After **✅ Took it**, the watcher follows the trade on 5m candles, as for every strategy, and adds two messages:
- **📈 Exit line moved**: the 20-day low has risen by 0.25R or more, and it is above your stop (until then the stop
  protects). Can't watch the market? Move your OKX stop-loss up to it, only ever up.
- **🚪 Trend exit**: a 4H candle closed below the 20-day low. Close the trade at market. This is the backtest's exit:
  at that candle's close.

The silent plan record of every alert is kept until its max hold (200 days), not dropped after 14 days.

## When it is tested

The nightly research tests 2 program strategies a night, never-tested ones first. Strategy 13 should come in the next
night or two; results appear in `reports/program.md`.

The usual bar applies, nothing lowered:
- fees and funding, the unseen last 30%;
- costs +50%, ±20% parameters, the trials counter;
- the walk-forward check, and beating the control;
- the trend family's drawdown gates.

A version positive on a coin, with at least 20 backtest trades there, sends 🔵 TEST alerts on that coin. Expect few:
**about 2 to 3 a year per coin**. PAPER and LIVE come only with your tap. Strategies 1 to 12 are not changed.

## Limits (honest)

- **Most trades lose.** About 55 to 60% end with a small loss or the full stop. Long losing streaks happen in
  sideways years.
- **The exit gives back part of the profit** at the end of every trend. That is the price of never cutting a big
  winner early.
- **Long only:** nothing to do in a bear market, which is what V2 is built for.
- **Few trades per coin:** about 20 in 9 years. Some coins (SUI, listed 2023) will not have the 20 backtest trades a
  TEST alert needs.
- **The numbers are flattered:** the versions were chosen after looking at the data. The nightly research and the
  live record decide.
- **Pyramiding** (adding a second position at +2 ATR) made the most in the study, but it is not built. It needs engine
  work, and it makes sense only once strategy 13 works live.
