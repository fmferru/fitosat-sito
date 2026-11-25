from PIL import Image, ImageDraw, ImageFont
exec(open('icon.py').read().split("out = {}")[0])
V = [('Crema', (244, 235, 230), (102, 40, 74)), ('Rosa antico', (224, 180, 200), (36, 22, 29)),
     ('Verde vigna', (46, 82, 44), (255, 255, 255)), ('Notte (orbita)', (14, 26, 48), (255, 255, 255)),
     ('Blu cielo', (40, 96, 196), (255, 255, 255)), ('Bianco', (255, 255, 255), (102, 40, 74))]
pv = Image.new('RGB', (6 * 200 + 40, 300), (244, 235, 230)); d = ImageDraw.Draw(pv)
try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
except Exception: fnt = None
for k, (name, bg, fg) in enumerate(V):
    a = mark((*bg, 255), fg=fg).resize((160, 160), Image.LANCZOS)
    m = Image.new('L', (160, 160), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 159, 159], radius=36, fill=255)
    x = 40 + k * 200
    d.rounded_rectangle([x - 1, 39, x + 160, 200], radius=37, fill=(225, 214, 208))
    pv.paste(a, (x, 40), m)
    f = mark((*bg, 255), fg=fg, rounded=True).resize((32, 32), Image.LANCZOS); pv.paste(f, (x + 64, 215), f)
    d.text((x + 80, 268), name, fill=(36, 22, 29), anchor='mm', font=fnt)
    a2 = mark((*bg, 255), fg=fg); a2.convert('RGB').resize((180, 180), Image.LANCZOS).save(f'apple-v{k}.png')
    mark((*bg, 255), fg=fg, rounded=True).resize((64, 64), Image.LANCZOS).save(f'fav-v{k}.png')
pv.save('/home/claude/preview/icons-variants.png')
