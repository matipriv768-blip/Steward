import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import {ALTO, ANCHO, DURACION_TOTAL, FPS} from './guion';

export const Root: React.FC = () => (
  <Composition id="Steward" component={Video} durationInFrames={DURACION_TOTAL} fps={FPS} width={ANCHO} height={ALTO} />
);
