# Segna l'appartenenza al Consorzio di Tutela dei Vini di Carmignano (elenco "Le aziende" del consorzio, consultato il 30 ottobre 2026).
import json,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
C=json.load(open(R+'/arricchimenti/consorzio_carmignano.json'))
n=0
for x in C['schede']:
    f=R+'/dati/'+x['slug']+'.json'
    d=json.load(open(f,encoding='utf8'))
    if C['consorzio'] in json.dumps(d,ensure_ascii=False): continue
    k=max([y['n'] for y in d['fonti']]+[0])+1
    d['sezioni'][0]['righe'].append({'etichetta':'Consorzio','valore':C['consorzio']+' [['+str(k)+']]'})
    d['fonti'].append({'n':k,'testo':'Elenco delle aziende del Consorzio di Tutela dei Vini di Carmignano, scheda dell’azienda consultata il 30 ottobre 2026.','url':x['url'],'etichetta':C['sito']})
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n+=1
print('consorzio carmignano:',n)
