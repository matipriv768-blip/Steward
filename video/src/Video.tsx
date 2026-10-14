// Encadena las escenas con un fundido entre una y otra.
import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {Fundido, useFuentes} from './componentes';
import {Banderas, Cierre, Contactos, Intro, Largada, Limites, Modos, Pantalla, Sanciones} from './escenas';
import {FUNDIDO, GUION} from './guion';

const ORDEN: [React.FC, number][] = [
  [Intro, GUION.intro.dur],
  [Limites, GUION.limites.dur],
  [Contactos, GUION.contactos.dur],
  [Banderas, GUION.banderas.dur],
  [Largada, GUION.largada.dur],
  [Sanciones, GUION.sanciones.dur],
  [Modos, GUION.modos.dur],
  [Pantalla, GUION.pantalla.dur],
  [Cierre, GUION.cierre.dur],
];

export const Video: React.FC = () => {
  useFuentes();
  let desde = 0;
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      {ORDEN.map(([Escena, dur], i) => {
        const inicio = desde;
        desde += dur;
        return (
          <Sequence key={i} from={i === 0 ? 0 : inicio - FUNDIDO} durationInFrames={i === 0 ? dur : dur + FUNDIDO}>
            <Fundido dur={i === 0 ? 1 : FUNDIDO}>
              <Escena />
            </Fundido>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
