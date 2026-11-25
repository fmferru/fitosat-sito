import sys
for path in ['/home/claude/staging/index.html','/home/claude/staging/en/index.html']:
    s=open(path,encoding='utf-8').read()
    def rep(o,n):
        global s
        assert s.count(o)==1,(path,o[:60]); s=s.replace(o,n)
    rep('<ul id="navList">','<button class="menubtn" id="menuBtn" type="button" aria-expanded="false" aria-controls="navList" aria-label="Menu"><span></span><span></span><span></span></button>\n  <ul id="navList">')
    css='''
  /* Menu a tre stanghette */
  .topnav, .topnav.light { left: auto; right: 1rem; }
  .menubtn { width: 2.75rem; height: 2.75rem; display: inline-flex; flex-direction: column; align-items: center; justify-content: center; gap: 5px; padding: 0; cursor: pointer;
    border-radius: 999px; background: rgba(30,20,24,.55); -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,.16); box-shadow: 0 4px 14px -8px rgba(0,0,0,.35); color: #f7eef0; margin-left: auto; }
  .menubtn span { display: block; width: 20px; height: 2px; border-radius: 2px; background: currentColor; transition: transform .25s ease, opacity .2s; }
  .topnav.open .menubtn span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
  .topnav.open .menubtn span:nth-child(2) { opacity: 0; }
  .topnav.open .menubtn span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
  .topnav.light .menubtn { color: var(--ink); background: rgba(255,255,255,.88); border-color: rgba(58,38,48,.14); }
  @media (prefers-color-scheme: dark) { .topnav.light .menubtn { background: rgba(38,27,31,.7); border-color: rgba(255,255,255,.08); } }
  .topnav { display: flex; flex-direction: column; align-items: flex-end; }
  .topnav ul, .topnav.light ul { display: none; position: absolute; top: calc(100% + .5rem); right: 0; min-width: 14rem; flex-direction: column; align-items: stretch; gap: .2rem;
    padding: .45rem; border-radius: 16px; background: var(--surface); border: 1px solid var(--line); box-shadow: var(--shadow-lg); grid-template-columns: none; }
  .topnav.open ul { display: flex; animation: menuIn .2s ease both; }
  @keyframes menuIn { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
  .topnav a, .topnav.light a { color: var(--ink); font-size: 1rem; text-align: left; justify-content: flex-start; min-height: 2.75rem; padding: .7rem 1rem .55rem; border-radius: 10px; display: flex; align-items: center; }
  .topnav a:hover, .topnav.light a:hover { background: var(--brand-soft); color: var(--ink); }
  .topnav a[aria-current="true"], .topnav.light a[aria-current="true"] { background: var(--brand-soft); color: var(--brand); }
  .topnav a.cta, .topnav.light a.cta { color: #fff; margin: .25rem 0 0; justify-content: center; border-radius: 3px 18px 3px 18px; padding: .7rem 1rem .55rem; }
  @media (max-width: 760px) {
    .topnav, .topnav.light { left: auto; right: .5rem; top: .45rem; }
    .topnav ul { min-width: min(16rem, calc(100vw - 1rem)); }
  }
  @media (prefers-reduced-motion: reduce) { .topnav.open ul { animation: none; } .menubtn span { transition: none; } }
'''
    rep('</style>', css+'</style>')
    rep('      if (!jumping && pastIntro && y > lastY + 4) navEl.classList.add("tucked");',
        '      if (!jumping && pastIntro && y > lastY + 4 && !navEl.classList.contains("open")) navEl.classList.add("tucked");')
    js='''
  /* Menu a tre stanghette: apri e chiudi */
  (function () {
    var nav = document.getElementById("topnav"), btn = document.getElementById("menuBtn");
    if (!nav || !btn) return;
    function set(open) { nav.classList.toggle("open", open); btn.setAttribute("aria-expanded", open ? "true" : "false"); }
    btn.addEventListener("click", function (e) { e.stopPropagation(); var o = !nav.classList.contains("open"); set(o); if (o) { var f = nav.querySelector("ul a"); if (f) f.focus(); } });
    nav.querySelectorAll("ul a").forEach(function (a) { a.addEventListener("click", function () { set(false); }); });
    document.addEventListener("click", function (e) { if (!e.target.closest("#topnav")) set(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("open")) { set(false); btn.focus(); } });
  })();

  /* Lingua: interruttore IT / EN */'''
    rep('\n  /* Lingua: interruttore IT / EN */', js)
    open(path,'w',encoding='utf-8').write(s)
print('ok')
