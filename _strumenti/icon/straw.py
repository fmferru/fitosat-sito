from PIL import Image, ImageDraw, ImageFont
exec(open('icon.py').read().split("out = {}")[0])
V = [('Paglia chiara', (230, 216, 168)), ('Paglia', (216, 196, 132)), ('Paglia scura', (196, 172, 104))]
fg = (102, 40, 74)
fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
pv = Image.new('RGB', (3 * 260 + 40, 320), (244, 235, 230)); d = ImageDraw.Draw(pv)
for k, (name, bg) in enumerate(V):
    a = mark((*bg, 255), fg=fg).resize((180, 180), Image.LANCZOS)
    m = Image.new('L', (180, 180), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 179, 179], radius=40, fill=255)
    x = 60 + k * 260
    pv.paste(a, (x, 40), m)
    f = mark((*bg, 255), fg=fg, rounded=True).resize((32, 32), Image.LANCZOS); pv.paste(f, (x + 74, 236), f)
    d.text((x + 90, 292), name, fill=(36, 22, 29), anchor='mm', font=fnt)
    mark((*bg, 255), fg=fg).convert('RGB').resize((180, 180), Image.LANCZOS).save(f'apple-straw{k}.png')
    mark((*bg, 255), fg=fg, rounded=True).resize((64, 64), Image.LANCZOS).save(f'fav-straw{k}.png')
pv.save('/home/claude/preview/icons-straw.png')
