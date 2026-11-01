# Fornacelle (San Gimignano, Chianti Colli Senesi/Vernaccia) e Fornacelle (Castagneto Carducci, Bolgheri) sono due aziende diverse:
# erano fuse per omonimia. Toglie dalla scheda di San Gimignano il riquadro e il Consorzio Bolgheri (la scheda Bolgheri resta in lista provvisoria).
import json,os,re
os.chdir('/home/claude/annuario')
P=json.load(open('produttori.json',encoding='utf8'))
for p in P:
    if p['slug']=='fornacelle': p['tipi'].pop('bolgheri',None)
json.dump(P,open('produttori.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
f='dati/fornacelle.json'; d=json.load(open(f,encoding='utf8'))
bad=[y['n'] for y in d['fonti'] if 'bolgheridoc.com' in y.get('url','')]
if bad:
    b=bad[0]
    def ren(t): return re.sub(r'\[\[(\d+)\]\]',lambda m:'[['+str(int(m.group(1))-1 if int(m.group(1))>b else int(m.group(1)))+']]',t)
    for s in d['sezioni']:
        for r in s.get('righe') or []:
            if r['etichetta'] in ('Consorzio','Consorzi'):
                ls=[l for l in r['valore'].split('\n') if 'Bolgheri' not in l]
                r['valore']='\n'.join(ls); r['etichetta']='Consorzio' if len(ls)==1 else 'Consorzi'
            r['valore']=ren(r['valore'])
    for s_ in d['sezioni']: s_['righe']=[r for r in s_['righe'] if r['valore'].strip()]
    d['fonti']=[dict(y,n=y['n']-1 if y['n']>b else y['n']) for y in d['fonti'] if y['n']!=b]
    json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('fornacelle divisa')
