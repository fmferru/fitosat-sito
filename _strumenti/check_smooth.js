const {chromium}=require('playwright');
const url='file://'+(process.argv[2]||'/home/claude/staging/index.html');
(async()=>{const b=await chromium.launch();let fail=0;const f=m=>{console.log('FAIL',m);fail++;};
const p=await b.newPage({viewport:{width:390,height:844}});await p.goto(url);await p.waitForTimeout(500);
let prev=null;const N=36;
for(let i=0;i<=N;i++){const y=Math.round(i/N*1.4*844);await p.evaluate(y=>window.scrollTo(0,y),y);await p.waitForTimeout(450);
 const st=await p.evaluate(()=>[...document.querySelectorAll('.intro-layer')].map(e=>{const m=new DOMMatrix(getComputedStyle(e).transform);return {o:+getComputedStyle(e).opacity,s:m.a}}));
 const vis=st.map(x=>x.o);
 // coverage: the top-most visible layers must cover (no see-through to black): 1-prod(1-o) >= .95
 const cov=1-vis.reduce((a,o)=>a*(1-o),1); if(cov<0.95) f(`y=${y} coverage ${cov.toFixed(2)}`);
 if(prev){st.forEach((x,k)=>{if(x.o>0.02&&prev[k].o>0.02&&x.s<prev[k].s-0.001) f(`layer ${k} zooms out at y=${y}`);
   const d=Math.abs(x.o-prev[k].o); if(d>0.35) f(`layer ${k} opacity jump ${d.toFixed(2)} at y=${y}`);});}
 prev=st;}
await b.close();console.log(fail?'FAIL '+fail:'PASS');process.exit(fail?1:0);})();
