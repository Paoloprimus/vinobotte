import re,html
SRC='/tmp/claude-0/-home-claude/d155faf6-1db0-5293-a642-f17d92f455f5/scratchpad/artifact-files/830e67ba-5715-4043-aae8-910a95c73d11/project/'
def main(t):
    m=t[t.index('<main>')+6:t.index('</main>')]
    m=re.sub(r'<h1[^>]*>.*?</h1>','<h1/>',m,flags=re.S)   # titolo: stile h1 volutamente uniformato
    m=re.sub(r'>\s+<','><',m)
    return m.strip()
ok=True
for orig,gen in (('Main.dc.html','pagine/le-salette.html'),('Begali.dc.html','pagine/begali.html')):
    a=main(open(SRC+orig,encoding='utf-8').read()); b=main(open(gen,encoding='utf-8').read())
    same=(a==b); ok&=same
    print(orig,'->',gen,'IDENTICO' if same else 'DIVERSO',len(a),len(b))
    if not same:
        i=next(k for k,(x,y) in enumerate(zip(a,b)) if x!=y)
        print(' orig:',a[max(0,i-80):i+120]);print(' gen :',b[max(0,i-80):i+120])
print('ESITO','OK' if ok else 'ERRORE')
