# Market mechanics

Append-only. HOW crypto markets move - the mechanisms behind the strategies' edge blocks and the briefings (funding, liquidations, open interest, expiries, liquidity, sessions, macro, listings, costs). Knowledge, not signals: each entry says how strong its evidence is. Claude's weekly research adds records with a source, confirms or rejects the build session's unsourced CLAIMs with a new `Review:` record, and never edits an old one.

Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` (section 22), then its details. `-` = not applicable.

### Perpetual futures funding
- timestamp: 2026-09-25 13:00 UTC · source: Claude build session (Phase 17 B) · evidence: CLAIM: general market-structure knowledge written by the build session; no source was opened - the weekly research confirms it with a source or rejects it · confidence: medium · strategy: all · asset: all · timeframe: all · regime: - · review: 2026-10-25
  What: perpetual futures have no expiry; a 'funding' payment between longs and shorts keeps their price near spot.
  On Binance USDT-M futures it is usually paid every 8 hours (00:00 / 08:00 / 16:00 UTC). Positive funding = longs pay shorts.
  Why it matters: very positive funding means many leveraged longs - fuel for a long squeeze if price drops.
  In this engine (FACT, config.yaml): every backtest charges funding_pct_per_8h = 0.01% per 8 hours, always against the trade (cautious).

### Liquidation cascades
- timestamp: 2026-09-25 13:00 UTC · source: Claude build session (Phase 17 B) · evidence: CLAIM: general market-structure knowledge written by the build session; no source was opened - the weekly research confirms it with a source or rejects it · confidence: medium · strategy: all · asset: all · timeframe: all · regime: - · review: 2026-10-25
  What: when price moves against a leveraged position, the exchange closes it by force (liquidation).
  Forced closes are market orders in the same direction as the move, so they can push price further and trigger more liquidations: long wicks and fast moves.
  Why it matters: stops placed just beyond obvious levels are often hit by these wicks; the engine's 'volatility_spike' loss tag measures candles >= 3 ATR during a trade.

### Open interest
- timestamp: 2026-09-25 13:00 UTC · source: Claude build session (Phase 17 B) · evidence: CLAIM: general market-structure knowledge written by the build session; no source was opened - the weekly research confirms it with a source or rejects it · confidence: medium · strategy: all · asset: all · timeframe: all · regime: - · review: 2026-10-25
  What: open interest (OI) = the number of futures / options contracts still open.
  Price up + OI up = new positions opening (conviction); price up + OI down = shorts closing (short squeeze, often weaker).
  Not in the engine yet (no OI data source) - a candidate feature, not evidence.

### Options expiries (Deribit)
- timestamp: 2026-09-25 13:00 UTC · source: Claude build session (Phase 17 B) · evidence: FACT: expiry time and open interest are measured hourly in reports/feeds.json (Deribit API); the 'max pain pull' is only a CLAIM · confidence: medium · strategy: all · asset: BTC, ETH · timeframe: all · regime: - · review: 2026-10-25
  What: Deribit BTC / ETH options expire at 08:00 UTC; daily, weekly (Friday), monthly (last Friday) and quarterly expiries.
  The fact sheet shows the next expiries with open interest, put/call ratio and 'max pain' (the strike where option buyers get least).
  CLAIM (weak evidence): price is 'pulled' toward max pain before a large expiry. Treat it as a hypothesis to test, never as a reason to trade.

### Stop clusters and liquidity pools
- timestamp: 2026-09-25 13:00 UTC · source: Claude build session (Phase 17 B) · evidence: CLAIM: general market-structure knowledge written by the build session; no source was opened - the weekly research confirms it with a source or rejects it · confidence: low · strategy: all · asset: all · timeframe: all · regime: - · review: 2026-10-25
  What: many traders put stops just beyond obvious swing highs / lows and yesterday's high / low.
  The SMC / ICT idea: price 'sweeps' these pools, then reverses. This is the premise of S5-S8 and liquidity_sweep_reversal.
  In this engine: the premise is TESTED against control twins without the SMC part (section 9); so far no SMC strategy has beaten its twin (see the scoreboard).

### Trading sessions and weekends
- timestamp: 2026-09-25 13:00 UTC · source: Claude build session (Phase 17 B) · evidence: CLAIM: general market-structure knowledge written by the build session; no source was opened - the weekly research confirms it with a source or rejects it · confidence: medium · strategy: all · asset: all · timeframe: all · regime: - · review: 2026-10-25
  What: crypto trades 24/7, but volume is highest when Europe and the US overlap (about 12:00-16:00 UTC) and lower in the Asian night and at weekends.
  Why it matters: thin weekend markets can have sharper, less reliable moves; session-based strategies (S7 Silver Bullet) depend on these windows.
  In this engine: failure attribution tags 'wrong_session' entries (config.yaml attribution.main_sessions).

### Scheduled macro releases
- timestamp: 2026-09-25 13:00 UTC · source: Claude build session (Phase 17 B) · evidence: FACT: the engine blocks live entries within 60 minutes of each events.yaml release (config.yaml risk.blackout_minutes); the size of the reaction is a CLAIM · confidence: medium · strategy: all · asset: all · timeframe: all · regime: - · review: 2026-10-25
  What: US jobs (NFP), CPI, PCE and FOMC decisions are released at fixed times (8:30 a.m. / 2:00 p.m. New York).
  Crypto often moves sharply in the minutes after, in either direction; spreads widen and slippage grows.
  In this engine: events.yaml + a +-60 minute blackout for live entries.

### Exchange listings, delistings and maintenance
- timestamp: 2026-09-25 13:00 UTC · source: Claude build session (Phase 17 B) · evidence: FACT: announcements are fetched hourly into reports/feeds.json (Binance); their price effect is a CLAIM · confidence: medium · strategy: all · asset: all · timeframe: all · regime: - · review: 2026-10-25
  What: a new listing on a large exchange often brings a burst of volume and volatility; a delisting or a deposit / withdrawal suspension can cut liquidity.
  Why it matters: signals on a coin with a listing / delisting / network upgrade that day are less reliable; the briefing should mention them.
  Not an engine rule yet.

### Fees and slippage measured in R
- timestamp: 2026-09-25 13:00 UTC · source: Claude build session (Phase 17 B) · evidence: FACT: engine arithmetic (config.yaml costs; research cost viability) · confidence: high · strategy: all · asset: all · timeframe: all · regime: - · review: 2026-10-25
  What: a trade's cost in R = (fees + slippage + funding) / the distance to the stop.
  A tight stop makes the same fee a bigger share of the risk: on 5m / 15m, fees can eat most of a small edge.
  In this engine: every backtest pays fees + slippage; a strategy is not cost-viable if the round-trip cost is more than 1/4 of the stop (0.25R), and it must stay profitable with costs +50%.

### Spot ETF and stablecoin flows
- timestamp: 2026-09-25 13:00 UTC · source: Claude build session (Phase 17 B) · evidence: CLAIM: general market-structure knowledge written by the build session; no source was opened - the weekly research confirms it with a source or rejects it · confidence: low · strategy: all · asset: BTC, ETH · timeframe: all · regime: - · review: 2026-10-25
  What: net money into spot bitcoin / ether ETFs and new stablecoin supply are watched as demand signals.
  Evidence that they predict the next day's price is weak and disputed; news headlines about them are CLAIMs.
  Not in the engine (no data source); the feeds give headlines only.
