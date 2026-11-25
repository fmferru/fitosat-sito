const {chromium}=require('playwright');const fs=require('fs');
const axe=fs.readFileSync('/home/claude/a11y/node_modules/axe-core/axe.min.js','utf8');
(async()=>{const b=await chromium.launch();let fail=0;const f=m=>{console.log('FAIL',m);fail++;};
for(const [f0,lng] of [['index.html','it'],['en/index.html','en']]){
 const p=await b.newPage({viewport:{width:1440,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/staging/'+f0);await p.waitForTimeout(600);
 // original numbers
 const orig=await p.evaluate(()=>[...document.querySelectorAll('.stats .num')].map(n=>n.textContent));
 // scroll through
 const H=await p.evaluate(()=>document.documentElement.scrollHeight);
 for(let y=0;y<H;y+=500){await p.evaluate(y=>window.scrollTo(0,y),y);await p.waitForTimeout(120);}
 await p.waitForTimeout(1800);
 const after=await p.evaluate(()=>[...document.querySelectorAll('.stats .num')].map(n=>n.textContent));
 if(JSON.stringify(orig)!==JSON.stringify(after)) f(lng+' numbers differ '+JSON.stringify([orig,after]));
 const hidden=await p.evaluate(()=>[...document.querySelectorAll('.stagger > li')].filter(l=>+getComputedStyle(l).opacity<0.99).length);
 if(hidden) f(lng+' stagger items still hidden '+hidden);
 await p.addScriptTag({content:axe});
 const v=await p.evaluate(async()=>(await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}})).violations.map(x=>x.id+':'+x.nodes.length));
 if(v.length) f(lng+' axe '+v);
 // skip link first tab
 await p.evaluate(()=>window.scrollTo(0,0));await p.waitForTimeout(300);await p.keyboard.press('Tab');await p.waitForTimeout(350);
 const sk=await p.evaluate(()=>{const e=document.activeElement;const r=e.getBoundingClientRect();return [e.className,r.top>=0&&r.bottom<=innerHeight]});
 if(sk[0]!=='skip'||!sk[1]) f(lng+' skip link '+sk);
 await p.keyboard.press('Enter');await p.waitForTimeout(1500);
 const fid=await p.evaluate(()=>document.activeElement.id);if(fid!=='progetto') f(lng+' skip focus '+fid);
 // focus rings
 await p.focus('#slider');await p.keyboard.press('ArrowRight');const ring=await p.evaluate(()=>getComputedStyle(document.getElementById('compare')).outlineStyle);if(ring==='none') f(lng+' slider ring');
 await p.focus('#segToggle');await p.keyboard.press('Shift+Tab');await p.keyboard.press('Tab');const tr=await p.evaluate(()=>getComputedStyle(document.querySelector('.switch .track')).outlineStyle);if(tr==='none') f(lng+' toggle ring');
 // fruit keyboard
 await p.evaluate(()=>document.getElementById('phone').scrollIntoView({block:'center'}));await p.waitForTimeout(2300);const ph=await p.evaluate(()=>{const e=document.getElementById('phone');return e.classList.contains('in')&&getComputedStyle(e.querySelector('.phone-note')).opacity==='1'&&getComputedStyle(e.querySelector('.mk-r')).opacity});if(ph!=='1') f(lng+' phone reveal '+ph);
 // privacy links
 const pl=await p.evaluate(()=>[...document.querySelectorAll('a[data-privacy]')].map(a=>a.textContent));if(pl.length<2) f(lng+' privacy links '+pl);
 if(errs.length) f(lng+' errors '+errs);
 await p.close();}
for(const pp of ['privacy.html','en/privacy.html']){const p=await b.newPage();await p.goto('file:///home/claude/staging/'+pp);await p.addScriptTag({content:axe});
 const v=await p.evaluate(async()=>(await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}})).violations.map(x=>x.id));if(v.length) f(pp+' axe '+v);await p.close();}
await b.close();console.log(fail?'FAIL '+fail:'PASS');process.exit(fail?1:0);})();
