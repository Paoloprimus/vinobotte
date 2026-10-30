import sys,os,json,re,glob,collections
os.chdir('/home/claude/annuario')
sys.path.insert(0,'/home/claude/annuario/rifusione')
import analisi
from analisi import regione as _reg_from_sede
DATI={}
for f in glob.glob('dati_vecchi/*.json'):
    d=json.load(open(f,encoding='utf-8')); DATI[d['slug']]=d
SPEC={}
for f in glob.glob('spec/**/*.txt',recursive=True):
    m=re.search(r'^slug: (\S+)',open(f,encoding='utf-8').read(),re.M)
    if m: SPEC[m.group(1)]=f
cerca={c[1]:c for c in json.load(open('rifusione/cerca_pre.json',encoding='utf-8'))}
def clean(v): return re.sub(r'\[\[\d+\]\]','',v)
def sede_rows(d):
    out=[]
    for s in d['sezioni']:
        for r in s.get('righe',[]):
            if re.match(r'(sede|indirizzo)',r['etichetta'],re.I): out.append((r['etichetta'],clean(r['valore'])))
    return out
def reg_scheda(slug):
    d=DATI[slug]
    for et,v in sede_rows(d):
        if re.match(r'altre? sed',et,re.I): continue
        r=_reg_from_sede('Sede | '+v.split(';')[0]+' [x]')
        if r: return r,'sede'
    return None,None
SECREG={'Valpolicella':'Veneto','Soave e Recioto di Soave':'Veneto','Lessini Durello':'Veneto','Bardolino':'Veneto','Custoza':'Veneto','Colli Euganei':'Veneto','Venezia':'Veneto','Conegliano Valdobbiadene':'Veneto','Asolo Montello':'Veneto','Colli Berici':'Veneto','Gambellara':'Veneto','Breganze':'Veneto','Collio':'Friuli Venezia Giulia','Friuli Colli Orientali e Ramandolo':'Friuli Venezia Giulia','Friuli Grave':'Friuli Venezia Giulia','Friuli DOC':'Friuli Venezia Giulia','Chianti Classico':'Toscana','Brunello di Montalcino':'Toscana','Maremma Toscana':'Toscana','Nobile di Montepulciano':'Toscana','Bolgheri':'Toscana','Chianti Colli Senesi':'Toscana','Valdarno di Sopra':'Toscana','Lugana':'Lombardia','Gutturnio (Colli Piacentini)':'Emilia-Romagna'}
STEMS=['-delle-venezie','-valpolicella','-soave','-durello','-bardolino','-custoza','-prosecco','-euganei','-venezia','-conegliano','-asolo','-collio','-colli-orientali','-friuli-grave','-friuli-doc','-colli-berici','-lugana','-gambellara','-garda','-breganze','-gutturnio','-brunello','-chianti-classico','-bolgheri','-nobile','-maremma','-colli-senesi','-valdarno']
MANUAL=[('tenuta-s-antonio-soave','tenuta-sant-antonio'),('ermacora-delle-venezie','ermacora-colli-orientali'),('valle-aziende-vitivinicole','valle-friuli-doc'),('valle-friuli-doc','valle-aziende-vitivinicole-colli-orientali'),('toffoli-conegliano','azienda-agricola-toffoli-vincenzo-conegliano'),('de-riz-conegliano','azienda-agricola-de-riz-luca-conegliano'),('il-colle-conegliano','azienda-vitivinicola-il-colle-conegliano'),('bortoluzzi-collio','bortoluzzi-borgo-tintor-delle-venezie'),('cantine-riondo-prosecco','cantine-riondo-delle-venezie'),('lorenzonetto-friuli-doc','lorenzonetto-guido-prosecco'),('begali','vini-begali'),('uccelliera-brunello','voliero-brunello'),('ruffino-brunello','ruffino-delle-venezie'),('bottega-brunello','bottega'),('maeli-euganei','maeli-2-euganei')]
PRIMF=['ruffino-delle-venezie','bottega','maeli-2-euganei','uccelliera-brunello']
COMF={'ruffino-delle-venezie':'Pontassieve'}
def comps():
    par={s:s for s in DATI}
    def find(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    for s,f in SPEC.items():
        if s not in DATI: continue
        for m in re.finditer(r'^Altro consorzio \|.*?/pagine/([a-z0-9-]+)\.html',open(f,encoding='utf-8').read(),re.M):
            if m.group(1) in DATI: par[find(s)]=find(m.group(1))
    for a,b in MANUAL:
        if a in DATI and b in DATI: par[find(a)]=find(b)
    c=collections.defaultdict(list)
    for s in DATI: c[find(s)].append(s)
    return list(c.values())
if __name__=='__main__':
    C=comps()
    print('produttori',len(C),'di',len(DATI),'schede')
    nores=0;conf=[]
    for v in C:
        rr={s:reg_scheda(s)[0] or SECREG.get(cerca[s][3]) for s in v if s in cerca}
        vals={x for x in rr.values() if x}
        if not vals: nores+=1
        if len(vals)>1: conf.append((v,rr))
    print('senza regione',nores,'conflitti',len(conf))
    for v,rr in conf: print(rr)
