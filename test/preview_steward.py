"""Dibuja los indicadores tal como los dibujaria el juego, para revisar el diseno."""
import sys
from lupa import luajit21 as lj
from PIL import Image, ImageDraw, ImageFont

APP = 'apps/lua/Steward/Steward.lua'
FDIR = 'apps/lua/Steward/fonts/'
IMG = 'apps/lua/Steward/img/'
BOLD = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
REG = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
SS = 2  # supersampling
_fonts = {}

def font(name, size):
    # name: el texto de la fuente que pide la app (o True/False en las etiquetas del pliego)
    if name is True: path = FDIR + 'Inter-600.ttf'
    elif name is False or name is None: path = FDIR + 'Inter-400.ttf'
    elif 'Fraunces' in name or 'Georgia' in name: path = FDIR + 'Fraunces-400.ttf'
    elif 'SemiBold' in name: path = FDIR + 'Inter-600.ttf'
    elif 'Bold' in name: path = FDIR + 'Inter-700.ttf'
    else: path = FDIR + 'Inter-400.ttf'
    key = (path, round(size * SS))
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, key[1])
    return _fonts[key]

def col(c, bg=None):
    a = c['mult'] if c['mult'] is not None else 1
    return (int(c['r'] * 255), int(c['g'] * 255), int(c['b'] * 255), int(max(0, min(1, a)) * 255))

def make(scene_lua, width, height, placements, bg):
    lua = lj.LuaRuntime(unpack_returned_tuples=True)
    state = {'bold': False, 'ops': [], 'origin': (0, 0)}
    lua.execute("local f = assert(loadfile('test/harness.lua')); f('%s')" % APP)
    g = lua.globals()
    ui = g.ui
    ui.pushDWriteFont = lambda name: state.__setitem__('bold', str(name))
    ui.popDWriteFont = lambda: None
    ui.measureDWriteText = lambda text, size: g.vec2(font(state['bold'], size).getlength(text) / SS, size)
    ui.getCursor = lambda: g.vec2(state['origin'][0], state['origin'][1])
    ui.drawRectFilled = lambda p1, p2, c, r=None: state['ops'].append(('rect', p1.x, p1.y, p2.x, p2.y, col(c), r or 0))
    ui.drawRect = lambda p1, p2, c, r=None, fl=None, th=None: state['ops'].append(('box', p1.x, p1.y, p2.x, p2.y, col(c), r or 0))
    ui.drawTriangleFilled = lambda a, b, c3, c: state['ops'].append(('tri', a.x, a.y, b.x, b.y, c3.x, c3.y, col(c)))
    ui.drawCircleFilled = lambda p, r, c, n=None: state['ops'].append(('circle', p.x, p.y, r, col(c)))
    ui.drawImage = lambda path, p1, p2, c=None, *a: state['ops'].append(('img', str(path), p1.x, p1.y, p2.x, p2.y))
    ui.dwriteDrawText = lambda text, size, p, c: state['ops'].append(('text', text, size, p.x, p.y, col(c), state['bold'], state.get('outline', False)))
    ui.beginOutline = lambda: state.__setitem__('outline', True)
    ui.endOutline = lambda c, *a: state.__setitem__('outline', False)
    lua.execute("for _, f in ipairs({ 'img/aviso.png', 'img/48/aviso.png', 'img/80/aviso.png', 'img/160/aviso.png', 'img/oscuro/aviso.png', 'fonts/Inter-400.ttf', 'fonts/Fraunces-400.ttf' }) do T.files['C:/logs/' .. f] = 'x' end")
    lua.execute(scene_lua)
    img = Image.new('RGBA', (width * SS, height * SS))
    d0 = ImageDraw.Draw(img)
    if isinstance(bg, str):
        photo = Image.open(bg).convert('RGBA')
        k = max(width * SS / photo.width, height * SS / photo.height)
        photo = photo.resize((int(photo.width * k) + 1, int(photo.height * k) + 1), Image.LANCZOS)
        img.paste(photo.crop((0, 0, width * SS, height * SS)), (0, 0))
        bg = None
        photo_used = True
    else:
        photo_used = False
    # fondo: cielo, horizonte y asfalto, para juzgar la legibilidad
    for y in range(height * SS):
        t = y / (height * SS)
        if t < 0.45:
            c = (int(120 + 60 * t), int(170 + 40 * t), int(225 - 20 * t), 255)
        elif t < 0.5:
            c = (70, 110, 60, 255)
        else:
            k = (t - 0.5) * 2
            c = (int(70 - 25 * k), int(72 - 25 * k), int(78 - 25 * k), 255)
        if not photo_used: d0.line([(0, y), (width * SS, y)], fill=c if bg else (30, 32, 36, 255))
    if bg and not photo_used:
        mx1, mx2 = (width - 512) // 2, (width + 512) // 2
        d0.rectangle([mx1 * SS, 85 * SS, mx2 * SS, 213 * SS], fill=(58, 62, 70, 255), outline=(20, 20, 22, 255), width=SS * 2)
        d0.text(((mx1 + 172) * SS, 138 * SS), 'espejo virtual del juego', font=font(False, 14), fill=(170, 175, 185, 255))
    for fn, (ox, oy) in placements:
        state['ops'] = []
        state['origin'] = (ox, oy)
        getattr(g.script, fn)(0.016)
        state['ops'] = []
        getattr(g.script, fn)(0.016)
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for op in state['ops']:
            k = op[0]
            if k == 'rect':
                _, x1, y1, x2, y2, c, r = op
                if x2 > x1 and y2 > y1:
                    tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
                    ImageDraw.Draw(tmp).rounded_rectangle([x1 * SS, y1 * SS, x2 * SS, y2 * SS], radius=min(r * SS, (x2 - x1) * SS / 2, (y2 - y1) * SS / 2), fill=c)
                    layer = Image.alpha_composite(layer, tmp); d = ImageDraw.Draw(layer)
            elif k == 'box':
                _, x1, y1, x2, y2, c, r = op
                tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
                ImageDraw.Draw(tmp).rounded_rectangle([x1 * SS, y1 * SS, x2 * SS, y2 * SS], radius=min(r * SS, (x2 - x1) * SS / 2, (y2 - y1) * SS / 2), outline=c, width=SS)
                layer = Image.alpha_composite(layer, tmp); d = ImageDraw.Draw(layer)
            elif k == 'tri':
                _, ax, ay, bx, by, cx, cy, c = op
                d.polygon([(ax * SS, ay * SS), (bx * SS, by * SS), (cx * SS, cy * SS)], fill=c)
            elif k == 'circle':
                _, x, y, r, c = op
                tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
                ImageDraw.Draw(tmp).ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=c)
                layer = Image.alpha_composite(layer, tmp); d = ImageDraw.Draw(layer)
            elif k == 'img':
                _, path, x1, y1, x2, y2 = op
                src = Image.open(IMG + path.split('/img/')[-1]).convert('RGBA')
                src = src.resize((max(1, int((x2 - x1) * SS)), max(1, int((y2 - y1) * SS))), Image.LANCZOS)
                tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
                tmp.paste(src, (int(x1 * SS), int(y1 * SS)))
                layer = Image.alpha_composite(layer, tmp); d = ImageDraw.Draw(layer)
            elif k == 'text':
                _, text, size, x, y, c, bold, outline = op
                f = font(bold, size)
                # DirectWrite ubica el texto desde la parte alta de la linea
                if outline:
                    d.text((x * SS, y * SS + size * SS * 0.08), text, font=f, fill=c, stroke_width=SS, stroke_fill=(0, 0, 0, int(230 * c[3] / 255)))
                else:
                    d.text((x * SS, y * SS + size * SS * 0.08), text, font=f, fill=c)
        img = Image.alpha_composite(img, layer)
    return img.resize((width, height), Image.LANCZOS)

if __name__ == '__main__':
    # uso: preview_steward.py salida.png [es|en] [claro|oscuro|sinfondo] [fondo.jpg] [escenas separadas por coma]
    out = sys.argv[1]
    LANG_ID = 2 if (len(sys.argv) > 2 and sys.argv[2] == 'en') else 1
    THEME = {'claro': 1, 'oscuro': 2, 'sinfondo': 0}[sys.argv[3] if len(sys.argv) > 3 else 'claro']
    BG = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else True
    PICK = [int(x) for x in sys.argv[5].split(',')] if len(sys.argv) > 5 else None
    W = 1000
    place = [('fullscreenUI', (0, 0))]
    base = 'T.screenW=1000; T.screenH=1080; T.cfg.hudFixed=true; T.cfg.hudTheme=THEME; T.cfg.hudY=22; T.cfg.lang=LANG; '
    scenes = [
      ('Bandera amarilla', base + 'T.cfg.flEnabled=true; T.sim.timeToSessionStart=-20000; place(0,0,150); place(1,200,0); run(1)'),
      ('Drive-through: aviso y sanción pendiente', base + 'T.cfg.flEnabled=true; T.sim.timeToSessionStart=-20000; T.cfg.tiers=true; T.cfg.pitLimit=82; T.cfg.pitTolerance=0; local c=place(0,0,90); c.isInPitlane=true; run(1); c.isInPitlane=false; place(0,0,150); run(1)'),
      ('Devolver la posición', base + 'T.cfg.flEnabled=true; T.sim.timeToSessionStart=-20000; place(0,0,170); place(1,4.5,150); run(0.5); hit(0); run(0.5); place(0,20,170); run(3); run(6)'),
      ('Salida lanzada: velocidad contra el límite', base + 'T.cfg.startMode=2; T.cfg.formShort=true; T.physicsAllowed=true; T.sim.carsCount=2; newSession(); T.sim.timeToSessionStart=-100; T.cars[0].racePosition=2; T.cars[1].racePosition=1; run(1); place(1,3200,96); place(0,3190,94); run(8)'),
      ('Bandera verde con semáforo', base + 'T.cfg.startMode=2; T.cfg.formShort=true; T.physicsAllowed=true; T.sim.carsCount=2; newSession(); T.sim.timeToSessionStart=-100; T.cars[0].racePosition=2; T.cars[1].racePosition=1; run(1); place(1,3200,96); place(0,3190,94); run(8); place(1,3420,96); place(0,3410,94); run(1.0)'),
      ('Descalificado', base + 'T.cfg.flEnabled=true; T.sim.timeToSessionStart=-20000; T.cfg.incDQ=1; T.cfg.tlMode=1; local c=place(0,0,150); c.wheelsOutside=4; run(1); c.wheelsOutside=0; run(5); c.wheelsOutside=4; run(1); c.wheelsOutside=0; run(1)'),
    ]
    if PICK: scenes = [scenes[i] for i in PICK]
    H = 470
    if len(scenes) == 1:
        img = make('LANG = %d; THEME = %d; ' % (LANG_ID, THEME) + scenes[0][1], W, H, place, BG)
        img.convert('RGB').save(out); print('ok', out, img.size); sys.exit(0)
    sheet = Image.new('RGBA', (W, (H + 34) * len(scenes) + 8), (18, 19, 22, 255))
    d = ImageDraw.Draw(sheet)
    lab = font(True, 16)
    for n, (name, lua_code) in enumerate(scenes):
        y = 8 + n * (H + 34)
        d.text((10, y + 6), name, font=lab, fill=(230, 230, 235, 255))
        sheet.paste(make('LANG = %d; THEME = %d; ' % (LANG_ID, THEME) + lua_code, W, H, place, BG), (0, y + 30))
    sheet.convert('RGB').save(out)
    print('ok', out, sheet.size)
