const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
for (const [tag,f] of [['after','index.html']]){
const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2,locale:'it-IT'});
await p.goto('file:///home/claude/staging/'+f);await p.waitForTimeout(400);
const H=await p.evaluate(()=>document.body.scrollHeight);
for(let y=0;y<H;y+=400){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(50);}
await p.waitForTimeout(1500);
const sels={team:'.team'};
for(const [k,s] of Object.entries(sels)){const el=await p.$(s);await el.scrollIntoViewIfNeeded();await p.waitForTimeout(700);await el.screenshot({path:`/home/claude/preview/c-${tag}-${k}.png`});}
}
await b.close();})();
