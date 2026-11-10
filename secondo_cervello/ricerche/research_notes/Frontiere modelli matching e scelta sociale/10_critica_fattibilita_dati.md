# Critica di fattibilità della scala urbana: dati, calcolo, MVP F1, prima parte della tesi, rischi (nota 10)

Data: 2026-11-10. Ruolo: revisore pragmatico (urban data scientist + architetto-ingegnere) di una commissione di dottorato. Oggetto: fattibilità della **scala urbana** (F1, gen–apr 2027) entro la laurea nei primi mesi del 2028, con una persona che lavora sere e weekend con l'IA.

**Marche** (CLAUDE.md): **[V]** verificato nei file del repo (file indicato); **[S]** visto solo come sintesi di una ricerca web o in fonte secondaria in questa sessione (8 ricerche, nessuna pagina ufficiale aperta per intero); **[I]** inferenza mia; **[H]** ipotesi da testare; **[L]** da verificare (portale, licenza, esistenza della variabile). Nessuna voce [S] o [L] va citata in tesi senza averla riscontrata sulla fonte primaria.

Letti: `tesi/DOMANDA_DI_RICERCA.md`, `tesi/DECISIONI.md`, `tesi/CALENDARIO.md`, `secondo_cervello/ricerche/06_riesame_spatial_milano_lab.md` (§1–3.4), `prove/in_evidenza/2026-10-25_spatial_milano_lab/lab_completo/results/paper.md` (§2–3.5), `secondo_cervello/modelli/MAPPA_MODELLI_ANALISI.md`, note 02 (intera), 05 §1, 06 §2, 07 §1–2 di questa cartella; 03 solo indice.

---

## 0. Verdetto in breve

- **Fattibile, a una condizione: restringere.** Il collo di bottiglia non è il calcolo (tutti i modelli candidati girano su un portatile alla scala di Milano, §2) ma **tre dati che mancano** — proprietà dei suoli, reddito sotto il CAP, costi reali di costruzione — già dichiarati mancanti dal paper del Lab [V, paper §2: "Mancano tre fonti decisive: la proprietà dei suoli, i costi di costruzione reali e le preferenze reali dei cittadini"]. Nessuno dei tre si risolve in F1 con dati aperti [I].
- **Conseguenza di metodo [I].** La scala urbana può dimostrare **proprietà dei meccanismi** (matching, gruppi, economia) su un caso milanese realistico, non **stime della domanda per NIL**. Il riesame ha già mostrato che con reddito a 38 CAP la "domanda" per NIL è una mappa degli affitti [V, riesame §3.2: Spearman 0,939 col canone OMI; 99,3% della varianza tra NIL è affitto]. Ripetere quell'errore è il rischio n. 1 di credibilità.
- **Calendario [I].** F1 = 17 settimane. A ~18–20 h/settimana (2 h × 4 sere + 2 giornate di weekend, meno imprevisti) sono ~300–340 h. L'MVP del §3 ne chiede ~310: **non c'è margine per più di un modello "di frontiera"** in F1.

---

## 1. Matrice dei dati

Colonne: variabile richiesta dai modelli → miglior fonte per Milano → risoluzione → licenza → lacune. "Stato" indica cosa è verificato.

### 1.1 Persone e famiglie

| Variabile | Fonte migliore | Risoluzione | Licenza | Stato | Lacune |
|---|---|---|---|---|---|
| Popolazione, età, cittadinanza, famiglie per numero di componenti | ISTAT, Censimento permanente 2021, dati per **sezione di censimento** su Basi territoriali 2021 | sezione (≈ isolato) e aree sub-comunali | [L] (dati ISTAT di norma CC-BY; da riscontrare) | Esistenza dei dati per sezione: [S] (nota informativa ISTAT 2024 e pagina "Basi territoriali e variabili censuarie"); variabili esatte: **[L]** | Confrontabilità col 2011 non garantita [S]; esiste anche un rilascio "edizione 2023" [S] da capire se sostituisce il 2021 [L]. **Da verificare se la sezione 2021 contiene titolo di godimento (affitto/proprietà) e composizione per tipo di nucleo** [L]: è decisivo per sostituire la quota affittuari piatta 0,30 del Lab [V, paper §2 Tab.1] |
| Lo stesso, già usato nel Lab | Censimento 2021 su **griglia esagonale** | celle | — | [V, paper §2] | Il Lab ha usato le celle, non le sezioni: va ricostruita la catena dalla fonte [I] |
| Residenti e famiglie per NIL da anagrafe (serie annuali) | Comune di Milano, dati.comune.milano.it | NIL | [L] | [L] | Utile per tendenze annuali e per controllo delle marginali [I] |
| **Reddito** delle famiglie | MEF – Dipartimento Finanze, open data IRPEF "comunali e sub-comunali", anno d'imposta 2024 [S] | Lab: **38 CAP** [V, paper §2] | [L] | Uso nel Lab [V]; contenuto sub-comunale = CAP: [L] | **Lacuna critica**: redditi di contribuenti, non di famiglie; per classi, non microdati; nessuna risoluzione a sezione o NIL [I]. ISEE aggregato per zona: non trovato [L]. Microdati geolocalizzati solo in ambiente ISTAT ad accesso controllato (ADELE) secondo la nota 05 §1 [L] |
| Soglia di povertà assoluta (paniere non abitativo) | ISTAT | per tipo di famiglia e area | — | valore 1.256,37 €/mese **da verificare** [V che il Lab lo segna come da verificare, paper §3.1] | Il moltiplicatore 1,5 × paniere decide quasi tutta la domanda [V, riesame §3.4: 102 famiglie contro 2.274] |
| Preferenze ed esigenze | **nessuna fonte aperta** | — | — | [V, paper §2] | Solo archetipi sintetici; dati reali solo in F2 [V, CALENDARIO] |

### 1.2 Prezzi e canoni

| Variabile | Fonte | Risoluzione | Licenza | Stato | Lacune |
|---|---|---|---|---|---|
| Canoni e prezzi di mercato | Agenzia Entrate, **OMI** (quotazioni semestrali min–max €/m² per zona e tipologia) | zona OMI, semestre | gratuita con autenticazione; obbligo di citare «Agenzia delle Entrate – OMI» [S] | Uso nel Lab (2019–2024, riportati a 88 NIL) [V, paper §2]; download e perimetri via "Forniture dati OMI"/GeoPOI [S]; specchio non ufficiale su GitHub (onData) [S] | Valori **di zona**, non transazioni; intervallo, non distribuzione [I, coerente con nota 05 §1]. Canoni dei contratti in essere: non disponibili [L] |
| Compravendite (volumi) | OMI, dettaglio comunale [S] | comune/zona | come sopra | [S] | Non servono al nucleo F1 [I] |
| Canone calmierato di riferimento | Piano straordinario Casa Accessibile del Comune: ERSC a **≤ 80 €/m²/anno**, obiettivo 10.000 alloggi [S]; indirizzi con Delibera GC n. 365 del 26/03/2026 [S]; bandi su tre aree pubbliche (ex Palasharp, San Romanello, Bovisasca) [S] | alloggio | atto pubblico | [S] (solo stampa e Assolombarda) | Da leggere gli atti originali [L]. **Utile come scenario-politica reale** per il confronto developer/cooperativa (la nota 06 §2 lo usa già come canone obiettivo) |

### 1.3 Lotti, vincoli, proprietà

| Variabile | Fonte | Risoluzione | Licenza | Stato | Lacune |
|---|---|---|---|---|---|
| Particelle catastali (geometria) | Agenzia Entrate, cartografia catastale INSPIRE: WFS e **download massivo GML** per comune, aggiornamento semestrale [S] | particella | **CC-BY 4.0** [S] | Uso nel Lab (112.568 particelle → 2.291 siti) [V, paper §3.2] | Nessuna informazione su intestatari [I] |
| Volumi edilizi | DBT 2020 (Regione Lombardia / Comune) | edificio | [L]: il Geoportale ha licenze diverse per dataset (IODL 2.0, CC-BY 4.0, CC-BY-NC-ND 4.0) [S] | Uso nel Lab [V, paper §2] | Licenza del DBT da leggere nella scheda metadati [L] |
| Uso del suolo | DUSAF 2024 (Regione/ERSAF) | poligoni | [L] | Uso nel Lab [V] | Licenza e versione da riscontrare [L]; nel Lab rischio di *leakage* post-designazione [V, riesame §3.1] |
| Strati del PGT 2030 (AT, ex AMB_DEG, srv_erp, rig) | Comune di Milano, geoportale/PGT | poligoni | [L] | Uso nel Lab [V, paper §2] | |
| NIL | dati.comune.milano.it, dataset "NIL vigenti PGT 2030" (ds964) | 88 NIL | **CC-BY 4.0** per la risorsa CSV [S]; shapefile in altro dataset (ds61), licenza [L] | [S] | Le schede NIL del PGT hanno revisioni 2019/2021/2023 [S]: fissare la versione |
| **Indici edificatori reali** (FAR) | PGT 2030, Piano delle Regole | ambito/particella | [L] | Il Lab usa **FAR 1,0 come assunzione** [V, paper §2] | Lacuna: la capacità dei lotti è inventata finché non si leggono gli indici (base, perequazione, premialità) [I] |
| Vincoli (paesaggio, bonifiche, rischio idraulico, fasce di rispetto) | SIBA Regione, anagrafe siti contaminati, PGRA, PGT vincoli | poligoni | [L] | **non usati nel Lab** [I: assenti in paper §3.2] | Lacuna seria per il cancello F1 "lotti che reggono una verifica tecnica" |
| **Proprietà** | Catasto: intestatari solo da visura (a pagamento, per particella, vincoli di privacy) [L]; patrimonio comunale e ERP (Comune, MM, ALER) [L] | particella | non aperta | **assente** [V, paper §2; §8 "designation is not ownership"] | **Lacuna critica, non colmabile con dati aperti** [I]. Sostituti: aree comunali messe a bando (Piano Casa) [S], elenchi di patrimonio pubblico [L], richiesta formale al Comune [H] |

### 1.4 Accessibilità

| Variabile | Fonte | Risoluzione | Licenza | Stato | Lacune |
|---|---|---|---|---|---|
| Rete stradale, servizi, scuole, verde | OpenStreetMap via Overpass (rete aperta il 09/11 [V, DECISIONI "Calcolo"]) | punto/arco | ODbL [I, licenza nota di OSM] | Lab: E2SFCA su servizi e verde [V, paper §3.3] | Qualità dei tag dei servizi da controllare con dati comunali [L] |
| Trasporto pubblico | GTFS ATM / Comune di Milano | fermata, orario | [L] | Lab: "accesso alla metro" [V, paper §3.3] | Senza GTFS l'accessibilità è solo distanza dalla metro [I] |
| Luoghi di lavoro / pendolarismo | ISTAT matrici del pendolarismo; Regione (indagine O/D) | comune / zona | [L] | Lab: "lavoro entro 5 km (rango)" [V] | Matrici a scala sub-comunale: [L] |

### 1.5 Costi, oneri, finanza

| Variabile | Fonte | Risoluzione | Licenza | Stato | Lacune |
|---|---|---|---|---|---|
| Costo di costruzione | Prezzario Regione Lombardia / listino Comune di Milano (prezzi unitari, non €/m² a edificio) [L]; pubblicazioni di costi per tipologia edilizia (DEI/Collegio Ingegneri e Architetti di Milano, a pagamento) [L]; indice ISTAT del costo di costruzione [L] | €/m² o voce | varia | Lab: **2.000 €/m² come assunzione** [V, paper §2] | **Lacuna critica** [V, paper §2]. Soluzione pratica: 2–3 computi parametrici da casi reali (bandi Piano Casa, cooperative a proprietà indivisa) [H] |
| Oneri di urbanizzazione | Delibera CC Milano n. 28/2023 (aggiornamento dopo 16 anni; aumento medio riportato +37,92%) [S]; criteri successivi (DD n. 9501 del 24/10/2025 su demolizione e ricostruzione) [S] | €/m³ o €/m² per zona e funzione | atto pubblico | [S] (fonti secondarie) | Tabelle ufficiali da scaricare dall'Albo/sito del Comune [L] |
| Contributo sul costo di costruzione | DPR 380/2001 art. 16 [L, nota 06]; costo base comunale annuo (un sito secondario riporta 484,78 €/m² per il 2025) [S, bassa affidabilità] | €/m² | atto pubblico | [S] | Riduzioni per edilizia convenzionata e per criteri ambientali [S] da riscontrare |
| Valore del suolo | Lab: suolo al 20% del prezzo OMI; srv_erp a 1 €/m² [V, paper §2] | sito | — | assunzione [V] | L'etichetta ERP "potential" del Lab era un artefatto di questo 1 €/m² [V, riesame §3.3c]. Va calcolato endogenamente come valore residuo (nota 06 §2, formula 1) |
| Tassi di mutuo, LTV | Banca d'Italia, Base dati statistica [L] | serie mensili | [L] | [L] | Parametro di sensibilità, non di stima [I] |
| Margine developer, soft cost | prassi RICS / nota 04 §1 [S nella nota 06] | — | — | [S] | Nessun riscontro italiano di prassi [V, nota 06 §2 Gaps] |

### 1.6 Sintesi della matrice [I]

- **Ci sono e sono aperti**: geometrie (particelle CC-BY [S], NIL CC-BY [S]), censimento per sezione [S], OMI [S], OSM. Bastano per **dove** e **quanto costa abitare a prezzo di mercato per zona**.
- **Ci sono solo grossolani**: reddito (CAP), costi (assunzioni), oneri (tabelle da scaricare).
- **Non ci sono**: proprietà, preferenze, vincoli di dettaglio integrati, indici edificatori per lotto già pronti.
- Una richiesta formale al Comune (patrimonio pubblico disponibile, aree ERSC, eventualmente dati anagrafici aggregati per sezione) costa poche ore e può sbloccare il rischio n. 1 [H]. Va fatta **in F0**, perché i tempi di risposta di un ente non dipendono da Dennis.

---

## 2. Trattabilità dei modelli alla scala di Milano

Scala di riferimento: **2.291 siti** [V, paper §3.2], qualche migliaio di famiglie sintetiche (diciamo 2.000–20.000 per scenario) [I], gruppi di convivenza di ~10–40 famiglie, quindi **~100–1.000 gruppi** [I]. Tutte le stime di tempo sono inferenze da complessità nota, **non misurate** [I].

| Modello | Problema alla scala Milano | Calcolabile? | Strumenti Python | Nota critica |
|---|---|---|---|---|
| **RSD / serial dictatorship** (famiglie o gruppi scelgono lotti in ordine sorteggiato) | O(n · m) | sì, istantaneo [I] | codice proprio (~30 righe); `numpy` | Strategy-proof e spiegabile (nota 02 §1). **Linea di base obbligatoria** |
| **Deferred acceptance con riserve / soft bounds** (famiglie singole su lotti con capacità e quote per tipo) | proposte ≤ n·m ≈ 10⁷–10⁸ nel caso peggiore, molto meno con liste corte | sì [I] | `matching` (implementazione Gale–Shapley/HR) [L: verificare il pacchetto con dependency-vetting]; meglio implementazione propria con priorità modificate (forma soft bounds, nota 02 §2) | Le liste di preferenza vanno troncate (top-k lotti per famiglia, k ≈ 10–20): nessuna famiglia ordina 2.291 lotti [I]. Lo dice anche la condizione di Kojima–Pathak–Roth (liste corte) [S, nota 02 §3] |
| **Gruppi con domanda multi-unità → lotti** (un gruppo vuole k alloggi nello stesso lotto) | complementarità: la stabilità può non esistere; vincolo tipo zaino multidimensionale [S, nota 02 §3] | come **assegnazione** (ILP) sì; come **matching stabile garantito** (Nguyen–Vohra, Scarf) no in pratica [I] | `highspy` (HiGHS, già usato nel Lab [V, paper §3.5]), `ortools` CP-SAT, `pulp` | Con ~500 gruppi × 2.291 siti = ~10⁶ variabili binarie: va pre-filtrato (ogni gruppo considera solo i lotti abbastanza grandi e nella sua lista) [I]. Proposta: **RSD a livello di gruppo** + verifica a posteriori delle coppie bloccanti, invece di inseguire la stabilità garantita |
| **Formazione dei gruppi – IS con 2 tipi** | polinomiale [S, nota 07 §1] | sì | codice proprio (ricerca locale con regola "entri se il gruppo acconsente") | Con ≥3 tipi l'IS può non esistere [S, nota 07 §1]: **misurare** la quota di famiglie con deviazione ammissibile, non presumerla |
| **Fair clustering** (proporzioni per tipo in ogni gruppo) | k-means/k-median con vincoli di proporzione su n = 10³–10⁴ | sì, come MILP/flusso di costo minimo per l'assegnazione dato i centri; LP + arrotondamento (Bera et al., nota 07 §2) | `scikit-learn` (centri), `ortools` (min-cost flow / CP-SAT), `highspy` | Il rischio non è il calcolo ma la **metrica**: con distanza = somiglianza di esigenze si rifà Housing Prime con quote [S, nota 07 §2]. Va dichiarata la metrica di compatibilità |
| **MES / Phragmén** (criteri o progetti votati) | m progetti, n votanti: polinomiale | sì per centinaia di progetti e migliaia di votanti [I] | `pabutools` (libreria del Pabulib) [L: verificare versione] | In F1 **non serve**: senza persone reali non c'è nulla di vero da aggregare. Spostare in F2 [I] |
| **Aggregazione di bilanci / pesi** (9 criteri) | dimensione 9 | banale | codice proprio (media, mediana, *moving phantoms*) | Stesso discorso: utile in F2 |
| **SMAA-2** | 2.291 siti × 10⁴ campioni di pesi × 9 criteri | sì; il Lab l'ha già fatto con filtro di dominanza [V, paper §3.4] | `numpy` | Riusare il motore del Lab, non riscriverlo |
| **Sorting logit / BLP / BFM** | stima con 88 NIL (o ~zone OMI) × pochi tipi di famiglia | calcolabile [I] | `pyblp`, `statsmodels`, `biogeme` | **Non identificabile in modo credibile** con un solo mercato, un periodo e reddito a CAP [S, nota 05 §1: problema Bartik–Epple; strumento per il prezzo]. Il problema è econometrico, non computazionale. **Fuori da F1** |
| **Cost-rent (Kostenmiete) vs valore residuo (VRA)** | 2.291 siti × 3 regimi del suolo × 10³ Monte Carlo ≈ 7·10⁶ valutazioni di formule chiuse | sì, secondi con `numpy` vettoriale [I] | `numpy`, `numpy-financial` (VAN/IRR) [L], `SALib` (Sobol) [L] | Il limite sono i **parametri** (§1.5), non il calcolo. Esito come regione di dominanza (nota 06 §2) |
| **Popolazione sintetica** (IPF / ricampionamento) | marginali per sezione o NIL | sì | `ipfn` [L], codice proprio, `numpy` | Il reddito resta a CAP: la popolazione sintetica **non** aggiunge informazione sul reddito sotto il CAP [I] |
| **Agenti LLM** come residenti simulati | migliaia di famiglie × più round = decine/centinaia di migliaia di chiamate | tecnicamente sì, **economicamente e metodologicamente no** in F1 [I] | SDK del modello scelto | Riproducono stereotipi, non esigenze (MAPPA §2.2; nota 05 §3). Usarli solo su 30–100 personaggi per collaudare l'interfaccia di dialogo [I] |
| **RL multi-agente** per coalizioni | spazio degli stati enorme | sproporzionato [I] | — | Chi scrive la ricompensa decide (nota 07 §3). Fuori da F1 |

**Conclusione [I].** Alla scala di Milano tutto il nucleo F1 è calcolabile in minuti su un portatile o in cloud con `numpy`, `geopandas`, `osmnx`/`r5py` [L], `highspy`/`ortools`, `scikit-learn`. Gli unici oggetti computazionalmente "difficili" (stabilità con gruppi, equilibrio HZ, core) vanno **evitati per scelta di metodo**, non inseguiti: sono anche quelli meno spiegabili ai partecipanti (nota 02 §1 Inferences).

---

## 3. MVP della pipeline F1 (gen–apr 2027)

Ordine vincolante: ogni passo ha **una linea di base e una metrica fissate prima** (MAPPA §2.8; riesame). Ore = stima [I]; budget F1 ~300–340 h.

| # | Passo | Prodotto verificabile | Ore [I] | Settimane |
|---|---|---|---|---|
| 0 | **Riproducibilità**: ambiente bloccato (`pyproject` + lockfile), manifest dei dati (URL, data, licenza, hash), cartella `data/raw` fuori dal repo, un comando che rigenera tutto | `make all` o script unico che parte da zero | 15 | gen 1 |
| 1 | **Acquisizione dati v1**: NIL, sezioni 2021 + variabili, IRPEF CAP, OMI (ultimi 4 semestri), particelle GML, PGT 2030, DUSAF, OSM; verificare ogni [L] del §1 e aggiornare la matrice | matrice dati con colonne licenza/risoluzione **verificate** | 30 | gen 1–3 |
| 2 | **Lotti**: rieseguire il filtro del Lab (→ ~2.291 siti), aggiungere vincoli (paesaggio, bonifiche, idraulica) e **indici reali del PGT** al posto di FAR 1,0; classificare la proprietà in 3 classi (pubblica nota / pubblica presunta / ignota) | elenco siti con capacità e classe di proprietà; **verifica a campione di 30–50 siti** (ortofoto, street view, PGT) con tasso di errore dichiarato | 40 | gen 4 – feb 2 |
| 3 | **Famiglie sintetiche e "pancia"**: popolazione per sezione/NIL con IPF sulle marginali del censimento; reddito da Dagum per CAP (motore del Lab); "pancia" definita **a livello di città per tipo di famiglia** con il test del reddito residuo, non come mappa per NIL | 3 scenari di popolazione; tabella di sensibilità al paniere (1,0 / 1,25 / 1,5) | 35 | feb 1–3 |
| 4 | **Motore economico per lotto**: VRA developer vs cost-rent cooperativa/ERSC, 3 regimi del suolo (mercato / diritto di superficie / cessione); oneri dalle tabelle ufficiali; **taratura su 1–2 casi reali milanesi** (un bando Piano Casa, una cooperativa a proprietà indivisa) | per ogni lotto: canone di pareggio, RTI per la "pancia", Δ_L (nota 06 §2 formula 6); tornado su 8 parametri | 45 | feb 3 – mar 2 |
| 5 | **Gruppi**: linea di base "per somiglianza" (k-means, alla Housing Prime) vs **fair clustering con UN vincolo binario** (per esempio almeno un nucleo over-65 e almeno uno con figli; nota 07 §1 [H]) + controllo IS a posteriori | curve: prezzo della diversità, quota di deviazioni IS, indice di diversità (nota 07 §2 [H]) | 40 | mar 1–3 |
| 6 | **Abbinamento gruppi→lotti**: (a) casuale, (b) RSD di gruppo con capacità, (c) DA con soft bounds sulle famiglie singole, (d) MILP dall'alto del Lab | stesse metriche per tutti: rango medio del lotto ottenuto, invidia giustificata, coppie bloccanti, RTI, quota di famiglie servite | 40 | mar 3 – apr 1 |
| 7 | **Esperimenti pre-registrati**: ipotesi con soglie (da F0), ≥20 semi, intervalli di confidenza, analisi di sensibilità ai 5 parametri decisivi | tabella risultati con IC; registro delle deviazioni | 25 | apr 1–2 |
| 8 | **Scrittura**: bozza del capitolo "Dati e lotti" (già da feb) + bozza paper 1 | testo | 40 | in parallelo, chiusura apr 3–4 |
| | **Totale** | | **~310** | |

**Cosa togliere se si è in ritardo (in quest'ordine) [I]:**
1. agenti LLM (tenere agenti a regole);
2. DA con soft bounds (resta RSD di gruppo + MILP + casuale: il confronto "scelta vs dall'alto" regge comunque);
3. Sobol → solo tornado one-at-a-time;
4. vincoli ambientali di dettaglio → solo esclusione dei vincoli più gravi (bonifiche, aree di rispetto) e dichiarazione del limite;
5. taratura economica su un solo caso invece di due;
6. verifica a campione dei siti da 50 a 30.

**Mai togliere**: passo 0 (riproducibilità), le linee di base, la sensibilità al paniere, la verifica a campione dei lotti. Sono le quattro cose la cui assenza ha invalidato metà dei risultati del Lab [V, riesame §2 tabella].

**Rinviare esplicitamente a F2 o oltre**: MES/aggregazione dei criteri, apprendimento bayesiano delle preferenze su persone reali, sorting logit, audit del PGT, rilevatore PU, matching dinamico.

---

## 4. Proposta di indice della PRIMA PARTE della tesi

Formato: tesi magistrale italiana (introduzione, parti, capitoli, conclusioni), ma con il rigore di un dottorato: ogni capitolo dichiara ciò che è **fonte**, **inferenza**, **ipotesi**. La prima parte è quella scrivibile prima di F2 e non dipende da dati umani. Le note di alimentazione sono indicate; **nessun capitolo si scrive da indici e mappe** (CLAUDE.md): si cita dalle schede complete o dal testo originale.

### Capitolo 1 — Introduzione
- 1.1 Il problema: crisi abitativa a Milano e la "pancia" della distribuzione (solo definizione e motivazione, i numeri vanno nel cap. 2).
- 1.2 Domanda di ricerca nelle sue due metà (promessa e controllo critico), sottodomande per scala urbana ed edificio.
- 1.3 Tesi del metodo: "il metodo è il contributo, il caso ne è la prova" [V, DECISIONI].
- 1.4 Ipotesi falsificabili con soglie fissate prima (da F0).
- 1.5 Struttura e convenzioni (marche, pre-registrazione, linee di base).
- *Alimentano*: `tesi/DOMANDA_DI_RICERCA.md`, `tesi/DECISIONI.md`, `secondo_cervello/sintesi/RIFORMULAZIONE_PHD.md`.
- *Deve contenere*: una pagina che dica cosa la tesi **non** fa (non stima la domanda reale per quartiere; non valuta il PGT; non sostituisce la decisione politica).

### Capitolo 2 — Abitare a Milano: chi è la "pancia" e che cosa si può misurare
- 2.1 Quadro del mercato e delle politiche (Piano Casa Accessibile, ERSC a ≤ 80 €/m²/anno [S → da verificare sugli atti]).
- 2.2 Definizioni di accessibilità: canone/reddito, overburden, **reddito residuo** (Stone) (nota 06 §2 punto 5).
- 2.3 Dati disponibili e loro limiti (versione testuale della matrice del §1, con licenze verificate).
- 2.4 La lezione del Lab: perché una domanda per NIL con reddito a CAP diventa una mappa degli affitti (riesame §3.2) — **questo è un risultato metodologico pubblicabile**, non un imbarazzo.
- *Alimentano*: questa nota §1; riesame 06; paper del Lab §2–3.1 e §4.1; nota 06.
- *Deve contenere*: la definizione operativa della "pancia" scelta e la sua sensibilità al paniere.

### Capitolo 3 — Cibernetica, partecipazione e mediazione
- 3.1 Cibernetica di secondo ordine e progetto (Pask, Beer/Cybersyn, Friedman, Morel) — **solo da schede complete**, molte letture sono ancora da fare in F0 [V, CALENDARIO F0 punto 4].
- 3.2 Partecipazione e potere: chi scrive criteri e pesi decide prima.
- 3.3 Il mediatore trasparente: requisiti (criteri pubblici e riscrivibili, model card, teach-back).
- *Alimentano*: corpus schede del secondo cervello, nota 04 (deliberazione mediata da IA), nota 03 §4.
- *Deve contenere*: un elenco di requisiti verificabili del "mediatore non nascosto" che i capitoli di metodo useranno come criteri di valutazione.

### Capitolo 4 — Strumenti formali per allocare, raggruppare, decidere (stato dell'arte critico)
- 4.1 Allocazione e matching: RSD, DA, TTC, PS; impossibilità; riserve e soft bounds; casi (Singapore HDB, lotterie abitative) — nota 02.
- 4.2 Gruppi eterogenei: giochi edonici, IS, fair clustering, prezzo della diversità — nota 07 §1–2.
- 4.3 Scelta sociale per criteri riscrivibili: proporzionalità, MES, aggregazione di bilanci — nota 03.
- 4.4 Preferenze: rivelate (sorting) vs dichiarate; limiti dei rispondenti LLM — nota 05.
- 4.5 Economia del lotto: valore residuo, cost-rent, CLT, limiti di equilibrio generale — nota 06.
- 4.6 Sintesi: tabella "proprietà garantite / sacrificate / spiegabilità / calcolabilità" (base: §2 di questa nota).
- *Deve contenere*: per ogni strumento, la proprietà che si sacrifica, **dichiarata**. Tutte le voci [L] delle note vanno verificate sul testo prima di entrare qui.

### Capitolo 5 — Metodo: architettura del sistema e protocollo di valutazione
- 5.1 Pipeline lotti → famiglie → gruppi → abbinamento → economia (MAPPA Parte 3).
- 5.2 Linee di base e metriche per ogni passo (§3 di questa nota).
- 5.3 Pre-registrazione, semi, intervalli, registro delle deviazioni (lezione di paper §3.7 e riesame).
- 5.4 Riproducibilità e dati (manifest, licenze).
- *Deve contenere*: le ipotesi con soglie **datate prima** degli esperimenti.

### Capitolo 6 — Il caso Milano alla scala urbana (risultati F1)
- 6.1 Lotti: procedura, verifica a campione, classi di proprietà, capacità da indici reali.
- 6.2 Economia per lotto: regioni di dominanza cooperativa vs developer, Δ_L.
- 6.3 Gruppi: curve di trade-off diversità/stabilità.
- 6.4 Abbinamento: scelta vs dall'alto vs caso.
- 6.5 Che cosa i risultati dimostrano e che cosa no (classi: evidenza / artefatto / ipotesi non testata, come nel riesame).

**Primo capitolo da scrivere [I]: il 2 (con 2.3 e 2.4), entro fine febbraio 2027.** Dipende solo dai dati del passo 1 e dal riesame, che esistono; rende concreta la matrice; produce un risultato metodologico (§2.4) che sopravvive qualunque cosa succeda dopo. Il cap. 4 si scrive a pezzi, a mano a mano che i [L] delle note vengono verificati; il cap. 3 dipende dalle letture F0 ancora aperte.

---

## 5. I cinque rischi principali di fattibilità

| # | Rischio | Perché è serio | Mitigazione |
|---|---|---|---|
| 1 | **Lotti non disponibili**: la proprietà è ignota [V, paper §2] e la capacità poggia su FAR 1,0 [V] | Il cancello di F1 è "lotti che reggono una verifica tecnica" [V, CALENDARIO]; senza proprietà un lotto "privato a valore di mercato" rende il confronto cooperativo quasi sempre perdente [I, coerente con H-a della nota 06] e la scala edificio (F3) parte da un lotto fittizio | (a) classi di proprietà e regime del suolo come **parametro di scenario**, non dato; (b) richiesta formale al Comune già in F0 [H]; (c) garantire **almeno 1–3 lotti pubblici reali** (es. aree dei bandi Piano Casa [S]) come caso di punta per F3; (d) indici dal PGT al posto del FAR fisso |
| 2 | **Reddito troppo grossolano** (38 CAP) [V] → la "domanda" ricade sugli affitti [V, riesame §3.2] | È l'errore principale del Lab; un revisore lo ritroverà subito | Non stimare domanda per NIL; definire la "pancia" per tipo di famiglia a scala di città; usare il reddito solo per costruire famiglie sintetiche plausibili; sensibilità al paniere obbligatoria; ipotesi del riesame [H: con reddito più fine la quota di varianza da reddito supera 0,25] dichiarata non testabile con dati aperti |
| 3 | **Dispersione del perimetro**: 5 famiglie di modelli + LLM + RL + scala edificio + prova reale, con ~20 h/settimana | Il Lab mostra cosa succede quando si fanno troppe cose in fretta: numeri non riconciliati tra versioni [V, riesame §3.2 "Numeri non riconciliati"] | MVP del §3 congelato a gennaio; un solo modello "di frontiera" per fase; lista "da togliere se in ritardo" decisa ora; revisione del calendario a fine fase [V, CALENDARIO] |
| 4 | **Circolarità degli agenti sintetici**: le famiglie simulate nascono dalle stesse assunzioni con cui le si valuta; gli agenti LLM riproducono stereotipi | Rischio di "dimostrare" ciò che si è codificato; la seconda metà della domanda (mediatore nascosto) diventa non testabile | Rivendicare in F1 solo **proprietà dei meccanismi** (strategy-proofness, invidia, prezzo della diversità) e confronti con linee di base; nessuna affermazione sui bisogni reali prima di F2; LLM solo per collaudo dell'interfaccia; ipotesi con soglie fissate prima |
| 5 | **Modello economico non tarato**: costi, oneri, finanza, margini sono assunzioni [V, paper §2; nota 06 Gaps] | "Più accessibile" è metà della promessa; se il motore non riproduce l'ordine di grandezza di un caso reale, il confronto developer/cooperativa è opinione | Oneri dalle tabelle ufficiali (Delibera 28/2023 [S → L]); taratura su 1–2 casi milanesi; risultato come **regione dei parametri** in cui la cooperativa domina, non come stima puntuale (nota 06 §2); un consulente esterno (estimatore o cooperativa) per una revisione di un'ora [H] |

**Rischio fuori scala urbana ma che la condiziona [I]:** la prova reale F2 (mag–lug 2027) ha partner non ancora scelto [V, DECISIONI]. Se F1 slitta di un mese, F2 si comprime sotto i tempi di un consenso informato e del reclutamento. Mitigazione: contattare 2–3 possibili partner (cooperative, associazioni di inquilini) già a marzo 2027, anche prima che il sistema sia finito, per i tempi burocratici.

---

## 6. Cose da verificare subito (lista per F0/inizio F1)

1. ISTAT: elenco delle variabili per sezione 2021 (titolo di godimento? tipo di nucleo?) e rapporto con l'edizione 2023 [L].
2. MEF: struttura del dataset IRPEF sub-comunale 2024 (CAP? classi?) e licenza [L].
3. OMI: procedura di download dei perimetri e licenza esatta [S → V].
4. dati.comune.milano.it: licenza dello shapefile NIL (ds61) [L]; dataset di patrimonio comunale e GTFS [L].
5. Geoportale Lombardia: licenza di DBT e DUSAF 2024 nella scheda metadati [L].
6. Comune di Milano: tabelle ufficiali degli oneri (Delibera CC 28/2023) e costo base del contributo [L].
7. Atti del Piano Casa (DGC 365/2026, bandi delle tre aree) per canoni e parametri [S → V].
8. Pacchetti Python (`matching`, `pabutools`, `pyblp`, `SALib`, `ipfn`, `r5py`): verificarne autenticità e versione prima di installarli [L].

## Fonti web consultate in questa sessione (solo sintesi di ricerca, [S])
- ISTAT, Nota informativa Basi territoriali 2021: https://www.istat.it/wp-content/uploads/2024/07/Nota-informativa-Basi-territoriali-2021.pdf ; pagina "Basi territoriali e variabili censuarie": https://www.istat.it/notizia/basi-territoriali-e-variabili-censuarie/
- Cartografia catastale aperta (CC-BY 4.0, GML): https://ediltecnico.it/catasto-e-dati-territoriali-aperti-entrate-lancia-i-primi-servizi-open-data/ ; https://www.lavoripubblici.it/news/stampa/35094
- MEF, Dichiarazioni fiscali: https://www1.finanze.gov.it/finanze/pagina_dichiarazioni/public/dichiarazioni.php
- OMI: https://github.com/ondata/quotazioni-immobiliari-agenzia-entrate ; https://www.idealista.it/news/node/137281
- Piano Casa Milano: https://www.assolombarda.it/servizi/immobili-urbanistica-e-territorio/informazioni/casa-accessibile-nuove-linee-di-indirizzo-del-piano-straordinario-del-comune-di-milano ; https://quifinanza.it/mercato-immobiliare/piano-casa-milano-case-canone-calmierato/859762/
- Oneri Milano: https://www.osborneclarke.com/it/insights/nuovi-criteri-applicativi-merito-alla-delibera-del-consiglio-comunale-n-282023 ; https://www.milanofree.it/milano/cronaca/milano-aggiorna-gli-oneri-di-urbanizzazione-un-nuovo-modello-per-favorire-la-rigenerazione-urbana.html ; https://realadvisor.it/it/blog/quanto-costa-urbanizzare-un-terreno
- Geoportale Lombardia: https://www.geoportale.regione.lombardia.it/ricerca
- NIL PGT 2030: https://dati.comune.milano.it/dataset/ds964-nil-vigenti-pgt-2030/resource/3fce7202-0076-4a7b-ac2c-d2ab9b5dc658
