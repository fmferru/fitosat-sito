const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 360, height: 760 } });
for (const u of ['index.html','pt/']) { await p.goto('http://localhost:8123/'+u); await p.waitForTimeout(500); await p.evaluate(()=>window.scrollTo(0,3000)); await p.waitForTimeout(800);
console.log(u, await p.evaluate(() => { const a=document.getElementById('langBtn').getBoundingClientRect(); const n=document.querySelector('.topnav'); const r=n&&n.getBoundingClientRect(); const v=n?getComputedStyle(n).visibility+'/'+getComputedStyle(n).opacity:''; return {btnRight:a.right, navLeft:r&&r.left, nav:v}; })); }
await b.close(); })();
