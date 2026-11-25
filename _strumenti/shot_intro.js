const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
for (const [w,h,tag] of [[1440,900,'d'],[390,844,'m']]) {
  const p = await b.newPage({ viewport: { width: w, height: h }, locale: 'it-IT' });
  await p.goto('http://localhost:8123/index.html'); await p.waitForTimeout(1500);
  const fr = [0.25, 0.45, 0.55, 0.7, 1.0];
  for (const z of fr) {
    await p.evaluate((z) => window.scrollTo({ top: z * innerHeight * 1.4, behavior: 'instant' }), z);
    await p.waitForTimeout(1200);
    await p.screenshot({ path: `/home/claude/preview/intro-${tag}-${z}.png` });
  }
}
await b.close(); })();
