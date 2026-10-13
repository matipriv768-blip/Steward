"""Captura la web con las letras locales (el contenedor no llega a Google Fonts). Uso: captura.py carpeta salida.png ancho [alto] [es|en]"""
import base64, os, sys
from playwright.sync_api import sync_playwright
site, out, w = sys.argv[1], sys.argv[2], int(sys.argv[3])
h = int(sys.argv[4]) if len(sys.argv) > 4 else 900
lang = sys.argv[5] if len(sys.argv) > 5 else 'es'
F = 'fonts_src/node_modules/@fontsource/'
css = ''
for fam, wt in (('fraunces', 400), ('fraunces', 500), ('inter', 400), ('inter', 500), ('inter', 600)):
    data = base64.b64encode(open(F + '%s/files/%s-latin-%d-normal.woff2' % (fam, fam, wt), 'rb').read()).decode()
    css += "@font-face{font-family:'%s';font-weight:%d;src:url(data:font/woff2;base64,%s) format('woff2')}\n" % (fam.capitalize(), wt, data)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
    pg.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body=css))
    pg.route('https://fonts.gstatic.com/**', lambda r: r.abort())
    pg.add_init_script("try{localStorage.setItem('steward-lang','%s')}catch(e){}" % lang)
    pg.goto('file://' + os.path.abspath(site) + '/index.html')
    pg.wait_for_timeout(600)
    pg.screenshot(path=out, full_page=True)
    b.close()
print('ok', out)
