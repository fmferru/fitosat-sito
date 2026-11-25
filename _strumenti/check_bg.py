import os,sys
from PIL import Image
import numpy as np
D='/home/claude/build/bg'; ok=True
for n in ['orbit','country','rows']:
    p=f'{D}/{n}.webp'
    if not os.path.exists(p): print('MISSING',p); ok=False; continue
    sz=os.path.getsize(p); im=Image.open(p)
    if sz>140000: print('TOO BIG',n,sz); ok=False
    if im.size!=(1600,1000): print('SIZE',n,im.size); ok=False
    if n=='rows':
        a=np.asarray(im.convert('RGB')).astype(float); top,bot=a[:500],a[500:]
        if not top[...,1].mean()>bot[...,1].mean()+15: print('rows green top/bot',top[...,1].mean(),bot[...,1].mean()); ok=False
        lum=(bot@[.299,.587,.114]).mean()
        if not lum<90: print('bottom lum',lum); ok=False
print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
