"""PRATYUSH — Hero 2 — character config (single source of truth).
CONFIRMED by Director: name, role, powers, reference image. Everything else = PROPOSAL (U-04)."""
import math

CFG = {
    'id': 'PRATYUSH', 'name': 'Pratyush', 'role': 'Hero 2 / main second lead',
    'powers': ['Super Speed', 'Magical Portal', 'Lightning'],
    'power_rows': ['speed', 'lightning', 'portal'],
    'reference': 'reference/pratyush_ref_01.png',
    'ref_notes': 'Taken: sleek armoured full-body speed suit, gloves, armoured boots, crackling lightning, sprint pose. '
                 'Kept original: navy / electric-blue colours (not red/gold), chevron emblem (no bolt-in-circle), no cowl.',
    'age': '17 (proposed)', 'height': 1.75,
    'body_type': 'Lean athletic sprinter: long legs, narrow waist, defined shoulders',
    'silhouette': 'Upward-swept hair spikes + high armoured collar + angular shoulder plates',
    'build': {'shoulder': 1.0, 'chest': 1.0, 'waist': .97, 'limb': 1.0, 'muscle': 1.1},
    'head': {'jaw': 1.05, 'chin': 1.05, 'cheek': 1.1, 'nose': 1.05, 'brow': 1.1},
    'expressions': ['neutral', 'happy', 'angry', 'sad', 'fear', 'shocked', 'confident', 'evil', 'serious',
                    'crying', 'blink'],
    'pal': {
        'skin': '#B07650', 'skin_tint': '#B5614A', 'lip': '#8E5141',
        'hair': '#17120F', 'hair_streak': '#2EA8FF', 'brow': '#17120F',
        'eye': '#5A361F', 'eye_dark': '#2A170C', 'power_eye': '#5BE0FF',
        'suit': '#16243F', 'armor': '#5C6B80', 'accent': '#2EA8FF', 'boot': '#1E2C4A', 'sole': '#2EA8FF',
        'glove': '#141519', 'metal': '#B7C0CC', 'power_glow': '#4FD8FF', 'power_core': '#F2FBFF',
        'portal_rim': '#6FE7FF', 'portal_deep': '#0A2A5A', 'speed_trail': '#2EA8FF',
    },
    'hair': {'style': 'spiky', 'streak': True},
    'eyes': {'size': 1.08}, 'mouth_w': 1.1,
    'materials': {
        'suit': {'type': 'accent', 'base': '#16243F', 'accent': '#2EA8FF', 'threshold': .80, 'rough': .45, 'sheen': .35, 'emit': .8, 'bump': .35},
        'armor': {'type': 'accent', 'base': '#5C6B80', 'accent': '#2EA8FF', 'threshold': .8, 'rough': .32, 'metal': .65, 'emit': 1.0, 'bump': .1},
        'boot': {'type': 'accent', 'base': '#1E2C4A', 'accent': '#2EA8FF', 'threshold': .6, 'rough': .4, 'emit': .6, 'bump': .1},
        'glove': {'base': '#141519', 'rough': .45, 'sheen': .2, 'bump': .2, 'bump_scale': 800},
        'metal': {'base': '#B7C0CC', 'rough': .25, 'metal': 1.0},
        'core': {'type': 'emission', 'base': '#4FD8FF', 'strength': 6.0},
    },
    'costume': [
        {'kind': 'trim', 'name': 'SUIT', 'mat': 'suit', 'offset': .004, 'solid': .002,
         'keep': lambda c: .10 < c.z < 1.515 and abs(c.x) < .705,
         'accent': lambda c, n: (abs(c.x) > .26 and n.z > .86 and c.z > 1.3) or
                                (abs(c.x) < .22 and abs(n.x) > .975 and .95 < c.z < 1.36) or
                                (abs(c.x) > .04 and c.z < .93 and n.x * math.copysign(1, c.x) > .97) or
                                (c.y < -.04 and abs(c.z - (1.21 - .55 * abs(c.x))) < .012 and abs(c.x) < .16)},
        {'kind': 'trim', 'name': 'COLLAR', 'mat': 'armor', 'offset': .017, 'solid': .005,
         'keep': lambda c: 1.43 < c.z < 1.535 and abs(c.x) < .11, 'accent': lambda c, n: c.z > 1.522},
        {'kind': 'trim', 'name': 'CHEST_PLATE', 'mat': 'armor', 'coll': 'ACCESSORIES', 'offset': .011, 'solid': .005, 'bevel': True,
         'keep': lambda c: c.y < -.012 and 1.23 < c.z < 1.47 and abs(c.x) < .20,
         'accent': lambda c, n: c.z < 1.245 or abs(c.x) > .185},
        {'kind': 'trim', 'name': 'PAULDRON', 'mirror': True, 'mat': 'armor', 'coll': 'ACCESSORIES', 'offset': .019, 'solid': .005,
         'bevel': True, 'keep': lambda c: .15 < c.x < .31 and c.z > 1.375, 'accent': lambda c, n: c.x > .29},
        {'kind': 'trim', 'name': 'KNEE', 'mirror': True, 'mat': 'armor', 'coll': 'ACCESSORIES', 'offset': .014, 'solid': .005,
         'bevel': True, 'keep': lambda c: c.x > 0 and .44 < c.z < .57 and c.y < .005},
        {'kind': 'trim', 'name': 'BOOT', 'mirror': True, 'mat': 'boot', 'offset': .011, 'solid': .003,
         'keep': lambda c: c.z < .33 and c.x > 0,
         'accent': lambda c, n: c.z < .024 or .285 < c.z or abs(c.z - .16) < .008},
        {'kind': 'trim', 'name': 'GLOVE', 'mirror': True, 'mat': 'glove', 'coll': 'ACCESSORIES', 'offset': .0028, 'solid': .0015,
         'keep': lambda c: .698 < c.x},
        {'kind': 'trim', 'name': 'BRACER', 'mirror': True, 'mat': 'metal', 'coll': 'ACCESSORIES', 'offset': .014, 'solid': .005,
         'keep': lambda c: .60 < c.x < .685},
        {'kind': 'trim', 'name': 'BELT', 'mat': 'armor', 'coll': 'ACCESSORIES', 'offset': .010, 'solid': .006,
         'keep': lambda c: .92 < c.z < 1.08 and abs(c.x) < .25, 'accent': lambda c, n: abs(c.z - 1.0) < .012},
        {'kind': 'box', 'name': 'BELT_BUCKLE', 'mat': 'metal', 'loc': (0, -.135, 1.0), 'size': (.042, .006, .030)},
        {'kind': 'disc', 'name': 'BRACER_CORE_L', 'mat': 'core', 'on': 'BRACER_L', 'pos': (.6425, 1.43), 'radius': .011,
         'bone': 'forearm_L', 'top': True, 'mirror': True},
        {'kind': 'emblem', 'name': 'EMBLEM', 'mat': 'core', 'on': 'CHEST_PLATE', 'pos': (0, 1.36), 'scale': 1.2,
         'poly': [(0, .026), (.034, -.010), (.022, -.020), (.004, -.002), (.006, -.016), (-.006, -.008),
                  (-.004, -.002), (-.022, -.020), (-.034, -.010)]},
    ],
}

CFG['glow_mats'] = ['core']
CFG['face_notes'] = [
    ('EYES', 'Dark-brown iris #5A361F, almond lids; glow #5BE0FF when powered'),
    ('BROWS', 'Straight, slightly raised outer end, tapered; near-black'),
    ('NOSE / LIPS', 'Straight bridge, rounded tip, defined alae; medium lips with philtrum'),
    ('JAW / CHIN', 'Defined jawline and gonial angle, firm rounded chin; high cheekbones'),
    ('PROPORTIONS', 'Eye line at 1/2 head height, eye spacing = 1 eye width, mouth at 2/3 of lower face'),
    ('HAIR', 'Near-black spiky ribbon clumps swept up & back; 1 electric-blue streak in the fringe'),
]
CFG['costume_groups'] = [
    ('suit', 'Main: armoured speed suit', ['SUIT'], 'Stretch technical knit (4-way)',
     '#16243F rough .45 sheen .35; piping #2EA8FF emissive', 'Skin-tight: skinned, no sim; corrective shapes elbows/knees'),
    ('armor', 'Outer: chest plate, pauldrons, knees, collar', ['CHEST_PLATE', 'PAULDRON_L', 'PAULDRON_R', 'KNEE_L', 'KNEE_R', 'COLLAR', 'EMBLEM'],
     'Moulded composite plates', '#5C6B80 metallic .65 rough .32; edge light #2EA8FF', 'Rigid, skinned 1:1'),
    ('boots', 'Shoes: armoured sprint boots', ['BOOT_L', 'BOOT_R'], 'Armoured synthetic leather', '#1E2C4A; sole & bands #2EA8FF', 'Rigid'),
    ('gloves', 'Gloves: full-finger grip', ['GLOVE_L'], 'Grip synthetic', '#141519 rough .45', 'Skinned per finger'),
    ('belt', 'Belt + buckle', ['BELT', 'BELT_BUCKLE'], 'Plate belt', '#5C6B80 / #B7C0CC metal', 'Rigid'),
    ('bracers', 'Special equipment: speed bracers', ['BRACER_L', 'BRACER_CORE_L'], 'Brushed metal + energy core',
     '#B7C0CC metal; core #4FD8FF emission', 'Rigid on forearm'),
    ('hair', 'Hair (cap + clumps)', ['HAIR', 'HAIR_CAP'], 'Stylised clump geometry', '#17120F rough .42 sheen .5', 'Optional spring bones'),
]
