import json,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
V=json.load(open(R+'/arricchimenti/vivino_presenza.json')); VIV=set(x['slug'] for x in json.load(open(R+'/vivino-nuovi.json')))
slugs=set(V['trovate'])|set(V.get('trovate_ricerca',{}))|VIV
n_ok=0
for slug in sorted(slugs):
    f=f'{R}/dati/{slug}.json'
    if not os.path.exists(f): continue
    d=json.load(open(f,encoding='utf8'))
    io=next((s for s in d['sezioni'] if s['titolo']=='Identità online'),None)
    if io is None: io={'titolo':'Identità online','righe':[]}; d['sezioni'].append(io)
    if any(r['etichetta']=='Vivino' for r in io['righe']): continue
    n=max([x['n'] for x in d['fonti']]+[0])+1
    d['fonti'].append({'n':n,'testo':'Vivino (sito di terzi): la cantina compare tra i produttori; corrispondenza per nome del produttore, verificata il 29 ottobre 2026.'})
    io['righe'].append({'etichetta':'Vivino','valore':f'Presente come produttore [[{n}]]'})
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n_ok+=1
print('vivino presenza:',n_ok)
