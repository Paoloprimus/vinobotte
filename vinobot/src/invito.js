// VINOBOT — crea un link personale per una cantina
// Uso: npm run invito -- --cantina "Valentina Cubi" [--giorni 60]
import "dotenv/config";
import crypto from "node:crypto";
import { createClient } from "@supabase/supabase-js";

const a = process.argv.slice(2);
const val = (k) => { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : undefined; };
const nome = val("--cantina");
const giorni = Number(val("--giorni") ?? 60);
if (!nome) {
  console.error('Manca il nome: npm run invito -- --cantina "Nome cantina"');
  process.exit(1);
}

const db = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SECRET_KEY, {
  auth: { persistSession: false },
});

const { data: cantina, error } = await db.from("cantine").select("id, nome").eq("nome", nome).maybeSingle();
if (error) throw error;
if (!cantina) {
  console.error(`Cantina non trovata: ${nome}`);
  process.exit(1);
}
const { data: scheda } = await db.from("schede").select("cantina_id").eq("cantina_id", cantina.id).maybeSingle();
if (!scheda) {
  console.error(`La cantina ${nome} non ha ancora una scheda: il bot non avrebbe dati.`);
  process.exit(1);
}

const codice = crypto.randomBytes(24).toString("base64url");
const hash = crypto.createHash("sha256").update(codice).digest("hex");
const scade = new Date(Date.now() + giorni * 24 * 60 * 60 * 1000);

const { error: e2 } = await db.from("inviti").insert({
  cantina_id: cantina.id,
  codice_hash: hash,
  scade_il: scade.toISOString(),
});
if (e2) throw e2;

const base = (process.env.VINOBOTTE_URL || "http://localhost:3000").replace(/\/$/, "");
console.log(`Link per ${cantina.nome} (scade il ${scade.toLocaleDateString("it-IT")}):`);
console.log(`${base}/c/${codice}`);
console.log("Il link si vede solo adesso: copialo subito.");
