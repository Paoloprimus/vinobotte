import re,sys
D=sys.argv[1];N=int(sys.argv[2]) if len(sys.argv)>2 else 1100
t=open(f'/home/claude/testi/testi_{D}.txt',encoding='utf-8').read()
pag=[(re.sub(r'^https?://[^/]+','',m.group(1)),m.group(2)) for m in re.finditer(r'^===== (\S+)\n(.*?)(?=^===== |\Z)',t,re.S|re.M)]
pag=[(u,p) for u,p in pag if not re.match(r'/(en|de|fr|es|ru|zh|us|it)/',u) or u.startswith('/it/')]
seen=0
for key in ['(contatt|contact|dove-siamo)','(chi-siamo|storia|about|azienda|la-cantina|cantina|famiglia|history|winery)','(vigne|vineyard|territor)','(visit|degust|ospital|tour|tasting|enoturismo|experience|wine-?experience)']:
    c=[(u,p) for u,p in pag if re.search(key,u,re.I) and '/blog' not in u and '/news' not in u]
    c.sort(key=lambda x:len(x[0]))
    for u,p in c[:2]:
        print('##',u,len(p));print(re.sub(r'\s+',' ',p)[:N]);print()
