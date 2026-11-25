// THE LAST 10 — 3D characters (procedural, built from the user's design-sheet palettes).
// Joint hierarchy (THREE.Group per bone) + rounded body/clothing meshes + painted animated face (eyes, brows, lip-sync mouth).
// Units: metres, feet at y = 0, character faces +z.
import * as THREE from 'three';

const DEF = {   // per-character build: sex, height (m), build, hair style, accessories (from the canon in the sheet README)
  aarav:  { sex: 'm', h: 1.78, fit: 1.0,  hair: 'short',   acc: ['radio'] },
  meera:  { sex: 'f', h: 1.65, fit: 0.2,  hair: 'bob',     acc: ['glasses', 'lanyard'] },
  kabir:  { sex: 'm', h: 1.75, fit: 0.8,  hair: 'messy',   acc: ['toolbelt'], hood: 1 },
  zoya:   { sex: 'f', h: 1.62, fit: 0.3,  hair: 'ponytail', acc: ['stethoscope'] },
  ryan:   { sex: 'm', h: 1.80, fit: 1.0,  hair: 'neat',    acc: ['patch'] },
  ananya: { sex: 'f', h: 1.64, fit: 0.25, hair: 'wavy',    acc: ['camera'] },
  dev:    { sex: 'm', h: 1.83, fit: 1.25, hair: 'buzz',    acc: ['backpack', 'beard'], shortSleeve: 1 },
  ishaan: { sex: 'm', h: 1.72, fit: 0.6,  hair: 'curly',   acc: ['headphones'], hood: 1 },
  sara:   { sex: 'f', h: 1.68, fit: 0.35, hair: 'bun',     acc: ['hammer'] },
  vikram: { sex: 'm', h: 1.81, fit: 1.15, hair: 'saltpep', acc: ['badge', 'belt'] },
};
const col = c => new THREE.Color(c);
const shadeC = (c, f) => { const x = col(c); return f < 0 ? x.multiplyScalar(1 + f) : x.lerp(new THREE.Color(1, 1, 1), f); };

function mat(c, rough = 0.75, extra = {}) { return new THREE.MeshStandardMaterial({ color: col(c), roughness: rough, metalness: 0, ...extra }); }
function capsule(r, len, m, segs = 14) { const g = new THREE.CapsuleGeometry(r, Math.max(0.001, len), 6, segs); const o = new THREE.Mesh(g, m); o.castShadow = true; o.receiveShadow = true; return o; }
// a limb segment hanging down from its joint (tapered capsule built with a lathe)
function limb(r0, r1, len, m, segs = 16) {
  const pts = []; const n = 10;
  for (let i = 0; i <= n; i++) { const a = i / n * Math.PI / 2; pts.push(new THREE.Vector2(Math.sin(a) * r0, Math.cos(a) * r0)); }         // top cap
  for (let i = 1; i < 8; i++) { const u = i / 8; pts.push(new THREE.Vector2(r0 + (r1 - r0) * u + Math.sin(u * Math.PI) * (r0 * 0.08), -len * u)); }
  for (let i = 0; i <= n; i++) { const a = Math.PI / 2 + i / n * Math.PI / 2; pts.push(new THREE.Vector2(Math.sin(a) * r1, -len + Math.cos(a) * r1)); }
  const g = new THREE.LatheGeometry(pts.reverse(), segs); g.computeVertexNormals(); const o = new THREE.Mesh(g, m); o.castShadow = o.receiveShadow = true; return o;
}
function bone(name, parent, x, y, z) { const b = new THREE.Group(); b.name = name; b.position.set(x, y, z); parent.add(b); return b; }

// ---------------- face (painted canvas on a shell over the front of the head) ----------------
function makeFace(P, female) {
  const c = document.createElement('canvas'); c.width = 512; c.height = 512; const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const draw = (st) => { const g = c.getContext('2d'); g.clearRect(0, 0, 512, 512);
    const E = st.emo || {}, hap = E.happy || 0, sad = E.sad || 0, ang = E.angry || 0, fear = E.fear || 0, sur = E.surprise || 0, pain = E.pain || 0, cry = E.cry || 0;
    const ex = 256, ey = 236, sp = female ? 66 : 60, er = (female ? 31 : 26) * (1 + 0.18 * (fear + sur)), look = st.look || [0, 0], bl = Math.max(st.blink || 0, 0.55 * pain);
    const upLid = clamp(0.45 * ang + 0.35 * sad + 0.35 * pain + 0.2 * cry - 0.3 * (fear + sur), 0, 0.75), loLid = clamp(0.55 * hap + 0.4 * pain + 0.3 * ang + 0.2 * cry, 0, 0.65);
    const skinC = P.skin;
    for (const s of [-1, 1]) { const x = ex + s * sp, y = ey, ry = er * (female ? 1.05 : 0.86) * (1 - bl * 0.94);
      g.save(); g.beginPath(); g.ellipse(x, y, er * 1.18, ry, 0, 0, 7); g.clip();
      g.fillStyle = '#f7f3ec'; g.fillRect(x - 70, y - 70, 140, 140);
      const ix = x + look[0] * er * 0.45, iy = y + look[1] * er * 0.3, pr = er * (0.32 + 0.08 * fear - 0.06 * ang);
      g.fillStyle = P.iris; g.beginPath(); g.arc(ix, iy, er * 0.62, 0, 7); g.fill(); g.fillStyle = '#120c0a'; g.beginPath(); g.arc(ix, iy, pr, 0, 7); g.fill();
      g.fillStyle = 'rgba(255,255,255,.95)'; g.beginPath(); g.arc(ix - er * 0.22, iy - er * 0.24, er * 0.17, 0, 7); g.fill();
      if (cry > 0.2) { g.fillStyle = `rgba(200,225,255,${0.55 * cry})`; g.fillRect(x - 70, y + ry * 0.35, 140, ry); }   // wet eyes
      // eyelids (skin) closing from above/below, tilted by emotion
      g.fillStyle = skinC; const tilt = s * (0.45 * ang - 0.5 * sad - 0.3 * fear - 0.3 * cry);
      g.save(); g.translate(x, y); g.rotate(tilt); g.fillRect(-80, -ry - 2, 160, ry * 2 * upLid + 2); g.restore();
      g.fillRect(x - 80, y + ry - ry * 2 * loLid, 160, ry * 2 * loLid + 4);
      g.restore();
      g.strokeStyle = '#221612'; g.lineWidth = female ? 6 : 4.5; g.save(); g.translate(x, y); g.rotate(tilt); g.beginPath(); g.ellipse(0, -ry * 2 * upLid * 0.5, er * 1.2, ry * (1 - upLid), 0, Math.PI * 1.05, Math.PI * 1.95); g.stroke(); g.restore();
      if (female) { g.lineWidth = 3; for (const k of [0.15, 0.32]) { const a2 = Math.PI * (s > 0 ? 1.95 - k * 0.3 : 1.05 + k * 0.3); g.beginPath(); g.moveTo(x + Math.cos(a2) * er * 1.2, y + Math.sin(a2) * ry); g.lineTo(x + Math.cos(a2) * er * 1.6, y + Math.sin(a2) * ry * 1.25 - 6); g.stroke(); } }
      // brows: inner end up (sad/fear), down (angry), whole brow up (surprise)
      const by = y - er * 1.7 - (st.brow || 0) * 3 - 26 * sur - 14 * fear + 12 * ang, inner = (-34 * ang + 32 * sad + 26 * fear + 18 * pain + 20 * cry), rot = s * (st.browRot || 0);
      g.save(); g.translate(x, by); g.rotate(rot); g.fillStyle = P.hair; g.beginPath(); const w = er * 1.25, hh = female ? 4.5 : 7.5;
      g.moveTo(s * w, 0); g.quadraticCurveTo(0, -hh * 2 - 2 * sur, -s * w, -inner * 0.6); g.lineTo(-s * w, -inner * 0.6 + hh * 1.4); g.quadraticCurveTo(0, -hh * 0.4, s * w, hh * 1.2); g.closePath(); g.fill(); g.restore();
      if (ang > 0.4) { g.strokeStyle = 'rgba(60,30,20,.4)'; g.lineWidth = 2.5; g.beginPath(); g.moveTo(256 + s * 10, by + 4); g.lineTo(256 + s * 16, by + 18); g.stroke(); }   // frown line
      if (cry > 0.3) { g.fillStyle = 'rgba(150,200,255,.95)'; const d = (st.t || 0) * 70 % 110; g.beginPath(); g.ellipse(x + s * 8, y + ry + 14 + d, 8, 13, 0, 0, 7); g.fill(); g.fillStyle = 'rgba(150,200,255,.55)'; g.fillRect(x + s * 8 - 4, y + ry, 8, 14 + d); } }
    // nose shadow, cheeks (blush with joy/crying), sweat drop (fear)
    g.fillStyle = 'rgba(80,40,30,.22)'; g.beginPath(); g.ellipse(256, 318, 13, 7, 0, 0, 7); g.fill();
    const bl2 = (female ? 0.35 : 0.12) + 0.3 * hap + 0.35 * cry; for (const s of [-1, 1]) { const gr = g.createRadialGradient(256 + s * 92, 305, 2, 256 + s * 92, 305, 34); gr.addColorStop(0, `rgba(230,110,110,${bl2})`); gr.addColorStop(1, 'rgba(230,110,110,0)'); g.fillStyle = gr; g.fillRect(256 + s * 92 - 40, 265, 80, 80); }
    if (fear > 0.4) { g.fillStyle = 'rgba(190,225,255,.8)'; g.beginPath(); g.moveTo(352, 150); g.quadraticCurveTo(366, 178, 352, 186); g.quadraticCurveTo(338, 178, 352, 150); g.fill(); }
    // mouth: lip-sync shape, corners bent by emotion
    g.save(); g.translate(256, 372); g.scale(1.22, 1.22); g.translate(-256, -372); const m = st.mouth || 'X', mx = 256, my = 370, lip = female ? '#a8504c' : '#6e3a30', curve = 30 * hap - 26 * sad - 14 * cry - 10 * ang + (st.smile || 0) * 6, wide = 1 + 0.35 * hap + 0.2 * fear - 0.15 * sad + 0.15 * cry;
    const ov = (rx, ry, oy = 0) => { rx *= wide; g.fillStyle = '#3a1418'; g.beginPath(); g.moveTo(mx - rx, my + oy - curve * 0.4); g.quadraticCurveTo(mx, my + oy - ry * 1.15, mx + rx, my + oy - curve * 0.4); g.quadraticCurveTo(mx, my + oy + ry * 1.15 + curve * 0.3, mx - rx, my + oy - curve * 0.4); g.fill(); g.strokeStyle = lip; g.lineWidth = female ? 6 : 4; g.stroke(); };
    const teeth = (w, y, h) => { g.fillStyle = '#f2eee6'; g.fillRect(mx - w / 2 * wide, my + y, w * wide, h); };
    const tongue = (y) => { g.fillStyle = '#b75a5a'; g.beginPath(); g.ellipse(mx, my + y, 15, 7, 0, 0, 7); g.fill(); };
    g.lineCap = 'round';
    switch (m) {
      case 'A': g.strokeStyle = lip; g.lineWidth = female ? 7 : 5; g.beginPath(); g.moveTo(mx - 24 * wide, my - curve * 0.5); g.quadraticCurveTo(mx, my + curve * 0.2, mx + 24 * wide, my - curve * 0.5); g.stroke(); break;
      case 'B': ov(24, 7, 2); teeth(32, -4, 5); break;
      case 'C': ov(23, 12, 4); teeth(30, -6, 5); break;
      case 'D': ov(25, 20, 8); tongue(18); teeth(30, -10, 6); break;
      case 'E': ov(15, 13, 4); break;
      case 'F': ov(10, 10, 2); break;
      case 'G': ov(21, 6, 2); teeth(30, -6, 8); break;
      case 'H': ov(20, 14, 4); tongue(2); break;
      case 'grit': ov(27, 7, 2); teeth(46, -5, 9); break;
      default: { const cv = curve + (st.smile || 0.4) * 4; g.strokeStyle = lip; g.lineWidth = female ? 6 : 4.5; g.beginPath(); g.moveTo(mx - 25 * wide, my - cv * 0.5); g.quadraticCurveTo(mx, my + cv * 0.6, mx + 25 * wide, my - cv * 0.5); g.stroke(); } }
    g.restore(); tex.needsUpdate = true; };
  return { canvas: c, tex, draw };
}

// ---------------- build ----------------
export function buildCharacter(key, palette) {
  const D = DEF[key], pal = palette[key], F = D.sex === 'f', H = D.h, s = H / 1.75;
  const P = { skin: pal.head[1], skinS: pal.head[0], hair: pal.hair_front[1] || pal.hair_back[0], top: pal.torso[1], topS: pal.torso[0], sleeve: (pal.upper_arm[1] || pal.torso[1]), pants: pal.thigh[1], shoe: pal.foot[1], iris: pal.eye_L[1] || '#3b2616' };
  if (key === 'ryan') P.top = '#2f5d9e';
  const M = { skin: mat(P.skin, 0.62), top: mat(P.top, 0.82), sleeve: mat(P.sleeve, 0.82), pants: mat(P.pants, 0.85), shoe: mat(P.shoe, 0.55), hair: mat(P.hair, 0.6), dark: mat('#1b1816', 0.6), metal: mat('#9aa0a6', 0.3, { metalness: 0.8 }) };
  const root = new THREE.Group(); root.name = key; const J = {};
  // proportions (fit men: broad shoulders, narrow waist; women: smaller frame, softer shape, slightly larger head)
  const legL = 0.47 * H, thighL = 0.245 * H, shinL = 0.205 * H, torsoL = 0.3 * H, headR = (F ? 0.08 : 0.075) * H;
  const shW = (F ? 0.1 : 0.112 + 0.01 * D.fit) * H, hipW = (F ? 0.085 : 0.07) * H, waist = (F ? 0.06 : 0.063 + 0.002 * D.fit) * H, chest = (F ? 0.078 : 0.088 + 0.01 * D.fit) * H;
  J.hips = bone('hips', root, 0, legL, 0); J.spine = bone('spine', J.hips, 0, 0.05 * H, 0); J.chest = bone('chest', J.spine, 0, 0.12 * H, 0);
  J.neck = bone('neck', J.chest, 0, torsoL - 0.175 * H, 0.0); J.head = bone('head', J.neck, 0, 0.035 * H, 0.008);
  // pelvis / trousers top
  { const g = new THREE.SphereGeometry(1, 20, 14); const m = new THREE.Mesh(g, M.pants); m.scale.set(hipW * 1.05, 0.05 * H, hipW * 0.66); m.position.set(0, 0.018 * H, -0.006 * H); m.castShadow = true; J.hips.add(m); }
  // torso: lathe profile from waist to shoulders, flattened front-to-back; jacket colour
  { const pts = [], n = 18; for (let i = 0; i <= n; i++) { const u = i / n; let r;
      r = u < 0.12 ? lerp(hipW * 0.95, waist, smooth(u / 0.12)) : u < 0.62 ? lerp(waist, chest, smooth((u - 0.12) / 0.5)) : u < 0.86 ? chest * (1 + (F ? 0.03 * Math.sin((u - 0.62) / 0.24 * Math.PI) : 0)) : lerp(chest, 0.04 * H, smooth((u - 0.86) / 0.14));
      pts.push(new THREE.Vector2(r, -0.02 * H + u * (torsoL - 0.02 * H))); }
    pts.unshift(new THREE.Vector2(0.001, -0.02 * H)); pts.push(new THREE.Vector2(0.001, torsoL));
    const g = new THREE.LatheGeometry(pts, 26); g.computeVertexNormals(); const m = new THREE.Mesh(g, M.top); m.scale.set(1.12, 1, 0.6); m.position.y = -0.05 * H; m.castShadow = m.receiveShadow = true; J.spine.add(m);
    // shoulder mass + collar
    { const yr = (F ? 0.026 : 0.031 + 0.004 * D.fit) * H * 0.98, yx = shW - 0.02 * H; const yk = limb(yr, yr, 2 * yx, M.top, 18); yk.rotation.z = Math.PI / 2; yk.position.set(-yx, torsoL - 0.2 * H - yr * 0.12, 0); yk.scale.z = 0.88; J.chest.add(yk); }
    const col_ = limb((F ? 0.036 : 0.044) * H, (F ? 0.04 : 0.048) * H, 0.032 * H, M.top, 20); col_.scale.set(1, 1, 0.95); col_.position.y = torsoL - 0.162 * H; J.chest.add(col_);
    if (D.hood) { const hd = new THREE.Mesh(new THREE.SphereGeometry(0.07 * H, 18, 12), mat(shadeC(P.top, -0.12).getStyle(), 0.85)); hd.scale.set(1.0, 0.62, 0.32); hd.rotation.x = -0.35; hd.position.set(0, torsoL - 0.205 * H, -chest * 0.5); J.chest.add(hd); }
    // zipper / placket line
    const zp = new THREE.Mesh(new THREE.BoxGeometry(0.006 * H, torsoL * 0.8, 0.004), mat(shadeC(P.top, -0.4).getStyle())); zp.position.set(0, 0.06 * H, chest * 0.62 + 0.002); J.spine.add(zp);
  }
  // neck + head
  { const nk = limb((F ? 0.025 : 0.031) * H, (F ? 0.026 : 0.033) * H, 0.045 * H, M.skin); nk.position.set(0, 0.045 * H, 0); J.neck.add(nk); }
  { const hg = new THREE.SphereGeometry(headR, 32, 24); const hm = new THREE.Mesh(hg, M.skin); hm.scale.set(F ? 0.9 : 0.88, 1.06, 0.98); hm.position.y = headR * 0.9; hm.castShadow = true; J.head.add(hm);
    // jaw / chin softness
    const jaw = new THREE.Mesh(new THREE.SphereGeometry(headR * 0.72, 20, 14), M.skin); jaw.scale.set(F ? 0.88 : 0.98, 0.78, 0.86); jaw.position.set(0, headR * 0.5, -headR * 0.02); J.head.add(jaw);
    for (const sx of [-1, 1]) { const ear = new THREE.Mesh(new THREE.SphereGeometry(headR * 0.2, 10, 8), M.skin); ear.scale.set(0.45, 1, 0.8); ear.position.set(sx * headR * 0.9, headR * 0.9, -headR * 0.05); J.head.add(ear); }
    const nose = new THREE.Mesh(new THREE.SphereGeometry(headR * 0.14, 12, 10), M.skin); nose.scale.set(0.8, 1.1, 1.1); nose.position.set(0, headR * 0.82, headR * 0.98); J.head.add(nose);
    // face shell (painted, animated)
    const face = makeFace(P, F); const fg = new THREE.SphereGeometry(headR * 1.014, 40, 30, Math.PI * 0.5 - 1.05, 2.1, Math.PI * 0.2, Math.PI * 0.56);
    const fm = new THREE.Mesh(fg, new THREE.MeshStandardMaterial({ map: face.tex, transparent: true, roughness: 0.6, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 }));
    fm.scale.copy(hm.scale); fm.position.copy(hm.position); fm.rotation.y = -Math.PI / 2 + Math.PI / 2; J.head.add(fm); root.userData.face = face;
    buildHair(D, J.head, headR, hm, M, P, F);
    if (D.acc.includes('beard')) { const b = new THREE.Mesh(new THREE.SphereGeometry(headR * 0.8, 20, 14, 0, Math.PI * 2, Math.PI * 0.45, Math.PI * 0.55), M.hair); b.scale.set(0.95, 0.95, 1.0); b.position.set(0, headR * 0.62, headR * 0.12); J.head.add(b); }
    if (D.acc.includes('glasses')) { const gm = mat('#141414', 0.3); for (const sx of [-1, 1]) { const r = new THREE.Mesh(new THREE.TorusGeometry(headR * 0.24, headR * 0.03, 8, 20), gm); r.position.set(sx * headR * 0.3, headR * 1.0, headR * 0.98); J.head.add(r); }
      const br = new THREE.Mesh(new THREE.BoxGeometry(headR * 0.16, headR * 0.03, headR * 0.03), gm); br.position.set(0, headR * 1.02, headR * 1.0); J.head.add(br); }
    if (D.acc.includes('headphones')) { const hm2 = mat('#34353d', 0.4); const band = new THREE.Mesh(new THREE.TorusGeometry(headR * 1.05, headR * 0.06, 8, 24, Math.PI), hm2); band.position.y = headR * 0.95; band.rotation.z = 0; J.neck.add(band); band.position.set(0, 0.055 * H + headR * 0.2, 0);
      for (const sx of [-1, 1]) { const cup = new THREE.Mesh(new THREE.CylinderGeometry(headR * 0.3, headR * 0.3, headR * 0.15, 16), hm2); cup.rotation.z = Math.PI / 2; cup.position.set(sx * headR * 1.0, 0.055 * H + headR * 0.2, 0); J.neck.add(cup);
        const led = new THREE.Mesh(new THREE.CircleGeometry(headR * 0.08, 10), new THREE.MeshBasicMaterial({ color: 0x39d0ff })); led.position.set(sx * headR * 1.08, 0.055 * H + headR * 0.2, 0); led.rotation.y = sx * Math.PI / 2; J.neck.add(led); } }
  }
  // arms
  for (const [side, sx] of [['L', 1], ['R', -1]]) {
    const sh = bone('shoulder' + side, J.chest, sx * (shW - 0.02 * H), torsoL - 0.2 * H, 0); const ua = bone('upperArm' + side, sh, 0, 0, 0);
    const uaL = 0.17 * H, faL = 0.15 * H, armR = (F ? 0.026 : 0.031 + 0.004 * D.fit) * H;
    ua.add(limb(armR * 1.05, armR * 0.85, uaL, D.shortSleeve ? M.top : M.sleeve));
    if (D.shortSleeve) { const arm = limb(armR * 0.85, armR * 0.78, uaL * 0.55, M.skin); arm.position.y = -uaL * 0.45; ua.add(arm); }
    const fa = bone('foreArm' + side, ua, 0, -uaL, 0); fa.add(limb(armR * 0.85, armR * 0.62, faL, D.shortSleeve ? M.skin : M.sleeve));
    if (!D.shortSleeve) { const cuff = limb(armR * 0.7, armR * 0.6, 0.02 * H, M.skin); cuff.position.y = -faL + 0.01 * H; fa.add(cuff); }
    const hand = bone('hand' + side, fa, 0, -faL, 0);
    { // palm + 4 two-segment fingers + thumb (each segment is a joint we can curl)
      const pw = armR * 1.55, pl = armR * 1.6, pd = armR * 0.62;
      const palm = new THREE.Mesh(new THREE.BoxGeometry(pw, pl, pd, 2, 2, 2), M.skin); { const g = palm.geometry, q = g.attributes.position; for (let i = 0; i < q.count; i++) { const y = q.getY(i); q.setZ(i, q.getZ(i) * (1 - 0.2 * Math.abs(y) / pl)); } g.computeVertexNormals(); }
      const pf = new THREE.Group(); pf.rotation.y = -sx * Math.PI / 2; hand.add(pf); hand.userData.palmFrame = pf;
      palm.position.y = -pl * 0.55; palm.castShadow = true; pf.add(palm); const fingers = [];
      for (let f = 0; f < 4; f++) { const fx = (f - 1.5) * pw * 0.25 * sx, L1 = armR * (f === 1 || f === 2 ? 0.78 : 0.66), r = armR * 0.17;
        const k1 = bone('f' + f + 'a', pf, fx, -pl * 1.05, 0), m1 = limb(r, r * 0.9, L1, M.skin, 8); k1.add(m1);
        const k2 = bone('f' + f + 'b', k1, 0, -L1, 0), m2 = limb(r * 0.9, r * 0.75, L1 * 0.82, M.skin, 8); k2.add(m2); fingers.push([k1, k2]); }
      const t1 = bone('thumbA', pf, sx * pw * 0.5, -pl * 0.25, pd * 0.35); t1.rotation.set(0.5, 0, -sx * 0.7); t1.add(limb(armR * 0.2, armR * 0.18, armR * 0.6, M.skin, 8));
      const t2 = bone('thumbB', t1, 0, -armR * 0.6, 0); t2.add(limb(armR * 0.18, armR * 0.15, armR * 0.5, M.skin, 8));
      hand.userData.fingers = fingers; hand.userData.thumb = [t1, t2]; hand.userData.sx = sx; }
    J['shoulder' + side] = sh; J['upperArm' + side] = ua; J['foreArm' + side] = fa; J['hand' + side] = hand;
  }
  // legs
  for (const [side, sx] of [['L', 1], ['R', -1]]) {
    const th = bone('thigh' + side, J.hips, sx * hipW * 0.55, -0.02 * H, 0), lr = (F ? 0.05 : 0.055 + 0.005 * D.fit) * H;
    th.add(limb(lr, lr * 0.72, thighL, M.pants)); const sn = bone('shin' + side, th, 0, -thighL, 0); sn.add(limb(lr * 0.72, lr * 0.5, shinL, M.pants));
    const ft = bone('foot' + side, sn, 0, -shinL, 0);
    { const sg = new THREE.BoxGeometry(lr * 1.05, 0.05 * H, 0.15 * H, 2, 2, 4); const p = sg.attributes.position; for (let i = 0; i < p.count; i++) { const z = p.getZ(i), y = p.getY(i); p.setY(i, y + (z > 0.03 * H ? -Math.max(0, y) * 0.5 : 0)); p.setX(i, p.getX(i) * (z > 0.05 * H ? 0.8 : 1)); } sg.computeVertexNormals();
      const shoe = new THREE.Mesh(sg, M.shoe); shoe.position.set(0, -0.012 * H, 0.04 * H); shoe.castShadow = true; ft.add(shoe);
      const sole = new THREE.Mesh(new THREE.BoxGeometry(lr * 1.1, 0.012 * H, 0.155 * H), M.dark); sole.position.set(0, -0.038 * H, 0.04 * H); ft.add(sole); }
    J['thigh' + side] = th; J['shin' + side] = sn; J['foot' + side] = ft;
  }
  // accessories
  if (D.acc.includes('backpack')) { const bp = new THREE.Mesh(new THREE.BoxGeometry(0.2 * H, 0.24 * H, 0.09 * H), mat('#4c4a32', 0.9)); bp.position.set(0, 0.05 * H, -chest * 0.62 - 0.045 * H); bp.castShadow = true; J.chest.add(bp);
    const rope = new THREE.Mesh(new THREE.TorusGeometry(0.045 * H, 0.009 * H, 8, 20), mat('#b8a27a', 0.9)); rope.position.set(0.07 * H, -0.02 * H, -chest * 0.62 - 0.1 * H); J.chest.add(rope); }
  if (D.acc.includes('toolbelt') || D.acc.includes('belt')) { const bt = new THREE.Mesh(new THREE.TorusGeometry(hipW * 1.05, 0.012 * H, 6, 24), mat(D.acc.includes('belt') ? '#151515' : '#5a3b24', 0.6)); bt.rotation.x = Math.PI / 2; bt.scale.set(1.1, 0.82, 1); bt.position.y = 0.035 * H; J.hips.add(bt);
    if (D.acc.includes('toolbelt')) for (const x of [-1, 1]) { const pouch = new THREE.Mesh(new THREE.BoxGeometry(0.04 * H, 0.05 * H, 0.03 * H), mat('#6b4a2e', 0.8)); pouch.position.set(x * hipW * 1.0, 0.0, hipW * 0.5); J.hips.add(pouch); } }
  if (D.acc.includes('stethoscope')) { const sm = mat('#2b2d31', 0.5), y0 = torsoL - 0.19 * H;
    const loop = new THREE.Mesh(new THREE.TorusGeometry(0.045 * H, 0.0045 * H, 6, 24, Math.PI), sm); loop.rotation.set(-1.2, 0, 0); loop.position.set(0, y0, -0.005 * H); J.chest.add(loop);
    for (const sg of [-1, 1]) { const tb = limb(0.0045 * H, 0.0045 * H, 0.15 * H, sm, 6); tb.position.set(sg * 0.045 * H, y0, chest * 0.35); tb.rotation.set(-0.35, 0, sg * -0.1); J.chest.add(tb); }
    const disk = new THREE.Mesh(new THREE.CylinderGeometry(0.014 * H, 0.014 * H, 0.006 * H, 16), mat('#c8ccd2', 0.3, { metalness: 0.7 })); disk.rotation.x = Math.PI / 2; disk.position.set(0.045 * H, y0 - 0.15 * H, chest * 0.62); J.chest.add(disk); }
  if (D.acc.includes('camera')) { const cam = new THREE.Mesh(new THREE.BoxGeometry(0.07 * H, 0.045 * H, 0.04 * H), mat('#2a2c31', 0.4)); cam.position.set(0.02 * H, 0.03 * H, chest * 0.64 + 0.02 * H); J.chest.add(cam);
    const lens = new THREE.Mesh(new THREE.CylinderGeometry(0.014 * H, 0.014 * H, 0.03 * H, 16), mat('#111', 0.2)); lens.rotation.x = Math.PI / 2; lens.position.set(0.02 * H, 0.03 * H, chest * 0.64 + 0.05 * H); J.chest.add(lens); }
  if (D.acc.includes('radio')) { const r = new THREE.Mesh(new THREE.BoxGeometry(0.03 * H, 0.05 * H, 0.018 * H), mat('#2b2e33', 0.5)); r.position.set(-0.05 * H, 0.08 * H, chest * 0.64 + 0.01 * H); J.chest.add(r);
    const led = new THREE.Mesh(new THREE.SphereGeometry(0.004 * H), new THREE.MeshBasicMaterial({ color: 0x3be37a })); led.position.set(-0.05 * H, 0.1 * H, chest * 0.64 + 0.02 * H); J.chest.add(led); root.userData.radioLed = led; }
  if (D.acc.includes('badge')) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.025 * H, 0.018 * H, 0.004 * H), mat('#d9b44a', 0.3, { metalness: 0.8 })); b.position.set(-0.05 * H, 0.1 * H, chest * 0.64); J.chest.add(b); }
  if (D.acc.includes('patch')) { const p = new THREE.Mesh(new THREE.CircleGeometry(0.018 * H, 16), mat('#d8c27a', 0.6)); p.position.set(0, -0.02 * H, 0.035 * H); p.rotation.y = Math.PI / 2; J.upperArmL.add(p); }
  if (D.acc.includes('hammer')) { const h = new THREE.Mesh(new THREE.BoxGeometry(0.012 * H, 0.12 * H, 0.012 * H), mat('#6b4a2e', 0.8)); h.position.set(-hipW * 1.1, -0.03 * H, 0); J.hips.add(h); }
  if (D.acc.includes('lanyard')) { const l = new THREE.Mesh(new THREE.TorusGeometry(0.05 * H, 0.003 * H, 6, 20, Math.PI), mat('#1f8a8a', 0.6)); l.rotation.set(0.2, 0, Math.PI); l.position.set(0, torsoL - 0.2 * H, chest * 0.55); J.chest.add(l); }
  root.userData.J = J; root.userData.def = D; root.userData.H = H; root.userData.legL = legL; root.userData.thighL = thighL; root.userData.shinL = shinL;
  root.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return root;
}
const lerp = (a, b, t) => a + (b - a) * t, smooth = x => x * x * (3 - 2 * x), clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));

function buildHair(D, head, R, hm, M, P, F) {
  const cap = (scale, pos, thetaLen = Math.PI * 0.55, m = M.hair, segs = 28) => { const g = new THREE.SphereGeometry(R * 1.06, segs, 18, 0, Math.PI * 2, 0, Math.min(thetaLen, Math.PI * 0.5)); const o = new THREE.Mesh(g, m); o.scale.set(...scale); o.position.set(pos[0], pos[1] - R * 0.05, pos[2] - R * 0.06); o.rotation.x = opts_tilt; o.castShadow = true; head.add(o); return o; };
  const hy = hm.position.y, sx = hm.scale.x, sz = hm.scale.z; const opts_tilt = ['buzz', 'saltpep'].includes(D.hair) ? -0.27 : ['neat', 'short'].includes(D.hair) ? -0.3 : -0.42;
  const tufts = (n, r, spread, seed, yb = 0.35) => { for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2 + seed, el = yb + ((i * 7) % 5) / 10; const t = new THREE.Mesh(new THREE.SphereGeometry(R * r, 10, 8), M.hair);
    t.position.set(Math.cos(a) * R * spread * Math.cos(el) * sx, hy + R * 0.25 + Math.sin(el) * R * 0.85, Math.min(R * 0.45, Math.sin(a) * R * spread * Math.cos(el) * sz) - R * 0.15); t.castShadow = true; head.add(t); } };
  // fringe: short tapered locks falling over the forehead; side locks: strands in front of the ears
  const fringe = (n, len) => { for (let i = 0; i < n; i++) { const u = (i / (n - 1) - 0.5), l = limb(R * 0.16, R * 0.05, R * len * (0.8 + 0.4 * Math.abs(Math.sin(i * 2.3))), M.hair, 8);
      l.position.set(u * R * 1.25 * sx, hy + R * 0.92, R * 0.62 * sz + Math.cos(u * 2) * R * 0.08); l.rotation.set(-0.75 - 0.15 * Math.cos(u * 3), 0, -u * 0.7); l.castShadow = true; head.add(l); } };
  const sideLocks = (len) => { for (const sgn of [-1, 1]) { const l = limb(R * 0.2, R * 0.08, R * len, M.hair, 8); l.position.set(sgn * R * 0.92 * sx, hy + R * 0.55, R * 0.35); l.rotation.set(-0.15, 0, sgn * 0.12); head.add(l); } };
  switch (D.hair) {
    case 'short': cap([sx * 1.0, 1.02, sz * 1.02], [0, hy + R * 0.12, -R * 0.03]); tufts(9, 0.3, 0.92, 0.3, 0.45); fringe(5, 0.55); break;
    case 'messy': cap([sx * 1.04, 1.0, sz * 1.04], [0, hy + R * 0.1, -R * 0.02]); tufts(14, 0.32, 0.95, 0.7, 0.35); fringe(6, 0.7); break;
    case 'neat': cap([sx * 1.02, 1.02, sz * 1.03], [0, hy + R * 0.06, -R * 0.02]); fringe(5, 0.3); break;
    case 'buzz': cap([sx * 1.01, 1.1, sz * 1.02], [0, hy + R * 0.03, R * 0.05], Math.PI * 0.5); break;
    case 'saltpep': { const m = mat('#7a7672', 0.7); cap([sx * 1.03, 1.1, sz * 1.04], [0, hy + R * 0.03, R * 0.05], Math.PI * 0.55, m); break; }
    case 'curly': cap([sx * 1.1, 1.05, sz * 1.08], [0, hy + R * 0.16, -R * 0.02]); tufts(26, 0.36, 1.02, 0.1, 0.15); break;
    case 'bob': { cap([sx * 1.08, 1.0, sz * 1.06], [0, hy + R * 0.08, -R * 0.04], Math.PI * 0.62); fringe(7, 0.22); const g = new THREE.CylinderGeometry(R * 1.02, R * 1.12, R * 0.9, 28, 1, true, Math.PI * 0.25, Math.PI * 1.5); const o = new THREE.Mesh(g, M.hair); o.material.side = THREE.DoubleSide; o.scale.set(sx, 1, sz); o.position.set(0, hy - R * 0.1, -R * 0.05); head.add(o); break; }
    case 'ponytail': { cap([sx * 1.04, 1.03, sz * 1.04], [0, hy + R * 0.1, -R * 0.03], Math.PI * 0.6); fringe(4, 0.5); sideLocks(0.9); const tail = limb(R * 0.28, R * 0.14, R * 1.9, M.hair, 12); tail.position.set(0, hy + R * 0.9, -R * 0.95); tail.rotation.x = 0.35; head.add(tail); head.userData.tail = tail;
      const tie = new THREE.Mesh(new THREE.TorusGeometry(R * 0.2, R * 0.06, 6, 14), mat('#c7362f', 0.6)); tie.position.set(0, hy + R * 0.9, -R * 0.95); tie.rotation.x = 0.35 + Math.PI / 2; head.add(tie); break; }
    case 'wavy': { cap([sx * 1.08, 1.0, sz * 1.06], [0, hy + R * 0.08, -R * 0.04], Math.PI * 0.62); for (const s of [-1, 1]) for (let k = 0; k < 3; k++) { const l = limb(R * 0.34, R * 0.22, R * 1.6, M.hair, 10); l.position.set(s * R * (0.72 + k * 0.08), hy + R * 0.2, -R * (0.1 + k * 0.32)); l.rotation.z = s * 0.12; head.add(l); }
      const back = limb(R * 0.9, R * 0.6, R * 1.5, M.hair, 18); back.scale.z = 0.5; back.position.set(0, hy + R * 0.3, -R * 0.6); head.add(back); break; }
    case 'bun': { cap([sx * 1.03, 1.03, sz * 1.03], [0, hy + R * 0.1, -R * 0.03], Math.PI * 0.6); sideLocks(0.7); const b = new THREE.Mesh(new THREE.SphereGeometry(R * 0.38, 14, 10), M.hair); b.position.set(0, hy - R * 0.05, -R * 1.02); head.add(b); break; }
  }
}

// ---------------- motion (applies a pose to the joints) ----------------
const TAU = Math.PI * 2;
export function hashf(n) { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }
function eyes(t, seed) { const per = 0.9 + hashf(seed + 1) * 0.8, seg = Math.floor((t + seed) / per), tt = (t + seed) % per, j = clamp(tt / 0.06);
  const a = [hashf(seg * 3.1 + seed) - 0.5, hashf(seg * 7.7 + seed) - 0.5], b = [hashf((seg - 1) * 3.1 + seed) - 0.5, hashf((seg - 1) * 7.7 + seed) - 0.5];
  const bp = 2.6 + hashf(seed + 9) * 2.4, bt = (t + seed * 1.3) % bp, bi = Math.floor((t + seed * 1.3) / bp), bk = x => x >= 0 && x < 0.15 ? Math.sin(x / 0.15 * Math.PI) : 0;
  let blink = bk(bt); if (hashf(bi + seed) > 0.75) blink = Math.max(blink, bk(bt - 0.22));
  return { look: [lerp(b[0], a[0], j) * 1.4, lerp(b[1], a[1], j) * 0.8], blink }; }
// pose: { hips:[x,y,z], hipY, spine:[...], chest, neck, head, thighL.. (x = forward swing), shinL (knee bend +), footL, upperArmL:[x,y,z], foreArmL, handL, face:{...} }
export function applyPose(ch, P) { const J = ch.userData.J;
  const set = (b, r) => { if (!r) { b.rotation.set(0, 0, 0); return; } b.rotation.set(r[0] || 0, r[1] || 0, r[2] || 0); };
  J.hips.position.y = ch.userData.legL + (P.hipY || 0); J.hips.position.x = P.hipX || 0; J.hips.position.z = P.hipZ || 0;
  for (const k of ['hips', 'spine', 'chest', 'neck', 'head', 'thighL', 'thighR', 'shinL', 'shinR', 'footL', 'footR', 'shoulderL', 'shoulderR', 'upperArmL', 'upperArmR', 'foreArmL', 'foreArmR', 'handL', 'handR']) set(J[k], P[k]);
  const tail = J.head.userData.tail; if (tail) tail.rotation.x = 0.35 + (P.tailSwing || 0);
  const f = ch.userData.face; if (f && P.face) { const key = JSON.stringify(P.face); if (key !== ch.userData.lastFace) { f.draw(P.face); ch.userData.lastFace = key; } }
}
// rest arms hang slightly away from the body (z-rotation), L side +x
const REST = { upperArmL: [0, 0, 0.09], upperArmR: [0, 0, -0.09], foreArmL: [-0.12, 0, 0], foreArmR: [-0.12, 0, 0] };
export function idle(t, seed, o = {}) { const br = Math.sin(t * TAU / 3.8 + seed), ws = Math.tanh(Math.sin(t * TAU / 6 + seed * 5) * 3), e = eyes(t, seed);
  return { hipY: -0.004 + br * 0.002, hipX: ws * 0.025, hips: [0, ws * 0.05, ws * 0.05], spine: [br * 0.012, 0, -ws * 0.03], chest: [br * 0.015, 0, -ws * 0.02], neck: [0, Math.sin(t * 0.37 + seed) * 0.08, 0], head: [Math.sin(t * 0.5 + seed) * 0.03, Math.sin(t * 0.23 + seed) * 0.06, ws * 0.02],
    thighL: [0, 0, -ws * 0.05 + 0.02], thighR: [ws > 0 ? -0.12 : 0, 0, -ws * 0.05 - 0.02], shinL: [ws < 0 ? 0.2 : 0.01, 0, 0], shinR: [ws > 0 ? 0.2 : 0.01, 0, 0], footL: [ws < 0 ? -0.1 : 0, 0, 0], footR: [ws > 0 ? -0.1 : 0, 0, 0],
    upperArmL: [0.03 + br * 0.01, 0, 0.1 + ws * 0.04], upperArmR: [0.03 + br * 0.01, 0, -0.1 + ws * 0.04], foreArmL: [-0.18, 0, 0], foreArmR: [-0.18, 0, 0], handL: [0, 0, 0.05], handR: [0, 0, -0.05],
    face: { look: e.look, blink: +e.blink.toFixed(2), mouth: 'X' }, tailSwing: ws * 0.05, ...o }; }
// real sagittal-plane walk: hip flex/extension, knee flex in swing + loading response, ankle roll, pelvis rotation + drop, arm swing with elbow lag
export function walk(t, seed, o = {}) { const ph = o.phase ?? t * TAU * 0.95, s = Math.sin(ph), c = Math.cos(ph), e = eyes(t, seed), amp = o.amp ?? 1;
  const leg = (p) => { const sp = Math.sin(p), swing = Math.max(0, Math.sin(p - 0.25)), push = Math.max(0, -Math.cos(p + 0.6));
    return { thigh: [-0.42 * sp * amp, 0, 0], shin: [(0.95 * swing * swing + 0.12 * Math.max(0, Math.cos(p)) ) * amp, 0, 0], foot: [(-0.25 * swing + 0.35 * push * 0.6 - 0.1 * Math.max(0, Math.cos(p))) * amp, 0, 0] }; };
  const L = leg(ph), R = leg(ph + Math.PI);
  return { hipY: (-0.012 - 0.018 * Math.cos(2 * ph)) * amp, hipX: 0.022 * s * amp, hips: [0.04 * amp, 0.12 * s * amp, 0.04 * s * amp], spine: [0.02, -0.07 * s * amp, -0.02 * s * amp], chest: [0.03, -0.1 * s * amp, 0], neck: [0, 0.08 * s * amp, 0], head: [-0.03, 0.04 * s * amp, 0],
    thighL: L.thigh, shinL: L.shin, footL: L.foot, thighR: R.thigh, shinR: R.shin, footR: R.foot,
    upperArmL: [0.38 * Math.sin(ph - 0.25) * amp, 0, 0.1], upperArmR: [-0.38 * Math.sin(ph - 0.25) * amp, 0, -0.1], foreArmL: [-0.25 - 0.3 * Math.max(0, Math.sin(ph - 0.6)) * amp, 0, 0], foreArmR: [-0.25 - 0.3 * Math.max(0, -Math.sin(ph - 0.6)) * amp, 0, 0],
    handL: [0, 0, 0.05], handR: [0, 0, -0.05], face: { look: e.look, blink: +e.blink.toFixed(2), mouth: 'X' }, tailSwing: 0.18 * Math.sin(2 * ph - 1), ...o }; }
export function run(t, seed, o = {}) { const ph = o.phase ?? t * TAU * 1.45, s = Math.sin(ph), e = eyes(t, seed);
  const leg = (p) => { const sp = Math.sin(p), swing = Math.max(0, Math.sin(p - 0.35)); return { thigh: [-0.85 * sp - 0.15, 0, 0], shin: [0.35 + 1.55 * swing * swing, 0, 0], foot: [-0.3 * swing + 0.25 * Math.max(0, -Math.cos(p + 0.5)), 0, 0] }; };
  const L = leg(ph), R = leg(ph + Math.PI), air = Math.max(0, -Math.cos(2 * ph));
  return { hipY: -0.06 + 0.05 * air, hipX: 0.015 * s, hips: [0.22, 0.16 * s, 0.03 * s], spine: [0.1, -0.1 * s, 0], chest: [0.08, -0.14 * s, 0], neck: [-0.15, 0.06 * s, 0], head: [-0.12, 0, 0],
    thighL: L.thigh, shinL: L.shin, footL: L.foot, thighR: R.thigh, shinR: R.shin, footR: R.foot,
    upperArmL: [0.85 * Math.sin(ph - 0.2), 0, 0.12], upperArmR: [-0.85 * Math.sin(ph - 0.2), 0, -0.12], foreArmL: [-1.45 - 0.2 * Math.sin(ph - 0.4), 0, 0], foreArmR: [-1.45 + 0.2 * Math.sin(ph - 0.4), 0, 0],
    handL: [0, 0, 0], handR: [0, 0, 0], face: { look: [0, 0], blink: +e.blink.toFixed(2), mouth: Math.floor(t * 4.3) % 2 ? 'C' : 'E', brow: 2 }, tailSwing: 0.45 * Math.sin(2 * ph - 1.2), airborne: air, ...o }; }
export function blendPose(a, b, w) { if (w <= 0) return a; if (w >= 1) return b; const P = { ...a };
  for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) { const x = a[k], y = b[k];
    if (Array.isArray(x) || Array.isArray(y)) { const X = x || [0, 0, 0], Y = y || [0, 0, 0]; P[k] = X.map((v, i) => lerp(v, Y[i] ?? 0, w)); }
    else if (typeof x === 'number' || typeof y === 'number') P[k] = lerp(+x || 0, +y || 0, w);
    else if (k === 'face') P[k] = w < 0.5 ? x : y; else P[k] = w < 0.5 ? x : y; }
  return P; }
export const CHAR_DEF = DEF;

// hand poses: curl per finger (0 open … 1 fist), spread, thumb curl
const HANDS = { relaxed: { c: [0.35, 0.4, 0.45, 0.5], t: 0.3, s: 0.05 }, fist: { c: [1, 1, 1, 1], t: 0.9, s: 0 }, point: { c: [0, 1, 1, 1], t: 0.8, s: 0 }, open: { c: [0.05, 0.05, 0.08, 0.1], t: 0.05, s: 0.25 },
  grip: { c: [0.7, 0.75, 0.8, 0.85], t: 0.6, s: 0 }, tense: { c: [0.15, 0.2, 0.25, 0.3], t: 0.2, s: 0.35 } };
export function setHand(ch, side, pose = 'relaxed', mix = null) { const h = ch.userData.J['hand' + side]; if (!h || !h.userData.fingers) return;
  const A = HANDS[pose] || HANDS.relaxed, B2 = mix ? HANDS[mix[0]] : null, w = mix ? mix[1] : 0, sx = h.userData.sx;
  h.userData.fingers.forEach(([a, b], i) => { const c = A.c[i] * (1 - w) + (B2 ? B2.c[i] * w : 0), sp = (A.s * (1 - w) + (B2 ? B2.s * w : 0)) * (i - 1.5) * 0.35;
    a.rotation.set(-c * 1.35, 0, sx * sp); b.rotation.set(-c * 1.5, 0, 0); });
  const tc = A.t * (1 - w) + (B2 ? B2.t * w : 0); h.userData.thumb[0].rotation.set(0.5 + tc * 0.4, 0, -sx * (0.7 - tc * 0.5)); h.userData.thumb[1].rotation.set(-tc * 0.9, 0, 0); }
// emotion + delivery from the script's direction text (Hinglish keywords)
export function emotionFrom(dir) { const n = (dir || '').toLowerCase(), E = { happy: 0, sad: 0, angry: 0, fear: 0, surprise: 0, pain: 0, cry: 0 }, has = (...w) => w.some(x => n.includes(x));
  if (has('muskaan', 'hasi', 'josh', 'khushi', 'mazaak', 'jeet')) E.happy = 0.7; if (has('jhooti muskaan')) E.happy = 0.3;
  if (has('aansu', 'ro-te', 'ro-ke', 'gala bhar', 'toot')) { E.sad = 0.7; E.cry = has('aansu', 'ro-te', 'ro-ke') ? 0.8 : 0.3; }
  if (has('gham', 'dheemi, bhaari', 'dard bhara', 'yaad')) E.sad = Math.max(E.sad, 0.5);
  if (has('gussa', 'sakht', 'chidh', 'hukm')) E.angry = 0.6; if (has('darr', 'ghabrahat', 'kaanp', 'scared')) E.fear = 0.7;
  if (has('hairani', 'chaunk', 'hairaan')) E.surprise = 0.7; if (has('dard', 'haanf', 'thaka', 'bukhaar', 'behosh')) E.pain = has('dard') ? 0.6 : 0.35;
  if (has('pakka', 'faisla', 'leader')) E.angry = Math.max(E.angry, 0.25);
  const D = { whisper: has('fusfus', 'khud se', 'dheemi'), shout: has('chill', 'cheekh', 'poori awaaz', 'poora zor', 'poori taaqat'), gesture: has('ishaara') ? 'point' : null };
  return { E, D }; }

// ---------------- ZENO: alien soldier on the same joint hierarchy (so mocap drives it) ----------------
export function buildZenoRig(opts = {}) {
  const H = opts.commander ? 3.0 : 2.6, s = H / 1.75, root = new THREE.Group(); root.name = 'zeno'; const J = {};
  const A = mat('#2e203a', 0.45), A2 = mat('#5c4270', 0.45), SK = mat('#18121e', 0.6), BN = mat('#786884', 0.5);
  const glow = (c, r) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 10, 8), new THREE.MeshBasicMaterial({ color: c })); return m; };
  const legL = 0.5 * H, torsoL = 0.3 * H;
  J.hips = bone('hips', root, 0, legL, 0); J.spine = bone('spine', J.hips, 0, 0.05 * H, 0); J.chest = bone('chest', J.spine, 0, 0.12 * H, 0.02 * H);
  J.neck = bone('neck', J.chest, 0, torsoL - 0.16 * H, 0.02 * H); J.head = bone('head', J.neck, 0, 0.09 * H, 0.05 * H);
  { const m = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 12), A); m.scale.set(0.08 * H, 0.05 * H, 0.06 * H); J.hips.add(m); }
  { const ab = limb(0.055 * H, 0.07 * H, 0.14 * H, SK); ab.rotation.x = Math.PI; ab.position.y = -0.01 * H; J.spine.add(ab);
    for (let k = 0; k < 3; k++) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.08 * H, 0.025 * H, 0.03 * H), A2); p.position.set(0, 0.02 * H + k * 0.04 * H, 0.05 * H); J.spine.add(p); }
    const ch = new THREE.Mesh(new THREE.SphereGeometry(1, 18, 14), A); ch.scale.set(0.13 * H, 0.1 * H, 0.085 * H); ch.position.y = 0.06 * H; J.chest.add(ch);
    const bp = new THREE.Mesh(new THREE.SphereGeometry(1, 14, 10), A2); bp.scale.set(0.08 * H, 0.05 * H, 0.04 * H); bp.position.set(0, 0.07 * H, 0.06 * H); J.chest.add(bp);
    for (let k = 0; k < 4; k++) { const sp = new THREE.Mesh(new THREE.ConeGeometry(0.015 * H, 0.09 * H, 6), BN); sp.position.set(0, 0.1 * H - k * 0.05 * H, -0.08 * H); sp.rotation.x = -1.9; J.chest.add(sp); } }
  { const nk = limb(0.03 * H, 0.035 * H, 0.1 * H, SK); nk.rotation.x = Math.PI; nk.position.y = -0.01 * H; J.neck.add(nk);
    for (let k = 0; k < 7; k++) { const a = (k / 6 - 0.5) * 1.8, g = glow(0x4fc3ff, 0.007 * H); g.position.set(Math.sin(a) * 0.034 * H, 0.04 * H, Math.cos(a) * 0.034 * H); J.neck.add(g); }
    const nl = new THREE.PointLight(0x4fc3ff, 1.2, 2.5); nl.position.set(0, 0.04 * H, 0.06 * H); J.neck.add(nl); root.userData.neckGlow = nl;
    const hd = limb(0.05 * H, 0.03 * H, 0.15 * H, A); hd.rotation.x = -Math.PI / 2 + 0.25; hd.position.set(0, 0.03 * H, -0.03 * H); J.head.add(hd);
    const crest = new THREE.Mesh(new THREE.ConeGeometry(0.025 * H, 0.1 * H, 6), A2); crest.position.set(0, 0.06 * H, -0.06 * H); crest.rotation.x = -2.2; J.head.add(crest);
    for (const [x, y] of [[-0.018, 0.035], [0.018, 0.035], [0, 0.048]]) { const e = glow(0xff323c, 0.007 * H); e.position.set(x * H, y * H, 0.1 * H); J.head.add(e); }
    if (opts.commander) for (const sg of [-1, 1]) { const horn = new THREE.Mesh(new THREE.ConeGeometry(0.018 * H, 0.16 * H, 6), mat('#967846', 0.4)); horn.position.set(sg * 0.04 * H, 0.08 * H, -0.04 * H); horn.rotation.set(-0.7, 0, sg * -0.5); J.head.add(horn); } }
  for (const [side, sx] of [['L', 1], ['R', -1]]) {
    const sh = bone('shoulder' + side, J.chest, sx * 0.12 * H, 0.1 * H, 0); const pad = new THREE.Mesh(new THREE.SphereGeometry(1, 12, 10), A2); pad.scale.set(0.06 * H, 0.04 * H, 0.06 * H); sh.add(pad);
    const ua = bone('upperArm' + side, sh, 0, 0, 0), uaL = 0.2 * H, faL = 0.19 * H; ua.add(limb(0.032 * H, 0.025 * H, uaL, A));
    const fa = bone('foreArm' + side, ua, 0, -uaL, 0); fa.add(limb(0.026 * H, 0.02 * H, faL, SK)); const br = new THREE.Mesh(new THREE.BoxGeometry(0.04 * H, 0.1 * H, 0.04 * H), A2); br.position.y = -faL * 0.5; fa.add(br);
    const hand = bone('hand' + side, fa, 0, -faL, 0); const g = glow(0x4fc3ff, 0.008 * H); g.position.set(0, 0.02 * H, 0.025 * H); hand.add(g);
    const fingers = []; for (let f = 0; f < 3; f++) { const k1 = bone('c' + f, hand, (f - 1) * 0.015 * H, -0.01 * H, 0), cl = limb(0.007 * H, 0.002 * H, 0.08 * H, BN, 6); k1.add(cl); k1.rotation.x = -0.3; fingers.push([k1, k1]); }
    hand.userData.claws = fingers; J['shoulder' + side] = sh; J['upperArm' + side] = ua; J['foreArm' + side] = fa; J['hand' + side] = hand; }
  for (const [side, sx] of [['L', 1], ['R', -1]]) {   // digitigrade look: thigh forward, long shin, raised heel
    const th = bone('thigh' + side, J.hips, sx * 0.06 * H, -0.01 * H, 0), thL = 0.23 * H, shL = 0.24 * H; th.add(limb(0.045 * H, 0.03 * H, thL, A));
    const kp = new THREE.Mesh(new THREE.SphereGeometry(0.03 * H, 10, 8), A2); kp.position.y = -thL; th.add(kp);
    const sn = bone('shin' + side, th, 0, -thL, 0); sn.add(limb(0.028 * H, 0.018 * H, shL, SK));
    const ft = bone('foot' + side, sn, 0, -shL, 0); const fm = limb(0.022 * H, 0.012 * H, 0.1 * H, A); fm.rotation.x = -Math.PI / 2 + 0.3; ft.add(fm);
    J['thigh' + side] = th; J['shin' + side] = sn; J['foot' + side] = ft; }
  root.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  root.userData.J = J; root.userData.H = H; root.userData.legL = legL; root.userData.def = { sex: 'z', h: H }; root.userData.zeno = true;
  return root;
}
export function addPlasmaRifle(zeno) { const h = zeno.userData.J.handR, H = zeno.userData.H, g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.BoxGeometry(0.035 * H, 0.05 * H, 0.32 * H), mat('#464250', 0.35, { metalness: 0.4 })); body.position.z = 0.1 * H; g.add(body);
  for (const sg of [-1, 1]) { const pr = new THREE.Mesh(new THREE.ConeGeometry(0.008 * H, 0.16 * H, 6), mat('#786884', 0.4)); pr.rotation.x = Math.PI / 2; pr.position.set(sg * 0.012 * H, 0, 0.3 * H); g.add(pr); }
  const core = new THREE.Mesh(new THREE.SphereGeometry(0.012 * H, 10, 8), new THREE.MeshBasicMaterial({ color: 0xbe5aff })); core.position.set(0, 0.03 * H, 0.08 * H); g.add(core);
  g.position.set(0, -0.03 * H, 0.02 * H); h.add(g); zeno.userData.rifle = g; zeno.userData.muzzle = new THREE.Vector3(0, 0, 0.38 * H); return g; }
