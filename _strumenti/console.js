const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = [];
for (const u of ['index.html','en/index.html','es/index.html','fr/index.html','pt/index.html','privacy.html','es/privacy.html','fr/note-legali.html','pt/note-legali.html']) {
  const p = await b.newPage(); p.on('console', m => { if (m.type()==='error' || m.type()==='warning') errs.push(u+': '+m.text()); }); p.on('pageerror', e => errs.push(u+': '+e.message));
  p.on('requestfailed', r => errs.push(u+': failed '+r.url()));
  await p.goto('http://localhost:8123/'+u); await p.evaluate(()=>window.scrollTo(0,document.body.scrollHeight)); await p.waitForTimeout(800); }
console.log(errs.length ? errs.join('\n') : 'no console errors'); await b.close(); })();
