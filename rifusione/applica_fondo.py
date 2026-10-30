import json,re,os
R=os.path.dirname(os.path.abspath(__file__))+'/..'
tot=dict(sito=0,assenti=0,gia=0)
for FILE,DATA in (('b10f_l1','28 ottobre 2026'),('b11f_l1','29 ottobre 2026'),('b12f_l1','29 ottobre 2026')):
  for slug,o in json.load(open(R+'/giro/%s.json'%FILE)).items():
      f=f'{R}/dati/{slug}.json'
      if not os.path.exists(f): tot['assenti']+=1; continue
      d=json.load(open(f,encoding='utf8'))
      ana=next(s for s in d['sezioni'] if s['titolo']=='Anagrafica')['righe']
      if any(r['etichetta']=='Sito ufficiale' for r in ana): tot['gia']+=1; continue
      url=o['pagine'][0]; host=re.sub(r'^https?://(www\.)?','',url).split('/')[0]
      fo=next((x for x in d['fonti'] if x.get('url')==url),None)
      if fo is None:
          n=max([x['n'] for x in d['fonti']]+[0])+1
          fo={'n':n,'testo':'Sito ufficiale della cantina, home e pagine collegate, consultato il '+DATA+'.','url':url,'etichetta':host}
          d['fonti'].append(fo)
      pos=1+max([i for i,r in enumerate(ana) if r['etichetta'] in('Sede','Contatti')]+[0])
      ana.insert(pos,{'etichetta':'Sito ufficiale','valore':'{{%s|%s}} [[%d]]'%(url,host,fo['n'])})
      json.dump(d,open(f,'w',encoding='utf8'),ensure_ascii=False,indent=1)
      tot['sito']+=1
      cf=f'{R}/chiarire/{slug}.txt'
      if os.path.exists(cf):
          keep=[l for l in open(cf,encoding='utf8').read().splitlines() if l.split('|')[0].strip()!='Sito']
          if keep: open(cf,'w',encoding='utf8').write('\n'.join(keep)+'\n')
          else: os.remove(cf)
print('fondo:',tot)
