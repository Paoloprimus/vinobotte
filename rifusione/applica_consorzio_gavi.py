# Segna l'appartenenza al Consorzio Tutela Vini d'Acqui (elenco delle aziende, consultato il 2 novembre 2026).
import json,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
C=json.load(open(R+'/arricchimenti/consorzio_gavi.json'))
PP=json.load(open(R+'/produttori.json',encoding='utf8'));ix={p['slug']:p for p in PP}
n=0
for x in C['schede']:
    t=ix[x['slug']]['tipi'].setdefault('gavi',[])
    if 'Gavi' not in t: t.append('Gavi')
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
print('consorzio gavi:',n)
json.dump(PP,open(R+'/produttori.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
