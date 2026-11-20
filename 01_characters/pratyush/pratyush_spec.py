"""Pratyush — design spec v1 (PROPOSAL, awaiting Director approval).

Single source of truth: the design sheet, the 3D model and the VFX all read
their colours / measurements from here, so they can never drift apart.
CONFIRMED by Director: name 'Pratyush', role Hero 2, powers Super Speed,
Magical Portal, Lightning. EVERYTHING ELSE below is a proposal.
"""

SPEC = {
    'name': 'Pratyush',
    'role': 'Hero 2',
    'powers': ['Super Speed', 'Magical Portal', 'Lightning'],       # CONFIRMED
    # ---- proposals ----
    'age': '17 (proposed)',
    'height_m': 1.75,             # without hair
    'head_height_m': 0.234,       # -> 7.5 heads tall (heroic stylized realism)
    'shoulder_width_m': 0.51,     # outer deltoids, arms relaxed (measured on model)
    'chest_width_m': 0.32,
    'arm_length_m': 0.75,         # shoulder joint -> fingertip
    'leg_length_m': 0.90,         # hip joint -> floor
    'inseam_m': 0.82,
    'hand_length_m': 0.19,
    'foot_length_m': 0.26,
    'body_type': 'Lean athletic sprinter build — long legs, narrow waist, defined shoulders',
    'silhouette': 'Sharp upward-swept hair spikes + high collar + angular shoulder plates = forward-leaning "arrow"',
    'reference': 'reference/pratyush_ref_01.png (Director). Taken from it: sleek armoured full-body speed suit,'
                 ' gloves, armoured boots, crackling lightning around the body, sprint pose. Kept ORIGINAL:'
                 ' colours (navy/electric blue, not red/gold), chevron emblem (not a circle bolt), no cowl.',
}

# Colour palette (HEX). Same dict drives materials, so sheet == model.
PAL = {
    'skin':        '#B07650',   # warm medium brown
    'lip':         '#8E5141',
    'hair':        '#17120F',   # near-black brown
    'hair_streak': '#2EA8FF',   # electric-blue streak in front fringe
    'eye':         '#5A361F',   # dark brown iris
    'eye_dark':    '#2A170C',
    'suit':        '#16243F',   # deep navy — main speed suit
    'armor':       '#5C6B80',   # gunmetal-blue armour plates
    'boot':        '#1E2C4A',
    'accent':      '#2EA8FF',   # electric-blue piping / lightning emblem
    'under':       '#262931',   # charcoal under-layer (side panels)
    'shoe_sole':   '#2EA8FF',
    'glove':       '#141519',
    'belt':        '#1D1E23',
    'metal':       '#B7C0CC',   # brushed silver (zip, buckle, bracers)
    'power_glow':  '#4FD8FF',   # lightning glow / bracer core
    'power_core':  '#F2FBFF',   # lightning core (white-hot)
    'power_eye':   '#5BE0FF',   # eyes when powered
    'portal_rim':  '#6FE7FF',
    'portal_deep': '#0A2A5A',
    'speed_trail': '#2EA8FF',
}

# ---------------------------------------------------------------- face shapes
# Mouth params: corner_l/r (m, + = up), open_u/open_l (m), width (x), pucker (0-1),
# lip_u/lip_l thickness (m), v0 vertical shift (m)
MOUTH_SHAPES = {
    'neutral':   {},
    'happy':     {'corner_l': 0.0065, 'corner_r': 0.0065, 'open_u': 0.0018, 'open_l': 0.0040, 'width': 1.10},
    'angry':     {'corner_l': -0.0026, 'corner_r': -0.0026, 'open_u': 0.0022, 'open_l': 0.0022, 'width': 0.96},
    'sad':       {'corner_l': -0.0061, 'corner_r': -0.0061, 'width': 0.90},
    'fear':      {'corner_l': -0.0023, 'corner_r': -0.0023, 'open_u': 0.0020, 'open_l': 0.0058, 'width': 1.08},
    'shocked':   {'open_u': 0.0040, 'open_l': 0.0115, 'width': 0.74, 'pucker': 0.6},
    'confident': {'corner_l': 0.0017, 'corner_r': 0.0061, 'width': 1.00},
    'evil':      {'corner_l': 0.0070, 'corner_r': 0.0099, 'open_u': 0.0030, 'open_l': 0.0034, 'width': 1.28},
    'serious':   {'corner_l': -0.0012, 'corner_r': -0.0012, 'width': 0.93, 'lip_u': 0.0026},
    'crying':    {'corner_l': -0.0072, 'corner_r': -0.0072, 'open_u': 0.0030, 'open_l': 0.0080, 'width': 1.05},
    # lip-sync phonemes (used in Stage 7, built now so topology is final)
    'PH_A':      {'open_u': 0.0040, 'open_l': 0.0120, 'width': 1.00},
    'PH_E':      {'open_u': 0.0030, 'open_l': 0.0060, 'width': 1.15, 'corner_l': 0.0010, 'corner_r': 0.0010},
    'PH_I':      {'open_u': 0.0020, 'open_l': 0.0040, 'width': 1.20, 'corner_l': 0.0020, 'corner_r': 0.0020},
    'PH_O':      {'open_u': 0.0050, 'open_l': 0.0100, 'width': 0.70, 'pucker': 0.7},
    'PH_U':      {'open_u': 0.0020, 'open_l': 0.0030, 'width': 0.56, 'pucker': 1.0, 'lip_u': 0.0040, 'lip_l': 0.0050},
    'PH_MBP':    {'lip_u': 0.0024, 'lip_l': 0.0032, 'width': 0.97},
    'PH_FV':     {'open_u': 0.0006, 'open_l': 0.0018, 'lip_l': 0.0030},
    'PH_L':      {'open_u': 0.0030, 'open_l': 0.0070, 'width': 0.95},
    'PH_W':      {'open_u': 0.0018, 'open_l': 0.0030, 'width': 0.50, 'pucker': 1.0, 'lip_u': 0.0040, 'lip_l': 0.0050},
    'PH_REST':   {'open_u': 0.0004, 'open_l': 0.0006},
}

BROW_SHAPES = {
    'neutral':   {},
    'happy':     {'inner': 0.0028, 'outer': 0.0021},
    'angry':     {'inner': -0.0059, 'outer': 0.0028, 'arch': 0.0010},
    'sad':       {'inner': 0.0059, 'outer': -0.0028, 'arch': 0.0010},
    'fear':      {'inner': 0.0070, 'outer': 0.0014},
    'shocked':   {'inner': 0.0084, 'outer': 0.0070, 'arch': 0.0040},
    'confident': {'l_extra': 0.0045},
    'evil':      {'inner': -0.0056, 'outer': 0.0042, 'l_extra': 0.0028},
    'serious':   {'inner': -0.0022, 'outer': 0.0007},
    'crying':    {'inner': 0.0073, 'outer': -0.0031},
}

# lid angles (deg): lid_up more negative = more open; lid_lo larger = more open
EXPRESSIONS = {
    'neutral':   {'mouth': 'neutral',   'brows': 'neutral',   'lid_up': -24, 'lid_lo': 30},
    'happy':     {'mouth': 'happy',     'brows': 'happy',     'lid_up': -22, 'lid_lo': 12},
    'angry':     {'mouth': 'angry',     'brows': 'angry',     'lid_up': -11, 'lid_lo': 22},
    'sad':       {'mouth': 'sad',       'brows': 'sad',       'lid_up': -13, 'lid_lo': 28, 'gaze': (0, -10)},
    'fear':      {'mouth': 'fear',      'brows': 'fear',      'lid_up': -42, 'lid_lo': 42},
    'shocked':   {'mouth': 'shocked',   'brows': 'shocked',   'lid_up': -48, 'lid_lo': 46},
    'confident': {'mouth': 'confident', 'brows': 'confident', 'lid_up': -17, 'lid_lo': 24, 'lid_up_L': -6},
    'evil':      {'mouth': 'evil',      'brows': 'evil',      'lid_up': -11, 'lid_lo': 16},
    'serious':   {'mouth': 'serious',   'brows': 'serious',   'lid_up': -17, 'lid_lo': 26},
    'crying':    {'mouth': 'crying',    'brows': 'crying',    'lid_up': 2,   'lid_lo': 8, 'tears': True},
    'blink':     {'mouth': 'neutral',   'brows': 'neutral',   'lid_up': 6,   'lid_lo': -4},
}
