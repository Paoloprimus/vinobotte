import re,json,html,sys
SRC='/tmp/claude-0/-home-claude/d155faf6-1db0-5293-a642-f17d92f455f5/scratchpad/artifact-files/830e67ba-5715-4043-aae8-910a95c73d11/project/'
def tok(s):
    s=re.sub(r'<a class="fn" href="#f(\d+)" aria-label="Fonte \d+">\[\d+\]</a>',r'[[\1]]',s)
    s=re.sub(r'<br\s*/?>','\n',s)
    s=re.sub(r'<a href="([^"]+)">(.*?)</a>',lambda m:'{{%s|%s}}'%(html.unescape(m.group(1)),html.unescape(m.group(2))),s)
    assert '<' not in s,s
    return html.unescape(s)
def estrai(fn):
    t=open(SRC+fn,encoding='utf-8').read()
    main=t[t.index('<main>'):t.index('</main>')]
    nome=re.search(r'<h1[^>]*>(.*?)</h1>',main).group(1)
    sezioni=[]
    for m in re.finditer(r'<section( class="fonti")?><h2>(.*?)</h2>(.*?)</section>',main,re.S):
        if m.group(1):
            fb=m.group(3)
            consultate=tok(re.search(r'<p>(.*?)</p>',fb).group(1))
            fonti=[]
            for li in re.finditer(r'<li id="f(\d+)">(.*?)</li>',fb,re.S):
                body=li.group(2)
                a=re.search(r'^(.*?) <a href="([^"]+)">(.*?)</a>$',body,re.S)
                fonti.append(dict(n=int(li.group(1)),testo=html.unescape(a.group(1)),url=html.unescape(a.group(2)),etichetta=html.unescape(a.group(3))))
            continue_fonti=dict(consultate=consultate,fonti=fonti)
            continue
        titolo=html.unescape(m.group(2));body=m.group(3)
        sez=dict(titolo=titolo)
        nota=re.search(r'<p class="nota">(.*?)</p>',body,re.S)
        if nota: sez['nota']=tok(nota.group(1))
        if '<div class="vini">' in body:
            vini=[]
            for v in re.finditer(r'<div class="vn">(.*?)</div><div class="vd">(.*?)</div><div class="va">(.*?)</div>',body):
                vini.append(dict(nome=html.unescape(v.group(1)),denominazione=html.unescape(v.group(2)),annata=html.unescape(v.group(3))))
            sez['tipo']='vini';sez['vini']=vini
        else:
            righe=[]
            for r in re.finditer(r'<div class="row"><div class="lab">(.*?)</div><div class="val">(.*?)</div></div>',body,re.S):
                val=r.group(2);riga=dict(etichetta=html.unescape(r.group(1)))
                ul=re.search(r'<ul class="vig">(.*?)</ul>',val,re.S)
                if ul:
                    riga['elenco']=[html.unescape(x) for x in re.findall(r'<li>(.*?)</li>',ul.group(1))]
                    val=val[:ul.start()]+val[ul.end():]
                riga['valore']=tok(val)
                righe.append(riga)
            sez['righe']=righe
        sezioni.append(sez)
    return dict(nome=html.unescape(nome),sezioni=sezioni,**continue_fonti)
for fn,out in (('Main.dc.html','le-salette'),('Begali.dc.html','begali')):
    d=estrai(fn)
    d['slug']=out
    json.dump(d,open('dati/%s.json'%out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print(out,d['nome'],[ (s['titolo'],len(s.get('righe',s.get('vini',[])))) for s in d['sezioni']],len(d['fonti']))
