# Aggiunge al gruppo Montecucco i produttori che la lista del Consorzio Tutela Vini Montecucco indica ma che erano solo in Maremma Toscana.
import json,os
os.chdir('/home/claude/annuario')
S="basile-az-ienda-agricola-biologica berretta-di-curzio-renaioli de-vinosalvo-vignaioli le-pianore maciarine pianirossi prato-al-pozzo ribusieri vegni-medaglini-giannetti poggio-lapparita civettaio tenuta-limpostino poggio-trevvalle".split()
P=json.load(open('produttori.json',encoding='utf-8'));n=0
for p in P:
    if p['slug'] in S and 'montecucco' not in p['tipi']:
        p['tipi']['montecucco']=['Montecucco']; n+=1
O="castel-porrona donatella-cinelli-colombini casanova-di-neri".split()  # lista soci Consorzio Vino Orcia (30 ott 2026)
for p in P:
    if p['slug'] in O and 'orcia' not in p['tipi']:
        p['tipi']['orcia']=['Orcia']; n+=1
T="badia-di-morrona pietro-beconcini villa-saletta".split()  # Consorzio Vini Terre di Pisa (30 ott 2026)
for p in P:
    if p['slug'] in T and 'terre-di-pisa' not in p['tipi']:
        p['tipi']['terre-di-pisa']=['Terre di Pisa']; n+=1
M="la-cura conti-di-san-bonifacio la-pierotta".split()  # Monteregio di Massa Marittima: confermato dai siti delle cantine (30 ott 2026)
for p in P:
    if p['slug'] in M and 'monteregio' not in p['tipi']:
        p['tipi']['monteregio']=['Monteregio di Massa Marittima']; n+=1
json.dump(P,open('produttori.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('montecucco aggiunti',n)
