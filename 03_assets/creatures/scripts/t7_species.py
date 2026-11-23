"""t7_species — TASK 07 milestone-1 concept species (PROPOSED — none is a confirmed story element).

Every entry: real-world measurements (metres) from field-guide ranges, region code (approved map rev 01 mapping), coat zones → colour,
fur length per zone (metres), comb rules. ORDINARY = real species; FANTASY = original proposal (no powers, no intelligence).
"""
import numpy as np
import t7_anatomy as A

SPECIES = {}


def sp(sid, **kw):
    SPECIES[sid] = kw
    return kw


# ------------------------------------------------------------------------------------------------------------------------------
# R-02 ENCHANTED FOREST
sp('sambar', name='Sambar deer (stag)', latin='Rusa unicolor', kind='ORDINARY', region='R-02 Enchanted Forest', cat='Forest wildlife',
   builder=A.ungulate,
   p=dict(sh=1.30, bl=1.30, hl=0.44, neck=0.44, neck_ang=66, neck_r0=0.34 * 0.45 * 1.30, neck_r1=0.18 * 0.45 * 1.30, head_pitch=34,
          tail=0.22, ear=0.21, ear_w=0.62, ear_dir=(-0.25, 1.0, 0.12), ear_pos=(-0.06 * 0.44, 0.48 * 0.44 * 0.44, 0.10 * 0.44), muzzle=0.56, head_w=0.44,
          preorbital=True, leg_r=1.05, cd=0.42 * 1.30, voxel=0.006),
   extra=[lambda m: {'antlers': A.antlers_sambar(m, beam=0.48)}],
   coat={'*': '#6E5A45', 'body': '#6E5A45', 'belly': '#5E4C3A', 'chest': '#5A4836', 'neck': '#5C4A38', 'throat': '#544332',
         'head': '#6A5642', 'face': '#665240', 'chin': '#B9A88E', 'nose': '#1B1714', 'leg': '#4A3C2E', 'hoof': '#1E1A17',
         'tail': '#3A2E24', 'rump': '#6E5A45', 'ear': '#5A4836', 'ear_in': '#B6A68E', 'gland': '#2B2420', 'lid': '#2E2620',
         'antler': '#6E5A44', 'burr': '#4F4234'},
   fur_len={'*': 0.022, 'neck': 0.055, 'throat': 0.075, 'face': 0.009, 'head': 0.012, 'chin': 0.010, 'nose': 0.0, 'leg': 0.010,
            'hoof': 0.0, 'tail': 0.05, 'ear': 0.006, 'ear_in': 0.012, 'gland': 0.0, 'lid': 0.002, 'antler': 0.0, 'burr': 0.0},
   fur={'density': 110000, 'radius': 0.00042, 'lift': 0.55, 'droop': 0.35, 'frizz': 0.35},
   gloss=('nose',),
   mat={'antlers': 'horn'},
   eye=dict(iris='#2A1A0E', pupil_r=0.55, pupil_shape='horiz'),
   ground='#4A4536')


# ------------------------------------------------------------------------------------------------------------------------------
# R-03 MOUNTAIN KINGDOM
sp('wolf', name='Himalayan wolf', latin='Canis lupus chanco', kind='ORDINARY', region='R-03 Mountain Kingdom', cat='Mountain wildlife',
   builder=A.carnivore,
   p=dict(sh=0.72, bl=0.86, hl=0.25, neck=0.24, neck_ang=40, head_pitch=14, head_w=0.58, muzzle=0.30, muzzle_r=0.26, ear=0.13,
          ear_w=0.75, leg_r=1.0, paw=0.085, tail=0.38, tail_r0=0.045, tail_r1=0.055, tail_droop=0.9, tail_tip=0.55, belly_tuck=0.55,
          eye_r=0.014, voxel=0.004),
   coat={'*': '#A97446', 'body': '#B07A48', 'belly': '#E6DCCB', 'chest': '#DDD1BD', 'neck': '#6E5F4E', 'throat': '#BDB2A0',
         'head': '#6C5C4A', 'face': '#8C7C68', 'chin': '#C4B8A6', 'nose': '#0E0D0D', 'lid': '#1E1A18', 'leg': '#C6A07A', 'paw': '#B89A78',
         'claw': '#2B2724', 'tail': '#A8743F', 'ear': '#8A5A38', 'ear_in': '#E0D6C4'},
   coat_fn=lambda P, W, C, m: A.tail_tip(A.saddle(P, W, C, '#5E5246', 0.62, 0.80, ('body', 'neck'), 0.7), m, '#16120F', 0.22)(P, W),   # photo ref 01 (Zoo Zurich): tawny body, grizzled ruff, dark saddle, black tail tip
   fur_len={'*': 0.045, 'neck': 0.075, 'throat': 0.065, 'body': 0.05, 'belly': 0.035, 'chest': 0.05, 'head': 0.018, 'face': 0.010,
            'chin': 0.008, 'nose': 0.0, 'lid': 0.0, 'leg': 0.014, 'paw': 0.010, 'claw': 0.0, 'tail': 0.075, 'ear': 0.010, 'ear_in': 0.016},
   fur={'density': 120000, 'radius': 0.00038, 'lift': 0.6, 'droop': 0.45, 'frizz': 0.4},
   gloss=('nose',),
   eye=dict(iris='#9A7A2E', pupil_r=0.42, sclera='#3A2C1C'),
   ground='#6B6458')


def _eagle(spread):
    return dict(L=0.85, body=0.44, bw=0.24, bh=0.22, stand=0.11, neck=0.08, neck_s=0.1, neck_r=0.055, head_r=0.050, head_w=0.82,
                head_l=1.30, head_h=0.78, brow=True, body_pitch=38 if spread < 0.5 else 0,
                bill=0.062, bill_r=0.018, bill_kind='hook', eye_r=0.0135, eye_dir=(0.62, 0.78, 0.0), eye_pos=(0.55, 0.48, 0.06),
                tars=0.10, tars_r=0.011, tibia=0.08, thigh_r=0.05, feathered_legs=True, toe=0.075, talon=0.28, ws=2.05, spread=spread,
                tail=0.31, tail_w=0.19, n_tail=12, tail_fan=14 if spread < 0.5 else 46, primary=0.47, secondary=0.31, chord=0.30, n_pri=10, n_sec=17,
                pri_w=0.21, sec_w=0.36, wing_th=0.012, voxel=0.0028, head_pitch=8 if spread < 0.5 else -2, emarg=1.0)


def _eagle_col(A, v):
    """golden eagle: dark brown flight feathers with faint grey-brown bars at the base (adult), tail grey-barred brown."""
    fid, ft, kind, fu = A['fid'], A['ft'], A['kind'], A['fu']
    base = np.where(kind[:, None] == 2, K_lin('#3A2C20'), K_lin('#2E241B'))
    bars = (np.sin(ft * 34 + fid * 0.7) > 0.55) & (ft < 0.6)
    c = np.where(bars[:, None], base * 1.55, base)
    c = c * (0.85 + 0.15 * np.cos(fid * 2.3))[:, None]
    c = np.where((ft > 0.93)[:, None], c * 0.75, c)
    return np.clip(c, 0, 1)


def K_lin(h):
    h = h.lstrip('#'); c = np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4).astype(np.float32)[None, :]


_EAGLE_COAT = {'*': '#4A3626', 'body': '#43311F', 'breast': '#3E2D1E', 'belly': '#3A2A1C', 'rump': '#3A2A1C', 'neck': '#9C7440',
               'head': '#8A6232', 'throat': '#5A4128', 'bill': '#2B2A2C', 'cere': '#D9B23A', 'lid': '#6F5A2E', 'thigh': '#4A3626',
               'leg_f': '#6E5434', 'leg': '#D6B04A', 'toe': '#D6B04A', 'claw': '#121212', 'wing': '#3A2B1E', 'covert': '#5A4129'}
for _sid, _spr, _nm in (('golden_eagle', 0.0, 'Golden eagle (perched)'), ('golden_eagle_flight', 1.0, 'Golden eagle (gliding — wingspan)')):
    _p = _eagle(_spr)
    sp(_sid, name=_nm, latin='Aquila chrysaetos', kind='ORDINARY', region='R-03 Mountain Kingdom', cat='Aerial creatures',
       builder=A.bird, p=_p,
       extra=[(lambda pp: (lambda m: {'wings': A.wing_part(m, pp)}))(_p)],
       feathers=(lambda pp: (lambda m: A.feathers(m, pp, None)))(_p), feather_col=_eagle_col,
       coat=_EAGLE_COAT, fur_len={'*': 0.0}, mat={'body': 'feather', 'wings': 'feather'}, plume_scale=110,
       bare=('bill', 'cere', 'leg', 'toe', 'claw', 'lid'), gloss=('bill', 'claw'), mottle=0.18, mottle_scale=14,
       eye=dict(iris='#8A5A22', pupil_r=0.5, sclera='#5A3A16'), ground='#6B6458')

sp('red_fox', name='Red fox (Himalayan)', latin='Vulpes vulpes montana', kind='ORDINARY', region='R-03 Mountain Kingdom', cat='Mountain wildlife',
   builder=A.carnivore,
   p=dict(sh=0.40, bl=0.50, hl=0.165, neck=0.13, neck_ang=38, head_pitch=10, head_w=0.56, muzzle=0.42, muzzle_r=0.18, ear=0.085,
          ear_w=0.85, leg_r=0.95, paw=0.045, tail=0.42, tail_r0=0.035, tail_r1=0.050, tail_droop=0.55, tail_tip=0.7, belly_tuck=0.5,
          eye_r=0.0095, eye_open=(0.95, 0.5), voxel=0.003),
   coat={'*': '#A8582A', 'body': '#A65A2C', 'belly': '#E4DCCB', 'chest': '#DCD2BE', 'neck': '#A4582B', 'throat': '#EDE6D8',
         'head': '#A9602F', 'face': '#B4673A', 'chin': '#F0EADD', 'nose': '#151313', 'lid': '#1E1A18', 'leg': '#2A2220', 'paw': '#1E1918',
         'claw': '#2B2724', 'tail': '#9C5A30', 'ear': '#2C2421', 'ear_in': '#D8CDBA'},
   coat_fn=lambda P, W, C, m: A.tail_tip(A.saddle(P, W, C, '#8E4A24', 0.30, 0.44, ('body', 'neck')), m, '#EFEAE0', 0.18)(P, W),
   fur_len={'*': 0.035, 'neck': 0.05, 'throat': 0.045, 'body': 0.04, 'belly': 0.03, 'chest': 0.04, 'head': 0.012, 'face': 0.007,
            'chin': 0.010, 'nose': 0.0, 'lid': 0.0, 'leg': 0.010, 'paw': 0.008, 'claw': 0.0, 'tail': 0.07, 'ear': 0.006, 'ear_in': 0.014},
   fur={'density': 200000, 'radius': 0.00026, 'lift': 0.6, 'droop': 0.4, 'frizz': 0.35},
   gloss=('nose',), eye=dict(iris='#B07A22', pupil_r=0.5, pupil_shape='vert', sclera='#3A2C1C'), ground='#6B6458')
