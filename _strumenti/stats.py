import json,re
P='/home/claude/staging/index.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,o[:70]; s=s.replace(o,n)
# Problem
rep('<cite><a href="https://www.fao.org/north-america/news/details/international-day-of-plant-health-2026-spotlights-plant-biosecurity-as-a-foundation-for-global-food-security/en" rel="noopener">FAO, 2026</a></cite>',
    '<cite><a href="https://ippc.int/en/news/press-release-international-day-of-plant-health-2026-spotlights-plant-biosecurity-as-a-foundation-for-global-food-security/" rel="noopener">FAO, maggio 2026</a></cite>')
rep('''<span class="num alert">10 mln</span>
          <p>di ulivi morti in Puglia per un solo batterio da quarantena.</p>
          <cite><a href="https://www.ansa.it/canale_terraegusto/notizie/mondo_agricolo/2026/10/15/xylella-30-milioni-di-euro-per-la-rigenerazione-degli-oliveti-in-puglia_1de4a5eb-65f1-491a-bf88-b985dc612a3b.html" rel="noopener">ANSA, ottobre 2026</a></cite>''',
'''<span class="num alert"><small>circa </small>10 mln</span>
          <p>di ulivi colpiti in Puglia dal 2013 da un solo batterio da quarantena.</p>
          <cite><a href="https://www.ilpost.it/2026/01/20/xylella-novita-salento-resilienza-batterio/" rel="noopener">Stima Regione Puglia, via Il Post, 2026</a></cite>''')
rep('<cite><a href="https://eprs.europarl.europa.eu/contents/publications/EPRS/2026/09/EPRS_BRI(2026)791467.html" rel="noopener">Eurostat, via Parlamento europeo, 2026</a></cite>',
    '<cite><a href="https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260513-3" rel="noopener">Eurostat, maggio 2026</a></cite>')
rep('<cite><a href="https://www.efanews.eu/item/62092-aziende-agricole-il-numero-si-mantiene-stabile.html" rel="noopener">Istat, 2026</a></cite>',
    '<cite><a href="https://www.istat.it/wp-content/uploads/2026/07/Focus-Struttura-produttiva-pratiche-gestionali-e-forza-lavoro-delle-aziende-agricole_Anno-2023.pdf" rel="noopener">Istat, luglio 2026</a></cite>')
# Vine
a=s.index('<ul class="stats">', s.index('<section class="vine">')); b=s.index('</ul>',a)+5
s=s[:a]+'''<ul class="stats">
        <li>
          <span class="num">726.000 ha</span>
          <p>di vigneti in Italia: primo Paese al mondo per produzione di vino.</p>
          <cite><a href="https://www.oiv.int/sites/default/files/2026-05/OIV-State_of_the_World_Wine_Sector_in_2025.pdf" rel="noopener">OIV, maggio 2026</a></cite>
        </li>
        <li>
          <span class="num alert"><small>circa il </small>60%</span>
          <p>dei fungicidi usati nell’Unione europea va alla viticoltura.</p>
          <cite><a href="https://cordis.europa.eu/project/id/101132223" rel="noopener">Commissione europea, CORDIS</a></cite>
        </li>
        <li>
          <span class="num alert">83%</span>
          <p>delle viti esaminate in 218 vigneti dell’Alessandrino nel 2025 aveva sintomi di mal dell’esca.</p>
          <cite><a href="https://www.ciaal-at.it/2026/05/05/progetto-mal-dellesca-nella-viticoltura-alessandrina-2025-2026/" rel="noopener">Monitoraggio Cia, Confagricoltura, Coldiretti, Codial, 2026</a></cite>
        </li>
        <li>
          <span class="num"><small>oltre </small>10.400</span>
          <p>trappole controllate in Piemonte nel 2025 per seguire una sola malattia da quarantena.</p>
          <cite><a href="https://www.regione.piemonte.it/web/sites/default/files/media/documenti/2026-03/fd_aggiornamento_2025_strategie2026.pdf" rel="noopener">Regione Piemonte, 2026</a></cite>
        </li>
      </ul>'''+s[b:]
# dictionary
a=s.index('var EN = ')+9; b=s.index('};',a)+1; EN=json.loads(s[a:b])
EN.update({
 "FAO, maggio 2026":"FAO, May 2026",
 "di ulivi colpiti in Puglia dal 2013 da un solo batterio da quarantena.":"olive trees hit in Apulia since 2013 by a single quarantine bacterium.",
 "Stima Regione Puglia, via Il Post, 2026":"Apulia Region estimate, via Il Post, 2026",
 "Eurostat, maggio 2026":"Eurostat, May 2026",
 "Istat, luglio 2026":"Istat, July 2026",
 "726.000 ha":"726,000 ha",
 "di vigneti in Italia: primo Paese al mondo per produzione di vino.":"of vineyards in Italy, the world’s largest wine producer.",
 "OIV, maggio 2026":"OIV, May 2026",
 "60%":"60%",
 "Commissione europea, CORDIS":"European Commission, CORDIS",
 "delle viti esaminate in 218 vigneti dell’Alessandrino nel 2025 aveva sintomi di mal dell’esca.":"of vines inspected across 218 vineyards around Alessandria in 2025 showed esca symptoms.",
 "Monitoraggio Cia, Confagricoltura, Coldiretti, Codial, 2026":"Survey by Cia, Confagricoltura, Coldiretti, Codial, 2026",
 "10.400":"10,400",
 "trappole controllate in Piemonte nel 2025 per seguire una sola malattia da quarantena.":"insect traps checked in Piedmont in 2025 to track a single quarantine disease.",
 "Regione Piemonte, 2026":"Piedmont Region, 2026",
 "circa":"about",
})
s=s[:a]+json.dumps(EN,ensure_ascii=False)+s[b:]
open(P,'w',encoding='utf-8').write(s)

# regenerate EN page
head_end=s.index('<body>'); sc=s.index('<script>',head_end)
head,body,tail=s[:head_end],s[head_end:sc],s[sc:]
def tx(m):
    raw=m.group(1); key=re.sub(r'\s+',' ',raw).strip()
    if key in EN:
        lead=re.match(r'^\s*',raw).group(0); trail=re.search(r'\s*$',raw).group(0); return '>'+lead+EN[key]+trail+'<'
    return m.group(0)
body=re.sub(r'>([^<>]+)<',tx,body)
body=re.sub(r'\b(aria-label|alt|data-hud|title|href)="([^"]*)"',lambda m: f'{m.group(1)}="{EN[m.group(2)]}"' if m.group(2) in EN else m.group(0),body)
head=head.replace('<html lang="it">','<html lang="en" data-page-lang="en">')
T='Fitosat – Radici in campo, occhi dal cielo'
head=head.replace(f'<title>{T}</title>',f'<title>{EN[T]}</title>').replace(f'content="{T}"',f'content="{EN[T]}"')
D='Fitosat osserva le tue coltivazioni dal satellite e ti avvisa quando qualcosa non va, pianta per pianta. Programma pilota aperto alle aziende agricole.'
head=head.replace(f'content="{D}"',f'content="{EN[D]}"')
head=head.replace('content="Scopri quali piante si stanno ammalando, prima che si veda. Fitosat osserva le tue coltivazioni dal satellite e ti avvisa quando qualcosa non va."','content="See which plants are getting sick, before it shows. Fitosat monitors your crops from satellite and alerts you when something is wrong."')
head=head.replace('<meta property="og:url" content="https://fitosat.it/">','<meta property="og:url" content="https://fitosat.it/en/">')
head=head.replace('<meta property="og:locale" content="it_IT">','<meta property="og:locale" content="en_GB">')
head=head.replace('<link rel="canonical" href="https://fitosat.it/">','<link rel="canonical" href="https://fitosat.it/en/">')
en=head+body+tail
open('/home/claude/staging/en/index.html','w',encoding='utf-8').write(en)
# compare with current live EN page apart from stats
old=open('/home/claude/site/en/index.html',encoding='utf-8').read()
import difflib
d=[l for l in difflib.unified_diff(old.splitlines(),en.splitlines(),lineterm='',n=0) if l[:1] in '+-' and not l.startswith(('+++','---'))]
print(len(d)); print('\n'.join(x[:160] for x in d if 'var EN' not in x))
