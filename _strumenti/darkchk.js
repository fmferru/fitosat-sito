const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844},colorScheme:'dark'});
await p.goto('file:///home/claude/staging/index.html');await p.waitForTimeout(400);
const r=await p.evaluate(()=>[...document.querySelectorAll('*')].filter(e=>{const c=getComputedStyle(e);return c.backgroundColor==='rgb(224, 180, 200)'||c.backgroundImage.includes('224, 180, 200')}).map(e=>e.tagName+'.'+e.className+' color='+getComputedStyle(e).color+' "'+(e.textContent||'').trim().slice(0,20)+'"'));
console.log(r.join('\n'));await b.close();})();
