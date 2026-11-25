import os,sys
from PIL import Image
import numpy as np
D='/home/claude/build/img'; ok=True
for n in ['orbit','country','rows']:
    for v,size in [('l',(2400,1500)),('p',(1400,2400))]:
        p=f'{D}/{n}-{v}.webp'
        if not os.path.exists(p): print('MISSING',p); ok=False; continue
        sz=os.path.getsize(p); im=Image.open(p)
        if sz>240000: print('TOO BIG',p,sz); ok=False
        if im.size!=size: print('SIZE',p,im.size); ok=False
print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
