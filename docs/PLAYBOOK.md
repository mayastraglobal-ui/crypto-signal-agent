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

Status: **3a done** (engine features). 3b (building blocks and strategies A / B / C) and 3c (risk rules and the
pass bar) follow; this page is updated with each part.

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
