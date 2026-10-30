# Integra le cantine toscane di Bere il Vino lette dai siti: schede nuove (DOC/DOCG dichiarata) + bere-da-collocare.
import json,re,os,csv,unicodedata,collections,sys
os.chdir('/home/claude/annuario')
B='bere-tosc/'
NUOVI=json.load(open(B+'nuovi.json',encoding='utf-8'))
DOM=json.load(open(B+'dom.json'))['ok']
EX=json.load(open(B+'esistenti_dom.json'))
COM=[l.strip() for l in open('toscana-dati/comuni_toscana.txt',encoding='utf-8') if l.strip()]
import re as _re
src=open('toscana-dati/gen_tosc.py',encoding='utf-8').read()
ALIAS=eval(_re.search(r'^ALIAS=(\{.*\})$',src,_re.M).group(1));ALIAS.update({'Artimino':'Carmignano','Orbetello Scalo':'Orbetello',"Montenero d'Orcia":'Castel del Piano','Poggio a Caiano':'Poggio a Caiano'})
COMS=sorted(set(COM)|set(ALIAS),key=lambda x:-len(x))
def noacc(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
def fixesc(s): return s.replace('\\u00f2','ò').replace('\\u00b0','°').replace('\\u00e0','à')
L={}
for l in open(B+'letture.tsv',encoding='utf-8'):
    p=l.rstrip('\n').split('\t')
    if len(p)>=6: L[int(p[0])]=[fixesc(x) for x in p]
PRE=re.compile(r"^(azienda agricola biologica|azienda biologica|azienda bioagricola|azienda agricola|azienda agraria|azienda vitivinicola|azienda vinicola|società agricola|societa agricola|casa vinicola|agricola|cantine|cantina)\s+",re.I)
def nome_pulito(n):
    n=re.sub(r'\s+',' ',n).strip()
    m=PRE.sub('',n)
    return m if len(m)>=4 and not re.match(r'(?i)^(del|della|dei|delle|di|da|dal|de)\s',m) else n
def slugify(s):
    s=noacc(s.lower()).replace("'",'')
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')
def comune_cap(addr):
    m=re.search(r'\b\d{5}\s+([A-ZÀ-Ý][A-Za-zÀ-ÿ\' .]+?)(?:\s*[,(]|\s+[A-Z]{2}$|$)',addr)
    if m: return m.group(1).strip().rstrip('.')
    m=re.search(r',\s*([A-ZÀ-Ý][A-Za-zÀ-ÿ\' .]+?)\s*(?:\(|,)\s*[A-Z]{2}\)?\b',addr)
    return m.group(1).strip() if m else ''
def comune_da(addr,prov_hint=''):
    c=comune_cap(addr)
    if c and not re.match(r'(?i)^(italia|loc|localit)',c): return ALIAS.get(c,c)
    a=noacc(addr).lower()
    for c in COMS:
        if re.search(r'(?<![a-z])'+re.escape(noacc(c).lower())+r'(?![a-z])',a): return ALIAS.get(c,c)
    return ''
# mappa denominazione -> chiave tipo
MAP=[(r'chianti classico','chianti-classico'),(r'colli senesi','colli-senesi'),(r'brunello','brunello'),(r'bolgheri','bolgheri'),
(r'nobile di montepulciano','nobile'),(r'maremma','maremma'),(r'valdarno di sopra','valdarno'),
(r'terre di casole','terre-di-casole'),(r'terre di pisa','terre-di-pisa'),(r'montescudaio','montescudaio'),(r'monteregio','monteregio'),
(r'colli di luni','colli-di-luni'),(r'colline lucchesi','colline-lucchesi'),(r'montecarlo','montecarlo'),(r'parrina','parrina'),
(r'suvereto|val di cornia','val-di-cornia'),(r'sovana|pitigliano','pitigliano'),(r'cortona','cortona'),(r'orcia','orcia'),
(r'montecucco','montecucco'),(r'carmignano|barco reale','carmignano'),(r'elba','elba'),(r'morellino','morellino'),
(r'vernaccia|san gimignano','vernaccia'),(r'etna','etna'),(r'prosecco','prosecco'),(r'euganei','euganei'),(r'chianti','chianti')]
def tipo_di(den):
    d=noacc(den).lower()
    for rx,k in MAP:
        if re.search(rx,d): return k
    return None
NUOVITIT={'chianti':('Produttori vini Chianti','Chianti|Chianti Superiore|Chianti Rufina|Chianti Colli Fiorentini|Chianti Colline Pisane|Chianti Montalbano|Vin Santo del Chianti'),
'morellino':('Produttori vini Morellino di Scansano','Morellino di Scansano'),
'vernaccia':('Produttori vini Vernaccia di San Gimignano','Vernaccia di San Gimignano|San Gimignano'),
'carmignano':('Produttori vini Carmignano','Carmignano|Barco Reale di Carmignano'),
'orcia':('Produttori vini Orcia','Orcia'),
'montecucco':('Produttori vini Montecucco','Montecucco'),
'elba':('Produttori vini Elba','Elba|Aleatico dell\'Elba'),
'terre-di-pisa':('Produttori vini Terre di Pisa','Terre di Pisa'),
'montescudaio':('Produttori vini Montescudaio','Montescudaio'),
'val-di-cornia':('Produttori vini Val di Cornia e Suvereto','Val di Cornia|Suvereto'),
'montecarlo':('Produttori vini Montecarlo','Montecarlo'),
'colline-lucchesi':('Produttori vini Colline Lucchesi','Colline Lucchesi'),
'pitigliano':('Produttori vini Bianco di Pitigliano e Sovana','Bianco di Pitigliano|Sovana'),
'cortona':('Produttori vini Cortona','Cortona'),
'colli-di-luni':('Produttori vini Colli di Luni','Colli di Luni'),
'parrina':('Produttori vini Parrina','Parrina'),
'monteregio':('Produttori vini Monteregio di Massa Marittima','Monteregio di Massa Marittima'),
'terre-di-casole':('Produttori vini Terre di Casole','Terre di Casole'),
'etna':('Produttori vini Etna','Etna')}
def prox(k): return '<option>'+'</option><option>'.join(NUOVITIT[k][1].split('|'))+'</option>'
tit=json.load(open('rifusione/tit.json',encoding='utf-8'))
for k,(t,o) in NUOVITIT.items():
    if k not in tit: tit[k]=[t,prox(k)]
json.dump(tit,open('rifusione/tit.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
# dedupe telefono con produttori esistenti
def digits(s): return re.sub(r'\D','',s)[-9:]
phones={}
for p in json.load(open('produttori.json')):
    try: t=json.dumps(json.load(open('dati/'+p['slug']+'.json')),ensure_ascii=False)
    except: continue
    for m in re.findall(r'(?:Tel\.?|tel\.?)[^;\[]{0,40}',t):
        d=digits(m)
        if len(d)>=8: phones[d]=p['slug']
existing_slugs={p['slug'] for p in json.load(open('produttori.json'))}
os.makedirs(B+'out/dati',exist_ok=True);os.makedirs(B+'out/chiarire',exist_ok=True)
for f in os.listdir(B+'out/dati'): os.remove(B+'out/dati/'+f)
for f in os.listdir(B+'out/chiarire'): os.remove(B+'out/chiarire/'+f)
placed=[];dacoll=[];dup_tel=[]
used=set(existing_slugs)
for i,r in enumerate(NUOVI):
    p=L.get(i)
    dom=DOM.get(str(i),'')
    bere=r['link'] or ('https://www.bereilvino.it/cantina/'+r['slug']+'/')
    base=dict(slug=r['slug'],nome=r['nome'],regione='Toscana',provincia=r['provincia'],cap=r['cap'],comune='',via='',telefono='',email='',sito='',link_bere_il_vino=bere,motivo='',nota_lettura='',vini_trovati='')
    if i in (252,253): continue
    if p is None:
        base['sito']=dom if dom and not re.search(r'cantinedelvino|bereilvino|facebook|winetourism|prodottitipici|duckduckgo|beverfood|wine-tour|tuscanywineries|toscanaelombardia|topimprese|winetradelab|passionevino|impetodivino|cittadelvino|wineflorence|sumupstore|vinievino|ibotriwm|valdamone|vincoop',dom) else ''
        base['motivo']=('sito non letto (esito della ricerca incerto o fuori selezione)' if base['sito'] else 'solo nome e CAP su Bere il Vino; sito ufficiale non trovato')
        dacoll.append(base);continue
    _,d,addr,tel,mail,vini=p[:6]
    base['sito']=d;base['via']=addr;base['telefono']=tel if tel!='-' else '';base['email']=mail if mail!='-' else '';base['vini_trovati']=vini if vini!='-' else ''
    base['comune']='' if addr.startswith(('Grosseto (','(')) else comune_da(addr)
    if 'NON TOSCANA' in addr or 'FUORI TOSCANA' in addr:
        base['motivo']='il sito trovato non corrisponde a una cantina toscana (omonimo): sede non in Toscana';base['nota_lettura']=addr;dacoll.append(base);continue
    dens=[x.strip() for x in vini.split(';') if x.strip() and x.strip()!='-' and re.search(r'DOC',x)]
    tipi={}
    for x in dens:
        k=tipo_di(x)
        if k:
            nome_den=re.sub(r'\s*(DOCG|DOC)(/DOCG)?\s*$','',x).strip()
            tipi.setdefault(k,[]);tipi[k].append(x)
    if not tipi:
        base['motivo']='sede toscana verificata sul sito, ma nessuna DOC/DOCG dichiarata' if dens==[] else 'denominazione dichiarata non riconducibile a una tessera'
        dacoll.append(base);continue
    d9=digits(tel)
    if d9 in phones and len(d9)>=8: dup_tel.append((i,r['nome'],phones[d9]))
    placed.append((i,r,p,base,tipi,dens))
for i,nm,sl in dup_tel:
    placed=[x for x in placed if x[0]!=i]
    for x in NUOVI[i:i+1]: pass
    b=dict(slug=NUOVI[i]['slug'],nome=NUOVI[i]['nome'],regione='Toscana',provincia=NUOVI[i]['provincia'],cap=NUOVI[i]['cap'],comune='',via=L[i][2],telefono=L[i][3],email=L[i][4],sito=L[i][1],link_bere_il_vino=NUOVI[i]['link'],motivo='stesso indirizzo e telefono di una cantina già in guida ('+sl+'): probabile stesso produttore, da confermare',nota_lettura='',vini_trovati=L[i][5])
    dacoll.append(b)
print('collocate',len(placed),'da-collocare',len(dacoll),'dup tel',dup_tel)
# scrivi schede
prods=[]
for i,r,p,base,tipi,dens in placed:
    _,d,addr,tel,mail,vini=p[:6]
    nome=nome_pulito(r['nome']);slug=slugify(nome)
    k=2;s0=slug
    while slug in used: slug=s0+'-'+str(k);k+=1
    used.add(slug)
    righe=[]
    sede=addr if not addr.startswith('(') else 'Provincia di '+r['provincia']+(' (CAP '+r['cap']+') — indirizzo non letto sul sito' )
    righe.append(dict(etichetta='Sede',valore=sede+' [[1]]'))
    cont='; '.join(x for x in [('Tel. '+tel) if tel!='-' else '',mail if mail!='-' else ''] if x)
    if cont: righe.append(dict(etichetta='Contatti',valore=cont+' [[1]]'))
    righe.append(dict(etichetta='Sito ufficiale',valore='{{https://www.%s/|%s}} [[1]]'%(d,d)))
    righe.append(dict(etichetta='Presenza in elenchi',valore='Presente nell’archivio delle cantine di Bere il Vino (scheda con nome, CAP e provincia) [[2]]'))
    den_txt='; '.join(dict.fromkeys(dens))
    P=dict(nome=nome,slug=slug,sezioni=[
     dict(titolo='Anagrafica',righe=righe),
     dict(titolo='Azienda: proprietà e struttura',righe=[dict(etichetta='Storia e proprietà',valore='Non disponibile nelle fonti consultate')]),
     dict(titolo='Vini',righe=[dict(etichetta='Denominazioni dichiarate',valore=den_txt+' [[1]]')]),
     dict(titolo='Riconoscimenti',righe=[dict(etichetta='Premi e punteggi',valore='Non presenti nelle fonti consultate')]),
     dict(titolo='Identità online',righe=[dict(etichetta='Negozi online e marketplace',valore='Presenza non verificata'),dict(etichetta='Piattaforme',valore='Google Business Profile, Vivino, Wine-Searcher, YouTube, Wikipedia: presenza non verificata')])],
     consultate='Sito ufficiale della cantina e scheda nell’archivio delle cantine di Bere il Vino, consultati il 26 ottobre 2026. Ogni dato della scheda rinvia alla fonte con il numero tra parentesi quadre.',
     fonti=[dict(n=1,testo='Sito ufficiale della cantina, pagina iniziale consultata il 26 ottobre 2026.',url='https://www.%s/'%d,etichetta=d),
            dict(n=2,testo='Bere il Vino, scheda della cantina nell’archivio delle cantine, consultata il 26 ottobre 2026.',url=base['link_bere_il_vino'],etichetta='bereilvino.it')])
    json.dump(P,open(B+'out/dati/'+slug+'.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    q=['Ragione sociale | Non indicata nel sito consultato | Qual è la ragione sociale e la partita IVA?',
       'Vini | Il sito consultato non elenca tutte le etichette | Quali sono i vini a denominazione e con quale marchio?',
       'Storia | Non presente nel sito consultato | Chi sono i proprietari e da quando esiste l’azienda?']
    if 'CAP -' in addr or re.search(r'\b-,',addr) or addr.startswith('('): q.insert(0,'Sede | Indirizzo incompleto nel sito consultato | Qual è via, numero e CAP della sede legale?')
    open(B+'out/chiarire/'+slug+'.txt','w',encoding='utf-8').write('\n'.join(q)+'\n')
    tp={k:list(dict.fromkeys(re.sub(r'\s*\(?(DOCG|DOC)\)?\s*(Riserva)?.*$','',x).strip() or x for x in v)) for k,v in tipi.items()}
    prods.append(dict(slug=slug,nome=nome,regione='Toscana',comune=base['comune'],tipi=tp,membri=[slug],primario=slug))
json.dump(prods,open(B+'out/produttori_extra.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
json.dump(dacoll,open(B+'out/dacollocare.json','w',encoding='utf-8'),ensure_ascii=False)
print('schede nuove',len(prods),collections.Counter(k for p in prods for k in p['tipi']).most_common())
print([ (p['nome'],p['comune']) for p in prods if not p['comune']])
