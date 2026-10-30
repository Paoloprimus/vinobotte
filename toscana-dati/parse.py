import json,re,csv,html
d=json.load(open('/tmp/tosc.json'))
rows=[]
def add(cons,nome,ind,tel,em,sito,url,vini=''):
    rows.append(dict(consorzio=cons,nome=re.sub(r'\s+',' ',nome).strip(),indirizzo=re.sub(r'\s+',' ',ind).strip(),telefono=tel.strip(),email=em.strip().lower(),sito=sito.strip(),fonte=url,vini=vini))
EM=re.compile(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+')
WEB=re.compile(r'(?:https?://)?(?:www\.)[\w.-]+\.[a-z]{2,}[\w/.-]*|https?://[\w.-]+\.[a-z]{2,}[\w/.-]*',re.I)
STR=r'(?:Via|V\.le|Viale|V\.|Loc\.|Località|Localit|Strada|Str\.|Podere|P\.zza|Piazza|Fraz|Frazione|Borgo|Largo|Vicolo|Contrada|Pod\.|S\.P\.|SP|SS|S\.S\.|Voc\.|Vocabolo|Corso|Fattoria|Tenuta)\b'
# Nobile
for r in d['rows']:
    t=r['t']; m=re.search(STR,t)
    nome=t[:m.start()] if m else t.split(' ')[0]
    rest=t[m.start():] if m else ''
    em=EM.search(t); web=WEB.search(t.replace(em.group(0),'') if em else t)
    tel=re.findall(r'(?:\+39\s?)?\b0\d{2,4}[\s/]?\d{5,8}\b|\b3\d{2}[\s]?\d{6,7}\b',rest)
    ind=rest
    for x in [em.group(0) if em else '',web.group(0) if web else '']+tel: ind=ind.replace(x,'')
    add('Vino Nobile di Montepulciano',nome.title() if nome.isupper() else nome,ind,' | '.join(tel),em.group(0) if em else '',web.group(0) if web else '',r['u'])
# CCS
for r in d['ccs']:
    p=[x.strip() for x in r['t'].split(' | ')]
    nome=re.sub(r'^\d+\s*[–-]\s*','',p[0]); ind=p[1] if len(p)>1 else ''
    tel=''; em=''; web=''
    for x in p[2:]:
        if x.startswith(('tel','cell')): tel=' '.join(re.findall(r'(?:tel|cell)\s*([\d +/]+)',x))
        if x.startswith('mail'): em=x[4:].strip()
        if x.startswith('web'): web=x[3:].strip()
    add('Chianti Colli Senesi',nome.title() if nome.isupper() else nome,ind,tel,em,web,'https://www.consorziochianticollisenesi.it/aziende-e-produttori/')
# Maremma
for n,a,tel,em,web,s in d['maremma']:
    tel=re.sub(r'^(\d+)\1$',r'\1',tel)
    add('Maremma Toscana',n.title() if n.isupper() else n,a,tel,em,web,'https://www.aziendevinimaremma.it/directory/listing/'+s)
# Chianti Classico
for n,u,t in d['chiantic']:
    i=t.rfind('Contatti ')
    c=t[i+9:] if i>=0 else ''
    c=re.split(r'\sOrari\b',c)[0]
    tel=re.search(r'Telefono:\s*(.*?)\s*(?:Email:|Sito Web:|$)',c); em=re.search(r'Email:\s*(\S+)',c); web=re.search(r'Sito Web:\s*(\S+)',c)
    ind=re.split(r'Telefono:|Email:|Sito Web:',c)[0]
    add('Chianti Classico',n,ind,tel.group(1) if tel else '',em.group(1) if em else '',web.group(1) if web else '','https://www.chianticlassico.com'+u)
# Brunello
for n,u,t in d['brunello']:
    if not re.search(r'Indirizzo',t): continue
    g=lambda k:(re.search(k+r' •\n(.*?)\n',t) or [None,''])[1]
    m=re.search(r'Produzione\n(.*?)(?:\nvisita cantine|\nvedi tutte|\n)(?:visita|vedi|Orario)',t,re.S)
    vini=''
    mm=re.search(r'Produzione\n(.*?)\n(?:visita cantine|vedi tutte le aziende)',t,re.S)
    if mm: vini='; '.join(x.strip() for x in mm.group(1).split('\n') if x.strip())
    add('Brunello di Montalcino',n,g('Indirizzo'),g('Telefono'),g('Email'),g('Sito web'),'https://www.consorziobrunellodimontalcino.it'+u,vini)
# Bolgheri
for n,u,t in d['bolgheri']:
    x=t.split(' ## ')[-1]
    mm=re.search(r'Raggiungici con Google Maps \|\s*(.*?)(?:\s*\|\s*)?([\w.+-]+@[\w.-]+\.\w+)',x)
    slug=u.rstrip('/').split('/')[-1]
    nm=n or slug.replace('-',' ').title()
    em=EM.search(x.split('Twitter')[0]); 
    pre=x.split('Twitter')[0]
    i=pre.find('Raggiungici con Google Maps')
    blk=pre[i+27:] if i>=0 else ''
    blk=blk.lstrip(' |')
    em2=EM.search(blk)
    tel=re.findall(r'\+39\s?[\d ]{8,13}',blk)
    web=WEB.search(blk.replace(em2.group(0),'') if em2 else blk)
    ind=blk
    if em2: ind=ind[:ind.find(em2.group(0))]
    ind=re.sub(r'\+39[\d ]*','',ind).strip(' |')
    add('Bolgheri',nm,ind,' | '.join(t_.strip() for t_ in tel),em2.group(0) if em2 else '',web.group(0) if web else '','https://www.bolgheridoc.com'+u)
# Valdarno
L=d['valdarno']; i=0; cur=[]; recs=[]
for ln in L:
    if ln.startswith('Consorzio Valdarno') or ln=='Soci': break
    cur.append(ln)
    if EM.search(ln): recs.append(cur); cur=[]
for r in recs:
    em=EM.search(r[-1]).group(0); tel=[x for x in r if re.match(r'\+?\d[\d +]{7,}$',x)]
    other=[x for x in r if x not in tel and x!=r[-1]]
    nome=other[0]; ind=' '.join(other[1:])
    add('Valdarno di Sopra',nome,ind,' | '.join(tel),em,'','https://www.valdarnodisopradoc.it/consorzio/')

# --- post-process
PH=re.compile(r'(?:\+39[\s.]?)?(?<!\d)[03]\d(?:[\s./]?\d){6,10}(?!\d)')
for r in rows:
    blob=' '.join([r['indirizzo'],r['telefono'],r['email'],r['sito']])
    blob=re.sub(r'(\.[a-z]{2,3})(?=www\.)',r'\1 ',blob)
    em=EM.findall(blob); r['email']=em[0].lower() if em else ''
    nb=blob
    for e in em: nb=nb.replace(e,' ')
    w=WEB.findall(nb); 
    if not r['sito'] or ':' in r['sito'][:2] or 'www' in r['email']: r['sito']=(w[0] if w else r['sito'].strip(': '))
    r['sito']=r['sito'].strip(': ').rstrip('/.,')
    tl=[]
    for src in (r['telefono'],r['indirizzo']):
        for m in PH.findall(src):
            m=re.sub(r'\s+',' ',m).strip()
            if m not in tl and re.sub(r'\D','',m) not in [re.sub(r'\D','',x) for x in tl]: tl.append(m)
    r['telefono']=' | '.join(tl)
    ind=r['indirizzo']
    ind=PH.sub('',ind); ind=re.sub(r'\(\)|Tel\.?|Cell\.?','',ind)
    r['indirizzo']=re.sub(r'\s+',' ',ind).strip(' |,-–')
w=csv.DictWriter(open('/tmp/tosc_soci.csv','w',newline='',encoding='utf-8-sig'),fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
from collections import Counter
print(Counter(r['consorzio'] for r in rows))
for c in Counter(r['consorzio'] for r in rows):
    rr=[r for r in rows if r['consorzio']==c]
    print(c,'noaddr',sum(not r['indirizzo'] for r in rr),'notel',sum(not r['telefono'] for r in rr),'noemail',sum(not r['email'] for r in rr),'nosito',sum(not r['sito'] for r in rr))
