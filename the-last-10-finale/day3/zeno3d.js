// ZENO — 3D alien meshes (software renderer, flat + rim shading, dark outline to match the cel style).
// Units: metres, y up, feet at y = 0, model faces +z.  Used by the design sheet now and by the animation engine later.
(function (G) {
  const V3 = {
    add: (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]], sub: (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]],
    mul: (a, k) => [a[0] * k, a[1] * k, a[2] * k], dot: (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2],
    cross: (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]],
    norm: a => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; },
  };
  const PAL = {
    armour: [46, 32, 58], armourHi: [92, 66, 112], skin: [24, 18, 30], joint: [16, 12, 20], bone: [120, 104, 132],
    glow: [79, 195, 255], eye: [255, 50, 60], plasma: [190, 90, 255], metal: [70, 66, 80], cape: [58, 14, 30], gold: [150, 120, 70],
  };
  // ellipsoid along a segment a→b with radii (r at middle, taper k at ends)
  function limb(M, a, b, r, col, opt = {}) {
    const N = opt.n || 10, S = opt.s || 7, ax = V3.sub(b, a), L = Math.hypot(...ax), d = V3.norm(ax);
    let up = Math.abs(d[1]) > 0.9 ? [1, 0, 0] : [0, 1, 0];
    const u = V3.norm(V3.cross(d, up)), v = V3.cross(u, d), base = M.V.length, flat = opt.flat || 1;
    for (let i = 0; i <= S; i++) {
      const t = i / S, prof = Math.sin(Math.PI * Math.min(1, Math.max(0, t))) ** (opt.pow || 0.22), rr = r * (opt.r0 !== undefined ? (opt.r0 + (opt.r1 - opt.r0) * t) : 1) * Math.max(0.04, prof);
      const c = V3.add(a, V3.mul(ax, t));
      for (let j = 0; j < N; j++) { const q = j / N * Math.PI * 2; M.V.push(V3.add(c, V3.add(V3.mul(u, Math.cos(q) * rr), V3.mul(v, Math.sin(q) * rr * flat)))); }
    }
    for (let i = 0; i < S; i++) for (let j = 0; j < N; j++) M.F.push({ v: [base + i * N + j, base + i * N + (j + 1) % N, base + (i + 1) * N + (j + 1) % N, base + (i + 1) * N + j], c: col, sheen: opt.sheen || 0 });
  }
  const blob = (M, c, r, col, opt = {}) => { const e = opt.e || [0, 1, 0]; limb(M, V3.sub(c, V3.mul(e, r[1])), V3.add(c, V3.mul(e, r[1])), r[0], col, { ...opt, flat: r[2] / r[0], pow: 0.5 }); };
  function cone(M, a, b, r, col) { limb(M, a, b, r, col, { r0: 1, r1: 0.05, pow: 0.15, n: 6, s: 3 }); }
  const glowPt = (M, p, rad, col, k) => M.L.push({ p, rad, col, k });

  function buildZeno(o = {}) {
    const M = { V: [], F: [], L: [] }, P = PAL, sc = o.scale || 1, S = p => [p[0] * sc, p[1] * sc, p[2] * sc];
    const lim = (a, b, r, c, op) => limb(M, S(a), S(b), r * sc, c, op);
    for (const s of [-1, 1]) {
      // digitigrade legs
      lim([0.17 * s, 1.34, -0.02], [0.23 * s, 0.78, 0.17], 0.13, P.armour, { sheen: 1 });
      lim([0.23 * s, 0.86, 0.15], [0.22 * s, 0.26, -0.17], 0.095, P.skin);
      lim([0.22 * s, 0.34, -0.18], [0.23 * s, 0.02, 0.05], 0.07, P.joint);
      lim([0.23 * s, 0.05, 0.04], [0.25 * s, 0.02, 0.30], 0.06, P.armour, { flat: 0.45, sheen: 1 });
      blob(M, S([0.23 * s, 0.82, 0.18]), [0.085 * sc, 0.06 * sc, 0.085 * sc], P.armourHi, { sheen: 1 });  // knee plate
      for (const j of [[0.17, 1.3, -0.02], [0.23, 0.82, 0.16], [0.22, 0.3, -0.17], [0.45, 1.58, 0.1]]) blob(M, S([j[0] * s, j[1], j[2]]), [0.085 * sc, 0.085 * sc, 0.085 * sc], P.joint);
      // long arms
      blob(M, S([0.37 * s, 2.03, 0.02]), [0.15 * sc, 0.09 * sc, 0.14 * sc], P.armourHi, { sheen: 1 });   // shoulder pad
      lim([0.36 * s, 2.04, 0.02], [0.45 * s, 1.54, 0.11], 0.095, P.armour, { sheen: 1 });
      lim([0.45 * s, 1.62, 0.09], [0.47 * s, 1.12, 0.27], 0.08, P.skin);
      blob(M, S([0.465 * s, 1.36, 0.19]), [0.075 * sc, 0.12 * sc, 0.07 * sc], P.armour, { sheen: 1, e: V3.norm([0.02 * s, -0.42, 0.16]) }); // bracer
      for (let k = -1; k <= 1; k++) lim([(0.47 + k * 0.025) * s, 1.16, 0.26], [(0.48 + k * 0.05) * s, 0.98, 0.32 + k * 0.03], 0.018, P.bone, { n: 5, s: 4 }); // claws
      glowPt(M, S([0.46 * s, 1.33, 0.26]), 0.025 * sc, P.glow, 0);
    }
    // pelvis, abdomen, chest (leaning forward)
    blob(M, S([0, 1.3, -0.02]), [0.22 * sc, 0.12 * sc, 0.15 * sc], P.armour, { sheen: 1 });
    lim([0, 1.22, -0.01], [0, 1.86, 0.04], 0.19, P.skin, { flat: 0.75 });
    for (let k = 0; k < 3; k++) blob(M, S([0, 1.44 + k * 0.1, 0.1]), [0.12 * sc, 0.035 * sc, 0.05 * sc], P.armourHi, { sheen: 1 }); // ab plates
    blob(M, S([0, 1.9, 0.05]), [0.34 * sc, 0.25 * sc, 0.22 * sc], P.armour, { sheen: 1, e: V3.norm([0, 1, 0.25]) });
    blob(M, S([0, 1.93, 0.16]), [0.2 * sc, 0.13 * sc, 0.1 * sc], P.armourHi, { sheen: 1 }); // breast plate
    // back spines
    for (let k = 0; k < 4; k++) cone(M, S([0, 2.06 - k * 0.15, -0.1 + k * 0.01]), S([0, 2.16 - k * 0.15, -0.34 + k * 0.03]), 0.04 * sc, P.bone);
    // long neck with the blue link ring (weak point)
    lim([0, 2.0, 0.04], [0, 2.4, 0.26], 0.085, P.skin);
    for (let k = 0; k < 7; k++) { const t = k / 6, a = (t - 0.5) * 1.6; glowPt(M, S([Math.sin(a) * 0.07, 2.18 + t * 0.05, 0.15 + Math.cos(a) * 0.05]), 0.016 * sc, P.glow, 1); }
    // elongated head + visor
    lim([0, 2.34, 0.14], [0, 2.5, 0.52], 0.13, P.armour, { sheen: 1, flat: 0.8 });
    lim([0, 2.45, 0.08], [0, 2.62, -0.12], 0.06, P.armourHi, { sheen: 1, r0: 1, r1: 0.2, pow: 0.3 }); // crest
    lim([0, 2.38, 0.40], [0, 2.43, 0.56], 0.07, P.joint, { flat: 0.7 }); // jaw
    [[-0.055, 2.47, 0.47], [0.055, 2.47, 0.47], [0, 2.51, 0.49]].forEach(p => glowPt(M, S(p), 0.022 * sc, P.eye, 2));
    if (o.commander) {
      for (const s of [-1, 1]) { cone(M, S([0.08 * s, 2.52, 0.12]), S([0.26 * s, 2.92, -0.1]), 0.045 * sc, P.bone); cone(M, S([0.05 * s, 2.55, 0.0]), S([0.14 * s, 2.86, -0.26]), 0.035 * sc, P.gold); }
      cone(M, S([0, 2.58, 0.06]), S([0, 3.0, -0.08]), 0.05 * sc, P.gold);
      // cape: a curved sheet hanging from the shoulders
      const cw = 9, ch = 6, base = M.V.length;
      for (let i = 0; i <= ch; i++) for (let j = 0; j <= cw; j++) { const u = j / cw - 0.5, t = i / ch; M.V.push(S([u * (0.75 + t * 0.55), 2.05 - t * 1.95, -0.18 - Math.cos(u * 2.6) * 0.12 - t * 0.22 + Math.sin(j * 1.7 + i) * 0.02])); }
      for (let i = 0; i < ch; i++) for (let j = 0; j < cw; j++) M.F.push({ v: [base + i * (cw + 1) + j, base + i * (cw + 1) + j + 1, base + (i + 1) * (cw + 1) + j + 1, base + (i + 1) * (cw + 1) + j], c: P.cape, two: 1 });
    }
    if (o.rifle) addRifle(M, S([0.47, 1.17, 0.27]), sc);
    return M;
  }
  function addRifle(M, grip, sc = 1) {
    const P = PAL, at = p => V3.add(grip, V3.mul(p, sc));
    limb(M, at([0, 0.02, -0.25]), at([0, 0.05, 0.62]), 0.055 * sc, P.metal, { flat: 0.7, sheen: 1 });      // body
    limb(M, at([0, 0.1, -0.05]), at([0, 0.09, 0.4]), 0.05 * sc, P.armour, { sheen: 1 });                 // top shell
    for (const s of [-1, 1]) limb(M, at([0.03 * s, 0.04, 0.35]), at([0.05 * s, 0.03, 0.82]), 0.02 * sc, P.bone, { n: 6, s: 4 }); // prongs
    for (let k = 0; k < 4; k++) M.L.push({ p: at([0, 0.06, 0.05 + k * 0.12]), rad: 0.02 * sc, col: P.plasma, k: 3 });
    M.L.push({ p: at([0, 0.04, 0.84]), rad: 0.05 * sc, col: P.plasma, k: 4 });
  }
  function buildRifle() { const M = { V: [], F: [], L: [] }; addRifle(M, [0, 0, 0], 1); return M; }
  function buildDrone() {
    const M = { V: [], F: [], L: [] }, P = PAL;
    blob(M, [0, 0, 0], [0.32, 0.22, 0.32], P.armour, { sheen: 1 });
    blob(M, [0, -0.12, 0.05], [0.2, 0.1, 0.2], P.metal, { sheen: 1 });
    for (let k = 0; k < 3; k++) { const a = k / 3 * Math.PI * 2 + Math.PI / 2, d = [Math.cos(a), 0, Math.sin(a)];
      limb(M, V3.mul(d, 0.2), V3.add(V3.mul(d, 0.78), [0, 0.1, 0]), 0.09, P.armourHi, { flat: 0.22, sheen: 1 });
      M.L.push({ p: V3.add(V3.mul(d, 0.78), [0, 0.1, 0]), rad: 0.035, col: P.eye, k: 5 }); }
    M.L.push({ p: [0, -0.02, 0.33], rad: 0.07, col: P.eye, k: 2 });
    M.L.push({ p: [0, -0.24, 0], rad: 0.06, col: P.glow, k: 1 });
    return M;
  }
  // render: cam {yaw, pitch, dist, f, cx, cy, target}
  function render(ctx, M, cam, t = 0) {
    const cy = Math.cos(cam.yaw), sy = Math.sin(cam.yaw), cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch), T = cam.target;
    const tr = p => { let x = p[0] - T[0], y = p[1] - T[1], z = p[2] - T[2];
      let X = x * cy - z * sy, Z = x * sy + z * cy; let Y = y * cp + Z * sp; Z = -y * sp + Z * cp; Z = cam.dist - Z;
      const k = cam.f / Z; return [cam.cx + X * k, cam.cy - Y * k, Z, X, Y]; };
    const P = M.V.map(tr), Ld = V3.norm([-0.5, 0.8, 0.6]);
    const lw = V3.norm([Ld[0] * cy - Ld[2] * sy, Ld[1], Ld[0] * sy + Ld[2] * cy]);
    const faces = [];
    for (const f of M.F) { const q = f.v.map(i => P[i]); if (q.some(p => p[2] < 0.3)) continue; const a = M.V[f.v[0]], b = M.V[f.v[1]], c = M.V[f.v[2]];
      let n = V3.norm(V3.cross(V3.sub(b, a), V3.sub(c, a)));
      let X = n[0] * cy - n[2] * sy, Z = n[0] * sy + n[2] * cy, Y = n[1] * cp + Z * sp; Z = -n[1] * sp + Z * cp; // view-space normal (towards camera = +Z)
      const area = (q[1][0] - q[0][0]) * (q[2][1] - q[0][1]) - (q[2][0] - q[0][0]) * (q[1][1] - q[0][1]);
      if (Z < 0) { X = -X; Y = -Y; Z = -Z; }
      const d = Math.max(0, X * lw[0] + Y * lw[1] + Z * lw[2]), rim = Math.pow(1 - Math.abs(Z), 3);
      faces.push({ q, z: q.reduce((s, p) => s + p[2], 0) / q.length, d, rim, f }); }
    faces.sort((a, b) => b.z - a.z);
    ctx.save(); ctx.lineJoin = 'round';
    for (const { q, d, rim, f } of faces) { const c = f.c, k = 0.42 + d * 0.75, sh = f.sheen ? Math.pow(d, 10) * 70 : 0;
      ctx.fillStyle = `rgb(${c[0] * k + sh + rim * 60},${c[1] * k + sh + rim * 80},${c[2] * k + sh + rim * 120})`;
      ctx.strokeStyle = ctx.fillStyle; ctx.lineWidth = 0.7;
      ctx.beginPath(); q.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath(); ctx.fill(); ctx.stroke(); }
    ctx.globalCompositeOperation = 'lighter';
    for (const L of M.L) { const p = tr(L.p); if (p[2] < 0.3) continue; const r = L.rad * cam.f / p[2], c = L.col, pulse = 0.85 + 0.15 * Math.sin(t * 3 + L.k);
      const g = ctx.createRadialGradient(p[0], p[1], 0, p[0], p[1], r * 4); g.addColorStop(0, `rgba(${c},${0.9 * pulse})`); g.addColorStop(0.25, `rgba(${c},${0.45 * pulse})`); g.addColorStop(1, `rgba(${c},0)`);
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p[0], p[1], r * 4, 0, 7); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.9)'; ctx.beginPath(); ctx.arc(p[0], p[1], r * 0.45, 0, 7); ctx.fill(); }
    ctx.restore();
    return tr;
  }
  G.ZENO = { PAL, buildZeno, buildRifle, buildDrone, render };
})(typeof window !== 'undefined' ? window : globalThis);
