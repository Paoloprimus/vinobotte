#!/usr/bin/env python3
"""Costruisce api/_dati-chat.json, l'indice compatto usato dalla funzione della chat.

Legge produttori.json e dati/*.json (le schede) e scrive un record per produttore
con i soli dati utili a rispondere: sede, contatti, denominazioni, vini (campo v), ospitalità,
negozio online, social, Vivino, consorzio, riconoscimenti, storia.
Toglie dai testi i numeri di fonte [[n]] e trasforma {{url|etichetta}} in "etichetta (url)".

Uso:  python3 costruisci-chat.py
"""
import json, re, sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
USCITA = QUI / 'api' / '_dati-chat.json'

# sezione -> etichette da tenere (None = tutte)
TIENI = {
    'Anagrafica': None,
    'Vini': None,
    'Ospitalità': None,
    'Produzione e servizi': None,
    'Presenza online': {'Sito', 'Negozio online', 'Social', 'Vivino', 'Google Maps'},
    'Riconoscimenti': {'Premi e punteggi', 'Premi', 'Punteggi'},
    'Riconoscimenti dichiarati dalla cantina': None,
    'Riconoscimenti verificati': None,
    'Azienda: proprietà e struttura': {'Storia e proprietà', 'Vigneti'},
    'Storia': None,
}
ASSENTE = re.compile(r'^(non presenti?|non indicat|nessun|n/d)', re.I)
MAX_VALORE = 500


def pulisci(v):
    v = re.sub(r'\s*\[\[\d+\]\]', '', v)
    v = re.sub(r'\{\{([^|}]*)\|([^}]*)\}\}', lambda m: f'{m.group(2)} ({m.group(1)})', v)
    v = re.sub(r'[ \t]+', ' ', v).strip()
    if len(v) > MAX_VALORE:
        v = v[:MAX_VALORE].rsplit(' ', 1)[0] + ' …'
    return v


def main():
    prod = json.load(open(QUI / 'produttori.json', encoding='utf-8'))
    out = []
    mancanti = 0
    for p in prod:
        f = QUI / 'dati' / f"{p['slug']}.json"
        righe, vini = {}, {}
        if f.exists():
            d = json.load(open(f, encoding='utf-8'))
            for s in d.get('sezioni', []):
                titolo = s.get('titolo')
                if titolo not in TIENI:
                    continue
                ok = TIENI[titolo]
                for r in s.get('righe', []):
                    et, val = r.get('etichetta'), pulisci(r.get('valore', ''))
                    if not val or ASSENTE.match(val):
                        continue
                    if ok is not None and et not in ok:
                        continue
                    if titolo == 'Vini' or re.search(r'denominazion', et, re.I):
                        vini[et if et not in vini else f'{et} ({titolo})'] = val
                    else:
                        righe[et if et not in righe else f'{et} ({titolo})'] = val
        else:
            mancanti += 1
        tipi = []
        for grp, dens in (p.get('tipi') or {}).items():
            tipi.append({'g': grp, 'd': dens})
        out.append({'s': p['slug'], 'n': p['nome'], 'r': p.get('regione', ''),
                    'c': p.get('comune', ''), 't': tipi, 'v': vini, 'k': righe})
    USCITA.parent.mkdir(exist_ok=True)
    json.dump(out, open(USCITA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    mb = USCITA.stat().st_size / 1e6
    print(f'produttori: {len(out)} | senza scheda: {mancanti} | {USCITA.relative_to(QUI)}: {mb:.1f} MB')


if __name__ == '__main__':
    sys.exit(main())
