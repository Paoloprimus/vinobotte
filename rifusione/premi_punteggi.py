import re
FN=re.compile(r'(?:\s*\[\[\d+\]\])+\s*$')
AWARD=re.compile(r'bicchier|medagli|\boro\b|argento|bronzo|stell|grappol|\bviti\b|corona|troph|trofe|premi|award|winehunter|top wine|wine of the year|miglior|top 100|top hundred|sigillo|selezionat|doppio oro|\bmedal',re.I)
SCORE=re.compile(r'\bpunt(?:i|eggi|eggio)\b|/\s*100\b|(?<![\d,./])(?:7\d|8\d|9\d|100)(?:[–-](?:7\d|8\d|9\d|100))?(?![\d,.]|\s*(?:bicchier|stell|grappol|viti|%))',re.I)
DESC=re.compile(r'^(il sito|la pagina|la sezione|la cantina|pagina|citat|secondo|il premio|la scheda|la scheda)',re.I)
def split_fn(v):
    m=FN.search(v); fn=m.group(0).strip() if m else ''
    return (v[:m.start()] if m else v).strip(), fn
def is_score(t):
    t2=re.sub(r'\b(19|20)\d\d\b','',t)
    return bool(SCORE.search(t2))
def classify(it):
    a=bool(AWARD.search(it)); s=is_score(it)
    if DESC.match(it) and not re.search(r'\d{2}',re.sub(r'\b(19|20)\d\d\b','',it)):
        return 'S' if re.search(r'punteggi|recension',it,re.I) and not a else 'P'
    if s and not a: return 'S'
    if a and not s: return 'P'
    if s and a: return 'M'
    return 'P'
def dividi(v):
    body,fn=split_fn(v); body=body.rstrip('.')
    premi=[];punt=[]
    for it in [x.strip(' .') for x in re.split(r';\s+',body) if x.strip(' .')]:
        c=classify(it)
        if c=='M':
            parts=[x.strip() for x in re.split(r',\s+(?=[A-ZÀ-Ý“«]|\d)',it) if x.strip()]
            prefix=''
            m=re.match(r'^([^:]{3,60}:)\s',it)
            for p in parts:
                cc=classify(p)
                (punt if cc=='S' else premi).append(p)
            if len(parts)==1: (punt if False else premi).append(it)
        elif c=='S': punt.append(it)
        else: premi.append(it)
    return premi,punt,fn
