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


FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">'
)


def topnav(catalog_href, checker_href):
    return (
        '<nav class="topnav">'
        f'<a class="brand" href="{catalog_href}">claude-skills-pitfalls</a>'
        '<span class="navlinks">'
        f'<a href="{catalog_href}">Catalog</a>'
        f'<a href="{checker_href}">Checker</a>'
        '<a href="https://github.com/livlign/claude-skills-pitfalls">GitHub</a>'
        '</span></nav>'
    )


def tier_badge(tier):
    if not tier:
        return ""
    cls = "tier-" + tier if tier in ("verified", "schema-only", "stub") else ""
    return f'<span class="tier {cls}">{tier}</span>'


def page_html(e, cat_entries, prev_e, next_e):
    canonical = f"{SITE}/pitfalls/{e['category']}/{e['slug']}.html"
    title_txt = strip_md_inline(e["title"])
    desc_txt = strip_md_inline(e["summary"]) or title_txt

    sib = "".join(
        f'<li class="{"current" if s["slug"] == e["slug"] else ""}">'
        f'<a href="{s["slug"]}.html">{html.escape(strip_md_inline(s["title"]))}</a></li>'
        for s in cat_entries
    )
    catnav = "".join(
        f'<li><a href="../index.html#cat-{c}">{c}</a></li>' for c in CATEGORIES
    )

    def navlink(p, cls, label):
        if not p:
            return "<span></span>"
        return (
            f'<a class="{cls}" href="../{p["category"]}/{p["slug"]}.html">'
            f'<span class="lbl">{label}</span>{html.escape(strip_md_inline(p["title"]))}</a>'
        )

    prevnext = ""
    if prev_e or next_e:
        prevnext = (
            '<nav class="prevnext">'
            + navlink(prev_e, "pv", "Previous")
            + navlink(next_e, "nx", "Next")
            + "</nav>"
        )

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
{FONTS}
<link rel="stylesheet" href="../../catalog.css">
</head>
<body>
{topnav("../index.html", "../../index.html")}
<div class="wrap">
  <div class="layout">
    <main>
      <p class="crumb"><a href="../index.html">catalog</a> / {html.escape(e['category'])}</p>
      <h1>{inline(e['title'], e['path'])}</h1>
      {tier_badge(e['tier'])}
      {e['body_html']}
      {prevnext}
      <footer class="pagefoot">
        <span><a href="../index.html">← All pitfalls</a></span>
        <span><a href="{GITHUB_BLOB}/{e['path']}">Edit this page on GitHub</a></span>
      </footer>
    </main>
    <aside class="sidebar">
      <p class="side-title">{html.escape(e['category'])}</p>
      <ul>{sib}</ul>
      <p class="side-title">Categories</p>
      <ul>{catnav}</ul>
    </aside>
  </div>
</div>
</body>
</html>
"""


# Client-side semantic search. Substring search works immediately; once the
# embedding model finishes loading (lazily, on first focus of the box) queries
# are ranked by cosine similarity of all-MiniLM-L6-v2 embeddings. If the model
# can't load (offline / CDN blocked), it falls back to substring search.
SEARCH_JS = r"""
(function(){
  var q=document.getElementById('q');
  var statusEl=document.getElementById('searchstatus');
  var results=document.getElementById('results');
  var nr=document.getElementById('noresults');
  var chips=document.querySelector('.chips');
  var cats=[].slice.call(document.querySelectorAll('.cat'));
  var data=JSON.parse(document.getElementById('searchdata').textContent);
  data.forEach(function(d){ d.lc=d.tx.toLowerCase(); });

  function browse(){
    cats.forEach(function(c){ c.style.display=''; });
    chips.style.display=''; results.style.display='none'; results.innerHTML=''; nr.style.display='none';
  }
  function show(hits, semantic){
    cats.forEach(function(c){ c.style.display='none'; });
    chips.style.display='none';
    if(!hits.length){ results.style.display='none'; nr.style.display=''; return; }
    nr.style.display='none'; results.style.display='';
    results.innerHTML=hits.map(function(h){
      var sc = semantic ? '<span class="score">'+Math.round(h.score*100)+'%</span>' : '';
      return '<div class="entry"><div class="row"><a href="'+h.d.href+'">'+h.d.ht+'</a>'+sc+'</div><span class="sum">'+h.d.hs+'</span></div>';
    }).join('');
  }
  function lexical(v){
    return data.map(function(d){ return {d:d, score:(d.lc.indexOf(v)>-1?1:0)}; })
               .filter(function(x){ return x.score>0; });
  }

  var extractor=null, docVecs=null, state='idle'; // idle | loading | ready | failed
  function cos(a,b){ var s=0; for(var i=0;i<a.length;i++) s+=a[i]*b[i]; return s; }

  async function ensureModel(){
    if(state!=='idle') return;
    state='loading';
    statusEl.textContent='Loading semantic model… (~20 MB, first visit only)';
    try{
      var T=await import('https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2');
      T.env.allowLocalModels=false;
      extractor=await T.pipeline('feature-extraction','Xenova/all-MiniLM-L6-v2',{quantized:true});
      statusEl.textContent='Indexing '+data.length+' entries…';
      docVecs=[];
      for(var i=0;i<data.length;i++){
        var o=await extractor(data[i].tx,{pooling:'mean',normalize:true});
        docVecs.push(o.data);
      }
      state='ready';
      statusEl.textContent='Semantic search ready — results ranked by meaning.';
      setTimeout(function(){ if(state==='ready') statusEl.textContent=''; }, 2500);
      if(q.value.trim()) run();
    }catch(err){
      state='failed';
      statusEl.textContent='Semantic model unavailable — using keyword search.';
    }
  }

  async function semantic(v){
    var o=await extractor(v,{pooling:'mean',normalize:true});
    var qv=o.data;
    var scored=data.map(function(d,i){ return {d:d, score:cos(qv,docVecs[i])}; });
    scored.sort(function(a,b){ return b.score-a.score; });
    return scored.filter(function(x){ return x.score>0.22; }).slice(0,15);
  }

  var timer=null;
  async function run(){
    var v=q.value.trim();
    if(!v){ browse(); return; }
    if(state==='ready'){
      try{ show(await semantic(v), true); return; }catch(e){}
    }
    show(lexical(v.toLowerCase()), false);
  }
  q.addEventListener('focus', ensureModel);
  q.addEventListener('input', function(){ clearTimeout(timer); timer=setTimeout(run, 150); });
})();
"""


def index_html(entries):
    by_cat = {c: [] for c in CATEGORIES}
    for e in entries:
        by_cat.setdefault(e["category"], []).append(e)
    for c in by_cat:
        by_cat[c].sort(key=lambda x: x["title"].lower())

    chips = "".join(
        f'<a href="#cat-{c}">{c} ({len(by_cat[c])})</a>'
        for c in CATEGORIES if by_cat.get(c)
    )

    search_records = []
    blocks = []
    for cat, desc in CATEGORIES.items():
        rows = []
        for e in by_cat.get(cat, []):
            rows.append(
                f'<div class="entry">'
                f'<div class="row"><a href="{cat}/{e["slug"]}.html">{inline(e["title"], "pitfalls/index.md")}</a>'
                f'{tier_badge(e["tier"])}</div>'
                f'<span class="sum">{inline(e["summary"], "pitfalls/index.md")}</span></div>'
            )
            search_records.append({
                "href": f'{cat}/{e["slug"]}.html',
                "ht": inline(e["title"], "pitfalls/index.md"),
                "hs": inline(e["summary"], "pitfalls/index.md"),
                # plain text fed to the embedding model
                "tx": f'{strip_md_inline(e["title"])}. {strip_md_inline(e["summary"])} ({cat})',
            })
        blocks.append(
            f'<section class="cat" id="cat-{cat}"><h2>{html.escape(cat)}</h2>'
            f'<p class="desc">{html.escape(desc)}</p>{"".join(rows)}</section>'
        )

    import json
    data_json = json.dumps(search_records, ensure_ascii=False).replace("</", "<\\/")
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
{FONTS}
<link rel="stylesheet" href="../catalog.css">
</head>
<body>
{topnav("index.html", "../index.html")}
<div class="wrap">
  <h1>Why Claude skills break across platforms</h1>
  <p class="lede">A catalog of {total} documented runtime pitfalls when writing Claude skills (<code>SKILL.md</code>) — hidden tool limits, cross-platform differences, sandbox constraints, and authoring traps. Each entry has a cause, a fix, and a verification label.</p>
  <input class="search" id="q" type="search" placeholder="Search by meaning — e.g. “file overwritten without warning”, “permission denied writing”…" autocomplete="off" aria-label="Search pitfalls">
  <span class="searchstatus" id="searchstatus"></span>
  <div class="chips">{chips}</div>
  <div id="results"></div>
  {"".join(blocks)}
  <p class="noresults" id="noresults">No pitfalls match your search.</p>
  <footer class="pagefoot">
    <span><a href="../index.html">← Compatibility checker</a></span>
    <span><a href="https://github.com/livlign/claude-skills-pitfalls">Source on GitHub</a></span>
  </footer>
</div>
<script type="application/json" id="searchdata">{data_json}</script>
<script>{SEARCH_JS}</script>
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

    # group by category (sorted by title) and build a global reading order
    by_cat = {c: [] for c in CATEGORIES}
    for e in entries:
        by_cat.setdefault(e["category"], []).append(e)
    for c in by_cat:
        by_cat[c].sort(key=lambda x: x["title"].lower())
    ordered = []
    for c in CATEGORIES:
        ordered.extend(by_cat.get(c, []))

    for i, e in enumerate(ordered):
        prev_e = ordered[i - 1] if i > 0 else None
        next_e = ordered[i + 1] if i < len(ordered) - 1 else None
        outdir = os.path.join(DOCS, "pitfalls", e["category"])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, e["slug"] + ".html"), "w", encoding="utf-8") as fh:
            fh.write(page_html(e, by_cat[e["category"]], prev_e, next_e))

    with open(os.path.join(DOCS, "pitfalls", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index_html(entries))
    with open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(sitemap(entries))
    with open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")

    print(f"Generated {len(entries)} entry pages + index + sitemap + robots.txt")


if __name__ == "__main__":
    main()
