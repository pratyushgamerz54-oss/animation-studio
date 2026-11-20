/* ---------- dark cinematic helpers ---------- */
const BT = i => (TIMING.beats && TIMING.beats[i]) || [0, 1.5, 3, 4.5];
const CR = {red: '#b3262a', dred: '#6e1517', bone: '#e9e4da', steel: '#8a9099', cool: '#a9bccb', char: '#16171c'};
function vign(a = .75) { const v = ctx.createRadialGradient(W / 2, H * .45, 320, W / 2, H / 2, 1250); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, `rgba(0,0,0,${a})`); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H); }
function cam(t, d, z0 = 1, z1 = 1.07, ox = 0, oy = 0, cx = W / 2, cy = H / 2) { const k = io(t / d), z = lerp(z0, z1, k); ctx.translate(cx + ox * k, cy + oy * k); ctx.scale(z, z); ctx.translate(-cx, -cy); }
function bgChar(top = '#0b0b0e', mid = '#17181d', bot = '#070708') { const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, top); g.addColorStop(.5, mid); g.addColorStop(1, bot); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); }
function glowAt(x, y, r, rgb = '179,38,42', a = .5) { const g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, `rgba(${rgb},${a})`); g.addColorStop(1, `rgba(${rgb},0)`); ctx.fillStyle = g; ctx.fillRect(x - r, y - r, r * 2, r * 2); }
function haze(n = 7, rgb = '140,140,150', a = .05) { for (let i = 0; i < n; i++) { const x = (hash(i * 3) * W + NOW * 12 * (hash(i) - .5) + W) % W, y = hash(i * 7 + 1) * H; glowAt(x, y, 300 + hash(i + 5) * 300, rgb, a); } }
function smooth(pts, closed = true) { const n = pts.length, Pp = i => pts[closed ? (i + n) % n : Math.max(0, Math.min(n - 1, i))]; ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
  for (let i = 0; i < (closed ? n : n - 1); i++) { const p0 = Pp(i - 1), p1 = Pp(i), p2 = Pp(i + 1), p3 = Pp(i + 2);
    const c1 = p1[2] ? p1 : [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6], c2 = p2[2] ? p2 : [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    ctx.bezierCurveTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1]); } if (closed) ctx.closePath(); }
function eyeIcon(x, y, r, k, col = CR.red) {
  if (k <= 0) return; ctx.save(); ctx.translate(x, y); ctx.scale(k, k);
  ctx.shadowColor = col; ctx.shadowBlur = 40; ctx.beginPath(); ctx.moveTo(-r, 0); ctx.quadraticCurveTo(0, -r * .75, r, 0); ctx.quadraticCurveTo(0, r * .75, -r, 0); ctx.closePath();
  ctx.fillStyle = '#0d0d10'; ctx.fill(); ctx.strokeStyle = col; ctx.lineWidth = r * .06; ctx.stroke(); ctx.shadowBlur = 0;
  const g = ctx.createRadialGradient(0, 0, 0, 0, 0, r * .42); g.addColorStop(0, '#ff6a5c'); g.addColorStop(.6, col); g.addColorStop(1, '#3a0808');
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, r * .4, 0, 7); ctx.fill(); ctx.fillStyle = '#050505'; ctx.beginPath(); ctx.arc(0, 0, r * .16, 0, 7); ctx.fill();
  ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.arc(-r * .12, -r * .12, r * .06, 0, 7); ctx.fill(); ctx.restore();
}
function angryFace(x, y, r) { ctx.save(); ctx.translate(x, y); ctx.fillStyle = '#e0563f'; ctx.beginPath(); ctx.arc(0, 0, r, 0, 7); ctx.fill(); ctx.strokeStyle = '#2a0a06'; ctx.lineWidth = r * .1; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-r * .55, -r * .45); ctx.lineTo(-r * .15, -r * .25); ctx.moveTo(r * .55, -r * .45); ctx.lineTo(r * .15, -r * .25); ctx.stroke();
  ctx.fillStyle = '#2a0a06'; ctx.beginPath(); ctx.arc(-r * .32, -r * .05, r * .1, 0, 7); ctx.arc(r * .32, -r * .05, r * .1, 0, 7); ctx.fill();
  ctx.beginPath(); ctx.moveTo(-r * .4, r * .5); ctx.quadraticCurveTo(0, r * .2, r * .4, r * .5); ctx.stroke(); ctx.restore(); }
function phoneBody(x, y, w, h, rot, screen, glow = .35) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
  if (glow) glowAt(0, 0, Math.max(w, h) * .9, '170,190,210', glow * .45);
  rr(-w / 2, -h / 2, w, h, w * .13); ctx.fillStyle = '#09090b'; ctx.fill(); ctx.strokeStyle = '#3a3b42'; ctx.lineWidth = Math.max(3, w * .015); ctx.stroke();
  ctx.save(); rr(-w / 2 + w * .045, -h / 2 + w * .05, w * .91, h - w * .1, w * .09); ctx.clip();
  ctx.fillStyle = '#101116'; ctx.fillRect(-w / 2, -h / 2, w, h); screen(-w / 2 + w * .045, -h / 2 + w * .05, w * .91, h - w * .1); ctx.restore();
  ctx.fillStyle = '#000'; rr(-w * .12, -h / 2 + w * .07, w * .24, w * .05, w * .025); ctx.fill();
  ctx.restore();
}
function feed(x, y, w, h, scroll, opt = {}) {
  const ch = opt.ch || w * .62, gap = w * .06, step = ch + gap, base = Math.floor(scroll / step);
  for (let k = -1; k < h / step + 2; k++) {
    const idx = base + k, yy = y - (scroll % step) + k * step, red = opt.red && idx % 4 === 2;
    ctx.save(); rr(x + w * .05, yy, w * .9, ch, w * .05); ctx.fillStyle = red ? 'rgba(150,32,34,.95)' : '#1d1e25'; ctx.fill();
    ctx.fillStyle = red ? '#e7b3ad' : '#3a3c46'; ctx.beginPath(); ctx.arc(x + w * .16, yy + ch * .16, ch * .08, 0, 7); ctx.fill();
    ctx.fillRect(x + w * .27, yy + ch * .11, w * .4, ch * .045); ctx.fillRect(x + w * .27, yy + ch * .19, w * .25, ch * .035);
    ctx.fillStyle = red ? 'rgba(255,255,255,.12)' : '#2a2c35'; ctx.fillRect(x + w * .1, yy + ch * .3, w * .8, ch * .52);
    if (red) angryFace(x + w * .5, yy + ch * .56, ch * .17);
    ctx.fillStyle = red ? '#f0c9c4' : '#4a4c57'; for (let b = 0; b < 3; b++) ctx.fillRect(x + w * (.12 + b * .2), yy + ch * .88, w * .1, ch * .04);
    ctx.restore();
  }
}
function crowdRow(y, n, s, col, seed, al = 1, w = W) { for (let i = 0; i < n; i++) { const x = (i + .5 + (hash(seed + i) - .5) * .5) * w / n; person(x, y + hash(seed * 3 + i) * 8, s * (.9 + hash(i + seed) * .2), col, al); } }
function isoBar(x, y, w, d, h, front, top, side) {
  ctx.fillStyle = front; ctx.fillRect(x, y - h, w, h);
  ctx.fillStyle = side; ctx.beginPath(); ctx.moveTo(x + w, y - h); ctx.lineTo(x + w + d, y - h - d * .6); ctx.lineTo(x + w + d, y - d * .6); ctx.lineTo(x + w, y); ctx.closePath(); ctx.fill();
  ctx.fillStyle = top; ctx.beginPath(); ctx.moveTo(x, y - h); ctx.lineTo(x + d, y - h - d * .6); ctx.lineTo(x + w + d, y - h - d * .6); ctx.lineTo(x + w, y - h); ctx.closePath(); ctx.fill();
}
function parliament(cx, by, s, k) {
  if (k <= 0) return; ctx.save(); ctx.translate(cx, by + (1 - eo(k)) * 120); ctx.scale(s, s); ctx.globalAlpha *= clamp(k * 1.5);
  glowAt(0, -160, 520, '179,38,42', .35);
  ctx.fillStyle = '#060607';
  ctx.beginPath(); ctx.ellipse(0, 0, 470, 60, 0, 0, 7); ctx.fill(); ctx.fillRect(-470, -150, 940, 150);
  ctx.beginPath(); ctx.ellipse(0, -150, 470, 50, 0, Math.PI, 0); ctx.fill();
  ctx.fillRect(-300, -240, 600, 100); ctx.beginPath(); ctx.ellipse(0, -240, 300, 34, 0, Math.PI, 0); ctx.fill();
  ctx.beginPath(); ctx.ellipse(0, -270, 120, 110, 0, Math.PI, 0); ctx.fill(); ctx.fillRect(-3, -440, 6, 80);
  ctx.fillStyle = 'rgba(179,38,42,.55)';
  for (let i = -15; i <= 15; i++) { const x = i * 29, yb = Math.sqrt(Math.max(0, 1 - (x / 470) ** 2)) * 30; ctx.fillRect(x - 6, -135 + yb * .2, 12, 120); }
  ctx.fillStyle = 'rgba(179,38,42,.35)'; for (let i = -9; i <= 9; i++) ctx.fillRect(i * 31 - 5, -228, 10, 80);
  ctx.restore();
}
function makeVillage() {
  const c = mk(), g = c.getContext('2d'), r = rng(81), vx = 540, vy = 900;
  let gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#9a9a9a'); gr.addColorStop(.45, '#c9c9c9'); gr.addColorStop(1, '#4a4a4a'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  [-1, 1].forEach(sd => { for (let k = 0; k < 9; k++) { const d0 = k / 9, d1 = (k + 1) / 9, f = d => Math.pow(d, .65);
    const xn = sd < 0 ? lerp(0, vx - 90, f(d0)) : lerp(W, vx + 90, f(d0)), xf = sd < 0 ? lerp(0, vx - 90, f(d1)) : lerp(W, vx + 90, f(d1));
    const top0 = lerp(260 - r() * 160, vy - 140, f(d0)), top1 = lerp(260 - r() * 160, vy - 140, f(d1)), b0 = lerp(1700, vy + 60, f(d0)), b1 = lerp(1700, vy + 60, f(d1));
    const sh = Math.round(60 + r() * 70 + d0 * 60); g.fillStyle = `rgb(${sh},${sh},${sh})`;
    g.beginPath(); g.moveTo(xn, top0); g.lineTo(xf, top1); g.lineTo(xf, b1); g.lineTo(xn, b0); g.closePath(); g.fill();
    g.fillStyle = `rgb(${sh - 30},${sh - 30},${sh - 30})`; const wy = lerp(top0, b0, .35); g.fillRect(Math.min(xn, xf) + Math.abs(xf - xn) * .3, wy, Math.abs(xf - xn) * .3, (b0 - top0) * .14);
    g.fillRect(Math.min(xn, xf), lerp(top0, b0, .55), Math.abs(xf - xn), 8 * (1 - d0)); } });
  g.strokeStyle = '#2a2a2a'; g.lineWidth = 2; for (let i = 0; i < 5; i++) { g.beginPath(); g.moveTo(0, 300 + i * 40); g.quadraticCurveTo(540, 520 + i * 30, W, 280 + i * 45); g.stroke(); }
  g.fillStyle = '#5a5a5a'; g.beginPath(); g.moveTo(vx - 90, vy + 60); g.lineTo(vx + 90, vy + 60); g.lineTo(W, 1920); g.lineTo(0, 1920); g.closePath(); g.fill();
  for (let row = 0; row < 4; row++) { const y = vy + 90 + row * 70, s = .5 + row * .35, n = 5 + row * 3;
    for (let i = 0; i < n; i++) { const x = vx + (i - (n - 1) / 2) * (40 + row * 38) + (r() - .5) * 20, sh = 40 + row * 4; g.fillStyle = `rgb(${sh},${sh},${sh})`;
      g.beginPath(); g.arc(x, y - 60 * s, 16 * s, 0, 7); g.fill(); g.fillRect(x - 20 * s, y - 44 * s, 40 * s, 70 * s); } }
  return toneize(c, [14, 12, 12], [196, 186, 176], 26, .65);
}
function makeRallyCrowd() {
  const c = mk(1080, 420), g = c.getContext('2d'), r = rng(91);
  for (let row = 0; row < 7; row++) { const y = 140 + row * 44, s = .45 + row * .14, n = 22 - row;
    for (let i = 0; i < n; i++) { const x = (i + .5 + (r() - .5) * .6) * 1080 / n, sh = 8 + row * 3; g.fillStyle = `rgb(${sh},${sh},${sh + 2})`;
      g.beginPath(); g.arc(x, y - 30 * s, 22 * s, 0, 7); g.fill(); g.beginPath(); g.ellipse(x, y + 30 * s, 40 * s, 44 * s, 0, Math.PI, 0); g.fill(); g.fillRect(x - 40 * s, y + 30 * s - 1, 80 * s, 60 * s);
      if (r() > .86) { g.fillRect(x + 18 * s, y - 120 * s, 4 * s, 110 * s); g.fillStyle = r() > .5 ? '#7d1d1f' : '#4a4b52'; g.fillRect(x + 22 * s, y - 120 * s, 46 * s, 30 * s); }
      if (r() > .8) { g.strokeStyle = `rgb(${sh},${sh},${sh})`; g.lineWidth = 10 * s; g.beginPath(); g.moveTo(x + 20 * s, y); g.lineTo(x + 34 * s, y - 70 * s); g.stroke(); } } }
  return c;
}

/* ---------- scenes ---------- */
const S = [
/* 0 HOOK — phone in the dark */
{ file: 1, tin: null, sfx: [[0, 'impact_big'], [.3, 'vibrate'], [.6, 'ticks', 2.4], [BT(0)[2] - .1, 'whoosh'], [BT(0)[2] + .1, 'rise', 1.2]],
  draw(t, d) {
    const b = BT(0), zt = P(t, b[2], d - b[2]);
    bgChar('#050506', '#0e0f13', '#030304'); haze(5, '120,130,150', .04);
    ctx.save(); const z = lerp(1, 2.6, io(zt)); ctx.translate(700, 960); ctx.scale(z, z); ctx.translate(-700, -960); cam(t, d, 1, 1.05);
    glowAt(650, 900, 700, '150,175,200', .22);
    ctx.fillStyle = '#020203';
    smooth([[250, 820], [270, 650], [380, 545], [520, 585], [560, 690], [575, 730], [612, 790, 1], [585, 812], [592, 840], [578, 866], [575, 900], [520, 950], [500, 1030], [660, 1150], [730, 1400], [740, 1920, 1], [-20, 1920, 1], [-20, 1240], [210, 1080], [255, 960]]);
    ctx.fill();
    ctx.save(); ctx.strokeStyle = 'rgba(190,210,230,.75)'; ctx.lineWidth = 4; ctx.shadowColor = '#cfe3f2'; ctx.shadowBlur = 18;
    smooth([[520, 585], [560, 690], [575, 730], [612, 790, 1], [585, 812], [592, 840], [578, 866], [575, 900], [520, 950]], false); ctx.stroke(); ctx.restore();
    ctx.fillStyle = 'rgba(200,220,235,.85)'; ctx.beginPath(); ctx.ellipse(538, 720, 12, 5, 0, 0, 7); ctx.fill();
    ctx.fillStyle = 'rgba(160,190,215,.12)'; ctx.beginPath(); ctx.moveTo(610, 830); ctx.lineTo(760, 880); ctx.lineTo(820, 1120); ctx.lineTo(560, 860); ctx.closePath(); ctx.fill();
    phoneBody(710, 1010, 230, 440, -.22, (x, y, w, h) => { feed(x, y, w, h, t * 520, {red: 1}); if (zt > 0) { ctx.fillStyle = `rgba(8,8,10,${eo(zt)})`; ctx.fillRect(x, y, w, h); eyeIcon(x + w / 2, y + h / 2, w * .32, eo(P(zt, .1, .5))); } });
    ctx.fillStyle = '#020203'; smooth([[640, 1200], [700, 1150], [790, 1130], [830, 1200], [800, 1300], [700, 1330]]); ctx.fill();
    ctx.restore();
    const k = P(t, .25, .35), hrs = Math.min(5, 5 * eo(P(t, .3, 1.6)));
    pop(540, 330, k * (1 - zt), () => {
      T(num(hrs, 1) + ' घंटे', 0, 0, 170, CR.bone, {a: 'center', f: F.bold, w: 800, glow: 'rgba(179,38,42,.8)', gb: 30});
      T('हर दिन · फ़ोन की स्क्रीन पर', 0, 64, 40, CR.steel, {a: 'center', w: 500});
      ctx.strokeStyle = CR.red; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(-330, -60, 46, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (t % 1)); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,.2)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(-330, -60, 46, 0, 7); ctx.stroke();
    });
    T('स्रोत: EY रिपोर्ट 2025', 540, 1290, 26, 'rgba(200,205,215,.55)', {a: 'center', w: 500, al: 1 - zt});
    vign(.8);
  }},
/* 1 map + parliament */
{ file: 2, tin: 'zoomin', sfx: [[.1, 'braam'], [.3, 'ticks', 1.4], [BT(1)[1], 'impact'], [BT(1)[2], 'braam'], [BT(1)[2] + .2, 'rise', 1.5]],
  draw(t, d) {
    const b = BT(1); bgChar('#0a0a0d', '#141419', '#050506'); haze(5, '179,38,42', .04);
    ctx.save(); cam(t, d, 1, 1.08, 0, 40);
    const pk = P(t, b[2], .9);
    drawMap({cx: 540, cy: lerp(880, 760, eo(pk)), scale: lerp(29, 25, eo(pk)), tilt: .95, yaw: lerp(-.25, .1, io(t / d)), top: ['#1d1e24', '#101115'],
      side: [[8, 8, 10], [40, 18, 20]], edge: '#c4363a', grid: 'rgba(179,38,42,.08)', dots: {k: eo(P(t, .2, Math.max(.5, b[1]))), color: 'rgba(235,90,80,.9)'},
      pins: Object.values(CITY).map((c, i) => ({lon: c[0], lat: c[1], h: 2 + hash(i) * 1.6, color: '#d23a3a', k: P(t, .4 + i * .1, .3)}))});
    parliament(540, 1290, .95, pk);
    ctx.restore();
    const s1 = P(t, 0, .3) * (1 - P(t, b[1] - .15, .15)), s2 = P(t, b[1], .3);
    pop(540, 330, s1, () => { T(num(Math.round(88 * eo(P(t, .1, 1.2)))) + ' करोड़+', 0, 0, 150, CR.bone, {a: 'center', f: F.bold, w: 800}); T('इंटरनेट यूज़र', 0, 60, 42, CR.steel, {a: 'center', w: 500}); });
    pop(540, 330, s2, () => { T(num(Math.round(97 * eo(P(t, b[1], 1)))) + ' करोड़', 0, 0, 150, CR.bone, {a: 'center', f: F.bold, w: 800, glow: 'rgba(179,38,42,.7)', gb: 30}); T('वोटर · लोकसभा 2024', 0, 60, 42, CR.steel, {a: 'center', w: 500}); });
    T('स्रोत: IAMAI–Kantar 2024 · चुनाव आयोग', 540, 1330, 24, 'rgba(200,205,215,.5)', {a: 'center', w: 500});
    vign();
  }},
/* 2 chessboard — the invisible game */
{ file: 3, tin: 'zoomin', sfx: [[.1, 'impact_small'], [.4, 'typewriter', 1], [BT(2)[1], 'string'], [BT(2)[1] + .2, 'braam']],
  draw(t, d) {
    const b = BT(2); bgChar('#08080a', '#121216', '#040405');
    ctx.save(); cam(t, d, 1.04, 1.12, 0, -60);
    const vx = 540, vy = 380, y0 = 760, y1 = 1500;
    for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) {
      const ya = lerp(y0, y1, (r / 8) ** 1.25), yb = lerp(y0, y1, ((r + 1) / 8) ** 1.25), wa = lerp(620, 1500, (r / 8) ** 1.25), wb = lerp(620, 1500, ((r + 1) / 8) ** 1.25);
      const xa = vx - wa / 2 + wa * c / 8, xa2 = vx - wa / 2 + wa * (c + 1) / 8, xb = vx - wb / 2 + wb * c / 8, xb2 = vx - wb / 2 + wb * (c + 1) / 8;
      ctx.fillStyle = (r + c) % 2 ? '#1c1c21' : '#3a1416'; ctx.beginPath(); ctx.moveTo(xa, ya); ctx.lineTo(xa2, ya); ctx.lineTo(xb2, yb); ctx.lineTo(xb, yb); ctx.closePath(); ctx.fill();
    }
    const pull = P(t, b[1], .8);
    for (let r = 0; r < 6; r++) for (let c = 0; c < 8; c++) { if (hash(r * 8 + c) < .35) continue;
      const f = ((r + .5) / 8) ** 1.25, y = lerp(y0, y1, f) + 10, w = lerp(620, 1500, f), x = vx - w / 2 + w * (c + .5) / 8, s = lerp(12, 34, f);
      const sway = Math.sin(NOW * 2 + r + c) * 3 * pull;
      ctx.save(); ctx.translate(x, y); ctx.rotate(sway * .02); person(0, 0, s, '#060607', 1); ctx.restore();
      ctx.strokeStyle = `rgba(200,50,50,${.45 * eo(P(t, .6 + (r * 8 + c) * .01, .5))})`; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(x, y - s * 1.7); ctx.lineTo(lerp(x, vx, .4), lerp(y - s * 1.7, 140, 1) - pull * 30); ctx.stroke();
    }
    ctx.globalAlpha = eo(P(t, b[1] - .2, .8)); ctx.fillStyle = '#030304';
    smooth([[300, 60 - pull * 30], [430, 30], [520, 110], [560, 40], [640, 120], [690, 50], [760, 140], [800, 80], [820, 200], [700, 260], [440, 240], [320, 180]]); ctx.fill();
    ctx.globalAlpha = 1; ctx.restore();
    glowAt(540, 300, 500, '179,38,42', .18);
    T(typed('अदृश्य खेल', P(t, .4, 1)), 540, 470, 140, CR.bone, {a: 'center', f: F.head, w: 400, glow: 'rgba(179,38,42,.7)', gb: 30});
    T('THE INVISIBLE GAME', 540, 530, 30, 'rgba(200,60,60,.8)', {a: 'center', f: F.mono, w: 700, al: P(t, 1.2, .5)});
    vign(.85);
  }},
/* 3 algorithm */
{ file: 4, tin: 'glitch', sfx: [[.1, 'pulse', 1.5], [BT(3)[1], 'impact_small'], [BT(3)[2], 'notif'], [BT(3)[2] + .3, 'notif'], [BT(3)[3], 'impact'], [BT(3)[3] + .1, 'blips']],
  draw(t, d) {
    const b = BT(3); bgChar('#08080b', '#121218', '#040405');
    ctx.save(); cam(t, d, 1, 1.06);
    for (let i = 0; i < 4; i++) { ctx.strokeStyle = `rgba(179,38,42,${.25 - i * .05})`; ctx.lineWidth = 3; ctx.setLineDash([14, 18]); ctx.lineDashOffset = NOW * (i % 2 ? 60 : -60);
      ctx.beginPath(); ctx.arc(540, 560, 200 + i * 50, 0, 7); ctx.stroke(); } ctx.setLineDash([]);
    eyeIcon(540, 560, 170, eo(P(t, .1, .5)));
    T('ALGORITHM', 540, 330, 34, 'rgba(210,70,70,.85)', {a: 'center', f: F.mono, w: 700});
    const focus = P(t, b[1], .5);
    if (focus > 0) { ctx.strokeStyle = `rgba(255,255,255,${.7 * focus})`; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(540 - 260, 560); ctx.lineTo(540 - 190, 560); ctx.moveTo(540 + 190, 560); ctx.lineTo(540 + 260, 560); ctx.moveTo(540, 300); ctx.lineTo(540, 360); ctx.stroke();
      T('आपका ध्यान', 540, 820, 64, CR.bone, {a: 'center', f: F.bold, w: 800, al: focus}); }
    const ang = P(t, b[2], .6);
    for (let i = 0; i < 9; i++) { const ph = (NOW * .45 + i / 9) % 1, x = 160 + (i % 3) * 380 + Math.sin(i * 2) * 40, y = lerp(1350, 760, ph), s = lerp(1, .55, ph);
      if (ang > 0 && i === 4) continue;
      ctx.save(); ctx.globalAlpha = (1 - ph) * .8; ctx.translate(x, y); ctx.scale(s, s); rr(-90, -60, 180, 120, 12); ctx.fillStyle = '#1e1f26'; ctx.fill(); ctx.fillStyle = '#3a3c46'; ctx.fillRect(-70, -40, 90, 10); ctx.fillRect(-70, -20, 140, 50); ctx.restore(); }
    if (ang > 0) {
      const grow = eo(ang), x = 540, y = lerp(1180, 1040, grow), s = lerp(.6, 1.5, grow);
      const spread = P(t, b[3], 1.5);
      for (let c = 0; c < 10 * spread; c++) { const a = c / 10 * Math.PI * 2 + NOW * .3, r = 260 * eo(spread); ctx.save(); ctx.globalAlpha = .55; ctx.translate(x + Math.cos(a) * r * 1.6, y + Math.sin(a) * r * .6); ctx.scale(.45, .45); rr(-90, -60, 180, 120, 12); ctx.fillStyle = '#7d1d1f'; ctx.fill(); angryFace(0, 0, 36); ctx.restore(); }
      ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.shadowColor = CR.red; ctx.shadowBlur = 40; rr(-110, -75, 220, 150, 14); ctx.fillStyle = '#9b2224'; ctx.fill(); ctx.shadowBlur = 0; angryFace(0, -6, 42);
      T('गुस्सा', 0, 64, 26, '#fff', {a: 'center', f: F.bold, w: 800}); ctx.restore();
      const shares = Math.round(lerp(120, 98000, eo(P(t, b[2], d - b[2]))));
      T('↗ ' + num(shares) + ' शेयर', 540, 1290, 44, '#f0b4ae', {a: 'center', f: F.mono, w: 700});
    }
    ctx.restore(); vign(.8);
  }},
/* 4 network race — false vs true */
{ file: 5, tin: 'whip', sfx: [[.1, 'impact_small'], [.3, 'blips'], [1.2, 'blips'], [BT(4)[1] + .1, 'impact'], [BT(4)[1] + 1.2, 'stamp']],
  draw(t, d) {
    const b = BT(4); bgChar('#07070a', '#111116', '#040405');
    if (!NET) buildNet();
    const fT = (t - .2) / .16, tT = (t - .2) / .96;
    ctx.lineWidth = 1.5; for (const [i, j] of NET.edges) { const a = NET.nodes[i], c = NET.nodes[j]; const lit = NET.hop[i] < fT && NET.hop[j] < fT;
      ctx.strokeStyle = lit ? 'rgba(210,50,50,.55)' : 'rgba(120,125,135,.15)'; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(c[0], c[1]); ctx.stroke(); }
    let nf = 0, nt = 0;
    NET.nodes.forEach((p, i) => { const f = NET.hop[i] < fT, tr = NET.hop[i] < tT; if (f) nf++; if (tr) nt++;
      ctx.fillStyle = f ? '#e04444' : '#3a3c44'; ctx.beginPath(); ctx.arc(p[0], p[1], f ? 7 : 5, 0, 7); ctx.fill();
      if (tr) { ctx.strokeStyle = '#f2f2f2'; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(p[0], p[1], 11, 0, 7); ctx.stroke(); } });
    const N = NET.nodes.length;
    T('झूठ', 120, 300, 56, '#e04444', {f: F.bold, w: 800}); T('सच', 120, 400, 56, CR.bone, {f: F.bold, w: 800});
    [[nf, '#c23434', 300], [nt, '#d9d9d9', 400]].forEach(([n, c, y]) => { ctx.fillStyle = 'rgba(255,255,255,.08)'; ctx.fillRect(260, y - 40, 680, 34); ctx.fillStyle = c; ctx.fillRect(260, y - 40, 680 * n / N, 34); });
    const k6 = P(t, b[1] + .1, .4);
    pop(540, 1180, k6, () => { T('6×', 0, 0, 220, CR.red, {a: 'center', f: F.bold, w: 800, glow: CR.red, gb: 40}); T('तेज़ फैलती है झूठी ख़बर', 0, 70, 46, CR.bone, {a: 'center', w: 600}); });
    T('स्रोत: Vosoughi, Roy & Aral · Science 2018 (MIT)', 540, 1330, 24, 'rgba(200,205,215,.5)', {a: 'center', w: 500});
    vign(.8);
  }},
/* 5 MID HOOK */
{ file: 0, tin: 'glitch', sfx: [[0, 'glitch'], [.1, 'heartbeat'], [BT(5)[1] - .1, 'heartbeat'], [BT(5)[1], 'impact_small']],
  draw(t) {
    const b = BT(5); ctx.fillStyle = '#040404'; ctx.fillRect(0, 0, W, H);
    for (let y = 0; y < H; y += 6) { ctx.fillStyle = 'rgba(255,255,255,.02)'; ctx.fillRect(0, y, W, 2); }
    const fr = Math.floor(NOW * 30);
    for (let i = 0; i < 6; i++) if (hash(fr + i * 13) > .65) { ctx.fillStyle = `rgba(179,38,42,${.05 + hash(fr * i) * .1})`; ctx.fillRect(0, hash(fr + i) * H, W, 6 + hash(i * fr) * 50); }
    const beat = Math.max(Math.exp(-(((t - .1) * 8) ** 2)), Math.exp(-(((t - b[1]) * 8) ** 2)));
    const v = ctx.createRadialGradient(W / 2, H / 2, 200, W / 2, H / 2, 1100); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, `rgba(150,25,28,${.18 + beat * .3})`); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
    const rgb = (s, y, size, col, k) => { if (k <= 0) return; const j = (hash(fr * 3.1) - .5) * 22 * (1 - k * .7), sc = 1 + beat * .05;
      ctx.save(); ctx.translate(W / 2, y); ctx.scale(sc, sc); ctx.globalCompositeOperation = 'lighter';
      T(s, -7 + j, 0, size, 'rgba(255,0,40,.8)', {a: 'center', f: F.bold, w: 800}); T(s, 7 - j, 0, size, 'rgba(0,200,255,.6)', {a: 'center', f: F.bold, w: 800});
      ctx.globalCompositeOperation = 'source-over'; T(s, 0, 0, size, col, {a: 'center', f: F.bold, w: 800}); ctx.restore(); };
    rgb('लेकिन…', 720, 140, CR.bone, P(t, .05, .1));
    rgb('असली खेल', 940, 170, CR.red, P(t, .6, .1));
    rgb('इससे भी गहरा है', 1140, 110, CR.bone, P(t, b[1], .1));
  }},
/* 6 evidence board — 2018 rumours */
{ file: 6, tin: 'zoomin', sfx: [[.1, 'paper'], [.3, 'pin'], [.6, 'pin'], [.9, 'string'], [1.2, 'typewriter', 1], [BT(6)[1] + .2, 'stamp'], [BT(6)[1], 'braam']],
  draw(t, d) {
    const b = BT(6); ctx.save(); cam(t, d, 1.08, 1); cover(IMG.cork); ctx.fillStyle = 'rgba(5,5,7,.62)'; ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = 'rgba(230,225,215,.5)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(80, 300); ctx.lineTo(1000, 300); ctx.stroke();
    [['2017', 230], ['2018', 540], ['2019', 850]].forEach(([y, x], i) => { const on = i === 1; ctx.fillStyle = on ? CR.red : 'rgba(230,225,215,.6)'; ctx.beginPath(); ctx.arc(x, 300, on ? 14 : 8, 0, 7); ctx.fill();
      T(y, x, 270, on ? 44 : 30, on ? '#f0b4ae' : 'rgba(230,225,215,.6)', {a: 'center', f: F.mono, w: 700}); });
    polaroid(290, 700, 420, 470, -.06, IMG.village, 'गाँव की गली · प्रतीकात्मक', P(t, .2, .2)); pin(290, 478);
    clipping(780, 660, 440, 420, .06, 61, P(t, .5, .2), (x, y, w) => {
      T('समाचार · 2018', x + 26, y + 56, 30, C.red, {w: 700}); ctx.fillStyle = C.ink; ctx.fillRect(x + 26, y + 72, w - 52, 3);
      T('अफ़वाह फैली,', x + 26, y + 150, 58, C.ink, {f: F.head, w: 400}); T('भीड़ बेक़ाबू', x + 26, y + 220, 58, C.ink, {f: F.head, w: 400});
      textBars(x + 26, y + 250, w - 52, 140, 7, 2); });
    pin(780, 458);
    const bub = [[150, 1110], [400, 1180], [650, 1110], [900, 1180]];
    bub.forEach(([x, y], i) => { const k = P(t, 1 + i * .25, .3); if (i) rope(bub[i - 1][0], bub[i - 1][1], x, y, P(t, .9 + i * .25, .4));
      pop(x, y, k, () => { rr(-100, -50, 200, 100, 18); ctx.fillStyle = '#e9e4da'; ctx.fill(); ctx.fillStyle = '#7d1d1f'; ctx.font = `700 22px ${F.mono}`; ctx.textAlign = 'center'; ctx.fillText('↪ FWD', 0, -10);
        ctx.fillStyle = '#5a5550'; ctx.fillRect(-70, 8, 140, 8); ctx.fillRect(-70, 24, 90, 8); }); });
    rope(540, 300, 290, 478, P(t, .7, .5)); rope(540, 300, 780, 458, P(t, .8, .5));
    stamp('बेगुनाहों की जान गई', 560, 960, -.1, P(t, b[1] + .2, .25), C.red, 66);
    ctx.restore(); vign(.7);
  }},
/* 7 forward limit */
{ file: 7, tin: 'whip', sfx: [[.1, 'notif'], [.6, 'notif'], [1.1, 'notif'], [1.9, 'stamp'], [2.2, 'impact_small']],
  draw(t, d) {
    bgChar('#09090c', '#131318', '#050506'); glowAt(540, 900, 700, '150,175,200', .12);
    ctx.save(); cam(t, d, 1, 1.05);
    phoneBody(540, 900, 560, 1040, 0, (x, y, w, h) => {
      ctx.fillStyle = '#1b1c22'; ctx.fillRect(x, y, w, 110); ctx.fillStyle = '#3a3c46'; ctx.beginPath(); ctx.arc(x + 60, y + 58, 28, 0, 7); ctx.fill();
      T('परिवार ग्रुप', x + 110, y + 70, 34, CR.bone, {w: 600});
      for (let i = 0; i < 4; i++) { const k = P(t, .1 + i * .5, .3); if (k <= 0) continue; const by = y + 150 + i * 190;
        ctx.save(); ctx.globalAlpha = eo(k); rr(x + 30, by, w - 130, 160, 18); ctx.fillStyle = '#25262e'; ctx.fill();
        T('↪↪ कई बार फ़ॉरवर्ड किया गया', x + 54, by + 40, 22, '#d58a84', {w: 600});
        T(['ज़रूर शेयर करें!!', 'ये सच है, सबको भेजो', 'सावधान रहें!!!', 'अभी फ़ॉरवर्ड करें'][i], x + 54, by + 92, 32, CR.bone, {w: 600});
        ctx.fillStyle = '#4a4c57'; ctx.fillRect(x + 54, by + 112, 200, 10); ctx.restore(); }
    });
    ctx.restore();
    stamp('सीमा: 5 चैट', 540, 1180, -.08, P(t, 1.9, .25), CR.red, 84);
    T('भारत · जुलाई 2018', 540, 320, 44, CR.steel, {a: 'center', f: F.mono, w: 700, al: P(t, .2, .4)});
    vign(.75);
  }},
/* 8 WEF risk ranking */
{ file: 8, tin: 'flash', sfx: [[.1, 'paper'], [.6, 'typewriter', .9], [1.6, 'blips'], [2.4, 'impact'], [2.6, 'braam']],
  draw(t, d) {
    bgChar('#09090c', '#141419', '#050506');
    ctx.save(); cam(t, d, 1, 1.07, 0, -30);
    clipping(540, 470, 900, 300, -.02, 71, P(t, .05, .3), (x, y, w) => {
      T('World Economic Forum', x + 40, y + 64, 30, '#5a4f44', {w: 600});
      T(typed('GLOBAL RISKS REPORT 2024', P(t, .5, .9)), x + 40, y + 140, 54, C.ink, {f: F.head, w: 400});
      T('ग़लत सूचना / दुष्प्रचार का ख़तरा', x + 40, y + 210, 36, C.red, {w: 700});
      textBars(x + 40, y + 236, w - 80, 40, 11, 3); }, '#dcd5c7');
    const hs = [520, 360, 330, 300, 280, 250, 230], base = 1240;
    hs.forEach((h, i) => { const k = eo(P(t, 1.4 + i * .1, .7)), x = 120 + i * 120, top = i === 0;
      isoBar(x, base, 84, 40, h * k, top ? '#a52427' : '#2b2c33', top ? '#d24a46' : '#3a3c45', top ? '#6e1517' : '#1c1d22');
      T(top ? '#1' : '#' + (i + 1), x + 42, base - h * k - 46, top ? 44 : 30, top ? '#f0b4ae' : 'rgba(200,205,215,.6)', {a: 'center', f: F.mono, w: 700, al: k}); });
    T('भारत', 162, base + 50, 40, '#f0b4ae', {a: 'center', f: F.bold, w: 800, al: P(t, 2.3, .4)});
    T('अन्य देश →', 640, base + 50, 30, 'rgba(200,205,215,.6)', {a: 'center', w: 500, al: P(t, 2.3, .4)});
    ctx.restore();
    T('स्रोत: WEF Global Risks Report 2024', 540, 1340, 24, 'rgba(200,205,215,.5)', {a: 'center', w: 500});
    vign(.75);
  }},
/* 9 rally · TV · phones → emotions */
{ file: 9, tin: 'zoomin', sfx: [[.05, 'crowd', 1.6], [.1, 'impact_small'], [BT(9)[0] + 1.2, 'static'], [BT(9)[0] + 1.3, 'impact_small'], [BT(9)[0] + 2.4, 'notif'], [BT(9)[0] + 2.5, 'impact_small'], [BT(9)[1], 'braam'], [BT(9)[2], 'heartbeat'], [BT(9)[2] + .7, 'heartbeat']],
  draw(t, d) {
    const b = BT(9), dur0 = Math.max(2.4, b[1] - b[0]); bgChar('#07070a', '#111115', '#040405');
    const panels = [[310, 'रैली'], [650, 'टीवी डिबेट'], [990, 'फ़ोन']], aim = P(t, b[1], .5), emo = P(t, b[2], .6);
    panels.forEach(([y, lab], i) => { const k = P(t, b[0] + i * dur0 / 3, .35); if (k <= 0) return;
      ctx.save(); ctx.globalAlpha = eo(k) * (1 - emo * .55); ctx.translate((1 - eo(k)) * (i % 2 ? 300 : -300), 0);
      ctx.beginPath(); rr(60, y - 150, 960, 300, 14); ctx.save(); ctx.clip();
      if (i === 0) { ctx.fillStyle = '#0d0d10'; ctx.fillRect(60, y - 150, 960, 300); for (let s = 0; s < 3; s++) { ctx.fillStyle = `rgba(230,220,200,${.06 + .04 * Math.sin(NOW * 2 + s)})`; ctx.beginPath(); ctx.moveTo(200 + s * 340, y - 150); ctx.lineTo(120 + s * 340, y + 150); ctx.lineTo(320 + s * 340, y + 150); ctx.closePath(); ctx.fill(); }
        ctx.fillStyle = '#2a0c0d'; ctx.fillRect(360, y - 110, 360, 70); T('जनसभा', 540, y - 62, 40, 'rgba(240,200,190,.8)', {a: 'center', f: F.bold, w: 800});
        ctx.drawImage(IMG.rally, 60, y - 80 + Math.sin(NOW * 6) * 3, 960, 373); }
      if (i === 1) { ctx.fillStyle = '#121218'; ctx.fillRect(60, y - 150, 960, 300); const sh = Math.sin(NOW * 9);
        for (let q = 0; q < 4; q++) { const qx = 90 + q * 232; ctx.fillStyle = '#1e1f27'; ctx.fillRect(qx, y - 130, 216, 180); person(qx + 108, y + 40, 46, '#060607', 1);
          if (q % 2 === (Math.floor(NOW * 3) % 2)) { ctx.fillStyle = CR.red; ctx.beginPath(); ctx.ellipse(qx + 108, y - 34, 9, 6 + Math.abs(sh) * 5, 0, 0, 7); ctx.fill(); } }
        ctx.fillStyle = CR.red; ctx.fillRect(60, y + 70, 960, 50); T('ब्रेकिंग · महाबहस', 90, y + 106, 30, '#fff', {f: F.bold, w: 800});
        ctx.fillStyle = 'rgba(255,255,255,.85)'; ctx.fillRect(420, y + 84, 580, 10); }
      if (i === 2) { ctx.fillStyle = '#0b0b0e'; ctx.fillRect(60, y - 150, 960, 300);
        for (let p = 0; p < 7; p++) { const px = 120 + p * 140; person(px, y + 120, 48, '#050506', 1); glowAt(px + 10, y + 20, 70, '160,185,210', .35); ctx.fillStyle = '#b9cad8'; ctx.fillRect(px - 6, y + 10, 22, 34); } }
      ctx.restore(); ctx.strokeStyle = 'rgba(200,60,60,.6)'; ctx.lineWidth = 3; rr(60, y - 150, 960, 300, 14); ctx.stroke();
      T(lab, 90, y - 110, 30, CR.bone, {f: F.mono, w: 700}); ctx.restore();
      if (aim > 0) { ctx.strokeStyle = `rgba(210,50,50,${.8 * aim})`; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(540, y + (i === 2 ? -150 : 150)); ctx.lineTo(540, lerp(y, 1180, eo(aim))); ctx.stroke(); } });
    if (aim > 0) { ctx.save(); ctx.translate(540, 1200); ctx.rotate(NOW * .6); ctx.strokeStyle = `rgba(230,60,60,${aim})`; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(0, 0, 90, 0, 7); ctx.moveTo(-130, 0); ctx.lineTo(-50, 0); ctx.moveTo(130, 0); ctx.lineTo(50, 0); ctx.moveTo(0, -130); ctx.lineTo(0, -50); ctx.moveTo(0, 130); ctx.lineTo(0, 50); ctx.stroke(); ctx.restore(); }
    if (emo > 0) { const pulse = 1 + Math.sin(NOW * 7) * .06; ctx.save(); ctx.translate(540, 1200); ctx.scale(eo(emo) * pulse, eo(emo) * pulse); glowAt(0, 0, 220, '210,40,40', .6);
      ctx.fillStyle = '#c42c2e'; ctx.beginPath(); ctx.moveTo(0, 60); ctx.bezierCurveTo(-120, -10, -70, -110, 0, -50); ctx.bezierCurveTo(70, -110, 120, -10, 0, 60); ctx.fill(); ctx.restore();
      T('भावनाएँ', 540, 1335, 54, CR.bone, {a: 'center', f: F.bold, w: 800, al: emo}); }
    vign(.75);
  }},
/* 10 voting booth + strings */
{ file: 10, tin: 'whip', sfx: [[.1, 'impact_small'], [.4, 'string'], [BT(10)[1], 'braam'], [BT(10)[1] + .1, 'string'], [BT(10)[1] + .4, 'beep']],
  draw(t, d) {
    const b = BT(10), pull = eo(P(t, b[1], .6)); bgChar('#08080a', '#121216', '#040405'); glowAt(540, 700, 600, '220,210,190', .1);
    ctx.save(); cam(t, d, 1, 1.08, 0, -20);
    ctx.fillStyle = '#1d1d22'; ctx.beginPath(); ctx.moveTo(140, 560); ctx.lineTo(940, 560); ctx.lineTo(1000, 1360); ctx.lineTo(80, 1360); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#26272d'; ctx.fillRect(180, 600, 720, 120); T('मतदान कक्ष', 540, 680, 50, 'rgba(230,225,215,.75)', {a: 'center', f: F.bold, w: 800});
    rr(300, 760, 480, 520, 16); ctx.fillStyle = '#b9b6ad'; ctx.fill(); ctx.strokeStyle = '#4a4a4a'; ctx.lineWidth = 4; ctx.stroke();
    for (let i = 0; i < 6; i++) { const y = 810 + i * 74; ctx.fillStyle = '#e9e6dd'; ctx.fillRect(330, y, 300, 56); ctx.fillStyle = '#6a6a6a'; ctx.font = `700 30px ${F.mono}`; ctx.textAlign = 'left'; ctx.fillText(String(i + 1), 346, y + 40);
      ctx.fillStyle = '#d3cfc4'; ctx.fillRect(390, y + 14, 200, 28); ctx.fillStyle = i === 2 && pull > .5 ? '#d24040' : '#3c4a8a'; ctx.beginPath(); ctx.ellipse(700, y + 28, 36, 22, 0, 0, 7); ctx.fill(); }
    const hx = lerp(820, 740, eo(P(t, .3, 1.2))) + Math.sin(NOW * 9) * 4 * pull, hy = lerp(1120, 960, eo(P(t, .3, 1.2))) - pull * 30;
    ctx.save(); ctx.translate(hx, hy); ctx.rotate(-.5);
    ctx.fillStyle = '#7a5038'; rr(-40, -10, 120, 70, 26); ctx.fill(); rr(-62, 0, 70, 30, 15); ctx.fill(); ctx.fillStyle = '#6e4632'; rr(60, 0, 260, 80, 30); ctx.fill();
    ctx.fillStyle = '#2a2050'; ctx.fillRect(-56, 6, 14, 18); ctx.restore();
    ctx.strokeStyle = `rgba(220,60,60,${.3 + .6 * pull})`; ctx.lineWidth = 2.5;
    [[hx - 50, hy - 30], [hx + 40, hy - 50], [hx + 160, hy - 20]].forEach(([x, y], i) => { ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + (i - 1) * 60, 0); ctx.stroke(); });
    ctx.fillStyle = '#020203'; ctx.globalAlpha = .2 + .8 * pull; smooth([[560, 40], [700, 10], [820, 90], [900, 40], [960, 150], [880, 220], [640, 200]]); ctx.fill(); ctx.globalAlpha = 1;
    ctx.restore();
    T('किसके हाथ में धागे?', 540, 380, 60, CR.bone, {a: 'center', f: F.head, w: 400, al: P(t, b[1], .5)});
    vign(.8);
  }},
/* 11 END — the forward button */
{ file: 0, tin: 'zoomin', sfx: [[0, 'impact_big'], [.4, 'vibrate'], [BT(11)[1], 'impact_small'], [BT(11)[1] + .2, 'heartbeat'], [BT(11)[1] + 1.0, 'heartbeat']],
  draw(t, d) {
    const b = BT(11); bgChar('#060607', '#101014', '#030304'); glowAt(540, 1050, 700, '150,175,200', .14);
    ctx.save(); cam(t, d, 1, 1.06, 0, 30);
    phoneBody(540, 1080, 520, 900, 0, (x, y, w, h) => {
      rr(x + 30, y + 80, w - 120, 210, 18); ctx.fillStyle = '#25262e'; ctx.fill();
      T('↪↪ कई बार फ़ॉरवर्ड किया गया', x + 54, y + 122, 22, '#d58a84', {w: 600}); T('ये ख़बर ज़रूर', x + 54, y + 180, 38, CR.bone, {w: 700}); T('सबको भेजें!!!', x + 54, y + 230, 38, CR.bone, {w: 700});
      const pulse = 1 + Math.sin(NOW * 6) * .05; ctx.save(); ctx.translate(x + w / 2, y + 470); ctx.scale(pulse, pulse); rr(-170, -55, 340, 110, 55); ctx.fillStyle = CR.red; ctx.fill(); T('फ़ॉरवर्ड  ↪', 0, 16, 46, '#fff', {a: 'center', f: F.bold, w: 800}); ctx.restore();
      const fy = y + 640 - Math.sin(NOW * 2) * 14; ctx.fillStyle = '#7a5038'; rr(x + w / 2 - 28, fy, 56, 300, 28); ctx.fill(); ctx.fillStyle = '#8a5d44'; rr(x + w / 2 - 22, fy + 6, 44, 40, 18); ctx.fill();
    });
    ctx.restore();
    pop(540, 330, P(t, .1, .3), () => { T('आख़िरी बार', 0, -60, 60, CR.steel, {a: 'center', f: F.bold, w: 800}); T('फ़ॉरवर्ड करने से पहले', 0, 30, 76, CR.bone, {a: 'center', f: F.bold, w: 800}); T('कब चेक किया?', 0, 125, 96, '#ef5a52', {a: 'center', f: F.bold, w: 800, glow: CR.red, gb: 24}); });
    pop(540, 1650, P(t, b[1], .3), () => { rr(-320, -56, 640, 112, 56); ctx.fillStyle = CR.red; ctx.fill(); T('कमेंट में बताइए ↓', 0, 20, 58, '#fff', {a: 'center', f: F.bold, w: 800}); });
    vign(.8);
  }}
];
let NET = null;
function buildNet() {
  const r = rng(13), nodes = [];
  while (nodes.length < 150) { const p = [90 + r() * 900, 480 + r() * 600]; if (nodes.every(q => Math.hypot(q[0] - p[0], q[1] - p[1]) > 48)) nodes.push(p); }
  const edges = [], adj = nodes.map(() => []);
  nodes.forEach((p, i) => { nodes.map((q, j) => [j, Math.hypot(q[0] - p[0], q[1] - p[1])]).filter(e => e[0] !== i).sort((a, b) => a[1] - b[1]).slice(0, 3).forEach(([j]) => { if (!adj[i].includes(j)) { adj[i].push(j); adj[j].push(i); edges.push([i, j]); } }); });
  let s = 0, best = 1e9; nodes.forEach((p, i) => { const dd = Math.hypot(p[0] - 540, p[1] - 780); if (dd < best) { best = dd; s = i; } });
  const hop = nodes.map(() => 1e9); hop[s] = 0; const qu = [s]; while (qu.length) { const i = qu.shift(); for (const j of adj[i]) if (hop[j] > hop[i] + 1) { hop[j] = hop[i] + 1; qu.push(j); } }
  NET = {nodes, edges, hop};
}
