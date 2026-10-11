# 🧭 Structure card (2026-10-11)

The playbook (section 2 and the pre-trade checklist) says: work top-down, and only trade when price is **at a
marked 4H zone, not in the middle of nowhere**. The agent already finds the market structure on every coin
(`engine/smc.py`: breaks of structure, liquidity pools, order blocks, fair value gaps). The structure card shows
it to you under every alert, so you can tick that checklist box in a few seconds.

**Information only.** It never makes, blocks or changes an alert, a rule, a size or a backtest. The strategies
decide the alerts exactly as before.

## What you see

Under every 🟡 PAPER / 🔵 TEST / 🟢 LIVE alert:

```
🧭 4H structure: uptrend · last BOS up at 109.80 (3 candles ago) · with your LONG
💧 Liquidity: above 115.20 (equal highs, 1.6R) · below 108.90 (yesterday's low, 0.9R)
📍 Location: ✅ at a 4H demand zone (order block 109.50-110.20)
Information only - the strategy's own rules made this alert.
```

- **4H structure:** the direction of the last 4H break of structure (BOS = with the trend, CHoCH = the first break
  against it). "⚠️ against your LONG" means the 4H structure points down.
- **Liquidity:** the nearest pool above and below price (equal highs / lows, swing points, yesterday's or last
  week's high / low) and how far away it is in R. **"⚠️ the pool above sits before TP1"**: price may stall there.
- **Location:**

| Location | For a LONG | For a SHORT |
|---|---|---|
| at a 4H demand zone (active order block or open fair value gap) | ✅ | ⚠️ buyers' area |
| at a 4H supply zone | ⚠️ sellers' area | ✅ |
| lower part of the 4H range (discount, below 35%) | ✅ | ⚠️ late |
| upper part (premium, above 65%) | ⚠️ late | ✅ |
| middle of the range (35-65%) | ⚠️ no edge | ⚠️ no edge |
| above / below the range | ℹ️ a breakout | ℹ️ a breakdown |

"At a zone" = inside it or within 0.25 x the 4H ATR of its edge. The 👀 watch note shows the location line only.

Everything is read at the **last 4H close** (closed candles only, like the strategies).

## /structure

- `/structure` - one line per coin: 4H trend and where price is.
- `/structure BTC` - the coin's trend and last break, the range and where price is in it, the nearest liquidity
  above and below, the nearest supply and demand zones.

## Learning from it (the weekly review)

GitHub's hourly scan saves each TEST / PAPER setup's location in `reports/signals_log.csv` (column
`structure_4h`, e.g. `good;demand;with` = verdict; location; 4H structure vs the direction). The Sunday review has
a section **"🧭 Location at the entry"**: closed setups grouped as *good* (a zone or edge that fits), *middle*,
*against*, *outside* (breakout) and *unknown*, with their average R after fees.

A difference only counts with **30+ setups in a group**. If one shows up, it is tested on 5 years of history first
(counted in the trials log), becomes a new version next to the old one, and goes TEST → PAPER only with your tap.
Nothing changes by itself.

## Settings

`config.yaml` → `structure`: `enabled`, `tf` (4h), `near_atr` (0.25), `middle` ([0.35, 0.65]).

## Same upgrade: two playbook extras

- **BTC dominance** (`/weather`, the market-weather report): BTC's share of the whole crypto market (CoinGecko,
  free, read every hour, kept 8 days in `reports/btc_dominance.json`) with its 24h / 7d change and the playbook's
  reading - e.g. "BTC down + BTC.D up: flight to BTC - careful with altcoin longs". Context only.
- **Drawdown brake** (`engine/risk.py`, `config.yaml` → `risk.drawdown_brake_pct` 10, `drawdown_brake_risk_pct`
  0.5): when the **real (LIVE)** account falls 10% below its peak, risk per trade drops to 0.5% until it is back at
  the peak. It does nothing today (no live trades; risk is already 0.5% in the first live month). The live watcher
  sizes with GitHub's risk % (`reports/risk_state.json`) when it is lower, and says why under the alert.
