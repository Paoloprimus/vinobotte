# Segna l'appartenenza a un consorzio di tutela (elenco soci consultato il 2 novembre 2026) sulle schede già in guida.
# Dati: arricchimenti/consorzi_gen.json = [{key, consorzio, sito, data, den, schede:[{slug,url}]}]. Vale per tutti i consorzi del «primo giro».
import json,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
CG=json.load(open(R+'/arricchimenti/consorzi_gen.json',encoding='utf8'))
PP=json.load(open(R+'/produttori.json',encoding='utf8'));ix={p['slug']:p for p in PP}
n=0;mancanti=0
for C in CG:
    for x in C['schede']:
        if x['slug'] not in ix or not os.path.exists(R+'/dati/'+x['slug']+'.json'): mancanti+=1; continue
        t=ix[x['slug']]['tipi'].setdefault(C['key'],[])
        if not t: t.append(C['den'])
        f=R+'/dati/'+x['slug']+'.json'
        d=json.load(open(f,encoding='utf8'))
        if C['consorzio'] in json.dumps(d,ensure_ascii=False): continue
        k=max([y['n'] for y in d['fonti']]+[0])+1
        riga=C['consorzio']+' [['+str(k)+']]'
        for s in d['sezioni']:
            for r in s.get('righe') or []:
                if r['etichetta'] in ('Consorzio','Consorzi'):
                    r['valore']=r['valore']+'\n'+riga; r['etichetta']='Consorzi'; riga=None; break
            if riga is None: break
        if riga: d['sezioni'][0]['righe'].append({'etichetta':'Consorzio','valore':riga})
        d['fonti'].append({'n':k,'testo':'Elenco dei produttori del '+C['consorzio']+', consultato il '+C['data']+'.','url':x['url'],'etichetta':C['sito']})
        json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n+=1
print('consorzi (primo giro):',n,'righe aggiunte, schede non trovate:',mancanti)
json.dump(PP,open(R+'/produttori.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
