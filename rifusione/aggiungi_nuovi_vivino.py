# Schede essenziali per produttori toscani trovati su Vivino (zona = denominazione), letti dal sito ufficiale. Da vivino-nuovi.json.
import json,os
os.chdir('/home/claude/annuario')
N=json.load(open('vivino-nuovi.json',encoding='utf-8'))
P=json.load(open('produttori.json',encoding='utf-8'));have={p['slug'] for p in P}
D='26 ottobre 2026'
for x in N:
    if x['slug'] in have: continue
    ana=[{'etichetta':'Sede','valore':x['sede']+' [[1]]'}] if x['sede'] else []
    if x['tel']: ana.append({'etichetta':'Contatti','valore':(x.get('contatti') or 'Tel. '+x['tel'])+' [[1]]'})
    if x['rag']: ana.append({'etichetta':'Ragione sociale e P.IVA','valore':x['rag']+' [[1]]'})
    ana.append({'etichetta':'Sito ufficiale','valore':'{{'+x['sito']+'|'+x['dom']+'}} [[1]]'})
    if x.get('elenco'): ana.append({'etichetta':'Presenza in elenchi','valore':x['elenco']})
    sez=[{'titolo':'Anagrafica','righe':ana}]
    if x['storia']: sez.append({'titolo':'Azienda: proprietà e struttura','righe':[{'etichetta':'Storia e proprietà','valore':x['storia']+' [[1]]'}]})
    vr=[]
    if x.get('dich'): vr.append({'etichetta':'Denominazioni dichiarate','valore':x['dich']})
    if x['den']: vr.append({'etichetta':'Denominazioni citate sul sito ufficiale','valore':x['den']+' [[1]]'})
    if vr: sez.append({'titolo':'Vini','righe':vr})
    sez+=[{'titolo':'Riconoscimenti','righe':[{'etichetta':'Premi e punteggi','valore':'Non presenti nelle fonti consultate'}]},
      {'titolo':'Identità online','righe':[{'etichetta':'Negozi online e marketplace','valore':'Presenza non verificata'},{'etichetta':'Piattaforme','valore':'Google Business Profile, Vivino, Wine-Searcher, YouTube, Wikipedia: presenza non verificata'}]}]
    d={'nome':x['nome'],'slug':x['slug'],'sezioni':sez,
       'consultate':('Sito ufficiale della cantina e scheda nell’archivio di Bere il Vino, consultati il ' if x.get('fonte2') else 'Sito ufficiale della cantina, consultato il ')+D+'. Ogni dato della scheda rinvia alla fonte con il numero tra parentesi quadre.',
       'fonti':[{'n':1,'testo':'Sito ufficiale della cantina, pagine iniziale e di contatto consultate il '+D+'.','url':x['sito'],'etichetta':x['dom']}]+([x['fonte2']] if x.get('fonte2') else [])}
    json.dump(d,open('dati/'+x['slug']+'.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    P.append({'slug':x['slug'],'nome':x['nome'],'regione':'Toscana','comune':x['comune'],'tipi':x['tipi'],'membri':[x['slug']],'primario':x['slug']})
json.dump(P,open('produttori.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('nuovi vivino',len(N))
