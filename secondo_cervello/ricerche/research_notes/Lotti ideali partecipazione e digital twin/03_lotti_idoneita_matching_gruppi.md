# Metodi computazionali per idoneità dei lotti e matching gruppi–lotti (stato al 2026-11)

Note di ricerca (agente), 2026-11-09. Uso: prove/materiale di lavoro, NON fonte citabile. Per citare, aprire il testo originale.
Legenda verifica: **[ver.]** = metadati (autori, anno, sede, DOI/URL) confermati in questa sessione da almeno un record bibliografico o pagina dell'editore/repository; **[non ver.]** = riportato da memoria o da snippet secondari, da controllare prima di citare. Nessun full text è stato letto: i risultati numerici vengono da abstract/record/riassunti di ricerca e vanno controllati sul testo.

## 1. Idoneità dei lotti per abitazioni (accessibili): GIS-MCDA, SMAA, sensitività, ML, GNN, embedding

### Takeaway
GIS-MCDA (overlay pesato, AHP, TOPSIS) resta lo standard negli studi applicati di localizzazione di abitazioni sociali o economiche. Questi studi sono quasi tutti piccoli casi studio con pesi elicitati, poca analisi d'incertezza e nessuna validazione esterna. SMAA è il modo consolidato per rendere esplicita l'incertezza sui pesi, e ha precedenti di localizzazione in ambito GIS (discariche, impianti). I modelli ML ed embedding (satellite, street view, foundation model geospaziali) sono la frontiera, ma ci vuole una "verità" etichettata, che per l'idoneità residenziale non esiste. Inoltre la loro valutazione è fragile per via dell'autocorrelazione spaziale.

### Cited Findings
**MCDA classica e casi applicati**
- Un preprint del 2026 riassume la prassi: la selezione dei siti usa AHP, TOPSIS e overlay GIS, metodi efficaci su problemi piccoli ma che "scalano male" a scala metropolitana con migliaia di particelle. Lo stesso preprint propone RL multi-obiettivo con vincoli normativi. [non ver.: preprint arXiv non revisionato, non letto per intero] — [arXiv 2602.03940](https://arxiv.org/pdf/2602.03940)
- Area funzionale di Wrocław (Polonia), GIS-MCA per aree di nuova residenza: i gruppi di criteri più pesati sono le infrastrutture di trasporto (31%) e quelle tecniche (28%). [non ver.: solo record ResearchGate] — [ResearchGate](https://www.researchgate.net/publication/311765727_Application_of_multi-criteria_analysis_in_GIS_for_optimal_planning_of_house_development_areas_Case_study_of_Wroclaw_Functional_Area)
- Babolsar (Iran), AHP+GIS per abitazioni a basso reddito, con criteri raccolti in quattro gruppi: socio-economici, fisici, verde, inclusività. [non ver.] — [ResearchGate](https://www.researchgate.net/publication/355661170_Low-income_housing_location_based_on_affordable_criteria_Using_AHP_Model_and_GIS_Technique_Case_Study_Babolsar_City)
- Al-Shalabi et al., FIG 2006, sulla housing site suitability con GIS-MCDA (AHP). È un paper di conferenza professionale. — [FIG 2006 PDF](https://www.fig.net/resources/proceedings/fig_proceedings/fig2006/papers/ts72/ts72_05_alshalabi_etal%20_0702.pdf)
- Uso istituzionale recente: San Francisco Planning, "Affordable Housing Sites Analysis and Strategies" (dicembre 2025). Applica filtri GIS sulle particelle, con ipotesi spaziali e di programma edilizio, per individuare i siti adatti al 100% affordable. È la cosa più vicina al passo (1) della pipeline di Dennis: filtro di particelle con assunzioni esplicite, non punteggio di idoneità. — [SF Planning PDF](https://sfplanning.org/sites/default/files/documents/citywide/AHSAS-final-report-2025.pdf)
- Londra (Hammersmith & Fulham), MCA GIS con 12 criteri per lo housing sociale: tutti i lotti risultanti cadono nelle categorie d'uso del suolo preselezionate (brownfield, orti). Il filtro iniziale ha quindi determinato l'esito. È una story map, non letteratura revisionata. — [ArcGIS StoryMap](https://storymaps.arcgis.com/stories/5c47e7cafb344b1b838dbadcbe3c961d)
- MIVES (Barcellona) è un metodo multicriterio di sostenibilità usato per prioritizzare investimenti pubblici (Land Use Policy 2017, 64:29–37). Una variante GIS + MIVES–Knapsack, pubblicata su Sustainability nel 2022, è stata usata per alloggi temporanei. [riferimento LUP 2017 non ver.; Sustainability ver. via DOI] — [doi:10.3390/su14084453](https://doi.org/10.3390/su14084453)
- Non ho trovato uno studio revisionato europeo che usi esplicitamente il binomio "social/affordable housing site selection + GIS-MCDA" in una grande città, con incertezza e validazione. Vedi Gaps.

**SMAA**
- Lahdelma, Hokkanen, Salminen (1998, EJOR) definiscono SMAA come esplorazione dello spazio dei pesi per più decisori. Gli output sono indici di accettabilità, vettori di pesi centrali e fattore di confidenza. I dati incerti sono rappresentati come distribuzioni di probabilità. [ver.] — [Aalto SAL](https://sal.aalto.fi/publications/abstracts/plah98.html)
- Lahdelma, Salminen, Hokkanen (2002, EJOR): SMAA-O per localizzare un impianto rifiuti vicino a Lappeenranta, senza preferenze e con criteri solo ordinali. Simula tutte le mappature ordinale→cardinale che conservano l'ordine. [ver.] — [Aalto research](https://research.aalto.fi/en/publications/locating-a-waste-treatment-facility-by-using-stochastic-multicrit/)
- Demesouka, Anagnostopoulos, Siskos (2019, EJOR 272(2):574–586): SMAA dentro un GIS raster per localizzare discariche (Grecia nord-orientale). SMAA indica con che frequenza un sito ottiene le prime posizioni in un insieme ampio di siti. È il precedente metodologico più vicino a "SMAA su particelle". [ver.] — [RePEc](https://ideas.repec.org/a/eee/ejores/v272y2019i2p574-586.html)
- Rassegna: Pelissari et al. (2020), 118 articoli SMAA tra 1998 e 2017. [non ver.: solo record repository] — [Mackenzie DSpace](https://dspace.mackenzie.br/items/4044d41b-4a7b-4b5d-ad3f-b7f2b5b6b0d8/full)

**ML, validazione spaziale**
- Ploton et al. (2020, Nature Communications, doi:10.1038/s41467-020-18321-y): con la cross-validation casuale si ignora la dipendenza tra campioni vicini e la stima delle prestazioni risulta "biased, overly optimistic". Con validazione spaziale, i modelli di mappatura su larga scala hanno prestazioni predittive scarse. [ver.] — [Nature Comms 2022 (risposta)](https://www.nature.com/articles/s41467-022-29838-9)
- Meyer & Pebesma (2022, Nature Communications, doi:10.1038/s41467-022-29838-9): con dati di riferimento sparsi e non rappresentativi, non si può valutare il modello nelle aree con condizioni molto diverse da quelle di training. Propongono di valutare l'area di applicabilità del modello, non solo un errore medio. [ver.] — [Nature](https://www.nature.com/articles/s41467-022-29838-9); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9033849)
- Posizione contraria: Wadoux et al. (2021) sostengono che la spatial CV non ha fondamento teorico per stimare l'accuratezza di una mappa. Con dati raccolti per campionamento probabilistico, la stima design-based è corretta. La CV standard resta però difettosa su dati clusterizzati. **La questione è aperta in letteratura.** [non ver.: solo record WUR] — [WUR](https://research.wur.nl/en/publications/spatial-cross-validation-is-not-the-right-way-to-evaluate-map-acc/)
- Rassegna sulle sfide di valutazione del geospatial ML. [non ver.] — [arXiv 2303.18087](https://ar5iv.labs.arxiv.org/html/2303.18087)

**Embedding satellitari, street-view e foundation model**
- Inghilterra (studio 2026, PMC): embedding di un foundation model geospaziale a 128 dimensioni sono competitivi con feature da censimento, copertura del suolo e morfologia urbana nel predire inquinamento e prezzi delle case. [non ver.: non letto per intero] — [PMC13497279](https://pmc.ncbi.nlm.nih.gov/articles/PMC13497279/)
- AlphaEarth (embedding a 64 dimensioni, risoluzione 10 m) usato con dati di mobilità come connettori di grafo (MobFusion, preprint 2026). [non ver.] — [arXiv 2606.01745](https://arxiv.org/html/2606.01745)
- CityLens: benchmark di vision-language model per predire indicatori socioeconomici da immagini satellitari e street view. 17 città, 11 indicatori. [non ver.] — [arXiv 2506.00530](https://arxiv.org/html/2506.00530)
- KnowCL: apprendimento contrastivo con knowledge graph su immagini satellitari e street view. Riporta guadagni di R² superiori al 30% rispetto ai baseline. [non ver.] — [arXiv 2302.13094](https://arxiv.org/abs/2302.13094)
- Preprint 2026 su embedding AlphaEarth/AnySat/TerraMind per la vivibilità urbana, con modello spaziale che tiene conto della dipendenza spaziale. [non ver.] — [arXiv 2609.09429](https://arxiv.org/pdf/2609.09429v1)
- GNN e RL su grafo di contiguità urbana: Zheng et al. (2023, Nature Computational Science 3:748–762, doi:10.1038/s43588-023-00503-5). Pianificano l'uso del suolo di comunità come processo decisionale di Markov, con DRL su GNN. Dichiarano risultati superiori ai piani di esperti sulle metriche oggettive del modello. Codice pubblico con due casi reali a Pechino. [ver.] — [Nature](https://www.nature.com/articles/s43588-023-00503-5); [GitHub mirror](https://git.tdem.in/tsinghua-fib-lab/DRL-urban-planning)

### Inferences
- **[inferenza]** Per il passo (1), la letteratura applicata sostiene "filtro di vincoli duri, poi MCDA con incertezza esplicita" più che un modello ML di idoneità. Manca un target osservato di idoneità residenziale: le alternative proxy (costruito recente, prezzo OMI) incorporerebbero proprio le dinamiche di mercato che la tesi critica. Un modello ML addestrato su "dove si è costruito" impara la redditività, non l'idoneità sociale.
- **[inferenza]** SMAA è coerente con il prototipo esistente, e il caso Demesouka 2019 fornisce un precedente revisionato su GIS raster. La lezione del caso di Londra vale anche per Milano: i filtri a monte (DUSAF/PGT) possono determinare il risultato più dei pesi. Conviene quindi una sensitività anche sulle soglie dei filtri, non solo sui pesi.
- **[inferenza]** Se si usano embedding (AlphaEarth e simili) come feature, servono una validazione a blocchi spaziali o a "area di applicabilità" (Meyer & Pebesma) e una dichiarazione esplicita del disaccordo con Wadoux et al. Gli embedding ereditano i bias dell'immagine: per esempio, la qualità percepita correla con il reddito.
- **[ipotesi]** Il problema emerso nella revisione (stime di domanda come artefatti di dati grossolani) è un caso del "modifiable areal unit problem" e del cambio di supporto. Le stesse cautele valgono per i punteggi di accessibilità calcolati su sezioni censuarie.

### Gaps
- Non trovato uno studio europeo revisionato di localizzazione di housing sociale o affordable che combini GIS-MCDA, incertezza (SMAA o Monte Carlo) e validazione ex post. Da cercare su Land Use Policy, CEUS, EPB con "social housing" e "site suitability". Non trovato nulla su Milano o sull'Italia in questa sessione.
- GNN su particelle catastali per idoneità residenziale: nessun paper specifico trovato. Zheng et al. lavora su grafi di contiguità di comunità, non su particelle catastali.
- Non verificato il full text di nessuno studio sugli embedding: le metriche riportate restano da controllare.

## 2. Misure di accessibilità (2SFCA/E2SFCA, città dei 15 minuti) e uso nella localizzazione residenziale

### Takeaway
2SFCA ed E2SFCA sono misure di accessibilità "offerta/domanda" con competizione. Sono preferibili alla semplice prossimità quando i servizi hanno capacità limitata (scuole, medici). Le metriche "15 minuti" basate su prossimità ignorano la capacità e, secondo dati di mobilità reali, descrivono male il comportamento effettivo.

### Cited Findings
- Luo & Wang (2003), Environment and Planning B 30:865–884, doi:10.1068/b29120: introducono il 2SFCA. Passo 1: per ogni servizio, il rapporto tra offerta e popolazione nel suo bacino. Passo 2: per ogni luogo di domanda, la somma dei rapporti dei servizi raggiungibili. Le fonti riportano titoli diversi per il paper del 2003: controllare il titolo sul DOI. [ver. per DOI/pagine] — [Wikipedia (con riferimenti)](https://en.wikipedia.org/wiki/Two-step_floating_catchment_area_method)
- Luo & Qi (2009), Health & Place 15(4):1100–1107, doi:10.1016/j.healthplace.2009.06.002: E2SFCA, con decadimento della distanza a fasce dentro il bacino. Varianti successive aggiungono bacini variabili e altre funzioni di decadimento. [ver.] — [Wikipedia](https://en.wikipedia.org/wiki/Two-step_floating_catchment_area_method); [IJHG 2012](https://link.springer.com/article/10.1186/1476-072X-11-50)
- Abbiasov et al. (2024), Nature Human Behaviour 8(3):445–455, doi:10.1038/s41562-023-01770-y. Dati GPS di 40 milioni di dispositivi USA. Il residente mediano fa solo il 14% dei viaggi di consumo entro 15 minuti a piedi. L'offerta locale di servizi spiega l'84% della variazione tra aree urbane e il 74% di quella interna alle aree. Un maggiore uso locale correla con una maggiore segregazione sperimentata dai residenti a basso reddito. [ver.] — [MIT Senseable PDF](https://senseable.mit.edu/papers/pdf/20240205_Abbiasov-etal_15-minuteCity_NatureHB.pdf); [RePEc](https://ideas.repec.org/a/nat/nathum/v8y2024i3d10.1038_s41562-023-01770-y.html)
- Moreno et al. (2021), "Introducing the 15-Minute City", Smart Cities 4(1):93–111, doi:10.3390/smartcities4010006: proposta concettuale. [non ver. in sessione, da memoria]

### Inferences
- **[inferenza]** Per Milano, un E2SFCA su servizi con capacità (posti nido e scuola, medici di base) sui lotti candidati è più difendibile di un conteggio di POI entro un raggio. La domanda nel denominatore va però stimata a risoluzione adeguata: si ricade nel problema di dati grossolani già emerso.
- **[inferenza]** Il risultato di Abbiasov sulla segregazione è rilevante per la tesi: ottimizzare la prossimità può aumentare l'isolamento dei gruppi a basso reddito. È un argomento per abbinare all'accessibilità una metrica di esposizione o mescolanza (audit di segregazione).

### Gaps
- Non trovati studi revisionati che usino esplicitamente 2SFCA come criterio di localizzazione di housing sociale (non solo di servizi sanitari). La ricerca andrebbe ripetuta su CEUS e J. Transport Geography.

## 3. Matching tra persone/gruppi e alloggi: teoria e applicazioni reali

### Takeaway
La teoria offre meccanismi con garanzie note: Deferred Acceptance per la stabilità, TTC e Random Serial Dictatorship per l'allocazione di case, Hylland–Zeckhauser per l'efficienza ex ante con lotterie. Esistono anche estensioni con vincoli distributivi e di diversità (Kamada–Kojima; riserve à la Hafalir–Yenmez–Yildirim). Le applicazioni reali più vicine sono il refugee matching (GeoMatch, Annie MOORE), che unisce ML predittivo e ottimizzazione intera, e il design delle liste d'attesa per le case popolari. In queste applicazioni la scelta degli assegnatari ha un valore economico misurabile.

### Cited Findings
**Teoria (classici)**
- Gale & Shapley (1962), "College Admissions and the Stability of Marriage", American Mathematical Monthly 69(1):9–15. [non ver. in sessione, da memoria]
- Shapley & Scarf (1974), "On cores and indivisibility", J. Math. Econ. 1(1):23–37: mercato di case e TTC (attribuito a Gale). [non ver. in sessione]
- Hylland & Zeckhauser (1979), "The Efficient Allocation of Individuals to Positions", JPE 87(2):293–314: pseudo-mercato con reddito fittizio uguale per tutti, per allocazioni probabilistiche efficienti. [non ver. in sessione]
- Abdulkadiroğlu & Sönmez (1999), "House allocation with existing tenants", JET 88(2):233–260, doi:10.1006/jeth.1999.2553. Nel modello un inquilino esistente che vuole spostarsi deve prima rinunciare alla propria casa. Gli autori propongono il meccanismo "you request my house – I get your turn". [ver.] — [Duke Scholars](https://scholars.duke.edu/publication/756540)
- Kamada & Kojima (2015), "Efficient Matching under Distributional Constraints: Theory and Applications", AER 105(1):67–99, doi:10.1257/aer.20101552. I meccanismi esistenti con tetti regionali soffrono di inefficienza e instabilità. Il meccanismo proposto migliora efficienza, stabilità e incentivi rispettando i vincoli. Seguono JET 2017 (concetti di stabilità con vincoli) e Theoretical Economics 2018 (condizione necessaria e sufficiente sulla struttura dei vincoli per avere un meccanismo stabile e strategy-proof). [ver.] — [IDEAS](https://ideas.repec.org/a/aea/aecrev/v105y2015i1p67-99.html); [TE 2018](https://www.econometricsociety.org/publications/theoretical-economics/2018/05/29/Stability-and-strategy-proofness-for-matching-with-constraints-a-necessary-and-sufficient-condition)
- Hafalir, Yenmez, Yildirim (2013), "Effective affirmative action in school choice", Theoretical Economics 8(2):325–363, doi:10.3982/TE1135. Le quote massime per la maggioranza possono danneggiare le minoranze stesse: nelle simulazioni fino al 25% delle minoranze e al 55% delle maggioranze stanno peggio. Le riserve per le minoranze con DA Pareto-dominano le quote. [ver.] — [Theoretical Economics](https://econtheory.org/ojs/index.php/te/article/viewArticle/20130325)
- Ehlers, Hafalir, Yenmez, Yildirim, "School choice with controlled choice constraints: hard bounds versus soft bounds" (JET 2014). [non ver. in sessione]

**Applicazioni: rifugiati**
- Bansak et al. (2018), "Improving refugee integration through data-driven algorithmic assignment", Science 359:325–329, doi:10.1126/science.aao4408 (Immigration Policy Lab, Stanford/ETH). Combina ML supervisionato, che predice la probabilità di impiego per ogni coppia famiglia–località, con assegnazione ottima sotto vincoli di capacità. Stima controfattuale su dati storici: occupazione +~40% negli USA e +~75% in Svizzera. Sono stime retrospettive, non effetti misurati in esercizio. [ver.] — [Immigration Policy Lab](https://immigrationlab.org/?p=4447); [LSE eprints](https://eprints.lse.ac.uk/107039)
- Rivalutazione 2026 dei risultati USA con off-policy evaluation, da parte di alcuni degli stessi autori. [non ver., non letto] — [arXiv 2605.06686](https://arxiv.org/html/2605.06686)
- Ahani, Andersson, Martinello, Teytelboym, Trapp (2021), "Placement Optimization in Refugee Resettlement", Operations Research 69(5):1468–1486, doi:10.1287/opre.2020.2093. Annie MOORE per l'agenzia HIAS: ML con ottimizzazione intera, decisione finale allo staff. Nel backtest sui reinsediamenti HIAS 2017, impiego +22–38% a seconda dei vincoli. In uso presso HIAS dal 2018. [ver.] — [ORA Oxford](https://ora.ox.ac.uk/objects/uuid:ac6d7b8d-203e-4fd8-9bb7-cf9f8735bb87); [WP Lund](https://lup.lub.lu.se/search/files/194855430/WP18_23.pdf); [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/opre.2020.2093)

**Applicazioni: case popolari e liste d'attesa**
- Waldinger (2021), "Targeting In-Kind Transfers through Market Design: A Revealed Preference Analysis of Public Housing Allocation", AER 111(8):2660–2696, dati di Cambridge (MA). Eliminare la scelta migliorerebbe il targeting ma ridurrebbe il benessere degli inquilini di oltre il 30%. Dare priorità ai redditi bassi mantenendo la scelta migliora il targeting senza peggiorare la qualità del match. [ver.] — [RePEc](https://econpapers.repec.org/RePEc:aea:aecrev:v:111:y:2021:i:8:p:2660-96); [JMP](https://economics.sas.upenn.edu/sites/default/files/filevault/event_papers/WaldingerJMP.pdf)
- Thakral, "The Public-Housing Allocation Problem: Theory and Evidence from Pittsburgh": unità che arrivano nel tempo, assegnate a una lista d'attesa. Senza trasferimenti monetari si ottiene equità d'accesso ma possibile inefficienza. [sede di pubblicazione non ver.] — [NBER conf paper](https://conference.nber.org/conf_papers/f129857.pdf)
- Arnosti & Shi, "Design of Lotteries and Waitlists for Affordable Housing Allocation" (Management Science 2020 [anno e sede non ver.]). Esiste un compromesso tra matching e targeting: la lotteria comune dà un matching quasi ottimo, i costi di partecipazione un targeting quasi ottimo. — [SSRN](https://papers.ssrn.com/abstract=2963178)
- Edilizia sociale francese: una tesi del 2024 conclude che i meccanismi basati solo sull'anzianità di attesa riducono il benessere. [non ver.] — [Toulouse Capitole](https://publications.ut-capitole.fr/53227/1/BotbolLisa2024.pdf)

### Inferences
- **[inferenza]** Il passo (3) "i gruppi scelgono tra i lotti" è formalmente un problema di house allocation o many-to-one con preferenze dei gruppi e capacità dei lotti (1 gruppo per lotto o più gruppi per lotto). Se l'ente pubblico ha priorità sui lotti (punteggi di bisogno), il quadro naturale è DA con vincoli distributivi (Kamada–Kojima), con riserve (HYY 2013) per garantire mescolanza tra quartieri. Se non ci sono priorità, servono RSD/TTC o Hylland–Zeckhauser.
- **[inferenza]** Il modello GeoMatch/Annie MOORE (predizione di esiti più assegnazione ottima) si traspone a "gruppo–lotto", ma richiede dati di esito osservati, che per Milano non esistono. Con dati storici assenti, la parte predittiva diventa un'ipotesi e va dichiarata come tale.
- **[inferenza]** Waldinger fornisce un argomento empirico forte per la tesi: la scelta degli assegnatari ha valore, e toglierla per migliorare il targeting costa benessere. È un'evidenza a favore di meccanismi con preferenze espresse rispetto all'assegnazione dall'alto.

### Gaps
- Classici Gale–Shapley, Shapley–Scarf, Hylland–Zeckhauser e Ehlers et al. 2014: metadati da memoria, non riverificati in sessione.
- Non trovate applicazioni di matching a gruppi di co-housing o a lotti edificabili (non alloggi esistenti). Sembra uno spazio libero in letteratura [ipotesi da verificare].
- Non esaminata la letteratura sui sistemi di assegnazione dell'ERP in Italia o in Lombardia.

## 4. Formazione di gruppi/coalizioni con diversità

### Takeaway
Tre filoni formalizzano la "mescolanza deliberata". I giochi edonici di diversità (stabilità con preferenze sulla composizione del gruppo) hanno problemi di esistenza e complessità del core. Il fair clustering (vincoli di rappresentanza proporzionale per cluster) si risolve con fairlet e min-cost flow. La team formation con vincoli o obiettivi di diversità usa massimizzazione submodulare, ILP e ricerca multi-obiettivo. La prassi del co-housing, invece, mostra che i gruppi reali si formano per auto-selezione e in tempi lunghi.

### Cited Findings
- Chierichetti, Kumar, Lattanzi, Vassilvitskii (2017), "Fair Clustering Through Fairlets", NeurIPS 2017. Il vincolo è che ogni classe protetta sia rappresentata in modo circa proporzionale in ogni cluster. Il problema si scompone in "trovare fairlet" (piccoli insiemi bilanciati) e poi applicare il clustering classico. Trovare fairlet ottimi può essere NP-hard: si usano approssimazioni via min-cost flow. Gli autori quantificano il "prezzo della fairness". Le pagine differiscono tra le fonti (5029–5037 o 5036–5044). [ver.] — [NeurIPS proceedings PDF](https://proceedings.neurips.cc/paper_files/paper/2017/file/978fce5bcc4eccc88ad48ce3914124a2-Paper.pdf); [arXiv 1802.05733](https://arxiv.org/abs/1802.05733v1)
- Bredereck, Elkind, Igarashi (2019), "Hedonic Diversity Games", AAMAS 2019. Due tipi di agenti, ciascuno con preferenze sulla frazione del proprio tipo nel gruppo; a differenza di Schelling, alcuni agenti possono preferire gruppi misti. Il core può non esistere e verificarne l'esistenza è computazionalmente difficile. Un esito individualmente stabile si trova in tempo polinomiale con preferenze single-peaked. Estensioni: Boehmer & Elkind (AAAI 2020). [ver.] — [AAMAS PDF](https://ifmas.csc.liv.ac.uk/Proceedings/aamas2019/pdfs/p565.pdf); [arXiv 1903.00303](https://www.arxiv.org/abs/1903.00303?context=cs); [AAAI 2020](https://ojs.aaai.org/index.php/AAAI/article/view/5549/5405)
- Ahmed, Dickerson, Fuge (2020), "Forming Diverse Teams from Sequentially Arriving People". Obiettivo monotono submodulare che combina diversità e qualità, con più vincoli e più attributi, e quantifica il costo della diversità. [non ver. oltre l'abstract] — [arXiv 2002.10697](https://arxiv.org/pdf/2002.10697)
- Fair team formation (WWW 2019): team di costo minimo che copre le competenze con numero uguale di membri da due classi. [non ver.] — [arXiv 2011.11611 / FERN](https://arxiv.org/abs/2011.11611)
- Diverse group formation con più attributi demografici. [non ver.] — [arXiv 2008.03808](https://arxiv.org/pdf/2008.03808)
- Prassi co-housing: Fernández Arrigoitia & Scanlon, "Of flux or finality? On the process and dynamics of a cohousing group in formation" (LSE, 2017) [sede non ver.]. — [LSE](https://researchonline.lse.ac.uk/id/eprint/87089)
- Centraal Wonen (NL), progetti 1977–1986: la composizione sociale dei gruppi è l'esito di un processo di auto-selezione. [non ver.] — [AGRIS](https://agris.fao.org/search/en/records/64746aa0bf943c8c797ffa11)
- Caso Cohaus (Nuova Zelanda): la formazione del gruppo allargato ha richiesto circa 18 mesi e i membri la indicano come critica per l'esito. È una fonte divulgativa di settore. — [Architecture Now](https://architecturenow.co.nz/articles/deconstructing-the-cohaus-journey-key-findings/)

### Inferences
- **[inferenza]** Il requisito "gruppi eterogenei, NON per somiglianza" corrisponde quasi alla lettera al vincolo di fair clustering (rappresentanza per cluster) o a un ILP di partizione con vincoli di composizione minima e massima per attributo (età, condizione). Il fair clustering però minimizza ancora la distanza intra-cluster: senza un'attenta scelta della metrica rischia di reintrodurre omogeneità sulle variabili non protette.
- **[inferenza]** I giochi edonici di diversità mostrano che un gruppo eterogeneo imposto dall'algoritmo può non essere stabile: i membri potrebbero voler deviare. Proporre gruppi va quindi distinto da come i gruppi tengono. La prassi co-housing (auto-selezione, mesi o anni) suggerisce di usare l'algoritmo per proporre composizioni e non per assegnarle.
- **[ipotesi]** Un formato ibrido: l'algoritmo propone k partizioni ammissibili e diverse, le famiglie esprimono preferenze e un meccanismo di stabilità individuale o di matching finalizza. Va testato per simulazione, non dimostrato.

### Gaps
- Non trovata letteratura revisionata su algoritmi applicati alla formazione di gruppi di co-housing o Baugemeinschaften. Non cercato in tedesco o in italiano.
- Non verificato se esistano studi empirici sulla durata o sul fallimento di gruppi co-housing intenzionalmente misti, contrapposti a quelli auto-selezionati.

## 5. Modelli ad agenti del mercato abitativo e della segregazione; RL multi-agente nella pianificazione

### Takeaway
Schelling è il baseline canonico per mostrare che preferenze lievi producono segregazione forte. Gli ABM di mercato abitativo calibrati su microdati (Bank of England) sono maturi per le politiche macroprudenziali, meno per la scala del lotto. DRL e GNN nella pianificazione sono frontiera recente, ottimizzano metriche definite dal modellatore e restano da validare sul piano partecipativo.

### Cited Findings
- Schelling (1971), "Dynamic models of segregation", J. Math. Sociology 1(2):143–186. [non ver. in sessione]
- Baptista, Farmer, Hinterschweiger, Low, Tang, Uluc (2016), "Macroprudential policy in an agent-based model of the UK housing market", Bank of England Staff WP 619. Agenti eterogenei (primo acquisto, proprietari, buy-to-let, affittuari) calibrati su microdati. Un settore buy-to-let più grande amplifica cicli e volatilità dei prezzi; un limite al rapporto loan-to-income li attenua. Esteso da Carro et al., Banco de España WP 2217 (2022). [ver.] — [Bank of England](https://www.bankofengland.co.uk/working-paper/2016/macroprudential-policy-in-an-agent-based-model-of-the-uk-housing-market); [Banco de España](https://repositorio.bde.es/bitstream/123456789/21082/1/dt2217e.pdf)
- Zheng et al. (2023), Nature Computational Science (vedi §1): DRL su grafo con workflow uomo–IA, in cui i progettisti generano piani più efficienti in molto meno tempo. [ver.] — [Nature](https://www.nature.com/articles/s43588-023-00503-5)
- Preprint 2026 con RL multi-obiettivo per la selezione di siti affordable sotto vincoli normativi. [non ver.] — [arXiv 2602.03940](https://arxiv.org/pdf/2602.03940)

### Inferences
- **[inferenza]** Per la tesi, un ABM tipo Schelling serve come simulatore controfattuale per l'audit di segregazione: i gruppi misti assegnati ai lotti si dissolvono, cioè si ri-segregano, sotto preferenze di trasferimento plausibili? Non serve a stimare la domanda. Un ABM di mercato tipo Baptista richiederebbe microdati di transazione per Milano (OMI ha solo quotazioni per zona) ed è probabilmente fuori scala per una tesi magistrale.
- **[inferenza]** Il RL nella pianificazione (Zheng 2023) ottimizza una ricompensa scelta dal modellatore. È coerente con l'approccio "cibernetico" della tesi solo se la funzione di ricompensa viene resa oggetto di deliberazione, non nascosta.

### Gaps
- Non cercate in questa sessione rassegne aggiornate su ABM di segregazione (es. Benenson, Crooks/Heppenstall, CASA) né lavori di MARL multi-agente in senso stretto per la pianificazione urbana. Lacuna da colmare.
- Nessun ABM su Milano trovato o cercato.
