set -e
cd /home/claude/annuario
python3 -I rifusione/fondi.py applica | tail -1
rm -rf dati chiarire pagine; cp -r rifusione/out/dati dati; cp -r rifusione/out/chiarire chiarire; cp rifusione/out/produttori.json produttori.json; mkdir pagine
python3 -I rifusione/aggiungi_extra.py
python3 -I rifusione/aggiungi_tile.py
python3 -I rifusione/aggiungi_nuovi_vernaccia.py
python3 -I rifusione/aggiungi_nuovi_vivino.py
python3 -I rifusione/aggiungi_montecucco.py
python3 -I rifusione/aggiungi_wip.py
python3 -I rifusione/applica_arricchimenti.py
python3 -I rifusione/applica_rs.py
python3 -I rifusione/applica_giro.py
python3 -I rifusione/applica_fondo.py
python3 -I rifusione/applica_piva_b13.py
python3 -I rifusione/applica_wikipedia.py
python3 -I rifusione/applica_google.py
python3 -I rifusione/applica_siti_google.py
python3 -I rifusione/applica_vivino_presenza.py
python3 -I rifusione/applica_piattaforme.py
python3 -I rifusione/applica_vini.py
python3 -I rifusione/applica_raggiungibilita.py
python3 -I rifusione/applica_consorzio_chianti.py
python3 -I rifusione/applica_consorzio_carmignano.py
python3 -I rifusione/applica_consorzio_candia.py
python3 -I rifusione/applica_consorzio_terre_di_pisa.py
python3 -I rifusione/applica_consorzio_montescudaio.py
python3 -I rifusione/applica_consorzio_val_di_cornia.py
python3 -I rifusione/rifinisci_presenza.py
python3 -I rifusione/rifinisci_anagrafica.py
python3 -I rifusione/rifinisci_testi.py
node genera-schede.mjs | tail -1
python3 -I rifusione/costruisci2.py 2>&1 | grep -v Deprec | grep -v "re.sub" | head -3
