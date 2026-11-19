// Renders index.html frame-by-frame to video.mp4 (no audio) and writes the sound cue list to sfx.json.
// Usage: node tools/render.js   (run from the india-explained folder; needs Playwright + ffmpeg)
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const fs = require('fs'); const path = require('path');
const dir = path.resolve(__dirname, '..');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(dir, 'index.html'));
  await p.waitForFunction(() => window.__doc && window.__doc.ready, null, { timeout: 60000 });
  await p.evaluate(() => window.__doc.stop());
  const { total, sfx } = await p.evaluate(() => ({ total: window.__doc.total, sfx: window.__doc.sfx }));
  fs.writeFileSync(path.join(__dirname, 'sfx.json'), JSON.stringify(sfx, null, 1));
  if (process.argv.includes('--cues-only')) { await b.close(); return; }
  const fps = 30, n = Math.round(total * fps);
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', path.join(dir, 'video_only.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < n; f++) {
    const d = await p.evaluate(g => { window.__doc.render(g); return document.getElementById('cv').toDataURL('image/jpeg', .93); }, (f + .5) / fps);
    if (!ff.stdin.write(Buffer.from(d.slice(d.indexOf(',') + 1), 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 300 === 0) console.log('frame', f, '/', n);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('video done');
})();
