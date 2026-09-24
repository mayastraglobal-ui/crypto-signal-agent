# Failure journal

Append-only (AGENT_PROMPT.md section 17), written by the engine. One entry per logged signal (validation / paper / live) that closed with a loss. Tags are measured by fixed rules (`engine/attribution.py`); root causes and fixes are added by the reviews - never by changing rules mid-trade. MAE / MFE = worst / best point of the trade, in R.

Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` (section 22), then its details. `-` = not applicable.
