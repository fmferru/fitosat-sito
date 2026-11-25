import re, json, html
s=open('/home/claude/build/index.html',encoding='utf-8').read()
a=s.index('var EN = ')+9; b=s.index('};',a)+1; EN=json.loads(s[a:b])
head_end=s.index('<body>'); script_start=s.index('<script>', head_end)
head, body, tail = s[:head_end], s[head_end:script_start], s[script_start:]
def tx(m):
    raw=m.group(1); key=re.sub(r'\s+',' ',raw).strip()
    if key in EN:
        lead=re.match(r'^\s*',raw).group(0); trail=re.search(r'\s*$',raw).group(0)
        return '>'+lead+EN[key]+trail+'<'
    return m.group(0)
# skip svg inner text? there is none translatable; translate text nodes
body=re.sub(r'>([^<>]+)<', tx, body)
def ta(m):
    name,val=m.group(1),m.group(2)
    return f'{name}="{EN[val]}"' if val in EN else m.group(0)
body=re.sub(r'\b(aria-label|alt|data-hud|title|href)="([^"]*)"', ta, body)
head=head.replace('<html lang="it">','<html lang="en" data-page-lang="en">')
T_it='Fitosat – Radici in campo, occhi dal cielo'
head=head.replace(f'<title>{T_it}</title>', f'<title>{EN[T_it]}</title>')
head=head.replace(f'content="{T_it}"', f'content="{EN[T_it]}"')
D_it='Fitosat osserva le tue coltivazioni dal satellite e ti avvisa quando qualcosa non va, pianta per pianta. Programma pilota aperto alle aziende agricole.'
head=head.replace(f'content="{D_it}"', f'content="{EN[D_it]}"')
head=head.replace('content="Scopri quali piante si stanno ammalando, prima che si veda. Fitosat osserva le tue coltivazioni dal satellite e ti avvisa quando qualcosa non va."',
                  'content="See which plants are getting sick, before it shows. Fitosat monitors your crops from satellite and alerts you when something is wrong."')
head=head.replace('<meta property="og:url" content="https://www.fitosat.it/">','<meta property="og:url" content="https://www.fitosat.it/en/">')
head=head.replace('<meta property="og:locale" content="it_IT">','<meta property="og:locale" content="en_GB">')
head=head.replace('<link rel="canonical" href="https://www.fitosat.it/">','<link rel="canonical" href="https://www.fitosat.it/en/">')
out=head+body+tail
import os; os.makedirs('/home/claude/build/en',exist_ok=True)
open('/home/claude/build/en/index.html','w',encoding='utf-8').write(out)
# report leftover Italian-looking text nodes
left=[m for m in re.findall(r'>([^<>]{3,})<', body) if re.search(r'[àèéìòù’]|\b(il|la|di|che|per|delle)\b', m)]
print(len(out)); print(left[:20])
