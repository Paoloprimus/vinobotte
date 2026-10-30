import glob,re,collections,json,os
os.chdir('/home/claude/annuario')
SP={}
for f in glob.glob('spec/**/*.txt',recursive=True):
    t=open(f,encoding='utf-8').read()
    m=re.search(r'^slug: (\S+)',t,re.M)
    if m: SP[m.group(1)]=(f,t)
PROV={}
for reg,ps in {'Veneto':'VR VI PD TV VE BL RO','Friuli Venezia Giulia':'UD PN GO TS','Toscana':'FI SI GR LI PI AR LU PT PO MS','Lombardia':'BS MI BG CO CR LC LO MN MB PV SO VA','Emilia-Romagna':'PC PR RE MO BO FE RA FC RN','Piemonte':'TO CN AT AL BI NO VB VC','Trentino-Alto Adige':'TN BZ','Lazio':'RM VT LT FR RI','Marche':'AN AP FM MC PU','Umbria':'PG TR','Abruzzo':'AQ CH PE TE','Campania':'NA SA AV BN CE','Puglia':'BA BT BR FG LE TA','Sicilia':'PA CT ME AG CL EN RG SR TP','Sardegna':'CA NU OR SS SU','Liguria':'GE SV IM SP','Valle d\'Aosta':'AO','Basilicata':'PZ MT','Calabria':'CZ CS KR RC VV','Molise':'CB IS'}.items():
    for p in ps.split(): PROV[p]=reg
def sede(t):
    m=re.search(r'^Sede \| (.*?)(?: \[|$)',t,re.M)
    return m.group(1) if m else ''
CAPR={}
for a,b in [(30,32),(35,37),(45,45)]:
    for i in range(a,b+1): CAPR[i]='Veneto'
for i in (33,34): CAPR[i]='Friuli Venezia Giulia'
for i in range(50,60): CAPR[i]='Toscana'
for i in (38,39): CAPR[i]='Trentino-Alto Adige'
for i in list(range(20,28))+[46]: CAPR[i]='Lombardia'
for i in [29]+list(range(40,45))+[47,48]: CAPR[i]='Emilia-Romagna'
for i in list(range(10,16))+[28]: CAPR[i]='Piemonte'
PN={'verona':'Veneto','vicenza':'Veneto','padova':'Veneto','treviso':'Veneto','venezia':'Veneto','belluno':'Veneto','rovigo':'Veneto','udine':'Friuli Venezia Giulia','pordenone':'Friuli Venezia Giulia','gorizia':'Friuli Venezia Giulia','trieste':'Friuli Venezia Giulia'}
def regione(t):
    s=sede(t)
    ps=re.findall(r'\(([A-Z]{2})\)',s)+re.findall(r'\b([A-Z]{2})\s*$',s.strip())+re.findall(r'\s([A-Z]{2})\s+\d{5}\b',s)+re.findall(r'\b\d{5}[^()]*?\b([A-Z]{2})\b',s)
    for p in ps:
        if p in PROV: return PROV[p]
    m=re.search(r'\b(\d{5})\b',s)
    if m and int(m.group(1)[:2]) in CAPR: return CAPR[int(m.group(1)[:2])]
    for k,v in PN.items():
        if re.search(r'\('+k+r'\)',s,re.I): return v
    return None
if __name__=='__main__':
    n=0;r=collections.Counter()
    for s,(f,t) in SP.items():
        g=regione(t); r[g]+=1
    print(r)
