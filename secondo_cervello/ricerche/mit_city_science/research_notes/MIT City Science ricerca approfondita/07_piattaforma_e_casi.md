# 07 - La piattaforma CityScope e i casi del MIT City Science Group: modelli, IA, esiti, limiti

Data: 2026-10-27. Lingua: italiano. Scopo: capire a fondo cosa hanno fatto Larson, Noyman, Alonso, Grignard, Winder, Zhang, Doorley e colleghi, e cosa ne segue per un dottorato sulla definizione partecipativa di lotti di social housing a Milano, con sole persone e senza developer.

**Legenda.** [V] letto nel PDF intero in questa sessione (con sezione o pagina). [V*] da riassunto di modello di una pagina web o di un PDF (WebFetch): non è lettura diretta. [I] inferenza mia. [H] ipotesi. Parafrasi, nessuna citazione lunga. "Non pubblicato" significa assente dalle fonti che ho potuto aprire, non assente in assoluto.

**Fonti lette per intero ([V]):**
- Noyman, Holtz, Kröger, Noennig, Larson, "FindingPlaces", arXiv:1811.10123, 10 pp. (KES 2017). Volume 112, pp. 2463-2472 e DOI 10.1016/j.procs.2017.08.180 confermati [V*] dal portale di ricerca HCU, non dal PDF.
- Noyman, Sakai, Larson, "CityScopeAR", arXiv:1907.08586, 5 pp. (workshop CHI '18, deposito arXiv 2019).
- Grignard, Macià, Alonso, Noyman, Zhang, Larson, "CityScope Andorra", AAMAS 2018, extended abstract, pp. 1939-1940.
- Zhang, Grignard, Lyons, Aubuchon, Larson, "Real-time Machine Learning Prediction of an Agent-Based Model for Urban Decision-making", AAMAS 2018, extended abstract, pp. 2171-2173 (CityMatrix).
- Yurrita, Grignard, Alonso, Zhang, Jara-Figueroa, Elkatsha, Larson, "Dynamic Urban Planning: an Agent-Based Model Coupling Mobility Mode and Housing Choice. Use case Kendall Square", arXiv:2106.14572 (2021).

**Fonti solo da riassunto ([V*]) o solo abstract:** articolo sui concorsi di progettazione di Amburgo (IJEPR 10(4), 2021: riassunto di modello del PDF dell'archivio HCU); tesi Noyman 2022 (solo abstract); tesi Zhang 2017 (solo abstract); paper Volpe (ICCS 2018, solo abstract; la copia Springer mirror è stata rifiutata dal sistema di permessi e non l'ho aggirata); pagine media.mit.edu, ira.mit.edu e README GitHub.

**Tentativi falliti.** La tesi Noyman (bitstream DSpace, indicata come 327 MB) ha risposto HTTP 429 a tre tentativi (il primo, poi due a circa 70 secondi), nessun byte scaricato. Non ho insistito oltre. Quindi la sintesi "dei casi" della tesi qui sotto è solo quella dell'abstract. Di Taipei e Helsinki non ho trovato nessun caso partecipativo documentato (vedi §9).

---

## 0. La piattaforma CityScope: architettura generale

### (1) Problema e contesto
La linea di ricerca nasce dal Changing Places Group del Media Lab, con radici dichiarate nell'"Augmented Urban Planning Workbench" e nel "Luminous Table" (fine anni Novanta) e nell'idea che il progetto urbano sia un'attività fisica, iterativa e collaborativa mentre gli strumenti CAD sono per singolo utente [V, FindingPlaces §2.1; CityScopeAR, introduzione]. CityScope (dal 2013, secondo CityScopeAR) vuole rendere leggibile a non esperti un sistema di analisi urbana, tenendo "complessità e leggibilità" in equilibrio. Gli autori distinguono "demo" (esperimenti al Media Lab) e "deployment" (strumenti usati in processi locali reali) [V, FindingPlaces §2.1].

### (2) Come funziona
Configurazione generica [V, FindingPlaces §2.2]: un modello fisico (maquette) su un tavolo, un'unità di analisi con telecamere e computer che scansiona la scena in tempo reale, un modulo di feedback (schermi, proiettori, talvolta AR/VR). Gli oggetti sono mattoncini LEGO con codici colore o tag ottici letti da telecamera; la tavola è una griglia fissa, le celle vuote sono bassi mattoncini bianchi che fungono da schermo per i proiettori [V, FindingPlaces §3.2].

Evoluzione del software [V, CityScopeAR "A Networked CityScope"; V* README]:
- 2015: tentativo con UDP (inaffidabile e bloccato dai browser), poi cityIO, un server HTTP in NodeJS, che trasforma l'ecosistema in sistema distribuito: tavolo, dispositivi AR, simulatori e web app sono client dello stesso stato.
- Oggi (README e documentazione, [V*]): cityIO (Rust) conserva per ogni "tabella" un GEOGRID (definizione delle celle e dei tipi) e un GEOGRIDDATA (stato corrente delle celle); gli scanner (CS_CityScoPy in Python, o scanner nel browser) leggono la griglia LEGO a tag e scrivono GEOGRIDDATA; i moduli (Python con la libreria Brix, GAMA, SUMO, rumore) si iscrivono via WebSocket, ricalcolano ad ogni aggiornamento e riscrivono gli indicatori; il front-end cityscopeJS li mostra (radar, heatmap). Il formato JSON esatto di GEOGRID non l'ho potuto leggere (la pagina "CityIO - Module" non lo riporta).

Convenzioni dei repository: `CS_*` strumenti comuni, `CSL_*` repository per città (nota 03).

### (3) Modello matematico e algoritmi
Il framework non impone una funzione di valutazione. Ogni indicatore è una classe Python con `return_indicator(geogrid_data)`; la documentazione di Brix lascia pesi e schema di punteggio "all'autore" e i numeri negli esempi sono segnaposto (anche `random.random()`) [V*, doc Brix; nota 03]. Casi espliciti:
- Diversità d'uso del suolo come entropia di Shannon: per ogni uso si calcola la quota p tra le celle con uso definito e si somma -p·log(p) [V*, README CS_Urban_Indicators].
- Indicatori compositi "Innovation Potential, Mobility Impact, Economic Impact, Social Wellbeing, Environmental Impact": nel README solo nominati e mediati con pesi uguali in un esempio; formule non pubblicate nel README [V*].
- Mobility Service: logit multinomiale a quattro modi (auto, bici, piedi, trasporto pubblico) con "costanti specifiche" modificabili (esempio con ASC del trasporto pubblico a -0,9), logit nidificato per nuovi modi (lambda 0,65 e 0,29 negli esempi), parametri di un nuovo modo come miscela pesata di modi esistenti (β = β_PT·s + β_walk·(1-s), s = 0,5 nell'esempio); scheduler di attività e scelta residenziale a due stadi: equazioni e coefficienti non pubblicati nel README; output CO2 e impatto sanitario normalizzati con minimi e massimi dichiarati [V*, README CS_Mobility_Service].

### (4) Uso di IA/ML
Nel nucleo: nessuno obbligatorio. ML compare come modulo (CNN surrogato in CityMatrix, §6; regressore k-NN in Dynamic Urban Planning, §8; GAN in "Deep Image of the City", §10). Il README del Mobility Service ha una funzione per generare dati di addestramento per surrogati ML [V*].

### (5) Cosa ha funzionato
Funziona come infrastruttura di ricerca e dimostrazione: moduli indipendenti, repliche in più città, 64 repository pubblici, licenza prevalente GPL-3.0 (nota 03). Il disaccoppiamento via cityIO è la scelta architetturale più riutilizzabile.

### (6) Non ha funzionato o non è dimostrato
Documentazione incompleta e in cambiamento ("work in progress" dichiarato); CityScopeAR e CityMatrix archiviati; Brix fermo all'ultima release di PyPI del 2021 (nota 03). Il formato GEOGRID e i pesi degli indicatori reali non sono nella documentazione che ho potuto leggere.

### (7) Limiti e bias
La griglia regolare impone una rasterizzazione (vedi §4, Grasbrook); i pesi stanno nel codice dell'autore del modulo, quindi chi scrive il modulo decide cosa conta [I]. Basso numero di manutentori (nota 03) [I].

### (8) Lezioni per Milano [I]
(a) Separare stato (lotti scelti) da valutazione (moduli) è una buona idea anche in un foglio di calcolo. (b) Un indicatore deve avere formula, normalizzazione e peso scritti e versionati: il punto debole del framework è proprio ciò che la tesi deve rendere esplicito. (c) La griglia di celle è poco adatta ai lotti catastali irregolari.

---

## 1. FindingPlaces (Amburgo, 2016)

### (1) Problema e contesto
Nel 2015 la Germania ricevette 442.000 domande di asilo; Amburgo concentrava le strutture in alcuni quartieri e vi furono proteste. Il primo sindaco Scholz avviò un dialogo con i cittadini; a febbraio 2016 incaricò il City Science Lab (HCU-MIT) di costruire in tre mesi un processo per trovare sistemazione a circa 79.000 rifugiati previsti. I risultati dovevano diventare raccomandazioni per la decisione politica [V, §1.1-1.2]. Obiettivo operativo: siti per 20.000 persone entro fine 2016 [V, §4.3].

### (2) Come funziona
Processo: 34 workshop da due ore (maggio-luglio 2016) all'HCU, sette distretti, quasi 400 partecipanti, fino a 20 invitati per sessione e 11 di media; registrazione online senza restrizioni, una sola sessione per distretto a persona; promozione con circa 40.000 opuscoli [V, §4.1]. Équipe di 6-8 persone: moderatore (agenzia steg), verbalizzante, ricercatore, tecnico, rappresentanti dello staff centrale rifugiati (ZKF) e del distretto [V, §4.2].

Tre stazioni [V, §4.3]: città (filmato, domanda guida "quali particelle comunali sono adatte", contatore che scende da 20.000 in tempo reale); distretto (tavolo CS con immagine satellitare, aree colorate per classe di inadeguatezza: rosso alta, arancione media, giallo probabilmente adatta; i partecipanti scelgono aree di interesse per conoscenza locale, equità di distribuzione o colore); quartiere (secondo tavolo CS, classi a tratteggio, un segnaposto su una particella mostra superficie, norme di piano, vincoli; si calcola e mostra una capacità potenziale; la discussione a pro e contro viene registrata e mostrata). La proposta si fa con un secondo pezzo che indica da 40 a 1.500 posti, e il dato compare subito su tutti gli schermi.

Tecnica [V, §3.2-3.3]: piccoli oggetti LEGO colorati sul lato inferiore, appoggiati su un piano trasparente a griglia quadrata; quattro telecamere sotto il tavolo, due single-board computer in streaming (ffmpeg), riconoscimento con OpenCV e numpy contro una tabella di codici colore noti; stato inviato via pub/sub (Crossbar, Autobahn su WebSocket) a un server GeoServer con PostGIS; client OpenLayers; backend Python. Ogni tavolo con proiettori; il tavolo "distretto" mostra la mappa dinamica. Rete locale HCU.

### (3) Modello matematico e algoritmi
Esplicito: classificazione in tre classi di inadeguatezza ottenuta "intersecando e pesando" strati (proprietà comunale, uso corrente, vincoli come riserve naturali). Alta: area significativamente toccata da criteri molto restrittivi (tutela naturalistica, cimiteri, forte rumore). Media: non toccata in modo significativo da quelli, ma da criteri meno restrittivi (parchi, aree ricreative, linee ad alta tensione). Bassa o nulla: nessun criterio molto restrittivo e criteri meno restrittivi su meno del 50% dell'area [V, §3.3]. Il 50% è l'unica soglia numerica.
Non pubblicati: i pesi, le soglie di "significativamente", la formula della capacità (solo un esempio di mattoncino da 50 persone, §3.1), il numero di particelle del dataset [V, confermato in nota 06]. Non c'è ottimizzazione: nessun algoritmo sceglie le particelle.

### (4) IA/ML
Nessuna. Visione artificiale classica (soglie su colore, OpenCV). [I] È un sistema di supporto alla conoscenza, non di decisione.

### (5) Cosa ha funzionato
Imbuto documentato [V, §4.4]: 161 localizzazioni proposte, soluzioni per quasi 24.000 persone (oltre l'obiettivo); quasi tre quarti giudicati non adatti in prima valutazione, 44 fattibili; 24 escluse dopo esame di dettaglio; 6 con raccomandazione di attuazione (circa 750 posti, circa 4% del target di 20.000) e 10 per pianificazione futura. Esiti e motivi pubblicati online entro due settimane dallo staff centrale [V, §4.4]. Qualitativamente: discussioni "per lo più calme e costruttive"; le critiche di "partecipazione finta" calavano con informazioni precise e passaggio a luoghi concreti; i partecipanti non potevano respingere una particella senza argomenti comprensibili agli altri; idee ideali dovevano superare un "controllo di realtà" normativo [V, §4.5].
Motivi di scarto [V, §4.4]: più della metà delle particelle proposte erano parchi, verde, paesaggio o aree agricole tutelate; circa il 15% campi sportivi o parchi giochi; più di un terzo respinto per indisponibilità dovuta ad altri usi, un altro terzo per conflitti d'uso.

### (6) Non ha funzionato o non è dimostrato
- Il giudizio "esperienza positiva" è degli stakeholder e degli autori, senza questionari o metriche per FindingPlaces [V, §5; nota 06].
- La quadratura non è spiegata: 44 fattibili, 24 escluse, 6 + 10 = 16; restano 4 non spiegate [V, nota 06].
- Il PDF non dice quante proposte ricadessero nelle classi GIS rosse, arancioni o gialle: il rapporto tra classi di pre-screening ed esito amministrativo è ignoto. Quindi non si può dire se il pre-screening abbia "funzionato" [V, nota 06 punto 1].
- Nessun follow-up sugli insediamenti realizzati. Le cifre delle pagine promozionali (9 siti, 1.500 persone, referendum) non compaiono nel paper (nota 06).
- Il mandato era di raccomandazioni: la decisione è rimasta amministrativa.

### (7) Limiti e bias
Dichiarati [V, §5]: tempi stretti; sede unica (HCU) con bias di selezione; pochi dati urbani; difficoltà dei non esperti con mappe e satellite. Minacce dichiarate: pre-elaborazione dei dati che permette manipolazione (codifica colore suggestiva), comunicazione fuorviante dei risultati, strumentalizzazione politica. Sospetto di manipolazione dei dati già espresso dai partecipanti [V, §4.5]. [I] Non dichiarati: il colore rosso/arancione/giallo fa da ancoraggio; registrazione aperta ma pubblico auto-selezionato; nessuna misura di chi abbia parlato di più; gli abitanti dei quartieri toccati non sono tracciati.

### (8) Lezioni per Milano [I]
1. Il modello trasferibile è il processo: mostrare i vincoli durante la proposta, contatore di fabbisogno, pubblicare esiti e motivi di scarto. 2. La lacuna da non ripetere: pesi e soglie non pubblicati. In una tesi con persone, la classificazione dei lotti deve avere pesi pubblici e confrontabili (due configurazioni, vedi H3 della nota 05). 3. Misurare l'imbuto per classe di pre-screening, cosa che Amburgo non fa. 4. Il pre-screening è pre-decisione: va dichiarato come tale. 5. Il valore dell'esperienza (il "controllo di realtà") è argomento di comprensione, non di qualità della decisione [H].

---

## 2. Boston BRT (2015) e CS PlayGround (Kendall)

### (1) Problema e contesto
Boston BRT: il Mobility Futures Collaborative (DUSP) e il Changing Places Group volevano mostrare ai residenti gli effetti di corridoi di autobus rapidi [V, FindingPlaces §2.3; V* MIT News 2015]. PlayGround: ripensare la riqualificazione di Kendall Square e dell'est del campus MIT con una zonizzazione dinamica [V, §2.3].

### (2) Come funziona
BRT: tre scale, regione (touchscreen web), quartiere e strada (due tavoli CS); sei workshop da due ore a ottobre 2015 con registrazione, orientamento, esplorazione e questionario; facilitatori comunitari per ridurre l'impressione che il controllo spetti agli sviluppatori [V, §2.3]. Evento di lancio 7 ottobre, workshop 8-10 ottobre, mostra 11-14 ottobre; piattaforma web CoAXs; partner Barr Foundation, Nuestra Comunidad [V*, MIT News]. CityScopeAR cita "oltre 300 partecipanti" in eventi con due tavoli [V, CityScopeAR "Tests"].
PlayGround: due gruppi, uno con carta e penna e uno con il tavolo tangibile, video registrati e codificati con uno schema predefinito di azioni, gesti e comunicazione [V, §2.3].

### (3) Modello matematico
Non pubblicato in queste fonti (BRT: prestazioni di corridoio non descritte; PlayGround: "feedback di violazione di zonizzazione" come regola di vincolo, senza formule).

### (4) IA/ML
Nessuna.

### (5) Cosa ha funzionato
BRT: i questionari di uscita e le riunioni successive indicano apprendimento "notevole"; i modelli multiscala favorivano la co-creazione [V, §2.3]. PlayGround: il codice di osservazione mostra più attività e comprensione condivisa con il tavolo; gli autori concludono che le TUI sono "superiori" alla partecipazione tradizionale in prototipazione rapida, collaborazione e decisione [V, §2.3, dalle fonti [11][12] Alrashed et al. 2015].

### (6) Non ha funzionato o non è dimostrato
BRT: pochi pezzi interagibili, esplorazione limitata; a nessuna scala sono stati documentati i risultati prodotti dagli utenti (corridoio preferito, disponibilità a rinunciare a parcheggi) [V, §2.3]. PlayGround: il paper FindingPlaces non riporta dimensione del campione, statistiche né effect size.

### (7) Limiti e bias
Campione PlayGround: comunità MIT (studenti, staff) [V, §2.3]. [I] Il confronto carta/tavolo sull'attività non misura la qualità della decisione.

### (8) Lezioni per Milano [I]
Documentare gli esiti individuali dei partecipanti (cosa hanno scelto) fin dall'inizio, cosa che BRT ha omesso. Prevedere un braccio di controllo (scheda cartacea) come in PlayGround, ma con misura delle scelte, non solo del comportamento.

---

## 3. CityScopeAR (2015-2019) e Andorra (AnodrrAR)

### (1) Problema e contesto
I CS fisici non mostravano volumi 3D, non permettevano più livelli dati insieme e non raccoglievano sistematicamente il feedback degli utenti; il sondaggio cartaceo era il solo strumento [V, CityScopeAR "Augmenting CityScope"]. Andorra: ricerca con lo Stato di Andorra; circa 80.000 residenti e oltre 8 milioni di visitatori l'anno [V, AAMAS Andorra §2].

### (2) Come funziona
Prototipo con laptop e webcam, Unity3d e Vuforia, poi ARtoolkit e tablet; poi Google Tango (inizio 2016) per un migliore riconoscimento in luce difficile, poi ARCore/ARKit (da fine 2017) [V]. Il modello CS è un'ancora: i dispositivi posizionano e scalano le modifiche su ancore geolocalizzate nel modello virtuale via cityIO; gli utenti, vicini o remoti, selezionano edifici, parchi, strade, commentano e mettono "mi piace"; è possibile scorrere la storia delle modifiche [V, CityScopeAR, fig. 4].
Andorra [V, AAMAS Andorra]: tavolo topografico 3D di Andorra la Vella ed Escaldes-Engordany (il resto del Paese come cluster astratti), interfaccia CityMatrix per modificare la struttura, AR via cityIO con quattro strati (origini da dati telecom, ambiente costruito, rappresentazione 3D delle iterazioni, analisi di mobilità). Livello computazionale in GAMA e Processing.

### (3) Modello matematico
Andorra ABM [V]: stato dell'agente = paese di residenza, origine (da dati telecom), destinazione preferita (sottomodulo decisionale non descritto), distanza, velocità, strade percorribili. Il comportamento segue la matrice origine-destinazione calcolata dai Call Detail Records, vincolata alla rete stradale pesata; in caso di alta congestione il percorso viene ricalcolato e, se un'amenità è piena, se ne sceglie un'altra. Dati CDR anonimizzati con SHA-512, tre anni (2014-2016). Parametri, regole di scelta della destinazione, calibrazione e validazione: non pubblicati nell'extended abstract.
CityScopeAR: nessun modello matematico (è un'interfaccia).

### (4) IA/ML
Nessuna in questi due lavori; l'ABM è esplicito.

### (5) Cosa ha funzionato
CityScopeAR: deployment a Barcellona (Smart Cities, T1 2016, quasi 200 commenti al giorno registrati), Caldea (esposizione permanente dal T1 2017), versioni analoghe a HCU 2016, Volpe 2017, Tongji (Shanghai) 2017 [V]. Andorra: installazione definitiva ad agosto 2017, "decine di workshop, classi e oltre un centinaio di dimostrazioni pubblico-private", dichiarato come prova di efficacia come strumento di engagement civico [V, AAMAS §4].

### (6) Non ha funzionato o non è dimostrato
Tango limita l'adozione (hardware raro) [V]. Nessuna valutazione del contenuto dei commenti, della rappresentatività o dell'effetto sul progetto. Il conteggio dei commenti è un indicatore di volume. Andorra: nessuna misura di accuratezza dell'ABM; "efficiente" non ha metrica. Il repository CityScopeAR è archiviato (nota 03).

### (7) Limiti e bias
Gli autori avvertono che allargare il pubblico può far crescere i costi di deliberazione "in modo esponenziale", senza misurarlo [V, Discussion]. [I] Commenti geolocalizzati: chi commenta è chi ha accesso al dispositivo e al luogo; mancano dati demografici.

### (8) Lezioni per Milano [I]
Il commento ancorato a un luogo e la cronologia delle modifiche sono un buon registro di tracciabilità per un tavolo sui lotti. Contare commenti non basta: serve profilo (anche minimo) di chi commenta e una regola di sintesi dichiarata.

---

## 4. Hamburg Grasbrook: strumento per concorsi di progettazione (IJEPR 2021) [V*]

Fonte: riassunto di modello del PDF dell'archivio HCU, non lettura diretta; autori e dettagli bibliografici secondo nota 05 (López Baeza e altri, IJEPR 10(4), 121-137).

### (1) Problema e contesto
Concorso a dialogo competitivo della HafenCity Hamburg GmbH per Grasbrook: sei studi di urbanistica e sei di paesaggio, formati tre team misti (dicembre 2019), vincitore scelto da una giuria ad aprile 2020. Le analisi esperte (rumore, microclima, vento, ombre, traffico, ciclo dell'acqua) arrivavano dopo; la giuria doveva confrontare proposte in formati disomogenei. CityScope girò come esperimento scientifico parallelo, senza valore giuridico. Workshop con i cittadini si erano svolti tra dicembre 2018 e marzo 2019 [V*].

### (2) Come funziona
Front-end, moduli dockerizzati e hub cityIO, scambio HTTP. Il progetto è rasterizzato in celle da 16 m × 16 m, quote discretizzate (4 m a terra, 3 m ai piani); ogni cella ha stato costruito/non costruito e funzione principale (residenza, commercio, istruzione, passeggiata, strada, parco). Motivazione: larghezza delle strade, profondità degli edifici per luce e ventilazione, livello di dettaglio gestibile in tempo reale. Credenziali individuali per squadra [V*].

### (3) Modello matematico
- Rumore: software IFSTTAR con implementazione semplificata della norma francese NMPB-08, sorgenti strade e ferrovie secondo carico atteso, diffrazione e riflessione, indice LDEN.
- Acque meteoriche: deflusso per cella = area × coefficiente di deflusso × pioggia annua; coefficienti dalla Tabella 9 della DIN 1986-100:2016-12 (valori non riportati nel paper).
- Pedonabilità: isocrona a 5 minuti verso scuola, museo e alimentari; tre profili (adulto, bambino, sedia a rotelle) con velocità e superfici percorribili diverse; flood fill con Dijkstra sulla griglia; velocità non riportate.
- Superficie lorda di pavimento (GFA) per categoria (residenza, commercio, altro).
Come la giuria usasse i valori (pesi, soglie): non descritto [V*].

### (4) IA/ML
Nessuna.

### (5) Cosa ha funzionato [V*]
Confronto del rumore con la consulenza esterna sul progetto vincitore: differenze oltre 10 dB su meno del 7,5% dell'area; 53% dell'area entro 5 dB; 39,5% tra 5 e 10 dB; valori generalmente più bassi, pattern spaziali simili. GFA: otto istanze, in sette su otto differenza assoluta tra 1% e 27% (media 14%).

### (6) Non ha funzionato o non è dimostrato [V*]
Acque e pedonabilità: nessuna accuratezza numerica, solo confronto qualitativo; l'acqua non include topografia e infrastrutture. GFA: un caso con differenza del 170% nella categoria "altro" per classificazione ambigua. Moduli microclima e dinamiche sociali ancora in sviluppo. Resistenza degli studi sotto pressione di tempo e possibile resistenza della giuria se l'algoritmo contrasta il giudizio esperto.

### (7) Limiti e bias
La rasterizzazione perde forme curve e libere; input manuale (BIM/CAD non importabile); i risultati dipendono dalla classificazione dell'utente. Gli autori dicono "più oggettiva" la valutazione attesa [nota 05]: [I] l'oggettività è relativa a una griglia e a categorie scelte da loro.

### (8) Lezioni per Milano [I]
Questo è il caso più utile per la verifica: confronto sistematico tra strumento rapido e analisi esperta, con errore dichiarato per modulo. Per i lotti: calcolare un indicatore semplice (superficie, SLP, distanza da servizi) con la stessa tolleranza dichiarata. L'errore dell'1-27% sul GFA mostra che anche l'indicatore più banale dipende dalle categorie scelte.

---

## 5. CityScope Volpe (Kendall Square, 2017-2018) [V* solo abstract]

### (1)-(2) Problema e funzionamento
Il paper di Alonso, Zhang, Grignard, Noyman, Sakai, ElKatsha e altri con Doorley e Larson (ICCS 2018, pp. 253-261) presenta una piattaforma data-driven con interfaccia tangibile per il sito Volpe a Cambridge, simulando gli effetti degli interventi prima del progetto di dettaglio e supportando consenso e ottimizzazione degli obiettivi [V*, pagina media.mit.edu; elenco autori troncato dalla pagina].

### (3)-(7)
Modelli, indicatori, esiti e limiti: non letti (testo non accessibile). L'unica informazione di seconda mano [V, Yurrita et al. 2021, §3.2] è che il calcolo della diversità di reddito usa la formula di Shannon-Weaver "come nella piattaforma CityScope [Volpe]".

### (8) Lezioni per Milano [I]
Nessuna lezione fondata; il caso va letto per intero prima di essere usato.

---

## 6. CityMatrix (Zhang 2017; AAMAS 2018) [V]

### (1) Problema e contesto
L'impegno comunitario nelle decisioni urbane è tardivo e poco informato; gli strumenti tradizionali richiedono anni di formazione [V, AAMAS 2018 p. 2171].

### (2) Come funziona
Tavolo con mattoncini LEGO otticamente taggati: ogni cella può diventare uno di sei tipi di edificio, strada o cortile; cursore e dock per la densità. Feedback: heatmap e radar con cinque metriche (densità, diversità, energia, traffico, solare). Quattro livelli: input utente, valutazione delle prestazioni, suggerimento di ottimizzazione, visualizzazione [V].

### (3) Modello matematico e algoritmi
ABM del traffico in GAMA, che assume viaggi di una flotta efficiente di veicoli autonomi condivisi; 24 ore a passi di 1 minuto, 1 minuto per simulazione. Addestramento: 10.000 configurazioni simulate (8 computer, 18 ore), 7.000 per il training e 3.000 per il test. Input 19×19×2. Suggerimento: ricerca casuale tra le mosse possibili a partire dallo stato corrente, con gli slider degli utenti che fissano i pesi degli obiettivi; la funzione di punteggio complessiva e la normalizzazione delle cinque metriche non sono pubblicate nell'abstract [V]. Dettagli della tesi: non letti.

### (4) IA/ML
CNN a tre strati convoluzionali (TensorFlow/Keras), efficace per la piccola dimensione dell'input e del dataset; migliore R² 0,86 contro 0,571 della regressione lineare, obiettivo dichiarato R² 0,8; inferenza in meno di 10 ms contro circa 1 minuto dell'ABM [V]. Il paper non specifica se l'R² sia calcolato sul test. Un secondo paper (Aubuchon, Lyons, Larson, ACADIA 2018) parla di CNN per traffico e solare, "migliaia di volte più veloci" [V*, abstract].

### (5) Cosa ha funzionato
Il surrogato approssima l'ABM con velocità interattiva. Cinque test pilota (gruppi da 4, 20 utenti in tutto, misti professionisti e non): i log mostrano che i suggerimenti hanno aiutato a stabilizzare e migliorare il punteggio collettivo nel tempo; l'85% degli utenti li ha trovati utili [V].

### (6) Non ha funzionato o non è dimostrato
Il surrogato è validato contro l'ABM stesso [V]; [I] l'ABM, che assume veicoli autonomi condivisi, non può avere riscontro empirico diretto. Test di generalizzazione fuori dalla distribuzione: non riportati. Pilota piccolo, senza gruppo di controllo senza IA nei dati del paper (la tesi dice di aver testato volontari con e senza suggerimenti [V*]).

### (7) Limiti e bias
Il "punteggio totale" cresce perché l'ottimizzatore lo ottimizza: è un risultato quasi circolare [I]. L'85% di utenti soddisfatti è su 20 persone, in gran parte con background urbano [V: gruppi misti, composizione non dettagliata].

### (8) Lezioni per Milano [I]
Un suggeritore che propone mosse su pesi scelti dagli utenti è esattamente il rischio di "automation bias" per lotti ERP; per la tesi, meglio un valutatore (che mostra) che un ottimizzatore (che propone). Il surrogato ML ha senso solo se c'è un simulatore con dati reali da imitare: a Milano non c'è.

---

## 7. Dynamic Urban Planning: scelta residenziale e mobilità, Kendall Square (2021) [V]

### (1) Problema e contesto
Il gruppo vuole un sistema di incentivi dinamici per case a prezzi accessibili entro 20 minuti a piedi dal lavoro; serve prevedere la scelta residenziale e di mobilità. Caso: Kendall Square, dove il costo delle case è esploso [V, §1 e §4].

### (2) Come funziona
GAMA; agenti "persone" con profilo di reddito (otto profili), lavoro in un edificio non residenziale; ambiente: block group del censimento, edifici dell'area, rete stradale. Dati di offerta da web scraping di annunci [V, §3.1].

### (3) Modello matematico
Iterazione 0: unità residenziale casuale; modi disponibili secondo il possesso di mezzi e la zona; punteggio di ogni modo come combinazione lineare dei criteri (prezzo, tempo, difficoltà, "schema sociale"). Esempio di pesi sintetici (Tab. 1): per redditi $45-60k prezzo -0,8, tempo -0,8, difficoltà -0,7, schema 0,7; per $100-125k -0,6, -0,9, -0,8, 0,95. Modi (Tab. 2): bici 0,01 $/km, 5 km/h; bus 0,1 $/km, 20 km/h; auto 0,32 $/km, 30 km/h.
Iterazioni successive: a ogni passo a ogni agente si assegna a caso un'alternativa abitativa; l'agente si sposta se il punteggio dell'alternativa supera quello corrente; i fattori sono prezzo, tempo di pendolarismo col modo migliore, preferenza di zona e accettazione della diversità. La diversità è Shannon-Weaver sulle fasce di reddito nell'edificio o nel block group. Si itera fino a che i movimenti tendono a zero. Esempio di pesi abitativi (Tab. 3): prezzo -0,8, accettazione della diversità 0, peso zona 0,4 (reddito basso); -0,5, -0,5, 0,6 (reddito $100-125k). Sono "dati sintetici" nell'esempio [V, tabelle].
Calibrazione: 8 fattori × 8 profili = 64 variabili; errore abitativo = RMSE tra la quota reale e simulata di ogni profilo per block group (reale ricostruita dai dati di spostamento e dal reddito medio di censimento); errore sui modi = RMSE rispetto a dati comunali di gestione della domanda di trasporto; esplorazione con hill climbing e prove batch; risultato: errore medio di 3,87% sull'abitazione e 2,30% sulla mobilità [V, §4].
Repository: regressore k-NN addestrato sui risultati batch (80/20) per prevedere in tempo quasi reale quota di chi vive e lavora nell'area, modi, tempo medio di spostamento, occupazione della griglia [V*, README CS_Dynamic_Urban_Planning].

### (4) IA/ML
Hill climbing per calibrare; k-NN come surrogato [V*]. Nessun LLM.

### (5) Cosa ha funzionato
La procedura di calibrazione converge a errori percentuali bassi sul caso. Il paper dichiara un metodo generico: cambiando i dati si applica ad altre città [V, §6].

### (6) Non ha funzionato o non è dimostrato
Il paper non descrive una validazione fuori campione: dai dati dichiarati si usano gli stessi dati censuari per calibrare e per misurare l'errore [I, non confermato nel testo]. L'hill climbing dipende dal punto di partenza (ammesso dagli autori, §5). Il calcolo in tempo reale è un vincolo aperto. Nessuna prova che gli incentivi funzionino: il lavoro è la "prima fase".

### (7) Limiti e bias
Pesi e criteri "dalla bibliografia"; "zona" aggrega molti attributi (verde, scuole, cibo); il modello è per lavoratori dell'area, non per chi cerca alloggio in graduatoria. Il reddito entra come otto fasce, non come ISEE e spesa residua.

### (8) Lezioni per Milano [I]
È il lavoro del gruppo più vicino al tema housing: mostra un modo esplicito di scrivere i criteri abitativi con pesi leggibili e di calibrarli per errore. Ma i pesi sono di agenti simulati, non elicitati da persone: una tesi con persone può sostituire i pesi sintetici con pesi elicitati e testare se rientrano nel range simulato (H7 nota 05). Il comportamento "si sposta se il punteggio è maggiore" è un modello di mercato, non di assegnazione di ERP.

---

## 8. Corktown/Detroit (Ford, 2019-2020), Riyadh, Champs-Élysées, Guadalajara CCU [V*]

Fonti: pagine progetto media.mit.edu e post di Winder su ira.mit.edu (riassunti di modello); nessun paper.

- Corktown (Ford, 30 acri): popolazione sintetica da censimento per scelta di casa, attività e modo (logit nidificato calibrato su indagini di viaggio), cinque categorie di indicatori (prestazione economica, potenziale di innovazione, mobilità sostenibile, edifici sostenibili, benefici comunitari), strumento web cityscopeJS dove si "dipingono" usi del suolo sulle celle; cinque scenari fissi. Esito dichiarato: le singole misure migliorano alcuni indicatori ma peggiorano altri; l'insieme compatto e misto migliora tutte le dimensioni. Valori degli indicatori non pubblicati nella pagina. [I] Il risultato dipende da indicatori e pesi scelti con Ford, non da una partecipazione di residenti.
- Riyadh (workshop di un'ora): quattro squadre da cinque del Riyadh Development Authority ridisegnano un quartiere; tre metriche (pedonabilità, energia degli edifici, luce diurna); tavolo AR con feedback a colori. Esito: forte coinvolgimento e apprezzamento del feedback immediato; nessuna misura. [V*, post personale di uno degli autori].
- Champs-Élysées (2020, Pavillon de l'Arsenal): ABM su GAMA per visualizzare le proposte; dati sintetici o stimati; nessun esito misurato [V*].
- CityScope Guadalajara (Centro Cultural Universitario): sistema per scenari su 82 ettari (modello su 456 ha), 14 indicatori, due scenari completi (stato attuale e masterplan) [V*]. Il paper di Palomo-Briones e altri (2026) è citato solo come titolo. Un lavoro separato sulla percezione di sicurezza a Lomas del Centinela (workshop SIGKDD 2020) compare con solo titolo; il legame con CityScope non è stabilito [V*].

Lezioni [I]: i casi con committente aziendale o accademico mostrano uno strumento di prova di scenari; non mostrano partecipazione di abitanti. Non trasferibili al caso senza developer.

---

## 9. Taipei e Helsinki: cosa si sa davvero

- Taipei: City Science Lab @ Taipei Tech (NTUT) fondato nel 2017, orientato a smart city, veicoli autonomi, robotica, IA generativa; la pagina non cita CityScope né progetti specifici [V*]. FindingPlaces elenca deployment a Taiwan senza dettagli [V, §2.1]. Un paper CHI EA '24 di una ricercatrice dell'Università Nazionale Cheng Kung usa il nome "CityScope" per un'app AR di meteorologia (AprilTag e rilevamento di piani, dati dell'ufficio meteo di Taiwan) [V]: [I] non l'ho potuto ricondurre al gruppo MIT, non va usato come caso del gruppo.
- Helsinki: non ho trovato nessun caso CityScope a Helsinki. Esiste un progetto Aalto-MIT (Otaniemi, sviluppo del campus) con piano triennale, descritto al futuro, senza esiti [V*].

Conclusione: per Taipei e Helsinki non c'è materiale partecipativo documentato in fonti aperte che ho trovato. Non ho prove di assenza.

---

## 10. Altri lavori e la tesi Noyman 2022

- "Deep Image of the City" (Noyman, 2019): una DCGAN addestrata sul dataset Cityscapes genera un rendering di strada dopo ogni modifica al tavolo; nessuna valutazione descritta [V*].
- Tesi Noyman (maggio 2022, rel. Larson) [V*, solo abstract]: quattro temi (Insight, Transformation, Prediction, Consensus); casi citati: alloggi per rifugiati in Germania, mappatura della sicurezza a Guadalajara, co-creazione di trasporto a Boston; conclusione dichiarata che CityScope ha sostenuto, migliorato e talvolta sostituito il decision-making tradizionale, e che "costruisce agency" tra chi era escluso. [I] Frasi di abstract, non evidenza: le sezioni di valutazione non le ho lette. Un'analisi dei casi richiede la lettura integrale (da ritentare: il server ha risposto 429).

---

## Sintesi critica trasversale

1. Cosa funziona, con evidenza: infrastruttura modulare (cityIO + moduli); imbuto di Amburgo con motivi di scarto pubblicati; confronto quantitativo con esperti a Grasbrook (rumore, GFA); surrogato ML veloce rispetto all'ABM (R² 0,86 sull'ABM). Tutto è evidenza degli stessi autori; nelle note 05 non risultano valutazioni indipendenti.
2. Cosa non è dimostrato: effetto sulla qualità della decisione, rappresentatività, impatto sull'attuazione (6 siti su 161 a Amburgo; nessun seguito noto).
3. Dove i pesi sono pubblicati: Dynamic Urban Planning (tabelle sintetiche) e README Brix (segnaposto). Dove no: FindingPlaces, CityMatrix (punteggio), Andorra, Volpe, indicatori compositi.
4. Per la tesi [I]: il contributo più difendibile sarebbe fare ciò che il gruppo non fa: pubblicare pesi e soglie dei lotti, misurare l'imbuto per classe di pre-screening, elicitare pesi da persone reali e confrontare con i pesi simulati, registrare chi decide cosa, riportare i rifiuti. L'alternativa più economica al software è un foglio di calcolo con indicatori per lotto (H nota 03).

## Lacune residue
Tesi Noyman 2022 e Zhang 2017 (429/non letti); paper Volpe, Guadalajara 2026, Andorra completo; formato GEOGRID; pesi di FindingPlaces; testo diretto dell'articolo IJEPR (solo riassunto); casi di Taipei e Helsinki.
