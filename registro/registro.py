# Registro della presenza online: per ogni cantina e ogni campo -> stato (trovato / cercato e non trovato / non cercato) + prova
import json,glob,os,re,csv,collections
DATA_GIRO='27–28 ottobre 2026'
CAMPI=['Sito ufficiale','Telefono','Email','Sede','Ragione sociale','P.IVA','Storia e proprietà','Elenco vini','Premi e punteggi',
 'Social','Negozio online sul sito','Marketplace','Google Business Profile','Vivino','Wine-Searcher','YouTube','Wikipedia','Presenza in elenchi o consorzio']
G={};ERR=set()
for f in sorted(glob.glob('giro/b0?.json')+['giro/b10.json','giro/b12.json','giro/b13.json']):
    for x in json.load(open(f)):
        (ERR.add(x['slug']) if 'errore' in x else G.__setitem__(x['slug'],x))
WK=json.load(open('arricchimenti/wikipedia.json')); WK_C=set(WK['cercate'])
VP=json.load(open('arricchimenti/vivino_presenza.json'))
GG=json.load(open('arricchimenti/google.json')); GG_C=set(GG['cercate'])
VIV=set(x['slug'] for x in json.load(open('vivino-nuovi.json')))
RS_T=set(l.split('|')[0] for l in open('rs/trovate.txt'))
RS_N=set(l.split('|')[0] for l in open('rs/nonrovate.txt'))
SITI29=set(open('registro/sito_cercati.txt').read().split())
FONDO=set(json.load(open('/tmp/nosito_rs.json')) and [a for a,_,_ in json.load(open('/tmp/nosito_rs.json'))])
def clean(v): return re.sub(r'\s*\[\[\d+\]\]','',v).strip()
PLACE=('Non ','Presenza non','Compare nell')
def isph(v):
    v=clean(v); return (not v) or v.startswith(('Non ','Presenza non'))
righe=[];summ=[]
for f in sorted(glob.glob('dati/*.json')):
    s=os.path.basename(f)[:-5];d=json.load(open(f))
    fonti={x['n']:x for x in d.get('fonti',[])}
    R=[(sec['titolo'],r) for sec in d['sezioni'] for r in sec.get('righe',[])]
    def rows(*labels):
        return [r for t,r in R if r['etichetta'] in labels or any(r['etichetta'].startswith(l) for l in labels if l.endswith('*'))]
    def prova(rs):
        ns=[];
        for r in rs: ns+= [int(n) for n in re.findall(r'\[\[(\d+)\]\]',r['valore'])]
        ns=sorted(set(ns)) or ([1] if 1 in fonti else [])
        urls=[fonti[n]['url'] for n in ns if n in fonti and fonti[n].get('url')]
        dts=[m.group(1) for n in ns if n in fonti for m in [re.search(r'consultat\w* il (\d+ \w+ 20\d\d)',fonti[n]['testo'])] if m]
        return ' ; '.join(dict.fromkeys(urls)),' ; '.join(dict.fromkeys(dts))
    letto=s in G; errore=s in ERR
    cons_url=fonti.get(1,{}).get('url','')
    st={}
    def T(c,rs,nota=''):
        u,dt=prova(rs); st[c]=('trovato',u,dt,nota)
    def C(c,u,dt,nota): st[c]=('cercato e non trovato',u,dt,nota)
    def N(c,nota=''): st[c]=('non cercato','','',nota)
    sito=[r for r in rows('Sito ufficiale','Sito') if not isph(r['valore'])]
    if sito: T('Sito ufficiale',sito)
    elif s in FONDO: C('Sito ufficiale','',  '28 ottobre 2026','ricerca web standard e ricerca approfondita (28 ottobre: motori di ricerca, portali, domini ipotizzati) senza sito verificato')
    elif s in SITI29: C('Sito ufficiale','','28–29 ottobre 2026','ricerca web (motori di ricerca, portali, domini ipotizzati) senza sito verificato')
    else: N('Sito ufficiale','nessun sito nell’elenco del Consorzio; ricerca autonoma non registrata')
    con=[r for r in rows('Contatti') if not isph(r['valore'])]
    tel=[r for r in con if re.search(r'Tel|\+?\d{2,}[\s\d]{6,}',r['valore'])]
    em=[r for r in con if '@' in r['valore']]
    sitoletto=letto or (s in RS_T or s in RS_N)
    def fallback(c,motivo_ok='sito della cantina letto (home e pagine collegate)'):
        if letto: C(c,sito and prova(sito)[0] or '',DATA_GIRO,motivo_ok)
        elif errore: N(c,'sito non leggibile (bloccato, lento o non disponibile)')
        elif not sito: N(c,'nessun sito noto')
        else: N(c,'sito noto ma non ancora letto per questo campo')
    for c,rr in (('Telefono',tel),('Email',em)):
        T(c,rr) if rr else fallback(c)
    sede=[r for r in rows('Sede','Sede e cantina','Collocazione') if not isph(r['valore'])]
    if sede: T('Sede',sede)
    else: C('Sede',cons_url,'24 ottobre 2026','pagina del Consorzio senza indirizzo') if cons_url else N('Sede')
    rag=[r for r in rows('Ragione sociale','Ragione sociale e P.IVA') if not isph(r['valore'])]
    if rag: T('Ragione sociale',rag)
    else:
        if s in RS_N or letto: C('Ragione sociale',prova(sito)[0] if sito else '',DATA_GIRO,'piè di pagina o note legali del sito letti, nome non trovato')
        elif errore: N('Ragione sociale','sito non leggibile')
        elif cons_url: C('Ragione sociale',cons_url,'24 ottobre 2026','pagina del Consorzio senza ragione sociale')
        else: N('Ragione sociale')
    piva=[r for r in rows('P.IVA','Partita IVA','Ragione sociale e P.IVA','Ragione sociale') if re.search(r'\b\d{11}\b',r['valore'])]
    if piva: T('P.IVA',piva)
    elif s in RS_N or letto: C('P.IVA',prova(sito)[0] if sito else '',DATA_GIRO,'piè di pagina o note legali del sito letti, P.IVA non trovata')
    elif errore: N('P.IVA','sito non leggibile')
    else: N('P.IVA','sito non letto per questo campo')
    for c,labs in (('Storia e proprietà',('Storia e proprietà',)),('Elenco vini',('Elenco vini*',)),('Premi e punteggi',('Premi e punteggi','Premi','Punteggi'))):
        rr=rows(*labs)
        ok=[r for r in rr if not isph(r['valore'])]
        if c=='Elenco vini':
            ok=[r for r in ok] or [r for t,r in R if t=='Vini' and not isph(r['valore']) and not r['etichetta'].startswith('Denominazioni')]
            if not ok and any(sec['titolo']=='Vini' and sec.get('vini') for sec in d['sezioni']): ok=[{'valore':'','etichetta':'Vini'}]
        if ok: T(c,ok)
        elif rr and any('sito della cantina' in r['valore'] and 'non ancora' not in r['valore'] for r in rr): C(c,'',DATA_GIRO,'sito della cantina letto')
        elif c=='Elenco vini': N(c,'non ancora raccolto dal sito della cantina')
        else: fallback(c)
    soc=[r for r in rows('Social') if not isph(r['valore'])]
    T('Social',soc) if soc else fallback('Social')
    vend=[r for r in rows('Vendita online','Negozio online') if not isph(r['valore'])]
    T('Negozio online sul sito',vend) if vend else fallback('Negozio online sul sito')
    mk=[r for r in rows('Marketplace') if not isph(r['valore'])]
    if mk: T('Marketplace',mk)
    else: N('Marketplace','presenza su marketplace mai verificata')
    if s in GG['trovate']: st['Google Business Profile']=('trovato',GG['trovate'][s]['url'],GG['data'],'')
    elif s in GG_C: C('Google Business Profile','',GG['data'],'ricerca con Google Places (nome + indirizzo), nessuna scheda corrispondente sicura')
    else: N('Google Business Profile','mai verificato');
    viv=[u['url'] for u in d.get('fonti',[]) if 'vivino' in (u.get('url') or '')]
    if viv: st['Vivino']=('trovato',' ; '.join(viv),'', '')
    elif s in VIV: st['Vivino']=('trovato','','','cantina individuata nell’elenco produttori di Vivino; indirizzo della scheda non salvato (prova da ricreare)')
    elif s in VP.get('trovate_ricerca',{}): st['Vivino']=('trovato','',VP['data'],'ricerca diretta su Vivino: vino «'+VP['trovate_ricerca'][s]+'»')
    elif s in VP['trovate']: st['Vivino']=('trovato','',VP['data'],'cantina presente negli elenchi Vivino scaricati; corrispondenza per nome: «'+VP['trovate'][s]+'»')
    elif s in set(VP.get('cercate',[])) and s not in VP['incerte']: C('Vivino','',VP['data'],'ricerca diretta su Vivino con 1-3 varianti del nome: nessun produttore corrispondente')
    elif s in VP['incerte']: N('Vivino','nome presente più volte negli elenchi Vivino, da verificare a mano')
    else: N('Vivino','non presente negli elenchi Vivino scaricati (13.672 cantine), non cercato direttamente')
    N('Wine-Searcher','mai verificato')
    yt=[r for r in soc if 'youtube' in r['valore'].lower()]
    T('YouTube',yt) if yt else (fallback('YouTube') if letto else N('YouTube','mai verificato'))
    if s in WK['trovate']: st['Wikipedia']=('trovato',WK['trovate'][s]['url'],WK['data'],'')
    elif s in WK_C: C('Wikipedia','',WK['data'],'ricerca su Wikipedia in italiano (nome della cantina + «vino», primi risultati) senza voce dedicata')
    else: N('Wikipedia','mai verificato')
    el=[r for r in rows('Consorzio','Presenza in elenchi') if not isph(r['valore'])]
    T('Presenza in elenchi o consorzio',el) if el else N('Presenza in elenchi o consorzio')
    cnt=collections.Counter(v[0] for v in st.values())
    for c in CAMPI:
        v=st[c]; righe.append([s,d['nome'],c,v[0],v[1],v[2],v[3]])
    summ.append([s,d['nome'],cnt['trovato'],cnt['cercato e non trovato'],cnt['non cercato'],round(cnt['trovato']/len(CAMPI),3),round((cnt['trovato']+cnt['cercato e non trovato'])/len(CAMPI),3)])
out='/tmp/claude-0/-home-claude/d155faf6-1db0-5293-a642-f17d92f455f5/scratchpad/'
with open(out+'vinobotte-web-campi.csv','w',newline='',encoding='utf-8-sig') as fh:
    w=csv.writer(fh);w.writerow(['slug','cantina','campo','stato','prova (pagina)','data prova','nota']);w.writerows(righe)
with open(out+'vinobotte-web-indice.csv','w',newline='',encoding='utf-8-sig') as fh:
    w=csv.writer(fh);w.writerow(['slug','cantina','campi trovati','campi cercati e non trovati','campi non cercati','indice di reperibilità (trovati/18)','copertura della ricerca (cercati/18)']);w.writerows(sorted(summ,key=lambda r:-r[2]))
tot=collections.Counter((r[2],r[3]) for r in righe)
print(len(summ),len(righe))
for c in CAMPI: print(c.ljust(34),[tot[(c,x)] for x in('trovato','cercato e non trovato','non cercato')])
idx=[r[5] for r in summ];print('indice medio',round(sum(idx)/len(idx),3),'max',max(idx),'min',min(idx))
import statistics;print('mediana',statistics.median(idx))
