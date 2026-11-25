"""Genera i tre sfondi della prima schermata (orbita, campagna, filari+terra)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1600, 1000
OUT = '/home/claude/build/bg'
rng = np.random.default_rng(11)


def noise(w, h, octaves=6, base=4, seed=0):
    r = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        n = base * 2 ** o
        g = r.random((n + 1, int(n * w / h) + 2)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        acc += np.asarray(im, np.float32) / 255 * amp; tot += amp; amp *= 0.5
    return acc / tot


def save(arr, name, q=72):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(f'{OUT}/{name}.webp', quality=q, method=6)


# ---------- 1. orbita ----------
def orbit():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    img = np.zeros((H, W, 3), np.float32)
    img[:] = np.array([8, 9, 18])
    # stelle
    for _ in range(700):
        sx, sy = rng.integers(0, W), rng.integers(0, int(H * 0.6))
        b = rng.random() ** 3 * 255
        img[sy, sx] = np.maximum(img[sy, sx], b)
    # Terra: cerchio enorme, bordo curvo nella parte bassa
    cx, cy, R = W * 0.5, H * 2.6, H * 1.75
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    inside = d < R
    n = noise(W, H, 6, 3, seed=5)
    land = n > 0.52
    sea = np.stack([18 + 25 * n, 42 + 40 * n, 78 + 50 * n], -1)
    ground = np.stack([70 + 60 * n, 88 + 55 * n, 52 + 30 * n], -1)
    lm = np.clip((n - 0.5) * 25, 0, 1)[..., None]
    surf = sea * (1 - lm) + ground * lm
    cl = noise(W, H, 6, 5, seed=9)
    cloud = np.clip((cl - 0.55) * 4, 0, 1)[..., None]
    surf = surf * (1 - cloud * 0.85) + 235 * cloud * 0.85
    # ombreggiatura verso il bordo
    limb = np.clip((R - d) / (H * 0.35), 0, 1)[..., None]
    surf = surf * (0.35 + 0.65 * limb)
    img = np.where(inside[..., None], surf, img)
    # atmosfera
    glow = np.exp(-((d - R) / 18) ** 2)[..., None] * np.array([110, 170, 255])
    halo = np.exp(-np.clip(d - R, 0, None) / 60)[..., None] * np.array([40, 70, 140]) * (d > R)[..., None]
    img = img + glow * 0.9 + halo
    save(img, 'orbit')


# ---------- 2. campagna dall'alto ----------
def country():
    S = 2
    im = Image.new('RGB', (W * S, H * S), (96, 104, 62))
    d = ImageDraw.Draw(im)
    cols = [(104, 122, 64), (126, 136, 72), (150, 140, 88), (88, 110, 58), (170, 150, 100), (112, 96, 66), (78, 98, 52)]
    r = np.random.default_rng(3)
    gx = np.linspace(-200, W * S + 200, 13); gy = np.linspace(-200, H * S + 200, 10)
    P = np.stack(np.meshgrid(gx, gy), -1) + r.normal(0, 45, (len(gy), len(gx), 2))
    edges = []
    for i in range(len(gy) - 1):
        for j in range(len(gx) - 1):
            poly = [tuple(P[i, j]), tuple(P[i, j + 1]), tuple(P[i + 1, j + 1]), tuple(P[i + 1, j])]
            c = cols[r.integers(0, len(cols))]
            d.polygon(poly, fill=c)
            if r.random() < 0.6:  # righe di coltivazione, ritagliate sul campo
                lay = Image.new('RGB', im.size, c); ld = ImageDraw.Draw(lay)
                m = Image.new('L', im.size, 0); ImageDraw.Draw(m).polygon(poly, fill=255)
                cx = np.mean([p[0] for p in poly]); cy = np.mean([p[1] for p in poly])
                ang = r.random() * np.pi; dk = (np.cos(ang), np.sin(ang))
                for k in range(-30, 31):
                    ox, oy = -dk[1] * 10 * k, dk[0] * 10 * k
                    ld.line([(cx + ox - dk[0] * 400, cy + oy - dk[1] * 400), (cx + ox + dk[0] * 400, cy + oy + dk[1] * 400)],
                            fill=tuple(int(v * 0.84) for v in c), width=4)
                im.paste(lay, (0, 0), m)
            edges += [(poly[0], poly[1]), (poly[1], poly[2])]
    d = ImageDraw.Draw(im)
    for e in edges:
        d.line(e, fill=(84, 92, 56), width=5)
        if r.random() < 0.18:  # siepi e filari di alberi lungo i confini
            (x0, y0), (x1, y1) = e
            for t in np.linspace(0, 1, 26):
                px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
                rr = 8 + r.random() * 6
                d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(54, 74, 40))
    # una strada che segue i confini
    i = len(gy) // 2
    d.line([tuple(P[i, j]) for j in range(len(gx))], fill=(190, 178, 148), width=9)
    im = im.filter(ImageFilter.GaussianBlur(1.6)).resize((W, H), Image.LANCZOS)
    a = np.asarray(im, np.float32)
    a = a * (0.9 + 0.2 * noise(W, H, 5, 6, seed=2)[..., None])
    save(a, 'country')


# ---------- 3. filari sopra, terra arata sotto ----------
def rows():
    S = 2
    im = Image.new('RGB', (W * S, H * S), (122, 98, 72))
    d = ImageDraw.Draw(im)
    r = np.random.default_rng(7)
    split = int(H * S * 0.5)
    # filari
    y = 18
    while y < split - 10:
        d.rectangle([0, y + 12, W * S, y + 22], fill=(138, 132, 82))  # erba nell'interfila
        x = -10
        while x < W * S + 20:
            rad = 13 + r.random() * 6
            g = [(79, 110, 51), (93, 125, 59), (106, 138, 68), (87, 118, 54)][r.integers(0, 4)]
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=g)
            x += 21 + r.random() * 6
        y += 46
    # terra arata
    d.rectangle([0, split, W * S, H * S], fill=(74, 52, 38))
    yy = split
    while yy < H * S:
        c = [(90, 64, 48), (63, 44, 32), (99, 70, 52)][r.integers(0, 3)]
        pts = [(x, yy + 3 * np.sin(x / 140 + yy)) for x in range(0, W * S + 40, 40)]
        d.line(pts, fill=c, width=9)
        yy += 17
    im = im.filter(ImageFilter.GaussianBlur(1.2)).resize((W, H), Image.LANCZOS)
    a = np.asarray(im, np.float32)
    a = a * (0.88 + 0.24 * noise(W, H, 5, 8, seed=4)[..., None])
    # bordo morbido tra filari e terra
    yv = np.arange(H)[:, None, None]
    band = np.clip(1 - np.abs(yv - H * 0.5) / (H * 0.03), 0, 1)
    a = a * (1 - 0.25 * band)
    # terra più scura verso il basso, per leggibilità dello slogan
    shade = np.clip((yv - H * 0.5) / (H * 0.5), 0, 1)
    a = a * (1 - 0.35 * shade)
    save(a, 'rows')


if __name__ == '__main__':
    orbit(); country(); rows()
