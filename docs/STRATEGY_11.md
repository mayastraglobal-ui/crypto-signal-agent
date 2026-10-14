# Strategy 11: early momentum (2026-10-13)

**The problem (operator, 12 Oct):** "1H and 30m candles fell strongly for hours on BTC, SOL, SUI, XRP, ZEC and I got no
alert." The 1H regime read TRANSITION and the 4H RANGE / TRANSITION. Strategies 1–10 need the 4H **and** the 1H trend
to agree, so they waited. Retail traders caught the first part of the move.

**The second problem:** a strategy that shorts every breakdown also shorts the **bottom**, when most of the fall is
done and a bounce comes.

Strategy 11 targets the **first steps** of a market-wide move and warns when a move is **late**.

## The phases of a move

```
  PHASE A        PHASE B             PHASE C           PHASE D
  Forming   →   Early move    →    Late / stretched  →  Bounce or continue?
  👀 note       🔵 trade (V1-V4)    ⚠️ note: no new     🔄 note when price is back
                (once tested)       trade that way      over the 30m average
```

On 12 Oct (Beijing time):

| Time | What happened | What strategy 11 does |
|---|---|---|
| 19:45 | SOL, SUI, XRP pressing on their 30m lows | 👀 forming notes |
| 21:00 | the 1st breakdown on most coins (`mkt_dn` = 6 of 7) | V1 SHORT SOL, SUI, XRP → all reached +2R |
| 23:00 | the 2nd step (ZEC's 1st) | V1 SHORT ZEC (+2R) and SUI (open); SOL / XRP blocked (RSI below 30); ⚠️ late notes for SOL and XRP |
| 01:00 | the 3rd step (RSI 21–24) | no trade; ⚠️ late notes for SUI and ZEC |

**The honest part of the same replay:** on the choppy 11–12 Oct the same V1 also lost on fake breaks:
- 5 shorts at 11:30–12:00 on 11 Oct;
- 3 longs at the 13:00 top on 12 Oct.

Over the three days V1 made about +3R before fees (a simple check: stop or +2R). Two days prove nothing: only the 5-year backtest decides.

## The gate: `intraday_momentum`

| | Strategies 1–10 (`intraday`) | Strategy 11 (`intraday_momentum`) |
|---|---|---|
| 1H | regime label bull / bear | **already moving**: 1H close beyond its EMA20 AND beyond the close 6 hours earlier (`dir_1h_mom`) |
| 4H | regime label must agree | must **not** be in a STRONG trend against it |
| 1W / 1D | context only | context only |

## New building blocks

- `mkt_up` / `mkt_dn`: how many of your 7 coins (`universe.own_coins`) closed above their 20-candle high / below their
  20-candle low on this candle or the one before. Fewer than 3 coins with data reads "unknown".
- `steps_up(n, gap, win)` / `steps_dn(n, gap, win)`: which breakout / breakdown step of the move this is. It counts
  new breaks (a break with no break in the `gap` candles before) in the last `win` candles.
  - 1 = the first step.
  - 3 = the third step, which is usually late.
- `dir_1h_mom`: the 1H momentum as +1 / −1 / 0.

All of them use closed candles only, identically in the backtest, the hourly scan and the live watcher.

## The versions (both directions, tested separately)

| Version | TF | Rules (SHORT; LONG mirrored) |
|---|---|---|
| **V1** | 30m | close below the 20-candle low, volume ≥ 1.5×, **≥ 3 coins breaking down** (`mkt_dn`), **BTC falling** and this coin **falling at least as hard as BTC** over 4 hours, **step 1–2 only**, **RSI > 30**, **not more than 2.5 ATR below the EMA20** |
| **V2** | 30m | V1 + the close is below the **24-hour low** (48 candles) + a **squeeze** (Bollinger width in its lowest 25%) within the last 12 candles |
| **V3** | 1H | V2 on 1H closes (steadier, later) |
| **V4** | 30m | **retest**: within 8 candles of a market-wide breakdown, price pulls back to the 30m EMA20 and closes red below it; step 1–2; stop 0.3 ATR above the candle's high |
| **C** | 30m | **control**: the plain breakout (close below the 20-candle low, 1.5× volume) under the same gate. V1 must beat it, or its extras add nothing. **Never sends an alert.** |

All versions use a 1.5 ATR stop (V4: the candle's high / low), targets 2R / 3R (50 / 50), and exit early on a close
beyond the 10-candle opposite extreme. The time stop is 24 candles, with a cooldown of 4 candles.

Every 🔵 TEST alert also waits for the **5m confirmation**, as all TEST alerts do.

## When it is tested

Research tests the program 2 strategies a night, the ones never tested first:
- 13 Oct night: 7 + 8;
- 14 Oct night: 9 + 10;
- **15 Oct (08:40 Beijing): 1 + 11**, results about 09:45 the same morning in `reports/program.md` (corrected 14 Oct).
- 16 Oct: strategy 12 ([`docs/STRATEGY_12.md`](STRATEGY_12.md)).

The usual bar applies, with nothing lowered:
- 5 years of data, fees and funding, the unseen last 30%;
- costs +50%, ±20% parameters, the trials counter;
- the walk-forward check, plus beating the control twin.

A version that is positive on a coin sends 🔵 TEST alerts there. PAPER and LIVE follow only with your tap.

## What 5 years say (checked 2026-10-13, after the first live morning)

The first live morning (13 Oct) went badly:
- 👀 forming at 05:45 was right;
- ⚠️ late at 06:00, at the start of a fall that continued to 08:30;
- a 🔵 SHORT from an old strategy at the bottom (08:05);
- about 20 messages in total.

So the idea itself was checked on 5 years of Binance 30m candles for the 7 coins. The sample: every 30m close
beyond the 20-candle low / high with 1.5× volume, at least 3 coins breaking together, and the 1H moving that way.
Each break was traded with a 1.5 ATR stop, a 2R target, a 12-hour limit and 0.12% costs.

| | Breaks | Average after costs | Win % | Price 4 hours later |
|---|---|---|---|---|
| SHORT after a market-wide breakdown | 11,321 | **−0.12R** | 35% | slightly **higher** (−0.13% for the short) |
| LONG after a market-wide breakout | 9,206 | **−0.12R** | 36% | slightly higher (+0.07%) |

What that means:
- On average a market-wide 30m break does **not** keep going far enough to pay the fees, early or late. This matches
  the program's own result: the same ideas lose on 1H / 30m / 15m and earn only on 4H.
- **"Late" does not mean "bounce" in a reliable way:**
  - shorts on step 2–3 did a little worse than on step 1 (−0.18R / −0.16R vs −0.09R);
  - very stretched breakdowns (3.5+ ATR from the EMA20) were the least bad (−0.03R);
  - on the long side, the most stretched breakouts (RSI above 80) kept rising the most.
- The only slightly positive groups were found by looking at the data:
  - shorts at step 1 with RSI 20–25 (+0.03R, 968 breaks);
  - longs at step 1 with RSI above 80 (+0.10R, 501 breaks).

  Finding them this way is how false strategies are made, so they are not used.

Changes on 13 Oct:
- The 🌊 notes are **off by default** (`/momentum on` switches them on). When on: one message per check for all
  coins, at least 3 coins, at most 6 a day.
- The step counter restarts after a close back over the 30m EMA20.
- Strategy 11 still gets its 5-year test (15 Oct morning). Expect it to fail; if a version passes the full bar, it will
  alert like any other.
- 🔵 TEST alerts on Telegram come only from strategies **not FAILED and positive overall**, on coins averaging at
  least +0.10R. That is 10 strategy timeframes, 9 of them 4H, instead of 30. GitHub still records every TEST setup.
- ✅ Took it pressed after the plan already hit its stop or TP1 is refused ("too late").

## 🌊 Momentum notes (information only, off by default since 13 Oct)

| Note | When | Text |
|---|---|---|
| 👀 forming | every 15m close | the 15m price within 0.3 × the 30m ATR of the 30m 20-candle low / high (not broken yet), 15m volume ≥ 1.2×, the 1H moving that way, the 4H not strongly against it, **and at least 2 coins doing the same** |
| ⚠️ late | 30m close | a break that is the 3rd step or later, RSI beyond 30 / 70, or more than 2.5 ATR from the 30m EMA20: "**No new short now**, already short: take profit or tighten your stop" |
| 🔄 bounce | 30m close, within 12 hours of a ⚠️ note | the 30m close is back over its EMA20: "the fall may be over; a bounce trade is NOT tested" |

Limits:
- at most 12 notes a day;
- 👀: one per coin and direction in 2 hours;
- ⚠️: one per coin and direction in 4 hours;
- 🔄: one per ⚠️ note.

`/momentum off` stops them and `/pause` holds them. Settings: `config.yaml` → `momentum_notes`.

These notes never make, block or size a trade.

## Limits (honest)

- Some step-1 breaks fail: the 11 Oct replay shows it. The market-wide count removes many of them, not all.
- A pure bounce trade (buying the bottom) is **not** a version. Bounce strategies were mostly negative in earlier tests.
  The 🔄 note only says "careful".
- Expect 1–3 versions to pass on some coins, not all.
