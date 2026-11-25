"""Intro 'orbita': globo realistico da NASA Blue Marble (pubblico dominio) + stelle."""
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import map_coordinates, gaussian_filter

SRC = '/tmp/earth'
OUT = '/home/claude/staging/img'


def load(path, mode='RGB'):
    return np.asarray(Image.open(path).convert(mode)).astype(np.float32)


DAY = load(f'{SRC}/tg/example/img/earth-blue-marble.jpg')
NIGHT = load(f'{SRC}/tg/example/img/earth-night.jpg')
WATER = load(f'{SRC}/tg/example/img/earth-water.png', 'L') / 255.0
CLOUD = np.asarray(Image.open(f'{SRC}/gg/example/clouds/clouds.png').convert('RGBA'))[..., 3].astype(np.float32) / 255.0
# NASA Blue Marble NG (agosto 2004, 21600x10800, pubblico dominio): ritaglio ad alta risoluzione sull'area visibile
Image.MAX_IMAGE_PIXELS = None
HLON0, HLON1, HLAT0, HLAT1 = -75.0, 100.0, -25.0, 88.0
_hi = Image.open('/tmp/bm/w.jpg')
_px = 21600 / 360.0
HI = np.asarray(_hi.crop((int((HLON0 + 180) * _px), int((90 - HLAT1) * _px), int((HLON1 + 180) * _px), int((90 - HLAT0) * _px)))).astype(np.float32)
del _hi
HIW = ((HI.max(-1) < 34) & (HI[..., 2] >= HI[..., 1] - 2) & (HI[..., 2] >= HI[..., 0] + 2)).astype(np.float32)
from scipy.ndimage import binary_opening
HIW = binary_opening(HIW > .5, iterations=1).astype(np.float32)
HIW = gaussian_filter(HIW, 1.0)


def sample_hi(tex, lat, lon):
    Ht, Wt = tex.shape[:2]
    u = (lon - HLON0) / (HLON1 - HLON0) * Wt - 0.5
    v = (HLAT1 - lat) / (HLAT1 - HLAT0) * Ht - 0.5
    if tex.ndim == 2:
        return map_coordinates(tex, [v, u], order=3, mode='nearest')
    return np.stack([map_coordinates(tex[..., k], [v, u], order=3, mode='nearest') for k in range(tex.shape[2])], -1)


def sample(tex, lat, lon):
    Ht, Wt = tex.shape[:2]
    u = ((lon + 180.0) % 360.0) / 360.0 * Wt - 0.5
    v = (90.0 - lat) / 180.0 * Ht - 0.5
    if tex.ndim == 2:
        return map_coordinates(tex, [v, u], order=1, mode='wrap')
    return np.stack([map_coordinates(tex[..., k], [v, u], order=1, mode='wrap') for k in range(tex.shape[2])], -1)


def stars(w, h, seed=5):
    rng = np.random.default_rng(seed)
    sky = np.zeros((h, w, 3), np.float32)
    # fondo: blu notte con una leggera fascia lattea
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    band = np.exp(-(((yy / h) - 0.28 - 0.25 * (xx / w)) / 0.16) ** 2)
    n = gaussian_filter(rng.random((h // 8 + 1, w // 8 + 1)).astype(np.float32), 3)
    n = np.asarray(Image.fromarray(((n - n.min()) / (np.ptp(n) + 1e-6) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    sky += np.array([5, 7, 16], np.float32)
    sky += (band * (0.4 + 0.8 * n))[..., None] * np.array([10, 12, 22], np.float32)
    # stelle piccole
    N = int(w * h / 700)
    sx = rng.integers(0, w, N); sy = rng.integers(0, h, N)
    b = rng.random(N) ** 3.2
    # più dense nella fascia
    keep = rng.random(N) < (0.45 + 0.55 * band[sy, sx])
    sx, sy, b = sx[keep], sy[keep], b[keep]
    tint = np.stack([1 - 0.12 * rng.random(len(b)), np.ones(len(b)), 1 + 0.1 * rng.random(len(b))], -1)
    pts = np.zeros((h, w, 3), np.float32)
    np.add.at(pts, (sy, sx), (b[:, None] * 255 * tint))
    sky += gaussian_filter(pts, (0.6, 0.6, 0)) * 2.2
    # poche stelle luminose con alone
    M = int(w * h / 60000)
    bx = rng.integers(0, w, M); by = rng.integers(0, h, M)
    big = np.zeros((h, w, 3), np.float32)
    big[by, bx] = 255 * (0.6 + 0.4 * rng.random(M))[:, None] * np.array([1.0, 0.98, 1.05])
    sky += gaussian_filter(big, (1.2, 1.2, 0)) * 9 + gaussian_filter(big, (5, 5, 0)) * 6
    return sky


def orbit(W, H, name, limb_frac, R_frac, target_frac, lon0=11.0, tgt_lat=44.0):
    w, h = W, H
    R = R_frac * max(w, h) if W > H else R_frac * w
    cx = w * 0.5
    cy = h * limb_frac + R
    # latitudine del centro di vista: l'Italia cade a target_frac dell'altezza
    ny_t = (cy - h * target_frac) / R
    lat0 = tgt_lat - np.degrees(np.arcsin(np.clip(ny_t, -1, 1)))
    phi0 = np.radians(lat0)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = (xx - cx) / R
    ny = (cy - yy) / R
    r2 = nx * nx + ny * ny
    inside = r2 < 1
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    lat = np.degrees(np.arcsin(np.clip(nz * np.sin(phi0) + ny * np.cos(phi0), -1, 1)))
    lon = lon0 + np.degrees(np.arctan2(nx, nz * np.cos(phi0) - ny * np.sin(phi0)))
    m = inside
    day = np.zeros((h, w, 3), np.float32); night = np.zeros_like(day)
    water = np.zeros((h, w), np.float32); cloud = np.zeros((h, w), np.float32)
    day[m] = sample(DAY, lat[m], lon[m])
    lonw = ((lon + 180.0) % 360.0) - 180.0
    hm = m & (lonw > HLON0 + .5) & (lonw < HLON1 - .5) & (lat > HLAT0 + .5) & (lat < HLAT1 - .5)
    hd = sample_hi(HI, lat[hm], lonw[hm]); hw = np.clip(sample_hi(HIW, lat[hm], lonw[hm]), 0, 1)[:, None]
    # terre dall'immagine ad alta risoluzione, mari dalla mappa con i fondali
    sea = sample(DAY, np.array([35.0, 38.0, 40.0]), np.array([18.0, -20.0, 5.0])).mean(0)
    day[hm] = hd * (1 - hw) + sea[None, :] * hw
    night[m] = sample(NIGHT, lat[m], lon[m])
    water[m] = sample(WATER, lat[m], lon[m])
    water[hm] = np.clip(sample_hi(HIW, lat[hm], lonw[hm]), 0, 1)
    cloud[m] = sample(CLOUD, lat[m], lon[m])
    # luce del sole: da sinistra, un po' davanti
    L = np.array([-0.62, 0.42, 0.66]); L /= np.linalg.norm(L)
    ndl = nx * L[0] + ny * L[1] + nz * L[2]
    lit = np.clip(ndl * 1.15 + 0.08, 0, 1)
    lit = lit ** 0.8
    # colore: Blue Marble un po' più saturo e contrastato
    base = day / 255.0
    base = np.clip((base - 0.04) * 1.12, 0, 1) ** 0.92
    # mare più scuro e profondo, come nelle foto reali
    w3 = water[..., None]
    base = base * (1 - w3) + (base * np.array([0.55, 0.62, 0.78]) + np.array([0.0, 0.015, 0.04])) * w3
    c = cloud[..., None] ** 1.1
    surf = base * (1 - 0.92 * c) + 0.96 * c
    col = surf * lit[..., None]
    # riflesso del sole sul mare
    H_ = L + np.array([0, 0, 1.0]); H_ /= np.linalg.norm(H_)
    ndh = np.clip(nx * H_[0] + ny * H_[1] + nz * H_[2], 0, 1)
    spec = (ndh ** 70) * water * (1 - cloud) * 0.55
    col += spec[..., None] * np.array([1.0, 0.95, 0.85])
    # luci delle città sul lato in ombra
    nl = np.clip(1 - (ndl + 0.05) * 6, 0, 1)
    col += (night / 255.0) ** 1.4 * nl[..., None] * np.array([1.0, 0.82, 0.55]) * 0.9 * (1 - c)
    # foschia atmosferica verso il bordo
    haze = np.clip(1 - nz, 0, 1) ** 2.2
    atm = np.array([0.42, 0.62, 1.0]) * (0.25 + 0.75 * np.clip(ndl + 0.3, 0, 1))[..., None]
    col = col * (1 - 0.7 * haze[..., None]) + atm * 0.7 * haze[..., None]
    img = stars(w, h) / 255.0
    img = np.where(inside[..., None], col, img)
    # alone atmosferico esterno, più luminoso dal lato del sole
    d = np.sqrt(r2) * R
    out = np.clip(d - R, 0, None)
    side = np.clip(0.35 + 0.65 * ((nx * L[0] + ny * L[1]) / (np.sqrt(r2) + 1e-6) * 0.5 + 0.5), 0, 1)
    rim = np.exp(-((d - R) / (R * 0.006)) ** 2) * (d > R * 0.996)
    glow = np.exp(-out / (R * 0.022)) * (d > R)
    img += (rim * 0.9 + glow * 0.55)[..., None] * side[..., None] * np.array([0.45, 0.68, 1.0])
    img = np.clip(img, 0, 1) * 255
    im = Image.fromarray(img.astype(np.uint8))
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    im.save(f'{OUT}/{name}.webp', quality=80, method=6)
    sw = {'orbit-l': 1600, 'orbit-p': 900}[name]
    im.resize((sw, round(h * sw / w)), Image.LANCZOS).save(f'{OUT}/{name}-{sw}.webp', quality=80, method=6)
    print(name, 'lat0=%.1f' % lat0, 'target y=%.0f%%' % (target_frac * 100))


if __name__ == '__main__':
    which = sys.argv[1:] or ['l', 'p']
    if 'l' in which:
        orbit(3200, 2000, 'orbit-l', limb_frac=0.71, R_frac=0.62, target_frac=0.93)
    if 'p' in which:
        orbit(1750, 3000, 'orbit-p', limb_frac=0.70, R_frac=0.95, target_frac=0.92)
