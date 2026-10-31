# VinoBotte / VinoBotte Web — il processo, in ordine di tempo

Ricostruito dall'inventario dei file sul Mac (`elenco-file.txt`: data/ora di ultima modifica, 18.782 voci) più la cronologia del lavoro. Le date sono quelle dei file: indicano **quando sono stati scritti/aggiornati**, non necessariamente quando è iniziata un'attività. Aggiornato al 30 ottobre 2026.

## In sintesi
- Prima data utile del progetto: **16 settembre 2026** (cartella `~/vinobot`). La sola data precedente (11 giugno 2025) è un ambiente Python in `~/vernaccia/.venv`, non fa parte del processo.
- **Ricerche/letture online sui siti delle cantine:** iniziano il **18 ottobre 2026** con la Valpolicella (primo progetto); si estendono all'Italia dal 19–21 ottobre (Vivino, IFW, CMW); la ricerca dei siti ufficiali "a tappeto" parte il **26 ottobre** (vernaccia-script); la lettura completa dei siti il **27 ottobre**; la ricerca a fondo per le cantine senza sito il **28 ottobre**.
- Prima (16 set – 14 ott) il lavoro era sulla **visibilità nelle risposte delle IA** (chat), non sulla raccolta di dati delle cantine.

## Fase 0 — VinoBot, prototipo e app (16–28 settembre)
Cartella `~/vinobot` (Next.js + Supabase). Prime tracce: `src/ai/perplexity.js`, `claude.js`, `supabase/schema.sql`, `lib/db.js` (16/9); `cantine.js`, `lavoro/api` (17–18/9, interrogazioni API delle IA); app, invito, report, classifica, infografiche (19–28/9); `data/report-completo.json` (22/9). Nessuna ricerca sui siti delle cantine.

## Fase 1 — Misura della visibilità nelle chat IA (3–14 ottobre)
- `~/vinobot/lavoro/chat` (3–19/10, ~4.600 file, di cui ~2.900 in `prove/`): prove con ChatGPT e Gemini tramite browser (Playwright), estrazione delle cantine citate, tabelle, varianti, confronto fonti (`tabella-cantine-chat`, `fonti-chat`, `confronto-*`).
- `~/vinobot/prove/chatgpt` (6–7/10) e `~/Downloads/downloadvinobotte` (dal 5/10): report e metodi (`ricerche-api-vino.md`, `ricerche-playwright-vino.md`, "metodi, risultati e decisioni" 6/10, "Riproducibilità della misura di visibilità" 7–8/10, `genera-report.mjs` 9–10/10).
- `lavoro/anagrafica` (5–6/10): prime anagrafiche.
→ Qui nasce l'idea poi ripresa oggi (reperibilità online → visibilità IA); i dati sulle cantine sono quelli *citati dalle IA*, non letti dai siti.

## Fase 2 — Valpolicella: il caso a parte (18–25 ottobre)
Cartella `~/Documents/valpolicella-web` (6.763 file; oltre 3.500 in `cmw/`). È il primo progetto con **ricerche online sistematiche**.
- **18/10** — Elenchi di partenza (`lista1-3.txt`, `beb_it_siti.csv`, `elenco_consorzio.csv`), `crawler_valpolicella.py`, `scheda.py`, `estrai.py`, classificazione aziende/siti (`classifica.py`, `classifica_web.csv`), confronto IA/web.
- **19/10** — Classificazione dei tipi di sito (`classifica_tipi.py`, `tipi_siti_finale.csv`, `tipi_manuali.csv`), `tabella_unica.csv`, `fonti_per_cantina.csv`. Prove Vivino (`vivino_prova.py` → `vivino_cantine.py`, `vivino_dati` ~1.500 file, `vivino_mancanti.py`). Prima prova Vinocom (`~/vinocom`, 23:25).
- **20/10** — `vivino_italia_elenco.py` (Vivino esteso all'Italia); `ifw/` (IFW: `ifw_cantine.py`, `ifw_api.py`, `ifw_tutto.py`); `cmw/cmw_categorie.py`.
- **21–22/10** — `cmw/`: scansione Vivino per regioni, filtri, uve, stili, coda dei mancanti (`vivino_italia_regioni2.py`, `vivino_scansione_filtri.py`, `vivino_scansione_uve.py`, `vivino_scarica_coda.py`, `vivino_nomi_uve.py`). In `~/Downloads/downloadvinobotte`: `cerca_email.py`, `stili_vivino.csv`, `uve_vivino.csv`; tabelle `tabella_cantine_v2.csv`, `rilevazioni_*`.
- **22/10** — `~/Documents/UVCI`: `cantine_v0 / v1`, `vini_v0 / v1`, `cantine_valpolicella_673.csv/xlsx`, legende e anomalie; PDF "Cantine della Valpolicella situazione e integrazione col nuovo approccio". `~/Desktop/vinobotultimo`: tipi cantine, statistica delle coppie, test web on/off (22–23/10), `sintesi_studio_visibilita_IA.pdf`.
- **23/10** — Database e estratti (`valpolicella_web.db`, `archivio_pagine.db`, `entita/attributi/menzioni/collegamenti/siti.csv`, `estratti_23ott_v1–v3.zip`); `riconoscimenti.py` e `riconoscimenti.csv`; `estrai_scheda.py` (testi Begali, Le Salette).
- **24/10** — Controllo `robots.txt` (`controlla_robots.py`, `robots_browser.py`, `robots_esito.csv`, test con diversi user-agent); `annuario/genera-schede.mjs` (generatore delle schede del sito); `testi_lotto1`, `export/`.
- **25/10** — "cantine valpolicella secondo vivino.txt" (ultimo file della cartella).

## Fase 3 — Dal solo Valpolicella a tutta Italia: il sito VinoBotte (24–26 ottobre)
Il generatore delle schede nasce in `valpolicella-web/annuario` (24/10). Poi il lavoro si sposta nel repository del sito (container `annuario/` → `~/Documents/vinobotte`, pubblicazione Vercel). Pipeline `rifusione/rebuild.sh` (fusione fonti, extra, Vernaccia, Vivino, arricchimenti, ragione sociale, giro, schede, build). Nel repo locale: file dal 28/10.

## Fase 4 — Ricerca dei siti ufficiali (26–27 ottobre) — `~/Downloads/vernaccia-script`
- **26/10** — `LEGGIMI.txt`, `cerca_siti.mjs` (ricerca del sito di ogni cantina via motore di ricerca), `estrai.py`.
- **27/10 notte–mattina** — `LEGGIMI2`, liste `siti_bere.txt`, `siti_bere2.txt`; `leggi_siti.mjs`, `cerca_incerti.mjs` (14:13); cartella `out/` (87 file, 14:32–17:39); `siti.txt`, `siti_incerti.txt`, `siti2.txt`, `siti2_dubbi.txt`, `nuovi_estratti.json`.

## Fase 5 — Lettura completa dei siti: il "giro unico" (27 ottobre sera)
`leggi_tutto.mjs` + `estrai2.py` (18:34–18:45): `out2/` con **1.684 siti letti** (18:34 → 23:11), consegnati in 9 blocchi (`bloccoNN.txt` / `bloccoNN_dati.json`, 18:45 → ~23:00): social, negozi online, e-mail, telefono, premi, storia. Applicati alle schede con `giro/prepara1.py` → `applica_giro.py`. Blocchi 1–5 pubblicati e confermati; 6–9 pubblicati ma da confermare.

## Fase 6 — Ricerca a fondo senza sito (28 ottobre)
`cerca_fondo.mjs` (06:05): 134 cantine senza sito, 3 query su DuckDuckGo e Bing, pagine di portali/consorzi, domini ipotizzati → `fondo_risultati.json`. Poi `verifica_fondo.mjs` (controllo nome/comune sulla home) → `fondo_ok.txt`, `fondo_dubbi.txt`. Scelti 76 siti, letti con `leggi_tutto.mjs` + `estrai2.py` → `fondo_blocco_dati.json`. Dopo controllo manuale: **63 cantine applicate** (sito, contatti, social, P.IVA); scartati 5 siti sbagliati, 7 illeggibili, 1 scheda a struttura diversa. **71 cantine restano senza sito.**

## Fase 7 — Registro VinoBotte Web (28 ottobre)
`registro/registro.py` → `vinobotte-web-campi.csv` (2650 × 18 campi: stato + prova) e `vinobotte-web-indice.csv` (indice di reperibilità). Documento "VinoBotte Web" con regola di aggiornamento a 3.500 / 4.000 / 4.500 cantine.

## Fase 8 — Struttura per regione e Toscana (26–30 ottobre)
- **Struttura (26/10):** un produttore = una sola scheda, nella regione della sede; i tipi di vino sono tessere per regione. Doppioni fusi, sezioni miste (Delle Venezie, Prosecco) divise per regione. Il consorzio è la fonte principale dei dati, non la struttura.
- **Toscana (da 27/10):** quattro canali (soci dei consorzi, Vivino, Bere il Vino, siti delle cantine). Consorzio Vino Toscana (IGT) non è tra i consorzi ufficiali della guida: se ne tengono solo i soci DOC/DOCG.
- **Regola delle schede incomplete (29/10):** le cantine con dati incompleti **non entrano nel sito**: stanno in `wip/schede-wip.csv` (tabella "schede wip", 250 righe al 30/10) e si inseriscono quando sono complete. Niente diciture come "scheda essenziale" sul sito.
- **Home (29–30/10):** regioni in ordine decrescente per numero di produttori; titolo "Italia" in maiuscoletto con sotto "Produttori DOC e DOCG" e il totale. Al 30/10: 2650 produttori (Veneto 1137, Toscana 1090, Friuli Venezia Giulia 397, Trentino-Alto Adige 14, Lombardia 7, Piemonte 3, Emilia-Romagna 1, Puglia 1).
- **Giro dei consorzi toscani (30/10), uno alla volta:** Chianti (42 schede segnate, 45 cantine mancanti in wip), Montecucco, Orcia, Cortona, Elba, Carmignano, Candia dei Colli Apuani, Terre di Pisa, Montescudaio, Suvereto e Val di Cornia, Terre di Casole, Monteregio, Colline Lucchesi, Montecarlo, Colli di Luni, Parrina, Pitigliano. Per ciascuno: confronto con la guida; le schede già presenti prendono il gruppo/tile e la riga "Consorzio" (con la fonte dell'elenco); le mancanti vanno in wip. Passi nella pipeline: `applica_consorzio_*.py` e `aggiungi_montecucco.py` (tile aggiunti a mano per fonte verificata).
- **Regola sulle fonti (30/10):** solo elenchi ufficiali o verificabili (siti dei consorzi, pagine delle cantine). Riassunti di AI e elenchi di terzi non sono fonte: servono come traccia da verificare cantina per cantina (es. Monteregio: tile solo dove il sito della cantina cita la denominazione). Elenco stampa 2021 di Suvereto sostituito dall'elenco ufficiale del sito.
- **Strumenti sul Mac (Playwright):** `cerca_siti.mjs`, `consorzio_esplora.mjs` (esplora un sito e salva testi/link), `monteregio_cerca.mjs`, `monteregio_cantine.mjs`, script Montecucco/Orcia.
- **Errori corretti:** Uccelliera di Pisa confusa con l'Uccelliera di Montalcino; commit con zip sbagliato (cartella `vinobot/` finita nel repo, modifiche del sito non pubblicate fino al commit 922f9007).
- **Aperti:** Morellino (elenco ufficiale non leggibile), Vernaccia, avanzi di Orcia/Montecucco/Cortona, Colli di Luni toscani (Massa-Carrara), Pitigliano (consorzio senza elenco), lettura dei siti delle cantine in wip per completare le schede, 19 cantine Montecucco senza sito, Consorzio Garda DOC.

## Cosa NON risulta dai file (e va ricostruito dalla cronologia delle conversazioni)
- Per le ricerche del 26–27/10 non c'è un log per singola ricerca: lo stato "cercato e non trovato" è dedotto da quali elenchi la cantina compare.
- Marketplace, Google Business Profile, Wine-Searcher, Wikipedia: mai cercati per nessuna cantina.
- Cartelle non incluse nell'inventario non sono visibili (es. Chianti, Prosecco, Montalcino se elaborati altrove: nell'inventario compaiono solo le schede finali).
- Le date dei file sono di ultima modifica: file riscritti più volte mostrano l'ultima data.

## Fase 9 — Lista temporanea: siti e promozione (30 ott 2026)
- Cercati i siti di 114 cantine senza sito (cerca_siti.mjs), letti 85 siti (leggi_tutto.mjs + estrai2.py), testi completi riletti per sede, P.IVA, denominazioni.
- Soglia di ingresso scelta: sede + sito ufficiale + DOC/DOCG confermata (dal sito o dall'elenco ufficiale del consorzio di denominazione).
- Promosse 33 cantine (28 toscane, 5 liguri): `arricchimenti/wip_promossi.json` + `rifusione/aggiungi_wip.py` (nel rebuild dopo aggiungi_montecucco). Nuova regione Liguria (gruppo Colli di Luni).
- Siti trovati sbagliati e corretti nella lista: La Tommasina e Via del Ferro (Piemonte), Morandi (Arezzo), Carlini (Rimini), Terre della Luna (Franciacorta), scambio Fattoria La Torre / Fattoria Tori.
- Restano in `wip/schede-wip.csv` le cantine senza DOC/DOCG indicata sul sito o senza sede, con il motivo nella colonna Stato.
- Val di Cornia: altre 7 cantine promosse con sede e contatti dalla scheda del consorzio (suveretowine.com): Bulichella, Montepeloso, Macchion dei Lupi, Rigoli, Sasso Orlando, Monte Solaio, Sant'Agnese. Totale promosse dalla lista: 40.
- Secondo blocco di lettura siti (68): promosse altre 30 cantine (21 Chianti con elenco del Consorzio Vino Chianti, 2 Carmignano, 2 Montecucco, 2 Morellino, 1 Cortona, 1 Elba, e Arrighi all’Elba); totale promosse dalla lista: 70. Restano 179 in `wip/schede-wip.csv`.
- Terzo passo: lettura del secondo blocco (68 siti) e promosse altre 38 cantine (Montecucco 17, Orcia 6, Cortona 4, Montescudaio 4, Candia 2, Carmignano 1, Chianti 1, Elba 1, Terre di Casole 1, Monteregio 1); totale promosse dalla lista: 108. Restavano 141 in `wip/schede-wip.csv`.
- Quarto passo (31 ottobre): riletti i 22 siti non leggibili più Varramista: 14 domini inesistenti, altri con certificato non valido o timeout, Varramista senza DOC/DOCG. Nessuna promossa; per decisione di Paolo le 23 sono state tolte da `wip/schede-wip.csv`, che ora ha 118 righe.
- Quinto passo (31 ottobre): riesame dei testi già letti per le cantine «sito letto, DOC non indicata»: 5 promosse (Tenute di Badia, Fattoria Valdrighi, Il Monticello, Cantina del Nonno Pescetto, La Pietra del Focolare), DOC confermata dalle pagine del sito. Lista provvisoria: 113 righe; sito: 2.763 produttori.
- Sesto passo (31 ottobre): per Tenuta di Valgiano, Cantine Lunae e Giacomelli la DOC è confermata da schede di vendita online (fonte 2 nella scheda), su indicazione di Paolo. Lista provvisoria: 110 righe; sito: 2.766 produttori.
- Settimo passo (31 ottobre): 12 cantine del Consorzio Vino Chianti promosse con sede, telefono, email e denominazioni dalla scheda del consorzio (fonte) e sito ufficiale. Lista provvisoria: 98 righe; sito: 2.778 produttori.
