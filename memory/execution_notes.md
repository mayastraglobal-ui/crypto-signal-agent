# Execution notes

Append-only. Observed data problems, fees and slippage. The engine records data problems when they START and when they END (not every hour), and every change of the fee settings. Slippage: the agent never trades, so there are no real fills yet - backtests use the configured slippage.

Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` (section 22), then its details. `-` = not applicable.

### START PROVE 1d data: DEGRADED: volume 52x normal on candle 09-23 00:00 UTC (possible bad data)
- timestamp: 2026-09-24 23:16 UTC · source: engine: hourly scan (data check) · evidence: FACT: measured by engine/data_quality.py · confidence: measured · strategy: - · asset: PROVE · timeframe: - · regime: - · review: 2026-10-24
  - signals from this data are blocked while it lasts

### Fee settings in use
- timestamp: 2026-09-24 23:16 UTC · source: engine: hourly scan (data check) · evidence: FACT: config.yaml -> costs · confidence: configured, not observed · strategy: - · asset: all · timeframe: - · regime: - · review: 2026-10-24
  - costs: {"long": {"maker_fee_pct": 0.1, "slippage_pct": 0.05, "taker_fee_pct": 0.1}, "short": {"funding_pct_per_8h": 0.01, "maker_fee_pct": 0.02, "slippage_pct": 0.05, "taker_fee_pct": 0.05}}

### END PROVE 1d data: DEGRADED: volume 52x normal on candle 09-23 00:00 UTC (possible bad data); DEGRADED: volume 245x normal on candle 09-24 00:00 UTC (possible bad data)
- timestamp: 2026-09-25 09:18 UTC · source: engine: hourly scan (data check) · evidence: FACT: the data passes the checks again · confidence: measured · strategy: - · asset: PROVE · timeframe: - · regime: - · review: 2026-10-25
  - problem first seen 2026-09-24 23:16 UTC UTC
