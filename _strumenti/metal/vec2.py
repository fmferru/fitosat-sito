import numpy as np, cv2, json
from PIL import Image
src = np.array(Image.open('/home/claude/staging/img/logo-dark.png').convert('RGBA'))
A = src[..., 3]; rgb = src[..., :3].astype(int)
red = (rgb[..., 0] > rgb[..., 2] * 1.3) & (rgb[..., 0] > 90) & (A > 30)
m = ((A > 100) & ~red).astype(np.uint8) * 255
K = 4
mb = cv2.resize(m, None, fx=K, fy=K, interpolation=cv2.INTER_CUBIC); mb = cv2.GaussianBlur(mb, (0, 0), 2)
circ = cv2.HoughCircles(mb, cv2.HOUGH_GRADIENT, dp=1, minDist=200, param1=120, param2=35, minRadius=90, maxRadius=170)
C = [] if circ is None else (circ[0] / K).tolist()
print('circles', np.round(C, 1).tolist())
# remove circles from mask, keep lines
rest = (m > 127).astype(np.uint8)
for x, y, r in C:
    cv2.circle(rest, (int(round(x)), int(round(y))), int(round(r)), 0, 5)
ys, xs = np.nonzero(red); ex, ey, er = xs.mean(), ys.mean(), np.sqrt(red.sum() / np.pi)
cv2.circle(rest, (int(ex), int(ey)), int(er * 1.4), 0, -1)
rb = cv2.resize(rest * 255, None, fx=K, fy=K, interpolation=cv2.INTER_CUBIC)
sk = cv2.ximgproc.thinning((rb > 127).astype(np.uint8) * 255)
L = cv2.HoughLinesP(sk, 1, np.pi / 720, threshold=30, minLineLength=60, maxLineGap=12)
segs = [] if L is None else (L.reshape(-1, 4) / K).tolist()
print('segments', len(segs))
json.dump({'circles': C, 'segs': segs, 'eye': [ex, ey, er], 'size': list(m.shape[::-1])}, open('geom.json', 'w'))
# preview reconstruction
S = 4; can = np.zeros((m.shape[0] * S, m.shape[1] * S), np.uint8)
for x, y, r in C: cv2.circle(can, (int(x * S), int(y * S)), int(r * S), 255, int(4.2 * S), cv2.LINE_AA)
for x1, y1, x2, y2 in segs: cv2.line(can, (int(x1 * S), int(y1 * S)), (int(x2 * S), int(y2 * S)), 255, int(4.2 * S), cv2.LINE_AA)
cv2.circle(can, (int(ex * S), int(ey * S)), int(er * S), 160, -1, cv2.LINE_AA)
o = np.dstack([m, cv2.resize(can, m.shape[::-1]), np.zeros_like(m)])
Image.fromarray(o).resize((m.shape[1] * 2, m.shape[0] * 2)).save('/home/claude/preview/vec-check.png')
