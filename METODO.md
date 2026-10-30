# Metodo VinoBotte (per riprendere dopo interruzioni)
Aggiornato al 30 ottobre 2026. La cronologia è in `registro/PROCESSO.md`.

## Come si costruisce il sito
- Tutto si rigenera con `bash rifusione/rebuild.sh` (container: `/home/claude/annuario`). Ordine: fusione delle fonti (`fondi.py`) → copia di `dati/`, `chiarire/`, `produttori.json` → aggiunte (extra, tile, Vernaccia, Vivino, Montecucco) → arricchimenti (ragione sociale, giro dei siti, fondo, P.IVA, Wikipedia, Google, Vivino, piattaforme, vini, raggiungibilità) → `applica_consorzio_*.py` (riga "Consorzio" sulle schede) → rifiniture (presenza, anagrafica, testi) → `node genera-schede.mjs` (le pagine delle schede) → `rifusione/costruisci2.py` (pagine per regione, per tipo di vino, home).
- Modifiche ai dati: mai a mano su `dati/` o `produttori.json` (vengono rigenerati). Si scrive un file in `arricchimenti/` (JSON) e il relativo `rifusione/applica_*.py`, oppure si aggiunge il tile in `rifusione/aggiungi_montecucco.py`, e si rilancia `rebuild.sh`.
- Scheda: `dati/<slug>.json` = {nome, slug, sezioni[righe etichetta/valore], fonti[n, testo, url, etichetta]}; ogni dato ha il numero di fonte; "Consorzio" è una riga di Anagrafica.
- `produttori.json`: slug, nome, regione, comune, tipi (gruppo → denominazioni), membri, primario. Titoli dei gruppi in `rifusione/tit.json`.

## Regole di Paolo
- **Struttura:** un produttore = una scheda, nella regione della sede (se due regioni: sede legale, casi dubbi da decidere insieme). I tipi di vino sono tessere per regione. La guida copre tutti i produttori DOC/DOCG d'Italia, non solo i soci dei consorzi: il consorzio è la fonte, non la struttura.
- **Solo produttori e solo DOC/DOCG:** niente distributori, commerciali, imbottigliatori; niente IGT/IGP, vini senza denominazione, distillati.
- **Schede incomplete fuori dal sito:** stanno in `wip/schede-wip.csv` (tabella "schede wip", separatore `;`, utf-8-sig) e si inseriscono quando sono complete. Mai diciture tipo "scheda essenziale".
- **Fonti:** solo elenchi ufficiali o verificabili. Riassunti di AI e elenchi di terzi non sono fonte: servono da traccia da verificare cantina per cantina. Un tile (es. Monteregio) si aggiunge a una cantina già in guida solo se il suo sito cita la denominazione.
- **Redazione:** sezione "Presenza online"; una presenza per riga; "Negozio online"/"Marketplace" e "Premi"/"Punteggi" righe separate; ragione sociale e P.IVA su righe separate, solo se il dato c'è; niente testi che ripetono la fonte; niente "non verificato"; le righe di assenza dopo una ricerca fatta restano.
- **Metodo di lavoro:** una cosa per messaggio; italiano sintetico; ogni modifica finisce con il "solito comando" git (`unzip -o`, add, commit, push, status, grep di verifica); i blocchi di controllo non nascondono le righe `inflating`.

## Consorzi: come si procede (uno alla volta)
1. Trovare la lista dei soci sul sito del consorzio (WebFetch; se il sito è bloccato ai robot, script Mac `consorzio_esplora.mjs <URL> <cartella>` e lo zip viene allegato).
2. Confrontare con `produttori.json` (per nome e comune: attenzione agli omonimi, es. Uccelliera di Pisa ≠ Uccelliera di Montalcino).
3. Cantine già in guida: riga "Consorzio" con fonte (`arricchimenti/consorzio_<nome>.json` + `applica_consorzio_<nome>.py` + riga in `rebuild.sh`) ed eventuale tile.
4. Cantine mancanti: righe in `wip/schede-wip.csv` (sito, sede, contatti, fonte, stato).
5. Rigenerare con `rebuild.sh`, creare lo zip e consegnare zip + `schede-wip.csv` + blocco git.

## Strumenti sul Mac (`~/Downloads/vernaccia-script`)
`cerca_siti.mjs` (trova il sito di una cantina), `consorzio_esplora.mjs` (legge un sito di consorzio), `leggi_tutto.mjs` + `estrai2.py` (legge i siti delle cantine), script specifici per Montecucco, Orcia, Monteregio. I siti bloccati ai bot si leggono solo con questi script (non con il Chrome).

## Stato
Vedi `registro/PROCESSO.md` (Fase 8 e "Aperti"). I file della prima fase Valpolicella (`digest.py`, `leggi.py`, `scheda.py`, `spec/`, `stato.txt`) sono ormai storici.
