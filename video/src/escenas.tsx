// Las escenas del video, en orden. Cada una dura lo que dice guion.ts.
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLOR, Foto, Hud, Iconos, SANS, SERIF, Sombra, Tarjeta, suave} from './componentes';
import {FUNDIDO, GUION} from './guion';

const g = GUION;

export const Intro: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const letras = g.intro.titulo.split('');
  return (
    <AbsoluteFill>
      <Foto src="atardecer.jpg" dur={g.intro.dur + 30} desde={{zoom: 1.02}} hasta={{zoom: 1.12, x: -1.5, y: 1}} />
      <Sombra fuerza={0.62} />
      <div style={{position: 'absolute', left: 120, top: 330}}>
        <div style={{
          fontFamily: SANS, fontWeight: 600, fontSize: 26, letterSpacing: '0.12em', textTransform: 'uppercase',
          color: 'rgba(255,255,255,0.88)', opacity: suave(f, 6, 26), transform: `translateY(${(1 - suave(f, 6, 26)) * 14}px)`,
        }}>
          {g.intro.antetitulo}
        </div>
        <div style={{display: 'flex', overflow: 'hidden', paddingBottom: 10, marginTop: 6}}>
          {letras.map((l, i) => {
            const a = spring({frame: f - 16 - i * 3, fps, config: {damping: 200}});
            return (
              <span key={i} style={{
                fontFamily: SERIF, fontSize: 250, lineHeight: 1.05, letterSpacing: '-0.03em', color: '#fff',
                display: 'inline-block', transform: `translateY(${(1 - a) * 110}%)`,
              }}>{l}</span>
            );
          })}
        </div>
        <div style={{height: 4, width: 640 * suave(f, 50, 80), backgroundColor: COLOR.senal, margin: '6px 0 30px'}} />
        <div style={{
          fontFamily: SERIF, fontSize: 52, color: '#fff', letterSpacing: '-0.01em',
          opacity: suave(f, 70, 95), transform: `translateY(${(1 - suave(f, 70, 95)) * 16}px)`,
        }}>
          {g.intro.lema}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const Limites: React.FC = () => (
  <AbsoluteFill>
    <Foto src="atardecer.jpg" dur={g.limites.dur + 15} desde={{zoom: 1.3, x: 9, y: -3}} hasta={{zoom: 1.42, x: 11, y: -5}} />
    <Sombra lado="abajo" fuerza={0.45} />
    <Hud src="limites-claro.png" entra={22} />
    <Tarjeta {...g.limites} />
  </AbsoluteFill>
);

export const Contactos: React.FC = () => (
  <AbsoluteFill>
    <Foto src="lado_a_lado.jpg" dur={g.contactos.dur + 15} desde={{zoom: 1.04}} hasta={{zoom: 1.16, x: -3, y: 1}} />
    <Sombra lado="abajo" fuerza={0.45} />
    <Hud src="contacto-claro.png" entra={20} sale={112} />
    <Hud src="devolver-claro.png" entra={124} />
    <Tarjeta {...g.contactos} />
  </AbsoluteFill>
);

// Banderas e íconos centrados abajo, después de que sale la tarjeta
const FilaIconos: React.FC<{items: [string, string][]; entra: number}> = ({items, entra}) => (
  <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center'}}>
    <div style={{marginBottom: 90}}>
      <Iconos items={items} entra={entra} cada={4} columnas={items.length} tam={110} enLinea />
    </div>
  </AbsoluteFill>
);

export const Banderas: React.FC = () => (
  <AbsoluteFill>
    <Foto src="banderillero.jpg" dur={g.banderas.dur + 15} desde={{zoom: 1.04}} hasta={{zoom: 1.14, x: -2}} />
    <Sombra lado="abajo" fuerza={0.5} />
    <Hud src="amarilla-claro.png" entra={18} />
    <Tarjeta {...g.banderas} sale={118} />
    <FilaIconos
      entra={130}
      items={[
        ['bandera_verde', 'Verde'], ['bandera_amarilla', 'Amarilla'], ['bandera_amarilla_total', 'Amarilla total'],
        ['bandera_roja', 'Roja'], ['bandera_azul', 'Azul'], ['bandera_blanca', 'Blanca'],
        ['bandera_cuadros', 'A cuadros'], ['bandera_negra', 'Negra'],
      ]}
    />
  </AbsoluteFill>
);

export const Largada: React.FC = () => (
  <AbsoluteFill>
    <Foto src="largada.jpg" dur={g.largada.dur + 15} desde={{zoom: 1.03}} hasta={{zoom: 1.14, y: 2}} />
    <Sombra lado="abajo" fuerza={0.45} />
    <Hud src="formacion-claro.png" entra={18} sale={124} />
    <Hud src="verde-claro.png" entra={134} />
    <Tarjeta {...g.largada} />
  </AbsoluteFill>
);

export const Sanciones: React.FC = () => (
  <AbsoluteFill>
    <Foto src="pits.jpg" dur={g.sanciones.dur + 15} desde={{zoom: 1.04}} hasta={{zoom: 1.15, x: -2.5}} />
    <Sombra lado="abajo" fuerza={0.5} />
    <Hud src="drive-claro.png" entra={18} />
    <Tarjeta {...g.sanciones} sale={124} />
    <FilaIconos
      entra={136}
      items={[
        ['tiempo', 'Tiempo'], ['levantar', 'Levantar el pie'], ['drive_through', 'Drive-through'],
        ['stop_and_go', 'Stop and go'], ['devolver', 'Devolver'], ['descalificado', 'Descalificado'],
      ]}
    />
  </AbsoluteFill>
);

export const Modos: React.FC = () => {
  const f = useCurrentFrame();
  const bloque = (linea: string, detalle: string, entra: number) => {
    const a = suave(f, entra, entra + 22);
    return (
      <div style={{opacity: a, transform: `translateY(${(1 - a) * 30}px)`, marginBottom: 56}}>
        <div style={{fontFamily: SERIF, fontSize: 110, lineHeight: 1.04, letterSpacing: '-0.025em', color: '#fff'}}>{linea}</div>
        <div style={{fontFamily: SANS, fontSize: 32, lineHeight: 1.4, color: 'rgba(255,255,255,0.82)', marginTop: 14, maxWidth: 1100}}>{detalle}</div>
      </div>
    );
  };
  return (
    <AbsoluteFill>
      <Foto src="largada.jpg" dur={g.modos.dur + 15} desde={{zoom: 1.1}} hasta={{zoom: 1.18, y: -1}} desenfoque={14} oscurecer={0.5} />
      <div style={{position: 'absolute', left: 140, top: 250}}>
        {bloque(g.modos.linea1, g.modos.detalle1, 12)}
        {bloque(g.modos.linea2, g.modos.detalle2, 70)}
      </div>
    </AbsoluteFill>
  );
};

export const Pantalla: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const cortes = [0, 62, 122];
  const activo = f < cortes[1] ? 0 : f < cortes[2] ? 1 : 2;
  const nombres = ['Claro', 'Oscuro', 'Sin fondo'];
  const a = spring({frame: f - 12, fps, config: {damping: 200}});
  return (
    <AbsoluteFill>
      <Foto src="lado_a_lado.jpg" dur={g.pantalla.dur + 15} desde={{zoom: 1.16, x: -3, y: 1}} hasta={{zoom: 1.22, x: -4, y: 1}} />
      <Sombra lado="abajo" fuerza={0.45} />
      <Hud src="amarilla-claro.png" entra={10} sale={cortes[1] - 4} />
      <Hud src="amarilla-oscuro.png" entra={cortes[1] + 2} sale={cortes[2] - 4} />
      <Hud src="amarilla-sinfondo.png" entra={cortes[2] + 2} />
      <div style={{
        position: 'absolute', left: 96, bottom: 96, width: 820, padding: '40px 46px 44px', borderRadius: 28,
        backgroundColor: 'rgba(254,255,252,0.86)', backdropFilter: 'blur(18px)', border: '1px solid rgba(255,255,255,0.65)',
        boxShadow: '0 18px 50px rgba(0,0,0,0.22)', opacity: a, transform: `translateY(${(1 - a) * 46}px)`,
      }}>
        <div style={{fontFamily: SANS, fontWeight: 600, fontSize: 21, letterSpacing: '0.08em', textTransform: 'uppercase', color: COLOR.ceniza}}>
          {g.pantalla.antetitulo}
        </div>
        <div style={{fontFamily: SERIF, fontSize: 70, lineHeight: 1.06, letterSpacing: '-0.02em', color: COLOR.tinta, margin: '14px 0 20px'}}>
          {g.pantalla.titulo}
        </div>
        <div style={{fontFamily: SANS, fontSize: 29, lineHeight: 1.42, color: COLOR.carbon}}>{g.pantalla.texto}</div>
        <div style={{display: 'flex', gap: 12, marginTop: 28}}>
          {nombres.map((n, i) => (
            <div key={n} style={{
              fontFamily: SANS, fontWeight: 600, fontSize: 24, padding: '12px 22px', borderRadius: 12,
              border: `1.5px solid ${i === activo ? COLOR.ocaso : COLOR.niebla}`,
              backgroundColor: i === activo ? COLOR.ocaso : 'transparent', color: i === activo ? '#fff' : COLOR.carbon,
            }}>{n}</div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const Cierre: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const largo = g.cierre.dur + FUNDIDO; // la escena empieza un fundido antes
  const a = spring({frame: f - 10, fps, config: {damping: 200}});
  const negro = interpolate(f, [largo - 24, largo - 2], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill>
      <Foto src="atardecer.jpg" dur={g.cierre.dur} desde={{zoom: 1.12, x: -1.5, y: 1}} hasta={{zoom: 1.2, x: -2, y: 1.5}} oscurecer={0.42} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center'}}>
        <div style={{opacity: a, transform: `translateY(${(1 - a) * 30}px)`}}>
          <div style={{fontFamily: SERIF, fontSize: 230, lineHeight: 1, letterSpacing: '-0.03em', color: '#fff'}}>{g.cierre.titulo}</div>
          <div style={{fontFamily: SANS, fontSize: 36, color: 'rgba(255,255,255,0.88)', margin: '26px 0 40px', opacity: suave(f, 30, 50)}}>
            {g.cierre.texto}
          </div>
          <div style={{
            display: 'inline-block', fontFamily: SANS, fontWeight: 600, fontSize: 32, color: '#fff', padding: '18px 30px', borderRadius: 14,
            border: `2px solid ${COLOR.senal}`, backgroundColor: 'rgba(31,31,41,0.55)', opacity: suave(f, 48, 68),
          }}>
            {g.cierre.link}
          </div>
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{backgroundColor: '#000', opacity: negro}} />
    </AbsoluteFill>
  );
};
