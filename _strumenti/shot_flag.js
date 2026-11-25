const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
for (const [w,h] of [[1280,800],[390,844]]) { const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 3, locale:'it-IT' });
  await p.goto('http://localhost:8123/index.html'); await p.waitForTimeout(800);
  for (const L of ['it','en','es','fr','pt']) {
    await p.click('#langBtn'); await p.click(`[data-lang="${L}"]`); await p.waitForTimeout(150);
    await p.screenshot({ path: `/tmp/flag-${w}-${L}.png`, clip: { x: 0, y: 0, width: 110, height: 60 } }); }
  await p.evaluate(()=>window.scrollTo(0,3000)); await p.waitForTimeout(800);
  await p.screenshot({ path: `/tmp/flag-${w}-light.png`, clip: { x: 0, y: 0, width: 110, height: 60 } });
  await p.close(); }
for (const L of ['fr','pt']) { const p = await b.newPage({ deviceScaleFactor: 3 }); await p.goto(`http://localhost:8123/${L}/`, {waitUntil:'domcontentloaded'}); await p.screenshot({ path:`/tmp/flag-static-${L}.png`, clip:{x:0,y:0,width:110,height:60}}); await p.close(); }
await b.close(); })();
