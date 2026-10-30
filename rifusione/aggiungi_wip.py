# Promuove nel sito le cantine della lista temporanea (wip/schede-wip.csv) che hanno sede, sito e DOC/DOCG confermati.
# Dati: arricchimenti/wip_promossi.json (letti dai siti ufficiali delle cantine, 30 ottobre 2026).
import json,os,re
R=os.path.dirname(os.path.abspath(__file__))+'/..'
os.chdir(R)
N=json.load(open('arricchimenti/wip_promossi.json',encoding='utf-8'))
P=json.load(open('produttori.json',encoding='utf-8'));have={p['slug'] for p in P}
D='30 ottobre 2026'
n=0
for x in N:
    if x['slug'] in have: continue
    ana=[]
    if x['rag']: ana.append({'etichetta':'Ragione sociale','valore':x['rag']+' [[1]]'})
    if x['piva']: ana.append({'etichetta':'Partita IVA','valore':x['piva']+' [[1]]'})
    ana.append({'etichetta':'Sede','valore':x['sede']+' [[1]]'})
    if x['tel']: ana.append({'etichetta':'Telefono','valore':x['tel']+' [[1]]'})
    if x['email']: ana.append({'etichetta':'Email','valore':x['email']+' [[1]]'})
    ana.append({'etichetta':'Sito ufficiale','valore':'{{'+x['sito']+'|'+x['dom']+'}} [[1]]'})
    sez=[{'titolo':'Anagrafica','righe':ana}]
    if x['den']: sez.append({'titolo':'Vini','righe':[{'etichetta':'Denominazioni dichiarate','valore':x['den']+' [[1]]'}]})
    sez.append({'titolo':'Riconoscimenti','righe':[{'etichetta':'Premi e punteggi','valore':'Non presenti nelle fonti consultate'}]})
    if x['social']:
        sez.append({'titolo':'Presenza online','righe':[{'etichetta':'Social','valore':'\n'.join(k+' {{'+v+'|'+re.sub(r'^https?://(www\.)?','',v).rstrip('/')+'}}' for k,v in x['social'].items())+' [[1]]'}]})
    d={'nome':x['nome'],'slug':x['slug'],'sezioni':sez,
       'consultate':'Fonti consultate il '+D+'. Ogni dato della scheda rinvia alla fonte con il numero tra parentesi quadre.',
       'fonti':[{'n':1,'testo':'Sito ufficiale della cantina, pagine iniziale, contatti e vini consultate il '+D+'.','url':x['sito'],'etichetta':x['dom']}]}
    json.dump(d,open('dati/'+x['slug']+'.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    P.append({'slug':x['slug'],'nome':x['nome'],'regione':x['regione'],'comune':x['comune'],'tipi':x['tipi'],'membri':[x['slug']],'primario':x['slug']})
    n+=1
json.dump(P,open('produttori.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('promosse dalla lista wip:',n)
