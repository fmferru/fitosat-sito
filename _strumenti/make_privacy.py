import re
s=open('/home/claude/staging/404.html',encoding='utf-8').read()
head_assets='\n'.join(re.findall(r'<link rel="(?:icon|apple-touch-icon)"[^>]+>',s))
fonts='\n'.join(re.findall(r'@font-face \{[^}]+\}',s))
CSS=f'''{fonts}
  :root {{ --bg:#f4ebe6; --surface:#fff; --ink:#24161d; --muted:#5a434c; --brand:#66284a; --line:#d6c2bc; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#1c1416; --surface:#261b1f; --ink:#f1e7e9; --muted:#d4c3c9; --brand:#e0b4c8; --line:#4d3842; }} }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Questrial","Avenir Next","Segoe UI",sans-serif; line-height:1.6; }}
  header {{ display:flex; justify-content:space-between; align-items:center; gap:1rem; max-width:46rem; margin:0 auto; padding:1.25rem 1.25rem 0; }}
  header a {{ color:var(--brand); font-weight:700; text-decoration:none; font-family:"Josefin Sans",sans-serif; }}
  main {{ max-width:46rem; margin:0 auto; padding:1.5rem 1.25rem 4rem; }}
  h1 {{ font-family:"Josefin Sans",sans-serif; font-weight:700; font-size:clamp(1.8rem,5vw,2.4rem); line-height:1.15; margin:.5rem 0 .25rem; }}
  h2 {{ font-family:"Josefin Sans",sans-serif; font-weight:700; font-size:1.2rem; margin:2rem 0 .4rem; color:var(--brand); }}
  p, li {{ color:var(--ink); }} .upd {{ color:var(--muted); font-size:.9rem; margin:0 0 1.5rem; }}
  a {{ color:var(--brand); }} ul {{ padding-left:1.2rem; }}
  .card {{ background:var(--surface); border:1px solid var(--line); border-radius:14px; padding:1rem 1.2rem; }}
  a:focus-visible {{ outline:3px solid var(--brand); outline-offset:2px; border-radius:3px; }}
'''
IT=dict(lang='it',title='Informativa privacy – Fitosat',home='./',home_t='← Torna a Fitosat',alt='en/privacy.html',alt_t='English',canon='https://fitosat.it/privacy.html',
body='''<h1>Informativa privacy</h1>
<p class="upd">Ultimo aggiornamento: 22 novembre 2026</p>
<p>Questa informativa spiega come Fitosat tratta i dati personali di chi visita il sito fitosat.it o ci contatta, ai sensi del Regolamento (UE) 2016/679 (GDPR) e del D.Lgs. 196/2003.</p>
<h2>Titolare del trattamento</h2>
<p class="card">Fitosat srl – Via Lanzone 5, 20123 Milano (MI)<br>Email: <a href="mailto:info@fitosat.it">info@fitosat.it</a></p>
<h2>Quali dati trattiamo</h2>
<ul>
<li><strong>Dati che ci invii tu.</strong> Se ci scrivi tramite il modulo del programma pilota, il pulsante “Provalo gratis” o un’email: nome, indirizzo email e le informazioni che scegli di indicare (azienda, coltura, ettari, messaggio). Il modulo non invia dati a un server: prepara un’email che parte dal tuo programma di posta.</li>
<li><strong>Dati di navigazione.</strong> Il servizio che ospita il sito registra in modo automatico dati tecnici come indirizzo IP, tipo di browser, pagina richiesta, data e ora, per garantire il funzionamento e la sicurezza del sito.</li>
<li><strong>Preferenza di lingua.</strong> Se scegli italiano o inglese, la scelta viene salvata solo nel tuo browser (archiviazione locale) e non ci viene inviata.</li>
</ul>
<h2>Perché li trattiamo e su quale base</h2>
<ul>
<li>Rispondere alle tue richieste e valutare la partecipazione al programma pilota: misure precontrattuali richieste da te (art. 6.1.b GDPR).</li>
<li>Funzionamento e sicurezza del sito: legittimo interesse (art. 6.1.f GDPR).</li>
</ul>
<p>Non usiamo i dati per profilazione o pubblicità e non li vendiamo né li cediamo a terzi per loro finalità.</p>
<h2>Cookie e strumenti di tracciamento</h2>
<p>Il sito non usa cookie, statistiche di visita né strumenti di tracciamento di terze parti. Per questo non è necessario un banner di consenso.</p>
<h2>Chi tratta i dati per nostro conto</h2>
<ul>
<li><strong>GitHub, Inc.</strong> (gruppo Microsoft), che ospita il sito e registra i dati di navigazione. I server possono trovarsi negli Stati Uniti: il trasferimento avviene sulla base delle garanzie previste dal GDPR, come il Data Privacy Framework UE-USA o le clausole contrattuali standard.</li>
<li><strong>Aruba S.p.A.</strong>, che gestisce la nostra casella email in Italia.</li>
</ul>
<h2>Per quanto tempo</h2>
<p>Conserviamo le email e i dati di contatto per il tempo necessario a gestire la richiesta e, se non nasce un rapporto, al massimo per 24 mesi. I dati di navigazione sono conservati dal fornitore di hosting per i tempi tecnici necessari.</p>
<h2>I tuoi diritti</h2>
<p>Puoi chiedere in ogni momento di accedere ai tuoi dati, correggerli, cancellarli, limitarne il trattamento, opporti o riceverli in formato portabile (artt. 15–22 GDPR), scrivendo a <a href="mailto:info@fitosat.it">info@fitosat.it</a>. Hai anche il diritto di presentare reclamo al Garante per la protezione dei dati personali (<a href="https://www.garanteprivacy.it">www.garanteprivacy.it</a>).</p>
<h2>Modifiche</h2>
<p>Potremo aggiornare questa informativa; la data in alto indica l’ultima versione.</p>''')
EN=dict(lang='en',title='Privacy notice – Fitosat',home='./',home_t='← Back to Fitosat',alt='../privacy.html',alt_t='Italiano',canon='https://fitosat.it/en/privacy.html',
body='''<h1>Privacy notice</h1>
<p class="upd">Last updated: 22 November 2026</p>
<p>This notice explains how Fitosat processes the personal data of people who visit fitosat.it or contact us, under Regulation (EU) 2016/679 (GDPR) and Italian Legislative Decree 196/2003.</p>
<h2>Data controller</h2>
<p class="card">Fitosat srl – Via Lanzone 5, 20123 Milan (MI), Italy<br>Email: <a href="mailto:info@fitosat.it">info@fitosat.it</a></p>
<h2>What data we process</h2>
<ul>
<li><strong>Data you send us.</strong> If you write to us through the pilot program form, the “Try it free” button or by email: your name, email address and any information you choose to include (company, crop, hectares, message). The form does not send data to a server: it prepares an email that you send from your own mail app.</li>
<li><strong>Browsing data.</strong> The service hosting the site automatically logs technical data such as IP address, browser type, requested page, date and time, to keep the site running and secure.</li>
<li><strong>Language preference.</strong> If you choose Italian or English, the choice is stored only in your browser (local storage) and is never sent to us.</li>
</ul>
<h2>Why we process it and on what basis</h2>
<ul>
<li>To reply to your requests and assess participation in the pilot program: pre-contractual steps taken at your request (Art. 6(1)(b) GDPR).</li>
<li>To run and secure the site: legitimate interest (Art. 6(1)(f) GDPR).</li>
</ul>
<p>We do not use your data for profiling or advertising, and we do not sell it or share it with third parties for their own purposes.</p>
<h2>Cookies and tracking</h2>
<p>The site uses no cookies, no visitor analytics and no third-party tracking tools, so no consent banner is needed.</p>
<h2>Who processes data on our behalf</h2>
<ul>
<li><strong>GitHub, Inc.</strong> (Microsoft group), which hosts the site and logs browsing data. Its servers may be located in the United States: transfers rely on the safeguards provided by the GDPR, such as the EU-US Data Privacy Framework or standard contractual clauses.</li>
<li><strong>Aruba S.p.A.</strong>, which runs our email inbox in Italy.</li>
</ul>
<h2>How long we keep it</h2>
<p>We keep emails and contact details for as long as needed to handle your request and, if no business relationship follows, for no more than 24 months. Browsing data is kept by the hosting provider for the time technically required.</p>
<h2>Your rights</h2>
<p>You can ask at any time to access, correct or delete your data, restrict or object to its processing, or receive it in a portable format (Arts. 15–22 GDPR), by writing to <a href="mailto:info@fitosat.it">info@fitosat.it</a>. You also have the right to lodge a complaint with the Italian Data Protection Authority (<a href="https://www.garanteprivacy.it">www.garanteprivacy.it</a>).</p>
<h2>Changes</h2>
<p>We may update this notice; the date at the top shows the latest version.</p>''')
for d,path in [(IT,'/home/claude/staging/privacy.html'),(EN,'/home/claude/staging/en/privacy.html')]:
    html=f'''<!DOCTYPE html>
<html lang="{d['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{d['title']}</title>
<link rel="canonical" href="{d['canon']}">
<link rel="alternate" hreflang="it" href="https://fitosat.it/privacy.html">
<link rel="alternate" hreflang="en" href="https://fitosat.it/en/privacy.html">
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
    pre='../' if path.count('/en/') else ''
    html=re.sub(r'(?<=["(])/?(fonts|img)/', lambda m: pre+m.group(1)+'/', html)
    open(path,'w',encoding='utf-8').write(html)
print('ok')
