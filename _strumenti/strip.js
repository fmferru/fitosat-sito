const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
for (const pg of ['_before.html','index.html']) {
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  await p.goto('http://localhost:8123/'+pg); await p.waitForTimeout(2000);
  for (let i = 0; i <= 12; i++) {
    await p.evaluate(y => window.scrollTo(0, y), i * 800 * 1.4 / 12 * 1.0);
    await p.waitForTimeout(700);
    await p.screenshot({ path: `/tmp/st-${pg[0]}-${String(i).padStart(2,'0')}.png` });
  }
  await p.close();
}
await b.close(); })();
