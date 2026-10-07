"""Assemble the static brand book from src/pages/*.html fragments.

Each fragment starts with a front-matter block:
<!--
title: The Mark
slug: logo
num: 02
description: ...
-->
Placeholders: {{root}} resolves to the relative path to the site root.
Run: python3 tools/build_site.py
"""
import os, re, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'src/pages')
SITE = 'https://cptnope.github.io/ReWAP-Brokerage-Concept-1/'

CHAPTERS = [
    ('01', 'essence', 'Brand Essence'),
    ('02', 'logo', 'The Mark'),
    ('03', 'color', 'Color'),
    ('04', 'typography', 'Typography'),
    ('05', 'photography', 'Art Direction'),
    ('06', 'layout', 'Layout'),
    ('07', 'interface', 'Interface'),
    ('08', 'motion', 'Motion'),
    ('09', 'standards', 'Build Standards'),
]

ICON_DOWN = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3.5 6l4.5 4.5L12.5 6"/></svg>'
ARROW = '<svg class="arrow" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'


def parse(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'\s*<!--(.*?)-->\s*', raw, re.S)
    meta = {}
    for line in m.group(1).strip().splitlines():
        k, _, v = line.partition(':')
        meta[k.strip()] = v.strip()
    return meta, raw[m.end():]


def href(root, slug):
    return f'{root}index.html' if slug == 'index' else f'{root}book/{slug}.html'


def masthead(root, current):
    items = []
    for num, slug, title in CHAPTERS:
        cur = ' aria-current="page"' if slug == current else ''
        items.append(f'<li><a href="{href(root, slug)}"{cur}><span class="num">{num}</span>{title}</a></li>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap masthead-inner">
    <a class="masthead-logo" href="{root}index.html" aria-label="REWAP Brokerage brand standards, home">
      <picture><source media="(max-width: 47.99rem)" srcset="{root}assets/logo/derived/rewap-wordmark-full-color.svg" width="228" height="66"><img src="{root}assets/logo/rewap-logo-full-color.svg" alt="REWAP Brokerage" width="480" height="168"></picture>
    </a>
    <p class="masthead-title"><b>Brand Standards</b>Concept 1 · Draft for review</p>
    <details class="book-nav">
      <summary>Chapters {ICON_DOWN}</summary>
      <nav aria-label="Brand book chapters"><ol>{"".join(items)}</ol></nav>
    </details>
  </div>
</header>'''


def footer(root, current):
    idx = [c[1] for c in CHAPTERS].index(current) if current in [c[1] for c in CHAPTERS] else -1
    pager = ''
    if idx >= 0:
        prev = CHAPTERS[idx - 1] if idx > 0 else None
        nxt = CHAPTERS[idx + 1] if idx < len(CHAPTERS) - 1 else None
        L = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M14 8H3M7 4L3 8l4 4"/></svg>'
        R = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'
        a = (f'<a href="{href(root, prev[1])}" rel="prev" aria-label="Previous chapter: {prev[2]}"><span class="dir t">{L}{prev[2]}</span><span class="n">Chapter {prev[0]}</span></a>'
             if prev else f'<a href="{root}index.html"><span class="dir t">{L}Contents</span><span class="n">Cover</span></a>')
        b = (f'<a href="{href(root, nxt[1])}" rel="next" aria-label="Next chapter: {nxt[2]}"><span class="dir t">{nxt[2]}{R}</span><span class="n">Chapter {nxt[0]}</span></a>'
             if nxt else f'<a href="{root}index.html"><span class="dir t">Contents{R}</span><span class="n">Cover</span></a>')
        pager = f'<nav class="wrap" aria-label="Chapter navigation"><div class="pager-book">{a}{b}</div></nav>'
    return f'''{pager}
<footer class="site-foot on-dark">
  <div class="wrap">
    <div class="grid">
      <div class="col-a"><img src="{root}assets/logo/rewap-logo-reversed.svg" alt="REWAP Brokerage" width="480" height="168"></div>
      <div class="col-b"><p>REWAP Brokerage LLC<br>652 Park Ave, Worcester, MA 01603<br><a href="tel:+15085097759">508-509-7759</a> · <a href="mailto:hongtran@lehonglaw.com">hongtran@lehonglaw.com</a></p></div>
      <div class="col-c"><p>Concept 1 brand standards, prepared for review by Hong Tran. Not a published identity; marks marked “derived” are pending approval.</p></div>
    </div>
    <div class="fine"><span>Type: Libre Caslon and Public Sans, SIL Open Font License.</span><span>Concept by Jeremy Anderson · jeremyanderson.tech</span></div>
  </div>
</footer>'''


def page(meta, body, root, slug):
    title = meta['title']
    full = 'REWAP Brokerage — Brand Standards' if slug == 'index' else f'{title} — REWAP Brokerage Brand Standards'
    desc = html.escape(meta.get('description', ''))
    url = SITE if slug == 'index' else f'{SITE}book/{slug}.html'
    body = body.replace('{{root}}', root)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#17283F">
<link rel="icon" href="{root}assets/logo/derived/rewap-favicon.svg" type="image/svg+xml">
<link rel="icon" href="{root}assets/logo/png/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{root}assets/logo/png/apple-touch-icon-180.png">
<link rel="preload" href="{root}assets/fonts/libre-caslon-display.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/public-sans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/tokens.css">
<link rel="stylesheet" href="{root}assets/css/book.css">
<script src="{root}assets/js/book.js" defer></script>
</head>
<body>
{masthead(root, slug) if slug != 'index' else '<a class="skip" href="#main">Skip to content</a>'}
<main id="main">
{body}
</main>
{footer(root, slug)}
</body>
</html>
'''


def main():
    os.makedirs(os.path.join(ROOT, 'book'), exist_ok=True)
    for f in sorted(os.listdir(SRC)):
        if not f.endswith('.html'):
            continue
        meta, body = parse(os.path.join(SRC, f))
        slug = meta['slug']
        if slug == 'index':
            out, root = os.path.join(ROOT, 'index.html'), ''
        else:
            out, root = os.path.join(ROOT, 'book', f'{slug}.html'), '../'
        open(out, 'w', encoding='utf-8').write(page(meta, body, root, slug))
        print('built', os.path.relpath(out, ROOT))


if __name__ == '__main__':
    main()
