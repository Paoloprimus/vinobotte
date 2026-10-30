import sys,os,json,re,collections,shutil
sys.path.insert(0,'/home/claude/annuario/rifusione')
from produttori import *
from produttori import _reg_from_sede
PLACE=re.compile(r'^(Non disponibile|Non presenti?|Presenza non verificata|Non indicat|Non ancora|Piattaforme .*non verificata|Elenco vini \|)',re.I)
def ph(v): return bool(PLACE.match(re.sub(r'\[\[\d+\]\]','',v).strip()))
def strip_suffix(slug):
    for st in sorted(STEMS,key=len,reverse=True):
        if slug.endswith(st): return slug[:-len(st)]
    return slug
# assegnazioni regione manuali (da confermare)
FORCE={'albino-armani':'Veneto','bosco-del-merlo':'Veneto','le-tenute-del-leone-alato':'Veneto','vendrame-vignis-del-doge':'Friuli Venezia Giulia','poggiolivi':'Toscana','ruffoni':'Veneto','contri-spumanti':'Veneto','marocchesa':'Veneto','cantine-sgarzi':'Emilia-Romagna'}
def regione_produttore(v):
    votes=collections.Counter()
    for s in v:
        r,w=reg_scheda(s)
        if r: votes[r]+=3
        else:
            x=SECREG.get(cerca[s][3])
            if x: votes[x]+=1
    return votes
def score(d): return sum(len(s.get('righe',[]))+len(s.get('vini',[])) for s in d['sezioni'])
def fondi(v,reg):
    # primario: nella regione, con più contenuto; preferisci slug senza suffisso
    cand=[s for s in v if (reg_scheda(s)[0] or SECREG.get(cerca[s][3]))==reg] or v
    prim=next((s for s in v if s in PRIMF),None) or max(cand,key=lambda s:(score(DATI[s]),-len(s)))
    P=json.loads(json.dumps(DATI[prim]))
    for sz in P['sezioni']:
        if 'righe' in sz: sz['righe']=[r for r in sz['righe'] if r['etichetta']!='Altro consorzio']
    P['sezioni']=[sz for sz in P['sezioni'] if sz.get('righe') or sz.get('vini')]
    fonti=P['fonti']
    idx={}
    for f in fonti: idx[f.get('url') or f['testo']]=f['n']
    consultate=[P['consultate']]
    for s in sorted(v,key=lambda x:(x!=prim,x)):
        if s==prim: continue
        O=json.loads(json.dumps(DATI[s]))
        mp={}
        for f in O['fonti']:
            k=f.get('url') or f['testo']
            if k in idx: mp[f['n']]=idx[k]
            else:
                n=len(fonti)+1;f2=dict(f);f2['n']=n;fonti.append(f2);idx[k]=n;mp[f['n']]=n
        rem=lambda t:re.sub(r'\[\[(\d+)\]\]',lambda m:'[[%d]]'%mp.get(int(m.group(1)),int(m.group(1))),t)
        if O['consultate'] not in consultate: consultate.append(O['consultate'])
        for sz in O['sezioni']:
            tgt=next((x for x in P['sezioni'] if x['titolo']==sz['titolo']),None)
            if tgt is None:
                sz2=dict(sz)
                if 'righe' in sz2: sz2['righe']=[dict(r,valore=rem(r['valore'])) for r in sz2['righe'] if r['etichetta']!='Altro consorzio' and not ph(r['valore'])]
                if 'nota' in sz2: sz2['nota']=rem(sz2['nota'])
                if 'vini' in sz2: sz2['vini']=[dict(x,annata=rem(x['annata'])) for x in sz2['vini']]
                if sz2.get('righe') or sz2.get('vini'): P['sezioni'].append(sz2)
                continue
            for r in sz.get('righe',[]):
                et=r['etichetta']
                if et=='Altro consorzio': continue
                val=rem(r['valore'])
                rows=tgt.setdefault('righe',[])
                if et=='Consorzio':
                    if not any(x['etichetta']=='Consorzio' and re.sub(r'\[\[\d+\]\]','',x['valore'])==re.sub(r'\[\[\d+\]\]','',val) for x in rows): rows.append(dict(r,valore=val))
                    continue
                ex=next((x for x in rows if x['etichetta']==et),None)
                if et.lower().startswith('sede') or et.lower().startswith('indirizzo'):
                    if any(x['etichetta'].lower().startswith(('sede','indirizzo')) for x in rows):
                        a=reg_scheda(prim)[0];b=_reg_from_sede('Sede | '+re.sub(r'\[\[\d+\]\]','',val).split(';')[0]+' [x]')
                        nz=lambda t:re.sub(r'[^a-z0-9]','',re.sub(r'\[\[\d+\]\]','',t.lower()))
                        if b and a and a!=b and not any(x['etichetta'].lower().startswith('altra sede') and nz(x['valore'])[:40]==nz(val)[:40] for x in rows) and not any(x['etichetta'].lower().startswith('altre sedi') and re.sub(r'\D','',val)[:5] in re.sub(r'\D','',x['valore']) for x in rows): rows.append(dict(etichetta='Altra sede (da altro elenco)',valore=val))
                        continue
                if ex is None and ph(val): continue
                if ex is None: rows.append(dict(r,valore=val))
                elif ph(ex['etichetta']+' | '+ex['valore']) or ph(ex['valore']):
                    if not ph(val): ex.update(dict(r,valore=val))
            if 'nota' in sz:
                n=rem(sz['nota'])
                if 'nota' not in tgt: tgt['nota']=n
                elif re.sub(r'\[\[\d+\]\]','',n) not in re.sub(r'\[\[\d+\]\]','',tgt['nota']): tgt['nota']+=' '+n
            if 'vini' in sz:
                have={(x['nome'].lower(),x['denominazione'].lower()) for x in tgt.setdefault('vini',[])}
                names={x['nome'].lower() for x in tgt['vini'] if 'non indicata' not in x['denominazione']}
                for x in sz['vini']:
                    k=(x['nome'].lower(),x['denominazione'].lower())
                    if k in have: continue
                    if 'non indicata' in x['denominazione'] and x['nome'].lower() in names: continue
                    tgt['vini'].append(dict(x,annata=rem(x['annata'])));have.add(k)
                tgt['tipo']='vini'
    if any(x.startswith('cantine-sgarzi') for x in v):
        an=next(x for x in P['sezioni'] if x['titolo']=='Anagrafica')
        n=len(fonti)+1
        fonti.append(dict(n=n,testo='Sito ufficiale della cantina, home; indirizzo riportato dal curatore della guida dal sito, consultato il 26 ottobre 2026.',url='https://cantinesgarzi.com/',etichetta='cantinesgarzi.com'))
        an['righe']=[r for r in an['righe'] if not r['etichetta'].lower().startswith('sede')]
        an['righe'].insert(0,dict(etichetta='Sede',valore='Via Bernarda 1650, 40024 Castel San Pietro Terme (BO) [[%d]]'%n))
        if not any(r['etichetta']=='Sito ufficiale' for r in an['righe']): an['righe'].append(dict(etichetta='Sito ufficiale',valore='{{https://cantinesgarzi.com/|cantinesgarzi.com}} [[%d]]'%n))
    P['consultate']=' '.join(consultate)
    # il Consorzio nelle righe: tieni tutte
    base=strip_suffix(prim)
    return prim,base,P
if __name__=='__main__':
    C=comps()
    out=[];slugs=collections.Counter()
    for v in C:
        votes=regione_produttore(v)
        key=next((k for k in FORCE if any(s.startswith(k) for s in v)),None)
        reg=FORCE[key] if key else (votes.most_common(1)[0][0] if votes else None)
        out.append((v,reg))
    print(collections.Counter(r for v,r in out))

TKEY={'Valpolicella':'valpolicella','Soave e Recioto di Soave':'soave','Lessini Durello':'durello','Bardolino':'bardolino','Custoza':'custoza','Prosecco DOC':'prosecco','Colli Euganei':'euganei','Venezia':'venezia','Conegliano Valdobbiadene':'conegliano','Asolo Montello':'asolo','Collio':'collio','Friuli Colli Orientali e Ramandolo':'colli-orientali','Friuli Grave':'friuli-grave','Friuli DOC':'friuli-doc','Colli Berici':'colli-berici','Gambellara':'gambellara','Garda DOC':'garda','Breganze':'breganze','Lugana':'lugana','Gutturnio (Colli Piacentini)':'gutturnio','Delle Venezie':'venezie','Brunello di Montalcino':'brunello','Chianti Classico':'chianti-classico','Bolgheri':'bolgheri','Nobile di Montepulciano':'nobile','Maremma Toscana':'maremma','Chianti Colli Senesi':'colli-senesi','Valdarno di Sopra':'valdarno'}
def applica(dest='/home/claude/annuario/rifusione/out'):
    import shutil
    for d in ('dati','chiarire'):
        shutil.rmtree(dest+'/'+d,ignore_errors=True);os.makedirs(dest+'/'+d)
    C=comps();prod=[];used=set()
    for v in C:
        votes=regione_produttore(v)
        key=next((k for k in FORCE if any(s.startswith(k) for s in v)),None)
        reg=FORCE[key] if key else (votes.most_common(1)[0][0] if votes else None)
        prim,base,P=fondi(v,reg)
        slug=base
        if slug in used or (slug in DATI and slug not in v):
            slug=prim
        k=2
        while slug in used: slug=base+'-'+str(k);k+=1
        used.add(slug)
        P['slug']=slug
        json.dump(P,open(dest+'/dati/'+slug+'.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        # chiarire: unione
        qs=[]
        for s in sorted(v,key=lambda x:(x!=prim,x)):
            p='chiarire_vecchi/'+s+'.txt'
            if os.path.exists(p):
                for l in open(p,encoding='utf-8'):
                    l=l.rstrip('\n')
                    if l and l not in qs: qs.append(l)
        # una sola domanda per titolo
        seen=set();q2=[]
        for l in qs:
            t=l.split(' | ')[0]
            if t in seen: continue
            seen.add(t);q2.append(l)
        if q2: open(dest+'/chiarire/'+slug+'.txt','w',encoding='utf-8').write('\n'.join(q2)+'\n')
        tipi={}
        for s in v:
            c=cerca[s]
            tk=TKEY[c[3]] 
            dd=[x for x in c[4].split(' · ') if x]
            tipi.setdefault(tk,[])
            for x in dd:
                if x not in tipi[tk]: tipi[tk].append(x)
        comune=COMF.get(prim) or cerca[prim][2] or next((cerca[s][2] for s in v if cerca[s][2]),'')
        prod.append(dict(slug=slug,nome=P['nome'],regione=reg,comune=comune,tipi=tipi,membri=sorted(v),primario=prim))
    json.dump(prod,open(dest+'/produttori.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    return prod
if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1]=='applica':
    p=applica();print(len(p),'produttori scritti')
    print(collections.Counter(len(x['membri']) for x in p))
