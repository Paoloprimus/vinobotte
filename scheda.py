# scheda.py <specfile> : spec compatta -> dati/<slug>.json (+ chiarire/<slug>.txt)
# Spec:  dominio: x.it | nome: ... | slug: ...
#  @Titolo sezione   (nota: testo   riga "Etichetta | valore [/pagina/] [C]"   "|| a ; b" elenco   "v | nome | denom | annata"  "? titolo | trovato | domanda")
import sys,re,json,csv,os
Q=os.path.dirname(os.path.abspath(__file__))
BERE_SITI=set(__import__('json').load(open('/home/claude/annuario/bere_siti.json'))) if __import__('os').path.exists('/home/claude/annuario/bere_siti.json') else set()
def run(path):
    L=[l.rstrip('\n') for l in open(path,encoding='utf-8') if l.strip() and not l.startswith('#')]
    meta={};sez=[];chi=[]
    for l in L:
        m=re.match(r'(dominio|nome|slug|consultate): (.*)',l)
        if m and not sez: meta[m.group(1)]=m.group(2).strip();continue
        if l.startswith('@'): sez.append(dict(titolo=l[1:].strip(),righe=[]));continue
        if l.startswith('?'): chi.append([x.strip() for x in l[1:].split('|')]);continue
        s=sez[-1]
        if l.startswith('nota:'): s['nota']=l[5:].strip();continue
        if l.startswith('v |'):
            s['tipo']='vini';a=[x.strip() for x in l[3:].split('|')];s.setdefault('vini',[]).append(dict(nome=a[0],denominazione=a[1] if len(a)>1 else '—',annata=a[2] if len(a)>2 else '—'));continue
        el=None
        if '||' in l: l,e=l.split('||',1);el=[x.strip() for x in e.split(';') if x.strip()]
        a=l.split('|',1);r=dict(etichetta=a[0].strip(),valore=(a[1].strip() if len(a)>1 else '').replace('\\n','\n'))
        if el: r['elenco']=el
        s['righe'].append(r)
    D=meta['dominio'];T=open(f'/home/claude/testi/testi_{D}.txt',encoding='utf-8').read() if D!='-' else ''
    urls=re.findall(r'^===== (\S+)$',T,re.M)
    def risolvi(p):
        c=[u for u in urls if re.sub(r'^https?://[^/]+','',u)==p]
        if not c:
            c=[u for u in urls if re.sub(r'^https?://[^/]+','',u).rstrip('/').endswith(p.rstrip('/'))]
            if len(c)>1: c=[sorted(c,key=len)[0]]
        if not c:
            c=[u for u in urls if re.sub(r'^https?://[^/]+','',u).startswith(p.rstrip('/'))]
            if len({u.rstrip('/') for u in c})>1: c=[]
            c=c[:1]
        if not c: raise SystemExit(f'ERRORE {meta["nome"]}: pagina non salvata {p}')
        return c[0]
    num={};fonti=[]
    def ref(m):
        k=m.group(1)
        if k not in num:
            num[k]=len(num)+1
            if k=='V': fonti.append(dict(n=num[k],testo='Consorzio Vini Venezia, elenco delle cantine associate, consultato il 24 ottobre 2026 (testo copiato dal sito del Consorzio).',url='https://www.consorziovinivenezia.it/cantine-associate/',etichetta='consorziovinivenezia.it'))
            elif k=='E': fonti.append(dict(n=num[k],testo='Consorzio Tutela Vini D.O.C. Colli Euganei, elenco dei produttori, consultato il 24 ottobre 2026 (testo copiato dal sito del Consorzio).',url='https://www.consorziovinieuganei.it/',etichetta='consorziovinieuganei.it'))
            elif k=='P': fonti.append(dict(n=num[k],testo='Consorzio di Tutela della DOC Prosecco, mappa dei produttori, consultata il 24 ottobre 2026 (testo copiato dal sito del Consorzio).',url='https://www.prosecco.wine/produttori/',etichetta='prosecco.wine'))
            elif k=='K': fonti.append(dict(n=num[k],testo='Consorzio Tutela Vino Custoza DOC, elenco dei soci, consultato il 24 ottobre 2026 (testo copiato dal sito del Consorzio).',url='https://www.vinocustoza.it/',etichetta='vinocustoza.it'))
            elif k=='C': fonti.append(dict(n=num[k],testo='Consorzio Tutela Vini Valpolicella, elenco delle aziende del 7 agosto 2026 (PDF).',url='https://www.consorziovalpolicella.it/',etichetta='consorziovalpolicella.it'))
            elif k.startswith('http'):
                if 'ilsoave.com' in k: fonti.append(dict(n=num[k],testo='Consorzio Tutela Vini Soave e Recioto di Soave, '+('elenco dei produttori' if k.rstrip('/').endswith('produttori-soave') else 'scheda del produttore')+', consultato dal vivo il 24 ottobre 2026.',url=k,etichetta='ilsoave.com'))
                elif 'consorziobardolino.it' in k: fonti.append(dict(n=num[k],testo='Consorzio Tutela Vino Bardolino D.O.C., '+('elenco dei produttori' if k.rstrip('/').endswith('/cantine') else 'scheda del produttore')+', consultato dal vivo il 24 ottobre 2026.',url=k,etichetta='consorziobardolino.it'))
                elif 'prosecco.it/it/scheda-cantina' in k: fonti.append(dict(n=num[k],testo='Consorzio di Tutela del Conegliano Valdobbiadene Prosecco DOCG, scheda della cantina, consultata il 24 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='prosecco.it'))
                elif 'asolomontello.it' in k: fonti.append(dict(n=num[k],testo='Consorzio Vini Asolo Montello, elenco dei soci produttori, consultato il 24 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='asolomontello.it'))
                elif 'dellevenezie.it' in k: fonti.append(dict(n=num[k],testo='Consorzio Tutela Vini DOC Delle Venezie, elenco delle cantine associate, consultato il 24 ottobre 2026 (testo copiato dal sito del Consorzio).',url=k,etichetta='dellevenezie.it'))
                elif 'brigaldara.it' in k: fonti.append(dict(n=num[k],testo='Sito ufficiale della cantina, pagina «'+(re.sub(r'^https?://[^/]+/it/?','',k).strip('/') or 'home')+'», testo copiato a mano il 24 ottobre 2026 (il sito vieta la lettura automatica).',url=k,etichetta='brigaldara.it'))
                elif 'emarketstorage.it' in k: fonti.append(dict(n=num[k],testo='Masi Agricola S.p.A., comunicato al mercato con il bilancio consolidato al 31 dicembre 2024, pubblicato su emarketstorage.it (documento della società, non il sito della cantina), consultato il 25 ottobre 2026.',url=k,etichetta='emarketstorage.it'))
                elif 'decanter.com' in k: fonti.append(dict(n=num[k],testo='Decanter, articolo «Cecilia Beretta: the crown jewel of Pasqua wines» (sito di terzi, non della cantina), consultato il 25 ottobre 2026.',url=k,etichetta='decanter.com'))
                elif 'gamberorosso.it' in k: fonti.append(dict(n=num[k],testo='Gambero Rosso, articolo sulla guida Vini d’Italia (sito di terzi, non della cantina), consultato il 25 ottobre 2026.',url=k,etichetta='gamberorosso.it'))
                elif 'gamberorossointernational.com' in k: fonti.append(dict(n=num[k],testo='Gambero Rosso International, articolo «Prosecco Superiore: the 8 best selected by Gambero Rosso» (sito di terzi, non della cantina), consultato il 25 ottobre 2026.',url=k,etichetta='gamberorossointernational.com'))
                elif 'wineindustryadvisor.com' in k: fonti.append(dict(n=num[k],testo='Wine Industry Advisor, articolo «A year of accolades for Le Monde», 3 dicembre 2025 (sito di settore, non della cantina), consultato il 25 ottobre 2026.',url=k,etichetta='wineindustryadvisor.com'))
                elif 'vivino.com' in k: fonti.append(dict(n=num[k],testo='Vivino, pagina del vino (sito di terzi, non della cantina), consultata il 25 ottobre 2026; il punteggio degli utenti cambia nel tempo.',url=k,etichetta='vivino.com'))
                elif 'vitevis.com' in k: fonti.append(dict(n=num[k],testo='Cantine Vitevis Società Cooperativa Agricola, pagina «Cantina Colli Vicentini» (il sito collivicentini.com rimanda a questa pagina), consultata il 25 ottobre 2026.',url=k,etichetta='vitevis.com'))
                elif 'falstaff.com' in k: fonti.append(dict(n=num[k],testo='Falstaff, pagina del vino (sito di terzi, non della cantina), consultata il 25 ottobre 2026.',url=k,etichetta='falstaff.com'))
                elif 'vinicanella.com' in k: fonti.append(dict(n=num[k],testo='Sito ufficiale della cantina (in tedesco), pagine «Az. Agr. Canella», «Weinsortiment» e «Kontakt», testo copiato a mano il 25 ottobre 2026.',url=k,etichetta='vinicanella.com'))
                elif 'bereilvino.it' in k: fonti.append(dict(n=num[k],testo='Bere il Vino, scheda della cantina (sito di terzi, non della cantina), consultata il 25 ottobre 2026.',url=k,etichetta='bereilvino.it'))
                elif 'collio.it' in k: fonti.append(dict(n=num[k],testo='Consorzio Tutela Vini Collio, scheda della cantina nell’elenco dei produttori, consultata il 25 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='collio.it'))
                elif 'colliorientali.com' in k: fonti.append(dict(n=num[k],testo='Consorzio Tutela Vini Friuli Colli Orientali e Ramandolo, scheda della cantina nell’elenco delle aziende associate, consultata il 25 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='colliorientali.com'))
                elif 'docfriuli.eu' in k: fonti.append(dict(n=num[k],testo='Consorzio DOC Friuli, elenco delle aziende e schede delle singole aziende, consultati il 25 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='docfriuli.eu'))
                elif 'consorziobrunellodimontalcino.it' in k: fonti.append(dict(n=num[k],testo='Consorzio del Vino Brunello di Montalcino, scheda della cantina nell’elenco delle aziende associate, consultato il 26 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='consorziobrunellodimontalcino.it'))
                elif 'chianticlassico.com' in k: fonti.append(dict(n=num[k],testo='Consorzio Vino Chianti Classico, scheda dell’azienda nell’elenco delle aziende, consultato il 26 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='chianticlassico.com'))
                elif 'bolgheridoc.com' in k: fonti.append(dict(n=num[k],testo='Consorzio per la Tutela dei Vini DOC Bolgheri e DOC Bolgheri Sassicaia, scheda del consorziato, consultato il 26 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='bolgheridoc.com'))
                elif 'aziendeconsorziovinonobile.it' in k: fonti.append(dict(n=num[k],testo='Consorzio del Vino Nobile di Montepulciano, scheda dell’azienda nell’elenco delle aziende associate, consultato il 26 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='aziendeconsorziovinonobile.it'))
                elif 'aziendevinimaremma.it' in k: fonti.append(dict(n=num[k],testo='Consorzio Tutela Vini della Maremma Toscana, scheda dell’azienda nell’elenco delle aziende, consultato il 26 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='aziendevinimaremma.it'))
                elif 'consorziochianticollisenesi.it' in k: fonti.append(dict(n=num[k],testo='Consorzio Chianti Colli Senesi, elenco delle aziende e dei produttori, consultato il 26 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='consorziochianticollisenesi.it'))
                elif 'valdarnodisopradoc.it' in k: fonti.append(dict(n=num[k],testo='Consorzio Valdarno di Sopra DOC, elenco dei soci nella pagina «Consorzio», consultato il 26 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='valdarnodisopradoc.it'))
                elif 'docfriuligrave.com' in k: fonti.append(dict(n=num[k],testo='Consorzio Tutela Vini DOC Friuli Grave, elenco delle cantine e schede delle singole cantine, consultati il 25 ottobre 2026 (dati copiati dal sito del Consorzio).',url=k,etichetta='docfriuligrave.com'))
                elif 'albinoarmani.com' in k: fonti.append(dict(n=num[k],testo='Sito ufficiale della cantina, pagina «I nostri vini» (negozio) e schede prodotto, testo copiato a mano il 25 ottobre 2026.',url=k,etichetta='albinoarmani.com'))
                elif 'montelliana.it' in k: fonti.append(dict(n=num[k],testo='Sito ufficiale della cantina, pagine «Contatti», «La Cantina» e home, testo copiato a mano il 25 ottobre 2026 (il sito vieta la lettura automatica).',url=k,etichetta='montelliana.it'))
                elif 'collavini.it' in k: fonti.append(dict(n=num[k],testo='Sito ufficiale della cantina, pagine «Contatti», «La Cantina» e home, testo copiato a mano il 25 ottobre 2026 (il sito vieta la lettura automatica).',url=k,etichetta='collavini.it'))
                elif 'fantinel.com' in k: fonti.append(dict(n=num[k],testo='Sito ufficiale della cantina, pagine «Noi», «Prodotti», «Riconoscimenti» e «Contatti», testo copiato a mano il 25 ottobre 2026.',url=k,etichetta='fantinel.com'))
                elif 'venetosecrets.com' in k: fonti.append(dict(n=num[k],testo='Veneto Secrets, pagina «Cantina Quintarelli» (sito di terzi, non della cantina), testo copiato a mano il 24 ottobre 2026.',url=k,etichetta='venetosecrets.com'))
                elif 'montilessini.com' in k: fonti.append(dict(n=num[k],testo='Consorzio Tutela Vino Lessini Durello DOC, '+('elenco dei produttori' if k.rstrip('/').endswith('produttori-vino-durello') else 'scheda del produttore')+', consultato dal vivo il 24 ottobre 2026.',url=k,etichetta='montilessini.com'))
                else: fonti.append(dict(n=num[k],testo='Sito ufficiale della cantina, consultato dal vivo il '+('25' if k in BERE_SITI else '24')+' ottobre 2026, pagina «'+re.sub(r'^https?://(www\.)?','',k).rstrip('/')+'».',url=k,etichetta=re.sub(r'^https?://(www\.)?','',k).split('/')[0]))
            else:
                u=risolvi(k);dom=re.sub(r'^https?://(www\.)?','',u).rstrip('/')
                fonti.append(dict(n=num[k],testo='Sito ufficiale della cantina, '+('home.' if k=='/' else 'pagina «'+k.strip('/')+'».'),url=u,etichetta=dom))
        return f'[[{num[k]}]]'
    pat=re.compile(r'\[(C|K|P|E|V|/[^\]\s]*|https?://[^\]\s]+)\]')
    for s in sez:
        if 'nota' in s: s['nota']=pat.sub(ref,s['nota'])
        for r in s['righe']: r['valore']=pat.sub(ref,r['valore'])
        for v in s.get('vini',[]): v['annata']=pat.sub(ref,v['annata'])
        if s.get('tipo')=='vini' and not s['righe']: del s['righe']
        elif not s['righe']: del s['righe']
    # sezioni senza righe e non vini: errore
    for s in sez:
        if 'righe' not in s and 'vini' not in s: raise SystemExit('sezione vuota '+s['titolo'])
    pass
    out=dict(nome=meta['nome'],slug=meta['slug'],sezioni=sez,
      consultate=meta.get('consultate','Pagine consultate il 24 ottobre 2026 (da copia salvata del sito). Ogni dato della scheda rinvia qui con il numero tra parentesi quadre.'),fonti=fonti)
    json.dump(out,open(f'{Q}/dati/{meta["slug"]}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    if chi:
        with open(f'{Q}/chiarire/{meta["slug"]}.txt','w',encoding='utf-8') as f:
            for c in chi: f.write(' | '.join(c)+'\n')
    print('ok',meta['slug'],len(fonti),'fonti',len(chi),'da chiarire')
run(sys.argv[1])
