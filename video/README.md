# Video de Steward (Remotion)

Video de presentación de 63 segundos, en 1920 x 1080 a 30 cuadros por segundo, hecho con [Remotion](https://www.remotion.dev): cada escena es código que dibuja las fotos, los textos y los indicadores reales de la app.

## Qué hay aquí

- `src/guion.ts`: todos los textos y la duración de cada escena. Para cambiar lo que dice el video, se edita este archivo.
- `src/escenas.tsx`: las nueve escenas (intro, límites, contactos, banderas, largadas, sanciones, IA y online, pantalla, cierre).
- `src/componentes.tsx`: piezas comunes (foto con movimiento, tarjeta de texto, indicador, íconos).
- `public/fotos/`: fotos de GT3 en Spa generadas con Gemini.
- `public/hud/`: indicadores de Steward con fondo transparente. Se regeneran desde la raíz del repo con `python3 video/generar_hud.py`, que usa el código real de la app.
- `public/iconos/` y `public/fonts/`: copiados de la app.

## Usarlo

Se necesita Node.js 18 o más nuevo.

```
cd video
npm install
npm run dev      # abre Remotion Studio en el navegador para ver y ajustar el video
npm run render   # crea salida/steward.mp4
```

El video no lleva música; se le puede agregar después en cualquier editor.

Remotion es gratis para personas individuales y equipos de hasta 3 personas (ver https://www.remotion.dev/docs/license/faq).
