const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
for (const L of ['es','fr','pt']) { const p = await b.newPage({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce', deviceScaleFactor: 2 });
  await p.goto(`http://localhost:8123/${L}/`); await p.evaluate(() => document.querySelectorAll('img').forEach(i => i.loading='eager'));
  const f = await p.$('.vine-fig'); await f.scrollIntoViewIfNeeded(); await p.waitForTimeout(1500);
  await f.screenshot({ path: `/tmp/vine-${L}.png` }); }
await b.close(); })();
