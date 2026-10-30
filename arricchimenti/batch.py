import json,sys
L=json.load(open('/home/claude/annuario/arricchimenti/lista.json'))
a=int(sys.argv[1]);print(' '.join(f'{i}:{s[1].replace("http://","").replace("https://","").rstrip("/")}' for i,s in enumerate(L[a:a+20],a)))
