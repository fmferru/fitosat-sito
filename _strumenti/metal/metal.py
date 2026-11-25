import numpy as np, cv2
from PIL import Image
K = 4
src = Image.open('/home/claude/staging/img/logo-dark.png').convert('RGBA')
W, H = src.size
big = np.array(src.resize((W * K, H * K), Image.LANCZOS)).astype(np.float32) / 255
A = big[..., 3]
rgb = big[..., :3]
# occhio rosso: tonalità rossa
red = (rgb[..., 0] > rgb[..., 2] * 1.3) & (rgb[..., 0] > .35) & (A > .1)
redm = cv2.morphologyEx(red.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
n, lab, stats, cent = cv2.connectedComponentsWithStats(redm)
i = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA]); ex, ey = cent[i]; er = np.sqrt(stats[i, cv2.CC_STAT_AREA] / np.pi) * 1.05
yy, xx = np.mgrid[0:H * K, 0:W * K].astype(np.float32)
eye_d = np.hypot(xx - ex, yy - ey)
eye = eye_d < er
As = cv2.GaussianBlur(A, (0, 0), 3.2)
stroke = (As > .42) & ~(eye_d < er * 1.6)
# profilo a tubo (rilievo) dal campo di distanza
dt = cv2.distanceTransform(stroke.astype(np.uint8), cv2.DIST_L2, 5)
r = np.percentile(dt[stroke], 97)
h = cv2.GaussianBlur(stroke.astype(np.float32), (0, 0), r * .55) * r * 2.2
gy, gx = np.gradient(h)
nz = np.ones_like(h)
N = np.stack([-gx, -gy, nz], -1); N /= np.linalg.norm(N, axis=-1, keepdims=True)
# riflesso di un ambiente "da studio nello spazio": alto chiaro, banda fredda, basso scuro con luce calda della Terra
V = np.array([0, 0, 1.0])
R = 2 * N[..., 2:3] * N - V
ry = -R[..., 1]                       # verso l'alto dello schermo
env = np.interp(ry, [-1, -.35, -.05, .15, .45, 1], [.10, .22, .55, .95, .78, 1.0])
tint = np.stack([np.interp(ry, [-1, 0, 1], [.85, .92, 1.0]), np.interp(ry, [-1, 0, 1], [.82, .95, 1.0]), np.interp(ry, [-1, 0, 1], [.95, 1.05, 1.06])], -1)
col = env[..., None] * tint
# luce principale (sole) dall'alto a sinistra: riflesso speculare stretto
L = np.array([-.55, -.6, .58]); L /= np.linalg.norm(L)
Hh = (L + V); Hh /= np.linalg.norm(Hh)
spec = np.clip((N * Hh).sum(-1), 0, 1) ** 90
col = col * .92 + spec[..., None] * 1.1
# leggera variazione spazzolata lungo x
col *= (1 + .035 * np.sin(xx / 3.1 + yy / 47))[..., None]
alpha = np.clip((As - .32) / .2, 0, 1) * ~(eye_d < er * 1.6)
# occhio: lente rossa lucida con bordo metallico
d = eye_d / er
lens = d < .82
ring = (d >= .82) & (d < 1.0)
ez = np.sqrt(np.clip(1 - (d / .82) ** 2, 0, 1))
ecol = np.zeros(h.shape + (3,), np.float32)
base = np.stack([.86 - .35 * (d / .82), .06 + .02 * ez, .08 + .02 * ez], -1)
glow = np.exp(-((xx - (ex - er * .25)) ** 2 + (yy - (ey - er * .3)) ** 2) / (2 * (er * .14) ** 2))
ecol = base * (.55 + .6 * ez[..., None]) + glow[..., None] * 1.0
ringv = .35 + .6 * np.clip(np.cos((d - .91) / .09 * 1.57 + .6) * (1 - (yy - ey) / (er * 2)), 0, 1)
col = np.where(lens[..., None], ecol, col)
col = np.where(ring[..., None], ringv[..., None] * np.array([.9, .93, 1.0]), col)
alpha = np.maximum(alpha, (d < 1.0).astype(np.float32))
alpha = np.maximum(alpha, cv2.GaussianBlur((d < 1).astype(np.float32), (0, 0), .8))
# alone rosso del sensore
halo = np.exp(-np.clip(d - 1, 0, None) ** 2 / .35) * (d >= 1) * .55
out = np.zeros(h.shape + (4,), np.float32)
out[..., :3] = np.clip(col, 0, 1)
out[..., 3] = np.clip(alpha, 0, 1)
hal = np.zeros_like(out); hal[..., 0] = 1; hal[..., 1] = .18; hal[..., 2] = .2; hal[..., 3] = halo
a1 = out[..., 3:4]; a2 = hal[..., 3:4] * (1 - a1)
oa = a1 + a2
out[..., :3] = (out[..., :3] * a1 + hal[..., :3] * a2) / np.maximum(oa, 1e-4); out[..., 3:] = oa
img = Image.fromarray((out * 255).astype(np.uint8), 'RGBA')
img.resize((W * 3, H * 3), Image.LANCZOS).save('/home/claude/staging/img/logo-metal.png', optimize=True)
bg = Image.new('RGBA', (W * 2, H * 2), (8, 12, 26, 255)); bg.alpha_composite(img.resize((W * 2, H * 2), Image.LANCZOS))
bg.convert('RGB').save('/home/claude/preview/logo-metal.png')
print('ok', W * 3, H * 3)
