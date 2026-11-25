// Location sets for the finale (stylized 3D, toon-ready). Each builder adds meshes/lights to the scene and returns handles.
import * as THREE from 'three';
const TL = new THREE.TextureLoader();
function pbr(name, rep, extra = {}) { const ld = (k, srgb) => { const t = TL.load(`assets/ph/tex/${name}_${k}.jpg`); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); t.anisotropy = 8; if (srgb) t.colorSpace = THREE.SRGBColorSpace; return t; };
  return new THREE.MeshStandardMaterial({ map: ld('diff', 1), normalMap: ld('nor'), roughness: 0.95, ...extra }); }
const mat = (c, r = 0.8, x = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: r, ...x });
const box = (w, h, d, m) => { const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); o.castShadow = o.receiveShadow = true; return o; };
const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

// ---------------- LAB B-2 (Day 3): wrecked research lab, night, ceiling hole, screen with the Tesseract ----------------
export function buildLab(scene) {
  const G = new THREE.Group(); scene.add(G); const W = 12, D = 10, Hh = 3.6;
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(W, D), pbr('concrete_floor_damaged_01', [3, 3])); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; G.add(floor);
  const wallM = pbr('concrete_block_wall', [3, 1]), wallM2 = pbr('concrete_slab_wall', [2, 1]);
  const back = box(W, Hh, 0.2, wallM); back.position.set(0, Hh / 2, -D / 2); G.add(back);
  // left wall with the back door ("peeche wala raasta") at z 2.1–3.1 → service corridor
  const DZ0 = 2.1, DZ1 = 3.1, DH = 2.2;
  for (const [z0, z1, y0, y1] of [[-D / 2, DZ0, 0, Hh], [DZ1, D / 2, 0, Hh], [DZ0, DZ1, DH, Hh]]) { const w = box(0.2, y1 - y0, z1 - z0, wallM2); w.position.set(-W / 2, (y0 + y1) / 2, (z0 + z1) / 2); G.add(w); }
  const frameM = mat('#3b3e42', 0.5, { metalness: 0.4 }); for (const z of [DZ0, DZ1]) { const f = box(0.26, DH, 0.06, frameM); f.position.set(-W / 2, DH / 2, z); G.add(f); } { const f = box(0.26, 0.06, DZ1 - DZ0 + 0.06, frameM); f.position.set(-W / 2, DH, (DZ0 + DZ1) / 2); G.add(f); }
  const door = new THREE.Group(); door.position.set(-W / 2 - 0.02, 0, DZ0 + 0.03); G.add(door);
  { const leaf = box(0.05, DH - 0.04, DZ1 - DZ0 - 0.06, mat('#5b6066', 0.6, { metalness: 0.3 })); leaf.position.set(0, DH / 2, (DZ1 - DZ0 - 0.06) / 2); door.add(leaf);
    const bar = box(0.06, 0.04, 0.6, mat('#a8adb3', 0.3, { metalness: 0.8 })); bar.position.set(0.05, 1.0, 0.5); door.add(bar);
    const sign = box(0.01, 0.16, 0.36, new THREE.MeshBasicMaterial({ color: 0x1f9a4a })); sign.position.set(0.04, 1.75, 0.47); door.add(sign);
    const exitL = new THREE.PointLight(0x2bd46b, 0.8, 3, 2); exitL.position.set(-W / 2 + 0.3, DH + 0.2, (DZ0 + DZ1) / 2); G.add(exitL); }
  const exitSign = box(0.04, 0.14, 0.4, new THREE.MeshBasicMaterial({ color: 0x2bd46b })); exitSign.position.set(-W / 2 + 0.12, DH + 0.18, (DZ0 + DZ1) / 2); G.add(exitSign);
  // right wall with a blasted hole (the search-light comes through it)
  for (const [z0, z1, y0, y1] of [[-D / 2, -1.2, 0, Hh], [1.6, D / 2, 0, Hh], [-1.2, 1.6, 0, 0.6], [-1.2, 1.6, 2.6, Hh]]) { const w = box(0.25, y1 - y0, z1 - z0, wallM2); w.position.set(W / 2, (y0 + y1) / 2, (z0 + z1) / 2); G.add(w); }
  // ceiling with a hole (where the Zeno drops in), hanging cables
  const ceilM = mat('#3a3633', 0.95);
  for (const [x0, x1, z0, z1] of [[-W / 2, -1.4, -D / 2, D / 2], [1.4, W / 2, -D / 2, D / 2], [-1.4, 1.4, -D / 2, -2.6], [-1.4, 1.4, -0.4, D / 2]]) { const c = box(x1 - x0, 0.25, z1 - z0, ceilM); c.position.set((x0 + x1) / 2, Hh + 0.12, (z0 + z1) / 2); G.add(c); }
  for (let i = 0; i < 7; i++) { const a = hash(i) * 6.28, r = 1.3 + hash(i + 3) * 0.3, len = 0.6 + hash(i + 5) * 1.4; const cb = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, len, 5), mat('#111', 0.6)); cb.position.set(Math.cos(a) * r, Hh - len / 2, Math.sin(a) * r); cb.rotation.z = (hash(i + 7) - 0.5) * 0.5; G.add(cb); }
  for (let i = 0; i < 9; i++) { const s = 0.2 + hash(i * 3) * 0.5, slab = box(s * 1.6, 0.12, s, ceilM); slab.position.set((hash(i) - 0.5) * 3, 0.06 + hash(i + 1) * 0.05, (hash(i + 2) - 0.5) * 3); slab.rotation.set(hash(i + 4) * 0.4, hash(i + 5) * 3, hash(i + 6) * 0.3); G.add(slab); }
  // overturned lab bench (the trio hide behind/under it), working bench with glassware, server racks, whiteboard
  const benchM = mat('#6d6f72', 0.5, { metalness: 0.3 }), topM = mat('#2b2d31', 0.4);
  const over = new THREE.Group(); const top = box(2.4, 0.06, 0.9, topM); top.position.set(0, 0.45, 0); top.rotation.x = Math.PI / 2; over.add(top);
  for (const x of [-1.1, 1.1]) for (const z of [-0.2, 0.2]) { const leg = box(0.05, 0.05, 0.85, benchM); leg.position.set(x, 0.9 + 0.0, z * 0 - 0.42); over.add(leg); }
  over.position.set(-1.2, 0, 1.4); over.rotation.y = Math.PI + 0.1; G.add(over);
  const bench = new THREE.Group(); const bt = box(3, 0.06, 0.9, topM); bt.position.y = 0.92; bench.add(bt); const cab = box(2.9, 0.85, 0.85, benchM); cab.position.y = 0.45; bench.add(cab);
  const glass = new THREE.MeshStandardMaterial({ color: 0x9fd3e6, roughness: 0.05, transparent: true, opacity: 0.5 });
  for (let i = 0; i < 6; i++) { const f = new THREE.Mesh(i % 2 ? new THREE.CylinderGeometry(0.03, 0.03, 0.18, 10) : new THREE.ConeGeometry(0.07, 0.16, 12), glass); f.position.set(-1.2 + i * 0.45, 1.03, (hash(i) - 0.5) * 0.4); bench.add(f); }
  const micro = new THREE.Group(); const mb = box(0.18, 0.05, 0.25, mat('#ddd', 0.4)); mb.position.y = 0.97; micro.add(mb); const mc = box(0.05, 0.3, 0.05, mat('#ddd', 0.4)); mc.position.set(0, 1.12, -0.08); micro.add(mc); micro.position.x = 1.1; bench.add(micro);
  bench.position.set(1.8, 0, -2.6); G.add(bench);
  const rackM = mat('#1d1f24', 0.5, { metalness: 0.4 }), leds = [];
  for (let r = 0; r < 3; r++) { const rk = box(0.6, 2.1, 0.8, rackM); rk.position.set(-5.4, 1.05, -3.2 + r * 0.9); G.add(rk);
    for (let k = 0; k < 10; k++) { const l = new THREE.Mesh(new THREE.SphereGeometry(0.012, 6, 4), new THREE.MeshBasicMaterial({ color: k % 3 ? 0x2bd46b : 0xffa630 })); l.position.set(-5.09, 0.4 + k * 0.15, -3.4 + r * 0.9 + (k % 2) * 0.2); G.add(l); leds.push(l); } }
  const wb = box(2.2, 1.2, 0.04, mat('#e8e6df', 0.6)); wb.position.set(-2.2, 1.6, -4.88); G.add(wb);
  // the screen (Tesseract with Earth inside) — canvas, glows cyan
  const sc = document.createElement('canvas'); sc.width = 512; sc.height = 288; const sctx = sc.getContext('2d'), stex = new THREE.CanvasTexture(sc); stex.colorSpace = THREE.SRGBColorSpace;
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 1.07), new THREE.MeshBasicMaterial({ map: stex })); screen.position.set(1.6, 1.75, -4.88); G.add(screen);
  const frame = box(2.0, 1.17, 0.06, mat('#111', 0.4)); frame.position.set(1.6, 1.75, -4.92); G.add(frame);
  const scrL = new THREE.PointLight(0x5fd8ff, 4, 7, 1.5); scrL.position.set(1.6, 1.7, -4.2); G.add(scrL);
  function drawScreen(t, power = 1) { const g = sctx; g.fillStyle = '#04121a'; g.fillRect(0, 0, 512, 288); if (power <= 0.02) { stex.needsUpdate = true; return; }
    g.save(); g.translate(256, 144); g.globalAlpha = power; g.strokeStyle = '#5fd8ff'; g.lineWidth = 2;
    const R = 80, a = t * 0.4; for (const s of [1, 0.55]) { g.beginPath(); for (let k = 0; k < 5; k++) { const ang = a * (s === 1 ? 1 : -1.3) + k * Math.PI / 2; const x = Math.cos(ang) * R * s, y = Math.sin(ang) * R * s * 0.6; k ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); }
    for (let k = 0; k < 4; k++) { const ang = a + k * Math.PI / 2, ang2 = -a * 1.3 + k * Math.PI / 2; g.beginPath(); g.moveTo(Math.cos(ang) * R, Math.sin(ang) * R * 0.6); g.lineTo(Math.cos(ang2) * R * 0.55, Math.sin(ang2) * R * 0.33); g.stroke(); }
    const gr = g.createRadialGradient(-6, -6, 2, 0, 0, 30); gr.addColorStop(0, '#7fd0ff'); gr.addColorStop(0.6, '#1f6aa8'); gr.addColorStop(1, '#0b2a48'); g.fillStyle = gr; g.beginPath(); g.arc(0, 0, 28, 0, 7); g.fill();
    g.fillStyle = '#3c8a4a'; g.beginPath(); g.ellipse(-8 + Math.sin(t) * 3, -4, 9, 6, 0.5, 0, 7); g.fill(); g.restore();
    g.fillStyle = 'rgba(95,216,255,.8)'; g.font = '14px monospace'; g.fillText('SECTOR 07 · DATA TRANSFER', 14, 22); g.fillStyle = `rgba(255,255,255,${0.04 + 0.04 * Math.sin(t * 30)})`; for (let y = 0; y < 288; y += 3) g.fillRect(0, y, 512, 1); stex.needsUpdate = true; }
  // red search-light from the ship, through the wall hole (spot + visible beam)
  const spot = new THREE.SpotLight(0xff3020, 0, 22, 0.22, 0.6, 1.2); spot.position.set(9, 6, 0.2); spot.castShadow = true; spot.shadow.mapSize.set(1024, 1024); G.add(spot, spot.target);
  const beamM = new THREE.MeshBasicMaterial({ color: 0xff3a28, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
  const beam = new THREE.Mesh(new THREE.ConeGeometry(1.3, 10, 24, 1, true), beamM); G.add(beam);
  const emerg = new THREE.PointLight(0xff5a3a, 0.6, 9, 1.6); emerg.position.set(-4.5, 3.2, 3.5); G.add(emerg);
  const amb = new THREE.HemisphereLight(0x6a7c94, 0x221c18, 2.2); const fill = new THREE.PointLight(0x8aa8c8, 3.5, 9, 1.4); fill.position.set(0.5, 2.2, 4.2); G.add(fill); G.add(amb);
  function update(t, s = {}) { drawScreen(t, s.screen ?? 1); for (const [i, l] of leds.entries()) l.visible = Math.sin(t * (2 + (i % 5)) + i) > -0.2;
    emerg.intensity = 0.5 + 0.5 * Math.max(0, Math.sin(t * 2.2)) * (s.alarm ?? 1);
    const sw = s.sweep ?? 0, tgt = new THREE.Vector3(-1 + Math.sin(sw) * 3.2, 0, 0.5 + Math.cos(sw * 0.7) * 2.2); spot.intensity = (s.beam ?? 0) * 60; spot.target.position.copy(tgt);
    const dir = tgt.clone().sub(spot.position), len = dir.length(); beam.position.copy(spot.position).addScaledVector(dir, 0.5); beam.scale.set(1, len / 10, 1); beam.quaternion.setFromUnitVectors(new THREE.Vector3(0, -1, 0), dir.normalize()); beamM.opacity = 0.09 * (s.beam ?? 0); }
  return { G, update, screen, spot, hole: new THREE.Vector3(0, Hh, 0), bench: over, door, doorZ: [DZ0, DZ1], size: { W, D, Hh } };
}

// ---------------- service corridor behind the lab (Day 3): x from x0 going -x, centred on z = zc; flickering tubes, emergency red, debris, broken glass ----------------
export function buildCorridor(scene, o = {}) {
  const G = new THREE.Group(); scene.add(G); const x0 = o.x0 ?? -6.12, L = o.len ?? 16, zc = o.zc ?? 2.6, w = 2.0, Hh = 2.7, x1 = x0 - L;
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(L, w), pbr('concrete_floor_damaged_01', [L / 2, 1])); floor.rotation.x = -Math.PI / 2; floor.position.set((x0 + x1) / 2, 0.002, zc); floor.receiveShadow = true; G.add(floor);
  const wm = pbr('concrete_slab_wall', [L / 3, 1]); for (const sg of [-1, 1]) { const wl = box(L, Hh, 0.15, wm); wl.position.set((x0 + x1) / 2, Hh / 2, zc + sg * (w / 2 + 0.075)); G.add(wl); }
  const ceil = box(L, 0.15, w + 0.3, mat('#2e2c2a', 0.95)); ceil.position.set((x0 + x1) / 2, Hh + 0.075, zc); G.add(ceil);
  const end = box(0.15, Hh, w, wm); end.position.set(x1, Hh / 2, zc); G.add(end);
  // exit door at the far end (half open, night outside glows faintly)
  const out = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 2.1), new THREE.MeshBasicMaterial({ color: 0x1a2230 })); out.rotation.y = Math.PI / 2; out.position.set(x1 + 0.08, 1.05, zc + 0.3); G.add(out);
  const ed = box(0.05, 2.1, 0.95, mat('#555a60', 0.6, { metalness: 0.3 })); ed.position.set(x1 + 0.5, 1.05, zc + 0.3 + 0.45); ed.rotation.y = -1.1; G.add(ed);
  // pipes + cable trays along the ceiling, wall panels
  const pipeM = mat('#6b6f74', 0.4, { metalness: 0.6 }); for (const [y, z, r] of [[Hh - 0.18, zc - 0.75, 0.06], [Hh - 0.3, zc - 0.62, 0.035], [Hh - 0.2, zc + 0.8, 0.045]]) { const pp = new THREE.Mesh(new THREE.CylinderGeometry(r, r, L, 10), pipeM); pp.rotation.z = Math.PI / 2; pp.position.set((x0 + x1) / 2, y, z); pp.castShadow = true; G.add(pp); }
  for (let i = 0; i < 6; i++) { const dx = x0 - 1.5 - i * 2.6, side = i % 2 ? 1 : -1; const dr = box(0.9, 2.0, 0.05, mat(i === 3 ? '#6e4b3a' : '#4c5157', 0.7)); dr.position.set(dx, 1.0, zc + side * (w / 2 - 0.0)); G.add(dr); }
  // lights: tube fixtures (some dead, one flickering), red emergency beacons
  const tubes = []; for (let i = 0; i < 6; i++) { const x = x0 - 1.2 - i * 2.7; const fx = box(1.2, 0.05, 0.14, mat('#cfd6dc', 0.4)); fx.position.set(x, Hh - 0.03, zc); G.add(fx);
    const glow = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.02, 0.1), new THREE.MeshBasicMaterial({ color: 0xdfe8ff })); glow.position.set(x, Hh - 0.06, zc); G.add(glow);
    const l = new THREE.PointLight(0xc8d6ff, 0, 6, 1.6); l.position.set(x, Hh - 0.25, zc); G.add(l); tubes.push({ l, glow, dead: i === 1 || i === 4, flick: i === 2 }); }
  const reds = []; for (let i = 0; i < 3; i++) { const x = x0 - 2.5 - i * 5.5; const b = new THREE.Mesh(new THREE.SphereGeometry(0.06, 10, 8), new THREE.MeshBasicMaterial({ color: 0xff2a1a })); b.position.set(x, Hh - 0.25, zc + 0.95); G.add(b); const l = new THREE.PointLight(0xff3020, 1.2, 5, 1.6); l.position.set(x, Hh - 0.4, zc + 0.8); G.add(l); reds.push({ b, l, ph: i * 1.3 }); }
  // debris: fallen ceiling panel, toppled chair, papers, broken glass (an office partition shattered near x0-6)
  const panel = box(1.2, 0.03, 0.6, mat('#bdb7ad', 0.9)); panel.position.set(x0 - 3.4, 0.2, zc + 0.55); panel.rotation.set(0.35, 0.3, 0.05); G.add(panel);
  const chair = new THREE.Group(); { const cm = mat('#2b2d31', 0.6); const st = box(0.45, 0.05, 0.45, cm); st.position.y = 0.45; chair.add(st); const bk = box(0.45, 0.5, 0.05, cm); bk.position.set(0, 0.72, -0.2); chair.add(bk); for (const [a, b] of [[-0.2, -0.2], [0.2, -0.2], [-0.2, 0.2], [0.2, 0.2]]) { const lg = box(0.03, 0.45, 0.03, cm); lg.position.set(a, 0.22, b); chair.add(lg); } }
  chair.rotation.set(0, 0.8, Math.PI / 2); chair.position.set(x0 - 8.2, 0.24, zc - 0.65); G.add(chair);
  const paperM = mat('#e9e4d8', 0.9); for (let i = 0; i < 26; i++) { const pp = new THREE.Mesh(new THREE.PlaneGeometry(0.21, 0.29), paperM); pp.rotation.set(-Math.PI / 2, 0, hash(i) * 6); pp.position.set(x0 - 1 - hash(i + 9) * (L - 3), 0.004 + i * 0.0003, zc + (hash(i + 4) - 0.5) * 1.6); pp.receiveShadow = true; G.add(pp); }
  const glassX = o.glassX ?? x0 - 3.5, glassM = new THREE.MeshStandardMaterial({ color: 0xbfe6f2, roughness: 0.05, metalness: 0.1, transparent: true, opacity: 0.55, side: THREE.DoubleSide });
  for (let i = 0; i < 70; i++) { const s = 0.03 + hash(i * 5) * 0.09, g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0, s, 0, s * 0.3, s * 0.4, 0, s * 0.9], 3)); g.computeVertexNormals();
    const sh = new THREE.Mesh(g, glassM); sh.position.set(glassX - hash(i + 2) * 2.2, 0.006, zc + (hash(i + 3) - 0.5) * 1.7); sh.rotation.y = hash(i + 6) * 6; G.add(sh); }
  const frameM = mat('#8a9096', 0.4, { metalness: 0.6 }); { const fr = box(0.04, 2.1, 0.04, frameM); fr.position.set(glassX + 0.2, 1.05, zc - 0.95); G.add(fr); const pane = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 1.2), glassM); pane.position.set(glassX + 0.45, 1.5, zc - 0.94); G.add(pane); }
  function update(t) { for (const [i, tb] of tubes.entries()) { let on = tb.dead ? 0 : 1; if (tb.flick) on = (Math.sin(t * 23) > 0.3 && Math.sin(t * 3.1) > -0.6) ? 1 : 0.08; tb.l.intensity = 2.2 * on; tb.glow.material.color.setScalar(0.1 + 0.85 * on); }
    for (const r of reds) { const k = Math.max(0, Math.sin(t * 3 + r.ph)); r.l.intensity = 0.3 + 1.8 * k; r.b.material.color.setRGB(0.3 + 0.7 * k, 0.05, 0.03); } }
  return { G, update, x0, x1, zc, glassX };
}
