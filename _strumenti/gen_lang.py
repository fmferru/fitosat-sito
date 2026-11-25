import json, re
P = '/home/claude/staging/index.html'
s = open(P, encoding='utf-8').read()
def dict_of(name):
    a = s.index(f'var {name} = ') + len(f'var {name} = '); b = s.index('};', a) + 1; return json.loads(s[a:b])
OGD = 'Scopri quali piante stanno soffrendo, prima che sia evidente in campo. Fitosat osserva le tue coltivazioni dal satellite e ti avvisa quando qualcosa non va.'
OGA = 'Fitosat: logo nel cielo stellato sopra la Terra vista dallo spazio'
META = {
 'en': dict(ogd='See which plants are struggling, before it&#39;s obvious in the field. Fitosat monitors your crops from satellite and alerts you when something is wrong.',
            oga='Fitosat: logo in the starry sky above the Earth seen from space', loc='en_GB', img='og-image-en.jpg'),
 'es': dict(ogd='Descubre qué plantas están sufriendo, antes de que se note en el campo. Fitosat observa tus cultivos desde el satélite y te avisa cuando algo no va bien.',
            oga='Fitosat: logotipo en el cielo estrellado sobre la Tierra vista desde el espacio', loc='es_ES', img='og-image-es.jpg'),
 'fr': dict(ogd='Découvrez quelles plantes souffrent, avant que cela se voie au champ. Fitosat observe vos cultures depuis le satellite et vous alerte quand quelque chose ne va pas.',
            oga='Fitosat : logo dans le ciel étoilé au-dessus de la Terre vue de l’espace', loc='fr_FR', img='og-image-fr.jpg'),
 'pt': dict(ogd='Descubra que plantas estão a sofrer, antes de se notar no campo. A Fitosat observa as suas culturas a partir do satélite e avisa-o quando algo não está bem.',
            oga='Fitosat: logótipo no céu estrelado sobre a Terra vista do espaço', loc='pt_PT', img='og-image-pt.jpg'),
}
head_end = s.index('<body>'); sc = s.index('<script>', head_end)
H0, B0, tail = s[:head_end], s[head_end:sc], s[sc:]
for L in ['en', 'es', 'fr', 'pt']:
    D = dict_of(L.upper()); M = META[L]
    def tx(m):
        raw = m.group(1); key = re.sub(r'\s+', ' ', raw).strip()
        if key in D:
            lead = re.match(r'^\s*', raw).group(0); trail = re.search(r'\s*$', raw).group(0); return '>' + lead + D[key] + trail + '<'
        return m.group(0)
    body = re.sub(r'>([^<>]+)<', tx, B0)
    body = re.sub(r'\b(aria-label|alt|data-hud|title|href)="([^"]*)"', lambda m: f'{m.group(1)}="{D[m.group(2)]}"' if m.group(2) in D else m.group(0), body)
    head = H0.replace('<html lang="it">', f'<html lang="{L}" data-page-lang="{L}">')
    T = 'Fitosat – Radici nella terra, occhi dal cielo'
    head = head.replace(f'<title>{T}</title>', f'<title>{D[T]}</title>').replace(f'content="{T}"', f'content="{D[T]}"')
    Dd = 'Immagini satellitari e machine learning per scoprire in tempo dove le tue colture soffrono. Prova gratuita per aziende agricole.'
    head = head.replace(f'content="{Dd}"', f'content="{D[Dd]}"')
    head = head.replace(f'content="{OGD}"', f'content="{M["ogd"]}"').replace(f'content="{OGA}"', f'content="{M["oga"]}"')
    head = head.replace('<meta property="og:url" content="https://fitosat.it/">', f'<meta property="og:url" content="https://fitosat.it/{L}/">')
    head = head.replace('<meta property="og:locale" content="it_IT">', f'<meta property="og:locale" content="{M["loc"]}">')
    head = head.replace('https://fitosat.it/img/og-image.jpg', f'https://fitosat.it/img/{M["img"]}')
    head = head.replace('<link rel="canonical" href="https://fitosat.it/">', f'<link rel="canonical" href="https://fitosat.it/{L}/">')
    body = re.sub(r'(?<=["\s,])(img|fonts)/', r'../\1/', body)
    body = re.sub(r'(<p class="nojs-lang">.*?</p>)', lambda m: re.sub(r'href="([^"]*)"', lambda h: 'href="../' + ('' if h.group(1) == './' else h.group(1)) + '"', m.group(1)), body, flags=re.S)
    head = re.sub(r'(?<=["\s,(])(img|fonts)/', r'../\1/', head)
    import os; os.makedirs(f'/home/claude/staging/{L}', exist_ok=True)
    open(f'/home/claude/staging/{L}/index.html', 'w', encoding='utf-8').write(head + body + tail)
    left = [m.strip() for m in re.findall(r'>([^<>]{4,})<', body) if re.sub(r'\s+', ' ', m).strip() not in D.values()]
    it_left = [x for x in left if re.search(r'\b(il|la|di|che|per|delle|una|dove|sono)\b|[àèìòù’]', x) and not x.startswith(('{', '/*'))]
    print(L, 'possibly untranslated:', it_left[:12])
