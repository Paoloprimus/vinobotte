import json,re,sys
n=sys.argv[1];mode=sys.argv[2]
d=json.load(open(f'giro/b{n}.json'))
if mode=='p':
    KP=re.compile(r'Gambero|Veronelli|Bibenda|medagli|punti|/100|Suckling|Falstaff|Decanter|WineHunter|Wine Hunter|Slow Wine|Vitae|Mundus|Bruxelles|Bicchieri|Wine Spectator|Parker|Vinous|Wine Enthusiast|Grappoli',re.I)
    for x in d:
        if 'errore' in x: continue
        p=x.get('premi_testo') or x.get('riconoscimenti')
        if p:
            p=' | '.join(map(str,p)) if isinstance(p,list) else p
            p=re.sub(r'\s+',' ',p);m=KP.search(p)
            if m and not re.match(r'Curriculum',p[m.start():]): print('##',x['slug'],'::',p[max(0,m.start()-40):m.start()+190])
else:
    K=re.compile(r'(fondat|dal 1[0-9]{3}|nel 1[0-9]{3}|nel 20[0-2][0-9]|generazion|nasce|nata |acquist|rileva|fondazione|since|founded)',re.I)
    for x in d:
        if 'errore' in x: continue
        s=x.get('storia')
        if isinstance(s,list): s=' '.join(map(str,s))
        if not s: continue
        s=re.sub(r'\s+',' ',s)
        fr=[f.strip() for f in re.split(r'(?<=[.!?])\s+',s) if K.search(f) and 40<len(f)<240 and not re.search(r'cookie|privacy|©|copyright|MENU|HOME|Curriculum|shop|sconto|acquist(a|i|are) ',f,re.I)]
        if fr: print('##',x['slug'],'::',fr[0])
