import json,re,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
D=json.load(open(R+'/arricchimenti/piva_b13.json')); n_ok=0
for slug,o in D.items():
    f=f'{R}/dati/{slug}.json'
    if not os.path.exists(f): continue
    d=json.load(open(f,encoding='utf8'))
    ana=next(s for s in d['sezioni'] if s['titolo']=='Anagrafica')['righe']
    if any(re.search(r'\b\d{11}\b',r['valore']) for s in d['sezioni'] for r in s.get('righe',[]) if r['etichetta'] in('P.IVA','Partita IVA','Ragione sociale e P.IVA','Ragione sociale')): continue
    n=max([x['n'] for x in d['fonti']]+[0])+1
    host=re.sub(r'^https?://(www\.)?','',o['url']).split('/')[0]
    d['fonti'].append({'n':n,'testo':'Sito ufficiale della cantina, piè di pagina o note legali, consultato il 29 ottobre 2026.','url':o['url'],'etichetta':host})
    pos=next((i+1 for i,r in enumerate(ana) if r['etichetta'].startswith('Ragione sociale')),min(len(ana),2))
    ana.insert(pos,{'etichetta':'P.IVA','valore':f'{o["piva"]} [[{n}]]'})
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n_ok+=1
print('piva b13:',n_ok)
