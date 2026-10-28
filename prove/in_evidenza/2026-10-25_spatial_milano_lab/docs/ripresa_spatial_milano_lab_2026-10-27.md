# Ripresa del lavoro: sessione "Riprogettazione con design sync" (Spatial Milano Lab)

Fonte: trascrizione della sessione `session_01MJjd6gJAUPJRfeZPBRhiPW` (letta tramite list_events, solo messaggi utente, assistente e risultati), più `istruzioni_progetto_tesi.md` e `stato_avanzamento.md`.
Limiti di lettura: ho letto per intero il riassunto di compattazione e le ultime due pagine di eventi (circa 200 eventi). Un'ultima pagina più vecchia (prima del riassunto) non l'ho aperta: la cronologia iniziale la ricostruisco solo dal riassunto. Alcune risposte dell'assistente nella trascrizione sono troncate. I file citati stanno sul PC di Dennis (cartella di scratch della sessione), non li ho aperti. Etichette: **[S]** risulta dalla sessione, **[I]** inferenza mia.

## 1. Cosa stava facendo
- **[S]** Costruire una piattaforma stile SPATIAL / ZHA Digital Planning Hub (mappa scura, chat LLM a destra, dashboard) con dati reali: prima Monza e Brianza, poi solo il Comune di Milano (88 NIL, PGT, DUSAF, DBT 2020 con altezze, catasto, redditi, affitti OMI), con edifici e lotti in 3D.
- **[S]** Obiettivo dichiarato da Dennis: strumento per trovare più aree candidate al social housing (la "pancia della gaussiana" di Sanchez, *Architecture for the Commons*), che persone e Comune confrontano pesando i fattori in base ai bisogni reali. Idea guida: cibernetica e partecipazione.
- **[S]** Modello base protetto: `mi/` e l'artifact "Spatial Milano" (GaPJf4tLYL8WZTkokBZkMn). Non va mai modificato; ogni prototipo è separato.
- **[S]** Ultima richiesta: un team di ricerca di livello dottorale (agenti che si revisionano a vicenda) per scoprire e testare modelli matematici, economici o di ML. Poi Dennis ha precisato: non il "lotto migliore", ma più portafogli di lotti tra cui scelgono le persone; e la domanda centrale è se le aree del PGT, confrontate con i bisogni reali, creino segregazione o abbiano potenziale. Ha chiesto anche di valutare il reale potere d'acquisto a Milano.

## 2. Cosa è stato completato
- **Tabella dei lotti**: `lab/data/parcels.csv.gz` (119.352 particelle, 78 colonne) e `nil.csv`.
- **Tre proposte** in `lab/proposals/`: A economia e ricerca operativa (domanda, portafogli MILP), B scienza delle decisioni (SMAA, domande a coppie, consenso), C ML e spaziale (accessibilità E2SFCA, rilevatore di lotti da rigenerare con validazione a blocchi spaziali). Riepilogo di A in `lab/proposals/A_econ_or/summary.md`.
- **Revisione 1** (`lab/reviews/review1.md`) e **revisione 2** (`review2.md`, esito "accettato con revisioni importanti"). Modello integrato in `lab/model/` (`run.py`, `tests.py`, `results.md`, `model.json`), 17 test superati, esecuzione circa 23 minuti.
- **Prototipo** `lab/prototype/` e artifact separato **Spatial Milano Lab**: https://claude.ai/artifact/LHHSCseATyEEmS4g7SoTW5 (scene "Laboratorio" e "Potere d'acquisto", portafogli P1–P6, schede "PGT contro persone", ciclo "Il tuo voto").
- **Paper in italiano**: `lab/results/paper.md`.
- Altri artifact della sessione: "Spatial agent prototipo" (Monza) e "Spatial Milano" (base).

## 3. Risultati principali (tutti da trattare come ipotesi di lavoro, non fonti)
- **Dati PGT**: `pgt_dism` e `pgt_rig` quasi coincidenti (r = 0,998); gli ambiti di trasformazione sono in gran parte Parchi della Campagna Urbana. Esclusi dai candidati. La regola "soft site" originale è pari al caso.
- **Validazione**: PR-AUC 0,93 con validazione casuale, 0,33 con blocchi di 4 km.
- **Domanda**: la domanda stimata di A coincideva con la mappa degli affitti (ρ = 0,987), un artefatto di risoluzione (redditi su 38 CAP, affitti su 88 NIL). Famiglie in difficoltà: 9.259 con regola affitto oltre il 30%, 2.274 con paniere "dignitoso" (1,5 volte ISTAT, ipotesi), 102 con minimo ISTAT. Lettura: ceto schiacciato dall'affitto, non povero. Il 37–38% di "ceto medio escluso" citato dall'ANSA non è stato riprodotto.
- **PGT contro persone** (dopo la revisione 2):
  - Ambiti di trasformazione: più poveri (reddito residuo −92 €/mese contro −22/−38 di lotti equivalenti) ma nessun rischio di segregazione dimostrato; vale a livello di lotto, non confrontando NIL interi; dipende molto da un solo NIL (Stephenson).
  - Aree ERP: convenienti solo se il terreno è gratuito (non verificato).
  - Aree degradate: nessuna informazione (5 siti).
  - Ambiti di rigenerazione: il segnale più solido (53 NIL, p ≈ 0,001).
  - Persone contro PGT: +48% grezzo, +22% a parità di numero di siti, +5% a parità di distanza dal centro.
- **Metodo**: il confronto lotto per lotto dà falsi allarmi nel 24% dei casi se le aree sono concentrate in pochi NIL; il confronto a blocchi solo nello 0,3%.
- **Portafogli** P1–P6: praticamente equivalenti (1.781–1.795 famiglie servite); la scelta spetta alle persone.
- Tutte le preferenze dei cittadini negli esperimenti sono sintetiche.

## 4. Cosa resta da fare
- Verificare la chat LLM nell'artifact pubblicato (non provata) e il layout mobile.
- Leggere `paper.md` e le due revisioni; la revisione 2 ha segnalato che i cinque indicatori di segregazione vengono da una sola fonte (CAP).
- Sette decisioni aperte (**[S]** dal riassunto): gruppo target (ERP o fascia esclusa), di chi sono i pesi, impegno del Comune, unità spaziale, alloggi ERP vuoti, piattaforma autonoma o Decidim, verifica della "gaussiana" in Sanchez (non trovata nei testi accessibili).
- Dati da verificare: proprietà dei terreni ERP, inflazione di Milano 2019–2025 (usata la serie nazionale), redditi 2019, soglia di affitto sostenibile (scelta politica).
- Eventuale aggancio alla tesi: AI Act (graduare i lotti è ammesso, punteggi di idoneità delle famiglie sono ad alto rischio, Annex III 5a).
- Avvisi tecnici: i riepiloghi dei sottoagenti non potevano scrivere file (alcuni `summary.md` sono stati scritti dalla sessione principale); il servizio claude-mem della sessione non salva memoria (credenziali scadute dal 2026-10-11).

## 5. Rapporto con la tesi (inferenza)
- **[I]** Questo filone è la Fase 3 (sperimentazione) applicata a Milano. `stato_avanzamento.md` (ultima voce 2026-10-25) **non** lo registra: manca una voce su laboratorio, revisioni, risultati e artifact. In `tesi_handoff/` e `abitare-cinisello/` risultano file collegati (pipeline Milano, valutazione Spatial Milano, tavola rotonda) che non ho aperto.
- **[I]** Regola di progetto: ogni dato citato nel Report fondativo va distinto tra dichiarato, inferito e ipotesi. Qui quasi tutto è output di modelli su dati non verificati e preferenze sintetiche.
- **[I]** Lo stato dice che il Report fondativo è l'obiettivo della fase attuale, mentre questo lavoro è sperimentale: va deciso come si colloca.
