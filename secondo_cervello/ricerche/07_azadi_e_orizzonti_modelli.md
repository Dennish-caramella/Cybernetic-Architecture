# 07. Azadi (TU/e) e orizzonti di modelli per la Fase 1

Ticket: GitHub Dennish-caramella/Cybernetic-Architecture #7 (figlio di #5). Data di consultazione: 2026-10-27.

## Domanda

Che cosa dicono, a livello di abstract e di articoli ad accesso aperto, la tesi di Azadi (Augmented Urban Planning, TU/e) e i lavori collegati? Quali modelli scientifici e matematici sono candidati per Spatial Milano Lab, e con quale grado di verifica?

## Come leggere le etichette (e un limite di metodo)

- `[V]` letto nella fonte in questa sessione. **Attenzione**: gli strumenti di lettura restituiscono una sintesi automatica della pagina o del PDF, non il testo grezzo. `[V]` vale quindi «pagina o abstract aperti e letti nella sintesi», non «lettura integrale». Dove ho aperto un PDF lo dico.
- `[S]` riportato da una scheda del corpus (`37_*`), non riaperto da me.
- `[I]` inferenza. `[H]` ipotesi.
- Stato fonte: `verificata` = aperta e letta; `da verificare` = vista solo in scheda o in risultati di ricerca, o aperta con metadati incompleti.
- Dove una fonte non si è aperta, c'è scritto. La tesi integrale è sotto embargo fino al 2027-09-23: non è stata cercata né letta.

## 1. Che cosa si è potuto aprire dell'universo Azadi

| # | Fonte | Stato | Cosa è stato letto |
|---|---|---|---|
| A1 | Azadi, S. (2026). *Augmented Urban Planning: A Systematic Framework for Sociotechnical Integration of Digital Representations in Urban Planning*. Tesi PhD, TU/e. https://research.tue.nl/en/publications/augmented-urban-planning-a-systematic-framework-for-sociotechnica/ | da verificare (record non riaperto; testo sotto embargo) | `[S]` dalla scheda 37: record, abstract, promotore van Wesemael, copromotori Kasraian e Nourian. Nessun DOI. |
| A2 | Azadi, Kasraian, Nourian, van Wesemael (2025). *What Have Urban Digital Twins Contributed to Urban Planning and Decision Making? From a Systematic Literature Review Toward a Socio-Technical Research and Development Agenda*. Smart Cities 8(1), 32. DOI 10.3390/smartcities8010032. https://www.mdpi.com/2624-6511/8/1/32 | **verificata** (pagina MDPI, ad accesso aperto) | `[V]` sotto |
| A3 | Azadi, Kasraian, Nourian, van Wesemael (2025; fascicolo 2026). *Formalizing-modelling-utilizing ontology: A semantic framework for adaptive stakeholder-specific urban digital twins in urban planning processes*. Environment and Planning B 53(4), 804–830. DOI 10.1177/23998083251329398. Record: https://research.tue.nl/en/publications/formalizing-modelling-utilizing-ontology-a-semantic-framework-for/ | **verificata a livello di abstract e metadati**; PDF CC BY-NC 4.0 **non apribile** (403 dal proxy; fetch fallito) | `[V]` sotto |
| A4 | Azadi, Kasraian, Nourian, van Wesemael (2025). *Stakeholder-Specific Urban Digital Twins as Means for Participatory Planning: Evaluation of the FMU Ontology*. CUPUM 2025, art. 167. https://osf.io/mkqfe | da verificare | `[S]` dalla scheda 37. La pagina OSF si apre ma è vuota (solo titolo del sito). |
| A5 | Azadi, Nourian, Kasraian, van Wesemael. *Participatory Digital Twinning for Urban Planning Processes: Evaluation of Interdisciplinary Integration*. SSRN, DOI 10.2139/ssrn.6571117 | da verificare | Il titolo e gli autori compaiono nei risultati di ricerca; la pagina non si è potuta aprire. Abstract, data e stato (preprint) ignoti. |
| A6 | Azadi, Bai, Nourian (2024; vol. 9 del 2023). *Ergonomics of spatial configurations: a voxel-based modelling framework for accessibility and visibility simulations*. Frontiers in Built Environment 9. DOI 10.3389/fbuil.2023.1300843. https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2023.1300843/full | **verificata** (pagina, accesso aperto) | `[V]` sotto. Nuova rispetto al corpus. |
| A7 | Azadi, *Augmented Urban Planning: A Framework for Strategic Urban Planning* (ResearchGate, 2023) | da verificare | Solo titolo nei risultati di ricerca; autori e sede non confermati; pagina non apribile. |

### Che cosa dicono A2, A3, A6 `[V]`

- **A2.** Rassegna PRISMA 2020 di 88 articoli (ricerca su Scopus al 2024-12-31; un solo ricercatore per lo screening). Tre categorie di sfide sociotecniche: integrazione interdisciplinare (II), contestualizzazione consensuale (CC), operazionalizzazione procedurale (PO). L'integrazione interdisciplinare ha ricevuto più attenzione (oltre l'80% dei contributi implementativi). Nella CC, la maggior parte degli studi considera stakeholder ipotetici e solo tre coinvolgono cittadini. Nessuna implementazione risulta integrata in un vero processo di pianificazione. L'AUP definisce un UDT ideale come raccolta coerente di dati e modelli e propone un quadro con UDT personalizzabili, specifici e adattivi. Modelli citati dalle opere recensite (non dagli autori come proprie scelte): knowledge graph (World Avatar), traffico agent-based, federated learning, differential privacy, standard IFC/COBie. Limiti dichiarati dagli autori: solo Scopus, solo inglese, solo letteratura peer reviewed; esclusi i campi vicini (smart city, planning support systems); quadro descritto come «mero schema speculativo» bisognoso di prova in pratica; mancano metodi di valutazione per ciascuna dimensione.
- **A3.** L'ontologia FMU offre rappresentazioni semantiche per tre scopi: interoperabilità tra dati e modelli disciplinari; reti di UDT specifici per stakeholder; inserimento nei flussi di pianificazione. Validazione con test di consistenza e di competenza; caso: densificazione strategica a Eindhoven. La pagina non indica dati né codice disponibili. Il portale TU/e riserva i contenuti anche al text-and-data-mining e all'addestramento di IA: da rispettare se si pensa di darli a un modello.
- **A6.** Il lavoro più «matematico» del gruppo trovato: spazi pedonabili voxelizzati, grafi di accessibilità e di visibilità come matrici sparse, centralità di Katz (con il pacchetto topoGenesis), due dimostrazioni (una mesh ipotetica, un distretto di Rotterdam). Dichiarati dagli autori: non è una simulazione del comportamento reale di camminata; nessuna validazione empirica; modelli associativi e generativi solo come lavoro futuro; il grafo di visibilità è molto denso; sensibilità di Katz al parametro di attenuazione non valutata; dati dell'esempio con link non funzionante.

### Cosa non si è trovato `[L]`

- Il Dynamic Knowledge Graph usato dalla tesi per la valutazione, il toolbox open source (repository, licenza), i capitoli su CC e PO: nessuna fonte aperta li descrive. `[S]` La scheda 37 lo conferma. Il termine «entropia» tra i tag del record TU/e è un tag automatico: non permette di dire che la valutazione sia basata sull'entropia `[H]`.
- Limiti dichiarati da Azadi nei lavori A3–A5: non leggibili.

## 2. Lettura per Spatial Milano Lab `[I]`

Il lab (`spatial_milano_lab/lab/`) ha già, nei documenti di proposta e nei riassunti, i modelli seguenti: filtro di dominanza e SMAA sui criteri, selezione attiva delle domande (guadagno informativo atteso, EIG), prior di popolazione, aggregazione con seq-PAV e audit di Justified Representation, accessibilità E2SFCA, rilevatore PU di siti, Moran/FDR e max-p per le regioni di bisogno. I riferimenti del lab sono marcati «dalla memoria». Qui sotto si sale di livello solo dove ho aperto la fonte.

Azadi non fornisce un modello di selezione dei lotti `[I]`: A2 e A3 sono quadro, ontologia e valutazione di processo; A6 fornisce grafi di accessibilità e centralità. L'apporto concreto è (a) una griglia di valutazione sulle tre dimensioni (II, CC, PO), (b) una struttura per rendere i criteri e i dati tracciabili e specifici per attore, (c) il grafo voxel come alternativa di accessibilità a scala fine. Tutti gli altri candidati vengono dalla letteratura di base qui sotto.

## 3. Modelli candidati e grado di verifica

Convenzione: «verifica della fonte» = quanto ho letto; «verifica nel lab» = ciò che il lab riporta come risultato `[S]` (sintetico o reale come dichiarato nei suoi file; non l'ho ricalcolato).

### 3.1 Decisione multicriterio e incertezza dei pesi

| Modello | Fonte | Stato | Cosa dice `[V]` | Limiti / bias |
|---|---|---|---|---|
| SMAA (analisi stocastica di accettabilità multicriterio) | Lahdelma, Hokkanen, Salminen (1998). *SMAA - Stochastic multiobjective acceptability analysis*. European Journal of Operational Research 106(1), 137–143. https://sal.aalto.fi/publications/abstracts/plah98.html | **verificata** (abstract; DOI non mostrato dalla pagina) | Invece di chiedere i pesi, esplora lo spazio dei pesi e dà per ogni alternativa un indice di accettabilità, un peso centrale e un fattore di confidenza; gli input incerti sono distribuzioni di probabilità. | Solo abstract letto. Il risultato dipende dalle distribuzioni scelte per pesi e punteggi `[I]`. |
| SMAA-2 | Lahdelma, Salminen (2001). *SMAA-2: Stochastic Multicriteria Acceptability Analysis for Group Decision Making*. Operations Research 49(3), 444–454. https://sal.aalto.fi/publications/abstracts/plah01.html | **verificata** (abstract) | Considera l'intero spettro dei ranghi, non solo il primo posto; fa emergere candidati di compromesso; gestisce informazione parziale sulle preferenze. | Come sopra. `[S]` Il lab osserva che nessun lotto è primo per più del 8–15% dei vettori di pesi: l'output va letto come probabilità. |
| Quadro GIS-MCDA | Malczewski (2006). *GIS-based multicriteria decision analysis: a survey of the literature*. IJGIS 20(7), 703–726. DOI 10.1080/13658810600661508 (pagina scilit) | **verificata** (metadati e abstract; autore non mostrato dalla pagina, attribuzione a Malczewski dalla mia ricerca, titolo coincidente) | Rassegna di oltre 300 articoli 1990–2004, con tassonomia. | Fonte del 2006; non copre le tecniche di dopo. Non ho letto le critiche sui pesi. |

### 3.2 Accessibilità

| Modello | Fonte | Stato | Cosa dice `[V]` | Limiti / bias |
|---|---|---|---|---|
| E2SFCA | Luo, Qi (2009). *An enhanced two-step floating catchment area (E2SFCA) method for measuring spatial accessibility to primary care physicians*. Health & Place 15(4), 1100–1107. DOI 10.1016/j.healthplace.2009.06.002 (registro bibliotecario bib-bvb) | **verificata** (abstract) | Estende la 2SFCA pesando le fasce di tempo di viaggio (decadimento con la distanza); è un caso particolare del modello gravitazionale; applicata a medici di base in Illinois. | Nata per la sanità; per scuole, verde e servizi a Milano è un trasferimento `[I]`. `[S]` Il lab osserva instabilità dove la popolazione è bassa e usa la normalizzazione per rango. |
| E2SFCA a confronto con misure semplici | Drake et al. (2021). *A comparison of methods for measuring spatial access to health care*. Health Services Research 56(5), 777–787. https://deepblue.lib.umich.edu/items/b1257328-d320-4f30-853b-26f1267d5988/full | **verificata** (pagina) | Distanza euclidea, tempo di viaggio e rapporto fornitori/popolazione mancano, rispetto alla E2SFCA, tra il 30% e il 52% dei tratti a basso accesso (caso: prescrittori di buprenorfina, 14 contee della Pennsylvania). | Un solo caso sanitario USA. |
| Grafi voxel di accessibilità/visibilità e centralità di Katz | A6 (Azadi, Bai, Nourian) | **verificata** | Vedi sopra. | Non validata empiricamente; costosa; scala di edificio e di quartiere più che di città intera `[I]`. |

### 3.3 Apprendimento delle preferenze e domande attive

| Modello | Fonte | Stato | Cosa dice `[V]` | Limiti / bias |
|---|---|---|---|---|
| Apprendimento attivo bayesiano (BALD) per classificazione e preferenze a coppie | Houlsby, Huszár, Ghahramani, Lengyel (2011). *Bayesian Active Learning for Classification and Preference Learning*. arXiv:1112.5745 (preprint) | **verificata** (abstract) | Criterio di informazione attesa riscritto con entropie predittive; applicato a classificatori gaussiani e al GP di preferenze a coppie. | Preprint su arXiv; non controllata una versione pubblicata. Il lab usa EIG su un modello di pesi, non un GP: parentela, non identità `[I]`. |

### 3.4 Aggregazione e giustizia della rappresentanza

| Modello | Fonte | Stato | Cosa dice `[V]` | Limiti / bias |
|---|---|---|---|---|
| Axiomi di rappresentanza proporzionale nel bilancio partecipativo (approvazioni) | Aziz, Lee, Talmon (2017). *Proportionally Representative Participatory Budgeting: Axioms and Algorithms*. arXiv:1711.08226 (senza sede indicata dalla pagina) | **verificata** (abstract) | Adatta la rappresentanza proporzionale delle elezioni multi-vincitore al bilancio partecipativo; la difficoltà di calcolo varia molto; presenta metodi che soddisfano gli assiomi. | La pagina non nomina seq-PAV né JR: il legame con ciò che usa il lab è `[I]`. |
| Idem, con preferenze ordinali | Aziz, Lee (2020, v2). *Proportionally Representative Participatory Budgeting with Ordinal Preferences*. arXiv:1911.00864; AAAI 2021 (https://ojs.aaai.org/index.php/AAAI/article/view/16646) | **verificata** (abstract arXiv; pagina AAAI non aperta) | Introduce IPSC; PAV soddisfa EJR e IPSC; algoritmo in tempo polinomiale. | Come sopra. |

La definizione originale di Justified Representation (Aziz et al. 2017, committee voting) e la regola seq-PAV: **non aperte** `[L]`. `[S]` Il lab riporta che media dei pesi, Borda e Kemeny violano JR con una minoranza polarizzata e che seq-PAV conserva più rappresentanza al prezzo di 0,05–0,08 di soddisfazione totale (dati sintetici).

### 3.5 Deliberazione assistita da IA e consenso

| Modello | Fonte | Stato | Cosa dice `[V]` | Limiti / bias |
|---|---|---|---|---|
| Habermas Machine | Tessler et al. (2024). *AI can help humans find common ground in democratic deliberation*. Science 386, eadq2852. DOI 10.1126/science.adq2852. Letta su copia PDF (https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf), non sul sito della rivista | **verificata** (copia terza) | Due modelli linguistici: uno propone dichiarazioni di gruppo, un modello di ricompensa personalizzato prevede i ranghi di ciascuno; aggregazione col metodo di Schulze. 5.734 partecipanti; 75 gruppi di sei con mediatori umani (439 persone); assemblea virtuale di 200. Dichiarazioni dell'IA preferite 56% a 44%; accordo in aumento di circa 6–9 punti. Mediazione senza IA: nessuno spostamento. | Autori: campione di convenienza, UK, gruppi piccoli, nessun controllo dei fatti né moderazione, accordo non sempre desiderabile. `[I]` Misura il consenso su opinioni, non scelte su lotti con vincoli. Sætra (critica, CACM): `[S]`, da verificare. |
| Polis | Small, Bjorkegren, Erkkilä, Shaw, Megill (2021). *Polis: Scaling Deliberation by Mapping High Dimensional Opinion Spaces*. Recerca 26(2), 1–26. DOI 10.6035/recerca.5516 (https://www.e-revistes.uji.es/index.php/recerca/article/view/5516; contenuto letto da copia PDF gwern.net) | **verificata** | Matrice di voti (+1/−1/0), PCA a 2D, K-means a due livelli con scelta di K per silhouette, metrica di consenso consapevole dei gruppi; caso vTaiwan su Uber (circa 1.238 partecipanti). | Autori: funziona male con gruppi piccoli o pochi commenti; dipende da moderatori in buona fede; gestione dei dati mancanti ad hoc; i partecipanti precoci votano più commenti. `[I]` Mappa opinioni, non preferenze su alternative spaziali. |
| Pianificazione partecipativa simulata con agenti LLM | Zhou, Lin, Jin, Li (2024). *Large Language Model for Participatory Urban Planning*. arXiv:2402.17161 (preprint) | **verificata** (abstract) | Pianificatore e popolazione di residenti, entrambi LLM, sul piano d'uso del suolo; test su due distretti di Pechino; punteggi dichiarati di soddisfazione e inclusività. | Non ci sono residenti reali: il bisogno è generato dal modello. `[S]` Il corpus riporta lo stesso limite. È un controesempio da usare come tale. |

### 3.6 Apprendimento a partire da esempi positivi (siti noti) e validazione spaziale

| Modello | Fonte | Stato | Cosa dice `[V]` | Limiti / bias |
|---|---|---|---|---|
| Classificatore PU (positivi e non etichettati) | Elkan, Noto (2008). *Learning Classifiers from Only Positive and Unlabeled Data*. KDD '08. Letta su copia PDF (mirror CBIO Mines ParisTech). DOI non verificato | **verificata** (copia terza; DOI non mostrato) | Ipotesi «selezionati completamente a caso»: ogni positivo ha la stessa probabilità di essere etichettato; stima della costante c con tre stimatori. | Gli autori: stime esatte solo con probabilità ben calibrate; un solo dominio testato (proteine). `[I]` Per i lotti la selezione dei siti da parte dei pianificatori non è a caso: l'ipotesi è violata. `[S]` Il lab osserva c da 0,055 a 0,51 tra i blocchi e usa il punteggio solo come rango. |
| Validazione a blocchi | Roberts et al. (2017). *Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure*. Ecography 40, 913–929. DOI 10.1111/ecog.02881 (copia PDF, Univ. Freiburg) | **verificata** | La validazione incrociata casuale è ottimista su dati con dipendenza; raccomandati blocchi più larghi dell'autocorrelazione residua. | Blocchi troppo grandi inducono estrapolazione. `[S]` Il lab riporta PR-AUC 0,928 con piegature casuali contro 0,326 con blocchi di 4 km. |

### 3.7 Struttura spaziale del bisogno

| Modello | Fonte | Stato | Cosa dice `[V]` | Limiti / bias |
|---|---|---|---|---|
| max-p-regions | Duque, Anselin, Rey (2012). *The max-p-regions problem*. Journal of Regional Science 52(3), 397–419. DOI 10.1111/j.1467-9787.2011.00743.x (https://asu.elsevierpure.com/en/publications/the-max-p-regions-problem/) | **verificata** (abstract) | Raggruppa aree in quante più regioni omogenee possibile, con soglia minima per un attributo additivo; programmazione intera mista più euristica. | Risultato dipende dalla soglia e dalla soluzione euristica; `[S]` il lab misura ARI 0,71 tra varianti. |
| Moran globale/locale con FDR | non cercata | da verificare | — | — |

### 3.8 Modelli di mercato e di simulazione urbana

| Modello | Fonte | Stato | Cosa dice `[V]` | Limiti / bias |
|---|---|---|---|---|
| UrbanSim | Waddell (2002). *UrbanSim: Modeling Urban Development for Land Use, Transportation, and Environmental Planning*. JAPA 68(3), 297–314. DOI 10.1080/01944360208976274 (pagina scilit); testo letto da copia PDF (nature.berkeley.edu) | **verificata** (copia terza) | Componenti: scelta di localizzazione delle famiglie (multinomial logit), sviluppatore (logit), prezzo del suolo (regressione edonica). | Autore: test su dati con crescita modesta, dati base del 1980 con errori, non per l'uso fine a 150 m, eventi isolati non previsti. È un modello del 2002 per Eugene-Springfield. `[S]` Il corpus riporta il repository open source e la licenza: non verificati. |
| Gemelli digitali urbani, quadro dei modelli | Batty (2024), *Digital twins in city planning*, Nature Computational Science 4, 192–199, DOI 10.1038/s43588-024-00606-7 | da verificare (`[S]` dal corpus; non riaperta) | — | — |

## 4. Fonti del corpus non riaperte

Restano `[S]`/`da verificare`: Ketzler et al. 2020; Caprari et al. 2022; De Jaeger e Swerts 2026; Altındaş et al. 2026; Dembski et al. 2020; Schrotter e Hürzeler 2020; Safransky 2020; Flechtner (arXiv 2608.10186); Sætra (CACM); Roy, Lessig, Tang (arXiv 2503.11714); Zali et al. 2026. Non ho verificato nulla di quanto il corpus afferma su di esse.

## 5. Bias e limiti dell'insieme

1. **Gran parte delle fonti metodologiche viene da altri domini.** E2SFCA dalla sanità, PU dalla bioinformatica, Roberts dall'ecologia, Houlsby dal machine learning generale. Il trasferimento a Milano e ai lotti è `[I]`, non evidenza.
2. **Livello di lettura basso.** Quasi tutto è abstract o sintesi automatica di pagina. Nessuna cifra qui è stata controllata sul PDF originale, tranne quando indicato come copia PDF; anche lì la lettura passa dalla sintesi.
3. **Fonti terze.** Tessler, Polis, Elkan–Noto, Roberts e Waddell sono state lette su copie ospitate da terzi; i dati bibliografici coincidono con i metadati delle pagine ufficiali dove li ho trovati, ma la copia non è la versione di riferimento.
4. **Azadi tratta esperti, non abitanti.** `[V]` Per A2 la maggior parte delle UDT recensite usa stakeholder ipotetici e solo tre studi coinvolgono cittadini; `[S]` per A4 il workshop è di 12 esperti. Il progetto del lab è diverso per costruzione.
5. **Autoreferenzialità del gruppo.** A2–A5 hanno gli stessi quattro autori e la mappatura articolo-capitolo è `[I]`.
6. **Bias di pubblicazione e di ricerca.** Ricerca web limitata a pagine accessibili; Google Scholar e PDF di editore bloccati (403). Assenza di una fonte nei risultati non prova che non esista.
7. **Costo del suolo e mercato.** `[S]` Safransky avverte che criteri di mercato riproducono la storia dei prezzi; non l'ho riletta. Resta un rischio per il criterio «costo».
8. **IA e consenso.** Il guadagno di accordo di Tessler et al. è misurato su opinioni di volontari; non dimostra che un consenso su lotti sia legittimo `[I]`.
9. **Regola del lab** (README, regola 4): niente punteggi di idoneità su singole famiglie (AI Act All. III 5a). I modelli di questa nota vanno applicati a lotti e portafogli di lotti `[S]`.
10. **Diritti.** Il portale TU/e riserva i contenuti al text-and-data-mining e all'addestramento di IA `[V]`: prima di dare i PDF a un modello, verificare la licenza reale.

## 6. Cosa resta da fare (ordine di priorità)

1. Aprire il PDF di A3 da una rete senza blocco (URL del record TU/e) e leggere: classi dell'ontologia, domande di competenza, limiti dichiarati, link a dati e codice.
2. Aprire A4 (OSF) e A5 (SSRN) per verificare se descrivono il Dynamic Knowledge Graph e il toolbox.
3. Leggere sul testo originale Aziz et al. 2017 (JR) e la definizione di seq-PAV.
4. Verificare Batty 2024 e le fonti del corpus elencate al punto 4, se serviranno nella tesi.
5. Cercare fonti sul contesto italiano (L.R. 18/2019, PGT, OMI) e su Moran/LISA: fuori dall'ambito di questa nota.

## In breve

Dell'universo Azadi sono verificate a livello di pagina la rassegna sugli UDT (Smart Cities 2025), l'abstract dell'ontologia FMU (Environment and Planning B) e il lavoro sui grafi voxel (Frontiers 2024). Il PDF dell'ontologia, la pagina OSF e quella SSRN non si sono aperti. Azadi fornisce una griglia di valutazione (II, CC, PO), non un metodo di scelta dei lotti: i candidati sono SMAA, E2SFCA, apprendimento attivo bayesiano, seq-PAV/JR, PU con validazione a blocchi, max-p. Sono tutte fonti aperte a livello di abstract, di domini diversi da Milano. Habermas Machine, Polis e agenti LLM sono riferimenti sul consenso e controesempi. Letto quasi solo abstract o sintesi; nessuna cifra ricontrollata sull'originale.
