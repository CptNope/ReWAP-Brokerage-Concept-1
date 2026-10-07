"""Generates src/pages/03-color.html from tokens/palette.json (run tools/palette.py first)."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
D = json.load(open(os.path.join(ROOT, 'tokens/palette.json')))
C, T = D['colors'], D['contrast']
NAMES = {'night': 'Night', 'navy': 'Registry Navy', 'navy-700': 'Navy 700', 'navy-500': 'Harbor', 'navy-200': 'Fog', 'navy-100': 'Mist',
         'bronze-700': 'Bronze Deep', 'bronze': 'Bronze', 'bronze-300': 'Bronze Light', 'bronze-100': 'Bronze Tint',
         'gallery': 'Gallery', 'plaster': 'Plaster', 'limestone': 'Limestone', 'hairline': 'Hairline', 'granite': 'Granite',
         'slate': 'Slate', 'ink': 'Ink', 'success': 'Success', 'warning': 'Warning', 'warning-fill': 'Warning Fill', 'error': 'Error', 'white': 'White'}
LIGHT_TEXT = {'night', 'navy', 'navy-700', 'navy-500', 'bronze-700', 'slate', 'ink', 'success', 'warning', 'error'}
def sw(k, tall=False, note=None):
    v = C[k]; fg = '#FAFAF9' if k in LIGHT_TEXT else ('#000000' if k == 'granite' else '#0C1827')
    border = ' bordered' if k in ('gallery', 'white', 'plaster', 'hairline', 'limestone', 'navy-100', 'bronze-100') else ''
    return (f'<div class="swatch"><div class="swatch-chip{" tall" if tall else ""}{border}" style="background:{v["hex"]};color:{fg}">--c-{k}</div>'
            f'<div class="swatch-info"><span class="swatch-name">{NAMES[k]}</span>'
            f'<span class="swatch-values"><button type="button" data-copy="{v["oklch"]}">{v["oklch"]}</button><br>'
            f'<button type="button" data-copy="{v["hex"]}">{v["hex"]}</button></span>'
            f'<span class="swatch-role">{note or v["role"]}</span></div></div>')
def section(code, id_, title, intro, body, alt=False, dark=False):
    cls = 'section' + (' alt' if alt else '') + (' on-dark' if dark else '')
    return (f'<section class="{cls}" id="{id_}" aria-labelledby="{id_}-h"><div class="wrap"><div class="section-head"><span class="code">{code}</span>'
            f'<h2 id="{id_}-h">{title}</h2><p>{intro}</p></div>{body}</div></section>\n')
rows = []
for t in T:
    f, b = C[t['fg']], C[t['bg']]
    cls = 'pass' if t['ratio'] >= 4.5 else ('limit' if t['ratio'] >= 3 else '')
    rows.append(f'<tr><td><span class="pair-chip" style="background:{b["hex"]};color:{f["hex"]}" aria-hidden="true">Aa</span></td>'
                f'<td>{NAMES[t["fg"]]} on {NAMES[t["bg"]]}</td><td class="r num">{t["ratio"]:.2f} : 1</td><td class="{cls}">{t["use"]}</td></tr>')
html = f'''<!--
title: Color
slug: color
num: 03
description: The REWAP color system in OKLCH with hex fallbacks: Registry Navy, Bronze, gallery neutrals, interactive and status colors, proportions, contrast pairs and tokens.
-->
<header class="opener">
  <div class="wrap grid">
    <p class="opener-num" aria-hidden="true">03</p>
    <div class="opener-head">
      <h1>Color</h1>
      <p class="lead">Two colors from the mark, held with restraint against gallery walls. Navy carries authority; bronze is a signature, not a finish.</p>
    </div>
    <div class="opener-aside"><ul class="toc-inline" aria-label="On this page">
      <li><a href="#approach">Approach</a></li><li><a href="#primary">Primary</a></li><li><a href="#neutrals">Neutrals</a></li><li><a href="#proportion">Proportion</a></li>
      <li><a href="#interactive">Interactive &amp; status</a></li><li><a href="#contrast">Contrast</a></li><li><a href="#tokens">Tokens</a></li></ul></div>
  </div>
</header>
''' + section('3.1', 'approach', 'Away from black and gold',
 'Luxury real estate has a default: black, metallic gold and a serif. REWAP’s own mark points somewhere quieter.',
 '''<div class="body-cols"><div class="main stack">
 <p>The logo is navy and bronze, not black and gold. The system keeps that distinction and widens it. <strong>Registry Navy</strong>, drawn from the W, does the work black usually does: text, statement fields, primary actions. <strong>Bronze</strong> is reserved for the mark, for 1 px rules and for a few moments of emphasis; it never fills a button and never becomes metallic outside the logo itself.</p>
 <p>Grounds are gallery neutrals, measured to sit just off white with almost no chroma, so photography and property data carry the color. The names come from the materials of New England civic buildings: granite, slate, limestone, plaster.</p>
 <p>Every value is defined in OKLCH so lightness steps are perceptually even and contrast is predictable. Hex values are the fallback for older browsers and for vendors.</p>
 </div></div>''') + section('3.2', 'primary', 'Primary: navy and bronze', 'Click any value to copy it.',
 '<div class="plates four">' + ''.join(sw(k, True) for k in ['night', 'navy', 'navy-700', 'navy-500']) + '</div>'
 '<div class="plates four mt-7">' + ''.join(sw(k, True) for k in ['bronze-700', 'bronze', 'bronze-300', 'bronze-100']) + '</div>'
 '<div class="plates four mt-7">' + ''.join(sw(k) for k in ['navy-200', 'navy-100']) + '</div>', alt=False) + section('3.3', 'neutrals', 'Neutrals and text',
 'Surfaces stay quiet so content leads. Text is navy-tinted ink, never pure black.',
 '<div class="plates four">' + ''.join(sw(k) for k in ['gallery', 'plaster', 'limestone', 'hairline']) + '</div>'
 '<div class="plates four mt-7">' + ''.join(sw(k) for k in ['ink', 'slate', 'granite']) + '</div>', alt=True) + section('3.4', 'proportion', 'Proportion',
 'How much of each color a typical page shows. Bronze stays under five percent; if a layout needs more, it needs a photograph instead.',
 '''<div class="ratio-bar" role="img" aria-label="Gallery 62 percent, Plaster 14 percent, Registry Navy 16 percent, Ink 5 percent, Bronze 3 percent">
 <span style="flex:62;background:#FAFAF9;color:#545C66">Gallery 62%</span><span style="flex:14;background:#F4F2EF;color:#545C66">Plaster 14%</span>
 <span style="flex:16;background:#17283F;color:#FAFAF9">Navy 16%</span><span style="flex:5;background:#192331;color:#FAFAF9">Ink</span><span style="flex:3;background:#AD7E50"></span></div>
 <p class="small mt-6">Ink 5% and Bronze 3% complete the bar. Statement pages such as a founder letter may invert this, running navy as the dominant field.</p>''') + section('3.5', 'interactive', 'Interactive and status',
 'Interaction is navy with a bronze signal; status colors are used only for status.',
 '<ul class="spec-list"><li><b>Links</b><span>Registry Navy text with a 1 px Bronze underline; the underline turns navy on hover.</span></li>'
 '<li><b>Primary action</b><span>Registry Navy fill, Gallery text. Hover Navy 700; pressed Night.</span></li>'
 '<li><b>Focus</b><span>2 px Bronze Deep outline, 3 px offset (Bronze Light on navy). Never removed.</span></li>'
 '<li><b>Input borders</b><span>Granite (3.76 : 1 against Gallery) to meet non-text contrast.</span></li>'
 '<li><b>Selected</b><span>Mist fill with Harbor border for chips and rows.</span></li></ul>'
 '<div class="plates four mt-7">' + ''.join(sw(k) for k in ['success', 'warning', 'warning-fill', 'error']) + '</div>', alt=True) + section('3.6', 'contrast', 'Contrast pairs',
 'Ratios computed from the sRGB values (WCAG 2.2). Body text requires 4.5 : 1; large text and UI components 3 : 1.',
 '<div class="scroll-x"><table class="data-table"><thead><tr><th scope="col">Sample</th><th scope="col">Pair</th><th scope="col" class="r">Ratio</th><th scope="col">Cleared for</th></tr></thead><tbody>'
 + ''.join(rows) + '</tbody></table></div><p class="note mt-6">Bronze on Gallery (3.42 : 1) is cleared for rules, large display numerals and the mark only. Small bronze text uses Bronze Deep.</p>') + section('3.7', 'tokens', 'Tokens',
 'Primitives name the color; semantic tokens name the job. Components only ever reference semantic tokens.',
 '''<div class="scroll-x"><table class="data-table"><thead><tr><th scope="col">Semantic token</th><th scope="col">Resolves to</th><th scope="col">Used for</th></tr></thead><tbody>
 <tr><td><code>--surface-page</code></td><td><code>--c-gallery</code></td><td>Page ground</td></tr>
 <tr><td><code>--surface-alt</code></td><td><code>--c-plaster</code></td><td>Alternating sections, plates</td></tr>
 <tr><td><code>--surface-statement</code></td><td><code>--c-navy</code></td><td>Statement rooms, CTA bands</td></tr>
 <tr><td><code>--text</code></td><td><code>--c-ink</code></td><td>Body copy</td></tr>
 <tr><td><code>--text-secondary</code></td><td><code>--c-slate</code></td><td>Captions, metadata</td></tr>
 <tr><td><code>--accent</code></td><td><code>--c-bronze</code></td><td>Rules, numerals, underline</td></tr>
 <tr><td><code>--accent-text</code></td><td><code>--c-bronze-700</code></td><td>Bronze text on light</td></tr>
 <tr><td><code>--control-border</code></td><td><code>--c-granite</code></td><td>Inputs, outlined controls</td></tr>
 <tr><td><code>--focus</code></td><td><code>--c-bronze-700</code></td><td>Focus outline</td></tr>
 </tbody></table></div>
 <p class="small mt-6">Files: <a href="{{root}}assets/css/tokens.css">tokens.css</a> · <a href="{{root}}tokens/tokens.json">tokens.json</a> (W3C design tokens) · <a href="{{root}}tokens/theme.json">theme.json</a> (WordPress block theme draft).</p>''')
open(os.path.join(ROOT, 'src/pages/03-color.html'), 'w').write(html)
print('ok')
