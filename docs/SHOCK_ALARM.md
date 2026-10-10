# The shock alarm ⚡

Built 2026-10-10 at the operator's request ("build the shock alarm": tell me while the market falls or rallies
suddenly, not only at the next candle close). Code: `engine/shock.py` (the checks), `live_watcher.py` (every minute,
the note, the log), settings in `config.yaml` → `shock_alarm`.

## Why

The strategies look at the market only when their candle closes (4H, 1H, 30m, 15m), and a TEST alert also waits for
a confirming 5m candle. A sudden 3% drop at 14:07 was invisible until a setup formed at a close. The shock alarm
fills that gap. It is **information only**: never a trade signal, gate, size or approval, and it never changes a
strategy, a test or a risk rule.

## How it works

Every minute (5 seconds after it, when OKX has closed the 1-minute candle), while the PC watcher runs, it reads the
newest closed 1-minute candles of the watched coins (OKX public data, no keys) and checks:

| Check | Fires when | Why |
|---|---|---|
| Fast move | the last 15 minutes moved at least **1.8x** the coin's normal 1-hour range (ATR 14 of the 1H candles) | a move far beyond normal, measured in the coin's own units (ZEC moves more than BTC) |
| Volume spike | the last 15 minutes traded **5x** the normal volume (the 4 hours before) **and** moved at least 1.2x the 1H range | big players acting; volume without a move was mostly noise in the replay |
| Sweep | price broke **yesterday's high or low** (the UTC day, which starts 08:00 Beijing) by 0.1x the 1H range, **during a move of 1x the 1H range**, the first time today | stops sit there; the move often runs or snaps back |

A 1-minute candle missing in the window (2 or more) skips the check: never a guess.

## Keeping it quiet

- One note for all coins that fire in the same minute, with the other coins' 15-minute moves underneath.
- One note per coin in 30 minutes, unless its move has **doubled** in the same direction ("getting bigger").
- **Waves:** the coins of a market-wide move follow each other within minutes. Same-direction shocks within 15 minutes
  of a note are the same wave and only logged, unless **2 or more coins new to the wave** join it (the move is
  spreading: a second note).
- At most **8 notes a Beijing day**; `/shock off` stops them; `/pause` holds them. Held shocks are still logged.

## The note (an example)

```
⚡ Market shock · 23:12 Beijing
📉 ZEC 241.30 · -3.1% in 15 min (1.9x its normal 1H range) · volume 6.2x
Others (15 min): BTC -0.4% · ETH -0.6% · SOL -0.5% · SUI -1.0% · XRP -0.3%
⚠️ You follow a LONG on ZEC: check its stop on OKX.
Information only - not a trade signal. Your strategies check at their next candle close; never chase a shock.
```

What to do: if you have a trade open on that coin, check its stop on OKX. Otherwise **watch, don't chase**. If a
strategy sees a setup, a 👀 watch note or a 🔵 TEST alert follows at the candle close with a stop and size.

## The 14-day replay (tuning)

`live_watcher.py --shock-replay 14` (Windows: `windows\8_replay_shocks.bat`) replays the last 14 days minute by
minute on real OKX candles with these rules and sends nothing. The first settings (1.5x move, 3x volume, any sweep)
gave 226 shocks in 14 days and hit the daily cap every day. With today's settings (27 Sep - 10 Oct 2026, BTC ETH SOL
ZEC XRP SUI):

- 75 shocks, **44 notes**: about **3 a day**, at most 7 in one Beijing day;
- the 7 Oct crash: one note at 09:58 Beijing as it started (BTC broke yesterday's low on 9.5x volume, ZEC -2%), a
  second at 10:01 when ETH, SOL, SUI and XRP joined;
- the 8 Oct 23:12 drop: ZEC first, then a second note at 23:21 when BTC, ETH and SUI followed;
- **4 hours later only 35 of 75 had kept going** in the shock's direction - a coin flip. This is why the note says
  "never chase": a shock is not an edge until a strategy proves one.

## The log and the Sunday review

Each shock waits 4 hours, then one row goes to `journal\shocks.csv` on the PC (kept by updates): time, coin, side,
checks, move, volume, the level broken, sent / held (off, paused, same wave, daily cap), the % move 1 hour and 4 hours
later and the best / worst meanwhile (+ = it kept going), and how many strategy alerts followed on that coin within
4 hours (and how many in the same direction). With journal sync (`windows\6_journal_sync.bat`) the file goes to the
branch `journal`; the hourly scan (`journal_review.py`) writes `reports/shocks_review.json` and the weekly review
shows "⚡ Shock alarm": how many, by kind and coin, kept going vs reversed, and how many a strategy caught. When the
strategies miss most shocks, that is material for the research (a reversal or sweep version), tested like every card.

## Commands and files

- `/shock on` · `/shock off` · `/shock` (what it checks, notes sent today); `/status` shows "⚡ Shock alarm: ON · N
  sent today (max 8)".
- `config.yaml` → `shock_alarm`: `enabled`, `window_min`, `move_atr`, `vol_x`, `vol_move_atr`, `sweep`,
  `sweep_move_atr`, `cooldown_min`, `wave_min`, `max_per_day` (more in `engine/shock.py` DEFAULTS).
- Limits: it runs only while the PC watcher runs (the "PC is off" email covers that); about 1 minute late (closed
  1-minute candles); 6 OKX requests a minute, far under OKX's limits.
