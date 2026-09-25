"""
The idea queue (Phase 18 C item 7): strategy cards written in advance and added to the lab one by one, within the
limits, over the weeks.

memory/experiments.md holds one record per queued card, in queue order:

    ### Queue: <id>@<version>
    - timestamp: ... (the section 22 line)
      - queue: <name>, <k> of <n> - ...
      - card:
    ```yaml
    - id: ...            (the whole card, without `added`)
    ```

The weekly research copies the next queued card(s) into strategies_lab.yaml UNCHANGED, only with `added` = that day,
while the card's factory quota allows (the fact sheet shows the next card ready to paste). The Brain guard refuses a
queued card whose copy differs. Pure functions.
"""
import re

import yaml

TITLE = "Queue:"


class _NoAlias(yaml.SafeDumper):
    """Write every value out in full (no &id001 / *id001 anchors) - the card is copied by hand."""
    def ignore_aliases(self, data):
        return True


FENCE = re.compile(r"```yaml\n(.*?)\n```", re.S)


def parse(text):
    """[dict(key, card)] of the queued cards, in file order (a record whose card does not parse is skipped)."""
    out = []
    for part in ("\n" + (text or "")).split("\n### ")[1:]:
        title = part.splitlines()[0].strip()
        if not title.startswith(TITLE):
            continue
        m = FENCE.search(part)
        if not m:
            continue
        try:
            doc = yaml.safe_load(m.group(1))
        except yaml.YAMLError:
            continue
        card = doc[0] if isinstance(doc, list) and doc and isinstance(doc[0], dict) else None
        if card is not None:
            out.append(dict(key=f"{card.get('id')}@{card.get('version')}", card=card))
    return out


def pending(queue, cards):
    """The queued cards not yet in the lab or the library (cards = every card dict of both files)."""
    have = {f"{c.get('id')}@{c.get('version')}" for c in cards if isinstance(c, dict)}
    return [q for q in queue if q["key"] not in have]


def ready(q, today):
    """The card as it goes into strategies_lab.yaml: unchanged, with added = today."""
    return dict(q["card"], added=str(today))


def copy_problems(card, queue):
    """A card that is in the queue must be copied unchanged (only `added` is set). [] = fine or not queued."""
    key = f"{card.get('id')}@{card.get('version')}"
    q = next((x for x in queue if x["key"] == key), None)
    if q is None:
        return []
    got = {k: v for k, v in card.items() if k != "added"}
    if got != q["card"]:
        diff = sorted(k for k in set(got) | set(q["card"]) if got.get(k) != q["card"].get(k))
        return [f"{key} is a queued card (memory/experiments.md) - copy it unchanged, only with added = today "
                f"(differs in: {', '.join(diff)})"]
    return []


def record(card, name, k, n, source, timestamp, review):
    """The experiments.md record of one queued card."""
    tfs = ", ".join(card["timeframes"])
    body = yaml.dump([card], Dumper=_NoAlias, sort_keys=False, allow_unicode=True, width=110).rstrip()
    return (f"\n### {TITLE} {card['id']}@{card['version']}\n"
            f"- timestamp: {timestamp} · source: {source} · evidence: HYPOTHESIS: a community strategy idea, not tested "
            f"here yet · confidence: untested idea · strategy: {card['id']} v{card['version']} · asset: research coins · "
            f"timeframe: {tfs} · regime: {', '.join(card['regimes'])} · review: {review}\n"
            f"  - queue: {name}, {k} of {n} - the weekly research copies it into strategies_lab.yaml unchanged (added = "
            f"that day) when the {card.get('factory')} quota allows\n"
            f"  - card:\n```yaml\n{body}\n```\n")
