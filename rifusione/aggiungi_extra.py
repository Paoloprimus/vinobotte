# Aggiunge le schede extra (Bere il Vino Toscana) a dati/, chiarire/, produttori.json dopo la rifusione.
import json,os,shutil
os.chdir('/home/claude/annuario')
B='bere-tosc/out/'
if os.path.exists(B+'produttori_extra.json'):
    for f in os.listdir(B+'dati'): shutil.copy(B+'dati/'+f,'dati/'+f)
    for f in os.listdir(B+'chiarire'): shutil.copy(B+'chiarire/'+f,'chiarire/'+f)
    P=json.load(open('produttori.json',encoding='utf-8'));ex=json.load(open(B+'produttori_extra.json',encoding='utf-8'))
    have={p['slug'] for p in P}
    P+= [p for p in ex if p['slug'] not in have]
    json.dump(P,open('produttori.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    print('extra aggiunte',len(ex))
