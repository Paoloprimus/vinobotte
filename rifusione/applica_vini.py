import json,re,os,glob
R=os.path.dirname(os.path.abspath(__file__))+'/..'
tot=dict(applicate=0,assenti=0)
for fn in sorted(glob.glob(R+'/arricchimenti/vini_sito_*.json')):
    DATA='29 ottobre 2026'
    for slug,o in json.load(open(fn,encoding='utf8')).items():
        f=f'{R}/dati/{slug}.json'
        if not os.path.exists(f): tot['assenti']+=1; continue
        d=json.load(open(f,encoding='utf8'))
        url=o['url']; host=re.sub(r'^https?://(www\.)?','',url).split('/')[0]
        fo=next((x for x in d['fonti'] if x.get('url')==url and 'prodotti' in x.get('testo','')),None)
        if fo is None:
            n=max([x['n'] for x in d['fonti']]+[0])+1
            fo={'n':n,'testo':'Sito ufficiale della cantina, pagine dei vini e dei prodotti, consultato il %s.'%DATA,'url':url,'etichetta':host}
            d['fonti'].append(fo)
        voci=o['vini']
        sv=next((s for s in d['sezioni'] if s['titolo']=='Vini'),None)
        if sv is None:
            sv={'titolo':'Vini','righe':[]}; d['sezioni'].insert(2,sv)
        riga={'etichetta':'Elenco vini','valore':'Denominazioni DOC e DOCG indicate sul sito ufficiale: '+'; '.join(voci)+' [[%d]]'%fo['n']}
        i=next((k for k,r in enumerate(sv['righe']) if r['etichetta'].startswith('Elenco vini')),None)
        if i is None: sv['righe'].insert(0,riga)
        else: sv['righe'][i]=riga
        json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1)
        tot['applicate']+=1
print('vini sito:',tot)
