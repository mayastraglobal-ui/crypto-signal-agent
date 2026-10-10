# The Failure Lab

Built 2026-10-10 at the operator's request ("build the failure lab"). The research run turns **why trades lose**
into new strategy versions by itself, tests them like every other card, and **learns which repairs work**.

## Why

Every night the engine measures the loss causes (tags) of every strategy and timeframe (`engine/attribution.py`,
AGENT_PROMPT.md section 17). For example, the 4H Donchian breakout averages **-0.09R** a trade when the breakout fails
within 5 candles (`false_breakout`) and **+0.49R** without those trades. Until now, only Claude's daily review could
turn such a cause into a new card (factory `failure`), and in its first weeks it wrote none. The engine's variant search
only improved strategies that were still testing, never a failed one.

## How it works (every research run, `engine/failure_lab.py`)

1. **Candidates.** A strategy timeframe with 100+ backtest trades that is still testing (BACKTESTING), or FAILED but
   positive **before fees** (a near miss). It also needs a loss tag that:
   - hurts: the trades with it average less than the trades without it;
   - has 30+ losing trades;
   - is systematic (flagged) or appears in 25%+ of the losses.
2. **Repair.** One fixed repair per tag, each **one change** built only from existing building blocks:

   | Loss tag | Repairs, in the order tried at first |
   |---|---|
   | false_breakout | DISP (a strong candle within 3), RVOL (volume 1.5x), RETEST (limit order 0.5 ATR back) |
   | no_displacement | DISP |
   | low_relative_volume | RVOL |
   | range_market | ADX (> 20), REGIME (drop the regimes where it lost) |
   | htf_conflict | HTF (higher timeframe agrees), DAILY (never against the daily regime) |
   | trend_reversal, regime_mismatch | REGIME, HTF |
   | overextended_entry | NOTEXT (not more than 2 ATR from the EMA20), RETEST |
   | late_entry | NOTLATE (not after a 3 ATR move in 10 candles), RETEST |
   | stop_too_tight / stop_too_wide | WIDESTOP (x1.25) / TIGHTSTOP (x0.8) |
   | fees_slippage | LIMIT (limit entry), FEECAP (no trade above 0.25R of costs) |
   | wrong_session | SESSION (London and New York only) |
   | bad_target | NEARTP (targets 2R / 3R when the first target was farther) |

3. **Ranking.** expected gain × the repair's track record. The expected gain is the "without the tag" average minus
   today's average. A tag known only after the entry (a failed breakout, a regime change) counts half, because
   hindsight overstates what a filter can reach. The record is (times it helped + 1) / (times tried + 2).
4. **The card.** It gets the id `<parent>-F<KIND>`, e.g. `P02-EMA-PULLBACK-V4-FHTF`, and goes into
   `strategies_lab.yaml`:
   - factory `failure`, with the tag and its losing-trade count in `factory_evidence`;
   - a `repair:` block (tag, kind, timeframe, parent cell).
5. **Judging.** Once tested, each repair is compared with its parent on the same timeframe:
   - **helped** = better on the unseen part of the data AND overall;
   - **passed** = it reached VALIDATION or better.
6. **Learning.** The record per repair kind (tried / helped / passed) decides which repair of a tag is tried first. A
   kind tried 4 times without helping once is **stopped**. Results are kept in `reports/failure_lab.json`, even after
   a card is retired, so a lesson is never lost.

## Limits (it cannot fool itself)

- **At most 1 repair a night**, within the weekly `failure` quota (`config.yaml` → `lab.factory_quota.failure`: 3 per
  7 days, shared with Claude).
- One repair per parent per night. A repair is never repeated, and a chain stops at a repair of a repair.
- Every repair is a normal lab card:
  - the same checks (2R first target, the edge text, one change);
  - every test (fees, walk-forward, costs +50%, ±20%, coins, bias check);
  - **counted in the trials file**, so more tries raise the luck bar for everyone.
- A running card is never edited. Lab cards never become LIVE on their own: real money still needs the library, 20
  good paper signals and the operator's approval line.
- A library card without targets cannot be repaired. Its first target is below 2R, so a repair would need two changes;
  its lab versions with 2R / 3R targets can be repaired.

## Where you see it

- **Sunday weekly review** (Telegram): "🔧 Failure Lab: N repair(s) judged - X beat their parent, Y reached VALIDATION;
  Z waiting". `reports/weekly_review.md` has the details.
- **Weekly email:** "Failure Lab:" lines in the Forward Test Program part.
- **Claude:** the daily and weekly fact sheets. The weekly research explains the record and may write a repair the
  engine has no rule for (`tasks/weekly_research.md`, step 7b).
- **Files:** `reports/failure_lab.json` (new repairs, results, the record per kind and per tag, stopped kinds) and
  `failure_lab` in `reports/research.json`.

## Settings (`config.yaml` → `failure_lab`)

`enabled`, `per_run` (1), `min_trades` (100), `min_losers` (30), `min_share` (0.25), `near_miss_gross_r` (0.0),
`retire_after` (4), `max_depth` (2).
