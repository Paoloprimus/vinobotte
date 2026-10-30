# Segna l'appartenenza al Consorzio Vino Chianti (elenco aziende del consorzio, consultato il 29 ottobre 2026).
import json,os,re
R=os.path.dirname(os.path.abspath(__file__))+'/..'
M=json.load(open(R+'/arricchimenti/consorzio_chianti.json'))
n=0
for slug,url in M.items():
    f=R+'/dati/'+slug+'.json'
    d=json.load(open(f,encoding='utf8'))
    if re.search(r'Consorzio Vino Chianti(?! Classico)',json.dumps(d,ensure_ascii=False)): continue
    k=max([x['n'] for x in d['fonti']]+[0])+1
    ana=d['sezioni'][0]
    assert ana['titolo']=='Anagrafica'
    ana['righe'].append({'etichetta':'Consorzio','valore':'Consorzio Vino Chianti [['+str(k)+']]'})
    d['fonti'].append({'n':k,'testo':'Elenco delle aziende del Consorzio Vino Chianti, scheda dell’azienda consultata il 29 ottobre 2026.','url':url,'etichetta':'consorziovinochianti.it'})
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n+=1
print('consorzio chianti:',n)
