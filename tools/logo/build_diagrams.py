"""Construction overlay + clear-space diagram for the brand book, from build_logo.py geometry."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import build_logo as G
ROOT = G.ROOT
B = '#AD7E50'; E = '#B1322D'; N = '#17283F'
VB = "24 2 480 168"
lab = 'font-family="Public Sans, sans-serif" font-size="7.5" font-weight="600" letter-spacing=".4"'
def t(x, y, s, anchor='start', c=E):
    return f'<text x="{x}" y="{y}" fill="{c}" text-anchor="{anchor}" {lab}>{s}</text>'
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" aria-hidden="true"><g fill="none" stroke="{E}" stroke-width=".45">']
for y, name in [(62, 'KEY TOP 62'), (66, 'CAP 66'), (79.9, 'B-CAP 79.9'), (106.1, 'B-BASE 106.1'), (114.6, 'BASE 114.6'), (121.2, 'KEY BASE 121.2')]:
    o.append(f'<path d="M24 {y}H504" stroke-dasharray="2 1.6"/>')
o.append(f'<path d="M{G.CX} 2V170M24 {G.CY}H504" stroke-width=".35"/>')
for rx, ry, sw in G.RINGS:
    o.append(f'<ellipse cx="{G.CX}" cy="{G.CY}" rx="{rx}" ry="{ry}" stroke-dasharray="1 1.2"/>')
o.append(f'<path d="M469.6 62L499.2 91.6L469.6 121.2" stroke-width=".6"/>')
o.append(f'<path d="M129.2 121.1L143.7 93.5L158 121.1" stroke-width=".6"/>')
o.append('</g>')
def call(x, y, n):
    return (f'<g><circle cx="{x}" cy="{y}" r="6.2" fill="{E}"/>'
            f'<text x="{x}" y="{y + 3}" fill="#fff" text-anchor="middle" font-family="Public Sans, sans-serif" font-size="8.4" font-weight="700">{n}</text></g>')
for x, y, n in [(30, 62, 1), (30, 66 + 4, 2), (262, 79.9, 3), (30, 114.6, 4), (30, 121.2 + 4, 5), (G.CX, G.CY, 6), (499.2, 91.6, 7), (158.5, 104, 8)]:
    o.append(call(x, y, n))
o.append('</svg>\n')
open(os.path.join(ROOT, 'assets/img/logo-construction.svg'), 'w').write("".join(o))

# Clear space: unit r = roof height (27.6) — the house in the W is the measure.
r = 27.6
x0, y0, x1, y1 = 28.9, 5.9, 499.2, 166.3
logo = open(os.path.join(ROOT, 'assets/logo/rewap-logo-full-color.svg')).read()
inner = re.sub(r'^<svg[^>]*>', '', logo.strip())[:-6]
vb = f"{x0 - r - 14} {y0 - r - 14} {x1 - x0 + 2 * r + 28} {y1 - y0 + 2 * r + 28}"
c = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-labelledby="cs"><title id="cs">Clear space: one roof unit on every side</title>']
c.append(f'<rect x="{x0 - r}" y="{y0 - r}" width="{x1 - x0 + 2 * r}" height="{y1 - y0 + 2 * r}" fill="#F4F2EF"/>')
c.append(f'<svg x="24" y="2" width="480" height="168" viewBox="{VB}">{inner}</svg>')
c.append(f'<g fill="none" stroke="{B}" stroke-width=".6"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" stroke-dasharray="2 2"/>'
         f'<rect x="{x0 - r}" y="{y0 - r}" width="{x1 - x0 + 2 * r}" height="{y1 - y0 + 2 * r}"/></g>')
# roof unit markers on each side
def roof(cx, cy):
    return (f'<g transform="translate({cx} {cy}) scale(.5)"><path d="M0 -13.8L14.4 13.8H10.3L0 -4L-10.3 13.8H-14.4Z" fill="{B}"/></g>')
c.append(roof(x0 - r / 2, (y0 + y1) / 2) + roof(x1 + r / 2, (y0 + y1) / 2) + roof((x0 + x1) / 2, y0 - r / 2) + roof((x0 + x1) / 2, y1 + r / 2))
c.append(f'<g font-family="Public Sans, sans-serif" font-size="7" font-weight="600" fill="{N}" letter-spacing=".5">'
         f'<text x="{x0 - r}" y="{y0 - r - 5}">CLEAR SPACE = 1 r (ROOF HEIGHT) ON ALL SIDES</text></g>')
c.append('</svg>\n')
open(os.path.join(ROOT, 'assets/img/logo-clearspace.svg'), 'w').write("".join(c))
print('ok')
