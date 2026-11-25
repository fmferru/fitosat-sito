const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 900 } });
await p.goto('http://localhost:8123/index.html');
console.log(await p.evaluate(() => { const li = document.querySelector('.vine-fig .vine-uses li'); const h=li.querySelector('h4'); const dv=li.querySelector('div'); return [getComputedStyle(li).textAlign, getComputedStyle(dv).textAlign, getComputedStyle(h).textAlign, getComputedStyle(dv).flexGrow, dv.getBoundingClientRect().width, li.getBoundingClientRect().width]; }));
await b.close(); })();
