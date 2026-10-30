import re,json,collections
STOP=r"(?=\s*(?:[-–—|•·,;©]|\bVia\b|\bV\.le\b|\bViale\b|\bStr(?:ada)?\b|\bLoc(?:\.|alit[àa])\b|\bPiazza\b|\bP\.?\s?I|\bC\.?F|\bPartita\b|\bCod|\bSede\b|\bREA\b|\bCap(?:itale)?\b|\bTel|\bFax|\bN\.?\s?Iscr|\bR\.?E\.?A|\bIT\s?\d|\d{3,}|$))"
LEG=r"(?:S\.?\s?r\.?\s?l\.?s?|S\.?\s?p\.?\s?A\.?|S\.?\s?s\.?\s?a\.?|S\.?\s?a\.?\s?s\.?|S\.?\s?n\.?\s?c\.?|S\.?\s?s\.?|Soc\.?\s?Coop\.?(?:\s?Agr(?:\.|icola)?)?(?:\s?a\.?\s?r\.?\s?l\.?)?|Societ[àa]\s+(?:Cooperativa|Semplice)(?:\s+Agricola)?)"
PRE=r"(?:Societ[àa]'?\s+Agricol[ae]|Societ[àa]\s+Agrari[ae]|Soc\.?\s?Agr\.?|Azienda\s+Agricol[ae]|Azienda\s+Agrari[ae]|Az\.?\s?Agr\.?(?:icola)?|Cantina\s+Sociale|Cantina|Fattoria|Tenuta|Cooperativa|Consorzio|Agricola|Vinicola|Casa\s+Vinicola|Tenute|Cantine)"
W=r"[A-ZÀ-Ú0-9][\w'’&.À-ÿ]*|[a-zà-ÿ]{1,4}\.?"
def rag(ctx):
    # ctx: testo che precede 'P.IVA'
    w=ctx[-170:]
    c=[]
    # forma con forma giuridica finale
    for m in re.finditer(r"((?:%s)(?:\s+(?:%s)){0,8}?\s+%s)\b\.?"%(PRE,W,LEG),w): c.append(m.group(1))
    for m in re.finditer(r"((?:[A-ZÀ-Ú][\w'’&.À-ÿ]*)(?:\s+(?:%s)){0,6}?\s+%s)(?=[\s,.|©-]|$)"%(W,LEG),w): c.append(m.group(1))
    # forma con prefisso: Azienda Agricola X Y
    for m in re.finditer(r"((?:%s)(?:\s+[A-ZÀ-Ú][\w'’&.À-ÿ]*(?:\s+(?:di|de|del|della|dei|degli|e|&|da|d')?\s*[A-ZÀ-Ú][\w'’&.À-ÿ]*){0,5}))%s"%(PRE,STOP),w): c.append(m.group(1))
    c=[x.strip(' .,-') for x in c if len(x)>6]
    if not c: return ''
    # preferisci l'ultimo (più vicino alla P.IVA), ma non troppo corto
    return c[-1]
if __name__=='__main__':
    out=[]
    for l in open('rs/trovate.txt'):
        s,p,ctx,u=l.rstrip('\n').split('|',3)
        i=ctx.lower().rfind(p)
        pre=re.sub(r'(?i)(p\.?\s?iva|partita\s+iva|p\.?\s?i\.|vat[^0-9]*|c\.?f\.?\s*(e|/)\s*)[^A-Za-z]*$','',ctx[:ctx.find(p)])
        out.append((s,p,rag(pre),pre[-90:]))
    n=sum(1 for o in out if o[2]); print(len(out),'con nome',n)
    for o in out[:60]: print(o[0],'|',o[2],'|',o[3][-60:])
