"""TASK 06 · contact sheet of the populated-region previews (python3 + Pillow).
    python3 t6_pop_sheet.py → 02_world/ecosystem/renders/T6_POPULATED_PREVIEWS.png (+ _small.jpg)"""
import os, glob
from PIL import Image, ImageDraw
from t6_compose_sheets import F, BG, INK, SUB, HEAD
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
D = os.path.join(ROOT, '02_world', 'ecosystem', 'renders', 'populated')
REG = [('T6_POP_R01_ASHRAM_VALLEY', 'R-01 ASHRAM VALLEY — meadow, Banj oak + Burans groves, deodar ring, ONE Peepal on a PROPOSED chabutra, PROPOSED garden (Tulsi + Marigold)'),
       ('T6_POP_R02_ENCHANTED_FOREST', 'R-02 ENCHANTED FOREST — ~75 % natural (Giant Elder, Teal Beech, Moss Oak, Yew, snags) / ~25 % approved fantasy, ferns, moss, logs'),
       ('T6_POP_R03_MOUNTAIN_KINGDOM', 'R-03 MOUNTAIN KINGDOM (zone M1, cave entrance) — spruce + silver fir forest, blue pine, Burans, birch, tussock clearings'),
       ('T6_POP_R04_GOLDEN_DESERT', 'R-04 GOLDEN DESERT — bare dunes; wadis: khejri, acacia, aak, ber, sewan grass; rocky slopes: euphorbia; oases: date palms'),
       ('T6_POP_R05_FORBIDDEN_LANDS', 'R-05 FORBIDDEN LANDS — outer rim only: charred dead trees, dead thorn shrubs, grey lichen, sparse hardy grass')]
W = 2600; tw = (W - 120) // 2; th = int(tw * 9 / 16)
rows = [(k, t, sorted(glob.glob(os.path.join(D, f'{k}_v001__*.png')))) for k, t in REG]
rows = [r for r in rows if r[2]]
H = 170 + sum(80 + ((len(fs) + 1) // 2) * (th + 50) for _, _, fs in rows)
im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, 150], fill=HEAD)
d.text((40, 22), 'TASK 06 · MILESTONE 2 — POPULATED REGIONS (NG_T6_ECOSYSTEM on the approved TASK 05 terrain)', fill=(240, 240, 232), font=F(40, True))
d.text((40, 86), 'preview resolution (final 4K on the GPU PC) · spring · wind breeze frame · T6 eye-level cameras + the approved TASK 05 shot cameras · TASK 05 files untouched',
       fill=(196, 206, 198), font=F(21))
y = 170
for k, t, fs in rows:
    d.text((40, y), t, fill=INK, font=F(24, True)); y += 44
    for i, f in enumerate(fs):
        x = 40 + (i % 2) * (tw + 40); yy = y + (i // 2) * (th + 50)
        im.paste(Image.open(f).convert('RGB').resize((tw, th), Image.LANCZOS), (x, yy))
        d.text((x, yy + th + 6), os.path.basename(f).split('__')[-1][:-4], fill=SUB, font=F(18))
    y += ((len(fs) + 1) // 2) * (th + 50) + 36
out = os.path.join(ROOT, '02_world', 'ecosystem', 'renders', 'T6_POPULATED_PREVIEWS.png')
im = im.crop((0, 0, W, y)); im.save(out, optimize=True)
im.resize((im.width // 2, im.height // 2), Image.LANCZOS).save(out[:-4] + '_small.jpg', quality=86); print('POP_SHEET', out, im.size)
