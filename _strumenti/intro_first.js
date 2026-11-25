const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
for (const [n,vp] of [['m',{width:390,height:844}],['d',{width:1440,height:900}]]){
const p=await b.newPage({viewport:vp,deviceScaleFactor:2,locale:'it-IT'});
await p.goto('file:///home/claude/staging/index.html');await p.waitForTimeout(2600);
await p.screenshot({path:`/home/claude/preview/intro-${n}.png`});
await p.evaluate(()=>scrollTo(0,innerHeight*0.45));await p.waitForTimeout(1200);
await p.screenshot({path:`/home/claude/preview/intro-${n}-2.png`});}
await b.close();})();
