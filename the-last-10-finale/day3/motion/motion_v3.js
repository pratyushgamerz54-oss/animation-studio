// THE LAST 10 — motion v2: human-like body mechanics for the 2D cut-out rigs (front view).
// Rig units: 1 head = 100, feet at y = 0, hip pivot [0,-380], shoulder [77.5,-558], neck [0,-602].
// drawChar2(ctx, IMG, k, x, footY, scale, P) draws one character from a pose object P produced by the motion generators below.
(function (G) {
  const TAU = Math.PI * 2, clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v)), lerp = (a, b, t) => a + (b - a) * t;
  const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const noise = (t, seed) => Math.sin(t * 0.73 + seed) * 0.5 + Math.sin(t * 1.37 + seed * 2.1) * 0.3 + Math.sin(t * 2.91 + seed * 3.7) * 0.2;
  const smooth = x => x * x * (3 - 2 * x);
  const easeOutBack = (x, k = 1.9) => 1 + (k + 1) * Math.pow(x - 1, 3) + k * Math.pow(x - 1, 2);
  const LEG = 336;  // hip → ankle length in rig units

  // ---------------- drawing ----------------
  function drawChar2(ctx, IMG, k, x, footY, s, P) {
    const R = IMG[k]; if (!R) return;
    const about = (p, a) => { ctx.translate(p[0], p[1]); ctx.rotate(a); ctx.translate(-p[0], -p[1]); };
    const sclY = (p, sy, sx = 1) => { ctx.translate(p[0], p[1]); ctx.scale(sx, sy); ctx.translate(-p[0], -p[1]); };
    // some sheet parts (hair_back) are stored relative to their pivot, the rest in body space — place both correctly
    const part = n => { const q = R[n]; if (!(q && q.img && (q.img.complete === undefined || q.img.complete) && (q.img.naturalWidth || q.img.width))) return;
      const oy = (q.vb[1] > -300 && q.pivot[1] < -300) ? q.pivot[1] : 0; ctx.drawImage(q.img, q.vb[0], q.vb[1] + oy, q.vb[2], q.vb[3]); };
    const segs = (names, S, mirror) => { ctx.save(); if (mirror) ctx.scale(-1, 1);
      names.forEach((n, i) => { const q = R[n]; if (!q) return; const [a, sy, sx] = S[i] || [0, 1, 1]; about(q.pivot, a || 0); sclY(q.pivot, sy || 1, sx || 1); part(n); }); ctx.restore(); };
    const hx = P.hipShift || 0, drop = P.drop || 0, br = P.breath || 0, shrug = P.shrug || 0, tw = P.twist || 0, bend = P.bend || 0, back = !!P.back;
    const bendY = 178 * 0.34 * bend;                          // shoulders come down when the torso folds forward
    const head = () => { ctx.translate(hx * 0.8 + (P.headX || 0) - tw * 4, drop + (P.headY || 0) - br * 1.2 - shrug * 6 + bendY * 1.35 + (P.hairBounce || 0) * 0); about([0, -560], P.chestTilt || 0); about([0, -602], P.headTilt || 0); };
    ctx.save(); ctx.translate(x, footY); ctx.scale(s * (P.flip ? -1 : 1), s);
    if (P.shake) ctx.translate(P.shake[0], P.shake[1]);
    // contact shadow follows the feet, shrinks when airborne
    const air = P.airborne || 0; ctx.fillStyle = `rgba(0,0,0,${0.36 - air * 0.14})`; ctx.beginPath(); ctx.ellipse(hx * 0.3, -4, 82 - air * 30, 13 - air * 3, 0, 0, 7); ctx.fill();
    ctx.translate(0, -air * 26);
    if (!back) { ctx.save(); head(); ctx.translate(0, (P.hairBounce || 0)); part('hair_back'); ctx.restore(); }
    // legs hang from the (shifted, tilted) pelvis; stance feet stay planted. Seen from behind, the character's left leg is on screen right.
    const legs = () => {
      ctx.save(); ctx.translate(hx, drop); about([0, -380], P.hipTilt || 0); sclY([0, -380], 1, 1 + tw * 0.04 * (back ? -1 : 1));
      const L = back ? (P.legR || {}) : (P.legL || {}), Rr = back ? (P.legL || {}) : (P.legR || {});
      const plant = hx / LEG, kc = (LEG - drop) / LEG;
      const heel = l => [[(l.f || 0), 1, l.fs || 1]];
      segs(['thigh', 'shin', 'foot'], [[(L.a || 0) - plant, (L.sy || 1) * kc], [L.k || 0, L.sk || 1], [L.f || 0, L.fh || 1, L.fs || 1]], true);
      segs(['thigh', 'shin', 'foot'], [[(Rr.a || 0) + plant, (Rr.sy || 1) * kc], [Rr.k || 0, Rr.sk || 1], [Rr.f || 0, Rr.fh || 1, Rr.fs || 1]], false);
      ctx.restore(); };
    legs();
    // body: pelvis turns with the hips, chest counter-turns (twist), torso folds forward with bend
    ctx.save(); ctx.translate(hx * 0.9, drop); about([0, -380], P.hipTilt || 0);
    ctx.save(); sclY([0, -380], 1, 1 + tw * 0.05); part('pelvis'); ctx.restore();
    about([0, -380], -(P.hipTilt || 0)); about([0, -380], P.chestTilt || 0);
    const drawArms = () => { ctx.save(); ctx.translate(0, -br * 1.6 - shrug * 10 + bendY);
    const A = (arm) => [[arm[0] || 0, arm[3] || 1], [arm[1] || 0, arm[4] || 1], [arm[2] || 0, 1]];
      const aL = back ? P.armR : P.armL, aR = back ? P.armL : P.armR;
      ctx.save(); ctx.translate(-tw * 7, 0); segs(['upper_arm', 'forearm', 'hand'], A(aL || [0.04, 0.06, 0]), true); ctx.restore();
      ctx.save(); ctx.translate(-tw * 7, 0); segs(['upper_arm', 'forearm', 'hand'], A(aR || [0.04, 0.06, 0]), false); ctx.restore();
    ctx.restore(); };
    if (back) drawArms();
    ctx.save(); sclY([0, -380], (1 + br * 0.012) * (1 - 0.34 * bend), (1 + br * 0.008) * (1 - tw * 0.05)); part(back ? 'torsoBack' : 'torso'); ctx.restore();
    const acc = R.accessory; if (!back && acc && acc.pivot[1] > -600) part('accessory');
    if (!back) drawArms();
    ctx.restore();
    if (back) {   // back of the head: hair-covered head, then the back hair hanging over it
      ctx.save(); head(); part('headBack'); ctx.translate(0, (P.hairBounce || 0)); part('hair_back'); if (P.backHairFront) part('hair_front'); ctx.restore();
      ctx.restore(); return;
    }
    // head + face (head turn = features slide + slight squash)
    ctx.save(); head(); const turn = P.turn || 0; sclY([0, -602], 1, 1 - Math.abs(turn) * 0.05); part('head');
    const bl = 1 - clamp(P.blink || 0) * 0.9, lx = (P.lookX || 0) + turn * 6, ly = P.lookY || 0;
    ctx.save(); ctx.translate(turn * 5, 0);
    ['eye_L', 'eye_R'].forEach(n => { const q = R[n]; if (!q) return; ctx.save(); ctx.translate(q.pivot[0] + lx, q.pivot[1] + ly); ctx.scale(1, bl); ctx.translate(-q.pivot[0], -q.pivot[1]); part(n); ctx.restore(); });
    const bw = R.brow_L; if (bw) [false, true].forEach(m => { ctx.save(); if (m) ctx.scale(-1, 1); ctx.translate(0, -(P.brow || 0)); about(bw.pivot, (P.browRot || 0)); part('brow_L'); ctx.restore(); });
    mouth(ctx, P.mouth || 'X'); ctx.restore();
    ctx.save(); ctx.translate(0, (P.hairBounce || 0) * 0.6); part('hair_front'); ctx.restore(); if (R.glasses) part('glasses'); if (acc && acc.pivot[1] <= -600) part('accessory');
    ctx.restore();
    ctx.restore();
  }
  function mouth(ctx, m) { ctx.save(); ctx.translate(0, -620); ctx.lineWidth = 2.6; ctx.strokeStyle = '#2b2321'; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    const ov = (rx, ry, y = 0) => { ctx.fillStyle = '#4a2226'; ctx.beginPath(); ctx.ellipse(0, y, rx, ry, 0, 0, 7); ctx.fill(); ctx.stroke(); };
    const teeth = (w, y, h) => { ctx.fillStyle = '#f5f1e8'; ctx.fillRect(-w / 2, y, w, h); };
    switch (m) { case 'A': ctx.beginPath(); ctx.moveTo(-8, 0); ctx.lineTo(8, 0); ctx.lineWidth = 3.4; ctx.stroke(); break;
      case 'B': ov(8, 2.6, 1); teeth(11, -0.6, 1.6); break; case 'C': ov(7.5, 4, 2); teeth(10, -1, 1.8); break;
      case 'D': ov(8, 6.5, 3); ctx.fillStyle = '#c96b6b'; ctx.beginPath(); ctx.ellipse(0, 6.5, 4.5, 2, 0, 0, 7); ctx.fill(); teeth(10, -2.8, 1.8); break;
      case 'E': ov(5, 4, 2); break; case 'F': ov(3.2, 3.2, 1); break; case 'G': ov(7, 2, 1); teeth(10, -1.8, 2.6); break;
      case 'H': ov(6.5, 4.6, 2); ctx.fillStyle = '#c96b6b'; ctx.beginPath(); ctx.ellipse(0, 0, 3, 1.6, 0, 0, 7); ctx.fill(); break;
      case 'grit': ov(9, 2.4, 1); teeth(16, -0.4, 2.2); break;
      case 'frown': ctx.beginPath(); ctx.moveTo(-9, 2); ctx.quadraticCurveTo(0, -3, 9, 2); ctx.stroke(); break;
      default: ctx.beginPath(); ctx.moveTo(-9, 0); ctx.quadraticCurveTo(0, 2, 9, 0); ctx.stroke(); }
    ctx.restore(); }

  // ---------------- motion generators (all return a pose object) ----------------
  // eyes: saccades (quick jumps, then hold) + irregular blinks with occasional double blink
  function eyes(t, seed) {
    const seg = Math.floor((t + hash(seed) * 3) / (0.9 + hash(seed + 1) * 0.8)); const tt = (t + hash(seed) * 3) % (0.9 + hash(seed + 1) * 0.8);
    const jump = clamp(tt / 0.06), a = hash(seg * 3.1 + seed), b = hash(seg * 7.7 + seed), pa = hash((seg - 1) * 3.1 + seed), pb = hash((seg - 1) * 7.7 + seed);
    const lookX = lerp((pa - 0.5) * 5, (a - 0.5) * 5, jump), lookY = lerp((pb - 0.5) * 1.6, (b - 0.5) * 1.6, jump);
    const per = 2.6 + hash(seed + 9) * 2.4, bt = (t + seed * 1.3) % per, bi = Math.floor((t + seed * 1.3) / per);
    const blinkAt = x => x >= 0 && x < 0.16 ? Math.sin(x / 0.16 * Math.PI) : 0;
    let blink = blinkAt(bt); if (hash(bi + seed) > 0.75) blink = Math.max(blink, blinkAt(bt - 0.24));
    return { lookX, lookY, blink };
  }
  // idle: breathing, weight shift between legs, settling, micro head drift, saccades
  function idle(t, seed, o = {}) {
    const breath = Math.sin(t * TAU / (3.4 + hash(seed) * 0.8) + seed);
    const ws = Math.tanh(Math.sin(t * TAU / (5 + hash(seed + 2) * 3) + seed * 5) * 3);   // shifts and holds
    const hipShift = ws * 7, hipTilt = ws * 0.035, relaxed = ws > 0 ? 'legR' : 'legL';
    const P = { breath, hipShift, hipTilt, chestTilt: -hipTilt * 0.55 + noise(t * 0.5, seed) * 0.008,
      headTilt: noise(t * 0.4, seed + 4) * 0.025 - hipTilt * 0.35, headY: breath * -0.6,
      armR: [0.04 - hipTilt * 0.6 + breath * 0.005, 0.07 + noise(t * 0.6, seed) * 0.02, 0.02], armL: [0.04 + hipTilt * 0.6 + breath * 0.005, 0.07 + noise(t * 0.6, seed + 3) * 0.02, 0.02],
      legL: {}, legR: {}, ...eyes(t, seed) };
    P[relaxed] = { a: 0.035, sy: 0.975, k: -0.03 };
    return Object.assign(P, o);
  }
  // walk (toward camera): stride, double bob, hip shift over the stance leg, hip drop on the swing side,
  // counter-rotating shoulders, arms opposite to legs with elbow lag, head stabilised
  function walk(t, seed, o = {}) {
    const sp = o.speed || 1, amp = o.amp ?? 1, f = 0.95 * sp, ph = (o.phase ?? t * TAU * f) + seed;
    const sR = Math.sin(ph), sL = -sR, liftR = Math.max(0, sR), liftL = Math.max(0, sL);
    // push-off: the trailing foot rolls onto its toes just before it lifts (heel rises = foot looks shorter)
    const push = s => Math.max(0, -Math.cos(Math.asin(s)) * 0) + Math.max(0, Math.sin(ph + (s === sR ? 0.9 : 0.9 + Math.PI))) ** 6;
    const legOf = (lift, toe) => ({ a: 0.018 * lift, sy: 1 - 0.19 * lift * amp, k: -0.025 * lift, sk: 1 - 0.09 * lift * amp, fs: 1 + 0.28 * lift * amp, f: 0.05 * lift, fh: 1 - 0.35 * toe * amp });
    const hipTilt = 0.042 * sR * amp, lag = 0.5, twist = 0.9 * sR * amp;
    const fR = -Math.sin(ph - lag), fL = -fR;
    const arm = (fw) => [0.05 - 0.08 * Math.max(0, -fw) * amp, 0.14 + 0.46 * Math.max(0, fw) * amp, 0.06 * Math.sin(ph - lag * 2), 1 - 0.14 * Math.max(0, fw) * amp, 1 - 0.1 * Math.max(0, fw) * amp];
    return Object.assign({ breath: Math.sin(ph * 0.5) * 0.6, drop: 5 * Math.cos(2 * ph) * amp, hipShift: -6.5 * sR * amp, hipTilt, chestTilt: -0.55 * hipTilt, twist,
      headTilt: -0.3 * hipTilt + noise(t * 0.5, seed) * 0.01, headY: 1.4 * Math.cos(2 * ph - 0.6) * amp, hairBounce: 2.2 * Math.cos(2 * ph - 1.1) * amp,
      legR: legOf(liftR, Math.max(0, Math.sin(ph + 0.9 + Math.PI)) ** 6), legL: legOf(liftL, Math.max(0, Math.sin(ph + 0.9)) ** 6),
      armR: arm(fR), armL: arm(fL), ...eyes(t, seed) }, o);
  }
  // run: contact (absorb) → push → flight (both feet off the ground) ×2 per cycle; strong arm pump; torso leans (folds) forward
  function run(t, seed, o = {}) {
    const f = 1.45 * (o.speed || 1), ph = (o.phase ?? t * TAU * f) + seed, sR = Math.sin(ph), liftR = Math.max(0, sR), liftL = Math.max(0, -sR);
    const c2 = Math.cos(2 * ph);                                   // +1 at contact (low), −1 mid-flight (high)
    const air = Math.max(0, -c2 - 0.25) / 0.75;                    // airborne fraction
    const leg = (l, rear) => ({ a: 0.035 * l, sy: 1 - 0.3 * l, k: -0.06 * l, sk: 1 - 0.16 * l, fs: 1 + 0.36 * l, f: 0.1 * l, fh: 1 - 0.45 * rear });
    const pump = s => [0.12 - 0.16 * Math.max(0, -s), 1.15 + 0.6 * Math.max(0, s), 0.15, 1 - 0.22 * Math.max(0, s), 1 - 0.12 * Math.max(0, s)];
    const hipTilt = 0.05 * sR;
    return Object.assign({ drop: 16 + 12 * Math.max(0, c2), airborne: air, hipShift: -7 * sR, hipTilt, chestTilt: -0.6 * hipTilt, twist: 1.2 * sR, bend: 0.32,
      headTilt: -0.25 * hipTilt, headY: 3 + 3 * Math.cos(2 * ph - 0.7), breath: Math.sin(ph) * 1.2, shrug: 0.12, hairBounce: 5 * Math.cos(2 * ph - 1.2),
      legR: leg(liftR, Math.max(0, Math.sin(ph + Math.PI + 0.8)) ** 4), legL: leg(liftL, Math.max(0, Math.sin(ph + 0.8)) ** 4),
      armR: pump(-Math.sin(ph - 0.3)), armL: pump(Math.sin(ph - 0.3)), brow: 3, mouth: (Math.floor(t * 4.2) % 2) ? 'C' : 'E', ...eyes(t, seed) }, o);
  }
  // out of breath after running: hands on knees, deep fast breathing, head hanging, then slowly straightens
  function panting(t, t0, seed) {
    const d = Math.max(0, t - t0), stand = smooth(clamp((d - 3.2) / 1.6)), b = Math.sin(d * TAU * 1.1), u = 1 - stand;
    const P = idle(t, seed);
    return Object.assign(P, { bend: 0.75 * u, drop: 52 * u + b * 2.5 * u, headY: (16 + b * 3) * u, headTilt: 0.02, breath: b * 2.6,
      armR: [0.04 + 0.24 * u, 0.06 - 0.02 * u, 0.25 * u, 1, 1], armL: [0.04 + 0.24 * u, 0.06 - 0.02 * u, 0.25 * u, 1, 1],
      legL: { a: -0.06 * u }, legR: { a: -0.06 * u }, shrug: 0.25 * u * (0.5 + 0.5 * b),
      mouth: (b > 0.2) ? 'D' : 'C', brow: 3, blink: P.blink });
  }
  // limp: injured right leg — short, painful stance on it (body dips + tilts away, head dips, wince), stiff swing
  function limp(t, seed, o = {}) {
    const raw = t * TAU * 0.8 + seed, ph = raw + 0.55 * Math.sin(raw);     // time-warp: less time on the bad leg
    const sR = Math.sin(ph), liftR = Math.max(0, sR), liftL = Math.max(0, -sR), onBad = Math.max(0, -sR);
    const W = (lift, stiff) => ({ a: 0.02 * lift, sy: 1 - 0.17 * lift * stiff, k: -0.02 * lift, sk: 1 - 0.08 * lift * stiff, fs: 1 + 0.22 * lift * stiff });
    const pain = Math.pow(onBad, 3);
    const hipTilt = 0.04 * sR + 0.05 * pain;
    return Object.assign({ drop: 3 * Math.cos(2 * ph) + 12 * pain, hipShift: -9 * sR, hipTilt, chestTilt: -0.9 * hipTilt - 0.03 * pain,
      headTilt: 0.05 * pain - 0.2 * hipTilt, headY: 6 * pain, shrug: 0.3 * pain,
      legR: Object.assign(W(liftR, 0.45), { a: 0.02 * liftR + 0.03 }), legL: W(liftL, 1.25),
      armR: [-0.1 - 0.12 * pain, 0.35 + 0.25 * pain, 0.25], armL: [0.06 + 0.08 * Math.sin(ph), 0.15 + 0.2 * Math.max(0, Math.sin(ph)), 0],
      brow: 3 + 4 * pain, browRot: 0.12 * pain, mouth: pain > 0.4 ? 'grit' : 'X', ...eyes(t, seed), blink: Math.max(eyes(t, seed).blink, pain > 0.75 ? 0.8 : 0) }, o);
  }
  // cold: hunched, arms hugging the body, shoulders up, fast tremor, chattering teeth
  function shiver(t, seed, o = {}) {
    const P = idle(t, seed); const tr = Math.sin(t * TAU * 11) * (0.6 + 0.4 * Math.sin(t * 1.7)), burst = Math.max(0, Math.sin(t * 0.9 + seed)) ** 4;
    return Object.assign(P, { shrug: 0.8, drop: 6, shake: [tr * (1.1 + burst * 1.5), 0], headTilt: P.headTilt + 0.05, headY: 4,
      armR: [0.62 + tr * 0.01, 2.05, 0.35], armL: [0.62 - tr * 0.01, 2.05, 0.35], legL: { a: -0.02, sy: 0.98 }, legR: { a: -0.02, sy: 0.98 },
      mouth: (Math.floor(t * 14) % 2) ? 'grit' : 'X', brow: 4, browRot: 0.14 }, o);
  }
  // flinch: fast protective crouch (arms to face, head away, eyes shut), then a damped settle
  function flinch(t, te) {
    const d = t - te; if (d < 0 || d > 2.2) return null;
    const r = d < 0.09 ? smooth(d / 0.09) : d < 0.5 ? 1 : Math.exp(-(d - 0.5) * 2.0) * Math.cos((d - 0.5) * 3.2) * 0.85 + 0.15 * Math.exp(-(d - 0.5) * 1.0);
    const sh = d < 0.5 ? [Math.sin(d * 90) * 4 * (1 - d / 0.5), Math.cos(d * 77) * 2 * (1 - d / 0.5)] : [0, 0];
    return { r: clamp(r, -0.2, 1), pose: { drop: 26 * r, shrug: 1 * r, headTilt: -0.14 * r, headY: 10 * r, turn: -0.6 * r, blink: d < 0.75 ? 1 : 0, brow: 5 * r, browRot: 0.2 * r,
      armR: [0.55 * r, 2.35 * r, 0.3 * r], armL: [0.45 * r, 2.2 * r, 0.3 * r], legL: { sy: 1 - 0.06 * r, a: -0.04 * r }, legR: { sy: 1 - 0.06 * r, a: -0.04 * r }, shake: sh, mouth: r > 0.5 ? 'grit' : undefined } };
  }
  // gesture with anticipation → strike (overshoot) → hold (micro motion) → release
  function gesture(t, ts, te, target, from) {
    if (t < ts - 0.2 || t > te + 0.6) return null;
    let w, antic = 0;
    if (t < ts) { w = 0; antic = Math.sin(clamp((t - ts + 0.2) / 0.2) * Math.PI) * 0.6; }
    else if (t < ts + 0.28) w = easeOutBack(clamp((t - ts) / 0.28));
    else if (t < te) w = 1 + Math.sin((t - ts) * 3.1) * 0.03;
    else w = 1 - smooth(clamp((t - te) / 0.6));
    const out = {};
    for (const key of Object.keys(target)) { const v = target[key], f = from[key];
      if (Array.isArray(v)) out[key] = v.map((x, i) => { const a = (f || [0, 0, 0, 1, 1])[i] ?? (i > 2 ? 1 : 0); const delayed = i === 2 ? Math.max(0, w - 0.08) : w; return lerp(a, x, delayed) - (i === 0 ? antic * 0.12 : 0); });
      else out[key] = lerp(f || 0, v, w); }
    return out;
  }
  function mix(base, add) { if (!add) return base; const P = { ...base }; for (const k of Object.keys(add)) { const v = add[k]; if (v === undefined) continue;
    if (Array.isArray(v) && Array.isArray(P[k]) && k !== 'shake') P[k] = v; else if (typeof v === 'object' && !Array.isArray(v) && P[k]) P[k] = { ...P[k], ...v }; else P[k] = v; } return P; }
  function blend(a, b, w) { if (w <= 0) return a; if (w >= 1) return b; const P = { ...a };
    for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) { const x = a[k], y = b[k];
      if (typeof x === 'number' || typeof y === 'number') P[k] = lerp(+x || 0, +y || 0, w);
      else if (Array.isArray(x) || Array.isArray(y)) { const X = x || [0.04, 0.06, 0, 1, 1], Y = y || [0.04, 0.06, 0, 1, 1]; P[k] = X.map((v, i) => lerp(v ?? (i > 2 ? 1 : 0), Y[i] ?? (i > 2 ? 1 : 0), w)); }
      else if (x && y && typeof x === 'object') { P[k] = {}; for (const j of new Set([...Object.keys(x), ...Object.keys(y)])) P[k][j] = lerp(x[j] ?? (j[0] === 's' || j === 'fs' ? 1 : 0), y[j] ?? (j[0] === 's' || j === 'fs' ? 1 : 0), w); }
      else P[k] = w < 0.5 ? x : y; }
    return P; }
  G.MOTION2 = { drawChar2, idle, walk, run, panting, limp, shiver, flinch, gesture, mix, blend, eyes, noise, hash };
})(typeof window !== 'undefined' ? window : globalThis);
