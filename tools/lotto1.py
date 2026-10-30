import sys,os
sys.path.insert(0,'tools')
from arricchisci import apply
SP='spec/prosecco/%s-prosecco.txt'; SC='spec/conegliano/%s-conegliano.txt'
D=[]
D.append(('47-anno-domini','https://www.47annodomini.it/',dict(
 rs='Società Agricola 47 Anno Domini S.s.; P.IVA 03384780262', sede='Via Treviso Mare 2, 31056 Roncade (TV)', contatti='Tel. +39 0422 849976; info@47annodomini.it',
 sito='https://www.47annodomini.it/',
 vini_nota_p='Il sito elenca solo le linee (Diamante, Sottovoce, Riserve, I versatili, Perlage 47), senza indicare le denominazioni',
 domande=['Vini Prosecco DOC | Il sito elenca solo le linee, senza denominazione | Quali sono i vini a denominazione Prosecco DOC e con quale marchio?','Storia | Nel sito compare solo il motto «Progettiamo il futuro, consapevoli del nostro passato» | Chi sono i proprietari e da quando esiste l’azienda?']),['p']))
D.append(('abbazia-di-busco','https://www.abbaziadibusco.com/',dict(
 rs='Cantina Abbazia di Busco Società Agricola Liasora S.S.; P.IVA 02488900271', sede='Via IV Novembre 31, 31047 Busco di Ponte di Piave (TV)', contatti='Tel. 0422 752152; WhatsApp 339 191 47 09',
 sito='https://www.abbaziadibusco.com/', storia='Il nome richiama i monaci benedettini dell’Abbazia di Sant’Andrea a Busco; il sito non indica anno di fondazione né proprietari',
 vini_p=[('Battistero (Prosecco Brut Millesimato)','Prosecco DOC','—'),('Portico (Prosecco Extra Dry)','Prosecco DOC','—'),('Pulpito (Prosecco Frizzante)','Prosecco DOC','—'),('Capitolo','Pinot Grigio delle Venezie DOC','—')], filtrati=True,
 domande=['Novizio (Prosecco Rosé Extra Dry) | Il sito non indica la denominazione | Quale denominazione ha il Novizio?','Sede di Roma | Il sito indica anche una sede in Via Eleonora Duse 5G, Roma (tel. 06 8070361) | Che ruolo ha la sede di Roma?']),['p']))
D.append(('abbazia-di-san-gaudenzio','https://www.abbazia.it/',dict(
 rs='Casa Vinicola Abbazia di San Gaudenzio s.r.l.; P.IVA 03159210040', sede='Via Abbazia 6, 12058 Santo Stefano Belbo (CN)', sede_p=True,
 sito='https://www.abbazia.it/', storia='Il sito indica la famiglia Santero come proprietaria e gestore della cantina (sezione «La Famiglia»)',
 vini_nota_p='Il sito elenca linee (Fortuna, Atmosphere, Zoë, Panorama) e cita Moscato, Asti e Prosecco senza indicare le denominazioni',
 domande=['Vini Prosecco DOC | Il sito non indica denominazioni | Quali sono i vini Prosecco DOC e con quale marchio?']),['p']))
D.append(('antonio-facchin-figli','http://www.antoniofacchin.com/',dict(
 rs='Antonio Facchin & Figli s.s. Società Agricola; P.IVA 03750810263', sede='Via Barucchella 10, 31020 San Polo di Piave (TV)',
 sito='http://www.antoniofacchin.com/', storia='Attiva dal 1870; oggi quarta generazione: i fratelli Angelo e Giuseppe, entrambi enologi, seguono cantina e vigneti; la sorella Giusi gestisce l’agriturismo, nato nel 1996',
 vini_c=[('Millesimato Brut','Conegliano Valdobbiadene Prosecco Superiore DOCG','—')], filtrati=True,
 vini_nota_p='Il sito ha una categoria «Prosecco DOC e DOCG» senza elencare le singole etichette',
 premi='Il sito dichiara riconoscimenti in concorsi nazionali e internazionali, senza indicare concorsi, anni o medaglie',
 domande=['Vini Prosecco DOC | Il sito non elenca le etichette Prosecco DOC | Quali sono i vini Prosecco DOC e con quale marchio?']),['p','c']))
D.append(('antonio-introvigne','http://www.introvigne.it/',dict(
 rs='Società Agricola Antonio Introvigne S.S.; P.IVA 05529310269', sede='Via Roma 275, 31043 Fontanelle (TV)', contatti='Tel. +39 0422 749106; cell. +39 351 3184536 (Elia) e +39 360 953356 (Antonio); vini.introvigne@gmail.com',
 sito='http://www.introvigne.it/', storia='Il sito parla di viticoltura «da sempre» e di una «tradizione vinicola scritta nel DNA»; non indica anno di fondazione né proprietari',
 vini_p=[('Merlot','Venezia DOC','2021')], filtrati=True,
 vini_nota_c='Il sito cita il Prosecco senza specificarne la denominazione',
 premi='Premio Vin Piave 2025 per il Merlot DOC Venezia 2021 (news dell’8 febbraio 2026)',
 domande=['Prosecco | Il sito cita il Prosecco ma non indica se DOC o DOCG | Quali sono i Prosecco e con quale denominazione?']),['p','c']))
D.append(('arcadia','https://www.lemondewine.com/',dict(
 rs='Arcadia Società Agricola s.r.l. (marchio Le Monde); P.IVA 01119510939', sede='Via Giuseppe Garibaldi 2, Località Le Monde, 33080 Prata di Pordenone (PN)', sede_p=True,
 sito='https://www.lemondewine.com/', desc='Azienda vitivinicola a Prata di Pordenone, nelle Grave del Friuli',
 vini_nota_p='Il sito elenca collezioni (Bianchi, Rossi, Spumanti, Le Icone, Animo) senza indicare le denominazioni',
 domande=['Vini Prosecco DOC | Il sito non indica denominazioni | Quali sono i vini Prosecco DOC e con quale marchio?']),['p']))
D.append(('barollo','https://www.barollo.com/',dict(
 rs='Società Agricola Barollo Marco e Nicola S.S.; P.IVA 03669680286', sede='Via Rio Serva 4B, 31022 Preganziol (TV)', sede_diversa=True, contatti='Tel. +39 0422 633014; info@barollo.com',
 sito='https://www.barollo.com/', storia='Il sito dice: «Da oltre vent’anni produciamo vini»; non indica proprietari né anno di fondazione',
 vini_nota_p='Il sito elenca Prosecco Rosé Millesimato Brut, Prosecco Barollo Millesimato Brut e Metodo Classico Riserva Alfredo Barollo senza indicare le denominazioni',
 domande=['Sede | La mappa del Consorzio indica Via Belludi, Padova; il sito indica Preganziol | Qual è la sede dell’azienda e a cosa corrisponde l’indirizzo di Padova?','Vini Prosecco DOC | Il sito non indica denominazioni per etichetta | Quali sono i vini Prosecco DOC?']),['p']))
D.append(('barro-sante','http://www.barrosante.com/',dict(
 rs='Azienda Agricola Barro Sante; P.IVA 01436370264', sede='Via Muggia 36, 31045 Motta di Livenza (TV)', contatti='Tel. 0422 768130; cell. +39 348 6404270; info@barrosante.com',
 sito='http://www.barrosante.com/', storia='Nata con il fondatore Sante Barro nei primi anni del Novecento, nel territorio della DOC Prosecco tra le province di Treviso e Venezia; il sito parla di produzione «dalla famiglia Barro»',
 vini_p=[('Extra Dry','Prosecco DOC','—')], filtrati=True),['p']))
D.append(('battista-ii','https://www.battista2.it/',dict(
 rs='Az. Agr. Battista II di Lorenzonetto Enologo Mauro', sede='Via Lignano Sabbiadoro 16, 33050 Pertegada di Latisana (UD)', contatti='Tel. +39 0431 55054; info@battista2.it',
 sito='https://www.battista2.it/', storia='Avviata nel 1968 da Giovanni Battista Lorenzonetto e dalla moglie Luciana a Pertegada; oggi la guida il figlio Mauro, enologo',
 vini_nota_p='Il sito parla di «12 varietà di vini» (rossi, bianchi, frizzanti) senza indicare le denominazioni',
 domande=['Partita IVA | Non indicata nel sito | Qual è la P.IVA?','Vini Prosecco DOC | Il sito non indica denominazioni | Quali sono i vini Prosecco DOC?']),['p']))
D.append(('biancavigna','https://www.biancavigna.it/',dict(
 rs='BiancaVigna S.S. Agricola; P.IVA e C.F. 04103630267', contatti='Tel. 0438 788403; cell. +39 345 4059568; info@biancavigna.it',
 sito='https://www.biancavigna.it/', desc='Azienda con 30 ettari di vigna nelle zone DOCG e DOC',
 vini_p=[('Extra Dry','Prosecco DOC','—'),('Brut','Prosecco DOC','—'),('Rosé','Prosecco Rosé DOC','—'),('Frizzante','Prosecco DOC','—')],
 vini_c=[('Extra Dry Millesimato','Conegliano Valdobbiadene DOCG','—'),('Brut Millesimato','Conegliano Valdobbiadene DOCG','—'),('Brut Millesimato biologico','Conegliano Valdobbiadene DOCG','—'),('Rive di Collalto Extra Dry Millesimato','Conegliano Valdobbiadene DOCG (Rive di Collalto)','—'),('Rive di Soligo Extra Brut Millesimato','Conegliano Valdobbiadene DOCG (Rive di Soligo)','—'),('Rive di Ogliano Extra Brut Millesimato','Conegliano Valdobbiadene DOCG (Rive di Ogliano)','—'),('SL Brut Nature Millesimato','Conegliano Valdobbiadene DOCG','—')], filtrati=True,
 domande=['Storia | Il sito cita la sezione «La Storia di BiancaVigna, una giovane tradizione» ma il testo non era leggibile | Quando è nata l’azienda e chi la possiede?']),['p','c']))
D.append(('bisol-desiderio-figli','https://www.bisol.it/',dict(
 sito='https://www.bisol.it/',
 vini_nota_p='Il sito cita il Cartizze DOCG e il Prosecco Superiore di Valdobbiadene, senza elencare le singole etichette',
 domande=['Anno di fondazione | Il sito riporta 1542 nel titolo e 1952 nel nome del sito | Qual è l’anno corretto?','Ragione sociale e P.IVA | Non indicate nelle pagine lette | Quali sono i dati societari?']),['p']))
D.append(('borgoluce','http://www.borgoluce.it',dict(
 rs='Borgoluce Società Agricola s.s.; P.IVA 03766630267',
 sito='http://www.borgoluce.it', desc='Tenuta di 1000 ettari a Susegana (TV), tra Venezia e le Dolomiti; coltiva direttamente le proprie vigne e ha una cantina all’interno della tenuta',
 vini_nota_p='Il sito cita il Conegliano Valdobbiadene Prosecco Superiore DOCG e le categorie Biologici, Bollicine e Vini Fermi, senza elencare le etichette',
 vini_nota_c='Il sito cita il Conegliano Valdobbiadene Prosecco Superiore DOCG e le categorie Biologici, Bollicine e Vini Fermi, senza elencare le etichette',
 domande=['Vini | Il sito non elenca le etichette con denominazione | Quali sono i vini a denominazione?']),['p','c']))
for base,U,d,kinds in D:
    for k in kinds:
        path=(SP if k=='p' else SC)%base
        assert os.path.exists(path),path
        apply(path,U,d,k)
        print('ok',path)
