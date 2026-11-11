# Vuoti urbani da immagini satellitari e aeree: modelli, uso reale, potenziale, fattibilità a Milano (ticket #36)

Data: 2026-11-11. Parte di #15. Domanda: esistono modelli che riconoscono i vuoti urbani (aree dismesse, incolte, sottoutilizzate) da immagini e ne stimano il potenziale, chi li usa con quale accuratezza validata, e si possono usare a Milano con dati aperti per trovare "aree grigie" non registrate come dismesse?

**Legenda.** [V] letto sulla fonte primaria in questa sessione (abstract, pagina ufficiale, PDF o file di licenza). [S] da fonte secondaria o da un riassunto di ricerca web, non riletto sulla fonte. [I] inferenza mia. [H] ipotesi. [L] lacuna.

**Limiti del metodo.** Per gli articoli Elsevier (ScienceDirect) non ho potuto aprire il testo integrale: dominio bloccato o 403. Per questi ho letto solo l'abstract (OpenAlex, Crossref, DOAJ) e le cifre dell'articolo sono [S]. Le cifre [V] di Urban Atlas, AerialWaste e ISPRA vengono dai PDF ufficiali, letti con `pdftotext`. Nessuna cifra di questa scheda va citata in tesi senza riaprire la fonte.

---

## 1. Risposta breve

1. **I modelli esistono, ma sono quasi tutti prototipi di ricerca.** Il riferimento più solido è Mao et al. 2022: segmentazione DeepLabv3 su 36 città cinesi, con codice, pesi e risultati aperti. Ha però una precisione modesta proprio sulla classe "vuoto": produttore e utente intorno al 66–67% [S]. Il prodotto operativo europeo più vicino, Urban Atlas 2018 classe 13400 "Land without current use", è fatto a mano da fotointerpreti su immagini VHR. Anche così la validazione ufficiale gli dà un'accuratezza dell'utente del 59,44% (approccio cieco) e un'accuratezza del produttore minima del 17,20% (34,93% con l'approccio di plausibilità) [V]. Il "vuoto" è la classe più difficile di tutte, anche per gli esseri umani.
2. **Nella pratica le città non usano modelli su immagini per trovare vuoti.** Usano registri amministrativi incrociati (Philadelphia, dal 2016 [V]), censimenti sul campo (Detroit 2013–14 [S], Cleveland 2015 e 2022 [S]) e filtri GIS a regole (Nottingham: da oltre 7.000 siti a 384 [V]). Le immagini con IA sono in fase pilota: Cleveland con telecamere su auto, 2025–26 [S]; il MHCLG britannico con gli embedding geospaziali per il brownfield, in sperimentazione nel 2026 e senza risultati pubblicati [V]. In Lombardia l'unico uso operativo vicino riguarda le **discariche abusive**, non i vuoti: ARPA con Politecnico, su ortofoto AGEA [V].
3. **Il "potenziale" si stima quasi sempre fuori dall'immagine**, con analisi multicriterio o modelli su variabili socio-spaziali: TIMBRE [V], Jinan [V], il registro brownfield inglese [V]. Nessuna fonte trovata stima il potenziale abitativo o sociale dalle sole immagini [L].
4. **Milano:** un pilota a basso costo con dati aperti è fattibile: embedding AlphaEarth a 10 m (CC BY 4.0) [V], le etichette che abbiamo e una validazione cieca su ortofoto. Ma le etichette sono parziali e distorte, e la risoluzione di 10 m non vede gli edifici dismessi con il tetto intatto, che a Milano sono la parte principale del dismesso [I]. Il collo di bottiglia vero è la validazione, non il modello. La Base L v2 non ha passato il controllo su ortofoto (0,34 contro una soglia di 0,70) [V, repo].

**Raccomandazione: rinviare**, con una condizione di riapertura precisa (§7). Prima di un modello conviene aggiungere due fonti istituzionali non-IA già esistenti: lo strato regionale "Aree della rigenerazione" e il database del dismesso del Politecnico (MAUD).

---

## 2. Modelli (domanda 1)

### 2.1 Tabella

| Famiglia | Lavoro di riferimento | Ingressi e risoluzione | Etichette | Accuratezza riportata e validazione | Codice, pesi, licenza |
|---|---|---|---|---|---|
| Segmentazione CNN del vuoto urbano | **Mao, Zheng, Meng, Zhou, Zhao, Yang, Long 2022**, *Landscape and Urban Planning*, doi:10.1016/j.landurbplan.2022.104384 [V metadati] | immagini ad alta risoluzione, risoluzione consigliata intorno a 1,6 m [V README] | maschere manuali in 3 città rappresentative (Pechino, Shenzhen, Lanzhou), poi applicate per gruppo di città a 36 città [S] | "oltre il 90% del livello di revisori professionisti" (accordo con esperti, non mIoU) [S]; sulla sola classe vuoto, produttore 65,87% e utente 67,42% [S, da verificare sul testo] | codice GPL-3.0 [V LICENSE]; DeepLabv3 con ResNet-18, 4 modelli addestrati su link esterni [V README]; risultati per 36 città su Mendeley Data, doi:10.17632/3c8myvygjj.1, CC BY 4.0 [V DataCite] |
| Vuoto industriale (CNN più filtri) | **Sun, Hu, Han, Wang, Zheng 2023**, *ISPRS IJGI* 12(10):409, doi:10.3390/ijgi12100409 [V abstract] | immagini telerilevate più densità di popolazione e temperatura superficiale per filtrare le predizioni [V] | aree industriali dismesse a Tangshan [V] | HRNet "model accuracy" 97,84% [V abstract]; [I] è un'accuratezza in pixel su una classe rara, quindi gonfiata dalle aree di sfondo | [L] |
| Regole più fusione dati (open source) | **Xu & Ehlers 2022**, *Computers, Environment and Urban Systems*, doi:10.1016/j.compenvurbsys.2021.101729 [V abstract] | immagini telerilevate, strati GIS, dati di citizen science; tipologia in 4 classi (infrastrutture, siti naturali sfavorevoli, residui o riserve, brownfield) [V] | regole per tipo, nessun addestramento [V] | 63 distretti tedeschi; controllo di qualità su foto aeree aperte [V]; accuratezza complessiva 96,3% [S], ma il controllo sovrapponeva i siti trovati a foto aeree e Google, quindi misura la precisione e non il richiamo [S] | articolo CC BY [V OpenAlex]; software libero [V] |
| Brownfield, classificazione di scena | **Dürrbeck et al. 2024**, *EcoBrownfieldNet*, LNNS, doi:10.1007/978-981-97-4799-3_35 [V metadati]; BrownViTNet (stesso filone, CNN più ViT su ortofoto DOP20 tedesche) [S] | immagini satellitari pubbliche, oltre 2.000 [S]; ortofoto DOP20 e immagini Google o Bing [S] | brownfield, area attiva, cantiere [S] | [L] cifre non lette | [L] |
| Case abbandonate da street view | **Zou & Wang 2021**, *ISPRS J. Photogramm. Remote Sens.*, doi:10.1016/j.isprsjprs.2021.03.020 [V metadati]; **Zou & Wang 2022**, *Int. J. Appl. Earth Obs. Geoinf.*, doi:10.1016/j.jag.2022.103018 [V abstract] | Google Street View (2021); VHR diurno, luci notturne VHR e GSV fusi con Dempster-Shafer più random forest geografica (2022) [V] | case abbandonate a livello di singolo edificio; Detroit, Buffalo, Cleveland [V] | "promising performance" nelle due città [V]; cifre [L] | [L]; GSV non è un dato aperto [I] |
| Indicatori di degrado da street view | Detroit, *Urban Blight Tracker* (Development Seed con CPAL e Kaart, 2024) [S]; Midtown Detroit, Faster R-CNN su serie storiche GSV, PLOS ONE 2022 [S] | immagini stradali | finestre murate o rotte, lotti vuoti, gravità [S] | [L] | [L] |
| Luci notturne | **Chen et al. 2015**, *IEEE JSTARS* 8(5), doi:10.1109/jstars.2015.2418201 [V abstract] | NPP-VIIRS più copertura del suolo [V] | tassi di vacanza statistici di 15 aree metropolitane USA [V] | "forte correlazione" con i dati statistici [V] | [I] scala metropolitana o di griglia da 500 m: inutile per il singolo lotto a Milano |
| Foundation model: Prithvi | **Prithvi-EO-1.0** (arXiv 2310.18660) e **2.0** (arXiv 2412.02732), NASA e IBM [V abstract] | HLS (Landsat e Sentinel-2) a **30 m**, serie temporali [V] | da affinare con poche etichette [V] | benchmark generali (GEO-Bench), nessuno sul vuoto urbano [V] | pesi Apache-2.0 su Hugging Face [V] |
| Foundation model: SatMAE | **Cong et al. 2022**, arXiv 2207.08051 [V abstract] | multispettrale e temporale [V] | affinamento [V] | +14% nella classificazione della copertura del suolo rispetto allo stato dell'arte di allora [V] | **CC BY-NC 4.0** [V LICENSE] |
| Foundation model: Clay v1.5 | Clay Foundation [V README e specifica] | Sentinel-2, Landsat, Sentinel-1, NAIP, LINZ, MODIS, con dimensioni e bande qualsiasi: **accetta ortofoto aeree RGB** [V] | embedding, poi classificatore leggero [V] | [L] nessuna valutazione sul vuoto | codice **e pesi** Apache-2.0 [V] |
| Foundation model: AlphaEarth e Satellite Embedding | **Brown et al. 2025**, arXiv 2507.22291 [V abstract]; collezione GEE `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` [V] | fusione di più sensori (Sentinel-1 e 2, Landsat e altri) → vettore a 64 dimensioni per pixel, **10 m**, annuale 2017–2024 [V] | poche etichette (pensato per "sparse label data") [V] | "unico a superare in modo consistente" gli altri metodi di featurization nelle valutazioni degli autori, senza riaddestramento [V abstract]; nessuna valutazione sul vuoto [L] | **CC BY 4.0** con attribuzione obbligatoria [V]; modello non rilasciato, solo gli embedding [I] |
| SAM e derivati | **Segment Anything**, Kirillov et al., arXiv 2304.02643 [V]; **samgeo**, Wu & Osco 2023, JOSS, doi:10.21105/joss.05663 [V README] | qualsiasi immagine RGB [V] | nessuna (zero-shot); prompt a punti o box [V] | zero-shot "spesso competitivo" su compiti generali [V]; [I] SAM segmenta oggetti ma non sa *che cosa* sia un vuoto: serve un classificatore a valle | SAM Apache-2.0 [V]; samgeo MIT [V] |
| Analogo lombardo (non vuoti) | **AerialWaste**: Torres & Fraternali 2023, *Scientific Data*, doi:10.1038/s41597-023-01976-9 [V]; Torres & Fraternali 2021, *Remote Sensing* 13:4520 [V abstract] | **ortofoto AGEA 2018 (circa 20 cm)**, WorldView-3 (circa 30 cm), Google Earth (circa 50 cm), riquadri da 210 × 210 m [V] | 3.478 positivi e 6.956 negativi, etichettati dai fotointerpreti di **ARPA Lombardia**, 487 comuni [V] | sole immagini AGEA: AP 94,5% e F1 88,2% [V]; 2021: precisione 88% e richiamo 87% in un'area di test [V] | dataset pubblico (aerialwaste.org) [V]; licenza [L] |

### 2.2 Che cosa dicono, insieme [I]
- Non esiste un modello "vuoto urbano" pronto da scaricare e applicare a Milano. Il più vicino (Mao 2022) è addestrato su città cinesi a circa 1,6 m e riporta circa il 66% sulla classe vuoto [S]. Va riaddestrato.
- Il dato più importante è il **soffitto umano**: in Urban Atlas la classe 13400 è definita in modo esplicito ("aree in attesa di essere usate o riusate… brownfield… nessun uso agricolo o ricreativo… vegetazione ruderale secondaria" [V, Mapping Guide v6.3 p. 30]) ed è prodotta da fotointerpreti. Eppure la validazione cieca le dà un'accuratezza dell'utente del 59,44% su 31 punti [V, tabella 16]. Un modello addestrato su etichette così non può superare la loro affidabilità.
- I foundation model riducono il bisogno di etichette, non il bisogno di **definire** il vuoto. Nessuno è stato validato su questo compito [L].

---

## 3. Chi li usa oggi (domanda 2)

| Chi | Che cosa fa | Immagini con IA? | Stato | Marca |
|---|---|---|---|---|
| **Philadelphia** (OIT con L&I, OPA, Land Bank, Water Dept.) | *Vacant Property Indicators*: per ogni particella somma indicatori amministrativi di vacanza (violazioni, codice OPA, ecc.); entra se ne soddisfa almeno metà; più indicatori concordano, più alta è l'affidabilità | **No**, dati amministrativi | operativo dal 14/11/2016 | [V comunicato] |
| Philadelphia (strumento successivo) | combina immagini aeree, street view, violazioni e dati termici in GIS | parzialmente | data e metodo [L] | [S WHYY] |
| **Detroit**, Motor City Mapping | rilievo di oltre 370.000 particelle con tablet e foto (dicembre 2013 – febbraio 2014), per la Blight Task Force e la Land Bank | **No**, rilievo umano | concluso | [S] |
| **Cleveland** | auto con 2 telecamere (City Detect), oltre 150.000 proprietà fotografate, possibili problemi segnalati sul 46% delle particelle; "nessuno viene sanzionato solo sulla base dell'auto, tutto è confermato" | sì, da strada | pilota annuale, 85.000 $; anno 2 da decidere | [S News5 2026] |
| **Nottingham e Sevenoaks** (UK) | LANDCLAN: filtri GIS 2D a regole, da oltre 7.000 a 384 siti, poi valutazione dei funzionari | **No** | pilota, caso di studio governativo | [V gov.uk] |
| **Lewisham** (UK) | strumento IA e GIS: oltre 3.000 piccoli siti potenziali | non dichiarato | pilota PropTech Fund | [S LocalGov] |
| **MHCLG AI Lab** con Homes England e Imago (UK) | sta "testando il potenziale degli embedding per localizzare il brownfield in tutta l'Inghilterra"; risultati promessi, non pubblicati | sì (embedding) | sperimentazione, luglio 2026 | [V blog] |
| **Inghilterra**, registri brownfield (SI 2017/403) | registro obbligatorio dei comuni; criteri: almeno 0,25 ha o almeno 5 alloggi, adatto, disponibile, realizzabile entro 15 anni | **No** | obbligo di legge | [V reg. 4] |
| **Copernicus Urban Atlas 2018** | classe 13400 su 0,25 ha di MMU; immagini VHR 2017–2019, segmentazione automatica solo per le classi di base, poi "raffinamento manuale con interpretazione visiva… necessario" | in minima parte | operativo; Milano è coperta [I] | [V Mapping Guide] |
| **ISPRA e SNPA** | carta di copertura del suolo da Sentinel-1 e 2, classificazione semi-automatica più fotointerpretazione; accuratezza globale dell'83% su campione stratificato (carta 2018, non la carta del consumo di suolo) | sì (classificazione, non deep learning sul vuoto) | operativo | [V Ecoscienza 5/2021] |
| **Regione Lombardia**, "Aree della rigenerazione" | strato aggiornato dai Comuni dal 2018 tramite editing web, partendo dal censimento 2008–2010 (aree dismesse oltre 2.000 m² se industriali); in Provincia di Varese le aree sono state riconosciute **a mano su ortofoto**; mostra anche lo strato comunale di Milano (art. 11 NdA) | **No** | operativo | [V scheda tecnica 2019] |
| **Politecnico di Milano** (MAUD e DAStU) | database del dismesso lombardo: 3.393 aree a ottobre 2019 [S]; poi circa 3.800 aree e circa 5.300 ha, di cui oltre 1.000 nella Città metropolitana [S]; anche da fonti web | **No** | ricerca, accesso [L] | [S] |
| **ARPA Lombardia e Politecnico** (PERIVALLON) | IA su ortofoto e immagini satellitari per le **discariche abusive**; pilota su oltre 100 comuni lombardi | **sì** | pilota e ricerca | [V Polimi] |
| **Comune di Milano** | ds503: edifici degradati o dismessi 2014–2017 (art. 11 NdA PdR) | **No** | fermo al 2017 | [V, repo `milano_dati/01`] |

**Lettura [I].** Dove l'adozione è reale (Philadelphia, i registri inglesi, Urban Atlas, la Regione Lombardia), il "vuoto" nasce da **dati amministrativi e giudizio umano**. Le immagini con IA servono, quando servono, a **segnalare candidati** che un funzionario poi verifica (Cleveland, MHCLG, ARPA). Non ho trovato nessun caso italiano o milanese di IA su immagini per i vuoti urbani [L, ricerca negativa: web, Polimi, Comune].

---

## 4. Stimare il "potenziale", non solo trovare il vuoto (domanda 3)

- **TIMBRE Brownfield Prioritization Tool**: Pizzol et al. 2016, *J. Environmental Management*, doi:10.1016/j.jenvman.2015.09.030 [V metadati]. Strumento web che ordina portafogli di brownfield con un'analisi multicriterio su "fattori di successo" scelti con gli stakeholder (potenziale di riuso, commerciabilità, rischio) [S]. Il progetto europeo è FP7 [S].
- **Jinan**: Gulshad et al. 2022, *Land* 11(3):317, doi:10.3390/land11030317 [V abstract]. Stacking ANN-RF-SVM per la probabilità che un'area vuota diventi infrastruttura verde: AUC 0,941. Fattori principali: temperatura superficiale, distanza dall'acqua, densità di popolazione, pioggia [V]. È una *predizione di ciò che è successo*, non una valutazione di ciò che sarebbe desiderabile [I].
- **Registro brownfield inglese**: il "potenziale" è **giuridico**: adatto, disponibile (il proprietario ha dichiarato di voler vendere o costruire) e realizzabile entro 15 anni secondo l'autorità locale [V reg. 4]. La disponibilità non si vede da nessuna immagine [I].
- **Pechino** (riuso di aree liberate, random forest più indici di idoneità, coerenza oltre il 78% con gli esiti 2021) [S, solo comunicato stampa].
- **Lacuna [L]**: nessuno studio trovato valuta il potenziale *sociale* (abitazione accessibile, servizi di quartiere) di vuoti trovati da immagini. Il potenziale si costruisce con criteri espliciti fuori dal modello. Per la tesi è una buona notizia [I]: la Base L lo fa già con criteri del PGT, vincoli e capacità, e l'area di attivazione (CONTEXT.md) è esattamente un giudizio di potenziale non abitativo.

---

## 5. Fattibilità a Milano con dati aperti (domanda 4)

### 5.1 Immagini

| Fonte | Risoluzione | Licenza | Note |
|---|---|---|---|
| Sentinel-2 | 10 m (bande visibili e NIR) | aperta (Copernicus) [I, nota] | serie dal 2015: utile per il *cambiamento* (vegetazione spontanea, suolo nudo) |
| AlphaEarth Satellite Embedding | 10 m, 64 dimensioni, annuale 2017–2024 | **CC BY 4.0** [V] | pronta in GEE; nessun preprocessing |
| Ortofoto AGEA 2018–2019 (servizio di Regione Lombardia) | fino a 0,26 m/pixel dal servizio a tasselli [V, repo L v2]; circa 20 cm all'origine [V AerialWaste] | proprietà AGEA, "visione e stampa con citazione" [S, repo]; record INSPIRE non aperto [L] | **licenza da chiarire prima di addestrare**: gli embedding derivati sono un'opera derivata? [L] |
| Ortofoto 2021 | [S] circa 0,2 m | come sopra | il servizio WMS ha risposto con errore 400 l'11/11 [V, repo] |
| Google ed ESRI | — | non aperte | escluse |
| Street view | — | GSV non aperto [I]; Mapillary: copertura di Milano [L] | utile solo per validare a campione |
| Urban Atlas 2018 (Milano FUA) | vettoriale, MMU 0,25 ha | Copernicus, aperta [I] | etichetta indipendente da DUSAF per la classe 13400 [I] |

**Problema di scala [I].** Un pixel a 10 m è 100 m². La soglia di 1.500 m² della Base L equivale a 15 pixel. Sono pochi ma sufficienti per un vettore medio di particella. Non bastano però per distinguere un cortile da un'area incolta. A 10 m un **edificio dismesso con il tetto intatto** è identico a un edificio in uso. Per i lotti da riusare (diruti, ds503) l'immagine dall'alto aiuta solo se il degrado è visibile: tetto crollato, vegetazione interna (cfr. codice T3/V2 in `esperimenti/L_lotti_v2/controllo_umano/casi.csv`).

### 5.2 Etichette che abbiamo e loro distorsioni

| Etichetta | Che cosa registra davvero | Distorsione principale |
|---|---|---|
| DUSAF 8.0 classi 131–134 e 1412 | fotointerpretazione regionale (cave, discariche, cantieri, aree degradate non utilizzate, aree verdi incolte) [V repo] | **circolarità**: è prodotta guardando le stesse ortofoto, quindi un modello impara il fotointerprete e non il vuoto [I]. Le fabbriche dismesse restano spesso codificate come 12111 (produttivo): sottostima sistematica del dismesso edificato [V repo, L v1 G1] |
| PGT, ambiti AT ed ex AMB_DEG | **designazioni di piano**, non stati fisici [I] | il piano registra ciò che il Comune ha già deciso di trasformare: proprio l'opposto di un'area grigia "non registrata" |
| DBT, edifici diruti | stato dell'edificio nel database topografico (2020) [V repo] | solo edifici, non aree; confermati su ortofoto nel 65% dei casi [V, L v2] |
| ds503 (2014–2017) | immobili privati in degrado, tavola R.10 [V repo] | vecchio: confermato su ortofoto solo nel 31% dei casi, molti edifici sono di nuovo in uso [V, L v2] |
| Codifica su ortofoto della Base L v2 | 200 righe codificate (100 lotti e 100 particelle di base) con schema Q1, tetto, vegetazione, uso [V, `tabelle/codifica_ortofoto.csv`] | un solo codificatore, non indipendente [V, L v2 §limiti]; è comunque il miglior seme di negativi e positivi che abbiamo |
| (da acquisire) Regione, "Aree della rigenerazione" | aree segnalate dai Comuni dal 2018 [V] | auto-dichiarazione comunale; scaricabilità [L] |
| (da acquisire) Database MAUD del Politecnico | dismesso lombardo, oltre 1.000 aree nella Città metropolitana [S] | accesso e licenza [L] |

**Distorsione comune [I].** Ogni registro contiene ciò che un'istituzione ha avuto motivo di guardare. Un modello addestrato su questi positivi trova *aree simili a quelle già note*: utile, ma per costruzione cieco alle aree grigie *diverse* da quelle note. È il limite principale del pilota, e va dichiarato.

### 5.3 Pilota minimo (proposta [H], non eseguita)

**Domanda del pilota.** Una classifica di particelle basata su embedding trova aree "vuote o sottoutilizzate" **non presenti in nessun registro** con una precisione superiore al tasso di base, verificata alla cieca?

1. **Unità**: le particelle catastali di Milano di almeno 1.500 m², fuori dai registri noti (DUSAF 13x e 1412, PGT AT e AMB_DEG, ds503, diruti DBT, Aree della rigenerazione), dopo gli stessi filtri E2 della Base L v2 (acque, infrastrutture, verde in uso, residenza occupata).
2. **Caratteristiche**: la media e la deviazione standard degli embedding AlphaEarth per particella, per il 2018 e il 2024, più la distanza coseno tra i due anni come segnale di cambiamento [H]. Nessun dato AGEA nel modello finché la licenza non è chiarita.
3. **Modello**: *positive-unlabeled learning* (PU) o, più semplice, una ricerca di similarità (k-NN coseno) verso i positivi confermati. Positivi: i lotti della Base L v2 codificati "dismesso o libero" su ortofoto e i diruti DBT confermati. Negativi certi: le particelle di base codificate "in uso". Niente reti da addestrare: una regressione logistica o un k-NN su 64 o 128 numeri [I, ponytail].
4. **Uscita**: le prime N = 100 particelle **non registrate**, come "candidati aree grigie da verificare", mai come lotti.
5. **Validazione pre-registrata** (seguendo `esperimenti/PROTOCOLLO_LABORATORIO.md` e la lezione della v1, G2):
   - due codificatori **ciechi** sull'origine (candidato del modello, particella casuale o lotto già noto, mescolati), ortofoto 2021 se il servizio risponde, altrimenti 2018 più Mapillary; κ di Cohen dichiarato;
   - metrica: precisione@100 del modello contro il tasso di base su 100 particelle casuali con gli stessi filtri (nella v2 il tasso di base era 0,09 [0,048; 0,162] [V]);
   - criterio [H]: limite inferiore dell'IC della differenza (Newcombe) di almeno 0,15. Sopralluogo su 10 casi;
   - controllo del richiamo: validazione spaziale per blocchi (leave-NIL-out) sui positivi noti, per misurare se il modello ritrova ciò che è registrato in quartieri che non ha visto;
   - controllo di circolarità: nessuna etichetta di validazione derivata da DUSAF.
6. **Costo stimato [I]**: da 1 a 3 giorni di lavoro più la codifica umana (circa 200 immagini per due codificatori).

### 5.4 Che cosa lo farebbe fallire [I]
- **Il vuoto milanese è soprattutto edificato**: capannoni chiusi, uffici sfitti con il tetto intatto. A 10 m e dall'alto è invisibile. Il pilota troverebbe soprattutto aree *non edificate* (incolti, piazzali), che DUSAF 1412 e 134 in gran parte già coglie.
- **Falsi positivi strutturali** (vale anche per Urban Atlas, dove 13400 si confonde con verde, sport e industriale [V, tabella 16]): parcheggi, scali e depositi ferroviari, cantieri, campi sportivi, orti, cortili grandi, piazzali logistici attivi.
- **Tasso di base basso**: con un'area grigia vera su 10 o 20 particelle, anche un buon ranking dà molti falsi allarmi. Senza un controllo umano robusto il risultato non è interpretabile.
- **Sfasamento temporale**: embedding 2024, ortofoto 2018–2021, ds503 2014–2017.
- **Licenza AGEA**: se non permette l'uso derivato, il ramo ad alta risoluzione (Clay o SAM su ortofoto) è precluso [L].
- **"Sottoutilizzato" non è una proprietà dell'immagine**: dipende da occupazione, proprietà e domanda, dati che mancano [V repo, L v2 §limiti].

---

## 6. Risposte puntuali per la tesi [I]
- La letteratura conferma la scelta della Base L di partire da **registri incrociati** (come Philadelphia) e non da un modello di visione.
- Gli embedding (AlphaEarth, Clay) sono oggi il modo più economico per aggiungere un segnale da immagine a una pipeline tabellare. Lo dice anche il MHCLG [V], che però non ha ancora pubblicato risultati.
- AerialWaste mostra che in Lombardia si può costruire un dataset utile su ortofoto AGEA **se** un ente (ARPA) fornisce migliaia di etichette professionali [V]. Per i vuoti urbani questo ente non c'è: il Comune ha fermato ds503 al 2017.

---

## 7. Raccomandazione

**Rinviare**, non scartare.

Motivi:
1. La Base L v2 non è ancora congelata e ha fallito proprio il controllo su ortofoto (0,34 [0,255; 0,437] contro 0,70) [V]. Una nuova fonte di candidati non validata aggiunge rumore a un sistema che ancora non sa misurare la propria precisione.
2. Lo stato dell'arte non offre un modello trasferibile. Nemmeno gli esseri umani superano circa il 60% di precisione sulla classe vuoto (Urban Atlas) [V].
3. Le fonti istituzionali non-IA (Aree della rigenerazione della Regione, database MAUD del Politecnico) sono più economiche, citabili e coerenti con l'uso reale. Vanno provate prima.

**Condizione di riapertura** (tutte e tre):
- (a) la Base L v3 ha un protocollo di codifica cieca con un secondo codificatore e un κ accettabile;
- (b) è chiarita la licenza AGEA oppure si accetta il solo ramo a 10 m;
- (c) Dennis approva una pre-registrazione del pilota del §5.3, da tenere come esperimento separato e **non** come ingresso della Base L finché non passa il criterio.

Se il pilota passa, i candidati entrano nella Base L come quarta origine "candidato da immagine", sempre soggetta a verifica e mai come lotto per definizione.

---

## 8. Lacune aperte [L]
- Cifre di Mao 2022 (produttore e utente 65,87% e 67,42%), Zou & Wang 2021, EcoBrownfieldNet e Xu & Ehlers (96,3%): da leggere sul testo integrale (ScienceDirect non raggiungibile da qui).
- Licenza e scaricabilità di: ortofoto AGEA 2018 e 2021 (Regione Lombardia), strato "Aree della rigenerazione", database MAUD.
- Copertura Mapillary di Milano.
- Metodo e data dello strumento di Philadelphia descritto da WHYY.
- Esiti della sperimentazione MHCLG sugli embedding per il brownfield (da ricontrollare nel 2027).

---

## 9. Fonti

Lette in questa sessione [V]:
- Mao et al. 2022: metadati https://doi.org/10.1016/j.landurbplan.2022.104384 ; codice https://github.com/SkydustZ/Large-scale-Automatic-Identification-of-Urban-Vacant-Land (LICENSE GPL-3.0); dati https://doi.org/10.17632/3c8myvygjj.1 (CC BY 4.0)
- Sun et al. 2023, abstract: https://doi.org/10.3390/ijgi12100409
- Xu & Ehlers 2022, abstract: https://doi.org/10.1016/j.compenvurbsys.2021.101729
- Zou & Wang 2022, abstract (DOAJ): https://doi.org/10.1016/j.jag.2022.103018
- Chen et al. 2015, abstract: https://doi.org/10.1109/jstars.2015.2418201
- Gulshad et al. 2022, abstract: https://doi.org/10.3390/land11030317
- Pizzol et al. 2016, metadati: https://doi.org/10.1016/j.jenvman.2015.09.030
- Prithvi: https://arxiv.org/abs/2310.18660 , https://arxiv.org/abs/2412.02732 ; Hugging Face `ibm-nasa-geospatial/Prithvi-EO-2.0-300M` (apache-2.0)
- SatMAE: https://arxiv.org/abs/2207.08051 ; LICENSE CC BY-NC 4.0 su github.com/sustainlab-group/SatMAE
- Clay: README e specifica v1.5, github.com/Clay-foundation/model (Apache-2.0, pesi inclusi)
- AlphaEarth: https://arxiv.org/abs/2507.22291 ; https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL
- SAM: https://arxiv.org/abs/2304.02643 ; samgeo https://doi.org/10.21105/joss.05663 (MIT)
- AerialWaste: https://doi.org/10.1038/s41597-023-01976-9 ; https://doi.org/10.3390/rs13224520 ; Polimi, https://www.polimi.it/en/research/news/detail/ai-and-satellites-to-detect-illegal-landfills-with-90-accuracy
- Urban Atlas Mapping Guide v6.3: https://land.copernicus.eu/en/technical-library/urban_atlas_2012_2018_mapping_guide (classe 1.3.4, p. 30; specifiche di prodotto p. 4; metodo §4.2.1–4.2.4)
- Urban Atlas 2018 Validation Report (issue 1.6): https://land.copernicus.eu/en/technical-library/urban-atlas-2018-validation-report (tabelle 16 e 17; sintesi §4.5)
- Munafò, Marinosci, Congedo, *Ecoscienza* 5/2021: https://aggiornati.arpae.it/it/ecoscienza/numeri-ecoscienza/anno-2021/numero-5-anno-2021/programma-copernicus/munafo_et_al_es2021_5.pdf
- Regione Lombardia, scheda tecnica "Aree della Rigenerazione" (10/07/2019): https://www.geoportale.regione.lombardia.it/documents/10180/0/SchedaTecnica_AreeRigenerazione/82fc39a6-644f-4dcd-bdba-0b0e34e9a198
- Philadelphia, comunicato del 14/11/2016: https://www.phila.gov/press-releases/kenney/city-releases-open-data-on-vacant-property-indicators/
- UK SI 2017/403, reg. 4: https://www.legislation.gov.uk/uksi/2017/403/regulation/4/made
- GOV.UK, Nottingham e Sevenoaks: https://www.gov.uk/government/case-studies/nottingham-and-sevenoaks-speed-up-identifying-and-assessing-sites
- MHCLG Digital blog, 16/07/2026: https://mhclgdigital.blog.gov.uk/2026/07/16/from-pixels-to-policy-the-potential-of-geospatial-embeddings-for-mhclg/

Secondarie o giornalistiche [S]:
- Cleveland e City Detect, News5 2026: https://www.news5cleveland.com/news/local-news/cleveland-is-using-ai-to-flag-property-problems-and-fight-blight-heres-how-it-works
- Philadelphia, WHYY: https://whyy.org/articles/philly-inspectors-get-new-eyes-on-vacant-potentially-unsafe-buildings/
- Lewisham, LocalGov 05/08/2026: https://www.localgov.co.uk/Lewisham-identifies-3000-small-sites-for-potential-new-homes-using-AI/64783
- Motor City Mapping: https://data.amerigeoss.org/dataset/motor-city-mapping-certified-results-winter-2013-14-census-tract-aggregation-1b5a5 e articoli Xconomy, Michigan Public 2014
- Dismesso lombardo, dati DAStU: rassegna MAUD https://www.maudlab.polimi.it/wp-content/uploads/2019/11/AD-191114.pdf ; Il Giorno https://www.ilgiorno.it/cronaca/aree-dismesse-lombardia-44a837a7
- Development Seed, Urban Blight Tracker: https://developmentseed.org/blog/2024-07-29-urban-blight-tracker/
- Interne al repo: `esperimenti/L_lotti/REPORT.md`, `esperimenti/L_lotti_v2/REPORT.md`, `esperimenti/L_lotti_v2/esecuzioni/00_preregistrazione.txt`, `secondo_cervello/ricerche/milano_dati/01_audit_dati_e_piani.md`
