import numpy as np, cv2, potrace, cairosvg, io
from PIL import Image
src = Image.open('/home/claude/staging/img/logo-dark.png').convert('RGBA')
W, H = src.size; K = 4
a = np.array(src).astype(np.float32) / 255
A = cv2.resize(a[..., 3], (W * K, H * K), interpolation=cv2.INTER_CUBIC)
A = cv2.GaussianBlur(A, (0, 0), 2.6)
bm = potrace.Bitmap(A > .36)
plist = bm.trace(turdsize=20, alphamax=1.15, opticurve=True, opttolerance=.4)
d = []
for c in plist:
    d.append('M %f %f' % (c.start_point.x, c.start_point.y))
    for seg in c.segments:
        if seg.is_corner: d.append('L %f %f L %f %f' % (seg.c.x, seg.c.y, seg.end_point.x, seg.end_point.y))
        else: d.append('C %f %f %f %f %f %f' % (seg.c1.x, seg.c1.y, seg.c2.x, seg.c2.y, seg.end_point.x, seg.end_point.y))
    d.append('Z')
svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d"><path fill-rule="evenodd" d="%s" fill="#fff"/></svg>' % (W * K, H * K, ' '.join(d))
open('logo-trace.svg', 'w').write(svg)
S = 8  # rasterizza a 8x l'originale
png = cairosvg.svg2png(bytestring=svg.encode(), output_width=W * S, output_height=H * S)
m = np.array(Image.open(io.BytesIO(png)).convert('RGBA'))[..., 3]
np.save('mask8.npy', m); print('mask', m.shape, len(plist), 'paths')
