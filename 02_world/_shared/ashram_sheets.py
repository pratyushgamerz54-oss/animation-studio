"""Compose the Ashram concept sheets from the blockout renders.

Run:  python3 02_world/_shared/ashram_sheets.py
Out:  02_world/ashram/00_REFERENCE/ASHRAM_concept_sheet_v1.png   (all camera views)
      02_world/ashram/00_REFERENCE/ASHRAM_layout_plan_v1.png     (bird's-eye with labelled zones, grid, scale)
      02_world/ashram/00_REFERENCE/ASHRAM_lighting_sheet_v1.png  (day vs night)
      02_world/ashram/00_REFERENCE/ASHRAM_materials_sheet_v1.png (material palette swatches)
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import worldgen as wg

V2 = 'v1' not in sys.argv
A = os.path.join(HERE, '..', 'ashram'); R = os.path.join(A, '09_RENDER', 'concept_v2' if V2 else 'concept_v1'); O = os.path.join(A, '00_REFERENCE')
VER = 'v2' if V2 else 'v1'; DAY = 'golden' if V2 else 'day'
F = lambda p, s: ImageFont.truetype(p, s)
BG = (16, 18, 24); INK = (240, 230, 205); DIM = (170, 170, 180); GOLD = (255, 214, 90)


def head(d, W, title, sub):
    d.rectangle((0, 0, W, 120), fill=(12, 13, 18)); d.rectangle((0, 116, W, 120), fill=(214, 166, 60))
    d.text((40, 18), title, font=F(wg.FS, 48), fill=INK); d.text((40, 80), sub, font=F(wg.FR, 22), fill=DIM)
    d.text((W - 40, 30), 'PROPOSAL — awaiting Director approval', font=F(wg.FB, 24), fill=(255, 190, 70), anchor='ra')


def img(n, w):
    p = os.path.join(R, n)
    if not os.path.exists(p):
        im = Image.new('RGB', (w, int(w * 9 / 16)), (40, 40, 48)); ImageDraw.Draw(im).text((20, 20), 'missing ' + n, fill=(255, 80, 80)); return im
    im = Image.open(p).convert('RGB'); return im.resize((w, int(w * im.height / im.width)), Image.LANCZOS)


VIEWS = [('CAM_01_WIDE_ESTABLISHING', 'Wide establishing — valley, lake, northern range'), ('CAM_02_FRONT_GATE', 'Front — approach to the gate'),
         ('CAM_03_COURTYARD', 'Courtyard · character height 1.65 m'), ('CAM_04_HALL_DETAIL', 'Detail — verandah, carved pillars, brackets, eaves'),
         ('CAM_05_PAVILION_LAKE', 'Meditation pavilion + lake ghat'), ('CAM_06_BACK_FROM_SLOPE', 'Back — from the forest slope'),
         ('CAM_07_SIDE_WEST', 'Side — west'), ('CAM_08_TRAINING', 'Training ground (Ø 44 m)'), ('CAM_09_BIRDSEYE_ORTHO', 'Bird’s-eye (ortho)')]


def concept():
    W = 2600
    big = img(VIEWS[0][0] + f'_{DAY}.png', W - 80)
    tw = (W - 80 - 2 * 30) // 3
    th = int(tw * 9 / 16)
    H = 140 + big.height + 60 + 3 * (th + 60) + 40
    S = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(S)
    head(d, W, f'ASHRAM — ENVIRONMENT CONCEPT {VER}', 'Renders of the real 3D scene (ASHRAM_concept_v002.blend) · direction: “Himalayan foothill gurukul” · golden hour · '
         'same model in every view · red cylinders = 1.75 m scale figures')
    S.paste(big, (40, 140)); d.text((56, 152), VIEWS[0][1], font=F(wg.FB, 28), fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    y0 = 140 + big.height + 40
    for k, (n, cap) in enumerate(VIEWS[1:]):
        x = 40 + (k % 3) * (tw + 30); y = y0 + (k // 3) * (th + 60)
        S.paste(img(n + f'_{DAY}.png', tw), (x, y)); d.text((x, y + th + 8), cap, font=F(wg.FB, 22), fill=INK)
    S.save(os.path.join(O, f'ASHRAM_concept_sheet_{VER}.png'), optimize=True)


ZONES = [((0, 34), '1', 'Main hall (Headmaster / assembly)'), ((-42, 0), '2', 'Student residence — west'), ((42, 0), '3', 'Student residence — east'),
         ((-38, 44), '4', 'Service hall (kitchen / stores)'), ((38, 44), '5', 'Study hall / library'), ((0, 4), '6', 'Courtyard + sacred tree'),
         ((0, -62), '7', 'Entrance gate (stone torana)'), ((0, -100), '8', 'Training ground (Ø 44 m)'), ((62, -78), '9', 'Meditation pavilion'),
         ((62, -96), '10', 'Lake ghat (steps into the water)'), ((-60, 30), '11', 'Boundary wall (modular 4 m segments)')]


def layout():
    top = os.path.join(R, ('CAM_09_BIRDSEYE_ORTHO' if V2 else 'CAM_10_BIRDSEYE_ORTHO') + f'_{DAY}.png')
    base = Image.open(top).convert('RGB') if os.path.exists(top) else Image.new('RGB', (1400, 1400), (60, 80, 50))
    N = base.width; scale = 300.0
    P = lambda x, y: ((x / scale + .5) * N, (-(y + 20) / scale + .5) * N)
    W = N + 900
    S = Image.new('RGB', (W, N + 160), BG); d = ImageDraw.Draw(S)
    head(d, W, f'ASHRAM — BIRD’S-EYE LAYOUT PLAN {VER}', 'Orthographic top view of the 3D blockout · north up · 300 m frame · grid 25 m · local origin = courtyard centre')
    S.paste(base, (0, 140))
    ov = Image.new('RGBA', base.size, (0, 0, 0, 0)); o = ImageDraw.Draw(ov)
    for g in range(-150, 151, 25):
        a = P(g, -170)[0]; o.line((a, 0, a, N), fill=(255, 255, 255, 45))
        b = P(0, g - 20)[1]; o.line((0, b, N, b), fill=(255, 255, 255, 45))
    for (x, y), num, lab in ZONES:
        px, py = P(x, y)
        o.ellipse((px - 22, py - 22, px + 22, py + 22), fill=(255, 214, 90, 235), outline=(40, 25, 0, 255), width=3)
        o.text((px, py), num, font=F(wg.FB, 22), fill=(30, 20, 0, 255), anchor='mm')
    S.paste(ov, (0, 140), ov)
    # scale bar + north arrow on the image
    x0, y0 = 40, 140 + N - 60
    d.rectangle((x0, y0, x0 + 50 / scale * N, y0 + 14), fill=(255, 255, 255)); d.text((x0, y0 + 20), '50 m', font=F(wg.FB, 22), fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    cx, cy = N - 70, 220
    d.polygon([(cx, cy - 50), (cx - 14, cy), (cx + 14, cy)], fill=(255, 255, 255)); d.text((cx, cy - 86), 'N', font=F(wg.FB, 28), fill=(255, 255, 255), anchor='ma', stroke_width=3, stroke_fill=(0, 0, 0))
    x = N + 40; y = 180
    d.text((x, y), 'ZONES (all PROPOSED)', font=F(wg.FB, 30), fill=GOLD); y += 54
    for (_, _), num, lab in ZONES:
        d.ellipse((x, y, x + 34, y + 34), fill=GOLD); d.text((x + 17, y + 17), num, font=F(wg.FB, 18), fill=(30, 20, 0), anchor='mm')
        d.text((x + 50, y + 4), lab, font=F(wg.FR, 23), fill=INK); y += 48
    y += 20
    notes = ['CONFIRMED: the Ashram is associated with the Headmaster,', 'students and training.',
             'PROPOSED: every building, its use and position.', 'NOT CONFIRMED: interiors, number of students,',
             'other buildings, exact surroundings.', '',
             'Compound ≈ 120 m x 125 m (wall), main axis north–south:', 'gate → courtyard → main hall, mountains behind.',
             'Training ground outside the gate = space for power', 'and portal VFX without damaging buildings.',
             'Lake ghat + pavilion = calm contrast location.']
    for t in notes:
        d.text((x, y), t, font=F(wg.FR, 21), fill=DIM if not t.startswith(('CONFIRMED', 'PROPOSED', 'NOT')) else INK); y += 32
    S.save(os.path.join(O, f'ASHRAM_layout_plan_{VER}.png'), optimize=True)


def lighting():
    pairs = [('CAM_01_WIDE_ESTABLISHING', 'Wide'), ('CAM_02_FRONT_GATE', 'Front gate'), ('CAM_03_COURTYARD', 'Courtyard')] if V2 else \
        [('CAM_01_WIDE_ESTABLISHING', 'Wide'), ('CAM_02_FRONT', 'Front'), ('CAM_06_GROUND_LEVEL', 'Ground level')]
    tw = 1180; th = int(tw * 9 / 16)
    W = 40 + 2 * (tw + 30) + 10
    S = Image.new('RGB', (W, 140 + 3 * (th + 60) + 20), BG); d = ImageDraw.Draw(S)
    head(d, W, f'ASHRAM — LIGHTING TEST {VER}', 'Golden hour: low west sun + physical sky + haze + lake mist · Night: moon + lanterns + window glow · story time of day = NOT CONFIRMED')
    for k, (n, cap) in enumerate(pairs):
        for j, tod in enumerate((DAY, 'night')):
            x = 40 + j * (tw + 30); y = 140 + k * (th + 60)
            S.paste(img(f'{n}_{tod}.png', tw), (x, y)); d.text((x, y + th + 8), f'{cap} — {tod.upper()}', font=F(wg.FB, 22), fill=INK)
    S.save(os.path.join(O, f'ASHRAM_lighting_sheet_{VER}.png'), optimize=True)


def materials():
    sw = [('Coursed stone', '#8E8372', 'plinths, gate, ghat · rough .8'), ('Rough stone', '#6A6156', 'gate pillars, rock · rough .9'),
          ('Lime plaster', '#E6D8BE', 'walls · rough .8'), ('Timber', '#6B4426', 'pillars, bands · rough .55'),
          ('Dark timber', '#4A2E19', 'pillar caps · rough .6'), ('Clay roof tile', '#A4512F', 'roofs · rough .6'),
          ('Brass', '#C9A040', 'finials · metal 1, rough .3'), ('Prayer cloth', '#C8452E', 'flags · rough .8'),
          ('Path earth', '#A88A5E', 'paths, training ground'), ('Grass', '#6E8F45', 'valley floor'), ('Foliage', '#3E6B32', 'trees'),
          ('Lake water', '#2B5D73', 'rough .04'), ('Lantern glow', '#FFB35A', 'emission (night)'), ('Snow', '#EEF2F5', 'peaks > 1 050 m (tile)')]
    W = 2400; S = Image.new('RGB', (W, 140 + ((len(sw) - 1) // 4 + 1) * 170 + 40), BG); d = ImageDraw.Draw(S)
    head(d, W, f'ASHRAM — MATERIAL PALETTE {VER}', 'PBR standard in WORLD_BIBLE.md §6 · blockout uses procedural shaders, final assets get baked BaseColor / Roughness / Normal / AO')
    for k, (n, hx, note) in enumerate(sw):
        x = 40 + (k % 4) * 590; y = 150 + (k // 4) * 170
        d.rounded_rectangle((x, y, x + 140, y + 140), 14, fill=tuple(int(v) for v in wg.hexrgb(hx)))
        d.text((x + 160, y + 10), n, font=F(wg.FB, 26), fill=INK); d.text((x + 160, y + 50), hx, font=F(wg.FR, 22), fill=INK)
        d.text((x + 160, y + 84), note, font=F(wg.FR, 18), fill=DIM)
    S.save(os.path.join(O, f'ASHRAM_materials_sheet_{VER}.png'), optimize=True)


if __name__ == '__main__':
    concept(); layout(); lighting(); materials(); print('wrote ashram sheets')
