const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();for(const [w,h] of [[390,844],[1440,900]]){const p=await b.newPage({viewport:{width:w,height:h}});
await p.goto('file:///home/claude/staging/index.html');await p.waitForTimeout(400);
const z=[0.27,0.29,0.31,0.33];for(let i=0;i<z.length;i++){await p.evaluate(y=>window.scrollTo(0,y),Math.round(z[i]*1.4*h));await p.waitForTimeout(1200);
await p.screenshot({path:`/home/claude/build/h_${w}_${i}.png`,clip:{x:w/2-160,y:0,width:320,height:80}});}
await p.close();}await b.close();})();
