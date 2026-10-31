# Costruisce le pagine per REGIONE: un produttore = una scheda, nella regione della sede.
# Tessere = (tipo di vino, regione). Legge produttori.json e dati/*.json.
import json,re,os,glob,collections,unicodedata
os.chdir('/home/claude/annuario')
PROD=json.load(open('produttori.json',encoding='utf-8'))
TIT=json.load(open('rifusione/tit.json',encoding='utf-8'))
TPL=open('rifusione/template.html',encoding='utf-8').read()
ORDER=[k for k in TIT if k!='prosecco-fvg']
REGORD=['Veneto','Friuli Venezia Giulia','Toscana','Lombardia','Piemonte','Emilia-Romagna','Trentino-Alto Adige','Puglia']
RSLUG={'Friuli Venezia Giulia':'friuli-venezia-giulia'}
def rs(r): return RSLUG.get(r) or re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFD',r.lower()).encode('ascii','ignore').decode()).strip('-')
RSHORT={'Friuli Venezia Giulia':'fvg'}
def rshort(r): return RSHORT.get(r) or rs(r)
# regioni e conteggi per tipo
G=collections.defaultdict(list)
for p in PROD:
    if not p['regione']: continue
    for t,den in p['tipi'].items():
        G[(t,p['regione'])].append(dict(n=p['nome'],s=p['slug'],c=p['comune'] or '',d=sorted(den)))
primreg={}
for t in ORDER:
    c=collections.Counter({r:len(v) for (tt,r),v in G.items() if tt==t})
    if c: primreg[t]=c.most_common(1)[0][0]
def chiave(t,r):
    if r==primreg[t]: return t
    return t+'-'+rshort(r)
PAGES={}   # key -> (tipo, regione)
for (t,r),v in G.items(): PAGES[chiave(t,r)]=(t,r)
def scrivi(key,tipo,reg,voci):
    titolo,opz=TIT[tipo]
    voci.sort(key=lambda x:x['n'].lower())
    dati=json.dumps(voci,ensure_ascii=False,separators=(',',':'))
    html=TPL.replace('@@TIT@@',titolo).replace('@@OPZ@@',opz).replace('__DATI__',dati)
    os.makedirs(key,exist_ok=True)
    open(key+'/index.html','w',encoding='utf-8').write(html)
for key,(t,r) in PAGES.items(): scrivi(key,t,r,G[(t,r)])
# meta regione nelle pagine scheda + cerca.json
ALL=[]
conta=collections.Counter()
for p in PROD:
    if not p['regione']: continue
    conta[p['regione']]+=1
    pf='pagine/'+p['slug']+'.html'
    if os.path.exists(pf):
        ph=open(pf,encoding='utf-8').read()
        ph=re.sub(r'<meta name="vb-sez"[^>]*>\n?','',ph)
        ph=ph.replace('</head>','<meta name="vb-sez" content="'+rs(p['regione'])+'">\n</head>',1)
        open(pf,'w',encoding='utf-8').write(ph)
    dj=json.load(open('dati/'+p['slug']+'.json',encoding='utf-8'))
    vv=sorted({(x['nome']+' '+x['denominazione']) for sz in dj['sezioni'] for x in sz.get('vini',[])})
    tit=' · '.join(TIT[t][0].replace('Produttori vini ','') for t in p['tipi'])
    den=' · '.join(sorted({d for v in p['tipi'].values() for d in v}))
    ALL.append([p['nome'],p['slug'],p['comune'] or '',tit,den,'; '.join(vv)[:300],p['regione']])
json.dump(ALL,open('cerca.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(len(ALL),'voci in cerca.json',dict(conta))
# pagine regionali
CSS='''<style>
:root{--bg:#faf8f4;--ink:#1d1b19;--line:#d9d3c8;--acc:#7a1f2b}
@media (prefers-color-scheme:dark){:root{--bg:#171513;--ink:#f1ece4;--line:#3a352f;--acc:#e08a96}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.45 Georgia,'Times New Roman',serif;padding:24px 16px 56px}
main{max-width:1080px;margin:0 auto}
.top a{color:var(--acc);text-decoration:none;font-weight:700}
h1.reg{margin:18px 0 26px;font-size:28px;font-weight:400;font-variant:small-caps;letter-spacing:.14em;color:var(--acc);text-align:center}
.griglia{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media (max-width:900px){.griglia{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.griglia{grid-template-columns:1fr}}
a.vai{display:flex;align-items:center;justify-content:center;text-align:center;min-height:56px;padding:10px 12px;font-size:19px;color:var(--acc);text-decoration:none}
a.vai:hover,a.vai:focus-visible{text-decoration:underline}
.num{margin:-16px 0 22px;font-size:13px;color:var(--ink);opacity:.75;text-align:center;letter-spacing:.02em}
a.vai{flex-direction:column}
a.vai small{display:block;margin-top:4px;font-size:13px;color:var(--ink);opacity:.75}
</style>'''
def fmt(n): return format(n,',').replace(',','.')
NAV=[]
for r in REGORD+[x for x in conta if x not in REGORD]:
    if not conta.get(r): continue
    tiles=[]
    for t in ORDER:
        k=chiave(t,r) if t in primreg else None
        if k in PAGES and PAGES[k]==(t,r):
            tiles.append((k,TIT[t][0].replace('Produttori vini ',''),len(G[(t,r)])))
    tiles.sort(key=lambda x:PAGES[x[0]][1]!=primreg[PAGES[x[0]][0]])
    h='<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>'+r+' — VinoBotte</title>\n'+CSS+'\n</head>\n<body>\n<main>\n<h1 class="reg">'+r+'</h1>\n<p class="num">'+fmt(conta[r])+' produttori</p>\n<div class="griglia">\n'
    h+=''.join('<a class="vai" href="/%s/">%s<small>%s produttori</small></a>\n'%(k,n,fmt(c)) for k,n,c in tiles)
    h+='</div>\n</main>\n<script src="/shell.js" defer></script>\n</body>\n</html>\n'
    os.makedirs(rs(r),exist_ok=True)
    open(rs(r)+'/index.html','w',encoding='utf-8').write(h)
    NAV.append(dict(n=r,h='/'+rs(r)+'/',t=[[n,'/'+k+'/'] for k,n,c in tiles]))
# home
home=open('index.html',encoding='utf-8').read()
sec=''.join('<section class="regione">\n<h2 class="reg"><a href="/%s/">%s</a></h2>\n<p class="num">%s produttori</p>\n</section>\n'%(rs(r),r,fmt(conta[r])) for r in sorted([x for x in conta if conta.get(x)],key=lambda x:(-conta[x],x)))
tot='<h1 class="tot">In <span class="cap">I</span>talia ci sono %d produttori di vini DOP</h1>\n'%sum(conta.values())
home=re.sub(r'(<div class="griglia" id="griglia">\n).*?(</div>\n</main>)',lambda m:m.group(1)+tot+sec+m.group(2),home,1,flags=re.S)
home=re.sub(r'\.griglia \.tot\{[^}]*\}\n(\.griglia \.tot2\{[^}]*\}\n)?','',home)
home=home.replace('.griglia .regione{width:calc(25% - 18px)','.griglia .tot{width:100%;margin:6px 0 10px;text-align:center;font-size:20px;font-weight:400;font-variant:all-small-caps;color:var(--acc);letter-spacing:.09em}\n.griglia .tot::before,.griglia .tot::after{content:"";display:block;width:64px;height:1px;margin:0 auto;background:var(--acc);opacity:.35}\n.griglia .tot .cap{font-variant:normal}\n.griglia .tot::before{margin-bottom:12px}\n.griglia .tot::after{margin-top:12px}\n.griglia .tot2{width:100%;margin:-22px 0 4px;text-align:center;font-size:17px;color:var(--ink);opacity:.8;letter-spacing:.03em}\n.griglia .regione{width:calc(25% - 18px)',1)
open('index.html','w',encoding='utf-8').write(home)
# shell.js: menu, breadcrumb
sh=open('shell.js',encoding='utf-8').read()
navjs=json.dumps(NAV,ensure_ascii=False,separators=(',',':'))
sh=re.sub(r'^var (?:SEZ|NAV)=.*$','var NAV='+navjs.replace('\\','\\\\')+';',sh,1,flags=re.M)
menu="pm.innerHTML='<button class=\"sh-b x\" data-chiudi>✕</button><h2>Menu</h2><a href=\"/\">Home</a>'+NAV.map(function(r){return '<a href=\"'+r.h+'\">'+r.n+'</a><div class=\"sub\">'+r.t.map(function(x){return '<a href=\"'+x[1]+'\">'+x[0]+'</a>'}).join('')+'</div>'}).join('');"
sh=re.sub(r"^pm\.innerHTML='.*$",lambda m:menu,sh,1,flags=re.M)
a=sh.index(" var REG=") if " var REG=" in sh else sh.index(" var h1=");b=sh.index(" if(tr){")
bc=''' var h1=document.querySelector('h1'),nome=h1?h1.textContent.trim():document.title.split(' — ')[0];
 var RMAP={},TMAP={};NAV.forEach(function(r){RMAP[r.h]=r;r.t.forEach(function(x){TMAP[x[1]]=[r,x[0]]})});
 if(p==='/'||p==='')tr=null;
 else if(RMAP[p])tr.push([RMAP[p].n]);
 else if(TMAP[p]){tr.push([TMAP[p][0].n,TMAP[p][0].h]);tr.push([TMAP[p][1]]);}
 else if(p.indexOf('/pagine/')===0){
  var mt=document.querySelector('meta[name=vb-sez]'),k=mt&&('/'+mt.content+'/');
  if(k&&RMAP[k])tr.push([RMAP[k].n,k]);
  tr.push([nome]);
 } else tr.push([nome]);
'''
sh=sh[:a]+bc+sh[b:]
open('shell.js','w',encoding='utf-8').write(sh)
# elenco directory da pubblicare
json.dump(sorted(set(list(PAGES)+[rs(r) for r in conta])),open('rifusione/dirs.json','w'))
print('pagine tipo',len(PAGES));
for r in conta: print(r,[(k,len(G[PAGES[k]])) for k in PAGES if PAGES[k][1]==r])
