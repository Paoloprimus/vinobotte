#!/usr/bin/env python3
# Interpreta i testi in out/*.txt e produce nuovi_estratti.json (da mandare a Claude) + un riepilogo da controllare.
# Uso: python3 estrai.py
import re,json,glob,os,unicodedata
def piva_ok(p):
    if not re.fullmatch(r'\d{11}',p): return False
    t=0
    for i,c in enumerate(p):
        d=int(c)
        if i%2:
            d*=2
            if d>9:d-=9
        t+=d
    return t%10==0
DEN=['Vernaccia di San Gimignano DOCG Riserva','Vernaccia di San Gimignano DOCG','Vernaccia di San Gimignano','Chianti Colli Senesi DOCG','Chianti Colli Senesi','Chianti Classico','Chianti DOCG','Chianti','San Gimignano Rosso','San Gimignano DOC','Vin Santo di San Gimignano','Vin Santo del Chianti','Vin Santo','Toscana IGT','Toscana Bianco IGT','Toscana Rosso IGT','Rosato IGT','Vermentino','Sangiovese','Brunello di Montalcino','Morellino di Scansano']
def a(s): return unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()
def slug(s):
    s=unicodedata.normalize('NFD',s.lower());s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')
out=[];rep=[]
for f in sorted(glob.glob('out/*.txt')):
    T=open(f,encoding='utf8').read()
    nome=re.search(r'^# (.+)$',T,re.M).group(1).strip()
    url=re.search(r'^# (https?://\S+)',T,re.M).group(1)
    dom=re.sub(r'^https?://(www\.)?','',url).strip('/')
    corpo=re.sub(r'^#.*$','',T,flags=re.M)
    # P.IVA: prima valida tra le sequenze di 11 cifre dopo "P.IVA/P.I./Partita IVA"
    pivas=[]
    for m in re.finditer(r'(?:P\.?\s?IVA|P\.?\s?I\.|Partita\s+IVA|C\.?F\.?)[^0-9A-Za-z]{0,6}(?:IT)?\s*(\d{11})',corpo,re.I):
        if piva_ok(m.group(1)) and m.group(1) not in pivas: pivas.append(m.group(1))
    # ragione sociale: riga con P.IVA, ripulita
    rag=''
    for l in corpo.split('\n'):
        if pivas and pivas[0] in l.replace(' ','') or (pivas and pivas[0] in l):
            r=re.sub(r'\s*[|\-–]\s*(Credits|Privacy|Cookie).*$','',l).strip()
            r=re.sub(r'^©\s*\d{4}\s*','',r)
            if 10<len(r)<200: rag=r;break
    # indirizzo: Loc./Via ... 53037 San Gimignano
    ind=''
    m=re.search(r'((?:Loc(?:alit[àa])?\.?|Via|Viale|Strada|Str\.|S\.P\.|SP|Podere|Fraz(?:ione)?\.?)\s[^\n]{3,80}?,?\s*(?:5\d{4})\s*(?:-|,)?\s*([A-Z][A-Za-zÀ-ÿ\' ]{2,30}?)(?:\s*[\(,-]\s*([A-Z]{2})\)?|\s*$|\n))',corpo,re.I|re.M)
    comune=''
    if m:
        ind=re.sub(r'\s+',' ',m.group(1)).strip()
        comune=m.group(2).strip().title()
    tel=[]
    for m in re.finditer(r'(?:\+39\s?)?(?<!\d)(0\d{2,3}[\s./-]?\d{5,7}|3\d{2}[\s./-]?\d{6,7})(?!\d)',corpo):
        t=re.sub(r'\s+',' ',m.group(0)).strip()
        if t not in tel and not re.fullmatch(r'\d{11}',re.sub(r'\D','',t)) : tel.append(t)
    mail=sorted(set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+',corpo)))
    mail=[x for x in mail if not re.search(r'(sentry|example|wixpress|iubenda)',x)]
    # storia: primo paragrafo con anni/fondazione
    st=''
    for p in re.split(r'\n{1,}',corpo):
        p=p.strip()
        if 60<len(p)<500 and re.search(r'(nasce|nata|fondat|dal\s(19|20)\d\d|nel\s(19|20)\d\d|generazion|famiglia)',p,re.I):
            st=p;break
    den=[]
    low=corpo.lower()
    for d in DEN:
        if d.lower() in low and not any(d.lower() in x.lower() for x in den): den.append(d)
    vino=len(re.findall(r'\b(vino|vini|wine|cantina|vigneti|vernaccia|chianti|brunello|docg|doc|igt)\b',corpo,re.I))
    nome_ok=any(t in a(corpo) for t in re.findall(r'[a-z]{4,}',a(nome)) )
    out.append(dict(verifica=('' if vino>=5 and nome_ok else 'CONTROLLARE: pagina poco "da vino" o nome non trovato'),slug=slug(nome),nome=nome,comune=comune,sede=ind,tel='; '.join(tel[:3]),
      contatti=('Tel. '+'; '.join(tel[:3])+(('; email '+mail[0]) if mail else '')) if tel else '',
      rag=rag,piva=pivas[0] if pivas else '',sito=url,dom=dom,storia=st,den='; '.join(den)))
    rep.append(f"{'[!] ' if (vino<5 or not nome_ok) else ''}{nome}: sede={'ok' if ind else 'MANCA'} tel={'ok' if tel else 'MANCA'} piva={'ok' if pivas else 'MANCA'} storia={'ok' if st else '-'} den={len(den)}")
json.dump(out,open('nuovi_estratti.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
print('\n'.join(rep));print('\nScritto nuovi_estratti.json ->',len(out),'cantine')
