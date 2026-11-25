// Shared shot runtime: renderer + post canvas, toon conversion + character outlines, lip-sync lookup, grain/vignette, small FX helpers.
import * as THREE from 'three'; import { OutlineEffect } from 'three/addons/effects/OutlineEffect.js'; import * as C3 from './char3d.js';
export const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v)), lerp = (a, b, t) => a + (b - a) * t, sm = x => x * x * (3 - 2 * x), hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
export const W = 1920, H = 1080;
export function setup(o = {}) { const QS = new URLSearchParams(location.search), PR = +(QS.get('pr') || 1);
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true }); renderer.setPixelRatio(PR); renderer.setSize(W, H); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.VSMShadowMap; renderer.outputColorSpace = THREE.SRGBColorSpace;
  const wrap = document.getElementById('wrap'); wrap.appendChild(renderer.domElement); const post = document.createElement('canvas'); post.width = W; post.height = H; wrap.appendChild(post);
  const scene = new THREE.Scene(); scene.background = new THREE.Color(o.bg ?? 0x05070a); if (o.fog) scene.fog = new THREE.FogExp2(o.fog[0], o.fog[1]);
  const camera = new THREE.PerspectiveCamera(o.fov ?? 40, W / H, 0.05, 200); return { renderer, scene, camera, pg: post.getContext('2d') }; }
const grad = new THREE.DataTexture(new Uint8Array([60, 60, 60, 255, 140, 140, 140, 255, 235, 235, 235, 255]), 3, 1, THREE.RGBAFormat); grad.minFilter = grad.magFilter = THREE.NearestFilter; grad.needsUpdate = true;
export function toonMat(m) { if (!m.isMeshStandardMaterial) return m; const t = new THREE.MeshToonMaterial({ color: m.color, map: m.map, gradientMap: grad, transparent: m.transparent, opacity: m.opacity, side: m.side, depthWrite: m.depthWrite, polygonOffset: m.polygonOffset, polygonOffsetFactor: m.polygonOffsetFactor, emissive: m.emissive, emissiveIntensity: m.emissiveIntensity }); t.userData.outlineParameters = { visible: false }; return t; }
export function toonify(root) { root.traverse(o => { if (!o.isMesh || !o.material) return; o.material = Array.isArray(o.material) ? o.material.map(toonMat) : toonMat(o.material); (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => m.userData.outlineParameters = { visible: false }); }); }
export function outlineChars(chars) { for (const c of chars) c.traverse(o => { if (o.isMesh) (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => m.userData.outlineParameters = { visible: !m.transparent && !m.isMeshBasicMaterial, thickness: 0.004, color: [0.06, 0.05, 0.05] }); }); }
export const makeOutline = r => new OutlineEffect(r, { defaultThickness: 0.003 });
// lip-sync: lines.json (retimed master timeline) → mouth shape for a character at shot-relative time
export async function loadLines(shotId) { const L = await (await fetch('lines.json')).json(); const lines = L.lines.filter(x => x.shot === shotId), shot = L.shots.find(s => s.id === shotId);
  return { shot, lines, at(who, t) { for (const ln of lines) if (ln.who === who && t >= ln.rel && t < ln.rel + ln.dur) { const v = L.vis[ln.key], i = Math.floor((t - ln.rel) * 30); return { mouth: v[Math.min(v.length - 1, i)] || 'X', line: ln, emo: C3.emotionFrom(ln.note || ''), u: (t - ln.rel) / ln.dur }; } return { mouth: 'X', line: null, emo: null }; } }; }
export function finish(pg, t, o = {}) { pg.clearRect(0, 0, W, H); const vg = pg.createRadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H * 0.9); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, `rgba(0,0,0,${o.vig ?? 0.6})`); pg.fillStyle = vg; pg.fillRect(0, 0, W, H);
  pg.globalAlpha = 0.05; const f = Math.floor(t * 30); for (let i = 0; i < 1200; i++) { pg.fillStyle = hash(i + f * 7) > 0.5 ? '#fff' : '#000'; pg.fillRect(hash(i * 3 + f) * W, hash(i * 7 + f) * H, 2, 2); } pg.globalAlpha = 1;
  if (o.flash > 0) { pg.fillStyle = `rgba(255,236,220,${o.flash})`; pg.fillRect(0, 0, W, H); } if (o.black > 0) { pg.fillStyle = `rgba(0,0,0,${o.black})`; pg.fillRect(0, 0, W, H); } }
export function softSprite(color = 0x8a8076) { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.5, 'rgba(255,255,255,.45)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  return new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), color, transparent: true, opacity: 0, depthWrite: false }); }

// ---------------- no-interpenetration: every character (and chosen props) is approximated by small spheres that follow its meshes.
// resolve() pushes the yielding character out horizontally until nothing overlaps; qa() reports any overlap left (shot QA).
const _v = new THREE.Vector3(), _s = new THREE.Vector3(), _q = new THREE.Quaternion(), _p = new THREE.Vector3();
export function collider(root, o = {}) { const parts = []; root.updateMatrixWorld(true);
  root.traverse(m => { if (!m.isMesh || !m.geometry || m.isSprite || m.material?.transparent || m.material?.isMeshBasicMaterial || m.userData.noCollide) return;
    if (!m.geometry.boundingBox) m.geometry.computeBoundingBox(); const b = m.geometry.boundingBox, size = b.getSize(new THREE.Vector3()); m.matrixWorld.decompose(_p, _q, _s);
    const ws = new THREE.Vector3(size.x * Math.abs(_s.x), size.y * Math.abs(_s.y), size.z * Math.abs(_s.z)); if (Math.max(ws.x, ws.y, ws.z) < (o.minSize ?? 0.035)) return;
    const r = Math.max(0.012, Math.min(ws.x, ws.y, ws.z) / 2) * (o.shrink ?? 0.92), n = [ws.x, ws.y, ws.z].map(e => Math.max(1, Math.min(8, Math.round(e / (2 * r))))), pts = [];
    for (let i = 0; i < n[0]; i++) for (let j = 0; j < n[1]; j++) for (let k = 0; k < n[2]; k++) pts.push(new THREE.Vector3(b.min.x + size.x * (i + 0.5) / n[0], b.min.y + size.y * (j + 0.5) / n[1], b.min.z + size.z * (k + 0.5) / n[2]));
    // spheres in the corners of a long thin limb would poke out of its rounded shape: keep only the ones inside the inscribed ellipsoid-ish volume
    const c = b.getCenter(new THREE.Vector3()), keep = pts.filter(p => { const d = p.clone().sub(c); const e = (d.x / (size.x / 2 + 1e-6)) ** 2 + (d.y / (size.y / 2 + 1e-6)) ** 2 + (d.z / (size.z / 2 + 1e-6)) ** 2; return e <= 1.15 || pts.length <= 2; });
    parts.push({ m, pts: keep.length ? keep : [c], r, name: m.name || m.parent?.name || '' }); });
  return { root, parts, world: [] }; }
export function updateCollider(C) { const out = C.world; out.length = 0; for (const P of C.parts) { if (!P.m.visible || !visibleUp(P.m)) continue; for (const p of P.pts) out.push({ c: p.clone().applyMatrix4(P.m.matrixWorld), r: P.r, part: P }); } return out; }
const visibleUp = o => { for (let x = o; x; x = x.parent) if (!x.visible) return false; return true; };
function overlap(A, B, tol) { let best = null, push = new THREE.Vector3(), n = 0, maxD = 0;
  for (const a of A) for (const b of B) { const d = a.c.distanceTo(b.c), depth = a.r + b.r - d - tol; if (depth > 0) { n++; if (depth > maxD) { maxD = depth; best = [a, b]; } } }
  if (n) { const [a, b] = best; push.copy(b.c).sub(a.c); const full = push.length(); push.y = 0; const hl = push.length(); if (hl < 1e-4) push.copy(B.length ? B[0].c : push).set(1, 0, 0); push.normalize(); if (hl > 1e-4 && full > 1e-4) maxD = maxD * full / hl * 0.5 + maxD * 0.5; }
  return n ? { dir: push.normalize(), depth: maxD, pair: best, n } : null; }
// pairs: [[colliderA, colliderB, mode]] mode: 'b' = B yields, 'a' = A yields, 'both' = split; static props never move
export function resolve(pairs, o = {}) { const tol = o.tol ?? 0.006; for (const [A, B] of pairs) { (A.root.userData.push ||= new THREE.Vector3()).set(0, 0, 0); (B.root.userData.push ||= new THREE.Vector3()).set(0, 0, 0); } for (let it = 0; it < (o.iters ?? 10); it++) { let moved = false;
    for (const [A, B, mode] of pairs) { updateCollider(A); updateCollider(B); const r = overlap(A.world, B.world, tol); if (!r) continue; moved = true; const d = r.dir.clone().multiplyScalar(r.depth + 0.004);
      const mv = (R, k) => { R.position.addScaledVector(d, k); R.userData.push.addScaledVector(d, k); };
      if (mode === 'a') mv(A.root, -1); else if (mode === 'both') { mv(A.root, -0.5); mv(B.root, 0.5); } else mv(B.root, 1);
      A.root.updateMatrixWorld(true); B.root.updateMatrixWorld(true); }
    if (!moved) break; } }
export function qa(pairs, t, tag = '', tol = 0.015) { const bad = []; for (const [A, B, , label] of pairs) { updateCollider(A); updateCollider(B); const r = overlap(A.world, B.world, tol); if (r) { const nm = x => { for (let o = x.part.m; o; o = o.parent) if (o.name) return o.name; return '?'; }; bad.push(`${label || ''} depth ${(r.depth * 100).toFixed(1)}cm (${r.n}) ${nm(r.pair[0])}~${nm(r.pair[1])} push ${(B.root.userData.push?.length() * 100 || 0).toFixed(1)}cm`); } }
  if (bad.length) console.error('QA-OVERLAP', tag, t.toFixed(2), bad.join(' | ')); return bad; }
