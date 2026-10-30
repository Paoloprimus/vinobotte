// Cerca il sito di ogni cantina di lista.txt con DuckDuckGo (in Chromium) e scrive:
//   siti.txt         -> nome|url      (sito molto probabile: il dominio contiene il nome)
//   siti_incerti.txt -> nome|url|altri (da controllare a mano)
// Uso: node cerca_siti.mjs      (si può interrompere e rilanciare: salta quelli già fatti)
import { chromium } from 'playwright';
import fs from 'node:fs';

const righe = fs.readFileSync('lista.txt', 'utf8').split('\n').map(r => r.trim()).filter(r => r && !r.startsWith('#'));
const fatti = new Set();
for (const f of ['siti.txt', 'siti_incerti.txt', 'siti_nonrovati.txt'])
  if (fs.existsSync(f)) fs.readFileSync(f, 'utf8').split('\n').forEach(l => { const n = l.split('|')[0].trim(); if (n) fatti.add(n); });
const PORTALI = /(vivino|wine-searcher|facebook|instagram|tripadvisor|trovaprezzi|informazione-aziende|italianwinerydirectory|italiantastemap|booking|amazon|youtube|linkedin|paginebianche|firmania|ufficiocamerale|registroaziende|reteimprese|infobel|misterimprese|cellartracker|delectable|wikipedia|gamberorosso|vinoandina|quattrocalici|cantinedelvino|vinievino|hellotaste|enosearcher|callmewine|winesurf|decanto|decanter|falstaff|cybo|coobiz|empresite|italy724|icribis|agriturismo\.it|agriturismi|tuscanywineries|vinorandum|bbr\.com|klwines|tanners|totalwine|drinks|wineonline|tannico|bernabei|vino75|xtrawine|enoteca|wineshop|shop\.|bereilvino|beverfood|stradadelvino|toscana\.it|visittuscany|pinterest|twitter|tiktok|google|bing|duckduckgo)/i;
const sl = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
const STOP = new Set(['azienda','agricola','fattoria','tenuta','podere','cantina','cantine','societa','vini','vino','castello','villa','casa','della','delle','dello','dell','degli','dei','del','di','da','il','la','le','lo','the','wine','winery','famiglia','fratelli']);
const tokens = n => sl(n).replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter(t => t.length >= 4 && !STOP.has(t));

const browser = await chromium.launch({ headless: false });
const ctx = await browser.newContext({ locale: 'it-IT' });
const page = await ctx.newPage();
const pausa = ms => new Promise(r => setTimeout(r, ms));
for (const riga of righe) {
  const [nome, zona] = riga.split('|').map(x => x.trim());
  if (fatti.has(nome)) continue;
  const q = `${nome} ${zona} vino azienda agricola`;
  try {
    await page.goto('https://html.duckduckgo.com/html/?q=' + encodeURIComponent(q), { waitUntil: 'domcontentloaded', timeout: 45000 });
    const urls = await page.evaluate(() => [...document.querySelectorAll('a.result__a')].map(a => { try { return new URL(a.href).searchParams.get('uddg') || a.href; } catch { return a.href; } }));
    const cand = []; const visti = new Set();
    for (const u of urls) { try { const x = new URL(u); const h = x.host.replace(/^www\./, ''); if (PORTALI.test(h) || visti.has(h)) continue; visti.add(h); cand.push(x.origin + '/'); } catch {} }
    const tk = tokens(nome);
    const buono = cand.find(u => { const h = sl(new URL(u).host).replace(/[^a-z0-9]/g, ''); return tk.some(t => h.includes(t)); });
    if (buono) { fs.appendFileSync('siti.txt', `${nome}|${buono}\n`); console.log('OK   ', nome, buono); }
    else if (cand.length) { fs.appendFileSync('siti_incerti.txt', `${nome}|${cand[0]}|${cand.slice(1, 3).join(' ')}\n`); console.log('INCERTO', nome, cand[0]); }
    else { fs.appendFileSync('siti_nonrovati.txt', `${nome}|\n`); console.log('NO   ', nome); }
  } catch (e) { console.log('ERRORE', nome, e.message); }
  await pausa(3500);
}
await browser.close();
