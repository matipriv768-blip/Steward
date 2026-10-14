// Piezas que usan todas las escenas: fotos con movimiento, tarjetas de texto, indicadores e íconos.
import React, {useEffect, useState} from 'react';
import {
  AbsoluteFill, Easing, Img, continueRender, delayRender, interpolate, spring, staticFile,
  useCurrentFrame, useVideoConfig,
} from 'remotion';

// Colores y letras de Steward (los mismos de la app y de la web)
export const COLOR = {
  pergamino: '#fefffc', tinta: '#2c2c2c', carbon: '#444141', ceniza: '#646464', niebla: '#dee2de',
  crepusculo: '#1f1f29', ocaso: '#282834', senal: '#41a1cf', senalTexto: '#1f78ad',
};
export const SERIF = 'Fraunces, Georgia, serif';
export const SANS = 'Inter, Arial, sans-serif';

const FUENTES: [string, string, string][] = [
  ['Fraunces', 'Fraunces-400.ttf', '400'],
  ['Inter', 'Inter-400.ttf', '400'],
  ['Inter', 'Inter-600.ttf', '600'],
  ['Inter', 'Inter-700.ttf', '700'],
];

// Espera a que carguen las letras antes de dibujar el primer cuadro
export const useFuentes = () => {
  const [espera] = useState(() => delayRender('Cargando letras'));
  useEffect(() => {
    Promise.all(FUENTES.map(([familia, archivo, peso]) =>
      new FontFace(familia, `url(${staticFile('fonts/' + archivo)})`, {weight: peso}).load()
        .then((f) => { (document.fonts as unknown as {add: (x: FontFace) => void}).add(f); })))
      .catch((e) => console.error(e))
      .finally(() => continueRender(espera));
  }, [espera]);
};

const suave = (f: number, desde: number, hasta: number) =>
  interpolate(f, [desde, hasta], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});

// Encuadre de una foto: zoom y desplazamiento en % (positivo = la foto se corre a la derecha / abajo)
type Encuadre = {zoom: number; x?: number; y?: number};

export const Foto: React.FC<{
  src: string; dur: number; desde: Encuadre; hasta: Encuadre; desenfoque?: number; oscurecer?: number;
}> = ({src, dur, desde, hasta, desenfoque = 0, oscurecer = 0}) => {
  const f = useCurrentFrame();
  const p = suave(f, 0, dur);
  const zoom = desde.zoom + (hasta.zoom - desde.zoom) * p;
  const x = (desde.x ?? 0) + ((hasta.x ?? 0) - (desde.x ?? 0)) * p;
  const y = (desde.y ?? 0) + ((hasta.y ?? 0) - (desde.y ?? 0)) * p;
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: '#14141a'}}>
      <Img
        src={staticFile('fotos/' + src)}
        style={{
          width: '100%', height: '100%', objectFit: 'cover',
          transform: `scale(${zoom}) translate(${x}%, ${y}%)`,
          filter: desenfoque ? `blur(${desenfoque}px)` : undefined,
        }}
      />
      {oscurecer > 0 && <AbsoluteFill style={{backgroundColor: `rgba(16,16,24,${oscurecer})`}} />}
    </AbsoluteFill>
  );
};

// Degradado para que el texto se lea sobre la foto
export const Sombra: React.FC<{lado?: 'izquierda' | 'abajo'; fuerza?: number}> = ({lado = 'izquierda', fuerza = 0.55}) => (
  <AbsoluteFill
    style={{
      background: lado === 'izquierda'
        ? `linear-gradient(90deg, rgba(14,14,20,${fuerza}) 0%, rgba(14,14,20,${fuerza * 0.4}) 45%, rgba(14,14,20,0) 70%)`
        : `linear-gradient(0deg, rgba(14,14,20,${fuerza}) 0%, rgba(14,14,20,0) 55%)`,
    }}
  />
);

// Tarjeta de texto esmerilada, abajo a la izquierda (el mismo estilo de la web)
export const Tarjeta: React.FC<{antetitulo: string; titulo: string; texto: string; entra?: number; sale?: number}> = ({
  antetitulo, titulo, texto, entra = 12, sale,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spring({frame: f - entra, fps, config: {damping: 200}});
  const fuera = sale === undefined ? 1 : 1 - suave(f, sale, sale + 12);
  return (
    <div
      style={{
        position: 'absolute', left: 96, bottom: 96, width: 820, padding: '40px 46px 46px', borderRadius: 28,
        backgroundColor: 'rgba(254,255,252,0.86)', backdropFilter: 'blur(18px)',
        border: '1px solid rgba(255,255,255,0.65)', boxShadow: '0 18px 50px rgba(0,0,0,0.22)',
        opacity: a * fuera, transform: `translateY(${(1 - a) * 46}px)`,
      }}
    >
      <div style={{fontFamily: SANS, fontWeight: 600, fontSize: 21, letterSpacing: '0.08em', textTransform: 'uppercase', color: COLOR.ceniza}}>
        {antetitulo}
      </div>
      <div style={{fontFamily: SERIF, fontSize: 70, lineHeight: 1.06, letterSpacing: '-0.02em', color: COLOR.tinta, margin: '14px 0 20px'}}>
        {titulo}
      </div>
      <div style={{fontFamily: SANS, fontSize: 29, lineHeight: 1.42, color: COLOR.carbon, letterSpacing: '-0.01em'}}>{texto}</div>
    </div>
  );
};

// Indicador real de la app (PNG generado con video/generar_hud.py), arriba al centro como en el juego
export const Hud: React.FC<{src: string; entra?: number; sale?: number; y?: number}> = ({src, entra = 18, sale, y = 54}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spring({frame: f - entra, fps, config: {damping: 18, stiffness: 140}});
  const fuera = sale === undefined ? 1 : 1 - suave(f, sale, sale + 10);
  return (
    <Img
      src={staticFile('hud/' + src)}
      style={{
        position: 'absolute', left: '50%', top: y, width: 1382,
        transform: `translateX(-50%) translateY(${(1 - a) * -24}px) scale(${0.96 + 0.04 * a})`, transformOrigin: 'top center',
        opacity: Math.min(1, a) * fuera, filter: 'drop-shadow(0 10px 24px rgba(0,0,0,0.25))',
      }}
    />
  );
};

// Fila de íconos de la app, cada uno con su nombre, entrando uno tras otro
export const Iconos: React.FC<{items: [string, string][]; entra: number; cada?: number; columnas?: number; tam?: number; enLinea?: boolean}> = ({
  items, entra, cada = 5, columnas = 4, tam = 104, enLinea = false,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <div
      style={{
        ...(enLinea ? {} : {position: 'absolute' as const, right: 96, bottom: 96}), display: 'grid', gridTemplateColumns: `repeat(${columnas}, ${tam + 44}px)`,
        gap: 14,
      }}
    >
      {items.map(([archivo, nombre], i) => {
        const a = spring({frame: f - entra - i * cada, fps, config: {damping: 14, stiffness: 160}});
        return (
          <div
            key={archivo + i}
            style={{
              padding: '14px 6px 14px', borderRadius: 18, textAlign: 'center',
              backgroundColor: 'rgba(254,255,252,0.86)', backdropFilter: 'blur(14px)', border: '1px solid rgba(255,255,255,0.65)',
              opacity: Math.min(1, a), transform: `translateY(${(1 - a) * 30}px) scale(${0.85 + 0.15 * a})`,
            }}
          >
            <Img src={staticFile('iconos/' + archivo + '.png')} style={{width: tam, height: tam * 0.69, objectFit: 'contain', display: 'block', margin: '0 auto 8px'}} />
            <div style={{fontFamily: SANS, fontWeight: 600, fontSize: 17, lineHeight: 1.2, color: COLOR.tinta}}>{nombre}</div>
          </div>
        );
      })}
    </div>
  );
};

// Fundido de entrada para encadenar escenas
export const Fundido: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{opacity: suave(f, 0, dur)}}>{children}</AbsoluteFill>;
};

export {suave};
