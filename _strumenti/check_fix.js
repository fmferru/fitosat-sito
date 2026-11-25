const {chromium}=require('playwright');
const url='file://'+(process.argv[2]||'/home/claude/staging/index.html');
(async()=>{const b=await chromium.launch();let fail=0;
const p=await b.newPage({viewport:{width:1440,height:900}});await p.goto(url);await p.waitForTimeout(400);
await p.setViewportSize({width:1440,height:650});await p.waitForTimeout(500);
await p.evaluate(()=>window.scrollTo(0,Math.round(0.29*1.4*650)));await p.waitForTimeout(1300);
const d=await p.evaluate(()=>{const a=document.querySelector('#introLogo .wordmark').getBoundingClientRect();const bb=document.querySelector('#brandBar svg').getBoundingClientRect();return Math.abs((a.top+a.height/2)-(bb.top+bb.height/2))});
if(d>8){console.log('FAIL resize-height handoff miss',d);fail++;}
const p2=await b.newPage({viewport:{width:1440,height:900}});await p2.goto(url);await p2.waitForTimeout(400);
for(let i=0;i<4;i++){await p2.keyboard.press('Tab');const r=await p2.evaluate(()=>{const e=document.activeElement;return {id:e.id,op:+getComputedStyle(e).opacity}});if(r.id==='brandBar'&&r.op<0.5){console.log('FAIL invisible brandBar focused');fail++;}}
await b.close();console.log(fail?'FAIL '+fail:'PASS');process.exit(fail?1:0);})();
