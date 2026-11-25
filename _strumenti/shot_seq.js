const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, locale: 'it-IT' });
await p.goto('http://localhost:8123/index.html'); await p.waitForTimeout(1500);
const zs = [0.2, 0.3, 0.38, 0.46, 0.56, 0.8];
for (const z of zs) { await p.evaluate((z) => window.scrollTo({ top: z * innerHeight * 1.4, behavior: 'instant' }), z); await p.waitForTimeout(900);
  await p.screenshot({ path: `/tmp/seq-${z}.png` }); }
await b.close(); })();
