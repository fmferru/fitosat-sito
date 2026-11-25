import re
import json,re,sys
s=open('/home/claude/staging/index.html',encoding='utf-8').read()
a=s.index('var EN = ')+9; b=s.index('};',a)+1; EN=json.loads(s[a:b])
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
T='Fitosat – Radici nella terra, occhi dal cielo'
head=head.replace(f'<title>{T}</title>',f'<title>{EN[T]}</title>').replace(f'content="{T}"',f'content="{EN[T]}"')
D='Immagini satellitari e machine learning per scoprire in tempo dove le tue colture soffrono. Prova gratuita per aziende agricole.'
head=head.replace(f'content="{D}"',f'content="{EN[D]}"')
head=head.replace('content="Scopri quali piante stanno soffrendo, prima che sia evidente in campo. Fitosat osserva le tue coltivazioni dal satellite e ti avvisa quando qualcosa non va."','content="See which plants are struggling, before it&#39;s obvious in the field. Fitosat monitors your crops from satellite and alerts you when something is wrong."')
head=head.replace('<meta property="og:url" content="https://fitosat.it/">','<meta property="og:url" content="https://fitosat.it/en/">')
head=head.replace('<meta property="og:locale" content="it_IT">','<meta property="og:locale" content="en_GB">')
head=head.replace('https://fitosat.it/img/og-image.jpg','https://fitosat.it/img/og-image-en.jpg')
head=head.replace('content="Fitosat: logo nel cielo stellato sopra la Terra vista dallo spazio"','content="Fitosat: logo in the starry sky above the Earth seen from space"')
head=head.replace('<link rel="canonical" href="https://fitosat.it/">','<link rel="canonical" href="https://fitosat.it/en/">')
body=re.sub(r'(?<=["\s,])(img|fonts)/', r'../\1/', body)
body=body.replace('<a href="en/" hreflang="en" lang="en">English version</a>','<a href="../" hreflang="it" lang="it">Versione italiana</a>')  # nojs-lang
head=re.sub(r'(?<=["\s,(])(img|fonts)/', r'../\1/', head)
open('/home/claude/staging/en/index.html','w',encoding='utf-8').write(head+body+tail)
# report untranslated visible text
left=[m.strip() for m in re.findall(r'>([^<>]{4,})<', body) if re.search(r'[a-zà-ù]{3}',m) and re.sub(r'\s+',' ',m).strip() not in EN.values()]
print('possibly untranslated:', [x for x in left if re.search(r'\b(il|la|di|che|per|delle|una|dove|sono)\b|[àèéìòù’]',x)][:30])
