# Crea schede essenziali per produttori Vernaccia (elenco Consorzio) non presenti, da vernaccia-nuovi.json.
import json,os
os.chdir('/home/claude/annuario')
N=json.load(open('vernaccia-nuovi.json',encoding='utf-8'))
P=json.load(open('produttori.json',encoding='utf-8'));have={p['slug'] for p in P}
D='26 ottobre 2026'
for x in N:
    if x['slug'] in have: continue
    ana=[{'etichetta':'Sede','valore':x['sede']+' [['+str(x.get('sede_fonte',1))+']]'}]+([{'etichetta':'Contatti','valore':(x.get('contatti') or 'Tel. '+x['tel'])+' [[1]]'}] if x['tel'] else [])+([{'etichetta':'Ragione sociale e P.IVA','valore':x['rag']+' [[1]]'}] if x['rag'] else [])+([{'etichetta':'Sito ufficiale','valore':'{{'+x['sito']+'|'+x['dom']+'}} [[1]]'}] if x['sito'] else [])+[
         {'etichetta':'Presenza in elenchi','valore':x.get('elenco') or 'Compare nell’elenco dei produttori del Consorzio Tutela Vernaccia di San Gimignano [[2]]'}]
    sez=[{'titolo':'Anagrafica','righe':ana}]
    if x['storia']: sez.append({'titolo':'Azienda: proprietà e struttura','righe':[{'etichetta':'Storia e proprietà','valore':x['storia']+' [[1]]'}]})
    vr=[{'etichetta':'Denominazioni dichiarate','valore':x.get('dich') or 'Vernaccia di San Gimignano DOCG [[2]]'}]
    if x['den']: vr.append({'etichetta':'Denominazioni citate sul sito ufficiale','valore':x['den']+' [[1]]'})
    sez+= [{'titolo':'Vini','righe':vr},
      {'titolo':'Riconoscimenti','righe':[{'etichetta':'Premi e punteggi','valore':'Non presenti nelle fonti consultate'}]},
      {'titolo':'Identità online','righe':[{'etichetta':'Negozi online e marketplace','valore':'Presenza non verificata'},{'etichetta':'Piattaforme','valore':'Google Business Profile, Vivino, Wine-Searcher, YouTube, Wikipedia: presenza non verificata'}]}]
    d={'nome':x['nome'],'slug':x['slug'],'sezioni':sez,
       'consultate':'Sito ufficiale della cantina ed elenco dei produttori del consorzio, consultati il '+D+'. Ogni dato della scheda rinvia alla fonte con il numero tra parentesi quadre.',
       'fonti':[dict({'n':1,'testo':'Sito ufficiale della cantina, pagina iniziale consultata il '+D+'.'},**({'url':x['sito'],'etichetta':x['dom']} if x['sito'] else {})),
                x.get('fonte2') or {'n':2,'testo':'Consorzio Tutela Vernaccia di San Gimignano, elenco dei produttori, consultato il '+D+'.','url':'https://vernaccia.it/produttori/','etichetta':'vernaccia.it'}]}
    json.dump(d,open('dati/'+x['slug']+'.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    P.append({'slug':x['slug'],'nome':x['nome'],'regione':'Toscana','comune':x['comune'],'tipi':x.get('tipi') or {'vernaccia':['Vernaccia di San Gimignano']},'membri':[x['slug']],'primario':x['slug']})
json.dump(P,open('produttori.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('nuovi vernaccia',len(N))
