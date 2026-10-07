"""REWAP Concept 1 palette: OKLCH source of truth -> hex fallbacks + WCAG contrast table."""
import math, json, sys
P = {
 # name: (L, C, h, role)
 'night':        (0.205, 0.035, 256, 'Deepest navy; text on light, dark fields'),
 'navy':         (0.275, 0.048, 256, 'Registry Navy — primary; from the mark\'s W'),
 'navy-700':     (0.345, 0.052, 256, 'Navy hover / pressed'),
 'navy-500':     (0.480, 0.045, 256, 'Info, secondary UI on light'),
 'navy-200':     (0.860, 0.018, 256, 'Tint, selected rows'),
 'navy-100':     (0.935, 0.010, 256, 'Faint tint'),
 'bronze-700':   (0.480, 0.075, 62,  'Bronze Deep — the only bronze allowed as text on light'),
 'bronze':       (0.630, 0.085, 65,  'Bronze — the mark\'s flat color; rules and large marks only'),
 'bronze-300':   (0.790, 0.070, 70,  'Bronze Light — accents and text on navy'),
 'bronze-100':   (0.935, 0.025, 75,  'Bronze tint'),
 'gallery':      (0.985, 0.002, 90,  'Gallery — page ground'),
 'plaster':      (0.962, 0.004, 85,  'Plaster — alternate surface'),
 'limestone':    (0.915, 0.006, 85,  'Limestone — strong rule, input border on plaster'),
 'hairline':     (0.880, 0.006, 85,  'Hairline — default 1px rule'),
 'granite':      (0.600, 0.012, 256, 'Granite — disabled, decorative meta (not body text)'),
 'slate':        (0.470, 0.020, 256, 'Slate — secondary text'),
 'ink':          (0.255, 0.030, 256, 'Ink — body text'),
 'success':      (0.480, 0.090, 155, 'Status: success'),
 'warning':      (0.500, 0.100, 70,  'Status: warning (text/icon)'),
 'warning-fill': (0.880, 0.080, 85,  'Status: warning surface'),
 'error':        (0.510, 0.165, 27,  'Status: error'),
 'white':        (1.0, 0, 0,        'Pure white for knock-outs'),
}
def oklch_to_srgb(L, C, h):
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    def enc(x):
        x = min(max(x, 0), 1)
        return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
    return tuple(round(enc(v) * 255) for v in (r, g, bb)), (r, g, bb)
def rel(rgb):
    def lin(c):
        c /= 255; return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = map(lin, rgb); return 0.2126 * r + 0.7152 * g + 0.0722 * b
def contrast(a, b):
    la, lb = sorted([rel(a), rel(b)], reverse=True); return (la + 0.05) / (lb + 0.05)
out = {}
for k, (L, C, h, role) in P.items():
    rgb, _ = oklch_to_srgb(L, C, h)
    out[k] = {'oklch': f'oklch({L*100:.1f}% {C:.3f} {h})', 'hex': '#%02X%02X%02X' % rgb, 'rgb': rgb, 'role': role}
pairs = [('ink','gallery'),('ink','plaster'),('slate','gallery'),('slate','plaster'),('navy','gallery'),('bronze-700','gallery'),('bronze-700','plaster'),
         ('bronze','gallery'),('granite','gallery'),('gallery','navy'),('bronze-300','navy'),('navy-200','navy'),('bronze','navy'),('gallery','night'),('bronze-300','night'),
         ('success','gallery'),('warning','gallery'),('error','gallery'),('night','warning-fill'),('night','bronze-100'),('hairline','gallery'),('limestone','gallery'),('slate','limestone')]
table = []
for fg, bg in pairs:
    c = contrast(out[fg]['rgb'], out[bg]['rgb'])
    use = 'AA body' if c >= 4.5 else ('AA large / UI' if c >= 3 else 'decorative only')
    table.append({'fg': fg, 'bg': bg, 'ratio': round(c, 2), 'use': use})
if __name__ == '__main__':
    for k, v in out.items(): print(f"{k:13s} {v['hex']}  {v['oklch']}")
    for t in table: print(f"{t['fg']:12s} on {t['bg']:12s} {t['ratio']:5.2f}  {t['use']}")
    json.dump({'colors': out, 'contrast': table}, open(sys.argv[1] if len(sys.argv) > 1 else '/dev/null', 'w'), indent=1)
