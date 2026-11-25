const { chromium } = require('playwright');
(async () => { const [, , html, out, w, h] = process.argv; const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w || 2400, height: +h || 1350 } });
  p.on('pageerror', e => console.log('ERR', e.message)); await p.goto('file://' + html); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 20000 });
  await p.screenshot({ path: out }); await b.close(); })();
