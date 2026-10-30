import sys,re,csv
D=sys.argv[1]
t=open(f'/home/claude/testi/testi_{D}.txt',encoding='utf-8').read()
pag=[(m.group(1),m.group(2)) for m in re.finditer(r'^===== (\S+)\n(.*?)(?=^===== |\Z)',t,re.S|re.M)]
rows=list(csv.DictReader(open('/home/claude/out/elenco_consorzio_pulito.csv',encoding='utf-8-sig'),delimiter=';'))
for r in rows:
    if r['dominio'].replace('www.','')==D: print('CONSORZIO:',r['nome'],'|',r['via'],r['cap'],r['comune'],r['provincia'],'|',r['stato'],r['nota']);break
print('PAGINE',len(pag),sum(len(p) for _,p in pag)//1000,'KB')
base=re.compile(r'https?://[^/]+')
for u,p in pag:
    pth=re.sub(r'^https?://[^/]+','',u)
    if re.match(r'/(en|de|fr|es|ru|zh|us)/',pth) or '/page/' in pth or 'cookie' in pth or 'privacy' in pth: continue
    print(' ',pth[:60],'|',p.strip()[:45].replace('\n',' '),'|',len(p))
allt='\n'.join(p for _,p in pag)
def ctx(pat,n=3,w=80):
    seen=[];
    for m in re.finditer(pat,allt,re.I):
        s=allt[max(0,m.start()-w):m.end()+w].replace('\n',' ')
        if not any(s[:50] in x for x in seen): seen.append(s)
        if len(seen)>=n:break
    return seen
for lab,pat,n in [('PIVA',r'(p\.?\s?iva|partita iva|vat)[^0-9]{0,15}\d{11}',2),('TEL',r'(\+39|tel\.?|phone)[\s:]*[\d ./]{8,}',2),('MAIL',r'[\w.-]+@[\w.-]+\.\w+',2),
 ('ETTARI',r'\d+[.,]?\d*\s*(ettari|hectares|ha\b)',4),('ANNO',r'(dal|nel|since|fondata|founded|nata|nasce)\s+(il\s+)?(18|19|20)\d\d',3),
 ('ORARI',r'(lun|mon)[a-zì]*\s*[-–/]\s*(ven|fri|sab|sat|dom|sun)[^.]{0,80}',3),('PREZZI',r'(€\s?\d+|\d+\s?€|\d+\s?euro)',5),
 ('PRENOT',r'(prenota|booking|book |su appuntamento|by appointment)',2),('BIO',r'(biologic|organic|SQNPI|biodynamic|biodinamic|vegan|certificaz|certified)',3),
 ('PREMI',r'(gambero rosso|tre bicchieri|veronelli|james suckling|decanter|wine spectator|ais |slow wine|medagli|punti|points|parker|wine enthusiast|luca maroni)',4),
 ('SHOP',r'(carrello|add to cart|aggiungi al carrello|shop online|e-?commerce|acquista)',2),
 ('SOCIAL',r'(instagram|facebook|youtube|tripadvisor)\.com/[\w./-]+',3)]:
    for s in ctx(pat,n): print(f'[{lab}]',s)
