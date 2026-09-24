"""
Failure attribution (AGENT_PROMPT.md section 17) - WHY trades lose, measured by fixed rules.

- context():   what the market looked like at every candle (for the conditions at entry)
- tag_trade(): the section 17 reason tags of one trade. Conditions at entry are measured for EVERY trade
               (winners too), so a tag only counts when it is more common among losers than winners.
- summarize(): per strategy x timeframe - tag table (losers vs winners), MAE / MFE, results by regime,
               session and direction, and the 8 questions of section 17.3 answered from the numbers.
- strong_moves() / missed-move helpers: section 17.4 missed-trade learning.

Not measurable yet (and said so, never guessed): news_event, overtrading (need the event calendar and
risk engine, Phase 11), fvg_ignored (needs per-trade gap tracking).
Pure functions only: no internet, no files.
"""
import numpy as np
import pandas as pd

from engine import features as fe
from engine import regime as rg
from engine import smc

DEFAULTS = dict(
    range_adx=20,              # range_market: ADX(14) on the trade's own timeframe below this
    low_rel_vol=0.8,           # low_relative_volume: signal-candle volume below 0.8x normal
    overextended_atr=2.0,      # overextended_entry: close >= 2 ATR beyond EMA20 in the trade direction ...
    overextended_rsi=75,       # ... or RSI(14) >= 75 (long) / <= 25 (short)
    late_move_atr=3.0,         # late_entry: price already moved >= 3 ATR the trade's way ...
    late_move_bars=10,         # ... over the 10 candles before the signal
    displacement_bars=3,       # no_displacement: no strong candle in the trade direction in the last 3
    wide_stop_atr=2.5,         # stop_too_wide: stop wider than 2.5 ATR
    bad_target_share=0.8,      # bad_target: reached 80% of the way to TP1 but never hit it
    false_breakout_bars=5,     # false_breakout: closed back inside within 5 candles
    spike_atr=3.0,             # volatility_spike: a candle >= 3 ATR big during the trade
    lag_mfe_r=0.25,            # indicator_lag: the trade never got past +0.25R
    main_sessions=["London", "NY AM", "Silver Bullet"],   # wrong_session: intraday entry outside these
    min_losses=30,             # a tag can only be called systematic with >= 30 losing trades
    frequent_share=0.25,       # loser-only tags: 'frequent' when in >= 25% of losses
    strong_move_atr=5.0,       # missed moves: >= 5x the 1H ATR ...
    strong_move_bars=12,       # ... within 12 hours
    missed_lookback_hours=24,  # ... in the last 24 hours
    signal_window_bars=3,      # a signal counts if it came up to 3 hours before the move started
)
CONDITIONS = ["range_market", "htf_conflict", "low_relative_volume", "overextended_entry", "late_entry",
              "no_displacement", "wrong_session", "data_issue"]
PATH_TAGS = ["stop_too_wide", "false_breakout", "trend_reversal", "regime_mismatch", "volatility_spike",
             "ob_failed"]                                      # measured for winners too
LOSER_TAGS = ["fees_slippage", "funding", "stop_too_tight", "bad_target", "sweep_continued",
              "indicator_lag"]                                 # only make sense for losing trades
NOT_MEASURABLE = {"news_event": "needs the event calendar (Phase 11)",
                  "overtrading": "needs the risk engine / position book (Phase 11)",
                  "fvg_ignored": "needs per-trade gap tracking (later phase)"}
TREND_FAMILIES = {"trend_following", "momentum", "mtf_pullback"}
BREAKOUT_FAMILIES = {"breakout", "momentum"}
PERMISSION_TFS = ["1w", "1d", "4h", "1h"]


def settings(cfg_section):
    out = dict(DEFAULTS)
    out.update(cfg_section or {})
    return out


def context(df, feats, reg, tf_ms):
    """Arrays describing every candle (known at its close). reg = {regime tf: (labels, exp_dirs)} aligned."""
    c = df["close"].astype(float)
    atr = feats["atr"].to_numpy(dtype=float)
    ema20 = c.ewm(span=20, adjust=False, min_periods=20).mean().to_numpy()
    kz = (smc.killzone_hours(df["open_time"].to_numpy()) if tf_ms <= 3_600_000
          else np.full(len(df), None, dtype=object))
    col = lambda k: (feats[k].to_numpy() if k in feats else np.full(len(df), np.nan))
    return dict(open=df["open"].to_numpy(dtype=float), high=df["high"].to_numpy(dtype=float),
                low=df["low"].to_numpy(dtype=float), close=c.to_numpy(), atr=atr, ema20=ema20,
                rsi=fe.rsi(c, 14).to_numpy(), adx=rg._adx(df, 14).to_numpy(), rel_vol=col("rel_vol"),
                disp_up=col("displacement_up").astype(bool), disp_dn=col("displacement_down").astype(bool),
                fail_up=col("failed_breakout_up").astype(bool), fail_dn=col("failed_breakout_down").astype(bool),
                h4_bull_ob_low=col("h4_bull_ob_low"), h4_bear_ob_high=col("h4_bear_ob_high"),
                kz=kz, intraday=tf_ms <= 3_600_000, reg=reg, n=len(df))


def _dirs(reg, t_from, t_to):
    labels, exp = reg
    return rg_dirs(labels[t_from:t_to + 1], exp[t_from:t_to + 1]), labels[t_from:t_to + 1]


def rg_dirs(labels, exp):
    labels, exp = np.asarray(labels, dtype=object), np.asarray(exp, dtype=object)
    bull = np.isin(labels, list(rg.BULL)) | ((labels == "EXPANSION") & (exp == "up"))
    bear = np.isin(labels, list(rg.BEAR)) | ((labels == "EXPANSION") & (exp == "down"))
    return np.where(bull, 1, np.where(bear, -1, 0))


def conditions(ctx, t, d, strat, A, data_ok=True):
    """Tags describing the market when the signal came (candle t) - measured for every trade."""
    a = ctx["atr"][t]
    out = []
    if strat["gate"] != "mean_reversion" and np.isfinite(ctx["adx"][t]) and ctx["adx"][t] < A["range_adx"]:
        out.append("range_market")              # (a range is exactly where mean reversion is meant to trade)
    for tf in PERMISSION_TFS:
        if tf in ctx["reg"] and ctx["reg"][tf][0][t] == ("STRONG_BEAR" if d == 1 else "STRONG_BULL"):
            out.append("htf_conflict")
            break
    if np.isfinite(ctx["rel_vol"][t]) and ctx["rel_vol"][t] < A["low_rel_vol"]:
        out.append("low_relative_volume")
    if np.isfinite(a) and a > 0:
        ext = d * (ctx["close"][t] - ctx["ema20"][t]) / a
        r = ctx["rsi"][t]
        if (np.isfinite(ext) and ext >= A["overextended_atr"]) or \
           (np.isfinite(r) and ((d == 1 and r >= A["overextended_rsi"]) or (d == -1 and r <= 100 - A["overextended_rsi"]))):
            out.append("overextended_entry")
        k = int(A["late_move_bars"])
        if t >= k and d * (ctx["close"][t] - ctx["close"][t - k]) / a >= A["late_move_atr"]:
            out.append("late_entry")
    if strat["family"] in BREAKOUT_FAMILIES or (strat["family"] == "smc" and strat["gate"] == "trend"):
        # breakouts and SMC continuation setups claim a strong candle; reversals (e.g. S8) do not
        disp = ctx["disp_up"] if d == 1 else ctx["disp_dn"]
        if not disp[max(0, t - int(A["displacement_bars"]) + 1):t + 1].any():
            out.append("no_displacement")
    if ctx["intraday"] and ctx["kz"][t] not in A["main_sessions"]:
        out.append("wrong_session")
    if not data_ok:
        out.append("data_issue")
    return out


def outcome_tags(ctx, tr, strat, regime_tf):
    """Tags describing what happened during (and just after) the trade."""
    A = strat.get("_A") or DEFAULTS
    d, t, i0, i1 = tr["dir"], tr["signal_idx"], tr["entry_idx"], tr["exit_idx"]
    a = ctx["atr"][t]
    out = []
    if np.isfinite(a) and a > 0:
        if tr["R"] / a > A["wide_stop_atr"]:
            out.append("stop_too_wide")
        if (ctx["high"][i0:i1 + 1] - ctx["low"][i0:i1 + 1]).max() >= A["spike_atr"] * a:
            out.append("volatility_spike")
    if strat["family"] in BREAKOUT_FAMILIES:
        fail = ctx["fail_up"] if d == 1 else ctx["fail_dn"]
        if fail[i0:min(ctx["n"], i0 + int(A["false_breakout_bars"]))].any():
            out.append("false_breakout")
    if regime_tf in ctx["reg"]:
        dirs, labels = _dirs(ctx["reg"][regime_tf], i0, i1)
        start_dir = rg_dirs([ctx["reg"][regime_tf][0][t]], [ctx["reg"][regime_tf][1][t]])[0]
        if start_dir != -d and (dirs == -d).any():
            out.append("trend_reversal")
        elif not np.isin(labels, list(strat["regimes"])).all():
            out.append("regime_mismatch")
    rules = " ".join(map(str, (strat.get("long") or []) + (strat.get("short") or [])))
    if "h4_bull_ob" in rules or "h4_bear_ob" in rules:
        lvl = ctx["h4_bull_ob_low"][t] if d == 1 else ctx["h4_bear_ob_high"][t]
        closes = ctx["close"][i0:i1 + 1]
        if np.isfinite(lvl) and ((d == 1 and (closes < lvl).any()) or (d == -1 and (closes > lvl).any())):
            out.append("ob_failed")
    if tr["r"] < 0:                                            # loser-only tags
        if strat["family"] in TREND_FAMILIES and tr["mfe_r"] < A["lag_mfe_r"]:
            out.append("indicator_lag")
        if tr["r"] + tr["cost_r"] >= 0:
            out.append("fees_slippage")
        if d == -1 and tr["r"] + tr.get("funding_r", 0.0) >= 0:
            out.append("funding")
        if tr["reason"] == "SL":
            end = min(ctx["n"], i0 + int(strat["time_stop_bars"]))
            after_hi, after_lo = ctx["high"][i1 + 1:end], ctx["low"][i1 + 1:end]
            if len(after_hi) and ((d == 1 and after_hi.max() >= tr["tp1"]) or (d == -1 and after_lo.min() <= tr["tp1"])):
                out.append("stop_too_tight")
            st = strat["stop"]
            if st.get("method") == "structure" and "sweep" in str(st.get("long_level" if d == 1 else "short_level")):
                out.append("sweep_continued")
        tp1_r = abs(tr["tp1"] - tr["entry"]) / tr["R"]
        if tr["hit"] == 0 and tr["mfe_r"] >= A["bad_target_share"] * tp1_r:
            out.append("bad_target")
    return out


def tag_trade(ctx, tr, strat, regime_tf, A, data_ok=True):
    """Adds 'tags' (conditions at entry + what happened) and 'regime' / 'session' to a backtest trade."""
    t, d = tr["signal_idx"], tr["dir"]
    s = dict(strat, _A=A)
    tr["tags"] = conditions(ctx, t, d, strat, A, data_ok) + outcome_tags(ctx, tr, s, regime_tf)
    lab = ctx["reg"][regime_tf][0][t] if regime_tf in ctx["reg"] else None
    tr["regime"] = lab if isinstance(lab, str) else "unknown"
    tr["session"] = (ctx["kz"][t] or "outside killzones") if ctx["intraday"] else "n/a (4H and above)"
    return tr


def _share(k, n):
    return k / n if n else 0.0


def _seg(trades, key):
    out = {}
    for t in trades:
        out.setdefault(str(t.get(key)), []).append(t["r"])
    return {k: dict(n=len(v), avg_r=round(float(np.mean(v)), 3)) for k, v in sorted(out.items())}


def summarize(trades, A):
    """Everything section 17 asks about one strategy version x timeframe (backtest trades with tags)."""
    losers = [t for t in trades if t["r"] < 0]
    winners = [t for t in trades if t["r"] >= 0]
    nL, nW = len(losers), len(winners)
    tags = {}
    for tag in CONDITIONS + PATH_TAGS + LOSER_TAGS:
        kL = sum(tag in t["tags"] for t in losers)
        kW = sum(tag in t["tags"] for t in winners)
        with_ = [t["r"] for t in trades if tag in t["tags"]]
        without = [t["r"] for t in trades if tag not in t["tags"]]
        p, q = _share(kL, nL), _share(kW, nW)
        row = dict(losers=kL, loss_share=round(p, 3), n_with=len(with_),
                   avg_r_with=round(float(np.mean(with_)), 3) if with_ else None,
                   avg_r_without=round(float(np.mean(without)), 3) if without else None)
        if tag in LOSER_TAGS:
            row.update(kind="losers only", flag=bool(nL >= A["min_losses"] and p >= A["frequent_share"]))
        else:
            se = np.sqrt(p * (1 - p) / max(nL, 1) + q * (1 - q) / max(nW, 1))
            row.update(kind="losers vs winners", win_share=round(q, 3),
                       flag=bool(nL >= A["min_losses"] and nW > 0 and p - q > 2 * se))
        if kL or kW:
            tags[tag] = row
    r = np.array([t["r"] for t in trades], dtype=float)
    gross = np.array([t["r"] + t.get("cost_r", 0.0) + t.get("funding_r", 0.0) for t in trades], dtype=float)
    mae_w = [t["mae_r"] for t in winners]
    mfe_l = [t["mfe_r"] for t in losers]
    q = lambda x, p: round(float(np.percentile(x, p)), 2) if x else None
    return dict(losses=nL, wins=nW, tags=tags, not_measurable=NOT_MEASURABLE,
                avg_r=round(float(r.mean()), 3) if len(r) else None,
                se_r=round(float(r.std() / np.sqrt(len(r))), 3) if len(r) > 1 else None,
                gross_avg_r=round(float(gross.mean()), 3) if len(r) else None,
                systematic=[k for k, v in tags.items() if v["flag"]],
                mae_mfe=dict(winners_mae_median=q(mae_w, 50), winners_mae_p90=q(mae_w, 10),
                             losers_mfe_median=q(mfe_l, 50), losers_mfe_p75=q(mfe_l, 75)),
                by_regime=_seg(trades, "regime"), by_session=_seg(trades, "session"),
                by_direction=_seg([dict(t, side="long" if t["dir"] == 1 else "short") for t in trades], "side"))


def diagnose(att, other_tfs, A, stop_variants=None):
    """The 8 questions of section 17.3, answered from the numbers of summarize().
    other_tfs: {timeframe: average R} of the same strategy version on its other timeframes.
    stop_variants: the +-20% stop-size rows of the Phase 8 test (the evidence behind any stop change)."""
    n, avg = att["losses"] + att["wins"], att["avg_r"]
    rs_ = [x for x in att["by_regime"].items() if x[1]["n"] >= 10]
    pos = [k for k, v in rs_ if v["avg_r"] > 0]
    neg = [k for k, v in rs_ if v["avg_r"] <= 0]
    tags = att["tags"]
    share = lambda k: tags.get(k, {}).get("loss_share", 0.0)
    out = []
    if n < A["min_losses"]:
        out.append(f"Sample too small: only {n} trades - no conclusion yet.")
    elif att["se_r"] and abs(avg) < 2 * att["se_r"]:
        out.append(f"Sample: {n} trades, {avg:+.2f}R per trade - cannot be told apart from zero (±2 standard errors "
                   f"= ±{2 * att['se_r']:.2f}R).")
    else:
        out.append(f"Sample: {n} trades, {avg:+.2f}R per trade - clearly {'above' if avg > 0 else 'below'} zero.")
    if rs_:
        if not pos:
            out.append("Strategy wrong? It loses in every regime with 10+ trades (" + ", ".join(neg) + ").")
        elif neg:
            out.append(f"Regime: profitable in {', '.join(pos)}; losing in {', '.join(neg)}.")
        else:
            out.append(f"Regime: profitable in every regime with 10+ trades ({', '.join(pos)}).")
    mm = att["mae_mfe"]
    if mm["losers_mfe_median"] is not None:
        out.append(("Timing / exits: half the losers were at least "
                    f"{mm['losers_mfe_median']:+.2f}R in profit first - exits or targets are worth testing.")
                   if mm["losers_mfe_median"] >= 0.5 else
                   f"Timing: losers rarely went our way (median best point {mm['losers_mfe_median']:+.2f}R).")
    out.append(f"Stop / target: stopped out and then TP1 reached anyway in {share('stop_too_tight') * 100:.0f}% of "
               f"losses; target nearly reached (≥ 80%) in {share('bad_target') * 100:.0f}%."
               + (" Measured stop changes (±20% test): " + "; ".join(f"{v['change']} → {v['avg_r']:+.2f}R"
                                                                     for v in stop_variants) + "."
                  if stop_variants else ""))
    gross = att["gross_avg_r"]
    if gross is not None and avg is not None:
        out.append(f"Costs: {gross:+.2f}R per trade before fees and slippage, {avg:+.2f}R after"
                   + (" - costs destroy the edge." if gross > 0 >= avg else "."))
    if other_tfs:
        best = max(other_tfs.items(), key=lambda x: x[1])
        out.append(f"Other timeframes: best is {best[0]} at {best[1]:+.2f}R per trade.")
    out.append("Systematic causes: " + (", ".join(att["systematic"]) if att["systematic"] else
                                       "none stands out - with this sample the losses look random."))
    return out


# ---------------------------------------------------------------- missed moves (section 17.4)
def strong_moves(df, atr, now_ms, A):
    """Strong moves on 1H candles in the last missed_lookback_hours: net move >= strong_move_atr x ATR(1H)
    within strong_move_bars candles. Returns the biggest one per direction: dict(start, end, dir, size_atr, pct)."""
    ot, c = df["open_time"].to_numpy(), df["close"].to_numpy(dtype=float)
    since = now_ms - int(A["missed_lookback_hours"]) * 3_600_000
    k = int(A["strong_move_bars"])
    best = {}
    for e in np.flatnonzero(ot >= since):
        for s in range(max(0, e - k), e):
            a = atr[s]
            if not np.isfinite(a) or a <= 0:
                continue
            size = (c[e] - c[s]) / a
            d = 1 if size > 0 else -1
            if abs(size) >= A["strong_move_atr"] and abs(size) > best.get(d, {}).get("size_atr", 0):
                best[d] = dict(start=s, end=e, dir=d, size_atr=round(abs(float(size)), 1),
                               pct=round(float((c[e] / c[s] - 1) * 100), 2),
                               start_ms=int(ot[s]), end_ms=int(ot[e]) + 3_600_000)
    return list(best.values())


def check_move(move, tf_close_times, raw_l, raw_s, reg_ok, perm_l, perm_s, final_l, final_s, A):
    """What ONE strategy on ONE timeframe did around a strong move: 'signal', 'blocked by the regime gate',
    'blocked by the permission gate', 'no valid stop / target' or 'no setup'. Signals up to
    signal_window_bars hours before the move started, until 1 hour after it started, count."""
    a = move["start_ms"] - int(A["signal_window_bars"]) * 3_600_000
    b = move["start_ms"] + 3_600_000
    idx = np.flatnonzero((tf_close_times >= a) & (tf_close_times < b))
    if not len(idx):
        return "no candles"
    raw = (raw_l if move["dir"] == 1 else raw_s)[idx]
    if not raw.any():
        return "no setup"
    fin = (final_l if move["dir"] == 1 else final_s)[idx]
    if fin.any():
        return "signal"
    if not reg_ok[idx][raw].any():
        return "blocked by the regime gate"
    perm = (perm_l if move["dir"] == 1 else perm_s)[idx]
    if not (perm & reg_ok[idx])[raw].any():
        return "blocked by the permission gate"
    return "no valid stop / target"


def move_verdict(findings):
    kinds = set(findings.values())
    if "signal" in kinds:
        return "identifiable: at least one strategy had a valid signal before the move"
    if any(k.startswith("blocked") or k.startswith("no valid") for k in kinds):
        return "a setup existed but was filtered out (see which gate) - do NOT change a rule because of one move"
    return "not identifiable: no strategy had a setup before the move"
