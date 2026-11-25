const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const fails = []; const f = m => fails.push(m);
const IT_WORDS = /\b(piante|filare|vigneto|coltur[ae]|ettari|Scopri|Provalo|Contatti|soffrendo)\b/;
const errs = [];
// pagine statiche
for (const L of ['es','fr','pt']) {
  for (const js of [true,false]) {
    const c = await b.newContext({ javaScriptEnabled: js, viewport: { width: 1280, height: 800 }, locale: 'it-IT' }); const p = await c.newPage();
    p.on('pageerror', e => errs.push(L+': '+e.message)); p.on('requestfailed', r => errs.push(L+' failed '+r.url()));
    await p.goto(`http://localhost:8123/${L}/`); await p.waitForTimeout(600);
    const r = await p.evaluate(() => ({ lang: document.documentElement.lang, title: document.title, h1: document.querySelector('h1').textContent, txt: document.body.innerText, priv: (document.querySelector('a[data-privacy]')||{}).getAttribute && document.querySelector('a[data-privacy]').getAttribute('href') }));
    if (r.lang !== L) f(`${L} js=${js} html lang ${r.lang}`);
    const m = r.txt.match(IT_WORDS); if (m) f(`${L} js=${js} italian word left: ${m[0]} …${r.txt.slice(Math.max(0,m.index-60), m.index+40).replace(/\n/g,' ')}`);
    if (js && r.priv !== 'privacy.html') f(`${L} privacy href ${r.priv}`);
    await c.close();
  }
}
// cambio lingua dal menu sulla pagina italiana
const c = await b.newContext({ viewport: { width: 1280, height: 800 }, locale: 'it-IT' }); const p = await c.newPage();
await p.goto('http://localhost:8123/index.html'); await p.waitForTimeout(500);
for (const [L, word] of [['es','Descubre'],['fr','Découvrez'],['pt','Descubra'],['en','See which'],['it','Scopri']]) {
  await p.click('#langBtn'); await p.click(`[data-lang="${L}"]`); await p.waitForTimeout(200);
  const r = await p.evaluate(() => ({ h1: document.querySelector('h1').textContent, cur: document.getElementById('langCur').textContent, lang: document.documentElement.lang, priv: document.querySelector('a[data-privacy]').getAttribute('href'), legal: document.querySelector('a[data-legal]').getAttribute('href'), txt: document.body.innerText }));
  if (!r.h1.startsWith(word)) f(`switch ${L}: h1 ${r.h1}`);
  if (r.cur !== L.toUpperCase() || r.lang !== L) f(`switch ${L}: cur/lang ${r.cur}/${r.lang}`);
  const wantP = L === 'it' ? 'privacy.html' : L + '/privacy.html'; if (r.priv !== wantP) f(`switch ${L}: privacy ${r.priv}`);
  if (L !== 'it') { const m = r.txt.match(IT_WORDS); if (m) f(`switch ${L}: italian left ${m[0]} …${r.txt.slice(Math.max(0,m.index-60), m.index+40).replace(/\n/g,' ')}`); }
}
// lingua del browser
for (const [loc, want] of [['es-ES','ES'],['fr-FR','FR'],['pt-BR','PT'],['de-DE','EN']]) {
  const c2 = await b.newContext({ locale: loc }); const p2 = await c2.newPage(); await p2.goto('http://localhost:8123/index.html'); await p2.waitForTimeout(300);
  const cur = await p2.evaluate(() => document.getElementById('langCur').textContent); if (cur !== want) f(`browser ${loc} -> ${cur}`); await c2.close();
}
// pagine legali
for (const L of ['es','fr','pt']) for (const pg of ['privacy.html','note-legali.html']) {
  const c3 = await b.newContext(); const p3 = await c3.newPage(); const res = await p3.goto(`http://localhost:8123/${L}/${pg}`);
  if (res.status() !== 200) f(`${L}/${pg} ${res.status()}`);
  const r = await p3.evaluate(() => ({ lang: document.documentElement.lang, links: [...document.querySelectorAll('header nav a')].map(a => a.getAttribute('href')), css: getComputedStyle(document.body).fontFamily }));
  if (r.lang !== L || r.links.length !== 5) f(`${L}/${pg} ${JSON.stringify(r)}`);
  for (const h of r.links) { const rr = await p3.request.get(new URL(h, `http://localhost:8123/${L}/${pg}`).href); if (rr.status() !== 200) f(`${L}/${pg} link ${h} ${rr.status()}`); }
  await c3.close();
}
if (errs.length) f(errs.join('\n'));
console.log(fails.length ? fails.join('\n') : 'PASS'); await b.close(); })();
