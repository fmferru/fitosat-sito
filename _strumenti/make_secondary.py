"""Privacy e Note legali in IT, EN, ES, FR, PT (stesso stile). Riusa CSS e testi IT/EN dagli script esistenti."""
import re, os
LANGS = ['it', 'en', 'es', 'fr', 'pt']
NAMES = {'it': 'Italiano', 'en': 'English', 'es': 'Español', 'fr': 'Français', 'pt': 'Português'}
HOME_T = {'it': '← Torna a Fitosat', 'en': '← Back to Fitosat', 'es': '← Volver a Fitosat', 'fr': '← Retour à Fitosat', 'pt': '← Voltar à Fitosat'}
ST = '/home/claude/staging'

def load(path):
    src = open(path, encoding='utf-8').read()
    src = src[:src.index('for d')]
    g = {}; exec(src, g); return g

P = load('/home/claude/build/make_privacy.py')
L = load('/home/claude/build/make_legal.py')
CF, REA = L['CF'], L['REA']; rows = L['rows']

# testi della lingua: ora le lingue sono cinque
P['IT']['body'] = P['IT']['body'].replace('Se scegli italiano o inglese, la scelta', 'Se scegli una lingua, la scelta')
P['EN']['body'] = P['EN']['body'].replace('If you choose Italian or English, the choice', 'If you choose a language, the choice')

PRIV = {'it': P['IT'], 'en': P['EN']}
LEG = {'it': L['IT'], 'en': L['EN']}

PRIV['es'] = dict(title='Política de privacidad – Fitosat', body='''<h1>Política de privacidad</h1>
<p class="upd">Última actualización: 23 de noviembre de 2026</p>
<p>Esta política explica cómo Fitosat trata los datos personales de quienes visitan fitosat.it o se ponen en contacto con nosotros, conforme al Reglamento (UE) 2016/679 (RGPD) y al Decreto Legislativo italiano 196/2003.</p>
<h2>Responsable del tratamiento</h2>
<p class="card">Fitosat srl – Via Lanzone 5, 20123 Milán (MI), Italia<br>Correo: <a href="mailto:info@fitosat.it">info@fitosat.it</a></p>
<h2>Qué datos tratamos</h2>
<ul>
<li><strong>Datos que nos envías.</strong> Si nos escribes mediante el formulario del programa piloto, el botón “Pruébalo gratis” o por correo: nombre, dirección de correo y la información que decidas indicar (empresa, cultivo, hectáreas, mensaje). El formulario no envía datos a ningún servidor: prepara un correo que sale de tu propio programa de correo.</li>
<li><strong>Datos de navegación.</strong> El servicio que aloja el sitio registra automáticamente datos técnicos como dirección IP, tipo de navegador, página solicitada, fecha y hora, para garantizar el funcionamiento y la seguridad del sitio.</li>
<li><strong>Preferencia de idioma.</strong> Si eliges un idioma, la elección se guarda solo en tu navegador (almacenamiento local) y no se nos envía.</li>
</ul>
<h2>Por qué los tratamos y con qué base</h2>
<ul>
<li>Responder a tus solicitudes y valorar la participación en el programa piloto: medidas precontractuales solicitadas por ti (art. 6.1.b RGPD).</li>
<li>Funcionamiento y seguridad del sitio: interés legítimo (art. 6.1.f RGPD).</li>
</ul>
<p>No usamos los datos para elaborar perfiles ni para publicidad, y no los vendemos ni los cedemos a terceros para sus propios fines.</p>
<h2>Cookies y herramientas de seguimiento</h2>
<p>El sitio no usa cookies, estadísticas de visitas ni herramientas de seguimiento de terceros. Por eso no hace falta un banner de consentimiento.</p>
<h2>Quién trata los datos por nuestra cuenta</h2>
<ul>
<li><strong>GitHub, Inc.</strong> (grupo Microsoft), que aloja el sitio y registra los datos de navegación. Sus servidores pueden estar en Estados Unidos: la transferencia se basa en las garantías previstas por el RGPD, como el Marco de Privacidad de Datos UE-EE. UU. o las cláusulas contractuales tipo.</li>
<li><strong>Aruba S.p.A.</strong>, que gestiona nuestro buzón de correo en Italia.</li>
</ul>
<h2>Durante cuánto tiempo</h2>
<p>Conservamos los correos y los datos de contacto el tiempo necesario para gestionar la solicitud y, si no surge una relación, como máximo 24 meses. El proveedor de alojamiento conserva los datos de navegación durante el tiempo técnicamente necesario.</p>
<h2>Tus derechos</h2>
<p>Puedes solicitar en cualquier momento acceder a tus datos, rectificarlos, suprimirlos, limitar su tratamiento, oponerte o recibirlos en un formato portable (arts. 15–22 RGPD), escribiendo a <a href="mailto:info@fitosat.it">info@fitosat.it</a>. También tienes derecho a presentar una reclamación ante la autoridad italiana de protección de datos, el Garante per la protezione dei dati personali (<a href="https://www.garanteprivacy.it">www.garanteprivacy.it</a>), o ante la autoridad de tu país.</p>
<h2>Cambios</h2>
<p>Podemos actualizar esta política; la fecha de arriba indica la última versión.</p>''')

PRIV['fr'] = dict(title='Politique de confidentialité – Fitosat', body='''<h1>Politique de confidentialité</h1>
<p class="upd">Dernière mise à jour : 23 novembre 2026</p>
<p>Cette politique explique comment Fitosat traite les données personnelles des personnes qui visitent fitosat.it ou nous contactent, conformément au Règlement (UE) 2016/679 (RGPD) et au décret législatif italien 196/2003.</p>
<h2>Responsable du traitement</h2>
<p class="card">Fitosat srl – Via Lanzone 5, 20123 Milan (MI), Italie<br>E-mail : <a href="mailto:info@fitosat.it">info@fitosat.it</a></p>
<h2>Quelles données nous traitons</h2>
<ul>
<li><strong>Les données que vous nous envoyez.</strong> Si vous nous écrivez via le formulaire du programme pilote, le bouton « Essayez gratuitement » ou par e-mail : nom, adresse e-mail et les informations que vous choisissez d’indiquer (entreprise, culture, hectares, message). Le formulaire n’envoie aucune donnée à un serveur : il prépare un e-mail qui part de votre propre messagerie.</li>
<li><strong>Données de navigation.</strong> Le service qui héberge le site enregistre automatiquement des données techniques comme l’adresse IP, le type de navigateur, la page demandée, la date et l’heure, afin d’assurer le fonctionnement et la sécurité du site.</li>
<li><strong>Préférence de langue.</strong> Si vous choisissez une langue, ce choix est enregistré uniquement dans votre navigateur (stockage local) et ne nous est pas transmis.</li>
</ul>
<h2>Pourquoi nous les traitons et sur quelle base</h2>
<ul>
<li>Répondre à vos demandes et évaluer votre participation au programme pilote : mesures précontractuelles prises à votre demande (art. 6.1.b RGPD).</li>
<li>Fonctionnement et sécurité du site : intérêt légitime (art. 6.1.f RGPD).</li>
</ul>
<p>Nous n’utilisons pas vos données à des fins de profilage ou de publicité, et nous ne les vendons ni ne les cédons à des tiers pour leurs propres finalités.</p>
<h2>Cookies et outils de suivi</h2>
<p>Le site n’utilise ni cookies, ni statistiques de visite, ni outils de suivi tiers. Aucun bandeau de consentement n’est donc nécessaire.</p>
<h2>Qui traite les données pour notre compte</h2>
<ul>
<li><strong>GitHub, Inc.</strong> (groupe Microsoft), qui héberge le site et enregistre les données de navigation. Ses serveurs peuvent se trouver aux États-Unis : le transfert repose sur les garanties prévues par le RGPD, comme le cadre de protection des données UE-États-Unis ou les clauses contractuelles types.</li>
<li><strong>Aruba S.p.A.</strong>, qui gère notre messagerie en Italie.</li>
</ul>
<h2>Durée de conservation</h2>
<p>Nous conservons les e-mails et les coordonnées le temps nécessaire pour traiter la demande et, si aucune relation ne s’ensuit, 24 mois au maximum. Les données de navigation sont conservées par l’hébergeur pendant la durée techniquement nécessaire.</p>
<h2>Vos droits</h2>
<p>Vous pouvez à tout moment demander à accéder à vos données, à les rectifier ou à les effacer, à en limiter le traitement, à vous y opposer ou à les recevoir dans un format portable (art. 15–22 RGPD), en écrivant à <a href="mailto:info@fitosat.it">info@fitosat.it</a>. Vous avez aussi le droit d’introduire une réclamation auprès de l’autorité italienne de protection des données, le Garante per la protezione dei dati personali (<a href="https://www.garanteprivacy.it">www.garanteprivacy.it</a>), ou auprès de l’autorité de votre pays.</p>
<h2>Modifications</h2>
<p>Nous pouvons mettre à jour cette politique ; la date en haut indique la dernière version.</p>''')

PRIV['pt'] = dict(title='Política de privacidade – Fitosat', body='''<h1>Política de privacidade</h1>
<p class="upd">Última atualização: 23 de novembro de 2026</p>
<p>Esta política explica como a Fitosat trata os dados pessoais de quem visita fitosat.it ou nos contacta, nos termos do Regulamento (UE) 2016/679 (RGPD) e do Decreto Legislativo italiano 196/2003.</p>
<h2>Responsável pelo tratamento</h2>
<p class="card">Fitosat srl – Via Lanzone 5, 20123 Milão (MI), Itália<br>E-mail: <a href="mailto:info@fitosat.it">info@fitosat.it</a></p>
<h2>Que dados tratamos</h2>
<ul>
<li><strong>Dados que nos envia.</strong> Se nos escrever através do formulário do programa piloto, do botão “Experimente grátis” ou por e-mail: nome, endereço de e-mail e as informações que decidir indicar (empresa, cultura, hectares, mensagem). O formulário não envia dados para nenhum servidor: prepara um e-mail que sai do seu próprio programa de e-mail.</li>
<li><strong>Dados de navegação.</strong> O serviço que aloja o site regista automaticamente dados técnicos como endereço IP, tipo de navegador, página pedida, data e hora, para garantir o funcionamento e a segurança do site.</li>
<li><strong>Preferência de idioma.</strong> Se escolher um idioma, a escolha fica guardada apenas no seu navegador (armazenamento local) e não nos é enviada.</li>
</ul>
<h2>Porque os tratamos e com que fundamento</h2>
<ul>
<li>Responder aos seus pedidos e avaliar a participação no programa piloto: diligências pré-contratuais a seu pedido (art. 6.º, n.º 1, al. b) do RGPD).</li>
<li>Funcionamento e segurança do site: interesse legítimo (art. 6.º, n.º 1, al. f) do RGPD).</li>
</ul>
<p>Não usamos os dados para definição de perfis nem publicidade, e não os vendemos nem os cedemos a terceiros para fins próprios.</p>
<h2>Cookies e ferramentas de rastreio</h2>
<p>O site não usa cookies, estatísticas de visitas nem ferramentas de rastreio de terceiros. Por isso não é necessário um aviso de consentimento.</p>
<h2>Quem trata os dados em nosso nome</h2>
<ul>
<li><strong>GitHub, Inc.</strong> (grupo Microsoft), que aloja o site e regista os dados de navegação. Os servidores podem situar-se nos Estados Unidos: a transferência baseia-se nas garantias previstas pelo RGPD, como o Quadro de Privacidade de Dados UE-EUA ou as cláusulas contratuais-tipo.</li>
<li><strong>Aruba S.p.A.</strong>, que gere a nossa caixa de correio em Itália.</li>
</ul>
<h2>Durante quanto tempo</h2>
<p>Conservamos os e-mails e os dados de contacto pelo tempo necessário para tratar o pedido e, se não surgir uma relação, no máximo durante 24 meses. Os dados de navegação são conservados pelo fornecedor de alojamento durante o tempo tecnicamente necessário.</p>
<h2>Os seus direitos</h2>
<p>Pode pedir a qualquer momento o acesso aos seus dados, a retificação, o apagamento, a limitação do tratamento, a oposição ou a portabilidade (arts. 15.º–22.º do RGPD), escrevendo para <a href="mailto:info@fitosat.it">info@fitosat.it</a>. Tem também o direito de apresentar reclamação à autoridade italiana de proteção de dados, o Garante per la protezione dei dati personali (<a href="https://www.garanteprivacy.it">www.garanteprivacy.it</a>), ou à autoridade do seu país.</p>
<h2>Alterações</h2>
<p>Podemos atualizar esta política; a data no topo indica a última versão.</p>''')

def leg(h1, upd, comp, items, web_h, web_p, cont_h, cont_p):
    return f'''<h1>{h1}</h1>
<p class="upd">{upd}</p>
<h2>{comp}</h2>
<dl class="card">
{rows(items)}
</dl>
<h2>{web_h}</h2>
<p>{web_p}</p>
<h2>{cont_h}</h2>
<p>{cont_p}</p>'''

MAIL = '<a href="mailto:info@fitosat.it">info@fitosat.it</a>'
LEG['es'] = dict(title='Aviso legal – Fitosat', body=leg('Aviso legal', 'Última actualización: 23 de noviembre de 2026', 'Datos de la empresa',
    [("Razón social", "Fitosat srl"), ("Domicilio social", "Via Lanzone 5, 20123 Milán (MI), Italia"),
     ("Código fiscal y NIF-IVA", CF), ("Registro Mercantil", "Milano Monza Brianza Lodi, n.º " + CF),
     ("Número REA", REA), ("Condición", "Startup innovadora inscrita en la sección especial del Registro Mercantil italiano"), ("Correo", MAIL)],
    'Sitio web', 'El sitio fitosat.it está alojado en GitHub Pages (GitHub, Inc.). No usa cookies ni herramientas de seguimiento. Para el tratamiento de los datos personales, consulta la <a href="privacy.html">política de privacidad</a>.',
    'Contenidos e imágenes', 'Los textos, gráficos y la marca Fitosat pertenecen a Fitosat srl. Las imágenes de la Tierra vista desde el espacio se han elaborado a partir de Blue Marble, de la NASA. Las imágenes de campos e hileras y los mapas de demostración son ilustraciones creadas para este sitio y no representan datos reales de clientes. Cada dato estadístico citado indica su fuente.'))
LEG['fr'] = dict(title='Mentions légales – Fitosat', body=leg('Mentions légales', 'Dernière mise à jour : 23 novembre 2026', 'Informations sur la société',
    [("Raison sociale", "Fitosat srl"), ("Siège social", "Via Lanzone 5, 20123 Milan (MI), Italie"),
     ("Code fiscal et n° TVA", CF), ("Registre des entreprises", "Milano Monza Brianza Lodi, n° " + CF),
     ("Numéro REA", REA), ("Statut", "Startup innovante inscrite dans la section spéciale du Registre des entreprises italien"), ("E-mail", MAIL)],
    'Site web', 'Le site fitosat.it est hébergé par GitHub Pages (GitHub, Inc.). Il n’utilise ni cookies ni outils de suivi. Pour le traitement des données personnelles, voir la <a href="privacy.html">politique de confidentialité</a>.',
    'Contenus et images', 'Les textes, les graphismes et la marque Fitosat appartiennent à Fitosat srl. Les images de la Terre vue de l’espace sont élaborées à partir de Blue Marble, de la NASA. Les images de parcelles et de rangs ainsi que les cartes de démonstration sont des illustrations réalisées pour ce site et ne représentent pas de données réelles de clients. Chaque donnée statistique citée indique sa source.'))
LEG['pt'] = dict(title='Informação legal – Fitosat', body=leg('Informação legal', 'Última atualização: 23 de novembro de 2026', 'Dados da empresa',
    [("Firma", "Fitosat srl"), ("Sede", "Via Lanzone 5, 20123 Milão (MI), Itália"),
     ("Código fiscal e n.º IVA", CF), ("Registo comercial", "Milano Monza Brianza Lodi, n.º " + CF),
     ("Número REA", REA), ("Estatuto", "Startup inovadora inscrita na secção especial do Registo comercial italiano"), ("E-mail", MAIL)],
    'Site', 'O site fitosat.it está alojado no GitHub Pages (GitHub, Inc.). Não usa cookies nem ferramentas de rastreio. Sobre o tratamento de dados pessoais, consulte a <a href="privacy.html">política de privacidade</a>.',
    'Conteúdos e imagens', 'Os textos, os grafismos e a marca Fitosat pertencem à Fitosat srl. As imagens da Terra vista do espaço foram elaboradas a partir do Blue Marble, da NASA. As imagens de campos e linhas e os mapas de demonstração são ilustrações criadas para este site e não representam dados reais de clientes. Cada dado estatístico citado indica a respetiva fonte.'))

LANGCSS = '''
  header nav {{ display:flex; gap:.7rem; flex-wrap:wrap; justify-content:flex-end; font-size:.9rem; }}
  header nav a {{ font-weight:400; }} header nav a[aria-current] {{ font-weight:700; text-decoration:underline; text-underline-offset:3px; }}
'''.replace('{{', '{').replace('}}', '}')

def write(kind, D, CSS):
    fn = {'privacy': 'privacy.html', 'legal': 'note-legali.html'}[kind]
    for l in LANGS:
        d = D[l]
        pre = '' if l == 'it' else '../'
        url = lambda x: 'https://fitosat.it/' + ('' if x == 'it' else x + '/') + fn
        alts = '\n'.join(f'<link rel="alternate" hreflang="{x}" href="{url(x)}">' for x in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{url("it")}">'
        rel = lambda x: (pre + ('' if x == 'it' else x + '/') + fn)
        nav = ''.join(f'<a href="{rel(x)}" hreflang="{x}" lang="{x}"' + (' aria-current="page"' if x == l else '') + f'>{x.upper()}</a>' for x in LANGS)
        html = f'''<!DOCTYPE html>
<html lang="{l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{d['title']}</title>
<link rel="canonical" href="{url(l)}">
{alts}
{P['head_assets']}
<style>{CSS}{LANGCSS}</style>
</head>
<body>
<header><a href="./">{HOME_T[l]}</a><nav aria-label="Lingua / Language">{nav}</nav></header>
<main>
{d['body']}
</main>
</body>
</html>
'''
        html = re.sub(r'(?<=["(])/?(fonts|img)/', lambda m: pre + m.group(1) + '/', html)
        os.makedirs(f'{ST}/' + ('' if l == 'it' else l), exist_ok=True)
        open(f'{ST}/' + ('' if l == 'it' else l + '/') + fn, 'w', encoding='utf-8').write(html)

write('privacy', PRIV, P['CSS'])
write('legal', LEG, L['CSS'])
print('ok')
