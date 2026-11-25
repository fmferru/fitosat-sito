const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 }, locale:'it-IT' });
await p.goto('http://localhost:8123/index.html'); await p.waitForTimeout(1500);
for (let i = 1; i <= 10; i++) { await p.keyboard.press('Tab'); await p.waitForTimeout(400);
  const r = await p.evaluate(() => { const e = document.activeElement; const cs = getComputedStyle(e); let o=1, x=e; while (x && x!==document.body){ o*= +getComputedStyle(x).opacity; x=x.parentElement;} const rc=e.getBoundingClientRect(); return (e.id||e.tagName)+' "'+(e.textContent||'').trim().slice(0,25)+'" outline='+cs.outlineStyle+' '+cs.outlineWidth+' '+cs.outlineColor+' opacity='+o.toFixed(2)+' y='+Math.round(rc.top); });
  console.log(i, r); if (i==4||i==8||i==9) await p.screenshot({ path: `/tmp/tab${i}.png` }); }
await b.close(); })();
