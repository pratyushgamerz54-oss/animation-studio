"""Compose Pratyush's design-sheet pages from the raw renders (PIL only).

Run:  python3 01_characters/pratyush/compose_sheet.py
Out:  01_characters/pratyush/design/PRATYUSH_sheet_0N_<page>.png
"""
import os, sys, json, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pratyush_spec import SPEC, PAL

RAW = os.path.join(HERE, 'design', 'raw')
OUT = os.path.join(HERE, 'design')
MEAS = json.load(open(os.path.join(HERE, 'qc', 'measurements.json')))

BG, PANEL, INK, DIM, ACC = (22, 25, 31), (34, 38, 46), (235, 238, 243), (150, 158, 170), (46, 168, 255)
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FM = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
F = lambda p, s: ImageFont.truetype(p, s)
W = 2400


def raw(n):
    return Image.open(os.path.join(RAW, n)).convert('RGBA')


def fit(im, w=None, h=None):
    if w and h:
        s = min(w / im.width, h / im.height)
    elif w:
        s = w / im.width
    else:
        s = h / im.height
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)


def bloom(im, thresh=0.62, k1=0.7, k2=0.55):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    lum = a.max(axis=2, keepdims=True)
    bright = (np.clip(lum - thresh, 0, 1) / (1 - thresh)) * a
    b = Image.fromarray((bright * 255).astype(np.uint8))
    b1 = np.asarray(b.filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
    b2 = np.asarray(b.filter(ImageFilter.GaussianBlur(28))).astype(np.float32) / 255
    o = np.clip(a + k1 * b1 + k2 * b2, 0, 1)
    return Image.fromarray((o * 255).astype(np.uint8)).convert('RGBA')


class Page:
    def __init__(self, key, title, h):
        self.key, self.im = key, Image.new('RGBA', (W, h), BG)
        self.d = ImageDraw.Draw(self.im)
        d = self.d
        d.rectangle((0, 0, W, 96), fill=(14, 16, 21))
        d.rectangle((0, 92, W, 96), fill=ACC)
        d.text((40, 20), 'PRATYUSH', font=F(FB, 44), fill=INK)
        d.text((330, 34), f'Hero 2  ·  Design Sheet v1  ·  {title}', font=F(FR, 28), fill=DIM)
        d.text((W - 40, 34), 'PROPOSAL — awaiting Director approval', font=F(FB, 24), fill=(255, 196, 64),
               anchor='ra')
        d.text((40, h - 40), 'Powers (confirmed): Super Speed · Magical Portal · Lightning     '
               '|  Appearance, age, costume & colours are proposals (U-04)     |  3D renders of the real '
               'Blender model pratyush_v001.blend', font=F(FR, 20), fill=DIM)

    def paste(self, im, x, y, label=None, panel=True, sub=None):
        if panel:
            self.d.rounded_rectangle((x - 8, y - 8, x + im.width + 8, y + im.height + 8), 14, fill=PANEL)
        self.im.alpha_composite(im, (int(x), int(y)))
        if label:
            self.d.text((x + im.width / 2, y + im.height + 18), label, font=F(FB, 24), fill=INK, anchor='ma')
        if sub:
            self.d.text((x + im.width / 2, y + im.height + 50), sub, font=F(FR, 19), fill=DIM, anchor='ma')

    def text(self, x, y, s, size=22, bold=False, color=INK, mono=False):
        self.d.text((x, y), s, font=F(FM if mono else (FB if bold else FR), size), fill=color)

    def save(self, n):
        p = os.path.join(OUT, f'PRATYUSH_sheet_{n:02d}_{self.key}.png')
        self.im.convert('RGB').save(p, optimize=True)
        print('wrote', p)


def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- pages
def p_turn():
    pg = Page('turnaround', 'Full-body turnaround (neutral pose, orthographic)', 1020)
    views = [('front', 'Front'), ('three_quarter_front', '3/4 Front'), ('right', 'Right side'),
             ('three_quarter_back', '3/4 Back'), ('back', 'Back'), ('left', 'Left side')]
    x = 50
    for k, lab in views:
        im = fit(raw(f'turn_{k}.png'), h=780)
        pg.paste(im, x + (370 - im.width) / 2, 130, lab)
        x += 385
    return pg


def p_poses():
    pg = Page('poses_measurements', 'T-pose · A-pose · Neutral + measurement guide', 1080)
    H = 760
    t = fit(raw('pose_T.png'), h=H); pg.paste(t, 50, 130, 'T-pose (modelling & rigging)')
    a = fit(raw('pose_A.png'), h=H); pg.paste(a, 50 + t.width + 40, 130, 'A-pose (deformation checks)')
    n = raw('pose_NEUTRAL.png')
    s = H / n.height
    n = fit(n, h=H)
    nx, ny = 50 + t.width + a.width + 80, 130
    pg.paste(n, nx, ny, 'Neutral + head units')
    d = pg.d
    ppm = 1120 / 2.0 * s            # pixels per metre (ortho 2.0 m tall, 1120 px)
    zpx = lambda z: ny + (560 - (z - 1.0) * 560) * s
    hh = MEAS['head_height_m']
    for i in range(9):
        z = i * hh
        if z > MEAS['height_with_hair_m'] + 0.01:
            break
        y = zpx(z)
        d.line((nx - 6, y, nx + n.width + 6, y), fill=(90, 170, 255, 255) if i % 2 == 0 else (70, 110, 160, 255), width=2)
        d.text((nx + n.width + 14, y - 12), f'{i}', font=F(FB, 20), fill=ACC)
    ytop, ybot = zpx(MEAS['head_top_z']), zpx(0)
    d.line((nx - 30, ytop, nx - 30, ybot), fill=(255, 196, 64), width=3)
    d.text((nx - 40, (ytop + ybot) / 2), f"{MEAS['height_no_hair_m'] * 100:.1f} cm", font=F(FB, 22),
           fill=(255, 196, 64), anchor='rm')
    # table
    tx = nx + n.width + 80
    pg.text(tx, 140, 'BODY PROPORTIONS', 30, True, ACC)
    rows = [
        ('Height (no hair)', f"{SPEC['height_m'] * 100:.0f} cm", f"{MEAS['height_no_hair_m'] * 100:.1f} cm"),
        ('Height (with hair)', '—', f"{MEAS['height_with_hair_m'] * 100:.1f} cm"),
        ('Head height', f"{SPEC['head_height_m'] * 100:.1f} cm", f"{MEAS['head_height_m'] * 100:.1f} cm"),
        ('Head-to-body ratio', '7.5 heads', f"{MEAS['heads_tall']} heads"),
        ('Shoulder width', f"{SPEC['shoulder_width_m'] * 100:.0f} cm", f"{MEAS['shoulder_width_m'] * 100:.1f} cm"),
        ('Chest width', f"{SPEC['chest_width_m'] * 100:.0f} cm", f"{MEAS['chest_width_m'] * 100:.1f} cm"),
        ('Hip width', '—', f"{MEAS['hip_width_m'] * 100:.1f} cm"),
        ('Arm length', f"{SPEC['arm_length_m'] * 100:.0f} cm", f"{MEAS['arm_length_m'] * 100:.1f} cm"),
        ('Leg length (hip→floor)', f"{SPEC['leg_length_m'] * 100:.0f} cm", f"{MEAS['leg_length_m'] * 100:.1f} cm"),
        ('Hand length', f"{SPEC['hand_length_m'] * 100:.0f} cm", 'by build (palm 8.5 + finger 10)'),
        ('Foot length', f"{SPEC['foot_length_m'] * 100:.0f} cm", 'by build'),
    ]
    pg.text(tx, 195, f"{'':26}{'SPEC':>12}{'MEASURED (model)':>22}", 20, mono=True, color=DIM)
    for i, (k, a_, b_) in enumerate(rows):
        pg.text(tx, 230 + i * 38, f'{k:26}{a_:>12}{b_:>22}', 21, mono=True)
    y = 230 + len(rows) * 38 + 30
    pg.text(tx, y, 'BUILD', 26, True, ACC)
    pg.text(tx, y + 40, SPEC['body_type'], 21)
    pg.text(tx, y + 80, 'SILHOUETTE', 26, True, ACC)
    for j, line in enumerate(['Upward-swept hair spikes + high armoured collar', '+ angular shoulder plates',
                              '= forward-leaning "arrow" read, distinct from Hero 1']):
        pg.text(tx, y + 120 + j * 32, line, 21)
    pg.text(tx, y + 240, 'Measured values are read from the evaluated Blender', 19, color=DIM)
    pg.text(tx, y + 266, 'mesh by render_sheet.py (qc/measurements.json).', 19, color=DIM)
    return pg


def p_face():
    pg = Page('face', 'Face design · hairline · eye', 1260)
    views = [('front', 'Face — front'), ('three_quarter', 'Face — 3/4'), ('side', 'Face — side'),
             ('back_three_quarter', 'Hairstyle — back 3/4')]
    x = 50
    for k, lab in views:
        im = fit(raw(f'face_{k}.png'), h=600)
        pg.paste(im, x, 130, lab)
        x += im.width + 40
    e = fit(raw('face_eye_detail.png'), h=300)
    pg.paste(e, 50, 830, 'Eye detail (left eye)')
    tx = 50 + e.width + 80
    notes = [
        ('EYES', f"Dark-brown iris {PAL['eye']}, almond shape from upper/lower lid shells; glow {PAL['power_eye']} when powered"),
        ('BROWS', 'Straight, slightly angled up at the outer end; tapered; hair colour'),
        ('NOSE / LIPS', 'Straight bridge, rounded tip, soft alae; medium lips, upper lip thinner'),
        ('JAW / EARS', 'Defined jaw angle, rounded chin; ears from brow line to nose base'),
        ('PROPORTIONS', 'Eye line at 1/2 head height · eye spacing = 1 eye width · mouth at ~2/3 of lower face'),
        ('HAIR', f"Near-black {PAL['hair']} spiky ribbon clumps swept up & back; 1 electric-blue streak {PAL['hair_streak']} in fringe"),
    ]
    for i, (k, v) in enumerate(notes):
        pg.text(tx, 840 + i * 42, f'{k:13}', 22, True, ACC)
        pg.text(tx + 200, 840 + i * 42, v, 21)
    return pg


def p_expr():
    pg = Page('expressions', 'Facial expressions (face rig: lids, brows, mouth shape keys)', 1140)
    fs = sorted(glob.glob(os.path.join(RAW, 'expr_*.png')))
    for i, f in enumerate(fs):
        im = fit(Image.open(f).convert('RGBA'), h=400)
        x = 50 + (i % 6) * (im.width + 40)
        y = 130 + (i // 6) * 490
        lab = os.path.basename(f)[8:-4].replace('_', ' ').title()
        pg.paste(im, x, y, f'{i + 1}. {lab}' if lab != 'Blink' else 'Extra: Blink')
    return pg


COST_TEXT = {
    'suit': ('Stretch technical knit (4-way)', f"Base {PAL['suit']} rough 0.45 sheen 0.35; piping {PAL['accent']} emissive 0.8",
             'Tight-fit: NO cloth sim — skinned to rig; corrective shape keys at elbow/knee'),
    'armor': ('Moulded composite plates', f"{PAL['armor']} metallic 0.65 rough 0.32; edge light {PAL['accent']}",
              'Rigid: bone-parented / skinned 1:1, no sim'),
    'boots': ('Armoured synthetic leather', f"{PAL['boot']} rough 0.4; sole & bands {PAL['shoe_sole']}", 'Rigid, skinned to foot/toe'),
    'gloves': ('Grip synthetic', f"{PAL['glove']} rough 0.45", 'Skinned per finger bone'),
    'belt': ('Plate belt + buckle', f"{PAL['armor']} / {PAL['metal']} metal", 'Rigid'),
    'bracers': ('Brushed metal + energy core', f"{PAL['metal']} metal 1.0 rough 0.25; core {PAL['power_glow']} emission",
                'Rigid on forearm'),
    'hair': ('Stylised clump geometry', f"{PAL['hair']} rough 0.42 sheen 0.5", 'Optional spring-bone jiggle on long spikes'),
}


def p_costume():
    pg = Page('costume', 'Costume & accessories breakdown', 1240)
    from render_sheet import COSTUME
    for i, (k, lab, _) in enumerate(COSTUME):
        im = fit(raw(f'costume_{k}.png'), h=300)
        x = 50 + (i % 4) * 590
        y = 130 + (i // 4) * 540
        pg.paste(im, x, y)
        tl, tline = [], ''
        for w_ in lab.split():
            if len(tline) + len(w_) > 19:
                tl.append(tline); tline = ''
            tline += w_ + ' '
        tl.append(tline)
        for q, l in enumerate(tl[:2]):
            pg.text(x + 330, y - 4 + q * 26, l, 20, True, ACC)
        fab, mat, sim = COST_TEXT[k]
        for j, (h_, v) in enumerate((('Fabric', fab), ('Material', mat), ('Sim', sim))):
            words, line, lines = v.split(), '', []
            for w_ in words:
                if len(line) + len(w_) > 22:
                    lines.append(line); line = ''
                line += w_ + ' '
            lines.append(line)
            pg.text(x + 330, y + 62 + j * 110, h_, 18, True, DIM)
            for q, l in enumerate(lines[:4]):
                pg.text(x + 330, y + 86 + j * 110 + q * 22, l, 17)
    return pg


def p_palette():
    pg = Page('palette', 'Colour palette (exact values used by the 3D materials)', 1100)
    items = [(k, v) for k, v in PAL.items()]
    cols = 4
    for i, (k, v) in enumerate(items):
        x = 50 + (i % cols) * 585
        y = 130 + (i // cols) * 150
        r, g, b = hex_rgb(v)
        pg.d.rounded_rectangle((x, y, x + 120, y + 120), 12, fill=(r, g, b))
        pg.text(x + 140, y + 10, k.replace('_', ' ').upper(), 24, True)
        pg.text(x + 140, y + 48, f'HEX  {v.upper()}', 22, mono=True)
        pg.text(x + 140, y + 80, f'RGB  {r:3d}, {g:3d}, {b:3d}', 22, mono=True, color=DIM)
    return pg


def power_img(n, after=None):
    im = raw(n).convert('RGB')
    if after:
        base = np.asarray(im).astype(np.float32)
        for f, alpha in after:
            ai = raw(f)
            arr = np.asarray(ai).astype(np.float32)
            a = arr[..., 3:4] / 255 * alpha
            tint = arr[..., :3] * np.array([0.35, 0.75, 1.3]) + np.array([10, 60, 120])
            base = base * (1 - a) + np.clip(tint, 0, 255) * a
        im = Image.fromarray(base.astype(np.uint8))
    return bloom(im)


def p_powers():
    pg = Page('powers', 'Power activation design + VFX reference', 2140)
    stages = ['normal', 'activation', 'full', 'deactivation']
    rows = [('SUPER SPEED', 'speed', 'Trails + afterimages + footstep sparks', 'hand_speed.png'),
            ('LIGHTNING', 'lightning', 'Arcs along arms, palm discharge, body aura', 'hand_lightning.png'),
            ('MAGICAL PORTAL', 'portal', 'Swirl disc, white-hot rim, spark ring, hand rune', 'hand_portal.png')]
    for r, (title, key, desc, hand) in enumerate(rows):
        y = 130 + r * 600
        pg.text(50, y, title, 34, True, ACC)
        pg.text(50, y + 46, desc, 21, color=DIM)
        x = 50
        for s in stages:
            if s == 'normal':
                im = power_img('power_normal.png')
            elif key == 'speed' and s == 'full':
                im = power_img('power_speed_full.png', [('power_speed_afterimage_0.png', 0.45),
                                                       ('power_speed_afterimage_1.png', 0.22)])
            else:
                im = power_img(f'power_{key}_{s}.png')
            im = fit(im, h=470)
            pg.paste(im, x, y + 90)
            pg.text(x + 10, y + 100, s.upper(), 20, True)
            x += im.width + 30
        hi = fit(power_img(hand), w=470)
        pg.paste(hi, x + 10, y + 90)
        pg.text(x + 20, y + 100, 'HAND FX', 20, True)
    y = 130 + 3 * 600
    pg.text(50, y + 10, 'EYE TRANSFORMATION', 28, True, ACC)
    pg.text(50, y + 50, '(all powers)', 21, color=DIM)
    x = 420
    for s in ('normal', 'activation', 'full'):
        im = fit(power_img(f'eyes_{s}.png'), h=170)
        pg.paste(im, x, y + 10)
        pg.text(x + 10, y + 20, s.upper(), 18, True)
        x += im.width + 30
    return pg


if __name__ == '__main__':
    for i, fn in enumerate([p_turn, p_poses, p_face, p_expr, p_costume, p_palette, p_powers], 1):
        fn().save(i)
