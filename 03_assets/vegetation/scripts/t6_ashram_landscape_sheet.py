"""Decision Sheet 01 §4 · Ashram landscaping overlay on the approved-for-review layout plan v3 (local origin = courtyard centre,
north up, 4.67 px / m in the 2300 px plan). Draws: landmark Peepal (canopy + trunk) on its stone sitting platform in the courtyard,
the Ashram garden (only place for Tulsi + Marigold), grass / grove zones. Output: 02_world/ashram/00_REFERENCE/ASHRAM_landscaping_plan_v1.png"""
import os
from PIL import Image, ImageDraw, ImageFont
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '02_world', 'ashram', '00_REFERENCE'))
im = Image.open(os.path.join(R, 'ASHRAM_layout_plan_v3.png')).convert('RGBA')
OX, OY, PPM = 699, 736, 4.67
P = lambda x, y: (OX + x * PPM, OY - y * PPM)
F = lambda n, b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/' + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), n)
ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
def rect(x0, y0, x1, y1, fill, outline, w=3):
    a, b = P(x0, y1), P(x1, y0); d.rectangle([a[0], a[1], b[0], b[1]], fill=fill, outline=outline, width=w)
def circ(x, y, r, fill, outline, w=3):
    a, b = P(x - r, y + r), P(x + r, y - r); d.ellipse([a[0], a[1], b[0], b[1]], fill=fill, outline=outline, width=w)
# Peepal: canopy Ø ≈ 28–34 m (library hero 28.3 × 33.7 m) centred on the courtyard; trunk Ø 3 m; stone platform (chabutra) 9 × 9 m
circ(0, 0, 15.5, (60, 140, 50, 70), (40, 110, 40, 255), 4)
rect(-4.5, -4.5, 4.5, 4.5, (205, 190, 160, 230), (120, 100, 70, 255), 3)
circ(0, 0, 1.5, (90, 70, 50, 255), (60, 40, 30, 255), 2)
# garden: two beds flanking the gate path, south lawn (x ±6..±28, y −30..−52); Tulsi = raised planters on the path side
for sx in (-1, 1):
    x0, x1 = (6, 28) if sx > 0 else (-28, -6)
    rect(x0, -52, x1, -30, (120, 170, 70, 150), (240, 200, 60, 255), 4)
    for k in range(5):                                         # marigold rows (orange)
        yy = -33 - k * 4.2; a, b = P(min(x0, x1) + 2, yy), P(max(x0, x1) - 6, yy)
        d.line([a, b], fill=(240, 138, 18, 255), width=7)
    for k in range(3):                                         # tulsi planters (raised, 1.2 m)
        cx = 8.5 * sx; cy = -34 - k * 7.5
        a, b = P(cx - .8, cy + .8), P(cx + .8, cy - .8); d.rectangle([a[0] - 3, a[1] - 3, b[0] + 3, b[1] + 3], fill=(62, 106, 44, 255), outline=(250, 250, 240, 255), width=2)
im = Image.alpha_composite(im, ov); d = ImageDraw.Draw(im)
def tag(x, y, t, dx=0, dy=0):
    a = P(x, y); d.rounded_rectangle([a[0] + dx - 6, a[1] + dy - 4, a[0] + dx + d.textlength(t, font=F(19, True)) + 6, a[1] + dy + 26], 6, fill=(20, 20, 20, 220))
    d.text((a[0] + dx, a[1] + dy), t, fill=(255, 230, 120), font=F(19, True))
tag(16, 12, 'A  landmark Peepal + stone sitting platform', 0, 0)
tag(-22, -54, 'B  Ashram garden (2 beds)', 0, 4)
# legend panel (right side of the plan, under the zone list)
x0, y0 = 1440, 1180
d.rectangle([x0 - 20, y0 - 20, 2280, 1545], fill=(17, 18, 22, 255))
d.text((x0, y0), 'LANDSCAPING — Decision Sheet 01 (APPROVED)', fill=(255, 210, 90), font=F(26, True))
L = ['A  ONE landmark Peepal (Ficus religiosa) at the courtyard centre (= "sacred tree"',
     '    of zone 6), canopy Ø ≈ 30 m, H ≈ 24 m; stone sitting platform 9 × 9 m, 0.6 m high',
     'B  Ashram garden = the ONLY place for Tulsi (raised planters) + Marigold (beds)',
     '    two beds 22 × 22 m flanking the gate path — position PROPOSED',
     'green circle = Peepal canopy · orange = marigold rows · dark squares = tulsi planters']
for i, t in enumerate(L):
    d.text((x0, y0 + 44 + i * 32), t, fill=(230, 230, 225), font=F(18))
out = os.path.join(R, 'ASHRAM_landscaping_plan_v1.png'); im.convert('RGB').save(out, optimize=True); print('SAVED', out)
