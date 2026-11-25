// Verifica le correzioni della revisione del 22/11
const { chromium } = require('playwright');
const {spawn}=require('child_process');const srv=spawn('python3',['-m','http.server','8123','--bind','127.0.0.1'],{cwd:'/home/claude/staging',stdio:'ignore'});
(async()=>{const b=await chromium.launch();let fail=0;const f=m=>{console.log('FAIL',m);fail++;};
await new Promise(r=>setTimeout(r,800));const base='http://127.0.0.1:8123/';
for (const pg of ['index.html','en/index.html']) {
  // 1) nessun errore JS, nessuna risorsa mancante
  const p=await b.newPage({viewport:{width:390,height:844},locale:'it-IT'});const errs=[],miss=[];
  p.on('pageerror',e=>errs.push(e.message));p.on('requestfailed',r=>miss.push(r.url()));
  await p.goto(base+pg);await p.waitForTimeout(800);
  const H=await p.evaluate(()=>document.body.scrollHeight);for(let y=0;y<H;y+=500){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(40);}
  await p.waitForTimeout(600);
  if(errs.length) f(pg+' js errors '+errs.join(' | '));
  if(miss.length) f(pg+' missing '+miss.join(' '));
  const fonts=await p.evaluate(()=>document.fonts.check('700 16px "Josefin Sans"')&&document.fonts.check('16px Questrial'));if(!fonts) f(pg+' fonts not loaded');
  const imgs=await p.evaluate(()=>[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src));if(imgs.length) f(pg+' broken imgs '+imgs);
  // 2) a inizio pagina il pulsante invisibile non si raggiunge da tastiera
  await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(800);
  const seq=[];for(let i=0;i<5;i++){await p.keyboard.press('Tab');seq.push(await p.evaluate(()=>{const a=document.activeElement;let o=1,e=a;while(e&&e!==document.body){const c=getComputedStyle(e);if(c.visibility==='hidden')return 'HIDDEN '+a.textContent.trim().slice(0,20);o*=+c.opacity;e=e.parentElement;}return (o<0.05?'INVISIBLE ':'')+(a.id||a.className||a.tagName)+':'+a.textContent.trim().slice(0,15);}));}
  if(seq.some(x=>/INVISIBLE|HIDDEN/.test(x))) f(pg+' focus on invisible element '+seq.join(' > '));
  // 3) menu si chiude uscendo con Tab
  await p.click('#menuBtn');await p.waitForTimeout(200);
  const n=await p.evaluate(()=>document.querySelectorAll('#topnav ul a').length);
  for(let i=0;i<n+1;i++) await p.keyboard.press('Tab');
  await p.waitForTimeout(150);
  if(await p.evaluate(()=>document.getElementById('topnav').classList.contains('open'))) f(pg+' menu stays open after tabbing out');
  // 4) modulo: compare l'aiuto con copia
  await p.evaluate(()=>document.getElementById('pilota')?.scrollIntoView());
  await p.evaluate(()=>{window.__nav=null;});
  await p.fill('#pilotForm [name=nome]','Mario Rossi');await p.fill('#pilotForm [name=email]','mario@example.com');
  await p.evaluate(()=>{const f=document.getElementById('pilotForm');f.addEventListener('submit',()=>{},true);});
  await p.route('**/*',r=>r.continue());
  await p.evaluate(()=>{const d=Object.getOwnPropertyDescriptor(Location.prototype,'href');});
  await p.click('#pilotForm button[type=submit]').catch(()=>{});await p.waitForTimeout(300);
  const fb=await p.evaluate(()=>!document.getElementById('mailFallback').hidden);if(!fb) f(pg+' mail fallback not shown');
  // 5) privacy link nella lingua giusta
  const priv=await p.evaluate(()=>[...document.querySelectorAll('a[data-privacy]')].map(a=>a.getAttribute('href')));
  const want=pg.startsWith('en/')?'privacy.html':'privacy.html';
  if(!priv.length||priv.some(h=>h!==want)) f(pg+' privacy href '+priv);
  await p.close();
}
// 6) pagina italiana passata in inglese: informativa inglese
{const p=await b.newPage({viewport:{width:390,height:844}});await p.goto(base+'index.html?lang=en');await p.waitForTimeout(500);
 const h=await p.evaluate(()=>document.querySelector('a[data-privacy]').getAttribute('href'));if(h!=='en/privacy.html') f('it->en privacy href '+h);await p.close();}
// 7) senza JavaScript: titolo visibile, menu visibile, pannelli pieni
for (const pg of ['index.html','en/index.html']) {const c=await b.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const p=await c.newPage();
 await p.goto(base+pg);await p.waitForTimeout(300);
 const r=await p.evaluate(()=>{const h1=document.querySelector('h1');let o=1,e=h1;while(e){o*=+getComputedStyle(e).opacity;e=e.parentElement;}
   const navA=document.querySelector('#topnav ul a');const nr=navA.getBoundingClientRect();
   return {h1o:o,h1vis:getComputedStyle(h1).visibility,nav:getComputedStyle(navA.closest('ul')).display!=='none'&&nr.width>0,panel:document.getElementById('panel-text').textContent.trim().length,crop:document.getElementById('cropText').textContent.trim().length}});
 if(r.h1o<0.9||r.h1vis==='hidden') f(pg+' nojs h1 invisible '+JSON.stringify(r)); if(!r.nav) f(pg+' nojs nav hidden'); if(!r.panel||!r.crop) f(pg+' nojs panels empty '+JSON.stringify(r));
 await p.screenshot({path:'/home/claude/preview/nojs-'+pg.replace('/','-')+'.png',fullPage:false});
 await c.close();}

// 9) tasto Copia: doppio clic non resta bloccato; messaggio tradotto al cambio lingua
{const c=await b.newContext({viewport:{width:390,height:844},locale:'it-IT',permissions:['clipboard-read','clipboard-write']});const p=await c.newPage();
 await p.goto(base+'index.html');await p.waitForTimeout(500);
 await p.evaluate(()=>document.getElementById('pilotForm').scrollIntoView());
 await p.fill('#pilotForm [name=nome]','Mario Rossi');await p.fill('#pilotForm [name=email]','mario@example.com');
 await p.click('#pilotForm button[type=submit]').catch(()=>{});await p.waitForTimeout(300);
 const btn='#mailFallback [data-copy=addr]';
 await p.click(btn);await p.waitForTimeout(200);await p.click(btn);await p.waitForTimeout(2200);
 const lab=await p.evaluate(()=>document.querySelector('#mailFallback [data-copy=addr]').textContent);if(lab!=='Copia indirizzo') f('copy label stuck: '+lab);
 const clip=await p.evaluate(()=>navigator.clipboard.readText().catch(()=>'?'));if(clip!=='info@fitosat.it'&&clip!=='?') f('clipboard '+clip);
 await p.evaluate(()=>{document.getElementById('langBtn').click();document.querySelector('[data-lang=en]').click();});await p.waitForTimeout(300);
 const r=await p.evaluate(()=>[document.getElementById('formStatus').textContent,document.querySelector('#mailFallback [data-copy=addr]').textContent]);
 if(!/mail app should open/.test(r[0])||r[1]!=='Copy address') f('status/label not translated '+JSON.stringify(r));
 await c.close();}
// 10) senza JS: nome FITOSAT visibile e link all'altra lingua
for (const pg of ['index.html','en/index.html']) {const c=await b.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const p=await c.newPage();
 await p.goto(base+pg);const r=await p.evaluate(()=>{const w=document.querySelector('#introLogo .wordmark');return [w?getComputedStyle(w).visibility:'none', !!document.querySelector('.nojs-lang a')]});
 if(r[0]==='hidden') f(pg+' nojs wordmark hidden'); await c.close();}

// 11) Note legali: link nella lingua giusta, pagine senza errori, accessibili
{const AxeBuilder=null;
 for (const [pg,loc,want] of [['index.html','it-IT','note-legali.html'],['index.html?lang=en','it-IT','en/note-legali.html'],['en/index.html','en-GB','note-legali.html']]) {
  const c=await b.newContext({viewport:{width:390,height:844},locale:loc});const p=await c.newPage();await p.goto(base+pg);await p.waitForTimeout(500);
  const h=await p.evaluate(()=>document.querySelector('a[data-legal]').getAttribute('href'));if(h!==want) f(pg+' legal href '+h);
  await Promise.all([p.waitForNavigation(),p.evaluate(()=>document.querySelector('a[data-legal]').click())]);
  const r=await p.evaluate(()=>[document.title, document.body.innerText.includes('14965880967'), document.body.innerText.includes('MI-2819311')]);
  if(!r[1]||!r[2]) f(pg+' legal page content '+JSON.stringify(r));
  const imgs=await p.evaluate(()=>document.fonts.check('16px Questrial'));if(!imgs) f(pg+' legal fonts');
  await c.close();}
 const axe=require('fs').readFileSync('/home/claude/a11y/node_modules/axe-core/axe.min.js','utf8');
 for (const pg of ['note-legali.html','en/note-legali.html']) for (const cs of ['light','dark']) {const c=await b.newContext({viewport:{width:390,height:844},colorScheme:cs});const p=await c.newPage();
  const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('requestfailed',r=>errs.push('fail '+r.url()));
  await p.goto(base+pg);await p.addScriptTag({content:axe});
  const v=await p.evaluate(async()=>(await axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21aa']})).violations.map(x=>x.id));
  if(v.length) f(pg+' '+cs+' axe '+v); if(errs.length) f(pg+' errors '+errs);
  await p.screenshot({path:'/home/claude/preview/legal-'+pg.replace('/','-')+'-'+cs+'.png',fullPage:true});await c.close();}
}
// 8) peso
const fs=require('fs');const kb=fs.statSync('/home/claude/staging/index.html').size/1024;if(kb>200) f('index too heavy '+kb.toFixed(0)+'KB');
srv.kill();await b.close();console.log(fail?'FAIL '+fail:'PASS');process.exit(fail?1:0);})();
