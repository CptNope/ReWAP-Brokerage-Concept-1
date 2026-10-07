"""
REWAP logo vectorisation + variant builder.

Source: assets/logo/source/rewap-logo-original.png (512x171 raster supplied by REWAP).
Method:
  * Letterforms (R E W A P / BROKERAGE) are traced from an 8x upscale of the raster,
    smoothed to remove compression noise, and fitted with potrace curves. Their
    design is the original's; nothing is substituted with a font.
  * Geometric parts (double ring, key shaft, skyline, tip chevron, roof, windows)
    are rebuilt as exact primitives from measurements of the raster.
All coordinates live in the original 512x171 pixel space.
Requires: pillow numpy scipy scikit-image potracer
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from skimage.measure import label, regionprops
import potrace

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'assets/logo/source/rewap-logo-original.png')
OUT = os.path.join(ROOT, 'assets/logo')
S = 8

# ---------------------------------------------------------------- trace letters
def masks():
    """Returns (W silhouette, navy BROKERAGE ink, bronze ink) at 8x.
    The W is taken as the single dark connected shape (its own dark rim included);
    bronze letters are every other opaque pixel outside it."""
    from scipy.ndimage import binary_dilation
    src = Image.open(SRC).convert('RGBA')
    big = np.array(src.resize((src.width * S, src.height * S), Image.LANCZOS)).astype(float)
    r, g, b, a = [big[..., i] for i in range(4)]
    op = a > 128
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    clear_bronze = op & (r - b > 35) & (lum > 85)
    dark = op & ~clear_bronze
    wreg = region(dark, 96.0, 194.0, 58, 124)
    lab = label(wreg, connectivity=1)
    big_id = max(regionprops(lab), key=lambda rp: rp.area).label
    W = lab == big_id
    navy_text = region(op & (b >= r - 2) & (lum < 115), 250, 472, 76, 110)
    bronze = op & ~binary_dilation(W, iterations=3) & ~navy_text
    return W, navy_text, bronze

def region(m, x0, x1, y0, y1):
    o = np.zeros_like(m)
    sl = (slice(int(y0 * S), int(y1 * S)), slice(int(x0 * S), int(x1 * S)))
    o[sl] = m[sl]
    return o

def smooth(m, sig=6.0):
    from scipy.ndimage import binary_fill_holes, binary_opening
    from skimage.morphology import remove_small_objects, remove_small_holes
    m = remove_small_objects(m, max_size=6 * S * S)
    m = remove_small_holes(m, max_size=2 * S * S)
    return gaussian_filter(m.astype(float), sig) > 0.5

def trace(mask, minarea=8, alphamax=1.25, opt=0.8):
    d = []
    lab = label(mask, connectivity=2)
    for rp in regionprops(lab):
        if rp.area < minarea * S * S:
            continue
        y0, x0, y1, x1 = rp.bbox
        oy, ox = max(0, y0 - 3), max(0, x0 - 3)
        sub = lab[oy:y1 + 3, ox:x1 + 3] == rp.label
        pl = potrace.Bitmap(~sub).trace(turdsize=20, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
                                       alphamax=alphamax, opticurve=True, opttolerance=opt)
        f = lambda p: f"{(p.x + ox) / S:.2f} {(p.y + oy) / S:.2f}"
        for c in pl:
            d.append("M" + f(c.start_point))
            for s in c.segments:
                d.append(("L" + f(s.c) + "L" + f(s.end_point)) if s.is_corner
                         else ("C" + f(s.c1) + " " + f(s.c2) + " " + f(s.end_point)))
            d.append("Z")
    return "".join(d)

def trace_letters():
    W, navy_text, bronze = masks()
    ap = bronze.copy(); ap[:int(67.5 * S), int(226 * S):] = False      # bar belongs to the key, not the P
    ap_solo = bronze.copy(); ap_solo[:int(69.5 * S), int(238 * S):] = False
    return {
        'RE': trace(smooth(region(bronze, 25, 113.6, 64.6, 117))),
        'AP': trace(smooth(region(ap, 160, 252, 64.6, 116.9))),
        'AP_solo': trace(smooth(region(ap_solo, 160, 250.2, 65.9, 116.7))),
        'W': trace(smooth(W, 5.5)),
        'BROKERAGE': trace(smooth(navy_text, 4.5), minarea=4),
    }

# ---------------------------------------------------------------- geometry
CX, CY = 144.4, 86.1
RINGS = [(83.3, 78.2, 4.0), (67.35, 63.45, 3.9)]          # rx, ry, stroke (centre-line)
BAND = (64.25, 117.0)                                     # rings break behind the letter band
SKYLINE = ("M230 64L230 62L251 62L251 51L264 51L264 40L283 40L283 62L293.5 62L307 51.3L320.5 62"
           "L324 62L324 51L334 51L334 38L352 38L352 54L356 54L356 47L374.5 47L374.5 54.5L382 54.5"
           "L382 44.5L401 34L401 49.5L410.5 49.5L410.5 62L418 62L427.5 53L437 62L469.6 62L469.6 64Z")
FRAME = ("M230 62L469.6 62L499.2 91.6L469.6 121.2L226 121.2L226 116.9L467.25 116.9L492.55 91.6"
         "L468.15 67.2L230 67.2Z")
CHEVRON = "M471.3 78.9L484.9 92.2L471.3 105.5L471.3 101.6L481 92.2L471.3 82.8Z"
ROOF = "M143.7 93.5L158 121.1L153.9 121.1L143.6 103L133.3 121.1L129.2 121.1Z"
WINDOWS = [(139.1, 112.0), (144.7, 112.0), (139.1, 117.2), (144.7, 117.2)]
WIN = (3.7, 3.8)

def windows_svg(fill):
    return "".join(f'<rect x="{x}" y="{y}" width="{WIN[0]}" height="{WIN[1]}" fill="{fill}"/>' for x, y in WINDOWS)

# ---------------------------------------------------------------- palettes
GRAD = """
<linearGradient id="{p}bz-type" gradientUnits="userSpaceOnUse" x1="0" y1="61" x2="0" y2="121">
  <stop offset="0" stop-color="#E9CBA2"/><stop offset=".14" stop-color="#D5AF86"/>
  <stop offset=".38" stop-color="#B88D61"/><stop offset=".56" stop-color="#A67C52"/>
  <stop offset=".64" stop-color="#C39A6E"/><stop offset=".82" stop-color="#93693F"/>
  <stop offset="1" stop-color="#6E4A27"/></linearGradient>
<linearGradient id="{p}bz-ring" gradientUnits="userSpaceOnUse" x1="62" y1="6" x2="226" y2="166">
  <stop offset="0" stop-color="#E6C59D"/><stop offset=".42" stop-color="#B98D5F"/>
  <stop offset=".68" stop-color="#D2AA7E"/><stop offset="1" stop-color="#8A6038"/></linearGradient>
<linearGradient id="{p}bz-key" gradientUnits="userSpaceOnUse" x1="0" y1="34" x2="0" y2="122">
  <stop offset="0" stop-color="#E5C49C"/><stop offset=".3" stop-color="#C59C6F"/>
  <stop offset=".34" stop-color="#B38759"/><stop offset=".62" stop-color="#C79F73"/>
  <stop offset="1" stop-color="#94693F"/></linearGradient>
<linearGradient id="{p}nv" gradientUnits="userSpaceOnUse" x1="0" y1="61" x2="0" y2="122">
  <stop offset="0" stop-color="#2D4055"/><stop offset=".22" stop-color="#18293C"/>
  <stop offset="1" stop-color="#050C16"/></linearGradient>
"""

MODES = {
    # name: (bronze type, bronze ring, bronze key, navy W, navy text, bevel stroke)
    'full-color':     ('url(#{p}bz-type)', 'url(#{p}bz-ring)', 'url(#{p}bz-key)', 'url(#{p}nv)', '#0E1A27', '#4A2C12'),
    'flat':           ('#AD7E50', '#AD7E50', '#AD7E50', '#17283F', '#17283F', None),
    'reversed':       ('url(#{p}bz-type)', 'url(#{p}bz-ring)', 'url(#{p}bz-key)', '#FAFAF9', '#FAFAF9', None),
    'reversed-flat':  ('#C49C72', '#C49C72', '#C49C72', '#FAFAF9', '#FAFAF9', None),
}
MONO = {'mono-navy': '#17283F', 'mono-black': '#000000', 'mono-white': '#FFFFFF', 'mono-bronze': '#AD7E50'}

VB_PRIMARY = "24 2 480 168"

def ring_svg(stroke, clip=True, p=''):
    cp = f' clip-path="url(#{p}band)"' if clip else ''
    return "".join(f'<ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry}" fill="none" stroke="{stroke}" stroke-width="{sw}"{cp}/>'
                   for rx, ry, sw in RINGS)

def band_clip(p=''):
    return (f'<clipPath id="{p}band"><rect x="0" y="0" width="512" height="{BAND[0]}"/>'
            f'<rect x="0" y="{BAND[1]}" width="512" height="{171 - BAND[1]}"/></clipPath>')

def primary(L, mode, title, p='r-'):
    if mode in MONO:
        c = MONO[mode]
        defs = band_clip(p) + (
            f'<mask id="{p}ko" maskUnits="userSpaceOnUse" x="0" y="0" width="512" height="171">'
            f'<rect width="512" height="171" fill="#fff"/>'
            f'<g fill="#000" stroke="#000" stroke-width="3" stroke-linejoin="round">'
            f'<path d="{ROOF}"/><path d="{L["RE"]}"/><path d="{L["AP"]}"/></g>'
            f'{windows_svg("#000")}</mask>')
        body = (f'<g fill="{c}">{ring_svg(c, p=p)}<path d="{SKYLINE}"/><path d="{FRAME}"/><path d="{CHEVRON}"/>'
                f'<path d="{L["RE"]}"/><path d="{L["AP"]}"/><path d="{ROOF}"/>{windows_svg(c)}'
                f'<path d="{L["W"]}" mask="url(#{p}ko)"/><path d="{L["BROKERAGE"]}"/></g>')
        return wrap(VB_PRIMARY, title, defs, body)
    t, ring, key, nvw, nvt, bevel = [s.format(p=p) if isinstance(s, str) else s for s in MODES[mode]]
    bv = f' stroke="{bevel}" stroke-width=".45" stroke-linejoin="round"' if bevel else ''
    defs = (GRAD.format(p=p) if 'url' in t else '') + band_clip(p)
    body = (f'{ring_svg(ring, p=p)}'
            f'<g fill="{key}"{bv}><path d="{SKYLINE}"/><path d="{FRAME}"/><path d="{CHEVRON}"/></g>'
            f'<g fill="{t}"{bv}><path d="{L["RE"]}"/><path d="{L["AP"]}"/></g>'
            f'<path d="{L["W"]}" fill="{nvw}"/>'
            f'<g fill="{t}"{bv}><path d="{ROOF}"/>{windows_svg(t)}</g>'
            f'<path d="{L["BROKERAGE"]}" fill="{nvt}"/>')
    return wrap(VB_PRIMARY, title, defs, body)

def wrap(vb, title, defs, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><defs>{defs}</defs>{body}</svg>\n')

# Derived marks ---------------------------------------------------------------
def emblem(L, scheme, p='e-'):
    """Derived sub-mark: the W + house within the double ring, rings closed into true circles."""
    dx, dy = CX - 145.7, CY - 91.25
    rings = [(80.6, 4.0), (65.3, 3.9)]
    if scheme == 'full-color':
        defs = GRAD.format(p=p); ring, w, roof = f'url(#{p}bz-ring)', f'url(#{p}nv)', f'url(#{p}bz-type)'
        bg = ''
    elif scheme == 'reversed':
        defs = GRAD.format(p=p); ring, w, roof = f'url(#{p}bz-ring)', '#FAFAF9', f'url(#{p}bz-type)'
        bg = ''
    else:
        c = MONO[scheme]; defs = ''; ring = w = roof = c; bg = ''
    rs = "".join(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{ring}" stroke-width="{sw}"/>' for r, sw in rings)
    ko = ''
    if scheme in MONO:
        defs += (f'<mask id="{p}ko" maskUnits="userSpaceOnUse" x="0" y="0" width="512" height="171">'
                 f'<rect width="512" height="171" fill="#fff"/><path d="{ROOF}" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
                 f'{windows_svg("#000")}</mask>')
        ko = f' mask="url(#{p}ko)"'
    body = (f'{bg}{rs}<g transform="translate({dx:.2f} {dy:.2f})"><path d="{L["W"]}" fill="{w}"{ko}/>'
            f'<path d="{ROOF}" fill="{roof}"/>{windows_svg(roof)}</g>')
    r = 84
    return wrap(f"{CX - r - 2} {CY - r - 2} {2 * r + 4} {2 * r + 4}", "REWAP emblem (derived sub-mark)", defs, body)

def wordmark(L, scheme, p='w-'):
    """Derived: REWAP letters only, for spaces where the key and rings cannot be reproduced."""
    if scheme == 'full-color':
        defs = GRAD.format(p=p); t, w, bv = f'url(#{p}bz-type)', f'url(#{p}nv)', ' stroke="#4A2C12" stroke-width=".45" stroke-linejoin="round"'
    elif scheme == 'reversed':
        defs = GRAD.format(p=p); t, w, bv = f'url(#{p}bz-type)', '#FAFAF9', ''
    else:
        c = MONO[scheme]; defs = ''; t = w = c; bv = ''
    ko = ''
    if scheme in MONO:
        defs += (f'<mask id="{p}ko" maskUnits="userSpaceOnUse" x="0" y="0" width="512" height="171">'
                 f'<rect width="512" height="171" fill="#fff"/><g fill="#000" stroke="#000" stroke-width="3" stroke-linejoin="round">'
                 f'<path d="{ROOF}"/><path d="{L["RE"]}"/><path d="{L["AP_solo"]}"/></g>{windows_svg("#000")}</mask>')
        ko = f' mask="url(#{p}ko)"'
    body = (f'<g fill="{t}"{bv}><path d="{L["RE"]}"/><path d="{L["AP_solo"]}"/></g><path d="{L["W"]}" fill="{w}"{ko}/>'
            f'<g fill="{t}"{bv}><path d="{ROOF}"/>{windows_svg(t)}</g>')
    return wrap("25 58 228 66", "REWAP wordmark (derived)", defs, body)

def favicon(L):
    """Derived app/favicon tile: W + house reversed out of Registry navy."""
    s = 1.7
    defs = GRAD.format(p='f-')
    cx, cy = 145.7, 91.25
    body = (f'<rect width="128" height="128" rx="14" fill="#17283F"/>'
            f'<g transform="translate(64 66) scale({s * 0.62}) translate({-cx} {-cy})">'
            f'<path d="{L["W"]}" fill="#FAFAF9"/><path d="{ROOF}" fill="url(#f-bz-type)"/>{windows_svg("url(#f-bz-type)")}</g>')
    return wrap("0 0 128 128", "REWAP", defs, body)

def main():
    cache = os.path.join(os.path.dirname(__file__), '.letters.json')
    if os.path.exists(cache) and '--retrace' not in sys.argv:
        L = json.load(open(cache))
    else:
        L = trace_letters(); json.dump(L, open(cache, 'w'))
    files = {}
    for m in list(MODES) + list(MONO):
        files[f'rewap-logo-{m}.svg'] = primary(L, m, 'REWAP Brokerage')
    for sc in ['full-color', 'reversed', 'mono-navy', 'mono-white', 'mono-black']:
        files[f'derived/rewap-emblem-{sc}.svg'] = emblem(L, sc)
        files[f'derived/rewap-wordmark-{sc}.svg'] = wordmark(L, sc)
    files['derived/rewap-favicon.svg'] = favicon(L)
    os.makedirs(os.path.join(OUT, 'derived'), exist_ok=True)
    for k, v in files.items():
        open(os.path.join(OUT, k), 'w').write(v)
        print(f'{k:48s} {len(v)/1024:6.1f} KB')

if __name__ == '__main__':
    main()
