const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
for (const [w,h,t] of [[1440,900,'d'],[390,844,'m']]) { const p = await b.newPage({ viewport: { width: w, height: h }, locale: 'it-IT', deviceScaleFactor: 2 });
  await p.goto('http://localhost:8123/index.html'); await p.waitForTimeout(2500);
  await p.screenshot({ path: `/home/claude/preview/logo-${t}.png` }); }
await b.close(); })();
