import json,os,glob,re
R=os.path.dirname(os.path.abspath(__file__))+'/..'
FN=re.compile(r'(?:\s*\[\[\d+\]\])+\s*$')
def fn(v):
    m=FN.search(v); return (v[:m.start()],m.group(0).strip()) if m else (v,'')
def toks(t): return re.findall(r'\w+',t.lower())
def ridondante(val,altri):
    val=re.sub(r'\[\[\d+\]\]','',val)
    U=' '.join(altri); ut=set(toks(U)); ud=re.sub(r'\D','',U)
    for t in toks(val):
        if t in('tel','fax','email','cell','whatsapp'): continue
        if t.isdigit() and len(t)>=6:
            if t not in ud: return False
        elif t not in ut: return False
    return True
RANK=lambda e:(2.5 if e=='Contatti' else 0 if e.startswith('Ragione sociale') else 1 if e.startswith('Partita IVA') or e in('P.IVA','Codice fiscale / P. IVA','REA','Capitale sociale') else 3 if e in('Telefono','Email') else 4 if e=='Sito ufficiale' else 5 if e in('Consorzio','Consorzi') else 6 if e.startswith('Dati ') else 2)
PIVA=re.compile(r'(?:p\.?\s?i\.?v\.?a\.?|p\.\s?i\.|partita\s+iva)\s*:?\s*((?:IT)?\d{11})',re.I)

PIVA=re.compile(r'((?:C\.\s?F\.\s*(?:e|/)\s*)?(?:partita\s+iva|P\.?\s?I(?:\.|VA)?\.?)(?:\s*(?:e|/)\s*(?:C\.?\s?F\.?|codice fiscale|codice fiscale))?)\s*:?\s*(?:IT\s?)?(\d{11})',re.I)
BARE=re.compile(r'^(?:IT\s?)?(\d{11})$')
RUMORE=re.compile(r'Powered|Cod\. dest|Agency',re.I)
def maiusc(t): return t[:1].upper()+t[1:]
def pulisci_nome(n):
    n=n.replace('©','').strip(); n=re.sub(r'^[\s\-–—,;:.]+','',n)
    n=re.sub(r'^[\s\-–—]+','',n)
    if re.match(r'^(GPS|Tel|CIN|CIR)\b',n): return ''
    mm=re.split(r'\s*-\s+',n,1)
    if len(mm)==2 and re.search(r'\d',mm[1]): n=mm[0]
    seg=n.split(', ')
    n=', '.join([seg[0]]+[x for i,x in enumerate(seg[1:]) if not re.search(r'\d',x)] if not any(re.search(r'\d',x) for x in seg[1:]) else [seg[0]])
    n=re.sub(r'\s+Loc\..*$','',n)
    return re.sub(r'[\s,;:–—-]+$','',n).strip()
def analizza(v,piva_label=False):
    """Restituisce (nome, piva, cf_flag, rea, cap, note, fns)."""
    fns=[]
    for m in re.finditer(r'\[\[\d+\]\]',v):
        if m.group(0) not in fns: fns.append(m.group(0))
    c=re.sub(r'\s*\[\[\d+\]\]','',v).strip()
    if c.startswith('Non disponibile'): return None
    nome='';piva=None;cf=False;rea=None;cap=None;note=[]
    segs=[x.strip() for x in re.split(r';\s+',c) if x.strip()]
    for i,sg in enumerate(segs):
        m=PIVA.search(sg); b=BARE.match(sg)
        if i==0 and piva_label and not b:
            mb=re.match(r'^(?:P\.?\s?I(?:\.|VA)?\.?\s*:?\s*)?(?:IT\s?)?(\d{11})\b[\s,]*(.*)$',sg,re.I)
            if mb:
                piva=mb.group(1)
                if mb.group(2).strip(): note.append(mb.group(2).strip())
                continue
        if i>0 and m and piva is None and m.start()==0 and not b:
            piva=m.group(2); cf=bool(re.search(r'C\.?\s?F|codice',m.group(1),re.I))
            for t in re.split(r',\s*',sg[m.end():].strip(' ,.')):
                if t.strip(): segs.append(t.strip())
            continue
        if i==0 and not b:
            if m:
                nome=pulisci_nome(sg[:m.start()]); piva=m.group(2); cf=bool(re.search(r'C\.?\s?F|codice',m.group(1),re.I))
                resto=sg[m.end():]
                if RUMORE.search(resto): resto=''
                for t in re.split(r',\s*',resto.strip(' ,.')):
                    t=t.strip()
                    if t and not re.match(r'^[\s\-–]*(CIN|CIR|GPS|Tel|Cell)\b',t): segs.append(t)
            else:
                mm=re.match(r'^(.*?),\s*(che .*)$',sg)
                if mm: nome=pulisci_nome(mm.group(1)); note.append(mm.group(2))
                else: nome=pulisci_nome(sg)
            continue
        if b and piva is None: piva=b.group(1); continue
        if m and piva is None and re.fullmatch(r'\s*'+PIVA.pattern+r'\s*',sg,re.I): piva=m.group(2); cf=bool(re.search(r'C\.?\s?F|codice',m.group(1),re.I)); continue
        if re.match(r'^REA\b',sg,re.I): rea=re.sub(r'^REA\s*(?:n\.\s*)?','',sg,flags=re.I).strip(); continue
        if re.match(r'^capitale sociale',sg,re.I): cap=re.sub(r'^capitale sociale\s*','',sg,flags=re.I).strip(); continue
        if RUMORE.search(sg) or re.match(r'^[\s\-–]*(CIN|CIR|GPS|Tel|Cell)\b',sg): continue
        note.append(sg)
    return nome,piva,cf,rea,cap,note,fns

tot={'cont':0,'cons':0,'dati':0}
for f in glob.glob(R+'/dati/*.json'):
    d=json.load(open(f,encoding='utf8'))
    for s in d['sezioni']:
        if s['titolo']!='Anagrafica': continue
        righe=[]; cons=[]
        for r in s['righe']:
            e,v=r['etichetta'],r['valore']
            if re.match(r'^(Non indicat|Non disponibil)',v) or (e.startswith('Denominazioni') and re.match(r'^Non indicat',v)):
                tot['nd']=tot.get('nd',0)+1; continue
            v=re.sub(r'\s*\([^()]*(?:non indicat|non riportat|non letto)[^()]*\)','',v)
            v=re.sub(r'\s*—\s*indirizzo non letto[^\[]*','',v)
            if e=='Sito ufficiale':
                mu=re.search(r'\{\{(?:https?://)?(?:https?://)?([^|}]*)\|',v,re.I)
                if mu and ('@' in mu.group(1) or not re.match(r'^[^/]*\.[a-z]{2,}(?:/|$)',mu.group(1),re.I)): tot['sitobad']=tot.get('sitobad',0)+1; continue
                v=re.sub(r'(?i)https?://https?://','http://',v)
            if e in('Ragione sociale e P.IVA','Ragione sociale','Partita IVA','P.IVA'):
                v=re.sub(r'\s*\(come da (?:elenco|mappa|scheda)[^)]*\)','',v)
                A=analizza(v,e in('Partita IVA','P.IVA'))
                pl=e in('Partita IVA','P.IVA')
                if A is None: tot['nd']=tot.get('nd',0)+1; continue
                nome,piva,cf,rea,cap,note,fns=A; nf=' '+' '.join(fns) if fns else ''
                if pl and note: righe.append({'etichetta':'Partita IVA','valore':piva+nf+''.join('\n'+maiusc(x) for x in note)}); piva=None
                elif nome: righe.append({'etichetta':'Ragione sociale','valore':nome+nf+''.join('\n'+maiusc(x) for x in note)})
                elif note: righe.append({'etichetta':'Ragione sociale','valore':'\n'.join(maiusc(x) for x in note)+nf})
                if piva: righe.append({'etichetta':'Partita IVA e codice fiscale' if cf else 'Partita IVA','valore':piva+nf})
                if rea: righe.append({'etichetta':'REA','valore':rea+nf})
                if cap: righe.append({'etichetta':'Capitale sociale','valore':cap+nf})
                continue
            if e=='Contatti':
                c,nf=fn(v); tel=[]; em=[]; altro=[]; orari=[]
                c=re.sub(r'\s+E-?mail:\s*','; ',c,flags=re.I)
                for p in re.split(r';\s*|\s+·\s+',c):
                    p=p.strip()
                    if not p: continue
                    if re.search(r'non (?:indicat|present|riport|disponib)|assent',p,re.I) and not re.search(r'\d{6,}|@',p): continue
                    if p.startswith('('): continue
                    p=re.sub(r'\s*\([^()]*non (?:indicat|riport|present|disponib)[^()]*\)','',p).strip()
                    if '@' in p: em.append(re.sub(r'^email\s*','',p,flags=re.I))
                    elif len(re.sub(r'\D','',p))>=6 and not re.search(r'\d{1,2}[:.]?\d*\s*–\s*\d',p) or re.match(r'^(Tel|fax|cell|mobile|WhatsApp)',p,re.I): tel.append(re.sub(r'^Tel\.\s+','',p))
                    elif re.match(r'^(Aperto|Wine shop|Orari)',p) or re.search(r'\d{1,2}(?::\d\d)?\s*–\s*\d{1,2}',p): orari.append(p)
                    else: altro.append(p)
                sf=' '+nf if nf else ''
                if tel: righe.append({'etichetta':'Telefono','valore':'\n'.join(tel)+sf})
                if em: righe.append({'etichetta':'Email','valore':'\n'.join(em)+sf})
                if orari: righe.append({'etichetta':'Orari','valore':'\n'.join(maiusc(x) for x in orari)+sf})
                if altro: righe.append({'etichetta':'Contatti','valore':'\n'.join(maiusc(x) for x in altro)+sf})
                tot['cont']+=1; continue
            if e=='Consorzio':
                c,nf=fn(v); m=re.search(r'(Consorzio.*)$',c)
                cons.append(((m.group(1) if m else c).strip()+(' '+nf if nf else ''),len(righe))); continue
            righe.append({'etichetta':e,'valore':v})
        if cons:
            seen=[];[seen.append(x) for x,_ in cons if x not in seen]
            seen.sort(key=lambda x:int((re.findall(r'\[\[(\d+)\]\]',x) or ['99'])[0]))
            righe.append({'etichetta':'Consorzi' if len(seen)>1 else 'Consorzio','valore':'\n'.join(seen)}); tot['cons']+=1
        base=[r for r in righe if not r['etichetta'].startswith('Dati ')]
        fin=[]
        for r in righe:
            if r['etichetta'].startswith('Dati ') and ridondante(r['valore'],[b['valore'] for b in base]): tot['dati']+=1; continue
            fin.append(r)
        uniti=[]; idx={}
        for r in fin:
            if r['etichetta'] in idx:
                t=uniti[idx[r['etichetta']]]
                vn,fnn=fn(r['valore']); chiavi=[re.sub(r'\s*(\[\[\d+\]\])+\s*$','',l).strip() for l in t['valore'].split('\n')]
                if vn.strip() in chiavi:
                    k=chiavi.index(vn.strip()); ls=t['valore'].split('\n'); a,b2=fn(ls[k])
                    ls[k]=a+' '+' '.join(dict.fromkeys((b2+' '+fnn).split())); t['valore']='\n'.join(ls)
                else: t['valore']+='\n'+r['valore']
            else: idx[r['etichetta']]=len(uniti); uniti.append(dict(r))
        fin=uniti
        s['righe']=sorted(fin,key=lambda r:RANK(r['etichetta']))
    # rinumera note per ordine di comparsa
    txt=json.dumps(d['sezioni'],ensure_ascii=False)
    ordine=[]
    for m in re.finditer(r'\[\[(\d+)\]\]',txt):
        if int(m.group(1)) not in ordine: ordine.append(int(m.group(1)))
    resto=[x['n'] for x in d['fonti'] if x['n'] not in ordine]
    mp={o:i+1 for i,o in enumerate(ordine+resto)}
    d['sezioni']=json.loads(re.sub(r'\[\[(\d+)\]\]',lambda m:'[[%d]]'%mp[int(m.group(1))],txt))
    for x in d['fonti']: x['n']=mp[x['n']]
    d['fonti'].sort(key=lambda x:x['n'])
    if 'consultate' in d and isinstance(d['consultate'],str): pass
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print(tot)
