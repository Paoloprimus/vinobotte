import json,re,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
rg=json.load(open(R+'/arricchimenti/raggiungibilita.json'))
tot=dict(si=0,no=0,assenti=0)
for slug,o in rg.items():
    f=f'{R}/dati/{slug}.json'
    if not os.path.exists(f): tot['assenti']+=1; continue
    d=json.load(open(f,encoding='utf8')); ch=False; fatto=False
    for sz in d['sezioni']:
        for r in sz.get('righe',[]):
            if r['etichetta'].startswith('Sito') and not fatto and 'controllo del' not in r['valore']:
                fatto=True
                t=('raggiungibile' if o['ok'] else 'non raggiungibile')+' al controllo del 29 ottobre 2026'
                r['valore']=re.sub(r'(\}\})(\s*\[\[\d+\]\])?\s*$',lambda m:m.group(1)+' — '+t+(m.group(2) or ''),r['valore'],count=1)
                ch=True; tot['si' if o['ok'] else 'no']+=1
    if ch: json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('raggiungibilita:',tot)
