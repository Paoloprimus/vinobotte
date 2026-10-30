import json,os,glob,re
R=os.path.dirname(os.path.abspath(__file__))+'/..'
n=0
FRASE=re.compile(r'(?:\s*;\s*dichiarati|\s*Dichiarati) dalla cantina(?: sul proprio sito)?, non verificati da VinoBot sulle guide\.?')
for f in glob.glob(R+'/dati/*.json'):
    x=open(f,encoding='utf8').read(); y=FRASE.sub('',x)
    if y!=x: open(f,'w',encoding='utf8').write(y)
for f in glob.glob(R+'/dati/*.json'):
    d=json.load(open(f,encoding='utf8')); ch=False
    for s in d['sezioni']:
        if s['titolo']=='Identità online': s['titolo']='Presenza online'; ch=True
        if s['titolo']!='Presenza online': continue
        nuove=[]
        for r in s.get('righe',[]):
            v=r['valore']
            if r['etichetta'].startswith('Negozi online'):
                if v.strip()=='Presenza non verificata': ch=True; continue
                v2=re.sub(r';\s*altri marketplace: presenza non verificata','',v)
                if v2!=v: r['valore']=v2; ch=True
            if r['etichetta']=='Piattaforme':
                righe=[]
                for l in v.split('\n'):
                    l=re.sub(r';\s*altre presenze non verificate','',l)
                    m=re.match(r'^(.+?) (indicat[oi]|citat[oi]) (dal sito|nella cookie policy del sito)(.*?)((?:\s*\[\[\d+\]\])*)$',l)
                    if m:
                        voci=[x.strip() for x in re.split(r',\s*|\s+e\s+(?=[A-Z])',m.group(1)) if x.strip()]
                        if len(voci)>1:
                            verbo='indicato' if m.group(2).startswith('indic') else 'citato'
                            for i,x in enumerate(voci):
                                righe.append(f'{x}: {verbo} {m.group(3)}{m.group(4)}'+(m.group(5) if i==len(voci)-1 else ''))
                            continue
                    righe.append(l)
                nv='\n'.join(righe)
                if nv!=v: r['valore']=nv; v=nv; ch=True
            if r['etichetta']=='Social' and '; ' in v and '\n' not in v:
                m=re.search(r'\s*(\[\[\d+\]\])\s*$',v); fn=m.group(1) if m else ''
                body=v[:m.start()] if m else v
                r['valore']='\n'.join(body.split('; '))+(' '+fn if fn else ''); ch=True
            if r['etichetta']=='Sito' and '; ' in v and '\n' not in v:
                m=re.search(r'((?:\s*\[\[\d+\]\])+)\s*$',v); fn=m.group(1) if m else ''
                body=v[:m.start()] if m else v
                r['valore']='\n'.join(body.split('; '))+fn; ch=True
            if r['etichetta']=='Vivino' and v.startswith('Presente su Vivino come'):
                r['valore']=v.replace('Presente su Vivino come','Presente come'); ch=True
            if not r['valore'].strip(): ch=True; continue
            nuove.append(r)
        s['righe']=nuove
    d['sezioni']=[s for s in d['sezioni'] if s.get('righe') or s.get('tipo')=='vini' or s['titolo']!='Presenza online']
    if ch: json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n+=1
print('presenza online:',n)

# ---- seconda passata: premi/punteggi a mano, negozi/marketplace, ridondanze
MAN={}
_b=open(R+'/rifusione/premi_manuali.txt',encoding='utf8').read().strip().split('\n\n')
for b in _b:
    L=b.split('\n'); MAN[L[0].strip()]=([x[3:] for x in L[1:] if x.startswith('P: ')],[x[3:] for x in L[1:] if x.startswith('S: ')])
FNR=re.compile(r'((?:\s*\[\[\d+\]\])+)\s*$')
MKT={'nicolis','dal-moro','schenk-italia','trabucchi-dillasi'}
GEN=re.compile(r'^(Negozio online|Negozio|Wine shop online|Wine shop|Shop online|Shop)(?: sul sito)?\s*',re.I)
n2=0
for f in glob.glob(R+'/dati/*.json'):
    d=json.load(open(f,encoding='utf8')); slug=d['slug']; ch=False
    for s in d['sezioni']:
        righe=s.get('righe')
        if not righe: continue
        has_ve=any(r['etichetta']=='Vendita online' and r['valore'].startswith('Negozio online sul sito della cantina') for r in righe)
        nuove=[]
        for r in righe:
            e=r['etichetta']; v=r['valore']
            if e=='Premi e punteggi' and slug in MAN:
                m=FNR.search(v); fn=m.group(1).strip() if m else ''
                P,S=MAN[slug]
                if P: nuove.append({'etichetta':'Premi','valore':'\n'.join(P)+(' '+fn if fn else '')})
                if S: nuove.append({'etichetta':'Punteggi','valore':'\n'.join(S)+(' '+fn if fn else '')})
                ch=True; continue
            if e=='Vendita online' and v.startswith('Negozio online sul sito della cantina: '):
                r['etichetta']='Negozio online'; r['valore']=v.replace('Negozio online sul sito della cantina: ','',1); ch=True
            elif e.startswith('Negozi online') :
                v2=re.sub(r';\s*marketplace: presenza non verificata','',v)
                if v2.startswith('Presenza su marketplace non verificata'): ch=True; continue
                if slug in MKT: r['etichetta']='Marketplace'
                elif has_ve: ch=True; continue
                else:
                    r['etichetta']='Negozio online'
                    m=FNR.search(v2); fn=m.group(1).strip() if m else ''
                    body=v2[:m.start()] if m else v2
                    mm=GEN.match(body)
                    if mm:
                        rest=body[mm.end():].strip()
                        body='Presente'+(' '+rest if rest else '')
                    v2=body+(' '+fn if fn else '')
                r['valore']=v2; ch=True
            if r['etichetta'] in ('Piattaforme','Social','Marketplace'):
                ls=[]
                for l in r['valore'].split('\n'):
                    if re.match(r'^(YouTube|Instagram|Social|Facebook|LinkedIn|Twitter|X|TikTok)\w*:? non indicat[oi] dal sito',l): continue
                    l=re.sub(r':? (?:indicat[oiae]|citat[oiae]) dal sito','',l)
                    ls.append(l)
                v3='\n'.join(ls).strip(' ,;')
                if v3!=r['valore']: r['valore']=v3; ch=True
                if not v3.strip(): continue
            v4=r['valore'].replace('Denominazioni DOC e DOCG indicate sul sito ufficiale:','Denominazioni DOC e DOCG:')
            v4=re.sub(r',\s*(?=\[\[)',' ',v4)
            if v4!=r['valore']: r['valore']=v4; ch=True
            nuove.append(r)
        s['righe']=nuove
    d['sezioni']=[s for s in d['sezioni'] if s.get('righe') or s.get('tipo')=='vini' or 'righe' not in s]
    if ch: json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n2+=1
print('seconda passata:',n2)
