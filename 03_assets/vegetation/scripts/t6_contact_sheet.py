"""TASK 06 · milestone-1 contact sheet: every tree / shrub front view + every plant hero view, grouped by region, with labels."""
import os, json, glob
from PIL import Image, ImageDraw, ImageFont
from t6_compose_sheets import VEG, F, BG, INK, SUB, LINE, HEAD, BADGE, NAMES, TITLE, alpha_over
W = 3300; cell = (300, 420); pcell = (300, 300)
rows = []
for reg in ('AV', 'EF', 'MK'):
    inv = json.load(open(os.path.join(VEG, 'library', f'T6_VEG_{NAMES[reg]}_inventory.json')))
    rows.append((reg, [(n, v) for n, v in inv.items() if v['kind'] != 'plant'], [(n, v) for n, v in inv.items() if v['kind'] == 'plant']))
per = (W - 80) // (cell[0] + 12)
Hh = 170
for reg, t, p in rows:
    Hh += 60 + ((len(t) + per - 1) // per) * (cell[1] + 70) + ((len(p) + per - 1) // per) * (pcell[1] + 70)
im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, 150], fill=HEAD)
d.text((40, 22), 'TASK 06 · MILESTONE 1 — ECOSYSTEM VEGETATION CONCEPTS (real 3D assets, Blender 4.5)', fill=(240, 240, 232), font=F(42, True))
d.text((40, 88), 'green dot = SPECIES-INSPIRED · orange dot = PROPOSED FANTASY (needs approval) · trees: front view (scale differs per tile — see sheets) · plants: hero view, 10 cm grid',
       fill=(196, 206, 198), font=F(22))
y = 170
for reg, trees, plants in rows:
    d.text((40, y), TITLE[reg], fill=INK, font=F(32, True)); y += 52
    for group, cs, view in ((trees, cell, 'front'), (plants, pcell, 'hero')):
        for i, (n, v) in enumerate(group):
            x = 40 + (i % per) * (cs[0] + 12); yy = y + (i // per) * (cs[1] + 70)
            pth = os.path.join(VEG, 'renders', reg, f'{n}_{view}.png')
            if os.path.exists(pth):
                img = alpha_over(Image.open(pth)); img.thumbnail(cs, Image.LANCZOS)
                im.paste(img, (x + (cs[0] - img.width) // 2, yy + (cs[1] - img.height) // 2))
            d.rectangle([x, yy, x + cs[0], yy + cs[1]], outline=LINE)
            col = BADGE.get(v['label'], ((90, 90, 90), ''))[0]; d.ellipse([x + 4, yy + cs[1] + 10, x + 18, yy + cs[1] + 24], fill=col)
            lab = v['common'][:30]; d.text((x + 24, yy + cs[1] + 6), lab, fill=INK, font=F(16, True))
            h = v['stats']['height_m']; hs = f'{h:.1f} m' if h >= 1 else f'{h * 100:.0f} cm'
            d.text((x + 24, yy + cs[1] + 28), f"{n.split('_')[1]} · {hs}", fill=SUB, font=F(14))
        y += ((len(group) + per - 1) // per) * (cs[1] + 70)
    y += 8
im = im.crop((0, 0, W, y + 20)); out = os.path.join(VEG, 'sheets', 'T6_SHEET_M1.png'); im.save(out, optimize=True)
im.resize((im.width // 3, im.height // 3), Image.LANCZOS).save(out[:-4] + '_small.jpg', quality=88); print('CONTACT', out, im.size)
