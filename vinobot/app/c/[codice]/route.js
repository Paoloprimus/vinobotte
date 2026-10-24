import { NextResponse } from "next/server";
import { db } from "../../../lib/db.js";
import { COOKIE, cantinaDaCodice } from "../../../lib/sessione.js";

export const dynamic = "force-dynamic";

// Link personale: riconosce la cantina, salva il codice in un cookie protetto
// e porta alla conversazione (così il codice sparisce dalla barra degli indirizzi).
export async function GET(req, { params }) {
  const { codice } = await params;
  const s = await cantinaDaCodice(codice);
  if (!s) return NextResponse.redirect(new URL("/non-valido", req.url));

  await db().from("inviti").update({ ultimo_accesso: new Date().toISOString() }).eq("id", s.invitoId);

  const res = NextResponse.redirect(new URL("/chat", req.url));
  res.cookies.set(COOKIE, codice, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 60 * 24 * 90,
  });
  return res;
}
