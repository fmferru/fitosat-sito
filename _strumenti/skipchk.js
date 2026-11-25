const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844}});
await p.goto('file:///home/claude/staging/index.html');await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelector('.pilotbox').scrollIntoView());await p.waitForTimeout(800);
console.log(await p.evaluate(()=>{const r=document.querySelector('.skip').getBoundingClientRect();return [r.top,r.bottom, document.activeElement.className]}));
await b.close();})();
