import json,re,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
G=json.load(open(R+'/arricchimenti/google.json')); n_ok=0; no_sez=0
for slug,o in G['trovate'].items():
    f=f'{R}/dati/{slug}.json'
    if not os.path.exists(f): continue
    d=json.load(open(f,encoding='utf8'))
    io=next((s for s in d['sezioni'] if s['titolo']=='Identità online'),None)
    if io is None:
        io={'titolo':'Identità online','righe':[]}; d['sezioni'].append(io); no_sez+=1
    if any(r['etichetta']=='Google Maps' for r in io['righe']): continue
    n=max([x['n'] for x in d['fonti']]+[0])+1
    d['fonti'].append({'n':n,'testo':f'Scheda «{o["nome"]}» su Google Maps, trovata con ricerca del {G["data"]} (Google Places).','url':o['url'],'etichetta':'maps.google.com'})
    t='{{'+o['url']+'|Mappa}}'
    if o.get('rating') and o.get('n'): t+=f' — valutazione {str(o["rating"]).replace(".",",")} su 5 ({o["n"]:,} recensioni)'.replace(',','.',1) if False else f' — valutazione {str(o["rating"]).replace(".",",")} su 5 ({o["n"]} recensioni)'
    if o.get('stato')=='CLOSED_PERMANENTLY': t+=' — Google la segnala come chiusa definitivamente'
    elif o.get('stato')=='CLOSED_TEMPORARILY': t+=' — Google la segnala come temporaneamente chiusa'
    io['righe'].append({'etichetta':'Google Maps','valore':t+f' [[{n}]]'})
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n_ok+=1
print('google:',n_ok,'sezioni create:',no_sez)
