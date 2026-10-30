# Aggiunge tipi (tile) a produttori esistenti, da tile_extra.tsv (slug \t tipo \t denominazione).
import json,os
os.chdir('/home/claude/annuario')
P=json.load(open('produttori.json',encoding='utf-8'));ix={p['slug']:p for p in P}
n=0
for l in open('tile_extra.tsv',encoding='utf-8'):
    l=l.rstrip('\n')
    if not l: continue
    s,t,d=l.split('\t');p=ix[s]
    if d not in p['tipi'].setdefault(t,[]): p['tipi'][t].append(d);n+=1
json.dump(P,open('produttori.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('tile aggiunti',n)
