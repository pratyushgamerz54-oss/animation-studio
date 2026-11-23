/* ---------- Naya Bharat: cinematic gold palette ---------- */
const GD = {gold: '#f2c14e', amber: '#e39a2b', saffron: '#ff9933', green: '#2fa35a', white: '#f4efe4', navy: '#101a2e', steel: '#9aa3b2'};
const glowG = (x, y, r, a = .5) => glowAt(x, y, r, '242,170,60', a);
function sunrise(t, y = 1150, a = 1) {
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#07080c'); g.addColorStop(.45, '#151722'); g.addColorStop(.62, '#3a2414'); g.addColorStop(1, '#0a0806');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); glowG(540, y, 900, .45 * a); glowAt(540, y, 300, '255,214,140', .5 * a);
}
function flag(x, y, s, t) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = '#cfc8b8'; ctx.fillRect(-3, 0, 6, 220);
  const band = (c, k) => { ctx.fillStyle = c; ctx.beginPath(); for (let i = 0; i <= 20; i++) { const u = i / 20, wv = Math.sin(u * 5 - NOW * 5) * 8 * u; const px = 3 + u * 150, py = k * 32 + wv; i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); }
    for (let i = 20; i >= 0; i--) { const u = i / 20, wv = Math.sin(u * 5 - NOW * 5) * 8 * u; ctx.lineTo(3 + u * 150, (k + 1) * 32 + wv); } ctx.closePath(); ctx.fill(); };
  band(GD.saffron, 0); band('#f6f3ea', 1); band('#138808', 2);
  const wv = Math.sin(.5 * 5 - NOW * 5) * 4; ctx.strokeStyle = '#0b3d91'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(78, 48 + wv, 12, 0, 7); ctx.stroke();
  ctx.restore();
}
function counterHead(top, big, sub, y, k, col = GD.gold) {
  pop(540, y, k, () => {
    if (top) T(top, 0, -150, 44, GD.steel, {a: 'center', w: 600});
    const s = fitSize(big, 150, 980, 800, F.bold);
    T(big, 0, 0, s, col, {a: 'center', f: F.bold, w: 800, glow: 'rgba(242,170,60,.7)', gb: 30});
    if (sub) T(sub, 0, 64, 40, GD.white, {a: 'center', w: 500});
  });
}
const src = (s, y = 1300) => T('स्रोत: ' + s, 540, y, 24, 'rgba(225,215,195,.55)', {a: 'center', w: 500});
const AIRPORTS = [[77.1, 28.56], [72.87, 19.09], [80.17, 12.99], [77.71, 13.2], [78.43, 17.24], [88.45, 22.65], [73.92, 18.58], [72.63, 23.07], [75.81, 26.82], [80.89, 26.76], [85.09, 25.59], [91.59, 26.11],
  [76.27, 10.15], [73.83, 15.38], [77.93, 30.19], [74.87, 31.71], [83.82, 25.45], [81.73, 21.18], [79.05, 21.09], [85.82, 20.24], [92.8, 23.84], [94.11, 27.3], [76.4, 9.94], [79.92, 23.18], [74.6, 24.6], [86.2, 23.3], [93.9, 24.76], [75.4, 19.86]];
const ROADS = [[[77.2, 28.6], [75.8, 26.9], [72.6, 23.0], [72.9, 19.1]], [[72.9, 19.1], [73.9, 18.5], [77.6, 13.0], [80.3, 13.1]], [[80.3, 13.1], [85.8, 20.3], [88.4, 22.6]], [[88.4, 22.6], [85.1, 25.6], [80.9, 26.8], [77.2, 28.6]],
  [[77.2, 28.6], [78.5, 23.3], [79.1, 21.1], [78.5, 17.4], [77.6, 13.0], [76.3, 10.0], [77.5, 8.2]], [[77.2, 28.6], [76.8, 30.7], [74.9, 31.6], [74.8, 34.1]], [[88.4, 22.6], [88.4, 26.7], [91.7, 26.1], [94.1, 27.3]],
  [[72.6, 23.0], [75.8, 22.7], [79.1, 21.1], [81.6, 21.2], [85.8, 20.3]], [[73.9, 18.5], [75.3, 19.9], [78.5, 17.4], [80.6, 16.5], [83.3, 17.7]]];
function vial(x, y, s, fill) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  rr(-16, -60, 32, 70, 6); ctx.fillStyle = 'rgba(220,230,240,.22)'; ctx.fill(); ctx.strokeStyle = 'rgba(230,235,245,.6)'; ctx.lineWidth = 2; ctx.stroke();
  ctx.fillStyle = `rgba(242,180,80,${.4 + .5 * fill})`; ctx.fillRect(-13, 8 - 50 * fill, 26, 50 * fill); ctx.fillStyle = '#c9cdd3'; ctx.fillRect(-18, -72, 36, 14); ctx.fillStyle = GD.amber; ctx.fillRect(-14, -80, 28, 9); ctx.restore(); }

/* ---------- scenes ---------- */
const S = [
/* 0 HOOK — 10th to top 5 */
{ file: 1, tin: null, sfx: [[0, 'impact_big'], [.2, 'rise', 1.5], [BT(0)[2], 'braam'], [BT(0)[2] + .1, 'impact'], [BT(0)[4], 'whoosh']],
  draw(t, d) {
    const b = BT(0), climb = io(P(t, b[2] - .2, 1.4)), zt = P(t, b[4], d - b[4]);
    sunrise(t, 1050, .6 + .4 * climb);
    ctx.save(); const z = lerp(1, 1.9, io(zt)); ctx.translate(540, 820); ctx.scale(z, z); ctx.translate(-540, -820); cam(t, d, 1, 1.04);
    for (let r = 10; r >= 1; r--) { const i = 10 - r, x = 110 + i * 86, y = 1230 - i * 62;
      isoBar(x, y + 80, 80, 36, 80 + i * 62, r <= 5 ? '#3b2a14' : '#22232a', r <= 5 ? '#6a4a1c' : '#34353e', r <= 5 ? '#2a1c0c' : '#18191e');
      T('#' + r, x + 40, y + 60, 30, r === 5 ? GD.gold : 'rgba(220,215,200,.55)', {a: 'center', f: F.mono, w: 700}); }
    const step = lerp(10, 5, climb), i = 10 - step, ox = 110 + i * 86 + 58, oy = 1230 - i * 62 - (80 + i * 62) + 70 - Math.abs(Math.sin(climb * Math.PI * 5)) * 30;
    glowG(ox, oy - 20, 160, .8); flag(ox - 4, oy - 230, .7, t);
    ctx.fillStyle = '#ffe6b0'; ctx.beginPath(); ctx.arc(ox, oy - 10, 18, 0, 7); ctx.fill();
    ctx.restore();
    T(climb < .5 ? '2014 · दुनिया में 10वाँ' : 'आज · टॉप 5', 540, 330, 76, climb < .5 ? GD.steel : GD.gold, {a: 'center', f: F.bold, w: 800, glow: climb < .5 ? null : 'rgba(242,170,60,.7)', gb: 24, al: P(t, .2, .4) * (1 - zt)});
    T('अर्थव्यवस्था का आकार (नॉमिनल GDP)', 540, 395, 34, 'rgba(225,215,195,.7)', {a: 'center', w: 500, al: 1 - zt});
    src('IMF World Economic Outlook', 1310); vign(.75);
  }},
/* 1 leadership — parliament + timeline */
{ file: 2, tin: 'zoomin', sfx: [[.1, 'braam'], [.4, 'drumroll', 1.6], [BT(1)[2], 'whoosh'], [BT(1)[2] + .2, 'impact']],
  draw(t, d) {
    const b = BT(1); sunrise(t, 1000, .8);
    ctx.save(); cam(t, d, 1, 1.08, 0, 30);
    ctx.save(); ctx.translate(0, 0); parliament(540, 1150, 1.0, eo(P(t, .05, 1)) ); ctx.restore();
    flag(540, 640 - eo(P(t, .3, 1)) * 40, 1, t);
    ctx.restore();
    const k = io(P(t, b[2] - .3, d - b[2]));
    const x0 = 100, x1 = 980, y = 450;
    ctx.strokeStyle = 'rgba(240,230,210,.25)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(x1, y); ctx.stroke();
    ctx.save(); ctx.shadowColor = GD.gold; ctx.shadowBlur = 20; ctx.strokeStyle = GD.gold; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(lerp(x0, x1, Math.max(.05, k)), y); ctx.stroke(); ctx.restore();
    [2014, 2017, 2020, 2023, 2026].forEach((yr, i) => { const x = lerp(x0, x1, i / 4), on = k >= i / 4 - .001 || i === 0;
      ctx.fillStyle = on ? GD.gold : 'rgba(240,230,210,.4)'; ctx.beginPath(); ctx.arc(x, y, on ? 10 : 6, 0, 7); ctx.fill(); T(String(yr), x, y - 26, 30, on ? GD.white : 'rgba(240,230,210,.4)', {a: 'center', f: F.mono, w: 700}); });
    T('नेतृत्व · नई रफ़्तार', 540, 330, 64, GD.white, {a: 'center', f: F.head, w: 400, al: P(t, .3, .5)});
    vign(.75);
  }},
/* 2 Jan Dhan */
{ file: 3, tin: 'zoomin', sfx: [[.1, 'impact_small'], [.3, 'coins', 1.6], [.4, 'ticks', 1.6], [BT(2)[1], 'rise', 1]],
  draw(t, d) {
    const b = BT(2); sunrise(t, 1100, .5);
    ctx.save(); cam(t, d, 1, 1.06);
    drawMap({cx: 540, cy: 860, scale: 27, tilt: .9, yaw: lerp(-.2, .1, io(t / d)), top: ['#2a2416', '#15120b'], side: [[12, 10, 6], [70, 52, 26]], edge: GD.gold, grid: 'rgba(242,193,78,.08)',
      dots: {k: eo(P(t, .2, Math.max(1, b[1]))), color: 'rgba(255,214,120,.95)'}});
    ctx.restore();
    pop(820, 1150, P(t, .3, .4), () => { ctx.rotate(-.08); rr(-120, -80, 240, 160, 10); ctx.fillStyle = '#1b3a7a'; ctx.fill(); ctx.strokeStyle = GD.gold; ctx.lineWidth = 3; ctx.stroke();
      T('बैंक पासबुक', 0, -20, 30, GD.gold, {a: 'center', f: F.bold, w: 800}); ctx.fillStyle = 'rgba(242,193,78,.5)'; ctx.fillRect(-80, 10, 160, 8); ctx.fillRect(-80, 30, 110, 8); });
    counterHead('जन धन योजना', num(Math.round(55 * eo(P(t, .2, 1.6)))) + ' करोड़+', 'बैंक खाते', 380, P(t, .1, .3));
    if (t > b[1]) { for (let i = 0; i < 12; i++) { const k = P(t, b[1] + i * .06, .3); person(130 + i * 75, 1250, 18, `rgba(255,214,140,${.25 + .7 * k})`, 1); } }
    src('वित्त मंत्रालय, PMJDY (2025)', 1310); vign(.75);
  }},
/* 3 toilets + LPG */
{ file: 4, tin: 'whip', sfx: [[.1, 'impact_small'], [.3, 'ticks', 1.2], [BT(3)[1] - .1, 'stamp'], [BT(3)[2], 'whoosh'], [BT(3)[2] + .4, 'flame'], [BT(3)[3], 'ticks', 1]],
  draw(t, d) {
    const b = BT(3), gas = P(t, b[2], .6); sunrise(t, 900, .7);
    ctx.save(); cam(t, d, 1, 1.05, 0, -10);
    ctx.fillStyle = '#17120c'; ctx.fillRect(0, 1060, W, 400);
    ctx.fillStyle = '#2b2118'; ctx.fillRect(130, 760, 420, 300); ctx.fillStyle = '#4a2f1a'; ctx.beginPath(); ctx.moveTo(100, 770); ctx.lineTo(340, 620); ctx.lineTo(580, 770); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#0d0a07'; ctx.fillRect(300, 900, 90, 160); ctx.fillStyle = 'rgba(255,200,120,.5)'; ctx.fillRect(180, 830, 70, 60);
    const toilet = P(t, b[1] - .1, .5);
    pop(780, 960, toilet, () => { ctx.fillStyle = '#d9dde3'; ctx.fillRect(-90, -120, 180, 220); ctx.fillStyle = '#2f6fb0'; ctx.fillRect(-100, -140, 200, 26); ctx.fillStyle = '#5b7fa8'; ctx.fillRect(-40, -40, 80, 140);
      T('शौचालय', 0, -150, 30, GD.white, {a: 'center', f: F.bold, w: 800}); });
    const sx = 400, sy = 1240;
    ctx.fillStyle = '#2e2e33'; rr(sx - 150, sy - 40, 300, 60, 10); ctx.fill(); ctx.fillStyle = '#c43f2f'; rr(sx + 170, sy - 160, 90, 180, 30); ctx.fill(); T('LPG', sx + 215, sy - 60, 26, '#fff', {a: 'center', f: F.bold, w: 800});
    if (gas < 1) for (let i = 0; i < 6; i++) { const ph = (NOW * .4 + i / 6) % 1; ctx.fillStyle = `rgba(120,110,100,${.25 * (1 - ph) * (1 - gas)})`; ctx.beginPath(); ctx.arc(sx - 40 + Math.sin(i + NOW) * 20, sy - 60 - ph * 300, 30 + ph * 50, 0, 7); ctx.fill(); }
    if (gas > 0) { for (let i = 0; i < 9; i++) { const x = sx - 80 + i * 20, h = 26 + Math.sin(NOW * 20 + i) * 6; const g = ctx.createLinearGradient(x, sy - 40, x, sy - 40 - h); g.addColorStop(0, `rgba(70,140,255,${gas})`); g.addColorStop(1, 'rgba(160,210,255,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, sy - 40 - h / 2, 8, h / 2, 0, 0, 7); ctx.fill(); } }
    ctx.restore();
    const s1 = P(t, .1, .3) * (1 - P(t, b[2] - .1, .15)), s2 = P(t, b[2], .3);
    counterHead('स्वच्छ भारत मिशन', num(Math.round(11 * eo(P(t, .2, 1.2)))) + ' करोड़+', 'शौचालय', 380, s1);
    counterHead('उज्ज्वला योजना', num(Math.round(10 * eo(P(t, b[2], 1)))) + ' करोड़+', 'घरों तक गैस', 380, s2, '#8fc0ff');
    src('जल शक्ति मंत्रालय · पेट्रोलियम मंत्रालय', 1310); vign(.75);
  }},
/* 4 highways + airports */
{ file: 5, tin: 'zoomin', sfx: [[.1, 'braam'], [.3, 'whoosh'], [BT(4)[1], 'ticks', 1.2], [BT(4)[3], 'jet', 2], [BT(4)[3] + .2, 'blips']],
  draw(t, d) {
    const b = BT(4), road = io(P(t, .2, Math.max(1.5, b[3] - .2))), air = P(t, b[3], 1.4);
    bgChar('#07080b', '#12141a', '#050506'); glowG(540, 900, 800, .14);
    ctx.save(); cam(t, d, 1, 1.07);
    const pr = drawMap({cx: 540, cy: 880, scale: 28, tilt: .92, yaw: lerp(-.18, .12, io(t / d)), top: ['#1c1d24', '#101116'], side: [[8, 8, 10], [44, 36, 22]], edge: 'rgba(242,193,78,.7)', grid: 'rgba(242,193,78,.06)',
      pins: AIRPORTS.map((c, i) => ({lon: c[0], lat: c[1], h: 1.6, color: '#7fc4ff', k: P(air, i / AIRPORTS.length * .8, .2)}))});
    ctx.save(); ctx.shadowColor = GD.gold; ctx.shadowBlur = 14; ctx.strokeStyle = GD.gold; ctx.lineWidth = 4; ctx.lineCap = 'round';
    ROADS.forEach((rd, ri) => { const k = clamp(road * ROADS.length - ri * .6, 0, 1); if (k <= 0) return; const segs = rd.length - 1, upto = k * segs;
      ctx.beginPath(); for (let s = 0; s <= Math.floor(upto); s++) { const [x, y] = pr(rd[s][0], rd[s][1], .05); s ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
      const f2 = upto - Math.floor(upto), s0 = Math.floor(upto); if (s0 < segs) { const a = rd[s0], c = rd[s0 + 1], [x, y] = pr(lerp(a[0], c[0], f2), lerp(a[1], c[1], f2), .05); ctx.lineTo(x, y); } ctx.stroke(); });
    ctx.restore();
    if (air > 0) { const ph = (NOW * .35) % 1, a = pr(77.1, 28.56, 1.5), c = pr(80.17, 12.99, 1.5), mx = (a[0] + c[0]) / 2 + 160, my = (a[1] + c[1]) / 2 - 120;
      const px = (1 - ph) ** 2 * a[0] + 2 * (1 - ph) * ph * mx + ph * ph * c[0], py = (1 - ph) ** 2 * a[1] + 2 * (1 - ph) * ph * my + ph * ph * c[1];
      ctx.strokeStyle = 'rgba(160,210,255,.35)'; ctx.setLineDash([8, 10]); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.quadraticCurveTo(mx, my, c[0], c[1]); ctx.stroke(); ctx.setLineDash([]);
      ctx.save(); ctx.translate(px, py); ctx.rotate(Math.atan2(c[1] - a[1], c[0] - a[0]) * .6 + 1.2); ctx.fillStyle = '#e9f2ff'; ctx.beginPath(); ctx.moveTo(0, -18); ctx.lineTo(5, 0); ctx.lineTo(20, 6); ctx.lineTo(5, 6); ctx.lineTo(3, 16); ctx.lineTo(-3, 16); ctx.lineTo(-5, 6); ctx.lineTo(-20, 6); ctx.lineTo(-5, 0); ctx.closePath(); ctx.fill(); ctx.restore(); }
    ctx.restore();
    const hk = P(t, .1, .3) * (1 - P(t, b[3] - .15, .15)), km = lerp(91287, 146000, eo(P(t, b[1], 1.4)));
    counterHead('नेशनल हाईवे', num(Math.round(km / 100) * 100) + ' किमी', '2014: 91,287 किमी', 380, hk);
    counterHead('एयरपोर्ट', '74 → ' + Math.round(lerp(74, 150, eo(P(t, b[3], 1.2)))) + '+', '2014 से आज तक', 380, P(t, b[3], .3), '#9fd0ff');
    src('सड़क परिवहन मंत्रालय · नागर विमानन मंत्रालय', 1310); vign(.75);
  }},
/* 5 MID HOOK */
{ file: 0, tin: 'glitch', sfx: [[0, 'impact_small'], [.1, 'heartbeat'], [BT(5)[1] - .1, 'heartbeat'], [BT(5)[1], 'braam']],
  draw(t) {
    const b = BT(5); ctx.fillStyle = '#040404'; ctx.fillRect(0, 0, W, H);
    const beat = Math.max(Math.exp(-(((t - .1) * 8) ** 2)), Math.exp(-(((t - b[1]) * 8) ** 2)));
    glowG(540, 1250, 500, .15 + beat * .25);
    T('लेकिन…', 540, 640, 130, GD.white, {a: 'center', f: F.bold, w: 800, al: P(t, .05, .15)});
    T('असली क्रांति', 540, 840, 150, GD.gold, {a: 'center', f: F.bold, w: 800, glow: 'rgba(242,170,60,.9)', gb: 40, al: P(t, .5, .2)});
    const pk = P(t, b[1], .4);
    if (pk > 0) { phoneBody(540, 1180, 240 * eo(pk) + 1, 440 * eo(pk) + 1, 0, (x, y, w, h) => { glowAt(x + w / 2, y + h / 2, w, '242,193,78', .5); T('₹', x + w / 2, y + h / 2 + 40, 120 * eo(pk), GD.gold, {a: 'center', f: F.bold, w: 800}); }, .6);
      T('आपकी जेब में', 540, 1500, 80, GD.white, {a: 'center', f: F.bold, w: 800, al: pk}); }
  }},
/* 6 UPI */
{ file: 6, tin: 'zoomin', sfx: [[.1, 'impact_small'], [.5, 'beep'], [.7, 'ding'], [BT(6)[1], 'ticks', 1.5], [BT(6)[2], 'whoosh'], [BT(6)[2] + .3, 'impact']],
  draw(t, d) {
    const b = BT(6), world = P(t, b[2], .7); bgChar('#08080b', '#15151b', '#060606'); glowG(540, 1000, 700, .18);
    ctx.save(); cam(t, d, 1, 1.05); ctx.globalAlpha = 1 - world * .85;
    ctx.fillStyle = '#2a1d10'; ctx.fillRect(140, 900, 800, 300); ctx.fillStyle = '#4a3016'; ctx.fillRect(110, 860, 860, 50); ctx.fillStyle = GD.amber; ctx.fillRect(110, 640, 860, 70);
    T('चाय की दुकान', 540, 692, 46, '#2a1606', {a: 'center', f: F.bold, w: 800});
    ctx.fillStyle = '#8a8f98'; rr(220, 760, 110, 100, 12); ctx.fill(); ctx.fillStyle = '#6a6f78'; ctx.fillRect(320, 780, 30, 14);
    for (let i = 0; i < 3; i++) { const ph = (NOW * .5 + i / 3) % 1; ctx.fillStyle = `rgba(220,220,220,${.2 * (1 - ph)})`; ctx.beginPath(); ctx.arc(270 + Math.sin(NOW + i) * 8, 740 - ph * 120, 14 + ph * 20, 0, 7); ctx.fill(); }
    ctx.fillStyle = '#f4efe4'; ctx.fillRect(600, 740, 160, 200); ctx.fillStyle = '#111';
    for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) if (hash(r * 9 + c) > .45 || (r < 3 && c < 3) || (r < 3 && c > 5) || (r > 5 && c < 3)) ctx.fillRect(616 + c * 14, 770 + r * 14, 12, 12);
    T('स्कैन करें', 680, 925, 22, '#111', {a: 'center', f: F.bold, w: 800});
    const paid = P(t, .6, .3);
    phoneBody(700, 1120, 200, 360, -.25, (x, y, w, h) => { if (paid > 0) { ctx.fillStyle = '#123'; ctx.fillRect(x, y, w, h); ctx.fillStyle = `rgba(47,163,90,${paid})`; ctx.beginPath(); ctx.arc(x + w / 2, y + h * .4, 46, 0, 7); ctx.fill();
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 8; ctx.beginPath(); ctx.moveTo(x + w / 2 - 20, y + h * .4); ctx.lineTo(x + w / 2 - 4, y + h * .4 + 16); ctx.lineTo(x + w / 2 + 22, y + h * .4 - 16); ctx.stroke();
      T('₹10 भुगतान सफल', x + w / 2, y + h * .65, 22, '#e8f5ec', {a: 'center', f: F.bold, w: 800}); } else feed(x, y, w, h, 0); }, .4);
    ctx.globalAlpha = 1; ctx.restore();
    counterHead('UPI · हर महीने', num(Math.round(20 * eo(P(t, b[1], 1.2)))) + ' अरब+', 'लेन-देन', 380, P(t, b[1], .3) * (1 - P(t, b[2] - .1, .15)));
    if (world > 0) { const cx = 540, cy = 900, r = 260 * eo(world);
      ctx.fillStyle = '#2a2b33'; ctx.beginPath(); ctx.arc(cx, cy, r, 0, 7); ctx.fill();
      ctx.fillStyle = GD.amber; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * .49 * eo(P(t, b[2] + .2, 1))); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.15)'; ctx.lineWidth = 2; for (let k = 0; k < 6; k++) { ctx.beginPath(); ctx.ellipse(cx, cy, r, r * Math.abs(Math.cos(k / 6 * Math.PI + NOW * .3)), 0, 0, 7); ctx.stroke(); }
      T('भारत ~49%', cx + 140, cy - 40, 54, '#fff', {a: 'center', f: F.bold, w: 800, al: world});
      T('दुनिया के रियल-टाइम डिजिटल पेमेंट', 540, 380, 46, GD.white, {a: 'center', f: F.bold, w: 800, al: world}); }
    src(world > 0 ? 'ACI Worldwide 2024' : 'NPCI (2025)', 1310); vign(.75);
  }},
/* 7 Chandrayaan-3 */
{ file: 7, tin: 'flash', sfx: [[.1, 'rocket', 2.4], [BT(7)[2] - .2, 'whoosh'], [BT(7)[2] + 1, 'impact'], [BT(7)[2] + 1.2, 'triumph', 2]],
  draw(t, d) {
    const b = BT(7), moon = P(t, b[2] - .2, .5);
    if (moon < 1) { ctx.save(); ctx.globalAlpha = 1 - moon;
      bgChar('#05060a', '#0f1220', '#0b0907'); glowAt(540, 1300, 600, '255,170,80', .25);
      const lift = io(P(t, .4, 3)) * 900, ry = 1080 - lift;
      ctx.fillStyle = '#121216'; ctx.fillRect(300, 760, 40, 520); for (let y = 780; y < 1280; y += 40) { ctx.fillRect(300, y, 120, 6); }
      for (let i = 0; i < 26; i++) { const ph = (NOW * 1.6 + i / 26) % 1, sp = ph * (200 + lift * .3); ctx.fillStyle = `rgba(${255},${170 + ph * 60},${80 + ph * 120},${.55 * (1 - ph)})`; ctx.beginPath(); ctx.arc(560 + (hash(i) - .5) * sp, ry + 230 + ph * 260, 24 + ph * 70, 0, 7); ctx.fill(); }
      glowAt(560, ry + 220, 160, '255,200,120', .8);
      ctx.fillStyle = '#e9e6df'; rr(530, ry - 200, 60, 380, 8); ctx.fill(); ctx.fillStyle = '#c9c4b8'; rr(486, ry - 20, 40, 220, 16); ctx.fill(); rr(594, ry - 20, 40, 220, 16); ctx.fill();
      ctx.fillStyle = '#e9e6df'; ctx.beginPath(); ctx.moveTo(530, ry - 200); ctx.quadraticCurveTo(560, ry - 280, 590, ry - 200); ctx.fill(); ctx.fillStyle = GD.saffron; ctx.fillRect(532, ry - 60, 56, 10);
      T('ISRO · LVM3', 560, ry + 40, 18, '#333', {a: 'center', f: F.mono, w: 700});
      ctx.restore(); }
    if (moon > 0) { ctx.save(); ctx.globalAlpha = moon;
      ctx.fillStyle = '#030305'; ctx.fillRect(0, 0, W, H); for (let i = 0; i < 120; i++) { ctx.fillStyle = `rgba(255,255,255,${.3 + hash(i) * .6})`; ctx.fillRect(hash(i * 3) * W, hash(i * 7) * 900, 2, 2); }
      ctx.fillStyle = '#2a8bd6'; ctx.beginPath(); ctx.arc(860, 300, 60, 0, 7); ctx.fill(); ctx.fillStyle = 'rgba(255,255,255,.4)'; ctx.beginPath(); ctx.arc(845, 285, 22, 0, 7); ctx.fill();
      const g = ctx.createLinearGradient(0, 900, 0, H); g.addColorStop(0, '#8a8680'); g.addColorStop(1, '#2a2826'); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(0, 980); ctx.quadraticCurveTo(540, 880, W, 980); ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.closePath(); ctx.fill();
      for (let i = 0; i < 9; i++) { ctx.fillStyle = 'rgba(40,38,36,.5)'; ctx.beginPath(); ctx.ellipse(hash(i) * W, 1050 + hash(i + 3) * 250, 40 + hash(i + 5) * 70, 12 + hash(i + 2) * 20, 0, 0, 7); ctx.fill(); }
      const land = io(P(t, b[2], 1.1)), ly = lerp(560, 1000, land);
      if (land >= 1) for (let i = 0; i < 14; i++) { const ph = P(t, b[2] + 1.1, 1.2); ctx.fillStyle = `rgba(180,175,165,${.4 * (1 - ph)})`; ctx.beginPath(); ctx.arc(540 + (hash(i) - .5) * 500 * ph, 1010 - ph * 40, 20 + ph * 30, 0, 7); ctx.fill(); }
      ctx.fillStyle = '#c9a54a'; rr(490, ly - 70, 100, 70, 8); ctx.fill(); ctx.fillStyle = '#d9d6cf'; ctx.fillRect(500, ly - 100, 80, 30);
      ctx.strokeStyle = '#d9d6cf'; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(500, ly); ctx.lineTo(470, ly + 30); ctx.moveTo(580, ly); ctx.lineTo(610, ly + 30); ctx.stroke();
      if (land < 1) glowAt(540, ly + 20, 80, '255,210,150', .6);
      T('चंद्रयान-3 · 23 अगस्त 2023', 540, 1180, 48, GD.white, {a: 'center', f: F.bold, w: 800, al: P(t, b[2] + 1, .4)});
      T('दक्षिणी ध्रुव के पास उतरने वाला पहला मिशन', 540, 1240, 34, GD.gold, {a: 'center', w: 600, al: P(t, b[2] + 1.2, .4)});
      ctx.restore(); }
    T('2023', 540, 330, 80, GD.gold, {a: 'center', f: F.mono, w: 700, al: P(t, .1, .3)}); src('ISRO', 1310); vign(.7);
  }},
/* 8 vaccines */
{ file: 8, tin: 'zoomin', sfx: [[.1, 'impact_small'], [.3, 'ticks', 2], [1.8, 'impact']],
  draw(t, d) {
    bgChar('#07080b', '#11141a', '#050506'); glowAt(540, 900, 700, '140,200,255', .1);
    ctx.save(); cam(t, d, 1, 1.07);
    for (let r = 0; r < 5; r++) for (let c = 0; c < 8; c++) { const k = P(t, .2 + (r * 8 + c) * .03, .4), s = .9 + r * .18, x = 130 + c * 117 + (r % 2) * 20, y = 620 + r * 140;
      ctx.save(); ctx.globalAlpha = eo(k); vial(x, y, s, eo(k)); ctx.restore(); }
    ctx.restore();
    counterHead('कोरोना के दौर में', num(Math.round(220 * eo(P(t, .3, 1.8)))) + ' करोड़+', 'वैक्सीन डोज़', 380, P(t, .1, .3), '#bfe2ff');
    src('स्वास्थ्य मंत्रालय · CoWIN', 1310); vign(.75);
  }},
/* 9 poverty */
{ file: 9, tin: 'whip', sfx: [[.1, 'impact_small'], [.4, 'rise', 1.6], [BT(9)[3], 'triumph', 1.6]],
  draw(t, d) {
    const b = BT(9); sunrise(t, 1250, .4 + .5 * P(t, b[3], 1.2));
    const base = 1180, sc = 17, bars = [[29.17, '2013-14', '#5a5b66', .5], [11.28, '2022-23', GD.gold, 1.4]];
    bars.forEach(([v, yr, col, st], i) => { const k = io(P(t, st, 1)), h = v * sc * k, x = 260 + i * 360;
      ctx.fillStyle = col; rr(x, base - h, 200, h, [10, 10, 0, 0]); ctx.fill();
      T(num(v * k, 2) + '%', x + 100, base - h - 24, 50, GD.white, {a: 'center', f: F.bold, w: 800, al: k > 0 ? 1 : 0}); T(yr, x + 100, base + 48, 32, GD.steel, {a: 'center', f: F.mono, w: 700}); });
    for (let i = 0; i < 14; i++) { const k = P(t, b[3] + i * .05, .5); person(90 + i * 70, 1260, 16, `rgba(255,214,140,${.2 + .75 * k})`, 1); }
    counterHead('नीति आयोग के मुताबिक़', '~' + num(24.82 * eo(P(t, .3, 2)), 2) + ' करोड़', 'लोग बहुआयामी गरीबी से बाहर', 380, P(t, .1, .3));
    src('नीति आयोग, 2024', 1310); vign(.75);
  }},
/* 10 2047 */
{ file: 10, tin: 'zoomin', sfx: [[.1, 'braam'], [.3, 'rise', 2.4], [BT(10)[1], 'triumph', 2.4]],
  draw(t, d) {
    const b = BT(10), k = P(t, b[1], 1.2); sunrise(t, 1150, .5 + .5 * k);
    ctx.save(); cam(t, d, 1.05, 1);
    drawMap({cx: 540, cy: 920, scale: 26, tilt: .88, yaw: lerp(.1, -.08, io(t / d)), top: ['#5a4320', '#2a1e0e'], side: [[30, 20, 8], [120, 84, 30]], edge: '#ffd27a', grid: 'rgba(255,210,120,.08)', alpha: .4 + .6 * eo(P(t, .1, .8))});
    ctx.restore();
    const x0 = 120, x1 = 960, y = 450, kk = io(P(t, .2, d - .4));
    ctx.strokeStyle = 'rgba(255,230,190,.3)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(x1, y); ctx.stroke();
    ctx.save(); ctx.shadowColor = GD.gold; ctx.shadowBlur = 20; ctx.strokeStyle = GD.gold; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(lerp(x0, x1, kk), y); ctx.stroke(); ctx.restore();
    [['2014', 0], ['आज', .4], ['2047', 1]].forEach(([s, u]) => { const on = kk >= u - .001; ctx.fillStyle = on ? GD.gold : 'rgba(255,230,190,.4)'; ctx.beginPath(); ctx.arc(lerp(x0, x1, u), y, on ? 12 : 7, 0, 7); ctx.fill();
      T(s, lerp(x0, x1, u), y - 28, 34, on ? GD.white : 'rgba(255,230,190,.5)', {a: 'center', f: F.mono, w: 700}); });
    pop(540, 330, k, () => T('विकसित भारत 2047', 0, 0, 92, GD.gold, {a: 'center', f: F.bold, w: 800, glow: 'rgba(242,170,60,.8)', gb: 30}));
    T(typed('सफ़र अभी लंबा है…', P(t, .1, .8)), 540, 330, 64, GD.white, {a: 'center', f: F.head, w: 400, al: 1 - k});
    flag(830, 880 - 220, .8, t);
    vign(.7);
  }},
/* 11 END question */
{ file: 0, tin: 'zoomin', sfx: [[0, 'impact_big'], [.5, 'blips'], [BT(11)[2], 'impact_small'], [BT(11)[2] + .2, 'heartbeat']],
  draw(t, d) {
    const b = BT(11); sunrise(t, 1300, .5);
    pop(540, 360, P(t, .1, .3), () => { T('आपके हिसाब से', 0, -70, 56, GD.steel, {a: 'center', f: F.bold, w: 800}); T('2014 के बाद', 0, 20, 76, GD.white, {a: 'center', f: F.bold, w: 800}); T('सबसे बड़ा बदलाव?', 0, 120, 92, GD.gold, {a: 'center', f: F.bold, w: 800, glow: 'rgba(242,170,60,.7)', gb: 24}); });
    ['UPI', 'हाईवे', 'चंद्रयान', 'गैस', 'बैंक खाते', 'वैक्सीन'].forEach((s, i) => { const x = 300 + (i % 2) * 480, y = 720 + Math.floor(i / 2) * 140;
      pop(x, y, P(t, .5 + i * .15, .3), () => { rr(-215, -52, 430, 104, 14); ctx.fillStyle = 'rgba(16,14,10,.9)'; ctx.fill(); ctx.strokeStyle = i % 2 ? GD.gold : GD.saffron; ctx.lineWidth = 3; ctx.stroke();
        T(String.fromCharCode(65 + i), -175, 16, 44, i % 2 ? GD.gold : GD.saffron, {a: 'center', f: F.mono, w: 700}); T(s, 20, 16, 50, GD.white, {a: 'center', f: F.bold, w: 800}); }); });
    const pulse = 1 + Math.sin(NOW * 6) * .04;
    pop(540, 1280, P(t, b[2], .3), () => { ctx.scale(pulse, pulse); rr(-330, -60, 660, 120, 60); ctx.fillStyle = GD.amber; ctx.fill(); T('कमेंट में बताइए ↓', 0, 22, 62, '#1a1206', {a: 'center', f: F.bold, w: 800}); });
    vign(.7);
  }}
];
