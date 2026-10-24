"use client";

import { useEffect, useRef, useState } from "react";

const SUGGERIMENTI = [
  "Perché le intelligenze artificiali non ci nominano?",
  "Da dove prendono le informazioni su di noi?",
  "Cosa possiamo fare subito?",
];

export default function Chat({ nome }) {
  const [messaggi, setMessaggi] = useState([]);
  const [testo, setTesto] = useState("");
  const [stato, setStato] = useState("carico"); // carico | pronto | scrivo
  const [errore, setErrore] = useState("");
  const fondo = useRef(null);
  const campo = useRef(null);

  useEffect(() => {
    fetch("/api/chat")
      .then(async (r) => {
        const d = await r.json();
        if (!r.ok) throw new Error(d.errore || "Errore");
        setMessaggi(d.messaggi);
      })
      .catch((e) => setErrore(e.message))
      .finally(() => setStato("pronto"));
  }, []);

  useEffect(() => {
    fondo.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messaggi, stato]);

  async function invia(contenuto) {
    const t = contenuto.trim();
    if (!t || stato !== "pronto") return;
    setErrore("");
    setTesto("");
    setMessaggi((m) => [...m, { id: `tmp-${Date.now()}`, ruolo: "user", testo: t }]);
    setStato("scrivo");
    try {
      const r = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ testo: t }),
      });
      const d = await r.json();
      if (!r.ok) throw new Error(d.errore || "Errore");
      setMessaggi((m) => [...m, d.messaggio]);
    } catch (e) {
      setErrore(e.message);
    } finally {
      setStato("pronto");
      campo.current?.focus();
    }
  }

  function tasto(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      invia(testo);
    }
  }

  const soloBenvenuto = messaggi.length === 1 && messaggi[0].ruolo === "assistant";

  return (
    <div className="pagina">
      <header className="testata">
        <p className="marchio">VinoBotte</p>
        <h1>{nome}</h1>
        <p className="sottotitolo">Come la vedono le intelligenze artificiali, e cosa si può fare.</p>
      </header>

      <main className="conversazione" aria-live="polite">
        {stato === "carico" && <p className="attesa">VinoBotte sta preparando i suoi dati…</p>}

        {messaggi.map((m) => (
          <div key={m.id} className={m.ruolo === "assistant" ? "msg bot" : "msg utente"}>
            {m.testo}
          </div>
        ))}

        {stato === "scrivo" && <p className="attesa">VinoBotte sta scrivendo…</p>}

        {soloBenvenuto && stato === "pronto" && (
          <div className="suggerimenti">
            {SUGGERIMENTI.map((s) => (
              <button key={s} type="button" onClick={() => invia(s)}>
                {s}
              </button>
            ))}
          </div>
        )}

        {errore && <p className="errore" role="alert">{errore}</p>}
        <div ref={fondo} />
      </main>

      <form
        className="scrivi"
        onSubmit={(e) => {
          e.preventDefault();
          invia(testo);
        }}
      >
        <label htmlFor="domanda" className="nascosto">Scriva la sua domanda</label>
        <textarea
          id="domanda"
          ref={campo}
          rows={2}
          maxLength={2000}
          placeholder="Scriva qui la sua domanda"
          value={testo}
          onChange={(e) => setTesto(e.target.value)}
          onKeyDown={tasto}
          disabled={stato !== "pronto"}
        />
        <button type="submit" disabled={stato !== "pronto" || !testo.trim()}>
          Invia
        </button>
      </form>
    </div>
  );
}
