import numpy as np, cv2, json
from PIL import Image
src = np.array(Image.open('/home/claude/staging/img/logo-dark.png').convert('RGBA'))
A = src[..., 3]; rgb = src[..., :3].astype(int)
red = (rgb[..., 0] > rgb[..., 2] * 1.3) & (rgb[..., 0] > 90) & (A > 30)
m = ((A > 100) & ~red).astype(np.uint8) * 255
K = 4
mb = cv2.resize(m, None, fx=K, fy=K, interpolation=cv2.INTER_CUBIC)
mb = cv2.GaussianBlur(mb, (0, 0), 2)
circ = cv2.HoughCircles(mb, cv2.HOUGH_GRADIENT, dp=1, minDist=150, param1=120, param2=40, minRadius=70, maxRadius=110)
print('circles', None if circ is None else np.round(circ[0] / K, 1).tolist())
# skeleton
sk = cv2.ximgproc.thinning((mb > 127).astype(np.uint8) * 255) if hasattr(cv2, 'ximgproc') else None
print('ximgproc', sk is not None)
dt = cv2.distanceTransform((m > 127).astype(np.uint8), cv2.DIST_L2, 5); print('stroke half-width px', np.percentile(dt[m > 127], [50, 90, 99]))
ys, xs = np.nonzero(red); print('eye', xs.mean(), ys.mean(), np.sqrt(red.sum() / np.pi))
