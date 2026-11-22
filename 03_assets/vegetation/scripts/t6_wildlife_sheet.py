"""TASK 06 · wildlife PROPOSAL sheet (text + colour codes; no creature models until the Director approves the list)."""
import os
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '02_world', 'ecosystem', 'WILDLIFE_PROPOSAL.png'))
FD = '/usr/share/fonts/truetype/dejavu/'
F = lambda n, b=False: ImageFont.truetype(FD + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), n)
ROWS = [
    ('R-01 ASHRAM VALLEY', '#3E7A2A', ['sparrow, myna, rose-ringed parakeet', 'peacock (open ground), kingfisher (river)', 'crows'],
     ['butterflies (common Mormon, blue tiger)', 'bees at flowers, dragonflies at the pond', 'fireflies (dusk)'],
     ['squirrels, hares', 'langur monkeys in the groves'], ['spotted deer at the forest edge (distant)'], ['small fish, frogs (pond)']),
    ('R-02 ENCHANTED FOREST', '#1F4F44', ['owls, woodpeckers', 'hornbill (canopy), small songbirds'], ['moths, beetles on logs', 'butterflies in sun patches', 'fireflies'],
     ['flying squirrel', 'red-panda-like climbers'], ['deer, wild boar (rare, distant)'], ['newts, frogs at pools']),
    ('R-03 MOUNTAIN KINGDOM', '#1F3F33', ['eagle / lammergeier (soaring)', 'Himalayan monal (pheasant)', 'snowcock'], ['bumblebees, alpine butterflies'],
     ['pika, marmot'], ['Himalayan tahr / blue sheep (cliffs)', 'snow leopard (very rare, distant)'], ['trout (streams)']),
    ('R-06 GREEN PLAINS', '#7A9A3A', ['larks, kites', 'starling flocks'], ['grasshoppers, butterflies'], ['hares, mongoose'], ['blackbuck / antelope herds', 'wild horses'], ['—']),
    ('R-08 CRYSTAL LAKES', '#3E7A9A', ['herons, egrets, ducks, cranes'], ['dragonflies, damselflies'], ['otters'], ['—'], ['fish, turtles']),
    ('R-04 GOLDEN DESERT', '#C8962E', ['vultures, desert sparrows'], ['beetles'], ['desert fox, gerbils'], ['camels at oases (only if inhabited — NOT CONFIRMED)'], ['—']),
    ('R-05 FORBIDDEN LANDS', '#4A3A4F', ['ravens only (or none)'], ['none'], ['none'], ['none'], ['none']),
]
COLS = ['Birds', 'Insects / butterflies', 'Small mammals', 'Larger animals', 'Aquatic']
W, H = 3300, 1500
im = Image.new('RGB', (W, H), (236, 234, 228)); d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, 150], fill=(30, 44, 38))
d.text((40, 22), 'WILDLIFE PROPOSAL  ·  ecosystem life per region', fill=(240, 240, 232), font=F(46, True))
d.text((40, 88), 'PROPOSAL ONLY — ordinary, real-world animals; no intelligent species, monsters or story creatures. Director picks → then low-poly rigs + flocks.',
       fill=(196, 206, 198), font=F(23))
x0, y = 40, 180; cw = [520] + [540] * 5
xs = [x0]; [xs.append(xs[-1] + c) for c in cw[:-1]]
for i, c in enumerate(['Region'] + COLS):
    d.text((xs[i] + 10, y), c.upper(), fill=(28, 34, 30), font=F(22, True))
y += 44
for reg, col, *cells in ROWS:
    h = max(len(c) for c in cells) * 30 + 30
    d.rectangle([x0, y, W - 40, y + h], fill=(246, 245, 240), outline=(170, 172, 166))
    hx = col.lstrip('#'); rgb = tuple(int(hx[k:k + 2], 16) for k in (0, 2, 4))
    d.rectangle([x0, y, x0 + 18, y + h], fill=rgb)
    d.text((x0 + 32, y + 14), reg, fill=(28, 34, 30), font=F(22, True))
    for j, cell in enumerate(cells):
        for k, line in enumerate(cell):
            d.text((xs[j + 1] + 10, y + 14 + k * 30), line, fill=(28, 34, 30), font=F(19))
    y += h + 12
d.text((40, y + 10), 'Use in film: ambient life (mostly mid / far shots: flocks, butterflies near camera, deer at forest edges). Sky Realms / Underground: NOT CONFIRMED → nothing proposed.',
       fill=(92, 98, 94), font=F(20))
im = im.crop((0, 0, W, y + 60)); im.save(OUT, optimize=True); print('WILDLIFE', OUT, im.size)
