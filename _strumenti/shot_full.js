const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const out=process.argv[2]||'/home/claude/preview/before';
for (const [n,vp] of [['m',{width:390,height:844}],['d',{width:1440,height:900}]]){
const p=await b.newPage({viewport:vp,deviceScaleFactor:1});
await p.goto('file:///home/claude/staging/index.html');await p.waitForTimeout(500);
const H=await p.evaluate(()=>document.body.scrollHeight);
for(let y=0;y<H;y+=400){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(60);}
await p.waitForTimeout(1500);
// screenshot content after intro
const introH=await p.evaluate(()=>document.querySelector('.intro').offsetHeight);
await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(300);
await p.screenshot({path:`${out}-${n}.png`,fullPage:true});
}
await b.close();})();
