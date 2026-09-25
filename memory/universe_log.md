# Universe log

Append-only record of which coins the agent watches, and why (AGENT_PROMPT.md section 4). Written by the engine; only CHANGES are logged.
JOIN / LEAVE = signal list (top 7) · EXCLUDED / ELIGIBLE = rule results · FLAG = worth knowing, not excluded.

## 2026-09-24 18:21 UTC
- **EXCLUDED** PROVE - 7-day average volume $36M < $50M; order book too thin: $64k within 1% (need $250k)
- **FLAG** PROVE - price data DEGRADED - stays in the list, but no signals
- **EXCLUDED** LTC - 7-day average volume $34M < $50M
- **EXCLUDED** ONDO - 7-day average volume $30M < $50M; order book too thin: $181k within 1% (need $250k)
- **JOIN** BTC - starting list (no members yet): rank #1
- **JOIN** ETH - starting list (no members yet): rank #2
- **JOIN** ZEC - starting list (no members yet): rank #3
- **JOIN** XRP - starting list (no members yet): rank #4
- **JOIN** SOL - starting list (no members yet): rank #5
- **JOIN** BNB - starting list (no members yet): rank #6
- **JOIN** UNI - starting list (no members yet): rank #7

## 2026-09-24 19:16 UTC
- **EXCLUDED** ONDO - 7-day average volume $30M < $50M; 24h move +25.5% is beyond ±25% - suspended for the rest of the UTC day; order book too thin: $199k within 1% (need $250k)

## 2026-09-24 21:17 UTC
- **EXCLUDED** PROVE - 7-day average volume $36M < $50M; spread 0.128% > 0.1%; order book too thin: $49k within 1% (need $250k)

## 2026-09-24 22:18 UTC
- **EXCLUDED** PROVE - 7-day average volume $36M < $50M; order book too thin: $66k within 1% (need $250k)

## 2026-09-25 00:26 UTC
- **EXCLUDED** PROVE - order book too thin: $63k within 1% (need $250k)
- **ELIGIBLE** LTC - passes every rule again

## 2026-09-25 01:17 UTC
- **EXCLUDED** PROVE - spread 0.129% > 0.1%; order book too thin: $57k within 1% (need $250k)
- **LEAVE** UNI - outside the top 7 for 2 runs in a row (now #8)
- **JOIN** LTC - in the top 7 for 2 runs in a row (now #6)
