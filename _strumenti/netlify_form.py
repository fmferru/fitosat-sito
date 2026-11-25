import sys
for path in ['index.html','en/index.html']:
    s=open(path,encoding='utf-8').read()
    old='<form class="pilot-form" id="pilotForm" action="/contatto.php" method="post" novalidate>'
    assert s.count(old)==1
    s=s.replace(old,'<form class="pilot-form" id="pilotForm" name="pilota" action="/" method="post" data-netlify="true" netlify-honeypot="sito" novalidate>\n          <input type="hidden" name="form-name" value="pilota">\n          <input type="hidden" name="lingua" value="">\n          <input type="hidden" name="subject" value="Programma pilota – nuova richiesta dal sito">')
    old2='''      var data = new FormData(f); data.append("lingua", lang);
      fetch(f.getAttribute("action"), { method: "POST", body: data, headers: { "Accept": "application/json" } })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) {
          btn.disabled = false;
          if (j && j.ok) {'''
    assert s.count(old2)==1
    s=s.replace(old2,'''      f.elements.lingua.value = lang;
      var data = new URLSearchParams(new FormData(f)).toString();
      fetch("/", { method: "POST", body: data, headers: { "Content-Type": "application/x-www-form-urlencoded" } })
        .then(function (r) {
          btn.disabled = false;
          if (r.ok) {''')
    open(path,'w',encoding='utf-8').write(s)
print('ok')
