# Research sources

Append-only (AGENT_PROMPT.md section 18). Every source behind a strategy idea: title, URL (only if known - **citations are never invented**), date, claim, evidence class (FACT · RESEARCH_FINDING · BACKTEST_EVIDENCE · CLAIM · HYPOTHESIS · MODEL_OUTPUT · UNVERIFIED_OPINION), derived hypothesis and limitations. The engine adds one record when a strategy version is first tested (from its card); the reviews add external sources. Test results live in `memory/strategy_registry.csv`.

Every entry is a record: a `###` title, one line `- timestamp: … · source: … · evidence: … · confidence: … · strategy: … · asset: … · timeframe: … · regime: … · review: YYYY-MM-DD` (section 22), then its details. `-` = not applicable.
