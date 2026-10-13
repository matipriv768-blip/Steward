"""Exporta las fotos de la web en dos tamanos (1376 y 800 px) a docs/assets/fotos."""
import sys, os
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
for name in ('atardecer', 'lado_a_lado', 'banderillero', 'pits', 'largada'):
    im = Image.open(os.path.join(src, name + '.jpg')).convert('RGB')
    for w in (1376, 800):
        x = im if im.width == w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        x.save(os.path.join(out, '%s-%d.jpg' % (name, w)), quality=82, optimize=True, progressive=True)
print(sorted(os.listdir(out)))
