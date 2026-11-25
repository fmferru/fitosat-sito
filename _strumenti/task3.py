import re
P='/home/claude/staging/index.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,c=1):
    global s
    assert s.count(o)==c,(s.count(o),o[:90]); s=s.replace(o,n)
wm=re.search(r'<path class="wordmark" d="([^"]+)"',s).group(1)
rep('<nav class="topnav" id="topnav"','<a class="brandbar" id="brandBar" href="#top" aria-label="Fitosat"><svg viewBox="48 10 306 58" aria-hidden="true"><path d="'+wm+'"/></svg></a>\n<nav class="topnav" id="topnav"')
css='''
  /* Scritta FITOSAT sempre al centro della barra */
  .brandbar { position: fixed; z-index: 51; left: 50%; top: calc(.9rem + 1.375rem); transform: translate(-50%, -50%); display: block; padding: .62rem 1.05rem; border-radius: 999px;
    color: #fff; border: 1px solid transparent; opacity: 0; pointer-events: none; transition: opacity .25s ease, background-color .3s, color .3s, border-color .3s; }
  .brandbar.on { opacity: 1; pointer-events: auto; }
  .brandbar svg { display: block; height: 22px; width: auto; fill: currentColor; filter: drop-shadow(0 1px 6px rgba(0,0,0,.45)); }
  .brandbar.light { color: var(--ink); background: rgba(255,255,255,.88); border-color: rgba(58,38,48,.14); -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); box-shadow: 0 4px 14px -8px rgba(0,0,0,.35); }
  .brandbar.light svg { filter: none; }
  @media (prefers-color-scheme: dark) { .brandbar.light { background: rgba(38,27,31,.85); border-color: rgba(255,255,255,.08); } }
  @media (max-width: 760px) { .brandbar { top: calc(.45rem + 1.375rem); padding: .6rem .8rem; } }
  @media (max-width: 400px) { .brandbar svg { height: 19px; } .brandbar { padding: .55rem .65rem; } }
  .topnav.tucked, .langnav.tucked { transform: none; opacity: 1; pointer-events: auto; }
  .intro.static .intro-logo .wordmark { visibility: hidden; }
'''
rep('</style>',css+'</style>')
# --- measure: compute handoff geometry ---
rep('''    logoTarget = (nb && nb.left < rect.right && nb.right > rect.left) ? Math.round(nb.bottom + 14) : 28;
    logoTop = rect.top;''','''    logoTarget = (nb && nb.left < rect.right && nb.right > rect.left) ? Math.round(nb.bottom + 14) : 28;
    logoTop = rect.top;
    var wmR = logoEl.querySelector(".wordmark").getBoundingClientRect();
    brand.classList.add("on"); var bR = brand.querySelector("svg").getBoundingClientRect(); brand.classList.remove("on");
    handS = bR.height / wmR.height;
    var wmCy = wmR.top + wmR.height / 2;
    handTy = (bR.top + bR.height / 2) - rect.top - (wmCy - rect.top) * handS;''')
rep('  var logoTarget = 28;','  var logoTarget = 28, handS = 0.6, handTy = 0;\n  var brand = document.getElementById("brandBar");\n  var symbolEls = Array.prototype.slice.call(logoEl.querySelectorAll("image, .tagline"));')
rep('''    logoEl.style.transform = "translate3d(0," + (-p * Math.max(0, logoTop - logoTarget)).toFixed(1) + "px,0) scale(" + (1 - p * 0.5).toFixed(4) + ")";''','''    var hp = seg(0, 0.3); hp = hp * hp * (3 - 2 * hp);
    logoEl.style.transform = "translate3d(0," + (hp * handTy).toFixed(1) + "px,0) scale(" + (1 + hp * (handS - 1)).toFixed(4) + ")";
    var so = (1 - seg(0, 0.2)).toFixed(3);
    symbolEls.forEach(function (e) { e.style.opacity = so; });
    var handed = z >= 0.3;
    brand.classList.toggle("on", handed);
    logoEl.style.visibility = handed ? "hidden" : "visible";''')
# remove unused p variable usage? keep p line if exists
# static (reduced motion): brand always on
rep('''    intro.classList.add("static");''','''    intro.classList.add("static");
    brand.classList.add("on");''')
# navTone: no tucking, brand tone
rep('''      if (!jumping && pastIntro && y > lastY + 4 && !navEl.classList.contains("open")) navEl.classList.add("tucked");
      if (y < lastY - 4 || !pastIntro) navEl.classList.remove("tucked");
      if (ln) ln.classList.toggle("tucked", navEl.classList.contains("tucked") && document.getElementById("langMenu").hidden);''','''      navEl.classList.remove("tucked"); if (ln) ln.classList.remove("tucked");
      var bb = document.getElementById("brandBar"); if (bb) bb.classList.toggle("light", inContent);''')
open(P,'w',encoding='utf-8').write(s)
print('ok')
