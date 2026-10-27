# MIT City Science: cosa esplorare per la Fase 1 (ticket #8)

Data: 2026-10-27. Ambito: partecipazione e definizione dei lotti di social housing a Milano (Spatial Milano Lab).

**Legenda.** [V] letto nella fonte in questa sessione. [S] riportato da una scheda del corpus, non riletto. [I] inferenza. [H] ipotesi. Stati: `verificata` = pagina o PDF aperto e letto; `da verificare` = non aperto.

**Avvertenza sul metodo.** Il tool di fetch restituisce un riassunto prodotto da un modello, non il testo integrale. Anche le mie letture [V] sono quindi di seconda mano rispetto al PDF. Cifre e sezioni vanno ricontrollate sul documento prima di una citazione in tesi. Non ho potuto aprire: il PDF della tesi Noyman 2022 (errore di accesso), la pagina HAL dell'articolo ABM 2018 (blocco anti-bot), né il testo integrale di nessun articolo Springer.

Corpus di partenza: `tesi_out/ricerche_progetti/01_MIT_City_Science/ricerca.md` [S] (README: stato al 2026-10-19) e `03_Analisi Approfondite/37_note_ricerca_grezze/udt_partecipazione.md` [S].

---

## 1. Risposta breve

- **Trasferibile come metodo:** il processo FindingPlaces di Amburgo (pre-screening GIS dei lotti pubblici, tavolo con dati visibili, workshop strutturati), la logica "surrogato ML di un modello ad agenti per feedback in tempo reale", e la costruzione di un indice composto di benessere con formule esplicite.
- **Non trasferibile così com'è:** la CNN sul traffico (dominio, griglia e ipotesi specifici), i valori dell'indice di benessere (dati USA), l'esito numerico di Amburgo (contesto di emergenza e mandato politico).
- **Il corpus afferma meno della fonte** sulla partecipazione (Amburgo era segnato come "menzione" e l'inferenza "i cittadini non sono coinvolti" è smentita) **e più della fonte** su alcune letture di CityScope come strumento di cittadinanza attiva.

---

## 2. Fonti

| # | Autori, anno | Titolo | Sede | DOI / URL | Stato |
|---|---|---|---|---|---|
| 1 | Noyman A., Holtz T., Kröger J., Noennig J.R., Larson K., 2017 | FindingPlaces: HCI Platform for Public Participation in Refugees' Accommodation Process | Procedia Computer Science 112, pp. 2463-2472 (KES 2017, Marsiglia) | DOI 10.1016/j.procs.2017.08.180; `arxiv.org/abs/1811.10123` (arXiv, testo identico al pubblicato secondo la pagina) | **verificata** [V] |
| 2 | Zhang Y., Grignard A., Lyons K., Aubuchon A., Larson K., 2018 | Real-time Machine Learning Prediction of an Agent-Based Model for Urban Decision-making (Extended Abstract) | AAMAS 2018, Stoccolma, pp. 2171-2173 | `ifaamas.csc.liv.ac.uk/Proceedings/aamas2018/pdfs/p2171.pdf` (DOI non trovato) | **verificata** [V] |
| 3 | Zhang Y., 2017 | CityMatrix: an urban decision support system augmented by artificial intelligence | Tesi S.M., MIT Media Arts and Sciences (relatore K. Larson) | `dspace.mit.edu/handle/1721.1/114059` | **verificata** (solo abstract del repository) [V]; testo integrale non letto |
| 4 | Orii L., Alonso L., Larson K., 2020 | Methodology for Establishing Well-Being Urban Indicators at the District Level to be Used on the CityScope Platform | Sustainability 12(22), 9458 | DOI 10.3390/su12229458; `mdpi.com/2071-1050/12/22/9458` | **verificata** [V] |
| 5 | Alonso L., Zhang Y.R., Grignard A., Noyman A., Sakai Y., ElKatsha M., et al., Larson K., 2018 | CityScope: A Data-Driven Interactive Simulation Tool for Urban Design. Use Case Volpe | Unifying Themes in Complex Systems IX (ICCS 2018), Springer, pp. 253-261 | DOI 10.1007/978-3-319-96661-8_27 (da pagina Springer) | **verificata** (solo abstract) [V] |
| 6 | Noyman A., Sakai Y., Larson K., 2019 (arXiv, 19 luglio) | CityScopeAR: Urban Design and Crowdsourced Engagement Platform | arXiv:1907.08586 (cs.HC). La lista MIT di Noyman la dà come CHI 2018 | `arxiv.org/abs/1907.08586`; nessun DOI né riferimento di rivista sull'arXiv | **verificata** (arXiv); sede formale **da verificare** |
| 7 | Noyman A., 2022 | CityScope: An Urban Modeling and Simulation Platform | Tesi di dottorato, MIT Media Arts and Sciences (relatore K. Larson) | `dspace.mit.edu/handle/1721.1/145128` | **verificata** (solo abstract); PDF non aperto |
| 8 | Grignard A., Alonso L., Taillandier P., Gaudou B., Nguyen-Huu T., Gruel W., Larson K., 2018 | The Impact of New Mobility Modes on a City: A Generic Approach Using ABM | Conferenza ICCS 2018, Springer, pp. 272-280 [S] | `media.mit.edu/publications/the-impact-of-new-mobility-modes-on-a-city-a-generic-approach-using-abm/`; DOI non trovato (HAL bloccato) | **da verificare** in questa sessione; [S] "verificata (abstract)" |
| 9 | Larson K., Noyman A., 2016 circa (data dedotta) | Shifting Priorities, Finding Places | Post su Medium (MIT Media Lab), non peer-reviewed | `medium.com/mit-media-lab/shifting-priorities-finding-places-9ad3bdbe38b8` | **verificata** [V] come fonte di parte, non scientifica |
| 10 | MIT Media Lab, s.d. | FindingPlaces (pagina di progetto) | media.mit.edu | `www-prod.media.mit.edu/projects/finding-places/overview/` | **verificata** [V]; fonte di parte |
| 11 | MIT Media Lab, s.d. | CityScope (pagina di progetto) | media.mit.edu | `media.mit.edu/projects/cityscope/overview/` | **verificata** [V] |
| 12 | Hu K., Atchade-Adelomou P., Adornetto C., Mora-Carrero A., Alonso-Pastor L., Noyman A., Liu Y., Larson K., 2025 | Graph RAG as Human Choice Model: Building a Data-Driven Mobility Agent with Preference Chain | arXiv:2508.16172 (cs.AI), preprint | `arxiv.org/abs/2508.16172` | **verificata** (abstract); non peer-reviewed |
| 13 | Noyman A., Larson K., 2020 | A deep image of the city: Generative urban-design visualization | Symposium on Simulation for Architecture and Urban Design (11th) | Solo citazione nella lista autore; nessun DOI né abstract | **da verificare** |
| 14 | Doorley R., Noyman A., Sakai Y., Larson K., 2019 | What's your MoCho? Real-time Mode Choice Prediction Using Discrete Choice Models and a HCI Platform | UrbComp, SIGKDD 2019 | Solo citazione nella lista autore | **da verificare** |

La lista autore (`media.mit.edu/people/noyman/publications/`) è stata letta come indice [V]; le righe 13-14 e la sede CHI 2018 di #6 vengono solo da lì.

---

## 3. Cosa dicono le fonti

### 3.1 Amburgo, FindingPlaces (fonti 1, 9, 10): il caso più vicino ai lotti

- Contesto [V]: nel 2015 Amburgo doveva ospitare circa 79.000 rifugiati previsti; il sindaco Scholz chiese al City Science Lab un processo partecipativo, con circa tre mesi per ideazione e sviluppo. L'obiettivo era usare la conoscenza locale dei cittadini per individuare **lotti di proprietà comunale**.
- Sistema [V]: tavolo con mattoncini colorati letti da quattro camere (OpenCV), backend Python/JavaScript, PostGIS, proiezioni su due tavoli.
- Selezione dei lotti [V]: strati GIS (proprietà, uso del suolo, aree protette, rumore, elettrodotti) incrociati e pesati; i lotti sono classificati in tre classi di indicazione di inadeguatezza e mostrati come base di discussione, non come verdetto. La capacità abitativa stimata è calcolata per lotto. I pesi non sono riportati nel riassunto letto [I: da cercare nel testo integrale].
- Processo [V]: 34 workshop da due ore, maggio-luglio 2016, sette distretti; circa 400 partecipanti (media 11, massimo 20 invitati); tre stazioni (città, distretto, quartiere); proposte da 40 a 1.500 posti per lotto.
- Esiti [V]: 161 lotti proposti, capacità quasi 24.000 posti (sopra il target di 20.000). Circa tre quarti giudicati non idonei dalla valutazione GIS iniziale; 44 fattibili, 24 esclusi dopo verifica; **6 raccomandati per l'attuazione e 10 per il futuro**. I 6 lotti raccomandati valgono circa 750 posti, circa il 4% del target. Oltre metà dei lotti proposti era parco o verde, in gran parte sotto tutela.
- Limiti dichiarati dagli autori [V]: tempi stretti; bias di selezione (workshop solo all'HCU, nessun dato demografico sistematico); alcuni partecipanti sospettavano manipolazione dei dati e parlavano di partecipazione "finta"; difficoltà dei non esperti a leggere mappe e contenuti; i dati preprocessati e i colori potevano influenzare la discussione; rischio di strumentalizzazione politica. La valutazione positiva degli stakeholder è qualitativa e proviene dal team: nessun sondaggio formale né confronto controllato.
- Fonti di parte [V]: il post Medium e la pagina di progetto riportano cifre in parte diverse (es. "oltre 150" lotti, "circa 20" partecipanti a incontro, 40 sedi in revisione accelerata, costruzione avviata in 9 siti per circa 1.500 persone) e rivendicano effetti politici (evitato un referendum) non verificati. La pagina di progetto non cita il dato dei 750 posti.

### 3.2 CNN come surrogato di un ABM (fonti 2, 3)

- Fonte 2 [V]: ABM di traffico in GAMA (24 ore, passo di 1 minuto, circa 1 minuto per run; 10.000 simulazioni in 18 ore su otto computer). Si assume che tutti gli spostamenti usino una flotta condivisa di veicoli autonomi. CNN a tre strati (TensorFlow/Keras), input 19×19×2, 7.000 casi di addestramento e 3.000 di test.
- Metriche [V]: regressione lineare migliore R² = 0,571; CNN migliore R² = 0,86; inferenza sotto 10 ms contro circa 1 minuto dell'ABM.
- Non riportati [V]: filtri, kernel, strati densi, iperparametri; altri modelli provati, senza numeri. L'ottimizzazione dei suggerimenti usa ricerca casuale (sez. 2.5), senza prestazioni riportate.
- Valutazione utenti [V]: cinque test pilota con 20 utenti (professionisti e non); 85% ha trovato utili i suggerimenti (questionario, non misura controllata).
- Fonte 3 [V, solo abstract]: tesi del 2017 con ML per previsioni in tempo reale e ricerca di ottimizzazione per i suggerimenti; ipotesi centrale: uomo più macchina decidono meglio. Test con e senza suggerimenti AI, esito dichiarato "promettente" senza numeri nella pagina.

### 3.3 Indice di benessere (fonte 4)

- Cinque indicatori [V]: Community Connectedness, Safety & Security, Physical Health, Mental Health, Diversity.
- **Le formule sono presenti nell'articolo** [V]: copertura dei parchi (area parchi / area città), accessibilità entro 10 minuti a piedi, giardini comunitari ogni 1.000 residenti con rango percentile, diversità con indice di Simpson (1 − Σp²) su sei dimensioni, media ponderata normalizzata 0-100. **Pesi uguali (w = 1)** per tutti gli attributi e gli indicatori, scelti come default e non da evidenza.
- Sicurezza percepita presa dall'indice Numbeo (a sondaggio): 143 risposte per Boston, 67 per Kansas City [V].
- Limiti dichiarati [V]: scala di città che nasconde differenze di quartiere; normalizzazione min-max lineare; campioni piccoli; nessuna validazione con comunità o lavoro sul campo; solo due città; la tesi "Boston ha più benessere" è definita speculazione.
- **Partecipazione nella costruzione dell'indice: assente** [V]. Il metodo è una sintesi della letteratura e di indici esistenti; la partecipazione compare solo come uso futuro in CityScope.
- Nota [V]: l'articolo è incoerente su Community Connectedness (cinque attributi in un punto, sei in un altro).

### 3.4 CityScope come piattaforma (fonti 5, 6, 7, 11)

- Fonte 11 [V]: CityScope è "un concetto di calcolo condiviso e interattivo per la pianificazione urbana"; dichiara che sviluppo, strumenti e software sono open source, ma la pagina letta non riporta link né licenza [da verificare su GitHub].
- Fonte 5 [V, abstract]: modella gli effetti di interventi prima del progetto di dettaglio, con interazione degli stakeholder in tempo reale, caso Volpe a Kendall Square. Non descrive metodi di partecipazione né esiti misurati.
- Fonte 6 [V]: CityScopeAR aggiunge realtà aumentata e un server di scambio dati (cityIO). Deployment citati: Boston BRT con oltre 300 partecipanti, Andorra, Amburgo, Volpe, Tongji. Nessuna valutazione formale; gli autori dicono che allargare il pubblico può far crescere "esponenzialmente" i costi di deliberazione, senza soluzione proposta. Il paper non cita Guadalajara.
- Fonte 7 [V, abstract]: dissertazione di Noyman con tre applicazioni (alloggi per rifugiati in Germania, mappatura della sicurezza a Guadalajara, co-creazione del trasporto pubblico a Boston). Afferma che CityScope "aiuta a costruire agency" per chi era escluso e che ha "supportato, potenziato e talvolta sostituito" i processi tradizionali. [I] È una dichiarazione dell'autore sul proprio lavoro; il testo integrale (esperimenti di laboratorio, campioni) non è stato letto.

### 3.5 Altri lavori recenti

- Fonte 12 [V]: Preference Chain (Graph RAG + LLM) per simulare scelte di modo di trasporto sul dataset Replica; limiti dichiarati: inferenza lenta, rischio di allucinazioni. Riguarda la mobilità, non i lotti. Preprint.
- Fonti 13-14: titoli di ML (immagine generativa della città; predizione della scelta modale) solo da lista; nessun contenuto letto.
- Ricerca specifica su "urbanistica generata dai cittadini" oltre CityScope/FindingPlaces e Preference Chain: **non trovato nulla di mirato** in queste ricerche. Non è un'assenza provata.

---

## 4. Trasferibilità a Spatial Milano Lab

Non conosco i dati, i lotti e i vincoli del Lab; le valutazioni sono [I] o [H].

### Trasferibile

1. **Pre-screening dei lotti prima del workshop** (fonte 1). [I] Il dato più utile è l'imbuto: 161 lotti proposti, 6 raccomandati (circa 750 posti su 24.000 proposti). Se i cittadini scelgono liberamente, la maggior parte delle proposte cade sui vincoli; mostrare i vincoli durante la proposta è la parte replicabile. Per Milano servirebbero strati equivalenti (proprietà ERP/Comune, PGT, vincoli, rumore, TPL).
2. **Capacità stimata per lotto in tempo reale** (fonte 1). [H] Per i lotti di social housing, un contatore del fabbisogno (come il contatore verso 20.000 posti) rende visibile il trade-off collettivo.
3. **Surrogato ML di un modello ad agenti** (fonte 2). [I] È un pattern tecnico: simulare molti scenari offline, addestrare una rete sulla griglia, ottenere stime in millisecondi. È replicabile se il Lab ha un proprio modello (accessibilità, costo, mix sociale). Il valore del lavoro sta nel confronto con una base di riferimento lineare (0,571 contro 0,86), non nell'architettura, che non è descritta.
4. **Indice composto con formule esplicite** (fonte 4). [I] Accessibilità a 10 minuti a piedi, diversità di Simpson e rango percentile sono formule semplici e riutilizzabili. Vanno rese esplicite le scelte di peso.

### Non trasferibile (o solo con forte rilavorazione)

1. **La CNN del traffico così com'è.** Dominio (flotta di veicoli autonomi condivisi), griglia 19×19×2 e dati simulati sono specifici di CityMatrix; il testo non dà l'architettura per riprodurla.
2. **I valori e le conclusioni dell'indice di benessere.** Dati USA (Numbeo, ParkScore, politiche d'uso della forza); pesi uguali non validati; nessuna partecipazione nella costruzione.
3. **L'esito di Amburgo come prova di efficacia.** Mandato del sindaco, lotti comunali, emergenza, tre mesi; valutazione qualitativa fatta dal team stesso. [I] Non dimostra che la partecipazione migliori la decisione, solo che il processo è stato eseguibile.
4. **L'idea che il tavolo dia potere ai cittadini.** Gli autori ammettono bias di selezione, sospetti di manipolazione e rischio di strumentalizzazione. [H] A Milano, con residenti e liste d'attesa ERP, il reclutamento andrebbe progettato con criteri di rappresentatività che la fonte non offre.
5. **Scalabilità.** Il costo di deliberazione cresce con il pubblico (fonte 6), senza soluzione.

---

## 5. Dove il corpus afferma più (o meno) della fonte

| Punto | Corpus [S] | Fonte [V] | Giudizio |
|---|---|---|---|
| Formula del Well-Being Index | "Non reperita"; PDF MDPI non aperto | Formule (Eq. 1-7) e pesi uguali presenti nell'articolo | Il corpus **afferma meno**: lacuna colmata |
| Amburgo | "Strumento di coinvolgimento degli stakeholder", solo menzione; inferenza: cittadini non coinvolti | 400 cittadini in 34 workshop, scelta di lotti comunali | L'inferenza del corpus (cittadini solo utenti o fonti di dati) **è smentita** per questo caso. Resta valida per Well-Being Index, BoxLab, PEV |
| CNN | R² 0,86, tre strati, 19×19×2, 10.000 casi | Confermati. In più: base lineare unica, flotta AV assunta, 20 utenti, 85% da questionario, ottimizzazione casuale | Il corpus **omette** i limiti; le cifre reggono |
| "CityScope dichiara partecipazione" | Schede: "strumenti partecipativi" | La pagina CityScope non descrive metodi; solo FindingPlaces ha un protocollo documentato | Il corpus **afferma più** per Volpe, Andorra, BostonBRT, Riyadh: restano menzioni senza metodo |
| Esito di Amburgo (24.000 posti) | Non presente | Fonti di parte citano il totale proposto; il dato sui 6 lotti e circa 750 posti sta solo nel paper | Citare il totale senza l'imbuto **sovrastima** l'efficacia |
| CityScopeAR | Assente | Sede: CHI 2018 (lista MIT) contro arXiv 2019; nessun DOI | Da chiarire |
| Volpe | Springer, pp. 253-261 | DOI trovato; la lista MIT riporta anche una versione 2019 con titolo diverso ("Data-driven, evidence-based simulation of urban dynamics") | Possibile duplicato o capitolo gemello: non risolto |
| `udt_partecipazione.md`: lacuna housing | "Nessun articolo UDT aperto affronta la localizzazione di alloggi sociali" | FindingPlaces (localizzazione alloggi per rifugiati) è un controesempio, fuori dal campo UDT | Il giudizio sul vuoto di ricerca va **ridimensionato**: non vale per i tavoli partecipativi, forse ancora per gli UDT |
| `udt_partecipazione.md` e CityScope | CityScope "non aperto" | Aperto in questa sessione (sez. 3.4) | Il corpus non ne fa uso: gap ora colmabile |

Le fonti del file `udt_partecipazione.md` (Azadi, Ketzler, Batty, ecc.) non sono state riverificate qui.

---

## 6. Limiti e bias

- Quasi tutte le fonti MIT hanno gli autori coinvolti nei progetti; le pagine di progetto e il post Medium sono promozionali [V].
- Letture via riassunto automatico (vedi avvertenza); tesi 2017 e 2022 solo da abstract.
- Nessuna valutazione indipendente di FindingPlaces trovata: non è stata cercata letteratura terza sistematica (Scholar, Scopus). [H] Potrebbe esistere critica esterna non individuata.
- Ricerca non esaustiva: nessuna copertura di GitHub (codice, licenza, dataset), Riyadh, BostonBRT, Andorra, Kendall Square ABM, tesi Noyman integrale.
- Pubblicazioni 2025-2026: trovata solo la #12.

## 7. Cosa esplorare in Fase 1 (domande aperte)

1. Leggere il testo integrale di FindingPlaces per i pesi del pre-screening e l'impatto su ogni classe di lotto.
2. Leggere il capitolo "Consensus" e quelli su FindingPlaces della tesi Noyman 2022 per campioni e metodi di valutazione.
3. Controllare codice e licenza di CityScope su GitHub prima di ipotizzare riuso.
4. Cercare critiche indipendenti a FindingPlaces e a CityScope (letteratura PSS e partecipazione).
5. Decidere se per Milano serve davvero un surrogato ML: dipende dall'esistenza di un modello ad agenti proprio e dal tempo di calcolo richiesto.
6. Risolvere DOI e sede di #6, #8, #13, #14.

---

## In breve

Il caso più utile per i lotti è FindingPlaces (Amburgo, 2016): 34 workshop, circa 400 cittadini, 161 lotti comunali proposti, ma solo 6 raccomandati (circa 750 posti su quasi 24.000 proposti). Trasferibile: pre-screening GIS dei lotti, contatore di fabbisogno, surrogato ML di un ABM (CNN R² 0,86 contro regressione 0,571) e indice con formule esplicite. Non trasferibili: la CNN sul traffico, i valori dell'indice di benessere (dati USA, pesi uguali non validati) e l'esito di Amburgo come prova di efficacia (valutazione interna e qualitativa). Il corpus sbaglia nel considerare Amburgo una semplice menzione e nel dire che la formula del benessere manca; omette i limiti della CNN. Non ho potuto aprire la tesi Noyman 2022 né HAL.
