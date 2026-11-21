"""TASK 06 · compose the vegetation reference sheets from the renders (python3 + Pillow).

    python3 t6_compose_sheets.py AV EF MK

Out (03_assets/vegetation/sheets/):
  <REGION>/TREE_<asset>.png     per tree / shrub: front · side · back with height ruler + 1.75 m figure, leaf close-up,
                                trunk-foot close-up, bark texture (scan) + leaf atlas tile + normal map, palette, specification
  <REGION>/PLANTS_<REGION>.png  plant & flower library: hero + detail per plant (10 cm grid ground), specs, palette
  <REGION>/REGION_<REGION>.png  regional vegetation sheet: tree height lineup (ruler), plant lineup, identity, palette
"""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); VEG = os.path.abspath(os.path.join(HERE, '..'))
PH = os.path.abspath(os.path.join(VEG, '..', 'external', 'polyhaven'))
FD = '/usr/share/fonts/truetype/dejavu/'
F = lambda n, b=False, i=False: ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf', n + 2) if i else ImageFont.truetype(FD + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), n)
BG, INK, SUB, LINE = (236, 234, 228), (28, 34, 30), (92, 98, 94), (170, 172, 166)
HEAD = (30, 44, 38)
BADGE = {'SPECIES-INSPIRED': ((46, 110, 64), 'SPECIES-INSPIRED (real plant reference)'),
         'PROPOSED FANTASY': ((196, 110, 24), 'PROPOSED FANTASY — needs Director approval')}
NAMES = {'AV': 'ASHRAM_VALLEY', 'EF': 'ENCHANTED_FOREST', 'MK': 'MOUNTAIN_KINGDOM'}
TITLE = {'AV': 'R-01 ASHRAM VALLEY', 'EF': 'R-02 ENCHANTED FOREST', 'MK': 'R-03 MOUNTAIN KINGDOM (Great Northern Range)'}
IDENT = {
    'AV': ['Warm-temperate Himalayan-foothill valley (~700–900 m): open meadows, groves and a forest ring (approved valley layout).',
           'Trees: ancient Peepal as a lone landmark, Banj-oak groves on moist slopes + stream banks, Rhododendron at forest edges,',
           'Chir pine on dry sunny slopes, Deodar ring on the cooler upper slopes, Bamboo clumps in moist hollows.',
           'Ground: meadow grass + wildflowers, tall kans grass on river bars, lotus + reed-mace only in still water (pond / slow river).',
           'Cultivated (PROPOSED): tulsi + marigold only inside the Ashram courtyard / gardens. Mood: green, gentle, golden light.'],
    'EF': ['Deep old-growth forest (~660 m), teal-green colour key (World Bible): three canopy layers — emergent Giant Elders (60 m+),',
           'main canopy Teal Beech + Ancient Moss Oak (25–35 m), understorey Yew + giant ferns; moss carpets, hanging lianas + beard moss,',
           'dead snags and fallen giants. Fantasy proposals (orange labels): Veil Willow, Spiral-root Tree, Lantern Tree, Glowcap fungi —',
           'all OPTIONAL, used sparingly (≤ 5 % of trees) so the forest stays believable. No glow anywhere unless the Director approves.'],
    'MK': ['Altitude zones on the Great Northern Range (true-scale terrain; TASK 05 scatter tree line = 3 550 m — kept):',
           'M1 montane forest 1 500–3 000 m — Himalayan spruce (dense, dark, conical; Deodar on the lower flanks)',
           'M2 tree line 3 000–3 550 m — Himalayan birch (white bark, twisted) + wind-bent pine (krummholz) on exposed ridges',
           'M3 alpine 3 550–4 500 m — juniper mats, dwarf rhododendron, tussock grass, gentian, edelweiss, blue poppy, cushion plants',
           'M4 nival > 4 500 m — bare rock, lichen, snow only. No fantasy species proposed for the mountains (realistic, harsh, sparse).'],
}


def font_fit(d, text, maxw, size, b=False):
    while size > 10 and d.textlength(text, font=F(size, b)) > maxw:
        size -= 1
    return F(size, b)


def nice_step(h):
    for s in (.05, .1, .2, .25, .5, 1, 2, 5, 10, 20):
        if h / s <= 8:
            return s
    return 20


def alpha_over(im, bg=(214, 220, 224)):
    """renders are transparent (shadow catcher) → put them on a soft vertical gradient backdrop."""
    im = im.convert('RGBA'); w, h = im.size
    g = np.linspace(0, 1, h)[:, None, None]
    top, bot = np.array([196, 210, 222]), np.array([232, 230, 222])
    grad = (top * (1 - g) + bot * g).repeat(w, 1).astype(np.uint8)
    base = Image.fromarray(np.dstack([grad, np.full((h, w), 255, np.uint8)]), 'RGBA'); base.alpha_composite(im)
    return base.convert('RGB')


def ruler(d, x, img_box, view, H, scale):
    """vertical height ruler for an orthographic view. img_box = (x0, y0) where the view image was pasted, scale = paste scale."""
    x0, y0 = img_box; ppm = view['ry'] / view['ortho_scale'] * scale
    zpx = lambda z: y0 + (view['ry'] / 2 + (view['zc'] - z) * view['ry'] / view['ortho_scale']) * scale
    st = nice_step(H); z = 0.0
    d.line([(x, zpx(0)), (x, zpx(H))], fill=INK, width=2)
    while z <= H + 1e-6:
        y = zpx(z); d.line([(x - 8, y), (x + 8, y)], fill=INK, width=2)
        lab = f'{z:g} m'; d.text((x - 12 - d.textlength(lab, font=F(18)), y - 11), lab, fill=INK, font=F(18)); z += st
    yH = zpx(H); d.line([(x - 14, yH), (x + 40, yH)], fill=(170, 40, 30), width=2)
    d.text((x + 44, yH - 12), f'H = {H:.1f} m', fill=(170, 40, 30), font=F(20, True))


def palette(d, x, y, cols, sw=64):
    for i, c in enumerate(cols):
        h = c.lstrip('#'); rgb = tuple(int(h[k:k + 2], 16) for k in (0, 2, 4))
        d.rectangle([x + i * (sw + 10), y, x + i * (sw + 10) + sw, y + sw], fill=rgb, outline=LINE)
        d.text((x + i * (sw + 10), y + sw + 4), c.upper(), fill=SUB, font=F(13))


def badge(d, x, y, label):
    col, txt = BADGE.get(label, ((90, 90, 90), label))
    w = d.textlength(txt, font=F(22, True)) + 30
    d.rounded_rectangle([x, y, x + w, y + 40], 8, fill=col); d.text((x + 15, y + 8), txt, fill=(255, 255, 255), font=F(22, True))
    return w


def header(d, W, title, sub, label, right):
    d.rectangle([0, 0, W, 150], fill=HEAD)
    d.text((40, 22), title, fill=(240, 240, 232), font=F(46, True))
    d.text((40, 86), sub, fill=(196, 206, 198), font=F(26, i=True))
    if label:
        bw = d.textlength(BADGE.get(label, ((0, 0, 0), label))[1], font=F(22, True)) + 30
        badge(d, W - 40 - bw, 24, label)
    d.text((W - 40 - d.textlength(right, font=F(20)), 100), right, fill=(196, 206, 198), font=F(20))


def tex_swatch(path, size, tint=None):
    im = Image.open(path).convert('RGB').resize(size, Image.LANCZOS)
    if tint:
        h = tint.lstrip('#'); t = np.array([int(h[k:k + 2], 16) for k in (0, 2, 4)]) / 255
        im = Image.fromarray(np.clip(np.asarray(im, np.float32) * t, 0, 255).astype(np.uint8))
    return im


def atlas_tile(atlas, size, which='col'):
    p = os.path.join(VEG, 'textures', 'leaves', f'{atlas}_{which}.png'); im = Image.open(p)
    w, h = im.size; tile = im.crop((0, 0, w // 2, h // 2))
    if which == 'col':
        bg = Image.new('RGBA', tile.size, (226, 228, 222, 255)); bg.alpha_composite(tile.convert('RGBA')); tile = bg
    return tile.convert('RGB').resize(size, Image.LANCZOS)


def tree_sheet(reg, name, v, V, outd):
    W, Hh = 3300, 1900
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    st = v['stats']; H = st['height_m']
    header(d, W, f"{name}  ·  {v['common']}", v['latin'], v['label'], f"{TITLE[reg]}  ·  {v['category']}  ·  TASK 06 milestone 1 concept (v001)")
    rd = os.path.join(VEG, 'renders', reg)
    sc = 1060 / 840; x = 150; y0 = 190
    for i, view in enumerate(('front', 'side', 'back')):
        p = os.path.join(rd, f'{name}_{view}.png')
        if not os.path.exists(p):
            continue
        img = alpha_over(Image.open(p)).resize((int(600 * sc), 1060), Image.LANCZOS)
        im.paste(img, (x, y0)); d.rectangle([x, y0, x + img.width, y0 + 1060], outline=LINE)
        d.text((x + 12, y0 + 10), view.upper() + (' (with 1.75 m figure)' if view == 'front' else ''), fill=INK, font=F(22, True))
        if view in V.get(name, {}):
            ruler(d, x - 18 if i == 0 else x + 36, (x, y0), V[name][view], H, sc)
        x += img.width + (70 if i == 0 else 22)
    # right column
    X = x + 20; cw = W - X - 40; hw = (cw - 20) // 2
    d.text((X, 190), 'LEAF / FOLIAGE CLOSE-UP', fill=INK, font=F(20, True)); d.text((X + hw + 20, 190), 'TRUNK FOOT · ROOTS ON GROUND', fill=INK, font=F(20, True))
    for j, kind in enumerate(('leaf', 'base')):
        p = os.path.join(rd, f'{name}_{kind}.png')
        if os.path.exists(p):
            img = alpha_over(Image.open(p)).resize((hw, hw), Image.LANCZOS); im.paste(img, (X + j * (hw + 20), 220))
    yy = 220 + hw + 30
    sw = (cw - 40) // 3
    bark = v.get('bark'); B = v.get('bark_tint', '#FFFFFF')
    d.text((X, yy), 'BARK (scan + tint)', fill=INK, font=F(18, True))
    d.text((X + sw + 20, yy), 'LEAF ATLAS', fill=INK, font=F(18, True))
    d.text((X + 2 * (sw + 20), yy), 'LEAF NORMAL', fill=INK, font=F(18, True))
    yy += 28
    if bark and bark != 'culm':
        bp = os.path.join(PH, 'textures', bark, f'{bark}_diff_2k.jpg')
        if os.path.exists(bp):
            im.paste(tex_swatch(bp, (sw, sw), B), (X, yy))
            d.text((X, yy + sw + 4), f'Poly Haven: {bark}', fill=SUB, font=font_fit(d, f'Poly Haven: {bark}', sw, 14))
    elif bark == 'culm':
        d.rectangle([X, yy, X + sw, yy + sw], fill=(110, 140, 58)); d.text((X + 10, yy + 10), 'procedural culm\n(waxy green, nodes)', fill=(255, 255, 255), font=F(16))
    if v.get('atlas'):
        im.paste(atlas_tile(v['atlas'], (sw, sw)), (X + sw + 20, yy)); im.paste(atlas_tile(v['atlas'], (sw, sw), 'nor'), (X + 2 * (sw + 20), yy))
        d.text((X + sw + 20, yy + sw + 4), f"{v['atlas']} · 4 var · 2K", fill=SUB, font=font_fit(d, f"{v['atlas']} · 4 var · 2K", sw, 14))
    yy += sw + 36
    d.text((X, yy), 'COLOUR PALETTE', fill=INK, font=F(18, True)); palette(d, X, yy + 28, v['palette'][:7], 66); yy += 130
    d.text((X, yy), 'SPECIFICATION', fill=INK, font=F(18, True)); yy += 30
    rows = [('Height', f"{H:.1f} m  (design {v.get('design_h', H):.1f} m, variants ±7 %)"),
            ('Canopy (X × Y)', f"{st['canopy_x_m']:.1f} × {st['canopy_y_m']:.1f} m"),
            ('Trunk Ø at foot', f"{st['trunk_d_m']:.2f} m" + (' (clump Ø)' if 'BAMBOO' in name or v['kind'] == 'shrub' else '')),
            ('Habitat', v['habitat']), ('Altitude', v['altitude']),
            ('Geometry', f"{st['tris']:,} tris · {st['branches']:,} branches · {st['leaf_cards']:,} leaf cards"),
            ('Ground contact', f"roots / foot sink to {st['lowest_z']:.2f} m (no floating)"),
            ('Rig / wind', 'wind attributes + NG_T6_WIND (T6_WIND_CONTROL)'), ('File', f"library/T6_VEG_{NAMES[reg]}_v001.blend → T6_{name}")]
    for k_, val in rows:
        d.text((X, yy), k_, fill=SUB, font=F(17, True))
        words = val.split(); line = ''
        for wd in words:
            if d.textlength((line + ' ' + wd).strip(), font=F(17)) > cw - 200 and line:
                d.text((X + 200, yy), line.strip(), fill=INK, font=F(17)); yy += 24; line = ''
            line += ' ' + wd
        d.text((X + 200, yy), line.strip(), fill=INK, font=F(17)); yy += 28
    im = im.crop((0, 0, W, max(y0 + 1060, yy) + 40)); Hh = im.height
    im.save(os.path.join(outd, f'TREE_{name}.png'), optimize=True)
    im.resize((W // 3, Hh // 3), Image.LANCZOS).save(os.path.join(outd, 'thumbs', f'TREE_{name}.jpg'), quality=88)


def plant_sheet(reg, inv, V, outd):
    names = [n for n, v in inv.items() if v['kind'] == 'plant']
    if not names:
        return
    cols = 2; cwid = 1600; ch = 560; W = cols * cwid + 60; Hh = 170 + ((len(names) + 1) // 2) * (ch + 20) + 40
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    header(d, W, f'PLANT & FLOWER LIBRARY  ·  {TITLE[reg]}', 'grass · wildflowers · ferns · moss · fungi · aquatic · vines · alpine — real geometry, ground grid = 10 cm',
           None, 'TASK 06 milestone 1 concept (v001)')
    rd = os.path.join(VEG, 'renders', reg)
    for i, n in enumerate(names):
        v = inv[n]; cx = 30 + (i % 2) * cwid; cy = 180 + (i // 2) * (ch + 20)
        d.rectangle([cx, cy, cx + cwid - 20, cy + ch], fill=(246, 245, 240), outline=LINE)
        for j, kind in enumerate(('hero', 'detail')):
            p = os.path.join(rd, f'{n}_{kind}.png')
            if os.path.exists(p):
                im.paste(alpha_over(Image.open(p)).resize((ch - 20, ch - 20), Image.LANCZOS), (cx + 10 + j * (ch - 10), cy + 10))
        tx = cx + 2 * (ch - 10) + 20; tw = cwid - 20 - (tx - cx) - 14
        d.text((tx, cy + 14), n, fill=INK, font=font_fit(d, n, tw, 24, True))
        d.text((tx, cy + 48), v['common'], fill=INK, font=font_fit(d, v['common'], tw, 20))
        d.text((tx, cy + 76), v['latin'], fill=SUB, font=font_fit(d, v['latin'], tw, 17))
        col = BADGE.get(v['label'], ((90, 90, 90), ''))[0]
        d.rounded_rectangle([tx, cy + 106, tx + tw, cy + 138], 6, fill=col)
        d.text((tx + 10, cy + 112), v['label'], fill=(255, 255, 255), font=F(17, True))
        st = v['stats']; yy = cy + 152
        for k_, val in (('Category', v['category']), ('Height', f"{st['height_m'] * 100:.0f} cm"), ('Spread', f"{st['spread_x_m'] * 100:.0f} × {st['spread_y_m'] * 100:.0f} cm"),
                        ('Region', v['region']), ('Geometry', f"{st['tris']:,} tris")):
            d.text((tx, yy), k_, fill=SUB, font=F(15, True)); d.text((tx + 95, yy), val, fill=INK, font=font_fit(d, val, tw - 95, 15)); yy += 24
        hb = v.get('habitat') or ''
        words = hb.split(); line = ''; yy += 4
        for wd in words:
            if d.textlength(line + ' ' + wd, font=F(14)) > tw:
                d.text((tx, yy), line.strip(), fill=SUB, font=F(14)); yy += 19; line = ''
            line += ' ' + wd
        if line:
            d.text((tx, yy), line.strip(), fill=SUB, font=F(14)); yy += 19
        palette(d, tx, cy + ch - 92, v['palette'][:5], 44)
    im.save(os.path.join(outd, f'PLANTS_{reg}.png'), optimize=True)
    im.resize((W // 3, Hh // 3), Image.LANCZOS).save(os.path.join(outd, 'thumbs', f'PLANTS_{reg}.jpg'), quality=88)


def region_sheet(reg, inv, V, outd):
    W, Hh = 3300, 3200
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    header(d, W, f'REGIONAL VEGETATION SHEET  ·  {TITLE[reg]}', 'vegetation identity · height comparison · plant palette (map rev 01 = PROPOSAL; layout preserved)',
           None, 'TASK 06 milestone 1 concept (v001)')
    rd = os.path.join(VEG, 'renders', reg); y = 180
    for ln in IDENT[reg]:
        d.text((40, y), ln, fill=INK, font=F(22)); y += 32
    y += 10
    p = os.path.join(rd, 'LINEUP_TREES.png')
    if os.path.exists(p):
        L = V.get('LINEUP_TREES'); img = alpha_over(Image.open(p)); s = (W - 200) / img.width
        img = img.resize((W - 200, int(img.height * s)), Image.LANCZOS); im.paste(img, (150, y)); d.rectangle([150, y, 150 + img.width, y + img.height], outline=LINE)
        d.text((165, y + 10), 'TREES + SHRUBS — HEIGHT COMPARISON (orthographic, 1.75 m figure at right)', fill=INK, font=F(22, True))
        if L:
            Hm = max(v['stats']['height_m'] for v in inv.values() if v['kind'] != 'plant')
            ppm = L['rx'] / L['ortho_scale'] * s
            zpx = lambda z: y + (L['ry'] / 2 + (L['zc'] - z) * L['rx'] / L['ortho_scale']) * s
            st = nice_step(Hm); z = 0; xr = 130
            d.line([(xr, zpx(0)), (xr, zpx(Hm))], fill=INK, width=2)
            while z <= Hm + 1e-6:
                yy = zpx(z); d.line([(xr - 8, yy), (xr + 8, yy)], fill=INK, width=2)
                d.text((xr - 14 - d.textlength(f'{z:g} m', font=F(18)), yy - 11), f'{z:g} m', fill=INK, font=F(18)); z += st
            if 'cx' in L:
                for k, it in enumerate(L['items']):
                    xx = 150 + (L['rx'] / 2 + (it['x'] - L['cx']) * L['rx'] / L['ortho_scale']) * s
                    lab = it['name'].split('_', 2)[-1].replace('_', ' ').title()
                    hh = inv[it['name']]['stats']['height_m']; lab2 = f'{hh:.1f} m'
                    yl = zpx(0) + 14 + (k % 2) * 26
                    d.text((xx - d.textlength(lab, font=F(17, True)) / 2, yl), lab, fill=INK, font=F(17, True))
                    d.text((xx - d.textlength(lab2, font=F(15)) / 2, zpx(hh) - 22), lab2, fill=(170, 40, 30), font=F(15, True))
        y += img.height + 30
    p = os.path.join(rd, 'LINEUP_PLANTS.png')
    if os.path.exists(p):
        img = alpha_over(Image.open(p)); s = min((W - 200) / img.width, 700 / img.height)
        img = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS); im.paste(img, (150, y)); d.rectangle([150, y, 150 + img.width, y + img.height], outline=LINE)
        d.text((165, y + 10), 'GROUND LAYER — grasses · flowers · ferns · moss · fungi · aquatic (perspective, 10 cm grid)', fill=INK, font=F(22, True))
        y += img.height + 30
    # species list with labels
    d.text((40, y), 'SPECIES IN THIS REGION (milestone 1)', fill=INK, font=F(24, True)); y += 40
    names = list(inv); colw = (W - 80) // 3
    for i, n in enumerate(names):
        v = inv[n]; cx = 40 + (i % 3) * colw; cy = y + (i // 3) * 30
        col = BADGE.get(v['label'], ((90, 90, 90), ''))[0]
        d.ellipse([cx, cy + 6, cx + 14, cy + 20], fill=col)
        t = f"{n} — {v['common']}"
        d.text((cx + 22, cy), t, fill=INK, font=font_fit(d, t, colw - 30, 18))
    im = im.crop((0, 0, W, min(Hh, y + ((len(names) + 2) // 3) * 30 + 40)))
    im.save(os.path.join(outd, f'REGION_{reg}.png'), optimize=True)
    im.resize((im.width // 3, im.height // 3), Image.LANCZOS).save(os.path.join(outd, 'thumbs', f'REGION_{reg}.jpg'), quality=88)


if __name__ == '__main__':
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location('sp', os.path.join(HERE, 't6_species.py')); SP = importlib.util.module_from_spec(spec); spec.loader.exec_module(SP)
    TINT = {t['name']: t['bark'].get('tint', '#FFFFFF') for t in SP.TREES + SP.SHRUBS}
    DESIGN = {t['name']: t['height'] for t in SP.TREES + SP.SHRUBS}
    for reg in (sys.argv[1:] or ['AV', 'EF', 'MK']):
        inv = json.load(open(os.path.join(VEG, 'library', f'T6_VEG_{NAMES[reg]}_inventory.json')))
        vj = os.path.join(VEG, 'renders', reg, 'views.json'); V = json.load(open(vj)) if os.path.exists(vj) else {}
        outd = os.path.join(VEG, 'sheets', reg); os.makedirs(os.path.join(outd, 'thumbs'), exist_ok=True)
        for n, v in inv.items():
            if v['kind'] in ('tree', 'shrub'):
                v['bark_tint'] = TINT.get(n, '#FFFFFF'); v['design_h'] = DESIGN.get(n, v['stats']['height_m'])
                tree_sheet(reg, n, v, V, outd); print('SHEET', n, flush=True)
        plant_sheet(reg, inv, V, outd); region_sheet(reg, inv, V, outd)
        print('REGION SHEETS', reg)
    print('T6_COMPOSE_DONE')
