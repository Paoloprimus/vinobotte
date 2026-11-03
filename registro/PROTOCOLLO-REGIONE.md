# Protocollo per chiudere una regione

Ricavato dal Piemonte (3 novembre 2026). Principio: mostrare l'esistenza online dei produttori DOP legittimi, senza doppioni. Il consorzio, Vivino e il web sono strumenti, non l'obiettivo.

## Regole fisse
1. **Una scheda = un produttore che imbottiglia vino DOP a nome proprio.** Fuori i conferitori di uve (soci "viticoli"), i ristoranti, gli agriturismi senza vino proprio, i rivenditori.
2. **Fonti sulla scheda:** solo ciò che è stato letto: sito ufficiale e/o elenco del Consorzio. Vivino e il web servono come prova interna, non si citano come fonte dei dati.
3. **Nessun doppione:** controllo per dominio, partita IVA e nome (le parole principali del nome coincidono con una scheda già in guida).
4. **Dati personali:** niente email personali (solo info@ e simili). Telefoni come pubblicati dal consorzio o dal sito.
5. **Niente si inventa:** sede completa (via, CAP, comune, provincia) o almeno CAP e comune dall'elenco; se manca, la voce resta in wip.

## Fasi (in quest'ordine)
1. **Inventario.** Quante schede ha già la regione, quante voci sono in wip, quali consorzi/denominazioni mancano. Elenco dei consorzi della regione con l'indirizzo del loro elenco soci.
2. **Consorzi con elenco soci.** Per ogni consorzio: scaricare l'elenco, separare i tipi di socio dove l'elenco li distingue (es. Langhe: "vinificatore" sì, "viticolo" no). Per ogni voce: nome, comune/sede, contatti, sito se c'è. Se la scheda del socio sul sito del consorzio ha indirizzo e vini dichiarati, leggerla (Roero, Alto Piemonte).
3. **Con sito.** Leggere il sito (sede, partita IVA, denominazioni citate). Se la pagina non mostra l'indirizzo senza browser, rileggerla con il browser vero sul Mac di Paolo.
4. **Vivino.** Scaricare l'elenco Vivino della regione (browser vero sul Mac). Serve a due cose: trovare produttori non nei consorzi e **provare** che un socio senza sito imbottiglia (vini propri su Vivino). Prima si provano i siti per dominio probabile, poi la ricerca su DuckDuckGo con il browser; si scartano pubblicità, aggregatori, registri imprese.
5. **Senza sito e senza prova.** Ricerca web per nome+comune. Prova accettata solo se un risultato nomina la cantina come produttore di vino (sito proprio, annuario di produttori, guida). Registri imprese, ristoranti e pagine dello stesso consorzio non valgono.
6. **Pubblicare a lotti**, con il passo nel registro, zip dei file cambiati, commit sul Mac e push. Dopo ogni lotto: numero di produttori in guida.
7. **Chiusura.** Elenco di ciò che resta in wip e perché (conferitori, nessuna prova, sede mancante). La regione si dichiara chiusa solo con questo elenco.

## Come si ricontrolla
- Campione di schede a caso sul sito dopo ogni lotto.
- Nomi puliti (senza "Az. Agr.", "S.S." e simili), province corrette, nessun indirizzo condiviso da cantine diverse senza motivo.

## Piemonte come esempio (numeri)
Guida: da ~3.900 a 4.747 produttori; Piemonte da ~470 a 1.249 schede. Canali: consorzi (Langhe 158, Colli Tortonesi 28, Barbera/Casalese/Gavi 43, Roero 22, Alto Piemonte 28+23), Vivino con sito (427 in 6 giri), recupero sedi (60+29), ricerca web (19). Rimasero fuori ~600 voci (soci viticoli, nessuna prova, sede mancante).
