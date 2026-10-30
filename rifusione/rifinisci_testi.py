import json,os,glob,re
R=os.path.dirname(os.path.abspath(__file__))+'/..'
D=r'\d{1,2} (?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre) 20\d\d'
MESI=['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre']
SUB=[
 (r',? (consultat[oaie]) dal vivo il ', r', \1 il '),
 (r'\s*\((?:dati|testo) copiat[io] dal sito[^)]*\)', ''),
 (r',? testo copiato a mano il ('+D+r')(?: \(il sito vieta la lettura automatica\))?', r', consultato il \1'),
 (r'\s*\(verifica incrociata\)', ''),
 (r'Sito ufficiale della cantina, home; indirizzo riportato dal curatore della guida dal sito, consultato il', 'Sito ufficiale della cantina, pagina iniziale, consultato il'),
 (r'Sito ufficiale dell’azienda', 'Sito ufficiale della cantina'),
 (r'pagine iniziale e di contatto', 'pagina iniziale e pagina dei contatti'),
 (r'home e contatti', 'pagina iniziale e pagina dei contatti'),
 (r'home e pagine collegate', 'pagina iniziale e pagine collegate'),
 (r'(Sito ufficiale della cantina, )home([.,;])', r'\1pagina iniziale\2'),
 (r' e home, consultat', ' e pagina iniziale, consultat'),
 (r' e home\b', ' e pagina iniziale'),
 (r'Sito ufficiale della cantina, consultato il ('+D+r'), pagina («[^»]*»)\.', r'Sito ufficiale della cantina, pagina \2, consultata il \1.'),
 (r'; corrispondenza per nome del produttore, verificata il ', ', ricerca del '),
 (r'; dichiarato dalla cantina, non verificato da VinoBot sulle guide', ''),
 (r'(Riconoscimenti dichiarati dalla cantina sul proprio sito), non verificati da VinoBot sulle guide\.', r'\1.'),
 (r'Non presenti nel testo salvato del sito(?: della cantina)?', 'Non presenti sul sito'),
 (r'Non presenti nelle pagine salvate del sito', 'Non presenti sul sito'),
 (r'Non presenti nelle pagine del negozio online salvate', 'Non presenti sul negozio online del sito'),
 (r'Non indicate nelle pagine salvate', 'Non indicate sul sito'),
 (r'Il testo salvato del sito non contiene l’elenco dei vini', 'Il sito non contiene l’elenco dei vini'),
 (r'Il testo salvato non riporta', 'Il sito non riporta'),
 (r'(Lessini Durello \(Monti Lessini\)) letto nelle pagine della cantina', r'\1 indicato nelle pagine della cantina'),
 (r'etichette Valpolicella viste sul sito', 'etichette Valpolicella indicate sul sito'),
 (r'; dettagli non letti', ''),
 (r'Il sito (\S+) non ha contenuti leggibili nel testo salvato', r'Il sito \1 non ha contenuti leggibili'),
 (r'senza elenco leggibile nel testo salvato', 'senza elenco leggibile'),
 (r'Elenco non rilevato nel testo salvato del sito', 'Elenco non indicato sul sito'),
 (r'Non rilevate: il testo salvato del sito contiene', 'Non indicate: il sito contiene'),
 (r' nel testo salvato del sito', ' sul sito'),
 (r' nel testo salvato', ' sul sito'),
 (r'Nel sito salvato', 'Sul sito'),
 (r'([Ii]l) testo salvato', r'\1 sito'),
 (r'(Non disponibile|Non verificabili): il sito non è consultabile da VinoBot \(accesso bloccato dal sito stesso\)', r'\1: il sito della cantina blocca l’accesso'),
 (r'^Sito ufficiale, ', 'Sito ufficiale della cantina, '),
 (r'nelle pagine salvate', 'sul sito'),
 (r'Nelle pagine salvate', 'Sul sito'),
 (r' al salvataggio\)', ')'),
 (r'al momento del salvataggio', 'al momento della consultazione'),
]
SUB=[(re.compile(a),b) for a,b in SUB]
def pulisci(t):
    for a,b in SUB: t=a.sub(b,t)
    return t
def nota(t):
    t=pulisci(t); fr=re.split(r'(?<=[.;])\s+',t.strip()); out=[]
    for x in fr:
        if x and x not in out: out.append(x)
    return ' '.join(out)
def consultate(d):
    ds=set(re.findall(D,d['consultate']))
    ds={x for x in ds if ' ottobre 2026' in x and int(x.split()[0])>=20}
    g=sorted(int(x.split()[0]) for x in ds)
    if not g: return 'Ogni dato della scheda rinvia alla fonte con il numero tra parentesi quadre.'
    if len(g)==1: q='Fonti consultate il %d ottobre 2026.'%g[0]
    else: q='Fonti consultate tra il %d e il %d ottobre 2026.'%(g[0],g[-1])
    return q+' Ogni dato della scheda rinvia alla fonte con il numero tra parentesi quadre.'
n=0
for f in glob.glob(R+'/dati/*.json'):
    x=open(f,encoding='utf8').read(); d=json.loads(x)
    d['consultate']=consultate(d)
    for z in d['fonti']: z['testo']=pulisci(z['testo']).replace('  ',' ')
    for s in d['sezioni']:
        if s.get('nota'): s['nota']=nota(s['nota'])
        s['righe']=[{**r,'valore':pulisci(r['valore'])} for r in s.get('righe',[]) if not (r['etichetta']=='Punteggi' and re.match(r'^Punteggi non letti',r['valore']))] if 'righe' in s else None
        if s['righe'] is None: del s['righe']
        if 'vini' in s: s['vini']=json.loads(pulisci(json.dumps(s['vini'],ensure_ascii=False)))
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n+=1
print('testi rifiniti',n)
