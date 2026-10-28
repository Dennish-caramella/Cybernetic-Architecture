# Lettura critica dei documenti di Fase 1 (Milano)

**Data:** 2026-10-21
**Documenti letti:** `ORCHESTRATORE_FASE_1_MILANO.md`, `PIPELINE_FASE_1_DIGITAL_TWIN_MILANO.md` (copie in `05_Urbanistica/` e in `00_Avanzamento/02_sintesi/`), `GRAPH_REPORT.md` aggiornato.
**Marche:** [S] riportato dai documenti, [I] mia inferenza, [L] lacuna o da verificare.

## 1. Che cosa sono i nuovi file

- **Orchestratore:** specifica tecnica a moduli 0–6: dati su griglia esagonale H3, PCA, K-Means in tre classi di lotto, isocrone e indice PAI, valutazione multicriterio con pesi negoziabili, validazione con agenti LLM, dashboard CesiumJS. [S]
- **Pipeline:** stessa idea in sette passi, con in più il bilancio finanziario con sussidiazione incrociata (60/15/15/10), l'arbitro di Pareto con agenti LLM locali (Ollama), e un catalogo di librerie. [S]
- **`05_Urbanistica/00_Metadati/`** è vuota. Nessuno script citato nella struttura dei file esiste ancora. [S]
- **Il grafo** è stato rigenerato il 2026-10-20: 38 file, 507 nodi, 677 archi. Non modificato da me.

## 2. Che cosa regge

- La scelta del lotto passa da una valutazione multicriterio con vincoli rigidi e pesi esposti. Risponde alla mia riserva: il cluster non basta, servono criteri dichiarati. [I]
- La domanda abitativa è definita con un target di canone e un'aritmetica coerente (7,5–8,5 €/m²/mese su 75 m² dà 560–640 €/mese). [S]
- L'uso di H3 risolve il problema pratico dei confini diversi tra dataset. Le aree medie delle celle (0,737 km² a livello 8, 0,105 km² a livello 9) sono quelle standard di H3. [I, da riverificare sulla documentazione]

## 3. Problemi da correggere (in ordine di gravità)

1. **Risultati scritti prima dell'analisi.** Le tre classi A, B, C, la varianza spiegata dalle prime tre componenti (">75%" in un file, ">80%" nell'altro) e gli "esempi di lotti" (Scalo Farini est, Rogoredo, Giambellino e altri) sono presentati come esiti. Nessun dato è stato elaborato. K-Means su tre componenti di mercato, accessibilità e suolo non può scoprire "studentati" o "co-housing": le etichette sono imposte dopo. K=3 è fissato in anticipo, poi "validato". Va riscritto come ipotesi da verificare, con K deciso dai dati.
2. **Doppio conteggio.** Rent gap e PAI entrano sia nella PCA e nel clustering sia nella formula di idoneità. Il termine "Classe_Lotto" è una variabile nominale moltiplicata per un peso: serve una codifica numerica dichiarata.
3. **Gli agenti LLM spostano i pesi.** Nel prompt di esempio l'agente "propone una variazione sui pesi". Se un modello muove i pesi, il potere sui criteri passa al modello, il contrario dell'ipotesi H2 della tesi. Inoltre 1.000 persone sintetiche generate da un LLM non misurano preferenze reali: sono scenario, non evidenza (rischio 2 del Report). Il test di solvibilità è aritmetica e non richiede un LLM.
4. **Pareto definito sui pesi.** Il paragrafo 5.4 definisce l'ottimo sui vettori di pesi. La frontiera di Pareto si calcola sulle alternative (lotto, mix, tipologia), non sui pesi. L'espressione "massimizzare il benessere collettivo" richiede una funzione di aggregazione: è una scelta politica, e il documento non la discute. [L: teoria della scelta sociale]
5. **Attribuzione errata.** "Protocollo T1 di Alexander" e "Slider Negoziabili T1 (Alexander)": T1 è il protocollo di test di questo progetto, non un'opera di Alexander.
6. **Fonti non verificabili.** ZHA "Benghazi 2050 Digital Planning Hub", l'account Instagram `zha.world`, un video YouTube per MIT City Science e il dato di 22.417 edifici non compaiono in nessuna analisi del corpus, e Systematica, accessX, H3, 2SFCA non compaiono in nessuna delle 36 analisi. Una tesi non può citare un account social come fonte. Serve la pubblicazione ufficiale, o la rimozione. [L]
7. **Numeri senza fonte.** Soglie ISEE per ERP, reddito 24.000–45.000 €, canone libero oltre 20 €/m²/mese, soglia di 220 €/m²/anno, sconto "fino all'80%" sugli oneri, ripartizione 60/15/15/10. Tutti da verificare e datare. [L]
8. **Definizioni incoerenti.** (a) PAI: nell'Orchestratore è una somma di soglie su 6 servizi (con scala 0–5, ma sei servizi danno 0–6); nella Pipeline è un indice 2SFCA. (b) "Rent gap": nell'Orchestratore è il divario tra canone di mercato e canone sostenibile; nella Pipeline è il rent gap di Smith, un concetto diverso (rendita del suolo). (c) Velocità pedonale: 6 km/h (Tobler) in un file, 4,5 km/h nell'altro. (d) Le misure delle celle H3 sono chiamate diametro in un file e raggio dell'apotema nell'altro.
9. **MAUP non risolto.** H3 elimina l'effetto dei confini amministrativi, non il problema dell'unità di analisi: cambiare risoluzione cambia i risultati, e portare dati da poligoni a celle richiede un'interpolazione che introduce errore. Serve un test di sensibilità tra livello 8 e 9. Inoltre una cella di livello 9 (circa 10 ettari) non è un lotto: la scelta del lotto richiede dati di particella.
10. **Ordine delle priorità.** Avevi detto: prima verificare che il cuore (il gioco) funzioni, poi ingegnerizzare. Questi file mettono per primi dashboard 3D e slider temporale 2024–2050, senza un modello dell'evoluzione nel tempo. Il cuore, T1, entra solo come modulo di pesi.
11. **Dati.** Quotazioni OMI sono intervalli stimati, non transazioni. Il reddito IRPEF potrebbe non esistere alla granularità dei NIL o delle sezioni. Costi di costruzione e di suolo non sono nei dataset. Il bilancio con "ROI e breakeven" è promesso e non calcolato. [L]
12. **Hardware.** Un modello da 3B parametri per "calcoli quantitativi" e output JSON rigoroso è una scelta debole: serve validazione dell'output, non fiducia.

## 4. Proposta di ordine di lavoro

1. Chiudere le definizioni (PAI, rent gap, velocità, K) e le fonti dei numeri, in un glossario unico.
2. Fare l'analisi urbana come esplorazione: PCA e clustering con K deciso dai dati, stabilità dei cluster, test di sensibilità sulla risoluzione.
3. Fare la valutazione multicriterio con pesi modificati da persone, non dal modello.
4. Spostare gli agenti LLM da validatori a strumento di elicitazione, e dichiararli come scenario.
5. Solo dopo, dashboard e bilancio finanziario.

Questa lettura è mia. Le decisioni di direzione restano tue.

## 5. Addendum 2026-10-21 (terzo file: MODELLI_ZHA_E_MIT_ANALISI_COMPARATIVA.md)

Il file esiste in tre copie (`01_Ricerche Teoriche/`, `05_Urbanistica/`, `00_Avanzamento/02_sintesi/`). Confronta due modelli e li usa come base della tesi.

- **Descrive ZHA/Systematica e MIT City Science come fatti, con dettagli specifici** (22.417 edifici, "Dynamic Detours", arbitrato di Pareto automatico, willingness-to-pay stimata dal LLM). Nessuno di questi dettagli è verificabile dal corpus; la sola fonte indicata è un canale social e una conferenza. Finché non c'è un riferimento pubblicato, vanno trattati come descrizione non verificata [L], e il confronto "ZHA vs MIT" come ipotesi di lavoro.
- **Il "contributo originale" contiene numeri senza fonte**: costo 1.450 €/m², sconto oneri del 80%, breakeven 92 €, ripartizione 60/15/15/10, "norme ERS del PGT di Milano". Da verificare e datare [L]. Il breakeven non è calcolato in nessun file.
- **Il mock-up descritto mostra valori** (Lotto #014, PAI 4,4/5,0, pesi 35/25/25/15) che sono dimostrativi: se compaiono in un prototipo, vanno marcati come dati finti.
- **Nella barra del prototipo compare "Brand ZHA x POLIMI"** e il documento si firma "Politecnico di Milano". Implica una collaborazione con ZHA e un'affiliazione che il materiale non documenta. Va tolto o reso esplicito che è solo un riferimento di stile.
- **Il prototipo `milano_digital_planning_hub.html` è citato ma non l'ho trovato** nella scansione della cartella.
- **Restano gli errori già segnalati**: "Protocollo T1 di Alexander", cella H3 di livello 9 definita "scala del lotto" mentre ha circa 10 ettari, il MAUP dichiarato risolto, e gli agenti che muovono i pesi (qui con "Arbitrato di Pareto Automatico" che "ricalibra l'assetto ottimo collettivo").
- **Incoerenza nuova**: il PAI qui è un indice 0–5 su rapporto capacità/popolazione (2SFCA), cioè la terza definizione dopo le due già segnalate.
