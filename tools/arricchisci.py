import re,sys
NOTA="Solo vini a denominazione DOC/DOCG; esclusi IGT, vini senza denominazione e distillati."
def apply(path, U, d, kind):
    """kind: 'p' (prosecco) o 'c' (conegliano). d: dict dati."""
    t=open(path,encoding='utf-8').read()
    L=t.split('\n')
    def find(prefix):
        for i,l in enumerate(L):
            if l.startswith(prefix+' |'): return i
        return -1
    def setrow(label,val,after=None):
        i=find(label)
        row=f"{label} | {val}"
        if i>=0: L[i]=row
        else:
            j=find(after) if after else -1
            if j<0: j=find('Ragione sociale')
            L.insert(j+1,row)
    # consultate
    for i,l in enumerate(L):
        if l.startswith('consultate:'):
            L[i]="consultate: Scheda del Consorzio e sito ufficiale della cantina, consultati il 25 ottobre 2026. Ogni dato della scheda rinvia alla fonte con il numero tra parentesi quadre."
    old_sede=L[find('Sede')].split(' | ',1)[1] if find('Sede')>=0 else ''
    old_cont=L[find('Contatti')].split(' | ',1)[1] if find('Contatti')>=0 else ''
    S=f"[{U}]"
    if d.get('rs'): setrow('Ragione sociale',d['rs']+' '+S)
    if d.get('sede'):
        if d.get('sede_diversa'):
            setrow('Sede',d['sede']+' '+S,'Ragione sociale')
        else:
            setrow('Sede',d['sede']+' '+S+(' [P]' if d.get('sede_p') else ''),'Ragione sociale')
    if d.get('sede_diversa') or d.get('contatti_diversi'):
        lab='Dati nella mappa del Consorzio Prosecco DOC' if kind=='p' else 'Dati nell’elenco del Consorzio Conegliano Valdobbiadene'
        parts=[]
        if d.get('sede_diversa'): parts.append(re.sub(r'\s*\[P\]$','',old_sede))
        if d.get('contatti_diversi'): parts.append(re.sub(r'\s*\[P\]$','',old_cont))
        if find(lab)<0 and parts: setrow(lab,'; '.join(parts)+' [P]','Sede')
    if d.get('contatti'): setrow('Contatti',d['contatti']+' '+S,'Sede')
    if d.get('sito'):
        i=find('Sito ufficiale')
        row=f"Sito ufficiale | {{{{{d['sito']}|{d['sito'].split('//')[1].rstrip('/')}}}}} {S}"
        if i>=0: L[i]=row
        else: L.insert(find('Contatti')+1 if find('Contatti')>=0 else find('Sede')+1,row)
    if d.get('desc'): setrow('Descrizione',d['desc']+' '+S,'Sito ufficiale')
    if d.get('storia'):
        i=find('Storia e proprietà')
        row=f"Storia e proprietà | {d['storia']} {S}"
        if i>=0: L[i]=row
    vini=d.get('vini_'+kind)
    note=d.get('vini_nota_'+kind)
    if kind=='p':
        i=find('Elenco vini Prosecco DOC')
        if i>=0:
            rows=[]
            if vini:
                rows.append("nota: "+NOTA+" "+S) if d.get('filtrati') else None
                rows+= [f"v | {n} | {den} | {an} {S}" for n,den,an in vini]
            else:
                rows.append(f"Elenco vini Prosecco DOC | {note or 'Il sito non indica vini con la denominazione'} {S}")
            L[i:i+1]=[r for r in rows if r]
    else:
        # sostituisci blocco @Vini
        a=[i for i,l in enumerate(L) if l.startswith('@Vini')][0]
        b=a+1
        while b<len(L) and not L[b].startswith('@'): b+=1
        if vini:
            rows=(["nota: "+NOTA+" "+S] if d.get('filtrati') else [])+[f"v | {n} | {den} | {an} {S}" for n,den,an in vini]
            L[a+1:b]=rows
        elif note:
            L[a+1:b]=[L[x] for x in range(a+1,b)]+[f"Nota sito ufficiale | {note} {S}"]
    if d.get('premi'):
        i=find('Premi e punteggi')
        if i>=0: L[i]=f"Premi e punteggi | {d['premi']} {S}"
    # domande
    out=[]
    for l in L:
        if l.startswith('? Scheda essenziale'): continue
        if l.startswith('? Vini Prosecco DOC') and (vini or note): continue
        if l.startswith('? Nomi dei vini') and vini: continue
        if l.startswith('? Comune') and d.get('sede') and not d.get('comune_incerto'): continue
        if l.startswith('? Vini Prosecco DOC') or l.startswith('? Nomi dei vini'):
            pass
        out.append(l)
    for q in d.get('domande',[]): out.append('? '+q)
    open(path,'w',encoding='utf-8').write('\n'.join(out))
