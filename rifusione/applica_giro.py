import json,re,os,glob
R=os.path.dirname(os.path.abspath(__file__))+'/..'
def esc(s): return s.replace('{{','').replace('}}','').replace('[[','').replace(']]','')
tot=dict(social=0,shop=0,email=0,tel=0,premi=0,storia=0,assenti=0)
files=sorted(glob.glob(R+'/arricchimenti/giro_*_l1.json'))
man=R+'/arricchimenti/giro_manual.json'
DATA={}
for f in files:
    for s,o in json.load(open(f)).items(): DATA.setdefault(s,{}).update(o)
if os.path.exists(man):
    for s,o in json.load(open(man)).items(): DATA.setdefault(s,{}).update(o)
for slug,o in DATA.items():
    f=f'{R}/dati/{slug}.json'
    if not os.path.exists(f): tot['assenti']+=1; continue
    d=json.load(open(f,encoding='utf8'))
    secs={s['titolo']:s for s in d['sezioni']}
    ana=secs['Anagrafica']['righe']
    url=(o.get('pagine') or [''])[0]
    host=re.sub(r'^https?://(www\.)?','',url).split('/')[0] or 'sito ufficiale'
    n=max([x['n'] for x in d['fonti']]+[0])+1; used=False
    m=f' [[{n}]]'
    # contatti
    cont=next((r for r in ana if r['etichetta']=='Contatti'),None)
    cur=re.sub(r'\[\[\d+\]\]','',cont['valore']) if cont else ''
    em=o.get('email'); tl=o.get('tel')
    raw=cont['valore'] if cont else ''
    needem=bool(em) and not re.search(r'@',cur)
    needtel=bool(tl) and not re.search(r'\d{6}',cur)
    if needem or needtel:
        base=re.sub(r'\s*\(la scheda del Consorzio non riporta[^)]*\)\s*','',raw).strip(' ;') if needem else raw
        if re.match(r'^Non disponibil',base): base=''
        parts=[]
        if needtel: parts.append('Tel. '+tl+m)
        if base: parts.append(base)
        if needem: parts.append('email '+em+m)
        newv='; '.join(parts)
        if cont: cont['valore']=newv
        else: ana.insert(min(len(ana),1),{'etichetta':'Contatti','valore':newv})
        used=True
        tot['email']+=needem; tot['tel']+=needtel
    # identità online
    io=secs.get('Identità online')
    if io is not None:
        rows=io['righe']
        pos=next((i for i,r in enumerate(rows) if r['etichetta'].startswith('Negozi online')),len(rows))
        if o.get('social'):
            txt='; '.join(f'{a} {{{{{u}|{esc(h)}}}}}' for a,u,h in o['social'])+m
            ex=next((r for r in rows if r['etichetta']=='Social'),None)
            if ex: ex['valore']=txt
            else: rows.insert(pos,{'etichetta':'Social','valore':txt}); pos+=1
            tot['social']+=1; used=True
        if o.get('shop'):
            lab=re.sub(r'^https?://(www\.)?','',o['shop']).rstrip('/')
            txt=f'Negozio online sul sito della cantina: {{{{{o["shop"]}|{esc(lab)}}}}}'+m
            ex=next((r for r in rows if r['etichetta']=='Vendita online'),None)
            if ex: ex['valore']=txt
            else: rows.insert(pos,{'etichetta':'Vendita online','valore':txt})
            tot['shop']+=1; used=True
    if o.get('premi') and 'Riconoscimenti' in secs:
        for r in secs['Riconoscimenti']['righe']:
            if r['etichetta']=='Premi e punteggi' and re.match(r'Non ',r['valore']):
                r['valore']=esc(o['premi'])+m; tot['premi']+=1; used=True
    if o.get('storia'):
        for s in d['sezioni']:
            for r in s.get('righe',[]):
                if r['etichetta']=='Storia e proprietà' and re.match(r'Non ',r['valore']):
                    r['valore']=esc(o['storia'])+m; tot['storia']+=1; used=True
    if not used: continue
    d['fonti'].append({'n':n,'testo':'Sito ufficiale della cantina, home e pagine collegate, consultato il 27 ottobre 2026.','url':url,'etichetta':host})
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1)
    cf=f'{R}/chiarire/{slug}.txt'
    if os.path.exists(cf):
        keep=[]
        for l in open(cf,encoding='utf8').read().splitlines():
            h=l.split('|')[0].strip()
            if h=='Storia' and o.get('storia'): continue
            if h in('Email',) and o.get('email'): continue
            keep.append(l)
        if keep: open(cf,'w',encoding='utf8').write('\n'.join(keep)+'\n')
        else: os.remove(cf)
print('giro:',tot)
