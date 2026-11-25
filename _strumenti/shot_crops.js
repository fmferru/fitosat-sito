const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
for (const [w,h] of [[1100,560],[1440,900]]) { const p = await b.newPage({ viewport: { width: w, height: h }, locale: 'it-IT' });
await p.goto('http://localhost:8123/index.html');
await p.evaluate(() => { const f=document.querySelector('.beyond'); const r=f.getBoundingClientRect(); window.scrollTo({top: scrollY + r.top + 20, behavior:'instant'}); });
await p.waitForTimeout(900); await p.screenshot({ path: `/home/claude/preview/crops-${w}.png` }); }
await b.close(); })();
