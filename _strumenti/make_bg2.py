"""Sfondi ad alta definizione per la prima schermata.
Per ogni scena: versione orizzontale (2400x1500) e verticale (1400x2400).
Rendering a 1.5x e riduzione LANCZOS per bordi puliti."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = '/home/claude/build/img'
SS = 1.5  # supersampling


def noise(w, h, octaves=7, base=3, seed=0, persist=0.5):
    r = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        n = base * 2 ** o
        gh = n + 2; gw = max(2, int(n * w / h) + 2)
        g = r.random((gh, gw)).astype(np.float32)
        im = Image.fromarray(g, 'F').resize((w, h), Image.BICUBIC)
        acc += np.asarray(im, np.float32) * amp; tot += amp; amp *= persist
    a = acc / tot
    return (a - a.min()) / (a.max() - a.min() + 1e-6)


def finish(arr, W, H, name, q):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    im.save(f'{OUT}/{name}.webp', quality=q, method=6)


# ---------------- orbita ----------------
def orbit(W, H, name, limb_frac=0.80):
    w, h = int(W * SS), int(H * SS)
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    img = np.zeros((h, w, 3), np.float32) + np.array([6, 7, 15], np.float32)
    r = np.random.default_rng(1)
    n_st = int(w * h / 2500)
    sx = r.integers(0, w, n_st); sy = r.integers(0, h, n_st); sb = r.random(n_st) ** 4 * 255
    img[sy, sx] = np.maximum(img[sy, sx], sb[:, None])
    # pianeta: bordo curvo, curvatura legata alla larghezza
    R = max(w, h) * 1.35
    cx, cy = w * 0.5, h * limb_frac + R
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    inside = d < R
    # coordinate "sferiche" per stirare la texture verso il bordo
    t = np.clip((R - d) / (h * (1 - limb_frac) + 1), 0, 1)
    sq = 0.25 + 0.75 * t
    n = noise(w, h, 8, 3, seed=21)
    det = noise(w, h, 6, 24, seed=22)
    land = np.clip((n + 0.12 * det - 0.55) * 18, 0, 1)
    shallow = np.clip((n - 0.47) * 12, 0, 1) * (1 - land)
    ocean = np.stack([10 + 18 * det, 34 + 30 * det, 74 + 40 * det], -1)
    ocean = ocean * (1 - shallow[..., None]) + np.array([40, 120, 150]) * shallow[..., None]
    lv = noise(w, h, 7, 10, seed=23)
    green = np.stack([58 + 40 * lv, 86 + 44 * lv, 44 + 22 * lv], -1)
    dry = np.stack([150 + 40 * lv, 128 + 30 * lv, 88 + 20 * lv], -1)
    mix = np.clip((noise(w, h, 5, 4, seed=24) - 0.45) * 3, 0, 1)[..., None]
    ground = green * (1 - mix) + dry * mix
    # rilievo
    gy, gx = np.gradient(det)
    relief = np.clip(1 + (gx - gy) * 120, 0.75, 1.25)[..., None]
    surf = ocean * (1 - land[..., None]) + ground * relief * land[..., None]
    cl = noise(w, h, 8, 6, seed=25, persist=0.55)
    cloud = np.clip((cl - 0.56) * 5, 0, 1) ** 1.2
    cloud = cloud[..., None]
    surf = surf * (1 - 0.9 * cloud) + np.array([236, 240, 246]) * 0.9 * cloud
    shade = (0.3 + 0.7 * np.sqrt(t))[..., None]
    surf = surf * shade
    img = np.where(inside[..., None], surf, img)
    glow = np.exp(-((d - R) / (h * 0.012)) ** 2)[..., None] * np.array([120, 185, 255])
    halo = np.exp(-np.clip(d - R, 0, None) / (h * 0.05))[..., None] * np.array([40, 75, 150]) * (d > R)[..., None]
    img = img + glow * 0.95 + halo
    finish(img, W, H, name, 80)


# ---------------- campagna ----------------
def country(W, H, name, seed=3):
    w, h = int(W * SS), int(H * SS)
    r = np.random.default_rng(seed)
    base = Image.new('RGB', (w, h), (98, 108, 64))
    d = ImageDraw.Draw(base)
    palette = [(108, 128, 66), (128, 140, 74), (156, 146, 92), (90, 114, 60), (176, 158, 106), (118, 100, 70), (80, 102, 54), (140, 150, 84)]
    cell = int(max(w, h) / 11)
    nx, ny = w // cell + 3, h // cell + 3
    gx = np.arange(nx) * cell - cell; gy = np.arange(ny) * cell - cell
    P = np.stack(np.meshgrid(gx, gy), -1).astype(np.float32) + r.normal(0, cell * 0.16, (ny, nx, 2))
    rowlayer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for i in range(ny - 1):
        for j in range(nx - 1):
            poly = [tuple(P[i, j]), tuple(P[i, j + 1]), tuple(P[i + 1, j + 1]), tuple(P[i + 1, j])]
            c = palette[r.integers(0, len(palette))]
            d.polygon(poly, fill=c)
            if r.random() < 0.65:
                m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
                lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
                cx = np.mean([p[0] for p in poly]); cy = np.mean([p[1] for p in poly])
                ang = r.random() * np.pi; ux, uy = np.cos(ang), np.sin(ang)
                sp = 7 * SS
                dark = tuple(int(v * 0.8) for v in c) + (255,)
                for k in range(-int(cell / sp), int(cell / sp) + 1):
                    ox, oy = -uy * sp * k, ux * sp * k
                    ld.line([(cx + ox - ux * cell, cy + oy - uy * cell), (cx + ox + ux * cell, cy + oy + uy * cell)], fill=dark, width=max(2, int(2.4 * SS)))
                rowlayer.paste(lay, (0, 0), m)
    base.paste(rowlayer, (0, 0), rowlayer)
    d = ImageDraw.Draw(base)
    # confini, siepi con chiome ombreggiate
    trees = []
    for i in range(ny):
        for j in range(nx):
            for (a, b) in [((i, j), (i, j + 1)), ((i, j), (i + 1, j))]:
                if b[0] >= ny or b[1] >= nx: continue
                p0, p1 = P[a], P[b]
                d.line([tuple(p0), tuple(p1)], fill=(86, 92, 58), width=int(3 * SS))
                if r.random() < 0.22:
                    L = np.hypot(*(p1 - p0)); k = int(L / (11 * SS))
                    for t in np.linspace(0, 1, max(k, 2)):
                        trees.append((p0 + (p1 - p0) * t + r.normal(0, 2 * SS, 2), (7 + r.random() * 5) * SS))
    for _ in range(int(nx * ny * 0.6)):  # alberi sparsi e cascine
        trees.append((np.array([r.random() * w, r.random() * h]), (6 + r.random() * 6) * SS))
    for (p, rr) in trees:  # ombre
        d.ellipse([p[0] - rr + 3 * SS, p[1] - rr + 4 * SS, p[0] + rr + 3 * SS, p[1] + rr + 4 * SS], fill=(52, 58, 36))
    for (p, rr) in trees:
        d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=(48, 70, 36))
        d.ellipse([p[0] - rr * 0.65, p[1] - rr * 0.75, p[0] + rr * 0.25, p[1] + rr * 0.15], fill=(70, 96, 48))
    # strada sterrata lungo i confini
    i = ny // 2
    pts = [tuple(P[i, j]) for j in range(nx)]
    d.line(pts, fill=(176, 164, 136), width=int(9 * SS)); d.line(pts, fill=(196, 184, 154), width=int(6 * SS))
    a = np.asarray(base, np.float32)
    a = a * (0.92 + 0.16 * noise(w, h, 6, 8, seed=seed + 5)[..., None])
    finish(a, W, H, name, 70)


# ---------------- filari + terra ----------------
def rows(W, H, name, split=0.5, seed=7):
    w, h = int(W * SS), int(H * SS)
    r = np.random.default_rng(seed)
    soil = np.array([122, 98, 72], np.float32)
    img = Image.new('RGB', (w, h), (126, 102, 74))
    d = ImageDraw.Draw(img)
    ys = int(h * split)
    pitch = int(54 * SS)
    canopy = int(17 * SS)
    # interfila inerbita
    y = int(pitch * 0.5)
    rowsy = []
    while y < ys - canopy:
        rowsy.append(y); y += pitch
    for yy in rowsy:
        gy0 = yy + int(pitch * 0.32); gy1 = yy + int(pitch * 0.68)
        d.rectangle([0, gy0, w, gy1], fill=(132, 132, 82))
    # ombre delle chiome (luce da nord-ovest)
    for yy in rowsy:
        x = -20
        while x < w + 20:
            rr = canopy * (0.75 + r.random() * 0.4)
            d.ellipse([x - rr + 6 * SS, yy - rr + 8 * SS, x + rr + 6 * SS, yy + rr + 8 * SS], fill=(78, 70, 48))
            x += canopy * (1.0 + r.random() * 0.35)
    # chiome: grappoli di foglie con luce
    greens = [(74, 104, 46), (86, 118, 52), (98, 132, 60), (80, 112, 50)]
    for yy in rowsy:
        x = -20
        while x < w + 20:
            rr = canopy * (0.75 + r.random() * 0.4)
            c = greens[r.integers(0, 4)]
            d.ellipse([x - rr, yy - rr, x + rr, yy + rr], fill=c)
            for k in range(5):
                lx = x + r.normal(-rr * 0.2, rr * 0.35); ly = yy + r.normal(-rr * 0.25, rr * 0.3); lr = rr * (0.28 + r.random() * 0.2)
                cc = tuple(min(255, int(v * (1.1 + r.random() * 0.2))) for v in c)
                d.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=cc)
            x += canopy * (1.0 + r.random() * 0.35)
    # terra arata: solchi con zolle
    d.rectangle([0, ys, w, h], fill=(78, 56, 40))
    a = np.asarray(img, np.float32).copy()
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    fur = 0.5 + 0.5 * np.sin((yy + 6 * SS * np.sin(xx / (260 * SS))) * 2 * np.pi / (18 * SS))
    grain = noise(w, h, 4, 90, seed=seed + 1)
    clods = np.clip((noise(w, h, 3, 160, seed=seed + 2) - 0.6) * 4, 0, 1)
    soilshade = (0.72 + 0.38 * fur + 0.12 * (grain - 0.5) - 0.25 * clods)
    lower = (yy >= ys)
    soilcol = np.array([92, 66, 47], np.float32)
    a = np.where(lower[..., None], soilcol * soilshade[..., None], a)
    # grana generale e passaggio morbido
    a = a * (0.95 + 0.1 * noise(w, h, 5, 40, seed=seed + 3)[..., None])
    band = np.clip(1 - np.abs(yy - ys) / (h * 0.025), 0, 1)
    a = a * (1 - 0.22 * band[..., None])
    shade = np.clip((yy - ys) / (h - ys), 0, 1)
    a = a * (1 - 0.38 * shade[..., None])
    finish(a, W, H, name, 76)


if __name__ == '__main__':
    import os
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ['orbit', 'country', 'rows']
    if 'orbit' in which:
        orbit(2400, 1500, 'orbit-l'); orbit(1400, 2400, 'orbit-p', limb_frac=0.82)
    if 'country' in which:
        country(2400, 1500, 'country-l'); country(1400, 2400, 'country-p')
    if 'rows' in which:
        rows(2400, 1500, 'rows-l'); rows(1400, 2400, 'rows-p', split=0.52)
