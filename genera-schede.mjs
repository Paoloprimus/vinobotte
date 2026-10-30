// genera-schede.mjs
// Legge i file in dati/*.json (uno per cantina) e scrive una pagina HTML per cantina in pagine/.
// Lo stile è quello delle schede approvate (Le Salette, Begali): si cambia solo qui, in STILE.
// Uso:  node genera-schede.mjs

import { readdirSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const QUI = dirname(fileURLToPath(import.meta.url));
const DATI = join(QUI, 'dati');
const PAGINE = join(QUI, 'pagine');

const STILE = `:root{--bg:#faf8f4;--ink:#1d1b19;--line:#d9d3c8;--acc:#7a1f2b}
@media (prefers-color-scheme:dark){:root{--bg:#171513;--ink:#f1ece4;--line:#3a352f;--acc:#e08a96}}
*{box-sizing:border-box}
body{margin:0}
.pg{background:var(--bg);color:var(--ink);font:16px/1.45 Georgia,'Times New Roman',serif;min-height:100%}
.pg main{max-width:720px;margin:0 auto;padding:20px 16px 48px}
.pg a{color:var(--acc)}
.pg h1{font-size:clamp(28px,7vw,34px);line-height:1.15;font-weight:700;margin:0 0 6px}
.pg h2{font-size:16px;line-height:1.3;font-weight:700;color:var(--acc);margin:0 0 4px}
.pg p{margin:0 0 2px}
section{border-top:1px solid var(--line);padding:12px 0 8px;margin-top:10px}
.row{display:grid;grid-template-columns:160px 1fr;gap:0 16px;padding:2px 0}
.val{overflow-wrap:anywhere}
.vig{margin:2px 0 0;padding-left:18px}
.vig li{margin:0}
.fn{margin-left:2px;text-decoration:none;font-size:10px;line-height:0;vertical-align:super}
.lab{color:var(--acc)}
.fonti,.fonti h2,.fonti li,.fonti p,.foot p{font-size:12px}
.fonti .fn,.fonti a.fn{font-size:inherit;vertical-align:baseline}
.vini{margin-left:176px}
.vino{display:grid;grid-template-columns:3fr 2fr 2.5em;gap:0 16px;padding:2px 0}
.foot{border-top:1px solid var(--line);margin-top:10px;padding-top:12px}
.foot p{font-style:italic}
.fonti ol{margin:0;padding-left:24px}
.fonti li{margin:0 0 2px}
@media (max-width:560px){
 .row{grid-template-columns:1fr}
 .row .lab{font-weight:400}
 .vini{margin-left:0}
 .vino{grid-template-columns:1fr 6.5em}
 .vino .vd{grid-column:1 / -1;order:3}
 .vino .va{text-align:right}
}`;

const PIEDE = `Scheda compilata da VinoBot esclusivamente da fonti pubbliche, indicate in calce con la data di consultazione. Ricerca, verifica e pubblicazione dei dati sono svolte con strumenti di IA sotto controllo umano in ogni fase. La cantina non è stata interpellata prima della pubblicazione: se un dato risulta sbagliato o incompleto, può proporne la correzione in ogni momento scrivendo a <a href="mailto:info@vinobotte.it">info@vinobotte.it</a>. <a href="#nota-metodologica">Nota metodologica</a> · <a href="#informativa-privacy">Informativa privacy</a>`;

// Caratteri speciali -> HTML
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Testo con segni speciali -> HTML:
//   [[7]]            numero di fonte
//   {{indirizzo|testo}}  collegamento
//   a capo           riga nuova
const testo = (s) =>
  esc(s)
    .replace(/\[\[(\d+)\]\]/g, '<a class="fn" href="#f$1" aria-label="Fonte $1">[$1]</a>')
    .replace(/\{\{([^|}]+)\|([^}]+)\}\}/g, '<a href="$1" target="_blank" rel="noopener">$2</a>')
    .replace(/\n/g, '<br>');

const riga = (r) =>
  `<div class="row"><div class="lab">${esc(r.etichetta)}</div><div class="val">${testo(r.valore)}` +
  (r.elenco ? `<ul class="vig">${r.elenco.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : '') +
  `</div></div>`;

const vino = (v) =>
  `<div class="vino"><div class="vn">${esc(v.nome)}</div><div class="vd">${esc(v.denominazione)}</div><div class="va">${testo(v.annata).replace(/^—\s*/, "")}</div></div>`;

function sezione(s) {
  let h = `<section><h2>${esc(s.titolo)}</h2>\n`;
  if (s.nota) h += `<p class="nota">${testo(s.nota)}</p>\n`;
  if (s.tipo === 'vini') h += `<div class="vini">${s.vini.map(vino).join('\n')}\n</div>\n`;
  else h += s.righe.map(riga).join('\n') + '\n';
  return h + '</section>';
}

function fonti(c) {
  const voci = c.fonti
    .map((f) => `<li id="f${f.n}">${esc(f.testo)}${f.url ? ` <a href="${esc(f.url)}" target="_blank" rel="noopener">${esc(f.etichetta)}</a>` : ''}</li>`)
    .join('\n');
  return `<section class="fonti"><h2>Fonti e note</h2>\n<p>${testo(c.consultate)}</p>\n<ol>\n${voci}\n</ol></section>`;
}

function pagina(c) {
  return `<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Scheda cantina — ${esc(c.nome)}</title>
<style>
${STILE}
</style>
</head>
<body>
<div class="pg"><main>
<h1 style="text-align:center;font-size:clamp(30px,8vw,40px)">${esc(c.nome)}</h1>
${c.sezioni.map(sezione).join('\n')}
${fonti(c)}
</main></div>
<script src="/shell.js" defer></script>
</body>
</html>
`;
}

mkdirSync(PAGINE, { recursive: true });
const file = readdirSync(DATI).filter((f) => f.endsWith('.json')).sort();
for (const f of file) {
  const c = JSON.parse(readFileSync(join(DATI, f), 'utf8'));
  const slug = c.slug || f.replace(/\.json$/, '');
  writeFileSync(join(PAGINE, `${slug}.html`), pagina(c));
  console.log(`ok  ${slug}.html`);
}
console.log(`${file.length} pagine generate in ${PAGINE}`);
