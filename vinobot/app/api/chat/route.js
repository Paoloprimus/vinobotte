import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { db } from "../../../lib/db.js";
import { COOKIE, cantinaDaCodice } from "../../../lib/sessione.js";
import { creaDossier } from "../../../lib/dossier.js";
import { rispondi, aggiornaRiassunto, ISTRUZIONE_BENVENUTO } from "../../../lib/bot.js";

export const dynamic = "force-dynamic";
export const maxDuration = 60;

const MAX_CARATTERI = 2000;
const MAX_MESSAGGI_AL_GIORNO = 60;
const SOGLIA_RIASSUNTO = 40; // messaggi non riassunti che fanno partire il riassunto
const DA_RIASSUMERE = 20; // quanti dei più vecchi vengono riassunti

async function sessione() {
  const codice = (await cookies()).get(COOKIE)?.value;
  return cantinaDaCodice(codice);
}

const errore = (msg, status) => NextResponse.json({ errore: msg }, { status });

async function leggiContesto(cantinaId) {
  const sb = db();
  const { data: rias } = await sb
    .from("riassunti").select("testo, fino_a_messaggio_id").eq("cantina_id", cantinaId).maybeSingle();
  const da = rias?.fino_a_messaggio_id ?? 0;
  const { data: storia, error } = await sb
    .from("messaggi").select("id, ruolo, testo")
    .eq("cantina_id", cantinaId).gt("id", da).order("id").limit(SOGLIA_RIASSUNTO + 10);
  if (error) throw error;
  return { riassunto: rias?.testo ?? null, storia };
}

async function salva(cantinaId, ruolo, testo) {
  const { data, error } = await db()
    .from("messaggi").insert({ cantina_id: cantinaId, ruolo, testo })
    .select("id, ruolo, testo, created_at").single();
  if (error) throw error;
  return data;
}

async function magariRiassumi(cantinaId) {
  const sb = db();
  const { riassunto, storia } = await leggiContesto(cantinaId);
  if (storia.length < SOGLIA_RIASSUNTO) return;
  const vecchi = storia.slice(0, DA_RIASSUMERE);
  const testo = await aggiornaRiassunto({ vecchio: riassunto, messaggi: vecchi });
  const { error } = await sb.from("riassunti").upsert({
    cantina_id: cantinaId,
    testo,
    fino_a_messaggio_id: vecchi[vecchi.length - 1].id,
    aggiornato_il: new Date().toISOString(),
  });
  if (error) throw error;
}

// Storico da mostrare a schermo; alla prima apertura prepara il messaggio di benvenuto.
export async function GET() {
  const s = await sessione();
  if (!s) return errore("Accesso non valido", 401);
  try {
    const { data, error } = await db()
      .from("messaggi").select("id, ruolo, testo, created_at")
      .eq("cantina_id", s.cantinaId).order("id", { ascending: false }).limit(100);
    if (error) throw error;
    let messaggi = data.reverse();

    if (!messaggi.length) {
      const dossier = await creaDossier(s.cantinaId);
      const testo = await rispondi({
        nome: dossier.nome,
        dossier: dossier.testo,
        riassunto: null,
        storia: [{ ruolo: "user", testo: ISTRUZIONE_BENVENUTO }],
      });
      messaggi = [await salva(s.cantinaId, "assistant", testo)];
    }
    return NextResponse.json({ messaggi });
  } catch (e) {
    console.error(e);
    return errore("VinoBotte non riesce a caricare la conversazione. Riprovi tra qualche minuto.", 500);
  }
}

export async function POST(req) {
  const s = await sessione();
  if (!s) return errore("Accesso non valido", 401);

  let testo;
  try {
    testo = String((await req.json())?.testo ?? "").trim();
  } catch {
    return errore("Messaggio non leggibile", 400);
  }
  if (!testo) return errore("Scriva un messaggio", 400);
  if (testo.length > MAX_CARATTERI) return errore(`Il messaggio supera i ${MAX_CARATTERI} caratteri`, 400);

  try {
    const sb = db();
    const inizioGiorno = new Date();
    inizioGiorno.setHours(0, 0, 0, 0);
    const { count } = await sb
      .from("messaggi").select("id", { count: "exact", head: true })
      .eq("cantina_id", s.cantinaId).eq("ruolo", "user").gte("created_at", inizioGiorno.toISOString());
    if ((count ?? 0) >= MAX_MESSAGGI_AL_GIORNO) {
      return errore("Per oggi è stato raggiunto il numero massimo di messaggi. Può riprendere domani.", 429);
    }

    await salva(s.cantinaId, "user", testo);
    const [dossier, contesto] = await Promise.all([creaDossier(s.cantinaId), leggiContesto(s.cantinaId)]);
    const risposta = await rispondi({
      nome: dossier.nome,
      dossier: dossier.testo,
      riassunto: contesto.riassunto,
      storia: contesto.storia,
    });
    const salvato = await salva(s.cantinaId, "assistant", risposta);

    try {
      await magariRiassumi(s.cantinaId);
    } catch (e) {
      console.error("Riassunto non aggiornato:", e);
    }
    return NextResponse.json({ messaggio: salvato });
  } catch (e) {
    console.error(e);
    return errore("VinoBotte non è riuscito a rispondere. Riprovi tra qualche minuto.", 500);
  }
}
