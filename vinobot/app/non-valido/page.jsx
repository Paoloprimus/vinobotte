export const metadata = { title: "Link non valido · VinoBotte" };

export default function NonValido() {
  return (
    <div className="pagina pagina-breve">
      <header className="testata">
        <p className="marchio">VinoBotte</p>
        <h1>Questo link non funziona</h1>
      </header>
      <main className="conversazione">
        <p>
          Il link è scaduto oppure non è corretto. Scriva a Paolo Olivato per riceverne uno nuovo.
        </p>
      </main>
    </div>
  );
}
