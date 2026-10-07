"""Authored fine-line elevation drawings — REWAP's placeholder/illustration language.
Navy line on transparent; sit on Plaster. Original drawings, no reference images traced."""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets/img/elevations')
os.makedirs(OUT, exist_ok=True)
N = '#17283F'
def svg(title, w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">'
            f'<g fill="none" stroke="{N}" stroke-width="1.4" stroke-linejoin="miter" stroke-linecap="square">{body}</g></svg>\n')
def rect(x, y, w, h, sw=None):
    s = f' stroke-width="{sw}"' if sw else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}"{s}/>'
def line(x1, y1, x2, y2, sw=None, op=None):
    s = (f' stroke-width="{sw}"' if sw else '') + (f' stroke-opacity="{op}"' if op else '')
    return f'<path d="M{x1} {y1}L{x2} {y2}"{s}/>'
def window(x, y, w, h, panes=(2, 2)):
    b = rect(x, y, w, h) + rect(x - 3, y + h, w + 6, 4, 1)
    cols, rows = panes
    for i in range(1, cols): b += line(x + w * i / cols, y, x + w * i / cols, y + h, .7)
    for j in range(1, rows): b += line(x, y + h * j / rows, x + w, y + h * j / rows, .7)
    return b
def ground(w, y):
    return line(20, y, w - 20, y, 1.6) + "".join(line(x, y + 6, x + 14, y + 6, .6, .5) for x in range(30, w - 40, 26))

# 1. Triple-decker (front gable, stacked porches)
b = ground(600, 360)
b += f'<path d="M188 124L300 46L412 124"/>' + f'<path d="M200 116L300 56L400 116" stroke-width=".7"/>'
b += rect(200, 120, 200, 240)
b += f'<path d="M286 96a14 14 0 0 1 28 0v12h-28z"/>'          # attic lunette
for k in range(3):                                         # three floors
    y0 = 120 + k * 80
    b += line(200, y0, 400, y0, 1.6)
    # porch (left bay)
    b += line(206, y0 + 4, 206, y0 + 80) + line(282, y0 + 4, 282, y0 + 80)
    b += line(202, y0 + 6, 286, y0 + 6, 2.2)                    # porch beam
    b += line(206, y0 + 52, 282, y0 + 52) + line(206, y0 + 56, 282, y0 + 56, .7)
    b += "".join(line(x, y0 + 56, x, y0 + 80, .6) for x in range(212, 282, 7))
    b += rect(224, y0 + 18, 22, 52, .9)                         # porch door
    b += window(254, y0 + 18, 18, 30, (1, 2))
    # paired windows (right bay)
    b += window(306, y0 + 18, 30, 46) + window(352, y0 + 18, 30, 46)
    b += "".join(line(292, y, 400, y, .45, .55) for y in range(y0 + 10, y0 + 80, 8))
b += rect(214, 352, 60, 8, 1) + rect(222, 344, 44, 8, 1)       # steps
open(os.path.join(OUT, 'triple-decker.svg'), 'w').write(svg('Elevation drawing: three-decker house', 600, 400, b))

# 2. Mill building (brick block, stair tower, stack)
b = ground(600, 360)
b += rect(50, 170, 500, 190) + line(44, 170, 556, 170, 2.4) + line(50, 178, 550, 178, .7)
for f in range(4):
    y = 186 + f * 44
    for i in range(12):
        x = 62 + i * 39.5
        if x + 24 > 260 and x < 340: continue
        b += f'<path d="M{x} {y+32}V{y+8}Q{x+12} {y} {x+24} {y+8}V{y+32}Z"/>' + line(x + 12, y + 3, x + 12, y + 32, .6)
    b += line(50, y + 38, 550, y + 38, .45, .6)
b += rect(266, 104, 68, 256) + f'<path d="M260 104L300 66L340 104Z"/>' + line(258, 104, 342, 104, 2.2)
for y in (128, 186, 244, 302):
    b += f'<path d="M286 {y+34}V{y+10}Q300 {y} 314 {y+10}V{y+34}Z"/>'
b += rect(504, 30, 20, 140) + line(500, 30, 528, 30, 2.2) + "".join(line(504, y, 524, y, .5, .6) for y in range(42, 170, 12))
b += f'<path d="M282 360V330Q300 318 318 330V360"/>'
open(os.path.join(OUT, 'mill.svg'), 'w').write(svg('Elevation drawing: brick mill building', 600, 400, b))

# 3. Center-chimney colonial (five-bay, side gable)
b = ground(600, 360)
b += f'<path d="M136 222L206 150H394L464 222"/>' + line(130, 222, 470, 222, 2.2)
b += rect(150, 222, 300, 138) + rect(288, 118, 24, 34) + line(284, 118, 316, 118, 2)
xs = [168, 220, 285, 350, 402]
for x in xs:
    b += window(x, 236, 30, 44, (2, 3))
    if x != 285: b += window(x, 296, 30, 50, (2, 3))
b += rect(284, 302, 32, 58) + f'<path d="M280 302a20 14 0 0 1 40 0z"/>' + line(300, 302, 300, 360, .7)
b += rect(274, 290, 52, 6, 1)
b += "".join(line(150, y, 450, y, .45, .5) for y in range(232, 360, 9))
open(os.path.join(OUT, 'colonial.svg'), 'w').write(svg('Elevation drawing: center-chimney colonial', 600, 400, b))
print('ok')

# 4. Cape (one-and-a-half story, side gable, center door, dormers)
b = ground(600, 360)
b += '<path d="M140 270L230 196H370L460 270"/>' + line(134, 270, 466, 270, 2.2) + rect(156, 270, 288, 90)
for x in (236, 330):
    b += f'<path d="M{x} 222V204L{x+17} 190L{x+34} 204V222Z"/>' + window(x + 7, 206, 20, 16, (2, 1))
b += rect(291, 178, 18, 20) + line(287, 178, 313, 178, 2)
for x in (178, 222, 352, 396):
    b += window(x, 290, 26, 40, (2, 3))
b += rect(284, 286, 32, 74) + rect(278, 280, 44, 6, 1) + line(300, 286, 300, 360, .7)
b += "".join(line(156, y, 444, y, .45, .5) for y in range(278, 360, 8))
open(os.path.join(OUT, 'cape.svg'), 'w').write(svg('Elevation drawing: Cape house', 600, 400, b))

# 5. Brick row house (three stories, bay, cornice, stoop)
b = ground(600, 360)
b += rect(190, 110, 220, 250) + line(180, 110, 420, 110, 3) + line(186, 118, 414, 118, 1) + "".join(line(x, 110, x, 118, .7) for x in range(196, 410, 12))
b += '<path d="M290 360V150H404V360"/>'                       # bay
for k, y in enumerate((150, 220, 290)):
    b += line(290, y, 404, y, 1.2)
    for x in (300, 334, 368):
        if k == 2 and x == 300: continue
        b += window(x, y + 12, 26, 46, (1, 2))
for y in (140, 210):
    b += window(214, y, 30, 48, (2, 2)) + f'<path d="M210 {y-4}H248" stroke-width="2"/>'
b += rect(212, 290, 44, 70) + f'<path d="M208 290a26 14 0 0 1 52 0z"/>'   # door with transom
b += rect(196, 344, 76, 8, 1) + rect(204, 336, 60, 8, 1)       # stoop
b += "".join(line(190, y, 290, y, .4, .45) for y in range(126, 360, 7))
open(os.path.join(OUT, 'rowhouse.svg'), 'w').write(svg('Elevation drawing: brick row house', 600, 400, b))
print('ok2')
