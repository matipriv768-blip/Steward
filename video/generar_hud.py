"""Genera los indicadores de Steward con fondo transparente para el video.

Se corre desde la raiz del repo:  python3 video/generar_hud.py
Usa el codigo real de la app (apps/lua/Steward/Steward.lua) a traves del simulador de test/.
Deja los PNG en video/public/hud/, recortados a 1440 x 484.
"""
import os
import sys

os.environ['HUD_GRANDE'] = '1'
sys.path.insert(0, 'test')
import preview_steward as P  # noqa: E402

OUT = 'video/public/hud'
os.makedirs(OUT, exist_ok=True)
BASE = 'T.screenW=1000; T.screenH=1080; T.cfg.hudFixed=true; T.cfg.hudTheme=THEME; T.cfg.hudY=22; T.cfg.lang=LANG; '
CARRERA = 'T.cfg.flEnabled=true; T.sim.timeToSessionStart=-20000; '
FORMACION = ('T.cfg.startMode=2; T.cfg.formShort=true; T.physicsAllowed=true; T.sim.carsCount=2; newSession(); '
             'T.sim.timeToSessionStart=-100; T.cars[0].racePosition=2; T.cars[1].racePosition=1; run(1); '
             'place(1,3200,96); place(0,3190,94); run(8)')
ESCENAS = {
    'limites': CARRERA + 'T.cfg.tlMode=1; local c=place(0,0,150); c.wheelsOutside=4; run(1); c.wheelsOutside=0; run(1)',
    'contacto': CARRERA + 'place(0,0,170); place(1,4.5,150); run(0.5); hit(0); run(0.6)',
    'devolver': CARRERA + 'place(0,0,170); place(1,4.5,150); run(0.5); hit(0); run(0.5); place(0,20,170); run(3); run(6)',
    'amarilla': CARRERA + 'place(0,0,150); place(1,200,0); run(1)',
    'drive': CARRERA + 'T.cfg.tiers=true; T.cfg.pitLimit=82; T.cfg.pitTolerance=0; local c=place(0,0,90); c.isInPitlane=true; run(1); c.isInPitlane=false; place(0,0,150); run(1)',
    'formacion': FORMACION,
    'verde': FORMACION + '; place(1,3420,96); place(0,3410,94); run(1.0)',
}
TEMAS = {'claro': 1, 'oscuro': 2, 'sinfondo': 0}
pedidos = [(n, 'claro') for n in ESCENAS] + [('amarilla', 'oscuro'), ('amarilla', 'sinfondo')]
for nombre, tema in pedidos:
    lua = 'LANG = 1; THEME = %d; ' % TEMAS[tema] + BASE + ESCENAS[nombre]
    img = P.make(lua, 1000, 470, [('fullscreenUI', (0, 0))], 'transparente')
    img = img.crop((280, 456, 1720, 940))
    ruta = '%s/%s-%s.png' % (OUT, nombre, tema)
    img.save(ruta)
    print(ruta, img.getbbox())
