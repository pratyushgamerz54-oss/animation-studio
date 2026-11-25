const { chromium } = require('playwright');
(async () => { const [, , html, out, ...ts] = process.argv; const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message)); await p.goto('file://' + html + '#render'); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 });
  for (const t of ts) { await p.evaluate(t => draw(t), +t); await p.screenshot({ path: out.replace('%', t) }); } await b.close(); })();
