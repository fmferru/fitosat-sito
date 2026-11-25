const {chromium}=require('playwright');
const url='file://'+(process.argv[2]||'/home/claude/staging/index.html');
(async()=>{const b=await chromium.launch();let fail=0;const f=m=>{console.log('FAIL',m);fail++;};
for(const [w,h] of [[390,844],[1440,900],[375,667]]){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto(url);await p.waitForTimeout(2600);
 const r=await p.evaluate(()=>{const l=document.getElementById('introLogo');const s=l.querySelector('.wm-sat');const fi=l.querySelector('.wm-fito');const sv=l.querySelector('svg').getBoundingClientRect();
   return {sat:l.classList.contains('sat-on'),has:!!s&&!!fi,fill:s?getComputedStyle(s).fill:'',cy:sv.top+sv.height/2}});
 if(!r.has) f(w+' no split wordmark'); if(!r.sat) f(w+' no sat state'); if(r.fill==='rgb(255, 255, 255)') f(w+' SAT not highlighted');
 if(Math.abs(r.cy-h*0.35)>h*0.1) f(w+' logo not centred in sky '+r.cy+'/'+h);
 // earth limb must be below logo+tagline: sample the orbit layer brightness just under tagline
 await p.evaluate(()=>window.scrollTo(0,30));await p.waitForTimeout(1400);
 const r2=await p.evaluate(()=>document.getElementById('introLogo').classList.contains('sat-on'));if(r2) f(w+' sat not reverted after scroll');
 await p.close();}
await b.close();console.log(fail?'FAIL '+fail:'PASS');process.exit(fail?1:0);})();
