"""
The email layout (email redesign, format v2): every email is a short list of BLOCKS, rendered twice - as a Gmail /
phone safe HTML card (600 px, tables, inline CSS only, no external fonts, no JavaScript) and as the plain-text part of
the same email. Both come from the same blocks, so they always say the same thing.

Format v2: the header starts with a TYPE PILL (LIVE, PAPER, ALERT, FIXED, BRIEFING, DAILY, WEEKLY); every email has an
ACTION box right under its banner / headline; a PAPER email is a dashed blue card and never uses the LIVE green.

A block is a tuple (kind, data):
  ("header", (pill, label, when))            the type pill, a small caps label, date + time right
  ("banner", dict(title, sub, right, big, tone, note))  the big coloured headline (tone: long / short / win / loss /
                                             plain / amber / teal / teal_solid / paper)
  ("headline", (text, sub))                  a big sentence and one sub-sentence (briefing, reviews)
  ("section", title)                         a small caps section title
  ("tiles", (tone, [(label, value, note[, value tone])]))  2-4 number tiles (tone: grey / teal / paper)
  ("table", dict(cols, rows, tones, mono))   a short table; tones[i][j] = None / "up" / "down" colours one cell
  ("kv", [(label, text), ...])               key - value rows (WHAT BROKE, TEST / CHECK / STUDY ...)
  ("list", [text, ...])                      numbered one-line items (reasons, actions)
  ("bullets", [text, ...])                   short lines without numbers
  ("label", text)                            a small caps sub-title inside a section
  ("chips", [(text, ok), ...])               check chips: ok True = green tick, False = amber warning
  ("box", dict(title, lines, tone, strong, color, numbered))  a framed box; strong + color = the ACTION box
  ("line", text)                             one muted line
  ("score", [part, ...])                     the score line (monospace, grey): R today, week, open trades ...
  ("progress", (left, right, fraction))      a progress bar with a label on each side
  ("squares", (results, legend))             small squares, one per trade: True = win (light), False = loss (dark)
  ("timeline", [(time, text, state)])        a short trade history; state done / now / next
  ("grid", (cells, per_row, legend))         small cells, per_row a row (backtests per coin)
  ("bars", [(label, value_text, fraction, note)])  progress bars (closest to passing)
  ("ideas", [dict(name, what, source, status)])     new lab cards with a SOURCE and a STATUS chip
  ("image", cid)                             the chart image (signal emails only), shown from the attachment
  ("buttons", [(label, url), ...])           1-2 buttons (a missing url is left out)
  ("footer", text)                           the grey footer line

Missing numbers are shown as "–" (never guessed): see val(). Pure functions.
"""
import html
import math
import re

PAGE, CARD, BORDER, TEXT, MUTED, TEAL = "#F4F1EA", "#FFFFFF", "#E3DED3", "#1B1F24", "#5B6470", "#0F5E63"
GREEN, GREEN_BG, RED, RED_BG = "#146C43", "#E3F1E8", "#A61B1B", "#F8E4E4"
AMBER, AMBER_BG, TILE, TEAL_BG = "#7A4F00", "#FFF1D6", "#F6F4EF", "#E1EEEE"
PAPER_BLUE, PAPER_BG = "#1D4E89", "#E4EDF8"                 # format v2: practice (paper) emails
GREY_LINE, WIN_SQUARE, LOSS_SQUARE = "#C9C3B6", "#9FD3B4", "#0A3B3E"
WHITE = "#FFFFFF"
FONT = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',Menlo,Consolas,monospace"
DASH = "–"
TONES = {"long": (GREEN, WHITE), "short": (RED, WHITE), "win": (GREEN_BG, GREEN), "loss": (RED_BG, RED),
         "amber": (AMBER_BG, AMBER), "teal": (TEAL_BG, TEAL), "plain": (TILE, TEXT), "paper": (PAPER_BG, PAPER_BLUE),
         "teal_solid": (TEAL, WHITE), "alert": (RED, WHITE)}
PILLS = {"LIVE": (GREEN, WHITE), "PAPER": (PAPER_BG, PAPER_BLUE), "ALERT": (RED, WHITE), "FIXED": (GREEN_BG, GREEN),
         "BRIEFING": (TEAL_BG, TEAL), "DAILY": (TEAL_BG, TEAL), "WEEKLY": (TEAL, WHITE)}
LIVE_TONES = ("long", "short")                               # the solid LIVE banners: never on a PAPER email
CHIP = {"TESTING": (AMBER_BG, AMBER), "FAILED": (RED_BG, RED), "PASSED": (GREEN_BG, GREEN)}
MAX_SUBJECT = 70
_MD = re.compile(r"(\*\*|__|```|`|^#+\s+|^\s*[-*]\s+\[.\]\s*)", re.M)


def missing(x):
    return x is None or x == "" or (isinstance(x, float) and not math.isfinite(x))


def val(x, fmt="{}"):
    """A value for the email, or '–' when it is missing (never a guess)."""
    return DASH if missing(x) else fmt.format(x)


def plain(text):
    """Text for an email with no markdown symbols (**bold**, `code`, # headings): the symbols are removed."""
    s = _MD.sub("", str(text or "")).replace("*", "").strip()
    return re.sub(r"\s+", " ", s)


def subject(parts, limit=MAX_SUBJECT):
    """Parts joined with ' · ', under the limit: the last parts are dropped first, then the text is cut.
    The first part keeps its type word (LIVE ▲ LONG BTC 1H, PAPER ..., ! ..., ✓ Fixed, 08:20 ...)."""
    parts = [plain(p) for p in parts if p not in (None, "")]
    while len(parts) > 1 and len(" · ".join(parts)) > limit:
        parts.pop()
    s = " · ".join(parts)
    return s if len(s) <= limit else s[:limit - 1].rstrip() + "…"


def price(x):
    """Prices as traders read them: 84,050 · 2,717.7 · 120.74 · 1.6009 · 0.061234."""
    if missing(x):
        return DASH
    x = float(x)
    a = abs(x)
    return (f"{x:,.0f}" if a >= 10_000 else f"{x:,.1f}" if a >= 1_000 else f"{x:,.2f}" if a >= 10 else
            f"{x:,.4f}" if a >= 1 else f"{x:.6g}")


def signed(x, unit="R", digits=1):
    if missing(x):
        return DASH
    x = float(x)
    s = f"{abs(x):,.{digits}f}{unit}"
    return ("+" if x > 0 else "−" if x < 0 else "") + s          # a real minus sign


def pct(x, digits=2):
    return signed(x, "%", digits)


def frac(x):
    try:
        return max(0.0, min(1.0, float(x)))
    except (TypeError, ValueError):
        return 0.0


# ---------------------------------------------------------------- plain text ----------------------------------------
def text(blocks):
    L = []
    for kind, d in blocks:
        if kind == "header":
            pill, label, when = d if len(d) == 3 else (None, d[0], d[1])
            L += [(f"[{pill}] " if pill else "") + f"{label}  |  {when}", ""]
        elif kind == "banner":
            L += [d["title"] + (f"   {d['big']}" if d.get("big") else "")]
            L += [x for x in (d.get("sub"), d.get("note"), d.get("right")) if x]
            L.append("")
        elif kind == "headline":
            L += [d[0]] + ([d[1]] if d[1] else []) + [""]
        elif kind == "section":
            L.append(d.upper())
        elif kind == "label":
            L.append(f"  {d.upper()}")
        elif kind == "tiles":
            L += [f"  {t[0]}: {t[1]}" + (f" ({t[2]})" if t[2] else "") for t in d[1]] + [""]
        elif kind == "table":
            rows = [d["cols"]] + d["rows"] if d.get("cols") else d["rows"]
            if rows:
                w = [max(len(str(r[j])) for r in rows) for j in range(len(rows[0]))]
                L += ["  " + " | ".join(str(c).ljust(w[j]) for j, c in enumerate(r)).rstrip() for r in rows]
            L.append("")
        elif kind == "kv":
            L += [f"  {k.upper()}: {v}" for k, v in d] + [""]
        elif kind == "list":
            L += [f"  {i}. {x}" for i, x in enumerate(d, 1)] + [""]
        elif kind == "bullets":
            L += [f"  - {x}" for x in d] + [""]
        elif kind == "chips":
            L += ["  " + " · ".join(("✓ " if ok else "! ") + t for t, ok in d), ""]
        elif kind == "box":
            items = [f"{i}. {x}" for i, x in enumerate(d["lines"], 1)] if d.get("numbered") else d["lines"]
            L += ([d["title"].upper()] if d.get("title") else []) + [f"  {x}" for x in items] + [""]
        elif kind == "line":
            L += [d, ""]
        elif kind == "score":
            L += ["  " + " · ".join(d), ""]
        elif kind == "progress":
            n = int(round(frac(d[2]) * 20))
            L += [f"  {d[0]}" + (f"  ({d[1]})" if d[1] else ""), "  [" + "#" * n + "." * (20 - n) + "]", ""]
        elif kind == "squares":
            L += ["  " + " ".join("W" if w else "L" for w in d[0])] + ([f"  {d[1]}"] if d[1] else []) + [""]
        elif kind == "timeline":
            L += [f"  {t:>5}  {x}" for t, x, _ in d] + [""]
        elif kind == "grid":
            cells, per = d[0], d[1]
            L += ["  " + "   ".join(cells[i:i + per]) for i in range(0, len(cells), per)]
            L += ([f"  {d[2]}"] if d[2] else []) + [""]
        elif kind == "bars":
            L += [f"  {lab}: {v}" + (f" - {n}" if n else "") for lab, v, _, n in d] + [""]
        elif kind == "ideas":
            L += [f"  {x['name']} [{x['source']} · {x['status']}]" + (f" - {x['what']}" if x.get("what") else "")
                  for x in d] + [""]
        elif kind == "image":
            L += ["(chart image attached)", ""]
        elif kind == "buttons":
            L += [f"{lab}: {url}" for lab, url in d if url] + [""]
        elif kind == "footer":
            L += ["--", d]
    while L and not L[-1]:
        L.pop()
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- HTML ----------------------------------------------
def e(x):
    return html.escape(str(x), quote=True)


def _row(inner, pad="0 24px 16px"):
    return f'<tr><td style="padding:{pad};">{inner}</td></tr>'


def _label(t, color=MUTED):
    return (f'<div style="font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:{color};'
            f'font-weight:700;">{e(t)}</div>')


def _tone_cell(x, tone):
    c = GREEN if tone == "up" else RED if tone == "down" else TEXT
    return f'<span style="color:{c};font-family:{MONO};">{e(x)}</span>' if tone else e(x)


def _table(inner):
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{inner}</table>'


def _html_block(kind, d, accent=TEAL):
    if kind == "header":
        pill, label, when = d if len(d) == 3 else (None, d[0], d[1])
        bg, fg = PILLS.get(pill, (TEAL_BG, TEAL))
        p = (f'<span style="display:inline-block;background:{bg};color:{fg};font-size:11px;font-weight:700;'
             f'letter-spacing:1px;padding:4px 8px;border-radius:6px;margin-right:8px;">{e(pill)}</span>') if pill else ""
        return _row(_table(f'<tr><td style="font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:{MUTED};'
                           f'font-weight:700;">{p}{e(label)}</td>'
                           f'<td align="right" style="font-size:12px;color:{MUTED};">{e(when)}</td></tr>'),
                    "20px 24px 14px")
    if kind == "banner":
        bg, fg = TONES.get(d.get("tone"), TONES["plain"])
        sub_fg = fg if d.get("tone") in LIVE_TONES + ("teal_solid", "alert") else TEXT
        big = (f'<td align="right" valign="middle" style="font-size:30px;font-weight:800;color:{fg};'
               f'font-family:{MONO};">{e(d["big"])}</td>') if d.get("big") else ""
        right = (f'<td align="right" valign="bottom" style="font-size:12px;color:{fg};">{e(d["right"])}</td>'
                 if d.get("right") and not d.get("big") else "")
        return _row(_table(f'<tr><td style="padding:16px 18px;background:{bg};border-radius:10px;">'
                           + _table(f'<tr><td valign="top"><div style="font-size:26px;font-weight:800;color:{fg};'
                                    f'line-height:1.2;">{e(d["title"])}</div>'
                                    + (f'<div style="font-size:13px;color:{sub_fg};margin-top:4px;">{e(d["sub"])}</div>'
                                       if d.get("sub") else "")
                                    + (f'<div style="font-size:12px;font-weight:700;letter-spacing:1px;color:{fg};'
                                       f'margin-top:6px;">{e(d["note"])}</div>' if d.get("note") else "")
                                    + f'</td>{big}{right}</tr>')
                           + '</td></tr>'), "0 24px 14px")
    if kind == "headline":
        return _row(f'<div style="font-size:22px;font-weight:800;color:{TEXT};line-height:1.25;">{e(d[0])}</div>'
                    + (f'<div style="font-size:14px;color:{MUTED};margin-top:6px;line-height:1.45;">{e(d[1])}</div>'
                       if d[1] else ""))
    if kind == "section":
        return _row(_label(d), "6px 24px 8px")
    if kind == "label":
        return _row(_label(d, accent), "0 24px 4px")
    if kind == "tiles":
        bg = {"teal": TEAL_BG, "paper": PAPER_BG}.get(d[0], TILE)
        fg = {"teal": TEAL, "paper": PAPER_BLUE}.get(d[0], TEXT)
        items = d[1]
        per = 2 if len(items) == 4 else max(1, len(items))
        rows = ""
        for i in range(0, len(items), per):
            tds = ""
            for t in items[i:i + per]:
                lab, v, n = t[0], t[1], t[2]
                vc = GREEN if len(t) > 3 and t[3] == "up" else RED if len(t) > 3 and t[3] == "down" else fg
                tds += (f'<td width="{int(100 / per)}%" valign="top" style="padding:4px;"><div style="background:{bg};'
                        f'border-radius:8px;padding:10px 10px;"><div style="font-size:11px;color:{MUTED};">{e(lab)}</div>'
                        f'<div style="font-size:18px;font-weight:800;color:{vc};font-family:{MONO};margin-top:2px;">'
                        f'{e(v)}</div>'
                        + (f'<div style="font-size:11px;color:{MUTED};margin-top:2px;">{e(n)}</div>' if n else "")
                        + '</div></td>')
            rows += f"<tr>{tds}</tr>"
        return _row(_table(rows), "0 20px 14px")
    if kind == "table":
        tones = d.get("tones") or []
        head = ("<tr>" + "".join(f'<td style="padding:6px 6px;border-bottom:1px solid {BORDER};">{_label(c)}</td>'
                                 for c in d["cols"]) + "</tr>") if d.get("cols") else ""
        body = "".join("<tr>" + "".join(
            f'<td style="padding:7px 6px;border-bottom:1px solid {BORDER};font-size:13px;color:{TEXT};'
            + (f'font-family:{MONO};' if j in (d.get("mono") or []) else "") + '">'
            + _tone_cell(c, (tones[i][j] if i < len(tones) and j < len(tones[i]) else None)) + "</td>"
            for j, c in enumerate(r)) + "</tr>" for i, r in enumerate(d["rows"]))
        return _row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
                    f'style="border-collapse:collapse;">{head}{body}</table>')
    if kind == "kv":
        body = "".join(f'<tr><td valign="top" style="width:34%;padding:7px 8px 7px 0;border-bottom:1px solid {BORDER};">'
                       f'{_label(k, accent)}</td><td style="padding:7px 0;border-bottom:1px solid {BORDER};font-size:13px;'
                       f'color:{TEXT};line-height:1.4;">{e(v)}</td></tr>' for k, v in d)
        return _row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
                    f'style="border-collapse:collapse;">{body}</table>')
    if kind == "list":
        items = "".join(f'<tr><td valign="top" style="width:22px;font-weight:800;color:{accent};font-size:14px;'
                        f'padding:3px 0;">{i}.</td><td style="font-size:14px;color:{TEXT};padding:3px 0;line-height:1.4;">'
                        f'{e(x)}</td></tr>' for i, x in enumerate(d, 1))
        return _row(_table(items))
    if kind == "bullets":
        return _row("".join(f'<div style="font-size:13px;color:{TEXT};line-height:1.45;margin:2px 0;">{e(x)}</div>'
                            for x in d))
    if kind == "chips":
        chips = "".join(f'<span style="display:inline-block;margin:0 6px 6px 0;padding:5px 10px;border-radius:14px;'
                        f'font-size:12px;background:{GREEN_BG if ok else AMBER_BG};color:{GREEN if ok else AMBER};">'
                        f'{"✓" if ok else "!"} {e(t)}</span>' for t, ok in d)
        return _row(chips)
    if kind == "box":
        bg, fg = TONES.get(d.get("tone"), (CARD, TEXT))
        col = d.get("color") or (TEAL if d.get("tone") in (None, "teal", "plain") else fg)
        border = f"2px solid {col}" if d.get("strong") else f"1px solid {BORDER if d.get('tone') is None else bg}"
        items = d["lines"]
        if d.get("numbered"):
            lines = "".join(f'<div style="font-size:14px;color:{TEXT};line-height:1.45;margin-top:4px;">'
                            f'<b style="color:{col};">{i}.</b> {e(x)}</div>' for i, x in enumerate(items, 1))
        else:
            size = "15px;font-weight:600" if d.get("strong") else "14px"
            lines = "".join(f'<div style="font-size:{size};color:{TEXT};line-height:1.45;margin-top:4px;">{e(x)}</div>'
                            for x in items)
        return _row(f'<div style="border:{border};background:{bg if d.get("tone") else CARD};border-radius:10px;'
                    f'padding:12px 14px;">' + (_label(d["title"], (MUTED if col == GREY_LINE else col) if d.get("strong")
                                                      else fg if d.get("tone") else TEAL)
                                               if d.get("title") else "") + f'{lines}</div>')
    if kind == "line":
        return _row(f'<div style="font-size:13px;color:{MUTED};line-height:1.45;">{e(d)}</div>')
    if kind == "score":
        w = int(100 / max(1, len(d)))
        tds = "".join(f'<td width="{w}%" align="{"left" if i == 0 else "right" if i == len(d) - 1 else "center"}" '
                      f'style="font-size:12px;color:#3F4650;font-family:{MONO};padding:10px 12px;">{e(x)}</td>'
                      for i, x in enumerate(d))
        return _row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{TILE};'
                    f'border-radius:10px;"><tr>{tds}</tr></table>')
    if kind == "progress":
        w = int(round(frac(d[2]) * 100))
        return _row(_table(f'<tr><td style="font-size:13px;color:{TEXT};">{e(d[0])}</td><td align="right" '
                           f'style="font-size:12px;color:{MUTED};">{e(d[1] or "")}</td></tr>')
                    + f'<div style="background:{PAPER_BG if accent == PAPER_BLUE else TILE};border-radius:5px;height:10px;'
                      f'margin-top:6px;"><div style="background:{accent};width:{w}%;height:10px;border-radius:5px;">'
                      f'</div></div>')
    if kind == "squares":
        sq = "".join(f'<span style="display:inline-block;width:12px;height:12px;border-radius:3px;margin:0 4px 4px 0;'
                     f'background:{WIN_SQUARE if w else LOSS_SQUARE};"></span>' for w in d[0])
        return _row(f'<div>{sq}</div>' + (f'<div style="font-size:11px;color:{MUTED};">{e(d[1])}</div>' if d[1] else ""))
    if kind == "timeline":
        dots = {"done": accent, "now": GREEN, "next": GREY_LINE}
        rows = "".join(f'<tr><td valign="top" style="width:48px;font-size:12px;color:{MUTED};font-family:{MONO};'
                       f'padding:3px 0;">{e(t)}</td><td valign="top" style="width:16px;padding:6px 0 0;"><div style="'
                       f'width:10px;height:10px;border-radius:5px;background:{dots.get(s, accent)};"></div></td>'
                       f'<td style="font-size:13px;color:{TEXT};padding:3px 0;line-height:1.4;'
                       f'{"font-weight:700;" if s == "now" else ""}">{e(x)}</td></tr>' for t, x, s in d)
        return _row(_table(rows))
    if kind == "grid":
        cells, per = d[0], d[1]
        rows = "".join("<tr>" + "".join(f'<td width="{int(100 / per)}%" style="padding:3px;"><div style="background:{TILE};'
                                        f'border-radius:6px;padding:6px 6px;font-size:12px;font-family:{MONO};color:{TEXT};">'
                                        f'{e(c)}</div></td>' for c in cells[i:i + per]) + "</tr>"
                       for i in range(0, len(cells), per))
        return _row(_table(rows) + (f'<div style="font-size:11px;color:{MUTED};margin-top:4px;">{e(d[2])}</div>'
                                    if d[2] else ""))
    if kind == "bars":
        out = ""
        for lab, v, fr, note in d:
            w = int(round(frac(fr) * 100))
            out += ('<div style="margin-bottom:10px;">' + _table(
                f'<tr><td style="font-size:13px;color:{TEXT};">{e(lab)}</td>'
                f'<td align="right" style="font-size:12px;color:{MUTED};font-family:{MONO};">{e(v)}</td></tr>')
                + f'<div style="background:{TILE};border-radius:4px;height:8px;margin-top:4px;">'
                f'<div style="background:{TEAL};width:{w}%;height:8px;border-radius:4px;"></div></div>'
                + (f'<div style="font-size:11px;color:{MUTED};margin-top:3px;">{e(note)}</div>' if note else "")
                + "</div>")
        return _row(out)
    if kind == "ideas":
        out = ""
        for x in d:
            bg, fg = CHIP.get(x["status"], (TILE, MUTED))
            out += (f'<div style="border-bottom:1px solid {BORDER};padding:8px 0;"><div style="font-size:14px;'
                    f'font-weight:700;color:{TEXT};">{e(x["name"])}</div>'
                    + (f'<div style="font-size:13px;color:{MUTED};margin-top:2px;">{e(x["what"])}</div>' if x.get("what")
                       else "")
                    + f'<div style="margin-top:5px;"><span style="font-size:10px;letter-spacing:1px;padding:3px 7px;'
                    f'border-radius:10px;background:{TEAL_BG};color:{TEAL};margin-right:6px;">{e(x["source"])}</span>'
                    f'<span style="font-size:10px;letter-spacing:1px;padding:3px 7px;border-radius:10px;background:{bg};'
                    f'color:{fg};">{e(x["status"])}</span></div></div>')
        return _row(out)
    if kind == "image":
        return _row(f'<img src="cid:{e(d)}" width="552" alt="Chart" style="width:100%;max-width:552px;border-radius:8px;'
                    f'display:block;">')
    if kind == "buttons":
        b = "".join(f'<a href="{e(url)}" style="display:inline-block;margin:0 8px 8px 0;padding:11px 18px;'
                    f'border-radius:8px;background:{accent if i == 0 else CARD};color:{WHITE if i == 0 else accent};'
                    f'border:1px solid {accent};font-size:14px;font-weight:700;text-decoration:none;">{e(lab)}</a>'
                    for i, (lab, url) in enumerate([x for x in d if x[1]]))
        return _row(b, "4px 24px 16px") if b else ""
    if kind == "footer":
        return (f'<tr><td style="padding:14px 24px;background:{TILE};border-top:1px solid {BORDER};font-size:12px;'
                f'color:{MUTED};line-height:1.45;border-radius:0 0 14px 14px;">{e(d)}</td></tr>')
    raise ValueError(f"unknown block {kind}")


def to_html(blocks, title="", frame=None):
    """frame 'paper' = the practice card: a 2 px dashed blue border and blue accents (never the LIVE green)."""
    paper = frame == "paper"
    accent = PAPER_BLUE if paper else TEAL
    border = f"2px dashed {PAPER_BLUE}" if paper else f"1px solid {BORDER}"
    rows = "".join(_html_block(k, d, accent) for k, d in blocks)
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><title>{e(title)}</title></head>'
            f'<body style="margin:0;padding:0;background:{PAGE};">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{PAGE};">'
            f'<tr><td align="center" style="padding:16px 8px;">'
            f'<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;'
            f'background:{CARD};border:{border};border-radius:14px;font-family:{FONT};color:{TEXT};">'
            f'{rows}</table></td></tr></table></body></html>')


def render(subject_text, blocks, attachments=(), kind="", frame=None, pill=None):
    """The email as a dict: subject, text, html (+ the chart attachment paths, the kind and the type pill, for
    notify.py and the tests)."""
    if pill is None:
        pill = next((d[0] for k, d in blocks if k == "header" and len(d) == 3), None)
    return dict(subject=subject_text, text=text(blocks), html=to_html(blocks, subject_text, frame),
                attachments=[a for a in attachments if a], kind=kind, pill=pill,
                tones=[d.get("tone") for k, d in blocks if k == "banner"],
                has_action=any(k == "box" and d.get("strong") for k, d in blocks))
