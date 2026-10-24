import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { COOKIE, cantinaDaCodice } from "../../lib/sessione.js";
import Chat from "./Chat.jsx";

export const dynamic = "force-dynamic";

export const metadata = { title: "VinoBotte" };

export default async function PaginaChat() {
  const codice = (await cookies()).get(COOKIE)?.value;
  const s = await cantinaDaCodice(codice);
  if (!s) redirect("/non-valido");
  return <Chat nome={s.nome} />;
}
