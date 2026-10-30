import json,re,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
W=json.load(open(R+'/arricchimenti/wikipedia.json')); n_ok=0
for slug,o in W['trovate'].items():
    f=f'{R}/dati/{slug}.json'
    if not os.path.exists(f): continue
    d=json.load(open(f,encoding='utf8'))
    io=next((s for s in d['sezioni'] if s['titolo']=='Identità online'),None)
    if io is None or any(r['etichetta']=='Wikipedia' for r in io['righe']): continue
    n=max([x['n'] for x in d['fonti']]+[0])+1
    d['fonti'].append({'n':n,'testo':f'Voce «{o["titolo"]}» su Wikipedia in italiano, trovata con ricerca del {W["data"]}.','url':o['url'],'etichetta':'it.wikipedia.org'})
    io['righe'].append({'etichetta':'Wikipedia','valore':'{{'+o['url']+'|'+o['titolo'].replace('|','')+'}} [['+str(n)+']]'})
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n_ok+=1
print('wikipedia:',n_ok)
