# Changelog

Every change to the rules, config, prompt or engine is logged here (AGENT_PROMPT.md §0, §22).
Newest entries at the bottom. Format: date · who · what · why.

## 2026-09-24 · Operator (Maya) + Claude (BUILD mode) · Phase 0 — operator settings
- **Risk per trade:** 1.0% → **0.5%** (`config.yaml` → `account.risk_per_trade_pct`). Why: AGENT_PROMPT.md §15/§26 — 0.5% during validation and the first live month, max 1% after. Operator decision.
- **Costs split by direction** (`config.yaml` → `costs`). Why: §11 "longs use spot costs, shorts use futures costs" + funding. Exchange not decided yet, so Binance VIP 0 fees are used. Operator decision.
  - LONG (spot): taker 0.10%, maker 0.10%, slippage 0.05% — unchanged from before.
  - SHORT (futures only): taker 0.05%, maker 0.02%, slippage 0.05%, **funding 0.01% per 8h always charged against the short** (cautious: real funding history is not fetched, and it can be positive or negative).
  - Note: shorts now pay lower fees than before (futures fees are lower than spot fees). This is more accurate, not a lower bar. Validation gates are unchanged.
- Shorts are labelled **"futures only"** in reports and emails.
- Added `tests/test_costs.py`, including guard tests that fail if costs are set to 0, risk goes above 1%, or the validation bar is lowered.

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 1 — data quality
- New `engine/data_quality.py` (AGENT_PROMPT.md §3). Checks every candle table: order, duplicates, unfinished candles (dropped, never used), zero/negative/missing prices, high < low, open/close outside the range, negative volume, off-grid timestamps, missing candles, stale feed, volume spikes on the newest candles, Binance-vs-OKX price difference.
- States: GOOD (signals allowed) · DEGRADED (analysis only) · UNSAFE (no signals). System UNSAFE when BTC is UNSAFE, BTC is missing, or > 30% of coins are UNSAFE/failed → `DATA_STALE / SIGNAL_DISABLED`, all signals stop.
- A signal now also needs GOOD data on its timeframe, its higher timeframe and the cross-exchange check. UNSAFE data is not backtested; open forward-test signals are not scored on UNSAFE data.
- `scanner.py`: `_finish` no longer silently cleans candles; all downloads go through `fetch_checked()` so problems are reported, not hidden. New report section "0. Data check" and `reports/data_quality.json`. New `--fault` option (offline only) to plant bad data for testing.
- `notify.py system`: one `[SYSTEM] DATA_STALE / SIGNAL_DISABLED` email when data turns UNSAFE, one "Data recovered" email when it recovers (state kept in `reports/system_alert_state.json`). Scan-failure email now starts with `[SYSTEM]`.
- Thresholds in `config.yaml` → `data_quality`. Refinement vs the plan: old gaps (outside the newest 300 candles, under 1% of history) are only a note, because they do not affect current indicators.
- Workflows: `scan.yml` runs `notify.py system`; new `tests.yml` runs all tests on every push/PR.
- Tests: `tests/test_data_quality.py` (planted faults, look-ahead tests, end-to-end offline runs, email once-only behaviour).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 2 — tradable universe
- New `engine/universe.py` (AGENT_PROMPT.md §4): **7 signal coins** (only these can give signals) + **3 research-only coins** (backtested, never a signal), ranked by 24h quote volume; BTC and ETH always included when eligible.
- **Eligibility** (all must pass; limits in `config.yaml` → `universe`): ≥ 180 days history · 24h volume ≥ $50M · 7-day average volume ≥ $50M · 24h volume ≤ 3× the 7-day average · 24h move within ±25% (else suspended for the rest of the UTC day) · spread ≤ 0.10% · ≥ $250k order-book depth within 1% on each side · daily price data not UNSAFE · not on an exclusion list · does not behave like a stablecoin (price within ±2% for 30 days — measurable, not by name).
- **Hysteresis:** a newcomer must rank top 7 for 2 runs in a row to join; a member must rank outside the top 7 for 2 runs in a row to leave. A member that breaks a rule, or whose data turns UNSAFE, leaves at once. A freed slot stays empty until a coin qualifies (BTC/ETH re-join at once).
- **Operator decisions (2026-09-24):** NEAR added to `exclude_ai` ("the blockchain for AI"); a member with DEGRADED data stays in the list but gets no signals (Phase 1 gate); suspected wash volume (24h volume > 1000× the 1% depth) is **flag only** for now — review the threshold after a week of live data.
- Config: `always_include` reduced to BTC, ETH (SOL, BNB, XRP must now earn their place); `top_n_coins` and `market.min_24h_volume_usdt` ($30M) replaced by the `universe` section ($50M); new `exclude_gold` (PAXG moved there, XAUT added).
- Engine: only the 10 research coins get full downloads (was ~25 coins) → faster runs, fewer backtest trades; the validation bar is unchanged, so passing is slightly harder.
- New outputs: report section "0b. Coins this run", `reports/universe.json`, `reports/universe_state.json`, append-only `memory/universe_log.md` (changes only). `scan.yml` now also saves `memory/`.
- Offline test feed: extra coins (a hidden stablecoin FAKEUSD, a +40% mover PUMP), `--scenario` option, deterministic random numbers.
- Tests: `tests/test_universe.py` (22 tests: every rule, hysteresis sequences, log-only-changes, 3-run end-to-end rotation).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 3 — timeframes 1W → 5m
- New `engine/timeframes.py` (AGENT_PROMPT.md §3, §5): `align_higher()` — the one safe way to use a higher timeframe (only candles closed at or before the lower candle's close); `rolling_7d()` (rolling 7-day candles from closed daily candles, windows with a missing day dropped); `consistency()` (a higher candle must equal the lower candles inside it: open/high/low/close exactly within 0.01%, volume within 1%); timeframe models A–D with roles (bias / setup / trigger / execution / veto).
- Downloads: **1W** (500 weekly candles ≈ 10 years or since listing) added; **1D** from 400 to 1000 candles (≈ 2.7 years). 7D built from the daily candles (no extra download). 1W goes through the Phase 1 data check (stale = newest closed weekly candle older than 2 weeks).
- **Cross-timeframe check** on every research coin (5m>15m, 15m>30m, 30m>1h, 1h>4h, 4h>1d, 1d>1w; newest 50 fully covered candles): a disagreement makes the HIGHER timeframe DEGRADED. Not run in offline mode (synthetic timeframes are generated independently) — tested with unit tests instead.
- `config.yaml`: `timeframes` gets `1w: 500` and `1d: 1000`; new `timeframe_model` section — **Model B active** (1W veto → 1D → 4H → 1H → 30m setup → 15m trigger → 5m entry); A, C, D written down for later comparison; D needs 2H, which is not downloaded until D is tested.
- **Unchanged on purpose:** the 8 current strategies still use the same higher-timeframe filter (`htf_up`/`htf_down` via `LEGACY_HTF`); a regression test proves identical output. The 1W veto and "2 of 1D/4H/1H" rule arrive with the regime engine (Phase 5) and strategy spec v3 (Phase 7). Longer daily history means the daily EMAs behind the 4H filter warm up better, so backtest numbers may move very slightly.
- Report: new section "0c. Timeframes loaded" (model, candle counts per timeframe, weekly history start, cross-check result). `latest.json` gets a `timeframes` block.
- Tests: `tests/test_timeframes.py` (18 tests: look-ahead tests for alignment and 7D, mid-week weekly visibility, planted cross-timeframe errors, legacy filter identical, weekly data checks, model config, offline end-to-end).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan + operator addition) · Phase 4 — feature engine + candle evidence
- New `engine/features.py` (AGENT_PROMPT.md §7): per closed candle — body/wick %, close location, consecutive closes, range ÷ ATR (expansion ≥ 1.5, contraction ≤ 0.5), ATR vs its 100-candle median, momentum persistence, relative volume (vs the previous 20), volume acceleration, displacement (range ≥ 1.5×ATR, body ≥ 60%, rel. volume ≥ 1.3), engulfing, pin bars, swings (3 candles each side, **known only 3 candles later**), HH/HL/LH/LL structure, RSI divergence at confirmed swings, support/resistance from confirmed swings (+ touches), consolidation, breakout/breakdown, retest, failed breakout, impulse, pullback (38.2–61.8%), Stochastic RSI, ROC, Keltner, VWAP (UTC-day reset, below 1D only), OBV. Volume profile not built (data not available). Limits in `config.yaml` → `features`.
- Strategy rule language: every feature is usable by name (e.g. `displacement_up`, `close_loc > 0.7`). Existing building blocks are never replaced; the 8 current strategies give **identical** results (offline scoreboard compared before/after, plus a test).
- New `engine/evidence.py` — **candle evidence, RESEARCH EVIDENCE, NOT A SIGNAL**: for displacement, engulfing and pin-bar candles on each timeframe (pooled over the 10 research coins): enter at the next open, stop 1 ATR, share reaching +1R/+2R/+3R **after costs** before the stop (max 30 candles; stop first when both touch in one candle). **Operator addition:** a **random-entry baseline** per pattern (same coins, same direction, same stop/targets/costs, 10 random entries per pattern entry, fixed seeds) and a verdict: "beats chance" only if +1R share beats random by more than 2 standard errors; "too few to judge" under 30 entries.
- Outputs: report sections "0d. Market features now" (signal coins, 1H) and "0e. Candle evidence"; `reports/features.json`; `reports/feature_evidence.json`. New `memory/feature_notes.md` (definitions; all features NOT YET TESTED, the candle patterns RAW EVIDENCE).
- Scan time: about +10 s (mostly the evidence tool).
- Tests: `tests/test_features.py` (20 tests: whole-table look-ahead test, swings invisible until confirmed, hand-made candles for each definition, strategies unchanged, evidence maths incl. costs and stop-first, planted edge "beats chance" vs random data not, determinism, end-to-end).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 5 — market regime engine
- New `engine/regime.py` (AGENT_PROMPT.md §6): a label for **every closed candle** on 1W/1D/4H/1H (so later phases can segment backtest trades by regime): STRONG_BULL, WEAK_BULL, RANGE, HIGH_VOL_RANGE, WEAK_BEAR, STRONG_BEAR, EXPANSION (up/down), COMPRESSION, TRANSITION, UNCLEAR.
- Inputs: 3 direction votes (EMA structure close/EMA-fast/EMA-slow; EMA-fast slope over 10 candles vs ±1 ATR; HH/HL vs LH/LL swing structure from Phase 4), ADX(14) (> 25 strong, < 20 weak), ATR vs its 100-candle median, Bollinger width percentile (vs the last 100 candles), relative volume. Rules checked in order: UNCLEAR (not enough history) → EXPANSION → COMPRESSION → STRONG (3 votes + ADX ≥ 25) → WEAK (≥ 2 votes) → HIGH_VOL_RANGE / RANGE (mixed votes, ADX < 20) → TRANSITION (mixed votes, ADX ≥ 25) → UNCLEAR (mixed, ADX 20–25).
- **Change vs the approved plan (found by testing):** EXPANSION uses **range expansion** (a candle range ≥ 1.5× the ATR before it, within the last 3 candles) instead of "ATR ≥ 1.5× normal". The 14-candle ATR reacts too slowly: a breakout straight out of a squeeze (the classic expansion) could never reach 1.5× its normal ATR. §7 names range expansion directly.
- Evidence record for the newest candle: supporting and contradicting evidence in plain words; confidence strong (0 contradictions) / moderate (1) / weak (≥ 2, or UNCLEAR) — never a %; ADX within 2 points of 20/25 counts as a contradiction; volatility / momentum / structure states.
- **Operator decisions (2026-09-24):** weekly uses **EMA 10/40** (≈ the calendar span of 50/200 daily; 200 weeks = 4 years of history many coins lack); all other timeframes EMA 50/200. Regimes and permission are **shown only** — they gate strategies from Phase 7.
- Permission (§5): LONG needs ≥ 2 of 1D/4H/1H bullish (STRONG/WEAK_BULL or EXPANSION up) and no 1W STRONG_BEAR (weekly veto); SHORT mirror; otherwise NO TRADE with the reason.
- Outputs: report section "0f. Market regime" (table + BTC evidence), `reports/regime.json`, append-only `memory/market_regime_log.md` (once per UTC day, BTC context first; not written offline). Limits in `config.yaml` → `regime`.
- Note found while testing: offline results depend on the clock hour (synthetic timeframes are anchored to "now"); before/after comparisons must run in the same hour. The strategy scoreboard is identical to the pre-Phase-5 code when compared that way.
- Tests: `tests/test_regime.py` (17 tests: every rule row, realistic zig-zag trends, fresh squeeze → COMPRESSION → breakout → EXPANSION, weekly 10/40, confidence counting, permission + weekly veto, look-ahead, daily log once per day).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 6 — SMC / ICT detectors
- New `engine/smc.py` (AGENT_PROMPT.md §9, version smc-1.0): one pass over closed candles; every event stamped at the candle where it became knowable. Liquidity pools (confirmed swings, equal highs/lows within 0.1%, PDH/PDL, PWH/PWL from the last CLOSED day/week), sweeps (wick ≥ 0.1 ATR through a pool and close back inside), BOS, CHoCH (needs a displacement candle within 3 candles; otherwise WEAK_BREAK, trend unchanged), fair value gaps (≥ 0.25 ATR; first retrace; filled), order blocks (last opposite candle before the displacement of a BOS/CHoCH; retest; invalid on a close through it), breakers (retest from the other side), premium/discount (last swing range), OTE (62–79%), killzones (New York time, DST handled, candles up to 1H), power of 3 (consolidation → sweep → CHoCH within 10 candles). Inducement not implemented (§9: research only until defined).
- A liquidity pool is used up only by a real sweep (≥ 0.1 ATR through) or a close beyond it; a tiny poke leaves it alive (found by testing: otherwise equal highs could never form).
- Runs on 4H/1H/30m/15m/5m for the research coins. SMC event flags join the features (usable by name as `smc_*` in rules) — the 8 current strategies are unchanged (scoreboard identical when compared in the same hour).
- **Operator decisions (2026-09-24):** live log `memory/smc_events.csv` = signal coins, 4H/1H/30m/15m, starting one hour before the first live run (no backfill), append-only, watermarks in `reports/smc_state.json`; each row carries killzone and the higher-timeframe regime at that moment. SMC events added to the candle-evidence table vs random entries: sweep (bull/bear), BOS (up/down), CHoCH (up/down), first FVG retrace (bull/bear) — research evidence, not a signal.
- Outputs: report section "0g. SMC now", `reports/smc.json`, `memory/smc_research.md` (definitions + status). `requirements.txt` gets `tzdata` (New York time everywhere). Scan time ≈ +15 s (bigger evidence table).
- Tests: `tests/test_smc.py` (19 tests: hand-made candles for every concept, AMD, killzones summer/winter, previous-day levels only from closed days, look-ahead, event log watermarks without backfill or duplicates, offline end-to-end).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 7 — strategy spec v3, lifecycle, market gates, S5–S8 + control twins
- **Strategy ID cards** (AGENT_PROMPT.md §10): every strategy in `strategies.yaml` now has id, version, status, family (A–H), gate type, allowed regimes, hypothesis, source, stop, targets, time stop, cooldown, control twin, known weaknesses and a changelog. New `engine/strategy_spec.py` checks every card; an incomplete card is listed in the report ("not run") and skipped - the engine keeps running.
- **Tested versions are immutable:** the trade-deciding parts are fingerprinted in `memory/strategy_registry.csv` (§22; one row per version × timeframe with status, metrics, failed gates, dates). A tested version whose rules are edited without a new version number is refused, with the reason in the report. `memory/experiments.md` counts every version ever tested; each earlier version of the same idea raises the bar by +0.02R (§11).
- **Lifecycle** (§12, new `engine/lifecycle.py`): the author sets IDEA / FORMALIZED / RETIRED; the engine sets BACKTESTING / VALIDATION / FAILED per version × timeframe every run and logs each change in `memory/strategy_lifecycle.md`. PAPER_TRADING needs the Phase 8 tests (not reachable yet); APPROVED always needs the operator's yes.
- **Operator decisions (2026-09-24):**
  1. Pass bar = §12 "→ VALIDATION": ≥ 30 trades, **≥ +0.10R** per trade after costs (was +0.05R), **PF ≥ 1.2** (was 1.15), **max drawdown ≤ 10R** (new), still profitable in both train and unseen test, ≥ 10 unseen-test trades. Stricter, never lower.
  2. **Only APPROVED versions give emailed signals** (`[ENTRY]` subject). VALIDATION versions give "validation signals": shown in the report and logged in `reports/signals_log.csv` (new columns version, stage, tp_split), never emailed.
  3. Gates: trend / breakout / SMC = 2 of 1D/4H/1H in the trade direction + weekly veto (no trade against 1W STRONG trend); reversal type = 2 of 3, no weekly veto (§5); **mean reversion** = only in RANGE / HIGH_VOL_RANGE and never against a STRONG 1W/1D/4H trend (resolves the §5 vs §6 clash).
  4. S5–S8 v1.0 run without 5m confirmation (Phase 10 adds it as a new version, tested against these).
  5. S5 on 30m/15m, S6 and S7 on 15m, S8 on 1H/30m; no 5m (fees 0.5–0.8R per trade there).
- **Market gates applied to every candle, in backtests and live** (closed candles only): allowed regimes on the regime timeframe (1D for 1D, 4H for 4H, 1H for 1H and below) + the gate type above. The scoreboard shows how many signal candles each gate stood down.
- **Existing 8 strategies re-versioned as v1.0:** rules, stops and hold times unchanged; they now carry allowed regimes and a gate (rsi2_dip_buy = mean reversion; liquidity_sweep_reversal = reversal; the rest trend). Their backtest numbers change because trades outside their regimes / without permission are no longer counted - that is the point of the gates.
- **Backtester:** structure stops (level + 0.2 ATR buffer, no trade if wider than `max_width_atr`), targets in R, at a level, or "max(3R, next pool)", a "need ≥ 2R to the pool" rule, cooldown between trades; skipped setups are counted on the scoreboard. Next-bar-open fills, full costs and stop-first are unchanged. The forward test replays each logged signal with its own targets.
- **SMC S5–S8 + control twins** (§9) - see `memory/smc_research.md`. The SMC engine gains per-candle context columns (range position, active order blocks, in-OB, prior-day sweep, sweep extremes, nearest pools, prior-day levels, killzones), and timeframes below 4H get the newest CLOSED 4H context as `h4_*`. New rule helpers `within(x, n)` and `bars_since(x)`.
- Report: section 2 explains that only APPROVED strategies give signals (+ "2b. Validation signals - NOT emailed"); section 3 shows version, status, max drawdown, stood-down and skipped counts; new "3b. Strategy lifecycle and control twins" (twin verdict only with ≥ 30 trades and ≥ 10 unseen-test trades on both sides).
- Tests: `tests/test_strategy_spec.py` (26 tests: the shipped cards, bad cards, fingerprints/immutability, registry CSV, targets, every gate type incl. weekly veto and EXPANSION direction, the pass bar and re-tune penalty, structure stops/cooldown/skips, look-ahead tests for the SMC context and h4_* columns, offline end-to-end incl. an edited-without-new-version card). `tests/test_costs.py` guard raised to the new bar.

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 8 — research layers A/B/C, cost viability, stress, ±20% test, automatic PAPER_TRADING
- **New daily research run** (`research.py`, workflow `.github/workflows/research.yml`, 00:40 UTC + a manual button; shares the `scan` concurrency group). It uses exactly the same engine as the hourly scan (`scanner.prepare_coin` / `strategy_signals` / `backtest`) on the signal + research coins of the newest hourly scan. Long history: new `engine/history.py`, cached in the GitHub Actions cache (`data/history`, git-ignored), only new candles downloaded; every table re-checked by `engine/data_quality.py`; long history only from Binance (if Binance is down the run fails with a `[SYSTEM]` email and yesterday's statuses stay).
- **Layers** (§11, new `engine/research.py`): **A** = last 15 days, days 1–10 vs 11–15, recomputed hourly, shown only. **B** = full history (develop = first 70% of each coin, validate = last 30%). **C** = walk-forward over 6 equal time windows (first = warm-up). Also: long vs short, results per coin, drawdown now measured in time order.
- **VALIDATION gate** (now on Layer B, once a day) adds **cost viability**: median fees + slippage per trade ≤ 0.25R, i.e. stop ≥ 4× the round-trip cost (`validation.max_cost_to_r`).
- **PAPER_TRADING (automatic, §12)** = VALIDATION + walk-forward + edge on ≥ 3 coins + costs +50% still profitable + every ±20% variant still profitable + no HIGH OVERFITTING RISK flag (> 50% of the profit from one coin or one window) + beats its control twin (overall and validate part, ≥ 30 / ≥ 10 trades both sides). Paper signals are logged in `reports/signals_log.csv` (stage PAPER_TRADING), never emailed.
- **Leaving paper:** RETIRED if the last 20 paper signals average < −0.10R or the paper record falls > 8R from its best point; back to its Layer B status after failing the VALIDATION bar 2 research runs in a row. RETIRED stays retired (a new version is needed). The engine never sets APPROVED.
- **Operator decisions (2026-09-24):** heavy tests daily (also ends hourly status flipping); history 1D/4H/1H since listing, 30m 2 years, 15m 1 year, 5m 90 days; walk-forward ≥ 3 of 5 profitable + together profitable (< 5 trades = no information); ±20% = every single variant > 0R; costs +50% > 0R; leave paper after 2 failed runs.
- **Strategy cards get `params:`** (numbers in rules written as `{name}`), so the ±20% test can move them. Fingerprints are taken from the rendered rules: all 16 v1.0 fingerprints are **unchanged** (guarded by a test) - no new versions, no re-tune penalty. Built-in variants: stop size (ATR multiple, or buffer + max width) and time stop.
- **Hourly scan:** no longer judges strategies; statuses and Layer B/C numbers come from the latest research run (`reports/research.json`), Layer A is computed each hour; 5m download raised to 5000 candles (15 days). Before the first research run every version shows "waiting for the first daily research run". The per-coin code moved into shared functions (scoreboard proven identical to the previous code in the same hour before the judging change).
- Report: section 3 (Layer B/C/A columns), 3b (lifecycle + twins from research), new 3c (history used per timeframe). `memory/strategy_registry.csv` gains walk-forward, stress, ±20% worst, coins, cost, overfit, paper columns (older files still readable). `notify.py research_failed`.
- Tests: `tests/test_research.py` (history cache full/incremental/deeper, every layer, every gate, freeze rules, registry format, frozen fingerprints, end-to-end scan → research → scan incl. an edited-in-place card refused by both runs).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 9 — failure attribution, MAE / MFE, missed moves
- New `engine/attribution.py` (AGENT_PROMPT.md section 17). Every backtest trade (daily research run) and every logged signal gets reason tags by fixed rules (numbers in `config.yaml` → `attribution`):
  - **at entry (measured for winners too):** range_market (ADX < 20 on the trade's timeframe; not for mean reversion), htf_conflict (a STRONG opposite regime on 1W/1D/4H/1H), low_relative_volume (< 0.8x), overextended_entry (≥ 2 ATR from EMA20 or RSI ≥ 75 / ≤ 25), late_entry (≥ 3 ATR the trade's way in the 10 candles before), no_displacement (breakout / momentum / SMC continuation only), wrong_session (intraday, outside London / NY AM / Silver Bullet), data_issue;
  - **during the trade:** stop_too_wide (> 2.5 ATR), false_breakout (breakout / momentum, back inside within 5 candles), trend_reversal, regime_mismatch, volatility_spike (a ≥ 3 ATR candle), ob_failed (4H order block broken, S6);
  - **losers only:** fees_slippage, funding, stop_too_tight (stopped, then TP1 within the hold time), bad_target (≥ 80% of the way to TP1), sweep_continued, indicator_lag (trend / momentum trade never past +0.25R);
  - strategy level: structural_change (develop profitable, validate losing). Not measurable yet, and said so: news_event, overtrading (Phase 11), fvg_ignored.
- **Operator decisions (2026-09-24):** tag rules and numbers as proposed; **systematic** = ≥ 30 losses and more common among losers than winners by > 2 standard errors (loser-only tags: in ≥ 25% of losses); strong move = ≥ 5x the 1H ATR within 12 hours, checked daily over the last 24 hours; failure journal = one entry per logged losing signal (validation / paper / live), backtest losses as summaries; candidate lessons (systematic in ≥ 2 tests) are shown only - `memory/lessons.md` waits for the reviews (Phase 14).
- **MAE / MFE** and funding paid are measured for every simulated trade (backtest and forward test).
- Research run: per strategy version × timeframe a tag table (losers vs winners, average R with / without), MAE / MFE, results by regime / session / direction, and the 8 questions of section 17.3 answered from the numbers (incl. the ±20% stop-size results as the evidence for any stop change); **missed moves** with, per strategy and timeframe, "signal / blocked by the regime gate / blocked by the permission gate / no valid stop or target / no setup". Written to `reports/research.json`, `memory/missed_trades.md`.
- Hourly scan: each logged signal records its conditions, regime and session at entry; when it closes it gets MAE / MFE and tags, and a losing one is written to `memory/failure_journal.md` (new `signals_log.csv` columns: conditions, regime_at_entry, session, mae_r, mfe_r, tags). Report section **3d. Why trades lose**.
- Found by testing: writing text tags into an all-empty column of the signals log failed (pandas reads it as numbers) - text columns are now kept as text.
- Tests: `tests/test_attribution.py` (every tag on hand-made candles, loser-only tags never on winners, the statistics rule, diagnosis, missed moves, no look-ahead, forward test + journal); research end-to-end test extended.

## 2026-09-24 · Operator request + Claude (BUILD mode, operator-approved plan) · Housekeeping — storage and test speed
- **Storage (operator request):** the large report files replaced every run (`reports/latest.json` 369 KB, `smc.json` 207 KB, `features.json` 111 KB, `feature_evidence.json`, `regime.json`, `data_quality.json`, and the daily `research.json`) are no longer committed to main (~800 KB per hourly scan). New `publish_live.py` publishes them to branch **`live-reports`** as ONE parentless commit, force-pushed every run (no history); files a run did not make are carried over from the previous copy. Both workflows save main first, then publish (a failure turns the run red → `[SYSTEM]` email). The hourly scan first restores `research.json` from `live-reports`. The files are `.gitignore`d on main; main's existing history is NOT rewritten (operator decision; ~2 MB of old copies stay).
- Main keeps the history that matters: `memory/`, `reports/signals_log.csv`, `strategy_scoreboard.csv`, `reports/daily/`, `latest.md`, plus the small state files (`universe.json`, `*_state.json`, `notified.json`).
- `notify.py` is unchanged (it reads the files in the same run, before anything is committed; its links point to `latest.md` on main). README file table and new `reports/README.md` link the files on `live-reports`; `latest.md` ends with links to them and starts with a **storage line** (repository size from GitHub's API, size of this run's large files).
- **Rulebook (operator approved):** AGENT_PROMPT.md §22 memory table gets one row - "branch `live-reports`": where the large replaced-every-run files live, so Claude's briefings read them there.
- **Tests (operator request):** from ~9.5 min to ~2.7 min. The 4 end-to-end tests that only read a plain offline scan now share one run (`shared_offline_run()`); new `tests/run_all.py` runs the test files in parallel (4 processes, slowest first) and is what the Tests workflow runs. Same tests; `python -m unittest discover -s tests` still works. Workflow time limit stays 25 min (raised in Phase 8).
- Tests: `tests/test_publish.py` (one commit and no history on a temporary git server, carry-over, restore, restore before the branch exists, never overwriting this run's file, main untouched, `.gitignore` and workflow order).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 10 — signal state machine, 5-minute confirmation, position book
- **States (§13, new `engine/positions.py`):** every logged signal is AWAITING_5M → ENTRY_TRIGGERED → POSITION_ACTIVE → TP1_HIT → CLOSED (TP / BE / TRAIL / SL / TIME / EXIT_RULE), or EXPIRED / INVALIDATED. `reports/signals_log.csv` gains state, planned entry, entry time, 5m bars, confirmation time, optional 5m SMC signs, close reason, current stop, warnings, next action (older rows still load: OPEN = active). Every state change is appended to the new `reports/position_events.csv`; `reports/positions.json` holds the book. WATCH / SETUP_FORMING (filters open / all entry rules but one true) are shown in report section 2c only.
- **5-minute protocol (§8, new `engine/confirm5m.py`, `config.yaml` → `confirm_5m`):** after a closed 15m / 30m trigger of a card with `confirm_5m: true`, up to 6 closed 5m bars: CONFIRMED = closes in the trade direction, body ≥ 50%, relative volume ≥ 1.0, within entry ± 0.2R, no opposing displacement since the trigger; INVALIDATED = stop touched or a 5m BOS / CHoCH against the trade first; EXPIRED = none in 6 bars. Entry = the confirming bar's close (+ slippage); the stop and target prices stay where the trigger put them. Optional 5m sweep / displacement / engulfing are recorded, never required.
- **Backtest:** `backtest_5m()` runs the protocol and manages the trade on 5m bars (same clock-time time stop; the exit rule fires on the 5m bar closing with the trigger candle). **Fair control twin:** the same signals without the check, entered at the next open and managed on the same 5m bars over the same period. For these cards develop / validate and the walk-forward windows are taken over the 5m history (90 days) - with the trigger timeframe's year every trade would sit in "validate" and 4 of 5 windows would be empty.
- **New cards S5-SWEEP-MSS-FVG-5M, S6-OB-FVG-5M, S7-SILVER-BULLET-5M, S8-PDH-PDL-SWEEP-5M (v1.0):** exactly their plain version + the 5m check; the engine refuses a 5m card whose rules, stop, targets, exits, gates or hold time differ from its twin, or that runs outside 15m / 30m. The 16 existing fingerprints are unchanged.
- **Monitoring (§16, operator decision):** open positions follow exactly the backtest's rules - **now including the strategy's exit rule, which the forward test did not apply before** - and are managed on 5m bars for -5M strategies. An opposite structure break, an opposite displacement candle, a regime change or ATR ≥ 2x since entry only add "watch: ..." to the next action (never tested, so never an exit).
- **Position book (§16):** first thing in `latest.md` and in `[ENTRY]` emails (which now end "Research signal. Not financial advice."): active (APPROVED) · awaiting 5m · paper (PAPER_TRADING / VALIDATION) · closed today with R · day / week R vs -3R / -6R · heat n/3. Limits are shown only; Phase 11's risk engine enforces them.
- **Fixed (found while planning): PAPER_TRADING signals were never logged** (the plan filter only let VALIDATION and APPROVED through), so no paper record could build up and the "leave paper" rules could not work. No strategy had reached PAPER_TRADING, so nothing was lost.
- **Also changed:** every plan is logged, not only the best one per coin shown in the report (each strategy's paper record needs all of its signals); each hourly run looks at every candle closed since the previous run (`signals.scan_interval_minutes: 60`: 15m 4 candles, 5m 12) instead of 2 candles, so 15m / 5m triggers no longer fall between two runs. An APPROVED -5M setup is not emailed at the trigger; its state-change emails come with Phase 12 (none is APPROVED).
- **Operator decisions (2026-09-24):** keep the hourly scan (each run replays the closed 5m bars - exact record, alerts up to an hour late; faster cadence decided in Phase 11/12); §16 extra checks = warnings only; add the 4 -5M cards with the plain versions as control twins.
- Tests: `tests/test_positions.py` (every protocol condition, expiry, invalidation, short mirror, never a bar from before the trigger, no look-ahead at any cut; 5m backtest entry / twin / skip / truncation; 5m cards = twin + check; state moves; book incl. day / week sums; confirm → TP1 → breakeven, exit rule, time stop, old log files; offline end-to-end). Library tests updated to 20 cards, frozen fingerprints extended.

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 11 — risk engine and event blackout
- **New `engine/risk.py`** (AGENT_PROMPT.md section 14 steps 9-13 and section 15), separate from signal generation. Checks for every new signal: event blackout ±60 min (step 11); daily −3R and weekly (Mon-Sun UTC) −6R halts on closed LIVE results; strategy (version × timeframe) suspended above 8R live drawdown; heat ≤ 3 open live positions, ≤ 1 per coin, ≤ 1 per direction in a group of correlated coins (1h returns over 720 candles, correlation ≥ 0.7, joined transitively); reward to TP1 ≥ 2R (step 9); no opposing liquidity pool / support-resistance level between entry and TP1 (step 10, a level within 0.05R of TP1 is the target itself); no duplicate while the same strategy / coin / timeframe is open or cooling down (step 13).
- **Sizing:** size = account × risk% ÷ |entry − stop|; risk% = config value capped at 1%, and at 0.5% until 30 days after the first live entry (no live entry yet = validating); leverage never above 3x - the position is made smaller instead (report says so). Size never depends on earlier results (tested); one position per coin rules out averaging down; stops only move towards profit (tested).
- **APPROVED signals** that fail a step are logged as the new state **NO_TRADE** (with the failed steps, never emailed). **Paper / validation signals** are logged in full; the new `risk_blocks` column records which steps would have blocked them live, so each rule can be measured later. Operator decisions (2026-09-24): calendar kept by hand in `config.yaml` → `events` (+ a "calendar not maintained" warning when nothing is listed for 7 days; no invented dates, no unofficial feed); paper not filtered; TP1 ≥ 2R as written - so the 8 older strategies (TP1 at 1R) cannot give live signals until a new version with TP1 ≥ 2R is tested; correlation ≥ 0.7; a suspended strategy resumes only via `risk.resume` ("id@version|tf": date - its drawdown then counts from that date).
- **Alerts:** `reports/risk_state.json` remembers halts / suspensions; each start and end is one `[SYSTEM]` email (`notify.py system`, never twice for the same run). The position book gets a "Risk:" line (halts, suspensions, risk %, next event, calendar warning); new report section **2d. Risk engine**. Shutdowns on data failure were already in place (section 3 / Phase 1).
- Config: new `risk:` and `events:` sections; `account.max_open_trades` is replaced by `risk.max_positions`.
- Tests: `tests/test_risk.py` (calendar parsing and blackout edges, day / week boundaries, suspension + resume, heat / coin / correlated / hedge, correlation groups, 2R and path edges, duplicates and cooldown, sizing caps, first live month, size independent of results, stops only move towards profit, one alert per change, offline end-to-end with a planted −3.5R day and an event 30 min ahead).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 12 — emails and chart images
- **Emails (AGENT_PROMPT.md section 20), written by the engine (no AI):** every email opens with the position book and ends with "Research signal. Not financial advice." Content is built during the scan (`engine/briefs.py`, `scanner.EmailContext`), `notify.py` only sends it.
  - `[ENTRY] LONG ETH/USDT | 15m | S6-OB-FVG v1.0 | R:R 2.4`, one email per APPROVED signal that passes the risk engine: UTC + Beijing time, data state, spot / futures only, regime 1W → 5m (4 regime timeframes + 30m/15m/5m structure), entry zone, stop, targets with the close % and stop moves, R:R, 5m confirmation bar, size after the risk engine, expiry (one candle after the scan), 3-5 reasons measured at the signal candle (trend, structure, momentum, volume, SMC context incl. liquidity taken, FVG / OB, premium / discount, session; flagged conditions as "Caution"), what cancels it (stop, exit rule, time stop, 5m rules, watch items), evidence (Layers B / C / A with sample sizes, paper and live record), chart. -5M strategies email at the 5m confirmation, not the trigger.
  - `[EXIT] ETH/USDT LONG | TP1 / TP2 / BE / TRAIL / SL / TIME / EXIT_RULE` for APPROVED positions: realised R, reason, next action, chart.
  - `[DAILY]` (new `notify.py daily`, workflow step): the first scan after 00:00 UTC (= 08:00 Beijing, before 06:00 UTC only, once per day): BTC context, signal-coin matrix (price, 24h volume, 1W/1D/4H/1H regime, 30m momentum, 15m setup state, 5m trigger state), position book, strategy status changes of the last 24h + halts / suspensions, event calendar.
  - `[SYSTEM]`: now also with the position book; new one-time reminder "a strategy is APPROVED while scans are still hourly".
  - `[WATCH]` digest only with the new setting `signals.email_watching: true` (default false).
- **Charts** (`engine/charts.py`, new dependency matplotlib): last 120 candles with entry / stop / targets / current stop and the entry / exit candle; email attachments only (`reports/charts/` is git-ignored).
- **Operator decisions (2026-09-24):** scans stay hourly until a strategy is APPROVED (one [SYSTEM] reminder then; switching is a one-line cron change); emails for entry, TP1 and close only - waiting-for-5m / expired / invalidated stay in the report (section 20: no noisy alerts for incomplete setups); `[WATCH]` off by default. The weekly email is Claude's Sunday task (Phase 14).
- Found while building: a signal found up to an hour late whose trade already ended in the same run would have produced an [ENTRY] and an [EXIT] email at once - such signals are no longer emailed (still logged); the expiry is now one candle after the scan.
- Tests: `tests/test_emails.py` (subjects and every body part, futures only, 5m bar, why-points only from facts up to the signal candle, evidence, daily layout, chart PNG, which state changes email, the late-signal rule, reminder, notify.py dry runs: one email per signal with its chart, book first, disclaimer last, never twice, daily once per day and only in the morning, watch only when enabled, no secrets = nothing sent and nothing marked).

## 2026-09-24 · Claude (BUILD mode, operator-approved plan) · Phase 13 — memory files
- **Every section 22 file exists** with a header (what, who writes it, format): new `lessons.md`, `research_sources.md`, `coin_notes.md`, `execution_notes.md`; `failure_journal.md` and `missed_trades.md` created up front. New index `memory/README.md`.
- **One record format for the knowledge files** (new `engine/memory.py`): a `###` title + one line with timestamp · source · evidence (a section 18 class first) · confidence · strategy · asset · timeframe · regime · review date. Used for new entries of the failure journal, missed trades, research sources, coin notes and execution notes; older entries stay as they are; the machine logs (lifecycle, universe, regime, experiments, smc_events, registry) keep their tables (operator decision).
- **Engine-written facts:** `research_sources.md` - one record per strategy version when first tested (back-fills the existing cards once): source, URL only from an optional card field `source_url` (never invented), claim, evidence class (SMC / ICT ideas incl. their -5M versions = CLAIM; older indicator strategies and control twins = HYPOTHESIS), derived hypothesis, limitations. `execution_notes.md` - data problems (DEGRADED / UNSAFE per coin and timeframe, cross-exchange deviations, failed downloads) when they start and end, and the fee settings (first run + every change). `coin_notes.md` - weekly (first scan on Sunday UTC) measured facts per signal coin: daily range, 1D regime shares over 90 days, correlated coins, 24h volume, strategies profitable on it (≥ min coin trades). `missed_trades.md` records now carry the 1H regime before the move. `lessons.md` - never written by the engine (reviews / operator only).
- **Append-only guard** (section 17): new `memory_guard.py` runs in both workflows before `git add`; any append-only file (`engine/memory.py` → `APPEND_ONLY`, incl. `reports/position_events.csv`) whose earlier lines changed or that was deleted stops the run - nothing is committed, the failure email goes out. Registry, signals log and the living definition files (`feature_notes.md`, `smc_research.md`) may change by design.
- **Reviews due:** review dates (config `memory.review_days`: lessons / coin notes 30, sources 90, failure journal / missed trades 7, execution notes 30); report section **3e. Memory** lists the files (size, records, newest) and the records whose review date has passed.
- Tests: `tests/test_memory.py` (record format and parsing, bad evidence class / unknown fields, headers never overwritten, due reviews, the guard in a real git repository incl. allowed in-place files, workflow order, every section 22 file known, each writer's records, start / end-only notes, fee change, Sunday-only coin notes, 90-day facts, sources back-filled once with no invented URLs, evidence classes).

## 2026-09-25 · Claude (BUILD mode, operator-approved plan) · Phase 14 — Claude daily / weekly tasks, weekly email, approval packs
- **Claude's scheduled tasks (§19), instructions in the new `tasks/` folder:** `briefing.md` (08:20 / 14:20 / 21:20 Beijing), `daily_review.md` (23:30 Beijing) and `weekly_research.md` (Sunday 10:00 Beijing), with shared rules in `COMMON.md`. Claude explains and researches. Every number comes from the engine: the new `brain_pack.py` prints the fact sheet (position book, market, signals, risk, closed results with LIVE / PAPER / VALIDATION kept apart, loss tags, lifecycle, missed moves, failing cells with their diagnosis, approval packs, reviews due, existing lessons) and the only file name the run may write.
- **Brain guard (new `engine/brain.py`, `brain_guard.py`, workflow `brain.yml`, every 15 min, always run from main):** tasks push to their own branch (`claude/brain-briefing`, `-daily`, `-weekly`), never to main.
  - Allowed: new files in `reports/claude/briefings|daily|weekly/` with the expected name, and section 22 records added at the end of 8 knowledge files.
  - Refused: code, config, `strategies.yaml`, workflows, engine files, edits or deletions of earlier lines, records without all fields, lessons without FACT / RESEARCH_FINDING / BACKTEST_EVIDENCE plus counts, and profit promises or trade win probabilities (§25).
  - One problem refuses the whole push, and one `[SYSTEM]` email says why. Additions are copied onto the newest main. `reports/claude/state.json` stops a push being applied twice.
  - New strategy versions arrive as pull requests for the operator (decision 2026-09-25).
- **Union merge for append-only files (new `.gitattributes`):** when the hourly scan, the research run and the Brain workflow append to the same memory file at the same time, git keeps both sides' lines instead of failing the push. `memory_guard.py` still checks that nothing earlier changed.
- **Approval packs and the operator's yes (§12, §21; new `engine/approval.py`, run by the daily research run):**
  - Eligible = PAPER_TRADING, ≥ 20 closed paper signals, paper average ≥ 0R, and at most 0.30R below the backtest on unseen data (`config.yaml` → `approval`).
  - Each eligible version × timeframe gets a pack in `reports/approval/`: definition and lineage, Layers A/B/C, walk-forward, paper, control twin, ±20%, cost stress, risk, failure attribution, limitations, and the exact line to copy.
  - **APPROVED is set only when the operator adds that line to `config.yaml` → `approvals:`.** Deleting the line returns it to PAPER_TRADING. An approval of a version that isn't eligible is not applied, with a warning.
  - **Gap closed:** there was no way to say yes before this.
  - The paper record of an approved version now continues with its live results, so the retirement limits (§12) keep applying after approval.
- **Emails:**
  - New `[WEEKLY]` (`notify.py weekly`, Sunday, first scan from 04:00 UTC, once per ISO week). It is built by the engine: results of the week (LIVE / PAPER / VALIDATION apart), scoreboard, lifecycle changes, loss tags and candidate lessons, SMC control-twin findings, missed moves, approval packs with the yes/no question, then Claude's weekly research if the file exists ("not available" otherwise).
  - New `[BRIEFING]` (`notify.py brain`, after the guard applies a briefing): the engine adds the position book and the disclaimer.
  - `[DAILY]` now shows the summary of yesterday's Claude daily review, marked as AI-written.
- **Operator decisions (2026-09-25):** new strategies from the research come as pull requests; briefings 3× daily with email; Claude creates the three Routines after the merge.
- Tests: `tests/test_brain.py`.
  - Guard: allowed names; never overwrite; append onto the newest main; edit, delete and prefix changes; lesson evidence; record fields; code, config, strategies and workflows; all-or-nothing; file limit; honesty phrases incl. allowed negations and macro odds.
  - End to end on a real git repository: apply once, idempotent, refusal leaves main unchanged, union merge keeps both sides.
  - Approval: settings, parsing, eligibility edges incl. exactly 0.30R, only the operator approves, removal, retired; the pack has every §21 part and its line parses back; stale packs removed.
  - Weekly: timing, stages kept apart, window, lifecycle blocks, every section, the Claude part or "not available".
  - Daily Claude summary; notify weekly-once, briefing and refusal emails once with one disclaimer; the fact sheet's file names match the guard and the weekly email.

## 2026-09-25 · Claude (BUILD mode, operator-approved plan) · Phase 15 — Pine Script export for TradingView
- **New `engine/pine.py`** turns a strategy card into a TradingView **Pine Script v6 strategy**, as a visual cross-check (§2 "Eyes"). It is deterministic (no AI) and TradingView never sends signals.
- **RULES mode:** used when every building block has an exact translation. The rules, ATR / structure stop, R-multiple targets, split, break-even and TP1 stop moves, time stop, exit rule and cooldown are all translated.
  - Every function call is hoisted into its own line, because Pine v6 evaluates `and` / `or` lazily and stateful functions must run on every candle.
  - Custom Pine functions copy the engine's exact formulas where TradingView's built-ins differ: EMA / RMA seeding, RSI, ATR, ADX, supertrend (TradingView uses the opposite sign) and percent rank.
  - The higher-timeframe trend uses the newest higher candle closed by the lower candle's close, as in `timeframes.align_higher`, with no look-ahead.
- **REPLAY mode:** used for SMC detectors, feature-engine columns and level targets, which have no exact translation. Re-writing them would create a second, different engine. Pine instead enters on the engine's embedded signals with the engine's stop and target prices, and TradingView manages the trades independently.
- **Engine entries** (newest 300 per coin, including stop and targets) are embedded as markers, with a matched / only engine / only Pine table.
- **Costs:** one commission per side (long taker fee + slippage), fills at the next open, 1% risk per trade (so the tester reads in R). The known differences are written in each script's header.
- **Output:**
  - APPROVED version × timeframe: exported automatically by the daily research run to `reports/pine/`, listed in research.json and the report.
  - Any card: `pine_export.py <id> <version> <tf>` (engine backtest on the newest candles of the signal coins), or the new manual workflow `pine.yml`. Its inputs go through env, never straight into the shell.
  - Approval packs explain how to look at the strategy on TradingView first.
- Backtest trades now keep all their target prices (`tps`), which REPLAY needs. Results and fingerprints are unchanged.
- **Operator decisions (2026-09-25):** a strategy script with the tester plus markers; APPROVED exported automatically, others by hand.
- Tests: `tests/test_pine.py`.
  - Translation of every block, defaults, hoisting, computed-once, and refusal by name.
  - Mode per card; the custom Pine functions pinned to the engine's formulas.
  - **Equivalence:** the translated tree evaluated with Pine semantics equals the engine bar by bar, for every rule of every RULES card on 3 synthetic coins and timeframes, plus 12 indicator values and the higher-timeframe trend with no look-ahead.
  - Every card × timeframe builds a structurally sound script; costs, plan, split, structure-stop width and embedded entries are checked; offline export end to end; workflow input safety.
  - TradingView's own compiler is not available offline: the operator's first paste is the final check.

## 2026-09-25 · Claude (BUILD mode, operator-approved plan) · Phase 16 (optional part: web dashboard only)
- **New web dashboard** (`engine/dashboard.py`, `build_dashboard.py`) at https://mayastraglobal-ui.github.io/crypto-signal-agent/. It is one self-contained HTML page: no external scripts, styles, fonts or images. Charts are inline SVG drawn by Python. It is readable on a phone and follows light / dark mode. The page is built by code only and shows the engine's numbers; it computes nothing new.
- **Sections:** position book (LIVE / PAPER labelled, day / week R vs limits, heat, closed today, a chart per open trade with entry / stop / TP1); market (BTC context, signal-coin matrix, a 1h chart of the last 5 days per coin); signals (LIVE / PAPER-VALIDATION / watching); strategies (BACKTEST and LIVE columns kept apart); approval packs and Pine scripts; risk (halts, suspensions, blackout, events, groups, limits); Claude's newest briefing and daily review, marked AI.
- **Stale warning in the browser:** the top bar turns red when the engine report is more than 2 hours old.
- **Safety:** all text from files is HTML-escaped. Claude's markdown gets a small safe renderer that only links http(s).
- **Publishing:**
  - The page goes to the branch `gh-pages` as one parentless commit (`publish_live.publish` gained branch / readme / title / strip). It is rebuilt after every hourly scan, after the daily research run, and after the Brain workflow applies Claude work. The Brain workflow never rebuilds it on its empty 15-minute checks.
  - Every dashboard step is continue-on-error, so it never stops a run.
  - The scan writes `reports/dashboard_data.json` (last 120 candles per signal coin and timeframe) to `live-reports` only.
  - Position book entries now also carry TP1, the managed timeframe and the start time.
- **Operator decisions (2026-09-25):** dashboard only (no database, no streaming); rebuilt after scan + research + briefing; charts = 7 coins on 1h + each open trade.
- **One-time operator step:** Settings → Pages → Deploy from a branch → gh-pages / (root).
- Tests: `tests/test_dashboard.py`. Built from a real offline scan: every section, a chart per coin, self-contained, only repository links, size, stale script. LIVE / PAPER labels are never mixed; everything is escaped (script / javascript: / img); Claude marked AI; approval and risk. Chart labels never overlap and levels stay inside the plot; flat and missing candles are handled; markdown. The build survives missing or broken files and picks the newest briefing. Publishing to gh-pages was tested in a real git repository: one commit at the root, main untouched. Workflow order and continue-on-error. Checked visually in headless Chromium at desktop width and 390 px phone width.

## 2026-09-25 · Claude (BUILD mode, operator request) · Event calendar, weekly calendar upkeep, workflow fixes, -5M review
- **New `events.yaml` (the event calendar, read together with `config.yaml` → `events`)** with the US high-impact releases through December 2026, in UTC:
  - PCE: 30 Sep, 29 Oct, 25 Nov, 23 Dec.
  - Jobs report (NFP): 2 Oct.
  - CPI: 14 Oct, 10 Nov, 10 Dec.
  - FOMC decisions: 28 Oct 18:00, 9 Dec 19:00.
  - US data at 8:30 a.m. New York = 12:30 UTC until 1 Nov, 13:30 UTC after it.
- **How the dates were checked:** the official pages (bls.gov, bea.gov, federalreserve.gov) are blocked by this environment's network, so every date was read through a web search restricted to that official site, and each entry says so (`check: official_search`).
  - CPI 10 Nov is `indirect`: the official regional CPI releases for October are dated 10 Nov.
  - CPI 10 Dec is `operator`: given by the operator, not confirmed.
  - **The November and December jobs reports are NOT listed:** their dates could not be confirmed, and none is invented. The weekly research flags the gap.
  - BLS also has a notice about revised dates after the 2025 **and 2026** lapses in appropriations: dates can move.
- **The weekly research keeps the calendar filled** (`tasks/weekly_research.md` step 4): the next 90 days, checked on the official calendars, converted to UTC, only appended.
  - The Brain guard accepts `events.yaml` **additions only**. Each new entry needs a valid UTC time, a known type, a name, an https source on an official site and a check mark, and must not be a duplicate. The result must still parse on the newest main. Edits and deletions stay the operator's.
  - The fact sheet shows the listed events and the missing NFP / CPI / PCE per month.
  - Candidates are now written as PROPOSED cards in the weekly file: the task session can only push its own branch.
- **brain.yml:**
  - "Save" no longer fails when `reports/claude` (or `reports/brain_sent.json`) does not exist yet; it adds only paths that exist.
  - pyyaml is installed for the guard.
- **All workflows:** `actions/checkout@v5` and `actions/setup-python@v6` (Node 24); `runs-on: ubuntu-24.04` pinned, because ubuntu-latest moves to Ubuntu 26 on 19 Oct 2026. `actions/cache@v4` (research) is unchanged.
- **-5M strategies with 0 research trades - finding** (first research run, 25 Sep): the 5-minute check is not the main cause.
  - Over the same 90 days of 5m history, the plain versions without the check made S5 15m 1, S5 30m 0, S6 0 and S7 1 trades. Over a full year of 15m history the plain versions made S5 4 / 6 (15m / 30m), S6 0 and S7 3 trades.
  - Most raw signals are blocked by the market gates. S5 15m: 51 signal candles, 34 blocked by regime, 11 by permission. S6: 6 signal candles, all blocked.
  - S6's combination (4H order block in discount + touch within 20 candles + a 15m CHoCH) almost never occurs.
  - **Conclusion:** 90 days is too short for any verdict (30 trades are needed), but a longer 5m history alone would not fix it (about 4 trades a year). The entry rules / gates are the bottleneck.
  - Nothing was changed. Rule changes are new versions, one change each, and need the operator's decision.
- Tests (test_brain.py):
  - calendar guard (applied, 13 refusals, fits the newest main, the committed calendar meets the rules);
  - calendar file (weekdays, 8:30 / 2:00 p.m. New York → UTC incl. the 1 Nov switch, FOMC dates, loader errors, scanner reads it, fact-sheet gaps);
  - workflows (pinned runner, Node 24 actions, the Save step in a real git repository with and without changes).

## 2026-09-25 · Claude (BUILD mode, operator request) · Phase 17 part A - close the learning loop
- **New `strategies_lab.yaml` (the strategy lab).** Claude's daily review and weekly research may now ADD strategy cards there, instead of writing "PROPOSED" cards into their reports.
  - The Brain guard (`engine/brain.py` `check_lab`, card rules in `engine/strategy_spec.py`) accepts additions only, and only from `claude/brain-daily` and `claude/brain-weekly`. It refuses the whole push unless every new card:
    - is FORMALIZED, a new id or a new version that changes exactly ONE thing vs the latest version (with a changelog line);
    - uses only the engine's building blocks. The rules are parsed, never run, during the check: only known column names, known functions, numbers and operators. No attribute access, indexing, text, powers or other code - the engine evaluates these rules. The lists are tested against the engine's real rule namespace;
    - has its first target >= 2R, a source, an evidence class and `added:` = today (UTC);
    - has a control twin (`twin_of` this id, without the ingredient) when its entry rules use SMC / ICT blocks, or it uses the 5m check;
    - keeps within 3 new cards per UTC day and 10 per 7 days (both tasks together; twins count).
  - Earlier cards can never be edited, even by an indented "addition". An addition must still fit the newest lab file on main.
  - brain.yml now installs requirements.txt (the guard uses the engine's card checker) and saves `strategies_lab.yaml`.
- **Lab cards in the engine:** `scanner.load_cards()` reads `strategies.yaml` + the lab. Lab cards are tested exactly like the library (same fees, gates, walk-forward, costs +50%, ±20%, control twin) and may reach BACKTESTING / VALIDATION / PAPER_TRADING automatically.
  - They are never APPROVED. `approval.decide(lab=True)` refuses an approvals line with a warning. The scan caps a lab cell at PAPER_TRADING, and the [ENTRY] email filter excludes lab plans (a second lock).
  - To approve one, the operator copies the card unchanged into `strategies.yaml` by pull request; the lab copy is then ignored and the results carry over (same id, version and fingerprint). Its approval pack says so first.
  - A broken lab file is reported ("not run") and never stops the library. Lab cards are marked 🧪 in the report.
- **Trials counter (`memory/trials.csv`, `engine/trials.py`):** one row per strategy version × timeframe the first time it is tested. The file is append-only and back-filled from the registry on the first run (46 cells today).
  - PAPER_TRADING now also needs the average trade's t-statistic >= z(1 - alpha / trials). This is Bonferroni, one-sided, with `research.trials_alpha: 0.05`. With 46 trials the bar is 3.07; it rises as more ideas are tested.
  - The bar is shown in the report (section 3b), the research cells (`t_stat`, `need_t`), the fact sheets and the [WEEKLY] email ("Trials counter").
  - This bar is added on top of every earlier test; nothing was loosened. Fees, risk limits, gates and the other pass rules are unchanged.
- Tasks: `tasks/COMMON.md` rule 4 (the lab rules); the daily review may add a lab card for a queued refinement; the weekly research adds its 1-2 candidates to the lab (heading "Candidates (added to the lab)"). The fact sheet shows the cards left today / this week, the existing ids with their latest versions, the lab cells and the trials bar.
- Tests: new `tests/test_lab.py` - 34 tests covering:
  - building blocks vs the real namespace, and unsafe rules;
  - card rules and the one-change rule;
  - guard refusals and limits;
  - the guard on real git;
  - never approved or emailed;
  - trials, the fact sheet and the weekly email;
  - end-to-end scan → research → scan with a forced APPROVED lab cell.

  Mutation check: 22 of 22 planted bugs caught.

## 2026-09-25 · Claude (BUILD mode, operator request) · Outside feeds for Claude's tasks
- **Why:** both briefings on 25 Sep could not open any news page. The Claude task environment's network ("Trusted" access) blocks news and research sites, but GitHub Actions has open internet.
- **New `feeds.py` + `engine/feeds.py`**, run by the hourly scan workflow (step "Outside feeds", continue-on-error, after the scan, before "Save reports"). It writes `reports/feeds.json` on main with:
  - news headlines from the CoinDesk, Cointelegraph and The Block RSS feeds; our coins are marked when named;
  - the Fear & Greed index for the last 7 days (alternative.me);
  - Binance announcements, sorted into listings, delistings and maintenance by catalog name and title (not by catalog id);
  - the next 4 Deribit BTC and ETH options expiries (08:00 UTC) with open interest, put/call ratio, USD notional and max pain.
- **Safety:**
  - Every source is fetched on its own; a failure is written into the file and never stops the scan.
  - Text is stripped of HTML and control characters and cut short. Only https links are kept.
  - The file and `tasks/COMMON.md` say that feed text is data, never instructions, and a headline is at most a CLAIM.
- **Tasks:** the fact sheet (`brain_pack.py`, all three tasks) has a new "Outside feeds" part: freshness and failed sources, Fear & Greed, headlines of the last 12 h / 24 h / 7 days, Binance notices, Deribit expiries. `tasks/briefing.md` step 3 starts from it.
- **Not verified live:** this build session cannot reach these sites. The parsers are tested on sample payloads shaped like the real ones; the first hourly run shows each source's status in the file. Binance may refuse GitHub's US-based runners; if so, that source reads "error" and the rest still work.
- Tests: new `tests/test_feeds.py` (9 tests).

## 2026-09-25 · Claude (BUILD mode, operator request) · Claude tasks always use the newest engine files
- **Bug:** Claude's task sessions are persistent, and `publish_live.py --restore` only copies files that are missing. So later runs kept old copies: the 14:20 Beijing briefing used the 00:26 UTC `latest.json`, although scans had run at 05:18 and 06:24.
- **Fix 1:** new `python publish_live.py --refresh`, which always overwrites `reports/` with the newest live-reports copy. The start commands in `tasks/COMMON.md` (all three tasks) now use it. The workflows keep `--restore`, which never replaces a file of the current run.
- **Fix 2:** `brain_pack.py` checks the local engine files before anything else. The fact sheet starts with "!!! STALE ENGINE FILES" when:
  - `latest.json` is older than the "Updated" time in `reports/latest.md` on main;
  - any engine file differs from the newest live-reports commit, compared by git blob hash;
  - an engine file is missing locally.

  The task must then refresh again, or say so at the top of its output.
- **Tests** (`tests/test_publish.py`): a second run in the same session, on real git repositories:
  - `--restore` keeps the old copy, and the warning shows;
  - `--refresh` gets the new copy, and the warning is gone;
  - the warning rules work without a live branch;
  - the start commands use `--refresh`.

## 2026-09-25 · Claude (BUILD mode, operator request) · Phase 17 part B - edge, mechanics, playbook, curriculum
- The operator's Part B text was not in this session: only the four names. I built the reading I proposed on 25 Sep. Any part can be changed in review.
- **Edge block** (`engine/strategy_spec.py`): `edge: {who_pays, mechanism, fails_when, kill_rule}` on a card.
  - It is a hypothesis, not proof, and it is not one of the rule keys, so the fingerprints are unchanged and no version change is needed.
  - Written for all 16 non-twin library cards. The -5M cards say why the 5m check should help. Every kill rule names the engine's retirement rules and, for SMC cards, beating the control twin.
  - Required on lab cards: the Brain guard refuses a card without all four lines (at least 20 characters each). Control twins are exempt.
  - The approval pack shows the edge in section 1, before the numbers, or "NOT WRITTEN". The fact sheet lists the edges of VALIDATION / PAPER / APPROVED and lab cards, and names the cards that have none.
- **`memory/market_mechanics.md`** (new knowledge file, append-only, union merge; tasks may add records): 10 records seeded by the build session.
  - They cover funding, liquidations, open interest, Deribit expiries, stop clusters, sessions, macro releases, listings, fees in R, and ETF / stablecoin flows.
  - No source could be opened from this session, so general knowledge is labelled `CLAIM` (unsourced). Only what the engine itself measures or enforces is labelled `FACT`.
  - The weekly research must confirm or reject one CLAIM a week with a real source (new step 5).
- **`memory/playbook.md`** (`engine/playbook.py`): rewritten by every daily research run, and also stored in `research.json` → `playbook`. It is built from backtest trades split by the regime at entry.
  - For each regime it lists the families (trade-weighted average R), the cells that made money (30+ trades, at least +0.01R), the cells that lost money (at most -0.10R), and what "no trade" looks like.
  - It says "NOTHING made money - standing aside IS the playbook" when that is the measured truth.
  - The first version is written from the 25 Sep research run. It currently shows no tested strategy making money in RANGE, HIGH_VOL_RANGE or COMPRESSION.
  - The fact sheet shows the playbook for the regimes the signal coins are in right now, and the briefing's regime section uses it. Claude's tasks cannot write it.
- **`memory/curriculum.md`** (`engine/curriculum.py`): 14 beginner lessons. Each [DAILY] email carries the next one, remembered in `reports/curriculum_sent.json`; the course starts again after the last lesson. A broken lesson file never stops the daily email.
- Tests: new `tests/test_knowledge.py` (16 tests). `tests/test_lab.py` end-to-end now also checks the offline playbook. Mutation check: 12 of 12 planted bugs caught.

## 2026-09-25 · Claude (BUILD mode, operator request) · Phase 17 part B corrections (the operator's full plan)
- The operator pasted the full Phase 17 plan. Part B had been built from the four names only, and three things differed. They are corrected here:
- **Edge block:**
  - It now also needs `type` (behavioural / forced_flow / risk_premium / structural) and `works_in` (the regimes it should work in; a subset of the card's regimes).
  - Added to all 16 library edge blocks. `works_in` = the card's regimes. Rules and fingerprints are unchanged.
- **market_mechanics.md:**
  - New records must name the mechanism and the strategies that use it, as detail lines `- mechanism:` and `- strategies:`; the Brain guard checks this.
  - The first 10 records are append-only, so they are not edited. A new "Index" record maps each of them to its mechanism and the strategies that use it.
- **playbook.md:**
  - It now starts with the table the plan asks for: strategy family × timeframe × BULL / BEAR / RANGE / TRANSITION, with average R and trade count, ✓ for made money and ✗ for lost money.
  - It is rewritten weekly (the Sunday research run, or when the file is missing); the per-regime detail follows.
- **curriculum.md is now the agent's rotating reading plan** (24 items: 10 papers, 4 books via public summaries, 3 exchange / data-provider research topics, 5 blow-up post-mortems, 2 interviews).
  - The daily review studies one item a day (new step 6). The fact sheet names today's item: the first not studied yet, then the one studied longest ago, tracked through `[Cxx]` record titles in research_sources.md.
  - For each item the review writes one research_sources record and at most one hypothesis.
  - References are from the build session's memory, are marked as not opened, and contain no URLs; the task checks them on the real source before citing.
- The beginner lessons for the operator moved to `memory/beginner_course.md` and still come with the [DAILY] email.
- Tests: test_knowledge.py now has 21 tests (reading plan, rotation, mechanics rule, edge type / works_in, playbook matrix).

## 2026-09-25 · Claude (BUILD mode, operator request) · Phase 17 part C - futures data, real funding costs, idea factories
- **Futures data recorded every hour** (new `derivs.py` + `engine/derivs.py`), in the scan workflow before the scan, with continue-on-error.
  - What: funding rate history, and hourly open interest (USD), long/short account ratio and taker buy/sell ratio, for every signal and research coin.
  - Sources: Binance USDT-M futures API first, the OKX public API when Binance refuses (US servers). Older days are back-filled from data.binance.vision daily metrics and monthly funding files, 4 days per coin per run, up to 365 days (`config.yaml` → `derivs`).
  - Storage: the history is appended to `reports/derivs_hourly.csv.gz` and `reports/funding.csv.gz` on the live-reports branch, carried over every run. History is never shrunk or replaced: an unreadable file stops the step instead.
  - Data checks per coin: freshness (> 3 h = STALE), gaps in 7 days, impossible values (ignored), mixed sources. They are shown in `reports/derivs_quality.json` and report section 0b.
  - Not verified live: this session cannot reach the exchanges. The parsers are tested on sample payloads; the first hourly run shows each coin's source and errors.
- **New building blocks**, each value as KNOWN at the candle close (an hourly row counts from the end of its hour; unknown or too old = NaN, so the rule is false): `funding_rate`, `funding_z(n)`, `oi`, `oi_chg(n)`, `ls_ratio`, `taker_ratio`, and `btc_ret(n)` (BTC's return on the same timeframe; only the same closed candle is used).
- **Real funding in short costs:** where the funding history is known, a short pays max(config 0.01% per 8 h, the real rate it would have paid) × `funding_real_x` (1.0; the costs +50% test makes it 1.5). Funding received is never counted, so backtest costs only go up.
- **Six idea factories** (`engine/ideas.py`, `strategy_spec.factory_problems`):
  - Every lab card names its `factory` and `factory_evidence`. The Brain guard checks each factory's evidence:
    - literature: needs a source_url;
    - failure: needs a loss tag and n >= 30 losing trades;
    - missed_move: needs the move's date;
    - market_structure: must use a futures block;
    - lead_lag: must use btc_ret.
  - Each factory has a weekly quota (`config.yaml` → `lab.factory_quota`: 2 / 3 / 2 / 2 / 3 / 1).
  - variant_search is reserved for the engine. The engine's variant cards do not use up Claude's 3-a-day / 10-a-week limits.
- **Engine variant search (factory e):** the research run appends up to 3 cards per 7 days to strategies_lab.yaml. Each is a one-change variant of the strongest BACKTESTING cells (30+ trades, best unseen-data average first).
  - The variants tried: 2R/3R targets when the first target is below 2R, dropping regimes that lost (-0.10R or worse over 30+ trades), an ADX or relative-volume filter, or a neighbouring timeframe.
  - Every variant passes the same card checks, is tested like any card, and is counted in trials.csv.
  - SMC / 5m parents and control twins are skipped, because a variant of them would need its own twin.
  - research.yml now commits strategies_lab.yaml; `.gitattributes` union-merges it.
- **Lead-lag measurement (factory f):** per alt, the correlation of its 1h return with BTC's return 1-3 hours earlier, marked "clear" when |corr| > 2/sqrt(n). It is shown in the fact sheet.
- **Pass rate per factory:** lab cards → strategy/timeframe cells that reached VALIDATION or better. Shown in `research.json`, the [WEEKLY] email and the fact sheet, along with the quota left per factory.
- Tests: new `tests/test_ideas.py` (20 tests). They cover the parsers (Binance, OKX, data.binance.vision), the history merge and source preference, the data checks, no look-ahead, the building blocks, real funding never below the config rate, factory evidence and quotas, variant search, lead-lag, pass rates, and the recorder end to end with fallback, back-fill and history protection. Mutation check: 11 of 12 planted bugs caught; the survivor is a redundant second lock.

## 2026-09-25 · Claude (BUILD mode, operator request) · Phase 17 part D - the agent's report card, monthly clean-up
- **Weekly agent report card** (`engine/report_card.py`) in the [WEEKLY] email, just before Claude's weekly research, and in the weekly research's fact sheet. It is measured from the engine's own files, so it is complete even if Claude did not run. It has 11 items:
  1. ideas researched (new research_sources records, lab cards by factory);
  2. lab cells tested for the first time (trials.csv);
  3. pass rate per factory;
  4. days from a card's `added` date to its first test (median, longest, cards still waiting);
  5. paper vs backtest-unseen gap for cells with 5+ closed paper signals;
  6. late signals (expired before entry, or tagged late_entry) and false signals (lost without ever reaching +0.25R), per stage;
  7. missed moves by verdict;
  8. news-feed sources failing now, plus the pages Claude listed as not opened;
  9. Claude task runs delivered vs expected (21 briefings / 7 daily / 1 weekly), median run time from each output's run log, reported problems (usage limit ...), and pushes refused by the guard;
  10. lab slots used vs allowed per factory;
  11. ONE process improvement from the weekly research's `## Process improvement` section - a proposal; the operator decides.
- `tasks/COMMON.md`: every output ends with `## Pages that failed to open` and `## Run log` (start / finish time, problems). The weekly research writes one `## Process improvement` from the report card.
- `brain_guard.py` appends every push it handles to `reports/claude/runs.csv` (append-only, union merge).
- **Monthly clean-up** (`engine/cleanup.py`) runs in the research run on the 1st (`--cleanup` forces it). It only adds; nothing is deleted.
  - Versions FAILED or RETIRED on every tested timeframe for 30+ days are appended to `memory/retired_cards.csv`. They are no longer re-tested (they show as "RETIRED (monthly clean-up)"), but the cards stay in their files; deleting the line brings one back.
  - Possible duplicate lessons (title word overlap >= 0.6, pairs not already merged) and re-checks of lessons 30+ days old (is their loss tag still systematic in 2+ of today's tests?) go into `memory/cleanup_log.md` (append-only).
  - The engine never writes lessons (section 17.7). In the first 3 days of the month the daily review's fact sheet lists that work, and the review writes one `Merged:` / `Re-check:` record each (new step 7).
- Tests: new `tests/test_report_card.py` (12 tests). Mutation check: 10 of 10 planted bugs caught.

## 2026-09-25 · Claude (BUILD mode, operator correction) · Phase 17 C fix - one futures-data series per source
- **Problem (found by the operator):** the history merged Binance files and OKX rows into one line per coin and hour. Their open-interest and long/short levels are not comparable, so building blocks could jump at the boundary: a fake open-interest change, or a z-score mixing two exchanges.
- **Fix:**
  - The history keeps **one series per source**: rows are unique per coin, source and time, and are never merged across sources.
  - **OKX is the main series** (`engine/derivs.MAIN_SOURCE`). `oi`, `oi_chg`, `ls_ratio`, `taker_ratio`, `funding_rate` and `funding_z` read only it, in backtests and live alike. Binance (API + data.binance.vision files) is recorded as a separate research series; it never stands in for missing OKX data (missing = unknown).
  - The recorder fetches OKX and Binance independently each hour; a Binance failure no longer changes the source of anything.
- **Guard:** `align()` returns each candle's source code. `oi_chg(n)` returns unknown when the two compared values come from different sources, and `funding_z(n)` when its window holds more than one source.
- **Quality:** a main series holding more than one source is **DEGRADED**, never GOOD. Research rows are only counted (`research_rows`). A coin with Binance data but no OKX data is MISSING, not GOOD.
- **Costs** are not a building block: a short still pays the HIGHEST real funding any recorded exchange charged, and never less than the config rate.
- Tests (test_ideas.py, 24 tests), including the boundary jump: OKX history, then Binance files at twice the level.
  - The main series never shows the Binance level, and `oi_chg` never shows the fake +100%.
  - A series forced to hold both sources gives unknown at the boundary and measured changes on both sides.
  - It is DEGRADED, and costs take the highest real funding.
  - Mutation check: 6 of 6 planted bugs caught.

## 2026-09-25 · Claude (BUILD mode) · Phase 18 A - a research brain that learns by itself (R1, R2, R8)
- **Sources opened first** (records `[R1]`, `[R2]`, `[R8]` in `memory/research_sources.md`, with the commit read, what we take, what we do NOT take and the licence): Microsoft RD-Agent (MIT), TradingAgents (Apache-2.0), Microsoft Qlib (MIT). Only the repositories were read; the two arXiv papers could not be opened from the build environment and are not cited. No code was copied.
- **Research loop (R1):**
  - lab cards must name `parent: "<kind>: <reference>"` (result, card, lesson, failure, missed_move, experiment, source). `strategy_spec.parent_problems` checks the format and that a named card exists; the Brain guard checks that a named record exists on main or in the same push. Control twins and `strategies.yaml` cards need none. The engine's variant-search cards name `result: <parent cell>`.
  - `engine/research_loop.py`: `Feedback: <id>@<version>` records in `memory/experiments.md` need parent / hypothesis / result (with numbers) / teaches / next (the next hypothesis or "stop this line"); the guard enforces it. A card is due for feedback once tested, and again when a cell changes status after the last feedback. Idea chains follow `result:` / `card:` parents between lab cards.
  - The daily fact sheet lists the results waiting for feedback and the chains; the weekly fact sheet and the [WEEKLY] email show the chains ("IDEA CHAINS"; a failure never stops the email). `tasks/daily_review.md` step 5b, `weekly_research.md` and COMMON.md rule 4 explain it.
  - The engine's experiments table starts a new header when review records came after it (the table stays readable; nothing is edited).
- **Bull vs bear (R2):** `engine/debate.py`. Bull and Bear cases hold only engine numbers (backtest, unseen part, walk-forward, costs +50%, ±20%, coins, control twin, paper, drawdown, loss tags, overfit flags, regime matrix); an empty side says so. The risk manager VETOES on: event within the blackout window, heat full, regime against (a signal's direction, or no signal coin in a strategy's regimes on its timeframe), data not GOOD / report stale or missing, day or week result at 75% of its limit or a halt. It only ever says "not now". Approval packs get section 0 (the research run fetches the newest hourly report for it); the weekly email and fact sheets repeat the risk line; the briefing fact sheet gives the cases per signal coin and per signal; the guard refuses a briefing without `## Bull vs bear` and its three lines.
- **Curriculum:** R1-R8 added to `memory/curriculum.md` as a weekly list (the daily C-list is unchanged); the weekly fact sheet names the next project, `weekly_research.md` step 4b studies it.
- No fee, risk or gate was changed; APPROVED stays operator-only; live [ENTRY] emails are unchanged.
- Tests: new `tests/test_learn.py` (22 tests); lab and brain fixtures updated with `parent` and the briefing section. Mutation check: 17 of 17 planted bugs caught.

## 2026-09-25 · Claude (BUILD mode) · Phase 18 B - stronger tests, so a "winning" strategy is really winning (R3, R5)
- **Sources opened first** (records `[R3]`, `[R5]` in `memory/research_sources.md`): freqtrade's lookahead-analysis and recursive-analysis docs (GPL-3.0 - ideas only) and Jesse's Monte Carlo and rule-significance docs (MIT). No code was copied. Jesse's own "rule significance" is a next-bar bootstrap p-value; we follow the operator's plan instead (one entry rule removed at a time) and say so in the record.
- **Lookahead + recursive check** (`engine/bias.py`, run by research.py on the first research coin):
  - lookahead: the history is cut right after 6 signal candles (`research.bias_check.lookahead_cuts`) on every timeframe and recomputed; every single entry / exit rule and every stop / target level must give EXACTLY the same answer on all shared candles;
  - recursive: every trade timeframe starts 500 candles later; after 1000 settling candles at most 0.1% of the candles may differ.
  - A card that fails is BIASED: FAILED on every timeframe of that version, for good (sticky through the registry column `bias`, even if a later check misses it). Cells whose card was not checked cannot reach PAPER_TRADING.
  - On synthetic data every library card passes; planted bugs (the close 2 candles later; a running candle count) are caught as lookahead and recursive respectively. Note: SMC sweep levels remember old swings, so with only 3000 candles the S8 level flips on ~1% of candles - with real history (1000 settling candles, tens of thousands compared) it stays far below the 0.1% tolerance.
- **Monte Carlo** (`engine/research.monte_carlo`): 1000 deterministic shuffles of each cell's trades -> drawdown as it happened, median, 95% worst; longest losing streak as it happened, median, 95% level. PAPER_TRADING also needs the 95% worst drawdown <= `research.monte_carlo_max_dd_r` (8R; the engine uses the lower of it and `risk.strategy_max_dd_r`). Registry columns `mc_dd95_r`, `mc_streak95`. Approval packs: section 8 shows the expected worst losing streak; the Bear case repeats it.
- **Rule significance** (`strategy_spec.rule_drops`, `research.rule_significance`): each card re-tested with ONE entry rule removed (from the long and short lists; a one-rule side keeps it; a parameter only that rule used goes with it). A rule "adds nothing" when the card without it has 30+ trades and an average trade at least as good. Approval packs list each rule's verdict (section 6b); registry column `rules_adding_nothing`. `ideas.simpler_cards` queues the simpler card in the lab (engine card, factory `variant_search`, `parent: result: <cell>`) before the other variants, within the same weekly quota; cells FAILED / BIASED are only reported; when a simpler card cannot be queued (e.g. the parent's first target is below 2R) the reason is recorded.
- **Duration:** the report shows the research run's duration against `research.time_budget_min` (90); after 60% of the budget the rule test is skipped for the remaining coins. Offline: bias check ~15 s; at full history size ~2.5 min; the rule test adds ~20%.
- New config keys (operator-owned): `research.monte_carlo_runs`, `monte_carlo_max_dd_r`, `bias_check`, `time_budget_min`. No fee, risk or gate was loosened; APPROVED stays operator-only; live [ENTRY] emails are unchanged.
- Tests: new `tests/test_robust.py` (20 tests, including an offline research run with a planted lookahead card); 506 tests pass. Mutation check: 20 of 20 planted bugs caught.

## 2026-09-25 · Claude (BUILD mode) · Phase 18 C - more strategy ideas and tools (R4)
- **Source opened first** (record `[R4]` in `memory/research_sources.md`): freqtrade-strategies at commit f3340ce - the entry / exit logic of about 25 strategy files. GPL-3.0: ideas only, no code copied.
- **10 R4 ideas, queued** (`Queue: R4-...` records in `memory/experiments.md`, full cards in YAML): BbandRsi, ClucMay72018, hlhb, AwesomeMacd, VolatilitySystem, TrendFollowingStrategy, Supertrend, Strategy001, AdxSmas, Simple. Each card names its file (`source`, `source_url`), how it differs from the file (`factory_evidence`: mirror-image shorts, our ATR stop, a first target of 2R instead of the file's ROI table, the engine's regime gates, approximations such as the Heikin-Ashi close), an edge block, `parent: source: [R4] freqtrade-strategies`, factory `literature`. None has an SMC / 5m ingredient, so none needs a control twin. Left out on purpose: ideas needing indicators we do not have (CCI, MFI, CMF, Fisher RSI, TEMA, candle-pattern libraries) and the repository's own lookahead_bias examples.
- **Spread over the weeks** (`engine/idea_queue.py`): the weekly fact sheet shows the next queued card(s) ready to paste, within the card's factory quota (literature: 2 a week) and the lab limits - about 5 weeks for all 10. `tasks/weekly_research.md` step 3 adds them first; the Brain guard refuses a queued card whose copy differs (only `added` may be set).
- **New building blocks** (all closed-candle only; `strategy_spec.COLUMNS` / `FUNCTIONS`; strategies.yaml header):
  - Fibonacci retracements of the last confirmed swing leg (`fib_382/500/618/786`, `fib_dir`);
  - anchored VWAP from the daily open (`avwap_day`) and from the last confirmed swing low / high (`avwap_swing_low/high`), summed per anchor window so it does not depend on where history starts;
  - volume profile of the last n candles (`vp_poc(n)`, `vp_vah(n)`, `vp_val(n)`: 24 bins, value area = the fewest fullest bins holding 70% of the volume);
  - Ichimoku 9 / 26 / 52 (`ichi_tenkan`, `ichi_kijun`, `ichi_span_a/b`, `ichi_cloud_top/bottom`, the cloud as known at the candle). The chikou span is left out: in a backtest it is lookahead.
- Tests: new `tests/test_pros.py` (14 tests: exact values, the same values with later candles removed, settling when history starts later, a plain-loop check of the volume profile; the 10 queued cards pass every lab rule, fire on synthetic data and pass the Phase 18 B lookahead / recursive check; queue copy rules and the fact sheet quota). 520 tests pass. Mutation check: 14 of 14 planted bugs caught.
- No fee, risk or gate was changed; APPROVED stays operator-only; live [ENTRY] emails are unchanged.

## 2026-09-25 · Claude (BUILD mode) · Phase 18 D - see it on the chart (R6, R7)
- **Sources opened first** (records `[R6]`, `[R7]` in `memory/research_sources.md`): backtesting.py's plotting code (AGPL-3.0 - the layout idea only, no code) and TradingView Lightweight Charts 5.2.1 (Apache-2.0; npm integrity checked; README licence / attribution section; NOTICE).
- **Backtest chart page** (`engine/btcharts.py`, published as `chart.html`): pick a strategy × timeframe and a coin; the newest 1500 candles with buy / sell arrows and exit dots (won / lost), the chosen trade's entry, stop and targets as price lines (◀ ▶ through every trade; a trade older than the candles shown is said to be), the equity curve and the drawdown below. BACKTEST is labelled on the page.
- **Library bundled** in `vendor/lightweight-charts/` (the unchanged standalone production file, LICENSE, NOTICE, README with version, npm integrity and file sha256) and published with the page; nothing is loaded from outside; the page shows the notice with a link to tradingview.com and keeps the attribution logo on.
- **Data**: the research run writes `reports/backtest_charts/` (gitignored): `index.json`, one candle file per coin × timeframe, one trade file per cell × coin (the same trades as the research; equity and drawdown over all of them). `build_dashboard.py` copies it into the site and publishes it; runs without their own chart data (hourly scan, Claude tasks) list the published copy's files so `publish()` keeps them.
- **Links**: dashboard strategy table ("chart") and approval cards (chart + Pine script); every approval pack starts with "Check the trades before you say yes" - the chart page and the Pine script, now exported for every eligible cell (`reports/pine/`); [ENTRY] and [EXIT] emails keep their chart image and add one last line "Backtest chart of this strategy: <link>". Paper signals are not emailed (unchanged), so there is no paper email to extend.
- New `config.yaml` key `dashboard.url` (null = GitHub Pages of the repository).
- Tests: new `tests/test_charts.py` (13 tests, including the page drawn in headless Chromium when available - skipped on CI - and an offline research run); `test_dashboard` / `test_learn` updated. Mutation check: 15 of 15 planted bugs caught.
- No fee, risk or gate was changed; APPROVED stays operator-only.

## 2026-09-25 · Claude (BUILD mode) · Email redesign - short, clean, readable in 30 seconds on a phone
- Every email is an HTML card (600 px, table layout, inline CSS, no external fonts / scripts; the chart image only on signal emails) plus a plain-text copy built from the same blocks (`engine/mailkit.py`). No markdown symbols. Subjects under 70 characters. Missing numbers show "–".
- Six templates (`engine/emails.py`): ENTRY SIGNAL, TRADE UPDATE (TP1 / target / stop / time exit / exit rule / cancelled - cancelled is new), ACTION NEEDED + FIXED, BRIEFING, DAILY REVIEW, WEEKLY REPORT (+ RISK NOTICE / reminders / WATCH in the same frame). The numbers come from the engine files (`engine/mailfacts.py`).
- Workflow failures: one failure is retried silently; the 2nd in a row sends one ACTION NEEDED email (notify.py reads the earlier runs via the GitHub API, `actions: read`); the first success after 2+ failures sends one FIXED email.
- Research run: `counts` in research.json and one line per day in `reports/research_counts.json` (backtests per coin, strategies, tests, coins, new lab cards) for the daily and weekly emails.
- Claude's reports get a `## Email summary` block (headline, sub, do, dont / lesson, tomorrow / next, improvement) that the Brain guard checks (`engine/summary.py`); every report becomes a page on the dashboard (`engine/mdpage.py`), linked from the email. The morning [DAILY] email is replaced by the 08:20 BRIEFING and the 23:30 DAILY REVIEW, each with an engine-only fallback if Claude's report does not arrive. The beginner lesson becomes a page linked from the DAILY REVIEW.
- Unchanged: signals, fees, risk limits, gates, approvals and the send-once rules.
## 2026-09-26 · Claude (BUILD mode) · Fix: false BIASED alarm on every htf_up / htf_down card (bias check v2)
- The first real research run with the Phase 18 B checks (2026-09-26 00:40 UTC) called 5 cards BIASED (bb_squeeze_breakout, donchian_breakout, macd_trend_cross, supertrend_flip, trend_pullback), all for the same reason: "recursive on 1h: htf_up / htf_down (489 of 78216 candles differ, first 2017-10-18)".
- Cause: a false alarm in the check, not in the cards. The recursive run starts every trade timeframe 500 of ITS OWN candles later, so the 4h input of htf_up on 1h starts 2000 hours later, and after 1000 settling 1h candles the 4h trend (EMA 20/50) had not settled yet. On real history the 1h and 4h candles cover the same years; the synthetic test data did not (and 4h was not a trade timeframe in the test), so the tests missed it.
- Fix (`engine/bias.py` check v2): a timeframe is compared only after its own candles AND every longer timeframe's candles have settled (`settled_from`). A test reproduces the real case (1h + 4h over the same 500 days): check v1 flags the htf_up cards, check v2 does not; the planted lookahead and running-count bugs are still caught.
- Stored findings carry their check version (`... (check v2)`); a finding of an older check (v1) no longer keeps a card FAILED for good - the next run checks the card again, and a real bias is found again and stored as v2. Nothing else changes: gates, fees and risk limits are the same.
- Operator follow-up (same day): recursive differences that die out early (none in the later half of the compared history) are now a **warm-up warning**, never BIASED (section 3b shows them as "⚠ warm-up only"); lookahead differences and differences that persist stay BIASED. A plain EMA-based higher-timeframe filter card (htf_up + close > ema(close,50)) is in the test and must pass. The operator approved clearing the 5 cards' BIASED flags: they were written by check v1, so the next research run ignores them and checks the cards again.

## 2026-09-26 · Claude (BUILD mode) · Fix: the risk manager's data check uses only the signal coins
- The whole-market line (briefing fact sheet) and the approval packs' risk manager counted every coin in the data-quality report, including candidate coins the universe only watches (e.g. BABY, VTHO), so one bad candidate vetoed everything. Now: the data check looks at the system state plus the signal coins (or, for one signal, that coin only). Candidates are still checked by the universe step and are never traded.
