"""Arma docs/index.html de Steward (GitHub Pages). Uso: python3 construir_web.py carpeta_docs"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from ilustraciones import hero, circuit, network
from textos import T, GLYPHS, REPO, GIST

OUT = sys.argv[1] if len(sys.argv) > 1 else 'docs'


def t(key, tag='span', cls=None, attrs=''):
    c = ' class="%s"' % cls if cls else ''
    return '<%s%s data-i18n="%s"%s>%s</%s>' % (tag, c, key, attrs, html.escape(T[key][0]), tag)


FEATURES = ''.join('''
      <article class="card feature">
        <span class="feature-n">0%d</span>
        %s
        %s
      </article>''' % (n, t('f%d_t' % n, 'h3'), t('f%d_p' % n, 'p')) for n in range(1, 7))

GLYPH_GRID = ''.join('''
        <figure class="glyph"><img src="assets/senales/%s.png" alt="" width="160" height="110" loading="lazy">%s</figure>''' % (
    f, t(k, 'figcaption')) for f, k in GLYPHS)

STEPS = ''.join('''
      <li class="card step"><span class="step-n">%d</span>%s%s</li>''' % (n, t('i%d_t' % n, 'h3'), t('i%d_p' % n, 'p')) for n in range(1, 5))

FAQ = ''.join('''
      <details class="faq">%s%s</details>''' % (t('q%d' % n, 'summary'), t('a%d' % n, 'p')) for n in range(1, 6))

PRESET = """[SCRIPT_...]
SCRIPT = '%s'
rollingStart = 1
formationSpeed = 100
greenMeters = 100
startMeters = 500
adminPass = 'tu-clave'
requireApp = 1""" % GIST

KEYS = ''.join('<li><code>%s</code>%s</li>' % (k, t(v)) for k, v in (
    ('rollingStart', 'k_rolling'), ('formationSpeed', 'k_speed'), ('greenMeters', 'k_green'),
    ('startMeters', 'k_start'), ('adminPass', 'k_admin'), ('requireApp', 'k_require')))

TABS_STYLE = ''.join('<button type="button" class="seg" data-style="%s" aria-pressed="%s">%s</button>' % (
    s, 'true' if s == 'claro' else 'false', t(k)) for s, k in (('claro', 'st_light'), ('oscuro', 'st_dark'), ('sinfondo', 'st_none')))
TABS_SCENE = ''.join('<button type="button" class="chip" data-scene="%s" aria-pressed="%s">%s</button>' % (
    s, 'true' if s == 'amarilla' else 'false', t(k)) for s, k in (
    ('amarilla', 'sc_yellow'), ('sancion', 'sc_pen'), ('largada', 'sc_start'), ('devolver', 'sc_back')))

I18N = json.dumps({k: {'es': v[0], 'en': v[1]} for k, v in T.items()}, ensure_ascii=False)

CSS = r"""
:root{
  --parchment:#fefffc;--paper:#ffffff;--linen:#f9faf7;--ink:#171717;--graphite:#2c2c2c;--charcoal:#444141;--ash:#646464;
  --fog:#b4b8b4;--mist:#dee2de;--twilight:#282834;--dusk:#1f1f29;--signal:#41a1cf;--signal-text:#1f78ad;--cerulean:#0081c0;
  --serif:'Fraunces',Georgia,'Times New Roman',serif;--sans:'Inter',ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  --shadow-card:rgba(0,0,0,.08) 0 1px 1px 0,rgba(0,0,0,.08) 0 4px 5px 0;--shadow-diagram:rgba(0,0,0,.05) 0 1px 8px 0;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--parchment);color:var(--charcoal);font-family:var(--sans);font-size:16px;line-height:1.5;letter-spacing:-.01em}
img{max-width:100%;display:block}
a{color:inherit}
h1,h2,h3{color:var(--graphite);margin:0;font-weight:400}
h1,h2{font-family:var(--serif);font-feature-settings:"liga" 0;letter-spacing:-.02em;line-height:1.1}
h1{font-size:clamp(36px,5.2vw,54px)}
h2{font-size:clamp(30px,4vw,48px)}
h3{font-family:var(--sans);font-size:18px;font-weight:600;line-height:1.3;letter-spacing:-.012em}
p{margin:0}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em}
.wrap{max-width:1200px;margin:0 auto;padding:0 24px}
.eyebrow{font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--ash);margin-bottom:16px;display:block}
.lead{font-size:18px;line-height:1.5;color:var(--ash);max-width:640px}

/* navegacion: pildora esmerilada */
.nav{position:fixed;top:16px;left:50%;transform:translateX(-50%);z-index:20;display:flex;align-items:center;gap:6px;
  padding:6px 6px 6px 14px;border-radius:50px;border:1px solid rgba(255,255,255,.55);background:rgba(254,255,252,.62);
  -webkit-backdrop-filter:blur(14px) saturate(1.2);backdrop-filter:blur(14px) saturate(1.2);box-shadow:rgba(0,0,0,.15) 0 2px 6px 0;
  max-width:calc(100% - 32px)}
.brand{display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--twilight);font-family:var(--serif);font-size:20px;letter-spacing:-.02em;margin-right:6px}
.brand svg{width:22px;height:22px}
.nav a.link{text-decoration:none;color:var(--twilight);font-size:15px;font-weight:500;padding:7px 10px;border-radius:8px;white-space:nowrap}
.nav a.link:hover{background:rgba(40,40,52,.06)}
.lang{display:flex;border:1px solid var(--mist);border-radius:8px;overflow:hidden;margin:0 4px}
.lang button{all:unset;cursor:pointer;font-size:13px;font-weight:600;padding:6px 8px;color:var(--ash)}
.lang button[aria-pressed="true"]{background:var(--twilight);color:#fff}
.btn{display:inline-flex;align-items:center;gap:10px;text-decoration:none;font-size:15px;font-weight:500;line-height:1;
  padding:9px 12px 9px 14px;border-radius:8px;border:1px solid var(--twilight);color:var(--twilight);background:transparent;white-space:nowrap;cursor:pointer}
.btn .arrow{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;border:1px solid currentColor;font-size:12px}
.btn.primary{border-color:var(--signal);color:var(--signal-text)}
.btn.primary:hover{background:rgba(65,161,207,.08)}
.btn.dark{background:var(--dusk);border-color:var(--twilight);color:#fff;padding:10px 16px}
.btn:focus-visible,.lang button:focus-visible,.seg:focus-visible,.chip:focus-visible{outline:2px solid var(--signal);outline-offset:2px}

/* portada */
.hero{position:relative;height:100vh;min-height:640px;overflow:hidden;background:#151a33}
.hero-art{position:absolute;inset:0;width:100%;height:100%}
.hero-card{position:absolute;left:clamp(16px,4vw,56px);bottom:clamp(16px,6vh,64px);max-width:600px;padding:32px;border-radius:24px;
  background:rgba(254,255,252,.78);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.6)}
.hero-card h1{margin:4px 0 16px}
.hero-card p.sub{color:var(--charcoal);font-size:17px}
.hero-actions{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0 14px}
.hero-note{font-size:13px;color:var(--ash);line-height:1.3}

section{padding:96px 0}
.intro{display:grid;grid-template-columns:repeat(12,1fr);gap:24px}
.intro h2{grid-column:1 / span 7}
.intro .lead{grid-column:8 / span 5;align-self:end}
.features{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:56px}
.card{background:var(--paper);border:1px solid var(--mist);border-radius:12px;box-shadow:var(--shadow-card)}
.feature{padding:20px 20px 24px}
.feature-n{display:block;font-family:var(--serif);font-size:27px;letter-spacing:-.04em;color:var(--fog);line-height:1.2;margin-bottom:12px}
.feature h3{margin-bottom:8px}
.feature p{color:var(--ash);font-size:15px}

/* pantalla */
.screen-head{display:grid;grid-template-columns:repeat(12,1fr);gap:24px;align-items:end}
.screen-head > div:first-child{grid-column:1 / span 6}
.screen-head .lead{grid-column:7 / span 6}
.viewer{margin-top:40px;padding:12px;border-radius:16px;background:rgba(255,255,255,.7);box-shadow:var(--shadow-diagram);border:1px solid var(--mist)}
.viewer-bar{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;padding:4px 4px 12px}
.segs{display:inline-flex;border:1px solid var(--mist);border-radius:8px;overflow:hidden}
.seg{all:unset;cursor:pointer;font-size:15px;font-weight:500;padding:8px 14px;color:var(--charcoal)}
.seg[aria-pressed="true"]{background:var(--dusk);color:#fff}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{all:unset;cursor:pointer;font-size:15px;font-weight:500;padding:7px 12px;border-radius:8px;border:1px solid var(--mist);color:var(--charcoal)}
.chip[aria-pressed="true"]{border-color:var(--signal);color:var(--signal-text)}
.viewer img{width:100%;height:auto;border-radius:8px;aspect-ratio:1200/460;object-fit:cover;background:#2a2b33}
.caption{font-size:13px;color:var(--ash);margin-top:10px;padding:0 4px}

/* senales */
.glyphs{display:grid;grid-template-columns:repeat(8,1fr);gap:8px;margin-top:40px}
.glyph{margin:0;padding:12px 8px 14px;border-radius:12px;border:1px solid var(--mist);background:var(--paper);text-align:center}
.glyph img{width:100%;height:auto;max-width:120px;margin:0 auto 6px}
.glyph figcaption{font-size:13px;line-height:1.3;color:var(--charcoal)}

/* tarjeta azul */
.blue{position:relative;overflow:hidden;border-radius:24px;background:var(--cerulean);color:#fff;padding:clamp(32px,7vw,96px);
  box-shadow:rgba(0,0,0,.06) 0 2px 2px 0,rgba(0,0,0,.04) 0 0 0 5px}
.blue h2{color:#fff;max-width:620px;position:relative}
.blue p{max-width:560px;margin-top:20px;font-size:17px;color:#eef7fb;position:relative}
.circuit-art{position:absolute;right:-60px;bottom:-30px;width:min(760px,80%);opacity:.9;pointer-events:none}
.net{display:grid;grid-template-columns:repeat(12,1fr);gap:24px;align-items:center;margin-top:80px}
.net > div:first-child{grid-column:1 / span 5}
.net h3{font-family:var(--serif);font-size:27px;font-weight:400;letter-spacing:-.04em;line-height:1.3;margin-bottom:12px}
.net p{color:var(--ash)}
.diagram{grid-column:7 / span 6;padding:12px;border-radius:16px;background:rgba(255,255,255,.75);box-shadow:var(--shadow-diagram);border:1px solid var(--mist)}
.net-art{width:100%;height:auto}

/* instalar */
.steps{list-style:none;padding:0;margin:40px 0 0;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.step{padding:20px}
.step-n{display:inline-grid;place-items:center;width:32px;height:32px;border-radius:50%;border:1px solid var(--twilight);font-family:var(--serif);font-size:17px;color:var(--twilight);margin-bottom:16px}
.step h3{margin-bottom:8px}
.step p{font-size:15px;color:var(--ash)}
.note{margin-top:16px;padding:14px 16px;background:var(--linen);border-bottom:1px solid var(--charcoal);font-size:15px;color:var(--charcoal)}

/* servidor */
.server{display:grid;grid-template-columns:repeat(12,1fr);gap:24px}
.server > div:first-child{grid-column:1 / span 5}
.server .code{grid-column:6 / span 7}
.code{position:relative;align-self:start;background:var(--dusk);color:#e9ece7;border-radius:12px;padding:20px 20px 18px;overflow:auto}
.code pre{padding-top:30px}
.code pre{margin:0;font-size:13.5px;line-height:1.6;white-space:pre}
.code .copy{position:absolute;top:12px;right:12px;border-color:rgba(255,255,255,.35);color:#fff;padding:6px 10px;font-size:13px}
.keys{list-style:none;padding:0;margin:24px 0 0;display:grid;gap:10px}
.keys li{display:grid;grid-template-columns:140px 1fr;gap:12px;font-size:15px;color:var(--ash)}
.keys code{color:var(--twilight)}
.more{display:inline-block;margin-top:20px;color:var(--charcoal);font-size:16px}

/* preguntas */
.faqs{margin-top:40px;border-top:1px solid var(--mist)}
.faq{border-bottom:1px solid var(--mist);padding:18px 4px}
.faq summary{cursor:pointer;list-style:none;font-size:18px;font-weight:500;color:var(--graphite);display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-family:var(--serif);font-size:24px;line-height:1;color:var(--ash)}
.faq[open] summary::after{content:"–"}
.faq p{margin-top:10px;color:var(--ash);max-width:760px}

footer{background:var(--paper);border-top:1px solid var(--mist);padding:80px 0 48px}
footer h2{max-width:760px}
.foot-links{display:flex;flex-wrap:wrap;gap:20px;margin:32px 0 40px}
.foot-links a{text-decoration:none;font-size:15px;font-weight:500;color:var(--twilight)}
.foot-links a:hover{text-decoration:underline}
.credit{font-size:13px;color:var(--ash);max-width:820px;line-height:1.5}

@media (max-width:980px){
  .nav a.link{display:none}
  .intro h2,.intro .lead,.screen-head > div:first-child,.screen-head .lead,.net > div:first-child,.diagram,.server > div:first-child,.server .code{grid-column:1 / -1}
  .features{grid-template-columns:repeat(2,1fr)}
  .steps{grid-template-columns:repeat(2,1fr)}
  .glyphs{grid-template-columns:repeat(4,1fr)}
}
@media (max-width:620px){
  section{padding:64px 0}
  .wrap{padding:0 16px}
  .nav{padding-left:12px}
  .nav .btn{display:none}
  .hero{min-height:700px}
  .hero-card{left:16px;right:16px;padding:24px;bottom:16px}
  .features,.steps{grid-template-columns:1fr}
  .glyphs{grid-template-columns:repeat(2,1fr)}
  .keys li{grid-template-columns:1fr;gap:2px}
  .viewer-bar{flex-direction:column}
  .viewer img{aspect-ratio:4/3;object-position:50% 0}
  .circuit-art{position:relative;right:auto;bottom:auto;width:100%;margin:24px 0 -8px}
}
"""

JS = r"""
(function(){
  var I = %s;
  var lang = 'es';
  try { lang = localStorage.getItem('steward-lang') || ((navigator.language || 'es').slice(0,2) === 'es' ? 'es' : 'en'); } catch (e) {
    lang = (navigator.language || 'es').slice(0,2) === 'es' ? 'es' : 'en';
  }
  var style = 'claro', scene = 'amarilla';
  var shot = document.getElementById('shot');
  function paintShot(){ shot.src = 'assets/hud/hud-' + scene + '-' + style + '-' + lang + '.jpg'; }
  function apply(){
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i18n]').forEach(function(el){
      var k = el.getAttribute('data-i18n'); if (I[k]) el.textContent = I[k][lang];
    });
    document.title = I.title[lang];
    var m = document.querySelector('meta[name=description]'); if (m) m.setAttribute('content', I.meta[lang]);
    document.querySelectorAll('.lang button').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.lang === lang ? 'true' : 'false'); });
    paintShot();
  }
  document.querySelectorAll('.lang button').forEach(function(b){
    b.addEventListener('click', function(){ lang = b.dataset.lang; try { localStorage.setItem('steward-lang', lang); } catch (e) {} apply(); });
  });
  document.querySelectorAll('.seg').forEach(function(b){
    b.addEventListener('click', function(){
      style = b.dataset.style;
      document.querySelectorAll('.seg').forEach(function(x){ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      paintShot();
    });
  });
  document.querySelectorAll('.chip').forEach(function(b){
    b.addEventListener('click', function(){
      scene = b.dataset.scene;
      document.querySelectorAll('.chip').forEach(function(x){ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      paintShot();
    });
  });
  var copy = document.querySelector('.copy');
  copy.addEventListener('click', function(){
    var text = document.getElementById('preset').textContent;
    function done(){ copy.textContent = I.server_copied[lang]; setTimeout(function(){ copy.textContent = I.server_copy[lang]; }, 1600); }
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function(){}); 
  });
  apply();
})();
""" % I18N

MARK = '''<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="29" fill="none" stroke="currentColor" stroke-width="3"/>
<line x1="22" y1="15" x2="22" y2="50" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"/>
<rect x="23.5" y="18" width="21" height="15" fill="none" stroke="currentColor" stroke-width="2.5"/>
<path d="M23.5 18h5.25v5h-5.25zM34 18h5.25v5H34zM28.75 23h5.25v5h-5.25zM39.25 23h5.25v5h-5.25zM23.5 28h5.25v5h-5.25zM34 28h5.25v5H34z" fill="currentColor"/></svg>'''

PAGE = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(T['title'][0])}</title>
<meta name="description" content="{html.escape(T['meta'][0])}">
<meta property="og:title" content="Steward">
<meta property="og:description" content="{html.escape(T['meta'][0])}">
<meta property="og:image" content="assets/og.png">
<meta name="theme-color" content="#151a33">
<link rel="icon" href="assets/icono.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<nav class="nav" aria-label="Principal">
  <a class="brand" href="#top">{MARK}Steward</a>
  <a class="link" href="#que-hace">{t('nav_what')}</a>
  <a class="link" href="#pantalla">{t('nav_screen')}</a>
  <a class="link" href="#instalar">{t('nav_install')}</a>
  <a class="link" href="#servidor">{t('nav_server')}</a>
  <a class="link" href="#preguntas">{t('nav_faq')}</a>
  <div class="lang" role="group" aria-label="Idioma / Language"><button type="button" data-lang="es" aria-pressed="true">ES</button><button type="button" data-lang="en" aria-pressed="false">EN</button></div>
  <a class="btn primary" href="{REPO}/releases/latest">{t('nav_cta')}<span class="arrow">→</span></a>
</nav>

<header class="hero" id="top">
  {hero()}
  <div class="hero-card">
    {t('hero_eyebrow', 'span', 'eyebrow')}
    {t('hero_h1', 'h1')}
    {t('hero_p', 'p', 'sub')}
    <div class="hero-actions">
      <a class="btn primary" href="{REPO}/releases/latest">{t('hero_cta')}<span class="arrow">→</span></a>
      <a class="btn" href="{REPO}">{t('hero_code')}</a>
    </div>
    {t('hero_note', 'p', 'hero-note')}
  </div>
</header>

<main>
<section id="que-hace">
  <div class="wrap">
    <div class="intro">{t('intro_h2', 'h2')}{t('intro_p', 'p', 'lead')}</div>
    <div class="features">{FEATURES}
    </div>
  </div>
</section>

<section id="pantalla" style="background:var(--paper);border-top:1px solid var(--mist);border-bottom:1px solid var(--mist)">
  <div class="wrap">
    <div class="screen-head"><div>{t('screen_eyebrow', 'span', 'eyebrow')}{t('screen_h2', 'h2')}</div>{t('screen_p', 'p', 'lead')}</div>
    <div class="viewer">
      <div class="viewer-bar"><div class="segs" role="group">{TABS_STYLE}</div><div class="chips" role="group">{TABS_SCENE}</div></div>
      <img id="shot" src="assets/hud/hud-amarilla-claro-es.jpg" alt="" width="1200" height="460">
      {t('screen_note', 'p', 'caption')}
    </div>
  </div>
</section>

<section id="senales">
  <div class="wrap">
    {t('flags_eyebrow', 'span', 'eyebrow')}{t('flags_h2', 'h2')}
    <div class="glyphs">{GLYPH_GRID}
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="blue">{circuit()}{t('blue_h2', 'h2')}{t('blue_p', 'p')}</div>
    <div class="net">
      <div>{t('net_h3', 'h3')}{t('net_p', 'p')}</div>
      <div class="diagram">{network()}</div>
    </div>
  </div>
</section>

<section id="instalar" style="background:var(--paper);border-top:1px solid var(--mist);border-bottom:1px solid var(--mist)">
  <div class="wrap">
    {t('install_eyebrow', 'span', 'eyebrow')}{t('install_h2', 'h2')}
    <ol class="steps">{STEPS}
    </ol>
    {t('install_note', 'p', 'note')}
  </div>
</section>

<section id="servidor">
  <div class="wrap server">
    <div>
      {t('server_eyebrow', 'span', 'eyebrow')}{t('server_h2', 'h2')}
      <p class="lead" style="margin-top:20px" data-i18n="server_p">{html.escape(T['server_p'][0])}</p>
      <ul class="keys">{KEYS}</ul>
      <a class="more" href="{REPO}#caso-3-crear-tu-propio-servidor-con-steward" data-i18n="server_more">{html.escape(T['server_more'][0])}</a>
    </div>
    <div class="code"><button type="button" class="btn copy" data-i18n="server_copy">{T['server_copy'][0]}</button><pre id="preset">{html.escape(PRESET)}</pre></div>
  </div>
</section>

<section id="preguntas" style="padding-top:0">
  <div class="wrap">
    {t('faq_eyebrow', 'span', 'eyebrow')}{t('faq_h2', 'h2')}
    <div class="faqs">{FAQ}
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    {t('foot_h2', 'h2')}
    <div class="foot-links">
      <a href="{REPO}">GitHub</a>
      <a href="{REPO}/releases">{t('foot_releases')}</a>
      <a href="{REPO}/blob/main/CHANGELOG.md">{t('foot_changes')}</a>
      <a href="{REPO}/blob/main/LICENSE">{t('foot_license')}</a>
    </div>
    {t('foot_credit', 'p', 'credit')}
  </div>
</footer>
<script>{JS}</script>
</body>
</html>
'''

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(PAGE)
print('ok', len(PAGE))
