"""Blocco di vigneto sospeso, assonometria, con i 5 casi d'uso."""
import json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 2
W, H = 1400, 960
S = 52 * SS
EX = np.array([0.92, 0.30]) * S       # lungo i filari
EY = np.array([-0.60, 0.42]) * S      # tra i filari
EZ = np.array([0.0, -1.0]) * S * 0.92
NR, L, SP = 10, 16.0, 0.5
X0, X1, Y0, Y1 = -0.9, L + 0.9, -0.75, NR - 0.25
T = 2.4
rng = np.random.default_rng(11)

# centra il blocco nella tela
def raw(x, y, z=0.0): return x * EX + y * EY + z * EZ
cs = np.array([raw(x, y, z) for x in (X0, X1) for y in (Y0, Y1) for z in (0, -T, 1.2)])
lo, hi = cs.min(0), cs.max(0)
ORIG = np.array([W * SS, H * SS]) / 2 - (lo + hi) / 2 + np.array([0, -10 * SS])
def P(x, y, z=0.0):
    p = ORIG + raw(x, y, z); return (float(p[0]), float(p[1]))

img = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))

# ombra morbida sotto il blocco
sh = Image.new('L', img.size, 0)
base = [P(X0, Y0, -T), P(X1, Y0, -T), P(X1, Y1, -T), P(X0, Y1, -T)]
c = np.mean(base, 0)
ImageDraw.Draw(sh).polygon([((x - c[0]) * .78 + c[0], (y - c[1]) * .45 + c[1] + 70 * SS) for x, y in base], fill=70)
sh = sh.filter(ImageFilter.GaussianBlur(34 * SS))
sl = Image.new('RGBA', img.size, (70, 52, 56, 0)); sl.putalpha(sh)
img = Image.alpha_composite(img, sl); d = ImageDraw.Draw(img)

# fianchi: fasce di terreno
STRATA = [(0.0, (96, 134, 60)), (0.12, (84, 60, 42)), (0.75, (122, 88, 60)), (1.45, (156, 120, 82)), (2.0, (172, 142, 104))]
def face(edge, shade, seed):
    r = np.random.default_rng(seed)
    ts = np.linspace(0, 1, 200)
    bottom = T + 0.10 * np.sin(ts * 13 + seed) + 0.05 * np.sin(ts * 41) + np.cumsum(r.normal(0, .02, len(ts)))
    bounds = [np.zeros_like(ts)]
    for k, (dep, col) in enumerate(STRATA[1:], 1):
        bounds.append(np.minimum(dep + 0.09 * np.sin(ts * (4 + 2 * k) + k) + 0.03 * np.sin(ts * 37 + k), bottom))
    bounds.append(bottom)
    for k, (dep, col) in enumerate(STRATA):
        poly = [P(*edge(t), -z) for t, z in zip(ts, bounds[k])] + [P(*edge(t), -z) for t, z in zip(ts[::-1], bounds[k + 1][::-1])]
        d.polygon(poly, fill=tuple(int(v * shade) for v in col) + (255,))
    for _ in range(70):
        t = r.random(); z = r.uniform(0.85, T - 0.2)
        if z > np.interp(t, ts, bottom) - 0.12: continue
        x, y = P(*edge(t), -z); rr = r.uniform(1.5, 4.5) * SS; g = int(r.uniform(165, 205) * shade)
        d.ellipse([x - rr, y - rr * .7, x + rr, y + rr * .7], fill=(g, g - 10, g - 22, 255))
    for _ in range(26):
        t = r.random(); x, y = P(*edge(t), -0.13); pts = [(x, y)]
        for i in range(5):
            x += r.normal(0, 2.2) * SS; y += r.uniform(3, 7) * SS; pts.append((x, y))
        d.line(pts, fill=(int(58 * shade), int(40 * shade), int(28 * shade), 255), width=SS)
face(lambda t: (X0 + t * (X1 - X0), Y1), 1.0, 1)
face(lambda t: (X1, Y1 - t * (Y1 - Y0)), 0.8, 2)

# superficie: erba con interfile
top_poly = [P(X0, Y0), P(X1, Y0), P(X1, Y1), P(X0, Y1)]
d.polygon(top_poly, fill=(120, 156, 72, 255))
for r in range(NR + 1):
    y = r - 0.5
    d.polygon([P(X0 + .25, y - .3), P(X1 - .25, y - .3), P(X1 - .25, y + .3), P(X0 + .25, y + .3)],
              fill=(132, 166, 80, 255) if r % 2 else (114, 150, 66, 255))
for r in range(NR):
    d.polygon([P(-0.25, r - .17), P(L + .25, r - .17), P(L + .25, r + .3), P(-0.25, r + .3)], fill=(140, 110, 74, 255))
arr = np.array(img).astype(np.int16)
m = Image.new('L', img.size, 0); ImageDraw.Draw(m).polygon(top_poly, fill=255); m = np.array(m) > 0
nz = rng.normal(0, 6, m.shape)
for ch in range(3): arr[..., ch][m] += nz[m].astype(np.int16)
img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)

# zona di vendemmia: tinta al suolo
ZR0, ZR1, ZX0, ZX1 = 7.5, 9.45, 10.0, 15.9
zl = Image.new('RGBA', img.size, (0, 0, 0, 0))
ImageDraw.Draw(zl).polygon([P(ZX0, ZR0), P(ZX1, ZR0), P(ZX1, ZR1), P(ZX0, ZR1)], fill=(140, 84, 168, 80))
img = Image.alpha_composite(img, zl); d = ImageDraw.Draw(img)

# filari a siepe
VIG_ROW, GAP_ROW = 1, 4
GAPS = {7, 8, 9, 10, 19, 20, 21}
def col_at(r, x):
    c = np.array([58, 110, 46], float)
    s = math.exp(-(((x - 2.5) / 3.2) ** 2 + ((r - 8.2) / 1.5) ** 2))
    c = c * (1 - .8 * s) + np.array([184, 170, 72]) * .8 * s
    if r == VIG_ROW and x >= 5:
        f = min(1, (x - 5) / 9); w = min(1, (x - 5) / 1.5)
        hot = np.array([238, 152, 54]) * (1 - f) + np.array([212, 56, 46]) * f
        c = c * (1 - w) + hot * w
    return c
HW, Z0, Z1 = 0.19, 0.38, 1.05
def C(c, k): return tuple(int(v) for v in np.clip(c * k, 0, 255)) + (255,)
for r in range(NR):
    # ombra della siepe sul lato davanti
    d.polygon([P(-.1, r + HW, 0), P(L + .1, r + HW, 0), P(L + .3, r + HW + .32, 0), P(.1, r + HW + .32, 0)], fill=(70, 86, 44, 255))
    n = int(L / SP)
    for i in range(n):
        x0, x1 = i * SP, (i + 1) * SP
        xm = (x0 + x1) / 2
        if r == GAP_ROW and i in GAPS:
            d.line([P(xm, r, 0), P(xm, r, .3)], fill=(92, 66, 46, 255), width=3 * SS)
            continue
        c = col_at(r, xm) * rng.uniform(.93, 1.07)
        d.line([P(xm, r + HW, 0), P(xm, r + HW, Z0)], fill=(84, 60, 42, 255), width=2 * SS)      # tronco
        d.polygon([P(x0, r + HW, Z0), P(x1, r + HW, Z0), P(x1, r + HW, Z1), P(x0, r + HW, Z1)], fill=C(c, .78))
        d.polygon([P(x0, r - HW, Z1), P(x1, r - HW, Z1), P(x1, r + HW, Z1), P(x0, r + HW, Z1)], fill=C(c, 1.08))
        for _ in range(5):  # foglie
            xx = rng.uniform(x0, x1); zz = rng.uniform(Z0 + .05, Z1); cx, cy = P(xx, r + HW, zz); R = rng.uniform(3, 6) * SS
            d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=C(c, rng.uniform(.7, .95)))
        for _ in range(3):
            xx = rng.uniform(x0, x1); yy = rng.uniform(r - HW, r + HW); cx, cy = P(xx, yy, Z1 + .03); R = rng.uniform(3, 6) * SS
            d.ellipse([cx - R, cy - R * .7, cx + R, cy + R * .7], fill=C(c, rng.uniform(1.0, 1.2)))
        if ZR0 - .3 <= r <= ZR1 and ZX0 <= xm <= ZX1 and i % 2 == 0:   # grappoli sul lato davanti
            gx, gy = P(xm + rng.uniform(-.06, .06), r + HW + .02, Z1 - .2)
            for k, (dx, dy) in enumerate([(-3, -4), (0, -4.5), (3, -4), (-1.5, -1), (1.5, -1), (0, 2), (-3, -1.5), (3, -1.5)]):
                rr = 3.4 * SS
                cx, cy = gx + dx * SS * 1.5, gy + dy * SS * 1.5 + 8 * SS
                d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(88, 40, 92, 255) if k % 3 else (112, 58, 120, 255))
            d.ellipse([gx - 5 * SS, gy + 1 * SS, gx - 2 * SS, gy + 4 * SS], fill=(196, 160, 206, 255))
            d.line([(gx, gy - 1 * SS), (gx + 2 * SS, gy - 6 * SS)], fill=(96, 120, 50, 255), width=2 * SS)
    for x in (-0.3, L + 0.3):   # pali di testata
        d.line([P(x, r, 0), P(x, r, 1.25)], fill=(156, 128, 92, 255), width=2 * SS)

# recinto tratteggiato della zona
def dashed(a, b, col, dash=11 * SS, gap=7 * SS, w=2 * SS):
    a, b = np.array(a), np.array(b); n = np.linalg.norm(b - a); u = (b - a) / n; s = 0
    while s < n:
        e = min(s + dash, n); d.line([tuple(a + u * s), tuple(a + u * e)], fill=col, width=w); s = e + gap
zc = [P(ZX0, ZR0 - .3, 1.3), P(ZX1, ZR0 - .3, 1.3), P(ZX1, ZR1, 1.3), P(ZX0, ZR1, 1.3)]
for k in range(4): dashed(zc[k], zc[(k + 1) % 4], (246, 236, 252, 255))

# spilli: controlli mirati
PINS = [(VIG_ROW, 11.0), (8, 2.6)]
for r, x in PINS:
    a, b = P(x, r, Z1), P(x, r, 2.15)
    d.line([a, b], fill=(120, 96, 62, 255), width=2 * SS)
    R = 8 * SS
    d.ellipse([b[0] - R, b[1] - R, b[0] + R, b[1] + R], fill=(214, 170, 84, 255), outline=(255, 248, 228, 255), width=2 * SS)

out = img.resize((W, H), Image.LANCZOS)
bb = out.getbbox(); print('bbox', bb)
cx0, cy0 = max(0, bb[0] - 12), max(0, bb[1] - 20)
out = out.crop((cx0, cy0, min(W, bb[2] + 12), min(H, bb[3] + 10)))
off = cy0; HH = out.size[1]; WW = out.size[0]
out.save('vine3d.png')
an = {'vigoria': P(7.0, VIG_ROW, Z1), 'fallanze': P(4.4, GAP_ROW, 0.6), 'vendemmia': zc[1],
      'stress': P(2.0, 8.2, Z1), 'controlli': P(11.0, VIG_ROW, 2.15)}
json.dump({k: [round((v[0] / SS - cx0) / WW * 100, 1), round((v[1] / SS - off) / HH * 100, 1)] for k, v in an.items()},
          open('anchors.json', 'w'))
print(out.size, open('anchors.json').read())
