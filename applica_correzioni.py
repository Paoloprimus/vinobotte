# Correzioni post-generazione sulle schede Valpolicella (da revisione 25 ott 2026). Eseguire UNA volta dopo scheda.py+filtra_vini.py.
import json,re,sys,csv
Q='/home/claude/annuario'
sl=[r[1] for r in json.load(open(f'{Q}/cerca.json')) if r[3]=='Valpolicella']
log=[]
def load(s): return json.load(open(f'{Q}/dati/{s}.json',encoding='utf-8'))
def save(s,d): json.dump(d,open(f'{Q}/dati/{s}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
def vini(d):
    for z in d['sezioni']:
        for v in z.get('vini',[]): yield z,v
# --- 1. sigle denominazione
def sigla(den):
    d=den.strip()
    d=re.sub(r'\s*\((produzione limitata|Corvina[^)]*|Indicazione geografica)\)','',d)
    d=re.sub(r'\bDOP\b','DOC',d)
    if re.search(r'\bDOCG?\b',d): return d
    if re.match(r'Amarone$|Amarone (Classico|Riserva)',d) or d.startswith('Amarone Classico'): d=re.sub(r'^Amarone','Amarone della Valpolicella',d)
    if re.search(r'Amarone|Recioto|Soave Classico Superiore|Soave Superiore|Bardolino Superiore|Franciacorta',d): return d+' DOCG'
    if re.search(r'Valpolicella|Ripasso|Soave|Lugana|Bardolino|Chiaretto|Prosecco|Custoza|Garda|Arcole|Durello|Lessini',d): return d+' DOC'
    return d
for s in sl:
    d=load(s);ch=False
    for z,v in vini(d):
        n=sigla(v['denominazione'])
        if n!=v['denominazione']: log.append((s,'denominazione',v['denominazione'],n));v['denominazione']=n;ch=True
    if ch: save(s,d)
# --- 2. correzioni puntuali
def edit(s,fn):
    d=load(s);fn(d);save(s,d)
def sub_all(d,a,b):
    t=json.dumps(d,ensure_ascii=False).replace(a,b);return json.loads(t)
def rm_vino(d,nome): 
    for z in d['sezioni']:
        if 'vini' in z: z['vini']=[v for v in z['vini'] if v['nome']!=nome]
def setden(d,nome,den):
    for z,v in vini(d):
        if v['nome']==nome: v['denominazione']=den
d=load('fratelli-degani');d=sub_all(d,'+39 045 6895162','+39 045 9780193');save('fratelli-degani',d)
edit('cavalchina',lambda d:(setden(d,'Brolo','Amarone della Valpolicella Riserva DOCG'),setden(d,'Morari','Valpolicella Superiore DOC')))
edit('giarola',lambda d:(rm_vino(d,'Crèar'),rm_vino(d,'L’Umbe Rosso')))
edit('canoso',lambda d:rm_vino(d,'Lento'))
edit('ca-dei-ronchi',lambda d:setden(d,'Magnifico','Amarone della Valpolicella DOCG'))
d=load('meroni');d=sub_all(d,'37010','37015');save('meroni',d)
d=load('tenute-falezza')
for z in d['sezioni']:
    if 'vini' in z: z['nota']=z['nota'].replace('Solo i vini a denominazione Valpolicella e i rossi IGT; la cantina produce anche bianchi, passito e spumante.','Solo i vini a denominazione Valpolicella; la cantina produce anche altri vini.')
save('tenute-falezza',d)
# Delibori: aggiungere Amarone (home del sito)
d=load('cantine-delibori')
n=len(d['fonti'])+1
d['fonti'].append(dict(n=n,testo='Sito ufficiale della cantina, consultato il 25 ottobre 2026, pagina «cantinedelibori.com» (verifica incrociata).',url='https://www.cantinedelibori.com/',etichetta='cantinedelibori.com'))
for z in d['sezioni']:
    if 'vini' in z:
        z['vini'].insert(0,dict(nome='Amarone della Valpolicella',denominazione='Amarone della Valpolicella DOCG',annata=f'— [[{n}]]'))
        z['nota']=z['nota'].replace('i vini in elenco non sono di denominazione Valpolicella.','la home del sito elenca anche l’Amarone della Valpolicella; gli altri vini in elenco non sono di denominazione Valpolicella.')
save('cantine-delibori',d)
# --- 3. fonti non citate: tolte e rinumerate
def cited(d):
    t=json.dumps(d['sezioni'],ensure_ascii=False);return {int(x) for x in re.findall(r'\[\[(\d+)\]\]',t)}
for s in sl:
    d=load(s);c=cited(d);keep=[f for f in d['fonti'] if f['n'] in c]
    if len(keep)==len(d['fonti']): continue
    mp={f['n']:i+1 for i,f in enumerate(keep)}
    t=json.dumps(d['sezioni'],ensure_ascii=False)
    t=re.sub(r'\[\[(\d+)\]\]',lambda m:f'[[{mp[int(m.group(1))]}]]',t)
    d['sezioni']=json.loads(t)
    log.append((s,'fonti tolte',str(sorted(f['n'] for f in d['fonti'] if f['n'] not in c)),''))
    for f in keep: f['n']=mp[f['n']]
    d['fonti']=keep;save(s,d)
# --- 4. P.IVA / contatti
def sito(d):
    for z in d['sezioni']:
        for r in z.get('righe',[]):
            m=re.search(r'\{\{(https?://[^|}]+)',r['valore'])
            if r['etichetta'].startswith('Sito') and m: return m.group(1)
for l in open(f'{Q}/correzioni-contatti.txt',encoding='utf-8'):
    p=[x.strip() for x in l.rstrip('\n').split('|')]
    if len(p)<5: continue
    s,piva,tel,mail,url=p[:5];d=load(s)
    url=url or sito(d)
    if not url: log.append((s,'NESSUN URL','',''));continue
    txt=json.dumps(d,ensure_ascii=False)
    dig=re.sub(r'\D','',piva)
    haspiva=bool(re.search(r'P\.?\s?IVA|Partita IVA',txt))
    haspiva = haspiva
    add=[]
    if piva and not haspiva: add.append(('Partita IVA',piva))
    cont=[]
    if tel and re.sub(r'\D','',tel)[-9:] not in re.sub(r'\D','',txt): cont.append('Tel. '+tel)
    if mail and mail.lower() not in txt.lower(): cont.append(mail)
    if not add and not cont: continue
    f=[x for x in d['fonti'] if x['url']==url]
    if f: n=f[0]['n']
    else:
        n=len(d['fonti'])+1;dom=re.sub(r'^https?://(www\.)?','',url).split('/')[0]
        d['fonti'].append(dict(n=n,testo='Sito ufficiale della cantina, consultato il 25 ottobre 2026, pagina «'+re.sub(r'^https?://(www\.)?','',url).rstrip('/')+'» (verifica incrociata).',url=url,etichetta=dom))
    an=[z for z in d['sezioni'] if z['titolo'] in('Anagrafica','Azienda') and 'righe' in z] or [z for z in d['sezioni'] if 'righe' in z]
    z=an[0]
    pos=0
    for i,r in enumerate(z['righe']):
        if r['etichetta'].startswith('Ragione'): pos=i+1
    for lab,val in add:
        z['righe'].insert(pos,dict(etichetta=lab,valore=f'{val} [[{n}]]'));pos+=1
        log.append((s,'P.IVA',val,url))
    if cont:
        ex=[r for r in z['righe'] if r['etichetta']=='Contatti']
        if ex: ex[0]['valore']=ex[0]['valore'].rstrip()+' · '+' · '.join(cont)+f' [[{n}]]'
        else: z['righe'].insert(pos,dict(etichetta='Contatti',valore=' · '.join(cont)+f' [[{n}]]'))
        log.append((s,'contatti',' · '.join(cont),url))
    save(s,d)
w=csv.writer(open(f'{Q}/correzioni-applicate.csv','w',encoding='utf-8-sig',newline=''),delimiter=';');w.writerow(['cantina','tipo','valore','dettaglio']);w.writerows(log)
import collections;print(collections.Counter(x[1] for x in log))
