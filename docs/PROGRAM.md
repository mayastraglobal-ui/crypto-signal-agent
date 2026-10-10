# The Forward Test Program

Agreed with the operator on 2026-10-09. Goal: find out which strategies really work, **per coin**, first in a
5-year backtest and then on the live market, without forcing signals. Only the proven ones move towards real money,
and real money always needs the operator's "yes".

## The plan in three pull requests

| PR | What | Status |
|---|---|---|
| **1. Strategy lab** | 10 strategies × 4 versions, the 4H + 1H gate, 5 years of 30m / 15m history, nightly batches, results per coin after and before fees | **built 2026-10-09** |
| 2. Signal Center | silent live tracking of every positive strategy / version / coin, 🔵 TEST alerts for the best (new layout, ✅ Took it / ❌ Skip / ℹ️ Details), `/tests on|off`, demo book, a 2-week replay check | **built 2026-10-09** |
| 3. Weekly review | weekly report per strategy / version / coin / market type before and after fees, honest confidence, new version ideas, promote to 🟡 PAPER with one tap (max 5, one per strategy per coin), demote weak ones, system check | **built 2026-10-09** |

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
| V5 | V2 with the **fast 4H trend** (added 2026-10-09) | the trend strategies 1, 2, 3, 4, 7, 8, 9 only - the 4H direction from the 4H close and EMA20 vs EMA50 instead of the slower 4H regime label |

## The market gates (why a falling market can now be traded)

- **4H + 1H** (`gate: intraday`): a long needs the 4H AND the 1H regime bullish, a short both bearish. 1W and 1D are
  shown as context only - they never block. (The library's `trend` gate needs 2 of 1D / 4H / 1H and has a weekly veto:
  that is why the BTC drop from 87,000 to 81,900 in early October gave no short - the daily was still bullish.)
- **range** (`gate: intraday_reversal`): the strategy trades only in its range regimes and never against a STRONG 4H
  trend; 1W / 1D never block.
- Version V3 adds the daily back as one rule (`dir_1d`), so the program measures whether the daily filter helps.
- **fast 4H + 1H** (`gate: intraday_fast`, version V5): like the 4H + 1H gate, but the 4H direction is the 4H
  close and EMA20 vs EMA50 (UP / DOWN / FLAT, building block `dir_4h_fast`). Why: in the 6-9 Oct BTC fall the 4H
  regime label stayed UNCLEAR / TRANSITION while the 1H was STRONG_BEAR, so no short passed; the fast 4H trend turned
  DOWN on 8 Oct 08:00 UTC (about 83,000) and caught the leg to 81,000 (not the 86,000 -> 83,000 part - any moving
  average is a little late).

## How it is tested

- **Same tests as every strategy**: fees and funding of OKX futures, walk-forward, costs +50%, every number ±20%, at
  least 3 positive coins, the trials counter (luck bar), the bias check. Nothing is lowered.
- **History**: 4H / 1H since 2017 (Binance spot), 30m / 15m **5 years** (OKX perpetuals, Binance spot before a
  coin's OKX listing and inside an OKX hole - ZEC's perpetual was delisted 2023-12-19 to 2025-11-06; a younger coin
  has less - SUI since May 2023), 5m 2 years (only for entry confirmation).
- **Coins**: the hourly scan's coins plus the operator's pinned coins (`config.yaml` → `universe.research_pinned`:
  BTC, ETH, SOL, BNB, XRP, ZEC, SUI), so a quiet weekend that pushes a coin under the volume rules never removes it
  from the program's results (research only - alerts still need the volume rules).
- **5m entry confirmation** (operator decision 2026-10-09, option A): not part of the backtest cards; PR 2 adds it to
  the live TEST alerts (an alert waits for a confirming 5m candle).
- **Nightly batches** (`config.yaml` → `program`): 2 strategies (all 4 versions, all timeframes) per night, the ones
  tested longest ago first, so the first full pass takes **5 nights** and then it keeps rotating. A strategy with a
  version in VALIDATION / PAPER_TRADING is tested every night. A strategy not tested tonight keeps its status and
  its last results. Safety: if a night is already past 95 minutes when a coin starts (`skip_after_min`), that night's
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

## The Signal Center (PR 2)

- **Which pairs send 🔵 TEST alerts** (`config.yaml` → `signal_center`, `engine/signal_center.py`): a program cell on a
  coin with at least 20 backtest trades, an average above 0R after fees and an unseen last part that is not negative
  (`reports/program.json`). A cell already in 🟡 PAPER / 🟢 LIVE alerts with that label instead; a cell whose live
  record failed it (20 signals averaging below -0.10R) stops.
- **Live watcher**: on the real chart, long and short; 1W / 1D never block (⚠️ when against the daily); a 5m candle
  must confirm (operator choice A); one alert per coin + direction + strategy (versions / timeframes merged, ⭐ when
  another timeframe or strategy agrees within 4 hours); at most 10 a Beijing day; `/tests on|off`; ✅ Took it = demo
  book (never in the loss limits); ℹ️ Details = the strategy, its rules, why / when it fails, its backtest.
- **GitHub (silent tracking)**: the hourly scan records every TEST setup in `reports/signals_log.csv` as stage TEST
  with the market type (`market_type`: the coin's verdict and its 1D / 4H / 1H labels) - without the 5m check, so the
  weekly review can compare both. Never emailed, never in the position book or the risk limits. Bad live results
  (20 signals below -0.10R) fail the cell, as for every strategy.
- **Safety replay**: `windows\7_replay_test_alerts.bat` (`python live_watcher.py --replay 14`).
- **First replay (2026-10-09, BTC, the BTC-only backtest of the PR 1 measurement)**: 12 BTC cells qualified; in 14
  days 15 setups, 3 confirmed by the 5m candle (+0.17R together), the 12 the 5m check removed would have made +3.91R -
  far too few trades to judge either way. No short setup passed the gate during the 6-9 Oct fall: the 1H regime was
  STRONG_BEAR but the 4H regime only UNCLEAR / TRANSITION (the regime classifier is slow to call a 4H bear).
- **V5 replay (2026-10-09, BTC, last 14 days; V5 had no backtest yet, so it used V2's BTC numbers to be listed)**:
  V5 gave 15 short setups on 8-9 Oct where the old gate gave none. With the 5m check 4 went out and all 4 were
  stopped (-5.0R, BTC bounced 81,000 -> 83,000 on 9 Oct); without it the 16 V5 setups were about flat (-0.66R).
  One coin, two weeks: no conclusion - the 5-year backtest of V5 (tested with its strategy each rotation) decides.

## The weekly review (PR 3)

- **The report** (`engine/weekly_review.py`, `config.yaml` → `weekly_review`): `reports/weekly_review.md|json`,
  rewritten by every hourly scan, final on Sunday from 04:00 UTC (12:00 Beijing). It shows, for every program
  strategy / version / timeframe / coin with live results: TEST and PAPER trades, win %, average R **after fees** and
  **before fees**, this week, by market type (the coin's verdict at each setup), the 5-year backtest on that coin, and
  an **honest confidence** line ("+0.30R over 12 trades: still uncertain - could be luck"). Also: with vs without
  the 5m check, ideas for new versions, and a **system check** (research every night, the hourly scan, the program
  rotation, the watcher's journal).
- **Promote to 🟡 PAPER** - candidates: 10+ closed live TEST setups, positive after fees, positive backtest on that
  coin; the best evidence first; at most 5 pairs in PAPER, one per strategy per coin. **Your tap**: on Sunday the
  live watcher sends the review to Telegram with a "🟡 Promote" button per candidate. With journal sync on, the tap
  reaches GitHub (`journal/decisions.csv` on the branch `journal`) and the next nightly research makes that cell PAPER
  **on that coin only** (its other positive coins stay TEST). Without journal sync the bot sends you the line to add
  under `promotions:` in `config.yaml`.
- **Demote** (automatic, the safe direction): a promoted pair whose last 10 paper signals average below 0R goes back
  to 🔵 TEST by itself.
- **LIVE is not easier**: a cell that is PAPER only because of a promotion is never eligible for approval from that -
  LIVE still needs the full backtest pass bar, 20 good paper signals and your approvals line.
- **Telegram**: `/review` shows the newest review any time. The Sunday weekly email has a "Forward Test Program"
  part. Claude's weekly research (`tasks/weekly_research.md`, step 7b) explains it in plain words and may turn ONE of
  the review's ideas into a new lab version (one change, tested like every card).
