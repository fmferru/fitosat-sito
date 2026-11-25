"""Rimuove dichiarazioni CSS sovrascritte da una regola successiva con lo stesso selettore
nello stesso contesto (@media). Sicuro: stesso selettore = stessa specificità, la regola
successiva vince comunque; togliere quella precedente non cambia il risultato."""
import re, sys
P = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/staging/index.html'
s = open(P, encoding='utf-8').read()
a = s.index('<style>') + 7; b = s.index('</style>', a)
css = s[a:b]


def parse(block, ctx, out):
    i, n = 0, len(block)
    while i < n:
        m = re.match(r'\s+|/\*.*?\*/', block[i:], re.S)
        if m:
            out.append(('raw', block[i:i + m.end()])); i += m.end(); continue
        j = block.find('{', i)
        if j < 0:
            out.append(('raw', block[i:])); break
        d, k = 0, j
        while k < n:
            if block[k] == '{': d += 1
            elif block[k] == '}':
                d -= 1
                if d == 0: break
            k += 1
        head, body = block[i:j], block[j + 1:k]
        h = head.strip()
        if h.startswith('@media') or h.startswith('@supports'):
            inner = []
            parse(body, ctx + (re.sub(r'\s+', ' ', h),), inner)
            out.append(('at', head, inner))
        elif h.startswith('@'):
            out.append(('raw', block[i:k + 1]))
        else:
            out.append(('rule', head, ctx, re.sub(r'\s+', ' ', h), body))
        i = k + 1


def decls(body):
    parts, d, cur = [], 0, ''
    for ch in body:
        if ch == '(': d += 1
        elif ch == ')': d -= 1
        if ch == ';' and d == 0:
            parts.append(cur); cur = ''
        else:
            cur += ch
    if cur.strip(): parts.append(cur)
    res = []
    for p in parts:
        if not p.strip(): continue
        if ':' not in p or p.strip().startswith('@'):
            return None  # nested or odd: leave untouched
        prop = p.split(':', 1)[0].strip().lower()
        res.append((prop, p, '!important' in p))
    return res


tree = []
parse(css, (), tree)
flat = []
def walk(t):
    for x in t:
        if x[0] == 'rule': flat.append(x)
        elif x[0] == 'at': walk(x[2])
walk(tree)

# for each rule, which properties are overridden later by identical (ctx, selector)
info = {}
for idx, r in enumerate(flat):
    info[id(r)] = decls(r[4])
removed = 0
newbody = {}
for idx, r in enumerate(flat):
    ds = info[id(r)]
    if ds is None: continue
    later = {}
    for r2 in flat[idx + 1:]:
        if r2[2] == r[2] and r2[3] == r[3] and info[id(r2)] is not None:
            for prop, _, imp in info[id(r2)]:
                later[prop] = later.get(prop, False) or imp
    # vendor/fallback pairs (same prop twice in one rule, e.g. height:100vh;height:100svh) are kept
    keep = []
    for prop, txt, imp in ds:
        if prop in later and (later[prop] or not imp) and not prop.startswith('--'):
            removed += 1; continue
        keep.append(txt)
    if len(keep) != len(ds):
        newbody[id(r)] = (';'.join(keep) + ('; ' if keep else '')) if keep else ''


def emit(t):
    o = []
    for x in t:
        if x[0] == 'raw': o.append(x[1])
        elif x[0] == 'at':
            inner = emit(x[2])
            if re.sub(r'\s|/\*.*?\*/', '', inner, flags=re.S): o.append(x[1] + '{' + inner + '}')
        else:
            body = newbody.get(id(x), x[4])
            if body.strip(): o.append(x[1] + '{' + body + '}')
    return ''.join(o)


new = emit(tree)
new = re.sub(r'\n\s*\n+', '\n', new)
s = s[:a] + new + s[b:]
open(P, 'w', encoding='utf-8').write(s)
print('declarations removed:', removed, 'css', len(css), '->', len(new))
