# Strategy 12: follow the leader (2026-10-14)

**The question (operator, 14 Oct):** "When BTC falls, do the weaker coins fall harder? Can I make money from it?"

**The 5-year answer (Binance 4H, BTC ETH SOL BNB XRP ZEC SUI, Oct 2021 - Oct 2026):**
- Yes, the coins move harder than BTC. When BTC falls 5% in a day, SOL falls about 7%, SUI 6.6%, ZEC and ETH 6%,
  XRP 5.4%, BNB 4.6%.
- **Shorting the weakest coin after a BTC fall does not pay:** about 0R, and the unseen last 30% was negative.
- **Buying the strongest coin after a BTC jump is slightly positive:**

| After BTC rises 3%+ in 24 hours | Trades | Average after costs | Unseen 30% |
|---|---|---|---|
| Buy the **leader** (the coin rising most vs BTC) | 271 | **+0.10R** | +0.10R |
| Buy the **laggard** (the coin rising least) | 271 | −0.18R | −0.37R |
| Buy BTC | 271 | −0.08R | −0.17R |
| Buy every coin | 271 | −0.05R | −0.14R |

The leader beat the laggard by +0.27R a trade (t = 3.7): picking the right coin matters.

**The honest catch:** most of the profit came from ZEC's big 2025 rally. Without ZEC the leader averaged about 0R, and
2 of the 6 years were negative. So strategy 12 is a test, not a promise.

## The rules

| Step | |
|---|---|
| 1. Trigger | BTC's close is up **at least 3%** over the last 24 hours (the first candle that crosses it) |
| 2. Choose | the coin with the **highest gain minus BTC's gain** over those 24 hours among your coins (`lead_rank(n) == 1`) |
| 3. Entry | buy (LONG) at the candle close |
| 4. Exit | stop 1.5 ATR below, target +2R, time stop 48 hours |
| Direction | **long only** (the short rule `close < 0` never fires) |
| Gate | `intraday_reversal`: never while the 4H is in a STRONG bear trend |

## The versions

| Version | TF | What changes |
|---|---|---|
| **V1** | 4H | the rules above (24 hours = 6 candles) |
| **V2** | 4H | over 12 hours (3 candles): a sharper jump. The study's best version (+0.30R), found by trying ~25 versions - expect less |
| **V3** | 1H | V1 on 1H closes (24 candles): up to 3 hours earlier. The 1H study result was −0.03R: expect it to fail |
| **C** | 4H | **control**: V1 without the leader pick - buy every coin after a BTC jump. V1 must beat it. **Never alerts.** |

Through the agent's own engine on the same 5 years (simple scoring, before funding):
- V1: 337 trades, +0.10R (unseen +0.12R);
- V2: 246 trades, +0.28R (unseen +0.54R);
- V3: 625 trades, −0.03R;
- C: 2,206 trades, −0.03R.

V1 finds more trades than the study (337 vs 271) because "the first candle that crosses +3%" can fire again after BTC
dips back under 3%. Those extra trades averaged +0.08R.

## The new building block: `lead_rank(n)`

- This coin's rank among `universe.own_coins` other than BTC, by its gain minus BTC's gain over the last n closed
  candles. 1 = the strongest; ties share a rank.
- Made for n = 3, 6, 12 and 24 on 4H and 1H (`scanner.LEAD_NS`, `scanner.LEAD_TFS`). Any other n, BTC itself, a coin
  outside your list, or fewer than 3 coins with data reads "unknown", so the rule is false.
- Built by `scanner.leader_frames`, joined with strategy 11's counts in `scanner.market_frames`, carried with BTC's
  candles (`btc_frames`) and handed to each coin by `attach_market(..., base)`. The same path runs in the nightly
  research, the hourly scan and the live watcher.

The live watcher now also downloads **every coin of your list** (BNB too, which is below the $50M volume rule) only
for these counts and ranks, so live uses the same coins as the backtest. It never sends a signal for them.

## When it is tested

The nightly research tests 2 program strategies a night, never-tested ones first:
- 15 Oct (08:40 Beijing): strategies 1 + 11;
- **16 Oct (08:40 Beijing): strategy 12**, results about 09:45 in `reports/program.md`.

The usual bar applies, nothing lowered:
- 5 years of data, fees and funding, the unseen last 30%;
- costs +50%, ±20% parameters, the trials counter;
- the walk-forward check, and beating the control.

A version that is positive on a coin sends 🔵 TEST alerts there (about 1 a week if V1 passes). PAPER and LIVE come only
with your tap. Strategies 1 to 11 are not changed.

## Limits (honest)

- Few trades: one coin per BTC jump, about 1 a week.
- Long only. In a falling market it is quiet.
- A leader pushed by its own news can reverse fast.
- The study's profit leaned on one coin (ZEC). Expect V1 to fail or pass only just.
