import json,re,sys
KEEP=re.compile(r'^(Amarone|Recioto|Valpolicella|Soave|Lugana|Bardolino|Chiaretto|Prosecco|Durello|Custoza|Bianco di Custoza|Garda|Lessini|Lison|Colli|Arcole|Gambellara|Montello|Asolo|Conegliano|Valdobbiadene|Breganze|Merlara|Monti Lessini|Pinot Grigio delle Venezie|Delle Venezie|Venezia)\b',re.I)
def ok(den):
    if re.search(r'\bIG[TP]\b',den,re.I): return False
    return bool(re.search(r'\bDOC[G]?\b|\bDOP\b',den)) or bool(KEEP.match(den.strip()))
NOTA=' Solo vini a denominazione DOC/DOCG; esclusi IGT, vini senza denominazione e distillati.'
slugs=sys.argv[1:]
rem=[];vuoti=[]
for s in slugs:
    p=f'dati/{s}.json';d=json.load(open(p,encoding='utf-8'));ch=False
    for z in d['sezioni']:
        if 'vini' not in z: continue
        keep=[]
        for v in z['vini']:
            if ok(v.get('denominazione','')): keep.append(v)
            else: rem.append((s,v['nome'],v.get('denominazione',''))); ch=True
        z['vini']=keep
        if ch and 'DOC/DOCG' not in z.get('nota',''):
            z['nota']=(z.get('nota','').rstrip()+NOTA).strip()
        if not keep: vuoti.append(s)
    if ch: json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
open('vini-rimossi.csv','w',encoding='utf-8-sig').write('cantina;vino;denominazione\n'+'\n'.join(';'.join(r) for r in rem))
print(len(rem),'righe tolte;',len(vuoti),'schede senza vini:',vuoti[:30])
