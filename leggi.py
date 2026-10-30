import re,sys
D,u=sys.argv[1],sys.argv[2];a=int(sys.argv[3]) if len(sys.argv)>3 else 0;b=int(sys.argv[4]) if len(sys.argv)>4 else 2500
t=open(f'/home/claude/testi/testi_{D}.txt',encoding='utf-8').read()
for m in re.finditer(r'^===== (\S+)\n(.*?)(?=^===== |\Z)',t,re.S|re.M):
    if re.sub(r'^https?://[^/]+','',m.group(1))==u: import re as _r;x=_r.split(r'Informazioni sui cookie|Gestisci consenso|Gestisci Consenso|Utilizziamo i cookie|Questo sito utilizza (i )?cookie|We use cookies|This website uses cookies',m.group(2))[0];print(x[a:b]);break
else: print('NON TROVATA')
