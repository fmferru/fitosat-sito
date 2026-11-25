import re, json
P='/home/claude/index_before_critique.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,count=1):
    global s
    n=s.count(old)
    assert n==count, (n, old[:80])
    s=s.replace(old,new)

# ---------- CSS ----------
css_add = r'''
  /* === Revisione: pagina continua, CTA unica, modulo, misure minime === */
  :root { --cta-a: #3f7d30; --cta-b: #2a6121; }
  .btn { background: linear-gradient(135deg, var(--cta-a), var(--cta-b)); color: #fff; border: 0; cursor: pointer;
    border-radius: 3px 22px 3px 22px; box-shadow: 0 10px 22px -12px rgba(42,97,33,.8); transition: transform .2s, filter .2s; }
  .btn:hover { filter: brightness(1.08); transform: translateY(-1px); }
  .pilotbox .btn { background: linear-gradient(135deg, var(--cta-a), var(--cta-b)); color: #fff; }
  .topnav a.cta { background: linear-gradient(135deg, var(--cta-a), var(--cta-b)); }
  .intro-cta { margin-top: 1.6rem; align-self: center; font-size: 1rem; padding: .85rem 1.4rem .7rem; }
  .intro-slogan { pointer-events: none; }
  .intro-slogan.live { pointer-events: auto; }
  .intro.static .intro-slogan { pointer-events: auto; }

  /* Misure minime dei testi: 12px etichette mono, 13px didascalie */
  .stats cite, .tag, .crop-legend, .state-legend, .chev .when, .steps .n, .flow h3::before, .langbtn, .topnav a { font-size: .8125rem; }
  .hud::after, .specs dt, .team .role, .langmenu .code { font-size: .75rem; }
  .idx { font-size: .75rem; }

  /* Menu su telefono: aree da toccare di 44px */
  @media (max-width: 760px) {
    .topnav a { font-size: .78rem; min-height: 2.75rem; padding: .3rem .2rem .2rem; }
    .langbtn { min-height: 2.75rem; min-width: 2.75rem; justify-content: center; font-size: .8125rem; }
    .group > section:first-child { padding-top: 5rem; }
  }

  /* Pilota: testo + modulo */
  .pilotbox { grid-template-columns: 1fr 1.05fr; gap: 2.5rem; align-items: start; padding: 2.25rem; }
  .pilot-form { background: var(--surface); color: var(--ink); border-radius: 14px; padding: 1.4rem 1.4rem 1.2rem; display: grid; grid-template-columns: 1fr 1fr; gap: .85rem 1rem; box-shadow: 0 18px 40px -22px rgba(0,0,0,.6); }
  .pilot-form .full { grid-column: 1 / -1; }
  .pilot-form label { display: grid; gap: .3rem; font-size: .8125rem; font-weight: 600; color: var(--muted); text-align: left; }
  .pilot-form input, .pilot-form select, .pilot-form textarea { font: inherit; font-size: 1rem; color: var(--ink); background: var(--bg); border: 1px solid var(--line); border-radius: 10px; padding: .65rem .75rem; min-height: 2.75rem; width: 100%; }
  .pilot-form textarea { min-height: 5.5rem; resize: vertical; }
  .pilot-form input:focus, .pilot-form select:focus, .pilot-form textarea:focus { outline: 2px solid var(--brand); outline-offset: 1px; border-color: var(--brand); }
  .pilot-form .hp { position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }
  .pilot-form .btn { justify-self: start; font-size: 1rem; }
  .pilot-form .privacy { margin: 0; font-size: .8125rem; color: var(--muted); line-height: 1.45; }
  .pilot-form .status { margin: 0; font-size: .95rem; font-weight: 600; color: var(--brand); min-height: 1.4em; }
  .pilot-form .status.err { color: var(--alert); }
  .pilot-form.sent > :not(.status) { display: none; }
  .pilot-form.sent .status { font-size: 1.1rem; text-align: center; padding: 2rem .5rem; }
  .pilotbox p.badge { margin-top: 1.25rem; }
  @media (max-width: 860px) {
    .pilotbox { grid-template-columns: 1fr; }
    .pilot-form { grid-template-columns: 1fr; width: 100%; }
  }
  @media (max-width: 760px) {
    .pilotbox { padding: 1.75rem 1rem; }
    .pilot-form { padding: 1.2rem 1rem; }
    .pilot-form .btn { justify-self: stretch; text-align: center; }
  }

  /* Team: monogramma */
  .team .who { display: flex; align-items: center; gap: .85rem; }
  .team .avatar { flex: none; width: 3rem; height: 3rem; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center;
    font-family: var(--display); font-weight: 700; font-size: 1.05rem; padding-top: .12em; color: #fff; background: linear-gradient(135deg, #7a3e5c, #4e2a38); }
  @media (max-width: 760px) { .team .who { flex-direction: column; gap: .5rem; } }
'''
rep("</style>", css_add + "</style>")
rep("  .group[hidden] { display: none; }\n", "")
rep("  .group { animation: groupIn .45s ease both; }\n", "")
rep("section.intro { height: 190vh;", "section.intro { height: 140vh;")

# ---------- HTML ----------
rep('''Immagini ad altissima risoluzione e intelligenza artificiale, in una mappa che ti dice dove intervenire.</p>
      </div>''', '''Immagini ad altissima risoluzione e intelligenza artificiale, in una mappa che ti dice dove intervenire.</p>
        <a class="btn intro-cta" href="#pilota" data-go="contatti">Partecipa al programma pilota</a>
      </div>''')
for g in ['funziona','applicazioni','contatti']:
    rep(f'data-group="{g}" hidden>', f'data-group="{g}">')

form = '''<form class="pilot-form" id="pilotForm" action="/contatto.php" method="post" novalidate>
          <label>Nome e cognome<input name="nome" autocomplete="name" required maxlength="120"></label>
          <label>Email<input name="email" type="email" autocomplete="email" required maxlength="160"></label>
          <label>Azienda<input name="azienda" autocomplete="organization" maxlength="160"></label>
          <label>Coltura<select name="coltura"><option value="">Seleziona</option><option>Vite</option><option>Olivo</option><option>Nocciolo</option><option>Caffè</option><option>Verde urbano</option><option>Altro</option></select></label>
          <label class="full">Ettari (circa)<input name="ettari" inputmode="decimal" maxlength="20"></label>
          <label class="full">Messaggio (facoltativo)<textarea name="messaggio" maxlength="3000"></textarea></label>
          <label class="hp" aria-hidden="true">Sito<input name="sito" tabindex="-1" autocomplete="off"></label>
          <p class="privacy full">Usiamo questi dati solo per risponderti. Non li cediamo a terzi.</p>
          <button class="btn full" type="submit">Invia la richiesta</button>
          <p class="status full" id="formStatus" role="status" aria-live="polite"></p>
        </form>'''
rep('''        <a class="btn" href="mailto:info@fitosat.it?subject=Programma%20pilota%20Fitosat">Partecipa al programma pilota</a>''', "        " + form)
rep('<div class="pilotbox">', '<div class="pilotbox" id="pilota">')
rep('<p class="who"><strong>Filippo Ferrucci</strong>', '<p class="who"><span class="avatar" aria-hidden="true">FF</span><span><strong>Filippo Ferrucci</strong>')
rep('<span class="role">Fondatore e CEO</span></p>', '<span class="role">Fondatore e CEO</span></span></p>')
rep('<p class="who"><strong>Lorenzo Gavazzeni</strong>', '<p class="who"><span class="avatar" aria-hidden="true">LG</span><span><strong>Lorenzo Gavazzeni</strong>')
rep('<span class="role">CTO</span></p>', '<span class="role">CTO</span></span></p>')
# hreflang
rep('<link rel="canonical" href="https://www.fitosat.it/">', '<link rel="canonical" href="https://www.fitosat.it/">\n<link rel="alternate" hreflang="it" href="https://www.fitosat.it/">\n<link rel="alternate" hreflang="en" href="https://www.fitosat.it/en/">\n<link rel="alternate" hreflang="x-default" href="https://www.fitosat.it/">')

# ---------- JS ----------
# intro timings
rep('var p = Math.min(1, y / (vh * 0.4));', 'var p = Math.min(1, y / (vh * 0.22));')
rep('var o = Math.min(1, Math.max(0, (y - vh * 0.32) / (vh * 0.25)));', 'var o = Math.min(1, Math.max(0, (y - vh * 0.12) / (vh * 0.2)));')
rep('slogan.style.opacity = o.toFixed(3);', 'slogan.style.opacity = o.toFixed(3); slogan.classList.toggle("live", o > 0.6);')

# menu: continuous page with scrollspy
old_menu_start = s.index('  /* Menu: un gruppo di contenuti alla volta */')
old_menu_end = s.index('  /* Lingua: interruttore IT / EN */')
new_menu = r'''  /* Menu: pagina continua, il menu porta alla sezione e segue la lettura */
  (function () {
    var groups = Array.prototype.slice.call(document.querySelectorAll("[data-group]"));
    var navLinks = Array.prototype.slice.call(document.querySelectorAll(".topnav [data-go]"));
    var wrap = document.getElementById("groups");
    var navEl = document.getElementById("topnav");
    var lastY = window.scrollY, jumping = false, jt = null;
    function go(id) {
      var target = document.getElementById(id);
      if (!target) return;
      jumping = true; navEl.classList.remove("tucked");
      clearTimeout(jt); jt = setTimeout(function () { jumping = false; lastY = window.scrollY; }, 1100);
      var top = target.getBoundingClientRect().top + window.scrollY;
      if (target.classList.contains("pilotbox")) top -= navEl.offsetHeight + 28;
      window.scrollTo({ top: Math.max(0, top), behavior: reduce ? "auto" : "smooth" });
      if (history.replaceState) history.replaceState(null, "", "#" + id);
    }
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      var id = a.getAttribute("href").slice(1);
      if (!id || id === "top") return;
      a.addEventListener("click", function (e) { e.preventDefault(); go(id); });
    });
    document.getElementById("toTop").addEventListener("click", function (e) {
      e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
      if (history.replaceState) history.replaceState(null, "", location.pathname + location.search);
    });
    window.addEventListener("hashchange", function () { go(location.hash.slice(1)); });
    function spy() {
      var line = window.innerHeight * 0.35, cur = null;
      groups.forEach(function (g) { if (g.getBoundingClientRect().top <= line) cur = g.id; });
      navLinks.forEach(function (a) { a.setAttribute("aria-current", a.dataset.go === cur ? "true" : "false"); });
    }
    function navTone() {
      var y = window.scrollY, inContent = wrap.getBoundingClientRect().top < navEl.offsetHeight + 40;
      var introEl = document.getElementById("intro");
      var pastIntro = y > introEl.offsetHeight - window.innerHeight - 10;
      navEl.classList.toggle("light", inContent);
      var ln = document.getElementById("langnav"); if (ln) { ln.classList.toggle("light", inContent); }
      navEl.classList.toggle("at-intro", !inContent);
      if (!jumping && pastIntro && y > lastY + 4) navEl.classList.add("tucked");
      if (y < lastY - 4 || !pastIntro) navEl.classList.remove("tucked");
      if (ln) ln.classList.toggle("tucked", navEl.classList.contains("tucked") && document.getElementById("langMenu").hidden);
      if (Math.abs(y - lastY) > 4) lastY = y;
      spy();
    }
    window.addEventListener("scroll", navTone, { passive: true });
    window.addEventListener("resize", navTone);
    navTone();
    var h = location.hash.slice(1);
    if (h && document.getElementById(h)) setTimeout(function () { go(h); }, 80);
  })();

  /* Modulo programma pilota: invio al server, altrimenti email precompilata */
  (function () {
    var f = document.getElementById("pilotForm");
    if (!f) return;
    var st = document.getElementById("formStatus");
    function val(n) { return (f.elements[n].value || "").trim(); }
    function mailto() {
      var body = t("Nome e cognome") + ": " + val("nome") + "\n" + "Email: " + val("email") + "\n" + t("Azienda") + ": " + val("azienda") + "\n" +
        t("Coltura") + ": " + (val("coltura") ? t(val("coltura")) : "") + "\n" + t("Ettari (circa)") + ": " + val("ettari") + "\n\n" + val("messaggio");
      var subj = lang === "en" ? "Fitosat pilot program" : "Programma pilota Fitosat";
      window.location.href = "mailto:info@fitosat.it?subject=" + encodeURIComponent(subj) + "&body=" + encodeURIComponent(body);
      st.className = "status full"; st.textContent = t("Si sta aprendo il tuo programma di posta con la richiesta già compilata.");
    }
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!val("nome") || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val("email"))) {
        st.className = "status full err"; st.textContent = t("Inserisci nome ed email validi.");
        (val("nome") ? f.elements.email : f.elements.nome).focus(); return;
      }
      if (val("sito")) return;
      st.className = "status full"; st.textContent = t("Invio in corso…");
      var btn = f.querySelector("button[type=submit]"); btn.disabled = true;
      if (location.protocol === "file:" || !window.fetch) { btn.disabled = false; mailto(); return; }
      var data = new FormData(f); data.append("lingua", lang);
      fetch(f.getAttribute("action"), { method: "POST", body: data, headers: { "Accept": "application/json" } })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) {
          btn.disabled = false;
          if (j && j.ok) { f.classList.add("sent"); st.className = "status full"; st.textContent = t("Grazie! Ti risponderemo entro pochi giorni."); }
          else mailto();
        })
        .catch(function () { btn.disabled = false; mailto(); });
    });
  })();

'''
s = s[:old_menu_start] + new_menu + s[old_menu_end:]

# i18n: reverse dictionary so the switch works on both the IT and EN pages
rep('''    for (var n; (n = walker.nextNode());) {
      var raw = n.nodeValue, key = raw.replace(/\\s+/g, " ").trim();
      if (Object.prototype.hasOwnProperty.call(EN, key)) texts.push({ n: n, raw: raw, key: key, lead: raw.match(/^\\s*/)[0], trail: raw.match(/\\s*$/)[0] });
    }''', '''    var IT = {}; for (var k0 in EN) if (!Object.prototype.hasOwnProperty.call(IT, EN[k0])) IT[EN[k0]] = k0;
    function itKey(v) { return Object.prototype.hasOwnProperty.call(EN, v) ? v : Object.prototype.hasOwnProperty.call(IT, v) ? IT[v] : null; }
    for (var n; (n = walker.nextNode());) {
      var raw = n.nodeValue, key = itKey(raw.replace(/\\s+/g, " ").trim());
      if (key !== null) { var lead = raw.match(/^\\s*/)[0], trail = raw.match(/\\s*$/)[0]; texts.push({ n: n, raw: lead + key + trail, key: key, lead: lead, trail: trail }); }
    }''')
rep('''        var v = el.getAttribute(a);
        if (Object.prototype.hasOwnProperty.call(EN, v)) attrs.push({ el: el, a: a, v: v });''', '''        var v = itKey(el.getAttribute(a));
        if (v !== null) attrs.push({ el: el, a: a, v: v });''')
rep('''var meta = document.querySelector('meta[name="description"]'), metaIt = meta ? meta.content : "", titleIt = document.title;''',
    '''var meta = document.querySelector('meta[name="description"]'), metaIt = meta ? (itKey(meta.content) || meta.content) : "", titleIt = itKey(document.title) || document.title;''')
rep('''    var start = q || saved || ((navigator.language || "it").toLowerCase().indexOf("it") === 0 ? "it" : "en");
    if (start !== "it") apply(start); else { cur.textContent = "IT"; }''', '''    var pageLang = document.documentElement.getAttribute("data-page-lang") || "it";
    var bot = /bot|crawl|spider|slurp|lighthouse/i.test(navigator.userAgent || "");
    var start = q || (pageLang === "en" ? "en" : (bot ? "it" : (saved || ((navigator.language || "it").toLowerCase().indexOf("it") === 0 ? "it" : "en"))));
    if (start !== "it" || pageLang !== "it") apply(start); else { cur.textContent = "IT"; }''')

# dictionary additions
start = s.index('var EN = {')+len('var EN = ')
end = s.index('};', start)+1
EN = json.loads(s[start:end])
EN.update({
 "Nome e cognome":"Full name","Azienda":"Farm or company","Coltura":"Crop","Seleziona":"Select","Altro":"Other",
 "Ettari (circa)":"Hectares (approx.)","Messaggio (facoltativo)":"Message (optional)","Sito":"Website",
 "Usiamo questi dati solo per risponderti. Non li cediamo a terzi.":"We use this data only to reply to you. We never share it.",
 "Invia la richiesta":"Send request","Invio in corso…":"Sending…",
 "Grazie! Ti risponderemo entro pochi giorni.":"Thank you! We’ll get back to you within a few days.",
 "Si sta aprendo il tuo programma di posta con la richiesta già compilata.":"Your email app is opening with the request already filled in.",
 "Inserisci nome ed email validi.":"Please enter a valid name and email.",
})
s = s[:start] + json.dumps(EN, ensure_ascii=False) + s[end:]
open('/home/claude/build/index.html','w',encoding='utf-8').write(s)
print('ok', len(s))
