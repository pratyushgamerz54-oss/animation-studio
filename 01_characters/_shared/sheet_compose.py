"""Compose a character's design-sheet pages from raw renders (config-driven, PIL).

Run:  python3 01_characters/_shared/sheet_compose.py <folder>
Out:  01_characters/<folder>/design/<ID>_sheet_NN_<page>.png
"""
import os, sys, json, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_char import load_cfg

FOLDER = sys.argv[1]
CFG, DIR = load_cfg(FOLDER)
PAL, CID = CFG['pal'], CFG['id']
RAW = os.path.join(DIR, 'design', 'raw')
OUT = os.path.join(DIR, 'design')
MEAS = json.load(open(os.path.join(DIR, 'qc', 'measurements.json')))
ACC = tuple(int(CFG.get('ui_accent', PAL.get('accent', '#2EA8FF')).lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
BG, PANEL, INK, DIM, WARN = (22, 25, 31), (34, 38, 46), (235, 238, 243), (150, 158, 170), (255, 196, 64)
FB, FR, FM = ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
              '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
F = lambda p, s: ImageFont.truetype(p, s)
W = 2400


def raw(n):
    return Image.open(os.path.join(RAW, n)).convert('RGBA')


def has(n):
    return os.path.exists(os.path.join(RAW, n))


def fit(im, w=None, h=None):
    s = min(w / im.width, h / im.height) if (w and h) else (w / im.width if w else h / im.height)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)


def bloom(im, thresh=.62, k1=.7, k2=.55):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    lum = a.max(axis=2, keepdims=True)
    br = Image.fromarray(((np.clip(lum - thresh, 0, 1) / (1 - thresh)) * a * 255).astype(np.uint8))
    b1 = np.asarray(br.filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
    b2 = np.asarray(br.filter(ImageFilter.GaussianBlur(28))).astype(np.float32) / 255
    return Image.fromarray((np.clip(a + k1 * b1 + k2 * b2, 0, 1) * 255).astype(np.uint8)).convert('RGBA')


def noise(w, h, seed=3, scale=24):
    rng = np.random.default_rng(seed)
    n = np.zeros((h, w), np.float32)
    for oc, amp in ((scale, 1.0), (scale // 2, .5), (scale // 4, .25)):
        small = Image.fromarray((rng.random((max(2, h // oc), max(2, w // oc))) * 255).astype(np.uint8))
        n += np.asarray(small.resize((w, h), Image.BICUBIC)).astype(np.float32) / 255 * amp
    n -= n.min(); n /= n.max()
    return n


def dissolve(a_img, b_img, level, edge_hex, seed=3):
    """Show a_img where noise > level, b_img elsewhere, with a glowing edge band."""
    A = np.asarray(a_img.convert('RGB')).astype(np.float32)
    B = np.asarray(b_img.convert('RGB')).astype(np.float32)
    h, w = A.shape[:2]
    n = noise(w, h, seed)[..., None]
    m = np.clip((n - level) / .04, 0, 1)
    band = np.clip(1 - abs(n - level) / .03, 0, 1) * (np.abs(A - B).sum(axis=2, keepdims=True) > 30)
    e = np.array([int(edge_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)], np.float32)
    o = B * (1 - m) + A * m + band * e * 1.2
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).convert('RGBA')


def alpha_dissolve(char_rgba, bg, level, edge_hex, seed=5):
    C = np.asarray(char_rgba).astype(np.float32)
    Bg = np.asarray(bg.convert('RGB')).astype(np.float32)
    h, w = C.shape[:2]
    n = noise(w, h, seed, 12)[..., None]
    a = C[..., 3:4] / 255
    keep = np.clip((n - level) / .05, 0, 1) * a
    band = np.clip(1 - abs(n - level) / .04, 0, 1) * a
    e = np.array([int(edge_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)], np.float32)
    o = Bg * (1 - keep) + C[..., :3] * keep + band * e * 1.4
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).convert('RGBA')


class Page:
    def __init__(self, key, title, h):
        self.key, self.im = key, Image.new('RGBA', (W, h), BG)
        d = self.d = ImageDraw.Draw(self.im)
        d.rectangle((0, 0, W, 96), fill=(14, 16, 21)); d.rectangle((0, 92, W, 96), fill=ACC)
        nm = CFG['name'].upper()
        d.text((40, 20), nm, font=F(FB, 44), fill=INK)
        x = 40 + d.textlength(nm, font=F(FB, 44)) + 30
        d.text((x, 34), f"{CFG['role']}  ·  Design Sheet v1  ·  {title}", font=F(FR, 26), fill=DIM)
        d.text((W - 40, 34), 'PROPOSAL — awaiting Director approval', font=F(FB, 24), fill=WARN, anchor='ra')
        pw = ' · '.join(CFG['powers']) if CFG['powers'] else 'NOT CONFIRMED'
        d.text((40, h - 40), f'Powers (confirmed): {pw}   |  Appearance & costume = proposals   |  3D renders of '
               f'the real Blender model {FOLDER}_v002.blend', font=F(FR, 20), fill=DIM)

    def paste(self, im, x, y, label=None):
        self.d.rounded_rectangle((x - 8, y - 8, x + im.width + 8, y + im.height + 8), 14, fill=PANEL)
        self.im.alpha_composite(im, (int(x), int(y)))
        if label:
            self.d.text((x + im.width / 2, y + im.height + 18), label, font=F(FB, 24), fill=INK, anchor='ma')

    def text(self, x, y, s, size=22, bold=False, color=INK, mono=False):
        self.d.text((x, y), s, font=F(FM if mono else (FB if bold else FR), size), fill=color)

    def wrap(self, x, y, s, width_chars, size=20, color=INK, lh=26, maxl=99):
        line, n = '', 0
        for w_ in s.split():
            if len(line) + len(w_) > width_chars:
                self.text(x, y + n * lh, line, size, color=color); n += 1; line = ''
                if n >= maxl:
                    return n
            line += w_ + ' '
        self.text(x, y + n * lh, line, size, color=color)
        return n + 1

    def save(self, n):
        p = os.path.join(OUT, f'{CID}_sheet_{n:02d}_{self.key}.png')
        self.im.convert('RGB').save(p, optimize=True)
        print('wrote', p)


def hex_rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def p_turn():
    pg = Page('turnaround', 'Full-body turnaround (neutral pose, orthographic)', 1020)
    x = 50
    for k, lab in (('front', 'Front'), ('three_quarter_front', '3/4 Front'), ('right', 'Right side'),
                   ('three_quarter_back', '3/4 Back'), ('back', 'Back'), ('left', 'Left side')):
        im = fit(raw(f'turn_{k}.png'), h=780)
        pg.paste(im, x + (370 - im.width) / 2, 130, lab); x += 385
    return pg


def p_poses():
    pg = Page('poses_measurements', 'T-pose · A-pose · Neutral + measurement guide', 1000)
    H = 660
    t = fit(raw('pose_T.png'), h=H); pg.paste(t, 50, 130, 'T-pose (modelling & rigging)')
    a = fit(raw('pose_A.png'), h=H); pg.paste(a, 50 + t.width + 40, 130, 'A-pose (deformation checks)')
    n0 = raw('pose_NEUTRAL.png'); sc = H / n0.height; n = fit(n0, h=H)
    nx, ny = 50 + t.width + a.width + 80, 130
    pg.paste(n, nx, ny, 'Neutral + head units')
    # camera: ortho scale = max(2.0, 1.1*top) centred at top/2 over 1120 px
    top = MEAS['height_total_m']
    osz = max(2.0, top * 1.1); ppm = 1120 / osz
    zpx = lambda z: ny + (560 - (z - top / 2) * ppm) * sc
    hh = MEAS['head_height_m']
    for i in range(10):
        z = i * hh
        if z > top + .01:
            break
        y = zpx(z)
        pg.d.line((nx - 6, y, nx + n.width + 6, y), fill=(90, 170, 255) if i % 2 == 0 else (70, 110, 160), width=2)
        pg.d.text((nx + n.width + 14, y - 12), f'{i}', font=F(FB, 20), fill=ACC)
    yt, yb = zpx(MEAS['head_top_z']), zpx(0)
    pg.d.line((nx - 30, yt, nx - 30, yb), fill=WARN, width=3)
    pg.d.text((nx - 40, (yt + yb) / 2), f"{MEAS['height_no_hair_m'] * 100:.1f} cm", font=F(FB, 22), fill=WARN, anchor='rm')
    tx = nx + n.width + 80
    pg.text(tx, 140, 'BODY PROPORTIONS (measured on model)', 26, True, ACC)
    rows = [('Height (body+head)', f"{MEAS['height_no_hair_m'] * 100:.1f} cm"),
            ('Height (incl. hair/horns)', f"{MEAS['height_total_m'] * 100:.1f} cm"),
            ('Head height', f"{MEAS['head_height_m'] * 100:.1f} cm"), ('Head-to-body', f"{MEAS['heads_tall']} heads"),
            ('Shoulder width', f"{MEAS['shoulder_width_m'] * 100:.1f} cm"), ('Chest width', f"{MEAS['chest_width_m'] * 100:.1f} cm"),
            ('Hip width', f"{MEAS['hip_width_m'] * 100:.1f} cm"), ('Arm length', f"{MEAS['arm_length_m'] * 100:.1f} cm"),
            ('Leg (hip→floor)', f"{MEAS['leg_length_m'] * 100:.1f} cm"), ('Hand length', f"{MEAS['hand_length_m'] * 100:.1f} cm"),
            ('Foot length', f"{MEAS['foot_length_m'] * 100:.1f} cm")]
    for i, (k, v) in enumerate(rows):
        pg.text(tx, 195 + i * 36, f'{k:26}{v:>12}', 20, mono=True)
    y = 195 + len(rows) * 36 + 30
    pg.text(tx, y, 'BUILD', 24, True, ACC); n_ = pg.wrap(tx, y + 36, CFG['body_type'], 44)
    y += 50 + n_ * 26
    pg.text(tx, y, 'SILHOUETTE', 24, True, ACC); pg.wrap(tx, y + 36, CFG['silhouette'], 44)
    return pg


def p_face():
    pg = Page('face', 'Face design · hair · eye', 1260)
    x = 50
    for k, lab in (('front', 'Face — front'), ('three_quarter', 'Face — 3/4'), ('side', 'Face — side'),
                   ('back_three_quarter', 'Back 3/4 (hair / headwear)')):
        im = fit(raw(f'face_{k}.png'), h=600); pg.paste(im, x, 130, lab); x += im.width + 40
    e = fit(raw('face_eye_detail.png'), h=300); pg.paste(e, 50, 830, 'Eye detail (left eye)')
    tx = 50 + e.width + 80
    for i, (k, v) in enumerate(CFG.get('face_notes', [])):
        pg.text(tx, 840 + i * 44, f'{k:13}', 22, True, ACC); pg.wrap(tx + 200, 840 + i * 44, v, 100, 20, maxl=1)
    return pg


def p_expr():
    pg = Page('expressions', 'Facial expressions (lids, brows, mouth shape keys)', 1140)
    fs = sorted(glob.glob(os.path.join(RAW, 'expr_*.png')))
    for i, f in enumerate(fs):
        im = fit(Image.open(f).convert('RGBA'), h=400)
        x = 50 + (i % 6) * (im.width + 40); y = 130 + (i // 6) * 490
        lab = os.path.basename(f)[8:-4].replace('_', ' ').title()
        pg.paste(im, x, y, f'{i + 1}. {lab}' if lab != 'Blink' else 'Extra: Blink')
    return pg


def p_costume():
    grp = CFG['costume_groups']
    rows = (len(grp) + 3) // 4
    pg = Page('costume', 'Costume & accessories breakdown', 180 + rows * 540)
    for i, (k, lab, _, fab, mat, sim) in enumerate(grp):
        im = fit(raw(f'costume_{k}.png'), h=300)
        x = 50 + (i % 4) * 590; y = 130 + (i // 4) * 540
        pg.paste(im, x, y)
        n = pg.wrap(x + 330, y - 4, lab, 19, 20, ACC, 26, 2)
        for j, (h_, v) in enumerate((('Fabric', fab), ('Material', mat), ('Sim', sim))):
            pg.text(x + 330, y + 62 + j * 110, h_, 18, True, DIM)
            pg.wrap(x + 330, y + 86 + j * 110, v, 22, 17, INK, 22, 4)
    return pg


def p_palette():
    items = list(PAL.items())
    rows = (len(items) + 3) // 4
    pg = Page('palette', 'Colour palette (exact values used by the 3D materials)', 200 + rows * 150)
    for i, (k, v) in enumerate(items):
        x = 50 + (i % 4) * 585; y = 130 + (i // 4) * 150
        r, g, b = hex_rgb(v)
        pg.d.rounded_rectangle((x, y, x + 120, y + 120), 12, fill=(r, g, b), outline=(70, 76, 88), width=2)
        pg.text(x + 140, y + 10, k.replace('_', ' ').upper(), 24, True)
        pg.text(x + 140, y + 48, f'HEX  {v.upper()}', 22, mono=True)
        pg.text(x + 140, y + 80, f'RGB  {r:3d}, {g:3d}, {b:3d}', 22, mono=True, color=DIM)
    return pg


def power_img(n, after=None):
    im = raw(n).convert('RGB')
    if after:
        base = np.asarray(im).astype(np.float32)
        for f, alpha in after:
            arr = np.asarray(raw(f)).astype(np.float32)
            a = arr[..., 3:4] / 255 * alpha
            tint = arr[..., :3] * np.array([.35, .75, 1.3]) + np.array([10, 60, 120])
            base = base * (1 - a) + np.clip(tint, 0, 255) * a
        im = Image.fromarray(base.astype(np.uint8))
    return bloom(im)


TITLES = {'speed': ('SUPER SPEED', 'Long horizontal trails + afterimages + footstep sparks'),
          'lightning': ('LIGHTNING', 'Jagged branching arcs along the arms, palm discharge, body aura'),
          'portal': ('MAGICAL PORTAL', 'Round swirl disc, white-hot rim, spark ring, hand rune'),
          'corrupted_portal': ('MAGICAL PORTAL (corrupted)', 'Reverse swirl, blood-red rim, black core, smoke tongues'),
          'fire': ('FIRE', 'Hand flames → fireball with tail → full-body fire aura; embers on release'),
          'dark_magic': ('DARK MAGIC', 'Violet-black licking wisps, dark orb between the hands, crackle'),
          'invisibility': ('INVISIBILITY', 'Noise dissolve into refractive glass body with faint rim → reappear'),
          'laser': ('LASER', 'Perfectly straight coherent beam: white core, coloured sheath, charge orb, impact burst'),
          'teleport': ('TELEPORTATION', 'Body-hugging light rings + warp bubble; body breaks into motes (no round portal)')}


def stage_img(key, s):
    if s == 'normal':
        return power_img('power_normal.png')
    if key == 'speed' and s == 'full':
        return power_img('power_speed_full.png', [('power_speed_afterimage_0.png', .45), ('power_speed_afterimage_1.png', .22)])
    if key == 'invisibility':
        b, g = raw('power_invisibility_base.png'), raw('power_invisibility_glass.png')
        lvl = {'activation': .35, 'full': 1.1, 'deactivation': .70}[s]
        return bloom(dissolve(b, g, lvl, PAL.get('power_glow', '#9A7BFF')))
    if key == 'teleport' and s != 'activation':
        ch, fx_ = raw(f'power_teleport_{s}_char.png'), raw(f'power_teleport_{s}_fx.png')
        return bloom(alpha_dissolve(ch, fx_, .62 if s == 'full' else .28, PAL.get('teleport', '#B57BFF')))
    return power_img(f'power_{key}_{s}.png')


def hand_img(key):
    if key == 'invisibility':
        return bloom(dissolve(raw('hand_invisibility_base.png'), raw('hand_invisibility_glass.png'), .5,
                              PAL.get('power_glow', '#9A7BFF')))
    return power_img(f'hand_{key}.png')


def p_powers():
    rows = CFG['power_rows']
    pg = Page('powers', 'Power activation design + VFX reference', 330 + len(rows) * 600)
    for r, key in enumerate(rows):
        title, desc = TITLES[key]
        y = 130 + r * 600
        pg.text(50, y, title, 34, True, ACC); pg.text(50, y + 46, desc, 21, color=DIM)
        x = 50
        for s in ('normal', 'activation', 'full', 'deactivation'):
            im = fit(stage_img(key, s), h=470); pg.paste(im, x, y + 90)
            pg.text(x + 10, y + 100, {'deactivation': 'REAPPEAR' if key == 'invisibility' else
                                      ('ARRIVAL' if key == 'teleport' else 'DEACTIVATION'),
                                      'full': 'DEPARTURE' if key == 'teleport' else 'FULL'}.get(s, s.upper()), 20, True)
            x += im.width + 30
        hi = fit(hand_img(key), w=470); pg.paste(hi, x + 10, y + 90); pg.text(x + 20, y + 100, 'HAND FX', 20, True)
    y = 130 + len(rows) * 600
    pg.text(50, y + 10, 'EYE TRANSFORMATION', 28, True, ACC); pg.text(50, y + 50, '(all powers)', 21, color=DIM)
    x = 420
    for s in ('normal', 'activation', 'full'):
        im = fit(power_img(f'eyes_{s}.png'), h=170); pg.paste(im, x, y + 10); pg.text(x + 10, y + 20, s.upper(), 18, True)
        x += im.width + 30
    return pg


def p_extras():
    if not has('cost_A_fracture_veins.png'):
        return None
    pg = Page('borrowed_power_cost', 'Borrowed-power life cost — 3 ALTERNATIVES for approval (U-08)', 1120)
    alts = [('cost_A_fracture_veins.png', 'A · Fracture veins', 'Glowing red cracks spread over the skin with every borrowed power; more cost = more cracks.'),
            ('cost_B_ash_drain.png', 'B · Ash drain', 'Skin greys to ash and eyes dim while the borrowed power runs; colour returns slowly.'),
            ('cost_C_core_siphon.png', 'C · Core siphon', 'Energy is visibly pulled out of his chest core into the power; the core dims and flickers.')]
    x = 50
    for f, t, d in alts:
        im = fit(bloom(raw(f)), h=760); pg.paste(im, x, 130)
        pg.text(x, 920, t, 28, True, ACC); pg.wrap(x, 960, d, 46, 20, DIM)
        x += im.width + 50
    pg.text(x + 20, 140, 'Story rule (confirmed):', 24, True, WARN)
    pg.wrap(x + 20, 180, 'Borrowing a power costs Saithan part of his own life. The exact visual is NOT decided — '
            'choose A, B, C or a mix.', 30, 21)
    return pg


if __name__ == '__main__':
    pages = [p_turn, p_poses, p_face, p_expr, p_costume, p_palette]
    if CFG.get('power_rows'):
        pages.append(p_powers)
    pages.append(p_extras)
    n = 1
    for fn in pages:
        pg = fn()
        if pg is not None:
            pg.save(n); n += 1
