const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
for (const w of [1440, 390]) { const p = await b.newPage({ viewport: { width: w, height: 800 }, locale: 'it-IT' });
await p.goto('http://localhost:8123/index.html'); const f = await p.$('footer'); await f.scrollIntoViewIfNeeded(); await p.waitForTimeout(300);
await f.screenshot({ path: `/home/claude/preview/foot-${w}.png` }); }
await b.close(); })();
