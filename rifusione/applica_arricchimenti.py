import json,re,os,sys
R=os.path.dirname(os.path.abspath(__file__))+'/..'
SENT={'ROBOTS','REDIR','ERR','SKIP','DUP','SPAM','DUBBIO','-',''}
GEN={'azienda','agricola','agricole','fattoria','tenuta','societa','società','soc','cantina','cantine','podere','vini','vino','casa','vinicola','srl','spa','agr','coop','cooperativa','castello','villa','del','della','dei','delle','di','da','il','la','le','lo','the','wine','winery','fratelli','figli'}
def toks(s):
    return {t for t in re.findall(r'[a-zà-ú]{4,}',s.lower()) if t not in GEN}
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
def esc(s): return s.replace('{{','').replace('}}','').replace('[[','').replace(']]','')
tot={'rag':0,'piva':0,'storia':0,'vini':0,'skip_nome':0}
for ln in open(R+'/arricchimenti/toscana_all.tsv',encoding='utf8'):
    p=ln.rstrip('\n').split('\t')
    if len(p)<5: continue
    slug,rag,piva,storia,vini=[x.strip() for x in p[:5]]
    f=f'{R}/dati/{slug}.json'
    if not os.path.exists(f): continue
    if rag in ('ROBOTS','REDIR','ERR','SKIP','DUP','SPAM','DUBBIO'): continue
    d=json.load(open(f,encoding='utf8'))
    secs={s['titolo']:s for s in d['sezioni']}
    url=None
    for r in secs.get('Anagrafica',{}).get('righe',[]):
        if r['etichetta']=='Sito ufficiale':
            m=re.search(r'\{\{(.*?)\|',r['valore']); url=m.group(1) if m else None
    rag_ok=rag not in SENT and bool(toks(rag)&toks(d['nome']+' '+slug.replace('-',' ')))
    if rag not in SENT and not rag_ok: tot['skip_nome']+=1
    piva=re.sub(r'\D','',piva) if piva not in SENT else ''
    piva_v=piva if piva_ok(piva) else ''
    if rag_ok is False and rag not in SENT: piva_v=''
    st=storia if storia not in SENT else ''
    vi=[v.strip() for v in vini.split(';') if v.strip() and v.strip()!='-'] if vini not in SENT else []
    if not(rag_ok or piva_v or st or vi): continue
    n=max([x['n'] for x in d['fonti']]+[0])+1
    d['fonti'].append({'n':n,'testo':'Sito ufficiale dell’azienda, pagina iniziale, consultato il 26 ottobre 2026.','url':url or '','etichetta':(re.sub(r'^https?://(www\.)?','',url).split('/')[0] if url else 'sito ufficiale')})
    m=f' [[{n}]]'
    ana=secs['Anagrafica']['righe']
    if rag_ok or piva_v:
        txt=(esc(rag) if rag_ok else '')+(', ' if rag_ok and piva_v else '')+(f'P.IVA {piva_v}' if piva_v else '')
        pos=min(len(ana),2)
        ana.insert(pos,{'etichetta':'Ragione sociale e P.IVA','valore':txt+m})
        if rag_ok: tot['rag']+=1
        if piva_v: tot['piva']+=1
    if st:
        for s in d['sezioni']:
            for r in s['righe']:
                if r['etichetta']=='Storia e proprietà':
                    if r['valore'].startswith('Non disponibile') or r['valore'].startswith('Non '):
                        r['valore']=esc(st)+m
                    else: r['valore']+=' '+esc(st)+m
        tot['storia']+=1
    if vi:
        sv=secs.get('Vini')
        if sv is None:
            sv={'titolo':'Vini','righe':[]}; d['sezioni'].insert(2,sv)
        sv['righe'].append({'etichetta':'Denominazioni citate sul sito ufficiale','valore':'; '.join(esc(v) for v in vi)+m})
        tot['vini']+=1
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1)
    cf=f'{R}/chiarire/{slug}.txt'
    if os.path.exists(cf):
        keep=[]
        for l in open(cf,encoding='utf8').read().splitlines():
            h=l.split('|')[0].strip()
            if h=='Ragione sociale' and rag_ok: continue
            if h=='Vini' and vi: continue
            if h=='Storia' and st: continue
            keep.append(l)
        if keep: open(cf,'w',encoding='utf8').write('\n'.join(keep)+'\n')
        else: os.remove(cf)
print('arricchimenti:',tot)
