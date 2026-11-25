// node render.js <dir> <page.html> <out.mp4|snap:t1,t2,...> <seconds> [fps]
// Serves <dir> on localhost (ES modules need http), renders frames sequentially (physics is stepped frame by frame).
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const http = require('http'); const fs = require('fs'); const path = require('path');
const [, , dir, page, out, secs, fpsArg] = process.argv; const fps = +fpsArg || 30;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json' };
const srv = http.createServer((q, r) => { const f = path.join(dir, decodeURIComponent(q.url.split('?')[0].split('#')[0])); if (!f.startsWith(dir) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); });
srv.listen(0, '127.0.0.1', async () => {
  const port = srv.address().port, b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] }), p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('console', m.text()); });
  await p.goto(`http://127.0.0.1:${port}/${page}#render`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 180000 });
  const wrap = await p.$('#wrap');
  if (out.startsWith('snap:')) { const ts = out.slice(5).split(',').map(Number), N = Math.round(Math.max(...ts) * fps);
    for (let i = 0; i <= N; i++) { const t = i / fps, hit = ts.find(x => Math.abs(x - t) < 0.5 / fps); await p.evaluate(([t, nr]) => draw(t, nr), [t, hit === undefined]); if (hit !== undefined) { await wrap.screenshot({ path: path.join(dir, `_snap_${hit}.png`) }); console.log('snap', hit); } }
  } else { const N = Math.round(+secs * fps), t0 = Date.now(), from = +(process.env.FROM || 0);
    for (let i = 0; i < Math.round(from * fps); i++) await p.evaluate(t => draw(t, true), i / fps);
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = Math.round(from * fps); i < N; i++) { await p.evaluate(t => draw(t), i / fps); const buf = await wrap.screenshot({ type: 'jpeg', quality: 92 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 60 === 0) console.log('frame', i, '/', N, ((Date.now() - t0) / 1000 / (i + 1)).toFixed(2), 's/frame'); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log('done', out); }
  await b.close(); srv.close(); });
