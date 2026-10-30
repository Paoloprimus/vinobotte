import json,sys
D=" Dichiarati dalla cantina, non verificati da VinoBot sulle guide."
def add(S,P):
    M=json.load(open('arricchimenti/giro_manual.json'))
    for s,t in S.items(): M.setdefault(s,{})['storia']=t
    for s,t in P.items(): M.setdefault(s,{})['premi']=t+D
    json.dump(M,open('arricchimenti/giro_manual.json','w'),ensure_ascii=False,indent=0)
