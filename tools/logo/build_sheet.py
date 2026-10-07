"""Builds assets/logo/rewap-logo-sheet.svg: every logo version on its approved ground, in one SVG."""
import os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
L = os.path.join(ROOT, 'assets/logo')
cells = [
    ('rewap-logo-full-color.svg', '#FFFFFF', 'Full color', 'Default · light grounds'),
    ('rewap-logo-flat.svg', '#F4F2EF', 'Flat two-color', 'Spot color, signage, small sizes'),
    ('rewap-logo-reversed.svg', '#17283F', 'Reversed', 'Registry Navy and Night grounds'),
    ('rewap-logo-reversed-flat.svg', '#0C1827', 'Reversed flat', 'Dark-ground print, embroidery'),
    ('rewap-logo-mono-navy.svg', '#FFFFFF', 'One-color navy', 'Letterhead, legal documents'),
    ('rewap-logo-mono-black.svg', '#FFFFFF', 'One-color black', 'Newsprint, fax, engraving'),
    ('rewap-logo-mono-white.svg', '#4D5F77', 'One-color white', 'Single-ink on dark grounds'),
    ('rewap-logo-mono-bronze.svg', '#FFFFFF', 'One-color bronze', 'Foil, single-ink bronze'),
    ('derived/rewap-emblem-full-color.svg', '#FFFFFF', 'Emblem · derived', 'Pending approval'),
    ('derived/rewap-emblem-reversed.svg', '#17283F', 'Emblem reversed · derived', 'Pending approval'),
    ('derived/rewap-wordmark-full-color.svg', '#FFFFFF', 'Wordmark · derived', 'Pending approval'),
    ('derived/rewap-favicon.svg', '#FFFFFF', 'Favicon tile · derived', 'Pending approval'),
]
CW, CH, PAD, CAP, COLS, GAP = 560, 250, 34, 54, 2, 16
rows = (len(cells) + COLS - 1) // COLS
W = COLS * CW + (COLS + 1) * GAP
H = 120 + rows * (CH + CAP + GAP) + GAP
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="sheet-t">',
       '<title id="sheet-t">REWAP Brokerage logo versions</title>',
       f'<rect width="{W}" height="{H}" fill="#FAFAF9"/>',
       f'<text x="{GAP}" y="58" font-family="Libre Caslon Display, Georgia, serif" font-size="34" fill="#0C1827">REWAP Brokerage · Logo versions</text>',
       f'<text x="{GAP}" y="90" font-family="Public Sans, Arial, sans-serif" font-size="14" fill="#545C66">Concept 1 brand standards · vector masters rebuilt from the supplied artwork · derived marks pending approval</text>']
for i, (f, bg, title, meta) in enumerate(cells):
    src = open(os.path.join(L, f)).read().strip()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    inner = re.sub(r'^<svg[^>]*>', '', src)[:-len('</svg>')]
    inner = re.sub(r'<title[^>]*>.*?</title>', '', inner)
    p = f'c{i}-'
    inner = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m.group(1)})', inner)
    c, r = i % COLS, i // COLS
    x = GAP + c * (CW + GAP); y = 120 + r * (CH + CAP + GAP)
    stroke = ' stroke="#D9D7D3"' if bg in ('#FFFFFF', '#F4F2EF') else ''
    out.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{bg}"{stroke}/>')
    out.append(f'<svg x="{x + PAD}" y="{y + PAD}" width="{CW - 2 * PAD}" height="{CH - 2 * PAD}" viewBox="{vb}" preserveAspectRatio="xMidYMid meet">{inner}</svg>')
    out.append(f'<text x="{x}" y="{y + CH + 24}" font-family="Libre Caslon Text, Georgia, serif" font-style="italic" font-size="16" fill="#0C1827">{title}</text>')
    out.append(f'<text x="{x}" y="{y + CH + 44}" font-family="Public Sans, Arial, sans-serif" font-size="12.5" fill="#545C66">{meta} · {f}</text>')
out.append('</svg>\n')
open(os.path.join(L, 'rewap-logo-sheet.svg'), 'w').write(''.join(out))
print('sheet', W, H)
