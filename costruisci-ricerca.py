# Legge dati/*.json e scrive valpolicella/index.html (ricerca statica nel browser).
import json,glob,re,os,csv
rows=list(csv.reader(open('/home/claude/out/elenco_consorzio_pulito.csv',encoding='utf-8-sig'),delimiter=';'))[1:]
POR_DOM={};POR_NOME={}
for r in rows:
    r=(r+['']*9)[:9]
    com=r[3].replace('\u2019',"'").replace(' In ',' in ').replace("D'Alpone","d'Alpone").replace('Negrar in Valpolicella','Negrar di Valpolicella').replace('in colle','in Colle').strip()
    if r[6]: POR_DOM[r[6]]=com
    POR_NOME[r[0]]=com
SLUG_DOM={}
for f in glob.glob('spec/*.txt'):
    t=open(f,encoding='utf-8').read()
    m=re.search(r'^slug: (\S+)',t,re.M);d=re.search(r'^dominio: (\S+)',t,re.M)
    if m and d: SLUG_DOM[m.group(1)]=d.group(1)

FRAZ={'Costalunga di Monteforte d\'Alpone':'Monteforte d\'Alpone','Brognoligo di Monteforte d\'Alpone':'Monteforte d\'Alpone','Castelcerino di Soave':'Soave','Cellore d\'Illasi':'Illasi','Terrossa di Roncà':'Roncà','San Martino Buon Albergo':'San Martino Buon Albergo','Pedemonte di Valpolicella':'San Pietro in Cariano','Arbizzano-Santa Maria':'Negrar di Valpolicella','Arbizzano di Negrar':'Negrar di Valpolicella','Arbizzano':'Negrar di Valpolicella','Palazzolo di Sona':'Sona','San Pietro In Cariano':'San Pietro in Cariano'}
FVG=set(open('fvg-prosecco.txt',encoding='utf-8').read().split())
SUFALL=['-soave.json','-durello.json','-bardolino.json','-custoza.json','-prosecco.json','-euganei.json','-venezia.json','-conegliano.json','-asolo.json','-delle-venezie.json','-collio.json','-colli-orientali.json','-friuli-grave.json','-friuli-doc.json','-colli-berici.json','-lugana.json','-gambellara.json','-garda.json','-breganze.json','-gutturnio.json']+['-%s.json'%x for x in ['brunello','chianti-classico','bolgheri','nobile','maremma','colli-senesi','valdarno']]
OV=json.load(open('/home/claude/annuario/bere_overlay.json',encoding='utf-8'))
_T=json.load(open('/home/claude/annuario/tosc_overlay.json',encoding='utf-8'))
OV['comuni'].update(_T['comuni']);OV['den'].update(_T['den'])
def costruisci(sez):
    sezr=sez
    if sez=='prosecco-fvg': sez='prosecco'
    soave=(sez=='soave');durello=(sez=='durello');bard=(sez=='bardolino');cust=(sez=='custoza');pros=(sez=='prosecco');eug=(sez=='euganei');ven=(sez=='venezia');con=(sez=='conegliano');aso=(sez=='asolo');dve=(sez=='venezie');col=(sez=='collio');cor=(sez=='colli-orientali');gra=(sez=='friuli-grave');fdo=(sez=='friuli-doc')
    suf={'valpolicella':None,'soave':'-soave.json','durello':'-durello.json','bardolino':'-bardolino.json','custoza':'-custoza.json','prosecco':'-prosecco.json','euganei':'-euganei.json','venezia':'-venezia.json','conegliano':'-conegliano.json','asolo':'-asolo.json','venezie':'-delle-venezie.json','collio':'-collio.json','colli-orientali':'-colli-orientali.json','friuli-grave':'-friuli-grave.json','friuli-doc':'-friuli-doc.json','colli-berici':'-colli-berici.json','lugana':'-lugana.json','gambellara':'-gambellara.json','garda':'-garda.json','breganze':'-breganze.json','gutturnio':'-gutturnio.json'}.get(sez) if sez in ('valpolicella','soave','durello','bardolino','custoza','prosecco','euganei','venezia','conegliano','asolo','venezie','collio','colli-orientali','friuli-grave','friuli-doc','colli-berici','lugana','gambellara','garda','breganze','gutturnio') else '-'+sez+'.json'
    voci=[]
    def inSez(x):
        if sezr=='prosecco-fvg': return os.path.basename(x)[:-5] in FVG
        if sezr=='prosecco': return x.endswith(suf) and os.path.basename(x)[:-5] not in FVG
        if suf: return x.endswith(suf)
        return not any(x.endswith(t) for t in SUFALL)
    for f in sorted(x for x in glob.glob('dati/*.json') if inSez(x)):
        c=json.load(open(f,encoding='utf-8'))
        comune='';den=set()
        for s in c['sezioni']:
            for r in s.get('righe',[]):
                if r['etichetta'].lower().startswith('sede') and not comune:
                    v=re.sub(r'\[\[\d+\]\]','',r['valore'])
                    m=re.search(r'\b\d{5}\s+([^()\[;,]+?)\s*(?:\(|;|$|\n)',v)
                    if m: comune=m.group(1).strip()
                    elif soave or durello or bard:
                        m2=re.search(r',\s*([^,()\[]+?)\s*\(',v)
                        if m2: comune=m2.group(1).strip()
            if bard:
                for r in s.get('righe',[]):
                    if r['etichetta'].startswith('Denominazioni Bardolino'):
                        dd=re.sub(r'\[\[\d+\]\]','',r['valore']).lower()
                        if 'chiaretto' in dd: den.add('Chiaretto di Bardolino')
                        if re.search(r'(?<!chiaretto di )bardolino (classico )?(superiore|novello)?',dd) and re.search(r'(?:^|; )bardolino',dd): den.add('Bardolino')
                        if 'superiore' in dd: den.add('Bardolino Superiore')
            for v in s.get('vini',[]):
                d=v['denominazione'].lower()
                if durello:
                    if 'durello' in d or 'monti lessini' in d: den.add('Lessini Durello')
                    elif 'gambellara' in d: den.add('Lessini Durello')
                    continue
                if soave:
                    if 'recioto' in d: den.add('Recioto di Soave')
                    elif 'superiore' in d: den.add('Soave Superiore')
                    elif 'classico' in d: den.add('Soave Classico')
                    elif 'soave' in d: den.add('Soave')
                    continue
                if 'amarone' in d: den.add('Amarone')
                if 'ripasso' in d: den.add('Ripasso')
                if 'recioto' in d: den.add('Recioto')
                if re.search(r'valpolicella',d) and 'amarone' not in d and 'ripasso' not in d and 'recioto' not in d: den.add('Valpolicella')
        comune=comune.replace('’',"'")
        sede_c=comune
        rs=''
        for sec in c['sezioni']:
            for r in sec.get('righe',[]):
                if r['etichetta']=='Ragione sociale': rs=re.sub(r'\[\[\d+\]\]','',r['valore'])
        cc=POR_DOM.get(SLUG_DOM.get(c['slug'],''))
        if not cc and SLUG_DOM.get(c['slug'],'-')!='-':
            for nome,com in POR_NOME.items():
                if nome and nome in rs: cc=com;break
        if cc and not sede_c: comune=cc
        for a,b in FRAZ.items():
            if comune==a: comune=b
        if bard:
            cm=json.load(open('/home/claude/bardolino/comuni.json',encoding='utf-8')).get(c['slug'])
            if cm:
                cm=re.sub(r' VR$','',cm).replace('Custoza di Sommacampagna','Sommacampagna')
                if cm=='Negrar': cm='Negrar di Valpolicella'
                comune=cm
        if cust:
            cm=json.load(open('/home/claude/custoza/comuni.json',encoding='utf-8')).get(c['slug'])
            if cm: comune=cm
            den={'Custoza'}
        if pros:
            if re.fullmatch(r'[A-Za-z]{2}',comune): comune=''
            cm=json.load(open('/home/claude/prosecco/comuni.json',encoding='utf-8')).get(c['slug'])
            if cm: comune=cm
            den={'Prosecco DOC'}
        if eug:
            cm=json.load(open('/home/claude/euganei/comuni.json',encoding='utf-8')).get(c['slug'])
            if cm: comune=cm
            den={'Colli Euganei'}
        if ven:
            cm=json.load(open('/home/claude/venezia/comuni.json',encoding='utf-8')).get(c['slug'])
            if cm: comune=cm
            den=set(json.load(open('/home/claude/venezia/den.json',encoding='utf-8')).get(c['slug'],[]))
        if con:
            cm=json.load(open('/home/claude/conegliano/comuni.json',encoding='utf-8')).get(c['slug'])
            if cm: comune=cm
            den=set(json.load(open('/home/claude/conegliano/den.json',encoding='utf-8')).get(c['slug'],[]))
        if aso:
            cm=json.load(open('/home/claude/asolo/comuni.json',encoding='utf-8')).get(c['slug'])
            if cm: comune=cm
            den={'Asolo Montello'}
        if fdo:
            cm=json.load(open('/home/claude/annuario/friuli-doc/comuni.json',encoding='utf-8')).get(c['slug'][:-len('-friuli-doc')])
            if cm: comune=cm
            den={'Friuli DOC'}
        if gra:
            cm=json.load(open('/home/claude/annuario/friuli-grave/comuni.json',encoding='utf-8')).get(c['slug'][:-len('-friuli-grave')])
            if cm: comune=cm
            den={'Friuli Grave'}
        if cor:
            cm=json.load(open('/home/claude/annuario/colli-orientali/comuni.json',encoding='utf-8')).get(c['slug'][:-len('-colli-orientali')])
            if cm: comune=cm
            den=set(x.split(' ',1)[1] if False else x for x in json.load(open('/home/claude/annuario/colli-orientali/den.json',encoding='utf-8')).get(c['slug'],[]))
        if col:
            cm=json.load(open('/home/claude/annuario/collio/comuni.json',encoding='utf-8')).get(c['slug'][:-7])
            if cm: comune=cm
            den={'Collio'}
        if dve:
            cm=json.load(open('/home/claude/venezie/comuni.json',encoding='utf-8')).get(c['slug'])
            if cm:
                cm=re.split(r'\s*[,(–-]\s*',cm)[0].strip()
                cm=' '.join(w if i==0 or w.lower() not in ('di','del','della','al','sul','in','e','d') else w.lower() for i,w in enumerate(cm.title().split()))
                cm=cm.replace('’',"'")
                while len(cm.split())>1 and re.fullmatch(r'[A-Za-z]{2}|Udine|Italia|Vicenza|Verona|Belluno',cm.split()[-1]): cm=' '.join(cm.split()[:-1])
                cm=re.sub(r"D'A",lambda m:"d'A",cm)
                if cm.upper() in ('UD','VI','TV','PN','PD'): cm=''
                comune=cm
            if len(comune)<=2 or comune.upper() in ('UD','VI','TV','PN','PD'): comune=''
            den={'Delle Venezie'}
        if c['slug'] in OV['comuni']:
            if OV['comuni'][c['slug']]: comune=OV['comuni'][c['slug']]
            den=set(OV['den'][c['slug']])
        voci.append(dict(n=c['nome'],s=c['slug'],c=comune,d=sorted(den)))
    return voci

ALL=[]
SEZN={}
def scrivi(sez,titolo,opzioni):
    global COUNT
    voci=costruisci(sez)
    SEZN[sez]=len(voci)
    voci.sort(key=lambda x:x['n'].lower())
    for v in voci:
        try:
            pf='pagine/'+v['s']+'.html'
            if os.path.exists(pf):
                ph=open(pf,encoding='utf-8').read()
                ph=re.sub(r'<meta name="vb-sez"[^>]*>\n?','',ph)
                ph=ph.replace('</head>','<meta name="vb-sez" content="'+sez+'">\n</head>',1)
                open(pf,'w',encoding='utf-8').write(ph)
        except Exception: pass
        try:
            dj=json.load(open('dati/'+v['s']+'.json',encoding='utf-8'))
            vv=sorted({(x['nome']+' '+x['denominazione']) for sz in dj['sezioni'] for x in sz.get('vini',[])})
        except Exception: vv=[]
        ALL.append([v['n'],v['s'],v['c'] or '',titolo.replace('Produttori vini ',''),' · '.join(v['d']),'; '.join(vv)[:300],'Friuli Venezia Giulia' if sez in ('prosecco-fvg','collio','colli-orientali','friuli-grave','friuli-doc') else {'lugana':'Lombardia','gutturnio':'Emilia-Romagna','brunello':'Toscana','chianti-classico':'Toscana','bolgheri':'Toscana','nobile':'Toscana','maremma':'Toscana','colli-senesi':'Toscana','valdarno':'Toscana'}.get(sez,'Veneto')])
    dati=json.dumps(voci,ensure_ascii=False,separators=(',',':'))
    html='''<!doctype html>
    <html lang="it">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>'''+titolo+''' — VinoBotte</title>
    <style>
    :root{--bg:#faf8f4;--ink:#1d1b19;--line:#d9d3c8;--acc:#7a1f2b}
    @media (prefers-color-scheme:dark){:root{--bg:#171513;--ink:#f1ece4;--line:#3a352f;--acc:#e08a96}}
    *{box-sizing:border-box}
    body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.45 Georgia,'Times New Roman',serif}
    main{max-width:720px;margin:0 auto;padding:20px 16px 48px}
    a{color:var(--acc)}
    .top a{text-decoration:none;font-weight:700}
    h1{font-size:clamp(26px,7vw,32px);line-height:1.15;margin:14px 0 14px}
    .filtri{display:grid;grid-template-columns:2fr 1fr 1fr;gap:8px;margin-bottom:10px}
    input,select{font:inherit;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:8px;width:100%}
    #n{color:var(--ink);margin:6px 0;font-size:14px}
    ul{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
    li{border-bottom:1px solid var(--line)}
    li a{display:grid;grid-template-columns:1fr auto;gap:2px 12px;padding:10px 2px;text-decoration:none;color:inherit}
    li a:hover .nm,li a:focus-visible .nm{text-decoration:underline}
    .nm{color:var(--acc);font-weight:700}
    .sub{font-size:14px;grid-column:1 / -1}
    @media (max-width:560px){.filtri{grid-template-columns:1fr}}
    </style>
    </head>
    <body>
    <main>
    <h1>'''+titolo+'''</h1>
    <div class="filtri">
    <input id="q" type="search" placeholder="Nome cantina" aria-label="Nome cantina">
    <select id="c" aria-label="Comune"><option value="">Tutti i comuni</option></select>
    <select id="d" aria-label="Denominazione"><option value="">Tutte le denominazioni</option>'''+opzioni+'''</select>
    </div>
    <div id="n" role="status"></div>
    <ul id="l"></ul>
    </main>
    <script>
    const D=__DATI__;
    const q=document.getElementById('q'),c=document.getElementById('c'),d=document.getElementById('d'),l=document.getElementById('l'),n=document.getElementById('n');
    [...new Set(D.map(x=>x.c).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'it')).forEach(x=>{const o=document.createElement('option');o.textContent=x;c.appendChild(o)});
    const norm=s=>s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
    function esc(s){return s.replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]))}
    function mostra(){
     const t=norm(q.value.trim());
     const r=D.filter(x=>(!t||norm(x.n).includes(t))&&(!c.value||x.c===c.value)&&(!d.value||x.d.includes(d.value)));
     n.textContent=r.length+(r.length===1?' cantina':' cantine');
     l.innerHTML=r.map(x=>'<li><a href="/pagine/'+x.s+'.html"><span class="nm">'+esc(x.n)+'</span><span>'+esc(x.c)+'</span><span class="sub">'+esc(x.d.join(' · '))+'</span></a></li>').join('');
    }
    [q,c,d].forEach(e=>e.addEventListener('input',mostra));
    mostra();
    </script>
    <script src="/shell.js" defer></script>
    </body>
    </html>
    '''.replace('__DATI__',dati)
    os.makedirs(sez,exist_ok=True)
    open(sez+'/index.html','w',encoding='utf-8').write(html)
    print(len(voci),'cantine;',sum(1 for v in voci if not v['c']),'senza comune;',sum(1 for v in voci if not v['d']),'senza denominazioni')

scrivi('valpolicella','Produttori vini Valpolicella','<option>Amarone</option><option>Ripasso</option><option>Recioto</option><option>Valpolicella</option>')
scrivi('soave','Produttori vini Soave e Recioto di Soave','<option>Soave</option><option>Soave Classico</option><option>Soave Superiore</option><option>Recioto di Soave</option>')
scrivi('durello','Produttori vini Lessini Durello','<option>Lessini Durello</option>')
scrivi('bardolino','Produttori vini Bardolino','<option>Bardolino</option><option>Bardolino Superiore</option><option>Chiaretto di Bardolino</option>')
scrivi('custoza','Produttori vini Custoza','<option>Custoza</option>')
scrivi('prosecco','Produttori vini Prosecco DOC','<option>Prosecco DOC</option>')
scrivi('prosecco-fvg','Produttori vini Prosecco DOC','<option>Prosecco DOC</option>')
scrivi('euganei','Produttori vini Colli Euganei','<option>Colli Euganei</option>')
scrivi('venezia','Produttori vini Venezia','<option>Venezia</option><option>Lison Pramaggiore</option><option>Lison</option><option>Piave</option><option>Malanotte</option>')
scrivi('conegliano','Produttori vini Conegliano Valdobbiadene','<option>Conegliano Valdobbiadene Prosecco Superiore</option><option>Valdobbiadene Superiore di Cartizze</option><option>Conegliano Valdobbiadene Prosecco</option>')
scrivi('asolo','Produttori vini Asolo Montello','<option>Asolo Montello</option>')
scrivi('collio','Produttori vini Collio','<option>Collio</option>')
scrivi('colli-orientali','Produttori vini Friuli Colli Orientali e Ramandolo','<option>DOC Friuli Colli Orientali</option><option>DOCG Colli Orientali del Friuli Picolit</option><option>DOCG Ramandolo</option><option>DOCG Rosazzo</option>')
scrivi('friuli-grave','Produttori vini Friuli Grave','<option>Friuli Grave</option>')
scrivi('friuli-doc','Produttori vini Friuli DOC','<option>Friuli DOC</option>')
scrivi('colli-berici','Produttori vini Colli Berici','<option>Colli Berici</option>')
scrivi('gambellara','Produttori vini Gambellara','<option>Gambellara</option>')
scrivi('garda','Produttori vini Garda DOC','<option>Garda</option>')
scrivi('breganze','Produttori vini Breganze','<option>Breganze</option>')
scrivi('lugana','Produttori vini Lugana','<option>Lugana</option>')
scrivi('gutturnio','Produttori vini Gutturnio (Colli Piacentini)','<option>Gutturnio</option>')
scrivi('brunello','Produttori vini Brunello di Montalcino','<option>Brunello di Montalcino</option><option>Rosso di Montalcino</option><option>Sant'+"'"+'Antimo</option>')
scrivi('chianti-classico','Produttori vini Chianti Classico','<option>Chianti Classico</option>')
scrivi('bolgheri','Produttori vini Bolgheri','<option>Bolgheri</option>')
scrivi('nobile','Produttori vini Nobile di Montepulciano','<option>Vino Nobile di Montepulciano</option>')
scrivi('maremma','Produttori vini Maremma Toscana','<option>Maremma Toscana</option>')
scrivi('colli-senesi','Produttori vini Chianti Colli Senesi','<option>Chianti Colli Senesi</option>')
scrivi('valdarno','Produttori vini Valdarno di Sopra','<option>Valdarno di Sopra</option>')
scrivi('venezie','Produttori vini Delle Venezie','<option>Delle Venezie</option>')
json.dump(ALL,open('cerca.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(len(ALL),'voci in cerca.json')

# conteggio produttori sotto il nome di ogni regione (home e pagine regionali)
_cnt={}
for _v in ALL: _cnt[_v[6]]=_cnt.get(_v[6],0)+1
_pag={'Lombardia':('index.html','lombardia/index.html','/lombardia/'),'Emilia-Romagna':('index.html','emilia-romagna/index.html','/emilia-romagna/'),'Veneto':('index.html','veneto/index.html','/veneto/'),'Friuli Venezia Giulia':('index.html','friuli-venezia-giulia/index.html','/friuli-venezia-giulia/'),'Toscana':('index.html','toscana/index.html','/toscana/')}
_css='.num{margin:-16px 0 22px;font-size:13px;color:var(--ink);opacity:.75;text-align:center;letter-spacing:.02em}'
for _r,(_h,_p,_href) in _pag.items():
    _n=_cnt.get(_r,0);_t='<p class="num">'+format(_n,',').replace(',','.')+' produttori</p>'
    _s=open(_h,encoding='utf-8').read()
    _s=re.sub(r'(<h2 class="reg"><a href="'+re.escape(_href)+r'">[^<]*</a></h2>)(\n<p class="num">[^<]*</p>)?',lambda m:m.group(1)+'\n'+_t,_s,1)
    if '.num{' not in _s: _s=_s.replace('</style>',_css.replace('-16px 0 22px','-4px 0 10px')+'\n</style>',1)
    open(_h,'w',encoding='utf-8').write(_s)
    _s=open(_p,encoding='utf-8').read()
    _s=re.sub(r'(<h1 class="reg">[^<]*</h1>)(\n<p class="num">[^<]*</p>)?',lambda m:m.group(1)+'\n'+_t,_s,1)
    if '.num{' not in _s: _s=_s.replace('</style>',_css+'\n</style>',1)
    open(_p,'w',encoding='utf-8').write(_s)
print('conteggi',_cnt)

# conteggio produttori sotto ogni tipo di vino (tessere delle pagine regionali)
for _p in ('veneto/index.html','friuli-venezia-giulia/index.html','lombardia/index.html','emilia-romagna/index.html','toscana/index.html'):
    _s=open(_p,encoding='utf-8').read()
    def _r(m):
        k=m.group(1).strip('/')
        if k not in SEZN: return m.group(0)
        return '<a class="vai" href="'+m.group(1)+'">'+m.group(2)+'<small>'+format(SEZN[k],',').replace(',','.')+' produttori</small></a>'
    _s=re.sub(r'<a class="vai" href="(/[a-z-]+/)">(.*?)(?:<small>[^<]*</small>)?</a>',_r,_s)
    if 'a.vai small' not in _s:
        _s=_s.replace('</style>','a.vai{flex-direction:column}\na.vai small{display:block;margin-top:4px;font-size:13px;color:var(--ink);opacity:.75}\n</style>',1)
    open(_p,'w',encoding='utf-8').write(_s)
print('tipi',SEZN)
