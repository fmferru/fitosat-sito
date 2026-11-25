"""Genera le pagine 'Note legali' (IT/EN) con lo stesso stile dell'informativa privacy."""
import re
s = open('/home/claude/staging/404.html', encoding='utf-8').read()
head_assets = '\n'.join(re.findall(r'<link rel="(?:icon|apple-touch-icon)"[^>]+>', s))
fonts = '\n'.join(re.findall(r'@font-face \{[^}]+\}', s))
CSS = f'''{fonts}
  :root {{ --bg:#f4ebe6; --surface:#fff; --ink:#24161d; --muted:#5a434c; --brand:#66284a; --line:#d6c2bc; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#1c1416; --surface:#261b1f; --ink:#f1e7e9; --muted:#d4c3c9; --brand:#e0b4c8; --line:#4d3842; }} }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Questrial","Avenir Next","Segoe UI",sans-serif; line-height:1.6; }}
  header {{ display:flex; justify-content:space-between; align-items:center; gap:1rem; max-width:46rem; margin:0 auto; padding:1.25rem 1.25rem 0; }}
  header a {{ color:var(--brand); font-weight:700; text-decoration:none; font-family:"Josefin Sans",sans-serif; }}
  main {{ max-width:46rem; margin:0 auto; padding:1.5rem 1.25rem 4rem; }}
  h1 {{ font-family:"Josefin Sans",sans-serif; font-weight:700; font-size:clamp(1.8rem,5vw,2.4rem); line-height:1.15; margin:.5rem 0 .25rem; }}
  h2 {{ font-family:"Josefin Sans",sans-serif; font-weight:700; font-size:1.2rem; margin:2rem 0 .4rem; color:var(--brand); }}
  p, li, dd {{ color:var(--ink); }} .upd {{ color:var(--muted); font-size:.9rem; margin:0 0 1.5rem; }}
  a {{ color:var(--brand); }}
  .card {{ background:var(--surface); border:1px solid var(--line); border-radius:14px; padding:.4rem 1.2rem; margin:0; }}
  .card div {{ display:grid; grid-template-columns:minmax(9rem, 14rem) 1fr; gap:.2rem 1rem; padding:.7rem 0; border-top:1px solid var(--line); }}
  .card div:first-child {{ border-top:0; }}
  .card dt {{ color:var(--muted); font-size:.92rem; }}
  .card dd {{ margin:0; font-variant-numeric:tabular-nums; overflow-wrap:anywhere; }}
  @media (max-width: 520px) {{ .card div {{ grid-template-columns:1fr; }} }}
  a:focus-visible {{ outline:3px solid var(--brand); outline-offset:2px; border-radius:3px; }}
'''
CF = '14965880967'
REA = 'MI-2819311'

def rows(items):
    return '\n'.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in items)

IT = dict(lang='it', title='Note legali – Fitosat', home='./', home_t='← Torna a Fitosat', alt='en/note-legali.html', alt_t='English',
canon='https://fitosat.it/note-legali.html',
body=f'''<h1>Note legali</h1>
<p class="upd">Ultimo aggiornamento: 22 novembre 2026</p>
<h2>Dati societari</h2>
<dl class="card">
{rows([("Ragione sociale","Fitosat srl"),
       ("Sede legale","Via Lanzone 5, 20123 Milano (MI)"),
       ("Codice fiscale e Partita IVA",CF),
       ("Registro delle Imprese","Milano Monza Brianza Lodi, n. "+CF),
       ("Numero REA",REA),
       ("Qualifica","Startup innovativa iscritta nella sezione speciale del Registro delle Imprese"),
       ("Email",'<a href="mailto:info@fitosat.it">info@fitosat.it</a>')])}
</dl>
<h2>Sito web</h2>
<p>Il sito fitosat.it è ospitato da GitHub Pages (GitHub, Inc.). Non usa cookie né strumenti di tracciamento. Per il trattamento dei dati personali vedi l’<a href="privacy.html">informativa privacy</a>.</p>
<h2>Contenuti e immagini</h2>
<p>Testi, grafica e marchio Fitosat appartengono a Fitosat srl. Le immagini della Terra vista dallo spazio sono elaborate a partire da Blue Marble, NASA. Le immagini di campi e filari e le mappe dimostrative sono illustrazioni realizzate per questo sito e non rappresentano dati reali di clienti. I dati statistici citati riportano ciascuno la propria fonte.</p>''')

EN = dict(lang='en', title='Legal information – Fitosat', home='./', home_t='← Back to Fitosat', alt='../note-legali.html', alt_t='Italiano',
canon='https://fitosat.it/en/note-legali.html',
body=f'''<h1>Legal information</h1>
<p class="upd">Last updated: 22 November 2026</p>
<h2>Company details</h2>
<dl class="card">
{rows([("Company name","Fitosat srl"),
       ("Registered office","Via Lanzone 5, 20123 Milano (MI), Italy"),
       ("Tax code and VAT no.",CF),
       ("Companies Register","Milano Monza Brianza Lodi, no. "+CF),
       ("REA number",REA),
       ("Status","Innovative startup registered in the special section of the Companies Register"),
       ("Email",'<a href="mailto:info@fitosat.it">info@fitosat.it</a>')])}
</dl>
<h2>Website</h2>
<p>fitosat.it is hosted by GitHub Pages (GitHub, Inc.). It uses no cookies and no tracking tools. For how we handle personal data, see the <a href="privacy.html">privacy notice</a>.</p>
<h2>Content and images</h2>
<p>Texts, graphics and the Fitosat brand belong to Fitosat srl. The images of the Earth seen from space are derived from NASA’s Blue Marble. The images of fields and vine rows and the demo maps are illustrations made for this site and do not show real customer data. Each statistic quoted on the site cites its own source.</p>''')

for d, path in [(IT, '/home/claude/staging/note-legali.html'), (EN, '/home/claude/staging/en/note-legali.html')]:
    html = f'''<!DOCTYPE html>
<html lang="{d['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{d['title']}</title>
<link rel="canonical" href="{d['canon']}">
<link rel="alternate" hreflang="it" href="https://fitosat.it/note-legali.html">
<link rel="alternate" hreflang="en" href="https://fitosat.it/en/note-legali.html">
{head_assets}
<style>{CSS}</style>
</head>
<body>
<header><a href="{d['home']}">{d['home_t']}</a><a href="{d['alt']}" hreflang="{'en' if d['lang']=='it' else 'it'}">{d['alt_t']}</a></header>
<main>
{d['body']}
</main>
</body>
</html>
'''
    pre = '../' if '/en/' in path else ''
    html = re.sub(r'(?<=["(])/?(fonts|img)/', lambda m: pre + m.group(1) + '/', html)
    open(path, 'w', encoding='utf-8').write(html)
print('ok')
