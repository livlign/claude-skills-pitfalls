#!/usr/bin/env python3
"""Generate static HTML catalog pages from the pitfalls/*.md sources.

Reads every pitfall entry under pitfalls/<category>/<slug>.md, converts the
Markdown (a small fixed subset — headings, blockquote, bullets, fenced code,
inline code, bold, links) to HTML, and writes:

  docs/pitfalls/<category>/<slug>.html   one page per entry (SEO landing pages)
  docs/pitfalls/index.html               catalog index grouped by category
  docs/sitemap.xml                       all site URLs
  docs/robots.txt                        points crawlers at the sitemap

The output is committed so GitHub Pages serves it with no build step.
Re-run after adding or editing entries:  python3 tools/build_catalog.py
"""

import glob
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SITE = "https://livlign.github.io/claude-skills-pitfalls"
GITHUB_BLOB = "https://github.com/livlign/claude-skills-pitfalls/blob/main"

CATEGORIES = {
    "tool-constraints": "Hidden limits on a single tool — schema-enforced caps and undocumented ceilings.",
    "tool-behaviors":   "Undocumented runtime behaviors — prerequisite calls, path resolution, side effects.",
    "cross-platform":   "Divergences across Claude.ai, Claude Code, and Claude Desktop.",
    "environment":      "Sandbox, filesystem, and network constraints.",
    "skill-structure":  "SKILL.md authoring traps — file paths, references, hot-reload.",
}

# repo-relative paths of every entry we generate (for link rewriting)
MD_SET = set()


def md_files():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "pitfalls", "**", "*.md"), recursive=True)):
        base = os.path.basename(f)
        if base in ("README.md", "_template.md"):
            continue
        out.append(f)
    return out


def rewrite_href(href, cur_md_relpath):
    """Map a Markdown link target to its place in the generated HTML site."""
    if href.startswith(("http://", "https://", "#", "mailto:")):
        return href
    if href == "../":  # category/back-to-all-categories link → catalog index
        return "../index.html"
    if href.endswith(".md"):
        cur_dir = os.path.dirname(cur_md_relpath)
        target = os.path.normpath(os.path.join(cur_dir, href))  # repo-relative
        if target in MD_SET:
            return href[:-3] + ".html"
        # points at something we don't publish (e.g. matrix/) → GitHub source
        return f"{GITHUB_BLOB}/{target}"
    return href


def _spans(seg):
    """Render inline code and bold within already-HTML-escaped text."""
    parts = re.split(r"(`[^`]+`)", seg)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) >= 2:
            out.append("<code>" + p[1:-1] + "</code>")  # contents already escaped
        else:
            out.append(re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", p))
    return "".join(out)


def inline(text, cur_md_relpath):
    """Inline Markdown → HTML for one block of text (no block structure).

    Links are handled before code/bold so a link whose label contains inline
    code (e.g. [`foo.md`](foo.md)) is matched as a whole, then its label is
    span-rendered.
    """
    esc = html.escape(text)
    out = []
    last = 0
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", esc):
        out.append(_spans(esc[last:m.start()]))
        label = _spans(m.group(1))
        href = rewrite_href(html.unescape(m.group(2)), cur_md_relpath)
        out.append(f'<a href="{html.escape(href)}">{label}</a>')
        last = m.end()
    out.append(_spans(esc[last:]))
    return "".join(out)


def convert(md, cur_md_relpath):
    """Convert the full Markdown body (after the H1) to HTML blocks."""
    lines = md.split("\n")
    html_out = []
    i = 0
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            html_out.append("</ul>")
            in_list = False

    while i < len(lines):
        line = lines[i]

        # fenced code
        if line.strip().startswith("```"):
            close_list()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1  # skip closing fence
            html_out.append("<pre><code>" + "\n".join(buf) + "</code></pre>")
            continue

        # blank line
        if not line.strip():
            close_list()
            i += 1
            continue

        # headings
        m = re.match(r"^(#{2,4})\s+(.*)$", line)
        if m:
            close_list()
            level = len(m.group(1))
            html_out.append(f"<h{level}>{inline(m.group(2), cur_md_relpath)}</h{level}>")
            i += 1
            continue

        # blockquote (may span multiple lines)
        if line.startswith(">"):
            close_list()
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            html_out.append("<blockquote><p>" + inline(" ".join(buf), cur_md_relpath) + "</p></blockquote>")
            continue

        # bullet list
        if re.match(r"^- \s*", line) or line.startswith("- "):
            if not in_list:
                html_out.append("<ul>")
                in_list = True
            item = line[2:]
            html_out.append("<li>" + inline(item, cur_md_relpath) + "</li>")
            i += 1
            continue

        # paragraph (gather until blank / block boundary)
        close_list()
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", ">", "- ", "```")):
            buf.append(lines[i])
            i += 1
        html_out.append("<p>" + inline(" ".join(buf), cur_md_relpath) + "</p>")

    close_list()
    return "\n".join(html_out)


def parse_entry(path):
    raw = open(path, encoding="utf-8").read()
    relpath = os.path.relpath(path, ROOT)
    category = relpath.split(os.sep)[1]
    slug = os.path.splitext(os.path.basename(path))[0]

    lines = raw.split("\n")
    title = ""
    summary = ""
    body_start = 0
    for idx, ln in enumerate(lines):
        if ln.startswith("# "):
            title = ln[2:].strip()
            body_start = idx + 1
            break
    # first blockquote after the title = summary / meta description
    for ln in lines[body_start:]:
        if ln.startswith(">"):
            summary = re.sub(r"^>\s?", "", ln).strip()
            break
        if ln.startswith("# "):
            break

    tier = ""
    mt = re.search(r"Verification tier:\*\*\s*([a-z\- ]+)", raw)
    if mt:
        tier = mt.group(1).strip().split("|")[0].strip()

    body_md = "\n".join(lines[body_start:])
    body_html = convert(body_md, relpath)
    return {
        "path": relpath, "category": category, "slug": slug,
        "title": title, "summary": summary, "tier": tier,
        "body_html": body_html,
    }


def strip_md_inline(s):
    """Plain text for <title>/meta/description: drop backticks, bold, links."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = s.replace("`", "").replace("**", "")
    return s.strip()


def page_html(e):
    rel_to_docs = "../.."   # docs/pitfalls/<cat>/<slug>.html → docs/
    canonical = f"{SITE}/pitfalls/{e['category']}/{e['slug']}.html"
    title_txt = strip_md_inline(e["title"])
    desc_txt = strip_md_inline(e["summary"]) or title_txt
    cat_label = e["category"]
    tier_class = "tier-" + e["tier"] if e["tier"] in ("verified", "schema-only", "stub") else ""
    tier_badge = f'<span class="tier {tier_class}">{e["tier"]}</span>' if e["tier"] else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title_txt)} — Claude skills pitfalls</title>
<meta name="description" content="{html.escape(desc_txt)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title_txt)}">
<meta property="og:description" content="{html.escape(desc_txt)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel_to_docs}/catalog.css">
</head>
<body>
<div class="wrap">
  <header class="masthead">
    <span class="site"><a href="{rel_to_docs}/index.html">claude-skills-pitfalls</a></span>
    <span class="crumb"><a href="../index.html">catalog</a> / {html.escape(cat_label)} / {html.escape(e['slug'])}</span>
  </header>
  <main>
    <h1>{inline(e['title'], e['path'])}</h1>
    {tier_badge}
    {e['body_html']}
  </main>
  <footer class="pagefoot">
    <span><a href="../index.html">← All pitfalls</a></span>
    <span><a href="{GITHUB_BLOB}/{e['path']}">Edit this page on GitHub</a></span>
  </footer>
</div>
</body>
</html>
"""


def index_html(entries):
    by_cat = {c: [] for c in CATEGORIES}
    for e in entries:
        by_cat.setdefault(e["category"], []).append(e)
    blocks = []
    for cat, desc in CATEGORIES.items():
        items = sorted(by_cat.get(cat, []), key=lambda x: x["title"].lower())
        rows = []
        for e in items:
            rows.append(
                f'<div class="entry"><a href="{cat}/{e["slug"]}.html">{inline(e["title"], "pitfalls/index.md")}</a>'
                f'<span class="sum">{inline(e["summary"], "pitfalls/index.md")}</span></div>'
            )
        blocks.append(
            f'<section class="cat"><h2>{html.escape(cat)}</h2>'
            f'<p class="desc">{html.escape(desc)}</p>{"".join(rows)}</section>'
        )
    total = len(entries)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Catalog — why Claude skills break across platforms ({total} pitfalls)</title>
<meta name="description" content="A browsable catalog of {total} documented ways Claude skills (SKILL.md) silently break across Claude Code, Claude.ai, and Claude Desktop — with causes, fixes, and reproductions.">
<link rel="canonical" href="{SITE}/pitfalls/index.html">
<meta property="og:type" content="website">
<meta property="og:title" content="Claude skills pitfalls — catalog">
<meta property="og:description" content="{total} documented ways Claude skills silently break across platforms, with causes and fixes.">
<meta property="og:url" content="{SITE}/pitfalls/index.html">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../catalog.css">
</head>
<body>
<div class="wrap">
  <header class="masthead">
    <span class="site"><a href="../index.html">claude-skills-pitfalls</a></span>
    <span class="crumb"><a href="../index.html">compatibility checker</a></span>
  </header>
  <main>
    <h1>Why Claude skills break across platforms</h1>
    <p class="lede">A catalog of {total} documented runtime pitfalls when writing Claude skills (<code>SKILL.md</code>) — hidden tool limits, cross-platform differences, sandbox constraints, and authoring traps. Each entry has a cause, a fix, and a verification label.</p>
    {"".join(blocks)}
  </main>
  <footer class="pagefoot">
    <span><a href="../index.html">← Compatibility checker</a></span>
    <span><a href="https://github.com/livlign/claude-skills-pitfalls">Source on GitHub</a></span>
  </footer>
</div>
</body>
</html>
"""


def sitemap(entries):
    urls = [f"{SITE}/", f"{SITE}/pitfalls/index.html"]
    urls += [f"{SITE}/pitfalls/{e['category']}/{e['slug']}.html" for e in entries]
    items = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'


def main():
    files = md_files()
    for f in files:
        MD_SET.add(os.path.relpath(f, ROOT))
    entries = [parse_entry(f) for f in files]

    for e in entries:
        outdir = os.path.join(DOCS, "pitfalls", e["category"])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, e["slug"] + ".html"), "w", encoding="utf-8") as fh:
            fh.write(page_html(e))

    with open(os.path.join(DOCS, "pitfalls", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index_html(entries))
    with open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(sitemap(entries))
    with open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")

    print(f"Generated {len(entries)} entry pages + index + sitemap + robots.txt")


if __name__ == "__main__":
    main()
