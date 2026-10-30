import json,re,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
def esc(s): return s.replace('{{','').replace('}}','').replace('[[','').replace(']]','')
PLACE=re.compile(r'^(Non indicat|Non disponibil|Non present)',re.I)
tot=dict(applicate=0,con_nome=0,saltate_gia=0,assenti=0)
for ln in open(R+'/arricchimenti/rs.tsv',encoding='utf8'):
    p=ln.rstrip('\n').split('\t')
    if len(p)<4: continue
    slug,rag,piva,url=p[:4]
    f=f'{R}/dati/{slug}.json'
    if not os.path.exists(f): tot['assenti']+=1; continue
    d=json.load(open(f,encoding='utf8'))
    ana=next((s for s in d['sezioni'] if s['titolo']=='Anagrafica'),None)
    if ana is None: continue
    if any(r['etichetta'].startswith('Ragione sociale') and not PLACE.match(re.sub(r'\[\[\d+\]\]','',r['valore']).strip()) for r in ana['righe']): tot['saltate_gia']+=1; continue
    if re.search(r'(?<!\d)'+piva+r'(?!\d)',json.dumps(d)): tot['saltate_gia']+=1; continue
    ana['righe']=[r for r in ana['righe'] if not r['etichetta'].startswith('Ragione sociale')]
    n=max([x['n'] for x in d['fonti']]+[0])+1
    host=re.sub(r'^https?://(www\.)?','',url).split('/')[0]
    d['fonti'].append({'n':n,'testo':'Sito ufficiale dell’azienda, piè di pagina o note legali, consultato il 27 ottobre 2026.','url':url,'etichetta':host})
    txt=(esc(rag)+', ' if rag else '')+'P.IVA '+piva
    ana['righe'].insert(min(len(ana['righe']),2),{'etichetta':'Ragione sociale e P.IVA' if rag else 'P.IVA','valore':txt+f' [[{n}]]'})
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1)
    tot['applicate']+=1; tot['con_nome']+=1 if rag else 0
    cf=f'{R}/chiarire/{slug}.txt'
    if os.path.exists(cf):
        keep=[l for l in open(cf,encoding='utf8').read().splitlines() if not (l.split('|')[0].strip()=='Ragione sociale' and rag)]
        if keep: open(cf,'w',encoding='utf8').write('\n'.join(keep)+'\n')
        else: os.remove(cf)
print('rs:',tot)
