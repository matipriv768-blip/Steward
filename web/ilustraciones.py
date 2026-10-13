"""Ilustraciones SVG de la web de Steward: el circuito al atardecer (portada) y el trazado en linea (tarjeta azul).
Se generan con un poco de azar fijo (semilla) para que las siluetas de los arboles se vean hechas a mano."""
import math
import random

random.seed(11)


def ridge(y0, amp, step, w=1600, base=900, jitter=0.5):
    """Linea de cerros u arboles: puntos con ruido suave."""
    pts = []
    x = -20
    ph = random.random() * 6
    while x <= w + 40:
        y = y0 + math.sin(x / 210 + ph) * amp + math.sin(x / 77 + ph * 2) * amp * 0.35 + random.uniform(-1, 1) * amp * jitter * 0.3
        pts.append((x, y))
        x += step
    d = 'M%.1f,%d ' % (pts[0][0], base) + ' '.join('L%.1f,%.1f' % p for p in pts) + ' L%.1f,%d Z' % (pts[-1][0], base)
    return d


def treeline(y0, h, w=1600, base=900):
    """Copas de arboles: arcos chicos de altura variable."""
    x = -20
    d = 'M-20,%d L-20,%.1f ' % (base, y0)
    while x < w + 40:
        r = random.uniform(9, 22)
        top = y0 - random.uniform(0.3, 1.0) * h
        d += 'Q%.1f,%.1f %.1f,%.1f ' % (x + r, top - r * 0.6, x + 2 * r, y0 - random.uniform(0, h * 0.25))
        x += 2 * r
    d += 'L%.1f,%d Z' % (x, base)
    return d


def hero():
    stars = ''.join('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#fefffc" opacity="%.2f"/>' % (
        random.uniform(0, 1600), random.uniform(0, 260), random.uniform(0.6, 1.6), random.uniform(0.25, 0.8)) for _ in range(70))
    lights = ''
    for x in (300, 520, 1340):
        lights += f'''
    <g opacity="0.95">
      <line x1="{x}" y1="612" x2="{x}" y2="430" stroke="#1a1b2e" stroke-width="5"/>
      <rect x="{x - 26}" y="418" width="52" height="16" rx="3" fill="#1a1b2e"/>
      <circle cx="{x}" cy="426" r="70" fill="url(#lamp)"/>
      <g fill="#fff6dd">{''.join('<circle cx="%d" cy="426" r="3"/>' % (x - 18 + i * 9) for i in range(5))}</g>
    </g>'''
    windows = ''.join('<rect x="%d" y="%d" width="5" height="3" fill="#ffd79a" opacity="%.2f"/>' % (
        180 + i * 13, 571 + (i % 3) * 9, random.uniform(0.35, 0.9)) for i in range(26))
    return f'''<svg class="hero-art" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Circuito al atardecer, con un puesto de comisarios y una bandera amarilla">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#151a33"/><stop offset="0.32" stop-color="#2f3a68"/>
      <stop offset="0.55" stop-color="#8a6f8f"/><stop offset="0.7" stop-color="#d99a86"/><stop offset="0.8" stop-color="#f3c99c"/>
    </linearGradient>
    <radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#fff1d6"/><stop offset="0.35" stop-color="#ffd9a8" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#f3b48a" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="lamp" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#fff3cf" stop-opacity="0.85"/><stop offset="1" stop-color="#ffd38f" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="asphalt" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3a3b55"/><stop offset="1" stop-color="#1e1f30"/>
    </linearGradient>
    <linearGradient id="grass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2c4a3d"/><stop offset="1" stop-color="#132219"/>
    </linearGradient>
    <linearGradient id="haze" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f3c99c" stop-opacity="0"/><stop offset="1" stop-color="#f3c99c" stop-opacity="0.35"/>
    </linearGradient>
    <filter id="soft" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
    <filter id="brush" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.04" numOctaves="3" seed="4" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="14"/>
    </filter>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="9"/>
      <feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.4  0 0 0 0.07 0"/>
    </filter>
  </defs>
  <rect width="1600" height="900" fill="url(#sky)"/>
  {stars}
  <circle cx="1130" cy="560" r="190" fill="url(#sun)"/>
  <circle cx="1130" cy="560" r="46" fill="#fff0d2" opacity="0.9"/>
  <g filter="url(#soft)" opacity="0.55">
    <ellipse cx="420" cy="330" rx="260" ry="26" fill="#e7a8a0"/>
    <ellipse cx="1240" cy="300" rx="320" ry="22" fill="#d99aa2"/>
    <ellipse cx="900" cy="420" rx="380" ry="18" fill="#f2c0a0"/>
  </g>
  <g filter="url(#brush)">
    <path d="{ridge(520, 34, 22)}" fill="#6a6590" opacity="0.75"/>
    <path d="{ridge(560, 26, 18)}" fill="#4c4b74"/>
    <rect y="520" width="1600" height="120" fill="url(#haze)"/>
    <path d="{treeline(600, 46)}" fill="#2a2b46"/>
  </g>
  <!-- tribuna -->
  <g>
    <path d="M150,612 L150,566 L520,548 L520,612 Z" fill="#202137"/>
    <path d="M140,566 L530,544 L530,538 L140,560 Z" fill="#33344f"/>
    {windows}
  </g>
  {lights}
  <!-- pasto y pista -->
  <path d="M0,640 C300,600 700,612 1600,598 L1600,900 L0,900 Z" fill="url(#grass)"/>
  <path d="M-40,900 C260,760 520,700 860,676 C1120,658 1380,660 1660,640 L1660,712 C1380,734 1150,738 900,760 C620,786 420,840 300,920 Z" fill="url(#asphalt)"/>
  <path d="M-40,900 C260,760 520,700 860,676 C1120,658 1380,660 1660,640" fill="none" stroke="#fefffc" stroke-width="6" stroke-dasharray="26 26" opacity="0.92"/>
  <path d="M-40,900 C260,760 520,700 860,676 C1120,658 1380,660 1660,640" fill="none" stroke="#d64532" stroke-width="6" stroke-dasharray="26 26" stroke-dashoffset="26" opacity="0.92"/>
  <path d="M300,920 C420,840 620,786 900,760 C1150,738 1380,734 1660,712" fill="none" stroke="#fefffc" stroke-width="3" opacity="0.55"/>
  <!-- barrera -->
  <path d="M0,628 C300,592 700,604 1600,588" fill="none" stroke="#9aa0b8" stroke-width="3" opacity="0.5"/>
  <!-- puesto de comisarios con bandera amarilla -->
  <g transform="translate(1180 700)">
    <rect x="-40" y="-70" width="80" height="70" fill="#1c1d30"/>
    <path d="M-52,-70 L0,-104 L52,-70 Z" fill="#26273e"/>
    <rect x="-24" y="-54" width="48" height="22" fill="#ffd79a" opacity="0.85"/>
    <line x1="64" y1="12" x2="64" y2="-128" stroke="#e9ece7" stroke-width="4" stroke-linecap="round"/>
    <path d="M66,-126 C92,-136 112,-118 140,-126 L140,-80 C112,-72 92,-90 66,-80 Z" fill="#f2c230"/>
  </g>
  <rect width="1600" height="900" filter="url(#grain)"/>
</svg>'''


def circuit():
    # trazado inventado, en linea blanca: recta, horquilla, eses y una curva rapida
    d = ('M180,420 L620,420 C700,420 720,380 700,340 C680,300 600,300 560,270 C520,240 540,180 600,170 '
         'L840,150 C900,145 930,190 900,230 C870,270 900,310 960,310 L1040,310 C1100,310 1120,370 1080,410 '
         'C1050,440 1000,440 960,450 L300,500 C220,505 160,470 180,420 Z')
    marks = ''.join('<rect x="%d" y="%d" width="10" height="10" fill="#fefffc"/>' % (380 + (i % 2) * 10, 410 + (i // 2) * 10 - 0)
                    for i in range(4) if (i % 2 + i // 2) % 2 == 0)
    return f'''<svg class="circuit-art" viewBox="0 0 1200 600" role="img" aria-label="Trazado de un circuito dibujado en línea">
  <path d="{d}" fill="none" stroke="#fefffc" stroke-opacity="0.18" stroke-width="34" stroke-linejoin="round"/>
  <path d="{d}" fill="none" stroke="#fefffc" stroke-width="3.5" stroke-linejoin="round"/>
  <line x1="390" y1="404" x2="390" y2="436" stroke="#fefffc" stroke-width="3"/>
  {marks}
  <g fill="#fefffc" font-family="Inter, sans-serif" font-size="15" letter-spacing="0.08em">
    <circle cx="700" cy="340" r="6"/><text x="716" y="345">T1</text>
    <circle cx="600" cy="170" r="6"/><text x="560" y="152">T4</text>
    <circle cx="900" cy="230" r="6"/><text x="916" y="236">T7</text>
    <circle cx="1080" cy="410" r="6"/><text x="1096" y="416">T9</text>
  </g>
</svg>'''


def network():
    return '''<svg class="net-art" viewBox="0 0 560 360" role="img" aria-label="Cada piloto tiene la app y el script del servidor coordina la largada">
  <g fill="none" stroke="#282834" stroke-width="1.5">
    <path d="M140,110 L280,250" stroke-dasharray="5 6"/><path d="M420,110 L280,250" stroke-dasharray="5 6"/>
    <path d="M170,90 L390,90"/>
  </g>
  <g font-family="Inter, sans-serif" font-size="14" fill="#2c2c2c" text-anchor="middle">
    <rect x="60" y="60" width="160" height="60" rx="8" fill="#ffffff" stroke="#dee2de"/>
    <text x="140" y="86" font-weight="600" data-i18n="net_you">Tu app</text>
    <text x="140" y="106" fill="#646464" font-size="12" data-i18n="net_you_sub">vigila tu auto</text>
    <rect x="340" y="60" width="160" height="60" rx="8" fill="#ffffff" stroke="#dee2de"/>
    <text x="420" y="86" font-weight="600" data-i18n="net_friend">App de tu amigo</text>
    <text x="420" y="106" fill="#646464" font-size="12" data-i18n="net_friend_sub">vigila el suyo</text>
    <rect x="190" y="240" width="180" height="64" rx="8" fill="#ffffff" stroke="#41a1cf"/>
    <text x="280" y="267" font-weight="600" data-i18n="net_server">Script del servidor</text>
    <text x="280" y="287" fill="#646464" font-size="12" data-i18n="net_server_sub">fila, verde y reglamento</text>
    <text x="280" y="80" fill="#646464" font-size="12" data-i18n="net_link">se avisan entre sí</text>
  </g>
</svg>'''
