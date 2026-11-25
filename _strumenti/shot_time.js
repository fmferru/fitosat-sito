const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
for (const [w,h] of [[1100,560],[1440,900],[390,780]]) { const p = await b.newPage({ viewport: { width: w, height: h }, locale: 'it-IT' });
await p.goto('http://localhost:8123/index.html');
await p.evaluate(() => { const f=document.querySelector('.how #field'); const r=f.getBoundingClientRect(); window.scrollTo({top: scrollY + r.top - 90, behavior:'instant'}); });
await p.waitForTimeout(600); await p.screenshot({ path: `/home/claude/preview/how-${w}.png` });
await p.evaluate(() => { const f=document.querySelector('.time'); const r=f.getBoundingClientRect(); window.scrollTo({top: scrollY + r.top, behavior:'instant'}); });
await p.waitForTimeout(600); await p.screenshot({ path: `/home/claude/preview/time-${w}.png` }); }
await b.close(); })();
