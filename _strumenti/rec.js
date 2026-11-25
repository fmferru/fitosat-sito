const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:'it-IT',recordVideo:{dir:'/home/claude/build/vid',size:{width:390,height:844}}});
const p=await c.newPage();await p.goto('file:///home/claude/staging/index.html');await p.waitForTimeout(2600);
const H=Math.round(1.45*844);for(let y=0;y<=H;y+=6){await p.mouse.wheel(0,6);await p.waitForTimeout(16);} await p.waitForTimeout(1500);
await c.close();await b.close();})();
