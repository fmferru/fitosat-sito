import json,re
P='/home/claude/staging/index.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,c=1):
    global s
    assert s.count(o)==c,(s.count(o),o[:80]); s=s.replace(o,n)
def cut(start,end):
    global s
    a=s.index(start); b=s.index(end,a)+len(end); seg=s[a:b]; s=s[:a]+s[b:]; return seg
# --- A: scale section into how ---
cut('  <section class="scale">','  </section>\n')
rep('''      <h2>Dallo spazio alla singola pianta</h2>
      <p class="prose">Quattro passaggi, dall’immagine alla mappa.</p>''','''      <h2>Dallo spazio alla singola pianta</h2>
      <p class="prose">Una sola immagine copre un intero territorio e distingue la singola pianta. Fitosat la unisce a meteo e suolo in una mappa del rischio.</p>
      <dl class="specs">
        <div><dt>Dettaglio</dt><dd>decine di centimetri</dd></div>
        <div><dt>Bande</dt><dd>visibile, red edge, infrarosso</dd></div>
        <div><dt>Accesso</dt><dd>ovunque, senza entrare in campo</dd></div>
      </dl>''')
# --- B: drop missions, move "what" into funziona after time ---
cut('  <section class="missions">','  </section>\n')
what=cut('  <section class="what">','  </section>\n')
what=what.replace('''      <h2>Uno strumento per decidere</h2>''','''      <h2>Uno strumento per decidere</h2>
      <p class="prose">Oggi ti mostra dove le piante stanno cedendo. Domani ti dirà dove una malattia è probabile, prima dei sintomi.</p>''')
rep('''  </section>
  </div>
  <div class="group" id="applicazioni" data-group="applicazioni">''','''  </section>
'''+what+'''  </div>
  <div class="group" id="applicazioni" data-group="applicazioni">''')
# --- C: steps inside pilot box ---
rep('''      <ol class="steps">
        <li><span class="n">01</span><h3>Ci indichi i tuoi appezzamenti</h3><p>Posizione e confini delle parcelle.</p></li>
        <li><span class="n">02</span><h3>Fitosat li osserva</h3><p>Per tutta la stagione, senza che tu faccia nulla.</p></li>
        <li><span class="n">03</span><h3>Ricevi mappa e avvisi</h3><p>Dove controllare e quando, da telefono o computer.</p></li>
      </ol>
''','')
rep('''          <p>Selezioniamo un numero limitato di aziende agricole per sperimentare Fitosat in campo, con istituti di ricerca del settore.</p>''','''          <p>Selezioniamo un numero limitato di aziende agricole per sperimentare Fitosat in campo, con istituti di ricerca del settore.</p>
          <ol class="pilot-steps">
            <li><strong>Ci indichi i tuoi appezzamenti</strong><span>Posizione e confini delle parcelle.</span></li>
            <li><strong>Fitosat li osserva</strong><span>Per tutta la stagione, senza che tu faccia nulla.</span></li>
            <li><strong>Ricevi mappa e avvisi</strong><span>Dove controllare e quando, da telefono o computer.</span></li>
          </ol>''')
# --- D: natural colours for steps 1-2 of the field ---
rep('#field[data-step="1"] .bg, #field[data-step="2"] .bg { fill: #3b3b3b; }','#field[data-step="1"] .bg, #field[data-step="2"] .bg { fill: #7a6248; }')
rep('#field[data-step="1"] .p { fill: #9c9c9c; }','#field[data-step="1"] .p { fill: var(--nat); }')
rep('#field[data-step="2"] .p { fill: #8c8c8c; }','#field[data-step="2"] .p { fill: var(--nat); }')
rep('''      c.style.setProperty("--c", color(v));''','''      c.style.setProperty("--c", color(v));
      var gtone = R2(); c.style.setProperty("--nat", gtone < .33 ? "#4f6e33" : gtone < .66 ? "#5d7d3b" : "#6a8a44");''')
rep('''  var row = 0;
  for (var yy = -170; yy <= 570; yy += 22) {''','''  var grass = el("g", { "class": "grass", stroke: "#8a8a52", "stroke-width": 7, opacity: .5 }, fg);
  for (var gy = -159; gy <= 581; gy += 22) el("line", { x1: -140, y1: gy, x2: 740, y2: gy }, grass);
  var row = 0;
  for (var yy = -170; yy <= 570; yy += 22) {''')
# --- CSS ---
css='''
  /* Revisione 19/11: sezioni unite, campo a colori, schede compatte su telefono */
  #field .grass { transition: opacity .5s; }
  #field[data-step="3"] .grass, #field[data-step="4"] .grass { opacity: 0; }
  .how .specs { margin: 1.25rem auto 2rem; max-width: 52rem; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; }
  .what .prose { text-align: center; margin-left: auto; margin-right: auto; }
  .pilot-steps { list-style: none; counter-reset: ps; margin: 1.4rem 0 0; padding: 0; display: grid; gap: .8rem; text-align: left; }
  .pilot-steps li { counter-increment: ps; position: relative; padding-left: 2.6rem; }
  .pilot-steps li::before { content: counter(ps); position: absolute; left: 0; top: .05rem; width: 1.8rem; height: 1.8rem; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center; font-family: var(--display); font-weight: 700; font-size: .95rem; padding-top: .12em;
    background: rgba(255,255,255,.16); color: #fff; border: 1px solid rgba(255,255,255,.35); }
  .pilot-steps strong { display: block; font-family: var(--display); font-size: 1.02rem; color: #fff; }
  .pilot-steps span { display: block; font-size: .92rem; opacity: .85; }
  .start h2 + .pilotbox { margin-top: 2rem; }
  @media (max-width: 760px) {
    .group .stats { grid-template-columns: 1fr 1fr; gap: .6rem; }
    .group .stats li { padding: .9rem .7rem; }
    .group .stats .num { font-size: 1.3rem; }
    .group .stats .num small { display: block; font-size: .75rem; margin: 0 0 .1rem; }
    .group .stats p { font-size: .86rem; line-height: 1.4; margin: .35rem 0 .45rem; }
    .group .stats cite { font-size: .75rem; line-height: 1.35; }
    .vine-uses { grid-template-columns: 1fr 1fr; gap: .55rem; }
    .vine-uses li { padding: .8rem .7rem; }
    .vine-uses h4 { font-size: .95rem; }
    .vine-uses p { font-size: .85rem; }
    .vine-uses li:last-child:nth-child(odd) { grid-column: 1 / -1; }
    .pilot-steps { max-width: 22rem; margin-left: auto; margin-right: auto; }
  }
'''
rep('</style>',css+'</style>')
# --- EN dictionary ---
a=s.index('var EN = ')+9; b=s.index('};',a)+1; EN=json.loads(s[a:b])
EN.update({
 "Una sola immagine copre un intero territorio e distingue la singola pianta. Fitosat la unisce a meteo e suolo in una mappa del rischio.":"A single image covers an entire territory and still tells each plant apart. Fitosat combines it with weather and soil into a risk map.",
 "Oggi ti mostra dove le piante stanno cedendo. Domani ti dirà dove una malattia è probabile, prima dei sintomi.":"Today it shows you where plants are failing. Tomorrow it will tell you where a disease is likely, before symptoms appear.",
})
for k in ["Ci indichi i tuoi appezzamenti","Posizione e confini delle parcelle.","Fitosat li osserva","Per tutta la stagione, senza che tu faccia nulla.","Ricevi mappa e avvisi","Dove controllare e quando, da telefono o computer."]:
    assert k in EN, k
s=s[:a]+json.dumps(EN,ensure_ascii=False)+s[b:]
open(P,'w',encoding='utf-8').write(s)
print('ok')
