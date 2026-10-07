"""Generates src/pages/05-photography.html (shot plates are drawn here as composition diagrams)."""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
L = '#C9D2DD'; B = '#D8B38A'
def frame(w, h, body, label):
    thirds = (f'<g stroke="{L}" stroke-opacity=".28" stroke-width="1"><path d="M{w/3} 0V{h}M{2*w/3} 0V{h}M0 {h/3}H{w}M0 {2*h/3}H{w}"/></g>')
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" preserveAspectRatio="xMidYMid slice">{thirds}'
            f'<g fill="none" stroke="{L}" stroke-width="1.6">{body}</g></svg>')
def sun(x, y, dx, dy):
    return (f'<g stroke="{B}" stroke-width="1.6"><circle cx="{x}" cy="{y}" r="9" fill="none"/>'
            f'<path d="M{x+dx*.25} {y+dy*.25}L{x+dx} {y+dy}" stroke-dasharray="4 4"/></g>')
shots = [
 ('r32', 600, 400, 'Mill façade, raking light',
  sun(560, 40, -120, 90) + '<path d="M0 300H600"/>' + '<path d="M40 300V120H520V300"/>' +
  ''.join(f'<path d="M{x} 280V230Q{x+14} 218 {x+28} 230V280Z" stroke-width="1.1"/><path d="M{x} 200V150Q{x+14} 138 {x+28} 150V200Z" stroke-width="1.1"/>' for x in range(64, 500, 46)) +
  '<path d="M420 120V40H446V120"/>',
  'Brick and granite industrial architecture, adaptive reuse', 'Late afternoon raking light across the façade · 35 mm · eye level · verticals corrected'),
 ('r45', 400, 500, 'Three-decker porches, overcast',
  '<path d="M0 470H400"/><path d="M90 470V140L200 70L310 140V470"/>' + ''.join(f'<path d="M90 {y}H310" stroke-width="1.1"/><path d="M100 {y+70}H190" stroke-width="1"/>' for y in (140, 250, 360)) +
  ''.join(f'<path d="M{x} 140V470" stroke-width=".8"/>' for x in (100, 190)),
  'Neighborhood streetscape: a three-decker as it is lived in', 'Soft overcast · 50 mm · from across the street · no cars cropped mid-frame'),
 ('r169', 640, 360, 'Hill town horizon, morning',
  sun(110, 70, 60, 60) + '<path d="M0 240C120 200 220 230 320 205S520 190 640 215"/><path d="M0 280C160 255 300 280 640 262" stroke-width="1"/>' +
  '<path d="M420 236V200L440 186L460 200V236" stroke-width="1.2"/><path d="M450 194V170" stroke-width="1.2"/>',
  'Regional landscape: every region, equal standing', 'Early morning, low mist · 85 mm compression · a single building for scale'),
 ('r11', 400, 400, 'Material detail',
  ''.join(f'<path d="M0 {y}H400" stroke-width="1"/>' for y in range(40, 400, 40)) + ''.join(f'<path d="M{x + (40 if (y//40)%2 else 0)} {y}V{y+40}" stroke-width="1"/>' for y in range(0, 400, 40) for x in range(0, 400, 80)) +
  '<rect x="150" y="130" width="120" height="150" fill="#0C1827"/><path d="M160 140H260V270H160Z"/><circle cx="246" cy="210" r="5" stroke="#D8B38A"/>',
  'Details and materials: brick, slate, cast iron, original hardware', 'Window light · 100 mm macro · shallow focus on one honest detail'),
 ('r45', 400, 500, 'Founder portrait, environmental',
  '<path d="M0 420H400"/><path d="M40 60H180V420" stroke-width="1"/><path d="M60 80H160V300H60Z" stroke-width="1"/>' +
  '<rect x="214" y="150" width="120" height="270" stroke-dasharray="6 5"/><text x="274" y="290" text-anchor="middle" font-family="Public Sans, sans-serif" font-size="13" font-weight="600" letter-spacing="2" fill="#C9D2DD" stroke="none">SUBJECT</text><path d="M190 360H380" stroke-width="1"/>' + sun(70, 70, 70, 50),
  'Team: environmental portrait at work', 'Available light from a window · 85 mm · subject off-centre, at the desk with documents'),
 ('r32', 600, 400, 'Client at the table, documentary',
  '<path d="M0 290H600"/><path d="M60 290L120 230H480L540 290"/><rect x="230" y="246" width="110" height="34" stroke-width="1.1"/><path d="M250 258H320M250 268H300" stroke-width=".9"/>' +
  '<rect x="150" y="150" width="90" height="82" stroke-dasharray="6 5"/><rect x="360" y="150" width="90" height="82" stroke-dasharray="6 5"/><text x="300" y="200" text-anchor="middle" font-family="Public Sans, sans-serif" font-size="13" font-weight="600" letter-spacing="2" fill="#C9D2DD" stroke="none">HANDS · DOCUMENTS</text>',
  'Clients: hands, documents, attention', 'Documentary, unposed, with written consent · 35 mm · faces optional'),
]
plates = []
for ratio, w, h, label, body, title, meta in shots:
    plates.append(f'<figure class="plate shot"><div class="shot-frame {ratio}">{frame(w, h, body, "Composition diagram: " + label)}</div>'
                  f'<figcaption class="caption"><span class="caption-title">{title}</span><span class="caption-meta">{meta}</span></figcaption></figure>')
elev = ''.join(f'<figure class="plate"><div class="elev" style="aspect-ratio:3/2"><img src="{{{{root}}}}assets/img/elevations/{n}.svg" alt="{a}" width="600" height="400" loading="lazy" style="width:100%;height:100%;object-fit:contain"></div>'
               f'<figcaption class="caption"><span class="caption-title">{t}</span><span class="caption-meta">{m}</span></figcaption></figure>'
               for n, a, t, m in [('triple-decker', 'Line elevation of a three-decker house', 'Three-decker', 'Elevation · placeholder for multi-family listings'),
                                  ('mill', 'Line elevation of a brick mill building', 'Mill conversion', 'Elevation · lofts, commercial, adaptive reuse'),
                                  ('colonial', 'Line elevation of a center-chimney colonial', 'Colonial', 'Elevation · single-family placeholder')])
html = '''<!--
title: Art Direction
slug: photography
num: 05
description: REWAP photographic language and commissioning shot list: architecture, Massachusetts regions, homes, streetscapes, materials, clients and team, plus the elevation drawing set and caption system.
-->
<header class="opener">
  <div class="wrap grid">
    <p class="opener-num" aria-hidden="true">05</p>
    <div class="opener-head">
      <h1>Art Direction</h1>
      <p class="lead">Photograph buildings the way an architect would and people the way a documentary photographer would. Nothing staged, nothing sold.</p>
    </div>
    <div class="opener-aside"><ul class="toc-inline" aria-label="On this page">
      <li><a href="#principles">Principles</a></li><li><a href="#shotlist">Shot list</a></li><li><a href="#light">Light and grade</a></li><li><a href="#people">People</a></li>
      <li><a href="#avoid">Avoid</a></li><li><a href="#elevations">Elevations</a></li><li><a href="#captions">Captions</a></li><li><a href="#crops">Crops</a></li></ul></div>
  </div>
</header>

<section class="section" id="principles" aria-labelledby="principles-h"><div class="wrap">
  <div class="section-head"><span class="code">5.1</span><h2 id="principles-h">Principles</h2>
  <p>REWAP has no photography library yet. This chapter is the brief for commissioning one; no stock or generated image stands in for it.</p></div>
  <ul class="spec-list">
    <li><b>Observe, do not stage</b><span>Real buildings, real streets, real light. The photographer waits for the scene instead of arranging it.</span></li>
    <li><b>Architecture first</b><span>Straight verticals, considered frames, the building as the subject. Shoot from the sidewalk a buyer would stand on.</span></li>
    <li><b>Every region</b><span>The Berkshires to the Cape, Merrimack Valley to the South Coast. The library is balanced by region before it is balanced by price.</span></li>
    <li><b>Places, not people</b><span>Neighborhood images show buildings, streets, parks and civic life without implying who lives there. This is Fair Housing practice, not only taste.</span></li>
    <li><b>Quiet over spectacular</b><span>An overcast morning on a three-decker porch beats a sunset drone shot. Restraint is the luxury.</span></li>
  </ul>
</div></section>

<section class="section alt" id="shotlist" aria-labelledby="shotlist-h"><div class="wrap">
  <div class="section-head"><span class="code">5.2</span><h2 id="shotlist-h">Commissioning shot list</h2>
  <p>Composition diagrams for the first commission. Thirds grid, light direction in bronze. Each plate carries the brief a photographer needs.</p></div>
  <div class="plates three lead-first">''' + ''.join(plates) + '''</div>
  <p class="note mt-6">Diagrams indicate composition and light only. Commission locally, with releases for every identifiable person and property owner permission where required.</p>
</div></section>

<section class="section" id="light" aria-labelledby="light-h"><div class="wrap">
  <div class="section-head"><span class="code">5.3</span><h2 id="light-h">Light and grade</h2><p>One look across every photographer, so the library reads as one body of work.</p></div>
  <ul class="spec-list">
    <li><b>Light</b><span>Overcast, early morning or late raking light. No midday hard shadows on façades, no twilight “glow” interiors.</span></li>
    <li><b>Color</b><span>Natural and slightly cool in the shadows; whites stay white. No HDR halos, sky replacement, fake fires in fireplaces or virtual staging without a clear label.</span></li>
    <li><b>Geometry</b><span>Verticals corrected in camera or post. Horizons level. Interiors shot at chest height, never from the ceiling corner.</span></li>
    <li><b>Interiors</b><span>Real rooms, tidied, with daylight. Lamps off unless they are the subject.</span></li>
  </ul>
</div></section>

<section class="section alt" id="people" aria-labelledby="people-h"><div class="wrap">
  <div class="section-head"><span class="code">5.4</span><h2 id="people-h">Clients and team</h2><p>People appear as themselves, doing real work, with consent.</p></div>
  <ul class="spec-list">
    <li><b>Team portraits</b><span>Environmental, at a desk, in the office or on a street the person knows. Available window light, 4:5 vertical, subject off-centre. One background family for the whole team.</span></li>
    <li><b>Founder</b><span>Hong Tran photographed at work with documents; authority shown through attention, not pose.</span></li>
    <li><b>Clients</b><span>Documentary, unposed and only with written consent. Hands, papers, a doorway, a walk-through. Faces are optional.</span></li>
    <li><b>Affiliated teams</b><span>Teams such as The Oberdorfer Group may keep their own portrait style; REWAP pages present it as theirs.</span></li>
  </ul>
</div></section>

<section class="section" id="avoid" aria-labelledby="avoid-h"><div class="wrap">
  <div class="section-head"><span class="code">5.5</span><h2 id="avoid-h">Avoid, and why</h2><p>These images say “template.” Each one undermines the brand’s claim to candor.</p></div>
  <div class="scroll-x"><table class="pairs"><thead><tr><th scope="col">Never</th><th scope="col">Because</th></tr></thead><tbody>
    <tr><td>Keys handed over</td><td>A cliché that claims a closing instead of showing care.</td></tr>
    <tr><td>Family on a sofa</td><td>Staged, and it tells visitors who a home is “for.”</td></tr>
    <tr><td>Handshakes</td><td>Deals are made in documents, not grips.</td></tr>
    <tr><td>Aerial subdivisions</td><td>Generic, placeless; it could be any state.</td></tr>
    <tr><td>Stock skylines</td><td>The logo already carries the skyline. Photography should be specific.</td></tr>
    <tr><td>AI-generated homes or people</td><td>A brokerage that fabricates images cannot ask to be trusted on facts.</td></tr>
  </tbody></table></div>
</div></section>

<section class="section alt" id="elevations" aria-labelledby="elevations-h"><div class="wrap">
  <div class="section-head"><span class="code">5.6</span><h2 id="elevations-h">Elevation drawings</h2>
  <p>A fine-line drawing set, authored for REWAP. It fills the gap honestly when a photograph does not exist yet: a listing awaiting media, a guide before its shoot, print where photography would muddy.</p></div>
  <div class="plates three">''' + elev + '''</div>
  <ul class="spec-list mt-7">
    <li><b>Line</b><span>Registry Navy, 1.4 px at 600 px width; hairline detail at 0.45–0.7. No fills, no shading, no people.</span></li>
    <li><b>Ground</b><span>Always Plaster. Never on photography.</span></li>
    <li><b>Set</b><span>Extend with the building types of each region: Cape, saltbox, Victorian, ranch, row house, storefront block.</span></li>
  </ul>
</div></section>

<section class="section" id="captions" aria-labelledby="captions-h"><div class="wrap">
  <div class="section-head"><span class="code">5.7</span><h2 id="captions-h">Captions, like a wall label</h2>
  <p>Every image carries a caption set like a museum wall label: an italic title, then the facts. It is the system’s quiet signature.</p></div>
  <div class="body-cols"><div class="main">
    <figure class="plate"><div class="elev" style="aspect-ratio:3/2"><img src="{{root}}assets/img/elevations/triple-decker.svg" alt="Line elevation of a three-decker" width="600" height="400" loading="lazy" style="width:100%;height:100%;object-fit:contain"></div>
    <figcaption class="caption"><span class="caption-title">Three-decker, Elm Park area, Worcester</span><span class="caption-meta">Built 1912 · three units · photographed for REWAP, October 2026</span></figcaption></figure>
    <p class="note mt-6">Example caption for illustration. Formula: title (what, where) · facts (year, type) · credit and date.</p>
  </div></div>
</div></section>

<section class="section alt" id="crops" aria-labelledby="crops-h"><div class="wrap">
  <div class="section-head"><span class="code">5.8</span><h2 id="crops-h">Crops and ratios</h2><p>Four ratios cover every surface. Deliver masters at 3000 px on the long edge.</p></div>
  <div class="scroll-x"><table class="data-table"><thead><tr><th scope="col">Ratio</th><th scope="col">Use</th><th scope="col" class="r">Master size</th></tr></thead><tbody>
    <tr><td class="num">3 : 2</td><td>Page heroes, guides, neighborhood headers</td><td class="r num">3000 × 2000</td></tr>
    <tr><td class="num">4 : 3</td><td>Listing cards and galleries (matches most MLS media)</td><td class="r num">3000 × 2250</td></tr>
    <tr><td class="num">4 : 5</td><td>Portraits, vertical details</td><td class="r num">2400 × 3000</td></tr>
    <tr><td class="num">1 : 1</td><td>Social, thumbnails</td><td class="r num">2400 × 2400</td></tr>
  </tbody></table></div>
</div></section>
'''
open(os.path.join(ROOT, 'src/pages/05-photography.html'), 'w').write(html)
print('ok')
