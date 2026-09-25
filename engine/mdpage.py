"""
Claude's full reports (briefings, daily reviews, weekly research - reports/claude/) as clean HTML pages on the
dashboard (email redesign): the emails show only the core and link here.

A small markdown reader of our own (headings, paragraphs, lists, tables, code blocks, bold / italic / code, links):
everything is HTML-escaped first, and only http(s) links become links. No JavaScript, no external files.
Pure functions.
"""
import html
import re

CSS = """
:root{--bg:#F4F1EA;--card:#FFFFFF;--line:#E3DED3;--text:#1B1F24;--muted:#5B6470;--teal:#0F5E63;--tile:#F6F4EF}
@media (prefers-color-scheme: dark){:root{--bg:#15181B;--card:#1E2226;--line:#2E3338;--text:#E8E6E1;--muted:#9AA3AD;
--teal:#5FB3B8;--tile:#262B30}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif}
main{max-width:760px;margin:0 auto;padding:16px}
article{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 22px;overflow-wrap:anywhere}
nav{font-size:13px;margin:4px 2px 12px;color:var(--muted)} nav a{color:var(--teal)}
h1{font-size:24px;line-height:1.25;margin:0 0 12px} h2{font-size:18px;margin:26px 0 8px;color:var(--teal)}
h3{font-size:16px;margin:18px 0 6px} a{color:var(--teal)}
code{font-family:'SFMono-Regular',Menlo,Consolas,monospace;font-size:13px;background:var(--tile);padding:1px 4px;
border-radius:4px} pre{background:var(--tile);padding:12px;border-radius:8px;overflow-x:auto} pre code{padding:0}
table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow-x:auto}
td,th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
ul,ol{padding-left:22px} li{margin:3px 0} footer{color:var(--muted);font-size:12px;margin:14px 4px}
"""


def _inline(s):
    s = html.escape(s, quote=False)
    code = []

    def keep(m):
        code.append(m.group(1))
        return f"\x00{len(code) - 1}\x00"
    s = re.sub(r"`([^`]+)`", keep, s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r'(?<!href=")(?<![">])(https?://[^\s<)]+)', r'<a href="\1">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"<em>\1</em>", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{code[int(m.group(1))]}</code>", s)


def to_html(md):
    """The body HTML of a markdown text."""
    out, lines, i = [], (md or "").splitlines(), 0
    para = []

    def flush():
        if para:
            out.append("<p>" + " ".join(_inline(x.strip()) for x in para) + "</p>")
            para.clear()
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("```"):
            flush()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(lines[i + 1:j]), quote=False) + "</code></pre>")
            i = j + 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            flush()
            n = min(3, len(m.group(1)))
            out.append(f"<h{n}>{_inline(m.group(2).strip())}</h{n}>")
            i += 1
            continue
        if re.match(r"^\s*\|.*\|\s*$", ln):
            flush()
            rows = []
            while i < len(lines) and re.match(r"^\s*\|.*\|\s*$", lines[i]):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.match(r"^:?-{2,}:?$", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            if rows:
                out.append("<table><tr>" + "".join(f"<th>{_inline(c)}</th>" for c in rows[0]) + "</tr>"
                           + "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
                           + "</table>")
            continue
        m = re.match(r"^(\s*)([-*•]|\d+[.)])\s+(.*)$", ln)
        if m:
            flush()
            tag = "ol" if m.group(2)[0].isdigit() else "ul"
            items = []
            while i < len(lines):
                m2 = re.match(r"^(\s*)([-*•]|\d+[.)])\s+(.*)$", lines[i])
                if m2:
                    items.append(m2.group(3))
                elif lines[i].startswith("  ") and lines[i].strip() and items:
                    items[-1] += " " + lines[i].strip()
                else:
                    break
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if not ln.strip():
            flush()
        else:
            para.append(ln)
        i += 1
    flush()
    return "\n".join(out)


def title_of(md, default="Report"):
    return next((ln[2:].strip() for ln in (md or "").splitlines() if ln.startswith("# ")), default)


def page(md, source_path, back="../../index.html"):
    """A whole page for one report."""
    t = html.escape(re.sub(r"[*`_]", "", title_of(md)))
    return ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" "
            f"content=\"width=device-width,initial-scale=1\"><title>{t}</title><style>{CSS}</style></head><body><main>"
            f"<nav><a href=\"{back}\">← Dashboard</a> · written by Claude from the engine's numbers</nav>"
            f"<article>{to_html(md)}</article><footer>Source: {html.escape(source_path)} · Research signal. Not "
            "financial advice.</footer></main></body></html>\n")


def page_path(report_path):
    """reports/claude/daily/2026-09-25.md -> claude/daily/2026-09-25.html (inside the dashboard)."""
    rel = str(report_path).split("reports/", 1)[-1]
    return rel[:-3] + ".html" if rel.endswith(".md") else rel + ".html"
