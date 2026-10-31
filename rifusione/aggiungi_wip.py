# Promuove nel sito le cantine della lista temporanea (wip/schede-wip.csv) che hanno sede, sito e DOC/DOCG confermati.
# Dati: arricchimenti/wip_promossi.json (letti dai siti ufficiali delle cantine, 30 ottobre 2026; Franciacorta: schede del Consorzio e siti, 31 ottobre 2026).
import json,os,re
R=os.path.dirname(os.path.abspath(__file__))+'/..'
os.chdir(R)
N=json.load(open('arricchimenti/wip_promossi.json',encoding='utf-8'))
P=json.load(open('produttori.json',encoding='utf-8'));have={p['slug'] for p in P}
D0='30 ottobre 2026'
n=0
for x in N:
    if x['slug'] in have: continue
    cons=x.get('dati_consorzio')  # sede e contatti dalla scheda del consorzio (fonte 1), il resto dal sito (fonte 2)
    a='[[1]]'; b='[[2]]' if cons else '[[1]]'
    bs=a if x.get('social_consorzio') else b  # social letti dalla scheda del consorzio
    ana=[]
    if x['rag']: ana.append({'etichetta':'Ragione sociale','valore':x['rag']+' '+b})
    if x['piva']: ana.append({'etichetta':'Partita IVA','valore':x['piva']+' '+b})
    ana.append({'etichetta':'Sede','valore':x['sede']+(' [[2]]' if x.get('fonte_sede') else ' '+a)})
    if x['tel']: ana.append({'etichetta':'Telefono','valore':x['tel']+' '+a})
    if x['email']: ana.append({'etichetta':'Email','valore':x['email']+' '+a})
    ana.append({'etichetta':'Sito ufficiale','valore':'{{'+x['sito']+'|'+x['dom']+'}} '+a})
    if cons: ana.append({'etichetta':'Consorzio','valore':x.get('consorzio_nome','Consorzio di tutela DOP Suvereto e Val di Cornia Wine')+' [[1]]'})
    if x.get('elenco_consorzio'): ana.append({'etichetta':'Consorzio','valore':x['consorzio_nome']+' [[2]]'})  # socio del consorzio: solo dall'elenco soci (contatti e dati dal sito)
    sez=[{'titolo':'Anagrafica','righe':ana}]
    if x['den']: sez.append({'titolo':'Vini','righe':[{'etichetta':'Denominazioni dichiarate','valore':x['den']+(' [[%d]]'%((3 if x.get('elenco_consorzio') else 2) if x.get('fonte_den') else 1))}]})
    if x.get('ospitalita'): sez.append({'titolo':'Ospitalità','righe':[{'etichetta':k,'valore':v+' [[1]]'} for k,v in x['ospitalita']]})
    if not x.get('premi_da_verificare'): sez.append({'titolo':'Riconoscimenti','righe':[{'etichetta':'Premi e punteggi','valore':'Non presenti nelle fonti consultate'}]})  # se la scheda del consorzio o il sito citano premi, la sezione si compila a mano
    if x['social']:
        sez.append({'titolo':'Presenza online','righe':[{'etichetta':'Social','valore':'\n'.join(k+' {{'+v+'|'+re.sub(r'^https?://(www\.)?','',v).rstrip('/')+'}}' for k,v in x['social'].items())+' '+bs}]})
    D=x.get('data_consultazione',D0)  # data di consultazione dei dati della scheda, se diversa dal 30 ottobre
    d={'nome':x['nome'],'slug':x['slug'],'sezioni':sez,
       'consultate':'Fonti consultate il '+D+'. Ogni dato della scheda rinvia alla fonte con il numero tra parentesi quadre.',
       'fonti':([{'n':1,'testo':'Elenco delle '+('aziende del '+x['consorzio_nome'] if x.get('consorzio_nome') else 'cantine del Consorzio di tutela DOP Suvereto e Val di Cornia Wine')+', scheda dell’azienda consultata il '+x.get('data_consorzio',D)+'.','url':x['url_consorzio'],'etichetta':x.get('dom_consorzio','suveretowine.com')}] if cons else [])+([{'n':2 if cons else 1,'testo':'Sito ufficiale della cantina, pagine iniziale, contatti e vini consultate il '+D+'.','url':x['sito'],'etichetta':x['dom']}] if (not cons or x['rag'] or x['piva'] or (x['social'] and not x.get('social_consorzio')) or (x['den'] and not cons)) else [])}
    if x.get('elenco_consorzio'):
        d['fonti'].append({'n':2,'testo':'Elenco dei produttori associati al '+x['consorzio_nome']+', consultato il '+x.get('data_consorzio',D)+'.','url':x['url_consorzio'],'etichetta':x['dom_consorzio']})
    if x.get('fonte_sede'):  # indirizzo trovato in una pagina esterna al sito della cantina
        d['fonti'].append({'n':2,'testo':x['fonte_sede']['testo']+' Consultata il 31 ottobre 2026.','url':x['fonte_sede']['url'],'etichetta':x['fonte_sede']['etichetta']})
    if x.get('fonte_den'):  # denominazione confermata da una pagina esterna (vendita online) invece che dal sito della cantina
        d['fonti'].append({'n':3 if x.get('elenco_consorzio') else 2,'testo':x['fonte_den']['testo']+' Consultata il 31 ottobre 2026.','url':x['fonte_den']['url'],'etichetta':x['fonte_den']['etichetta']})
    json.dump(d,open('dati/'+x['slug']+'.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    P.append({'slug':x['slug'],'nome':x['nome'],'regione':x['regione'],'comune':x['comune'],'tipi':x['tipi'],'membri':[x['slug']],'primario':x['slug']})
    n+=1
json.dump(P,open('produttori.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('promosse dalla lista wip:',n)
