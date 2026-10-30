import sys,os
sys.path.insert(0,'tools')
from arricchisci import apply
SP='spec/prosecco/%s-prosecco.txt'; SC='spec/conegliano/%s-conegliano.txt'
N='Il sito non indica le denominazioni dei vini'
D=[]
def add(base,U,kinds,**d): D.append((base,U,d,kinds))
add('ca-di-rajo','https://www.cadirajo.it/',['p','c'],
 rs='Ca’ Di Rajo Soc. Agr.; P.IVA 04249490261', sede='Via del Carmine 2/2, 31020 San Polo di Piave (TV)', contatti='Tel. +39 0422 855885; info@cadirajo.it', contatti_diversi=True, sito='https://www.cadirajo.it/',
 storia='Il sito la lega alla famiglia Cecchetto: i fratelli Simone, Alessio e Fabio sono indicati come attuali responsabili; la pagina «Storia» porta il titolo «Ca’ di Rajo dal 2005»',
 vini_nota_p='Il sito cita il Prosecco Superiore e il Raboso senza indicare nomi commerciali né denominazioni', vini_nota_c='Il sito cita il Prosecco Superiore e il Raboso senza indicare nomi commerciali né denominazioni')
add('cabert','https://www.cabert.it/',['p'],
 rs='Cabert S.p.A. (Cantina di Bertiolo); P.IVA 00167540301', sede='Via Madonna 27, 33032 Bertiolo (UD)', sito='https://www.cabert.it/', storia='Il sito riporta «Passione per il vino dal 1960»',
 vini_p=[(n,dn,'—') for n,dn in [('Chardonnay','Friuli DOC'),('Friulano','Friuli DOC'),('Pinot Grigio','Friuli DOC'),('Sauvignon','Friuli DOC'),('Traminer Aromatico','Friuli DOC'),('Cabernet Franc','Friuli DOC'),('Cabernet Sauvignon','Friuli DOC'),('Pinot Nero','Friuli DOC'),('Merlot','DOC (denominazione specifica non indicata nel sito)'),('Refosco dal Peduncolo Rosso','DOC (denominazione specifica non indicata nel sito)'),('Prosecco','Prosecco DOC'),('Prosecco Rosé','Prosecco Rosé DOC'),('Violino Frizzante','Prosecco DOC'),('Picolit','DOCG'),('Chardonnay','Friuli Colli Orientali DOC'),('Friulano','Friuli Colli Orientali DOC'),('Pinot Grigio','Friuli Colli Orientali DOC'),('Ribolla Gialla','Friuli Colli Orientali DOC'),('Sauvignon','Friuli Colli Orientali DOC'),('Cabernet Sauvignon','Friuli Colli Orientali DOC'),('Merlot','Friuli Colli Orientali DOC'),('Refosco dal Peduncolo Rosso','Friuli Colli Orientali DOC'),('Schioppettino','Friuli Colli Orientali DOC'),('Pinot Grigio','Delle Venezie DOC'),('Pinot Grigio Blush','Delle Venezie DOC')]], filtrati=True,
 premi='Il sito parla di vini «pluripremiati in tutto il mondo» (recensione) ma non elenca premi',
 domande=['Storia | Il sito rimanda a una pagina «La nostra storia» non leggibile | Chi sono i soci e come è nata la cantina?','Premi | La sezione «Premi e Riconoscimenti» del sito non era leggibile | Quali premi ha ottenuto?'])
add('cantina-colli-del-soligo','https://www.collisoligo.com/',['p','c'],
 rs='Cantina Colli del Soligo S.A.C.; P.IVA 00179830260', sede='Via Lino Toffolin 6, Fraz. Solighetto, 31053 Pieve di Soligo (TV)', sito='https://www.collisoligo.com/',
 desc='Cooperativa di soci viticoltori; il sito riporta «Emozioni in bottiglia dal 1957»',
 vini_nota_p='Il sito ha le linee «Prosecco DOC Treviso» e «Valdobbiadene Prosecco Superiore DOCG», senza nomi commerciali per la prima',
 vini_c=[('Col de Mez','Valdobbiadene Prosecco Superiore DOCG','—')], filtrati=True)
add('cantina-colli-euganei','https://cantinacollieuganei.it',['p'],
 sede='Via G. Marconi 314, 35030 Vo’ (PD)', contatti='Tel. +39 049 9940011; info@cantinavo.it', contatti_diversi=True, sito='https://cantinacollieuganei.it',
 vini_p=[('Spumante Dosaggio Zero Millesimato','Prosecco DOC','—'),('Spumante Extra Brut','Prosecco DOC','—'),('Fior d’Arancio Secco','Fior d’Arancio DOCG','—'),('Fior d’Arancio Spumante Dolce','Fior d’Arancio DOCG','—'),('Sogno di Giotto','Colli Euganei Riserva DOC','—'),('Notte di Galileo','DOC (denominazione specifica non indicata nel sito)','—'),('Merlot','DOC (denominazione specifica non indicata nel sito)','—'),('Rialto Sauvignon','DOC (denominazione specifica non indicata nel sito)','—'),('Rialto Carmenere','DOC (denominazione specifica non indicata nel sito)','—')], filtrati=True,
 domande=['Partita IVA e ragione sociale | Non indicate nel sito | Quali sono i dati societari?','Premi | Il sito ha una pagina «I riconoscimenti» non leggibile | Quali premi ha ottenuto?'])
add('cantina-de-pra','https://www.cantinadepra.com/',['p','c'],
 rs='Cantina De Pra S.r.l.; P.IVA 02103200263', sede='Via Armentaressa 75, 31024 Ormelle (TV)', contatti='Tel. 0422 745304; cell. +39 331 1989379; info@cantinadepra.com; laboratorio@cantinadepra.com', sito='https://www.cantinadepra.com/',
 storia='Il sito parla di una tradizione familiare «dal 1959» e di vigneti propri a Ormelle, Motta di Livenza e in altre località della Marca Trevigiana',
 vini_nota_p='Il sito non indica vini Prosecco DOC con la denominazione', vini_c=[('Malanotte del Piave','Malanotte del Piave DOCG','—')], filtrati=True,
 premi='Il sito dice che i vini sono stati «premiati nel corso degli anni», senza indicare premi, concorsi o anni')
add('cantina-di-conegliano-e-vittorio-veneto','https://cantinadiconeglianoevittorioveneto.it',['p','c'],
 rs='Cantina di Conegliano, Vittorio Veneto e Casarsa S.A.C., società agricola cooperativa; P.IVA 00190690263', sede='Via del Campardo 3, 31029 Vittorio Veneto (TV)', contatti='Tel. 0438 500209; info@cantinacovive.it',
 desc='Cooperativa nata dall’integrazione della Cantina Sociale di Vittorio Veneto, della Cantina di Conegliano, di quella di Sacile e Fontanafredda e dei Viticoltori Friuliani La Delizia; stabilimenti a Vittorio Veneto, Conegliano (Via San Giuseppe), Casarsa della Delizia (PN) e Fontanafredda (PN)',
 vini_p=[('Extra Dry','Prosecco Treviso DOC','—'),('Frizzante','Prosecco Treviso DOC','—')],
 vini_c=[('Extra Dry','Conegliano Valdobbiadene Prosecco Superiore DOCG','—'),('Frizzante','Conegliano Valdobbiadene Prosecco DOCG','—')], filtrati=True)
add('cantina-di-rauscedo','http://www.cantinarauscedo.com/',['p'],
 rs='Cantina di Rauscedo; P.IVA 00072770936', sede='Via del Sile 16, 33095 Rauscedo (PN)', sito='http://www.cantinarauscedo.com/',
 vini_nota_p='Il sito elenca nomi commerciali (Casa Quaranta, Le Gemme, Rauscedo) senza indicare le denominazioni')
add('cantina-la-salute','https://www.cantinalasalute.it/',['p'],
 rs='Cantina La Salute S.r.l.; P.IVA 05048690266', sede='Via Salute 8, 31047 Ponte di Piave (TV)', contatti='Email info@cantinalasalute.it (PEC cantinalasalute@pec.it)', contatti_diversi=True, sito='https://www.cantinalasalute.it/',
 storia='Il sito la descrive come «un vivace gruppo di viticoltori che coopera per produrre vini da più di 50 anni»',
 vini_nota_p='Il sito elenca le linee La Salute, Forcola e Bag in box senza indicare le denominazioni', premi='Il sito dice di aver ottenuto «numerosi premi e riconoscimenti», senza indicarli')
add('cantine-riondo','http://www.cantineriondo.com',['p'],
 rs='Cantine Riondo S.p.A.',
 storia='Nata nel 2008 «come costola del grande gruppo cooperativo COLLIS» (sezione iniziale del sito)',
 vini_nota_p='Il sito elenca Amarone, Recioto, Ripasso, Pinot Grigio e Prosecco Brut senza indicare le denominazioni',
 premi='Dichiarati dalla cantina sul sito, senza collegarli a un vino: 5 Star Wines 05/2023 (92); Luca Maroni 07/2022 (96); The Wine Hunter 05/2022; Vinordic Wine Challenge 05/2023 (oro); Mundus Vini 02/2022 (oro, Best of Show, argento) e 03/2021 (oro, argento); Gilbert & Gaillard 03/2021 (oro); Berliner Wein Trophy 12/2021 (Grand Gold)')
add('casa-vinicola-canella','https://www.bellinicanella.com/',['p','c'],
 rs='Casa Vinicola Canella S.p.A.; P.IVA 00270430275', contatti='Tel. +39 0421 52446; fax +39 0421 330262; info@bellinicanella.com', contatti_diversi=True, sito='https://www.bellinicanella.com/',
 storia='Il sito fa iniziare la storia nel 1947 nell’osteria di famiglia a San Donà di Piave; Luciano Canella produce e imbottiglia il Bellini nel 1988; dal 1991 l’azienda è gestita da Alessandra, Lorenzo, Nicoletta e Monica; nel 2017 entra Tommaso, terza generazione',
 vini_nota_p='Il sito cita Bellini, Mimosa, Rossini, Puccini, Limoni e «prosecchi» senza indicare le denominazioni', vini_nota_c='Il sito cita «prosecchi» senza indicare le denominazioni',
 domande=['Vini a denominazione | Il sito presenta soprattutto cocktail e prodotti a base di pesca | Quali sono i vini Prosecco DOC e Conegliano Valdobbiadene DOCG prodotti?'])
add('castello-di-roncade','https://www.castellodironcade.com/',['p'],
 contatti=None, sito='https://www.castellodironcade.com/',
 storia='Complesso rinascimentale del 1508 (Villa Giustinian), legato alla famiglia Baroni Ciani Bassetti; il legame tra vino e ospitalità nasce nel 1988 con Vincenzo Ciani Bassetti',
 vini_nota_p='Il sito rimanda a «Scopri tutti i vini» senza elencare etichette né denominazioni',
 domande=['Partita IVA e ragione sociale | Non indicate nel sito | Quali sono i dati societari?'])
add('cielo-e-terra','https://www.cieloeterravini.com/',['p'],
 rs='Cielo e Terra S.p.A. Società Benefit; P.IVA 02160070245', sede='Via IV Novembre 39, 36050 Montorso Vicentino (VI)', contatti='Tel. +39 0444 485211; info@cieloeterravini.com', contatti_diversi=True, sito='https://www.cieloeterravini.com/',
 storia='Il sito indica due radici: la famiglia Cielo (podere con vigneto Casa Defrà acquistato nel 1908) e i viticoltori delle Cantine dei Colli Berici; nel 2021 è stata acquistata Villa «La Favorita»',
 vini_nota_p='Il sito elenca marchi (Bericanto, Maia, Cielo 1908, Casa Defrà, Pradio, Bella Storia, Freschello, 3Passo, Deconti, Gran Passaia, Baccolo) senza indicare le denominazioni',
 domande=['Produzione | Il sito non dice se vinifica in proprio o con uve di conferitori | Produce direttamente?'])
add('conte-collalto','https://www.cantine-collalto.it/',['p','c'],
 rs='Azienda Agricola Conte Collalto S.A.R.L. con socio unico; P.IVA 07921480963', sito='https://www.cantine-collalto.it/',
 storia='Il sito racconta la famiglia dei Conti di Collalto (con una donazione del 958 a Rambaldo I) e dice che dal 1904 i vini sono prodotti nella cantina della famiglia',
 vini_nota_p='Il sito cita il Prosecco DOCG Conegliano Valdobbiadene senza nomi commerciali', vini_nota_c='Il sito cita il Prosecco DOCG Conegliano Valdobbiadene senza nomi commerciali')
add('corazzin','https://www.proseccocorazzin.com/',['p','c'],
 rs='Corazzin Azienda Agricola Adelaide S.S.; P.IVA 04666390267', sito='https://www.proseccocorazzin.com/',
 desc='Il sito dice di produrre vini «esclusivamente da vitigni di proprietà»',
 vini_nota_p='Il sito non indica nomi commerciali né denominazioni', vini_nota_c='Il sito non indica nomi commerciali né denominazioni')
add('dal-bello-antonio','https://dalbellovini.it/',['p'],
 rs='Azienda Agricola Dal Bello Antonio; P.IVA 03702610266', sito='https://dalbellovini.it/',
 storia='Il sito la presenta come «una famiglia di viticoltori dal 1906»',
 vini_p=[('Prosecco','Prosecco Treviso DOC','—')], filtrati=True,
 premi='Una news del sito parla di partecipazione a competizioni internazionali, senza elencare i premi')
add('de-stefani','https://www.de-stefani.it/',['p'],
 rs='De Stefani (ragione sociale completa non indicata nel sito); P.IVA 01915440281', sito='https://www.de-stefani.it/',
 storia='Il sito parla di cinque generazioni di famiglia; Alessandro De Stefani è indicato come enologo di quarta generazione',
 vini_nota_p='Il sito elenca vini Valdobbiadene Prosecco Superiore DOCG e linee (Bailo, Redentore, Naturalmente, DS, Zero) senza denominazioni per le linee',
 premi='Tre Bicchieri (Gambero Rosso) al Rive di Refrontolo Valdobbiadene Prosecco Superiore DOCG Extra Brut Millesimato, secondo una news del sito; una news cita James Suckling senza dettagli',
 domande=['Vini DOCG | Il sito elenca vini Valdobbiadene Prosecco Superiore DOCG che non compaiono in questa scheda | Questa cantina compare anche nel Consorzio Conegliano Valdobbiadene?'])
add('fantinel','https://www.fantinel.com/',['p'],
 rs='Gruppo Vinicolo Fantinel S.p.A.; P.IVA 00486360308', sito='https://www.fantinel.com/',
 desc='Gruppo con più marchi e tenute: Tenuta Sant’Helena, La Roncaia, Zuccolo, Testa & Molinaro, Sun Goddess, The Independent Prosecco',
 vini_nota_p='Il sito parla di «vini friulani del Collio» e «vini DOC» senza elencare etichette né denominazioni',
 domande=['Produzione | Il sito non dice se il gruppo produce direttamente o con tenute associate | Quali cantine produce direttamente?'])
add('carpene-malvolti','https://www.carpene-malvolti.com/',['p','c'],
 sede='Via Antonio Carpenè 1, 31015 Conegliano (TV)', contatti='Tel. +39 0438 364601', contatti_diversi=True, sito='https://www.carpene-malvolti.com/',
 storia='Il sito dice «Dal 1868 la nostra famiglia guida l’evoluzione della spumantistica italiana»; Antonio Carpenè fondò nel 1876 la prima Scuola Enologica d’Italia',
 vini_nota_p='Il sito elenca le linee Tarvisium, Revival 1924, Linea 1868 e Linea Storico senza indicare le denominazioni', vini_nota_c='Il sito elenca le linee Tarvisium, Revival 1924, Linea 1868 e Linea Storico senza indicare le denominazioni')
add('furlan','https://www.furlanvini.com/',['p','c'],
 rs='Furlan Società Agricola S.S.; P.IVA 03004870261', sede='Vicolo Saccon 48, 31020 San Vendemiano (TV)', contatti='Tel./fax 0438 778267; info@furlanvini.com', sito='https://www.furlanvini.com/',
 storia='Fondata nel 1930 dal nonno Amadio; oggi gestita dai nipoti Amedeo, Alberto e Moreno; ha anche un agriturismo',
 vini_nota_p='Il sito non elenca vini con denominazione', vini_nota_c='Il sito non elenca vini con denominazione')
for base,U,d,kinds in D:
    for k in kinds:
        path=(SP if k=='p' else SC)%base
        if not os.path.exists(path): print('MANCA',path); continue
        apply(path,U,d,k); print('ok',path)
