const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
for (const [w,h] of [[1100,560],[1440,900],[390,780]]) { const p = await b.newPage({ viewport: { width: w, height: h }, locale: 'it-IT' });
await p.goto('http://localhost:8123/index.html'); await p.evaluate(() => document.querySelectorAll('img').forEach(i => i.loading='eager'));
await p.evaluate(() => { document.querySelectorAll('.stagger').forEach(e => e.classList.add('in')); const f=document.querySelector('.vine-fig'); const r=f.getBoundingClientRect(); window.scrollTo({top: scrollY + r.top - (innerHeight - r.height)/2 - 20, behavior:'instant'}); });
await p.waitForTimeout(900); await p.screenshot({ path: `/home/claude/preview/fit-${w}.png` }); }
await b.close(); })();
