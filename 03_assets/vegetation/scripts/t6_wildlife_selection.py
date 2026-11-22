"""Decision Sheet 01 §5 · WILDLIFE SELECTION SHEET (pending Director). Source list = the existing wildlife proposal
(ECOSYSTEM_BIBLE.md §7 = WILDLIFE_PROPOSAL.png) — no animal added or removed. Writes the .md table and a .png sheet."""
import os
from PIL import Image, ImageDraw, ImageFont
ECO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '02_world', 'ecosystem'))
REF = 'text only — WILDLIFE_PROPOSAL.png / ECOSYSTEM_BIBLE §7 (no visual design yet)'
# (animal, region code, habitat, proposed film appearance, recommendation)  — recommendation is NOT a decision
A = [
 ('House sparrow', 'R-01', 'valley villages, Ashram roofs + yard', 'small flocks on roofs / courtyard ground', 'OPTIONAL'),
 ('Common myna', 'R-01', 'open valley, around buildings', 'pairs on the courtyard / walls', 'OPTIONAL'),
 ('Rose-ringed parakeet', 'R-01', 'groves, Peepal canopy', 'flock flying out of the Peepal', 'ESSENTIAL (rec.)'),
 ('Peacock (Indian peafowl)', 'R-01', 'open ground, field edges', 'one male displaying near the training ground (wide)', 'OPTIONAL'),
 ('Kingfisher', 'R-01', 'river + lake bay', 'perched by the ghat, dive (close detail)', 'OPTIONAL'),
 ('Crow', 'R-01', 'villages, Ashram', 'background calls / silhouettes', 'OPTIONAL'),
 ('Common Mormon butterfly', 'R-01', 'Ashram garden, flowers', 'near camera in the garden (spring)', 'ESSENTIAL (rec.)'),
 ('Blue tiger butterfly', 'R-01', 'meadows, flowers', 'meadow ambience', 'OPTIONAL'),
 ('Honey bee', 'R-01', 'flowers, marigold beds', 'macro detail in the garden', 'OPTIONAL'),
 ('Dragonfly', 'R-01 / R-08', 'pond, lake bay, still water', 'hovering over lotus / lake', 'OPTIONAL'),
 ('Firefly', 'R-01 / R-02', 'meadow + forest edge at dusk', 'night ambience (particles)', 'OPTIONAL'),
 ('Squirrel', 'R-01', 'groves, Peepal trunk', 'running up the Peepal (close)', 'OPTIONAL'),
 ('Hare', 'R-01 / R-06', 'meadows, grassland', 'darting across a field (mid)', 'OPTIONAL'),
 ('Langur monkey', 'R-01', 'groves, forest ring', 'troop in the oak groves (mid / far)', 'OPTIONAL'),
 ('Spotted deer (chital)', 'R-01', 'forest edge, meadows', 'small herd at the forest edge (far)', 'ESSENTIAL (rec.)'),
 ('Small pond fish', 'R-01', 'Ashram lake bay / pond', 'under the lotus (water close-up)', 'OPTIONAL'),
 ('Frog', 'R-01 / R-02', 'pond margins, forest pools', 'sound + one close detail', 'OPTIONAL'),
 ('Owl', 'R-02', 'old forest, hollow trees', 'night shot on a branch', 'OPTIONAL'),
 ('Woodpecker', 'R-02', 'dead snags, old trunks', 'on the Dead Snag (mid)', 'OPTIONAL'),
 ('Hornbill', 'R-02', 'canopy of giant trees', 'crossing between Giant Elders', 'OPTIONAL'),
 ('Small songbirds', 'R-02', 'all forest layers', 'ambience', 'OPTIONAL'),
 ('Moth', 'R-02', 'night forest, glowing plants', 'around Lantern-tree pods at night', 'OPTIONAL'),
 ('Beetle', 'R-02 / R-04', 'logs, forest floor; desert sand', 'macro on logs / sand', 'OPTIONAL'),
 ('Forest butterflies', 'R-02', 'sun patches in glades', 'in light shafts (close / mid)', 'OPTIONAL'),
 ('Flying squirrel', 'R-02', 'giant trees', 'glide between trunks (night)', 'OPTIONAL'),
 ('Red-panda-like climber', 'R-02', 'mid canopy', 'on a moss-oak limb', 'OPTIONAL'),
 ('Deer', 'R-02', 'forest glades', 'rare, distant', 'OPTIONAL'),
 ('Wild boar', 'R-02', 'forest floor', 'rare, distant', 'OPTIONAL'),
 ('Newt', 'R-02', 'forest pools', 'macro at pools', 'OPTIONAL'),
 ('Eagle / lammergeier', 'R-03', 'cliffs, open sky', 'soaring over the range (wide)', 'ESSENTIAL (rec.)'),
 ('Himalayan monal', 'R-03', 'alpine meadows, tree line', 'colourful pheasant in a meadow', 'OPTIONAL'),
 ('Snowcock', 'R-03', 'high rocky slopes', 'far', 'OPTIONAL'),
 ('Bumblebee', 'R-03', 'alpine flowers', 'on gentian / poppy (macro)', 'OPTIONAL'),
 ('Alpine butterflies', 'R-03', 'alpine meadows', 'meadow ambience', 'OPTIONAL'),
 ('Pika', 'R-03', 'boulder fields', 'between rocks (close)', 'OPTIONAL'),
 ('Marmot', 'R-03', 'alpine meadows', 'standing sentinel (mid)', 'OPTIONAL'),
 ('Himalayan tahr / blue sheep', 'R-03', 'steep cliffs', 'herd on cliffs (far)', 'OPTIONAL'),
 ('Snow leopard', 'R-03', 'high cliffs', 'very rare, distant', 'OPTIONAL'),
 ('Trout', 'R-03', 'mountain streams', 'in a clear stream', 'OPTIONAL'),
 ('Lark', 'R-06', 'grasslands', 'ambience', 'OPTIONAL'),
 ('Kite', 'R-06', 'open sky over plains', 'circling (wide)', 'OPTIONAL'),
 ('Starling flock', 'R-06', 'plains, sky', 'murmuration (wide)', 'OPTIONAL'),
 ('Grasshopper', 'R-06', 'grassland', 'macro', 'OPTIONAL'),
 ('Mongoose', 'R-06', 'grassland, shrubs', 'mid', 'OPTIONAL'),
 ('Blackbuck / antelope', 'R-06', 'open plains', 'herd running (wide)', 'OPTIONAL'),
 ('Wild horses', 'R-06', 'open plains', 'herd (wide)', 'OPTIONAL'),
 ('Heron', 'R-08', 'lake shores', 'wading (mid)', 'OPTIONAL'),
 ('Egret', 'R-08', 'lake shores, reeds', 'white accents on the shore', 'OPTIONAL'),
 ('Ducks', 'R-08', 'open lake water', 'swimming (mid)', 'OPTIONAL'),
 ('Cranes', 'R-08', 'lake shallows', 'flock (far)', 'OPTIONAL'),
 ('Damselfly', 'R-08', 'reeds, still water', 'macro', 'OPTIONAL'),
 ('Otter', 'R-08', 'lake shores', 'mid', 'OPTIONAL'),
 ('Lake fish', 'R-08', 'lakes', 'underwater / jumping', 'OPTIONAL'),
 ('Turtle', 'R-08', 'lake shallows, logs', 'basking (close)', 'OPTIONAL'),
 ('Vulture', 'R-04', 'desert sky, rocks', 'circling (wide)', 'OPTIONAL'),
 ('Desert sparrow', 'R-04', 'oases, shrubs', 'ambience', 'OPTIONAL'),
 ('Desert fox', 'R-04', 'dunes, wadis', 'at dusk (mid)', 'OPTIONAL'),
 ('Gerbil', 'R-04', 'sand, shrubs', 'macro', 'OPTIONAL'),
 ('Camel (oasis)', 'R-04', 'oases — only if inhabited (NOT CONFIRMED)', 'only if the story has people there', 'OPTIONAL'),
 ('Raven (or none)', 'R-05', 'crater rim', 'one silhouette or nothing', 'OPTIONAL'),
]
L = ['# WILDLIFE SELECTION SHEET — PENDING DIRECTOR SELECTION (Decision Sheet 01 §5)', '',
     '> **Nothing here is selected or final.** Source: the existing wildlife proposal (`02_world/ecosystem/ECOSYSTEM_BIBLE.md` §7 =',
     '> `WILDLIFE_PROPOSAL.png`). There is no separate "Wildlife Design Bible" file in the project; that proposal is the complete existing',
     '> wildlife list — nothing was added or removed. No fantasy creatures. No wildlife 3D assets will be created until you select.',
     '> "Essential / optional" column = **my recommendation only** (marked "rec."); your choice replaces it.', '',
     f'Total animals in the existing list: **{len(A)}** · actual 3D assets existing in the project: **0** (none yet; Poly Haven has only a',
     '`street_rat` scan, not downloaded, not part of the list).', '',
     '| # | Animal | Region | Existing design reference | Natural habitat | Proposed film appearance | Essential / optional | 3D asset exists | Director selection |',
     '|---|---|---|---|---|---|---|---|---|']
for i, (n, r, h, f, e) in enumerate(A, 1):
    L.append(f'| {i} | {n} | {r} | {REF} | {h} | {f} | {e} | No | ☐ select ☐ reject |')
L += ['', 'Sky Realms / Hidden Underground: no wildlife proposed (Sky Realms = proposed region, story role not confirmed).', '',
      'After your selection: low-poly rigged models (birds, deer, monkeys …) + particle flocks / insects, ambient animation cycles, sheets with',
      'turnaround + scale, QC — only for the selected animals.']
open(os.path.join(ECO, 'WILDLIFE_SELECTION_SHEET.md'), 'w').write('\n'.join(L) + '\n')
# PNG
FD = '/usr/share/fonts/truetype/dejavu/'; F = lambda n, b=False: ImageFont.truetype(FD + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), n)
W = 3300; RH = 34; H = 260 + RH * (len(A) + 1) + 120
im = Image.new('RGB', (W, H), (236, 234, 228)); d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, 150], fill=(30, 44, 38))
d.text((40, 20), 'WILDLIFE SELECTION SHEET  ·  PENDING DIRECTOR SELECTION', fill=(240, 240, 232), font=F(44, True))
d.text((40, 86), f'{len(A)} animals = the complete existing proposal list (nothing added) · no fantasy creatures · 3D assets existing: 0 · "rec." = recommendation only',
       fill=(196, 206, 198), font=F(22))
cols = [('#', 60), ('Animal', 380), ('Region', 160), ('Natural habitat', 620), ('Proposed film appearance', 760), ('Essential / optional (rec.)', 330),
        ('3D asset', 150), ('Existing design ref.', 380), ('Select', 300)]
x = 40; y = 180
for c, w in cols:
    d.text((x + 6, y), c, fill=(28, 34, 30), font=F(20, True)); x += w
y += 40
for i, (n, r, h, f, e) in enumerate(A, 1):
    if i % 2:
        d.rectangle([40, y - 4, W - 40, y + RH - 6], fill=(246, 245, 240))
    vals = [str(i), n, r, h, f, e, 'No', 'text only (§7)', '☐ select   ☐ reject']; x = 40
    for (c, w), v in zip(cols, vals):
        col = (46, 110, 64) if v.startswith('ESSENTIAL') else (28, 34, 30)
        fnt = F(18, v.startswith('ESSENTIAL'))
        while d.textlength(v, font=fnt) > w - 12 and len(v) > 4:
            v = v[:-2]
        d.text((x + 6, y), v, fill=col, font=fnt); x += w
    y += RH
d.text((40, y + 20), 'Status: PENDING — no wildlife selection is final; no wildlife 3D asset will be made before the Director selects. Source: ECOSYSTEM_BIBLE §7 / WILDLIFE_PROPOSAL.png.',
       fill=(150, 60, 30), font=F(22, True))
im.save(os.path.join(ECO, 'WILDLIFE_SELECTION_SHEET.png'), optimize=True); print('WILDLIFE SELECTION', len(A))
