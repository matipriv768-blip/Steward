// Guion del video: textos y duraciones. Para cambiar lo que dice el video, se edita este archivo.
// Las duraciones van en cuadros: el video corre a 30 cuadros por segundo (30 = 1 segundo).

export const FPS = 30;
export const ANCHO = 1920;
export const ALTO = 1080;
export const FUNDIDO = 15; // cuadros que dura el fundido entre una escena y la siguiente

export const GUION = {
  intro: {
    dur: 165,
    antetitulo: 'Comisario de carrera para Assetto Corsa',
    titulo: 'Steward',
    lema: 'Carreras limpias, decididas en la pista.',
  },
  limites: {
    dur: 210,
    antetitulo: '01 · Límites de pista',
    titulo: 'Solo cuenta el atajo con ventaja',
    texto: 'Si sales con las cuatro ruedas y ganas tiempo, es un aviso. Si sueltas el acelerador y pierdes tiempo, no cuenta. Al tercer aviso llega la sanción.',
  },
  contactos: {
    dur: 240,
    antetitulo: '02 · Contactos',
    titulo: 'Con culpa, como en una carrera de verdad',
    texto: 'Roce, contacto o choque fuerte según la diferencia de velocidad. Quien alcanza por detrás es responsable y tiene 20 segundos para devolver el puesto.',
  },
  banderas: {
    dur: 225,
    antetitulo: '03 · Banderas',
    titulo: 'Cada bandera, a tiempo',
    texto: 'Amarilla con un auto detenido a menos de 300 m, azul cuando te van a doblar, blanca en la última vuelta. La dirección de carrera puede declarar amarilla total o roja.',
  },
  largada: {
    dur: 240,
    antetitulo: '04 · Largadas',
    titulo: 'Parada o lanzada, en dos filas',
    texto: 'En la vuelta de formación ves tu velocidad contra el máximo y la distancia al de adelante. La verde sale cuando el líder está a 100 m de la meta.',
  },
  sanciones: {
    dur: 240,
    antetitulo: '05 · Sanciones',
    titulo: 'Sanciones que se cumplen en pista',
    texto: 'Tiempo, levantar el pie, drive-through, stop and go o descalificación, con plazo en vueltas para cumplirlas.',
  },
  modos: {
    dur: 210,
    linea1: 'Offline contra la IA.',
    detalle1: 'La IA también recibe sanciones y las cumple en pista o en pits.',
    linea2: 'Online con los tuyos.',
    detalle2: 'Sin servidor central ni nada que pagar. Un script gratis ordena la largada.',
  },
  pantalla: {
    dur: 180,
    antetitulo: '06 · Tu pantalla',
    titulo: 'Claro, oscuro o sin fondo',
    texto: 'Una barra con tu sesión y tarjetas que aparecen solo cuando pasa algo.',
  },
  cierre: {
    dur: 180,
    titulo: 'Steward',
    texto: 'Gratis y de código abierto',
    link: 'matipriv768-blip.github.io/Steward',
  },
};

export const DURACION_TOTAL = Object.values(GUION).reduce((suma, escena) => suma + escena.dur, 0);
