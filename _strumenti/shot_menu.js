const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 844 }, locale: 'it-IT', deviceScaleFactor: 2 });
await p.goto('http://localhost:8123/index.html'); await p.waitForTimeout(1500); await p.click('#langBtn'); await p.waitForTimeout(300);
await p.screenshot({ path: '/home/claude/preview/langmenu.png', clip: { x: 0, y: 0, width: 260, height: 300 } }); await b.close(); })();
