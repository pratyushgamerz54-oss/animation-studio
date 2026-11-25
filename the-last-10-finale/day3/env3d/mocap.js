// Mocap retargeting: plays clips on a hidden source skeleton (Mixamo "Soldier", "Nerd Survivor") and copies the
// per-bone rotations onto our scanned characters (char_rp.js), corrected for rest-pose and facing differences.
// Also: layered blending (lower/upper body), foot-driven root motion (no foot sliding), ground lock (no foot penetration).
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { BVHLoader } from 'three/addons/loaders/BVHLoader.js';

export const SRC_MAPS = {
  mixamo: { hips: 'Hips', spine: 'Spine', chest: 'Spine1', chest2: 'Spine2', neck: 'Neck', head: 'Head', shoulderL: 'LeftShoulder', upperArmL: 'LeftArm', foreArmL: 'LeftForeArm', handL: 'LeftHand', shoulderR: 'RightShoulder', upperArmR: 'RightArm', foreArmR: 'RightForeArm', handR: 'RightHand',
    thighL: 'LeftUpLeg', shinL: 'LeftLeg', footL: 'LeftFoot', thighR: 'RightUpLeg', shinR: 'RightLeg', footR: 'RightFoot', toeL: 'LeftToeBase', toeR: 'RightToeBase' },
  cmu: { hips: 'Hips', spine: 'LowerBack', chest: 'Spine', chest2: 'Spine1', neck: 'Neck', head: 'Head', shoulderL: 'LeftShoulder', upperArmL: 'LeftArm', foreArmL: 'LeftForeArm', handL: 'LeftHand', shoulderR: 'RightShoulder', upperArmR: 'RightArm', foreArmR: 'RightForeArm', handR: 'RightHand',
    thighL: 'LeftUpLeg', shinL: 'LeftLeg', footL: 'LeftFoot', thighR: 'RightUpLeg', shinR: 'RightLeg', footR: 'RightFoot', toeL: 'LeftToeBase', toeR: 'RightToeBase' },
  nerd: { hips: 'Spine_1', spine: 'Spine_2', chest: 'Spine_3', chest2: 'Spine_4', neck: 'Spine_5', head: 'Head', shoulderL: 'Arm_1_L', upperArmL: 'Arm_2_L', foreArmL: 'Arm_3_L', handL: 'Hand_1_L', shoulderR: 'Arm_1_R', upperArmR: 'Arm_2_R', foreArmR: 'Arm_3_R', handR: 'Hand_1_R',
    thighL: 'Leg_1_L', shinL: 'Leg_2_L', footL: 'Leg_3_L', thighR: 'Leg_1_R', shinR: 'Leg_2_R', footR: 'Leg_3_R', toeL: 'Leg_4_L', toeR: 'Leg_4_R' },
};
const CHILD = { upperArmL: 'foreArmL', foreArmL: 'handL', upperArmR: 'foreArmR', foreArmR: 'handR', thighL: 'shinL', shinL: 'footL', thighR: 'shinR', shinR: 'footR', footL: 'toeL', footR: 'toeR', shoulderL: 'upperArmL', shoulderR: 'upperArmR' };
export const ORDER = ['hips', 'spine', 'chest', 'chest2', 'neck', 'head', 'shoulderL', 'upperArmL', 'foreArmL', 'handL', 'shoulderR', 'upperArmR', 'foreArmR', 'handR', 'thighL', 'shinL', 'footL', 'thighR', 'shinR', 'footR'];
export const UPPER = new Set(['spine', 'chest', 'chest2', 'neck', 'head', 'shoulderL', 'upperArmL', 'foreArmL', 'handL', 'shoulderR', 'upperArmR', 'foreArmR', 'handR']);
const norm = n => n.replace(/^mixamorig:?/, '').replace(/_\d+$/, '');

export class Mocap {
  // CMU motion-capture (BVH): several clips, one skeleton each; zero rotations = T-pose rest; includes root motion
  static async loadBVH(files) { const out = {}; for (const [name, f] of Object.entries(files)) { const r = await new BVHLoader().loadAsync(f), grp = new THREE.Group(); grp.add(r.skeleton.bones[0]); r.clip.name = name;
      const m = new Mocap({ scene: grp, animations: [r.clip] }, SRC_MAPS.cmu); m.isBVH = true; out[name] = m; } return out; }
  static async load(file, mapName) { const g = await new GLTFLoader().loadAsync(file); return new Mocap(g, SRC_MAPS[mapName]); }
  constructor(g, map) {
    this.scene = g.scene; this.clips = Object.fromEntries(g.animations.map(a => [a.name, a])); this.B = {};
    const cand = {}; this.scene.traverse(o => { if (o.isBone) for (const [k, v] of Object.entries(map)) if (norm(o.name) === v) (cand[k] = cand[k] || []).push(o); if (o.isSkinnedMesh) { this.skel = o.skeleton; o.visible = false; } });
    this.root = new THREE.Group(); this.root.add(this.scene); this.root.updateMatrixWorld(true);
    // several nodes can share a name (props, helpers): keep the one that belongs to the body (closest to the hips)
    const hp = cand.hips[0].getWorldPosition(new THREE.Vector3());
    for (const [k, list] of Object.entries(cand)) this.B[k] = list.sort((a, b) => a.getWorldPosition(new THREE.Vector3()).distanceTo(hp) - b.getWorldPosition(new THREE.Vector3()).distanceTo(hp))[0];
    this.mixer = new THREE.AnimationMixer(this.scene); this.actions = {};
    // rest pose: the rig's own T-pose clip when it has one (bind matrices can be in another unit/axis space), else the bind pose
    if (this.clips.TPose) { const a = this.mixer.clipAction(this.clips.TPose); a.play(); this.mixer.setTime(0); this.root.updateMatrixWorld(true); this.rest = this.capture(); a.stop(); this.mixer.uncacheAction(this.clips.TPose); }
    else { if (this.skel) this.skel.pose(); this.root.updateMatrixWorld(true); this.rest = this.capture(); }
    this.restDir = this.dirs(); this.basis = this.frame();
  }
  capture() { const rq = this.root.getWorldQuaternion(new THREE.Quaternion()).invert(), out = {};
    for (const [k, b] of Object.entries(this.B)) { const p = b.getWorldPosition(new THREE.Vector3()); this.root.worldToLocal(p); out[k] = { q: rq.clone().multiply(b.getWorldQuaternion(new THREE.Quaternion())), p }; } return out; }
  dirs() { const d = {}; for (const [k, c] of Object.entries(CHILD)) if (this.rest[k] && this.rest[c]) d[k] = this.rest[c].p.clone().sub(this.rest[k].p).normalize(); return d; }
  frame() {   // rotation taking the source's own (up, forward) to (+y, +z): handles Z-up and backward-facing rigs
    const up = this.rest.head.p.clone().sub(this.rest.hips.p).normalize();
    let f = this.rest.toeL && this.rest.footL ? this.rest.toeL.p.clone().sub(this.rest.footL.p).add(this.rest.toeR.p.clone().sub(this.rest.footR.p)) : new THREE.Vector3(0, 0, 1);
    f.addScaledVector(up, -f.dot(up)).normalize(); const r = new THREE.Vector3().crossVectors(up, f).normalize();
    const m = new THREE.Matrix4().makeBasis(r, up, f); return new THREE.Quaternion().setFromRotationMatrix(m).invert(); }
  // pose the source at clip time t, return per-bone character-space delta rotations (relative to rest)
  sample(name, t, loop = true) { const clip = this.clips[name]; if (!clip) throw new Error('no clip ' + name);
    let a = this.actions[name]; if (!a) { a = this.actions[name] = this.mixer.clipAction(clip); a.play(); }
    for (const [n, x] of Object.entries(this.actions)) x.enabled = n === name;
    const tt = loop ? ((t % clip.duration) + clip.duration) % clip.duration : Math.min(t, clip.duration - 1e-3); this.mixer.setTime(tt); this.root.updateMatrixWorld(true);
    const cur = this.capture(), D = {}; for (const k of Object.keys(cur)) D[k] = cur[k].q.clone().multiply(this.rest[k].q.clone().invert());
    // remove the clip's constant body yaw (e.g. Mixamo idles stand turned ~40°) so the character faces where we point it
    const yo = this.yawOffset(name); if (yo) { const qy = new THREE.Quaternion().setFromAxisAngle(this.upAxis(), -yo); for (const k of Object.keys(D)) D[k] = qy.clone().multiply(D[k]); }
    D._pos = cur; D._hip = cur.hips.p.clone().applyQuaternion(this.basis).applyAxisAngle(new THREE.Vector3(0, 1, 0), -(this._yo && this._yo[name] || 0)); D._height = this.rest.head.p.clone().sub(this.rest.footL.p).applyQuaternion(this.basis).y; return D; }
  upAxis() { return new THREE.Vector3(0, 1, 0).applyQuaternion(this.basis.clone().invert()); }
  yawOffset(name) { this._yo = this._yo || {}; if (name in this._yo) return this._yo[name]; this._yo[name] = 0; const clip = this.clips[name]; let sx = 0, sz = 0;
    for (let i = 0; i < 12; i++) { const D = this.sample(name, clip.duration * i / 12); const f = new THREE.Vector3(0, 0, 1).applyQuaternion(this.basis.clone().invert()).applyQuaternion(D.hips).applyQuaternion(this.basis); sx += f.x; sz += f.z; }
    const y = Math.atan2(sx, sz); this._yo[name] = Math.abs(y) > 0.15 ? y : 0; return this._yo[name]; }
}
// blend two delta sets; w = weight of b; mask (Set) limits b to those bones
export function blendD(a, b, w, mask = null) { if (w <= 0) return a; const o = {};
  if (a._pos && b._pos) { o._pos = {}; for (const k of Object.keys(a._pos)) { const ww = mask && !mask.has(k) ? 0 : Math.min(1, w); o._pos[k] = { p: a._pos[k].p.clone().lerp(b._pos[k].p, ww) }; } } else o._pos = a._pos || b._pos;
  for (const k of Object.keys(a)) if (k[0] === '_' && k !== '_pos') o[k] = a[k];
  for (const k of new Set([...Object.keys(a), ...Object.keys(b)].filter(k => k[0] !== '_'))) { const qa = a[k] || new THREE.Quaternion(), qb = b[k] || new THREE.Quaternion(); const ww = mask && !mask.has(k) ? 0 : w; o[k] = qa.clone().slerp(qb, Math.min(1, ww)); } return o; }

// bind a source to a target character (rest/facing correction cached per pair)
export function bind(src, ch) { const U = ch.userData, key = src === ch.userData._srcCache?.src ? null : 1;
  U._bind = U._bind || new Map(); if (U._bind.has(src)) return U._bind.get(src);
  // facing correction (source forward → target forward = +z)
  const F = src.basis.clone(), Fi = F.clone().invert();
  const align = {}; for (const k of ORDER) { const sd = src.restDir[k], b = U.B[k], c = { upperArmL: 'foreArmL', foreArmL: 'handL', upperArmR: 'foreArmR', foreArmR: 'handR', thighL: 'shinL', shinL: 'footL', thighR: 'shinR', shinR: 'footR', shoulderL: 'upperArmL', shoulderR: 'upperArmR' }[k];
    if (sd && b && c && U.rest[c]) { const td = U.rest[c].p.clone().sub(U.rest[k].p).normalize(); align[k] = new THREE.Quaternion().setFromUnitVectors(td, sd.clone().applyQuaternion(F)); } }
  const r = { F, Fi, align }; U._bind.set(src, r); return r; }

const _p = new THREE.Quaternion();
// apply source deltas to the character bones; face/jaw handled separately
export function applyD(ch, src, D) { const U = ch.userData, B = U.B, bd = bind(src, ch);
  ch.updateMatrixWorld(true); const rootQ = ch.getWorldQuaternion(new THREE.Quaternion());
  const SW = { upperArmL: 'foreArmL', foreArmL: 'handL', upperArmR: 'foreArmR', foreArmR: 'handR', thighL: 'shinL', shinL: 'footL', thighR: 'shinR', shinR: 'footR' };
  for (const k of ORDER) { const b = B[k]; if (!b || !D[k]) continue;
    if (U.isC3 && (k === 'handL' || k === 'handR')) { b.rotation.set(0, 0, 0); b.updateMatrixWorld(true); continue; }
    const c = SW[k];
    if (c && D._pos && D._pos[k] && D._pos[c] && U.rest[c]) {
      const want = D._pos[c].p.clone().sub(D._pos[k].p).applyQuaternion(bd.F).normalize(), td = U.rest[c].p.clone().sub(U.rest[k].p).normalize();
      // keep the joint's bend plane from the parent: swing from the rest direction carried by the parent's current rotation
      const pq = rootQ.clone().invert().multiply(b.parent.getWorldQuaternion(new THREE.Quaternion())), pr = U.rest[k].parentQ || new THREE.Quaternion();
      const carried = pq.clone().multiply(pr.clone().invert()), base = carried.clone().multiply(U.rest[k].q), tdNow = td.clone().applyQuaternion(carried);
      const t = new THREE.Quaternion().setFromUnitVectors(tdNow, want).multiply(base);
      const w = rootQ.clone().multiply(t); b.parent.getWorldQuaternion(_p); b.quaternion.copy(_p.invert().multiply(w)); b.updateMatrixWorld(true); continue; }
    let d = bd.F.clone().multiply(D[k]).multiply(bd.Fi);                       // delta expressed in target facing
    if (k === 'neck' || k === 'head') d = new THREE.Quaternion().slerp(d, 0.5);
    const t = d.multiply(bd.align[k] || new THREE.Quaternion()).multiply(U.rest[k].q);
    const w = rootQ.clone().multiply(t); b.parent.getWorldQuaternion(_p); b.quaternion.copy(_p.invert().multiply(w)); b.updateMatrixWorld(true); } }

// foot-driven locomotion: move the character so the planted foot does not slide; keep the lowest sole on the ground
export function plantFeet(ch, state, opts = {}) { const U = ch.userData, B = U.B; ch.updateMatrixWorld(true);
  const fl = B.footL.getWorldPosition(new THREE.Vector3()), fr = B.footR.getWorldPosition(new THREE.Vector3());
  // procedural characters: use the real lowest point of each shoe (sole/heel/toe follow the foot's pitch), not the ankle height
  const soleY = f => { const b = new THREE.Box3().setFromObject(f, true); return b.min.y; };
  const soleL = U.isC3 ? soleY(B.footL) : fl.y - U.rest.footL.p.y, soleR = U.isC3 ? soleY(B.footR) : fr.y - U.rest.footR.p.y, low = Math.min(soleL, soleR);
  ch.position.y -= low; ch.updateMatrixWorld(true);
  const stance = soleL < soleR ? 'L' : 'R', sp = (stance === 'L' ? B.footL : B.footR).getWorldPosition(new THREE.Vector3());
  if (opts.move !== false && state.stance === stance && state.p) { const d = state.p.clone().sub(sp); d.y = 0;
    if (opts.forwardOnly) { const f = new THREE.Vector3(0, 0, 1).applyQuaternion(ch.quaternion); f.y = 0; f.normalize(); const s = Math.max(0, d.dot(f)); d.copy(f.multiplyScalar(s)); }
    ch.position.add(d); ch.updateMatrixWorld(true); sp.add(d); }
  state.stance = stance; state.p = sp; return state; }

// make a procedural char3d character a retarget target (its joint groups are the bones; rest = zero rotations)
export function adoptC3(ch) { /* see also restParents() */ const J = ch.userData.J, B = {}; for (const k of ORDER) if (J[k]) B[k] = J[k];
  ch.updateMatrixWorld(true); const rq = ch.getWorldQuaternion(new THREE.Quaternion()).invert(), rest = {};
  for (const [k, b] of Object.entries(B)) { const p = b.getWorldPosition(new THREE.Vector3()); ch.worldToLocal(p); rest[k] = { q: rq.clone().multiply(b.getWorldQuaternion(new THREE.Quaternion())), p }; }
  // char3d feet: sole sits ~0.04·H below the ankle joint
  ch.userData.B = B; ch.userData.rest = rest; ch.userData.isC3 = true; ch.userData.inner = ch.userData.inner || { scale: { x: 1 } }; return ch; }
// settle loose objects with the physics engine before the shot starts (no floating rubble)
export function settle(world, steps = 240) { for (let i = 0; i < steps; i++) world.step(1 / 60); }

export function restParents(ch) { ch.updateMatrixWorld(true); const rq = ch.getWorldQuaternion(new THREE.Quaternion()).invert(), U = ch.userData;
  for (const [k, b] of Object.entries(U.B)) if (U.rest[k]) U.rest[k].parentQ = rq.clone().multiply(b.parent.getWorldQuaternion(new THREE.Quaternion())); }

// root motion: move the character by the source hip travel (scaled to the character, rotated to its facing)
export function rootMotion(ch, D, state, scale) { const h = D._hip.clone(); h.y = 0; if (!state.prev) { state.prev = h; return; }
  const d = h.clone().sub(state.prev); state.prev = h; if (d.length() > 0.5 * (1 / scale)) return;   // loop wrap
  d.multiplyScalar(scale).applyQuaternion(ch.quaternion); ch.position.add(d); }
