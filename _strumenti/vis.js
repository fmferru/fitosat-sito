// screenshots at fixed states for visual comparison: node vis.js <html> <outprefix>
const {chromium}=require('playwright');const [,,f,out]=process.argv;
(async()=>{const b=await chromium.launch();let n=0;
for(const [w,h,cs] of [[390,844,'light'],[1440,900,'light'],[390,844,'dark']]){
 const c=await b.newContext({viewport:{width:w,height:h},colorScheme:cs,reducedMotion:'no-preference'});const p=await c.newPage();
 await p.goto('file://'+f);await p.waitForTimeout(2700);
 const H=await p.evaluate(()=>document.documentElement.scrollHeight);
 const ys=[0,Math.round(.5*1.4*h),Math.round(1.4*h)];for(let y=Math.round(1.4*h)+h;y<H;y+=h)ys.push(y);
 for(const y of ys){await p.evaluate(y=>window.scrollTo(0,y),y);await p.waitForTimeout(y===0?200:1300);
  await p.evaluate(()=>document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in')));await p.waitForTimeout(150);
  await p.screenshot({path:`${out}_${String(n++).padStart(3,'0')}.png`});}
 await c.close();}
await b.close();console.log('shots',n);})();
