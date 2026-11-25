// node render_test.js <html> <out.mp4> <seconds> [fps]   — frames → ffmpeg (H.264)
const { chromium } = require('playwright'); const { spawn } = require('child_process');
(async () => {
  const [, , html, out, secs, fpsArg] = process.argv, fps = +fpsArg || 30, N = Math.round(+secs * fps);
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await p.goto('file://' + html + '#render'); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 });
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < N; i++) { await p.evaluate(t => draw(t), i / fps); const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if (i % 90 === 0) console.log('frame', i, '/', N); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('done', out);
})();
