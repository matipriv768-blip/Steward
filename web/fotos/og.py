"""Imagen para compartir el link (1200x630): foto del atardecer con tarjeta Steward."""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
src, fonts, out = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(src).convert('RGB')
W, H = 1200, 630
s = max(W / im.width, H / im.height)
im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
x0 = (im.width - W) // 2; y0 = int((im.height - H) * .55)
im = im.crop((x0, y0, x0 + W, y0 + H))
box = (48, 330, 640, 582)
blur = im.crop(box).filter(ImageFilter.GaussianBlur(18))
card = Image.blend(blur, Image.new('RGB', blur.size, (254, 255, 252)), .78)
mask = Image.new('L', blur.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, *blur.size), 22, fill=255)
im.paste(card, box[:2], mask)
d = ImageDraw.Draw(im)
d.rounded_rectangle(box, 22, outline=(255, 255, 255), width=1)
d.text((84, 366), 'COMISARIO DE CARRERA · ASSETTO CORSA', font=ImageFont.truetype(fonts + '/Inter-600.ttf', 17), fill=(100, 100, 100))
d.text((80, 396), 'Steward', font=ImageFont.truetype(fonts + '/Fraunces-400.ttf', 84), fill=(44, 44, 44))
d.text((84, 512), 'Carreras limpias, decididas en la pista.', font=ImageFont.truetype(fonts + '/Inter-400.ttf', 25), fill=(68, 65, 65))
im.save(out, quality=86, optimize=True)
print('ok')
