# The operator's scalping playbook in the agent

The operator's rule book, `docs/playbook/Crypto_Scalping_Playbook.txt` (uploaded 2026-10-06, "follow all rules
strictly"), is the source. This page maps every rule to the agent: **exact** (coded as written), **approximated**
(coded as close as the data allows; the difference is stated), or **not possible** (no data; what happens instead).

The operator's decisions (2026-10-06):
- The playbook's risk rules apply to the **playbook strategies only**; the agent's other strategies keep their rules.
- **CVD** comes from real aggressive buy / sell volume: Binance USDT-M futures (taker buy volume per 5m candle) for
  the backtests, OKX's taker volume for live alerts. Each strategy also has a twin without CVD; CVD is kept only if
  it helps.
- The playbook strategies must pass the playbook's **stricter bar** as well as the agent's own tests.

Status: **3a** (engine features), **3b** (building blocks and strategies A / B / C), **3c** (risk rules and the
pass bar) and **step 3d** (flexible versions: graded setups, the operator's three rule changes, the fee fix) are built. The strategies start at BACKTESTING like every new card; they alert in Telegram only once the
research promotes them to PAPER_TRADING (and LIVE only after the operator's approval).

## The chain (playbook section 1)

Every link is a filter; a failed link = no trade.

| Link | In the agent |
|---|---|
| Context (news, session, funding, OI, BTC) | 3c risk rules + 3b session / funding / OI / BTC building blocks |
| Regime (1H trend / range / transition) | 3b building block; the card uses `gate: playbook`, so the agent's own regime gate is NOT added on top (3a) |
| Bias (1H) | 3b building block |
| Location (marked level zone) | 3b building blocks |
| Setup (A / B / C) | 3b strategy cards |
| Trigger (5m candle closed) | the cards run on closed 5m candles (backtest, hourly scan, live watcher) |
| Risk (>= 1.5R after fees) | `targets.min_rr_after_fees: 1.5` (3a) |
| Management (1R partial, breakeven, trail, time stop) | the card's `manage` block (3a) |
| Review (journal, expectancy) | the research run + `journal/my_trades.csv` (Telegram buttons) |

## Engine features (3a, done)

| Playbook rule | Card setting | Status |
|---|---|---|
| Regime / bias are the playbook's own (1D / 1W only a map) | `gate: playbook` | exact |
| A: "limit order at the 50% level of the trigger candle, or market on close if the candle is small" | `entry: {type: limit, long_level, short_level, valid_bars}`; the level column is empty for a small candle → market at the next open | exact (the market order fills at the next candle's open, the closest a backtest gets to "on close") |
| TP1 = 1R, close 50% | `targets: {long: ["1R", ...], split: [0.5, 0.5]}` | exact |
| B: TP1 = 1R or VWAP, whichever first | target `min(1R, vwap)` | exact |
| TP2 = a level / measured move, at least 2R (A) | target `max(2R, <level column>)` | exact |
| Trade must give >= 1.5R to TP2 after fees and slippage | `targets.min_rr_after_fees: 1.5` (taker fee + slippage both ways, the cautious case) | exact |
| Stop below 0.5 x ATR(5m) or above 3 x ATR(5m) = no trade | `stop: {min_width_atr: 0.5, max_width_atr: 3}` | exact |
| At TP1: stop to breakeven **plus fees** | `manage.be_plus_fees: true` | exact |
| Trail the rest behind the last confirmed 5m swing low or EMA9, whichever is further | `manage.trail: {swing_n: 3, ema: 9}` (engine/manage.py; a swing is confirmed 3 candles later) | exact; "in strong trend days trail on 15m swings" is a judgement call and is not coded |
| Time stop: +0.5R not reached within 6 (A) / 4 (B) 5m candles → exit at market | `manage.progress: {r: 0.5, bars: 6}` | exact |
| Invalidation exits (A: 15m close below the pullback low; B: 5m close below the swept level; C: 5m close back inside by > 0.3 ATR) | `manage.invalidate: {long, short, every}` (the level is fixed at the signal; `every: 15m` checks only 15m closes) | exact |
| A: or 1H bias flips to neutral | the card's `exit_long` / `exit_short` rule (3b) | exact |
| The same management in paper trades and in the Telegram follow-up | `scanner.update_forward`, `engine/follow.py` | exact (the follow-up messages "move the stop to X" when the trail moves 0.25R or more) |
| Pine export | REPLAY mode (TradingView cannot recompute the playbook management) | approximated |

## Data the playbook asks for (section 8.1)

| Feed | Status |
|---|---|
| OHLCV 5m / 15m / 1H / 4H / 1D | exact: OKX USDT perpetuals, 2 years on 5m / 15m / 30m (step 2), Binance spot since 2017 above |
| 1m (precision entries) | not used: the playbook says it never generates signals; entries use the 5m candle |
| CVD (aggressive buy - sell) | 3b: Binance USDT-M futures taker buy volume (backtest), OKX taker volume (live) |
| Open interest | approximated: hourly OI (derivs.py); "OI drops >= 1% during the sweep" uses the hourly change known at the sweep candle |
| Funding | exact: the recorded funding history |
| Order book / spread | live only (3c: the live watcher checks the OKX spread before an alert); backtests assume a normal spread |
| Liquidation heatmap | not possible (no history): liquidation clusters are not used as targets or stop zones |
| Economic calendar | exact: events.yaml (3c: the playbook's ±15 minutes for playbook strategies) |

## Human rules (sections 10-12)

Screenshots, emotional state and "no trading when tired" are the operator's part. The agent supports them with the
Telegram buttons (✅ took it / ❌ skipped, saved in `journal/my_trades.csv`) and, in 3c, the size rules it can check
(half size after a large win, in late US hours and at weekends).

## Strategies (3b)

`engine/scalp_playbook.py` computes the playbook on closed 5m candles (`pb_*`, `pbA_*`, `pbB_*`, `pbC_*` columns;
higher timeframes = their last closed candle, swings only after their confirmation candles - a test cuts the future
off and checks nothing changes). The cards are in `strategies.yaml` (`PB-*`, `gate: playbook`, timeframe 5m):

| Card | Playbook | CVD |
|---|---|---|
| `PB-A-PULLBACK` | 5.1 Strategy A, as written | without (the playbook calls CVD optional for A) |
| `PB-A-PULLBACK-CVD` | 5.1 + the optional CVD confirmation (trigger candle's delta in the trade direction) | with; must beat PB-A-PULLBACK |
| `PB-B-SWEEP` | 5.2 Strategy B, confirmation = any of CVD divergence, absorption, OI drop >= 1% | with |
| `PB-B-SWEEP-noCVD` | the same, OI drop only | control twin |
| `PB-C-BREAKOUT` | 5.3 Strategy C, with "CVD not making a new low" on the retest | with |
| `PB-C-BREAKOUT-noCVD` | the same without the CVD check | control twin |

Every card also has the section 5.4 filters: funding above +0.05% / below -0.05% per 8h blocks that side; an
altcoin long is blocked while BTC's 15m structure is breaking down (and vice versa).

### Where the playbook is silent (assumptions, each written in the card's changelog)

| Point | Assumption |
|---|---|
| Regime when the trend conditions hold but price crossed VWAP 4+ times | range (the crossings say price is chopping, not trending) |
| Which session for which strategy | the "Use" column of section 2.3 read literally: A only in NY (13:00-16:00 UTC), B in Asia, London and NY, C in London and NY; 10:00-13:00 and 16:00-24:00 UTC are not listed, so no entries there |
| A: how long the 50% limit waits | 3 x 5m candles |
| A: the pullback | the candles after the highest high since the last confirmed 15m swing low (long) |
| B: range low / high | the 24 x 15m candles' range; equal lows = two confirmed 15m swing lows within 0.1 x ATR(15m) |
| B: major levels | PDH / PDL, Asia high / low, previous week high / low, weekly open |
| B: absorption | a delta >= 1.5 x the average absolute delta against the move, closing in the candle's favourable half |
| B: "OI drops 1% during the sweep" | the hourly OI change known at the sweep candle (OI is recorded hourly; its history starts 2025-09-29) |
| C: "directly under a level" / "near a session open" | the level within 0.5 x ATR(15m) of the 8-candle box; the first hour of London (07:00) or NY (13:30) |
| C: time stop | 6 candles (section 7 gives 4-6) |
| Unbroken 1H / 4H swings | the last 480 candles of each (what the live watcher holds) |
| "Large win" (11) | +2R or more |
| Ranges (daily loss -2R to -3R, 6-8 trades a day) | the stricter end: -2R, 6 trades |
| The engine's outer time limit | 48 x 5m candles (4 hours); the playbook's own time stop is the +0.5R rule |

### What the first measurement shows (BTC, 2024-10 to 2026-10)

The rules as written are selective. On BTC, before costs and the other filters:
- **A:** about 2 signals a year. The 1H trend, bias, NY session, pullback quality and trigger must all agree.
- **B:** about 1,100 sweeps back inside a marked level before the confirmation. It is the busiest of the three.
- **C:** close to none. The playbook's compression ("the last 8 x 15m candles inside 1.2 x ATR") happened on about
  0.2% of 15m candles.

The playbook asks for 100 trades before judging (9.2), so A and C may stay in BACKTESTING for lack of trades. That is
the honest result of the rules as written. Changing a number (for example the compression box) is the operator's
decision: a new card version, one change at a time (9.1 and 10.2).

## Step 3d: flexible versions (operator, 2026-10-06)

The operator: "the market never follows a rule book perfectly - rules this strict may never give a trade". The first
measurement agreed (A ~2 trades a year, C none), and showed a second problem: on 5m the stop is so close that fees
and slippage cost B a median 0.84R a trade. The originals stay exactly as written (the benchmark); next to them:

| Card | What changes | Why |
|---|---|---|
| `PB-A-PULLBACK-LDN` | A, London (07:00-10:00 UTC) as well as NY | operator's change 1 (one change only) |
| `PB-B-SWEEP-15M` | B on 15m trigger candles (outer limit 16 x 15m = 4 hours, as on 5m) | operator's change 2: a wider stop makes the fees smaller in R |
| `PB-C-BREAKOUT-W20` | C with the compression box 2.0 x ATR (was 1.2) | operator's change 3 |
| `PB-B-SWEEP-LIMIT` | B + the fee fix: limit entry at the signal close (maker fee, waits 2 candles) and `stop.max_cost_r: 0.25` | fees |
| `PB-A-GRADED`, `PB-B-GRADED` (5m and 15m), `PB-C-GRADED` | graded setups (below), London / NY for A, the 2.0 box for C, the fee fix | rules that bend without dropping the safety rules |
| `PB-A-APLUS`, `PB-B-APLUS` (5m and 15m), `PB-C-APLUS` | only the graded setups with 3+ points | measures the grades separately: if GRADED does no better than APLUS, the grade B trades add nothing |

**Graded setups.** Every must-have stays a must-have; the other conditions become bonus points. 2 points = a trade at
**half size** (grade B, shown in the alert), 3 or more = full size (A+), fewer = no trade.

| | Must-haves (all) | Bonus points (1 each) |
|---|---|---|
| A | 1H trend + bias, London / NY, the 15m higher low intact, the pullback in the EMA21 / VWAP zone near a level, a 5m rejection / engulfing candle beyond EMA9 | pullback >= 0.8 ATR deep, pullback on lower volume, trigger volume >= 1.2 x average, CVD on the trigger candle, NY session |
| B | the sweep (>= 0.1 ATR beyond a marked level), the first close back inside within 3 candles, the playbook's regime rule | OI drop >= 1%, CVD divergence, absorption, Asia / London / NY session, a major level |
| C | a box within 2.0 x ATR(15m) under a level, a breakout close >= 0.2 ATR beyond with a 60% body, not against a 1H trend, the retest rejection candle before a close back inside | the playbook's tight compression, the breakout's volume spike, CVD holding, London / NY, the playbook's regime rule |

Every playbook A signal is a graded A+ setup (the test checks it). The thresholds 2 and 3 are a choice, not
measured; they are not tuned to the data (tuning to the data the strategy is judged on is how backtests lie).

**Fee fix.** `stop.max_cost_r: 0.25` = no trade when the round trip (the entry fee - maker for a limit, taker +
slippage at market - plus a market exit with slippage) costs more than 0.25R. With OKX's fees that means a stop at
least ~0.5% away for a limit entry, ~0.8% at market: on 5m BTC most stops are closer, so few 5m trades pass; on 15m
more do. The research counts these as `skipped_fee_cost`.

**First measurement** (2 years, 2024-10 to 2026-10, all costs; a pre-check, the research run decides):

| Card | BTC trades | BTC avg | ETH trades | ETH avg |
|---|---|---|---|---|
| PB-B-SWEEP (as written) | 130 | -0.93R | 81 | -0.68R |
| PB-B-SWEEP-15M | 25 | -0.96R | 16 | -0.53R |
| PB-B-SWEEP-LIMIT (fee fix) | 11 | -0.25R | 15 | +0.04R |
| PB-B-GRADED 5m / 15m | 37 / 16 | -0.21R / -0.43R | 76 / 26 | -0.06R / -0.40R |
| PB-B-APLUS 5m / 15m | 8 / 2 | -0.24R / -0.61R | 13 / 6 | +0.10R / -0.80R |
| PB-A-PULLBACK / -LDN / -GRADED | 1 / 1 / 3 | all losses | 1 / 2 / 8 | -1.22R / -0.38R / -0.36R |
| PB-C-* (all versions) | 0 | - | 0-1 | - |

What it says: the fee fix is the biggest single improvement (B from -0.93R / -0.68R to about -0.2R / 0R: the median
cost falls from 0.84R to 0.20R) - but it removes most trades, and nothing is clearly profitable yet; every sample is far
below the 100 trades the playbook asks for. 15m triggers did not help B (most 15m sweeps fail the 1.5R-after-fees
rule to TP2). C stays near zero: strong breakouts straight out of a quiet box with a clean retest are rare whatever
the box width. The daily research run tests every coin and decides.

Every new card starts at BACKTESTING and needs the same tests and pass bar as the originals; nothing was loosened
in the gates, the trials bar or the costs. 10 more cards also make the trials bar a little stricter for everyone.

## Risk rules (3c, for the PB-* strategies only)

`config.yaml` -> `playbook` (the other strategies keep the agent's rules):

| Playbook | In the agent |
|---|---|
| 2.1 no entries +-15 min around high-impact news | `risk.blackout_minutes: 15` (the agent's other strategies: 60) |
| 2.5 coins: BTC, ETH + SOL / BNB / XRP meeting $500M 24h volume and < 0.02% spread, 2-4 pairs | `coins_core`, `coins_extra`, `max_coins: 4`, checked on OKX perpetuals (hourly scan and live watcher) |
| 5.4 spread above 2x normal → skip the pair | live watcher: no alert when the OKX spread is above 2 x 0.02% |
| 6.1 max 2 positions, max 1.5% open risk | `max_positions: 2`, `max_open_risk_pct: 1.5` |
| 6.1 daily loss -2R / weekly -6R | `day_limit_r: -2`, `week_limit_r: -6` (then half size the next week) |
| 6.1 3 losses in a row = 30-minute break, 4 = stop for the day | `pause_after_losses`, `pause_minutes`, `stop_after_losses` |
| 6.1 6-8 trades a day | `max_trades_day: 6` |
| 6.1 isolated margin, liquidation >= 2x the stop distance beyond the stop | the alert gives the highest isolated leverage that keeps it (`liq_x: 2`) |
| 2.3 / 5.2 / 11 half size: late US and weekends, counter-trend sweeps, after a large win | the size in the alert and the paper record is halved, with the reason |
| 9.2 / 9.1 pass bar: +0.15R, PF 1.3, 100 trades, 50 paper signals | `playbook.validation` - the stricter of these and the agent's own numbers |

In the Telegram alerts the day limits come from the operator's own trades (the ✅ Took it buttons and their results).
In the hourly scan and the paper record they come from the APPROVED (live) record, like the agent's other rules.
