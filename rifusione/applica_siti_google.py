import json,re,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
S=json.load(open(R+'/arricchimenti/siti_google.json')); G=json.load(open(R+'/arricchimenti/google.json'))
n_ok=0
for slug,o in S.items():
    f=f'{R}/dati/{slug}.json'
    if not os.path.exists(f): continue
    d=json.load(open(f,encoding='utf8'))
    ana=next(s for s in d['sezioni'] if s['titolo']=='Anagrafica')['righe']
    if any(r['etichetta'].startswith('Sito') and re.search(r'\{\{',r['valore']) for r in ana): continue
    g=G['trovate'].get(slug)
    n=max([x['n'] for x in d['fonti']]+[0])+1
    d['fonti'].append({'n':n,'testo':f'Sito indicato nella scheda Google Maps della cantina, ricerca del {G["data"]}.','url':(g or {}).get('url',''),'etichetta':'maps.google.com'})
    host=re.sub(r'^https?://(www\.)?','',o['url']).rstrip('/').split('/')[0]
    pos=next((i+1 for i,r in enumerate(ana) if r['etichetta']=='Contatti'),min(len(ana),2))
    ana.insert(pos,{'etichetta':'Sito ufficiale','valore':'{{'+o['url']+'|'+host+'}} [['+str(n)+']]'})
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n_ok+=1
print('siti google:',n_ok)
