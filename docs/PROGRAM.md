# The Forward Test Program

Agreed with the operator on 2026-10-09. Goal: find out which strategies really work, **per coin**, first in a
5-year backtest and then on the live market, without forcing signals. Only the proven ones move towards real money,
and real money always needs the operator's "yes".

## The plan in three pull requests

| PR | What | Status |
|---|---|---|
| **1. Strategy lab** | 10 strategies × 4 versions, the 4H + 1H gate, 5 years of 30m / 15m history, nightly batches, results per coin after and before fees | **built 2026-10-09** |
| 2. Signal Center | silent live tracking of every positive strategy / version / coin, 🔵 TEST alerts for the best (new layout, ✅ Took it / ❌ Skip / ℹ️ Details), `/tests on|off`, demo book, a 2-week replay check before switching on | next |
| 3. Weekly review | weekly report per strategy / version / coin / market type before and after fees, honest confidence, new version ideas, promote to 🟡 PAPER with one tap (max 5, one per strategy per coin), demote weak ones, system check | after PR 2 |

## The 10 strategies

All rules are written with the engine's building blocks (`strategies.yaml` header lists them). Every card is in
`strategies_program.yaml`.

| # | Strategy | What it looks for | Indicators | Gate |
|---|---|---|---|---|
| 1 | Breakout | close beyond the 20-candle high / low with 1.5× volume | Donchian, volume, ADX | 4H + 1H |
| 2 | EMA trend pullback | dip to the 20 EMA in a trend, closes back above it | EMA 20 / 50, RSI, anchored VWAP | 4H + 1H |
| 3 | Fibonacci pullback | retrace into 50-61.8% of the last swing and hold it | Fibonacci, EMA 20 / 50 | 4H + 1H |
| 4 | Trend momentum | MACD crosses up while Supertrend is up | MACD, Supertrend | 4H + 1H |
| 5 | Range reversal | back inside the Bollinger band after an RSI extreme | Bollinger, RSI | range |
| 6 | VWAP reversion | stretched 2 ATR from the day's VWAP, turns back | VWAP, ATR, RSI | range |
| 7 | Squeeze breakout & retest | squeeze → breakout → retest that holds | Bollinger width, breakout / retest | 4H + 1H |
| 8 | Session open breakout | first break of the Asia range in London / New York | Asia high / low, sessions, volume | 4H + 1H |
| 9 | Liquidity sweep + structure shift | stops under a low taken, then a strong close above recent highs | sweep, displacement | 4H + 1H |
| 10 | Crowding fade | crowded side (funding, open interest) and price turns against it | funding, open interest | range |

## The 4 versions of each strategy

Each version differs from V1 in **one** way, so the results show what each change is worth.

| Version | What | Timeframes |
|---|---|---|
| V1 | base | 4H (strategy 8: 1H) |
| V2 | the same rules, faster | 1H / 30m / 15m (strategy 8: 30m / 15m) |
| V3 | V1 + the daily regime must agree | 4H (8: 1H) - shows whether the daily filter helps or only blocks moves |
| V4 | V1 with a trailing ATR exit | 4H (8: 1H) - targets 2R / 10R, after TP1 the stop trails 3 ATR(22) behind the high / low |

## The market gates (why a falling market can now be traded)

- **4H + 1H** (`gate: intraday`): a long needs the 4H AND the 1H regime bullish, a short both bearish. 1W and 1D are
  shown as context only - they never block. (The library's `trend` gate needs 2 of 1D / 4H / 1H and has a weekly veto:
  that is why the BTC drop from 87,000 to 81,900 in early October gave no short - the daily was still bullish.)
- **range** (`gate: intraday_reversal`): the strategy trades only in its range regimes and never against a STRONG 4H
  trend; 1W / 1D never block.
- Version V3 adds the daily back as one rule (`dir_1d`), so the program measures whether the daily filter helps.

## How it is tested

- **Same tests as every strategy**: fees and funding of OKX futures, walk-forward, costs +50%, every number ±20%, at
  least 3 positive coins, the trials counter (luck bar), the bias check. Nothing is lowered.
- **History**: 4H / 1H since 2017 (Binance spot), 30m / 15m **5 years** (OKX perpetuals, Binance spot before a
  coin's OKX listing), 5m 2 years (only for entry confirmation).
- **Nightly batches** (`config.yaml` → `program`): 2 strategies (all 4 versions, all timeframes) per night, the ones
  tested longest ago first, so the first full pass takes **5 nights** and then it keeps rotating. A strategy with a
  version in VALIDATION / PAPER_TRADING is tested every night. A strategy not tested tonight keeps its status and
  its last results. Safety: if a night is already past 65 minutes when a coin starts (`skip_after_min`), that night's
  batch is dropped whole - never half-tested - and goes first the next night, so the run always ends in time.
- **Results**: `reports/program.md` (one table per strategy: trades, win %, average R **after fees** and **before
  fees**, the unseen-test part, the coins where it was positive) and `reports/program.json` (the same for the next
  steps of the plan). Per coin, a coin counts as positive with enough trades and an average above 0R after fees.
- **Approval** never changes: a program card can reach PAPER_TRADING on its own, but to go live it must be copied into
  `strategies.yaml` by pull request and the operator adds the approval line.
- **The agent may add versions**: the engine's variant search may write new one-change versions of a strong program
  cell into `strategies_lab.yaml`; a running card is never edited.

## Commands

```
python research.py                    # tonight's batch (the default, --program auto)
python research.py --program all      # every program strategy in one run (long - by hand only)
python research.py --program 1,4      # only strategies 1 and 4
python research.py --program none     # the library only
```

## Honest expectations

- Most of the 59 tests will fail - that is the point of testing. The earlier library: 69 of 105 FAILED.
- Testing 59 more ideas raises the luck bar (trials counter, `memory/trials.csv`) from t ≥ 3.49 to about 3.61 for
  every strategy once all 59 are tested (each new test counts twice while the family gates run in shadow: once per
  rule set). More ideas tested means a winner must be stronger, so luck does not make "winners".
- Strategy 10 (crowding fade) has only about 1 year of funding / open-interest history: few backtest trades, it
  mostly has to prove itself live.
- 15m results carry the most fees (about 0.18R a trade); 4H the least (about 0.04R).
