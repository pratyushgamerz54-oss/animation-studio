// Real (scanned) Sketchfab humans (Renderpeople, CC-BY) driven by our procedural motion.
// - normalises scale, recolours skin/clothes to the design-sheet palette (shader colour keys), adds accessories,
// - retargets the pose of our canonical joint hierarchy (char3d.js) onto the model's own bones,
// - drives jaw (lip-sync), eyelids (blinks) and eyes (gaze) from the face state.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import * as C3 from './char3d.js';

const MAP = { hips: 'hip', spine: 'spine_01', chest: 'spine_02', chest2: 'spine_03', neck: 'neck', head: 'head', jaw: 'jaw', eyeL: 'eye_l', eyeR: 'eye_r', lidL: 'eyelid_l', lidR: 'eyelid_r', browL: 'eyebrow_l', browR: 'eyebrow_r', mouthL: 'mouth_l', mouthR: 'mouth_r',
  shoulderL: 'shoulder_l', upperArmL: 'upperarm_l', foreArmL: 'lowerarm_l', handL: 'hand_l', shoulderR: 'shoulder_r', upperArmR: 'upperarm_r', foreArmR: 'lowerarm_r', handR: 'hand_r',
  thighL: 'upperleg_l', shinL: 'lowerleg_l', footL: 'foot_l', thighR: 'upperleg_r', shinR: 'lowerleg_r', footR: 'foot_r' };
// which canonical joint drives each model bone (rotation accumulated down our hierarchy), and the canonical rest direction for limbs
const DRIVE = { hips: 'hips', spine: 'spine', chest: 'chest', chest2: 'chest', neck: 'neck', head: 'head', shoulderL: 'shoulderL', upperArmL: 'upperArmL', foreArmL: 'foreArmL', handL: 'handL', shoulderR: 'shoulderR', upperArmR: 'upperArmR', foreArmR: 'foreArmR', handR: 'handR',
  thighL: 'thighL', shinL: 'shinL', footL: 'footL', thighR: 'thighR', shinR: 'shinR', footR: 'footR' };
const LIMB_CHILD = { upperArmL: 'foreArmL', foreArmL: 'handL', upperArmR: 'foreArmR', foreArmR: 'handR', thighL: 'shinL', shinL: 'footL', thighR: 'shinR', shinR: 'footR' };
const DOWN = new THREE.Vector3(0, -1, 0);
const OPEN = { X: 0, A: 0.02, B: 0.07, C: 0.14, D: 0.24, E: 0.12, F: 0.09, G: 0.05, H: 0.16, grit: 0.03, frown: 0 };

function recolor(mat, R) {   // R: { skin:[r,g,b] multiplier, top:'#hex' (replaces whites/greys), pants:'#hex' (replaces blue denim), hair:'#hex' (darkens light hair) }
  const U = { uSkin: { value: new THREE.Vector3(...R.skin) }, uTop: { value: new THREE.Color(R.top) }, uPants: { value: new THREE.Color(R.pants || '#000') }, uPantsOn: { value: R.pants ? 1 : 0 },
    uHair: { value: new THREE.Color(R.hair || '#000') }, uHairOn: { value: R.hair ? 1 : 0 }, uTopSat: { value: R.topSat ?? 0.16 }, uTopVal: { value: R.topVal ?? 0.5 } };
  mat.onBeforeCompile = sh => { Object.assign(sh.uniforms, U);
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
      uniform vec3 uSkin; uniform vec3 uTop; uniform vec3 uPants; uniform float uPantsOn; uniform vec3 uHair; uniform float uHairOn; uniform float uTopSat; uniform float uTopVal;
      vec3 rgb2hsv(vec3 c){ vec4 K=vec4(0.,-1./3.,2./3.,-1.); vec4 p=mix(vec4(c.bg,K.wz),vec4(c.gb,K.xy),step(c.b,c.g)); vec4 q=mix(vec4(p.xyw,c.r),vec4(c.r,p.yzx),step(p.x,c.r)); float d=q.x-min(q.w,q.y); return vec3(abs(q.z+(q.w-q.y)/(6.*d+1e-10)),d/(q.x+1e-10),q.x); }
      vec3 retint(vec3 c, vec3 tgt){ float l = dot(c, vec3(.299,.587,.114)); return tgt * clamp(l / 0.62, 0.15, 1.35); }`)
      .replace('#include <map_fragment>', `#include <map_fragment>
      { vec3 c = diffuseColor.rgb; vec3 s = pow(max(c, 0.0), vec3(1./2.2)); vec3 h = rgb2hsv(s);
        float skin = smoothstep(0.0, 0.02, h.x) * (1.0 - smoothstep(0.1, 0.14, h.x)) * smoothstep(0.14, 0.24, h.y) * (1.0 - smoothstep(0.7, 0.8, h.y)) * smoothstep(0.2, 0.35, h.z);
        float top = (1.0 - smoothstep(uTopSat, uTopSat + 0.08, h.y)) * smoothstep(uTopVal - 0.1, uTopVal + 0.05, h.z);
        float pants = uPantsOn * smoothstep(0.5, 0.55, h.x) * (1.0 - smoothstep(0.7, 0.75, h.x)) * smoothstep(0.1, 0.2, h.y);
        float hair = uHairOn * smoothstep(0.03, 0.06, h.x) * (1.0 - smoothstep(0.14, 0.17, h.x)) * smoothstep(0.35, 0.5, h.y) * smoothstep(0.25, 0.4, h.z) * (1.0 - skin);
        c = mix(c, c * uSkin, skin);
        c = mix(c, retint(c, uTop), top * (1.0 - skin));
        c = mix(c, retint(c, uPants), pants);
        c = mix(c, retint(c, uHair) * 0.8, hair);
        diffuseColor.rgb = c; }`); };
  mat.customProgramCacheKey = () => 'recolor' + JSON.stringify(R); mat.needsUpdate = true; }

export async function loadRP(file, key, palette, opts) {
  const g = await new GLTFLoader().loadAsync(file), model = g.scene;
  const box0 = new THREE.Box3().setFromObject(model); const h0 = box0.getSize(new THREE.Vector3()).y;
  const B = {}; let skel = null;
  model.traverse(o => { if (o.isSkinnedMesh) { skel = o.skeleton; o.frustumCulled = false; o.castShadow = o.receiveShadow = true; const m = o.material; m.metalness = 0; m.roughness = 0.88; m.envMapIntensity = 0.28; if (m.roughnessMap) m.roughnessMap = null; m.specularIntensity !== undefined && (m.specularIntensity = 0.25); if (opts.recolor) recolor(m, opts.recolor); }
    if (o.isBone) for (const [k, v] of Object.entries(MAP)) if (o.name.replace(/^rp_[a-z]+_(animated|rigged)_\d+_[a-z]+_/, '').replace(/_\d+$/, '') === v) B[k] = o; });
  if (skel) skel.pose();                                  // bind pose (drop the baked clip)
  const root = new THREE.Group(); root.name = key; const inner = new THREE.Group(); root.add(inner); inner.add(model);
  model.updateMatrixWorld(true); const box = new THREE.Box3().setFromObject(model), sz = box.getSize(new THREE.Vector3()), c = box.getCenter(new THREE.Vector3());
  const H = C3.CHAR_DEF[key].h, sc = H / sz.y; inner.scale.setScalar(sc); model.position.set(-c.x, -box.min.y, -c.z);
  root.updateMatrixWorld(true);
  // canonical driver skeleton (never rendered) — same hierarchy the procedural motions are written for
  const dummy = C3.buildCharacter(key, palette); dummy.traverse(o => { if (o.isMesh) { o.geometry.dispose(); } });
  // rest data in character space
  const rootQinv = root.getWorldQuaternion(new THREE.Quaternion()).invert(), rest = {};
  for (const [k, b] of Object.entries(B)) { const q = rootQinv.clone().multiply(b.getWorldQuaternion(new THREE.Quaternion())), p = b.getWorldPosition(new THREE.Vector3()); root.worldToLocal(p); rest[k] = { q, p }; }
  const align = {};
  for (const [k, ch] of Object.entries(LIMB_CHILD)) { if (!B[k] || !B[ch]) continue; const d = rest[ch].p.clone().sub(rest[k].p).normalize(); align[k] = new THREE.Quaternion().setFromUnitVectors(d, DOWN); }
  align.handL = align.foreArmL; align.handR = align.foreArmR;
  root.userData = { rp: true, B, rest, align, dummy, H, key, inner };
  if (opts.attach) opts.attach(root, B, sc);
  return root;
}
const _q = new THREE.Quaternion(), _q2 = new THREE.Quaternion(), _p = new THREE.Quaternion();
const ORDER = ['hips', 'spine', 'chest', 'chest2', 'neck', 'head', 'shoulderL', 'upperArmL', 'foreArmL', 'handL', 'shoulderR', 'upperArmR', 'foreArmR', 'handR', 'thighL', 'shinL', 'footL', 'thighR', 'shinR', 'footR'];
export function applyPoseRP(ch, P) {
  const U = ch.userData, B = U.B, D = U.dummy; C3.applyPose(D, P); D.updateMatrixWorld(true); const DJ = D.userData.J;
  ch.updateMatrixWorld(true); const rootQ = ch.getWorldQuaternion(new THREE.Quaternion());
  const cum = name => DJ[name].getWorldQuaternion(new THREE.Quaternion());           // dummy root is at identity
  const setWorld = (bone, charQ) => { const w = rootQ.clone().multiply(charQ); bone.parent.getWorldQuaternion(_p); bone.quaternion.copy(_p.invert().multiply(w)); bone.updateMatrixWorld(true); };
  for (const k of ORDER) { const b = B[k]; if (!b) continue; const R = cum(DRIVE[k]); const a = U.align[k];
    const t = a ? R.clone().multiply(a).multiply(U.rest[k].q) : R.clone().multiply(U.rest[k].q); setWorld(b, t); }
  // face: jaw (lip-sync), eyelids (blink), eyes (gaze), brows
  const F = P.face || {}, Rh = cum('head');
  if (B.jaw) { const open = OPEN[F.mouth || 'X'] ?? 0; setWorld(B.jaw, Rh.clone().multiply(_q.setFromAxisAngle(new THREE.Vector3(1, 0, 0), open * 1.6)).multiply(U.rest.jaw.q)); }
  for (const s of ['L', 'R']) {
    const lid = B['lid' + s]; if (lid) setWorld(lid, Rh.clone().multiply(_q.setFromAxisAngle(new THREE.Vector3(1, 0, 0), (F.blink || 0) * 0.55)).multiply(U.rest['lid' + s].q));
    const eye = B['eye' + s]; if (eye) { const lk = F.look || [0, 0]; setWorld(eye, Rh.clone().multiply(_q.setFromEuler(new THREE.Euler(lk[1] * 0.25, lk[0] * 0.35, 0))).multiply(U.rest['eye' + s].q)); }
    const br = B['brow' + s]; if (br) { br.position.copy(br.userData.p0 || (br.userData.p0 = br.position.clone())); br.position.y += (F.brow || 0) * 0.15; }
  }
}
export { recolor };
// face only (jaw lip-sync, blinks, gaze, brows) on top of whatever body pose is applied
export function applyFaceRP(ch, F) { const U = ch.userData, B = U.B; ch.updateMatrixWorld(true); const rootQ = ch.getWorldQuaternion(new THREE.Quaternion());
  const headQ = rootQ.clone().invert().multiply(B.head.getWorldQuaternion(new THREE.Quaternion())), headD = headQ.multiply(U.rest.head.q.clone().invert());
  const setWorld = (bone, charQ) => { const w = rootQ.clone().multiply(charQ); bone.parent.getWorldQuaternion(_p); bone.quaternion.copy(_p.invert().multiply(w)); bone.updateMatrixWorld(true); };
  const X = new THREE.Vector3(1, 0, 0);
  if (B.jaw) setWorld(B.jaw, headD.clone().multiply(_q.setFromAxisAngle(X, (OPEN[F.mouth || 'X'] ?? 0) * 1.6)).multiply(U.rest.jaw.q));
  for (const s of ['L', 'R']) { const lid = B['lid' + s]; if (lid) setWorld(lid, headD.clone().multiply(_q.setFromAxisAngle(X, (F.blink || 0) * 0.55)).multiply(U.rest['lid' + s].q));
    const eye = B['eye' + s]; if (eye) { const lk = F.look || [0, 0]; setWorld(eye, headD.clone().multiply(_q.setFromEuler(new THREE.Euler(lk[1] * 0.25, lk[0] * 0.35, 0))).multiply(U.rest['eye' + s].q)); } } }
// spring-physics hair chain (e.g. a ponytail): verlet points hanging from a head-local anchor, rendered as a tapered tube
export function addHairChain(ch, opts) { const U = ch.userData, n = opts.segments || 7, len = opts.length || 0.32, r0 = opts.r0 || 0.035, r1 = opts.r1 || 0.012;
  const mat = new THREE.MeshStandardMaterial({ color: opts.color || '#1d1517', roughness: 0.7 }), pts = [];
  for (let i = 0; i <= n; i++) pts.push({ p: new THREE.Vector3(), o: new THREE.Vector3(), init: false });
  const mesh = new THREE.Mesh(new THREE.BufferGeometry(), mat); mesh.castShadow = true; mesh.frustumCulled = false; ch.parent ? ch.parent.add(mesh) : null; U.hairMesh = mesh;
  U.hair = { pts, n, len, r0, r1, anchor: new THREE.Vector3(...opts.anchor), mat, mesh, wind: opts.wind || 0 }; return mesh; }
export function stepHair(ch, dt, t) { const H = ch.userData.hair; if (!H) return; const B = ch.userData.B, seg = H.len / H.n;
  if (!H.mesh.parent && ch.parent) ch.parent.add(H.mesh);
  const a = H.anchor.clone(); B.head.localToWorld(a.multiplyScalar(1 / ch.userData.inner.scale.x));   // anchor given in metres, head bone is in model units
  const P = H.pts; if (!P[0].init) for (let i = 0; i <= H.n; i++) { P[i].p.copy(a).add(new THREE.Vector3(0, -seg * i, -0.02 * i)); P[i].o.copy(P[i].p); P[i].init = true; }
  P[0].p.copy(a); P[0].o.copy(a);
  const g = new THREE.Vector3(0, -9.8 * dt * dt, 0), wind = new THREE.Vector3(Math.sin(t * 1.3) * H.wind, 0, Math.cos(t * 0.9) * H.wind * 0.4).multiplyScalar(dt * dt);
  for (let i = 1; i <= H.n; i++) { const q = P[i], v = q.p.clone().sub(q.o).multiplyScalar(0.96); q.o.copy(q.p); q.p.add(v).add(g).add(wind); }
  for (let it = 0; it < 6; it++) { for (let i = 1; i <= H.n; i++) { const A = P[i - 1].p, Bp = P[i].p, d = Bp.clone().sub(A), L = d.length() || 1e-6, diff = (L - seg) / L;
      if (i === 1) Bp.addScaledVector(d, -diff); else { A.addScaledVector(d, diff * 0.5); Bp.addScaledVector(d, -diff * 0.5); } }
    // keep the hair out of the head/neck (sphere collider)
    const hc = new THREE.Vector3(); B.head.getWorldPosition(hc); hc.y += 0.08; for (let i = 1; i <= H.n; i++) { const d = P[i].p.clone().sub(hc), L = d.length(); if (L < 0.1) P[i].p.copy(hc).addScaledVector(d.normalize(), 0.1); } }
  const curve = new THREE.CatmullRomCurve3(P.map(q => q.p.clone())); const geo = new THREE.TubeGeometry(curve, H.n * 3, 1, 8, false);
  const pos = geo.attributes.position, nrm = geo.attributes.normal, cp = new THREE.Vector3();   // taper the tube
  for (let i = 0; i < pos.count; i++) { const u = Math.floor(i / 9) / (H.n * 3); curve.getPointAt(Math.min(1, u), cp); const r = H.r0 + (H.r1 - H.r0) * u; const v = new THREE.Vector3(pos.getX(i), pos.getY(i), pos.getZ(i)).sub(cp); pos.setXYZ(i, cp.x + v.x * r, cp.y + v.y * r, cp.z + v.z * r); }
  geo.computeVertexNormals(); H.mesh.geometry.dispose(); H.mesh.geometry = geo; }
