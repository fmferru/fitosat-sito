const {chromium}=require('playwright');
const url='file://'+(process.argv[2]||'/home/claude/staging/index.html');
(async()=>{const b=await chromium.launch();let fail=0;const f=(m)=>{console.log('FAIL',m);fail++;};
for (const vp of [{width:390,height:844},{width:1440,height:900},{width:375,height:667},{width:1366,height:768}]){
  const c=await b.newContext({viewport:vp});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto(url);await p.waitForTimeout(400);
  const L=async()=>p.evaluate(()=>{const ls=[...document.querySelectorAll('.intro-layer')].map(e=>+getComputedStyle(e).opacity);const s=document.getElementById('slogan');const r=s.querySelector('h1').getBoundingClientRect();const cta=s.querySelector('.intro-cta').getBoundingClientRect();return {ls,so:+getComputedStyle(s).opacity,top:r.top,bot:cta.bottom}});
  const go=async y=>{await p.evaluate(y=>window.scrollTo(0,y),y);await p.waitForTimeout(1100);};
  let r=await L(); if(r.ls.length!==2) {f(vp.width+' layers '+r.ls.length);} else if(!(r.ls[0]>0.9)) f(vp.width+' start layer0 '+r.ls);
  await go(Math.round(0.5*1.4*vp.height)); r=await L(); if(!(r.ls[1]>0.5)) f(vp.width+' mid rows '+r.ls);
  await go(Math.round(1.4*vp.height)); r=await L();
  if(!(r.ls[1]>0.9)) f(vp.width+' end rows '+r.ls); if(!(r.so>0.9)) f(vp.width+' slogan op '+r.so);
  if(!(r.top>=0.5*vp.height-2)) f(vp.width+'x'+vp.height+' slogan top '+r.top); if(!(r.bot<=vp.height)) f(vp.width+'x'+vp.height+' cta bottom '+r.bot);
  if(errs.length) f('errors '+errs);
  await c.close();}
const c=await b.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});const p=await c.newPage();await p.goto(url);await p.waitForTimeout(400);
const st=await p.evaluate(()=>({s:document.getElementById('intro').classList.contains('static'),l2:+getComputedStyle(document.querySelectorAll('.intro-layer')[1]||document.body).opacity}));
if(!st.s||!(st.l2>0.9)) f('reduced motion '+JSON.stringify(st));
await b.close();console.log(fail?'FAIL '+fail:'PASS');process.exit(fail?1:0);})();
