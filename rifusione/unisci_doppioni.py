# Unisce le schede doppie (stessa azienda, stesso sito e stessa sede): tiene la scheda più ricca (keep),
# aggiunge i riquadri (tipi) e le righe Consorzio dell'altra (drop) e la elimina. Elenco in arricchimenti/doppioni.json.
import json,os,re
os.chdir('/home/claude/annuario')
C=json.load(open('arricchimenti/doppioni.json',encoding='utf8'))
P=json.load(open('produttori.json',encoding='utf8'));ix={p['slug']:p for p in P}
CONS=('Consorzio','Consorzi')
def cons(d):
    for s in d['sezioni']:
        for r in s.get('righe') or []:
            if r['etichetta'] in CONS: return s,r
    return None,None
drop_set=set()
for keep,drop,*nm in C['coppie']:
    if keep not in ix or drop not in ix: continue
    K,D=ix[keep],ix[drop]
    for g,l in D['tipi'].items():
        K['tipi'].setdefault(g,[])
        for x in l:
            if x not in K['tipi'][g]: K['tipi'][g].append(x)
    K['membri']=list(dict.fromkeys(K.get('membri',[])+D.get('membri',[])))
    if not K.get('comune') and D.get('comune'): K['comune']=D['comune']
    dk=json.load(open('dati/'+keep+'.json',encoding='utf8'));dd=json.load(open('dati/'+drop+'.json',encoding='utf8'))
    sk,rk=cons(dk);sd,rd=cons(dd)
    if rd:
        nuove=[l for l in rd['valore'].split('\n') if re.sub(r'\s*\[\[\d+\]\]','',l) not in (rk['valore'] if rk else '')]
        if nuove:
            off=max([f['n'] for f in dk['fonti']]+[0]); 
            ref=lambda t:re.sub(r'\[\[(\d+)\]\]',lambda m:'[['+str(int(m.group(1))+off)+']]',t)
            usate={int(n) for l in nuove for n in re.findall(r'\[\[(\d+)\]\]',l)}
            for f in dd['fonti']:
                if f['n'] in usate: dk['fonti'].append(dict(f,n=f['n']+off))
            txt='\n'.join(ref(l) for l in nuove)
            if rk: rk['valore']=rk['valore']+'\n'+txt; rk['etichetta']='Consorzi'
            else: dk['sezioni'][0]['righe'].append({'etichetta':'Consorzio' if len(nuove)==1 else 'Consorzi','valore':txt})
            json.dump(dk,open('dati/'+keep+'.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
    if drop in C.get('porta_contenuto',[]):
        # porta nella scheda tenuta le righe 'Azienda' e 'Riconoscimenti' della doppia (con le fonti), al posto di quelle vuote
        off=max([f['n'] for f in dk['fonti']]+[0]); usate=set()
        ref=lambda t:re.sub(r'\[\[(\d+)\]\]',lambda m:'[['+str(int(m.group(1))+off)+']]',t)
        for tit_d,tit_k in (('Azienda','Azienda'),('Riconoscimenti','Riconoscimenti')):
            sd_=next((x for x in dd['sezioni'] if x['titolo']==tit_d),None)
            sk_=next((x for x in dk['sezioni'] if x['titolo'].startswith(tit_k)),None)
            if not sd_ or not sk_ or not sd_.get('righe'): continue
            sk_['righe']=[r for r in sk_.get('righe',[]) if not re.match(r'^(Non disponibil|Non present)',r['valore'])]
            for r in sd_['righe']:
                usate|={int(n) for n in re.findall(r'\[\[(\d+)\]\]',r['valore'])}
                sk_['righe'].append({'etichetta':r['etichetta'],'valore':ref(r['valore'])})
        for f in dd['fonti']:
            if f['n'] in usate: dk['fonti'].append(dict(f,n=f['n']+off))
        json.dump(dk,open('dati/'+keep+'.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
    if nm:
        K['nome']=nm[0]; dk['nome']=nm[0]
        json.dump(dk,open('dati/'+keep+'.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
    drop_set.add(drop)
    if os.path.exists('dati/'+drop+'.json'): os.remove('dati/'+drop+'.json')
P=[p for p in P if p['slug'] not in drop_set]
json.dump(P,open('produttori.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
print('doppioni uniti:',len(drop_set))
