# Steward: guía para Claude Code

Steward (antes se llamaba Comisario) es una app Lua para Assetto Corsa con Custom Shaders Patch (CSP). Hace de comisario de carrera: límites de pista, contactos, puntos de incidente, banderas, largadas parada y lanzada, y sanciones reales para el piloto y para la IA, offline y online. El autor es Matías.

## Cómo trabajar con Matías

- Escríbele en español de Chile, claro y directo. No tiene experiencia programando: cuando tenga que hacer algo él (instalar, probar en el juego, subir una versión), dale pasos numerados, en el orden en que los va a hacer, sin dar nada por sabido.
- Si no estás seguro de algo (una función de CSP, una ruta en su PC, un dato), dilo en vez de suponer.
- Si su idea tiene un problema, díselo directo antes de programarla.
- Las notas de versión para GitHub las prefiere en texto plano, sin Markdown.
- Cada vez que cambie `servidor/comisario_servidor.lua`, recuérdale que tiene que pegar el archivo nuevo en el gist, y pásale siempre estos dos links:
  - Editar: https://gist.github.com/matipriv768-blip/3d8548a91410b553ecd85a07440cbccf/edit
  - Ver: https://gist.github.com/matipriv768-blip/3d8548a91410b553ecd85a07440cbccf

## Estructura

| Ruta | Qué es |
| - | - |
| `apps/lua/Steward/Steward.lua` | Toda la app (unas 5.000 líneas, en secciones numeradas). |
| `apps/lua/Steward/manifest.ini` | Ventanas de la app y versión. |
| `apps/lua/Steward/img/` | Íconos claros en 48, 80 y 160 px; `img/oscuro/` son los del estilo oscuro. |
| `apps/lua/Steward/fonts/` | Fraunces e Inter (licencia OFL), que la app carga con DWrite. |
| `apps/lua/Comisario/` | Aviso vacío que reemplaza la app vieja de quien venía de Comisario. Su `Comisario.lua` empieza con `-- STEWARD_STUB`; no borres esa marca, la app la usa para saber que no es la versión vieja. |
| `servidor/comisario_servidor.lua` | Script online del servidor (versión 1.14). El servidor lo carga desde el gist. |
| `test/` | Simulador de la API de CSP (`harness.lua`) y las pruebas. |
| `arte/` | Generadores de íconos y logo. |
| `web/` y `docs/` | El sitio web. `docs/` es lo que publica GitHub Pages; se genera con `web/`. |
| `herramientas/empaquetar.py` | Arma el zip de una versión. |

## Pruebas (córrelas siempre antes de un commit)

Se necesita Python 3 y `pip install lupa`.

```
python3 test/check_i18n.py apps/lua/Steward/Steward.lua
python3 test/run_tests.py apps/lua/Steward/Steward.lua
python3 test/run_online.py apps/lua/Steward/Steward.lua
python3 test/run_server.py servidor/comisario_servidor.lua
```

En la versión 2.0.0 dan: 484 traducciones sin problemas, 209/209, 21/21 y 42/42. GitHub Actions corre lo mismo en cada push (`.github/workflows/pruebas.yml`). Si agregas o cambias una regla, agrega una prueba que falle sin tu cambio.

Para revisar el diseño sin abrir el juego:

- `python3 test/preview_settings.py salida.png es` dibuja la ventana de ajustes (`en` para inglés).
- `python3 test/preview_steward.py salida.png es claro` dibuja los indicadores (`oscuro` o `sinfondo` para los otros estilos).

## Reglas del código

- Usa solo funciones de CSP verificadas en el SDK oficial (`acc-lua-sdk`). Las dudosas van dentro de `pcall`.
- Lua admite 200 variables locales por archivo y la app está cerca del tope. Lo nuevo va dentro de una tabla existente (`W` para los ajustes, `HX` para los indicadores, `RS` para cosas de Steward).
- Los textos que ve el piloto se escriben en español dentro de `tr('...')`, y la traducción va en la tabla `EN` al final del archivo, con los mismos huecos (`%s`, `%d`) en el mismo orden. El mensaje grande del juego no admite tildes: pasa por `plain()`.
- Los ajustes nuevos van en `DEFAULTS` con un valor que no cambie el comportamiento anterior. Si son parte del reglamento, también van en `RULE_KEYS`, y hay que subir el número de la clave `comisario:reglas:N` (hoy es 8), porque cambia el formato del mensaje online.
- Las claves online siguen llamándose `comisario:*` a propósito, para no romper la compatibilidad con el script del servidor ni con versiones anteriores. No las renombres.
- Los mensajes online viajan por el chat del servidor: menos de 175 bytes y al menos 200 ms entre uno y otro.
- Los indicadores tienen tres estilos (`hudTheme`: 0 sin fondo, 1 claro, 2 oscuro) con sus colores en `HX.PAL`. Los títulos de las tarjetas van en Fraunces y en tipo oración (`HX.sentence`).
- Los ajustes de quien venía de Comisario se copian una sola vez desde `Comisario.ini` (`RS.migrate`).
- No copies código de otros plugins.

## Publicar una versión

1. Sube la versión en `Steward.lua` (`local VERSION`) y en `manifest.ini`, y escribe la entrada en `CHANGELOG.md`.
2. Corre las cuatro pruebas.
3. `python3 herramientas/empaquetar.py` crea `Steward-<versión>.zip` (el zip no se sube al repo; está en `.gitignore`).
4. En GitHub, Releases > Draft a new release, tag `v<versión>`, adjuntar el zip y pegar la descripción en texto plano.

## Sitio web

`python3 web/construir_web.py docs` regenera `docs/index.html` a partir de `web/textos.py` (español e inglés) y `web/ilustraciones.py`. Las fotos están en `docs/assets/fotos` y los scripts que las preparan en `web/fotos/`. GitHub Pages publica `main` / `docs` en https://matipriv768-blip.github.io/Steward/.

## Probar en el juego

La app se instala copiando la carpeta `apps/lua/Steward` dentro de la carpeta de Assetto Corsa (en Steam suele ser `steamapps/common/assettocorsa`, pero confirma la ruta en el PC de Matías antes de copiar). El registro queda en `Documentos/Assetto Corsa/logs/steward_log.txt`; pídeselo cuando algo falle en el juego.
