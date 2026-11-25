const { chromium } = require('playwright');
(async () => { for (const args of [[], ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'], ['--use-gl=angle', '--use-angle=swiftshader-webgl']]) {
  const b = await chromium.launch({ args }); const p = await b.newPage();
  const r = await p.evaluate(() => { const c = document.createElement('canvas'); const g = c.getContext('webgl2'); if (!g) return 'no webgl2'; const d = g.getExtension('WEBGL_debug_renderer_info'); return d ? g.getParameter(d.UNMASKED_RENDERER_WEBGL) : 'webgl2 ok'; });
  console.log(JSON.stringify(args), '→', r); await b.close(); } })();
