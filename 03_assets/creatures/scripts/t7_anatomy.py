"""t7_anatomy — body-plan builders (real proportions, metres) → t7sdf Parts.

Each builder takes a parameter dict (species file) and returns
    parts : {name: (Part, opts)}   body / ears / antlers / horns ... (opts: quads, fur, material kind)
    marks : dict of named world points (eyes, nose, head frame, joint positions) used for eyes, fur combing, rig later
Joint positions are anatomical (shoulder, elbow, carpus, fetlock …) so the rig in milestone 2 can be built on the same marks.
"""
import numpy as np
import t7sdf as S

F = np.float32


class Frame:
    """local frame: origin o, axes from look_mat(fwd, up). to(p_local) → world."""

    def __init__(self, o, fwd, up=(0, 0, 1)):
        self.o = np.asarray(o, F); self.R = S.look_mat(fwd, up)

    def to(self, p):
        return (self.o + self.R @ np.asarray(p, F)).astype(F)

    def mir(self, p):          # mirrored lateral
        q = np.asarray(p, F).copy(); q[1] = -q[1]; return self.to(q)


def V(*a):
    return np.asarray(a, F)


def trace(part, start, d, maxd=1.0, eps=2e-4):
    """sphere-trace the part's current SDF from start along d → surface point."""
    p = np.asarray(start, F).copy(); d = S._n(d); t = 0.0
    for _ in range(200):
        dist = float(part.field(p[None, :])[0])
        if dist < eps:
            return p
        p = p + d * dist * 0.9; t += dist * 0.9
        if t > maxd:
            break
    return p


def place_eye(part, eye_guess, edir, er, hl, open_=(0.95, 0.62), lid=1.0):
    """eye on the real head surface: trace along -edir, sink the ball 55 % (real eyes show ~40 % between the lids), lids around it."""
    s = trace(part, eye_guess + edir * hl * 0.6, -edir, hl * 1.5)
    c = s - edir * er * 0.55
    R = S.look_mat(edir, (0, 0, 1))
    part.ell(c + edir * er * 0.20, V(er * 0.62, er * 1.32 * lid, er * 1.08 * lid), R, zone='lid', k=er * 0.35, mirror=True)        # lids
    part.ell(c + edir * er * 0.75, V(er * 0.62, er * open_[0], er * open_[1]), R, zone='lid', k=er * 0.18, sub=True, mirror=True)  # almond opening
    part.ell(c, V(er * 0.99, er * 0.99, er * 0.99), R, zone='lid', k=er * 0.1, sub=True, mirror=True)                              # ball seat
    return c


def leg(part, pts, radii, zone='leg', k=0.03, mirror=True, foot_zone=None, foot_n=1):
    part.chain(pts[:-foot_n] if foot_n else pts, radii[:-foot_n] if foot_n else radii, zone, k, mirror=mirror)
    if foot_n:
        part.chain(pts[-foot_n - 1:], radii[-foot_n - 1:], foot_zone or zone, k * 0.5, mirror=mirror)


# ==============================================================================================================================
def ungulate(p):
    """deer / sheep / goat / antelope.  p: sh (shoulder height), bl (trunk length withers-front → buttock), cd (chest depth),
    cw (chest width), hh (hip height), neck (length), neck_ang (deg above horizontal), hl (head length), head_pitch (deg down),
    leg_r (scale), tail, ear (length), ear_w, muzzle (0..1 length share), stocky (0..1)."""
    sh, L = p['sh'], p['bl']
    cd = p.get('cd', 0.48 * sh); cw = p.get('cw', 0.50 * cd); hh = p.get('hh', sh * 0.98)
    lr = p.get('leg_r', 1.0) * sh
    b = S.Part('body', voxel=p.get('voxel', 0.006)); m = {}
    xf, xr = 0.5 * L, -0.5 * L                      # chest front / buttock
    # ---------------- trunk
    b.ell(V(0.22 * L, 0, sh - 0.50 * cd), V(0.28 * L, cw * 0.50, cd * 0.50), zone='body', k=0.08)               # rib cage
    b.ell(V(0.06 * L, 0, sh - 0.48 * cd), V(0.26 * L, cw * 0.52, cd * 0.42), zone='body', k=0.10)              # belly
    b.ell(V(0.02 * L, 0, sh - 0.95 * cd), V(0.22 * L, cw * 0.36, cd * 0.10), zone='belly', k=0.10)              # underline
    b.ell(V(-0.28 * L, 0, hh - 0.32 * cd), V(0.21 * L, cw * 0.38, cd * 0.32), zone='body', k=0.09)              # haunch
    b.ell(V(-0.20 * L, cw * 0.30, hh - 0.14 * cd), V(0.05 * L, cw * 0.10, cd * 0.07), zone='body', k=0.05, mirror=True)  # hip point (tuber coxae)
    b.ell(V(-0.25 * L, cw * 0.25, 0.70 * sh), V(0.13 * L, cw * 0.17, 0.24 * sh), S.rot_mat(0, -22, 0), zone='body', k=0.07, mirror=True)  # thigh muscles
    b.ell(V(0.30 * L, 0, sh - 0.06 * sh), V(0.16 * L, cw * 0.22, cd * 0.16), zone='body', k=0.08)               # withers
    b.rcone(V(0.30 * L, 0, sh - 0.12 * cd), V(-0.36 * L, 0, hh - 0.12 * cd), 0.12 * cd, 0.13 * cd, zone='body', k=0.10)  # topline
    b.ell(V(0.40 * L, 0, sh - 0.62 * cd), V(0.10 * L, cw * 0.36, cd * 0.30), zone='chest', k=0.07)              # brisket
    b.ell(V(0.33 * L, cw * 0.36, sh - 0.33 * cd), V(0.13 * L, cw * 0.12, cd * 0.30), S.rot_mat(0, -25, 0), zone='body', k=0.06, mirror=True)  # scapula
    b.ell(V(-0.40 * L, 0, hh - 0.50 * cd), V(0.10 * L, cw * 0.30, cd * 0.30), zone='rump', k=0.07)              # rump / buttock
    # ---------------- neck + head
    nb = V(0.40 * L, 0, sh - 0.36 * cd)
    na = np.radians(p.get('neck_ang', 48))
    nl = p.get('neck', 0.55 * sh)
    hb = nb + V(np.cos(na) * nl, 0, np.sin(na) * nl)
    b.rcone(nb, hb, p.get('neck_r0', 0.34 * cd), p.get('neck_r1', 0.17 * cd), zone='neck', k=0.08)
    b.rcone(nb + V(0.02, 0, -0.12 * cd), hb + V(0.02, 0, -0.06 * cd), 0.22 * cd, 0.11 * cd, zone='throat', k=0.07)
    hp = np.radians(p.get('head_pitch', 38)); hl = p['hl']
    fwd = V(np.cos(hp), 0, -np.sin(hp))
    H = Frame(hb + V(0.02 * hl, 0, 0.06 * hl), fwd)
    hw = p.get('head_w', 0.40)                                                      # head width / length
    b.ell(H.to((0.20 * hl, 0, 0.04 * hl)), V(0.30 * hl, hw * 0.5 * hl, 0.26 * hl), H.R, zone='head', k=0.05)  # cranium
    b.ell(H.to((0.02 * hl, 0, -0.10 * hl)), V(0.22 * hl, hw * 0.42 * hl, 0.22 * hl), H.R, zone='head', k=0.06)  # jowl / masseter
    mz = p.get('muzzle', 0.62)
    b.rcone(H.to((0.30 * hl, 0, 0.0)), H.to((0.26 * hl + mz * hl, 0, -0.03 * hl)), 0.17 * hl, 0.075 * hl, zone='face', k=0.06)
    b.ell(H.to((0.62 * hl, 0, -0.02 * hl)), V(0.30 * hl, hw * 0.28 * hl, 0.13 * hl), H.R, zone='face', k=0.05)  # nasal bridge
    tip = 0.30 * hl + mz * hl
    b.ell(H.to((tip - 0.02 * hl, 0, -0.035 * hl)), V(0.055 * hl, 0.07 * hl, 0.065 * hl), H.R, zone='nose', k=0.02)  # rhinarium
    b.ell(H.to((0.62 * hl, 0, -0.15 * hl)), V(0.28 * hl, hw * 0.26 * hl, 0.07 * hl), H.R, zone='chin', k=0.04)  # lower jaw
    b.ell(H.to((tip + 0.015 * hl, 0.045 * hl, -0.03 * hl)), V(0.03 * hl, 0.018 * hl, 0.035 * hl), H.R, zone='nose', k=0.01, sub=True, mirror=True)  # nostrils
    b.box(H.to((tip - 0.06 * hl, 0, -0.10 * hl)), V(0.10 * hl, 0.07 * hl, 0.0025), H.R, rr=0.0015, zone='face', k=0.004, sub=True)  # mouth line
    eye = H.to((0.33 * hl, hw * 0.40 * hl, 0.10 * hl)); er = p.get('eye_r', 0.050 * hl)
    edir = S._n(H.R @ S._n((0.30, 1.0, 0.15)))
    eye = place_eye(b, eye, edir, er, hl, open_=(0.95, 0.66), lid=1.0)
    eye[1] = abs(eye[1])
    if p.get('preorbital'):
        b.ell(H.to((0.43 * hl, hw * 0.43 * hl, 0.05 * hl)), V(0.06 * hl, 0.02 * hl, 0.03 * hl), H.R, zone='gland', k=0.01, sub=True, mirror=True)
    m.update(head=H, hl=hl, eye=eye, eye_r=er, eye_dir=edir, nose=H.to((tip, 0, -0.03 * hl)), neck_base=nb, head_base=hb)
    # ---------------- legs (anatomical joints)
    yf = cw * 0.30; yh = cw * 0.30
    fl = [V(0.34 * L, yf, sh - 0.42 * cd), V(0.40 * L, yf, sh - 0.70 * cd), V(0.26 * L, yf * 0.95, sh - 1.02 * cd),
          V(0.28 * L, yf * 0.9, 0.29 * sh), V(0.29 * L, yf * 0.9, 0.085 * sh), V(0.32 * L, yf * 0.9, 0.03 * sh)]
    fr = [0.11 * lr, 0.085 * lr, 0.052 * lr, 0.030 * lr, 0.024 * lr, 0.020 * lr]
    b.chain(fl[:3], fr[:3], 'body', 0.06, mirror=True)
    b.chain(fl[2:5], fr[2:5], 'leg', 0.025, mirror=True)
    b.rcone(fl[1] + V(-0.06 * L, 0, -0.02), fl[2] + V(-0.01, 0, 0.02), 0.075 * lr, 0.06 * lr, 'body', 0.05, mirror=True)   # triceps → elbow
    b.rcone(fl[2] + V(0.01, 0, -0.02), fl[3] + V(0, 0, 0.06 * sh), 0.050 * lr, 0.030 * lr, 'leg', 0.03, mirror=True)        # forearm muscle
    b.rcone(fl[3], fl[3] + V(-0.01, 0, 0.02), fr[3] * 1.22, fr[3] * 1.1, 'leg', 0.02, mirror=True)               # carpus bulge
    b.rcone(fl[4], fl[4] + V(0, 0, 0.012), fr[4] * 1.35, fr[4] * 1.2, 'leg', 0.015, mirror=True)                 # fetlock
    hl_ = [V(-0.30 * L, yh, hh - 0.30 * cd), V(-0.14 * L, yh * 1.05, 0.56 * sh), V(-0.35 * L, yh * 0.9, 0.36 * sh),
           V(-0.335 * L, yh * 0.9, 0.085 * sh), V(-0.31 * L, yh * 0.9, 0.03 * sh)]
    hr = [0.17 * lr, 0.080 * lr, 0.034 * lr, 0.024 * lr, 0.020 * lr]
    b.chain(hl_[:2], hr[:2], 'body', 0.07, mirror=True)
    b.rcone(V(-0.47 * L, yh * 0.8, hh - 0.45 * cd), hl_[2] + V(0.0, 0, 0.10 * sh), 0.10 * lr, 0.045 * lr, 'body', 0.06, mirror=True)  # hamstrings (buttock → hock)
    b.rcone(hl_[1], hl_[2], 0.070 * lr, 0.036 * lr, 'leg', 0.03, mirror=True)                                    # gaskin
    b.ell(hl_[1] * 0.55 + hl_[2] * 0.45 + V(-0.03 * lr, 0, 0.02), V(0.05 * lr, 0.035 * lr, 0.10 * lr), S.rot_mat(0, -40, 0), zone='leg', k=0.03, mirror=True)  # gastrocnemius
    b.rcone(hl_[2] + V(-0.04 * lr, 0, 0.03 * lr), hl_[2], 0.022 * lr, 0.03 * lr, 'leg', 0.02, mirror=True)       # calcaneus (point of hock)
    b.chain(hl_[2:4], hr[2:4], 'leg', 0.02, mirror=True)
    b.rcone(hl_[3], hl_[3] + V(0, 0, 0.012), hr[3] * 1.35, hr[3] * 1.2, 'leg', 0.015, mirror=True)
    # cloven hooves (two claws + dew claws)
    for base in (fl, hl_):
        f = base[-2]
        b.rcone(f, V(f[0] + 0.012 * lr, f[1], 0.45 * f[2]), 0.024 * lr, 0.021 * lr, 'leg', 0.012, mirror=True)  # pastern
        for s in (-1, 1):
            b.rcone(V(f[0] + 0.006 * lr, f[1] + s * 0.010 * lr, 0.40 * f[2]), V(f[0] + 0.048 * lr, f[1] + s * 0.012 * lr, 0.011 * lr),
                    0.018 * lr, 0.011 * lr, 'hoof', 0.006, mirror=True)
        b.ell(f + V(-0.028 * lr, 0, -0.01 * lr), V(0.009 * lr, 0.016 * lr, 0.008 * lr), zone='hoof', k=0.004, mirror=True)  # dew claws
    m.update(front_leg=fl, hind_leg=hl_)
    # ---------------- tail
    tl = p.get('tail', 0.14 * sh)
    t0 = V(-0.47 * L, 0, hh - 0.10 * cd)
    b.rcone(t0, t0 + V(-0.25 * tl, 0, -0.95 * tl), p.get('tail_r', 0.028 * sh), 0.016 * sh, 'tail', 0.025)
    m.update(tail=(t0, t0 + V(-0.25 * tl, 0, -0.95 * tl)))
    parts = {'body': b}
    # ---------------- ears (separate thin part)
    el, ew = p.get('ear', 0.38 * hl), p.get('ear_w', 0.45)
    e = S.Part('ears', voxel=0.0025)
    ebase = H.to(p.get('ear_pos', (-0.04 * hl, hw * 0.44 * hl, 0.16 * hl)))
    ed = S._n(H.R @ S._n(p.get('ear_dir', (-0.55, 1.0, 0.30))))
    ER = S.look_mat(ed, H.R @ V(0.3, 0, 1))
    e.ell(ebase + ed * el * 0.5, V(el * 0.5, el * ew * 0.5, el * 0.06), ER, zone='ear', k=0.004, mirror=True)
    e.ell(ebase + ed * el * 0.52 + ER @ V(0, 0, el * 0.05), V(el * 0.44, el * ew * 0.42, el * 0.05), ER, zone='ear_in', k=0.004, sub=True, mirror=True)
    e.rcone(ebase - ed * 0.02, ebase + ed * el * 0.2, el * 0.09, el * 0.12, zone='ear', k=0.01, mirror=True)       # ear base
    parts['ears'] = e
    m['ear_base'] = ebase
    return parts, m


def _path(p0, dirs, length, n=10):
    """integrate a smoothly turning direction list (world) → n+1 points."""
    pts = [np.asarray(p0, F)]
    for i in range(n):
        t = (i + 0.5) / n; k = t * (len(dirs) - 1); j = min(int(k), len(dirs) - 2); f = k - j
        d = S._n(np.asarray(dirs[j], F) * (1 - f) + np.asarray(dirs[j + 1], F) * f)
        pts.append(pts[-1] + d * length / n)
    return pts


def antlers_sambar(m, beam=0.62, r0=0.028):
    """rusine antler (3 points per side, real sambar shape): brow tine forward-up from just above the burr, main beam up-back-out,
    terminal fork (inner tine up-forward, beam tip back-out). World-frame directions (+X = forward)."""
    H = m['head']; hl = m['hl']
    a = S.Part('antlers', voxel=0.003)
    base = H.to((0.04 * hl, 0.17 * hl, 0.27 * hl))
    pts = _path(base, [(-0.10, 0.60, 1.0), (-0.45, 0.62, 1.0), (-0.35, 0.35, 1.0), (-0.05, 0.10, 1.0)], beam, 10)
    rad = [r0 * (1 - 0.5 * i / 10) for i in range(11)]
    a.chain(pts, rad, 'antler', 0.004, mirror=True)
    a.rcone(base - V(0, 0, 0.012), base + V(0, 0, 0.012), r0 * 1.4, r0 * 1.3, 'burr', 0.004, mirror=True)       # burr / coronet
    a.rcone(base - V(0, 0, 0.05), base, r0 * 1.0, r0 * 1.1, 'burr', 0.006, mirror=True)                            # pedicle
    p0 = pts[1]
    br = _path(p0, [(1.0, 0.25, 0.45), (0.7, 0.15, 0.9)], beam * 0.42, 6)
    a.chain(br, [rad[1] * 0.85 * (1 - 0.75 * i / 6) for i in range(7)], 'antler', 0.006, mirror=True)           # brow tine
    p1 = pts[8]
    it = _path(p1, [(0.35, -0.10, 1.0), (0.15, -0.15, 1.0)], beam * 0.30, 5)
    a.chain(it, [rad[8] * 0.9 * (1 - 0.75 * i / 5) for i in range(6)], 'antler', 0.005, mirror=True)           # inner tine
    a.rcone(pts[-2], pts[-1] + (pts[-1] - pts[-2]) * 1.2, rad[-2], rad[-1] * 0.25, 'antler', 0.004, mirror=True)
    return a


# ==============================================================================================================================
def paw(part, heel, toe_dir, size, claws=0.4, zone='paw', mirror=True, toes=4, splay=1.0, web=False):
    """digitigrade / plantigrade paw: main pad + toes + claws. heel = back of the pad on the ground plane."""
    d = S._n(V(toe_dir[0], toe_dir[1], 0)); side = V(-d[1], d[0], 0)
    c = heel + d * size * 0.45 + V(0, 0, size * 0.18)
    part.ell(c, V(size * 0.50, size * 0.42, size * 0.20), S.look_mat(d), zone=zone, k=size * 0.25, mirror=mirror)
    for i in range(toes):
        t = (i - (toes - 1) / 2) / max((toes - 1) / 2, 1)
        tp = heel + d * size * (0.95 - 0.12 * abs(t)) + side * t * size * 0.36 * splay + V(0, 0, size * 0.13)
        part.ell(tp, V(size * 0.17, size * 0.13, size * 0.14), S.look_mat(d), zone=zone, k=size * 0.10, mirror=mirror)
        if claws:
            part.rcone(tp + d * size * 0.10 + V(0, 0, size * 0.04), tp + d * size * (0.16 + 0.22 * claws) - V(0, 0, size * 0.08),
                       size * 0.045, size * 0.012, 'claw', size * 0.02, mirror=mirror)
    if web:
        part.ell(heel + d * size * 0.85 + V(0, 0, size * 0.08), V(size * 0.25, size * 0.55, size * 0.035), S.look_mat(d), zone=zone, k=size * 0.08, mirror=mirror)


def carnivore(p):
    """canids, felids, bears, mustelids, red panda.  p: sh, bl, cd, cw, hh, neck, neck_ang, hl, head_pitch, head_w, muzzle (share of hl),
    muzzle_r, ear (length), ear_w, ear_round, leg_r, paw, planti (bear / red panda sole), tail, tail_r0, tail_r1, tail_droop, belly_tuck."""
    sh, L = p['sh'], p['bl']
    cd = p.get('cd', 0.44 * sh); cw = p.get('cw', 0.62 * cd); hh = p.get('hh', 0.97 * sh)
    lr = p.get('leg_r', 1.0) * sh
    b = S.Part('body', voxel=p.get('voxel', 0.005)); m = {}
    tuck = p.get('belly_tuck', 0.35)
    b.ell(V(0.20 * L, 0, sh - 0.50 * cd), V(0.30 * L, cw * 0.50, cd * 0.50), zone='body', k=0.25 * cd)                 # rib cage
    b.ell(V(-0.08 * L, 0, sh - (0.45 + 0.05 * (1 - tuck)) * cd), V(0.26 * L, cw * 0.46, cd * (0.48 - 0.16 * tuck)), zone='body', k=0.25 * cd)  # loin / belly
    b.ell(V(-0.32 * L, 0, hh - 0.36 * cd), V(0.20 * L, cw * 0.44, cd * 0.38), zone='body', k=0.22 * cd)               # haunch
    b.rcone(V(0.30 * L, 0, sh - 0.14 * cd), V(-0.40 * L, 0, hh - 0.14 * cd), 0.14 * cd, 0.14 * cd, zone='body', k=0.2 * cd)  # back
    b.ell(V(0.40 * L, 0, sh - 0.58 * cd), V(0.11 * L, cw * 0.38, cd * 0.32), zone='chest', k=0.2 * cd)                 # chest / brisket
    b.ell(V(0.02 * L, 0, sh - 0.92 * cd), V(0.26 * L, cw * 0.34, cd * 0.10), zone='belly', k=0.2 * cd)
    b.ell(V(0.33 * L, cw * 0.30, sh - 0.35 * cd), V(0.12 * L, cw * 0.13, cd * 0.32), S.rot_mat(0, -25, 0), zone='body', k=0.18 * cd, mirror=True)  # scapula
    b.ell(V(-0.30 * L, cw * 0.26, hh - 0.62 * cd), V(0.14 * L, cw * 0.18, cd * 0.42), S.rot_mat(0, -15, 0), zone='body', k=0.15 * cd, mirror=True)  # thigh
    # neck + head
    nb = V(0.40 * L, 0, sh - 0.34 * cd)
    na = np.radians(p.get('neck_ang', 35)); nl = p.get('neck', 0.40 * sh)
    hb = nb + V(np.cos(na) * nl, 0, np.sin(na) * nl)
    b.rcone(nb, hb, p.get('neck_r0', 0.40 * cd), p.get('neck_r1', 0.27 * cd), zone='neck', k=0.25 * cd)
    b.rcone(nb + V(0.0, 0, -0.15 * cd), hb + V(0.0, 0, -0.10 * cd), 0.26 * cd, 0.18 * cd, zone='throat', k=0.2 * cd)
    hl = p['hl']; hp = np.radians(p.get('head_pitch', 12)); hw = p.get('head_w', 0.62)
    H = Frame(hb + V(0.05 * hl, 0, 0.02 * hl), V(np.cos(hp), 0, -np.sin(hp)))
    mz = p.get('muzzle', 0.42); mr = p.get('muzzle_r', 0.20)
    b.ell(H.to((0.20 * hl, 0, 0.06 * hl)), V(0.34 * hl, hw * 0.44 * hl, 0.30 * hl), H.R, zone='head', k=0.08 * hl)       # cranium
    b.ell(H.to((0.26 * hl, 0, -0.06 * hl)), V(0.18 * hl, hw * 0.52 * hl, 0.20 * hl), H.R, zone='head', k=0.10 * hl)      # zygomatic / cheeks
    b.ell(H.to((0.16 * hl, 0, 0.26 * hl)), V(0.24 * hl, hw * 0.30 * hl, 0.08 * hl), H.R, zone='head', k=0.08 * hl)      # sagittal / forehead
    m0 = 0.52 * hl; m1 = m0 + mz * hl
    b.rcone(H.to((m0 - 0.08 * hl, 0, -0.02 * hl)), H.to((m1 - 0.04 * hl, 0, -0.03 * hl)), mr * hl * 1.15, mr * hl * 0.70, zone='face', k=0.08 * hl)  # muzzle
    b.ell(H.to(((m0 + m1) / 2, 0, -0.11 * hl)), V(mz * hl * 0.48, hw * 0.24 * hl, 0.09 * hl), H.R, zone='chin', k=0.06 * hl)  # lower jaw / lips
    b.ell(H.to((m1 - 0.01 * hl, 0, 0.01 * hl)), V(0.075 * hl, 0.10 * hl * mr / 0.2, 0.07 * hl), H.R, zone='nose', k=0.02 * hl)   # nose leather
    b.ell(H.to((m1 + 0.015 * hl, 0.035 * hl, -0.005 * hl)), V(0.025 * hl, 0.018 * hl, 0.02 * hl), H.R, zone='nose', k=0.01 * hl, sub=True, mirror=True)
    eye = H.to(p.get('eye_pos', (0.46 * hl, hw * 0.30 * hl, 0.10 * hl))); er = p.get('eye_r', 0.065 * hl)
    edir = S._n(H.R @ S._n(p.get('eye_dir', (0.75, 0.62, 0.12))))
    eye = place_eye(b, eye, edir, er, hl, open_=p.get('eye_open', (0.95, 0.62)))
    m.update(head=H, hl=hl, eye=eye, eye_r=er, eye_dir=edir, nose=H.to((m1, 0, 0)), head_base=hb, neck_base=nb)
    # legs
    yf, yh = cw * 0.34, cw * 0.32
    ps = p.get('paw', 0.11 * sh)
    planti = p.get('planti', False)
    fl = [V(0.34 * L, yf, sh - 0.45 * cd), V(0.40 * L, yf, sh - 0.72 * cd), V(0.28 * L, yf * 0.95, sh - 1.05 * cd),
          V(0.31 * L, yf * 0.9, (0.10 if planti else 0.17) * sh), V(0.33 * L, yf * 0.9, ps * 0.32)]
    fr = [0.12 * lr, 0.085 * lr, 0.050 * lr, 0.034 * lr, 0.032 * lr]
    b.chain(fl[:3], fr[:3], 'body', 0.06 * sh, mirror=True)
    b.chain(fl[2:], fr[2:], 'leg', 0.04 * sh, mirror=True)
    b.rcone(fl[2] + V(0.0, 0, -0.02), fl[3] + V(0, 0, 0.12 * sh), 0.050 * lr, 0.034 * lr, 'leg', 0.03 * sh, mirror=True)   # forearm muscles
    paw(b, fl[4] - V(0.30 * ps, 0, fl[4][2]), (1, 0), ps, p.get('claws', 0.35), toes=p.get('toes', 4), web=p.get('web', False))
    if planti:
        hk = V(-0.30 * L, yh * 0.9, 0.08 * sh); toe = hk + V(0.10 * sh + ps * 0.6, 0, -0.05 * sh)
    else:
        hk = V(-0.40 * L, yh * 0.9, 0.27 * sh); toe = V(-0.33 * L, yh * 0.9, ps * 0.32)
    hl_ = [V(-0.30 * L, yh, hh - 0.32 * cd), V(-0.14 * L, yh * 1.05, 0.55 * sh if not planti else 0.42 * sh), hk, toe]
    hr = [0.16 * lr, 0.065 * lr, 0.036 * lr, 0.032 * lr]
    b.chain(hl_[:2], hr[:2], 'body', 0.07 * sh, mirror=True)
    b.rcone(V(-0.45 * L, yh * 0.8, hh - 0.45 * cd), hk + V(0.0, 0, 0.10 * sh), 0.09 * lr, 0.040 * lr, 'body', 0.06 * sh, mirror=True)  # hamstrings
    b.chain(hl_[1:], hr[1:], 'leg', 0.04 * sh, mirror=True)
    paw(b, (toe - V(0.30 * ps, 0, toe[2])) if not planti else V(hk[0] - 0.06 * sh, hk[1], 0), (1, 0),
        ps * (1.0 if not planti else 1.35), p.get('claws', 0.35), toes=p.get('toes', 4), web=p.get('web', False))
    if planti:   # sole: heel → toes on the ground
        b.ell(V(hk[0] + 0.05 * sh, hk[1], 0.035 * sh), V(0.12 * sh, 0.05 * sh, 0.04 * sh), zone='leg', k=0.03 * sh, mirror=True)
    m.update(front_leg=fl, hind_leg=hl_)
    # tail
    tl = p.get('tail', 0.5 * sh); r0, r1 = p.get('tail_r0', 0.06 * sh), p.get('tail_r1', 0.04 * sh)
    t0 = V(-0.48 * L, 0, hh - 0.16 * cd)
    dr = p.get('tail_droop', 0.8); curl = p.get('tail_curl', 0.15)
    pts = [t0]
    for i in range(1, 7):
        t = i / 6
        pts.append(t0 + V(-tl * (0.35 + 0.65 * (1 - dr)) * t - curl * tl * t ** 3 * 0, 0, -tl * dr * (t ** 0.9) + curl * tl * t ** 2.5))
    rad = [r0 + (r1 - r0) * (i / 6) ** 0.8 for i in range(7)]
    rad[-1] = r1 * p.get('tail_tip', 0.6)
    b.chain(pts, rad, 'tail', 0.03 * sh)
    m['tail'] = pts
    parts = {'body': b}
    # ears
    el, ew = p.get('ear', 0.30 * hl), p.get('ear_w', 0.75)
    e = S.Part('ears', voxel=min(0.003, el * 0.05))
    ebase = H.to(p.get('ear_pos', (0.06 * hl, hw * 0.33 * hl, 0.26 * hl)))
    ed = S._n(H.R @ S._n(p.get('ear_dir', (-0.05, 0.45, 1.0))))
    ER = S.look_mat(ed, H.R @ V(1, 0, 0))
    if p.get('ear_round'):
        e.ell(ebase + ed * el * 0.45, V(el * 0.5, el * ew * 0.5, el * 0.10), ER, zone='ear', k=el * 0.05, mirror=True)
        e.ell(ebase + ed * el * 0.48 + ER @ V(0, 0, el * 0.10), V(el * 0.40, el * ew * 0.40, el * 0.09), ER, zone='ear_in', k=el * 0.04, sub=True, mirror=True)
    else:   # triangular: stack of shrinking ellipsoids toward the tip
        for i in range(5):
            t = i / 4
            e.ell(ebase + ed * el * (0.12 + 0.70 * t), V(el * 0.20, el * ew * 0.5 * (1 - 0.8 * t), el * 0.08 * (1 - 0.5 * t)), ER, zone='ear', k=el * 0.12, mirror=True)
        e.ell(ebase + ed * el * 0.42 + ER @ V(0, 0, el * 0.09), V(el * 0.42, el * ew * 0.36, el * 0.08), ER, zone='ear_in', k=el * 0.04, sub=True, mirror=True)
    e.rcone(ebase - ed * el * 0.15, ebase + ed * el * 0.15, el * 0.16, el * 0.20, zone='ear', k=el * 0.06, mirror=True)
    parts['ears'] = e
    return parts, m


# ==============================================================================================================================
# BIRDS — body / neck / head / beak / legs as SDF; flight + tail feathers as real blade meshes (see feathers()).
def bird(p):
    """p: L (bill-tip to tail-tip, field-guide length), body (body length), bw (body width), bh (body height), stand (hip height above
    ground when perched), neck (length), neck_s (S-curve 0..1), neck_r, head_r, bill (length), bill_r (base radius), bill_kind
    ('hook' raptor, 'dagger' heron, 'flat' duck, 'casque' hornbill, 'short' pheasant / owl), tars (tarsus length), tars_r,
    toe (length), feathered_legs, ws (wingspan), spread (0 folded … 1 full glide), tail (length), tail_w, facial_disc (owl)."""
    bL, bw, bh = p['body'], p['bw'], p['bh']
    st = p['stand']; spread = p.get('spread', 0.0)
    b = S.Part('body', voxel=p.get('voxel', 0.003)); m = {}
    pitch = p.get('body_pitch', 25 if spread < 0.5 else 0)        # perched birds hold the body tilted up
    R = S.rot_mat(0, -pitch, 0)
    c = V(0, 0, st + bh * 0.5)
    B = Frame(c, R @ V(1, 0, 0), R @ V(0, 0, 1))
    b.ell(B.to((0.05 * bL, 0, 0)), V(bL * 0.48, bw * 0.5, bh * 0.5), B.R, zone='body', k=0.25 * bh)                   # trunk
    b.ell(B.to((0.22 * bL, 0, -0.05 * bh)), V(bL * 0.30, bw * 0.48, bh * 0.48), B.R, zone='breast', k=0.25 * bh)     # breast / keel muscles
    b.ell(B.to((-0.30 * bL, 0, -0.02 * bh)), V(bL * 0.28, bw * 0.36, bh * 0.32), B.R, zone='belly', k=0.25 * bh)     # vent
    b.ell(B.to((-0.40 * bL, 0, 0.12 * bh)), V(bL * 0.22, bw * 0.24, bh * 0.14), B.R, zone='rump', k=0.2 * bh)       # rump / uropygium
    # neck (S-curve) + head
    nl = p.get('neck', 0.25 * bL); ns = p.get('neck_s', 0.2); nr = p.get('neck_r', 0.22 * bw)
    n0 = B.to((0.40 * bL, 0, 0.18 * bh))
    up = S._n(B.R @ V(0.35, 0, 1.0)) if spread < 0.5 else S._n(V(1, 0, 0.25))
    pts = [n0]
    for i in range(1, 7):
        t = i / 6
        bend = np.sin(t * np.pi) * ns * nl * 0.5
        pts.append(n0 + up * nl * t + V(-bend if spread < 0.5 else 0, 0, 0) + V(ns * nl * 0.35 * t ** 2, 0, 0))
    rads = [nr * (1.25 - 0.3 * i / 6) for i in range(7)]
    b.chain(pts, rads, 'neck', 0.4 * nr)
    hr = p['head_r']
    hc = pts[-1] + V(0.25 * hr, 0, 0.35 * hr)
    hp = np.radians(p.get('head_pitch', 0))
    H = Frame(hc, V(np.cos(hp), 0, -np.sin(hp)))
    b.ell(H.to((0, 0, 0)), V(hr * p.get('head_l', 1.05), hr * p.get('head_w', 0.9), hr * p.get('head_h', 0.95)), H.R, zone='head', k=0.3 * hr)
    if p.get('brow'):     # raptor supraorbital ridge (the 'fierce' brow)
        b.ell(H.to((0.52 * hr, 0.36 * hr, 0.30 * hr)), V(hr * 0.48, hr * 0.26, hr * 0.15), H.R @ S.rot_mat(14, 0, -14), zone='head', k=0.10 * hr, mirror=True)
    b.ell(H.to((0.35 * hr, 0, -0.35 * hr)), V(hr * 0.6, hr * 0.62, hr * 0.5), H.R, zone='throat', k=0.3 * hr)
    if p.get('facial_disc'):
        for s_ in (1,):
            b.ell(H.to((0.62 * hr, 0.38 * hr, 0.0)), V(hr * 0.30, hr * 0.48, hr * 0.62), H.R @ S.rot_mat(-30, 0, 0), zone='disc', k=0.15 * hr, sub=True, mirror=True)
        b.ell(H.to((0.50 * hr, 0, 0)), V(hr * 0.45, hr * 1.02, hr * 0.92), H.R, zone='disc_rim', k=0.2 * hr)
    # bill
    bl_, br_ = p['bill'], p['bill_r']; kind = p.get('bill_kind', 'short')
    b0 = H.to((0.80 * hr, 0, -0.08 * hr))
    if kind == 'hook':
        bp = [b0, H.to((0.8 * hr + 0.45 * bl_, 0, -0.02 * hr)), H.to((0.8 * hr + 0.85 * bl_, 0, -0.15 * hr)), H.to((0.8 * hr + 0.95 * bl_, 0, -0.45 * hr - 0.2 * bl_))]
        b.chain(bp, [br_, br_ * 0.75, br_ * 0.45, br_ * 0.12], 'bill', 0.3 * br_)
        b.ell(H.to((0.82 * hr, 0, 0.02 * hr)), V(br_ * 0.6, br_ * 1.05, br_ * 0.75), H.R, zone='cere', k=0.3 * br_)       # cere
    elif kind == 'dagger':
        b.rcone(b0, H.to((0.8 * hr + bl_, 0, -0.08 * hr)), br_, br_ * 0.08, 'bill', 0.3 * br_)
    elif kind == 'flat':
        b.ell(H.to((0.8 * hr + 0.45 * bl_, 0, -0.12 * hr)), V(bl_ * 0.55, br_ * 1.25, br_ * 0.55), H.R, zone='bill', k=0.4 * br_)
        b.ell(H.to((0.8 * hr + 0.95 * bl_, 0, -0.14 * hr)), V(bl_ * 0.10, br_ * 0.9, br_ * 0.45), H.R, zone='nail', k=0.3 * br_)
    elif kind == 'casque':
        bp = [b0, H.to((0.8 * hr + 0.5 * bl_, 0, -0.10 * hr)), H.to((0.8 * hr + bl_, 0, -0.45 * hr))]
        b.chain(bp, [br_, br_ * 0.6, br_ * 0.12], 'bill', 0.3 * br_)
        cq = [H.to((0.55 * hr, 0, 0.55 * hr)), H.to((0.8 * hr + 0.45 * bl_, 0, 0.35 * hr)), H.to((0.8 * hr + 0.62 * bl_, 0, 0.12 * hr))]
        b.chain(cq, [br_ * 0.75, br_ * 0.62, br_ * 0.3], 'casque', 0.4 * br_)
    else:
        bp = [b0, H.to((0.8 * hr + 0.7 * bl_, 0, -0.12 * hr)), H.to((0.8 * hr + bl_, 0, -0.30 * hr))]
        b.chain(bp, [br_, br_ * 0.55, br_ * 0.12], 'bill', 0.3 * br_)
    b.box(H.to((0.8 * hr + 0.4 * bl_, 0, -0.10 * hr)), V(bl_ * 0.5, br_ * 1.4, max(br_ * 0.04, 0.0006)), H.R, rr=0.0004, zone='bill', k=0.001, sub=True)  # gape
    er = p.get('eye_r', 0.28 * hr)
    edir = S._n(H.R @ S._n(p.get('eye_dir', (0.25, 1.0, 0.1))))
    eye = place_eye(b, H.to(np.asarray(p.get('eye_pos', (0.42, 0.6, 0.18)), F) * hr), edir, er, hr * 3, open_=p.get('eye_open', (0.92, 0.88)), lid=0.9)
    m.update(head=H, hl=hr * 2 + bl_, eye=eye, eye_r=er, eye_dir=edir, nose=H.to((0.8 * hr + bl_, 0, 0)), body=B)
    # legs: thigh hidden in the body, tibiotarsus, tarsometatarsus, toes (3 fwd + hallux)
    tars, tr = p['tars'], p.get('tars_r', 0.08 * p['tars'] + 0.002)
    yl = bw * 0.22
    if spread < 0.5:
        knee = B.to((-0.02 * bL, yl, -0.35 * bh)); ank = V(knee[0] + 0.15 * tars, yl, tars * 0.98 + p.get('toe_h', 0.0))
        tib = p.get('tibia', 0.9 * tars)
        knee = ank + S._n(V(-0.35, 0, 1)) * tib
        foot = V(ank[0] + 0.05 * tars, yl, 0.0)
        legz = 'leg_f' if p.get('feathered_legs') else 'leg'
        b.rcone(B.to((-0.05 * bL, yl, -0.25 * bh)), knee, p.get('thigh_r', tr * 2.6), p.get('thigh_r', tr * 2.6) * 0.62, 'thigh', 0.5 * tr * 3)
        b.rcone(knee, ank, tr * 1.6, tr * 1.1, legz, 0.4 * tr)
        b.rcone(ank, foot + V(0, 0, tr), tr, tr * 0.9, 'leg' if not p.get('feathered_legs') else 'leg_f', 0.3 * tr)
        toe = p.get('toe', 0.6 * tars)
        for ang in (-28, 0, 28, 180):
            d = V(np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0)
            ln = toe * (0.55 if ang == 180 else (1.0 if ang == 0 else 0.8))
            tp = [foot + V(0, 0, tr * 0.9), foot + d * ln * 0.55 + V(0, 0, tr * 0.7), foot + d * ln + V(0, 0, tr * 0.6)]
            b.chain(tp, [tr * 0.9, tr * 0.65, tr * 0.45], 'toe', 0.3 * tr)
            b.rcone(tp[-1], tp[-1] + d * ln * p.get('talon', 0.15) - V(0, 0, ln * p.get('talon', 0.15) * 0.8), tr * 0.42, tr * 0.08, 'claw', 0.15 * tr)
        for pr in [x for x in b.prims[-30:] if x.zone in ('thigh', 'leg', 'leg_f', 'toe', 'claw')]:
            pass
        _mirror_tail(b, ('thigh', 'leg', 'leg_f', 'toe', 'claw'))
    else:   # flight: legs tucked under the tail
        legz = 'leg_f' if p.get('feathered_legs') else 'leg'
        k0 = B.to((-0.15 * bL, yl, -0.35 * bh))
        b.rcone(k0, B.to((-0.45 * bL, yl * 0.7, -0.38 * bh)), tr * 1.6, tr, legz, 0.4 * tr, mirror=True)
        b.rcone(B.to((-0.45 * bL, yl * 0.7, -0.38 * bh)), B.to((-0.62 * bL, yl * 0.6, -0.30 * bh)), tr * 1.3, tr * 0.6, 'toe', 0.4 * tr, mirror=True)
    m['legs_tucked'] = spread >= 0.5
    parts = {'body': b}
    return parts, m


def _mirror_tail(part, zones):
    """mirror (in Y) the prims of the given zones that were added without mirror."""
    new = []
    for pr in part.prims:
        if pr.zone in zones and pr.p.get('a', pr.p.get('c'))[1] > 0:
            q = S.Prim(pr.kind, pr.zone, pr.k, pr.sub, None, **{k: (v * np.array([1, -1, 1], F) if k in ('a', 'b', 'c') else v) for k, v in pr.p.items()})
            if 'R' in q.p:
                Mm = np.diag([1, -1, 1]).astype(F); q.p['R'] = (Mm @ q.p['R'] @ Mm).astype(F)
            q.bbox = S._bbox(q); new.append(q)
    part.prims += new


def wing_joints(B, p, side=1):
    """FLIGHT pose (spread = 1): body horizontal, wing along ±Y. shoulder, elbow, wrist, hand tip (world)."""
    ws = p['ws']; bL, bw, bh = p['body'], p['bw'], p['bh']
    half = ws / 2
    sh_ = B.to((0.20 * bL, side * bw * 0.42, 0.22 * bh))
    hand_tip_y = half - p.get('primary', 0.25 * ws) * 0.55        # primaries extend the span beyond the hand
    el = sh_ + V(-0.02 * bL, side * (hand_tip_y - abs(sh_[1])) * 0.36, 0.01)
    wr = sh_ + V(0.06 * bL, side * (hand_tip_y - abs(sh_[1])) * 0.74, 0.02)
    tip = V(wr[0] - 0.04 * bL, side * hand_tip_y, wr[2] + 0.01)
    return sh_, el, wr, tip, None


def wing_part(m, p):
    """solid wing parts. FOLDED: wing cloak on each flank (shoulder → rump, coverts + scapulars).
    FLIGHT: arm with leading-edge patagium + coverts sheet (chord toward the tail)."""
    B = m['body']; w = S.Part('wings', voxel=p.get('voxel', 0.003))
    bL, bw, bh = p['body'], p['bw'], p['bh']; th = p.get('wing_th', 0.05 * bh)
    if p.get('spread', 0) < 0.5:
        # cloak: flattened ellipsoids on the flanks, slightly raised at the shoulder, tapering to the rump
        w.ell(B.to((0.02 * bL, 0.40 * bw, 0.14 * bh)), V(0.40 * bL, 0.16 * bw, 0.36 * bh), B.R @ S.rot_mat(4, 0, -12), zone='covert', k=th, mirror=True)
        w.ell(B.to((-0.24 * bL, 0.32 * bw, 0.22 * bh)), V(0.34 * bL, 0.13 * bw, 0.26 * bh), B.R @ S.rot_mat(8, 0, -18), zone='wing', k=th, mirror=True)
        w.ell(B.to((0.20 * bL, 0.36 * bw, 0.26 * bh)), V(0.14 * bL, 0.14 * bw, 0.18 * bh), B.R, zone='covert', k=th, mirror=True)   # shoulder / wrist bulge
        return w
    for side in (1,):
        sh_, el, wr, tip, _ = wing_joints(B, p, side)
        w.chain([sh_, el, wr, tip], [th * 1.8, th * 1.3, th * 1.0, th * 0.5], 'wing', th * 0.8, mirror=True)
        ch = p.get('chord', 0.30 * p['ws'] / 2)
        for a, b_, c0, c1 in ((sh_, el, 0.62, 0.55), (el, wr, 0.55, 0.42), (wr, tip, 0.30, 0.12)):
            for t in np.linspace(0, 1, 4):
                q = a + (b_ - a) * t; c = ch * (c0 + (c1 - c0) * t)
                w.ell(q + V(-c * 0.42, 0, th * 0.1), V(c * 0.48, np.linalg.norm(b_ - a) * 0.22, th * 0.75), zone='covert', k=th * 1.5, mirror=True)
    return w


def feathers(m, p, collection_mesh):
    """real feather blades (rachis + asymmetric vanes) for primaries, secondaries and the tail.
    Returns (verts, faces, attrs) — t7_build turns it into one mesh 'feathers' with per-feather 'fid' / 'ft' (0 base → 1 tip) attributes."""
    B = m['body']; spread = p.get('spread', 0.0)
    V_, F_, A_ = [], [], {'fid': [], 'ft': [], 'fu': [], 'kind': []}
    fid = 0

    def blade(base, d, n, L_, W_, asym=0.35, curve=0.08, twist_up=None, kind=0):
        nonlocal fid
        d = S._n(d); n = S._n(n - d * (n @ d)); s = np.cross(n, d)
        segs, cols = 10, 5
        idx0 = len(V_)
        for i in range(segs + 1):
            t = i / segs
            w = W_ * min(1.0, 0.35 + 4.0 * t) * np.sqrt(max(0.0, 1 - max(0.0, (t - 0.72) / 0.28) ** 2))   # broad vane, rounded tip
            for j in range(cols):
                u = j / (cols - 1) * 2 - 1                 # -1 outer vane … +1 inner vane
                ww = w * (asym if u < 0 else 1.0)
                pos = base + d * L_ * t + s * ww * u * 0.5 + n * (curve * L_ * t * t - 0.012 * L_ * abs(u) * (1 - t))
                V_.append(pos); A_['fid'].append(fid); A_['ft'].append(t); A_['fu'].append(u); A_['kind'].append(kind)
        for i in range(segs):
            for j in range(cols - 1):
                a = idx0 + i * cols + j
                F_.append((a, a + 1, a + cols + 1, a + cols))
        fid += 1

    up = V(0, 0, 1)
    n_pri, n_sec = p.get('n_pri', 10), p.get('n_sec', 12)
    lp = p.get('primary', 0.25 * p['ws']); ls = p.get('secondary', 0.62 * lp)
    bL, bw, bh = p['body'], p['bw'], p['bh']
    for side in (1, -1):
        if spread < 0.5:
            # FOLDED: primaries stacked along the back (outermost on top), tips toward the tail; secondaries beneath
            wr = B.to((0.16 * bL, side * 0.40 * bw, 0.30 * bh))
            nB = B.R @ V(0, 0, 1)
            for i in range(n_pri):
                t = i / (n_pri - 1)
                base = wr + B.R @ V(-0.06 * bL * t, -side * 0.06 * bw * t, 0.012 * (1 - t))
                d = S._n(B.R @ V(-1, -side * 0.10, -0.06))
                Lp = lp * (0.70 + 0.30 * np.sin(np.pi * (0.2 + 0.65 * t)))
                blade(base, d, nB + B.R @ V(0, side * 0.6, 0), Lp, Lp * p.get('pri_w', 0.16) * 0.9, asym=0.45, curve=0.02, kind=0)
            for i in range(n_sec):
                t = i / (n_sec - 1)
                base = B.to((0.10 * bL - 0.32 * bL * t, side * (0.44 - 0.04 * t) * bw, 0.18 * bh - 0.06 * bh * t))
                d = S._n(B.R @ V(-1, -side * 0.06, -0.10))
                blade(base, d, nB + B.R @ V(0, side * 0.8, 0), ls * 0.9, ls * p.get('sec_w', 0.28), asym=0.6, curve=0.02, kind=1)
            continue
        sh_, el, wr, tip, _ = wing_joints(B, p, side)
        # secondaries + tertials along the forearm / upper arm, pointing back
        for i in range(n_sec + 3):
            t = i / (n_sec + 2)
            base = sh_ + (wr - sh_) * (0.05 + 0.93 * t)
            d = S._n(V(-1, side * 0.06 * t, -0.02))
            Ls = ls * (0.92 + 0.08 * np.sin(np.pi * t)) * (0.85 if i < 3 else 1.0)
            blade(base + V(0, 0, -0.004), d, up, Ls, Ls * p.get('sec_w', 0.28), asym=0.6, curve=-0.02, kind=1)
        # primaries fan along the hand: innermost back, outermost out (slotted 'fingers')
        for i in range(n_pri):
            t = i / (n_pri - 1)
            base = wr + (tip - wr) * (0.15 + 0.85 * t ** 0.8)
            ang = np.radians(10 + 62 * t ** 1.1)                  # angle from 'back' toward 'out'
            d = S._n(V(-np.cos(ang), side * np.sin(ang), 0.01 * t))
            Lp = lp * (0.68 + 0.32 * np.sin(np.pi * (0.15 + 0.55 * t))) * (0.88 if i == n_pri - 1 else 1.0)
            emarg = p.get('emarg', 1.0) if t > 0.45 else 0.0
            W = Lp * p.get('pri_w', 0.16) * (1 - 0.45 * emarg)
            blade(base + V(0, 0, -0.003 + 0.004 * t), d, up, Lp, W, asym=0.45, curve=0.06 * t, kind=0)
    # tail fan
    nt = p.get('n_tail', 12); tl = p.get('tail', 0.3 * p['body']); tw = p.get('tail_w', 0.18)
    t0 = B.to((-0.42 * p['body'], 0, 0.10 * p['bh']))
    tdir = S._n(B.R @ V(-1, 0, -0.18)) if spread < 0.5 else S._n(V(-1, 0, -0.03))
    fan = np.radians(p.get('tail_fan', 18 if spread < 0.5 else 55))
    for i in range(nt):
        u = i / (nt - 1) * 2 - 1
        a = fan * u * 0.5
        d = S._n(tdir * np.cos(a) + V(0, 1, 0) * np.sin(a))
        Lt = tl * (1 - p.get('tail_fork', 0.0) * (1 - abs(u)) - p.get('tail_round', 0.08) * abs(u) ** 2)
        blade(t0 + V(0, u * p['bw'] * 0.18, 0.002 * abs(u)), d, V(0, 0, 1), Lt, Lt * tw, asym=0.8, curve=0.02, kind=2)
    return np.array(V_, F), np.array(F_, np.int32), {k: np.array(v, F) for k, v in A_.items()}
