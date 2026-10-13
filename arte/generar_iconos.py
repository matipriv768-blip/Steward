"""Iconos, logo e icono de ventana de Steward, en estilo editorial: formas planas, trazo fino y una sola tinta.

Cada imagen se dibuja en SVG y se renderiza con Chromium (Playwright). Salen dos juegos de iconos:
- claro: trazo tinta (#282834), para el tema claro y el modo sin fondo
- oscuro: trazo papel (#e9ece7), para el tema oscuro

Uso: python3 arte/generar_iconos.py carpeta_salida carpeta_fuentes
La carpeta de fuentes es la de @fontsource (npm install @fontsource/fraunces @fontsource/inter): node_modules/@fontsource
"""
import base64
import os
import sys

from playwright.sync_api import sync_playwright

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
FONTS = sys.argv[2] if len(sys.argv) > 2 else 'node_modules/@fontsource'
W, H = 640, 440

INK, PAPER_INK = '#282834', '#e9ece7'
FILL = {'green': '#2f9e5b', 'yellow': '#f2c230', 'red': '#d64532', 'blue': '#1f86c4',
        'white': '#fbfbf7', 'black': '#23232d'}
TAG = {'red': '#d64532', 'orange': '#e07a1f', 'green': '#2f9e5b'}


def font_face():
    css = []
    for fam, weight in (('fraunces', 400), ('inter', 500), ('inter', 600)):
        path = os.path.join(FONTS, fam, 'files', '%s-latin-%d-normal.woff2' % (fam, weight))
        data = base64.b64encode(open(path, 'rb').read()).decode()
        css.append("@font-face{font-family:'%s';font-weight:%d;src:url(data:font/woff2;base64,%s) format('woff2');}"
                   % (fam.capitalize(), weight, data))
    return '\n'.join(css)


# ---------------------------------------------------------------------------------------------- banderas
# Bandera con una sola ondulacion suave, en su asta. Coordenadas del cuadro de 640 x 440.
POLE_X, POLE_TOP, POLE_BOT = 132, 34, 420
FLAG = ('M{x},62 C230,30 330,96 430,62 C490,42 540,46 588,62 '
        'L588,282 C540,266 490,262 430,282 C330,316 230,250 {x},282 Z').format(x=POLE_X)


def flag_inner(kind, uid):
    """Relleno de la tela, recortado por la forma de la bandera."""
    if kind in FILL:
        return '<rect x="100" y="0" width="520" height="340" fill="%s"/>' % FILL[kind]
    if kind == 'check':
        s = 46
        out = ['<rect x="100" y="0" width="520" height="340" fill="%s"/>' % FILL['white']]
        for r in range(0, 8):
            for c in range(0, 11):
                if (r + c) % 2 == 0:
                    out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (POLE_X + c * s, 40 + r * s, s, s, FILL['black']))
        return ''.join(out)
    if kind == 'warn':
        return ('<rect x="100" y="0" width="520" height="340" fill="%s"/>'
                '<polygon points="100,0 100,340 620,340" fill="%s"/>') % (FILL['white'], FILL['black'])
    raise ValueError(kind)


def flag(kind, uid, stroke, transform=''):
    # una banda clara muy suave sigue la ondulacion: da volumen sin brillos ni texturas
    return f'''
<g transform="{transform}">
  <defs><clipPath id="c{uid}"><path d="{FLAG}"/></clipPath>
    <linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#000" stop-opacity="0.10"/><stop offset="0.35" stop-color="#fff" stop-opacity="0.10"/>
      <stop offset="0.62" stop-color="#000" stop-opacity="0.06"/><stop offset="1" stop-color="#fff" stop-opacity="0.08"/>
    </linearGradient></defs>
  <g clip-path="url(#c{uid})">{flag_inner(kind, uid)}<rect x="100" y="0" width="520" height="340" fill="url(#g{uid})"/></g>
  <path d="{FLAG}" fill="none" stroke="{stroke}" stroke-width="15" stroke-linejoin="round"/>
  <line x1="{POLE_X}" y1="{POLE_TOP}" x2="{POLE_X}" y2="{POLE_BOT}" stroke="{stroke}" stroke-width="17" stroke-linecap="round"/>
  <circle cx="{POLE_X}" cy="{POLE_TOP - 4}" r="15" fill="{stroke}"/>
</g>'''


def crossed(kind, uid, stroke):
    # amarilla total: dos amarillas cruzadas, las astas se juntan abajo y las telas salen hacia afuera
    t = 'translate(262 404) rotate(22) scale(0.6) translate(%g %g)' % (-POLE_X, -POLE_BOT)
    return (f'<g transform="translate(640 0) scale(-1 1)">{flag(kind, uid + "a", stroke, t)}</g>'
            + flag(kind, uid + 'b', stroke, t))


# ---------------------------------------------------------------------------------------------- placas
def board(uid, tag, inner, stroke, face, x=110, y=40, w=420, h=290, handle=True):
    hx = x + w / 2
    handle_svg = (f'<line x1="{hx}" y1="{y + h}" x2="{hx}" y2="420" stroke="{stroke}" stroke-width="17" stroke-linecap="round"/>'
                  if handle else '')
    return f'''
<g>
  <defs><clipPath id="b{uid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34"/></clipPath></defs>
  {handle_svg}
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="{face}"/>
  <rect x="{x}" y="{y}" width="{w}" height="40" fill="{TAG[tag]}" clip-path="url(#b{uid})"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="none" stroke="{stroke}" stroke-width="15"/>
  <g transform="translate({x + w / 2} {y + 20 + h / 2})">{inner}</g>
</g>'''


def serif(t, size, color, dy=0, spacing=-0.02):
    return ('<text x="0" y="{dy}" text-anchor="middle" dominant-baseline="central" font-family="Fraunces" font-weight="400" '
            'font-size="{s}" letter-spacing="{sp}em" fill="{c}">{t}</text>').format(dy=dy, s=size, sp=spacing, c=color, t=t)


def pictogram(name, ink):
    s = 'fill="none" stroke="%s" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"' % ink
    if name == 'time':
        return f'''<g {s}><circle cx="34" cy="8" r="78"/><path d="M34,8 L34,-34"/><path d="M34,8 L64,30"/>
          <path d="M14,-86 L54,-86"/><path d="M34,-86 L34,-70"/><path d="M-150,8 h56 M-122,-20 v56"/></g>'''
    if name == 'lift':
        return f'''<g {s}><rect x="-120" y="-30" width="92" height="120" rx="18" transform="rotate(-14 -74 30)"/>
          <path d="M-98,6 h48 M-102,38 h48" transform="rotate(-14 -74 30)"/>
          <path d="M74,86 L74,-76"/><path d="M28,-30 L74,-80 L120,-30"/></g>'''
    if name == 'giveback':
        return f'''<g {s}><path d="M-128,-38 H112"/><path d="M70,-80 L114,-38 L70,4"/>
          <path d="M128,52 H-112"/><path d="M-70,10 L-114,52 L-70,94"/></g>'''
    if name == 'ok':
        return f'<path d="M-104,4 L-36,70 L108,-74" fill="none" stroke="{TAG["green"]}" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>'
    raise ValueError(name)


def icon_set(stroke, face, ink):
    return {
        'bandera_verde': lambda: flag('green', 'a', stroke),
        'bandera_amarilla': lambda: flag('yellow', 'a', stroke),
        'bandera_azul': lambda: flag('blue', 'a', stroke),
        'bandera_blanca': lambda: flag('white', 'a', stroke),
        'bandera_negra': lambda: flag('black', 'a', stroke),
        'bandera_roja': lambda: flag('red', 'a', stroke),
        'bandera_cuadros': lambda: flag('check', 'a', stroke),
        'aviso': lambda: flag('warn', 'a', stroke),
        'bandera_amarilla_total': lambda: crossed('yellow', 'y', stroke),
        'drive_through': lambda: board('d', 'red', serif('DT', 190, ink), stroke, face),
        'stop_and_go': lambda: board('s', 'red', serif('SG', 190, ink), stroke, face),
        'tiempo': lambda: board('t', 'orange', pictogram('time', ink), stroke, face),
        'levantar': lambda: board('l', 'orange', pictogram('lift', ink), stroke, face),
        'devolver': lambda: board('g', 'orange', pictogram('giveback', ink), stroke, face),
        'cumplida': lambda: board('c', 'green', pictogram('ok', ink), stroke, face),
        'descalificado': lambda: (flag('black', 'a', stroke, 'translate(-6 0) scale(0.9)')
                                  + board('q', 'red', serif('DSQ', 112, ink, dy=4), stroke, face,
                                          x=318, y=196, w=290, h=200, handle=False)),
    }


# ---------------------------------------------------------------------------------------------- logo
def mark(cx, cy, r, ring, inner_bg, pole):
    # sello: un circulo con una bandera a cuadros minima
    s = r / 100.0
    cells = []
    for row in range(3):
        for col in range(4):
            if (row + col) % 2 == 0:
                cells.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>' % (
                    cx - 30 * s + col * 16 * s, cy - 40 * s + row * 16 * s, 16 * s, 16 * s, pole))
    return f'''
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{inner_bg}" stroke="{ring}" stroke-width="{6 * s}"/>
<line x1="{cx - 34 * s}" y1="{cy - 52 * s}" x2="{cx - 34 * s}" y2="{cy + 58 * s}" stroke="{pole}" stroke-width="{8 * s}" stroke-linecap="round"/>
<rect x="{cx - 30 * s}" y="{cy - 40 * s}" width="{64 * s}" height="{48 * s}" fill="none" stroke="{pole}" stroke-width="{5 * s}"/>
{''.join(cells)}'''


def wordmark(color, mark_bg, mark_ink, w=1200, h=360):
    return f'''
{mark(180, h / 2, 118, mark_ink, mark_bg, mark_ink)}
<text x="340" y="{h / 2 + 8}" dominant-baseline="central" font-family="Fraunces" font-weight="400" font-size="210"
  letter-spacing="-0.03em" fill="{color}">Steward</text>'''


def app_icon():
    return f'''
<rect x="0" y="0" width="512" height="512" rx="112" fill="#1f1f29"/>
<text x="256" y="236" text-anchor="middle" dominant-baseline="central" font-family="Fraunces" font-weight="400"
  font-size="330" fill="#fefffc">S</text>
<rect x="166" y="404" width="180" height="12" rx="6" fill="#41a1cf"/>'''


def page(svg, w, h):
    return f'''<!doctype html><html><head><style>{font_face()} html,body{{margin:0;background:transparent}}</style></head>
<body><svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg}</svg></body></html>'''


def shot(pg, svg, w, h, path):
    pg.set_viewport_size({'width': w, 'height': h})
    pg.set_content(page(svg, w, h))
    pg.wait_for_timeout(120)
    pg.locator('svg').screenshot(path=path, omit_background=True)


def main():
    for sub in ('claro', 'oscuro', 'logo'):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(device_scale_factor=2)
        for sub, stroke, face, ink in (('claro', INK, '#ffffff', INK), ('oscuro', PAPER_INK, '#2a2a36', PAPER_INK)):
            for name, fn in icon_set(stroke, face, ink).items():
                shot(pg, fn(), W, H, os.path.join(OUT, sub, name + '.png'))
        shot(pg, wordmark('#2c2c2c', '#fefffc', '#282834'), 1200, 360, os.path.join(OUT, 'logo', 'logo_claro.png'))
        shot(pg, wordmark('#f2f3ef', '#1f1f29', '#e9ece7'), 1200, 360, os.path.join(OUT, 'logo', 'logo_oscuro.png'))
        shot(pg, app_icon(), 512, 512, os.path.join(OUT, 'logo', 'icono.png'))
        shot(pg, mark(256, 256, 236, '#282834', '#fefffc', '#282834'), 512, 512, os.path.join(OUT, 'logo', 'sello.png'))
        b.close()
    print('listo')


if __name__ == '__main__':
    main()
