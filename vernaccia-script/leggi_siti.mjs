// Legge le cantine di siti.txt con Chromium (Playwright): home + pagine contatti/azienda/vini.
// Uso: node leggi_siti.mjs      -> crea la cartella out/ con un .txt per cantina
import { chromium } from 'playwright';
import fs from 'node:fs';

const righe = fs.readFileSync(process.argv[2] || 'siti.txt', 'utf8').split('\n')
  .map(r => r.trim()).filter(r => r && !r.startsWith('#'));
const slug = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const CHIAVE = /(contatt|chi-siamo|azienda|storia|cantina|vini|prodotti|wine|about|contact|dove|privacy|cookie)/i;
fs.mkdirSync('out', { recursive: true });

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ locale: 'it-IT', viewport: { width: 1280, height: 900 } });
const pausa = ms => new Promise(r => setTimeout(r, ms));

async function lavora(riga) {
  await Promise.race([lavoraRaw(riga), new Promise(r => setTimeout(r, 150000))]);
}
async function lavoraRaw(riga) {
  const [nome, url] = riga.split('|').map(x => x.trim());
  if (!url || fs.existsSync(`out/${slug(nome)}.txt`)) return;
  const page = await ctx.newPage();
  const visti = new Set();
  let testo = `# ${nome}\n# ${url}\n`;
  async function leggi(u) {
    if (visti.has(u) || visti.size >= 6) return [];
    visti.add(u);
    try {
      await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await page.waitForTimeout(1200);
      const t = await page.evaluate(() => document.body.innerText);
      const links = await page.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.href));
      testo += `\n\n===== ${u} =====\n${t}`;
      return links;
    } catch (e) { testo += `\n\n===== ${u} ===== ERRORE ${e.message}`; return []; }
  }
  const host = new URL(url).host.replace(/^www\./, '');
  const links = await leggi(url);
  const extra = [...new Set(links)].filter(l => {
    try { const x = new URL(l); return x.host.replace(/^www\./, '') === host && CHIAVE.test(x.pathname + x.search) && !/\.(pdf|jpg|png)$/i.test(x.pathname); } catch { return false; }
  }).slice(0, 5);
  for (const l of extra) { await leggi(l); await pausa(800); }
  fs.writeFileSync(`out/${slug(nome)}.txt`, testo);
  console.log(nome, '->', visti.size, 'pagine,', testo.length, 'caratteri');
  await page.close();
  await pausa(1500);
}

let i = 0;
await Promise.all(Array.from({ length: 12 }, async () => { while (i < righe.length) await lavora(righe[i++]); }));
await browser.close();
