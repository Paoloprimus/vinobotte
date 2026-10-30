import crypto from "node:crypto";
import { db } from "./db.js";

export const COOKIE = "vinobotte";

export const hashCodice = (codice) => crypto.createHash("sha256").update(codice).digest("hex");

// Dal codice personale ricava la cantina. Restituisce null se il codice non è valido,
// è scaduto o è stato revocato.
export async function cantinaDaCodice(codice) {
  if (typeof codice !== "string" || codice.length < 20 || codice.length > 100) return null;
  const { data, error } = await db()
    .from("inviti")
    .select("id, cantina_id, scade_il, revocato, cantine(nome)")
    .eq("codice_hash", hashCodice(codice))
    .maybeSingle();
  if (error || !data || data.revocato || new Date(data.scade_il) < new Date()) return null;
  return { invitoId: data.id, cantinaId: data.cantina_id, nome: data.cantine?.nome ?? "" };
}
