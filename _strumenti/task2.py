import re,base64
P='/home/claude/staging/index.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,c=1):
    global s
    assert s.count(o)==c,(s.count(o),o[:90]); s=s.replace(o,n)
b64=lambda n: base64.b64encode(open(f'/home/claude/build/bg/{n}.webp','rb').read()).decode()
m=re.search(r'      <img class="intro-bg" src="data:image/jpeg;base64,[^"]+" alt="">\n',s); assert m
layers=''.join(f'      <img class="intro-layer" data-k="{k}" src="data:image/webp;base64,{b64(n)}" alt="">\n' for k,n in enumerate(['orbit','country','rows']))
s=s[:m.start()]+layers+s[m.end():]
rep('section.intro { height: 140vh;','section.intro { height: 260vh;')
rep('''    if (curY < window.innerHeight * 1.2 || target < window.innerHeight * 1.2) render(curY);''','''    if (curY < window.innerHeight * 2 || target < window.innerHeight * 2) render(curY);''')
rep('''  function render(y) {
    var vh = window.innerHeight;''','''  var layers = Array.prototype.slice.call(document.querySelectorAll(".intro-layer"));
  function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function render(y) {
    var vh = window.innerHeight;
    var z = clamp01(y / (vh * 1.4));
    function seg(a, b) { return clamp01((z - a) / (b - a)); }
    var L = [
      [1 - seg(0.25, 0.5), 1 + 1.2 * seg(0, 0.5)],
      [seg(0.25, 0.5) * (1 - seg(0.6, 0.8)), 1.4 + 1.0 * seg(0.25, 0.8)],
      [seg(0.6, 0.8), 1.3 - 0.3 * seg(0.6, 1)]
    ];
    layers.forEach(function (el, i) { el.style.opacity = L[i][0].toFixed(3); el.style.transform = "scale(" + L[i][1].toFixed(4) + ")"; });''')
rep('''    var o = Math.min(1, Math.max(0, (y - vh * 0.12) / (vh * 0.2)));''','''    var o = seg(0.8, 0.95);''')
css='''
  /* Prima schermata: zoom dallo spazio */
  .intro-layer { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; will-change: transform, opacity; }
  .intro-layer[data-k="0"] { transform-origin: 50% 88%; }
  .intro-layer[data-k="1"], .intro-layer[data-k="2"] { opacity: 0; }
  .intro-veil { background: linear-gradient(180deg, rgba(20,12,8,0) 48%, rgba(20,12,8,.25) 60%, rgba(20,12,8,.6) 100%); }
  .intro:not(.static) .intro-slogan { top: 52%; bottom: 2.5%; justify-content: center; padding-top: .5rem; padding-bottom: .5rem; }
  .intro:not(.static) .intro-slogan h1 { font-size: clamp(1.45rem, min(5vw, 4.6vh), 3.4rem); margin-bottom: .8rem; }
  .intro:not(.static) .intro-slogan .lead { font-size: clamp(.9rem, 2vh, 1.1rem); }
  .intro:not(.static) .intro-cta { margin-top: 1.1rem; }
  .intro.static .intro-layer { opacity: 0; }
  .intro.static .intro-layer[data-k="2"] { opacity: 1; }
'''
rep('</style>',css+'</style>')
open(P,'w',encoding='utf-8').write(s)
print('ok',len(s))
