const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const w of [1440, 1000, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 }, locale: 'it-IT' });
    await p.goto('http://localhost:8123/index.html');
    await p.evaluate(() => { document.querySelectorAll('.stagger').forEach(e => e.classList.add('in')); });
    const el = await p.$('.vine-why'); await el.scrollIntoViewIfNeeded();
    await p.evaluate(() => document.querySelectorAll('img').forEach(i => i.loading = 'eager'));
    await p.waitForTimeout(1200);
    const bb = await p.evaluate(() => { const a = document.querySelector('.vine-why').getBoundingClientRect(), f = document.querySelector('.vine-fig').getBoundingClientRect(); return { y: a.top, height: f.bottom - a.top }; });
    await p.screenshot({ path: `/home/claude/preview/vine-${w}.png`, fullPage: true, clip: { x: 0, y: bb.y + (await p.evaluate(() => scrollY)) - 110, width: w, height: bb.height + 220 } });
  }
  await b.close();
})();
