import json,re
P='/home/claude/staging/index.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,c=1):
    global s
    assert s.count(o)==c,(s.count(o),o[:90]); s=s.replace(o,n)
# ---- skip link
rep('<body>\n','<body>\n<a class="skip" href="#progetto">Vai al contenuto</a>\n')
# ---- privacy link near form + footer
rep('class="privacy full">Usiamo questi dati solo per risponderti. Non li cediamo a terzi.</p>',
    'class="privacy full">Usiamo questi dati solo per risponderti. Non li cediamo a terzi. <a href="privacy.html">Informativa privacy</a></p>')
rep('''    <!-- Dopo l'iscrizione al Registro delle Imprese: sostituire la riga sotto con P.IVA, numero REA, capitale sociale versato e PEC. -->
    <p>© 2026 Fitosat srl</p>
    <p>Partita IVA e numero REA in fase di attribuzione</p>''','''    <!-- Dopo l'iscrizione al Registro delle Imprese: sostituire la riga sotto con P.IVA, numero REA, capitale sociale versato e PEC. -->
    <p>© 2026 Fitosat srl · Sede legale: Via Lanzone 5, 20123 Milano (MI)</p>
    <p>Partita IVA e numero REA in fase di attribuzione</p>''')
rep('<p class="foot-links"><a href="mailto:info@fitosat.it">info@fitosat.it</a>','<p class="foot-links"><a href="mailto:info@fitosat.it">info@fitosat.it</a><a href="privacy.html">Privacy</a>')
# ---- stagger lists
s=s.replace('<ul class="stats">','<ul class="stats stagger">')
rep('<ul class="vine-uses">','<ul class="vine-uses stagger">')
# ---- fruit items focusable
for q in range(4):
    rep(f'<li data-q="{q}">',f'<li data-q="{q}" tabindex="0">')
css='''
  /* Accessibilità e movimento (22/11) */
  .skip { position: fixed; z-index: 100; left: 50%; top: .5rem; transform: translate(-50%, -160%); background: var(--ink); color: var(--bg); padding: .7rem 1.1rem; border-radius: 10px; font-weight: 700; text-decoration: none; transition: transform .2s; }
  .skip:focus { transform: translate(-50%, 0); outline: 3px solid var(--brand); outline-offset: 2px; }
  .compare:has(#slider:focus-visible) .handle { width: 5px; margin-left: -2.5px; box-shadow: 0 0 0 3px var(--brand), 0 0 0 6px #fff; }
  .compare:has(#slider:focus-visible) { outline: 3px solid var(--brand); outline-offset: 3px; }
  .switch input:focus-visible + .track { outline: 3px solid var(--brand); outline-offset: 3px; }
  .fruit-text li:focus { outline: none; }
  .fruit-text li:focus-visible h3 { outline: 3px solid var(--brand); outline-offset: 4px; border-radius: 6px; }
  .privacy a { color: inherit; text-decoration: underline; }
  [tabindex="-1"]:focus { outline: none; }
  .brandbar { transition: background-color .3s, color .3s, border-color .3s; }
  .js-anim .stagger > li { opacity: 0; transform: translateY(16px); transition: opacity .55s ease, transform .55s cubic-bezier(.2,.7,.2,1); }
  .js-anim .stagger.in > li { opacity: 1; transform: none; }
  .js-anim .stagger.in > li:nth-child(2) { transition-delay: .09s; }
  .js-anim .stagger.in > li:nth-child(3) { transition-delay: .18s; }
  .js-anim .stagger.in > li:nth-child(4) { transition-delay: .27s; }
  .js-anim .stagger.in > li:nth-child(5) { transition-delay: .36s; }
  .js-anim .stagger.in > li:nth-child(6) { transition-delay: .45s; }
'''
rep('</style>',css+'</style>')
# ---- JS: fruit keyboard
rep('''      li.addEventListener("mouseenter", function () { paused = true; i = k; show(k); });''','''      li.addEventListener("mouseenter", function () { paused = true; i = k; show(k); });
      li.addEventListener("focus", function () { paused = true; i = k; show(k); });
      li.addEventListener("blur", function () { paused = false; });''')
# ---- JS: focus target after menu/skip jump
rep('''      if (history.replaceState) history.replaceState(null, "", "#" + id);''','''      if (history.replaceState) history.replaceState(null, "", "#" + id);
      if (!target.hasAttribute("tabindex")) target.setAttribute("tabindex", "-1");
      try { target.focus({ preventScroll: true }); } catch (e) {}''')
# ---- JS: stagger + count-up
js='''
  /* Comparsa a cascata e numeri che salgono */
  (function () {
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce || !("IntersectionObserver" in window)) return;
    document.documentElement.classList.add("js-anim");
    var running = [];
    langHooks.push(function () { running.forEach(function (r) { r.cancel = true; }); });
    function countUp(node) {
      var full = node.nodeValue, m = full.match(/\\d[\\d.,]*/);
      if (!m) return;
      var raw = m[0], grp = lang === "en" ? "," : ".", dec = lang === "en" ? "." : ",";
      var parts = raw.split(dec), intPart = parts[0].split(grp).join(""), frac = parts[1] || "";
      var target = parseFloat(intPart + (frac ? "." + frac : "")), decimals = frac.length;
      if (!isFinite(target)) return;
      var job = { cancel: false }; running.push(job);
      var t0 = null, dur = 1300;
      function fmt(v) {
        var str = v.toFixed(decimals).split("."), ip = str[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, intPart.length > 3 || raw.indexOf(grp) >= 0 ? grp : "");
        return ip + (decimals ? dec + str[1] : "");
      }
      function step(ts) {
        if (job.cancel) return;
        if (t0 === null) t0 = ts;
        var p = Math.min(1, (ts - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        node.nodeValue = p < 1 ? full.replace(raw, fmt(target * e)) : full;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        if (!x.isIntersecting) return;
        var el = x.target; io.unobserve(el); el.classList.add("in");
        el.querySelectorAll(".num").forEach(function (n) {
          var tn = null; n.childNodes.forEach(function (c) { if (c.nodeType === 3 && /\\d/.test(c.nodeValue)) tn = c; });
          if (tn) countUp(tn);
        });
      });
    }, { threshold: 0.25 });
    document.querySelectorAll(".stagger").forEach(function (el) { io.observe(el); });
  })();

  /* Lingua: interruttore IT / EN */'''
rep('\n  /* Lingua: interruttore IT / EN */',js)
# ---- EN dictionary
a=s.index('var EN = ')+9; b=s.index('};',a)+1; EN=json.loads(s[a:b])
EN.update({"Vai al contenuto":"Skip to content","Informativa privacy":"Privacy notice","Privacy":"Privacy",
 "© 2026 Fitosat srl · Sede legale: Via Lanzone 5, 20123 Milano (MI)":"© 2026 Fitosat srl · Registered office: Via Lanzone 5, 20123 Milan (MI), Italy"})
s=s[:a]+json.dumps(EN,ensure_ascii=False)+s[b:]
open(P,'w',encoding='utf-8').write(s)
print('ok')
