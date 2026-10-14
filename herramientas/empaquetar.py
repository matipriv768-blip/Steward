"""Arma el zip de una version para subirlo a GitHub (Releases).

Uso:  python3 herramientas/empaquetar.py
Sale: Steward-<version>.zip en la raiz del repo, con la version que diga apps/lua/Steward/manifest.ini.

El zip lleva apps/lua/Steward (la app) y apps/lua/Comisario (un aviso vacio que reemplaza
la app vieja de quien venga de Comisario). Content Manager lo instala arrastrandolo a su ventana.
"""
import os
import re
import sys
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
manifest = open(os.path.join(RAIZ, 'apps/lua/Steward/manifest.ini'), encoding='utf-8').read()
m = re.search(r'^VERSION\s*=\s*(\S+)', manifest, re.M)
if not m:
    sys.exit('No encontre VERSION en manifest.ini')
version = m.group(1)

lua = open(os.path.join(RAIZ, 'apps/lua/Steward/Steward.lua'), encoding='utf-8').read()
v = re.search(r"VERSION\s*=\s*'([^']+)'", lua)
if v and v.group(1) != version:
    sys.exit('La version de Steward.lua (%s) no coincide con manifest.ini (%s)' % (v.group(1), version))

salida = os.path.join(RAIZ, 'Steward-%s.zip' % version)
with zipfile.ZipFile(salida, 'w', zipfile.ZIP_DEFLATED) as z:
    for carpeta in ('apps/lua/Steward', 'apps/lua/Comisario'):
        for base, _, archivos in os.walk(os.path.join(RAIZ, carpeta)):
            for nombre in sorted(archivos):
                if nombre.endswith('.pyc'):
                    continue
                ruta = os.path.join(base, nombre)
                z.write(ruta, os.path.relpath(ruta, RAIZ))
print('Listo:', salida)
