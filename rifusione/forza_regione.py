# Sposta in una regione diversa dalla sede legale le schede decise a mano (arricchimenti/regione_forzata.json).
import json,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
F=json.load(open(R+'/arricchimenti/regione_forzata.json',encoding='utf8'))
P=json.load(open(R+'/produttori.json',encoding='utf8'));n=0
for p in P:
    if p['slug'] in F and p['regione']!=F[p['slug']]['regione']: p['regione']=F[p['slug']]['regione'];n+=1
json.dump(P,open(R+'/produttori.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
print('regione forzata:',n)
