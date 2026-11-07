import json,re,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
em=json.load(open(R+'/arricchimenti/email.json'))
DATA='7 novembre 2026'
tot=dict(email=0,assenza=0,senzasito=0,irragg=0,gia=0,assenti=0)
for slug,o in em.items():
    f=f'{R}/dati/{slug}.json'
    if not os.path.exists(f): tot['assenti']+=1; continue
    d=json.load(open(f,encoding='utf8'))
    an=next((s for s in d['sezioni'] if s['titolo']=='Anagrafica'),None)
    ASSENZA='Non presente nelle pagine del sito ufficiale consultate'
    esist=[(s,r) for s in d['sezioni'] for r in s.get('righe',[]) if r['etichetta'].startswith('Email')]
    if an is None or (esist and not (o['email'] and all(r['valore'].startswith(ASSENZA) for s,r in esist))):
        tot['gia']+=1; continue
    for s,r in esist: s['righe'].remove(r)
    if o['email']:
        n=max([x['n'] for x in d.get('fonti',[])]+[0])+1
        pag=o['pagina']
        if o.get('fonte'): d.setdefault('fonti',[]).append(dict({'n':n,'testo':o['fonte']},**({'url':o['url'],'etichetta':re.sub(r'^https?://(www\.)?([^/]+).*',r'\2',o['url'])} if o.get('url') else {})))
        else: d.setdefault('fonti',[]).append({'n':n,'testo':f'Sito ufficiale della cantina, pagina «{re.sub(r"^https?://(www\.)?","",pag).rstrip("/")}», consultata il {DATA}.','url':pag,'etichetta':re.sub(r'^https?://(www\.)?([^/]+).*',r'\2',pag)})
        riga={'etichetta':'Email','valore':f'{o["email"]} [[{n}]]'}; tot['email']+=1
    elif o.get('motivo')=='senza-sito':
        riga={'etichetta':'Email','valore':f'Assenza di sito ufficiale, nessuna email individuata (controllo del {DATA})'}; tot['senzasito']+=1
    elif o.get('motivo')=='irraggiungibile':
        riga={'etichetta':'Email','valore':f'Sito ufficiale irraggiungibile, nessuna email individuata (controllo del {DATA})'}; tot['irragg']+=1
    else:
        riga={'etichetta':'Email','valore':f'Non presente nelle pagine del sito ufficiale consultate (controllo del {DATA})'}; tot['assenza']+=1
    righe=an['righe']; pos=len(righe)
    for i,r in enumerate(righe):
        if r['etichetta'].startswith('Telefono'): pos=i+1; break
    else:
        for i,r in enumerate(righe):
            if r['etichetta'].startswith('Sede'): pos=i+1; break
    righe.insert(pos,riga)
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('email:',tot)
