const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
for (const L of ['es','fr','pt']) for (const [w,h] of [[1440,900],[390,844]]) {
  const p = await b.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
  await p.goto(`http://localhost:8123/${L}/`); await p.waitForTimeout(400);
  await p.evaluate(() => { document.querySelectorAll('img').forEach(i => i.loading='eager'); document.querySelectorAll('.stagger').forEach(e => e.classList.add('in')); });
  await p.waitForTimeout(1200);
  const ov = await p.evaluate(() => { const W = document.documentElement.clientWidth; return [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.right > W + 1 && getComputedStyle(e).position !== 'fixed' && !e.closest('.intro'); }).slice(0,5).map(e => e.tagName + '.' + e.className + ' ' + (e.textContent||'').slice(0,40)); });
  console.log(L, w, 'overflow:', JSON.stringify(ov));
  await p.screenshot({ path: `/tmp/lang-${L}-${w}.png`, fullPage: true });
}
await b.close(); })();
