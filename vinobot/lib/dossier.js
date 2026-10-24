import { db } from "./db.js";

const NOMI_AI = { chatgpt: "ChatGPT", claude: "Claude", gemini: "Gemini", perplexity: "Perplexity" };
const MAX_TESTO = 3000;

const nomeBase = (s) => s.replace(/\s*\(.*\)\s*$/, "").trim();
const data = (d) => new Date(d).toLocaleDateString("it-IT");

function dominio(fonte) {
  try {
    const host = new URL(fonte.url).hostname.replace(/^www\./, "");
    // Gemini passa le fonti da un indirizzo di Google: il sito vero è nel titolo
    if (host.includes("vertexaisearch") && fonte.titolo) return fonte.titolo.replace(/^www\./, "");
    return host;
  } catch {
    return fonte.titolo || null;
  }
}

// Prepara il dossier di UNA cantina: solo i suoi dati e quelli delle sue domande.
export async function creaDossier(cantinaId) {
  const sb = db();
  const { data: scheda, error: e1 } = await sb
    .from("schede").select("fatti, domande_ids, concorrenti, cantine(nome)")
    .eq("cantina_id", cantinaId).single();
  if (e1) throw e1;

  const ids = scheda.domande_ids ?? [];
  const nomeCantina = scheda.cantine?.nome ?? "";
  const concorrenti = (scheda.concorrenti ?? []).map((c) => ({ etichetta: c, nome: nomeBase(c) }));

  const { data: domande, error: e2 } = await sb
    .from("domande").select("id, testo, gruppo").in("id", ids).order("id");
  if (e2) throw e2;

  const { data: risposte, error: e3 } = await sb
    .from("risposte").select("id, domanda_id, ai, ripetizione, testo, fonti, created_at")
    .in("domanda_id", ids).is("errore", null).order("id");
  if (e3) throw e3;

  const idsRisposte = risposte.map((r) => r.id);
  const { data: menzioni, error: e4 } = idsRisposte.length
    ? await sb.from("menzioni")
        .select("risposta_id, cantina_id, posizione, raccomandata, cantine(nome)")
        .in("risposta_id", idsRisposte)
    : { data: [], error: null };
  if (e4) throw e4;

  const righe = [];
  righe.push(`CANTINA: ${nomeCantina}`);
  righe.push("");
  righe.push("FATTI VERIFICATI SULLA CANTINA:");
  righe.push(scheda.fatti.trim());
  righe.push("");
  righe.push(`CONCORRENTI CHE PUOI NOMINARE (e nessun altro): ${concorrenti.map((c) => c.etichetta).join(", ") || "nessuno"}`);
  righe.push("");
  righe.push("MISURAZIONE:");
  righe.push("Ogni domanda è stata posta più volte a ChatGPT, Claude e Gemini, con la ricerca web attiva e dal contesto italiano.");

  for (const d of domande) {
    const rs = risposte.filter((r) => r.domanda_id === d.id);
    if (!rs.length) continue;
    const date = rs.map((r) => r.created_at).sort();
    const ms = menzioni.filter((m) => rs.some((r) => r.id === m.risposta_id));
    const suaCantina = ms.filter((m) => m.cantina_id === cantinaId);
    const rispCantina = new Set(suaCantina.map((m) => m.risposta_id));

    righe.push("");
    righe.push(`DOMANDA: "${d.testo}"`);
    righe.push(`Tipo: ${d.gruppo === "marchio" ? "domanda che contiene il nome della cantina" : "domanda generica, senza il nome della cantina"}`);
    righe.push(`Risposte raccolte: ${rs.length}, tra il ${data(date[0])} e il ${data(date[date.length - 1])}`);

    const perAi = Object.keys(NOMI_AI)
      .map((ai) => {
        const tot = rs.filter((r) => r.ai === ai);
        if (!tot.length) return null;
        const si = tot.filter((r) => rispCantina.has(r.id)).length;
        return `${NOMI_AI[ai]} ${si}/${tot.length}`;
      })
      .filter(Boolean);
    righe.push(`${nomeCantina} nominata in ${rispCantina.size}/${rs.length} risposte (${perAi.join(", ")})`);
    if (suaCantina.length) {
      const pos = suaCantina.reduce((s, m) => s + m.posizione, 0) / suaCantina.length;
      const racc = suaCantina.filter((m) => m.raccomandata).length;
      righe.push(`Posizione media tra le cantine nominate: ${pos.toFixed(1)}; consigliata esplicitamente in ${racc} risposte`);
    }

    if (d.gruppo !== "marchio") {
      for (const c of concorrenti) {
        const rsC = new Set(ms.filter((m) => m.cantine?.nome === c.nome).map((m) => m.risposta_id));
        const aiC = new Set(rs.filter((r) => rsC.has(r.id)).map((r) => NOMI_AI[r.ai]));
        righe.push(`${c.etichetta} nominata in ${rsC.size}/${rs.length} risposte${aiC.size ? ` (${[...aiC].join(", ")})` : ""}`);
      }
      const altre = new Set(ms.map((m) => m.cantina_id).filter((id) => id !== cantinaId));
      righe.push(`Numero totale di cantine diverse nominate in queste risposte: ${altre.size}`);
    }

    const conteggio = new Map();
    for (const r of rs) {
      for (const f of r.fonti ?? []) {
        const dm = dominio(f);
        if (dm) conteggio.set(dm, (conteggio.get(dm) ?? 0) + 1);
      }
    }
    const top = [...conteggio.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);
    if (top.length) righe.push(`Fonti più usate dalle AI: ${top.map(([dm, n]) => `${dm} (${n})`).join(", ")}`);

    if (d.gruppo === "marchio") {
      for (const r of rs.filter((x) => x.ripetizione === 1)) {
        const t = (r.testo ?? "").slice(0, MAX_TESTO);
        righe.push("");
        righe.push(`Testo della risposta di ${NOMI_AI[r.ai] ?? r.ai}:`);
        righe.push(t + ((r.testo ?? "").length > MAX_TESTO ? " [...]" : ""));
      }
    }
  }

  return { nome: nomeCantina, testo: righe.join("\n") };
}
