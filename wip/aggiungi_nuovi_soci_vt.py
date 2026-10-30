# Schede essenziali per i soci del Consorzio Vino Toscana che producono vini DOC/DOCG. Da soci-vt-nuovi.json.
import json,os
os.chdir('/home/claude/annuario')
N=json.load(open('soci-vt-nuovi.json',encoding='utf-8'))
P=json.load(open('produttori.json',encoding='utf-8'));have={p['slug'] for p in P}
D='29 ottobre 2026'
for x in N:
    if x['slug'] in have: continue
    ana=[{'etichetta':'Sito ufficiale','valore':'{{'+x['sito']+'|'+x['dom']+'}} [[1]]'},
         {'etichetta':'Consorzio','valore':'Consorzio Vino Toscana [[2]]'}]
    sez=[{'titolo':'Anagrafica','righe':ana},
         {'titolo':'Vini','righe':[{'etichetta':'Denominazioni citate sul sito ufficiale','valore':x['den']+' [[1]]'}]},
         {'titolo':'Riconoscimenti','righe':[{'etichetta':'Premi e punteggi','valore':'Non presenti nelle fonti consultate'}]},
         {'titolo':'Identità online','righe':[{'etichetta':'Negozi online e marketplace','valore':'Presenza non verificata'},{'etichetta':'Piattaforme','valore':'Google Business Profile, Vivino, Wine-Searcher, YouTube, Wikipedia: presenza non verificata'}]},
         {'titolo':'Stato della scheda','righe':[{'etichetta':'Da completare','valore':'Scheda essenziale: i dati completi dell’azienda (sede, contatti, storia, vini, riconoscimenti) vanno ancora aggiunti.'}]}]
    d={'nome':x['nome'],'slug':x['slug'],'sezioni':sez,
       'consultate':'Sito ufficiale della cantina e elenco dei soci del Consorzio Vino Toscana, consultati il '+D+'. Ogni dato della scheda rinvia alla fonte con il numero tra parentesi quadre.',
       'fonti':[{'n':1,'testo':'Sito ufficiale della cantina, consultato il '+D+'.','url':x['sito'],'etichetta':x['dom']},
                {'n':2,'testo':'Elenco dei soci del Consorzio Vino Toscana, consultato il '+D+'.','url':'https://www.consorziovinotoscana.it/soci/','etichetta':'consorziovinotoscana.it'}]}
    json.dump(d,open('dati/'+x['slug']+'.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    P.append({'slug':x['slug'],'nome':x['nome'],'regione':'Toscana','comune':'','tipi':x['tipi'],'membri':[x['slug']],'primario':x['slug']})
json.dump(P,open('produttori.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('nuovi soci vt',len(N))
