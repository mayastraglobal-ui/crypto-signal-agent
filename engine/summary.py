"""
The '## Email summary' block of Claude's reports (email redesign): a few short, machine-readable lines the engine
puts into the email next to its own numbers. The full report is published as a page on the dashboard.

    ## Email summary
    - headline: Nothing to trade. Wait.
    - sub: BTC is flat near 84,000 while altcoins jumped; the jobs report is on Friday.
    - mood: Calm
    - do: Wait for a LIVE entry email before any trade.
    - dont: Don't chase the SUI +13% candle.

Which keys each report needs (KEYS); the Brain guard refuses a report whose block is missing or breaks a rule
(problems()). Pure functions.
"""
import re

MOODS = ("Calm", "Busy", "Volatile", "Risk-off")
KEYS = {                                      # report kind -> (required keys, optional keys)
    "briefing": (("headline", "sub", "do", "dont"), ("mood",)),   # the email's mood word is the engine's
    "daily": (("lesson", "tomorrow"), ("sub", "watch", "avoid")),                 # format v2: TOMORROW rows
    "weekly": (("headline", "sub", "next", "improvement"), ("test", "fix", "study")),   # format v2: NEXT WEEK rows
}
MAX_WORDS = {"headline": 8, "sub": 20}
MAX_WORDS_OTHER = 30
HEADING = "## Email summary"
_LINE = re.compile(r"^\s*-\s*([a-z_']+)\s*:\s*(.*?)\s*$", re.I)
_MARKDOWN = re.compile(r"\*|`|^#|\[[^\]]*\]\(|__|https?://")


def kind_of(path):
    """reports/claude/briefings/... -> 'briefing' (daily / weekly), or None."""
    for folder, k in (("/briefings/", "briefing"), ("/daily/", "daily"), ("/weekly/", "weekly")):
        if folder in "/" + str(path):
            return k
    return None


def block_lines(text):
    """The lines of the '## Email summary' section (until the next '## ' heading), or None when there is none."""
    parts = ("\n" + (text or "")).split("\n" + HEADING, 1)
    if len(parts) < 2:
        return None
    body = parts[1].split("\n", 1)[1] if "\n" in parts[1] else ""
    return body.split("\n## ", 1)[0].splitlines()


def parse(text):
    """{key: value} of the block ('don't' / "dont" both give 'dont'), or None when there is no block."""
    lines = block_lines(text)
    if lines is None:
        return None
    out = {}
    for ln in lines:
        m = _LINE.match(ln)
        if m:
            k = m.group(1).lower().replace("'", "")
            out.setdefault(k, m.group(2))
    return out


def problems(text, kind):
    """Why the block is not good enough for the email ([] = fine)."""
    if kind not in KEYS:
        return []
    lines = block_lines(text)
    if lines is None:
        return [f"no '{HEADING}' section (the email is built from it - see tasks/COMMON.md)"]
    req, opt = KEYS[kind]
    probs, seen = [], set()
    for ln in lines:
        if not ln.strip():
            continue
        m = _LINE.match(ln)
        if not m:
            probs.append(f"'{HEADING}': every line must be '- key: text' (got {ln.strip()[:60]!r})")
            continue
        k, v = m.group(1).lower().replace("'", ""), m.group(2)
        if k not in req + opt:
            probs.append(f"'{HEADING}': unknown key '{k}' (a {kind} has {', '.join(req + opt)})")
            continue
        if k in seen:
            probs.append(f"'{HEADING}': '{k}' twice")
        seen.add(k)
        if not v:
            probs.append(f"'{HEADING}': '{k}' is empty")
            continue
        if _MARKDOWN.search(v):
            probs.append(f"'{HEADING}': '{k}' must be plain text (no *, `, #, links or URLs)")
        n = len(v.split())
        limit = MAX_WORDS.get(k, MAX_WORDS_OTHER)
        if n > limit:
            probs.append(f"'{HEADING}': '{k}' has {n} words - at most {limit}")
        if k == "mood" and v not in MOODS:
            probs.append(f"'{HEADING}': mood must be one of {', '.join(MOODS)}")
    probs += [f"'{HEADING}': '{k}' is missing" for k in req if k not in seen]
    return probs
