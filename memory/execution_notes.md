# Execution notes

Append-only. Observed data problems, fees and slippage. The engine records data problems when they START and when they END (not every hour), and every change of the fee settings. Slippage: the agent never trades, so there are no real fills yet - backtests use the configured slippage.

Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` (section 22), then its details. `-` = not applicable.
