"""
The trials counter (Phase 17; AGENT_PROMPT.md sections 11-12 - the multiple-testing problem).

Every strategy version x timeframe the daily research run has EVER tested is one trial, written once to
memory/trials.csv (append-only; it only grows, even when a version is retired). Testing many ideas makes it likely
that some look good by pure luck. So the PAPER_TRADING bar rises with the number of trials N:

  the average trade's t-statistic (mean R / (standard deviation of R / sqrt(trades))) must reach
  z(1 - alpha / N), the one-sided normal value with a Bonferroni correction (alpha = research.trials_alpha).

  N = 1 -> 1.64 · N = 50 -> 3.09 · N = 100 -> 3.29 · N = 500 -> 3.72 · N = 1000 -> 3.89

Bonferroni is deliberately simple and conservative (it assumes the trials are unrelated; related versions of the
same idea make it stricter than needed, never looser). Trades of one cell overlap in time across coins, so the
t-statistic is an approximation - one more bar on top of every Phase 8 test, not a replacement for them.

Pure functions; research.py reads and appends the file.
"""
import csv
import io
import math
from statistics import NormalDist

COLUMNS = ["trial", "first_tested_utc", "strategy", "version", "tf", "origin"]


def need_t(n_trials, alpha):
    """The t-statistic an average trade must reach after n_trials trials (Bonferroni, one-sided)."""
    return NormalDist().inv_cdf(1 - float(alpha) / max(1, int(n_trials)))


def t_stat(r):
    """t-statistic of the mean of per-trade R values (None with < 2 trades or no spread)."""
    r = [float(x) for x in r]
    n = len(r)
    if n < 2:
        return None
    m = sum(r) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in r) / (n - 1))
    return m / (sd / math.sqrt(n)) if sd > 0 else None


def parse(text):
    """memory/trials.csv -> [row dicts] (empty text -> [])."""
    if not (text or "").strip():
        return []
    return [dict(r) for r in csv.DictReader(io.StringIO(text))]


def key(row):
    return f"{row['strategy']}@{row['version']}|{row['tf']}"


def backfill(registry):
    """The trials the engine ran before the counter existed: every cell of memory/strategy_registry.csv, in the
    order the versions were first tested."""
    rows = []
    for ck in sorted(registry["cells"], key=lambda c: (registry["versions"].get(c.split("|")[0], {}).get("experiment") or 0, c)):
        k, tf = ck.split("|")
        v = registry["versions"].get(k, {})
        sid, ver = k.rsplit("@", 1)
        rows.append(dict(strategy=sid, version=ver, tf=tf, first_tested_utc=v.get("first_tested_utc") or "-",
                         origin="before the counter (strategy_registry.csv)"))
    return rows


def additions(existing, tested, now_txt):
    """New trial rows for cells tested this run that are not in the file yet.
    tested: [(strategy, version, tf, origin)]. Numbers continue after the existing rows."""
    have = {key(r) for r in existing}
    out = []
    for sid, ver, tf, origin in tested:
        r = dict(strategy=sid, version=str(ver), tf=tf, first_tested_utc=now_txt, origin=origin)
        if key(r) not in have:
            have.add(key(r))
            out.append(r)
    return number(out, len(existing))


def number(rows, start):
    return [dict(r, trial=start + i + 1) for i, r in enumerate(rows)]


def to_csv(rows, header):
    buf = io.StringIO()
    wr = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    if header:
        wr.writeheader()
    for r in rows:
        wr.writerow({c: r.get(c) for c in COLUMNS})
    return buf.getvalue()


def summary(rows, alpha, since_txt=None):
    """What the report and the emails show: total trials, new since a date, the bar now and with one trial."""
    new = [r for r in rows if since_txt and str(r.get("first_tested_utc") or "") >= since_txt]
    return dict(total=len(rows), new=len(new), alpha=float(alpha), need_t=round(need_t(len(rows), alpha), 3),
                need_t_one=round(need_t(1, alpha), 3),
                lab=sum(r.get("origin") == "lab" for r in rows))
