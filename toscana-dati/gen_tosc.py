import csv,re,json,os,glob,unicodedata,collections
os.chdir('/home/claude/annuario')
R=list(csv.DictReader(open('toscana-dati/tosc_soci.csv',encoding='utf-8-sig'),delimiter=';'))
COM=[l.strip() for l in open('toscana-dati/comuni_toscana.txt',encoding='utf-8') if l.strip()]
ALIAS={'Bolgheri':'Castagneto Carducci','Donoratico':'Castagneto Carducci','Valiano':'Montepulciano','Gracciano':'Montepulciano','Acquaviva':'Montepulciano','Abbadia':'Montepulciano','Monticello Amiata':'Cinigiano','Colle Val d\'Elsa':'Colle di Val d\'Elsa','Colle di Val d\'Elsa':'Colle di Val d\'Elsa','Sant\'Angelo in Colle':'Montalcino','Sant\'Angelo Scalo':'Montalcino','Castelnuovo dell\'Abate':'Montalcino','Castelnuovo Abate':'Montalcino','Torrenieri':'Montalcino','Poggio alle Mura':'Montalcino','Greve':'Greve in Chianti','Tavarnelle':'Barberino Tavarnelle','Barberino Val d\'Elsa':'Barberino Tavarnelle','Tavarnelle Val di Pesa':'Barberino Tavarnelle','Figline Valdarno':'Figline e Incisa Valdarno','Pergine':'Pergine Valdarno','Mercatale Valdarno':'Montevarchi','Cervognano':'Montepulciano','Poggiano':'Montepulciano','Sant\'Albino':'Montepulciano','Pantano':'Montepulciano','Montefollonico':'Torrita di Siena','Piazze':'Cetona','Fonteblanda':'Orbetello','Albinia':'Orbetello','Saturnia':'Manciano','Montemassi':'Roccastrada','Sovana':'Sorano','Pescia Fiorentina':'Capalbio','Montiano':'Magliano in Toscana','Levane':'Montevarchi','Panzano in Chianti':'Greve in Chianti','Castiglion Fibocchi':'Castiglion Fibocchi','Panzano':'Greve in Chianti','Strada in Chianti':'Greve in Chianti','Badia a Passignano':'Barberino Tavarnelle','Marcialla':'Barberino Tavarnelle'}
COM=sorted(set(COM)|set(ALIAS),key=lambda x:-len(x))
SEZ={'Brunello di Montalcino':('brunello','Consorzio del Vino Brunello di Montalcino','Brunello di Montalcino'),
'Chianti Classico':('chianti-classico','Consorzio Vino Chianti Classico','Chianti Classico'),
'Bolgheri':('bolgheri','Consorzio per la Tutela dei Vini DOC Bolgheri e DOC Bolgheri Sassicaia','Bolgheri'),
'Vino Nobile di Montepulciano':('nobile','Consorzio del Vino Nobile di Montepulciano','Vino Nobile di Montepulciano'),
'Maremma Toscana':('maremma','Consorzio Tutela Vini della Maremma Toscana','Maremma Toscana'),
'Chianti Colli Senesi':('colli-senesi','Consorzio Chianti Colli Senesi','Chianti Colli Senesi'),
'Valdarno di Sopra':('valdarno','Consorzio Valdarno di Sopra DOC','Valdarno di Sopra')}
DEN={'brunello':['Brunello di Montalcino'],'chianti-classico':['Chianti Classico'],'bolgheri':['Bolgheri'],'nobile':['Vino Nobile di Montepulciano'],'maremma':['Maremma Toscana'],'colli-senesi':['Chianti Colli Senesi'],'valdarno':['Valdarno di Sopra']}
def noacc(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
LEGAL=re.compile(r"\b(s\.?\s?r\.?\s?l\.?|s\.?\s?p\.?\s?a\.?|s\.?\s?n\.?\s?c\.?|s\.?\s?a\.?\s?s\.?|s\.?\s?s\.?\s?a?\.?|s\.?\s?a\.?\s?r\.?\s?l\.?|soc\.?\s?coop\.?\s?agr\.?|societa'? agricola( semplice)?|soc\.?\s?agr\.?(icola)?( semplice)?|soc\.? semplice|cooperativa)\b\.?",re.I)
PREF=re.compile(r"^(azienda agricola biologica|azienda agrituristica|azienda bioagricola|azienda agricola|az\.? ?agr\.?|az\.|azienda)\s+",re.I)
def titleit(n):
    if n.isupper() and len(n)>3:
        n=n.title()
        n=re.sub(r"\b(Di|Del|Della|Dei|Delle|Da|Al|Alla|Alle|E|In|La|Il|Le|Lo|Ai|Dal)\b",lambda m:m.group(1).lower() if True else m.group(1),n)
        n=re.sub(r"(?<=\w)’S\b","’s",n)
        n=n[0].upper()+n[1:]
    return n
def clean_name(raw):
    n=re.sub(r'\s+',' ',raw).strip()
    n=n.replace('’',"’")
    rs=''
    if LEGAL.search(n) or PREF.match(n): rs=n
    n=PREF.sub('',n)
    n=LEGAL.sub('',n)
    n=re.sub(r"\s*\((?:[^)]*)\)\s*$",'',n) if re.search(r'\(.*S\.?S',n) else n
    n=re.sub(r'\s+',' ',n).strip(' -–,.')
    n=titleit(n)
    n=re.sub(r"\bDi\b(?=\s)",'di',n) if False else n
    return n,rs
def key(n):
    k=noacc(n.lower()); k=re.sub(r"[’'`.]",'',k); k=LEGAL.sub(' ',k)
    k=re.sub(r'\b(azienda agricola|az agr|societa agricola|fattoria|tenuta|tenute|podere|agricola|cantina|cantine|la|il|le|lo|di|del|della|dei|delle|e|&|srl|spa|ss|sas|snc|vini)\b',' ',k)
    return re.sub(r'[^a-z0-9]+',' ',k).strip()
def dom(s):
    s=re.sub(r'^https?://','',(s or '').lower()); s=re.sub(r'^www\.','',s); return s.split('/')[0]
FIX={}  # slug sorgente -> nome corretto
def comune_di(ind):
    t=ind
    m=re.search(r'\b(5\d{4})\b',t)
    seg=t[m.end():] if m else t
    best=None
    for src in ([seg,t] if m else [t]):
        hits=[]
        for c in COM:
            for mm in re.finditer(r'(?<![\w])'+re.escape(c).replace("'", "['’]")+r'(?![\w])',src,re.I):
                hits.append((mm.start(),mm.end(),c))
        if hits:
            # preferisci il match più lungo tra quelli che iniziano per primi dopo il CAP
            hits.sort(key=lambda h:(h[0],-(h[1]-h[0])))
            if src is seg: best=hits[0][2]
            else:
                hits.sort(key=lambda h:(-h[1],-(h[1]-h[0]))); best=hits[0][2]
            break
    best=ALIAS.get(best,best)
    return best or ''
def pulisci_ind(i):
    i=re.sub(r'([a-zà-ù])(\d{5})',r'\1 \2',i)
    i=re.sub(r',?\s*Ital(?:y|ia)\b','',i)
    i=re.sub(r'\s+',' ',i).strip(' ,;-–')
    return i
# nome da slug per Nobile
def slugname(u): return u.rstrip('/').split('/')[-1].replace('-',' ').title()
NT={x['u']:x['t'] for x in json.load(open('toscana-dati/tosc.json'))['rows']}
NOBMAN={'6086':'D&D','az-ag-ercolani-carlo-marco':'Ercolani Carlo e Marco','az-ag-cantina-priorino':'Cantina Priorino','podere-lamberto':'Podere Lamberto'}
def nobile_nome(u):
    if u.rstrip('/').split('/')[-1] in NOBMAN: return NOBMAN[u.rstrip('/').split('/')[-1]]
    t=NT.get(u,'');sl=[w for w in u.rstrip('/').split('/')[-1].split('-') if w]
    words=t.split(' ');acc=[];toks=[]
    for w in words:
        acc.append(w);toks+=[x for x in re.sub(r'[^a-z0-9 ]+',' ',noacc(w.lower())).split() if x]
        if toks==sl: return ' '.join(acc)
        if len(toks)>len(sl): break
    return ' '.join(x.capitalize() for x in sl)
rec=[]
for r in R:
    if r['fonte'].rstrip('/').endswith('/il-coventino'): continue
    n=r['nome']
    if r['consorzio']=='Vino Nobile di Montepulciano': n=nobile_nome(r['fonte'])
    if r['consorzio']=='Vino Nobile di Montepulciano' and n.strip()=='D&D': n='D&D'
    if r['consorzio']=='Bolgheri' and not n: n=slugname(r['fonte'])
    nome,rs=clean_name(n)
    if r['consorzio']=='Vino Nobile di Montepulciano' and nome.upper()==nome and len(nome)>4: nome=titleit(nome)
    rec.append(dict(r,nome_orig=r['nome'],nome=nome,rs=rs,key=key(nome),dom=dom(r['sito'])))
# merge entro lo stesso consorzio e fra consorzi: stessa chiave, oppure stesso dominio con nomi sottoinsieme
G=[]  # gruppi = cantine
idx={}
for i,r in enumerate(rec):
    placed=None
    for gi,g in enumerate(G):
        for j in g:
            o=rec[j]
            if r['key'] and r['key']==o['key']: placed=gi;break
            if r['dom'] and r['dom']==o['dom'] and r['indirizzo'] and r['indirizzo']==o['indirizzo']: placed=gi;break
            if r['dom'] and r['dom']==o['dom'] and r['key'] and o['key']:
                a,b=set(r['key'].split()),set(o['key'].split())
                if a<=b or b<=a: placed=gi;break
        if placed is not None:break
    if placed is None: G.append([i])
    else: G[placed].append(i)
print('record',len(rec),'cantine distinte',len(G))
# scheda per (gruppo, consorzio)
SPEC={};SLUGS=set()
def slugify(n):
    s=noacc(n.lower()).replace('&',' e ').replace("'",'').replace('’','')
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')
EXIST=set()
for f in glob.glob('spec/**/*.txt',recursive=True):
    m=re.search(r'^slug: (\S+)',open(f,encoding='utf-8').read(),re.M)
    if m: EXIST.add(m.group(1))
cant=[]
for g in G:
    rows=[rec[i] for i in g]
    nome=min((r['nome'] for r in rows),key=lambda x:(x.isupper(),len(x)))
    cons=collections.OrderedDict()
    for r in rows: cons.setdefault(r['consorzio'],[]).append(r)
    cant.append((nome,cons))
slug_of={}
for nome,cons in cant:
    for c in cons:
        sz=SEZ[c][0]; base=slugify(nome)+'-'+sz; s=base;k=2
        while s in SLUGS or s in EXIST: s=base+'-'+str(k);k+=1
        SLUGS.add(s); slug_of[(nome,c)]=s
OVc={};OVd={}
os.makedirs('spec/toscana',exist_ok=True)
def tel_fmt(t):
    out=[]
    for x in t.split(' | '):
        x=x.strip()
        if not x: continue
        d=re.sub(r'\D','',x)
        if d.startswith('39') and len(d)>10: d=d[2:]
        out.append(('+39 '+d) if len(d)>=9 else x)
    return out
for nome,cons in cant:
    for c,rows in cons.items():
        sz,consfull,den=SEZ[c]
        slug=slug_of[(nome,c)]
        r0=rows[0]
        src='['+r0['fonte']+']'
        L=['dominio: -','nome: '+nome,'slug: '+slug,'consultate: Scheda della cantina nell’elenco delle aziende associate a '+consfull+', consultata il 26 ottobre 2026. Ogni dato della scheda rinvia alla fonte con il numero tra parentesi quadre.','@Anagrafica']
        rs=next((r['rs'] for r in rows if r['rs']),'')
        if rs and key(rs)!=key(nome) or (rs and rs.lower()!=nome.lower()): L.append('Ragione sociale | '+rs+' (come da elenco del Consorzio) '+src)
        ind=''
        for r in rows:
            if r['indirizzo'] and not re.match(r'(www\.|https?:)',r['indirizzo']): ind=pulisci_ind(r['indirizzo']);break
        com=''
        for r in rows:
            com=comune_di(pulisci_ind(r['indirizzo'])) if r['indirizzo'] else ''
            if com: break
        if ind: L.append('Sede | '+ind+' '+src)
        tels=[];ems=[]
        for r in rows:
            for t in tel_fmt(r['telefono']):
                if t not in tels: tels.append(t)
            if r['email'] and r['email'] not in ems: ems.append(r['email'])
        cc=[]
        if tels: cc.append('Tel. '+' / '.join(tels))
        cc+=ems
        if cc: L.append('Contatti | '+'; '.join(cc)+' '+src)
        sito=next((r['sito'] for r in rows if r['sito']),'')
        if sito:
            u=sito if sito.startswith('http') else 'http://'+sito
            L.append('Sito ufficiale | {{'+u+'|'+re.sub(r'^https?://(www\.)?','',u).rstrip('/')+'}} '+src)
        L.append('Consorzio | Compare nell’elenco delle aziende associate a '+consfull+' '+src)
        for c2,rows2 in cons.items():
            if c2==c: continue
            sz2,consfull2,den2=SEZ[c2]
            nm2=rows2[0]['nome_orig']
            L.append('Altro consorzio | Compare anche nell’elenco di '+consfull2+': {{/pagine/'+slug_of[(nome,c2)]+'.html|scheda '+den2+'}} ['+rows2[0]['fonte']+']')
        L.append('@Azienda: proprietà e struttura')
        L.append('Storia e proprietà | Non disponibile nelle fonti consultate')
        L.append('@Vini')
        vini=next((r['vini'] for r in rows if r['vini']),'')
        dens=list(DEN[sz])
        if vini:
            L.append('Denominazioni dichiarate | '+vini+' '+src)
        else:
            L.append('Elenco vini | Non indicato nella scheda del Consorzio; non ancora raccolto '+src)
        L+=['@Riconoscimenti','Premi e punteggi | Non presenti nelle fonti consultate','@Identità online','Negozi online e marketplace | Presenza non verificata','Piattaforme | Google Business Profile, Vivino, Wine-Searcher, YouTube, Wikipedia: presenza non verificata']
        L.append('? Ragione sociale | Non indicata nell’elenco del Consorzio | Qual è la ragione sociale e la partita IVA?')
        L.append('? Vini | Il Consorzio non elenca i vini dell’azienda | Quali sono i vini a denominazione '+den+' e con quale marchio?')
        L.append('? Storia | Non presente nell’elenco del Consorzio | Chi sono i proprietari e da quando esiste l’azienda?')
        open('spec/toscana/'+slug+'.txt','w',encoding='utf-8').write('\n'.join(L)+'\n')
        OVc[slug]=com
        d=set(dens)
        if vini:
            if 'Rosso di Montalcino' in vini: d.add('Rosso di Montalcino')
            if 'Sant' in vini: d.add("Sant'Antimo")
        OVd[slug]=sorted(d)
json.dump({'comuni':OVc,'den':OVd},open('tosc_overlay.json','w',encoding='utf-8'),ensure_ascii=False)
print('spec scritte',len(OVc),'senza comune',sum(1 for v in OVc.values() if not v))
multi=[(n,list(c)) for n,c in cant if len(c)>1]
print('cantine in piu consorzi',len(multi))
