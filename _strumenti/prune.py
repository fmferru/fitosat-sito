import re,json,sys
P='/home/claude/staging/index.html'
s=open(P,encoding='utf-8').read()
a=s.index('<style>')+7; b=s.index('</style>')
css=s[a:b]; rest=s[:a]+s[b:]
rest_nob64=re.sub(r'base64,[A-Za-z0-9+/=]+','',rest)
words=set(re.findall(r'[A-Za-z_][\w-]*',rest_nob64))
removed=[]
def sel_dead(sel):
    toks=re.findall(r'\.([A-Za-z_][\w-]*)',re.sub(r'\[[^\]]*\]|url\([^)]*\)','',sel))+re.findall(r'#([A-Za-z_][\w-]*)',sel)
    return any(t not in words for t in toks)
def split_top(h):
    out=[];d=0;cur=''
    for ch in h:
        if ch=='(':d+=1
        elif ch==')':d-=1
        if ch==',' and d==0: out.append(cur);cur=''
        else: cur+=ch
    out.append(cur); return out
def process(block):
    out=[];i=0;n=len(block)
    while i<n:
        # skip whitespace/comments
        m=re.match(r'\s+|/\*.*?\*/',block[i:],re.S)
        if m: out.append(m.group(0)); i+=m.end(); continue
        j=block.find('{',i)
        if j<0: out.append(block[i:]); break
        head=block[i:j]
        # find matching brace
        depth=0;k=j
        while k<n:
            if block[k]=='{':depth+=1
            elif block[k]=='}':
                depth-=1
                if depth==0:break
            k+=1
        body=block[j+1:k]
        h=head.strip()
        if h.startswith('@media') or h.startswith('@supports'):
            inner=process(body)
            if re.sub(r'\s|/\*.*?\*/','',inner,flags=re.S): out.append(head+'{'+inner+'}')
            else: removed.append(h[:60]+' (empty)')
        elif h.startswith('@'):
            out.append(block[i:k+1])
        else:
            sels=[x.strip() for x in split_top(h)]
            keep=[x for x in sels if not sel_dead(x)]
            if not keep: removed.append(h[:90])
            else:
                if len(keep)<len(sels): removed.append('partial: '+', '.join(x for x in sels if x not in keep)[:90])
                lead=re.match(r'\s*',head).group(0)
                out.append(lead+', '.join(keep)+' {'+body+'}')
        i=k+1
    return ''.join(out)
newcss=process(css)
# collapse blank lines
newcss=re.sub(r'\n\s*\n+','\n',newcss)
s=s[:a]+newcss+s[b:]
open(P,'w',encoding='utf-8').write(s)
print('css',len(css),'->',len(newcss),'rules removed/partial:',len(removed))
open('/home/claude/build/pruned.txt','w').write('\n'.join(removed))
