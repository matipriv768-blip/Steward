# Traspaso del proyecto Steward

Escrito el 10 de noviembre de 2026, al pasar el proyecto a una sesión nueva. `CLAUDE.md` tiene las reglas fijas del código. Este archivo cuenta en qué estado quedó todo, qué se decidió y por qué, qué falta y qué trampas ya se pisaron. Léelos los dos antes de tocar algo.

## 1. Qué es y en qué estado está

Steward es una app Lua para Assetto Corsa con Custom Shaders Patch (CSP), hecha por Matías desde cero. Antes se llamaba Comisario. Hace de comisario de carrera, offline y online:

- límites de pista y salidas de pista;
- contactos con autos y golpes contra el muro;
- puntos de incidente;
- banderas;
- largada parada y lanzada;
- sanciones reales para el piloto y para la IA.

| Qué | Estado |
| - | - |
| Repo | https://github.com/matipriv768-blip/Steward (público, rama `main`). Todo está subido; el último commit es `927e246`. |
| Versión en el repo | 2.2.0, con el estilo Cristal en rojo F1 y la letra Saira. |
| Versión instalada en el PC de Matías | 2.1.0. La 2.2.0 todavía no la copia al juego ni se ha visto en pantalla real. |
| Releases publicadas en GitHub | v1.5.0, v1.6.3, v1.6.4 y v2.0.0. Faltan la 2.1.0 y la 2.2.0, que las publica él (ver 7). |
| Script del servidor | 1.14, sin cambios desde la 2.0. Vive en su gist. |
| Pruebas | 501 traducciones, 218/218, 21/21 y 42/42. GitHub Actions las pasa en verde. |
| Sitio web | https://matipriv768-blip.github.io/Steward/ (sale de `docs/`). Todavía muestra el diseño de la 2.0. |
| Respaldo | Tag `respaldo-2026-11-10` en GitHub, más un zip con el historial completo (ver 9). |

## 2. Cómo trabajar con Matías

- Es estudiante de Ingeniería en Administración de Empresas en Chile. No sabe programar.
- Escríbele siempre en español de Chile, claro y directo. Una vez se molestó por una respuesta en inglés.
- Cuando él tenga que hacer algo, dale pasos numerados en el orden exacto, sin dar nada por sabido: la ruta completa de la carpeta, qué botón apretar.
- Escribe mensajes cortos y con faltas ("el efectao crsital transparente q pusimos, dejalo en rojo"). Interpreta la intención; pregunta solo si de verdad no se entiende.
- Si no estás seguro de algo, dilo. Si su idea tiene un problema, díselo antes de programarla.
- Evita palabras que suenan a texto de IA: además, cabe destacar, crucial, fundamental, esencial, vital, integral, transformar, fomentar, aprovechar, optimizar, "no solo... sino también", en conclusión, en resumen.
- Las notas de versión para GitHub las quiere en texto plano, sin Markdown.
- Cada vez que cambie `servidor/comisario_servidor.lua`, recuérdale pegarlo en el gist y pásale los dos links:
  - Editar: https://gist.github.com/matipriv768-blip/3d8548a91410b553ecd85a07440cbccf/edit
  - Ver (para sacar el Raw): https://gist.github.com/matipriv768-blip/3d8548a91410b553ecd85a07440cbccf
- Cuando le entregues una versión, mándale el zip y una imagen de vista previa (`test/preview_steward.py`). Él revisa el aspecto mirando la imagen.

## 3. Lo que Matías quiere del reglamento (decisiones ya tomadas)

No las cambies sin preguntarle. Varias salen de cosas que le molestaron probando.

- Un solo reglamento por defecto. No quiere elegir entre "real", "iRacing" y otros.
- El estilo es iRacing realista: chocar a un auto sanciona, y un roce leve ("chapa chapa") no sanciona.
- Por sesión:
  - en práctica solo se cuenta, no se sanciona;
  - en clasificación la única sanción es invalidar la vuelta.
- Si pierdes el control y después chocas un auto o una pared, ese choque también cuenta.
- La IA sancionada tiene que soltar el acelerador. No se le limita la velocidad, porque eso causaba más accidentes.
- Ir a pits por salirse de la pista 3 veces le parece mucho.
- Hay un cronómetro invisible estilo iRacing: una misma salida de pista no se cuenta dos veces.
- Con 17 puntos de incidente el piloto queda descalificado. La descalificación tiene que ser efectiva: el piloto no puede seguir corriendo ni ganar. Online, el servidor lo manda a pits con el auto sin controles, porque sus amigos no la iban a respetar.
- Se puede devolver la posición tras un accidente o un adelantamiento ilegal, o si no, ir a boxes.
- Largada lanzada:
  - salida corta, partiendo en la última o penúltima curva;
  - velocímetro de formación como en ACC;
  - semáforo verde animado.
- Online, solo él como administrador cambia la configuración. A sus amigos solo se les impone la largada y se les obliga a cumplir las sanciones.
- Online corren él y sus amigos, sin IA. Cada amigo instala la app; el servidor lo arma él con Content Manager en su PC.
- Al terminar, un aviso dice quién ganó.
- Es código abierto para que la comunidad lo arregle. No se copia código de otros plugins, tampoco de Real Penalty.

## 4. Historia reciente (lo que se hizo en la última sesión)

### 2.1.0

- Corregido el falso "golpe contra el muro" al pasar por un piano grueso con el F1 2006. El salto vertical se sumaba como golpe. Ahora:
  - se mide solo la velocidad horizontal;
  - el auto tiene que terminar más lento de lo que entró (pérdida neta de al menos `wallMinKmh/3`);
  - el umbral es `RS.WALL_G = 6`, o `RS.WALL_G_KERB = 10` si alguna rueda va sobre piano.
- `RS.onKerb` lee `car.wheels[k].surfaceExtendedType == ac.SurfaceExtendedType.Kerb` dentro de `pcall`. En el juego funciona: el registro anota "Pianos: el juego informa la superficie de las ruedas".
- Lo descartado queda en el registro con las dos medidas. Se probó en Spa con la IA (De la Rosa, Triviño, Barrichello): tres pisadas de piano de 15 a 19 km/h que antes contaban como muro ahora se descartan. Los golpes reales en su registro anterior eran de 16 a 25 km/h.
- Cada indicador se acomoda por separado: `FIXED_ORDER` (Status, Start, Msg, Pen), ajustes `hud<Clave>X/Y/S/On`, `hudFree`, y un mapa para arrastrar (`W.layoutMap`).
- Nuevo estilo Medianoche (estilo Raycast).

### 2.2.0

- Estilo Cristal, inspirado en un dashboard de vidrio oscuro que él mandó. Primero era azul y después lo pidió en rojo F1:
  - brillo `#e10600`;
  - marca `#ff3b30`;
  - fondos oscuros con tinte rojizo;
  - texto blanco;
  - el rojo de las sanciones quedó más rosado (`#ff5468`) para que se lea sobre la tarjeta.
- Letra Saira. Pidió "la letra de los juegos de F1", pero la oficial (Formula1 Display) es privada y no se puede incluir. Saira tiene licencia OFL y no declara nombre reservado. Se fijaron tres cortes a partir de la variable de Google Fonts, con el instanciador de fontTools, reducidos a letras latinas y con el nombre cambiado:
  - `Saira-400.ttf`
  - `Saira-600.ttf`
  - `SairaExpanded-700.ttf`
- Al actualizar, todos pasan una vez a Cristal: migración `uiVersion < 6` → `hudTheme = 3`.

### Probado en el juego (con permiso, en su PC)

- Funcionan:
  - el arreglo de los pianos;
  - la FCY;
  - la bandera azul;
  - los avisos de contacto de la IA;
  - arrastrar, el tamaño y que se guarde.
- No se pudieron probar las sanciones al piloto (límites, pits, salto en la largada): no se pudo manejar con su control de Xbox desde el control remoto.

## 5. Pendiente

1. Ver la 2.2.0 dentro del juego (Cristal rojo, Saira) y confirmar que se lee bien en pantalla real.
2. Probar las sanciones al piloto manejando él.
3. Publicar las releases v2.1.0 y v2.2.0 en GitHub (las hace él; dale los pasos y el texto en texto plano).
4. Sitio web y video. Muestran el diseño de la 2.0, así que cuando quiera habrá que:
   - regenerar las imágenes (`python3 video/generar_hud.py` y las capturas de `docs/`);
   - actualizar `web/textos.py`.
5. Se le ofreció usar Saira en los otros estilos; no ha respondido.

## 6. Cómo se prueba sin el juego

Se necesita Python 3 y `pip install lupa`. Desde la raíz:

```
python3 test/check_i18n.py apps/lua/Steward/Steward.lua
python3 test/run_tests.py apps/lua/Steward/Steward.lua
python3 test/run_online.py apps/lua/Steward/Steward.lua
python3 test/run_server.py servidor/comisario_servidor.lua
python3 test/preview_steward.py vista.png es cristal      # medianoche, claro, sinfondo
python3 test/preview_settings.py ajustes.png es
python3 herramientas/empaquetar.py                          # crea Steward-<version>.zip
```

`test/harness.lua` simula la API de CSP. Solo acepta funciones de `ui` que estén en su lista `known`; una función nueva da el error "Funcion de ui no verificada". Si usas una función nueva del SDK (verificada en `acc-lua-sdk`), agrégala ahí y en `preview_steward.py` si dibuja algo.

## 7. Cómo publica Matías una release (pásale esto)

1. Entrar a https://github.com/matipriv768-blip/Steward/releases.
2. Apretar "Draft a new release".
3. En "Choose a tag" escribir `v2.2.0` y elegir "Create new tag".
4. Título: `Steward 2.2.0`.
5. Pegar la descripción en texto plano (se saca de la entrada de `CHANGELOG.md`, sin asteriscos ni almohadillas).
6. Arrastrar el zip `Steward-2.2.0.zip` donde dice "Attach binaries".
7. Apretar "Publish release".

## 8. Su PC y cómo probar en el juego

- Windows. El nombre del equipo es `desktop-k28ghmj` y el usuario es `Cerix`.
- Assetto Corsa por Steam, con Content Manager y CSP de pago (Preview, con Rain FX). Tiene muchas apps Lua instaladas: CMRT HUD, PitWall (otro proyecto suyo), CrashCam y otras.
- Rutas:
  - App instalada: `C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\apps\lua\Steward`
  - Ajustes guardados de la app: `C:\Users\Cerix\Documents\Assetto Corsa\cfg\extension\state\lua\app\Steward.ini`
  - Registro: `C:\Users\Cerix\Documents\Assetto Corsa\logs\steward_log.txt`
- La carpeta `apps\lua\Comisario` es el aviso vacío (`-- STEWARD_STUB`). No la borres.
- Para instalar una versión, él:
  1. descomprime el zip;
  2. copia la carpeta `apps` dentro de `C:\Program Files (x86)\Steam\steamapps\common\assettocorsa`;
  3. acepta reemplazar los archivos.
- Si la sesión está vinculada a su PC con la app de escritorio de Claude, se puede copiar la app directo y leer el registro.
- Trampas al probar en su PC:
  - No abras Assetto Corsa con `open_application("Acs")` si ya está abierto: lanza una segunda instancia.
  - La ventana de Claude escritorio a veces salta encima del juego. No hagas clic en ella.
  - Al escribir archivos con `device_commit_files`, usa una ruta de preparación nueva cada vez. Si se repite, escribe la copia vieja que quedó en caché.
  - Cuando termines de probar, apaga el PC solo si él lo pidió (una vez lo pidió).

## 9. Trampas del código ya conocidas

- Lua admite 200 variables locales por archivo y `Steward.lua` (unas 5.500 líneas) está en el tope:
  - todo lo nuevo va dentro de `W`, `HX` o `RS`;
  - un `for` suelto al nivel del archivo también cuenta (por eso existe `RS.styleWindows()`).
- `RS` se declara arriba, junto a `RP`, para usarlo desde cualquier sección.
- Los estilos de `hudTheme`:
  - 0 sin fondo, 1 claro, 2 Medianoche, 3 Cristal (el de fábrica);
  - `HX.dark = theme >= 2`;
  - un valor desconocido cae en claro.
- Colores y letras de los estilos:
  - los colores de los indicadores están en `HX.PAL`, los de las ventanas en `RS.tint()` y la lista de estilos en `RS.styleList()`;
  - las letras se eligen con `HX.font` (en Cristal salen de `HX.F.race`).
- Las barras con relleno pasan por `HX.fill`, que en Cristal dibuja franjas dentro de `pushClipRect`/`popClipRect`. Las pruebas revisan que el push y el pop queden parejos.
- Las claves online siguen llamándose `comisario:*` a propósito, y `comisario:reglas:8` es la versión actual del formato. Los mensajes online pesan menos de 175 bytes y van con al menos 200 ms entre uno y otro.
- El mapa de los indicadores va antes de los deslizadores de la columna. Si van después, el mapa salta al cambiar de modo a mitad de un arrastre.
- `/home/claude/comisario` es un clon viejo del repo con el nombre anterior. No lo uses.

## 10. Privacidad y commits

- Nunca subas al repo ni al gist claves de API reales ni su clave de administrador real. En los ejemplos se usa `tuclave`.
- Si algo necesita una clave, va en `.env`, que está en `.gitignore`.
- El correo de los commits es `matipriv768-blip@users.noreply.github.com`. No uses su correo personal en servicios externos.
- La letra oficial de la F1 no entra al repo.

## 11. Respaldo del 10 de noviembre de 2026

- En GitHub: el tag `respaldo-2026-11-10` apunta al estado exacto de este traspaso. Para volver ahí: `git checkout respaldo-2026-11-10`.
- En su PC: `C:\Users\Cerix\Documents\Assetto Corsa\Steward respaldo 2026-11-10\`. Ahí están:
  - `Steward-respaldo-2026-11-10.zip`, con el repo completo, su historial (`steward.bundle`, se restaura con `git clone steward.bundle Steward`) y el zip de la 2.2.0;
  - una copia de la app 2.1.0 que estaba instalada;
  - una copia de sus ajustes (`Steward.ini`).
