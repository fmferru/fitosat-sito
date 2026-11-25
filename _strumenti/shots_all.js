const { chromium } = require('playwright');
const tag = process.argv[2];
(async () => { const b = await chromium.launch();
for (const [w,h] of [[1440,900],[390,844]]) { const p = await b.newPage({ viewport: { width: w, height: h }, locale: 'it-IT', reducedMotion: 'reduce' });
  await p.goto('http://localhost:8123/index.html'); await p.waitForTimeout(500);
  await p.evaluate(() => { document.querySelectorAll('img').forEach(i => i.loading='eager'); document.querySelectorAll('.stagger').forEach(e => e.classList.add('in')); });
  await p.waitForTimeout(1500);
  await p.screenshot({ path: `/tmp/cmp-${tag}-${w}.png`, fullPage: true }); }
await b.close(); })();
