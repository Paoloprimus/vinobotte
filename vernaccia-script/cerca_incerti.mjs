// Per le cantine di lista.txt senza sito certo: cerca su DuckDuckGo e APRE i primi risultati,
// accetta il sito solo se la pagina contiene il nome della cantina e parla di vino in Toscana.
// Scrive: siti2.txt (verificati) e siti2_dubbi.txt (nessun risultato convincente, con i candidati).
// Uso: node cerca_incerti.mjs     (rilanciabile: salta i già fatti)
import { chromium } from 'playwright';
import fs from 'node:fs';

const leggiNomi = f => fs.existsSync(f) ? fs.readFileSync(f, 'utf8').split('\n').map(l => l.split('|')[0].trim()).filter(Boolean) : [];
const fatti = new Set([...leggiNomi('siti.txt'), ...leggiNomi('siti2.txt'), ...leggiNomi('siti2_dubbi.txt')]);
const righe = fs.readFileSync('lista.txt', 'utf8').split('\n').map(r => r.trim()).filter(r => r && !r.startsWith('#'));
const PORTALI = /(vivino|wine-searcher|facebook|instagram|tripadvisor|trovaprezzi|booking|amazon|youtube|linkedin|wikipedia|pinterest|twitter|tiktok|google|bing|duckduckgo|consorzio|brunello-montalcino|rabissimontalcino|vinomontecucco|vignaiolidiscansano|montepulciano\.org|aziendevinimaremma|candiadeicolliapuani|bolgheridoc|cortonaweb|vernaccia\.it|winearound|vinit\.net|vino\.it|vinoandina|signorvino|callmewine|tannico|xtrawine|enoteca|shop|agriturismo|paginegialle|infobel|cybo|italia-italy|winetourism|winetales|corrieredelvino|gamberorosso|decanter|falstaff|quattrocalici|cellartracker|delectable|bereilvino|vinitipici|onlyitalian|ilgolosario|stradadelvino|toscana\.it)/i;
const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9 ]/g, ' ');
const STOP = new Set(['azienda','agricola','fattoria','tenuta','podere','cantina','cantine','societa','vini','vino','castello','villa','casa','della','delle','dello','dell','degli','dei','del','di','da','il','la','le','lo','the','wine','winery','famiglia','fratelli','selection']);
const sig = n => norm(n).split(/\s+/).filter(t => t.length >= 3 && !STOP.has(t));
const pausa = ms => new Promise(r => setTimeout(r, ms));

const browser = await chromium.launch({ headless: false });
const ctx = await browser.newContext({ locale: 'it-IT' });
const ds = await ctx.newPage();

const conTempo = (p, ms) => Promise.race([p, new Promise(r => setTimeout(() => r(false), ms))]);
async function verificaRaw(url, nome) {
  const p = await ctx.newPage();
  try {
    await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await p.waitForTimeout(1500);
    const t = norm(await p.title() + ' ' + (await p.evaluate(() => document.body.innerText)).slice(0, 30000));
    const tk = sig(nome);
    const trovati = tk.filter(x => t.includes(x)).length;
    const nomeOk = tk.length ? trovati >= Math.max(1, Math.ceil(tk.length * 0.6)) : false;
    const vino = (t.match(/\b(vino|vini|wine|wines|cantina|vigneti|vigneto|vitigni|uve|bottiglie)\b/g) || []).length;
    const tosc = /toscana|tuscany|siena|firenze|grosseto|montalcino|livorno|lucca|pisa|arezzo|massa|carrara|pistoia|prato|chianti/.test(t);
    return nomeOk && vino >= 4 && tosc;
  } catch { return false; } finally { await p.close().catch(() => {}); }
}
const verifica = (url, nome) => conTempo(verificaRaw(url, nome), 40000);

for (const riga of righe) {
  const [nome, zona] = riga.split('|').map(x => x.trim());
  if (fatti.has(nome)) continue;
  let cand = []; const visti = new Set();
  for (const q of [`"${nome}" vino ${zona} Toscana sito ufficiale`, `${nome} cantina ${zona}`]) {
    try {
      await ds.goto('https://html.duckduckgo.com/html/?q=' + encodeURIComponent(q), { waitUntil: 'domcontentloaded', timeout: 45000 });
      let urls = await ds.evaluate(() => [...document.querySelectorAll('a.result__a')].map(a => { try { return new URL(a.href).searchParams.get('uddg') || a.href; } catch { return a.href; } }));
      if (!urls.length) {
        await ds.goto('https://www.bing.com/search?setlang=it&q=' + encodeURIComponent(q), { waitUntil: 'domcontentloaded', timeout: 45000 });
        urls = await ds.evaluate(() => [...document.querySelectorAll('li.b_algo h2 a')].map(a => a.href));
      }
      for (const u of urls) { try { const x = new URL(u); const h = x.host.replace(/^www\./, ''); if (PORTALI.test(h) || visti.has(h)) continue; visti.add(h); cand.push(x.origin + '/'); } catch {} }
    } catch {}
    await pausa(3000);
    if (cand.length >= 4) break;
  }
  cand = cand.slice(0, 5);
  let scelto = '';
  for (const u of cand) { if (await verifica(u, nome)) { scelto = u; break; } }
  if (scelto) { fs.appendFileSync('siti2.txt', `${nome}|${scelto}\n`); console.log('OK   ', nome, scelto); }
  else { fs.appendFileSync('siti2_dubbi.txt', `${nome}|${cand.join(' ')}\n`); console.log('DUBBIO', nome, cand[0] || '-'); }
}
await browser.close();
