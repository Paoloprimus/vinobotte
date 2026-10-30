import json,os,glob,re
R=os.path.dirname(os.path.abspath(__file__))+'/..'
RX=re.compile(r'(?:Social, )?Google Business Profile, [^:;\n]*?: presenza non verificata')
G=json.load(open(R+'/arricchimenti/google.json')); GT=set(G['trovate'])
V=json.load(open(R+'/arricchimenti/vivino_presenza.json')); VIV=set(x['slug'] for x in json.load(open(R+'/vivino-nuovi.json')))
VT=set(V['trovate'])|set(V.get('trovate_ricerca',{}))|VIV; VC=set(V.get('cercate',[]))
W=set(json.load(open(R+'/arricchimenti/wikipedia.json'))['trovate'])
n=0
for f in glob.glob(R+'/dati/*.json'):
    d=json.load(open(f,encoding='utf8')); slug=d['slug']; ch=False
    for s in d['sezioni']:
        has_social=any(r['etichetta']=='Social' for r in s.get('righe',[]))
        for r in s.get('righe',[]):
            if r['etichetta']!='Piattaforme': continue
            m=RX.search(r['valore'])
            if not m: continue
            seg=m.group(0); tutto=json.dumps(d,ensure_ascii=False).lower().replace(r['valore'].lower(),'')
            p=[]
            if seg.startswith('Social, ') and not has_social: p.append('Social: non indicati dal sito')
            if slug not in GT: p.append('Google Maps: nessuna scheda trovata (ricerca del 29 ottobre 2026)')
            if slug not in VT: p.append('Vivino: non trovata tra i produttori (ricerca del 29 ottobre 2026)' if slug in VC and slug not in V['incerte'] else 'Vivino: presenza non verificata')
            if 'Instagram' in seg and 'instagram' not in tutto: p.append('Instagram: non indicato dal sito')
            if 'YouTube' in seg and 'youtube' not in tutto: p.append('YouTube: non indicato dal sito')
            if slug not in W: p.append('Wikipedia: nessuna voce in italiano (ricerca del 29 ottobre 2026)')
            v=r['valore']; pre=v[:m.start()].rstrip('; ,').strip(); suf=v[m.end():].strip()
            righe=[x for x in pre.split('; ') if x]
            if righe and suf: righe[-1]+=' '+suf
            elif suf and not righe and not p: righe=[suf]
            r['valore']='\n'.join(righe+p); ch=True
    if ch: json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1); n+=1
print('piattaforme:',n)
