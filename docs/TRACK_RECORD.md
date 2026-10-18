# 📈 Live track record + 🚨 drift monitor (2026-10-13)

The operator asked for a professional signal tracker that learns, built "in a perfectly safe way". Before any real
money, the question is no longer "what did the backtest say?" but **"does it work live?"**

## The track record

Every hour GitHub's scan writes `reports/track_record.md` (and `.json`). It covers **every 🔵 TEST, 🟡 PAPER and
🟢 LIVE setup** it recorded:
- entry at the signal candle's close, with the same plan rules for every setup;
- results **after fees**.

It shows:

| Part | What |
|---|---|
| Per stage | closed setups, win %, average R, total R, worst drawdown, longest losing run |
| Per strategy and coin | the same, **next to the 5-year backtest on that coin** (from `reports/research.json`) |
| Equity curve | the running total of every live setup |

In Telegram, `/track` gives the short version. The Sunday review adds one line, plus a section in
`reports/weekly_review.md`.

The setups are the GitHub record (no 5m check). The alerts actually sent (5m-confirmed) are in the journal review,
and the 4H side-by-side record compares both.

## Your alerts vs the silent research records (2026-10-18)

GitHub records **every** 🔵 TEST setup of every program strategy that was positive on a coin in its backtest, also the
weak ones that never reach your Telegram (since 13 Oct only the strategies that are not FAILED and average at least
+0.10R on that coin send alerts). Mixing them made the headline look much worse than your real alerts: on 18 Oct it
said 22 closed, -16.04R, while your alerts were 1 trade (-1.05R).

So the track record, `/track` and the Sunday review now show two groups:

| Group | What it is |
|---|---|
| **Your alerts** (the headline) | setups whose strategy / coin is on the watcher's alert list (`signal_center.alert_pairs`), plus every 🟡 PAPER / 🟢 LIVE signal. Versions of one setup (same coin, direction and candle - one merged Telegram alert) count **once** |
| **Silent research records** | every other positive program pair. They are kept on purpose: they show whether the research's weaker results hold up live (this week they lost, as their near-zero backtest predicted) |

- The per-strategy table has a **Sent to you** column (✅ yes / silent).
- The 🚨 drift monitor pauses only pairs that can reach you (a silent pair never alerts, so there is nothing to pause).
- The list is today's alert list; when a strategy joins or leaves it, its past records move with it.
- Nothing else changed: the same results, the same checks, the same files.

## The drift monitor

For every strategy and coin with live results, it asks every hour: **is this still inside what its own backtest
calls normal?**

| Check | Pauses when |
|---|---|
| Losing run | the current run of L losses would appear in **less than 5%** of n-trade periods at the backtest's win rate on that coin: chance = 1 − (1 − q^L)^(n − L + 1), q = the backtest's loss rate. Example: 8 losses in a row at a 40% win rate |
| Average | **15+ live setups**, the live average **below 0R** and more than **2 standard errors** below the backtest average |

Weaker signs are listed as ⚠️ warnings without a pause.

**What a pause does:** that strategy and coin sends **no Telegram alerts** (TEST, PAPER and LIVE alike). You get one
🚨 note saying why.

**What it never does:** promote, change a rule, gate, size, cost or approval. Better-than-expected results are only
reported. Promotion stays the weekly review plus your tap.

**How a pause ends:** GitHub keeps recording that pair's setups silently, so the checks keep running on the growing
record. When neither check fires any more (for example, a win ended the run and the average is back in range), the
alerts come back by themselves and you get one ✅ note.

A pair without a backtest on that coin is never paused, only reported.

## Settings

`config.yaml` → `track_record`: `enabled`, `streak_p` (0.05), `min_streak` (3), `avg_min_n` (15), `avg_z` (2.0),
`sd_floor` (1.0 R), `curve_points`.

## First record (13 Oct)

5 closed TEST setups, all losses: −5.94R. They came from P03 V5 1h SOL, P01 V5 1h BTC and ETH, and P04 V5 30m XRP.
All of those are weak cells (FAILED overall, or about +0.01R on that coin) and no longer reach Telegram since 13 Oct.
They are still recorded, which is exactly what the record is for.
