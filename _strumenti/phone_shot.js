const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
for (const [n,vp,url] of [['m',{width:390,height:844},'index.html'],['d',{width:1280,height:800},'index.html'],['en',{width:390,height:844},'en/index.html'],['dark',{width:390,height:844},'index.html']]){
const p=await b.newPage({viewport:vp,deviceScaleFactor:2,locale:'it-IT',colorScheme:n==='dark'?'dark':'light'});
await p.goto('file:///home/claude/staging/'+url);await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelector('section.whatis').scrollIntoView());await p.waitForTimeout(150);
await p.evaluate(()=>document.getElementById('phone').scrollIntoView({block:'center'}));await p.waitForTimeout(2400);
await p.evaluate(()=>document.querySelector('section.whatis').scrollIntoView());await p.waitForTimeout(300);
await (await p.$('section.whatis')).screenshot({path:`/home/claude/preview/phone-${n}.png`});}
await b.close();})();
