const {chromium}=require('playwright');
const url='file://'+(process.argv[2]||'/home/claude/staging/index.html');
function lum(c){const a=c.map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*a[0]+.7152*a[1]+.0722*a[2];}
(async()=>{const b=await chromium.launch();let fail=0;const f=m=>{console.log('FAIL',m);fail++;};
for (const [w,h,cs] of [[320,568,'light'],[390,844,'light'],[1440,900,'light'],[390,844,'dark']]){
  const c=await b.newContext({viewport:{width:w,height:h},colorScheme:cs});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto(url);await p.waitForTimeout(400);
  const H=await p.evaluate(()=>document.documentElement.scrollHeight);
  const pos=[['mid',Math.round(0.7*h)],['end',Math.round(1.4*h)],['page',Math.round(H/2)],['bottom',H]];
  const probe=async(tag)=>{const r=await p.evaluate(()=>{const g=id=>{const e=document.getElementById(id);return e?e.getBoundingClientRect():null};
      const bb=document.getElementById('brandBar');if(!bb)return null;const cs=getComputedStyle(bb);
      return {bb:g('brandBar'),lang:g('langBtn'),menu:g('menuBtn'),op:+cs.opacity,tucked:document.getElementById('topnav').classList.contains('tucked'),color:cs.color,bg:cs.backgroundColor,body:getComputedStyle(document.body).backgroundColor,light:bb.classList.contains('light')}});
    if(!r){f(`${w} ${tag} no #brandBar`);return;}
    const cx=r.bb.left+r.bb.width/2, cy=r.bb.top+r.bb.height/2, my=r.menu.top+r.menu.height/2;
    if(r.op<0.9) f(`${w}${cs} ${tag} opacity ${r.op}`);
    if(Math.abs(cx-w/2)>4) f(`${w} ${tag} not centred ${cx}`);
    if(Math.abs(cy-my)>4) f(`${w} ${tag} not aligned ${cy} vs ${my}`);
    const ov=(a,b2)=>a.left<b2.right&&a.right>b2.left&&a.top<b2.bottom&&a.bottom>b2.top;
    if(ov(r.bb,r.lang)||ov(r.bb,r.menu)) f(`${w} ${tag} overlaps buttons`);
    if(r.tucked) f(`${w} ${tag} topnav tucked`);
    if(r.light){const P=s=>s.match(/[\d.]+/g).map(Number);const fg=P(r.color),bg=P(r.bg),bd=P(r.body);const a=bg[3]===undefined?1:bg[3];
      const mix=[0,1,2].map(i=>bg[i]*a+bd[i]*(1-a));const L1=lum(fg),L2=lum(mix);const ratio=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
      if(ratio<4.5) f(`${w}${cs} ${tag} contrast ${ratio.toFixed(2)}`);}
  };
  for(const [tag,y] of pos){await p.evaluate(y=>window.scrollTo(0,y),y);await p.waitForTimeout(1100);await p.evaluate(()=>window.scrollBy(0,-1));await p.waitForTimeout(300);await probe(tag);}
  await p.evaluate(()=>window.scrollTo(0,0));await p.waitForTimeout(800);
  await p.click('#menuBtn');await p.waitForTimeout(200);await p.click('#topnav a[data-go="contatti"]');await p.waitForTimeout(1600);await probe('menu-contatti');
  if(errs.length) f('errors '+errs);
  await c.close();}
await b.close();console.log(fail?'FAIL '+fail:'PASS');process.exit(fail?1:0);})();
