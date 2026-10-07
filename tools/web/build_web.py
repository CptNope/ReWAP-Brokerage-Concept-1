"""Builds the Concept 1 website pages into /site from assets/data/*.json.
Run: python3 tools/web/make_data.py && (cd tools/web && npm i && node build_map.mjs) && python3 tools/web/build_web.py
"""
import json, os, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
D = json.load(open(os.path.join(ROOT, 'assets/data/listings.json')))
M = json.load(open(os.path.join(ROOT, 'assets/data/ma-map.json')))
LST, REG = D['listings'], {r['slug']: r['name'] for r in D['regions']}
SITE_URL = 'https://cptnope.github.io/ReWAP-Brokerage-Concept-1/site/'
esc = html.escape

# ---------------------------------------------------------------- icons
ICONS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-search" viewBox="0 0 20 20"><g fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8.5" cy="8.5" r="5.5"/><path d="M12.6 12.6L17 17"/></g></symbol>
<symbol id="i-heart" viewBox="0 0 20 20"><path d="M10 16.5S3 12.4 3 7.6A3.6 3.6 0 0 1 10 6a3.6 3.6 0 0 1 7 1.6c0 4.8-7 8.9-7 8.9z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></symbol>
<symbol id="i-arrow" viewBox="0 0 16 16"><path d="M2 8h11M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.5"/></symbol>
<symbol id="i-x" viewBox="0 0 16 16"><path d="M4 4l8 8M12 4l-8 8" fill="none" stroke="currentColor" stroke-width="1.5"/></symbol>
<symbol id="i-menu" viewBox="0 0 20 20"><path d="M3 6h14M3 10h14M3 14h14" fill="none" stroke="currentColor" stroke-width="1.5"/></symbol>
<symbol id="i-sliders" viewBox="0 0 20 20"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 6h9M15 6h2M3 14h2M8 14h9"/><circle cx="13.5" cy="6" r="1.8"/><circle cx="6.5" cy="14" r="1.8"/></g></symbol>
<symbol id="i-map" viewBox="0 0 20 20"><path d="M2.5 5l5-2 5 2 5-2v12l-5 2-5-2-5 2zM7.5 3v12M12.5 5v12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></symbol>
<symbol id="i-share" viewBox="0 0 20 20"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M10 13V3M6.5 6.5L10 3l3.5 3.5M4 10v7h12v-7"/></g></symbol>
<symbol id="i-cal" viewBox="0 0 20 20"><g fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="4.5" width="14" height="12"/><path d="M3 8.5h14M7 2.5v4M13 2.5v4"/></g></symbol>
<symbol id="i-chain" viewBox="0 0 12 12"><path d="M3 2l5 4-5 4" fill="none" stroke="currentColor" stroke-width="1.5"/></symbol>
</svg>'''
def icon(n, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} aria-hidden="true"><use href="#i-{n}"/></svg>'

# ---------------------------------------------------------------- helpers
def price(n): return f'${n:,}'
def kprice(n): return f'${n/1e6:.2f}M'.replace('.00M', 'M') if n >= 1e6 else f'${round(n/1000)}k'
def facts(l):
    f = []
    if l['type'] == 'Multi-family': f.append(f"{l['units']} units")
    f += [f"{l['beds']} bd", f"{l['baths']:g} ba", f"{l['sqft']:,} sq ft"]
    if l['lotAcres']: f.append(f"{l['lotAcres']:g} ac")
    return f
def facts_html(l): return '<span class="property-facts clip"><span class="pf">' + ''.join(f'<span>{x}</span>' for x in facts(l)) + '</span></span>'
def lhref(root, l): return f"{root}homes/{l['slug']}.html"
def elev(root, l, alt=''): return f'<img src="{root}../assets/img/elevations/{l["elevation"]}.svg" alt="{esc(alt)}" width="600" height="400" loading="lazy" style="object-fit:contain">'

def card(root, l):
    st = 'open' if l['status'] == 'Open house' else ''
    label = f"Open {l['openHouse']}" if l['openHouse'] else l['status']
    return f'''<article class="property">
  <div class="property-media elev">{elev(root, l)}</div>
  <span class="property-status {st}">{esc(label)}</span>
  <button class="icon-btn property-save" type="button" data-save="{l['id']}" data-label="{esc(l['address'])}" aria-pressed="false" aria-label="Save {esc(l['address'])}">{icon('heart')}</button>
  <div class="property-body">
    <span class="property-price">{price(l['price'])}</span>
    <h3 class="property-address"><a href="{lhref(root, l)}">{esc(l['address'])}, {l['town']}</a></h3>
    {facts_html(l)}
    <span class="property-attrib">{esc(l['office'])} · Sample listing</span>
  </div>
</article>'''

def clusters(listings):
    """Greedy screen-space clustering in map units: a price pin is ~85 x 32 units."""
    out = []
    for l in listings:
        p = M['towns'][l['town']]
        for c in out:
            if abs(c['x'] - p['x']) < 85 and abs(c['y'] - p['y']) < 34:
                c['items'].append(l); n = len(c['items'])
                c['x'] += (p['x'] - c['x']) / n; c['y'] += (p['y'] - c['y']) / n
                break
        else:
            out.append({'x': p['x'], 'y': p['y'], 'items': [l]})
    return out

REGION_POS = {'The Berkshires': (122, 250), 'Pioneer Valley': (275, 182), 'Central': (455, 215), 'MetroWest': (575, 238),
              'Greater Boston': (775, 200), 'North Shore': (735, 92), 'South Shore': (792, 332), 'South Coast': (610, 470), 'Cape & Islands': (895, 470)}
REGION_ANCHOR = {'The Berkshires': 'Berkshire', 'Pioneer Valley': 'Hampshire', 'Central': 'Worcester', 'MetroWest': 'Middlesex',
                 'Greater Boston': 'Suffolk', 'North Shore': 'Essex', 'South Shore': 'Plymouth', 'South Coast': 'Bristol', 'Cape & Islands': 'Barnstable'}
LABEL_NUDGE = {'MetroWest': (-40, 40), 'Greater Boston': (60, -6), 'North Shore': (10, -18), 'Cape & Islands': (20, 46), 'South Shore': (24, 6), 'Central': (0, 30), 'South Coast': (-10, 34)}

def map_plate(root, listings=None, highlight=None, region_labels=False, dot=None, pins=True, label_towns=False, aria='Map of Massachusetts', focus=None):
    W, H = M['width'], M['height']
    vx, vy, vw, vh = 0, 0, W, H
    if focus:
        b = next(c['b'] for c in M['counties'] if c['name'] == focus); pad = 34
        vx, vy = b[0] - pad, b[1] - pad; vw, vh = b[2] - b[0] + 2 * pad, b[3] - b[1] + 2 * pad
        vw = max(vw, vh * 1.25); vx = (b[0] + b[2]) / 2 - vw / 2
    cents = {c['name']: c['c'] for c in M['counties']}
    cs = ''.join(f'<path class="county{" on" if highlight and c["name"] in highlight else ""}" d="{c["d"]}"><title>{c["name"]} County</title></path>' for c in M['counties'])
    labels = ''
    if label_towns:
        labels += ''.join(f'<circle class="town" cx="{p["x"]}" cy="{p["y"]}" r="3"/>' for t, p in M['towns'].items())
    if region_labels:
        for n, (x, y) in REGION_POS.items():
            labels += f'<text class="region-label" x="{x}" y="{y}" text-anchor="middle">{esc(n)}</text>'
    overlay = ''
    if pins and listings:
        for c in clusters(listings):
            ids = ','.join(l['id'] for l in c['items']); n = len(c['items'])
            lab = kprice(c['items'][0]['price']) if n == 1 else f'{n} homes'
            al = f"{price(c['items'][0]['price'])}, {esc(c['items'][0]['address'])}, {c['items'][0]['town']}" if n == 1 else f"{n} homes near {c['items'][0]['town']}"
            prices = ','.join(kprice(l['price']) for l in c['items'])
            overlay += (f'<button class="pin{" cluster" if n > 1 else ""}" type="button" data-ids="{ids}" data-prices="{prices}" data-near="{c["items"][0]["town"]}" '
                        f'style="left:{c["x"]/W*100:.2f}%;top:{c["y"]/H*100:.2f}%" aria-label="{al}">{lab}</button>')
    if dot:
        p = M['towns'][dot]
        overlay += f'<span class="dot" style="left:{(p["x"]-vx)/vw*100:.2f}%;top:{(p["y"]-vy)/vh*100:.2f}%" aria-hidden="true"></span>'
    lbl = ''
    if focus:
        lbl = ''
    return (f'<div class="map"><div class="map-frame" style="aspect-ratio:{vw:.1f} / {vh:.1f}"><svg class="base" viewBox="{vx:.1f} {vy:.1f} {vw:.1f} {vh:.1f}" role="img" aria-label="{esc(aria)}">{cs}'
            f'<path class="inner" d="{M["inner"]}" vector-effect="non-scaling-stroke"/><path class="outline" d="{M["state"]}" vector-effect="non-scaling-stroke"/>{labels}{lbl}</svg>{overlay}</div>'
            f'<span class="map-attrib">Boundaries: U.S. Census Bureau</span></div>')

NAV = [('Buy', 'search.html'), ('Sell', 'index.html#disciplines'), ('Invest', 'index.html#disciplines'), ('Communities', 'communities/worcester.html'),
       ('Market', 'index.html#market'), ('The Firm', 'index.html#firm')]

def head(root, current):
    items = ''.join(f'<li><a href="{root}{h}"{" aria-current=\"page\"" if n == current else ""}>{n}</a></li>' for n, h in NAV)
    sheet = ''.join(f'<li><a href="{root}{h}">{n}</a></li>' for n, h in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
{ICONS}
<div class="concept-bar"><div class="wrap"><span>Concept 1 website · every listing, figure and address is fictional sample data</span><a href="{root}../index.html">Back to the brand standards</a></div></div>
<header class="site-head">
  <div class="wrap">
    <a class="site-logo" href="{root}index.html" aria-label="REWAP Brokerage, home"><picture><source media="(max-width: 47.99rem)" srcset="{root}../assets/logo/derived/rewap-wordmark-full-color.svg" width="228" height="66"><img src="{root}../assets/logo/rewap-logo-full-color.svg" alt="REWAP Brokerage" width="480" height="168"></picture></a>
    <nav class="site-nav" aria-label="Primary"><ul>{items}</ul></nav>
    <div class="head-actions">
      <a class="saved-link" href="{root}search.html">{icon('heart')}<span class="t">Saved</span> <span class="saved-count"></span></a>
      <a class="btn small" href="{root}search.html">Search homes</a>
      <button class="icon-btn menu-btn" type="button" data-open="menu" aria-haspopup="dialog" aria-expanded="false" aria-label="Open menu">{icon('menu')}</button>
    </div>
  </div>
</header>
<dialog class="sheet" id="menu" aria-label="Menu">
  <div class="sheet-inner">
    <div class="sheet-head"><img src="{root}../assets/logo/derived/rewap-wordmark-full-color.svg" alt="REWAP" width="116" height="34" style="width:116px"><button class="icon-btn" type="button" data-close aria-label="Close menu">{icon('x')}</button></div>
    <nav class="sheet-body" aria-label="Menu"><ul class="sheet-nav">{sheet}</ul></nav>
    <div class="sheet-foot small">652 Park Ave, Worcester, MA 01603<br><a href="tel:+15085097759">508-509-7759</a> · <a href="mailto:hongtran@lehonglaw.com">hongtran@lehonglaw.com</a></div>
  </div>
</dialog>'''

def foot(root):
    regions = ''.join(f'<li><a href="{root}search.html?region={s}">{esc(n)}</a></li>' for s, n in list(REG.items())[:5])
    return f'''<footer class="site-footer on-dark">
  <div class="wrap">
    <div class="foot-grid">
      <div class="stack" style="margin:0"><img src="{root}../assets/logo/rewap-logo-reversed.svg" alt="REWAP Brokerage" width="480" height="168" style="width:220px">
        <p>REWAP Brokerage LLC<br>652 Park Ave, Worcester, MA 01603<br><a href="tel:+15085097759">508-509-7759</a> · <a href="mailto:hongtran@lehonglaw.com">hongtran@lehonglaw.com</a></p></div>
      <nav aria-label="Services"><h2>Services</h2><ul><li><a href="{root}search.html">Buy</a></li><li><a href="{root}index.html#disciplines">Sell</a></li><li><a href="{root}index.html#disciplines">Invest</a></li><li><a href="{root}index.html#market">Market updates</a></li></ul></nav>
      <nav aria-label="Regions"><h2>Regions</h2><ul>{regions}<li><a href="{root}index.html#regions">All regions</a></li></ul></nav>
      <nav aria-label="The firm"><h2>The firm</h2><ul><li><a href="{root}index.html#firm">About REWAP</a></li><li><a href="{root}teams/oberdorfer-group.html">The Oberdorfer Group</a></li><li><a href="{root}index.html#contact">Contact</a></li></ul></nav>
      <nav aria-label="Legal"><h2>Legal</h2><ul><li><a href="#main">Agency disclosure</a></li><li><a href="#main">Fair Housing</a></li><li><a href="#main">Privacy</a></li><li><a href="#main">Accessibility</a></li></ul></nav>
    </div>
    <div class="foot-legal">
      <div class="row"><span class="eho"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M4 15L16 5l12 10v13H4z" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M11 17h10M11 21h10" stroke="currentColor" stroke-width="2"/></svg>Equal Housing Opportunity</span>
        <span>REWAP Brokerage LLC is a licensed Massachusetts real estate brokerage. License numbers to be added.</span></div>
      <p>Listing data on the live site will be provided by MLS PIN through an IDX feed and is deemed reliable but not guaranteed. This concept uses fictional sample data only.</p>
      <div class="row"><span>© 2026 REWAP Brokerage LLC</span><span>Concept 1 website by Jeremy Anderson · jeremyanderson.tech</span></div>
    </div>
  </div>
</footer>'''

def page(root, title, desc, body, current='', jsonld=None, body_cls=''):
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    bc = f' class="{body_cls}"' if body_cls else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#17283F">
<link rel="icon" href="{root}../assets/logo/derived/rewap-favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}../assets/logo/png/apple-touch-icon-180.png">
<link rel="preload" href="{root}../assets/fonts/libre-caslon-display.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}../assets/fonts/public-sans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}../assets/css/tokens.css">
<link rel="stylesheet" href="{root}../assets/css/book.css">
<link rel="stylesheet" href="{root}../assets/css/site.css">
<script src="{root}../assets/js/book.js" defer></script>
<script src="{root}../assets/js/site.js" defer></script>
{ld}
</head>
<body{bc}>
{head(root, current)}
<main id="main">
{body}
</main>
{foot(root)}
</body>
</html>
'''

ORG = {"@context": "https://schema.org", "@type": "RealEstateAgent", "@id": SITE_URL + "#org", "name": "REWAP Brokerage LLC", "url": SITE_URL,
       "telephone": "+1-508-509-7759", "email": "hongtran@lehonglaw.com",
       "address": {"@type": "PostalAddress", "streetAddress": "652 Park Ave", "addressLocality": "Worcester", "addressRegion": "MA", "postalCode": "01603", "addressCountry": "US"},
       "areaServed": {"@type": "State", "name": "Massachusetts"}, "founder": {"@type": "Person", "name": "Hong Tran", "jobTitle": "Founder, Real Estate Lawyer"}}

def crumbs(items):
    lis = ''.join(f'<li><a href="{h}">{esc(n)}</a></li>' if h else f'<li aria-current="page">{esc(n)}</li>' for n, h in items)
    return f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'

def write(rel, s):
    import re
    s = re.sub(r'<span class="code">[^<]*</span>', '', s)
    p = os.path.join(ROOT, 'site', rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').write(s); print('built site/' + rel)

# ================================================================ HOME
def home():
    r = ''
    own = [l for l in LST if l['own']][:3]
    counts = {s: sum(1 for l in LST if l['region'] == s) for s in REG}
    towns_by = {s: sorted({l['town'] for l in LST if l['region'] == s}) for s in REG}
    region_items = ''.join(f'<li><a href="{r}search.html?region={s}"><b>{esc(n)}</b><span>{", ".join(towns_by[s])}</span><span class="n">{counts[s]}</span></a></li>' for s, n in REG.items())
    guides = [('What does a home inspection contingency actually protect?', 'The clause, what it lets you do, and the deadline most buyers miss.', 'Buying guide · 8 minute read'),
              ('Reading a rent roll before you offer on a three-decker', 'Which numbers to ask for, which to verify, and which to discount.', 'Investing explainer · 11 minute read'),
              ('Selling a home in Massachusetts, from listing to deed', 'The six weeks before you list, the purchase and sale agreement, and closing day.', 'Selling guide · 12 minute read')]
    gcards = ''.join(f'<a class="article" href="communities/worcester.html#guides"><h3>{t}</h3><p>{d}</p><span class="article-meta">{m}</span></a>' for t, d, m in guides)
    body = f'''
<section class="hero" aria-labelledby="hero-h">
  <div class="wrap grid">
    <div class="hero-text">
      <h1 id="hero-h">Real estate, with clarity.</h1>
      <p class="lead">Buying, selling and investing across Massachusetts, guided by a brokerage founded and led by a real estate lawyer.</p>
      <form class="hero-search" action="search.html" role="search" aria-label="Search homes">
        <div class="seg"><label for="h-q">Where</label><input id="h-q" name="q" type="search" placeholder="Town, ZIP or address" autocomplete="off"></div>
        <button class="btn" type="submit" aria-label="Search">{icon('search')}<span class="t">Search</span></button>
      </form>
      <ul class="paths" aria-label="How we help">
        <li><a href="search.html"><b>Buy a home</b><span>Search every region; understand every term before you offer.</span>{icon('arrow')}</a></li>
        <li><a href="#disciplines"><b>Sell a property</b><span>Pricing you can check, and a lawyer’s reading of every agreement.</span>{icon('arrow')}</a></li>
        <li><a href="#disciplines"><b>Invest in Massachusetts</b><span>Multi-family and value-add, with sourced numbers and plain terms.</span>{icon('arrow')}</a></li>
      </ul>
    </div>
    <figure class="hero-plate" style="margin:0">
      <div class="elev" style="aspect-ratio:4/5;display:grid;place-items:center;overflow:hidden"><img src="../assets/img/elevations/triple-decker.svg" alt="" width="600" height="400" style="width:138%;max-width:none"></div>
      <figcaption class="caption"><span class="caption-title">Three-decker porches, Worcester</span><span class="caption-meta">Photograph to commission: soft overcast, 50 mm, from across the street (art direction 5.2)</span></figcaption>
    </figure>
  </div>
</section>
<div class="trust"><div class="wrap"><ul><li><b>Founded by Hong Tran</b>, real estate lawyer</li><li><b>652 Park Ave</b>, Worcester</li><li><b>Every region</b> of Massachusetts</li><li><b>Buyers, sellers and investors</b></li></ul></div></div>

<section class="section" id="regions" aria-labelledby="regions-h">
  <div class="wrap">
    <div class="section-head"><span class="code">Coverage</span><h2 id="regions-h">Every region, equal standing</h2>
      <p>Worcester is the home office, not the boundary. Choose a region to see its sample listings.</p></div>
    <div class="regions">
      <ul class="region-list">{region_items}</ul>
      <figure style="margin:0">{map_plate(r, LST, region_labels=True, pins=False, label_towns=True, aria='Massachusetts by county, with the towns where sample listings are located')}
        <figcaption class="caption"><span class="caption-title">Massachusetts, by county</span><span class="caption-meta">Towns with sample listings marked · numbers count sample listings per region</span></figcaption></figure>
    </div>
  </div>
</section>

<section class="section on-dark" aria-labelledby="promise-h">
  <div class="wrap">
    <h2 id="promise-h" class="statement-line">You will always know where you stand.</h2>
    <div class="principles">
      <div><h3>Counsel before commerce</h3><p>We advise on the decision first. Sometimes the right advice is to wait, or to walk away.</p></div>
      <div><h3>Every line read</h3><p>Offers, disclosures and purchase and sale agreements are read by someone qualified to read them, before you sign.</p></div>
      <div><h3>Advice that lasts</h3><p>We measure the relationship in years and properties, not in one closing.</p></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="selected-h">
  <div class="wrap">
    <div class="section-head"><span class="code">Listings</span><h2 id="selected-h">Selected properties</h2><p>Represented by REWAP and its teams. Sample listings for this concept.</p></div>
    <div class="plates three">{''.join(card(r, l) for l in own)}</div>
    <p class="mt-7"><a class="btn secondary" href="search.html">View all {len(LST)} sample listings</a></p>
  </div>
</section>

<section class="section alt" id="disciplines" aria-labelledby="disc-h">
  <div class="wrap">
    <div class="section-head"><span class="code">Services</span><h2 id="disc-h">Three disciplines, one standard</h2><p>Each service has its own path. All of them have a lawyer’s reading at the moments that matter.</p></div>
    <div class="ledger">
      <div class="ledger-row"><h3>Buying</h3><p class="what">Search, showings, offer strategy and negotiation, from first visit to closing.</p><p class="law"><b>Where the law matters</b>The offer and the purchase and sale agreement: contingencies, deadlines, deposits.</p><a class="btn quiet go" href="search.html"><span>Start a search</span></a></div>
      <div class="ledger-row"><h3>Selling</h3><p class="what">Pricing from comparable sales we show you, preparation, marketing and negotiation.</p><p class="law"><b>Where the law matters</b>Required disclosures, the purchase and sale agreement, and title before closing.</p><a class="btn quiet go" href="#contact"><span>Request a pricing review</span></a></div>
      <div class="ledger-row"><h3>Investing</h3><p class="what">Multi-family, mixed-use and value-add property, evaluated on sourced numbers.</p><p class="law"><b>Where the law matters</b>Leases and rent rolls, tenancy at transfer, lead paint and certificate requirements.</p><a class="btn quiet go" href="search.html?type=Multi-family"><span>See multi-family</span></a></div>
    </div>
  </div>
</section>

<section class="section" id="firm" aria-labelledby="firm-h">
  <div class="wrap firm">
    <figure style="margin:0"><div class="portrait-frame"><span>Portrait to commission · art direction 5.4</span></div>
      <figcaption class="caption"><span class="caption-title">Hong Tran</span><span class="caption-meta">Founder · Real Estate Lawyer</span></figcaption></figure>
    <div class="stack" style="margin:0">
      <h2 id="firm-h">An advisory firm that happens to be exceptional at real estate</h2>
      <p class="lead" style="max-width:40ch">REWAP Brokerage was founded and is led by Hong Tran, a real estate lawyer. The firm brings legal-level care to every stage of buying, selling and investing.</p>
      <p>From the office at 652 Park Avenue in Worcester, REWAP serves clients across Massachusetts. Brokers, agents and affiliated teams work under the firm, each keeping their own name.</p>
      <div class="team-ref">
        <p class="affil-chain"><b>REWAP Brokerage</b>{icon('chain')}<b>The Oberdorfer Group</b></p>
        <p>A Central Massachusetts team led by Brandon and Kait Oberdorfer, operating under REWAP Brokerage.</p>
        <a class="btn quiet" href="teams/oberdorfer-group.html"><span>Meet The Oberdorfer Group</span></a>
      </div>
    </div>
  </div>
</section>

<section class="section alt" id="market" aria-labelledby="market-h">
  <div class="wrap">
    <div class="section-head"><span class="code">Intelligence</span><h2 id="market-h">Market updates and guides</h2><p>Monthly figures with their source and date, and plain-language guides to the decisions behind them.</p></div>
    <div class="scroll-x">
      <table class="data-table">
        <caption class="sr-only">Monthly market figures by region</caption>
        <thead><tr><th scope="col">Region</th><th scope="col" class="r">Median sale price</th><th scope="col" class="r">Closed sales</th><th scope="col" class="r">Median days on market</th><th scope="col" class="r">Change, year on year</th></tr></thead>
      </table>
    </div>
    <p class="pending-row">Figures for every region publish monthly from MLS PIN statistics, each with its source and date, beginning the first full month after launch.</p>
    <div class="plates three" id="guides">{gcards}</div>
  </div>
</section>

<section class="section close" id="contact" aria-labelledby="cta-h">
  <div class="wrap close-grid">
    <h2 id="cta-h" class="display-close">Start with a conversation.</h2>
    <div class="stack" style="margin:0">
      <p class="lead" style="max-width:36ch">Tell us what you are buying, selling or weighing. We will explain the options and what each one commits you to, before anything is signed.</p>
      <div class="btn-row"><a class="btn" href="mailto:hongtran@lehonglaw.com">Request a consultation</a><a class="btn quiet" href="tel:+15085097759"><span>Or call 508-509-7759</span></a></div>
      <p class="small">652 Park Ave, Worcester, MA 01603 · hongtran@lehonglaw.com</p>
    </div>
  </div>
</section>'''
    write('index.html', page('', 'REWAP Brokerage — Real estate, with clarity', 'Massachusetts real estate brokerage founded and led by a real estate lawyer. Buying, selling and investing across every region, from Worcester.', body, '',
                             [ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": "REWAP Brokerage", "url": SITE_URL,
                                    "potentialAction": {"@type": "SearchAction", "target": SITE_URL + "search.html?q={q}", "query-input": "required name=q"}}]))

# ================================================================ SEARCH
def search():
    rows = ''
    for l in LST:
        st = 'own' if l['own'] else ''
        status = f"Open {l['openHouse']}" if l['openHouse'] else l['status']
        f = ' · '.join(facts(l))
        rows += f'''<article class="result" data-id="{l['id']}" data-price="{l['price']}" data-beds="{l['beds']}" data-sqft="{l['sqft']}" data-type="{l['type']}" data-region="{l['region']}" data-status="{l['status']}"
  data-search="{esc((l['address'] + ' ' + l['town'] + ' ' + REG[l['region']]).lower())}" data-href="{lhref('', l)}" data-address="{esc(l['address'])}, {l['town']}" data-facts="{esc(f)}">
  <div class="property-media elev">{elev('', l)}</div>
  <div class="body">
    <div class="top"><span class="status {st}">{esc(status)}</span><button class="icon-btn" type="button" data-save="{l['id']}" data-label="{esc(l['address'])}" aria-pressed="false" aria-label="Save {esc(l['address'])}">{icon('heart')}</button></div>
    <span class="property-price">{price(l['price'])}</span>
    <h2 class="property-address" style="font:italic 400 1.0625rem/1.35 var(--font-text);letter-spacing:0"><a href="{lhref('', l)}">{esc(l['address'])}, {l['town']}</a></h2>
    {facts_html(l)}
    <span class="property-attrib">{esc(l['office'])} · {l['id']}</span>
  </div>
</article>'''
    opts_region = ''.join(f'<option value="{s}">{esc(n)}</option>' for s, n in REG.items())
    body = f'''
<div class="search-page" data-search-page>
<form id="search-form" class="search-tools" role="search" aria-label="Filter sample listings">
  <div class="bar">
    <div class="tool loc"><label for="s-q">Location</label><input class="input" id="s-q" name="q" type="search" placeholder="Town, region or address" autocomplete="off"></div>
    <div class="tool"><label for="s-region">Region</label><select class="select" id="s-region" name="region"><option value="">All regions</option>{opts_region}</select></div>
    <div class="tool opt"><label for="s-max">Max price</label><select class="select" id="s-max" name="max"><option value="">Any</option><option value="400000">$400,000</option><option value="600000">$600,000</option><option value="800000">$800,000</option><option value="1000000">$1,000,000</option></select></div>
    <div class="tool opt"><label for="s-beds">Beds</label><select class="select" id="s-beds" name="beds"><option value="">Any</option><option value="2">2+</option><option value="3">3+</option><option value="4">4+</option></select></div>
    <div class="tool opt"><label for="s-type">Type</label><select class="select" id="s-type" name="type"><option value="">All types</option><option>Single-family</option><option>Multi-family</option><option>Condo</option></select></div>
    <button class="btn secondary" type="button" data-open="filters" aria-haspopup="dialog" aria-expanded="false" style="min-height:44px">{icon('sliders')}Filters</button>
  </div>
  <dialog class="sheet bottom" id="filters" aria-label="All filters">
    <div class="sheet-inner">
      <div class="sheet-head"><h2 style="font:400 1.5rem/1.2 var(--font-display)">Filters</h2><button class="icon-btn" type="button" data-close aria-label="Close filters">{icon('x')}</button></div>
      <div class="sheet-body form-grid">
        <div class="field"><label for="f-status">Status</label><select class="select" id="f-status" name="status"><option value="">Any status</option><option>For sale</option><option>Open house</option><option>Under agreement</option></select></div>
        <div class="field"><label for="f-min">Min price</label><select class="select" id="f-min" name="min"><option value="">No minimum</option><option value="300000">$300,000</option><option value="500000">$500,000</option><option value="750000">$750,000</option></select></div>
        <div class="field"><label for="f-sort">Sort</label><select class="select" id="f-sort" name="sort"><option value="">Newest</option><option value="price-asc">Price, low to high</option><option value="price-desc">Price, high to low</option><option value="size">Largest</option></select></div>
        <p class="small">Max price, beds and type sit in the bar above on larger screens.</p>
      </div>
      <div class="sheet-foot btn-row"><button class="btn" type="submit">Show results</button><button class="btn quiet" type="button" data-reset><span>Clear all</span></button></div>
    </div>
  </dialog>
</form>
<div class="split" data-view="list">
  <section class="list-pane" aria-labelledby="results-h">
    <div class="results-head"><h1 id="results-h" class="sr-only">Search results</h1><p role="status" aria-live="polite"><b data-count>{len(LST)} sample homes</b> in Massachusetts</p>
      <button class="btn quiet small" type="button"><span>Save this search</span></button></div>
    <div class="results">{rows}</div>
    <div class="empty" hidden><p style="font:400 var(--fs-h3)/1.2 var(--font-display);color:var(--c-night)">No sample listings match these filters.</p><p class="small">Widen the price range or choose another region.</p><button class="btn secondary small" type="button" data-reset>Clear filters</button></div>
    <p class="property-attrib" style="padding-top:var(--s-5)">On the live site, listing data comes from MLS PIN via IDX and is deemed reliable but not guaranteed. Listing office shown on every result.</p>
  </section>
  <section class="map-pane" aria-label="Map of results">
    {map_plate('', LST, aria='Map of Massachusetts with sample listing prices')}
    <div class="map-card" aria-live="polite"></div>
  </section>
</div>
<button class="btn view-toggle" type="button" aria-label="Show results on the map">{icon('map')}<span>Map</span></button>
</div>'''
    write('search.html', page('', 'Search Massachusetts homes — REWAP Brokerage', 'Search homes for sale across every region of Massachusetts.', body, 'Buy',
                               [ORG], 'search-body'))

# ================================================================ LISTING
def town_link(r, t):
    return f"{r}communities/worcester.html" if t == 'Worcester' else f"{r}search.html?q={t.replace(' ', '+')}"

N = '#17283F'
COUNTY = {'Pittsfield': 'Berkshire', 'Lenox': 'Berkshire', 'Great Barrington': 'Berkshire', 'Northampton': 'Hampshire', 'Springfield': 'Hampden',
          'Greenfield': 'Franklin', 'Worcester': 'Worcester', 'Shrewsbury': 'Worcester', 'Sturbridge': 'Worcester', 'Fitchburg': 'Worcester',
          'Grafton': 'Worcester', 'Framingham': 'Middlesex', 'Natick': 'Middlesex', 'Somerville': 'Middlesex', 'Quincy': 'Norfolk', 'Lowell': 'Middlesex',
          'Salem': 'Essex', 'Newburyport': 'Essex', 'Plymouth': 'Plymouth', 'Hingham': 'Plymouth', 'New Bedford': 'Bristol', 'Fall River': 'Bristol',
          'Falmouth': 'Barnstable', 'Chatham': 'Barnstable'}
def site_plan(l):
    import math
    street = l['address'].split(' ', 1)[1].split(',')[0]
    a = max(l['lotAcres'], 0.08); w = 300; h = max(110, min(170, 60 + a * 100))
    x0, y0 = 50, 206 - h; fw = 120 if l['type'] != 'Condo' else 200; fd = 70 if l['type'] != 'Condo' else 110
    fx, fy = x0 + (w - fw) / 2, y0 + h - fd - 40
    return (f'<svg viewBox="0 0 400 300" role="img" aria-label="Site plan drawing of {esc(l["address"])}, not to scale"><g fill="none" stroke="{N}" stroke-width="1.3">'
            f'<rect x="{x0}" y="{y0:.0f}" width="{w}" height="{h:.0f}" stroke-dasharray="6 4"/>'
            f'<rect x="{fx:.0f}" y="{fy:.0f}" width="{fw}" height="{fd}" fill="#E5EAF0"/>'
            f'<path d="M{fx+fw-30:.0f} {fy+fd:.0f}V{y0+h:.0f}M{fx+fw-6:.0f} {fy+fd:.0f}V{y0+h:.0f}" stroke-width=".8"/>'
            f'<path d="M20 214H380" stroke-width="2"/><path d="M20 226H380" stroke-width=".8" stroke-dasharray="10 8"/>'
            f'<path d="M360 40V74M360 40l-7 14h14z" stroke-width="1.2"/></g>'
            f'<g font-family="Public Sans, sans-serif" fill="{N}"><text x="360" y="34" font-size="11" font-weight="600" text-anchor="middle">N</text>'
            f'<text x="200" y="246" font-size="11" text-anchor="middle" letter-spacing="1">{esc(street.upper())}</text>'
            f'<text x="{x0+6}" y="{y0+16:.0f}" font-size="10" fill="#545C66">LOT · {l["lotAcres"]:g} AC</text></g></svg>') if l['lotAcres'] else (
            f'<svg viewBox="0 0 400 300" role="img" aria-label="Building outline drawing of {esc(l["address"])}"><g fill="none" stroke="{N}" stroke-width="1.3">'
            f'<rect x="60" y="40" width="280" height="150"/><rect x="200" y="70" width="110" height="80" fill="#E5EAF0"/><path d="M20 214H380" stroke-width="2"/>'
            f'<path d="M360 20V54M360 20l-7 14h14z" stroke-width="1.2"/></g><g font-family="Public Sans, sans-serif" fill="{N}"><text x="360" y="14" font-size="11" font-weight="600" text-anchor="middle">N</text>'
            f'<text x="255" y="166" font-size="10" text-anchor="middle" fill="#545C66">THIS UNIT</text><text x="200" y="240" font-size="11" text-anchor="middle" letter-spacing="1">{esc(street.upper())}</text></g></svg>')

def unit_stack(l):
    n = l['units']; per = l['beds'] // n; h = 180 / n
    rows = ''.join(f'<rect x="110" y="{50 + i*h:.0f}" width="180" height="{h:.0f}"/><text x="200" y="{50 + i*h + h/2 + 4:.0f}" text-anchor="middle" font-size="12" stroke="none" fill="{N}">Unit {n-i} · {per} bd</text>' for i in range(n))
    return (f'<svg viewBox="0 0 400 300" role="img" aria-label="Unit stack drawing: {n} units, one per floor"><g fill="none" stroke="{N}" stroke-width="1.3" font-family="Public Sans, sans-serif">'
            f'<path d="M100 50L200 18L300 50"/>{rows}<rect x="110" y="230" width="180" height="26" stroke-dasharray="4 3"/>'
            f'<text x="200" y="247" text-anchor="middle" font-size="11" stroke="none" fill="#545C66">Basement · mechanicals</text><path d="M40 256H360" stroke-width="2"/></g></svg>')

def describe(l):
    t, y = l['type'], l['yearBuilt']
    if t == 'Multi-family':
        return (f"A {y} {'three-decker' if l['elevation'] == 'triple-decker' else 'multi-family building'} with {l['units']} separately metered units "
                f"and {l['beds']} bedrooms in total, on a {l['lotAcres']:g}-acre lot in {l['town']}. Existing tenancies are summarized below.")
    if t == 'Condo':
        return (f"A {l['beds']}-bedroom, {l['baths']:g}-bath condominium of {l['sqft']:,} square feet in {l['address'].split(',')[0]}, "
                f"a building dating from {y}. Association documents and the monthly fee are listed below.")
    return (f"A {y} {'Cape' if l['elevation'] == 'cape' else 'colonial' if l['elevation'] == 'colonial' else 'house'} with {l['beds']} bedrooms and "
            f"{l['baths']:g} baths in {l['sqft']:,} square feet, on {l['lotAcres']:g} acres in {l['town']}.")

def know(l):
    k = []
    if l['yearBuilt'] < 1978:
        k.append(('Lead paint', 'Built before 1978. Massachusetts requires the seller to provide the Property Transfer Lead Paint Notification, and the buyer has a right to an inspection.'))
    k.append(('Smoke and CO', 'A smoke and carbon monoxide detector compliance certificate from the local fire department is required at transfer.'))
    if l['type'] == 'Multi-family':
        k.append(('Tenancies', 'Existing leases transfer with the building. Review each lease, security deposits and last month’s rent held before closing.'))
        k.append(('Zoning', f"Confirm the legal number of units and any open permits with the {l['town']} building department before the purchase and sale agreement."))
    elif l['type'] == 'Condo':
        k.append(('Association', 'Request the master deed, bylaws, budget, reserve study and recent minutes, and ask whether any special assessment is planned.'))
    else:
        k.append(('Septic or sewer', f"Confirm whether the property is on town sewer; a private septic system must pass a Title 5 inspection before transfer."))
    return ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in k)

def listing(l):
    r = '../'
    sim = [x for x in LST if x['type'] == l['type'] and x['id'] != l['id']][:3]
    contact = ('Brandon Oberdorfer', 'Broker · The Oberdorfer Group') if l['team'] == 'oberdorfer' else ('Hong Tran', 'Founder · Real Estate Lawyer')
    listed = 'Listed by REWAP Brokerage' if l['own'] else f"Listing courtesy of {l['office']}"
    gfig = f'<figure><img src="{r}../assets/img/elevations/{l["elevation"]}.svg" alt="Front elevation drawing of {esc(l["address"])}" width="600" height="400"><figcaption>Front elevation · drawing</figcaption></figure>'
    gfig += f'<figure>{site_plan(l)}<figcaption>Site plan · drawing, not to scale</figcaption></figure>'
    if l['type'] == 'Multi-family':
        gfig += f'<figure>{unit_stack(l)}<figcaption>Unit stack · drawing</figcaption></figure>'
    ncls = 'n3' if l['type'] == 'Multi-family' else 'n2'
    units = ''
    if l['type'] == 'Multi-family':
        per_b = l['beds'] // l['units']; per_s = l['sqft'] // l['units']; rent = round(l['price'] / l['units'] / 115 / 25) * 25
        rows = ''.join(f'<tr><td class="nw">Unit {i}</td><td class="r num">{per_b}</td><td class="r num">1</td><td class="r num">{per_s:,}</td><td class="r num">${rent + (i-2)*50:,}</td></tr>' for i in range(1, l['units'] + 1))
        units = f'''<section aria-labelledby="units-h" class="stack">
      <h2 id="units-h" class="lh">Units and rents</h2>
      <div class="scroll-x"><table class="data-table"><caption class="sr-only">Units and stated rents</caption>
        <thead><tr><th scope="col">Unit</th><th scope="col" class="r">Beds</th><th scope="col" class="r">Baths</th><th scope="col" class="r">Sq ft</th><th scope="col" class="r">Stated rent</th></tr></thead>
        <tbody>{rows}</tbody></table></div>
      <p class="small">Sample rents as stated by the seller; not verified. Ask for the leases and rent roll before making an offer.</p>
    </section>'''
    extra = f'<tr><th scope="row">Association fee</th><td class="r num">${round(l["price"]*0.00095/5)*5:,} / mo</td></tr>' if l['type'] == 'Condo' else f'<tr><th scope="row">Lot</th><td class="r num">{l["lotAcres"]:g} ac</td></tr>'
    oh = f'<p class="notice info" role="note"><svg aria-hidden="true"><use href="#i-cal"/></svg>Open house {l["openHouse"]}. No appointment needed.</p>' if l['openHouse'] else ''
    jl = {"@context": "https://schema.org", "@type": "Residence", "name": f"{l['address']}, {l['town']}, MA",
          "address": {"@type": "PostalAddress", "streetAddress": l['address'], "addressLocality": l['town'], "addressRegion": "MA", "addressCountry": "US"},
          "geo": {"@type": "GeoCoordinates", "latitude": l['lat'], "longitude": l['lng']}, "numberOfRooms": l['beds'],
          "floorSize": {"@type": "QuantitativeValue", "value": l['sqft'], "unitCode": "FTK"},
          "offers": {"@type": "Offer", "price": l['price'], "priceCurrency": "USD", "availability": "https://schema.org/InStock"}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL}, {"@type": "ListItem", "position": 2, "name": "Search", "item": SITE_URL + "search.html"},
        {"@type": "ListItem", "position": 3, "name": l['town']}, {"@type": "ListItem", "position": 4, "name": l['address']}]}
    kf = [('Beds', l['beds']), ('Baths', f"{l['baths']:g}"), ('Living area', f"{l['sqft']:,} sq ft"), ('Built', l['yearBuilt'])]
    if l['type'] == 'Multi-family': kf.insert(0, ('Units', l['units']))
    if l['lotAcres']: kf.append(('Lot', f"{l['lotAcres']:g} ac"))
    kfh = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in kf)
    body = f'''
{crumbs([('Home', r + 'index.html'), ('Search', r + 'search.html'), (l['town'], town_link(r, l['town'])), (l['address'], None)])}
<div class="wrap"><div class="gallery {ncls}" aria-label="Drawings of the property">{gfig}</div><p class="small gallery-note">Photographs to commission: front, kitchen, living areas, rear{" and each unit" if l['type'] == 'Multi-family' else ''}. Drawings stand in until they exist (art direction 5.6).</p></div>
<div class="wrap listing-grid">
  <div class="stack-lg" style="margin:0">
    <header class="listing-title">
      <p class="small"><span class="status{' own' if l['own'] else ''}">{l['status']}</span> · {esc(listed)} · Sample listing</p>
      <span class="property-price">{price(l['price'])}</span>
      <h1>{esc(l['address'])}, {l['town']}, MA</h1>
      <dl class="keyfacts">{kfh}</dl>
      <div class="btn-row" style="margin-top:var(--s-4)">
        <button class="btn secondary small" type="button" data-save="{l['id']}" data-label="{esc(l['address'])}" aria-pressed="false">{icon('heart')}<span>Save</span></button>
        <button class="btn secondary small" type="button" data-share>{icon('share')}<span>Share</span></button>
      </div>
    </header>
    {oh}
    <section aria-labelledby="about-h" class="stack">
      <h2 id="about-h" class="lh">About this property</h2>
      <p>{describe(l)}</p>
      <p class="note">Sample description in REWAP’s listing voice: facts first, no adjectives doing a number’s job.</p>
    </section>
    {units}
    <section aria-labelledby="know-h" class="stack">
      <h2 id="know-h" class="lh">What to know before you offer</h2>
      <ul class="spec-list">{know(l)}</ul>
      <p class="note">General guidance written by REWAP; confirm every item for a real property.</p>
    </section>
    <section aria-labelledby="facts-h" class="stack">
      <h2 id="facts-h" class="lh">Facts</h2>
      <div class="scroll-x"><table class="data-table"><caption class="sr-only">Listing facts</caption><tbody>
        <tr><th scope="row">Status</th><td class="r">{l['status']}</td></tr>
        <tr><th scope="row">Type</th><td class="r">{l['type']}{f", {l['units']} units" if l['type'] == 'Multi-family' else ''}</td></tr>
        <tr><th scope="row">Year built</th><td class="r num">{l['yearBuilt']}</td></tr>{extra}
        <tr><th scope="row">Region</th><td class="r">{esc(REG[l['region']])}</td></tr>
        <tr><th scope="row">MLS #</th><td class="r num">{l['id']}</td></tr>
      </tbody></table></div>
    </section>
    <section aria-labelledby="loc-h" class="stack">
      <h2 id="loc-h" class="lh">Location</h2>
      <figure style="margin:0">{map_plate(r, None, highlight=[COUNTY[l['town']]], dot=l['town'], pins=False, focus=COUNTY[l['town']], aria=f"Map of {COUNTY[l['town']]} County with {l['town']} marked")}
        <figcaption class="caption"><span class="caption-title">{l['town']}, {COUNTY[l['town']]} County</span><span class="caption-meta">Exact location shared on request on the live site</span></figcaption></figure>
    </section>
    <p class="property-attrib">{esc(listed)}. Sample listing for the Concept 1 website; on the live site listing data comes from MLS PIN via IDX and is deemed reliable but not guaranteed.</p>
  </div>
  <aside aria-label="Contact about this property">
    <div class="contact-card">
      <div class="agent" style="border:0;padding:0;grid-template-columns:5rem 1fr">
        <div class="portrait-frame"><span>Portrait</span></div>
        <div><p class="agent-name">{contact[0]}</p><p class="agent-role">{contact[1]}<br>REWAP Brokerage</p></div>
      </div>
      <form class="form-grid" data-demo novalidate aria-label="Ask about this property">
        <div class="field"><label for="c-name">Name</label><input class="input" id="c-name" autocomplete="name"></div>
        <div class="field"><label for="c-email">Email</label><input class="input" id="c-email" type="email" autocomplete="email"></div>
        <div class="field"><label for="c-msg">Message</label><textarea class="textarea" id="c-msg" style="min-height:6rem">I would like to see {esc(l['address'])}.</textarea></div>
        <button class="btn" type="submit">Request a showing</button>
        <p class="small">Or call <a href="tel:+15085097759">508-509-7759</a>. Demo form; nothing is sent.</p>
      </form>
    </div>
  </aside>
</div>
<section class="section alt" aria-labelledby="sim-h"><div class="wrap">
  <div class="section-head"><span class="code">Similar</span><h2 id="sim-h">Similar {l['type'].lower()} property</h2><p>Sample listings elsewhere in Massachusetts.</p></div>
  <div class="plates three">{''.join(card(r, x) for x in sim)}</div>
</div></section>
<div class="bottom-bar">
  <button class="icon-btn" type="button" data-save="{l['id']}" data-label="{esc(l['address'])}" aria-pressed="false" aria-label="Save {esc(l['address'])}">{icon('heart')}</button>
  <button class="icon-btn" type="button" data-share aria-label="Share this listing">{icon('share')}<span class="sr-only">Share</span></button>
  <a class="btn" href="#c-name">Request a showing</a>
</div>'''
    write(f"homes/{l['slug']}.html", page(r, f"{l['address']}, {l['town']}, MA — {price(l['price'])} — REWAP Brokerage", f"{l['type']} in {l['town']}, MA. Sample listing.", body, 'Buy', [ORG, jl, bc], 'has-bottom-bar'))

# ================================================================ COMMUNITY
def community():
    r = '../'
    wl = [l for l in LST if l['town'] == 'Worcester']
    hoods = [('Canal District', 'Named for the Blackstone Canal that once ran beneath it; brick commercial blocks, Kelley Square and Polar Park.'),
             ('Shrewsbury Street', 'A restaurant corridor running east from downtown toward Lake Quinsigamond, with triple-deckers on the side streets.'),
             ('Elm Park and the West Side', 'Around Elm Park, one of the earliest public parks in the country, with larger single-family homes on the hills nearby.'),
             ('Main South', 'Along Main Street around Clark University, with multi-family housing and storefront blocks.'),
             ('Grafton Hill', 'An east-side hill of three-deckers and two-families above Grafton Street.'),
             ('Downtown', 'Union Station, the courthouse and City Hall, with apartments and condominiums in converted commercial buildings.')]
    hl = ''.join(f'<li><h3>{n}</h3><p>{d}</p></li>' for n, d in hoods)
    faq = [('What is a three-decker?', 'A wood-frame building with three stacked apartments, usually one per floor, often with front porches on every level. Worcester has one of the largest stocks of them in New England, and they remain a common first investment property.'),
           ('Do I need a lawyer to buy a home in Massachusetts?', 'Real estate closings in Massachusetts are conducted by attorneys, and buyers commonly hire their own to review the purchase and sale agreement and title. REWAP is founded by a real estate lawyer, so legal questions are part of the conversation from the first meeting.'),
           ('What should I know about lead paint in older Worcester homes?', 'Most of Worcester’s housing was built before 1978. Massachusetts law requires sellers and landlords to give buyers the Property Transfer Lead Paint Notification, and homes where children under six live must be deleaded. Ask about the paint history of any older building before you offer.')]
    fq = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q} <span class="pm" aria-hidden="true"></span></summary><div class="panel"><p>{a}</p></div></details>' for i, (q, a) in enumerate(faq))
    jfaq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    jplace = {"@context": "https://schema.org", "@type": "Place", "name": "Worcester, Massachusetts", "containedInPlace": {"@type": "AdministrativeArea", "name": "Worcester County, Massachusetts"},
              "geo": {"@type": "GeoCoordinates", "latitude": 42.2626, "longitude": -71.8023}}
    body = f'''
{crumbs([('Home', r + 'index.html'), ('Communities', r + 'index.html#regions'), ('Central Massachusetts', r + 'search.html?region=central'), ('Worcester', None)])}
<section class="place-hero" aria-labelledby="place-h">
  <div class="wrap grid">
    <div class="t">
      <h1 id="place-h">Worcester</h1>
      <p class="lead">New England’s second-largest city and REWAP’s home office: three-deckers and mill buildings, hilltop neighborhoods and a downtown on the commuter rail to Boston.</p>
      <dl class="fact-row">
        <div><dt>County</dt><dd>Worcester County</dd></div>
        <div><dt>Region</dt><dd>Central Massachusetts</dd></div>
        <div><dt>Rail</dt><dd>MBTA Framingham/Worcester Line, Union Station</dd></div>
        <div><dt>REWAP office</dt><dd>652 Park Ave</dd></div>
      </dl>
    </div>
    <figure class="m" style="margin:0">{map_plate(r, None, highlight=['Worcester'], dot='Worcester', pins=False, focus='Worcester', aria='Map of Worcester County with the city of Worcester marked')}
      <figcaption class="caption"><span class="caption-title">Worcester County, Massachusetts</span><span class="caption-meta">City of Worcester marked</span></figcaption></figure>
  </div>
</section>

<section class="section" aria-labelledby="snap-h"><div class="wrap">
  <div class="section-head"><span class="code">Market</span><h2 id="snap-h">Market snapshot</h2><p>Monthly, sourced and dated. Nothing is estimated.</p></div>
  <div class="scroll-x"><table class="data-table"><caption class="sr-only">Worcester market snapshot</caption>
    <thead><tr><th scope="col">Median sale price</th><th scope="col">Closed sales, 12 months</th><th scope="col">Median days on market</th><th scope="col">Active listings</th></tr></thead>
    </table></div>
  <p class="pending-row">Worcester figures publish monthly from MLS PIN statistics, with source and date, beginning the first full month after launch.</p>
</div></section>

<section class="section alt" aria-labelledby="stock-h"><div class="wrap">
  <div class="section-head"><span class="code">Housing</span><h2 id="stock-h">The housing stock</h2><p>Worcester’s buildings explain its market. Three types account for much of what comes up for sale.</p></div>
  <div class="plates three">
    <figure class="plate"><div class="elev" style="aspect-ratio:3/2"><img src="{r}../assets/img/elevations/triple-decker.svg" alt="" width="600" height="400" loading="lazy" style="width:100%;height:100%;object-fit:contain"></div><figcaption class="caption"><span class="caption-title">Three-deckers</span><span class="caption-meta">Owner-occupant and investor buildings across the east side, Main South and Grafton Hill</span></figcaption></figure>
    <figure class="plate"><div class="elev" style="aspect-ratio:3/2"><img src="{r}../assets/img/elevations/mill.svg" alt="" width="600" height="400" loading="lazy" style="width:100%;height:100%;object-fit:contain"></div><figcaption class="caption"><span class="caption-title">Mill and commercial conversions</span><span class="caption-meta">Lofts and condominiums in former industrial buildings, especially near the Canal District</span></figcaption></figure>
    <figure class="plate"><div class="elev" style="aspect-ratio:3/2"><img src="{r}../assets/img/elevations/colonial.svg" alt="" width="600" height="400" loading="lazy" style="width:100%;height:100%;object-fit:contain"></div><figcaption class="caption"><span class="caption-title">Single-family homes</span><span class="caption-meta">Colonials and Capes on the West Side and in the neighborhoods near the city line</span></figcaption></figure>
  </div>
</div></section>

<section class="section" aria-labelledby="hood-h"><div class="wrap">
  <div class="section-head"><span class="code">Places</span><h2 id="hood-h">Neighborhoods</h2><p>Places, not people: what is there, not who it is for. Draft copy for REWAP to review.</p></div>
  <ul class="hood-list">{hl}</ul>
</div></section>

<section class="section alt" aria-labelledby="wl-h"><div class="wrap">
  <div class="section-head"><span class="code">Listings</span><h2 id="wl-h">For sale in Worcester</h2><p>Sample listings.</p></div>
  <div class="plates three">{''.join(card(r, l) for l in wl)}</div>
  <p class="mt-7"><a class="btn secondary" href="{r}search.html?q=worcester">Search Worcester</a></p>
</div></section>

<section class="section" id="guides" aria-labelledby="faq-h"><div class="wrap">
  <div class="section-head"><span class="code">Questions</span><h2 id="faq-h">Buying a home in Worcester: common questions</h2><p>Short answers first; ask us for the detail that applies to you.</p></div>
  <div class="body-cols"><div class="full accordion" style="max-width:52rem">{fq}</div></div>
</div></section>'''
    write('communities/worcester.html', page(r, 'Worcester, MA real estate and community guide — REWAP Brokerage', 'Worcester, Massachusetts: housing stock, neighborhoods, market snapshot and common questions about buying a home in Worcester.', body, 'Communities', [ORG, jplace, jfaq]))

# ================================================================ TEAM
def team():
    r = '../'
    tl = [l for l in LST if l['team'] == 'oberdorfer']
    jteam = {"@context": "https://schema.org", "@type": "Organization", "name": "The Oberdorfer Group", "parentOrganization": {"@id": SITE_URL + "#org"},
             "member": [{"@type": "Person", "name": "Brandon Oberdorfer", "jobTitle": "Broker"}, {"@type": "Person", "name": "Kait Oberdorfer"}],
             "areaServed": {"@type": "AdministrativeArea", "name": "Central Massachusetts"}}
    body = f'''
{crumbs([('Home', r + 'index.html'), ('The Firm', r + 'index.html#firm'), ('Teams', r + 'index.html#firm'), ('The Oberdorfer Group', None)])}
<section class="team-hero" aria-labelledby="team-h"><div class="wrap team-hero-grid">
  <div class="stack" style="margin:0">
    <span class="team-mark-slot primary">The Oberdorfer Group mark<br>(theirs, to be supplied)</span>
    <h1 id="team-h" style="font-size:var(--fs-h1);max-width:16ch">The Oberdorfer Group</h1>
    <p class="lead" style="max-width:40ch">A Central Massachusetts real estate team led by Brandon and Kait Oberdorfer.</p>
    <p class="under"><span>Operating under</span><img src="{r}../assets/logo/rewap-logo-mono-navy.svg" alt="REWAP Brokerage" width="480" height="168"></p>
    <div class="btn-row"><a class="btn" href="#tc-h">Contact the team</a><a class="btn quiet" href="#tl-h"><span>See their listings</span></a></div>
  </div>
  <figure style="margin:0">{map_plate(r, None, highlight=['Worcester'], pins=False, aria='Map of Massachusetts with Worcester County, the team\'s home market, shaded', focus='Worcester')}
    <figcaption class="caption"><span class="caption-title">Central Massachusetts</span><span class="caption-meta">The team’s home market, within REWAP’s statewide coverage</span></figcaption></figure>
</div></section>

<section class="section" aria-labelledby="members-h"><div class="wrap">
  <div class="section-head"><span class="code">Team</span><h2 id="members-h">Who you will work with</h2><p>Biographies supplied by the team.</p></div>
  <div class="members">
    <article class="member"><div class="portrait-frame"><span>Portrait · theirs</span></div><div class="stack" style="margin:0"><p class="agent-name">Brandon Oberdorfer</p><p class="agent-role">Broker · The Oberdorfer Group</p><p class="note">Biography to be supplied by the team.</p></div></article>
    <article class="member"><div class="portrait-frame"><span>Portrait · theirs</span></div><div class="stack" style="margin:0"><p class="agent-name">Kait Oberdorfer</p><p class="agent-role">The Oberdorfer Group · title to confirm</p><p class="note">Biography to be supplied by the team.</p></div></article>
  </div>
</div></section>

<section class="section alt" aria-labelledby="tl-h"><div class="wrap">
  <div class="section-head"><span class="code">Listings</span><h2 id="tl-h">Listed by The Oberdorfer Group</h2><p>Sample listings.</p></div>
  <div class="plates three">{''.join(card(r, l) for l in tl)}</div>
</div></section>

<section class="section" aria-labelledby="tc-h"><div class="wrap">
  <div class="section-head"><span class="code">Contact</span><h2 id="tc-h">Contact the team</h2><p>Messages from this page go straight to The Oberdorfer Group.</p></div>
  <div class="body-cols"><form class="full form-grid two" data-demo novalidate aria-label="Contact The Oberdorfer Group" style="max-width:44rem">
    <input type="hidden" name="route" value="team:oberdorfer-group">
    <div class="field"><label for="t-name">Name</label><input class="input" id="t-name" autocomplete="name"></div>
    <div class="field"><label for="t-phone">Phone</label><input class="input" id="t-phone" type="tel" autocomplete="tel"></div>
    <div class="field span-2"><label for="t-email">Email</label><input class="input" id="t-email" type="email" autocomplete="email"></div>
    <div class="field span-2"><label for="t-msg">How can we help?</label><textarea class="textarea" id="t-msg"></textarea></div>
    <div class="span-2 btn-row"><button class="btn" type="submit">Send to the team</button><span class="small">Demo form; nothing is sent.</span></div>
  </form></div>
</div></section>'''
    write('teams/oberdorfer-group.html', page(r, 'The Oberdorfer Group at REWAP Brokerage', 'The Oberdorfer Group, a Central Massachusetts real estate team operating under REWAP Brokerage.', body, 'The Firm', [ORG, jteam]))

if __name__ == '__main__':
    home(); search(); community(); team()
    for l in LST: listing(l)
