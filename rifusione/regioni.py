import sys,os,json,collections
sys.path.insert(0,'/home/claude/annuario/rifusione')
from analisi import *
cerca=json.load(open('cerca.json',encoding='utf-8'))
COMS={c[1]:c[2] for c in cerca}
SECREG={'Valpolicella':'Veneto','Soave e Recioto di Soave':'Veneto','Lessini Durello':'Veneto','Bardolino':'Veneto','Custoza':'Veneto','Colli Euganei':'Veneto','Venezia':'Veneto','Conegliano Valdobbiadene':'Veneto','Asolo Montello':'Veneto','Colli Berici':'Veneto','Gambellara':'Veneto','Breganze':'Veneto','Collio':'Friuli Venezia Giulia','Friuli Colli Orientali e Ramandolo':'Friuli Venezia Giulia','Friuli Grave':'Friuli Venezia Giulia','Friuli DOC':'Friuli Venezia Giulia','Chianti Classico':'Toscana','Brunello di Montalcino':'Toscana','Maremma Toscana':'Toscana','Nobile di Montepulciano':'Toscana','Bolgheri':'Toscana','Chianti Colli Senesi':'Toscana','Valdarno di Sopra':'Toscana','Lugana':'Lombardia','Gutturnio (Colli Piacentini)':'Emilia-Romagna'}
CER={c[1]:c for c in cerca}
# regione per scheda
reg={};why={}
for s,(f,t) in SP.items():
    r=regione(t)
    if r: reg[s]=r;why[s]='sede'
# comune -> regione (dalle risolte)
cr=collections.defaultdict(collections.Counter)
for s,r in reg.items():
    c=COMS.get(s)
    if c: cr[c][r]+=1
for s in SP:
    if s in reg: continue
    c=COMS.get(s)
    if c and c in cr: reg[s]=cr[c].most_common(1)[0][0];why[s]='comune'
for s in SP:
    if s in reg: continue
    sec=CER[s][3] if s in CER else None
    if sec in SECREG: reg[s]=SECREG[sec];why[s]='sezione'
# componenti
par={s:s for s in SP}
def find(x):
    while par[x]!=x: par[x]=par[par[x]];x=par[x]
    return x
for s,(f,t) in SP.items():
    for m in re.finditer(r'^Altro consorzio \|.*?/pagine/([a-z0-9-]+)\.html',t,re.M):
        if m.group(1) in SP: par[find(s)]=find(m.group(1))
comp=collections.defaultdict(list)
for s in SP: comp[find(s)].append(s)
if __name__=='__main__':
    print(collections.Counter(why.values()), 'senza regione',[s for s in SP if s not in reg][:10], sum(1 for s in SP if s not in reg))
    conf=[]
    for k,v in comp.items():
        rs={reg.get(s) for s in v}
        if len(rs)>1: conf.append(v)
    print('produttori con schede in regioni diverse',len(conf))
    for v in conf[:60]: print([ (s[:28],reg.get(s),why.get(s)) for s in v])
