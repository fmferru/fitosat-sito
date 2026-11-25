from PIL import Image, ImageDraw
S = 1024
def mark(bg, fg=(255, 255, 255), dot=(226, 38, 44), rounded=False):
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if rounded: d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * .225), fill=bg)
    else: d.rectangle([0, 0, S, S], fill=bg)
    r, w = 104, 44                      # raggio dei cerchi, spessore del tratto
    cx, top, dx, dy = S / 2, 284, 262, 228
    pts = [(cx - dx, top), (cx + dx, top), (cx - dx / 2, top + dy), (cx + dx / 2, top + dy), (cx, top + 2 * dy)]
    for x, y in pts:
        d.ellipse([x - r, y - r, x + r, y + r], outline=fg, width=w)
    R = 80
    d.ellipse([cx - R, top - R, cx + R, top + R], fill=dot)
    return im
out = {}
for name, bg in (('ink', (36, 22, 29, 255)), ('brand', (102, 40, 74, 255))):
    a = mark(bg); a.convert('RGB').resize((180, 180), Image.LANCZOS).save(f'apple-{name}.png')
    f = mark(bg, rounded=True); f.resize((64, 64), Image.LANCZOS).save(f'fav-{name}.png')
    out[name] = (a, f)
# anteprima: icona grande, come su iPhone (angoli arrotondati), favicon in una scheda
pv = Image.new('RGB', (1000, 420), (244, 235, 230)); d = ImageDraw.Draw(pv)
for k, name in enumerate(('ink', 'brand')):
    a = out[name][0].resize((220, 220), Image.LANCZOS)
    m = Image.new('L', (220, 220), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 219, 219], radius=50, fill=255)
    pv.paste(a, (60 + k * 480, 60), m)
    f = Image.open(f'fav-{name}.png').resize((32, 32), Image.LANCZOS)
    d.rounded_rectangle([320 + k * 480, 120, 500 + k * 480, 165], radius=10, fill=(255, 255, 255))
    pv.paste(f, (330 + k * 480, 126), f)
    d.text((370 + k * 480, 136), 'Fitosat', fill=(36, 22, 29))
    f16 = Image.open(f'fav-{name}.png').resize((16, 16), Image.LANCZOS); pv.paste(f16, (330 + k * 480, 200), f16)
pv.save('/home/claude/preview/icons-new.png')
