# Completa le schede Bolgheri con dati letti sui siti (arricchimenti/bolgheri_completa.json).
import json,os,re
os.chdir('/home/claude/annuario')
C=json.load(open('arricchimenti/bolgheri_completa.json',encoding='utf8'))
P=json.load(open('produttori.json',encoding='utf8'));ix={p['slug']:p for p in P}
ORD=['Ragione sociale','Partita IVA','Sede','Telefono','Email','Sito ufficiale','Consorzio','Consorzi']
n=0
for slug,x in C['schede'].items():
    f='dati/'+slug+'.json'
    d=json.load(open(f,encoding='utf8'))
    k=max([y['n'] for y in d['fonti']]+[0])+1
    d['fonti'].append({'n':k,'testo':x['fonte'],'url':x.get('sito') or x.get('url'),'etichetta':(x.get('dom') or re.sub(r'^https?://(www\.)?|/$','',x.get('url','')))})
    sec=d['sezioni'][0]; rows={r['etichetta']:r for r in sec['righe']}
    def put(lab,val):
        rows[lab]={'etichetta':lab,'valore':val+' [['+str(k)+']]'}
    if 'rag' in x: put('Ragione sociale',x['rag'])
    if 'piva' in x: put('Partita IVA',x['piva'])
    if 'sede' in x: put('Sede',x['sede'])
    if 'tel' in x: put('Telefono',x['tel'])
    if 'email' in x: put('Email',x['email'])
    if 'sito' in x: put('Sito ufficiale','{{'+x['sito']+'|'+x['dom']+'}}')
    sec['righe']=[rows[l] for l in ORD if l in rows]+[r for l,r in rows.items() if l not in ORD]
    if 'vini' in x:
        for s in d['sezioni']:
            for r in s.get('righe') or []:
                if r['etichetta']=='Elenco vini': r['valore']='Denominazioni DOC e DOCG: '+x['vini']+' ['+'['+str(k)+']]'
    for s_ in d['sezioni']:
        for r in s_['righe']: r['valore']=re.sub(r'(\[\[\d+\]\]) \1',r'\1',r['valore'])
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1)
    if slug in ix and x.get('comune'): ix[slug]['comune']=x['comune']
    n+=1
json.dump(P,open('produttori.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
print('bolgheri completate:',n)
