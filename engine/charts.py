"""
Chart images for emails (AGENT_PROMPT.md section 20) - Phase 12.

One PNG per trade email (entry / update): the last candles of the signal's timeframe with the entry, stop and
target lines, the entry candle marked and (for an exit) the exit candle. Files go to reports/charts/, which
is NOT committed to main (they are email attachments only).

No internet. Uses matplotlib without a screen (Agg backend).
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

UP, DOWN = "#26a69a", "#ef5350"


def trade_chart(df, path, title, entry, stop, targets, entry_ms=None, exit_ms=None, exit_price=None,
                current_stop=None, bars=120):
    """Draw candles of df (open_time, open, high, low, close; closed candles only) and the trade levels.
    entry_ms / exit_ms: open time of the entry / exit candle (marked when inside the window). Returns path."""
    d = df.tail(bars).reset_index(drop=True)
    if d.empty:
        raise ValueError("no candles to draw")
    x = np.arange(len(d))
    o, h, l, c = (d[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close"))
    col = np.where(c >= o, UP, DOWN)
    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    ax.vlines(x, l, h, color=col, linewidth=0.8)
    ax.bar(x, np.maximum(np.abs(c - o), (h - l) * 0.01 + 1e-12), bottom=np.minimum(o, c), color=col, width=0.7)
    levels = [("entry", entry, "#1e88e5", "-"), ("stop", stop, DOWN, "--")]
    levels += [(f"TP{i}", t, UP, "--") for i, t in enumerate(targets or [], 1) if t is not None and np.isfinite(t)]
    if current_stop is not None and np.isfinite(current_stop) and abs(current_stop - stop) > 1e-12:
        levels.append(("stop now", current_stop, "#fb8c00", ":"))
    for name, y, colr, ls in levels:
        ax.axhline(y, color=colr, linestyle=ls, linewidth=1)
        ax.text(len(d) + 0.5, y, f" {name} {y:.6g}", va="center", fontsize=8, color=colr)
    ot = d["open_time"].to_numpy()
    for ms, mark, colr, lab in ((entry_ms, "^", "#1e88e5", "entry"), (exit_ms, "x", "#6d4c41", "exit")):
        if ms is None:
            continue
        i = int(np.searchsorted(ot, ms, side="right") - 1)
        if 0 <= i < len(d):
            y = exit_price if (lab == "exit" and exit_price is not None) else (entry if lab == "entry" else c[i])
            ax.plot([i], [y], marker=mark, color=colr, markersize=10, label=lab)
    step = max(1, len(d) // 6)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([pd.to_datetime(t, unit="ms").strftime("%m-%d %H:%M") for t in ot[::step]], fontsize=8)
    ax.set_xlim(-1, len(d) + 8)
    ax.set_title(title, fontsize=10)
    ax.grid(alpha=0.2)
    ax.text(0.01, 0.01, "Research signal. Not financial advice. Times in UTC.", transform=ax.transAxes,
            fontsize=7, color="grey")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path
