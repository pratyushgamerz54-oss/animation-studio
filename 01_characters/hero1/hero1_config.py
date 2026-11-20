"""HERO 1 — main hero — character config. NAME NOT CONFIRMED (U-01): use 'HERO 1'.
CONFIRMED: role, powers Fire + Magical Portal. Director: build Hero 1 by combining elements of the
reference set. Everything visual = PROPOSAL."""
import math

AX = lambda c: abs(c.x)
CFG = {
    'id': 'HERO1', 'name': 'Hero 1', 'role': 'Hero 1 / main hero (name pending)',
    'powers': ['Fire Manipulation', 'Magical Portal'],
    'power_rows': ['fire', 'portal'],
    'reference': 'combination of the Director reference set (no own reference)',
    'ref_notes': 'Combined: long flowing coat with embroidered trim (Ramarat), glowing chest core (Saithan), '
                 'fitted armoured under-suit & pauldrons (Pratyush), forearm gauntlets (Max), energy on the arms (Yayaki). '
                 'Own identity: crimson + gold fire palette, swept hair with flame-orange tips.',
    'age': '18 (proposed)', 'height': 1.80,
    'body_type': 'Athletic heroic build — broad shoulders, V-taper, strong arms',
    'silhouette': 'Swept-back flame hair + high coat collar + long split coat tails = triangular "flame" read',
    'build': {'shoulder': 1.07, 'chest': 1.06, 'waist': .98, 'limb': 1.06, 'muscle': 1.25},
    'head': {'jaw': 1.12, 'chin': 1.1, 'cheek': 1.15, 'nose': 1.0, 'brow': 1.2},
    'eyes': {'size': 1.05}, 'mouth_w': 1.1,
    'expressions': ['neutral', 'happy', 'angry', 'sad', 'fear', 'shocked', 'confident', 'evil', 'serious', 'crying', 'blink'],
    'pal': {
        'skin': '#9C6B4A', 'skin_tint': '#A9564A', 'lip': '#7E4436',
        'hair': '#2A1A12', 'hair_tip': '#FF7A1A', 'brow': '#24160F',
        'eye': '#B8741F', 'eye_dark': '#5A3008', 'power_eye': '#FFB347',
        'coat': '#7A1414', 'suit': '#1C1A1F', 'gold': '#D4A440', 'armor': '#3A2E2A',
        'boot': '#1E1715', 'accent': '#FF8A1F',
        'fire_core': '#FFF2B0', 'fire_mid': '#FF8A1F', 'fire_outer': '#B3170A',
        'portal_rim': '#FFC25A', 'portal_deep': '#3A0A05', 'power_glow': '#FF9A3C', 'power_core': '#FFF2D6',
    },
    'hair': {'style': 'swept', 'seed': 12},
    'materials': {
        'suit': {'type': 'accent', 'base': '#1C1A1F', 'accent': '#FF8A1F', 'threshold': .8, 'rough': .5, 'sheen': .3, 'emit': .6, 'bump': .3},
        'coat': {'type': 'accent', 'base': '#7A1414', 'accent': '#D4A440', 'threshold': .6, 'rough': .6, 'sheen': .45, 'metal': .0, 'bump': .4},
        'armor': {'type': 'accent', 'base': '#3A2E2A', 'accent': '#D4A440', 'threshold': .7, 'rough': .35, 'metal': .6, 'bump': .1},
        'gold': {'base': '#D4A440', 'rough': .3, 'metal': 1.0},
        'boot': {'type': 'accent', 'base': '#1E1715', 'accent': '#D4A440', 'threshold': .6, 'rough': .4, 'metal': .2},
        'glove': {'base': '#1A1414', 'rough': .5, 'sheen': .2, 'bump': .2, 'bump_scale': 800},
        'core': {'type': 'emission', 'base': '#FF8A1F', 'strength': 7.0},
    },
    'glow_mats': ['core'],
    'costume': [
        {'kind': 'trim', 'name': 'SUIT', 'mat': 'suit', 'offset': .004, 'solid': .002,
         'keep': lambda c: .10 < c.z < 1.515 and AX(c) < .705,
         'accent': lambda c, n: (AX(c) < .22 and abs(n.x) > .975 and .95 < c.z < 1.36) or
                                (AX(c) > .04 and c.z < .93 and n.x * math.copysign(1, c.x) > .97)},
        # coat body: open front (shows the suit + fire core), sleeves to the forearm
        {'kind': 'trim', 'name': 'COAT', 'mat': 'coat', 'offset': .016, 'solid': .004,
         'keep': lambda c: .98 < c.z < 1.50 and AX(c) < .62 and not (c.y < -.02 and AX(c) < .075 and c.z < 1.44),
         'accent': lambda c, n: (c.y < -.02 and .055 < AX(c) < .095 and c.z < 1.44) or AX(c) > .595 or c.z < 1.0},
        {'kind': 'trim', 'name': 'COAT_COLLAR', 'mat': 'coat', 'offset': .030, 'solid': .004,
         'keep': lambda c: 1.42 < c.z < 1.545 and AX(c) < .12 and not (c.y < -.04 and AX(c) < .03)},
        {'kind': 'skirt', 'name': 'COAT_TAILS', 'mat': 'coat', 'z_top': 1.0, 'z_bottom': .32, 'flare': .45,
         'open_front': 1.1, 'offset': .03, 'hem': .05, 'front_band': 1, 'back_extra': .05},
        {'kind': 'trim', 'name': 'PAULDRON', 'mirror': True, 'mat': 'armor', 'coll': 'ACCESSORIES', 'offset': .028,
         'solid': .005, 'bevel': True, 'keep': lambda c: .15 < c.x < .30 and c.z > 1.385, 'accent': lambda c, n: c.x > .28},
        {'kind': 'trim', 'name': 'GAUNTLET', 'mirror': True, 'mat': 'armor', 'coll': 'ACCESSORIES', 'offset': .020,
         'solid': .005, 'bevel': True, 'keep': lambda c: .56 < c.x < .70, 'accent': lambda c, n: c.x > .685 or c.x < .575},
        {'kind': 'trim', 'name': 'BOOT', 'mirror': True, 'mat': 'boot', 'offset': .011, 'solid': .003,
         'keep': lambda c: c.z < .36 and c.x > 0, 'accent': lambda c, n: c.z < .022 or c.z > .33},
        {'kind': 'trim', 'name': 'GLOVE', 'mirror': True, 'mat': 'glove', 'coll': 'ACCESSORIES', 'offset': .0028,
         'solid': .0015, 'keep': lambda c: .70 < c.x},
        {'kind': 'trim', 'name': 'BELT', 'mat': 'gold', 'coll': 'ACCESSORIES', 'offset': .020, 'solid': .005,
         'keep': lambda c: .95 < c.z < 1.06 and AX(c) < .25},
        {'kind': 'disc', 'name': 'CHEST_CORE', 'mat': 'core', 'pos': (0, 1.30), 'radius': .032, 'depth': .01},
        {'kind': 'disc', 'name': 'CORE_RING', 'mat': 'gold', 'pos': (0, 1.30), 'radius': .040, 'depth': .006},
    ],
    'face_notes': [
        ('EYES', 'Amber iris #B8741F; glow #FFB347 when fire is active'),
        ('BROWS', 'Thick, straight, determined; dark brown'),
        ('NOSE / LIPS', 'Strong straight nose, medium lips'),
        ('JAW / CHIN', 'Broad heroic jaw, square chin, high cheekbones'),
        ('PROPORTIONS', '7.5 heads; eye line at 1/2 head height'),
        ('HAIR', 'Dark brown swept up-and-back clumps; tips burn to flame-orange #FF7A1A'),
    ],
    'costume_groups': [
        ('suit', 'Inner: armoured under-suit', ['SUIT'], 'Fire-resistant aramid knit', '#1C1A1F; seams #FF8A1F', 'Skinned, no sim'),
        ('coat', 'Outer: long battle coat', ['COAT', 'COAT_COLLAR', 'COAT_TAILS'], 'Heavy wool-silk blend, gold embroidery',
         '#7A1414 rough .6 sheen .45; trim #D4A440', 'Coat tails: cloth sim (pinned at waist)'),
        ('armor', 'Pauldrons + gauntlets', ['PAULDRON_L', 'PAULDRON_R', 'GAUNTLET_L'], 'Forged plate', '#3A2E2A metal .6; gold edges', 'Rigid'),
        ('core', 'Special: chest fire core', ['CHEST_CORE', 'CORE_RING'], 'Crystal core + gold ring', 'core #FF8A1F emission; ring gold', 'Rigid'),
        ('boots', 'Shoes: plated boots', ['BOOT_L', 'BOOT_R'], 'Leather + plate', '#1E1715; gold bands', 'Rigid'),
        ('gloves', 'Gloves', ['GLOVE_L'], 'Leather', '#1A1414', 'Skinned per finger'),
        ('belt', 'Belt', ['BELT'], 'Gold plate belt', '#D4A440 metal 1.0', 'Rigid'),
        ('hair', 'Hair', ['HAIR', 'HAIR_CAP'], 'Stylised clumps, flame tips', 'root #2A1A12 → tip #FF7A1A', 'Optional spring bones'),
    ],
}
