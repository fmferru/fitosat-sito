const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const [n,w,h,sc] of [['m',390,844,2],['d',1440,900,1]]){const c=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:sc,locale:'it-IT'});const p=await c.newPage();
await p.goto('file:///home/claude/staging/index.html');await p.waitForTimeout(400);
const fr=[0,0.4,0.65,1.0];for(let i=0;i<fr.length;i++){await p.evaluate(y=>window.scrollTo(0,y),Math.round(fr[i]*1.4*h));await p.waitForTimeout(1200);await p.screenshot({path:`/home/claude/build/pv_${n}_${i}.png`});}
const y=await p.evaluate(()=>document.getElementById('funziona').offsetTop+200);await p.evaluate(y=>window.scrollTo(0,y),y);await p.waitForTimeout(900);await p.screenshot({path:`/home/claude/build/pv_${n}_4.png`});
await c.close();}await b.close();})();
