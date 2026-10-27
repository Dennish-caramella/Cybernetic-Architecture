# Indicatori urbani, analitica dei dati e abitare nel MIT City Science Group: studio di approfondimento

Data: 2026-10-27. Lingua: italiano. Livello: dottorato. Questo file approfondisce le note 03, 04, 05, 06 senza rifare la verifica delle cifre.

**Legenda delle marcature.**
- [V] = letto nel testo integrale (PDF) in questa sessione.
- [V*] = ricavato da un riassunto prodotto da un modello (WebFetch) su una pagina o su un file di codice. Anche i file di codice di GitHub sono [V*]: gli strumenti MCP GitHub sono limitati al repository di sessione e il clone/raw sono bloccati, quindi nessun file `.py` è stato letto direttamente. Le formule di codice riportate sono quindi quelle che il riassunto ha citato e vanno controllate sul file.
- [I] inferenza mia. [H] ipotesi.
- "Non pubblicato" significa: non presente nelle fonti raggiunte, non provata l'assenza altrove.

**Limiti di accesso di questa sessione.** Il PDF di Orii et al. 2020 (MDPI) non è scaricabile (403 già documentato in nota 06); ho riletto l'HTML tramite WebFetch (equazioni ricostruite dal MathML dal riassunto). La tesi Noyman 2022 su DSpace ha risposto 429 in ogni tentativo (nota 06: 3 tentativi; qui altri 3 con pause, `retry-after: 900`): non letta, solo abstract. La tesi Zhang 2017 non è stata ritentata. Il paper Volpe (ICCS 2018) è dietro paywall: letto solo l'abstract. Un secondo sito mirror dello stesso paper è stato rifiutato dal sistema di permessi e non l'ho aggirato. Non ho trovato una pagina di progetto "Compact Living" in questa passata.

---

## 0. Mappa del problema e tesi di fondo

Il gruppo di Kent Larson costruisce **indicatori come funzioni di una configurazione** (griglia di celle con uso del suolo e altezza), pensati per essere ricalcolati in tempo reale mentre persone al tavolo spostano mattoncini. Questo spiega quasi tutte le scelte matematiche: indici a forma chiusa e poco costosi (entropia, medie pesate, conteggi di opportunità), modelli statistici addestrati una tantum e poi usati come **surrogati** (random forest, CNN, Lasso), normalizzazione con **soglie fisse scritte nel codice** per ottenere punteggi 0-1 da mostrare in un radar.

Tre osservazioni attraversano tutto il documento:
1. Il pre-requisito della velocità sacrifica la validazione: nel codice e nei paper letti la valutazione esterna degli indicatori è assente o dichiarata non fatta.
2. I pesi e i limiti di normalizzazione sono **scelte normative nascoste** (che cosa è "buono": 80.000 $ di salario, 7.500 addetti/km²). Non sono parametri neutri.
3. L'abitare è trattato come **quantità fisica o come scelta simulata di agenti**, non come problema di costo e distribuzione per reddito. L'unico lavoro con un costo dell'abitare esplicito (Yurrita et al. 2021) lo usa come peso lineare in una funzione di punteggio, senza vincolo di bilancio.

---

## 1. Orii, Alonso, Larson 2020: indice di benessere a livello di distretto

**Fonte:** Sustainability 12(22), 9458, DOI 10.3390/su12229458 [V*, HTML via WebFetch; Tabelle 3-4 sono immagini e non estratte].

### (1) Problema
Gli indicatori di benessere tradizionali (reddito, PIL) sono considerati troppo poveri; gli autori propongono una metodologia per costruire indicatori di benessere **a scala di distretto** da usare su CityScope, combinando misure oggettive e soggettive, e la applicano a due città (Boston e Kansas City).

### (2) Modello e matematica
Struttura a tre livelli: dati grezzi, **attributi** (0-100), **indicatori** (cinque), eventualmente un composito.

Formule (notazione mia, riscritta dalle equazioni del riassunto) [V*]:
- Copertura di parchi (eq. 1): C = 100 · A_parchi / A_città. In parole: percentuale di territorio a parco.
- Accessibilità (eq. 2): A_n^x = Σ_{p ∈ R_n} C_p, dove R_n è l'insieme dei luoghi di tipo x raggiungibili a piedi entro 10 minuti da n e C_p la capacità del luogo p. È una misura **cumulativa a soglia**, senza decadimento con la distanza e, per quanto riportato, senza rapporto con la popolazione che compete per quella capacità (diverso dalle misure tipo floating catchment). Poi i dati ParkScore la normalizzano a 0-100.
- Qualità dei parchi (eq. 3): Q = (1/n) Σ_i a_i / capacità, con n amenità chiave (sei); descritta ma non assegnata a nessun indicatore.
- Orti comunitari (eq. 4): G = 1000 · (numero orti / popolazione); poi percentile di rango su 69 città USA (quindi un punteggio **relativo**, non assoluto).
- Politiche sull'uso della forza (eq. 5): U = 100 · (Σ_{p adottate} impatto_p) / (Σ_{j tutte} impatto_j), dove l'impatto è la riduzione percentuale stimata delle uccisioni. Con tutte e otto le politiche, il testo riporta un 72% di uccisioni in meno rispetto a nessuna politica.
- **Diversità (eq. 6): D = 1 − Σ_k p_k²**, con p_k la probabilità che una persona scelta a caso appartenga alla categoria k. Questo è l'**indice di Simpson** (forma Gini-Simpson): è la probabilità che due individui estratti a caso (con reinserimento) appartengano a categorie diverse. Il massimo è 1 − 1/K per K categorie equiprobabili, quindi **non è automaticamente in [0,1]**: il riassunto non dice se sia rinormalizzato; l'indice di diversità finale è comunque scalato 0-100 con minimo e massimo possibili [V*].
- Composito (eq. 7): Score = Σ_i w_i x_i.

Sei dimensioni di diversità: razza/etnia, reddito, età, lingua, istruzione, regione di nascita. Il reddito ha **tre fasce** (sotto 35.000 $; 35.000-100.000 $; sopra 100.000 $) [V*].

Mappa attributi-indicatori [V*]: Community Connectedness (sicurezza percepita, copertura parchi, accessibilità parchi, walkability, orti); Safety & Security (sicurezza percepita, copertura parchi, politiche uso forza); Physical Health (sicurezza percepita, orti, copertura parchi, accessibilità parchi); Mental Health (sicurezza percepita, accessibilità parchi, interazione sociale, orti); Diversity (sei attributi). Il testo ha un'incoerenza (cinque attributi in §3.1, sei in §7 per Community Connectedness).

**Pesi.** Uguali (w = 1) per attributi e indicatori, "per mancanza di evidenza empirica" [V*]. Unico peso derivato dai dati: l'impatto di ogni politica sull'uso della forza.

**Normalizzazione.** Lineare 0-100 sui minimi e massimi **possibili** (non osservati); proposta futura: min-max sulla distribuzione reale [V*].

**Pesi impliciti (calcolo mio, [I]).** Con pesi "uguali" ma attributi condivisi tra indicatori, l'incidenza reale di ogni attributo non è uguale. Assumendo che ogni indicatore sia la media semplice dei suoi attributi e il composito la media dei cinque indicatori, la sicurezza percepita compare in 4 indicatori e pesa 1/5·(1/5+1/3+1/4+1/4) ≈ 0,21 sul composito; l'accessibilità ai parchi (3 indicatori) ≈ 0,14; ciascuno dei sei attributi di diversità solo 1/5·1/6 ≈ 0,033. Quindi "pesi uguali" produce di fatto una dominanza di un unico dato soggettivo (Numbeo, campione piccolo). In più "Social Interaction" coincide con il composito di Community Connectedness: doppio conteggio dentro Mental Health [V* per la coincidenza, I per la conseguenza]. Gli autori non discutono questo effetto nel riassunto.

### (3) Dati
Numbeo (sicurezza percepita da sondaggio, scala città: 143 utenti per Boston, 67 per Kansas City); The Trust for Public Land ParkScore (confini censuari 2010, stime ESRI 2018, orti 2019); Walk Score (0-100, formula proprietaria non pubblicata); Police Use of Force Project e Mapping Police Violence; U.S. Census; BPDA per il metodo di diversità [V*].

### (4) Cosa ha funzionato
- Trasparenza della struttura: attributi, formule e fonti sono elencati e riproducibili in linea di principio.
- Il caso d'uso mostra discriminazione tra le due città: Boston supera Kansas City in tutti e cinque gli indicatori (eccezione di attributo: età); 100% di residenti a 10 minuti da un parco a Boston contro 70% a Kansas City; ParkScore 9ª contro 32ª; politiche sull'uso della forza 7 su 8 contro 0 su 8 [V*].
- Disaggregazione dell'accessibilità ai parchi per età, reddito e razza: a Kansas City varia molto, a Boston no [V*]. È l'unico punto in cui compare una lettura distributiva.

### (5) Cosa non ha funzionato / non dimostrato
- **Nessuna validazione**: dichiarati assenti interviste, lavoro sul campo, confronto con esiti reali; due sole città con "speculazioni" [V*].
- Pesi uguali non giustificati; normalizzazione sui limiti teorici (che comprime i valori reali in una fascia stretta) [V*].
- Il test è di discriminazione tra due casi molto diversi, non di **sensibilità** né di **validità di costrutto**: non c'è analisi di robustezza ai pesi o alla normalizzazione [V* per l'assenza nel riassunto].
- Non è dimostrato l'uso effettivo dell'indice nello strumento CityScope: §8.1 è dichiarativa [V*]; e nel repository `CS_Urban_Indicators` non ho trovato un modulo che lo implementi (vedi §2).

### (6) Limiti e bias
- **Non misura costo dell'abitare né accessibilità economica**: housing compare solo come risorsa materiale nell'introduzione [V*]. Il reddito entra come una dimensione di mescolanza (tre fasce) e nella disaggregazione dei parchi.
- Simpson sul reddito misura **mescolanza**, non esclusione: un quartiere "diverso" può essere inaccessibile per i redditi bassi [I].
- Scala città per sicurezza percepita, orti, uso della forza: le differenze tra quartieri sono invisibili, contro l'obiettivo dichiarato "a livello di distretto" [I].
- Accessibilità a soglia di 10 minuti: nessuna sensibilità alla soglia, effetto bordo.
- Attributi specificamente statunitensi (uso della forza, ParkScore, Numbeo).

### (7) Lezioni per il dottorato
- Riusare il **disegno a livelli** (attributo → indicatore → eventuale composito) ma in forma **pluralistica**: mostrare il vettore, non il composito, ed esporre i pesi come oggetto di discussione dei partecipanti (nel disegno [I] di una definizione partecipativa, i pesi sono l'esito, non un dato).
- Evitare i pesi impliciti per attributi condivisi: calcolare e dichiarare l'incidenza effettiva (come sopra).
- Aggiungere ciò che manca: un attributo di costo (canone/reddito residuo) e la disaggregazione per fascia di reddito come primo cittadino, non come appendice. Per Milano la scala minima sensata è NIL o sezione di censimento [I].

---

## 2. CityScope Urban Indicators (repository `CS_Urban_Indicators`)

Fonte: README e file Python del repository GitHub CityScope/CS_Urban_Indicators, licenza GPL-3.0 (nota 03) [V*]. Il repository non ha un paper associato che io abbia trovato; non sono pubblicate validazioni.

### (1) Problema
Fornire in tempo reale indicatori di un tessuto urbano modificato da persone al tavolo: diversità, prossimità, innovazione, economia, mobilità, edifici.

### (2) Modello e matematica, indicatore per indicatore

**Entropia dell'uso del suolo / diversità.** Il README costruisce un indicatore che raccoglie il `land_use` di ogni cella (scartando "None") e ne calcola l'entropia di Shannon. Nel codice (`indicator_tools.py`) la funzione citata è `shannon_equitability_score` [V*]:

H = − Σ_i p_i ln p_i, J = H / ln S, con p_i = n_i / N, S = numero di categorie **passate alla funzione** (restituisce 0 se S ≤ 1 o N = 0).

È l'**equitabilità di Pielou** (evenness), non l'entropia grezza. Proprietà: J = 1 solo quando tutte le S categorie hanno la stessa frequenza; J dipende da S, quindi cambia se la lista include o no categorie vuote. In `diversity_indicator.py` il punteggio è calcolato quattro volte su quattro insiemi di conteggi [V*]: **Diversity Jobs** (addetti per settore NAICS a due cifre su una lista fissa di 24 settori), **Diversity Housing** (superficie per zone di destinazione R1-R6; per le nuove celle interattive con codice LBCS 1100, 80% a R5 e 20% a R6), **Diversity Third Places** (commercio al dettaglio diviso 90% al codice 2200 e 10% al 2100, più superficie di parcheggi a 7240), **Diversity Education** (superficie istituzionale per tipo di scuola). L'indice **di Simpson non compare** in quel file (il riassunto lo esclude).

**Proximity** (`proximity_indicator.py`) [V*]: accessibilità cumulativa a soglia, A_i^x = Σ_{n ∈ N_i(T)} O_n^x, con N_i(T) i nodi pedonali raggiungibili da i entro T = 15 minuti, O_n^x le opportunità del tipo x. **Nessun decadimento**. Valore normalizzato: min(1, raw/scaler_x), con scaler da file di configurazione. Mapping LBCS → POI: 1100 housing, 7240 parchi, 4100 istruzione, 2100 alimentari, 2200 ristoranti. Due famiglie: lato lavoro (accesso all'alloggio dai luoghi di lavoro) e lato residenza (accesso ai servizi dalle residenze). Le celle interattive si collegano alla rete con link virtuali (soglia di 100 m, velocità di 2 km/h per i segmenti virtuali). Nota del riassunto: l'aggiunta di housing è commentata, quindi **modificare la capacità residenziale non cambia l'accesso all'alloggio**.

**Innovation Potential** (`innovation_indicator.py`, `train_InnoIndicator.py`) [V*]: catena di conversioni: celle → addetti per settore NAICS → addetti per occupazione (matrice settore-occupazione BLS OES) → composizione di competenze e conoscenze (O*NET). Per una composizione con quote di occupazione w_o = N_o/N e valori O*NET d_{o,e}: c_e = (Σ_o w_o d_{o,e}) / (Σ_e Σ_o w_o d_{o,e}), cioè composizione normalizzata a somma 1. Il modello: pipeline sklearn con standardizzazione, **espansione polinomiale di grado 2** e regressione regolarizzata (Lasso con α = 0,01 per le competenze, 0,001 per le conoscenze; il riassunto cita anche Ridge α = 1 per le competenze). Target: per le competenze ln(brevetti pro capite) = ln(nPats/pop); per le conoscenze, una trasformazione logaritmica spostata di un indice "EQI" (con RECPI fuso nei dati e poi tolto dalle covariate; **il significato dell'acronimo RECPI non è spiegato nei file letti**). Dati a scala di area metropolitana (colonne MSA/CBSA, filtri per stato, SFR > 1). Normalizzazione: min-max con limiti fissi, [−16, −5] per le competenze, [−11, −7] per le conoscenze, ritagliata a [0,1]. Terzo sotto-indicatore: R&D per addetto, RnD_pc = investimento/occupati, media pesata sugli occupati, poi log10(x+1) e normalizzazione con limiti [4, 5]. `marginal_effect_innovation_indicator.py` stima un **effetto marginale medio** perturbando la quota di un settore di dx (mediana dei salti tra quote non nulle) e riportando la variazione dell'indicatore per un aumento di 0,1 [V*].

**Economic** (`economic_indicator.py`) [V*]: salario medio (media pesata sulle occupazioni dei salari medi nazionali OES 2019) normalizzato come min(1, salario/80.000); produttività = Σ addetti per settore × output per addetto (tolti settori 11 e 92), normalizzata su un massimo di 5·10⁹; densità di addetti = addetti/4 km² (area **cablata**), normalizzata su 7.500 addetti/km².

**Mobility** (`mobility_indicator.py`) [V*]: due random forest (n_estimators = 50) addestrate su output di simulazione (`mobility_sim_output.json`) con target `avg_co2` e `delta_f_physical_activity_pp`; feature: piani per tipo di cella e un parametro di mobilità futura. Normalizzazione a limiti fissi (CO₂: 5-12; attività fisica: 0-0,004). "Mobility CO2 Performance" = 1 − norm; "Mobility Health Impacts" = norm, non invertito, con unità "mortality/year": direzione dell'etichetta ambigua.

**Buildings Energy Performance** (`buildings_indicator.py`) [V*]: random forest addestrata su un'indagine 2012 sugli edifici commerciali (variabile MFBTU); energia per occupante = Σ predetto / Σ addetti; normalizzazione con limiti fissi 50.000-100.000 (migliaia di Btu/persona/anno), invertita.

**Social Wellbeing e Environmental Impact:** compaiono solo come nomi in un dizionario di output d'esempio nel README; **non ho trovato il codice che li calcola** nei file letti [V*]. Le formule non sono pubblicate nelle fonti raggiunte. Il README descrive anche un `CompositeIndicator` che media altri indicatori (esempio con tre) [V*]: quindi il composito, quando c'è, è una media semplice.

### (3) Dati
BLS OES 2018/2019 (dati federali USA), shapefile Census 2019, Zip Code Business Patterns, dati brevettuali e O*NET, indagine sugli edifici commerciali 2012, OpenStreetMap (`osm_amenities.json`). I nomi di file `corktown_*` suggeriscono un caso di Detroit [I]. Licenze dei dati non dichiarate nel repository (nota 03).

### (4) Cosa ha funzionato
- Architettura modulare e leggibile: un indicatore = una classe con `setup` e `return_indicator`; facile da ricalcolare e da riscrivere.
- Il pattern **surrogato statistico** (random forest o CNN su output di simulazione) permette risposte in millisecondi; nel paper CityMatrix (Zhang et al., AAMAS 2018, [V]) una CNN a tre strati su input 19×19×2 raggiunge R² = 0,86 contro 0,571 della regressione lineare, addestrata su 10.000 simulazioni (7.000 train / 3.000 test; 18 ore su otto computer; 1 minuto per simulazione contro meno di 10 ms per la predizione).
- Interesse metodologico dell'effetto marginale medio per settore: rende leggibile come cambia un indicatore al variare della composizione industriale.

### (5) Cosa non ha funzionato / non dimostrato
- **Validazione assente nel codice:** in `train_InnoIndicator.py` il modello finale è addestrato con `test_model=False` e non c'è set di prova separato; la validazione leave-one-out esiste ma è opzionale [V*]. Nessun R² dell'indicatore di innovazione è riportato nei file letti.
- Il paper CityMatrix dichiara una valutazione utente su soli cinque test pilota (20 persone); l'85% ha giudicato utili i suggerimenti di ottimizzazione [V]. Non è una validazione dell'indicatore, e il risultato "l'ottimizzazione ha stabilizzato e migliorato il punteggio collettivo" è tratto dai log, senza gruppo di controllo.
- Incoerenze di codice segnalate dai riassunti: area di 4 km² cablata; funzioni `main()` che richiamano metodi non definiti; unità ambigue.

### (6) Limiti e bias
- **Non misura costo dell'abitare né distribuzione per reddito.** "Diversity Housing" è l'uniformità delle superfici per tipo di zona R1-R6, non per prezzo, canone o fascia di reddito dei residenti. L'indicatore economico riguarda i **salari dei posti di lavoro presenti**, non la sostenibilità del costo abitativo di chi vi abita; e il cap a 80.000 $ rende premiante il salario alto (un distretto di lavoratori ben pagati è "migliore"), con effetto implicito di gentrificazione [I].
- **Salto di scala:** i modelli di innovazione sono addestrati su aree metropolitane e applicati a pochi isolati (ecological fallacy): un Lasso con interazioni quadratiche calibrato su MSA non prova che cambiare un lotto cambi i brevetti.
- La relazione competenze → brevetti è associativa, non causale; il "potenziale di innovazione" è una predizione di brevetti pro capite, che privilegia settori brevettuali (biotech, IT) rispetto ad altre forme di valore.
- Limiti fissi = un giudizio di valore nascosto; l'evenness di Pielou assume che l'equidistribuzione sia l'ottimo (critica nella sezione 4 sotto).
- Accessibilità a soglia: nessun decadimento, nessuna competizione per la capacità.

### (7) Lezioni per il dottorato
- Copiare lo schema "stato → funzione → vettore → radar", non i modelli di innovazione/economia, che non hanno senso per lotti di social housing.
- Se si usa un indice di mescolanza, scegliere **a priori** categorie e riferimento (non l'equipartizione) e mostrare sempre il vettore delle quote accanto all'indice.
- Registrare in chiaro ogni soglia di normalizzazione (come variabile da discutere con i partecipanti) e testarne la sensibilità: nel codice letto le soglie sono costanti nascoste.
- La velocità in tempo reale può essere ottenuta con calcoli diretti (conteggi su rete) senza surrogati ML, che aggiungono errore non necessario per un tavolo con pochi lotti [I].

---

## 3. Accessibilità: `CS_Accessibility`, pandana, urbanaccess

### (1) Problema
Calcolare, per una configurazione modificabile (tabella cityIO), quante opportunità (lavoro, ristoranti, istruzione, parchi) sono raggiungibili a piedi e con trasporto pubblico.

### (2) Modello e matematica [V*]
README: modulo che calcola metriche di accessibilità a piedi e con trasporto pubblico con i moduli `urbanaccess` e `pandana` della UDST. Il file `python/access_service_nx.py` però usa **networkx**, non pandana, e non fa riferimento diretto a GTFS: la rete di trasporto arriva da CSV di nodi e archi già prodotti con UrbanAccess [V*].
- Rete diretta con pesi di arco in minuti; le celle interattive si connettono con link virtuali entro 100 m dalla rete, velocità 2 km/h (≈ 33 m/min), collegamento di punti di campionamento entro 30 m.
- Isocrona: `nx.ego_graph` con raggio RADIUS = 20 (unità minuti).
- Aggregazione: A_i^x = Σ_{n ∈ ego(i,20)} O_n^x. Nessuna funzione di decadimento. Le opportunità vengono da OpenStreetMap (query Overpass) e da POI zonali (lavoratori e residenti da `model_area.geojson`); le celle di uso del suolo producono POI tramite una tabella (es. abitazione = 1000), con arrotondamento **probabilistico** dei valori frazionari.
- Normalizzazione: divisione per un valore massimo (massimo dei punti campione; per i valori interattivi, 1,1 volte il massimo della prima passata).
- Ottimizzazione: per aggiornare in tempo reale il grafo viene invertito una volta e si ricalcolano solo i punti campione toccati dalla cella modificata.

Forma generale (notazione mia): A_i = Σ_j O_j · 1[t_ij ≤ T]. Una variante con decadimento, A_i = Σ_j O_j f(t_ij), e le misure con competizione per l'offerta, tipo E2SFCA (R_j = S_j / Σ_k P_k f(t_kj), A_i = Σ_j R_j f(t_ij)), sono state non lette in questa sessione e le cito come **riferimento non MIT da leggere**, non come fonte verificata [I].

### (3) Dati
OSM (Overpass), reti pedonali/transito derivate da UrbanAccess, tabelle `grasbrook` (Amburgo) come esempio.

### (4) Cosa ha funzionato
Calcolo incrementale efficace in tempo reale; la pipeline separa isocrone, opportunità e normalizzazione; è riusabile con OSM per qualsiasi città.

### (5) Non dimostrato
Nessuna validazione dell'accessibilità rispetto a comportamento osservato o a uno standard; non esiste (nei file letti) un confronto con le misure a decadimento o con la soglia di 10, 15, 20 minuti (si vede già l'incoerenza tra i moduli: 15 minuti in `proximity_indicator.py`, 20 in `access_service_nx.py`). Nessun risultato scientifico pubblicato che io abbia trovato per questo modulo.

### (6) Limiti e bias
Accesso **teorico**, non effettivo: non considera orari, capienza, prezzo, qualità, ammissibilità (ERP/ISEE). Un'ottima accessibilità a una scuola non dice se i residenti con reddito basso possano permettersi l'alloggio vicino. Il rischio MAUP (scelta delle celle campione) e l'effetto bordo non sono discussi.

### (7) Lezioni
Per i lotti è tecnicamente semplice replicare l'accessibilità a piedi con OSM e GTFS; ciò che va deciso insieme ai partecipanti è la **soglia temporale** e quali servizi contano. Adottare almeno due soglie e riportare la variazione (analisi di sensibilità). Se la competizione per la capacità importa (nidi, ambulatori), usare un metodo con rapporto offerta/popolazione.

---

## 4. Entropia, Simpson, mixed-use e densità: lettura critica comparata

**Differenza tra gli indici usati.** Nel gruppo coesistono: Pielou (J = H/ln S) in CS_Urban_Indicators [V*]; Shannon-Weaver per la diversità dei profili di reddito in Yurrita et al. 2021, "seguendo la metodologia di diversità della piattaforma CityScope" [V]; Simpson (1 − Σp²) in Orii et al. 2020 [V*]. Sono tutti indici di **evenness/variazione**: scelte diverse danno graduatorie diverse (Simpson dà più peso alle categorie comuni, Shannon alle rare).

**Critica non MIT, letta (Chen e Song, arXiv:2105.10383, preprint) [V].** La forma CSE = −Σ A_ij ln A_ij / ln N_j è l'indice di uso misto più comune. Le critiche: (a) problema dell'unità areale modificabile e effetto bordo; (b) l'ottimo è l'**equipartizione** (33/33/33), senza giustificazione teorica: nelle città il residenziale domina e il commercio è sotto il 5% del suolo, e uno studio citato (Im e Choi 2018) trova una relazione quadratica incoerente con il traffico pedonale; (c) l'indice non distingue i tipi di uso (un mix industria-parco vale quanto residenza-commercio) e ignora l'adiacenza; (d) è simmetrico rispetto alla permutazione delle quote. Gli autori propongono una pesatura geografica e un riferimento regionale (quoziente di localizzazione) e un approccio per cluster; **non è un lavoro MIT** e il confronto con indicatori CityScope è mio [I].

**Netto, Peres, Cacholas 2024 (arXiv:2403.15199, capitolo) [V parziale]:** conferma che gli indici entropici di uso del suolo derivano da Cervero e dalla standardizzazione di Frank e Pivo, e che il risultato dipende dai confini scelti; menziona un'entropia relativa a una "geografia di riferimento". Non MIT.

**Densità.** Nei file letti la densità non è un indice formalizzato: nel codice economico è addetti/km² con cap 7.500; nel paper CityMatrix (AAMAS 2018) gli output sono "density, diversity, energy, traffic, solar" senza formule nell'estratto [V]. Nel paper Volpe (ICCS 2018) i riferimenti bibliografici citano Hawley sulla densità e Sevtsuk et al. sull'accessibilità pedonale, ma le formule sono dietro paywall e **non le ho lette** [V* solo sull'abstract e sui riferimenti].

**Città dei 15 minuti.** La pagina di progetto MIT "Understanding the 15 Minute City" non contiene descrizione né pubblicazioni (nota 04); il repository CS_NTT_Rome ha solo metadati. Non ho trovato un articolo scientifico MIT con metodo esplicito. Confronto non MIT (note 04, riassunti [V*]): Bruno et al. 2024 (arXiv:2408.03794) modellano la prossimità con tempo medio ai 20 POI più vicini per categoria e soglia di 15 minuti, e mostrano Milano già ben ottimizzata, senza reddito né costo; Zádor et al. 2026 (arXiv:2604.00699) integrano il trasporto pubblico e misurano la mescolanza socio-economica con Gini.

**Implicazione:** per i lotti conviene non ridurre il "misto" a un numero: riportare le quote per categoria e un confronto con la composizione del NIL/quartiere di riferimento [I].

---

## 5. Reversed Urbanism (Noyman et al. 2019) e CityScope Andorra

**Fonte:** Environment and Planning B 46(8), 1480-1498 (DOI 10.1177/2399808319840668). Letti due abstract (IDEAS/RePEc e MIT Media Lab) [V*]. Paper integrale non letto. La tesi Noyman 2022 (abstract: CityScope come piattaforma di modellazione, con casi su alloggi per rifugiati in Germania, sicurezza a Guadalajara, trasporto pubblico a Boston) non letta [V* abstract].

### (1) Problema
Gli spazi pubblici di successo si studiano con osservazione occasionale e costosa. RevUrb propone di **inferire la performance di luoghi dall'uso osservato**, per un intero paese, con dati di telefonia.

### (2) Modello e matematica (dall'abstract)
- Dati telecom anonimizzati e geolocalizzati di Andorra.
- *Stay-point*: evento in cui un dispositivo resta entro un raggio di spostamento fissato per un tempo fissato.
- Aggregazione dei stay-point in **cluster di attività**, caratterizzati da dimensione, persistenza e diversità.
- Regressione lineare multivariata che collega le caratteristiche dei cluster a morfologia e uso del suolo a risoluzione 25-50 m.
- Schema (mio, non pubblicato nell'abstract) [I]: y_c = β₀ + Σ_k β_k x_{c,k} + ε_c, con y_c ∈ {dimensione, persistenza, diversità} del cluster c e x_{c,k} variabili di forma e uso (servizi, intrattenimento, acqua, betweenness, istruzione, parchi).
- **Non pubblicato nelle fonti raggiunte:** raggio e durata del stay-point, algoritmo di clustering, definizione di "diversità" del cluster, controlli, R², trattamento dell'autocorrelazione spaziale.

### (3) Dati
Telecom anonimizzati di Andorra, morfologia e uso del suolo.

### (4) Cosa ha funzionato
Risultato: servizi e intrattenimento, corsi d'acqua e betweenness della rete stradale sono associati a cluster grandi, diversi e duraturi [V*]. Il metodo offre una misura **comportamentale** a scala nazionale, che per ordine di grandezza supera i conteggi manuali.

### (5) Non dimostrato
Associazione, non causalità; effetto **negativo** di amenità educative e parchi, interpretato dagli autori ma non spiegato nell'abstract: può essere un artefatto della definizione di cluster (i parchi disperdono la presenza; le scuole hanno orari concentrati) [H]. Nessuna validazione esterna nell'abstract.

### (6) Limiti
Solo utenti con telefono di un operatore, un solo paese di piccole dimensioni con turismo e frontalieri; la "performance" è definita come aggregazione, non come benessere o equità; nessun dato su chi frequenta (reddito, status). Per l'abitare: nulla.

### (7) Lezioni
Idea: usare tracce d'uso per validare in modo indiretto la scelta dei servizi. A Milano i dati telecom non sono pubblici [I]; alternative con fonti aperte (OSM POI, Foursquare non verificato). Il tema di fondo, "un indice di performance dell'uso costruito su dati osservati", mostra il rischio di normativizzare la vitalità come merito.

**CityScope Andorra** (AAMAS 2018, pp. 1939-1940; Mobility and COVID-19 in Andorra, IEEE JBHI 26(1), 2021): solo titoli (nota 04); contenuti non letti. Non ho nulla da dire sulla matematica.

---

## 6. Abitare: Housing Choice / Dynamic Urban Planning (Yurrita et al. 2021)

**Fonte:** Yurrita, Grignard, Alonso, Zhang, Jara-Figueroa, Elkatsha, Larson, "Dynamic Urban Planning: an Agent-Based Model Coupling Mobility Mode and Housing Choice. Use case Kendall Square", arXiv:2106.14572 [V, 12 pagine lette per intero]. Codice: `CS_Dynamic_Urban_Planning` (GAML + Python) [V*]. Il modello "Housing Choice" del repository GAMA ha una pagina wiki vuota (solo titolo) [V*].

### (1) Problema
Prevedere come cittadini di profili di reddito diversi scelgono casa e modalità di spostamento, come primo passo di un "sistema dinamico di incentivi" per promuovere equità, diversità, walkability ed efficienza; motivazione: la carenza di alloggi accessibili vicino al lavoro, con l'idea di alloggi accessibili entro 20 minuti a piedi dal posto di lavoro [V]. Caso: Kendall Square, Cambridge MA.

### (2) Modello e matematica [V]
Agenti "persone" lavorano in un edificio non residenziale dell'area; ogni persona ha un profilo di reddito (otto profili). Ambiente: block group del censimento, edifici dell'area fine, rete stradale.

**Punteggio (combinazione lineare).** Per la modalità m (iterazione 0): S_mob(m) = Σ_k w_k^{(r)} x_{k}(m), con k ∈ {prezzo, tempo, difficoltà, schema sociale}, r il profilo di reddito. Pesi in [−1, 0] per prezzo, tempo, difficoltà; [0, 1] per lo "schema". Per l'alloggio: S_ab(h) = w_prezzo · prezzo_h + w_div · D_h + w_zona · 1[zona preferita] + (componente di spostamento dal punteggio della modalità migliore), con "diversity acceptance" in [−1, 1], peso della zona in [0,1]. L'agente **si trasferisce se S(alternativa) > S(corrente)**. Alternative: una opzione scelta a caso a ogni iterazione; si procede finché il numero di chi si sposta tende a zero. Ispirazione dichiarata: modello di segregazione di Schelling.

**Diversità.** Formula di Shannon-Weaver sui profili di reddito presenti nell'edificio (area fine) o nel block group (periferia): H = −Σ p_r ln p_r [V: formula nominata, non scritta nel paper].

**Valori d'esempio.** Le tabelle 1-3 del paper contengono valori **sintetici**: es. per i tre profili medi: peso del prezzo −0,8/−0,6/−0,5 e accettazione della diversità 0/−0,3/−0,5 al crescere del reddito (cioè nell'esempio, chi guadagna di più è meno tollerante alla mescolanza, per costruzione); pesi del tempo −0,8/−0,85/−0,9 [V]. Non sono stime.

**Calibrazione.** Otto fattori × otto profili = 64 variabili. Due errori: errore sull'abitare (RMSE tra percentuali reali e simulate di ciascun profilo di reddito in ogni block group dove vivono i lavoratori di Kendall) e errore sulla mobilità (RMSE tra quote modali simulate e reali dei dati PTDM di Cambridge). Ottimizzazione con **hill climbing** su esperimenti batch. Risultato: errore medio 3,87% (abitare) e 2,30% (mobilità) [V]. Il paper stesso ammette che l'hill climbing dipende dal punto di partenza.

**Estensioni nel repository** [V*]: calibrazione per percentuale; modello principale con esperimento `batch_save` su area aggiuntiva e incentivi; regressore **k-NN** su 80/20 addestramento/prova, che predice sei output (quote di residenti e lavoratori per profilo, uso delle modalità, tempo e distanza medi di spostamento, occupazione del sito di costruzione); R² e RMSE vengono scritti in un file, **non riportati** nel README.

### (3) Dati
Shapefile census block group (US Census), annunci di affitto ottenuti con web scraping (PadMapper) per prezzi e vacanze, MBTA, PTDM Cambridge 2014, Census (profili di reddito); il profilo di reddito dei lavoratori di Kendall è approssimato con il reddito medio annuo del block group di residenza [V].

### (4) Cosa ha funzionato
- Una struttura chiara e trasferibile: criteri esplicitati per profilo, errore di calibrazione definito, iterazione fino a convergenza.
- Tra i pochissimi lavori del gruppo in cui il **prezzo dell'alloggio entra nel modello** e in cui l'esito è distribuito per profilo di reddito.
- Calibrazione con errori medi bassi su quote aggregate.

### (5) Cosa non ha funzionato / non dimostrato
- **Nessun risultato su incentivi o politiche** nel paper: contiene solo la descrizione e la calibrazione [V]. L'effetto degli incentivi sull'accessibilità abitativa è annunciato come sviluppo successivo. Ho trovato solo la pagina di progetto "Algorithmic Zoning" che parla in termini generali [V*].
- **Convalida = adattamento in campione:** gli stessi dati servono a calibrare e a "validare"; il paper non descrive un insieme di verifica separato [V]. Con 64 parametri e target aggregati, l'identificabilità è dubbia [I].
- Il modello non include vincolo di bilancio, rapporto canone/reddito, disponibilità effettiva (non è detto che una vacanza venga occupata e tolta), formazione dei prezzi, proprietari, ricerca con informazione parziale oltre la scelta casuale. Alcuni di questi punti il paper non specifica; li segnalo come non pubblicati.
- Pesi di esempio sintetici: nessuna fonte empirica che giustifichi la tolleranza decrescente alla diversità.

### (6) Limiti e bias
- Il costo entra come **peso lineare sul prezzo**: la sostituibilità prezzo-diversità-zona è assunta (compensativa); un nucleo con reddito basso e prezzo fuori portata non è "escluso" ma ottiene un punteggio più basso.
- Reddito = otto classi di reddito medio di block group → inferenza ecologica; si osservano solo i lavoratori di un'area, non tutta la popolazione.
- Il mercato è quello di Cambridge (annunci online): non rappresenta affitti regolati o alloggi pubblici.
- **Nessun termine esplicito di affordability né di quota di alloggi sociali** nel modello descritto.

### (7) Lezioni per il dottorato
- Come *guida concettuale*: esplicitare i criteri, il peso per profilo e la regola di scelta. Per Milano i profili dovrebbero essere definiti da ISEE/reddito, tipologia familiare e titolo (mercato, canone moderato, ERP).
- Invertire la logica: invece di calibrare i pesi su dati aggregati, **elicitare** i pesi dalle persone in sessione, usando il modello solo per mostrare conseguenze (nell'impianto [I], i pesi sono l'esito della partecipazione).
- Inserire il vincolo di bilancio (rapporto canone/reddito) come criterio di ammissibilità e non come peso.

---

## 7. CityHome, Compact Living, abitazioni robotiche e trasformabili

### (1) Problema
Rendere abitabili micro-appartamenti (circa 18,6 m², 200 sf) tramite pareti trasformabili con mobili motorizzati (CityHome), poi commercializzati come arredo robotico (Ori).

### (2) Modello e matematica
**Non c'è un modello matematico pubblicato** nelle fonti raggiunte: né ottimizzazione di layout, né funzione di benessere, né misura dello spazio guadagnato. La pagina del Media Lab (OLD_cityhome2) dice che la casa può funzionare come un appartamento da due a tre volte la sua dimensione, senza dati, senza costo, senza valutazione [V*]. L'articolo di BD+C (2014) descrive pareti con sensori e motori, comandi gestuali e vocali, scenari "potenziali" [V*, nota 04].

### (3) Dati
Nessun dato quantitativo pubblicato. Fonte di mercato (articolo su Ori, sito robotics.mit.edu, di tono aziendale) [V*]: un prototipo in un monolocale di 200 sf al quinto piano del Media Lab; ricerche di mercato iniziali; installazioni in alcuni appartamenti di Boston; piloti in 10 città; prima linea commerciale intorno a 10.000 $; produzione iniziale pianificata di 500 unità; vendita a **developer** (nominati Skanska, Samuels and Associates, Hines).

### (4) Cosa ha funzionato
Come prodotto: è arrivato al mercato come impresa derivata (Ori), con piloti presso developer [V*, fonte aziendale]. Come ricerca: nessuna evidenza pubblicata di vivibilità, durata o soddisfazione.

### (5) Non dimostrato
Il moltiplicatore "2-3 volte" non è misurato; non c'è un'analisi di costo ciclo di vita, di manutenzione, di sicurezza o di accettazione. Non ho trovato né lavori scientifici su "Compact Living" né su abitazioni modulari robotiche oltre a queste pagine; non provata l'assenza.

### (6) Limiti e bias
- **Costo:** 10.000 $ per unità (fonte aziendale) è un costo aggiuntivo che aumenta il costo di realizzazione, mentre l'affordability non è discussa [V*].
- **Distribuzione:** il target è il mercato di locazione con developer; non c'è un'analisi di chi possa permettersi o gradire microunità. Compattezza ≠ accessibilità economica [I]; il rischio è usare la riduzione di superficie per giustificare affitti elevati per metro quadrato [H].
- Non c'è un indicatore di *adeguatezza abitativa* (affollamento, luce, privacy), mentre le soglie normative italiane (superficie minima per abitante) sono vincolanti [I, da verificare].

### (7) Lezioni
Il kit di componenti trasformabili è un'idea di progetto da citare come ipotesi di flessibilità interna dei lotti, non come evidenza. Per social housing senza developer, il tema è chi finanzia e manutiene la tecnologia: l'unico canale commerciale documentato passa dai developer, cioè l'attore escluso da [I]. Servono costi, test d'uso e valutazioni indipendenti prima di qualunque uso nel dottorato.

---

## 8. Come il gruppo tratta costo dell'abitare, affordability e mix sociale: sintesi

| Lavoro | Costo dell'abitare | Reddito/distribuzione | Mix sociale |
|---|---|---|---|
| Orii et al. 2020 | assente [V*] | tre fasce solo come dimensione di Simpson; disaggregazione parchi per reddito [V*] | Simpson 1 − Σp² su sei dimensioni [V*] |
| CS_Urban_Indicators | assente; "salario medio" dei posti di lavoro (cap 80.000 $) [V*] | assente | Pielou su settori, tipi di zona R1-R6, scuole, "third places" [V*] |
| CS_Accessibility / proximity | assente | assente | n/a |
| Reversed Urbanism | assente | assente | "diversità" del cluster di attività, non sociale [V*] |
| Yurrita et al. 2021 | prezzo come peso lineare; affitti da annunci [V] | otto profili di reddito, esito per profilo [V] | Shannon-Weaver sui profili di reddito, "accettazione" per profilo [V] |
| CityHome / Ori | prezzo unità ≈ 10.000 $ (fonte aziendale); affitto non trattato [V*] | assente | assente |

**Conclusione:** l'affordability non è mai una variabile di esito. Il solo lavoro con redditi e prezzi (Yurrita) ha un obiettivo dichiarato di accessibilità ma pubblica solo la calibrazione. Il mix sociale è misurato con indici di uniformità, mai con una soglia di accesso economico.

---

## 9. Termini di paragone non MIT (marcati)

- **Non MIT** Chen e Song (arXiv:2105.10383, preprint) [V]: critica all'entropia di Shannon come indice di uso misto; indica alternative con pesatura geografica e riferimento regionale.
- **Non MIT** Netto, Peres, Cacholas (arXiv:2403.15199) [V parziale]: storia e usi urbani dell'entropia; ricorda che la standardizzazione per ln(numero di classi) enfatizza l'evenness e che i confini di analisi pesano.
- **Non MIT** Bruno et al. 2024 (arXiv:2408.03794) e Zádor et al. 2026 (arXiv:2604.00699) [V*, da nota 04]: città dei 15 minuti, Milano in un caso; nessuna misura di costo abitativo nel primo; mescolanza socio-economica con Gini nel secondo.
- **Non MIT, non letti:** letteratura E2SFCA e indici di costo abitazione+trasporto: da cercare. Non li uso come evidenza.
- Per la partecipazione e i suoi bias si veda la nota 05 (Flacke et al. 2020; Champlin et al. 2019; Sloane et al. 2022), non ripetuta qui.

---

## 10. Sintesi: cosa ha funzionato, cosa no

**Ha funzionato (con evidenza):**
- Il surrogato CNN di un ABM di traffico: R² = 0,86 su test di 3.000 configurazioni, tempo di risposta da 1 minuto a meno di 10 ms [V].
- Calibrazione di un ABM di scelta casa-mobilità su quote aggregate (errori medi 3,87% e 2,30%) [V]; sul piano dei risultati è un adattamento a dati aggregati, non una previsione.
- Calcolo incrementale delle isocrone [V*].

**Non dimostrato o non funzionante:**
- Validazione degli indici (benessere, innovazione, economia): assente o non pubblicata.
- Effetto di incentivi sull'accessibilità abitativa: non pubblicato.
- CityHome: nessuna valutazione.
- Social Wellbeing ed Environmental Impact: formule non trovate.

**Cosa non misurano:** il costo dell'abitare rispetto al reddito; la distribuzione per fasce di reddito oltre una mescolanza; chi non può entrare nel quartiere.

## 11. Lezioni operative per il dottorato (solo persone, nessun developer)

1. **Vettore, non composito.** Per ogni lotto una scheda con le quote e le distanze (a piedi) dei servizi scelti dai partecipanti, più un indicatore di costo (canone/reddito per fascia). Ogni numero con la sua formula esposta.
2. **I pesi sono l'esito.** Elicitare i pesi con le persone; l'indice è uno strumento di discussione, non di verdetto (contro la deriva "pesi uguali" di Orii e i limiti fissi di CS_Urban_Indicators).
3. **Soglie e normalizzazioni dichiarate e testate.** Sensibilità a 10/15/20 minuti; confronto min-max osservato contro soglie normative.
4. **Mescolanza con riferimento.** Quote per categoria e rapporto con il quartiere, non equipartizione.
5. **Affordability come vincolo.** Rapporto canone/reddito per fascia come criterio di ammissibilità, non peso compensativo.
6. **Niente surrogati ML senza necessità.** Pochi lotti → calcolo diretto; riservare ML a casi con molte simulazioni.
7. **Validazione dichiarata.** Test-retest con le persone, confronto con dati esterni (ISTAT), insieme di verifica separato.
8. **Open problems [H]:** definire cosa conta come "servizio" per un nucleo ERP o a canone moderato; quanta diversità di reddito è desiderata dalle persone coinvolte (non da un parametro); come trattare le microunità trasformabili senza assumere che compattezza equivalga ad accessibilità.

## 12. Lacune residue
Tesi Noyman 2022 e Zhang 2017; paper Volpe ICCS 2018 (formule di densità, diversità, prossimità); PDF di Orii (tabelle 3-4); codice reale dei file `.py` (solo riassunti); modello GAMA Housing Choice; una pagina "Compact Living"; articolo MIT sul framework 15-minute city; valutazioni indipendenti di CityScope.
